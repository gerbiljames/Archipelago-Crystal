from .bases import PokemonCrystalTestBase
from ..data import data, load_json_data
from ..rom import _build_reverse_conn_lookup


_VALID_CATEGORIES = frozenset(load_json_data("entrance_types.json").values())


class EntranceDataStructureTest(PokemonCrystalTestBase):
    """Verify entrance_data.json structural invariants without generating a world."""
    auto_construct = False

    VALID_CATEGORIES = _VALID_CATEGORIES

    def test_every_connection_has_a_category(self):
        """Every connection in entrance_data.json must have a valid category."""
        for name, conn in data.entrance_connections.items():
            self.assertIn(conn.category, self.VALID_CATEGORIES,
                          f"{name} has invalid category {conn.category!r}")

    def test_no_orphan_entries_in_entrance_types(self):
        """Every key in entrance_types.json must correspond to a real connection."""
        entrance_types = load_json_data("entrance_types.json")
        connection_names = set(data.entrance_connections.keys())
        orphans = set(entrance_types.keys()) - connection_names
        self.assertEqual(orphans, set(), f"Orphan entrance_types.json entries: {orphans}")

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
            self.assertEqual(conn.category, reverse_conn.category,
                             f"{name} has category '{conn.category}' but reverse {reverse_name} "
                             f"has category '{reverse_conn.category}'")

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


_ALL_CATEGORIES = sorted(_VALID_CATEGORIES)


class ERAllMixedCoupledTest(PokemonCrystalTestBase):
    """Default mix_entrances (all categories mixed) with coupling on."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "coupled_entrances": True,
    }

    def test_er_pairings_generated(self):
        self.assertTrue(len(self.world.er_pairings) > 0)

    def test_every_pairing_has_valid_source(self):
        conns = data.entrance_connections
        for source_name, _ in self.world.er_pairings:
            self.assertIn(source_name, conns,
                          f"Pairing source '{source_name}' not in entrance_connections")

    def test_every_pairing_resolves_for_patching(self):
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
                         "Unresolved pairings:\n" + "\n".join(
                             f"  {s} => {t}: {reason}" for s, t, reason in unresolved))

    def test_no_duplicate_source_pairings(self):
        seen = set()
        for source_name, _ in self.world.er_pairings:
            self.assertNotIn(source_name, seen,
                             f"'{source_name}' appears as source multiple times")
            seen.add(source_name)


class ERAllMixedDecoupledTest(PokemonCrystalTestBase):
    """Same as above but decoupled. One-ways remain structurally one-way either way."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "coupled_entrances": False,
    }

    def test_decoupled_generates(self):
        self.assertTrue(len(self.world.er_pairings) > 0)


class ERGymIsolatedTest(PokemonCrystalTestBase):
    """Gym and Gym Interior removed from mix_entrances — gym entrances shuffle only with each other,
    unless the cascade promotes them into the mixed pool because the isolated pool can't balance."""
    auto_construct = False
    options = {
        "randomize_entrances": sorted(_VALID_CATEGORIES),
        "mix_entrances": [c for c in sorted(_VALID_CATEGORIES) if not c.startswith("Gym")],
        "coupled_entrances": True,
    }

    def test_gym_pairings_respect_isolation_or_cascade(self):
        """Every Gym-category source pairs to a Gym-category target UNLESS the cascade promoted Gym."""
        import logging
        import worlds.pokemon_crystal_prerelease.world as crystal_world

        with self.assertLogs(logging.getLogger(crystal_world.__name__),
                             level="WARNING") as log_ctx:
            # Emit a guard log so assertLogs always has at least one record
            # (assertLogs raises if zero records are captured).
            logging.getLogger(crystal_world.__name__).warning("test-guard: setup starting")
            self.world_setup()

        cascade_fired = any("promoting to the mixed pool" in line for line in log_ctx.output)

        conns = data.entrance_connections
        reverse_lookup = _build_reverse_conn_lookup(conns)
        self.assertTrue(len(self.world.er_pairings) > 0, "expected some ER pairings")

        if cascade_fired:
            # Cascade promoted Gym into the mixed pool; strict isolation does not hold this seed.
            return

        for source_name, target_name in self.world.er_pairings:
            src = conns[source_name]
            if src.category != "Gym":
                continue
            if target_name.endswith(" (one-way target)"):
                tgt_name = target_name.removesuffix(" (one-way target)")
            else:
                tgt_name = reverse_lookup.get(target_name, target_name)
            tgt = conns.get(tgt_name)
            if tgt is None:
                continue
            self.assertEqual(tgt.category, "Gym",
                             f"Gym source {source_name} paired to non-Gym target "
                             f"{tgt_name} (category={tgt.category})")


class ERMultipleIsolatedTest(PokemonCrystalTestBase):
    """Multiple closed pools — Gym and Mart each shuffle only within themselves."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "mix_entrances": [c for c in _ALL_CATEGORIES
                          if not c.startswith("Gym") and not c.startswith("Mart")],
        "coupled_entrances": True,
    }

    def test_generates(self):
        self.assertTrue(len(self.world.er_pairings) > 0)


class EROffTest(PokemonCrystalTestBase):
    """Empty randomize_entrances disables ER entirely."""
    options = {
        "randomize_entrances": [],
    }

    def test_no_er_pairings(self):
        self.assertEqual(len(self.world.er_pairings), 0)


class EROneWayOnlyTest(PokemonCrystalTestBase):
    """Only One-Ways randomized. Validates the One-Way-isolated pool works on its own."""
    options = {
        "randomize_entrances": ["One-Way"],
    }

    def test_oneway_generate(self):
        conns = data.entrance_connections
        self.assertTrue(len(self.world.er_pairings) > 0)
        for source_name, _ in self.world.er_pairings:
            self.assertEqual(conns[source_name].category, "One-Way")


class ERGroupLookupTest(PokemonCrystalTestBase):
    """Unit tests for _build_er_group_lookup and _er_group_for_connection (no world gen)."""
    auto_construct = False

    def test_all_mixed_produces_single_pool(self):
        from ..regions import _build_er_group_lookup, _ER_GROUP_MIXED
        randomize = {"Gym", "Mart", "Building"}
        mix = {"Gym", "Mart", "Building"}
        lookup, preserve, isolated = _build_er_group_lookup(randomize, mix)
        self.assertEqual(lookup, {_ER_GROUP_MIXED: [_ER_GROUP_MIXED]})
        self.assertEqual(isolated, {})
        self.assertFalse(preserve)

    def test_gym_isolated_gets_own_pool(self):
        from ..regions import (_build_er_group_lookup, _ER_GROUP_MIXED,
                               _ER_GROUP_ISOLATED_BASE)
        randomize = {"Gym", "Mart", "Building"}
        mix = {"Mart", "Building"}  # Gym not in mix -> isolated
        lookup, _, isolated = _build_er_group_lookup(randomize, mix)
        self.assertEqual(isolated, {"Gym": _ER_GROUP_ISOLATED_BASE})
        self.assertIn(_ER_GROUP_MIXED, lookup)
        self.assertEqual(lookup[_ER_GROUP_ISOLATED_BASE], [_ER_GROUP_ISOLATED_BASE])

    def test_oneway_always_isolated(self):
        from ..regions import _build_er_group_lookup, _ER_GROUP_ONEWAY
        # Even with One-Ways in mix_entrances, it gets its own pool.
        randomize = {"One-Way", "Building"}
        mix = {"One-Way", "Building"}
        lookup, _, _ = _build_er_group_lookup(randomize, mix)
        self.assertEqual(lookup[_ER_GROUP_ONEWAY], [_ER_GROUP_ONEWAY])

    def test_no_mixed_pool_when_all_isolated(self):
        from ..regions import _build_er_group_lookup, _ER_GROUP_MIXED
        randomize = {"Gym", "Mart"}
        mix = set()  # nothing mixes
        lookup, _, _ = _build_er_group_lookup(randomize, mix)
        self.assertNotIn(_ER_GROUP_MIXED, lookup)

    def test_er_group_for_connection_routes_correctly(self):
        from ..regions import (_er_group_for_connection, _ER_GROUP_ONEWAY,
                               _ER_GROUP_MIXED, _ER_GROUP_ISOLATED_BASE)
        isolated = {"Gym": _ER_GROUP_ISOLATED_BASE}
        self.assertEqual(_er_group_for_connection("One-Way", isolated), _ER_GROUP_ONEWAY)
        self.assertEqual(_er_group_for_connection("Gym", isolated), _ER_GROUP_ISOLATED_BASE)
        self.assertEqual(_er_group_for_connection("Building", isolated), _ER_GROUP_MIXED)


class ERCascadePromotionTest(PokemonCrystalTestBase):
    """Verify the ER fallback cascade promotes isolated pools into the mixed pool
    when the first randomization attempt fails."""
    auto_construct = False

    def test_cascade_promotes_isolated_on_failure(self):
        import logging
        from unittest.mock import patch

        # Gym isolated (not in mix). If the first randomize_entrances call raises,
        # the cascade should promote Gym into the mixed pool and retry.
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [c for c in _ALL_CATEGORIES if not c.startswith("Gym")],
            "coupled_entrances": True,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError

        call_count = {"n": 0}
        real_randomize = entrance_rando.randomize_entrances

        def flaky_randomize(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise EntranceRandomizationError("simulated isolated pool failure")
            return real_randomize(*args, **kwargs)

        import worlds.pokemon_crystal_prerelease.world as crystal_world

        with patch.object(entrance_rando, "randomize_entrances", flaky_randomize), \
             self.assertLogs(logging.getLogger(crystal_world.__name__),
                             level="WARNING") as log_ctx:
            self.world_setup()

        self.assertGreaterEqual(call_count["n"], 2,
                                "Expected cascade to trigger a retry after first failure")
        warning_text = "\n".join(log_ctx.output)
        self.assertIn("promoting to the mixed pool", warning_text,
                      f"Expected cascade promotion warning in log, got:\n{warning_text}")


class ERCascadeNoOrphanEntrancesTest(PokemonCrystalTestBase):
    """After cascade promotion, every ER entrance in the pool must have a valid connected_region.
    Reproduces the fuzzer-found bug where the promotion retry ran on partial ER state,
    leaving some entrances with connected_region=None."""
    auto_construct = False

    def test_all_er_entrances_connected_after_cascade(self):
        """Every entrance in the ER pool must have a connected_region after world generation.
        A None connected_region indicates the cascade retry ran on polluted partial state."""
        import logging
        from unittest.mock import patch

        # Gym isolated (not in mix). Force the first randomize_entrances call to fail,
        # triggering the cascade to promote Gym into the mixed pool and retry.
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [c for c in _ALL_CATEGORIES if not c.startswith("Gym")],
            "coupled_entrances": True,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError

        call_count = {"n": 0}
        real_randomize = entrance_rando.randomize_entrances

        def fail_first_then_real(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise EntranceRandomizationError("forced cascade trigger")
            return real_randomize(*args, **kwargs)

        import worlds.pokemon_crystal_prerelease.world as crystal_world

        with patch.object(entrance_rando, "randomize_entrances", fail_first_then_real), \
             self.assertLogs(logging.getLogger(crystal_world.__name__),
                             level="WARNING") as log_ctx:
            logging.getLogger(crystal_world.__name__).warning("test-guard: setup starting")
            self.world_setup()

        self.assertGreaterEqual(call_count["n"], 2,
                                "Expected cascade to trigger a retry after first failure")
        self.assertIn("promoting to the mixed pool", "\n".join(log_ctx.output),
                      "Expected cascade promotion warning in logs")

        # Every ER entrance must have a connected_region after successful generation.
        null_entrances = [
            entrance.name
            for entrance, _vanilla in self.world.er_entrances
            if entrance.connected_region is None
        ]
        self.assertEqual(null_entrances, [],
                         f"ER entrances with connected_region=None after cascade: {null_entrances}")
