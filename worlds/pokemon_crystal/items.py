from BaseClasses import Item, ItemClassification
from .data import data


class PokemonCrystalItem(Item):
    game: str = "Pokemon Crystal"
    tags: frozenset[str]

    def __init__(self, name: str, classification: ItemClassification, code: int | None, player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[code].tags


def create_item_label_to_code_map() -> dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    label_to_code_map: dict[str, int] = {}
    for item_value, attributes in data.items.items():
        label_to_code_map[attributes.label] = item_value

    return label_to_code_map


def get_item_classification(item_code: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[item_code].classification


def item_const_name_to_id(const_name):
    ids = [item_id for item_id, item_data in data.items.items() if item_data.item_const == const_name]
    if ids:
        return ids[0]
    return 0


def item_const_name_to_label(const_name):
    labels = [item_data.label for _item_id, item_data in data.items.items() if item_data.item_const == const_name]
    if len(labels):
        return labels[0]
    return "Poke Ball"


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
    "Kanto Tickets": {"Pass", "S.S. Ticket"},
    "Ruins of Alph chamber unlocks": {"Water Stone", "HM05 Flash", "Escape Rope", "Rainbow Wing"},
    "Tin Tower access": {"Rainbow Wing", "Clear Bell"},
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
