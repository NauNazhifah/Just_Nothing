
import pygame
import random

pygame.init()

# WINDOW
WIDTH, HEIGHT = 720, 700
SCALE = 14

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Rose - Bloom")

clock = pygame.time.Clock()

# COLOR PALETTE
C = {
    "D": (105, 12, 38),       # Shadow
    "R": (190, 20, 55),       # Deep red
    "r": (225, 35, 70),       # Red
    "P": (250, 75, 115),      # Pink
    "L": (255, 145, 175),     # Highlight
    "Y": (255, 205, 115),     # Center
    "G": (35, 115, 65),       # Dark green
    "g": (55, 165, 85),       # Green
    "H": (115, 205, 110),     # Leaf highlight
}

BG = (25, 20, 39)
BG_LIGHT = (43, 31, 60)

# ROSE PIXEL DESIGN
art = [
    "          DDDDD          ",
    "       DDDrrrPPDD        ",
    "     DDRRrrrPPPrrD       ",
    "    DRRRRRrrrPPrrrD      ",
    "   DRRRPPPRRRrrrPrrD     ",
    "  DRRRPPPPPRRrrrPrrrD    ",
    "  DRRRRPPPRRRRrrrRRrD    ",
    "   DRRRRRRRRRrrrRRRD     ",
    "    DRRRRRRRRRRRRRD      ",
    "      DRRRRRRRRRD        ",
    "        DDDDDDD          ",
    "           G             ",
    "           G             ",
    "      HHHggG             ",
    "     HHHHggG             ",
    "      HHHggG             ",
    "           GGG           ",
    "           GGGg          ",
    "           GGGgg         ",
    "           GGG           ",
    "          GGG            ",
    "         GGG  G          ",
    "        GGG    GG        ",
    "       GGG      GG       ",
    "      GGG        G       ",
]

# CREATE PIXEL CANVAS
ART_WIDTH = max(len(row) for row in art)
ART_HEIGHT = len(art)

canvas = pygame.Surface((ART_WIDTH, ART_HEIGHT))

# SPARKLES
sparkles = [
    (3, 5), (21, 4), (1, 15),
    (23, 16), (5, 22), (20, 24)
]

# DRAW ROSE
def draw_rose():
    canvas.fill(BG)

    for y, row in enumerate(art):
        for x, char in enumerate(row):
            if char in C:
                pygame.draw.rect(
                    canvas,
                    C[char],
                    (x, y, 1, 1)
                )

# DRAW SPARKLES
def draw_sparkles(frame):
    for i, (x, y) in enumerate(sparkles):
        if (frame // 10 + i) % 2 == 0:
            color = (255, 220, 145)
            pygame.draw.rect(canvas, color, (x, y, 1, 1))
            pygame.draw.rect(canvas, color, (x - 1, y, 3, 1))
            pygame.draw.rect(canvas, color, (x, y - 1, 1, 3))

# TEXT
title_font = pygame.font.SysFont("consolas", 28, bold=True)
small_font = pygame.font.SysFont("consolas", 17)

title = title_font.render(
    "A LITTLE ROSE FOR YOU",
    True, (255, 150, 180)
)

subtitle = small_font.render(
    "MADE WITH LOVE",
    True, (205, 170, 220)
)

# MAIN LOOP
running = True
frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG)

    # Background decoration
    pygame.draw.rect(screen, BG_LIGHT, (0, 0, WIDTH, 5))
    pygame.draw.rect(screen, BG_LIGHT, (0, HEIGHT - 5, WIDTH, 5))

    draw_rose()
    draw_sparkles(frame)

    # Enlarge without blur
    enlarged = pygame.transform.scale(
        canvas,
        (ART_WIDTH * SCALE, ART_HEIGHT * SCALE)
    )

    screen.blit(
        enlarged,
        ((WIDTH - enlarged.get_width()) // 2, 80)
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 550)
    )

    screen.blit(
        subtitle,
        (WIDTH // 2 - subtitle.get_width() // 2, 595)
    )

    pygame.display.flip()

    clock.tick(30)
    frame += 1

pygame.quit()
