from dataclasses import asdict
from typing import Dict, Any, TextIO, ClassVar, Optional

import settings
from BaseClasses import Tutorial, Region
from Options import Option
from Utils import Version
from worlds.AutoWorld import WebWorld, World
from .Items import item_descriptions, DMC3Item, dmc3_items, ItemData, junk_pool
from .Locations import location_descriptions, DMC3Location, BaseLocationData, adjudicators, \
    adjudicator_info, dmc3_locations, location_name_groups, default_shop_locations, gun_level_purchases, Adjudicator
from .Options import DMC3Options, option_groups
from .Regions import dmc3_regions, setup_all_goal, setup_linear_goal
from .Rules import *
from .Skills import *
from ..LauncherComponents import Component, components, launch as launch_component, Type

DEBUG = False

class DMC3Settings(settings.Group):
    class FloorsPerHint(int):
        """Amount of BP floors needed to generate a hint"""

    floors_per_hint: FloorsPerHint = FloorsPerHint(50)

def launch_client(*args: str):
    from .DMC3Client import launch
    launch_component(launch, name="DMC3Client", args=args)

def launch_hint_client(*args: str):
    from .DMC3HintClient import launch
    launch_component(launch, name="DMC3HintClient", args=args)


components.append(Component("Devil May Cry 3 Client", "DMC3Client", func=launch_client,
                            component_type=Type.CLIENT))

components.append(Component("Devil May Cry 3 Hint Client", "DMC3HintClient", func=launch_hint_client,
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
    option_groups = option_groups


def get_weapon_name_from_option(val) -> str:
    return {
        0: "Rebellion",
        1: "Cerberus",
        2: "Agni and Rudra",
        3: "Nevan",
        4: "Beowulf",
        5: "Ebony & Ivory",
        6: "Shotgun",
        7: "Artemis",
        8: "Spiral",
        9: "Kalina Ann",
        255: "None",
    }.get(val)


class DevilMayCry3World(World):
    """
        Devil May Cry 3 originally released in 2005 is the hit sequel to Devil May Cry 2. Featuring all new weapons, fights and the newly added style mechanic.
        """

    game = "Devil May Cry 3"
    options: DMC3Options
    options_dataclass = DMC3Options
    topology_present: bool = True
    web = DevilMayCry3Web()
    settings: ClassVar[DMC3Settings]
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
    ut_can_gen_without_yaml = True

    def grouped_mission_order(self):
        size = -(-20 // self.options.mission_group.value)

        # Work on a copy and pull out Mission 20
        order = [m for m in self.dmc3_mission_order if m != 20]

        groups = [order[i:i + size] for i in range(0, len(order), size)]
        shuffled = [
            item
            for group in groups
            for item in self.random.sample(group, len(group))
        ]

        # Ensure Mission 20 is always last because of unfixed bug
        shuffled.append(20)
        self.dmc3_mission_order = shuffled

    def weighted_mission_order(self):
        int_weights = {mission: self.options.mission_weights.value.get(
            f"Mission #{mission}",
            self.options.mission_weights.default[f"Mission #{mission}"])
            for mission in range(1, 21)}
        pool = list(int_weights.items())
        result = []

        while pool:
            keys = [k for k, w in pool]
            w = [w for k, w in pool]

            chosen = self.random.choices(keys, weights=w, k=1)[0]
            result.append(chosen)

            pool = [(k, w) for k, w in pool if k != chosen]

        self.dmc3_mission_order = result

    def __init__(self, world, player: int):
        super(DevilMayCry3World, self).__init__(world, player)

    def generate_early(self) -> None:
        # Universal Tracker stuff
        # Knowing what is excluded still requires YAML
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            # Set all your options here instead of getting them from the YAML
            for key, value in slot_data.items():
                if key == "adjudicators":
                    self.options.random_adjudicators.value = True
                    self.adjudicator_generated_values = {
                        k: Adjudicator(weapon = v["weapon"], ranking = v["ranking"]) for k, v in value.items()
                    }
                if key == "shop_checks":
                    self.options.shop_orb_checks.value = True
                    self.options.shop_gun_checks.value = True
                if key == "mission_order":
                    self.dmc3_mission_order = value
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))

        # Check to see if both melee slots have the same weapon
        if self.options.start_melee.value == self.options.start_second_melee.value:
            print("Both melee slots have the same weapon, re-rolling second melee")
            # Need to pick from a pool of weapons we don't already have
            self.options.start_second_melee.value = \
                self.random.choices([n for n in [0, 1, 2, 3, 4] if n != self.options.start_melee.value])[0]

        # Check to see if both gun slots have the same gun
        if self.options.start_gun.value == self.options.start_second_gun.value:
            print("Both gun slots have the same gun, re-rolling second gun")
            # Need to pick from a pool of guns we don't already have
            self.options.start_second_gun.value = \
                self.random.choices([n for n in [5, 6, 7, 8, 9] if n != self.options.start_gun.value])[0]

        # Add starting weapons to precollected pool
        for option_value in [
            self.options.start_melee.value,
            self.options.start_gun.value,
            self.options.start_second_melee.value,
            self.options.start_second_gun.value,
        ]:
            if option_value != 255:
                self.multiworld.push_precollected(
                    self.create_item(get_weapon_name_from_option(option_value))
                )

        if self.options.goal == self.options.goal.option_random_order and not hasattr(self.multiworld, "generation_is_fake"):
            match self.options.mission_shuffle.value:
                case self.options.mission_shuffle.option_rng:
                    self.random.shuffle(self.dmc3_mission_order)
                case self.options.mission_shuffle.option_grouped:
                    self.grouped_mission_order()
                case self.options.mission_shuffle.option_weighted:
                    self.weighted_mission_order()

            print(f"Mission Order: {self.dmc3_mission_order}")
        # If a style isn't already in the start inventory, pick one at random
        if self.options.randomize_styles:
            if item_name_groups["styles"] & self.options.start_inventory.keys():
                pass
            else:
                self.push_precollected(self.create_item(self.random.choice(item_name_groups["styles"])))
        # Generate random adjudicator settings
        if self.options.random_adjudicators and not hasattr(self.multiworld, "generation_is_fake"):
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
        if self.options.shop_orb_checks:
            menu_region.add_locations({
                m_loc: self.location_name_to_id[m_loc]
                for m_loc in [loc for loc in default_shop_locations]
            }, DMC3Location)
        if self.options.shop_gun_checks:
            menu_region.add_locations({
                m_loc: self.location_name_to_id[m_loc]
                for m_loc in [loc for loc in gun_level_purchases]
            }, DMC3Location)
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

            # current_region.add_event(f"Finish Mission #{mission}", None, lambda state, mi=mission: state.can_reach_location(f"Mission #{mi} Complete", self.player), DMC3Location, DMC3Item)

            current_region.add_exits(["Menu"])
            self.multiworld.regions.append(current_region)

            # Goal specific stuff
            match self.options.goal.value:
                case self.options.goal.option_standard:
                    setup_linear_goal(mission, mission_name, current_region, self, menu_region)
                case self.options.goal.option_all:
                    setup_all_goal(mission, mission_name, current_region, self, menu_region)
                case self.options.goal.option_random_order:
                    setup_linear_goal(mission, mission_name, current_region, self, menu_region)

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
        if self.options.randomize_gun_levels:
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
            'starter_items': [item.name for item in self.multiworld.precollected_items[self.player]],
            'generated_version': self.world_version
        }
        if self.options.random_adjudicators:
            data.update({'adjudicators': {key: asdict(adj) for key, adj in self.adjudicator_generated_values.items()}})
        if self.options.goal == self.options.goal.option_random_order:
            data.update({'mission_order': self.dmc3_mission_order})
        data.update(self.options.as_dict("start_melee", "start_second_melee", "start_gun", "start_second_gun",
                                         "randomize_skills", "randomize_gun_levels", "randomize_styles",
                                         "purple_orb_mode",
                                         "devil_trigger_mode", "goal", "mission_clear_rank", "mission_clear_difficulty",
                                         "initially_unlocked_difficulties", "check_ss_difficulty", "shop_orb_checks", "shop_gun_checks",
                                         "death_link", toggles_as_bools=True))
        return data

    # Universal Tracker support
    def interpret_slot_data(self, slot_data: dict[str, Any]) -> dict[str, Any]:
        # Error if APWorld versions don't match
        if Version(*slot_data["generated_version"]) != self.world_version:
            raise Exception("Current DMC3 APWorld version ({}) does not match slot data version ({})".format(self.world_version, Version(*slot_data["generated_version"])))
        # Trigger a regen in UT
        return slot_data

    # Add in explanation text for certain checks?
    # def explain_rule(self, target_name: str, state: CollectionState) -> list[JSONMessagePart]:
    #     return [{"type": "text", "text": "You gotta pick it up"}]