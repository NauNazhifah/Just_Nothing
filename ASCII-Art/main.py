
import os
import time
import random

RED = "\033[91m"
PINK = "\033[95m"
GREEN = "\033[92m"
WHITE = "\033[97m"
RESET = "\033[0m"

rose = [
    "          .-~~~~-.          ",
    "       .-'  .--.  '-.       ",
    "      /   .'    '.   \\      ",
    "     |   /  .--.  \\   |     ",
    "      \\  | (    ) |  /      ",
    "       '.\\  '--' /.'        ",
    "         '-.____.-'          ",
    "             ||              ",
    "        _____||_____         ",
    "       /     ||     \\        ",
    "      /      ||      \\       ",
    "             ||              ",
    "             ||              ",
    "            /  \\             ",
    "           /____\\            "
]

envelope = [
    "       ___________________       ",
    "      /                   \\      ",
    "     /                     \\     ",
    "    /                       \\    ",
    "   /_________________________\\   ",
    "   \\                         /   ",
    "    \\                       /    ",
    "     \\_____________________/     "
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def show_rose():
    clear()

    for i, line in enumerate(rose):
        if i < 7:
            print(RED + line + RESET)
        else:
            print(GREEN + line + RESET)

    print()
    print(PINK + "      A LITTLE ROSE FOR YOU ♡" + RESET)


def show_envelope():
    clear()

    for line in envelope:
        print(PINK + line + RESET)

    print()
    print(WHITE + "      A LETTER FOR YOU ♡" + RESET)


def main():
    for frame in range(5):
        show_rose()
        time.sleep(0.7)

        show_envelope()
        time.sleep(0.7)

    clear()
    print(RED + "       MADE WITH LOVE ♡" + RESET)


main()