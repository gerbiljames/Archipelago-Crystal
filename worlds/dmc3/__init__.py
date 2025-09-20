from dataclasses import asdict
from typing import Dict, Any, TextIO

from BaseClasses import Tutorial, Region
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from .Items import item_descriptions, DMC3Item, dmc3_items, ItemData, junk_pool
from .Locations import location_descriptions, DMC3Location, BaseLocationData, adjudicators, \
    adjudicator_info, dmc3_locations, location_name_groups
from .Options import DMC3Options
from .Regions import dmc3_regions
from .Skills import *
from ..LauncherComponents import Component, components, launch as launch_component, Type

DEBUG = True


def launch_client(*args: str):
    from .DMC3Client import launch
    launch_component(launch, name="DMC3Client", args=args)


components.append(Component("Devil May Cry 3 Client", "DMC3Client", func=launch_client,
                            component_type=Type.CLIENT))


# icon_paths['dante'] = local_path('data', 'dante.png')

class DevilMayCry3Web(WebWorld):
    location_descriptions = location_descriptions
    item_descriptions = item_descriptions
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


def has_air_hike(state, player) -> bool:
    for melee in item_name_groups["melees"]:
        if state.has(melee, player) and state.has("{} - Air Hike".format(melee), player):
            return True

    return False


class DevilMayCry3World(World):
    """
        Devil May Cry 3 originally released in 2005 is the hit sequel to Devil May Cry 2. Featuring all new weapons, fights and the newly added style mechanic.
        """

    game = "Devil May Cry 3"
    options: DMC3Options
    options_dataclass = DMC3Options
    topology_present: bool = True
    web = DevilMayCry3Web()
    base_id = 1
    adjudicator_generated_values = adjudicator_info.copy()

    item_name_to_id = {name: data.code for name, data in (dmc3_items | combined_upgrades).items() if
                       data.code is not None}

    location_name_to_id = {name: id for id, name in
                           enumerate(dmc3_locations, base_id)}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def __init__(self, world, player: int):
        super(DevilMayCry3World, self).__init__(world, player)

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
                    self.random.choices(Items.item_name_groups["melees"])[
                        0]
                if self.options.adjudicator_rankings.value != self.options.adjudicator_rankings.option_unchanged:
                    info.ranking = Locations.Ranking(
                        self.random.randrange(Locations.Ranking.C.value, self.options.adjudicator_rankings.value + 1))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        base_mission_check = 300
        for mission, data in dmc3_regions.items():
            mission_name = f"Mission #{mission}"
            current_region = Region(mission_name, self.player, self.multiworld)
            mission_locations = [loc for loc in dmc3_locations if dmc3_locations[loc].mission_number == mission]
            current_region.add_locations({
                loc: self.location_name_to_id[loc]
                for loc in mission_locations
            }, DMC3Location)
            current_region.add_exits(["Menu"])
            self.multiworld.regions.append(current_region)
            if mission == 1:
                menu_region.connect(current_region)
            if mission > 1:
                self.get_region(f"Mission #{mission - 1}").add_exits([mission_name])
            if mission == 20:
                victory_loc = DMC3Location(self.player, "Mission #20 Complete", None,
                                           current_region)
                # victory_loc = self.multiworld.get_location("Mission #20 Complete", self.player)
                victory_loc.place_locked_item(
                    DMC3Item("Finish Game", ItemClassification.progression, None, self.player))
                current_region.locations.append(victory_loc)
            if data["secret"] != [0]:
                for secret in data["secret"]:
                    secret_mission_name = f"Secret Mission #{secret}"
                    secret_region = Region(secret_mission_name, self.player, self.multiworld)
                    secret_region.locations.append(DMC3Location(self.player, secret_mission_name,
                                                                self.location_name_to_id.get(
                                                                    secret_mission_name, None), current_region))
                    current_region.connect(secret_region)
                    self.multiworld.regions.append(secret_region)
                    secret_region.add_exits(["Menu", mission_name])

    def create_item(self, item: str) -> DMC3Item:
        item = DMC3Item(item, (dmc3_items | combined_upgrades)[item].classification, self.item_name_to_id[item],
                        self.player)
        return item

    def create_items(self) -> None:
        # Add items to the Multiworld.
        # If there are two of the same item, the item has to be twice in the pool.
        # Which items are added to the pool may depend on player options, e.g. custom win condition like triforce hunt.
        # Having an item in the start inventory won't remove it from the pool.
        # If an item can't have duplicates it has to be excluded manually.

        # List of items to exclude, as a copy since it will be destroyed below
        exclude = [item for item in self.multiworld.precollected_items[self.player]]
        exclude.append(self.create_item("Blue Orb Fragment"))
        exclude.append(self.create_item("Purple Orb"))
        exclude.append(self.create_item("Blue Orb"))
        # exclude.append(self.create_item("Rebellion (Awakened)"))
        item_pool = []
        # Add enough blue and purple to ensure max magic+hp can be obtained
        item_pool.extend([self.create_item("Blue Orb") for _ in range(14)])  # Max HP is 20k, start with 6k
        item_pool.extend([self.create_item("Purple Orb") for _ in range(10)])  # Max Magic is 10k
        for item in map(self.create_item, dmc3_items):
            if item in exclude:
                exclude.remove(item)  # this is destructive. create unique list above
                # item_pool.append(self.create_item(self.get_filler_item_name()))
            else:
                item_pool.append(item)
        if self.options.randomize_skills:  # For toggling if skills are to be rando'd
            for skill in map(self.create_item, weapon_skills):
                item_pool.append(skill)
            # Yes this is cheeky
            for gun_level in map(self.create_item, gun_levels):
                item_pool.append(gun_level)
            for gun_level in map(self.create_item, gun_levels):
                item_pool.append(gun_level)
        if DEBUG:
            print("Item pool len: {}".format(len(item_pool)))
            print("Location count: {}".format(len(dmc3_locations)))
        while len(item_pool) < len(self.multiworld.get_unfilled_locations(self.player)):
            item_pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))[0]

    ### For mission order 1-20
    def add_linear_rules(self):
        add_rule(self.multiworld.get_entrance("Mission #4 -> Mission #5", self.player),
                 lambda state: state.has("Astronomical Board", self.player))
        add_rule(self.multiworld.get_entrance("Mission #5 -> Mission #6", self.player),
                 lambda state: state.has("Soul of Steel", self.player))

        add_rule(self.multiworld.get_entrance("Mission #6 -> Mission #7", self.player),
                 lambda state: state.count_group("essences", self.player) >= 2)

        add_rule(self.multiworld.get_entrance("Mission #7 -> Mission #8", self.player),
                 lambda state: state.has("Crystal Skull", self.player))

        add_rule(self.multiworld.get_entrance("Mission #8 -> Mission #9", self.player),
                 lambda state: state.has("Ignis Fatuus", self.player))
        add_rule(self.multiworld.get_entrance("Mission #9 -> Mission #10", self.player),
                 lambda state: state.has("Ambrosia", self.player))
        add_rule(self.multiworld.get_entrance("Mission #10 -> Mission #11", self.player),
                 lambda state: state.has("Neo Generator", self.player))

        add_rule(self.multiworld.get_entrance("Mission #12 -> Mission #13", self.player),
                 lambda state: state.has("Haywire Neo Generator", self.player))

        add_rule(self.multiworld.get_entrance("Mission #13 -> Mission #14", self.player),
                 lambda state: state.has("Full Orihalcon", self.player))
        # # This one blocks the door in M14 because it's to make sure you have beowulf (in vanilla)
        add_rule(self.multiworld.get_entrance("Mission #14 -> Mission #15", self.player),
                 lambda state: state.can_reach_location("Mission #14 - Combat Adjudicator #9",
                                                        self.player))
        add_rule(self.multiworld.get_entrance("Mission #15 -> Mission #16", self.player),
                 lambda state: state.count_group("fragments", self.player) == 3)

        add_rule(self.multiworld.get_entrance("Mission #16 -> Mission #17", self.player),
                 lambda state: state.has("Golden Sun", self.player) and state.has("Onyx Moonshard", self.player))

        add_rule(self.multiworld.get_entrance("Mission #19 -> Mission #20", self.player),
                 lambda state: state.has("Samsara", self.player))

    def set_rules(self) -> None:

        if True:
            self.add_linear_rules()

        add_rule(self.multiworld.get_location("Mission #5 - Combat Adjudicator #2", self.player),
                 lambda state: state.has("Soul of Steel", self.player))

        add_rule(self.multiworld.get_location("Mission #9 - Blue Orb Fragment #5", self.player),
                 lambda state: has_air_hike(state, self.player))

        add_rule(self.multiworld.get_location("Mission #14 - Combat Adjudicator #9", self.player),
                 lambda state: state.can_reach_location("Mission #14 - Beowulf", self.player))

        add_rule(self.multiworld.get_location("Mission #5 - Vajura", self.player),
                 lambda state: state.has("Astronomical Board", self.player))

        add_rule(self.multiworld.get_location("Mission #5 - Soul of Steel", self.player),
                 lambda state: state.has("Vajura", self.player))
        add_rule(self.multiworld.get_location("Mission #5 - Agni and Rudra", self.player),
                 lambda state: state.has("Soul of Steel", self.player))
        add_rule(self.multiworld.get_location("Mission #7 - Siren's Shriek", self.player),
                 lambda state: state.has("Orihalcon Fragment", self.player))
        add_rule(self.multiworld.get_location("Mission #7 - Crystal Skull", self.player),
                 lambda state: state.has("Siren's Shriek", self.player))

        add_rule(self.multiworld.get_location("Mission #10 - Neo Generator", self.player),
                 lambda state: state.has("Stone Mask", self.player))

        add_rule(self.multiworld.get_location("Mission #6 - Artemis", self.player),
                 lambda state: state.count_group("essences", self.player) == 3)

        add_rule(self.multiworld.get_location("Secret Mission #6", self.player),
                 # Flight of the Demon, needs air raid
                 lambda state: state.has("Nevan", self.player) and state.has("Nevan - Air Raid", self.player) and
                               (state.has("Purple Orb", self.player, count=3) or state.has("Rebellion (Awakened)",
                                                                                           self.player)))

        for adjudicator in adjudicators:
            weapon = self.adjudicator_generated_values[adjudicator].weapon
            location = self.multiworld.get_location(adjudicator, self.player)
            add_rule(location,
                     lambda state, wep=weapon:
                     state.has(wep, self.player))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Finish Game", self.player)
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nAdjudicator Information ({self.player_name}):\n")
        for adjudicator in adjudicators:
            weapon = self.adjudicator_generated_values[adjudicator].weapon
            location = self.multiworld.get_location(adjudicator, self.player)
            spoiler_handle.write(f"{location.name}: {weapon}\n")

    def fill_slot_data(self) -> Dict[str, Any]:
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
            'adjudicators': {key: asdict(adj) for key, adj in self.adjudicator_generated_values.items()},
        }
        data.update(self.options.as_dict("random_adjudicators", "adjudicator_rankings", "start_melee", "start_gun",
                                         "randomize_skills",
                                         "death_link"))

        return data
