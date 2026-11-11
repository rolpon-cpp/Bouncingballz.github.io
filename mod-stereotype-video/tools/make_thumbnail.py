# Written by Claude Sonnet 5.5
"""Step 7: 1280 x 720 PNG thumbnail drawn with Pillow (no outside images).

A smug purple-named cartoon mod with a tiny crown holding a giant gavel, big text "BANNED?!", on a dark
blurred chat-window background. A small credit line is in the corner (use --no-watermark to leave it off).
Usage: python tools/make_thumbnail.py [--no-watermark]
Output: output/thumbnail.png
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import thumb_character as tc
from modkit import config as C

W, H, S = 1280, 720, tc.S
BOLD = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"


def font(path, size):
    return ImageFont.truetype(path, tc.sc(size))


def background():
    """Vertical gradient plus a blurred, dark chat-window with invented members, then a purple glow."""
    size = (W * S, H * S)
    base = Image.new("RGBA", size)
    px = base.load()
    for y in range(size[1]):
        t = y / size[1]
        col = (int(11 + 20 * t), int(13 + 8 * t), int(26 + 28 * t), 255)
        for x in range(size[0]):
            px[x, y] = col
    ui = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ui)
    d.rounded_rectangle([tc.sc(26), tc.sc(26), tc.sc(W - 26), tc.sc(H - 26)], radius=tc.sc(28), fill=(21, 24, 38, 255))
    d.rectangle([tc.sc(26), tc.sc(26), tc.sc(250), tc.sc(H - 26)], fill=(14, 16, 26, 255))
    d.rectangle([tc.sc(1030), tc.sc(26), tc.sc(W - 26), tc.sc(H - 26)], fill=(14, 16, 26, 255))
    colors = [(255, 122, 156), (255, 159, 69), (90, 169, 255), (57, 217, 138), (255, 210, 63), (45, 212, 191)]
    for i in range(8):
        y = 60 + i * 80
        c = colors[i % 6]
        tc.ellipse(d, 300, y + 28, 26, 26, c + (255,))
        d.rounded_rectangle([tc.sc(345), tc.sc(y + 6), tc.sc(345 + 120 + (i * 37) % 90), tc.sc(y + 22)], radius=tc.sc(8), fill=c + (255,))
        d.rounded_rectangle([tc.sc(345), tc.sc(y + 34), tc.sc(345 + 300 + (i * 71) % 260), tc.sc(y + 50)], radius=tc.sc(8), fill=(70, 78, 112, 255))
        d.rounded_rectangle([tc.sc(345), tc.sc(y + 58), tc.sc(345 + 200 + (i * 53) % 220), tc.sc(y + 72)], radius=tc.sc(8), fill=(52, 58, 88, 255))
    for i in range(7):
        c = colors[i % 6]
        tc.ellipse(d, 1075, 90 + i * 70, 20, 20, c + (255,))
        d.rounded_rectangle([tc.sc(1110), tc.sc(80 + i * 70), tc.sc(1110 + 80 + (i * 19) % 50), tc.sc(98 + i * 70)], radius=tc.sc(8), fill=(88, 96, 130, 255))
    for i in range(6):
        d.rounded_rectangle([tc.sc(60), tc.sc(100 + i * 56), tc.sc(60 + 110 + (i * 23) % 60), tc.sc(118 + i * 56)], radius=tc.sc(8), fill=(60, 68, 100, 255))
    ui = ui.filter(ImageFilter.GaussianBlur(tc.sc(5)))
    ui.putalpha(ui.getchannel("A").point(lambda v: int(v * 0.8)))
    base.alpha_composite(ui)
    base.alpha_composite(tc.glow(size, 930, 400, 380, 330, (109, 75, 216, 170), 70))
    base.alpha_composite(tc.glow(size, 560, 420, 300, 260, (255, 77, 94, 70), 80))
    return base


def vignette(img):
    mask = Image.radial_gradient("L").resize(img.size)
    black = Image.new("RGBA", img.size, (0, 0, 0, 255))
    black.putalpha(mask.point(lambda v: int(max(0, v - 90) * 0.75)))
    img.alpha_composite(black)


def title_text(size_px=176):
    """'BANNED' in white and '?!' in yellow, with a thick dark outline and a drop shadow."""
    f = font(BOLD, size_px)
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    w1 = d0.textlength("BANNED", font=f)
    w2 = d0.textlength("?!", font=f)
    pad = tc.sc(40)
    layer = Image.new("RGBA", (int(w1 + w2) + 2 * pad, tc.sc(size_px * 1.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for dx, dy, col, sw in ((tc.sc(8), tc.sc(10), (0, 0, 0, 170), tc.sc(15)), (0, 0, (0, 0, 0, 255), tc.sc(15))):
        d.text((pad + dx, tc.sc(10) + dy), "BANNED", font=f, fill=col, stroke_width=sw, stroke_fill=col)
        d.text((pad + dx + w1, tc.sc(10) + dy), "?!", font=f, fill=col, stroke_width=sw, stroke_fill=col)
    d.text((pad, tc.sc(10)), "BANNED", font=f, fill=(255, 255, 255, 255))
    d.text((pad + w1, tc.sc(10)), "?!", font=f, fill=(255, 210, 63, 255))
    return layer.rotate(3, resample=Image.BICUBIC, expand=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-watermark", action="store_true")
    args = ap.parse_args()

    canvas = background()
    size = canvas.size

    # impact burst behind the gavel head
    burst = Image.new("RGBA", size, (0, 0, 0, 0))
    tc.starburst(burst, 505, 430, 235, 135, 12, (255, 210, 63, 255), tc.OUTLINE)
    tc.starburst(burst, 505, 430, 170, 100, 12, (255, 244, 176, 255))
    canvas.alpha_composite(burst)

    # the moderator (body and head are drawn first, then the gavel and the arm in front)
    mod = Image.new("RGBA", size, (0, 0, 0, 0))
    cx, cy, r = 955, 425, 165
    tc.draw_mod(mod, cx, cy, r)
    canvas.alpha_composite(mod)

    # giant gavel, tilted so the head swings up to the right
    g = tc.gavel_layer()
    g = g.resize((int(g.width * 0.72), int(g.height * 0.72)), Image.LANCZOS)
    g = g.rotate(-38, resample=Image.BICUBIC, expand=True)
    gx, gy = 360, 615
    canvas.alpha_composite(g, (tc.sc(gx) - g.width // 2, tc.sc(gy) - g.height // 2))

    # arm and fist gripping the handle
    arm = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(arm)
    shoulder, fist = (cx - r * 1.2, cy + r * 1.25), (402, 575)
    tc.thick_line(d, [shoulder, ((shoulder[0] + fist[0]) / 2, (shoulder[1] + fist[1]) / 2 + 18), fist], 112, tc.OUTLINE)
    tc.thick_line(d, [shoulder, ((shoulder[0] + fist[0]) / 2, (shoulder[1] + fist[1]) / 2 + 18), fist], 96, (109, 75, 216, 255))
    tc.ellipse(d, fist[0] - 12, fist[1] - 4, 62, 58, tc.SKIN, tc.OUTLINE, 7)
    for k in range(3):
        tc.thick_line(d, [(fist[0] - 40, fist[1] - 24 + k * 22), (fist[0] - 8, fist[1] - 24 + k * 22)], 5, tc.SKIN_SHADE)
    canvas.alpha_composite(arm)

    # purple name plate on the hoodie
    plate = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(plate)
    d.rounded_rectangle([tc.sc(cx - 230), tc.sc(622), tc.sc(cx + 230), tc.sc(702)], radius=tc.sc(40), fill=(22, 25, 37, 255), outline=(183, 148, 255, 255), width=tc.sc(6))
    f = font(SEMI, 42)
    label = "Tyler | Moderator"
    tw = d.textlength(label, font=f)
    d.text((tc.sc(cx) - tw / 2, tc.sc(645)), label, font=f, fill=(183, 148, 255, 255))
    canvas.alpha_composite(plate)

    # big title text, top left
    title = title_text()
    canvas.alpha_composite(title, (tc.sc(18), tc.sc(-4)))

    vignette(canvas)
    if not args.no_watermark:
        wm = ImageDraw.Draw(canvas)
        small = font(SEMI, 24)
        text = "Art by " + C.MODEL_NAME
        tw = wm.textlength(text, font=small)
        wm.rounded_rectangle([tc.sc(W - 24) - tw - tc.sc(24), tc.sc(14), tc.sc(W - 12), tc.sc(56)], radius=tc.sc(14), fill=(0, 0, 0, 150))
        wm.text((tc.sc(W - 24) - tw - tc.sc(12), tc.sc(21)), text, font=small, fill=(235, 238, 250, 255))
    out = canvas.resize((W, H), Image.LANCZOS).convert("RGB")
    C.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = C.OUTPUT_DIR / "thumbnail.png"
    out.save(path, optimize=True)
    print(f"wrote {path} ({out.size[0]}x{out.size[1]}, {path.stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()
