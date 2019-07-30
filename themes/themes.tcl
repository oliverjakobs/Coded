set base_theme_dir [file join [pwd] [file dirname [info script]]]

array set base_themes {
  dark 0.1
  black 0.1
  light 0.1
  waldorf 0.1
}

foreach {theme version} [array get base_themes] {
  package ifneeded ttk::theme::$theme $version \
    [list source [file join $base_theme_dir $theme $theme.tcl]]
}
