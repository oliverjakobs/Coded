import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from extendedTk import Fileview
from extendedTk import NumberedTextFrame

from highlight import Highlighter

from pygments.lexers.python import PythonLexer
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.tcl import TclLexer
from pygments.lexers.c_cpp import CLexer
from pygments.lexers.configs import IniLexer

import os
import pathlib

class TabData:
    def __init__(self, index, path, text):
        self.index = index
        self.path = path
        self.text = text
        pass

class Workspace(ttk.PanedWindow):
    def __init__(self, master, location, style=None, **kw):
        super().__init__(master, **kw)

        self.location = location
        self.style = style

        # content
        self.notebook = ttk.Notebook(self)
        self.tabs = {}

        self.fileview = Fileview(self, style=style, location=location, title="Explorer")

        # adding content to the workspace
        self.add(self.fileview)
        self.add(self.notebook)

        # events
        # TODO: <Configure> event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.fileview.tree.bind("<<TreeviewOpen>>", self.on_open)

    def on_open(self, *args):
        filename = self.fileview.focus_path()
        if not os.path.isdir(filename):
            self.load_tab(filename)
    
    def on_tab_changed(self, event):
        # print(self.notebook.index("current"))
        pass

    def set_current_name(self, name):
        self.notebook.tab("current", text=name)

    def get_current_name(self):
        return self.notebook.tab("current", option="text")

    def change_tab_path(self, name, new_path):
        if not new_path:
            return self.tabs[name]

        new_name = os.path.relpath(new_path)
        if new_name == name:
            return self.tabs[name]

        tab = self.tabs.pop(name, None)
        if tab:
            tab.path = new_path

            self.tabs[new_name] = tab
            self.set_current_name(new_name)

        return tab

    def delete_tab(self, name=None):
        if name and name in self.tabs:
            data = self.tabs.pop(name)
            self.notebook.forget(data.index)
        else:
            self.tabs.pop(self.get_current_name())
            self.notebook.forget("current")

    def load_tab(self, path):
        name = os.path.relpath(path) if path else "untitled"
        
        if name in self.tabs:   # tab with this name is already open
            self.notebook.select(self.tabs[name].index)
            return 1

        tab = NumberedTextFrame(self, style=self.style, wrap=tk.NONE, bd=0, padx=5, pady=5)
        self.notebook.add(tab, text=name)
        self.notebook.select(tab)


        lexers = {
            '.py': PythonLexer(),
            '.md': MarkdownLexer(),
            '.tcl': TclLexer(),
            '.c': CLexer(),
            '.h': CLexer(),
            '.ini' : IniLexer()
        }
        lexer = lexers.get(pathlib.Path(name).suffix, None)

        tab.text.highlighter = Highlighter(tab.text, "config.ini", lexer)

        # add to tab dict
        self.tabs[name] = TabData(self.notebook.index(tab), path, tab.text)

        if not path: # new tab no text to insert
            return 0

        try:
            tab.text.read(path)
            return 0
        except UnicodeDecodeError as e:
            messagebox.showerror("UnicodeDecodeError", "Could not open {0}: \n{1}".format(path, e))
            self.delete_tab()
        except FileNotFoundError as e:
            messagebox.showerror("FileNotFoundError", "Could not open {0}: \n{1}".format(path, e))
            self.delete_tab()
        return -1

    def save_tab(self, path=None):
        tab = self.tabs[self.get_current_name()]
        try:
            if path or tab.path:
                tab = self.change_tab_path(self.get_current_name(), path)
                tab.text.write(tab.path)
                return 0, tab.path
                
            # current tab does not have a path yet and no path was specified
            return 1, None
        except Exception as e:
            messagebox.showerror("Error", "Could not save {0}: \n{1}".format(tab.path, e))
        return -1, tab.path
