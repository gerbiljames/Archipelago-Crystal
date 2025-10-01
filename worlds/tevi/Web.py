"""Web UI related classes for Tevi"""
from worlds.AutoWorld import WebWorld
from BaseClasses import Tutorial

class TeviWeb(WebWorld):
    """Web integration for Tevi"""
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A unfinished guide to setting up the Tevi randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["BlackSoulKnight"],
        )
    ]
