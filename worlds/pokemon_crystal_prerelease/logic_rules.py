import dataclasses
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import Rule

from .data import data as crystal_data

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

GAME = crystal_data.manifest.game


class _DescribedResolved(Rule.Resolved):
    """Base for the world's custom rules that renders `/explain` output as a `Has`/`Missing`
    phrase, coloured by whether the rule is satisfied in the given state."""

    def _describe(self, state: CollectionState | None) -> str:
        """Human-readable noun phrase for what this rule requires."""
        raise NotImplementedError

    @override
    def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
        text = self._describe(state)
        if state is None:
            return [{"type": "text", "text": f"Has {text}"}]
        satisfied = self(state)
        return [
            {"type": "text", "text": "Has " if satisfied else "Missing "},
            {"type": "color", "color": "green" if satisfied else "salmon", "text": text},
        ]

    @override
    def explain_str(self, state: CollectionState | None = None) -> str:
        prefix = "Has" if state is None or self(state) else "Missing"
        return f"{prefix} {self._describe(state)}"


@dataclasses.dataclass()
class HasNPokemon(Rule["PokemonCrystalWorld"], game=GAME):
    """At least `count` unique caught species, tracked by the world's collect/remove hooks."""

    count: int

    @override
    def _instantiate(self, world: "PokemonCrystalWorld") -> Rule.Resolved:
        return self.Resolved(
            self.count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(_DescribedResolved):
        count: int
        # Depends on a custom counter, not prog_items, so it can't use the item-dependency cache.
        force_recalculate: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.pc_unique_species[self.player] >= self.count

        @override
        def _describe(self, state: CollectionState | None) -> str:
            return f"{self.count} unique Pokemon"


class _HasSpeciesKeys(_DescribedResolved):
    """Player has at least one of a set of per-source `species@source` items.

    Both the source set and (for requests) the assigned species are finalized in connect_entrances,
    after set_rules, so they are read dynamically from the world each evaluation rather than
    snapshotted at resolve time. The world is fetched from the state (not stored on the resolved
    rule) because resolved rules are interned in a process-lifetime cache and would otherwise leak it.
    """

    force_recalculate: ClassVar[bool] = True

    def _keys(self, world: "PokemonCrystalWorld") -> tuple[str, ...]:
        raise NotImplementedError

    @override
    def _evaluate(self, state: CollectionState) -> bool:
        world = state.multiworld.worlds[self.player]
        pi = state.prog_items[self.player]
        return any(pi[k] for k in self._keys(world))


@dataclasses.dataclass()
class HasSpeciesDex(Rule["PokemonCrystalWorld"], game=GAME):
    """Player can register `species` in the dex via any of its in-logic dex sources."""

    species: str

    @override
    def _instantiate(self, world: "PokemonCrystalWorld") -> Rule.Resolved:
        return self.Resolved(
            self.species,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(_HasSpeciesKeys):
        species: str

        @override
        def _keys(self, world: "PokemonCrystalWorld") -> tuple[str, ...]:
            return world._get_dex_keys(self.species)

        @override
        def _describe(self, state: CollectionState | None) -> str:
            if state is None:
                return f"{self.species} in the Pokedex"
            world = state.multiworld.worlds[self.player]
            return f"{world.generated_pokemon[self.species].friendly_name} in the Pokedex"


@dataclasses.dataclass()
class HasRequestSlot(Rule["PokemonCrystalWorld"], game=GAME):
    """Player can satisfy the pokemon request assigned to `generated_request_pokemon[slot]`.

    The assigned species is randomized after set_rules, so it is looked up by slot at eval time.
    """

    slot: int

    @override
    def _instantiate(self, world: "PokemonCrystalWorld") -> Rule.Resolved:
        return self.Resolved(
            self.slot,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(_HasSpeciesKeys):
        slot: int

        @override
        def _keys(self, world: "PokemonCrystalWorld") -> tuple[str, ...]:
            return world._get_request_keys(world.generated_request_pokemon[self.slot])

        @override
        def _describe(self, state: CollectionState | None) -> str:
            if state is None:
                return "the requested Pokemon"
            world = state.multiworld.worlds[self.player]
            species = world.generated_request_pokemon[self.slot]
            return f"{world.generated_pokemon[species].friendly_name} (for a request)"


@dataclasses.dataclass()
class HasTradeRequest(Rule["PokemonCrystalWorld"], game=GAME):
    """Player can satisfy the request for the pokemon traded by `generated_trades[trade_id]`.

    The traded species is randomized after set_rules, so it is looked up by trade id at eval time.
    """

    trade_id: str

    @override
    def _instantiate(self, world: "PokemonCrystalWorld") -> Rule.Resolved:
        return self.Resolved(
            self.trade_id,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(_HasSpeciesKeys):
        trade_id: str

        @override
        def _keys(self, world: "PokemonCrystalWorld") -> tuple[str, ...]:
            return world._get_request_keys(world.generated_trades[self.trade_id].requested_pokemon)

        @override
        def _describe(self, state: CollectionState | None) -> str:
            if state is None:
                return "the traded Pokemon"
            world = state.multiworld.worlds[self.player]
            species = world.generated_trades[self.trade_id].requested_pokemon
            return f"{world.generated_pokemon[species].friendly_name} (for a trade)"


@dataclasses.dataclass()
class HasDexCount(Rule["PokemonCrystalWorld"], game=GAME):
    """At least `count` species registered in the dex, tracked by the world's collect/remove hooks."""

    count: int

    @override
    def _instantiate(self, world: "PokemonCrystalWorld") -> Rule.Resolved:
        return self.Resolved(
            self.count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(_DescribedResolved):
        count: int
        force_recalculate: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.pc_dex_species_count[self.player] >= self.count

        @override
        def _describe(self, state: CollectionState | None) -> str:
            return f"{self.count} Pokedex registrations"
