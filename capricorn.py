import os
import sys
from configparser import ConfigParser

# import tkinter
import tkinter as tk
from tkinter import ttk, filedialog

# import own stuff
from workspace import Workspace
from extendedTk import ExtendedStyle, FadingLabel

class CapricornMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        # file
        menu_file = tk.Menu(self, tearoff=0)
        menu_file.add_command(label="New File", accelerator="Ctrl+N", command=master.new_file)
        menu_file.add_separator()
        menu_file.add_command(label="Open File", accelerator="Ctrl+O", command=master.open_file)
        menu_file.add_command(label="Open Folder", accelerator="Ctrl+Shift+O", command=master.open_folder)
        menu_file.add_separator()
        menu_file.add_command(label="Save", accelerator="Ctrl+S", command=master.save)
        menu_file.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=master.save_as)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=master.exit)

        # edit
        menu_edit = tk.Menu(self, tearoff=0)
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
        menu_view = tk.Menu(self, tearoff=0)
        menu_view.add_command(label="Themes")

        # help
        menu_help = tk.Menu(self, tearoff=0)
        menu_help.add_command(label="About")

        self.add_cascade(label="File", menu=menu_file)
        self.add_cascade(label="Edit", menu=menu_edit)
        self.add_cascade(label="View", menu=menu_view)
        self.add_cascade(label="Help", menu=menu_help)

class Statusbar(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, style='Statusbar.TFrame')

        self.status = FadingLabel(self, text="Status", style='Statusbar.TLabel')

        self.insert_pos = tk.StringVar(value="Ln: -| Col: -")
        label = ttk.Label(self, textvariable=self.insert_pos, style='Statusbar.TLabel')

        # grid
        self.columnconfigure(1, weight=1)

        self.status.grid(row=0, column=0, sticky=tk.W, padx=8, pady=2)
        label.grid(row=0, column=1, sticky=tk.E, padx=32, pady=2)

    def write(self, msg):
        self.status.write(msg)

    def update_insert_label(self, event):
        ln, col = event.widget.index('insert').split('.')
        self.insert_pos.set("Ln: {}| Col: {}".format(ln, col))

class Capricorn(tk.Tk):
    def __init__(self, config_path, tabs):
        super().__init__()

        # parse config file
        config = ConfigParser()
        config.optionxform = str
        config.read(config_path)

        theme_dir = config.get('Theme', 'dir', fallback=None)
        theme_name = config.get('Theme', 'name', fallback=None)
        theme_loader = "_themes"

        # load themes
        if theme_dir:
            # Append a theme dir to the Tk interpreter auto_path
            self.tk.call("lappend", "auto_path", "[{}]".format(theme_dir))
            # Load the themes into the Tkinter interpreter
            self.tk.eval("source {}/{}.tcl".format(theme_dir, theme_loader)) 
        
        # setup
        self.title("Capricorn")
        self.geometry("1200x800")
        
        self.iconbitmap('capricorn.ico')

        self._filedialog_options = { "defaultextension" : ".txt", "filetypes": [ ("All Files", "*.*") ] }

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # style
        self.style = ExtendedStyle(dir=theme_dir, theme=theme_name)
        
        # menubar
        self.menu = CapricornMenu(self)
        self.config(menu=self.menu)

        # workspace
        self.token = dict(config['Token']) if 'Token' in config.sections() else {}
        self.load_workspace(os.getcwd())

        # status bar
        self.statusbar = Statusbar(self)
        self.statusbar.grid(row=1, column=0, sticky=tk.EW)

        # events
        self.bind("<Control-n>", self.new_file)
        self.bind("<Control-o>", self.open_file)
        self.bind("<Control-O>", self.open_folder)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-S>", self.save_as)
        
        self.bind("<<InsertMove>>", self.statusbar.update_insert_label)

        # Command Line Arguments
        for tab in tabs:
            self.workspace.load_tab(tab, self.token)
            
    def load_workspace(self, location) -> bool:
        try:
            self.workspace = Workspace(self, location, self.token, style=self.style, orient=tk.HORIZONTAL)
            self.workspace.grid(row=0, column=0, sticky=tk.NSEW)
            return True
        except FileNotFoundError:
            print("Directory: {0} does not exist".format(location))
        except NotADirectoryError:
            print("{0} is not a directory".format(location))
        except PermissionError:
            print("You do not have permissions to change to {0}".format(location))

    def new_file(self, *args):
         self.workspace.load_tab(None)

    def open_file(self, *args):
        filename = filedialog.askopenfilename(**self._filedialog_options)

        if filename:
            result = self.workspace.load_tab(filename)
            if result > 0:
                self.statusbar.write("{0} already open".format(filename))
            elif result < 0:
                self.statusbar.write("[Error]: Failed to open {0}".format(filename))
            else:
                self.statusbar.write("Opened {0}".format(filename))

    def open_folder(self, *args):
        #No file extention options need to be passed while opening folders
        foldername = filedialog.askdirectory()

        if foldername == os.getcwd():
            self.statusbar.write("{0} already open".format(foldername))
        else:
            self.workspace.destroy()
            if self.load_workspace(foldername): 
                self.statusbar.write("Opened {0}".format(foldername))  

    def save(self, *args):
        result, filename = self.workspace.save_tab()
        if result > 0:
            self.save_as()
        elif result < 0:
            self.statusbar.write("[Error]: Failed to save {0}".format(filename))
        else:
            self.statusbar.write("Successfully saved {0}".format(filename))

    def save_as(self, *args):
        filename = filedialog.asksaveasfilename(**self._filedialog_options)

        if filename:
            result, filename = self.workspace.save_tab(os.path.relpath(filename))
            if result == 0:
                self.statusbar.write("Successfully saved {0}".format(filename))
            else:
                self.statusbar.write("[Error]: Failed to save {0}".format(filename))

    def exit(self, *args):
        self.destroy()


if __name__ == "__main__":
    app = Capricorn("config.ini", sys.argv[1:])
    app.mainloop()

