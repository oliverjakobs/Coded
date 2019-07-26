
from pygments import lex
from pygments.lexers import PythonLexer

import tkinter as tk
from style import Style

class Highlighter:
    def __init__(self, text, style):
        self.text = text
        self._configure(style)

    def _configure(self, style):
        for t in style.tokens:
            self.text.tag_configure("Token." + t, foreground=style.tokens[t])

    def clean(self, start, end):
        """ remove all tags from all characters between start and end """
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, start, end)
    
    def pygmentize_line(self, line_number):
        """ highlight the given line """
        line_start = "%d.%d" % (line_number, 0)
        line_end = "%d.end" % (line_number)

        line = self.text.get(line_start, line_end)

        self.clean(line_start, line_end)

        self.text.mark_set("range_start", line_start)

        for token, content in lex(line, PythonLexer()):
            self.text.mark_set("range_end", "range_start + %dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")

    def pygmentize_current(self):
        """ highlight the given line where the cursor is """ 
        index = self.text.index(tk.INSERT).split(".")
        self.pygmentize_line(int(index[0]))

    def pygmentize_all(self):
        """ highlight the whole text ... this can take pretty long for larger files """
        code = self.text.get("1.0", "end-1c")
        i = 1
        for line in code.splitlines():
            self.text.index("%d.0" %i)
            self.pygmentize_line(line_number=i)
            self.text.update()
            i += 1


if __name__ == "__main__":
    root = tk.Tk()

    width = 800
    height = 600

    root.title("Highlight")
    root.geometry("{0}x{1}".format(width, height))

    filename = "fibonacci.py"

    text = tk.Text(root, width=width, height=height)
    text.pack(fill = tk.BOTH)
    highlighter = Highlighter(text, Style("style.json"))

    with open(filename, "r") as f:
        text.insert(1.0, f.read())
    highlighter.pygmentize_all()

    def on_event(*args):
        highlighter.pygmentize_current()

    text.bind("<Control-s>", on_event)

    root.mainloop()