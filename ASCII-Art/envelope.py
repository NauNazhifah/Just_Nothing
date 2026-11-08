import os
import time

PINK = '\033[95m'
RED = '\033[91m'
WHITE = '\033[97m'
RESET = '\033[0m'

closed = [
    "       ___________________       ",
    "      /                   \\      ",
    "     /                     \\     ",
    "    /                       \\    ",
    "   /_________________________\\   ",
    "   \\                         /   ",
    "    \\                       /    ",
    "     \\_____________________/     "
]

opened = [
    "       ___________________       ",
    "      \\        ♥          /      ",
    "       \\                 /       ",
    "        \\_______________/        ",
    "        |               |        ",
    "        |   DEAR YOU    |        ",
    "        |   ♥  ♥  ♥     |        ",
    "        |_______________|        "
]

for frame in range(6):

    os.system("cls")

    if frame % 2 == 0:
        picture = closed
    else:
        picture = opened

    for line in picture:
        print(PINK + line + RESET)

    print()
    print(WHITE + "     A LETTER FOR YOU ♡" + RESET)

    time.sleep(0.6)

os.system("cls")

for line in opened:
    print(RED + line + RESET)

print()
print(WHITE + "         WITH LOVE, ALWAYS ♡" + RESET)