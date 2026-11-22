# Wi-Fi CSI datasets for aggregate room occupancy

Use empty versus occupied labels for same-room experiments. A packet count measures recording volume. Recordings, sessions, participants and rooms determine independent evaluation coverage.

| Dataset | Recorded coverage | Use and limits |
| --- | --- | --- |
| [BUET ESP32-S3](https://github.com/Tahmid-Mahmud-Fahim/esp32-based-presence-and-motion-detection-using-wifi-csi) | 39 sessions, 78 receiver files, 227,505 packets | Map static and moving to occupied. Keep simultaneous receivers in the same partition and evaluate one receiver at a time for the single-link hardware configuration. |
| [HomeOccupancy](https://huggingface.co/datasets/gadgadgad/HomeOccupancy) | Approximately 1.7 million packets, nine recordings, two ESP32-C6 devices | Map sleep and work to occupied. Use the published session split. Treat board and environment transfer as separate experiments. |
| [Mendeley ESP32](https://data.mendeley.com/datasets/zycty7ksky/1) | 17,008 records, three sessions | Exclude unlabeled rows. Inspect class coverage per session before computing balanced accuracy. |
| [Multi-room ESP32-S3 thesis](https://github.com/venkatasasikiranreddykotapati/wifi-csi-occupancy) | Three room types reported, four example recordings released | Request the complete dataset from the author for an independent room-transfer evaluation. |

Keep acquisition links here. Review each upstream license before redistributing files. Record dataset version, source recording and checksum alongside each experiment.

## Physical evaluation for the two-board kit

Collect consenting same-room observations with the transmitter and receiver together in room A, then move the pair to room B. Record multiple sessions and days with each class represented in each room. Include occupied sessions where participants sit still and empty sessions with fans running. Record ground truth independently. Lock the feature extractor and operating threshold before opening the test labels. Report per-room false alarms, missed occupied periods and time to detect changes in addition to balanced accuracy. Two sequential room tests evaluate transfer; simultaneous coverage requires a separate experiment.

Train on complete sessions, fit preprocessing only on training sessions, and keep overlapping windows together. Compare with a majority baseline and a shuffled-label control. For incompatible boards or data formats, evaluate separately before attempting pooled training. Keep new labeled sessions for supervised retraining and a permanent untouched evaluation set.
