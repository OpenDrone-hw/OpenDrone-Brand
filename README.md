<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OpenDrone-hw/OpenDrone-Brand/main/lockup/opendrone-lockup-ondark-2000.png">
    <img src="https://raw.githubusercontent.com/OpenDrone-hw/OpenDrone-Brand/main/lockup/opendrone-lockup-onlight-2000.png" alt="OpenDrone, an incutec project" width="560">
  </picture>
</p>

# OpenDrone brand assets

Every OpenDrone logo, in vector, with the rules for using them. If you are
writing about OpenDrone, reviewing a board, or listing us as a supplier, take
what you need from here instead of screenshotting the website.

## What is in here

| Folder | Contents |
|---|---|
| `wordmark/` | The **OpenDrone** logotype. Primary asset. On-light, on-dark, the same two with the brand background baked in, and one-colour black, white and gold. |
| `mark/` | The **OD monogram**, for favicons, app icons and tight spaces. |
| `avatar/` | The GitHub and social avatar: the mark on a gold squircle. |
| `lockup/` | **OpenDrone, an incutec project**, for when the company relationship needs to be visible. |
| `sheet/` | One-page brand sheet, for vendors and press. |
| `src/` | The two source logotypes, and the frozen type outlines. |
| `tools/` | The generator. |

Everything exists as SVG. The wordmark, mark and sheet also ship as PDF, which
opens and edits natively in Illustrator, Affinity and Inkscape, and as PNG for
previews. **Send a vendor the SVG or the PDF, never the PNG.** All text is
outlined, so nothing falls back to a substitute typeface on a machine without
SF Pro.

## Colour

**[`tokens.json`](tokens.json) is the source of truth**, for this repo and every
other one: screen values, the physical standard, tolerances, per-substrate
specs, and the retired hexes so a grep for an old value lands somewhere useful.
Read it rather than copying values out of this page.

One gold, `#ffb700`, on every ground. It sits on the sRGB chroma ceiling for its
hue, so there is nothing more gold a screen can show. It is 11.11:1 on the dark
surface and **1.62:1 on the light one**: logos are exempt from contrast rules, so
the mark and the wordmark are fine, but gold on a light ground is a brand accent
and never body copy, a focus ring or a control boundary.

Off screen, the master is **Pantone 1235 C** (dE2000 0.82 from the screen gold,
below the threshold where a difference is visible). `#ffb700` is outside CMYK
gamut, so a hex is not a specification a supplier can work from. One rule keeps
aluminium, print and fabric agreeing with each other:

> Every substrate is matched to the **1235 C chip**. Never to the hex, and never
> to another substrate.

## Using it

The logotypes are trademarks. Publishing them here is so that people who talk
about OpenDrone can do it accurately, not a grant to use them as your own.

**Fine, no permission needed:** referring to OpenDrone in an article, video,
review, forum post, comparison table or supplier list. Saying your project is
compatible with, based on, or a fork of an OpenDrone board.

**Ask first:** merchandise, a product name or logo of your own that
incorporates ours, or anything where a reader could reasonably think we made or
endorsed it. The hardware licence lets you fork and sell the boards; it does not
come with the name.

**Never:** recolour, stretch, rotate, outline, add effects, or rebuild the
logotype in a different typeface. Do not place the wordmark on a background that
leaves less than 4.5:1 against the "Open" half.

**Clear space:** at least the height of the "O" on all sides. Minimum wordmark
width 120 px on screen, 25 mm in print. Below that use the mark alone.

Forked a board and want to make clear it is yours, not ours? Change the
silkscreen. That is what the CERN-OHL-S copyleft asks of you anyway.

## Regenerating

```
python3 tools/generate.py           # rebuild everything from src/
python3 tools/generate.py --check   # prove the build is reproducible
```

A rerun that changes nothing gives an empty diff. `--check` is the same build
into a scratch tree, compared file by file: it exits non-zero if any committed
SVG differs from a fresh one, which makes reproducibility something the repo
proves rather than claims.

The SVGs are the assets, and they are byte-identical on any machine. Geometry is
solved analytically in `tools/geometry.py`, never measured off a raster; type is
frozen in `src/sf-outlines.json`; no timestamp or random value enters a file.
Writing them is pure Python with no third-party imports.

PDF and PNG are renditions, made by `rsvg-convert` where it is installed. Their
bytes carry the local cairo and libpng, so `--check` reports a difference there
as renderer drift, not a build failure. Without `rsvg-convert` the SVGs still
build.

The connector words ("by", "an", "project") and the brand sheet are set in
**SF Pro Display**, the family the OpenDrone wordmark was drawn from, and
converted to outlines. Those outlines live in `src/sf-outlines.json`, so a build
needs neither the font nor macOS. Re-cutting them is a deliberate step:

```
python3 tools/generate.py --refresh-outlines   # macOS + fonttools
```

It reads the installed SF Pro, rewrites the JSON with the font version recorded,
and rebuilds. Review that diff like any other artwork change. No font is
embedded or redistributed here.

## Provenance

The OpenDrone wordmark is drawn from SF Pro Display Bold. The mark is that
wordmark's own O with its counter cut by a single vertical line at 0.4054 of the
O's width and closed flat, which turns the O's counter into a D's. It is one
path with two contours and no boolean operation, so it stays exact at any size.
The incutec logotype is Incutec's own artwork, included so the endorsement
lockups can be rebuilt. Geometry is not hand-placed: the two logotypes are
matched on **x-height**, measured off the ink of the letter `e` in each, and
every frame is cropped to measured ink bounds, so no file carries dead padding.

The generator is MIT. The artwork is not: see **Using it** above.

---

<sub>OpenDrone is a product line of Incutec BV, Leuven, Belgium.</sub>
