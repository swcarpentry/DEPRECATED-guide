from turtle import Turtle, mainloop

class Dinosaur(Turtle):
    def __init__(self, distance, color, speed):
        Turtle.__init__(self)
        self.pencolor(color)
        self.speed = speed
        self.penup()
        self.forward(distance)
        self.pendown()

class Duckbill(Dinosaur):
    def __init__(self, distance, color, speed, angle):
        Dinosaur.__init__(self, distance, color, speed)
        self.angle = angle
        self.left(90)

    def move(self):
        self.forward(self.speed)
        self.left(self.angle)

class Raptor(Dinosaur):
    def __init__(self, distance, color, speed):
        Dinosaur.__init__(self, distance, color, speed)

    def move(self, target):
        angle = self.towards(target.pos())
        self.setheading(angle)
        self.forward(self.speed)

class SmartRaptor(Dinosaur):
    def __init__(self, distance, color, speed):
        Dinosaur.__init__(self, distance, color, speed)

    def move(self, target):
        angle = self.towards(target.next_pos())
        self.setheading(angle)
        self.forward(self.speed)

duckbill = Duckbill(200, "green", 8, 6)
raptors = [Raptor(-200, "red", 7.5),
           SmartRaptor(-200, "orange", 7.5)]
for i in range(120):
    for r in raptors:
        r.move(duckbill)
    duckbill.move()

mainloop()
