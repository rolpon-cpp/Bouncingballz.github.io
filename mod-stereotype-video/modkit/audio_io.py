# Written by Claude Sonnet 5.5
"""Small WAV and DSP helpers (numpy and scipy only)."""
import wave
from pathlib import Path

import numpy as np
from scipy import signal

from .config import SAMPLE_RATE


def read_wav(path):
    """Read a PCM WAV file. Returns (float32 mono array in [-1, 1], sample_rate)."""
    with wave.open(str(path), "rb") as w:
        sr, ch, width, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if width == 2:
        x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    elif width == 4:
        x = np.frombuffer(raw, dtype="<i4").astype(np.float32) / 2147483648.0
    elif width == 1:
        x = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
    else:
        raise ValueError(f"unsupported sample width {width} in {path}")
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x, sr


def write_wav(path, x, sr=SAMPLE_RATE):
    """Write float audio (mono shape (n,) or stereo shape (n, 2)) as 16-bit PCM."""
    x = np.asarray(x, dtype=np.float64)
    channels = 1 if x.ndim == 1 else x.shape[1]
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).round().astype("<i2")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def resample(x, sr_in, sr_out=SAMPLE_RATE):
    if sr_in == sr_out:
        return np.asarray(x, dtype=np.float32)
    from math import gcd
    g = gcd(int(sr_in), int(sr_out))
    return signal.resample_poly(x, int(sr_out) // g, int(sr_in) // g).astype(np.float32)


def highpass(x, fc, sr=SAMPLE_RATE, order=2):
    sos = signal.butter(order, fc, btype="highpass", fs=sr, output="sos")
    return signal.sosfilt(sos, x).astype(np.float32)


def lowpass(x, fc, sr=SAMPLE_RATE, order=2):
    sos = signal.butter(order, min(fc, sr / 2 - 100), btype="lowpass", fs=sr, output="sos")
    return signal.sosfilt(sos, x).astype(np.float32)


def bandpass(x, lo, hi, sr=SAMPLE_RATE, order=2):
    sos = signal.butter(order, [lo, min(hi, sr / 2 - 100)], btype="bandpass", fs=sr, output="sos")
    return signal.sosfilt(sos, x).astype(np.float32)


def trim_silence(x, sr, thresh_db=-48.0, keep_ms=60):
    """Trim leading and trailing near-silence, keeping a short margin."""
    if len(x) == 0:
        return x
    thresh = 10 ** (thresh_db / 20.0) * max(1e-9, float(np.max(np.abs(x))))
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    keep = int(sr * keep_ms / 1000)
    return x[max(0, idx[0] - keep): min(len(x), idx[-1] + keep + 1)]


def peak(x):
    return float(np.max(np.abs(x))) if len(x) else 0.0


def active_rms(x, floor_db=-40.0):
    """RMS over the non-silent part of the signal (ignores pauses)."""
    if len(x) == 0:
        return 0.0
    thresh = 10 ** (floor_db / 20.0) * max(1e-9, peak(x))
    a = x[np.abs(x) > thresh]
    return float(np.sqrt(np.mean(a ** 2))) if len(a) else 0.0
