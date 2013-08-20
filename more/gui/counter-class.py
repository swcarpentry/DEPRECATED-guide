from Tkinter import Tk, Label, Button, IntVar

class Application(object):

    def __init__(self, root):
        self.counter = IntVar()
        self.counter.set(0)

        self.label = Label(root, textvariable=self.counter)
        self.label.pack()

        self.button = Button(root, text="add one", command=self.increment)
        self.button.pack()

    def increment(self):
        self.counter.set(self.counter.get() + 1)

if __name__ == "__main__":
    root = Tk()
    root.title("Counter")
    app = Application(root)
    root.mainloop()
