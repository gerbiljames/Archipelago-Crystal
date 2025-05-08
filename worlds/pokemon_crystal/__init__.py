import copy
import logging
import pkgutil
from threading import Event
from typing import List, ClassVar, Dict, Any, Tuple

import settings
from BaseClasses import Tutorial, ItemClassification, MultiWorld
from Fill import fill_restrictive, FillError
from Options import Toggle
from worlds.AutoWorld import World, WebWorld
from .client import PokemonCrystalClient
from .data import PokemonData, TrainerData, MiscData, TMHMData, data as crystal_data, \
    WildData, StaticPokemon, MusicData, MoveData, FlyRegion, TradeData, MiscOption
from .items import PokemonCrystalItem, create_item_label_to_code_map, get_item_classification, \
    ITEM_GROUPS, item_const_name_to_id, item_const_name_to_label
from .level_scaling import perform_level_scaling
from .locations import create_locations, PokemonCrystalLocation, create_location_label_to_id_map
from .misc import misc_activities, get_misc_spoiler_log
from .moves import randomize_tms, randomize_move_values, randomize_move_types
from .music import randomize_music
from .options import PokemonCrystalOptions, JohtoOnly, RandomizeBadges, Goal, HMBadgeRequirements, Route32Condition, \
    LevelScaling, RedGyaradosAccess, FreeFlyLocation
from .phone import generate_phone_traps
from .phone_data import PhoneScript
from .pokemon import randomize_pokemon, randomize_starters, randomize_traded_pokemon
from .regions import create_regions, setup_free_fly_regions
from .rom import generate_output, PokemonCrystalProcedurePatch
from .rules import set_rules
from .trainers import boost_trainer_pokemon, randomize_trainers, vanilla_trainer_movesets
from .utils import get_random_filler_item, get_free_fly_locations
from .wild import randomize_wild_pokemon, randomize_static_pokemon


class PokemonCrystalSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        description = "Pokemon Crystal (UE) (V1.0 or V1.1) ROM File"
        copy_to = "Pokemon - Crystal Version (UE) [C][!].gbc"
        md5s = ["9f2922b235a5eeb78d65594e82ef5dde", "301899b8087289a6436b0a241fbbb474"]

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
    apworld_version = "3.2.2"

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

    free_fly_location: FlyRegion
    map_card_fly_location: FlyRegion
    generated_moves = Dict[str, MoveData]
    generated_pokemon: Dict[str, PokemonData]
    generated_starters: Tuple[List[str], List[str], List[str]]
    generated_starter_helditems: Tuple[str, str, str]
    generated_trainers: Dict[str, TrainerData]
    generated_palettes: Dict[str, List[int]]
    generated_phone_traps: List[PhoneScript]
    generated_phone_indices: List[int]
    generated_misc: MiscData
    generated_tms: Dict[str, TMHMData]
    generated_wild: WildData
    generated_music: MusicData
    generated_wooper: str
    generated_static: Dict[str, StaticPokemon]
    generated_trades: List[TradeData]
    encounter_name_list: List[str]
    encounter_level_list: List[int]
    trainer_name_list: List[str]
    trainer_level_list: List[int]
    trainer_name_level_dict: Dict[str, int]

    blocklisted_moves: set

    finished_level_scaling: Event

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.generated_moves = copy.deepcopy(crystal_data.moves)
        self.generated_trainers = copy.deepcopy(crystal_data.trainers)
        self.generated_misc = copy.deepcopy(crystal_data.misc)
        self.generated_tms = copy.deepcopy(crystal_data.tmhm)
        self.generated_wild = copy.deepcopy(crystal_data.wild)
        self.generated_static = copy.deepcopy(crystal_data.static)
        self.generated_trades = copy.deepcopy(crystal_data.trades)
        self.generated_music = copy.deepcopy(crystal_data.music)
        self.generated_pokemon = copy.deepcopy(crystal_data.pokemon)
        self.generated_starters = (["CYNDAQUIL", "QUILAVA", "TYPHLOSION"],
                                   ["TOTODILE", "CROCONAW", "FERALIGATR"],
                                   ["CHIKORITA", "BAYLEEF", "MEGANIUM"])
        self.generated_starter_helditems = ("BERRY", "BERRY", "BERRY")
        self.generated_palettes = {}
        self.generated_phone_traps = []
        self.generated_phone_indices = []
        self.generated_wooper = "WOOPER"
        self.trainer_name_list = []
        self.trainer_level_list = []
        self.trainer_name_level_dict = {}
        self.encounter_name_list = []
        self.encounter_level_list = []

        self.blocklisted_moves = set()

        self.finished_level_scaling = Event()

    def generate_early(self) -> None:
        if self.options.early_fly:
            self.multiworld.local_early_items[self.player]["HM02 Fly"] = 1
            if (self.options.hm_badge_requirements.value != HMBadgeRequirements.option_no_badges
                    and "Fly" not in self.options.remove_badge_requirement.value
                    and self.options.randomize_badges == RandomizeBadges.option_completely_random):
                self.multiworld.local_early_items[self.player]["Storm Badge"] = 1

        if self.options.randomize_badges.value != RandomizeBadges.option_completely_random and self.options.radio_tower_badges.value > (
                7 if self.options.johto_only else 15):
            self.options.radio_tower_badges.value = 7 if self.options.johto_only else 15
            logging.warning(
                "Pokemon Crystal: Radio Tower Badges >%d incompatible with vanilla or shuffled badges. "
                "Changing Radio Tower Badges to %d for player %s.",
                self.options.radio_tower_badges.value,
                self.options.radio_tower_badges.value,
                self.multiworld.get_player_name(self.player))

        if self.options.johto_only:
            if self.options.goal == Goal.option_red and self.options.johto_only == JohtoOnly.option_on:
                self.options.goal.value = Goal.option_elite_four
                logging.warning(
                    "Pokemon Crystal: Red goal is incompatible with Johto Only "
                    "without Silver Cave. Changing goal to Elite Four for player %s.",
                    self.multiworld.get_player_name(self.player))
            if self.options.randomize_badges != RandomizeBadges.option_completely_random:
                if self.options.red_badges.value > 8:
                    self.options.red_badges.value = 8
                    logging.warning(
                        "Pokemon Crystal: Red Badges >8 incompatible with Johto Only "
                        "if badges are not completely random. Changing Red Badges to 8 for player %s.",
                        self.multiworld.get_player_name(self.player))
                if self.options.elite_four_badges.value > 8:
                    self.options.elite_four_badges.value = 8
                    logging.warning(
                        "Pokemon Crystal: Elite Four Badges >8 incompatible with Johto Only "
                        "if badges are not completely random. Changing Elite Four Badges to 8 for player %s.",
                        self.multiworld.get_player_name(self.player))
                if self.options.radio_tower_badges.value > 8:
                    self.options.radio_tower_badges.value = 8
                    logging.warning(
                        "Pokemon Crystal: Radio Tower Badges >8 incompatible with Johto Only "
                        "if badges are not completely random. Changing Radio Tower Badges to 8 for player %s.",
                        self.multiworld.get_player_name(self.player))
                if self.options.mt_silver_badges.value > 8:
                    self.options.mt_silver_badges.value = 8
                    logging.warning(
                        "Pokemon Crystal: Mt. Silver Badges >8 incompatible with Johto Only "
                        "if badges are not completely random. Changing Mt. Silver Badges to 8 for player %s.",
                        self.multiworld.get_player_name(self.player))

        if (self.options.red_gyarados_access
                and self.options.randomize_badges.value == RandomizeBadges.option_vanilla
                and "Whirlpool" and not self.options.hm_badge_requirements == HMBadgeRequirements.option_no_badges
                and "Whirlpool" not in self.options.remove_badge_requirement):
            self.options.red_gyarados_access.value = RedGyaradosAccess.option_vanilla
            logging.warning("Pokemon Crystal: Red Gyarados access requires Whirlpool and Vanilla Badges are not "
                            "compatible, setting Red Gyarados access to vanilla for player %s.",
                            self.multiworld.get_player_name(self.player))

        # In race mode we don't patch any item location information into the ROM
        if self.multiworld.is_race and not self.options.remote_items:
            logging.warning("Pokemon Crystal: Forcing Player %s (%s) to use remote items due to race mode.",
                            self.player, self.player_name)
            self.options.remote_items.value = Toggle.option_true

        self.blocklisted_moves = {move.replace(" ", "_").upper() for move in self.options.move_blocklist.value}

    def create_regions(self) -> None:
        regions = create_regions(self)
        create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())
        if self.options.free_fly_location:
            get_free_fly_locations(self)
            setup_free_fly_regions(self)

    def create_items(self) -> None:
        item_locations = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ]

        if self.options.randomize_badges.value == RandomizeBadges.option_shuffle:
            item_locations = [location for location in item_locations if "Badge" not in location.tags]

        total_badges = max(self.options.elite_four_badges.value, self.options.radio_tower_badges.value)
        if self.options.johto_only.value == JohtoOnly.option_include_silver_cave:
            total_badges = max(total_badges, self.options.mt_silver_badges.value, self.options.red_badges.value)

        add_badges = []
        # Extra badges to add to the pool in johto only
        if self.options.johto_only and total_badges > 8:
            kanto_badges = [item_id for item_id, item_data in crystal_data.items.items() if
                            "KantoBadge" in item_data.tags]
            self.random.shuffle(kanto_badges)
            add_badges = kanto_badges[:total_badges - 8]

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
                default_itempool += [self.create_item_by_code(item_code)]
            elif add_badges:
                default_itempool += [self.create_item_by_code(add_badges.pop())]
            elif self.random.randint(0, 100) < total_trap_weight:
                default_itempool += [get_random_trap()]
            elif item_code == 0:  # item is NO_ITEM, trainersanity checks
                default_itempool += [self.create_item_by_const_name(get_random_filler_item(self.random))]
            else:
                default_itempool += [self.create_item_by_code(item_code)]

        if self.options.johto_only.value != JohtoOnly.option_off:
            # Replace the S.S. Ticket with the Silver Wing for Johto only seeds
            default_itempool = [item if item.name != "S.S. Ticket" else self.create_item_by_const_name("SILVER_WING")
                                for
                                item in default_itempool]

        self.multiworld.itempool += default_itempool

    def set_rules(self) -> None:
        set_rules(self)

    def pre_fill(self) -> None:
        if self.options.randomize_badges.value == RandomizeBadges.option_shuffle:
            badge_locs = [loc for loc in self.multiworld.get_locations(self.player) if "Badge" in loc.tags]
            badge_items = [self.create_item_by_code(loc.default_item_code) for loc in badge_locs]
            if self.options.early_fly and "Fly" not in self.options.remove_badge_requirement.value:
                # take one of the early badge locations, set it to storm badge
                if self.options.route_32_condition.value == Route32Condition.option_any_badge:
                    early_badge_tag = "EarlyBadge_Route32RequiresBadge"
                elif self.options.remove_ilex_cut_tree:
                    early_badge_tag = "EarlyBadge_RemovedIlexCutTree"
                else:
                    early_badge_tag = "EarlyBadge"
                storm_loc = self.random.choice([loc for loc in badge_locs if early_badge_tag in loc.tags])
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

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        perform_level_scaling(multiworld)

    def generate_output(self, output_directory: str) -> None:

        if self.options.randomize_move_values.value:
            randomize_move_values(self)

        if self.options.randomize_move_types.value:
            randomize_move_types(self)

        if self.options.randomize_trades.value:
            randomize_traded_pokemon(self)

        if self.options.randomize_music.value:
            randomize_music(self)

        if self.options.enable_mischief.value:
            misc_activities(self)

        if self.options.phone_trap_weight.value:
            generate_phone_traps(self)

        if self.options.randomize_tm_moves.value:
            randomize_tms(self)

        randomize_pokemon(self)

        if self.options.randomize_wilds.value:
            randomize_wild_pokemon(self)

        self.finished_level_scaling.wait()

        if self.options.boost_trainers:
            boost_trainer_pokemon(self)

        if self.options.randomize_trainer_parties.value:
            randomize_trainers(self)
        elif self.options.randomize_learnsets.value:
            vanilla_trainer_movesets(self)

        if self.options.randomize_static_pokemon.value:
            randomize_static_pokemon(self)

        patch = PokemonCrystalProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff4"))
        patch.write_file("basepatch11.bsdiff4", pkgutil.get_data(__name__, "data/basepatch11.bsdiff4"))
        generate_output(self, output_directory, patch)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "goal",
            "johto_only",
            "elite_four_badges",
            "red_badges",
            "randomize_badges",
            "randomize_hidden_items",
            "require_itemfinder",
            "trainersanity",
            "randomize_pokegear",
            "hm_badge_requirements",
            "randomize_berry_trees",
            "remove_ilex_cut_tree",
            "radio_tower_badges",
            "route_32_condition",
            "mt_silver_badges",
            "east_west_underground",
            "undergrounds_require_power",
            "red_gyarados_access",
            "route_2_access",
            "blackthorn_dark_cave_access",
            "national_park_access",
            "kanto_access_condition",
            "kanto_access_badges",
            "route_3_access"
        )
        slot_data["apworld_version"] = self.apworld_version
        slot_data["tea_north"] = 1 if "North" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_east"] = 1 if "East" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_south"] = 1 if "South" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_west"] = 1 if "West" in self.options.saffron_gatehouse_tea.value else 0

        for hm in self.options.remove_badge_requirement.valid_keys:
            slot_data["free_" + hm.lower()] = 1 if hm in self.options.remove_badge_requirement.value else 0

        slot_data["free_fly_location"] = 0
        slot_data["map_card_fly_location"] = 0

        if self.options.free_fly_location.value in [FreeFlyLocation.option_free_fly,
                                                    FreeFlyLocation.option_free_fly_and_map_card]:
            slot_data["free_fly_location"] = self.free_fly_location.id

        if self.options.free_fly_location.value in [FreeFlyLocation.option_free_fly_and_map_card,
                                                    FreeFlyLocation.option_map_card]:
            slot_data["map_card_fly_location"] = self.map_card_fly_location.id

        slot_data["enable_mischief"] = 1 if (self.options.enable_mischief
                                             and MiscOption.SecretSwitch.value in self.generated_misc.selected) else 0

        return slot_data

    def write_spoiler(self, spoiler_handle) -> None:
        if self.options.randomize_starters:
            spoiler_handle.write(f"\n\nStarter Pokemon ({self.multiworld.player_name[self.player]}):\n\n")
            for evo in self.generated_starters:
                types_0 = ", ".join(self.generated_pokemon[evo[0]].types)
                types_1 = ", ".join(self.generated_pokemon[evo[1]].types)
                types_2 = ", ".join(self.generated_pokemon[evo[2]].types)
                spoiler_handle.write(f"{evo[0]} ({types_0}) -> {evo[1]} ({types_1}) -> {evo[2]} ({types_2})\n")

        if self.options.free_fly_location.value in [FreeFlyLocation.option_free_fly,
                                                    FreeFlyLocation.option_free_fly_and_map_card]:
            spoiler_handle.write(f"\n\n")
            spoiler_handle.write(f"Free Fly Location ({self.multiworld.player_name[self.player]}): "
                                 f"{self.free_fly_location.name}\n")

        if self.options.free_fly_location.value in [FreeFlyLocation.option_free_fly_and_map_card,
                                                    FreeFlyLocation.option_map_card]:
            spoiler_handle.write(f"Map Card Fly Location ({self.multiworld.player_name[self.player]}): "
                                 f"{self.map_card_fly_location.name}\n")

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
