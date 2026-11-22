# Wi-Fi CSI room occupancy experiments

The project evaluates binary empty-versus-occupied detection from Wi-Fi channel state information (CSI). The [original experiment review](original-experiment-review.md) documents split reuse and the lack of measured performance for counts above one.

## Reproduce the public-data benchmarks

The [BUET RX1 benchmark](../wifi_benchmark/README.md) uses 13 precomputed features from one receiver. From the repository root, install NumPy and run the pinned downloader and training script.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install numpy
python wifi_benchmark/download_data.py
OPENBLAS_NUM_THREADS=1 python wifi_benchmark/benchmark.py
```

The [HomeOccupancy group-fold workflow](../.github/workflows/home-occupancy-folds.yml) downloads the pinned raw CSI recordings and runs three exploratory folds. To run locally, use the workflow's pinned dependencies and download commands. The command takes a directory containing all nine CSVs and an output path.

```sh
python benchmarks/home_occupancy_group_folds.py /path/to/home-occupancy home-occupancy-fold-metrics.json
```

The [model and inference guide](../benchmarks/HOME_OCCUPANCY_MODEL.md) covers the [fitted model artifact](https://github.com/srcsandy11/ttw-person-detection-using-wifi/actions/runs/45011341043/artifacts/14749019738), input format and offline prediction command.

Keep the public recordings local and fetch them from the pinned sources. The [dataset catalog](occupancy-datasets.md) links to sources and covers room and device compatibility.

## Results

| Dataset and validation | Window balanced accuracy | Test coverage |
| --- | ---: | --- |
| BUET RX1, published test split | 97.23% | 1,089 overlapping windows across 9 recordings |
| HomeOccupancy, group 1 | 99.75% | 3 held-out recordings |
| HomeOccupancy, group 2 | 98.50% | 3 held-out recordings |
| HomeOccupancy, group 3 | 94.53% | 3 held-out recordings |
| HomeOccupancy, pooled out of fold | 97.47% | 6,280 windows across 9 recordings |

The [HomeOccupancy workflow run](https://github.com/srcsandy11/ttw-person-detection-using-wifi/actions/runs/45011125246) produced 2,163 true negatives, 16 false positives, 177 false negatives, and 3,924 true positives across the three folds.

## Interpret the evaluation

For BUET, averaging probabilities per recording classified all nine test recordings correctly, two of which were empty. This was one room with one acquisition setup.

HomeOccupancy groups are based on the session number within each activity label. Every fold holds out three complete recordings, one per label. HomeOccupancy was previously evaluated on the third group, so the folds are exploratory. Session numbering does not establish a shared day or participant across labels. The recordings cover one room.

Use an independent set of labeled rooms and acquisition sessions to measure room transfer, sustained false alarms, missed occupancy, and detection latency. Record the hardware and link geometry alongside the ground truth.

[EHUNAM](https://doi.org/10.6084/m9.figshare.28541225) has 2,401 labeled MAT files across eight environments, including 624 files labeled empty and counts up to eight. Multiple receiver files can come from one acquisition. Group them by original capture before splitting, and keep complete rooms out of training when testing room transfer. These are metadata counts.

## Exploratory EHUNAM counting

The [count benchmark](https://github.com/srcsandy11/ttw-person-detection-using-wifi/blob/6fe7d3c/.github/workflows/ehunam-inspect.yml) used 115 receiver-1 captures from the Basement Room with reported counts of 0–4. A random forest used statistics of normalized CSI amplitude and differences between successive packets. Each direction trained on one date group from the summary spreadsheet and tested on the other, with no exact original-filename overlap. The spreadsheet date and original-filename date can differ, so recording-day independence requires further verification.

| Train and test capture counts | Balanced accuracy | Mean absolute count error |
| --- | ---: | ---: |
| 60 and 55 | 28.9% | 0.927 people |
| 55 and 60 | 37.0% | 0.867 people |

See the [completed count benchmark run](https://github.com/srcsandy11/ttw-person-detection-using-wifi/actions/runs/45011455483).

## Exploratory EHUNAM room transfer

The [held-room benchmark](https://github.com/srcsandy11/ttw-person-detection-using-wifi/blob/c828a84/.github/workflows/ehunam-room.yml) used one receiver and selected up to 12 captures per room and binary occupancy label. It held out each room in turn and trained on the other three.

| Held-out room | Test captures | Balanced accuracy |
| --- | ---: | ---: |
| Classroom | 23 | 69.3% |
| Office 1 | 23 | 86.4% |
| Laboratory | 22 | 50.0% |
| Storage Room | 22 | 80.0% |

Every Laboratory capture was predicted occupied. The small sample and differences in acquisition date, hardware and activity limit what can be inferred about room transfer. See the [completed room benchmark run](https://github.com/srcsandy11/ttw-person-detection-using-wifi/actions/runs/45011527402).

## Run the two-room replay

Open `dashboard/index.html` locally in a browser. The built-in playback uses simulated readings. To replay model output, join each window prediction with its actual room and observation timestamp, then import a JSON file following the [replay format](../dashboard/README.md).
