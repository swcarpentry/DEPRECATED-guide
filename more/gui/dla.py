import sys
import random
from Tkinter import Tk, Canvas, mainloop

WINDOW = 600
BACKGROUND = "white"

#-------------------------------------------------------------------------------

class Grid(object):

    Offsets = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, size):
        self.size = size
        self.data = []
        for i in range(size):
            self.data.append([False] * size)

    def __getitem__(self, where):
        x, y = where
        assert self.on_grid(x, y)
        return self.data[x][y]

    def __setitem__(self, where, value):
        x, y = where
        assert self.on_grid(x, y)
        self.data[x][y] = value

    def on_grid(self, x, y):
        return (0 <= x < self.size) and (0 <= y < self.size)

    def random_edge_cell(self):
        r = random.randint(1, self.size-2)
        dx, dy = random.choice(self.Offsets)
        options = [r, 0, self.size-1]
        x = options[dx]
        y = options[dy]
        return x, y

#-------------------------------------------------------------------------------

class Speck(object):

    def __init__(self, grid, coords=None):
        self.grid = grid
        if coords is None:
            self.x, self.y = grid.random_edge_cell()
        else:
            assert len(coords) == 2
            self.x, self.y = coords
        self.steps = 0

    def on_grid(self):
        return self.grid.on_grid(self.x, self.y)

    def stuck(self):
        for ox, oy in self.grid.Offsets:
            x = self.x + ox
            y = self.y + oy
            if self.grid.on_grid(x, y) and self.grid[x, y]:
                return True
        return False

    def move(self):
        x, y = random.choice(self.grid.Offsets)
        self.x += x
        self.y += y
        self.steps += 1

    # mistakes: use self.y += x

    def on_edge(self):
        return (self.x == 0) or (self.x == self.grid.size-1) or \
               (self.y == 0) or (self.y == self.grid.size-1)

#-------------------------------------------------------------------------------

class Colorizer(object):

    STEP = 2

    def __init__(self):
        self.red = 128 - self.STEP
        self.green = 192
        self.blue = 256 - self.STEP

    def next(self):
        self.red = (self.red + self.STEP) % 256
        self.blue = (self.blue + self.STEP) % 256
        return "#%02x%02x%02x" % (self.red, self.green, self.blue)

#-------------------------------------------------------------------------------

class Application(object):

    def __init__(self, root, grid_size):
        root.title("Diffusion-Limited Aggregation")
        self.cell_size = WINDOW / grid_size
        self.grid = Grid(grid_size)
        self.canvas = Canvas(root, width=WINDOW, height=WINDOW)
        self.canvas.create_rectangle(0, 0, WINDOW, WINDOW, fill=BACKGROUND)
        self.canvas.pack()
        self.colorizer = Colorizer()

    def fill(self, x, y, color):
        x *= self.cell_size
        y *= self.cell_size
        self.canvas.create_rectangle(x, y,
                                     x + self.cell_size, y + self.cell_size,
                                     fill=color)
        self.canvas.update()

    def mark(self, speck, color):
        grid = speck.grid
        grid[speck.x, speck.y] = True
        self.fill(speck.x, speck.y, color)

    def evolve(self):
        # Fill in center cell.
        self.mark(Speck(self.grid, (self.grid.size/2, self.grid.size/2)),
                  self.colorizer.next())

        # Fill until the edge.
        number = 0
        while True:
            speck = Speck(self.grid)
            self.fill(speck.x, speck.y, "red")
            while speck.on_grid() and not speck.stuck():
                speck.move()
            if speck.on_grid():
                print "%d,+%d" % (number, speck.steps)
                self.mark(speck, self.colorizer.next())
                if speck.on_edge():
                    break
            else:
                print "%d,-%d" % (number, speck.steps)
            number += 1

# mistakes: do not nest the final speck.on_edge test inside the speck.on_grid

#-------------------------------------------------------------------------------

def main(args):
    grid_size = int(args[0])
    seed = int(args[1])
    random.seed(seed)

    print "#", grid_size, seed

    root = Tk()
    app = Application(root, grid_size)
    app.evolve()

    return root

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    root = main(sys.argv[1:])
    root.mainloop()
