import sys
from Tkinter import Tk, Canvas, NW
import Image
import ImageTk

assert len(sys.argv) == 2, "Need a filename"

image = Image.open(sys.argv[1]) 

root = Tk()
root.title(sys.argv[1])
canvas = Canvas(root, width=image.size[0], height=image.size[1])
canvas.pack()

photo = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=NW, image=photo)

root.mainloop()
