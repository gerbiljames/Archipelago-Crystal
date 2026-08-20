import functools
import logging
from collections import defaultdict
from typing import TYPE_CHECKING

from .data import data, FlyRegion, Landmark, FlypointWarp
from .options import FreeFlyLocation, Route32Condition, JohtoOnly, RandomizeFlyUnlocks
from .utils import should_include_region

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def get_fly_regions(world: "PokemonCrystalWorld") -> list[FlyRegion]:
    fly_regions = list(data.fly_regions)

    if world.options.johto_only == JohtoOnly.option_on:
        fly_regions = [region for region in fly_regions if region.name != "Silver Cave"]

    if world.options.johto_only:
        fly_regions = [region for region in fly_regions if region.johto]

    if world.options.randomize_fly_destinations:
        # shuffled destinations fill flypoint slots by id, so the pool has to stay contiguous
        fly_regions = [region for region in fly_regions if region.id <= len(fly_regions)]

    return fly_regions


def get_free_fly_locations(world: "PokemonCrystalWorld"):
    location_pool = data.fly_regions[:]

    if not world.options.randomize_starting_town:
        location_pool = \
            [region for region in location_pool if not region.exclude_vanilla_start]
        if world.options.route_32_condition.value != Route32Condition.option_any_badge:
            # Azalea, Goldenrod
            location_pool = [region for region in location_pool if region.name not in ("Azalea Town", "Goldenrod City")]
        if not world.options.remove_ilex_cut_tree and world.options.route_32_condition.value != Route32Condition.option_any_badge:
            # Goldenrod
            location_pool = [region for region in location_pool if region.name != "Goldenrod City"]
    available_regions = set(get_fly_regions(world))
    location_pool = [region for region in location_pool if region in available_regions]

    if world.options.randomize_starting_town:
        world.options.free_fly_blocklist.value.add(world.starting_town.name)

    blocklist = set(world.options.free_fly_blocklist.value)
    if "_Johto" in blocklist:
        blocklist.remove("_Johto")
        blocklist.update(town.name for town in data.fly_regions if town.johto)
    if "_Kanto" in blocklist:
        blocklist.remove("_Kanto")
        blocklist.update(town.name for town in data.fly_regions if not town.johto)

    # only do any of this if there even is a fly location blocklist
    if blocklist:

        # figure out how many fly locations are needed
        locations_required = 1
        if world.options.free_fly_location.value == FreeFlyLocation.option_free_fly_and_map_card:
            locations_required = 2

        # calculate what the list of locations would be after the blocklist
        location_pool_after_blocklist = [item for item in location_pool if
                                         item.name not in blocklist]

        # if the list after the blocked locations are removed is long enough to satisfy all the requested fly locations, set the location pool to it
        if len(location_pool_after_blocklist) >= locations_required:
            location_pool = location_pool_after_blocklist
        else:
            logging.warning("Pokemon Crystal: All valid free fly locations blocked for player %s (%s). "
                            "Using global list instead.", world.player, world.player_name)

    world.random.shuffle(location_pool)
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        world.free_fly_location = location_pool.pop()
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        world.map_card_fly_location = location_pool.pop()


@functools.cache
def _arrival_index() -> dict[tuple[str, int], list]:
    index = defaultdict(list)
    for conn in data.entrance_connections.values():
        index[(conn.arrival_map, conn.arrival_warp_index)].append(conn)
    return index


def flypoint_arrival_connections(flypoint: FlypointWarp) -> list:
    """Connections whose arrival is this flypoint's warp tile."""
    return _arrival_index().get((flypoint.map_name, flypoint.warp_index), [])


def _get_flyable_warps() -> dict[Landmark, list[FlypointWarp]]:
    flypoints = {
        l: [flypoint for flypoint in flypoints if flypoint_arrival_connections(flypoint)]
        for l, flypoints in data.flypoints.items()
    }
    flypoints[Landmark.NationalPark] = [
        flypoint for flypoint in flypoints[Landmark.NationalPark]
        if flypoint.map_name != "NationalParkBugContest"
    ]
    return flypoints


def randomize_fly_destinations(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker or not world.options.randomize_fly_destinations: return

    def flyable_filter(flypoint):
        if not world.options.route_23_restored and flypoint.map_name == "Route23Restored":
            return False
        # A flypoint targets a specific warp tile on an outdoor map; that tile
        # may sit in a sub-region gated by another option (e.g. the Flooded
        # Mine entrance tile lives in REGION_CHERRYGROVE_CITY:FLOODED_MINE_
        # ENTRANCE, which only exists when flooded_mine is on). Drop those.
        for conn in flypoint_arrival_connections(flypoint):
            if not should_include_region(data.regions[conn.entrance_region], world):
                return False
        return True

    if world.options.johto_only.value == JohtoOnly.option_off:
        eligible_landmarks = Landmark.all()
    else:
        eligible_landmarks = Landmark.johto_only()

    num_flypoints = len(get_fly_regions(world))

    if world.options.johto_only.value == JohtoOnly.option_on \
            or world.options.randomize_fly_unlocks.value == RandomizeFlyUnlocks.option_exclude_silver_cave:
        eligible_landmarks.remove(Landmark.Route28)
        eligible_landmarks.remove(Landmark.SilverCave)
        # option_on already drops Silver Cave from the pool
        if world.options.johto_only.value != JohtoOnly.option_on:
            num_flypoints -= 1

    flyable_flypoints = {
        l: [flypoint for flypoint in flypoints if flyable_filter(flypoint)]
        for l, flypoints in _get_flyable_warps().items()
    }
    eligible_landmarks = [l for l in eligible_landmarks if len(flyable_flypoints.get(l, [])) > 0]
    selected_landmarks = world.random.sample(eligible_landmarks, num_flypoints)
    fly_destinations = [world.random.choice(flyable_flypoints[l]) for l in selected_landmarks]

    if world.options.randomize_fly_unlocks.value == RandomizeFlyUnlocks.option_exclude_silver_cave \
            and world.options.johto_only.value != JohtoOnly.option_on:
        silver_index = next(fly_region.id for fly_region in data.fly_regions if fly_region.name == "Silver Cave")
        silver_flypoint = data.flypoints[Landmark.SilverCave][0]
        fly_destinations.insert(silver_index, silver_flypoint)

    world.fly_destinations = fly_destinations


