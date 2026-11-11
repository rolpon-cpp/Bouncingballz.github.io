# Written by Claude Sonnet 5.5
"""Scene 1 (COLD OPEN) cue sheet: a typed chat skit, then the narrator over a freeze on Tyler's name."""
from ..plan import Plan
from ..script_data import chat_lines

HEAD = 0.35  # seconds for a message header to pop in before its text types


def _msg(p: Plan, k: int, t0: float, text: str, cps: float) -> float:
    p.at(f"m{k}_head", t0, HEAD)
    p.sfx("msg_pop", t0, 0.22)
    return p.typed(f"m{k}", t0 + HEAD, text, cps)


def build() -> Plan:
    p = Plan(1)
    chat = chat_lines(1)                      # six typed lines: Jess, Tyler, Jess, Tyler, Jess, Tyler
    p.at("fade_in", 0.0, 0.9)

    t = _msg(p, 1, 1.7, chat[0][1], 15)       # JESS: hey does anyone know when the update drops?

    # Tyler's typing indicator, held uncomfortably long, with a slow push-in on it
    t_typing = t + 0.7
    p.at("typing_in", t_typing, 0.3)
    p.sfx("bubble_pop", t_typing, 0.3)
    p.at("typing_zoom_in", t_typing + 0.3, 6.2)
    p.at("typing_zoom_out", t_typing + 6.5, 0.5)
    t = t_typing + 7.0 + 0.3

    t = _msg(p, 2, t, chat[1][1], 16)         # TYLER: Please read #rules before posting.
    t = _msg(p, 3, t + 0.9, chat[2][1], 14)   # JESS: it's just a question lol
    t = _msg(p, 4, t + 0.9, chat[3][1], 14)   # TYLER: Rule 4. Warned.

    t_stamp = t + 0.45                        # yellow warning icon stamps by Jess's name
    p.at("stamp", t_stamp, 0.75)
    p.sfx("gavel_tap", t_stamp + 0.12, 0.85)

    t = _msg(p, 5, t_stamp + 0.75 + 0.6, chat[4][1], 14)   # JESS: wait what? I didn't even
    p.at("scroll", t + 0.9, 0.4)                           # the list scrolls up one message
    t = _msg(p, 6, t + 0.9 + 0.4, chat[5][1], 16)          # TYLER: Arguing with staff. Banned.

    t_ban = t + 0.8                           # gavel swings, slams; Jess vanishes from the member list
    p.at("gavel_swing", t_ban, 0.32)
    p.sfx("whoosh_down", t_ban, 0.25)
    t_slam = t_ban + 0.32
    p.at("slam", t_slam, 0.5)
    p.sfx("gavel_slam", t_slam, 0.8)
    p.sfx("glitch", t_slam + 0.05, 0.22)
    p.at("collapse", t_slam + 0.55, 0.45)

    t_freeze = t_slam + 1.25                  # freeze on Tyler's name, record scratch
    p.at("freeze", t_freeze, 0.6)
    p.sfx("record_scratch", t_freeze - 0.05, 0.6)

    end = p.narrate("n01", t_freeze + 0.9)    # NARRATOR: You know this guy ...
    p.at("title", p.t("n01_s3"), 0.7)         # title text appears on "Today we find out ..."
    p.sfx("whoosh_up", p.t("n01_s3"), 0.18)
    p.at("outro", end + 2.3, 0.6)             # fade to Tyler's name alone, the start of Scene 2
    return p.finish(end + 2.9)
