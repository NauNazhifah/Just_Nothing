
import turtle
import math
import colorsys

screen = turtle.Screen()
screen.bgcolor("black")
screen.colormode(1.0)
screen.setup(800, 800)
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(2)

N = 50
layers = 30

for j in range(layers):
    scale = 5 + j * 0.7

    t.pencolor(colorsys.hsv_to_rgb(j / layers, 1, 1))

    for i in range(N + 1):
        a = 2 * math.pi * i / N

        x = 16 * math.sin(a)**3
        y = (13 * math.cos(a)
             - 5 * math.cos(2*a)
             - 2 * math.cos(3*a)
             - math.cos(4*a))

        x *= scale
        y *= scale

        if i == 0:
            t.penup()
            t.goto(x, y)
            t.pendown()
        else:
            t.goto(x, y)

    screen.update()

turtle.done()
