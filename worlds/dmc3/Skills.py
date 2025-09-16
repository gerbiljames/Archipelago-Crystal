from dataclasses import dataclass

from BaseClasses import ItemClassification
from .Items import item_name_groups

skill_descriptions = {
    "N/A": "N/A"
}


@dataclass
class SkillData:
    code: int
    classification: ItemClassification
    description: str


# We are going to treat everything >=0x40 as skills
weapon_skills: dict[str, SkillData] = {
    # Rebellion
    "Rebellion (Normal) - Progressive Stinger": SkillData( # Stinger Level 1
        0x40, ItemClassification.useful, skill_descriptions["N/A"]),
    # "Rebellion (Normal) - Stinger Level 2": SkillData(
    #     0x41, ItemClassification.useful, skill_descriptions["N/A"]),
    "Rebellion (Normal) - Drive": SkillData(
        0x42, ItemClassification.useful, skill_descriptions["N/A"]),
    "Rebellion (Normal) - Air Hike": SkillData(
        0x43, ItemClassification.progression, skill_descriptions["N/A"]),

    # Cerberus (Why does Cerberus only have two purchasable skills?)
    "Cerberus - Revolver Level 2": SkillData(
        0x44, ItemClassification.useful, skill_descriptions["N/A"]),
    "Cerberus - Windmill": SkillData(
        0x45, ItemClassification.useful, skill_descriptions["N/A"]),

    # Agni and Rudra
    "Agni and Rudra - Progressive Jet Stream": SkillData( #Jet Stream Level 2
        0x46, ItemClassification.useful, skill_descriptions["N/A"]),
    # "Agni and Rudra - Jet Stream Level 3": SkillData(
    #     0x47, ItemClassification.useful, skill_descriptions["N/A"]),
    "Agni and Rudra - Whirlwind": SkillData(
        0x48, ItemClassification.useful, skill_descriptions["N/A"]),
    "Agni and Rudra - Air Hike": SkillData(
        0x49, ItemClassification.progression, skill_descriptions["N/A"]),

    # Nevan
    "Nevan - Progressive Reverb Shock": SkillData(
        0x4A, ItemClassification.useful, skill_descriptions["N/A"]),
    # "Nevan - Reverb Shock Level 2": SkillData(
    #     0x4B, ItemClassification.useful, skill_descriptions["N/A"]),
    "Nevan - Bat Rift Level 2": SkillData(
        0x4C, ItemClassification.useful, skill_descriptions["N/A"]),
    "Nevan - Air Raid": SkillData(  # Needed for SM6
        0x4D, ItemClassification.progression, skill_descriptions["N/A"]),
    "Nevan - Volume Up": SkillData(
        0x4E, ItemClassification.useful, skill_descriptions["N/A"]
    ),

    # Beowulf
    "Beowulf - Straight Level 2": SkillData(
        0x4F, ItemClassification.useful, skill_descriptions["N/A"]),
    "Beowulf - Beast Uppercut": SkillData(
        0x50, ItemClassification.useful, skill_descriptions["N/A"]),
    "Beowulf - Rising Dragon": SkillData(
        0x51, ItemClassification.useful, skill_descriptions["N/A"]),
    "Beowulf - Air Hike": SkillData(
        0x52, ItemClassification.progression, skill_descriptions["N/A"]),
}

gun_levels = {
    "Ebony & Ivory Progressive Upgrade": SkillData(0x53, ItemClassification.filler,
                                                   skill_descriptions["N/A"]),
    "Shotgun Progressive Upgrade": SkillData(0x54, ItemClassification.filler,
                                             skill_descriptions["N/A"]),
    "Artemis Progressive Upgrade": SkillData(0x55, ItemClassification.filler,
                                             skill_descriptions["N/A"]),
    "Spiral Progressive Upgrade": SkillData(0x56, ItemClassification.filler,
                                            skill_descriptions["N/A"]),
    "Kalina Ann Progressive Upgrade": SkillData(0x57, ItemClassification.filler,
                                                skill_descriptions["N/A"]),
}

skills_dict: dict[str, list[SkillData]] = {
    item: [skill for name, skill in weapon_skills.items() if name.startswith(item)]
    for item in item_name_groups["melees"]
}

gun_levels_dict: dict[str, list[SkillData]] = {
    item: [skill for name, skill in weapon_skills.items() if name.startswith(item)]
    for item in item_name_groups["guns"]
}

combined_upgrades = weapon_skills | gun_levels
skill_upgrades: dict[str, list[SkillData]] = skills_dict | gun_levels_dict
