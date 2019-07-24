
from pygments import lex
from pygments.lexers import PythonLexer

import tkinter as tk

def highlight(text, lineNumber=None):
    ''' highlight the line where the cursor is '''
        
    index = text.index(tk.INSERT).split(".")
    line_no = int(index[0])
    if lineNumber == None:
        line_text = text.get("%d.%d" % (line_no, 0),  "%d.end" % (line_no))
        text.mark_set("range_start", str(line_no) + '.0')
        
    elif lineNumber is not None:
        line_text = text.get("%d.%d" % (lineNumber, 0), "%d.end" % (lineNumber))
        text.mark_set("range_start", str(lineNumber) + '.0')

    for token, content in lex(line_text, PythonLexer()):
        # Debug
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

        text.mark_set("range_end", "range_start + %dc" % len(content))
        text.tag_add(str(token), "range_start", "range_end")
        text.mark_set("range_start", "range_end")
    
def highlight_all(text):
    ''' highlight whole text ... this can take pretty long for larger files '''
        
    code = text.get("1.0", "end-1c")
    i = 1
    for line in code.splitlines():
        text.index("%d.0" %i)
        highlight(text, lineNumber=i)
        text.update()
        i += 1