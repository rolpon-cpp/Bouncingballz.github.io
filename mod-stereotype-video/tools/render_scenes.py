# Written by Claude Sonnet 5.5
"""Render the Manim scenes and check that each video is exactly as long as its audio.

Usage:
    python tools/render_scenes.py --quality test              # 854x480, 30 fps, all scenes
    python tools/render_scenes.py --quality final --jobs 4    # 1920x1080, 30 fps, 4 scenes at a time
    python tools/render_scenes.py --quality test --scenes 1   # only scene 1
Output: output/scenes/sceneN_<quality>.mp4
"""
import argparse
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modkit import config as C
from modkit.plans import get_plan

RES = {"test": C.RES_TEST, "final": C.RES_FINAL}


def count_frames(path: Path) -> int:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return int(out)


def render_one(number: int, quality: str) -> tuple:
    file_name, cls, _ = C.SCENES[number]
    w, h = RES[quality]
    media = C.MEDIA_DIR / quality / f"scene{number}"   # separate scratch folder per scene (parallel renders)
    logs = C.MEDIA_DIR / quality / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "manim", "render", str(C.SCENES_DIR / file_name), cls,
           "-r", f"{w},{h}", "--fps", str(C.FPS), "--media_dir", str(media),
           "--progress_bar", "none", "-v", "WARNING", "--disable_caching", "--output_file", f"scene{number}"]
    env = dict(os.environ, PYTHONPATH=str(C.ROOT))
    t0 = time.time()
    with open(logs / f"scene{number}.log", "w") as log:
        rc = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, cwd=str(C.ROOT)).returncode
    secs = time.time() - t0
    if rc != 0:
        return number, False, f"manim failed (exit {rc}), see {logs / f'scene{number}.log'}", secs
    produced = media / "videos" / Path(file_name).stem / f"{h}p{C.FPS}" / f"scene{number}.mp4"
    if not produced.exists():
        return number, False, f"missing output {produced}", secs
    C.CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    dest = C.CLIPS_DIR / f"scene{number}_{quality}.mp4"
    shutil.copy2(produced, dest)
    got, want = count_frames(dest), C.frames(get_plan(number).total)
    ok = got == want
    return number, ok, f"{got} frames, plan {want} frames ({'match' if ok else 'MISMATCH'})", secs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quality", choices=sorted(RES), default="test")
    ap.add_argument("--scenes", type=int, nargs="*", default=sorted(C.SCENES))
    ap.add_argument("--jobs", type=int, default=1, help="scenes rendered in parallel")
    args = ap.parse_args()
    failed = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for number, ok, msg, secs in pool.map(lambda n: render_one(n, args.quality), args.scenes):
            print(f"scene {number}: {'OK  ' if ok else 'FAIL'} {msg} [{secs / 60:.1f} min]", flush=True)
            failed += 0 if ok else 1
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
