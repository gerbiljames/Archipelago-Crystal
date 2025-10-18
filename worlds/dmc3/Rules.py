from ..dmc3 import adjudicators
from ..generic.Rules import add_rule


def has_air_hike(state, world) -> bool:
    for melee in world.item_name_groups["air_hike_capable"]:
        if state.has(melee, world.player):
            # If rando skills isn't on, it'll have to be bought. Otherwise, check to see if the weapon has air hike unlocked
            if world.options.randomize_skills:
                return state.has("{} - Air Hike".format(melee), world.player)
            else:
                return True

    return False


def has_air_raid(state, world) -> bool:
    if state.has("Nevan", world.player):
        if world.options.randomize_skills:
            return state.has("Nevan - Air Raid", world.player)
        else:
            return True
    return False


def has_sky_star(state, world) -> bool:
    # Lv2 Trickster gives Sky Star, if randomized styles is off, player will have to level Trickster
    if world.options.randomize_styles:
        return state.has("Progressive Trickster", world.player, count=2)
    else:
        return True


def has_devil_trigger(state, world) -> bool:
    if world.options.devil_trigger_mode:
        dt = state.has("Devil Trigger", world.player)
    else:
        # DT is 'always' accessible, just needs 3 runes
        dt = True
    if world.options.purple_orb_mode:
        orbs = state.has("Purple Orb", world.player, count=3)
    else:
        orbs = (state.has("Purple Orb", world.player, count=3) or state.has("Devil Trigger",
                                                                            world.player))

    return dt and orbs


# For mission order 1-20
def add_linear_rules(self):
    # TODO Why is this here?
    add_rule(self.multiworld.get_entrance("Mission #4 -> Mission #5", self.player),
             lambda state: state.has("Astronomical Board", self.player))
    # Needed to open the door to the lift to get to A&R
    add_rule(self.multiworld.get_entrance("Mission #5 -> Mission #6", self.player),
             lambda state: state.has("Soul of Steel", self.player))

    # Statue laser needs 2 essences
    add_rule(self.multiworld.get_entrance("Mission #6 -> Mission #7", self.player),
             lambda state: state.count_group("essences", self.player) >= 2)

    # Opens the door leading to Vergil's Arena
    add_rule(self.multiworld.get_entrance("Mission #7 -> Mission #8", self.player),
             lambda state: state.has("Crystal Skull", self.player))

    # Open 'door' to boss
    add_rule(self.multiworld.get_entrance("Mission #8 -> Mission #9", self.player),
             lambda state: state.has("Ignis Fatuus", self.player))

    # Slots into door leading to Nevan
    # TODO, should this be moved to general rules? Then set Nevan fight as #9 -> #M10 for linear rules?
    # ^ Could be a logic issue now thinking about it, if Nevan is set to have Ambrosia as her drop
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

    # Elevator needs all 3 fragments
    add_rule(self.multiworld.get_entrance("Mission #15 -> Mission #16", self.player),
             lambda state: state.count_group("fragments", self.player) == 3)

    # Door needs both to be slotted in
    add_rule(self.multiworld.get_entrance("Mission #16 -> Mission #17", self.player),
             lambda state: state.has("Golden Sun", self.player) and state.has("Onyx Moonshard", self.player))

    # Stuck in a loop without the Samsara being slotted in
    add_rule(self.multiworld.get_entrance("Mission #19 -> Mission #20", self.player),
             lambda state: state.has("Samsara", self.player))


# Generic Location rules, independent of goal
def add_generic_rules(world):
    # Across the pit that needs the soul of steel to cross
    add_rule(world.multiworld.get_location("Mission #5 - Combat Adjudicator #2", world.player),
             lambda state: state.has("Soul of Steel", world.player))

    add_rule(world.multiworld.get_location("Mission #9 - Blue Orb Fragment #5", world.player),
             # TODO Probably have a trickster check here
             lambda state: has_air_hike(state, world) and has_sky_star(state, world))

    # Extra insurance, even if it may be un-needed. Both locations are in the same room.
    add_rule(world.multiworld.get_location("Mission #14 - Combat Adjudicator #9", world.player),
             lambda state: state.can_reach_location("Mission #14 - Beowulf", world.player))

    # Astronomical board removes the walls blocking access
    add_rule(world.multiworld.get_location("Mission #5 - Vajura", world.player),
             lambda state: state.has("Astronomical Board", world.player))

    # Vajura opens the cage to access this check
    add_rule(world.multiworld.get_location("Mission #5 - Soul of Steel", world.player),
             lambda state: state.has("Vajura", world.player))

    # Across the pit that needs the soul of steel to cross
    add_rule(world.multiworld.get_location("Mission #5 - Agni and Rudra", world.player),
             lambda state: state.has("Soul of Steel", world.player))

    # ??
    add_rule(world.multiworld.get_location("Mission #7 - Siren's Shriek", world.player),
             lambda state: state.has("Orihalcon Fragment", world.player))

    # Needed to dispel the flames blocking the door to this room.
    # TODO May also need Orihalcon Fragment to take the elevator down
    add_rule(world.multiworld.get_location("Mission #7 - Crystal Skull", world.player),
             lambda state: state.has("Siren's Shriek", world.player))

    # Stone Mask is needed to raise a bridge to the platform that leads to the Neo Generator and SM6
    add_rule(world.multiworld.get_location("Mission #10 - Neo Generator", world.player),
             lambda state: state.has("Stone Mask", world.player))

    # Statue needs all 3 essences to lower down artemis
    add_rule(world.multiworld.get_location("Mission #6 - Artemis", world.player),
             lambda state: state.count_group("essences", world.player) == 3)

    # Flight of the Demon, needs air raid and DT (Needs Stone Mask to raise bridge leading to it)
    add_rule(world.multiworld.get_location("Secret Mission #6", world.player),
             lambda state: has_air_raid(state, world) and
                           has_devil_trigger(state, world) and state.has("Stone Mask", world.player))


def set_rules(dmc3_world) -> None:
    if True:
        add_linear_rules(dmc3_world)

    add_generic_rules(dmc3_world)

    for adjudicator in adjudicators:
        weapon = dmc3_world.adjudicator_generated_values[adjudicator].weapon
        location = dmc3_world.multiworld.get_location(adjudicator, dmc3_world.player)
        add_rule(location,
                 lambda state, wep=weapon:
                 state.has(wep, dmc3_world.player))

    dmc3_world.multiworld.completion_condition[dmc3_world.player] = lambda state: state.has("Finish Game",
                                                                                            dmc3_world.player)
