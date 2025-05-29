import sys
import os
import unittest

if len(sys.argv) != 3:
    print("Usage: tests.py apworld_name game_name")
    sys.exit(1)


ap_root = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), "../../")
sys.path.insert(0, ap_root)
import Utils

Utils.local_path.cached_path = ap_root
Utils.user_path()

from worlds.AutoWorld import AutoWorldRegister
from worlds.Files import AutoPatchRegister
from test.bases import WorldTestBase

apworld_name = sys.argv[1]
world_name = sys.argv[2]

# Shamelessly stolen from https://github.com/Eijebong/Archipelago-yaml-checker
# Unload as many worlds as possible before running tests
loaded_worlds = list(AutoWorldRegister.world_types.keys())
for loaded_world in loaded_worlds:
    # Those 2 worlds are essential to testing, don't unload them. Hopefully in the future ALTTP can get yeeted from here too.
    if loaded_world in ("Test Game", "A Link to the Past"):
        continue

    if loaded_world != world_name:
        del AutoWorldRegister.world_types[loaded_world]

        if loaded_world in AutoPatchRegister.patch_types:
            del AutoPatchRegister.patch_types[loaded_world]


class FilteredTestCase(unittest.TestCase):
    def subTest(self, msg=None, **params):
        if 'game' in params and params['game'] != world_name:
            self.skipTest("Game isn't what's being tested")
            return

        return super().subTest(msg, **params)


unittest.TestCase = FilteredTestCase

class WorldTest(WorldTestBase):
    game = world_name


runner = unittest.TextTestRunner(verbosity=1)

suite = unittest.TestSuite()
suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(WorldTest))
suite.addTests(unittest.defaultTestLoader.discover("test/general", top_level_dir="."))
suite.addTests(unittest.defaultTestLoader.discover(f"worlds/{apworld_name}/test", top_level_dir="."))
results = runner.run(suite)

if not results.wasSuccessful():
    sys.exit(1)
