# Why is `$TERM` important?

When a program needs to use a particular terminal capability, it queries `$TERM`
to determine in which terminal it's currently running in.

Then,  it queries  the terminfo  db,  for the  current terminal  and the  needed
capability.
Finally,  the program  reads  the  definition of  the  latter  into an  external
variable.

So, `$TERM` must be properly set for the programs to send the right sequences to
the terminal.

# What does `$TERM` = 'xterm' really mean?

It doesn't mean that we're inside `xterm`.
A  lot  of terminals  lie  and  advertise themselves  as  being  `xterm`, to  be
compatible with a wider range of terminfo db.

However, this information can still be useful.
For example, to detect that the terminal is not running a tmux client.

##
# How to list all valid terminal types?

    $ toe -as
      │    ││
      │    │└ sort the output according to the names of the terminals
      │    │
      │    └ look in all terminal databases; not just the 1st one you find
      │
      └ mnemonic: Table Of Entries

List primary names  of all terminal types, to which  `$TERM` can legitimately be
set.

In addition  to those,  you can  also set `$TERM`  to any  alias present  in the
description of a given terminal.

## What does `*` and `+` mean in the output of the previous command?

When a terminal type is marked with:

   - `*`, it means a *conflicting* entry is present in another db
   - `+`, it means an *equivalent* entry is present in another db

##
# How to get the long name of
## the current terminal?

    $ tput longname

## the terminal type `screen-256color`?

    $ tput -Ttmux-256color longname
    tmux with 256 colors~

##
# Why shouldn't I use a file sourced by the shell to set `$TERM`?

There's no reliable way for the shell  to determine the identity of the terminal
it's running in.

# Where to set `$TERM`?

The *only*  place where you  should set `$TERM`  is in a  terminal configuration
file, like `~/.Xresources` for `urxvt` or `xterm`.

---

Unfortunately, such a file doesn't always exist.
It doesn't for xfce4-terminal.
You may still be able to configure the latter like this:

   1. right-click
   2. preferences entry
   3. compatibility tab
   4. emulation setting field

But you  will need to convert  a terminfo description for  `xfce4-terminal` into
`/etc/termcap`.

##
# Tmux
## Which value should I assign to `$TERM` inside tmux?

The only valid values are `screen`, `tmux` and some variants like `tmux-256color`.

`tmux-256color` is the best value, because it enables modern color schemes to be
correctly displayed, as well as italics.

### How to assign it?

Use the `default-terminal` tmux server option:

    set -s default-terminal tmux-256color

###
## Which issue can I face if `$TERM` contains `256color` inside tmux?

All programs  will think  that they're  connected to  a terminal  supporting 256
colors.
In reality, they're run by the tmux  server, which will pass their output to the
tmux client, which in turn will pass it to the local terminal.

If the  latter is a  “dumb” terminal supporting only  8 colors, it  will receive
control sequences which it doesn't understand.

---

TODO:

You must make sure that you use a “smart” terminal when you attach a tmux client
to a session.

Create a `tmux` function on the local  machine, which checks the identity of the
terminal before starting a tmux client.
It should serve as  a guard and prevent tmux from being  started if the terminal
is too dumb.
It could display a warning message when it fails, because the terminal is dumb.

The function should be able to parse optional arguments.
Take inspiration from `nv()`.

Update:
Maybe we could send a sequence encoding a color above `88`, to determine whether
the terminal supports 256 color...

    $ printf '\e]4;%d;?\a' 123 | if read -d $'\a' -s -t 1; then echo 'color 123 is supported'; fi

Source: https://unix.stackexchange.com/a/23789/289772

##
# Remote machine
## What's the value of `$TERM` on a remote machine to which you connect via ssh?

`$TERM` is mirrored by SSH to the remote session, unlike other common
environment variables (`$COLORTERM`, `$XTERM_VERSION`, `$VTE_VERSION`, ...).

## The terminfo db on my remote machine doesn't contain information about my current `$TERM`.  What to do?

You can reset `$TERM` just for the running `ssh` process.
The new value will be mirrored to the remote machine.
Choose a value which is present inside the remote terminfo db.

`xterm` is probably supported everywhere, so you could try:

    $ TERM=xterm ssh host

