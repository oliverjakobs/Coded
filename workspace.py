import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from editor import Editor
from fileview import FileView
from terminal import Terminal
from style import Style

class Workspace(ttk.PanedWindow):
    def __init__(self, master, location, width, height, prop=0.86, **kw):
        ttk.PanedWindow.__init__(self, master, width=width, height=height, **kw)

        self.location = location
        self.width = width
        self.height = height

        # content
        editor_width = int(width * prop)

        self.editor = Editor(self, style=Style("style.json"), width=editor_width)
        self.fileview = FileView(self, path=location, text="Explorer")

        # adding content to the workspace
        self.add(self.editor)
        self.add(self.fileview)

        # events
        # TODO: <Configure> event
        self.editor.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.fileview.tree.bind("<<TreeviewOpen>>", self.on_open)

    def on_open(self, *args):
        self.load_tab(self.fileview.focus_path())
    
    def on_tab_changed(self, event):
        #print(self.editor.get_index())
        pass

    def load_tab(self, filename, new_tab=False):
        if new_tab:
            self.editor.add_tab(filename, new_tab, wrap=tk.NONE, bd=0, padx=5, pady=5)
            return 0, filename

        try:
            text = self.editor.add_tab(filename, wrap=tk.NONE, bd=0, padx=5, pady=5)
            if text:
                text.insert_from_file(filename)
                return 0, filename
            return 1, filename
        except UnicodeDecodeError as e:
            messagebox.showerror("UnicodeDecodeError", "Could not open {0}: \n{1}".format(filename, e))
            self.editor.delete_tab()   
        except FileNotFoundError as e:
            messagebox.showerror("FileNotFoundError", "Could not open {0}: \n{1}".format(filename, e))
            self.editor.delete_tab(filename)
        return -1, filename  

    def save_tab(self, filename=None):
        try:
            if not filename:
                filename = self.editor.get_name()
                if self.editor.get_new(filename):
                    return 1, filename
            with open(filename, "w") as f:
                f.write(self.editor.get_text().get(1.0, tk.END))
            self.editor.set_name(filename)
            return 0, filename
        except Exception as e:
            messagebox.showerror("Error", "Could not save {0}: \n{1}".format(filename, e))
        return -1, filename


        
