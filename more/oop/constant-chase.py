from turtle import Turtle, mainloop

def setup(color, distance):
    t = Turtle()
    t.pencolor(color)
    t.penup()
    t.forward(distance)
    t.pendown()
    return t

raptor = setup("red", -200)
duckbill = setup("green", 200)

for i in range(20):
    raptor.forward(10)
    duckbill.forward(10)

mainloop()
