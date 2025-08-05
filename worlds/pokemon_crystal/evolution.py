from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data as crystal_data, PokemonData, EvolutionData
from .options import RandomizeEvolution

if TYPE_CHECKING:
    from . import PokemonCrystalWorld

def randomize_evolution(world: "PokemonCrystalWorld") -> dict[str, str]:
    if not world.options.randomize_evolution: return dict()

    # evolved_pkmn_dict:
    # Keys: Pokemon that can be evolved into.
    # Values: The first Pokemon in id-order that evolves into this Pokemon. Relevant for breeding.
    evolved_pkmn_dict: dict[str, str] = dict()

    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        type_groupings = generate_type_groupings(world)
    else:
        # skip populating the type groupings when not relevant
        type_groupings = dict()

    for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[1].id):
        if not pkmn_data.evolutions:
            continue

        new_evolutions: list[EvolutionData] = []
        valid_evolutions: list[str] = __determine_valid_evolutions(world, pkmn_data, type_groupings)

        if not valid_evolutions:
            valid_evolutions = __handle_no_valid_evolution(pkmn_data, type_groupings, world)

        for evolution in pkmn_data.evolutions:
            new_evo_pkmn = world.random.choice(valid_evolutions)
            if new_evo_pkmn not in evolved_pkmn_dict:
                evolved_pkmn_dict[new_evo_pkmn] = pkmn_name

            new_evolutions.append(
                replace(
                    evolution,
                    pokemon=new_evo_pkmn
                )
            )

        world.generated_pokemon[pkmn_name] = replace(
            world.generated_pokemon[pkmn_name],
            evolutions=new_evolutions,
        )

    __update_base(evolved_pkmn_dict.keys(), world)

    return evolved_pkmn_dict

def generate_type_groupings(world: "PokemonCrystalWorld"):
    # dict[type, list[tuple[pkmn_name, pkmn_data]]]
    type_groupings: dict[str, list[tuple[str, PokemonData]]] = dict((pkmn_type, []) for pkmn_type in crystal_data.types)

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        weight = 3 - len(pkmn_data.types)

        for pkmn_type in pkmn_data.types:
            for _ in range(weight):
                type_groupings.get(pkmn_type).append((pkmn_name, pkmn_data))

    return type_groupings

def __determine_valid_evolutions(world: "PokemonCrystalWorld", pkmn_data, type_groupings):
    valid_evolutions = []
    own_bst = pkmn_data.bst

    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        for pkmn_type in pkmn_data.types:
            valid_evolutions.extend(name for name,data in type_groupings.get(pkmn_type) if data.bst > own_bst)
    else:
        valid_evolutions.extend(name for name,data in world.generated_pokemon.items() if data.bst > own_bst)

    return valid_evolutions

def __update_base(evolved_pkmn, world: "PokemonCrystalWorld"):
    for pkmn_name in world.generated_pokemon.keys():
        world.generated_pokemon[pkmn_name] = replace(
            world.generated_pokemon[pkmn_name],
            is_base = pkmn_name not in evolved_pkmn,
        )

def __handle_no_valid_evolution(pkmn_data: PokemonData,
                                type_groupings: dict[str, list[tuple[str, PokemonData]]],
                                world: "PokemonCrystalWorld"
                                ) -> list[str]:
    backup_evolution_options: list[tuple[str, PokemonData]] = []
    all_final_evolutions = [(k, v) for k, v in world.generated_pokemon.items() if not v.evolutions]

    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        # Type backup: Highest BST final evolution within the type
        for pkmn_type in pkmn_data.types:
            backup_evolution_options.extend((k,v) for k,v in type_groupings.get(pkmn_type) if not v.evolutions)

        if backup_evolution_options:
            max_bst_final = max(backup_evolution_options, key=lambda x: x[1].bst)
            return [max_bst_final[0]]
        else:
            # Type backup 2: Higher BST final evolution, dropping the type match
            own_bst = pkmn_data.bst

            second_backup = [name for name,data in all_final_evolutions if data.bst > own_bst]
            if second_backup:
                return second_backup

    # Last resort: Just evolve into the final evolution with the highest bst
    max_bst_final: tuple[str, PokemonData] = max(all_final_evolutions, key=lambda x: x[1].bst)
    return [max_bst_final[0]]

