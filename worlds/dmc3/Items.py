from enum import Enum
from typing import NamedTuple, Literal

from BaseClasses import Item, ItemClassification

item_descriptions = {
    "Astronomical Board": "The key item that is needed in Mission #5, normally obtained at the end of Mission #4",
    "N/A": "Not yet written"
}


class ItemData(NamedTuple):
    name: str
    code: int
    classification: ItemClassification
    description: str


dmc3_items: dict[str, ItemData] = {
    # Orbs
    "Blue Orb": ItemData("Blue Orb", 0x07, ItemClassification.useful, item_descriptions["N/A"]),
    "Purple Orb": ItemData("Purple Orb", 0x08, ItemClassification.useful, item_descriptions["N/A"]),
    "Blue Orb Fragment": ItemData("Blue Orb Fragment", 0x09, ItemClassification.useful, item_descriptions["N/A"]),

    # Consumables
    "Vital Star L": ItemData("Vital Star L", 0x10, ItemClassification.filler, item_descriptions["N/A"]),
    "Vital Star S": ItemData("Vital Star S", 0x11, ItemClassification.filler, item_descriptions["N/A"]),
    "Devil Star": ItemData("Devil Star", 0x12, ItemClassification.filler, item_descriptions["N/A"]),
    "Holy Water": ItemData("Holy Water", 0x13, ItemClassification.filler, item_descriptions["N/A"]),

    # Melee
    "Rebellion (Normal)": ItemData("Rebellion (Normal)", 0x16, ItemClassification.useful, item_descriptions["N/A"]),
    "Cerberus": ItemData("Cerberus", 0x17, ItemClassification.useful, item_descriptions["N/A"]),
    "Agni and Rudra": ItemData("Agni and Rudra", 0x18, ItemClassification.useful, item_descriptions["N/A"]),
    # Tie Awakened Rebellion to DT unlock?
    "Rebellion (Awakened)": ItemData("Rebellion (Awakened)", 0x19, ItemClassification.useful, item_descriptions["N/A"]),
    "Nevan": ItemData("Nevan", 0x1A, ItemClassification.useful, item_descriptions["N/A"]),
    "Beowulf": ItemData("Beowulf", 0x1B, ItemClassification.useful, item_descriptions["N/A"]),

    # Guns
    "Ebony & Ivory": ItemData("Ebony & Ivory", 0x1C, ItemClassification.useful, item_descriptions["N/A"]),
    "Shotgun": ItemData("Shotgun", 0x1D, ItemClassification.useful, item_descriptions["N/A"]),
    "Artemis": ItemData("Artemis", 0x1E, ItemClassification.useful, item_descriptions["N/A"]),
    "Spiral": ItemData("Spiral", 0x1F, ItemClassification.useful, item_descriptions["N/A"]),
    "Kalina Ann": ItemData("Kalina Ann", 0x21, ItemClassification.useful, item_descriptions["N/A"]),

    # Key items
    "Astronomical Board": ItemData("Astronomical Board", 0x24, ItemClassification.progression, item_descriptions["Astronomical Board"]),
    "Vajura": ItemData("Vajura", 0x25, ItemClassification.progression, item_descriptions["N/A"]),
    # "high_roller": ItemData("high_roller", 0x26, ItemClassification.progression, item_descriptions["N/A"]),
    "Soul of Steel": ItemData("Soul of Steel", 0x27, ItemClassification.progression, item_descriptions["N/A"]),
    "Essence of Fighting": ItemData("Essence of Fighting", 0x28, ItemClassification.progression, item_descriptions["N/A"]),
    "Essence of Technique": ItemData("Essence of Technique", 0x29, ItemClassification.progression, item_descriptions["N/A"]),
    "Essence of Intelligence": ItemData("Essence of Intelligence", 0x2A, ItemClassification.progression,
                                     item_descriptions["N/A"]),
    # These 5 may be wrong
    "Orihalcon Fragment": ItemData("Orihalcon Fragment", 0x2B, ItemClassification.progression,
                                   item_descriptions["N/A"]),
    "Siren's Shriek": ItemData("Siren's Shriek", 0x2C, ItemClassification.progression, item_descriptions["N/A"]),
    "Crystal Skull": ItemData("Crystal Skull", 0x2D, ItemClassification.progression, item_descriptions["N/A"]),
    "Ignis Fatuus": ItemData("Ignis Fatuus", 0x2E, ItemClassification.progression, item_descriptions["N/A"]),
    "Ambrosia": ItemData("Ambrosia", 0x2F, ItemClassification.progression, item_descriptions["N/A"]),
    "Stone Mask": ItemData("Stone Mask", 0x30, ItemClassification.progression, item_descriptions["N/A"]),
    "Neo Generator": ItemData("Neo Generator", 0x31, ItemClassification.progression, item_descriptions["N/A"]),
    "Haywire Neo Generator": ItemData("Haywire Neo Generator", 0x32, ItemClassification.progression,
                                      item_descriptions["N/A"]),
    "Full Orihalcon": ItemData("Full Orihalcon", 0x33, ItemClassification.progression, item_descriptions["N/A"]),
    "Orihalcon Fragment (Right)": ItemData("Orihalcon Fragment (Right)", 0x34, ItemClassification.progression, item_descriptions["N/A"]),
    "Orihalcon Fragment (Bottom)": ItemData("Orihalcon Fragment (Bottom)", 0x35, ItemClassification.progression, item_descriptions["N/A"]),
    "Orihalcon Fragment (Left)": ItemData("Orihalcon Fragment (Left)", 0x36, ItemClassification.progression, item_descriptions["N/A"]),
    "Golden Sun": ItemData("Golden Sun", 0x37, ItemClassification.progression, item_descriptions["N/A"]),
    "Onyx Moonshard": ItemData("Onyx Moonshard", 0x38, ItemClassification.progression, item_descriptions["N/A"]),
    "Samsara": ItemData("Samsara", 0x39, ItemClassification.progression, item_descriptions["N/A"]),
}


class Type(Enum):
    MELEE = 0
    GUN = 1,
    KEY = 2


weapons: set[tuple[ItemData, Literal[Type.MELEE]] | tuple[ItemData, Literal[Type.GUN]]] = {
    (dmc3_items["Rebellion (Normal)"], Type.MELEE),
    (dmc3_items["Cerberus"], Type.MELEE),
    (dmc3_items["Agni and Rudra"], Type.MELEE),
    (dmc3_items["Rebellion (Awakened)"], Type.MELEE),
    (dmc3_items["Nevan"], Type.MELEE),
    (dmc3_items["Beowulf"], Type.MELEE),

    (dmc3_items["Ebony & Ivory"], Type.GUN),
    (dmc3_items["Shotgun"], Type.GUN),
    (dmc3_items["Artemis"], Type.GUN),
    (dmc3_items["Spiral"], Type.GUN),
    (dmc3_items["Kalina Ann"], Type.GUN),
}

key_items: list[str] = [
    "Astronomical Board", "Vajura", "Soul of Steel", "Essence of Fighting", "Essence of Technique", "Essence of Intelligence",
    "Orihalcon Fragment", "Siren's Shriek", "Crystal Skull", "Ignis Fatuus", "Ambrosia", "Stone Mask", "Neo Generator",
    "Haywire Neo Generator", "Full Orihalcon", "Orihalcon Fragment (Right)", "Orihalcon Fragment (Left)", "Orihalcon Fragment (Bottom)", "Golden Sun",
    "Onyx Moonshard", "Samsara"

]

junk_pool: dict[str, int] = {
    "Vital Star S": 5,
    "Vital Star L": 3,
    "Devil Star": 5,
    "Holy Water": 2
}


class DMC3Item(Item):
    game = "Devil May Cry 3"


# def is_progression(item_name):
#     if item_name in key_items:
#         return True
#     return False


def get_item_type(self):
    return True
