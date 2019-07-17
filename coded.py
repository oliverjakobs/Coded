import os
import sys

# import tkinter
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# import own stuff
from fileview import FileView
from editor import Editor
from workspace import Workspace

filetypes = [
    ("All Files", "*.*"),
    ("Json Files", "*.json"),
    ("Python Scripts", "*.py"),
    ("Text Files", "*.txt")]

def set_status(msg):
    global status
    status["text"] = msg

def set_title(title):
    global root
    root.title(title)

def new_file():
    global workspace
    workspace.new_tab()

# TODO: better status desc
# TODO: filedialog
def open_file():
    global workspace
    filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=filetypes)

    if filename:
        result = workspace.load_tab(os.path.relpath(filename))
        if result > 0:
            set_status("open_file: Already Open")
        elif result < 0:
            set_status( "open_file: error")
        else:
            set_status("open_file: Success")

def save():
    global workspace

    result = workspace.save_tab()
    if result > 0:
        save_as()
    elif result < 0:
        set_status( "save: error")
    else:
        set_status("save: Success")

def save_as():
    global workspace
    filename = filedialog.asksaveasfilename(initialfil="Untitled.txt", defaultextension=".txt", 
    filetypes=filetypes)

    if filename:
        result = workspace.save_tab(os.path.relpath(filename))
        if result == 0:
            set_status("save_as: Success")
        else:
            set_status( "save_as: error")

# setup
root = tk.Tk()
root.title("Coded")
root.geometry("1200x800")
# root.iconbitmap("icon.ico")

root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

# style
style = ttk.Style()

# menubar
menu = tk.Menu(root)
root.config(menu=menu)

# file
menu_file = tk.Menu(menu, tearoff=0)
menu_file.add_command(label="New File", command=new_file)
menu_file.add_separator()
menu_file.add_command(label="Open File", command=open_file)
menu_file.add_separator()
menu_file.add_command(label="Save", command=save)
menu_file.add_command(label="Save As", command=save_as)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.destroy)

# edit
menu_edit = tk.Menu(menu, tearoff=0)
menu_edit.add_command(label="Undo")
menu_edit.add_command(label="Redo")
menu_edit.add_separator()
menu_edit.add_command(label="Copy")
menu_edit.add_command(label="Cut")
menu_edit.add_command(label="Paste")
menu_edit.add_separator()
menu_edit.add_command(label="Find")
menu_edit.add_command(label="Replace")

# view
menu_view = tk.Menu(menu, tearoff=0)

# help
menu_help = tk.Menu(menu, tearoff=0)
menu_help.add_command(label="About")

menu.add_cascade(label="File", menu=menu_file)
menu.add_cascade(label="Edit", menu=menu_edit)
menu.add_cascade(label="View", menu=menu_view)
menu.add_cascade(label="Help", menu=menu_help)

# toolbar
toolbar = tk.Frame(root, bg="grey")
toolbar.grid(row=0, column=0, sticky=tk.EW)

# button_run = ttk.Button(toolbar, text="Run")
# button_run.pack(side=tk.RIGHT)

# run_cmd = ttk.Combobox(toolbar, values=["Choose Command", "Manage..."])
# run_cmd.current(0)
# run_cmd.pack(side=tk.RIGHT)

# get the size of the workspace
root.update()

ws_width = root.winfo_width()
ws_height = root.winfo_height()

# workspace
workspace = Workspace(root, os.getcwd(), ws_width, ws_height, orient=tk.HORIZONTAL)
workspace.grid(row=1, column=0, sticky=tk.NSEW)

# console
console = ttk.Notebook(workspace)
#workspace.add(console)

console.add(ttk.Frame(console), text="Output")
console.add(ttk.Frame(console), text="Terminal")

# status bar
status = tk.Label(root, text="Status...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.grid(row=2, column=0, sticky=tk.EW)

# Command Line Arguments
for arg in sys.argv[1:]:
    workspace.load_tab(arg)

# run
root.mainloop()


