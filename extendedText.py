import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import TclError

from highlight import Highlighter

import traceback
import time

def classifyws(s, tabwidth):
    raw = effective = 0
    for ch in s:
        if ch == ' ':
            raw = raw + 1
            effective = effective + 1
        elif ch == '\t':
            raw = raw + 1
            effective = (effective // tabwidth + 1) * tabwidth
        else:
            break
    return raw, effective


def index2line(index):
    return int(float(index))

class BetterText(tk.Text):
    """ Allows intercepting Text commands at Tcl-level """
    def __init__(self, master=None, cnf={}, read_only=False, **kw):
        tk.Text.__init__(self, master=master, cnf=cnf, **kw)
        
        self._read_only = read_only
        self.highlighter = None

        # indent
        self.tabwidth = 8 # See comments in idlelib.EditorWindow 
        self.indentwidth = 4 
        self.usetabs = False
        
        self._w_orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._w_orig)
        self.tk.createcommand(self._w, self._dispatch_tk_operation)
        self._tk_proxies = {}
        
        self._original_insert = self._register_tk_proxy_function("insert", self.intercept_insert)
        self._original_delete = self._register_tk_proxy_function("delete", self.intercept_delete)
        self._original_mark = self._register_tk_proxy_function("mark", self.intercept_mark)

        # events
        self.bind("<Control-z>", lambda e: self.edit_undo)
        self.bind("<Control-y>", lambda e: self.edit_redo)
        self.bind("<Tab>", self.indent_or_dedent, True)

######################################################################
# tk funtions
######################################################################
    def _register_tk_proxy_function(self, operation, function):
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
            if (str(e).lower() == '''text doesn't contain any characters tagged with "sel"'''
                and operation in ["delete", "index", "get"] 
                and args in [("sel.first", "sel.last"), ("sel.first",)]):
                pass
            else:
                traceback.print_exc()

######################################################################
# Utility funtions
######################################################################
    def set_highlighter(self, highlighter):
        self.highlighter = highlighter
    
    def set_read_only(self, value):
        self._read_only = value
    
    def is_read_only(self):
        return self._read_only

    def set_content(self, chars):
        self.direct_delete("1.0", tk.END)
        self.direct_insert("1.0", chars)
        
######################################################################
# Intercept funtions
######################################################################
    def intercept_mark(self, *args):
        self.direct_mark(*args)
    
    def intercept_insert(self, index, chars, tags=None):
        if chars >= "\uf704" and chars <= "\uf70d": # Function keys F1..F10 in Mac cause these
            pass
        elif self.is_read_only():
            self.bell()
        else:
            self.direct_insert(index, chars, tags)
    
    def intercept_delete(self, index1, index2=None):
        if self.is_read_only():
            self.bell()            
        elif index1.startswith("sel.") and not self.has_selection():
            """ 
            Paste can cause deletes where index1 is sel.start but 
            text has no selection. This would cause errors
            """
            pass
        else:
            self.direct_delete(index1, index2)

######################################################################
# Direct funtions
######################################################################
    def direct_mark(self, *args):
        self._original_mark(*args)
        
        if args[:2] == ("set", "insert"):
            self.event_generate("<<CursorMove>>")

    def direct_insert(self, index, chars, tags=None):
        self._original_insert(index, chars, tags)
        if self.highlighter:
            self.highlighter.pygmentize_current()
        self.event_generate("<<TextChange>>")
    
    def direct_delete(self, index1, index2=None):
        self._original_delete(index1, index2)
        if self.highlighter:
            self.highlighter.pygmentize_current()
        self.event_generate("<<TextChange>>")

######################################################################
# Selection funtions
######################################################################
    def index_sel_first(self):
        """ Tk will give error without this check """
        if self.tag_ranges("sel"):
            return self.index("sel.first")
        else:
            return None
    
    def index_sel_last(self):
        if self.tag_ranges("sel"):
            return self.index("sel.last")
        else:
            return None

    def has_selection(self):
        return len(self.tag_ranges("sel")) > 0
    
    def get_selection_indices(self):
        """ 
        If a selection is defined in the text widget, return (start,
        end) as Tkinter text indices, otherwise return (None, None)
        """
        if self.has_selection():
            return self.index("sel.first"), self.index("sel.last")
        else:
            return None, None
        
######################################################################
# File funtions
######################################################################
    def read(self, filename):
        with open(filename, "r") as f:
            self.insert(1.0, f.read())
        if self.highlighter:
            self.highlighter.pygmentize_all()

    def write(self, filename):
        with open(filename, "w") as f:
            f.write(self.get(1.0, tk.END))

######################################################################
# ident/detent
######################################################################
    def _make_blanks(self, n):
        # Make string that displays as n leading blanks.
        if self.usetabs:
            ntabs, nspaces = divmod(n, self.tabwidth)
            return '\t' * ntabs + ' ' * nspaces
        else:
            return ' ' * n

    def _reindent_to(self, column):
        # Delete from beginning of line to insert point, then reinsert
        # column logical (meaning use tabs if appropriate) spaces.
        if self.compare("insert linestart", "!=", "insert"):
            self.delete("insert linestart", "insert")
        if column:
            self.insert("insert", self._make_blanks(column))

    def _get_region(self):
        first, last = self.get_selection_indices()
        if first and last:
            head = self.index(first + " linestart")
            tail = self.index(last + "-1c lineend +1c")
        else:
            head = self.index("insert linestart")
            tail = self.index("insert lineend +1c")
        chars = self.get(head, tail)
        lines = chars.split("\n")
        return head, tail, chars, lines

    def _set_region(self, head, tail, chars, lines):
        newchars = "\n".join(lines)
        if newchars == chars:
            self.bell()
            return
        self.tag_remove("sel", "1.0", "end")
        self.mark_set("insert", head)
        self.delete(head, tail)
        self.insert(head, newchars)
        self.tag_add("sel", head, "insert")

    def perform_smart_tab(self, event=None):        
        """
        if intraline selection:
            delete it
        elif multiline selection:
            do indent-region
        else:
            indent one level
        """

        first, last = self.get_selection_indices()
        if first and last:
            if index2line(first) != index2line(last):
                return self.indent_region(event)
            self.delete(first, last)
            self.mark_set("insert", first)
        prefix = self.get("insert linestart", "insert")
        raw, effective = classifyws(prefix, self.tabwidth)
        if raw == len(prefix):
            # only whitespace to the left
            self._reindent_to(effective + self.indentwidth)
        else:
            # tab to the next 'stop' within or to right of line's text:
            if self.usetabs:
                pad = '\t'
            else:
                effective = len(prefix.expandtabs(self.tabwidth))
                n = self.indentwidth
                pad = ' ' * (n - effective % n)
            self.insert("insert", pad)
        self.see("insert")
        return "break"

    def indent_or_dedent(self, event=None):
        if event.state in [1,9]: # shift is pressed (1 in Mac, 9 in Win)
            return self.dedent_region(event)
        else:
            return self.perform_smart_tab(event)  

    def indent_region(self, event=None):
        head, tail, chars, lines = self._get_region()
        for pos in range(len(lines)):
            line = lines[pos]
            if line:
                raw, effective = classifyws(line, self.tabwidth)
                effective = effective + self.indentwidth
                lines[pos] = self._make_blanks(effective) + line[raw:]
        self._set_region(head, tail, chars, lines)
        return "break"

    def dedent_region(self, event=None):
        head, tail, chars, lines = self._get_region()
        for pos in range(len(lines)):
            line = lines[pos]
            if line:
                raw, effective = classifyws(line, self.tabwidth)
                effective = max(effective - self.indentwidth, 0)
                lines[pos] = self._make_blanks(effective) + line[raw:]
        self._set_region(head, tail, chars, lines)
        return "break"


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")

    text = BetterText(root)
    text.pack()


    root.mainloop()


