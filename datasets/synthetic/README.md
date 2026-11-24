# Synthetic room occupancy fixture

[Example replay](example-replay.json) contains 16 synthetic readings across eight synchronized timestamps for two virtual rooms. The scripted scenario includes empty, still and moving room states, with counts from zero to three. Room dimensions and all labels are fictional. The data has no CSI measurements, occupant identifiers or individual coordinates.

Run the generator with Python 3.10 or later from the repository root.

```sh
python3 datasets/synthetic/generate.py datasets/synthetic/example-replay.json
```

Open [the dashboard](../../dashboard/index.html) locally, choose **Open replay**, and select the generated file. The dashboard uses the shared binary fields. `occupant_count`, `movement`, `length_m` and `width_m` are fixture fields for testing other room-level views. Use the sample for interface tests and visualization demos. Use measured recordings for benchmark or hardware claims.
