from dataclasses import dataclass

from Options import Toggle, Choice, PerGameCommonOptions, OptionCounter, Range, ExcludeLocations, OptionGroup


class RandomizeAdjudicators(Toggle):
    """Randomizes Adjudicators in the game, changing their required weapon type"""
    display_name = "Randomize Adjudicators"


class AdjudicatorRankings(Choice):
    """Set the max style rank for randomized adjudicators.

    Leave at default to not change them (I can't recommend SS or SSS)"""
    display_name = "Max Rando. Adjudicator Rank (Inclusive)"
    # option_d_rank = 1 # Pretty sure this will result in all adjudicators insta popping, iirc
    option_unchanged = 0
    option_c_rank = 2
    option_b_rank = 3
    option_a_rank = 4
    option_s_rank = 5
    option_ss_rank = 6
    option_sss_rank = 7
    default = 0  # Unchanged

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == 6 or value == 7:
            # A little silly, but oh well
            return cls.name_lookup[value].replace("s", "S").replace("_", " ").replace("r", "R")
        return super().get_option_name(value)


class StartMelee(Choice):
    """Set your starting melee weapon"""
    display_name = "Starting Melee"
    option_rebellion = 0
    option_cerberus = 1
    option_agni_and_rudra = 2
    option_nevan = 3
    option_beowulf = 4
    default = 0


class StartGun(Choice):
    """Set your starting gun"""
    display_name = "Starting Gun"
    option_ebony_and_ivory = 0
    option_shotgun = 1
    option_artemis = 2
    option_spiral = 3
    option_kalina_ann = 4
    default = 0


class RandomizeSkills(Toggle):
    """Should weapon skills and gun levels be items?"""
    display_name = "Randomize Skills and Gun Levels"


class RandomizeStyles(Toggle):
    """Add Dante's styles into the world as progressive upgrades. The starting style will be chosen at random unless one is specified via start inventory"""
    display_name = "Randomize Styles"


class PurpleOrbMode(Toggle):
    """
    On: 10 Purple orbs will be added to the item pool (DT Item will be worth 0 runes if it is in the item pool)

    Off: 7 Purple orbs will be added to the item pool as well as the Devil Trigger Item (Worth 3 DT Runes)
    """
    display_name = "Purple Orb Mode"


class DevilTriggerMode(Toggle):
    """
    **On**: Devil Trigger item will be needed to access Devil Trigger (DT Item will be added to the item pool)

    **Off**: Devil Trigger will be accessible upon reaching 3 runes
    """
    display_name = "Devil Trigger Mode"

class MissionClearRank(Choice):
    """
    What minimum rank is needed to give a mission's completed check.

    **D** will be any and all ranks

    **C, B, A, S** are self-explanatory

    **SS** is a perfect S rank, all sub ranks must be S as well. (Only choose this if you are confident in your abilities)
    """
    display_name = "Minimum Mission Clear Rank"
    option_d_rank = 0
    option_c_rank = 2
    option_b_rank = 3
    option_a_rank = 4
    option_s_rank = 5
    option_ss_rank = 6
    default = 0  # Unchanged

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == 6:
            # A little silly, but oh well
            return cls.name_lookup[value].replace("s", "S").replace("_", " ").replace("r", "R")
        return super().get_option_name(value)


class SSRankGoodies(Toggle):
    """
    Allow excluded SS Rank Mission Clears to have useful items and not just filler
    """
    display_name = "Useful SS Rank Goodies"


class DeathLinkSettings(Choice):
    """
    **DeathLink**: Standard DeathLink behavior.

    **HurtLink**: Sends DeathLink messages out when you die. But any received DeathLink's will cause (Difficulty Dependent) damage rather than insta kill.

    **None**: No death link features will be enabled
    """
    display_name = "Death Link"
    option_none = 0
    option_deathlink = 1
    option_hurtlink = 2
    default = 0


class DMC3Goal(Choice):
    """
    Which goal setting to use:

    **Standard**: Beat M20 in linear order M1-M20

    **All**: Beat all missions, all are unlocked at start

    **Random Order**: Beat all missions in a random linear order
    """
    display_name = "Goal"
    option_standard = 0
    option_all = 1
    option_random_order = 2
    default = 0


class MissionShuffle(Choice):
    """
    **Grouped**: All 20 missions are divided into blocks of 5 missions. The order of these blocks is then randomized

    **Pure RNG**: Leave it all up to chance. You may get Mission #1 as your first, or you may get Mission #20.
    Not recommended for Synchronous games.

    **Weighted**: Mission order is based on the provided weights
    """
    display_name = "Mission Order Setting"
    option_weighted = 0
    option_grouped = 1
    option_rng = 2
    default = 1

class MissionOrderGroup(Range):
    """
    Used for the "Grouped" Mission order setting

    Set's how many mission "groups" there are

    I.e 20/N where N is number of groups.
    """
    display_name = "Mission Order Group Count"
    range_start = 1
    range_end = 20
    default = 4

class MissionOrderWeights(OptionCounter):
    """
    Mission weight setting for the weighted mission order option

    Bigger number means it's more likely to be picked near the beginning. Smaller number means it has less of a chance of being picked.

    (If you don't know what to do, leave this alone)
    """
    display_name = "Mission Order Weights"
    valid_keys = [f"Mission #{mission_name}" for mission_name in range(1, 21)]
    min = 1
    default = {
        "Mission #1": 30,
        "Mission #2": 30,
        "Mission #3": 20,
        "Mission #4": 20,
        "Mission #5": 20,
        "Mission #6": 20,
        "Mission #7": 15,
        "Mission #8": 20,
        "Mission #9": 20,
        "Mission #10": 20,
        "Mission #11": 20,
        "Mission #12": 20,
        "Mission #13": 5,
        "Mission #14": 20,
        "Mission #15": 20,
        "Mission #16": 20,
        "Mission #17": 20,
        "Mission #18": 10,
        "Mission #19": 5,
        "Mission #20": 5,
    }

# Default exclusion list. I don't like doing these SM's
class DMC3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({"Secret Mission #3", "Secret Mission #6", "Secret Mission #7", "Secret Mission #12"}|
                        # Don't want progression in these
                        {f"Mission #{mission_numb} SS Rank" for mission_numb in range(1,21)})


@dataclass
class DMC3Options(PerGameCommonOptions):
    random_adjudicators: RandomizeAdjudicators
    adjudicator_rankings: AdjudicatorRankings
    start_melee: StartMelee
    start_gun: StartGun
    randomize_skills: RandomizeSkills
    death_link: DeathLinkSettings
    randomize_styles: RandomizeStyles
    purple_orb_mode: PurpleOrbMode
    devil_trigger_mode: DevilTriggerMode
    mission_clear_rank: MissionClearRank
    useful_ss_checks: SSRankGoodies
    goal: DMC3Goal
    mission_shuffle: MissionShuffle
    mission_weights: MissionOrderWeights
    mission_group: MissionOrderGroup
    exclude_locations: DMC3ExcludeLocations

option_groups = [
    OptionGroup("Item & Location Options", [
        DMC3ExcludeLocations,

    ])
]

dmc3_presets = {
    # Excludes a few locations I don't like doing
    "Ash's Default": {
        "random_adjudicators": True,
        "adjudicator_rankings": 4,
        "randomize_skills": True,
        "randomize_styles": True,
        "purple_orb_mode": False,
        "devil_trigger_mode": True,
        "goal": "standard",
        "exclude_locations": ["Secret Mission #3", "Secret Mission #6", "Secret Mission #7", "Secret Mission #12"]
    }
}
