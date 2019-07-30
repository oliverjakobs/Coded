import os
import tkinter as tk
from tkinter import ttk

from style import ExtendedStyle

class Tooltip():
    def __init__(self, widget):
        self.widget = widget
        self.tipWindow = None
        self.id = None
        self.x = self.y = 0
    
    def showtip(self, text):
        self.text = text
        if self.tipWindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 0
        y = y + cy + self.widget.winfo_rooty() + 40
        self.tipWindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#e6e6e6", foreground="#424242", relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)
     
    def hidetip(self):
        tw = self.tipWindow
        self.tipWindow = None
        if tw:
            tw.destroy()


class Toolbar(ttk.Frame):
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master=master, **kw)

        self.dir = os.getcwd().replace("\\", "/") + "/"

        img_run = tk.PhotoImage(file=self.dir + "images/run.png")
        btn_run = ttk.Button(self, image=img_run, command=self.run)
        
        img_terminal = tk.PhotoImage(file=self.dir + "images/terminal.png")
        btn_terminal = ttk.Button(self, image=img_terminal, command=self.terminal)

        img_interpreter = tk.PhotoImage(file=self.dir + "images/interpreter.png")
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
        #runButton.bind("<Button-3>", self.popupRun)

    def create_tooltip(self, widget, text):
        tooltip = Tooltip(widget)
        widget.bind("<Enter>", lambda e: tooltip.showtip(text))
        widget.bind("<Leave>", lambda e: tooltip.hidetip())

    def interpreter(self):
        print("Python")

    
    def terminal(self):
        print("Terminal")

    def run(self):
        print("Run")

if __name__ == "__main__":
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