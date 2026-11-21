"""PHOTO -> colored ASCII portrait on a starfield, like the red/green poster.

    python fourteen.py photo.jpg                     # colored ASCII in the terminal
    python fourteen.py photo.jpg --png for_you.png   # save the poster
    python fourteen.py --selftest                    # sanity check

Pillow only. Colors are the photo's own, pushed vivid, so red/green lighting
in the source (LED strips, gels) comes out exactly like the reference.
"""

import colorsys
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

RAMP = " .`':;~+*xoO8%#@"  # dark -> bright
COLS = 100


def vivid(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    s = min(1.0, s * 1.9 + 0.25)
    v = min(1.0, v * 1.35)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def ascii_grid(img, cols=COLS):
    w, h = img.size
    rows = max(1, round(h / w * cols * 0.5))  # chars are ~2x taller than wide
    px = img.convert("RGB").resize((cols, rows), Image.LANCZOS).tobytes()
    grid = []
    for y in range(rows):
        row = []
        for x in range(cols):
            i = (y * cols + x) * 3
            c = px[i], px[i + 1], px[i + 2]
            lum = (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255
            if lum < 0.06:
                row.append((" ", c))
            else:
                row.append((RAMP[int(lum * (len(RAMP) - 1))], vivid(*c)))
        grid.append(row)
    return grid


def to_terminal(grid):
    if os.name == "nt":
        os.system("")  # enable ANSI escapes in the Windows console
    lines = []
    for row in grid:
        line = ""
        for ch, (r, g, b) in row:
            line += " " if ch == " " else f"\x1b[38;2;{r};{g};{b}m{ch}"
        lines.append(line + "\x1b[0m")
    return "\n".join(lines)


def load_font(size):
    for name in ("consola.ttf", "cour.ttf", "DejaVuSansMono.ttf", "Courier New.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size)


def starfield(d, w, h, seed=7):
    rng = random.Random(seed)
    for _ in range(w * h // 2600):
        x, y = rng.randrange(w), rng.randrange(h)
        v = rng.randint(70, 255)
        d.point((x, y), (v, v, min(255, v + 15)))
    for _ in range(7):  # sparkles
        x, y, r = rng.randrange(w), rng.randrange(h), rng.randint(6, 16)
        for dx in range(-r, r + 1):
            f = 1 - abs(dx) / r
            t = int(200 * f)
            d.point((x + dx, y), (t, t, t))
        for dy in range(-r, r + 1):
            f = 1 - abs(dy) / r
            t = int(200 * f)
            d.point((x, y + dy), (t, t, t))


def to_png(grid, path, caption="FOR YOU", font_size=15):
    font = load_font(font_size)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    cw = probe.textlength("M", font=font) or font_size * 0.6
    chh = font_size * 1.12
    pad = 70
    w = int(len(grid[0]) * cw) + pad * 2
    h = int(len(grid) * chh) + pad * 2 + 90
    img = Image.new("RGB", (w, h), (3, 4, 9))
    d = ImageDraw.Draw(img)
    starfield(d, w, h)

    y = pad
    for row in grid:
        x = pad
        for ch, c in row:
            if ch != " ":
                d.text((x, y), ch, font=font, fill=c)
            x += cw
        y += chh

    cap_font = load_font(int(font_size * 1.15))
    text = " ".join(caption)  # F O R   Y O U
    tw = probe.textlength(text, font=cap_font)
    d.text(((w - tw) / 2, y + 30), text, font=cap_font, fill=(228, 228, 235))
    img.save(path)
    return path


def selftest():
    grad = Image.new("RGB", (80, 80))
    grad.putdata([(i * 3, i * 3, i * 3) for i in range(80) for _ in range(80)])
    grid = ascii_grid(grad, cols=40)
    assert len(grid[0]) == 40 and len(grid) == 20, len(grid)
    assert any(ch != " " for row in grid for ch, _ in row)
    assert grid[0][0][0] == " "
    assert "\x1b[38;2;" in to_terminal(grid)
    out = to_png(grid, "selftest.png", caption="TEST")
    assert Image.open(out).size[0] > 0
    os.remove(out)
    print("ok")


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if "--selftest" in argv:
        return selftest()
    if not args:
        print(__doc__)
        return
    cols = COLS
    if "--cols" in argv:
        cols = int(argv[argv.index("--cols") + 1])
    grid = ascii_grid(Image.open(args[0]), cols)
    if "--png" in argv:
        out = argv[argv.index("--png") + 1]
        print(to_png(grid, out, font_size=15))
    else:
        print(to_terminal(grid))


if __name__ == "__main__":
    main(sys.argv)
