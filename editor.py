import tkinter as tk
from tkinter import ttk

class Editor(ttk.Notebook):
    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.bind("<<NotebookTabChanged>>", self.on_event)

        self.tab_texts = []

    def add_tab(self, name):
        tab = ttk.Frame(self)
        self.add(tab, text=name)
        self.select(tab)

        text = tk.Text(tab)

        # add to list
        self.tab_texts.append(text)

        scroll = ttk.Scrollbar(tab, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        return text

    def on_event(self, event):
        pass

    def get_text(self):
        return self.tab_texts[self.index("current")]

    def set_name(self, name):
        self.tab("current", text=name)

    def get_name(self):
        return self.tab("current", option="text")

