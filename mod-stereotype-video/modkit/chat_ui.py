# Written by Claude Sonnet 5.5
"""An invented dark chat-app UI ("Cozy Cat Hangout") built from Manim shapes.

All servers, channels and people are fictional. The layout and palette are original and do not copy
any real app. The window fills x from -6.9 to 6.9 and y from -3.05 to 3.9, which leaves the bottom
band of the 16:9 frame free for burned-in captions.
"""
import numpy as np
from manim import *

from .anims import Hide, Show, hide
from .characters import avatar
from .icons import cat_logo, dots3, speaker
from .theme import *

WIN_L, WIN_R, WIN_T, WIN_B = -6.9, 6.9, 3.9, -3.05
LEFT_W, RIGHT_W = 2.7, 3.0
CL, CR = WIN_L + LEFT_W, WIN_R - RIGHT_W        # centre panel edges
HEADER_H = 0.78
MSG_TOP0 = WIN_T - HEADER_H - 0.15
MSG_X0 = CL + 0.35
MSG_TEXT_X = MSG_X0 + 0.75
MSG_MAX_W = CR - 0.3 - MSG_TEXT_X
MENTION = "#8fb4ff"

MOD_LABEL_Y, MOD_ROW_Y = 3.4, 2.88
MEM_LABEL_Y, MEM_ROW_Y0, MEM_STEP = 1.95, 1.45, 0.6

# All invented. key -> display data
PEOPLE = {
    "TYLER": dict(name="Tyler | Moderator", short="Tyler", color=PURPLE, name_color=PURPLE, weight="SEMIBOLD"),
    "JESS": dict(name="Jess", short="Jess", color=PINK, name_color="#ffc2d3", weight="SEMIBOLD"),
    "MOCHI": dict(name="Mochi", short="Mochi", color=ORANGE, name_color="#ffd2a8", weight="SEMIBOLD"),
    "PIXEL": dict(name="Pixel", short="Pixel", color=BLUE, name_color="#bcdcff", weight="SEMIBOLD"),
    "ORBIT": dict(name="Orbit", short="Orbit", color=GREEN, name_color="#b4f0d2", weight="SEMIBOLD"),
    "BISCUIT": dict(name="Biscuit", short="Biscuit", color=YELLOW, name_color="#ffe9a0", weight="SEMIBOLD"),
    "NOVA": dict(name="Nova", short="Nova", color=TEAL, name_color="#a8efe6", weight="SEMIBOLD"),
    "PRIYA": dict(name="Priya | Moderator", short="Priya", color=TEAL, name_color=TEAL, weight="SEMIBOLD"),
}
DEFAULT_MEMBERS = ("JESS", "MOCHI", "PIXEL", "ORBIT", "BISCUIT", "NOVA")


def mention_colors(text):
    """Colour any #channel mention in a message."""
    toks = {t.strip(".,!?"): MENTION for t in text.split() if t.startswith("#") and len(t) > 1}
    return toks or None


class Message:
    """One chat message (avatar, name, text). Created hidden; reveal with Show and TypeText."""

    def __init__(self, chat, key, text, top):
        p = PEOPLE[key]
        r = 0.27
        self.key, self.top = key, top
        self.avatar = avatar(p["short"][0], p["color"], r).move_to([MSG_X0 + r, top - 0.33, 0])
        self.name = T(p["name"], 30, p["name_color"], p["weight"]).move_to([MSG_TEXT_X, top - 0.2, 0], aligned_edge=LEFT)
        self.text = T(wrap(text, 34, MSG_MAX_W), 34, TEXT, t2c=mention_colors(text)).move_to([MSG_TEXT_X, top - 0.5, 0], aligned_edge=UL)
        self.header = VGroup(self.avatar, self.name)
        self.group = VGroup(self.header, self.text)   # header must be a child, or animating it dissolves the chat
        self.height = 0.5 + self.text.height + 0.22
        hide(self.group)

    @property
    def bottom(self):
        return self.top - self.height


class ChatWindow(VGroup):
    """The whole window. Messages are added hidden with add_message; the scene reveals them."""

    def __init__(self, server="Cozy Cat Hangout", active="general", members=DEFAULT_MEMBERS, channel_hint="friendly chat, be kind", mod="TYLER"):
        super().__init__()
        self.mod = mod
        self.member_rows, self.member_order, self._removed = {}, [], {}
        self.msg_top = MSG_TOP0
        self.messages = []
        self._build_frame()
        self._build_left(server, active)
        self._build_center(active, channel_hint)
        self._build_right(members)

    # ---- construction ----------------------------------------------------------------------
    def _build_frame(self):
        cx, cy = (WIN_L + WIN_R) / 2, (WIN_T + WIN_B) / 2
        shadow = rrect(WIN_R - WIN_L + 0.3, WIN_T - WIN_B + 0.3, 0.3, "#05060a", opacity=0.55).move_to([cx, cy - 0.06, 0])
        self.base = rrect(WIN_R - WIN_L, WIN_T - WIN_B, 0.22, PANEL_DARK, stroke=LINE, sw=3).move_to([cx, cy, 0])
        self.centre = Rectangle(width=CR - CL, height=WIN_T - WIN_B - 0.05, fill_color=PANEL, fill_opacity=1, stroke_width=0)
        self.centre.move_to([(CL + CR) / 2, cy, 0])
        self.add(shadow, self.base, self.centre)

    def _build_left(self, server, active):
        top_band = Rectangle(width=LEFT_W, height=HEADER_H, fill_color="#14172a", fill_opacity=1, stroke_width=0)
        top_band.move_to([WIN_L + LEFT_W / 2, WIN_T - HEADER_H / 2 - 0.02, 0])
        logo = cat_logo(0.27).move_to([WIN_L + 0.5, WIN_T - HEADER_H / 2 - 0.02, 0])
        name = fit_width(T(server, 25, TEXT, "SEMIBOLD"), LEFT_W - 1.05).move_to([WIN_L + 0.9, WIN_T - HEADER_H / 2 - 0.02, 0], aligned_edge=LEFT)
        self.server_name = name
        self.add(top_band, logo, name)
        self.add(T("TEXT CHANNELS", 19, DIM, "SEMIBOLD").move_to([WIN_L + 0.35, 2.78, 0], aligned_edge=LEFT))
        for i, ch in enumerate(["rules", "announcements", "general", "memes", "support"]):
            y = 2.32 - i * 0.55
            if ch == active:
                self.add(rrect(LEFT_W - 0.4, 0.5, 0.1, "#262b45").move_to([WIN_L + LEFT_W / 2, y, 0]))
            self.add(T("# " + ch, 28, TEXT if ch == active else MUTED, "SEMIBOLD" if ch == active else "MEDIUM")
                     .move_to([WIN_L + 0.45, y, 0], aligned_edge=LEFT))
        self.add(T("VOICE", 19, DIM, "SEMIBOLD").move_to([WIN_L + 0.35, -0.72, 0], aligned_edge=LEFT))
        for i, v in enumerate(["Lounge", "Study Room"]):
            y = -1.2 - i * 0.55
            self.add(speaker(0.3, DIM).move_to([WIN_L + 0.58, y, 0]))
            self.add(T(v, 28, MUTED, "MEDIUM").move_to([WIN_L + 0.95, y, 0], aligned_edge=LEFT))

    def _build_center(self, active, hint):
        hdr = Rectangle(width=CR - CL, height=HEADER_H, fill_color=HEADER, fill_opacity=1, stroke_width=0)
        hdr.move_to([(CL + CR) / 2, WIN_T - HEADER_H / 2 - 0.02, 0])
        self.add(hdr)
        self.channel_title = T("# " + active, 32, TEXT, "BOLD").move_to([CL + 0.35, WIN_T - HEADER_H / 2 - 0.02, 0], aligned_edge=LEFT)
        self.add(self.channel_title)
        div = Line([CL + 0.35 + self.channel_title.width + 0.25, WIN_T - 0.28, 0], [CL + 0.35 + self.channel_title.width + 0.25, WIN_T - HEADER_H + 0.24, 0])
        div.set_stroke(LINE, width=3)
        self.add(div)
        self.add(T(hint, 24, DIM, "MEDIUM").move_to([div.get_x() + 0.25, WIN_T - HEADER_H / 2 - 0.02, 0], aligned_edge=LEFT))
        self.input_bar = rrect(CR - CL - 0.7, 0.62, 0.15, HEADER).move_to([(CL + CR) / 2, -2.65, 0])
        self.add(self.input_bar)
        self.placeholder = T("Message #" + active, 27, DIM, "MEDIUM").move_to([CL + 0.65, -2.65, 0], aligned_edge=LEFT)
        self.add(self.placeholder)
        # "is typing" line above the input bar (hidden until used)
        self.typing_line = VGroup(dots3(0.045, MUTED, 0.14), T(PEOPLE[self.mod]["name"] + " is typing...", 24, MUTED, "MEDIUM"))
        self.typing_line[1].next_to(self.typing_line[0], RIGHT, buff=0.18)
        self.typing_line.move_to([MSG_X0 + self.typing_line.width / 2 + 0.02, -2.08, 0])
        self.add(self.typing_line)
        hide(self.typing_line)

    def _build_right(self, members):
        panel = Rectangle(width=RIGHT_W, height=WIN_T - WIN_B - 0.05, fill_color=PANEL_DARK, fill_opacity=1, stroke_width=0)
        panel.move_to([CR + RIGHT_W / 2 - 0.01, (WIN_T + WIN_B) / 2, 0])
        edge = Line([CR, WIN_T - 0.15, 0], [CR, WIN_B + 0.15, 0]).set_stroke(LINE, width=3)
        self.add(panel, edge)
        self.add(T("MODERATOR", 19, DIM, "SEMIBOLD").move_to([CR + 0.35, MOD_LABEL_Y, 0], aligned_edge=LEFT))
        self.add(T("MEMBERS", 19, DIM, "SEMIBOLD").move_to([CR + 0.35, MEM_LABEL_Y, 0], aligned_edge=LEFT))
        self.tyler_row = self._member_row(self.mod, MOD_ROW_Y, mod=True)   # the moderator row (Tyler unless mod= is set)
        self.add(self.tyler_row)
        self.member_rows[self.mod] = self.tyler_row
        for i, k in enumerate(members):
            row = self._member_row(k, MEM_ROW_Y0 - i * MEM_STEP)
            self.add(row)
            self.member_rows[k] = row
            self.member_order.append(k)
        # typing indicator pill under Tyler's name (hidden until used)
        self.tyler_dots = dots3(0.04, "#cfd3ea", 0.15)
        pill = rrect(0.68, 0.27, 0.135, "#2a2f45")
        self.tyler_pill = VGroup(pill, self.tyler_dots)
        self.tyler_dots.move_to(pill.get_center())
        self.tyler_pill.move_to([CR + 0.45 + 0.38 + 0.4, MOD_ROW_Y - 0.4, 0])
        self.add(self.tyler_pill)
        hide(self.tyler_pill)

    def _member_row(self, key, y, mod=False):
        p = PEOPLE[key]
        av = avatar(p["short"][0], p["color"], 0.2).move_to([CR + 0.45, y, 0])
        dot = VGroup(disc(0.085, PANEL_DARK), disc(0.058, GREEN)).move_to(av.get_center() + np.array([0.15, -0.15, 0]))
        nm = T(p["name"], 28 if mod else 29, p["name_color"] if mod else "#c9cde0", "SEMIBOLD" if mod else "MEDIUM")
        fit_width(nm, RIGHT_W - 1.05)
        nm.move_to([CR + 0.85, y, 0], aligned_edge=LEFT)
        row = VGroup(av, dot, nm)
        row.name_mob = nm
        return row

    # ---- messages --------------------------------------------------------------------------
    def add_message(self, key, text):
        """Create a hidden message below the previous one and add it to the window."""
        m = Message(self, key, text, self.msg_top)
        self.msg_top = m.bottom - 0.04
        self.messages.append(m)
        self.add(m.group)
        return m

    def scroll_anims(self, dy, fade=(), extras=()):
        """Scroll the message list up by dy. Messages in `fade` fade out as they leave the top;
        `extras` are other mobjects (stamps and so on) that move with the messages."""
        anims = []
        for m in self.messages:
            if m in fade:
                anims.append(Hide(m.group, shift=UP * dy))
            else:
                anims.append(m.group.animate.shift(UP * dy))
        for e in extras:
            anims.append(e.animate.shift(UP * dy))
        self.msg_top += dy
        return anims

    # ---- members ---------------------------------------------------------------------------
    def remove_member_instant(self, key):
        """Take a member out of the list without animation (rows below slide up)."""
        idx = self.member_order.index(key)
        for k in self.member_order[idx + 1:]:
            self.member_rows[k].shift(UP * MEM_STEP)
        hide(self.member_rows[key])
        self.member_order.remove(key)
        self._removed[key] = idx

    def leave_anims(self, key, hide_row=True):
        """Animations for a member leaving: their row fades out (unless already hidden) and the rows below slide up."""
        idx = self.member_order.index(key)
        below = [self.member_rows[k] for k in self.member_order[idx + 1:]]
        self.member_order.remove(key)
        self._removed[key] = idx
        first = [Hide(self.member_rows[key], shift=LEFT * 0.3)] if hide_row else []
        return first + [b.animate.shift(UP * MEM_STEP) for b in below]

    def join_anims(self, key):
        """Animations for a member returning: rows below slide down and the row fades back in."""
        idx = self._removed.pop(key)
        below = [self.member_rows[k] for k in self.member_order[idx:]]
        self.member_order.insert(idx, key)
        return [Show(self.member_rows[key], shift=RIGHT * 0.3)] + [b.animate.shift(DOWN * MEM_STEP) for b in below]

    def row_center(self, key):
        return self.member_rows[key][0].get_center()
