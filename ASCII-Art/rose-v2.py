
import os
import time

RESET = "\033[0m"

def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

COLORS = {
    "R": rgb(220, 25, 55),
    "P": rgb(255, 90, 130),
    "L": rgb(255, 160, 185),
    "D": rgb(140, 15, 45),
    "G": rgb(35, 150, 75),
    "H": rgb(100, 220, 115),
    "Y": rgb(255, 220, 100),
}

art = [
    "       PPPPP       ",
    "     PPRRRRPP     ",
    "    PRRRRRRRRP    ",
    "   PRRPPPRRRRRP   ",
    "  PRRPPPPPRRRRRP  ",
    "  PRRPPPPPRRRRRP  ",
    "   PRRPPPRRRRRP   ",
    "    PRRRRRRRRP    ",
    "     PPRRRRPP     ",
    "       DDD        ",
    "        G         ",
    "       GGG        ",
    "      GGHGG       ",
    "     GGGGGGG      ",
    "        G         ",
    "        G         ",
    "       G G        ",
    "      G   G       ",
    "     GG   GG      ",
]

for frame in range(20):
    os.system("cls")

    print()

    print("       " + COLORS["Y"] + "✦" + RESET +
          "                  " + COLORS["Y"] + "✧" + RESET)

    print()

    for row in art:
        for pixel in row:
            if pixel == " ":
                print("  ", end="")
            else:
                print(COLORS[pixel] + "██" + RESET, end="")
        print()

    print()
    print(COLORS["Y"] + "      ✧       ✦       ✧" + RESET)
    print()
    print(COLORS["L"] + "       A LITTLE ROSE FOR YOU" + RESET)
    print(COLORS["P"] + "                ♡" + RESET)
    print()

    time.sleep(0.3)
