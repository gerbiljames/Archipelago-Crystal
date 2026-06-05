from .bases import PokemonCrystalTestBase, verify_location_access, verify_region_access
from ..items import EVOLUTION_ITEMS, item_const_name_to_label


class EvolutionItemsTest(PokemonCrystalTestBase):
    options = {}

    def test_at_least_one_of_each_in_pool(self):
        for item_const in EVOLUTION_ITEMS:
            label = item_const_name_to_label(item_const)
            count = sum(1 for item in self.multiworld.itempool if item.name == label)
            self.assertGreaterEqual(count, 1, f"{label} missing from the pool")

    def test_item_evolution_requires_item(self):
        verify_location_access(self, ["Water Stone"], ["Evolve Eevee into Vaporeon"])

    def test_trade_evolution_requires_link_cable(self):
        verify_location_access(self, ["Link Cable"], ["Evolve Machoke into Machamp"])

    def test_held_item_trade_evolution_requires_both_items(self):
        verify_location_access(self, ["Up-Grade"], ["Evolve Porygon into Porygon2"])
        verify_location_access(self, ["Link Cable"], ["Evolve Porygon into Porygon2"])
        verify_location_access(self, ["Metal Coat"], ["Evolve Onix into Steelix"])
        verify_location_access(self, ["Link Cable"], ["Evolve Onix into Steelix"])

    def test_link_cable_in_pool_once(self):
        count = sum(1 for item in self.multiworld.itempool if item.name == "Link Cable")
        self.assertEqual(count, 1)

    def test_omanyte_chamber_requires_water_stone(self):
        verify_region_access(self, ["Water Stone"], ["REGION_RUINS_OF_ALPH_OMANYTE_ITEM_ROOM"])


class EvolutionItemsNoHeldItemMethodTest(PokemonCrystalTestBase):
    options = {
        "evolution_methods_required": ["Level", "Level and Stat", "Use Item", "Happiness"],
    }

    def test_held_item_trade_evolutions_not_in_logic(self):
        with self.assertRaises(KeyError):
            self.multiworld.get_location("Evolve Onix into Steelix", self.player)
        # itemless trade evolutions are gated by Use Item and remain in logic
        self.multiworld.get_location("Evolve Machoke into Machamp", self.player)


class EvolutionItemsJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on",
    }

    def test_at_least_one_of_each_in_pool(self):
        for item_const in EVOLUTION_ITEMS:
            label = item_const_name_to_label(item_const)
            count = sum(1 for item in self.multiworld.itempool if item.name == label)
            self.assertGreaterEqual(count, 1, f"{label} missing from the pool")
