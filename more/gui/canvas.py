from Tkinter import Tk, Canvas

root = Tk()

canvas = Canvas(root, width=100, height=100, background="black")
canvas.pack()

canvas.create_rectangle(40, 40, 60, 60, fill="red")

root.mainloop()
