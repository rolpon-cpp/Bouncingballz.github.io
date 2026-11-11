# Written by Claude Sonnet 5.5
"""Check the project against the rules it was built under. Exit status 1 if anything fails.

Rules checked
  1. no em dash or en dash in any code, script, caption or metadata file (so none can reach the screen)
  2. every code file starts with the line "# Written by <model name>"
  3. the description contains the required sentence about the script and fictional characters
  4. the final video frame shows the credit line (checked on output/final_last_frame.png by pixel count)
  5. the credit text in the config is exactly the requested wording
Usage: python tools/lint_text.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

from modkit import config as C

ROOT = C.ROOT
BAD = (chr(0x2014), chr(0x2013))          # em dash and en dash, built from code points


def files(patterns):
    for pat in patterns:
        for p in sorted(ROOT.glob(pat)):
            if ".venv" in p.parts or "media" in p.parts or "__pycache__" in p.parts:
                continue
            yield p


def main() -> int:
    fails = []
    text_files = list(files(["*.md", "*.sh", "*.txt", "modkit/**/*.py", "scenes/*.py", "tools/*.py", "output/*.txt", "output/captions.*"]))
    for p in text_files:
        s = p.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(s.splitlines(), 1):
            if any(ch in line for ch in BAD):
                fails.append(f"dash character in {p.relative_to(ROOT)}:{i}")
    for p in files(["modkit/**/*.py", "scenes/*.py", "tools/*.py", "*.sh"]):
        first = p.read_text(encoding="utf-8").splitlines()[:1]
        if not first or first[0].strip().lstrip("#").strip() != C.SIGNATURE:
            fails.append(f"missing signature line in {p.relative_to(ROOT)}")
    desc = ROOT / "output" / "description.txt"
    if desc.exists():
        if C.DESCRIPTION_LINE not in desc.read_text(encoding="utf-8"):
            fails.append("description.txt lacks the required sentence")
    else:
        fails.append("output/description.txt not found")
    if C.CREDIT_LINE != "Script and video made with " + C.MODEL_NAME:
        fails.append("CREDIT_LINE wording")
    last = ROOT / "output" / "final_last_frame.png"
    if last.exists():
        im = Image.open(last).convert("L")
        w, h = im.size
        box = im.crop((int(w * 0.55), int(h * 0.9), w, h))           # bottom-right corner, where the credit sits
        bright = sum(1 for v in box.getdata() if v > 150)
        if bright < 400:
            fails.append(f"credit line not detected in the last frame ({bright} bright pixels)")
        else:
            print(f"credit line present in the last frame ({bright} bright pixels in the corner)")
    else:
        fails.append("output/final_last_frame.png not found (run tools/assemble.py)")
    checked = len(text_files)
    if fails:
        print("\n".join("FAIL " + f for f in fails))
        return 1
    print(f"all checks passed ({checked} text files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
