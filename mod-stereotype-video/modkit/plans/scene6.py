# Written by Claude Sonnet 5.5
"""Scene 6 (CLOSING) cue sheet: Tyler apologises and unbans Jess, the narrator closes, then the end card."""
from ..plan import Plan
from ..script_data import chat_lines

HEAD = 0.35


def build() -> Plan:
    p = Plan(6)
    lines = chat_lines(6)                       # TYLER: Hey Jess, sorry ...   JESS: ...yes please
    p.at("fade_in", 0.0, 0.8)

    # Tyler's typing indicator, then his apology
    p.at("typing_in", 1.2, 0.3)
    p.sfx("bubble_pop", 1.2, 0.3)
    p.at("typing", 1.5, 3.1)
    t = 4.9
    p.at("m1_head", t, HEAD)
    p.sfx("msg_pop", t, 0.22)
    t = p.typed("m1", t + HEAD, lines[0][1], 18)

    # Jess answers, hesitantly, and returns to the member list
    t += 1.1
    p.at("m2_head", t, HEAD)
    p.sfx("msg_pop", t, 0.22)
    t = p.typed("m2", t + HEAD, lines[1][1], 9)
    p.at("jess_back", t + 0.6, 0.7)
    p.sfx("ui_open", t + 0.6, 0.3)
    p.at("heart", t + 1.4, 0.7)                 # a purple heart pops up by Tyler's name
    p.sfx("heart_pop", t + 1.4, 0.7)
    p.sfx("sparkle", t + 1.6, 0.25)

    end = p.narrate("n16", t + 3.1)
    s = lambda k: p.t(f"n16_s{k}")
    p.at("raid", s(1) + p.d("n16_s1") * 0.5, 2.6)  # a faint "3:12 AM" for "the 3 a.m. raid you never saw"
    p.sfx("timer_tick", s(1) + p.d("n16_s1") * 0.5, 0.25)

    # fade to the end card
    p.at("to_card", end + 0.9, 0.9)
    tc = end + 1.8
    p.at("card_mark", tc, 0.6)
    p.sfx("end_chime", tc, 0.6)
    p.at("card_1", tc + 0.6, 0.8)
    p.at("card_2", tc + 2.2, 0.8)
    p.sfx("ui_open", tc + 2.2, 0.2)
    p.at("card_credit", tc + 0.3, 0.8)
    return p.finish(tc + 10.0)                   # the credit line stays up for the whole end card
