import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import TclError

class TclText(tk.Text):
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



class NumberedFrame(ttk.Frame):
    # Decorates text with scrollbars and line numbers
    def __init__(self, master, first_line=1, **text_options):
        ttk.Frame.__init__(self, master=master)
  
        self.text = TclText(self, text_options)
        self.text.grid(row=0, column=1, sticky=tk.NSEW)

        options = {
            "bd" : 0,
            "width" : 4,
            "takefocus" : False,
            "highlightthickness" : 0,
            "font" : self.text["font"],
            "background" : "#e0e0e0",
            "foreground" : "#999999"
        }

        options.update(text_options)
        
        self.line_numbers = tk.Text(self, **options)
        
        # margin will be gridded later
        self.set_line_numbers(first_line)
        
        self.vbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.vbar.grid(row=0, column=2, sticky=tk.NSEW)
        
        self.hbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hbar.grid(row=1, column=0, sticky=tk.NSEW, columnspan=2)
        
        self.text["yscrollcommand"] = self.vertical_scrollbar_update  
        self.text["xscrollcommand"] = self.horizontal_scrollbar_update    
        self.vbar["command"] = self.vertical_scroll 
        self.hbar["command"] = self.horizontal_scroll
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.text.bind("<<TextChange>>", self.text_changed, True)
    
    def focus_set(self):
        self.text.focus_set()
    
    def set_line_numbers(self, first):
        self.first_line = first
        if self.line_numbers.winfo_ismapped():
            self.line_numbers.grid_forget()
        else:
            self.line_numbers.grid(row=0, column=0, sticky=tk.NSEW)
            self.update_line_numbers()
    
    def text_changed(self, event):
        self.update_line_numbers()
    
    def vertical_scrollbar_update(self, *args):
        self.vbar.set(*args)
        self.line_numbers.yview(tk.MOVETO, args[0])
    
    def horizontal_scrollbar_update(self,*args):
        self.hbar.set(*args)
    
    def vertical_scroll(self,*args):
        self.text.yview(*args)
        self.line_numbers.yview(*args)
    
    def horizontal_scroll(self,*args):
        self.text.xview(*args)
    
    def update_line_numbers(self):
        text_line_count = int(self.text.index("end-1c").split(".")[0])
        # save yview position
        yview = self.line_numbers.yview()
        # update line numbers
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        for i in range(text_line_count):
            self.line_numbers.insert(tk.END, str(i + self.first_line).rjust(3))
            if i < text_line_count-1:
                self.line_numbers.insert(tk.END, "\n")
        
        self.line_numbers.yview(tk.MOVETO, yview[0])
        self.line_numbers.config(state=tk.DISABLED)