# Written by Claude Sonnet 5.5
"""Scene 1: COLD OPEN. A tense chat skit in a fictional server, then a freeze on Tyler's name.

Run from the project root:
    PYTHONPATH=. manim render scenes/scene1_cold_open.py ColdOpen -r 1920,1080 --fps 30
"""
import numpy as np
from manim import *

from modkit.anims import Flicker, Hide, Pop, Shake, Show, Throb, TypeText, Zoom, hide
from modkit.base_scene import TimedScene
from modkit.chat_ui import ChatWindow
from modkit.icons import gavel, starburst, warning
from modkit.script_data import chat_lines
from modkit.theme import *


class ColdOpen(TimedScene):
    SCENE_NO = 1

    def construct(self):
        P = self.plan
        lines = chat_lines(1)
        chat = ChatWindow()
        msgs = [chat.add_message(who, text) for who, text in lines]
        jess_row = chat.member_rows["JESS"]
        pill, tline = chat.tyler_pill, chat.typing_line

        # fade up from black
        curtain = overlay(1.0)
        self.add(chat, curtain)
        self.play(Hide(curtain), run_time=P.d("fade_in"))

        def say(i, together=()):
            m = msgs[i]
            self.at(f"m{i + 1}_head")
            self.play(Show(m.header, shift=DOWN * 0.1), *together, run_time=P.d(f"m{i + 1}_head"))
            self.play(TypeText(m.text), run_time=P.d(f"m{i + 1}"))

        say(0)                                                     # Jess asks about the update

        # Tyler's typing indicator, held uncomfortably long, with a slow push-in
        self.at("typing_in")
        self.play(Show(pill), Show(tline), run_time=P.d("typing_in"))
        focus = pill.get_center()
        self.play(Zoom(chat, 1.12, focus), Throb(chat.tyler_dots), run_time=P.d("typing_zoom_in"))
        self.play(Zoom(chat, 1 / 1.12, focus), Throb(chat.tyler_dots), run_time=P.d("typing_zoom_out"))

        say(1, together=[Hide(pill), Hide(tline)])                 # Tyler: Please read #rules
        say(2)                                                     # Jess: it's just a question lol
        say(3)                                                     # Tyler: Rule 4. Warned.

        # yellow warning icon stamps by Jess's name (chat message and member list)
        stamp = warning(0.42).next_to(msgs[2].name, RIGHT, buff=0.2)
        badge = warning(0.27).next_to(jess_row.name_mob, RIGHT, buff=0.12)
        for s in (stamp, badge):
            hide(s)
        chat.add(stamp)
        jess_row.add(badge)
        ring = Circle(radius=0.26, stroke_color=YELLOW, stroke_width=7, fill_opacity=0).move_to(stamp.get_center())
        self.at("stamp")
        self.play(Pop(stamp, 3.4), Pop(badge, 3.0), run_time=0.3)
        self.add(ring)
        self.play(ring.animate.scale(3.4).set_stroke(opacity=0), run_time=P.d("stamp") - 0.3)
        self.remove(ring)

        say(4)                                                     # Jess: wait what? I didn't even

        # the list scrolls up one message to make room
        self.at("scroll")
        dy = msgs[0].height + 0.04
        self.play(*chat.scroll_anims(dy, fade=[msgs[0]], extras=[stamp]), run_time=P.d("scroll"))
        say(5)                                                     # Tyler: Arguing with staff. Banned.

        # the ban: gavel slam, Jess vanishes from the member list
        self.at("gavel_swing")
        pivot = np.array([4.3, 0.9, 0.0])
        g = gavel(3.2)
        g.set_z_index(60)
        g.move_to(pivot + UP * 1.6)
        self.add(g)
        swing = np.radians(112)
        self.play(Rotate(g, angle=swing, about_point=pivot, rate_func=rush_into), run_time=P.d("gavel_swing"))
        head = pivot + 2.6 * np.array([-np.sin(swing), np.cos(swing), 0.0])
        burst = starburst(1.5, YELLOW).move_to(head).set_z_index(61)
        self.add(burst)
        self.at("slam")
        self.play(Shake(chat, amp=0.14), Flicker(jess_row, blinks=3), burst.animate.scale(2.3).set_opacity(0),
                  run_time=P.d("slam"))
        self.remove(burst)
        self.at("collapse")
        self.play(*chat.leave_anims("JESS", hide_row=False), Hide(g), run_time=P.d("collapse"))
        self.remove(g)

        # freeze on Tyler's name
        spot = T("Tyler | Moderator", 92, PURPLE, "SEMIBOLD").move_to([0, 0.4, 0])
        spot.set_z_index(70)
        glow = glow_rect(spot.width + 0.9, spot.height + 0.6, 0.3, PURPLE_DEEP, layers=8, spread=0.12, peak=0.14)
        glow.move_to(spot.get_center()).set_z_index(69)
        cover = overlay(0.94).set_z_index(40)
        for m in (cover, glow, spot):
            hide(m)
        self.add(cover, glow, spot)
        self.at("freeze")
        self.play(Show(cover), Show(glow), Show(spot, pop=0.06), run_time=P.d("freeze"))

        # the narrator speaks over a very slow push-in on the name
        self.at("n01")
        self.play(spot.animate.scale(1.07), glow.animate.scale(1.07), run_time=P.t("title") - self.now)

        # title text appears; the name settles into the position Scene 2 starts from
        t1 = T("WHY DO DISCORD MODS", 84, TEXT, "HEAVY")
        t2 = T("HAVE A REPUTATION?", 84, TEXT, "HEAVY", t2c={"REPUTATION?": PURPLE})
        block = VGroup(t1, t2).arrange(DOWN, buff=0.2).move_to([0, -0.2, 0]).set_z_index(71)
        sub = T("(a story about power, volunteers, and 3 a.m.)", 38, MUTED, "MEDIUM").move_to([0, -1.85, 0]).set_z_index(71)
        hide(block)
        hide(sub)
        self.add(block, sub)
        self.at("title")
        k = text_width("Tyler | Moderator", HANDOFF_PX, "SEMIBOLD") / spot.width
        self.play(spot.animate.scale(k).move_to(HANDOFF_POS), glow.animate.scale(k).move_to(HANDOFF_POS),
                  Show(block, shift=DOWN * 0.25), Show(sub, shift=DOWN * 0.15), run_time=P.d("title"))

        # hold, then leave only Tyler's name on the page (Scene 2 starts exactly here)
        self.at("outro")
        self.play(Hide(block), Hide(sub), Hide(glow), cover.animate.set_fill(opacity=1.0), run_time=P.d("outro"))
        self.finish()
