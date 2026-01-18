import asyncio
import functools
from typing import List, Any, Iterable

import websockets

import Utils
from CommonClient import CommonContext, gui_enabled, ClientCommandProcessor, logger, get_base_parser
from MultiServer import Endpoint
from NetUtils import decode, encode

DEBUG = False


class DMC3CommandProcessor(ClientCommandProcessor):
    def _cmd_dmc3(self):
        """Check DMC3 Connection State"""
        if isinstance(self.ctx, DMC3Context):
            if not self.ctx.is_proxy_connected():
                logger.info(f"DMC3 Status: Not connected")
            else:
                logger.info(f"DMC3 Status: Connected")

    def _cmd_floors_needed(self, new_floor: int):
        """Change how many BP floors are required to generate a hint Range: (1 to 10,000)"""
        if 0 < new_floor <= 10000:
            print(f"Floors needed is now {new_floor}")
            from . import DevilMayCry3World
            # TODO Saving new FPH isn't working
            DevilMayCry3World.settings.floors_per_hint = DevilMayCry3World.settings.FloorsPerHint(new_floor)
            self.ctx.on_package("Bounced", {"cmd": "Bounced", "data": {"floors_per_hint": new_floor}})
        else:
            pass


class DMC3Context(CommonContext):
    command_processor = DMC3CommandProcessor

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.proxy = None
        self.proxy_task = None
        self.endpoint = None
        self.items_handling = 0b000
        self.room_info = None
        self.connected_msg = None
        self.game_connected = False
        self.awaiting_info = False
        self.server_msgs: List[Any] = []
        self.want_slot_data = False
        self.tags = {"AP", "HintGame"}

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(DMC3Context, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    async def send_message_to_game(self, msgs: Iterable[dict]) -> bool:
        if not self.endpoint or not self.endpoint.socket.open or self.endpoint.socket.closed:
            return False

        if DEBUG:
            logger.info(f"Outgoing message: {msgs}")

        await self.endpoint.socket.send(msgs)
        return True

    async def disconnect_proxy(self):
        if self.endpoint and not self.endpoint.socket.closed:
            await self.endpoint.socket.close()
        if self.proxy_task is not None:
            await self.proxy_task

    async def disconnect(self, allow_autoreconnect: bool = False):
        print("Disconnected!")
        await super().disconnect(allow_autoreconnect)
        if self.endpoint and not self.endpoint.socket.closed:
            await self.endpoint.socket.close()

    def is_connected(self) -> bool:
        return self.server and self.server.socket.open

    def is_proxy_connected(self) -> bool:
        return self.endpoint and self.endpoint.socket.open

    def on_print_json(self, args: dict):
        self.server_msgs.append(encode([args]))

        if self.ui:
            self.ui.print_json(args["data"])
        else:
            text = self.jsontotextparser(args["data"])
            logger.info(text)

    def on_package(self, cmd: str, args: dict):
        match cmd:
            case "Connected":
                if DEBUG:
                    print(args)
                from . import DevilMayCry3World
                args["slot_data"] = {
                    "client_version": DevilMayCry3World.world_version,
                    "floors_per_hint": DevilMayCry3World.settings.floors_per_hint
                }
                self.connected_msg = encode([args])
                if self.awaiting_info:
                    self.server_msgs.append(self.room_info)
                    self.awaiting_info = False
            case "RoomUpdate":
                self.server_msgs.append(encode([args]))
            case "RoomInfo":
                self.seed_name = args["seed_name"]
                self.room_info = encode([args])
            case "Bounced":
                self.server_msgs.append(encode([args]))
            case _:
                if cmd != "PrintJSON":
                    self.server_msgs.append(encode([args]))


async def proxy(websocket, path: str = "/", ctx: DMC3Context = None):
    ctx.endpoint = Endpoint(websocket)
    try:
        await on_client_connected(ctx)

        if ctx.is_proxy_connected():
            async for data in websocket:
                if DEBUG:
                    logger.info(f"Incoming message: {data}")

                for msg in decode(data):
                    if msg["cmd"] == "Connect":
                        if ctx.connected_msg and ctx.is_connected():
                            await ctx.send_message_to_game(ctx.connected_msg)
                        continue

                    if msg["cmd"] == "ConnectUpdate":
                        ctx.tags = msg["tags"]

                    if not ctx.is_proxy_connected():
                        break

                    await ctx.send_msgs([msg])

    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logger.exception(e)
    finally:
        await ctx.disconnect_proxy()


async def on_client_connected(ctx: DMC3Context):
    if ctx.room_info and ctx.is_connected():
        await ctx.send_message_to_game(ctx.room_info)
    else:
        ctx.awaiting_info = True


async def proxy_loop(ctx: DMC3Context):
    try:
        while not ctx.exit_event.is_set():
            if len(ctx.server_msgs) > 0:
                for msg in ctx.server_msgs:
                    await ctx.send_message_to_game(msg)

                ctx.server_msgs.clear()
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.exception(e)
        logger.info("Aborting DMC3 Proxy Client due to errors")


def launch(*launch_args: str):
    async def main():
        parser = get_base_parser()
        args = parser.parse_args(launch_args)

        ctx = DMC3Context(args.connect, args.password)
        logger.info("Starting DMC3 Hint Proxy Client")
        ctx.proxy = websockets.serve(functools.partial(proxy, ctx=ctx),
                                     host="localhost", port=21705, ping_timeout=999999, ping_interval=999999)
        ctx.proxy_task = asyncio.create_task(proxy_loop(ctx), name="ProxyLoop")

        if gui_enabled:
            from .DMC3HintClientGui import start_gui
            start_gui(ctx)
        ctx.run_cli()

        await ctx.proxy
        await ctx.proxy_task
        await ctx.exit_event.wait()

    Utils.init_logging("DMC3HintClient")

    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
