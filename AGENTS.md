# Agent instructions

Read `BRAND.md` before visual work.

- `tokens/` is canonical for screen values.
- `standards/production.json` is canonical for physical production.
- Edit `src/` or `tools/`, never generated asset directories directly.
- Do not invent colours, typefaces, logo variants or visual effects.
- Preserve the existing public asset paths.
- `board-art/` is independent reference work, not generator output.
- `packaging/` owns OpenDrone-specific packaging direction, but compliance
  facts and readiness come from the sibling compliance repository.
- `radio/` owns OpenDrone-branded EdgeTX media and fleet setup; keep it
  independent of any operator's calibration data.
- Validation: `python3 tools/generate.py --check` after every change. CI runs
  the same command on plain Ubuntu (`.github/workflows/ci.yml`); PDF and PNG
  bytes are reported, not failed.

## By task

- Change the artwork or a colour: edit `src/` or `tokens/`, run `python3 tools/generate.py`, commit the regenerated `mark/`, `wordmark/`, `avatar/`, `lockup/` and `sheet/` output with the source change.
- Verify before a pull request: `python3 tools/generate.py --check` exits 0 when the committed SVGs match the generator.
- Set up a test-fleet radio: mount the EdgeTX SD card, then `python3 radio/apply_radio_setup.py "/Volumes/RADIO" radio/boot.wav`; it backs up `MODELS/model00.yml` and `RADIO/radio.yml` first (see `radio/README.md`).
- Prepare packaging artwork: follow `packaging/vistaprint.md`; board art comes from the hardware tooling's `packaging_art.py` with `--color` and `--body` set, as that file specifies.
