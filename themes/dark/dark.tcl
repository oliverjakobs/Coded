# Theme dark
namespace eval ttk::theme::dark {
    
    # Widget colors
    variable colors
    array set colors {
        -fg             "#dedede"
        -bg             "#363636"
        -disabledbg     "#2e2e2e"
        -disabledfg     "#999999"
        -selectbg       "#414141"
        -selectfg       "#a6a6a6"
        -window         "#373737"
        -focuscolor     "#bebebe"
        -checklight     "#e6e6e6"
        -dark	        "#222222"
        -darker 	    "#121212"
        -darkest	    "#000000"
        -lighter	    "#626262"
        -lightest   	"#ffffff"
        -blue           "#0057a8"
    }
        
    # Create a new ttk::style
    ttk::style theme create dark -parent default -settings {
        # Configure basic style settings
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-bg) \
            -bordercolor $colors(-darkest) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -fieldbackground $colors(-window) \
            -font TkDefaultFont \
            -borderwidth 1 \
            -focuscolor $colors(-focuscolor)
        
        # Map disabled colors to disabledfg
        ttk::style map . -foreground [list disabled $colors(-disabledfg)]
        
        # WIDGET LAYOUTS
        ttk::style layout TButton {
            Button.button -children {
                Button.focus -children {
                    Button.padding -children {
                        Button.label -side left -expand true
                    }
                }
            }
        }

        ttk::style layout Toolbutton {
            Toolbutton.button -children {
                Toolbutton.focus -children {
                    Toolbutton.padding -children {
                        Toolbutton.label -side left -expand true
                    }
                }
            }
        }

        ttk::style layout Vertical.TScrollbar {
            Vertical.Scrollbar.trough -sticky ns -children {
                Vertical.Scrollbar.thumb -expand true
            }
        }

        ttk::style layout Horizontal.TScrollbar {
            Horizontal.Scrollbar.trough -sticky ew -children {
                Horizontal.Scrollbar.thumb -expand true
            }
        }

        ttk::style layout TMenubutton {
            Menubutton.button -children {
                Menubutton.focus -children {
                    Menubutton.padding -children {
                        Menubutton.indicator -side right
                        Menubutton.label -side right -expand true
                    }
                }
            }
        }

        ttk::style layout TCombobox {
            Combobox.field -sticky nswe -children {
                Combobox.downarrow -side right -sticky ns -children {
                    Combobox.arrow -side right
                }
                Combobox.padding -expand true -sticky nswe -children {
                    Combobox.textarea -sticky nswe
                }
            }
        }

        ttk::style layout TSpinbox {
            Spinbox.field -side top -sticky we -children {
                Spinbox.buttons -side right -children {
                    null -side right -sticky {} -children {
                        Spinbox.uparrow -side top -sticky nse -children {
                            Spinbox.symuparrow -side right -sticky e
                        }
                        Spinbox.downarrow -side bottom -sticky nse -children {
                            Spinbox.symdownarrow -side right -sticky e
                        }
                    }
                }
                Spinbox.padding -sticky nswe -children {
                    Spinbox.textarea -sticky nswe
                }
            }
        }

        # Style elements
        
        # Text 
        ttk::style configure Text -background $colors(-bg)

        # Statusbar
        ttk::style configure TFrame -background $colors(-blue)
        ttk::style configure TLabel -background $colors(-blue)

        # Settings
        ttk::style configure TButton -padding {8 4 8 4} -width -10 -anchor center -background $colors(-darker)
        ttk::style configure TMenubutton -padding {8 4 4 4}
        ttk::style configure Toolbutton -anchor center
        ttk::style configure TCheckbutton -padding 3
        # Radiobutton and Checkbutton hover highlighting: disabled by default
        # ttk::style map TRadiobutton -background [list active $colors(-checklight)]
        # ttk::style map TCheckbutton -background [list active $colors(-checklight)]
        ttk::style configure TRadiobutton -padding 3
        ttk::style configure TSeparator -background $colors(-bg)

        # Notebook
        ttk::style configure TNotebook -tabmargins {0 2 0 0} -borderwidth 0
        ttk::style configure TNotebook.Tab -padding {6 2 6 2} -expand {0 0 2} -bordercolor $colors(-darkest)
        ttk::style map TNotebook.Tab \
            -expand     [list selected {1 2 4 2}] \
            -background [list !selected $colors(-lighter)] 

        # Treeview
        ttk::style configure Treeview -background $colors(-window)
        ttk::style configure Treeview.Item -padding {2 0 0 0}
        ttk::style map Treeview \
            -background [list selected $colors(-selectbg)] \
            -foreground [list selected $colors(-selectfg)]
    }
}

variable version 0.1
package provide ttk::theme::dark $version

