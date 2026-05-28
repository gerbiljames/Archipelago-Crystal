from .bases import PokemonCrystalTestBase


class IndigoFlyRegionRegisteredTest(PokemonCrystalTestBase):
    options = {}

    def test_indigo_in_fly_regions(self):
        from ..data import data
        indigo = next((fr for fr in data.fly_regions if fr.name == "Indigo Plateau"), None)
        self.assertIsNotNone(indigo)
        self.assertEqual(indigo.id, 23)
        self.assertEqual(indigo.base_identifier, "INDIGO")
        self.assertEqual(indigo.unlock_region, "REGION_ROUTE_23")
        self.assertEqual(indigo.exit_region, "REGION_ROUTE_23")
        self.assertFalse(indigo.johto)


class IndigoFlyUnlockTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_unlocks": "on",
    }

    def test_visit_location_exists_on_route_23(self):
        location = self.multiworld.get_location("Visit Indigo Plateau", self.player)
        self.assertEqual(location.parent_region.name, "REGION_ROUTE_23")

    def test_fly_item_exists(self):
        item_names = {item.name for item in self.multiworld.get_items()
                      if item.player == self.player}
        self.assertIn("Fly Indigo Plateau", item_names)


class IndigoFlyDestinationsTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_destinations": "on",
    }

    def test_all_23_slots_populated(self):
        self.assertEqual(len(self.world.fly_destinations), 23)


class IndigoBlocklistAcceptsIndigoTest(PokemonCrystalTestBase):
    options = {
        "free_fly_location": "free_fly",
        "fly_location_blocklist": ["Indigo Plateau"],
    }

    def test_blocklist_accepts_indigo(self):
        self.assertNotEqual(self.world.free_fly_location.name, "Indigo Plateau")


class IndigoFlyRegionNameValidForBlocklistTest(PokemonCrystalTestBase):
    options = {}

    def test_indigo_in_blocklist_valid_keys(self):
        from ..options import FlyLocationBlocklist
        self.assertIn("Indigo Plateau", FlyLocationBlocklist.valid_keys)
