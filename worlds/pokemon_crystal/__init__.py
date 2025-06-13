import copy
import logging
import pkgutil
from collections import defaultdict
from threading import Event
from typing import ClassVar, Any

import settings
from BaseClasses import Tutorial, ItemClassification, MultiWorld
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import World, WebWorld
from .client import PokemonCrystalClient
from .data import PokemonData, TrainerData, MiscData, TMHMData, data as crystal_data, StaticPokemon, \
    MusicData, MoveData, FlyRegion, TradeData, MiscOption, APWORLD_VERSION, POKEDEX_OFFSET, StartingTown, \
    LogicalAccess, EncounterKey, EncounterMon
from .items import PokemonCrystalItem, create_item_label_to_code_map, get_item_classification, ITEM_GROUPS, \
    item_const_name_to_id, item_const_name_to_label
from .level_scaling import perform_level_scaling
from .locations import create_locations, PokemonCrystalLocation, create_location_label_to_id_map, LOCATION_GROUPS
from .misc import randomize_mischief, get_misc_spoiler_log
from .moves import randomize_tms, randomize_move_values, randomize_move_types
from .music import randomize_music
from .options import PokemonCrystalOptions, JohtoOnly, RandomizeBadges, Goal, HMBadgeRequirements, Route32Condition, \
    LevelScaling, RedGyaradosAccess, FreeFlyLocation, EliteFourRequirement, MtSilverRequirement, RedRequirement, \
    EarlyFly, Route44AccessRequirement, BlackthornDarkCaveAccess, RadioTowerRequirement, RequireItemfinder
from .phone import generate_phone_traps
from .phone_data import PhoneScript
from .pokemon import randomize_pokemon_data, randomize_starters, randomize_traded_pokemon, \
    fill_wild_encounter_locations, generate_breeding_data, generate_evolution_data
from .regions import create_regions, setup_free_fly_regions
from .rom import generate_output, PokemonCrystalProcedurePatch
from .rules import set_rules
from .trainers import boost_trainer_pokemon, randomize_trainers, vanilla_trainer_movesets
from .utils import get_random_filler_item, get_free_fly_locations, get_random_ball, get_random_starting_town, \
    adjust_options
from .wild import randomize_wild_pokemon, randomize_static_pokemon


class PokemonCrystalSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        description = "Pokemon Crystal (UE) (V1.0 or V1.1) ROM File"
        copy_to = "Pokemon - Crystal Version (UE) [C][!].gbc"
        md5s = PokemonCrystalProcedurePatch.hash

    rom_file: RomFile = RomFile(RomFile.copy_to)


class PokemonCrystalWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokemon Crystal with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AliceMousie", "gerbiljames"]
    )]


class PokemonCrystalWorld(World):
    """Pokémon Crystal is the culmination of the Generation I and II Pokémon games.
    Explore the Johto and Kanto regions, become the Pokémon League Champion, and
    defeat the elusive Red at the peak of Mt. Silver!"""
    game = "Pokemon Crystal"
    apworld_version = APWORLD_VERSION

    topology_present = True
    web = PokemonCrystalWebWorld()

    settings_key = "pokemon_crystal_settings"
    settings: ClassVar[PokemonCrystalSettings]

    options_dataclass = PokemonCrystalOptions
    options: PokemonCrystalOptions

    required_client_version = (0, 6, 0)

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()
    item_name_groups = ITEM_GROUPS  # item_groups
    location_name_groups = LOCATION_GROUPS  # location groups

    auth: bytes

    free_fly_location: FlyRegion
    map_card_fly_location: FlyRegion

    starting_town: StartingTown

    generated_moves: dict[str, MoveData]
    generated_pokemon: dict[str, PokemonData]

    generated_trainers: dict[str, TrainerData]

    generated_tms: dict[str, TMHMData]
    generated_wild: dict[EncounterKey, list[EncounterMon]]
    generated_wild_region_logic: dict[EncounterKey, LogicalAccess]
    generated_static: dict[EncounterKey, StaticPokemon]
    generated_trades: list[TradeData]

    generated_dexsanity: set[str]
    generated_dexcountsanity: list[int]
    generated_wooper: str
    generated_starters: tuple[list[str], list[str], list[str]]
    generated_starter_helditems: tuple[str, str, str]
    generated_palettes: dict[str, list[int]]
    generated_breeding: dict[str, set[str]]

    generated_music: MusicData
    generated_misc: MiscData

    generated_phone_traps: list[PhoneScript]
    generated_phone_indices: list[int]

    encounter_name_list: list[str]
    encounter_level_list: list[int]
    trainer_name_list: list[str]
    trainer_level_list: list[int]
    trainer_name_level_dict: dict[str, int]

    blocklisted_moves: set

    finished_level_scaling: Event

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.generated_moves = crystal_data.moves.copy()
        self.generated_pokemon = crystal_data.pokemon.copy()
        self.generated_trainers = crystal_data.trainers.copy()
        self.generated_tms = crystal_data.tmhm.copy()
        self.generated_wild = {key: encounters.copy() for key, encounters in crystal_data.wild.items()}
        self.generated_wild_region_logic = defaultdict(lambda: LogicalAccess.Inaccessible)
        self.generated_static = crystal_data.static.copy()
        self.generated_trades = crystal_data.trades.copy()
        self.generated_dexsanity = set()
        self.generated_dexcountsanity = list()
        self.generated_wooper = "WOOPER"
        self.generated_starters = (["CYNDAQUIL", "QUILAVA", "TYPHLOSION"],
                                   ["TOTODILE", "CROCONAW", "FERALIGATR"],
                                   ["CHIKORITA", "BAYLEEF", "MEGANIUM"])
        self.generated_starter_helditems = ("BERRY", "BERRY", "BERRY")
        self.generated_palettes = {}
        self.generated_breeding = defaultdict(lambda: set())
        self.generated_music = copy.copy(crystal_data.music)
        self.generated_misc = copy.copy(crystal_data.misc)
        self.generated_phone_traps = []
        self.generated_phone_indices = []

        self.trainer_name_list = []
        self.trainer_level_list = []
        self.trainer_name_level_dict = {}
        self.encounter_name_list = []
        self.encounter_level_list = []

        self.blocklisted_moves = set()

        self.logically_available_pokemon = set()

        self.finished_level_scaling = Event()

    def generate_early(self) -> None:
        if self.options.early_fly:
            self.multiworld.local_early_items[self.player]["HM02 Fly"] = 1
            if (self.options.hm_badge_requirements.value != HMBadgeRequirements.option_no_badges
                    and "Fly" not in self.options.remove_badge_requirement.value
                    and self.options.randomize_badges == RandomizeBadges.option_completely_random):
                self.multiworld.local_early_items[self.player]["Storm Badge"] = 1

        adjust_options(self)

        self.blocklisted_moves = {move.replace(" ", "_").upper() for move in self.options.move_blocklist.value}

    def create_regions(self) -> None:
        if self.options.randomize_starting_town:
            get_random_starting_town(self)

        regions = create_regions(self)

        randomize_wild_pokemon(self)
        randomize_static_pokemon(self)
        randomize_pokemon_data(self)
        randomize_starters(self)
        generate_evolution_data(self)
        generate_breeding_data(self)

        create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

        if self.options.free_fly_location:
            get_free_fly_locations(self)
            setup_free_fly_regions(self)

    def create_items(self) -> None:
        item_locations = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None and location.address < POKEDEX_OFFSET
        ]

        if self.options.randomize_badges.value == RandomizeBadges.option_shuffle:
            item_locations = [location for location in item_locations if "Badge" not in location.tags]

        badge_option_counts = [8]
        if self.options.radio_tower_requirement == RadioTowerRequirement.option_badges:
            badge_option_counts.append(self.options.radio_tower_count.value)
        if self.options.elite_four_requirement == EliteFourRequirement.option_badges:
            badge_option_counts.append(self.options.elite_four_count.value)
        if self.options.route_44_access_requirement.value == Route44AccessRequirement.option_badges:
            badge_option_counts.append(self.options.route_44_access_count.value)

        if self.options.johto_only.value == JohtoOnly.option_include_silver_cave:
            if self.options.mt_silver_requirement.value == MtSilverRequirement.option_badges:
                badge_option_counts.append(self.options.mt_silver_count.value)
            if self.options.red_requirement.value == RedRequirement.option_badges:
                badge_option_counts.append(self.options.red_count.value)

        required_badges = max(badge_option_counts)

        add_items = []
        # Extra badges to add to the pool in johto only
        if self.options.johto_only and required_badges > 8:
            kanto_badges = [item_data.item_const for item_data in crystal_data.items.values() if
                            "KantoBadge" in item_data.tags]
            self.random.shuffle(kanto_badges)
            add_items.extend(kanto_badges[:required_badges - 8])

        if self.options.johto_only:
            add_items.append("SUPER_ROD")

        trap_names, trap_weights = zip(
            ("Phone Trap", self.options.phone_trap_weight.value),
            ("Sleep Trap", self.options.sleep_trap_weight.value),
            ("Poison Trap", self.options.poison_trap_weight.value),
            ("Burn Trap", self.options.burn_trap_weight.value),
            ("Freeze Trap", self.options.freeze_trap_weight.value),
            ("Paralysis Trap", self.options.paralysis_trap_weight.value),
        )
        total_trap_weight = sum(trap_weights)

        def get_random_trap():
            return self.create_item(self.random.choices(trap_names, trap_weights)[0])

        default_itempool = []

        for location in item_locations:
            item_code = location.default_item_code
            if item_code > 0 and get_item_classification(item_code) != ItemClassification.filler:
                default_itempool.append(self.create_item_by_code(item_code))
            elif add_items:
                default_itempool.append(self.create_item_by_const_name(add_items.pop()))
            elif self.random.randint(0, 100) < total_trap_weight:
                default_itempool.append(get_random_trap())
            elif item_code == 0:  # item is NO_ITEM, trainersanity checks
                default_itempool.append(self.create_item_by_const_name(get_random_filler_item(self.random)))
            else:
                default_itempool.append(self.create_item_by_code(item_code))

        if self.options.dexsanity:
            default_itempool.extend(
                self.create_item_by_const_name(get_random_ball(self.random)) if
                self.random.randint(0, 100) >= total_trap_weight else get_random_trap()
                for _ in self.generated_dexsanity)

        if self.generated_dexcountsanity:
            default_itempool.extend(
                self.create_item_by_const_name(get_random_ball(self.random)) if
                self.random.randint(0, 100) >= total_trap_weight else get_random_trap()
                for _ in self.generated_dexcountsanity)

        if self.options.johto_only.value != JohtoOnly.option_off:
            # Replace the S.S. Ticket with the Silver Wing for Johto only seeds
            default_itempool = [item if item.name != "S.S. Ticket" else self.create_item_by_const_name("SILVER_WING")
                                for item in default_itempool]

        self.multiworld.itempool.extend(default_itempool)

    def set_rules(self) -> None:
        set_rules(self)

    def pre_fill(self) -> None:
        if self.options.randomize_badges.value == RandomizeBadges.option_shuffle:
            badge_locs = [loc for loc in self.multiworld.get_locations(self.player) if "Badge" in loc.tags]
            badge_items = [self.create_item_by_code(loc.default_item_code) for loc in badge_locs]
            if self.options.early_fly and "Fly" not in self.options.remove_badge_requirement.value:
                early_badge_locs = [loc for loc in
                                    self.multiworld.get_reachable_locations(self.multiworld.state, self.player) if
                                    "Badge" in loc.tags]
                # take one of the early badge locations, set it to storm badge
                if early_badge_locs:
                    storm_loc = self.random.choice(early_badge_locs)
                    storm_badge = next(item for item in badge_items if item.name == "Storm Badge")
                    storm_loc.place_locked_item(storm_badge)
                    badge_locs.remove(storm_loc)
                    badge_items.remove(storm_badge)

            collection_state = self.multiworld.get_all_state(False)

            # If we can't do this in 5 attempts then just accept our fate
            for attempt in range(6):
                attempt_locs = badge_locs.copy()
                attempt_items = badge_items.copy()
                self.random.shuffle(attempt_locs)
                fill_restrictive(self.multiworld, collection_state, attempt_locs, attempt_items,
                                 single_player_placement=True, lock=True, allow_excluded=True, allow_partial=True)
                if not attempt_items and not attempt_locs:
                    break

                if attempt >= 5:
                    raise FillError(
                        f"Failed to shuffle badges for player {self.player} ({self.player_name}). Aborting.")

                for location in badge_locs:
                    location.locked = False
                    if location.item is not None:
                        location.item.location = None
                        location.item = None

                logging.debug(f"Failed to shuffle badges for player {self.player} ({self.player_name}). Retrying.")

        fill_wild_encounter_locations(self)

    def generate_basic(self) -> None:
        randomize_move_values(self)
        randomize_move_types(self)
        randomize_traded_pokemon(self)
        randomize_music(self)
        randomize_mischief(self)
        randomize_tms(self)

        self.auth = self.random.randbytes(16)

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        perform_level_scaling(multiworld)

    def generate_output(self, output_directory: str) -> None:
        generate_phone_traps(self)
        self.finished_level_scaling.wait()

        randomize_trainers(self)

        patch = PokemonCrystalProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff4"))
        patch.write_file("basepatch11.bsdiff4", pkgutil.get_data(__name__, "data/basepatch11.bsdiff4"))
        generate_output(self, output_directory, patch)

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data = self.options.as_dict(
            "goal",
            "johto_only",
            "elite_four_requirement",
            "elite_four_count",
            "red_requirement",
            "red_count",
            "randomize_badges",
            "trainersanity",
            "dexsanity",
            "randomize_pokegear",
            "hm_badge_requirements",
            "randomize_berry_trees",
            "remove_ilex_cut_tree",
            "radio_tower_requirement",
            "radio_tower_count",
            "route_44_access_requirement",
            "route_44_access_count",
            "route_32_condition",
            "mt_silver_requirement",
            "mt_silver_count",
            "east_west_underground",
            "undergrounds_require_power",
            "red_gyarados_access",
            "route_2_access",
            "blackthorn_dark_cave_access",
            "national_park_access",
            "kanto_access_requirement",
            "kanto_access_count",
            "route_3_access",
            "vanilla_clair",
            "static_pokemon_required",
            "breeding_methods_required",
            "evolution_gym_levels",
            "rematchsanity",
            "all_pokemon_seen",
            "dexcountsanity_leniency",
            "dexcountsanity_step"
        )
        slot_data["apworld_version"] = self.apworld_version
        slot_data["tea_north"] = 1 if "North" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_east"] = 1 if "East" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_south"] = 1 if "South" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_west"] = 1 if "West" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["dexsanity_count"] = len(self.generated_dexsanity)
        slot_data["dexsanity_pokemon"] = [self.generated_pokemon[poke].id for poke in self.generated_dexsanity]
        wild_encounters = dict[int, set[str]]()  # This should be defaultdict but pickle doesn't like it
        for encounter_key, encounters in self.generated_wild.items():
            for i, encounter in enumerate(encounters):
                dex_id = self.generated_pokemon[encounter.pokemon].id
                if dex_id not in wild_encounters:
                    wild_encounters[dex_id] = set()
                wild_encounters[dex_id].add(f"{encounter_key.region_name()}_{i + 1}")

        for encounter_key, encounter in self.generated_static.items():
            dex_id = self.generated_pokemon[encounter.pokemon].id
            if dex_id not in wild_encounters:
                wild_encounters[dex_id] = set()
            wild_encounters[dex_id].add(f"{encounter_key.region_name()}_1")

        slot_data["wild_encounters"] = wild_encounters

        for hm in self.options.remove_badge_requirement.valid_keys:
            slot_data["free_" + hm.lower()] = 1 if hm in self.options.remove_badge_requirement.value else 0

        slot_data["free_fly_location"] = 0
        slot_data["map_card_fly_location"] = 0

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                    FreeFlyLocation.option_free_fly_and_map_card):
            slot_data["free_fly_location"] = self.free_fly_location.id

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                    FreeFlyLocation.option_map_card):
            slot_data["map_card_fly_location"] = self.map_card_fly_location.id

        slot_data["enable_mischief"] = 1 if (self.options.enable_mischief
                                             and MiscOption.SecretSwitch.value in self.generated_misc.selected) else 0

        slot_data["starting_town"] = 0
        if self.options.randomize_starting_town:
            slot_data["starting_town"] = self.starting_town.id

        slot_data["dexcountsanity"] = self.generated_dexcountsanity[-1] if self.generated_dexcountsanity else 0
        slot_data["dexcountsanity_checks"] = len(self.generated_dexcountsanity)
        slot_data["dexcountsanity_counts"] = self.generated_dexcountsanity

        slot_data["encmethod_land"] = 1 if "Land" in self.options.wild_encounter_methods_required else 0
        slot_data["encmethod_water"] = 1 if "Surfing" in self.options.wild_encounter_methods_required else 0
        slot_data["encmethod_fishing"] = 1 if "Fishing" in self.options.wild_encounter_methods_required else 0
        slot_data["encmethod_headbutt"] = 1 if "Headbutt" in self.options.wild_encounter_methods_required else 0
        slot_data["encmethod_rocksmash"] = 1 if "Rock Smash" in self.options.wild_encounter_methods_required else 0

        slot_data["evomethod_happiness"] = 1 if "Happiness" in self.options.evolution_methods_required else 0
        slot_data["evomethod_level"] = 1 if "Level" in self.options.evolution_methods_required else 0
        slot_data["evomethod_tyrogue"] = 1 if "Level Tyrogue" in self.options.evolution_methods_required else 0
        slot_data["evomethod_useitem"] = 1 if "Use Item" in self.options.evolution_methods_required else 0

        if not self.options.randomize_hidden_items:
            if not self.options.require_itemfinder:
                hidden_items_setting = 0
            elif self.options.require_itemfinder.value == RequireItemfinder.option_logically_required:
                hidden_items_setting = 1
            else:
                hidden_items_setting = 2
        else:
            if not self.options.require_itemfinder:
                hidden_items_setting = 3
            elif self.options.require_itemfinder.value == RequireItemfinder.option_logically_required:
                hidden_items_setting = 4
            else:
                hidden_items_setting = 5

        slot_data["hiddenitem_logic"] = hidden_items_setting

        return slot_data

    def modify_multidata(self, multidata: dict[str, Any]):
        import base64
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] \
            = multidata["connect_names"][self.player_name]

    def write_spoiler(self, spoiler_handle) -> None:
        if self.options.randomize_starters:
            spoiler_handle.write(f"\n\nStarter Pokemon ({self.multiworld.player_name[self.player]}):\n\n")
            for evo in self.generated_starters:
                types_0 = ", ".join(self.generated_pokemon[evo[0]].types)
                types_1 = ", ".join(self.generated_pokemon[evo[1]].types)
                types_2 = ", ".join(self.generated_pokemon[evo[2]].types)
                spoiler_handle.write(f"{evo[0]} ({types_0}) -> {evo[1]} ({types_1}) -> {evo[2]} ({types_2})\n")

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                    FreeFlyLocation.option_free_fly_and_map_card):
            spoiler_handle.write(f"\n\n")
            spoiler_handle.write(f"Free Fly Location ({self.multiworld.player_name[self.player]}): "
                                 f"{self.free_fly_location.name}\n")

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                    FreeFlyLocation.option_map_card):
            spoiler_handle.write(f"Map Card Fly Location ({self.multiworld.player_name[self.player]}): "
                                 f"{self.map_card_fly_location.name}\n")

        if self.options.randomize_starting_town:
            spoiler_handle.write(f"Starting Town ({self.multiworld.player_name[self.player]}): "
                                 f"{self.starting_town.name}\n")

        if self.options.enable_mischief:
            spoiler_handle.write(f"\n\nMischief ({self.multiworld.player_name[self.player]}):\n\n")
            get_misc_spoiler_log(self, spoiler_handle.write)

    def create_item(self, name: str) -> PokemonCrystalItem:
        return self.create_item_by_code(self.item_name_to_id[name])

    def get_filler_item_name(self) -> str:
        item = get_random_filler_item(self.random)
        return item_const_name_to_label(item)

    def create_item_by_const_name(self, item_const: str) -> PokemonCrystalItem:
        item_code = item_const_name_to_id(item_const)
        return self.create_item_by_code(item_code)

    def create_item_by_code(self, item_code: int) -> PokemonCrystalItem:
        return PokemonCrystalItem(
            self.item_id_to_name[item_code],
            get_item_classification(item_code),
            item_code,
            self.player
        )

    def create_event(self, name: str) -> PokemonCrystalItem:
        return PokemonCrystalItem(
            name,
            ItemClassification.progression,
            None,
            self.player
        )
