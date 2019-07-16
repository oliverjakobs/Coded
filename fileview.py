import os
import tkinter as tk
from tkinter import ttk

class FileView(ttk.Frame):
    def __init__(self, master, path):
        ttk.Frame.__init__(self, master)
        self.tree = ttk.Treeview(self)
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text=path, anchor=tk.W)

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', tk.END, text=abspath, open=True)
        self.process_directory(root_node, abspath)

        self.tree.grid(row=0, column=0, sticky=tk.NS)
        ysb.grid(row=0, column=1, sticky=tk.NS)
        xsb.grid(row=1, column=0, sticky=tk.EW)

        self.grid_rowconfigure(0, weight=1)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, tk.END, text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)