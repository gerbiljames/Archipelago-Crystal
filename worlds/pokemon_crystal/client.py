import time
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from .data import data, APWORLD_VERSION, POKEDEX_OFFSET, POKEDEX_COUNT_OFFSET
from .options import Goal

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

TRACKER_EVENT_FLAGS = [
    "EVENT_GOT_KENYA",
    "EVENT_GAVE_KENYA",
    "EVENT_JASMINE_RETURNED_TO_GYM",
    "EVENT_DECIDED_TO_HELP_LANCE",
    "EVENT_CLEARED_ROCKET_HIDEOUT",
    "EVENT_CLEARED_RADIO_TOWER",
    "EVENT_BEAT_ELITE_FOUR",
    "EVENT_RESTORED_POWER_TO_KANTO",
    "EVENT_BLUE_GYM_TRACKER",
    "EVENT_BEAT_RED",
    "EVENT_CLEARED_SLOWPOKE_WELL",
    "EVENT_HERDED_FARFETCHD",
    "EVENT_RELEASED_THE_BEASTS",
    "EVENT_BEAT_FALKNER",
    "EVENT_BEAT_BUGSY",
    "EVENT_BEAT_WHITNEY",
    "EVENT_BEAT_MORTY",
    "EVENT_BEAT_JASMINE",
    "EVENT_BEAT_CHUCK",
    "EVENT_BEAT_PRYCE",
    "EVENT_BEAT_CLAIR",
    "EVENT_BEAT_BROCK",
    "EVENT_BEAT_MISTY",
    "EVENT_BEAT_LTSURGE",
    "EVENT_BEAT_ERIKA",
    "EVENT_BEAT_JANINE",
    "EVENT_BEAT_SABRINA",
    "EVENT_BEAT_BLAINE",
    "EVENT_BEAT_BLUE",
    "EVENT_FAST_SHIP_FOUND_GIRL",
    "EVENT_FOUGHT_SNORLAX",
    "EVENT_MET_BILL"
]

EVENT_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_EVENT_FLAGS}

TRACKER_STATIC_EVENT_FLAGS = [
    "EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE",
    "EVENT_FOUGHT_SUDOWOODO",
    "EVENT_LAKE_OF_RAGE_RED_GYARADOS",
    "EVENT_FOUGHT_HO_OH",
    "EVENT_FOUGHT_LUGIA",
    "EVENT_FOUGHT_SUICUNE",
    "EVENT_TEAM_ROCKET_BASE_B2F_ELECTRODE_1",
    "EVENT_TEAM_ROCKET_BASE_B2F_ELECTRODE_2",
    "EVENT_TEAM_ROCKET_BASE_B2F_ELECTRODE_3",
    "EVENT_GOT_SHUCKIE",
    "EVENT_GOT_EEVEE",
    "EVENT_GOT_DRATINI",
    "EVENT_TOGEPI_HATCHED",
    "EVENT_GOT_TYROGUE_FROM_KIYO",
    "EVENT_UNION_CAVE_B2F_LAPRAS",
    "EVENT_FOUGHT_CELEBI",
    "EVENT_GOT_ODD_EGG"
]

STATIC_EVENT_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_STATIC_EVENT_FLAGS}

TRACKER_ROCKET_TRAP_EVENTS = [
    "EVENT_EXPLODING_TRAP_1",
    "EVENT_EXPLODING_TRAP_2",
    "EVENT_EXPLODING_TRAP_3",
    "EVENT_EXPLODING_TRAP_4",
    "EVENT_EXPLODING_TRAP_5",
    "EVENT_EXPLODING_TRAP_6",
    "EVENT_EXPLODING_TRAP_7",
    "EVENT_EXPLODING_TRAP_8",
    "EVENT_EXPLODING_TRAP_9",
    "EVENT_EXPLODING_TRAP_10",
    "EVENT_EXPLODING_TRAP_11",
    "EVENT_EXPLODING_TRAP_12",
    "EVENT_EXPLODING_TRAP_13",
    "EVENT_EXPLODING_TRAP_14",
    "EVENT_EXPLODING_TRAP_15",
    "EVENT_EXPLODING_TRAP_16",
    "EVENT_EXPLODING_TRAP_17",
    "EVENT_EXPLODING_TRAP_18",
    "EVENT_EXPLODING_TRAP_19",
    "EVENT_EXPLODING_TRAP_20",
    "EVENT_EXPLODING_TRAP_21",
    "EVENT_EXPLODING_TRAP_22"
]

ROCKET_TRAP_EVENT_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_ROCKET_TRAP_EVENTS}

TRACKER_KEY_ITEM_FLAGS = [
    "EVENT_ZEPHYR_BADGE_FROM_FALKNER",
    "EVENT_HIVE_BADGE_FROM_BUGSY",
    "EVENT_PLAIN_BADGE_FROM_WHITNEY",
    "EVENT_FOG_BADGE_FROM_MORTY",
    "EVENT_STORM_BADGE_FROM_CHUCK",
    "EVENT_MINERAL_BADGE_FROM_JASMINE",
    "EVENT_GLACIER_BADGE_FROM_PRYCE",
    "EVENT_RISING_BADGE_FROM_CLAIR",
    "EVENT_BOULDER_BADGE_FROM_BROCK",
    "EVENT_CASCADE_BADGE_FROM_MISTY",
    "EVENT_THUNDER_BADGE_FROM_LTSURGE",
    "EVENT_RAINBOW_BADGE_FROM_ERIKA",
    "EVENT_SOUL_BADGE_FROM_JANINE",
    "EVENT_MARSH_BADGE_FROM_SABRINA",
    "EVENT_VOLCANO_BADGE_FROM_BLAINE",
    "EVENT_EARTH_BADGE_FROM_BLUE",

    "EVENT_GOT_RADIO_CARD",
    "EVENT_GOT_MAP_CARD",
    "EVENT_GOT_PHONE_CARD",
    "EVENT_GOT_EXPN_CARD",
    "EVENT_GOT_POKEGEAR",
    "EVENT_GOT_POKEDEX",
    "EVENT_MART_ESCAPE_ROPE",
    "EVENT_MART_WATER_STONE"
]
KEY_ITEM_FLAG_MAP = {data.event_flags[event]: event for event in TRACKER_KEY_ITEM_FLAGS}

DEATH_LINK_MASK = 0b00010000
DEATH_LINK_SETTING_ADDR = data.ram_addresses["wArchipelagoOptions"] + 4
COUNT_ALL_POKEMON = len(data.pokemon)

INVERTED_EVENTS = {
    "EVENT_MET_BILL"
}

INVERTED_EVENT_IDS = {data.event_flags[event] for event in INVERTED_EVENTS}


class PokemonCrystalClient(BizHawkClient):
    game = "Pokemon Crystal"
    system = ("GB", "GBC")
    patch_suffix = ".apcrystal"

    local_checked_locations: set[int]
    goal_flag: int | None
    local_set_events: dict[str, bool]
    local_set_static_events: dict[str, bool]
    local_set_rocket_trap_events: dict[str, bool]
    local_found_key_items: dict[str, bool]
    local_pokemon: dict[str, list[int]]
    phone_trap_locations: list[int]
    current_map: list[int]
    last_death_link: float

    def initialize_client(self) -> None:
        self.local_checked_locations = set()
        self.goal_flag = None
        self.local_set_events = dict()
        self.local_set_static_events = dict()
        self.local_set_rocket_trap_events = dict()
        self.local_found_key_items = dict()
        self.local_pokemon = {"seen": list(), "caught": list()}
        self.phone_trap_locations = list()
        self.current_map = [0, 0]
        self.last_death_link = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:

            # Check we're operating on a 2MB ROM
            if await bizhawk.get_memory_size(ctx.bizhawk_ctx, "ROM") != 2097152: return False

            # Check ROM name/patch version
            rom_info = ((await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_ROM_Header"], 11, "ROM"),
                                                              (data.rom_addresses["AP_ROM_Version"], 2, "ROM"),
                                                              (data.rom_addresses["AP_ROM_Revision"], 1, "ROM"),
                                                              (data.rom_addresses["AP_Setting_RemoteItems"], 1, "ROM"),
                                                              (data.rom_addresses["AP_Version"], 32, "ROM")
                                                              ])))

            rom_name = bytes([byte for byte in rom_info[0] if byte != 0]).decode("ascii")
            rom_version = int.from_bytes(rom_info[1], "little")
            rom_revision = int.from_bytes(rom_info[2], "little")
            remote_items = int.from_bytes(rom_info[3], "little")

            if rom_name == "PM_CRYSTAL":
                logger.info("ERROR: You appear to be running an unpatched version of Pokemon Crystal. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != "AP_CRYSTAL":
                return False

            required_rom_version = data.rom_version if rom_revision == 0 else data.rom_version_11
            if rom_version != required_rom_version:
                generator_apworld_version = bytes([byte for byte in rom_info[4] if byte != 0]).decode("ascii")
                if not generator_apworld_version:
                    generator_apworld_version = "too old to know"
                generator_version = "{0:x}".format(rom_version)
                client_version = "{0:x}".format(required_rom_version)
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your version of pokemon_crystal.apworld "
                            "against the version used to generate this game.")
                logger.info(f"Client APWorld version: {APWORLD_VERSION}, "
                            f"Generator APWorld version: {generator_apworld_version}")
                logger.info(f"ROM Revision: V1.{rom_revision}, Client checksum: {client_version}, "
                            f"Generator checksum: {generator_version}")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b011 if remote_items else 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_Seed_Auth"], 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        if ctx.slot_data["goal"] == Goal.option_elite_four:
            self.goal_flag = data.event_flags["EVENT_BEAT_ELITE_FOUR"]
        else:
            self.goal_flag = data.event_flags["EVENT_BEAT_RED"]

        try:
            overworld_guard = (data.ram_addresses["wArchipelagoSafeWrite"], [1], "WRAM")

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoItemReceived"], 5, "WRAM")], [overworld_guard])

            if read_result is None:  # Not in overworld
                return

            num_received_items = int.from_bytes([read_result[0][1], read_result[0][2]], "little")
            received_item_is_empty = read_result[0][0] == 0
            phone_trap_index = read_result[0][4]

            if num_received_items < len(ctx.items_received) and received_item_is_empty:
                next_item = ctx.items_received[num_received_items].item
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (data.ram_addresses["wArchipelagoItemReceived"],
                     next_item.to_bytes(1, "little"), "WRAM")
                ])

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wEventFlags"], 0x104, "WRAM"),  # Flags
                 (data.ram_addresses["wArchipelagoPokedexCaught"], 0x20, "WRAM"),
                 (data.ram_addresses["wArchipelagoPokedexSeen"], 0x20, "WRAM")],
                [overworld_guard]
            )

            if read_result is None:
                return

            pokedex_caught_bytes = read_result[1]
            pokedex_seen_bytes = read_result[2]

            game_clear = False
            local_checked_locations = set()
            local_set_events = {flag_name: False for flag_name in TRACKER_EVENT_FLAGS}
            local_set_static_events = {flag_name: False for flag_name in TRACKER_STATIC_EVENT_FLAGS}
            local_set_rocket_trap_events = {flag_name: False for flag_name in TRACKER_ROCKET_TRAP_EVENTS}
            local_found_key_items = {flag_name: False for flag_name in TRACKER_KEY_ITEM_FLAGS}
            local_pokemon: dict[str, list[int]] = {"caught": list(), "seen": list()}

            flag_bytes = read_result[0]
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    location_id = byte_i * 8 + i
                    event_set = byte & (1 << i)
                    invert_event = location_id in INVERTED_EVENT_IDS
                    if (not invert_event and event_set != 0) or (invert_event and event_set == 0):
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if self.goal_flag is not None and location_id == self.goal_flag:
                            game_clear = True

                        if location_id in EVENT_FLAG_MAP:
                            local_set_events[EVENT_FLAG_MAP[location_id]] = True

                        if location_id in STATIC_EVENT_FLAG_MAP:
                            local_set_static_events[STATIC_EVENT_FLAG_MAP[location_id]] = True

                        if location_id in ROCKET_TRAP_EVENT_FLAG_MAP:
                            local_set_rocket_trap_events[ROCKET_TRAP_EVENT_FLAG_MAP[location_id]] = True

                        if location_id in KEY_ITEM_FLAG_MAP:
                            local_found_key_items[KEY_ITEM_FLAG_MAP[location_id]] = True

            for byte_i, byte in enumerate(pokedex_caught_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        dex_number = (byte_i * 8 + i) + 1
                        location_id = dex_number + POKEDEX_OFFSET
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)
                        local_pokemon["caught"].append(dex_number)

            for byte_i, byte in enumerate(pokedex_seen_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        dex_number = (byte_i * 8 + i) + 1
                        local_pokemon["seen"].append(dex_number)

            if local_pokemon != self.local_pokemon and ctx.slot is not None:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_pokemon_{ctx.team}_{ctx.slot}",
                    "default": {},
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": local_pokemon}, ]
                }])
                self.local_pokemon = local_pokemon

            if ctx.slot_data["dexcountsanity_counts"]:
                dex_count = len(local_pokemon["caught"])
                check_counts = ctx.slot_data["dexcountsanity_counts"]

                for count in check_counts[:-1]:
                    location_id = count + POKEDEX_COUNT_OFFSET
                    if dex_count >= count and location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)

                if dex_count >= check_counts[-1]:
                    location_id = COUNT_ALL_POKEMON + POKEDEX_COUNT_OFFSET
                    if location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)

            if local_checked_locations != self.local_checked_locations:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(local_checked_locations)
                }])

                self.local_checked_locations = local_checked_locations

            # Send game clear
            if not ctx.finished_game and game_clear:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

            if not self.phone_trap_locations:
                phone_result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [(data.rom_addresses["AP_Setting_Phone_Trap_Locations"], 0x20, "ROM")],
                    [overworld_guard]
                )
                if phone_result is not None:
                    read_locations = []
                    for i in range(0, 16):
                        loc = int.from_bytes(phone_result[0][i * 2:(i + 1) * 2], "little")
                        read_locations.append(loc)
                    self.phone_trap_locations = read_locations
            else:
                hint_locations = [location for location in self.phone_trap_locations[:phone_trap_index] if
                                  location != 0
                                  and location not in ctx.locations_scouted
                                  and location not in local_checked_locations
                                  and location not in ctx.checked_locations]
                if hint_locations:
                    await ctx.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": hint_locations,
                        "create_as_hint": 2
                    }])

            if local_set_events != self.local_set_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_EVENT_FLAGS):
                    if local_set_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_events_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_set_events = local_set_events

            if local_set_static_events != self.local_set_static_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_STATIC_EVENT_FLAGS):
                    if local_set_static_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_statics_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_set_static_events = local_set_static_events

            if local_set_rocket_trap_events != self.local_set_rocket_trap_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_ROCKET_TRAP_EVENTS):
                    if local_set_rocket_trap_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_rockettraps_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_set_rocket_trap_events = local_set_rocket_trap_events

            if local_found_key_items != self.local_found_key_items:
                key_bitfield = 0
                for i, location_name in enumerate(TRACKER_KEY_ITEM_FLAGS):
                    if local_found_key_items[location_name]:
                        key_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_keys_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": key_bitfield}],
                }])
                self.local_found_key_items = local_found_key_items

            await self.handle_death_link(ctx, overworld_guard)

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wMapGroup"], 2, "WRAM")],  # Current Map
                [overworld_guard]
            )

            if read_result is not None:
                current_map = [int(x) for x in read_result[0]]
                if self.current_map != current_map:
                    self.current_map = current_map
                    message = [{"cmd": "Bounce", "slots": [ctx.slot],
                                "data": {"mapGroup": current_map[0], "mapNumber": current_map[1]}}]
                    await ctx.send_msgs(message)

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def handle_death_link(self, ctx: "BizHawkClientContext", guard):

        death_link_setting_status = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [(DEATH_LINK_SETTING_ADDR, 1, "WRAM")],
            [guard]
        )

        if death_link_setting_status and death_link_setting_status[0][0] & DEATH_LINK_MASK:

            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
                self.last_death_link = ctx.last_death_link
                await bizhawk.write(ctx.bizhawk_ctx,
                                    [(data.ram_addresses["wArchipelagoDeathLink"], [0], "WRAM")])

            death_link_status = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wArchipelagoDeathLink"], 1, "WRAM")], [guard])

            if not death_link_status: return

            if death_link_status[0][0] == 1:
                await ctx.send_death(ctx.player_names[ctx.slot] + " is out of usable Pokémon! "
                                     + ctx.player_names[ctx.slot] + " whited out!")
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoDeathLink"], [0], "WRAM")])
                self.last_death_link = time.time()
            elif ctx.last_death_link > self.last_death_link and not death_link_status[0][0]:
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoDeathLink"], [2], "WRAM")])
                self.last_death_link = ctx.last_death_link

        elif "DeathLink" in ctx.tags:
            await ctx.update_death_link(False)
            self.last_death_link = 0
