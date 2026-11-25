from unittest.mock import patch

from BaseClasses import ItemClassification

from .bases import PokemonCrystalTestBase
from ..data import data
from ..options import TrapWeights
from ..rom import PokemonCrystalAPPatchExtension, PokemonCrystalProcedurePatch
from ..utils import convert_to_ingame_text


# AP item ID and flag item number in the ROM.
VISUAL_TRAPS = {
    "Fly Glitch Trap": (587, 75),
    "Empty Menu Trap": (588, 76),
    "Surf Glitch Trap": (589, 77),
    "Color Glitch Trap": (590, 78),
    "Battle Glitch Trap": (591, 79),
}


class VisualTrapsTest(PokemonCrystalTestBase):
    auto_construct = False
    run_default_tests = False

    def test_trap_item_ids(self):
        for name, (item_id, flag_index) in VISUAL_TRAPS.items():
            with self.subTest(trap=name):
                item = data.items[item_id]
                self.assertEqual(item.label, name)
                self.assertEqual(item.flag_index, flag_index)
                self.assertEqual(item.classification, ItemClassification.trap)
                self.assertIn("Trap", item.tags)

    def test_trap_weights(self):
        for name in VISUAL_TRAPS:
            with self.subTest(trap=name):
                self.assertEqual(TrapWeights.default[name], 0)
                self.options = {"filler_trap_percentage": 100, "trap_weights": {name: 1}}
                self.world_setup(seed=426)
                traps = {item.name for item in self.multiworld.itempool if item.trap}
                self.assertEqual(traps, {name})

    def test_basepatch_requires_visual_traps(self):
        seed_patch = PokemonCrystalProcedurePatch()
        address = data.rom_addresses["AP_Setting_VisualTrapCapabilities"]
        marker = bytes(convert_to_ingame_text("GLITCH5")) + b"\x01"

        for revision in (0, 1):
            with self.subTest(revision=revision):
                original = bytearray(0x200000)
                original[data.rom_addresses["AP_ROM_Revision"]] = revision
                # Stand in for the ROM produced by the basepatch.
                native = bytearray(len(original))
                with patch("worlds.pokemon_crystal.rom.bsdiff4.patch", return_value=native):
                    for unsupported in (bytes(len(marker)), marker[:-1] + b"\x02"):
                        native[address:address + len(marker)] = unsupported
                        with self.assertRaisesRegex(AssertionError, "visual traps"):
                            PokemonCrystalAPPatchExtension.apply_base_patch(seed_patch, original)

                    native[address:address + len(marker)] = marker
                    result = PokemonCrystalAPPatchExtension.apply_base_patch(seed_patch, original)
                    self.assertEqual(result[address:address + len(marker)], marker)
