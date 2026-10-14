from .bases import PokemonCrystalTestBase
from ..items import PokemonCrystalItem
from ..options import PokemonSourceLogic, PokemonRequestLogic, DexsanityLogic

HM_LOGIC_WITH_TRADES = ["Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest", "Statics",
                        "Evolution", "Breeding", "Trades"]


class SourceTaggingTest(PokemonCrystalTestBase):
    """Species event items emitted at source-specific locations carry the matching source tag."""
    options = {
        "randomize_wilds": "completely_random",
        "randomize_trades": "both",
        "randomize_pokemon_requests": "pokemon",
        "hm_logic": HM_LOGIC_WITH_TRADES,
    }

    def test_wild_events_tagged_with_encounter_source(self):
        # Every locked species event placed at a wild slot must carry a wild source
        # (Land/Surfing/Fishing/Headbutt/Rock Smash) and a matching source_key.
        wild_sources = {
            PokemonSourceLogic.LAND, PokemonSourceLogic.SURFING, PokemonSourceLogic.FISHING,
            PokemonSourceLogic.HEADBUTT, PokemonSourceLogic.ROCK_SMASH,
        }
        wild_tagged = [loc for loc in self.multiworld.get_locations(self.player)
                       if isinstance(loc.item, PokemonCrystalItem)
                       and loc.item.source in wild_sources]
        self.assertTrue(wild_tagged, "expected at least one wild-tagged species event")
        for loc in wild_tagged:
            item = loc.item
            self.assertEqual(item.source_key, f"{item.name}@{item.source}",
                             f"source_key mismatch on {loc.name}")

    def test_trade_event_tagged_trades(self):
        # Trades are placed for any randomized trade location.
        trade_locations = [loc for loc in self.multiworld.get_locations(self.player)
                           if loc.name.startswith("TRADE_") and loc.item is not None]
        self.assertTrue(trade_locations, "expected at least one trade location with an item")
        for loc in trade_locations:
            self.assertEqual(loc.item.source, PokemonSourceLogic.TRADES,
                             f"trade location {loc.name} not tagged TRADES")

    def test_non_species_event_has_no_source(self):
        # Pokegear / generic events shouldn't be tagged.
        for loc in self.multiworld.get_locations(self.player):
            item = loc.item
            if not isinstance(item, PokemonCrystalItem):
                continue
            if item.source is None:
                self.assertIsNone(item.source_key)


class StateMixinInitTest(PokemonCrystalTestBase):
    """The PokemonCrystalCollectionState mixin attaches per-player counters."""
    options = {}

    def test_mixin_attributes_present(self):
        state = self.multiworld.state
        self.assertIn(self.player, state.pc_dex_species_count)
        self.assertIn(self.player, state.pc_dex_species_seen)
        self.assertIn(self.player, state.pc_diploma_species_count)
        self.assertIn(self.player, state.pc_diploma_species_seen)


class CollectRemoveCountersTest(PokemonCrystalTestBase):
    """Collecting and removing tagged species events maintains the mixin counters."""
    options = {}

    def _make_species_item(self, name: str, source: str) -> PokemonCrystalItem:
        return self.world.create_event(name, source=source)

    def test_collect_bumps_diploma_and_dex(self):
        # Default dexsanity_logic and diploma_logic include LAND; collecting a LAND-tagged species bumps both.
        state = self.multiworld.state
        before_unique = state.pc_diploma_species_count[self.player]
        before_dex = state.pc_dex_species_count[self.player]

        item = self._make_species_item("PIKACHU", PokemonSourceLogic.LAND)
        state.collect(item, prevent_sweep=True)

        self.assertEqual(state.pc_diploma_species_count[self.player], before_unique + 1)
        self.assertEqual(state.pc_dex_species_count[self.player], before_dex + 1)
        self.assertIn("PIKACHU", state.pc_dex_species_seen[self.player])
        self.assertEqual(state.prog_items[self.player][f"PIKACHU@{PokemonSourceLogic.LAND}"], 1)

    def test_remove_decrements(self):
        state = self.multiworld.state
        item = self._make_species_item("PIKACHU", PokemonSourceLogic.LAND)
        state.collect(item, prevent_sweep=True)
        before_unique = state.pc_diploma_species_count[self.player]
        before_dex = state.pc_dex_species_count[self.player]

        state.remove(item)

        self.assertEqual(state.pc_diploma_species_count[self.player], before_unique - 1)
        self.assertEqual(state.pc_dex_species_count[self.player], before_dex - 1)
        self.assertNotIn("PIKACHU", state.pc_dex_species_seen[self.player])
        self.assertEqual(state.prog_items[self.player][f"PIKACHU@{PokemonSourceLogic.LAND}"], 0)

    def test_two_sources_one_species_count_once(self):
        # Same species collected via two different dex sources only bumps dex count once.
        state = self.multiworld.state
        before_dex = state.pc_dex_species_count[self.player]

        wild = self._make_species_item("PIKACHU", PokemonSourceLogic.LAND)
        evo = self._make_species_item("PIKACHU", PokemonSourceLogic.EVOLUTION)
        state.collect(wild, prevent_sweep=True)
        state.collect(evo, prevent_sweep=True)

        self.assertEqual(state.pc_dex_species_count[self.player], before_dex + 1)
        # Removing one source still leaves the species via the other source.
        state.remove(wild)
        self.assertEqual(state.pc_dex_species_count[self.player], before_dex + 1)
        self.assertIn("PIKACHU", state.pc_dex_species_seen[self.player])
        # Removing the last source drops the dex count.
        state.remove(evo)
        self.assertEqual(state.pc_dex_species_count[self.player], before_dex)
        self.assertNotIn("PIKACHU", state.pc_dex_species_seen[self.player])


class DexCounterIgnoresNonDexSourceTest(PokemonCrystalTestBase):
    """A species collected via a source not in dexsanity_logic does not bump pc_dex_species_count."""
    options = {
        "dexsanity_logic": ["Land"],  # only LAND counts for dex
    }

    def test_breeding_source_does_not_bump_dex(self):
        state = self.multiworld.state
        before_dex = state.pc_dex_species_count[self.player]

        bred = self.world.create_event("PICHU", source=PokemonSourceLogic.BREEDING)
        state.collect(bred, prevent_sweep=True)

        # BREEDING isn't in dex_sources, so dex count should be unchanged.
        self.assertEqual(state.pc_dex_species_count[self.player], before_dex)
        # Default diploma_logic includes BREEDING, so the diploma count is still bumped.
        self.assertGreater(state.pc_diploma_species_count[self.player], 0)


class EffectiveSourcesFallbackTest(PokemonCrystalTestBase):
    """An empty pokemon_request_logic falls back to every active source at rule-set time."""
    options = {
        "pokemon_request_logic": [],
        "randomize_pokemon_requests": "pokemon",
    }

    def test_request_sources_fall_back_to_active(self):
        # set_rules has run and stashed effective sources on the world.
        self.assertEqual(self.world.request_sources, self.world.active_sources)


class TradesInSourcesTest(PokemonCrystalTestBase):
    """TRADES is a valid source for both dexsanity and requests, but off by default."""
    options = {}

    def test_trades_in_dex_valid_keys(self):
        self.assertIn(PokemonSourceLogic.TRADES, DexsanityLogic.valid_keys)
        self.assertNotIn(PokemonSourceLogic.TRADES, DexsanityLogic.default)

    def test_trades_in_request_valid_keys(self):
        self.assertIn(PokemonSourceLogic.TRADES, PokemonRequestLogic.valid_keys)
        self.assertNotIn(PokemonSourceLogic.TRADES, PokemonRequestLogic.default)

    def test_trades_not_active_by_default(self):
        self.assertNotIn(PokemonSourceLogic.TRADES, self.world.active_sources)


class TradesAcyclicTest(PokemonCrystalTestBase):
    """No trade waits on another trade's reward.

    Johto-only vanilla wilds leave plenty of species obtainable only from a trade, so drawing
    every request from the finished pool deadlocks a chunk of seeds here.
    """
    options = {
        "randomize_trades": "both",
        "hm_logic": HM_LOGIC_WITH_TRADES,
        "johto_only": "on",
        "randomize_wilds": "vanilla",
        "randomize_pokemon_requests": "pokemon",
    }

    def test_trades_reachable(self):
        state = self.world.get_world_collection_state()
        trade_locations = [loc for loc in self.multiworld.get_locations(self.player)
                           if loc.name.startswith("TRADE_")]
        self.assertTrue(trade_locations)
        for location in trade_locations:
            self.assertTrue(location.can_reach(state), f"{location.name} unreachable with everything collected")


class TradesAsRequestSourceTest(PokemonCrystalTestBase):
    """With only Trades selected, requests draw from trade-received Pokemon."""
    options = {
        "pokemon_request_logic": ["Trades"],
        "randomize_pokemon_requests": "pokemon",
        "randomize_trades": "both",
        "hm_logic": HM_LOGIC_WITH_TRADES,
    }

    def test_requests_gated_on_trades(self):
        self.assertIn(PokemonSourceLogic.TRADES, self.world.request_sources)
        trade_species = {trade.received_pokemon for trade in self.world.generated_trades.values()}
        self.assertTrue(set(self.world.generated_request_pokemon) <= trade_species)

    def test_sources_fall_back_when_trades_are_the_only_source(self):
        # Trades pick from the active-sources fallback, so gating has to widen to match.
        self.assertEqual(self.world.request_sources, self.world.active_sources)


class RequestPicksAreGrantedTest(PokemonCrystalTestBase):
    """Picked species always have an event item granting them.

    Evolution and breeding locations are built from the pool as it stands in create_regions, so a
    pool that grew afterwards would let a pick land on a species nothing grants.
    """
    options = {
        "randomize_trades": "both",
        "hm_logic": HM_LOGIC_WITH_TRADES,
        "randomize_pokemon_requests": "pokemon",
        "pokemon_request_logic": ["Trades", "Evolution"],
    }

    def test_picked_species_have_event_items(self):
        granted = {item.name for item in self.multiworld.get_items() if item.source_key is not None}
        picks = set(self.world.generated_request_pokemon) | {trade.requested_pokemon for trade
                                                             in self.world.generated_trades.values()}
        self.assertFalse(sorted(picks - granted), "picked species with no event item")


class IndependentGroupsTest(PokemonCrystalTestBase):
    """A source only in dexsanity_logic is in logic, counts for dex, but not for HMs."""
    options = {
        "dexsanity": 20,
        "hm_logic": ["Land", "Surfing", "Fishing", "Statics", "Evolution", "Breeding"],
        "pokemon_request_logic": ["Land", "Surfing", "Fishing", "Statics", "Evolution", "Breeding"],
        "dexsanity_logic": ["Headbutt"],
    }

    def test_dex_only_source_is_active(self):
        self.assertIn(PokemonSourceLogic.HEADBUTT, self.world.active_sources)
        self.assertIn(PokemonSourceLogic.HEADBUTT, self.world.dex_sources)
        self.assertNotIn(PokemonSourceLogic.HEADBUTT, self.world.hm_sources)

    def test_dex_only_source_does_not_teach(self):
        species = next(iter(self.world.logic.pokemon_hm_use))
        state = self.multiworld.state
        before = state.prog_items[self.player].copy()
        state.collect(self.world.create_event(species, source=PokemonSourceLogic.HEADBUTT), prevent_sweep=True)
        for teach in self.world.logic.pokemon_hm_use[species]:
            self.assertEqual(state.prog_items[self.player][teach], before[teach])


class DisabledGroupIsInactiveTest(PokemonCrystalTestBase):
    """dexsanity_logic doesn't add sources while dexsanity is off."""
    options = {
        "dexsanity": 0,
        "dexcountsanity": 0,
        "hm_logic": ["Land", "Surfing", "Fishing", "Statics", "Evolution", "Breeding"],
        "pokemon_request_logic": ["Land", "Surfing", "Fishing", "Statics", "Evolution", "Breeding"],
        "dexsanity_logic": ["Headbutt"],
    }

    def test_headbutt_not_active(self):
        self.assertNotIn(PokemonSourceLogic.HEADBUTT, self.world.active_sources)


class DiplomaLogicTest(PokemonCrystalTestBase):
    """The diploma counts only species from diploma_logic sources."""
    options = {
        "goal": ["Diploma"],
        "diploma_logic": ["Land"],
    }

    def test_diploma_count_matches_diploma_pool(self):
        self.assertEqual(self.world.pokemon_pool.diploma_count,
                         len(self.world.pokemon_pool.get_filtered(self.world.options.diploma_logic)))
        self.assertEqual(self.world.diploma_sources, frozenset({PokemonSourceLogic.LAND}))

    def test_non_diploma_source_not_counted(self):
        state = self.multiworld.state
        before = state.pc_diploma_species_count[self.player]
        state.collect(self.world.create_event("PICHU", source=PokemonSourceLogic.BREEDING), prevent_sweep=True)
        self.assertEqual(state.pc_diploma_species_count[self.player], before)
