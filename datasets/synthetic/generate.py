"""Generate a deterministic replay fixture with synthetic room-level labels."""

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOMS = [
    {"id": "room-a", "name": "Room A", "length_m": 7, "width_m": 5},
    {"id": "room-b", "name": "Room B", "length_m": 6, "width_m": 4},
]
# Each frame holds (count, movement) for each room in room order.
SCENARIO = [
    [(0, "none"), (0, "none")],
    [(1, "moving"), (0, "none")],
    [(1, "still"), (1, "moving")],
    [(2, "moving"), (1, "still")],
    [(1, "moving"), (2, "moving")],
    [(0, "none"), (3, "still")],
    [(0, "none"), (2, "moving")],
    [(0, "none"), (0, "none")],
]


def make_replay():
    """Return two rooms with synchronized readings every 30 simulated seconds."""
    start = datetime(2026, 1, 1, 9, tzinfo=timezone.utc)
    readings = []
    for frame_index, frame in enumerate(SCENARIO):
        timestamp = (start + timedelta(seconds=30 * frame_index)).isoformat()
        for room, (count, movement) in zip(ROOMS, frame, strict=True):
            readings.append({
                "room_id": room["id"],
                "observed_at": timestamp,
                "occupied": count > 0,
                "occupant_count": count,
                "movement": movement,
            })
    return {"source": "simulated", "rooms": ROOMS, "readings": readings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="JSON path for the generated replay")
    output = parser.parse_args().output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(make_replay(), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
