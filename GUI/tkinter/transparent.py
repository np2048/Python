from tkinter import Tk # or(from Tkinter import Tk) on Python 2.x
root = Tk()
root.wait_visibility(root)
root.wm_attributes('-alpha',0.3)
root.mainloop()
