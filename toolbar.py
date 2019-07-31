import os
import threading
import tkinter as tk
from tkinter import ttk
from extendedTk import Dialog

class RunThread(threading.Thread):
    def __init__(self, command):
        threading.Thread.__init__(self)
        self.command = command
    
    def run(self):
        try:
            os.system(self.command)
        except Exception as e:
            print(str(e))

# TODO: fix tooltip overshooting
class Tooltip():
    def __init__(self, widget):
        self.widget = widget
        self.window = None
    
    def show(self, text):
        if self.window or not text:
            return
        # get postion
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 0
        y = y + cy + self.widget.winfo_rooty() + 40

        self.window = tk.Toplevel(self.widget)
        self.window.wm_overrideredirect(True)
        self.window.wm_geometry("+%d+%d" % (x, y))
        
        # load actual tooltip
        label = tk.Label(self.window, text=text)
        label["justify"] = tk.LEFT
        label["background"] = "#e6e6e6"
        label["foreground"] = "#424242"
        label["relief"] = tk.SOLID
        label["borderwidth"] = 1
        label.pack(ipadx=1)
     
    def hide(self):
        if self.window:
            self.window.destroy()
            self.window = None

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

class Toolbar(ttk.Frame):
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master=master, **kw)

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
        thread = RunThread("start cmd /K python")
        thread.start()

    def terminal(self):
        thread = RunThread("start cmd")
        thread.start()

    def run(self):
        thread = RunThread("start cmd " + self.run_cmd)
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