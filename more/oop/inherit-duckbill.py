from turtle import Turtle, mainloop

class Duckbill(Turtle):
    def __init__(self, distance, color, speed, angle):
        Turtle.__init__(self)
        self.pencolor(color)
        self.speed = speed
        self.angle = angle

        self.penup()
        self.forward(distance)
        self.pendown()
        self.left(90)

    def move(self):
        self.forward(self.speed)
        self.left(self.angle)

duckbill = Duckbill(200, "green", 8, 6)

for i in range(120):
    duckbill.move()

mainloop()
