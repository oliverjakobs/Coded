class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,output):
        self.output = output

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self,str):
        self.output.write(str,False)

class StderrRedirector(IORedirector):
    '''A class for redirecting stderr to this Text widget.'''
    def write(self,str):
        self.output.write(str,True)

class Output:
    def write(self, val, stderr=False)


if __name__ == "__main__":

    root = tk.Tk()

    root.title("Terminal")
    root.geometry("600x400")

    terminal = Terminal(root, caller=os.getcwd())
    terminal.pack()

    original_stdout = sys.stdout
    stdout_redirector = StdoutRedirector()
    sys.stdout = stdout_redirector

    root.mainloop()

    sys.stdout = original_stdout

