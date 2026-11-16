"""
LONDON AT NIGHT — pixel art edition (pygame)

A tiny 400x225 pixel canvas, scaled up with nearest-neighbour scaling:
Big Ben, the London Eye, The Shard, the Thames, and a red bus rolling by.
Everything is drawn procedurally, no images needed.

Run:
    python thirteen.py

Optional:
    python thirteen.py --frames 300 --shot frame.png
"""

import math
import random
import sys

import pygame

# ---------------------------------------------------------------------------
# canvas
# ---------------------------------------------------------------------------
BASE_W, BASE_H = 400, 225
HORIZON = 155
ROAD_BOTTOM = 176
WATER_TOP = 176

SKY_STOPS = [
    (0.00, (5, 7, 36)),
    (0.40, (18, 12, 58)),
    (0.68, (44, 18, 82)),
    (0.88, (76, 28, 78)),
    (1.00, (104, 42, 72)),
]
WATER_STOPS = [
    (0.00, (11, 20, 50)),
    (0.35, (8, 14, 38)),
    (1.00, (3, 4, 14)),
]

WARM = [(255, 216, 148), (244, 190, 118), (214, 168, 104)]
COOL = [(176, 202, 240), (120, 150, 190)]
BULB = [(255, 236, 170), (255, 176, 210), (150, 214, 255),
        (250, 250, 255), (200, 170, 255)]

# x, width, height above the street
BUILDINGS = [
    (0, 26, 46), (26, 22, 60), (48, 30, 38),
    (110, 24, 48), (134, 18, 64), (152, 16, 54), (166, 5, 42),
    (262, 20, 56), (282, 16, 72), (298, 14, 50),
    (348, 20, 62), (368, 24, 46), (392, 8, 54),
]

EYE_CX, EYE_CY, EYE_R = 215, 105, 44
EYE_LIGHTS = 24
BUS_W = 46

STARS = []
SPARKLES = []
FLICKER = []


# ---------------------------------------------------------------------------
# colour / gradient helpers
# ---------------------------------------------------------------------------
def mix(c1, c2, f):
    f = max(0.0, min(1.0, f))
    return tuple(round(a + (b - a) * f) for a, b in zip(c1, c2))


def sample(stops, f):
    f = max(0.0, min(1.0, f))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if f <= p1:
            return mix(c0, c1, (f - p0) / (p1 - p0))
    return stops[-1][1]


def sky_at_row(y):
    return sample(SKY_STOPS, y / (HORIZON - 1))


def vgrad(surf, y0, y1, stops):
    for y in range(y0, y1):
        f = (y - y0) / max(1, (y1 - y0 - 1))
        pygame.draw.line(surf, sample(stops, f), (0, y), (BASE_W - 1, y))


# ---------------------------------------------------------------------------
# primitive pixel shapes
# ---------------------------------------------------------------------------
def fill_circle(surf, cx, cy, r, colour):
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(max(r * r - dy * dy, 0)))
        pygame.draw.line(surf, colour, (cx - dx, cy + dy), (cx + dx, cy + dy))


def circle_outline(surf, cx, cy, r, colour):
    x, y, d = r, 0, 1 - r
    while x >= y:
        for px, py in ((x, y), (y, x), (-y, x), (-x, y),
                       (-x, -y), (-y, -x), (y, -x), (x, -y)):
            surf.set_at((cx + px, cy + py), colour)
        y += 1
        if d < 0:
            d += 2 * y + 1
        else:
            x -= 1
            d += 2 * (y - x) + 1


# ---------------------------------------------------------------------------
# static background
# ---------------------------------------------------------------------------
def draw_moon(surf):
    cx, cy, r = 52, 29, 12
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 > r * r:
                continue
            if (x - cx - 5) ** 2 + (y - cy + 3) ** 2 <= (r - 2) ** 2:
                continue
            surf.set_at((x, y), (250, 236, 172))


def draw_distant(surf):
    random.seed(7)
    x = 0
    while x < BASE_W:
        w = random.randint(10, 24)
        h = random.randint(18, 52)
        surf.fill((10, 12, 32), (x, HORIZON - h, w, h))
        x += w + random.randint(1, 5)


def draw_buildings(surf):
    random.seed(2026)
    for bx, bw, bh in BUILDINGS:
        by = HORIZON - bh
        body = (15, 18, 44)
        surf.fill(body, (bx, by, bw, bh))
        surf.fill(mix(body, (255, 255, 255), 0.10), (bx, by, bw, 1))

        cols = max(1, (bw - 4) // 3)
        rows = max(1, (bh - 6) // 4)
        ox = bx + 2 + ((bw - 4) - cols * 3) // 2

        for r in range(rows):
            for c in range(cols):
                if random.random() > 0.52:
                    continue
                wx = ox + c * 3
                wy = by + 4 + r * 4
                colour = random.choice(WARM) if random.random() < 0.75 else random.choice(COOL)
                colour = mix(body, colour, random.uniform(0.45, 1.0))
                surf.fill(colour, (wx, wy, 1, 2))

                in_eye = (EYE_CX - EYE_R - 3 <= wx <= EYE_CX + EYE_R + 3 and
                          EYE_CY - EYE_R - 3 <= wy <= EYE_CY + EYE_R + 3)
                if not in_eye and random.random() < 0.12:
                    FLICKER.append((wx, wy, colour, random.uniform(0, 6.28),
                                    random.uniform(0.9, 2.4), body))


def draw_big_ben(surf):
    # base
    surf.fill((22, 22, 46), (82, 138, 26, HORIZON - 138))
    surf.fill((30, 30, 58), (84, 140, 22, HORIZON - 140))
    # shaft
    surf.fill((17, 18, 40), (87, 58, 16, 82))
    surf.fill((72, 60, 34), (87, 58, 1, 82))
    surf.fill((72, 60, 34), (102, 58, 1, 82))
    surf.fill((72, 60, 34), (87, 58, 16, 1))

    # windows up the tower
    for i, y in enumerate(range(64, 134, 9)):
        glow = (255, 210, 130) if i % 3 != 2 else (240, 190, 112)
        surf.fill(glow, (90, y, 2, 3))
        surf.fill(glow, (98, y, 2, 3))

    # clock room
    surf.fill((24, 24, 50), (85, 40, 20, 18))
    surf.fill((112, 88, 46), (85, 40, 20, 1))
    fill_circle(surf, 95, 49, 7, (168, 132, 60))
    fill_circle(surf, 95, 49, 6, (250, 240, 205))
    for tx, ty in ((95, 43), (101, 49), (95, 55), (89, 49)):
        surf.set_at((tx, ty), (110, 86, 44))
    pygame.draw.line(surf, (34, 24, 16), (95, 49), (95, 44), 1)
    pygame.draw.line(surf, (34, 24, 16), (95, 49), (99, 50), 1)
    surf.set_at((95, 49), (34, 24, 16))

    # spire
    pygame.draw.polygon(surf, (14, 15, 36), [(86, 40), (95, 20), (104, 40)])
    pygame.draw.lines(surf, (96, 78, 44), False, [(86, 40), (95, 20), (104, 40)], 1)

    # lit base
    surf.fill((255, 206, 126), (86, 146, 2, 3))
    surf.fill((255, 206, 126), (98, 146, 2, 3))
    surf.fill((84, 62, 36), (91, 146, 5, 9))


def draw_eye_static(surf):
    cx, cy, R = EYE_CX, EYE_CY, EYE_R
    pygame.draw.line(surf, (52, 68, 98), (cx - 9, HORIZON), (cx, cy), 2)
    pygame.draw.line(surf, (52, 68, 98), (cx + 9, HORIZON), (cx, cy), 2)
    pygame.draw.line(surf, (40, 54, 80), (cx - 20, 132), (cx + 5, 142), 1)
    pygame.draw.line(surf, (40, 54, 80), (cx + 20, 132), (cx - 5, 142), 1)

    circle_outline(surf, cx, cy, R, (140, 168, 206))
    circle_outline(surf, cx, cy, R - 3, (66, 84, 116))

    for i in range(16):
        a = math.radians(i * 22.5)
        pygame.draw.line(surf, (58, 74, 104), (cx, cy),
                         (int(cx + math.cos(a) * (R - 4)),
                          int(cy + math.sin(a) * (R - 4))), 1)

    fill_circle(surf, cx, cy, 3, (255, 244, 210))
    circle_outline(surf, cx, cy, 4, (150, 172, 200))


def shard_half(y):
    if y <= 70:
        return 7 * (y - 30) / 40
    return 7 + 8 * (y - 70) / (HORIZON - 70)


def draw_shard(surf):
    pts = [(315, HORIZON), (322, 70), (330, 30), (338, 70), (345, HORIZON)]
    pygame.draw.polygon(surf, (19, 29, 54), pts)
    pygame.draw.lines(surf, (110, 170, 210), False, pts, 1)
    pygame.draw.line(surf, (44, 72, 104), (318, HORIZON), (330, 34), 1)
    pygame.draw.line(surf, (44, 72, 104), (342, HORIZON), (330, 34), 1)
    pygame.draw.line(surf, (44, 72, 104), (330, HORIZON), (330, 34), 1)

    for y in range(38, 152, 5):
        half = int(shard_half(y))
        if half > 1:
            pygame.draw.line(surf, (36, 58, 88), (330 - half + 1, y),
                             (330 + half - 1, y), 1)

    random.seed(5)
    for _ in range(42):
        y = random.randint(42, 150)
        half = int(shard_half(y))
        if half < 2:
            continue
        x = 330 + random.randint(-half + 1, half - 1)
        surf.set_at((x, y), (180, 220, 250))


def draw_road(surf):
    surf.fill((11, 14, 28), (0, HORIZON, BASE_W, ROAD_BOTTOM - HORIZON))
    surf.fill((30, 36, 64), (0, HORIZON, BASE_W, 1))
    for x in range(8, BASE_W, 26):
        surf.fill((34, 36, 58), (x, HORIZON - 7, 1, 7))
        surf.fill((255, 214, 150), (x - 1, HORIZON - 8, 3, 1))
        surf.fill((70, 60, 60), (x - 2, HORIZON - 10, 5, 1))


def draw_water_base(surf):
    vgrad(surf, WATER_TOP, BASE_H, WATER_STOPS)
    surf.fill((40, 54, 92), (0, WATER_TOP, BASE_W, 1))
    random.seed(3)
    for _ in range(42):
        y = random.randint(WATER_TOP + 4, BASE_H - 2)
        x = random.randint(0, BASE_W - 40)
        surf.fill((14, 22, 48), (x, y, random.randint(8, 40), 1))


def draw_background(surf):
    vgrad(surf, 0, HORIZON, SKY_STOPS)
    draw_moon(surf)
    draw_distant(surf)
    draw_buildings(surf)
    draw_big_ben(surf)
    draw_eye_static(surf)
    draw_shard(surf)
    draw_road(surf)
    draw_water_base(surf)


# ---------------------------------------------------------------------------
# animated layers
# ---------------------------------------------------------------------------
def build_stars(bg):
    random.seed(51)
    tries = 0
    while len(STARS) < 95 and tries < 6000:
        tries += 1
        x = random.randint(3, BASE_W - 4)
        y = random.randint(3, HORIZON - 6)
        if tuple(bg.get_at((x, y)))[:3] != sky_at_row(y):
            continue
        STARS.append((x, y, random.uniform(0, 6.28),
                      random.uniform(0.6, 2.4), random.random() < 0.22))


def build_sparkles():
    random.seed(73)
    for _ in range(70):
        SPARKLES.append((random.randint(4, BASE_W - 5),
                         random.randint(WATER_TOP + 6, BASE_H - 4),
                         random.uniform(0, 6.28),
                         random.uniform(0.8, 2.2),
                         random.random() < 0.55))


def draw_stars(surf, t):
    for x, y, phase, speed, big in STARS:
        b = 0.1 + 0.9 * (0.5 + 0.5 * math.sin(t * speed + phase))
        colour = mix((26, 28, 58), (255, 248, 214), b)
        surf.set_at((x, y), colour)
        if big and b > 0.5:
            dim = mix((26, 28, 58), colour, 0.45)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                surf.set_at((x + dx, y + dy), dim)


def draw_flicker(surf, t):
    for x, y, colour, phase, speed, body in FLICKER:
        lit = math.sin(t * speed + phase) > -0.15
        surf.fill(colour if lit else body, (x, y, 1, 2))


def draw_eye_lights(surf, t):
    cx, cy, R = EYE_CX, EYE_CY, EYE_R
    for i in range(EYE_LIGHTS):
        a = math.radians(i * 360 / EYE_LIGHTS)
        wave = 0.5 + 0.5 * math.sin(math.radians(i * 45) - t * 3.2)
        colour = BULB[(i // 3 + int(t * 1.5)) % len(BULB)]
        colour = mix((40, 44, 66), colour, 0.35 + 0.65 * wave)
        x = int(cx + math.cos(a) * R)
        y = int(cy + math.sin(a) * R)
        surf.fill(colour, (x - 1, y - 1, 2, 2))

    pulse = 0.5 + 0.5 * math.sin(t * 2.4)
    fill_circle(surf, cx, cy, 2 + int(pulse * 2),
                mix((90, 90, 120), (255, 250, 220), 0.3 + 0.7 * pulse))


def reflect(surf, cx, colour, half, length, t, phase, strength):
    for i in range(0, length, 2):
        y = WATER_TOP + 4 + i
        if y >= BASE_H:
            break
        f = i / length
        wave = math.sin(i * 0.45 + t * 2.2 + phase)
        w = half * (1 - 0.35 * f) * (0.55 + 0.45 * wave)
        off = wave * 2.5 * (0.4 + f)
        col = mix((7, 11, 30), colour, strength * (1 - 0.75 * f))
        x1 = int(cx - w + off)
        x2 = int(cx + w + off)
        if x2 > x1:
            pygame.draw.line(surf, col, (x1, y), (x2, y), 1)


def draw_water(surf, t):
    reflect(surf, 52, (200, 190, 150), 10, 32, t, 0.0, 0.55)
    reflect(surf, 95, (255, 196, 110), 13, 42, t, 1.0, 0.95)
    reflect(surf, 215, (255, 170, 200), 15, 46, t, 2.0, 0.75)
    reflect(surf, 215, (140, 200, 255), 10, 40, t, 2.6, 0.75)
    reflect(surf, 330, (150, 200, 235), 12, 42, t, 3.2, 0.8)

    for x, y, phase, speed, cool in SPARKLES:
        b = math.sin(t * speed + phase)
        if b <= 0.05:
            continue
        base = (170, 210, 255) if cool else (255, 214, 150)
        colour = mix((7, 11, 30), base, 0.15 + 0.5 * b)
        drift = int(math.sin(t * 0.6 + phase) * 2)
        surf.set_at((x + drift, y), colour)


def draw_bus(surf, x, t):
    x = int(x)
    y = 157
    body = (188, 42, 40)
    surf.fill(body, (x, y, BUS_W, 16))
    surf.fill((212, 64, 54), (x, y, BUS_W, 2))
    surf.fill((244, 228, 196), (x, y + 8, BUS_W, 1))

    for i in range(5):
        surf.fill((255, 212, 150), (x + 3 + i * 9, y + 3, 6, 4))
    for i in range(4):
        surf.fill((248, 236, 200), (x + 3 + i * 9, y + 10, 6, 3))

    surf.fill((92, 28, 28), (x + 37, y + 9, 5, 5))
    fill_circle(surf, x + 10, y + 16, 2, (16, 16, 24))
    fill_circle(surf, x + 35, y + 16, 2, (16, 16, 24))
    surf.fill((255, 240, 170), (x + 44, y + 8, 2, 2))


def draw_beacons(surf, t):
    if math.sin(t * 3.0) > 0.2:
        surf.fill((255, 74, 60), (330, 28, 1, 1))
    if math.sin(t * 2.2 + 1.0) > 0.4:
        surf.fill((255, 200, 120), (95, 19, 1, 1))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    max_frames = None
    shot_path = None
    if "--frames" in sys.argv:
        max_frames = int(sys.argv[sys.argv.index("--frames") + 1])
    if "--shot" in sys.argv:
        shot_path = sys.argv[sys.argv.index("--shot") + 1]

    pygame.init()
    pygame.display.set_caption("London at Night — thirteen.py")

    info = pygame.display.Info()
    scale = max(1, min(4, info.current_w // BASE_W, info.current_h // BASE_H))
    window = pygame.display.set_mode((BASE_W * scale, BASE_H * scale))
    canvas = pygame.Surface((BASE_W, BASE_H)).convert()

    bg = pygame.Surface((BASE_W, BASE_H)).convert()
    draw_background(bg)
    build_stars(bg)
    build_sparkles()

    clock = pygame.time.Clock()
    bus_x = -50.0
    frame = 0
    start = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.quit()
                return

        t = (pygame.time.get_ticks() - start) / 1000.0

        canvas.blit(bg, (0, 0))
        draw_stars(canvas, t)
        draw_flicker(canvas, t)
        draw_eye_lights(canvas, t)
        draw_water(canvas, t)
        draw_bus(canvas, bus_x, t)
        draw_beacons(canvas, t)

        pygame.transform.scale(canvas, window.get_size(), window)
        pygame.display.flip()

        bus_x += 0.55
        if bus_x > BASE_W + 6:
            bus_x = -BUS_W - 6

        frame += 1
        if shot_path and frame == 400:
            pygame.image.save(window, shot_path)
        if max_frames is not None and frame >= max_frames:
            break

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
