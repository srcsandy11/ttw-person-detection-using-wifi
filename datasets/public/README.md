# Public datasets

| Dataset | Available in this checkout | What to use it for |
| --- | --- | --- |
| [EHUNAM](ehunam-basement-30/) | 30 measured CSI matrices, labels, and checksums | Load a small real counting dataset with labels from 0 to 4 in one room. |
| [ESP32 presence](esp32-presence/) | 28 example packet rows, 437 derived windows, and the extraction script | Inspect the packet format and compare empty, present and moving recordings. |
| [TU Wien presence](tu-wien-presence/) | Verified opt-in downloader and attribution | Obtain the two presence spectrogram archives directly from the publisher. |

The [registry](../dataset_registry.csv) lists additional upstream research datasets, including WiCount, WiMANS, Wallhack and 3DO. Their full archives are hosted upstream. Check each source's usage terms. The HomeOccupancy and BUET training procedures are in the [experiment handoff](../../docs/experiment-handoff.md).

## Which data matches two exterior boards?

The team uses a 7Semi ESP32-S3 DevKitC-1 N8R2 as transmitter and another as receiver, both outside the room. Its [classroom recordings](../custom/classroom-csi/) explicitly document both boards outside the measured classroom. The [trial-level signal summary](../custom/classroom-csi/derived/trial_summary.csv) retains the corridor label so hallway walking can be distinguished from indoor occupancy.

[Wallhack1.8k acquisition and verification](wallhack/) gives access to NLoS samples with empty and moving-occupied labels. TU Wien presence also has an NLoS split. Neither NLoS label, on its own, establishes the same corridor geometry. The [3DO study](https://zenodo.org/records/10925351) is a distinct single-person through-wall experiment. For team validation keep confirmed exterior classroom trials separate from all public comparisons.

Strohmayer's [collection diagrams, Figures 5.1 and 5.3](https://repositum.tuwien.at/bitstream/20.500.12708/222429/1/Strohmayer%20Julian%20-%202025%20-%20WiFi-Based%20Person-Centric%20Sensing.pdf) clarify the distinction. The five-room through-wall experiment used exterior endpoints beyond the end rooms. In 3DO the subject occupied the central office, with one radio in each neighboring room on opposite sides. Both are useful exterior-radio comparisons, but a link spanning the target room and a link along one corridor wall are different experiments.

The [ESP32 NLoS activity subset](esp32-nlos-activities/) ships with the checkout: 80 occupied activity trials. It uses a Wi-Fi router transmitter and an ESP32 receiver, so use it as a secondary preprocessing baseline. For a closer public hardware comparison, TU Wien's published System A uses ESP32-S3-DevKitC-1 hardware with an external antenna; see Figures 4.2 and 5.1 in the collection reference above.
