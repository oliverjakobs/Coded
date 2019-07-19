from tkinter.ttk import Scrollbar

class AutoScrollbar(Scrollbar):
    def __init__(self, master=None, **kw):
        Scrollbar.__init__(self, master=master, **kw)

    def set(self, first, last):
        # Hide and show scrollbar as needed
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            self.grid_remove()
        else:
            self.grid()
        super(Scrollbar, self).set(first, last)