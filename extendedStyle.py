import json
import tkinter as tk
from tkinter import ttk

import utils

def style_configure(widget, name):
    kw = {}
    for key in widget.keys():
        value = ttk.Style().lookup(name, key)
        if value:
            kw[key] = value

    widget.configure(**kw)

# TODO: adjust themes
class ExtendedStyle(ttk.Style):
    """
    Style that loads themes from tcl files. Can be
    used as a drop-in replacement for normal ttk.Style instances.
    """
    def __init__(self, *args, **kwargs):
        """
        :param theme: Theme to set up initialization completion. If the
                      theme is not available, fails silently.
        """
        theme = kwargs.pop("theme", None)

        # Initialize as ttk.Style
        ttk.Style.__init__(self, *args, **kwargs)

        # Initialize as ThemedObject        
        self._load_themes()

        # Set the initial theme
        if theme is not None and theme in self.get_themes():
            self.set_theme(theme)

    def _load_themes(self):
        """Load the themes into the Tkinter interpreter"""
        with utils.chdir_temp(utils.get_file_directory()):
            self._append_theme_dir("themes")
            self.tk.eval("source themes/themes.tcl")
        
    def _append_theme_dir(self, name):
        """Append a theme dir to the Tk interpreter auto_path"""
        path = "[{}]".format(utils.get_file_directory() + "/" + name)
        self.tk.call("lappend", "auto_path", path)

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
        if theme_name is not None:
            self.set_theme(theme_name)
        return ttk.Style.theme_use(self)

class JSONStyle(ExtendedStyle):
    """
    Style that loads token styles from a json file
    """
    def __init__(self, *args, **kwargs):
        """
        :param path: path to the json file
        """
        path = kwargs.pop("path", None)
        ExtendedStyle.__init__(self, *args, **kwargs)
        
        with open(path) as style_sheet:
            style = json.load(style_sheet)

            self.backgrounds = style["Background"] # backgrounds["Primary"] and backgrounds["Secondary"]
            self.foregrounds = style["Foreground"] # foregrounds["Primary"] and foregrounds["Secondary"]
            self.tokens = style["Token"]
            self.theme_use(style["Theme"])


    
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