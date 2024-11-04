from tkinter import Tk, filedialog
from pathlib import Path
import readline
import os


def select_directory_gui(**kwargs):

    title = kwargs.get("title", "Select a directory")
    dir_initial = kwargs.get("dir_initial", os.getcwd())

    tk = Tk()
    tk.withdraw()
    tk.attributes("-topmost", True)

    dir_selected = filedialog.askdirectory(initialdir=dir_initial, title=title)
    return Path(dir_selected)
