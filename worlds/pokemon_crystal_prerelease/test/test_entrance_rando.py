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


def _count_cross_category(world) -> int:
    conns = data.entrance_connections
    cross = 0
    for src, tgt in world.er_pairings:
        cs, ct = conns.get(src), conns.get(tgt)
        if cs and ct and cs.category != ct.category:
            cross += 1
    return cross


def _orphan_er_entrances(world) -> list:
    return [e.name for e, _v in world.er_entrances if e.connected_region is None]


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


class ERDeferredReconnectCoupledTest(PokemonCrystalTestBase):
    """Deferred (Universal Tracker) reconnection under coupled ER.

    Regression: walking through a door must only open that door and the
    partner door the player arrives at (the coupled walk-back), never the
    vanilla string-reverse of the door's name, which is an unrelated,
    independently-randomized entrance the player never discovered.
    """
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "coupled_entrances": True,
    }

    def _enter_deferred_mode(self):
        world = self.world
        world.multiworld.re_gen_passthrough = {world.game: {
            "er_pairings": list(world.er_pairings),
            "coupled_entrances": True,
        }}
        world.multiworld.enforce_deferred_connections = "on"
        world._reconnect_ut_entrances()

    def test_coupled_walk_back_opens_partner_not_vanilla_reverse(self):
        conns = data.entrance_connections
        warp_id_by_tile = {
            (w["map"], w["warp_index"]): w["id"]
            for w in load_json_data("warp_ids.json")["warps"]
        }
        self._enter_deferred_mode()
        world = self.world
        world._ensure_warp_lookups()
        targets = world._deferred_entrance_targets
        partners = world._deferred_entrance_partners
        w2e = world._warp_to_entrances

        # Find a two-way door whose exit warp maps unambiguously to itself, whose
        # coupled partner differs from the vanilla string-reverse, and where that
        # reverse is itself a deferred entrance we can check stays closed.
        candidate = None
        for source, partner in partners.items():
            conn = conns.get(source)
            if conn is None or not conn.exit_warps:
                continue
            tile = (conn.exit_warps[0].map_name, conn.exit_warps[0].warp_index)
            if w2e.get(tile) != [source]:
                continue
            if tile not in warp_id_by_tile:
                continue
            left, right = source.split(" -> ", 1)
            reverse = f"{right} -> {left}"
            if reverse == partner or reverse not in targets:
                continue
            candidate = (source, partner, reverse, warp_id_by_tile[tile])
            break

        self.assertIsNotNone(candidate, "No suitable coupled door found for the test")
        source, partner, reverse, warp_id = candidate

        get = lambda name: world.multiworld.get_entrance(name, world.player)
        # Deferred: nothing connected until its warp is discovered.
        self.assertIsNone(get(source).connected_region)
        self.assertIsNone(get(partner).connected_region)
        self.assertIsNone(get(reverse).connected_region)

        world.reconnect_found_entrances("k", [warp_id])

        self.assertIsNotNone(get(source).connected_region,
                             "Walked door did not open")
        self.assertIsNotNone(get(partner).connected_region,
                             "Coupled partner (walk-back) did not open")
        self.assertIsNone(get(reverse).connected_region,
                          "Vanilla string-reverse was opened without being discovered")


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

        cascade_fired = any("fully mixed pool" in line for line in log_ctx.output)

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


class ERTransientFailureRetryTest(PokemonCrystalTestBase):
    """A transient ER failure is recovered by retrying with a fresh RNG draw,
    keeping pools isolated instead of mixing them together."""
    auto_construct = False

    def test_retry_recovers_without_mixing(self):
        from unittest.mock import patch

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],  # everything isolated
            "coupled_entrances": False,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError

        call_count = {"n": 0}
        real_randomize = entrance_rando.randomize_entrances

        def flaky_randomize(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise EntranceRandomizationError("simulated transient failure")
            return real_randomize(*args, **kwargs)

        with patch.object(entrance_rando, "randomize_entrances", flaky_randomize):
            self.world_setup(seed=1)

        self.assertGreaterEqual(call_count["n"], 2,
                                "Expected a retry after the transient failure")
        self.assertEqual(_orphan_er_entrances(self.world), [],
                         "ER entrances left unconnected after retry recovery")
        self.assertEqual(_count_cross_category(self.world), 0,
                         "Isolated pools were mixed despite a recoverable failure")


class ERDecoupledEmptyMixIsolationTest(PokemonCrystalTestBase):
    """Regression: decoupled + empty mix_entrances must produce fully isolated
    pools (the reported bug mixed everything when an isolated pool failed once)."""
    auto_construct = False

    def test_decoupled_empty_mix_stays_isolated(self):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
        }
        for seed in range(1, 6):
            with self.subTest(seed=seed):
                self.world_setup(seed=seed)
                self.assertEqual(_orphan_er_entrances(self.world), [],
                                 "ER entrances left unconnected")
                self.assertEqual(_count_cross_category(self.world), 0,
                                 "decoupled empty mix produced cross-category pairings")


class ERCoupledEmptyMixSucceedsTest(PokemonCrystalTestBase):
    """Coupled + empty mix_entrances must always generate successfully with no orphaned
    entrances (retries, then pinning/mixing fallbacks, guarantee completion)."""
    auto_construct = False

    def test_coupled_empty_mix_generates(self):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": True,
        }
        for seed in range(1, 6):
            with self.subTest(seed=seed):
                self.world_setup(seed=seed)
                self.assertEqual(_orphan_er_entrances(self.world), [],
                                 "ER entrances left unconnected")


class ERFallbackToMixedTest(PokemonCrystalTestBase):
    """When isolation is genuinely unsolvable, ER must fall back to a fully mixed pool
    rather than failing generation. Forces every isolated grouping to fail and only the
    mixed grouping to succeed."""
    auto_construct = False

    def test_falls_back_to_mixed_pool(self):
        import logging
        from unittest.mock import patch

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError
        from ..regions import _ER_GROUP_MIXED
        import worlds.pokemon_crystal_prerelease.world as crystal_world

        real_randomize = entrance_rando.randomize_entrances

        def isolated_unsolvable(world, *, coupled, target_group_lookup, preserve_group_order):
            if _ER_GROUP_MIXED not in target_group_lookup:
                raise EntranceRandomizationError("forced isolated failure")
            return real_randomize(world, coupled=coupled, target_group_lookup=target_group_lookup,
                                  preserve_group_order=preserve_group_order)

        # Empty stranded set so pin rounds break straight to the mixed fallback
        # instead of pinning the whole (unplaced) pool to vanilla.
        with patch.object(entrance_rando, "randomize_entrances", isolated_unsolvable), \
             patch.object(crystal_world.PokemonCrystalWorld,
                          "_find_unplaced_er_entrances", lambda self: set()), \
             self.assertLogs(logging.getLogger(crystal_world.__name__), level="WARNING") as log_ctx:
            self.world_setup(seed=1)

        self.assertIn("fully mixed pool", "\n".join(log_ctx.output),
                      "Expected the mixed-pool fallback warning")
        self.assertEqual(_orphan_er_entrances(self.world), [],
                         "ER entrances left unconnected after fallback")
        self.assertGreater(_count_cross_category(self.world), 0,
                           "fallback should mix categories together")
