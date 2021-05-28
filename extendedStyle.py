import tkinter as tk
from tkinter import ttk

# TODO: adjust themes
class ExtendedStyle(ttk.Style):
    """
    Style that loads themes from tcl files. Can be
    used as a drop-in replacement for normal ttk.Style instances.
    """
    def __init__(self, dir, theme=None, *args, **kwargs):
        """
        :param theme: Theme to set up initialization completion. If the
                      theme is not available, fails silently.
        """
 
        # Initialize as ttk.Style
        ttk.Style.__init__(self, *args, **kwargs)

        # Append a theme dir to the Tk interpreter auto_path
        self.tk.call("lappend", "auto_path", "[{}]".format(dir))
        # Load the themes into the Tkinter interpreter
        self.tk.eval("source {}/themes.tcl".format(dir))

        # Set the initial theme
        if theme and theme in self.get_themes():
            self.set_theme(theme)

    def set_theme(self, theme_name):
        """
        Set new theme to use. Uses a direct tk call to allow usage
        of the themes supplied with this package.

        :param theme_name: name of theme to activate
        """
        self.tk.call("package", "require", "ttk::theme::{}".format(theme_name))
        self.tk.call("ttk::setTheme", theme_name)

    def get_themes(self):
        """Return a list of names of available themes"""
        return list(set(self.tk.call("ttk::themes")))

    def theme_use(self, theme_name=None):
        """
        Set a new theme to use or return current theme name

        :param theme_name: name of theme to use
        :returns: active theme name
        """
        if theme_name:
            self.set_theme(theme_name)
        return ttk.Style.theme_use(self)


if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.geometry("600x400")

    #style = JSONStyle(path="style.json")
    style = ExtendedStyle(theme="equilux")

    nb = ttk.Notebook()
    nb.pack()

    print(style.get_themes())

    nb.add(ttk.Label(text="Hello Style"), text="Tab")

    root.mainloop()
