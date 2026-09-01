<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OpenDrone-hw/OpenDrone-Brand/main/lockup/opendrone-lockup-ondark-2000.png">
    <img src="https://raw.githubusercontent.com/OpenDrone-hw/OpenDrone-Brand/main/lockup/opendrone-lockup-onlight-2000.png" alt="OpenDrone, an incutec project" width="560">
  </picture>
</p>

# OpenDrone brand

The OpenDrone brand package: guidance, DTCG design tokens, production colour
standards and generated identity assets.

## Structure

- `BRAND.md` — identity, usage and trademark rules.
- `tokens/` — canonical [DTCG 2025.10](https://www.designtokens.org/tr/2025.10/format/) screen tokens and theme resolver.
- `standards/` — physical colour standards and retired values.
- `src/` — canonical artwork and frozen type outlines.
- `mark/`, `wordmark/`, `avatar/`, `lockup/`, `sheet/` — generated exports.
- `tools/` — deterministic, dependency-free generator.

## Workflow

```sh
python3 tools/generate.py          # regenerate assets
python3 tools/generate.py --check  # verify committed SVGs exactly
```

Do not edit generated artwork. PDF and PNG bytes may vary with the local
renderer; SVG output is deterministic.

## Licence

Generator code is MIT. OpenDrone and Incutec artwork is trademarked; see
`BRAND.md` and `LICENSE`.
