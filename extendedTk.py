import os
import tkinter as tk

from tkinter import ttk
from extendedText import ExtendedText

class AutoScrollbar(ttk.Scrollbar):
    """ Scrollbar that is only visible when needed """
    def __init__(self, master=None, **kw):
        ttk.Scrollbar.__init__(self, master=master, **kw)

    def set(self, first, last):
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            self.grid_remove()
        else:
            self.grid()
        super().set(first, last)

class FadingLabel(ttk.Label):
    """ Label that fades back to an idle text after a given time """
    def __init__(self, master=None, delay=2500, **kw):
        """
        :param delay: delay after which the text return to idle
        """
        ttk.Label.__init__(self, master=master, **kw)
        self._idle_text = self["text"]
        self._delay = delay

    def write(self, msg):
        self["text"] = msg
        self.after(self._delay, lambda: self.config(text=self._idle_text))


######################################################################

######################################################################
class Fileview(ttk.Frame):
    def __init__(self, master, location, **kw):
        title = kw.pop("title", "")
        ttk.Frame.__init__(self, master=master)
        
        # Setup tree and its scrollbars
        scrollY = AutoScrollbar(self, orient=tk.VERTICAL)
        scrollX = AutoScrollbar(self, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(self)

        self.tree["yscrollcommand"] = scrollY.set
        self.tree["xscrollcommand"] = scrollX.set                                

        scrollY["command"] = self.tree.yview
        scrollX["command"] = self.tree.xview

        # Fill the Treeview
        self.tree.heading("#0", text=title, anchor=tk.W)
        abspath = os.path.abspath(location)
        root_node = self.tree.insert('', tk.END, text=abspath, open=True)
        self.process_directory(root_node, abspath)

        # Arrange the tree and its scrollbars in the grid
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        scrollY.grid(row=0, column=1, sticky=tk.NS)
        scrollX.grid(row=1, column=0, sticky=tk.EW)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, tk.END, text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)

    def focus_name(self):
        return self.tree.item(self.tree.focus())["text"]
 
    def focus_path(self):
        item_id = self.tree.focus()
        path = self.tree.item(item_id)["text"]

        item_id = self.tree.parent(item_id)
        while self.tree.parent(item_id) != '':
            path = self.tree.item(item_id)["text"] + "\\" + path
            item_id = self.tree.parent(item_id)

        return path


######################################################################

######################################################################
class NumberedFrame(ttk.Frame):
    """ Decorates text with scrollbars and line numbers """
    def __init__(self, master=None, **kw):
        """
        :param style: 
        """
        ttk.Frame.__init__(self, master=master)
  
        self.text = ExtendedText(self, **kw)
        self.text.grid(row=0, column=1, sticky=tk.NSEW)

        kw.pop("style", None)
        kw["bd"] = 0 
        kw["width"] = 4 
        kw["takefocus"] = False
        kw["fg"] = self.text["fg"]
        kw["bg"] = self.text["bg"]
        kw["font"] = self.text["font"]
        
        self._line_numbers = tk.Text(self, **kw)
        self._line_numbers.bind("<MouseWheel>", lambda e: "break")
        self._set_line_numbers(1)
        
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


######################################################################


######################################################################
# TODO: fix tooltip overshooting
class Tooltip():
    def __init__(self, widget):
        self.widget = widget
        self.window = None
    
    def show(self, text):
        if self.window or not text:
            return
        # get postion
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 0
        y = y + cy + self.widget.winfo_rooty() + 40

        self.window = tk.Toplevel(self.widget)
        self.window.wm_overrideredirect(True)
        self.window.wm_geometry("+%d+%d" % (x, y))
        
        # load actual tooltip
        label = tk.Label(self.window, text=text)
        label["justify"] = tk.LEFT
        label["background"] = "#e6e6e6"
        label["foreground"] = "#424242"
        label["relief"] = tk.SOLID
        label["borderwidth"] = 1
        label.pack(ipadx=1)
     
    def hide(self):
        if self.window:
            self.window.destroy()
            self.window = None



