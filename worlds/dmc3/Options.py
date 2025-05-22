from dataclasses import dataclass

from Options import Toggle, DeathLink, Choice, PerGameCommonOptions


class RandomizeAdjudicators(Toggle):
    """Randomizes Adjudicators in the game, changing their required weapon type"""
    display_name = "Randomize Adjudicators"

class AdjudicatorRankings(Choice):
    """Set the max style rank for randomized adjudicators. Leave at default to not change them (I can't recommend SS or SSS)"""
    display_name = "Max Rando. Adjudicator Rank (Inclusive)"
    default = 0 # Unchanged
    #option_d_rank = 1 # Pretty sure this will result in all adjudicators insta popping, iirc
    option_c_rank = 2
    option_b_rank = 3
    option_a_rank = 4
    option_s_rank = 5
    option_ss_rank = 6 # Don't know how to fix the capitalization here
    option_sss_rank = 7



class StartMelee(Choice):
    """Set your starting melee weapon"""
    display_name = "Starting Melee"
    #valid_keys = ["Rebellion", "Cerberus", "Agni and Rudra", "Nevan", "Beowulf"]
    default = 0
    option_rebellion = 0
    option_cerberus = 1
    option_agni_and_rudra = 2
    option_nevan = 3
    option_beowulf = 4


class StartGun(Choice):
    """Set your starting gun"""
    display_name = "Starting Gun"
    #valid_keys = ["Ebony & Ivory", "Shotgun", "Artemis", "Spiral", "Kalina_ann"]
    default = 0
    option_ebony_and_ivory = 0
    option_shotgun = 1
    option_artemis = 2
    option_spiral = 3
    option_kalina_ann = 4

@dataclass
class DMC3Options(PerGameCommonOptions):
    random_adjudicators: RandomizeAdjudicators
    adjudicator_rankings: AdjudicatorRankings
    start_melee: StartMelee
    start_gun: StartGun
    death_link: DeathLink
