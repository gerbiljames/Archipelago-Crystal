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
        from ..pokemon_data import SWARM_TRAINER_REGISTRATION
        swarm_loc = registration_event = None
        for loc in self.world.multiworld.get_locations(self.world.player):
            key = getattr(loc.parent_region, "key", None)
            if (key is not None and key.encounter_type is EncounterType.Swarm
                    and "wild encounter" in loc.tags):
                event = SWARM_TRAINER_REGISTRATION.get(key.region_id)
                if event is not None:
                    swarm_loc, registration_event = loc, event
                    break
        self.assertIsNotNone(swarm_loc, "expected a swarm wild-encounter location with a registration event")
        self.assertTrue(swarm_loc.access_rule(self.multiworld.get_all_state(False)),
                        "swarm location should be reachable in all-state")
        state = self.multiworld.get_all_state(False)
        state.remove(self.world.create_event(registration_event))
        self.assertFalse(swarm_loc.access_rule(state),
                         "removing the registration event should gate the swarm location")
