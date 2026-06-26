from .bases import PokemonCrystalTestBase
from ..data import data
from ..regions import fly_back_edge_name


def _distinct_unlock_johto():
    return [fr for fr in data.fly_regions if fr.johto and fr.unlock_region != fr.exit_region]


class FlyCheeseVanillaTest(PokemonCrystalTestBase):
    options = {}

    def test_lake_of_rage_edge_exists(self):
        name = fly_back_edge_name("REGION_LAKE_OF_RAGE:FLY", "REGION_LAKE_OF_RAGE")
        entrance = self.multiworld.get_entrance(name, self.player)
        self.assertEqual(entrance.parent_region.name, "REGION_LAKE_OF_RAGE:FLY")
        self.assertEqual(entrance.connected_region.name, "REGION_LAKE_OF_RAGE")

    def test_lake_of_rage_edge_requires_fly(self):
        name = fly_back_edge_name("REGION_LAKE_OF_RAGE:FLY", "REGION_LAKE_OF_RAGE")
        entrance = self.multiworld.get_entrance(name, self.player)
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))

    def test_all_distinct_unlock_regions_have_edge(self):
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        for fr in _distinct_unlock_johto():
            self.assertIn(fly_back_edge_name(fr.unlock_region, fr.exit_region), entrance_names,
                          f"Missing fly cheese edge for {fr.name}")

    def test_unlock_source_edges_exist(self):
        # Every back-area entry point declared on the FlyRegion is wired by the fly system,
        # for those whose regions are present in this world (e.g. flooded_mine is off here).
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        for fr in data.fly_regions:
            if fr.unlock_region not in region_names:
                continue
            for src in fr.unlock_sources:
                if src not in region_names:
                    continue
                self.assertIn(f"{src} -> {fr.unlock_region}", entrance_names,
                              f"Missing unlock-source edge {src} -> {fr.unlock_region}")


class VermilionFlyEntryPointsTest(PokemonCrystalTestBase):
    options = {}

    def test_extra_unlock_edges_exist(self):
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        self.assertIn("REGION_ROUTE_11 -> REGION_VERMILION_CITY:FLY", entrance_names)
        self.assertIn("REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE -> REGION_VERMILION_CITY:FLY",
                      entrance_names)

    def test_cheese_back_to_main_requires_fly(self):
        name = fly_back_edge_name("REGION_VERMILION_CITY:FLY", "REGION_VERMILION_CITY")
        entrance = self.multiworld.get_entrance(name, self.player)
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))


class VermilionFlyEntryPointsJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on",
    }

    def test_no_kanto_unlock_edges(self):
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        self.assertNotIn("REGION_ROUTE_11 -> REGION_VERMILION_CITY:FLY", entrance_names)
        self.assertNotIn("REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE -> REGION_VERMILION_CITY:FLY",
                         entrance_names)


class MahoganyEastRegionTest(PokemonCrystalTestBase):
    options = {}

    def test_east_region_links(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertIn("REGION_MAHOGANY_TOWN:EAST", region_names)
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        self.assertIn("REGION_MAHOGANY_TOWN:EAST -> REGION_ROUTE_44", entrance_names)
        self.assertIn("REGION_MAHOGANY_TOWN:EAST -> REGION_MAHOGANY_RED_GYARADOS_SPEECH_HOUSE",
                      entrance_names)
        self.assertIn("REGION_MAHOGANY_TOWN:EAST -> REGION_MAHOGANY_TOWN:FLY", entrance_names)

    def test_salesman_gate_both_directions(self):
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        for name in ("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_TOWN:EAST",
                     "REGION_MAHOGANY_TOWN:EAST -> REGION_MAHOGANY_TOWN"):
            entrance = self.multiworld.get_entrance(name, self.player)
            self.assertFalse(entrance.access_rule(empty_state))

    def test_route_44_into_east_is_free(self):
        entrance = self.multiworld.get_entrance("REGION_ROUTE_44 -> REGION_MAHOGANY_TOWN:EAST", self.player)
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertTrue(entrance.access_rule(empty_state))


class RemoteFlyUnlockPlacementTest(PokemonCrystalTestBase):
    options = {
        "remote_items": "true",
    }

    def test_visit_places_matching_fly_unlock(self):
        # With remote items and fly unlocks not randomized, each "Visit X" must
        # hold that town's own fly unlock. Guards against FlyRegion id / flypoint
        # ordering drift (e.g. the Saffron/Celadon transposition).
        for fr in data.fly_regions:
            loc = self.multiworld.get_location(f"Visit {fr.name}", self.player)
            self.assertEqual(loc.item.name, f"Fly {fr.name}",
                             f"Visit {fr.name} holds {loc.item.name}, expected Fly {fr.name}")


class FlyCheeseDestinationRandomTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_destinations": "on",
    }

    def test_no_unlock_to_exit_edge(self):
        # Under destination randomization a flypoint no longer lands at its own town,
        # so the unlock_region -> exit_region cheese edge must not be asserted; fly is
        # instead modelled through REGION_FLY -> randomized destination.
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        for fr in _distinct_unlock_johto():
            self.assertNotIn(fly_back_edge_name(fr.unlock_region, fr.exit_region), entrance_names)
