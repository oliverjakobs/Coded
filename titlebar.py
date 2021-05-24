import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    root = tk.Tk()

    width = 800
    height = 600

    root.title("Titlebar")
    root.attributes("-alpha", 0.0)

    #toplevel follows root taskbar events (minimize, restore)
    def onRootIconify(event): 
        top.withdraw()
    root.bind("<Unmap>", onRootIconify)
    def onRootDeiconify(event): 
        top.deiconify()
    root.bind("<Map>", onRootDeiconify)

    top = tk.Toplevel(root)
    top.wm_overrideredirect(True)
    top.geometry("{0}x{1}+500+500".format(width, height))

    text = tk.Text(top)
    text.pack(fill=tk.BOTH)

    top.mainloop()

