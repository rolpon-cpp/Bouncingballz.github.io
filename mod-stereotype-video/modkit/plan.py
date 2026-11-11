# Written by Claude Sonnet 5.5
"""Plan: the per-scene cue sheet shared by the animation (Manim) and the audio mixer.

A scene's plan is built from the measured narration durations, so the visual timeline and the
sound timeline come from one source and scene length always equals audio length.
"""
import numpy as np

from .config import snap
from .narration_data import load_narration


class Plan:
    def __init__(self, number: int):
        self.number = number
        self.cues = {}      # name -> (start_sec, duration_sec)
        self.audio = []     # (kind, name, start_sec, gain); kind is "narr" or "sfx"
        self.total = 0.0
        self.narr = load_narration()

    # ---- cues (used by the animation) -------------------------------------------------------
    def at(self, name: str, t: float, dur: float = 0.0) -> float:
        """Register a cue; returns its end time so cues can be chained."""
        self.cues[name] = (float(t), float(dur))
        return float(t) + float(dur)

    def t(self, name: str) -> float:
        return self.cues[name][0]

    def d(self, name: str) -> float:
        return self.cues[name][1]

    def end(self, name: str) -> float:
        t, d = self.cues[name]
        return t + d

    # ---- audio events (used by the mixer) ---------------------------------------------------
    def narrate(self, clip_id: str, t: float, gain: float = 1.0) -> float:
        """Place a narrator clip. Registers cues clip_id and clip_id_s0, clip_id_s1... (sentences)."""
        clip = self.narr[clip_id]
        self.audio.append(("narr", clip_id, float(t), gain))
        self.cues[clip_id] = (float(t), clip["duration"])
        for k, s in enumerate(clip["sentences"]):
            self.cues[f"{clip_id}_s{k}"] = (float(t) + s["start"], s["end"] - s["start"])
        return float(t) + clip["duration"]

    def sfx(self, name: str, t: float, gain: float = 0.5) -> None:
        self.audio.append(("sfx", name, max(0.0, float(t)), gain))

    def ticks(self, t0: float, dur: float, n_chars: int, gain: float = 0.22, every: int = 2) -> None:
        """Soft key-click sounds spread over a typed message."""
        n = max(1, n_chars // every)
        for i in range(n):
            tt = t0 + dur * (i + 0.5) / n
            self.sfx(f"type_tick_{i % 4 + 1}", tt, gain * (0.8 + 0.2 * ((i * 7) % 3) / 2))

    def typed(self, name: str, t0: float, text: str, cps: float, gain: float = 0.22) -> float:
        """Register a typed message cue (duration from characters per second) plus key clicks."""
        dur = max(0.7, len(text) / cps)
        self.at(name, t0, dur)
        self.ticks(t0, dur, len(text), gain)
        return t0 + dur

    def finish(self, total: float) -> "Plan":
        self.total = snap(total)
        return self

    def last_audio_end(self) -> float:
        """Latest end of any narrator clip (sanity check for the total)."""
        ends = [t + self.narr[n]["duration"] for k, n, t, _ in self.audio if k == "narr"]
        return max(ends) if ends else 0.0


def chain(*times):
    """Small helper: the largest of several times."""
    return float(np.max(times))
