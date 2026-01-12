import hashlib
import logging
import os
import pkgutil
import random

from BaseClasses import MultiWorld, Item, Tutorial
import settings
from typing import Dict
import Utils
from worlds.AutoWorld import World, CollectionState, WebWorld

from .Client import PokemonStadiumClient # Unused, but required to register with BizHawkClient
from .Items import create_item, create_itempool, gym_keys, item_table
from .Locations import get_location_names, get_total_locations
from .options import PokemonStadiumOptions
from .Regions import create_regions
from .Rom import MD5Hash, PokemonStadiumProcedurePatch, write_tokens
from .Rom import get_base_rom_path as get_base_rom_path
from .Rules import set_rules

class PokemonStadiumSettings(settings.Group):
    class PokemonStadiumRomFile(settings.UserFilePath):
        """File name of the Pokemon Stadium (US, 1.0) ROM"""
        description = "Pokemon Stadium (US, 1.0) ROM File"
        copy_to = "Pokemon Stadium (US, 1.0).z64"
        md5s = [PokemonStadiumProcedurePatch.hash]

    rom_file: PokemonStadiumRomFile = PokemonStadiumRomFile(PokemonStadiumRomFile.copy_to)

class PokemonStadiumWeb(WebWorld):
    theme = "Party"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up (the game you are randomizing) for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["JCIII"]
    )]

class PokemonStadiumWorld(World):
    game = "Pokemon Stadium"

    settings_key = "stadium_options"
    settings: PokemonStadiumSettings

    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}

    location_name_to_id = get_location_names()

    options_dataclass = PokemonStadiumOptions
    options: PokemonStadiumOptions

    web = PokemonStadiumWeb()

    starting_gym_keys = random.sample(gym_keys, 3)

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def generate_early(self):
        for key in self.starting_gym_keys:
            self.multiworld.push_precollected(self.create_item(key))

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def set_rules(self):
        set_rules(self)

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "options": {
                "VictoryCondition": self.options.VictoryCondition.value,
                "BaseStatTotalRandomness":   self.options.BaseStatTotalRandomness.value,
                "GymCastleRentalRandomness":   self.options.GymCastleRentalRandomness.value,
                "GymCastleTrainerRandomness":   self.options.GymCastleTrainerRandomness.value,
            },
            "Seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "Slot": self.multiworld.player_name[self.player],  # to connect to server
            "TotalLocations": get_total_locations(self) # get_total_locations(self) comes from Locations.py
        }

        return slot_data

    def generate_output(self, output_directory: str) -> None:
        # === Step 1: Build ROM and player metadata ===
        outfilepname = f"_P{self.player}_"
        outfilepname += f"{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"

        # ROM name metadata (embedded in ROM for client/UI)
        self.rom_name_text = f'PokemonStadium{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:011}\0'
        self.romName = bytearray(self.rom_name_text, "utf8")[:0x20]
        self.romName.extend([0] * (0x20 - len(self.romName)))  # pad to 0x20
        self.rom_name = self.romName

        # Player name metadata
        self.playerName = bytearray(self.multiworld.player_name[self.player], "utf8")[:0x20]
        self.playerName.extend([0] * (0x20 - len(self.playerName)))

        # === Step 3: Create procedure patch object ===
        patch = PokemonStadiumProcedurePatch(
            player=self.player,
            player_name=self.multiworld.player_name[self.player]
        )

        # === Step 4: Apply token modifications directly ===
        write_tokens(self, patch)
        procedure = [("apply_tokens", ["token_data.bin"])]

        # === Step 6: Finalize procedure ===
        patch.procedure = procedure

        # Generate output file path
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch_file_path = os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}")

        # Write the final patch file (.bps)
        patch.write(patch_file_path)

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)
