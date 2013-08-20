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
duckbill.left(90)

for i in range(80):
    target = duckbill.pos()
    angle = raptor.towards(target)
    raptor.setheading(angle)
    raptor.forward(5)
    duckbill.forward(5)

mainloop()
