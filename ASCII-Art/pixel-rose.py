
import pygame
import random
import math

pygame.init()

# ==================================================
# 1. WINDOW & SETTINGS
# ==================================================

WIDTH = 700
HEIGHT = 700

PIXEL = 5
ART_SIZE = 128

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blooming Rose | A Little Rose for You")

clock = pygame.time.Clock()

canvas = pygame.Surface((ART_SIZE, ART_SIZE), pygame.SRCALPHA)

# ==================================================
# 2. COLOR PALETTE
# ==================================================

BG_TOP = (19, 16, 35)
BG_BOTTOM = (43, 25, 53)

SHADOW = (75, 8, 35)
DARK_RED = (120, 12, 42)
CRIMSON = (165, 18, 50)
RED = (205, 27, 61)
ROSE = (235, 52, 88)
PINK = (250, 91, 125)
LIGHT_PINK = (255, 145, 166)
PALE_PINK = (255, 190, 200)

DARK_GREEN = (22, 82, 52)
GREEN = (35, 125, 70)
MID_GREEN = (54, 157, 83)
LIGHT_GREEN = (105, 195, 105)

GOLD = (255, 215, 135)
STAR_WHITE = (255, 235, 220)

# ==================================================
# 3. DRAWING HELPERS
# ==================================================

def polygon(surface, color, points):
    pygame.draw.polygon(surface, color, points)


def pixel(surface, x, y, color, size=1):
    pygame.draw.rect(
        surface,
        color,
        (x, y, size, size)
    )


def line(surface, color, start, end, width=1):
    pygame.draw.line(surface, color, start, end, width)


# ==================================================
# 4. DRAW LEAVES
# ==================================================

def draw_leaves():
    # Left leaf shadow
    polygon(canvas, DARK_GREEN, [
        (61, 89), (53, 79), (40, 75),
        (25, 77), (35, 88), (49, 94)
    ])

    # Left leaf body
    polygon(canvas, GREEN, [
        (59, 89), (51, 81), (39, 78),
        (29, 79), (38, 86), (50, 91)
    ])

    # Left leaf highlight
    polygon(canvas, MID_GREEN, [
        (55, 87), (47, 81), (36, 80),
        (43, 85), (51, 89)
    ])

    # Right leaf shadow
    polygon(canvas, DARK_GREEN, [
        (67, 96), (76, 83), (91, 78),
        (105, 81), (95, 91), (79, 99)
    ])

    # Right leaf body
    polygon(canvas, GREEN, [
        (68, 95), (78, 85), (91, 81),
        (100, 82), (91, 90), (79, 96)
    ])

    # Right leaf highlight
    polygon(canvas, MID_GREEN, [
        (75, 91), (84, 85), (96, 83),
        (88, 89), (79, 94)
    ])

    # Leaf veins
    line(canvas, LIGHT_GREEN, (60, 89), (34, 80))
    line(canvas, LIGHT_GREEN, (69, 95), (97, 83))

    # Small leaf on upper stem
    polygon(canvas, DARK_GREEN, [
        (64, 80), (54, 73), (44, 72),
        (52, 81), (63, 84)
    ])

    polygon(canvas, MID_GREEN, [
        (62, 80), (54, 75), (48, 74),
        (55, 80), (62, 82)
    ])


# ==================================================
# 5. DRAW STEM
# ==================================================

def draw_stem():
    polygon(canvas, DARK_GREEN, [
        (62, 65), (67, 65), (71, 116),
        (65, 118), (62, 91)
    ])

    polygon(canvas, GREEN, [
        (63, 67), (66, 67), (68, 114),
        (65, 115)
    ])

    line(canvas, LIGHT_GREEN, (64, 73), (66, 108))


# ==================================================
# 6. DRAW OUTER PETALS
# ==================================================

def draw_outer_petals():
    # Left outer petal
    polygon(canvas, SHADOW, [
        (63, 48), (49, 61), (35, 65),
        (21, 57), (18, 43), (23, 29),
        (34, 22), (47, 28), (55, 39)
    ])

    polygon(canvas, CRIMSON, [
        (61, 47), (48, 59), (35, 62),
        (24, 55), (22, 43), (27, 32),
        (36, 26), (47, 31), (55, 41)
    ])

    # Left petal light
    polygon(canvas, RED, [
        (51, 43), (43, 34), (34, 32),
        (28, 39), (30, 49), (39, 56),
        (48, 54)
    ])

    # Right outer petal
    polygon(canvas, SHADOW, [
        (65, 48), (77, 34), (91, 24),
        (106, 29), (113, 41), (110, 56),
        (97, 65), (81, 62), (70, 55)
    ])

    polygon(canvas, CRIMSON, [
        (67, 47), (80, 36), (92, 29),
        (104, 33), (109, 43), (106, 54),
        (96, 61), (82, 59), (71, 53)
    ])

    # Right petal light
    polygon(canvas, RED, [
        (77, 47), (88, 36), (99, 35),
        (104, 44), (101, 53), (91, 57),
        (81, 54)
    ])

    # Lower outer petal
    polygon(canvas, SHADOW, [
        (29, 51), (43, 56), (63, 61),
        (84, 56), (102, 50), (99, 65),
        (87, 75), (67, 79), (46, 73),
        (34, 64)
    ])

    polygon(canvas, DARK_RED, [
        (33, 54), (46, 59), (64, 64),
        (82, 59), (97, 54), (94, 64),
        (83, 71), (66, 75), (47, 70),
        (37, 63)
    ])

    polygon(canvas, RED, [
        (43, 62), (55, 65), (68, 66),
        (83, 62), (91, 59), (83, 69),
        (67, 72), (52, 68)
    ])


# ==================================================
# 7. DRAW INNER PETALS
# ==================================================

def draw_inner_petals():
    # Back inner petal
    polygon(canvas, DARK_RED, [
        (43, 44), (45, 30), (55, 20),
        (68, 18), (79, 25), (82, 39),
        (72, 50), (57, 52)
    ])

    polygon(canvas, RED, [
        (47, 42), (49, 31), (57, 24),
        (68, 22), (76, 28), (78, 39),
        (70, 47), (58, 49)
    ])

    # Upper left petal
    polygon(canvas, DARK_RED, [
        (34, 43), (35, 31), (45, 21),
        (57, 24), (61, 36), (53, 48),
        (43, 52)
    ])

    polygon(canvas, ROSE, [
        (38, 40), (39, 32), (47, 26),
        (55, 29), (57, 37), (50, 46),
        (43, 48)
    ])

    # Upper right petal
    polygon(canvas, DARK_RED, [
        (68, 37), (75, 24), (88, 22),
        (98, 33), (95, 46), (83, 52),
        (72, 47)
    ])

    polygon(canvas, ROSE, [
        (72, 37), (78, 29), (87, 27),
        (93, 35), (91, 44), (82, 48),
        (74, 44)
    ])

    # Center spiral petal
    polygon(canvas, CRIMSON, [
        (51, 42), (57, 34), (68, 31),
        (78, 37), (80, 46), (72, 54),
        (59, 55), (50, 50)
    ])

    polygon(canvas, PINK, [
        (55, 42), (61, 37), (69, 36),
        (75, 41), (73, 47), (66, 51),
        (57, 48)
    ])

    polygon(canvas, LIGHT_PINK, [
        (60, 42), (65, 39), (70, 41),
        (69, 45), (64, 47), (60, 45)
    ])


# ==================================================
# 8. PETAL PIXEL DETAILS
# ==================================================

def draw_petals_details():
    # Light catching the upper petals
    highlights = [
        (45, 28, 3, 2),
        (49, 25, 3, 1),
        (53, 29, 2, 2),
        (76, 29, 3, 2),
        (81, 27, 3, 1),
        (87, 31, 2, 2),
        (31, 37, 3, 2),
        (27, 43, 2, 3),
        (96, 41, 3, 2),
        (99, 47, 2, 2),
    ]

    for x, y, w, h in highlights:
        pygame.draw.rect(
            canvas,
            PINK,
            (x, y, w, h)
        )

    # Bright pink accents
    accents = [
        (47, 31), (51, 32), (54, 35),
        (77, 33), (82, 31), (88, 36),
        (34, 44), (39, 49), (92, 48)
    ]

    for x, y in accents:
        pixel(canvas, x, y, LIGHT_PINK, 2)

    # Dark folds between petals
    folds = [
        (40, 52), (44, 54), (48, 56),
        (78, 53), (83, 51), (88, 50),
        (57, 57), (66, 59), (72, 56)
    ]

    for x, y in folds:
        pixel(canvas, x, y, DARK_RED, 2)


# ==================================================
# 9. FLOWER CENTER
# ==================================================

def draw_center():
    # Small spiral-like center
    polygon(canvas, DARK_RED, [
        (57, 39), (65, 35), (74, 39),
        (76, 46), (70, 52), (61, 51),
        (55, 46)
    ])

    polygon(canvas, PINK, [
        (60, 40), (66, 38), (72, 42),
        (71, 47), (66, 49), (60, 46)
    ])

    polygon(canvas, LIGHT_PINK, [
        (63, 41), (68, 40), (70, 44),
        (67, 47), (63, 45)
    ])

    pixel(canvas, 65, 42, PALE_PINK, 2)


# ==================================================
# 10. COMPLETE ROSE
# ==================================================

def draw_rose():
    canvas.fill((0, 0, 0, 0))

    draw_stem()
    draw_leaves()

    draw_outer_petals()
    draw_inner_petals()
    draw_petals_details()
    draw_center()


# ==================================================
# 11. ANIMATED SPARKLES
# ==================================================

stars = [
    (14, 27),
    (109, 26),
    (16, 58),
    (110, 61),
    (36, 12),
    (94, 12),
    (24, 91),
    (105, 91)
]

def draw_star(surface, x, y, color):
    pixel(surface, x, y, color, 1)
    pixel(surface, x - 1, y, color, 1)
    pixel(surface, x + 1, y, color, 1)
    pixel(surface, x, y - 1, color, 1)
    pixel(surface, x, y + 1, color, 1)


# ==================================================
# 12. BACKGROUND
# ==================================================

def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        color = (
            int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio),
            int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio),
            int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        )

        pygame.draw.line(
            screen,
            color,
            (0, y),
            (WIDTH, y)
        )


# Background stars
background_stars = [
    (
        random.randint(15, WIDTH - 15),
        random.randint(20, HEIGHT - 120),
        random.choice([1, 2])
    )
    for _ in range(65)
]


# ==================================================
# 13. TYPOGRAPHY
# ==================================================

title_font = pygame.font.SysFont(
    "georgia",
    36,
    bold=True
)

subtitle_font = pygame.font.SysFont(
    "consolas",
    17
)

footer_font = pygame.font.SysFont(
    "consolas",
    13
)

title = title_font.render(
    "A Little Rose For You",
    True,
    (255, 180, 195)
)

subtitle = subtitle_font.render(
    "a small flower, with a lot of love",
    True,
    (220, 190, 215)
)

footer = footer_font.render(
    "MADE WITH LOVE  |  2026",
    True,
    (165, 140, 180)
)


# ==================================================
# 14. MAIN LOOP
# ==================================================

running = True
frame = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background
    draw_background()

    # Background stars
    for x, y, size in background_stars:
        pygame.draw.circle(
            screen,
            (105, 85, 135),
            (x, y),
            size
        )

    # Draw flower
    draw_rose()

    # Animate sparkles on canvas
    for i, (x, y) in enumerate(stars):

        visible = (frame // 15 + i) % 3 != 0

        if visible:
            draw_star(
                canvas,
                x,
                y,
                GOLD
            )

    # Enlarge pixel art without blur
    enlarged = pygame.transform.scale(
        canvas,
        (ART_SIZE * PIXEL, ART_SIZE * PIXEL)
    )

    # Center the rose
    rose_x = (WIDTH - enlarged.get_width()) // 2
    rose_y = 45

    screen.blit(
        enlarged,
        (rose_x, rose_y)
    )

    # Text
    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            820
        )
    )

    screen.blit(
        subtitle,
        (
            WIDTH // 2 - subtitle.get_width() // 2,
            860
        )
    )

    screen.blit(
        footer,
        (
            WIDTH // 2 - footer.get_width() // 2,
            883
        )
    )

    pygame.display.flip()

    clock.tick(30)
    frame += 1

pygame.quit()
