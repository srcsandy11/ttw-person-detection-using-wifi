"""Binary room occupancy on the public HomeOccupancy session holdout."""

import argparse
import json
import os
import re
import warnings
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)

DATASET = "gadgadgad/HomeOccupancy"
REVISION = "6eda463a036aa3d8b471522fb3d8828a1c2866ee"
BASE_URL = f"https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}"
CLASSES = ("empty", "sleep", "work")
WINDOW_PACKETS = 256
SEED = 42
MIN_PACKETS = 10_000
CSI_ROW = re.compile(rb'^CSI_DATA,.*?\[([^\[\]]+)\]"?\s*$')
INTEGER = re.compile(rb"^-?\d+$")
SUBCARRIERS = np.r_[6:32, 33:59]


def decode_packet(line):
    """Accept quoted or unquoted arrays while rejecting ambiguous packets."""
    match = CSI_ROW.fullmatch(line.rstrip())
    if match is None:
        return None
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        try:
            packet = np.fromstring(match[1], sep=",", dtype=np.int16)
        except (ValueError, DeprecationWarning):
            return None
    if len(packet) != 128 or np.any(packet < -128) or np.any(packet > 127):
        return None
    # fromstring may silently accept a partial token on some NumPy releases.
    if not INTEGER.fullmatch(match[1].rsplit(b",", 1)[-1].strip()):
        return None
    return packet


def window_features(packets):
    pairs = np.asarray(packets, dtype=np.float32).reshape(-1, 64, 2)
    amplitude = np.hypot(pairs[:, SUBCARRIERS, 0], pairs[:, SUBCARRIERS, 1])
    amplitude /= np.maximum(amplitude.mean(axis=1, keepdims=True), 1e-6)
    # Summarize movement within a window using relative CSI magnitudes only.
    variation = amplitude.std(axis=0)
    steps = np.abs(np.diff(amplitude, axis=0))
    return np.concatenate((variation, steps.mean(axis=0), np.quantile(steps, 0.9, axis=0)))


def read_session(path):
    """Process one file in source order without materializing all raw packets."""
    features, window = [], []
    valid = rejected = ignored = 0
    with path.open("rb") as source:
        for line in source:
            if not line.startswith(b"CSI_DATA,"):
                ignored += 1
                continue
            packet = decode_packet(line)
            if packet is None:
                rejected += 1
                continue
            valid += 1
            window.append(packet)
            if len(window) == WINDOW_PACKETS:
                features.append(window_features(window))
                window.clear()

    if valid < MIN_PACKETS:
        raise ValueError(f"{path.name}: expected at least {MIN_PACKETS} valid packets, got {valid}")
    return np.asarray(features), {
        "valid_packets": valid,
        "rejected_csi_rows": rejected,
        "ignored_nonpacket_rows": ignored,
        "discarded_tail_packets": len(window),
        "windows": len(features),
    }


def scores(target, predicted, probability):
    precision, recall, f1, _ = precision_recall_fscore_support(
        target, predicted, average="binary", zero_division=0
    )
    return {
        "accuracy": accuracy_score(target, predicted),
        "balanced_accuracy": balanced_accuracy_score(target, predicted),
        "occupied_precision": precision,
        "occupied_recall": recall,
        "occupied_f1": f1,
        "roc_auc": roc_auc_score(target, probability),
        "average_precision": average_precision_score(target, probability),
        "confusion_matrix_empty_occupied": confusion_matrix(
            target, predicted, labels=[0, 1]
        ).tolist(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    sets = {"train": [], "test": []}
    sessions = {}
    for category in CLASSES:
        for number in (1, 2, 3):
            name = f"{category}_{number}.csv"
            split = "test" if number == 3 else "train"
            features, counts = read_session(args.data_dir / name)
            label = int(category != "empty")
            sessions[name] = {"split": split, "label": label, **counts}
            sets[split].append((name, features, np.full(len(features), label)))
            print(name, sessions[name], flush=True)

    _, training_features, training_labels = zip(*sets["train"])
    names, test_features, test_labels = zip(*sets["test"])
    training_target = np.concatenate(training_labels)
    test_target = np.concatenate(test_labels)
    model = RandomForestClassifier(
        n_estimators=300, max_depth=12, min_samples_leaf=8,
        class_weight="balanced", random_state=SEED, n_jobs=2,
    )
    model.fit(np.concatenate(training_features), training_target)
    probability = model.predict_proba(np.concatenate(test_features))[:, 1]
    predicted = (probability >= 0.5).astype(int)
    majority = int(np.bincount(training_target).argmax())
    baseline = np.full(test_target.shape, majority)
    offset = 0
    for name, labels in zip(names, test_labels):
        end = offset + len(labels)
        sessions[name]["correct_windows"] = int(np.sum(labels == predicted[offset:end]))
        sessions[name]["correct_fraction"] = float(np.mean(labels == predicted[offset:end]))
        offset = end

    report = {
        "dataset": DATASET,
        "revision": REVISION,
        "dataset_license": "CC BY 4.0",
        "dataset_authors": ["Gad Gad", "Iqra Batool", "Mostafa M. Fouda",
                            "Shikhar Verma", "Zubair Md Fadlullah"],
        "dataset_url": f"https://huggingface.co/datasets/{DATASET}/tree/{REVISION}",
        "scope": "binary occupancy, one residential room, held-out sessions",
        "window_packets": WINDOW_PACKETS,
        "random_seed": SEED,
        "training_windows": len(training_target),
        "test_windows": len(test_target),
        "majority_baseline_class": majority,
        "majority_baseline": scores(test_target, baseline, baseline),
        "random_forest": scores(test_target, predicted, probability),
        "sessions": sessions,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output = json.dumps(report, indent=2)
    args.output.write_text(output + "\n", encoding="utf-8")
    print(output, flush=True)
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary, "a", encoding="utf-8") as stream:
            print("## HomeOccupancy session holdout\n\n```json\n" + output + "\n```", file=stream)


if __name__ == "__main__":
    main()
