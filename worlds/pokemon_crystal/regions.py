import logging
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from BaseClasses import Region, ItemClassification, Entrance
from .data import data
from .items import PokemonCrystalItem
from .locations import PokemonCrystalLocation
from .options import FreeFlyLocation, JohtoOnly, LevelScaling, BlackthornDarkCaveAccess, Goal
from .rules import can_map_card_fly

if TYPE_CHECKING:
    from . import PokemonCrystalWorld

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
    "RIVAL_FERALIGATR_INDIGO", "RIVAL_MEGANIUM_INDIGO", # Rival is in a Kanto region rn,
    "RIVAL_TYPHLOSION_INDIGO", "SAILOR_HUEY_POWER",     # so this is redundant, but eh.
    "SCHOOLBOY_ALAN_POWER", "SCHOOLBOY_CHAD_POWER",
    "SCHOOLBOY_JACK_POWER"
]

E4_LOCKED = list(set(CHAMPION_LOCKED + KANTO_LOCKED))
REMATCHES = list(set(MAP_LOCKED + ROCKETHQ_LOCKED + RADIO_LOCKED + E4_LOCKED + KANTO_LOCKED))



class RegionData:
    name: str
    exits: List[str]
    locations: List[str]
    distance: Optional[int]


def create_regions(world: "PokemonCrystalWorld") -> Dict[str, Region]:
    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []
    johto_only = world.options.johto_only.value

    def should_include_region(region):
        # check if region should be included per selected Johto Only option
        return (region.johto
                or johto_only == JohtoOnly.option_off
                or (region.silver_cave and johto_only == JohtoOnly.option_include_silver_cave))

    def exclude_scaling(trainer: str):
        if not world.options.rematchsanity and trainer in REMATCHES:
            return True
        elif johto_only != JohtoOnly.option_off and trainer in KANTO_LOCKED:
            return True
        elif world.options.goal.value == Goal.option_elite_four and trainer in E4_LOCKED:
            return True
        else:
            return False

    for region_name, region_data in data.regions.items():
        if should_include_region(region_data):
            new_region = Region(region_name, world.player, world.multiworld)

            regions[region_name] = new_region

            for event_data in region_data.events:
                event = PokemonCrystalLocation(world.player, event_data.name, new_region)
                event.show_in_spoiler = False
                event.place_locked_item(PokemonCrystalItem(
                    event_data.name, ItemClassification.progression, None, world.player))
                new_region.locations.append(event)

            # Level Scaling
            if world.options != LevelScaling.option_off:
                trainer_name_level_list: List[Tuple[str, int]] = []
                encounter_name_level_list: List[Tuple[str, int]] = []

                # Create plando locations for the trainers in their regions.
                for trainer in region_data.trainers:
                    if exclude_scaling(trainer.name):
                        logging.debug(
                            f"Excluding {trainer.name} from level scaling for {world.player_name}")
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
                        world.player, static.name, new_region, None, None, None, frozenset({"static scaling"}))
                    scaling_event.show_in_spoiler = False
                    scaling_event.place_locked_item(PokemonCrystalItem(
                        "Static Pokemon", ItemClassification.filler, None, world.player))
                    new_region.locations.append(scaling_event)

                # Create plando locations for the wilds in their regions.
                # TODO once wilds logic gets implemented.

                min_level = 100
                # Create a new list of all the Trainer Pokemon and their levels
                for trainer in region_data.trainers:
                    if exclude_scaling(trainer.name):
                        continue
                    for pokemon in trainer.pokemon:
                        min_level = min(min_level, pokemon.level)
                    # We grab the level and add it to our custom list.
                    trainer_name_level_list.append((trainer.name, min_level))
                    world.trainer_name_level_dict[trainer.name] = min_level

                min_level = 100
                # Now we do the same for statics.
                for static in region_data.statics:
                    min_level = min(min_level, static.level)
                    encounter_name_level_list.append((static.name, min_level))

                # And finally the wilds.
                # TODO add wilds scaling.

                # Make the lists for level_scaling.py to use
                trainer_name_level_list.sort(key=lambda i: i[1])
                world.trainer_name_list += [i[0] for i in trainer_name_level_list]
                world.trainer_level_list += [i[1] for i in trainer_name_level_list]
                encounter_name_level_list.sort(key=lambda i: i[1])
                world.encounter_name_list += [i[0] for i in encounter_name_level_list]
                world.encounter_level_list += [i[1] for i in encounter_name_level_list]
                # End level scaling in regions.py

            for region_exit in region_data.exits:
                connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

    for name, source, dest in connections:
        if should_include_region(data.regions[source]) and should_include_region(data.regions[dest]):
            regions[source].connect(regions[dest], name)

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions["REGION_PLAYERS_HOUSE_2F"], "Start Game")
    regions["Menu"].connect(regions["REGION_FLY"], "Fly")

    if world.options.johto_only.value == JohtoOnly.option_off and world.options.east_west_underground:
        regions["REGION_ROUTE_7"].connect(regions["REGION_ROUTE_8"])
        regions["REGION_ROUTE_8"].connect(regions["REGION_ROUTE_7"])

    if world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_waterfall:
        regions["REGION_DARK_CAVE_VIOLET_ENTRANCE"].connect(regions["REGION_DARK_CAVE_BLACKTHORN_ENTRANCE"])

    world.trainer_level_list.sort()
    world.encounter_level_list.sort()

    return regions


def setup_free_fly_regions(world: "PokemonCrystalWorld"):
    fly = world.get_region("REGION_FLY")
    if world.options.free_fly_location.value in [FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card]:
        free_fly_location = world.free_fly_location
        fly_region = world.get_region(free_fly_location.region_id)
        connection = Entrance(
            world.player,
            f"REGION_FLY -> {free_fly_location.region_id}",
            fly
        )
        fly.exits.append(connection)
        connection.connect(fly_region)

    if world.options.free_fly_location.value in [FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card]:
        map_card_fly_location = world.map_card_fly_location
        map_card_region = world.get_region(map_card_fly_location.region_id)
        connection = Entrance(
            world.player,
            f"REGION_FLY -> {map_card_fly_location.region_id}",
            fly
        )
        connection.access_rule = lambda state: can_map_card_fly(state, world)
        fly.exits.append(connection)
        connection.connect(map_card_region)
