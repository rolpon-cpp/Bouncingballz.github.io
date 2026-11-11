# Written by Claude Sonnet 5.5
"""Scene 2 (THE JOB NOBODY APPLIED FOR) cue sheet.

Order follows the script: zoom out to a calendar (narration 1), shift timeline with four
notification bubbles (narration 2), a buzzing phone and a tired hand (narration 3), then four
face-down cards fan out on "four reasons".
"""
from ..plan import Plan


def build() -> Plan:
    p = Plan(2)

    # --- calendar: zoom out from Tyler's name, icons pop in, the narrator explains the job ---
    p.at("zoom", 0.7, 2.3)
    p.sfx("whoosh_down", 0.7, 0.35)
    for i, t in enumerate((3.0, 3.5, 4.0)):                  # shield, clock, bell
        p.at(f"icon{i}", t, 0.4)
        p.sfx("ui_open", t, 0.22)
    end = p.narrate("n02", 1.7)
    s = lambda k: p.t(f"n02_s{k}")
    p.at("sweep", s(1), 6.5)                                  # days light up: "volunteers"
    p.at("shield_pulse", s(1) + 0.2, 0.7)
    p.at("clock_spin", s(2), 4.6)                             # "no salary, no benefits"
    p.sfx("timer_tick", s(2) + 0.3, 0.3)
    p.at("role", s(3), 0.6)                                   # "hands them a role"
    p.sfx("sparkle", s(3) + 0.1, 0.28)
    p.at("keep", p.end("n02_s3") - 1.7, 0.5)                  # "keep it clean."
    p.sfx("bubble_pop", p.end("n02_s3") - 1.7, 0.3)
    p.at("bell", p.end("n02_s3") - 1.1, 1.2)
    p.sfx("ping_a", p.end("n02_s3") - 1.1, 0.25)
    p.at("cal_out", end + 1.5, 0.7)

    # --- shift timeline ---
    t = end + 2.5
    p.at("tl_in", t, 1.2)
    p.sfx("slide", t, 0.3)
    p.at("marker0", t + 1.2, 0.6)                             # marker runs from 6 AM to the first event
    tb = t + 1.9
    p.at("b1", tb, 0.5)
    p.sfx("ping_a", tb, 0.4)
    p.at("b2", tb + 5.4, 0.5)
    p.sfx("ping_b", tb + 5.4, 0.4)
    end3 = p.narrate("n03", tb + 6.2)
    p.at("b3", p.t("n03") + 1.9, 0.5)
    p.sfx("ping_c", p.t("n03") + 1.9, 0.4)
    p.at("b4", p.t("n03") + 3.6, 0.6)
    p.sfx("ping_alert", p.t("n03") + 3.6, 0.45)
    p.at("tl_out", end3 + 2.1, 0.7)

    # --- bedroom desk: the phone buzzes, a tired hand reaches for it ---
    tp = end3 + 3.0
    p.at("phone_in", tp, 0.8)
    p.at("buzz1", tp + 1.4, 0.55)
    p.sfx("phone_buzz", tp + 1.4, 0.6)
    p.at("buzz2", tp + 2.4, 0.55)
    p.sfx("phone_buzz", tp + 2.4, 0.6)
    p.at("hand", tp + 3.1, 2.9)
    p.sfx("hand_slide", tp + 3.1, 0.5)
    end4 = p.narrate("n04", tp + 3.7)
    p.at("drag", tp + 6.1, 2.0)
    p.at("phone_out", p.t("n04_s1") - 0.5, 0.4)

    # --- four face-down cards fan out on "four reasons" ---
    p.at("fan", p.t("n04_s1"), 1.5)
    p.sfx("whoosh_up", p.t("n04_s1"), 0.28)
    for i in range(4):
        p.sfx("card_flip", p.t("n04_s1") + 0.2 + 0.18 * i, 0.3)
    return p.finish(end4 + 3.6)
