from dataclasses import dataclass
from enum import Enum

from BaseClasses import Location

location_descriptions = {
    "Mission #3 - Blue Orb Fragment #1": "On a damaged building before entering Cerberus' boss fight",
}


@dataclass
class BaseLocationData:
    mission_number: int  # Mission Number, 0 if irrelevant
    room_number: int  # Room Number
    default_item: int  # Default Item
    secret: bool = False  # Secret mission?
    offset: int = 0x0  # Offset
    adjudicator: bool = False
    xCoord: int = 0
    yCoord: int = 0
    zCoord: int = 0


class Ranking(int, Enum):
    D = 1
    C = 2
    B = 3
    A = 4
    S = 5
    SS = 6
    SSS = 7


@dataclass
class Adjudicator:
    weapon: str
    ranking: Ranking


adjudicator_info: dict[str, Adjudicator] = {
    "Mission #3 - Combat Adjudicator #1": Adjudicator(weapon="Rebellion", ranking=Ranking.B),
    "Mission #5 - Combat Adjudicator #2": Adjudicator(weapon="Cerberus", ranking=Ranking.A),
    "Mission #6 - Combat Adjudicator #3": Adjudicator(weapon="Agni and Rudra", ranking=Ranking.A),
    "Mission #7 - Combat Adjudicator #4": Adjudicator(weapon="Rebellion", ranking=Ranking.SSS),
    "Mission #8 - Combat Adjudicator #5": Adjudicator(weapon="Cerberus", ranking=Ranking.SS),
    "Mission #9 - Combat Adjudicator #6": Adjudicator(weapon="Nevan", ranking=Ranking.B),
    "Mission #11 - Combat Adjudicator #7": Adjudicator(weapon="Agni and Rudra", ranking=Ranking.SS),
    "Mission #13 - Combat Adjudicator #8": Adjudicator(weapon="Nevan", ranking=Ranking.SS),
    "Mission #14 - Combat Adjudicator #9": Adjudicator(weapon="Beowulf", ranking=Ranking.C),
    "Mission #17 - Combat Adjudicator #10": Adjudicator(weapon="Beowulf", ranking=Ranking.SSS),
}

dmc3_locations: dict[str, BaseLocationData] = ({
    "Mission #2 - Vital Star S": BaseLocationData(mission_number=2, default_item=0x11, room_number=1, offset=0x5C4C50),

    "Mission #3 - Shotgun": BaseLocationData(mission_number=3, default_item=0x1D, room_number=3, offset=0x0),
    "Mission #3 - Blue Orb Fragment #1": BaseLocationData(mission_number=3, default_item=0x09, room_number=5,
                                                          offset=0x5C4C20, xCoord=0xF10DAD45, yCoord=0x62DD8444,
                                                          zCoord=0x55E52345),
    "Mission #3 - Cerberus": BaseLocationData(mission_number=3, default_item=0x17, room_number=6, offset=0x0),

    "Mission #4 - Blue Orb Fragment #2": BaseLocationData(mission_number=4, default_item=0x09, room_number=110,
                                                          offset=0x5C4C24, xCoord=0x1C780D45, yCoord=0xFEFFBE44,
                                                          zCoord=0x05053B45),
    # ?
    "Mission #4 - Astronomical Board": BaseLocationData(mission_number=4, default_item=0x24, room_number=110,
                                                        xCoord=0x75ABBD44, yCoord=0xFE7F5144, zCoord=0x5AA6D043),

    "Mission #5 - Vajura": BaseLocationData(mission_number=5, default_item=0x25, room_number=100),
    "Mission #5 - Soul of Steel": BaseLocationData(mission_number=5, default_item=0x27, room_number=102),
    "Mission #5 - Agni and Rudra": BaseLocationData(mission_number=5, default_item=0x18, room_number=121),

    "Mission #6 - Essence of Technique": BaseLocationData(mission_number=6, default_item=0x29, room_number=125),
    "Mission #6 - Essence of Intelligence": BaseLocationData(mission_number=6, default_item=0x2A, room_number=126),
    "Mission #6 - Essence of Fighting": BaseLocationData(mission_number=6, default_item=0x28, room_number=124),
    "Mission #6 - Artemis": BaseLocationData(mission_number=6, default_item=0x1E, room_number=122),
    # Special case for artemis in later Mission if not obtained earlier

    "Mission #7 - Orihalcon Fragment": BaseLocationData(mission_number=7, default_item=0x2B, room_number=115,
                                                        xCoord=0x3069E144, yCoord=0x0000803F, zCoord=0x321A6345),
    "Mission #7 - Holy Water": BaseLocationData(mission_number=7, default_item=0x13, room_number=114, offset=0x5C4C64),
    "Mission #7 - Blue Orb Fragment #3": BaseLocationData(mission_number=7, default_item=0x09, room_number=134,
                                                          offset=0x5C4C28),
    "Mission #7 - Vital Star S": BaseLocationData(mission_number=7, default_item=0x11, room_number=135,
                                                  offset=0x5C4C40),
    "Mission #7 - Siren's Shriek": BaseLocationData(mission_number=7, default_item=0x2C, room_number=136),
    "Mission #7 - Crystal Skull": BaseLocationData(mission_number=7, default_item=0x2D, room_number=105,
                                                   xCoord=0x55991E45, yCoord=0x55991E45, zCoord=0x15C92845),

    "Mission #8 - Blue Orb Fragment #4": BaseLocationData(mission_number=8, default_item=0x09, room_number=300,
                                                          offset=0x5C4C2C),
    "Mission #8 - Ignis Fatuus": BaseLocationData(mission_number=8, default_item=0x2E, room_number=305),

    "Mission #9 - Blue Orb Fragment #5": BaseLocationData(mission_number=9, default_item=0x09, room_number=203,
                                                          offset=0x5C4C30),
    "Mission #9 - Spiral": BaseLocationData(mission_number=9, default_item=0x1F, room_number=206),
    "Mission #9 - Ambrosia": BaseLocationData(mission_number=9, default_item=0x2F, room_number=208, xCoord=0x55404E45,
                                              yCoord=0x0000F042, zCoord=0x9FEA7645),
    # why did I put 0x0D as the default item
    "Mission #9 - Devil Star": BaseLocationData(mission_number=9, default_item=0x12, room_number=209, offset=0x5C4C9C,
                                                xCoord=0x9C757144, yCoord=0x4561CA43, zCoord=0x8C3CBC45),
    "Mission #9 - Nevan": BaseLocationData(mission_number=9, default_item=0x1A, room_number=210),  # ?

    "Mission #10 - Stone Mask": BaseLocationData(mission_number=10, default_item=0x30, room_number=209,
                                                 xCoord=0x7F665F45, yCoord=0x00D00345, zCoord=0x90A44E44),
    "Mission #10 - Neo Generator": BaseLocationData(mission_number=10, default_item=0x31, room_number=206,
                                                    xCoord=0x22982846, yCoord=0x3E474445, zCoord=0xF2F3E645),

    "Mission #11 - Devil Star": BaseLocationData(mission_number=11, default_item=0x12, room_number=212,
                                                 offset=0x5C4C94),  # ??, # 04 d4 4c 12
    "Mission #11 - Blue Orb Fragment #6": BaseLocationData(mission_number=11, default_item=0x09, room_number=213,
                                                           offset=0x5C4C34, xCoord=0x15FC3F44, yCoord=0xFEBF7044,
                                                           zCoord=4391237),
    "Mission #11 - Holy Water": BaseLocationData(mission_number=11, default_item=0x13, room_number=239, offset=0x5C4C44,
                                                 xCoord=0x55704F45, yCoord=0xFDFF4744, zCoord=0x15148245),

    "Mission #12 - Haywire Neo Generator": BaseLocationData(mission_number=12, default_item=0x32, room_number=217),
    # M12
    "Mission #12 - Vital Star L": BaseLocationData(mission_number=12, default_item=0x10, room_number=218,
                                                   offset=0x5C4C4C),
    "Mission #12 - Quicksilver": BaseLocationData(mission_number=12, default_item=0x22, room_number=228),

    "Mission #13 - Devil Star": BaseLocationData(mission_number=13, default_item=0x12, room_number=241,
                                                 offset=0x5C4C98),
    "Mission #13 - Orihalcon": BaseLocationData(mission_number=13, default_item=0x33, room_number=233),  # ??

    "Mission #14 - Beowulf": BaseLocationData(mission_number=14, default_item=0x1B, room_number=237),
    "Mission #14 - Vital Star S": BaseLocationData(mission_number=14, default_item=0x11, room_number=236,
                                                   offset=0x5C4C5C, xCoord=0x55B9B445, yCoord=0x55B9B445,
                                                   zCoord=0xE0360A45),
    "Mission #14 - Blue Orb Fragment #7": BaseLocationData(mission_number=14, default_item=0x09, room_number=236,
                                                           offset=0x5C4C60, xCoord=0xFF5E2C44, yCoord=0x0000A040,
                                                           zCoord=0xABA9F944),  # hell highway?
    "Mission #14 - Devil Star": BaseLocationData(mission_number=14, default_item=0x12, room_number=231,
                                                 offset=0x5C4C58),
    "Mission #14 - Holy Water": BaseLocationData(mission_number=14, default_item=0x13, room_number=8, offset=0x5C4CA4),

    "Mission #15 - Orihalcon Fragment #1": BaseLocationData(mission_number=15, default_item=0x34, room_number=213,
                                                            xCoord=0xAE21C245, yCoord=0x0000EC42, zCoord=0x41291E45),
    # Right
    "Mission #15 - Orihalcon Fragment #2": BaseLocationData(mission_number=15, default_item=0x35, room_number=208,
                                                            xCoord=0xB8454E45, yCoord=0x0000F042, zCoord=0x00E07645),
    # Bottom
    "Mission #15 - Orihalcon Fragment #3": BaseLocationData(mission_number=15, default_item=0x36, room_number=224),
    # Left
    "Mission #15 - Blue Orb Fragment #8": BaseLocationData(mission_number=15, default_item=0x09, room_number=238,
                                                           offset=0x5C4C38),

    "Mission #16 - Devil Star": BaseLocationData(mission_number=16, default_item=0x12, room_number=105, offset=0x5C4CA0,
                                                 xCoord=0x15411C45, yCoord=0x0000803F, zCoord=0x6B1AC844),
    "Mission #16 - Onyx Moonshard": BaseLocationData(mission_number=16, default_item=0x38, room_number=109),
    "Mission #16 - Golden Sun": BaseLocationData(mission_number=16, default_item=0x37, room_number=146),
    "Mission #16 - Vital Star S": BaseLocationData(mission_number=16, default_item=0x11, room_number=116,
                                                   offset=0x5C4C68),
    # "Mission #16 - Blue Orb Fragment #9": BaseLocationData(mission_number=16, default_item=0x09, room_number=0),
    "Mission #16 - Kalina Ann": BaseLocationData(mission_number=16, default_item=0x21, room_number=119),
    # M16 R117 for 2nd artemis spawn

    "Mission #17 - Vital Star S": BaseLocationData(mission_number=17, default_item=0x11, room_number=133,
                                                   offset=0x5C4C48),
    "Mission #17 - Blue Orb Fragment #10": BaseLocationData(mission_number=17, default_item=0x09, room_number=120,
                                                            offset=0x5C4C3C),
    "Mission #17 - Doppelganger": BaseLocationData(mission_number=17, default_item=0x23, room_number=139),
    # M17 R130 - Gold Orb

    "Mission #18 - Blue Orb Fragment #11": BaseLocationData(mission_number=18, room_number=403, default_item=0x09,
                                                            offset=0x0),  # Boss fight arena

    "Mission #19 - Vital Star L": BaseLocationData(mission_number=19, room_number=405, default_item=0x10,
                                                   offset=0x5C4C54),
    # Where?? # 00 95 4d 10, I dont get it
    "Mission #19 - Samsara": BaseLocationData(mission_number=19, room_number=404, default_item=0x39),

    "Mission #3 - Combat Adjudicator #1": BaseLocationData(mission_number=3, room_number=5, default_item=0x09,
                                                           adjudicator=True, offset=0x5C4C6C + (0x4 * 0),
                                                           xCoord=0x00108745, yCoord=0x00406D44, zCoord=0x00503A45),
    "Mission #5 - Combat Adjudicator #2": BaseLocationData(mission_number=5, room_number=112, default_item=0x09,
                                                           adjudicator=True, offset=0x5C4C6C + (0x4 * 1)),
    "Mission #6 - Combat Adjudicator #3": BaseLocationData(mission_number=6, room_number=127, default_item=0x09,
                                                           adjudicator=True, offset=0x5C4C6C + (0x4 * 2)),
    "Mission #7 - Combat Adjudicator #4": BaseLocationData(mission_number=7, room_number=137, default_item=0x09,
                                                           adjudicator=True, offset=0x5C4C6C + (0x4 * 3)),
    "Mission #8 - Combat Adjudicator #5": BaseLocationData(mission_number=8, room_number=306, default_item=0x09,
                                                           adjudicator=True, offset=0x5C4C6C + (0x4 * 4)),
    "Mission #9 - Combat Adjudicator #6": BaseLocationData(mission_number=9, room_number=206, default_item=0x09,
                                                           adjudicator=True, offset=0x5C4C6C + (0x4 * 5),
                                                           xCoord=0x00D43046, yCoord=0x00402445, zCoord=0x0020AD45),
    # Think so?
    "Mission #11 - Combat Adjudicator #7": BaseLocationData(mission_number=11, room_number=239, default_item=0x09,
                                                            adjudicator=True, offset=0x5C4C6C + (0x4 * 6),
                                                            xCoord=0x0000C844, yCoord=0x00C0C144, zCoord=0x00D08445),
    "Mission #13 - Combat Adjudicator #8": BaseLocationData(mission_number=13, room_number=232, default_item=0x09,
                                                            adjudicator=True, offset=0x5C4C6C + (0x4 * 7)),
    "Mission #14 - Combat Adjudicator #9": BaseLocationData(mission_number=14, room_number=237, default_item=0x09,
                                                            adjudicator=True, offset=0x5C4C6C + (0x4 * 8),
                                                            xCoord=0x00008C42, yCoord=0x000048C2, zCoord=0x00B09A45),
    "Mission #17 - Combat Adjudicator #10": BaseLocationData(mission_number=17, room_number=128, default_item=0x09,
                                                             adjudicator=True, offset=0x5C4C6C + (0x4 * 9)),

    # Secret Missions (All are Blue Orb Fragments)
    "Secret Mission #1": BaseLocationData(mission_number=21, room_number=600, secret=True, default_item=0x09),
    "Secret Mission #2": BaseLocationData(mission_number=22, room_number=601, secret=True, default_item=0x09),
    "Secret Mission #3": BaseLocationData(mission_number=23, room_number=602, secret=True, default_item=0x09),
    "Secret Mission #4": BaseLocationData(mission_number=24, room_number=603, secret=True, default_item=0x09),
    "Secret Mission #5": BaseLocationData(mission_number=25, room_number=604, secret=True, default_item=0x09),
    "Secret Mission #6": BaseLocationData(mission_number=26, room_number=605, secret=True, default_item=0x09),
    "Secret Mission #7": BaseLocationData(mission_number=27, room_number=606, secret=True, default_item=0x09),
    "Secret Mission #8": BaseLocationData(mission_number=28, room_number=607, secret=True, default_item=0x09),
    "Secret Mission #9": BaseLocationData(mission_number=29, room_number=608, secret=True, default_item=0x09),
    "Secret Mission #10": BaseLocationData(mission_number=31, room_number=609, secret=True, default_item=0x09),
    "Secret Mission #11": BaseLocationData(mission_number=32, room_number=610, secret=True, default_item=0x09),
    "Secret Mission #12": BaseLocationData(mission_number=33, room_number=611, secret=True, default_item=0x09),
    # "Mission #20 - Finished": BaseLocationData(mission_number=20, room_number=000, default_item=0x00),
    # Room 101 M7 Has a gold orb
    # Room 10 M14 Gold Orb
}|
    {"Mission #{} Complete".format(mission_numb): BaseLocationData(mission_number=mission_numb, room_number=0, default_item=0x00)
     for mission_numb in range(1,20)})

location_name_groups = {
                           # TODO Normally 21, but M20 is empty... unless it should have the complete check in it.
    f"Mission #{numb}": [location for location, data in dmc3_locations.items() if data.mission_number == numb] for numb in range(1,20)
}|{"Secret Missions": [f"Secret Mission #{numb}"] for numb in range(1,13)}

class DMC3Location(Location):
    game = "Devil May Cry 3"

    def __init__(self, player: int, name="", code=None, parent=None) -> None:
        super(DMC3Location, self).__init__(player, name, code, parent)
        self.event = code is None


adjudicators = [key for (key, val) in dmc3_locations.items() if val.adjudicator == True]
