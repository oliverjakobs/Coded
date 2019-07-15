import tkinter as tk

from tkinter import ttk
from tkinter import filedialog

from widgets import MenuBar      

class PyNote:
    def __init__(self, root):
        # setup
        root.title("Untitled - PyNote")
        root.geometry("800x600")

        self.root = root
        self.filename = None

        # style
        self.style = ttk.Style()
        for t in self.style.theme_names():
            print(t)


        # font
        font_specs = ("ubuntu", 18)

        # textarea
        self.textarea = tk.Text(root, font=font_specs)
        self.scroll = ttk.Scrollbar(root, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # menubar
        self.menubar = MenuBar(self)

    def set_title(self, name=None):
        if name:
            self.root.title(name + " - PyNote")
        else:
            self.root.title("Untitled - PyNote")

    def new_file(self):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_title()

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt", 
        filetypes= [
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("Python Scripts", "*.py"),
            ("Json Files", "*.json")])

        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
            self.set_title(self.filename)

    def save(self):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self):
        try:
            new_file = filedialog.asksaveasfilename(initialfil="Untitled.txt", defaultextension=".txt", 
                filetypes= [
                    ("All Files", "*.*"),
                    ("Text Files", "*.txt"),
                    ("Python Scripts", "*.py"),
                    ("Json Files", "*.json")])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_title(new_file)
        except Exception as e:
            print(e)

    

if __name__ == "__main__":
    root = tk.Tk()
    pn = PyNote(root)
    root.mainloop()