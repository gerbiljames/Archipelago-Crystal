from dataclasses import dataclass


@dataclass
class RomPatchEntry:
    bank: int
    address: int
    data: list[int]
    # patch is skipped unless every entry's ROM bytes match (overrides apply after token writes)
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
    # Qwilfish swarm applied to every fishing spot instead of only Route 32, and outlived ENGINE_QWILFISH_SWARM
    RomPatch("Qwilfish swarm fishgroup and engine flag check", [
        # bank $24 free space: z if fishgroup is QWILFISH, ENGINE_QWILFISH_SWARM set and swarm flag QWILFISH
        RomPatchEntry(0x24, 0x7fcb, [
            0x7a,              # ld a, d
            0xfe, 0x0a,        # cp FISHGROUP_QWILFISH
            0xc0,              # ret nz
            0xfa, 0x5b, 0xdc,  # ld a, [wDailyFlags1]
            0x2f,              # cpl
            0xcb, 0x57,        # bit DAILYFLAGS1_FISH_SWARM_F, a
            0xc0,              # ret nz
            0xfa, 0xd4, 0xdf,  # ld a, [wFishingSwarmFlag]
            0xfe, 0x01,        # cp FISHSWARM_QWILFISH
            0xc9,              # ret
        ], expected=[0x00] * 17),
        # Fish: ld a, [wFishingSwarmFlag] / cp FISHSWARM_QWILFISH -> call $7fcb / nop / nop
        RomPatchEntry(0x24, 0x682f, [0xcd, 0xcb, 0x7f, 0x00, 0x00],
                      expected=[0xfa, 0xd4, 0xdf, 0xfe, 0x01]),
    ]),
    # swarms persist until the triggering trainer is called again
    RomPatch("Keep swarm flags across daily reset", [
        # ROM0 free space: clear daily flags except the swarm bits, return a = 0
        RomPatchEntry(0x00, 0x0082, [
            0x21, 0x5b, 0xdc,  # ld hl, wDailyFlags1
            0x7e,              # ld a, [hl]
            0xe6, 0x04,        # and 1 << DAILYFLAGS1_FISH_SWARM_F
            0x22,              # ld [hli], a
            0xaf,              # xor a
            0x22,              # ld [hli], a ; wDailyFlags2
            0x7e,              # ld a, [hl]
            0xe6, 0x0c,        # and (1 << SWARMFLAGS_DUNSPARCE_SWARM_F) | (1 << SWARMFLAGS_YANMA_SWARM_F)
            0x22,              # ld [hli], a ; wSwarmFlags
            0xaf,              # xor a
            0x77,              # ld [hl], a ; wSwarmFlags + 1
            0xc9,              # ret
        ], expected=[0x00] * 16),
        # CheckDailyResetTimer: xor a / ld hl, wDailyFlags1 / ld [hli], a x3 / ld [hl], a -> call $0082 / nop x5
        RomPatchEntry(0x04, 0x53db, [0xcd, 0x82, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                      expected=[0xaf, 0x21, 0x5b, 0xdc, 0x22, 0x22, 0x22, 0x77]),
    ]),
    # simple mode incoming calls only start swarms; ending one requires calling the trainer
    RomPatch("Incoming calls don't end swarms", [
        # <Trainer>PhoneCallerScript.Simple: iffalse/sjump <Trainer>_ToggleSwarm -> .TryActivate
        RomPatchEntry(0x2f, 0x59f8, [0xe1, 0x59], expected=[0x0e, 0x5a]),  # Ralph
        RomPatchEntry(0x2f, 0x5a02, [0xe1, 0x59], expected=[0x0e, 0x5a]),
        RomPatchEntry(0x2f, 0x5bb6, [0x9f, 0x5b], expected=[0xcc, 0x5b]),  # Anthony
        RomPatchEntry(0x2f, 0x5bc0, [0x9f, 0x5b], expected=[0xcc, 0x5b]),
        RomPatchEntry(0x2f, 0x5e1d, [0x06, 0x5e], expected=[0x33, 0x5e]),  # Arnie
        RomPatchEntry(0x2f, 0x5e27, [0x06, 0x5e], expected=[0x33, 0x5e]),
    ]),
]
