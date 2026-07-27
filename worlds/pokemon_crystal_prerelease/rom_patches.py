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
            # GameInit (01:6921): call ClearWindowData (01:6927) -> call $7ff5
            RomPatchEntry(bank=0x01, address=0x6927, data=[0xCD, 0xF5, 0x7F]),
            # Stub in bank 1's remaining free space ($7ff5-$7fff, exactly 11 bytes)
            RomPatchEntry(bank=0x01, address=0x7ff5, data=[
                0xCD, 0xFA, 0x1F,  # call ClearWindowData
                0xFA, 0x88, 0x5D,  # ld a, [AP_Setting_UnlockableTimeOfDay + 1]
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
    # The AP item popup owns a window split: the window draws the box over the top three rows
    # and the LCD HBlank handler clears rLCDC_WINDOW_ENABLE at scanline 23 so it stops there.
    # VBlank0 runs its whole body with interrupts disabled, sound engine included, and routinely
    # overruns ~30 scanlines into the visible frame, so that write cannot happen until VBlank0
    # returns and the window keeps rendering to wherever that lands - the transfer's unused
    # fourth row in full, plus a line of stale VRAM past it - whatever the split is armed to.
    # Once the VRAM work is done, hold interrupts open just long enough for the LCD handler to
    # make that one write, then close them again before UpdateJoypad and _UpdateSound. Leaving
    # them open across the sound update corrupts graphics: Request2bpp switches the ROM bank to
    # the source's bank and halts with it held until served, so an HBlank serve landing while
    # _UpdateSound has banked to audio copies music data into VRAM.
    # Only runs while the split is armed; with no popup up this is vanilla behaviour.
    RomPatch(
        name="vblank0_service_window_split",
        entries=[
            # VBlank0 .done_oam (00:0319): xor a / ld [wVBlankOccurred], a -> call stub
            RomPatchEntry(bank=0x00, address=0x0319, data=[
                0xCD, 0x70, 0x00,  # call $0070
                0x00,              # nop
            ]),
            # Stub in the free gap between the interrupt vectors and the header ($63-$100)
            RomPatchEntry(bank=0x00, address=0x0070, data=[
                0xF0, 0xD5,        # ldh a, [hWindowSplit]
                0xA7,              # and a
                0x28, 0x0D,        # jr z, .skip            ; no popup -> vanilla path
                0x47,              # ld b, a
                0x04,              # inc b                  ; wait past the split line's HBlank
                0xFB,              # ei
                0xF0, 0x44,        # .wait: ldh a, [rLY]
                0xFE, 0x90,        # cp LY_VBLANK
                0x30, 0xFA,        # jr nc, .wait           ; still in VBlank
                0xB8,              # cp b
                0x38, 0xF7,        # jr c, .wait            ; not past the split yet
                0xF3,              # di
                0xAF,              # .skip: xor a
                0xEA, 0xB3, 0xCF,  # ld [wVBlankOccurred], a
                0xC9,              # ret
            ]),
        ],
    ),
    # The grass rustle sprite is a tracking object: every frame it copies the player's sprite
    # position, so it stays glued to the player until its lifetime expires. Vanilla sets that
    # lifetime to (player step duration - 1) so it dies exactly as the step ends.
    # MovementFunction_ShakingGrass instead clamps every duration under 8 up to 7, to dodge the
    # degenerate turbo-bike values (0 underflows to $FF, 1 becomes 0 and never deletes because
    # StepFunction_TrackingObject rets on a zero duration). That over-corrects: a bike step is
    # 4 frames and a turbo step 2, so the rustle outlives the step by 3-5 frames and trails the
    # player several tiles past the grass. Restore the vanilla decrement with a floor of 2, the
    # minimum that still renders one frame with valid coords and can never reach the zero case.
    RomPatch(
        name="grass_rustle_lingers_after_leaving_grass",
        entries=[
            # MovementFunction_ShakingGrass (01:4c6c), lifetime clamp at 01:4c7d (10 bytes):
            #   cp 8 / jr nc, .decrement / ld a, 7 / jr .store / .decrement: sub 1 / .store:
            # ->
            #   sub 1 / jr c, .floor / cp 2 / jr nc, .store / .floor: ld a, 2 / .store:
            RomPatchEntry(bank=0x01, address=0x4c7d, data=[
                0xD6, 0x01,  # sub 1
                0x38, 0x04,  # jr c, .floor
                0xFE, 0x02,  # cp 2
                0x30, 0x02,  # jr nc, .store
                0x3E, 0x02,  # .floor: ld a, 2
            ]),
        ],
    ),
    # Boarding the Fast Ship blackoutmods the cabin so a whiteout mid-voyage keeps you on the
    # ship, which throws away the pokecenter you actually last used. Vanilla restores it on
    # arrival, but under ER the ports can't (the port city's center is not necessarily reachable)
    # so they ClearLastSpawn instead, and every teleport/whiteout after a crossing falls back to
    # SPAWN_HOME. Teleport can't be used on the ship at all (TryTeleport requires an outdoor map),
    # so the cabin spawn only ever feeds GetWhiteoutSpawn - derive it from the current map there
    # and stop writing it to wLastSpawnMap, which leaves your real spawn untouched by the trip.
    RomPatch(
        name="fast_ship_spawn_keeps_last_pokecenter",
        entries=[
            # GetWhiteoutSpawn (04:6531): ld [wDefaultSpawnpoint], a (04:6544) -> jp stub
            RomPatchEntry(bank=0x04, address=0x6544, data=[0xC3, 0xDD, 0x7F]),
            # Stub in bank 4 end-of-bank free space ($7fdd-$7fff)
            RomPatchEntry(bank=0x04, address=0x7fdd, data=[
                0x47,              # ld b, a                    ; spawn from the wLastSpawnMap lookup
                0xFA, 0xBC, 0xDC,  # ld a, [wMapGroup]
                0xFE, 0x0F,        # cp GROUP_FAST_SHIP_1F
                0x20, 0x0D,        # jr nz, .done
                0xFA, 0xBD, 0xDC,  # ld a, [wMapNumber]
                0xFE, 0x03,        # cp MAP_FAST_SHIP_1F        ; ship maps are 3-7 in the group,
                0x38, 0x06,        # jr c, .done                ; the ports and passages are not
                0xFE, 0x08,        # cp MAP_FAST_SHIP_B1F + 1
                0x30, 0x02,        # jr nc, .done
                0x06, 0x32,        # ld b, SPAWN_FAST_SHIP
                0x78,              # .done: ld a, b
                0xEA, 0x01, 0xD0,  # ld [wDefaultSpawnpoint], a
                0xC9,              # ret
            ]),
            # FastShip1FEnterShipScript (1d:522e): blackoutmod FAST_SHIP_CABINS_SW_SSW_NW
            # (1d:5241) -> sjump to the next command
            RomPatchEntry(bank=0x1D, address=0x5241, data=[0x03, 0x44, 0x52]),
            # VermilionPortLeaveShipScript (1d:4e74): the ER branch's iftrue (1d:4e8e) targets
            # callasm ClearLastSpawn ($4e95) -> the end after blackoutmod ($4e94), so ER now
            # leaves the spawn alone. Non-ER still blackoutmods the port city as in vanilla.
            RomPatchEntry(bank=0x1D, address=0x4E8F, data=[0x94]),
            # OlivinePortLeaveShipScript (1d:49bf): same, $49e0 -> $49df
            RomPatchEntry(bank=0x1D, address=0x49DA, data=[0xDF]),
        ],
    ),
]
