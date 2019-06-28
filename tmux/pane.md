# How to set the title of the current pane?  (2)

    $ tmux selectp -T 'my title'

    $ printf '\033]2;My Title\033\\'

# How to enable/disable input to the current pane?

    $ tmux selectp -e
    $ tmux selectp -d

##
# Can a pane have a title?  A name?

A pane can only have a title.

# Can a window have a title?  A name?

A window can have a name.
It can't have its own title, but it automatically gets the one of its active pane.

From `$ man tmux /NAMES AND TITLES`:
> Windows themselves do not have titles - a window's title is the title of its active pane.

