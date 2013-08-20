import sys
from Tkinter import Tk, Label, Button

class Application(object):

    def __init__(self, root):
        self.label = Label(root, text="Click the button below")
        self.label.pack()
        self.button = Button(root, text="quit", command=self.quit)
        self.button.pack()

    def quit(self):
        sys.exit(0)

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
