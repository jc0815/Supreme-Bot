from tkinter import *
from tkinter.ttk import Combobox

window = Tk()

var = StringVar()
variable = StringVar(window)
variable.set("one") # default value

w = OptionMenu(window, variable, "one", "two", "three")
w.pack(side='center', ipadx=20, padx=30)

window.title('Supreme Config')
window.geometry("1000x1000+300+500")
window.mainloop()