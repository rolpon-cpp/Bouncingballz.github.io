# Written by Claude Sonnet 5.5
"""Build burned-in captions for the narrator from the real narration timings.

Each narrator sentence has exact start and end times (see audio/narration/narration.json). Sentences are
wrapped to at most two lines; a very long sentence is split into several cues whose times are shared out
by character count. Writes output/captions.ass (styled, burned in by tools/assemble.py) and
output/captions.srt (for uploading to YouTube as a caption track).
Typed chat lines are already on screen, so only the NARRATOR is captioned.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modkit import config as C
from modkit.plans import get_plan

MAX_LINE = 54            # characters per caption line
MAX_LINES = 2


def scene_offsets() -> dict:
    """Start time (seconds) of each scene in the final video, from exact frame counts."""
    off, t = {}, 0
    for n in sorted(C.SCENES):
        off[n] = t / C.FPS
        t += C.frames(get_plan(n).total)
    return off


def wrap_two_lines(text: str):
    """Split text into chunks of at most MAX_LINES lines of MAX_LINE characters (greedy at spaces)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > MAX_LINE:
            lines.append(cur)
            cur = w
        else:
            cur = w if not cur else cur + " " + w
    if cur:
        lines.append(cur)
    chunks = [lines[i:i + MAX_LINES] for i in range(0, len(lines), MAX_LINES)]
    return ["\n".join(c) for c in chunks]


def build_cues() -> list:
    off = scene_offsets()
    cues = []
    for n in sorted(C.SCENES):
        plan = get_plan(n)
        for kind, clip_id, t0, _ in plan.audio:
            if kind != "narr":
                continue
            clip = plan.narr[clip_id]
            for sent in clip["sentences"]:
                a = off[n] + t0 + sent["start"]
                b = off[n] + t0 + sent["end"]
                chunks = wrap_two_lines(sent["text"])
                total = sum(len(c.replace("\n", " ")) for c in chunks)
                pos = a
                for c in chunks:
                    share = (b - a) * len(c.replace("\n", " ")) / total
                    cues.append([pos, pos + share, c])
                    pos += share
    cues.sort(key=lambda c: c[0])
    for i, c in enumerate(cues):                      # hold a caption slightly past the last word, never overlapping
        nxt = cues[i + 1][0] if i + 1 < len(cues) else c[1] + 1.0
        c[1] = min(c[1] + 0.25, nxt - 0.02)
        c[0] = max(0.0, c[0] - 0.05)
    return cues


def ts_srt(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def ts_ass(t: float) -> str:
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter SemiBold,44,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3.4,1.2,2,120,120,34,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def main():
    cues = build_cues()
    C.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    srt = []
    ass = [ASS_HEADER]
    for i, (a, b, text) in enumerate(cues, 1):
        srt.append(f"{i}\n{ts_srt(a)} --> {ts_srt(b)}\n{text}\n")
        ass.append(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},Default,,0,0,0,,{text.replace(chr(10), chr(92) + 'N')}")
    (C.OUTPUT_DIR / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    (C.OUTPUT_DIR / "captions.ass").write_text("\n".join(ass) + "\n", encoding="utf-8")
    print(f"{len(cues)} caption cues, first at {cues[0][0]:.2f}s, last ends {cues[-1][1]:.2f}s")
    longest = max(len(c[2].split("\n")[0]) for c in cues)
    print(f"longest caption line: {longest} characters")


if __name__ == "__main__":
    main()
