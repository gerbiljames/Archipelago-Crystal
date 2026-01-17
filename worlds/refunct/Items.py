import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class RefunctItem(Item):
    game: str = "Refunct"
    button_nr: int


item_table = {f"Trigger Cluster {i}": ItemData(10000000 + i, ItemClassification.progression) for i in range(1, 31)}
item_table["Grass"] = ItemData(9999999, ItemClassification.progression_deprioritized_skip_balancing) 
item_table["Starting Platform"] = ItemData(9999998, ItemClassification.filler) 
item_table["Final Platform"] = ItemData(9999997, ItemClassification.progression)
item_table[":)"] = ItemData(9999996, ItemClassification.filler)

item_table["Ledge Grab"] = ItemData(9999990, ItemClassification.progression | ItemClassification.useful)
item_table["Progressive Wall Jump"] = ItemData(9999991, ItemClassification.progression | ItemClassification.useful)
item_table["Swim"] = ItemData(9999992, ItemClassification.progression | ItemClassification.useful)
item_table["Jump Pads"] = ItemData(9999993, ItemClassification.progression)
item_table["Pipes"] = ItemData(9999994, ItemClassification.progression)
item_table["Lifts"] = ItemData(9999995, ItemClassification.progression)

item_table["Cubes Bag"] = ItemData(9999989, ItemClassification.progression)

item_table["Flower"] = ItemData(9999981, ItemClassification.filler)

item_table["Unlock Vanilla Minigame"] = ItemData(9999980, ItemClassification.progression)
item_table["Unlock Seeker Minigame"] = ItemData(9999970, ItemClassification.progression)
item_table["Unlock Button Galore Minigame"] = ItemData(9999960, ItemClassification.progression)
item_table["Unlock OG Randomizer Minigame"] = ItemData(9999950, ItemClassification.progression)

# for i in range(0, 101):
#     item_table[f"DEBUGA {i}"] = ItemData(20000000 + i, ItemClassification.filler)
#     item_table[f"DEBUGB {i}"] = ItemData(30000000 + i, ItemClassification.filler)
#     item_table[f"DEBUGC {i}"] = ItemData(40000000 + i, ItemClassification.filler)
#     item_table[f"DEBUGD {i}"] = ItemData(50000000 + i, ItemClassification.filler)
# item_table[f"Disable Wall Ledge"] = ItemData(60000000, ItemClassification.filler)
# item_table[f"Enable One Wall"] = ItemData(60000001, ItemClassification.filler)
# item_table[f"Disable Swim"] = ItemData(60000005, ItemClassification.filler)
# item_table[f"Disable Jumppads"] = ItemData(60000010, ItemClassification.filler)
# item_table[f"DEBUG Goal"] = ItemData(60000015, ItemClassification.filler)

item_table[f"Dark skies"] = ItemData(9999001, ItemClassification.trap)
item_table[f"No skylight"] = ItemData(9999002, ItemClassification.trap)
item_table[f"Slo-mo"] = ItemData(9999003, ItemClassification.trap)
item_table[f"Fast-mo"] = ItemData(9999004, ItemClassification.trap)
# item_table[f"Disco sky"] = ItemData(9999005, ItemClassification.trap)
item_table[f"Starry sky"] = ItemData(9999006, ItemClassification.trap)
item_table[f"Red sky"] = ItemData(9999007, ItemClassification.trap)
item_table[f"Hurricane"] = ItemData(9999008, ItemClassification.trap)
item_table[f"Blurrrrgh"] = ItemData(9999009, ItemClassification.trap)