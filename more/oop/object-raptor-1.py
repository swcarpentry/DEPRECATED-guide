class Raptor(object):
    def __init__(self, distance, color, speed):
        self.turtle = Turtle()
        self.turtle.pencolor(color)
        self.speed = speed

        self.turtle.penup()
        self.turtle.forward(distance)
        self.turtle.pendown()
