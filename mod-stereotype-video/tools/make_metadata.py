# Written by Claude Sonnet 5.5
"""Step 8: write output/title.txt, output/description.txt and output/tags.txt.

Chapter timestamps are computed from the real durations of the rendered scene clips (ffprobe) plus the
cue times in each scene's plan, so they match the final video. Chapters must be at least 10 s long and
the first must be 0:00 (YouTube rules); both are asserted.
Usage: python tools/make_metadata.py
"""
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modkit import config as C
from modkit.plans import get_plan
from modkit.script_data import headings


def clip_seconds(n: int) -> float:
    clip = C.CLIPS_DIR / f"scene{n}_final.mp4"
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0", str(clip)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def mmss(t: float) -> str:
    t = max(0, math.ceil(t - 0.02))     # round up, so a chapter never starts inside the previous scene
    return f"{t // 60}:{t % 60:02d}"


def chapters():
    starts, t = {}, 0.0
    for n in sorted(C.SCENES):
        starts[n] = t
        t += clip_seconds(n)
    total = t
    p3, p4, p5 = get_plan(3), get_plan(4), get_plan(5)
    reasons = {k: title for k, (_, title) in enumerate(headings(3), 1)}
    beats = {k: title for k, (_, title) in enumerate(headings(4), 1)}
    rows = [
        (0.0, "Cold open: the mod everyone knows"),
        (starts[2], C.SCENES[2][2]),
        (starts[3], f"Reason 1: {reasons[1]}"),
        (starts[3] + p3.t("r2_appear"), f"Reason 2: {reasons[2]}"),
        (starts[3] + p3.t("r3_appear"), f"Reason 3: {reasons[3]}"),
        (starts[3] + p3.t("r4_appear"), f"Reason 4: {reasons[4]}"),
        (starts[4], C.SCENES[4][2]),
        (starts[4] + p4.t("b1_title"), beats[1]),
        (starts[4] + p4.t("b2_title"), beats[2]),
        (starts[4] + p4.t("b3_title"), beats[3]),
        (starts[4] + p4.t("b4_title"), beats[4]),
        (starts[5], C.SCENES[5][2]),
        (starts[5] + p5.t("card0"), "What to do: members, mods and server owners"),
        (starts[6], "Closing: the unban"),
    ]
    assert rows[0][0] == 0.0
    for (a, _), (b, name) in zip(rows, rows[1:] + [(total, "end")]):
        assert b - a >= 10.0, f"chapter at {mmss(a)} is only {b - a:.1f} s long"
    return rows, total


TITLES = [
    "Why Discord Mods Got The Stereotype",
    "Why Everyone Thinks Discord Mods Are Power-Hungry",
    "The Real Reason Discord Mods Have a Bad Reputation",
]

TAGS = [
    "discord mods", "discord moderators", "discord moderation", "moderator stereotype", "power tripping mods",
    "discord mod abuse", "volunteer moderators", "online communities", "community moderation", "internet culture",
    "discord server", "discord drama", "mod burnout", "discord explained", "animated explainer",
    "community management", "discord ban appeal", "how to appeal a ban", "tips for discord mods", "mod stereotype memes",
]


def main():
    rows, total = chapters()
    out = C.OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    (out / "title.txt").write_text("\n".join(f"{i}. {t}" for i, t in enumerate(TITLES, 1)) + "\n", encoding="utf-8")

    chap = "\n".join(f"{mmss(t)} {name}" for t, name in rows)
    desc = f"""Why do Discord moderators have a reputation for power-tripping? This short animated story follows one strict mod, one banned member and one quiet 3 a.m. cleanup to show where the stereotype comes from, why it keeps feeding itself, and what members, mods and server owners can do about it.

CHAPTERS
{chap}

IN THIS VIDEO
- Most Discord moderators are unpaid volunteers
- Four reasons the stereotype exists: the tiny crown, you only see the punishments, how mods get picked, and memes
- Why the stereotype feeds itself: no training, no appeal, burnout
- Quick checklists for members, mods and server owners

Got a mod story? Comment it. No names please.

{C.DESCRIPTION_LINE}

CREDITS AND NOTES
- Video made with {C.MODEL_NAME}, using Manim, ffmpeg and Pillow. All art is original and drawn in code.
- Narration is a synthetic voice (Piper text-to-speech, public-domain voice {C.VOICE_NAME}).
- Sound effects are synthesized. No music is used.
- Graphics marked "Illustrative, not real data" are examples, not statistics.
- Not affiliated with or endorsed by Discord. Discord is a trademark of its owner.

#Discord #Moderators #OnlineCommunities
"""
    (out / "description.txt").write_text(desc, encoding="utf-8")
    tags = ", ".join(TAGS)
    assert len(tags) <= 500, len(tags)
    (out / "tags.txt").write_text(tags + "\n", encoding="utf-8")
    print(f"video length {mmss(total)} ({total:.1f} s); {len(rows)} chapters; tags {len(tags)} characters")
    print(chap)


if __name__ == "__main__":
    main()
