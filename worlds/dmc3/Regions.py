from typing import TypedDict


# class ConnectionDict(TypedDict, total=False):
#     target: str
#
#
# class RegionDict(TypedDict, total=False):
#     name: str
#     connections: List[ConnectionDict]
#
#
# class Mission(NamedTuple):
#     name: str
#     secret_num: int = 0

class Mission(TypedDict):
    secret: list
    #locations: list = []


# regions: Dict[int, Mission] = {
#     1: Mission()
# }

dmc3_regions: dict[int, Mission] = {
    # First number is mission number, 2nd is secret mission indexes. 0 if the mission doesn't have one
    1: Mission(secret=[0]),
    2: Mission(secret=[0]),
    3: Mission(secret=[1]),
    4: Mission(secret=[0]),
    5: Mission(secret=[2]),
    6: Mission(secret=[0]),
    7: Mission(secret=[3]),
    8: Mission(secret=[4]),
    9: Mission(secret=[5]),
    10: Mission(secret=[6]),
    11: Mission(secret=[7]),
    12: Mission(secret=[0]),
    13: Mission(secret=[8, 9]),
    14: Mission(secret=[0]),
    15: Mission(secret=[0]),
    16: Mission(secret=[10]),
    17: Mission(secret=[11]),
    18: Mission(secret=[12]),
    19: Mission(secret=[0]),
    20: Mission(secret=[0])
}


# dmc3_regions: dict[int, Mission] = {
#     # First number is mission number, 2nd is secret mission indexes. 0 if the mission doesn't have one
#     1: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 1]},
#     2: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 2]},
#     3: {[1], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 3]},
#     4: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 4]},
#     5: {[2], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 5]},
#     6: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 6]},
#     7: {[3], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 7]},
#     8: {[4], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 8]},
#     9: {[5], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 9]},
#     10: {[6], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 10]},
#     11: {[7], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 11]},
#     12: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 12]},
#     13: {[8, 9], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 13]},
#     14: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 14]},
#     15: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 15]},
#     16: {[10], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 16]},
#     17: {[11], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 17]},
#     18: {[12], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 18]},
#     19: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 19]},
#     20: {[0], [loc for loc in dmc3_locations if dmc3_locations[loc][1] == 20]}
#
# }
