from Tkinter import Tk, Label, Button, IntVar

root = Tk()
root.title("Counter")

counter = IntVar()
counter.set(0)

def increment():
    global counter
    counter.set(counter.get() + 1)

label = Label(root, textvariable=counter)
label.pack()

button = Button(root, text="add one", command=increment)
button.pack()

root.mainloop()
