# Written by Claude Sonnet 5.5
"""Parse script.md into structured data.

script.md is the single source of truth: narration text, typed chat lines, checklist items,
diagram labels and headings are all read from it, so on-screen text always matches the script.
"""
import re
from dataclasses import dataclass, field
from functools import lru_cache

from .config import SCRIPT_MD

_TAG = re.compile(r"^(VISUAL|SFX|TEXT(?: \([^)]*\))?|JESS|TYLER|NARRATOR):\s*(.*)$")
_SCENE = re.compile(r"^SCENE (\d+): (.+?) \((\d+:\d\d)-(\d+:\d\d)\)$")
_HEADING = re.compile(r"^((?:Reason|Beat) \d), (.+?)\.?$")
_CHECKLIST = re.compile(r"^If you (are a member|are a mod|run a server):\s*(.*)$")


@dataclass
class Item:
    kind: str          # VISUAL, SFX, TEXT, TEXT (corner), JESS, TYLER, NARRATOR, HEADING, CHECKLIST
    text: str
    label: str = ""    # HEADING: "Reason 1"; CHECKLIST: "are a member"


@dataclass
class Scene:
    number: int
    title: str
    start: str
    end: str
    items: list = field(default_factory=list)


@lru_cache(maxsize=1)
def parse_script() -> tuple:
    scenes, scene, cur = [], None, None
    for raw in SCRIPT_MD.read_text(encoding="utf-8").splitlines():
        m = _SCENE.match(raw)
        if m:
            scene = Scene(int(m.group(1)), m.group(2), m.group(3), m.group(4))
            scenes.append(scene)
            cur = None
            continue
        if scene is None:
            continue
        if not raw.strip():
            cur = None
            continue
        m = _TAG.match(raw)
        if m:
            cur = Item(m.group(1), m.group(2).strip())
            scene.items.append(cur)
            continue
        m = _HEADING.match(raw)
        if m:
            cur = Item("HEADING", m.group(2).strip(), label=m.group(1))
            scene.items.append(cur)
            continue
        m = _CHECKLIST.match(raw)
        if m:
            cur = Item("CHECKLIST", m.group(2).strip(), label=m.group(1))
            scene.items.append(cur)
            continue
        if cur is not None:  # continuation of a hard-wrapped line
            cur.text = (cur.text + " " + raw.strip()).strip()
    return tuple(scenes)


def scene(number: int) -> Scene:
    return next(s for s in parse_script() if s.number == number)


def narration_lines() -> list:
    """All NARRATOR lines in order: [{id, scene, index, text}], ids n01..n16."""
    out = []
    for s in parse_script():
        idx = 0
        for it in s.items:
            if it.kind == "NARRATOR":
                idx += 1
                out.append({"id": f"n{len(out) + 1:02d}", "scene": s.number, "index": idx, "text": it.text})
    return out


def chat_lines(number: int) -> list:
    """Typed chat lines of a scene in order: [(speaker, text)], speaker in {"TYLER", "JESS"}."""
    return [(it.kind, it.text) for it in scene(number).items if it.kind in ("TYLER", "JESS")]


def headings(number: int) -> list:
    """Untagged headings such as 'Reason 1, The tiny crown.' -> [("Reason 1", "The tiny crown")]."""
    return [(it.label, it.text) for it in scene(number).items if it.kind == "HEADING"]


def checklists() -> list:
    """Scene 5 checklist cards: [(title, [bullets])] with the first letter capitalised."""
    out = []
    for it in scene(5).items:
        if it.kind == "CHECKLIST":
            bullets = [b.strip().rstrip(".") for b in it.text.split(";") if b.strip()]
            bullets = [b[0].upper() + b[1:] for b in bullets]
            out.append(("If you " + it.label, bullets))
    return out


def loop_nodes() -> list:
    """Scene 4 loop diagram labels (the last label repeats the first, so it is dropped)."""
    visual = next(it for it in scene(4).items if it.kind == "VISUAL" and "loop diagram" in it.text)
    labels = re.findall(r'"([^"]+)"', visual.text)
    return labels[:-1] if labels[-1] == labels[0] else labels


def shift_events() -> list:
    """Scene 2 shift timeline: [(time_label, description)] such as ("7:00 AM", "report about ...")."""
    visual = next(it for it in scene(2).items if it.kind == "VISUAL" and "timeline" in it.text)
    body = visual.text.split("notification bubbles:", 1)[1].strip()
    parts = re.split(r"(?=\b\d{1,2}:\d\d [AP]M\b)", body)
    out = []
    for p in parts:
        m = re.match(r"(\d{1,2}:\d\d [AP]M) (.+?)\.?$", p.strip())
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def sentences(text: str) -> list:
    """Split narration into sentences (a split needs end punctuation, a space and a capital letter)."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if s.strip()]


if __name__ == "__main__":
    for line in narration_lines():
        print(line["id"], "scene", line["scene"], len(sentences(line["text"])), "sentences:", line["text"][:60])
    print("chat s1:", chat_lines(1))
    print("chat s6:", chat_lines(6))
    print("headings s3:", headings(3))
    print("headings s4:", headings(4))
    print("loop:", loop_nodes())
    print("shift:", shift_events())
    for t, b in checklists():
        print(t, b)
