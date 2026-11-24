# TU Wien Wi-Fi CSI presence datasets

Julian Strohmayer and Martin Kampel (TU Wien Computer Vision Lab), *WiFi CSI-Based Long-Range Through-Wall Human Activity Recognition with the ESP32*, version 1.0.0 (2023). [Zenodo dataset](https://doi.org/10.5281/zenodo.8021099) · [Conference paper](https://doi.org/10.1007/978-3-031-44137-0_4)

The [Zenodo metadata](https://zenodo.org/api/records/8021099) specifies [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The [record's Download and Use section](https://zenodo.org/records/8021099) also says that use is limited to non-commercial research and asks users to cite the conference paper. Download directly from Zenodo for non-commercial research. Confirm other uses or redistribution with the authors.

## Download and verify

From the repository root, run:

```sh
python3 datasets/public/tu-wien-presence/download.py /path/to/tu-wien-presence
```

The downloader retrieves only the two presence archives and verifies their pinned sizes and SHA-256 digests. Add `--verify-only` to verify existing local files. The upstream archives use PNG CSI amplitude spectrograms, each representing about four seconds of measurements at 100 Hz.

| Archive | Scenario | Labeled samples | Bytes | Zenodo MD5 |
| --- | --- | ---: | ---: | --- |
| `DP_LOS.zip` | Line of sight | 392 | 3,811,918 | `1dc93fae1800f93598eab74a4ebdd39e` |
| `DP_NLOS.zip` | Non-line of sight | 384 | 3,575,606 | `f9b318d0e9b1531caf6938cffe961293` |

## Binary occupancy labels

Use the archive's `trainLabels.csv`, `validationLabels.csv`, and `testLabels.csv` to select PNGs and preserve the published splits. Each headerless row contains the PNG's numeric stem and the upstream class. Map class `0` to empty and classes `1` through `5` to occupied. Each positive sample represents presence of one person under the corresponding capture condition.

| Archive | Train empty / occupied | Validation empty / occupied | Test empty / occupied |
| --- | ---: | ---: | ---: |
| `DP_LOS.zip` | 58 / 256 | 11 / 28 | 6 / 33 |
| `DP_NLOS.zip` | 57 / 251 | 7 / 31 | 6 / 32 |

Only use images referenced by the split files. Both archives contain an unlabeled `102.png`, and `DP_NLOS.zip` also contains an unlabeled `348.png`.
