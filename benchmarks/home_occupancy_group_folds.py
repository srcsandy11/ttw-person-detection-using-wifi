"""Three recording-group holdouts on HomeOccupancy; exploratory, not an untouched test."""
import argparse
import json
import joblib
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from home_occupancy import CLASSES, DATASET, REVISION, SEED, WINDOW_PACKETS, read_session, scores

def main():
    p = argparse.ArgumentParser()
    p.add_argument("data_dir", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--model-output", type=Path, required=True)
    args = p.parse_args()
    sessions = {}
    for cls in CLASSES:
        for number in (1, 2, 3):
            name = f"{cls}_{number}.csv"
            x, counts = read_session(args.data_dir / name)
            sessions[name] = (number, int(cls != "empty"), x, counts)
            print(name, counts, flush=True)

    folds, ys, preds, probs = [], [], [], []
    for held_out in (1, 2, 3):
        train = [v for v in sessions.values() if v[0] != held_out]
        test = [(n, v) for n, v in sessions.items() if v[0] == held_out]
        X = np.concatenate([v[2] for v in train])
        y = np.concatenate([np.full(len(v[2]), v[1]) for v in train])
        model = RandomForestClassifier(n_estimators=300, max_depth=12,
            min_samples_leaf=8, class_weight="balanced", random_state=SEED, n_jobs=2)
        model.fit(X, y)
        if held_out == 3:
            args.model_output.parent.mkdir(parents=True, exist_ok=True)
            joblib.dump(model, args.model_output)
        per_session = {}
        fold_y, fold_p, fold_probs = [], [], []
        for name, (_, label, x, counts) in test:
            probability = model.predict_proba(x)[:, 1]
            predicted = (probability >= 0.5).astype(int)
            truth = np.full(len(x), label)
            per_session[name] = {"label": label, "windows": len(x),
                "correct": int((predicted == truth).sum()),
                "predicted_occupied_fraction": float(predicted.mean())}
            fold_y.append(truth); fold_p.append(predicted); fold_probs.append(probability)
        fy, fp, fprob = map(np.concatenate, (fold_y, fold_p, fold_probs))
        folds.append({"held_out_session_number": held_out,
            "training_windows": len(y), "test_windows": len(fy),
            "metrics": scores(fy, fp, fprob), "per_session": per_session})
        ys.append(fy); preds.append(fp); probs.append(fprob)

    report = {"dataset": DATASET, "revision": REVISION, "window_packets": WINDOW_PACKETS,
        "model": "random forest, 300 trees, max_depth 12, min_samples_leaf 8, balanced classes",
        "seed": SEED, "threshold": 0.5,
        "evaluation": "three exploratory group folds; each holds out one full recording per class",
        "caveat": "Only nine recordings in one room; windows within recordings are correlated. "
                  "Fold 3 was previously used as a test set; this is not a fresh independent test. "
                  "Session numbers across labels may not be aligned by day or person. "
                  "Results are binary presence, not person counting, through-wall localization, or live validation.",
        "folds": folds, "pooled_out_of_fold": scores(np.concatenate(ys), np.concatenate(preds), np.concatenate(probs))}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2), flush=True)

if __name__ == "__main__":
    main()
