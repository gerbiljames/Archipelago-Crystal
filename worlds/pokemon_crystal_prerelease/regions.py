import logging
from collections import defaultdict
from typing import TYPE_CHECKING

from BaseClasses import Region, ItemClassification
from entrance_rando import disconnect_entrance_for_randomization, EntranceType
from .data import data, RegionData, EncounterMon, StaticPokemon, LogicalAccess, EncounterKey, FishingRodType, \
    TreeRarity, EncounterType
from .items import PokemonCrystalItem
from .locations import PokemonCrystalLocation
from .options import FreeFlyLocation, JohtoOnly, BlackthornDarkCaveAccess, Goal, FlyCheese, Route42Access, LevelCurve
from .utils import get_fly_regions, should_include_region

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

# Rematches
MAP_LOCKED = [
    "BUG_CATCHER_ARNIE_BLACKTHORN", "BUG_CATCHER_ARNIE_LAKE",
    "BUG_CATCHER_WADE_GOLDENROD", "BUG_CATCHER_WADE_MAHOGANY",
    "CAMPER_TODD_BLACKTHORN", "CAMPER_TODD_CIANWOOD",
    "HIKER_ANTHONY_OLIVINE", "LASS_DANA_CIANWOOD",
    "PICNICKER_GINA_MAHOGANY", "SCHOOLBOY_ALAN_BLACKTHORN",
    "SCHOOLBOY_ALAN_OLIVINE", "SCHOOLBOY_CHAD_MAHOGANY",
    "SCHOOLBOY_JACK_OLIVINE", "YOUNGSTER_JOEY_GOLDENROD",
    "YOUNGSTER_JOEY_OLIVINE"
]

ROCKETHQ_LOCKED = [
    "FISHER_TULLY_ROCKETHQ", "POKEMANIAC_BRENT_ROCKETHQ"
]

RADIO_LOCKED = [
    "BUG_CATCHER_WADE_RADIO", "HIKER_ANTHONY_RADIO",
    "LASS_DANA_RADIO", "PICNICKER_GINA_RADIO",
    "PICNICKER_TIFFANY_RADIO", "SAILOR_HUEY_RADIO",
    "SCHOOLBOY_CHAD_RADIO", "SCHOOLBOY_JACK_RADIO",
    "YOUNGSTER_JOEY_RADIO"
]

CHAMPION_LOCKED = [
    "BIRD_KEEPER_JOSE_CHAMPION", "BIRD_KEEPER_VANCE_CHAMPION",
    "BUG_CATCHER_ARNIE_CHAMPION", "BUG_CATCHER_WADE_CHAMPION",
    "CAMPER_TODD_CHAMPION", "COOLTRAINERF_BETH_CHAMPION",
    "COOLTRAINERF_REENA_CHAMPION", "COOLTRAINERM_GAVEN_CHAMPION",
    "FISHER_TULLY_CHAMPION", "FISHER_WILTON_CHAMPION",
    "HIKER_ANTHONY_CHAMPION", "HIKER_PARRY_CHAMPION",
    "LASS_DANA_CHAMPION", "PICNICKER_ERIN_CHAMPION",
    "PICNICKER_GINA_CHAMPION", "PICNICKER_TIFFANY_CHAMPION",
    "POKEMANIAC_BRENT_CHAMPION", "SAILOR_HUEY_CHAMPION",
    "SCHOOLBOY_ALAN_CHAMPION", "SCHOOLBOY_CHAD_CHAMPION",
    "SCHOOLBOY_JACK_CHAMPION", "YOUNGSTER_JOEY_CHAMPION",
    "PICNICKER_LIZ_CHAMPION"
]

KANTO_LOCKED = [
    "BIRD_KEEPER_JOSE_POWER", "BIRD_KEEPER_VANCE_POWER",
    "BUG_CATCHER_ARNIE_POWER", "CAMPER_TODD_POWER",
    "COOLTRAINERF_BETH_POWER", "COOLTRAINERF_REENA_POWER",
    "COOLTRAINERM_GAVEN_POWER", "FISHER_TULLY_POWER",
    "FISHER_WILTON_POWER", "HIKER_ANTHONY_POWER",
    "HIKER_PARRY_POWER", "LASS_DANA_POWER",
    "PICNICKER_ERIN_POWER", "PICNICKER_GINA_POWER",
    "PICNICKER_TIFFANY_POWER", "POKEMANIAC_BRENT_POWER",
    "SAILOR_HUEY_POWER", "SCHOOLBOY_ALAN_POWER",
    "SCHOOLBOY_CHAD_POWER", "SCHOOLBOY_JACK_POWER"
]

LOGIC_EXCLUDE_STATICS = [
    "Raikou", "Entei", "CatchTutorial1", "CatchTutorial2", "CatchTutorial3"
]

E4_LOCKED = list(set(CHAMPION_LOCKED + KANTO_LOCKED))
REMATCHES = list(set(MAP_LOCKED + ROCKETHQ_LOCKED + RADIO_LOCKED + E4_LOCKED + KANTO_LOCKED))


def _build_type_to_group(er_types: set[str]) -> dict[str, int]:
    """Map each entrance type string to a stable integer group ID."""
    return {t: i for i, t in enumerate(sorted(er_types))}


def _er_group(conn, grouping: int, type_to_group: dict[str, int]) -> int:
    """Return the randomization_group integer for a given connection."""
    from .options import EntranceRandomizationGrouping
    if grouping == EntranceRandomizationGrouping.option_by_area:
        return 0 if conn.area == "johto" else 1
    if grouping == EntranceRandomizationGrouping.option_by_type:
        return type_to_group.get(conn.entrance_type, 0)
    return 0


def _build_er_group_lookup(er_types: set[str], grouping: int) -> tuple[dict[int, list[int]], bool]:
    """Build the target_group_lookup dict and preserve_group_order flag for randomize_entrances."""
    from .options import EntranceRandomizationGrouping
    if grouping == EntranceRandomizationGrouping.option_any:
        return {0: [0]}, False
    if grouping == EntranceRandomizationGrouping.option_by_type:
        type_to_group = _build_type_to_group(er_types)
        all_groups = sorted(type_to_group.values())
        # Soft preference: same-type targets are tried first via preserve_group_order,
        # but cross-type is allowed as a fallback to prevent generation failures caused
        # by dead-end/non-dead-end ratio imbalance across types.
        return {g: [g] + [x for x in all_groups if x != g] for g in all_groups}, True
    if grouping == EntranceRandomizationGrouping.option_by_area:
        return {0: [0], 1: [1]}, False
    return {0: [0]}, False


def _generate_curve_levels(n: int, min_level: int, max_level: int, shape: int) -> list[int]:
    if n == 0:
        return []
    if n == 1:
        return [min_level]
    lo, hi = min(min_level, max_level), max(min_level, max_level)
    span = hi - lo
    levels = []
    for i in range(n):
        t = i / (n - 1)
        if shape == LevelCurve.option_sqrt:
            t = t ** 0.5
        elif shape == LevelCurve.option_quadratic:
            t = t ** 2
        elif shape == LevelCurve.option_s_curve:
            t = t * t * (3 - 2 * t)  # smoothstep
        levels.append(round(lo + span * t))
    return levels


def create_regions(world: "PokemonCrystalWorld") -> dict[str, Region]:
    regions: dict[str, Region] = {}
    connections: list[tuple[str, str, str]] = []
    johto_only = world.options.johto_only.value
    rematches = world.options.rematchsanity or world.options.randomize_phone_call_items

    wild_name_level_list: list[tuple[str, list[int]]] = []
    trainer_name_level_list: list[tuple[str, int]] = []
    static_name_level_list: list[tuple[str, int]] = []

    wild_scaling_locations = set()

    grass_keys_by_region = defaultdict(list)
    for k in world.generated_wild:
        if k.encounter_type is EncounterType.Grass:
            grass_keys_by_region[k.region_id].append(k)

    def exclude_scaling(trainer: str):
        if not rematches and (trainer in REMATCHES):
            return True
        elif johto_only != JohtoOnly.option_off and trainer in KANTO_LOCKED:
            return True
        elif world.options.goal.value == {Goal.ELITE_FOUR} and trainer in E4_LOCKED:
            return True
        else:
            return False

    def create_scaling_location(parent_region: Region, wild_key: EncounterKey):
        if wild_key.region_name() in wild_scaling_locations: return
        if world.options.level_scaling and wild_key.encounter_type in [EncounterType.Grass,
                                                                       EncounterType.Water]:
            wild_name_level_list.append((
                wild_key.region_name(),
                [slot.level for slot in world.generated_wild[wild_key]]
            ))

            scaling_event = PokemonCrystalLocation(
                world.player, wild_key.region_name(), parent_region, None, None, None,
                frozenset({"wilds scaling"}))
            scaling_event.show_in_spoiler = False
            scaling_event.place_locked_item(PokemonCrystalItem(
                "Wild Pokemon", ItemClassification.filler, None, world.player))
            scaling_event.encounter_key = wild_key
            parent_region.locations.append(scaling_event)
            wild_scaling_locations.add(scaling_event.name)

    def create_wild_region(parent_region: Region, wild_key: EncounterKey, wilds: list[EncounterMon | StaticPokemon],
                           tags: set[str] | None = None):
        region_name = wild_key.region_name()
        if region_name not in regions:
            wild_region = Region(region_name, world.player, world.multiworld)
            wild_region.key = wild_key
            regions[region_name] = wild_region

            # We place a slot for each encounter here, but we don't care about what they are yet
            for i in range(len(wilds)):
                location = PokemonCrystalLocation(
                    world.player,
                    f"{region_name}_{i + 1}",
                    wild_region,
                    tags=frozenset(tags | {"wild encounter"} if tags else {"wild encounter"})
                )
                location.show_in_spoiler = False
                wild_region.locations.append(location)
        else:
            wild_region = regions[region_name]
        parent_region.connect(wild_region)

    def setup_wild_regions(parent_region: Region, wild_region_data: RegionData):

        if wild_region_data.wild_encounters:
            if wild_region_data.wild_encounters.grass:
                grass_name = wild_region_data.wild_encounters.grass
                grass_keys = grass_keys_by_region[grass_name]
                for encounter_key in grass_keys:
                    create_scaling_location(parent_region, encounter_key)
                    if "Land" in world.options.wild_encounter_methods_required:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                    else:
                        if not world.options.enforce_wild_encounter_methods_logic:
                            world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                        if world.is_universal_tracker:
                            create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.surfing:
                encounter_key = EncounterKey.water(wild_region_data.wild_encounters.surfing)
                create_scaling_location(parent_region, encounter_key)
                if "Surfing" in world.options.wild_encounter_methods_required:
                    world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                    create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    if not world.options.enforce_wild_encounter_methods_logic:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                    if world.is_universal_tracker:
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.fishing:
                if "Fishing" in world.options.wild_encounter_methods_required:
                    for fishing_rod in (FishingRodType.Old, FishingRodType.Good, FishingRodType.Super):
                        encounter_key = EncounterKey.fish(wild_region_data.wild_encounters.fishing, fishing_rod)
                        world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    for fishing_rod in (FishingRodType.Old, FishingRodType.Good, FishingRodType.Super):
                        encounter_key = EncounterKey.fish(wild_region_data.wild_encounters.fishing, fishing_rod)
                        if not world.options.enforce_wild_encounter_methods_logic:
                            world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                        if world.is_universal_tracker:
                            create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.headbutt:
                if "Headbutt" in world.options.wild_encounter_methods_required:
                    for rarity in (TreeRarity.Common, TreeRarity.Rare):
                        encounter_key = EncounterKey.tree(wild_region_data.wild_encounters.headbutt, rarity)
                        world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    for rarity in (TreeRarity.Common, TreeRarity.Rare):
                        encounter_key = EncounterKey.tree(wild_region_data.wild_encounters.headbutt, rarity)
                        if not world.options.enforce_wild_encounter_methods_logic:
                            world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                        if world.is_universal_tracker:
                            create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.rock_smash:
                encounter_key = EncounterKey.rock_smash()
                if "Rock Smash" in world.options.wild_encounter_methods_required:
                    world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                    create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    if not world.options.enforce_wild_encounter_methods_logic:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                    if world.is_universal_tracker:
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

        for static_id in wild_region_data.statics:
            static_encounter = world.generated_static[static_id]
            encounter_key = EncounterKey.static(static_encounter.name)
            if (world.options.static_pokemon_required
                    and static_encounter.name not in LOGIC_EXCLUDE_STATICS):
                world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                create_wild_region(parent_region, encounter_key, [static_encounter])
            else:
                world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                if world.is_universal_tracker:
                    create_wild_region(parent_region, encounter_key, [static_encounter])

    def setup_mart_regions(parent_region: Region, region_data: RegionData):
        for mart in region_data.marts:
            mart_data = data.marts[mart]
            if mart_data.category in world.options.shopsanity.value:
                region_name = f"REGION_{mart}"
                new_region = Region(region_name, world.player, world.multiworld)
                regions[region_name] = new_region
                parent_region.connect(new_region)

    for region_name, region_data in data.regions.items():
        if should_include_region(region_data, world):
            new_region = Region(region_name, world.player, world.multiworld)

            regions[region_name] = new_region

            for event_data in region_data.events:
                event_location = PokemonCrystalLocation(world.player, event_data.name, new_region)
                event_location.show_in_spoiler = False
                event_location.place_locked_item(world.create_event(event_data.name))
                new_region.locations.append(event_location)

            setup_wild_regions(new_region, region_data)
            if world.options.shopsanity:
                setup_mart_regions(new_region, region_data)

            # Level Scaling
            if world.options.level_scaling and not world.is_universal_tracker:
                # Create plando locations for the trainers in their regions.
                for trainer in region_data.trainers:
                    if exclude_scaling(trainer.name):
                        logging.debug(
                            f"Excluding %s from level scaling for %s", trainer.name, world.player_name)
                        continue
                    scaling_event = PokemonCrystalLocation(
                        world.player, trainer.name, new_region, None, None, None, frozenset({"trainer scaling"}))
                    scaling_event.show_in_spoiler = False
                    scaling_event.place_locked_item(PokemonCrystalItem(
                        "Trainer Party", ItemClassification.filler, None, world.player))
                    new_region.locations.append(scaling_event)

                # Create plando locations for the statics in their regions.
                for static in region_data.statics:
                    scaling_event = PokemonCrystalLocation(
                        world.player, world.generated_static[static].name, new_region, None, None, None,
                        frozenset({"static scaling"}))
                    scaling_event.show_in_spoiler = False
                    scaling_event.place_locked_item(PokemonCrystalItem(
                        "Static Pokemon", ItemClassification.filler, None, world.player))
                    new_region.locations.append(scaling_event)

                # Create a new list of all the Trainer Pokemon and their levels
                for trainer in region_data.trainers:
                    if exclude_scaling(trainer.name):
                        continue
                    min_level = 100
                    for pokemon in trainer.pokemon:
                        min_level = min(min_level, pokemon.level)
                    # We grab the level and add it to our custom list.
                    trainer_name_level_list.append((trainer.name, min_level))
                    world.trainer_name_level_dict[trainer.name] = min_level

                # Now we do the same for statics.
                for static_id in region_data.statics:
                    static = world.generated_static[static_id]
                    static_name_level_list.append((static.name, static.level))

            if world.options.grasssanity and region_name in data.grass_tiles:
                grass_region = Region(f"{region_name}:GRASS", world.player, world.multiworld)
                regions[grass_region.name] = grass_region
                new_region.connect(grass_region)

            for region_exit in region_data.exits:
                connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

    er_types = world.options.entrance_randomization.value  # frozenset of type strings
    grouping = world.options.entrance_randomization_grouping.value
    er_one_way = world.options.entrance_randomization_one_way.value
    type_to_group = _build_type_to_group(er_types)

    # Pin certain pokecenter entrances to vanilla so the player always has pokecenter access.
    vanilla_pokecenter: set[str] = set()
    if er_types:
        # Build lookup: town region → pokecenter entrance connection names
        pokecenter_by_town: dict[str, set[str]] = {}
        for conn_name, conn_data in data.entrance_connections.items():
            if conn_data.entrance_type == "pokecenter":
                # The pokecenter interior has _1F suffix; the other side is the town region.
                if "POKECENTER_1F" not in conn_data.exit_region:
                    town_region = conn_data.exit_region
                elif "POKECENTER_1F" not in conn_data.entrance_region:
                    town_region = conn_data.entrance_region
                else:
                    continue
                pokecenter_by_town.setdefault(town_region, set()).add(conn_name)

        if world.options.randomize_starting_town:
            starting_town = world.starting_town
        else:
            starting_town = next(t for t in data.starting_towns if t.region_id == "REGION_NEW_BARK_TOWN")

        if starting_town.pokecenter_region:
            vanilla_pokecenter = pokecenter_by_town.get(starting_town.pokecenter_region, set())

    for name, source, dest in connections:
        if should_include_region(data.regions[source], world) and should_include_region(data.regions[dest], world):
            entrance = regions[source].connect(regions[dest], name)
            # Disconnect for ER if this connection is in the randomizable pool
            conn = data.entrance_connections.get(name)
            if conn and conn.entrance_type in er_types and name not in vanilla_pokecenter and (not conn.one_way or er_one_way):
                if conn.one_way:
                    entrance.randomization_type = EntranceType.ONE_WAY
                else:
                    entrance.randomization_type = EntranceType.TWO_WAY
                entrance.randomization_group = _er_group(conn, grouping, type_to_group)
                world.er_entrances.append((entrance, regions[dest]))
                disconnect_entrance_for_randomization(
                    entrance,
                    one_way_target_name=f"{name} (one-way target)" if conn.one_way else None,
                )

    if world.options.skip_elite_four:
        regions["REGION_INDIGO_PLATEAU_POKECENTER_1F"].connect(regions["REGION_LANCES_ROOM"])

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    if world.options.randomize_starting_town:
        regions["Menu"].connect(regions[world.starting_town.region_id])
    elif world.options.entrance_randomization:
        regions["Menu"].connect(regions["REGION_NEW_BARK_TOWN"], "Start Game")
    else:
        regions["Menu"].connect(regions["REGION_PLAYERS_HOUSE_2F"], "Start Game")

    regions["Menu"].connect(regions["REGION_FLY"], "Fly")

    if world.options.randomize_fly_unlocks or world.options.remote_items:
        fly_region = regions["REGION_FLY"]
        for region in get_fly_regions(world):
            fly_region.connect(regions[region.exit_region])

    if world.options.fly_cheese == FlyCheese.option_in_logic:
        regions["REGION_ROUTE_44"].connect(regions["REGION_MAHOGANY_TOWN:FLY"])

        if not world.options.johto_only:
            regions["REGION_DIGLETTS_CAVE:SOUTH_ENTRANCE"].connect(regions["REGION_VERMILION_CITY:FLY"])
            regions["REGION_ROUTE_11"].connect(regions["REGION_VERMILION_CITY:FLY"])


    if world.options.blackthorn_dark_cave_access == BlackthornDarkCaveAccess.option_waterfall:
        regions["REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHWEST"].connect(
            regions["REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHWEST"])

    if world.options.route_42_access != Route42Access.option_blocked:
        regions["REGION_ROUTE_42:WEST"].connect(regions["REGION_ROUTE_42:CENTER"])
        regions["REGION_ROUTE_42:CENTER"].connect(regions["REGION_ROUTE_42:WEST"])
        regions["REGION_ROUTE_42:EAST"].connect(regions["REGION_ROUTE_42:CENTER"])
        regions["REGION_ROUTE_42:CENTER"].connect(regions["REGION_ROUTE_42:EAST"])

    if world.options.route_42_access in \
            (Route42Access.option_blocked, Route42Access.option_whirlpool_open_mortar):
        regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTH"].connect(
            regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:WATERFALL_ISLAND"])
        regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:WATERFALL_ISLAND"].connect(
            regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTH"])
        regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:WATERFALL_ISLAND"].connect(
            regions["REGION_MOUNT_MORTAR_1F_INSIDE:SOUTH"])
        regions["REGION_MOUNT_MORTAR_1F_INSIDE:SOUTH"].connect(
            regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:WATERFALL_ISLAND"])
    else:
        del regions["REGION_MOUNT_MORTAR_1F_OUTSIDE:WATERFALL_ISLAND"]

    if world.options.dexsanity or world.options.dexcountsanity:
        pokedex_region = Region("Pokedex", world.player, world.multiworld)
        regions["Pokedex"] = pokedex_region
        regions["Menu"].connect(regions["Pokedex"])
    if world.options.evolution_methods_required or world.is_universal_tracker:
        evolution_region = Region("Evolutions", world.player, world.multiworld)
        regions["Evolutions"] = evolution_region
        regions["Menu"].connect(regions["Evolutions"])
    if world.options.breeding_methods_required or world.is_universal_tracker:
        breeding_region = Region("Breeding", world.player, world.multiworld)
        regions["Breeding"] = breeding_region
        regions["Menu"].connect(regions["Breeding"])

    if world.options.level_scaling and not world.is_universal_tracker:
        trainer_name_level_list.sort(key=lambda i: i[1])
        world.trainer_name_list = [i[0] for i in trainer_name_level_list]
        static_name_level_list.sort(key=lambda i: i[1])
        world.static_name_list = [i[0] for i in static_name_level_list]
        wild_name_level_list.sort(key=lambda i: max(i[1]))
        world.encounter_region_name_list = [i[0] for i in wild_name_level_list]
        flat_wild_levels = [j for i in wild_name_level_list for j in i[1]]
        flat_wild_levels.sort()

        if world.options.level_curve != LevelCurve.option_vanilla:
            min_level = world.options.level_curve_min_level.value
            max_level = world.options.level_curve_max_level.value
            shape = world.options.level_curve.value
            wild_static_max = max(min_level, round(max_level * 2 / 3))
            world.trainer_level_list = _generate_curve_levels(len(trainer_name_level_list), min_level, max_level, shape)
            world.static_level_list = _generate_curve_levels(len(static_name_level_list), min_level, wild_static_max, shape)
            world.encounter_region_levels_list = _generate_curve_levels(len(flat_wild_levels), min_level, wild_static_max, shape)
        else:
            world.trainer_level_list = [i[1] for i in trainer_name_level_list]
            world.static_level_list = [i[1] for i in static_name_level_list]
            world.encounter_region_levels_list = flat_wild_levels
    return regions


def setup_free_fly_regions(world: "PokemonCrystalWorld"):
    fly = world.get_region("REGION_FLY")
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        free_fly_location = world.free_fly_location
        fly_region = world.get_region(free_fly_location.exit_region)
        fly.connect(fly_region, f"Free Fly {free_fly_location.exit_region}")

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        map_card_fly_location = world.map_card_fly_location
        map_card_region = world.get_region(map_card_fly_location.exit_region)
        fly.connect(map_card_region, f"Free Fly {map_card_fly_location.exit_region}")
