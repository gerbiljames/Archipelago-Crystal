import pkgutil
from dataclasses import dataclass, field, replace
from enum import Enum, StrEnum
from typing import Any

import orjson
import yaml

from BaseClasses import ItemClassification

APWORLD_VERSION = "4.0.0-beta.7"
POKEDEX_OFFSET = 10000
POKEDEX_COUNT_OFFSET = 20000


@dataclass(frozen=True)
class ItemData:
    label: str
    item_id: int
    item_const: str
    classification: ItemClassification
    tags: frozenset[str]


@dataclass(frozen=True)
class LocationData:
    name: str
    label: str
    parent_region: str
    default_item: int
    rom_address: int
    flag: int
    tags: frozenset[str]
    script: str


@dataclass(frozen=True)
class EventData:
    name: str
    parent_region: str


@dataclass(frozen=True)
class TrainerPokemon:
    level: int
    pokemon: str
    item: str | None
    moves: list[str]


@dataclass(frozen=True)
class TrainerData:
    name: str
    trainer_type: str
    pokemon: list[TrainerPokemon]
    name_length: int


@dataclass(frozen=True)
class LearnsetData:
    level: int
    move: str


class EvolutionType(Enum):
    Level = 0
    Item = 1
    Happiness = 2
    Stats = 3
    Trade = 4

    @staticmethod
    def from_string(evo_type_string):
        if evo_type_string == "EVOLVE_LEVEL": return EvolutionType.Level
        if evo_type_string == "EVOLVE_ITEM": return EvolutionType.Item
        if evo_type_string == "EVOLVE_HAPPINESS": return EvolutionType.Happiness
        if evo_type_string == "EVOLVE_STAT": return EvolutionType.Stats
        if evo_type_string == "EVOLVE_TRADE": return EvolutionType.Trade
        raise ValueError(f"Invalid evolution type: {evo_type_string}")


@dataclass(frozen=True)
class EvolutionData:
    evo_type: EvolutionType
    level: int | None
    condition: str | None
    pokemon: str
    length: int


@dataclass(frozen=True)
class PokemonData:
    id: int
    friendly_name: str
    base_stats: list[int]
    types: list[str]
    evolutions: list[EvolutionData]
    learnset: list[LearnsetData]
    tm_hm: list[str]
    is_base: bool
    bst: int
    egg_groups: list[str]
    gender_ratio: str


@dataclass(frozen=True)
class MoveData:
    id: str
    rom_id: int
    type: str
    power: int
    accuracy: int
    pp: int
    is_hm: bool
    name: str


@dataclass(frozen=True)
class TMHMData:
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
    IcePath = 11

    @staticmethod
    def all():
        return list(map(lambda c: c.value, MiscOption))


@dataclass(frozen=True)
class MiscWarp:
    coords: tuple[int, int]
    id: int


@dataclass(frozen=True)
class MiscSaffronWarps:
    warps: dict[str, MiscWarp]
    pairs: list[tuple[str, str]]


@dataclass(frozen=True)
class MiscMomItem:
    index: int
    item: str


@dataclass(frozen=True)
class MiscData:
    fuchsia_gym_trainers: list[list[int]]
    radio_tower_questions: list[str]
    saffron_gym_warps: MiscSaffronWarps
    radio_channel_addresses: list[int]
    mom_items: list[MiscMomItem]
    selected: list[MiscOption] = field(default_factory=lambda: MiscOption.all())


@dataclass(frozen=True)
class MusicConst:
    id: int
    loop: bool


@dataclass(frozen=True)
class MusicData:
    consts: dict[str, MusicConst]
    maps: dict[str, str]
    encounters: list[str]
    scripts: dict[str, str]

    def __copy__(self):
        return replace(
            self,
            consts=self.consts.copy(),
            maps=self.maps.copy(),
            encounters=self.encounters.copy(),
            scripts=self.scripts.copy()
        )


@dataclass(frozen=True)
class EncounterMon:
    level: int
    pokemon: str


class EncounterType(StrEnum):
    Grass = "WildGrass"
    Water = "WildWater"
    Fish = "WildFish"
    Tree = "WildTree"
    RockSmash = "WildRockSmash"
    Static = "Static"


class GrassTimeOfDay(Enum):
    Morn = 0
    Day = 1
    Nite = 2


class FishingRodType(StrEnum):
    Old = "Old"
    Good = "Good"
    Super = "Super"


class TreeRarity(StrEnum):
    Common = "Common"
    Rare = "Rare"


@dataclass(frozen=True)
class EncounterKey:
    encounter_type: EncounterType
    region_id: str | None = None
    time_of_day: GrassTimeOfDay | None = None
    fishing_rod: FishingRodType | None = None
    rarity: TreeRarity | None = None

    def region_name(self):
        if (self.encounter_type is EncounterType.Grass
                or self.encounter_type is EncounterType.Water
                or self.encounter_type is EncounterType.Static):
            return f"{str(self.encounter_type)}_{self.region_id}"
        elif self.encounter_type is EncounterType.Fish:
            return f"{str(self.encounter_type)}_{self.region_id}_{str(self.fishing_rod)}"
        elif self.encounter_type is EncounterType.Tree:
            return f"{str(self.encounter_type)}_{self.region_id}_{str(self.rarity)}"
        elif self.encounter_type is EncounterType.RockSmash:
            return f"{str(self.encounter_type)}"
        else:
            raise ValueError(f"Invalid encounter type: {self.encounter_type}")

    @staticmethod
    def grass(region_id: str, time_of_day: GrassTimeOfDay = GrassTimeOfDay.Day):
        return EncounterKey(EncounterType.Grass, region_id, time_of_day=time_of_day)

    @staticmethod
    def water(region_id: str):
        return EncounterKey(EncounterType.Water, region_id)

    @staticmethod
    def fish(region_id: str, fishing_rod: FishingRodType):
        return EncounterKey(EncounterType.Fish, region_id, fishing_rod=fishing_rod)

    @staticmethod
    def tree(region_id: str, rarity: TreeRarity):
        return EncounterKey(EncounterType.Tree, region_id, rarity=rarity)

    @staticmethod
    def rock_smash():
        return EncounterKey(EncounterType.RockSmash)

    @staticmethod
    def static(name: str):
        return EncounterKey(EncounterType.Static, name)


class LogicalAccess(Enum):
    InLogic = 0
    OutOfLogic = 1
    Inaccessible = 2


@dataclass(frozen=True)
class StaticPokemon:
    name: str
    pokemon: str
    addresses: list[str]
    level: int
    level_type: str
    level_address: str | None


@dataclass(frozen=True)
class TradeData:
    index: int
    requested_pokemon: str
    received_pokemon: str
    requested_gender: int
    held_item: str


@dataclass(frozen=True)
class RegionWildEncounterData:
    grass: str | None
    surfing: str | None
    fishing: str | None
    headbutt: str | None
    rock_smash: bool


@dataclass(frozen=True)
class RegionData:
    name: str
    johto: bool
    silver_cave: bool
    exits: list[str]
    trainers: list[TrainerData]
    statics: list[EncounterKey]
    locations: list[str]
    events: list[EventData]
    wild_encounters: RegionWildEncounterData | None


@dataclass(frozen=True)
class StartingTown:
    id: int
    name: str
    region_id: str
    johto: bool
    restrictive_start: bool = False


@dataclass(frozen=True)
class FlyRegion:
    id: int
    name: str
    region_id: str
    johto: bool
    exclude_vanilla_start: bool = False


@dataclass(frozen=True)
class PhoneScriptData:
    name: str
    caller: str
    script: list[str]


@dataclass(frozen=True)
class PokemonCrystalGameSetting:
    option_byte_index: int
    offset: int
    length: int
    values: dict[str, int]
    default: int

    def set_option_byte(self, option_selection: str | None, option_bytes: bytearray):
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


@dataclass(frozen=True)
class PokemonCrystalMapSizeData:
    width: int
    height: int


@dataclass(frozen=True)
class PokemonCrystalData:
    rom_version: int
    rom_version_11: int
    rom_addresses: dict[str, int]
    ram_addresses: dict[str, int]
    event_flags: dict[str, int]
    regions: dict[str, RegionData]
    locations: dict[str, LocationData]
    items: dict[int, ItemData]
    trainers: dict[str, TrainerData]
    pokemon: dict[str, PokemonData]
    moves: dict[str, MoveData]
    wild: dict[EncounterKey, list[EncounterMon]]
    types: list[str]
    type_ids: dict[str, int]
    tmhm: dict[str, TMHMData]
    misc: MiscData
    music: MusicData
    static: dict[EncounterKey, StaticPokemon]
    trades: list[TradeData]
    fly_regions: list[FlyRegion]
    starting_towns: list[StartingTown]
    game_settings: dict[str, PokemonCrystalGameSetting]
    phone_scripts: list[PhoneScriptData]
    map_sizes: dict[str, tuple[int, int]]


def load_json_data(data_name: str) -> list[Any] | dict[str, Any]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))


def load_yaml_data(data_name: str) -> list[Any] | dict[str, Any]:
    return yaml.safe_load(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))


def _parse_encounters(encounter_list: list) -> list[EncounterMon]:
    return [EncounterMon(int(pkmn["level"]), pkmn["pokemon"]) for pkmn in encounter_list]


data: PokemonCrystalData


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

    claimed_locations: set[str] = set()

    trainers = {}

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

        trainers[trainer_name] = TrainerData(
            trainer_name,
            trainer_type,
            pokemon,
            trainer_attributes["name_length"]
        )

    statics = dict[EncounterKey, StaticPokemon]()
    for static_name, static_data in data_json["static"].items():
        static_key = EncounterKey(EncounterType.Static, static_name)
        level_type = static_data["type"]
        if level_type == "loadwildmon" or level_type == "givepoke":
            level_address = static_data["addresses"][0]
        elif level_type == "custom":
            level_address = static_data["level_address"]
        else:
            level_address = None
        statics[static_key] = StaticPokemon(
            static_name,
            static_data["pokemon"],
            static_data["addresses"],
            static_data["level"],
            static_data["type"],
            level_address
        )

    regions = {}
    locations = {}

    for region_name, region_json in regions_json.items():

        region_locations = []

        for location_name in region_json["locations"]:
            if location_name in claimed_locations:
                raise AssertionError(f"Location [{location_name}] was claimed by multiple regions")
            location_json: dict[str, Any] = location_data[location_name]
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
            region_locations.append(location_name)
            locations[location_name] = new_location
            claimed_locations.add(location_name)

        region_locations.sort()

        new_region = RegionData(
            name=region_name,
            johto=region_json["johto"],
            silver_cave=region_json["silver_cave"] if "silver_cave" in region_json else False,
            exits=[region_exit for region_exit in region_json["exits"]],
            statics=[EncounterKey(EncounterType.Static, static) for static in region_json.get("statics", [])],
            trainers=[trainers[trainer] for trainer in region_json.get("trainers", [])],
            events=[EventData(event, region_name) for event in region_json["events"]],
            locations=region_locations,
            wild_encounters=RegionWildEncounterData(
                region_json["wild_encounters"].get("grass"),
                region_json["wild_encounters"].get("surfing"),
                region_json["wild_encounters"].get("fishing"),
                region_json["wild_encounters"].get("headbutt"),
                region_json["wild_encounters"].get("rock_smash")
            ) if "wild_encounters" in region_json else None
        )

        regions[region_name] = new_region

    # items

    items = {}
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

        items[item_codes[item_constant_name]] = ItemData(
            attributes["name"],
            item_codes[item_constant_name],
            item_constant_name,
            item_classification,
            frozenset(attributes["tags"])
        )

    pokemon = {}
    for pokemon_name, pokemon_data in data_json["pokemon"].items():
        evolutions = []
        for evo in pokemon_data["evolutions"]:
            evo_type = EvolutionType.from_string(evo[0])
            if len(evo) == 4:
                evolutions.append(EvolutionData(evo_type, int(evo[1]), evo[2], evo[3], len(evo)))
            elif evo_type is EvolutionType.Level:
                evolutions.append(EvolutionData(evo_type, int(evo[1]), None, evo[2], len(evo)))
            else:
                evolutions.append(EvolutionData(evo_type, None, evo[1], evo[2], len(evo)))
        pokemon[pokemon_name] = PokemonData(
            pokemon_data["id"],
            pokemon_data["friendly_name"],
            pokemon_data["base_stats"],
            pokemon_data["types"],
            evolutions,
            [LearnsetData(move[0], move[1]) for move in pokemon_data["learnset"]],
            pokemon_data["tm_hm"],
            pokemon_data["is_base"],
            pokemon_data["bst"],
            pokemon_data["egg_groups"],
            pokemon_data["gender_ratio"]
        )

    moves = {
        move_name: MoveData(
            move_name,
            move_attributes["id"],
            move_attributes["type"],
            move_attributes["power"],
            move_attributes["accuracy"],
            move_attributes["pp"],
            move_attributes["is_hm"],
            move_attributes["name"],
        ) for move_name, move_attributes in move_data.items()
    }

    wild = dict[EncounterKey, list[EncounterMon]]()

    for grass_name, grass_data in wild_data["grass"].items():
        wild[EncounterKey.grass(grass_name)] = _parse_encounters(
            grass_data["day"])

    for water_name, water_data in wild_data["water"].items():
        wild[EncounterKey.water(water_name)] = _parse_encounters(water_data)

    for fish_name, fish_data in wild_data["fish"].items():
        wild[EncounterKey.fish(fish_name, FishingRodType.Old)] = _parse_encounters(fish_data["Old"])
        wild[EncounterKey.fish(fish_name, FishingRodType.Good)] = _parse_encounters(fish_data["Good"])
        wild[EncounterKey.fish(fish_name, FishingRodType.Super)] = _parse_encounters(fish_data["Super"])

    for tree_name, tree_data in wild_data["tree"].items():
        if "rare" in tree_data:
            wild[EncounterKey.tree(tree_name, TreeRarity.Common)] = _parse_encounters(tree_data["common"])
            wild[EncounterKey.tree(tree_name, TreeRarity.Rare)] = _parse_encounters(tree_data["rare"])
        else:
            wild[EncounterKey.rock_smash()] = _parse_encounters(tree_data["common"])

    saffron_warps = {warp_name: MiscWarp(warp_data["coords"], warp_data["id"]) for warp_name, warp_data in
                     saffron_data["warps"].items()}

    radio_tower_data = ["Y", "Y", "N", "Y", "N"]

    mom_items = [MiscMomItem(item["index"], item["item"]) for item in mom_items_data]

    misc = MiscData(fuchsia_data, radio_tower_data, MiscSaffronWarps(saffron_warps, saffron_data["pairs"]),
                    radio_addr_data, mom_items)

    types = type_data["types"]
    type_ids = type_data["ids"]

    tmhm = {tm_name: TMHMData(
        tm_name,
        tm_data["tm_num"],
        tm_data["type"],
        tm_data["is_hm"],
        move_data[tm_name]["id"]
    ) for tm_name, tm_data in tmhm_data.items()}

    music_consts = {music_name: MusicConst(music_data["id"], music_data["loop"]) for music_name, music_data in
                    data_json["music"]["consts"].items()}

    music_maps = {map_name: "" for map_name in data_json["music"]["maps"]}

    music = MusicData(music_consts,
                      music_maps,
                      data_json["music"]["encounters"],
                      data_json["music"]["scripts"])

    trades = [TradeData(
        trade_data["index"],
        trade_data["requested_pokemon"],
        trade_data["received_pokemon"],
        trade_data["requested_gender"],
        trade_data["held_item"]
    ) for trade_data in data_json["trade"]]

    starting_towns = [
        StartingTown(2, "Pallet Town", "REGION_PALLET_TOWN", False, restrictive_start=True),
        StartingTown(3, "Viridian City", "REGION_VIRIDIAN_CITY", False, restrictive_start=True),
        StartingTown(4, "Pewter City", "REGION_PEWTER_CITY", False, restrictive_start=True),
        StartingTown(5, "Cerulean City", "REGION_CERULEAN_CITY", False, restrictive_start=True),
        StartingTown(6, "Rock Tunnel", "REGION_ROUTE_9", False, restrictive_start=True),
        StartingTown(7, "Vermilion City", "REGION_VERMILION_CITY", False, restrictive_start=True),
        StartingTown(8, "Lavender Town", "REGION_LAVENDER_TOWN", False, restrictive_start=True),
        StartingTown(9, "Saffron City", "REGION_SAFFRON_CITY", False),
        StartingTown(10, "Celadon City", "REGION_CELADON_CITY", False, restrictive_start=True),
        StartingTown(11, "Fuchsia City", "REGION_FUCHSIA_CITY", False, restrictive_start=True),
        # StartingTown(12, "Cinnabar Island", "REGION_CINNABAR_ISLAND", False, restrictive_start=True),

        StartingTown(14, "New Bark Town", "REGION_NEW_BARK_TOWN", True),
        StartingTown(15, "Cherrygrove City", "REGION_CHERRYGROVE_CITY", True),
        StartingTown(16, "Violet City", "REGION_VIOLET_CITY", True),
        StartingTown(17, "Union Cave", "REGION_ROUTE_32:SOUTH", True),
        StartingTown(18, "Azalea Town", "REGION_AZALEA_TOWN", True),
        StartingTown(19, "Cianwood City", "REGION_CIANWOOD_CITY", True, restrictive_start=True),
        StartingTown(20, "Goldenrod City", "REGION_GOLDENROD_CITY", True),
        StartingTown(21, "Olivine City", "REGION_OLIVINE_CITY", True),
        StartingTown(22, "Ecruteak City", "REGION_ECRUTEAK_CITY", True),
        StartingTown(23, "Mahogany Town", "REGION_MAHOGANY_TOWN", True),
        StartingTown(24, "Lake of Rage", "REGION_LAKE_OF_RAGE", True),
        StartingTown(25, "Blackthorn City", "REGION_BLACKTHORN_CITY", True)
    ]

    fly_regions = [
        FlyRegion(2, "Pallet Town", "REGION_PALLET_TOWN", False),
        FlyRegion(3, "Viridian City", "REGION_VIRIDIAN_CITY", False),
        FlyRegion(4, "Pewter City", "REGION_PEWTER_CITY", False),
        FlyRegion(5, "Cerulean City", "REGION_CERULEAN_CITY", False),
        FlyRegion(7, "Vermilion City", "REGION_VERMILION_CITY", False),
        FlyRegion(8, "Lavender Town", "REGION_LAVENDER_TOWN", False),
        FlyRegion(9, "Saffron City", "REGION_SAFFRON_CITY", False),
        FlyRegion(10, "Celadon City", "REGION_CELADON_CITY", False),
        FlyRegion(11, "Fuchsia City", "REGION_FUCHSIA_CITY", False),
        FlyRegion(12, "Cinnabar Island", "REGION_CINNABAR_ISLAND", False),

        FlyRegion(14, "New Bark Town", "REGION_NEW_BARK_TOWN", True, exclude_vanilla_start=True),
        FlyRegion(15, "Cherrygrove City", "REGION_CHERRYGROVE_CITY", True, exclude_vanilla_start=True),
        FlyRegion(16, "Violet City", "REGION_VIOLET_CITY", True, exclude_vanilla_start=True),
        FlyRegion(18, "Azalea Town", "REGION_AZALEA_TOWN", True),
        FlyRegion(19, "Cianwood City", "REGION_CIANWOOD_CITY", True),
        FlyRegion(20, "Goldenrod City", "REGION_GOLDENROD_CITY", True),
        FlyRegion(21, "Olivine City", "REGION_OLIVINE_CITY", True),
        FlyRegion(22, "Ecruteak City", "REGION_ECRUTEAK_CITY", True),
        FlyRegion(23, "Mahogany Town", "REGION_MAHOGANY_TOWN", True),
        FlyRegion(24, "Lake of Rage", "REGION_LAKE_OF_RAGE", True),
        FlyRegion(25, "Blackthorn City", "REGION_BLACKTHORN_CITY", True),
        FlyRegion(26, "Silver Cave", "REGION_SILVER_CAVE_OUTSIDE", True)
    ]

    game_settings = {
        "text_speed": PokemonCrystalGameSetting(0, 0, 2, {"instant": 0, "fast": 1, "mid": 2, "slow": 3}, 2),
        "battle_shift": PokemonCrystalGameSetting(0, 3, 1, {"shift": 1, "set": 0}, 1),
        "battle_animations": PokemonCrystalGameSetting(0, 4, 2,
                                                       {"all": 0, "no_scene": 1, "no_bars": 2, "speedy": 3}, 0),
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
        "turbo_button": PokemonCrystalGameSetting(3, 4, 2, {"none": 0, "a": 1, "b": 2, "a_or_b": 3}, 0),
        "short_fanfares": PokemonCrystalGameSetting(3, 6, 1, ON_OFF, 0),
        "dex_area_beep": PokemonCrystalGameSetting(3, 7, 1, ON_OFF, 0),

        "skip_dex_registration": PokemonCrystalGameSetting(4, 0, 1, ON_OFF, 0),
        "blind_trainers": PokemonCrystalGameSetting(4, 1, 1, ON_OFF, 0),
        "guaranteed_catch": PokemonCrystalGameSetting(4, 2, 1, ON_OFF, 0),
        "ap_item_sound": PokemonCrystalGameSetting(4, 3, 1, ON_OFF, 1),
        "_death_link": PokemonCrystalGameSetting(4, 4, 1, ON_OFF, 0)
    }

    map_sizes = {map_name: (map_size[0], map_size[1]) for map_name, map_size in
                 map_size_data.items()}

    phone_scripts = []
    phone_yaml = load_yaml_data("phone_data.yaml")
    for script_name, script_data in phone_yaml.items():
        try:
            phone_scripts.append(
                PhoneScriptData(script_name, script_data.get("caller"), script_data.get("script")))
        except Exception as ex:
            raise ValueError(f"Error processing phone script '{script_name}': {ex}") from ex

    global data
    data = PokemonCrystalData(
        rom_version=data_json["rom_version"],
        rom_version_11=data_json["rom_version11"],
        ram_addresses=ram_address_data,
        rom_addresses=rom_address_data,
        event_flags=event_flag_data,
        regions=regions,
        locations=locations,
        items=items,
        trainers=trainers,
        pokemon=pokemon,
        moves=moves,
        wild=wild,
        types=types,
        type_ids=type_ids,
        tmhm=tmhm,
        misc=misc,
        music=music,
        static=statics,
        trades=trades,
        fly_regions=fly_regions,
        starting_towns=starting_towns,
        game_settings=game_settings,
        phone_scripts=phone_scripts,
        map_sizes=map_sizes
    )


_init()
