from dataclasses import dataclass
from BaseClasses import Item, ItemClassification as IC
from .Enums import *

class BuckshotRouletteItem(Item):
    game = "Buckshot Roulette"

@dataclass
class ItemData:
    id: int
    classification: IC
    flags: int = 0x00

item_table: dict[str, ItemData] = {
    "Double or Nothing Pills":      ItemData(1,  IC.progression, I_DOUBLE_OR_NOTHING | I_PILLS),
    "Hand Saw":                     ItemData(2,  IC.progression, I_CONSUMABLE),
    "Magnifying Glass":             ItemData(3,  IC.progression, I_CONSUMABLE),
    "Beer":                         ItemData(4,  IC.progression, I_CONSUMABLE),
    "Cigarette Pack":               ItemData(5,  IC.progression, I_CONSUMABLE),
    "Handcuffs":                    ItemData(6,  IC.progression, I_CONSUMABLE),
    "Expired Medicine":             ItemData(7,  IC.progression, I_CONSUMABLE | I_DOUBLE_OR_NOTHING),
    "Burner Phone":                 ItemData(8,  IC.progression, I_CONSUMABLE | I_DOUBLE_OR_NOTHING),
    "Adrenaline":                   ItemData(9,  IC.progression, I_CONSUMABLE | I_DOUBLE_OR_NOTHING),
    "Inverter":                     ItemData(10, IC.progression, I_CONSUMABLE | I_DOUBLE_OR_NOTHING),

    "Progressive Item Luck":        ItemData(11, IC.useful, I_SPECIAL),
    "Life Bank Charge":             ItemData(12, IC.useful, I_SPECIAL),

    "Stolen Package Trap":          ItemData(13, IC.trap),
    "Schrodinger's Bullet Trap":    ItemData(14, IC.trap),

    "Empty Shell":                  ItemData(15, IC.filler),
    "Empty Cigarette Box":          ItemData(16, IC.filler),
    "Broken Magnifying Glass":      ItemData(17, IC.filler),
    "Crushed Beer Can":             ItemData(18, IC.filler),
    "Sawed-Off Shotgun Barrel":     ItemData(19, IC.filler),
    "Broken Handcuffs":             ItemData(20, IC.filler),
    "Empty Pill Packet":            ItemData(21, IC.filler),
    "Double Inverter":              ItemData(22, IC.filler),
    "Snapped Burner Phone":         ItemData(23, IC.filler),
    "Empty Adrenaline Vial":        ItemData(24, IC.filler),

    "Base Game Beaten":             ItemData(25, IC.progression, I_EVENT),
    "WINNER":                       ItemData(26, IC.progression, I_EVENT)
}

item_id_table = {name: data.id for name, data in item_table.items()}