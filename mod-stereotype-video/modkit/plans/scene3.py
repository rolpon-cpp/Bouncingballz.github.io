# Written by Claude Sonnet 5.5
"""Scene 3 (WHERE THE STEREOTYPE COMES FROM) cue sheet: four reasons, each opened by a card flip."""
from ..plan import Plan


def _reveal(p: Plan, k: int, t0: float) -> float:
    """Card k steps forward, flips, shows its title, then tucks into the tab. Returns the end time."""
    appear = 0.0 if k == 1 else 0.5
    if appear:
        p.at(f"r{k}_appear", t0, appear)
        p.sfx("whoosh_up", t0, 0.2)
    t = t0 + appear + (0.8 if k == 1 else 0.2)
    p.at(f"r{k}_card", t, 0.6)
    p.sfx("slide", t, 0.25)
    t += 0.6
    p.at(f"r{k}_flip", t, 0.5)
    p.sfx("card_flip", t + 0.05, 0.4)
    t += 0.5
    p.at(f"r{k}_show", t, 1.5)
    t += 1.5
    p.at(f"r{k}_tuck", t, 0.6)
    p.sfx("ui_open", t + 0.2, 0.2)
    return t + 0.6


def _blips(p: Plan, t0: float, dur: float, n: int, gain: float = 0.1) -> None:
    """n tiny check-mark blips spread evenly over [t0, t0 + dur)."""
    for i in range(n):
        p.sfx(f"check_{i % 3 + 1}", t0 + dur * i / n, gain)


def build() -> Plan:
    p = Plan(3)

    # ---- reason 1: the tiny crown --------------------------------------------------------------
    t = _reveal(p, 1, 0.0)
    end = p.narrate("n05", t + 0.4)
    s = lambda k: p.t(f"n05_s{k}")
    p.at("r1_profile", t, 0.7)
    p.at("r1_crown", t + 1.0, 0.5)
    p.sfx("crown_clink", t + 1.45, 0.55)
    for i in range(3):                                         # Mute, Kick, Ban Member
        p.at(f"r1_btn{i}", s(0) + 1.9 + 0.5 * i, 0.35)
        p.sfx("ui_open", s(0) + 1.9 + 0.5 * i, 0.25)
    for i in range(3):                                         # "No manager, no handbook, no appeals form"
        p.sfx("left_pop", s(2) + p.d("n05_s2") * i / 3, 0.3)
    swell_t, swell_d = s(3) - 0.3, p.d("n05_s3") + 1.0
    p.at("r1_swell", swell_t, swell_d)                         # "Ban Member" swells to fill the screen
    p.sfx("riser", swell_t + swell_d - 3.4, 0.45)
    p.sfx("error_hit", swell_t + swell_d, 0.6)
    t_out = max(end, swell_t + swell_d) + 1.4
    p.at("r1_out", t_out, 0.5)
    t = t_out + 0.5

    # ---- reason 2: you only see the punishments -------------------------------------------------
    t = _reveal(p, 2, t)
    p.at("r2_panels", t, 0.8)
    p.sfx("slide", t, 0.3)
    end = p.narrate("n06", t + 0.6)
    s = lambda k: p.t(f"n06_s{k}")
    p.at("r2_legend", s(0) + 0.2, 3.2)
    p.at("r2_chkA", s(0) + 0.3, p.d("n06_s0") - 0.5)           # quiet good work piles up
    _blips(p, p.t("r2_chkA"), p.d("r2_chkA"), 14)
    p.at("r2_banned", s(1) + 0.4, 0.5)                         # one red BANNED message
    p.sfx("error_hit", s(1) + 0.4, 0.55)
    p.at("r2_chkB", s(1) + 1.0, p.d("n06_s1") - 1.2)
    _blips(p, p.t("r2_chkB"), p.d("r2_chkB"), 6)
    p.at("r2_eyes", s(1) + 1.2, 1.6)                           # a whole channel watches
    for i in range(8):
        p.sfx("bubble_pop", s(1) + 1.2 + 0.2 * i, 0.12)
    p.at("r2_chkC", s(2), p.d("n06_s2"))
    _blips(p, p.t("r2_chkC"), p.d("r2_chkC"), 12)
    p.at("r2_shot", p.end("n06_s3") - 1.5, 0.4)                # "makes a screenshot"
    p.sfx("shutter", p.end("n06_s3") - 1.5, 0.6)
    t_out = end + 1.8
    p.at("r2_out", t_out, 0.5)
    t = t_out + 0.5

    # ---- reason 3: how mods get picked ----------------------------------------------------------
    t = _reveal(p, 3, t)
    end = p.narrate("n07", t + 0.4)
    s = lambda k: p.t(f"n07_s{k}")
    p.at("r3_profile", t, 0.8)
    p.sfx("slide", t, 0.25)
    p.at("r3_since", s(0) + 0.45, 0.5)
    p.sfx("ui_open", s(0) + 0.45, 0.22)
    p.at("r3_rope", s(0) + p.d("n07_s0") * 0.45, 1.0)          # "or whoever the owner already knows"
    p.sfx("slide", s(0) + p.d("n07_s0") * 0.45, 0.3)
    p.at("r3_check", s(1), 0.5)                                # "Plenty of them are great."
    p.sfx("sparkle", s(1), 0.3)
    p.at("r3_eyes", s(2) + 1.6, 1.8)                           # "in public, with an audience"
    for i in range(6):
        p.sfx("bubble_pop", s(2) + 1.6 + 0.28 * i, 0.12)
    t_out = end + 1.8
    p.at("r3_out", t_out, 0.5)
    t = t_out + 0.5

    # ---- reason 4: memes turn stories into a type -----------------------------------------------
    t = _reveal(p, 4, t)
    end = p.narrate("n08", t + 0.3)
    s = lambda k: p.t(f"n08_s{k}")
    p.at("r4_a", s(0) + 0.2, p.d("n08_s0") - 0.2)
    p.sfx("whoosh_up", s(0) + 0.2, 0.25)
    p.sfx("thud", s(0) + 1.5, 0.35)
    p.at("r4_b", s(1) + 0.2, 4.2)
    p.sfx("whoosh_up", s(1) + 0.2, 0.25)
    p.at("r4_c", s(1) + 4.6, p.d("n08_s1") - 4.6)
    p.sfx("whoosh_up", s(1) + 4.6, 0.25)
    p.at("r4_collage", s(2), 1.0)
    p.sfx("slide", s(2), 0.3)
    return p.finish(end + 3.6)
