"""Fast unit tests for the under-test item pool-removal logic."""

import unittest
from collections import Counter

from BaseClasses import Item, ItemClassification

from .. import remove_relocated_items

PROG = ItemClassification.progression
FILLER = ItemClassification.filler


def _item(name, classification, player=1):
    return Item(name, classification, 1, player)


class TestRemoveRelocatedItems(unittest.TestCase):
    def test_removes_all_recorded_copies_regardless_of_class(self):
        # Every networkable copy of a name is relocated, so both the progression
        # and filler copies of "Dup" must be removed.
        pool = [_item("Dup", FILLER), _item("Dup", PROG), _item("Other", FILLER)]
        new_pool, leftover = remove_relocated_items(pool, 1, Counter({"Dup": 2, "Other": 1}))

        self.assertEqual(leftover, 0)
        self.assertEqual([i.name for i in new_pool], [])

    def test_removes_exact_counts(self):
        pool = [_item("Badge", PROG) for _ in range(3)] + [_item("Potion", FILLER)]
        new_pool, leftover = remove_relocated_items(pool, 1, Counter({"Badge": 3, "Potion": 1}))

        self.assertEqual(leftover, 0)
        self.assertEqual(new_pool, [])

    def test_ignores_other_players(self):
        pool = [_item("Key", PROG, player=2), _item("Key", PROG, player=1)]
        new_pool, leftover = remove_relocated_items(pool, 1, Counter({"Key": 1}))

        self.assertEqual(leftover, 0)
        self.assertEqual([(i.name, i.player) for i in new_pool], [("Key", 2)])

    def test_reports_leftover_when_not_found(self):
        pool = [_item("X", FILLER)]
        new_pool, leftover = remove_relocated_items(pool, 1, Counter({"Missing": 1}))

        self.assertEqual(leftover, 1)
        self.assertEqual(len(new_pool), 1)
