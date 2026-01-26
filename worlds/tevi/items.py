"""This module represents item definitions for Tevi"""
from typing import Dict, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import TeviWorld


class TeviItem(Item):
    """Tevi Item Definition"""
    game: str = "Tevi"

    @staticmethod
    def is_progression_item(name: str, options):
        """
        not used
        Defines if an item is considered a progression item.

        This will likely be updated as future logic changes happen.
        For now im porting the logic from the existing rando as is.
        """
        progression_items = {
            "Knife",
            "Double Juump",
            "Wall Jump",
            "Air Dash",
            "Gear",
            "Jet Pack",
            "Water Movement",
            "Air Slide",
            "High Jump",
            "Vortex Glove",
            "Cross Bomb",
            "Area Bomb",
            "Nap Pillow"
        }
        return name in progression_items


class TeviItemData():
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    default_quantity: int = 1
    max_quantity: int = 1
    weight: int = 1
    def __init__(self,category: str,
                code: Optional[int] = None,
                classification: ItemClassification = ItemClassification.filler,
                default_quantity: int = 1,
                max_quantity: int = 1,
                weight: int = 1):
        self.category= category
        self.code: Optional[int] = code
        self.classification = classification
        self.default_quantity: int = default_quantity
        self.max_quantity: int = max_quantity
        self.weight: int = weight


def get_items_by_category(category: str) -> Dict[str, TeviItemData]:
    item_dict: Dict[str, TeviItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict


def get_potential_new_item(world: "TeviWorld") -> Dict[str, TeviItemData]:
    item_dict: Dict[str, TeviItemData] = {}
    for name, data in item_table.items():
        if world.item_quantities[name] < data.max_quantity and name != "Astral Gear":
            item_dict.setdefault(name, data)
    return item_dict


def get_potential_new_filler_item(world: "TeviWorld") -> Dict[str, TeviItemData]:
    item_dict: Dict[str, TeviItemData] = {}
    for name, data in item_table.items():
        if world.item_quantities[name] < data.max_quantity and data.classification == ItemClassification.filler:
            item_dict.setdefault(name, data)
    return item_dict

def get_item_groups():
    item_name_groups = {}
    item_name_groups["Progression"] = []
    for item,data in item_table.items():
        if data.category in item_name_groups:
            item_name_groups[data.category].add(item)
        else:
            item_name_groups[data.category] = {item}
        if data.classification == ItemClassification.progression:
            item_name_groups["Progression"] += {item}

    for item,data in teleporter_table.items():
        if data.category in item_name_groups:
            item_name_groups[data.category].add(item)
            item_name_groups["Progression"] += {item}
        else:
            item_name_groups[data.category] = {item}
    return item_name_groups

item_table: Dict[str,TeviItemData] ={
    # Goal Requiment
    "Astral Gear":                                             TeviItemData("Goal",    44966541_001, ItemClassification.progression_skip_balancing,       25, 255),

    #Stat Buffs
    "Kiwi Bunny Potion":                                       TeviItemData("Stat",    44966541_002, ItemClassification.filler,                           35, 255),
    "Blueberry Bunny Potion":                                 TeviItemData("Stat",    44966541_003, ItemClassification.filler,                           35, 255),
    "Lemon Bunny Potion":                                      TeviItemData("Stat",    44966541_004, ItemClassification.filler,                           35, 255),
    "Cherry Bunny Potion":                                     TeviItemData("Stat",    44966541_005, ItemClassification.filler,                           35, 255),
    "Grape Bunny Potion":                                      TeviItemData("Stat",    44966541_006, ItemClassification.filler,                           35, 255),
    "Bag Expander":                                            TeviItemData("Stat",    44966541_007, ItemClassification.filler,                           5, 255),
    "Rainbow Bunny Potion":                                    TeviItemData("Stat",    44966541_008, ItemClassification.filler,                           15, 255),

    #custom items
    "500 Zennie Pack":                                         TeviItemData("Custom",   44966541_014,  ItemClassification.filler,                             591,585),
    "Magitite Shard":                                          TeviItemData("Upgrade",   44966541_015,  ItemClassification.progression,                             70,66),
    "Mananite Shard":                                          TeviItemData("Upgrade",   44966541_016,  ItemClassification.progression,                             97,93),

    #Items
    "Celia":                                                   TeviItemData("Weapon",    44966541_019, ItemClassification.progression),
    "Sable":                                                   TeviItemData("Weapon",    44966541_020, ItemClassification.progression),
    "Dagger":                                                  TeviItemData("Weapon",    44966541_022, ItemClassification.progression,                      3, 255),
    "Orbitars":                                                TeviItemData("Weapon",    44966541_023, ItemClassification.progression,                      3, 255),
    "Cross Bomb":                                              TeviItemData("Weapon",    44966541_024, ItemClassification.progression,                      3, 255),
    "Cluster Bomb":                                            TeviItemData("Weapon",    44966541_025, ItemClassification.progression,                      3, 255),
    "Bomb Fuel":                                               TeviItemData("Item",    44966541_026, ItemClassification.progression,                      3, 255),
    "Rabi Boots":                                              TeviItemData("Movement",    44966541_027, ItemClassification.progression,                      1, 255),
    "Running Boots":                                           TeviItemData("Movement",    44966541_028, ItemClassification.progression,                      3, 255),
    "Slick Boots":                                             TeviItemData("Movement",    44966541_029, ItemClassification.progression,                      1, 255),
    "Parkour Boots":                                           TeviItemData("Movement",    44966541_030, ItemClassification.progression,                      3, 255),
    "Double Rabi Boots":                                       TeviItemData("Movement",    44966541_031, ItemClassification.progression,                      1, 1),
    "Jetpack":                                                 TeviItemData("Movement",    44966541_032, ItemClassification.progression,                      3, 255),
    "Hydrodynamo":                                             TeviItemData("Movement",    44966541_033, ItemClassification.progression,                      1, 255),
    "PK Recon Badge":                                          TeviItemData("Item",    44966541_034, ItemClassification.useful,                           1, 255),
    "Decay Mask":                                              TeviItemData("Item",    44966541_035, ItemClassification.progression,                      3, 255),
    "Red Module Type-B":                                       TeviItemData("Item",    44966541_036, ItemClassification.progression,                      1, 255),
    "Red Module Type-C":                                       TeviItemData("Item",    44966541_037, ItemClassification.progression,                      1, 255),
    "Blue Module Type-B":                                      TeviItemData("Item",    44966541_038, ItemClassification.progression,                      1, 255),
    "Blue Module Type-C":                                      TeviItemData("Item",    44966541_039, ItemClassification.progression,                      1, 255),
    "Decay Antidote":                                          TeviItemData("Item",    44966541_040, ItemClassification.progression,                           1, 255),
    "Combustible":                                             TeviItemData("Item",    44966541_041, ItemClassification.progression,                      3, 255),
    "Slipstream Boots":                                        TeviItemData("Movement",    44966541_042, ItemClassification.progression,                      3, 255),
    "Tartarus VIP Pass":                                      TeviItemData("Item",    44966541_043, ItemClassification.progression),
    "Valhalla VIP Pass":                                       TeviItemData("Item",    44966541_044, ItemClassification.progression),
    "Royal Emblem":                                            TeviItemData("Item",    44966541_045, ItemClassification.useful),
    "Grip Sole Boots":                                         TeviItemData("Item",    44966541_046, ItemClassification.useful),
    "Explorer's Compass":                                      TeviItemData("Item",    44966541_047, ItemClassification.progression,                      3,   3),
    "Equilibrium Ring":                                        TeviItemData("Item",    44966541_048, ItemClassification.progression,                      3,   3),
    "Modular Blueprints":                                      TeviItemData("Item",    44966541_049, ItemClassification.progression,                      3, 255),
    "Core Module Type-U":                                      TeviItemData("Item",    44966541_050, ItemClassification.useful),
    "Core Module Type-D":                                      TeviItemData("Item",    44966541_051, ItemClassification.useful),
    "Deadly Reach":                                            TeviItemData("Item",    44966541_052, ItemClassification.progression,                      3, 255),
    "Shining Bangle":                                          TeviItemData("Item",    44966541_053, ItemClassification.progression,                      3, 255),
    "Spanner of Wisdom":                                       TeviItemData("Item",    44966541_054, ItemClassification.progression,                      3,   3),
    #"Notebook":                                               TeviItemData("Item",    44966541_055, ItemClassification.progression),
    "Delicious Secret Notes":                                  TeviItemData("Item",    44966541_056, ItemClassification.useful),
    "Rapid Shots Modchip":                                     TeviItemData("Item",    44966541_057, ItemClassification.progression,                      3,   4),
    #"Backpack":                                               TeviItemData("Item",    44966541_058, ItemClassification.progression),
    "Soul Burst Module":                                       TeviItemData("Item",    44966541_059, ItemClassification.progression,                      3, 255),
    "Trinketeer's Fortune":                                    TeviItemData("Item",    44966541_060, ItemClassification.progression,                      3, 255),
    "Alterscope":                                              TeviItemData("Item",    44966541_061, ItemClassification.useful),
    "Gilded Exultation":                                       TeviItemData("Item",    44966541_062, ItemClassification.useful),
    "Vortex Gloves":                                           TeviItemData("Item",    44966541_063, ItemClassification.progression,                      3, 255),
    "Airy Powder":                                             TeviItemData("Movement",    44966541_064, ItemClassification.progression),
    "Kitty Paw Charm":                                         TeviItemData("Item",    44966541_065, ItemClassification.useful),
    "Alembic Crystal":                                         TeviItemData("Item",    44966541_066, ItemClassification.progression),

    #Quest Items
    "Crystal Flute":                                           TeviItemData("Item",    44966541_099, ItemClassification.progression),
    "Memory Box":                                              TeviItemData("Item",    44966541_100, ItemClassification.progression),
    "Frozen Fate":                                             TeviItemData("Item",    44966541_102, ItemClassification.progression),
    "Gilded Left Hand":                                        TeviItemData("Item",    44966541_106, ItemClassification.progression),
    "Gilded Right Hand":                                       TeviItemData("Item",    44966541_107, ItemClassification.progression),
    "Nap Pillow":                                              TeviItemData("Item",    44966541_109, ItemClassification.progression),
    "Library Key":                                             TeviItemData("Item",    44966541_110, ItemClassification.progression),

    #Badges
    "Palladium":                                               TeviItemData("Badge",    44966541_120, ItemClassification.filler),
    "Backstab":                                                TeviItemData("Badge",    44966541_121, ItemClassification.filler),
    "C. Count Frenzy: Hotshot":                                TeviItemData("Badge",    44966541_122, ItemClassification.filler),
    "Health Plus":                                             TeviItemData("Badge",    44966541_123, ItemClassification.useful),
    "Celia Type-B: Prism":                                     TeviItemData("Badge",    44966541_124, ItemClassification.filler),
    "Knives Out":                                              TeviItemData("Badge",    44966541_125, ItemClassification.filler),
    "Red Haze":                                                TeviItemData("Badge",    44966541_126, ItemClassification.filler),
    "Dodge Enhancer: Upper":                                   TeviItemData("Badge",    44966541_127, ItemClassification.filler),
    "Dodge Enhancer: Spiral":                                  TeviItemData("Badge",    44966541_128, ItemClassification.filler),
    #"Dodge Enhancer: Airdash":                                TeviItemData("Badge",    44966541_129, ItemClassification.useful),
    "Dodge Enhancer: Spanner":                                 TeviItemData("Badge",    44966541_130, ItemClassification.filler),
    "Dodge Enhancer: Slide":                                   TeviItemData("Badge",    44966541_131, ItemClassification.filler),
    "EP Booster: Dodge":                                       TeviItemData("Badge",    44966541_132, ItemClassification.filler),
    "Style Combo: Windmill B":                                 TeviItemData("Badge",    44966541_133, ItemClassification.filler),
    "MP Surge: Tag Out":                                       TeviItemData("Badge",    44966541_134, ItemClassification.filler),
    "MP Surge: Concuss":                                       TeviItemData("Badge",    44966541_135, ItemClassification.filler),
    "Celia Type-A: Beguile":                                   TeviItemData("Badge",    44966541_136, ItemClassification.filler),
    "Lucky 7: A":                                              TeviItemData("Badge",    44966541_137, ItemClassification.filler),
    "MP Quicken: Accelerate":                                  TeviItemData("Badge",    44966541_138, ItemClassification.filler),
    "C. Count Frenzy: Acrobatics":                             TeviItemData("Badge",    44966541_139, ItemClassification.filler),
    "Upper Slash: Vicious":                                    TeviItemData("Badge",    44966541_140, ItemClassification.filler),
    "Titanium Spanner":                                        TeviItemData("Badge",    44966541_141, ItemClassification.filler),
    "Aerial Accel":                                            TeviItemData("Badge",    44966541_142, ItemClassification.filler),
    "Sable Type-A: Fanged":                                    TeviItemData("Badge",    44966541_143, ItemClassification.filler),
    "Invictus":                                                TeviItemData("Badge",    44966541_144, ItemClassification.filler),
    "Grub Guru":                                               TeviItemData("Badge",    44966541_145, ItemClassification.filler),
    "Intrepid Explorer":                                       TeviItemData("Badge",    44966541_146, ItemClassification.filler),
    "Heavy Metal":                                             TeviItemData("Badge",    44966541_147, ItemClassification.useful),
    "MP Surge: Battle Start":                                  TeviItemData("Badge",    44966541_148, ItemClassification.filler),
    "Aplomb":                                                  TeviItemData("Badge",    44966541_149, ItemClassification.filler),
    "MP Saver: Fireworks":                                     TeviItemData("Badge",    44966541_150, ItemClassification.useful),
    "C. Count Frenzy: Uprise":                                 TeviItemData("Badge",    44966541_151, ItemClassification.filler),
    "MP Surge: Dodge":                                         TeviItemData("Badge",    44966541_152, ItemClassification.filler),
    "MP Quicken: Step Up":                                     TeviItemData("Badge",    44966541_153, ItemClassification.filler),
    "Celia Type-A: Stunning":                                  TeviItemData("Badge",    44966541_154, ItemClassification.filler),
    "Dodge Recovery":                                          TeviItemData("Badge",    44966541_155, ItemClassification.filler),
    "Combo Crasher":                                           TeviItemData("Badge",    44966541_156, ItemClassification.filler),
    "Battlecry":                                               TeviItemData("Badge",    44966541_157, ItemClassification.filler),
    "Air Combo: Focus":                                        TeviItemData("Badge",    44966541_158, ItemClassification.filler),
    "Acrobat":                                                 TeviItemData("Badge",    44966541_159, ItemClassification.filler),
    "Aerial Kinetics":                                         TeviItemData("Badge",    44966541_160, ItemClassification.filler),
    "Mana Armor":                                              TeviItemData("Badge",    44966541_161, ItemClassification.useful),
    "Deft A":                                                  TeviItemData("Badge",    44966541_162, ItemClassification.useful),
    "Deft B":                                                  TeviItemData("Badge",    44966541_163, ItemClassification.useful),
    "Quickstab: Sunder":                                       TeviItemData("Badge",    44966541_164, ItemClassification.filler),
    "Combo Time Extend A ":                                    TeviItemData("Badge",    44966541_165, ItemClassification.filler),
    "Combo Time Extend B":                                     TeviItemData("Badge",    44966541_166, ItemClassification.filler),
    "Combo Time Extend C":                                     TeviItemData("Badge",    44966541_167, ItemClassification.filler),
    "Whipcrack":                                               TeviItemData("Badge",    44966541_168, ItemClassification.filler),
    "Combo Momentum: Fever":                                   TeviItemData("Badge",    44966541_169, ItemClassification.filler),
    "Two-pronged Shot":                                        TeviItemData("Badge",    44966541_170, ItemClassification.useful),
    "Full Stop A":                                             TeviItemData("Badge",    44966541_171, ItemClassification.filler),
    "Under Score":                                             TeviItemData("Badge",    44966541_172, ItemClassification.filler),
    "Upper Slash: Augment":                                    TeviItemData("Badge",    44966541_173, ItemClassification.filler),
    "Dodge: Panic Switch":                                     TeviItemData("Badge",    44966541_174, ItemClassification.filler),
    "C. Count Frenzy: Preemptive":                             TeviItemData("Badge",    44966541_175, ItemClassification.filler),
    "Health Surge":                                            TeviItemData("Badge",    44966541_176, ItemClassification.useful),
    "Glass Knife":                                             TeviItemData("Badge",    44966541_177, ItemClassification.useful),
    "Buns of Steel":                                           TeviItemData("Badge",    44966541_178, ItemClassification.filler),
    "Combo Momentum: Dodge":                                   TeviItemData("Badge",    44966541_179, ItemClassification.filler),
    "Break Extend":                                            TeviItemData("Badge",    44966541_180, ItemClassification.filler),
    "Nasty Break-up":                                          TeviItemData("Badge",    44966541_181, ItemClassification.useful),
    "MP Surge: Break":                                         TeviItemData("Badge",    44966541_182, ItemClassification.filler),
    "Combo Momentum: Saver":                                   TeviItemData("Badge",    44966541_183, ItemClassification.filler),
    "Perseverance A":                                          TeviItemData("Badge",    44966541_184, ItemClassification.filler),
    "EP Booster: Quintuple":                                   TeviItemData("Badge",    44966541_185, ItemClassification.filler),
    "Quick Break":                                             TeviItemData("Badge",    44966541_186, ItemClassification.useful),
    "Power Drop":                                              TeviItemData("Badge",    44966541_187, ItemClassification.useful),
    "Pogo Drop":                                               TeviItemData("Badge",    44966541_188, ItemClassification.useful),
    "Double Drop":                                             TeviItemData("Badge",    44966541_189, ItemClassification.useful),
    "Crystalline Scarlet":                                     TeviItemData("Badge",    44966541_190, ItemClassification.filler),
    "Crystalline Cyan":                                        TeviItemData("Badge",    44966541_191, ItemClassification.filler),
    "Terrestrial Agility":                                     TeviItemData("Badge",    44966541_192, ItemClassification.useful),
    "Aerial Agility":                                          TeviItemData("Badge",    44966541_193, ItemClassification.filler),
    "Galvanise":                                               TeviItemData("Badge",    44966541_194, ItemClassification.useful),
    "Orbital Efficiency A":                                    TeviItemData("Badge",    44966541_195, ItemClassification.filler),
    "Orbital Efficiency B":                                    TeviItemData("Badge",    44966541_196, ItemClassification.filler),
    "Quick Bomber":                                            TeviItemData("Badge",    44966541_197, ItemClassification.filler),
    "Quickstab: Lightning":                                    TeviItemData("Badge",    44966541_198, ItemClassification.filler),
    "Quickstab: Flurry":                                       TeviItemData("Badge",    44966541_199, ItemClassification.filler),
    #"Bombastic":                                              TeviItemData("Badge",    44966541_200, ItemClassification.useful),
    "Spiral Slash: Flurry":                                    TeviItemData("Badge",    44966541_201, ItemClassification.filler),
    "Spiral Slash: Cyclone":                                   TeviItemData("Badge",    44966541_202, ItemClassification.filler),
    "Bomb Pitcher":                                            TeviItemData("Badge",    44966541_203, ItemClassification.filler),
    "Style Combo: Flash A":                                    TeviItemData("Badge",    44966541_204, ItemClassification.filler),
    "High Defence Bomber":                                     TeviItemData("Badge",    44966541_205, ItemClassification.filler),
    "Low Defence Bomber":                                      TeviItemData("Badge",    44966541_206, ItemClassification.filler),
    "Style Combo: Triple Flash S":                             TeviItemData("Badge",    44966541_207, ItemClassification.filler),
    "Style Combo: Tornado A":                                  TeviItemData("Badge",    44966541_208, ItemClassification.filler),
    "Short Fuse":                                              TeviItemData("Badge",    44966541_209, ItemClassification.filler),
    "Style Combo: Lock On A":                                  TeviItemData("Badge",    44966541_210, ItemClassification.filler),
    "Style Combo: Bunny Kick S":                               TeviItemData("Badge",    44966541_211, ItemClassification.filler),
    "Style Combo: Trickshot":                                  TeviItemData("Badge",    44966541_212, ItemClassification.filler),
    "C. Rank Frenzy: Focus A":                                 TeviItemData("Badge",    44966541_213, ItemClassification.filler),
    "C. Rank Frenzy: Focus S":                                 TeviItemData("Badge",    44966541_214, ItemClassification.filler),
    "C. Rank Frenzy: Focus MAX":                               TeviItemData("Badge",    44966541_215, ItemClassification.filler),
    "Tornado Spin: Pressure":                                  TeviItemData("Badge",    44966541_216, ItemClassification.filler),
    "Unlucky 7":                                               TeviItemData("Badge",    44966541_217, ItemClassification.filler),
    "Core Expansion: Vitalize":                                TeviItemData("Badge",    44966541_218, ItemClassification.filler),
    "Cursed 6":                                                TeviItemData("Badge",    44966541_219, ItemClassification.filler),
    "Core Expansion: Charge":                                  TeviItemData("Badge",    44966541_220, ItemClassification.filler),
    "MP Quicken: Steady":                                      TeviItemData("Badge",    44966541_221, ItemClassification.filler),
    "MP Quicken: Style":                                       TeviItemData("Badge",    44966541_222, ItemClassification.filler),
    "MP Quicken: Combo":                                       TeviItemData("Badge",    44966541_223, ItemClassification.filler),
    "MP Surge: Recovery":                                      TeviItemData("Badge",    44966541_224, ItemClassification.filler),
    "Coffee Break":                                            TeviItemData("Badge",    44966541_225, ItemClassification.useful),
    "Sable Type-B: Malediction":                               TeviItemData("Badge",    44966541_226, ItemClassification.filler),
    "Core Expansion: Dazzle":                                  TeviItemData("Badge",    44966541_227, ItemClassification.filler),
    "Dodge: Optimize":                                         TeviItemData("Badge",    44966541_228, ItemClassification.filler),
    "C. Rank Frenzy: Attack":                                  TeviItemData("Badge",    44966541_229, ItemClassification.filler),
    "C. Rank Frenzy: Defend":                                  TeviItemData("Badge",    44966541_230, ItemClassification.filler),
    "Debuff Counter":                                          TeviItemData("Badge",    44966541_231, ItemClassification.filler),
    "Crystal Boon":                                            TeviItemData("Badge",    44966541_232, ItemClassification.filler),
    "Triple Threat":                                           TeviItemData("Badge",    44966541_233, ItemClassification.filler),
    "Dogfight":                                                TeviItemData("Badge",    44966541_234, ItemClassification.filler),
    "Magic Cannon":                                            TeviItemData("Badge",    44966541_235, ItemClassification.filler),
    "Dextrous":                                                TeviItemData("Badge",    44966541_236, ItemClassification.useful),
    "Hero Call":                                               TeviItemData("Badge",    44966541_237, ItemClassification.filler),
    "Dodge: Feeling Lucky":                                    TeviItemData("Badge",    44966541_238, ItemClassification.filler),
    "Buff Rush":                                               TeviItemData("Badge",    44966541_239, ItemClassification.filler),
    "Dodge: Discharge":                                        TeviItemData("Badge",    44966541_240, ItemClassification.filler),
    "Core Expansion: Recovery":                                TeviItemData("Badge",    44966541_241, ItemClassification.filler),
    "Punisher":                                                TeviItemData("Badge",    44966541_242, ItemClassification.filler),
    "Synchronized Support II":                                 TeviItemData("Badge",    44966541_243, ItemClassification.filler),
    "Celia Type-B: Halo":                                      TeviItemData("Badge",    44966541_244, ItemClassification.filler),
    "Bounce Bonus":                                            TeviItemData("Badge",    44966541_245, ItemClassification.filler),
    "MP Reset A":                                              TeviItemData("Badge",    44966541_246, ItemClassification.filler),
    "MP Reset B":                                              TeviItemData("Badge",    44966541_247, ItemClassification.filler),
    "EP Booster: Perfectionist":                               TeviItemData("Badge",    44966541_248, ItemClassification.filler),
    "Core Expansion: Extend":                                  TeviItemData("Badge",    44966541_249, ItemClassification.filler),
    "Backflip Flurry":                                         TeviItemData("Badge",    44966541_250, ItemClassification.filler),
    "Shock Armor":                                             TeviItemData("Badge",    44966541_251, ItemClassification.filler),
    "Head Over Heels":                                         TeviItemData("Badge",    44966541_252, ItemClassification.filler),
    "Dual Combo: Flow":                                        TeviItemData("Badge",    44966541_253, ItemClassification.filler),
    "Dual Combo: Rush":                                        TeviItemData("Badge",    44966541_254, ItemClassification.filler),
    "Perseverance D":                                          TeviItemData("Badge",    44966541_255, ItemClassification.filler),
    "Perseverance B":                                          TeviItemData("Badge",    44966541_256, ItemClassification.filler),
    "EP Booster: Variety":                                     TeviItemData("Badge",    44966541_257, ItemClassification.filler),
    "MP Surge: Brawl":                                         TeviItemData("Badge",    44966541_258, ItemClassification.filler),
    "Perseverance C":                                          TeviItemData("Badge",    44966541_259, ItemClassification.filler),
    "Rapid Shots Enhance":                                     TeviItemData("Badge",    44966541_260, ItemClassification.filler),
    "EP Booster: HP":                                          TeviItemData("Badge",    44966541_261, ItemClassification.filler),
    "Sable Type-A: Ensnare":                                   TeviItemData("Badge",    44966541_262, ItemClassification.filler),
    "Celia Type-A: Meteoric":                                  TeviItemData("Badge",    44966541_263, ItemClassification.filler),
    "Sable Type-B: Backlash":                                  TeviItemData("Badge",    44966541_264, ItemClassification.filler),
    "Sable Type-C: Ignite":                                    TeviItemData("Badge",    44966541_265, ItemClassification.filler),
    "MP Quicken: Bloodlust":                                   TeviItemData("Badge",    44966541_266, ItemClassification.useful),
    "MP Quicken: Sacrifice":                                   TeviItemData("Badge",    44966541_267, ItemClassification.filler),
    "MP Saver: Rhythm":                                        TeviItemData("Badge",    44966541_268, ItemClassification.filler),
    "Swift Shots":                                             TeviItemData("Badge",    44966541_269, ItemClassification.filler),
    "Dodge: Golden Luck":                                      TeviItemData("Badge",    44966541_270, ItemClassification.filler),
    "Sable Type-A: Voracious":                                 TeviItemData("Badge",    44966541_271, ItemClassification.filler),
    "Celia Type-C: Barrage":                                   TeviItemData("Badge",    44966541_272, ItemClassification.filler),
    "Celia Type-C: Panoptic":                                  TeviItemData("Badge",    44966541_273, ItemClassification.filler),
    "Sable Type-C: Fervid":                                    TeviItemData("Badge",    44966541_274, ItemClassification.filler),
    "Blood Magic":                                             TeviItemData("Badge",    44966541_275, ItemClassification.filler),
    "The Untamed":                                             TeviItemData("Badge",    44966541_276, ItemClassification.filler),
    "MP Quicken: Melee":                                       TeviItemData("Badge",    44966541_277, ItemClassification.filler),
    "Synchronized Support I":                                  TeviItemData("Badge",    44966541_278, ItemClassification.filler),
    "Ranged Roulette":                                         TeviItemData("Badge",    44966541_279, ItemClassification.filler),
    "Lucky 7: B":                                              TeviItemData("Badge",    44966541_280, ItemClassification.filler),
    "Attenu-8":                                                TeviItemData("Badge",    44966541_281, ItemClassification.filler),
    "Supercluster Bomb":                                       TeviItemData("Badge",    44966541_282, ItemClassification.filler),
    "Crouching Bunny":                                         TeviItemData("Badge",    44966541_283, ItemClassification.filler),
    "Tornado Spin: Flurry":                                    TeviItemData("Badge",    44966541_284, ItemClassification.filler),
    "Tornado Spin: Grav Reversal":                             TeviItemData("Badge",    44966541_285, ItemClassification.filler),
    "EP Booster: Melee Menace":                                TeviItemData("Badge",    44966541_286, ItemClassification.filler),
    "Dodge: Headstrong":                                       TeviItemData("Badge",    44966541_287, ItemClassification.filler),
    "Aerial Assist":                                           TeviItemData("Badge",    44966541_288, ItemClassification.filler),
    "Lucky 7: C":                                              TeviItemData("Badge",    44966541_289, ItemClassification.filler),
    "Ballasting Off":                                          TeviItemData("Badge",    44966541_290, ItemClassification.filler),
    "Life Steal":                                              TeviItemData("Badge",    44966541_291, ItemClassification.filler),
    "MP Surge: Explosives":                                    TeviItemData("Badge",    44966541_292, ItemClassification.filler),
    "EP Booster: MP":                                          TeviItemData("Badge",    44966541_293, ItemClassification.filler),
    "Mana Flare":                                              TeviItemData("Badge",    44966541_294, ItemClassification.filler),
    "Double Airstrike":                                        TeviItemData("Badge",    44966541_295, ItemClassification.filler),
    "Spanner Bash: Wrecker":                                   TeviItemData("Badge",    44966541_296, ItemClassification.filler),
    "Supernova":                                               TeviItemData("Badge",    44966541_297, ItemClassification.useful),
    "Daisy Chain":                                             TeviItemData("Badge",    44966541_298, ItemClassification.filler),
    "Blood Armor":                                             TeviItemData("Badge",    44966541_299, ItemClassification.useful),
    "Even Keel":                                               TeviItemData("Badge",    44966541_300, ItemClassification.filler),
    "Enthusiastic Excavator":                                  TeviItemData("Badge",    44966541_301, ItemClassification.filler),
    "MP Surge: Soul":                                          TeviItemData("Badge",    44966541_302, ItemClassification.filler),
    "Auto Heal":                                               TeviItemData("Badge",    44966541_303, ItemClassification.filler),
    "Headbutt":                                                TeviItemData("Badge",    44966541_304, ItemClassification.filler),
    "Bulletproof Pillar S":                                    TeviItemData("Badge",    44966541_305, ItemClassification.filler),
    "Bulletproof Pillar C":                                    TeviItemData("Badge",    44966541_306, ItemClassification.filler),
    "MP Quicken: Battlescars":                                 TeviItemData("Badge",    44966541_307, ItemClassification.filler),
    "Excuse Me":                                               TeviItemData("Badge",    44966541_308, ItemClassification.filler),
    "Slash Quartet":                                           TeviItemData("Badge",    44966541_309, ItemClassification.filler),
    "Thick Pillar":                                            TeviItemData("Badge",    44966541_310, ItemClassification.filler),
    "Dominator":                                               TeviItemData("Badge",    44966541_311, ItemClassification.filler),
    "Drop Kick":                                               TeviItemData("Badge",    44966541_312, ItemClassification.filler),
    "Crystal Shrapnel":                                        TeviItemData("Badge",    44966541_313, ItemClassification.filler),
    "Slide Basher":                                            TeviItemData("Badge",    44966541_314, ItemClassification.filler),
    "Refractor":                                               TeviItemData("Badge",    44966541_315, ItemClassification.filler),
    "MP Quicken: Sugar Rush":                                  TeviItemData("Badge",    44966541_316, ItemClassification.filler),
    "Terrestrial Momentum":                                    TeviItemData("Badge",    44966541_317, ItemClassification.filler),
    "Crystal Mirror":                                          TeviItemData("Badge",    44966541_318, ItemClassification.filler),
    "Ground Control":                                          TeviItemData("Badge",    44966541_319, ItemClassification.filler),
    "Bone Breaker":                                            TeviItemData("Badge",    44966541_320, ItemClassification.filler),
    "Act Tough":                                               TeviItemData("Badge",    44966541_321, ItemClassification.filler),
    "Razor Arrow":                                             TeviItemData("Badge",    44966541_322, ItemClassification.filler),
    "Style Combo: Afterimage S":                               TeviItemData("Badge",    44966541_323, ItemClassification.useful),
    "Sigil Quicken":                                           TeviItemData("Badge",    44966541_324, ItemClassification.filler),
    "Blood Boil":                                              TeviItemData("Badge",    44966541_325, ItemClassification.filler),
    "Core Expansion: Erase":                                   TeviItemData("Badge",    44966541_326, ItemClassification.filler),
    "Crystal Healing":                                         TeviItemData("Badge",    44966541_327, ItemClassification.filler),
    "Core Expansion: Transcend":                               TeviItemData("Badge",    44966541_328, ItemClassification.filler),
    "Core Expansion: Combo":                                   TeviItemData("Badge",    44966541_329, ItemClassification.filler),
    "Supersonic":                                              TeviItemData("Badge",    44966541_330, ItemClassification.progression),
    "Crystallize":                                             TeviItemData("Badge",    44966541_331, ItemClassification.filler),
    "Hot Buzz":                                                TeviItemData("Badge",    44966541_332, ItemClassification.filler),
    "EP Booster: Shopaholic":                                  TeviItemData("Badge",    44966541_333, ItemClassification.filler),
    "EP Booster: Synthesizer":                                 TeviItemData("Badge",    44966541_334, ItemClassification.filler),
    "Muscle Memory":                                           TeviItemData("Badge",    44966541_335, ItemClassification.filler),
    "Slayer":                                                  TeviItemData("Badge",    44966541_336, ItemClassification.filler),
    "Shooting Star":                                           TeviItemData("Badge",    44966541_337, ItemClassification.filler),
    "Upper Slash: Shatter":                                    TeviItemData("Badge",    44966541_338, ItemClassification.filler),
    "Core Expansion: Radiant":                                 TeviItemData("Badge",    44966541_339, ItemClassification.filler),
    "Core Expansion: Saver":                                   TeviItemData("Badge",    44966541_340, ItemClassification.filler),
    "Overdrive":                                               TeviItemData("Badge",    44966541_341, ItemClassification.useful),
    "C. Rank Frenzy: Fierce":                                  TeviItemData("Badge",    44966541_342, ItemClassification.filler),
    "Fast Pillar":                                             TeviItemData("Badge",    44966541_343, ItemClassification.filler),
    "Spanner Bash: Bounce":                                    TeviItemData("Badge",    44966541_344, ItemClassification.filler),
    "Upper Slash: Volley":                                     TeviItemData("Badge",    44966541_345, ItemClassification.filler),
    "Electric Wind":                                           TeviItemData("Badge",    44966541_346, ItemClassification.filler),
    "Style Combo: Upper A":                                    TeviItemData("Badge",    44966541_347, ItemClassification.filler),
    "Style Combo: Power A":                                    TeviItemData("Badge",    44966541_348, ItemClassification.filler),
    "Style Combo: Aerial A":                                   TeviItemData("Badge",    44966541_349, ItemClassification.filler),
    "Slide Halt":                                              TeviItemData("Badge",    44966541_350, ItemClassification.filler),
    "Metamorphose":                                            TeviItemData("Badge",    44966541_351, ItemClassification.filler),
    "Style Combo: Backbomb S":                                 TeviItemData("Badge",    44966541_352, ItemClassification.useful),
    "C. Rank Frenzy: Starter":                                 TeviItemData("Badge",    44966541_353, ItemClassification.filler),
    "Windmill Strike":                                         TeviItemData("Badge",    44966541_354, ItemClassification.filler),
    "Orbital Slash":                                           TeviItemData("Badge",    44966541_355, ItemClassification.filler),
    "Spring Back":                                             TeviItemData("Badge",    44966541_356, ItemClassification.filler),
    "Bombard":                                                 TeviItemData("Badge",    44966541_357, ItemClassification.useful),
    "Shell Shock":                                             TeviItemData("Badge",    44966541_358, ItemClassification.filler),
    "Biscuit Delivery":                                        TeviItemData("Badge",    44966541_359, ItemClassification.filler),
    "Full Stop B":                                             TeviItemData("Badge",    44966541_360, ItemClassification.filler),
    "Magic Mixer":                                             TeviItemData("Badge",    44966541_361, ItemClassification.filler),
    "Inhale Dessert":                                          TeviItemData("Badge",    44966541_362, ItemClassification.filler),
    "Combo Assist":                                            TeviItemData("Badge",    44966541_363, ItemClassification.filler),
    "Flash Point":                                             TeviItemData("Badge",    44966541_364, ItemClassification.filler),
    "Special Action: Question Mark":                           TeviItemData("Badge",    44966541_365, ItemClassification.filler),
    "Special Action: Show Off":                                TeviItemData("Badge",    44966541_366, ItemClassification.filler),
    "Special Action: Paparazzo":                               TeviItemData("Badge",    44966541_367, ItemClassification.filler),
    "Special Action: Speechless":                              TeviItemData("Badge",    44966541_368, ItemClassification.filler),
    "Special Action: Yawn":                                    TeviItemData("Badge",    44966541_369, ItemClassification.filler),
    "Special Action: Olive Branch":                            TeviItemData("Badge",    44966541_370, ItemClassification.filler),
    "Weak Dominance A":                                        TeviItemData("Badge",    44966541_371, ItemClassification.filler),
    "Weak Dominance B":                                        TeviItemData("Badge",    44966541_372, ItemClassification.filler),
    "Armor Piercer":                                           TeviItemData("Badge",    44966541_373, ItemClassification.filler),
    "Core Expansion: Full Offense":                            TeviItemData("Badge",    44966541_374, ItemClassification.filler),
    "Range Break":                                             TeviItemData("Badge",    44966541_375, ItemClassification.filler),
    "Mana Platform":                                           TeviItemData("Badge",    44966541_376, ItemClassification.useful),
    "Go Ballistic":                                            TeviItemData("Badge",    44966541_377, ItemClassification.useful),

    #Consumeables
    "Cocoa Truffles":                                          TeviItemData("Consumeable",  44966541_380, ItemClassification.filler,0,999999), 
    "Fluffy Cream Puff":                                       TeviItemData("Consumeable",  44966541_381, ItemClassification.filler,0,999999), 
    "Vitalolly":                                               TeviItemData("Consumeable",  44966541_382, ItemClassification.filler,0,999999), 
    "Energy Happy Juice":                                      TeviItemData("Consumeable",  44966541_383, ItemClassification.filler,0,999999), 
    "Crispy Crunchsicle":                                      TeviItemData("Consumeable",  44966541_384, ItemClassification.filler,0,999999), 
    "Rewind Donut":                                            TeviItemData("Consumeable",  44966541_385, ItemClassification.filler,0,999999), 
    "Voodoo's Mewmew Cookie":                                  TeviItemData("Consumeable",  44966541_386, ItemClassification.filler,0,999999), 
    "Snowflake Rumi Cake":                                     TeviItemData("Consumeable",  44966541_387, ItemClassification.filler,0,999999), 
    "Rainbowba":                                               TeviItemData("Consumeable",  44966541_388, ItemClassification.filler,0,999999), 
    "Waffle of Wonder (Attempt)":                              TeviItemData("Consumeable",  44966541_389, ItemClassification.filler,0,999999), 
    "Mysterious Confection":                                   TeviItemData("Consumeable",  44966541_390, ItemClassification.filler,0,999999), 
    "Honeycloud Waffle":                                       TeviItemData("Consumeable",  44966541_391, ItemClassification.filler,1,999999), 
    "Toasted Meringue Waffle":                                 TeviItemData("Consumeable",  44966541_392, ItemClassification.filler,1,999999), 
    "Good Morning Waffle":                                     TeviItemData("Consumeable",  44966541_393, ItemClassification.filler,1,999999), 
    "Berry Pink Waffle":                                       TeviItemData("Consumeable",  44966541_394, ItemClassification.filler,1,999999), 
    "Blueberry Waffle":                                        TeviItemData("Consumeable",  44966541_395, ItemClassification.filler,1,999999), 
    "Whimsical Waffle of Wonder":                              TeviItemData("Consumeable",  44966541_396, ItemClassification.filler,0,999999), 
    #"Silver Bell":                                            TeviItemData("Consumeable",  44966541_397, ItemClassification.filler), 
    "Void Bomb":                                               TeviItemData("Consumeable",  44966541_398, ItemClassification.progression,1,999999), 
    "Cloud Bomb":                                              TeviItemData("Consumeable",  44966541_399, ItemClassification.progression,1,999999), 
    "BB Rabbit":                                               TeviItemData("Consumeable",  44966541_400, ItemClassification.progression,1,999999), 
    "Calico Bomb":                                             TeviItemData("Consumeable",  44966541_401, ItemClassification.progression,1,999999), 
    "Tabby Bomb":                                              TeviItemData("Consumeable",  44966541_402, ItemClassification.progression,1,999999), 
    "Memorial Bookmark":                                       TeviItemData("Consumeable",  44966541_403, ItemClassification.filler,0,0), 
    "Burnt Dessert":                                           TeviItemData("Consumeable",  44966541_404, ItemClassification.filler,0,999999), 
    "Pocket Biscuit":                                          TeviItemData("Consumeable",  44966541_405, ItemClassification.filler,0,999999) 
    }

teleporter_table: Dict[str,TeviItemData] = {
    "Teleporter Desert Base":                                       TeviItemData("Teleporter",  44966541_500, ItemClassification.progression,1,1), 
    "Teleporter Canyon":                                            TeviItemData("Teleporter",  44966541_501, ItemClassification.progression,1,1), 
    "Teleporter Oasis":                                             TeviItemData("Teleporter",  44966541_502, ItemClassification.progression,1,1), 
    "Teleporter Morose":                                            TeviItemData("Teleporter",  44966541_503, ItemClassification.progression,1,1), 
    "Teleporter ForestMaze":                                        TeviItemData("Teleporter",  44966541_504, ItemClassification.progression,1,1), 
    "Teleporter Forest":                                            TeviItemData("Teleporter",  44966541_505, ItemClassification.progression,1,1), 
    "Teleporter Mines":                                             TeviItemData("Teleporter",  44966541_506, ItemClassification.progression,1,1), 
    "Teleporter Industry":                                          TeviItemData("Teleporter",  44966541_507, ItemClassification.progression,1,1), 
    "Teleporter Copper Forest":                                     TeviItemData("Teleporter",  44966541_508, ItemClassification.progression,1,1), 
    "Teleporter Anathema":                                          TeviItemData("Teleporter",  44966541_509, ItemClassification.progression,1,1), 
    "Teleporter Gloamwood":                                         TeviItemData("Teleporter",  44966541_510, ItemClassification.progression,1,1), 
    "Teleporter Plague":                                            TeviItemData("Teleporter",  44966541_511, ItemClassification.progression,1,1), 
    "Teleporter Ulvosa":                                            TeviItemData("Teleporter",  44966541_512, ItemClassification.progression,1,1), 
    "Teleporter Snow Village":                                      TeviItemData("Teleporter",  44966541_513, ItemClassification.progression,1,1), 
    "Teleporter Sea":                                               TeviItemData("Teleporter",  44966541_514, ItemClassification.progression,1,1), 
    "Teleporter Ocean":                                             TeviItemData("Teleporter",  44966541_515, ItemClassification.progression,1,1), 
    "Teleporter Forgotten City":                                    TeviItemData("Teleporter",  44966541_516, ItemClassification.progression,1,1), 
    "Teleporter Tartarus":                                          TeviItemData("Teleporter",  44966541_517, ItemClassification.progression,1,1), 
    "Teleporter Snow City":                                         TeviItemData("Teleporter",  44966541_518, ItemClassification.progression,1,1), 
    "Teleporter Magma Depths":                                      TeviItemData("Teleporter",  44966541_519, ItemClassification.progression,1,1), 
    "Teleporter Dreamkeeper Outside":                               TeviItemData("Teleporter",  44966541_520, ItemClassification.progression,1,1), 
    "Teleporter Dreamkeeper Inside":                                TeviItemData("Teleporter",  44966541_521, ItemClassification.progression,1,1), 
    "Teleporter Deep Dream":                                        TeviItemData("Teleporter",  44966541_522, ItemClassification.progression,1,1), 
    "Teleporter Valhalla Breath East":                              TeviItemData("Teleporter",  44966541_523, ItemClassification.progression,1,1), 
    "Teleporter Valhalla City":                                     TeviItemData("Teleporter",  44966541_524, ItemClassification.progression,1,1), 
    "Teleporter Heavens Valley West":                               TeviItemData("Teleporter",  44966541_525, ItemClassification.progression,1,1), 
    "Teleporter Valhalla Breath West":                              TeviItemData("Teleporter",  44966541_526, ItemClassification.progression,1,1), 
    "Teleporter Ruins":                                             TeviItemData("Teleporter",  44966541_527, ItemClassification.progression,1,1), 
    "Teleporter Sinner's Hell":                                     TeviItemData("Teleporter",  44966541_528, ItemClassification.progression,1,1), 
    "Teleporter Relicts":                                           TeviItemData("Teleporter",  44966541_529, ItemClassification.progression,1,1), 
    "Teleporter Catacombs":                                         TeviItemData("Teleporter",  44966541_530, ItemClassification.progression,1,1), 
    "Teleporter Lab":                                               TeviItemData("Teleporter",  44966541_531, ItemClassification.progression,1,1), 
    "Teleporter Cloister":                                          TeviItemData("Teleporter",  44966541_532, ItemClassification.progression,1,1), 
    "Teleporter Gallery of Mirrors":                                TeviItemData("Teleporter",  44966541_533, ItemClassification.progression,1,1), 
    "Teleporter Gallery of Souls":                                  TeviItemData("Teleporter",  44966541_534, ItemClassification.progression,1,1), 
    "Teleporter Blushwood":                                         TeviItemData("Teleporter",  44966541_535, ItemClassification.progression,1,1), 
    "Teleporter Evernight Garden":                                  TeviItemData("Teleporter",  44966541_536, ItemClassification.progression,1,1), 
}

event_item_table: Dict[str, TeviItem] = {

}