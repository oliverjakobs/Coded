import tkinter as tk
from tkinter import ttk

from tktextext import TextFrame 

class Editor(ttk.Notebook):
    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.bind("<<NotebookTabChanged>>", self.on_event)
        self.tab_texts = []

    def add_tab(self, name):
        tab = TextFrame(self, read_only=False, wrap=tk.NONE, line_numbers=True)
        self.add(tab, text=name)
        self.select(tab)

        # add to list
        self.tab_texts.append(tab.text)

        return tab.text

    def on_event(self, event):
        pass

    def get_text(self):
        return self.tab_texts[self.index("current")]

    def set_name(self, name):
        self.tab("current", text=name)

    def get_name(self):
        return self.tab("current", option="text")

