# Written by Claude Sonnet 5.5
"""Scene 4: WHY IT KEEPS HAPPENING. A loop that feeds itself, then four beats.

Beat 1 unpaid jobs pay in status (Salary and Respect bars), 2 mods see the worst of the internet
(the opening skit again, with Tyler's thought bubble), 3 there is no appeal (a locked door),
4 the wrong people stay (calm mods leave, the one with the hammer stays).
"""
import numpy as np
from manim import *

from modkit.anims import Hide, Pop, Shake, Show, TypeText, hide
from modkit.base_scene import TimedScene
from modkit.characters import avatar, bust, cartoon_mod
from modkit.chat_ui import ChatWindow
from modkit.icons import checkmark, crown, lock
from modkit.memes import meme_grass, meme_hammer, meme_screenshot
from modkit.props import door, hammer, speech_bubble, tab_chip, thought_bubble
from modkit.script_data import chat_lines, headings, loop_nodes
from modkit.theme import *


def spam_tag(scale=1.0):
    tag = VGroup(rrect(1.25, 0.42, 0.1, RED_DEEP, stroke=RED, sw=2), T("SPAM?", 22, WHITE, "BOLD"))
    tag[1].move_to(tag[0].get_center())
    return tag.scale(scale)


class Grow(Animation):
    """Grow a rounded bar from the left edge to a given width (a rounded rectangle cannot just be stretched)."""

    def __init__(self, bar, left_x, height, color, full_w, **kwargs):
        kwargs.setdefault("rate_func", linear)
        super().__init__(bar, **kwargs)
        self.left_x, self.h, self.color, self.full_w = left_x, height, color, full_w
        self.cy = bar.get_center()[1]

    def interpolate_mobject(self, alpha):
        w = max(self.h, self.full_w * self.rate_func(alpha))
        new = rrect(w, self.h, self.h / 2, self.color)
        new.move_to([self.left_x + w / 2, self.cy, 0])
        self.mobject.become(new)


class WhyItKeepsHappening(TimedScene):
    SCENE_NO = 4

    def construct(self):
        self.titles = {i + 1: t for i, (_, t) in enumerate(headings(4))}
        self.tab = None
        self.loop_part()
        for k in range(1, 5):
            self.beat_title(k)
            getattr(self, f"beat{k}")()
        self.finish()

    # ---- the loop ----------------------------------------------------------------------------------
    def loop_part(self):
        P = self.plan
        labels = loop_nodes()
        colors = [BLUE, ORANGE, PINK, PURPLE, RED, TEAL]
        pos = [(0, 2.35), (4.4, 1.2), (4.4, -1.2), (0, -2.4), (-4.4, -1.2), (-4.4, 1.2)]
        nodes = []
        for lab, col, (x, y) in zip(labels, colors, pos):
            t = T(wrap(lab, 34, 3.1, "SEMIBOLD"), 34, WHITE, "SEMIBOLD", line_spacing=0.95)
            box = rrect(max(t.width + 0.8, 2.7), t.height + 0.5, 0.26, "#1b1f30", stroke=col, sw=4)
            t.move_to(box.get_center())
            nodes.append(VGroup(box, t).move_to([x, y, 0]))
        arrows = [Arrow(nodes[i], nodes[(i + 1) % 6], buff=0.14, stroke_width=7, color=colors[(i + 1) % 6],
                        tip_length=0.26, max_tip_length_to_length_ratio=0.3) for i in range(6)]
        for n in nodes:
            hide(n)
        self.add(*nodes)

        self.hold_until(P.t("node0"))
        self.play(Show(nodes[0], shift=DOWN * 0.2, pop=0.1), run_time=P.d("node0"))
        for i in range(1, 6):
            self.at(f"node{i}")
            self.play(Create(arrows[i - 1]), Show(nodes[i], shift=DOWN * 0.2, pop=0.1), run_time=P.d(f"node{i}"))
        self.at("loop_close")
        self.play(Create(arrows[5]), run_time=P.d("loop_close"))
        glow = VGroup(glow_disc(0.24, WHITE, layers=5, spread=0.07, peak=0.3), disc(0.12, WHITE))
        glow.move_to(nodes[0].get_center()).set_z_index(10)
        path = VMobject()
        path.set_points_as_corners([n.get_center() for n in nodes] + [nodes[0].get_center()])
        self.add(glow)
        self.hold_until(P.t("dot"))
        half = P.d("dot") / 2
        self.play(MoveAlongPath(glow, path, rate_func=linear), run_time=half)
        self.play(MoveAlongPath(glow, path, rate_func=linear), run_time=half)
        self.at("loop_out")
        everything = VGroup(*nodes, *arrows, glow)
        self.play(Hide(everything), run_time=P.d("loop_out"))
        self.remove(*nodes, *arrows, glow)

    # ---- beat title: big in the middle, then it morphs into the top-left tab --------------------------
    def beat_title(self, k):
        P = self.plan
        tab = tab_chip(k, self.titles[k])
        big = tab.copy().scale(2.2).move_to([0, 0.4, 0]).set_z_index(40)
        hide(big)
        self.add(big)
        self.hold_until(P.t(f"b{k}_title"))
        self.play(Show(big, shift=UP * 0.2, pop=0.06), run_time=0.45)
        self.wait(P.d(f"b{k}_title") - 0.45)
        anims = [Transform(big, tab)]
        if self.tab is not None:
            anims.append(Hide(self.tab))
        self.play(*anims, run_time=P.d(f"b{k}_tuck"))
        if self.tab is not None:
            self.remove(self.tab)
        self.tab = big

    # ---- beat 1: unpaid jobs pay in status -------------------------------------------------------------
    def beat1(self):
        P = self.plan
        x0, x1 = -3.6, 4.0
        sal_lab = T("Salary", 46, TEXT, "BOLD").move_to([-6.6, 0.8, 0], aligned_edge=LEFT)
        res_lab = T("Respect", 46, TEXT, "BOLD").move_to([-6.6, -1.0, 0], aligned_edge=LEFT)
        sal_bar = rrect(x1 - x0, 0.7, 0.35, "#1b1f30", stroke="#4a5070", sw=4).move_to([(x0 + x1) / 2, 0.8, 0])
        res_bar = rrect(x1 - x0, 0.7, 0.35, "#1b1f30", stroke="#4a5070", sw=4).move_to([(x0 + x1) / 2, -1.0, 0])
        zero = T("$0", 34, MUTED, "SEMIBOLD").move_to([x0 + 0.55, 0.8, 0])
        fill = rrect(0.7, 0.7, 0.35, PURPLE_DEEP).move_to([x0 + 0.35, -1.0, 0])
        glow = glow_rect(x1 - x0, 0.7, 0.35, PURPLE, layers=5, spread=0.08, peak=0.0)
        badge = VGroup(disc(0.62, "#1b1f30", stroke=PURPLE, sw=4), crown(0.62)).move_to([5.45, -1.0, 0])
        bubble = speech_bubble("this rule makes no sense", 27, tail=1, stroke=ORANGE, max_w=2.7).move_to([5.35, 0.95, 0])
        group = VGroup(sal_lab, res_lab, sal_bar, res_bar, zero)
        for m in (group, badge, bubble):
            hide(m)
        self.add(group, fill, badge, bubble)
        fill.set_fill(opacity=0)

        self.hold_until(P.t("b1_bars"))
        self.play(Show(group, shift=RIGHT * 0.25), run_time=P.d("b1_bars"))
        fill.set_fill(opacity=1)
        self.hold_until(P.t("b1_fill"))
        self.play(Grow(fill, x0, 0.7, PURPLE_DEEP, (x1 - x0) * 0.92), run_time=P.d("b1_fill"))
        self.at("b1_badge")
        self.play(Show(badge, pop=0.4), run_time=P.d("b1_badge"))
        self.at("b1_challenge")
        self.play(Show(bubble, pop=0.2, shift=DOWN * 0.15, run_time=0.4), Shake(badge, amp=0.07, freq=80, run_time=1.0),
                  run_time=P.d("b1_challenge"))
        self.at("b1_out")
        self.play(Hide(VGroup(group, badge, bubble)), Hide(fill), run_time=P.d("b1_out"))
        self.remove(group, fill, badge, bubble)

    # ---- beat 2: the skit again, with Tyler's thought bubble -----------------------------------------------
    def beat2(self):
        P = self.plan
        lines = chat_lines(1)
        chat = ChatWindow()
        m1 = chat.add_message("JESS", lines[0][1])
        m2 = chat.add_message("TYLER", lines[1][1])               # only its header is shown: Tyler is thinking
        chat.scale(0.86).move_to([0, -0.15, 0])
        curtain = overlay(1.0).set_z_index(30)
        self.tab.set_z_index(40)
        self.add(chat, curtain)
        self.hold_until(P.t("b2_chat"))
        self.play(Hide(curtain), run_time=P.d("b2_chat"))
        self.at("b2_jess_head")
        self.play(Show(m1.header, shift=DOWN * 0.08), Show(m2.header, shift=DOWN * 0.08), run_time=P.d("b2_jess_head"))
        self.play(TypeText(m1.text), run_time=P.d("b2_jess"))

        think = thought_bubble("That is the 40th 'when is the update' today.", 28, tail="left", max_w=3.3)
        think.move_to([m2.name.get_right()[0] + 0.7 + think.width / 2, m2.avatar.get_center()[1] - 0.45, 0])
        spam = spam_tag().next_to(m1.name, RIGHT, buff=0.25)
        rows = [chat.member_rows[k] for k in ("JESS", "MOCHI", "PIXEL", "ORBIT", "BISCUIT", "NOVA")]
        tags = [spam_tag(0.52).next_to(r.name_mob, RIGHT, buff=0.1) for r in rows]
        ok = VGroup(disc(0.2, "#1d5c44"), checkmark(0.22, GREEN, 4)).move_to(m1.avatar.get_center() + np.array([-0.3, 0.3, 0]))
        for m in (think, spam, ok, *tags):
            hide(m)
        self.add(think, spam, ok, *tags)

        self.at("b2_think")
        self.play(Show(think, pop=0.15, shift=RIGHT * 0.2), run_time=P.d("b2_think"))
        self.at("b2_spam")
        self.play(Show(spam, pop=0.6), run_time=P.d("b2_spam"))
        self.hold_until(P.t("b2_tags"))
        self.play(self.stagger_anim(tags, P.d("b2_tags"), make=lambda m: Show(m, pop=0.5, run_time=0.25)),
                  run_time=P.d("b2_tags"))
        self.at("b2_check")
        self.play(Hide(spam), Hide(tags[0]), Show(ok, pop=0.5), run_time=P.d("b2_check"))
        self.at("b2_out")
        curtain2 = overlay(1.0).set_z_index(30)
        hide(curtain2)
        self.add(curtain2)
        self.play(Show(curtain2), run_time=P.d("b2_out"))
        self.remove(chat, curtain, think, spam, ok, *tags, curtain2)

    # ---- beat 3: there is no appeal -----------------------------------------------------------------------
    def beat3(self):
        P = self.plan
        av = avatar("J", PINK, 0.42).move_to([-5.9, 0.7, 0])
        box = rrect(6.0, 0.95, 0.22, HEADER, stroke=LINE, sw=3).move_to([-2.2, 0.7, 0])
        cursor = Line([-4.95, 0.42, 0], [-4.95, 0.98, 0]).set_stroke(MUTED, width=4)
        padlock_small = lock(0.5, "#6a708f").move_to([0.35, 0.7, 0])
        left = VGroup(av, box, cursor, padlock_small)
        button = VGroup(rrect(5.2, 0.9, 0.22, "#1c66d4"), T("Contact the moderators", 34, WHITE, "BOLD"))
        button[1].move_to(button[0].get_center())
        button.move_to([-2.6, -0.95, 0])
        dr = door(3.3).move_to([4.6, 0.0, 0])
        padlock = lock(0.9, GOLD).move_to(dr.leaf.get_center() + np.array([-0.1, -0.15, 0]))
        arrow = Arrow(button.get_right() + RIGHT * 0.1, dr.get_left() + LEFT * 0.1, buff=0.05, stroke_width=7, color=MUTED, tip_length=0.28)
        loud = speech_bubble("this ban is unfair!!", 36, stroke=RED, tail=-1, max_w=5.0).move_to([-3.0, 2.3, 0])
        minis = [meme_hammer().scale(0.27), meme_grass().scale(0.27), meme_screenshot().scale(0.27)]
        targets = [np.array([0.6, 2.35, 0]), np.array([2.9, 2.35, 0]), np.array([5.2, 2.35, 0])]
        for mini, tgt in zip(minis, targets):
            mini.move_to(tgt)
        for m in (left, button, dr, padlock, loud, *minis):
            hide(m)
        self.add(left, button, dr, padlock, loud, *minis)

        self.hold_until(P.t("b3_scene"))
        self.play(Show(left, shift=RIGHT * 0.3), run_time=P.d("b3_scene"))
        self.at("b3_button")
        self.play(Show(button, shift=UP * 0.2, pop=0.1), run_time=P.d("b3_button"))
        self.at("b3_click")
        self.play(ScaleInPlace(button, 0.93, rate_func=there_and_back), run_time=P.d("b3_click"))
        self.at("b3_door")
        self.play(Create(arrow), Show(dr, shift=LEFT * 0.3), run_time=P.d("b3_door"))
        self.at("b3_knock")
        self.play(Shake(dr, amp=0.05, freq=90, decay_pow=0.0), run_time=0.95)
        self.play(Pop(padlock, 2.4), run_time=0.35)
        self.at("b3_bubble")
        self.play(Show(loud, pop=0.2, shift=DOWN * 0.15), run_time=P.d("b3_bubble"))
        self.hold_until(P.t("b3_memes"))
        starts = [loud.get_center() - t for t in targets]
        parts = [Succession(Wait(0.4 * i), Show(m, shift=st, pop=0.1, run_time=0.8)) if i else Show(m, shift=st, pop=0.1, run_time=0.8)
                 for i, (m, st) in enumerate(zip(minis, starts))]
        group = AnimationGroup(*parts)
        self.play(group, run_time=group.run_time)
        self.at("b3_out")
        everything = VGroup(left, button, dr, padlock, loud, *minis)
        self.play(Hide(everything), Hide(arrow), run_time=P.d("b3_out"))
        self.remove(left, button, dr, padlock, loud, arrow, *minis)

    # ---- beat 4: the wrong people stay -----------------------------------------------------------------------
    def beat4(self):
        P = self.plan
        names = ["Marlow", "Ines", "Kofi", "Tess", "Dev"]
        cols = [TEAL, BLUE, ORANGE, GREEN, PINK]
        skins = ["#f0c4a0", "#d9a07a", "#b8805e", "#f3cfb3", "#e2b48f"]
        hairs = ["#3a2a1e", "#1c1a26", "#5b3a22", "#c58a3c", "#2a2140"]
        xs = [-5.2, -3.1, -1.0, 1.1, 3.2]
        calm = []
        for n, c, sk, hr, x in zip(names, cols, skins, hairs, xs):
            b = bust(c, 0.66, sk, hr, face=True).move_to([x, 0.95, 0])
            lab = T(n, 28, MUTED, "MEDIUM").move_to([x, -0.15, 0])
            calm.append(VGroup(b, lab))
        tyler = cartoon_mod(0.78).move_to([5.3, 1.1, 0])
        tname = T("Tyler", 30, PURPLE, "SEMIBOLD").move_to([5.3, -0.15, 0])
        ham = hammer(1.9).rotate(np.radians(-18), about_point=ORIGIN)
        ham.move_to([6.15, 0.55, 0])
        hold = VGroup(tyler, tname, ham)
        halo = glow_disc(1.5, PURPLE_DEEP, layers=7, spread=0.2, peak=0.28).move_to(tyler.get_center())
        logs = VGroup(*[T(f"{n} has left the server", 27, MUTED, "MEDIUM", slant=ITALIC).move_to([-6.6, -1.1 - 0.42 * i, 0], aligned_edge=LEFT)
                        for i, n in enumerate(names)])
        for m in (*calm, hold, halo, logs):
            hide(m)
        self.add(halo, *calm, hold, logs)

        self.hold_until(P.t("b4_row"))
        self.play(Show(VGroup(*calm), shift=UP * 0.2), Show(hold, shift=UP * 0.2), run_time=P.d("b4_row"))
        for i in range(5):                                           # the calm ones leave, one message each
            self.at(f"b4_leave{i}")
            self.play(Hide(calm[i], shift=DOWN * 0.25), Show(logs[i], shift=RIGHT * 0.2), run_time=P.d(f"b4_leave{i}"))
        self.at("b4_hammer")
        pivot = ham.get_bottom()
        self.play(Show(halo), Succession(Rotate(ham, angle=np.radians(-35), about_point=pivot, rate_func=rush_into, run_time=0.35),
                                          Rotate(ham, angle=np.radians(35), about_point=pivot, rate_func=smooth, run_time=0.85)),
                  run_time=P.d("b4_hammer"))
        self.at("b4_truer")
        grow = hold.animate.scale(1.7, about_point=np.array([5.3, 0.5, 0])).shift(LEFT * 3.0 + DOWN * 0.1)
        self.play(grow, halo.animate.scale(1.7, about_point=halo.get_center()).move_to([2.3, 1.0, 0]), run_time=P.d("b4_truer"),
                  rate_func=smooth)
