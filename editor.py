import tkinter as tk
from tkinter import ttk

from text import NumberedFrame

class Editor(ttk.Notebook):
    def __init__(self, master, **kw):
        ttk.Notebook.__init__(self, master, **kw)
        self.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.tab_texts = []
        self.tab_names = []

    def add_tab(self, name):
        if name in self.tab_names:
            return None

        options = {
            "wrap" : tk.NONE,
            "borderwidth" : 0,
            "padx" : 5,
            "pady" : 5
        }

        tab = NumberedFrame(self, **options)
        self.add(tab, text=name)
        self.select(tab)

        # add to list
        self.tab_texts.append(tab.text)
        self.tab_names.append(name)

        return tab.text

    def delete_tab(self, name=None):
        if name:
            if name in self.tab_names:
                index = self.tab_names.index(name)
                self.forget(index)
                self.tab_names.pop(index)
                self.tab_texts.pop(index)
        else:
            self.forget("current")

    def on_tab_changed(self, event):
        pass

    def get_text(self):
        return self.tab_texts[self.index("current")]

    def set_name(self, name):
        if self.tab_names[self.index("current")] != name:
            self.tab_names[self.index("current")] = name
            self.tab("current", text=name)

    def get_name(self):
        return self.tab("current", option="text")


