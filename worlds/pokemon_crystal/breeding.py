from dataclasses import replace
from typing import TYPE_CHECKING

from .options import RandomizeBreeding, BreedingMethodsRequired
from .utils import pokemon_convert_friendly_to_ids

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def randomize_breeding(world: "PokemonCrystalWorld", preevolutions: dict[str, list[str]]) -> None:
    if not world.options.randomize_breeding: return

    blocklist = pokemon_convert_friendly_to_ids(world, world.options.breeding_blocklist)
    global_breeding_pool = [poke for poke in world.generated_pokemon.keys() if poke not in blocklist]

    if not global_breeding_pool:
        global_breeding_pool = list(world.generated_pokemon.keys())

    if "UNOWN" in global_breeding_pool: global_breeding_pool.remove("UNOWN")

    global_base_pool = [poke for poke in global_breeding_pool if world.generated_pokemon[poke].is_base]

    if not global_base_pool:
        global_base_pool = [poke for poke, data in world.generated_pokemon.items() if data.is_base]

    for pokemon, pokemon_data in world.generated_pokemon.items():
        if not can_breed(world, pokemon): continue

        if world.options.randomize_breeding == RandomizeBreeding.option_completely_random:
            world.generated_pokemon[pokemon] = replace(pokemon_data,
                                                       produces_egg=world.random.choice(global_breeding_pool))

        elif world.options.randomize_breeding == RandomizeBreeding.option_decrease_bst:
            local_breeding_pool = [poke for poke in global_breeding_pool if
                                   world.generated_pokemon[poke].bst <= pokemon_data.bst]

            if not local_breeding_pool:
                local_breeding_pool = global_breeding_pool

            world.generated_pokemon[pokemon] = replace(pokemon_data,
                                                       produces_egg=world.random.choice(local_breeding_pool))
        elif world.options.randomize_breeding == RandomizeBreeding.option_any_base:
            world.generated_pokemon[pokemon] = replace(pokemon_data, produces_egg=world.random.choice(global_base_pool))
        elif world.options.randomize_breeding == RandomizeBreeding.option_line_base:
            local_breeding_pool = list(set(_recursive_get_bases(pokemon, preevolutions)))

            if not local_breeding_pool:
                local_breeding_pool = global_base_pool

            world.generated_pokemon[pokemon] = replace(pokemon_data,
                                                       produces_egg=world.random.choice(local_breeding_pool))


def _recursive_get_bases(pokemon: str, preevolutions: dict[str, list[str]]) -> list[str]:
    if pokemon not in preevolutions: return [pokemon]
    return sum([_recursive_get_bases(poke, preevolutions) for poke in preevolutions[pokemon]], [])


def generate_breeding_data(world: "PokemonCrystalWorld"):
    if not world.options.breeding_methods_required: return

    for pokemon_id, data in world.generated_pokemon.items():
        if pokemon_id not in world.logic.available_pokemon: continue
        if not can_breed(world, pokemon_id): continue
        if (world.options.breeding_methods_required.value == BreedingMethodsRequired.option_any
                and data.gender_ratio in ("GENDER_F100", "GENDER_F0", "GENDER_UNKNOWN")): continue
        world.logic.breeding[data.produces_egg].add(pokemon_id)
        if data.produces_egg == "NIDORAN_F":
            world.logic.breeding["NIDORAN_M"].add(pokemon_id)

    world.logic.available_pokemon.update(world.logic.breeding.keys())


def can_breed(world: "PokemonCrystalWorld", parent: str) -> bool:
    data = world.generated_pokemon[parent]
    if "EGG_DITTO" in data.egg_groups or "EGG_NONE" in data.egg_groups: return False
    return True

def breeding_is_randomized(world: "PokemonCrystalWorld") -> bool:
    return (world.options.randomize_evolution and world.options.randomize_breeding) or \
            world.options.randomize_breeding.value > RandomizeBreeding.option_line_base
