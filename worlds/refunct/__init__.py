
import pkgutil
from typing import Any, Dict, List, Union

import orjson

from BaseClasses import Item, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import RefunctItem, item_table
from .Locations import location_table, RefunctLocation, starting_platform, platforms_with_button_on_them, number_buttons_per_cluster, platforms_without_button_ids
from .Options import RefunctOptions, FinalPlatform


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
    
    origin_region_name = "10010102"  # Platform 1-2

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in location_table.items()}

    ap_world_version = "0.3.2"        
        
    def get_filler_item_name(self) -> str:
        return ":)"

    def create_items(self):        
        for name in item_table:
            if "Trigger" in name and name != "Trigger Cluster 1":
                self.multiworld.itempool.append(self.create_item(name))
        self.multiworld.itempool.append(self.create_item("Ledge Grab"))
        self.multiworld.itempool.append(self.create_item("Progressive Wall Jump"))
        self.multiworld.itempool.append(self.create_item("Progressive Wall Jump"))
        self.multiworld.itempool.append(self.create_item("Jumppads"))
        self.multiworld.itempool.append(self.create_item("Swim"))
        
        self.multiworld.push_precollected(self.create_item("Trigger Cluster 1"))
        
        for _ in range(174):  # -2 for Victory Location and :)
            self.multiworld.itempool.append(self.create_item("Grass"))
        # for _ in range(74):  # -2 for Victory Location and :)
        #     self.multiworld.itempool.append(self.create_item("Flower"))
            
        if "Vanilla Minigame" in self.options.minigames.value:
            self.multiworld.itempool.append(self.create_item("Unlock Vanilla Minigame"))
            for _ in range(9):
                self.multiworld.itempool.append(self.create_item("Flower"))
                
        if "Seeker Minigame" in self.options.minigames.value:
            self.multiworld.itempool.append(self.create_item("Unlock Seeker Minigame"))
            for _ in range(9):
                self.multiworld.itempool.append(self.create_item("Flower"))
                
        early_items = [
            "Trigger Cluster 2",
            "Trigger Cluster 4",
            "Trigger Cluster 6",
            "Trigger Cluster 8",
        ]
        early_item_name = self.multiworld.random.choice(early_items)
        self.multiworld.local_early_items[self.player][early_item_name] = 1
        

    def create_regions(self):
        regions = []
        
        def load_json_data_dict(data_name: str) -> Union[List[Any], Dict[str, Any]]:
            return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))

        clusters: Dict[int, Any] = load_json_data_dict("clusters.json")
        
        for key in clusters:
            regions.append(Region(f"{key}", self.player, self.multiworld))

        # We now need to add these regions to multiworld.regions so that AP knows about their existence.
        self.multiworld.regions += regions
        
        for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.type_of_check == "Platform"]:
            region = None
            for cluster_key, node_list in clusters.items():
                if loc_data.id in node_list:
                    region = cluster_key
                    break
            if region is None:
                raise Exception(f"Could not find region for location {loc_name} with id {loc_data.id}")
            region_object = self.multiworld.get_region(f"{region}", self.player)
            region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
            
        if "Vanilla Minigame" in self.options.minigames.value:
            self.multiworld.regions.append(Region("Vanilla Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Vanilla"]:
                region_object = self.multiworld.get_region("Vanilla Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        if "Seeker Minigame" in self.options.minigames.value:
            self.multiworld.regions.append(Region("Seeker Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Seeker"]:
                region_object = self.multiworld.get_region("Seeker Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
            
        seeker_pressed_platforms = platforms_without_button_ids.copy()
        self.seeker_pressed_platforms = self.multiworld.random.sample(seeker_pressed_platforms, len(seeker_pressed_platforms) - 10)
        
        
    def set_rules(self):
        def load_json_data_list_of_lists(data_name: str) -> List[List[Any]]:
            return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))    
        
        connections_vanilla = load_json_data_list_of_lists("connections_vanilla.json")
        connections_swim = load_json_data_list_of_lists("connections_swim.json")
        connections_ledge_grab = load_json_data_list_of_lists("connections_ledge_grab.json")
        connections_jumppad = load_json_data_list_of_lists("connections_jumppad.json")
        connections_one_wall_jump = load_json_data_list_of_lists("connections_one_wall_jump.json")
        connections_inf_wall_jump = load_json_data_list_of_lists("connections_inf_wall_jump.json")
        
        logic_info = [
            (connections_vanilla, None, None),
            (connections_swim, "Swim", 1),
            (connections_ledge_grab, "Ledge Grab", 1),
            (connections_jumppad, "Jumppads", 1),
            (connections_one_wall_jump, "Progressive Wall Jump", 1),
            (connections_inf_wall_jump, "Progressive Wall Jump", 2),
        ]
        
        for logics in logic_info:
            connections, item_name, item_count = logics
            for [a,b] in connections:
                c1 = (a - 10010000) // 100
                c2 = (b - 10010000) // 100
                region_a = self.multiworld.get_region(f"{a}", self.player)
                region_b = self.multiworld.get_region(f"{b}", self.player)
                if item_name is None:
                    region_a.connect(region_b, f"{a} to {b}", 
                        lambda state, c1=c1, c2=c2: 
                            all([
                                state.has(f"Trigger Cluster {c1}", self.player), 
                                state.has(f"Trigger Cluster {c2}", self.player)
                            ]))
                else:
                    region_a.connect(region_b, f"{a} to {b} ({item_name})", 
                        lambda state, c1=c1, c2=c2, item_name=item_name, item_count=item_count: 
                            all([
                                state.has(f"Trigger Cluster {c1}", self.player),
                                state.has(f"Trigger Cluster {c2}", self.player),
                                state.has(item_name, self.player, item_count)
                            ]))
                    
        possible_final_platforms = [i for i,j in location_table.items() if j.type_of_check == "Platform"]
        
        location_names = [i.name for i in self.multiworld.get_locations(self.player)]
        for button, platform in platforms_with_button_on_them:  # put a :) on every button platform
            loc_name = f"Platform {button}-{platform}"
            if loc_name in location_names:
                self.get_location(loc_name).address = None # never let people go to these platforms to avoid buttons
                self.get_location(loc_name).place_locked_item(
                    self.create_item(":)")
                )
                possible_final_platforms.remove(loc_name)
                    
        self.finish_platform = None
        if self.options.final_platform.value == FinalPlatform.option_1_5:
            self.finish_platform = (1,5)
        elif self.options.final_platform.value == FinalPlatform.option_21_1:
            self.finish_platform = (21,1)
        elif self.options.final_platform.value == FinalPlatform.option_29_2:
            self.finish_platform = (29,2)
        else:  # random
            valid_candidates = possible_final_platforms
            finish_platform_name = self.multiworld.random.choice(valid_candidates)
            self.finish_platform = (int(finish_platform_name.split(" ")[1].split("-")[0]), int(finish_platform_name.split(" ")[1].split("-")[1]))
                
        victory_location_name = f"Platform {self.finish_platform[0]}-{self.finish_platform[1]}"
        # self.get_location(victory_location_name).address = None
        self.get_location(victory_location_name).place_locked_item(
            self.create_item("Final Platform")
        )
        
        if "Vanilla Minigame" in self.options.minigames.value:
            location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Vanilla Minigame" in i.name]
            location_names_el = self.multiworld.random.sample(location_names, 27)
            for loc in location_names_el:
                self.get_location(loc).place_locked_item(
                    self.create_item("Flower")
                )
        
        
        self.multiworld.completion_condition[self.player] = lambda state: all([state.has("Final Platform", self.player), state.has("Grass", self.player, self.options.required_grass.value)])
        
        if "Vanilla Minigame" in self.options.minigames.value:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Vanilla Minigame", self.player)
            region_a.connect(region_b, f"Enter Vanilla Minigame", 
                lambda state: state.has("Unlock Vanilla Minigame", self.player))
            
        if "Seeker Minigame" in self.options.minigames.value:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Seeker Minigame", self.player)
            region_a.connect(region_b, f"Enter Seeker Minigame", 
                lambda state: state.has("Unlock Seeker Minigame", self.player))
        

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = RefunctItem(name, item_data.classification, item_data.code, self.player)
        return item
    
    def fill_slot_data(self):
        """
        make slot data, which consists of refunct_data, options, and some other variables.
        """
        slot_data = self.options.as_dict(
            "required_grass",
        )
        slot_data["finish_platform_c"] = self.finish_platform[0]
        slot_data["finish_platform_p"] = self.finish_platform[1]
        
        if "Seeker Minigame" in self.options.minigames.value:
            slot_data["seeker_pressed_platforms"] = self.seeker_pressed_platforms
        
        slot_data["ap_world_version"] = self.ap_world_version
        slot_data["final_platform_known"] = self.options.final_platform.value != FinalPlatform.option_random_unknown

        return slot_data