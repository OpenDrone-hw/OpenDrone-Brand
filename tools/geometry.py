#!/usr/bin/env python3
"""Exact path geometry for the OpenDrone identity.

Everything here is analytic. Nothing is measured off a raster, so the numbers
are identical on every machine and at every zoom level, and the generator can
be trusted to produce byte-identical output from the same source artwork.

Only cubic Beziers, lines and closepaths appear in the traced logotypes, which
is why the parser handles exactly those.
"""

import math
import re

TOKEN = re.compile(r"([MmCcLlZzHhVvQqSsTt])|(-?\d*\.?\d+(?:[eE][-+]?\d+)?)")

# Number formatting is pinned so two runs cannot disagree in the last digit.
PRECISION = 4


def fmt(v):
    """Fixed-precision, trailing zeros stripped, no negative zero."""
    s = f"{v:.{PRECISION}f}"
    if s.startswith("-") and float(s) == 0:
        s = s[1:]
    s = s.rstrip("0").rstrip(".")
    return s or "0"


def parse(d):
    """Path data -> list of contours, each a list of absolute cubics (p0,p1,p2,p3).

    Lines are stored as degenerate cubics so every consumer sees one segment
    type. Closing lines are inserted explicitly, so a contour is always closed.
    """
    toks = [a or b for a, b in TOKEN.findall(d)]
    i = 0
    cur = start = (0.0, 0.0)
    cmd = None
    contours = []
    con = []

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v

    prev_c2 = None      # for S/s
    prev_q1 = None      # for T/t

    def line_to(pt):
        con.append((cur, cur, pt, pt))

    def quad_to(q, pt):
        """Exact quadratic -> cubic. TrueType outlines arrive as quadratics."""
        c1 = (cur[0] + 2 / 3 * (q[0] - cur[0]), cur[1] + 2 / 3 * (q[1] - cur[1]))
        c2 = (pt[0] + 2 / 3 * (q[0] - pt[0]), pt[1] + 2 / 3 * (q[1] - pt[1]))
        con.append((cur, c1, c2, pt))

    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]
            i += 1
            if i >= len(toks) and cmd not in "Zz":
                break
        if cmd in ("M", "m"):
            x, y = num(), num()
            if cmd == "m":
                x, y = cur[0] + x, cur[1] + y
            if con:
                contours.append(con)
                con = []
            cur = start = (x, y)
            cmd = "L" if cmd == "M" else "l"          # implicit lineto, per spec
        elif cmd in ("C", "c"):
            a = [num() for _ in range(6)]
            if cmd == "c":
                a = [a[0] + cur[0], a[1] + cur[1],
                     a[2] + cur[0], a[3] + cur[1],
                     a[4] + cur[0], a[5] + cur[1]]
            con.append((cur, (a[0], a[1]), (a[2], a[3]), (a[4], a[5])))
            prev_c2, prev_q1 = (a[2], a[3]), None
            cur = (a[4], a[5])
        elif cmd in ("S", "s"):
            a = [num() for _ in range(4)]
            if cmd == "s":
                a = [a[0] + cur[0], a[1] + cur[1], a[2] + cur[0], a[3] + cur[1]]
            c1 = (2 * cur[0] - prev_c2[0], 2 * cur[1] - prev_c2[1]) if prev_c2 else cur
            con.append((cur, c1, (a[0], a[1]), (a[2], a[3])))
            prev_c2, prev_q1 = (a[0], a[1]), None
            cur = (a[2], a[3])
        elif cmd in ("Q", "q"):
            a = [num() for _ in range(4)]
            if cmd == "q":
                a = [a[0] + cur[0], a[1] + cur[1], a[2] + cur[0], a[3] + cur[1]]
            quad_to((a[0], a[1]), (a[2], a[3]))
            prev_q1, prev_c2 = (a[0], a[1]), None
            cur = (a[2], a[3])
        elif cmd in ("T", "t"):
            x, y = num(), num()
            if cmd == "t":
                x, y = cur[0] + x, cur[1] + y
            q = (2 * cur[0] - prev_q1[0], 2 * cur[1] - prev_q1[1]) if prev_q1 else cur
            quad_to(q, (x, y))
            prev_q1, prev_c2 = q, None
            cur = (x, y)
        elif cmd in ("L", "l"):
            x, y = num(), num()
            if cmd == "l":
                x, y = cur[0] + x, cur[1] + y
            line_to((x, y))
            cur = (x, y)
        elif cmd in ("H", "h"):
            x = num()
            if cmd == "h":
                x += cur[0]
            line_to((x, cur[1]))
            cur = (x, cur[1])
        elif cmd in ("V", "v"):
            y = num()
            if cmd == "v":
                y += cur[1]
            line_to((cur[0], y))
            cur = (cur[0], y)
        elif cmd in ("Z", "z"):
            if cur != start:
                line_to(start)
            cur = start
            contours.append(con)
            con = []
        else:
            raise ValueError(f"unsupported path command {cmd!r}")
    if con:
        contours.append(con)
    return contours


def at(a, b, c, d, t):
    u = 1 - t
    return u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d


def point(seg, t):
    return (at(seg[0][0], seg[1][0], seg[2][0], seg[3][0], t),
            at(seg[0][1], seg[1][1], seg[2][1], seg[3][1], t))


def _extrema(a, b, c, d):
    """Parameters where a 1-D cubic Bezier turns."""
    A = -a + 3 * b - 3 * c + d
    B = 2 * (a - 2 * b + c)
    C = b - a
    if abs(A) < 1e-12:
        if abs(B) < 1e-12:
            return []
        return [t for t in (-C / B,) if 0 < t < 1]
    disc = B * B - 4 * A * C
    if disc < 0:
        return []
    s = math.sqrt(disc)
    return [t for t in ((-B + s) / (2 * A), (-B - s) / (2 * A)) if 0 < t < 1]


def bbox(contours):
    """Exact ink bounds. Includes curve extrema, not just anchor points."""
    xs, ys = [], []
    for con in contours:
        for seg in con:
            for axis, acc in ((0, xs), (1, ys)):
                a, b, c, d = (p[axis] for p in seg)
                acc.append(a)
                acc.append(d)
                acc.extend(at(a, b, c, d, t) for t in _extrema(a, b, c, d))
    return min(xs), min(ys), max(xs), max(ys)


def _roots_x(seg, x):
    """Parameters where a cubic crosses the vertical line at x."""
    x0, x1, x2, x3 = (p[0] for p in seg)
    A = -x0 + 3 * x1 - 3 * x2 + x3
    B = 3 * x0 - 6 * x1 + 3 * x2
    C = -3 * x0 + 3 * x1
    D = x0 - x
    if abs(A) < 1e-9:
        if abs(B) < 1e-9:
            return [] if abs(C) < 1e-9 else _keep(-D / C)
        disc = C * C - 4 * B * D
        if disc < 0:
            return []
        s = math.sqrt(disc)
        return _keep((-C + s) / (2 * B), (-C - s) / (2 * B))
    b, c, d = B / A, C / A, D / A
    p = c - b * b / 3
    q = 2 * b ** 3 / 27 - b * c / 3 + d
    disc = (q / 2) ** 2 + (p / 3) ** 3
    if disc > 0:
        s = math.sqrt(disc)
        u = math.copysign(abs(-q / 2 + s) ** (1 / 3), -q / 2 + s)
        v = math.copysign(abs(-q / 2 - s) ** (1 / 3), -q / 2 - s)
        return _keep(u + v - b / 3)
    r = math.sqrt(max(0.0, -p ** 3 / 27))
    phi = math.acos(max(-1.0, min(1.0, -q / (2 * r)))) if r else 0.0
    m = 2 * math.sqrt(max(0.0, -p / 3))
    return _keep(*(m * math.cos((phi + 2 * math.pi * k) / 3) - b / 3 for k in range(3)))


def _keep(*ts):
    return sorted(t for t in ts if 1e-9 < t < 1 - 1e-9)


def _split(seg, t):
    p0, p1, p2, p3 = seg
    lerp = lambda a, b: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    a, b, c = lerp(p0, p1), lerp(p1, p2), lerp(p2, p3)
    d, e = lerp(a, b), lerp(b, c)
    f = lerp(d, e)
    return (p0, a, d, f), (f, e, c, p3)


def cut_left_of(contour, x):
    """Keep the part of a closed contour at or right of x, close it flat.

    The O's counter is convex, so a vertical line crosses it exactly twice and
    the kept side is a single arc. Closing it with a straight line is what turns
    the counter into a D counter, and it is why the mark needs no boolean
    library: the result is one contour, exact, with no seam.
    """
    pieces = []
    for seg in contour:
        cur, base = seg, 0.0
        for t in _roots_x(seg, x):
            head, cur = _split(cur, (t - base) / (1 - base))
            pieces.append(head)
            base = t
        pieces.append(cur)

    kept = [point(s, 0.5)[0] >= x for s in pieces]
    if all(kept) or not any(kept):
        raise ValueError(f"vertical line at {x} does not cut this contour")

    n = len(pieces)
    start = next(i for i in range(n) if kept[i] and not kept[(i - 1) % n])
    run, i = [], start
    while kept[i]:
        run.append(pieces[i])
        i = (i + 1) % n
    return run


def to_path(contours):
    """Contours -> a single path 'd', for fill-rule evenodd."""
    out = []
    for con in contours:
        p0 = con[0][0]
        out.append(f"M{fmt(p0[0])} {fmt(p0[1])}")
        for _, p1, p2, p3 in con:
            out.append(f"C{fmt(p1[0])} {fmt(p1[1])} "
                       f"{fmt(p2[0])} {fmt(p2[1])} {fmt(p3[0])} {fmt(p3[1])}")
        out.append("Z")
    return " ".join(out)
