from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, OptionGroup, OptionSet, PerGameCommonOptions, Range, Toggle

class Goal(Choice):
    """
    Specify the goal for your game.

    - **70K**: Beat the base game.
    - **140K**: Win Double or Nothing mode after doubling your earnings.
    - **1000K**: Cash out a minimum of $1,000,000 in Double or Nothing mode.
    - **Custom**: Cash out a mininum of a specified amount of money in Double or Nothing mode.
    """
    display_name = "Goal"
    option_70k = 0
    option_140k = 1
    option_1000k = 2
    option_custom = 3
    default = 1

class CustomGoalAmount(Range):
    """
    If Goal is set to Custom, specify the minimum amount of money needed to be cashed out.
    """
    display_name = "Custom Goal Amount"
    range_start = 1
    range_end = 100000000
    default = 1000000

class DoubleOrNothingRequirements(Choice):
    """
    Specify the requirements to unlock Double or Nothing mode

    - **Free**: Double or Nothing is unlocked from the start.
    - **Vanilla**: Double or Nothing is unlocked after beating the base game.
    - **Pills**: Double or Nothing is unlocked after obtaining the Double or Nothing Pills item in the multiworld.
    - **Vanilla Plus**: Double or Nothing is unlocked after beating the base game and finding the pills.
    """
    display_name = "Double or Nothing Requirements"
    option_free = 0
    option_vanilla = 1
    option_pills = 2
    option_vanilla_plus = 3
    default = 1

class ConsumableItemLogic(Choice):
    """
    Specify how consumable items affect the logic for your game. In solo worlds, this only has a noticeable effect
    when Goal is 1000K or Custom (with a sufficiently large goal amount).

    - **Tight**:
        Two consumable items are expected before beating the 2nd round of the base game.
        Three consumable items are expected before beating the 3rd round of the base game.
        An additional item is expected for every round of Double or Nothing.
            (e.g. The 140K goal will logically expect obtaining every consumable item before goaling)

    - **Normal**:
        One consumable item is expected before beating the 2nd round of the base game.
        Two consumable items are expected before beating the 3rd round of the base game.
        An additional item is expected for every 3 rounds of Double or Nothing.
            (e.g. The 140K goal will logically expect obtaining 4 consumable items before goaling,
                  The 1000K goal will logically expect obtaining every consumable item before goaling)

    - **Minimal**:
        No consumable items are expected before beating the base game.
        An additional item is expected for every 3 rounds of Double or Nothing.
            (e.g. The 140K goal will logically expect obtaining 2 consumable items before goaling,
                  The 1000K goal will logically expect obtaining 7 consumable items before goaling)

    - **None**: Consumable items are not considered logically required for goal
        (except for obtaining certain achievements).
    """
    display_name = "Consumable Item Logic"
    option_tight = 0
    option_normal = 1
    option_minimal = 2
    option_none = 3
    default = 1

class IncludedCustomMechanics(OptionSet):
    """
    Specify which custom mechanics are added to the game.
    
    **Item Luck**: Adds 3 items to the pool named "Progressive Item Luck". For each progressive item luck you
    obtain, the likelihood of failing to pull an item decreases.

    **Life Bank**: Adds a life bank to the game, accessible by clicking the icon on the top right of the UI.
    You gain life bank charges by finding items called "Life Bank Charge" spread throughout the multiworld.
    Spend a charge from your life bank any time during your turn to restore a charge during the round. Your
    charges are given back to you on a new run.
    """
    display_name = "Included Custom Mechanics"
    valid_keys = ["Item Luck", "Life Bank"]
    default = frozenset({"Item Luck", "Life Bank"})

class IncludedTraps(OptionSet):
    """
    Specify which traps are added to the game.
    
    **Stolen Package Trap**: Your box will be empty the next time you draw items.

    **Schrodinger's Bullet Trap**: The current shell is randomized the next time you
    pick up the shotgun.
    """
    display_name = "Included Traps"
    valid_keys = ["Stolen Package Trap", "Schrodinger's Bullet Trap"]
    default = frozenset({"Stolen Package Trap", "Schrodinger's Bullet Trap"})

class TrapFillPercentage(Range):
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 10

class Achievements(DefaultOnToggle):
    """
    Specify whether achievements are added as locations to your game.
    """
    display_name = "Achivements"

class ExcludeFullHouse(DefaultOnToggle):
    """
    Specify whether the Full House achivement should be excluded from the location list.
    """
    display_name = "Exclude Full House"

class Shotsanity(Choice):
    """
    Shotsanity adds locations for every successful live and blank shot up to a specified amount.
 
    - **Off**:
        Shotsanity is disabled.
    - **Balanced**:
        Shotsanity is enabled. Consumable item logic also applies to shotsanity locations.
    - **Unreasonable**:
        Shotsanity is enabled. No logic applies to shotsanity locations.
    """
    display_name = "Shotsanity"
    option_off = 0
    option_balanced = 1
    option_unreasonable = 2
    default = 0

class ShotsanityCount(Range):
    """
    If Shotsanity is enabled, specify the number of locations to add for each successful shot.
    """
    display_name = "Shotsanity Count"
    range_start = 1
    range_end = 1000
    default = 50

class BalancedShotsanityCountPerRound(Range):
    """
    If Shotsanity is set to Balanced, specify the number of shot locations in logic during each round,
    starting from the second round of the base game.
        (e.g. If this setting is set to 10:
            - Shotsanity Locations beyond 10 expect Base Game Second Round
            - Shotsanity Locations beyond 20 expect Base Game Final Round
            - Shotsanity Locations beyond 30 expect Double or Nothing - 1 Round
            and so on...
        )

    No matter what value is set, all shotsanity locations will be in logic after beating the penultimate round before
    your goal.
        - If your goal is 70K, all shotsanity locations are in logic after Base Game Second Round.
        - If your goal is 140K, all shotsanity locations are in logic after Double or Nothing - 5 Rounds.
        - If your goal is 1000K, all shotsanity locations are in logic after Double or Nothing - 14 Rounds.

    You are **NOT** restricted from obtaining shotsanity locations out of logic.
    """
    display_name = "Balanced Shotsanity Live Count Per Round"
    range_start = 1
    range_end = 1000
    default = 5

@dataclass
class BuckshotRouletteOptions(PerGameCommonOptions):
    goal: Goal
    custom_goal_amount: CustomGoalAmount
    double_or_nothing_requirements: DoubleOrNothingRequirements
    consumable_item_logic: ConsumableItemLogic
    included_custom_mechanics: IncludedCustomMechanics
    included_traps: IncludedTraps
    trap_fill_percentage: TrapFillPercentage
    achievements: Achievements
    exclude_full_house: ExcludeFullHouse
    shotsanity: Shotsanity
    shotsanity_count: ShotsanityCount
    balanced_shotsanity_count_per_round: BalancedShotsanityCountPerRound

option_groups = [
    OptionGroup("Goal", [
        Goal,
        CustomGoalAmount,
        DoubleOrNothingRequirements
    ]),
    OptionGroup("Difficulty", [
        ConsumableItemLogic,
        IncludedCustomMechanics,
        IncludedTraps,
        TrapFillPercentage
    ]),
    OptionGroup("Achievements", [
        Achievements,
        ExcludeFullHouse
    ]),
    OptionGroup("Shotsanity", [
        Shotsanity,
        ShotsanityCount,
        BalancedShotsanityCountPerRound
    ])
]