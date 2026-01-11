import typing

from BaseClasses import Location


number_buttons_per_cluster = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 2,
    8: 1,
    9: 1,
    10: 2,
    11: 1,
    12: 1,
    13: 1,
    14: 1,
    15: 1,
    16: 1,
    17: 1,
    18: 2,
    19: 1,
    20: 1,
    21: 1,
    22: 1,
    23: 1,
    24: 1,
    25: 1,
    26: 3,
    27: 1,
    28: 2,
    29: 1,
    30: 1,
    31: 1,        
}

number_platforms_per_cluster = {
    1: 7,
    2: 7,
    3: 9,
    4: 9,
    5: 6,
    6: 5,
    7: 4,
    8: 11,
    9: 10,
    10: 9,
    11: 8,
    12: 5,
    13: 4,
    14: 3,
    15: 4,
    16: 3,
    17: 4,
    18: 11,
    19: 5,
    20: 10,
    21: 15,
    22: 2,
    23: 4,
    24: 9,
    25: 8,
    26: 14,
    27: 8,
    28: 20,
    29: 18,
    30: 14,
    31: 5,
}

platforms_with_button_on_them = [
    (1,1),
    (2,3),
    (3,2),
    (4,4),
    (5,1),
    (6,1),
    (7,1),
    (7,2),
    (8,11),
    (9,6),
    (10,1),
    (10,3),
    (11,8),
    (12,1),
    (13,1),
    (14,3),
    (15,2),
    (16,1),
    (17,2),
    (18,2),
    (18,1),
    (19,5),
    (20,7),
    (21,8),
    (22,2),
    (23,3),
    (24,1),
    (25,5),
    (26,12),
    (26,7),
    (26,9),
    (27,8),
    (28,18),
    (28,8),
    (29,4),
    (30,12),
    (31,2),
]

starting_platform = (1,2)

cube_clusters = [           
    (4,1),
    (7,1),
    (8,1),
    (8,2),
    (9,1),
    (10,1),
    (12,1),
    (13,1),
    (14,1),
    (18,1),
    (21,1),
    (21,2),
    (23,1),
    (27,1),
    (28,1),
    (29,1),
    (29,2),
    (30,1),
]
    
class LocData(typing.NamedTuple):
    id: int
    main_nr: int
    sub_nr: int
    type_of_check: str = "Platform"
    minigame: str = ""
    
class RefunctLocation(Location):
    game: str = "Refunct"

location_table = {
    **{f"Platform {i}-{j}": LocData(10010000 + i * 100 + j, i, j, "Platform", None)
       for i in range(1, 31) for j in range(1, number_platforms_per_cluster[i] + 1)},
    **{f"Vanilla Minigame: Button {i}-{j}": LocData(10020000 + i * 100 + j, i, j, "Minigame", "Vanilla")
       for i in range(1, 32) for j in range(1, number_buttons_per_cluster[i] + 1)},
    **{f"Seeker Minigame: Platform #{i}": LocData(10030000 + i, i, None, "Minigame", "Seeker")
       for i in range(1, 11)},
    **{f"Button Galore Minigame: Button {i}-{j}": LocData(10040000 + i * 100 + j, i, j, "Minigame", "Button Galore")
       for i in range(1, 32) for j in range(1, number_buttons_per_cluster[i] + 1)},
    **{f"OG Randomizer Minigame: Button {i}-{j}": LocData(10050000 + i * 100 + j, i, j, "Minigame", "OG Randomizer")
       for i in range(1, 32) for j in range(1, number_buttons_per_cluster[i] + 1)},
    **{f"Cube {i}-{j}": LocData(10060000 + i * 100 + j, i, j, "Cube", None)
       for (i, j) in cube_clusters},
    
}
    
platforms_with_button_ids = []
platforms_without_button_ids = []
for cluster, num_platforms in number_platforms_per_cluster.items():
    for platform in range(1, num_platforms + 1):
        if (cluster, platform) not in platforms_with_button_on_them:
            platforms_without_button_ids.append(10010000 + cluster * 100 + platform)
        else:
            platforms_with_button_ids.append(10010000 + cluster * 100 + platform)