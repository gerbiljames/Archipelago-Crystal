from .data import data

ALL_UNOWN = [
    f"UNOWN_{char}" for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
]

LEGENDARY_POKEMON = {"Articuno", "Zapdos", "Moltres", "Mewtwo", "Mew", "Entei", "Raikou", "Suicune", "Celebi",
                     "Lugia", "Ho-Oh"}

NON_LEGENDARY_POKEMON = {pokemon.friendly_name for pokemon in data.pokemon.values() if
                         pokemon.friendly_name not in LEGENDARY_POKEMON}

VANILLA_STARTERS = (
    ("CYNDAQUIL", "QUILAVA", "TYPHLOSION"),
    ("TOTODILE", "CROCONAW", "FERALIGATR"),
    ("CHIKORITA", "BAYLEEF", "MEGANIUM"),
)

# Phone-trainer swarms. Each is a single-slot synthetic encounter (see data.py) attached to the
# normal-encounter host region. The ROM synthesizes the actual in-game encounter from patchpoints
# (engine/overworld/wildmons.asm, engine/events/fish.asm).
#   swarm region_id -> (host map for grass: wild_encounters.grass key,
#                       host group for fishing: wild_encounters.fishing key)
SWARM_REGISTRATIONS = {
    "Dunsparce_Swarm": {"grass_host": "DARK_CAVE_VIOLET_ENTRANCE", "fishing_host": None},
    "Yanma_Swarm":     {"grass_host": "ROUTE_35",                  "fishing_host": None},
    "Qwilfish_Swarm":  {"grass_host": None,                        "fishing_host": "Qwilfish"},
}

# Swarm region_id -> registration event placed in the trainer's home AP region (regions.json).
# Swarm logic gates on state.has(event) rather than state.can_reach_region.
SWARM_TRAINER_REGISTRATION = {
    "Dunsparce_Swarm": "EVENT_REGISTERED_ANTHONY",
    "Yanma_Swarm":     "EVENT_REGISTERED_ARNIE",
    "Qwilfish_Swarm":  "EVENT_REGISTERED_RALPH",
}
