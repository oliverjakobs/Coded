import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from editor import Editor
from fileview import FileView
from terminal import Terminal

class Workspace(ttk.PanedWindow):
    def __init__(self, master, location, width, height, hor_prop=0.86, vert_prop=0.8, **kw):
        ttk.PanedWindow.__init__(self, master, width=width, height=height, **kw)

        self.location = location
        self.width = width
        self.height = height

        # content
        pane = ttk.PanedWindow(self, orient=tk.VERTICAL)

        editor_width = int(width * hor_prop)
        editor_height = int(height * vert_prop)

        self.editor = Editor(pane, width=editor_width, height=editor_height)
        self.fileview = FileView(self, path=location, text="Explorer")
        self.console = ttk.Notebook(self)

        self.console.add(Terminal(self.console, caller=location), text="Terminal")

        # adding content to the workspace
        pane.add(self.editor)
        pane.add(self.console)

        self.add(pane)
        self.add(self.fileview)

        # events
        # TODO: <Configure> event
        self.editor.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.fileview.tree.bind("<<TreeviewOpen>>", self.on_open)

        # print("Workspace loaded:")
        # print("Location:", location)
        # print("Size:", width, height)

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
                with open(filename, "r") as f:
                    text.insert(1.0, f.read())
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


        
