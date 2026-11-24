# PPD Wi-Fi occupancy experiments

This repository evaluates whether a single Wi-Fi transmitter–receiver link can distinguish an empty room from an occupied room using public CSI recordings. The reference hardware for the student project is a pair of 7Semi ESP32-S3 DevKitC-1 N8R2 boards.

## Find project files

| Need | Location |
| --- | --- |
| Public, team-collected and simulated datasets | [Datasets](datasets/README.md) |
| Fitted models and inference instructions | [Models](models/) |
| Reproduce training | [HomeOccupancy benchmarks](benchmarks/), [BUET RX1](wifi_benchmark/), [experiment workflows](.github/workflows/) |
| Test results and limitations | [Experiment handoff](docs/experiment-handoff.md) |
| Run the dashboard locally | [Replay instructions](dashboard/README.md) |

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

Review the [audit of the original project](docs/original-experiment-review.md) and the [dataset catalog and two-room test plan](docs/occupancy-datasets.md) before interpreting performance. The BUET benchmark covers one room. The separate EHUNAM study evaluates transfer across four rooms. Physical ESP32-S3 validation remains open.

See the [experiment handoff](docs/experiment-handoff.md) for HomeOccupancy group-fold results and offline inference.

Open `dashboard/index.html` locally for the two-room replay, or see the [dashboard instructions](dashboard/README.md).
