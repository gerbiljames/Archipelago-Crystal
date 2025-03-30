from dataclasses import dataclass

from Options import Toggle, Choice, DefaultOnToggle, Range, PerGameCommonOptions, NamedRange, OptionSet, \
    StartInventoryPool
from .data import data


class Goal(Choice):
    """
    Elite Four: collect 8 badges and enter the Hall of Fame
    Red: collect 16 badges and defeat Red at Mt. Silver
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


class EliteFourBadges(Range):
    """
    Number of badges required to enter Victory Road
    """
    display_name = "Elite Four Badges"
    default = 8
    range_start = 1
    range_end = 16


class RedBadges(Range):
    """
    Number of badges required to battle Red
    """
    display_name = "Red Badges"
    default = 16
    range_start = 1
    range_end = 16


class MtSilverBadges(Range):
    """
    Number of badges required to access Mt. Silver and Silver Cave
    """
    display_name = "Mt. Silver Badges"
    default = 16
    range_start = 1
    range_end = 16


class RadioTowerBadges(Range):
    """
    Number of badges at which Team Rocket takes over the Goldenrod Radio Tower
    """
    display_name = "Radio Tower Badges"
    default = 7
    range_start = 1
    range_end = 16


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


class RequireItemfinder(DefaultOnToggle):
    """
    Hidden items require Itemfinder in logic
    """
    display_name = "Require Itemfinder"


class Route32Condition(Choice):
    """
    Sets the condition required to pass into the south part of Route 32
    Egg from aide: Collect the Egg from the aide in the Violet City Pokemon Center after beating Falkner
    Any badge: Obtain any badge
    None: No requirement
    """
    display_name = "Route 32 Access Condition"
    default = 0
    option_egg_from_aide = 0
    option_any_badge = 1
    option_none = 2


class Trainersanity(Toggle):
    """
    Adds checks for defeating trainers
    """
    display_name = "Trainersanity"


class TrainersanityAlerts(Choice):
    """
    Shows a message box or plays a sound for Trainersanity checks
    """
    display_name = "Trainersanity Alerts"
    default = 1
    option_no_alerts = 0
    option_message_box = 1
    option_sound_only = 2


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


class RandomizeWilds(Toggle):
    """
    Randomizes species of wild Pokemon
    """
    display_name = "Randomize Wilds"


class ForceFullyEvolved(Range):
    """
    When an opponent uses a Pokemon of the specified level or higher, restricts the species to only fully evolved Pokemon.

    Only applies when trainer parties are randomized.
    """
    display_name = "Force Fully Evolved"
    range_start = 1
    range_end = 100
    default = 100


class NormalizeEncounterRates(Toggle):
    """
    Normalizes the chance of encountering each wild Pokemon in a given area
    """
    display_name = "Normalize Encounter Rates"


class RandomizeStaticPokemon(Toggle):
    """
    Randomizes species of static Pokemon encounters
    """
    display_name = "Randomize Static Pokemon"


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


class LearnsetTypeBias(NamedRange):
    """
    This option will have an effect only if Randomize Learnset option is ENABLED.

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
    Percent chance for Pokemon to be compatible with a TM
    """
    display_name = "TM Compatibility"
    default = 0
    range_start = 1
    range_end = 100
    special_range_names = {
        "vanilla": 0,
        "fully_compatible": 100
    }


class HMCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with a HM
    """
    display_name = "HM Compatibility"
    default = 0
    range_start = 50
    range_end = 100
    special_range_names = {
        "vanilla": 0,
        "fully_compatible": 100
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


class RandomizeMusic(Toggle):
    """
    Randomize all music
    """
    display_name = "Randomize Music"


# class RandomizeSFX(Toggle):
#     """
#     Randomize all sound effects
#     """
#     display_name = "Randomize SFX"
#     default = 0


class FreeFlyLocation(Choice):
    """
    If enabled, unlocks a random fly location for free
    If Free Fly and Map Card is selected, an extra fly location
    is unlocked when the Pokegear and Map Card are obtained
    """
    display_name = "Free Fly Location"
    default = 0
    option_off = 0
    option_free_fly = 1
    option_free_fly_and_map_card = 2


class EarlyFly(Toggle):
    """
    HM02 Fly will be placed early in the game
    If this option is enabled, you will be able to Fly before being forced to use an item to progress
    """
    display_name = "Early Fly"


class HMBadgeRequirements(Choice):
    """
    Vanilla: HMs require their vanilla badges
    No Badges: HMs do not require a badge to use
    Add Kanto: HMs can be used with the Johto or Kanto badge
    """
    display_name = "HM Badge Requirements"
    default = 0
    option_vanilla = 0
    option_no_badges = 1
    option_add_kanto = 2


class RemoveBadgeRequirement(OptionSet):
    """
    Specify which HMs do not require a badge to use. This overrides the HM Badge Requirements setting.
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
    Valid options are: North, East, South and West in any combination.
    """
    display_name = "Saffron Gatehouse Tea"
    valid_keys = ["North", "East", "South", "West"]


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


class GuaranteedCatch(Toggle):
    """
    Balls have a 100% success rate
    """
    display_name = "Guaranteed Catch"


class MinimumCatchRate(Range):
    """
    Sets a minimum catch rate for wild Pokemon
    """
    display_name = "Minimum Catch Rate"
    default = 0
    range_start = 0
    range_end = 255


class BlindTrainers(Toggle):
    """
    Trainers have no vision and will not start battles unless interacted with
    """
    display_name = "Blind Trainers"


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


class PhoneTrapWeight(Range):
    """
    Adds random Pokegear calls that acts as traps
    Weight is a percentage of filler items to replace
    """
    display_name = "Phone Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class SleepTrapWeight(Range):
    """
    Trap that causes Sleep status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Sleep Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class PoisonTrapWeight(Range):
    """
    Trap that causes Poison status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Poison Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class BurnTrapWeight(Range):
    """
    Trap that causes Burn status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Burn Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class FreezeTrapWeight(Range):
    """
    Trap that causes Freeze status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Freeze Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class ParalysisTrapWeight(Range):
    """
    Trap that causes Paralysis status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Paralysis Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class ItemReceiveSound(DefaultOnToggle):
    """
    Play item received sound on receiving a remote item
    All items will be considered remote when Remote Items is enabled
    """
    display_name = "Item Receive Sound"


class EnableMischief(Toggle):
    """
    If I told you what this does, it would ruin the surprises :)
    """
    display_name = "Enable Mischief"


class MoveBlocklist(OptionSet):
    """
    Pokemon won't learn these moves via learnsets or TM's.
    Moves should be provided in the form: ICE_BEAM
    """
    display_name = "Move Blocklist"
    valid_keys = sorted(set(data.moves.keys()))


class FlyLocationBlocklist(OptionSet):
    """
    These locations won't be given to you as fly locations either as your free one or from receiving the map card.
    Locations should be provided in the format "Ecruteak City"
    New Bark Town, Cherrygrove City and Indigo Plateau cannot be chosen as free fly locations and are not valid options
    If you blocklist enough locations that there aren't enough locations left for your total number of free fly locations, the blocklist will simply do nothing
    """
    display_name = "Fly Location Blocklist"
    valid_keys = [region.name for region in data.fly_regions]


class RemoteItems(Toggle):
    """
    Instead of placing your own items directly into the ROM, all items are received from the server, including items you find for yourself.
    This enables co-op of a single slot and recovering more items after a lost save file (if you're so unlucky).
    But it changes pickup behavior slightly and requires connection to the server to receive any items.
    """
    display_name = "Remote Items"


@dataclass
class PokemonCrystalOptions(PerGameCommonOptions):
    goal: Goal
    johto_only: JohtoOnly
    elite_four_badges: EliteFourBadges
    red_badges: RedBadges
    mt_silver_badges: MtSilverBadges
    radio_tower_badges: RadioTowerBadges
    randomize_badges: RandomizeBadges
    randomize_hidden_items: RandomizeHiddenItems
    require_itemfinder: RequireItemfinder
    route_32_condition: Route32Condition
    trainersanity: Trainersanity
    trainersanity_alerts: TrainersanityAlerts
    randomize_pokegear: RandomizePokegear
    randomize_berry_trees: RandomizeBerryTrees
    randomize_starters: RandomizeStarters
    starters_bst_average: StarterBST
    randomize_wilds: RandomizeWilds
    force_fully_evolved: ForceFullyEvolved
    normalize_encounter_rates: NormalizeEncounterRates
    randomize_static_pokemon: RandomizeStaticPokemon
    level_scaling: LevelScaling
    randomize_trades: RandomizeTrades
    randomize_trainer_parties: RandomizeTrainerParties
    boost_trainers: BoostTrainerPokemonLevels
    trainer_level_boost: TrainerLevelBoostValue
    randomize_learnsets: RandomizeLearnsets
    learnset_type_bias: LearnsetTypeBias
    randomize_move_values: RandomizeMoveValues
    randomize_move_types: RandomizeMoveTypes
    randomize_tm_moves: RandomizeTMMoves
    tm_compatibility: TMCompatibility
    hm_compatibility: HMCompatibility
    randomize_base_stats: RandomizeBaseStats
    randomize_types: RandomizeTypes
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
    guaranteed_catch: GuaranteedCatch
    minimum_catch_rate: MinimumCatchRate
    blind_trainers: BlindTrainers
    skip_elite_four: SkipEliteFour
    better_marts: BetterMarts
    experience_modifier: ExpModifier
    phone_trap_weight: PhoneTrapWeight
    sleep_trap_weight: SleepTrapWeight
    poison_trap_weight: PoisonTrapWeight
    burn_trap_weight: BurnTrapWeight
    freeze_trap_weight: FreezeTrapWeight
    paralysis_trap_weight: ParalysisTrapWeight
    remote_items: RemoteItems
    item_receive_sound: ItemReceiveSound
    enable_mischief: EnableMischief
    start_inventory_from_pool: StartInventoryPool
