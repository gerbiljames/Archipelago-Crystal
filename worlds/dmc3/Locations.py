# noinspection PyPackageRequirements
from pydantic import BaseModel

from BaseClasses import Location

location_descriptions = {
    "Blue Orb Fragment #1": "Mission 3 before entering Cerberus' boss fight",
}


class BaseLocationData(BaseModel):
    mission_number: int # Mission Number, 0 if irrelevant
    room_number: int # Room Number
    secret: bool = False # Secret mission?
    default_item: int # Default Item
    offset: int = 0x0 # Offset



class DMC3Location(Location):
    game = "Devil May Cry 3"

    def __init__(self, player: int, name="", code=None, parent=None) -> None:
        super(DMC3Location, self).__init__(player, name, code, parent)
        self.event = code is None
