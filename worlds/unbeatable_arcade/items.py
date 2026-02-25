from __future__ import annotations

from typing import TYPE_CHECKING

import math

from BaseClasses import Item, ItemClassification

from . import songs
from .game_info import GAME_NAME
from .options import UNBEATABLEArcadeOptions
from .songs import difficulty_key_from_rank

if TYPE_CHECKING:
    from .world import UNBEATABLEArcadeWorld

DEFAULT_CLASSIFICATIONS = {
    "Song": ItemClassification.progression_deprioritized,
    # Will no longer be filler once challenge board is included
    # because certain characters are needed for some challenges
    "Character": ItemClassification.filler,
    "Trap": ItemClassification.trap
}

CHARACTER_NAMES = [
    "Beat",
    "Beat (Hoodie)",
    "Beat (Guitar)",
    "Beat (Nothing)",
    "Beat (Up)",
    "Clef",
    "Quaver",
    "Quaver (Acoustic)",
    "Quaver (CQC)",
    "Treble",
    "Rest"
]

TRAP_NAMES = [
    "Silence Trap",
    "Stealth Trap",
    "Rainbow Trap",
    "Zoom Trap",
    "Crawl Trap"
]

# This isn't a real item, but UNBEATABLE has no infinite filler items
FILLER_NAME = "Worn Out Tape"

SONG_PREFIX = "Progressive Song: "
CHAR_PREFIX = "Character: "

# Generate IDs based on the lists so that it's not a nightmare to maintain game updates
ITEM_NAME_TO_ID = {}

curr_id = 1
for song in songs.all_songs:
    ITEM_NAME_TO_ID[f"{SONG_PREFIX}{song["name"]}"] = curr_id
    curr_id += 1

for char in CHARACTER_NAMES:
    ITEM_NAME_TO_ID[f"{CHAR_PREFIX}{char}"] = curr_id
    curr_id += 1

for trap in TRAP_NAMES:
    ITEM_NAME_TO_ID[trap] = curr_id
    curr_id += 1

ITEM_NAME_TO_ID[FILLER_NAME] = curr_id

ITEM_NAME_GROUPS = {
    "songs": set(f"{SONG_PREFIX}{entry["name"]}" for entry in songs.all_songs),
    "characters": set(f"{CHAR_PREFIX}{char}" for char in CHARACTER_NAMES),
    "traps": set(TRAP_NAMES),
    "filler": {FILLER_NAME}
}

# Add our aliases as item name groups (hacky way to make them valid hints)
for alias_entry in songs.song_aliases:
    for alias in alias_entry["aliases"]:
        ITEM_NAME_GROUPS[f"{SONG_PREFIX}{alias}"] = {f"{SONG_PREFIX}{alias_entry["name"]}"}


class UNBEATABLEArcadeItem(Item):
    game = GAME_NAME


def get_diff_count(options: UNBEATABLEArcadeOptions) -> int:
    # Min difficulty ranges from 0 to 4, and max ranges from 0 to 5.
    # We need enough progressive diffs to unlock min difficulty and get up to max
    return (options.max_difficulty - options.min_difficulty) + 1


def get_trap_count(item_count: int, trap_amount: float) -> int:
    trap_percent = trap_amount / 100
    return math.floor(float(item_count) * trap_percent)


def get_max_items():
    # There are a maximum of 6 progressive items per song
    count = len(songs.all_songs) * 6
    count += len(CHARACTER_NAMES)

    good_item_count = count
    for i in range(0, len(TRAP_NAMES)):
        # There is a maximum trap item amount of 10%
        count += get_trap_count(good_item_count, 10)

    return count


def add_traps_non_local(world: UNBEATABLEArcadeWorld) -> None:
    non_local_items = world.options.non_local_items.value
    for trap_name in TRAP_NAMES:
        non_local_items.add(trap_name)


def get_random_filler_item_name(world: UNBEATABLEArcadeWorld) -> str:
    if world.options.use_traps:
        return world.random.choice(TRAP_NAMES)

    return FILLER_NAME


def create_item_with_classification(world: UNBEATABLEArcadeWorld, name: str) -> UNBEATABLEArcadeItem:
    classification = ItemClassification.filler
    item_id = 0
    
    if name in ITEM_NAME_TO_ID:
        item_id = ITEM_NAME_TO_ID[name]

    if name in TRAP_NAMES:
        classification = DEFAULT_CLASSIFICATIONS["Trap"]
    elif name in CHARACTER_NAMES:
        classification = DEFAULT_CLASSIFICATIONS["Character"]
    elif any(f"{SONG_PREFIX}{song["name"]}" == name for song in songs.all_songs):
        classification = DEFAULT_CLASSIFICATIONS["Song"]

    return UNBEATABLEArcadeItem(name, classification, item_id, world.player)


def get_item_count(world: UNBEATABLEArcadeWorld) -> int:
    diff_count = get_diff_count(world.options)

    item_count = 0
    for song in world.included_songs:
        for i in range(0, diff_count):
            diff_rank = i + world.options.min_difficulty
            diff_key = difficulty_key_from_rank(diff_rank)
            if song[diff_key] < 0:
                continue
            
            item_count += 1

    item_count += len(CHARACTER_NAMES)

    # Starting items are removed from the pool
    item_count -= world.options.start_song_count
    item_count -= world.options.start_char_count

    if world.options.use_traps:
        good_item_count = item_count
        item_count += get_trap_count(good_item_count, world.options.silence_amount)
        item_count += get_trap_count(good_item_count, world.options.stealth_amount)
        item_count += get_trap_count(good_item_count, world.options.rainbow_amount)
        item_count += get_trap_count(good_item_count, world.options.zoom_amount)
        item_count += get_trap_count(good_item_count, world.options.crawl_amount)

    return item_count


def create_all_items(world: UNBEATABLEArcadeWorld) -> None:
    # Grant the player's starting songs
    start_song_count = world.options.start_song_count
    start_song_names = []
    # Only songs with a valid first difficulty can be start songs, otherwise
    # get_item_count's assumption (each start song removes 1 valid item) breaks
    first_diff_key = difficulty_key_from_rank(world.options.min_difficulty)
    valid_start_songs = [s for s in world.included_songs if s[first_diff_key] >= 0]
    for i in range(0, start_song_count):
        new_song_name = world.random.choice(valid_start_songs)["name"]
        while new_song_name in start_song_names:
            # In case we roll the same song twice, just roll again
            new_song_name = world.random.choice(valid_start_songs)["name"]

        start_song_names.append(new_song_name)

        song_item_name = f"{SONG_PREFIX}{new_song_name}"
        new_song = world.create_item(song_item_name)
        world.push_precollected(new_song)

    # Grant the player's starting characters
    start_char_count = world.options.start_char_count
    start_char_names = []
    for i in range(0, start_char_count):
        new_char_name = world.random.choice(CHARACTER_NAMES)
        while new_char_name in start_char_names:
            new_char_name = world.random.choice(CHARACTER_NAMES)

        start_char_names.append(new_char_name)

        char_item_name = f"{CHAR_PREFIX}{new_char_name}"
        new_char = world.create_item(char_item_name)
        world.push_precollected(new_char)

    item_pool: list[Item] = []

    diff_count = get_diff_count(world.options)

    for song in world.included_songs:
        song_item_name = f"{SONG_PREFIX}{song["name"]}"
        for i in range(0, diff_count):
            if i == 0 and song["name"] in start_song_names:
                # We started with the first difficulty of this song
                continue

            diff_rank = i + world.options.min_difficulty
            diff_key = difficulty_key_from_rank(diff_rank)
            if song[diff_key] < 0:
                continue
            
            item_pool.append(world.create_item(song_item_name))

    for char in CHARACTER_NAMES:
        if char in start_char_names:
            continue

        char_item_name = f"{CHAR_PREFIX}{char}"
        item_pool.append(world.create_item(char_item_name))

    if world.options.use_traps:
        item_count = len(item_pool)
        for i in range(0, get_trap_count(item_count, world.options.silence_amount)):
            item_pool.append(world.create_item(TRAP_NAMES[0]))
        for i in range(0, get_trap_count(item_count, world.options.stealth_amount)):
            item_pool.append(world.create_item(TRAP_NAMES[1]))
        for i in range(0, get_trap_count(item_count, world.options.rainbow_amount)):
            item_pool.append(world.create_item(TRAP_NAMES[2]))
        for i in range(0, get_trap_count(item_count, world.options.zoom_amount)):
            item_pool.append(world.create_item(TRAP_NAMES[3]))
        for i in range(0, get_trap_count(item_count, world.options.crawl_amount)):
            item_pool.append(world.create_item(TRAP_NAMES[4]))


    world.multiworld.itempool += item_pool