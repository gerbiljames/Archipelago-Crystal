from __future__ import annotations

from typing import TYPE_CHECKING

import bisect

from BaseClasses import CollectionState

from . import custom_rating_calculator
from .star_calculator import get_expected_acc_curve
from ..items import SONG_PREFIX, get_diff_count
from ..options import UNBEATABLEArcadeOptions
from ..songs import difficulty_key_from_rank

if TYPE_CHECKING:
    from ..world import UNBEATABLEArcadeWorld

expected_fail_threshold = 55


def get_songs_with_ratings(songs: list, options: UNBEATABLEArcadeOptions) -> dict[str, dict[int, float]]:
    rated_songs = {}

    skill_rating = float(options.skill_rating) / 1000
    diff_count = get_diff_count(options)

    allow_pfc = options.allow_pfc
    acc_curve_cutoff = float(options.acc_curve_cutoff) / 100
    acc_curve_bias = float(options.acc_curve_bias) / 100
    acc_curve_low_bias = float(options.acc_curve_low_bias) / 100

    # Calculate the expected rating to be earned from each song in the list
    for song in songs:
        new_rating = {}
        # Populate the rating entries with only the difficulties we'll unlock in the AP
        # This makes it easy to index the expected ratings by Progressive Difficulty inventory count
        for i in range(0, diff_count):
            diff_rank = options.min_difficulty + i
            diff_key = difficulty_key_from_rank(diff_rank)

            diff_level = song[diff_key]
            if diff_level < 0:
                # Negative values represent a nonexistent difficulty, so we can't get rating from this
                new_rating[diff_rank] = -1
                continue

            expected_acc = get_expected_acc_curve(
                skill_rating, diff_level, acc_curve_cutoff, acc_curve_bias, acc_curve_low_bias, allow_pfc
            )
            expected_rating = custom_rating_calculator.get_custom_rating_from_play(
                diff_level, expected_acc, False, expected_acc < expected_fail_threshold
            )
            new_rating[diff_rank] = expected_rating

        rated_songs[f"{SONG_PREFIX}{song["name"]}"] = new_rating

    return rated_songs


def get_target_rating(world: UNBEATABLEArcadeWorld) -> float:
    diff_count = get_diff_count(world.options)

    sorted_scores = [];
    for song in world.included_songs:
        rated_song = world.rated_songs[f"{SONG_PREFIX}{song["name"]}"]
        for i in range(0, diff_count):
            rank = i + world.options.min_difficulty
            key = difficulty_key_from_rank(rank)
            if song[key] < 0:
                continue

            score_rating = rated_song[rank]
            bisect.insort(sorted_scores, score_rating)

    target_rating = 0
    score_idx = 0
    for rating in reversed(sorted_scores):
        target_rating += custom_rating_calculator.get_score_contribution(rating, score_idx)
        score_idx += 1

    return target_rating * world.options.completion_percent / 100


def set_state_dirty(state: CollectionState, player: int) -> None:
    state.unbeatable_is_dirty[player] = True


def get_max_rating(state: CollectionState, player: int) -> float:
    if not state.unbeatable_is_dirty[player]:
        return state.unbeatable_max_rating[player]

    scores = state.unbeatable_sorted_scores[player]

    max_rating = 0
    score_idx = 0
    for entry in reversed(scores):
        score_rating = entry["rating"]

        max_rating += custom_rating_calculator.get_score_contribution(score_rating, score_idx)
        score_idx += 1

    state.unbeatable_max_rating[player] = max_rating
    state.unbeatable_is_dirty[player] = False

    return max_rating


def add_song(state: CollectionState, player: int, rated_songs: dict[str, dict[int, float]], song_name: str) -> None:
    # Insert all the difficulties added by the song
    unlocked_rank = state.count(song_name, player) - 1

    rated_song = rated_songs[song_name]

    rating = 0
    found_count = 0
    for rank in rated_song.keys():
        if rated_song[rank] < 0:
            # This difficulty doesn't exist
            continue

        if found_count >= unlocked_rank:
            # This is the rank we just unlocked
            rating = rated_song[rank]
            break

        found_count += 1

    # Add this difficulty to our unlocked scores, in ascending order
    # This format makes it easiest to calculate our max rating
    new_entry = {
        "name": song_name,
        "rank": unlocked_rank,
        "rating": rating
    }
    bisect.insort(state.unbeatable_sorted_scores[player], new_entry, key=lambda x: x["rating"])

    set_state_dirty(state, player)


def remove_song(state: CollectionState, player: int, song_name: str) -> None:
    removed_rank = state.count(song_name, player)

    to_remove = None
    for entry in state.unbeatable_sorted_scores[player]:
        if entry["name"] == song_name and entry["rank"] == removed_rank:
            to_remove = entry
            break

    if to_remove:
        # Remove the entry while we aren't traversing the target list
        state.unbeatable_sorted_scores[player].remove(to_remove)

    set_state_dirty(state, player)