"""
This module serves as an entrypoint into the Tevi AP world.
"""
from collections import defaultdict
from typing import ClassVar, Dict, Set,List,Union,Any

from BaseClasses import ItemClassification,LocationProgressType
from Fill import swap_location_item
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from .items import TeviItem, item_table, event_item_table, get_items_by_category,get_potential_new_item,get_potential_new_filler_item,get_item_groups,teleporter_table
from .Regions import RegionDef, get_all_possible_locations,get_location_group_names
from .Options import TeviOptions
from .Web import TeviWeb
from .Utility import GetAllUpgradeables
from .TeviToApNames import TeviToApNames,ApNamesToTevi
from entrance_rando import randomize_entrances
from settings import Group,FilePath
from . import ut_stuff

class TeviSettings(Group):
    class UTPoptrackerPath(FilePath):
        """Path to the user's TEvi Poptracker Pack."""
        description = "Tevi Poptracker Pack zip file"
        required = False    
    ut_poptracker_path: Union[UTPoptrackerPath, str] = UTPoptrackerPath()

class TeviWorld(World):
    """
    Description of TEVI
    """
    version = "0.6.2"
    
    game: str = "Tevi"
    options_dataclass = TeviOptions
    options: TeviOptions
    settings: ClassVar[TeviSettings]
    topology_present: bool = False
    web: WebWorld = TeviWeb()

    base_id: int = 44966541000

    item_name_groups: Dict[str, Set[str]] = {}
    location_name_groups: Dict[str, Set[str]] = {}

    item_name_to_id: Dict[str, int] = {name: data.code for name, data in (item_table|teleporter_table).items()} 
    location_name_to_id: Dict[str, int] = {
        name: id_num for
        id_num, name in enumerate(get_all_possible_locations(), base_id)
    }

    item_name_groups = get_item_groups()
    location_name_groups = get_location_group_names()
    ut_player:int = -1

            
    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.total_locations = 0
        self.region_def = None
        self.tracker_world["map_page_setting_key"] = r"Slot:{player}:currentMap"


    def generate_early(self) -> None:
        """Set world specific generation properties"""
        #Set up the number of find able Gears
        item_table["Astral Gear"].quantity = self.options.gear_count.value
        # Reduce Goal to match Gear count if its greater
        if self.options.gear_count.value < self.options.goal_count.value:
            self.options.goal_count.value = self.options.gear_count.value

        if (hasattr(self.multiworld, "re_gen_passthrough") and "Tevi" in getattr(self.multiworld, "re_gen_passthrough")):
            self.options.traverse_Mode.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["traverse_mode"]
            self.options.goal_type.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["goal_type"]
            self.options.cKick.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["cKick"]
            self.options.hiddenP.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["hiddenP"]
            self.options.earlydream.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["earlydream"]
            self.options.barrierSkip.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["barrierSkip"]
            self.options.adcKick.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["adcKick"]
            self.options.superBosses.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["superBosses"]
            self.options.open_morose.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["open_morose"]
            self.options.randomize_item_upgrade.value = self.multiworld.re_gen_passthrough["Tevi"]["options"]["randomize_item_upgrade"]



    def create_item(self, name: str) -> TeviItem:
        """Create a Tevi item for this player"""
        data = (item_table|teleporter_table)[name]
        return TeviItem(name, data.classification, data.code, self.player)

    def create_teleporter(self,name:str) -> TeviItem:
        data = teleporter_table[name]
        return TeviItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> TeviItem:
        data = event_item_table[name]
        return TeviItem(name, data.classification, data.code, self.player)

    def create_regions(self) -> None:
        """
        Define regions and locations.
        This also defines access rules for the regions and locations.
        """
        self.region_def = RegionDef(self.multiworld, self.player, self.options)
        self.region_def.set_regions()
        self.total_locations = self.region_def.set_locations(self.location_name_to_id)
        self.region_def.set_events()
        
    def connect_entrances(self) -> None:
        self.region_def.connect_regions()
        
    def create_items(self) -> None:
        item_pool: List[TeviItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        upgradeable = GetAllUpgradeables()
        #total_locations += 2
        start_items = self.options.start_inventory.value
        removingPotions = [0,0,0,0,0]
        if self.options.traverse_Mode.value ==2:
            for name, data in teleporter_table.items():
                data.quantity = data.default_quantity
                item_pool += [self.create_teleporter(name) for _ in range(0, data.quantity)]
                pot = self.multiworld.random.randint(0,4)
                if removingPotions[pot] == 35:
                    pot = (pot +1)%5
                removingPotions[pot] += 1
                
        potIndex = 0
        for name, data in item_table.items():
            data.quantity = data.default_quantity
            if "Potion" in name:
                if potIndex <5:
                    data.quantity -= removingPotions[potIndex]
                    potIndex += 1
            start_item_amount = 0
            if name in start_items:
                start_item_amount = start_items[name]
                data.quantity -= max(0,min(start_item_amount,data.quantity))
                
            if data.quantity <= 0:
                pass    
            elif not self.options.randomize_knife.value and name == "Dagger":
                data.quantity -=1
                total_locations -=1
            elif name == "Astral Gear":
                data.quantity = max(self.options.gear_count.value,self.options.goal_count)
            elif not self.options.randomize_orb.value and name == "Orbitars":
                data.quantity -=1
                total_locations -=1
            # Celia and Sable are added to the player start inventory
            #if self.options.celia_sable.value and (name == "I20" or name =="I19"):
                #data.quantity -=1
                #total_locations -=1
            if not self.options.randomize_item_upgrade.value and ApNamesToTevi[name] in upgradeable:
                amount = min(2,max(0,start_item_amount))
                data.quantity -= 2-amount
                total_locations -= 2-amount

            if self.options.chaos_mode.value and data.classification != ItemClassification.progression  \
                                             and data.classification != ItemClassification.progression_skip_balancing:
                data.quantity = 0 
            
            item_pool += [self.create_item(name) for _ in range(0, data.quantity)]


        while len(item_pool) < total_locations:
            if self.options.chaos_mode.value:
                item_pool.append(self.create_item(self.get_chaos_item_name()))
            else:
                item_pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool += item_pool

    def fill_slot_data(self) -> dict:
        transitionData = []
        options = self.options.getOptions()
        if self.options.traverse_Mode.value == 2:
            for connection in self.region_def.randomizedEntrances:
                transitionData.append({
                    "from":connection[0],
                    "to":connection[0]
                    })
        else:
            for connection in self.region_def.randomizedEntrances:
                transitionData.append({
                    "from":connection[0],
                    "to":connection[1]
                    })

        return {
            "version":self.version,
            "openMorose": self.options.open_morose.value,
            "attackMode": self.options.free_attack_up.value,
            "CeliaSable": self.options.celia_sable.value,
            "GoalCount": self.options.goal_count.value,
            "transitionData":transitionData,
            "options": options
        }

    def set_rules(self) -> None:
        """
        Set remaining rules (for now this is just the win condition). 
        """
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.can_reach_region("Illusion Palace",self.player)

    def pre_fill(self) -> None:
        start_items = self.options.start_inventory.value

        if not self.options.randomize_knife.value and not ("Dagger" in start_items and start_items["Dagger"] >= 3):
            self.multiworld.get_location("Thanatara Canyon - Dagger",self.player).place_locked_item(self.create_item("Dagger"))
        if not self.options.randomize_orb.value and not ("Orbitars" in start_items and start_items["Orbitars"] >= 3):
            self.multiworld.get_location("Thanatara Canyon - Orbitars",self.player).place_locked_item(self.create_item("Orbitars"))
        if not self.options.randomize_item_upgrade.value:
            for item in GetAllUpgradeables():
                if not (TeviToApNames[item] in start_items and start_items[TeviToApNames[item]] >= 2):
                    self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #1",self.player).place_locked_item(self.create_item(TeviToApNames[item]))
                if not (TeviToApNames[item] in start_items and start_items[TeviToApNames[item]] >= 1):
                    self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #2",self.player).place_locked_item(self.create_item(TeviToApNames[item]))
                self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #1",self.player).progress_type = LocationProgressType.EXCLUDED
                self.multiworld.get_location(f"Item Upgrade - {TeviToApNames[item]} #2",self.player).progress_type = LocationProgressType.EXCLUDED


    def get_chaos_item_name(self) -> str:
        fillers = get_potential_new_item()
        weights = [data.weight for data in fillers.values()]
        choice = self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
        #this needs to be change / Multiple Tevi Games will run into an itempool overflow
        item_table[choice].quantity +=1
        return choice
    
    def get_filler_item_name(self) -> str:
        fillers = get_potential_new_filler_item()
        weights = [data.weight for data in fillers.values()]
        choice = self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
        #this needs to be change / Multiple Tevi Games will run into an itempool overflow
        item_table[choice].quantity +=1
        return choice
    
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        # we are using re_gen_passthrough over modifying the world here due to complexities with ER
        return slot_data   
    
    tracker_world = {
    "map_page_maps": ["maps/maps.jsonc"],
    "map_page_locations": [
        "locations/locations.jsonc"
],
    "map_page_setting_key": f"Slot:-1:currentMap",
    "map_page_index": ut_stuff.map_page_index,
    "external_pack_key": "ut_poptracker_path",
    "poptracker_name_mapping": ut_stuff.poptracker_data
}


