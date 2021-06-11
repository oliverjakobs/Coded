import tkinter as tk
from pygments import lex

class Highlighter:
    def __init__(self, text, token, lexer):
        self.text = text
        self._lexer = lexer

        for t in token:
            self.text.tag_configure("Token.{}".format(t), foreground=token[t])

    def clean(self, start, end):
        """ remove all token related tags from all characters between start and end """
        [self.text.tag_remove(tag, start, end) for tag in self.text.tag_names() if tag.startswith("Token.")]
    
    def pygmentize_line(self, line_number):
        """ highlight the given line """
        if not self._lexer:
            return

        line_start = "%d.%d" % (line_number, 0)
        line_end = "%d.end" % (line_number)

        line = self.text.get(line_start, line_end)

        self.clean(line_start, line_end)

        self.text.mark_set("range_start", line_start)

        for token, content in lex(line, self._lexer):
            self.text.mark_set("range_end", "range_start + %dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")

    def pygmentize_lines(self, start, end):
        """ highlight the given lines """
        for i in range(start, end+1):
            self.text.index("%d.0" % (i))
            self.pygmentize_line(line_number=i)

    def pygmentize_current(self):
        """ highlight the line where the cursor is """ 
        index = self.text.index(tk.INSERT).split(".")
        self.pygmentize_line(int(index[0]))

    def pygmentize_all(self):
        """ highlight the whole text ... this can take pretty long for larger files """
        for i in range(1, int(self.text.index("end").split(".")[0])):
            self.text.index("%d.0" % (i))
            self.pygmentize_line(line_number=i)


if __name__ == "__main__":
    from extendedTk import ExtendedStyle
    root = tk.Tk()

    width = 800
    height = 600

    root.title("Highlight")
    root.geometry("{0}x{1}".format(width, height))

    filename = "highlight.py"

    text = tk.Text(root, width=width, height=height)
    text.pack(fill = tk.BOTH)
    highlighter = Highlighter(text, ExtendedStyle("dark"), "themes/token.json")

    with open(filename, "r") as f:
        text.insert(1.0, f.read())
    highlighter.pygmentize_all()

    def on_event(*args):
        highlighter.pygmentize_current()

    text.bind("<Control-s>", on_event)

    root.mainloop()




