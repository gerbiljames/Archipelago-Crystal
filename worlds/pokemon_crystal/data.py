import pkgutil
from enum import Enum
from typing import Dict, List, NamedTuple, Set, FrozenSet, Any, Union, Optional

import orjson
import yaml

from BaseClasses import ItemClassification


class ItemData(NamedTuple):
    label: str
    item_id: int
    item_const: str
    classification: ItemClassification
    tags: FrozenSet[str]


class LocationData(NamedTuple):
    name: str
    label: str
    parent_region: str
    default_item: int
    rom_address: int
    flag: int
    tags: FrozenSet[str]
    script: str


class EventData(NamedTuple):
    name: str
    parent_region: str


class TrainerPokemon(NamedTuple):
    level: int
    pokemon: str
    item: Union[str, None]
    moves: List[str]


class TrainerData(NamedTuple):
    name: str
    trainer_type: str
    pokemon: List[TrainerPokemon]
    name_length: int


class LearnsetData(NamedTuple):
    level: int
    move: str


class EvolutionData(NamedTuple):
    evo_type: str
    level: Union[int, None]
    condition: Union[str, None]
    pokemon: str
    length: int


class PokemonData(NamedTuple):
    id: int
    base_stats: List[int]
    types: List[str]
    evolutions: List[EvolutionData]
    learnset: List[LearnsetData]
    tm_hm: List[str]
    is_base: bool
    bst: int


class MoveData(NamedTuple):
    id: str
    rom_id: int
    type: str
    power: int
    accuracy: int
    pp: int
    is_hm: bool
    name: str


class TMHMData(NamedTuple):
    id: str
    tm_num: int
    type: str
    is_hm: bool
    move_id: int


class MiscOption(Enum):
    FuchsiaGym = 0
    SaffronGym = 1
    RadioTowerQuestions = 2
    Amphy = 3
    FanClubChairman = 4
    SecretSwitch = 5
    EcruteakGym = 6
    RedGyarados = 7
    OhkoMoves = 8
    RadioChannels = 9
    MomItems = 10

    @staticmethod
    def all():
        return list(map(lambda c: c.value, MiscOption))


class MiscWarp(NamedTuple):
    coords: List[int]
    id: int


class MiscSaffronWarps(NamedTuple):
    warps: Dict[str, MiscWarp]
    pairs: List[List[str]]


class MiscMomItem(NamedTuple):
    index: int
    item: str


class MiscData(NamedTuple):
    fuchsia_gym_trainers: List[List[int]]
    radio_tower_questions: List[str]
    saffron_gym_warps: MiscSaffronWarps
    radio_channel_addresses: List[int]
    mom_items: List[MiscMomItem]
    selected: List[MiscOption] = MiscOption.all()


class MusicConst(NamedTuple):
    id: int
    loop: bool


class MusicData(NamedTuple):
    consts: Dict[str, MusicConst]
    maps: Dict[str, str]
    encounters: List[str]
    scripts: Dict[str, str]


class EncounterMon(NamedTuple):
    level: int
    pokemon: str


class FishData(NamedTuple):
    old: List[EncounterMon]
    good: List[EncounterMon]
    super: List[EncounterMon]


class TreeMonData(NamedTuple):
    common: List[EncounterMon]
    rare: List[EncounterMon]


class WildData(NamedTuple):
    grass: Dict[str, List[EncounterMon]]
    water: Dict[str, List[EncounterMon]]
    fish: Dict[str, FishData]
    tree: Dict[str, TreeMonData]


class StaticPokemon(NamedTuple):
    name: str
    pokemon: str
    addresses: List[str]
    level: int
    level_type: str
    level_address: Optional[str]


class TradeData(NamedTuple):
    index: int
    requested_pokemon: str
    received_pokemon: str
    requested_gender: int
    held_item: str


class RegionData:
    name: str
    johto: bool
    silver_cave: bool
    exits: List[str]
    warps: List[str]
    trainers: List[TrainerData]
    statics: List[StaticPokemon]
    locations: List[str]
    events: List[EventData]

    def __init__(self, name: str):
        self.name = name
        self.exits = []
        self.warps = []
        self.trainers = []
        self.statics = []
        self.locations = []
        self.events = []


class FlyRegion(NamedTuple):
    id: int
    name: str
    region_id: str

class PhoneScriptData:
    name: str
    caller: str
    script: List[str]

    def __init__(self, name: str, caller: str, script: List[str]):
        self.name = name
        self.caller = caller
        self.script = script

class PokemonCrystalData:
    rom_version: int
    rom_version_11: int
    rom_addresses: Dict[str, int]
    ram_addresses: Dict[str, int]
    event_flags: Dict[str, int]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    items: Dict[int, ItemData]
    trainers: Dict[str, TrainerData]
    pokemon: Dict[str, PokemonData]
    moves: Dict[str, MoveData]
    wild: WildData
    types: List[str]
    type_ids: Dict[str, int]
    tmhm: Dict[str, TMHMData]
    tm_replace_map: List[int]
    misc: MiscData
    music: MusicData
    static: Dict[str, StaticPokemon]
    trades: List[TradeData]
    fly_regions: List[FlyRegion]

    def __init__(self) -> None:
        self.rom_addresses = {}
        self.ram_addresses = {}
        self.event_flags = {}
        self.regions = {}
        self.locations = {}
        self.items = {}
        self.trainers = {}
        self.pokemon = {}
        self.trades = []
        self.moves = {}


class PokemonCrystalGameSetting(NamedTuple):
    option_byte_index: int
    offset: int
    length: int
    values: dict[str, int]
    default: int

    def set_option_byte(self, option_selection: Optional[str], option_bytes: bytearray):
        if option_selection is True:
            option_selection = "on"
        elif option_selection is False:
            option_selection = "off"
        elif isinstance(option_selection, int):
            option_selection = str(option_selection)

        value = self.values.get(option_selection, self.default)
        mask = ((self.length * 2) - 1) << self.offset
        value = (value << self.offset) & mask

        option_bytes[self.option_byte_index] &= ~mask
        option_bytes[self.option_byte_index] |= value


ON_OFF = {"off": 0, "on": 1}
INVERTED_ON_OFF = {"off": 1, "on": 0}


class PokemonCrystalMapSizeData(NamedTuple):
    width: int
    height: int


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))

def load_yaml_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return yaml.safe_load(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))

data = PokemonCrystalData()


def _init() -> None:
    location_data = load_json_data("locations.json")
    regions_json = load_json_data("regions.json")

    items_json = load_json_data("items.json")

    data_json = load_json_data("data.json")
    rom_address_data = data_json["rom_addresses"]
    ram_address_data = data_json["ram_addresses"]
    event_flag_data = data_json["event_flags"]
    item_codes = data_json["items"]
    move_data = data_json["moves"]
    trainer_data = data_json["trainers"]
    wild_data = data_json["wilds"]
    type_data = data_json["types"]
    fuchsia_data = data_json["misc"]["fuchsia_gym_trainers"]
    saffron_data = data_json["misc"]["saffron_gym_warps"]
    radio_addr_data = data_json["misc"]["radio_channel_addresses"]
    mom_items_data = data_json["misc"]["mom_items"]
    tmhm_data = data_json["tmhm"]
    map_size_data = data_json["map_sizes"]

    data.rom_version = data_json["rom_version"]
    data.rom_version_11 = data_json["rom_version11"]

    claimed_locations: Set[str] = set()

    data.trainers = {}

    for trainer_name, trainer_attributes in trainer_data.items():
        trainer_type = trainer_attributes["trainer_type"]
        pokemon = []
        for poke in trainer_attributes["pokemon"]:
            if trainer_type == "TRAINERTYPE_NORMAL":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], None, []))
            elif trainer_type == "TRAINERTYPE_ITEM":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], poke[2], []))
            elif trainer_type == "TRAINERTYPE_MOVES":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], None, poke[2:]))
            else:
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], poke[2], poke[3:]))

        data.trainers[trainer_name] = TrainerData(
            trainer_name,
            trainer_type,
            pokemon,
            trainer_attributes["name_length"]
        )

    data.static = {}
    for static_name, static_data in data_json["static"].items():
        level_type = static_data["type"]
        if level_type == "loadwildmon" or level_type == "givepoke":
            level_address = static_data["addresses"][0]
        elif level_type == "custom":
            level_address = static_data["level_address"]
        else:
            level_address = None
        data.static[static_name] = StaticPokemon(static_name,
                                                 static_data["pokemon"],
                                                 static_data["addresses"],
                                                 static_data["level"],
                                                 static_data["type"],
                                                 level_address)

    data.regions = {}

    for region_name, region_json in regions_json.items():
        new_region = RegionData(region_name)

        # Locations
        for location_name in region_json["locations"]:
            if location_name in claimed_locations:
                raise AssertionError(f"Location [{location_name}] was claimed by multiple regions")
            location_json = location_data[location_name]
            new_location = LocationData(
                location_name,
                location_json["label"],
                region_name,
                item_codes[location_json["default_item"]],
                rom_address_data[location_json["script"]],
                event_flag_data[location_json["flag"]],
                frozenset(location_json["tags"]),
                location_json["script"]
            )
            new_region.locations.append(location_name)
            data.locations[location_name] = new_location
            claimed_locations.add(location_name)

        new_region.locations.sort()
        # events
        for event in region_json["events"]:
            new_region.events.append(EventData(event, region_name))

        # trainers
        if "trainers" in region_json:
            for trainer in region_json["trainers"]:  #
                new_region.trainers.append(data.trainers[trainer])
        #
        # statics
        if "statics" in region_json:
            for static in region_json["statics"]:
                new_region.statics.append(data.static[static])

        # Exits
        for region_exit in region_json["exits"]:
            new_region.exits.append(region_exit)
        new_region.johto = region_json["johto"]
        new_region.silver_cave = region_json["silver_cave"] if "silver_cave" in region_json else False
        data.regions[region_name] = new_region

    # items

    data.items = {}
    data.tm_replace_map = []
    for item_constant_name, attributes in items_json.items():
        item_classification = None
        if attributes["classification"] == "PROGRESSION":
            item_classification = ItemClassification.progression
        elif attributes["classification"] == "USEFUL":
            item_classification = ItemClassification.useful
        elif attributes["classification"] == "FILLER":
            item_classification = ItemClassification.filler
        elif attributes["classification"] == "TRAP":
            item_classification = ItemClassification.trap
        else:
            item_classification = ItemClassification.filler
            # raise ValueError(f"Unknown classification {attributes['classification']} for item {item_constant_name}")

        data.items[item_codes[item_constant_name]] = ItemData(
            attributes["name"],
            item_codes[item_constant_name],
            item_constant_name,
            item_classification,
            frozenset(attributes["tags"])
        )

        if "TM" in attributes["tags"] and item_constant_name != "TM_ROCK_SMASH":
            # Make a copy of the TM item without the move name for randomized TMs
            tm_num = attributes["name"][2:4]
            # Offset by 256 from normal TM item code
            data.items[item_codes[item_constant_name] + 256] = ItemData(
                "TM" + tm_num,
                item_codes[item_constant_name],
                "TM_" + tm_num,
                item_classification,
                frozenset(attributes["tags"])
            )
            data.tm_replace_map.append(item_codes[item_constant_name])

    data.ram_addresses = {}
    for address_name, address in ram_address_data.items():
        data.ram_addresses[address_name] = address

    data.rom_addresses = {}
    for address_name, address in rom_address_data.items():
        data.rom_addresses[address_name] = address

    data.event_flags = {}
    for event_name, event_number in event_flag_data.items():
        data.event_flags[event_name] = event_number

    data.pokemon = {}
    for pokemon_name, pokemon_data in data_json["pokemon"].items():
        evolutions = []
        for evo in pokemon_data["evolutions"]:
            if len(evo) == 4:
                evolutions.append(EvolutionData(evo[0], int(evo[1]), evo[2], evo[3], len(evo)))
            elif evo[0] == "EVOLVE_LEVEL":
                evolutions.append(EvolutionData(evo[0], int(evo[1]), None, evo[2], len(evo)))
            else:
                evolutions.append(EvolutionData(evo[0], None, evo[1], evo[2], len(evo)))
        data.pokemon[pokemon_name] = PokemonData(
            pokemon_data["id"],
            pokemon_data["base_stats"],
            pokemon_data["types"],
            evolutions,
            [LearnsetData(move[0], move[1]) for move in pokemon_data["learnset"]],
            pokemon_data["tm_hm"],
            pokemon_data["is_base"],
            pokemon_data["bst"]
        )

    data.moves = {}
    for move_name, move_attributes in move_data.items():
        data.moves[move_name] = MoveData(
            move_name,
            move_attributes["id"],
            move_attributes["type"],
            move_attributes["power"],
            move_attributes["accuracy"],
            move_attributes["pp"],
            move_attributes["is_hm"],
            move_attributes["name"],
        )

    grass_dict = {}
    for grass_name, grass_data in wild_data["grass"].items():
        encounter_list = []
        for pkmn in grass_data:
            grass_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            encounter_list.append(grass_encounter)
        grass_dict[grass_name] = encounter_list

    water_dict = {}
    for water_name, water_data in wild_data["water"].items():
        encounter_list = []
        for pkmn in water_data:
            water_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            encounter_list.append(water_encounter)
        water_dict[water_name] = encounter_list

    fish_dict = {}
    for fish_name, fish_data in wild_data["fish"].items():
        old_encounters = []
        good_encounters = []
        super_encounters = []
        for pkmn in fish_data["Old"]:
            new_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            old_encounters.append(new_encounter)
        for pkmn in fish_data["Good"]:
            new_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            good_encounters.append(new_encounter)
        for pkmn in fish_data["Super"]:
            new_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            super_encounters.append(new_encounter)

        fish_dict[fish_name] = FishData(
            old_encounters,
            good_encounters,
            super_encounters
        )

    tree_dict = {}
    for tree_name, tree_data in wild_data["tree"].items():
        common_list = []
        rare_list = []
        for pkmn in tree_data["common"]:
            tree_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
            common_list.append(tree_encounter)
        if "rare" in tree_data:
            for pkmn in tree_data["rare"]:
                tree_encounter = EncounterMon(int(pkmn["level"]), pkmn["pokemon"])
                rare_list.append(tree_encounter)
        tree_dict[tree_name] = TreeMonData(common_list, rare_list)

    data.wild = WildData(grass_dict, water_dict, fish_dict, tree_dict)

    saffron_warps = {}
    for warp_name, warp_data in saffron_data["warps"].items():
        saffron_warps[warp_name] = MiscWarp(warp_data["coords"], warp_data["id"])

    radio_tower_data = ["Y", "Y", "N", "Y", "N"]

    mom_items = [MiscMomItem(item["index"], item["item"]) for item in mom_items_data]

    data.misc = MiscData(fuchsia_data, radio_tower_data, MiscSaffronWarps(saffron_warps, saffron_data["pairs"]),
                         radio_addr_data, mom_items)

    data.types = type_data["types"]
    data.type_ids = type_data["ids"]

    data.tmhm = {}
    for tm_name, tm_data in tmhm_data.items():
        data.tmhm[tm_name] = TMHMData(
            tm_name,
            tm_data["tm_num"],
            tm_data["type"],
            tm_data["is_hm"],
            move_data[tm_name]["id"]
        )

    music_consts = {}
    for music_name, music_data in data_json["music"]["consts"].items():
        music_consts[music_name] = MusicConst(music_data["id"], music_data["loop"])

    music_maps = {}
    for map_name in data_json["music"]["maps"]:
        music_maps[map_name] = ""

    data.music = MusicData(music_consts,
                           music_maps,
                           data_json["music"]["encounters"],
                           data_json["music"]["scripts"])

    data.trades = []
    for trade_data in data_json["trade"]:
        data.trades.append(
            TradeData(trade_data["index"],
                      trade_data["requested_pokemon"],
                      trade_data["received_pokemon"],
                      trade_data["requested_gender"],
                      trade_data["held_item"]))

    data.fly_regions = [
        FlyRegion(2, "Pallet Town", "REGION_PALLET_TOWN"),
        FlyRegion(3, "Viridian City", "REGION_VIRIDIAN_CITY"),
        FlyRegion(4, "Pewter City", "REGION_PEWTER_CITY"),
        FlyRegion(5, "Cerulean City", "REGION_CERULEAN_CITY"),
        FlyRegion(7, "Vermilion City", "REGION_VERMILION_CITY"),
        FlyRegion(8, "Lavender Town", "REGION_LAVENDER_TOWN"),
        FlyRegion(9, "Saffron City", "REGION_SAFFRON_CITY"),
        FlyRegion(10, "Celadon City", "REGION_CELADON_CITY"),
        FlyRegion(11, "Fuchsia City", "REGION_FUCHSIA_CITY"),
        FlyRegion(12, "Cinnabar Island", "REGION_CINNABAR_ISLAND"),

        FlyRegion(18, "Azalea Town", "REGION_AZALEA_TOWN"),
        FlyRegion(19, "Cianwood City", "REGION_CIANWOOD_CITY"),
        FlyRegion(20, "Goldenrod City", "REGION_GOLDENROD_CITY"),
        FlyRegion(21, "Olivine City", "REGION_OLIVINE_CITY"),
        FlyRegion(22, "Ecruteak City", "REGION_ECRUTEAK_CITY"),
        FlyRegion(23, "Mahogany Town", "REGION_MAHOGANY_TOWN"),
        FlyRegion(24, "Lake of Rage", "REGION_LAKE_OF_RAGE"),
        FlyRegion(25, "Blackthorn City", "REGION_BLACKTHORN_CITY"),
        FlyRegion(26, "Silver Cave", "REGION_SILVER_CAVE_OUTSIDE")
    ]

    data.game_settings = {
        "text_speed": PokemonCrystalGameSetting(0, 0, 2, {"instant": 0, "fast": 1, "mid": 2, "slow": 3}, 2),
        "battle_shift": PokemonCrystalGameSetting(0, 3, 1, {"shift": 1, "set": 0}, 1),
        "battle_animations": PokemonCrystalGameSetting(0, 4, 2, {"all": 0, "no_scene": 1, "no_bars": 2, "speedy": 3},
                                                       0),
        "sound": PokemonCrystalGameSetting(0, 6, 1, {"mono": 0, "stereo": 1}, 0),
        "menu_account": PokemonCrystalGameSetting(0, 7, 1, ON_OFF, 1),

        "text_frame": PokemonCrystalGameSetting(1, 0, 4, dict([(f"{x + 1}", x) for x in range(8)]), 0),
        "bike_music": PokemonCrystalGameSetting(1, 4, 1, INVERTED_ON_OFF, 1),
        "surf_music": PokemonCrystalGameSetting(1, 5, 1, INVERTED_ON_OFF, 1),
        "skip_nicknames": PokemonCrystalGameSetting(1, 6, 1, ON_OFF, 0),
        "auto_run": PokemonCrystalGameSetting(1, 7, 1, ON_OFF, 0),

        "spinners": PokemonCrystalGameSetting(2, 0, 1, {"normal": 0, "rotators": 1}, 0),
        "fast_egg_hatch": PokemonCrystalGameSetting(2, 1, 1, ON_OFF, 0),
        "fast_egg_make": PokemonCrystalGameSetting(2, 2, 1, ON_OFF, 0),
        "rods_always_work": PokemonCrystalGameSetting(2, 3, 1, ON_OFF, 0),
        "catch_exp": PokemonCrystalGameSetting(2, 4, 1, ON_OFF, 0),
        "poison_flicker": PokemonCrystalGameSetting(2, 5, 1, INVERTED_ON_OFF, 0),
        "low_hp_beep": PokemonCrystalGameSetting(2, 6, 1, INVERTED_ON_OFF, 0),
        "battle_move_stats": PokemonCrystalGameSetting(2, 7, 1, ON_OFF, 0),

        "time_of_day": PokemonCrystalGameSetting(3, 0, 2, {"auto": 0, "morn": 1, "day": 2, "nite": 3}, 0),
        "exp_distribution": PokemonCrystalGameSetting(3, 2, 2, {"gen2": 0, "gen6": 1, "gen8": 2, "no_exp": 3}, 0),
        "turbo_button": PokemonCrystalGameSetting(3, 4, 2, {"none": 0, "a": 1, "b": 2, "a_or_b": 3}, 0)
    }

    data.map_sizes = {}

    for map_name, map_size in map_size_data.items():
        data.map_sizes[map_name] = PokemonCrystalMapSizeData(map_size[0], map_size[1])

    data.phone_scripts = []
    phone_yaml = load_yaml_data("phone_data.yaml")
    for script_name, script_data in phone_yaml.items():
        try:
            data.phone_scripts.append(PhoneScriptData(script_name, script_data.get("caller"), script_data.get("script")))
        except Exception as ex:
            raise ValueError(f"Error processing phone script '{script_name}': {ex}") from ex

_init()
