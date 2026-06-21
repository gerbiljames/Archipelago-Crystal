import logging
from collections.abc import Iterable
from dataclasses import replace
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, CollectionState
from .data import data as crystal_data, LogicalAccess, EncounterType, MiscOption, EncounterMon, GrowthRate
from .evolution import get_random_pokemon_evolution
from .items import get_random_filler_item
from .moves import get_tmhm_compatibility, randomize_learnset, moves_convert_friendly_to_ids
from .options import RandomizeTypes, RandomizePalettes, RandomizeBaseStats, RandomizeStarters, RandomizeTrades, \
    DexsanityStarters, EncounterGrouping, RandomizePokemonRequests, Goal, GrowthRates, WildEncounterMethodsRequired, \
    PokemonSourceLogic
from .pokemon_pool import ENCOUNTER_TYPE_TO_SOURCE_KEY
from .pokemon_data import ALL_UNOWN, LEGENDARY_POKEMON, NON_LEGENDARY_POKEMON
from .utils import should_include_region

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def randomize_pokemon_data(world: "PokemonCrystalWorld"):
    if world.options.growth_rates == GrowthRates.option_normalized:
        for pkmn_name, pkmn_data in world.generated_pokemon.items():
            new_rate = GrowthRate.Slow if pkmn_data.friendly_name in LEGENDARY_POKEMON else GrowthRate.MediumFast
            if pkmn_data.growth_rate != new_rate:
                world.generated_pokemon[pkmn_name] = replace(pkmn_data, growth_rate=new_rate)

    # follow_evolutions can change types after the pokemon has already been randomized,
    # so we randomize types before all else
    if world.options.randomize_types.value:
        for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[0]):
            evolution_line_list = [pkmn_name]
            if world.options.randomize_types.value == RandomizeTypes.option_follow_evolutions:
                # skip evolved pokemon if follow_evolutions
                if (not pkmn_data.is_base
                        and pkmn_name not in ("FLAREON", "JOLTEON", "VAPOREON", "ESPEON", "UMBREON")):
                    continue
                for evo in pkmn_data.evolutions:
                    evolution_line_list.append(evo.pokemon)
                    evo_poke = world.generated_pokemon[evo.pokemon]
                    for second_evo in evo_poke.evolutions:
                        evolution_line_list.append(second_evo.pokemon)

            new_types = get_random_types(world)
            for pokemon in evolution_line_list:
                world.generated_pokemon[pokemon] = replace(
                    world.generated_pokemon[pokemon],
                    types=new_types
                )

    move_blocklist = moves_convert_friendly_to_ids(world, world.options.move_blocklist)

    for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[0]):
        new_base_stats = pkmn_data.base_stats
        new_learnset = pkmn_data.learnset
        new_tm_hms = pkmn_data.tm_hm

        if world.options.randomize_palettes.value and world.options.randomize_palettes.value != RandomizePalettes.option_swap_shiny:
            if world.options.randomize_palettes.value == RandomizePalettes.option_match_types:
                world.generated_palettes[pkmn_name] = get_type_colors(pkmn_data.types, world.random)
            else:
                world.generated_palettes[pkmn_name] = get_random_colors(world.random)

        if world.options.randomize_base_stats.value:
            multiple = 5 if world.options.base_stats_multiples_of_five else 1

            if world.options.randomize_base_stats.value == RandomizeBaseStats.option_keep_bst:
                new_base_stats = get_random_base_stats(world.random, multiple, pkmn_data.bst)
            else:
                new_base_stats = get_random_base_stats(world.random, multiple)

        if world.options.randomize_learnsets or world.options.metronome_only:
            new_learnset = randomize_learnset(world, pkmn_name, move_blocklist)

        if (world.options.tm_same_type_compatibility >= 0
                or world.options.tm_other_type_compatibility >= 0
                or world.options.hm_same_type_compatibility >= 0
                or world.options.hm_other_type_compatibility >= 0):
            new_tm_hms = get_tmhm_compatibility(world, pkmn_name)

        world.generated_pokemon[pkmn_name] = replace(
            world.generated_pokemon[pkmn_name],
            tm_hm=new_tm_hms,
            learnset=new_learnset,
            base_stats=new_base_stats,
            bst=sum(new_base_stats)
        )

    if MiscOption.DontFuckleWithShuckle.value in world.generated_misc.selected:
        new_base_stats = list(world.generated_pokemon["SHUCKLE"].base_stats)
        attack = new_base_stats[1]
        new_base_stats[1] = new_base_stats[2]
        new_base_stats[2] = attack
        sp_atk = new_base_stats[4]
        new_base_stats[4] = new_base_stats[5]
        new_base_stats[5] = sp_atk
        world.generated_pokemon["SHUCKLE"] = replace(
            world.generated_pokemon["SHUCKLE"],
            base_stats=new_base_stats,
        )


def randomize_starters(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker or not world.options.randomize_starters: return

    blocklist = world.options.starter_blocklist.get_ids(world)

    base_only = world.options.randomize_starters.value == RandomizeStarters.option_unevolved_only
    for evo_line in world.generated_starters:
        starter_pokemon = get_random_pokemon(world, base_only=base_only, starter=True, exclude_unown=True,
                                             blocklist=blocklist)
        blocklist.add(starter_pokemon)
        starter_data = world.generated_pokemon[starter_pokemon]
        evo_line[0] = starter_pokemon

        middle_evo_pokemon = get_random_pokemon_evolution(world.random, starter_pokemon, starter_data)
        middle_data = world.generated_pokemon[middle_evo_pokemon]
        evo_line[1] = middle_evo_pokemon

        final_evo_pokemon = get_random_pokemon_evolution(world.random, middle_evo_pokemon, middle_data)
        evo_line[2] = final_evo_pokemon

    if MiscOption.UnLuckyEgg.value in world.generated_misc.selected:
        new_helditems = ("LUCKY_EGG", "LUCKY_EGG", "LUCKY_EGG")
    else:
        new_helditems = (get_random_filler_item(world),
                         get_random_filler_item(world),
                         get_random_filler_item(world))

    world.generated_starter_helditems = new_helditems


def randomize_trade_received_pokemon(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker: return

    if world.options.randomize_trades.value not in (RandomizeTrades.option_received,
                                                    RandomizeTrades.option_both): return

    blocklist = getattr(world, "unique_static_wild_block", set()) or None
    for trade_id, trade in world.generated_trades.items():
        received_pokemon = trade.received_pokemon
        world.generated_trades[trade_id] = replace(
            trade,
            received_pokemon=get_random_pokemon(world, blocklist=blocklist),
            held_item=get_random_filler_item(world) if received_pokemon != "ABRA" else "TM_9"
        )


def randomize_trade_requested_pokemon(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker: return

    randomize_requested = world.options.randomize_trades.value in (RandomizeTrades.option_requested,
                                                                       RandomizeTrades.option_both)

    logically_available_pokemon = sorted(world.pokemon_pool.get_filtered(world.options.pokemon_request_logic,
                                                                          exclude_unown=True))

    assert logically_available_pokemon
    while len(logically_available_pokemon) < len(world.generated_trades):
        logically_available_pokemon.append(world.random.choice(logically_available_pokemon))

    world.random.shuffle(logically_available_pokemon)

    for trade_id, trade in world.generated_trades.items():
        if randomize_requested:
            requested_pokemon = logically_available_pokemon.pop()
        else:
            requested_pokemon = trade.requested_pokemon \
                if trade.requested_pokemon in logically_available_pokemon else logically_available_pokemon.pop()

        world.generated_trades[trade_id] = replace(
            trade,
            requested_gender=0 if world.options.randomize_trades else trade.requested_gender,  # no gender
            requested_pokemon=requested_pokemon,
        )


def randomize_request_pokemon(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker: return

    if world.options.randomize_pokemon_requests in (RandomizePokemonRequests.option_items_and_pokemon,
                                                    RandomizePokemonRequests.option_pokemon):

        request_pool = world.pokemon_pool.get_filtered(world.options.pokemon_request_logic, exclude_unown=True)
        logically_available_pokemon = sorted(request_pool)

        assert logically_available_pokemon
        while len(logically_available_pokemon) < len(world.generated_request_pokemon):
            logically_available_pokemon.append(world.random.choice(logically_available_pokemon))

        world.random.shuffle(logically_available_pokemon)
        world.generated_request_pokemon = [logically_available_pokemon.pop() for _ in world.generated_request_pokemon]
    elif world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items:
        # ideally we should never need this, but best to be safe
        request_pool = world.pokemon_pool.get_filtered(world.options.pokemon_request_logic, exclude_unown=True)
        logically_available_pokemon = sorted(request_pool)

        world.generated_request_pokemon = [
            world.random.choice(logically_available_pokemon) if mon not in request_pool else mon for
            mon in world.generated_request_pokemon]


def fill_trade_locations(world: "PokemonCrystalWorld"):
    if not world.options.trades_required: return

    for trade_id, trade in world.generated_trades.items():
        try:
            location = world.get_location(trade_id)
            location.place_locked_item(world.create_event(trade.received_pokemon,
                                                          source=PokemonSourceLogic.TRADES))
        except KeyError:
            continue


def ensure_fly_learner_in_sphere_1(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker or not world.options.early_fly:
        return

    fly_override = world.options.hm_compatibility_override.value.get("Fly")
    if fly_override == 100:
        return
    if (fly_override is None
            and world.options.hm_same_type_compatibility.value == 100
            and world.options.hm_other_type_compatibility.value == 100):
        return

    fly_learners = set(world.logic.compatible_hm_pokemon["FLY"])

    state = CollectionState(world.multiworld)
    locations = world.multiworld.get_reachable_locations(state=state, player=world.player)
    early_region_keys = {
        loc.parent_region.key for loc in locations
        if "wild encounter" in loc.tags
        and world.logic.wild_regions[loc.parent_region.key] is LogicalAccess.InLogic
    }

    sphere_1_species: set[str] = set()
    for key in early_region_keys:
        for enc in world.generated_wild.get(key, ()):
            sphere_1_species.add(enc.pokemon)
        if key in world.generated_static:
            sphere_1_species.add(world.generated_static[key].pokemon)

    if sphere_1_species & fly_learners:
        return

    if not sphere_1_species:
        logging.warning(
            "Pokemon Crystal: early_fly is enabled but no sphere 1 Pokemon are catchable "
            "for player %s (%s); HM02 Fly may be unusable until later.",
            world.player, world.player_name)
        return

    target = world.random.choice(sorted(sphere_1_species))
    pkmn = world.generated_pokemon[target]
    if "FLY" not in pkmn.tm_hm:
        world.generated_pokemon[target] = replace(pkmn, tm_hm=tuple(pkmn.tm_hm) + ("FLY",))
        world.logic.add_hm_compatible_pokemon("FLY", target)


def place_starters_in_early_wilds(world: "PokemonCrystalWorld", allow_partial_entrances: bool = False):
    if (world.options.dexsanity_starters.value != DexsanityStarters.option_available_early
            or world.is_universal_tracker):
        return

    # Only move starters between encounter types that dexsanity_logic actually counts. Otherwise the
    # swap could shift a starter into an uncounted type (e.g. Land when only Fishing counts), silently
    # dropping it from the logical dex pool and desyncing the dexcountsanity milestones.
    def counts_for_dex(region) -> bool:
        return ENCOUNTER_TYPE_TO_SOURCE_KEY.get(region.key.encounter_type) in world.options.dexsanity_logic

    locations = world.multiworld.get_reachable_locations(
        state=CollectionState(world.multiworld, allow_partial_entrances=allow_partial_entrances),
        player=world.player)
    early_wild_regions = [loc.parent_region for loc in locations if "wild encounter" in loc.tags]
    early_wild_regions = [region for region in early_wild_regions if
                          world.logic.wild_regions[region.key] is LogicalAccess.InLogic
                          and region.key.encounter_type is not EncounterType.Static
                          and counts_for_dex(region)]
    early_wild_regions.sort(key=lambda region: region.name)
    world.random.shuffle(early_wild_regions)

    other_wild_regions = [loc.parent_region for loc in world.multiworld.get_locations(world.player) if
                          "wild encounter" in loc.tags
                          and loc.parent_region not in early_wild_regions
                          and world.logic.wild_regions[loc.parent_region.key] is LogicalAccess.InLogic
                          and loc.parent_region.key.encounter_type is not EncounterType.Static
                          and counts_for_dex(loc.parent_region)]
    other_wild_regions.sort(key=lambda region: region.name)
    world.random.shuffle(other_wild_regions)

    if not (early_wild_regions and other_wild_regions):
        return

    for evo_line in world.generated_starters:

        if not early_wild_regions: continue
        starter = evo_line[0]
        source_region = None
        source_encounters = None

        if any(encounter
               for region in early_wild_regions
               for encounter in world.generated_wild[region.key]
               if encounter.pokemon == starter):
            continue

        for region in other_wild_regions:
            source_encounters = world.generated_wild[region.key]
            if starter in [encounter.pokemon for encounter in source_encounters]:
                source_region = region
                break

        if not source_region:  continue
        target_region = None
        target_encounters: list[EncounterMon] = []
        while not target_encounters:
            if not early_wild_regions: break
            target_region = early_wild_regions.pop()
            target_encounters = world.generated_wild[target_region.key]

        if not target_encounters: continue

        if (world.options.encounter_grouping == EncounterGrouping.option_one_to_one
                or not world.options.randomize_wilds):
            pokemon_to_swap = target_encounters[0].pokemon
            target_indexes = [i for i, enc in enumerate(target_encounters) if enc.pokemon == pokemon_to_swap]
            source_indexes = [i for i, enc in enumerate(source_encounters) if enc.pokemon == starter]
            for i in target_indexes:
                target_encounters[i] = replace(target_encounters[i], pokemon=starter)
            for i in source_indexes:
                source_encounters[i] = replace(source_encounters[i], pokemon=pokemon_to_swap)
        elif world.options.encounter_grouping.value == EncounterGrouping.option_all_split:
            starter_index = next(
                i for i, encounter in enumerate(source_encounters) if encounter.pokemon == starter)
            source_encounters[starter_index] = replace(source_encounters[starter_index],
                                                       pokemon=target_encounters[0].pokemon)
            target_encounters[0] = replace(target_encounters[0], pokemon=starter)
        else:
            pokemon_to_swap = target_encounters[0].pokemon
            target_encounters = [replace(mon, pokemon=starter) for mon in target_encounters]
            source_encounters = [replace(mon, pokemon=pokemon_to_swap) for mon in source_encounters]
        world.generated_wild[source_region.key] = source_encounters
        world.generated_wild[target_region.key] = target_encounters


def fill_wild_encounter_locations(world: "PokemonCrystalWorld"):
    for region_key, encounters in world.generated_wild.items():
        region_logic = world.logic.wild_regions[region_key]
        if region_logic is LogicalAccess.InLogic or (
                world.is_universal_tracker and region_logic is LogicalAccess.OutOfLogic):
            wild_source = ENCOUNTER_TYPE_TO_SOURCE_KEY.get(region_key.encounter_type)
            seen_pokemon = set()
            for i, encounter in enumerate(encounters):
                location = world.get_location(f"{region_key.region_name()}_{i + 1}")
                location.place_locked_item(world.create_event(encounter.pokemon, source=wild_source))
                if encounter.pokemon in seen_pokemon:
                    location.item.classification = ItemClassification.useful
                seen_pokemon.add(encounter.pokemon)

    for region_key, static in world.generated_static.items():
        access = world.logic.wild_regions[region_key]
        if access is LogicalAccess.InLogic or (world.is_universal_tracker and access is LogicalAccess.OutOfLogic):
            location = world.get_location(f"{region_key.region_name()}_1")
            location.place_locked_item(world.create_event(static.pokemon, source=PokemonSourceLogic.STATICS))

    if WildEncounterMethodsRequired.BUG_CATCHING_CONTEST in world.options.wild_encounter_methods_required or world.is_universal_tracker:
        for i, slot in enumerate(world.generated_contest):
            location = world.get_location(f"Bug Catching Contest Slot {i + 1}")
            location.place_locked_item(world.create_event(slot.pokemon,
                                                          source=PokemonSourceLogic.BUG_CATCHING_CONTEST))


def build_pokemon_pool_index(world: "PokemonCrystalWorld"):
    """Pre-compute indexed pokemon pools for fast lookup by type and BST.

    Must be called after all pokemon data mutations (types, base stats, evolutions) are finalized."""
    from bisect import insort

    by_type: dict[str, set[str]] = {}
    bst_sorted: list[tuple[int, str]] = []
    all_names: set[str] = set()
    base_only_names: set[str] = set()
    fully_evolved_names: set[str] = set()

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        all_names.add(pkmn_name)
        for t in pkmn_data.types:
            by_type.setdefault(t, set()).add(pkmn_name)
        insort(bst_sorted, (pkmn_data.bst, pkmn_name))
        if pkmn_data.is_base:
            base_only_names.add(pkmn_name)
        if not pkmn_data.evolutions:
            fully_evolved_names.add(pkmn_name)

    world._pokemon_pool_index = {
        "by_type": by_type,
        "bst_sorted": bst_sorted,
        "all": all_names,
        "base_only": base_only_names,
        "fully_evolved": fully_evolved_names,
    }


def _filter_bst_range(bst_sorted: list[tuple[int, str]], target_bst: int, bst_range: float) -> set[str]:
    """Return names of pokemon whose BST is within range of target, using binary search."""
    from bisect import bisect_left, bisect_right

    lo = bisect_left(bst_sorted, (int(target_bst - bst_range),))
    hi = bisect_right(bst_sorted, (int(target_bst + bst_range), "\xff"))
    return {name for _, name in bst_sorted[lo:hi]}


def get_random_pokemon(world: "PokemonCrystalWorld", priority_pokemon: set[str] | None = None, types=None,
                       base_only=False, force_fully_evolved_at=None, current_level=None, starter=False,
                       exclude_unown=False, blocklist: set[str] | None = None,
                       match_bst: int | None = None) -> str:
    index = world._pokemon_pool_index

    # Start with either the priority set or the full set
    if priority_pokemon:
        pool = set(priority_pokemon)
    else:
        pool = set(index["all"])

    # Apply blocklist
    if blocklist:
        pool -= blocklist

    # Exclude Unown
    if exclude_unown:
        pool.discard("UNOWN")

    # Filter by type — keep pokemon that match at least one of the requested types
    if types is not None:
        type_matches = set()
        for t in set(types):
            type_pool = index["by_type"].get(t)
            if type_pool:
                type_matches |= type_pool
        pool &= type_matches

    # Base-only filter
    if base_only:
        pool &= index["base_only"]

    # Force fully evolved filter
    if force_fully_evolved_at and current_level is not None and current_level >= force_fully_evolved_at:
        pool &= index["fully_evolved"]

    # Starter-specific filters
    if starter:
        if world.options.randomize_starters == RandomizeStarters.option_first_stage_can_evolve:
            pool &= index["base_only"] - index["fully_evolved"]
        elif world.options.randomize_starters == RandomizeStarters.option_base_stat_mode:
            bst_avg = world.options.starters_bst_average
            bst_matches = _filter_bst_range(index["bst_sorted"], bst_avg, bst_avg * .10)
            starter_pool = pool & bst_matches
            if not starter_pool:
                bst_matches = _filter_bst_range(index["bst_sorted"], bst_avg, bst_avg * .20)
                starter_pool = pool & bst_matches
            if starter_pool:
                pool = starter_pool

    # BST matching for trainer pokemon
    if match_bst is not None:
        bst_matches = _filter_bst_range(index["bst_sorted"], match_bst, match_bst * .10)
        bst_pool = pool & bst_matches
        if not bst_pool:
            bst_matches = _filter_bst_range(index["bst_sorted"], match_bst, match_bst * .20)
            bst_pool = pool & bst_matches
        if bst_pool:
            pool = bst_pool

    # Final fallback — if everything got filtered out, use all pokemon
    if not pool:
        pool = set(index["all"])
        if exclude_unown:
            pool.discard("UNOWN")

    return world.random.choice(sorted(pool))


def get_random_nezumi(random):
    # 🐁
    pokemon_pool = ["RATTATA", "RATICATE", "NIDORAN_F", "NIDORAN_M", "NIDORINA", "NIDORINO", "PIKACHU", "RAICHU",
                    "SANDSHREW", "SANDSLASH", "CYNDAQUIL", "QUILAVA", "SENTRET", "FURRET", "MARILL"]
    return random.choice(pokemon_pool)


def _locations_to_pokemon(world: "PokemonCrystalWorld", locations: Iterable[str]) -> set[str]:
    pokemon = set()
    for location in locations:
        parts = location.split("- ")
        if len(parts) != 2: continue
        if "Catch" in parts[1]: continue
        pokemon.add(parts[1])

    if "_Legendaries" in pokemon:
        pokemon.discard("_Legendaries")
        pokemon.update(LEGENDARY_POKEMON)
    elif "_Non-Legendaries" in pokemon:
        pokemon.discard("_Non-Legendaries")
        pokemon.update(NON_LEGENDARY_POKEMON)

    pokemon_ids = {pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if
                   pokemon_data.friendly_name in pokemon}

    return pokemon_ids


def get_chamber_event_for_unown(unown_letter: str) -> str:
    char = unown_letter[-1]
    if char < "L": return "ENGINE_UNLOCKED_UNOWNS_A_TO_K"
    if char < "S": return "ENGINE_UNLOCKED_UNOWNS_L_TO_R"
    if char < "X": return "ENGINE_UNLOCKED_UNOWNS_S_TO_W"
    return "ENGINE_UNLOCKED_UNOWNS_X_TO_Z"


def randomize_unown_signs(world: "PokemonCrystalWorld"):
    if Goal.UNOWN_HUNT not in world.options.goal: return
    available_signs = []
    for region in crystal_data.regions.values():
        if not should_include_region(region, world): continue
        for sign in region.signs:
            available_signs.append(sign)

    all_unown = list(ALL_UNOWN)
    world.random.shuffle(all_unown)
    world.random.shuffle(available_signs)

    for unown in all_unown:
        world.generated_unown_signs[available_signs.pop()] = unown


def get_priority_dexsanity(world: "PokemonCrystalWorld") -> set[str]:
    return _locations_to_pokemon(world, world.options.priority_locations.value)


def get_excluded_dexsanity(world: "PokemonCrystalWorld") -> set[str]:
    return _locations_to_pokemon(world, world.options.exclude_locations.value)


def get_pokemon_id_by_rom_id(id: int) -> str:
    return next(poke_id for poke_id, poke_data in crystal_data.pokemon.items() if poke_data.id == id)


def get_random_base_stats(random, multiple=1, bst=None):
    if bst is None:
        # sunkern to mewtwo
        bst = random.randrange(180, 681, multiple)
    # add 0.5 to prevent a single stat exceeding 255
    # biggest possible variance on max bst is (1.5 * 680) / 4 = 255
    # for this reason, multiple must not be a number where half-to-even rounds ((1.5 * 680) / (4 * multiple)) upward
    randoms = [random.random() + 0.5 for _i in range(0, 6)]
    total = sum(randoms)
    base_stats = [int(round((stat * bst) / (total * multiple)) * multiple) for stat in randoms]
    return __place_base_stats_remainder(random, base_stats, bst - sum(base_stats), random.randint(0, 5))

def __place_base_stats_remainder(random, stats: list[int], remainder: int, stat: int):
    if remainder == 0:
        return stats

    new_base_stat = stats[stat] + remainder
    if new_base_stat > 255 or new_base_stat < 5:
        stats = __place_base_stats_remainder(random, stats, remainder, (stat + 1) % 6)
    else:
        stats[stat] = new_base_stat
    return stats

def get_random_types(world: "PokemonCrystalWorld") -> list[str]:
    all_types = list(crystal_data.types.keys())
    if world.options.shared_primary_type:
        new_types = [type_id for type_id, type_data in crystal_data.types.items() if
                     type_data.rom_id == world.options.shared_primary_type.value - 1]
    else:
        new_types = [world.random.choice(all_types)]
    # approx. 110/251 Pokemon are dual type in gen 2
    if world.random.randint(0, 24) < 11:
        new_types.append(world.random.choice([t for t in all_types if t not in new_types]))
    return new_types


def add_hm_compatibility(world: "PokemonCrystalWorld", pokemon_id: str, hm: str):
    pokemon_data = world.generated_pokemon[pokemon_id]
    world.generated_pokemon[pokemon_id] = replace(pokemon_data, tm_hm=[hm] + list(pokemon_data.tm_hm))
    world.logic.add_hm_compatible_pokemon(hm, pokemon_id)


# palettes stuff
def get_random_colors(random):
    return [
        c for _ in range(4)
        for c in convert_color(random.randint(0, 31), random.randint(0, 31), random.randint(0, 31))
    ]


def get_type_colors(types, random):
    type1 = types[0]
    type2 = types[-1]

    c1 = type_palettes[type1][0]
    c2 = type_palettes[type2][1]

    r1, g1, b1 = shift_color(c1[0], c1[1], c1[2], random)
    r2, g2, b2 = shift_color(c2[0], c2[1], c2[2], random)

    # normal colors
    color1 = convert_color(r1, g1, b1)
    color2 = convert_color(r2, g2, b2)

    # invert colors for shiny palette
    color3 = convert_color(31 - r1, 31 - g1, 31 - b1)
    color4 = convert_color(31 - r2, 31 - g2, 31 - b2)
    return list(color1 + color2 + color3 + color4)


def shift_color(r: int, g: int, b: int, random):
    return r + random.randint(-1, 1), \
           g + random.randint(-1, 1), \
           b + random.randint(-1, 1)


def convert_color(r: int, g: int, b: int):
    r = max(0, min(r, 31))
    g = max(0, min(g, 31))
    b = max(0, min(b, 31))

    color = (b << 10) | (g << 5) | r
    return color.to_bytes(2, "little")


type_palettes = {
    "NORMAL": [[31, 27, 31], [31, 24, 30]],
    "FIGHTING": [[30, 17, 1], [24, 9, 0]],
    "FLYING": [[17, 21, 31], [15, 11, 28]],
    "POISON": [[27, 21, 31], [15, 10, 24]],
    "GROUND": [[28, 19, 13], [24, 14, 0]],
    "ROCK": [[21, 20, 22], [18, 15, 4]],
    "BUG": [[23, 25, 6], [16, 18, 4]],
    "GHOST": [[10, 8, 14], [5, 3, 15]],
    "STEEL": [[19, 19, 21], [12, 14, 13]],
    "FIRE": [[31, 7, 0], [31, 15, 0]],
    "WATER": [[5, 8, 31], [2, 4, 26]],
    "GRASS": [[8, 31, 5], [4, 24, 2]],
    "ELECTRIC": [[31, 23, 7], [31, 17, 0]],
    "PSYCHIC_TYPE": [[31, 14, 30], [24, 4, 14]],
    "ICE": [[17, 25, 30], [22, 27, 30]],
    "DRAGON": [[16, 20, 25], [9, 12, 23]],
    "DARK": [[4, 2, 7], [3, 2, 6]],
}
