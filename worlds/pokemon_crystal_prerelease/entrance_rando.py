"""Entrance randomization for Pokemon Crystal: pool grouping, pod pre-placement,
plando handling and the retry ladder around Archipelago's Generic Entrance Randomizer
(the top-level ``entrance_rando`` module). A mixin, to stay out of ``world.py``."""
import logging
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Region

from .data import data, EntranceConnection, OUTDOOR_ENVIRONMENTS
from .utils import build_reverse_conn_lookup

if TYPE_CHECKING:
    from entrance_rando import EntranceType
    from worlds.AutoWorld import World as _MixinBase
    from .options import PokemonCrystalOptions
else:
    _MixinBase = object

# Group IDs for ER pools; arbitrary but stable within a generation run.
ER_GROUP_MIXED = 0
ER_GROUP_ONEWAY = 1
# Isolated pools claim sequential IDs from here, in sorted-category order.
ER_GROUP_ISOLATED_BASE = 2

# A self-mapped coupled pool can glue two overworld mouths, islanding the interiors
# behind them; splitting by side of the wall makes that pairing unrepresentable.
_ER_SIDE_OUTDOOR = "outdoor"
_ER_SIDE_INTERIOR = "interior"
_ER_SIDE_OPPOSITE = {_ER_SIDE_OUTDOOR: _ER_SIDE_INTERIOR, _ER_SIDE_INTERIOR: _ER_SIDE_OUTDOOR}

# Category alone, or category plus side when the category is split.
ErPoolKey = tuple[str, str | None]


class Sphere1CapacityError(RuntimeError):
    """Full placement with too few sphere-1 slots: a bad spawn draw, not a deadlock."""


def er_connection_side(conn: EntranceConnection) -> str | None:
    """Side of the wall this connection's door mouth stands on; None if unknown."""
    if not conn.exit_warps:
        return None
    map_data = data.maps.get(conn.exit_warps[0].map_name)
    if map_data is None:
        return None
    return _ER_SIDE_OUTDOOR if map_data.environment in OUTDOOR_ENVIRONMENTS else _ER_SIDE_INTERIOR


def _compute_er_split_categories() -> frozenset[str]:
    """Categories forming a true overworld/interior bipartition: every connection has a
    reverse on the opposite side. Anything else keeps a single self-mapped pool."""
    reverse_lookup = build_reverse_conn_lookup(data.entrance_connections)
    bipartite: dict[str, bool] = {}
    for name, conn in data.entrance_connections.items():
        if conn.one_way:
            continue
        reverse_name = reverse_lookup.get(name)
        reverse = data.entrance_connections.get(reverse_name) if reverse_name else None
        side = er_connection_side(conn)
        opposite = side is not None and reverse is not None and er_connection_side(reverse) != side
        bipartite[conn.category] = bipartite.get(conn.category, True) and opposite
    return frozenset(cat for cat, ok in bipartite.items() if ok)


ER_SPLIT_CATEGORIES = _compute_er_split_categories()


def _er_pool_key(conn: EntranceConnection, split_categories: frozenset[str]) -> ErPoolKey:
    """The isolated-pool key a connection belongs to."""
    if conn.category not in split_categories:
        return conn.category, None
    return conn.category, er_connection_side(conn)


def _build_isolated_group_map(
        isolated_categories: set[str],
        split_categories: frozenset[str],
) -> dict[ErPoolKey, int]:
    """Assign a stable integer group ID to each pool key in the isolated set.
    Split categories contribute two keys, one per side of the wall."""
    keys: list[ErPoolKey] = []
    for cat in sorted(isolated_categories):
        if cat in split_categories:
            keys.append((cat, _ER_SIDE_OUTDOOR))
            keys.append((cat, _ER_SIDE_INTERIOR))
        else:
            keys.append((cat, None))
    return {key: ER_GROUP_ISOLATED_BASE + i for i, key in enumerate(keys)}


def er_group_for_connection(
        conn: EntranceConnection,
        isolated_group_map: dict[ErPoolKey, int],
        split_categories: frozenset[str],
) -> int:
    """randomization_group for a connection; only call for randomized categories."""
    if conn.category == "One-Way":
        return ER_GROUP_ONEWAY
    return isolated_group_map.get(_er_pool_key(conn, split_categories), ER_GROUP_MIXED)


def build_er_group_lookup(
        randomize: set[str],
        mix: set[str],
        split_categories: frozenset[str] = ER_SPLIT_CATEGORIES,
) -> tuple[dict[int, list[int]], bool, dict[ErPoolKey, int]]:
    """(target_group_lookup, preserve_group_order, isolated_group_map) for
    randomize_entrances(). Unsplit pools map to themselves, split halves map to each
    other; preserve_group_order is always False."""
    randomized_non_oneway = randomize - {"One-Way"}
    isolated_categories = randomized_non_oneway - mix
    isolated_group_map = _build_isolated_group_map(isolated_categories, split_categories)

    lookup: dict[int, list[int]] = {}
    # The mixed pool needs a randomized non-one-way category in mix_entrances.
    if randomized_non_oneway & mix:
        lookup[ER_GROUP_MIXED] = [ER_GROUP_MIXED]
    if "One-Way" in randomize:
        lookup[ER_GROUP_ONEWAY] = [ER_GROUP_ONEWAY]
    for (cat, side), gid in isolated_group_map.items():
        lookup[gid] = [isolated_group_map[cat, _ER_SIDE_OPPOSITE[side]]] if side else [gid]

    return lookup, False, isolated_group_map


@dataclass
class _PlandoOrphanTarget:
    """An ER target left in the pool by a plando pairing that pre-connected its
    entrance. It has no er_entrances row, so reset rebuilds it from this."""
    region: Region
    name: str
    connection_name: str
    randomization_type: "EntranceType"
    group: int = 0


class EntranceRandoMixin(_MixinBase):
    """Entrance randomization behaviour for :class:`PokemonCrystalWorld`."""

    if TYPE_CHECKING:
        # Provided by PokemonCrystalWorld.
        options: "PokemonCrystalOptions"  # pyright: ignore[reportIncompatibleVariableOverride]
        er_entrances: list[tuple]
        er_pairings: list[tuple[str, str]]
        is_universal_tracker: bool
        ut_slot_data: dict
        _warps_by_id: dict[int, dict]
        _warp_to_entrances: dict[tuple[str, int], list[str]]

        def _resolve_pairing_target(self, target_name: str) -> str | None: ...
        def _disconnect_er_entrances_for_deferral(self, paired_sources: set[str]) -> None: ...
        def _ensure_warp_lookups(self) -> None: ...

    # Attempts run ~0.6s each on heavy option sets; 10 keeps the slowest
    # configurations inside the fuzzer's 15s budget.
    _MAX_ER_ATTEMPTS = 10
    _MAX_PIN_ROUNDS = 10
    # Per pin round: a pinned pool balances quickly or fails again, revealing more pins.
    _MAX_ER_PIN_ATTEMPTS = 5
    # Must cover the ladder's worst case (10 deadlocks + 5 sphere-1 retries + 10 pin
    # rounds x 5) so the all-pinned limit stays reachable. Deterministic on purpose.
    _MAX_TOTAL_ER_ATTEMPTS = 65
    # ER target names claimed by plando_connections; never rebuilt on retry.
    _plando_consumed_targets: frozenset[str] = frozenset()
    # Targets plando orphaned: still in the pool, but reset must rebuild them from here.
    _plando_orphan_targets: tuple["_PlandoOrphanTarget", ...] = ()

    def _shuffle_entrances(self) -> None:
        """Randomize this world's entrances. Called from connect_entrances once the
        pokemon/trade/wild fills that ER logic depends on are done."""
        if not self.options.randomize_entrances:
            if self.options.plando_connections:
                logging.warning(f"plando_connections for {self.player_name} ignored because "
                                f"randomize_entrances is not enabled.")
                self.options.plando_connections.value = []
            return

        if self.is_universal_tracker:
            self._reconnect_ut_entrances()
            return

        from entrance_rando import (randomize_entrances, EntranceRandomizationError, EntranceType,
                                    disconnect_entrance_for_randomization)

        # Pods must be found while the graph is still vanilla-connected.
        pods = self._er_pods = self._find_er_pods() if self.options.coupled_entrances else {}

        for entrance, _dest in self.er_entrances:
            if entrance.connected_region is None:
                continue
            disconnect_entrance_for_randomization(
                entrance,
                one_way_target_name=f"{entrance.name} (one-way target)"
                if entrance.randomization_type == EntranceType.ONE_WAY else None,
            )
        coupled = bool(self.options.coupled_entrances)
        randomize = set(self.options.randomize_entrances.value)
        mix = set(self.options.mix_entrances.value)

        _er_logger = logging.getLogger(__name__)

        # A split half only balances if outdoor exits match interior targets and vice
        # versa; plando consumes exits and targets independently, so a category that
        # does not balance falls back to a single pool.
        def _viable_split_categories(mix_set: set) -> frozenset[str]:
            candidates = ER_SPLIT_CATEGORIES & ((randomize - {"One-Way"}) - mix_set)
            exits: Counter[tuple[str, str | None]] = Counter()
            targets: Counter[tuple[str, str | None]] = Counter()
            for entrance, _dest in self.er_entrances:
                conn = data.entrance_connections.get(entrance.name)
                if conn is None or conn.category not in candidates:
                    continue
                exits[_er_pool_key(conn, candidates)] += 1
                if entrance.name not in self._plando_consumed_targets:
                    targets[_er_pool_key(conn, candidates)] += 1
            for orphan in self._plando_orphan_targets:
                conn = data.entrance_connections.get(orphan.connection_name)
                if conn is not None and conn.category in candidates:
                    targets[_er_pool_key(conn, candidates)] += 1

            viable = set()
            for cat in candidates:
                counts = (exits[cat, _ER_SIDE_OUTDOOR], targets[cat, _ER_SIDE_INTERIOR],
                          exits[cat, _ER_SIDE_INTERIOR], targets[cat, _ER_SIDE_OUTDOOR])
                if counts[0] and counts[0] == counts[1] and counts[2] == counts[3]:
                    viable.add(cat)
                elif counts[0] or counts[2]:
                    _er_logger.warning(
                        "ER: %s pool for %s cannot be split (%d outdoor exits need %d interior "
                        "targets, %d interior exits need %d outdoor targets), most likely from "
                        "plando_connections; shuffling it as a single pool.",
                        cat, self.player_name, *counts)
            return frozenset(viable)

        # Assign entrance groups for the given mix and return the target lookup. Targets
        # inherit groups on reset, so this runs per mix, not per attempt.
        def _assign_er_groups(mix_set: set):
            split = _viable_split_categories(mix_set)
            lookup, _preserve, isolated_group_map = build_er_group_lookup(randomize, mix_set, split)
            for entrance, _dest in self.er_entrances:
                conn = data.entrance_connections.get(entrance.name)
                if conn is None:
                    continue
                entrance.randomization_group = er_group_for_connection(conn, isolated_group_map, split)
            # Plando orphan targets have no entrance to inherit from, so group them here.
            for orphan in self._plando_orphan_targets:
                conn = data.entrance_connections.get(orphan.connection_name)
                if conn is not None:
                    orphan.group = er_group_for_connection(conn, isolated_group_map, split)
            return lookup

        def _try_randomize(target_group_lookup):
            return randomize_entrances(
                self, coupled=coupled,
                target_group_lookup=target_group_lookup,
                preserve_group_order=False,
            )

        self.er_pairings: list[tuple[str, str]] = []
        self._apply_plando_connections()
        forced_pairings = list(self.er_pairings)
        forced_targets = {tgt for _, tgt in forced_pairings}

        pinned_names: set[str] = set()
        sphere_1_failures = 0
        attempts_used = 0
        last_error = None

        def _run_attempt(target_group_lookup):
            nonlocal sphere_1_failures, attempts_used
            attempts_used += 1
            er_state = _try_randomize(target_group_lookup)
            if sphere_1_failures < self._MAX_SPHERE_1_FAILS:
                try:
                    self._check_sphere_1_capacity()
                except Sphere1CapacityError:
                    sphere_1_failures += 1
                    raise
            return er_state

        # Try a grouping with fresh RNG per attempt; commits er_pairings on success.
        def _try_group(target_group_lookup, attempts) -> bool:
            nonlocal last_error
            deadlocks = 0
            while deadlocks < attempts:
                if attempts_used >= self._MAX_TOTAL_ER_ATTEMPTS:
                    return False
                self._reset_er_entrances_to_vanilla()
                pod_pairings = self._preplace_pod_entrances(pods, target_group_lookup)
                try:
                    er_state = _run_attempt(target_group_lookup)
                except Sphere1CapacityError as error:
                    # Solvable grouping, barren spawn draw; retry without spending a deadlock.
                    last_error = error
                    continue
                except EntranceRandomizationError as error:
                    last_error = error
                    deadlocks += 1
                    continue
                self.er_pairings = forced_pairings + pod_pairings + [
                    (src, tgt) for src, tgt in er_state.pairings
                    if tgt not in forced_targets
                ]
                return True
            return False

        # Stage 1: the requested grouping; a failed isolated pool usually balances on
        # another draw.
        requested_lookup = _assign_er_groups(mix)
        if _try_group(requested_lookup, self._MAX_ER_ATTEMPTS):
            return

        pin_rounds_run = 0

        # Pin the last failure's unplaced remainder to vanilla, then retry the grouping.
        def _pin_rounds(target_group_lookup, attempts, budget) -> bool:
            nonlocal pin_rounds_run, pinned_names
            for _pin_round in range(self._MAX_PIN_ROUNDS):
                if attempts_used >= budget:
                    return False
                stranded = self._find_unplaced_er_entrances() - pinned_names
                if not stranded:
                    return False
                self._reset_er_entrances_to_vanilla()
                newly_pinned = self._pin_connections_to_vanilla(stranded)
                if not newly_pinned:
                    # All unpinnable (plando holds their targets); no round can progress.
                    return False
                pinned_names |= newly_pinned
                pin_rounds_run += 1
                _er_logger.warning(
                    "ER: pin round %d for %s: pinning stranded connections to vanilla: %s",
                    pin_rounds_run, self.player_name, sorted(newly_pinned))
                if _try_group(target_group_lookup, attempts):
                    return True
            return False

        # Stage 2 (last resort): vanilla pins are within-category, so isolation always
        # holds; in the limit an all-pinned pool trivially satisfies GER.
        _er_logger.warning(
            "ER: could not place all entrances for %s after %d retries; pinning "
            "stranded connections to vanilla. Reason: %s",
            self.player_name, self._MAX_ER_ATTEMPTS, str(last_error))
        if _pin_rounds(requested_lookup, self._MAX_ER_PIN_ATTEMPTS, self._MAX_TOTAL_ER_ATTEMPTS):
            return

        plando_hint = (" This usually means plando_connections left the requested "
                       "grouping unsatisfiable." if forced_pairings else "")
        raise EntranceRandomizationError(
            f"Pokemon Crystal: Entrance randomization failed for player {self.player} "
            f"({self.player_name}) after retries and {pin_rounds_run} vanilla pin rounds."
            f"{plando_hint} Pinned to vanilla: {sorted(pinned_names)}\n\n{last_error}")

    def _check_sphere_1_capacity(self) -> None:
        state = CollectionState(self.multiworld)
        state.sweep_for_advancements(self.get_locations())
        count = 0
        for loc in self.multiworld.get_unfilled_locations(self.player):
            if loc.address is None:
                continue
            if loc.can_reach(state):
                count += 1
        if count < self._MIN_SPHERE_1_SLOTS:
            raise Sphere1CapacityError(
                f"sphere 1 has {count} fillable slots (< {self._MIN_SPHERE_1_SLOTS})")

    def _reset_er_entrances_to_vanilla(self) -> None:
        """Disconnect every ER entrance and rebuild its target stub, clearing partial
        state. Plando-claimed targets are not recreated: their exits stay in
        er_entrances, but the stub left the pool for good."""
        from entrance_rando import EntranceType

        def rebuild(region: Region, name: str, group: int, rand_type: "EntranceType") -> None:
            for existing in region.entrances:
                if existing.name == name and existing.parent_region is None:
                    region.entrances.remove(existing)
                    break
            target = region.create_er_target(name)
            target.randomization_group = group
            target.randomization_type = rand_type

        # One-way targets can be anywhere ER put them; sweep them in one region pass.
        one_way_names = {self._er_stub(entrance, vanilla)[1]
                         for entrance, vanilla in self.er_entrances
                         if entrance.randomization_type == EntranceType.ONE_WAY}
        if one_way_names:
            for region in self.multiworld.get_regions(self.player):
                if any(e.name in one_way_names and e.parent_region is None for e in region.entrances):
                    region.entrances = [e for e in region.entrances
                                        if not (e.name in one_way_names and e.parent_region is None)]

        for entrance, vanilla_region in self.er_entrances:
            if entrance.connected_region:
                entrance.connected_region.entrances.remove(entrance)
            entrance.connected_region = None
            host, name = self._er_stub(entrance, vanilla_region)
            if name in self._plando_consumed_targets:
                continue
            rebuild(host, name, entrance.randomization_group, entrance.randomization_type)

        for orphan in self._plando_orphan_targets:
            rebuild(orphan.region, orphan.name, orphan.group, orphan.randomization_type)

    @staticmethod
    def _er_stub(entrance, vanilla_region: Region) -> tuple[Region, str]:
        """(host region, name) of an entrance's ER target: two-way in the parent region
        under its own name, one-way in the vanilla destination under a suffixed name."""
        from entrance_rando import EntranceType
        if entrance.randomization_type == EntranceType.TWO_WAY:
            return entrance.parent_region, entrance.name
        return vanilla_region, f"{entrance.name} (one-way target)"

    # Set by _shuffle_entrances.
    _er_pods: Mapping[str, str] = MappingProxyType({})

    def _find_er_pods(self) -> dict[str, str]:
        """Interior exit -> door for each pod: a cluster behind one two-way randomized
        connection with no locations, no other way in or out, and no entrance-rule
        references. Runs on the live, still-vanilla-connected graph."""
        from entrance_rando import EntranceType
        reverse_lookup = build_reverse_conn_lookup(data.entrance_connections)
        er_names = {ent.name for ent, _vanilla in self.er_entrances}
        indirect = self.multiworld.indirect_connections
        pods: dict[str, str] = {}
        for entrance, _vanilla in self.er_entrances:
            interior = reverse_lookup.get(entrance.name)
            if (entrance.randomization_type != EntranceType.TWO_WAY
                    or entrance.connected_region is None
                    or interior is None or interior not in er_names):
                continue
            cluster = {entrance.connected_region}
            stack = [entrance.connected_region]
            closed = True
            while stack and closed:
                region = stack.pop()
                for region_exit in region.exits:
                    if region_exit.name in er_names:
                        if region_exit.name != interior:
                            closed = False
                            break
                    elif region_exit.connected_region is None:
                        closed = False
                        break
                    elif region_exit.connected_region not in cluster:
                        cluster.add(region_exit.connected_region)
                        stack.append(region_exit.connected_region)
            if not closed or any(region.locations or region in indirect for region in cluster):
                continue
            if any(inbound is not entrance and inbound.parent_region not in cluster
                   for region in cluster for inbound in region.entrances):
                continue
            pods[interior] = entrance.name
        return pods

    def _preplace_pod_entrances(self, pods: dict[str, str],
                                target_group_lookup: dict[int, list[int]]) -> list[tuple[str, str]]:
        """Permute each isolated pool's pods across its vanilla pod doors before GER
        runs, mirroring coupled GER placement. Post-reset state only; er_entrances keeps
        the entries so reset restores them. Mixed pools never deadlock and keep their
        pods with GER."""

        def stub(region: Region, name: str):
            for existing in region.entrances:
                if existing.name == name and existing.parent_region is None:
                    return existing
            return None

        by_name = {ent.name: ent for ent, _vanilla in self.er_entrances}
        active = [name for name in pods
                  if (pod_exit := by_name.get(name)) is not None
                  and pod_exit.connected_region is None
                  and pod_exit.randomization_group != ER_GROUP_MIXED
                  and name not in self._plando_consumed_targets]
        if not active:
            return []

        # Vanilla pod doors consume exactly the stubs vanilla consumes, so nothing can
        # island; arbitrary doors can (Day Care yard, Tin Tower roof) and measure worse.
        pod_doors = {pods[name] for name in active}

        def safe_partner(ent) -> bool:
            return (ent.name in pod_doors and ent.connected_region is None
                    and ent.name not in self._plando_consumed_targets)

        partners = [ent for ent, _vanilla in self.er_entrances if safe_partner(ent)]
        self.random.shuffle(partners)

        pairings: list[tuple[str, str]] = []
        for name in active:
            pod_exit = by_name[name]
            pod_region = pod_exit.parent_region
            pod_stub = stub(pod_region, name)
            group = pod_exit.randomization_group
            partner = next((p for p in partners
                            if group in target_group_lookup.get(p.randomization_group, ())), None)
            if pod_stub is None or partner is None:
                continue
            partner_stub = stub(partner.parent_region, partner.name)
            if partner_stub is None:
                continue
            partners.remove(partner)
            partner_host = partner.parent_region
            partner_host.entrances.remove(partner_stub)
            pod_region.entrances.remove(pod_stub)
            partner.connect(pod_region)
            pod_exit.connect(partner_host)
            pairings.append((partner.name, name))
            pairings.append((name, partner.name))
        return pairings

    def _find_unplaced_er_entrances(self) -> set[str]:
        """Names of ER entrances the last failed attempt left unconnected."""
        return {entrance.name for entrance, _vanilla in self.er_entrances
                if entrance.connected_region is None}

    def _pin_connections_to_vanilla(self, connection_names: set[str]) -> set[str]:
        """Pin the named connections (plus reverses) to vanilla and drop them from
        er_entrances. Post-reset state only. Returns the names actually pinned."""

        reverse = build_reverse_conn_lookup(data.entrance_connections)
        names = set(connection_names)
        for n in list(names):
            rev = reverse.get(n)
            if rev:
                names.add(rev)

        randomize_set = set(self.options.randomize_entrances.value)

        remaining: list[tuple] = []
        pinned: set[str] = set()
        for entrance, vanilla_region in self.er_entrances:
            if entrance.name not in names:
                remaining.append((entrance, vanilla_region))
                continue

            conn = data.entrance_connections.get(entrance.name)
            assert conn is not None, (
                f"_pin_connections_to_vanilla: unknown connection "
                f"{entrance.name!r}")
            assert conn.category in randomize_set, (
                f"_pin_connections_to_vanilla: refusing to pin "
                f"{entrance.name!r} with category {conn.category!r}, "
                f"which is not in randomize_entrances={sorted(randomize_set)!r}")

            stub_host, stub_name = self._er_stub(entrance, vanilla_region)

            # Plando claimed this target; pinning would retire an exit with no stub.
            if stub_name in self._plando_consumed_targets:
                remaining.append((entrance, vanilla_region))
                continue

            stub_host.entrances = [
                e for e in stub_host.entrances
                if not (e.name == stub_name and e.parent_region is None)
            ]

            entrance.connected_region = vanilla_region
            vanilla_region.entrances.append(entrance)
            pinned.add(entrance.name)

        self.er_entrances = remaining
        return pinned

    def _validate_plando_pool_crossings(self, overrides: dict[str, str],
                                        rl: dict[str, str]) -> None:
        """A pairing without its mirror consumes an exit and a target from different
        pools; if those pools cannot mix, no retry or pin can rebalance them."""
        from Options import OptionError
        randomize = set(self.options.randomize_entrances.value)
        mix = set(self.options.mix_entrances.value)

        def bucket(category: str) -> str:
            return category if category == "One-Way" or category not in mix else "mixed"

        for src, ent in overrides.items():
            src_conn = data.entrance_connections.get(src)
            ent_conn = data.entrance_connections.get(ent)
            if (src_conn is None or ent_conn is None
                    or src_conn.category not in randomize or ent_conn.category not in randomize):
                continue
            mirror_src = rl.get(ent)
            mirrored = mirror_src is not None and overrides.get(mirror_src) == rl.get(src)
            if not mirrored and bucket(src_conn.category) != bucket(ent_conn.category):
                raise OptionError(
                    f"plando_connections: {src!r} => {ent!r} is one-directional and "
                    f"crosses pools that cannot mix under mix_entrances "
                    f"({src_conn.category} vs {ent_conn.category}), which makes entrance "
                    f"randomization unsatisfiable.")

    def _apply_plando_connections(self) -> None:
        """Pre-connect plando connections in the region graph and remove them from the ER pool."""
        if not self.options.plando_connections:
            return

        rl = build_reverse_conn_lookup(data.entrance_connections)

        overrides: dict[str, str] = {}
        def _add_override(src: str, dst: str, desc: str) -> None:
            if overrides.get(src) == dst:
                # Hand-written both-direction pairs collapse to duplicates; allow it.
                return
            if src in overrides:
                from Options import OptionError
                raise OptionError(
                    f"plando_connections: exit {src!r} is used by multiple pairings "
                    f"(check for conflicts with direction 'both' reverse pairings): {desc!r}"
                )
            overrides[src] = dst

        for conn in self.options.plando_connections:
            source_name = conn.entrance  # door walked through
            dest_name = conn.exit        # where you arrive
            direction = conn.direction
            desc = f"{source_name} => {dest_name}"

            if direction in ("entrance", "both"):
                _add_override(source_name, dest_name, desc)
            if direction in ("exit", "both"):
                rev_entrance = rl.get(dest_name)
                rev_exit = rl.get(source_name)
                if rev_entrance and rev_exit:
                    _add_override(rev_entrance, rev_exit, desc)

        self._validate_plando_pool_crossings(overrides, rl)

        # ER target names are reverse connection names, one-way-suffixed where needed.
        resolved: dict[str, str] = {}
        seen_targets: dict[str, str] = {}
        for src, ent in overrides.items():
            target_name = rl.get(ent, ent)
            conn = data.entrance_connections.get(target_name)
            if conn and conn.one_way:
                target_name = f"{target_name} (one-way target)"
            if target_name in seen_targets:
                from Options import OptionError
                raise OptionError(
                    f"plando_connections: target {target_name!r} is used by multiple pairings "
                    f"(exits {seen_targets[target_name]!r} and {src!r})"
                )
            seen_targets[target_name] = src
            resolved[src] = target_name

        # Build lookups of disconnected exits and parentless targets
        all_exits = {}
        all_targets = {}
        for region in self.multiworld.get_regions(self.player):
            for ex in region.exits:
                if not ex.connected_region:
                    all_exits[ex.name] = ex
            for ent in region.entrances:
                if not ent.parent_region:
                    all_targets[ent.name] = ent

        # A self-loop pairing almost always means the reverse connection was used for
        # "exit" when trying to pin to vanilla; catch it up-front.
        for src_name, tgt_name in resolved.items():
            source_exit = all_exits.get(src_name)
            target_entrance = all_targets.get(tgt_name)
            if not source_exit or not target_entrance:
                continue
            if source_exit.parent_region is target_entrance.connected_region:
                from Options import OptionError
                raise OptionError(
                    f"plando_connections: {src_name!r} would loop back to its own "
                    f"region {source_exit.parent_region.name!r}. To pin an entrance to "
                    f"its vanilla destination, use the same connection name for both "
                    f"'entrance' and 'exit' (e.g. entrance: {src_name!r}, exit: {src_name!r})."
                )

        # Connect each forced pairing in the region graph
        vanilla_by_name = {ent.name: vreg for ent, vreg in self.er_entrances}
        connected_exit_names: set[str] = set()
        applied_targets: set[str] = set()
        orphan_candidates: list[_PlandoOrphanTarget] = []
        for src_name, tgt_name in resolved.items():
            source_exit = all_exits.get(src_name)
            target_entrance = all_targets.get(tgt_name)
            if not source_exit:
                logging.warning(f"plando_connections: exit {src_name!r} not found in ER pool")
                continue
            if not target_entrance:
                logging.warning(f"plando_connections: target {tgt_name!r} not found in ER pool")
                continue

            target_region = target_entrance.connected_region
            target_region.entrances.remove(target_entrance)
            source_exit.connect(target_region)
            applied_targets.add(tgt_name)

            # Only the way in was forced: the source door's own target stays in the
            # pool, and reset must rebuild it from the orphan record.
            if src_name in vanilla_by_name:
                host, stub_name = self._er_stub(source_exit, vanilla_by_name[src_name])
                orphan_candidates.append(_PlandoOrphanTarget(
                    host, stub_name, src_name, source_exit.randomization_type))

            self.er_pairings.append((src_name, tgt_name))
            connected_exit_names.add(src_name)

        # Skipped pairings consumed nothing; reset must keep rebuilding their targets.
        self._plando_consumed_targets = frozenset(applied_targets)
        self._plando_orphan_targets = tuple(
            candidate for candidate in orphan_candidates if candidate.name not in applied_targets)

        # Remove forced entrances from er_entrances so the retry loop doesn't reset them
        self.er_entrances = [
            (ent, vreg) for ent, vreg in self.er_entrances
            if ent.name not in connected_exit_names
        ]

    def _reconnect_ut_entrances(self):
        """Reconnect ER entrances from slot data for Universal Tracker. With deferred
        connections on, entrances stay unconnected and reconnect_found_entrances wires
        them in as the player discovers each warp."""
        pairings = self.ut_slot_data.get("er_pairings", [])
        if not pairings:
            return

        deferred = getattr(self.multiworld, "enforce_deferred_connections", "off") != "off"
        self._deferred_entrance_targets = {}
        self._deferred_entrance_partners = {}

        paired_sources = {source_name for source_name, _ in pairings}

        if deferred:
            self._disconnect_er_entrances_for_deferral(paired_sources)

        for source_name, target_name in pairings:
            target_region_name = self._resolve_pairing_target(target_name)
            if target_region_name is None:
                continue
            if deferred:
                self._deferred_entrance_targets[source_name] = target_region_name
                # Coupled two-way: target_name is the partner connection to open for
                # the walk-back, not the string-reverse of source_name.
                if not target_name.endswith(" (one-way target)"):
                    self._deferred_entrance_partners[source_name] = target_name
            else:
                source = self.multiworld.get_entrance(source_name, self.player)
                if source is not None:
                    source.connect(self.get_region(target_region_name))
        self.er_pairings = [(s, t) for s, t in pairings]

    def reconnect_found_entrances(self, key: str, value) -> None:
        """Universal Tracker callback for the found-entrances data-storage key; value is
        the full list of discovered warp ids. Coupled ER also opens the partner entrance
        so the player can walk back the way they came."""
        if not value or not self._deferred_entrance_targets:
            return
        self._ensure_warp_lookups()
        targets = self._deferred_entrance_targets
        coupled = bool(self.ut_slot_data.get("coupled_entrances", False))

        def connect(ent_name: str) -> None:
            if ent_name not in targets:
                return
            entrance = self.multiworld.get_entrance(ent_name, self.player)
            if entrance is None or entrance.connected_region is not None:
                return
            entrance.connect(self.get_region(targets[ent_name]))

        for warp_id in value:
            warp = self._warps_by_id.get(warp_id)
            if warp is None:
                continue
            for ent_name in self._warp_to_entrances.get((warp["map"], warp["warp_index"]), ()):
                connect(ent_name)
                if coupled:
                    partner = self._deferred_entrance_partners.get(ent_name)
                    if partner is not None:
                        connect(partner)

    _MIN_SPHERE_1_SLOTS = 5
    _MAX_SPHERE_1_FAILS = 5
