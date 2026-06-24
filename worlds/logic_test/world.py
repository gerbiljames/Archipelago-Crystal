"""Logic Test: a generic logic-leak tester.

Add this world as one extra slot alongside ONE OR MORE games-under-test. During
generation it generates all the under-test slots together as one nested
multiworld, reads their OVERALL (cross-game) sphere structure, then builds itself
as a linear chain of gated spheres matching it:

* ALL of the under-test games' (networkable) items are pulled OUT and locked into
  this world's own sphere locations (each still owned by its original game).
* In their place, every under-test location receives a ``KEY_i`` macguffin,
  ``N_i`` of them, where ``N_i`` is the number of items in overall sphere ``i``.
* Sphere ``i`` here only opens once this slot has received ``N_i`` copies of
  ``KEY_i``, which releases all of sphere ``i``'s original items.

Play is forced into lock-step with the intended overall spheres. Every check
matters: to open sphere ``i`` you must collect every ``KEY_i``, i.e. reach every
location the model places in sphere ``i`` (across all games). A logic leak (an
access rule looser in the model than the real game) shows up as a hard stall: a
``KEY_i`` the model says is reachable but isn't, so the next sphere never opens.

Setup: add one Logic Test slot plus one or more games-under-test. Slot order does
not matter; the Logic Test reproduces each under-test game's RNG from its slot
number, so the YAMLs can be in any order.
"""

from collections import defaultdict, deque

from BaseClasses import Item, ItemClassification, Location, Region
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, Type, components, launch_subprocess

from .options import LogicTestOptions
from .pass_a import compute_spheres, run_under_test, under_test_rng_seed

MAX_SPHERES = 512
MAX_LOCATIONS = 200_000
FILLER_NAME = "Logic Test Filler"


def _launch_client():
    from .client import launch
    launch_subprocess(launch, name="LogicTestClient")


components.append(Component("Logic Test Client", func=_launch_client, component_type=Type.CLIENT))


class LogicTestWeb(WebWorld):
    tutorials = []


class LogicTestWorld(World):
    """A diagnostic slot that reproduces another game's spheres to surface logic leaks."""

    game = "Logic Test"
    options_dataclass = LogicTestOptions
    options: LogicTestOptions
    web = LogicTestWeb()

    # Fixed pools, frozen at import. Only a per-seed prefix is actually used.
    # IDs start at 1 (AutoWorldRegister drops id 0 and treats it as an event).
    item_name_to_id = {**{f"KEY_{i}": i for i in range(1, MAX_SPHERES + 1)},
                       FILLER_NAME: MAX_SPHERES + 1}
    location_name_to_id = {f"TestLoc_{i}": i for i in range(1, MAX_LOCATIONS + 1)}

    def generate_early(self) -> None:
        others = sorted(p for p in self.multiworld.player_ids if p != self.player)
        if not others:
            raise Exception("Logic Test requires at least one other player (a world under test).")
        ut_worlds = [self.multiworld.worlds[p] for p in others]
        for w in ut_worlds:
            if w.game == self.game:
                raise Exception("Logic Test cannot be used alongside another Logic Test slot.")
            if w.options.item_links.value:
                raise Exception(f"Logic Test does not support item_links in under-test slots "
                                f"(player {w.player}): all items are relocated, so links can't apply.")

        # nested player k (1..N) corresponds to outer under-test player others[k-1]
        nested_to_outer = {k: w.player for k, w in enumerate(ut_worlds, 1)}
        nested = run_under_test(ut_worlds, self.multiworld.seed)
        raw = compute_spheres(nested, count_events=bool(self.options.count_events))
        # translate nested player numbers back to outer slots
        # records: (loc_name, loc_outer_player, item_name, item_outer_player)
        self.spheres = [
            [(loc_name, nested_to_outer[loc_np], item_name, nested_to_outer[item_np])
             for (loc_name, loc_np, item_name, item_np) in sphere]
            for sphere in raw
        ]

        if len(self.spheres) > MAX_SPHERES:
            raise Exception(f"Logic Test: under-test seed has {len(self.spheres)} spheres, exceeding "
                            f"MAX_SPHERES={MAX_SPHERES}. Raise the limit in worlds/logic_test.")
        total = sum(len(s) for s in self.spheres)
        if total > MAX_LOCATIONS:
            raise Exception(f"Logic Test: under-test seed has {total} networkable items, exceeding "
                            f"MAX_LOCATIONS={MAX_LOCATIONS}. Raise the limit in worlds/logic_test.")

    def create_regions(self) -> None:
        p = self.player
        mw = self.multiworld
        menu = Region("Menu", p, mw)
        mw.regions.append(menu)

        self.sphere_locations = []  # list of list[Location], parallel to self.spheres
        prev = menu
        loc_index = 0
        for i, sphere in enumerate(self.spheres, start=1):
            region = Region(f"Sphere {i}", p, mw)
            mw.regions.append(region)
            locs = []
            for _ in sphere:
                loc_index += 1
                name = f"TestLoc_{loc_index}"
                loc = Location(p, name, self.location_name_to_id[name], region)
                region.locations.append(loc)
                locs.append(loc)
            self.sphere_locations.append(locs)

            key_name = f"KEY_{i}"
            need = len(sphere)
            prev.connect(
                region, f"To Sphere {i}",
                lambda state, k=key_name, c=need, pl=p: state.has(k, pl, c),
            )
            prev = region

        self.last_region_name = prev.name

    def create_items(self) -> None:
        # This world contributes nothing to the item pool: every sphere location is
        # pre-locked with an under-test item in pre_fill, and the KEY tokens are
        # locked directly into under-test locations.
        pass

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = \
            lambda state, r=self.last_region_name, p=self.player: state.can_reach_region(r, p)

    def pre_fill(self) -> None:
        mw = self.multiworld

        # Relocate the outer pool's actual items into our sphere locations and drop
        # a KEY at each under-test location. Match each record by exact name first,
        # then fill the rest from leftover pool items, so any divergence between the
        # nested and outer pools (non-deterministic generation) is tolerated.
        by_name = defaultdict(lambda: defaultdict(deque))
        for item in mw.itempool:
            by_name[item.player][item.name].append(item)

        # flatten: (logic_test_location, ut_loc_name, ut_loc_player, item_player, item_name, key_name)
        targets = []
        for i, sphere in enumerate(self.spheres, start=1):
            key_name = f"KEY_{i}"
            locs = self.sphere_locations[i - 1]
            for j, (loc_name, loc_player, item_name, item_player) in enumerate(sphere):
                targets.append((locs[j], loc_name, loc_player, item_player, item_name, key_name))

        assigned = [None] * len(targets)
        for idx, (_lt, _ln, _lp, item_player, item_name, _key) in enumerate(targets):
            queue = by_name[item_player].get(item_name)
            if queue:
                assigned[idx] = queue.popleft()

        leftover = defaultdict(deque)
        for player, names in by_name.items():
            for queue in names.values():
                leftover[player].extend(queue)
        for idx, (_lt, _ln, _lp, item_player, _name, _key) in enumerate(targets):
            if assigned[idx] is None and leftover[item_player]:
                assigned[idx] = leftover[item_player].popleft()

        relocated = []
        for idx, (lt_loc, loc_name, loc_player, item_player, _name, key_name) in enumerate(targets):
            item = assigned[idx]
            if item is None:
                raise Exception(f"Logic Test: not enough items in player {item_player}'s pool to "
                                f"relocate; the nested and outer generations produced different counts.")
            ut_loc = mw.get_location(loc_name, loc_player)
            if ut_loc.item is not None:
                raise Exception(f"Logic Test: under-test location '{loc_name}' was already filled "
                                f"before pre_fill; cannot place {key_name}.")
            ut_loc.place_locked_item(self.create_item(key_name))
            lt_loc.place_locked_item(item)
            relocated.append(item)

        relocated_ids = {id(item) for item in relocated}
        mw.itempool[:] = [item for item in mw.itempool if id(item) not in relocated_ids]

    def create_item(self, name: str) -> Item:
        classification = ItemClassification.progression if name.startswith("KEY_") \
            else ItemClassification.filler
        return Item(name, classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return FILLER_NAME

    def fill_slot_data(self):
        return {
            "spheres": [
                {
                    "key_item": f"KEY_{i}",
                    "key_id": self.item_name_to_id[f"KEY_{i}"],
                    "required": len(sphere),
                    "locations": [loc.address for loc in self.sphere_locations[i - 1]],
                }
                for i, sphere in enumerate(self.spheres, start=1)
            ]
        }
