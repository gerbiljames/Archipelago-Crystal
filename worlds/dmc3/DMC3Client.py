import asyncio
import functools
from typing import List, Any, Iterable

import websockets

import Utils
from CommonClient import CommonContext, gui_enabled, ClientCommandProcessor, logger, get_base_parser
from MultiServer import Endpoint
from NetUtils import decode, encode, NetworkItem
from . import styles
from .Items import key_items, dmc3_items
from .Skills import combined_upgrades

DEBUG = False


class DMC3CommandProcessor(ClientCommandProcessor):
    def _cmd_dmc3(self):
        """Check DMC3 Connection State"""
        if isinstance(self.ctx, DMC3Context):
            if not self.ctx.is_proxy_connected():
                logger.info(f"DMC3 Status: Not connected")
            else:
                logger.info(f"DMC3 Status: Connected")

    def _cmd_deathlink(self):
        """Toggles deathlink"""
        if "DeathLink" in self.ctx.tags:
            self.output(f"Death Link turned off")
            self.ctx.update_death_link(False)
        else:
            self.output(f"Death Link turned on")
            self.ctx.update_death_link(True)



class DMC3Context(CommonContext):
    command_processor = DMC3CommandProcessor
    game = "Devil May Cry 3"
    item_name_to_id = {name: data.code for name, data in (dmc3_items | combined_upgrades | styles).items() if
                       data.code is not None}
    item_id_to_name = {code: name for name, code in item_name_to_id.items()}

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.proxy = None
        self.proxy_task = None
        self.endpoint = None
        self.items_handling = 0b111
        self.room_info = None
        self.connected_msg = None
        self.game_connected = False
        self.awaiting_info = False
        self.inventory: List[Any] = []
        self.server_msgs: List[Any] = []
        self.blue_orbs = 0
        self.purple_orbs = 0
        # self.tags.add("DeathLink")

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

    def update_items(self):
        if not self.is_connected():
            return

        self.server_msgs.append(encode([{"cmd": "ReceivedItems", "index": 0, "items": self.inventory}]))

    def on_package(self, cmd: str, args: dict):
        match cmd:
            case "Connected":
                if DEBUG:
                    print(args)
                self.connected_msg = encode([args])
                if self.awaiting_info:
                    self.server_msgs.append(self.room_info)
                    self.update_items()
                    self.update_death_link(args.get('slot_data', None).get("DeathLink"))
                    self.awaiting_info = False
            case "RoomUpdate":
                self.server_msgs.append(encode([args]))
            case "ReceivedItems":
                if args["index"] == 0:
                    self.inventory.clear()
                    self.blue_orbs = 0
                    self.purple_orbs = 0
                    if gui_enabled:
                        self.ui.checklist = {key: False for key in key_items}

                for item in args["items"]:
                    self.inventory.append(NetworkItem(*item))
                    if NetworkItem(*item).item == dmc3_items.get("Blue Orb").code:
                        self.blue_orbs += 1
                    if NetworkItem(*item).item == dmc3_items.get("Purple Orb").code:
                        self.purple_orbs += 1
                    if gui_enabled:
                        self.ui.checklist[self.item_id_to_name[NetworkItem(*item).item]] = True

                if gui_enabled:
                    self.ui.update_checklist(self.blue_orbs, self.purple_orbs)  # This is fine
                self.server_msgs.append(encode([args]))
            case "RoomInfo":
                self.seed_name = args["seed_name"]
                self.room_info = encode([args])
            case "DeathLink":
                logger.log("DeathLink sent to DMC3!")
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
                        # Proxy is connecting, make sure it is valid
                        if msg["game"] != ctx.game:
                            logger.info(f"Aborting proxy connection: game is not {ctx.game}")
                            await ctx.disconnect_proxy()
                            break

                        if ctx.seed_name:
                            seed_name = msg.get("seed_name", "")
                            if seed_name != "" and seed_name != ctx.seed_name:
                                logger.info("Aborting proxy connection: seed mismatch from save file")
                                logger.info(f"Expected: {ctx.seed_name}, got: {seed_name}")
                                text = encode([{"cmd": "PrintJSON",
                                                "data": [{"text": "Connection aborted - save file to seed mismatch"}]}])
                                await ctx.send_message_to_game(text)
                                await ctx.disconnect_proxy()
                                break

                        if ctx.connected_msg and ctx.is_connected():
                            await ctx.send_message_to_game(ctx.connected_msg)
                            ctx.update_items()
                        continue

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
        logger.info("Starting DMC3 Proxy Client")
        ctx.proxy = websockets.serve(functools.partial(proxy, ctx=ctx),
                                     host="localhost", port=21705, ping_timeout=999999, ping_interval=999999)
        ctx.proxy_task = asyncio.create_task(proxy_loop(ctx), name="ProxyLoop")

        if gui_enabled:
            from .DMC3ClientGui import start_gui
            start_gui(ctx)
        ctx.run_cli()

        await ctx.proxy
        await ctx.proxy_task
        await ctx.exit_event.wait()

    Utils.init_logging("DMC3Client")

    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
