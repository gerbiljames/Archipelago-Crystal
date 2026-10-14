from collections import defaultdict
from typing import TYPE_CHECKING

from .data import data as crystal_data, LogicalAccess, EncounterType
from .options import Goal, PokemonSourceLogic

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


ENCOUNTER_TYPE_TO_SOURCE_KEY = {
    EncounterType.Grass: PokemonSourceLogic.LAND,
    EncounterType.Water: PokemonSourceLogic.SURFING,
    EncounterType.Fish: PokemonSourceLogic.FISHING,
    EncounterType.Tree: PokemonSourceLogic.HEADBUTT,
    EncounterType.RockSmash: PokemonSourceLogic.ROCK_SMASH,
    EncounterType.Swarm: PokemonSourceLogic.SWARM,
}

WILD_SOURCES = frozenset(ENCOUNTER_TYPE_TO_SOURCE_KEY.values()) | {PokemonSourceLogic.BUG_CATCHING_CONTEST}


class PokemonPool:
    """Lazy, cached views of the logically available Pokemon for each Pokemon logic group.

    A single invalidate() call clears all caches. Evolution and breeding relationship
    data continues to live on PokemonCrystalLogic; this class reads it but does not own it.
    """

    def __init__(self, world: "PokemonCrystalWorld"):
        self._world = world
        self._sources: dict[str, set[str]] | None = None
        self._filtered_cache: dict[tuple, set[str]] = {}
        self._diploma_count: int | None = None
        self._dexcountsanity_total: int | None = None
        self._completable_trades: set[str] = set()
        self.trade_requests_assigned = False

    def invalidate(self) -> None:
        """Clear every cached pool."""
        self._sources = None
        self._filtered_cache.clear()
        self._diploma_count = None
        self._dexcountsanity_total = None

    def ensure_base_pools(self) -> None:
        """Compute the sources each species is obtainable from, over every active source.

        Populates `world.logic.evolution` and `world.logic.breeding` as a side
        effect. Received trade species must be randomized before this is called;
        requested species are randomized later and consume get_filtered().

        A trade only joins the pool once the species it asks for is in the pool, so trades
        can't bootstrap each other into it.
        """
        if self._sources is not None:
            return

        world = self._world
        sources = defaultdict[str, set[str]](set)

        for region_key, wilds in world.generated_wild.items():
            source = ENCOUNTER_TYPE_TO_SOURCE_KEY.get(region_key.encounter_type)
            if source and world.logic.wild_regions[region_key] is LogicalAccess.InLogic:
                for wild in wilds:
                    sources[wild.pokemon].add(source)

        if PokemonSourceLogic.BUG_CATCHING_CONTEST in world.active_sources:
            for slot in world.generated_contest:
                sources[slot.pokemon].add(PokemonSourceLogic.BUG_CATCHING_CONTEST)

        for region_key, static in world.generated_static.items():
            if world.logic.wild_regions[region_key] is LogicalAccess.InLogic:
                sources[static.pokemon].add(PokemonSourceLogic.STATICS)
        if Goal.UNOWN_HUNT in world.options.goal:
            sources["UNOWN"].add(PokemonSourceLogic.STATICS)

        self._completable_trades = set[str]()
        previous_size = -1
        while previous_size != len(sources):
            previous_size = len(sources)
            available = set(sources)
            for pokemon in self._compute_evolutions(available):
                sources[pokemon].add(PokemonSourceLogic.EVOLUTION)
            for pokemon in self._compute_breeding(available):
                sources[pokemon].add(PokemonSourceLogic.BREEDING)
            for pokemon in self._admit_trades(available):
                sources[pokemon].add(PokemonSourceLogic.TRADES)

        self._sources = dict(sources)

    @property
    def diploma_count(self) -> int:
        """Diploma-requirement count. UT-aware."""
        if self._diploma_count is None:
            world = self._world
            self._diploma_count = (world.ut_slot_data["diploma_count"] if world.is_universal_tracker
                                   else len(self.get_filtered(world.options.diploma_logic)))
        return self._diploma_count

    @property
    def dexcountsanity_total(self) -> int:
        """Total Pokemon count for dexcountsanity. UT-aware."""
        if self._dexcountsanity_total is None:
            world = self._world
            self._dexcountsanity_total = (world.ut_slot_data["logically_available_pokemon_count"]
                                          if world.is_universal_tracker
                                          else len(self.get_filtered(world.options.dexsanity_logic)))
        return self._dexcountsanity_total

    def get_filtered(self, source_logic: PokemonSourceLogic, exclude_unown: bool = False) -> set[str]:
        """Pokemon obtainable from a source in `source_logic`.

        Falls back to every active source if empty, matching the effective_sources fallback.
        """
        key = (frozenset(source_logic.value), exclude_unown)
        if key not in self._filtered_cache:
            self._filtered_cache[key] = (self._filter(key[0], exclude_unown)
                                         or self._filter(self._world.active_sources, exclude_unown))
        return self._filtered_cache[key]

    def effective_sources(self, source_logic: PokemonSourceLogic,
                          required_species: "set[str] | None" = None,
                          exclude_unown: bool = False) -> frozenset[str]:
        """Source set that matches the pool returned by get_filtered.

        Falls back to every active source when the configured filter is empty
        or any required species isn't obtainable from it. Rule sites should
        use this so gating matches the pool used to pick species; pass the same
        `exclude_unown` as the corresponding get_filtered call, or the emptiness
        check can disagree (e.g. a request pool of only UNOWN).
        """
        sources = frozenset(source_logic.value)
        pool = self._filter(sources, exclude_unown)
        if pool and (not required_species or required_species <= pool):
            return sources
        return self._world.active_sources

    def _filter(self, sources: frozenset[str], exclude_unown: bool) -> set[str]:
        self.ensure_base_pools()
        pool = {pokemon for pokemon, pokemon_sources in self._sources.items()
                if not pokemon_sources.isdisjoint(sources)}
        if exclude_unown:
            pool.discard("UNOWN")
        return pool

    def _compute_evolutions(self, available: set[str]) -> set[str]:
        from .evolution import evolution_in_logic
        world = self._world
        evolution_pokemon = set[str]()
        for evolver in world.logic.evolution.keys():
            world.logic.evolution[evolver] = []
        for evolving_pokemon in available:
            for evo in world.generated_pokemon[evolving_pokemon].evolutions:
                logical_access = (LogicalAccess.InLogic if evolution_in_logic(world, evo)
                                  else LogicalAccess.OutOfLogic)
                if not world.is_universal_tracker and logical_access is LogicalAccess.OutOfLogic:
                    continue
                world.logic.evolution[evolving_pokemon].append((evo, logical_access))
                if logical_access is LogicalAccess.InLogic:
                    evolution_pokemon.add(evo.pokemon)
        return evolution_pokemon

    def _compute_breeding(self, available: set[str]) -> set[str]:
        from .breeding import can_breed, breeding_requires_ditto
        world = self._world
        breeding_active = PokemonSourceLogic.BREEDING in world.active_sources
        if not breeding_active and not world.is_universal_tracker:
            return set()
        logical_access = LogicalAccess.InLogic if breeding_active else LogicalAccess.OutOfLogic
        breeding_pokemon = set[str]()
        for child in world.logic.breeding.keys():
            world.logic.breeding[child] = []
        for pokemon_id, data in world.generated_pokemon.items():
            if pokemon_id not in available:
                continue
            if not can_breed(world, pokemon_id):
                continue
            requires_ditto = breeding_requires_ditto(world, pokemon_id)
            world.logic.breeding[data.produces_egg].append((pokemon_id, logical_access, requires_ditto))
            if logical_access is LogicalAccess.InLogic:
                breeding_pokemon.add(data.produces_egg)
            if data.produces_egg == "NIDORAN_F":
                world.logic.breeding["NIDORAN_M"].append(
                    (pokemon_id, logical_access, breeding_requires_ditto(world, "NIDORAN_M")))
                if logical_access is LogicalAccess.InLogic:
                    breeding_pokemon.add("NIDORAN_M")
        return breeding_pokemon

    def _admit_trades(self, pool: set[str]) -> set[str]:
        """Received species of not-yet-admitted trades whose requested species is now in `pool`.

        Until the requests are assigned they're vanilla placeholders, so every trade is admitted:
        this pool builds the evolution/breeding locations, and must stay a superset of the final one.
        """
        from .utils import should_include_region
        world = self._world
        received = set[str]()
        if PokemonSourceLogic.TRADES not in world.active_sources:
            return received
        for region_data in crystal_data.regions.values():
            if not should_include_region(region_data, world):
                continue
            for trade_id in region_data.trades:
                if trade_id in self._completable_trades:
                    continue
                trade = world.generated_trades[trade_id]
                if self.trade_requests_assigned and trade.requested_pokemon not in pool:
                    continue
                self._completable_trades.add(trade_id)
                received.add(trade.received_pokemon)
        return received
