
import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 700
SCALE = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blooming Rose")

clock = pygame.time.Clock()

# Palette
BG = (24, 20, 39)
DARK = (100, 10, 35)
RED = (185, 18, 48)
ROSE = (230, 35, 70)
PINK = (250, 85, 125)
LIGHT = (255, 155, 180)

GREEN_DARK = (30, 105, 55)
GREEN = (45, 155, 75)
GREEN_LIGHT = (105, 205, 110)

GOLD = (255, 220, 135)

# Small pixel canvas
canvas = pygame.Surface((80, 65))

def rect(x, y, w, h, color):
    pygame.draw.rect(canvas, color, (x, y, w, h))

def draw_rose():
    canvas.fill(BG)

    # STEM
    rect(39, 34, 3, 20, GREEN_DARK)
    rect(40, 35, 1, 18, GREEN)

    # LEFT LEAF
    rect(24, 38, 10, 2, GREEN_DARK)
    rect(27, 35, 8, 3, GREEN)
    rect(23, 40, 9, 2, GREEN)
    rect(25, 37, 6, 2, GREEN_LIGHT)
    rect(28, 34, 3, 2, GREEN_LIGHT)

    # RIGHT LEAF
    rect(44, 43, 10, 2, GREEN_DARK)
    rect(44, 40, 8, 3, GREEN)
    rect(47, 45, 8, 2, GREEN)
    rect(47, 41, 5, 2, GREEN_LIGHT)

    # OUTER PETALS
    rect(22, 17, 8, 7, DARK)
    rect(28, 12, 8, 10, RED)
    rect(36, 10, 10, 12, ROSE)
    rect(46, 13, 8, 10, RED)
    rect(52, 18, 7, 7, DARK)

    # LOWER PETALS
    rect(25, 23, 10, 6, DARK)
    rect(32, 25, 16, 6, RED)
    rect(45, 23, 11, 6, DARK)
    rect(29, 27, 22, 5, RED)

    # INNER PETALS
    rect(31, 15, 7, 9, PINK)
    rect(37, 13, 8, 10, LIGHT)
    rect(44, 16, 6, 8, PINK)

    # PETAL FOLDS
    rect(25, 20, 5, 3, ROSE)
    rect(30, 25, 6, 2, PINK)
    rect(48, 22, 6, 3, ROSE)
    rect(40, 23, 5, 3, LIGHT)

    # CENTER
    rect(37, 18, 5, 5, RED)
    rect(39, 17, 3, 4, PINK)
    rect(40, 18, 2, 2, LIGHT)

    # SMALL PETAL DETAILS
    rect(33, 12, 3, 2, LIGHT)
    rect(46, 14, 3, 2, PINK)
    rect(28, 23, 3, 2, PINK)
    rect(51, 24, 3, 2, ROSE)

# SPARKLES
sparkles = [
    (13, 15), (65, 13),
    (17, 30), (63, 32),
    (30, 8), (55, 8)
]

def draw_sparkles(frame):
    for i, (x, y) in enumerate(sparkles):
        if (frame // 12 + i) % 2 == 0:
            rect(x, y, 1, 1, GOLD)
            rect(x - 1, y, 3, 1, GOLD)
            rect(x, y - 1, 1, 3, GOLD)

# TEXT
font = pygame.font.SysFont("consolas", 27, bold=True)
small = pygame.font.SysFont("consolas", 17)

title = font.render(
    "A LITTLE ROSE FOR YOU",
    True, (255, 150, 180)
)

subtitle = small.render(
    "MADE WITH LOVE",
    True, (210, 170, 220)
)

# LOOP
running = True
frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG)

    draw_rose()
    draw_sparkles(frame)

    enlarged = pygame.transform.scale(
        canvas,
        (800, 650)
    )

    screen.blit(enlarged, (0, 0))

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 580)
    )

    screen.blit(
        subtitle,
        (WIDTH // 2 - subtitle.get_width() // 2, 620)
    )

    pygame.display.flip()

    clock.tick(30)
    frame += 1

pygame.quit()