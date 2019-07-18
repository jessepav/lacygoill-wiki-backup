# Events
## Which mouse events does tmux recognize?  (8)

    ┌───────────────┬──────────────────────────────────────────────────────────────┐
    │ WheelDown     │ wheel scrolled downward                                      │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ WheelUp       │ wheel scrolled upward                                        │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ DoubleClick1  │ double left click                                            │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ TripleClick1  │ triple left click                                            │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ MouseDown1    │ left click pressed                                           │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ MouseUp1      │ left click released                                          │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ MouseDrag1    │ mouse moving after left click has been pressed               │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ MouseDragEnd1 │ left click released after it was pressed and the mouse moved │
    └───────────────┴──────────────────────────────────────────────────────────────┘

In the last 6 events, `1` can be replaced by `2` or `3`.

    ┌───┬───────────────────┐
    │ 1 │ left click used   │
    ├───┼───────────────────┤
    │ 2 │ middle click used │
    ├───┼───────────────────┤
    │ 3 │ right click used  │
    └───┴───────────────────┘

##
## What is the only way for me to run a command when a mouse event is fired?

Install a key binding whose lhs contains the name of the event.

### On which conditions does this work?

The session option 'mouse' must be on.

##
## Which events are fired, when I left-click on a pane,
### then release the click?

   1. `MouseDown1`
   2. `MouseUp1`

### move the mouse, then release the click?

   1. `MouseDown1`
   2. `MouseDrag1`
   3. `MouseDragEnd1`

`MouseUp1` is only fired if the mouse didn't move after `MouseDown1`.

##
## In which locations can a mouse event be fired?  (6)

    ┌───────────────┬───────────────────────────────────┐
    │ Pane          │ the contents of a pane            │
    ├───────────────┼───────────────────────────────────┤
    │ Border        │ a pane border                     │
    ├───────────────┼───────────────────────────────────┤
    │ Status        │ the status line window list       │
    ├───────────────┼───────────────────────────────────┤
    │ StatusLeft    │ the left part of the status line  │
    ├───────────────┼───────────────────────────────────┤
    │ StatusRight   │ the right part of the status line │
    ├───────────────┼───────────────────────────────────┤
    │ StatusDefault │ any other part of the status line │
    └───────────────┴───────────────────────────────────┘

### Which window does the special token `=` resolve to, in a key binding whose lhs ends with the suffix `Status`?

It resolves to the window over which the mouse event was fired.

---

Suppose you have this key binding:

    $ tmux bind -Troot MouseUp1Status display -t= '#W'

And 3 windows named 'foo', 'bar', and 'baz'.

Focus the  window 'foo', and  release a  left-click (without dragging  the mouse
before) over  the text  'bar' in  the status line  window list;  `:display` will
print 'bar' (not 'foo').

##
# Key bindings
## How to build the lhs of a mouse key binding?

Follow the syntax `MouseEvent + Location`.

## Which lhs should I use to run a command when I right-click on the left part of my status line?

    MouseDown3StatusLeft
    ├────────┘├────────┘
    │         └ location
    └ mouse event

Usage example:

    $ tmux bind -Troot MouseDown3StatusLeft display 'test'

## In the rhs of a mouse key binding, how to refer to the session/window/pane where the mouse event was fired?

Use the special token `{mouse}` or `=`.

Example:

    $ tmux bind -Troot DoubleClick1Pane display -t= '#{pane_current_command}'
                                                  ^

With this key binding,  tmux should print the command running  in the pane where
you double left-click.

Incidentally, it will also change the active pane; but you could prevent this with a `last-pane`:

    $ tmux bind -Troot DoubleClick1Pane display -t= '#D' \\\; last-pane
                                                              ^^^^^^^^^

##
## What's the purpose of the `-M` flag for `send-keys`?

It's necessary to prevent  tmux from consuming a mouse event,  and to forward it
to the command running in the current pane.

For example, run this command and try to select a Vim tab page, by left-clicking
once (not twice) on its title:

    $ tmux bind -n MouseDown1Pane selectp -t= \; set mouse on ; vim -Nu NONE +'set mouse=a | tabnew'

It fails.
Now repeat the same experiment after modifying the key binding like so:

    $ tmux bind -n MouseDown1Pane selectp -t= \\\; send -M \; set mouse on ; vim -Nu NONE +'set mouse=a | tabnew'
                                              ^^^^^^^^^^^^

This time it works.

---

Similarly, you can double left-click on a Vim tab page title to select it.
It works because there's no `DoubleClick1Pane` key binding.
But if there was one, you would need  to make sure tmux forwards the mouse event
to Vim:

    # we disable `MouseDown1Pane` so that only a double click can select a Vim tab page (not a single click)
    $ tmux bind -n MouseDown1Pane if -F 1 ''
    $ tmux bind -n DoubleClick1Pane selectp -t= \\\; send -M \; set mouse on ; vim -Nu NONE +'set mouse=a | tabnew'
                                                ^^^^^^^^^^^^

