# Written by Claude Sonnet 5.5
"""Scene 3: WHERE THE STEREOTYPE COMES FROM. Four reasons, each opened by a flipping card.

Reason 1 the tiny crown (a Ban Member button swells), 2 you only see the punishments (split screen),
3 how mods get picked (a profile and a velvet rope), 4 memes turn stories into a type (a montage).
"""
import numpy as np
from manim import *

from modkit.anims import Hide, Shake, Show, hide
from modkit.base_scene import TimedScene
from modkit.characters import avatar, bust, friend_group
from modkit.icons import camera_icon, checkmark, cross, crown, eye, warning
from modkit.memes import meme_grass, meme_hammer, meme_screenshot
from modkit.props import card_face, fan_angles, make_fan, velvet_rope
from modkit.script_data import headings
from modkit.theme import *

CARD_ICONS = {
    1: lambda: crown(1.0),
    2: lambda: eye(1.0),
    3: lambda: bust(PURPLE_DEEP, 0.5, SKIN, "#2a2140"),
    4: lambda: camera_icon(1.0, PURPLE_DEEP),
}


def check_badge(r=0.17):
    return VGroup(disc(r, "#1d5c44"), checkmark(r * 1.15, GREEN, 4))


class StereotypeOrigins(TimedScene):
    SCENE_NO = 3

    def construct(self):
        self.titles = {i + 1: title for i, (_, title) in enumerate(headings(3))}
        self.fan = make_fan(fanned=True)          # exactly the fan Scene 2 ended on
        self.add(self.fan)
        self.tab = None
        for k in range(1, 5):
            self.reveal(k)
            getattr(self, f"reason{k}")()
        self.finish()

    # ---- card reveal shared by all four reasons ---------------------------------------------------
    def make_tab(self, k):
        label = T(self.titles[k], 30, WHITE, "BOLD")
        pill = rrect(label.width + 1.2, 0.64, 0.32, PURPLE_DEEP)
        badge = disc(0.24, "#fff4d6").move_to(pill.get_left() + RIGHT * 0.42)
        num = T(str(k), 28, "#3a2788", "HEAVY").move_to(badge.get_center())
        label.move_to(badge.get_right() + RIGHT * (0.2 + label.width / 2))
        tab = VGroup(pill, badge, num, label)
        return tab.move_to([-6.7 + pill.width / 2, 3.45, 0])

    def reveal(self, k):
        P = self.plan
        if k == 1:
            cards = self.fan
        else:
            cards = make_fan(True, numbers=range(k, 5))
            hide(cards)
            self.add(cards)
            self.hold_until(P.t(f"r{k}_appear"))
            self.play(Show(cards, shift=DOWN * 0.3), run_time=P.d(f"r{k}_appear"))
        card = cards[0]
        angle = fan_angles(len(cards))[0]
        self.hold_until(P.t(f"r{k}_card"))
        self.play(card.animate.rotate(np.radians(-angle), about_point=card.get_center()).move_to([0, 0.35, 0]).scale(1.55),
                  *[Hide(c) for c in list(cards)[1:]], run_time=P.d(f"r{k}_card"), rate_func=smooth)

        self.hold_until(P.t(f"r{k}_flip"))
        face = card_face(k, self.titles[k], CARD_ICONS[k](), 2.3, 3.2).scale(1.55).move_to(card.get_center())
        face_w = face.width
        self.play(card.animate.stretch_to_fit_width(0.03), run_time=0.25)
        self.remove(card)
        face.stretch_to_fit_width(0.03)
        self.add(face)
        self.play(face.animate.stretch_to_fit_width(face_w), run_time=0.25)

        self.hold_until(P.t(f"r{k}_tuck"))
        tab = self.make_tab(k)
        hide(tab)
        self.add(tab)
        anims = [face.animate.scale(0.16).move_to(tab.get_left() + RIGHT * 0.45).set_opacity(0), Show(tab)]
        if self.tab is not None:
            anims.append(Hide(self.tab))
        self.play(*anims, run_time=P.d(f"r{k}_tuck"))
        self.remove(face, *list(cards))
        if self.tab is not None:
            self.remove(self.tab)
        self.tab = tab

    # ---- reason 1: the tiny crown -------------------------------------------------------------------
    def reason1(self):
        P = self.plan
        name = T("Tyler | Moderator", 78, PURPLE, "SEMIBOLD")
        av = avatar("T", PURPLE, 0.8).next_to(name, LEFT, buff=0.4)
        profile = VGroup(av, name).move_to([0, 0.95, 0])
        cr = crown(0.66).rotate(-0.2)
        rest = name.get_left() + np.array([0.3, 0.52, 0.0])
        cr.move_to(rest + UP * 4.6)

        def button(label, fill, stroke=None):
            r = rrect(3.0, 0.95, 0.22, fill, stroke=stroke, sw=4)
            return VGroup(r, T(label, 40, WHITE, "BOLD").move_to(r.get_center()))

        mute = button("Mute", "#3a4263").move_to([-3.5, -0.9, 0])
        kick = button("Kick", "#c9741a").move_to([0, -0.9, 0])
        ban = button("Ban Member", RED_DEEP, RED).move_to([3.5, -0.9, 0])
        ban_glow = glow_rect(3.0, 0.95, 0.22, RED, layers=7, spread=0.12, peak=0.34).move_to(ban.get_center())
        missing = VGroup()
        for text in ("No manager", "No handbook", "No appeals form"):
            lab = T(text, 32, TEXT, "SEMIBOLD")
            x = cross(0.28, RED, 6)
            chip = rrect(lab.width + 1.0, 0.7, 0.35, "#2a1d2a", stroke=RED, sw=3)
            x.move_to(chip.get_left() + RIGHT * 0.4)
            lab.move_to(x.get_right() + RIGHT * (0.2 + lab.width / 2))
            missing.add(VGroup(chip, x, lab))
        missing.arrange(RIGHT, buff=0.4).move_to([0, -2.3, 0])
        for m in (profile, mute, kick, ban, ban_glow, missing):
            hide(m)
        self.add(profile, mute, kick, ban_glow, ban, missing, cr)

        self.hold_until(P.t("r1_profile"))
        self.play(Show(profile, shift=UP * 0.2), run_time=P.d("r1_profile"))
        self.at("r1_crown")
        self.play(cr.animate.move_to(rest), run_time=P.d("r1_crown"), rate_func=ease_out_bounce)
        self.play(name.animate.scale(1.05), run_time=0.15, rate_func=there_and_back)
        for i, b in enumerate((mute, kick, ban)):
            self.at(f"r1_btn{i}")
            extra = [Show(ban_glow)] if i == 2 else []
            self.play(Show(b, shift=UP * 0.25, pop=0.12), *extra, run_time=P.d(f"r1_btn{i}"))

        self.hold_until(P.t("n05_s2"))
        self.play(self.stagger_anim(list(missing), P.d("n05_s2"), make=lambda m: Show(m, shift=UP * 0.2, pop=0.15, run_time=0.35)),
                  run_time=P.d("n05_s2"))

        # the Ban Member button swells until it fills the screen, glowing
        self.at("r1_swell")
        full = rrect(15.2, 8.6, 0.05, RED_DEEP)
        ban.set_z_index(50)
        ban_glow.set_z_index(49)
        self.play(Transform(ban[0], full), ban[1].animate.scale(3.6).move_to([0, 0.15, 0]),
                  ban_glow.animate.scale(5.0).set_opacity(0),
                  Hide(profile), Hide(mute), Hide(kick), Hide(missing), run_time=P.d("r1_swell"), rate_func=lambda a: a ** 2.4)
        self.at("r1_out")
        self.play(Hide(ban), run_time=P.d("r1_out"))
        self.remove(profile, mute, kick, ban, ban_glow, missing, cr)

    # ---- reason 2: you only see the punishments ------------------------------------------------------
    def reason2(self):
        P = self.plan
        lp = rrect(5.8, 4.3, 0.25, HEADER, stroke=LINE, sw=3).move_to([-3.5, 0.15, 0])
        rp = rrect(5.8, 4.3, 0.25, HEADER, stroke=LINE, sw=3).move_to([3.5, 0.15, 0])
        lt = T("What members see", 40, TEXT, "SEMIBOLD").move_to([-3.5, 2.75, 0])
        rt = T("What mods do", 40, TEXT, "SEMIBOLD").move_to([3.5, 2.75, 0])
        divider = Line([0, 2.95, 0], [0, -2.1, 0]).set_stroke(LINE, width=4)
        corner = T("Illustrative, not real data", 25, MUTED, "MEDIUM", slant=ITALIC).move_to([6.75, 3.5, 0], aligned_edge=RIGHT)

        skeleton = VGroup()
        for i, y in enumerate((1.65, 1.05, 0.45)):
            skeleton.add(disc(0.17, "#2a2f45").move_to([-5.9 + 0.55, y, 0]),
                         rrect(2.6 - 0.3 * i, 0.14, 0.07, "#2a2f45").move_to([-4.3 + (2.6 - 0.3 * i) / 2 - 0.0, y + 0.1, 0]),
                         rrect(1.7 + 0.3 * i, 0.14, 0.07, "#242840").move_to([-4.3 + (1.7 + 0.3 * i) / 2, y - 0.16, 0]))
        banner = VGroup(rrect(4.7, 1.15, 0.22, RED_DEEP, stroke=RED, sw=4), avatar("J", PINK, 0.3).move_to([-1.95, 0, 0]),
                        T("BANNED", 66, WHITE, "HEAVY").move_to([0.35, 0, 0]))
        banner.move_to([-3.5, -0.8, 0])
        eyes = VGroup()
        for i, x in enumerate((-5.3, -4.4, -2.6, -1.7)):
            eyes.add(eye(0.38, (0.0, -1.0)).move_to([x, 0.05, 0]), eye(0.38, (0.0, 1.0)).move_to([x, -1.65, 0]))

        grid = VGroup(*[check_badge().move_to([1.0 + c * 0.66 + 0.33, 1.75 - r * 0.5, 0]) for r in range(4) for c in range(8)])
        order = [grid[i] for i in np.random.default_rng(4).permutation(len(grid))]
        legend = VGroup()
        for i, text in enumerate(("deleted spam", "blocked scam link", "calmed argument")):
            row = VGroup(check_badge(0.14), T(text, 27, "#c9cde0", "MEDIUM"))
            row[1].next_to(row[0], RIGHT, buff=0.2)
            legend.add(row.move_to([1.2 + row.width / 2, -0.28 - i * 0.5, 0]))
        flash = rrect(5.8, 4.3, 0.25, WHITE, opacity=0.95).move_to(lp.get_center())
        cam = camera_icon(0.75, WHITE).move_to([-1.05, 1.9, 0])
        for m in (lp, rp, lt, rt, divider, corner, skeleton, banner, eyes, grid, legend, flash, cam):
            hide(m)
        self.add(lp, rp, lt, rt, divider, corner, skeleton, grid, legend, banner, eyes, flash, cam)

        self.hold_until(P.t("r2_panels"))
        self.play(Show(lp, shift=RIGHT * 0.3), Show(rp, shift=LEFT * 0.3), Show(lt), Show(rt), Show(divider), Show(skeleton),
                  Show(corner), run_time=P.d("r2_panels"))
        # all beats run as one block so each lands on its cue (and on its sound effect)
        shot = Succession(AnimationGroup(Show(flash, run_time=0.08), Show(cam, pop=0.3, run_time=0.2)),
                          Hide(flash, run_time=P.d("r2_shot") - 0.28))
        self.run_block([
            (P.t("r2_legend"), self.stagger_anim(list(legend), P.d("r2_legend"),
                                                 make=lambda m: Show(m, shift=RIGHT * 0.15, run_time=0.4))),
            (P.t("r2_chkA"), self.stagger_anim(order[:14], P.d("r2_chkA"))),
            (P.t("r2_banned"), Show(banner, pop=0.22, shift=DOWN * 0.2, run_time=P.d("r2_banned"))),
            (P.t("r2_chkB"), self.stagger_anim(order[14:20], P.d("r2_chkB"))),
            (P.t("r2_eyes"), self.stagger_anim(list(eyes), P.d("r2_eyes"))),
            (P.t("r2_chkC"), self.stagger_anim(order[20:], P.d("r2_chkC"))),
            (P.t("r2_shot"), shot),
        ])
        self.at("r2_out")
        everything = VGroup(lp, rp, lt, rt, divider, corner, skeleton, banner, eyes, grid, legend, cam)
        self.play(Hide(everything), run_time=P.d("r2_out"))
        self.remove(lp, rp, lt, rt, divider, corner, skeleton, grid, legend, banner, eyes, flash, cam)

    # ---- reason 3: how mods get picked -----------------------------------------------------------------
    def reason3(self):
        P = self.plan
        card = rrect(5.4, 4.5, 0.28, HEADER, stroke=LINE, sw=3).move_to([-3.6, -0.15, 0])
        av = avatar("T", PURPLE, 0.72).move_to([-3.6, 1.15, 0])
        online = VGroup(disc(0.19, HEADER), disc(0.13, GREEN)).move_to(av.get_center() + np.array([0.55, -0.55, 0]))
        nm = T("Tyler | Moderator", 40, PURPLE, "SEMIBOLD").move_to([-3.6, 0.2, 0])
        mini_cal = VGroup(rrect(0.38, 0.34, 0.06, "#2c3250"), rrect(0.38, 0.12, 0.05, PURPLE_DEEP).shift(UP * 0.11))
        since = VGroup(mini_cal, T("Member since: 3 weeks ago", 31, TEXT, "MEDIUM"))
        since[1].next_to(since[0], RIGHT, buff=0.2)
        since.move_to([-3.6, -0.7, 0])
        chip = VGroup(rrect(1.8, 0.5, 0.25, PURPLE_DEEP), T("Moderator", 25, WHITE, "SEMIBOLD"))
        chip[1].move_to(chip[0].get_center())
        chip.move_to([-3.6, -1.55, 0])
        ok = VGroup(disc(0.24, "#1d5c44"), checkmark(0.26, GREEN, 5)).move_to(av.get_center() + np.array([-0.62, 0.55, 0]))
        profile = VGroup(card, av, online, nm, chip)

        friends = friend_group(r=0.44).move_to([3.7, 0.75, 0])
        rope = velvet_rope(5.0, 1.7).move_to([3.7, -0.2, 0])
        sign = T("the owner's friends", 30, MUTED, "MEDIUM").move_to([3.7, 2.45, 0])
        eyes = VGroup(*[eye(0.4, look).move_to(pos) for look, pos in [
            ((1, 0), [-6.55, 1.3, 0]), ((1, 0), [-6.55, -0.2, 0]), ((1, 0), [-6.55, -1.7, 0]),
            ((0, -1), [-5.4, 2.65, 0]), ((0, -1), [-3.6, 2.7, 0]), ((0, -1), [-1.8, 2.65, 0])]])
        for m in (profile, since, ok, friends, rope, sign, eyes):
            hide(m)
        self.add(profile, since, friends, rope, sign, ok, eyes)

        self.hold_until(P.t("r3_profile"))
        self.play(Show(profile, shift=RIGHT * 0.3), run_time=P.d("r3_profile"))
        self.at("r3_since")
        self.play(Show(since, shift=UP * 0.15), run_time=P.d("r3_since"))
        self.at("r3_rope")
        self.play(Show(sign), Show(friends, shift=LEFT * 0.4), Show(rope, shift=LEFT * 0.4), run_time=P.d("r3_rope"))
        self.at("r3_check")
        self.play(Show(ok, pop=0.5), run_time=P.d("r3_check"))
        self.hold_until(P.t("r3_eyes"))
        self.staggered(list(eyes), P.t("r3_eyes"), P.d("r3_eyes"))
        self.at("r3_out")
        everything = VGroup(profile, since, ok, friends, rope, sign, eyes)
        self.play(Hide(everything), run_time=P.d("r3_out"))
        self.remove(profile, since, ok, friends, rope, sign, eyes)

    # ---- reason 4: memes turn stories into a type ------------------------------------------------------
    def reason4(self):
        P = self.plan
        memes = [meme_hammer(), meme_grass(), meme_screenshot()]
        tilts = (-0.04, 0.035, -0.025)
        for m, a in zip(memes, tilts):
            m.scale(1.14).rotate(a).move_to([0, 0.1, 0])
        chip_a = VGroup(rrect(3.9, 0.62, 0.31, "#3a1d2a", stroke=RED, sw=3), T("strict mod = proof", 29, "#ffb4bf", "SEMIBOLD"))
        chip_b = VGroup(rrect(4.4, 0.62, 0.31, "#232845", stroke=MUTED, sw=3), T("kind mod = exception", 29, "#c9cde0", "SEMIBOLD"))
        for c in (chip_a, chip_b):
            c[1].move_to(c[0].get_center())
        chip_a.move_to([-3.4, -2.65, 0])
        chip_b.move_to([3.4, -2.65, 0])
        for m in (*memes, chip_a, chip_b):
            hide(m)
        self.add(*memes, chip_a, chip_b)

        self.at("r4_a")
        self.play(Show(memes[0], shift=DOWN * 0.4, pop=0.1), run_time=0.35)
        self.play(Shake(memes[0], amp=0.07, freq=70), run_time=0.45)
        self.at("r4_b")
        self.play(Show(memes[1], shift=UP * 0.3, pop=0.1), run_time=0.3)
        self.at("r4_c")
        self.play(Show(memes[2], shift=DOWN * 0.3, pop=0.1), run_time=0.3)
        self.at("r4_collage")
        spots = [([-4.35, 0.5, 0], 0.55, -0.1), ([0.0, 0.5, 0], 0.55, 0.03), ([4.35, 0.5, 0], 0.55, 0.09)]
        moves = [m.animate.scale(s).move_to(pos).rotate(rot) for m, (pos, s, rot) in zip(memes, spots)]
        self.play(*moves, Show(chip_a, shift=UP * 0.2), Show(chip_b, shift=UP * 0.2), run_time=P.d("r4_collage"), rate_func=smooth)
