import os

# import tkinter
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog

# import own stuff
from fileview import FileView
from editor import Editor

def set_title(name=None):
    global root
    if name:
        root.title(name + " - Coded")
    else:
        root.title("Untitled - Coded")

def new_file():
    global editor
    editor.add_tab(name="Untitled")

def load_tab(filename):
    global editor

    if os.path.isfile(filename):
        text = editor.add_tab(os.path.relpath(filename))
        with open(filename, "r") as f:
            text.insert(1.0, f.read())

def open_selected(filename):
    global fileview
    load_tab(fileview.focus_path())

def open_file():
    filename = filedialog.askopenfilename(defaultextension=".txt", 
    filetypes= [
        ("All Files", "*.*"),
        ("Text Files", "*.txt"),
        ("Python Scripts", "*.py"),
        ("Json Files", "*.json")])

    load_tab(filename)

def save():
    global editor
    if editor.get_name() != "Untitled":
        try:
            with open(os.path.abspath(editor.get_name()), "w") as f:
                f.write(editor.get_text().get(1.0, tk.END))
        except Exception as e:
            print(e)
    else:
        save_as()

def save_as():
    global editor
    try:
        filename = filedialog.asksaveasfilename(initialfil="Untitled.txt", defaultextension=".txt", 
            filetypes= [
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("Python Scripts", "*.py"),
                ("Json Files", "*.json")])
        with open(filename, "w") as f:
            f.write(editor.get_text().get(1.0, tk.END))
        editor.set_name(os.path.relpath(filename))
    except Exception as e:
        print(e)

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
menu_file.add_command(label="Exit", command=root.quit)

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

button_run = ttk.Button(toolbar, text="Run")
button_run.pack(side=tk.RIGHT)

run_cmd = ttk.Combobox(toolbar, values=["Choose Command", "Manage..."])
run_cmd.current(0)
run_cmd.pack(side=tk.RIGHT)

# workspace
workspace = ttk.Frame(root)
workspace.grid(row=1, column=0, sticky=tk.NSEW)

relX = 0.8
relY = 0.8

# editor
editor = Editor(workspace)
editor.place(relx=0.0, rely=0.0, relwidth=relX, relheight=relY)

# fileview
fileview = FileView(workspace, path=os.getcwd(), text="Explorer")
fileview.place(relx=relX, rely=0.0, relwidth=(1.0-relX), relheight=relY)
fileview.tree.bind("<<TreeviewOpen>>", open_selected)

# console
console = ttk.Notebook(workspace)
console.place(relx=0.0, rely=relY, relwidth=1.0, relheight=(1.0-relY))

console.add(ttk.Frame(console), text="Output")
console.add(ttk.Frame(console), text="Terminal")

# status bar
status = tk.Label(root, text="Status...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.grid(row=2, column=0, sticky=tk.EW)

# run
root.mainloop()