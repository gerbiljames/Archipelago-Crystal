# Logic Test: logic-leak tester

Logic Test is a diagnostic slot you add **alongside one or more games-under-test**
to surface logic leaks, places where the generator's logic model is looser than
the real game (an access rule that says a location is reachable when it isn't).

## How it works

With `<game(s)> + Logic Test`, the Logic Test:

1. Generates all the under-test slots **together** as one nested multiworld (same
   options, same per-game seeds) and reads their **overall** (cross-game) spheres,
   i.e. which items become reachable, in what order, across all of them.
2. Pulls **all of those games' items** out and locks them inside itself (each
   recreated for its original owner), split into gated **spheres**.
3. Replaces every under-test location with a `KEY_i` macguffin, `N_i` of them in
   sphere `i`.
4. Gates Logic Test sphere `i` behind receiving `N_i` copies of `KEY_i`, which
   releases all of sphere `i`'s original items.

Play is forced into lock-step with the intended overall spheres, and **every
check matters**: to open sphere `i` you must collect every `KEY_i` (across all
games). If a rule leaks, a `KEY_i` the model thinks is reachable won't be
in-game, the next sphere never opens, and you hard-stall at the leaked point.

## Setup

1. Add one Logic Test slot plus one or more games-under-test. Slot order does not
   matter.
2. Generate normally (`python Generate.py`) and host the resulting seed.

## Options

- **`count_events`** (default off): whether in-game events cause a sphere
  boundary.
  - **Off** (default): events never create a boundary (the canonical
    sendable-sphere grouping), so spheres are coarser. Events are still collected
    in dependency order, so this stays solvable.
  - **On**: an item unlocked by an event creates a boundary, so spheres are
    finer-grained and faithful to real play order.

## Playing

- Play player 1 with its normal client/emulator.
- Run the Logic Test client (Launcher → **Logic Test Client**, or
  `python -m worlds.logic_test.client --name "<logic test slot>" <server>`).
- Use the **Logic Test** tab: it shows the current sphere, how many `KEY`s you
  have vs. need, and an **Open Sphere** button that lights up once you have them
  all. (The `/status` and `/proceed` console commands do the same.) Opening a
  sphere releases that sphere's original items back to player 1.

A correct game flows sphere by sphere to completion. A leak = `/proceed` never
becomes available because a key is unreachable in-game.

> Only real, networkable progression is gated. Event-style logic (gym clears,
> flags) stays in the under-test game and resolves through normal play.

## Limitations

The Logic Test relocates the under-test game's progression out of the main fill. If a
game places **real (networked) progression items in its own `pre_fill`** (some
worlds lock dungeon items or boss rewards there), generation will fail loudly,
since the Logic Test can't relocate an item that's already locked. Games that
place only *events* in `pre_fill` (the common case) are unaffected.
