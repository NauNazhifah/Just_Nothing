
import os
import time

RESET = "\033[0m"

def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

RED = rgb(245, 45, 75)
PINK = rgb(255, 130, 175)
LIGHT_PINK = rgb(255, 190, 210)
GREEN = rgb(65, 190, 105)
LIGHT_GREEN = rgb(130, 230, 145)
GOLD = rgb(255, 220, 120)
WHITE = rgb(255, 255, 255)

rose = [
    ('             .-""""-.', PINK),
    ("          .-'  .--.  '-.", PINK),
    ("        .'   .'    '.   '.", RED),
    ("       /   .'  .--.  '.   \\", RED),
    ("      ;   /   /    \\   \\   ;", RED),
    ("      |  |   |  ()  |   |  |", LIGHT_PINK),
    ("      ;   \\   \\____/   /   ;", RED),
    ("       \\   '.        .'   /", PINK),
    ("        '.   '-.__.-'   .'", PINK),
    ("          '-._______.-'", RED),
    ("               ||", GREEN),
    ("       .-------||-------.", LIGHT_GREEN),
    ("      /        ||        \\ ", GREEN),
    ("     /    _____||_____    \\ ", LIGHT_GREEN),
    ("               ||", GREEN),
    ("          _____||_____", GREEN),
    ("         /     ||     \\", LIGHT_GREEN),
    ("               ||", GREEN),
    ("              /  \\", GREEN),
    ("             /____\\", LIGHT_GREEN),
]

sparkles = ["✦", "✧", "·", "✧", "✦", "·"]

for frame in range(12):
    os.system("cls")

    print()

    print(GOLD + f"       {sparkles[frame % 6]}                 {sparkles[(frame + 2) % 6]}" + RESET)

    print()

    for line, color in rose:
        print(color + line + RESET)

    print()

    print(GOLD + f"    {sparkles[(frame + 1) % 6]}       {sparkles[(frame + 3) % 6]}       {sparkles[(frame + 5) % 6]}" + RESET)

    print()

    print(LIGHT_PINK + "       A LITTLE ROSE FOR YOU" + RESET)
    print(WHITE + "                ♡" + RESET)

    print()
    print(PINK + "        MADE WITH LOVE  ♡" + RESET)

    time.sleep(0.25)
