from dataclasses import dataclass


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
    # wUnlockedTimeOfDay is game data, only populated by NewGame or loading a save, so the
    # title-screen options menu reads 0 from cleared WRAM and shows Time of Day as LOCKED on
    # every seed. Hook GameInit to seed it with the ROM-patched initial bitmask (the immediate
    # at AP_Setting_UnlockableTimeOfDay + 1); NewGame/Continue overwrite it as before.
    RomPatch(
        name="unlocked_time_of_day_boot_init",
        entries=[
            # GameInit (01:6917): call ClearWindowData (01:691d) -> call $7f80
            RomPatchEntry(bank=0x01, address=0x691d, data=[0xCD, 0x80, 0x7F]),
            # Stub in bank 1 end-of-bank free space ($7f70-$7fff)
            RomPatchEntry(bank=0x01, address=0x7f80, data=[
                0xCD, 0xFA, 0x1F,  # call ClearWindowData
                0xFA, 0x7E, 0x5D,  # ld a, [AP_Setting_UnlockableTimeOfDay + 1]
                0xEA, 0xEB, 0xD6,  # ld [wUnlockedTimeOfDay], a
                0xC9,              # ret
            ]),
        ],
    ),
    # CheckRockets keys the radio tower takeover off EVENT_TEAM_ROCKET_DISBANDED, which is not
    # co-op synced. A save rolled back past the tower clear gets EVENT_CLEARED_RADIO_TOWER synced
    # back without any of the takeover/post-clear object state, forcing a full takeover replay
    # (or, under trainersanity, hiding the tower rocket trainers). Hook the DISBANDED check in
    # CheckRockets: when DISBANDED is clear but CLEARED_RADIO_TOWER is set, apply the 5F clear
    # script's world state idempotently and skip the takeover. Scenes, location flags and
    # DISBANDED itself are left untouched so the 5F cutscenes stay playable.
    RomPatch(
        name="radio_tower_cleared_self_heal",
        entries=[
            # CheckRockets (03:56cc): call EventFlagAction (03:56d4) -> call $7f80
            RomPatchEntry(bank=0x03, address=0x56d4, data=[0xCD, 0x80, 0x7F]),
            # Stub in bank 3 end-of-bank free space ($7d65-$7fff)
            RomPatchEntry(bank=0x03, address=0x7f80, data=[
                0xCD, 0x7D, 0x2E,  # call EventFlagAction        ; b=CHECK_FLAG, de=EVENT_TEAM_ROCKET_DISBANDED
                0x79,              # ld a, c
                0xA7,              # and a
                0xC0,              # ret nz                      ; disbanded -> caller takes .done
                0x21, 0x8C, 0xDA,  # ld hl, wEventFlags + 4
                0xCB, 0x4E,        # bit 1, [hl]                 ; EVENT_CLEARED_RADIO_TOWER (33)
                0xC8,              # ret z                       ; not cleared -> vanilla flow (c=0)
                0xCB, 0xEE,        # set 5, [hl]                 ; EVENT_USED_THE_CARD_KEY_IN_THE_RADIO_TOWER (37)
                0x21, 0x8A, 0xDA,  # ld hl, wEventFlags + 2
                0xCB, 0xB6,        # res 6, [hl]                 ; EVENT_RADIO_TOWER_5F_BEN (22)
                0x21, 0x57, 0xDB,  # ld hl, wEventFlags + 207
                0xCB, 0xFE,        # set 7, [hl]                 ; EVENT_GOLDENROD_CITY_ROCKET_SCOUT (1663)
                0x23,              # inc hl                      ; wEventFlags + 208
                0x7E,              # ld a, [hl]
                0xE6, 0xF3,        # and %11110011               ; res GOLDENROD_CITY_CIVILIANS (1666), RADIO_TOWER_CIVILIANS_AFTER (1667)
                0xF6, 0x31,        # or %00110001                ; set GOLDENROD_ROCKET_TAKEOVER (1664), BLACKBELT_BLOCKS_STAIRS (1668), ROCKET_BOSS (1669)
                0x77,              # ld [hl], a
                0xFA, 0x1E, 0xD8,  # ld a, [wStatusFlags]
                0x87,              # add a                       ; STATUSFLAGS_TRAINERSANITY_F (7) -> carry
                0x38, 0x04,        # jr c, .trainersanity
                0xCB, 0xCE,        # set 1, [hl]                 ; EVENT_RADIO_TOWER_ROCKET_TAKEOVER (1665): hide tower rockets
                0x18, 0x02,        # jr .cont
                0xCB, 0x8E,        # res 1, [hl]                 ; trainersanity: keep tower rocket trainers
                0x21, 0x5A, 0xDB,  # ld hl, wEventFlags + 210
                0xCB, 0xFE,        # set 7, [hl]                 ; EVENT_BLACKTHORN_CITY_SUPER_NERD_BLOCKS_GYM (1687)
                0x23,              # inc hl                      ; wEventFlags + 211
                0xCB, 0x86,        # res 0, [hl]                 ; EVENT_BLACKTHORN_CITY_SUPER_NERD_DOES_NOT_BLOCK_GYM (1688)
                0x21, 0x65, 0xDB,  # ld hl, wEventFlags + 221
                0xCB, 0x96,        # res 2, [hl]                 ; EVENT_MAHOGANY_MART_OWNERS (1770)
                0x21, 0x1F, 0xD8,  # ld hl, wStatusFlags2
                0xCB, 0x86,        # res 0, [hl]                 ; ENGINE_ROCKETS_IN_RADIO_TOWER
                0xCB, 0xBE,        # res 7, [hl]                 ; ENGINE_ROCKETS_IN_MAHOGANY
                0x0E, 0x01,        # ld c, 1                     ; caller takes .done, skipping SetGoldenrodRockets
                0xC9,              # ret
            ]),
        ],
    ),
    # Redrawing the AP item popup over a live one (stacked notifications) flickers a few
    # scanlines of window below the box. HDMATransfer_OnlyTopFourRows copies ~15 scanlines
    # worth of tilemap and then holds di for ~11 scanlines per HDMA block, twice; if that di
    # window covers the split line (23), the HBlank interrupt that clears rLCDC_WINDOW_ENABLE
    # is missed and the window keeps rendering past the box until the ei.
    # TriggerAPItemSign already waits for a "safe" rLY, but its upper bound of 110 is measured
    # before the copy: starting near it pushes HDMATransfer's own "wait for rLY < 120" gate
    # into the next frame, landing both di blocks right across line 23. Lower the bound to 60
    # so copy + both transfers (~37 scanlines) finish inside the same frame, below the box.
    RomPatch(
        name="ap_item_popup_redraw_split_flicker",
        entries=[
            # TriggerAPItemSign.wait_below_box (2e:4149): cp 110 -> cp 60
            RomPatchEntry(bank=0x2e, address=0x4150, data=[60]),
        ],
    ),
]
