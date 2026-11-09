
import pygame
import math
import random

pygame.init()

# ==========================================
# 1. WINDOW SETTINGS
# ==========================================

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DIGITAL BLOOM")

clock = pygame.time.Clock()

# ==========================================
# 2. COLORS
# ==========================================

BLACK = (5, 5, 12)
VIOLET = (170, 80, 255)
BLUE = (80, 150, 255)

# ==========================================
# 3. FLOWER SETTINGS
# ==========================================

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

PETAL_SIZE = 190
PARTICLE_COUNT = 2500

particles = []

for i in range(PARTICLE_COUNT):

    angle = random.uniform(0, math.tau)
    distance = random.random()

    radius = PETAL_SIZE * abs(math.cos(4 * angle)) * distance

    x = CENTER_X + radius * math.cos(angle)
    y = CENTER_Y + radius * math.sin(angle)

    color_mix = random.random()

    color = (
        int(VIOLET[0] * (1 - color_mix) + BLUE[0] * color_mix),
        int(VIOLET[1] * (1 - color_mix) + BLUE[1] * color_mix),
        int(VIOLET[2] * (1 - color_mix) + BLUE[2] * color_mix)
    )

    particles.append((x, y, color))

# ==========================================
# 4. MAIN LOOP
# ==========================================

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Draw flower particles
    for x, y, color in particles:
        pygame.draw.circle(
            screen,
            color,
            (int(x), int(y)),
            2
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
