# Model index

| Experiment | Files and usage |
| --- | --- |
| HomeOccupancy, fold 3 | [Trained binary occupancy model and evaluation JSON](home-occupancy/). Use the [pinned environment and input contract](../benchmarks/HOME_OCCUPANCY_MODEL.md). |
| BUET RX1 | The [training script](../wifi_benchmark/benchmark.py) exports weights when run with the upstream feature tables. |
| EHUNAM | [Counting and cross-room benchmark results](../docs/experiment-handoff.md). The exploratory runs recorded metrics only. |

For offline HomeOccupancy inference, run the following from the repository root after installing the dependencies in the model guide.

```sh
python benchmarks/predict_home_occupancy.py work_3.csv models/home-occupancy/home-occupancy-fold3.joblib predictions.json
```

The saved forest uses the HomeOccupancy input format. Performance on the team's classroom recordings requires separate validation. The [original model export](https://github.com/srcsandy11/ttw-person-detection-using-wifi/actions/runs/45011341043) includes its held-out inference check.
