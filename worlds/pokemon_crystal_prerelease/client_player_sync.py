"""Co-op player visibility: shows the partner sharing this slot as a second overworld sprite.

Position is broadcast with Bounce rather than data storage - it is ephemeral, worthless a
second later, and would otherwise churn a stored key several times a second. Bounces are
scoped to our own slot, so only co-op partners ever see them.

The ROM walks the ghost toward the reported tile and dresses it in the partner's form, so
this only has to report position, facing and player state.

Traffic is kept off the server unless it can actually be seen: the movement feed only runs
while a partner is known to be on the same map, and otherwise drops to a slow presence
beacon that exists purely so partners can find each other.
"""

import asyncio
import time
from typing import TYPE_CHECKING, NamedTuple, Optional

import worlds._bizhawk as bizhawk
from .data import data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

GHOST_KEY = "apGhost"

# game_watcher runs every 0.5s, which is four walking tiles - far too coarse for a
# position feed. This runs on its own task instead, doing nothing but the position
# read and the ghost write. bizhawk serialises requests behind a lock, so sharing
# the connection with game_watcher is safe.
POLL_INTERVAL = 0.1

POSITION_ADDR = data.ram_addresses["wMapGroup"]  # group, number, wYCoord, wXCoord
POSITION_SIZE = 4
FACING_ADDR = data.ram_addresses["wPlayerDirection"]
STATE_ADDR = data.ram_addresses["wPlayerState"]
GENDER_ADDR = data.ram_addresses["wPlayerGender"]
SAFE_WRITE_ADDR = data.ram_addresses["wArchipelagoSafeWrite"]

# A partner is dropped once their last report is this old, so a disconnected client's
# ghost does not stand around forever.
GHOST_TIMEOUT = 5.0

# Sends are throttled to actual movement, so a standing player would otherwise fall out
# of GHOST_TIMEOUT and vanish from their partner's screen. Resend while idle to keep the
# freshness check meaning "still connected" rather than "still walking".
HEARTBEAT_INTERVAL = 1.5

# Nobody can see us unless a partner is on our map, so the movement feed is only worth
# sending then. The rest of the time we emit this far slower beacon, which is what lets a
# partner notice us when they do walk in. Keep it under GHOST_TIMEOUT so the moment they
# arrive their client already holds a fresh report of us.
PRESENCE_INTERVAL = 4.0

GHOST_FLAG_ACTIVE = 0b00000001
GHOST_STATE_FEMALE = 0b10000000
GHOST_STATE_MASK = 0b01111111

GHOST_FLAGS_ADDR = data.ram_addresses["wArchipelagoGhostFlags"]
GHOST_BLOCK_SIZE = 7


class GhostState(NamedTuple):
    tracker_slot: int
    map_group: int
    map_number: int
    x: int
    y: int
    facing: int
    state: int
    received: float

    def is_fresh(self, now: float) -> bool:
        return now - self.received < GHOST_TIMEOUT


def build_ghost_payload(tracker_slot: int, map_group: int, map_number: int,
                        x: int, y: int, facing: int, state: int = 0) -> dict:
    return {"s": tracker_slot, "g": map_group, "n": map_number,
            "x": x, "y": y, "f": facing, "t": state}


def parse_ghost_payload(args: dict, own_tracker_slot: int) -> Optional[GhostState]:
    """Decode an incoming ghost bounce, or None if it is malformed or our own."""
    payload = (args.get("data") or {}).get(GHOST_KEY)
    if not isinstance(payload, dict):
        return None

    try:
        state = GhostState(
            tracker_slot=int(payload["s"]),
            map_group=int(payload["g"]),
            map_number=int(payload["n"]),
            x=int(payload["x"]),
            y=int(payload["y"]),
            facing=int(payload["f"]),
            state=int(payload.get("t", 0)) & 0xFF,
            received=time.time(),
        )
    except (KeyError, TypeError, ValueError):
        return None

    # Bounce echoes to every client on the slot, ourselves included.
    if state.tracker_slot == own_tracker_slot:
        return None
    # Tracker slot 0 means the player never picked one, so partners are indistinguishable.
    if state.tracker_slot == 0:
        return None
    # The ROM writes these into single bytes.
    if not all(0 <= v <= 0xFF for v in (state.map_group, state.map_number, state.x, state.y)):
        return None
    if not 0 <= state.facing <= 3:
        return None

    return state


def partner_on_map(state: Optional[GhostState], map_group: int, map_number: int,
                   now: float) -> bool:
    """Whether a partner is currently standing on the given map, per their last report."""
    if state is None or not state.is_fresh(now):
        return False
    return (state.map_group, state.map_number) == (map_group, map_number)


def ghost_block(state: Optional[GhostState], now: float) -> list[int]:
    """The 7 bytes at wArchipelagoGhostFlags for this partner state."""
    if state is None or not state.is_fresh(now):
        return [0] * GHOST_BLOCK_SIZE
    return [
        GHOST_FLAG_ACTIVE,
        state.map_group,
        state.map_number,
        state.x,
        state.y,
        state.facing,
        state.state,  # wPlayerState plus gender in the top bit
    ]


async def send_ghost_position(ctx: "BizHawkClientContext", tracker_slot: int, map_group: int,
                              map_number: int, x: int, y: int, facing: int,
                              state: int = 0) -> None:
    if ctx.slot is None or not tracker_slot:
        return
    await ctx.send_msgs([{
        "cmd": "Bounce",
        "slots": [ctx.slot],
        "data": {GHOST_KEY: build_ghost_payload(tracker_slot, map_group, map_number,
                                                x, y, facing, state)},
    }])


async def write_ghost_block(ctx: "BizHawkClientContext", state: Optional[GhostState], guard) -> None:
    await bizhawk.guarded_write(
        ctx.bizhawk_ctx,
        [(GHOST_FLAGS_ADDR, ghost_block(state, time.time()), "WRAM")],
        [guard],
    )


class PlayerSyncMixin:
    """Runs the position feed on its own task, away from the 0.5s game_watcher."""

    player_sync_task: Optional[asyncio.Task] = None

    def start_player_sync(self, ctx: "BizHawkClientContext") -> None:
        if self.player_sync_task is None or self.player_sync_task.done():
            self.player_sync_task = asyncio.create_task(self._player_sync_loop(ctx))

    def stop_player_sync(self) -> None:
        if self.player_sync_task is not None and not self.player_sync_task.done():
            self.player_sync_task.cancel()
        self.player_sync_task = None

    async def _player_sync_loop(self, ctx: "BizHawkClientContext") -> None:
        guard = (SAFE_WRITE_ADDR, [1], "WRAM")

        while not ctx.exit_event.is_set():
            await asyncio.sleep(POLL_INTERVAL)

            if ctx.server is None or ctx.server.socket.closed or ctx.slot is None:
                continue

            try:
                result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [(POSITION_ADDR, POSITION_SIZE, "WRAM"), (FACING_ADDR, 1, "WRAM"),
                     (STATE_ADDR, 1, "WRAM"), (GENDER_ADDR, 1, "WRAM")],
                    [guard],
                )
                if result is None:  # not in the overworld
                    continue

                position, facing_byte, state_byte, gender_byte = result
                map_group, map_number, y, x = (int(b) for b in position)
                facing = (facing_byte[0] >> 2) & 0b11

                # The ROM resolves this back to a sprite through the same
                # Chris/Kris tables the local player uses, so bike, surf and run
                # all come across without the client knowing any sprite ids.
                state = state_byte[0] & GHOST_STATE_MASK
                if gender_byte[0] & 1:
                    state |= GHOST_STATE_FEMALE

                tracker_slot = getattr(self, "local_tracker_slot", 0)
                if tracker_slot:
                    now = time.time()
                    current = (map_group, map_number, x, y, facing, state)
                    previous = getattr(self, "last_ghost_position", None)

                    # Only stream movement while a partner is actually on this map and
                    # able to see it. Otherwise fall back to the presence beacon: a map
                    # change goes out at once so an arriving partner is noticed straight
                    # away, and receiving their report is what promotes us back to
                    # streaming.
                    partner_here = partner_on_map(getattr(self, "remote_ghost", None),
                                                  map_group, map_number, now)
                    interval = HEARTBEAT_INTERVAL if partner_here else PRESENCE_INTERVAL

                    # Answer immediately the moment a partner turns up, rather than
                    # leaving them looking at a frozen ghost of us until our next beacon.
                    arrived = partner_here and not getattr(self, "partner_was_here", False)
                    self.partner_was_here = partner_here

                    map_changed = previous is None or previous[:2] != current[:2]
                    due = now - getattr(self, "last_ghost_sent", 0.0) >= interval

                    if map_changed or due or arrived or (partner_here and previous != current):
                        self.last_ghost_position = current
                        self.last_ghost_sent = now
                        await send_ghost_position(ctx, tracker_slot, map_group,
                                                  map_number, x, y, facing, state)

                await write_ghost_block(ctx, getattr(self, "remote_ghost", None), guard)
            except (bizhawk.RequestFailedError, bizhawk.NotConnectedError):
                continue  # game_watcher owns reconnection
            except asyncio.CancelledError:
                raise
