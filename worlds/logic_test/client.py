"""Semi-automatic console client for the Logic Test slot.

Connects to the Logic Test slot, tracks received ``KEY_i`` tokens, and lets you open
the next sphere once you hold all of its required keys. Opening a sphere sends
that sphere's location checks, releasing the under-test items the Logic Test was
holding back to the under-test player.

The GUI adds a "Logic Test" tab with live per-sphere progress and an "Open
Sphere" button; the ``/status`` and ``/proceed`` console commands do the same.
"""

import asyncio

from CommonClient import (
    CommonContext,
    ClientCommandProcessor,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)
from Utils import async_start


class LogicTestCommandProcessor(ClientCommandProcessor):
    def _cmd_status(self) -> bool:
        """Show current sphere progress and key counts."""
        self.ctx.print_status()
        return True

    def _cmd_proceed(self) -> bool:
        """Open the next sphere if all of its required keys have been received."""
        async_start(self.ctx.proceed(), name="logic test proceed")
        return True


class LogicTestContext(CommonContext):
    command_processor = LogicTestCommandProcessor
    game = "Logic Test"
    items_handling = 0b111  # receive everything
    want_slot_data = True

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.spheres = []          # list of {key_item, key_id, required, locations}
        self.current_sphere = 0    # index of the next sphere to open

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            slot_data = args.get("slot_data") or {}
            self.spheres = slot_data.get("spheres", [])
            # Resume at the first sphere whose locations aren't all checked yet.
            self.current_sphere = 0
            for idx, sphere in enumerate(self.spheres):
                if all(loc in self.checked_locations for loc in sphere["locations"]):
                    self.current_sphere = idx + 1
                else:
                    break
            logger.info("Connected to Logic Test: %d spheres.", len(self.spheres))
            self.print_status()
        elif cmd in ("ReceivedItems", "RoomUpdate"):
            self.print_status()

    def _received_count(self, item_id: int) -> int:
        # Count by item id (carried in slot_data) rather than resolving names, so
        # counting works even before the data package is processed.
        return sum(1 for net_item in self.items_received if net_item.item == item_id)

    def print_status(self) -> None:
        if not self.spheres:
            return
        if self.current_sphere >= len(self.spheres):
            logger.info("All %d spheres opened. Logic Test complete.", len(self.spheres))
            return
        sphere = self.spheres[self.current_sphere]
        have = self._received_count(sphere["key_id"])
        logger.info(
            "Sphere %d/%d: need %d x %s, have %d. %s",
            self.current_sphere + 1, len(self.spheres), sphere["required"], sphere["key_item"], have,
            "Ready. /proceed to open." if have >= sphere["required"] else "Waiting for keys.",
        )

    def make_gui(self):
        ui = super().make_gui()  # loads kvui/kivy first
        ctx = self

        from kivy.clock import Clock
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.progressbar import ProgressBar
        from kivy.uix.scrollview import ScrollView

        class LogicTestManager(ui):
            base_title = "Archipelago Logic Test Client"

            def build(self):
                container = super().build()

                panel = BoxLayout(orientation="vertical", padding=8, spacing=6)
                self.lt_summary = Label(text="Waiting for connection...", markup=True,
                                        size_hint_y=None, height=32, halign="left", valign="middle")
                self.lt_summary.bind(size=lambda w, *_: setattr(w, "text_size", w.size))
                self.lt_detail = Label(text="", size_hint_y=None, height=26)
                self.lt_progress = ProgressBar(max=1, value=0, size_hint_y=None, height=18)
                self.lt_button = Button(text="Proceed", size_hint_y=None, height=48, disabled=True)
                self.lt_button.bind(on_release=lambda *_: async_start(ctx.proceed(), name="logic test proceed"))

                self.lt_list = Label(text="", markup=True, size_hint_y=None, halign="left", valign="top")
                self.lt_list.bind(width=lambda w, val: setattr(w, "text_size", (val, None)),
                                  texture_size=lambda w, val: setattr(w, "height", val[1]))
                scroll = ScrollView()
                scroll.add_widget(self.lt_list)

                for widget in (self.lt_summary, self.lt_detail, self.lt_progress, self.lt_button):
                    panel.add_widget(widget)
                panel.add_widget(scroll)

                self.add_client_tab("Logic Test", panel)
                Clock.schedule_interval(self._lt_refresh, 0.5)
                return container

            def _lt_refresh(self, *_):
                spheres = ctx.spheres
                if not spheres:
                    self.lt_summary.text = "Waiting for connection / slot data..."
                    self.lt_detail.text = ""
                    self.lt_progress.value = 0
                    self.lt_button.disabled = True
                    self.lt_list.text = ""
                    return

                cur, total = ctx.current_sphere, len(spheres)
                if cur >= total:
                    self.lt_summary.text = f"[b]Complete![/b] All {total} spheres opened."
                    self.lt_detail.text = ""
                    self.lt_progress.max, self.lt_progress.value = 1, 1
                    self.lt_button.text = "Done"
                    self.lt_button.disabled = True
                else:
                    s = spheres[cur]
                    have, need = ctx._received_count(s["key_id"]), s["required"]
                    ready = have >= need
                    self.lt_summary.text = f"[b]Sphere {cur + 1} / {total}[/b]"
                    self.lt_detail.text = f"{s['key_item']}:  {have} / {need}" + ("   READY" if ready else "")
                    self.lt_progress.max = max(need, 1)
                    self.lt_progress.value = min(have, need)
                    self.lt_button.text = f"Open Sphere {cur + 1}" if ready else f"Waiting  ({have}/{need})"
                    self.lt_button.disabled = not ready

                lines = []
                for i, s in enumerate(spheres):
                    if i < cur:
                        mark = "[color=55ff55]done[/color]"
                    elif i == cur:
                        have = ctx._received_count(s["key_id"])
                        mark = f"[color=ffdd55]now {have}/{s['required']}[/color]"
                    else:
                        mark = f"locked ({s['required']} keys)"
                    lines.append(f"Sphere {i + 1}: {mark}")
                self.lt_list.text = "\n".join(lines)

        return LogicTestManager

    async def proceed(self) -> None:
        if not self.spheres:
            logger.info("Not connected to a Logic Test slot yet.")
            return
        if self.current_sphere >= len(self.spheres):
            logger.info("All spheres already opened.")
            return
        sphere = self.spheres[self.current_sphere]
        have = self._received_count(sphere["key_id"])
        if have < sphere["required"]:
            logger.info("Sphere %d not ready: need %d x %s, have %d.",
                        self.current_sphere + 1, sphere["required"], sphere["key_item"], have)
            return
        await self.check_locations(sphere["locations"])
        logger.info("Opened sphere %d, released %d item(s).",
                    self.current_sphere + 1, len(sphere["locations"]))
        self.current_sphere += 1
        self.print_status()


def launch(*args):
    async def main():
        parser = get_base_parser(description="Logic Test semi-automatic client.")
        parser.add_argument("--name", default=None, help="Slot name to connect as.")
        parser.add_argument("url", nargs="?", help="Archipelago connection url")
        parsed = parser.parse_args(args)

        ctx = LogicTestContext(parsed.connect, parsed.password)
        if parsed.name:
            ctx.auth = parsed.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()


if __name__ == "__main__":
    import sys
    launch(*sys.argv[1:])
