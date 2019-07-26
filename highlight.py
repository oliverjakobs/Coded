
from pygments import lex
from pygments.lexers import PythonLexer

import tkinter as tk

# TODO: colors from json
def highlight_line(text, line_number):
    ''' highlight the given line '''

    print("--------Highlight---------------")

    line_start = "%d.%d" % (line_number, 0)
    line_end = "%d.end" % (line_number)

    line = text.get(line_start, line_end)

    # clean-up
    for tag in text.tag_names():
        text.tag_remove(tag, line_start, line_end)

    text.mark_set("range_start", line_start)

    # Configure
    text.tag_configure("Token.Name", foreground="#404040")
    text.tag_configure("Token.Text", foreground="#404040")

    text.tag_configure("Token.Keyword", foreground="#a460bf")
    text.tag_configure("Token.Keyword.Constant", foreground="#a460bf")
    text.tag_configure("Token.Keyword.Declaration", foreground="#a460bf")
    text.tag_configure("Token.Keyword.Namespace", foreground="#a460bf")
    text.tag_configure("Token.Keyword.Pseudo", foreground="#a460bf")
    text.tag_configure("Token.Keyword.Reserved", foreground="#a460bf")
    text.tag_configure("Token.Keyword.Type", foreground="#a460bf")

    text.tag_configure("Token.Punctuation", foreground="#ff0000")

    text.tag_configure("Token.Name.Class", foreground="#ddd313")
    text.tag_configure("Token.Name.Exception", foreground="#ddd313")
    text.tag_configure("Token.Name.Function", foreground="#298fb5")
    text.tag_configure("Token.Name.Function.Magic", foreground="#298fb5")
    text.tag_configure("Token.Name.Decorator", foreground="#298fb5")
           
    text.tag_configure("Token.Name.Builtin", foreground="#CC7A00")
    text.tag_configure("Token.Name.Builtin.Pseudo", foreground="#CC7A00")

    text.tag_configure("Token.Operator", foreground="#FF0000")
    text.tag_configure("Token.Operator.Word", foreground="#CC7A00")

    text.tag_configure("Token.Comment", foreground="#3ca658")
    text.tag_configure("Token.Comment.Single", foreground="#3ca658")
    text.tag_configure("Token.Comment.Double", foreground="#3ca658")

    text.tag_configure("Token.Literal.Number.Integer", foreground="#50bfbf")
    text.tag_configure("Token.Literal.Number.Float", foreground="#50bfbf")

    text.tag_configure("Token.Literal.String.Single", foreground="#35c666")
    text.tag_configure("Token.Literal.String.Double", foreground="#35c666")

    for token, content in lex(line, PythonLexer()):
        text.mark_set("range_end", "range_start + %dc" % len(content))
        text.tag_add(str(token), "range_start", "range_end")
        text.mark_set("range_start", "range_end")

def highlight_current(text):
    ''' highlight the given line where the cursor is ''' 
    index = text.index(tk.INSERT).split(".")
    highlight_line(text, int(index[0]))
    
def highlight_all(text):
    ''' highlight the whole text ... this can take pretty long for larger files '''
        
    code = text.get("1.0", "end-1c")
    i = 1
    for line in code.splitlines():
        text.index("%d.0" %i)
        highlight_line(text, line_number=i)
        text.update()
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

    with open(filename, "r") as f:
        text.insert(1.0, f.read())
    highlight_all(text)

    def on_event(*args):
        highlight_current(text)

    text.bind("<Control-s>", on_event)

    root.mainloop()