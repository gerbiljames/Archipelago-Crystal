from typing import TYPE_CHECKING

from .data import FishData, EncounterMon, StaticPokemon, TreeMonData, WildLocation
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
    
    for name, data in world.generated_wild.grass.items(): 
        name=name+"-grass" #some wild locations have the exact same name for grass and water
        all_wilds[name]=data
        all_wild_names.append(name)
    for name, data in world.generated_wild.water.items(): 
        name=name+"-water"
        all_wilds[name]=data
        all_wild_names.append(name)
    world.random.shuffle(all_wild_names)

    temp_pokemons = []
    for wild_name in all_wild_names:
        wild= all_wilds[wild_name]
        new_encounters=[]
        for encounter in wild:
            try: #for some reason " if not temp_pokemons: " was not working in some cases. This is the safest way I could think of
                new_pkmn_name=temp_pokemons.pop(0)
            except:
                for pkmn_name in world.generated_pokemon.keys():
                    temp_pokemons.append(pkmn_name)
                world.random.shuffle(temp_pokemons)
                new_pkmn_name=temp_pokemons.pop(0)
            new_enc = EncounterMon(encounter.level, new_pkmn_name)
            new_encounters.append(new_enc)
        if len(new_encounters)==3:
            world.generated_wild.water[wild_name[:-6]]=new_encounters
        else:
            world.generated_wild.grass[wild_name[:-6]]=new_encounters

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

def find_spawns(world: "PokemonCrystalWorld"):
    pkmn_dict ={}
    for pkmn in world.generated_pokemon.keys():
        pkmn_loc=[]
        for wild_name, wild_data in world.generated_wild.grass.items():
            for encounter in wild_data:
                if pkmn == encounter.pokemon:
                    new_loc = WildLocation("grass", wild_name)
                    pkmn_loc.append(new_loc)                   
        for wild_name, wild_data in world.generated_wild.water.items():
            for encounter in wild_data:
                if pkmn == encounter.pokemon:
                    new_loc = WildLocation("grass", wild_name)
                    pkmn_loc.append(new_loc)
        pkmn_dict[pkmn]=pkmn_loc
    return pkmn_dict

def randomize_static_pokemon(world: "PokemonCrystalWorld"):
    for static_name, pkmn_data in world.generated_static.items():
        world.generated_static[static_name] = pkmn_data._replace(pokemon=get_random_pokemon(world))
