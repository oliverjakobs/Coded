import os
import tkinter as tk
from tkinter import ttk
from extendedTk import Dialog
from extendedTk import Tooltip

from utils import SubshellThread


class SettingsDialog(Dialog):   
    def __init__(self, master=None, cnf={}, **kw):
        """
        :param text: 
        """
        self.text = kw.pop("text", None)
        Dialog.__init__(self, master, cnf, **kw)

    def body(self, master):        
        ttk.Label(master, text="Cmd:").grid(row=0)
        self.entry = ttk.Entry(master)
        self.entry.grid(row=0, column=1)

        if self.text:
            self.entry.insert(0, self.text)

    def apply(self):
        self.result = self.entry.get()

class Toolbar(tk.Frame):
    def __init__(self, master=None, **kw):
        tk.Frame.__init__(self, master=master, **kw)

        # style
        self.configure(bg=ttk.Style().lookup("Label", "background"))

        images = os.getcwd() + "/images/"

        self.run_cmd = "/K python filename"

        img_run = tk.PhotoImage(file=images + "run.png")
        btn_run = ttk.Button(self, image=img_run, command=self.run)
        
        img_terminal = tk.PhotoImage(file=images + "terminal.png")
        btn_terminal = ttk.Button(self, image=img_terminal, command=self.terminal)

        img_interpreter = tk.PhotoImage(file=images + "interpreter.png")
        btn_interpreter = ttk.Button(self, image=img_interpreter, command=self.interpreter)

        # save imgs from garbage collection
        btn_run.image = img_run
        btn_terminal.image = img_terminal
        btn_interpreter.image = img_interpreter

        # layout
        btn_run.pack(side=tk.RIGHT)
        btn_terminal.pack(side=tk.RIGHT)
        btn_interpreter.pack(side=tk.RIGHT)

        # tool tips
        self.create_tooltip(btn_run, "Run File")
        self.create_tooltip(btn_terminal, "Open Terminal")
        self.create_tooltip(btn_interpreter, "Open Python Interpreter")

        # events
        btn_run.bind("<Button-3>", self.settings_run)

    def create_tooltip(self, widget, text):
        tooltip = Tooltip(widget)
        widget.bind("<Enter>", lambda e: tooltip.show(text))
        widget.bind("<Leave>", lambda e: tooltip.hide())

    def interpreter(self):
        thread = SubshellThread("start cmd /K python")
        thread.start()

    def terminal(self):
        thread = SubshellThread("start powershell")
        thread.start()

    def run(self):
        thread = SubshellThread("start cmd " + self.run_cmd)
        thread.start()

    def settings_run(self, event=None):
        dialog = SettingsDialog(master=self, title="Set run command", text=self.run_cmd)
        if dialog.result:
            self.run_cmd = dialog.result

if __name__ == "__main__":
    from style import ExtendedStyle
    root = tk.Tk()

    width = 800
    height = 600

    root.title("Toolbar")
    root.geometry("{0}x{1}".format(width, height))

    style = ExtendedStyle(theme="dark")

    toolbar = Toolbar(root)
    toolbar.pack(fill=tk.X)

    text = tk.Text(root, width=width, height=height)
    text.pack(fill=tk.BOTH)

    root.mainloop()