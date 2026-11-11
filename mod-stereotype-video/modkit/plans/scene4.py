# Written by Claude Sonnet 5.5
"""Scene 4 (WHY IT KEEPS HAPPENING) cue sheet: a self-feeding loop, then four beats."""
from ..plan import Plan


def _beat(p: Plan, k: int, t0: float) -> float:
    """Big beat title in the middle of the screen, then it shrinks into the top-left tab."""
    p.at(f"b{k}_title", t0, 2.2)
    p.sfx("whoosh_up", t0, 0.2)
    p.at(f"b{k}_tuck", t0 + 2.2, 0.6)
    p.sfx("ui_open", t0 + 2.4, 0.2)
    return t0 + 2.8


def build() -> Plan:
    p = Plan(4)

    # ---- the loop draws itself while the narrator says it feeds itself -------------------------------
    p.at("loop_in", 0.0, 0.5)
    end = p.narrate("n09", 0.6)
    s = lambda k: p.t(f"n09_s{k}")
    for i in range(6):
        p.at(f"node{i}", 0.9 + 1.0 * i, 0.45)
        p.sfx("ui_open", 0.9 + 1.0 * i, 0.22)
    p.at("loop_close", s(2), 0.7)
    p.sfx("success_chime", s(2), 0.25)
    p.at("dot", s(2) + 0.8, 6.0)                              # a light travels round the loop twice
    p.sfx("whoosh_up", s(2) + 0.8, 0.18)
    p.at("loop_out", s(2) + 7.1, 0.6)
    t = s(2) + 7.9

    # ---- beat 1: unpaid jobs pay in status -------------------------------------------------------------
    t = _beat(p, 1, t)
    p.at("b1_bars", t, 0.7)
    end = p.narrate("n10", t + 0.4)
    s = lambda k: p.t(f"n10_s{k}")
    p.at("b1_fill", s(0) + 0.3, p.d("n10_s0") - 1.5)           # Respect fills slowly, Salary stays empty
    p.sfx("slide", s(0) + 0.3, 0.2)
    p.at("b1_badge", p.end("n10_s0") - 1.0, 0.5)
    p.sfx("sparkle", p.end("n10_s0") - 1.0, 0.3)
    p.at("b1_challenge", s(1) + 1.0, 1.4)                      # a challenge to the rules hits the badge
    p.sfx("bubble_pop", s(1) + 1.0, 0.3)
    p.sfx("error_hit", s(1) + 1.45, 0.3)
    t_out = end + 1.8
    p.at("b1_out", t_out, 0.5)
    t = t_out + 0.5

    # ---- beat 2: mods see the worst of the internet daily ------------------------------------------------
    t = _beat(p, 2, t)
    p.at("b2_chat", t, 0.5)
    p.at("b2_jess_head", t + 0.6, 0.3)
    p.sfx("msg_pop", t + 0.6, 0.22)
    p.at("b2_jess", t + 0.9, 1.1)
    p.ticks(t + 0.9, 1.1, 43, 0.2)
    p.at("b2_think", t + 2.2, 0.6)
    p.sfx("bubble_pop", t + 2.2, 0.3)
    end = p.narrate("n11", t + 3.0)
    s = lambda k: p.t(f"n11_s{k}")
    p.at("b2_spam", s(0) + 0.2, 0.4)
    p.sfx("error_hit", s(0) + 0.2, 0.3)
    p.at("b2_tags", s(0) + 2.3, p.d("n11_s0") - 2.7)           # "everyone starts to look like the next one"
    for i in range(5):
        p.sfx("left_pop", s(0) + 2.3 + (p.d("n11_s0") - 2.7) * i / 5, 0.22)
    p.at("b2_check", s(1) + 0.1, 0.6)                          # "Jess was not a troll."
    p.sfx("sparkle", s(1) + 0.1, 0.3)
    t_out = end + 1.8
    p.at("b2_out", t_out, 0.5)
    t = t_out + 0.5

    # ---- beat 3: there is no appeal ---------------------------------------------------------------------
    t = _beat(p, 3, t)
    p.at("b3_scene", t, 0.8)
    p.sfx("slide", t, 0.25)
    end = p.narrate("n12", t + 0.3)
    s = lambda k: p.t(f"n12_s{k}")
    p.at("b3_button", t + 1.2, 0.5)
    p.sfx("ui_open", t + 1.2, 0.25)
    p.at("b3_click", t + 2.4, 0.3)
    p.sfx("timer_tick", t + 2.4, 0.4)
    p.at("b3_door", t + 2.8, 0.8)
    p.at("b3_knock", t + 3.8, 0.9)
    p.sfx("knock", t + 3.8, 0.6)
    p.sfx("lock_click", t + 4.8, 0.5)
    p.sfx("door_thud", t + 5.0, 0.35)
    p.at("b3_bubble", p.end("n12_s0") - 2.2, 0.6)              # "complain loudly somewhere else"
    p.sfx("bubble_pop", p.end("n12_s0") - 2.2, 0.35)
    p.at("b3_memes", s(1) + 0.2, 1.8)                          # the stories spread
    for i in range(3):
        p.sfx("whoosh_up", s(1) + 0.2 + 0.4 * i, 0.2)
    t_out = end + 1.8
    p.at("b3_out", t_out, 0.5)
    t = t_out + 0.5

    # ---- beat 4: the wrong people stay -----------------------------------------------------------------
    t = _beat(p, 4, t)
    p.at("b4_row", t, 0.8)
    p.sfx("slide", t, 0.25)
    end = p.narrate("n13", t + 0.3)
    s = lambda k: p.t(f"n13_s{k}")
    for i in range(5):                                         # the calm mods leave one by one
        p.at(f"b4_leave{i}", s(0) + 0.5 + 0.55 * i, 0.5)
        p.sfx("left_pop", s(0) + 0.5 + 0.55 * i, 0.3)
    p.at("b4_hammer", s(1) + 0.3, 1.2)                         # the one holding the hammer stays
    p.sfx("gavel_tap", s(1) + 0.5, 0.6)
    p.at("b4_truer", s(2), p.d("n13_s2"))
    p.sfx("crown_clink", s(2) + 1.0, 0.4)
    return p.finish(end + 3.6)
