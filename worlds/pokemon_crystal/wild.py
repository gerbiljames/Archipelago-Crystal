from typing import TYPE_CHECKING

from .data import FishData, EncounterMon, StaticPokemon, TreeMonData
from .pokemon import get_random_pokemon

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def randomize_wild_pokemon(world: "PokemonCrystalWorld"):
    world.generated_wooper = get_random_pokemon(world)

    for grass_name, grass_encounters in world.generated_wild.grass.items():
        new_encounters = []
        for encounter in grass_encounters:
            new_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        world.generated_wild.grass[grass_name] = new_encounters

    for water_name, water_encounter in world.generated_wild.water.items():
        new_encounters = []
        for encounter in water_encounter:
            new_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        world.generated_wild.water[water_name] = new_encounters

    for fish_name, fish_area in world.generated_wild.fish.items():
        old_encounters = []
        good_encounters = []
        super_encounters = []
        for encounter in fish_area.old:
            old_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in fish_area.good:
            good_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in fish_area.super:
            super_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))

        world.generated_wild.fish[fish_name] = FishData(
            old_encounters,
            good_encounters,
            super_encounters
        )

    for tree_name, tree_data in world.generated_wild.tree.items():
        new_common = []
        new_rare = []
        for encounter in tree_data.common:
            new_common.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in tree_data.rare:
            new_rare.append(encounter._replace(pokemon=get_random_pokemon(world)))

        world.generated_wild.tree[tree_name] = TreeMonData(
            new_common,
            new_rare
        )


    #this algoritm places every pokemon in dex one by one to any surf or grass slot, when the dex is empty all mons are shuffled back in
def randomize_wilds_catchem(world: "PokemonCrystalWorld"):
    world.generated_wooper = get_random_pokemon(world)

    #first we handle grass and water encounters together
    all_wilds = {}
    all_wild_names = []
    dex_ids=[]
    for name, data in world.generated_wild.grass.items(): 
        all_wilds[name]=data
        all_wild_names.append(name)
    for name, data in world.generated_wild.water.items(): 
        all_wilds[name]=data
        all_wild_names.append(name)
    world.random.shuffle(all_wild_names)
    for wild_name in all_wild_names:
        wild= all_wilds[wild_name]
        new_encounters=[]
        for encounter in wild:
            temp = give_pokemon_dexlist(world, dex_ids)
            dex_ids=temp[1]
            new_encounters.append(encounter._replace(pokemon=temp[0]))
        if len(new_encounters)==3:
            world.generated_wild.water[wild_name]=new_encounters
        else:
            world.generated_wild.grass[wild_name]=new_encounters

    #then fish and trees are handled randomly and same as normal wild randomization (code copied)
    for fish_name, fish_area in world.generated_wild.fish.items():
        old_encounters = []
        good_encounters = []
        super_encounters = []
        for encounter in fish_area.old:
            old_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in fish_area.good:
            good_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in fish_area.super:
            super_encounters.append(encounter._replace(pokemon=get_random_pokemon(world)))

        world.generated_wild.fish[fish_name] = FishData(
            old_encounters,
            good_encounters,
            super_encounters
        )

    for tree_name, tree_data in world.generated_wild.tree.items():
        new_common = []
        new_rare = []
        for encounter in tree_data.common:
            new_common.append(encounter._replace(pokemon=get_random_pokemon(world)))
        for encounter in tree_data.rare:
            new_rare.append(encounter._replace(pokemon=get_random_pokemon(world)))

        world.generated_wild.tree[tree_name] = TreeMonData(
            new_common,
            new_rare
        )


def give_pokemon_dexlist(world: "PokemonCrystalWorld", id_list):
    if len(id_list) == 0:
        id_list=[ i for i in range(1, 252)]
        world.random.shuffle(id_list)
    pkmn_id=id_list.pop(0)
    pkmn
    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        if pkmn_id==pkmn_data.id:
            pkmn=pkmn_name
            break
    return (pkmn, id_list)


def randomize_static_pokemon(world: "PokemonCrystalWorld"):
    for static_name, pkmn_data in world.generated_static.items():
        world.generated_static[static_name] = pkmn_data._replace(pokemon=get_random_pokemon(world))
