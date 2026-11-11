# Written by Claude Sonnet 5.5
"""Colors, fonts and text helpers shared by all scenes. The palette is original (not any real app's)."""
import numpy as np
from manim import *
from manim.utils.rate_functions import ease_in_back, ease_in_out_back, ease_out_back, ease_out_bounce, ease_out_elastic
from PIL import ImageFont

# ---- palette ---------------------------------------------------------------------------------
INK = "#0b0d14"          # page background
PANEL_DARK = "#10121b"   # side panels
PANEL = "#161925"        # main chat area
HEADER = "#1c2031"       # header strips and input bar
LINE = "#2a2f45"         # hairlines
TEXT = "#e8eaf4"
MUTED = "#8d93ab"
DIM = "#5d6380"
PURPLE = "#b794ff"       # moderator name colour
PURPLE_DEEP = "#6d4bd8"
GOLD = "#ffcf33"
GOLD_DARK = "#d39a00"
YELLOW = "#ffd23f"
RED = "#ff4d5e"
RED_DEEP = "#c81e3a"
GREEN = "#39d98a"
TEAL = "#2dd4bf"
PINK = "#ff7a9c"
ORANGE = "#ff9f45"
BLUE = "#5aa9ff"
SKIN = "#e9b995"
SKIN_DARK = "#c98f6b"
WOOD = "#c07a3a"
WOOD_DARK = "#8e5424"

# Scene 1 ends and Scene 2 begins with Tyler's name at exactly this place and size (seamless cut).
HANDOFF_POS = np.array([0.0, 2.35, 0.0])
HANDOFF_PX = 72

FONT = "Inter"
PX = 1.0 / 135.0         # one pixel at 1080p, in Manim units (frame height 8 = 1080 px)
PX_PER_FS = 1.877        # measured: Inter em in pixels per Manim font_size unit at 1080p

_FONT_FILES = {
    "NORMAL": "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
    "MEDIUM": "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
    "SEMIBOLD": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    "BOLD": "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "HEAVY": "/usr/share/fonts/opentype/inter/Inter-Black.otf",
}
_pil_cache = {}


def px(n: float) -> float:
    """Pixels (at 1080p) to Manim units."""
    return n * PX


def T(text, size=34, color=TEXT, weight="NORMAL", t2c=None, line_spacing=-1, font=FONT, **kw):
    """Text in Inter. `size` is the em height in pixels at 1080p (34 is body text)."""
    args = dict(font=font, font_size=size / PX_PER_FS, color=color, weight=weight)
    if t2c:
        args["t2c"] = t2c
    if line_spacing > 0:
        args["line_spacing"] = line_spacing
    return Text(text, **args, **kw)


def text_width(text: str, size: float, weight="NORMAL") -> float:
    """Width in Manim units of a one-line string, measured with the real font (fast, no Pango)."""
    key = (weight, round(size * 4))
    if key not in _pil_cache:
        path = _FONT_FILES.get(weight, _FONT_FILES["NORMAL"])
        _pil_cache[key] = ImageFont.truetype(path, int(round(size * 4)))
    return _pil_cache[key].getlength(text) / 4.0 * PX


def wrap(text: str, size: float, max_units: float, weight="NORMAL") -> str:
    """Greedy word wrap using measured widths; returns the text with newlines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if cur and text_width(trial, size, weight) > max_units:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    lines.append(cur)
    return "\n".join(lines)


def fit_width(mob, max_w):
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


def rstroke(mob, color, width, opacity=1.0):
    """Stroke with round caps and joins on every part (Manim keeps cap style per VMobject, not per group)."""
    for m in mob.get_family():
        m.set_stroke(color, width, opacity, family=False)
        m.cap_style = CapStyleType.ROUND
        m.joint_type = LineJointType.ROUND
    return mob


def rrect(w, h, r=0.12, fill=PANEL, stroke=None, sw=0, opacity=1.0, **kw):
    """Rounded rectangle with a fill and optional hairline stroke."""
    m = RoundedRectangle(width=w, height=h, corner_radius=min(r, w / 2, h / 2), fill_color=fill,
                         fill_opacity=opacity, stroke_width=sw if stroke else 0, **kw)
    if stroke:
        m.set_stroke(stroke, width=sw)
    return m


def disc(r, fill, opacity=1.0, stroke=None, sw=0):
    c = Circle(radius=r, fill_color=fill, fill_opacity=opacity, stroke_width=0)
    if stroke:
        c.set_stroke(stroke, width=sw)
    return c


def glow_rect(w, h, r, color, layers=6, spread=0.07, peak=0.16):
    """Soft glow built from stacked translucent rounded rectangles (no blur filter in Manim)."""
    g = VGroup()
    for i in range(layers, 0, -1):
        g.add(RoundedRectangle(width=w + 2 * spread * i, height=h + 2 * spread * i, corner_radius=r + spread * i,
                               fill_color=color, fill_opacity=peak * (1 - i / (layers + 1)), stroke_width=0))
    return g


def glow_disc(radius, color, layers=6, spread=0.08, peak=0.18):
    g = VGroup()
    for i in range(layers, 0, -1):
        g.add(Circle(radius=radius + spread * i, fill_color=color, fill_opacity=peak * (1 - i / (layers + 1)),
                     stroke_width=0))
    return g


def soft_glow_disc(radius, color, strength=0.4, n=30):
    """Smooth radial glow: `strength` is the total opacity at the centre, fading to nothing at `radius`."""
    a = 1.0 - (1.0 - strength) ** (1.0 / n)
    return VGroup(*[Circle(radius=radius * i / n, fill_color=color, fill_opacity=a, stroke_width=0) for i in range(n, 0, -1)])


def soft_glow_rect(w, h, r, color, strength=0.3, spread=0.8, n=26):
    """Smooth glow around a rounded rectangle: `strength` is the opacity at its edge, fading out over `spread`."""
    a = 1.0 - (1.0 - strength) ** (1.0 / n)
    return VGroup(*[RoundedRectangle(width=w + 2 * spread * i / n, height=h + 2 * spread * i / n, corner_radius=r + spread * i / n,
                                     fill_color=color, fill_opacity=a, stroke_width=0) for i in range(n, 0, -1)])


def overlay(opacity=0.7, color=INK):
    """Full-screen translucent rectangle for dimming."""
    return Rectangle(width=config.frame_width + 1, height=config.frame_height + 1, fill_color=color,
                     fill_opacity=opacity, stroke_width=0)


def zoom_rate(q):
    """Rate function that makes a linear scale interpolation look like an exponential zoom (q = end/start)."""
    if abs(q - 1.0) < 1e-6:
        return lambda a: a
    return lambda a: (q ** a - 1.0) / (q - 1.0)
