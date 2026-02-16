from collections.abc import Mapping
from typing import Any

from BaseClasses import CollectionState, Item, ItemClassification, Region
from Options import OptionError
from worlds.AutoWorld import World

from . import songs, items, locations, rules, web_world
from .game_info import GAME_NAME, VERSION, COMPATIBLE_VERSIONS
from .options import UNBEATABLEArcadeOptions
from .ratings import ratings_logic

class UNBEATABLEArcadeWorld(World):
    """
    UNBEATABLE is a rhythm game where music is illegal and you do crimes.
    UNBEATABLE Arcade Mode is a game mode separate from the story mode, where you can play songs from the game (and other places) to your heart's content.
    """

    game = GAME_NAME

    web = web_world.UNBEATABLEArcadeWebWorld()

    options_dataclass = UNBEATABLEArcadeOptions
    options: UNBEATABLEArcadeOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID

    item_name_to_id = items.ITEM_NAME_TO_ID
    item_name_groups = items.ITEM_NAME_GROUPS

    origin_region_name = "Arcade"

    included_songs: list
    item_count: int
    rated_songs: dict[str, dict[int, float]]
    target_rating: float


    def generate_early(self) -> None:
        if self.options.min_difficulty > self.options.max_difficulty:
            # Likely due to randomized settings, swap them so max > min
            print(f"{self.game} - {self.player_name} | Minimum difficulty is higher than maximum difficulty! Swapping.\n    (If you randomized min/max difficulty, you can ignore this)")
            swap = self.options.min_difficulty
            self.options.min_difficulty = self.options.max_difficulty
            self.options.max_difficulty = swap

        # Only activate non-local traps if there's another multiworld to send them to
        # if self.options.non_local_traps and len(self.multiworld.worlds) > 1:
            # The shorthand option for adding all traps to non_local_items
            # items.add_traps_non_local(self)

        # Since this is the first stage of generation, add our included songs here
        self.included_songs = songs.get_included_songs(self.options.use_breakout)
        self.item_count = items.get_item_count(self)

        # Precalculate the expected rating gains per-map
        # This is stored as a dictionary indexed by song item names,
        # then a list of ratings indexed by difficulty rank
        self.rated_songs = ratings_logic.get_songs_with_ratings(songs.all_songs, self.options)
        self.target_rating = ratings_logic.get_target_rating(self)
        if self.target_rating < 0.001:
            raise(OptionError(f"{self.game} - {self.player_name} | Target rating is zero! Try increasing skill rating, reducing difficulty, and/or increasing completion percentage."))


    def create_regions(self) -> None:
        # Only a single region for this world
        self.multiworld.regions += [Region(self.origin_region_name, self.player, self.multiworld)]
        locations.create_all_locations(self)


    def set_rules(self) -> None:
        rules.set_all_rules(self)
    

    def create_items(self) -> None:
        items.create_all_items(self)
    

    def create_item(self, name: str) -> items.UNBEATABLEArcadeItem:
        return items.create_item_with_classification(self, name)


    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)


    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = self.options.as_dict(
            "use_breakout",
            "max_difficulty",
            "min_difficulty",
            
            "allow_pfc",
            "acc_curve_bias",
            "acc_curve_low_bias",
            "acc_curve_cutoff"
        )

        slot_data["skill_rating"] = float(self.options.skill_rating) / 1000

        slot_data["item_count"] = self.item_count
        slot_data["target_rating"] = self.target_rating

        slot_data["version"] = VERSION
        slot_data["compatible_versions"] = COMPATIBLE_VERSIONS

        return slot_data
    

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)

        if change and item.name in self.item_name_groups["songs"]:
            # start_rating = ratings_logic.get_max_rating(state, self.player)
            # print(f"Added: {item.name}")
            ratings_logic.add_song(state, self.player, self.rated_songs, item.name)
            # end_rating = ratings_logic.get_max_rating(state, self.player)
            # print(f"New max rating: {end_rating} ({end_rating - start_rating})")
        
        return change
    

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)

        if change and item.name in self.item_name_groups["songs"]:
            ratings_logic.remove_song(state, self.player, item.name)
        
        return change