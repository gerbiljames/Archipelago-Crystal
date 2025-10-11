from dataclasses import dataclass

from BaseClasses import ItemClassification
from .Items import item_name_groups, ItemData

skill_descriptions = {
    "N/A": "N/A"
}


# We are going to treat everything >=0x40 as skills
weapon_skills: dict[str, ItemData] = {
    # Rebellion
    "Rebellion - Progressive Stinger": ItemData(  # Stinger Level 1
        0x40, ItemClassification.useful),
    # "Rebellion - Stinger Level 2": ItemData(
    #     0x41, ItemClassification.useful),
    "Rebellion - Drive": ItemData(
        0x42, ItemClassification.useful),
    "Rebellion - Air Hike": ItemData(
        0x43, ItemClassification.progression),

    # Cerberus (Why does Cerberus only have two purchasable skills?)
    "Cerberus - Revolver Level 2": ItemData(
        0x44, ItemClassification.useful),
    "Cerberus - Windmill": ItemData(
        0x45, ItemClassification.useful),

    # Agni and Rudra
    "Agni and Rudra - Progressive Jet Stream": ItemData(  # Jet Stream Level 2
        0x46, ItemClassification.useful),
    # "Agni and Rudra - Jet Stream Level 3": ItemData(
    #     0x47, ItemClassification.useful),
    "Agni and Rudra - Whirlwind": ItemData(
        0x48, ItemClassification.useful),
    "Agni and Rudra - Air Hike": ItemData(
        0x49, ItemClassification.progression),

    # Nevan
    "Nevan - Progressive Reverb Shock": ItemData(
        0x4A, ItemClassification.useful),
    # "Nevan - Reverb Shock Level 2": ItemData(
    #     0x4B, ItemClassification.useful),
    "Nevan - Bat Rift Level 2": ItemData(
        0x4C, ItemClassification.useful),
    "Nevan - Air Raid": ItemData(  # Needed for SM6
        0x4D, ItemClassification.progression),
    "Nevan - Volume Up": ItemData(
        0x4E, ItemClassification.useful
    ),

    # Beowulf
    "Beowulf - Straight Level 2": ItemData(
        0x4F, ItemClassification.useful),
    "Beowulf - Beast Uppercut": ItemData(
        0x50, ItemClassification.useful),
    "Beowulf - Rising Dragon": ItemData(
        0x51, ItemClassification.useful),
    "Beowulf - Air Hike": ItemData(
        0x52, ItemClassification.progression),
}

gun_levels = {
    "Ebony & Ivory Progressive Upgrade": ItemData(0x53, ItemClassification.filler),
    "Shotgun Progressive Upgrade": ItemData(0x54, ItemClassification.filler),
    "Artemis Progressive Upgrade": ItemData(0x55, ItemClassification.filler),
    "Spiral Progressive Upgrade": ItemData(0x56, ItemClassification.filler),
    "Kalina Ann Progressive Upgrade": ItemData(0x57, ItemClassification.filler),
}

styles = {
    "Progressive Trickster": ItemData(0x60, ItemClassification.filler),
    "Progressive Swordmaster": ItemData(0x61, ItemClassification.filler),
    "Progressive Gunslinger": ItemData(0x62, ItemClassification.filler),
    "Progressive Royalguard": ItemData(0x63, ItemClassification.filler),
}

skills_dict: dict[str, list[ItemData]] = {
    item: [skill for name, skill in weapon_skills.items() if name.startswith(item)]
    for item in item_name_groups["melees"]
}

gun_levels_dict: dict[str, list[ItemData]] = {
    item: [skill for name, skill in weapon_skills.items() if name.startswith(item)]
    for item in item_name_groups["guns"]
}

combined_upgrades = weapon_skills | gun_levels
skill_upgrades: dict[str, list[ItemData]] = skills_dict | gun_levels_dict
