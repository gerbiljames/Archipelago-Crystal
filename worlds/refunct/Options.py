from Options import Range, Toggle
from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Choice, OptionSet, Removed

class AmountOfGrass(Range):
    """In this randomizer, your goal is to collect enough grass and go to the final platform.
    This option sets the total amount of grass in the game."""
    display_name = "Amount Of Grass"
    default = 100
    range_start = 10
    range_end = 174
    
class RequiredGrassPercentage(Range):
    """This options sets the percentage of grass you need in order to win when you go to the final platform.
    0 means you don't need any grass at all and just need to find the final platform.
    Note: choosing max grass and 100% required may lead to some FillErrors in solo games."""
    display_name = "Required Grass Percentage"
    default = 70
    range_start = 0
    range_end = 100
    
class FinalPlatform(Choice):
    """Sets which platform is the final platform that needs to be reached to win the game.
    You can choose the following platforms:
    - Platform 1-5: right next to the starting platform
    - Platform 21-1: easy to reach platform in Cluster 21 (bottom-left)
    - Platform 29-2: epic high platform in Cluster 29 for which you need Cluster 25 and jumppads (top-left)
    - random_known: randomly chosen platform. The UI will show you which platform it is.
    - random_unknown: randomly chosen platform. The UI will NOT show you which platform it is until you jump on it. You can !hint Final Platform and it will tell you the location.
    """
    display_name = "Final Platform"
    option_1_5 = 0
    option_21_1 = 1
    option_29_2 = 2
    option_random_known = 98
    option_random_unknown = 99
    default = 2
    
class Minigames(OptionSet):
    """
    Refunct allows for adding several minigames to your game, which each have their own items and locations.
    You can switch between Move Rando (main game) and the minigames in the Archipelago menu in-game.
    
    Vanilla Minigame:
    Adding this minigame will let you play the original vanilla refunct game, once you unlock it.
    You have all your abilities and the buttons trigger the original platform movements.
    Every button will grant you a check
    Items added: 
      1x "Unlock Vanilla Minigame" (you need to collect this item to access the minigame)
     36x "Flower" (this item does nothing)
    Locations added:
     37x Button activations.
    Note: this minigame will have at least 27 flowers, so there are at most 10 useful items in this minigame.
     
    Seeker Minigame:
    Adding this minigame will let you search for 10 platforms that are not grassified yet, once you unlock it.
    You have all your abilities and jumping on empty platforms will give you checks.
    The final platform with the yellow button does not count but jumping on it might give you a nice overview.
    Items added:
      1x "Unlock Seeker Minigame" (you need to collect this item to access the minigame)
      9x "Flower" (this item does nothing)
    Locations added:
     10x Platform checks
    
    """

    display_name = "Minigames included"
    valid_keys = ["Vanilla Minigame", "Seeker Minigame"]
    default = ["Vanilla Minigame", "Seeker Minigame"]

    
@dataclass
class RefunctOptions(PerGameCommonOptions):
    required_grass: Removed
    amount_of_grass: AmountOfGrass
    required_grass_percentage: RequiredGrassPercentage
    final_platform: FinalPlatform
    minigames: Minigames