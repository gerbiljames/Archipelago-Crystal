from dataclasses import dataclass

import Options
from Options import Toggle, DeathLink


class RandomizeAdjudicators(Toggle):
    """Randomizes Adjudicators in the game, changing their required weapon type"""
    display_name = "Randomize Adjudicators"


class StartMelee(Options.Choice):
    """Set your starting melee weapon"""
    display_name = "Starting Melee"
    #valid_keys = ["Rebellion", "Cerberus", "Agni and Rudra", "Nevan", "Beowulf"]
    default = 0
    option_rebellion = 0
    option_cerberus = 1
    option_agni_and_rudra = 2
    option_nevan = 3
    option_beowulf = 4


class StartGun(Options.Choice):
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
class DMC3Options(Options.PerGameCommonOptions):
    random_adjudicators: RandomizeAdjudicators
    start_melee: StartMelee
    start_gun: StartGun
    death_link: DeathLink
