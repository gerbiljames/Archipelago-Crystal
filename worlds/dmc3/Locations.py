from typing import NamedTuple

from BaseClasses import Location

location_descriptions = {
    "Blue Orb Fragment #1": "Mission 3 before entering Cerberus' boss fight",
}


class DMC3LocationData(NamedTuple):
    mission_number: int # 0 If irrelevant
    default_item: int
    room_number: int = 0
    secret: bool = False,


dmc3_locations: dict[str, DMC3LocationData] = {
     "Mission #2 - Vital Star S": DMC3LocationData(mission_number=2, default_item=0x11, room_number=2),

    "Mission #3 - Shotgun": DMC3LocationData(mission_number=3, default_item=0x1D, room_number=3),
    "Mission #3 - Blue Orb Fragment #1": DMC3LocationData(mission_number=3, default_item=0x09, room_number=5),
    "Mission #3 - Cerberus": DMC3LocationData(mission_number=3, default_item=0x17, room_number=6),

    "Mission #4 - Blue Orb Fragment #2": DMC3LocationData(mission_number=4, default_item=0x09, room_number=110), #?
    "Mission #4 - Astronomical Board": DMC3LocationData(mission_number=4, default_item=0x24, room_number=110),

    "Mission #5 - Vajura": DMC3LocationData(mission_number=5, default_item=0x25, room_number=0),
    "Mission #5 - Soul of Steel": DMC3LocationData(mission_number=5, default_item=0x27, room_number=0),
    "Mission #5 - Agni and Rudra": DMC3LocationData(mission_number=5, default_item=0x18, room_number=0),

    "Mission #6 - Essence of Technique": DMC3LocationData(mission_number=6, default_item=0x29, room_number=0),
    "Mission #6 - Essence of Intelligence": DMC3LocationData(mission_number=6, default_item=0x2A, room_number=0),
    "Mission #6 - Essence of Fighting": DMC3LocationData(mission_number=6, default_item=0x28, room_number=0),
    "Mission #6 - Artemis": DMC3LocationData(mission_number=6, default_item=0x1E, room_number=0),

    "Mission #7 - Orichalcum Fragment": DMC3LocationData(mission_number=7, default_item=0x2B, room_number=0),
    "Mission #7 - Holy Water": DMC3LocationData(mission_number=7, default_item=0x13, room_number=0),
    "Mission #7 - Blue Orb Fragment #3": DMC3LocationData(mission_number=7, default_item=0x09, room_number=0),
    "Mission #7 - Vital Star S": DMC3LocationData(mission_number=7, default_item=0x11, room_number=0),
    "Mission #7 - Siren's Shriek": DMC3LocationData(mission_number=7, default_item=0x0E, room_number=0),
    "Mission #7 - Crystal Skull": DMC3LocationData(mission_number=7, default_item=0x0F, room_number=0),

    "Mission #8 - Blue Orb Fragment #4": DMC3LocationData(mission_number=8, default_item=0x09, room_number=0),
    "Mission #8 - Ignis Fatuus": DMC3LocationData(mission_number=8, default_item=0x0E, room_number=0),

    "Mission #9 - Blue Orb Fragment #5": DMC3LocationData(mission_number=9, default_item=0x09, room_number=0),
    "Mission #9 - Spiral": DMC3LocationData(mission_number=9, default_item=0x1F, room_number=0),
    "Mission #9 - Ambrosia": DMC3LocationData(mission_number=9, default_item=0x0D, room_number=0),
    "Mission #9 - Devil Star": DMC3LocationData(mission_number=9, default_item=0x12, room_number=0),
    "Mission #9 - Nevan": DMC3LocationData(mission_number=9, default_item=0x1A, room_number=0),

    "Mission #10 - Stone Mask": DMC3LocationData(mission_number=10, default_item=0x30, room_number=0),
    "Mission #10 - Neo Generator": DMC3LocationData(mission_number=10, default_item=0x31, room_number=0),

    "Mission #11 - Devil Star": DMC3LocationData(mission_number=11, default_item=0x12, room_number=0),
    "Mission #11 - Blue Orb Fragment #6": DMC3LocationData(mission_number=11, default_item=0x09, room_number=0),
    "Mission #11 - Holy Water": DMC3LocationData(mission_number=11, default_item=0x13, room_number=0),

    "Mission #12 - Haywire Neo Generator": DMC3LocationData(mission_number=12, default_item=0x32, room_number=0),
    "Mission #12 - Vital Star L": DMC3LocationData(mission_number=12, default_item=0x10, room_number=0),
    "Mission #12 - Quicksilver": DMC3LocationData(mission_number=12, default_item=0x22, room_number=0),

    "Mission #13 - Devil Star": DMC3LocationData(mission_number=13, default_item=0x12, room_number=0),
    "Mission #13 - Orihalcon": DMC3LocationData(mission_number=13, default_item=0x33, room_number=0),

    "Mission #14 - Beowulf": DMC3LocationData(mission_number=14, default_item=0x1B, room_number=0),
    "Mission #14 - Vital Star S": DMC3LocationData(mission_number=14, default_item=0x11, room_number=0),
    "Mission #14 - Blue Orb Fragment #7": DMC3LocationData(mission_number=14, default_item=0x09, room_number=0),
    "Mission #14 - Devil Star": DMC3LocationData(mission_number=14, default_item=0x12, room_number=0),
    "Mission #14 - Holy Water": DMC3LocationData(mission_number=14, default_item=0x13, room_number=0),

    "Mission #15 - Orihalcon Fragment #1": DMC3LocationData(mission_number=15, default_item=0x34, room_number=0),
    "Mission #15 - Orihalcon Fragment #2": DMC3LocationData(mission_number=15, default_item=0x35, room_number=0),
    "Mission #15 - Orihalcon Fragment #3": DMC3LocationData(mission_number=15, default_item=0x36, room_number=0),
    "Mission #15 - Blue Orb Fragment #8": DMC3LocationData(mission_number=15, default_item=0x09, room_number=0),

    "Mission #16 - Devil Star": DMC3LocationData(mission_number=16, default_item=0x12, room_number=0),
    "Mission #16 - Onyx Moonshard": DMC3LocationData(mission_number=16, default_item=0x38, room_number=0),
    "Mission #16 - Golden Sun": DMC3LocationData(mission_number=16, default_item=0x37, room_number=0),
    "Mission #16 - Vital Star S": DMC3LocationData(mission_number=16, default_item=0x11, room_number=0),
    "Mission #16 - Blue Orb Fragment #9": DMC3LocationData(mission_number=16, default_item=0x09, room_number=0),
    "Mission #16 - Kalina Ann": DMC3LocationData(mission_number=16, default_item=0x21, room_number=0),

    "Mission #17 - Vital Star S": DMC3LocationData(mission_number=17, default_item=0x11, room_number=0),
    "Mission #17 - Blue Orb Fragment #10": DMC3LocationData(mission_number=17, default_item=0x09, room_number=0),
    "Mission #17 - Doppelganger": DMC3LocationData(mission_number=17, default_item=0x23, room_number=0),

    "Mission #18 - Blue Orb Fragment #11": DMC3LocationData(mission_number=18, room_number=0, default_item=0x09),

    "Mission #19 - Vital Star L": DMC3LocationData(mission_number=19, room_number=0, default_item=0x10),
    "Mission #19 - Samsara": DMC3LocationData(mission_number=19, room_number=0, default_item=0x39),

    # "Mission #3 - Combat Adjudicator #1": DMC3LocationData(mission_number=3, room_number=0, default_item=0x09),
    # "Mission #5 - Combat Adjudicator #2": DMC3LocationData(mission_number=5, room_number=0, default_item=0x09),
    # "Mission #6 - Combat Adjudicator #3": DMC3LocationData(mission_number=6, room_number=0, default_item=0x09),
    # "Mission #7 - Combat Adjudicator #4": DMC3LocationData(mission_number=7, room_number=0, default_item=0x09),
    # "Mission #8 - Combat Adjudicator #5": DMC3LocationData(mission_number=8, room_number=0, default_item=0x09),
    # "Mission #9 - Combat Adjudicator #6": DMC3LocationData(mission_number=9, room_number=0, default_item=0x09),
    # "Mission #11 - Combat Adjudicator #7": DMC3LocationData(mission_number=11, room_number=0, default_item=0x09),
    # "Mission #13 - Combat Adjudicator #8": DMC3LocationData(mission_number=13, room_number=0, default_item=0x09),
    # "Mission #14 - Combat Adjudicator #9": DMC3LocationData(mission_number=14, room_number=0, default_item=0x09),
    # "Mission #17 - Combat Adjudicator #10": DMC3LocationData(mission_number=17, room_number=0, default_item=0x09),
    #
    # # Secret Missions (All are Blue Orb Fragments)
    # "Secret Mission #1": DMC3LocationData(mission_number=21, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #2": DMC3LocationData(mission_number=22, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #3": DMC3LocationData(mission_number=23, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #4": DMC3LocationData(mission_number=24, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #5": DMC3LocationData(mission_number=25, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #6": DMC3LocationData(mission_number=26, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #7": DMC3LocationData(mission_number=27, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #8": DMC3LocationData(mission_number=28, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #9": DMC3LocationData(mission_number=29, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #10": DMC3LocationData(mission_number=31, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #11": DMC3LocationData(mission_number=32, room_number=0, secret=True, default_item=0x09),
    # "Secret Mission #12": DMC3LocationData(mission_number=33, room_number=0, secret=True, default_item=0x09),
}


class DMC3Location(Location):
    game = "Devil May Cry 3"

    def __init__(self, player: int, name="", code=None, parent=None) -> None:
        super(DMC3Location, self).__init__(player, name, code, parent)
        self.event = code is None
