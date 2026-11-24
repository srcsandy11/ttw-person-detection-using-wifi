# ESP32 room-presence example

These recordings come from one indoor room in Suraj Dubal, Sushma Vispute, Ayush Deshmane, and Ganesh Ghumare's *Wi-Fi CSI Dataset for Person Presence Detection Using ESP32*, version 1, Mendeley Data, 2026. The dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Dataset and DOI](https://doi.org/10.17632/zycty7ksky.1).

- `packets.csv` contains 28 original packet records from the first labeled interval per session and class, with four sequential packets per included interval. The export omits the ESP32 local timestamp column and all unlabeled rows.
- `windows.csv` contains 437 room-level windows derived from 14,485 labeled packets. Windows span two seconds relative to the first packet of their labeled interval, with at least eight packets each. Features are the mean and population standard deviation of packet RSSI and packet CSI component RMS. CSI component RMS treats the deposited vector as numeric components.
- `occupied` is a binary label derived from the experimental annotations. `empty` maps to 0, and `present` and `moving` map to 1. The window counts are 161 empty, 138 present, and 138 moving.

| Source session | Room | Window count | Classes |
| --- | --- | ---: | --- |
| `session_20261024_235657` | `room1` | 215 | empty, present, moving |
| `session_20261025_000518` | `room1` | 215 | empty, present, moving |
| `session_20261025_001358` | `room1` | 7 | empty |

Use `session_id` to keep complete sessions together in a split. The third session supports checking empty-room errors. This dataset covers a single room and binary occupancy labels.

## Reproduce

Use Python 3.11+ and the cleaned source CSV. The script verifies the publisher's SHA-256 before extracting the two files.

```sh
curl -fL 'https://data.mendeley.com/public-files/datasets/zycty7ksky/files/102aa053-6c0f-429a-91df-3c820b3a487d/file_downloaded' -o room1_merged_clean.csv
python3 prepare.py room1_merged_clean.csv .
```

The original file has SHA-256 `304d0b31f2c027e7889ff130958484980ab9cb7002de4d949b33c03359ea6994`. The deposited `pc_time` has no timezone offset. The window index uses differences within an interval and does not depend on the absolute timezone.

[WiCount](https://huggingface.co/datasets/RS2002/WiCount) is a separate one-room count dataset with class labels 0–3. Its public data card does not specify a dataset redistribution license.
