"""Verify or download the versioned TU Wien presence archives."""

import argparse
import hashlib
import shutil
import tempfile
import urllib.request
from pathlib import Path


SOURCE = "https://zenodo.org/api/records/8021099/files"
ARCHIVES = {
    "DP_LOS.zip": (
        3811918,
        "8b59706dca1851f72b762228e763e111148e9a511ce1538b494e07b4bb97b8b1",
    ),
    "DP_NLOS.zip": (
        3575606,
        "91f10308e88f10c20aeceb59fcc9ea0812d2cf29583e5169e66bdc471e9a9516",
    ),
}


def verify(path, expected_bytes, expected_sha256):
    """Check the archive without extracting it."""
    sha256 = hashlib.sha256()
    with path.open("rb") as archive:
        while chunk := archive.read(1024 * 1024):
            sha256.update(chunk)
    if path.stat().st_size != expected_bytes or sha256.hexdigest() != expected_sha256:
        raise ValueError(f"Archive failed size or SHA-256 verification: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Location for the two archives")
    parser.add_argument("--verify-only", action="store_true", help="Skip downloads")
    args = parser.parse_args()

    if not args.verify_only:
        args.directory.mkdir(parents=True, exist_ok=True)

    try:
        for name, (size, sha256) in ARCHIVES.items():
            destination = args.directory / name
            if args.verify_only or destination.exists():
                verify(destination, size, sha256)
            else:
                with tempfile.TemporaryDirectory(dir=args.directory) as temporary:
                    candidate = Path(temporary) / name
                    with urllib.request.urlopen(
                        f"{SOURCE}/{name}/content", timeout=60
                    ) as response, candidate.open("wb") as archive:
                        shutil.copyfileobj(response, archive)
                    verify(candidate, size, sha256)
                    candidate.replace(destination)
            print(f"Verified {destination}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
