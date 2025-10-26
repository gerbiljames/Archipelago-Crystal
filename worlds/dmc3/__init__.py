from dataclasses import asdict
from typing import Dict, Any, TextIO

from BaseClasses import Tutorial, Region
from worlds.AutoWorld import WebWorld, World
from .Items import item_descriptions, DMC3Item, dmc3_items, ItemData, junk_pool
from .Locations import location_descriptions, DMC3Location, BaseLocationData, adjudicators, \
    adjudicator_info, dmc3_locations, location_name_groups
from .Options import DMC3Options
from .Regions import dmc3_regions, setup_all_goal, setup_linear_goal
from .Rules import *
from .Skills import *
from ..LauncherComponents import Component, components, launch as launch_component, Type

DEBUG = False


def launch_client(*args: str):
    from .DMC3Client import launch
    launch_component(launch, name="DMC3Client", args=args)


components.append(Component("Devil May Cry 3 Client", "DMC3Client", func=launch_client,
                            component_type=Type.CLIENT))


# icon_paths['dante'] = local_path('data', 'dante.png')

class DevilMayCry3Web(WebWorld):
    rich_text_options_doc = True
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
    options_presets = Options.dmc3_presets


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
    dmc3_mission_order = [i for i in range(1, 21)]

    item_name_to_id = {name: data.code for name, data in (dmc3_items | combined_upgrades | styles).items() if
                       data.code is not None}

    location_name_to_id = {name: id for id, name in
                           enumerate(dmc3_locations, base_id)}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    set_rules = Rules.set_dmc3_rules

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
        melee = "Rebellion"
        match self.options.start_melee.value:
            case 0:
                melee = "Rebellion"
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
        if self.options.goal == self.options.goal.option_random_order:
            self.random.shuffle(self.dmc3_mission_order)
            print(f"Mission Order: {self.dmc3_mission_order}")
        if self.options.randomize_styles:
            if item_name_groups["styles"] & self.options.start_inventory.keys():
                pass
            else:
                self.push_precollected(self.create_item(self.random.choice(item_name_groups["styles"])))
        if self.options.random_adjudicators:
            for (adjudicator, info) in self.adjudicator_generated_values.items():
                info.weapon = \
                    self.random.choices(Items.item_name_groups["melees"])[
                        0]
                if self.options.adjudicator_rankings.value != self.options.adjudicator_rankings.option_unchanged:
                    info.ranking = Locations.Ranking(
                        self.random.randrange(Locations.Ranking.C.value, self.options.adjudicator_rankings.value + 1))

    def create_regions(self) -> None:
        # Menu
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        # Setup missions+secret missions
        for mission_idx in range(20):
            mission = self.dmc3_mission_order[mission_idx]
            data = dmc3_regions[mission]
            mission_name = f"Mission #{mission}"

            # Generic mission stuff
            current_region = Region(mission_name, self.player, self.multiworld)
            current_region.add_locations({
                m_loc: self.location_name_to_id[m_loc]
                for m_loc in [loc for loc in dmc3_locations if dmc3_locations[loc].mission_number == mission]
            }, DMC3Location)

            #current_region.add_event(f"Finish Mission #{mission}", None, lambda state, mi=mission: state.can_reach_location(f"Mission #{mi} Complete", self.player), DMC3Location, DMC3Item)

            current_region.add_exits(["Menu"])
            self.multiworld.regions.append(current_region)

            # Goal specific stuff
            match self.options.goal.value:
                case self.options.goal.option_standard: setup_linear_goal(mission, mission_name, current_region, self, menu_region)
                case self.options.goal.option_all: setup_all_goal(mission, mission_name, current_region, self, menu_region)
                case self.options.goal.option_random_order: setup_linear_goal(mission, mission_name, current_region, self, menu_region)

            # Secret mission handling
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
        item = DMC3Item(item, (dmc3_items | combined_upgrades | styles)[item].classification,
                        self.item_name_to_id[item],
                        self.player)
        return item

    def create_items(self) -> None:
        # Setup exclude list so dupes aren't in pool
        exclude = [item for item in self.multiworld.precollected_items[self.player]]
        # Proper Purple+Blue orb counts are added below
        exclude.append(self.create_item("Purple Orb"))
        exclude.append(self.create_item("Blue Orb"))
        # Consumables are filler, don't add them to the pool
        for item in junk_pool.keys():
            exclude.append(self.create_item(item))

        # Initial item pool before excludes are taken out
        initial_item_pool = []
        for item in map(self.create_item, dmc3_items):
            initial_item_pool.append(item)

        # Style handling
        if self.options.randomize_styles:
            for style, _ in styles.items():
                # Every style has 3 levels, 1st level actually unlocks it
                initial_item_pool.extend([self.create_item(style) for _ in range(3)])

        # Skill+Gun level handling
        if self.options.randomize_skills:
            # Adds all skills to the pool
            for skill in map(self.create_item, weapon_skills):
                initial_item_pool.append(skill)
            # Progressive skills need a second copy to reach max level
            for skill in map(self.create_item, self.item_name_groups["upgradable_skills"]):
                initial_item_pool.append(skill)
            for gun, _ in gun_levels.items():
                # All guns go up to level 3, starting at 1
                initial_item_pool.extend([self.create_item(gun) for _ in range(2)])

        final_item_pool = []
        # Add enough blue and purple to ensure max magic+hp can be obtained
        final_item_pool.extend([self.create_item("Blue Orb") for _ in range(14)])  # Max HP is 20k, start with 6k
        # Max Magic is 10k
        final_item_pool.extend([self.create_item("Purple Orb") for _ in range(7)])  # Add 7 orbs no matter what

        # Remaining 3 if Purple mode is on, otherwise DT Item will be used to reach 10k magic
        if self.options.purple_orb_mode:
            final_item_pool.extend([self.create_item("Purple Orb") for _ in range(3)])

        # If we have 10 purple orbs in world and don't need the DT item to unlock DT, remove it from the world
        # If purple mode is off, then we need the DT item, and if DT mode is on, we need the DT item
        if self.options.purple_orb_mode and not self.options.devil_trigger_mode:
            exclude.append(self.create_item("Devil Trigger"))

        # Remove any items that are in the excluded pool
        for item in initial_item_pool:
            if item in exclude:
                exclude.remove(item)  # this is destructive. create unique list above
            else:
                final_item_pool.append(item)

        if DEBUG:
            print("Item pool len: {}".format(len(final_item_pool)))
            print("Location count: {}".format(len(dmc3_locations)))
        while len(final_item_pool) < len(self.multiworld.get_unfilled_locations(self.player)):
            final_item_pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool += final_item_pool

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))[0]

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        # Add adjudicator information to the spoiler log
        spoiler_handle.write(f"\nAdjudicator Information ({self.player_name}):\n")
        for adjudicator in adjudicators:
            weapon = self.adjudicator_generated_values[adjudicator].weapon
            rank = self.adjudicator_generated_values[adjudicator].ranking
            location = self.multiworld.get_location(adjudicator, self.player)
            spoiler_handle.write(f"{location.name}: {weapon} - Rank: {rank.name}\n")
        if self.options.goal == self.options.goal.option_random_order:
            spoiler_handle.write(f"\nMission Order ({self.player_name}):\n")
            spoiler_handle.write(f"{self.dmc3_mission_order}\n")

    def fill_slot_data(self) -> Dict[str, Any]:
        data = {
            'seed': self.multiworld.seed_name,
            'items': {
                location.name: dict(item_id=location.item.code,
                                    owner=location.item.player) for location in
                self.multiworld.get_filled_locations(self.player)
            },
            'starter_items': [item.name for item in self.multiworld.precollected_items[self.player]],
        }
        if self.options.random_adjudicators:
            data.update({'adjudicators': {key: asdict(adj) for key, adj in self.adjudicator_generated_values.items()}})
        if self.options.goal == self.options.goal.option_random_order:
            data.update({'mission_order': self.dmc3_mission_order})
        data.update(self.options.as_dict("start_melee", "start_gun",
                                         "randomize_skills", "randomize_styles", "purple_orb_mode",
                                         "devil_trigger_mode", "goal",
                                         "death_link", toggles_as_bools=True))
        return data
