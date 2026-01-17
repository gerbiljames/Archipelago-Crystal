from Options import DeathLink, OptionCounter, OptionDict, OptionGroup, Range, Toggle
from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Choice, OptionSet, Removed, Visibility
import collections
from schema import Schema, And
from Options import OptionDict, OptionError

class AmountOfGrass(Range):
    """In this randomizer, your goal is to collect enough grass and go to the final platform.
    This option sets the total amount of grass in the game. Remaining items become flower filler items."""
    display_name = "Amount Of Grass"
    default = 100
    range_start = 10
    range_end = 160
    
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

class Cubes(Choice):
    """
    Cubes are also location checks in the main gamemode! This option determines when you can collect cubes.
    Always: cubes are always collectable.
    Cubes Bag: [NOT IMPLEMENTED YET] you need to find the Cubes Bag item first to be able to collect cubes.
    Never: there are no cubes at all in your game (and they are not location checks).
    """
    display_name = "Cubes"
    option_always = 0
    # option_cubes_bag = 1
    option_never = 9
    default = 0

class NumberOfMinigames(Range):
    """
    Refunct allows for adding several minigames to your game, which you have to unlock first.
    This options sets how many minigames are included in the game.
    Set this to -1 if you want all minigames. Set this to 0 if you don't want any minigames.
    The next option allows you to tweak how likely each minigame is to be included, but the default is probably OK!
    """
    display_name = "Number of Minigames"
    default = -1
    range_start = -1
    range_end = 4
    
class NerfMinigameChecks(Toggle):
    """
    Most minigames have a lot of checks (~37).
    If this option is *on*, flowers will be forced into the minigames, so that only 10 items per minigame are not necessarily flowers.
    With the option *off*, all items in the minigames are actual checks.
    """
    display_name = "Nerf Minigame Checks"
    default = False
    

class NumberOfUnlocksPerMinigame(Range):
    """
    Each minigame needs to be unlocked first by finding its unlock item in the main game.
    This option sets how many unlock items of each minigame are there in the main game.
    Just one unlock item is enough to play, so having more than one makes it more likely that you can play that minigame.
    """
    display_name = "Number of Unlocks per Minigame"
    default = 1
    range_start = 1
    range_end = 2


class MinigamesLikeliness(OptionCounter):
    """
    Refunct allows for adding several minigames to your game, which each have their own items and locations.
    You can switch between Move Rando (main game) and the minigames in the Archipelago menu in-game.
    This setting determines the likeliness of each minigame to be included.
    The default settings are tweaked already so that the "better" minigames are more likely to appear.
    
    Vanilla Minigame:
    Adding this minigame will let you play the original vanilla refunct game, once you unlock it.
    You have all your abilities and every button is a check (up to 10 useful items).
     
    Seeker Minigame:
    Adding this minigame will let you search for 10 platforms that are not grassified yet, once you unlock it.
    You have all your abilities and jumping on empty platforms will give you checks.
     
    Button Galore Minigame:
    This minigame spawns you in a game with all plaforms already there.
    And you just press every button that there is for a check (up to 10 useful items). 
    
    OG Randomizer Minigame:
    This is where it all started, you'll get to play the very first Refunct randomizer.
    Hitting a button triggers a random platform to appear somewhere in the level, and it gives a check!
    """
   
    display_name = "Likeliness of minigames"
    # all keys must be present and values must be integers >= 0
    schema = Schema({
        "Vanilla Minigame": int,
        "Seeker Minigame": int,
        "Button Galore Minigame": int,
        "OG Randomizer Minigame": int,
    })
    min = 0
    default = {
        "Vanilla Minigame": 3,
        "Seeker Minigame": 2,
        "Button Galore Minigame": 1,
        "OG Randomizer Minigame": 3,
    }
class Traps(Choice):
    """
    This option determines which traps are added to the game. 
    Each trap is added twice and replaces a "flower" filler item, if there are enough flowers.
    "none" adds no traps at all.
    "pretty" adds pretty traps that visually change the game for 60 seconds:
    Dark skies, No skylight, Disco sky, Starry sky, Red sky, Hurricane
    "all" adds pretty traps and also adds gameplay affecting traps that last for 30 seconds:
    Slo-mo, Fast-mo, Blurrrrgh.
    """
    display_name = "Traps"
    option_none = 0
    option_pretty = 1
    option_all = 2
    default = 1

    
@dataclass
class RefunctOptions(PerGameCommonOptions):
    required_grass: Removed
    amount_of_grass: AmountOfGrass
    required_grass_percentage: RequiredGrassPercentage
    final_platform: FinalPlatform
    
    cubes: Cubes
    
    number_of_minigames: NumberOfMinigames
    nerf_minigame_checks: NerfMinigameChecks
    number_of_unlocks_per_minigame: NumberOfUnlocksPerMinigame
    minigames_likeliness: MinigamesLikeliness
    
    traps: Traps
    death_link: DeathLink

refunct_option_groups = [
    OptionGroup("Grass and Final Platform",
        [
            AmountOfGrass,
            RequiredGrassPercentage,
            FinalPlatform,
        ],
    ),
    OptionGroup(
        "Cubes",
        [
            Cubes
        ],
    ),
    OptionGroup(
        "Minigames",
        [
            NumberOfMinigames,
            NerfMinigameChecks,
            NumberOfUnlocksPerMinigame,
            MinigamesLikeliness,
        ],
    ),
    OptionGroup(
        "Traps and Deathlink",
        [
            Traps,
            DeathLink,
        ],
    ),
]