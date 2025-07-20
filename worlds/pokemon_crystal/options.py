from dataclasses import dataclass

from Options import Toggle, Choice, DefaultOnToggle, Range, PerGameCommonOptions, NamedRange, OptionSet, \
    StartInventoryPool, OptionDict, Visibility, DeathLink, OptionGroup
from .data import data


class Goal(Choice):
    """
    Elite Four: Defeat the Champion and enter the Hall of Fame
    Red: Defeat Red at Mt. Silver
    """
    display_name = "Goal"
    default = 0
    option_elite_four = 0
    option_red = 1


class JohtoOnly(Choice):
    """
    Excludes all of Kanto, disables Kanto access
    Forces Goal to Elite Four unless Silver Cave is included
    Goal badges will be limited to 8 if badges are shuffled or vanilla
    """
    display_name = "Johto Only"
    default = 0
    option_off = 0
    option_on = 1
    option_include_silver_cave = 2


class EliteFourRequirement(Choice):
    """
    Sets the requirement to enter Victory Road
    """
    display_name = "Elite Four Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class EliteFourCount(Range):
    """
    Sets the number of badges/gyms required to enter Victory Road
    """
    display_name = "Elite Four Count"
    default = 8
    range_start = 0
    range_end = 16


class RedRequirement(Choice):
    """
    Sets the requirement to battle Red
    """
    display_name = "Red Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class RedCount(Range):
    """
    Number of badges/gyms required to battle Red
    """
    display_name = "Red Count"
    default = 16
    range_start = 0
    range_end = 16


class MtSilverRequirement(Choice):
    """
    Sets the requirement to access Mt. Silver and Silver Cave
    """
    display_name = "Mt. Silver Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class MtSilverCount(Range):
    """
    Number of badges/gyms required to access Mt. Silver and Silver Cave
    """
    display_name = "Mt. Silver Count"
    default = 16
    range_start = 0
    range_end = 16


class RadioTowerRequirement(Choice):
    """
    Sets the requirement for Team Rocket to take over the Goldenrod Radio Tower
    """
    display_name = "Radio Tower Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class RadioTowerCount(Range):
    """
    Number of badges/gyms at which Team Rocket takes over the Goldenrod Radio Tower
    """
    display_name = "Radio Tower Count"
    default = 7
    range_start = 0
    range_end = 16


class Route44AccessRequirement(Choice):
    """
    Sets the requirement to pass between Mahogany Town and Route 44
    """
    display_name = "Route 44 Access Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class Route44AccessCount(Range):
    """
    Sets the number of badges/gyms required to pass between Mahogany Town and Route 44
    """
    display_name = "Route 44 Access Count"
    default = 7
    range_start = 0
    range_end = 16


class RandomizeStartingTown(Toggle):
    """
    Randomly chooses a town to start in.
    Any Pokemon Center except Indigo Plateau, Cinnabar Island and Silver Cave can be chosen.
    Lake of Rage can also be chosen.

    Other settings may additionally restrict which Pokemon Centers can be chosen.

    WARNING: Some starting towns without level scaling may produce difficult starts.
    """
    display_name = "Randomize Starting Town"


class StartingTownBlocklist(OptionSet):
    """
    Specify places which cannot be chosen as a starting town. If you block every valid option, this list will do
    nothing.
    Indigo Plateau, Cinnabar Island and Silver Cave cannot be chosen as starting towns and are not valid options
    "_Johto" and "_Kanto" are shortcuts for all Johto and Kanto towns respectively
    """
    display_name = "Starting Town Blocklist"
    valid_keys = sorted(town.name for town in data.starting_towns) + ["_Johto", "_Kanto"]


class VanillaClair(Toggle):
    """
    Clair refuses to give you the Rising Badge until you prove your worth
    to the Elders in the Dragon's Den Shrine, which requires Whirlpool to access.
    """
    display_name = "Vanilla Clair"


class RandomizeBadges(Choice):
    """
    Shuffles gym badge locations into the pool
    Vanilla: Does not randomize gym badges
    Shuffle: Randomizes gym badges between gym leaders
    Completely Random: Randomizes badges with all other items
    """
    display_name = "Randomize Badges"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeHiddenItems(Toggle):
    """
    Shuffles hidden item locations into the pool
    """
    display_name = "Randomize Hidden Items"


class RequireItemfinder(Choice):
    """
    Hidden items require Itemfinder in logic

    Not Required: Hidden items do not require the Itemfinder at all
    Logically Required: Hidden items will expect you to have Itemfinder for logic but can be picked up without it
    Hard Required: Hidden items cannot be picked up without the Itemfinder
    """
    display_name = "Require Itemfinder"
    default = 1
    option_not_required = 0
    option_logically_required = 1
    option_hard_required = 2


class Route32Condition(Choice):
    """
    Sets the condition required to pass between the north and south parts of Route 32
    Egg from aide: Collect the Egg from the aide in the Violet City Pokemon Center after beating Falkner
    Any badge: Obtain any badge
    Any gym: Beat any gym
    Zephyr Badge: Obtain the Zephyr Badge
    None: No requirement
    """
    display_name = "Route 32 Access Condition"
    default = 0
    option_egg_from_aide = 0
    option_any_badge = 1
    option_any_gym = 2
    option_zephyr_badge = 3
    option_none = 4


class KantoAccessRequirement(Choice):
    """
    Sets the requirement to pass between Victory Road gate and Kanto
    Wake Snorlax: Wake the Snorlax outside of Diglett's Cave
    Badges: Requires the number of badges specified by kanto_access_count
    Gyms: Requires beating the number of gyms specified by kanto_access_count
    Become Champion: Defeat Lance and enter the Hall of Fame

    This setting does nothing if Johto Only is enabled
    """
    display_name = "Kanto Access Requirement"
    default = 0
    option_wake_snorlax = 0
    option_badges = 1
    option_gyms = 2
    option_become_champion = 3


class KantoAccessCount(Range):
    """
    Sets the number of badges/gyms required to pass between Victory Road gate and Kanto
    Only applies if Kanto Access Condition is set to badges or gyms
    """
    display_name = "Kanto Access Count"
    default = 8
    range_start = 0
    range_end = 16


class RedGyaradosAccess(Choice):
    """
    Sets whether the Red Gyarados requires Whirlpool to access
    """
    display_name = "Red Gyarados Access"
    default = 0
    option_vanilla = 0
    option_whirlpool = 1


class Route2Access(Choice):
    """
    Sets the roadblock for moving between the west of Route 2 and Diglett's cave
    Vanilla: Cut is required
    Ledge: A ledge is added north of Diglett's cave allowing east -> west access without Cut
    Open: No requirement
    """
    display_name = "Route 2 Access"
    default = 1
    option_vanilla = 0
    option_ledge = 1
    option_open = 2


class Route3Access(Choice):
    """
    Sets the roadblock for moving between Pewter City and Route 3
    Vanilla: No requirement
    Boulder Badge: The Boulder Badge is required to pass
    """
    display_name = "Route 3 Access"
    default = 0
    option_vanilla = 0
    option_boulder_badge = 1


class BlackthornDarkCaveAccess(Choice):
    """
    Sets the roadblock for travelling from Route 31 to Blackthorn City through Dark Cave
    Vanilla: Traversal is not possible
    Waterfall: A waterfall is added to the Violet side of Dark Cave and a ledge is removed on the Blackthorn side,
    allowing passage with Flash, Surf and Waterfall
    """
    display_name = "Blackthorn Dark Cave Access"
    default = 0
    option_vanilla = 0
    option_waterfall = 1


class NationalParkAccess(Choice):
    """
    Sets the requirement to enter National Park
    Vanilla: No requirement
    Bicycle: The Bicycle is required
    """
    display_name = "National Park Access"
    default = 0
    option_vanilla = 0
    option_bicycle = 1


class MountMortarAccess(Choice):
    """
    Sets the requirement to pass through Mount Mortar east <> west
    Vanilla: No requirement
    Rock Smash: Rock Smash is required
    """
    default = 0
    option_vanilla = 0
    option_rock_smash = 1


class Trainersanity(Toggle):
    """
    Adds checks for defeating trainers
    """
    display_name = "Trainersanity"


class Rematchsanity(Toggle):
    """
    Adds rematch fights to the level scaling pool
    Note: This is extremely beta, and the logic and patch aren't fully fleshed out.
    This means that the game requires you beat the rematches in vanilla order,
    but the ap logic might have them in a different order, so earlier rematches might
    be higher level than later ones.
    """
    display_name = "Rematchsanity"
    visibility = Visibility.none


class TrainersanityAlerts(Choice):
    """
    Shows a message box or plays a sound for Trainersanity checks
    """
    display_name = "Trainersanity Alerts"
    default = 1
    option_no_alerts = 0
    option_message_box = 1
    option_sound_only = 2


class Dexsanity(NamedRange):
    """
    Adds checks for catching Pokemon
    Pokemon that cannot be logically obtained will never be included
    """
    display_name = "Dexsanity"
    default = 0
    range_start = 0
    range_end = 251
    special_range_names = {
        "none": default,
        "full": range_end
    }


class Dexcountsanity(NamedRange):
    """
    Adds checks for completing Pokedex milestones
    This setting specifies number of caught Pokemon on which you'll get your last check
    """
    display_name = "Dexcountsanity"
    default = 0
    range_start = 0
    range_end = 251
    special_range_names = {
        "none": default,
        "full": range_end
    }


class DexcountsanityStep(Range):
    """
    If Dexcountsanity is enabled, specifies the step interval at which your checks are placed.
    For example, if you have Dexcountsanity 50 and Dexcountsanity Step 10, you will have checks at
    10, 20, 30, 40 and 50 total Pokemon caught.
    """
    display_name = "Dexcountsanity Step"
    default = 1
    range_start = 1
    range_end = 251


class DexcountsanityLeniency(Range):
    """
    If Dexcountsanity is enabled, specifies the logic leniency for checks.
    For example, if you set Dexcountsanity Leniency to 5 and have a Dexcountsanity check at 10, you will not be
    logically required to obtain this check until you can obtain 15 Pokemon

    Checks that would go over the total number of logically available Pokemon will be clamped to that limit
    """
    display_name = "Dexcountsanity Leniency"
    default = 0
    range_start = 0
    range_end = 251


class DexsanityStarters(Choice):
    """
    Controls how Dexsanity treats starter Pokemon
    Allow: Starter Pokemon will be allowed as Dexsanity checks
    Block: Starter Pokemon will not be allowed as Dexsanity Checks
    Available Early: Starter Pokemon will all be obtainable in the wild immediately, unless there is nowhere to obtain
    wild Pokemon immediately
    """
    display_name = "Dexsanity Starters"
    default = 0
    option_allow = 0
    option_block = 1
    option_available_early = 2


class WildEncounterMethodsRequired(OptionSet):
    """
    Sets which wild encounter types may be logically required

    Swarms and roamers are NEVER in logic
    """
    display_name = "Wild Encounter Methods Required"
    valid_keys = ["Land", "Surfing", "Fishing", "Headbutt", "Rock Smash"]
    default = valid_keys


class EnforceWildEncounterMethodsLogic(Toggle):
    """
    Sets whether the game will prevent capture of Pokemon found through disabled wild encounter methods
    Statics and roamers can always be caught
    """
    display_name = "Enforce Wild Encounter Methods Logic"


class EvolutionMethodsRequired(OptionSet):
    """
    Sets which types of evolutions may be logically required
    """
    display_name = "Evolution Methods Required"
    valid_keys = ["Level", "Level Tyrogue", "Use Item", "Happiness"]
    default = valid_keys


class StaticPokemonRequired(DefaultOnToggle):
    """
    Sets whether static Pokemon may be logically required
    """
    display_name = "Static Pokemon Required"


class BreedingMethodsRequired(Choice):
    """
    Specifies which breeding methods may be logically required.
    """
    display_name = "Breeding Method Required"
    default = 1
    option_none = 0
    option_with_ditto = 1
    option_any = 2


class EvolutionGymLevels(Range):
    """
    Sets how many levels each beaten gym puts into logic for level (and Tyrogue) evolutions

    For example, if you set this to 4 and have beaten 5 gyms, evolutions up to level 20 would be in logic.

    If Johto only is enabled the minimum for this setting is 8.
    """
    display_name = "Evolution Gym Levels"
    default = 8
    range_start = 4
    range_end = 69


class Shopsanity(Choice):
    """
    Adds Pokemart items as locations, items in Pokemarts are added to the item pool
    """
    display_name = "Shopsanity"
    default = 0
    option_off = 0
    option_johto = 1
    option_kanto = 2
    option_both = 3


class ShopsanityPrices(Choice):
    """
    Sets how shop item prices are determined when Shopsanity is enabled
    - Vanilla: Shop prices are unchanged
    - Item Price: Shop prices are determined by the value of the item being sold
    - Spheres: Shop prices are determined by sphere access
    - Classification: Shop prices are determined by item classifications (Progression, Useful, Filler/Trap)
    - Spheres and Classifications: Shop prices are determined by both sphere access and item classifications
    - Completely Random: Shop prices will be completely random
    """
    display_name = "Shopsanity Prices"
    default = 0
    option_vanilla = 0
    option_item_price = 1
    option_spheres = 2
    option_classification = 3
    option_spheres_and_classification = 4
    option_completely_random = 5


class MinimumShopsanityPrice(Range):
    """
    Sets the minimum cost of shop items when Shopsanity is enabled
    """
    display_name = "Minimum Shopsanity Price"
    default = 100
    range_start = 0
    range_end = 10000


class MaximumShopsanityPrice(Range):
    """
    Sets the maximum cost of shop items when Shopsanity is enabled
    """
    display_name = "Maximum Shopsanity Price"
    default = 3000
    range_start = 0
    range_end = 10000


class ProvideShopHints(Choice):
    """
    Sends out hints when a randomized shop is accessed
    """
    display_name = "Provide Shop Hints"
    default = 0
    option_off = 0
    option_progression = 1
    option_progression_and_useful = 2
    option_all = 3


class ShopsanityRestrictRareCandies(Toggle):
    """
    Makes Rare Candies in shops only purchasable once
    """


class RandomizePokegear(Toggle):
    """
    Shuffles the Pokegear and cards into the pool
    """
    display_name = "Randomize Pokegear"


class RandomizeBerryTrees(Toggle):
    """
    Shuffles berry tree locations into the pool
    """
    display_name = "Randomize Berry Trees"


class RandomizeFlyUnlocks(Choice):
    """
    Shuffles Fly destination unlocks into the pool

    Indigo Plateau is not included.
    """
    display_name = "Shuffle Fly Unlocks"
    default = 0
    option_off = 0
    option_on = 1
    option_exclude_silver_cave = 2


class RandomizeStarters(Choice):
    """
    Randomizes species of starter Pokemon
    """
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_unevolved_only = 1
    option_completely_random = 2
    option_first_stage_can_evolve = 3
    option_base_stat_mode = 4


class StarterBlocklist(OptionSet):
    """
    These Pokemon will not be chosen as starter Pokemon
    Does nothing if starter Pokemon are not randomized
    You can use "_Legendaries" as a shortcut for all legendary Pokemon
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Starter Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class StarterBST(NamedRange):
    """
    If you chose Base Stat Mode for your starters, what is the average base stat total you want your available starters to be?
    """
    display_name = "Starter BST Range"
    default = 310
    range_start = 195
    range_end = 680
    special_range_names = {
        "normal_starters": 310
    }


class RandomizeWilds(Choice):
    """
    Randomizes species of wild Pokemon

    Base Forms: Ensures that at least every Pokemon that cannot be obtained through evolution is available in the wild
    Evolution Lines: Ensures that at least one Pokemon from each evolutionary line can be obtained in the wild
    Catch 'em All: Ensures that every Pokemon will be obtainable in the wild
    """
    display_name = "Randomize Wilds"
    default = 0
    option_vanilla = 0
    option_completely_random = 1
    option_base_forms = 2
    option_evolution_lines = 3
    option_catch_em_all = 4


class WildEncounterBlocklist(OptionSet):
    """
    These Pokemon will not appear in the wild
    Does nothing if wild Pokemon are not randomized
    You can use "_Legendaries" as a shortcut for all legendary Pokemon
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Wild Encounter Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class EncounterGrouping(Choice):
    """
    Determines how randomized wild Pokemon are grouped in encounter tables.

    All Split: Each encounter area will have each slot randomized separately. For example, grass areas will have seven
        randomized encounter slots.
    One to One: Each encounter area will retain its vanilla slot grouping. For example, if an area has two encounters
        in vanilla, it will be randomized as two slots.
    One per Method: Each encounter method on a route will be treated as a single slot. For example, the grass on a route
     will contain only a single encounter. Each rod is a separate encounter.

    This setting has no effect if wild Pokemon are not randomized.
    """
    display_name = "Encounter Grouping"
    default = 0
    option_all_split = 0
    option_one_to_one = 1
    option_one_per_method = 2


class ForceFullyEvolved(NamedRange):
    """
    When an opponent uses a Pokemon of the specified level or higher, restricts the species to only fully evolved Pokemon.

    Only applies when trainer parties are randomized.
    """
    display_name = "Force Fully Evolved"
    range_start = 1
    range_end = 100
    default = 0
    special_range_names = {
        "disabled": 0
    }


class EncounterSlotDistribution(Choice):
    """
    Sets how the Pokemon encounter slots in an area are distributed.

    Remove 1%'s modifies grass/cave encounters to 30%/25%/20%/10%/5%/5%/5% and does not modify any others.
    Balanced sets the following:
        Grass/Cave: 20%/20%/15%/15%/10%/10%/10%
        Headbutt:  20%/20%/20%/15%/15%/10%
        Rock Smash: 70%/30%
        Fishing (vanilla):
            Old Rod: 70%/15%/15%
            Good Rod: 35%/35%/20%/10%
            Super Rod: 40%/30%/20%/10%
    Equal sets all encounter slots to have (almost) equal probability.
    """
    display_name = "Encounter Slot Distribution"
    default = 1
    option_vanilla = 0
    option_remove_one_percents = 1
    option_balanced = 2
    option_equal = 3


class RandomizeStaticPokemon(Toggle):
    """
    Randomizes species of static Pokemon encounters
    This includes overworld Pokemon, gift Pokemon and gift egg Pokemon
    """
    display_name = "Randomize Static Pokemon"


class StaticBlocklist(OptionSet):
    """
    These Pokemon will not appear as static overworld encounters, gift eggs or gift Pokemon
    Does nothing if static Pokemon are not randomized
    You can use "_Legendaries" as a shortcut for all legendary Pokemon
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Static Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class RandomizeTrades(Choice):
    """
    Randomizes species of in-game trades
    """
    display_name = "Randomize Trades"
    default = 0
    option_vanilla = 0
    option_received = 1
    option_requested = 2
    option_both = 3


class RandomizeTrainerParties(Choice):
    """
    Randomizes Pokemon in enemy trainer parties
    """
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_completely_random = 2


class TrainerPartyBlocklist(OptionSet):
    """
    These Pokemon will not appear in enemy trainer parties
    Does nothing if trainer parties are not randomized
    You can use "_Legendaries" as a shortcut for all legendary Pokemon
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Trainer Party Blocklist"
    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + ["_Legendaries"]


class LevelScaling(Choice):
    """
    Sets whether Trainer levels are scaled based on sphere access.

    - Off: Vanilla levels are used.
    - Spheres: Levels are scaled based on sphere access only.
    - Spheres and Distance: Levels are scaled based on both sphere access and distance from starting town.
    """
    display_name = "Level Scaling"
    default = 0
    option_off = 0
    option_spheres = 1
    option_spheres_and_distance = 2


class BoostTrainerPokemonLevels(Choice):
    """
    Boost levels of every trainer's Pokemon. There are 2 different boost modes:
    Percentage Boost: Increases every trainer Pokemon's level by the boost percentage.
    Set Min Level: Trainer Pokemon will be the specified level or higher.
    """
    display_name = "Boost Trainer Pokemon Levels"
    default = 0
    option_vanilla = 0
    option_percentage_boost = 1
    option_set_min_level = 2


class TrainerLevelBoostValue(Range):
    """
    This Value only works if Boost Trainer Pokemon Levels is being used.
    The meaning of this value depends on Trainer Boost Mode.

    Percentage Boost: This value represents the boost amount percentage
    Set Min Level: Trainer Pokemon will never be lower than this level
    """
    display_name = "Trainer Level Boost Value"
    default = 1
    range_start = 1
    range_end = 100


class RandomizeLearnsets(Choice):
    """
    Vanilla: Vanilla learnsets
    Randomize: Random learnsets
    Start With Four Moves: Random learnsets with 4 starting moves
    """
    display_name = "Randomize Learnsets"
    default = 0
    option_vanilla = 0
    option_randomize = 1
    option_start_with_four_moves = 2


class MetronomeOnly(Toggle):
    """
    Only Metronome is usable in battle, PP is infinite
    You can still teach HMs and useful TMs
    """
    display_name = "Metronome Only"


class LearnsetTypeBias(NamedRange):
    """
    This option will have an effect only if Randomize Learnset option is enabled.

    Percent chance of each move in a Pokemon's learnset to match its type.
    Default value is -1. This means there will be no check in logic for type matches.
    The lowest possible type matching value is 0. There will be no STAB moves in a Pokemon's learnset
    If set to 100 all moves that a Pokemon will learn by leveling up will match one of its types
    """
    display_name = "Move Learnset Type Bias"
    default = -1
    range_start = -1
    range_end = 100
    special_range_names = {
        "vanilla": -1
    }


class RandomizeMoveValues(Choice):
    """
    Restricted: Generates values based on vanilla move values
    Multiplies the power of each move with a random number between 0.5 and 1.5
    Adds or subtracts 0, 5 or 10 from original PP | Min 5, Max 40

    Full Exclude Accuracy: Fully randomizes move Power and PP
    Randomizes each move's Power [20-150], PP [5-40] linearly. All possible values have the same weight.
    Multi-hit moves have their power divided by their average hit count.

    Full: Previous + also randomizes accuracy.
    Accuracy has a flat chance of 70% to be 100%, if not it is linearly distributed between 30-100.
    Does not randomize accuracy of OHKO moves, status moves (e.g. Toxic) and unique damage moves (e.g. Seismic Toss)
    """
    display_name = "Randomize Move Values"
    default = 0
    option_vanilla = 0
    option_restricted = 1
    option_full_exclude_accuracy = 2
    option_full = 3


class RandomizeMoveTypes(Toggle):
    """
    Randomizes each move's Type
    """
    display_name = "Randomize Move Types"


class RandomizeTMMoves(Toggle):
    """
    Randomizes the moves available as TMs
    """
    display_name = "Randomize TM Moves"


class TMCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with each TM
    Headbutt and Rock Smash are considered HMs when applying compatibility
    """
    display_name = "TM Compatibility"
    default = -1
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "fully_compatible": 100
    }


class HMCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with each HM
    Headbutt and Rock Smash are considered HMs when applying compatibility

    Minimal compatibility will ensure only the minimum required number of Pokemon can learn each HM, usually one
    """
    display_name = "HM Compatibility"
    default = -1
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "minimal": 0,
        "fully_compatible": 100
    }


class HMPowerCap(NamedRange):
    """
    Lowers the power of damaging HM moves that exceed the set power down to match it.
    Headbutt and Rock Smash are considered HMs for this setting.
    """
    display_name = "HM Power Cap"
    default = 255
    range_start = 20
    range_end = 255
    special_range_names = {
        "none": range_end
    }


class RandomizeBaseStats(Choice):
    """
    Vanilla: Vanilla base stats
    Keep BST: Random base stats, but base stat total is preserved
    Completely Random: Base stats and BST are completely random
    """
    display_name = "Randomize Base Stats"
    default = 0
    option_vanilla = 0
    option_keep_bst = 1
    option_completely_random = 2


class RandomizeTypes(Choice):
    """
    Vanilla: Vanilla Pokemon types
    Follow Evolutions: Types are randomized but preserved when evolved
    Completely Random: Types are completely random
    """
    display_name = "Randomize Types"
    default = 0
    option_vanilla = 0
    option_follow_evolutions = 1
    option_completely_random = 2


class RandomizeEvolution(Choice):
    """
    Vanilla: Pokemon evolve into the same Pokemon they do in vanilla
    Match a Type: Pokemon evolve into a random Pokemon with a higher base stat total, that shares at least one type with it.
    """
    display_name = "Randomize Evolution"
    default = 0
    option_vanilla = 0
    option_match_a_type = 1


class RandomizePalettes(Choice):
    """
    Vanilla: Vanilla Pokemon color palettes
    Match Types: Color palettes match Pokemon Type
    Completely Random: Color palettes are completely random
    """
    display_name = "Randomize Palettes"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_completely_random = 2


class RandomizeMusic(Choice):
    """
    Randomize all music
    - Shuffle will map each music track to a new track
    - Completely Random will map each music area to a new track
    """
    display_name = "Randomize Music"
    default = 0
    option_off = 0
    option_shuffle = 1
    option_completely_random = 2


# class RandomizeSFX(Toggle):
#     """
#     Randomize all sound effects
#     """
#     display_name = "Randomize SFX"
#     default = 0


class FreeFlyLocation(Choice):
    """
    Free Fly: Unlocks a random Fly destination when Fly is obtained.
    Free Fly and Map Card: Additionally unlocks a random Fly destination after obtaining both the Pokegear and Map Card.
    Map Card: Unlocks a single random Fly destination only after obtaining both the Pokegear and Map card.

    Indigo Plateau cannot be chosen as a free Fly location.
    """
    display_name = "Free Fly Location"
    default = 0
    option_off = 0
    option_free_fly = 1
    option_free_fly_and_map_card = 2
    option_map_card = 3


class EarlyFly(Toggle):
    """
    HM02 Fly will be placed early in the game
    If this option is enabled, you will be able to Fly before being forced to use an item to progress
    Early Fly is a best effort setting, if Fly and its badge cannot be placed early, then they will be placed
        randomly
    """
    display_name = "Early Fly"


class HMBadgeRequirements(Choice):
    """
    Vanilla: HMs require their vanilla badges
    No Badges: HMs do not require a badge to use
    Add Kanto: HMs can be used with the Johto or Kanto badge
    Regional: HMs can be used in Johto with the Johto badge or in Kanto with the Kanto badge
        This does not apply to Fly which will accept either badge
        Routes 26, 27, 28 and Tohjo Falls are in Johto for HM purposes
    """
    display_name = "HM Badge Requirements"
    default = 0
    option_vanilla = 0
    option_no_badges = 1
    option_add_kanto = 2
    option_regional = 3


class RemoveBadgeRequirement(OptionSet):
    """
    Specify which HMs do not require a badge to use. This overrides the HM Badge Requirements setting.

    HMs should be provided in the form: "Fly".
    """
    display_name = "Remove Badge Requirement"
    valid_keys = ["Cut", "Fly", "Surf", "Strength", "Flash", "Whirlpool", "Waterfall"]


class RemoveIlexCutTree(DefaultOnToggle):
    """
    Removes the Cut tree in Ilex Forest
    """
    display_name = "Remove Ilex Forest Cut Tree"


class SaffronGatehouseTea(OptionSet):
    """
    Sets which Saffron City gatehouses require Tea to pass. Obtaining the Tea will unlock them all.
    If any gatehouses are enabled, adds a new location in Celadon Mansion 1F and adds Tea to the item pool.
    Valid options are: North, East, South, West, and _Random in any combination.
    _Random gives each gate that is not already included a 50% chance to be included.
    """
    display_name = "Saffron Gatehouse Tea"
    valid_keys = ["North", "East", "South", "West", "_Random"]


class EastWestUnderground(Toggle):
    """
    Adds an Underground Pass between Route 7 and Route 8 in Kanto.
    """
    display_name = "East - West Underground"


class UndergroundsRequirePower(Choice):
    """
    Specifies which of the Kanto Underground Passes require the Machine Part to be returned to access.
    """
    display_name = "Undergrounds Require Power"
    default = 0
    option_both = 0
    option_north_south = 1
    option_east_west = 2
    option_neither = 3


class ReusableTMs(Toggle):
    """
    TMs can be used an infinite number of times
    """
    display_name = "Reusable TMs"


class MinimumCatchRate(Range):
    """
    Sets a minimum catch rate for wild Pokemon
    """
    display_name = "Minimum Catch Rate"
    default = 0
    range_start = 0
    range_end = 255


class SkipEliteFour(Toggle):
    """
    Go straight to Lance when challenging the Elite Four
    """
    display_name = "Skip Elite Four"


class BetterMarts(Toggle):
    """
    Improves the selection of items at Pokemarts
    """
    display_name = "Better Marts"


class ExpModifier(NamedRange):
    """
    Scale the amount of Experience Points given in battle
    Default is 20, for double set to 40, for half set to 10, etc
    """
    display_name = "Experience Modifier"
    default = 20
    range_start = 1
    range_end = 255
    special_range_names = {
        "half": default // 2,
        "normal": default,
        "double": default * 2,
        "triple": default * 3,
        "quadruple": default * 4,
        "quintuple": default * 5,
        "sextuple": default * 6,
        "septuple": default * 7,
        "octuple": default * 8,
    }


class StartingMoney(NamedRange):
    """
    Sets your starting money.
    """
    display_name = "Starting Money"
    default = 3000
    range_start = 0
    range_end = 999999
    special_range_names = {
        "vanilla": 3000
    }


class AllPokemonSeen(Toggle):
    """
    Start will all Pokemon seen in your Pokedex.
    This allows you to see where the Pokemon can be encountered in the wild.
    """
    display_name = "All Pokemon Seen"


class PhoneTrapWeight(Range):
    """
    Adds random Pokegear calls that acts as traps
    Weight is the percentage chance each filler item is replaced with a trap
    """
    display_name = "Phone Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class SleepTrapWeight(Range):
    """
    Trap that causes Sleep status on your party
    Weight is the percentage chance each filler item is replaced with a trap
    """
    display_name = "Sleep Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class PoisonTrapWeight(Range):
    """
    Trap that causes Poison status on your party
    Weight is the percentage chance each filler item is replaced with a trap
    """
    display_name = "Poison Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class BurnTrapWeight(Range):
    """
    Trap that causes Burn status on your party
    Weight is the percentage chance each filler item is replaced with a trap
    """
    display_name = "Burn Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class FreezeTrapWeight(Range):
    """
    Trap that causes Freeze status on your party
    Weight is the percentage chance each filler item is replaced with a trap
    """
    display_name = "Freeze Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class ParalysisTrapWeight(Range):
    """
    Trap that causes Paralysis status on your party
    Weight is the percentage chance each filler item is replaced with a trap
    """
    display_name = "Paralysis Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class EnableMischief(Toggle):
    """
    If I told you what this does, it would ruin the surprises :)
    """
    display_name = "Enable Mischief"


class MoveBlocklist(OptionSet):
    """
    Pokemon won't learn these moves via learnsets and no TM will contain them.
    Moves should be provided in the form: "Ice Beam"
    Does not apply to vanilla learnsets or vanilla TMs
    """
    display_name = "Move Blocklist"
    valid_keys = sorted(move.replace("_", " ").title() for move in data.moves.keys())


class FlyLocationBlocklist(OptionSet):
    """
    These locations won't be given to you as fly locations, either as your free one or from receiving the map card.
    Locations should be provided in the form: "Ecruteak City"
    Indigo Plateau cannot be chosen as a free fly location and is not a valid option
    If you blocklist enough locations that there aren't enough locations left for your total number of free fly locations, the blocklist will simply do nothing
    "_Johto" and "_Kanto" are shortcuts for all Johto and Kanto towns respectively
    """
    display_name = "Fly Location Blocklist"
    valid_keys = [region.name for region in data.fly_regions] + ["_Johto", "_Kanto"]


class RemoteItems(Toggle):
    """
    Instead of placing your own items directly into the ROM, all items are received from the server, including items you find for yourself.
    This enables co-op of a single slot and recovering more items after a lost save file (if you're so unlucky).
    But it changes pickup behavior slightly and requires connection to the server to receive any items.
    """
    display_name = "Remote Items"


class GameOptions(OptionDict):
    """
    Presets in-game options. These can be changed in-game later. Any omitted options will use their default.

    Allowed options and values, with default first:

    ap_item_sound: on/off - Sets whether a sound is played when a remote item is received
    auto_run: off/on - Sets whether run activates automatically, if on you can hold B to walk
    battle_animations: all/no_scene/no_bars/speedy - Sets which battle animations are played:
        all: All animations play, including entry and moves
        no_scene: Entry and move animations do not play
        no_bars: Entry, move and HP/EXP bar animations do not play
        speedy: No battle animations play and many delays are removed to make battles faster
    battle_move_stats: off/on - Sets whether or not to display power and accuracy of moves in battle
    battle_shift: shift/set - Sets whether you are asked to switch between trainer Pokemon
    bike_music: on/off - Sets whether the bike music will play
    blind_trainers: off/on - Sets whether trainers will see you without talking to them directly
    catch_exp: off/on - Sets whether or not you get EXP for catching a Pokemon
    dex_area_beep: off/on - Sets whether the Pokedex beeps for land and Surf encounters in the current area
    exp_distribution: gen2/gen6/gen8/no_exp - Sets the EXP distribution method:
        gen2: EXP is split evenly among battle participants, EXP Share splits evenly between participants and non-participants
        gen6: Participants earn 100% of EXP, non-participants earn 50% of EXP when EXP Share is enabled
        gen8: Participants earn 100% of EXP, non-participants earn 100% of EXP when EXP Share is enabled
        no_exp: EXP is disabled
    fast_egg_hatch: off/on - Sets whether eggs take a single cycle to hatch
    fast_egg_make: off/on - Sets whether eggs are guaranteed after one cycle at the day care
    guaranteed_catch: off/on - Sets whether balls have a 100% success rate
    low_hp_beep: on/off - Sets whether the low HP beep is played in battle
    menu_account: on/off - Sets whether your start menu selection is remembered
    poison_flicker: on/off - Sets whether the overworld poison flash effect is played
    rods_always_work: off/on - Sets whether the fishing rods always succeed
    short_fanfares: off/on - Sets whether item receive fanfares are shortened
    skip_dex_registration: off/on - Sets whether the Pokedex registration screen is skipped
    skip_nicknames: off/on - Sets whether you are asked to nickname a Pokemon upon receiving it
    sound: mono/stereo - Sets the sound mode
    spinners: normal/rotators - Sets whether trainers with random spin are turned into consistent rotators
    surf_music: on/off - Sets whether the surf music will play
    text_frame: 1-8 - Sets the textbox frame, "random" will pick a random frame
    text_speed: mid/slow/fast/instant - Sets the speed at which text advances
    time_of_day: auto/morn/day/nite - Sets a time of day override, auto follows the clock, "random" will pick a random time
    turbo_button: none/a/b/a_or_b - Sets which buttons auto advance text when held
    """
    display_name = "Game Options"
    default = {
        "text_speed": "mid",
        "battle_shift": "shift",
        "battle_animations": "all",
        "sound": "mono",
        "menu_account": "on",
        "text_frame": 1,
        "bike_music": "on",
        "surf_music": "on",
        "skip_nicknames": "off",
        "auto_run": "off",
        "spinners": "normal",
        "fast_egg_hatch": "off",
        "fast_egg_make": "off",
        "rods_always_work": "off",
        "exp_distribution": "gen2",
        "catch_exp": "off",
        "poison_flicker": "on",
        "turbo_button": "none",
        "low_hp_beep": "on",
        "time_of_day": "auto",
        "battle_move_stats": "off",
        "short_fanfares": "off",
        "dex_area_beep": "off",
        "skip_dex_registration": "off",
        "blind_trainers": "off",
        "guaranteed_catch": "off",
        "ap_item_sound": "on"
    }


class PokemonCrystalDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n\n    In Pokemon Crystal, whiting out sends a death and receiving a death causes you to white out."


@dataclass
class PokemonCrystalOptions(PerGameCommonOptions):
    goal: Goal
    johto_only: JohtoOnly
    elite_four_requirement: EliteFourRequirement
    elite_four_count: EliteFourCount
    red_requirement: RedRequirement
    red_count: RedCount
    mt_silver_requirement: MtSilverRequirement
    mt_silver_count: MtSilverCount
    radio_tower_requirement: RadioTowerRequirement
    radio_tower_count: RadioTowerCount
    route_44_access_requirement: Route44AccessRequirement
    route_44_access_count: Route44AccessCount
    vanilla_clair: VanillaClair
    randomize_starting_town: RandomizeStartingTown
    starting_town_blocklist: StartingTownBlocklist
    randomize_badges: RandomizeBadges
    randomize_hidden_items: RandomizeHiddenItems
    require_itemfinder: RequireItemfinder
    route_32_condition: Route32Condition
    kanto_access_requirement: KantoAccessRequirement
    kanto_access_count: KantoAccessCount
    red_gyarados_access: RedGyaradosAccess
    route_2_access: Route2Access
    route_3_access: Route3Access
    blackthorn_dark_cave_access: BlackthornDarkCaveAccess
    national_park_access: NationalParkAccess
    mount_mortar_access: MountMortarAccess
    trainersanity: Trainersanity
    trainersanity_alerts: TrainersanityAlerts
    rematchsanity: Rematchsanity
    randomize_wilds: RandomizeWilds
    dexsanity: Dexsanity
    dexsanity_starters: DexsanityStarters
    dexcountsanity: Dexcountsanity
    dexcountsanity_step: DexcountsanityStep
    dexcountsanity_leniency: DexcountsanityLeniency
    wild_encounter_methods_required: WildEncounterMethodsRequired
    enforce_wild_encounter_methods_logic: EnforceWildEncounterMethodsLogic
    static_pokemon_required: StaticPokemonRequired
    evolution_methods_required: EvolutionMethodsRequired
    evolution_gym_levels: EvolutionGymLevels
    breeding_methods_required: BreedingMethodsRequired
    shopsanity: Shopsanity
    shopsanity_prices: ShopsanityPrices
    shopsanity_minimum_price: MinimumShopsanityPrice
    shopsanity_maximum_price: MaximumShopsanityPrice
    provide_shop_hints: ProvideShopHints
    shopsanity_restrict_rare_candies: ShopsanityRestrictRareCandies
    randomize_pokegear: RandomizePokegear
    randomize_berry_trees: RandomizeBerryTrees
    randomize_fly_unlocks: RandomizeFlyUnlocks
    randomize_starters: RandomizeStarters
    starter_blocklist: StarterBlocklist
    starters_bst_average: StarterBST
    wild_encounter_blocklist: WildEncounterBlocklist
    encounter_grouping: EncounterGrouping
    force_fully_evolved: ForceFullyEvolved
    encounter_slot_distribution: EncounterSlotDistribution
    randomize_static_pokemon: RandomizeStaticPokemon
    static_blocklist: StaticBlocklist
    level_scaling: LevelScaling
    randomize_trades: RandomizeTrades
    randomize_trainer_parties: RandomizeTrainerParties
    trainer_party_blocklist: TrainerPartyBlocklist
    boost_trainers: BoostTrainerPokemonLevels
    trainer_level_boost: TrainerLevelBoostValue
    randomize_learnsets: RandomizeLearnsets
    metronome_only: MetronomeOnly
    learnset_type_bias: LearnsetTypeBias
    randomize_move_values: RandomizeMoveValues
    randomize_move_types: RandomizeMoveTypes
    randomize_tm_moves: RandomizeTMMoves
    tm_compatibility: TMCompatibility
    hm_compatibility: HMCompatibility
    hm_power_cap: HMPowerCap
    randomize_base_stats: RandomizeBaseStats
    randomize_types: RandomizeTypes
    randomize_evolution: RandomizeEvolution
    randomize_palettes: RandomizePalettes
    randomize_music: RandomizeMusic
    # randomize_sfx: RandomizeSFX
    move_blocklist: MoveBlocklist
    free_fly_location: FreeFlyLocation
    free_fly_blocklist: FlyLocationBlocklist
    early_fly: EarlyFly
    hm_badge_requirements: HMBadgeRequirements
    remove_badge_requirement: RemoveBadgeRequirement
    remove_ilex_cut_tree: RemoveIlexCutTree
    saffron_gatehouse_tea: SaffronGatehouseTea
    east_west_underground: EastWestUnderground
    undergrounds_require_power: UndergroundsRequirePower
    reusable_tms: ReusableTMs
    minimum_catch_rate: MinimumCatchRate
    skip_elite_four: SkipEliteFour
    better_marts: BetterMarts
    experience_modifier: ExpModifier
    starting_money: StartingMoney
    all_pokemon_seen: AllPokemonSeen
    phone_trap_weight: PhoneTrapWeight
    sleep_trap_weight: SleepTrapWeight
    poison_trap_weight: PoisonTrapWeight
    burn_trap_weight: BurnTrapWeight
    freeze_trap_weight: FreezeTrapWeight
    paralysis_trap_weight: ParalysisTrapWeight
    remote_items: RemoteItems
    game_options: GameOptions
    enable_mischief: EnableMischief
    start_inventory_from_pool: StartInventoryPool
    death_link: PokemonCrystalDeathLink


OPTION_GROUPS = [
    OptionGroup(
        "Map",
        [RandomizeStartingTown,
         StartingTownBlocklist,
         JohtoOnly]
    ),
    OptionGroup(
        "Roadblocks",
        [EliteFourRequirement, EliteFourCount,
         RedRequirement, RedCount,
         MtSilverRequirement, MtSilverCount,
         RadioTowerRequirement, RadioTowerCount,
         Route44AccessRequirement, Route44AccessCount,
         KantoAccessRequirement, KantoAccessCount,
         Route32Condition,
         Route2Access,
         Route3Access,
         MountMortarAccess,
         RedGyaradosAccess,
         BlackthornDarkCaveAccess,
         NationalParkAccess,
         SaffronGatehouseTea,
         RemoveIlexCutTree,
         UndergroundsRequirePower,
         EastWestUnderground,
         VanillaClair]
    ),
    OptionGroup(
        "Items",
        [RandomizeBadges,
         RandomizePokegear,
         RandomizeHiddenItems,
         RandomizeBerryTrees,
         RandomizeFlyUnlocks,
         RequireItemfinder,
         RemoteItems]
    ),
    OptionGroup(
        "Shopsanity",
        [Shopsanity,
         ShopsanityPrices,
         MinimumShopsanityPrice,
         MaximumShopsanityPrice,
         ProvideShopHints,
         ShopsanityRestrictRareCandies]
    ),
    OptionGroup(
        "HMs",
        [HMCompatibility,
         HMBadgeRequirements,
         RemoveBadgeRequirement,
         FreeFlyLocation,
         FlyLocationBlocklist,
         EarlyFly]
    ),
    OptionGroup(
        "Pokemon",
        [RandomizeWilds,
         WildEncounterBlocklist,
         RandomizeStaticPokemon,
         StaticBlocklist,
         RandomizeBaseStats,
         RandomizeTypes,
         RandomizeEvolution,
         RandomizeTrades,
         EncounterGrouping,
         EncounterSlotDistribution]
    ),
    OptionGroup(
        "Starters",
        [RandomizeStarters,
         StarterBST,
         StarterBlocklist]
    ),
    OptionGroup(
        "Moves",
        [RandomizeLearnsets,
         LearnsetTypeBias,
         MetronomeOnly,
         RandomizeMoveTypes,
         RandomizeMoveValues,
         HMPowerCap,
         RandomizeTMMoves,
         TMCompatibility,
         ReusableTMs,
         MoveBlocklist]
    ),
    OptionGroup(
        "Trainers",
        [RandomizeTrainerParties,
         TrainerPartyBlocklist,
         BoostTrainerPokemonLevels,
         TrainerLevelBoostValue,
         ForceFullyEvolved]
    ),
    OptionGroup(
        "Dexsanities",
        [Dexsanity,
         Dexcountsanity,
         DexcountsanityStep,
         DexcountsanityLeniency,
         DexsanityStarters]
    ),
    OptionGroup(
        "Trainersanity",
        [Trainersanity,
         TrainersanityAlerts]
    ),
    OptionGroup(
        "Pokemon Logic",
        [WildEncounterMethodsRequired,
         EnforceWildEncounterMethodsLogic,
         StaticPokemonRequired,
         EvolutionMethodsRequired,
         EvolutionGymLevels,
         BreedingMethodsRequired]
    ),
    OptionGroup(
        "Traps",
        [PhoneTrapWeight,
         SleepTrapWeight,
         PoisonTrapWeight,
         BurnTrapWeight,
         FreezeTrapWeight,
         ParalysisTrapWeight]
    ),
    OptionGroup(
        "Quality of Life",
        [GameOptions,
         LevelScaling,
         AllPokemonSeen,
         StartingMoney,
         BetterMarts,
         ExpModifier,
         SkipEliteFour,
         MinimumCatchRate,
         PokemonCrystalDeathLink]
    ),
    OptionGroup(
        "Cosmetic",
        [RandomizePalettes,
         RandomizeMusic]
    ),
    OptionGroup(
        ":3",
        [EnableMischief],
        False
    )
]
