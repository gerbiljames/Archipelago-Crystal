from .bases import PokemonCrystalTestBase


class FloodedMineOffTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "off",
        "randomize_hidden_items": "on",
    }

    def test_regions_excluded(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertNotIn("REGION_FLOODED_MINE", region_names)
        self.assertNotIn("REGION_FLOODED_MINE:NORTH_ENTRANCE", region_names)
        self.assertNotIn("REGION_FLOODED_MINE:SOUTH_ENTRANCE", region_names)
        self.assertNotIn("REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE", region_names)

    def test_locations_absent(self):
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertNotIn("Flooded Mine - Item", location_names)
        self.assertNotIn("Flooded Mine - Hidden Item Near Cherrygrove Entrance", location_names)
        self.assertNotIn("Flooded Mine - Hidden Item Southeast", location_names)
        self.assertNotIn("Flooded Mine - Hidden Item Northwest", location_names)


class FloodedMineOnTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "randomize_hidden_items": "on",
    }

    def test_regions_included(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertIn("REGION_FLOODED_MINE", region_names)
        self.assertIn("REGION_FLOODED_MINE:NORTH_ENTRANCE", region_names)
        self.assertIn("REGION_FLOODED_MINE:SOUTH_ENTRANCE", region_names)
        self.assertIn("REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE", region_names)

    def test_locations_present(self):
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn("Flooded Mine - Item", location_names)
        self.assertIn("Flooded Mine - Hidden Item Near Cherrygrove Entrance", location_names)
        self.assertIn("Flooded Mine - Hidden Item Southeast", location_names)
        self.assertIn("Flooded Mine - Hidden Item Northwest", location_names)

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR", "Victory"])
        self.assertBeatable(True)


class FloodedMineEntranceRandoTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "randomize_entrances": ["Dungeon", "Dungeon Interior"],
    }

    def test_external_entrances_two_way(self):
        from ..data import data
        for name in (
            "REGION_ROUTE_32:SOUTH -> REGION_FLOODED_MINE:NORTH_ENTRANCE",
            "REGION_FLOODED_MINE:NORTH_ENTRANCE -> REGION_ROUTE_32:SOUTH",
            "REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE -> REGION_FLOODED_MINE:SOUTH_ENTRANCE",
            "REGION_FLOODED_MINE:SOUTH_ENTRANCE -> REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE",
        ):
            self.assertIn(name, data.entrance_connections)
            self.assertFalse(data.entrance_connections[name].one_way, f"{name} should be two-way")

    def test_internal_warps_two_way(self):
        from ..data import data
        for name in (
            "REGION_FLOODED_MINE:NORTH_ENTRANCE -> REGION_FLOODED_MINE",
            "REGION_FLOODED_MINE -> REGION_FLOODED_MINE:NORTH_ENTRANCE",
            "REGION_FLOODED_MINE:SOUTH_ENTRANCE -> REGION_FLOODED_MINE",
            "REGION_FLOODED_MINE -> REGION_FLOODED_MINE:SOUTH_ENTRANCE",
        ):
            self.assertIn(name, data.entrance_connections)
            self.assertFalse(data.entrance_connections[name].one_way, f"{name} should be two-way")

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR", "Victory"])
        self.assertBeatable(True)


class FloodedMineJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "johto_only": "on",
    }

    def test_regions_included(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertIn("REGION_FLOODED_MINE", region_names)


class FloodedMineSurfGateTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
    }

    def test_cherrygrove_to_entrance_requires_surf(self):
        entrance = self.multiworld.get_entrance(
            "REGION_CHERRYGROVE_CITY -> REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE",
            self.player,
        )
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))

    def test_entrance_to_cherrygrove_requires_surf(self):
        entrance = self.multiworld.get_entrance(
            "REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE -> REGION_CHERRYGROVE_CITY",
            self.player,
        )
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))

    def test_mine_unreachable_without_surf_via_cherrygrove(self):
        # Route 32 side should remain reachable without surf; the surf gate is
        # only on the Cherrygrove approach.
        entrance = self.multiworld.get_entrance(
            "REGION_ROUTE_32:SOUTH -> REGION_FLOODED_MINE:NORTH_ENTRANCE",
            self.player,
        )
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertTrue(entrance.access_rule(empty_state))


class FloodedMineGrasssanityTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "grasssanity": "full",
    }

    def test_no_grass_locations_in_mine(self):
        from ..data import data
        for region_id in (
            "REGION_FLOODED_MINE",
            "REGION_FLOODED_MINE:NORTH_ENTRANCE",
            "REGION_FLOODED_MINE:SOUTH_ENTRANCE",
        ):
            self.assertNotIn(region_id, data.grass_tiles)
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        mine_grass = {name for name in location_names if name.startswith("Flooded Mine - Grass")}
        self.assertEqual(mine_grass, set())


class FloodedMineFlyDestinationRandoTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "randomize_fly_destinations": "on",
    }

    def test_mine_not_in_fly_destinations(self):
        from ..data import data
        fly_map_consts = {fly.base_identifier for fly in data.fly_regions}
        self.assertNotIn("FLOODED_MINE", fly_map_consts)

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR", "Victory"])
        self.assertBeatable(True)


class FloodedMineLabelsTest(PokemonCrystalTestBase):
    auto_construct = False

    def test_wild_table_labels_present(self):
        from ..data import data
        self.assertIn("AP_WildGrass_FLOODED_MINE", data.rom_addresses)
        self.assertIn("AP_WildWater_FLOODED_MINE", data.rom_addresses)

    def test_landmark_label_present(self):
        from ..data import data
        self.assertIn("AP_Landmark_FLOODED_MINE", data.rom_addresses)
