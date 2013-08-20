from turtle import *

def box(length):
    for i in range(4):
        forward(length)
        left(90)

def fan(count, length):
    for i in range(count):
        box(length)
        left(22.5)
        length *= 0.8

fan(8, 100)
mainloop()
