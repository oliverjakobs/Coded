import subprocess
import tkinter as tk


def call(cmd, cwd):
    with subprocess.Popen(cmd, cwd=self.caller, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
        output, errors = p.communicate()
        return output
        

# TODO: style/appearance 
# TODO: call stack
class Terminal(tk.Frame):
    def __init__(self, master=None, caller=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.caller = caller

        self.output = tk.Text(self, state='disabled')
        self.label = tk.Label(self, text=caller + ">")
        self.entry = tk.Entry(self)
        self.entry.bind("<Return>", self.execute)

        self.output.grid(row=0, column=0, sticky=tk.NSEW, columnspan=2)
        self.label.grid(row=1, column=0, sticky=tk.NSEW)
        self.entry.grid(row=1, column=1, sticky=tk.NSEW)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def get_cmd(self):
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        return cmd

    def write(self, msg):
        self.output.configure(state='normal')
        self.output.insert('end', msg + "\n")
        self.output.configure(state='disabled')

    def execute(self, *args):
        cmd = self.get_cmd()
        self.write(self.caller + "> " + cmd)
        self.write(call(cmd, caller).decode("utf-8"))



if __name__ == "__main__":
    import os

    root = tk.Tk()

    root.title("Terminal")
    root.geometry("600x400")

    terminal = Terminal(root, caller=os.getcwd())
    terminal.pack()

    root.mainloop()