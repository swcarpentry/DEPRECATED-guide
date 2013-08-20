from turtle import Turtle, mainloop

class Raptor(object):
    def __init__(self, distance, color, speed):
        self.turtle = Turtle()
        self.speed = speed
        self.turtle.pencolor(color)

        self.turtle.penup()
        self.turtle.forward(distance)
        self.turtle.pendown()

    def move(self, target):
        angle = self.turtle.towards(target)
        self.turtle.setheading(angle)
        self.turtle.forward(self.speed)

class Duckbill(object):
    def __init__(self, distance, color, speed, angle):
        self.turtle = Turtle()
        self.turtle.pencolor(color)
        self.speed = speed
        self.angle = angle

        self.turtle.penup()
        self.turtle.forward(distance)
        self.turtle.pendown()
        self.turtle.left(90)

    def move(self):
        self.turtle.forward(self.speed)
        self.turtle.left(self.angle)

raptors = [Raptor(-200, "red",    5),
           Raptor(-200, "orange", 7),
           Raptor(-200, "yellow", 9)]

duckbill = Duckbill(200, "green", 8, 6)

for i in range(240):
    for r in raptors:
        r.move(duckbill.turtle.pos())
    duckbill.move()

mainloop()
