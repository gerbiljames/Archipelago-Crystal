"""Entrance randomization for Pokemon Crystal: pool grouping, pod pre-placement,
plando handling and the retry ladder around Archipelago's Generic Entrance Randomizer
(the top-level ``entrance_rando`` module). A mixin, to stay out of ``world.py``."""
import logging
import pkgutil
import re
from collections.abc import Mapping
from dataclasses import dataclass
from itertools import chain
from types import MappingProxyType
from typing import TYPE_CHECKING

import orjson

from BaseClasses import CollectionState, Region

from .data import data, EntranceConnection

if TYPE_CHECKING:
    from entrance_rando import EntranceType
    from worlds.AutoWorld import World as _MixinBase
    from .options import PokemonCrystalOptions
else:
    _MixinBase = object


class Sphere1CapacityError(RuntimeError):
    """Full placement with too few sphere-1 slots: a bad spawn draw, not a deadlock."""


# Group IDs for ER pool assignment. Integers are arbitrary but must be stable
# within a single world-generation run.
ER_GROUP_ONEWAY = 0
# Isolated per-category groups get IDs >= ER_GROUP_ISOLATED_BASE. One ID per
# category in `isolated_categories`, assigned in sorted order for determinism.
ER_GROUP_ISOLATED_BASE = 1

_ER_BIPARTITE_ENTRANCE = "Entrance"
_ER_BIPARTITE_EXIT = "Exit"
_ER_SIDE_OPPOSITE = {_ER_BIPARTITE_ENTRANCE: _ER_BIPARTITE_EXIT, _ER_BIPARTITE_EXIT: _ER_BIPARTITE_ENTRANCE}
ER_BIPARTITE_SUFFIX = re.compile(f" ({_ER_BIPARTITE_ENTRANCE}|{_ER_BIPARTITE_EXIT})$")


def base_category(category: str) -> str:
    """The option-facing category name: a bipartite category without its side suffix."""
    return ER_BIPARTITE_SUFFIX.sub("", category)


def _load_entrance_categories() -> tuple[set[str], set[str]]:
    """Read data/entrance_types.json into a set of available entrance categories.
    Bipartite categories are a special group of categories that have a clear
    entrance/exit separation where we don't want one to map to itself,
    those have suffixes that we strip from the result set."""
    raw = pkgutil.get_data(__name__, "data/entrance_types.json")
    mapping = orjson.loads(raw.decode("utf-8-sig"))
    unique_categories = {cat for _, cat in mapping.items()}
    bipartite = {base_category(cat) for cat in unique_categories if ER_BIPARTITE_SUFFIX.search(cat)}
    regrouped_categories = {base_category(cat) for cat in unique_categories}
    return (frozenset(bipartite), frozenset(regrouped_categories))
ER_BIPARTITE_CATEGORIES, ENTRANCE_CATEGORIES = _load_entrance_categories()


def _build_group_map(
        randomized_categories: set[str],
) -> dict[str, int]:
    """Assign a stable integer group ID to each pool key in the randomized set.
    Bipartite categories contribute two keys, one per side of the wall."""
    group_map = {"One-Way": ER_GROUP_ONEWAY}
    keys: list[str] = []
    for cat in sorted(randomized_categories):
        if cat in ER_BIPARTITE_CATEGORIES:
            keys.append(f"{cat} {_ER_BIPARTITE_ENTRANCE}")
            keys.append(f"{cat} {_ER_BIPARTITE_EXIT}")
        else:
            keys.append(cat)
    group_map.update({key: ER_GROUP_ISOLATED_BASE + i for i, key in enumerate(keys)})
    return group_map


def build_er_group_lookup(
        randomize: set[str],
        mix: set[str],
) -> tuple[dict[int, list[int]], bool, dict[str, int]]:
    """Build target_group_lookup and group_map for randomize_entrances().

    Returns:
        target_group_lookup: maps each source group ID to the list of target
            group IDs it may match with. Non-bipartite pools map to themselves; the
            two halves of a bipartite pool map to each other.
        preserve_group_order: always False (no soft-preference fallback).
        group_map: name -> group ID for categories. Used by the caller
            to assign connections to the right group.
    """
    randomized_non_oneway = randomize - {"One-Way"}
    group_map = _build_group_map(randomized_non_oneway)

    lookup: dict[int, list[int]] = {}
    for cat, gid in group_map.items():
        if cat == "One-Way":
            # One-Way is always its own pool; mix_entrances never applies to it.
            if "One-Way" in randomize:
                lookup[gid] = [gid]
            continue
        regrouped = base_category(cat)
        # Sorted: GER concatenates the target groups in this order before shuffling, so an
        # unordered set here would make the same seed generate differently per process.
        destinations = sorted(mix & randomized_non_oneway if regrouped in mix else {regrouped})
        bipartite_match = ER_BIPARTITE_SUFFIX.search(cat)
        if bipartite_match:
            opposite = _ER_SIDE_OPPOSITE[bipartite_match.group(1)]
            lookup[gid] = [group_map[f"{dest} {opposite}" if dest in ER_BIPARTITE_CATEGORIES else dest]
                           for dest in destinations]
        else:
            keys = chain.from_iterable([[f"{dest} {_ER_BIPARTITE_ENTRANCE}", f"{dest} {_ER_BIPARTITE_EXIT}"]
                                        if dest in ER_BIPARTITE_CATEGORIES else [dest] for dest in destinations])
            lookup[gid] = [group_map[key] for key in keys]

    return lookup, False, group_map


def build_reverse_conn_lookup(conns: Mapping[str, EntranceConnection]) -> dict[str, str]:
    conn_names = set(conns.keys())
    lookup: dict[str, str] = {}
    for name, conn in conns.items():
        exact = f"{conn.entrance_region} -> {conn.exit_region}"
        if exact in conn_names:
            lookup[name] = exact
            continue

        dst = conn.entrance_region
        src_base = conn.exit_region.split(":")[0]
        if ":" in dst:
            dst_base = dst.split(":")[0]
            suffix = dst[len(dst_base):]  # includes the leading ":"
            candidate = f"{dst_base} -> {src_base}{suffix}"
            if candidate in conn_names:
                lookup[name] = candidate
    return lookup


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

        # Assign each entrance's randomization group for the given mix and return the
        # target lookup. Targets inherit the group on the next reset/disconnect, so this
        # only needs to run when the mix changes, not per attempt.
        def _assign_er_groups(mix_set: set):
            lookup, _preserve, group_map = build_er_group_lookup(randomize, mix_set)
            for entrance, _dest in self.er_entrances:
                conn = data.entrance_connections.get(entrance.name)
                if conn is None:
                    continue
                entrance.randomization_group = group_map[conn.category]
            # Plando orphan targets have no entrance to inherit from, so group them here.
            for orphan in self._plando_orphan_targets:
                conn = data.entrance_connections.get(orphan.connection_name)
                if conn is not None:
                    orphan.group = group_map[conn.category]
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

        # One-way targets can be anywhere ER put them, so they are swept out in a single
        # pass over this player's regions rather than once per entrance.
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

        def isolated(group: int) -> bool:
            # An isolated pool draws from exactly one target group; mixing widens it.
            return len(target_group_lookup.get(group, ())) <= 1

        by_name = {ent.name: ent for ent, _vanilla in self.er_entrances}
        active = [name for name in pods
                  if (pod_exit := by_name.get(name)) is not None
                  and pod_exit.connected_region is None
                  and isolated(pod_exit.randomization_group)
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
        """Restore the named ER connections (and their reverse direction) to
        their vanilla destinations and drop them from self.er_entrances.
        Must be called when entrances are in the post-reset disconnected
        state (i.e. immediately after _reset_er_entrances_to_vanilla).

        Returns the full set of connection names that were actually pinned
        (including reverse directions)."""

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
            assert base_category(conn.category) in randomize_set, (
                f"_pin_connections_to_vanilla: refusing to pin "
                f"{entrance.name!r} with category {conn.category!r}, "
                f"which is not in randomize_entrances={sorted(randomize_set)!r}")

            stub_host, stub_name = self._er_stub(entrance, vanilla_region)

            # Plando already claimed this connection's target, so there is no stub to
            # retire alongside the exit. Pinning it would drop an exit and no target.
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
        pools; if the exit's pool cannot draw from the target's, no retry or pin can
        rebalance them. Catches both an unmixable category crossing and a bipartite
        category paired to its own side."""
        from Options import OptionError
        randomize = set(self.options.randomize_entrances.value)
        mix = set(self.options.mix_entrances.value)
        lookup, _preserve, group_map = build_er_group_lookup(randomize, mix)

        for src, ent in overrides.items():
            src_conn = data.entrance_connections.get(src)
            # The stub a pairing consumes belongs to the arrival door's reverse.
            target_conn = data.entrance_connections.get(rl.get(ent, ent))
            if (src_conn is None or target_conn is None
                    or base_category(src_conn.category) not in randomize
                    or base_category(target_conn.category) not in randomize):
                continue
            mirror_src = rl.get(ent)
            mirrored = mirror_src is not None and overrides.get(mirror_src) == rl.get(src)
            src_group = group_map[src_conn.category]
            if not mirrored and group_map[target_conn.category] not in lookup.get(src_group, ()):
                raise OptionError(
                    f"plando_connections: {src!r} => {ent!r} is one-directional and "
                    f"lands in a pool {src_conn.category!r} cannot draw from "
                    f"({target_conn.category!r}), which makes entrance randomization "
                    f"unsatisfiable. Check mix_entrances, and that the arrival names the "
                    f"door you walk into rather than the one you come back out of.")

    def _apply_plando_connections(self) -> None:
        """Pre-connect plando connections in the region graph and remove them from the ER pool."""
        if not self.options.plando_connections:
            return

        rl = build_reverse_conn_lookup(data.entrance_connections)

        overrides: dict[str, str] = {}
        def _add_override(src: str, dst: str, desc: str) -> None:
            if overrides.get(src) == dst:
                # Spelling both directions out by hand produces the same pairing twice
                # once coupling promotes each one to "both". Harmless, so allow it.
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

        # Resolve target names: the ER target name is the reverse connection name,
        # with a one-way suffix if applicable
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

        # Detect self-loop pairings (arrival region == source region). These almost
        # always indicate the user mistakenly used the reverse connection for "exit"
        # when trying to pin to vanilla. Catch it up-front rather than letting it
        # silently destabilize ER into pin-round exhaustion.
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

            # This pairing only forced the way in, so the target at the source's own door
            # stays in the pool for something else to arrive at. Its entrance leaves
            # er_entrances below, so reset has to rebuild it from here instead.
            if src_name in vanilla_by_name:
                host, stub_name = self._er_stub(source_exit, vanilla_by_name[src_name])
                orphan_candidates.append(_PlandoOrphanTarget(
                    host, stub_name, src_name, source_exit.randomization_type))

            self.er_pairings.append((src_name, tgt_name))
            connected_exit_names.add(src_name)

        # Only pairings that actually applied consumed anything. A skipped one left its
        # target in the pool, so reset must keep rebuilding that one.
        self._plando_consumed_targets = frozenset(applied_targets)
        self._plando_orphan_targets = tuple(
            candidate for candidate in orphan_candidates if candidate.name not in applied_targets)

        # Remove forced entrances from er_entrances so the retry loop doesn't reset them
        self.er_entrances = [
            (ent, vreg) for ent, vreg in self.er_entrances
            if ent.name not in connected_exit_names
        ]

    def _reconnect_ut_entrances(self):
        """Reconnect ER entrances from slot data for Universal Tracker.

        When UT's `enforce_deferred_connections` is anything other than "off",
        we leave entrances unconnected and stash their intended targets so
        `reconnect_found_entrances` can wire them in as the player discovers
        each warp.
        """
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
                # For coupled two-way pairings, target_name is the partner
                # connection: the door the player arrives at, whose own pairing
                # leads back here. That is the entrance to open for the walk-back,
                # not the vanilla string-reverse of source_name.
                if not target_name.endswith(" (one-way target)"):
                    self._deferred_entrance_partners[source_name] = target_name
            else:
                source = self.multiworld.get_entrance(source_name, self.player)
                if source is not None:
                    source.connect(self.get_region(target_region_name))
        self.er_pairings = [(s, t) for s, t in pairings]

    def reconnect_found_entrances(self, key: str, value) -> None:
        """Universal Tracker callback. Called whenever the data-storage key
        named by `found_entrances_datastorage_key` updates. `value` is the
        full list of discovered warp ids.

        Under coupled ER, traversing one direction also connects the partner
        entrance the player arrived at, so they can walk back the way they
        came."""
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
