from dataclasses import dataclass
from enum import Enum

from BaseClasses import Item, ItemClassification

item_descriptions = {
    "Astronomical Board": "The key item that is needed in Mission #5, normally obtained at the end of Mission #4",
    "Vital Star S": "A consumable item",
    "N/A": "N/A"
}

item_name_groups = {
    "melees": ["Rebellion (Normal)", "Cerberus", "Agni and Rudra", "Nevan", "Beowulf"],
    "guns": ["Ebony & Ivory", "Shotgun", "Artemis", "Spiral", "Kalina Ann"],
    "essences": ["Essence of Fighting", "Essence of Technique", "Essence of Intelligence"],
    "fragments": ["Orihalcon Fragment (Right)", "Orihalcon Fragment (Left)", "Orihalcon Fragment (Bottom)"],
    "air_hikes": ["Rebellion (Normal) - Air Hike", "Agni and Rudra - Air Hike", "Nevan - Air Raid",
                  "Beowulf - Air Hike"]
}


class Mode(Enum):
    ORB = 0
    CONSUMABLE = 1,
    KEY = 2


@dataclass
class ItemData:
    code: int
    classification: ItemClassification
    description: str
    mode: Mode


dmc3_items: dict[str, ItemData] = {
    # Orbs
    "Blue Orb": ItemData(0x07, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.CONSUMABLE),
    "Purple Orb": ItemData(0x08, ItemClassification.useful, item_descriptions["N/A"],
                           mode=Mode.CONSUMABLE),
    "Blue Orb Fragment": ItemData(0x09, ItemClassification.useful, item_descriptions["N/A"],
                                  mode=Mode.CONSUMABLE),

    # Consumables
    "Vital Star L": ItemData(0x10, ItemClassification.filler, item_descriptions["N/A"],
                             mode=Mode.CONSUMABLE),
    "Vital Star S": ItemData(0x11, ItemClassification.filler, item_descriptions["N/A"],
                             mode=Mode.CONSUMABLE),
    "Devil Star": ItemData(0x12, ItemClassification.filler, item_descriptions["N/A"],
                           mode=Mode.CONSUMABLE),
    "Holy Water": ItemData(0x13, ItemClassification.filler, item_descriptions["N/A"],
                           mode=Mode.CONSUMABLE),

    # Melee
    "Rebellion (Normal)": ItemData(0x16, ItemClassification.progression, item_descriptions["N/A"],
                                   mode=Mode.KEY),
    "Cerberus": ItemData(0x17, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Agni and Rudra": ItemData(0x18, ItemClassification.progression, item_descriptions["N/A"],
                               mode=Mode.KEY),
    #
    "Rebellion (Awakened)": ItemData(0x19, ItemClassification.useful, item_descriptions["N/A"],
                                     mode=Mode.KEY),
    "Nevan": ItemData(0x1A, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Beowulf": ItemData(0x1B, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),

    # Guns
    "Ebony & Ivory": ItemData(0x1C, ItemClassification.useful, item_descriptions["N/A"],
                              mode=Mode.KEY),
    "Shotgun": ItemData(0x1D, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.KEY),
    "Artemis": ItemData(0x1E, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.KEY),
    "Spiral": ItemData(0x1F, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.KEY),
    "Kalina Ann": ItemData(0x21, ItemClassification.useful, item_descriptions["N/A"], mode=Mode.KEY),

    # Key items
    "Astronomical Board": ItemData(0x24, ItemClassification.progression,
                                   item_descriptions["Astronomical Board"], mode=Mode.KEY),
    "Vajura": ItemData(0x25, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    # "high_roller": ItemData(0x26, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Soul of Steel": ItemData(0x27, ItemClassification.progression, item_descriptions["N/A"],
                              mode=Mode.KEY),
    "Essence of Fighting": ItemData(0x28, ItemClassification.progression,
                                    item_descriptions["N/A"], mode=Mode.KEY),
    "Essence of Technique": ItemData(0x29, ItemClassification.progression,
                                     item_descriptions["N/A"], mode=Mode.KEY),
    "Essence of Intelligence": ItemData(0x2A, ItemClassification.progression,
                                        item_descriptions["N/A"], mode=Mode.KEY),
    # These 5 may be wrong
    "Orihalcon Fragment": ItemData(0x2B, ItemClassification.progression,
                                   item_descriptions["N/A"], mode=Mode.KEY),
    "Siren's Shriek": ItemData(0x2C, ItemClassification.progression, item_descriptions["N/A"],
                               mode=Mode.KEY),
    "Crystal Skull": ItemData(0x2D, ItemClassification.progression, item_descriptions["N/A"],
                              mode=Mode.KEY),
    "Ignis Fatuus": ItemData(0x2E, ItemClassification.progression, item_descriptions["N/A"],
                             mode=Mode.KEY),
    "Ambrosia": ItemData(0x2F, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Stone Mask": ItemData(0x30, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Neo Generator": ItemData(0x31, ItemClassification.progression, item_descriptions["N/A"],
                              mode=Mode.KEY),
    "Haywire Neo Generator": ItemData(0x32, ItemClassification.progression,
                                      item_descriptions["N/A"], mode=Mode.KEY),
    "Full Orihalcon": ItemData(0x33, ItemClassification.progression, item_descriptions["N/A"],
                               mode=Mode.KEY),
    "Orihalcon Fragment (Right)": ItemData(0x34, ItemClassification.progression,
                                           item_descriptions["N/A"], mode=Mode.KEY),
    "Orihalcon Fragment (Bottom)": ItemData(0x35, ItemClassification.progression,
                                            item_descriptions["N/A"], mode=Mode.KEY),
    "Orihalcon Fragment (Left)": ItemData(0x36, ItemClassification.progression,
                                          item_descriptions["N/A"], mode=Mode.KEY),
    "Golden Sun": ItemData(0x37, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
    "Onyx Moonshard": ItemData(0x38, ItemClassification.progression, item_descriptions["N/A"],
                               mode=Mode.KEY),
    "Samsara": ItemData(0x39, ItemClassification.progression, item_descriptions["N/A"], mode=Mode.KEY),
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
