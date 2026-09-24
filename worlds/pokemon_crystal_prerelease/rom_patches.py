from dataclasses import dataclass


@dataclass
class RomPatchEntry:
    bank: int
    address: int
    data: list[int]
    # only write if the ROM currently holds these bytes (overrides apply after token writes)
    expected: list[int] | None = None

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
    # Receiving a time of day item only forces the time when the player has the Pokegear to change it back
    RomPatch(
        name="tod_item_force_requires_pokegear",
        entries=[
            # ReceiveFlagItem.tod_set (43:54d0): ld a, [wArchipelagoFlagItemId] -> call $7f80
            RomPatchEntry(bank=0x43, address=0x54D0, data=[0xCD, 0x80, 0x7F]),
            # Stub in bank $43 end-of-bank free space ($7289-$7fff)
            RomPatchEntry(bank=0x43, address=0x7F80, data=[
                0xFA, 0x19, 0xDA,  # ld a, [wPokegearFlags]
                0xCB, 0x7F,        # bit POKEGEAR_OBTAINED_F, a
                0x28, 0x04,        # jr z, .no_pokegear
                0xFA, 0xEA, 0xD6,  # ld a, [wArchipelagoFlagItemId] ; overwritten
                0xC9,              # ret
                0xE1,              # .no_pokegear: pop hl ; return from .tod_pokemon
                0xC9,              # ret
            ]),
        ],
    ),
    # With unlockable time of day on, the options menu time of day setting also requires the Pokegear
    RomPatch(
        name="options_tod_requires_pokegear",
        entries=[
            # Options_TimeOfDay (7d:6887): ld a, [wUnlockedTimeOfDay] -> call $7f80
            RomPatchEntry(bank=0x7D, address=0x6887, data=[0xCD, 0x80, 0x7F]),
            # Stub in bank $7d end-of-bank free space ($7547-$7fff); returns ANYTIME to unlock the setting
            RomPatchEntry(bank=0x7D, address=0x7F80, data=[
                0xFA, 0xEB, 0xD6,  # ld a, [wUnlockedTimeOfDay] ; overwritten
                0xFE, 0x07,        # cp ANYTIME
                0xC0,              # ret nz
                0xFA, 0x19, 0xDA,  # ld a, [wPokegearFlags]
                0xCB, 0x7F,        # bit POKEGEAR_OBTAINED_F, a
                0x3E, 0x07,        # ld a, ANYTIME
                0xC0,              # ret nz
                0xE5,              # push hl
                0x3E, 0x01,        # ld a, BANK(NewGame)
                0x21, 0x7E, 0x5D,  # ld hl, NewGame.AP_Setting_UnlockableTimeOfDay + 1 ; ANYTIME when the option is off
                0xCD, 0x66, 0x30,  # call GetFarByte
                0xE1,              # pop hl
                0xC9,              # ret
            ]),
        ],
    ),
]
