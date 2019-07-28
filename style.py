import json

class JSONStyle:
    def __init__(self, path):
        with open(path) as style_sheet:
            style = json.load(style_sheet)

            self.backgrounds = style["Background"] # backgrounds["Primary"] and backgrounds["Secondary"]
            self.tokens = style["Token"]

    
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk
    from ttkthemes import ThemedTk

    root = ThemedTk(theme="black")
    root.geometry("600x400")

    nb = ttk.Notebook()
    nb.pack()

    print(root.get_themes())

    nb.add(ttk.Label(text="Hello Style"), text="Tab")

    root.mainloop()