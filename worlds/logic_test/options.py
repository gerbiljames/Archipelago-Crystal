from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle


class CountEvents(Toggle):
    """Whether in-game events cause a sphere boundary.

    Off (default): events never create a boundary (the canonical sendable-sphere
    grouping); they are still collected in dependency order, so spheres come out
    coarser.
    On: an item unlocked by an event that became reachable in a wave lands in the
    next sphere, so events create boundaries: finer spheres, faithful to real
    play order.
    """
    display_name = "Count Events For Spheres"


@dataclass
class LogicTestOptions(PerGameCommonOptions):
    count_events: CountEvents
