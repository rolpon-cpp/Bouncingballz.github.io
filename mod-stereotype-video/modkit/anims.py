# Written by Claude Sonnet 5.5
"""Small custom animations. They work on mobjects that are already in the scene but hidden.

hide(mob) remembers each part's designed opacity and makes it invisible; Show/TypeText bring it
back to exactly that opacity, so translucent parts (glows, dim panels) keep their look.
Note: Manim calls interpolate(0) inside Animation.begin(), so every animation here sets up its
own state BEFORE calling super().begin().
"""
import numpy as np
from manim import *


def _bg_opacity(m):
    """Opacity of the background stroke (text outlines); 0 when there is none."""
    try:
        return float(m.get_stroke_opacity(background=True))
    except Exception:
        return 0.0


def _remember(mob):
    for m in mob.get_family():
        if not hasattr(m, "_op"):
            m._op = (m.get_fill_opacity(), m.get_stroke_opacity(), _bg_opacity(m))


def hide(mob):
    """Make a mobject (and children) invisible, remembering the designed opacities."""
    _remember(mob)
    for m in mob.get_family():
        m.set_fill(opacity=0, family=False)
        m.set_stroke(opacity=0, family=False)
        if m._op[2] > 0:
            m.set_stroke(opacity=0, background=True, family=False)
    return mob


def _set_alpha(mob, a):
    for m in mob.get_family():
        f, s, b = getattr(m, "_op", (m.get_fill_opacity(), m.get_stroke_opacity(), _bg_opacity(m)))
        m.set_fill(opacity=f * a, family=False)
        m.set_stroke(opacity=s * a, family=False)
        if b > 0:
            m.set_stroke(opacity=b * a, background=True, family=False)


class Show(Animation):
    """Fade a (hidden) mobject in to its designed opacity, optionally sliding and popping."""

    def __init__(self, mobject, shift=ORIGIN, pop=0.0, **kwargs):
        _remember(mobject)
        super().__init__(mobject, **kwargs)
        self.shift_vec = np.array(shift, dtype=float)
        self.pop = pop
        self._c0 = None
        self._scale = 1.0

    def begin(self):
        self._c0 = self.mobject.get_center().copy()
        self._scale = 1.0
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        _set_alpha(self.mobject, min(1.0, a))
        if np.any(self.shift_vec):
            self.mobject.shift(self._c0 + self.shift_vec * (1 - a) - self.mobject.get_center())
        if self.pop:
            s = 1 + self.pop * np.sin(np.pi * a) * (1 - a)
            self.mobject.scale(s / self._scale)
            self._scale = s

    def finish(self):
        _set_alpha(self.mobject, 1.0)
        if np.any(self.shift_vec):
            self.mobject.shift(self._c0 - self.mobject.get_center())
        if self.pop and self._scale != 1.0:
            self.mobject.scale(1.0 / self._scale)
            self._scale = 1.0
        super().finish()


class Hide(Animation):
    """Fade a mobject out to invisible (it stays in the scene, hidden)."""

    def __init__(self, mobject, shift=ORIGIN, **kwargs):
        _remember(mobject)
        super().__init__(mobject, **kwargs)
        self.shift_vec = np.array(shift, dtype=float)
        self._c0 = None

    def begin(self):
        self._c0 = self.mobject.get_center().copy()
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        _set_alpha(self.mobject, 1.0 - a)
        if np.any(self.shift_vec):
            self.mobject.shift(self._c0 + self.shift_vec * a - self.mobject.get_center())

    def finish(self):
        _set_alpha(self.mobject, 0.0)
        super().finish()


class TypeText(Animation):
    """Reveal a Text one glyph at a time (spaces have no glyph, so it types at a steady pace)."""

    def __init__(self, text, **kwargs):
        _remember(text)
        kwargs.setdefault("rate_func", linear)
        super().__init__(text, **kwargs)
        self.glyphs = list(text.submobjects)

    def interpolate_mobject(self, alpha):
        n = len(self.glyphs)
        k = int(np.ceil(self.rate_func(alpha) * n - 1e-9))
        for i, g in enumerate(self.glyphs):
            f, s = getattr(g, "_op", (1.0, 1.0))[:2]
            on = i < k
            g.set_fill(opacity=f if on else 0, family=True)
            g.set_stroke(opacity=s if on else 0, family=True)

    def finish(self):
        for g in self.glyphs:
            f, s = getattr(g, "_op", (1.0, 1.0))[:2]
            g.set_fill(opacity=f, family=True)
            g.set_stroke(opacity=s, family=True)
        super().finish()


class Pop(Animation):
    """Stamp effect: the mobject slams in from a large scale to its normal size."""

    def __init__(self, mobject, from_scale=3.0, **kwargs):
        _remember(mobject)
        kwargs.setdefault("rate_func", linear)
        super().__init__(mobject, **kwargs)
        self.from_scale = from_scale
        self._c = None
        self._s = 1.0

    def begin(self):
        self._c = self.mobject.get_center().copy()
        self._s = 1.0
        super().begin()

    def interpolate_mobject(self, alpha):
        s = 1 + (self.from_scale - 1) * (1 - alpha) ** 2.2
        self.mobject.scale(s / self._s, about_point=self._c)
        self._s = s
        _set_alpha(self.mobject, min(1.0, alpha * 4))

    def finish(self):
        self.mobject.scale(1.0 / self._s, about_point=self._c)
        self._s = 1.0
        _set_alpha(self.mobject, 1.0)
        super().finish()


class Shake(Animation):
    """Camera-shake effect on a group: decaying random offsets, ends exactly where it started."""

    def __init__(self, mobject, amp=0.1, freq=38.0, seed=3, decay_pow=1.5, **kwargs):
        kwargs.setdefault("rate_func", linear)
        super().__init__(mobject, **kwargs)
        self.amp, self.freq, self.decay_pow = amp, freq, decay_pow
        self.phase = np.random.default_rng(seed).uniform(0, 6.28, 4)
        self._c = None

    def begin(self):
        self._c = self.mobject.get_center().copy()
        super().begin()

    def interpolate_mobject(self, alpha):
        decay = (1 - alpha) ** self.decay_pow if self.decay_pow else 1.0
        f = self.freq
        off = self.amp * decay * np.array([
            np.sin(f * alpha + self.phase[0]) + 0.5 * np.sin(2.3 * f * alpha + self.phase[1]),
            np.sin(1.1 * f * alpha + self.phase[2]) + 0.5 * np.sin(2.9 * f * alpha + self.phase[3]),
            0.0])
        self.mobject.shift(self._c + off - self.mobject.get_center())

    def finish(self):
        self.mobject.shift(self._c - self.mobject.get_center())
        super().finish()


class Flicker(Animation):
    """Flicker a mobject on and off a few times, ending hidden or visible."""

    def __init__(self, mobject, blinks=4, end_visible=False, **kwargs):
        _remember(mobject)
        kwargs.setdefault("rate_func", linear)
        super().__init__(mobject, **kwargs)
        self.blinks, self.end_visible = blinks, end_visible

    def interpolate_mobject(self, alpha):
        if alpha >= 1.0 - 1e-9:  # Animation.finish() calls interpolate(1): keep the intended end state
            _set_alpha(self.mobject, 1.0 if self.end_visible else 0.0)
            return
        phase = int(alpha * self.blinks * 2)
        _set_alpha(self.mobject, 1.0 if phase % 2 == 0 else 0.15)


class Zoom(Animation):
    """Slow camera-style push-in: scales a group about a fixed point. Incremental, so it composes
    with other animations that touch parts of the same group (like Throb)."""

    def __init__(self, mobject, factor, about_point, **kwargs):
        kwargs.setdefault("rate_func", smooth)
        super().__init__(mobject, **kwargs)
        self.factor = factor
        self.about = np.array(about_point, dtype=float)
        self._s = 1.0

    def begin(self):
        self._s = 1.0
        super().begin()

    def interpolate_mobject(self, alpha):
        s = self.factor ** self.rate_func(alpha)
        self.mobject.scale(s / self._s, about_point=self.about)
        self._s = s


class Throb(Animation):
    """Typing-dots effect: each dot swells in turn. Incremental scale about each dot's own centre."""

    def __init__(self, dots, period=0.9, amp=0.6, **kwargs):
        kwargs.setdefault("rate_func", linear)
        super().__init__(dots, **kwargs)
        self.dots, self.period, self.amp = list(dots), period, amp
        self._f = [1.0] * len(self.dots)

    def begin(self):
        self._f = [1.0] * len(self.dots)
        super().begin()

    def _factor(self, i, t):
        ph = (t / self.period - i * 0.2) % 1.0
        return 1.0 + self.amp * np.sin(np.pi * ph) ** 2

    def interpolate_mobject(self, alpha):
        t = alpha * self.run_time
        for i, d in enumerate(self.dots):
            f = 1.0 if alpha >= 1.0 - 1e-9 else self._factor(i, t)   # end at the normal size
            d.scale(f / self._f[i], about_point=d.get_center())
            self._f[i] = f


class FadeCurrent(Animation):
    """Fade out whatever is currently visible (each part keeps its own current opacity as the starting point).
    Use this instead of Hide when parts are already partly transparent."""

    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, **kwargs)
        self._cur = []

    def begin(self):
        self._cur = [(m, m.get_fill_opacity(), m.get_stroke_opacity()) for m in self.mobject.get_family()]
        super().begin()

    def interpolate_mobject(self, alpha):
        k = 1.0 - (1.0 if alpha >= 1.0 - 1e-9 else self.rate_func(alpha))
        for m, f, s in self._cur:
            m.set_fill(opacity=f * k, family=False)
            m.set_stroke(opacity=s * k, family=False)


class Sweep(Animation):
    """A bar that sweeps horizontally across the screen, fading in and out (a delete wipe)."""

    def __init__(self, mobject, x_from, x_to, peak=0.25, **kwargs):
        _remember(mobject)
        kwargs.setdefault("rate_func", smooth)
        super().__init__(mobject, **kwargs)
        self.x_from, self.x_to, self.peak = x_from, x_to, peak

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        x = self.x_from + (self.x_to - self.x_from) * a
        self.mobject.shift([x - self.mobject.get_center()[0], 0, 0])
        _set_alpha(self.mobject, self.peak * float(np.sin(np.pi * min(max(a, 0.0), 1.0))) / max(self.peak, 1e-6) * 1.0)
