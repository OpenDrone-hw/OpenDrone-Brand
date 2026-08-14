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
| `lockup/` | **OpenDrone by incutec** and **OpenDrone, an incutec project**, for when the company relationship needs to be visible. |
| `src/` | The two source logotypes everything is built from. |
| `tools/` | The generator. |

Every file exists as SVG. The wordmark and mark also ship as PDF, which opens
and edits natively in Illustrator, Affinity and Inkscape, and as PNG for
previews. **Send a vendor the SVG or the PDF, never the PNG.**

## Colour

| Token | Hex | Use |
|---|---|---|
| Gold | `#ffb700` | "Drone", the mark, the accent. Every ground, no exceptions |
| Ink | `#1a1a1e` | "Open" on light backgrounds |
| Off-white | `#e5e5e5` | "Open" on dark backgrounds |
| Surface dark | `#0d0d10` | Brand dark background |
| Surface light | `#f7f6f3` | Brand off-white background, not pure white |
| incutec teal | `#00B2A9` | The incutec accent. Only ever inside the incutec logotype |

**There is one gold and it does not change with the background.** It is hue
80.25 sitting exactly on the sRGB chroma ceiling, which is the most gold a
screen can be. Chroma falls above that lightness, so there is nothing brighter
to reach for and lightening it only turns it chalky.

Until 2026-08-14 there were two, `#c89d2e` on light and `#fdb600` on dark. They
were 0.112 apart in OKLab and the light one drifted 6 degrees toward green,
which is why it read brown on white. The hue drift and the missing chroma cost
nothing to fix. The lightness gap was doing real work and giving it up is a
deliberate trade: gold is 11.11:1 on the dark surface but **1.62:1 on the light
one**. Logos are exempt from contrast rules, so the mark and the wordmark are
fine. Gold text on a light ground is a brand accent, never body copy, and never
a focus ring or a control boundary.

`#ffb700` is outside CMYK gamut and cannot be reproduced in process colour.
Printed work needs a spot colour matched against a physical guide. Nobody has
picked one yet, so do not guess.

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
python3 tools/generate.py
```

Rebuilds **everything** from `src/`: the mark, the wordmark, the avatar and the
lockups. It is deterministic, so the same source produces byte-identical output
on any machine and a rerun that changes nothing gives an empty diff.

Writing the SVGs is pure Python with no third-party imports. Two dependencies
are optional and degrade cleanly: `rsvg-convert` for the PDF and PNG
renditions, and SF Pro (macOS) for the connector words in the endorsement
lockups. Without either, every other asset still builds.

Geometry is solved analytically in `tools/geometry.py`. Nothing is measured off
a raster, which is what used to make the output depend on the renderer version.

The geometry is not hand-placed. The two logotypes are matched on **x-height**,
measured off the ink of the letter `e` in each, so "incutec" reads as the same
size of type as the lowercase in "OpenDrone" instead of some arbitrary
percentage. Every frame is then cropped to measured ink bounds, so no file
carries dead padding that makes the logo render small.

Connector words ("by", "an", "project") are set in **SF Pro Display**, the same
family the OpenDrone wordmark was drawn from, and converted to outlines. No
font is embedded or redistributed here.

## Provenance

The OpenDrone wordmark is drawn from SF Pro Display Bold. The mark is that
wordmark's own O with its counter cut by a single vertical line at 0.4054 of the
O's width and closed flat, which turns the O's counter into a D's. It is one
path with two contours and no boolean operation, so it stays exact at any size. The incutec logotype
is Incutec's own artwork, included so the endorsement lockups can be rebuilt.
The generator is MIT. The artwork is not: see **Using it** above.

---

<sub>OpenDrone is a product line of Incutec BV, Leuven, Belgium.</sub>
