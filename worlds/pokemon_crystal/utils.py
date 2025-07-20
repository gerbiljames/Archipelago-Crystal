import logging
from random import Random
from typing import TYPE_CHECKING

from Options import Toggle
from .data import data, EvolutionData, EvolutionType, StartingTown, FlyRegion
from .options import FreeFlyLocation, Route32Condition, JohtoOnly, RandomizeBadges, UndergroundsRequirePower, \
    Route3Access, EliteFourRequirement, Goal, Route44AccessRequirement, BlackthornDarkCaveAccess, RedRequirement, \
    MtSilverRequirement, HMBadgeRequirements, RedGyaradosAccess, EarlyFly, RadioTowerRequirement, \
    BreedingMethodsRequired, Shopsanity
from ..Files import APTokenTypes

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def get_random_filler_item(random):
    # weights are roughly based on vanilla occurrence
    weighted_pool = [["RARE_CANDY"] * 3, ["ETHER", "ELIXER", "MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY"] * 5,
                     ["WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE", "MOON_STONE"] * 2,
                     ["ESCAPE_ROPE"] * 3, ["NUGGET", "STAR_PIECE", "STARDUST", "PEARL", "BIG_PEARL"] * 2,
                     ["POKE_BALL", "GREAT_BALL", "ULTRA_BALL"] * 5,
                     ["POTION", "SUPER_POTION", "ENERGY_ROOT", "ENERGYPOWDER"] * 12,
                     ["HYPER_POTION", "FULL_RESTORE"] * 2, ["REPEL", "SUPER_REPEL", "MAX_REPEL"] * 3,
                     ["REVIVE", "REVIVAL_HERB"] * 4 + ["MAX_REVIVE"] * 2,
                     ["HP_UP", "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", "IRON"] * 5,
                     ["GUARD_SPEC", "DIRE_HIT", "X_ATTACK", "X_DEFEND", "X_SPEED", "X_SPECIAL"] * 2,
                     ["HEAL_POWDER", "BURN_HEAL", "PARLYZ_HEAL", "ICE_HEAL", "ANTIDOTE", "AWAKENING", "FULL_HEAL"] * 5]
    group = random.choice(weighted_pool)
    return random.choice(group)


def get_random_ball(random: Random):
    balls = ["POKE_BALL", "GREAT_BALL", "ULTRA_BALL", "FRIEND_BALL", "HEAVY_BALL", "LOVE_BALL", "LEVEL_BALL",
             "LURE_BALL", "FAST_BALL"]
    ball_weights = [50, 30, 20, 1, 1, 1, 1, 1, 1]
    return random.choices(balls, weights=ball_weights)[0]


def adjust_options(world: "PokemonCrystalWorld"):
    __adjust_meta_options(world)
    __adjust_option_problems(world)

def __adjust_meta_options(world: "PokemonCrystalWorld"):
    __saffron_tea_random(world)

def __adjust_option_problems(world: "PokemonCrystalWorld"):
    __adjust_options_radio_tower_and_route_44(world)
    __adjust_options_johto_only(world)
    __adjust_options_gyarados(world)
    __adjust_options_early_fly(world)
    __adjust_options_encounters_and_breeding(world)
    __adjust_options_race_mode(world)

def __saffron_tea_random(world: "PokemonCrystalWorld"):
    teaset = world.options.saffron_gatehouse_tea.value
    if "_Random" in teaset:
        teaset.remove("_Random")
        for direction in ["North", "East", "South", "West"]:
            if direction not in teaset:
                if world.random.randint(0, 1) == 1:
                    teaset.add(direction)

def __adjust_options_radio_tower_and_route_44(world: "PokemonCrystalWorld"):
    if (world.options.randomize_badges.value != RandomizeBadges.option_completely_random
            and world.options.radio_tower_count.value > (7 if world.options.johto_only else 15)):
        world.options.radio_tower_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Radio Tower Count >%d incompatible with vanilla or shuffled badges. "
            "Changing Radio Tower Count to %d for player %s.",
            world.options.radio_tower_count.value,
            world.options.radio_tower_count.value,
            world.player_name)

    if (world.options.route_44_access_count.value > (7 if world.options.johto_only else 15)
            and world.options.randomize_badges.value != RandomizeBadges.option_completely_random):
        world.options.route_44_access_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Route 44 Access Count >%d incompatible with vanilla or shuffled badges. "
            "Changing Route 44 Access Count to %d for player %s.",
            world.options.route_44_access_count.value,
            world.options.route_44_access_count.value,
            world.player_name)

    if (world.options.route_44_access_requirement.value == Route44AccessRequirement.option_gyms
            and world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_vanilla
            and world.options.route_44_access_count.value > (7 if world.options.johto_only else 15)):
        world.options.route_44_access_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Route 44 Access Gyms >%d incompatible with vanilla Dark Cave. "
            "Changing Route 44 Access Gyms to %d for player %s.",
            world.options.route_44_access_count.value,
            world.options.route_44_access_count.value,
            world.player_name)

    if (world.options.radio_tower_requirement.value == RadioTowerRequirement.option_gyms
            and world.options.radio_tower_count.value > (7 if world.options.johto_only else 15)):
        world.options.radio_tower_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Radio Tower Gyms >%d is impossible. "
            "Changing Radio Tower Gyms to %d for player %s.",
            world.options.radio_tower_count.value,
            world.options.radio_tower_count.value,
            world.player_name)

def __adjust_options_johto_only(world: "PokemonCrystalWorld"):
    if world.options.johto_only:

        if world.options.goal == Goal.option_red and world.options.johto_only == JohtoOnly.option_on:
            world.options.goal.value = Goal.option_elite_four
            logging.warning(
                "Pokemon Crystal: Red goal is incompatible with Johto Only "
                "without Silver Cave. Changing goal to Elite Four for player %s.",
                world.player_name)

        if (world.options.elite_four_requirement.value == EliteFourRequirement.option_gyms
                and world.options.elite_four_count.value > 8):
            world.options.elite_four_count.value = 8
            logging.warning(
                "Pokemon Crystal: Elite Four Gyms >8 incompatible with Johto Only. "
                "Changing Elite Four Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.red_requirement.value == RedRequirement.option_gyms
                and world.options.red_count.value > 8):
            world.options.red_count.value = 8
            logging.warning(
                "Pokemon Crystal: Red Gyms >8 incompatible with Johto Only. "
                "Changing Red Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.mt_silver_requirement.value == MtSilverRequirement.option_gyms
                and world.options.mt_silver_count.value > 8):
            world.options.mt_silver_count.value = 8
            logging.warning(
                "Pokemon Crystal: Mt. Silver Gyms >8 incompatible with Johto Only. "
                "Changing Mt. Silver Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.route_44_access_requirement.value == Route44AccessRequirement.option_gyms
                and world.options.route_44_access_count.value > 8):
            world.options.route_44_access_count.value = 8
            logging.warning(
                "Pokemon Crystal: Route 44 Access Gyms >8 incompatible with Johto Only. "
                "Changing Route 44 Access Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.radio_tower_requirement.value == RadioTowerRequirement.option_gyms
                and world.options.radio_tower_count.value > 7):
            world.options.radio_tower_count.value = 7
            logging.warning(
                "Pokemon Crystal: Radio Tower Gyms >7 incompatible with Johto Only. "
                "Changing Radio Tower Gyms to 7 for player %s.",
                world.player_name)

        if world.options.evolution_gym_levels.value < 8:
            world.options.evolution_gym_levels.value = 8
            logging.warning(
                "Pokemon Crystal: Evolution Gym Levels <8 incompatible with Johto Only. "
                "Changing Evolution Gym Levels to 8 for player %s.",
                world.player_name)

        if world.options.randomize_badges != RandomizeBadges.option_completely_random:
            if world.options.red_count.value > 8 and world.options.red_requirement == RedRequirement.option_badges:
                world.options.red_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Red Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Red Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.elite_four_count.value > 8 and
                    world.options.elite_four_requirement.value == EliteFourRequirement.option_badges):
                world.options.elite_four_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Elite Four Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Elite Four Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.radio_tower_count.value > 8
                    and world.options.radio_tower_requirement.value == RadioTowerRequirement.option_badges):
                world.options.radio_tower_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Radio Tower Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Radio Tower Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.mt_silver_count.value > 8 and
                    world.options.mt_silver_requirement.value == MtSilverRequirement.option_badges):
                world.options.mt_silver_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Mt. Silver Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Mt. Silver Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.route_44_access_count.value > 8 and
                    world.options.route_44_access_requirement.value == Route44AccessRequirement.option_badges):
                world.options.route_44_access_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Route 44 Access Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Route 44 Access Badges to 8 for player %s.",
                    world.player_name)

def __adjust_options_gyarados(world: "PokemonCrystalWorld"):
    if (world.options.red_gyarados_access
            and world.options.randomize_badges.value == RandomizeBadges.option_vanilla
            and "Whirlpool" and not world.options.hm_badge_requirements == HMBadgeRequirements.option_no_badges
            and "Whirlpool" not in world.options.remove_badge_requirement):
        world.options.red_gyarados_access.value = RedGyaradosAccess.option_vanilla
        logging.warning("Pokemon Crystal: Red Gyarados access requires Whirlpool and Vanilla Badges are not "
                        "compatible, setting Red Gyarados access to vanilla for player %s.",
                        world.player_name)

def __adjust_options_early_fly(world: "PokemonCrystalWorld"):
    if (world.options.early_fly
            and world.options.randomize_starting_town
            and world.options.randomize_badges.value != RandomizeBadges.option_completely_random
            and "Fly" not in world.options.remove_badge_requirement
            and world.options.hm_badge_requirements != HMBadgeRequirements.option_no_badges):
        world.options.early_fly.value = EarlyFly.option_false
        logging.warning("Pokemon Crystal: Early fly is not compatible with Random Starting Town if Badges are "
                        "not completely random. Disabling Early Fly for player %s",
                        world.player_name)

def __adjust_options_encounters_and_breeding(world: "PokemonCrystalWorld"):
    if (world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto
            and "Ditto" in world.options.wild_encounter_blocklist):
        world.options.breeding_methods_required.value = BreedingMethodsRequired.option_none
        logging.warning(
            "Ditto cannot be blocklisted while Ditto only breeding is enabled. Disabling breeding logic for player %s.",
            world.player_name)

    if "Land" not in world.options.wild_encounter_methods_required and "Fishing" not in world.options.wild_encounter_methods_required:
        world.options.wild_encounter_methods_required.value.add(world.random.choice(("Land", "Fishing")))
        logging.warning(
            "At least one of Land or Fishing must be enabled in wild encounter methods required. "
            "Adding one at random for player %s.",
            world.player_name)

    if (world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto
            and not world.options.wild_encounter_methods_required):
        world.options.breeding_methods_required.value = BreedingMethodsRequired.option_none
        logging.warning(
            "At least one wild encounter type must be available for Ditto only breeding. "
            "Disabling breeding logic for player %s.",
            world.player_name)

def __adjust_options_race_mode(world: "PokemonCrystalWorld"):
    # In race mode we don't patch any item location information into the ROM
    if world.multiworld.is_race and not world.options.remote_items:
        logging.warning("Pokemon Crystal: Forcing Player %s (%s) to use remote items due to race mode.",
                        world.player, world.player_name)
        world.options.remote_items.value = Toggle.option_true


def get_random_starting_town(world: "PokemonCrystalWorld"):
    location_pool = data.starting_towns[:]
    location_pool = [loc for loc in location_pool if _starting_town_valid(world, loc)]

    blocklist = set(world.options.starting_town_blocklist.value)
    if "_Johto" in blocklist:
        blocklist.remove("_Johto")
        blocklist.update(town.name for town in data.starting_towns if town.johto)
    if "_Kanto" in blocklist:
        blocklist.remove("_Kanto")
        blocklist.update(town.name for town in data.starting_towns if not town.johto)

    filtered_pool = [loc for loc in location_pool if loc.name not in blocklist]
    if not filtered_pool: filtered_pool = location_pool

    world.random.shuffle(filtered_pool)
    world.starting_town = filtered_pool.pop()
    logging.debug(f"Starting town({world.player_name}): {world.starting_town.name}")

    if world.starting_town.name == "Cianwood City":
        world.multiworld.early_items[world.player]["HM03 Surf"] = 1


def _starting_town_valid(world: "PokemonCrystalWorld", starting_town: StartingTown):
    if world.options.johto_only and not starting_town.johto: return False
    if world.options.randomize_badges != RandomizeBadges.option_completely_random and starting_town.restrictive_start:
        return False

    immediate_hiddens = world.options.randomize_hidden_items and not world.options.require_itemfinder
    johto_shopsanity = world.options.shopsanity in (Shopsanity.option_johto, Shopsanity.option_both)
    kanto_shopsanity = world.options.shopsanity in (Shopsanity.option_kanto, Shopsanity.option_both)

    if starting_town.name == "Cianwood City":
        return world.options.static_pokemon_required and (
                    (world.options.trainersanity and immediate_hiddens) or johto_shopsanity)
    if starting_town.name in ("Lake of Rage", "Mahogany Town"):
        return not world.options.mount_mortar_access or world.options.trainersanity or johto_shopsanity

    if starting_town.name in ("Pallet Town", "Viridian City", "Pewter City"):
        return (immediate_hiddens or world.options.route_3_access == Route3Access.option_vanilla or kanto_shopsanity
                or world.options.randomize_berry_trees)
    if starting_town.name == "Rock Tunnel":
        return world.options.trainersanity
    if starting_town.name == "Vermilion City":
        return "South" not in world.options.saffron_gatehouse_tea or world.options.undergrounds_require_power not in (
            UndergroundsRequirePower.option_both, UndergroundsRequirePower.option_north_south) or kanto_shopsanity
    if starting_town.name == "Cerulean City":
        return "North" not in world.options.saffron_gatehouse_tea or immediate_hiddens or kanto_shopsanity
    if starting_town.name == "Celadon City":
        return "West" not in world.options.saffron_gatehouse_tea or immediate_hiddens or kanto_shopsanity
    if starting_town.name in ("Lavender Town", "Fuchsia City"):
        return "East" not in world.options.saffron_gatehouse_tea or (
                immediate_hiddens and world.options.randomize_berry_trees) or kanto_shopsanity

    return True


def get_fly_regions(world: "PokemonCrystalWorld") -> list[FlyRegion]:
    fly_regions = list(data.fly_regions)

    if world.options.johto_only == JohtoOnly.option_on:
        fly_regions = [region for region in fly_regions if region.name != "Silver Cave"]

    if world.options.johto_only:
        fly_regions = [region for region in fly_regions if region.johto]

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
    if world.options.johto_only:
        location_pool = [region for region in location_pool if region.johto]
    if world.options.johto_only.value == JohtoOnly.option_on:
        # Mt. Silver
        location_pool = [region for region in location_pool if region.name != "Silver Cave"]

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

    world.random.shuffle(location_pool)
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        world.free_fly_location = location_pool.pop()
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        world.map_card_fly_location = location_pool.pop()


def evolution_in_logic(world: "PokemonCrystalWorld", evolution: EvolutionData):
    if evolution.evo_type is EvolutionType.Level:
        return "Level" in world.options.evolution_methods_required.value
    if evolution.evo_type is EvolutionType.Happiness:
        return "Happiness" in world.options.evolution_methods_required.value
    if evolution.evo_type is EvolutionType.Item:
        return "Use Item" in world.options.evolution_methods_required.value
    if evolution.evo_type is EvolutionType.Stats:
        return "Level Tyrogue" in world.options.evolution_methods_required.value
    return False


def evolution_location_name(world: "PokemonCrystalWorld", from_pokemon: str, to_pokemon: str):
    return (f"Evolve {world.generated_pokemon[from_pokemon].friendly_name} "
            f"into {world.generated_pokemon[to_pokemon].friendly_name}")


def convert_to_ingame_text(text: str):
    charmap = {
        "…": 0x75, " ": 0x7f, "A": 0x80, "B": 0x81, "C": 0x82, "D": 0x83, "E": 0x84, "F": 0x85, "G": 0x86, "H": 0x87,
        "I": 0x88, "J": 0x89, "K": 0x8a, "L": 0x8b, "M": 0x8c, "N": 0x8d, "O": 0x8e, "P": 0x8f, "Q": 0x90, "R": 0x91,
        "S": 0x92, "T": 0x93, "U": 0x94, "V": 0x95, "W": 0x96, "X": 0x97, "Y": 0x98, "Z": 0x99, "(": 0x9a, ")": 0x9b,
        ":": 0x9c, ";": 0x9d, "[": 0x9e, "]": 0x9f, "a": 0xa0, "b": 0xa1, "c": 0xa2, "d": 0xa3, "e": 0xa4, "f": 0xa5,
        "g": 0xa6, "h": 0xa7, "i": 0xa8, "j": 0xa9, "k": 0xaa, "l": 0xab, "m": 0xac, "n": 0xad, "o": 0xae, "p": 0xaf,
        "q": 0xb0, "r": 0xb1, "s": 0xb2, "t": 0xb3, "u": 0xb4, "v": 0xb5, "w": 0xb6, "x": 0xb7, "y": 0xb8, "z": 0xb9,
        "Ä": 0xc0, "Ö": 0xc1, "Ü": 0xc2, "ä": 0xc3, "ö": 0xc4, "ü": 0xc5, "'": 0xe0, "-": 0xe3, "?": 0xe6, "!": 0xe7,
        ".": 0xe8, "&": 0xe9, "é": 0xea, "→": 0xeb, "▷": 0xec, "▶": 0xed, "▼": 0xee, "♂": 0xef, "¥": 0xf0, "/": 0xf3,
        ",": 0xf4, "0": 0xf6, "1": 0xf7, "2": 0xf8, "3": 0xf9, "4": 0xfa, "5": 0xfb, "6": 0xfc, "7": 0xfd, "8": 0xfe,
        "9": 0xff, "_": 0xe3, "♀": 0xf5
    }
    return [charmap[char] if char in charmap else charmap["?"] for char in text]


def bound(value: int, lower_bound: int, upper_bound: int) -> int:
    return max(min(value, upper_bound), lower_bound)


def replace_map_tiles(patch, map_name: str, x: int, y: int, tiles):
    # x and y are 0 indexed
    tile_index = (y * data.map_sizes[map_name][0]) + x
    base_address = data.rom_addresses[f"{map_name}_Blocks"]

    logging.debug(f"Writing {len(tiles)} new tile(s) to map {map_name} at {x},{y}")
    write_bytes(patch, tiles, base_address + tile_index)


def write_bytes(patch, byte_array, address):
    patch.write_token(
        APTokenTypes.WRITE,
        address,
        bytes(byte_array)
    )
