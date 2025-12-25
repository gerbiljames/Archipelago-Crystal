"""This module represents option defintions for Tevi"""
from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Toggle, Range,DeathLink


class OpenMorose(Toggle):
    """Gain access to Morose without Crossbomb or Clusterbomb"""
    display_name = "Open Morose"

class SuperBosses(Toggle):
    """Consider Tevi's Hidden Bosses in Library for the Logic"""
    display_name = "Super Bosses"

class RandomizeKnife(Toggle):
    """If set to false, you receive the Knife as Starting Item"""
    display_name = "Randomize Knife"

class RandomizeMoney(Toggle):
    """Randomize each Money Block"""
    display_name = "Randomize Money"
class RandomizeMananite(Toggle):
    """Randomize each Source of Mananite Shards"""
    display_name = "Randomize Mananite"

class RandomizeMagitite(Toggle):
    """Randomize each Source of Magitite Shards"""
    display_name = "Randomize Magitite"

class TraveseMode(Choice):
    """
    Choose how you want to Traverse the World
    Normal: no changes to the game
    Random Transition: Map transition like Morose -> Forest are randomized
    Random Teleporter: No Map transition and only through Teleport possible
    """
    display_name = "Traverse Mode"
    option_normal = 0
    option_random_transition = 1
    option_random_teleporter = 2
    default = 0


class RandomizeOrb(Toggle):
    """If set to false, you receive the Orb as Starting item"""
    display_name = "Randomize Orb"

class RandomizedItemUpgrades(Toggle):
    """
    If set to true, all Item upgrades in the Crafting Menu have random new Item
    and the Item upgrades are in a different Location i.e. on the overworld.     
    """
    display_name = "Randomized Item Upgrades"

class CeliaSableUnlocked(Toggle):
    """If this flag is true, Celia and Sable are already unlocked
    Also enables ChargeShot with only level 1 Orbitar
    """
    display_name = "Unlock Celia and Sable "

class FreeAttackUp(Range):
    """
    Start the Game with X amount of Atk Ups

    This is usefull to kill Bosses faster
    """
    range_start = 0
    range_end = 220
    default = 0
    
class ItemChaos(Toggle):
    """
    Item Chaos rerolls every non Progressive Item into a new Item.
    The new Item can be any type of Item as long as it can be stacked,
    this include even Item like High Jump.
    """
    display_name = "Chaos mode"

class GoalType(Choice):
    """
    Determines the requirement type to fight the Final Boss
    """ 
    display_name = "Goal Type"
    option_AstralGear = 0
    option_KillBosses = 1
  
class GearCount(Range):
    """
    The Amount of Gears found in the Game
    """
    range_start = 1
    range_end = 25
    default = 20

class GoalCount(Range):
    """
    The Amount of Gears required to Finish the Game
    If this Number is greater than Gear count,
    it is reduced to the Number of Gear count
    """
    range_start = 1
    range_end = 25
    default = 16

class WalljumpTrick(Choice):
    """
    Using Items to manipulate Movementspeed,
    for the Rabbit variants 200% Item use speed is required
    """
    display_name = "Walljump Tricks"
    option_disabled = 0
    option_AnyItem = 1
    option_RabbitJump = 2
    option_RabbitWalljump = 3
    default = 0

class Backflip(Toggle):
    """
    Backflip enables a early mini double jump
    """
    display_name = "Backflip"
class CKick(Toggle):
    """
    Use a dropkick against a ceiling to reverse movement Direction
    """
    display_name = "Ceiling kick"
    
class BarrierSkip(Choice):
    """
    Skip Cutscene Barriers with Airdash (easy) or Slide (hard) and requires 60 fps lock
    """
    display_name = "Barrier Skip"
    option_disable = 0
    option_easy = 1
    option_hard = 2
    default = 0
      
class HiddenPaths(Toggle):
    """
    Consider Hidden Paths in Free Roam for the logic
    """
    display_name = "Hidden Paths"

class EarlyDream(Toggle):
    "Skip Dreamkeeper wind with Dropkicks and Strong Air Up"
    display_name = "Dream Keeper entrance skip"


class ADCKick(Toggle):
    """
    Enter Gallery of Souls with a a precise Airdash into Walljump from Ceiling pixel 
    (very hard)
    """
    display_name = "ADCKick"


class ExcludeMemine(Toggle):
    """
    No progression items in Memine races
    """
    display_name = "Exclude Memine"
class ExcludeCrafting(Toggle):
    """
    No progression items in Crafting
    """
    display_name = "Exclude Item Crafting"
class ExcludeShop(Toggle):
    """
    No progression items in Shops
    """
    display_name = "Exclude Shops"
class ExcludeArcade(Toggle):
    """
    No progression items in Arcade
    """
    display_name = "Exclude Shops"
class ExcludeUpgradeCraft(Toggle):
    """
    No progression items in Item upgrades crafts
    """
    display_name = "Exclude Upgrade Crafting"

class pre_release_option_1(Toggle):
    """
    Does nothing
    """
    display_name = "Alpha Feature 1"

@dataclass
class TeviOptions(PerGameCommonOptions):
    """Tevi Options Definition"""
    traverse_Mode: TraveseMode
    open_morose: OpenMorose
    randomize_knife: RandomizeKnife
    randomize_orb: RandomizeOrb
    randomize_item_upgrade: RandomizedItemUpgrades
    randomize_money:RandomizeMoney
    randomize_mananite:RandomizeMananite
    randomize_magitite:RandomizeMagitite
    chaos_mode: ItemChaos
    celia_sable: CeliaSableUnlocked
    free_attack_up : FreeAttackUp
    goal_type: GoalType
    gear_count: GearCount
    goal_count: GoalCount
    walljumpTricks : WalljumpTrick
    backflip:Backflip
    cKick:CKick
    hiddenP:HiddenPaths
    earlydream: EarlyDream
    barrierSkip: BarrierSkip
    adcKick : ADCKick
    superBosses: SuperBosses

    excludeMemine:ExcludeMemine
    excludeCrafting:ExcludeCrafting
    excludeShop:ExcludeShop
    excludeUpgradeCraft:ExcludeUpgradeCraft
    excludeArcade:ExcludeArcade

    alphaFeature1:pre_release_option_1

    def getOptions(self):
        return {
            "traverse_mode":self.traverse_Mode.value,
            "open_morose":self.open_morose.value,
            "randomize_knife":self.randomize_knife.value,
            "randomize_orb":self.randomize_orb.value,
            "randomize_item_upgrade":self.randomize_item_upgrade.value,
            "chaos_mode":self.chaos_mode.value,
            "celia_sable":self.celia_sable.value,
            "free_attack_up":self.free_attack_up.value,
            "goal_type": self.goal_type.value,
            "gear_count":self.gear_count.value,
            "goal_count":self.goal_count.value,
            "walljumpTricks":self.walljumpTricks.value,
            "backflip":self.backflip.value,
            "cKick":self.cKick.value,
            "hiddenP":self.hiddenP.value,
            "earlydream":self.earlydream.value,
            "barrierSkip":self.barrierSkip.value,
            "adcKick":self.adcKick.value,
            "superBosses":self.superBosses.value
        }