from enum import Enum
from typing import NamedTuple, Literal

from BaseClasses import Item, ItemClassification

item_descriptions = {
    "Astronomical Board": "The key item that is needed in Mission #5, normally obtained at the end of Mission #4",
    "Vital Star S": "A consumable item",
    "N/A": "N/A"
}


class Mode(Enum):
    ORB = 0
    CONSUMABLE = 1,
    KEY = 2


class ItemData(NamedTuple):
    name: str
    code: int
    classification: ItemClassification
    description: str
    mode: Mode


dmc3_items: dict[str, ItemData] = {
    # Orbs
    "Blue Orb": ItemData("Blue Orb", 0x07, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.CONSUMABLE),
    "Purple Orb": ItemData("Purple Orb", 0x08, ItemClassification.useful, item_descriptions["N/A"],
                           mode=Mode.CONSUMABLE),
    "Blue Orb Fragment": ItemData("Blue Orb Fragment", 0x09, ItemClassification.useful, item_descriptions["N/A"],
                                  mode=Mode.CONSUMABLE),

    # Consumables
    "Vital Star L": ItemData("Vital Star L", 0x10, ItemClassification.filler, item_descriptions["N/A"],
                             mode=Mode.CONSUMABLE),
    "Vital Star S": ItemData("Vital Star S", 0x11, ItemClassification.filler, item_descriptions["N/A"],
                             mode=Mode.CONSUMABLE),
    "Devil Star": ItemData("Devil Star", 0x12, ItemClassification.filler, item_descriptions["N/A"],
                           mode=Mode.CONSUMABLE),
    "Holy Water": ItemData("Holy Water", 0x13, ItemClassification.filler, item_descriptions["N/A"],
                           mode=Mode.CONSUMABLE),

    # Melee
    "Rebellion (Normal)": ItemData("Rebellion (Normal)", 0x16, ItemClassification.progression, item_descriptions["N/A"],
                                   mode=Mode.KEY),
    "Cerberus": ItemData("Cerberus", 0x17, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Agni and Rudra": ItemData("Agni and Rudra", 0x18, ItemClassification.progression, item_descriptions["N/A"],
                               mode=Mode.KEY),
    # Tie Awakened Rebellion to DT unlock?
    "Rebellion (Awakened)": ItemData("Rebellion (Awakened)", 0x19, ItemClassification.useful, item_descriptions["N/A"],
                                     mode=Mode.KEY),
    "Nevan": ItemData("Nevan", 0x1A, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Beowulf": ItemData("Beowulf", 0x1B, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),

    # Guns
    "Ebony & Ivory": ItemData("Ebony & Ivory", 0x1C, ItemClassification.useful, item_descriptions["N/A"],
                              mode=Mode.KEY),
    "Shotgun": ItemData("Shotgun", 0x1D, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.KEY),
    "Artemis": ItemData("Artemis", 0x1E, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.KEY),
    "Spiral": ItemData("Spiral", 0x1F, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.KEY),
    "Kalina Ann": ItemData("Kalina Ann", 0x21, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.KEY),

    # Key items
    "Astronomical Board": ItemData("Astronomical Board", 0x24, ItemClassification.progression,
                                   item_descriptions["Astronomical Board"], mode=Mode.KEY),
    "Vajura": ItemData("Vajura", 0x25, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    # "high_roller": ItemData("high_roller", 0x26, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Soul of Steel": ItemData("Soul of Steel", 0x27, ItemClassification.progression, item_descriptions["N/A"],
                              mode=Mode.KEY),
    "Essence of Fighting": ItemData("Essence of Fighting", 0x28, ItemClassification.progression,
                                    item_descriptions["N/A"], mode=Mode.KEY),
    "Essence of Technique": ItemData("Essence of Technique", 0x29, ItemClassification.progression,
                                     item_descriptions["N/A"], mode=Mode.KEY),
    "Essence of Intelligence": ItemData("Essence of Intelligence", 0x2A, ItemClassification.progression,
                                        item_descriptions["N/A"], mode=Mode.KEY),
    # These 5 may be wrong
    "Orihalcon Fragment": ItemData("Orihalcon Fragment", 0x2B, ItemClassification.progression,
                                   item_descriptions["N/A"], mode=Mode.KEY),
    "Siren's Shriek": ItemData("Siren's Shriek", 0x2C, ItemClassification.progression, item_descriptions["N/A"],
                               mode=Mode.KEY),
    "Crystal Skull": ItemData("Crystal Skull", 0x2D, ItemClassification.progression, item_descriptions["N/A"],
                              mode=Mode.KEY),
    "Ignis Fatuus": ItemData("Ignis Fatuus", 0x2E, ItemClassification.progression, item_descriptions["N/A"],
                             mode=Mode.KEY),
    "Ambrosia": ItemData("Ambrosia", 0x2F, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Stone Mask": ItemData("Stone Mask", 0x30, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Neo Generator": ItemData("Neo Generator", 0x31, ItemClassification.progression, item_descriptions["N/A"],
                              mode=Mode.KEY),
    "Haywire Neo Generator": ItemData("Haywire Neo Generator", 0x32, ItemClassification.progression,
                                      item_descriptions["N/A"], mode=Mode.KEY),
    "Full Orihalcon": ItemData("Full Orihalcon", 0x33, ItemClassification.progression, item_descriptions["N/A"],
                               mode=Mode.KEY),
    "Orihalcon Fragment (Right)": ItemData("Orihalcon Fragment (Right)", 0x34, ItemClassification.progression,
                                           item_descriptions["N/A"], mode=Mode.KEY),
    "Orihalcon Fragment (Bottom)": ItemData("Orihalcon Fragment (Bottom)", 0x35, ItemClassification.progression,
                                            item_descriptions["N/A"], mode=Mode.KEY),
    "Orihalcon Fragment (Left)": ItemData("Orihalcon Fragment (Left)", 0x36, ItemClassification.progression,
                                          item_descriptions["N/A"], mode=Mode.KEY),
    "Golden Sun": ItemData("Golden Sun", 0x37, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Onyx Moonshard": ItemData("Onyx Moonshard", 0x38, ItemClassification.progression, item_descriptions["N/A"],
                               mode=Mode.KEY),
    "Samsara": ItemData("Samsara", 0x39, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
}


class Type(Enum):
    MELEE = 0
    GUN = 1,
    KEY = 2


weapons: set[tuple[ItemData, Literal[Type.MELEE]] | tuple[ItemData, Literal[Type.GUN]]] = {
    (dmc3_items["Rebellion (Normal)"], Type.MELEE),
    (dmc3_items["Cerberus"], Type.MELEE),
    (dmc3_items["Agni and Rudra"], Type.MELEE),
    # (dmc3_items["Rebellion (Awakened)"], Type.MELEE),
    (dmc3_items["Nevan"], Type.MELEE),
    (dmc3_items["Beowulf"], Type.MELEE),

    (dmc3_items["Ebony & Ivory"], Type.GUN),
    (dmc3_items["Shotgun"], Type.GUN),
    (dmc3_items["Artemis"], Type.GUN),
    (dmc3_items["Spiral"], Type.GUN),
    (dmc3_items["Kalina Ann"], Type.GUN),
}

key_items: list[str] = [
    "Astronomical Board", "Vajura", "Soul of Steel", "Essence of Fighting", "Essence of Technique",
    "Essence of Intelligence",
    "Orihalcon Fragment", "Siren's Shriek", "Crystal Skull", "Ignis Fatuus", "Ambrosia", "Stone Mask", "Neo Generator",
    "Haywire Neo Generator", "Full Orihalcon", "Orihalcon Fragment (Right)", "Orihalcon Fragment (Left)",
    "Orihalcon Fragment (Bottom)", "Golden Sun",
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
