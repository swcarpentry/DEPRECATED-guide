from turtle import Turtle, mainloop

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

duckbill = Duckbill(200, "green", 8, 6)

for i in range(120):
    duckbill.move()

mainloop()
