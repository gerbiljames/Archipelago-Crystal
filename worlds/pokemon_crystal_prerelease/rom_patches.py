from dataclasses import dataclass

from .utils import convert_to_ingame_text


@dataclass
class RomPatchEntry:
    bank: int
    address: int
    data: list[int]

    @property
    def rom_offset(self) -> int:
        if self.bank == 0:
            return self.address
        return (self.bank * 0x4000) + (self.address - 0x4000)


@dataclass
class RomPatch:
    name: str
    entries: list[RomPatchEntry]


ROM_PATCHES: list[RomPatch] = [
    # QwilfishText in fish.asm is missing its "@" terminator. The byte after the string is the
    # FishGroups chance byte which gets randomized per-seed, so the string reads into garbage.
    # Fix: write a terminated copy to free space at end of bank 0x24, update all 3 pointers.
    RomPatch("Fix QwilfishText missing terminator", [
        RomPatchEntry(bank=0x24, address=0x7E8E,
                      data=convert_to_ingame_text("ROUTES 12, 13, 32", string_terminator=True)),
        RomPatchEntry(bank=0x24, address=0x67CF, data=[0x8E, 0x7E]),
        RomPatchEntry(bank=0x24, address=0x681C, data=[0x8E, 0x7E]),
        RomPatchEntry(bank=0x24, address=0x686A, data=[0x8E, 0x7E]),
    ]),
    # The Pokecenter 2F battle sets wCatchDisabled and checks it at .can_escape to guarantee
    # fleeing. But three checks happen before .can_escape: Mean Look (SUBSTATUS_CANT_RUN),
    # trapping moves (wPlayerWrapCount), and the speed-based flee RNG (.cant_escape_2).
    # Fix: insert wCatchDisabled check inline at 0f:585E (right after the trainer battle check),
    # before all escape-prevention logic. Relocate original checks to trampoline in free space.
    RomPatch("Fix Pokecenter 2F battle flee with trapping moves", [
        # Inline wCatchDisabled check at 0f:585E, replacing the original 15 bytes of
        # SUBSTATUS_CANT_RUN + wPlayerWrapCount checks (relocated to trampoline)
        RomPatchEntry(bank=0x0F, address=0x585E, data=[
            0xFA, 0x5F, 0xD2,  # ld a, [wCatchDisabled]
            0xA7,               # and a
            0xC2, 0x47, 0x59,   # jp nz, .got_away_safely
            0xC3, 0xD9, 0x7F,   # jp trampoline
            0x00, 0x00, 0x00, 0x00, 0x00,  # nop padding (unreachable)
        ]),
        # Trampoline in free space at end of bank 0x0F: original checks then continue
        RomPatchEntry(bank=0x0F, address=0x7FD9, data=[
            0xFA, 0x71, 0xC6,  # ld a, [wEnemySubStatus5]
            0xCB, 0x7F,        # bit 7, a  (SUBSTATUS_CANT_RUN)
            0xC2, 0x09, 0x59,  # jp nz, .cant_escape
            0xFA, 0x30, 0xC7,  # ld a, [wPlayerWrapCount]
            0xA7,              # and a
            0xC2, 0x09, 0x59,  # jp nz, .cant_escape
            0xC3, 0x6D, 0x58,  # jp 586D (continue to flee item check)
        ]),
    ]),
]
