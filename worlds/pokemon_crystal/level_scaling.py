import logging
from typing import List, Set

from BaseClasses import CollectionState, MultiWorld
from .data import RegionData
from .locations import PokemonCrystalLocation
from .options import LevelScaling
from .regions import RegionData
from .utils import bound


def perform_level_scaling(multiworld: MultiWorld):
    # List of milestones for AP to use to create the level curve.
    # Commented out are for future-proofing, i.e. ER.
    battle_events = [
        # "EVENT_RIVAL_CHERRYGROVE_CITY",
        # "EVENT_BEAT_SAGE_LI", # Sprout Tower Boss
        "EVENT_ZEPHYR_BADGE_FROM_FALKNER",
        "EVENT_CLEARED_SLOWPOKE_WELL",
        # "EVENT_HIVE_BADGE_FROM_BUGSY",
        "EVENT_RIVAL_AZALEA_TOWN",
        "EVENT_PLAIN_BADGE_FROM_WHITNEY",
        # "EVENT_RIVAL_BURNED_TOWER",
        # "EVENT_BEAT_KIMONO_GIRL_MIKI", # final girl
        "EVENT_FOG_BADGE_FROM_MORTY",
        "EVENT_BEAT_POKEFANM_DEREK",  # Route 39
        "EVENT_STORM_BADGE_FROM_CHUCK",
        # "EVENT_FOUGHT_EUSINE", # in Cianwood, for legendary hunt maybe? could be fun.
        "EVENT_MINERAL_BADGE_FROM_JASMINE",
        "EVENT_CLEARED_ROCKET_HIDEOUT",
        "EVENT_GLACIER_BADGE_FROM_PRYCE",
        "EVENT_BEAT_ROCKET_EXECUTIVEM_3",  # False Director
        "EVENT_RIVAL_GOLDENROD_UNDERGROUND",
        # "EVENT_BEAT_ROCKET_GRUNTF_3", # Puzzle Room
        # "EVENT_BEAT_ROCKET_GRUNTM_24", # Warehouse
        "EVENT_CLEARED_RADIO_TOWER",
        "EVENT_RISING_BADGE_FROM_CLAIR",
        "EVENT_BEAT_COOLTRAINERM_DARIN",  # Dragon's Den Entrance
        "EVENT_RIVAL_VICTORY_ROAD",
        # "EVENT_BEAT_ELITE_4_WILL",
        # "EVENT_BEAT_ELITE_4_KOGA",
        # "EVENT_BEAT_ELITE_4_BRUNO",
        # "EVENT_BEAT_ELITE_4_KAREN",
        "EVENT_BEAT_ELITE_FOUR",
        "EVENT_FAST_SHIP_LAZY_SAILOR",  # boat quest
        "EVENT_THUNDER_BADGE_FROM_LTSURGE",
        "EVENT_MARSH_BADGE_FROM_SABRINA",
        "EVENT_RAINBOW_BADGE_FROM_ERIKA",
        # "EVENT_BEAT_BIRD_KEEPER_BOB", # Route 18
        "EVENT_SOUL_BADGE_FROM_JANINE",
        # "EVENT_BEAT_POKEFANM_JOSHUA", # Fred
        # "EVENT_BEAT_COOLTRAINERM_KEVIN", # Fabulous Prize
        "EVENT_CASCADE_BADGE_FROM_MISTY",
        "EVENT_BOULDER_BADGE_FROM_BROCK",
        "EVENT_VOLCANO_BADGE_FROM_BLAINE",
        "EVENT_EARTH_BADGE_FROM_BLUE",
        "EVENT_BEAT_RIVAL_IN_MT_MOON",
        # "EVENT_RIVAL_INDIGO_PLATEAU_POKECENTER", # this is the league rematch, wed and fri only; requires mt. moon rival
        "EVENT_KOJI_ALLOWS_YOU_PASSAGE_TO_TIN_TOWER",  # 3rd of Wise Trio.
        "EVENT_BEAT_RED"  # Either Red is the final boss, or he's not lol.  Either way, might as well have a roof.
    ]

    level_scaling_required = False
    state = CollectionState(multiworld)
    progression_locations = {loc for loc in multiworld.get_filled_locations() if loc.item.advancement}
    crystal_locations: Set[PokemonCrystalLocation] = {loc for loc in multiworld.get_filled_locations() if
                                                      loc.game == "Pokemon Crystal"}
    scaling_locations = {loc for loc in crystal_locations if
                         ("trainer scaling" in loc.tags) or ("static scaling" in loc.tags)}
    locations = progression_locations | scaling_locations
    collected_locations = set()
    spheres = []

    for world in multiworld.get_game_worlds("Pokemon Crystal"):
        if world.options.level_scaling != LevelScaling.option_off:
            level_scaling_required = True
        else:
            world.finished_level_scaling.set()

    if not level_scaling_required:
        return

    # AP runs through the seed and starts collecting locations and counting spheres
    # to find battle milestones as listed above. this is important for creating our level curve.
    while len(locations) > 0:
        new_spheres: List[Set] = []
        new_battle_events = set()
        battle_events_found = True

        while battle_events_found:
            battle_events_found = False
            events_found = True
            sphere = set()
            old_sphere = set()
            distances = {}

            while events_found:
                events_found = False

                for world in multiworld.get_game_worlds("Pokemon Crystal"):
                    if world.options.level_scaling != LevelScaling.option_spheres_and_distance:
                        continue
                    # Menu is region 0, so we start counting from here.
                    regions = {multiworld.get_region("Menu", world.player)}
                    checked_regions = set()
                    distance = 0
                    while regions:
                        update_regions = True
                        while update_regions:
                            update_regions = False
                            same_distance_regions = set()
                            for region in regions:
                                encounter_regions = {e.connected_region for e in region.exits if e.access_rule(state)}
                                same_distance_regions.update(encounter_regions)
                            regions_len = len(regions)
                            regions.update(same_distance_regions)
                            if len(regions) > regions_len:
                                update_regions = True
                        next_regions = set()
                        for region in regions:
                            if not hasattr(region, "distance") or distance < region.distance:
                                region.distance = distance
                            next_regions.update({e.connected_region for e in region.exits if
                                                 e.connected_region not in checked_regions and e.access_rule(state)})
                        checked_regions.update(regions)
                        regions = next_regions
                        distance += 1

                for location in locations:
                    def can_reach():
                        if location.can_reach(state):
                            return True
                        return False

                    if can_reach():
                        sphere.add(location)

                        if location.game == "Pokemon Crystal":
                            parent_region: RegionData = location.parent_region
                            if getattr(parent_region, "distance", None) is None:
                                distance = 0
                            else:
                                distance = parent_region.distance
                        else:
                            distance = 0

                        if distance not in distances:
                            distances[distance] = {location}
                        else:
                            distances[distance].add(location)

                locations -= sphere
                old_sphere ^= sphere

                for location in old_sphere:
                    if location.is_event and location.item and location not in collected_locations:
                        if location.name not in battle_events:
                            collected_locations.add(location)
                            state.collect(location.item, True, location)
                            events_found = True
                        else:
                            new_battle_events.add(location)
                            battle_events_found = True

                old_sphere |= sphere

            if sphere:
                for distance in sorted(distances.keys()):
                    new_spheres.append(distances[distance])

            for event in new_battle_events:
                if event.item and event not in collected_locations:
                    collected_locations.add(event)
                    state.collect(event.item, True, event)

        if len(new_spheres) > 0:
            for sphere in new_spheres:
                spheres.append(sphere)

                for location in sphere:
                    if location.item and location not in collected_locations:
                        collected_locations.add(location)
                        state.collect(location.item, True, location)
        else:
            spheres.append(locations)
            break

    for world in multiworld.get_game_worlds("Pokemon Crystal"):
        if world.options.level_scaling == LevelScaling.option_off:
            continue

        # red_goal_adjustment = 73 / 40  # adjusts for when red is goal, 1.8 times higher level
        # e4_base_level = 40

        for sphere in spheres:
            trainer_locations = [loc for loc in sphere if loc.player == world.player and "trainer scaling" in loc.tags]
            encounter_locations = [loc for loc in sphere if loc.player == world.player and "static scaling" in loc.tags]

            trainer_locations.sort(key=lambda loc: world.trainer_name_list.index(loc.name))
            encounter_locations.sort(key=lambda loc: world.encounter_name_list.index(loc.name))

            for trainer_location in trainer_locations:
                new_base_level = world.trainer_level_list.pop(0)
                old_base_level = world.trainer_name_level_dict[trainer_location.name]

                # if trainer_location.name in ["WILL_1", "KOGA_1", "BRUNO_1", "KAREN_1", "CHAMPION_1"]:
                #     e4_base_level = new_base_level
                # elif trainer_location.name == "RED_1":
                #     new_base_level = max(new_base_level, round(e4_base_level * red_goal_adjustment))

                trainer_data = world.generated_trainers[trainer_location.name]
                new_pokemon = []
                for pokemon in trainer_data.pokemon:
                    new_level = round(min((new_base_level * pokemon.level / old_base_level),
                                          (new_base_level + pokemon.level - old_base_level)))
                    new_level = bound(new_level, 1, 100)
                    new_pokemon.append(pokemon._replace(level=new_level))
                    logging.debug(
                        f"Setting level {new_level} {pokemon.pokemon} for {trainer_location.name} for {world.player_name}")
                world.generated_trainers[trainer_location.name] = trainer_data._replace(pokemon=new_pokemon)

            for encounter_location in encounter_locations:
                new_base_level = world.encounter_level_list.pop(0)

                pokemon_data = world.generated_static[encounter_location.name]
                new_pokemon = pokemon_data._replace(level=new_base_level)
                world.generated_static[encounter_location.name] = new_pokemon
                logging.debug(
                    f"Setting level {new_base_level} for static {pokemon_data.pokemon} for {world.player_name}")

        world.finished_level_scaling.set()
