import os
import tkinter as tk
from tkinter import ttk

class FileView(ttk.Frame):
    def __init__(self, master, path, text):
        ttk.Frame.__init__(self, master)
        self.tree = ttk.Treeview(self)
        scrollY = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollX = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=scrollY.set, xscroll=scrollX.set)
        self.tree.heading('#0', text=text, anchor=tk.W)

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', tk.END, text=abspath, open=True)
        self.process_directory(root_node, abspath)

        self.tree.grid(row=0, column=0, sticky=tk.NS)
        scrollY.grid(row=0, column=1, sticky=tk.NS)
        scrollX.grid(row=1, column=0, sticky=tk.EW)

        self.grid_rowconfigure(0, weight=1)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, tk.END, text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)

    def focus_name(self):
        return self.tree.item(self.tree.focus())["text"]
 
    def focus_path(self):
        item_id = self.tree.focus()
        path = self.tree.item(item_id)["text"]

        item_id = self.tree.parent(item_id)
        while item_id != '':
            path = self.tree.item(item_id)["text"] + "\\" + path
            item_id = self.tree.parent(item_id)

        return path