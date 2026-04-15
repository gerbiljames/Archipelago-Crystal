from .bases import PokemonCrystalTestBase

from ..data import data
from ..rom import _build_reverse_conn_lookup


def _simulate_elevator_writes(er_pairings):
    """Simulate write_entrance_pairings and return {(label, offset): (warp, group, map)} for elevator labels."""
    conns = data.entrance_connections
    reverse_lookup = _build_reverse_conn_lookup(conns)
    map_consts = data.map_constants

    writes: dict[tuple[str, int], tuple[int, int, int]] = {}
    for source_name, target_name in er_pairings:
        source_conn = conns.get(source_name)
        if source_conn is None:
            continue

        if target_name.endswith(" (one-way target)"):
            target_conn = conns.get(target_name.removesuffix(" (one-way target)"))
        else:
            reverse_target_name = reverse_lookup.get(target_name)
            target_conn = conns.get(reverse_target_name) if reverse_target_name else None
        if target_conn is None:
            continue

        arrival_const = target_conn.arrival_map_const
        if arrival_const not in map_consts:
            continue
        new_group, new_map_id = map_consts[arrival_const]
        new_warp_id = target_conn.arrival_warp_id

        for exit_warp in source_conn.exit_warps:
            if exit_warp.label and exit_warp.label.startswith("AP_ElevFloor_"):
                writes[(exit_warp.label, exit_warp.addr_offset)] = (new_warp_id, new_group, new_map_id)

    return writes


def _get_elevator_labels():
    """Return all AP_ElevFloor_* labels from entrance_data."""
    labels: set[str] = set()
    for conn in data.entrance_connections.values():
        if conn.entrance_type == "elevator":
            for ew in conn.exit_warps:
                if ew.label and ew.label.startswith("AP_ElevFloor_"):
                    labels.add(ew.label)
    return sorted(labels)


def _get_elevator_conn_names():
    """Return (forward_names, reverse_names) sets for elevator connections."""
    forward = set()  # "Floor -> Elevator:NF" connections
    reverse = set()  # "Elevator:NF -> Floor" connections
    for name, conn in data.entrance_connections.items():
        if conn.entrance_type != "elevator":
            continue
        if "ELEVATOR:" in conn.entrance_region:
            forward.add(name)
        elif "ELEVATOR:" in conn.exit_region:
            reverse.add(name)
    return forward, reverse


class ElevatorConnectionStructureTest(PokemonCrystalTestBase):
    """Verify elevator connections in entrance_data have the correct format."""
    auto_construct = False

    def test_forward_patches_floor_warp_and_entry_map(self):
        """Forward (Floor -> Elevator:NF) should patch the floor warp_event and elevfloor entry map (offset 4)."""
        for name, conn in data.entrance_connections.items():
            if conn.entrance_type != "elevator" or "ELEVATOR:" not in conn.entrance_region:
                continue
            regular_warps = [ew for ew in conn.exit_warps if ew.label is None]
            elev_warps = [ew for ew in conn.exit_warps if ew.label is not None]
            self.assertGreaterEqual(len(regular_warps), 1, f"{name}: expected at least 1 regular warp")
            for ew in regular_warps:
                self.assertEqual(ew.addr_offset, 2, f"{name}: regular warp addr_offset should be 2")
            self.assertEqual(len(elev_warps), 1, f"{name}: expected 1 elevfloor warp")
            self.assertEqual(elev_warps[0].addr_offset, 4, f"{name}: elevfloor addr_offset should be 4")

    def test_reverse_patches_exit_map(self):
        """Reverse (Elevator:NF -> Floor) should patch elevfloor exit map (offset 1)."""
        for name, conn in data.entrance_connections.items():
            if conn.entrance_type != "elevator" or "ELEVATOR:" not in conn.exit_region:
                continue
            self.assertEqual(len(conn.exit_warps), 1, f"{name}: expected 1 exit_warp")
            self.assertEqual(conn.exit_warps[0].addr_offset, 1, f"{name}: addr_offset should be 1")

    def test_forward_arrival_points_to_elevator_room(self):
        """Forward connection arrival should point to the elevator room."""
        elevator_rooms = {"CeladonDeptStoreElevator", "GoldenrodDeptStoreElevator"}
        for name, conn in data.entrance_connections.items():
            if conn.entrance_type != "elevator" or "ELEVATOR:" not in conn.entrance_region:
                continue
            self.assertIn(conn.arrival_map, elevator_rooms,
                          f"{name}: arrival should be elevator room, got {conn.arrival_map}")

    def test_forward_and_reverse_share_label(self):
        """Forward and reverse for the same floor should patch the same AP_ElevFloor label."""
        labels_by_floor: dict[str, set[str]] = {}
        for conn in data.entrance_connections.values():
            if conn.entrance_type != "elevator":
                continue
            for ew in conn.exit_warps:
                if ew.label and ew.label.startswith("AP_ElevFloor_"):
                    labels_by_floor.setdefault(ew.label, set()).add(conn.name)
        for label, conn_names in labels_by_floor.items():
            self.assertEqual(len(conn_names), 2,
                             f"{label}: expected 2 connections, got {conn_names}")


class ElevatorERCoupledTest(PokemonCrystalTestBase):
    options = {
        "entrance_randomization": ["Elevator", "Building"],
        "entrance_randomization_coupled": True,
    }

    def test_both_directions_appear_as_source(self):
        """Both forward and reverse elevator connections should appear as pairing sources."""
        forward_names, reverse_names = _get_elevator_conn_names()
        sources = {src for src, _ in self.world.er_pairings}
        for name in forward_names:
            self.assertIn(name, sources, f"Forward '{name}' not in pairing sources")
        for name in reverse_names:
            self.assertIn(name, sources, f"Reverse '{name}' not in pairing sources")

    def test_all_elevator_labels_patched(self):
        """Every elevator label should have both exit (offset 1) and entry (offset 4) writes."""
        writes = _simulate_elevator_writes(self.world.er_pairings)
        for label in _get_elevator_labels():
            self.assertIn((label, 1), writes, f"No exit write (offset 1) for {label}")
            self.assertIn((label, 4), writes, f"No entry write (offset 4) for {label}")


class ElevatorERDecoupledTest(PokemonCrystalTestBase):
    options = {
        "entrance_randomization": ["Elevator", "Building"],
        "entrance_randomization_coupled": False,
    }

    def test_decoupled_generates(self):
        """Decoupled ER with elevators should generate without errors."""
        self.assertTrue(len(self.world.er_pairings) > 0)

    def test_all_elevator_labels_patched(self):
        """Every elevator label should have both exit and entry writes."""
        writes = _simulate_elevator_writes(self.world.er_pairings)
        for label in _get_elevator_labels():
            self.assertIn((label, 1), writes, f"No exit write (offset 1) for {label}")
            self.assertIn((label, 4), writes, f"No entry write (offset 4) for {label}")
