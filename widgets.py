import tkinter as tk

class MenuBar:
    def __init__(self, parent):
        font_specs = ("ubuntu", 14)
        menu = tk.Menu(parent.root, font=font_specs)
        parent.root.config(menu=menu)

        # file
        file_menu = tk.Menu(menu, font=font_specs, tearoff=0)
        file_menu.add_command(label="New File", command=parent.new_file)
        file_menu.add_separator()
        file_menu.add_command(label="Open File", command=parent.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=parent.save)
        file_menu.add_command(label="Save As", command=parent.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=parent.root.destroy)

        menu.add_cascade(label="File", menu=file_menu)