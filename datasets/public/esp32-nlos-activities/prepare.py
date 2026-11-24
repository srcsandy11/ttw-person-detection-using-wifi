"""Extract one measured trial per subject and activity in the third environment."""
import argparse
import csv
import hashlib
import io
import re
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("archive", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
with args.archive.open("rb") as source:
    if hashlib.file_digest(source, "sha256").hexdigest() != "dbd2aace6430691d8e2c811d47cc43ce8ce60c076081995b31e32361162c87f4":
        parser.error("Archive differs from Mendeley version 1")
with zipfile.ZipFile(args.archive) as archive, args.output.open("w", newline="") as output:
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["trial", "activity", "packet_index", "rssi_dbm", "first_word_invalid", "csi_data"])
    for name in sorted(archive.namelist()):
        if not re.search(r"/Environment 3/[^/]+/E3_S\d+_A\d+_T01\.csv$", name, re.I):
            continue
        trial = Path(name)
        with archive.open(name) as file:
            rows = csv.DictReader(io.TextIOWrapper(file, encoding="utf-8-sig"))
            for index, row in enumerate(rows):
                if row["type"] == "CSI_DATA":
                    writer.writerow([trial.stem, trial.parent.name, index, row["rssi"], row["first_word_invalid"], row["data"]])
