from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .data import data
from .options import JohtoOnly, Route32Condition, UndergroundsRequirePower, Route2Access, BlackthornDarkCaveAccess, \
    NationalParkAccess, KantoAccessCondition, Route3Access

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def can_map_card_fly(state: CollectionState, world: "PokemonCrystalWorld"):
    if world.options.randomize_pokegear:
        return state.has("Map Card", world.player) and state.has("Pokegear", world.player)
    return state.has("EVENT_GOT_MAP_CARD", world.player) and state.has("EVENT_GOT_POKEGEAR", world.player)


def set_rules(world: "PokemonCrystalWorld") -> None:
    if world.options.hm_badge_requirements == 0:
        def can_cut(state: CollectionState):
            return state.has("HM01 Cut", world.player) and has_badge(state, "hive")

        def can_fly(state: CollectionState):
            return state.has("HM02 Fly", world.player) and has_badge(state, "storm")

        def can_surf(state: CollectionState):
            return state.has("HM03 Surf", world.player) and has_badge(state, "fog")

        def can_strength(state: CollectionState):
            return state.has("HM04 Strength", world.player) and has_badge(state, "plain")

        def can_flash(state: CollectionState):
            return state.has("HM05 Flash", world.player) and has_badge(state, "zephyr")

        def can_whirlpool(state: CollectionState):
            return state.has("HM06 Whirlpool", world.player) and has_badge(state, "glacier") and can_surf(state)

        def can_waterfall(state: CollectionState):
            return state.has("HM07 Waterfall", world.player) and has_badge(state, "rising") and can_surf(state)
    elif world.options.hm_badge_requirements == 1:
        def can_cut(state: CollectionState):
            return state.has("HM01 Cut", world.player)

        def can_fly(state: CollectionState):
            return state.has("HM02 Fly", world.player)

        def can_surf(state: CollectionState):
            return state.has("HM03 Surf", world.player)

        def can_strength(state: CollectionState):
            return state.has("HM04 Strength", world.player)

        def can_flash(state: CollectionState):
            return state.has("HM05 Flash", world.player)

        def can_whirlpool(state: CollectionState):
            return state.has("HM06 Whirlpool", world.player) and can_surf(state)

        def can_waterfall(state: CollectionState):
            return state.has("HM07 Waterfall", world.player) and can_surf(state)
    else:
        def can_cut(state: CollectionState):
            return state.has("HM01 Cut", world.player) and (
                    has_badge(state, "hive") or has_badge(state, "cascade"))

        def can_fly(state: CollectionState):
            return state.has("HM02 Fly", world.player) and (
                    has_badge(state, "storm") or has_badge(state, "thunder"))

        def can_surf(state: CollectionState):
            return state.has("HM03 Surf", world.player) and (
                    has_badge(state, "fog") or has_badge(state, "soul"))

        def can_strength(state: CollectionState):
            return state.has("HM04 Strength", world.player) and (
                    has_badge(state, "plain") or has_badge(state, "rainbow"))

        def can_flash(state: CollectionState):
            return state.has("HM05 Flash", world.player) and (
                    has_badge(state, "zephyr") or has_badge(state, "boulder"))

        def can_whirlpool(state: CollectionState):
            return state.has("HM06 Whirlpool", world.player) and (
                    has_badge(state, "glacier") or has_badge(state, "volcano")) and can_surf(state)

        def can_waterfall(state: CollectionState):
            return state.has("HM07 Waterfall", world.player) and (
                    has_badge(state, "rising") or has_badge(state, "earth")) and can_surf(state)

    if "Cut" in world.options.remove_badge_requirement:
        def can_cut(state: CollectionState):
            return state.has("HM01 Cut", world.player)

    if "Fly" in world.options.remove_badge_requirement:
        def can_fly(state: CollectionState):
            return state.has("HM02 Fly", world.player)

    if "Surf" in world.options.remove_badge_requirement:
        def can_surf(state: CollectionState):
            return state.has("HM03 Surf", world.player)

    if "Strength" in world.options.remove_badge_requirement:
        def can_strength(state: CollectionState):
            return state.has("HM04 Strength", world.player)

    if "Flash" in world.options.remove_badge_requirement:
        def can_flash(state: CollectionState):
            return state.has("HM05 Flash", world.player)

    if "Whirlpool" in world.options.remove_badge_requirement:
        def can_whirlpool(state: CollectionState):
            return state.has("HM06 Whirlpool", world.player)

    if "Waterfall" in world.options.remove_badge_requirement:
        def can_waterfall(state: CollectionState):
            return state.has("HM07 Waterfall", world.player)

    def can_rocksmash(state: CollectionState):
        return state.has("TM08 Rock Smash", world.player)

    def has_tea(state: CollectionState):
        return state.has("Tea", world.player)

    if world.options.randomize_badges.value == 0:
        badge_items = {"zephyr": "EVENT_ZEPHYR_BADGE_FROM_FALKNER",
                       "hive": "EVENT_HIVE_BADGE_FROM_BUGSY",
                       "plain": "EVENT_PLAIN_BADGE_FROM_WHITNEY",
                       "fog": "EVENT_FOG_BADGE_FROM_MORTY",
                       "mineral": "EVENT_STORM_BADGE_FROM_CHUCK",
                       "storm": "EVENT_MINERAL_BADGE_FROM_JASMINE",
                       "glacier": "EVENT_GLACIER_BADGE_FROM_PRYCE",
                       "rising": "EVENT_RISING_BADGE_FROM_CLAIR",

                       "boulder": "EVENT_BOULDER_BADGE_FROM_BROCK",
                       "cascade": "EVENT_CASCADE_BADGE_FROM_MISTY",
                       "thunder": "EVENT_THUNDER_BADGE_FROM_LTSURGE",
                       "rainbow": "EVENT_RAINBOW_BADGE_FROM_ERIKA",
                       "soul": "EVENT_SOUL_BADGE_FROM_JANINE",
                       "marsh": "EVENT_MARSH_BADGE_FROM_SABRINA",
                       "volcano": "EVENT_VOLCANO_BADGE_FROM_BLAINE",
                       "earth": "EVENT_EARTH_BADGE_FROM_BLUE"
                       }
    else:
        badge_items = {"zephyr": "Zephyr Badge",
                       "hive": "Hive Badge",
                       "plain": "Plain Badge",
                       "fog": "Fog Badge",
                       "mineral": "Mineral Badge",
                       "storm": "Storm Badge",
                       "glacier": "Glacier Badge",
                       "rising": "Rising Badge",

                       "boulder": "Boulder Badge",
                       "cascade": "Cascade Badge",
                       "thunder": "Thunder Badge",
                       "rainbow": "Rainbow Badge",
                       "soul": "Soul Badge",
                       "marsh": "Marsh Badge",
                       "volcano": "Volcano Badge",
                       "earth": "Earth Badge"
                       }

    def has_badge(state: CollectionState, badge):
        return state.has(badge_items[badge], world.player)

    def has_n_badges(state: CollectionState, n: int) -> bool:
        return state.has_from_list_unique(badge_items.values(), world.player, n)

    def has_rocket_badges(state: CollectionState):
        return has_n_badges(state, world.options.radio_tower_badges.value)

    def has_elite_four_badges(state: CollectionState):
        return has_n_badges(state, world.options.elite_four_badges.value)

    def has_red_badges(state: CollectionState):
        return has_n_badges(state, world.options.red_badges.value)

    def has_mt_silver_badges(state: CollectionState):
        return has_n_badges(state, world.options.mt_silver_badges.value)

    def has_kanto_access_badges(state: CollectionState):
        return has_n_badges(state, world.options.kanto_access_badges.value)

    def get_entrance(entrance: str):
        return world.multiworld.get_entrance(entrance, world.player)

    def get_location(location: str):
        if location in data.locations:
            location = data.locations[location].label

        return world.multiworld.get_location(location, world.player)

    def hidden():
        return world.options.randomize_hidden_items

    def pokegear():
        return world.options.randomize_pokegear

    def johto_only():
        return world.options.johto_only.value

    def trainersanity():
        return world.options.trainersanity

    def remove_ilex_cut_tree():
        return world.options.remove_ilex_cut_tree

    def require_badge_for_route_32():
        return world.options.route_32_condition.value == Route32Condition.option_any_badge

    def require_egg_for_route_32():
        return world.options.route_32_condition.value == Route32Condition.option_egg_from_aide

    def expn(state: CollectionState):
        if pokegear():
            return (state.has("Pokegear", world.player)
                    and state.has("Radio Card", world.player)
                    and state.has("EXPN Card", world.player))
        else:
            return (state.has("EVENT_GOT_POKEGEAR", world.player)
                    and state.has("EVENT_GOT_RADIO_CARD", world.player)
                    and state.has("EVENT_GOT_EXPN_CARD", world.player))

    # Free Fly
    set_rule(get_entrance("Fly"), can_fly)

    # Goal
    if world.options.goal == 1:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("EVENT_BEAT_RED", world.player)
    else:
        world.multiworld.completion_condition[world.player] = lambda state: state.has(
            "EVENT_BEAT_ELITE_FOUR", world.player)

    # New Bark Town
    # set_rule(get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_29"),
    #          lambda state: state.has("EVENT_GOT_A_POKEMON_FROM_ELM", world.player))

    set_rule(get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_27:WEST"), can_surf)

    # set_rule(get_location("Elm's Lab - Everstone from Elm"),
    #          lambda state: state.has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player))

    set_rule(get_location("Elm's Lab - Gift from Aide after returning Mystery Egg"),
             lambda state: state.has("Mystery Egg", world.player))

    set_rule(get_location("Elm's Lab - Master Ball from Elm"), lambda state: has_badge(state, "rising"))

    set_rule(get_location("Elm's Lab - S.S. Ticket from Elm"),
             lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    # Route 29
    set_rule(get_location("Route 29 - Pink Bow from Tuscany"), lambda state: has_badge(state, "zephyr"))
    # Route 30
    # set_rule(get_entrance("REGION_ROUTE_30 -> REGION_ROUTE_31"),
    #          lambda state: state.has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON", world.player))

    set_rule(get_location("Route 30 - Exp Share from Mr Pokemon"), lambda state: state.has("Red Scale", world.player))

    # Cherrygrove
    set_rule(get_location("Cherrygrove City - Mystic Water from Island Man"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_31 -> REGION_DARK_CAVE_VIOLET_ENTRANCE"), can_flash)

    if world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_waterfall:
        set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE"),
                 lambda state: can_surf(state) and can_waterfall(state))

    set_rule(get_location("EVENT_GAVE_KENYA"), lambda state: state.has("EVENT_GOT_KENYA", world.player))
    set_rule(get_location("Route 31 - TM50 for delivering Kenya"),
             lambda state: state.has("EVENT_GOT_KENYA", world.player))

    # Dark Cave Violet
    set_rule(get_location("Dark Cave Violet Entrance - Southeast Item (Left)"), can_rocksmash)
    set_rule(get_location("Dark Cave Violet Entrance - Southeast Item (Right)"), can_rocksmash)
    set_rule(get_location("Dark Cave Violet Entrance - Northeast Item"), can_rocksmash)
    if hidden():
        set_rule(get_location("Dark Cave Violet Entrance - Hidden Item"), can_rocksmash)

    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE -> REGION_ROUTE_46"), can_rocksmash)

    set_rule(get_entrance("REGION_ROUTE_46 -> REGION_DARK_CAVE_VIOLET_ENTRANCE"),
             lambda state: can_rocksmash(state) and can_flash(state))

    set_rule(get_entrance("REGION_ROUTE_45 -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE"),
             lambda state: can_surf(state) and can_flash(state))

    # Violet City
    if hidden():
        set_rule(get_location("Violet City - Hidden Item behind Cut Tree"), can_cut)
    set_rule(get_location("Violet City - Northwest Item across Water"), can_surf)
    set_rule(get_location("Violet City - Northeast Item across Water"), can_surf)

    set_rule(get_location("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE"),
             lambda state: state.has("EVENT_BEAT_FALKNER", world.player))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OUTSIDE:NORTH -> REGION_RUINS_OF_ALPH_OUTSIDE:SOUTH"),
             can_surf)
    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OUTSIDE:SOUTH -> REGION_RUINS_OF_ALPH_OUTSIDE:NORTH"),
             can_surf)

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_KABUTO_CHAMBER -> REGION_RUINS_OF_ALPH_KABUTO_ITEM_ROOM"),
             lambda state: state.has("EVENT_MART_ESCAPE_ROPE", world.player))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OMANYTE_CHAMBER -> REGION_RUINS_OF_ALPH_OMANYTE_ITEM_ROOM"),
             lambda state: state.has("EVENT_MART_WATER_STONE", world.player))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_AERODACTYL_CHAMBER -> REGION_RUINS_OF_ALPH_AERODACTYL_ITEM_ROOM"),
             can_flash)

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_HO_OH_CHAMBER -> REGION_RUINS_OF_ALPH_HO_OH_ITEM_ROOM"),
             lambda state: state.has("Rainbow Wing", world.player))

    # Route 32
    if require_badge_for_route_32():
        set_rule(get_entrance("REGION_ROUTE_32:NORTH -> REGION_ROUTE_32:SOUTH"), lambda state: has_n_badges(state, 1))

    if require_egg_for_route_32():
        set_rule(get_entrance("REGION_ROUTE_32:NORTH -> REGION_ROUTE_32:SOUTH"),
                 lambda state: state.has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player))

    set_rule(get_location("Route 32 - Miracle Seed from Man in North"), lambda state: has_badge(state, "zephyr"))
    set_rule(get_location("Route 32 - TM05 from Roar Guy"), can_cut)

    # Union Cave
    set_rule(get_entrance("REGION_UNION_CAVE_1F -> REGION_UNION_CAVE_B1F:SOUTH"), can_surf)
    set_rule(get_entrance("REGION_UNION_CAVE_B1F -> REGION_UNION_CAVE_B1F:NORTH"), can_surf)
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:NORTH -> REGION_RUINS_OF_ALPH_OUTSIDE:SOUTH:UNION_LEDGE"),
             can_strength)
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:SOUTH -> REGION_UNION_CAVE_B2F"), can_surf)

    # Azalea Town
    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F -> REGION_SLOWPOKE_WELL_B2F"),
             lambda state: can_strength(state) and can_surf(state))

    set_rule(get_entrance("REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    set_rule(get_location("Azalea Town - Lure Ball from Kurt"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    set_rule(get_location("RIVAL_BAYLEEF_1"), lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))
    set_rule(get_location("RIVAL_CROCONAW_1"), lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))
    set_rule(get_location("RIVAL_QUILAVA_1"), lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    # Ilex Forest
    if not remove_ilex_cut_tree():
        set_rule(get_entrance("REGION_ILEX_FOREST:NORTH -> REGION_ILEX_FOREST:SOUTH"), can_cut)
        set_rule(get_entrance("REGION_ILEX_FOREST:SOUTH -> REGION_ILEX_FOREST:NORTH"), can_cut)

    set_rule(get_location("Celebi"), lambda state: state.has("GS Ball", world.player))

    add_rule(get_entrance("REGION_ILEX_FOREST:SOUTH -> REGION_ILEX_FOREST:NORTH"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    # Route 34
    set_rule(get_entrance("REGION_ROUTE_34 -> REGION_ROUTE_34:WATER"), can_surf)

    # Goldenrod City
    set_rule(get_location("Goldenrod City - Squirtbottle from Flower Shop"),
             lambda state: has_badge(state, "plain"))
    set_rule(get_location("Goldenrod City - Post-E4 GS Ball from Trade Corner Receptionist"),
             lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    if not johto_only():
        set_rule(get_entrance("REGION_GOLDENROD_MAGNET_TRAIN_STATION -> REGION_SAFFRON_MAGNET_TRAIN_STATION"),
                 lambda state: state.has("Pass", world.player))

    # Underground

    set_rule(get_entrance("REGION_GOLDENROD_UNDERGROUND -> REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES"),
             lambda state: state.has("Basement Key", world.player))

    set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_B1F -> REGION_GOLDENROD_DEPT_STORE_B1F:WAREHOUSE"),
             lambda state: state.has("Card Key", world.player))

    set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_B1F:WAREHOUSE -> REGION_GOLDENROD_DEPT_STORE_B1F"),
             lambda state: state.has("Card Key", world.player))

    set_rule(get_entrance("REGION_GOLDENROD_UNDERGROUND_WAREHOUSE -> REGION_GOLDENROD_UNDERGROUND_WAREHOUSE:TAKEOVER"),
             has_rocket_badges)

    set_rule(get_entrance(
        "REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES -> REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES:TAKEOVER"),
        has_rocket_badges)

    # Radio Tower

    set_rule(get_entrance("REGION_RADIO_TOWER_2F -> REGION_RADIO_TOWER_3F:NOCARDKEY"), has_rocket_badges)

    set_rule(get_entrance("REGION_RADIO_TOWER_3F:NOCARDKEY -> REGION_RADIO_TOWER_3F:CARDKEY"),
             lambda state: state.has("Card Key", world.player))

    set_rule(get_location("Radio Tower 3F - TM11 from Woman"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    set_rule(get_location("Radio Tower 4F - Pink Bow from Mary"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    set_rule(get_location("GRUNTM_3"), has_rocket_badges)
    set_rule(get_location("GRUNTM_4"), has_rocket_badges)
    set_rule(get_location("GRUNTM_5"), has_rocket_badges)
    set_rule(get_location("GRUNTM_6"), has_rocket_badges)
    set_rule(get_location("GRUNTF_2"), has_rocket_badges)

    if trainersanity():
        set_rule(get_location("Radio Tower 1F - Grunt"), has_rocket_badges)

        set_rule(get_location("Radio Tower 2F - Grunt 1"), has_rocket_badges)
        set_rule(get_location("Radio Tower 2F - Grunt 2"), has_rocket_badges)
        set_rule(get_location("Radio Tower 2F - Grunt 3"), has_rocket_badges)
        set_rule(get_location("Radio Tower 2F - Grunt 4"), has_rocket_badges)

    # Route 35
    set_rule(get_location("Route 35 - HP Up after delivering Kenya"),
             lambda state: state.has("EVENT_GAVE_KENYA", world.player))

    set_rule(get_entrance("REGION_ROUTE_35 -> REGION_ROUTE_35:FRUITTREE"), can_surf)

    if world.options.national_park_access.value == NationalParkAccess.option_bicycle:
        set_rule(get_entrance("REGION_ROUTE_35_NATIONAL_PARK_GATE -> REGION_NATIONAL_PARK"),
                 lambda state: state.has("Bicycle", world.player))
        set_rule(get_entrance("REGION_ROUTE_36_NATIONAL_PARK_GATE -> REGION_NATIONAL_PARK"),
                 lambda state: state.has("Bicycle", world.player))

    # Sudowoodo
    set_rule(get_entrance("REGION_ROUTE_36:EAST -> REGION_ROUTE_37"),
             lambda state: state.has("Squirtbottle", world.player))
    set_rule(get_entrance("REGION_ROUTE_36:EAST -> REGION_ROUTE_36:WEST"),
             lambda state: state.has("Squirtbottle", world.player))
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_36:EAST"),
             lambda state: state.has("Squirtbottle", world.player))
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_37"),
             lambda state: state.has("Squirtbottle", world.player))
    set_rule(get_entrance("REGION_ROUTE_37 -> REGION_ROUTE_36:EAST"),
             lambda state: state.has("Squirtbottle", world.player))
    set_rule(get_entrance("REGION_ROUTE_37 -> REGION_ROUTE_36:WEST"),
             lambda state: state.has("Squirtbottle", world.player))
    set_rule(get_entrance("REGION_ROUTE_35 -> REGION_ROUTE_36:WEST"), can_cut)
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_35"), can_cut)

    set_rule(get_location("Route 36 - TM08 from Rock Smash Guy"), lambda state: state.has("Squirtbottle", world.player))

    # Ecruteak City
    set_rule(get_entrance("REGION_ECRUTEAK_CITY -> REGION_ECRUTEAK_GYM"),
             lambda state: state.has("EVENT_BURNED_TOWER_MORTY", world.player))

    set_rule(get_location("Burned Tower 1F - Item"), can_rocksmash)
    set_rule(get_location("Burned Tower B1F - Item"), can_strength)

    set_rule(get_entrance("REGION_ECRUTEAK_CITY -> REGION_TIN_TOWER_1F"),
             lambda state: state.has("Clear Bell", world.player))
    set_rule(get_entrance("REGION_TIN_TOWER_1F -> REGION_TIN_TOWER_2F"),
             lambda state: state.has("Rainbow Wing", world.player))

    set_rule(get_location("Ho_Oh"), lambda state: state.has("Rainbow Wing", world.player))

    set_rule(get_location("Tin Tower 1F - Rainbow Wing"),
             lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    # Olivine City
    set_rule(get_location("EVENT_JASMINE_RETURNED_TO_GYM"), lambda state: state.has("Secretpotion", world.player))

    if not johto_only():
        set_rule(get_entrance("REGION_OLIVINE_PORT -> REGION_FAST_SHIP_1F"),
                 lambda state: state.has("S.S. Ticket", world.player))

        if hidden():
            set_rule(get_location("Olivine Port - Hidden Item in Southwest Buoy"),
                     lambda state: state.has("S.S. Ticket", world.player) and can_surf(state))

    set_rule(get_entrance("REGION_OLIVINE_CITY -> REGION_OLIVINE_GYM"),
             lambda state: state.has("EVENT_JASMINE_RETURNED_TO_GYM", world.player))

    # Route 40

    set_rule(get_entrance("REGION_ROUTE_40 -> REGION_ROUTE_40:WATER"), can_surf)

    if hidden():
        set_rule(get_location("Route 40 - Hidden Item in Rock"), can_rocksmash)

    # Route 41

    if hidden():
        set_rule(get_location("Route 41 - Hidden Item on Southwest Island"), can_whirlpool)

    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_NW"),
             lambda state: can_whirlpool(state) and can_flash(state))
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_NE"),
             lambda state: can_whirlpool(state) and can_flash(state))
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_SW"),
             lambda state: can_whirlpool(state) and can_flash(state))
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_SE"),
             lambda state: can_whirlpool(state) and can_flash(state))

    set_rule(get_location("Lugia"), lambda state: state.has("Silver Wing", world.player))

    # Cianwood
    set_rule(get_entrance("REGION_CIANWOOD_CITY -> REGION_ROUTE_41"), can_surf)
    if hidden():
        set_rule(get_location("Cianwood City - Hidden Item in West Rock"), can_rocksmash)

        set_rule(get_location("Cianwood City - Hidden Item in North Rock"), can_rocksmash)

    set_rule(get_location("Cianwood City - HM02 from Chuck's Wife"),
             lambda state: state.has("EVENT_BEAT_CHUCK", world.player))

    set_rule(get_entrance("REGION_CIANWOOD_GYM -> REGION_CIANWOOD_GYM:STRENGTH"), can_strength)

    set_rule(get_location("Cianwood Pharmacy - Secretpotion"),
             lambda state: state.has("EVENT_JASMINE_EXPLAINED_AMPHYS_SICKNESS", world.player))

    # Route 42

    set_rule(get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER"), can_surf)
    set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:WEST"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_42:EAST -> REGION_ROUTE_42:CENTER"), can_surf)
    set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:EAST"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:CENTERFRUIT"), can_cut)

    if hidden():
        set_rule(get_location("Route 42 - Hidden Item in Pond Rock"), can_surf)

    # Mt Mortar
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER -> REGION_MOUNT_MORTAR_2F_OUTSIDE"),
             lambda state: can_surf(state) and can_waterfall(state))

    # 1F Inside Front
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_INSIDE:FRONT -> REGION_MOUNT_MORTAR_1F_INSIDE:STRENGTH"),
             can_strength)
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_INSIDE:STRENGTH -> REGION_MOUNT_MORTAR_1F_INSIDE:FRONT"),
             can_strength)

    # 1F C -> B1F Everything needs surf so im being lazy

    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER -> REGION_MOUNT_MORTAR_B1F"), can_surf)

    # Behind boulder, need to come down from 2F for this

    set_rule(get_entrance("REGION_MOUNT_MORTAR_B1F:BACK -> REGION_MOUNT_MORTAR_B1F"),
             lambda state: can_strength(state) and can_surf(state) and can_waterfall(state))

    # Mahogany Town

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_MART_1F"),
             lambda state: state.has("EVENT_DECIDED_TO_HELP_LANCE", world.player))

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_GYM"),
             lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_ROUTE_44"), has_rocket_badges)

    # Route 43

    set_rule(get_entrance("REGION_ROUTE_43 -> REGION_ROUTE_43:FRUITTREE"),
             lambda state: can_cut(state) and can_surf(state))

    set_rule(get_location("Route 43 - Sludge Bomb from Guard in Gate"),
             lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))

    # Lake of Rage
    if world.options.red_gyarados_access:
        set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:WATER"),
                 lambda state: can_surf(state) and can_whirlpool(state))
    else:
        set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:WATER"), can_surf)

    set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:CUT"), can_cut)

    # Route 44

    if hidden():
        set_rule(get_location("Route 44 - Hidden Item across Water"), can_surf)

    set_rule(get_location("Route 44 - Center Item across Water"), can_surf)

    # Ice Path
    set_rule(get_entrance("REGION_ICE_PATH_B2F_MAHOGANY_SIDE -> REGION_ICE_PATH_B2F_MAHOGANY_SIDE:MIDDLE"),
             can_strength)

    # Blackthorn

    set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_BLACKTHORN_GYM_1F"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    set_rule(get_entrance("REGION_BLACKTHORN_GYM_2F -> REGION_BLACKTHORN_GYM_1F:STRENGTH"), can_strength)

    set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_DRAGONS_DEN_1F"),
             lambda state: state.has("EVENT_BEAT_CLAIR", world.player) and can_surf(state))

    # Dragons Den
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F -> REGION_DRAGONS_DEN_B1F:WATER"), can_surf)
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:WATER -> REGION_DRAGONS_DEN_B1F:WHIRLPOOL"), can_whirlpool)

    # Route 45

    if hidden():
        set_rule(get_location("Route 45 - Hidden Item in Southeast Pond"), can_surf)

    # Route 27

    set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_NEW_BARK_TOWN"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_ROUTE_27:WESTWATER"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:CENTER -> REGION_ROUTE_27:EAST"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:EAST -> REGION_ROUTE_27:CENTER"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:EAST -> REGION_ROUTE_27:EASTWHIRLPOOL"), can_whirlpool)

    set_rule(get_location("Route 27 - West Item across Water"), can_surf)

    set_rule(get_location("Route 27 - East Item behind Whirlpool"),
             lambda state: can_surf(state) and can_whirlpool(state))
    if trainersanity():
        set_rule(get_location("Route 27 - Bird Keeper Jose"), lambda state: can_surf(state) and can_whirlpool(state))

    set_rule(get_location("Tohjo Falls - Item"), can_surf)

    set_rule(get_entrance("REGION_TOHJO_FALLS:WEST -> REGION_TOHJO_FALLS:EAST"),
             lambda state: can_surf(state) and can_waterfall(state))
    set_rule(get_entrance("REGION_TOHJO_FALLS:EAST -> REGION_TOHJO_FALLS:WEST"),
             lambda state: can_surf(state) and can_waterfall(state))

    set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_VICTORY_ROAD"), has_elite_four_badges)

    # Victory Road

    if johto_only() != JohtoOnly.option_on:
        set_rule(get_entrance("REGION_ROUTE_28 -> REGION_VICTORY_ROAD_GATE"),
                 lambda state: state.has("EVENT_OPENED_MT_SILVER", world.player))
        set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_28"),
                 lambda state: state.has("EVENT_OPENED_MT_SILVER", world.player))

        set_rule(get_location("EVENT_OPENED_MT_SILVER"), has_mt_silver_badges)
        set_rule(get_location("EVENT_BEAT_RED"), has_red_badges)
        # set_rule(get_location("RED_1"), has_red_badges)

        # Route 28
        set_rule(get_location("Route 28 - Steel Wing from Celebrity in House"), can_cut)
        if hidden():
            set_rule(get_location("Route 28 - Hidden Item behind Cut Tree"), can_cut)

        # Silver Cave
        set_rule(get_entrance("REGION_SILVER_CAVE_OUTSIDE -> REGION_SILVER_CAVE_ROOM_1"), can_flash)

        if hidden():
            set_rule(get_location("Outside Silver Cave - Hidden Item across Water"), can_surf)

        set_rule(get_location("Silver Cave 2F - Northeast Item"),
                 lambda state: can_surf(state) and can_waterfall(state))

        set_rule(get_location("Silver Cave 2F - West Item"), lambda state: can_surf(state) and can_waterfall(state))

        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2 -> REGION_SILVER_CAVE_ITEM_ROOMS"),
                 lambda state: can_surf(state) and can_waterfall(state))

    if not johto_only():

        if world.options.kanto_access_condition.value == KantoAccessCondition.option_wake_snorlax:
            set_rule(get_entrance("REGION_ROUTE_22 -> REGION_VICTORY_ROAD_GATE"),
                     lambda state: state.has("EVENT_FOUGHT_SNORLAX", world.player))

            set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_22"),
                     lambda state: state.has("EVENT_FOUGHT_SNORLAX", world.player))
        elif world.options.kanto_access_condition.value == KantoAccessCondition.option_become_champion:
            set_rule(get_entrance("REGION_ROUTE_22 -> REGION_VICTORY_ROAD_GATE"),
                     lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
            set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_22"),
                     lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))
        elif world.options.kanto_access_condition.value == KantoAccessCondition.option_badge_count:
            set_rule(get_entrance("REGION_ROUTE_22 -> REGION_VICTORY_ROAD_GATE"), has_kanto_access_badges)
            set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_22"), has_kanto_access_badges)

        # Viridian
        set_rule(get_location("Viridian City - TM42 from Sleepy Guy"), lambda state: can_surf(state) or can_cut(state))

        set_rule(get_entrance("REGION_VIRIDIAN_CITY -> REGION_VIRIDIAN_GYM"),
                 lambda state: state.has("EVENT_VIRIDIAN_GYM_BLUE", world.player))

        # Route 2
        if world.options.route_2_access.value != Route2Access.option_open:
            set_rule(get_entrance("REGION_ROUTE_2:WEST -> REGION_ROUTE_2:NORTHEAST"), can_cut)
        if world.options.route_2_access.value == Route2Access.option_vanilla:
            set_rule(get_entrance("REGION_ROUTE_2:NORTHEAST -> REGION_ROUTE_2:WEST"), can_cut)

        set_rule(get_entrance("REGION_ROUTE_2:WEST -> REGION_ROUTE_2:SOUTHEAST"), can_cut)

        set_rule(get_entrance("REGION_ROUTE_2:SOUTHEAST -> REGION_ROUTE_2:WEST"), can_cut)

        set_rule(get_entrance("REGION_ROUTE_2:SOUTHEAST -> REGION_ROUTE_2:NORTHEAST"), can_cut)

        set_rule(get_entrance("REGION_ROUTE_2:NORTHEAST -> REGION_ROUTE_2:SOUTHEAST"), can_cut)

        # Route 3
        if world.options.route_3_access.value == Route3Access.option_boulder_badge:
            set_rule(get_entrance("REGION_PEWTER_CITY -> REGION_ROUTE_3"),
                     lambda state: has_badge(state, "boulder"))
            set_rule(get_entrance("REGION_ROUTE_3 -> REGION_PEWTER_CITY"),
                     lambda state: has_badge(state, "boulder"))

        if hidden():
            set_rule(get_location("Mount Moon Square - Hidden Item under Rock"), can_rocksmash)

        # Cerulean
        if hidden():
            set_rule(get_location("Cerulean City - Hidden Item in Water"), can_surf)

        set_rule(get_entrance("REGION_CERULEAN_CITY -> REGION_ROUTE_9"), can_cut)

        set_rule(get_entrance("REGION_ROUTE_9 -> REGION_CERULEAN_CITY"), can_cut)

        set_rule(get_entrance("REGION_ROUTE_10_NORTH -> REGION_POWER_PLANT"), can_surf)

        # Route 25
        set_rule(get_location("Route 25 - Item behind Cut Tree"), can_cut)

        # Power Plant
        set_rule(get_location("EVENT_RESTORED_POWER_TO_KANTO"), lambda state: state.has("Machine Part", world.player))

        set_rule(get_location("Power Plant - TM07 from Manager"),
                 lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

        # Rock Tunnel
        set_rule(get_entrance("REGION_ROUTE_9 -> REGION_ROCK_TUNNEL_1F"), can_flash)

        set_rule(get_entrance("REGION_ROUTE_10_SOUTH -> REGION_ROCK_TUNNEL_1F"), can_flash)

        # Lavendar

        if pokegear():
            set_rule(get_location("Lavender Radio Tower - EXPN Card"), lambda state: state.has(
                "EVENT_RESTORED_POWER_TO_KANTO", world.player))
        else:
            set_rule(get_location("EVENT_GOT_EXPN_CARD"), lambda state: state.has(
                "EVENT_RESTORED_POWER_TO_KANTO", world.player))

        # Route 12

        set_rule(get_location("Route 12 - Item behind North Cut Tree"), can_cut)

        set_rule(get_location("Route 12 - Item behind South Cut Tree across Water"),
                 lambda state: can_cut(state) and can_surf(state))

        if hidden():
            set_rule(get_location("Route 12 - Hidden Item on Island"), can_surf)

        # Vermilion
        set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_VERMILION_GYM"),
                 lambda state: can_cut(state) or can_surf(state))

        set_rule(get_location("Vermilion City - HP Up from Man by PokeCenter"), lambda state: has_n_badges(state, 16))

        set_rule(get_location("Vermilion City - Lost Item from Guy in Fan Club"),
                 lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player) and state.has(
                     "EVENT_MET_COPYCAT_FOUND_OUT_ABOUT_LOST_ITEM", world.player))

        if hidden():
            set_rule(get_location("Vermilion Port - Hidden Item in Buoy"), can_surf)

        set_rule(get_location("EVENT_FOUGHT_SNORLAX"), expn)

        set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_ROUTE_11"), expn)

        set_rule(get_entrance("REGION_ROUTE_11 -> REGION_VERMILION_CITY"), expn)

        set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_DIGLETTS_CAVE"), expn)

        set_rule(get_entrance("REGION_DIGLETTS_CAVE -> REGION_VERMILION_CITY"), expn)

        set_rule(get_entrance("REGION_VERMILION_PORT_PASSAGE -> REGION_VERMILION_PORT"),
                 lambda state: state.has("S.S. Ticket", world.player))

        # Saffron
        set_rule(get_location("Copycat's House - Pass from Copycat"),
                 lambda state: state.has("Lost Item", world.player))

        set_rule(get_entrance("REGION_SAFFRON_MAGNET_TRAIN_STATION -> REGION_GOLDENROD_MAGNET_TRAIN_STATION"),
                 lambda state: state.has("Pass", world.player))

        if "North" in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_ROUTE_5_SAFFRON_GATE"), has_tea)
            set_rule(get_entrance("REGION_ROUTE_5_SAFFRON_GATE -> REGION_SAFFRON_CITY"), has_tea)

        if "East" in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_ROUTE_8_SAFFRON_GATE"), has_tea)
            set_rule(get_entrance("REGION_ROUTE_8_SAFFRON_GATE -> REGION_SAFFRON_CITY"), has_tea)

        if "South" in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_ROUTE_6_SAFFRON_GATE"), has_tea)
            set_rule(get_entrance("REGION_ROUTE_6_SAFFRON_GATE -> REGION_SAFFRON_CITY"), has_tea)

        if "West" in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_ROUTE_7_SAFFRON_GATE"), has_tea)
            set_rule(get_entrance("REGION_ROUTE_7_SAFFRON_GATE -> REGION_SAFFRON_CITY"), has_tea)

        # Underground Paths
        if world.options.undergrounds_require_power.value in [UndergroundsRequirePower.option_north_south,
                                                              UndergroundsRequirePower.option_both]:
            set_rule(get_entrance("REGION_ROUTE_5 -> REGION_ROUTE_5_UNDERGROUND_PATH_ENTRANCE"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

            set_rule(get_entrance("REGION_ROUTE_6 -> REGION_ROUTE_6_UNDERGROUND_PATH_ENTRANCE"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

        if (world.options.east_west_underground
                and world.options.undergrounds_require_power.value in [
                    UndergroundsRequirePower.option_east_west,
                    UndergroundsRequirePower.option_both]):
            set_rule(get_entrance("REGION_ROUTE_7 -> REGION_ROUTE_8"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

            set_rule(get_entrance("REGION_ROUTE_8 -> REGION_ROUTE_7"),
                     lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

        # Celadon

        set_rule(get_entrance("REGION_CELADON_CITY -> REGION_CELADON_GYM"), can_cut)

        # Cycling Road
        set_rule(get_entrance("REGION_ROUTE_16 -> REGION_ROUTE_17"), lambda state: state.has("Bicycle", world.player))

        set_rule(get_entrance("REGION_ROUTE_17_ROUTE_18_GATE -> REGION_ROUTE_17"),
                 lambda state: state.has("Bicycle", world.player))

        # Route 15
        set_rule(get_location("Route 15 - Item"), can_cut)

        # Fuchsia City
        if world.options.randomize_berry_trees:
            set_rule(get_location("Fuchsia City - Berry Tree"), can_cut)

        set_rule(get_entrance("REGION_ROUTE_19_FUCHSIA_GATE -> REGION_ROUTE_19"),
                 lambda state: state.has("EVENT_CINNABAR_ROCKS_CLEARED", world.player) and can_surf(state))

        set_rule(get_entrance("REGION_CINNABAR_ISLAND -> REGION_ROUTE_20"), can_surf)

        set_rule(get_entrance("REGION_CINNABAR_ISLAND -> REGION_ROUTE_21"), can_surf)

        set_rule(get_entrance("REGION_PALLET_TOWN -> REGION_ROUTE_21"), can_surf)

    if world.options.require_itemfinder:
        for location in world.multiworld.get_locations(world.player):
            if "Hidden" in location.tags:
                add_rule(location, lambda state: state.has("Itemfinder", world.player))
