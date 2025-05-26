from typing import TYPE_CHECKING, Dict

from BaseClasses import Location, Region, LocationProgressType
from .data import data, POKEDEX_OFFSET
from .options import Goal
from .utils import evolution_in_logic, evolution_location_name

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


class PokemonCrystalLocation(Location):
    game: str = "Pokemon Crystal"
    rom_address: int | None
    default_item_code: int | None
    flag: int | None
    tags: frozenset[str]

    def __init__(
            self,
            player: int,
            name: str,
            parent: Region | None = None,
            flag: int | None = None,
            rom_address: int | None = None,
            default_item_value: int | None = None,
            tags: frozenset[str] = frozenset(),
            progress_type: LocationProgressType = LocationProgressType.DEFAULT
    ) -> None:
        super().__init__(player, name, flag, parent)
        self.default_item_code = default_item_value
        self.rom_address = rom_address
        self.tags = tags
        self.progress_type = progress_type


def create_locations(world: "PokemonCrystalWorld", regions: dict[str, Region]) -> None:
    exclude = set()
    if not world.options.randomize_hidden_items:
        exclude.add("Hidden")
    if not world.options.randomize_pokegear:
        exclude.add("Pokegear")
    if not world.options.trainersanity:
        exclude.add("Trainersanity")
    if not world.options.randomize_badges:
        exclude.add("Badge")
    if not world.options.randomize_berry_trees:
        exclude.add("BerryTree")
    if not world.options.saffron_gatehouse_tea:
        exclude.add("RequiresSaffronGatehouses")
    if world.options.vanilla_clair:
        exclude.add("VanillaClairOff")
    else:
        exclude.add("VanillaClairOn")

    always_include = {"KeyItem"}

    for region_name, region_data in data.regions.items():
        if region_name in regions:
            region = regions[region_name]
            filtered_locations = [loc for loc in region_data.locations if
                                  always_include.intersection(set(data.locations[loc].tags)) or
                                  not exclude.intersection(set(data.locations[loc].tags))]
            for location_name in filtered_locations:
                location_data = data.locations[location_name]
                location = PokemonCrystalLocation(
                    world.player,
                    location_data.label,
                    region,
                    location_data.flag,
                    location_data.rom_address,
                    location_data.default_item,
                    location_data.tags,
                    LocationProgressType.DEFAULT if world.options.goal != Goal.option_elite_four or "PostE4"
                                                    not in location_data.tags else LocationProgressType.EXCLUDED

                )
                region.locations.append(location)

    if world.options.dexsanity:
        pokemon_items = list(world.logically_available_pokemon)
        world.random.shuffle(pokemon_items)
        for _ in range(min(world.options.dexsanity.value, len(pokemon_items))):
            world.generated_dexsanity.add(pokemon_items.pop())

        pokedex_region = regions["Pokedex"]

        for pokemon_id in world.generated_dexsanity:
            pokemon_data = world.generated_pokemon[pokemon_id]
            new_location = PokemonCrystalLocation(
                world.player,
                f"Pokedex - {pokemon_data.friendly_name}",
                pokedex_region,
                flag=POKEDEX_OFFSET + pokemon_data.id,
                tags=frozenset({"dexsanity"})
            )
            pokedex_region.locations.append(new_location)

    if world.options.evolution_methods_required:
        evolution_region = regions["Evolutions"]
        created_locations = set()
        for pokemon_id in world.logically_available_pokemon:
            for evolution in world.generated_pokemon[pokemon_id].evolutions:
                location_name = evolution_location_name(world, pokemon_id, evolution.pokemon)
                if not evolution_in_logic(world, evolution) or location_name in created_locations: continue
                new_location = PokemonCrystalLocation(
                    world.player,
                    location_name,
                    evolution_region,
                    tags=frozenset({"evolution"})
                )
                new_location.show_in_spoiler = False
                new_location.place_locked_item(
                    world.create_event(evolution.pokemon)
                )
                evolution_region.locations.append(new_location)
                created_locations.add(location_name)

    if world.options.breeding_methods_required:
        breeding_region = regions["Breeding"]
        for pokemon_id in world.generated_breeding.keys():
            new_location = PokemonCrystalLocation(
                world.player,
                f"Hatch {world.generated_pokemon[pokemon_id].friendly_name}",
                breeding_region,
                tags=frozenset({"breeding"})
            )
            new_location.show_in_spoiler = False
            new_location.place_locked_item(
                world.create_event(pokemon_id)
            )
            breeding_region.locations.append(new_location)


def create_location_label_to_id_map() -> dict[str, int]:
    """
    Creates a map from location labels to their AP location id (address)
    """
    label_to_id_map: Dict[str, int] = {}
    for region_data in data.regions.values():
        for location_name in region_data.locations:
            location_data = data.locations[location_name]
            label_to_id_map[location_data.label] = location_data.flag

    for pokemon in data.pokemon.values():
        label_to_id_map[f"Pokedex - {pokemon.friendly_name}"] = pokemon.id + POKEDEX_OFFSET

    return label_to_id_map
