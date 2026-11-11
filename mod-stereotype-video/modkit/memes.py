# Written by Claude Sonnet 5.5
"""Three ORIGINAL meme-style images drawn from shapes, for Scene 3 reason 4.

All characters and names are invented. Each image is 7.2 x 4.6 Manim units.
"""
import numpy as np
from manim import *

from .characters import avatar, cartoon_mod
from .icons import starburst
from .props import hammer
from .theme import *

W, H = 7.2, 4.6


def _frame(bg):
    return rrect(W, H, 0.14, bg, stroke="#f1f1f8", sw=6)


def _caption(text, size, y, color=WHITE):
    """Meme caption: heavy white text with a thick dark outline."""
    t = T(text, size, color, "HEAVY")
    t.set_stroke("#05060a", width=9, background=True)
    return t.move_to([0, y, 0])


def meme_hammer():
    """A cartoon mod swinging a giant hammer."""
    bg = _frame("#ff9d5c")
    sky = Rectangle(width=W - 0.12, height=2.0, fill_color="#ffcf8a", fill_opacity=1, stroke_width=0).move_to([0, 1.2, 0])
    ground = Rectangle(width=W - 0.12, height=1.15, fill_color="#5b3f9e", fill_opacity=1, stroke_width=0).move_to([0, -1.9, 0])
    sun = disc(0.55, "#fff1b8").move_to([2.3, 1.4, 0])
    mod = cartoon_mod(1.25).move_to([-1.5, -0.65, 0])
    hand = np.array([-0.55, 0.35, 0.0])
    arm = rstroke(Line([-0.8, -0.7, 0], hand), PURPLE_DEEP, 38)
    fist = disc(0.2, SKIN).move_to(hand)
    ham = hammer(2.5)
    ham.rotate(np.radians(-32), about_point=ham.get_bottom())
    ham.shift(hand - (ham.get_bottom() + np.array([0, 0.05, 0])))
    burst = starburst(1.5, YELLOW).move_to([2.0, -0.95, 0])
    bonk = T("BONK", 64, RED, "HEAVY").set_stroke("#05060a", width=8, background=True).rotate(np.radians(-12)).move_to(burst.get_center())
    lines = VGroup(*[Line([2.4 + 0.2 * i, -0.2 - 0.0 * i, 0], [2.9 + 0.25 * i, -0.45 - 0.35 * i, 0]).set_stroke("#05060a", width=5)
                     for i in range(3)])
    top = _caption("NEW MOD", 62, 1.82).shift(LEFT * 1.6)
    bottom = _caption("FIRST DAY ON THE JOB", 46, -2.0)
    return VGroup(bg, sky, ground, sun, mod, arm, fist, ham, burst, bonk, lines, top, bottom)


def meme_grass():
    """The 'touch grass' joke: a bright meadow and a tired mod being told to step outside."""
    bg = _frame("#8fd3ff")
    field = Rectangle(width=W - 0.12, height=1.9, fill_color="#3fbf5f", fill_opacity=1, stroke_width=0).move_to([0, -1.75, 0])
    hill = Ellipse(width=4.8, height=1.6, fill_color="#34a853", fill_opacity=1, stroke_width=0).move_to([-0.9, -1.0, 0])
    sun = VGroup(*[Line(0.62 * np.array([np.cos(a), np.sin(a), 0]), 0.9 * np.array([np.cos(a), np.sin(a), 0])).set_stroke("#ffd23f", width=7)
                   for a in np.arange(0, TAU, TAU / 12)], disc(0.52, "#ffd23f")).move_to([2.55, 1.25, 0])
    clouds = VGroup(*[VGroup(*[disc(r, WHITE, 0.95).shift(RIGHT * dx) for r, dx in ((0.3, 0), (0.42, 0.4), (0.3, 0.85))]).move_to(p)
                      for p in ([-2.4, 1.2, 0], [0.4, 0.55, 0])])
    tufts = VGroup(*[Polygon([x - 0.1, -2.3, 0], [x + 0.1, -2.3, 0], [x, -1.95, 0], fill_color="#1f8a3f", fill_opacity=1, stroke_width=0)
                     for x in np.arange(-3.2, 3.3, 0.55)])
    mod = cartoon_mod(1.0, with_crown=True).move_to([-0.3, -1.0, 0])
    arrow = VGroup(rstroke(Line([0.9, -0.35, 0], [1.9, -1.2, 0]), RED, 9),
                   Polygon([1.9, -1.2, 0], [1.55, -1.05, 0], [1.75, -0.8, 0], fill_color=RED, fill_opacity=1, stroke_width=0))
    top = _caption("GO TOUCH GRASS", 62, 1.85)
    bottom = _caption("(a mod, 3 a.m., after the raid)", 34, -2.05)
    return VGroup(bg, field, hill, sun, clouds, tufts, mod, arrow, top, bottom)


def meme_screenshot():
    """A parody 'mod abuse' screenshot with invented names, stamped PARODY."""
    bg = _frame("#171a28")
    head = Rectangle(width=W - 0.12, height=0.62, fill_color="#1f2336", fill_opacity=1, stroke_width=0).move_to([0, H / 2 - 0.37, 0])
    title = T("# general", 28, TEXT, "BOLD").move_to([-W / 2 + 0.4, H / 2 - 0.37, 0], aligned_edge=LEFT)
    rows = [("NewKid", BLUE, "hi everyone!", TEXT), ("Gavelrix | Mod", PURPLE, "Wrong greeting. Banned.", TEXT),
            ("NewKid", BLUE, "i just said hi??", TEXT), ("Gavelrix | Mod", PURPLE, "Arguing. Banned.", TEXT)]
    parts = VGroup()
    y = H / 2 - 1.2
    for name, col, msg, tc in rows:
        av = avatar(name[0], col, 0.2).move_to([-W / 2 + 0.55, y - 0.02, 0])
        nm = T(name, 24, col, "SEMIBOLD").move_to([-W / 2 + 0.95, y + 0.17, 0], aligned_edge=LEFT)
        tx = T(msg, 28, tc, "MEDIUM").move_to([-W / 2 + 0.95, y - 0.2, 0], aligned_edge=LEFT)
        parts.add(av, nm, tx)
        y -= 0.88
    circle = Ellipse(width=5.2, height=0.95, stroke_color=RED, stroke_width=6, fill_opacity=0).move_to([-0.55, H / 2 - 1.2 - 0.88 - 0.02, 0])
    stamp = VGroup(rrect(2.1, 0.7, 0.1, INK, opacity=0.0, stroke=RED, sw=6),
                   T("PARODY", 44, RED, "HEAVY")).rotate(np.radians(-10)).move_to([W / 2 - 1.5, -H / 2 + 0.75, 0])
    stamp[1].move_to(stamp[0].get_center())
    return VGroup(bg, head, title, parts, circle, stamp)
