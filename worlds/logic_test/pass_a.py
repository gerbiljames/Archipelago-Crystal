"""Pass A: generate the under-test slots together and read their overall spheres.

The Logic Test world calls :func:`run_under_test` during its own ``generate_early``
to produce a faithful generation of ALL the under-test games together (one nested
multiworld, same options, same per-game seeds), then :func:`compute_spheres` to
read the overall (cross-game) sphere structure the Logic Test enforces.

Determinism: a world seeds ``self.random = Random(multiworld.random.getrandbits(64))``
in ``World.__init__``, drawn from the seed stream in player order. So an under-test
world at outer player ``p`` got the p-th draw. :func:`under_test_rng_seed`
reproduces each value and :func:`run_under_test` forces it onto the matching nested
world, so every under-test structure (including entrance randomization) matches the
outer slots regardless of slot order; the nested fill then yields the overall
spheres.
"""

import copy
import logging
import random
from argparse import Namespace
from random import Random


def under_test_rng_seed(multiworld_seed, ut_player):
    """Reproduce the 64-bit value the under-test world seeded ``self.random`` with.

    Worlds draw their seed from ``multiworld.random.getrandbits(64)`` in player
    order, from a stream seeded with the multiworld seed, so the world at player
    ``ut_player`` got the ut_player-th draw.
    """
    rng = random.Random(multiworld_seed)
    value = 0
    for _ in range(ut_player):
        value = rng.getrandbits(64)
    return value


def run_under_test(ut_worlds, multiworld_seed):
    """Run a faithful generation of all under-test games together; return the
    fully-filled nested MultiWorld.

    ``ut_worlds`` are the outer under-test World objects, in the order they should
    occupy nested players 1..N. Each game's option values are deep-copied (so the
    nested run can mutate them freely) and its ``self.random`` is forced to the
    value it used in the outer multiworld (derived from its outer slot number), so
    the nested structures match the outer slots no matter their player numbers.
    Drives the real pipeline via ``Main.main`` with ``skip_output``.
    """
    from Main import main as ERmain

    # nested player k -> the seed the outer under-test world actually used
    seed_map = {k: under_test_rng_seed(multiworld_seed, w.player)
                for k, w in enumerate(ut_worlds, 1)}

    args = Namespace()
    for k, w in enumerate(ut_worlds, 1):
        for option_key in type(w.options).type_hints:
            values = getattr(args, option_key, {})
            values[k] = copy.deepcopy(getattr(w.options, option_key))
            setattr(args, option_key, values)

    count = len(ut_worlds)
    args.multi = count
    args.game = {k: w.game for k, w in enumerate(ut_worlds, 1)}
    args.name = {k: f"PassA{k}" for k in range(1, count + 1)}
    args.sprite = {k: None for k in range(1, count + 1)}
    args.sprite_pool = {k: None for k in range(1, count + 1)}
    args.plando = ut_worlds[0].multiworld.plando_options
    args.race = False
    args.outputname = None
    args.outputpath = None
    args.skip_output = True
    args.skip_prog_balancing = True
    args.spoiler = 0
    args.spoiler_only = False
    args.csv_output = False

    # Force each nested under-test world to its outer slot's RNG seed. Scoped to
    # this call; the outer world objects already exist and aren't reconstructed.
    classes = {type(w) for w in ut_worlds}
    originals = {cls: cls.__init__ for cls in classes}

    def make_seeded(original_init):
        def seeded_init(world_self, multiworld, player):
            original_init(world_self, multiworld, player)
            # Only force the real under-test players; item-link groups and other
            # synthetic players (constructed with higher ids) keep their own RNG.
            if player in seed_map:
                world_self.random = Random(seed_map[player])
                multiworld.per_slot_randoms[player] = world_self.random
        return seeded_init

    root = logging.getLogger()
    prior_level = root.level
    root.setLevel(logging.WARNING)
    for cls in classes:
        cls.__init__ = make_seeded(originals[cls])
    try:
        return ERmain(args, seed=multiworld_seed)
    finally:
        for cls, original_init in originals.items():
            cls.__init__ = original_init
        root.setLevel(prior_level)


def compute_spheres(multiworld, count_events=True):
    """Return the overall sphere structure as a list (one entry per sphere that
    contains networkable items) of ``[(loc_name, loc_player, item_name, item_player), ...]``.

    Records every networkable item across all players: a real ``code`` at a real
    (addressed) location. The location owner and item owner can differ (cross-game
    placement). Two kinds of placement are never recorded (so they're left in the
    under-test games, like normal play): events (``code``/``address`` of ``None``)
    can't be sent over the network, and ``locked`` locations are fixed placements
    the game requires to stay put. Both still advance state for sphere ordering.

    ``count_events`` controls whether events cause a sphere boundary:

    * True (default): each reachability wave collects everything in it (events
      included), so an item unlocked by an event that became reachable in that
      wave lands in the NEXT sphere; events create boundaries, finer spheres.
    * False: use the canonical ``MultiWorld.get_sendable_spheres``, which culls
      every reachable event before taking each sphere of sendable locations.
      Events are still collected in dependency order, so they never create a
      boundary; coarser spheres.
    """
    from BaseClasses import CollectionState

    def record(loc):
        return (loc.name, loc.player, loc.item.name, loc.item.player)

    if not count_events:
        spheres = []
        for sphere in multiworld.get_sendable_spheres():
            if not sphere:
                break  # empty set precedes the unreachable-locations set; stop here
            rec = [record(loc) for loc in sphere if not loc.locked]
            if rec:
                spheres.append(rec)
        return spheres

    state = CollectionState(multiworld)
    locations = set(multiworld.get_filled_locations())
    spheres = []
    while locations:
        sphere = {loc for loc in locations if loc.can_reach(state)}
        if not sphere:
            break  # remaining locations unreachable; should not happen on a valid seed
        rec = [record(loc) for loc in sphere
               if loc.item.code is not None and loc.address is not None and not loc.locked]
        if rec:
            spheres.append(rec)
        for loc in sphere:
            state.collect(loc.item, True, loc)
        locations -= sphere
    return spheres
