from .bases import PokemonCrystalTestBase
from ..data import data
from ..rom import _build_reverse_conn_lookup


class EntranceDataStructureTest(PokemonCrystalTestBase):
    """Verify entrance_data.json structural invariants without generating a world."""
    auto_construct = False

    def test_all_connections_have_reverse_lookup(self):
        """Every two-way connection should have a reverse in the lookup."""
        conns = data.entrance_connections
        reverse_lookup = _build_reverse_conn_lookup(conns)
        for name, conn in conns.items():
            if conn.one_way:
                continue
            self.assertIn(name, reverse_lookup,
                          f"Two-way connection {name} has no reverse in lookup")

    def test_reverse_lookup_is_symmetric(self):
        """If A's reverse is B, then B's reverse should be A."""
        conns = data.entrance_connections
        reverse_lookup = _build_reverse_conn_lookup(conns)
        for name, reverse_name in reverse_lookup.items():
            if conns[name].one_way:
                continue
            self.assertIn(reverse_name, reverse_lookup,
                          f"Reverse of {name} is {reverse_name} but {reverse_name} has no reverse")
            self.assertEqual(reverse_lookup[reverse_name], name,
                             f"Reverse is not symmetric: {name} -> {reverse_name} -> {reverse_lookup.get(reverse_name)}")

    def test_two_way_pairs_have_matching_types(self):
        """Both directions of a two-way pair should have the same entrance type."""
        conns = data.entrance_connections
        reverse_lookup = _build_reverse_conn_lookup(conns)
        for name, conn in conns.items():
            if conn.one_way:
                continue
            reverse_name = reverse_lookup.get(name)
            if reverse_name is None:
                continue
            reverse_conn = conns[reverse_name]
            self.assertEqual(conn.entrance_type, reverse_conn.entrance_type,
                             f"{name} has type '{conn.entrance_type}' but reverse {reverse_name} "
                             f"has type '{reverse_conn.entrance_type}'")

    def test_exit_warps_have_resolvable_labels(self):
        """Every exit_warp label should exist in rom_addresses."""
        rom_addrs = data.rom_addresses
        for name, conn in data.entrance_connections.items():
            for ew in conn.exit_warps:
                label = ew.label or f"AP_Warp_{ew.map_name}_{ew.warp_index}"
                self.assertIn(label, rom_addrs,
                              f"{name}: label {label} not found in rom_addresses")

    def test_arrival_map_consts_are_valid(self):
        """Every connection's arrival_map_const should exist in map_constants."""
        map_consts = data.map_constants
        for name, conn in data.entrance_connections.items():
            if not conn.arrival_map_const:
                continue
            self.assertIn(conn.arrival_map_const, map_consts,
                          f"{name}: arrival_map_const '{conn.arrival_map_const}' not in map_constants")


class ERAllTypesCoupledTest(PokemonCrystalTestBase):
    options = {
        "entrance_randomization": ["Gym", "Cave", "Building", "Pokecenter", "Mart",
                                   "Gate", "Interior", "Elevator"],
        "entrance_randomization_coupled": True,
    }

    def test_er_pairings_generated(self):
        """ER with all types should produce pairings."""
        self.assertTrue(len(self.world.er_pairings) > 0)

    def test_every_pairing_has_valid_source(self):
        """Every pairing source should be a known connection."""
        conns = data.entrance_connections
        for source_name, _ in self.world.er_pairings:
            self.assertIn(source_name, conns,
                          f"Pairing source '{source_name}' not in entrance_connections")

    def test_every_pairing_resolves_for_patching(self):
        """Every pairing should resolve to a writable ROM patch via write_entrance_pairings logic."""
        conns = data.entrance_connections
        reverse_lookup = _build_reverse_conn_lookup(conns)
        map_consts = data.map_constants

        unresolved = []
        for source_name, target_name in self.world.er_pairings:
            source_conn = conns.get(source_name)
            if source_conn is None or not source_conn.exit_warps:
                continue

            if target_name.endswith(" (one-way target)"):
                target_conn = conns.get(target_name.removesuffix(" (one-way target)"))
            else:
                reverse_target_name = reverse_lookup.get(target_name)
                target_conn = conns.get(reverse_target_name) if reverse_target_name else None

            if target_conn is None:
                unresolved.append((source_name, target_name, "no reverse target"))
            elif target_conn.arrival_map_const not in map_consts:
                unresolved.append((source_name, target_name, "bad arrival_map_const"))

        self.assertEqual(len(unresolved), 0,
                         f"Unresolved pairings:\n" + "\n".join(
                             f"  {s} => {t}: {reason}" for s, t, reason in unresolved))

    def test_no_duplicate_source_pairings(self):
        """Each connection should appear as source at most once in pairings."""
        seen = set()
        for source_name, _ in self.world.er_pairings:
            self.assertNotIn(source_name, seen,
                             f"'{source_name}' appears as source multiple times")
            seen.add(source_name)


class ERAllTypesDecoupledTest(PokemonCrystalTestBase):
    options = {
        "entrance_randomization": ["Gym", "Cave", "Building", "Pokecenter", "Mart",
                                   "Gate", "Interior", "Elevator"],
        "entrance_randomization_coupled": False,
    }

    def test_decoupled_generates(self):
        """Decoupled ER with all types should generate without errors."""
        self.assertTrue(len(self.world.er_pairings) > 0)

    def test_every_pairing_resolves_for_patching(self):
        """Every pairing should resolve to a writable ROM patch."""
        conns = data.entrance_connections
        reverse_lookup = _build_reverse_conn_lookup(conns)
        map_consts = data.map_constants

        unresolved = []
        for source_name, target_name in self.world.er_pairings:
            source_conn = conns.get(source_name)
            if source_conn is None or not source_conn.exit_warps:
                continue

            if target_name.endswith(" (one-way target)"):
                target_conn = conns.get(target_name.removesuffix(" (one-way target)"))
            else:
                reverse_target_name = reverse_lookup.get(target_name)
                target_conn = conns.get(reverse_target_name) if reverse_target_name else None

            if target_conn is None:
                unresolved.append((source_name, target_name, "no reverse target"))
            elif target_conn.arrival_map_const not in map_consts:
                unresolved.append((source_name, target_name, "bad arrival_map_const"))

        self.assertEqual(len(unresolved), 0,
                         f"Unresolved pairings:\n" + "\n".join(
                             f"  {s} => {t}: {reason}" for s, t, reason in unresolved))


class ERByTypeGroupingTest(PokemonCrystalTestBase):
    options = {
        "entrance_randomization": ["Gym", "Cave", "Building", "Elevator"],
        "entrance_randomization_coupled": True,
        "entrance_randomization_grouping": "by_type",
    }

    def test_by_type_generates(self):
        """By-type grouping should generate without errors."""
        self.assertTrue(len(self.world.er_pairings) > 0)


class ERByAreaGroupingTest(PokemonCrystalTestBase):
    options = {
        "entrance_randomization": ["Building", "Elevator"],
        "entrance_randomization_coupled": True,
        "entrance_randomization_grouping": "by_area",
    }

    def test_by_area_generates(self):
        """By-area grouping should generate without errors."""
        self.assertTrue(len(self.world.er_pairings) > 0)
