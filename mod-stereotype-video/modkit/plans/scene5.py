# Written by Claude Sonnet 5.5
"""Scene 5 (THE MODS YOU NEVER NOTICE) cue sheet.

A silent 3:12 AM cleanup (SFX only, no music), a calm morning with the narrator, then three
checklist cards. The cleanup is shown at a sped-up pace; the corner timer ends at 40 seconds.
"""
from ..plan import Plan
from ..script_data import chat_lines  # noqa: F401  (kept for symmetry with the other plans)

MORNING_LINES = [("MOCHI", "good morning everyone!"), ("PIXEL", "new cat pic in #memes"),
                 ("ORBIT", "who is up for game night?"), ("BISCUIT", "yes!! count me in")]


def build() -> Plan:
    p = Plan(5)

    # ---- 3:12 AM: the spam flood and the 40-second cleanup (no narration) --------------------------
    p.at("night_in", 0.0, 1.0)
    p.at("flood_up", 1.0, 1.0)
    p.sfx("spam_flood", 1.0, 0.45)
    p.at("flood_run", 2.0, 5.4)
    p.at("tools_in", 5.9, 0.6)
    p.sfx("slide", 5.9, 0.25)
    p.at("cur_a", 6.5, 0.6)
    p.at("click_a", 7.1, 0.3)
    p.sfx("timer_tick", 7.15, 0.5)
    p.at("lock", 7.4, 0.9)                                    # the channel locks, the flood stops
    p.sfx("lock_click", 7.45, 0.7)
    p.at("flood_brake", 7.4, 0.5)
    p.at("timer1", 8.3, 0.3)
    p.at("cur_b", 8.9, 0.6)
    p.at("click_b", 9.5, 0.3)
    p.sfx("timer_tick", 9.55, 0.5)
    p.at("bots_in", 9.8, 0.6)
    p.sfx("ui_open", 9.8, 0.3)
    p.at("bots_out", 10.6, 3.2)                               # four bot accounts removed
    for i in range(4):
        p.sfx("left_pop", 10.6 + 0.8 * i, 0.4)
    p.at("timer2", 13.9, 0.3)
    p.at("cur_c", 14.3, 0.6)
    p.at("click_c", 14.9, 0.3)
    p.sfx("timer_tick", 14.95, 0.5)
    p.at("delete", 15.2, 1.1)                                 # the mess is deleted
    p.sfx("delete_swoosh", 15.2, 0.65)
    p.at("timer3", 16.4, 0.3)
    p.at("cur_d", 16.8, 0.6)
    p.at("click_d", 17.4, 0.3)
    p.sfx("timer_tick", 17.45, 0.5)
    p.at("unlock", 17.7, 1.0)                                 # unlocked: a spotless channel
    p.sfx("lock_click", 17.75, 0.6)
    p.sfx("success_chime", 18.0, 0.4)
    p.at("timer4", 18.7, 0.4)                                 # the corner timer reads 40 seconds
    p.at("calm", 19.1, 3.0)

    # ---- morning: members chat cheerfully, the narrator introduces Priya ---------------------------
    p.at("dawn", 22.1, 1.8)
    p.sfx("whoosh_up", 22.1, 0.18)
    t = 24.2
    for i in range(4):
        p.at(f"m{i + 1}_head", t, 0.3)
        p.sfx("msg_pop", t, 0.2)
        t = p.typed(f"m{i + 1}", t + 0.3, MORNING_LINES[i][1], 14, 0.18) + 0.9
    end = p.narrate("n14", 25.1)
    s = lambda k: p.t(f"n14_s{k}")
    p.at("priya_hl", s(0), 1.2)                               # "Meet Priya."
    p.sfx("sparkle", s(0) + 0.3, 0.25)
    p.at("chips", s(2), p.d("n14_s2"))                        # "No thank-you, no screenshot, no applause."
    for i in range(3):
        p.sfx("left_pop", s(2) + p.d("n14_s2") * i / 3, 0.3)
    p.at("clean", s(3), 1.4)                                  # "Just a clean channel ..."
    end2 = p.narrate("n15", end + 0.8)
    p.at("morning_out", end2 + 0.2, 0.7)

    # ---- three checklist cards (silent, readable) ----------------------------------------------------
    t = end2 + 1.0
    for c in range(3):
        tc = t + c * 5.8
        p.at(f"card{c}", tc, 0.7)
        p.sfx("slide", tc, 0.3)
        for b in range(3):
            p.at(f"card{c}_b{b}", tc + 1.1 + 1.5 * b, 0.4)
            p.sfx(f"check_{b + 1}", tc + 1.1 + 1.5 * b, 0.22)
    return p.finish(t + 2 * 5.8 + 1.1 + 4.5 + 0.4 + 6.0)
