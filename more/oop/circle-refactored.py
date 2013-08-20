from turtle import Turtle, mainloop

def setup(color, distance):
    t = Turtle()
    t.pencolor(color)
    t.penup()
    t.forward(distance)
    t.pendown()
    return t

def move_raptor(raptor, duckbill, distance):
    target = duckbill.pos()
    angle = raptor.towards(target)
    raptor.setheading(angle)
    raptor.forward(distance)

def move_duckbill(duckbill, distance, angle):
    duckbill.forward(distance)
    duckbill.left(angle)

raptor = setup("red", -200)
duckbill = setup("green", 200)
duckbill.left(90)

for i in range(240):
    move_raptor(raptor, duckbill, 5)
    move_duckbill(duckbill, 8, 6)

mainloop()
