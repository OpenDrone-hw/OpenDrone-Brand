#!/usr/bin/env python3
"""Regenerate every OpenDrone identity asset from src/.

    python3 tools/generate.py                     build everything
    python3 tools/generate.py --check             prove the build is reproducible
    python3 tools/generate.py --refresh-outlines  re-cut the type (macOS only)

Deterministic, and --check is how you know: it rebuilds into a scratch tree and
compares. Every SVG is byte-identical anywhere, because geometry is solved
analytically in geometry.py, type comes from frozen outlines in
src/sf-outlines.json, nothing is measured off a raster, and no timestamp or
random value enters a file.

The SVGs are the assets. PDF and PNG are renditions, made by rsvg-convert when
it is installed; their bytes carry the local cairo and libpng, so --check
reports a difference there as renderer drift rather than a build failure.

What it writes:

    mark/       the OD monogram, the primary mark
    wordmark/   the OpenDrone logotype
    avatar/     the mark on a gold squircle, for GitHub and social
    lockup/     OpenDrone with the incutec endorsement
    sheet/      the one-page brand sheet

The mark is the D counter cut out of the O: one vertical line through the O's
counter, closed flat. It is a single path with two contours and no boolean
operation, which is why it stays exact at any size and has no seam.
"""

import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geometry as geo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/src"

# ---- colour ----------------------------------------------------------------
# Read, never declared. tokens.json is the source of truth for every OpenDrone
# colour, screen and physical, and this file is one of its consumers. Putting a
# hex here would make a second source, which is the whole thing tokens.json
# exists to prevent.
import json as _json

_T = _json.load(open(f"{ROOT}/tokens.json"))["screen"]
GOLD = _T["gold"]["hex"]
INK = _T["ink"]["hex"]
PAPER = _T["paper"]["hex"]
BG_DARK = _T["surface_dark"]["hex"]
BG_LIGHT = _T["surface_light"]["hex"]
TEAL = _T["incutec_teal"]["hex"]

# ---- source geometry -------------------------------------------------------
WM_TF = "translate(0,433) scale(0.1,-0.1)"     # traced units -> display units
WM_BOX = (-36, -17.32, 2472, 467.64)

# The mark's divider, as a fraction of the O's outer width. This single number
# is the whole design of the mark: it is where the counter's left arc is
# replaced by a straight line, which is what turns the O's counter into a D's.
STEM_RATIO = 0.4054

INC_BASELINE = 300.18                          # measured off the incutec artwork
INC_XHEIGHT = 72.02
INC_INK_X = (31.82, 468.18)


def _tf_point(x, y):
    """Traced path units -> display units, matching WM_TF."""
    return 0.1 * x, 433 - 0.1 * y


def _tf_box(b):
    x0, y0 = _tf_point(b[0], b[3])
    x1, y1 = _tf_point(b[2], b[1])
    return x0, y0, x1, y1


def od_paths():
    p = re.findall(r'<path d="(.*?)"', open(f"{SRC}/opendrone-wordmark.svg").read(), re.S)
    assert len(p) == 9, f"expected 9 glyph paths (OpenDrone), got {len(p)}"
    return [" ".join(x.split()) for x in p]


def inc_paths():
    raw = open(f"{SRC}/incutec-wordmark.svg").read()
    return [("accent" if c == "cls-2" else "text", " ".join(d.split()))
            for c, d in re.findall(r'<path class="(cls-\d)" d="(.*?)"', raw, re.S)]


_OD = od_paths()
_GLYPH = {n: geo.parse(d) for n, d in zip("OpenDrone", _OD)}   # p,n,e repeat: fine

# Baseline is measured off the artwork and stated as a literal, same as the
# incutec pair below. x-height is baseline to the ink top of 'e', so it carries
# the round-letter overshoot; incutec's is measured the same way, which is what
# makes the two logotypes read as the same size of type rather than being
# scaled to some arbitrary fraction of each other. Exact, not raster-probed.
OD_BASELINE = 355.95
OD_XHEIGHT = OD_BASELINE - _tf_box(geo.bbox(geo.parse(_OD[2])))[1]   # 'e' ink top
WM_INK = _tf_box(geo.bbox([c for d in _OD for c in geo.parse(d)]))


def mark_path():
    """The OD monogram as one path 'd', for fill-rule evenodd."""
    outer, counter = geo.parse(_OD[0])
    ob = geo.bbox([outer])
    cut = ob[0] + STEM_RATIO * (ob[2] - ob[0])
    return geo.to_path([outer, geo.cut_left_of(counter, cut)])


MARK_D = mark_path()
MARK_INK = _tf_box(geo.bbox(geo.parse(MARK_D)))


# ---- svg plumbing ----------------------------------------------------------
def _f(v):
    return geo.fmt(v)


def svg_doc(view, body, bg=None, label=""):
    x, y, w, h = view
    rect = (f'  <rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" '
            f'fill="{bg}"/>\n') if bg else ""
    aria = f' role="img" aria-label="{label}"' if label else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{_f(w)}" height="{_f(h)}" '
            f'viewBox="{_f(x)} {_f(y)} {_f(w)} {_f(h)}"{aria}>\n{rect}{body}</svg>\n')


def framed(body, ink, margin, bg=None, label=""):
    """Crop to the ink plus an even margin. No dead padding in any file."""
    x0, y0, x1, y1 = ink
    view = (x0 - margin, y0 - margin, (x1 - x0) + 2 * margin, (y1 - y0) + 2 * margin)
    return svg_doc(view, body, bg, label)


def _scaled(inner, tx, ty, k):
    return f'  <g transform="translate({_f(tx)},{_f(ty)}) scale({_f(k)})">\n{inner}  </g>\n'


def _box_at(box, tx, ty, k):
    return (tx + box[0] * k, ty + box[1] * k, tx + box[2] * k, ty + box[3] * k)


# ---- emitters. each returns (svg fragment, ink bbox) -----------------------
def wordmark(x, baseline, xheight, open_fill, drone_fill):
    k = xheight / OD_XHEIGHT
    tx, ty = x - WM_INK[0] * k, baseline - OD_BASELINE * k
    glyphs = "".join(
        f'      <path fill="{open_fill if i < 4 else drone_fill}" d="{d}"/>\n'
        for i, d in enumerate(_OD))
    inner = f'    <g transform="{WM_TF}" fill-rule="evenodd">\n{glyphs}    </g>\n'
    return _scaled(inner, tx, ty, k), _box_at(WM_INK, tx, ty, k)


def mark(x, y, height, fill):
    k = height / (MARK_INK[3] - MARK_INK[1])
    tx, ty = x - MARK_INK[0] * k, y - MARK_INK[1] * k
    inner = (f'    <g transform="{WM_TF}" fill-rule="evenodd">\n'
             f'      <path fill="{fill}" d="{MARK_D}"/>\n    </g>\n')
    return _scaled(inner, tx, ty, k), _box_at(MARK_INK, tx, ty, k)


def inc_wordmark(x, baseline, xheight, text_fill, accent_fill=TEAL):
    k = xheight / INC_XHEIGHT
    tx, ty = x - INC_INK_X[0] * k, baseline - INC_BASELINE * k
    body = "".join(
        f'    <path fill="{accent_fill if r == "accent" else text_fill}" d="{d}"/>\n'
        for r, d in inc_paths())
    frag = f'  <g transform="translate({_f(tx)},{_f(ty)}) scale({_f(k)})">\n{body}  </g>\n'
    ink = geo.bbox([c for _, d in inc_paths() for c in geo.parse(d)])
    return frag, (x, ty + ink[1] * k, x + (INC_INK_X[1] - INC_INK_X[0]) * k, ty + ink[3] * k)


# ---- SF Pro, connector words only ------------------------------------------
# The lockups and the sheet set a handful of words in SF Pro and convert them to
# outlines. Reading the font at build time made the output depend on the machine
# twice over: SFNS.ttf ships only with macOS, so a Linux run silently skipped
# those assets, and its outlines change between macOS releases, so two Macs
# could disagree. The outlines are therefore frozen into src/sf-outlines.json,
# which is what a normal build reads. Only --refresh-outlines touches the font,
# and doing so is a deliberate act with a reviewable diff.
SF = "/System/Library/Fonts/SFNS.ttf"
OUTLINES = f"{SRC}/sf-outlines.json"
_SF_CACHE = {}
_REFRESH = "--refresh-outlines" in sys.argv
_FROZEN = {}
_RECORDED = {}

if not _REFRESH and os.path.exists(OUTLINES):
    _FROZEN = _json.load(open(OUTLINES))


def _sf(weight, opsz):
    """The instantiated variable font. Only reachable under --refresh-outlines."""
    key = (weight, opsz)
    if key not in _SF_CACHE:
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont
        _SF_CACHE[key] = instantiateVariableFont(
            TTFont(SF), {"wght": weight, "opsz": opsz}, inplace=True)
    return _SF_CACHE[key]


def _face(weight):
    """Everything the generator needs at one weight: per-character outline and
    advance, plus the two reference heights it scales type by.

    Frozen: read from src/sf-outlines.json, keyed by weight.
    Refreshing: read from the installed font and recorded for writing out.
    """
    key = str(weight)
    if not _REFRESH:
        face = _FROZEN.get("weights", {}).get(key)
        if face is None:
            raise SystemExit(
                f"no frozen outlines for weight {weight} in {OUTLINES}.\n"
                "Run  python3 tools/generate.py --refresh-outlines  on a machine "
                "with SF Pro and fontTools, and commit the result.")
        return face
    face = _RECORDED.setdefault(key, {"glyphs": {}})
    if "e_height" not in face:
        f = _sf(weight, 96)
        gs, cmap = f.getGlyphSet(), f.getBestCmap()
        e = geo.bbox(geo.parse(_pen(gs, cmap[ord("e")])))
        h = geo.bbox(geo.parse(_pen(gs, cmap[ord("H")])))
        face["e_height"] = e[3] - e[1]
        face["cap_height"] = h[3] - h[1]
        face["units_per_em"] = f["head"].unitsPerEm
    return face


def _glyph(weight, ch):
    """Outline and advance for one character, or None where the font has no
    glyph for it (the callers space that case themselves)."""
    face = _face(weight)
    key = f"U+{ord(ch):04X}"
    if not _REFRESH:
        return face["glyphs"].get(key)
    if key not in face["glyphs"]:
        f = _sf(weight, 96)
        gs, cmap = f.getGlyphSet(), f.getBestCmap()
        name = cmap.get(ord(ch))
        face["glyphs"][key] = (
            None if name is None
            else {"d": _pen(gs, name), "adv": gs[name].width})
    return face["glyphs"][key]


def write_outlines():
    """Freeze what this build asked for. Sorted keys and a stable shape, so the
    file diffs line by line when a glyph really changes and not otherwise."""
    from fontTools.ttLib import TTFont
    ver = TTFont(SF)["name"].getDebugName(5) or "unknown"
    doc = {
        "$comment": (
            "SF Pro outlines for the connector words and the brand sheet, frozen "
            "so a build needs neither the font nor macOS. Regenerate with "
            "tools/generate.py --refresh-outlines; review the diff, since it "
            "changes the artwork."),
        "source": {"font": SF, "version": ver.strip(), "optical_size": 96},
        "weights": {
            w: {
                "units_per_em": f["units_per_em"],
                "e_height": f["e_height"],
                "cap_height": f["cap_height"],
                "glyphs": {k: f["glyphs"][k] for k in sorted(f["glyphs"])},
            }
            for w, f in sorted(_RECORDED.items(), key=lambda kv: int(kv[0]))
        },
    }
    open(OUTLINES, "w").write(_json.dumps(doc, indent=2, sort_keys=False) + "\n")
    n = sum(len(f["glyphs"]) for f in _RECORDED.values())
    print(f"   wrote {os.path.relpath(OUTLINES, ROOT)}  "
          f"({n} glyphs, {len(_RECORDED)} weights, {ver.strip()})")


def sf_run(text, x, baseline, xheight, fill, weight=400):
    """Connector words on the same x-height as the traced logotypes."""
    face = _face(weight)
    k = xheight / face["e_height"]
    parts, adv, boxes = [], 0.0, []
    for ch in text:
        g = _glyph(weight, ch)
        if g is None:
            raise SystemExit(f"no glyph for {ch!r} at weight {weight}")
        if g["d"]:
            parts.append(f'    <path transform="translate({_f(x + adv * k)},{_f(baseline)}) '
                         f'scale({_f(k)},{_f(-k)})" d="{g["d"]}"/>\n')
            b = geo.bbox(geo.parse(g["d"]))
            boxes.append((x + (adv + b[0]) * k, baseline - b[3] * k,
                          x + (adv + b[2]) * k, baseline - b[1] * k))
        adv += g["adv"]
    frag = f'  <g fill="{fill}">\n{"".join(parts)}  </g>\n'
    ink = (min(b[0] for b in boxes), min(b[1] for b in boxes),
           max(b[2] for b in boxes), max(b[3] for b in boxes))
    return frag, ink


def _pen(gs, name):
    from fontTools.pens.svgPathPen import SVGPathPen
    pen = SVGPathPen(gs)
    gs[name].draw(pen)
    return pen.getCommands()


def union(*boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


# ---- output ----------------------------------------------------------------
HAVE_RSVG = shutil.which("rsvg-convert") is not None

# cairo, which backs rsvg's PDF writer, stamps a creation date into every PDF.
# Pinning SOURCE_DATE_EPOCH is the reproducible-builds convention for exactly
# this; without it two runs a second apart produce different bytes. Any fixed
# value works, so this one is arbitrary and must simply never change.
ENV = dict(os.environ, SOURCE_DATE_EPOCH="1000000000")


def write(subdir, name, doc, pngs=(), pdf=False, png_bg=None):
    d = f"{ROOT}/{subdir}"
    os.makedirs(d, exist_ok=True)
    path = f"{d}/{name}.svg"
    open(path, "w").write(doc)
    made = ["svg"]
    if HAVE_RSVG:
        if pdf:
            subprocess.run(["rsvg-convert", "-f", "pdf", "-o", f"{d}/{name}.pdf", path],
                           check=True, env=ENV)
            made.append("pdf")
        for px in pngs:
            cmd = ["rsvg-convert", "-f", "png", "-w", str(px), "-o", f"{d}/{name}-{px}.png"]
            if png_bg:
                cmd += ["-b", png_bg]
            subprocess.run(cmd + [path], check=True, env=ENV)
        if pngs:
            made.append("png " + " ".join(str(p) for p in pngs))
    print(f"   {subdir}/{name}  ({', '.join(made)})")


CAP = 1000.0          # nominal drawing size; every file is cropped to its ink
MARGIN = 0.06         # crop margin, in cap heights


def build_mark():
    for name, fill, bg in (("gold", GOLD, None), ("black", "#000000", None),
                           ("white", "#ffffff", BG_DARK)):
        frag, ink = mark(0, 0, CAP, fill)
        doc = framed(frag, ink, CAP * MARGIN, None, "OpenDrone mark")
        write("mark", f"opendrone-mark-{name}", doc, (512, 1024), pdf=True, png_bg=bg)


def build_wordmark():
    variants = (
        ("onlight", INK, GOLD, None, None),
        ("ondark", PAPER, GOLD, None, BG_DARK),
        ("onlight-bg", INK, GOLD, BG_LIGHT, None),
        ("ondark-bg", PAPER, GOLD, BG_DARK, None),
        ("black", "#000000", "#000000", None, None),
        ("white", "#ffffff", "#ffffff", None, BG_DARK),
        ("gold", GOLD, GOLD, None, None),
    )
    for name, of, df, bg, png_bg in variants:
        frag, ink = wordmark(0, OD_BASELINE, OD_XHEIGHT, of, df)
        doc = framed(frag, ink, OD_XHEIGHT * 0.36, bg, "OpenDrone")
        write("wordmark", f"opendrone-wordmark-{name}", doc, (1200, 2400),
              pdf=True, png_bg=png_bg)


def build_avatar():
    """The mark knocked out of a gold squircle."""
    S, pad, radius = 1024.0, 0.18, 0.225
    h = S * (1 - 2 * pad)
    w = h * (MARK_INK[2] - MARK_INK[0]) / (MARK_INK[3] - MARK_INK[1])
    frag, _ = mark((S - w) / 2, S * pad, h, BG_DARK)
    body = f'  <rect width="{_f(S)}" height="{_f(S)}" rx="{_f(S * radius)}" fill="{GOLD}"/>\n' + frag
    write("avatar", "opendrone-avatar", svg_doc((0, 0, S, S), body, label="OpenDrone"),
          (1024, 512, 128, 32))


def build_lockups():
    XH, BASE, LEFT = 100.0, 800.0, 400.0
    for name, bg, open_f, inc_f, conn_f, pad, px in (
            ("opendrone-incutec-project-ondark", BG_DARK, PAPER, PAPER, PAPER, 0.55, 1600),
            ("opendrone-incutec-project-onlight", BG_LIGHT, INK, INK, INK, 0.55, 1600),
            ("opendrone-lockup-ondark", None, PAPER, PAPER, PAPER, 0.06, 2000),
            ("opendrone-lockup-onlight", None, INK, INK, INK, 0.06, 2000)):
        SUB = XH * 0.42
        b2 = BASE + XH * 1.35
        od, od_ink = wordmark(LEFT, BASE, XH, open_f, GOLD)
        w1 = od_ink[2] - od_ink[0]
        gap = SUB * 0.9
        _, ab = sf_run("an", 0, 0, SUB, conn_f)
        _, ib = inc_wordmark(0, 0, SUB, inc_f)
        _, pb = sf_run("project", 0, 0, SUB, conn_f)
        wa, wi, wp = ab[2] - ab[0], ib[2] - ib[0], pb[2] - pb[0]
        x = LEFT + (w1 - (wa + gap + wi + gap + wp)) / 2
        a, a_ink = sf_run("an", x, b2, SUB, conn_f)
        i, i_ink = inc_wordmark(x + wa + gap, b2, SUB, inc_f)
        p, p_ink = sf_run("project", x + wa + gap + wi + gap, b2, SUB, conn_f)
        doc = framed(od + a + i + p, union(od_ink, a_ink, i_ink, p_ink),
                     XH * pad, bg, "OpenDrone, an incutec project")
        write("lockup", name, doc, (px,))


def text(txt, x, y, px, fill, weight=400, anchor="start"):
    """SF Pro as outlines, positioned by cap height in px. The committed SVG
    carries no font dependency, and neither does the build: outlines come from
    src/sf-outlines.json."""
    face = _face(weight)
    k = px / face["cap_height"]
    parts, adv = [], 0.0
    for ch in txt:
        g = _glyph(weight, ch)
        if g is None:
            adv += face["units_per_em"] * 0.28
            continue
        if g["d"]:
            parts.append((g["d"], adv))
        adv += g["adv"]
    w = adv * k
    ox = x - w if anchor == "end" else (x - w / 2 if anchor == "middle" else x)
    body = "".join(
        f'    <path transform="translate({_f(ox + a * k)},{_f(y)}) '
        f'scale({_f(k)},{_f(-k)})" d="{d}"/>\n' for d, a in parts)
    return f'  <g fill="{fill}">\n{body}  </g>\n', w


def build_sheet():
    """One page a vendor or a journalist can be handed. Text is outlined, so it
    renders identically everywhere and cannot silently fall back to a substitute
    face the way the previous sheet did."""
    W, H = 1600.0, 800.0
    INK_L, MUTE = INK, "#6b6459"
    b = [f'  <rect width="{_f(W)}" height="{_f(H)}" fill="#ffffff"/>\n']
    b.append(text("OpenDrone brand sheet", 80, 96, 40, INK_L, 700)[0])
    b.append(text("One gold. One mark. Generated, never hand-placed.",
                  80, 136, 17, MUTE)[0])
    b.append(f'  <rect x="80" y="168" width="{_f(W - 160)}" height="1" fill="#e3ded2"/>\n')

    def cap(t, x, y):
        b.append(text(t, x, y, 11, MUTE, 500)[0])

    # wordmark, both grounds
    cap("PRIMARY / ON LIGHT", 80, 210)
    wm, ink = wordmark(80, 300, 62, INK, GOLD)
    b.append(wm)
    cap("PRIMARY / ON DARK", 840, 210)
    b.append(f'  <rect x="820" y="232" width="700" height="110" rx="10" fill="{BG_DARK}"/>\n')
    wm2, _ = wordmark(860, 300, 62, PAPER, GOLD)
    b.append(wm2)

    # mark + avatar
    cap("MARK", 80, 420)
    m1, _ = mark(80, 440, 110, GOLD)
    b.append(f'  <rect x="60" y="420" width="150" height="150" rx="10" fill="{BG_DARK}"/>\n')
    b.append(m1)
    m2, _ = mark(250, 440, 110, INK)
    b.append(m2)
    cap("AVATAR", 440, 420)
    b.append(f'  <rect x="440" y="440" width="150" height="150" rx="34" fill="{GOLD}"/>\n')
    m3, mi = mark(440 + (150 - 110 * (MARK_INK[2] - MARK_INK[0]) / (MARK_INK[3] - MARK_INK[1])) / 2,
                  460, 110, BG_DARK)
    b.append(m3)

    # colour
    cap("COLOUR / SCREEN", 840, 420)
    sw = [("Gold", GOLD), ("Ink", INK), ("Off-white", PAPER),
          ("Surface dark", BG_DARK), ("Surface light", BG_LIGHT)]
    for i, (n, hx) in enumerate(sw):
        x = 840 + i * 136
        b.append(f'  <rect x="{_f(x)}" y="440" width="120" height="76" rx="7" fill="{hx}" '
                 f'stroke="#e3ded2"/>\n')
        b.append(text(n, x, 540, 12, INK_L, 600)[0])
        b.append(text(hx, x, 560, 12, MUTE)[0])

    cap("COLOUR / PHYSICAL", 840, 600)
    b.append(text("Pantone 1235 C is the master. dE2000 0.82 from the screen gold.",
                  840, 626, 15, INK_L)[0])
    b.append(text("Every substrate matches the chip, never the hex and never another substrate.",
                  840, 650, 15, MUTE)[0])
    b.append(text("#ffb700 is outside CMYK gamut: specify the spot ink, never a process build.",
                  840, 674, 15, MUTE)[0])

    cap("CLEAR SPACE", 80, 640)
    b.append(text("At least the height of the O on every side.", 80, 666, 15, MUTE)[0])
    b.append(text("Minimum wordmark width 120 px on screen, 25 mm in print.", 80, 690, 15, MUTE)[0])

    b.append(f'  <rect x="80" y="{_f(H - 96)}" width="{_f(W - 160)}" height="1" fill="#e3ded2"/>\n')
    b.append(text("opendrone.store", 80, H - 56, 15, MUTE, 600)[0])
    b.append(text("Trademarks. See README before use.", W - 80, H - 56, 15, MUTE,
                  anchor="end")[0])
    write("sheet", "opendrone-brand-sheet",
          svg_doc((0, 0, W, H), "".join(b), label="OpenDrone brand sheet"),
          (1600,), pdf=True)

def build_all():
    print("mark:")
    build_mark()
    print("wordmark:")
    build_wordmark()
    print("avatar:")
    build_avatar()
    print("lockups:")
    build_lockups()
    print("sheet:")
    build_sheet()


def check():
    """Rebuild into a scratch tree and compare, so determinism is something the
    repo proves rather than claims.

    SVG is generated here in pure Python and must match byte for byte; a
    mismatch is a bug or an uncommitted edit. PDF and PNG come out of
    rsvg-convert, so their bytes follow the installed cairo and libpng and are
    only comparable against the machine that last wrote them: they are reported
    separately and do not fail the check.
    """
    import filecmp
    import tempfile

    global ROOT
    committed, tmp = ROOT, tempfile.mkdtemp(prefix="brand-check-")
    try:
        ROOT = tmp
        build_all()
    finally:
        ROOT = committed

    svg_bad, raster_bad, missing = [], [], []
    for sub in ("mark", "wordmark", "avatar", "lockup", "sheet"):
        d = f"{tmp}/{sub}"
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            rel = f"{sub}/{name}"
            here = f"{committed}/{rel}"
            if not os.path.exists(here):
                missing.append(rel)
            elif not filecmp.cmp(f"{d}/{name}", here, shallow=False):
                (svg_bad if name.endswith(".svg") else raster_bad).append(rel)

    shutil.rmtree(tmp, ignore_errors=True)
    print()
    if missing:
        print(f"missing from the repo ({len(missing)}):")
        for r in missing:
            print(f"   {r}")
    if raster_bad:
        print(f"renderer drift, not a determinism failure ({len(raster_bad)} "
              f"file(s)): rsvg-convert here differs from the one that wrote the "
              f"committed renditions. Rerun the generator to adopt this machine's.")
        for r in raster_bad:
            print(f"   {r}")
    if svg_bad:
        print(f"NOT DETERMINISTIC: {len(svg_bad)} SVG(s) differ from the committed build:")
        for r in svg_bad:
            print(f"   {r}")
        return 1
    if missing:
        return 1
    print("deterministic: every committed SVG is byte-identical to a fresh build.")
    return 0


if __name__ == "__main__":
    print(f"gold {GOLD} · baseline {OD_BASELINE:.3f} · x-height {OD_XHEIGHT:.3f} "
          f"· stem ratio {STEM_RATIO}")
    if not HAVE_RSVG:
        print("   rsvg-convert not found: writing SVG only")
    if _REFRESH:
        print(f"   refreshing outlines from {SF}")
    if "--check" in sys.argv:
        sys.exit(check())
    build_all()
    if _REFRESH:
        write_outlines()
