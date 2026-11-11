# Written by Claude Sonnet 5.5
"""Mix narration and sound effects into one stereo WAV per scene: audio/scenes/sceneN.wav.

Each file is exactly (video frames x 1600) samples long, so audio and video lengths match to the
sample. No music is added (royalty-free music only on request).
Usage: python tools/mix_scene_audio.py [scene numbers...]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from modkit import config as C
from modkit.audio_io import read_wav, resample, write_wav
from modkit.plans import get_plan
from modkit.sfx_lib import room_tone

_cache = {}


def load_clip(kind: str, name: str):
    key = (kind, name)
    if key not in _cache:
        path = (C.NARRATION_DIR if kind == "narr" else C.SFX_DIR) / f"{name}.wav"
        x, sr = read_wav(path)
        _cache[key] = resample(x, sr, C.SAMPLE_RATE).astype(np.float64)
    return _cache[key]


def mix_scene(number: int):
    plan = get_plan(number)
    n_frames = C.frames(plan.total)
    n = n_frames * C.SAMPLES_PER_FRAME
    mono = np.zeros(n)
    clipped = 0
    for kind, name, t, gain in plan.audio:
        x = load_clip(kind, name)
        i = int(round(t * C.SAMPLE_RATE))
        if i >= n:
            print(f"  warning: {name} at {t:.2f}s starts after the scene ends")
            continue
        seg = x[: n - i]
        if len(seg) < len(x):
            clipped += 1
        mono[i:i + len(seg)] += seg * gain
    mono += room_tone(n, seed=number)              # faint bed under everything
    peak = float(np.max(np.abs(mono))) if n else 0.0
    if peak > 0.97:
        print(f"  warning: scene {number} peaks at {peak:.2f}, applying soft limiter")
        mono = np.tanh(mono / 0.97) * 0.97
    stereo = np.stack([mono, mono], axis=1)
    out = C.SCENE_AUDIO_DIR / f"scene{number}.wav"
    write_wav(out, stereo, C.SAMPLE_RATE)
    print(f"scene {number}: {plan.total:6.2f} s = {n_frames} frames, {len(plan.audio)} events, "
          f"peak {peak:.2f}" + (f", {clipped} events cut at the end" if clipped else ""))
    return plan


if __name__ == "__main__":
    wanted = [int(a) for a in sys.argv[1:]] or sorted(C.SCENES)
    for num in wanted:
        mix_scene(num)
