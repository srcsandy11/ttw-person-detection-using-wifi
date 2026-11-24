# Classroom Wi-Fi CSI pilot recordings

Two ESP32-S3 boards recorded Wi-Fi channel state information from outside each classroom. Each trial lasts approximately 30 seconds. Use [index.csv](index.csv) to find a recording by room, session, indoor activity, and corridor activity. Paths in the index are relative to this directory.

| Session | Trials | Conditions |
|---|---:|---|
| [Room 1, session 01](room-1/session-01/) | 3 | The 5 x 7 m classroom with open rear windows. Empty, one person seated, and one walking. |
| [Room 2, session 01](room-2/session-01/) | 6 | Empty classroom with closed glass windows. Quiet corridor and corridor walking at three estimated spacings. |
| [Room 2, session 02](room-2/session-02/) | 8 | One person seated or walking inside. Some seated trials also include a second person walking in the corridor. |

## Reading a trial

Open the trial folder from the index. Use csi.csv for per-frame measurements, including signal strength and the hexadecimal CSI data in iq_hex. Each complex sample is a pair of signed 8-bit values in imaginary, real order. run.json contains the original download metadata. wire.bin contains the binary frames.

For activity labels, use the index. The recorder uses the generic label other for several conditions, including sitting inside and walking outside. The two activity columns preserve that distinction.

## Interpretation

The early spacings are estimates. In Room 2, TX stayed at a doorway and the 4 m placement put RX at or near a second doorway. The planned tape-measured sessions are a separate experiment. Room 2's attempted ninth trial (4 m, walking inside) produced no confirmed recording.

Room 2 occupancy is confounded with session: all empty-room examples come from session 01 and all occupied-room examples from session 02. Keep whole recordings together during evaluation. These pilot data alone cannot establish occupancy-detection accuracy or isolate a signal path through concrete.

The [trial summary](derived/trial_summary.csv) has one row per measured trial with mean and standard deviation of packet RSSI. Regenerate it with `python3 datasets/custom/classroom-csi/derived/build.py` from the repository root. These are the same 17 recordings summarized for inspection. In Room 2 the indoor label changes with the session, so these statistics alone cannot establish presence detection.
