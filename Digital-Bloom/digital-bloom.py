
import pygame
import math
import random

pygame.init()

# ==========================================
# 1. WINDOW
# ==========================================

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DIGITAL BLOOM")

clock = pygame.time.Clock()

BLACK = (5, 4, 15)

# ==========================================
# 2. FLOWER SETTINGS
# ==========================================

CENTER_X = WIDTH // 2
CENTER_Y = 310

PETAL_COUNT = 8
PETAL_SIZE = 190
PARTICLE_COUNT = 9000

particles = []

# ==========================================
# 3. PARTICLE GENERATION
# ==========================================

for i in range(PARTICLE_COUNT):

    angle = random.uniform(0, math.tau)

    # Rounded petal geometry
    petal_shape = (
        0.20 + 0.80 *
        ((1 + math.cos(PETAL_COUNT * angle)) / 2) ** 1.4
    )

    max_radius = PETAL_SIZE * petal_shape

    distance = math.sqrt(random.random())
    radius = max_radius * distance

    x = CENTER_X + radius * math.cos(angle)
    y = CENTER_Y + radius * math.sin(angle)

    # Violet to electric blue gradient
    t = (math.sin(angle * 2 + radius * 0.015) + 1) / 2

    purple = (190, 105, 255)
    blue = (75, 145, 255)

    color = tuple(
        int(purple[j] * (1 - t) + blue[j] * t)
        for j in range(3)
    )

    if random.random() < 0.12:
        color = (230, 165, 255)

    size = random.choice([1, 1, 2, 2, 2, 3])

    particles.append((x, y, color, size))

# ==========================================
# 4. GLOW EFFECT
# ==========================================

glow = pygame.Surface(
    (WIDTH, HEIGHT),
    pygame.SRCALPHA
)

for x, y, color, size in particles:

    pygame.draw.circle(
        glow,
        (*color, 22),
        (int(x), int(y)),
        5
    )

# ==========================================
# 5. MAIN LOOP
# ==========================================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Soft particle glow
    screen.blit(
        glow,
        (0, 0),
        special_flags=pygame.BLEND_ADD
    )

    # Main particles
    for x, y, color, size in particles:

        pygame.draw.circle(
            screen,
            color,
            (int(x), int(y)),
            size
        )

    # ======================================
    # FLOWER CENTER
    # ======================================

    pygame.draw.circle(
        screen, (75, 35, 130),
        (CENTER_X, CENTER_Y), 25
    )

    pygame.draw.circle(
        screen, (150, 90, 255),
        (CENTER_X, CENTER_Y), 15
    )

    pygame.draw.circle(
        screen, (230, 195, 255),
        (CENTER_X, CENTER_Y), 7
    )

    pygame.draw.circle(
        screen, (255, 255, 255),
        (CENTER_X, CENTER_Y), 3
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()