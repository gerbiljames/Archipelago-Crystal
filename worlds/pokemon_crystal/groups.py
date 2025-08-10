from typing import Dict, Set

from .data import data

LOCATION_GROUPS_A: Dict[str, Set[str]] = {}
for location in data.locations.values():
    for tag in location.tags:
        if tag not in LOCATION_GROUPS_A:
            LOCATION_GROUPS_A[tag] = set()
        LOCATION_GROUPS_A[tag].add(location.label)

if 'VanillaClairOn' in LOCATION_GROUPS_A:
    del LOCATION_GROUPS_A['VanillaClairOn']
if 'RequiresSaffronGatehouses' in LOCATION_GROUPS_A:
    del LOCATION_GROUPS_A['RequiresSaffronGatehouses']
if 'VanillaClairOff' in LOCATION_GROUPS_A:
    del LOCATION_GROUPS_A['VanillaClairOff']        

# # item_groups: Dict[str, Set[str]] = {}        
# # for item in data.items.values():
    # # for tag in item.tags:
        # # if tag not in item_groups:
            # # item_groups[tag] = set()
        # # item_groups[tag].add(item.name)

# The same can be done for item groups, if there's a need. Just have to create and import it under a different name than the one in items.py and then merge the two.