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


class WildSwarmDefaultOutOfLogicTest(PokemonCrystalTestBase):
    options = {
        "randomize_phone_call_items": "true",
        "phone_call_mode": "simple",
    }

    def test_swarm_regions_not_in_logic_by_default(self):
        from ..data import LogicalAccess
        for key, access in self.world.logic.wild_regions.items():
            if key.region_id is not None and key.region_id.endswith("_Swarm"):
                self.assertIsNot(access, LogicalAccess.InLogic,
                                 f"{key} should not be in logic when SWARM is not requested")


class WildSwarmInLogicTest(PokemonCrystalTestBase):
    options = {
        "randomize_phone_call_items": "true",
        "phone_call_mode": "simple",
        "randomize_pokegear": True,
        "wild_encounter_methods_required": [
            "Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest", "Swarm",
        ],
    }

    def test_swarm_species_available(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("DUNSPARCE", available)
        self.assertIn("YANMA", available)
        self.assertIn("QWILFISH", available)


class WildSwarmInLogicWithoutItemsRandomizedTest(PokemonCrystalTestBase):
    """Swarms qualify independently of Randomize Phone Call Items / Phone Call Mode —
    if the player asked for SWARM in wild_encounter_methods_required, they get it."""
    options = {
        "randomize_phone_call_items": "false",
        "phone_call_mode": "simple",
        "randomize_pokegear": True,
        "wild_encounter_methods_required": [
            "Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest", "Swarm",
        ],
    }

    def test_swarm_species_available(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("DUNSPARCE", available)
        self.assertIn("YANMA", available)
        self.assertIn("QWILFISH", available)


class WildSwarmRegistrationGatingTest(PokemonCrystalTestBase):
    options = {
        "randomize_phone_call_items": "true",
        "phone_call_mode": "simple",
        "randomize_pokegear": True,
        "wild_encounter_methods_required": [
            "Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest", "Swarm",
        ],
    }

    def test_swarm_locations_gated_on_registration_event(self):
        from ..data import EncounterType
        from BaseClasses import CollectionState
        # Empty state — no items collected — must not reach any swarm encounter location.
        empty = CollectionState(self.multiworld)
        any_swarm_loc = next(
            (loc for loc in self.world.multiworld.get_locations(self.world.player)
             if "wild encounter" in loc.tags
             and getattr(loc.parent_region, "key", None) is not None
             and loc.parent_region.key.encounter_type is EncounterType.Swarm),
            None,
        )
        self.assertIsNotNone(any_swarm_loc, "expected at least one swarm wild-encounter location")
        self.assertFalse(any_swarm_loc.can_reach(empty),
                         "swarm location should not be reachable with empty state")
