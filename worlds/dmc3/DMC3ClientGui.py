import asyncio

from kvui import GameManager
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

from . import DevilMayCry3World
from .DMC3Client import DMC3Context
from .Items import key_items


class TrackerGrid(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        grid = self.ids.checklist_grid
        self.checkboxes: dict[str, CheckBox] = {}
        for i in range(0, len(key_items), 3):
            row = key_items[i:i + 3]
            for item in row:
                label = Label(text=str(item), size_hint_x=1)
                cb = CheckBox(
                    active=False,
                    disabled=True,
                    size_hint_x=None,
                    width=40,
                )
                grid.add_widget(label)
                grid.add_widget(cb)
                self.checkboxes[item] = cb

    def update_checkboxes(self, checklist: dict[str, bool]):
        for item, cb in self.checkboxes.items():
            cb.active = checklist[item]

    def update_orbs(self, blue, purple):
        self.ids.blue_orbs.text = f"Blue Orbs: {blue}"
        self.ids.purple_orbs.text = f"Purple Orbs: {purple}"


class DMC3Manager(GameManager):
    logging_pairs = [("Client", "Archipelago")]
    base_title = "Archipelago Devil May Cry 3 Client"

    def __init__(self, ctx):
        super().__init__(ctx)
        self.tracker = None
        self.checklist = {key: False for key in key_items}

    def build(self):
        container = super().build()
        tracker = TrackerGrid(size_hint=(1, 1))
        self.add_client_tab("Tracker", tracker)
        self.tracker = tracker
        return container

    def update_checklist(self, blue, purple):
        self.tracker.update_checkboxes(self.checklist)
        self.tracker.update_orbs(blue, purple)


def start_gui(ctx: DMC3Context):
    ctx.ui = DMC3Manager(ctx)
    ctx.ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
    import pkgutil

    data = pkgutil.get_data(DevilMayCry3World.__module__, "dmc3client.kv").decode()
    Builder.load_string(data)
