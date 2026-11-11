# Written by Claude Sonnet 5.5
"""TimedScene: a Manim Scene whose every play() and wait() is frame-accurate.

Manim emits ceil(run_time * fps) frames for an animation but int(duration / dt) frames for a static
wait. This class converts every duration to a whole number of frames and compensates for both rules,
so the rendered video is exactly plan.total * fps frames long, the same length as the mixed audio.
"""
import sys

import numpy as np
from manim import *
from manim.animation.animation import Wait as _Wait

from .config import FPS, frames
from .plans import get_plan
from .theme import INK


class TimedScene(Scene):
    SCENE_NO = 0

    def setup(self):
        super().setup()
        self.plan = get_plan(self.SCENE_NO)
        self.fr = 0                       # frames emitted so far
        self.camera.background_color = INK

    @property
    def now(self) -> float:
        return self.fr / FPS

    # ---- scene bookkeeping --------------------------------------------------------------------
    def add_mobjects_from_animations(self, animations):
        """Manim adds the mobject of every animation that is not on screen yet. For an AnimationGroup (or a
        wrapper VGroup around things already on screen) that mobject is a temporary Group, and adding it
        extracts the members from their parents and re-appends them on top, which scrambles draw order and
        dissolves parent groups. Only genuinely new mobjects are added here."""
        on_screen = set(id(m) for m in self.get_mobject_family_members())
        for anim in animations:
            if anim.is_introducer() or isinstance(anim, AnimationGroup):
                continue
            mob = anim.mobject
            if id(mob) in on_screen:
                continue
            family = mob.get_family()
            if any(id(m) in on_screen for m in family if m is not mob):
                continue
            self.add(mob)
            on_screen.update(id(m) for m in family)

    def purge(self, *mobjects):
        """Remove mobjects and every part of them (remove() on a group dissolved earlier would leave the parts behind)."""
        parts = []
        for m in mobjects:
            parts.extend(m.get_family())
        self.remove(*parts)

    # ---- frame-accurate primitives -----------------------------------------------------------
    def play(self, *animations, run_time=None, **kwargs):
        if run_time is None:
            run_time = max((a.run_time for a in animations), default=1.0)
        n = max(1, frames(run_time))
        super().play(*animations, run_time=(n - 0.25) / FPS, **kwargs)
        self.fr += n

    def wait(self, duration=1.0, **kwargs):
        n = frames(duration)
        if n <= 0:
            return
        static = not (self.always_update_mobjects or self.updaters
                      or any(m.has_time_based_updater() for m in self.get_mobject_family_members()))
        d = (n + 0.25) / FPS if static else (n - 0.25) / FPS
        Scene.play(self, _Wait(run_time=d, stop_condition=kwargs.get("stop_condition"), frozen_frame=kwargs.get("frozen_frame")))
        self.fr += n

    def hold_until(self, t: float, who: str = ""):
        """Wait until absolute scene time t (seconds). Warns if the timeline already ran past it."""
        n = frames(t) - self.fr
        if n > 0:
            self.wait(n / FPS)
        elif n < -1:
            print(f"[timing] {self.__class__.__name__} {who}: {-n} frames late for t={t:.2f}s", file=sys.stderr)

    def stagger_anim(self, mobjects, dur: float, make=None, each: float = 0.25):
        """One AnimationGroup that reveals mobjects one after another across dur seconds (item i starts
        at i * dur / n), matching Plan.ticks / blips so each sound lines up with its item."""
        from .anims import Show
        make = make or (lambda m: Show(m, pop=0.4, run_time=each))
        dt = dur / max(1, len(mobjects))
        return AnimationGroup(*[Succession(Wait(i * dt), make(m)) if i else make(m) for i, m in enumerate(mobjects)])

    def staggered(self, mobjects, t0: float, dur: float, make=None, each: float = 0.25):
        """Play stagger_anim starting at scene time t0."""
        if not mobjects:
            return
        self.hold_until(t0)
        group = self.stagger_anim(mobjects, dur, make, each)
        self.play(group, run_time=max(group.run_time, 1.0 / FPS))
        self.hold_until(t0 + dur)

    def run_block(self, items):
        """Play several (start_time, animation) pairs together as one block, each at its own start time."""
        t0 = min(t for t, _ in items)
        self.hold_until(t0)
        parts = [Succession(Wait(t - t0), a) if t - t0 > 1e-3 else a for t, a in items]
        group = AnimationGroup(*parts)
        self.play(group, run_time=group.run_time)

    def at(self, name: str):
        """Wait until the plan's cue `name` starts."""
        self.hold_until(self.plan.t(name), name)

    def finish(self):
        """Pad to the planned scene length (the audio length)."""
        self.hold_until(self.plan.total, "end")
        if self.fr != frames(self.plan.total):
            print(f"[timing] {self.__class__.__name__}: emitted {self.fr} frames, plan has {frames(self.plan.total)}", file=sys.stderr)
