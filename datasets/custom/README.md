# Custom classroom CSI pilot

The [classroom CSI index](classroom-csi/index.csv) lists 17 approximately 30-second trials from two classrooms and three recording sessions. Each trial has a CSI CSV, recorder metadata and the original wire frames. Two ESP32-S3 boards recorded from outside each classroom. The counts below come from the trial index.

| Room | Session | Empty trials | Occupied trials | Conditions |
| --- | --- | ---: | ---: | --- |
| Room 1 | 01 | 1 | 2 | Empty, seated and walking |
| Room 2 | 01 | 6 | 0 | Quiet corridor or corridor walking at estimated 2, 3 and 4 m spans |
| Room 2 | 02 | 0 | 8 | Seated or walking inside, with and without corridor walking |

Derive binary occupancy from `room_activity` in the index. Keep `corridor_activity` separate so a corridor walk during an empty-room trial remains an empty-room observation. The recorder's generic `other` label covers several different conditions. Keep raw files intact and write derived files separately.

Use an entire recording as the smallest split unit. Room 2's occupancy label is tied to session, so a trial split inside these two sessions cannot test independent generalization. Further data requires both occupancy classes within multiple sessions and rooms, with independently recorded ground truth and measured link geometry. This pilot cannot distinguish a concrete-only path from propagation via doors or windows.

The raw files include board MAC addresses and recording metadata. Use the room and session codes in derived examples and omit hardware identifiers and unnecessary absolute timestamps from any new public export.

The supplied `csi_project.zip` holds code, demo files and prior reports. The supplied dataset roadmap describes additional data collection and public datasets. These two attachments contain no original CSI recordings. The classroom pilot recordings linked above come from the existing repository.
