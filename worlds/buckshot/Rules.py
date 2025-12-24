from typing import Callable
from BaseClasses import CollectionState
from .Enums import *
from .Items import item_table

def consumable_rule(world, count: int, exclude_don=False) -> Callable[[CollectionState], bool]:
    consumables: list[str] = [
        item_name
        for item_name, item_data in item_table.items()
        if item_data.flags & I_CONSUMABLE and (not item_data.flags & I_DOUBLE_OR_NOTHING if exclude_don else True)
    ]
    return lambda state: state.has_from_list(consumables, world.player, count)

def specific_consumables_rule(world, consumables: list[str]) -> Callable[[CollectionState], bool]:
    return lambda state: state.has_all(consumables, world.player)

def full_house_rule(world) -> Callable[[CollectionState], bool]:
    consumables: list[str] = [
        item_name
        for item_name, item_data in item_table.items()
        if (item_data.flags & I_CONSUMABLE) and item_name != "Adrenaline"
    ]
    return lambda state: state.has("Adrenaline", world.player) and state.has_from_list(consumables, world.player, 7)

def don_access_rule(world, items: list[str], location=None) -> Callable[[CollectionState], bool]:
    if location is None:
        return lambda state: state.has_all(items, world.player)
    else:
        return lambda state: state.has_all(items, world.player) and state.can_reach_location(location, world.player)