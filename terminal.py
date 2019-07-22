import subprocess, sys
import tkinter as tk

class Terminal(tk.Frame):
    def __init__(self, master=None, caller=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self._caller = caller
        self._call_stack = []
        self._call_stack.append("")
        self._call_index = 0

        self.output = tk.Text(self, state="disabled")
        self.label = tk.Label(self, text=caller + ">")
        self.entry = tk.Entry(self)
        self.entry.bind("<Return>", self.on_return)
        self.entry.bind("<Key-Up>", self.on_up)
        self.entry.bind("<Key-Down>", self.on_down)

        self.output.grid(row=0, column=0, sticky=tk.NSEW, columnspan=2)
        self.label.grid(row=1, column=0, sticky=tk.NSEW)
        self.entry.grid(row=1, column=1, sticky=tk.NSEW)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def on_up(self, *args):
        self._call_index = min(self._call_index + 1, len(self._call_stack) - 1)
        cmd = self._call_stack[self._call_index]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, cmd)

    def on_down(self, *args):
        self._call_index = max(self._call_index - 1, 0)
        cmd = self._call_stack[self._call_index]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, cmd)

    def on_return(self, *args):
        cmd = self.get_cmd()
        self._call_stack.insert(1, cmd)
        self._call_index = 0
        self.write(self._caller + "> " + cmd)
        self.execute(cmd)

    def get_cmd(self):
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        return cmd

    def execute(self, cmd):
        self.run(subprocess.Popen(cmd, cwd=self._caller, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True))

    def run(self, p):
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            return
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()
        self.after(20, self.run, p)


    def write(self, msg):
        if msg:
            self.output.configure(state="normal")
            self.output.insert("end", msg + "\n")
            self.output.configure(state="disabled")
        


if __name__ == "__main__":
    # import os

    # root = tk.Tk()

    # root.title("Terminal")
    # root.geometry("600x400")

    # terminal = Terminal(root, caller=os.getcwd())
    # terminal.pack()

    # root.mainloop()

    p = subprocess.Popen("python extendedText.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
    ## But do not wait till netstat finish, start displaying output immediately ##
    while True:
        out = p.stderr.read(1).decode("utf-8")
        if out == '' and p.poll() != None:
            print("Terminated")
            break
        if out != '':
            print("Run")
            sys.stdout.write(out)
            sys.stdout.flush()
