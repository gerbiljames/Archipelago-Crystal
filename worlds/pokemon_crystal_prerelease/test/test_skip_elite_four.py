from .bases import PokemonCrystalTestBase, verify_region_access


class SkipEliteFourRequirementTest(PokemonCrystalTestBase):
    options = {
        "skip_elite_four": "on",
        "randomize_badges": "completely_random",
        "victory_road_count": 0,
        "elite_four_requirement": "johto_badges",
        "elite_four_count": 8,
    }

    def test_skip_requires_elite_four_badges(self):
        verify_region_access(self, ["Hive Badge"], ["REGION_LANCES_ROOM", "REGION_HALL_OF_FAME"])
