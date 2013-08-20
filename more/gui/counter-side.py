from Tkinter import Tk, Label, Button, IntVar

class Application(object):

    def __init__(self, root):
        self.counter = IntVar()
        self.counter.set(0)

        self.label = Label(root, textvariable=self.counter)
        self.label.pack(side="left")

        self.up = Button(root, text="up", command=self.increment)
        self.up.pack(side="left")

        self.down = Button(root, text="down", command=self.decrement)
        self.down.pack(side="left")

    def increment(self):
        self.counter.set(self.counter.get() + 1)

    def decrement(self):
        self.counter.set(max(0, self.counter.get() - 1))

if __name__ == "__main__":
    root = Tk()
    root.title("Counter")
    app = Application(root)
    root.mainloop()
