import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class RefunctItem(Item):
    game: str = "Refunct"
    button_nr: int


item_table = {f"Trigger Cluster {i}": ItemData(10000000 + i, ItemClassification.progression) for i in range(2, 31)}
item_table["Grass"] = ItemData(9999999, ItemClassification.progression_skip_balancing) 
item_table[":)"] = ItemData(9999998, ItemClassification.filler) 
item_table["Victory Location"] = ItemData(9999997, ItemClassification.progression)

for i in range(0, 101):
    item_table[f"DEBUGA {i}"] = ItemData(20000000 + i, ItemClassification.filler)
    item_table[f"DEBUGB {i}"] = ItemData(30000000 + i, ItemClassification.filler)