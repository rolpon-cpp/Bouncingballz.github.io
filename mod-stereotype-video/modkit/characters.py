# Written by Claude Sonnet 5.5
"""Original flat vector characters. All names and faces are invented."""
import numpy as np
from manim import *

from .icons import crown
from .theme import *


def avatar(letter, color, r=0.25, ring=None):
    """Round avatar with an initial."""
    base = disc(r, color)
    t = T(letter.upper(), size=max(14, int(r * 135 * 1.0)), weight="HEAVY", color="#10121b")
    t.move_to(base.get_center())
    g = VGroup(base, t)
    if ring:
        g.add(Circle(radius=r + 0.04, stroke_color=ring, stroke_width=3, fill_opacity=0))
    return g


def bust(color, r=0.3, skin=SKIN, hair=None, bg=None, face=False):
    """Head and shoulders icon. Width is about 2r * 1.7."""
    shoulders = Sector(radius=r * 1.5, angle=PI, start_angle=0, fill_color=color, fill_opacity=1, stroke_width=0)
    shoulders.stretch_to_fit_height(r * 1.05)
    shoulders.move_to([0, -r * 0.72, 0])
    head = disc(r * 0.62, skin).move_to([0, r * 0.42, 0])
    parts = [shoulders, head]
    if hair:
        cap = Sector(radius=r * 0.66, angle=PI * 0.92, start_angle=PI * 0.04, fill_color=hair, fill_opacity=1, stroke_width=0)
        cap.move_to(head.get_center() + UP * r * 0.14)
        parts.append(cap)
    if face:
        hc = head.get_center()
        for dx in (-0.2, 0.2):
            parts.append(disc(r * 0.055, "#1a1d2b").move_to(hc + np.array([dx * r * 1.0, -r * 0.02, 0])))
        smile = Arc(radius=r * 0.2, start_angle=PI + 0.5, angle=PI - 1.0, stroke_color="#7a3b2e", stroke_width=3).move_to(hc + np.array([0, -r * 0.25, 0]))
        parts.append(smile)
    g = VGroup(*parts)
    if bg is not None:
        g.add_to_back(disc(r * 1.55, bg))
    return g


def smug_face(head_r=0.5, skin=SKIN):
    """Half-lidded eyes, one raised eyebrow, lopsided smirk. Centred on the head centre."""
    s = head_r / 0.5
    parts = VGroup()
    for x in (-0.18, 0.18):
        white = Ellipse(width=0.24, height=0.18, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to([x, 0.04, 0])
        pupil = disc(0.05, "#1a1d2b").move_to([x + 0.035, 0.015, 0])
        lid = Rectangle(width=0.27, height=0.105, fill_color=skin, fill_opacity=1, stroke_width=0).move_to([x, 0.085, 0])
        lid_line = rstroke(Line([x - 0.13, 0.045, 0], [x + 0.13, 0.045, 0]), "#2a2140", 4)
        parts.add(white, pupil, lid, lid_line)
    brow_l = rstroke(Line([-0.31, 0.19, 0], [-0.07, 0.3, 0]), "#2a2140", 6)
    brow_r = rstroke(Line([0.08, 0.2, 0], [0.3, 0.19, 0]), "#2a2140", 6)
    smirk = VMobject()
    smirk.start_new_path(np.array([-0.16, -0.19, 0]))
    smirk.add_cubic_bezier_curve_to(np.array([-0.05, -0.27, 0]), np.array([0.1, -0.26, 0]), np.array([0.23, -0.12, 0]))
    rstroke(smirk, "#2a2140", 5)
    smirk.set_fill(opacity=0)
    tick = rstroke(Line([0.23, -0.12, 0], [0.27, -0.08, 0]), "#2a2140", 4)
    cheeks = VGroup(*[Ellipse(width=0.13, height=0.07, fill_color=PINK, fill_opacity=0.35, stroke_width=0).move_to([x, -0.08, 0])
                      for x in (-0.3, 0.3)])
    parts.add(cheeks, brow_l, brow_r, smirk, tick)
    return parts.scale(s)


def cartoon_mod(scale=1.0, with_crown=True, hoodie=PURPLE_DEEP, hair="#2a2140"):
    """A smug cartoon moderator: round head, tiny crown, purple hoodie. Centre is the head centre."""
    body = rrect(1.35, 1.0, 0.36, hoodie).move_to([0, -0.88, 0])
    collar = Ellipse(width=0.78, height=0.3, fill_color="#5a3cc0", fill_opacity=1, stroke_width=0).move_to([0, -0.5, 0])
    strings = VGroup(Line([-0.12, -0.55, 0], [-0.14, -0.85, 0]), Line([0.12, -0.55, 0], [0.14, -0.85, 0]))
    rstroke(strings, WHITE, 3, 0.8)
    head = disc(0.5, SKIN)
    cap = Sector(radius=0.53, angle=PI * 0.9, start_angle=PI * 0.05, fill_color=hair, fill_opacity=1, stroke_width=0).shift(UP * 0.08)
    spikes = VGroup(*[Polygon([x - 0.08, 0.42, 0], [x + 0.08, 0.42, 0], [x + 0.02, 0.62, 0], fill_color=hair, fill_opacity=1, stroke_width=0)
                      for x in (-0.22, 0.0, 0.22)])
    face = smug_face(0.5, SKIN).shift(DOWN * 0.04)
    parts = [body, collar, strings, head, cap, spikes, face]
    g = VGroup(*parts)
    if with_crown:
        cr = crown(0.36).rotate(-0.15).move_to([0.06, 0.66, 0])
        g.add(cr)
        g.crown = cr
    g.head_center = ORIGIN.copy()
    g.shoulder_point = np.array([0.55, -0.62, 0])
    return g.scale(scale)


def hand_tired(skin=SKIN, sleeve="#4b5675"):
    """A relaxed hand drawn top-down, fingers pointing UP, with a sleeve running down off the bottom."""
    sk = skin
    palm = rrect(0.95, 0.95, 0.3, sk)
    fingers = VGroup()
    for x, ln, ang in [(-0.34, 0.66, 8), (-0.115, 0.8, 3), (0.115, 0.74, -2), (0.34, 0.54, -9)]:
        f = rrect(0.2, ln, 0.1, sk)
        f.move_to([x, 0.38 + ln / 2 - 0.12, 0]).rotate(np.radians(ang), about_point=np.array([x, 0.3, 0]))
        fingers.add(f)
    thumb = rrect(0.22, 0.56, 0.11, sk).rotate(np.radians(52)).move_to([-0.58, -0.02, 0])
    seams = VGroup(*[Line([x, 0.34, 0], [x, 0.0, 0]).set_stroke(SKIN_DARK, width=3, opacity=0.7) for x in (-0.23, 0.0, 0.23)])
    nails = VGroup(*[rrect(0.11, 0.1, 0.04, "#f6d6bf").move_to(f.get_top() + DOWN * 0.1).rotate(np.radians(a))
                     for f, a in zip(fingers, (8, 3, -2, -9))])
    cuff = rrect(1.2, 0.34, 0.12, "#6b7799").move_to([0, -0.62, 0])
    arm = rrect(1.15, 6.0, 0.2, sleeve).move_to([0, -3.55, 0])
    g = VGroup(arm, thumb, palm, fingers, seams, nails, cuff)
    return g


def priya_back(scale=1.0):
    """Back view of a person at a desk: hair bun, head, shoulders in a hoodie. Rim-lit by a screen."""
    dark, hair = "#1a1e32", "#241b3a"
    sh = Sector(radius=1.7, angle=PI, start_angle=0, fill_color=dark, fill_opacity=1, stroke_width=0)
    sh.stretch_to_fit_height(1.5).move_to([0, -1.0, 0])
    neck = Rectangle(width=0.4, height=0.35, fill_color="#2a2236", fill_opacity=1, stroke_width=0).move_to([0, -0.2, 0])
    head = disc(0.68, hair).move_to([0, 0.35, 0])
    bun = disc(0.27, hair).move_to([0.2, 1.08, 0])
    band = Arc(radius=0.68, start_angle=PI * 0.2, angle=PI * 0.6, stroke_color=PURPLE, stroke_width=5).move_to([0, 0.85, 0]).shift(DOWN * 0.0)
    g = VGroup(sh, neck, head, bun, band)
    rim = VGroup(*[m.copy().set_fill(opacity=0).set_stroke("#7aa2ff", width=3, opacity=0.45) for m in (sh, head, bun)])
    g.add(rim)
    return g.scale(scale)


def friend_group(colors=(PINK, ORANGE, BLUE, GREEN), r=0.34):
    """Four friends side by side, heads slightly different, for the velvet-rope picture."""
    g = VGroup()
    skins = ["#f0c4a0", "#d9a07a", "#b8805e", "#f3cfb3"]
    hairs = ["#3a2a1e", "#1c1a26", "#5b3a22", "#c58a3c"]
    for i, c in enumerate(colors):
        b = bust(c, r, skins[i % 4], hairs[i % 4], face=True)
        b.shift(RIGHT * i * r * 2.1 + UP * (0.06 if i % 2 else 0.0))
        g.add(b)
    return g.center()
