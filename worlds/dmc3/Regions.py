from typing import TypedDict

from BaseClasses import ItemClassification, Region
from .Items import DMC3Item
from .Locations import DMC3Location


class Mission(TypedDict):
    secret: list

dmc3_regions: dict[int, Mission] = {
    # First number is mission number, 2nd is secret mission indexes. 0 if the mission doesn't have one
    1: Mission(secret=[0]),
    2: Mission(secret=[0]),
    3: Mission(secret=[1]),
    4: Mission(secret=[0]),
    5: Mission(secret=[2]),
    6: Mission(secret=[0]),
    7: Mission(secret=[3]),
    8: Mission(secret=[4]),
    9: Mission(secret=[5]),
    10: Mission(secret=[6]),
    11: Mission(secret=[7]),
    12: Mission(secret=[0]),
    13: Mission(secret=[8, 9]),
    14: Mission(secret=[0]),
    15: Mission(secret=[0]),
    16: Mission(secret=[10]),
    17: Mission(secret=[11]),
    18: Mission(secret=[12]),
    19: Mission(secret=[0]),
    20: Mission(secret=[0])
}


def setup_all_goal(mission: int, mission_name: str, current_region: Region, world, menu_region):
    menu_region.connect(current_region)
    if mission == 1:
        victory_loc = DMC3Location(world.player, "Final Mission", None,
                                   current_region)
        victory_loc.place_locked_item(
            DMC3Item("Complete", ItemClassification.progression, None, world.player))
        menu_region.locations.append(victory_loc)


# For a linear mission order (1-20 or whatever random order AP comes up with)
def setup_linear_goal(mission: int, mission_name: str, current_region: Region, world, menu_region):
    if mission == world.dmc3_mission_order[0]:
        menu_region.connect(current_region)
    else:
        idx = world.dmc3_mission_order.index(mission)
        if idx > 0:
            prev_mission = world.dmc3_mission_order[idx - 1]
            world.get_region(f"Mission #{prev_mission}").add_exits([mission_name])

    if world.dmc3_mission_order[19] == mission:
        victory_loc = DMC3Location(world.player, "Final Mission", None,
                                   current_region)
        victory_loc.place_locked_item(
            DMC3Item("Complete", ItemClassification.progression, None, world.player))
        current_region.locations.append(victory_loc)