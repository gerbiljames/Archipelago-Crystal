import json
import os
from typing import Dict, Any

from BaseClasses import Tutorial, Region
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from worlds.dmc3.Items import item_descriptions, DMC3Item, get_item_type, dmc3_items, ItemData, junk_pool, Mode
from worlds.dmc3.Locations import location_descriptions, DMC3Location, BaseLocationData, adjudicators, \
    adjudicator_info, dmc3_locations
from worlds.dmc3.Options import DMC3Options
from worlds.dmc3.Regions import dmc3_regions
from worlds.generic.Rules import set_rule, add_rule, forbid_item


class DevilMayCry3Web(WebWorld):
    bug_report_page = "https://github.com/AshIndigo/Devil-May-Cry-3-Archipelago/issues"
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Devil May Cry 3 randomizer on your computer.",
        "English",
        "en_setup.md",
        "setup/en",
        ["AshIndigo"]
    )

    tutorials = [setup_en]
    options_presets = {
        # "Default": {
        #     "start_melee": ["rebellion"],
        #     "start_gun": ["ebony_and_ivory"]
        # }
    }


class DevilMayCry3World(World):
    """
        Devil May Cry 3 originally released in 2005 is the hit sequal to Devil May Cry 2. Featuring all new weapons, fights and the newly added style mechanic.
        """

    game = "Devil May Cry 3"
    options: DMC3Options
    options_dataclass = DMC3Options
    location_descriptions = location_descriptions
    item_descriptions = item_descriptions
    topology_present: bool = True
    web = DevilMayCry3Web()
    base_id = 1
    adjudicator_generated_values = Locations.adjudicator_info.copy()

    item_name_to_id = {name: data.code for name, data in dmc3_items.items() if
                       data.code is not None}  # TODO Something is wrong with this, it's saying it received a different item than it actually did
    # TODO Check this

    # item_name_to_id = {name: id for id, name in enumerate(dmc3_items)}
    location_name_to_id = {name: id for id, name in
                           enumerate(dmc3_locations, base_id)}  # You aren't giving me the first location...
    item_name_groups = {
        "melees": {"Rebellion (Normal)", "Cerberus", "Agni and Rudra", "Nevan", "Beowulf"},
        "guns": {"Ebony & Ivory", "Shotgun", "Artemis", "Spiral", "Kalina Ann"},
        "essences": {"Essence of Fighting", "Essence of Technique", "Essence of Intelligence"},
        "fragments": {"Orihalcon Fragment (Right)", "Orihalcon Fragment (Left)", "Orihalcon Fragment (Bottom)"}
    }

    def __init__(self, world, player: int):
        super(DevilMayCry3World, self).__init__(world, player)

    def generate_output(self, output_directory: str) -> None:
        data = {
            'seed': self.multiworld.seed_name,
            'slot': self.multiworld.player_name[self.player],
            'items': {
                location.name: dict(name=location.item.name
                if location.item.player == self.player else "Remote",
                                    description="{}'s {}".format(self.multiworld.player_name[location.item.player],
                                                                 location.item.name)) for location in
                self.multiworld.get_filled_locations(self.player)
            },
            'starter_items': [item.name for item in self.multiworld.precollected_items[self.player]],
            'players': [self.multiworld.player_name[player] for player in self.multiworld.player_ids],
            'adjudicators': {key: adj.model_dump() for key, adj in self.adjudicator_generated_values.items()},
        }
        out_file = os.path.join(output_directory, self.multiworld.get_out_file_name_base(self.player) + ".json")
        with open(out_file, 'w') as json_file:
            json.dump(data, json_file)

    def generate_early(self) -> None:
        gun = "Ebony & Ivory"
        match self.options.start_gun.value:
            case 0:
                gun = "Ebony & Ivory"
            case 1:
                gun = "Shotgun"
            case 2:
                gun = "Artemis"
            case 3:
                gun = "Spiral"
            case 4:
                gun = "Kalina Ann"
        melee = "Rebellion (Normal)"
        match self.options.start_melee.value:
            case 0:
                melee = "Rebellion (Normal)"
            case 1:
                melee = "Cerberus"
            case 2:
                melee = "Agni and Rudra"
            case 3:
                melee = "Nevan"
            case 4:
                melee = "Beowulf"
        self.multiworld.push_precollected(self.create_item(gun))
        self.multiworld.push_precollected(self.create_item(melee))
        if self.options.random_adjudicators.value:
            for (adjudicator, info) in self.adjudicator_generated_values.items():
                info.weapon = \
                self.random.choices(list({item[0].name for item in Items.weapons if item[1] == Items.Type.MELEE}))[0]
                if self.options.adjudicator_rankings.value != self.options.adjudicator_rankings.default:
                    info.ranking = Locations.Ranking(
                        self.random.randrange(Locations.Ranking.C.value, self.options.adjudicator_rankings.value + 1))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)  # or use += [menu_region...]

        for mission in dmc3_regions:
            region = Region("Mission #{}".format(mission), self.player, self.multiworld)
            locs = [loc for loc in dmc3_locations if dmc3_locations[loc].mission_number == mission]
            for loc in locs:
                loc_fin = DMC3Location(self.player, loc, self.location_name_to_id.get(loc, None), region)
                region.locations.append(loc_fin)
            if mission == 20:
                pass
                # victory_loc = DMC3Location(self.player, "Mission #20 - Finished", None, region)
                # victory_loc.place_locked_item(DMC3Item("Mission #20 - Finished", ItemClassification.progression, None, self.player))
                # region.locations.append(victory_loc)
            if mission == 1:
                menu_region.connect(region)
            if mission > 1:
                self.multiworld.get_region("Mission #{}".format(mission - 1), self.player).connect(region)
                region.connect(self.multiworld.get_region("Mission #{}".format(mission - 1), self.player))
            self.multiworld.regions.append(region)
            if dmc3_regions[mission]["secret"] != [0]:
                for secret in dmc3_regions[mission]["secret"]:
                    sec_reg = Region("Secret Mission #{}".format(secret), self.player, self.multiworld)
                    sec_reg.locations.append(DMC3Location(self.player, "Secret Mission #{}".format(secret),
                                                          self.location_name_to_id.get(
                                                              "Secret Mission #{}".format(secret), None), region))
                    region.connect(sec_reg)
                    sec_reg.connect(region)
                    self.multiworld.regions.append(sec_reg)

    def create_item(self, item: str) -> DMC3Item:
        item = DMC3Item(item, dmc3_items[item][2], self.item_name_to_id[item],
                        self.player)  # TODO Think I'm supplying the wrong id here?
        return item

    def create_items(self) -> None:
        # Add items to the Multiworld.
        # If there are two of the same item, the item has to be twice in the pool.
        # Which items are added to the pool may depend on player options, e.g. custom win condition like triforce hunt.
        # Having an item in the start inventory won't remove it from the pool.
        # If an item can't have duplicates it has to be excluded manually.

        # List of items to exclude, as a copy since it will be destroyed below
        exclude = [item for item in self.multiworld.precollected_items[self.player]]
        item_pool = []
        for item in map(self.create_item, dmc3_items):
            if item in exclude:
                exclude.remove(item)  # this is destructive. create unique list above
                item_pool.append(self.create_item(self.get_filler_item_name()))
            else:
                item_pool.append(item)

        while len(item_pool) < len(self.multiworld.get_unfilled_locations(self.player)):
            item_pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))[0]

    def set_rules(self) -> None:
        for dmc3_item in dmc3_items:
            if dmc3_items[dmc3_item].mode == Mode.CONSUMABLE:
                forbid_item(self.multiworld.get_location("Mission #5 - Soul of Steel", self.player), dmc3_item,
                            self.player)

        for adjudicator in adjudicators:
            set_rule(self.multiworld.get_location(adjudicator, self.player),
                     lambda state: state.has(self.adjudicator_generated_values[adjudicator].weapon, self.player))
        set_rule(self.multiworld.get_entrance("Mission #4 -> Mission #5", self.player),
                 lambda state: state.has("Astronomical Board", self.player))

        set_rule(self.multiworld.get_entrance("Mission #5 -> Mission #6", self.player),
                 lambda state: state.has("Soul of Steel", self.player))

        set_rule(self.multiworld.get_entrance("Mission #6 -> Mission #7", self.player),
                 lambda state: state.count_group("essences", self.player) >= 2)

        set_rule(self.multiworld.get_entrance("Mission #7 -> Mission #8", self.player),
                 lambda state: state.has("Crystal Skull", self.player))

        set_rule(self.multiworld.get_entrance("Mission #8 -> Mission #9", self.player),
                 lambda state: state.has("Ignis Fatuus", self.player))
        set_rule(self.multiworld.get_entrance("Mission #9 -> Mission #10", self.player),
                 lambda state: state.has("Ambrosia", self.player))
        set_rule(self.multiworld.get_entrance("Mission #10 -> Mission #11", self.player),
                 lambda state: state.has("Neo Generator", self.player))

        set_rule(self.multiworld.get_entrance("Mission #12 -> Mission #13", self.player),
                 lambda state: state.has("Haywire Neo Generator", self.player))

        set_rule(self.multiworld.get_entrance("Mission #13 -> Mission #14", self.player),
                 lambda state: state.has("Full Orihalcon", self.player))

        set_rule(self.multiworld.get_entrance("Mission #15 -> Mission #16", self.player),
                 lambda state: state.count_group("fragments", self.player) == 3)

        set_rule(self.multiworld.get_entrance("Mission #16 -> Mission #17", self.player),
                 lambda state: state.has("Golden Sun", self.player) and state.has("Onyx Moonshard", self.player))

        set_rule(self.multiworld.get_entrance("Mission #19 -> Mission #20", self.player),
                 lambda state: state.has("Samsara", self.player))

        add_rule(self.multiworld.get_location("Mission #5 - Soul of Steel", self.player),
                 lambda state: state.has("Vajura", self.player))
        add_rule(self.multiworld.get_location("Mission #7 - Siren's Shriek", self.player),
                 lambda state: state.has("Orihalcon Fragment", self.player))
        add_rule(self.multiworld.get_location("Mission #7 - Crystal Skull", self.player),
                 lambda state: state.has("Siren's Shriek", self.player))

        add_rule(self.multiworld.get_location("Mission #10 - Neo Generator", self.player),
                 lambda state: state.has("Stone Mask", self.player))

        add_rule(self.multiworld.get_location("Mission #6 - Artemis", self.player),
                 lambda state: state.count_group("essences", self.player) == 3)

        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Mission #20", "Region",
                                                                                          self.player)
        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict("random_adjudicators", "adjudicator_rankings", "start_melee", "start_gun", "death_link")
