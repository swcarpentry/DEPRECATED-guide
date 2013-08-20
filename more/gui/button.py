import sys
from Tkinter import Tk, Label, Button

def quit():
    sys.exit(0)

root = Tk()

label = Label(root, text="Click the button below")
label.pack()

button = Button(root, text="quit", command=quit)
button.pack()

root.mainloop()
