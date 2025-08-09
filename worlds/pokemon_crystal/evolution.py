import logging
from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data as crystal_data, PokemonData, EvolutionData
from .options import RandomizeEvolution
from .pokemon import pokemon_convert_friendly_to_ids

__ALL_KEY = "all"
__FINAL_KEY = "final"

if TYPE_CHECKING:
    from . import PokemonCrystalWorld

def randomize_evolution(world: "PokemonCrystalWorld") -> dict[str, str]:
    if not world.options.randomize_evolution: return dict()

    # evolved_pkmn_dict:
    # Keys: Pokemon that can be evolved into.
    # Values: The first Pokemon in id-order that evolves into this Pokemon. Relevant for breeding.
    evolved_pkmn_dict: dict[str, str] = dict()

    # dict[key, list[tuple[pkmn_name, pkmn_data]]]
    pkmn_groupings = generate_pokemon_groupings(world)

    for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[1].id):
        if not pkmn_data.evolutions:
            continue

        new_evolutions: list[EvolutionData] = []
        valid_evolutions: list[str] = __determine_valid_evolutions(world, pkmn_data, pkmn_groupings)

        if not valid_evolutions:
            valid_evolutions = __handle_no_valid_evolution(world, pkmn_data, pkmn_groupings)

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

def generate_pokemon_groupings(world: "PokemonCrystalWorld") -> dict[str, list[tuple[str, PokemonData]]]:
    blocklist = pokemon_convert_friendly_to_ids(world, world.options.evolution_blocklist.value)
    unblocked_pkmn = [(name, data) for name, data in world.generated_pokemon.items() if name not in blocklist]

    all_final_evolutions = [(k, v) for k, v in unblocked_pkmn if not v.evolutions]
    if not all_final_evolutions:
        # If all final evolutions are blocklisted, throw the blocklist in the trash
        logging.warning(
            "Pokemon Crystal: Every final evolution is blocklisted for player %s. Ignoring the blocklist.",
            world.player_name)
        unblocked_pkmn = [(name, data) for name, data in world.generated_pokemon.items()]
        all_final_evolutions = [(k, v) for k, v in world.generated_pokemon.items() if not v.evolutions]

    pkmn_groupings = dict(all=unblocked_pkmn, final=all_final_evolutions)
    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        pkmn_groupings = generate_type_groupings(pkmn_groupings)

    return pkmn_groupings


def generate_type_groupings(basic_groupings: dict[str, list[tuple[str, PokemonData]]]) -> dict[str, list[tuple[str, PokemonData]]]:
    type_groupings = dict((pkmn_type, []) for pkmn_type in crystal_data.types)

    for pkmn_name, pkmn_data in basic_groupings.get(__ALL_KEY):
        weight = 3 - len(pkmn_data.types)

        for pkmn_type in pkmn_data.types:
            for _ in range(weight):
                type_groupings.get(pkmn_type).append((pkmn_name, pkmn_data))

    return type_groupings | basic_groupings

def __determine_valid_evolutions(world: "PokemonCrystalWorld", pkmn_data, pkmn_groupings):
    valid_evolutions = []
    own_bst = pkmn_data.bst

    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        for pkmn_type in pkmn_data.types:
            valid_evolutions.extend(name for name,data in pkmn_groupings.get(pkmn_type) if data.bst > own_bst)
    else:
        valid_evolutions.extend(name for name,data in pkmn_groupings.get(__ALL_KEY) if data.bst > own_bst)

    return valid_evolutions

def __update_base(evolved_pkmn, world: "PokemonCrystalWorld"):
    for pkmn_name in world.generated_pokemon.keys():
        world.generated_pokemon[pkmn_name] = replace(
            world.generated_pokemon[pkmn_name],
            is_base = pkmn_name not in evolved_pkmn,
        )

def __handle_no_valid_evolution(world: "PokemonCrystalWorld",
                                pkmn_data: PokemonData,
                                pkmn_groupings: dict[str, list[tuple[str, PokemonData]]]
                                ) -> list[str]:
    backup_evolution_options: list[tuple[str, PokemonData]] = []

    if world.options.randomize_evolution == RandomizeEvolution.option_match_a_type:
        # Type backup: Highest BST final evolution within the type
        for pkmn_type in pkmn_data.types:
            backup_evolution_options.extend((k,v) for k,v in pkmn_groupings.get(pkmn_type) if not v.evolutions)

        if backup_evolution_options:
            max_bst_final = max(backup_evolution_options, key=lambda x: x[1].bst)
            return [max_bst_final[0]]
        else:
            # Type backup 2: Higher BST final evolution, dropping the type match
            own_bst = pkmn_data.bst

            second_backup = [name for name,data in pkmn_groupings.get(__FINAL_KEY) if data.bst > own_bst]
            if second_backup:
                return second_backup

    # Last resort: Just evolve into the final evolution with the highest bst
    max_bst_final: tuple[str, PokemonData] = max(pkmn_groupings.get(__FINAL_KEY), key=lambda x: x[1].bst)
    return [max_bst_final[0]]

