"""
fourteen.py — BIRTH FLOWER: Erica carnea (spring heath)

A particle renderer: a sprig of spring heath is grown out of ~200k
particles, then written out as a poster (JPG) and an animation (MP4).

Run:
    python fourteen.py

Options:
    python fourteen.py --frames 300 --points 200000
    python fourteen.py --image erica.jpg      # use a real photo instead
    python fourteen.py --preview art.png      # only dump the target art
    python fourteen.py --mid mid.png          # dump a half-way frame too
"""

import math
import os
import random
import sys
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import numpy as np
import pygame
import imageio_ffmpeg

# ---------------------------------------------------------------------------
# configuration
# ---------------------------------------------------------------------------
W, H = 600, 900
FPS = 30
FRAMES = 300
POINTS = 200_000
SUP = 2                      # supersampling factor for the artwork
SEED = 14

OUT_NAME = "Erica"
DATE_LINE = "SPRING HEATH"

BLACK = (7, 7, 9)

PINK = [(212, 94, 148), (226, 110, 162), (202, 84, 138), (236, 124, 174)]
PINK_MID = [(244, 146, 188), (252, 160, 200), (238, 132, 178), (255, 174, 208)]
PINK_HI = [(255, 190, 218), (255, 204, 228), (252, 184, 214), (255, 212, 234)]
PINK_LIP = [(250, 178, 208), (252, 190, 216), (248, 172, 204), (254, 196, 220)]
ORANGE = (226, 122, 74)
ORANGE_MID = (242, 152, 104)
ORANGE_HI = (255, 196, 146)
ORANGE_LIP = (255, 214, 178)
TIP = (96, 44, 40)

STEM = (56, 36, 26)
STEM_HI = (98, 68, 46)
LEAF_DARK = (30, 58, 42)
LEAF_MID = (44, 82, 54)
LEAF_HI = (74, 118, 76)
LEAF_RUST = (84, 54, 38)
LEAF_RUST_HI = (122, 84, 58)


# ---------------------------------------------------------------------------
# tiny 2D helpers (coordinates are in 600x900 space, drawing at 2x)
# ---------------------------------------------------------------------------
def S(v):
    return int(round(v * SUP))


def line(surf, p1, p2, colour, width=1):
    pygame.draw.line(surf, colour, (S(p1[0]), S(p1[1])),
                     (S(p2[0]), S(p2[1])), max(1, S(width)))


def poly(surf, pts, colour):
    pygame.draw.polygon(surf, colour, [(S(x), S(y)) for x, y in pts])


def blob(surf, cx, cy, a, b, angle, colour, flare=0.0, steps=28):
    ca, sa = math.cos(angle), math.sin(angle)
    pts = []
    for i in range(steps):
        th = 2 * math.pi * i / steps
        r = 1.0 + flare * max(0.0, math.sin(th)) ** 2
        lx = a * r * math.cos(th)
        ly = b * r * math.sin(th)
        pts.append((cx + lx * ca - ly * sa, cy + lx * sa + ly * ca))
    poly(surf, pts, colour)


def disc(surf, cx, cy, r, colour):
    pygame.draw.circle(surf, colour, (S(cx), S(cy)), max(1, S(r)))


# ---------------------------------------------------------------------------
# the flower artwork
# ---------------------------------------------------------------------------
BRANCHES = [
    [(300, 915), (296, 810), (304, 700), (322, 600), (344, 500), (368, 408)],
    [(300, 760), (258, 690), (214, 610), (176, 536)],
    [(306, 650), (262, 570), (230, 490), (206, 424)],
    [(312, 700), (362, 630), (410, 560), (448, 500)],
    [(330, 610), (380, 545), (424, 485), (456, 428)],
    [(346, 520), (322, 448), (302, 388), (300, 322)],
]


def branch_points(branch, n=90):
    out = []
    segs = len(branch) - 1
    for i in range(n):
        u = i / (n - 1) * segs
        k = min(int(u), segs - 1)
        f = u - k
        x = branch[k][0] + (branch[k + 1][0] - branch[k][0]) * f
        y = branch[k][1] + (branch[k + 1][1] - branch[k][1]) * f
        out.append((x, y))
    return out


def draw_stem(surf, branch):
    pts = branch_points(branch)
    n = len(pts)
    for i in range(n - 1):
        f = i / (n - 1)
        width = 5.2 * (1 - 0.6 * f) + 1.0
        line(surf, pts[i], pts[i + 1], STEM, width)
    for i in range(2, n - 1, 1):
        f = i / (n - 1)
        off = (0.9 * (1 - 0.4 * f), -0.6)
        line(surf,
             (pts[i][0] + off[0], pts[i][1] + off[1]),
             (pts[i + 1][0] + off[0], pts[i + 1][1] + off[1]),
             STEM_HI if f < 0.7 else STEM, 1.0)


def tangent(pts, i):
    a = pts[max(0, i - 2)]
    b = pts[min(len(pts) - 1, i + 2)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


def draw_leaves(surf, branch, count=72, rust_from=0.55):
    pts = branch_points(branch, count)
    rng = random.Random(SEED + hash(tuple(branch[:1])) % 97)
    for i in range(4, len(pts) - 1):
        u = i / (len(pts) - 1)
        tx, ty = tangent(pts, i)
        base_angle = math.atan2(ty, tx)
        rust = u > rust_from and rng.random() < 0.5
        for side in (-1, 1):
            for _ in range(2):
                ang = base_angle + side * math.radians(rng.uniform(28, 72)) \
                    + math.radians(rng.uniform(-14, 14))
                length = rng.uniform(5.0, 12.5) * (1 - 0.2 * u)
                tipx = pts[i][0] + math.cos(ang) * length
                tipy = pts[i][1] + math.sin(ang) * length
                if rust:
                    col = LEAF_RUST if rng.random() < 0.55 else LEAF_RUST_HI
                else:
                    col = rng.choice([LEAF_DARK, LEAF_MID, LEAF_MID, LEAF_HI])
                line(surf, pts[i], (tipx, tipy), col, rng.uniform(0.8, 1.6))


def draw_bell(surf, x, y, w, h, angle, body, mid, hi, lip, rng):
    ca, sa = math.cos(angle), math.sin(angle)

    def P(lx, ly):
        return (x + lx * ca - ly * sa, y + lx * sa + ly * ca)

    # neck where the flower joins the branch
    blob(surf, *P(0, 0.05 * h), w * 0.15, h * 0.05, angle, body, steps=16)

    # dark rim, then the bell body over it
    blob(surf, *P(0, 0.52 * h), w * 0.52, h * 0.475, angle,
         (188, 92, 140), flare=0.18, steps=30)
    blob(surf, *P(0, 0.52 * h), w * 0.48, h * 0.445, angle, body,
         flare=0.16, steps=30)

    # soft inner face
    blob(surf, *P(0, 0.45 * h), w * 0.33, h * 0.30, angle, mid,
         flare=0.10, steps=22)

    # sheen down the left side
    blob(surf, *P(-w * 0.17, 0.38 * h), w * 0.09, h * 0.20, angle, hi, steps=16)

    # pale lip at the mouth
    blob(surf, *P(0, 0.925 * h), w * 0.26, h * 0.030, angle, lip,
         flare=0.30, steps=18)

    # dark sepals at the tip
    blob(surf, *P(0, 1.005 * h), w * 0.085, h * 0.05, angle, TIP, steps=14)


def flower_cluster(surf, x, y, rng, count=None, scale=1.0, orange=False):
    count = count or rng.randint(3, 4)
    for k in range(count):
        spread = k - (count - 1) / 2
        dx = spread * 8.5 * scale + rng.uniform(-2.0, 2.0)
        dy = abs(spread) * 1.6 * scale + rng.uniform(0.0, 3.0)
        w = rng.uniform(13.0, 17.0) * scale
        h = rng.uniform(27.0, 35.0) * scale
        ang = math.radians(spread * 9.0 + rng.uniform(-10, 10))
        line(surf, (x, y), (x + dx, y + dy), (74, 48, 38), 1.1)
        if orange and k == 1:
            draw_bell(surf, x + dx, y + dy, w, h, ang,
                      ORANGE, ORANGE_MID, ORANGE_HI, ORANGE_LIP, rng)
        else:
            idx = rng.randrange(len(PINK))
            draw_bell(surf, x + dx, y + dy, w, h, ang,
                      PINK[idx], PINK_MID[idx], PINK_HI[idx],
                      PINK_LIP[idx], rng)


def draw_leaf_sprays(surf):
    """A light scatter of needles in front of the flowers, for depth."""
    rng = random.Random(SEED + 9)
    for branch in BRANCHES:
        pts = branch_points(branch, 60)
        for _ in range(12):
            i = rng.randint(int(len(pts) * 0.30), len(pts) - 2)
            tx, ty = tangent(pts, i)
            base = math.atan2(ty, tx)
            for side in (-1, 1):
                ang = base + side * math.radians(rng.uniform(45, 95)) \
                    + math.radians(rng.uniform(-10, 10))
                length = rng.uniform(5.0, 9.0)
                colour = rng.choice([LEAF_DARK, LEAF_MID, LEAF_RUST])
                line(surf, pts[i],
                     (pts[i][0] + math.cos(ang) * length,
                      pts[i][1] + math.sin(ang) * length),
                     colour, rng.uniform(0.9, 1.6))


def draw_flowers(surf):
    rng = random.Random(SEED + 1)
    specs = [
        (0, 0.32, 0.99, 10),
        (1, 0.50, 1.00, 7),
        (2, 0.46, 1.00, 6),
        (3, 0.48, 1.00, 7),
        (4, 0.44, 1.00, 7),
        (5, 0.32, 0.98, 6),
    ]
    for bi, lo, hi, count in specs:
        pts = branch_points(BRANCHES[bi], 80)
        for k in range(count):
            u = lo + (hi - lo) * k / max(1, count - 1)
            u = min(0.995, u + rng.uniform(-0.015, 0.015))
            i = int(u * (len(pts) - 1))
            px, py = pts[i]
            tx, ty = tangent(pts, i)
            nx, ny = -ty, tx
            off = rng.uniform(-3.0, 3.0)
            orange = (bi == 2 and k == 2) or (bi == 0 and k == 5)
            flower_cluster(surf, px + nx * off, py + ny * off + 2.0, rng,
                           scale=rng.uniform(0.85, 1.05), orange=orange)

    # a few buds at the very tips
    for bi, branch in enumerate(BRANCHES):
        tipx, tipy = branch[-1]
        for _ in range(3):
            bx = tipx + rng.uniform(-7, 7)
            by = tipy + rng.uniform(-4, 9)
            blob(surf, bx, by, rng.uniform(2.0, 3.4), rng.uniform(4.5, 7.0),
                 math.radians(rng.uniform(-30, 30)), (74, 40, 34), 0.1, 16)
            disc(surf, bx, by - 1, 1.2, (48, 26, 24))


def generate_art():
    random.seed(SEED)
    rng = random.Random(SEED)
    big = pygame.Surface((W * SUP, H * SUP))
    big.fill(BLACK)

    # soft glow behind the sprig
    glow = pygame.Surface((W * SUP, H * SUP), pygame.SRCALPHA)
    for r, alpha in ((300, 10), (210, 12), (130, 14)):
        pygame.draw.circle(glow, (34, 18, 30, alpha),
                           (S(300), S(560)), S(r))
    big.blit(glow, (0, 0))

    for branch in BRANCHES:
        draw_stem(big, branch)
        draw_leaves(big, branch, count=52, rust_from=0.55)

    draw_flowers(big)
    draw_leaf_sprays(big)

    # a little foreground foliage for depth
    fg = [(300, 620), (255, 585), (225, 560), (205, 548)]
    draw_stem(big, fg)
    draw_leaves(big, fg, count=18, rust_from=0.8)

    shifted = pygame.Surface(big.get_size())
    shifted.fill(BLACK)
    shifted.blit(big, (0, -46 * SUP))
    art = pygame.transform.smoothscale(shifted, (W, H))

    # fade the very bottom to black so the title sits on clean darkness
    fade = pygame.Surface((W, 170), pygame.SRCALPHA)
    for row in range(170):
        a = int(255 * (row / 169) ** 1.5)
        pygame.draw.line(fade, (7, 7, 9, a), (0, row), (W, row))
    art.blit(fade, (0, H - 170))
    return art


# ---------------------------------------------------------------------------
# particle model
# ---------------------------------------------------------------------------
def art_to_array(surface):
    raw = pygame.image.tobytes(surface, "RGB")
    return np.frombuffer(raw, dtype=np.uint8).reshape(H, W, 3).copy()


def load_photo(path):
    img = pygame.image.load(path).convert()
    src_w, src_h = img.get_size()
    scale = max(W / src_w, H / src_h)
    nw, nh = int(src_w * scale + 0.5), int(src_h * scale + 0.5)
    img = pygame.transform.smoothscale(img, (nw, nh))
    out = pygame.Surface((W, H))
    out.blit(img, ((W - nw) // 2, (H - nh) // 2))
    return out


def build_particles(art_array, n_points):
    rng = np.random.default_rng(SEED)
    rgb = art_array.astype(np.float32)
    lum = rgb @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    ys, xs = np.nonzero(lum > 12.0)
    weights = (lum[ys, xs] / 255.0) ** 0.62
    pick = rng.choice(len(xs), size=n_points, p=weights / weights.sum())

    tx = xs[pick].astype(np.float32) + rng.random(n_points).astype(np.float32)
    ty = ys[pick].astype(np.float32) + rng.random(n_points).astype(np.float32)
    colours = rgb[ys[pick], xs[pick]].astype(np.uint8)

    # start in a loose halo around each target: the flower condenses into place
    ang = rng.random(n_points).astype(np.float32) * 6.283
    radius = (26.0 + rng.random(n_points).astype(np.float32) ** 0.7 * 74.0)
    sx = (tx + np.cos(ang) * radius).astype(np.float32)
    sy = (ty + np.sin(ang) * radius).astype(np.float32)

    delay = (0.05 + 0.50 * (1.0 - ty / H)
             + rng.random(n_points).astype(np.float32) * 0.06)
    dur = (0.15 + rng.random(n_points).astype(np.float32) * 0.10)

    dx = tx - sx
    dy = ty - sy
    dist = np.hypot(dx, dy) + 1e-6
    px = -(dy / dist)
    py = (dx / dist)
    amp = (3.0 + rng.random(n_points).astype(np.float32) * 8.0)
    # random sign, so the swirl is not uniform
    sign = np.where(rng.random(n_points) < 0.5, -1.0, 1.0).astype(np.float32)

    return {
        "tx": tx, "ty": ty, "sx": sx, "sy": sy,
        "delay": delay, "dur": dur,
        "px": (px * sign).astype(np.float32),
        "py": (py * sign).astype(np.float32),
        "amp": amp,
        "phase": (rng.random(n_points) * 6.283).astype(np.float32),
        "speed": (0.7 + rng.random(n_points) * 1.6).astype(np.float32),
        "colour": colours,
    }


def build_splats(p, rng):
    """Every particle casts one dot; some cast hairs and streaks."""
    n = len(p["tx"])
    is_hair = rng.random(n) < 0.30
    is_streak = rng.random(n) < 0.04

    parents = [np.arange(n, dtype=np.int32)]
    offs = [np.zeros((n, 2), dtype=np.float32)]
    weights = [np.ones(n, dtype=np.float32)]

    hair_idx = np.nonzero(is_hair)[0].astype(np.int32)
    if len(hair_idx):
        ang = rng.random(len(hair_idx)) * 6.283
        ux = np.cos(ang).astype(np.float32)
        uy = np.sin(ang).astype(np.float32)
        for k in (-1.0, 0.0, 1.0):
            parents.append(hair_idx)
            offs.append(np.stack([ux * k * 1.1, uy * k * 1.1], axis=1))
            weights.append(np.full(len(hair_idx), 0.55, dtype=np.float32))

    streak_idx = np.nonzero(is_streak)[0].astype(np.int32)
    if len(streak_idx):
        ang = rng.random(len(streak_idx)) * 6.283
        ux = np.cos(ang).astype(np.float32)
        uy = np.sin(ang).astype(np.float32)
        for k in (-2.0, -1.0, 0.0, 1.0, 2.0):
            parents.append(streak_idx)
            offs.append(np.stack([ux * k * 1.4, uy * k * 1.4], axis=1))
            weights.append(np.full(len(streak_idx), 0.30, dtype=np.float32))

    parent = np.concatenate(parents)
    off = np.concatenate(offs, axis=0)
    w = np.concatenate(weights)
    colours = p["colour"][parent].astype(np.float32) * 1.06
    return parent, off, w, colours, len(hair_idx), len(streak_idx)


# ---------------------------------------------------------------------------
# frame renderer
# ---------------------------------------------------------------------------
PIX = W * H


def render_frame(p, parent, off, weight, splat_colour, t):
    e = np.clip((t - p["delay"]) / p["dur"], 0.0, 1.0).astype(np.float32)
    ease = 1.0 - (1.0 - e) ** 3

    x = p["sx"] + (p["tx"] - p["sx"]) * ease
    y = p["sy"] + (p["ty"] - p["sy"]) * ease

    swirl = (np.sin(np.pi * e) * p["amp"]).astype(np.float32)
    x = x + p["px"] * swirl
    y = y + p["py"] * swirl

    # after landing, a soft living shimmer
    idle = (e > 0.98).astype(np.float32)
    x = x + np.sin(t * p["speed"] * 6.0 + p["phase"]) * 0.6 * idle
    y = y + np.cos(t * p["speed"] * 5.0 + p["phase"]) * 0.5 * idle

    sx = x[parent] + off[:, 0]
    sy = y[parent] + off[:, 1]
    np.clip(sx, 0, W - 1, out=sx)
    np.clip(sy, 0, H - 1, out=sy)
    idx = (sy.astype(np.int32) * W + sx.astype(np.int32)).ravel()

    count = np.bincount(idx, weights=weight, minlength=PIX)
    rs = np.bincount(idx, weights=weight * splat_colour[:, 0], minlength=PIX)
    gs = np.bincount(idx, weights=weight * splat_colour[:, 1], minlength=PIX)
    bs = np.bincount(idx, weights=weight * splat_colour[:, 2], minlength=PIX)

    cover = 1.0 - np.exp(-2.4 * count)
    scale = cover / np.maximum(count, 1e-6)
    rgb = np.empty((PIX, 3), dtype=np.float32)
    rgb[:, 0] = np.clip(rs * scale, 0, 255)
    rgb[:, 1] = np.clip(gs * scale, 0, 255)
    rgb[:, 2] = np.clip(bs * scale, 0, 255)

    # a cheap bloom: average with a one-pixel-shifted copy
    img = rgb.reshape(H, W, 3)
    blur = (img + np.roll(img, 1, axis=0) + np.roll(img, 1, axis=1)) / 3.0
    out = np.clip(img * 0.85 + blur * 0.25, 0, 255).astype(np.uint8)
    return out


# ---------------------------------------------------------------------------
# text overlay
# ---------------------------------------------------------------------------
TEXT_LAYER = None


def get_font(size, bold=False, italic=False):
    for name in ("georgia", "timesnewroman", "dejavuserif", "serif"):
        path = pygame.font.match_font(name, bold=bold, italic=italic)
        if path:
            return pygame.font.Font(path, size)
    return pygame.font.SysFont(None, size, bold=bold, italic=italic)


def draw_spaced(surf, text, font, colour, cx, y, spacing):
    glyphs = [font.render(ch, True, colour) for ch in text]
    total = sum(g.get_width() for g in glyphs) + spacing * (len(glyphs) - 1)
    x = cx - total / 2
    for g in glyphs:
        surf.blit(g, (round(x), y))
        x += g.get_width() + spacing


def build_text_layer():
    layer = pygame.Surface((W, H), pygame.SRCALPHA)

    f_small = get_font(13, bold=True)
    draw_spaced(layer, "YOUR BIRTH FLOWER", f_small, (188, 180, 176), W // 2, 52, 3)

    f_tiny = get_font(11)
    draw_spaced(layer, DATE_LINE, f_tiny, (138, 130, 128), W // 2, 76, 4)

    f_title = get_font(48, bold=True)
    title = "Erica carnea"
    tw = f_title.size(title)[0]
    tx = (W - tw) // 2
    ty = H - 92
    shadow = f_title.render(title, True, (0, 0, 0))
    layer.blit(shadow, (tx + 1, ty + 2))
    ink = f_title.render(title, True, (240, 234, 230))
    layer.blit(ink, (tx, ty))
    return layer


def overlay_text(surf, alpha):
    if alpha <= 0:
        return
    TEXT_LAYER.set_alpha(int(alpha * 255))
    surf.blit(TEXT_LAYER, (0, 0))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def bar(progress, width=28):
    filled = int(progress * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def main():
    global W, H

    frames = FRAMES
    points = POINTS
    image_path = None
    preview_path = None
    mid_path = None
    out_name = OUT_NAME

    args = sys.argv[1:]
    if "--frames" in args:
        frames = int(args[args.index("--frames") + 1])
    if "--points" in args:
        points = int(args[args.index("--points") + 1])
    if "--image" in args:
        image_path = args[args.index("--image") + 1]
    if "--preview" in args:
        preview_path = args[args.index("--preview") + 1]
    if "--mid" in args:
        mid_path = args[args.index("--mid") + 1]
    if "--out" in args:
        out_name = args[args.index("--out") + 1]

    pygame.init()
    pygame.font.init()

    if image_path:
        art = load_photo(image_path)
        W, H = art.get_size()
    else:
        art = generate_art()

    if preview_path:
        pygame.image.save(art, preview_path)
        print(f"target art -> {preview_path}")
        pygame.quit()
        return

    global TEXT_LAYER
    TEXT_LAYER = build_text_layer()

    art_array = art_to_array(art)
    rng = np.random.default_rng(SEED + 6)
    p = build_particles(art_array, points)
    parent, off, weight, splat_colour, hairs, streaks = build_splats(p, rng)
    total_splats = len(parent)

    print(f"erica carnea - spring heath")
    print(f"points {points:,}  hairs {hairs:,}  streaks {streaks:,}"
          f"  splats {total_splats:,}")
    print(f"size {W}x{H}  frames {frames}  fps {FPS}")

    mp4_path = f"{out_name}_anim.mp4"
    jpg_path = f"{out_name}.jpg"
    writer = imageio_ffmpeg.write_frames(
        mp4_path, (W, H), fps=FPS, quality=7,
        pix_fmt_in="rgb24", pix_fmt_out="yuv420p",
        macro_block_size=4)
    writer.send(None)

    start = time.time()
    poster_surface = None

    for f in range(frames):
        t = f / (frames - 1)
        rgb = render_frame(p, parent, off, weight, splat_colour, t)

        frame_surf = pygame.image.frombuffer(rgb.tobytes(), (W, H), "RGB")
        fade = 0.0
        if t > 0.80:
            fade = min(1.0, (t - 0.80) / 0.17)
        overlay_text(frame_surf, fade)

        writer.send(pygame.image.tobytes(frame_surf, "RGB"))

        if fade >= 1.0 and poster_surface is None:
            poster_surface = frame_surf.copy()
        if mid_path and f == frames // 2:
            pygame.image.save(frame_surf, mid_path)

        done = (f + 1) / frames
        elapsed = time.time() - start
        fps_now = (f + 1) / elapsed if elapsed > 0 else 0.0
        print(f"\r{bar(done, 20)} {done * 100:3.0f}%  "
              f"{f + 1}/{frames}  {fps_now:4.1f} fps", end="", flush=True)

    writer.close()

    if poster_surface is None:
        poster_surface = pygame.Surface((W, H))
        poster_surface.fill(BLACK)
        poster_surface.blit(pygame.image.frombuffer(rgb.tobytes(), (W, H), "RGB"), (0, 0))
        overlay_text(poster_surface, 1.0)

    pygame.image.save(poster_surface, jpg_path)
    elapsed = time.time() - start
    print(f"\nposter  -> {jpg_path}")
    print(f"video   -> {mp4_path}")
    print(f"done in {elapsed:.1f}s")

    pygame.quit()


if __name__ == "__main__":
    main()
