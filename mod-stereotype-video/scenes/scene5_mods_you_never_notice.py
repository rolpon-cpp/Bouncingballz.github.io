# Written by Claude Sonnet 5.5
"""Scene 5: THE MODS YOU NEVER NOTICE.

3:12 AM: Priya's screen floods with spam too fast to read; she locks the channel, removes the bots,
deletes the mess and unlocks it (corner timer: 40 seconds). Morning: members chat cheerfully in a
spotless #general. Then three checklist cards for members, mods and server owners.
"""
import numpy as np
from manim import *

from modkit.anims import FadeCurrent, Hide, Show, Sweep, TypeText, _set_alpha, hide
from modkit.base_scene import TimedScene
from modkit.characters import priya_back
from modkit.chat_ui import ChatWindow
from modkit.icons import checkmark, clock, lock
from modkit.plans.scene5 import MORNING_LINES
from modkit.props import monitor
from modkit.script_data import checklists
from modkit.theme import *

MONO = "DejaVu Sans Mono"


class FloodScroll(Animation):
    """Spam flood: rows scroll upward through a region and fade at its edges, so no clipping is needed.
    Row velocity changes linearly from v0 to v1 over the animation; `state` carries offset and time between runs."""

    def __init__(self, rows, region, state, v0, v1, gap, **kwargs):
        kwargs.setdefault("rate_func", linear)
        super().__init__(VGroup(*rows), **kwargs)
        self.rows, self.top, self.bottom = list(rows), region[0], region[1]
        self.state, self.v0, self.v1, self.gap = state, v0, v1, gap
        self.cycle = gap * len(self.rows)

    def _place(self, off, t_total):
        fade_in = min(1.0, t_total / 0.7)
        for i, r in enumerate(self.rows):
            y = self.top - ((i * self.gap - off) % self.cycle)
            a = 0.0 if (y < self.bottom or y > self.top) else min(1.0, (self.top - y) / 0.3, (y - self.bottom) / 0.3)
            r.shift([0, y - r.get_center()[1], 0])
            _set_alpha(r, a * fade_in)

    def interpolate_mobject(self, alpha):
        t = alpha * self.run_time
        off = self.state["off"] + self.v0 * t + (self.v1 - self.v0) * t * t / (2 * max(self.run_time, 1e-6))
        self._place(off, self.state["t"] + t)

    def finish(self):
        d = self.run_time
        self.state["off"] += self.v0 * d + (self.v1 - self.v0) * d / 2
        self.state["t"] += d
        self.interpolate_mobject(1.0)
        if self.suspend_mobject_updating and self.mobject is not None:
            self.mobject.resume_updating()


def spam_row(rng, width):
    col = [ORANGE, PINK, YELLOW, GREEN, BLUE, TEAL, RED][rng.integers(0, 7)]
    av = disc(0.13, col).move_to([0.13, 0.0, 0])
    nm = rrect(rng.uniform(0.7, 1.4), 0.085, 0.04, col)
    nm.move_to([0.4 + nm.width / 2, 0.1, 0])
    tag = rrect(0.34, 0.14, 0.04, RED_DEEP).next_to(nm, RIGHT, buff=0.1)
    body = rrect(rng.uniform(1.4, width - 0.9), 0.085, 0.04, "#5a6188")
    body.move_to([0.4 + body.width / 2, -0.07, 0])
    link = rrect(rng.uniform(0.8, 1.7), 0.085, 0.04, BLUE)
    link.move_to([0.4 + link.width / 2, -0.21, 0])
    return VGroup(av, nm, tag, body, link)


def bot_icon():
    head = rrect(0.38, 0.3, 0.08, RED)
    eyes = VGroup(disc(0.04, WHITE).move_to([-0.09, 0.0, 0]), disc(0.04, WHITE).move_to([0.09, 0.0, 0]))
    ant = Line([0, 0.15, 0], [0, 0.28, 0]).set_stroke(RED, width=4)
    return VGroup(ant, head, eyes)


def banner(text, color, fill, locked, width):
    bar = VGroup(rrect(width, 0.95, 0.24, fill, stroke=color, sw=4), lock(0.62, color, locked=locked), T(text, 38, WHITE, "BOLD"))
    bar[1].move_to(bar[0].get_left() + RIGHT * 0.6)
    bar[2].move_to(bar[0].get_center() + RIGHT * 0.35)
    return bar


class ModsYouNeverNotice(TimedScene):
    SCENE_NO = 5

    def construct(self):
        self.night_part()
        self.morning_part()
        self.cards_part()
        self.finish()

    # ---- 3:12 AM -----------------------------------------------------------------------------------
    def night_part(self):
        P = self.plan
        self.bg = overlay(1.0, "#06070d").set_z_index(-5)
        self.mon = monitor(10.6, 5.9).move_to([1.2, 0.1, 0])
        self.glow = soft_glow_rect(10.6, 5.9, 0.22, BLUE, strength=0.28, spread=1.1).move_to(self.mon.get_center())
        self.glow.set_z_index(-2)
        self.mon.set_z_index(-1)
        chat = self.chat = ChatWindow(mod="PRIYA", members=("MOCHI", "PIXEL", "ORBIT", "BISCUIT", "NOVA"))
        self.msgs = [chat.add_message(k, t) for k, t in MORNING_LINES]       # hidden until morning
        chat.scale(0.72).move_to(self.mon.screen_rect.get_center())
        screen = self.mon.screen_rect
        self.screen_cover = rrect(screen.width, screen.height, 0.12, "#090b12").move_to(screen.get_center()).set_z_index(50)
        self.priya = priya_back(1.35).move_to([-5.45, -2.3, 0]).set_z_index(4)
        self.clock_txt = T("3:12 AM", 70, ORANGE, "BOLD", font=MONO).move_to([-5.0, 3.55, 0])

        pill = rrect(2.5, 0.75, 0.375, "#1b1f30", stroke=LINE, sw=3)
        ic = clock(0.46, TEAL).move_to(pill.get_left() + RIGHT * 0.45)
        timer_txt = T("0:00", 38, TEXT, "BOLD", font=MONO).move_to(pill.get_center() + RIGHT * 0.35)
        self.timer = VGroup(pill, ic, timer_txt).move_to([5.9, 3.45, 0])
        self.timer_txt = self.timer[2]

        # the spam flood (inside the chat's message area)
        left = chat.centre.get_left()[0] + 0.25
        width = chat.centre.width - 0.5
        top = chat.centre.get_top()[1] - 0.78 * 0.72 - 0.12
        bottom = chat.input_bar.get_top()[1] + 0.12
        self.region = (top, bottom)
        rng = np.random.default_rng(12)
        self.rows = [spam_row(rng, width).scale(1.1).move_to([left + width / 2, top - i * 0.55, 0]) for i in range(12)]
        for r in self.rows:
            r.shift(RIGHT * (left - r.get_left()[0]))
            hide(r)
        for r in self.rows:
            r.set_z_index(2)
        flood = {"off": 0.0, "t": 0.0}

        # mod tools, cursor, banners, bot list
        panel = rrect(3.2, 3.7, 0.25, "#171a28", stroke=LINE, sw=3).move_to([-5.4, 1.4, 0])
        ttl = T("Mod tools", 26, MUTED, "SEMIBOLD").move_to([-5.4, 3.0, 0])
        self.buttons = []
        for i, name in enumerate(["Lock channel", "Remove bots", "Delete messages", "Unlock channel"]):
            b = VGroup(rrect(2.8, 0.62, 0.16, "#262b45", stroke="#3a4060", sw=2), T(name, 25, TEXT, "SEMIBOLD"))
            b[1].move_to(b[0].get_center())
            self.buttons.append(b.move_to([-5.4, 2.4 - 0.78 * i, 0]))
        self.tools = VGroup(panel, ttl, *self.buttons)
        self.cursor = Polygon([0, 0, 0], [0, -0.62, 0], [0.16, -0.47, 0], [0.3, -0.78, 0], [0.43, -0.72, 0], [0.29, -0.42, 0], [0.5, -0.4, 0],
                              fill_color=WHITE, fill_opacity=1, stroke_color="#05060a", stroke_width=3).set_z_index(80)
        self.cursor.move_to([-6.6, -0.2, 0])
        cx = screen.get_center()[0]
        self.lockbar = banner("Channel locked", RED, "#2a1d2a", True, 5.4).move_to([cx, 0.35, 0]).set_z_index(60)
        self.unlockbar = banner("Channel unlocked", GREEN, "#10281f", False, 5.8).move_to([cx, 0.35, 0]).set_z_index(60)
        card = rrect(4.6, 3.2, 0.26, "#171a28", stroke=RED, sw=3)
        cap = T("Bot accounts", 30, WHITE, "SEMIBOLD").move_to(card.get_top() + DOWN * 0.45)
        self.bot_rows = []
        for i in range(4):
            ic2 = bot_icon().move_to(card.get_left() + np.array([0.55, 0.5 - 0.58 * i - 0.25, 0]))
            nm = T(f"giftbot_0{i + 1}", 27, "#c9cde0", "MEDIUM")
            nm.move_to([ic2.get_right()[0] + 0.25 + nm.width / 2, ic2.get_center()[1], 0])
            self.bot_rows.append(VGroup(ic2, nm))
        self.bot_card = VGroup(card, cap)
        self.bots = VGroup(self.bot_card, *self.bot_rows).move_to([cx, 0.35, 0]).set_z_index(61)
        sweep = rrect(0.7, top - bottom, 0.12, WHITE, opacity=0.25).set_z_index(55)
        sweep.move_to([chat.centre.get_right()[0], (top + bottom) / 2, 0])

        for m in (self.mon, self.glow, self.priya, self.clock_txt, self.timer, self.tools, self.cursor, self.lockbar,
                  self.unlockbar, self.bots, sweep):
            hide(m)
        self.add(self.bg, self.glow, self.mon, chat, self.screen_cover, *self.rows, self.priya, self.clock_txt, self.timer,
                 self.tools, self.cursor, self.lockbar, self.unlockbar, self.bots, sweep)

        def set_timer(text, cue, color=TEXT):
            new = T(text, 38, color, "BOLD", font=MONO).move_to(self.timer_txt.get_center())
            return (P.t(cue), Transform(self.timer_txt, new, run_time=P.d(cue)))

        def press(idx, cue_move, cue_click):
            btn = self.buttons[idx]
            target = btn.get_center() + np.array([0.7, -0.25, 0])
            move = ApplyMethod(self.cursor.move_to, target, run_time=P.d(cue_move), rate_func=smooth)
            click = ScaleInPlace(btn, 0.93, rate_func=there_and_back, run_time=P.d(cue_click))
            return Succession(move, click)

        first = Succession(AnimationGroup(Show(self.tools, shift=RIGHT * 0.3), Show(self.cursor), run_time=P.d("tools_in")),
                           press(0, "cur_a", "click_a"))
        flood_chain = Succession(FloodScroll(self.rows, self.region, flood, 0.0, 9.0, 0.55, run_time=P.d("flood_up")),
                                 FloodScroll(self.rows, self.region, flood, 9.0, 9.0, 0.55, run_time=P.d("flood_run")),
                                 FloodScroll(self.rows, self.region, flood, 9.0, 0.0, 0.55, run_time=P.d("lock")))
        bots_out = self.stagger_anim(self.bot_rows, P.d("bots_out"), make=lambda m: Hide(m, shift=RIGHT * 1.2, run_time=0.5))
        wipe = AnimationGroup(Sweep(sweep, chat.centre.get_right()[0] - 0.4, chat.centre.get_left()[0] + 0.4, 0.25, run_time=P.d("delete")),
                              FadeCurrent(VGroup(*self.rows), run_time=P.d("delete")),
                              Hide(self.lockbar, run_time=P.d("delete")))
        outro = AnimationGroup(Hide(self.unlockbar), Hide(self.tools), Hide(self.cursor), run_time=1.2)

        self.at("night_in")
        night_in = AnimationGroup(Show(self.mon), Show(self.glow), Show(self.priya), Show(self.clock_txt), Show(self.timer),
                                  Hide(self.screen_cover), run_time=P.d("night_in"))
        self.play(night_in, run_time=P.d("night_in"))
        self.run_block([
            (P.t("flood_up"), flood_chain),
            (P.t("tools_in"), first),
            (P.t("lock"), Show(self.lockbar, pop=0.15, shift=DOWN * 0.15, run_time=P.d("lock"))),
            set_timer("0:06", "timer1"),
            (P.t("cur_b"), press(1, "cur_b", "click_b")),
            (P.t("bots_in"), Show(self.bots, shift=UP * 0.2, pop=0.05, run_time=P.d("bots_in"))),
            (P.t("bots_out"), bots_out),
            (P.end("bots_out"), Hide(self.bot_card, run_time=0.1)),
            set_timer("0:19", "timer2"),
            (P.t("cur_c"), press(2, "cur_c", "click_c")),
            (P.t("delete"), wipe),
            set_timer("0:31", "timer3"),
            (P.t("cur_d"), press(3, "cur_d", "click_d")),
            (P.t("unlock"), Show(self.unlockbar, pop=0.15, shift=DOWN * 0.15, run_time=P.d("unlock"))),
            set_timer("0:40", "timer4", GREEN),
            (P.t("calm") + 1.0, outro),
        ])

    # ---- morning ------------------------------------------------------------------------------------
    def morning_part(self):
        P = self.plan
        chat = self.chat
        dawn = overlay(0.94, "#1d2a4a").set_z_index(-4)
        sun = soft_glow_disc(5.2, "#ffb86b", strength=0.42).move_to([-5.8, 3.3, 0]).set_z_index(-3)
        new_clock = T("7:30 AM", 70, GOLD, "BOLD", font=MONO).move_to(self.clock_txt.get_center())
        hide(dawn)
        hide(sun)
        self.add(dawn, sun)
        self.at("dawn")
        self.play(Show(dawn), Show(sun), Transform(self.clock_txt, new_clock), Hide(self.priya), Hide(self.timer), run_time=P.d("dawn"))

        row = chat.member_rows["PRIYA"]
        hl = soft_glow_rect(row.width + 0.1, row.height, 0.14, TEAL, strength=0.35, spread=0.3, n=14).move_to(row.get_center()).set_z_index(5)
        chips = []
        for i, label in enumerate(("thank you", "screenshot", "applause")):
            t = T(label, 30, "#c9cde0", "SEMIBOLD")
            c = VGroup(rrect(3.1, 0.68, 0.34, "#232845", stroke=MUTED, sw=3), t)
            t.move_to(c[0].get_center())
            c.add(Line(t.get_left() + LEFT * 0.12, t.get_right() + RIGHT * 0.12).set_stroke(RED, width=5))
            chips.append(c.move_to([-5.4, 1.5 - 0.9 * i, 0]))
        frame = rrect(chat.width + 0.2, chat.height + 0.2, 0.3, INK, opacity=0.0, stroke=GREEN, sw=6).move_to(chat.get_center()).set_z_index(5)
        for m in (hl, *chips, frame):
            hide(m)
        self.add(hl, *chips, frame)

        items = []
        for i in range(4):                                         # cheerful messages, typed while the narrator speaks
            m = self.msgs[i]
            items.append((P.t(f"m{i + 1}_head"), Succession(Show(m.header, shift=DOWN * 0.06, run_time=P.d(f"m{i + 1}_head")),
                                                            TypeText(m.text, run_time=P.d(f"m{i + 1}")))))
        items += [
            (P.t("priya_hl"), Show(hl, run_time=P.d("priya_hl"))),                                   # "Meet Priya."
            (P.t("chips"), self.stagger_anim(chips, P.d("chips"),
                                             make=lambda m: Show(m, shift=RIGHT * 0.2, pop=0.15, run_time=0.4))),
            (P.t("clean"), AnimationGroup(Show(frame), Hide(hl), run_time=P.d("clean"))),            # "a clean channel"
        ]
        self.run_block(items)
        self.at("morning_out")
        everything = VGroup(chat, self.mon, self.glow, dawn, sun, self.clock_txt, hl, frame, *chips)
        self.play(FadeCurrent(everything), Hide(self.bg), run_time=P.d("morning_out"))
        self.purge(chat, self.mon, self.glow, dawn, sun, self.clock_txt, hl, frame, *chips, self.bg, *self.rows, self.screen_cover,
                   self.priya, self.timer, self.tools, self.cursor, self.lockbar, self.unlockbar, self.bots)

    # ---- the three checklists -----------------------------------------------------------------------
    def cards_part(self):
        P = self.plan
        accents = [BLUE, PURPLE, GOLD]
        xs = [-4.65, 0.0, 4.65]
        heads, all_bullets = [], []
        for (title, bullets), acc, x in zip(checklists(), accents, xs):
            panel = rrect(4.3, 5.5, 0.3, "#171a28", stroke=acc, sw=4).move_to([x, 0.0, 0])
            head = T(title, 36, acc, "BOLD").move_to([x, 2.0, 0])
            y = 1.15
            rows = []
            for b in bullets:
                icon = VGroup(disc(0.19, "#1d5c44"), checkmark(0.22, GREEN, 4))
                txt = T(wrap(b, 29, 2.95, "MEDIUM"), 29, TEXT, "MEDIUM", line_spacing=0.95)
                icon.move_to([x - 1.75, y - 0.17, 0])
                txt.move_to([x - 1.35, y, 0], aligned_edge=UL)
                rows.append(VGroup(icon, txt))
                y -= txt.height + 0.42
            heads.append(VGroup(panel, head))
            all_bullets.append(rows)
        for h, rows in zip(heads, all_bullets):
            hide(h)
            for r in rows:
                hide(r)
            self.add(h, *rows)
        for c in range(3):
            self.hold_until(P.t(f"card{c}"))
            self.play(Show(heads[c], shift=RIGHT * 6.5), run_time=P.d(f"card{c}"), rate_func=smooth)
            for b in range(3):
                self.at(f"card{c}_b{b}")
                self.play(Show(all_bullets[c][b], shift=RIGHT * 0.25, pop=0.1), run_time=P.d(f"card{c}_b{b}"))
