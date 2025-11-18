import math
from typing import Dict

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import RefunctItem, item_table
from .Locations import location_table, RefunctLocation, starting_platform, finish_platform, platforms_with_button_on_them, number_platforms_per_cluster
from .Options import RefunctOptions
from .Rules import set_refunct_rules, set_refunct_completion


class RefunctWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Refunct.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks"],
        )
    ]


class RefunctWorld(World):
    """
    Refunct is a first-person platformer focused on movement and momentum.
    """

    game: str = "Refunct"
    options_dataclass = RefunctOptions

    web = RefunctWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in location_table.items()}

    ap_world_version = "0.0.1"        
        
    def get_filler_item_name(self) -> str:
        return ":)"

    def create_items(self):        
        for name in item_table:
            if "Trigger" in name:
                self.multiworld.itempool.append(self.create_item(name))
        for _ in range(176):
            self.multiworld.itempool.append(self.create_item("Grass"))

    def create_regions(self):
        # simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)
        
        board.locations = [
            RefunctLocation(self.player, loc_name, loc_data.id, board, loc_data.button_nr)
            for loc_name, loc_data in location_table.items()
            if loc_data.region == board.name and "Button" not in loc_name 
        ]
                
        victory_location_name = f"Platform {finish_platform[0]}-{finish_platform[1]}"
        # self.get_location(victory_location_name).address = None
        self.get_location(victory_location_name).place_locked_item(
            self.create_item("Victory Location")
        )
        
        self.get_location(f"Platform {starting_platform[0]}-{starting_platform[1]}").place_locked_item(
            self.create_item(":)")
        ) # this location is really annoying

        for button, platform in platforms_with_button_on_them:
            self.get_location(f"Platform {button}-{platform}").address = None # never let people go to these platforms to avoid buttons
            self.get_location(f"Platform {button}-{platform}").place_locked_item(
                self.create_item(":)")
            )


        # add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]
        

    def set_rules(self):
        """
        set rules per location, and add the rule for beating the game
        """
            
        set_refunct_rules(self.multiworld, self.player)
        set_refunct_completion(self.multiworld, self.player)

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = RefunctItem(name, item_data.classification, item_data.code, self.player)
        return item
    