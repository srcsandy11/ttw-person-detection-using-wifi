# PPD Wi-Fi occupancy experiments

This repository evaluates whether a single Wi-Fi transmitter–receiver link can distinguish an empty room from an occupied room using public CSI recordings. The reference hardware for the student project is a pair of 7Semi ESP32-S3 DevKitC-1 N8R2 boards.

## Reproduce the RX1 experiment

From the repository root, run:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install numpy
python wifi_benchmark/download_data.py
OPENBLAS_NUM_THREADS=1 python wifi_benchmark/benchmark.py
```

The training script exports local model weights and a JSON report. Download permissions and data provenance are described in the [experiment notes](wifi_benchmark/README.md). The checked-in [evaluation results](wifi_benchmark/results.json) include held-out session scores and 50 shuffled-label controls.

Review the [audit of the original project](docs/original-experiment-review.md) and the [dataset catalog and two-room test plan](docs/occupancy-datasets.md) before interpreting performance. The current BUET benchmark covers one room. Room transfer, simultaneous multi-room sensing and ESP32 deployment have no measured performance here.
