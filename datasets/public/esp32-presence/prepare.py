#!/usr/bin/env python3
"""Reproduce the room-level ESP32 example from the pinned Mendeley CSV."""

import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SOURCE_SHA256 = "304d0b31f2c027e7889ff130958484980ab9cb7002de4d949b33c03359ea6994"
LABELS = {"empty": 0, "present": 1, "moving": 1}
PACKET_COLUMNS = ["pc_time", "session_id", "receiver_id", "interval_id", "label", "rssi", "channel", "csi_data"]
WINDOW_COLUMNS = [
    "room_id", "session_id", "interval_id", "window_index", "label", "occupied",
    "packet_count", "rssi_mean", "rssi_stdev", "csi_component_rms_mean",
    "csi_component_rms_stdev",
]


def write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.source.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != SOURCE_SHA256:
        parser.error("source does not match the pinned Mendeley CSV SHA-256")

    interval_start = {}
    interval_label = {}
    windows = defaultdict(list)
    excerpt_intervals = {}
    excerpt_counts = defaultdict(int)
    excerpt = []
    with args.source.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            label = row["label"]
            if label not in LABELS:
                continue
            room = row["receiver_id"]
            session = row["session_id"]
            interval = int(row["interval_id"])
            key = (room, session, interval)
            if interval_label.setdefault(key, label) != label:
                raise ValueError(f"mixed labels in source interval {key}")
            time = datetime.fromisoformat(row["pc_time"])
            elapsed = (time - interval_start.setdefault(key, time)).total_seconds()
            if elapsed < 0:
                raise ValueError(f"packet acquired before start of interval {key}")
            components = json.loads(row["csi_data"])
            if not components:
                raise ValueError(f"empty CSI vector in source interval {key}")
            rms = math.sqrt(statistics.mean(value * value for value in components))
            windows[(*key, int(elapsed // 2), label)].append((int(row["rssi"]), rms))

            excerpt_key = (room, session, label)
            if interval == excerpt_intervals.setdefault(excerpt_key, interval) and excerpt_counts[excerpt_key] < 4:
                excerpt.append([row[column] for column in PACKET_COLUMNS])
                excerpt_counts[excerpt_key] += 1

    features = []
    for (room, session, interval, window, label), packets in sorted(windows.items()):
        if len(packets) < 8:
            continue
        rssi, rms = zip(*packets)
        values = [statistics.mean(rssi), statistics.pstdev(rssi), statistics.mean(rms), statistics.pstdev(rms)]
        features.append([room, session, interval, window, label, LABELS[label], len(packets),
                         *(f"{value:.6f}" for value in values)])
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "packets.csv", PACKET_COLUMNS, excerpt)
    write_csv(args.output / "windows.csv", WINDOW_COLUMNS, features)


if __name__ == "__main__":
    main()
