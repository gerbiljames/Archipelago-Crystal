from .bases import PokemonCrystalTestBase
from ..data import data, load_json_data
from ..utils import build_reverse_conn_lookup


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
        reverse_lookup = build_reverse_conn_lookup(conns)
        for name, conn in conns.items():
            if conn.one_way:
                continue
            self.assertIn(name, reverse_lookup,
                          f"Two-way connection {name} has no reverse in lookup")

    def test_reverse_lookup_is_symmetric(self):
        """If A's reverse is B, then B's reverse should be A."""
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
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
        reverse_lookup = build_reverse_conn_lookup(conns)
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


def _assert_pool_balanced(test, note: str) -> None:
    exits, targets = _free_pool_counts(test.world)
    test.assertEqual(exits, targets, f"pool unbalanced {note}: {exits} exits vs {targets} targets")


def _free_pool_counts(world) -> tuple[int, int]:
    """(unplaced exits, unclaimed ER targets) currently in the region graph."""
    exits = targets = 0
    for region in world.multiworld.get_regions(world.player):
        exits += sum(1 for ex in region.exits if not ex.connected_region)
        targets += sum(1 for ent in region.entrances if not ent.parent_region)
    return exits, targets


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
        reverse_lookup = build_reverse_conn_lookup(conns)
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
    """Gym and Gym Interior removed from mix_entrances — gym entrances shuffle only
    with each other. There is no fallback that mixes categories, so this holds on
    every seed."""
    options = {
        "randomize_entrances": sorted(_VALID_CATEGORIES),
        "mix_entrances": [c for c in sorted(_VALID_CATEGORIES) if not c.startswith("Gym")],
        "coupled_entrances": True,
    }

    def test_gym_pairings_respect_isolation(self):
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
        self.assertTrue(len(self.world.er_pairings) > 0, "expected some ER pairings")

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
    """Unit tests for build_er_group_lookup and er_group_for_connection (no world gen)."""
    auto_construct = False

    def test_all_mixed_produces_single_pool(self):
        from ..entrance_rando import build_er_group_lookup, ER_GROUP_MIXED
        randomize = {"Gym", "Mart", "Building"}
        mix = {"Gym", "Mart", "Building"}
        lookup, preserve, isolated = build_er_group_lookup(randomize, mix)
        self.assertEqual(lookup, {ER_GROUP_MIXED: [ER_GROUP_MIXED]})
        self.assertEqual(isolated, {})
        self.assertFalse(preserve)

    def test_gym_isolated_gets_own_pool(self):
        from ..entrance_rando import (build_er_group_lookup, ER_GROUP_MIXED,
                               ER_GROUP_ISOLATED_BASE)
        randomize = {"Gym", "Mart", "Building"}
        mix = {"Mart", "Building"}  # Gym not in mix -> isolated
        # Gym is a split category, so it claims two group IDs (one per side of the wall)
        lookup, _, isolated = build_er_group_lookup(randomize, mix)
        self.assertEqual(isolated, {("Gym", "outdoor"): ER_GROUP_ISOLATED_BASE,
                                    ("Gym", "interior"): ER_GROUP_ISOLATED_BASE + 1})
        self.assertIn(ER_GROUP_MIXED, lookup)

    def test_unsplittable_category_maps_to_itself(self):
        from ..entrance_rando import (build_er_group_lookup, ER_SPLIT_CATEGORIES,
                               ER_GROUP_ISOLATED_BASE)
        self.assertNotIn("Pokemon League", ER_SPLIT_CATEGORIES)
        lookup, _, isolated = build_er_group_lookup({"Pokemon League"}, set())
        self.assertEqual(isolated, {("Pokemon League", None): ER_GROUP_ISOLATED_BASE})
        self.assertEqual(lookup[ER_GROUP_ISOLATED_BASE], [ER_GROUP_ISOLATED_BASE])

    def test_oneway_always_isolated(self):
        from ..entrance_rando import build_er_group_lookup, ER_GROUP_ONEWAY
        # Even with One-Ways in mix_entrances, it gets its own pool.
        randomize = {"One-Way", "Building"}
        mix = {"One-Way", "Building"}
        lookup, _, _ = build_er_group_lookup(randomize, mix)
        self.assertEqual(lookup[ER_GROUP_ONEWAY], [ER_GROUP_ONEWAY])

    def test_no_mixed_pool_when_all_isolated(self):
        from ..entrance_rando import build_er_group_lookup, ER_GROUP_MIXED
        randomize = {"Gym", "Mart"}
        mix = set()  # nothing mixes
        lookup, _, _ = build_er_group_lookup(randomize, mix)
        self.assertNotIn(ER_GROUP_MIXED, lookup)

    def test_er_group_for_connection_routes_correctly(self):
        from ..entrance_rando import (build_er_group_lookup, er_group_for_connection,
                               ER_GROUP_ONEWAY, ER_GROUP_MIXED, ER_SPLIT_CATEGORIES)
        conns = data.entrance_connections
        _, _, isolated = build_er_group_lookup({"Gym", "Building", "One-Way"}, {"Building"})
        one_way = next(c for c in conns.values() if c.category == "One-Way")
        gym_outdoor = conns["REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"]
        gym_interior = conns["REGION_AZALEA_GYM -> REGION_AZALEA_TOWN"]
        building = conns["REGION_AZALEA_TOWN -> REGION_KURTS_HOUSE"]

        split = ER_SPLIT_CATEGORIES
        self.assertEqual(er_group_for_connection(one_way, isolated, split), ER_GROUP_ONEWAY)
        self.assertEqual(er_group_for_connection(building, isolated, split), ER_GROUP_MIXED)
        self.assertEqual(er_group_for_connection(gym_outdoor, isolated, split), isolated["Gym", "outdoor"])
        self.assertEqual(er_group_for_connection(gym_interior, isolated, split), isolated["Gym", "interior"])


class ERSplitPoolTest(PokemonCrystalTestBase):
    """The overworld/interior split that keeps isolated leaf pools solvable."""
    auto_construct = False

    def test_split_categories_are_the_expected_bipartite_ones(self):
        """Guards against data drift silently disabling a split (which would
        reintroduce the stranded-interior deadlock)."""
        from ..entrance_rando import ER_SPLIT_CATEGORIES
        self.assertEqual(set(ER_SPLIT_CATEGORIES), {"Building", "Gym", "Mart", "Pokecenter"})

    def test_split_categories_are_true_bipartitions(self):
        """Matching side counts are not enough: the two directions of every connection
        must land on opposite sides, or a permutation of the split pool could still
        strand a region."""
        from ..entrance_rando import ER_SPLIT_CATEGORIES, er_connection_side
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
        for name, conn in conns.items():
            if conn.one_way or conn.category not in ER_SPLIT_CATEGORIES:
                continue
            reverse_name = reverse_lookup.get(name)
            self.assertIsNotNone(reverse_name, f"{name} has no reverse")
            self.assertNotEqual(er_connection_side(conn),
                                er_connection_side(conns[reverse_name]),
                                f"{name} and its reverse {reverse_name} are on the same side")

    def test_split_pools_cross_map_and_never_self_map(self):
        from ..entrance_rando import build_er_group_lookup, ER_SPLIT_CATEGORIES
        categories = set(ER_SPLIT_CATEGORIES)
        lookup, _, isolated = build_er_group_lookup(categories, set())
        for category in categories:
            outdoor = isolated[category, "outdoor"]
            interior = isolated[category, "interior"]
            self.assertEqual(lookup[outdoor], [interior])
            self.assertEqual(lookup[interior], [outdoor])

    def test_connection_sides_follow_map_environment(self):
        from ..entrance_rando import er_connection_side
        conns = data.entrance_connections
        self.assertEqual(er_connection_side(conns["REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"]), "outdoor")
        self.assertEqual(er_connection_side(conns["REGION_AZALEA_GYM -> REGION_AZALEA_TOWN"]), "interior")


class ERSplitPoolIsolationTest(PokemonCrystalTestBase):
    """Isolating the four bipartite categories must hold, and every pairing must join
    opposite sides of the wall."""
    auto_construct = False

    def test_split_pools_stay_isolated(self):
        from ..entrance_rando import ER_SPLIT_CATEGORIES, er_connection_side

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [c for c in _ALL_CATEGORIES if c not in ER_SPLIT_CATEGORIES],
            "coupled_entrances": True,
        }
        conns = data.entrance_connections

        for seed in range(1, 4):
            with self.subTest(seed=seed):
                self.world_setup(seed=seed)

                for source_name, target_name in self.world.er_pairings:
                    source = conns.get(source_name)
                    if source is None or source.category not in ER_SPLIT_CATEGORIES:
                        continue
                    target = conns.get(target_name)
                    if target is None:
                        self.fail(f"{target_name} is not a connection")
                    self.assertEqual(target.category, source.category,
                                     f"{source_name} ({source.category}) paired outside its pool "
                                     f"to {target_name} ({target.category})")
                    self.assertNotEqual(er_connection_side(source), er_connection_side(target),
                                        f"{source_name} paired to same-side {target_name}; "
                                        f"this strands the interiors they led to")


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
    entrances (retries then vanilla pinning guarantee completion)."""
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


class ERPlandoCrossPoolTest(PokemonCrystalTestBase):
    """A one-directional plando pairing crossing pools that cannot mix is unsatisfiable
    and must raise an OptionError naming the pairing."""
    auto_construct = False

    def test_cross_pool_pairing_fails_fast(self):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
            "plando_connections": [{
                "entrance": "REGION_AZALEA_TOWN -> REGION_KURTS_HOUSE",  # Building
                "exit": "REGION_VIOLET_CITY -> REGION_VIOLET_GYM",       # Gym
                "direction": "entrance",
            }],
        }
        with self.assertRaises(Exception) as ctx:
            self.world_setup(seed=1)
        self.assertIn("REGION_AZALEA_TOWN -> REGION_KURTS_HOUSE", str(ctx.exception))
        self.assertIn("unsatisfiable", str(ctx.exception))


class ERUnsolvableIsolationRaisesTest(PokemonCrystalTestBase):
    """When the requested grouping is genuinely unsolvable even with vanilla pins, ER
    must fail generation loudly rather than silently mixing categories together."""
    auto_construct = False

    def test_unsolvable_grouping_raises(self):
        from unittest.mock import patch

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError
        import worlds.pokemon_crystal_prerelease.world as crystal_world

        def always_fail(world, *, coupled, target_group_lookup, preserve_group_order):
            raise EntranceRandomizationError("forced failure")

        # Empty stranded set so pin rounds cannot make progress.
        with patch.object(entrance_rando, "randomize_entrances", always_fail), \
             patch.object(crystal_world.PokemonCrystalWorld,
                          "_find_unplaced_er_entrances", lambda self: set()), \
             self.assertRaises(Exception) as ctx:
            self.world_setup(seed=1)

        self.assertIn("Entrance randomization failed", str(ctx.exception))


class ERPodPreplacementTest(PokemonCrystalTestBase):
    """Coupled ER detects pods (contentless closed clusters) from the live region graph
    and pre-places them; every pre-placed pod must be paired both ways, in-category when
    its pool is isolated."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "mix_entrances": [],
        "coupled_entrances": True,
    }

    def test_pods_detected(self):
        pods = self.world._er_pods
        reverse_lookup = build_reverse_conn_lookup(data.entrance_connections)
        self.assertIn("REGION_BLACKTHORN_CITY -> REGION_MOVE_DELETERS_HOUSE", pods.values())
        self.assertGreater(len(pods), 20)
        for interior, door in pods.items():
            self.assertEqual(reverse_lookup[door], interior)

    def test_pod_regions_have_no_locations(self):
        for door in self.world._er_pods.values():
            arrival = door.split(" -> ", 1)[1]
            self.assertFalse(self.world.get_region(arrival).locations,
                             f"pod region {arrival} has locations")

    def test_pod_pairings_in_category(self):
        conns = data.entrance_connections
        pairs = dict(self.world.er_pairings)
        placed = 0
        for interior in self.world._er_pods:
            if interior not in pairs:
                # Skipped by pre-placement (mixed group or plando) and pinned vanilla by
                # a fallback; pinned connections leave er_pairings.
                continue
            placed += 1
            partner = pairs[interior]
            self.assertEqual(conns[partner].category, conns[interior].category,
                             f"pod {interior} paired outside its pool to {partner}")
            self.assertEqual(pairs[partner], interior, f"pod {interior} pairing not coupled")
        self.assertGreater(placed, 30, "pod pre-placement did not run")


class ERIsolatedPinFallbackTest(PokemonCrystalTestBase):
    """When isolated retries keep failing but pinning the stranded connections to vanilla
    lets the grouping balance, the ladder must recover there, keeping every pool
    isolated."""
    auto_construct = False

    def test_pin_fallback_keeps_isolation(self):
        import logging
        from unittest.mock import patch

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError
        import worlds.pokemon_crystal_prerelease.entrance_rando as crystal_er

        real_randomize = entrance_rando.randomize_entrances
        pool_size = {"n": None}

        # Fail while the pool is untouched; succeed once a pin round has shrunk it.
        def fail_until_pinned(world, *, coupled, target_group_lookup, preserve_group_order):
            if pool_size["n"] is None:
                pool_size["n"] = len(world.er_entrances)
            if len(world.er_entrances) == pool_size["n"]:
                raise EntranceRandomizationError("forced isolated failure")
            return real_randomize(world, coupled=coupled, target_group_lookup=target_group_lookup,
                                  preserve_group_order=preserve_group_order)

        with patch.object(entrance_rando, "randomize_entrances", fail_until_pinned), \
             self.assertLogs(logging.getLogger(crystal_er.__name__), level="WARNING") as log_ctx:
            self.world_setup(seed=1)

        log_text = "\n".join(log_ctx.output)
        self.assertIn("pin round", log_text, "Expected a vanilla pin round")
        self.assertEqual(_orphan_er_entrances(self.world), [],
                         "ER entrances left unconnected after pin fallback")
        self.assertEqual(_count_cross_category(self.world), 0,
                         "pin fallback must keep pools isolated")


_PLANDO_SOURCE = "REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"
_PLANDO_ARRIVAL = "REGION_VIOLET_CITY -> REGION_VIOLET_GYM"


class ERPlandoResetBalanceTest(PokemonCrystalTestBase):
    """A plando pairing claims an ER target whose connection keeps its entrance in the pool
    (its exit still needs randomizing), and leaves behind a target whose entrance is gone
    from the pool. Reset rebuilt the first and dropped the second, so retries drifted out of
    balance and died at GER's count guard."""
    auto_construct = False

    def _setup(self, coupled: bool, direction: str):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": coupled,
            "plando_connections": [{
                "entrance": _PLANDO_SOURCE,
                "exit": _PLANDO_ARRIVAL,
                "direction": direction,
            }],
        }
        self.world_setup(seed=1)

    def test_generates_and_reset_keeps_the_pool_balanced(self):
        """Reset must neither resurrect a plando-claimed target nor lose the one the
        forced exit left behind."""
        for coupled, direction in ((True, "both"), (False, "entrance"), (False, "both")):
            with self.subTest(coupled=coupled, direction=direction):
                self._setup(coupled, direction)
                self.assertEqual(_orphan_er_entrances(self.world), [],
                                 "ER entrances left unconnected")
                self.assertIn(_PLANDO_SOURCE, [src for src, _ in self.world.er_pairings],
                              "forced pairing missing from er_pairings")
                self.assertTrue(self.world._plando_consumed_targets,
                                "expected plando to claim at least one target")
                for reset_round in range(2):
                    self.world._reset_er_entrances_to_vanilla()
                    _assert_pool_balanced(self, f"after reset {reset_round + 1}")

    def test_survives_a_transient_failure(self):
        """The first attempt failing forces a second pass through the reset path."""
        from unittest.mock import patch
        import entrance_rando
        from entrance_rando import EntranceRandomizationError

        calls = {"n": 0}
        real_randomize = entrance_rando.randomize_entrances

        def flaky_randomize(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                raise EntranceRandomizationError("simulated transient failure")
            return real_randomize(*args, **kwargs)

        with patch.object(entrance_rando, "randomize_entrances", flaky_randomize):
            self._setup(coupled=False, direction="entrance")

        self.assertGreaterEqual(calls["n"], 2, "expected a retry after the transient failure")
        self.assertEqual(_orphan_er_entrances(self.world), [],
                         "ER entrances left unconnected after retry")

    def test_one_directional_is_promoted_to_both_when_coupled(self):
        """Coupling already forces the return trip, so a one-directional pairing is
        corrected to 'both' rather than left to strand half of itself in ER."""
        for direction in ("entrance", "exit"):
            with self.subTest(direction=direction):
                self.options = {
                    "randomize_entrances": ["Gym"],
                    "coupled_entrances": True,
                    "plando_connections": [{
                        "entrance": _PLANDO_SOURCE,
                        "exit": _PLANDO_ARRIVAL,
                        "direction": direction,
                    }],
                }
                self.world_setup(seed=1)
                self.assertEqual(
                    [c.direction for c in self.world.options.plando_connections.value],
                    ["both"])
                self.assertEqual(_orphan_er_entrances(self.world), [],
                                 "ER entrances left unconnected")

    def test_mirrored_pairings_written_by_hand_are_accepted(self):
        """Promotion to 'both' regenerates the pairing the player already spelled out in
        the other direction. The duplicate is identical, so it must not be a conflict."""
        self.options = {
            "randomize_entrances": ["Gym"],
            "coupled_entrances": True,
            "plando_connections": [
                {"entrance": _PLANDO_SOURCE, "exit": _PLANDO_ARRIVAL, "direction": "entrance"},
                {"entrance": "REGION_VIOLET_GYM -> REGION_VIOLET_CITY",
                 "exit": "REGION_AZALEA_GYM -> REGION_AZALEA_TOWN", "direction": "entrance"},
            ],
        }
        self.world_setup(seed=1)
        sources = [src for src, _ in self.world.er_pairings]
        self.assertIn(_PLANDO_SOURCE, sources)
        self.assertIn("REGION_VIOLET_GYM -> REGION_VIOLET_CITY", sources)
        self.assertEqual(_orphan_er_entrances(self.world), [])


class ERPlandoPoolAccountingTest(PokemonCrystalTestBase):
    """Plando mutates the ER pool outside er_entrances, so every path that rebuilds or
    shrinks the pool has to agree with it. Each case here previously desynced the free
    exit and free target counts, which GER rejects outright."""
    auto_construct = False

    def _setup(self, categories, coupled, plando, seed=1):
        self.options = {
            "randomize_entrances": categories,
            "mix_entrances": [],
            "coupled_entrances": coupled,
            "plando_connections": plando,
        }
        self.world_setup(seed=seed)

    def test_skipped_pairing_does_not_claim_a_target(self):
        """A pairing naming a connection outside randomize_entrances is skipped with a
        warning, so it consumes nothing and reset must keep rebuilding that target."""
        self._setup(["Gym"], True, [{
            "entrance": "REGION_AZALEA_TOWN -> REGION_KURTS_HOUSE",  # Building, not randomized
            "exit": "REGION_VIOLET_CITY -> REGION_VIOLET_GYM",
            "direction": "both",
        }], seed=7)
        self.assertEqual(self.world._plando_consumed_targets, set())
        self.assertEqual(_orphan_er_entrances(self.world), [])
        self.assertGreater(len(self.world.er_pairings), 30,
                           "Gym shuffle collapsed to vanilla")

    def test_one_way_source_keeps_its_target_stub(self):
        """A one-way source's target lives in the child region under a suffixed name.
        Its entrance leaves er_entrances, so reset has to rebuild the stub from the
        orphan record or the pool loses a target the first time an attempt claims it."""
        # seed 1: this configuration shuffles fully on stage 1; the >800 guard below is
        # only meaningful without a legitimate pin-fallback recovery shrinking the pool.
        self._setup(_ALL_CATEGORIES, True, [{
            "entrance": "REGION_OLIVINE_LIGHTHOUSE_6F -> REGION_OLIVINE_LIGHTHOUSE_5F",
            "exit": "REGION_BLACKTHORN_GYM_2F -> REGION_BLACKTHORN_GYM_1F:HOLE_1",
            "direction": "both",
        }], seed=1)
        orphan_names = [orphan.name for orphan in self.world._plando_orphan_targets]
        self.assertIn("REGION_OLIVINE_LIGHTHOUSE_6F -> REGION_OLIVINE_LIGHTHOUSE_5F (one-way target)",
                      orphan_names)
        for reset_round in range(2):
            self.world._reset_er_entrances_to_vanilla()
            _assert_pool_balanced(self, f"after reset {reset_round + 1}")
        self.assertGreater(len(self.world.er_pairings), 800,
                           "entrance shuffle collapsed to vanilla")

    def test_pinning_a_consumed_targets_owner_keeps_the_pool_balanced(self):
        """Pinning retires an exit and its target stub together, but plando already took
        that stub. Such a connection has to be left unpinned."""
        consumed_owner = "REGION_VIOLET_GYM -> REGION_VIOLET_CITY"
        self._setup(_ALL_CATEGORIES, False, [{
            "entrance": _PLANDO_SOURCE,
            "exit": _PLANDO_ARRIVAL,
            "direction": "entrance",
        }])
        self.assertIn(consumed_owner, self.world._plando_consumed_targets)

        self.world._reset_er_entrances_to_vanilla()
        _assert_pool_balanced(self, "before pinning")
        self.world._pin_connections_to_vanilla({consumed_owner})
        _assert_pool_balanced(self, "after pinning")
        self.world._reset_er_entrances_to_vanilla()
        _assert_pool_balanced(self, "after the reset that follows pinning")

    def test_split_viability_counts_targets_not_exits(self):
        """Two uncoupled pairings, one per side of the wall, leave the exit counts even
        while the target counts are skewed. Splitting on the exit counts would hand GER
        an unsatisfiable pool for every attempt."""
        self._setup(_ALL_CATEGORIES, False, [
            {"entrance": "REGION_AZALEA_TOWN -> REGION_AZALEA_GYM",
             "exit": "REGION_VIOLET_CITY -> REGION_VIOLET_GYM", "direction": "entrance"},
            {"entrance": "REGION_AZALEA_GYM -> REGION_AZALEA_TOWN",
             "exit": "REGION_ECRUTEAK_CITY -> REGION_ECRUTEAK_GYM", "direction": "entrance"},
        ], seed=5)
        self.assertEqual(_orphan_er_entrances(self.world), [])
        self.assertGreater(len(self.world.er_pairings), 800,
                           "entrance shuffle collapsed to vanilla")
        # Splitting on the exit counts alone still generates -- it just burns every
        # isolated attempt and lands in the mixed-pool fallback, silently discarding
        # mix_entrances. That is the failure this guards, so assert isolation held.
        self.assertEqual(_count_cross_category(self.world), 0,
                         "isolation was lost to the mixed-pool fallback")
