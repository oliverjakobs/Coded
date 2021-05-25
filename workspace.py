import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from extendedTk import Fileview
from extendedTk import NumberedFrame

from highlight import Highlighter

import os

class Workspace(ttk.PanedWindow):
    def __init__(self, master, location, width, height, style=None, prop=0.86, **kw):
        ttk.PanedWindow.__init__(self, master, width=width, height=height, **kw)

        self.location = location
        self.width = width
        self.height = height
        self.style = style

        # content
        editor_width = int(width * prop)

        # editor notebook
        self.notebook = ttk.Notebook(self, width=editor_width)
        self._tab_texts = []
        self._tab_names = []
        self._new_tabs = []

        self.fileview = Fileview(self, style=style, location=location, title="Explorer")

        # adding content to the workspace
        self.add(self.notebook)
        self.add(self.fileview)

        # events
        # TODO: <Configure> event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.fileview.tree.bind("<<TreeviewOpen>>", self.on_open)

    def on_open(self, *args):
        filename = self.fileview.focus_path()
        if not os.path.isdir(filename):
            self.load_tab(filename)
    
    def on_tab_changed(self, event):
        #print(self.notebook.get_index())
        pass

    def add_tab(self, name, new=False, **tab_options):
        if name in self._tab_names:
            return None
        
        tab = NumberedFrame(self, style=self.style, **tab_options)
        self.notebook.add(tab, text=name)
        self.notebook.select(tab)

        tab.text.highlighter = Highlighter(tab.text, self.style)

        # add to list
        self._tab_texts.append(tab.text)
        self._tab_names.append(name)
        if new:
            self._new_tabs.append(name)

        return tab.text

    def delete_tab(self, name=None):
        if name and name in self._tab_names:
            index = self._tab_names.index(name)
            self._tab_names.pop(index)
            self._tab_texts.pop(index)
            self.notebook.forget(index)
        else:
            self._tab_texts.pop(self.notebook.index("current"))
            self._tab_names.pop(self.notebook.index("current"))
            self.notebook.forget("current")

    def get_text(self):
        return self._tab_texts[self.notebook.index("current")]

    def set_name(self, name):
        if self._tab_names[self.notebook.index("current")] != name:
            self._tab_names[self.notebook.index("current")] = name
            self.notebook.tab("current", text=name)

    def get_name(self):
        return self.notebook.tab("current", option="text")

    def get_index(self):
        return self.index("current")

    def get_new(self, name):
        return name in self._new_tabs

    def load_tab(self, filename, new_tab=False):
        text = self.add_tab(filename, new_tab, wrap=tk.NONE, bd=0, padx=5, pady=5)
        if new_tab: # new tab no text to insert
            return 0, filename
        if not text: # tab with this name is already open
            return 1, filename

        try:
            text.read(filename)
            return 0, filename
        except UnicodeDecodeError as e:
            messagebox.showerror("UnicodeDecodeError", "Could not open {0}: \n{1}".format(filename, e))
            self.delete_tab()
        except FileNotFoundError as e:
            messagebox.showerror("FileNotFoundError", "Could not open {0}: \n{1}".format(filename, e))
            self.delete_tab(filename)
        return -1, filename  

    def save_tab(self, filename=None):
        try:
            if not filename:
                filename = self.get_name()
                if self.get_new(filename):
                    return 1, filename
            self.get_text().write(filename)
            self.set_name(filename)
            return 0, filename
        except Exception as e:
            messagebox.showerror("Error", "Could not save {0}: \n{1}".format(filename, e))
        return -1, filename
