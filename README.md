<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OpenDrone-hw/OpenDrone-Brand/main/lockup/opendrone-lockup-ondark.png">
    <img src="https://raw.githubusercontent.com/OpenDrone-hw/OpenDrone-Brand/main/lockup/opendrone-lockup-onlight.png" alt="OpenDrone, an incutec project" width="560">
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
| `mark/` | The standalone **O**, for favicons, app icons and tight spaces. |
| `avatar/` | The GitHub and social avatar: the O knocked out of a Brand Gold square. |
| `lockup/` | **OpenDrone by incutec** and **OpenDrone, an incutec project**, for when the company relationship needs to be visible. |
| `src/` | The two source logotypes everything is built from. |
| `tools/` | The generator. |

Every file exists as SVG. The wordmark and mark also ship as PDF, which opens
and edits natively in Illustrator, Affinity and Inkscape, and as PNG for
previews. **Send a vendor the SVG or the PDF, never the PNG.**

## Colour

| Token | Hex | Use |
|---|---|---|
| Brand Gold | `#c89d2e` | "Drone", the mark, and the accent **on light backgrounds** |
| Gold Bright | `#fdb600` | Gold **on dark backgrounds**. Also the physical gold of the motors |
| Ink | `#1a1a1e` | "Open" on light backgrounds |
| Off-white | `#e5e5e5` | "Open" on dark backgrounds |
| Surface dark | `#0d0d10` | Brand dark background |
| Surface light | `#f7f6f3` | Brand off-white background, not pure white |
| incutec teal | `#00B2A9` | The incutec accent. Only ever inside the incutec logotype |

Gold is background-aware: it deepens on light surfaces and brightens on dark.
Using `#c89d2e` on a dark background is the single most common way to get this
wrong.

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

Rebuilds the avatar and both lockups from `src/`. Needs `fonttools`, `brotli`,
`Pillow`, `rsvg-convert`, and SF Pro, which ships with macOS.

The geometry is not hand-placed. The two logotypes are matched on **x-height**,
measured off the ink of the letter `e` in each, so "incutec" reads as the same
size of type as the lowercase in "OpenDrone" instead of some arbitrary
percentage. Every frame is then cropped to measured ink bounds, so no file
carries dead padding that makes the logo render small.

Connector words ("by", "an", "project") are set in **SF Pro Display**, the same
family the OpenDrone wordmark was drawn from, and converted to outlines. No
font is embedded or redistributed here.

## Provenance

The OpenDrone wordmark is drawn from SF Pro Display Bold. The incutec logotype
is Incutec's own artwork, included so the endorsement lockups can be rebuilt.
The generator is MIT. The artwork is not: see **Using it** above.

---

<sub>OpenDrone is a product line of Incutec BV, Leuven, Belgium.</sub>
