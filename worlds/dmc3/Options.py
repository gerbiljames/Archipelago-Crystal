from dataclasses import dataclass

from Options import Toggle, DeathLink, Choice, PerGameCommonOptions


class RandomizeAdjudicators(Toggle):
    """Randomizes Adjudicators in the game, changing their required weapon type"""
    display_name = "Randomize Adjudicators"


class AdjudicatorRankings(Choice):
    """Set the max style rank for randomized adjudicators. Leave at default to not change them (I can't recommend SS or SSS)"""
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
    display_name = "Randomize Skills+Levels"

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
    On: Devil Trigger item will be needed to access Devil Trigger (DT Item will be added to the item pool)
    Off: Devil Trigger will be accessible upon reaching 3 runes
    """
    display_name = "Devil Trigger Mode"

@dataclass
class DMC3Options(PerGameCommonOptions):
    random_adjudicators: RandomizeAdjudicators
    adjudicator_rankings: AdjudicatorRankings
    start_melee: StartMelee
    start_gun: StartGun
    randomize_skills: RandomizeSkills
    death_link: DeathLink
    randomize_styles: RandomizeStyles
    purple_orb_mode: PurpleOrbMode
    devil_trigger_mode: DevilTriggerMode
