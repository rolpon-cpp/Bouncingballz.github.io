# Written by Claude Sonnet 5.5
"""Synthesize every sound effect into audio/sfx/*.wav (original, royalty-free, no music)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from modkit import config as C
from modkit.audio_io import write_wav
from modkit.sfx_lib import REGISTRY


def main():
    C.SFX_DIR.mkdir(parents=True, exist_ok=True)
    for name, factory in REGISTRY.items():
        x = factory()
        assert np.isfinite(x).all(), name
        write_wav(C.SFX_DIR / f"{name}.wav", x, C.SAMPLE_RATE)
        rms = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))
        print(f"{name:15s} {len(x) / C.SAMPLE_RATE:5.2f} s  peak {np.max(np.abs(x)):.2f}  rms {rms:.3f}")
    print(f"wrote {len(REGISTRY)} sound effects to {C.SFX_DIR}")


if __name__ == "__main__":
    main()
