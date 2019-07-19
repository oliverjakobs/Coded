import tkinter as tk
from tkinter import ttk

from extendedTk import NumberedFrame

class Editor(ttk.Notebook):
    def __init__(self, master, **kw):
        ttk.Notebook.__init__(self, master, **kw)
        self._tab_texts = []
        self._tab_names = []
        self._new_tabs = []

    def add_tab(self, name, new=False, **tab_options):
        if name in self._tab_names:
            return None
        
        tab = NumberedFrame(self, **tab_options)
        self.add(tab, text=name)
        self.select(tab)

        # add to list
        self._tab_texts.append(tab.text)
        self._tab_names.append(name)
        if new:
            self._new_tabs.append(name)

        return tab.text

    def delete_tab(self, name=None):
        if name:
            if name in self._tab_names:
                index = self._tab_names.index(name)
                self._tab_names.pop(index)
                self._tab_texts.pop(index)
                self.forget(index)
        else:
            self._tab_texts.pop(self.index("current"))
            self._tab_names.pop(self.index("current"))
            self.forget("current")

    def get_text(self):
        return self._tab_texts[self.index("current")]

    def set_name(self, name):
        if self._tab_names[self.index("current")] != name:
            self._tab_names[self.index("current")] = name
            self.tab("current", text=name)

    def get_name(self):
        return self.tab("current", option="text")

    def get_index(self):
        return self.index("current")

    def get_new(self, name):
        return name in self._new_tabs


