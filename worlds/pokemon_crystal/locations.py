from typing import TYPE_CHECKING

from BaseClasses import Location, Region, LocationProgressType
from . import item_const_name_to_id
from .data import data, POKEDEX_OFFSET, POKEDEX_COUNT_OFFSET, FLY_UNLOCK_OFFSET
from .options import Goal, DexsanityStarters
from .pokemon import get_priority_dexsanity, get_excluded_dexsanity
from .utils import evolution_in_logic, evolution_location_name, get_fly_regions, get_mart_slot_location_name

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
    if not world.options.randomize_pokemon_requests:
        exclude.add("BillsGrandpa")
    if not world.options.johto_trainersanity and not world.options.kanto_trainersanity:
        exclude.add("Trainersanity")

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
        pokemon_items = list(world.logic.available_pokemon)
        priority_pokemon = get_priority_dexsanity(world)
        excluded_pokemon = get_excluded_dexsanity(world)

        if world.options.dexsanity_starters.value == DexsanityStarters.option_block:
            excluded_pokemon.update(starter[0] for starter in world.generated_starters)
        pokemon_items = [pokemon_id for pokemon_id in pokemon_items if pokemon_id not in excluded_pokemon]
        world.random.shuffle(pokemon_items)
        for _ in range(min(world.options.dexsanity.value, len(pokemon_items))):
            if priority_pokemon:
                pokemon = priority_pokemon.pop()
                if pokemon in pokemon_items:
                    world.generated_dexsanity.add(pokemon)
                    pokemon_items.remove(pokemon)
                    continue
            world.generated_dexsanity.add(pokemon_items.pop())

        pokedex_region = regions["Pokedex"]

        for pokemon_id in world.generated_dexsanity:
            pokemon_data = world.generated_pokemon[pokemon_id]
            new_location = PokemonCrystalLocation(
                world.player,
                f"Pokedex - {pokemon_data.friendly_name}",
                pokedex_region,
                rom_address=pokemon_data.id,
                flag=POKEDEX_OFFSET + pokemon_data.id,
                tags=frozenset({"dexsanity"})
            )
            pokedex_region.locations.append(new_location)

    if world.options.dexcountsanity:
        total_pokemon = len(world.logic.available_pokemon)
        dexcountsanity_total = min(world.options.dexcountsanity.value, total_pokemon)
        dexcountsanity_step = world.options.dexcountsanity_step.value

        world.generated_dexcountsanity = [i for i in
                                          range(dexcountsanity_step, dexcountsanity_total, dexcountsanity_step)]

        if dexcountsanity_total not in world.generated_dexcountsanity:
            world.generated_dexcountsanity.append(dexcountsanity_total)

        pokedex_region = regions["Pokedex"]

        for dexcountsanity_count in world.generated_dexcountsanity[:-1]:
            new_location = PokemonCrystalLocation(
                world.player,
                f"Pokedex - Catch {dexcountsanity_count} Pokemon",
                pokedex_region,
                rom_address=dexcountsanity_count,
                flag=POKEDEX_COUNT_OFFSET + dexcountsanity_count,
                tags=frozenset({"dexcountsanity"})
            )
            pokedex_region.locations.append(new_location)
        
        assert world.generated_dexcountsanity[-1]

        new_location = PokemonCrystalLocation(
            world.player,
            "Pokedex - Final Catch",
            pokedex_region,
            rom_address=world.generated_dexcountsanity[-1],
            flag=POKEDEX_COUNT_OFFSET + len(data.pokemon),
            tags=frozenset({"dexcountsanity"})
        )
        pokedex_region.locations.append(new_location)

    if world.options.evolution_methods_required:
        evolution_region = regions["Evolutions"]
        created_locations = set()
        for pokemon_id in world.logic.available_pokemon:
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

    if world.options.shopsanity:
        for mart, mart_data in data.marts.items():
            region_name = f"REGION_{mart}"
            if region_name in regions:
                region = regions[region_name]

                for i, item in enumerate(mart_data.items):
                    new_location = PokemonCrystalLocation(
                        world.player,
                        f"{mart_data.friendly_name} - {get_mart_slot_location_name(mart, i)}",
                        region,
                        tags=frozenset({"shopsanity"}),
                        flag=item.flag,
                        rom_address=item.address,
                        default_item_value=item_const_name_to_id(item.item)
                    )
                    new_location.price = item.price
                    region.locations.append(new_location)

    if world.options.randomize_fly_unlocks:

        for fly_region in get_fly_regions(world):
            parent_region = regions[data.regions[fly_region.unlock_region].name]

            location = PokemonCrystalLocation(
                world.player,
                f"Visit {fly_region.name}",
                parent_region,
                tags=frozenset({"fly"}),
                flag=data.event_flags[f"EVENT_VISITED_{fly_region.base_identifier}"],
                rom_address=data.rom_addresses[f"AP_FlyUnlock_{fly_region.base_identifier}"],
                default_item_value=FLY_UNLOCK_OFFSET + fly_region.id
            )

            parent_region.locations.append(location)


def create_location_label_to_id_map() -> dict[str, int]:
    """
    Creates a map from location labels to their AP location id (address)
    """
    label_to_id_map: dict[str, int] = {}
    for region_data in data.regions.values():
        for location_name in region_data.locations:
            location_data = data.locations[location_name]
            label_to_id_map[location_data.label] = location_data.flag

    for mart, mart_data in data.marts.items():
        for i, item in enumerate(mart_data.items):
            if item.flag:
                label_to_id_map[f"{mart_data.friendly_name} - {get_mart_slot_location_name(mart, i)}"] = item.flag

    for pokemon in data.pokemon.values():
        label_to_id_map[f"Pokedex - {pokemon.friendly_name}"] = pokemon.id + POKEDEX_OFFSET

    for i in range(1, len(data.pokemon)):
        label_to_id_map[f"Pokedex - Catch {i} Pokemon"] = i + POKEDEX_COUNT_OFFSET

    label_to_id_map["Pokedex - Final Catch"] = len(data.pokemon) + POKEDEX_COUNT_OFFSET

    for fly_region in data.fly_regions:
        label_to_id_map[f"Visit {fly_region.name}"] = data.event_flags[f"EVENT_VISITED_{fly_region.base_identifier}"]

    return label_to_id_map


DEXSANITY_LOCATIONS = {f"Pokedex - {pokemon.friendly_name}" for pokemon in data.pokemon.values()}
DEXCOUNTSANITY_LOCATIONS = {f"Pokedex - Catch {i + 1} Pokemon" for i in range(len(data.pokemon) - 1)} | {
    "Pokedex - Final Catch"}

LOCATION_GROUPS = {
    "Badges": {loc.label for loc in data.locations.values() if "Badge" in loc.tags},
    "Dexsanity": DEXSANITY_LOCATIONS,
    "Dexcountsanity": DEXCOUNTSANITY_LOCATIONS,
    "Dex": DEXSANITY_LOCATIONS | DEXCOUNTSANITY_LOCATIONS,
    "Hidden Items": {loc.label for loc in data.locations.values() if "Hidden" in loc.tags},
    "Item Balls": {loc.label for loc in data.locations.values() if "StandingItems" in loc.tags},
    "Trainersanity": {loc.label for loc in data.locations.values() if "Trainersanity" in loc.tags},
    "Berry Trees": {loc.label for loc in data.locations.values() if "BerryTree" in loc.tags},
    "Key Items": {loc.label for loc in data.locations.values() if "KeyItem" in loc.tags},
    "Ruins of Alph": {loc.label for loc in data.locations.values() if "AlphItemChambers" in loc.tags},
    "Shopsanity": {f"{mart_data.friendly_name} - {get_mart_slot_location_name(mart, i)}" for mart, mart_data in
                   data.marts.items() for i, item in
                   enumerate(mart_data.items) if item.flag},
    "Fly Unlocks": {f"Visit {region.name}" for region in data.fly_regions},
    "NPC Gifts": {loc.label for loc in data.locations.values() if "NPCGift" in loc.tags},
    "Azalea Town": {loc.label for loc in data.locations.values() if "Azalea" in loc.tags},
    "Burned Tower": {loc.label for loc in data.locations.values() if "Burned" in loc.tags},
    "Celadon City": {loc.label for loc in data.locations.values() if "Celadon" in loc.tags},
    "Cerulean City": {loc.label for loc in data.locations.values() if "Cerulean" in loc.tags},
    "Cianwood City": {loc.label for loc in data.locations.values() if "Cianwood" in loc.tags},
    "Cinnabar Island": {loc.label for loc in data.locations.values() if "Cinnabar" in loc.tags},
    "Dark Cave": {loc.label for loc in data.locations.values() if "Dark" in loc.tags},
    "Dragon's Den": {loc.label for loc in data.locations.values() if "Dragon" in loc.tags},
    "Ecruteak City": {loc.label for loc in data.locations.values() if "Ecruteak" in loc.tags},
    "Saffron City": {loc.label for loc in data.locations.values() if "Saffron" in loc.tags},
    "Goldenrod City": {loc.label for loc in data.locations.values() if "Goldenrod" in loc.tags},
    "Ice Path": {loc.label for loc in data.locations.values() if "Ice" in loc.tags},
    "Ilex Forest": {loc.label for loc in data.locations.values() if "Ilex" in loc.tags},
    "Lake of Rage": {loc.label for loc in data.locations.values() if "Rage" in loc.tags},
    "Mount Mortar": {loc.label for loc in data.locations.values() if "Mortar" in loc.tags},
    "National Park": {loc.label for loc in data.locations.values() if "Park" in loc.tags},
    "Olivine Lighthouse": {loc.label for loc in data.locations.values() if "Lighthouse" in loc.tags},
    "Olivine City": {loc.label for loc in data.locations.values() if "Olivine" in loc.tags},
    "Radio Tower": {loc.label for loc in data.locations.values() if "Radio" in loc.tags},
    "Rock Tunnel": {loc.label for loc in data.locations.values() if "Rock" in loc.tags},
    "Silver Cave": {loc.label for loc in data.locations.values() if "Silver" in loc.tags},
    "Slowpoke Well": {loc.label for loc in data.locations.values() if "Slow" in loc.tags},
    "Sprout Tower": {loc.label for loc in data.locations.values() if "Sprout" in loc.tags},
    "Team Rocket HQ": {loc.label for loc in data.locations.values() if "Rocket" in loc.tags},
    "Tin Tower": {loc.label for loc in data.locations.values() if "Tin" in loc.tags},
    "Union Cave": {loc.label for loc in data.locations.values() if "Union" in loc.tags},
    "Vermilion City": {loc.label for loc in data.locations.values() if "Vermilion" in loc.tags},
    "Victory Road": {loc.label for loc in data.locations.values() if "Victory" in loc.tags},
    "Violet City": {loc.label for loc in data.locations.values() if "Violet" in loc.tags},
    "Whirl Islands": {loc.label for loc in data.locations.values() if "Whirl" in loc.tags},
    "Cherrygrove City": {loc.label for loc in data.locations.values() if "Cherrygrove" in loc.tags},
    "One offs": {loc.label for loc in data.locations.values() if "One off" in loc.tags}, #locations with only one check 
    "New Bark Town": {loc.label for loc in data.locations.values() if "NewBark" in loc.tags},
    "Blackthorn City": {loc.label for loc in data.locations.values() if "Blackthorn" in loc.tags},
    "S.S. Aqua": {loc.label for loc in data.locations.values() if "Aqua" in loc.tags},
    "Fuchsia City": {loc.label for loc in data.locations.values() if "Fuchsia" in loc.tags},
    "Mahogany Town": {loc.label for loc in data.locations.values() if "Mahogany" in loc.tags},
    "Pewter City": {loc.label for loc in data.locations.values() if "Pewter" in loc.tags},
    "Viridian City": {loc.label for loc in data.locations.values() if "Viridian" in loc.tags},
    "Elite 4": {loc.label for loc in data.locations.values() if "Elite" in loc.tags},
}
