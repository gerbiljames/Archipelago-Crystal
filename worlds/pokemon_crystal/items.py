from random import Random
from typing import TYPE_CHECKING

from . import options
from BaseClasses import Item, ItemClassification
from .data import data
from .options import Shopsanity, ItemPoolFill

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


class PokemonCrystalItem(Item):
    game: str = "Pokemon Crystal"
    tags: frozenset[str]
    price: int

    def __init__(self, name: str, classification: ItemClassification, code: int | None, player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
            self.price = 0
        else:
            item = data.items[code]
            self.tags = item.tags
            self.price = item.price


def create_item_label_to_code_map() -> dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    return {attributes.label: item_value for item_value, attributes in data.items.items()}


def get_item_classification(item_code: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[item_code].classification


def get_item_price(item_code: int) -> int:
    return data.items[item_code].price


def item_const_name_to_id(const_name):
    ids = [item_id for item_id, item_data in data.items.items() if item_data.item_const == const_name]
    if ids:
        return ids[0]
    return 0
       

def get_random_filler_item(world: "PokemonCrystalWorld"):
    if world.options.item_pool_fill == ItemPoolFill.option_balanced:
        weighted_pool = [["RARE_CANDY", "ETHER", "ELIXER", "MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY", "WATER_STONE",
                        "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE", "MOON_STONE", "ESCAPE_ROPE", "NUGGET", 
                        "STAR_PIECE", "STARDUST", "PEARL", "BIG_PEARL", "POKE_BALL", "GREAT_BALL", "ULTRA_BALL", "POTION", 
                        "SUPER_POTION", "ENERGY_ROOT", "ENERGYPOWDER", "HYPER_POTION", "FULL_RESTORE", "REPEL", "SUPER_REPEL", 
                        "MAX_REPEL", "REVIVE", "REVIVAL_HERB", "MAX_REVIVE", "HP_UP", "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", 
                        "IRON", "GUARD_SPEC", "DIRE_HIT", "X_ATTACK", "X_DEFEND", "X_SPEED", "X_SPECIAL", "HEAL_POWDER", "BURN_HEAL", 
                        "PARLYZ_HEAL", "ICE_HEAL", "ANTIDOTE", "AWAKENING", "FULL_HEAL"] * 2, ["TWISTEDSPOON", "BRIGHTPOWDER", "LUCKY_EGG", "LEFTOVERS", "MAGNET", "MYSTIC_WATER", "FOCUS_BAND"] * 1]
    elif world.options.item_pool_fill == ItemPoolFill.option_youngster:
        weighted_pool = [["RARE_CANDY", "ESCAPE_ROPE"] * 11, ["ETHER", "ELIXER", "MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY"] * 9,
                        ["WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE", "MOON_STONE"] * 2,
                        ["GREAT_BALL"] * 1, ["POTION", "POKE_BALL", "REPEL"] * 12, ["SUPER_POTION", "ENERGY_ROOT", "ENERGYPOWDER", "SUPER_REPEL"] * 2,
                        ["HYPER_POTION", "FULL_RESTORE"] * 1, ["MAX_REPEL"] * 1,
                        ["REVIVE", "REVIVAL_HERB"] * 5 + ["MAX_REVIVE"] * 1,
                        ["HP_UP", "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", "IRON"] * 1,
                        ["HEAL_POWDER", "BURN_HEAL", "PARLYZ_HEAL", "ICE_HEAL", "ANTIDOTE", "AWAKENING", "FULL_HEAL"] * 2]
    elif world.options.item_pool_fill == ItemPoolFill.option_cooltrainer:
        weighted_pool = [["RARE_CANDY", "ESCAPE_ROPE"] * 11, ["MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY"] * 9,
                        ["WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE", "MOON_STONE"] * 5,
                        ["SUPER_POTION", "ENERGY_ROOT", "ENERGYPOWDER", "SUPER_REPEL"] * 1, ["NUGGET", "STAR_PIECE", "STARDUST", "PEARL", "BIG_PEARL"] * 5,
                        ["GUARD_SPEC", "DIRE_HIT", "X_ATTACK", "X_DEFEND", "X_SPEED", "X_SPECIAL"] * 10,
                        ["HYPER_POTION", "FULL_RESTORE", "MAX_REPEL"] * 10, ["REVIVE", "REVIVAL_HERB"] * 5 + ["MAX_REVIVE"] * 10,
                        ["ULTRA_BALL"] * 4, ["TWISTEDSPOON", "BRIGHTPOWDER", "LUCKY_EGG", "LEFTOVERS", "MAGNET", "MYSTIC_WATER", "FOCUS_BAND"] * 1
                        ["HP_UP", "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", "IRON"] * 10,
                        ["HEAL_POWDER", "BURN_HEAL", "PARLYZ_HEAL", "ICE_HEAL", "ANTIDOTE", "AWAKENING", "FULL_HEAL"] * 2]
    elif world.options.item_pool_fill == ItemPoolFill.option_vanilla:
        # weights are roughly based on vanilla occurrence
        weighted_pool = [["RARE_CANDY"] * 3, ["ETHER", "ELIXER", "MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY"] * 5,
                        ["WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE", "MOON_STONE"] * 2,
                        ["ESCAPE_ROPE"] * 3, ["NUGGET", "STAR_PIECE", "STARDUST", "PEARL", "BIG_PEARL"] * 2,
                        ["POKE_BALL", "GREAT_BALL", "ULTRA_BALL"] * 5,
                        ["POTION", "SUPER_POTION", "ENERGY_ROOT", "ENERGYPOWDER"] * 12,
                        ["HYPER_POTION", "FULL_RESTORE"] * 2, ["REPEL", "SUPER_REPEL", "MAX_REPEL"] * 3,
                        ["REVIVE", "REVIVAL_HERB"] * 4 + ["MAX_REVIVE"] * 2,
                        ["HP_UP", "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", "IRON"] * 5,
                        ["GUARD_SPEC", "DIRE_HIT", "X_ATTACK", "X_DEFEND", "X_SPEED", "X_SPECIAL"] * 2,
                        ["HEAL_POWDER", "BURN_HEAL", "PARLYZ_HEAL", "ICE_HEAL", "ANTIDOTE", "AWAKENING", "FULL_HEAL"] * 5]
    else:
        # oops :)
        weighted_pool = [["NUGGET"] * 100]
    group = world.random.choice(weighted_pool)
    return world.random.choice(group)


def get_random_ball(random: Random):
    balls = ["POKE_BALL", "GREAT_BALL", "ULTRA_BALL", "FRIEND_BALL", "HEAVY_BALL", "LOVE_BALL", "LEVEL_BALL",
             "LURE_BALL", "FAST_BALL"]
    ball_weights = [50, 30, 20, 1, 1, 1, 1, 1, 1]
    return random.choices(balls, weights=ball_weights)[0]


def item_const_name_to_label(const_name):
    labels = [item_data.label for _item_id, item_data in data.items.items() if item_data.item_const == const_name]
    if labels:
        return labels[0]
    return "Poke Ball"


def adjust_item_classifications(world: "PokemonCrystalWorld"):
    if Shopsanity.blue_card in world.options.shopsanity.value:
        for item in world.itempool:
            if item.name == "Blue Card":
                item.classification = ItemClassification.progression

    if Shopsanity.apricorns in world.options.shopsanity.value:
        for item in world.itempool:
            if "Apricorn" in item.tags:
                item.classification = ItemClassification.progression

    if world.options.require_itemfinder:
        for item in world.itempool:
            if item.name == "Itemfinder":
                item.classification = ItemClassification.progression


ITEM_GROUPS = {
    "Badges": {item.label for item in data.items.values() if "Badge" in item.tags},
    "Johto Badges": {item.label for item in data.items.values() if "JohtoBadge" in item.tags},
    "Kanto Badges": {item.label for item in data.items.values() if "KantoBadge" in item.tags},
    "HMs": {item.label for item in data.items.values() if "HM" in item.tags},
    "TMs": {item.label for item in data.items.values() if "TM" in item.tags},
    "Gear": {item.label for item in data.items.values() if "Gear" in item.tags},
    "Traps": {item.label for item in data.items.values() if "Trap" in item.tags},
    "Rods": {item.label for item in data.items.values() if "Rod" in item.tags},
    "Key Items": {item.label for item in data.items.values() if "KeyItem" in item.tags},
    "Fly Unlocks": {item.label for item in data.items.values() if "Fly" in item.tags},
    "Kanto Tickets": {"Pass", "S.S. Ticket"},
    "Ruins of Alph chamber unlocks": {"Water Stone", "HM05 Flash", "Escape Rope", "Rainbow Wing"},
    "Tin Tower access": {"Rainbow Wing", "Clear Bell"},
    "Apricorns": {item.label for item in data.items.values() if "Apricorn" in item.tags},
    "HM01": {"HM01 Cut"},
    "HM02": {"HM02 Fly"},
    "HM03": {"HM03 Surf"},
    "HM04": {"HM04 Strength"},
    "HM05": {"HM05 Flash"},
    "HM06": {"HM06 Whirlpool"},
    "HM07": {"HM07 Waterfall"},
    "TM02 Headbutt": {"TM02"},
    "TM08 Rock Smash": {"TM08"}
}
