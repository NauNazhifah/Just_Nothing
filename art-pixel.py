import turtle, colorsys

# Configurar pantalla
screen = turtle.Screen()
screen.bgcolor("black")

# Configurar tortuga
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# Dibujar espiral
for i in range(150):

# Color HSV: tono desde rojo hasta naranja/amarillo
    t.pencolor(colorsys.hsv_to_rgb(0.12 - i / 150 * 0.12, 1, 1))
    t.forward(i * 2.8)
    t.right(165)
# Finalizar
turtle.done()