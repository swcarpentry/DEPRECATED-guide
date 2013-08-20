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

Raptor_Specs = [
    ["red",    5],
    ["orange", 7],
    ["yellow", 9]
]

raptors = []
for (color, speed) in Raptor_Specs:
    r = setup(color, -200)
    raptors.append(r)

duckbill = setup("green", 200)
duckbill.left(90)

for i in range(240):
    for i in range(len(Raptor_Specs)):
        speed = Raptor_Specs[i][1]
        move_raptor(raptors[i], duckbill, speed)
    move_duckbill(duckbill, 8, 6)

mainloop()
