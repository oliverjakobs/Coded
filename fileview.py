import os
import tkinter as tk
from tkinter import ttk

from extendedTk import AutoScrollbar

class FileView(ttk.Frame):
    def __init__(self, master, path, text):
        ttk.Frame.__init__(self, master)
        
        # Setup tree and its scrollbars
        scrollY = AutoScrollbar(self, orient=tk.VERTICAL)
        scrollX = AutoScrollbar(self, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(self)

        self.tree["yscrollcommand"] = scrollY.set
        self.tree["xscrollcommand"] = scrollX.set                                

        scrollY["command"] = self.tree.yview
        scrollX["command"] = self.tree.xview

        # Fill the TreeView
        self.tree.heading("#0", text=text, anchor=tk.W)
        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', tk.END, text=abspath, open=True)
        self.process_directory(root_node, abspath)

        # Arrange the tree and its scrollbars in the grid
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        scrollY.grid(row=0, column=1, sticky=tk.NS)
        scrollX.grid(row=1, column=0, sticky=tk.EW)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

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
        while self.tree.parent(item_id) != '':
            path = self.tree.item(item_id)["text"] + "\\" + path
            item_id = self.tree.parent(item_id)

        return path
