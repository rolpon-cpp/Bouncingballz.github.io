# Written by Claude Sonnet 5.5
"""Original sound effects synthesized from scratch with numpy (no samples, nothing downloaded).

Every function returns a mono float32 array at 48 kHz, peak-normalised to about 0.9.
The mixer (tools/mix_scene_audio.py) sets the final level of each effect.
"""
import numpy as np
from scipy import signal

from .audio_io import bandpass, highpass, lowpass
from .config import SAMPLE_RATE as SR


# ---- building blocks ------------------------------------------------------------------------
def _n(dur):
    return int(round(dur * SR))


def _t(dur):
    return np.arange(_n(dur), dtype=np.float64) / SR


def _noise(dur, seed):
    return np.random.default_rng(seed).standard_normal(_n(dur))


def _exp(dur, tau, attack=0.002):
    t = _t(dur)
    return np.exp(-t / tau) * np.minimum(1.0, t / max(attack, 1e-4))


def _sine(f, dur, phase=0.0):
    return np.sin(2 * np.pi * f * _t(dur) + phase)


def _chirp(f0, f1, dur):
    t = _t(dur)
    f = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def _norm(x, peak=0.9):
    x = np.asarray(x, dtype=np.float64)
    m = np.max(np.abs(x)) if len(x) else 0.0
    return (x / m * peak).astype(np.float32) if m > 0 else x.astype(np.float32)


def _fade_out(x, ms=8):
    k = min(len(x), int(SR * ms / 1000))
    if k:
        x = x.copy()
        x[-k:] *= np.linspace(1, 0, k)
    return x


def _sum(*parts):
    n = max(len(p) for p in parts)
    out = np.zeros(n)
    for p in parts:
        out[: len(p)] += p
    return out


def _delay(x, sec):
    return np.concatenate([np.zeros(_n(sec)), x])


def _room(x, decay=0.25, seed=1, wet=0.3):
    """Cheap room tail: convolve with exponentially decaying noise."""
    n = _n(decay * 4)
    ir = np.random.default_rng(seed).standard_normal(n) * np.exp(-np.arange(n) / SR / decay)
    ir /= np.sqrt(np.sum(ir ** 2))
    wetsig = signal.fftconvolve(x, ir)[: len(x)]
    return x + wet * wetsig


def _sweep_noise(dur, f0, f1, seed=0, q=1.0):
    """Band-limited noise whose centre frequency glides from f0 to f1 (exponentially)."""
    x = _noise(dur, seed)
    n, block = len(x), 512
    out = np.zeros(n)
    zi = None
    nb = (n + block - 1) // block
    for i in range(nb):
        a, b = i * block, min(n, (i + 1) * block)
        fc = f0 * (f1 / f0) ** (i / max(1, nb - 1))
        lo, hi = max(40.0, fc / (1 + 1 / q)), min(SR / 2 - 200.0, fc * (1 + 1 / q))
        sos = signal.butter(2, [lo, hi], btype="bandpass", fs=SR, output="sos")
        if zi is None:
            zi = np.zeros((sos.shape[0], 2))
        seg, zi = signal.sosfilt(sos, x[a:b], zi=zi)
        out[a:b] = seg
    return out


# ---- chat / UI sounds -------------------------------------------------------------------------
def type_tick(variant=1):
    f = [980, 1120, 1260, 900][(variant - 1) % 4]
    dur = 0.04
    click = bandpass(_noise(dur, 20 + variant), 1800, 7000) * _exp(dur, 0.005, 0.0005)
    body = _sine(f, dur) * _exp(dur, 0.007, 0.0005) * 0.5
    return _norm(_sum(click, body), 0.8)


def msg_pop():
    dur = 0.14
    return _norm(_chirp(480, 920, dur) * _exp(dur, 0.045, 0.004), 0.8)


def ping(f0=880.0, tau=0.22):
    dur = 1.1
    x = _sine(f0, dur) * _exp(dur, tau, 0.003) + 0.45 * _sine(f0 * 2.01, dur) * _exp(dur, tau * 0.5, 0.003)
    x = x + 0.2 * _sine(f0 * 3.02, dur) * _exp(dur, tau * 0.3, 0.003)
    return _norm(_fade_out(x, 30))


def bubble_pop():
    dur = 0.12
    return _norm(_chirp(300, 760, dur) * _exp(dur, 0.04, 0.003), 0.8)


def ui_open():
    dur = 0.2
    return _norm((_chirp(420, 840, dur) * _exp(dur, 0.08, 0.005)), 0.7)


def left_pop():
    dur = 0.3
    x = _chirp(700, 330, dur) * _exp(dur, 0.12, 0.004)
    return _norm(x, 0.7)


def check_blip(f=880.0):
    dur = 0.1
    return _norm(_sine(f, dur) * _exp(dur, 0.03, 0.002), 0.7)


def timer_tick():
    dur = 0.03
    return _norm(bandpass(_noise(dur, 5), 1500, 5000) * _exp(dur, 0.006, 0.0005) + 0.4 * _sine(1500, dur) * _exp(dur, 0.01), 0.6)


def lock_click():
    dur = 0.25
    c1 = bandpass(_noise(dur, 31), 2500, 8000) * _exp(dur, 0.004, 0.0005) + 0.5 * _sine(2400, dur) * _exp(dur, 0.012)
    c2 = _delay(bandpass(_noise(dur, 32), 1800, 6000) * _exp(dur, 0.005, 0.0005) + 0.4 * _sine(1700, dur) * _exp(dur, 0.015), 0.07)
    return _norm(_sum(c1, c2))


def glitch():
    dur = 0.4
    rng = np.random.default_rng(9)
    out = np.zeros(_n(dur))
    pos = 0.0
    while pos < dur - 0.03:
        seg = rng.uniform(0.015, 0.045)
        f = rng.choice([220, 330, 440, 880, 1320, 1760])
        wave = np.sign(np.sin(2 * np.pi * f * _t(seg))) * rng.uniform(0.3, 1.0)
        i = _n(pos)
        out[i:i + len(wave)] += wave[: len(out) - i]
        pos += seg + rng.uniform(0.0, 0.025)
    return _norm(bandpass(out, 200, 6000) * np.linspace(1, 0.2, len(out)), 0.7)


def sparkle():
    dur = 0.9
    rng = np.random.default_rng(4)
    out = np.zeros(_n(dur))
    for i in range(14):
        t0 = rng.uniform(0, dur - 0.25)
        f = rng.choice([1568, 1760, 2093, 2349, 2637, 3136])
        blip = _sine(f, 0.22) * _exp(0.22, 0.05, 0.002) * rng.uniform(0.3, 1.0)
        j = _n(t0)
        out[j:j + len(blip)] += blip[: len(out) - j]
    return _norm(out, 0.7)


def heart_pop():
    dur = 0.6
    pop = _chirp(380, 1250, 0.18) * _exp(0.18, 0.07, 0.004)
    tw = _delay(_sine(2637, 0.4) * _exp(0.4, 0.09, 0.002) * 0.5, 0.07)
    return _norm(_sum(pop, tw), 0.8)


def success_chime():
    notes = [523.25, 659.25, 783.99, 1046.5]
    parts = [_delay(ping(f, 0.3)[: _n(1.0)].astype(np.float64), 0.11 * i) for i, f in enumerate(notes)]
    return _norm(_sum(*parts), 0.8)


def end_chime():
    x = ping(659.25, 0.6).astype(np.float64)
    y = _delay(ping(987.77, 0.6).astype(np.float64) * 0.6, 0.15)
    return _norm(_sum(x, y), 0.7)


# ---- impacts -----------------------------------------------------------------------------------
def gavel_tap():
    dur = 0.4
    knock = _sine(180, dur) * _exp(dur, 0.05) * 0.9 + _sine(390, dur) * _exp(dur, 0.03) * 0.4
    knock = knock + _sine(760, dur) * _exp(dur, 0.015) * 0.25
    click = bandpass(_noise(dur, 3), 1200, 5000) * _exp(dur, 0.006, 0.0005)
    return _norm(_sum(knock, click))


def gavel_slam():
    dur = 1.3
    thud = _chirp(140, 55, dur) * _exp(dur, 0.22, 0.002)
    knock = _sine(210, dur) * _exp(dur, 0.09) * 0.7 + _sine(430, dur) * _exp(dur, 0.05) * 0.4
    click = bandpass(_noise(dur, 11), 700, 6000) * _exp(dur, 0.012, 0.0005)
    x = np.tanh(1.6 * _sum(thud, knock, click))
    return _norm(_fade_out(_room(x, 0.25, 2, 0.35), 40))


def thud(f=70.0):
    dur = 0.7
    x = _chirp(f * 2, f * 0.7, dur) * _exp(dur, 0.16, 0.002) + lowpass(_noise(dur, 6), 400) * _exp(dur, 0.05, 0.001) * 0.6
    return _norm(np.tanh(1.4 * x))


def door_thud():
    return _norm(_sum(thud(60).astype(np.float64), _delay(lock_click().astype(np.float64) * 0.5, 0.18)))


def error_hit():
    dur = 0.5
    x = signal.sawtooth(2 * np.pi * 110 * _t(dur)) + signal.sawtooth(2 * np.pi * 116.5 * _t(dur))
    x = lowpass(x, 900) * _exp(dur, 0.16, 0.003)
    return _norm(np.tanh(1.3 * x))


def crown_clink():
    dur = 1.0
    parts = []
    for i, (f, tau) in enumerate([(2093, 0.35), (3140, 0.22), (4186, 0.14), (5587, 0.09), (7040, 0.05)]):
        parts.append(_sine(f, dur) * _exp(dur, tau, 0.001) / (1 + 0.5 * i))
    parts.append(bandpass(_noise(dur, 8), 3000, 9000) * _exp(dur, 0.01, 0.0005) * 0.6)
    return _norm(_sum(*parts), 0.8)


def knock():
    parts = []
    for i in range(3):
        w = (_sine(150, 0.3) * _exp(0.3, 0.045) + 0.5 * _sine(310, 0.3) * _exp(0.3, 0.025)
             + bandpass(_noise(0.3, 40 + i), 600, 3000) * _exp(0.3, 0.008, 0.0005) * 0.6)
        parts.append(_delay(w, 0.24 * i))
    return _norm(_sum(*parts))


def shutter():
    a = bandpass(_noise(0.12, 50), 2000, 9000) * _exp(0.12, 0.012, 0.0005)
    b = _delay(bandpass(_noise(0.12, 51), 1200, 6000) * _exp(0.12, 0.02, 0.0005) * 0.8, 0.07)
    c = _sine(1300, 0.2) * _exp(0.2, 0.012, 0.0005) * 0.3
    return _norm(_sum(a, b, c), 0.8)


def phone_buzz():
    dur = 0.5
    t = _t(dur)
    car = np.tanh(2.5 * _sine(135, dur))
    gate = 0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 30 * t))
    rattle = bandpass(_noise(dur, 60), 400, 1500) * 0.35
    env = np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.02)
    return _norm((car + rattle) * gate * env, 0.85)


# ---- whooshes and risers -------------------------------------------------------------------------
def whoosh(dur=0.6, up=True, seed=70):
    n = _sweep_noise(dur, 300, 5000, seed=seed, q=0.9) if up else _sweep_noise(dur, 5000, 300, seed=seed, q=0.9)
    t = _t(dur)
    return _norm(n * np.sin(np.pi * t / dur) ** 2)


def card_flip():
    w = whoosh(0.22, True, 71).astype(np.float64) * 0.9
    tick = _delay(bandpass(_noise(0.05, 72), 2000, 6000) * _exp(0.05, 0.006, 0.0005), 0.2)
    return _norm(_sum(w, tick), 0.8)


def slide():
    return _norm(whoosh(0.28, False, 73) * 0.9, 0.6)


def delete_swoosh():
    w = whoosh(0.45, False, 74).astype(np.float64)
    t = _delay(thud(90).astype(np.float64) * 0.4, 0.35)
    return _norm(_sum(w, t), 0.8)


def hand_slide():
    dur = 1.2
    t = _t(dur)
    x = bandpass(_noise(dur, 75), 500, 3200) * np.sin(np.pi * t / dur) ** 1.5
    return _norm(x, 0.5)


def riser(dur=3.4):
    t = _t(dur)
    nz = _sweep_noise(dur, 200, 7000, seed=2, q=0.8) * (t / dur) ** 2
    tone = _chirp(110, 880, dur) * (t / dur) ** 2 * 0.6
    return _norm(_fade_out(nz * 0.9 + tone, 20))


def record_scratch():
    dur = 0.65
    t = _t(dur)
    f = 1500 * np.exp(-t * 3.2) + 90 + 60 * np.sin(2 * np.pi * 18 * t)
    saw = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
    body = bandpass(0.7 * saw + 0.5 * _noise(dur, 5), 300, 6500)
    chops = 0.55 + 0.45 * np.sin(2 * np.pi * (22 + 12 * t) * t) ** 2
    env = np.minimum(1, t / 0.01) * np.where(t < 0.5, 1.0, np.exp(-(t - 0.5) / 0.03))
    return _norm(body * chops * env)


def spam_flood(dur=6.0, density=45, seed=7):
    rng = np.random.default_rng(seed)
    out = np.zeros(_n(dur))
    for _ in range(int(dur * density)):
        t0 = rng.uniform(0, dur - 0.03)
        f = rng.uniform(900, 3200)
        blip = _sine(f, 0.02) * _exp(0.02, 0.007, 0.001) * rng.uniform(0.3, 1.0)
        i = _n(t0)
        out[i:i + len(blip)] += blip[: len(out) - i]
    return _norm(out, 0.6)


def room_tone(n_samples, seed=0, level_db=-52.0):
    """A very faint low rumble used as a bed under the whole video, so silent beats do not sound like dropouts.
    It is noise, not music. level_db is its RMS level in dBFS."""
    x = np.random.default_rng(1000 + seed).standard_normal(n_samples)
    x = lowpass(x, 450.0, order=2).astype(np.float64)
    x /= max(1e-9, np.sqrt(np.mean(x ** 2)))
    return x * (10 ** (level_db / 20.0))


# name -> factory; tools/make_sfx.py writes each one to audio/sfx/<name>.wav
REGISTRY = {
    "type_tick_1": lambda: type_tick(1), "type_tick_2": lambda: type_tick(2),
    "type_tick_3": lambda: type_tick(3), "type_tick_4": lambda: type_tick(4),
    "msg_pop": msg_pop, "ui_open": ui_open, "bubble_pop": bubble_pop, "left_pop": left_pop,
    "ping_a": lambda: ping(784.0), "ping_b": lambda: ping(988.0), "ping_c": lambda: ping(1175.0),
    "ping_alert": lambda: ping(587.0, 0.3),
    "check_1": lambda: check_blip(880.0), "check_2": lambda: check_blip(1047.0), "check_3": lambda: check_blip(1319.0),
    "timer_tick": timer_tick, "lock_click": lock_click, "glitch": glitch, "sparkle": sparkle,
    "heart_pop": heart_pop, "success_chime": success_chime, "end_chime": end_chime,
    "gavel_tap": gavel_tap, "gavel_slam": gavel_slam, "thud": thud, "door_thud": door_thud,
    "error_hit": error_hit, "crown_clink": crown_clink, "knock": knock, "shutter": shutter,
    "phone_buzz": phone_buzz, "whoosh_up": lambda: whoosh(0.6, True), "whoosh_down": lambda: whoosh(0.6, False, 77),
    "card_flip": card_flip, "slide": slide, "delete_swoosh": delete_swoosh, "hand_slide": hand_slide,
    "riser": riser, "record_scratch": record_scratch, "spam_flood": spam_flood,
}
