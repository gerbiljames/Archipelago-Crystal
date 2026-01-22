
import pkgutil
from typing import Any, Dict, List, Union

import orjson

from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import RefunctItem, item_table
from .Locations import location_table, RefunctLocation, starting_platform, platforms_with_button_on_them, number_buttons_per_cluster, platforms_without_button_ids
from .Options import RefunctOptions, FinalPlatform, Traps, Cubes, refunct_option_groups


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
    option_groups = refunct_option_groups

    web = RefunctWeb()
    
    origin_region_name = "10010102"  # Platform 1-2

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in location_table.items()}

    ap_world_version = "0.6.1"        
        
    def get_filler_item_name(self) -> str:
        return ":)"

    def create_items(self):
        items_to_add = []
        for name in item_table:
            if "Trigger" in name and name != "Trigger Cluster 1":
                items_to_add.append(name)
        items_to_add.append("Ledge Grab")
        items_to_add.append("Progressive Wall Jump")
        items_to_add.append("Progressive Wall Jump")
        items_to_add.append("Jump Pads")
        items_to_add.append("Swim")
        items_to_add.append("Pipes")
        items_to_add.append("Lifts")
            
        self.multiworld.push_precollected(self.create_item("Trigger Cluster 1"))
        
        self.amount_of_grass = self.options.amount_of_grass.value
        self.required_grass = (self.options.required_grass_percentage.value * self.amount_of_grass) // 100
        for _ in range(self.required_grass):
            items_to_add.append("Grass")
        for _ in range(self.amount_of_grass - self.required_grass):
            items_to_add.append(["Grass", True])
        for _ in range(173 - self.amount_of_grass):
            items_to_add.append("Flower")
            
        if self.options.cubes == Cubes.option_always:
            for _ in range(18):
                items_to_add.append("Flower")
        # if self.options.cubes == Cubes.option_cubes_bag:
        #     items_to_add.append("Cubes Bag")
        #     for _ in range(17):
        #         items_to_add.append("Flower")
        
        num_unlocks = self.options.number_of_unlocks_per_minigame.value
        if "Vanilla Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("Unlock Vanilla Minigame")
            for _ in range(37 - num_unlocks):
                items_to_add.append("Flower")
                
        if "Seeker Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("Unlock Seeker Minigame")
            for _ in range(10 - num_unlocks):
                items_to_add.append("Flower")
                
        if "Button Galore Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("Unlock Button Galore Minigame")
            for _ in range(37 - num_unlocks):
                items_to_add.append("Flower")
        
        if "OG Randomizer Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("Unlock OG Randomizer Minigame")
            for _ in range(37 - num_unlocks):
                items_to_add.append("Flower")
                
                
        if self.options.nerf_minigame_checks.value:
            if "Vanilla Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Vanilla Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 27)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            # Seeker Minigame doesn't need locked flowers.
            if "Button Galore Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Button Galore Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 27)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            if "OG Randomizer Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "OG Randomizer Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 27)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
        
        trap_items = []
        if self.options.traps == Traps.option_pretty or self.options.traps == Traps.option_all:
            trap_items = [
                "Dark skies",
                "No skylight",
                # "Disco sky",
                "Starry sky",
                "Red sky",
                "Hurricane",
            ] * 2
        if self.options.traps == Traps.option_all:
            trap_items += [
                "Slo-mo",
                "Fast-mo",
                "Blurrrrgh",
            ] * 2
        
        if trap_items:
            self.multiworld.random.shuffle(trap_items)
            for item in trap_items:
                if "Flower" in items_to_add:
                    items_to_add.remove("Flower")
                    items_to_add.append(item)
                    
        for item in items_to_add:
            if isinstance(item, list) and item[1] == True:
                self.multiworld.itempool.append(self.create_item(item[0], force_useful=True))
            else:
                self.multiworld.itempool.append(self.create_item(item))
        

    def create_regions(self):       
        self.minigames = []
        minigames_weights = self.options.minigames_likeliness.value
        population = list(minigames_weights.keys())
        weights = list(minigames_weights.values())
        num_minigames = self.options.number_of_minigames.value
        if num_minigames == -1:
            num_minigames = len([w for w in weights if w > 0])
        
        k = min(num_minigames, len([w for w in weights if w > 0]))
        self.minigames = []
        for _ in range(k):
            choice = self.multiworld.random.choices(population=population, weights=weights, k=1)[0]
            idx = population.index(choice)
            self.minigames.append(choice)
            population.pop(idx)
            weights.pop(idx)
            
        
        regions = []
        
        def load_json_data_dict(data_name: str) -> Union[List[Any], Dict[str, Any]]:
            return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))

        clusters: Dict[int, Any] = load_json_data_dict("clusters.json")
        
        for key in clusters:
            regions.append(Region(f"{key}", self.player, self.multiworld))

        # We now need to add these regions to multiworld.regions so that AP knows about their existence.
        self.multiworld.regions += regions
        
        add_cubes = self.options.cubes != Cubes.option_never
        for loc_name, loc_data in [(a, b) for a, b in location_table.items()]:
            if loc_data.type_of_check == "Platform" or (add_cubes and loc_data.type_of_check == "Cube"):
                region = None
                for cluster_key, node_list in clusters.items():
                    if loc_data.id in node_list:
                        region = cluster_key
                        break
                if region is None:
                    raise Exception(f"Could not find region for location {loc_name} with id {loc_data.id}")
                region_object = self.multiworld.get_region(f"{region}", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
            
        if "Vanilla Minigame" in self.minigames:
            self.multiworld.regions.append(Region("Vanilla Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Vanilla"]:
                region_object = self.multiworld.get_region("Vanilla Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        if "Seeker Minigame" in self.minigames:
            self.multiworld.regions.append(Region("Seeker Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Seeker"]:
                region_object = self.multiworld.get_region("Seeker Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        if "Button Galore Minigame" in self.minigames:
            self.multiworld.regions.append(Region("Button Galore Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Button Galore"]:
                region_object = self.multiworld.get_region("Button Galore Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
        
        if "OG Randomizer Minigame" in self.minigames:
            self.multiworld.regions.append(Region("OG Randomizer Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "OG Randomizer"]:
                region_object = self.multiworld.get_region("OG Randomizer Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        
        
        # Seeker Minigame info
        seeker_pressed_platforms = platforms_without_button_ids.copy()
        self.seeker_pressed_platforms = self.multiworld.random.sample(seeker_pressed_platforms, len(seeker_pressed_platforms) - 10)
        
        # OG Randomizer Minigame info
        self.set_og_randomizer_order()
    
    def set_og_randomizer_order(self):
        # OG Randomizer Minigame info
        dependences = {}
        dependences[13] = [3, 11, 14, 15, # 23, 
                           24, 27]
        dependences[16] = [2, 17, 28]
        dependences[18] = [8]
        dependences[22] = [3, 11, 12, 20, 30]
        
        somewhat_close = {
            1: [2,4,6,10,3],
            2: [1,4,16,17,15,3],
            3: [23,22,12,11,10,1,2,15,13],
            4: [1,2,16,28,5,18,6],
            5: [16,28,18,6,4],
            6: [1,10,4,5,18,7,8,9],
            7: [6,18,8],
            8: [10,9,6,7,18],
            9: [19,11,10,6,8],
            10: [11,3,1,6,8,9,19],
            11: [12,3,1,1,9,19,21,20,30],
            12: [22,23,3,11,20,30],
            13: [24,27,14,15,3,23,11],
            14: [13,15,17,27,24],
            15: [13,14,17,16,2,3],
            16: [17,15,2,1,4,5,38],
            17: [27,14,15,2,16,28],
            18: [4,5,6,7,8],
            19: [21,20,11,10,9],
            20: [30,12,11,21],
            21: [19,20,11],
            22: [30,23,12],
            23: [22,13,12,3,29,24],
            24: [23,22,30,29,25,26,27,14,13],
            25: [24,26,29],
            26: [29,25,24,27],
            27: [14,17,13,24,26],
            28: [17,16,4,5,18],
            29: [26,25,24,23,22,30],
            30: [20,11,12,22,23,29],
        }
        
        self.og_randomizer_order = [1]
        remaining = list(range(2, 31))
        prev_far = 0.5
        while len(remaining) > 0:
            last = self.og_randomizer_order[-1]
            possible_next = []
            close = []
            for r in remaining:
                add = False
                if r in dependences:
                    if any([d in self.og_randomizer_order for d in dependences[r]]):
                        add = True
                else:
                    add = True
                if add:
                    possible_next.append(r)
                    if r in somewhat_close[last]:
                        close.append(r)
            options_next = possible_next
            
            if close and self.multiworld.random.random() < prev_far:
                options_next = close
            next_cluster = self.multiworld.random.choice(options_next)
            
            if next_cluster in close:
                prev_far = max(0, prev_far - 0.1)
            else:
                prev_far = 1            

            self.og_randomizer_order.append(next_cluster)
            remaining.remove(next_cluster)
        self.og_randomizer_order.append(31)
        
    def set_rules(self):
        def load_json_data_list_of_lists(data_name: str) -> List[List[Any]]:
            return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))    
        
        connections_vanilla = load_json_data_list_of_lists("connections_vanilla.json")
        connections_swim = load_json_data_list_of_lists("connections_swim.json")
        connections_ledge_grab = load_json_data_list_of_lists("connections_ledge_grab.json")
        connections_jumppad = load_json_data_list_of_lists("connections_jump_pads.json")
        connections_one_wall_jump = load_json_data_list_of_lists("connections_one_wall_jump.json")
        connections_inf_wall_jump = load_json_data_list_of_lists("connections_inf_wall_jump.json")
        connections_cubes = load_json_data_list_of_lists("connections_cubes.json")
        connections_pipes = load_json_data_list_of_lists("connections_pipes.json")
        connections_lifts = load_json_data_list_of_lists("connections_lifts.json")
        
        logic_info = [
            (connections_vanilla, None, None),
            (connections_swim, "Swim", 1),
            (connections_ledge_grab, "Ledge Grab", 1),
            (connections_jumppad, "Jump Pads", 1),
            (connections_one_wall_jump, "Progressive Wall Jump", 1),
            (connections_inf_wall_jump, "Progressive Wall Jump", 2),
            (connections_pipes, "Pipes", 1),
            (connections_lifts, "Lifts", 1),
        ]
        if self.options.cubes == Cubes.option_always:
            logic_info.append((connections_cubes, None, None))
        # if self.options.cubes == Cubes.option_cubes_bag:
        #     logic_info.append((connections_cubes, "Cubes Bag", 1))
        
        for logics in logic_info:
            connections, item_name, item_count = logics
            for [a,b] in connections:
                c1 = ((a - 10010000) % 10000) // 100
                c2 = ((b - 10010000) % 10000) // 100
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
        
        location_names = [i.name for i in self.get_locations()]
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
        self.multiworld.completion_condition[self.player] = lambda state: all([state.has("Final Platform", self.player), state.has("Grass", self.player, self.required_grass)])

        
        
        # ---
        if "Vanilla Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Vanilla Minigame", self.player)
            region_a.connect(region_b, f"Enter Vanilla Minigame", 
                lambda state: state.has("Unlock Vanilla Minigame", self.player))
            
        if "Seeker Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Seeker Minigame", self.player)
            region_a.connect(region_b, f"Enter Seeker Minigame", 
                lambda state: state.has("Unlock Seeker Minigame", self.player))
            
        if "Button Galore Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Button Galore Minigame", self.player)
            region_a.connect(region_b, f"Enter Button Galore Minigame", 
                lambda state: state.has("Unlock Button Galore Minigame", self.player))
        
        if "OG Randomizer Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("OG Randomizer Minigame", self.player)
            region_a.connect(region_b, f"Enter OG Randomizer Minigame", 
                lambda state: state.has("Unlock OG Randomizer Minigame", self.player))
        

    def create_item(self, name: str, force_useful = False) -> Item:
        item_data = item_table[name]
        if force_useful:
            item = RefunctItem(name, ItemClassification.useful, item_data.code, self.player)
        else:
            item = RefunctItem(name, item_data.classification, item_data.code, self.player)
        return item
    
    
    def fill_slot_data(self):
        """
        make slot data, which consists of refunct_data, options, and some other variables.
        """
        slot_data = {}
        slot_data["amount_grass"] = self.amount_of_grass
        slot_data["required_grass"] = self.required_grass
        slot_data["finish_platform_c"] = self.finish_platform[0]
        slot_data["finish_platform_p"] = self.finish_platform[1]
        
        slot_data["cubes"] = self.options.cubes.value
        
        slot_data["seeker_pressed_platforms"] = self.seeker_pressed_platforms
        slot_data["og_randomizer_order"] = self.og_randomizer_order
        
        slot_data["death_link"] = self.options.death_link.value
        
        slot_data["ap_world_version"] = self.ap_world_version
        slot_data["final_platform_known"] = self.options.final_platform.value != FinalPlatform.option_random_unknown

        return slot_data