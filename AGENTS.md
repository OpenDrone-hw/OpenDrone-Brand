# OpenDrone brand

The OpenDrone product identity: tokens, mark, wordmark, avatar, lockup, packaging and radio assets, generated from `src/` and `tokens/`.

Validate: `python3 tools/generate.py --check`

## Boundaries

- Edit `src/`, `tokens/` or `tools/`, never generated asset directories; regenerate with `python3 tools/generate.py`.
- No invented colours, typefaces, logo variants or visual effects; public asset paths stay stable.
- `standards/production.json` is canonical for physical production; compliance facts come from the compliance repository.
- `board-art/` is independent reference work, not generator output.
- `radio/` stays independent of any operator's calibration data.

## Pointers

- `BRAND.md`: read before visual work
- `radio/README.md`, `packaging/vistaprint.md`
