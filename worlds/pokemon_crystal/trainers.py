from typing import TYPE_CHECKING

from .data import data as crystal_data
from .moves import get_random_move_from_learnset
from .options import RandomizeTrainerParties, RandomizeLearnsets, BoostTrainerPokemonLevels
from .pokemon import get_random_pokemon, get_random_nezumi
from .utils import get_random_filler_item

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def is_rival_starter_pokemon(trainer_name, trainer_data, index):
    if not trainer_name.startswith("RIVAL"):
        return False
    # last pokemon
    return index == len(trainer_data.pokemon) - 1


def get_last_evolution(pokemon, random):
    """
    Returns the latest possible evolution for a pokemon.
    If there's more than one way down through the evolution line, one is picked at random
    """
    pkmn_data = crystal_data.pokemon[pokemon]
    if not pkmn_data.evolutions:
        return pokemon

    return get_last_evolution(random.choice(pkmn_data.evolutions).pokemon, random)


def randomize_trainers(world: "PokemonCrystalWorld"):
    for trainer_name, trainer_data in world.generated_trainers.items():
        new_party = trainer_data.pokemon
        for i, pkmn_data in enumerate(trainer_data.pokemon):
            new_pokemon = pkmn_data.pokemon
            new_item = pkmn_data.item
            new_moves = pkmn_data.moves

            # If the current pokemon is rival's starter, don't change its evolution line
            if is_rival_starter_pokemon(trainer_name, trainer_data, i):
                if pkmn_data.level >= world.options.force_fully_evolved:
                    new_pokemon = get_last_evolution(new_pokemon, world.random)
            else:
                match_types = None
                if world.options.randomize_trainer_parties == RandomizeTrainerParties.option_match_types:
                    match_types = crystal_data.pokemon[pkmn_data.pokemon].types

                if "LASS_3" in trainer_name:
                    new_pokemon = get_random_nezumi(world.random)
                else:
                    new_pokemon = get_random_pokemon(world, types=match_types,
                                                     force_fully_evolved_at=world.options.force_fully_evolved,
                                                     current_level=pkmn_data.level)
            if pkmn_data.item is not None:
                # If this trainer has items, add an item
                new_item = get_random_filler_item(world.random)
            if len(pkmn_data.moves):
                new_moves = randomize_trainer_pokemon_moves(world, pkmn_data, new_pokemon)
            new_party[i] = pkmn_data._replace(pokemon=new_pokemon, item=new_item, moves=new_moves)
        world.generated_trainers[trainer_name] = world.generated_trainers[trainer_name]._replace(pokemon=new_party)


def vanilla_trainer_movesets(world: "PokemonCrystalWorld"):
    # if trainers parties are vanilla but learnsets are randomized,
    # we need to change the predefined trainer movesets to account for this
    for trainer_name, trainer_data in world.generated_trainers.items():
        if trainer_data.trainer_type not in ["TRAINERTYPE_MOVES", "TRAINERTYPE_ITEM_MOVES"]:
            # if there's no predefined moveset, skip
            continue
        new_party = trainer_data.pokemon
        for i, pkmn_data in enumerate(trainer_data.pokemon):
            new_moves = randomize_trainer_pokemon_moves(world, pkmn_data, pkmn_data.pokemon)
            new_party[i] = pkmn_data._replace(moves=new_moves)
        world.generated_trainers[trainer_name] = world.generated_trainers[trainer_name]._replace(pokemon=new_party)


def randomize_trainer_pokemon_moves(world, pkmn_data, new_pokemon):
    new_moves = pkmn_data.moves
    for i, move in enumerate(pkmn_data.moves):
        # fill out all four moves if start_with_four_moves, else skip empty slots
        if move != "NO_MOVE" or world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves:
            new_move = get_random_move_from_learnset(world, new_pokemon, pkmn_data.level)
            new_moves[i] = new_move
    return new_moves


def boost_trainer_pokemon(world: "PokemonCrystalWorld"):
    # mode 1 multiplies PKMN levels by boost | mode 2 sets the levels to boost
    for trainer_name, trainer_data in world.generated_trainers.items():
        new_party = []
        for trainer_mon in trainer_data.pokemon:
            new_level = trainer_mon.level
            if world.options.boost_trainers == BoostTrainerPokemonLevels.option_percentage_boost:
                new_level = int(trainer_mon.level * (1 + world.options.trainer_level_boost / 100))
                if new_level > 100: new_level = 100
            elif world.options.boost_trainers == BoostTrainerPokemonLevels.option_set_min_level:
                if new_level < world.options.trainer_level_boost:
                    new_level = world.options.trainer_level_boost
            new_party.append(trainer_mon._replace(level=new_level))
        world.generated_trainers[trainer_name] = world.generated_trainers[trainer_name]._replace(pokemon=new_party)
