import json
import os

from ..Locations import dmc3_locations

def main():
    _dict = {k: v.model_dump() for k, v in dmc3_locations.items()}
    out_file = os.path.join(".", "locations.json")
    with open(out_file, 'w') as json_file:
        json.dump(_dict, json_file)


if __name__ == '__main__':
    main()
