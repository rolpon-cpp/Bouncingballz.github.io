# Written by Claude Sonnet 5.5
"""Original vector icons drawn with Manim primitives. Each returns a VGroup centred at the origin."""
import numpy as np
from manim import *

from .theme import *


def _poly(points, color, **kw):
    return Polygon(*[np.array([x, y, 0.0]) for x, y in points], color=color, fill_opacity=1, stroke_width=0, **kw)


def crown(width=1.0, color=GOLD, dark=GOLD_DARK, gems=(RED, BLUE, GREEN)):
    body = _poly([(-0.5, -0.22), (-0.5, 0.22), (-0.22, -0.04), (0.0, 0.3), (0.22, -0.04), (0.5, 0.22), (0.5, -0.22)],
                 color).round_corners(0.035)
    band = rrect(1.0, 0.16, 0.05, dark).move_to([0, -0.17, 0])
    tips = VGroup(*[disc(0.06, c).move_to([x, y, 0]) for (x, y), c in zip([(-0.5, 0.25), (0.0, 0.33), (0.5, 0.25)], gems)])
    shine = _poly([(-0.42, -0.05), (-0.3, 0.1), (-0.26, -0.02)], "#fff2b0").set_opacity(0.6)
    return VGroup(body, band, tips, shine).scale_to_fit_width(width)


def gavel(size=1.6, wood=WOOD, dark=WOOD_DARK, brass="#e8b94a"):
    """Gavel standing upright (handle down). Pivot for swings: get_bottom()."""
    handle = rrect(0.2, 1.3, 0.09, wood).move_to([0, -0.25, 0])
    grip = rrect(0.23, 0.34, 0.08, dark).move_to([0, -0.66, 0])
    head = rrect(1.0, 0.52, 0.13, wood).move_to([0, 0.5, 0])
    bands = VGroup(*[Rectangle(width=0.1, height=0.52, fill_color=brass, fill_opacity=1, stroke_width=0).move_to([x, 0.5, 0])
                     for x in (-0.36, 0.36)])
    shade = rrect(1.0, 0.16, 0.08, dark).move_to([0, 0.34, 0]).set_opacity(0.55)
    shine = rrect(0.5, 0.07, 0.035, "#ffd9a0").move_to([0, 0.64, 0]).set_opacity(0.6)
    return VGroup(handle, grip, head, bands, shade, shine).scale_to_fit_height(size)


def shield(size=1.0, color=BLUE, check=True):
    s = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    s.start_new_path(np.array([-0.45, 0.5, 0]))
    s.add_line_to(np.array([0.45, 0.5, 0]))
    s.add_line_to(np.array([0.45, 0.05, 0]))
    s.add_cubic_bezier_curve_to(np.array([0.45, -0.3, 0]), np.array([0.22, -0.5, 0]), np.array([0, -0.62, 0]))
    s.add_cubic_bezier_curve_to(np.array([-0.22, -0.5, 0]), np.array([-0.45, -0.3, 0]), np.array([-0.45, 0.05, 0]))
    s.close_path()
    half = VMobject(fill_color=WHITE, fill_opacity=0.14, stroke_width=0)
    half.start_new_path(np.array([-0.45, 0.5, 0]))
    half.add_line_to(np.array([0, 0.5, 0]))
    half.add_line_to(np.array([0, -0.62, 0]))
    half.add_cubic_bezier_curve_to(np.array([-0.22, -0.5, 0]), np.array([-0.45, -0.3, 0]), np.array([-0.45, 0.05, 0]))
    half.close_path()
    g = VGroup(s, half)
    if check:
        g.add(checkmark(0.42, WHITE, 7).move_to([0, 0.02, 0]))
    return g.scale_to_fit_height(size)


def checkmark(size=0.5, color=GREEN, width=6):
    c = VMobject()
    c.set_points_as_corners([np.array([-0.5, -0.02, 0]), np.array([-0.15, -0.38, 0]), np.array([0.5, 0.36, 0])])
    rstroke(c, color, width)
    c.set_fill(opacity=0)
    c.joint_type = LineJointType.ROUND
    return VGroup(c).scale_to_fit_width(size)


def cross(size=0.5, color=RED, width=6):
    a = Line([-0.4, 0.4, 0], [0.4, -0.4, 0])
    b = Line([-0.4, -0.4, 0], [0.4, 0.4, 0])
    g = rstroke(VGroup(a, b), color, width)
    return g.scale_to_fit_width(size)


def clock(size=1.0, color=TEAL, face=PANEL_DARK):
    ring = Circle(radius=0.5, fill_color=face, fill_opacity=1, stroke_color=color, stroke_width=7)
    ticks = VGroup(*[Line(0.38 * np.array([np.cos(a), np.sin(a), 0]), 0.44 * np.array([np.cos(a), np.sin(a), 0]))
                     .set_stroke(MUTED, width=3) for a in np.arange(0, TAU, TAU / 12)])
    h = rstroke(Line(ORIGIN, [0, 0.28, 0]), TEXT, 6)
    m = rstroke(Line(ORIGIN, [0.2, -0.1, 0]), TEXT, 5)
    pin = disc(0.04, color)
    g = VGroup(ring, ticks, h, m, pin)
    g.hand_hour, g.hand_min = h, m
    return g.scale_to_fit_height(size)


def bell(size=1.0, color=ORANGE, dark="#d9731a"):
    body = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    body.start_new_path(np.array([-0.42, -0.25, 0]))
    body.add_cubic_bezier_curve_to(np.array([-0.42, 0.2, 0]), np.array([-0.3, 0.45, 0]), np.array([0, 0.45, 0]))
    body.add_cubic_bezier_curve_to(np.array([0.3, 0.45, 0]), np.array([0.42, 0.2, 0]), np.array([0.42, -0.25, 0]))
    body.add_line_to(np.array([0.58, -0.33, 0]))
    body.add_line_to(np.array([-0.58, -0.33, 0]))
    body.close_path()
    lip = rrect(1.16, 0.09, 0.04, dark).move_to([0, -0.33, 0])
    knob = disc(0.07, dark).move_to([0, 0.5, 0])
    clap = disc(0.11, dark).move_to([0, -0.46, 0])
    shine = rrect(0.08, 0.38, 0.04, "#ffe0b8").move_to([-0.2, 0.08, 0]).set_opacity(0.55)
    g = VGroup(knob, body, shine, lip, clap)
    g.clapper = clap
    return g.scale_to_fit_height(size)


def warning(size=1.0, color=YELLOW):
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.55).round_corners(0.09)
    tri.stretch_to_fit_height(0.85)
    bar = rrect(0.1, 0.3, 0.05, INK).move_to(tri.get_center() + DOWN * 0.04 + UP * 0.05)
    dot = disc(0.06, INK).move_to(tri.get_center() + DOWN * 0.27)
    return VGroup(tri, bar, dot).scale_to_fit_height(size)


def lock(size=1.0, color=GOLD, locked=True):
    body = rrect(0.8, 0.6, 0.1, color).move_to([0, -0.1, 0])
    sh = Arc(radius=0.24, start_angle=0, angle=PI, stroke_color=color, stroke_width=10).move_to([0, 0.28, 0])
    legs = VGroup(Line([-0.24, 0.28, 0], [-0.24, 0.12, 0]), Line([0.24, 0.28, 0], [0.24, 0.12, 0]))
    legs.set_stroke(color, width=10)
    if not locked:
        sh.shift(RIGHT * 0.18 + UP * 0.1)
        legs[0].shift(UP * 0.1 + RIGHT * 0.0)
        legs.shift(RIGHT * 0.0)
    key = VGroup(disc(0.07, INK).move_to([0, -0.06, 0]), _poly([(-0.035, -0.08), (0.035, -0.08), (0.05, -0.26), (-0.05, -0.26)], INK))
    return VGroup(sh, legs, body, key).scale_to_fit_height(size)


def heart(size=1.0, color=PURPLE):
    f = lambda t: np.array([16 * np.sin(t) ** 3,
                            13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0]) / 34.0
    h = ParametricFunction(f, t_range=[0, TAU], fill_color=color, fill_opacity=1, stroke_width=0)
    sh = Ellipse(width=0.16, height=0.26, fill_color=WHITE, fill_opacity=0.45, stroke_width=0).rotate(0.5).move_to(h.get_center() + np.array([-0.2, 0.17, 0]))
    return VGroup(h, sh).scale_to_fit_height(size)


def eye(size=0.4, look=(0.0, 0.0)):
    w = Ellipse(width=1.0, height=0.7, fill_color=WHITE, fill_opacity=1, stroke_width=0)
    p = disc(0.18, "#1a1d2b").move_to([0.2 * look[0], 0.12 * look[1], 0])
    s = disc(0.05, WHITE).move_to(p.get_center() + np.array([0.06, 0.07, 0]))
    return VGroup(w, p, s).scale_to_fit_width(size)


def camera_icon(size=1.0, color=TEXT):
    body = rrect(1.0, 0.7, 0.12, color)
    top = rrect(0.4, 0.14, 0.05, color).move_to([-0.2, 0.4, 0])
    lens = disc(0.24, PANEL_DARK).move_to([0, -0.02, 0])
    lens2 = disc(0.14, BLUE).move_to([0, -0.02, 0])
    return VGroup(top, body, lens, lens2).scale_to_fit_width(size)


def speaker(size=0.4, color=MUTED):
    cone = _poly([(-0.5, -0.15), (-0.25, -0.15), (0.05, -0.4), (0.05, 0.4), (-0.25, 0.15), (-0.5, 0.15)], color)
    arcs = VGroup(*[Arc(radius=r, start_angle=-PI / 3, angle=2 * PI / 3, stroke_color=color, stroke_width=4).shift(RIGHT * 0.05)
                    for r in (0.22, 0.4)])
    return VGroup(cone, arcs).scale_to_fit_height(size)


def cat_logo(radius=0.3, bg=ORANGE, fg="#fff4e4"):
    base = disc(radius, bg)
    s = radius / 0.5
    ears = VGroup(_poly([(-0.34, 0.06), (-0.3, 0.38), (-0.07, 0.2)], fg), _poly([(0.34, 0.06), (0.3, 0.38), (0.07, 0.2)], fg))
    face = Ellipse(width=0.74, height=0.6, fill_color=fg, fill_opacity=1, stroke_width=0).move_to([0, -0.04, 0])
    eyes = VGroup(disc(0.045, INK).move_to([-0.15, 0.0, 0]), disc(0.045, INK).move_to([0.15, 0.0, 0]))
    nose = _poly([(-0.04, -0.07), (0.04, -0.07), (0, -0.12)], PINK)
    whisk = VGroup(*[Line([sx * 0.12, -0.1 + dy, 0], [sx * 0.36, -0.1 + dy * 2.2, 0]).set_stroke("#b9a58f", width=2)
                     for sx in (-1, 1) for dy in (0.02, -0.03)])
    cat = VGroup(ears, face, eyes, nose, whisk).scale(s * 0.78)
    return VGroup(base, cat)


def starburst(size=1.0, color=YELLOW, n=11):
    outer = Star(n=n, outer_radius=0.5, inner_radius=0.3, fill_color=color, fill_opacity=1, stroke_width=0)
    inner = Star(n=n, outer_radius=0.36, inner_radius=0.22, fill_color=WHITE, fill_opacity=0.5, stroke_width=0)
    return VGroup(outer, inner).scale_to_fit_width(size)


def dots3(radius=0.05, color=MUTED, gap=0.17):
    return VGroup(*[disc(radius, color).move_to([i * gap, 0, 0]) for i in (-1, 0, 1)])


def chat_icon(size=0.6, color=BLUE):
    """Speech-bubble icon with three dots."""
    box = rrect(1.0, 0.7, 0.22, color)
    tail = Polygon([-0.3, -0.3, 0], [-0.04, -0.3, 0], [-0.34, -0.58, 0], fill_color=color, fill_opacity=1, stroke_width=0)
    dots = dots3(0.06, WHITE, 0.24).move_to(box.get_center())
    return VGroup(tail, box, dots).scale_to_fit_width(size)
