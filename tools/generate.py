#!/usr/bin/env python3
"""Regenerate the OpenDrone identity assets from src/.

Run from anywhere:  python3 tools/generate.py
Needs: fonttools, brotli, Pillow, rsvg-convert, and SF Pro (macOS system font).


Avatar  : A3, the "O" mark knocked out of a Brand Gold squircle.
Lockups : the two logotypes, never redrawn, joined only by connector words.
          "OpenDrone by incutec"  and  "OpenDrone, an incutec project". Connector
          words are SF Pro Display, the family the wordmark itself was traced from.

Sizing rule: the two logotypes are matched on x-height, so "incutec" reads as
the same size of type as the lowercase in "OpenDrone" rather than being scaled
to some arbitrary fraction. Everything sits on one shared baseline.
"""

import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/src"
OUT = ROOT

GOLD = "#c89d2e"          # Brand Gold, the avatar field
GOLD_BRIGHT = "#fdb600"   # gold on dark grounds
TEAL = "#00B2A9"
INK = "#1a1a1e"
PAPER = "#e5e5e5"
BG_DARK = "#0d0d10"
BG_LIGHT = "#f7f6f3"
# connector words take the same ink as "Open": one white on dark, one black on light

WM_TF = "translate(0,433) scale(0.1,-0.1)"
WM_BOX = (-36, -17.32, 2472, 467.64)
MARK_BOX = (-25, -13, 381, 381)

# measured from the artwork (see brandfinal metrics below), in box units
OD_BASELINE = 355.95      # "O" sits on it
OD_XHEIGHT = None         # filled by measure()
INC_BOX = (26.0, 194.0, 448.0, 112.0)
INC_BASELINE = 300.18
INC_XHEIGHT = 72.02
INC_INK_X = (31.82, 468.18)


def od_paths():
    raw = open(f"{SRC}/opendrone-wordmark.svg").read()
    p = re.findall(r'<path d="(.*?)"', raw, re.S)
    assert len(p) == 9
    return [" ".join(x.split()) for x in p]


def inc_paths():
    raw = open(f"{SRC}/incutec-wordmark.svg").read()
    return [("accent" if c == "cls-2" else "text", " ".join(d.split()))
            for c, d in re.findall(r'<path class="(cls-\d)" d="(.*?)"', raw, re.S)]


def measure_od_xheight():
    """Ink bbox of the 'e' glyph, in wordmark box units."""
    from PIL import Image
    d = od_paths()[2]                      # O p e n D r o n e -> index 2 is 'e'
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str, WM_BOX))}">'
         f'<g transform="{WM_TF}" fill-rule="evenodd"><path d="{d}"/></g></svg>')
    open("/tmp/_x.svg", "w").write(s)
    subprocess.run(["rsvg-convert", "-w", "2000", "/tmp/_x.svg", "-o", "/tmp/_x.png"], check=True)
    im = Image.open("/tmp/_x.png").convert("RGBA")
    b = im.getbbox()
    kh = WM_BOX[3] / im.size[1]
    top = WM_BOX[1] + b[1] * kh
    return OD_BASELINE - top


SF = "/System/Library/Fonts/SFNS.ttf"   # SF Pro, the family the wordmark was traced from
_SF_CACHE = {}


def _sf(weight, opsz):
    """SF Pro instantiated at a weight and optical size, cached."""
    key = (weight, opsz)
    if key not in _SF_CACHE:
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont
        _SF_CACHE[key] = instantiateVariableFont(
            TTFont(SF), {"wght": weight, "opsz": opsz}, inplace=True)
    return _SF_CACHE[key]


def sf_glyphs(text, weight=400, opsz=96):
    """SF Pro Display outlines in font units, plus the ink height of its 'e'.

    Matching on the ink height of 'e' rather than the nominal sxHeight keeps the
    connector words on exactly the same x-height as the traced wordmark: both
    measurements then carry the same round-letter overshoot."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.boundsPen import BoundsPen
    f = _sf(weight, opsz)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()

    bp = BoundsPen(gs)
    gs[cmap[ord("e")]].draw(bp)
    e_ink = bp.bounds[3] - bp.bounds[1]

    out, x = [], 0.0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            x += f["head"].unitsPerEm * 0.3
            continue
        pen = SVGPathPen(gs)
        gs[g].draw(pen)
        if pen.getCommands():
            out.append((pen.getCommands(), x))
        x += gs[g].width
    return out, x, e_ink


# ---- emitters. every one takes a baseline y and returns (svg, advance) -----
def od_wordmark(x, baseline, xheight, fills):
    k = xheight / OD_XHEIGHT
    tx, ty = x - (-0.16) * k, baseline - OD_BASELINE * k
    p = od_paths()
    body = "\n".join(
        f'      <path fill="{fills[0] if i < 4 else fills[1]}" d="{d}"/>'
        for i, d in enumerate(p))
    s = (f'  <g transform="translate({tx:.4f},{ty:.4f}) scale({k:.6f})">\n'
         f'    <g transform="{WM_TF}" fill-rule="evenodd">\n{body}\n    </g>\n  </g>\n')
    return s, 2400.3 * k


def inc_wordmark(x, baseline, xheight, text_fill, accent_fill=TEAL):
    k = xheight / INC_XHEIGHT
    tx, ty = x - INC_INK_X[0] * k, baseline - INC_BASELINE * k
    body = "\n".join(
        f'    <path fill="{accent_fill if r == "accent" else text_fill}" d="{d}"/>'
        for r, d in inc_paths())
    s = f'  <g transform="translate({tx:.4f},{ty:.4f}) scale({k:.6f})">\n{body}\n  </g>\n'
    return s, (INC_INK_X[1] - INC_INK_X[0]) * k


def sf_run(text, x, baseline, xheight, fill, weight=400, tracking=0.0):
    glyphs, adv, e_ink = sf_glyphs(text, weight)
    k = xheight / e_ink
    parts, extra = [f'  <g fill="{fill}">'], 0.0
    for i, (d, gx) in enumerate(glyphs):
        parts.append(f'    <path transform="translate({x + gx * k + extra:.3f},{baseline:.3f}) '
                     f'scale({k:.6f},{-k:.6f})" d="{d}"/>')
        extra += tracking
    parts.append("  </g>")
    return "\n".join(parts) + "\n", adv * k + max(0, len(glyphs) - 1) * tracking


def mark(x, y, h, fill):
    k = h / MARK_BOX[3]
    tx, ty = x - MARK_BOX[0] * k, y - MARK_BOX[1] * k
    return (f'  <g transform="translate({tx:.4f},{ty:.4f}) scale({k:.6f})">\n'
            f'    <g transform="{WM_TF}" fill-rule="evenodd">\n'
            f'      <path fill="{fill}" d="{od_paths()[0]}"/>\n    </g>\n  </g>\n'), MARK_BOX[2] * k


def ink_bounds(body, w, h):
    """Ink bbox of a composed body, in user units. Renders once and reads alpha."""
    from PIL import Image
    probe = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}">'
             f'{body}</svg>')
    open("/tmp/_f.svg", "w").write(probe)
    subprocess.run(["rsvg-convert", "-w", "1600", "/tmp/_f.svg", "-o", "/tmp/_f.png"], check=True)
    im = Image.open("/tmp/_f.png").convert("RGBA")
    b = im.getbbox()
    kx, ky = w / im.size[0], h / im.size[1]
    return b[0] * kx, b[1] * ky, b[2] * kx, b[3] * ky


def framed(body, margin, bg=None, label="", canvas=(6000, 3000)):
    """Crop the frame to the artwork plus an even margin, in user units.

    Every asset here is composed on an oversized scratch canvas and then framed,
    so the file has no dead space and whatever lays it out is sizing the artwork
    itself rather than the padding around it."""
    x0, y0, x1, y1 = ink_bounds(body, *canvas)
    x0, y0 = x0 - margin, y0 - margin
    w, h = (x1 - x0) + margin, (y1 - y0) + margin
    rect = f'  <rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>\n' if bg else ""
    a = f' role="img" aria-label="{label}"' if label else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}"{a}>\n{rect}{body}</svg>\n')


def svg(w, h, body, bg=None, label=""):
    rect = f'  <rect width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>\n' if bg else ""
    a = f' role="img" aria-label="{label}"' if label else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="0 0 {w:.2f} {h:.2f}"{a}>\n{rect}{body}</svg>\n')


SUBDIR = {"opendrone-avatar": "avatar"}


def write(name, s, pngs=()):
    sub = SUBDIR.get(name, "lockup")
    d = f"{OUT}/{sub}"
    os.makedirs(d, exist_ok=True)
    p = f"{d}/{name}.svg"
    open(p, "w").write(s)
    for px in pngs:
        subprocess.run(["rsvg-convert", "-w", str(px), p, "-o", f"{d}/{name}-{px}.png"],
                       check=True)
    print("  ", name, *(f"{n}px" for n in pngs))


# ---- assets ----------------------------------------------------------------
def avatar():
    """A3: ink O knocked out of a Brand Gold squircle."""
    S, pad, radius = 1024, 0.195, 0.225
    h = S * (1 - 2 * pad)
    g, w = mark((S - MARK_BOX[2] * (h / MARK_BOX[3])) / 2, S * pad, h, BG_DARK)
    body = f'  <rect width="{S}" height="{S}" rx="{S * radius:.2f}" fill="{GOLD}"/>\n' + g
    write("opendrone-avatar", svg(S, S, body, label="OpenDrone"), (1024, 512, 128, 32))


def lockup_by(name, bg, open_f, drone_f, inc_f, conn_f, pad=0.55, px=1600):
    """OpenDrone by incutec, one line, one baseline."""
    XH = 100.0                       # shared x-height, drives everything
    baseline = 800.0                 # arbitrary, the frame is cropped to the ink
    gap = XH * 0.85
    x = 400.0
    od, w1 = od_wordmark(x, baseline, XH, (open_f, drone_f))
    x += w1 + gap
    by, w2 = sf_run("by", x, baseline, XH, conn_f)
    x += w2 + gap
    ic, w3 = inc_wordmark(x, baseline, XH, inc_f)
    write(name, framed(od + by + ic, XH * pad, bg, "OpenDrone by incutec"), (px,))


def lockup_project(name, bg, open_f, drone_f, inc_f, conn_f, pad=0.55, px=1600):
    """OpenDrone over 'an incutec project'.

    pad is the margin in x-heights, measured from the ink. The default is the
    clear-space rule for a standalone logo file; drop it for a transparent asset
    that gets sized by whatever lays it out, where baked-in margin only shrinks
    the artwork."""
    XH = 100.0
    SUB = XH * 0.42                  # the endorsement line is subordinate
    LEFT = 400.0                     # arbitrary, the frame is cropped to the ink
    b1 = 800.0
    b2 = b1 + XH * 1.35
    od, w1 = od_wordmark(LEFT, b1, XH, (open_f, drone_f))
    gap = SUB * 0.9
    _, wa = sf_run("an", 0, 0, SUB, conn_f)
    _, wi = inc_wordmark(0, 0, SUB, inc_f)
    _, wp = sf_run("project", 0, 0, SUB, conn_f)
    total = wa + gap + wi + gap + wp
    x = LEFT + (w1 - total) / 2
    a, _ = sf_run("an", x, b2, SUB, conn_f)
    i, _ = inc_wordmark(x + wa + gap, b2, SUB, inc_f)
    p, _ = sf_run("project", x + wa + gap + wi + gap, b2, SUB, conn_f)
    write(name, framed(od + a + i + p, XH * pad, bg,
                       "OpenDrone, an incutec project"), (px,))


if __name__ == "__main__":
    OD_XHEIGHT = measure_od_xheight()
    print(f"measured OpenDrone x-height: {OD_XHEIGHT:.2f} box units "
          f"(cap {OD_BASELINE:.0f}, ratio {OD_XHEIGHT / OD_BASELINE:.3f})")
    print("avatar:")
    avatar()
    print("lockups:")
    lockup_by("opendrone-by-incutec-ondark", BG_DARK, PAPER, GOLD_BRIGHT, PAPER, PAPER)
    lockup_by("opendrone-by-incutec-onlight", BG_LIGHT, INK, GOLD, INK, INK)
    lockup_project("opendrone-incutec-project-ondark", BG_DARK, PAPER, GOLD_BRIGHT, PAPER, PAPER)
    lockup_project("opendrone-incutec-project-onlight", BG_LIGHT, INK, GOLD, INK, INK)
    # transparent variants for the GitHub org profile
    lockup_project("opendrone-lockup-ondark", None, PAPER, GOLD_BRIGHT, PAPER, PAPER,
                   pad=0.06, px=2000)
    lockup_project("opendrone-lockup-onlight", None, INK, GOLD, INK, INK,
                   pad=0.06, px=2000)
