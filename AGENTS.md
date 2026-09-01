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
- Run `python3 tools/generate.py --check` after every change.
