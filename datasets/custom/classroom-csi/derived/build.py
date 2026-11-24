"""Summarize measured signal strength once per original classroom trial."""
import csv
from pathlib import Path
from statistics import mean, pstdev

root = Path(__file__).resolve().parents[1]
with (root / "index.csv").open(newline="") as index:
    trials = list(csv.DictReader(index))
out = root / "derived" / "trial_summary.csv"
with out.open("w", newline="") as handle:
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(["trial_folder", "room_activity", "corridor_activity", "frames", "rssi_mean_dbm", "rssi_sd_db"])
    for trial in trials:
        with (root / trial["trial_folder"] / "csi.csv").open(newline="") as capture:
            values = [int(row["rssi_dbm"]) for row in csv.DictReader(capture)]
        if len(values) != int(trial["frames"]):
            raise ValueError(f"Frame count mismatch in {trial['trial_folder']}")
        writer.writerow([trial["trial_folder"], trial["room_activity"], trial["corridor_activity"],
                         len(values), round(mean(values), 3), round(pstdev(values), 3)])
