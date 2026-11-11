# Written by Claude Sonnet 5.5
"""Original vector props: phone, hammer, door, velvet rope, calendar, cards, monitor, bedroom desk items."""
import numpy as np
from manim import *

from .icons import crown, lock
from .theme import *


def phone(height=3.4, screen=HEADER, lit=False):
    """Phone seen from above. Returns a VGroup with .screen for the lit display."""
    w = height * 0.5
    body = rrect(w, height, 0.18 * w, "#222638", stroke="#3a4060", sw=3)
    scr = rrect(w * 0.9, height * 0.93, 0.14 * w, screen)
    notch = rrect(w * 0.25, height * 0.018, 0.01, "#10121b").move_to(scr.get_top() + DOWN * 0.06)
    g = VGroup(body, scr, notch)
    g.screen = scr
    return g


def hammer(size=2.2, handle=WOOD, head="#9aa3b5", head_dark="#6b7388"):
    """Big mallet, handle down, head up. Pivot for swings: get_bottom()."""
    stick = rrect(0.2, 1.5, 0.09, handle).move_to([0, -0.5, 0])
    base = rrect(0.26, 0.2, 0.08, WOOD_DARK).move_to([0, -1.2, 0])
    h = rrect(1.25, 0.72, 0.16, head).move_to([0, 0.5, 0])
    cap_l = rrect(0.2, 0.72, 0.1, head_dark).move_to([-0.55, 0.5, 0])
    cap_r = rrect(0.2, 0.72, 0.1, head_dark).move_to([0.55, 0.5, 0])
    shine = rrect(0.7, 0.08, 0.04, WHITE).move_to([0, 0.72, 0]).set_opacity(0.4)
    return VGroup(stick, base, h, cap_l, cap_r, shine).scale_to_fit_height(size)


def door(height=3.2, locked=True):
    w = height * 0.58
    frame = rrect(w + 0.2, height + 0.15, 0.08, "#2c3250")
    leaf = rrect(w, height, 0.05, "#4a3a6a", stroke="#6a5a90", sw=3)
    p1 = rrect(w * 0.7, height * 0.34, 0.05, "#3c2f5a").move_to(leaf.get_center() + UP * height * 0.2)
    p2 = rrect(w * 0.7, height * 0.34, 0.05, "#3c2f5a").move_to(leaf.get_center() + DOWN * height * 0.2)
    knob = disc(0.07, GOLD).move_to(leaf.get_center() + RIGHT * w * 0.32)
    g = VGroup(frame, leaf, p1, p2, knob)
    g.leaf = leaf
    return g


def velvet_rope(width=4.6, post_h=1.5, color=RED_DEEP):
    """Two brass posts with a sagging velvet rope."""
    posts = VGroup()
    for x in (-width / 2, width / 2):
        base = rrect(0.5, 0.12, 0.05, "#b88a2a").move_to([x, -post_h / 2, 0])
        stem = rrect(0.1, post_h, 0.04, GOLD).move_to([x, 0, 0])
        ball = disc(0.14, GOLD).move_to([x, post_h / 2 + 0.06, 0])
        posts.add(base, stem, ball)
    a, b = np.array([-width / 2, post_h * 0.38, 0]), np.array([width / 2, post_h * 0.38, 0])
    rope = VMobject()
    rope.start_new_path(a)
    rope.add_cubic_bezier_curve_to(a + np.array([0.3, -0.62, 0]), b + np.array([-0.3, -0.62, 0]), b)
    rstroke(rope, color, 14)
    rope.set_fill(opacity=0)
    hi = rope.copy().set_stroke("#ff7a8a", width=4, opacity=0.6).shift(UP * 0.04)
    return VGroup(posts, rope, hi)


def calendar_panel(width=9.0, height=5.2, accent=PURPLE_DEEP):
    """Month grid: returns VGroup with .cells (list of day-cell rectangles) and .nums (Text list)."""
    panel = rrect(width, height, 0.25, "#1a1d2c", stroke=LINE, sw=3)
    head_h = 0.75
    head = rrect(width, head_h, 0.25, accent).move_to(panel.get_top() + DOWN * head_h / 2)
    head_fix = Rectangle(width=width, height=head_h / 2, fill_color=accent, fill_opacity=1, stroke_width=0).move_to(head.get_bottom() + UP * head_h / 4)
    rings = VGroup(*[rrect(0.14, 0.4, 0.07, "#d8d2ff").move_to(panel.get_top() + np.array([x, 0.02, 0])) for x in (-width * 0.3, width * 0.3)])
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    pad = 0.35
    cw = (width - 2 * pad) / 7
    ch = (height - head_h - 0.9) / 5
    labels = VGroup()
    cells, nums = [], []
    x0 = panel.get_left()[0] + pad + cw / 2
    for i, d in enumerate(days):
        labels.add(T(d, 22, MUTED, "SEMIBOLD").move_to([x0 + i * cw, panel.get_top()[1] - head_h - 0.3, 0]))
    y0 = panel.get_top()[1] - head_h - 0.7 - ch / 2
    for k in range(35):
        r, c = divmod(k, 7)
        cell = rrect(cw - 0.1, ch - 0.1, 0.08, "#222638").move_to([x0 + c * cw, y0 - r * ch, 0])
        cells.append(cell)
        if k < 30:
            n = T(str(k + 1), 24, DIM, "MEDIUM").move_to(cell.get_center())
            nums.append(n)
    g = VGroup(panel, head, head_fix, rings, labels, VGroup(*cells), VGroup(*nums))
    g.cells, g.nums, g.panel = cells, nums, panel
    return g


def card_back(num, w=2.2, h=3.1, color="#4a33a0"):
    """Face-down card with its number on the back (the script asks for numbers 1 to 4)."""
    base = rrect(w, h, 0.2, color, stroke="#8f78ff", sw=4)
    inner = rrect(w - 0.3, h - 0.3, 0.14, "#3a2788", stroke="#6a52d4", sw=2)
    badge = disc(0.5, "#fff4d6")
    n = T(str(num), 64, "#3a2788", "HEAVY").move_to(badge.get_center())
    mark = crown(0.5, "#8f78ff", "#6a52d4", ("#6a52d4",) * 3).move_to(inner.get_top() + DOWN * 0.55)
    mark2 = mark.copy().rotate(PI).move_to(inner.get_bottom() + UP * 0.55)
    g = VGroup(base, inner, mark, mark2, badge, n)
    return g


def card_face(num, title, icon, w=2.2, h=3.1, accent=PURPLE):
    """Face-up card: number, title, icon."""
    base = rrect(w, h, 0.2, "#f4f1ff", stroke=accent, sw=5)
    strip = rrect(w - 0.3, 0.12, 0.05, accent).move_to(base.get_top() + DOWN * 0.28)
    n = T(str(num), 52, PURPLE_DEEP, "HEAVY").move_to(base.get_top() + DOWN * 0.78)
    ic = icon.copy().scale_to_fit_height(0.78).move_to(base.get_center() + UP * 0.02)
    t = T(wrap(title, 24, w - 0.4, "BOLD"), 24, "#2a2140", "BOLD", line_spacing=0.9)
    fit_width(t, w - 0.35)
    t.move_to(base.get_bottom() + UP * 0.62)
    return VGroup(base, strip, n, ic, t)


def monitor(width=10.6, height=5.9):
    """Dark monitor frame; returns VGroup with .screen_rect (inner area) for content."""
    outer = rrect(width, height, 0.22, "#1d2132", stroke="#33395a", sw=3)
    screen = rrect(width - 0.35, height - 0.35, 0.12, PANEL)
    stand = Polygon([-0.5, 0, 0], [0.5, 0, 0], [0.8, -0.9, 0], [-0.8, -0.9, 0], fill_color="#1a1d2c", fill_opacity=1, stroke_width=0)
    stand.move_to(outer.get_bottom() + DOWN * 0.45)
    foot = rrect(2.4, 0.16, 0.08, "#222640").move_to(stand.get_bottom() + DOWN * 0.04)
    g = VGroup(stand, foot, outer, screen)
    g.screen_rect = screen
    return g


def mug(size=0.8, color="#d9d3ff"):
    cup = rrect(size, size * 0.9, size * 0.18, color)
    handle = Arc(radius=size * 0.25, start_angle=-PI / 2, angle=PI, stroke_color=color, stroke_width=8).move_to(cup.get_right() + RIGHT * size * 0.1)
    liquid = rrect(size * 0.86, size * 0.16, size * 0.06, "#4b3524").move_to(cup.get_top() + DOWN * size * 0.12)
    return VGroup(handle, cup, liquid)


def desk_lamp(size=1.4):
    base = rrect(size * 0.5, 0.1, 0.05, "#2a2f48").move_to([0, -size / 2, 0])
    arm1 = rstroke(Line([0, -size / 2, 0], [size * 0.22, 0.05, 0]), "#3a4060", 8)
    arm2 = rstroke(Line([size * 0.22, 0.05, 0], [-size * 0.1, size * 0.45, 0]), "#3a4060", 8)
    shade = Polygon([-size * 0.32, size * 0.42, 0], [size * 0.1, size * 0.5, 0], [size * 0.0, size * 0.22, 0], [-size * 0.38, size * 0.3, 0],
                    fill_color="#2f3556", fill_opacity=1, stroke_width=0)
    return VGroup(base, arm1, arm2, shade)


def window_night(w=3.0, h=3.6):
    """Night window with a moon and stars (flat shapes)."""
    frame = rrect(w + 0.3, h + 0.3, 0.1, "#1d2236")
    sky = rrect(w, h, 0.05, "#101a3a")
    moon = VGroup(disc(0.34, "#f3f1d8"), disc(0.3, "#101a3a").shift(RIGHT * 0.14 + UP * 0.07)).move_to(sky.get_center() + np.array([0.5, 0.8, 0]))
    stars = VGroup(*[disc(0.025, WHITE, 0.8).move_to(sky.get_center() + np.array(p)) for p in
                     [(-0.9, 1.1, 0), (-0.3, 0.5, 0), (0.1, 1.3, 0), (-1.1, 0.1, 0), (0.9, -0.2, 0), (-0.5, -0.9, 0), (0.4, -1.1, 0)]])
    bars = VGroup(Line(sky.get_top(), sky.get_bottom()), Line(sky.get_left(), sky.get_right())).set_stroke("#1d2236", width=10)
    return VGroup(frame, sky, moon, stars, bars)


# ---- speech bubbles and the four-card fan (shared by scenes 2 and 3) -------------------------------
FAN_PIVOT = np.array([0.0, -4.6, 0.0])
FAN_RADIUS = 5.4
FAN_ANGLES = (24.0, 8.0, -8.0, -24.0)   # positive = counter-clockwise, so card 1 is on the left


def speech_bubble(text, size=30, color=TEXT, fill="#232845", stroke=PURPLE, max_w=3.6, pad=0.26, tail=-1):
    """Rounded bubble with a small tail (tail=-1 bottom-left, 1 bottom-right, 0 none)."""
    t = T(wrap(text, size, max_w, "MEDIUM"), size, color, "MEDIUM")
    box = rrect(t.width + 2 * pad, t.height + 2 * pad, 0.24, fill, stroke=stroke, sw=3)
    t.move_to(box.get_center())
    parts = [box, t]
    if tail:
        x = box.get_center()[0] + tail * (box.width / 2 - 0.55)
        y = box.get_bottom()[1]
        tri = Polygon([x - 0.14, y + 0.02, 0], [x + 0.14, y + 0.02, 0], [x - tail * 0.18, y - 0.26, 0],
                      fill_color=fill, fill_opacity=1, stroke_width=0)
        edge = VMobject()
        edge.set_points_as_corners([np.array([x - 0.14, y, 0]), np.array([x - tail * 0.18, y - 0.26, 0]), np.array([x + 0.14, y, 0])])
        edge.set_stroke(stroke, width=3)
        parts = [edge, tri, box, t]
        cover = Line([x - 0.12, y, 0], [x + 0.12, y, 0]).set_stroke(fill, width=5)
        parts.insert(3, cover)
    return VGroup(*parts)


def thought_bubble(text, size=30, color=TEXT, fill="#232845", stroke=MUTED, max_w=4.4, pad=0.3, tail="down-left"):
    """Thought bubble: rounded box with two trailing circles (tail "down-left", "left" or "right")."""
    t = T(wrap(text, size, max_w, "MEDIUM"), size, color, "MEDIUM")
    box = rrect(t.width + 2 * pad, t.height + 2 * pad, 0.45, fill, stroke=stroke, sw=3)
    t.move_to(box.get_center())
    if tail == "left":
        x0, y0 = box.get_left()[0], box.get_center()[1] - 0.1
        c1 = Circle(radius=0.12, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to([x0 - 0.22, y0, 0])
        c2 = Circle(radius=0.07, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to([x0 - 0.48, y0 - 0.1, 0])
    elif tail == "right":
        x0, y0 = box.get_right()[0], box.get_center()[1] - 0.1
        c1 = Circle(radius=0.12, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to([x0 + 0.22, y0, 0])
        c2 = Circle(radius=0.07, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to([x0 + 0.48, y0 - 0.1, 0])
    else:
        x0, y0 = box.get_left()[0] + 0.6, box.get_bottom()[1]
        c1 = Circle(radius=0.12, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to([x0, y0 - 0.2, 0])
        c2 = Circle(radius=0.07, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to([x0 - 0.2, y0 - 0.42, 0])
    return VGroup(c2, c1, box, t)


def tab_chip(k, title):
    """Numbered title pill used at the top-left of Scenes 3 and 4. Anchored at x = -6.7, y = 3.45."""
    label = T(title, 30, WHITE, "BOLD")
    pill = rrect(label.width + 1.2, 0.64, 0.32, PURPLE_DEEP)
    badge = disc(0.24, "#fff4d6").move_to(pill.get_left() + RIGHT * 0.42)
    num = T(str(k), 28, "#3a2788", "HEAVY").move_to(badge.get_center())
    label.move_to(badge.get_right() + RIGHT * (0.2 + label.width / 2))
    return VGroup(pill, badge, num, label).move_to([-6.7 + pill.width / 2, 3.45, 0])


def fan_angles(n):
    """Fan angles for n cards, 16 degrees apart, leftmost card first (positive = counter-clockwise)."""
    return [(n - 1) / 2 * 16.0 - i * 16.0 for i in range(n)]


def make_fan(fanned=True, w=2.3, h=3.2, numbers=(1, 2, 3, 4)):
    """Numbered face-down cards. fanned=False stacks them, fanned=True spreads them in an arc."""
    cards = VGroup(*[card_back(n, w, h) for n in numbers])
    for c in cards:
        c.move_to(FAN_PIVOT + UP * FAN_RADIUS)
    if fanned:
        for c, a in zip(cards, fan_angles(len(numbers))):
            c.rotate(np.radians(a), about_point=FAN_PIVOT)
    return cards
