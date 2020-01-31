#!/usr/bin/python3
"Docstring"

import gui
from tkinter import Tk

if __name__ == "__main__":

    root = Tk()
    launcher = gui.Launcher(root)
    launcher.mainloop()
    root.destroy()
