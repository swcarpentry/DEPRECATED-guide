from Tkinter import *

class Application(object):

    def __init__(self, root):
        self.value = DoubleVar()
        self.slider = Scale(root, from_=0, to=100, orient=HORIZONTAL,
                            variable=self.value)
        self.slider.pack()
        self.button = Button(root, text="reset", command=self.reset)
        self.button.pack()

    def reset(self):
        self.value.set(0.0)

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
