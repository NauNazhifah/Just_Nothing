"""
LONDON AT NIGHT — in pure Python (turtle)

Big Ben, the London Eye, The Shard, the Thames and a red double-decker
bus — all painted with turtle graphics and animated in a small loop.

Run:
    python twelave.py
"""

import math
import random
import time
import turtle

# ---------------------------------------------------------------------------
# canvas / layout
# ---------------------------------------------------------------------------
W, H = 1000, 720
LEFT, RIGHT = -W / 2, W / 2
BOTTOM, TOP = -H / 2, H / 2

GROUND = -70                      # where the buildings meet the street
ROAD_TOP, ROAD_BOTTOM = -70, -118
RIVER_TOP = -118

ROAD = (14, 17, 34)
WARM = (255, 206, 120)
COOL = (206, 226, 255)

EYE_C = (60, 70)
EYE_R = 118

screen = turtle.Screen()
screen.setup(W, H)
screen.title("London at Night — Pure Python")
screen.colormode(255)
screen.bgcolor((4, 6, 30))
screen.tracer(0)
screen.delay(0)

BLOCKED = []                      # boxes that stars must keep out of


# ---------------------------------------------------------------------------
# tiny drawing helpers
# ---------------------------------------------------------------------------
def mix(c1, c2, f):
    """Blend two RGB colours, f = 0 -> c1, f = 1 -> c2."""
    f = max(0.0, min(1.0, f))
    return tuple(round(a + (b - a) * f) for a, b in zip(c1, c2))


def rect(pen, x, y, w, h, colour):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(colour)
    pen.begin_fill()
    pen.goto(x + w, y)
    pen.goto(x + w, y + h)
    pen.goto(x, y + h)
    pen.goto(x, y)
    pen.end_fill()
    pen.penup()


def disc(pen, cx, cy, r, colour):
    pen.penup()
    pen.goto(cx, cy - r)
    pen.setheading(0)
    pen.color(colour)
    pen.begin_fill()
    pen.circle(r)
    pen.end_fill()
    pen.penup()


def stroke(pen, x1, y1, x2, y2, colour, width=1):
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.color(colour)
    pen.width(width)
    pen.goto(x2, y2)
    pen.penup()
    pen.width(1)


def polygon(pen, pts, colour, outline=None, width=1):
    pen.penup()
    pen.color(outline or colour)
    pen.width(width)
    pen.begin_fill()
    pen.goto(pts[0])
    for p in pts[1:]:
        pen.goto(p)
    pen.goto(pts[0])
    pen.end_fill()
    pen.penup()
    pen.width(1)


def new_pen():
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()
    return pen


# ---------------------------------------------------------------------------
# sky gradient
# ---------------------------------------------------------------------------
SKY_STOPS = [
    (0.00, (4, 6, 34)),           # deep navy, top of the sky
    (0.38, (18, 12, 62)),
    (0.62, (42, 18, 84)),
    (0.82, (78, 30, 84)),
    (1.00, (112, 44, 78)),        # purple-red glow at the horizon
]


def sky_colour(f):
    f = max(0.0, min(1.0, f))
    for (p0, c0), (p1, c1) in zip(SKY_STOPS, SKY_STOPS[1:]):
        if f <= p1:
            return mix(c0, c1, (f - p0) / (p1 - p0))
    return SKY_STOPS[-1][1]


def sky_at(y):
    return sky_colour((TOP - y) / (TOP - GROUND))


def draw_sky(pen):
    bands = 96
    step = (TOP - GROUND) / bands
    for i in range(bands):
        y = GROUND + i * step
        rect(pen, LEFT, y, W, step + 0.8, sky_colour(1 - i / bands))


# ---------------------------------------------------------------------------
# moon (a real crescent, not a circle with a bite)
# ---------------------------------------------------------------------------
def crescent(pen, cx, cy, r, dx, dy, colour):
    d = math.hypot(dx, dy)
    r2 = 0.90 * r
    base = math.atan2(dy, dx)
    a = (r * r - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r * r - a * a, 0.0))
    half = math.acos(max(-1.0, min(1.0, a / r)))
    half2 = math.atan2(h, a - d)

    pts = []
    steps = 56
    for i in range(steps + 1):                       # outer rim
        ang = half + (2 * math.pi - 2 * half) * i / steps
        pts.append((math.cos(ang) * r, math.sin(ang) * r))
    for i in range(1, steps + 1):                    # the bite
        ang = -half2 + (2 * half2 - 2 * math.pi) * i / steps
        pts.append((d + math.cos(ang) * r2, math.sin(ang) * r2))

    ca, sa = math.cos(base), math.sin(base)
    pen.penup()
    pen.color(colour)
    pen.begin_fill()
    for x, y in pts:
        pen.goto(cx + x * ca - y * sa, cy + x * sa + y * ca)
    pen.end_fill()
    pen.penup()


def draw_moon(pen):
    cx, cy, r = -392, 286, 26
    disc(pen, cx, cy, r + 10, mix(sky_at(cy), (240, 226, 170), 0.06))
    disc(pen, cx, cy, r + 5, mix(sky_at(cy), (250, 236, 180), 0.10))
    crescent(pen, cx, cy, r, -8, 7, (250, 236, 176))
    BLOCKED.append((cx - r - 14, cy - r - 14, 2 * r + 28, 2 * r + 28))


# ---------------------------------------------------------------------------
# city buildings
# ---------------------------------------------------------------------------
def draw_building(pen, x, y, w, h, body, lit=0.5):
    rect(pen, x, y, w, h, body)
    rect(pen, x, y + h - 4, w, 4, mix(body, (255, 255, 255), 0.10))

    cols = max(2, int(w // 13))
    rows = max(2, int(h // 18))
    mx = 4.0
    cw = (w - mx * (cols + 1)) / cols
    ch = (h - 16 - mx * (rows + 1)) / rows
    if cw < 2 or ch < 2:
        return

    for r in range(rows):
        for c in range(cols):
            if random.random() > lit:
                continue
            wx = x + mx + c * (cw + mx)
            wy = y + 7 + r * (ch + mx)
            colour = WARM if random.random() < 0.72 else COOL
            rect(pen, wx, wy, cw, ch, mix(body, colour, random.uniform(0.45, 1.0)))

    BLOCKED.append((x - 4, y, w + 8, h + 8))


def draw_skyline(pen):
    # far away blocks, barely visible in the haze
    x = LEFT
    while x < RIGHT:
        w = random.uniform(40, 90)
        h = random.uniform(40, 120)
        rect(pen, x, GROUND - 2, w, h, (10, 12, 34))
        x += w + random.uniform(4, 16)

    near = [
        (-500, 70, 92), (-428, 62, 132), (-366, 54, 86),
        (-250, 48, 108), (-200, 58, 148), (-140, 44, 120), (-96, 46, 164),
        (-44, 34, 96), (182, 42, 124), (226, 48, 158), (276, 40, 104),
        (312, 18, 138), (430, 70, 150),
    ]
    for bx, bw, bh in near:
        draw_building(pen, bx, GROUND, bw, bh, (15, 18, 44), lit=0.55)


# ---------------------------------------------------------------------------
# Big Ben
# ---------------------------------------------------------------------------
def draw_big_ben(pen):
    # wide base building
    rect(pen, -352, GROUND, 104, 56, (20, 20, 44))
    rect(pen, -344, GROUND, 88, 48, (25, 25, 53))

    # tower shaft
    rect(pen, -326, -2, 52, 176, (16, 17, 40))
    stroke(pen, -322, 0, -322, 170, (58, 52, 92), 2)
    stroke(pen, -278, 0, -278, 170, (58, 52, 92), 2)

    # lit windows up the tower
    for y in range(10, 160, 24):
        rect(pen, -316, y, 8, 12, (255, 206, 120))
        rect(pen, -292, y, 8, 12, (255, 214, 140))

    # clock room
    rect(pen, -334, 174, 68, 46, (24, 24, 52))
    stroke(pen, -334, 174, -266, 174, (120, 100, 60), 2)

    # belfry
    rect(pen, -322, 220, 44, 26, (18, 19, 42))
    for x in (-316, -300, -284):
        rect(pen, x - 3, 226, 6, 14, (255, 210, 130))

    # spire
    polygon(pen, [(-326, 246), (-300, 296), (-274, 246)],
            (14, 15, 36), (90, 76, 48), 2)
    stroke(pen, -300, 252, -300, 292, (150, 128, 70), 2)

    # clock face
    disc(pen, -300, 197, 19, (168, 132, 60))
    disc(pen, -300, 197, 15, (250, 240, 205))
    stroke(pen, -300, 197, -300, 208, (40, 30, 20), 3)
    stroke(pen, -300, 197, -289, 193, (40, 30, 20), 3)

    BLOCKED.append((-356, GROUND, 112, 372))


# ---------------------------------------------------------------------------
# London Eye (static parts)
# ---------------------------------------------------------------------------
def draw_eye(pen):
    cx, cy = EYE_C
    R = EYE_R

    # support legs
    stroke(pen, cx - 16, GROUND, cx, cy, (62, 78, 110), 5)
    stroke(pen, cx + 16, GROUND, cx, cy, (62, 78, 110), 5)
    stroke(pen, cx - 34, -22, cx + 14, -60, (52, 66, 96), 2)
    stroke(pen, cx + 34, -22, cx - 14, -60, (52, 66, 96), 2)

    # rim
    pen.penup()
    pen.goto(cx, cy - R)
    pen.setheading(0)
    pen.color((150, 176, 214))
    pen.width(2)
    pen.pendown()
    pen.circle(R)
    pen.penup()

    pen.goto(cx, cy - R + 6)
    pen.color((70, 88, 120))
    pen.width(1)
    pen.pendown()
    pen.circle(R - 6)
    pen.penup()

    # spokes
    for i in range(20):
        a = math.radians(i * 18)
        stroke(pen, cx + math.cos(a) * 12, cy + math.sin(a) * 12,
               cx + math.cos(a) * (R - 5), cy + math.sin(a) * (R - 5),
               (70, 86, 118), 1)

    # hub
    disc(pen, cx, cy, 12, (120, 140, 170))
    disc(pen, cx, cy, 9, (255, 244, 214))

    BLOCKED.append((cx - R - 6, cy - R - 6, 2 * R + 12, 2 * R + 12))


# ---------------------------------------------------------------------------
# The Shard
# ---------------------------------------------------------------------------
def draw_shard(pen):
    pts = [(330, GROUND), (352, 150), (378, 318), (404, 150), (426, GROUND)]
    polygon(pen, pts, (18, 28, 52), (120, 178, 214), 2)

    # glass facets
    for x1, x2, top in ((342, 374, 300), (356, 376, 292),
                        (372, 378, 312), (392, 380, 300), (410, 382, 272)):
        stroke(pen, x1, GROUND, x2, top, (64, 104, 142), 1)

    # horizontal floor lines
    for y in range(-56, 272, 22):
        half = 48 * (1 - (y - GROUND) / 392) + 4
        stroke(pen, 378 - half, y, 378 + half, y, (40, 70, 102), 1)

    # a few lit floors
    for _ in range(46):
        y = random.uniform(-60, 250)
        half = 48 * (1 - (y - GROUND) / 392) + 3
        x = 378 + random.uniform(-half, half)
        rect(pen, x, y, 2, 2, (190, 225, 255))

    BLOCKED.append((326, GROUND, 104, 392))


# ---------------------------------------------------------------------------
# street, river and reflections
# ---------------------------------------------------------------------------
def draw_road(pen):
    rect(pen, LEFT, ROAD_BOTTOM, W, ROAD_TOP - ROAD_BOTTOM, ROAD)
    stroke(pen, LEFT, ROAD_TOP, RIGHT, ROAD_TOP, (34, 38, 66), 2)
    stroke(pen, LEFT, ROAD_BOTTOM, RIGHT, ROAD_BOTTOM, (28, 32, 58), 1)


def draw_river(pen):
    bands = 42
    step = (RIVER_TOP - BOTTOM) / bands
    top_colour = (10, 18, 46)
    bottom_colour = (4, 6, 18)
    for i in range(bands):
        y = BOTTOM + i * step
        rect(pen, LEFT, y, W, step + 0.8, mix(bottom_colour, top_colour, i / bands))
    stroke(pen, LEFT, RIVER_TOP, RIGHT, RIVER_TOP, (34, 46, 84), 2)

    # long, calm swells
    for _ in range(28):
        y = random.uniform(BOTTOM + 10, RIVER_TOP - 8)
        x = random.uniform(LEFT, RIGHT - 80)
        stroke(pen, x, y, x + random.uniform(30, 90), y, (16, 24, 52), 2)


def reflect(pen, cx, colour, half, length, strength=1.0):
    y = RIVER_TOP - 8
    while y > RIVER_TOP - length and y > BOTTOM + 4:
        f = (RIVER_TOP - y) / length
        w = half * random.uniform(0.55, 1.0) * (1 - 0.35 * f)
        off = random.uniform(-1, 1) * 5 * (0.3 + f)
        colour_now = mix((6, 10, 30), colour, strength * (1 - 0.75 * f))
        stroke(pen, cx - w + off, y, cx + w + off, y, colour_now, 2)
        y -= random.uniform(6, 11)


def draw_reflections(pen):
    random.seed(11)
    reflect(pen, -392, (210, 198, 158), 26, 215)
    reflect(pen, -300, (255, 190, 105), 34, 215)
    reflect(pen, 44, (255, 156, 196), 15, 235)
    reflect(pen, 60, (140, 196, 255), 20, 250)
    reflect(pen, 78, (255, 216, 150), 14, 220)
    reflect(pen, 378, (150, 200, 235), 38, 235)

    # scattered warm lights from the windows
    for _ in range(60):
        x = random.uniform(LEFT, RIGHT)
        y = random.uniform(RIVER_TOP - 10, RIVER_TOP - 190)
        w = random.uniform(3, 14)
        colour = WARM if random.random() < 0.7 else COOL
        stroke(pen, x, y, x + w, y, mix((6, 10, 30), colour, random.uniform(0.1, 0.4)), 2)


def draw_lamps(pen):
    for x in range(-474, 490, 70):
        stroke(pen, x, GROUND, x, GROUND + 16, (40, 42, 66), 2)
        disc(pen, x, GROUND + 17, 3, (255, 218, 150))


# ---------------------------------------------------------------------------
# the whole static scene
# ---------------------------------------------------------------------------
def draw_scene():
    random.seed(2026)
    pen = new_pen()

    draw_sky(pen)
    draw_moon(pen)
    draw_skyline(pen)
    draw_big_ben(pen)
    draw_eye(pen)
    draw_shard(pen)
    draw_road(pen)
    draw_river(pen)
    draw_reflections(pen)
    draw_lamps(pen)

    screen.update()
    return pen


# ---------------------------------------------------------------------------
# stars (animated with stamps)
# ---------------------------------------------------------------------------
star_pen = new_pen()
star_pen.shape("circle")
stars = []


def build_stars():
    random.seed(41)
    tries = 0
    while len(stars) < 52 and tries < 4000:
        tries += 1
        x = random.uniform(LEFT + 16, RIGHT - 16)
        y = random.uniform(GROUND + 26, TOP - 16)
        if any(bx - 8 <= x <= bx + bw + 8 and by - 8 <= y <= by + bh + 8
               for bx, by, bw, bh in BLOCKED):
            continue
        stars.append({
            "x": x, "y": y,
            "phase": random.uniform(0, 6.283),
            "speed": random.uniform(0.05, 0.17),
            "size": random.uniform(0.10, 0.21),
            "id": None,
        })


def update_stars(frame):
    for s in stars:
        b = 0.5 + 0.5 * math.sin(frame * s["speed"] + s["phase"])
        b = 0.15 + 0.85 * b
        if s["id"] is not None:
            star_pen.clearstamp(s["id"])
        star_pen.goto(s["x"], s["y"])
        star_pen.color(mix((30, 32, 62), (255, 248, 214), b))
        star_pen.shapesize(s["size"] * (0.7 + 0.6 * b))
        s["id"] = star_pen.stamp()


# ---------------------------------------------------------------------------
# London Eye lights
# ---------------------------------------------------------------------------
EYE_LIGHTS = 36
LIGHT_COLOURS = [
    (255, 236, 170), (255, 176, 210), (150, 214, 255),
    (250, 250, 255), (200, 170, 255),
]

eye_pen = new_pen()
eye_pen.shape("circle")
eye_ids = [None] * EYE_LIGHTS


def update_eye(frame):
    cx, cy = EYE_C
    for i in range(EYE_LIGHTS):
        ang = math.radians(i * 360 / EYE_LIGHTS)
        wave = 0.5 + 0.5 * math.sin(math.radians(i * 40) - frame * 0.22)
        colour = LIGHT_COLOURS[(i // 4 + frame // 14) % len(LIGHT_COLOURS)]

        if eye_ids[i] is not None:
            eye_pen.clearstamp(eye_ids[i])
        eye_pen.goto(cx + math.cos(ang) * EYE_R, cy + math.sin(ang) * EYE_R)
        eye_pen.color(mix((40, 44, 66), colour, 0.35 + 0.65 * wave))
        eye_pen.shapesize(0.16 + 0.14 * wave)
        eye_ids[i] = eye_pen.stamp()


# ---------------------------------------------------------------------------
# shimmer on the Thames
# ---------------------------------------------------------------------------
sparkle_pen = new_pen()
sparkle_pen.shape("circle")
sparkles = []


def build_sparkles():
    random.seed(73)
    for _ in range(46):
        sparkles.append({
            "x": random.uniform(LEFT + 10, RIGHT - 10),
            "y": random.uniform(BOTTOM + 14, RIVER_TOP - 14),
            "phase": random.uniform(0, 6.283),
            "speed": random.uniform(0.04, 0.11),
            "cool": random.random() < 0.55,
            "id": None,
        })


def update_water(frame):
    for s in sparkles:
        b = 0.5 + 0.5 * math.sin(frame * s["speed"] + s["phase"])
        if s["id"] is not None:
            sparkle_pen.clearstamp(s["id"])
        x = s["x"] + 7 * math.sin(frame * 0.015 + s["phase"])
        sparkle_pen.goto(x, s["y"])
        base = (140, 190, 255) if s["cool"] else (255, 214, 150)
        sparkle_pen.color(mix((8, 12, 34), base, 0.15 + 0.55 * b))
        sparkle_pen.shapesize(0.05 + 0.06 * b)
        s["id"] = sparkle_pen.stamp()


# ---------------------------------------------------------------------------
# the bus
# ---------------------------------------------------------------------------
BUS_Y = -106
bus_pen = new_pen()
bus_x = -140.0


def draw_bus(pen, x, y):
    rect(pen, x, y, 84, 30, (176, 40, 40))
    rect(pen, x, y + 16, 84, 14, (198, 52, 46))
    stroke(pen, x, y + 29, x + 84, y + 29, (120, 26, 30), 2)

    for i in range(5):                                  # upper deck windows
        rect(pen, x + 6 + i * 15, y + 17, 11, 9, (255, 214, 150))
    for i in range(4):                                  # lower deck windows
        rect(pen, x + 6 + i * 15, y + 5, 11, 8, (250, 236, 200))

    rect(pen, x + 68, y + 4, 10, 21, (96, 30, 30))
    disc(pen, x + 18, y + 1, 7, (18, 18, 26))
    disc(pen, x + 66, y + 1, 7, (18, 18, 26))
    disc(pen, x + 18, y + 1, 3, (120, 120, 140))
    disc(pen, x + 66, y + 1, 3, (120, 120, 140))
    disc(pen, x + 83, y + 8, 3, (255, 240, 170))


def update_bus():
    global bus_x
    bus_pen.clear()
    draw_bus(bus_pen, bus_x, BUS_Y)
    bus_x += 2.2
    if bus_x > RIGHT + 96:
        bus_x = LEFT - 96


# ---------------------------------------------------------------------------
# main loop
# ---------------------------------------------------------------------------
def main():
    draw_scene()
    build_stars()
    build_sparkles()

    frame = 0
    try:
        while True:
            frame += 1
            update_stars(frame)
            update_eye(frame)
            update_water(frame)
            update_bus()
            screen.update()
            time.sleep(0.02)
    except Exception:          # window closed while the loop was running
        pass


if __name__ == "__main__":
    main()
