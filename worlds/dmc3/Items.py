from dataclasses import dataclass

from BaseClasses import Item, ItemClassification

item_descriptions = {
    "Astronomical Board": "The key item that is needed in Mission #5, normally obtained at the end of Mission #4",
    "Vital Star S": "A consumable item",
}

item_name_groups = {
    "melees": ["Rebellion", "Cerberus", "Agni and Rudra", "Nevan", "Beowulf"],
    "guns": ["Ebony & Ivory", "Shotgun", "Artemis", "Spiral", "Kalina Ann"],
    "essences": ["Essence of Fighting", "Essence of Technique", "Essence of Intelligence"],
    "fragments": ["Orihalcon Fragment (Right)", "Orihalcon Fragment (Left)", "Orihalcon Fragment (Bottom)"],
    "air_hikes": ["Rebellion - Air Hike", "Agni and Rudra - Air Hike",
                  "Beowulf - Air Hike"],
    "air_hike_capable": ["Rebellion", "Agni and Rudra", "Beowulf"],
    "styles": ["Progressive Trickster", "Progressive Swordmaster", "Progressive Gunslinger", "Progressive Royalguard"],
    "upgradable_skills": ["Rebellion - Progressive Stinger", "Agni and Rudra - Progressive Jet Stream", "Nevan - Progressive Reverb Shock", "Beowulf - Progressive Uppercut"]
}


@dataclass
class ItemData:
    code: int
    classification: ItemClassification


dmc3_items: dict[str, ItemData] = {
    # Orbs
    "Blue Orb": ItemData(0x07, ItemClassification.useful),
    "Purple Orb": ItemData(0x08, ItemClassification.progression),
    #"Blue Orb Fragment": ItemData(0x09, ItemClassification.useful),

    # Consumables
    "Vital Star L": ItemData(0x10, ItemClassification.filler),
    "Vital Star S": ItemData(0x11, ItemClassification.filler),
    "Devil Star": ItemData(0x12, ItemClassification.filler),
    "Holy Water": ItemData(0x13, ItemClassification.filler),

    # Melee
    "Rebellion": ItemData(0x16, ItemClassification.progression), # Non-awakened Rebellion
    "Cerberus": ItemData(0x17, ItemClassification.progression),
    "Agni and Rudra": ItemData(0x18, ItemClassification.progression),
    "Devil Trigger": ItemData(0x19, ItemClassification.progression), # Awakened Rebellion
    "Nevan": ItemData(0x1A, ItemClassification.progression),
    "Beowulf": ItemData(0x1B, ItemClassification.progression),

    # Guns
    "Ebony & Ivory": ItemData(0x1C, ItemClassification.useful),
    "Shotgun": ItemData(0x1D, ItemClassification.useful),
    "Artemis": ItemData(0x1E, ItemClassification.useful),
    "Spiral": ItemData(0x1F, ItemClassification.useful),
    "Kalina Ann": ItemData(0x21, ItemClassification.useful),

    # Styles
    "Quicksilver Style": ItemData(0x22, ItemClassification.useful),
    "Doppelganger Style": ItemData(0x23, ItemClassification.useful),

    # Key items
    "Astronomical Board": ItemData(0x24, ItemClassification.progression),
    "Vajura": ItemData(0x25, ItemClassification.progression),

    "Soul of Steel": ItemData(0x27, ItemClassification.progression),
    "Essence of Fighting": ItemData(0x28, ItemClassification.progression),
    "Essence of Technique": ItemData(0x29, ItemClassification.progression),
    "Essence of Intelligence": ItemData(0x2A, ItemClassification.progression),
    "Orihalcon Fragment": ItemData(0x2B, ItemClassification.progression),
    "Siren's Shriek": ItemData(0x2C, ItemClassification.progression),
    "Crystal Skull": ItemData(0x2D, ItemClassification.progression),
    "Ignis Fatuus": ItemData(0x2E, ItemClassification.progression),
    "Ambrosia": ItemData(0x2F, ItemClassification.progression),
    "Stone Mask": ItemData(0x30, ItemClassification.progression),
    "Neo Generator": ItemData(0x31, ItemClassification.progression),
    "Haywire Neo Generator": ItemData(0x32, ItemClassification.progression),
    "Full Orihalcon": ItemData(0x33, ItemClassification.progression),
    "Orihalcon Fragment (Right)": ItemData(0x34, ItemClassification.progression),
    "Orihalcon Fragment (Bottom)": ItemData(0x35, ItemClassification.progression),
    "Orihalcon Fragment (Left)": ItemData(0x36, ItemClassification.progression),
    "Golden Sun": ItemData(0x37, ItemClassification.progression),
    "Onyx Moonshard": ItemData(0x38, ItemClassification.progression),
    "Samsara": ItemData(0x39, ItemClassification.progression),

    #"Remote": ItemData(0x26, ItemClassification.progression),
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
