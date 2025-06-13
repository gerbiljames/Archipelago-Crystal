from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data as crystal_data, LearnsetData, TMHMData
from .options import RandomizeLearnsets, RandomizeMoveValues

if TYPE_CHECKING:
    from . import PokemonCrystalWorld

MOVE_POWER_RATIO = {
    "BARRAGE": 3,
    "DOUBLESLAP": 3,
    "TRIPLE_KICK": 3,
    "BONEMERANG": 2,
    "COMET_PUNCH": 3,
    "DOUBLE_KICK": 2,
    "FURY_ATTACK": 3,
    "FURY_SWIPES": 3,
    "PIN_MISSILE": 3,
    "TWINEEDLE": 2,
    "SPIKE_CANNON": 3,
    "BONE_RUSH": 3
}

BAD_DAMAGING_MOVES = ["EXPLOSION", "SELFDESTRUCT", "STRUGGLE", "SNORE", "DREAM_EATER"]

HM_COMPAT_TMS = ["HEADBUTT", "ROCK_SMASH"]


def randomize_learnset(world: "PokemonCrystalWorld", pkmn_name):
    pkmn_data = world.generated_pokemon[pkmn_name]
    learn_levels = []
    new_learnset = []
    for move in pkmn_data.learnset:
        if move.move != "NO_MOVE":
            learn_levels.append(move.level)
        elif world.options.randomize_learnsets == RandomizeLearnsets.option_start_with_four_moves:
            learn_levels.insert(0, 1)

    for level in learn_levels:
        if world.options.metronome_only:
            new_learnset.append(LearnsetData(level, "METRONOME"))
        else:
            move_type = None

            if world.options.learnset_type_bias > -1:  # checks if user put an option for Move Type bias (default is -1)
                pkmn_types = pkmn_data.types
                if world.random.randint(1, 100) <= world.options.learnset_type_bias:  # rolls for the chance
                    # chooses one of the pokemons types to give to move generation function
                    move_type = world.random.choice(pkmn_types)
                else:  # chooses one of the types other than the pokemons to give to move generation function
                    rem_types = [type for type in crystal_data.types if type not in pkmn_types]
                    move_type = world.random.choice(rem_types)
            new_learnset.append(
                LearnsetData(level, get_random_move(world, move_type=move_type, cur_learnset=new_learnset)))

    if not world.options.metronome_only:
        # All moves available at Lv.1 that do damage (and don't faint the user)
        start_attacking = [learnset for learnset in new_learnset if
                           world.generated_moves[learnset.move].power > 0
                           and learnset.move not in BAD_DAMAGING_MOVES
                           and learnset.level == 1]

        if not start_attacking:  # if there are no attacking moves at Lv.1, add one
            new_learnset[0] = LearnsetData(1, get_random_move(world,
                                                              attacking=True))  # overwrites whatever the 1st move is

    return new_learnset


def get_random_move(world: "PokemonCrystalWorld", move_type=None, attacking=None, cur_learnset=None,
                    enforce_blocklist=True):
    if not cur_learnset:
        cur_learnset = []

    existing_moves = [entry.move for entry in cur_learnset]  # pulls the names of all the moves in current learnset

    move_pool = [move_name for move_name, move_data in world.generated_moves.items() if
                 not move_data.is_hm
                 # exclude beat up as it can softlock the game if an enemy trainer uses it
                 and move_name not in ("STRUGGLE", "BEAT_UP", "NO_MOVE")
                 and move_name not in existing_moves
                 and (not move_type or move_data.type == move_type)]

    if attacking is not None:
        move_pool = [move_name for move_name in move_pool if world.generated_moves[move_name].power > 0
                     and move_name not in BAD_DAMAGING_MOVES
                     and move_name not in existing_moves]

    # remove every move from move_pool that is in the blocklist
    if enforce_blocklist and world.blocklisted_moves:
        move_pool = [move_name for move_name in move_pool if
                     move_name not in world.blocklisted_moves]

    if move_pool:
        return world.random.choice(move_pool)
    elif move_type:
        return get_random_move(world)
    else:
        return get_random_move(world, enforce_blocklist=False)


def get_tmhm_compatibility(world: "PokemonCrystalWorld", pkmn_name):
    pkmn_data = world.generated_pokemon[pkmn_name]
    tm_value = world.options.tm_compatibility.value
    hm_value = world.options.hm_compatibility.value
    tmhms = []
    for tm_name, tm_data in world.generated_tms.items():
        use_value = hm_value if tm_data.is_hm or tm_name in HM_COMPAT_TMS else tm_value
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
    if not world.options.randomize_tm_moves and not world.options.metronome_only: return

    ignored_moves = ["ROCK_SMASH", "NO_MOVE", "STRUGGLE", "HEADBUTT"]
    if world.options.dexsanity:
        ignored_moves.append("SWEET_SCENT")
    global_move_pool = [move_data for move_name, move_data in world.generated_moves.items() if
                        not move_data.is_hm
                        and move_name not in ignored_moves]

    filtered_move_pool = [move for move in global_move_pool if move.id not in world.blocklisted_moves]

    world.random.shuffle(global_move_pool)
    world.random.shuffle(filtered_move_pool)

    for tm_name, tm_data in world.generated_tms.items():
        if tm_data.is_hm or tm_name in ignored_moves:
            continue
        if world.options.metronome_only:
            new_move = world.generated_moves["METRONOME"]
        elif not filtered_move_pool:
            new_move = global_move_pool.pop()
        else:
            new_move = filtered_move_pool.pop()
            global_move_pool.remove(new_move)
        world.generated_tms[tm_name] = TMHMData(new_move.id, tm_data.tm_num, new_move.type, False, new_move.rom_id)


def get_random_move_from_learnset(world: "PokemonCrystalWorld", pokemon, level):
    move_pool = [learn_move.move for learn_move in world.generated_pokemon[pokemon].learnset if
                 learn_move.level <= level and learn_move.move != "NO_MOVE"]
    # double learnset pool to dilute HMs slightly
    # exclude beat up as it can softlock the game if an enemy trainer uses it
    move_pool.extend(world.generated_tms[tm].id for tm in world.generated_pokemon[pokemon].tm_hm if
                     world.generated_tms[tm].id != "BEAT_UP")
    return world.random.choice(move_pool)


def randomize_move_values(world: "PokemonCrystalWorld"):
    if not world.options.randomize_move_values: return

    acc100 = 70  # Moves have a 70% chance to get 100% accuracy
    for move_name, move_data in world.generated_moves.items():
        if move_name in ("NO_MOVE", "CURSE", "DRAGON_RAGE", "SONICBOOM"):
            continue
        new_power = move_data.power
        new_acc = move_data.accuracy
        new_pp = move_data.pp
        if new_power > 1:
            if world.options.randomize_move_values.value == RandomizeMoveValues.option_restricted:
                new_power = int(new_power * (world.random.random() + 0.5))
                if new_power > 255: new_power = 255
                new_power //= MOVE_POWER_RATIO.get(move_name, 1)
                new_pp = new_pp + world.random.choice([-10, -5, 0, 5, 10])
                if new_pp < 5: new_pp = 5
                if new_pp > 40: new_pp = 40
            else:
                new_power = world.random.randint(20, 150)
                new_power //= MOVE_POWER_RATIO.get(move_name, 1)
                new_pp = world.random.randint(5, 40)

            if world.options.randomize_move_values.value == RandomizeMoveValues.option_full:
                if world.random.randint(1, 100) <= acc100:
                    new_acc = 100
                else:
                    # 30 is 76,5 so actual lowest accuracy is a bit lower than 30
                    new_acc = world.random.randint(30, 100)

        world.generated_moves[move_name] = replace(
            world.generated_moves[move_name],
            power=new_power,
            accuracy=new_acc,
            pp=new_pp
        )


def randomize_move_types(world: "PokemonCrystalWorld"):
    if not world.options.randomize_move_types: return

    for move_name, move_data in world.generated_moves.items():
        if move_name in ("NO_MOVE", "CURSE"):
            continue
        new_type = world.random.choice(crystal_data.types)
        world.generated_moves[move_name] = replace(
            world.generated_moves[move_name],
            type=new_type
        )
