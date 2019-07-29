import tkinter as tk
from tkinter import ttk

from extendedTk import NumberedFrame
from highlight import Highlighter
from style import JSONStyle

class Editor(ttk.Notebook):
    def __init__(self, master, style, **kw):
        ttk.Notebook.__init__(self, master, **kw)
        self._tab_texts = []
        self._tab_names = []
        self._new_tabs = []
        self.style = style

    def add_tab(self, name, new=False, **tab_options):
        if name in self._tab_names:
            return None
        
        tab = NumberedFrame(self, style=self.style, **tab_options)
        self.add(tab, text=name)
        self.select(tab)

        tab.text.set_highlighter(Highlighter(tab.text, self.style))

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


if __name__ == "__main__":
    root = tk.Tk()

    width = 1200
    height = 800

    root.title("Editor")
    root.geometry("{0}x{1}".format(width, height))
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    filename = "fibonacci.py"

    editor = Editor(root, width=1200, height=800, style=JSONStyle("style.json"))
    editor.grid(row=0, column=0, sticky=tk.NSEW)
    status = tk.Label(root, text="Row: 0 | Column: 0", anchor=tk.W, bg="#424242")
    status.grid(row=1, column=0, sticky=tk.EW)

    text = editor.add_tab(filename, True, wrap=tk.NONE, bd=0, padx=5, pady=5, bg="#363636")

    text.insert_from_file(filename)

    root.mainloop()