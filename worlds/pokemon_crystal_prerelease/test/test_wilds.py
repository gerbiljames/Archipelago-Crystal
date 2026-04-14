from .bases import PokemonCrystalTestBase
from ..wild import get_logically_available_wilds


class WildMagikarpPlacementTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "completely_random",
        "randomize_pokemon_requests": "pokemon",
    }

    def test_magikarp_in_logical_wilds(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("MAGIKARP", available, "MAGIKARP not found in logical wilds")


class WildMagikarpBlocklistedTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "completely_random",
        "randomize_pokemon_requests": "pokemon",
        "wild_encounter_blocklist": ["Magikarp"],
    }

    def test_magikarp_placed_despite_blocklist(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("MAGIKARP", available, "MAGIKARP not placed despite being required for logic")


class WildDittoPlacementTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "completely_random",
        "breeding_methods_required": "with_ditto",
    }

    def test_ditto_in_logical_wilds(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("DITTO", available, "DITTO not found in logical wilds")


class WildCatchEmAllWithBlocklistTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "catch_em_all",
        "randomize_pokemon_requests": "pokemon",
        "wild_encounter_blocklist": ["Magikarp", "_Water"],
    }

    def test_magikarp_placed_with_catch_em_all_and_blocklist(self):
        """Must-place pokemon are placed even when blocklisted."""
        available = get_logically_available_wilds(self.world)
        self.assertIn("MAGIKARP", available)


class WildMustPlaceNotOverwrittenTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "completely_random",
        "randomize_pokemon_requests": "pokemon",
        "breeding_methods_required": "with_ditto",
        "wild_encounter_blocklist": ["Magikarp"],
    }

    def test_magikarp_and_ditto_both_placed(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("MAGIKARP", available, "MAGIKARP not found in logical wilds")
        self.assertIn("DITTO", available, "DITTO not found in logical wilds")
