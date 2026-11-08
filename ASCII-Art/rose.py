import os
import time
import random

RED = "\033[91m"
PINK = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"

rose = [
    "             .-~~~~-.                  ",
    "          .-'  .--.  '-.               ",
    "        .'   .'    '.   '.             ",
    "       /   .'  .--.  '.   \\           ",
    "      |   /   (    )   \\   |          ",
    "      |   |    '--'    |    |          ",
    "       \\   '.        .'   /           ",
    "        '.   '-.__.-'   .'             ",
    "          '-.________.-'               ",
    "                 ||                    ",
    "          _      ||      _             ",
    "         / \\     ||     / \\          ",
    "        /   \\____||____/   \\         ",
    "                 ||                    ",
    "                 ||                    ",
    "                /  \\                  ",
    "               /____\\                 "
]

sparkles = ["✦", "✧", "*", "·", "+"]

colors = [RED, PINK, RED, YELLOW]

for frame in range(30):

    os.system("cls")
    
    flower_color = colors[frame % len(colors)]

    for i, line in enumerate(rose):
        
        if i < 9:
            print(flower_color + line + RESET)

        else:
            print(GREEN + line + RESET)

    print()

    left = random.choice(sparkles)
    right = random.choice(sparkles)
    
    print(PINK + f" {left} {right}" + RESET)
    print(WHITE + "  A little Rose for You" + RESET)

    time.sleep(0.3)

print("\n" + PINK + " Made with Python and Love! " + RESET)