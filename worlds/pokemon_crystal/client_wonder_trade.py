"""Wonder Trade: swaps a party Pokemon with another player via a shared server-side pool."""

import asyncio
import copy
import random
import time
import uuid
from typing import TYPE_CHECKING

import Utils
import worlds._bizhawk as bizhawk
from .data import data
from .util_wonder_trade import pokemon_data_to_json, json_to_pokemon_data, trade_is_eligible

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

BASE_COOLDOWN_MS = 5000
MAX_COOLDOWN_MS = 60000


def _pool_key(ctx: "BizHawkClientContext") -> str:
    return f"pokemon_wonder_trades_{ctx.team}"


# send_msgs silently drops messages while disconnected.
def _server_connected(ctx: "BizHawkClientContext") -> bool:
    return bool(ctx.server and ctx.server.socket.open and not ctx.server.socket.closed)


async def _update_pool(ctx: "BizHawkClientContext", operations: list[dict], **extra) -> None:
    await ctx.send_msgs([{
        "cmd": "Set",
        "key": _pool_key(ctx),
        "default": {"_lock": 0},
        "operations": operations,
        **extra,
    }])


class WonderTradeMixin:
    """Wonder Trade state and handlers, mixed into the Bizhawk client."""

    wonder_trade_update_event: asyncio.Event
    latest_wonder_trade_reply: dict
    wonder_trade_cooldown: int
    wonder_trade_cooldown_timer: int
    queued_received_trade: str | None
    wonder_trade_in_flight: bool
    wonder_trade_unmarked_buffer: bytes | None
    wonder_trade_send_token: object | None
    wonder_trade_receiving: bool

    def initialize_wonder_trade(self) -> None:
        self.wonder_trade_update_event = asyncio.Event()
        self.latest_wonder_trade_reply = {}
        self.wonder_trade_cooldown = BASE_COOLDOWN_MS
        self.wonder_trade_cooldown_timer = 0
        self.queued_received_trade = None
        self.wonder_trade_in_flight = False
        self.wonder_trade_unmarked_buffer = None
        self.wonder_trade_send_token = None
        self.wonder_trade_receiving = False

    async def handle_wonder_trade(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger

        magic_addr = data.sram_addresses["sArchipelagoWonderTradeMagic"]
        status_addr = data.sram_addresses["sArchipelagoWonderTradeStatus"]
        send_addr = data.sram_addresses["sArchipelagoWonderTradeSendBuffer"]
        player_id_addr = data.ram_addresses["wPlayerID"]

        try:
            read_result = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (magic_addr, 3, "CartRAM"),
                    (status_addr, 1, "CartRAM"),
                    (send_addr, 70, "CartRAM"),
                    (player_id_addr, 2, "WRAM"),
                ],
            )
        except bizhawk.RequestFailedError:
            return

        # Fresh cartridges have garbage SRAM until the ROM writes the magic.
        if read_result[0] != b"\xa5\x5a\xc3":
            return

        status = read_result[1][0]
        send_blob = read_result[2]
        # Keyed by trainer ID, not slot, so saves sharing a slot can trade but not with themselves.
        own_tid = int.from_bytes(read_result[3], "big")

        # READY (1) until a partner mon is delivered (INCOMING, 3); in-flight is client-side only.
        if status != 1:
            return

        if self.wonder_trade_unmarked_buffer == bytes(send_blob):
            await self._mark_posted(ctx, self.wonder_trade_unmarked_buffer)
            return

        # The ROM never reads the send buffer back, so a zeroed species marks it as already posted.
        if not self.wonder_trade_in_flight and send_blob[0] == 0:
            self.wonder_trade_in_flight = True

        if not self.wonder_trade_in_flight:
            party_mon = bytes(send_blob[0:48])
            nickname = bytes(send_blob[48:59])
            ot = bytes(send_blob[59:70])
            trainer_id = int.from_bytes(party_mon[6:8], "big")
            player_female = False
            try:
                gender_read = await bizhawk.read(
                    ctx.bizhawk_ctx, [(data.ram_addresses["wPlayerGender"], 1, "WRAM")]
                )
                player_female = bool(gender_read[0][0] & 1)
            except (KeyError, bizhawk.RequestFailedError):
                pass

            json_blob = pokemon_data_to_json(party_mon, nickname, ot, trainer_id, player_female)
            self.wonder_trade_in_flight = True
            token = self.wonder_trade_send_token = object()
            Utils.async_start(self.wonder_trade_send(ctx, json_blob, own_tid, bytes(send_blob), token))
            return

        if self.queued_received_trade is not None:
            decoded = json_to_pokemon_data(self.queued_received_trade)
            await bizhawk.write(ctx.bizhawk_ctx, [
                (data.sram_addresses["sArchipelagoWonderTradeRecvBuffer"], decoded["party_mon"], "CartRAM"),
                (data.sram_addresses["sArchipelagoWonderTradeRecvNick"], decoded["nickname"], "CartRAM"),
                (data.sram_addresses["sArchipelagoWonderTradeRecvOT"], decoded["ot"], "CartRAM"),
                (status_addr, [3], "CartRAM"),
            ])
            logger.info("Wonder trade received!")
            self.queued_received_trade = None
            self.wonder_trade_in_flight = False
            return

        if self.wonder_trade_receiving:
            return

        pool_key = _pool_key(ctx)
        if self.wonder_trade_cooldown_timer <= 0 and pool_key in ctx.stored_data:
            pool = ctx.stored_data[pool_key]
            if not isinstance(pool, dict):
                return
            if any(trade_is_eligible(item, own_tid) for key, item in pool.items() if key != "_lock"):
                self.wonder_trade_receiving = True
                Utils.async_start(self._receive_in_background(ctx, own_tid))
        else:
            self.wonder_trade_cooldown_timer -= int(ctx.watcher_timeout * 1000)

    async def _receive_in_background(self, ctx: "BizHawkClientContext", own_tid: int) -> None:
        trade = None
        try:
            trade = await self.wonder_trade_receive(ctx, own_tid)
        finally:
            if trade is None:
                self.wonder_trade_cooldown_timer = self.wonder_trade_cooldown
                self._back_off()
            else:
                self.queued_received_trade = trade
                self.wonder_trade_cooldown = BASE_COOLDOWN_MS
            self.wonder_trade_receiving = False

    def _back_off(self) -> None:
        self.wonder_trade_cooldown = min(self.wonder_trade_cooldown * 2, MAX_COOLDOWN_MS)
        self.wonder_trade_cooldown += random.randrange(0, 500)

    async def wonder_trade_acquire(self, ctx: "BizHawkClientContext", keep_trying: bool = False) -> dict | None:
        while not ctx.exit_event.is_set():
            lock = time.time_ns() // 1_000_000
            message_uuid = str(uuid.uuid4())
            self.wonder_trade_update_event.clear()
            await _update_pool(ctx, [{"operation": "update", "value": {"_lock": lock}}],
                               want_reply=True, uuid=message_uuid)
            try:
                await asyncio.wait_for(self.wonder_trade_update_event.wait(), 5)
            except asyncio.TimeoutError:
                if not keep_trying:
                    return None
                continue

            reply = copy.deepcopy(self.latest_wonder_trade_reply)

            value = reply.get("value")
            if reply.get("uuid") != message_uuid or not isinstance(value, dict) or value.get("_lock") != lock:
                if not keep_trying:
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown / 1000)
                continue

            original_lock = (reply.get("original_value") or {}).get("_lock", 0)
            if isinstance(original_lock, int) and lock - original_lock < 5000:
                self._back_off()
                if not keep_trying:
                    self.wonder_trade_cooldown_timer = self.wonder_trade_cooldown
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown / 1000)
                continue

            self.wonder_trade_cooldown = BASE_COOLDOWN_MS
            return reply

    async def wonder_trade_send(self, ctx: "BizHawkClientContext", blob: str, own_tid: int,
                                send_buffer: bytes, token: object) -> None:
        from CommonClient import logger

        posted = False
        try:
            reply = await self.wonder_trade_acquire(ctx, keep_trying=True)
            if reply is None:
                return

            slot = 0
            while str(slot) in reply["value"]:
                slot += 1

            if not _server_connected(ctx):
                return
            await _update_pool(ctx, [{"operation": "update", "value": {"_lock": 0, str(slot): (own_tid, blob)}}])
            posted = True
            logger.info("Wonder trade sent! Waiting for a partner.")
            # Retried from the watcher if this write fails.
            self.wonder_trade_unmarked_buffer = send_buffer
            try:
                await self._mark_posted(ctx, send_buffer)
            except bizhawk.RequestFailedError:
                pass
        finally:
            if not posted and self.wonder_trade_send_token is token:
                self.wonder_trade_in_flight = False

    async def _mark_posted(self, ctx: "BizHawkClientContext", send_buffer: bytes) -> None:
        send_addr = data.sram_addresses["sArchipelagoWonderTradeSendBuffer"]
        if await bizhawk.guarded_write(
            ctx.bizhawk_ctx,
            [(send_addr, [0], "CartRAM")],
            [(data.sram_addresses["sArchipelagoWonderTradeStatus"], [1], "CartRAM"),
             (send_addr, send_buffer, "CartRAM")],
        ):
            self.wonder_trade_unmarked_buffer = None

    async def wonder_trade_receive(self, ctx: "BizHawkClientContext", own_tid: int) -> str | None:
        reply = await self.wonder_trade_acquire(ctx)
        if reply is None:
            return None

        candidate_slots = [slot for slot, item in reply["value"].items()
                           if slot != "_lock" and trade_is_eligible(item, own_tid)]
        unlock = {"operation": "update", "value": {"_lock": 0}}
        if not candidate_slots:
            await _update_pool(ctx, [unlock])
            return None

        chosen = str(random.choice(candidate_slots))
        if not _server_connected(ctx):
            return None
        await _update_pool(ctx, [unlock, {"operation": "pop", "value": chosen}])
        return reply["value"][chosen][1]
