import asyncio

from kvui import GameManager
from .DMC3Client import DMC3Context


class DMC3Manager(GameManager):
    logging_pairs = [("Client", "Archipelago")]
    base_title = "Archipelago Devil May Cry 3 Hint Client"

def start_gui(ctx: DMC3Context):
    ctx.ui = DMC3Manager(ctx)
    ctx.ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")