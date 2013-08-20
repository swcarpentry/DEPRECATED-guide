from Tkinter import *

class Application(object):

    SIZE = 200
    WIDTH = 5

    def __init__(self, root):
        self.x = self.SIZE/2
        self.y = self.SIZE/2

        self.x_slider = Scale(root, label="X", from_=0, to=self.SIZE,
                              command=self.change_x)
        self.x_slider.set(self.x)
        self.x_slider.pack(side=LEFT)

        self.y_slider = Scale(root, label="Y", from_=0, to=self.SIZE,
                              command=self.change_y)
        self.y_slider.set(self.y)
        self.y_slider.pack(side=LEFT)

        self.canvas = Canvas(root, width=self.SIZE, height=self.SIZE, background="gray")
        self.canvas.pack(side=LEFT)

        self.cursor = self.draw("red")

    def change_x(self, value):
        self.x = int(value)
        self.redraw()

    def change_y(self, value):
        self.y = int(value)
        self.redraw()

    def redraw(self):
        self.canvas.delete(self.cursor)
        self.cursor = self.draw("red")
        self.canvas.update()

    def draw(self, color):
        return self.canvas.create_rectangle(self.x-self.WIDTH, self.y-self.WIDTH,
                                            self.x+self.WIDTH, self.y+self.WIDTH,
                                            fill=color)

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
