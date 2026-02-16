from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, Visibility
from .misc.float_range_text import FloatRangeText


class SkillRating(Range):
    """
    Your vanilla in-game rating.
    This is used to calculate your expected accuracy on each song for logic, and greatly impacts the difficulty and pacing of the randomizer.
    
    Your vanilla rating can be found just above your player profile, and more details can be found on the player leaderboard page by pressing `3`.
    It is recommended that you set at least 25 scores in the base game first so that you know your rating.
    If you have not set 25 scores yet, these are some good general ranges depending on what song difficulty you can perform well on:
    **beginner:** 2.500 - 3.500, **normal:** 3.500 - 4.500, **hard:** 4.500 - 5.500, **expert:** 5.500 - 7.000, **unbeatable:** 7.000 - 9.000, **star:** 9.000+

    NOTE: This value will be divided by 1000. For example, if you want to set a skill rating of 5.830, set this to 5830
    """

    # """The minimum value is 2.500, and the maximum is 13.000"""

    display_name = "Skill Rating"

    # range_start = 2.500
    # range_end = 13.000

    # default = "5.000"

    range_start = 2500
    range_end = 13000

    default = 5000


class MaxDifficulty(Choice):
    """
    Sets the highest difficulty to unlock.
    Difficulties above this will be inaccessible during the randomizer.
    You should set this to the highest difficulty where you can consistently pass all of the songs.
    """

    display_name = "Maximum Difficulty"

    option_beginner = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    option_unbeatable = 4
    option_star = 5

    default = option_hard


class MinDifficulty(Choice):
    """
    Sets the first unlocked difficulty. Lower difficulties than this will be inacessible.
    Higher difficulties must be unlocked by finding multiple 'Progressive Song' items for each song.
    The more difficulties there are between this and Maximum Difficulty, the longer the game will be.
    For shorter/sync games, sticking to just one or two difficulties is usually ideal.
    """

    display_name = "Minimum Difficulty"

    option_beginner = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    option_unbeatable = 4
    option_star = 5

    default = option_hard


class CompletionPercent(Range):
    """
    Sets how close to the maximum rating you need to reach to complete the randomizer.
    Lower values make logic more lenient but can lead to pacing issues.

    If you want a shorter randomizer, consider increasing Minimum Difficulty first.
    Raising this is a good option for asyncs or games with a low difficulty count.
    """

    display_name = "Completion Percentage"

    range_start = 1
    range_end = 99

    default = 90


class UseBreakout(Toggle):
    """
    Includes songs from UNBEATABLE - Breakout Edition.
    This requires that you own the UNBEATABLE - Breakout Edition Upgrade DLC and have it installed.
    """

    display_name = "Include Breakout Songs"

    default = False


class StartSongCount(Range):
    """
    Sets how many songs to start with.
    """

    display_name = "Starting Songs"

    range_start = 1
    range_end = 10
    
    default = 3


class StartCharacterCount(Range):
    """
    Sets how many characters to start with.
    These are currently filler items, but some challenges will require certain characters later.
    """

    display_name = "Starting Characters"

    range_start = 1
    range_end = 11

    default = 1


class AllowPfc(Toggle):
    """
    When enabled, logic may expect you to get 100% accuracy on low-difficulty charts.
    """

    display_name = "Allow PFC"
    visibility = Visibility.complex_ui

    default = True


class AccCurveBias(Range):
    """
    Adjusts the slope of the expected accuracy curve at high accuracy.
    Higher values lead to higher expected accuracy on low-difficulty charts.
    It's probably best to leave this unchanged.
    """

    display_name = "High Curve Bias"
    visibility = Visibility.complex_ui

    range_start = 0
    range_end = 2000

    default = 1200


class LowCurveBias(Range):
    """
    Adjusts the slope of the expected accuracy curve at low accuracy.
    Higher values lead to lower expected accuracy on high-difficulty charts.
    It's probably best to leave this unchanged.
    """

    display_name = "Low Curve Bias"
    visibility = Visibility.complex_ui

    range_start = 0
    range_end = 2000

    default = 400


class AccCurveCutoff(Range):
    """
    Sets the accuracy where the high accuracy bias takes effect.
    Low values tend to lead to higher expected accuracy on high-difficulty charts.
    It's probably best to leave this unchanged.
    """

    display_name = "Accuracy Curve Start Point"
    visibility = Visibility.complex_ui

    range_start = 0
    range_end = 100

    default = 85


class UseTraps(Toggle):
    """
    Adds trap items to the item pool, which cause negative effects for you when collected.
    All traps are temporary effects which deactivate at the end of a song or after a some time has passed.
    The duration of each trap can be adjusted client-side using the mod configuration.
    """

    display_name = "Include Traps"

    default = True


# class NonLocalTraps(Toggle):
#     """
#     Tries to place traps outside of your local world, so they're more likely to be found by other players.
#     This can make traps a bit more interesting by making them activate mid-song more often.
#     Enabling this is the same as adding all the trap item names to the Non-local Items setting.
#     """
#
#     display_name = "Non-local Traps"
#
#     default = False


class SilenceTrapAmount(Range):
    """
    The amount of Silence Traps to add to the pool, which mute the music.
    This represents a percentage of items to add compared to the pool of beneficial items.
    (i.e. if there are 200 songs/characters in the pool, and this is set to 5, 10 Silence Traps will be added)
    """

    display_name = "Silence Trap Amount"

    range_start = 0
    range_end = 10

    default = 4


class StealthTrapAmount(Range):
    """
    The amount of Stealth Traps to add to the pool, which activate a stealth effect on all notes.
    This represents a percentage of items to add compared to the pool of beneficial items.
    (i.e. if there are 200 songs/characters in the pool, and this is set to 5, 10 Stealth Traps will be added)
    """

    display_name = "Stealth Trap Amount"

    range_start = 0
    range_end = 10

    default = 4


class RainbowTrapAmount(Range):
    """
    The amount of Rainbow Traps to add to the pool, which randomize the colors of all notes.
    This represents a percentage of items to add compared to the pool of beneficial items.
    (i.e. if there are 200 songs/characters in the pool, and this is set to 5, 10 Rainbow Traps will be added)
    """

    display_name = "Rainbow Trap Amount"

    range_start = 0
    range_end = 10

    default = 4


class ZoomTrapAmount(Range):
    """
    The amount of Zoom Traps to add to the pool, which increase note movement speed.
    This represents a percentage of items to add compared to the pool of beneficial items.
    (i.e. if there are 200 songs/characters in the pool, and this is set to 5, 10 Zoom Traps will be added)
    """

    display_name = "Zoom Trap Amount"

    range_start = 0
    range_end = 10

    default = 4


class CrawlTrapAmount(Range):
    """
    The amount of Crawl Traps to add to the pool, which reduce note movement speed.
    This represents a percentage of items to add compared to the pool of beneficial items.
    (i.e. if there are 200 songs/characters in the pool, and this is set to 5, 10 Crawl Traps will be added)
    """

    display_name = "Crawl Trap Amount"

    range_start = 0
    range_end = 10

    default = 4


@dataclass
class UNBEATABLEArcadeOptions(PerGameCommonOptions):
    skill_rating: SkillRating

    use_breakout: UseBreakout
    max_difficulty: MaxDifficulty
    min_difficulty: MinDifficulty
    completion_percent: CompletionPercent
    start_song_count: StartSongCount
    start_char_count: StartCharacterCount

    use_traps: UseTraps
    # non_local_traps: NonLocalTraps
    silence_amount: SilenceTrapAmount
    stealth_amount: StealthTrapAmount
    rainbow_amount: RainbowTrapAmount
    zoom_amount: ZoomTrapAmount
    crawl_amount: CrawlTrapAmount

    allow_pfc: AllowPfc
    acc_curve_bias: AccCurveBias
    acc_curve_low_bias: LowCurveBias
    acc_curve_cutoff: AccCurveCutoff


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [SkillRating, MaxDifficulty, MinDifficulty]
    ),
    OptionGroup(
        "Generation Options",
        [CompletionPercent, StartSongCount, StartCharacterCount, UseBreakout]
    ),
    OptionGroup(
        "Trap Options",
        [UseTraps, SilenceTrapAmount, StealthTrapAmount, RainbowTrapAmount, ZoomTrapAmount, CrawlTrapAmount]
    ),
    OptionGroup(
        "Advanced Difficulty Options",
        [AllowPfc, AccCurveBias, AccCurveCutoff]
    )
]