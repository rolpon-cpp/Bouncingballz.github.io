# Written by Claude Sonnet 5.5
"""Drawing helpers for the thumbnail: a smug cartoon mod, a giant gavel and a tiny crown (Pillow only).

Everything is original and drawn in code at 2x scale (the caller downsamples for smooth edges).
Coordinates are in 1280 x 720 thumbnail units; S is the supersampling factor.
"""
import math

from PIL import Image, ImageDraw, ImageFilter

S = 2
OUTLINE = (42, 33, 64, 255)
SKIN = (233, 185, 149, 255)
SKIN_SHADE = (205, 150, 116, 255)


def sc(v):
    return int(round(v * S))


def pts(points):
    return [(sc(x), sc(y)) for x, y in points]


def rot(points, deg, cx, cy):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def bezier(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def thick_line(d, points, width, fill):
    """Polyline with round caps and joins."""
    d.line(pts(points), fill=fill, width=sc(width), joint="curve")
    r = width / 2
    for x, y in (points[0], points[-1]):
        d.ellipse([sc(x - r), sc(y - r), sc(x + r), sc(y + r)], fill=fill)


def ellipse(d, cx, cy, rx, ry, fill, outline=None, ow=0):
    d.ellipse([sc(cx - rx), sc(cy - ry), sc(cx + rx), sc(cy + ry)], fill=fill, outline=outline, width=sc(ow))


def crown(layer, cx, cy, width, tilt=-14):
    """A tiny gold crown centred on (cx, cy)."""
    d = ImageDraw.Draw(layer)
    w = width
    base = [(-0.5, 0.25), (-0.5, -0.2), (-0.22, 0.0), (0.0, -0.42), (0.22, 0.0), (0.5, -0.2), (0.5, 0.25)]
    p = rot([(cx + x * w, cy + y * w) for x, y in base], tilt, cx, cy)
    d.polygon(pts(p), fill=(255, 207, 51, 255), outline=OUTLINE, width=sc(5))
    band = rot([(cx - 0.5 * w, cy + 0.12 * w), (cx + 0.5 * w, cy + 0.12 * w), (cx + 0.5 * w, cy + 0.3 * w), (cx - 0.5 * w, cy + 0.3 * w)], tilt, cx, cy)
    d.polygon(pts(band), fill=(211, 154, 0, 255), outline=OUTLINE, width=sc(4))
    for (gx, gy), col in zip([(-0.5, -0.22), (0.0, -0.44), (0.5, -0.22)], [(255, 77, 94, 255), (90, 169, 255, 255), (57, 217, 138, 255)]):
        (qx, qy), = rot([(cx + gx * w, cy + gy * w)], tilt, cx, cy)
        ellipse(d, qx, qy, w * 0.07, w * 0.07, col, OUTLINE, 3)


def draw_mod(layer, cx, cy, r):
    """Smug cartoon moderator: hoodie, round head, hair, half-lidded eyes, raised brow, smirk. Head centre (cx, cy)."""
    d = ImageDraw.Draw(layer)
    # hoodie body (runs off the bottom of the canvas)
    d.rounded_rectangle([sc(cx - r * 1.55), sc(cy + r * 0.88), sc(cx + r * 1.55), sc(cy + r * 3.2)], radius=sc(r * 0.7),
                        fill=(109, 75, 216, 255), outline=OUTLINE, width=sc(7))
    ellipse(d, cx, cy + r * 1.0, r * 0.72, r * 0.2, (90, 60, 192, 255), OUTLINE, 5)
    for dx in (-0.12, 0.12):
        thick_line(d, [(cx + dx * r * 1.3, cy + r * 1.1), (cx + dx * r * 1.45, cy + r * 1.75)], 7, (255, 255, 255, 230))
    # head
    ellipse(d, cx, cy, r, r, SKIN, OUTLINE, 8)
    d.pieslice([sc(cx - r * 0.9), sc(cy - r * 0.55), sc(cx + r * 0.9), sc(cy + r * 1.05)], 20, 160, fill=SKIN_SHADE)
    ellipse(d, cx, cy - r * 0.04, r * 0.97, r * 0.97, SKIN)
    # hair: dark cap with spikes
    d.pieslice([sc(cx - r * 1.02), sc(cy - r * 1.02), sc(cx + r * 1.02), sc(cy + r * 1.02)], 188, 352, fill=OUTLINE)
    for off, up in ((-0.5, 1.2), (-0.05, 1.24), (0.4, 1.18)):
        d.polygon(pts([(cx + r * (off - 0.2), cy - r * 0.9), (cx + r * (off + 0.2), cy - r * 0.9), (cx + r * off, cy - r * up)]), fill=OUTLINE)
    # fringe line so the hair reads as a cap
    thick_line(d, bezier((cx - r * 0.98, cy - r * 0.32), (cx - r * 0.4, cy - r * 0.72), (cx + r * 0.4, cy - r * 0.45), (cx + r * 0.98, cy - r * 0.34)), 9, OUTLINE)
    # eyes: white, pupil looking sideways, heavy lids
    for ex in (-0.4, 0.38):
        x, y = cx + ex * r, cy + 0.02 * r
        ellipse(d, x, y, r * 0.23, r * 0.17, (255, 255, 255, 255), OUTLINE, 5)
        ellipse(d, x + r * 0.07, y + r * 0.01, r * 0.075, r * 0.075, (26, 29, 43, 255))
        d.rectangle([sc(x - r * 0.24), sc(y - r * 0.19), sc(x + r * 0.24), sc(y - r * 0.01)], fill=SKIN)
        thick_line(d, [(x - r * 0.25, y - r * 0.01), (x + r * 0.25, y - r * 0.01)], 9, OUTLINE)
    # eyebrows: left one raised, right one flat and low
    thick_line(d, [(cx - r * 0.7, cy - r * 0.24), (cx - r * 0.12, cy - r * 0.42)], 13, OUTLINE)
    thick_line(d, [(cx + r * 0.17, cy - r * 0.22), (cx + r * 0.68, cy - r * 0.2)], 13, OUTLINE)
    # smirk
    thick_line(d, bezier((cx - r * 0.45, cy + r * 0.5), (cx - r * 0.12, cy + r * 0.7), (cx + r * 0.3, cy + r * 0.68), (cx + r * 0.62, cy + r * 0.32)), 12, OUTLINE)
    thick_line(d, [(cx + r * 0.62, cy + r * 0.32), (cx + r * 0.72, cy + r * 0.4)], 9, OUTLINE)
    blush = Image.new("RGBA", layer.size, (0, 0, 0, 0))             # blend on a temporary layer so skin shows through
    bd = ImageDraw.Draw(blush)
    for ex in (-0.68, 0.7):
        ellipse(bd, cx + ex * r, cy + 0.3 * r, r * 0.17, r * 0.09, (255, 110, 140, 110))
    layer.alpha_composite(blush)
    crown(layer, cx - r * 0.2, cy - r * 1.06, r * 0.62, -14)


def gavel_layer(size=(760, 980)):
    """A giant gavel standing upright on its own transparent layer (head up). Returns (image, handle_bottom_xy)."""
    W, H = size
    img = Image.new("RGBA", (sc(W), sc(H)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    wood, dark, light, brass = (192, 122, 58, 255), (142, 84, 38, 255), (236, 170, 100, 255), (232, 185, 74, 255)
    # handle
    d.rounded_rectangle([sc(W / 2 - 42), sc(250), sc(W / 2 + 42), sc(H - 20)], radius=sc(40), fill=wood, outline=OUTLINE, width=sc(8))
    d.rounded_rectangle([sc(W / 2 - 42), sc(H - 250), sc(W / 2 + 42), sc(H - 20)], radius=sc(40), fill=dark, outline=OUTLINE, width=sc(8))
    d.rounded_rectangle([sc(W / 2 - 20), sc(280), sc(W / 2 - 8), sc(H - 270)], radius=sc(8), fill=light)
    # head
    d.rounded_rectangle([sc(40), sc(30), sc(W - 40), sc(300)], radius=sc(80), fill=wood, outline=OUTLINE, width=sc(9))
    d.rounded_rectangle([sc(40), sc(180), sc(W - 40), sc(300)], radius=sc(70), fill=dark)
    d.rounded_rectangle([sc(40), sc(30), sc(W - 40), sc(300)], radius=sc(80), outline=OUTLINE, width=sc(9))
    for x in (120, W - 120 - 50):
        d.rectangle([sc(x), sc(30), sc(x + 50), sc(300)], fill=brass, outline=OUTLINE, width=sc(6))
    d.rounded_rectangle([sc(150), sc(60), sc(W - 150), sc(100)], radius=sc(20), fill=light)
    return img


def starburst(layer, cx, cy, r_out, r_in, n, fill, outline=None):
    d = ImageDraw.Draw(layer)
    pts_ = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r_out if i % 2 == 0 else r_in
        pts_.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts(pts_), fill=fill, outline=outline, width=sc(6) if outline else 0)


def glow(size, cx, cy, rx, ry, color, blur):
    """A soft coloured ellipse on a transparent layer."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([sc(cx - rx), sc(cy - ry), sc(cx + rx), sc(cy + ry)], fill=color)
    return layer.filter(ImageFilter.GaussianBlur(sc(blur)))
