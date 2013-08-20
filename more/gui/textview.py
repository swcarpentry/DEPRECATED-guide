from Tkinter import Tk, Label

root = Tk()
root.title("Quotation")

quote = '''Science has proof without any certainty.
Creationists have certainty without any proof.
-- Ashley Montague'''

label = Label(root, text=quote)
label.pack()

root.mainloop()
