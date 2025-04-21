import logging
from typing import TYPE_CHECKING

from .data import data
from .options import FreeFlyLocation, Route32Condition, JohtoOnly
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


def get_free_fly_locations(world: "PokemonCrystalWorld"):
    location_pool = data.fly_regions[:]

    if world.options.route_32_condition.value != Route32Condition.option_any_badge:
        # Azalea, Goldenrod
        location_pool = [region for region in location_pool if region.id not in [18, 20]]
    if not world.options.remove_ilex_cut_tree:
        # Goldenrod
        location_pool = [region for region in location_pool if region.id != 20]
    if world.options.johto_only:
        # Pallet, Viridian, Pewter, Cerulean, Vermilion, Lavender, Saffron, Celadon, Fuchsia, Cinnabar
        location_pool = [region for region in location_pool if region.id not in [2, 3, 4, 5, 7, 8, 9, 10, 11, 12]]
    if world.options.johto_only.value == JohtoOnly.option_on:
        # Mt. Silver
        location_pool = [region for region in location_pool if region.id != 26]

    # only do any of this if there even is a fly location blocklist
    if world.options.free_fly_blocklist:

        # figure out how many fly locations are needed
        locations_required = 1
        if world.options.free_fly_location.value == FreeFlyLocation.option_free_fly_and_map_card:
            locations_required = 2

        # calculate what the list of locations would be after the blocklist
        location_pool_after_blocklist = [item for item in location_pool if
                                         item.name not in world.options.free_fly_blocklist]

        # if the list after the blocked locations are removed is long enough to satisfy all the requested fly locations, set the location pool to it
        if len(location_pool_after_blocklist) >= locations_required:
            location_pool = location_pool_after_blocklist

    world.random.shuffle(location_pool)
    if world.options.free_fly_location.value in [FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card]:
        world.free_fly_location = location_pool.pop()
    if world.options.free_fly_location.value in [FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card]:
        world.map_card_fly_location = location_pool.pop()


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
        "9": 0xff
    }
    return [charmap[char] if char in charmap else charmap["?"] for char in text]


def bound(value: int, lower_bound: int, upper_bound: int) -> int:
    return max(min(value, upper_bound), lower_bound)


def replace_map_tiles(patch, map_name: str, x: int, y: int, tiles):
    # x and y are 0 indexed
    tile_index = (y * data.map_sizes[map_name].width) + x
    base_address = data.rom_addresses[f"{map_name}_Blocks"]

    logging.debug(f"Writing {len(tiles)} new tile(s) to map {map_name} at {x},{y}")
    write_bytes(patch, tiles, base_address + tile_index)


def write_bytes(patch, byte_array, address):
    patch.write_token(
        APTokenTypes.WRITE,
        address,
        bytes(byte_array)
    )
