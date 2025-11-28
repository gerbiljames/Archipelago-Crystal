from typing import List, Dict, Any, ClassVar

from BaseClasses import Region, Tutorial, MultiWorld, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import BombHItem, item_data_table, item_table, stageid_to_name
from .Locations import BombHLocation, location_data_table, radio_data_table, location_table, radio_name_table, gem_data_table, gem_name_table, locked_locations, stage_names
from .Options import BombHOptions
from .Regions import region_data_table
from .Rules import *
from .Rom import MD5Hash, BombHProcedurePatch, write_tokens
from .Rom import get_base_rom_path as get_base_rom_path
from .Client import BombHClient

import Utils
import dataclasses
import typing
import random
import os
import pkgutil
import Patch
import settings

class BombHSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Bomberman Hero US rom"""
        copy_to = "BombermanHero.z64"
        description = "Bomberman Hero (US) ROM File"
        md5s = [MD5Hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class BombHWebWorld(WebWorld):
    theme = "partyTime"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Bomberman Hero.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Happyhappyism"]
    )

    setup_de = Tutorial(
        tutorial_name="Anleitung zum Anfangen",
        description="Eine Anleitung um Bomberman Hero zu spielen.",
        language="Deutsch",
        file_name="guide_de.md",
        link="guide/de",
        authors=["Held_der_Zeit"]
    )
    
    tutorials = [setup_en, setup_de]

class BombHWorld(World):
    """The greatest game of all time."""

    game = "Bomberman Hero"
    data_version = 1
    required_client_version = (0, 5, 1)
    web = BombHWebWorld()
    options: BombHOptions
    options_dataclass = BombHOptions
    settings: ClassVar[BombHSettings]
    topology_present = False
    settings_key = "bombermanhero_settings"
    location_name_to_id = location_table
    location_name_to_id.update(radio_name_table)
    location_name_to_id.update(gem_name_table)
    item_name_to_id = item_table

    included_stages = []
    second_stage = ""

    def __init__(self, world: MultiWorld, player: int):
        #self.included_stages = create_stage_list(self.options.stage_total.value)
        super().__init__(world, player)

    def create_stage_list(self, total) -> None:
        temp_stages = stage_names
        self.random.shuffle(temp_stages)
        #self.second_stage = temp_stages[0]
        inc_stages = []
        for x in range(total):
            inc_stages.append(temp_stages.pop(0))
        return inc_stages

    def create_item(self, name: str) -> BombHItem:
        return BombHItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[BombHItem] = []
        
        for name, item in item_data_table.items():
            if item.code and item.can_create(self):# and (name in self.included_stages):
                for x in range(item.num_exist):
                    item_pool.append(self.create_item(name))
            #self.multiworld.push_precollected(self.create_item("Green Key"))
        
        if self.options.max_adok.value < self.options.adok_bombs.value:
            adok_total = self.options.adok_bombs.value
        else:
            adok_total = self.options.max_adok.value
        for x in range(adok_total):
            item_pool.append(self.create_item("Adok Bomb"))
        if self.options.item_health:
            for x in range(4):
                item_pool.append(self.create_item("Healthup"))

        if self.options.two_stage:
            stage_pick = self.random.randint(0x134808,0x134859)
            while stage_pick not in stageid_to_name:
                stage_pick = self.random.randint(0x134809,0x134859)
            if stage_pick in stageid_to_name:
                self.multiworld.push_precollected(self.create_item(stageid_to_name[stage_pick]))

        junk = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        item_pool += [self.create_item(self.get_filler_item_name()) for _ in range(junk)]
        
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        #self.included_stages = self.create_stage_list(self.options.stage_total.value)
            
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        fixed_regions = ["Menu","Planet Bomber","Primus","Kanatia","Mazone","Garaden","Battle Room","Vs Bagular"]

        for region_name, region_data in region_data_table.items():
            
            #if region_name in self.included_stages or region_name in fixed_regions:
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self)# and (region_name in self.included_stages or region_name in fixed_regions)
            }, BombHLocation)
            if self.options.radio:
                region.add_locations({
                location_name: location_data.address for location_name, location_data in radio_data_table.items()
                if location_data.region == region_name and location_data.can_create(self)# and (region_name in self.included_stages or region_name in fixed_regions)
                }, BombHLocation)
            #region.add_locations({
            #    location_name: location_data.address for location_name, location_data in gem_data_table.items()
            #    if location_data.region == region_name and location_data.can_create(self)# and (region_name in self.included_stages or region_name in fixed_regions)
            #    }, BombHLocation)
            region.add_exits(region_data_table[region_name].connecting_regions)

            #loc = HKLocation(self.player, event_name, None, menu_region)
            #menu_region.locations.append(loc)
            planbomb_region = self.get_region("Planet Bomber")
            for x in range(1,(self.options.gem_check_total.value+1),1):
                check_name = f"Crystals {str(x)}"
                check_address = 0x1348060 + x
                planbomb_region.add_locations({check_name:check_address},BombHLocation)
                #loc = BombHLocation(self.player,check_name, None, planbomb_region)
                #planbomb_region.locations.append(loc)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue
            
            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)

        if self.options.item_health.value == 0:
            self.get_location("Crystals 1").place_locked_item(self.create_item("Healthup"))
            self.get_location("Crystals 2").place_locked_item(self.create_item("Healthup"))
            self.get_location("Crystals 3").place_locked_item(self.create_item("Healthup"))
            self.get_location("Crystals 4").place_locked_item(self.create_item("Healthup"))
        

    def get_filler_item_name(self) -> str:
        filler_items = ["Gold Heart","1 UP","Salt Bombs","Power Glove","Disabled HUD"]
        filler_weights = [0.5, 0.3,0.1,0.2,0.3]
        junk_item = self.random.choices(filler_items,filler_weights)[0]
        return junk_item

    def set_rules(self) -> None:
        player = self.player
        region_rules = get_region_rules(player)

        bagular_entrance = self.multiworld.get_entrance("Garaden -> Vs Bagular", player)
        bagular_entrance.access_rule = lambda state: state.has("Adok Bomb", player, self.options.adok_bombs.value)
        
        for entrance_name, rule in region_rules.items():
            entrance = self.multiworld.get_entrance(entrance_name, player)
            entrance.access_rule = rule


        location_rules = get_location_rules(player)

        for location in self.multiworld.get_locations(player):
            name = location.name
            #if name in location_rules and location_data_table[name].can_create(self.multiworld, player):
            if name in location_rules:
                location.access_rule = location_rules[name]
     # Completion condition.
        goaltype = self.options.game_goal.value
        if goaltype == 0:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Disk", player)
        elif goaltype == 1:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Adok Bomb", player, self.options.adok_bombs.value)
        elif goaltype == 2:
            from .Rules import STAGE_ITEMS
            self.multiworld.completion_condition[self.player] = lambda state: state.has_from_list(STAGE_ITEMS, player,self.options.stage_total.value)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "DeathLink": self.options.death_link.value
        }
    
    def generate_output(self, output_directory: str):
        outfilepname = f"_P{self.player}"
        outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
        self.rom_name_text = f'B64{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0'
        self.romName = bytearray(self.rom_name_text, "utf8")[:0x20]
        self.romName.extend([0] * (0x20 - len(self.romName)))
        self.rom_name = self.romName
        self.playerName = bytearray(self.multiworld.player_name[self.player], "utf8")[:0x20]
        self.playerName.extend([0] * (0x20 - len(self.playerName)))
        patch = BombHProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        #patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "bombt.bsdiff4"))
        #procedure = [("apply_bsdiff4", ["base_patch.bsdiff4"]), ("apply_tokens", ["token_data.bin"])]
        procedure = [("apply_tokens", ["token_data.bin"])]
        patch.procedure = procedure
        write_tokens(self, patch)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))
        