import tkinter as tk
from tkinter import ttk
from tkinter import TclError

class BetterText(tk.Text):
    # Allows intercepting Text commands at Tcl-level
    def __init__(self, master=None, cnf={}, read_only=False, **kw):
        tk.Text.__init__(self, master=master, cnf=cnf, **kw)
        
        self._read_only = read_only
        
        self._original_widget_name = self._w + "_orig"
        self.tk.call("rename", self._w, self._original_widget_name)
        self.tk.createcommand(self._w, self._dispatch_tk_operation)
        self._tk_proxies = {}
        
        self._original_insert = self._register_tk_proxy_function("insert", self.intercept_insert)
        self._original_delete = self._register_tk_proxy_function("delete", self.intercept_delete)
        self._original_mark = self._register_tk_proxy_function("mark", self.intercept_mark)
    
    def _register_tk_proxy_function(self, operation, function):
        self._tk_proxies[operation] = function
        setattr(self, operation, function)
        
        def original_function(*args):
            self.tk.call((self._original_widget_name, operation) + args)
            
        return original_function
    
    def _dispatch_tk_operation(self, operation, *args):
        f = self._tk_proxies.get(operation)
        try:
            if f:
                return f(*args)
            else:
                return self.tk.call((self._original_widget_name, operation) + args)
            
        except TclError as e:
            # Some Tk internal actions (eg. paste and cut) can cause this error
            if (str(e).lower() == '''text doesn't contain any characters tagged with "sel"'''
                and operation in ["delete", "index", "get"] 
                and args in [("sel.first", "sel.last"), ("sel.first",)]):
                pass
            else:
                traceback.print_exc()
    
    def set_read_only(self, value):
        self._read_only = value
    
    def is_read_only(self):
        return self._read_only

    def set_content(self, chars):
        self.direct_delete("1.0", tk.END)
        self.direct_insert("1.0", chars)
        
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
        elif self._is_erroneous_delete(index1, index2):
            pass
        else:
            self.direct_delete(index1, index2)
    
    def _is_erroneous_delete(self, index1, index2):
        # Paste can cause deletes where index1 is sel.start but text has no selection. This would cause errors
        return index1.startswith("sel.") and not self.has_selection()
    
    def direct_mark(self, *args):
        self._original_mark(*args)
        
        if args[:2] == ("set", "insert"):
            self.event_generate("<<CursorMove>>")
    
    def index_sel_first(self):
        # Tk will give error without this check
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
        # If a selection is defined in the text widget, return (start,
        # end) as Tkinter text indices, otherwise return (None, None)
        if self.has_selection():
            return self.index("sel.first"), self.index("sel.last")
        else:
            return None, None
        
    def direct_insert(self, index, chars, tags=None):
        self._original_insert(index, chars, tags)
        self.event_generate("<<TextChange>>")
    
    def direct_delete(self, index1, index2=None):
        self._original_delete(index1, index2)
        self.event_generate("<<TextChange>>")

