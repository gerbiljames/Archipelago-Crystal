from typing import Dict, Set

from .data import data

LOCATION_GROUPS_A: Dict[str, Set[str]] = {}
ITEM_GROUPS_A: Dict[str, Set[str]] = {}  

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

for item in data.items.values():
    for tag in item.tags:
        if tag not in ITEM_GROUPS_A:
            ITEM_GROUPS_A[tag] = set()
        ITEM_GROUPS_A[tag].add(item.label)

if 'INVALID' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['INVALID']
if 'Tracker' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['Tracker']
if 'Fly' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['Fly']
if 'Badge' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['Badge']
if 'HM' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['HM']
if 'Trap' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['Trap']
if 'JohtoBadge' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['JohtoBadge']
if 'KantoBadge' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['KantoBadge']
if 'TM' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['TM']
if 'Rod' in ITEM_GROUPS_A:
    del ITEM_GROUPS_A['Rod']
