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

for i in range(240):
    # Move the velociraptor toward the hadrosaur.
    target = duckbill.pos()
    angle = raptor.towards(target)
    raptor.setheading(angle)
    raptor.forward(5)

    # Move the hadrosaur in a circle.
    duckbill.forward(8)
    duckbill.left(6)

mainloop()
