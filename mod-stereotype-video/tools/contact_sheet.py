# Written by Claude Sonnet 5.5
"""Make a labelled contact sheet (grid of frames) from a video, for quick visual checks.

Usage:
    python tools/contact_sheet.py VIDEO OUT.png --times 1 4.5 9 --cols 3 --width 640
    python tools/contact_sheet.py VIDEO OUT.png --every 3 --cols 4
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def duration(video: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("--times", type=float, nargs="*")
    ap.add_argument("--every", type=float, default=None, help="one frame every N seconds")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--width", type=int, default=640)
    args = ap.parse_args()
    dur = duration(args.video)
    times = args.times or []
    if args.every:
        t = 0.2
        while t < dur - 0.05:
            times.append(round(t, 2))
            t += args.every
    times = [min(t, dur - 0.04) for t in times]
    font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 22)
    tiles = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, t in enumerate(times):
            f = Path(tmp) / f"f{i}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", args.video, "-frames:v", "1",
                            "-vf", f"scale={args.width}:-1", str(f)], check=True)
            im = Image.open(f).convert("RGB")
            d = ImageDraw.Draw(im)
            iw, ih = im.size
            d.rectangle([iw - 120, ih - 30, iw, ih], fill=(0, 0, 0))
            d.text((iw - 114, ih - 27), f"{t:6.2f}s", fill=(255, 220, 80), font=font)
            tiles.append(im)
    w, h = tiles[0].size
    rows = (len(tiles) + args.cols - 1) // args.cols
    sheet = Image.new("RGB", (w * args.cols + 4 * (args.cols + 1), h * rows + 4 * (rows + 1)), (40, 40, 40))
    for i, im in enumerate(tiles):
        r, c = divmod(i, args.cols)
        sheet.paste(im, (4 + c * (w + 4), 4 + r * (h + 4)))
    sheet.save(args.out)
    print(f"{len(tiles)} frames -> {args.out} ({sheet.size[0]}x{sheet.size[1]})")


if __name__ == "__main__":
    sys.exit(main())
