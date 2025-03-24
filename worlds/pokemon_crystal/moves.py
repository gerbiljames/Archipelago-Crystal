import copy
from typing import TYPE_CHECKING

from .data import data as crystal_data, LearnsetData, TMHMData
from .options import RandomizeLearnsets

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_learnset(world: "PokemonCrystalWorld", pkmn_name):
    pkmn_data = world.generated_pokemon[pkmn_name]
    learn_levels = []
    new_learnset = []
    data_types = copy.deepcopy(crystal_data.types)
    for move in pkmn_data.learnset:
        if move.move != "NO_MOVE":
            learn_levels.append(move.level)
        elif world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves:
            learn_levels.insert(0, 1)

    for level in learn_levels:
        move_type = None

        if world.options.learnset_type_bias > -1:  # checks if user put an option for Move Type bias (default is -1)
            pkmn_types = pkmn_data.types
            if world.random.randint(1, 100) <= world.options.learnset_type_bias:  # rolls for the chance
                # chooses one of the pokemons types to give to move generation function
                move_type = world.random.choice(pkmn_types)
            else:  # chooses one of the types other than the pokemons to give to move generation function
                rem_types = [type for type in data_types if type not in pkmn_types]
                move_type = world.random.choice(rem_types)
        new_learnset.append(LearnsetData(level, get_random_move(world, move_type=move_type, cur_learnset=new_learnset)))

    # All moves available at Lv.1 that do damage (and don't faint the user)
    start_attacking = [learnset for learnset in new_learnset if
                       world.generated_moves[learnset.move].power > 0
                       #This list is the damaging moves that should be ignored for checking starting attacking moves
                       and learnset.move not in ["EXPLOSION", "SELFDESTRUCT", "STRUGGLE", "SNORE","DREAM_EATER"] 
                       and learnset.level == 1]

    if not len(start_attacking):  # if there are no attacking moves at Lv.1, add one
        new_learnset[0] = LearnsetData(1, get_random_move(world, attacking=True)) #overwrites whatever the 1st move is

    return new_learnset


def get_random_move(world: "PokemonCrystalWorld", move_type=None, attacking=None, cur_learnset=None,
                    enforce_blocklist=True):
    if not cur_learnset:
        cur_learnset = []

    existing_moves = [entry.move for entry in cur_learnset]  # pulls the names of all the moves in current learnset

    move_pool = [move_name for move_name, move_data in crystal_data.moves.items() if
                 not move_data.is_hm
                 # exclude beat up as it can softlock the game if an enemy trainer uses it
                 and move_name not in ["STRUGGLE", "BEAT_UP", "NO_MOVE"]
                 and move_name not in existing_moves
                 and (not move_type or move_data.type == move_type)]
    
    if attacking is not None:
        move_pool = [move_name for move_name in move_pool if crystal_data.moves[move_name].power > 0
                     and move_name not in existing_moves]

    # remove every move from move_pool that is in the blocklist
    if enforce_blocklist and world.options.move_blocklist:
        move_pool = [move_name for move_name in move_pool if
                     move_name not in world.options.move_blocklist]

    if move_pool:
        return world.random.choice(move_pool)
    else:
        return get_random_move(world, enforce_blocklist=False)


def get_tmhm_compatibility(world: "PokemonCrystalWorld", pkmn_name):
    pkmn_data = world.generated_pokemon[pkmn_name]
    tm_value = world.options.tm_compatibility.value
    hm_value = world.options.hm_compatibility.value
    tmhms = []
    for tm_name, tm_data in world.generated_tms.items():
        use_value = hm_value if tm_data.is_hm else tm_value
        # if the value is 0, use vanilla compatibility
        if use_value == 0:
            if tm_name in pkmn_data.tm_hm:
                tmhms.append(tm_name)
                continue
        # double chance if types match
        if tm_data.type in pkmn_data.types:
            use_value = use_value * 2
        if world.random.randint(0, 99) < use_value:
            tmhms.append(tm_name)
    return tmhms


def randomize_tms(world: "PokemonCrystalWorld"):
  
    global_move_pool = [move_data for move_name, move_data in world.generated_moves.items() if
                 not move_data.is_hm and move_name not in ["ROCK_SMASH", "NO_MOVE", "STRUGGLE"]]
  
    filtered_move_pool = []

    # remove every move from filtered_move_pool that is in the blocklist

    if world.options.move_blocklist:
        filtered_move_pool = [move for move in global_move_pool if move.name not in world.options.move_blocklist]

    world.random.shuffle(global_move_pool)
    world.random.shuffle(filtered_move_pool)

    for tm_name, tm_data in world.generated_tms.items():
        if tm_data.is_hm or tm_name == "ROCK_SMASH":
            continue
        if not filtered_move_pool:
            new_move = global_move_pool.pop()
        else:
            new_move = filtered_move_pool.pop()
            global_move_pool.remove(new_move)
        world.generated_tms[tm_name] = TMHMData(tm_data.tm_num, new_move.type, False, new_move.id)


def get_random_move_from_learnset(world: "PokemonCrystalWorld", pokemon, level):
    move_pool = [move.move for move in world.generated_pokemon[pokemon].learnset if
                 move.level <= level and move.move != "NO_MOVE"]
    # double learnset pool to dilute HMs slightly
    # exclude beat up as it can softlock the game if an enemy trainer uses it
    move_pool += move_pool + [move for move in world.generated_pokemon[pokemon].tm_hm if move != "BEAT_UP"]
    return world.random.choice(move_pool)

def randomize_move_values(world: "PokemonCrystalWorld"):
    acc100 = 70 # I need a value for this I can take this from YAML
    for move_name, move_data in world.generated_moves.items():
        if move_name in ["NO_MOVE", "CURSE"]:
            continue
        new_power = move_data.power
        new_acc = move_data.accuracy
        new_pp = move_data.pp
        if new_power > 1: #dont touch status OHKO or Special Calculated Damage Moves POWER and ACCURACY (I will change this later)
            if world.options.randomize_move_values == 1:
                new_power = int(new_power*(world.random.random()+0.5))
                if new_power > 255: new_power = 255
                new_pp=new_pp+world.random.choice([-10,-5,0,5,10])
                if new_pp < 5: new_pp = 5
                if new_pp > 40: new_pp = 40
            else:
                new_power = world.random.randint(20,150)
                new_pp =world.random.randint(5,40)
            if world.options.randomize_move_values == 3: 
                if world.random.randint(1,100) <= acc100:
                    new_acc = 255
                else:
                    new_acc = world.random.randint(76,255) # 30 is 76,5 so actual lowest accuracy is a bit lower than 30
        world.generated_moves[move_name]=world.generated_moves[move_name]._replace(power=new_power,accuracy=new_acc,pp=new_pp)

def randomize_move_types(world: "PokemonCrystalWorld"):
    data_types = copy.deepcopy(crystal_data.types)
    for move_name, move_data in world.generated_moves.items():
        if move_name in ["NO_MOVE", "CURSE"]:
            continue
        new_type = world.random.choice(data_types)
        world.generated_moves[move_name]=world.generated_moves[move_name]._replace(type=new_type)