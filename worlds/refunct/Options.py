from Options import Range, Toggle
from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Choice

class RequiredGrass(Range):
    """In this randomizer, your goal is to collect enough grass and go to the final platform.
    There is a total of 173 grass in the game.
    This options sets the amount of grass you need."""
    display_name = "Required Grass"
    default = 100
    range_start = 10
    range_end = 173
    
class FinalPlatform(Choice):
    """Sets which platform is the final platform that needs to be reached to win the game.
    You can choose the following platforms:
    - Platform 1-5: right next to the starting platform
    - Platform 21-1: easy to reach platform in Cluster 21 (bottom-left)
    - Platform 29-2: epic high platform in Cluster 29 for which you need Cluster 25 and jumppads (top-left)
    - random_known: randomly chosen platform. The UI will show you which platform it is.
    
    - random_unknown: randomly chosen platform. The UI will NOT show you which platform it is until you jump on it.
                      you can !hint Final Platform and it will tell you the location.
    """
    display_name = "Final Platform"
    option_1_5 = 0
    option_21_1 = 1
    option_29_2 = 2
    option_random_known = 98
    option_random_unknown = 99
    default = 2

    
@dataclass
class RefunctOptions(PerGameCommonOptions):
    required_grass: RequiredGrass
    final_platform: FinalPlatform