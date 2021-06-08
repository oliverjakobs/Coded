import tkinter as tk
from tkinter import ttk
from tkinter import TclError

from highlight import Highlighter

import traceback

def index_to_line(index):
    """ convert a tkinter index to the matching line number """
    return int(float(index))

def classify_whitespaces(string, tabwidth):
    """ calculate the whitespaces raw and effective length """
    raw = effective = 0
    for ch in string:
        if ch == " ":
            raw = raw + 1
            effective = effective + 1
        elif ch == "\t":
            raw = raw + 1
            effective = (effective // tabwidth + 1) * tabwidth
        else:
            break
    return raw, effective

def create_whitespaces(n, tabwidth, usetabs):
    """ cerate a string that displays as n leading whitespaces """
    if usetabs:
        tabs, spaces = divmod(n, tabwidth)
        return "\t" * tabs + " " * spaces
    else:
        return " " * n

class ExtendedText(tk.Text):
    """ Allows intercepting Text commands at Tcl-level """
    def __init__(self, master=None, **kw):
        """
        :param read_only: 
        :param highlighter:
        :param tabwidth:
        :param indentwidth:
        :param usetabs: 
        """
        self._read_only = kw.pop("read_only", False)
        self.highlighter = kw.pop("highlighter", None)
        self.tabwidth = kw.pop("tabwidth", 8)
        self.indentwidth = kw.pop("indentwidth", 4)
        self.usetabs = kw.pop("usetabs", False)
        self.style = kw.pop("style", ttk.Style())

        super().__init__(master=master, **kw)

        # apply style
        self.configure(bg=self.style.lookup("Text", "background"))
        self.configure(fg=self.style.lookup("Text", "foreground"))

        self._w_orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._w_orig)
        self.tk.createcommand(self._w, self._dispatch_tk_operation)
        self._tk_proxies = {}
        
        self._original_insert = self._register_tk_proxy_function("insert", self.intercept_insert)
        self._original_delete = self._register_tk_proxy_function("delete", self.intercept_delete)
        self._original_mark = self._register_tk_proxy_function("mark", self.intercept_mark)

        self.tk.call("tcl_wordBreakAfter", "a b", 0) # make sure word.tcl is loaded
        self.tk.call("set", "tcl_wordchars",     "[a-zA-Z0-9_]")
        self.tk.call("set", "tcl_nonwordchars", "[^a-zA-Z0-9_]")

        # events
        self.bind("<Control-z>", lambda e: self.edit_undo)
        self.bind("<Control-y>", lambda e: self.edit_redo)

        #self.bind("<BackSpace>", self.backspace, True)
        self.bind("<Tab>", self.indent, True)
        self.bind("<Shift-Tab>", self.dedent_region, True)

######################################################################
# tk funtions
######################################################################
    def _register_tk_proxy_function(self, operation, function):
        """ register a proxy function for a given operation """
        self._tk_proxies[operation] = function
        setattr(self, operation, function)
        
        def original_function(*args):
            self.tk.call((self._w_orig, operation) + args)
            
        return original_function
    
    def _dispatch_tk_operation(self, operation, *args):
        f = self._tk_proxies.get(operation)
        try:
            if f:
                return f(*args)
            else:
                return self.tk.call((self._w_orig, operation) + args)
            
        except TclError as e:
            # Some Tk internal actions (eg. paste and cut) can cause this error
            if (str(e).lower() == """text doesn"t contain any characters tagged with "sel" """
                and operation in ["delete", "index", "get"] 
                and args in [("sel.first", "sel.last"), ("sel.first",)]):
                pass
            else:
                traceback.print_exc()
        
######################################################################
# Intercept funtions
######################################################################
    def intercept_mark(self, *args):
        """ intercept mark calls """
        self.direct_mark(*args)
    
    def intercept_insert(self, index, chars, tags=None):
        """ intercept insert calls process them and send them on to direct_insert """
        if chars >= "\uf704" and chars <= "\uf70d": # Function keys F1..F10 in Mac cause these
            pass
        elif self._read_only:
            self.bell()
        else:
            self.direct_insert(index, chars, tags)
    
    def intercept_delete(self, index1, index2=None):
        if self._read_only:
            self.bell()            
        elif index1.startswith("sel.") and not self.selection():
            # Possible Error: paste can cause deletes where index1 is sel.start but text has no selection
            pass
        else:
            self.direct_delete(index1, index2)

######################################################################
# Direct funtions
######################################################################
    def direct_mark(self, *args):
        """ mark the text and generate <<InsertMove>> event if the insertion cursor moved """
        self._original_mark(*args)
        if args[0] == "set" and (args[1] == "insert" or 
        (args[1] == "range_start" and not args[2].startswith("range"))):
            self.event_generate("<<InsertMove>>")

    def direct_insert(self, index, chars, tags=None):
        """ insert chars at index, highlight the text afterwards (if text has a highlighter) 
        and generate a <<TextChange>> event """
        self._original_insert(index, chars, tags)
        if self.highlighter:
            self.highlighter.pygmentize_current()
        self.event_generate("<<TextChange>>")
    
    def direct_delete(self, index1, index2=None):
        """ delete chars between index1 and index2 (not included), highlight the text afterwards
        (if text has a highlighter) and generate a <<TextChange>> event """
        self._original_delete(index1, index2)
        if self.highlighter:
            self.highlighter.pygmentize_current()
        self.event_generate("<<TextChange>>")

######################################################################
# Selection funtions
######################################################################
    def selection(self):
        return self.tag_ranges("sel")
    
    def get_selection(self):
        """ If a selection is defined, return (start, end) as Tkinter text indices, 
        otherwise return (None, None) """
        if self.selection():
            return self.index("sel.first"), self.index("sel.last")
        else:
            return None, None

    def get_region(self):
        first, last = self.get_selection()
        if first and last:
            head = self.index(first + " linestart")
            tail = self.index(last + "-1c lineend +1c")
        else:
            head = self.index("insert linestart")
            tail = self.index("insert lineend +1c")
        chars = self.get(head, tail)
        lines = chars.split("\n")
        return head, tail, chars, lines

    def set_region(self, head, tail, chars, lines):
        newchars = "\n".join(lines)
        if newchars == chars:
            self.bell()
            return
        self.tag_remove("sel", "1.0", "end")
        self.mark_set("insert", head)
        self.delete(head, tail)
        self.insert(head, newchars)
        self.tag_add("sel", head, "insert")

    def modify_region(self, modifier):
        head, tail, chars, lines = self.get_region()
        self.set_region(head, tail, chars, [modifier(line) if line else "" for line in lines])

        if self.highlighter:
            self.highlighter.pygmentize_lines(index_to_line(head), index_to_line(tail))
        
######################################################################
# File funtions
######################################################################
    def read(self, filename):
        """ read the content of the file and insert it into the widget """
        with open(filename, "r") as f:
            self.insert(1.0, f.read())
        if self.highlighter:
            self.highlighter.pygmentize_all()

    def write(self, filename):
        """ write the content of the widget and into the file """
        with open(filename, "w") as f:
            f.write(self.get(1.0, tk.END))

######################################################################
# indent/dedent
######################################################################
    def indent(self, event=None):    
        """ if there is a multiline selection indent the selected region and return
        if there is a itraline selection delete it and indent afterwards
        if there is no selection just indent one level """
        first, last = self.get_selection()
        if first and last:
            # multiline selection
            if index_to_line(first) != index_to_line(last):
                return self.indent_region(event)
            self.delete(first, last)
            self.mark_set("insert", first)
        
        # get text from linestart to insertion cursor
        prefix = self.get("insert linestart", "insert")
        # tab to the next "stop" within or to right of line"s text:
        if self.usetabs:
            pad = "\t"
        else:
            effective = len(prefix.expandtabs(self.tabwidth))
            pad = " " * (self.indentwidth - effective % self.indentwidth)
        self.insert("insert", pad)
        self.see("insert")
        return "break"

    def indent_region(self, event=None):
        """ indent the selected region """
        def modifier(line):
            raw, effective = classify_whitespaces(line, self.tabwidth)
            effective = effective + self.indentwidth
            return create_whitespaces(effective, self.tabwidth, self.usetabs) + line[raw:]

        self.modify_region(modifier)
        return "break"

    def dedent_region(self, event=None):
        """ dedent the selected region """
        def modifier(line):
            raw, effective = classify_whitespaces(line, self.tabwidth)
            effective = max(effective - self.indentwidth, 0)
            return create_whitespaces(effective, self.tabwidth, self.usetabs) + line[raw:]

        self.modify_region(modifier)
        return "break"

######################################################################
# backspace
######################################################################
    def backspace(self, event):
        """ extended backspace function """
        # TODO: delete indentation
        first, last = self.get_selection()
        if first and last:
            self.delete(first, last)
            self.mark_set("insert", first)
            return "break"
        # Delete whitespace left, until hitting a real char or closest
        # preceding virtual tab stop.
        chars = self.get("insert linestart", "insert")
        if chars == "":
            if self.compare("insert", ">", "1.0"):
                self.delete("insert-1c")
            else:
                self.bell()     # at start of buffer
            return "break"
        
        if  chars[-1] not in " \t":
            self.delete("insert-1c")
            return "break"

        self.delete("insert-1c")
        return "break"

if __name__ == "__main__":
    from extendedTk import ExtendedStyle

    root = tk.Tk()
    root.geometry("600x400")

    style = ExtendedStyle(dir="./themes", theme="dark")

    text = ExtendedText(root)
    text.highlighter = Highlighter(text, style)
    text.pack()

    label_text = tk.StringVar()
    label = tk.Label(root, textvariable=label_text)
    label_text.set("Ln: -| Col: -")

    label.pack()

    def update_label(event):
        ln, col = event.widget.index("insert").split(".")
        label_text.set("Ln: {}| Col: {}".format(ln, col))
        

    text.bind("<<InsertMove>>", update_label)

    text.read("fibonacci.py")

    root.mainloop()


