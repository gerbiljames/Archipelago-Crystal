import json
import os
from dataclasses import asdict

from worlds.dmc3.Locations import dmc3_locations, BaseLocationData


def main():
    _dict = {k: asdict(v) for k, v in (dmc3_locations|{"Mission #20 Complete": BaseLocationData(mission_number=20, room_number=0, default_item=0x00)}).items()}
    out_file = os.path.join("../test", "locations.json")
    with open(out_file, 'w') as json_file:
        json.dump(_dict, json_file)


if __name__ == '__main__':
    main()
