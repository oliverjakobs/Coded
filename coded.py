import os
import sys

# import tkinter
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# import own stuff
from extendedTk import FadingLabel
from fileview import FileView
from editor import Editor
from workspace import Workspace


class Coded(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # setup
        self.title("Coded")
        self.geometry("1200x800")
        # self.iconbitmap("icon.ico")

        #config
        self.state("zoomed")
        self._filedialog_options = {
            "defaultextension" : ".txt",
            "filetypes": [
                ("All Files", "*.*"),
                ("Json Files", "*.json"),
                ("Python Scripts", "*.py"),
                ("Text Files", "*.txt")]
        }

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # style
        self.style = ttk.Style()
        
        # menubar
        self.load_menu()

        # toolbar
        self.toolbar = tk.Frame(self, bg="grey")
        self.toolbar.grid(row=0, column=0, sticky=tk.EW)

        # button_run = ttk.Button(toolbar, text="Run")
        # button_run.pack(side=tk.RIGHT)

        # run_cmd = ttk.Combobox(toolbar, values=["Choose Command", "Manage..."])
        # run_cmd.current(0)
        # run_cmd.pack(side=tk.RIGHT)

        # get the size of the workspace
        self.update()

        ws_width = self.winfo_width()
        ws_height = self.winfo_height()

        # workspace
        self.workspace = Workspace(self, os.getcwd(), ws_width, ws_height, orient=tk.HORIZONTAL)
        self.workspace.grid(row=1, column=0, sticky=tk.NSEW)

        # console
        self.console = ttk.Notebook(self.workspace)
        #workspace.add(console)

        self.console.add(ttk.Frame(self.console), text="Output")
        self.console.add(ttk.Frame(self.console), text="Terminal")

        # status bar
        self.status = FadingLabel(self, text="Status", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.grid(row=2, column=0, sticky=tk.EW)

        # events
        self.bind("<Control-n>", self.new_file)
        self.bind("<Control-o>", self.open_file)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-S>", self.save_as)

        # Command Line Arguments
        for arg in sys.argv[1:]:
            self.workspace.load_tab(arg)

    def load_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        # file
        menu_file = tk.Menu(menu, tearoff=0)
        menu_file.add_command(label="New File", accelerator="Ctrl+N", command=self.new_file)
        menu_file.add_separator()
        menu_file.add_command(label="Open File", accelerator="Ctrl+O", command=self.open_file)
        menu_file.add_separator()
        menu_file.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        menu_file.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_as)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.destroy)

        # edit
        menu_edit = tk.Menu(menu, tearoff=0)
        menu_edit.add_command(label="Undo", accelerator="Ctrl+Z")
        menu_edit.add_command(label="Redo", accelerator="Ctrl+Y")
        menu_edit.add_separator()
        menu_edit.add_command(label="Cut", accelerator="Ctrl+X")
        menu_edit.add_command(label="Copy", accelerator="Ctrl+C")
        menu_edit.add_command(label="Paste", accelerator="Ctrl+V")
        menu_edit.add_command(label="Dublicate", accelerator="Ctrl+D")
        menu_edit.add_separator()
        menu_edit.add_command(label="Find", accelerator="Ctrl+F")
        menu_edit.add_command(label="Replace", accelerator="Ctrl+H")
        menu_edit.add_separator()
        menu_edit.add_command(label="Move Line Up", accelerator="Alt+UpArrow")
        menu_edit.add_command(label="Move Line Down", accelerator="Alt+DownArrow")

        # view
        menu_view = tk.Menu(menu, tearoff=0)

        # help
        menu_help = tk.Menu(menu, tearoff=0)
        menu_help.add_command(label="About")

        menu.add_cascade(label="File", menu=menu_file)
        menu.add_cascade(label="Edit", menu=menu_edit)
        menu.add_cascade(label="View", menu=menu_view)
        menu.add_cascade(label="Help", menu=menu_help)


    def new_file(self, *args):
         self.workspace.load_tab("Untitled", True)

    # TODO: better status desc
    def open_file(self, *args):
        filename = filedialog.askopenfilename(**self._filedialog_options)

        if filename:
            result, filename = self.workspace.load_tab(os.path.relpath(filename))
            if result > 0:
                self.status.write("{0} already open".format(filename))
            elif result < 0:
                self.status.write("[Error]: Failed to open {0}".format(filename))
            else:
                self.status.write("Open {0}".format(filename))

    def save(self, *args):
        result, filename = self.workspace.save_tab()
        if result > 0:
            self.save_as()
        elif result < 0:
            self.status.write("[Error]: Failed to save {0}".format(filename))
        else:
            self.status.write("Successfully saved {0}".format(filename))

    def save_as(self, *args):
        filename = filedialog.asksaveasfilename(**self._filedialog_options)

        if filename:
            result, filename = self.workspace.save_tab(os.path.relpath(filename))
            if result == 0:
                self.status.write("Successfully saved {0}".format(filename))
            else:
                self.status.write("[Error]: Failed to save {0}".format(filename))


if __name__ == "__main__":
    app = Coded()
    app.mainloop()








