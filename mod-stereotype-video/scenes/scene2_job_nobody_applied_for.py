# Written by Claude Sonnet 5.5
"""Scene 2: THE JOB NOBODY APPLIED FOR.

Zoom out from Tyler's name to a calendar, a mod's "shift" timeline with four notification bubbles,
a phone buzzing on a dark desk with a tired hand reaching for it, then four face-down cards fan out.
"""
import numpy as np
from manim import *

from modkit.anims import Hide, Show, Shake, hide
from modkit.base_scene import TimedScene
from modkit.characters import hand_tired
from modkit.icons import bell, cat_logo, chat_icon, clock, crown, shield, speaker, warning
from modkit.props import FAN_ANGLES, FAN_PIVOT, calendar_panel, desk_lamp, make_fan, mug, phone, speech_bubble
from modkit.script_data import shift_events
from modkit.theme import *


class JobNobodyAppliedFor(TimedScene):
    SCENE_NO = 2

    def construct(self):
        self.calendar_part()
        self.timeline_part()
        self.phone_part()
        self.cards_part()
        self.finish()

    # ---- helpers ---------------------------------------------------------------------------------
    # ---- 1. calendar --------------------------------------------------------------------------
    def calendar_part(self):
        P = self.plan
        cal = calendar_panel(9.2, 5.3).move_to([0, -0.35, 0])
        name = T("Tyler | Moderator", 33, PURPLE, "SEMIBOLD").move_to([-3.4, 3.2, 0])
        world = VGroup(cal, name)
        final_state = world.copy()
        z0 = HANDOFF_PX / 33
        pivot = name.get_center().copy()
        world.scale(z0, about_point=pivot).shift(HANDOFF_POS - pivot)   # start exactly where Scene 1 ended
        hide(cal)
        self.add(world)
        self.hold_until(P.t("zoom"))
        self.play(Transform(world, final_state), rate_func=zoom_rate(1 / z0), run_time=P.d("zoom"))

        def badge(icon):
            back = disc(0.78, "#1b1f30", stroke=LINE, sw=3)
            icon.move_to(back.get_center())
            return VGroup(back, icon)

        shield_i, clock_i, bell_i = shield(1.0), clock(1.0), bell(1.0)
        icons = [badge(shield_i).move_to([-4.6, 2.3, 0]), badge(clock_i).move_to([-4.6, -2.8, 0]),
                 badge(bell_i).move_to([4.6, -2.8, 0])]
        for ic in icons:
            hide(ic)
            self.add(ic)
        for i, ic in enumerate(icons):
            self.hold_until(P.t(f"icon{i}"))
            self.play(Show(ic, pop=0.4), run_time=P.d(f"icon{i}"))

        chip = VGroup(rrect(1.85, 0.5, 0.25, PURPLE_DEEP), T("Moderator", 25, WHITE, "SEMIBOLD"))
        chip[1].move_to(chip[0].get_center())
        chip.next_to(name, RIGHT, buff=0.3)
        owner_logo = cat_logo(0.34)
        owner = VGroup(owner_logo, crown(0.34).move_to(owner_logo.get_top() + UP * 0.12)).move_to([4.7, 3.1, 0])
        bubble = speech_bubble("keep it clean.", 28, tail=1, stroke=ORANGE).move_to([2.85, 3.2, 0])
        extras = [chip, owner, bubble]
        for m in extras:
            hide(m)
            self.add(m)

        cells, nums = cal.cells[:30], cal.nums
        sweep = LaggedStart(*[AnimationGroup(cells[i].animate.set_fill(PURPLE_DEEP, 0.9), nums[i].animate.set_color(WHITE))
                              for i in range(30)], lag_ratio=0.1)
        c = clock_i.get_center()
        spin = AnimationGroup(Rotate(clock_i.hand_min, angle=TAU * 3, about_point=c, rate_func=smooth),
                              Rotate(clock_i.hand_hour, angle=TAU / 4, about_point=c, rate_func=smooth))
        sweep.run_time = P.d("sweep")
        spin.run_time = P.d("clock_spin")
        shield_pulse = ScaleInPlace(icons[0], 1.3, rate_func=there_and_back, run_time=P.d("shield_pulse"))
        ring = Wiggle(icons[2], scale_value=1.12, rotation_angle=0.06 * TAU, n_wiggles=6,
                      rotate_about_point=icons[2].get_top(), run_time=P.d("bell"))
        self.run_block([
            (P.t("sweep"), sweep),
            (P.t("shield_pulse"), shield_pulse),
            (P.t("clock_spin"), spin),
            (P.t("role"), Show(chip, pop=0.3, run_time=P.d("role"))),
            (P.t("keep"), AnimationGroup(Show(owner, pop=0.3), Show(bubble, pop=0.2, shift=DOWN * 0.1), run_time=P.d("keep"))),
            (P.t("bell"), ring),
        ])
        self.at("cal_out")
        everything = VGroup(world, *icons, *extras)
        self.play(Hide(everything), run_time=P.d("cal_out"))
        self.remove(everything)

    # ---- 2. shift timeline ------------------------------------------------------------------------
    def timeline_part(self):
        P = self.plan
        events = shift_events()
        u, x0, x1, ay = 11.6 / 24, -5.8, 5.8, -0.2
        title = T('A mod\'s "shift"', 46, TEXT, "BOLD").move_to([-6.45, 3.3, 0], aligned_edge=LEFT)
        axis = rstroke(Line([x0, ay, 0], [x1, ay, 0]), "#3a4060", 8)
        ticks, labels = VGroup(), VGroup()
        for i, h in enumerate(["6 AM", "9 AM", "12 PM", "3 PM", "6 PM", "9 PM", "12 AM", "3 AM", "6 AM"]):
            x = x0 + i * 3 * u
            ticks.add(Line([x, ay - 0.14, 0], [x, ay + 0.14, 0]).set_stroke("#3a4060", width=4))
            lab = T(h, 22, DIM, "MEDIUM").move_to([x, ay - 0.45, 0])
            pad = rrect(lab.width + 0.16, lab.height + 0.12, 0.06, "#141a3c" if i >= 6 else INK).move_to(lab.get_center())
            labels.add(VGroup(pad, lab))
        night_x0 = x0 + 18 * u
        night = Rectangle(width=x1 - night_x0, height=1.0, fill_color="#141a3c", fill_opacity=0.95, stroke_width=0)
        night.move_to([(x1 + night_x0) / 2, ay, 0])
        moon = VGroup(disc(0.17, "#f3f1d8"), disc(0.15, "#141a3c").shift(RIGHT * 0.08 + UP * 0.05)).move_to([(x1 + night_x0) / 2, ay + 0.32, 0])
        base = VGroup(night, moon, axis, ticks, labels)

        accents = [BLUE, YELLOW, GREEN, RED]
        icon_makers = [lambda: chat_icon(0.62, BLUE), lambda: warning(0.62), lambda: speaker(0.62, GREEN),
                       lambda: bell(0.62, RED, RED_DEEP)]
        centres = [(-4.1, 1.7), (-1.9, -2.0), (1.0, 1.7), (3.95, -2.0)]
        hours = [1.0, 6.5, 10.75, 21.2]
        bubbles, links, xs = [], [], []
        for i, ((time, desc), acc) in enumerate(zip(events, accents)):
            desc = desc[0].upper() + desc[1:]
            tt = T(time, 32, acc, "BOLD")
            dd = T(wrap(desc, 28, 2.75, "MEDIUM"), 28, TEXT, "MEDIUM", line_spacing=0.95)
            w, h = 4.15, max(1.45, 0.3 + tt.height + 0.14 + dd.height + 0.3)
            box = rrect(w, h, 0.22, "#1b1f30", stroke=acc, sw=4)
            ic = icon_makers[i]().move_to([-w / 2 + 0.55, 0, 0])
            tt.move_to([-w / 2 + 1.1, h / 2 - 0.3 - tt.height / 2, 0], aligned_edge=LEFT)
            dd.move_to([-w / 2 + 1.1, tt.get_bottom()[1] - 0.14, 0], aligned_edge=UL)
            bub = VGroup(box, ic, tt, dd).move_to([centres[i][0], centres[i][1], 0])
            xa = x0 + hours[i] * u
            xs.append(xa)
            edge_y = bub.get_bottom()[1] if centres[i][1] > 0 else bub.get_top()[1]
            link = VGroup(Line([xa, ay, 0], [xa, edge_y, 0]).set_stroke(acc, width=4), disc(0.1, acc).move_to([xa, ay, 0]))
            bubbles.append(bub)
            links.append(link)

        glow = glow_disc(0.22, PURPLE, layers=5, spread=0.06, peak=0.25)
        marker = VGroup(glow, disc(0.14, WHITE)).move_to([x0, ay, 0])
        progress = rstroke(Line([x0, ay, 0], [x0 + 0.001, ay, 0]), PURPLE, 8)
        for m in [title, base, *bubbles, *links, marker, progress]:
            hide(m)
        self.add(night, moon, axis, progress, ticks, *links, labels, marker, *bubbles, title)
        # (add order puts bubbles and marker above the axis)

        self.hold_until(P.t("tl_in"))
        self.play(Show(title, shift=RIGHT * 0.3), Show(base), run_time=P.d("tl_in"))
        self.at("marker0")
        self.play(Show(marker), run_time=0.3)
        self.play(marker.animate.move_to([xs[0], ay, 0]), progress.animate.put_start_and_end_on([x0, ay, 0], [xs[0], ay, 0]),
                  run_time=P.d("marker0") - 0.3, rate_func=smooth)

        def pop(i, extra=()):
            sgn = DOWN if centres[i][1] < 0 else UP
            self.play(Show(links[i]), Show(bubbles[i], shift=-sgn * 0.25, pop=0.08), *extra, run_time=P.d(f"b{i + 1}"))

        def travel(i, until):
            """Marker runs from event i to event i+1, arriving exactly when that bubble starts."""
            run = until - self.now
            if run > 0.05:
                self.play(marker.animate.move_to([xs[i + 1], ay, 0]),
                          progress.animate.put_start_and_end_on([x0, ay, 0], [xs[i + 1], ay, 0]),
                          run_time=run, rate_func=linear)

        self.at("b1")
        pop(0)
        for i in range(1, 4):
            travel(i - 1, P.t(f"b{i + 1}"))
            self.at(f"b{i + 1}")
            pop(i, extra=(night.animate.set_fill("#1d1136", 1.0), marker.animate.set_color(RED)) if i == 3 else ())
        self.at("tl_out")
        group = VGroup(title, base, *bubbles, *links, marker, progress)
        self.play(Hide(group), run_time=P.d("tl_out"))
        self.remove(*group)

    # ---- 3. bedroom desk --------------------------------------------------------------------------
    def phone_part(self):
        P = self.plan
        desk = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1, fill_color="#10131c", fill_opacity=1, stroke_width=0)
        grain = VGroup(*[Line([-7.5, y, 0], [7.5, y + 0.15, 0]).set_stroke("#151926", width=3) for y in np.arange(-3.9, 4.0, 0.62)])
        moonlight = Polygon([-7.3, 4.2, 0], [-3.4, 4.2, 0], [1.5, -4.2, 0], [-2.4, -4.2, 0], fill_color="#6f8fe0", fill_opacity=0.05, stroke_width=0)
        keyboard = rrect(5.4, 1.5, 0.2, "#161a27", stroke="#232844", sw=3).move_to([-3.0, 2.5, 0])
        keys = VGroup(*[rrect(0.32, 0.26, 0.05, "#1d2235").move_to([-5.4 + c * 0.42, 2.9 - r * 0.38, 0]) for r in range(3) for c in range(12)])
        cup = mug(1.0, "#cfc8ff").move_to([5.4, 2.7, 0])
        lamp = desk_lamp(1.9).move_to([6.2, -2.6, 0])
        scene_bg = VGroup(desk, grain, moonlight, keyboard, keys, cup, lamp)

        # phone, its screen glow and the notification are built unrotated, then placed together
        ph = phone(3.9)
        phone_glow = glow_rect(1.95, 3.9, 0.35, BLUE, layers=7, spread=0.14, peak=0.2)
        notif = VGroup(
            T("3:12 AM", 40, WHITE, "BOLD").move_to(ph.screen.get_top() + DOWN * 0.7),
            rrect(1.62, 0.78, 0.14, "#2b3358").move_to(ph.screen.get_center() + UP * 0.25),
        )
        card = notif[1]
        notif.add(cat_logo(0.17).move_to(card.get_left() + RIGHT * 0.26),
                  T("Cozy Cat Hangout", 18, WHITE, "SEMIBOLD").move_to(card.get_center() + np.array([0.3, 0.14, 0])),
                  T("14 new mentions", 18, MUTED, "MEDIUM").move_to(card.get_center() + np.array([0.24, -0.15, 0])))
        c0, tilt, spot = ph.get_center(), np.radians(-10), np.array([-0.6, -0.15, 0])
        for m in (ph, phone_glow, notif):
            m.rotate(tilt, about_point=c0).shift(spot - c0)
        hide(phone_glow)
        hide(notif)

        # the hand: palm centre is the origin, fingers point left, sleeve runs off to the right
        hand = hand_tired().scale(1.55, about_point=ORIGIN).rotate(PI / 2, about_point=ORIGIN).shift(np.array([10.0, -0.9, 0]))

        hide(scene_bg)
        hide(ph)
        self.add(scene_bg, phone_glow, ph, hand)
        self.hold_until(P.t("phone_in"))
        self.play(Show(scene_bg), Show(ph), run_time=P.d("phone_in"))

        self.at("buzz1")
        ph.add(notif)
        self.play(Show(notif), Show(phone_glow), Shake(ph, amp=0.05, freq=140, decay_pow=0), run_time=P.d("buzz1"))
        self.at("buzz2")
        self.play(Shake(ph, amp=0.05, freq=140, decay_pow=0), run_time=P.d("buzz2"))

        self.at("hand")
        self.play(hand.animate.shift(np.array([2.15 - 10.0, -0.5 + 0.9, 0])), run_time=P.d("hand"), rate_func=smooth)
        self.at("drag")
        self.play(hand.animate.shift(np.array([-0.5, -0.2, 0])), run_time=0.7, rate_func=smooth)
        move = np.array([1.6, -0.9, 0])
        self.play(hand.animate.shift(move), ph.animate.shift(move), phone_glow.animate.shift(move),
                  run_time=P.d("drag") - 0.7, rate_func=smooth)
        self.at("phone_out")
        bed = VGroup(scene_bg, phone_glow, ph, hand)
        self.play(Hide(bed), run_time=P.d("phone_out"))
        self.remove(scene_bg, phone_glow, ph, hand)

    # ---- 4. the four cards ------------------------------------------------------------------------
    def cards_part(self):
        P = self.plan
        cards = make_fan(fanned=False)
        hide(cards)
        self.add(cards)
        self.at("fan")
        self.play(Show(cards, run_time=0.25))
        spread = LaggedStart(*[Rotate(c, angle=np.radians(a), about_point=FAN_PIVOT, rate_func=ease_out_back)
                               for c, a in zip(cards, FAN_ANGLES)], lag_ratio=0.18)
        self.play(spread, run_time=P.d("fan") - 0.25)
