# Written by Claude Sonnet 5.5
"""Step 5 helper: cut a short test clip (video plus its mixed audio) from a rendered scene.

Usage: python tools/make_test_clip.py [--scene 1] [--seconds 10] [--quality test]
Output: output/test/scene1_<quality>_<seconds>s.mp4
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modkit import config as C


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scene", type=int, default=1)
    ap.add_argument("--seconds", type=float, default=10.0)
    ap.add_argument("--quality", default="test")
    args = ap.parse_args()
    video = C.CLIPS_DIR / f"scene{args.scene}_{args.quality}.mp4"
    audio = C.SCENE_AUDIO_DIR / f"scene{args.scene}.wav"
    C.TEST_DIR.mkdir(parents=True, exist_ok=True)
    out = C.TEST_DIR / f"scene{args.scene}_{args.quality}_{int(args.seconds)}s.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(audio), "-t", str(args.seconds),
           "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
