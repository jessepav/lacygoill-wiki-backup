# I can't use `M-f` in xfce4-terminal to move forward!

    Right-click
    > Preferences...
    > Advanced
    > Disable all menu access keys (such as Alt+f)

# I try to push a commit from Vim.  After typing my username and pressing Enter, the terminal writes `^M`!

Try this:

    # check settings (`icrnl` should not be prefixed by `-`)
    $ stty -a

    # fix tty
    $ stty icrnl

Source: <https://askubuntu.com/a/454663/867754>

