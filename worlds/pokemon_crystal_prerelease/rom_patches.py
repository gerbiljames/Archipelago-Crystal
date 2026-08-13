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
            # GameInit (01:6917): call ClearWindowData (01:691d) -> call $0087
            RomPatchEntry(bank=0x01, address=0x691d, data=[0xCD, 0x87, 0x00]),
            # Stub in the home-bank gap between the joypad vector and the header (EMPTY
            # $0063-$00ff); bank 1's tail is the AP_BattleTowerTrainerRewards table, not free
            # space. Occupancy: $0070-$0086 vblank0_service_window_split, $0087-$0090 this.
            # Home is always mapped and calling into it does not switch banks, so the
            # ld a, [AP_Setting_UnlockableTimeOfDay + 1] below still reads bank 1.
            RomPatchEntry(bank=0x00, address=0x0087, data=[
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
            # Stub in the free gap between the interrupt vectors and the header (EMPTY
            # $0063-$00ff). Occupancy: $0070-$0086 this, $0087-$0090 unlocked_time_of_day.
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
            # MovementFunction_ShakingGrass (01:4c62), lifetime clamp at 01:4c73 (10 bytes):
            #   cp 8 / jr nc, .decrement / ld a, 7 / jr .store / .decrement: sub 1 / .store:
            # ->
            #   sub 1 / jr c, .floor / cp 2 / jr nc, .store / .floor: ld a, 2 / .store:
            RomPatchEntry(bank=0x01, address=0x4c73, data=[
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
    # SCENE_ELMSLAB_MEET_OFFICER, armed by the Cherrygrove rival, is the only thing that runs
    # NameRival and clears the officer out of the lab. With no route blocker in New Bark the
    # potion is routinely unclaimed by the time the officer shows up, and the aide stands by
    # the door below the officer's coord events - talking to them there overwrites the scene
    # with SCENE_ELMSLAB_NOOP and strands the officer with nothing left to trigger the naming.
    # Stop the potion script clobbering a pending officer scene, and re-arm it from the objects
    # callback so already-dead saves recover on their next visit. The potion is the only scene
    # write reachable from the door side; everything else is past the row 5 choke point.
    RomPatch(
        name="elms_lab_officer_scene_survives_aide",
        entries=[
            # AideScript_GivePotion (1e:517c): setscene SCENE_ELMSLAB_NOOP / end (1e:518e,
            # 3 bytes) -> sjump to stub. Reached by scall from the walk-over coord scripts and
            # by iffalse from ElmsAideScript; end behaves the same either way.
            RomPatchEntry(bank=0x1E, address=0x518E, data=[0x03, 0xF0, 0x7F]),
            # Stub in bank $1e end-of-bank free space ($7b30-$7fff)
            RomPatchEntry(bank=0x1E, address=0x7FF0, data=[
                0x13,                    # checkscene
                0x06, 0x03, 0xF7, 0x7F,  # ifequal SCENE_ELMSLAB_MEET_OFFICER, .keep
                0x14, 0x02,              # setscene SCENE_ELMSLAB_NOOP
                0x91,                    # .keep: end
            ]),
            # ElmsLabMoveElmCallback (1e:4cc5): checkscene / iftrue .Skip -> sjump to stub.
            # The 4th byte of the overwritten iftrue ($4cc8) is left dangling but unreachable.
            RomPatchEntry(bank=0x1E, address=0x4CC5, data=[0x03, 0xD0, 0x7F]),
            RomPatchEntry(bank=0x1E, address=0x7FD0, data=[
                0x31, 0xB6, 0x06,        # checkevent EVENT_COP_IN_ELMS_LAB
                0x09, 0xD8, 0x7F,        # iftrue .no_cop      ; set = officer already gone
                0x14, 0x03,              # setscene SCENE_ELMSLAB_MEET_OFFICER
                0x13,                    # .no_cop: checkscene ; original callback body
                0x09, 0xCD, 0x4C,        # iftrue ElmsLabMoveElmCallback.Skip
                0x72, 0x02, 0x03, 0x04,  # moveobject ELMSLAB_ELM, 3, 4
                0x90,                    # endcallback
            ]),
        ],
    ),
    # ReceiveArchipelagoItemBattle enqueues in-battle traps into wBattleTrapQueue and immediately
    # frees the server slot and increments the item index, so the trap counts as received. That
    # queue is only drained by CheckMoveTraps (reached by opening FIGHT) or HandleStatusTrap at a
    # residual-damage turn boundary, and the Dude's catch tutorial is auto-input driven straight
    # to ITEM -> Poke Ball -> guaranteed catch: it reaches neither, then ExitBattle zeroes the
    # queue and the trap is gone. Bail out of the battle receive path for BATTLETYPE_TUTORIAL,
    # alongside the existing link and Battle Tower guards, so the slot stays pending and the
    # overworld path delivers it once the tutorial script ends.
    RomPatch(
        name="no_item_delivery_during_catch_tutorial",
        entries=[
            # ReceiveArchipelagoItemBattle (7d:7466): ld a, [wLinkMode] -> jp stub
            RomPatchEntry(bank=0x7D, address=0x7466, data=[0xC3, 0xF0, 0x7F]),
            # Stub in bank $7d end-of-bank free space ($751d-$7fff)
            RomPatchEntry(bank=0x7D, address=0x7FF0, data=[
                0xFA, 0x37, 0xD2,  # ld a, [wBattleType]
                0xFE, 0x03,        # cp BATTLETYPE_TUTORIAL
                0xC8,              # ret z
                0xFA, 0xDC, 0xC2,  # ld a, [wLinkMode]              ; overwritten instruction
                0xC3, 0x69, 0x74,  # jp ReceiveArchipelagoItemBattle + 3
            ]),
        ],
    ),
    # ReceiveArchipelagoItemBattle pushes the trap-link slot into wBattleTrapQueue without the
    # IsBattleTrapId check the server-item path runs first, so a linked phone/tutorial/ice/shuffle
    # trap arriving while a battle menu is open lands in a queue that only CheckMoveTraps and
    # HandleStatusTrap drain. Neither matches a non-battle trap id, so ClearBattleTrapSlot never
    # pops it: the trap is lost and every later battle trap is stuck behind the dead head entry.
    # Gate the enqueue on IsBattleTrapId and apply non-battle traps immediately via ReceiveFlagItem,
    # which is what the flag item path already does with them.
    RomPatch(
        name="traplink_battle_queue_rejects_non_battle_traps",
        entries=[
            # ReceiveArchipelagoItemBattle.check_traplink (7d:74ed): farcall EnqueueBattleTrap
            # -> farcall stub, by retargeting the ld hl (7d:74f6). Both live in bank $43, so the
            # macro's ld a, BANK() at 7d:74f4 is already correct.
            RomPatchEntry(bank=0x7D, address=0x74F6, data=[0x21, 0x80, 0x7F]),
            # Stub in bank $43 end-of-bank free space ($724c-$7fff)
            RomPatchEntry(bank=0x43, address=0x7F80, data=[
                0xCD, 0x5E, 0x6C,  # call IsBattleTrapId           ; b = trap id, preserved
                0x30, 0x03,        # jr nc, .non_battle
                0xC3, 0x8B, 0x6C,  # jp EnqueueBattleTrap          ; carry = enqueued, as before
                0x78,              # .non_battle: ld a, b
                0xEA, 0xEA, 0xD6,  # ld [wArchipelagoFlagItemId], a
                0x3E, 0x01,        # ld a, 1
                0xEA, 0x13, 0xD1,  # ld [wItemQuantityChange], a
                0xCD, 0x9E, 0x52,  # call ReceiveFlagItem
                0x37,              # scf                           ; caller sounds it, frees the slot
                0xC9,              # ret
            ]),
        ],
    ),
    # MoveMonWOMail_InsertMon_SaveGame - the save Crystal runs when a mon is moved in PC storage -
    # is a full save, but SaveArchipelagoData/SaveBackupArchipelagoData were only ever added to
    # _SaveGameData, so it skips them. sArchipelagoData lives inside sGameData, which SaveChecksum
    # covers, so the file ends up with a valid checksum over an AP block left behind by the previous
    # full save: nothing flags it, and TryLoadSaveFile restores it as-is on the next continue. That
    # rolls back the grass/sign/battle tower/rematch location flags, the PC gift box, the EnergyLink
    # handshake and wItemQueue while the rest of the file stays current - and a rolled back item
    # queue re-delivers local items, so without remote items the player's own traps fire again.
    # Fold the two AP writes into the SavePokemonData/SaveBackupPokemonData call sites, which sit
    # exactly where _SaveGameData runs them and, crucially, ahead of both checksum writes.
    RomPatch(
        name="pc_storage_save_writes_archipelago_data",
        entries=[
            # MoveMonWOMail_InsertMon_SaveGame (05:4974): call SavePokemonData (05:499a) -> call stub
            RomPatchEntry(bank=0x05, address=0x499A, data=[0xCD, 0xE2, 0x7F]),
            # call SaveBackupPokemonData (05:49ac) -> call stub
            RomPatchEntry(bank=0x05, address=0x49AC, data=[0xCD, 0xE9, 0x7F]),
            # Stubs in bank $05 end-of-bank free space ($7f96-$7fff); 14 bytes at $7fe2-$7fef
            RomPatchEntry(bank=0x05, address=0x7FE2, data=[
                0xCD, 0x99, 0x4C,  # call SavePokemonData            ; overwritten instruction
                0xCD, 0xAE, 0x4C,  # call SaveArchipelagoData        ; before SaveChecksum at 05:49a0
                0xC9,              # ret
                0xCD, 0x5B, 0x4D,  # call SaveBackupPokemonData      ; overwritten instruction
                0xCD, 0x70, 0x4D,  # call SaveBackupArchipelagoData  ; before SaveBackupChecksum
                0xC9,              # ret
            ]),
        ],
    ),
    # SaveAfterLinkTrade - the save wonder trade runs to commit the party across the trade - only
    # writes SavePokemonData before recomputing both checksums, skipping SavePlayerData and
    # SaveArchipelagoData. sPlayerData holds wArchipelagoItemIndex, the cursor for server-delivered
    # items, so the file validates with a cursor from the previous full save. On the next continue
    # TryLoadSaveFile rewinds it and the client re-delivers everything received since - with remote
    # items that includes the player's own traps, so phone traps and friends fire again (and get
    # re-broadcast over TrapLink). Retarget the two SavePokemonData calls to stubs that save player
    # data first, then chain into the pc_storage stubs above for the pokemon + AP data writes.
    RomPatch(
        name="wonder_trade_save_writes_player_data",
        entries=[
            # SaveAfterLinkTrade (05:48a9): call SavePokemonData (05:48b8) -> call stub
            RomPatchEntry(bank=0x05, address=0x48B8, data=[0xCD, 0xF0, 0x7F]),
            # call SaveBackupPokemonData (05:48be) -> call stub
            RomPatchEntry(bank=0x05, address=0x48BE, data=[0xCD, 0xF6, 0x7F]),
            # Stubs at $7ff0-$7ffb, after the pc_storage stubs ($7fe2-$7fef)
            RomPatchEntry(bank=0x05, address=0x7FF0, data=[
                0xCD, 0x79, 0x4C,  # call SavePlayerData             ; before SaveChecksum at 05:48bb
                0xC3, 0xE2, 0x7F,  # jp $7fe2                        ; SavePokemonData + SaveArchipelagoData
                0xCD, 0x3A, 0x4D,  # call SaveBackupPlayerData       ; before SaveBackupChecksum
                0xC3, 0xE9, 0x7F,  # jp $7fe9                        ; backup pokemon + AP data
            ]),
        ],
    ),
    # Under trainersanity AdjustPaletteIfTrainersanity tints an uncollected trainer PAL_OW_EMOTE and
    # only recomputes it when the object struct is (re)loaded, so every other trainersanity NPC runs
    # special UpdateTrainerSpritePalettes right after handing over its item. Mt. Mortar's Kiyo never
    # does: on the path where the Tyrogue is actually given, the givepoke menus refresh the sprites
    # for free and hide it, but with a full party the script only ever opens text boxes and Kiyo
    # stays highlighted until the map is reloaded. Retarget the setevent that follows the item to a
    # stub that sets the flag and repaints.
    RomPatch(
        name="mount_mortar_kiyo_trainersanity_palette",
        entries=[
            # MountMortarB1FKiyoScript.Item (1f:6281): setevent EVENT_ITEM_FROM_BLACKBELT_KIYO
            # (1f:628f) -> sjump stub
            RomPatchEntry(bank=0x1F, address=0x628F, data=[0x03, 0xF8, 0x7F]),
            # Stub in bank $1f end-of-bank free space ($77ae-$7fff)
            RomPatchEntry(bank=0x1F, address=0x7FF8, data=[
                0x33, 0xD0, 0x04,  # setevent EVENT_ITEM_FROM_BLACKBELT_KIYO  ; overwritten command
                0x0F, 0xAC, 0x00,  # special UpdateTrainerSpritePalettes
                0x91,              # end                                     ; as .done
            ]),
        ],
    ),
    # The Battle Tower's between-rounds "heal" is RunBattleTowerTrainer reloading the whole party
    # from the save file: after every battle it runs LoadPokemonData + HealParty, and the save
    # always holds the original un-capped party (every save path restores the backup first). That
    # wipes BattleTower_LevelDownPartyAndBackup's level-down after round 1, so rounds 2-7 are
    # fought at full level; only a save+quit resume (which re-runs Script_BattleRoom) re-applies
    # the cap. Re-apply the level-down after the reload - the reloaded party is the original, so
    # the routine's re-snapshot of the SRAM backup stays correct.
    RomPatch(
        name="battle_tower_level_cap_survives_between_rounds",
        entries=[
            # RunBattleTowerTrainer (5c:4121): post-battle farcall HealParty (5c:414b, 6 bytes)
            # -> call stub + nops
            RomPatchEntry(bank=0x5C, address=0x414B, data=[
                0xCD, 0xF0, 0x7F,  # call $7ff0
                0x00, 0x00, 0x00,  # nop x3
            ]),
            # Stub in bank $5c end-of-bank free space ($726f-$7fff)
            RomPatchEntry(bank=0x5C, address=0x7FF0, data=[
                0x3E, 0x03,        # ld a, BANK(HealParty)
                0x21, 0x78, 0x46,  # ld hl, HealParty
                0xCF,              # rst FarCall
                0x3E, 0x7E,        # ld a, BANK(BattleTower_LevelDownPartyAndBackup)
                0x21, 0xEA, 0x73,  # ld hl, BattleTower_LevelDownPartyAndBackup
                0xCF,              # rst FarCall
                0xC9,              # ret
            ]),
        ],
    ),
    # The Battle Tower prize path can re-enter after a reset: a pack-full prize leaves SRAM state
    # WON_CHALLENGE, and on the next talk the receptionist goes straight back to
    # Script_GivePlayerHisPrize with wBTChoiceOfLvlGroup zeroed by ClearWRAM (sBTChoiceOfLevelGroup
    # is only current after a mid-streak save-and-quit). GiveReward then misindexes the reward
    # table with $ff and SetTierClaimedBit corrupts wPCFlagItems + 11. Persist the group at
    # challenge start via the CLEAR_CHALLENGE_RESUMED handler (BattleTowerRoomMenu has written it
    # by then, and it is the action's only call site; state 3 blocks new challenges, so SRAM stays
    # correct until the prize is claimed) and reload it at GiveReward's head, which also repairs
    # the script's later readers (.GetTierAPItemText, .DoTierFlagItem, .SetTierClaimedBit) - a
    # no-op in-session and on the save-and-quit resume path.
    RomPatch(
        name="battle_tower_level_group_persists",
        entries=[
            # BattleTower_GiveReward (5c:4507): ldh a, [rSVBK] / push af -> jp stub
            RomPatchEntry(bank=0x5C, address=0x4507, data=[0xC3, 0xC0, 0x7F]),
            # BattleTowerAction_ClearChallengeResumed (5c:46c5): ld c, FALSE / jr Set_s5_aa8d
            # (4 bytes) -> jp stub; trailing byte dangles unreachable
            RomPatchEntry(bank=0x5C, address=0x46C5, data=[0xC3, 0xD0, 0x7F]),
            # Stubs in bank $5c end-of-bank free space ($726f-$7fff);
            # $7ff0-$7ffc holds battle_tower_level_cap_survives_between_rounds
            RomPatchEntry(bank=0x5C, address=0x7FC0, data=[
                0xCD, 0x8D, 0x46,  # call LoadBattleTowerLevelGroup
                0xF0, 0x70,        # ldh a, [rSVBK]     ; overwritten instructions
                0xF5,              # push af
                0xC3, 0x0A, 0x45,  # jp BattleTower_GiveReward + 3
            ]),
            RomPatchEntry(bank=0x5C, address=0x7FD0, data=[
                0xCD, 0x74, 0x46,  # call SaveBattleTowerLevelGroup
                0x0E, 0x00,        # ld c, FALSE        ; overwritten instruction
                0xC3, 0xCB, 0x46,  # jp Set_s5_aa8d
            ]),
        ],
    ),
    # The Battle Tower reward handlers set the claim flags (wArchipelagoBattleTowerTrainerFlags,
    # wArchipelagoBattleTowerCompletedTiers) but never check them, and a tier is freely replayable
    # after its prize: the streak position maps to the same canonical trainer ids, so re-clearing a
    # tier hands out every per-trainer reward and the tier prize again - local giveitems and flag
    # items are real duplicates. Both handlers end in ld [wScriptVar], a / ret with de still
    # holding the flag bit index (canonical id / tier-1; GetFarByte preserves de), so retarget
    # that store into a shared stub that zeroes wScriptVar when the claim flag is set; the
    # scripts' existing ifequal 0 then skips the hand-out (trainer flow continues at
    # .ap_trainer_skip, prize flow at .finish, whose re-run of SetTierClaimedBit is idempotent).
    # Bag-full retries still work: those paths never set the flag, so the reward is re-offered.
    # The claim-skip newly exercises the prize script's ifequal-0 branch, which lands on closetext
    # with the congratulations text barely shown; route it through a waitbutton. With
    # battle_tower_sanity off this makes the default vitamin prizes one-time per tier too.
    RomPatch(
        name="battle_tower_rewards_not_repeatable",
        entries=[
            # BattleTower_LookupTrainerReward (5c:454d): ld [wScriptVar], a (5c:455c) -> jp stub;
            # the ret behind each retargeted store dangles unreachable
            RomPatchEntry(bank=0x5C, address=0x455C, data=[0xC3, 0x95, 0x7F]),
            # BattleTower_GiveReward (5c:4507): ld [wScriptVar], a (5c:4521) -> jp stub
            RomPatchEntry(bank=0x5C, address=0x4521, data=[0xC3, 0x90, 0x7F]),
            # Stub in bank $5c end-of-bank free space, below battle_tower_level_group_persists
            RomPatchEntry(bank=0x5C, address=0x7F90, data=[
                0x21, 0xD8, 0xD2,  # ld hl, wArchipelagoBattleTowerCompletedTiers  ; tier entry
                0x18, 0x03,        # jr .common
                0x21, 0xCF, 0xD2,  # ld hl, wArchipelagoBattleTowerTrainerFlags    ; trainer entry
                0xEA, 0xDD, 0xC2,  # .common: ld [wScriptVar], a  ; retargeted store, de = bit index
                0xF0, 0x70,        # ldh a, [rSVBK]
                0xF5,              # push af
                0x3E, 0x02,        # ld a, BANK(wArchipelagoBattleTowerTrainerFlags) ; both arrays
                0xE0, 0x70,        # ldh [rSVBK], a
                0x06, 0x02,        # ld b, CHECK_FLAG
                0xCD, 0x84, 0x2E,  # call FlagAction
                0xF1,              # pop af
                0xE0, 0x70,        # ldh [rSVBK], a
                0x79,              # ld a, c
                0xA7,              # and a
                0xC8,              # ret z              ; unclaimed -> reward as normal
                0xAF,              # xor a
                0xEA, 0xDD, 0xC2,  # ld [wScriptVar], a ; claimed -> skip hand-out
                0xC9,              # ret
            ]),
            # Script_GivePlayerHisPrize (27:65ee): ifequal 0, .finish -> retarget to stub
            RomPatchEntry(bank=0x27, address=0x65F0, data=[0xF0, 0x7F]),
            # Stub in bank $27 end-of-bank free space ($7bd8-$7fff)
            RomPatchEntry(bank=0x27, address=0x7FF0, data=[
                0x54,              # waitbutton         ; let the congratulations text be read
                0x03, 0x2A, 0x66,  # sjump Script_GivePlayerHisPrize.finish
            ]),
        ],
    ),
    # RunBattleTowerTrainer writes the next opponent's digit into wStringBuffer3 after each win,
    # but the AP trainer reward hand-out runs in between and clobbers it - GetFlagItemName builds
    # the flag item's name in that exact buffer - so "Next up, opponent no.X" can display an item
    # name. Regenerate the digit right before the prompt, covering every reward path.
    RomPatch(
        name="battle_tower_next_opponent_number_not_clobbered",
        entries=[
            # Script_BattleRoomLoop (27:7472): writetext Text_NextUpOpponentNo -> sjump stub
            RomPatchEntry(bank=0x27, address=0x7472, data=[0x03, 0xE0, 0x7F]),
            # Script stub in bank $27 end-of-bank free space
            RomPatchEntry(bank=0x27, address=0x7FE0, data=[
                0x0E, 0x5C, 0xE0, 0x7F,  # callasm digit fixup
                0x4C, 0x6E, 0x6F,        # writetext Text_NextUpOpponentNo
                0x03, 0x75, 0x74,        # sjump 27:7475        ; yesorno
            ]),
            # Asm stub in bank $5c end-of-bank free space; mirrors RunBattleTowerTrainer's write
            RomPatchEntry(bank=0x5C, address=0x7FE0, data=[
                0xFA, 0x64, 0xCF,  # ld a, [wNrOfBeatenBattleTowerTrainers]
                0xC6, 0xF7,        # add "1"
                0x21, 0x99, 0xD0,  # ld hl, wStringBuffer3
                0x22,              # ld [hli], a
                0x3E, 0x50,        # ld a, "@"
                0x77,              # ld [hl], a
                0xC9,              # ret
            ]),
        ],
    ),
    # Battle Tower opponent mons are full party-mon structs with precomputed stats baked into
    # AP_BattleTowerMons, used as-is: ReadBTTrainerParty copies them into wOTPartyMon and battle
    # tower battles take the link-battle path (InitEnemyMon), which trusts the struct's stat
    # fields. Recompute all six stats from base data / DVs / stat exp after the copy, so the
    # numbers always match the entry's inputs (and the seed's base data). Hook the
    # call ReadBTTrainerParty in RunBattleTowerTrainer; rSVBK is the resident bank 1 there, so
    # wOTPartyMon / wCurPartyLevel / wCurBaseData are all directly addressable. CalcMonStats is
    # invoked via Predef (preserves bc/de/hl into the routine; hl can't survive a farcall) with
    # the vanilla ABI: b=TRUE, de=stats dest (MON_MAXHP), hl=stat exp - 1, from which it also
    # reads the DVs at the party-struct offset. HP is then set to the fresh Max HP.
    RomPatch(
        name="battle_tower_mon_stats_recomputed",
        entries=[
            # RunBattleTowerTrainer (5c:4121): call ReadBTTrainerParty (5c:413a) -> call stub
            RomPatchEntry(bank=0x5C, address=0x413A, data=[0xCD, 0x40, 0x7F]),
            # Stub in bank $5c end-of-bank free space, below the other battle tower stubs
            RomPatchEntry(bank=0x5C, address=0x7F40, data=[
                0xCD, 0x7E, 0x41,  # call ReadBTTrainerParty         ; overwritten instruction
                0x21, 0x8F, 0xD2,  # ld hl, wOTPartyMon1Species
                0xCD, 0x4C, 0x7F,  # call .one
                0xCD, 0x4C, 0x7F,  # call .one                       ; falls through for mon 3
                0x7E,              # .one: ld a, [hl]                ; species
                0xEA, 0x60, 0xCF,  # ld [wCurSpecies], a
                0x54,              # ld d, h
                0x5D,              # ld e, l                         ; de = mon base
                0x21, 0x1F, 0x00,  # ld hl, MON_LEVEL
                0x19,              # add hl, de
                0x7E,              # ld a, [hl]
                0xEA, 0x4A, 0xD1,  # ld [wCurPartyLevel], a
                0xCD, 0x0A, 0x38,  # call GetBaseData                ; preserves bc/de/hl
                0xD5,              # push de                         ; mon base
                0x21, 0x0A, 0x00,  # ld hl, MON_STAT_EXP - 1
                0x19,              # add hl, de
                0xE5,              # push hl
                0x21, 0x24, 0x00,  # ld hl, MON_MAXHP
                0x19,              # add hl, de
                0x54,              # ld d, h
                0x5D,              # ld e, l                         ; de = stats dest
                0xE1,              # pop hl                          ; hl = stat exp - 1
                0x06, 0x01,        # ld b, TRUE
                0x3E, 0x0B,        # ld a, PREDEF_CALCMONSTATS
                0xCD, 0x89, 0x2D,  # call Predef
                0xD1,              # pop de                          ; mon base
                0x21, 0x24, 0x00,  # ld hl, MON_MAXHP
                0x19,              # add hl, de
                0x2A,              # ld a, [hli]                     ; max hp hi
                0x46,              # ld b, [hl]                      ; max hp lo
                0x21, 0x22, 0x00,  # ld hl, MON_HP
                0x19,              # add hl, de
                0x77,              # ld [hl], a
                0x23,              # inc hl
                0x70,              # ld [hl], b                      ; HP = Max HP
                0x21, 0x30, 0x00,  # ld hl, PARTYMON_STRUCT_LENGTH
                0x19,              # add hl, de                      ; hl = next mon
                0xC9,              # ret
            ]),
        ],
    ),
    RomPatch(
        name="flooded_mine_border_block",
        entries=[
            # FloodedMine_MapAttributes (25:670d): border block $00 -> $09
            RomPatchEntry(bank=0x25, address=0x670D, data=[0x09]),
        ],
    ),
    # The town map draws the landmark name from hlcoord 9, 0, leaving 11 tiles before the screen
    # edge. "FLOODED MINE" is 12 and spills off the right; every other 12+ char landmark name uses
    # the soft linebreak. Swap the space for one.
    RomPatch(
        name="flooded_mine_landmark_name_wrap",
        entries=[
            # FloodedMineName + 7 (72:6a3e): " " ($7f) -> "¯" ($1f)
            RomPatchEntry(bank=0x72, address=0x6A3E, data=[0x1F]),
        ],
    ),
]
