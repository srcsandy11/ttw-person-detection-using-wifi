"""Offline binary predictions for a compatible HomeOccupancy-format CSI recording."""
import argparse
import json
from pathlib import Path
import joblib
from home_occupancy import read_session, WINDOW_PACKETS

def main():
    p = argparse.ArgumentParser()
    p.add_argument("recording", type=Path)
    p.add_argument("model", type=Path, help="Trusted joblib model from the group-fold workflow")
    p.add_argument("output", type=Path)
    args = p.parse_args()
    features, counts = read_session(args.recording)
    model = joblib.load(args.model)
    probabilities = model.predict_proba(features)[:, 1]
    report = {"recording": args.recording.name, "window_packets": WINDOW_PACKETS,
              "threshold": 0.5, "packet_counts": counts,
              "windows": [{"window_index": i, "occupied_probability": float(p),
                           "occupied": bool(p >= 0.5)} for i, p in enumerate(probabilities)]}
    args.output.write_text(json.dumps(report, indent=2) + "\n")

if __name__ == "__main__":
    main()
