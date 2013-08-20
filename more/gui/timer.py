import sys
from Tkinter import Tk, Label, Button, StringVar

class Application(object):

    def __init__(self, root):
        self.root = root

        self.labeltext = StringVar()

        self.label = Label(root, textvariable=self.labeltext)
        self.label.pack()

        self.button = Button(root, text="quit", command=self.quit)
        self.button.pack()

        self.seconds = -1
        self.changetext()

    def quit(self):
        sys.exit(0)

    def changetext(self):
        self.seconds += 1
        self.labeltext.set(str(self.seconds))
        self.root.after(1000, self.changetext)

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
