from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data as crystal_data, PokemonData, EvolutionData

if TYPE_CHECKING:
    from . import PokemonCrystalWorld

def randomize_evolution(world: "PokemonCrystalWorld") -> dict[str, str]:
    if not world.options.randomize_evolution: return dict()

    # evolved_pkmn_dict:
    # Keys: Pokemon that can be evolved into.
    # Values: The first Pokemon in id-order that evolves into this Pokemon. Relevant for breeding.
    evolved_pkmn_dict: dict[str, str] = dict()
    type_groupings = generate_type_groupings(world)

    for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[1].id):
        new_evolutions: list[EvolutionData] = []
        valid_evolutions: list[str] = __determine_valid_evolutions(pkmn_data, type_groupings)

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
    # dict[type, list[tuple[pkmn_name, bst]]]
    type_groupings: dict[str, list[tuple[str, PokemonData]]] = dict((pkmn_type, []) for pkmn_type in crystal_data.types)

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        weight = 3 - len(pkmn_data.types)

        for pkmn_type in pkmn_data.types:
            for _ in range(weight):
                type_groupings.get(pkmn_type).append((pkmn_name, pkmn_data))

    return type_groupings


def __determine_valid_evolutions(pkmn_data: PokemonData, type_groupings: dict[str, list[tuple[str, PokemonData]]]):
    valid_evolutions = []
    own_bst = pkmn_data.bst

    for pkmn_type in pkmn_data.types:
        higher_bst_list = filter(lambda x: x[1].bst > own_bst, type_groupings.get(pkmn_type))
        valid_evolutions += map(lambda x: x[0], higher_bst_list)

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

    # Backup 1: Highest BST final evolution within the type
    for pkmn_type in pkmn_data.types:
        backup_evolution_options.extend((k,v) for k,v in type_groupings.get(pkmn_type) if not v.evolutions)

    if backup_evolution_options:
        return [k for (k,v) in [max(backup_evolution_options, key=lambda x: x[1].bst)]]
    else:
        # Backup 2: Higher BST final evolution, dropping the type match
        own_bst = pkmn_data.bst
        all_final_evolutions = {(k,v) for k,v in world.generated_pokemon.items() if not v.evolutions}
        second_backup = [k for k,v in all_final_evolutions if v.bst > own_bst]
        if second_backup:
            return second_backup
        else:
            # Last resort: Just evolve into the final evolution with the highest bst
            return [k for k,v in [max(all_final_evolutions, key=lambda x: x[1].bst)]]

