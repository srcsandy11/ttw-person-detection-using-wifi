# Wallhack1.8k v1.0.1

For aggregate occupancy comparisons, the publisher reports 291 no-presence and 596 moving-occupied NLoS spectrograms. There is no occupied-but-seated class. Both exterior endpoints on the same corridor side are unverified for these samples. Keep them separate from the classroom trials.

Download the authors' archive locally for non-commercial research. The Zenodo record lists CC BY 4.0 and also specifies non-commercial research use in its description. The raw archive stays upstream.

```sh
curl -fL --retry 2 https://zenodo.org/records/13950918/files/wallhack1.8k.zip -o wallhack1.8k.zip
python3 -c "import hashlib,pathlib; p=pathlib.Path('wallhack1.8k.zip'); assert p.stat().st_size == 135133863 and hashlib.md5(p.read_bytes()).hexdigest() == '57a0b9baa3532e1172b25d756536071a'"
```

Julian Strohmayer and Martin Kampel, [dataset and publication references](https://zenodo.org/records/13950918).
