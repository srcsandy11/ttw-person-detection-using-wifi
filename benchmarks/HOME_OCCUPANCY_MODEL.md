# HomeOccupancy grouped-fold model

The workflow `.github/workflows/home-occupancy-folds.yml` trains three random forests on the public HomeOccupancy recordings and uploads the metrics and fold-3 model as the `home-occupancy-group-folds` Actions artifact. Fold 3 trains on recordings numbered 1 and 2 for each class, and holds out recordings numbered 3. It is a research model for binary occupancy, not a person counter. The test set was previously used; it is not an untouched independent evaluation. This is one room and setup, so transfer, through-wall, and live performance are unknown.

For offline inference, install the exact dependency versions listed in the workflow and download the matching artifact from a successful workflow run. Use only a trusted model file: joblib loading can execute code.

```sh
python benchmarks/predict_home_occupancy.py /path/to/recording.csv /path/to/home-occupancy-fold3.joblib predictions.json
```

Input must follow the pinned dataset's ESP32 CSI CSV format: rows beginning `CSI_DATA,` with a final array of 128 signed 8-bit integers, interpreted as 64 I/Q pairs. The parser skips invalid rows, requires 10,000 valid packets, and groups successive valid packets into non-overlapping windows of 256; incomplete tails are dropped. It extracts 156 features from normalized magnitude on subcarriers 6–31 and 33–58: standard deviation, mean absolute packet difference, and 90th percentile absolute packet difference (52 each). The output is an ordered list with zero-based window index, model probability for class 1 (occupied), and thresholded result at 0.5. Labels are empty=0 and sleep/work=1. No actual timestamps, room IDs, head counts, confidence guarantees or raw live receiver interface are supplied. Invalid packets are skipped, so a window index is not a fixed time interval. Predictions for training or previously evaluated recordings are demonstrations, not new validation.

Reproduce on the pinned source files using the workflow commands. Compare the same exported fold-3 model on `work_3.csv`: 755 complete windows and 597 occupied predictions. This validates output consistency, not accuracy on a new dataset.
