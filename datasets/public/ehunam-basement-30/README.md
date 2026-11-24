# EHUNAM basement CSI subset (30 captures)

This subset contains 30 individual complex CSI matrices from EHUNAM, with 3 recordings for each count 0–4 on each of two dates in the supplied summary metadata. One receiver (Rx 1) and one basement room are included. Each .npz file contains one complex64 matrix named csi (packets × subcarriers); labels.csv supplies counts, binary occupancy, source names, dimensions, and SHA-256 checksums. Source matrices were converted from complex128 to complex64; each output was reloaded and numerically checked.

Source: de Armas et al., *EHUNAM, a WiFi CSI-based dataset for human and machine sensing*, Scientific Data 12 (2025), https://doi.org/10.1038/s41597-025-06238-4. Dataset: https://doi.org/10.6084/m9.figshare.28541225. Licensed under Creative Commons Attribution 4.0 International: https://creativecommons.org/licenses/by/4.0/. This is a selected and precision-converted derivative; no claims are made that it represents the full dataset.

The metadata dates below are copied from Summary.xlsx and do not consistently match dates embedded in source filenames. Treat date-based separation as provisional. Samples from one room, a small number of controlled captures and a single receiver do not establish performance in new rooms or hardware. Preserve complete source recordings as grouping units; never split packets from one recording across train and test. There are only 3 captures per count/date; this is a development subset, not a representative benchmark.

To load: `numpy.load("csi/sample_000.npz", allow_pickle=False)["csi"]` (relative to this directory). Verify checksums using labels.csv.
