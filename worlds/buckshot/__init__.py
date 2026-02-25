from typing import Any, Callable, Mapping

from BaseClasses import CollectionState, Item, ItemClassification as IC, Location, Tutorial
from Fill import fill_restrictive
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from .Enums import *
from .Items import BuckshotRouletteItem, item_id_table, item_table
from .Locations import BuckshotRouletteLocation, LocationData, location_id_table, location_table
from .Options import BuckshotRouletteOptions, option_groups
from .Regions import BuckshotRouletteRegion, region_table
from .Rules import consumable_rule, specific_consumables_rule, full_house_rule, don_access_rule

import logging
logger = logging.getLogger("BUCKSHOT")

class BuckshotWebWorld(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to playing Buckshot Roulette",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["asdfwyay"]
    )

    tutorials = [setup_en]

class BuckshotWorld(World):
    """A Computer Game by Mike Klubnika"""
    
    game = "Buckshot Roulette"
    web = BuckshotWebWorld()
    options: BuckshotRouletteOptions
    options_dataclass = BuckshotRouletteOptions
    location_name_to_id = location_id_table
    item_name_to_id = item_id_table

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.included_locations = dict[str, LocationData]()
        self.filler_items = [
            item_name
            for item_name, item_data in item_table.items()
            if item_data.classification == IC.filler
        ]
        self.pre_fill_pool = []

    def create_item(self, item_name: str) -> BuckshotRouletteItem:
        return BuckshotRouletteItem(item_name, item_table[item_name].classification, item_table[item_name].id, self.player)
    
    def create_event(self, event_name: str, id: int | None) -> BuckshotRouletteItem:
        return BuckshotRouletteItem(event_name, IC.progression, id, self.player)
    
    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_items)

    def get_location_subset(self, flags: int, combine="or") -> list[Location]:
        if combine == "or":
            return [
                self.get_location(location_name)
                for location_name, location_data in self.included_locations.items()
                if location_data.flags & flags
            ]
        else:
            return [
                self.get_location(location_name)
                for location_name, location_data in self.included_locations.items()
                if (location_data.flags & flags) == flags
            ]

    def create_items(self) -> None:
        # Setup Item Pool
        included_item_flags: int = I_CONSUMABLE
        total_locations: int = len(self.multiworld.get_unfilled_locations(self.player))

        if self.options.goal != "70k":
            included_item_flags |= I_DOUBLE_OR_NOTHING
        if self.options.double_or_nothing_requirements in ["pills", "vanilla_plus"]:
            included_item_flags |= I_PILLS

        # Add Progression Items
        item_pool: list[BuckshotRouletteItem] = [
            self.create_item(item_name)
            for item_name, item_data in item_table.items()
            if (
                not item_data.flags
                or item_data.flags & included_item_flags == item_data.flags
            ) and item_data.classification == IC.progression
        ]

        if (
            self.options.goal == "70k"
            and not self.options.achievements
            and self.options.shotsanity == "off"
        ):
            item_pool.pop(self.random.randrange(len(item_pool)))
        elif (
            self.options.consumable_item_logic == "tight"
            and self.options.goal != "70k"
            and not self.options.achievements
            and self.options.shotsanity == "off"
        ):
            base_game_consumable_item_names = [
                item_name
                for item_name, item_data in item_table.items()
                if item_data.flags == I_CONSUMABLE
            ]
            self.pre_fill_pool = self.multiworld.random.sample(
                [
                    item
                    for item in item_pool
                    if item.name in base_game_consumable_item_names
                ],
                3
            )
            item_pool = [item for item in item_pool if item not in self.pre_fill_pool]

        # Add Useful Items
        pre_fill_count = len(self.pre_fill_pool)
        if "Item Luck" in self.options.included_custom_mechanics.value:
            for _ in range(min(
                3,
                total_locations - len(item_pool) - 1 - pre_fill_count
            )):
                item_pool.append(self.create_item("Progressive Item Luck"))
        if "Life Bank" in self.options.included_custom_mechanics.value:
            for _ in range(min(
                1 + len(self.get_location_subset(L_DON_ROUND))//6,
                total_locations - len(item_pool) - 1 - pre_fill_count
            )):
                item_pool.append(self.create_item("Life Bank Charge"))

        # Add Traps
        if self.options.included_traps.value:
            num_traps = (total_locations - len(item_pool) - 1 - pre_fill_count)*self.options.trap_fill_percentage.value//100
            for _ in range(num_traps):
                item_pool.append(
                    self.create_item(self.random.choice(list(self.options.included_traps.value)))
                )

        # Add Filler Items
        item_pool += [self.create_filler() for _ in range(total_locations - len(item_pool) - 1 - pre_fill_count)]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Setup Locations
        included_location_flags: int = 0x00
        custom_goal_don_locations = 6*(1 + int_log2((self.options.custom_goal_amount - 1)//35000))

        if self.options.achievements:
            included_location_flags |= L_ACHIEVEMENT
        if not self.options.exclude_full_house:
            included_location_flags |= L_FULL_HOUSE
        if self.options.goal != "70k":
            included_location_flags |= L_DOUBLE_OR_NOTHING | L_DON_ROUND
        if self.options.goal != "70k" and (self.options.custom_goal_amount > 70000 if self.options.goal == "custom" else True):
            included_location_flags |= L_140K
        if self.options.goal == "1000k" or (self.options.goal == "custom" and self.options.custom_goal_amount >= 1000000):
            included_location_flags |= L_LARGE_GOAL
        if self.options.shotsanity != "off":
            included_location_flags |= L_SHOTSANITY
        if self.options.goal in ["1000k", "custom"]:
            included_location_flags |= L_CASH_OUT

        # Filter locations based on flags, goal, & shotsanity settings
        self.included_locations = {
            location_name: location_data
            for location_name, location_data in location_table.items()
            if (
                location_data.flags & included_location_flags == location_data.flags
                and (
                    (
                        self.options.goal == "140k" and location_data.id - L_OFST_DON <= 12
                        or self.options.goal == "1000k" and location_data.id - L_OFST_DON <= 30
                        or self.options.goal == "custom" and location_data.id - L_OFST_DON <= custom_goal_don_locations
                    )
                    if location_data.flags & L_DON_ROUND else True
                )
                and (
                    location_data.id - L_OFST_SS <= self.options.shotsanity_count
                    if location_data.flags & L_SHOTSANITY else True
                )
            )
        }

        # Create region graph and add locations
        for region_name, region_data in region_table.items():
            region = BuckshotRouletteRegion(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

            region_filtered_locations: dict[str, int] = {
                location_name: location_data.id
                for location_name, location_data in self.included_locations.items()
                if location_data.region == region_name
            }

            region.add_locations(region_filtered_locations, BuckshotRouletteLocation)

        for region_name, region_data in region_table.items():
            region = self.get_region(region_name)
            region.add_exits(region_data.connecting_regions)

    def set_rules(self) -> None:
        # Double or Nothing Access
        if self.options.goal != "70k":
            don_access: Callable[[CollectionState], bool] = None
            if self.options.double_or_nothing_requirements == "free":
                don_access = don_access_rule(self, [])
            elif self.options.double_or_nothing_requirements == "vanilla":
                don_access = don_access_rule(self, [], "Win Final Round")
            elif self.options.double_or_nothing_requirements == "pills":
                don_access = don_access_rule(self, ["Double or Nothing Pills"])
            elif self.options.double_or_nothing_requirements == "vanilla_plus":
                don_access = don_access_rule(self, ["Double or Nothing Pills"], "Win Final Round")

            for location in self.get_location_subset(L_DOUBLE_OR_NOTHING):
                add_rule(location, don_access)

        # Consumable Item Logic
        if self.options.consumable_item_logic != "none":
            consumable_item_counts: tuple[int] = (0, 0, float('inf'))
            if self.options.consumable_item_logic == "tight":
                consumable_item_counts = (2, 3, 1)
            if self.options.consumable_item_logic == "normal":
                consumable_item_counts = (1, 2, 3)
            if self.options.consumable_item_logic == "minimal":
                consumable_item_counts = (0, 0, 3)

            add_rule(
                self.get_location("Win Second Round - Item 1"),
                consumable_rule(self, consumable_item_counts[0], True)
            )
            add_rule(
                self.get_location("Win Second Round - Item 2"),
                consumable_rule(self, consumable_item_counts[0], True)
            )
            add_rule(
                self.get_location("Win Final Round"),
                consumable_rule(self, consumable_item_counts[1], True)
            )      

            for location in self.get_location_subset(L_DON_ROUND):
                min_cons = (((location.address - L_OFST_DON - 1) >> 1)//consumable_item_counts[2]) + consumable_item_counts[1] + 1
                add_rule(
                    location,
                    consumable_rule(self, min(min_cons, 9), False)
                )

            # Shotsanity Logic
            for location in self.get_location_subset(L_SHOTSANITY):
                if self.options.shotsanity != "balanced":
                    continue

                shotsanity_group = (location.address - L_OFST_SS - 1)//self.options.balanced_shotsanity_count_per_round
                
                if shotsanity_group == 2:
                    add_rule(
                        location,
                        consumable_rule(self, consumable_item_counts[0], True)
                    )
                elif shotsanity_group == 3:
                    add_rule(
                        location,
                        consumable_rule(self, consumable_item_counts[1], True)
                    )
                elif shotsanity_group >= 4:
                    min_cons = consumable_item_counts[1]
                    if self.options.goal != "70k":
                        min_cons += (shotsanity_group - 3)//consumable_item_counts[2] + 1
                        
                    add_rule(
                        location,
                        consumable_rule(self, min(min_cons, 9), False)
                    )

        # Achievement Rules
        if self.options.achievements:
            if self.options.consumable_item_logic != "none":
                add_rule(
                    self.get_location("Bronze Gates"),
                    consumable_rule(self, consumable_item_counts[0], True)
                )
                add_rule(
                    self.get_location("70K"),
                    consumable_rule(self, consumable_item_counts[1], True)
                )

            add_rule(
                self.get_location("Why?"),
                lambda state: specific_consumables_rule(self, ["Magnifying Glass"])(state) or 
                              specific_consumables_rule(self, ["Adrenaline"])(state) and
                              don_access(state)
            )
            add_rule(
                self.get_location("Going Out With Style!"),
                lambda state: specific_consumables_rule(self, ["Hand Saw"])(state) or 
                              specific_consumables_rule(self, ["Adrenaline"])(state) and
                              don_access(state)
            )
            
            if self.options.goal != "70k":
                add_rule(
                    self.get_location("Digita, Orava and Koni"),
                    specific_consumables_rule(self, ["Cigarette Pack", "Beer", "Expired Medicine"])
                )
                add_rule(
                    self.get_location("Nope!"),
                    lambda state: state.can_reach_location("Double or Nothing - Win 3 Rounds - Item 1", self.player)
                )

            if self.options.goal != "70k" and (self.options.custom_goal_amount > 70000 if self.options.goal == "custom" else True):
                add_rule(
                    self.get_location("140K"),
                    lambda state: state.can_reach_location("Double or Nothing - Win 6 Rounds - Item 1", self.player)
                )
            
            if self.options.goal == "1000k" or (self.options.goal == "custom" and self.options.custom_goal_amount >= 1000000):
                add_rule(
                    self.get_location("1000K"),
                    lambda state: state.can_reach_location("Double or Nothing - Win 15 Rounds - Item 1", self.player)
                )
                add_rule(
                    self.get_location("Know When To Quit"),
                    lambda state: state.can_reach_location("Double or Nothing - Win 15 Rounds - Item 1", self.player)
                )
            
            if self.options.goal != "70k" and not self.options.exclude_full_house:
                add_rule(
                    self.get_location("Full House"),
                    full_house_rule(self)
                )

            if self.options.goal == "1000k":
                add_rule(
                    self.get_location("Cash Out"),
                    lambda state: state.can_reach_location("1000K", self.player)
                )
            elif self.options.goal == "custom":
                max_don_round = 3*(1 + int_log2((self.options.custom_goal_amount - 1)//35000))
                add_rule(
                    self.get_location("Cash Out"),
                    lambda state: state.can_reach_location(f"Double or Nothing - Win {max_don_round} Rounds - Item 1", self.player)
                )

        # Completion Condition
        if self.options.goal == "70k":
            goal_location = "Win Final Round"
        elif self.options.goal == "140k":
            goal_location = "Double or Nothing - Win 6 Rounds - Item 1"
        else:
            goal_location = "Cash Out"

        self.multiworld.get_location(goal_location, self.player).place_locked_item(self.create_event("WINNER", 26))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("WINNER", self.player)

    def generate_early(self) -> None:
        '''
        if all([
            self.multiworld.players == 1,
            self.options.consumable_item_logic == "tight",
            self.options.goal != "70k",
            self.options.shotsanity == "off",
            not self.options.achievements
        ]):
            raise OptionError("Single-player worlds with 'tight' consumable item logic "
                              "must have one of the following options set:\n"
                              "- goal = '70k'\n"
                              "- shotsanity = 'balanced' or 'unreasonable'\n"
                              "- achievements = 'true'")
        '''
        pass

    def pre_fill(self) -> None:
        if (
            self.options.consumable_item_logic == "tight"
            and self.options.goal != "70k"
            and not self.options.achievements
            and self.options.shotsanity == "off"
        ):
            item_locations = [
                self.get_location(location_name)
                for location_name, location_data in location_table.items()
                if location_data.id <= 3
            ]
            state = CollectionState(self.multiworld)
            state.sweep_for_advancements(item_locations)
            fill_restrictive(self.multiworld, state, item_locations, self.pre_fill_pool, single_player_placement=True, lock=True)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "goal": self.options.goal.value,
            "custom_goal_amount": self.options.custom_goal_amount.value,
            "double_or_nothing_requirements": self.options.double_or_nothing_requirements.value
        }

def int_log2(x: int) -> int:
    count = 0
    while x > 1:
        x >>= 1
        count += 1
    return count