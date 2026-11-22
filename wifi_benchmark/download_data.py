"""Download the exact published feature tables used in this benchmark."""
import hashlib
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
COMMIT = 'adc39ac0c05b493e3ecd4c75447b528d120d6d1e'
BASE = ('https://raw.githubusercontent.com/Tahmid-Mahmud-Fahim/'
        'esp32-based-presence-and-motion-detection-using-wifi-csi/'
        f'{COMMIT}/phase1/data/processed/')
FILES = {
    'metadata.json': '4db41114eab534c646af97b0c1542e1728e1ec80d04d6482f61c220ea83a8e04',
    'train_features.csv': 'aed314bbb8ff3785f4530efda42072202d0aef995f07b8d2b1a026d35b204f0b',
    'val_features.csv': '1a70f68a9216119c15cf0ab40335c2cc38c829085aac2367ce63bf7f85b3ebbe',
    'test_features.csv': 'd339be983ad21101e5448c573690f062b6d67657967591f772692fca102b9c42',
}

def main():
    folder = ROOT / 'data'
    folder.mkdir(exist_ok=True)
    for filename, expected in FILES.items():
        with urlopen(BASE + filename, timeout=60) as response:
            contents = response.read()
        actual = hashlib.sha256(contents).hexdigest()
        if actual != expected:
            raise ValueError(f'{filename}: SHA-256 mismatch: {actual}')
        (folder / filename).write_bytes(contents)
        print(f'{filename}: verified {actual}')

if __name__ == '__main__':
    main()
