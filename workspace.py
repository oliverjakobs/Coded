import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from editor import Editor
from fileview import FileView

class Workspace(ttk.PanedWindow):
    def __init__(self, master, location, width, height, proportion=0.8, **kw):
        ttk.PanedWindow.__init__(self, master, width=width, height=height, **kw)

        self.location = location
        self.width = width
        self.height = height

        # content
        self.editor = Editor(self, width=int(width * proportion))
        self.fileview = FileView(self, path=location, text="Explorer")

        # adding content to the workspace
        self.add(self.editor)
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
            self.editor.add_tab(filename, new_tab)
            return 0

        try:
            text = self.editor.add_tab(filename)
            if text:
                with open(filename, "r") as f:
                    text.insert(1.0, f.read())
                return 0
            return 1
        except UnicodeDecodeError as e:
            messagebox.showerror("UnicodeDecodeError", "Could not open {0}: \n{1}".format(filename, e))
            self.editor.delete_tab(filename)   
        except FileNotFoundError as e:
            messagebox.showerror("FileNotFoundError", "Could not open {0}: \n{1}".format(filename, e))
            self.editor.delete_tab(filename)
        return -1   

    def save_tab(self, filename=None, save_as=None):
        try:
            if not filename:
                # TODO: better handling for new files
                filename = self.editor.get_name()
                if self.editor.get_new(filename):
                    return 1
            with open(filename, "w") as f:
                f.write(self.editor.get_text().get(1.0, tk.END))
            self.editor.set_name(filename)
            return 0
        except Exception as e:
            messagebox.showerror("Error", "Could not save {0}: \n{1}".format(filename, e))
        return -1


        
