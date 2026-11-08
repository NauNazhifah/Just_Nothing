import os
import time
import random

RESET = "\033[0m"

def rgb(r, g, b):
    return  f"\33[38;3;{r};{g};{b}m"

RED = rgb(255, 45, 75)
PINK = rgb(255, 130, 170)
DARK_RED = rgb(180, 20, 55)
GREEN = rgb(70, 210, 120)
LIGHT_GREEN = rgb(140, 255, 160)
GOLD = rgb(255, 220, 100)
WHITE = rgb(255, 255, 255)

rose = [
    "                 .-~~~~-.                 ",
    "             .-'  .--.  '-.               ",
    "           .'   .'    '.   '.             ",
    "          /   .'  .--.  '.   \\            ",
    "         |   /  .'    '.  \\   |           ",
    "         |  |  /  .--.  \\  |  |           ",
    "          \\  \\ | (    ) | /  /            ",
    "           '.  \\ '.__.' /  .'             ",
    "             '-.______.-'                 ",
    "                  ||                      ",
    "             _____||_____                 ",
    "            /     ||     \\                ",
    "           /      ||      \\               ",
    "                  ||                      ",
    "                  ||                      ",
    "                 /  \\                     ",
    "                /____\\                    "
]

sparkles = ["✦", "✧", "·", "*", "+"]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_rose(frame):
    clear()

    for i, line in enumerate(rose):
        if i < 9:
            color = [RED, PINK, DARK_RED][(i + frame) % 3]
        else:
            color = GREEN if i < 13 else LIGHT_GREEN

        print(color + line + RESET)

    print()

    stars = random.sample(sparkles, 3)

    print(GOLD + f"     {stars[0]}      {stars[1]}      {stars[2]} + RESET")
    print()
    print(WHITE + "     A LITLE ROSE FOR YOU" + RESET)
    print(PINK + "               ♡" + RESET)

def main():
    for frame in range(30):
        show_rose(frame)
        time.sleep(0.25)

    print()
    print(GOLD + "      MADE WITH LOVE  ♡" + RESET)

if __name__ == "__main__":
    main()
