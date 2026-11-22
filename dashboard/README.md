# Room occupancy replay

Open `index.html` in a browser to run the two-room simulator. The dashboard runs locally with no installation, backend, or external dependencies. Use **Play**, **Reset**, or the time slider to move through the readings. Playback advances one recorded timestamp per second and displays times in UTC. Each room card shows its latest reading at the selected time, or **No reading** before its first reading.

To load a file, choose **Open replay** and select `example-replay.json` or another file with the same structure. The browser reads the file locally.

## Replay format

| Field | Required value |
| --- | --- |
| `source` | `"simulated"` for demonstration data or `"model"` for recorded model predictions |
| `rooms` | Two objects, each with a distinct nonempty string `id` and a nonempty string `name` |
| `readings` | A nonempty array of reading objects |
| `readings[].room_id` | One of the declared room IDs |
| `readings[].observed_at` | An ISO 8601 timestamp with a time zone, such as `2026-01-01T09:00:00Z` |
| `readings[].occupied` | Boolean. `true` means occupied and `false` means vacant |
| `readings[].occupancy_probability` | Optional model probability for the occupied class, from 0 to 1 |

The dashboard sorts readings by time, shows readings for both rooms together when their times match, and rejects duplicate times within a room. The two states represent binary room occupancy. To feed the window classifier into replay, use the binary prediction for `occupied` and join it with the actual room and timestamp associated with that window. The classifier's session-level benchmark summary needs this separate window-level metadata.
