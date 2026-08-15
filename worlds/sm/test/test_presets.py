import unittest

from ..variaRandomizer.utils.parameters import Settings
from ..variaRandomizer.utils.utils import PresetLoader, getPresetDir


def load_preset(player: int, name: str) -> None:
    PresetLoader.factory("/".join((getPresetDir(name), name + ".json"))).load(player)


class TestPresetIsolation(unittest.TestCase):
    def test_presets_do_not_leak_between_players(self) -> None:
        """Each player's preset settings must be independent of every other player's."""
        load_preset(1, "casual")
        load_preset(2, "newbie")

        casual = Settings.SettingsDict[1]
        newbie = Settings.SettingsDict[2]

        for table in ("bossesDifficulty", "hellRuns", "hardRooms"):
            with self.subTest(table=table):
                self.assertIsNot(getattr(casual, table), getattr(newbie, table))
                self.assertIsNot(getattr(casual, table), getattr(Settings, table))

        self.assertNotEqual(casual.bossesDifficulty["Kraid"], newbie.bossesDifficulty["Kraid"])

    def test_class_defaults_are_not_mutated(self) -> None:
        """Loading a preset must leave the class-level defaults untouched."""
        default_kraid = Settings.bossesDifficultyPresets["Kraid"]["Default"]
        load_preset(3, "newbie")
        self.assertEqual(Settings.bossesDifficulty["Kraid"], default_kraid)
