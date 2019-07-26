import tkinter as tk

from tkinter import ttk
from extendedText import BetterText

class AutoScrollbar(ttk.Scrollbar):
    def __init__(self, master=None, **kw):
        ttk.Scrollbar.__init__(self, master=master, **kw)

    def set(self, first, last):
        # Hide and show scrollbar as needed
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            self.grid_remove()
        else:
            self.grid()
        super().set(first, last)

class FadingLabel(tk.Label):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Label.__init__(self, master, cnf, **kw)
        self._idle_text = self["text"]

    def write(self, msg):
        self["text"] = msg
        self.after(2500, lambda: self.config(text=self._idle_text))

class NumberedFrame(ttk.Frame):
    # Decorates text with scrollbars and line numbers
    def __init__(self, master, first_line=1, **text_options):
        ttk.Frame.__init__(self, master=master)
  
        self.text = BetterText(self, text_options)
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
        
        self._line_numbers = tk.Text(self, **options)
        self._line_numbers.bind("<MouseWheel>", lambda e: "break")
        self._set_line_numbers(first_line)
        
        self._scrollY = AutoScrollbar(self, orient=tk.VERTICAL)
        self._scrollX = AutoScrollbar(self, orient=tk.HORIZONTAL)

        self.text["yscrollcommand"] = self._on_text_vertical_scroll
        self.text["xscrollcommand"] = self._on_text_horizontal_scroll  

        self._scrollY["command"] = self._on_vertical_scroll 
        self._scrollX["command"] = self._on_horizontal_scroll

        self._scrollY.grid(row=0, column=2, sticky=tk.NSEW)
        self._scrollX.grid(row=1, column=0, sticky=tk.NSEW, columnspan=2)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.text.bind("<<TextChange>>", self._on_text_changed, True)

    def _set_line_numbers(self, first):
        self._first_line = first
        if self._line_numbers.winfo_ismapped():
            self._line_numbers.grid_forget()
        else:
            self._line_numbers.grid(row=0, column=0, sticky=tk.NSEW)
            self._update_line_numbers()

    def _on_text_changed(self, *args):
        self._update_line_numbers()
    
    def _on_text_vertical_scroll(self, first, last):
        self._scrollY.set(first, last)
        self._line_numbers.yview(tk.MOVETO, first)
    
    def _on_text_horizontal_scroll(self, first, last):
        self._scrollX.set(first, last)
    
    def _on_vertical_scroll(self,*args):
        self.text.yview(*args)
        self._line_numbers.yview(*args)
    
    def _on_horizontal_scroll(self,*args):
        self.text.xview(*args)
    
    def _update_line_numbers(self):
        text_line_count = int(self.text.index("end-1c").split(".")[0])
        # save yview position
        yview = self._line_numbers.yview()
        # update line numbers
        self._line_numbers.config(state=tk.NORMAL)
        self._line_numbers.delete("1.0", tk.END)
        for i in range(text_line_count):
            self._line_numbers.insert(tk.END, str(i + self._first_line).rjust(3))
            if i < text_line_count-1:
                self._line_numbers.insert(tk.END, "\n")
        
        self._line_numbers.yview(tk.MOVETO, yview[0])
        self._line_numbers.config(state=tk.DISABLED)


