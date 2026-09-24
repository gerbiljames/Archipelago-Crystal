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
    # Fruit trees holding a remote item don't refill daily
    RomPatch(
        name="remote_fruit_trees_dont_reset",
        entries=[
            # ResetFruitTrees (11:40b3): xor a / ld hl, wFruitTreeFlags -> jp $7f80
            # skipped when randomize_berry_trees has already replaced it with ret
            RomPatchEntry(bank=0x11, address=0x40B3, data=[0xC3, 0x80, 0x7F],
                          expected=[0xAF, 0x21, 0x90, 0xDB]),
            # Stub in bank $11 end-of-bank free space ($5cfe-$7fff)
            RomPatchEntry(bank=0x11, address=0x7F80, data=[
                0x21, 0x90, 0xDB,  # ld hl, wFruitTreeFlags
                0x11, 0x37, 0x41,  # ld de, FruitTreeItems
                0x06, 0x20,        # ld b, NUM_FRUIT_TREES
                0x0E, 0x01,        # ld c, 1
                0x1A,              # .loop: ld a, [de]
                0x13,              # inc de
                0xFE, 0xC7,        # cp AP_ITEM
                0x28, 0x04,        # jr z, .keep
                0x79,              # ld a, c
                0x2F,              # cpl
                0xA6,              # and [hl]
                0x77,              # ld [hl], a
                0xCB, 0x01,        # .keep: rlc c
                0x30, 0x01,        # jr nc, .next
                0x23,              # inc hl
                0x05,              # .next: dec b
                0x20, 0xEE,        # jr nz, .loop
                0x21, 0x5B, 0xDC,  # ld hl, wDailyFlags1
                0xCB, 0xE6,        # set DAILYFLAGS1_ALL_FRUIT_TREES_F, [hl]
                0xC9,              # ret
            ]),
        ],
    ),
    # Game corner prize Pokemon only show the Pokedex entry when the player has the Pokedex
    RomPatch(
        name="game_corner_dex_entry_requires_pokedex",
        entries=[
            # GameCornerPrizeMonCheckDex (03:4260): ld a, [SKIP_DEX_REGISTRATION_ADDRESS] -> call $7f80
            RomPatchEntry(bank=0x03, address=0x4260, data=[0xCD, 0x80, 0x7F]),
            # Stub in bank $03 end-of-bank free space ($7e7a-$7fff); a = 1 makes the following bit check skip
            RomPatchEntry(bank=0x03, address=0x7F80, data=[
                0xCD, 0xBE, 0x2E,  # call CheckReceivedDex
                0x3E, 0x01,        # ld a, 1
                0xC8,              # ret z
                0xFA, 0xCD, 0xCF,  # ld a, [SKIP_DEX_REGISTRATION_ADDRESS] ; overwritten
                0xC9,              # ret
            ]),
        ],
    ),
    # wBattleTrapQueue ($d301) isn't page-aligned, so indexing via ld h/ld l started at $d300 inside wPCFlagItems
    RomPatch(
        name="battle_trap_queue_index",
        entries=[
            # EnqueueBattleTrap (43:6cb7): ld h, HIGH(wBattleTrapQueue) / ld l, c -> call $7f90
            RomPatchEntry(bank=0x43, address=0x6CB7, data=[0xCD, 0x90, 0x7F], expected=[0x26, 0xD3, 0x69]),
            # LoadIncomingBattleTrap.check_queue (43:6cff): ld h, HIGH(wBattleTrapQueue) / ld l, c -> call $7f90
            RomPatchEntry(bank=0x43, address=0x6CFF, data=[0xCD, 0x90, 0x7F], expected=[0x26, 0xD3, 0x69]),
            # Stub in bank $43 end-of-bank free space ($7289-$7fff); hl = wBattleTrapQueue + c, clobbers a
            RomPatchEntry(bank=0x43, address=0x7F90, data=[
                0x79,              # ld a, c
                0xC6, 0x01,        # add LOW(wBattleTrapQueue)
                0x6F,              # ld l, a
                0x3E, 0xD3,        # ld a, HIGH(wBattleTrapQueue)
                0xCE, 0x00,        # adc 0
                0x67,              # ld h, a
                0xC9,              # ret
            ]),
        ],
    ),
    # PlayPCMSampleFar (01:7f8b) switches to wPCMWaveBackup's WRAMX bank; same-size rewrite since bank 1 is full
    RomPatch(
        name="pcm_wave_backup_bank",
        entries=[
            RomPatchEntry(bank=0x01, address=0x7F8B, data=[
                0xF3, 0xF0, 0x70, 0xF5, 0x3E, 0x02, 0xE0, 0x70, 0xD5, 0x3E, 0x80, 0xE0, 0x26, 0x3E, 0x77, 0xE0,
                0x24, 0xAF, 0xE0, 0x12, 0xE0, 0x17, 0xE0, 0x21, 0xE0, 0x1A, 0x21, 0x30, 0xFF, 0x11, 0x01, 0xD4,
                0x7E, 0x12, 0x13, 0x3E, 0xFF, 0x22, 0x7D, 0xFE, 0x40, 0x20, 0xF5, 0x3E, 0x80, 0xE0, 0x1A, 0xF0,
                0x25, 0xF6, 0x44, 0xE0, 0x25, 0x3E, 0x20, 0xE0, 0x1C, 0x3E, 0xFF, 0xE0, 0x1D, 0x3E, 0x87, 0xE0,
                0x1E, 0xE1, 0xCD, 0x95, 0x3D, 0x3E, 0x80, 0xE0, 0x26, 0xAF, 0xE0, 0x1A, 0x21, 0x30, 0xFF, 0x11,
                0x01, 0xD4, 0x1A, 0x13, 0x22, 0x7D, 0xFE, 0x40, 0x20, 0xF8, 0x3E, 0x80, 0xE0, 0x1A, 0xF0, 0x25,
                0xE6, 0xBB, 0xE0, 0x25, 0xF1, 0xE0, 0x70, 0xD9,
            ], expected=[
                0xF3, 0xC5, 0x62, 0x6B, 0xE5, 0xAF, 0xE0, 0x12, 0xE0, 0x17, 0xE0, 0x21, 0x3E, 0x80, 0xE0, 0x26,
                0x3E, 0x77, 0xE0, 0x24, 0xAF, 0xE0, 0x1A, 0x21, 0x30, 0xFF, 0x11, 0x01, 0xD4, 0x7E, 0x12, 0x13,
                0x3E, 0xFF, 0x22, 0x7D, 0xFE, 0x40, 0x20, 0xF5, 0x3E, 0x80, 0xE0, 0x1A, 0xF0, 0x25, 0xF6, 0x44,
                0xE0, 0x25, 0x3E, 0xFF, 0xE0, 0x1B, 0x3E, 0x20, 0xE0, 0x1C, 0x3E, 0xFF, 0xE0, 0x1D, 0x3E, 0x87,
                0xE0, 0x1E, 0xE1, 0xC1, 0xCD, 0x95, 0x3D, 0x3E, 0x80, 0xE0, 0x26, 0xAF, 0xE0, 0x1A, 0x21, 0x30,
                0xFF, 0x11, 0x01, 0xD4, 0x1A, 0x13, 0x22, 0x7D, 0xFE, 0x40, 0x20, 0xF8, 0x3E, 0x80, 0xE0, 0x1A,
                0xF0, 0x25, 0xE6, 0xBB, 0xE0, 0x25, 0xFB, 0xC9,
            ]),
        ],
    ),
]
