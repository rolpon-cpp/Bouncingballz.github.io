# Written by Claude Sonnet 5.5
"""Scene 6: CLOSING. Back to "Cozy Cat Hangout": Tyler apologises and unbans Jess, the narrator closes,
then the end card. The very last frame shows the credit line.
"""
import numpy as np
from manim import *

from modkit.anims import FadeCurrent, Hide, Pop, Show, Throb, TypeText, hide
from modkit.base_scene import TimedScene
from modkit.chat_ui import ChatWindow
from modkit.config import CREDIT_LINE
from modkit.icons import cat_logo, crown, heart
from modkit.script_data import chat_lines
from modkit.theme import *


class Closing(TimedScene):
    SCENE_NO = 6

    def construct(self):
        P = self.plan
        lines = chat_lines(6)
        chat = ChatWindow()
        m1 = chat.add_message("TYLER", lines[0][1])
        m2 = chat.add_message("JESS", lines[1][1])
        chat.remove_member_instant("JESS")                     # Jess is still banned
        pill, tline = chat.tyler_pill, chat.typing_line
        curtain = overlay(1.0).set_z_index(30)
        self.add(chat, curtain)
        self.play(Hide(curtain), run_time=P.d("fade_in"))

        # Tyler's typing indicator, then his apology
        self.at("typing_in")
        self.play(Show(pill), Show(tline), run_time=P.d("typing_in"))
        self.play(Throb(chat.tyler_dots), run_time=P.d("typing"))
        self.at("m1_head")
        self.play(Show(m1.header, shift=DOWN * 0.1), Hide(pill), Hide(tline), run_time=P.d("m1_head"))
        self.play(TypeText(m1.text), run_time=P.d("m1"))

        # Jess answers, then returns to the member list; a purple heart pops up by Tyler's name
        self.at("m2_head")
        self.play(Show(m2.header, shift=DOWN * 0.1), run_time=P.d("m2_head"))
        self.play(TypeText(m2.text), run_time=P.d("m2"))
        self.at("jess_back")
        self.play(*chat.join_anims("JESS"), run_time=P.d("jess_back"))
        big = heart(0.55, PURPLE).move_to([6.3, 3.4, 0])           # right end of the MODERATOR label line, by Tyler's name
        minis = [heart(0.22, PURPLE).move_to(big.get_center() + np.array([dx, dy, 0])) for dx, dy in ((-0.5, 0.0), (0.2, 0.33))]
        for h in (big, *minis):
            hide(h)
        self.add(big, *minis)
        self.at("heart")
        self.play(Show(big, pop=0.9, shift=DOWN * 0.1), *[Show(h, shift=DOWN * 0.1, pop=0.6) for h in minis], run_time=P.d("heart"))

        # narrator: the stereotype is real, and so are the people behind it
        raid = T("3:12 AM", 64, ORANGE, "BOLD", font="DejaVu Sans Mono").move_to([-2.8, 0.2, 0]).set_z_index(20)
        hide(raid)
        self.add(raid)
        self.at("raid")
        self.play(Show(raid, pop=0.1), run_time=0.6)
        self.wait(P.d("raid") - 1.2)
        self.play(Hide(raid), run_time=0.6)

        # fade to the end card
        self.at("to_card")
        card_bg = overlay(1.0, "#090a12").set_z_index(40)
        hide(card_bg)
        self.add(card_bg)
        self.play(Show(card_bg), run_time=P.d("to_card"))
        self.purge(chat, curtain, big, *minis, raid)

        glow = soft_glow_disc(5.2, PURPLE_DEEP, strength=0.5).move_to([0, 0.5, 0]).set_z_index(41)
        logo = cat_logo(0.55)
        mark = VGroup(logo, crown(0.5).move_to(logo.get_top() + UP * 0.2)).move_to([0, 2.3, 0]).set_z_index(42)
        l1 = T("Got a mod story? Comment it.", 70, WHITE, "HEAVY").move_to([0, 0.65, 0]).set_z_index(42)
        l1b = T("No names please.", 70, PURPLE, "HEAVY").move_to([0, -0.25, 0]).set_z_index(42)
        l2 = T("Like, subscribe, and be nice to your mods.", 44, "#c9cde0", "SEMIBOLD").move_to([0, -1.55, 0]).set_z_index(42)
        credit = T(CREDIT_LINE, 28, "#a9afc7", "MEDIUM").move_to([6.7, -3.55, 0], aligned_edge=RIGHT).set_z_index(43)
        title_block = VGroup(l1, l1b)
        for m in (glow, mark, title_block, l2, credit):
            hide(m)
        self.add(glow, mark, title_block, l2, credit)
        self.at("card_mark")
        self.play(Show(glow), Show(mark, pop=0.2, shift=DOWN * 0.2), Show(credit, shift=UP * 0.1), run_time=P.d("card_mark"))
        self.at("card_1")
        self.play(Show(title_block, shift=UP * 0.25), run_time=P.d("card_1"))
        self.at("card_2")
        self.play(Show(l2, shift=UP * 0.2), run_time=P.d("card_2"))
        self.finish()
