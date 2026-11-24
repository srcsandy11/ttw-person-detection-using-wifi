# ESP32 non-line-of-sight activity comparison

Zhe Yu Lim and Lee-Yeng Ong (2024), [Mendeley Data v1](https://doi.org/10.17632/x4x5xttvwt.1), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The authors used a D-Link AX3000 Wi-Fi router as transmitter and an ESP32 as receiver. Environment 3 is their non-line-of-sight condition. This is a secondary dataset for checking processing of occupied activity trials. Exterior placement of both radios is unverified. It has no empty-room controls or multi-person count labels in this subset.

The included packets.csv contains 14,879 measured CSI packet rows across 80 trials (one trial per subject and activity, eight subjects and ten activities). We selected trial T01 in Environment 3, retained RSSI, CSI and the invalid-first-word flag, and removed hardware addresses and other packet metadata. Packet indexes indicate source row order within each trial. Sitting down is an activity transition, not a sustained seated condition. Split whole trials or subjects before windowing.

To regenerate, download the original ZIP from the versioned record and run `python3.11 prepare.py archive.zip packets.csv` in this directory. The script checks the publisher's SHA-256 before extraction.
