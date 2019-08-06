import tkinter as tk
from tkinter import ttk

from extendedTk import FadingLabel
from extendedStyle import style_configure

class Statusbar(tk.Frame):
    def __init__(self, master=None, **kw):
        tk.Frame.__init__(self, master, {}, **kw)

        self.status = FadingLabel(self, text="Status")

        self.insert_pos = tk.StringVar()
        label = ttk.Label(self, textvariable=self.insert_pos)
        self.insert_pos.set("Ln: -| Col: -")

        # style 
        style_configure(self, "Statusbar")
        style_configure(self.status, "Statusbar.Child")
        style_configure(label, "Statusbar.Child")

        # grid
        self.columnconfigure(1, weight=1)

        self.status.grid(row=0, column=0, sticky=tk.W, padx=8, pady=2)
        label.grid(row=0, column=1, sticky=tk.E, padx=32, pady=2)

    def write(self, msg):
        self.status.write(msg)

    def update_insert_label(self, event):
        ln, col = event.widget.index("insert").split(".")
        self.insert_pos.set("Ln: {}| Col: {}".format(ln, col))

    