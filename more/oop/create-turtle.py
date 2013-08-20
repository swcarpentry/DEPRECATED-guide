from turtle import Turtle, mainloop

def box(t, length):
    for i in range(4):
        t.forward(length)
        t.left(90)

def fan(t, count, length):
    for i in range(count):
        box(t, length)
        t.left(22.5)
        length *= 0.8

t = Turtle()
fan(t, 8, 100)
mainloop()
