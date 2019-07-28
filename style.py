import json

class JSONStyle:
    def __init__(self, path):
        with open(path) as style_sheet:
            style = json.load(style_sheet)

            self.backgrounds = style["Background"] # backgrounds["Primary"] and backgrounds["Secondary"]
            self.tokens = style["Token"]

    
if __name__ == "__main__":
    import tkinter as tk

    def move_window(event):
        app.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    app = tk.Tk()
    app.overrideredirect(True)
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_coordinate = (screen_width/2) - (1050/2)
    y_coordinate = (screen_height/2) - (620/2)
    app.geometry("{}x{}+{}+{}".format(1050, 650, int(x_coordinate), int(y_coordinate)))
    title_bar = tk.Frame(app, bg='#090909', relief='raised', bd=0, height=20, width=1050)
    close_button = tk.Button(title_bar, text='X', command=app.destroy, width=5, bg="#090909", fg="#888", bd=0)
    title_bar.place(x=0, y=0)
    close_button.place(rely=0, relx=1, x=0, y=0, anchor=tk.NE)
    title_bar.bind('<B1-Motion>', move_window)
    app.mainloop()