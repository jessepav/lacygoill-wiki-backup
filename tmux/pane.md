# Can a pane have a title?  A name?

A pane can only have a title.

# Can a window have a title?  A name?

A window can have a name.
It can't have its own title, but it automatically gets the one of its active pane.

From `$ man tmux /NAMES AND TITLES`:
> Windows themselves do not have titles - a window's title is the title of its active pane.

##
# How to set the title of the current pane?  (2)

    $ tmux selectp -T 'my title'

    $ printf '\033]2;My Title\033\\'

# How to enable/disable input to the current pane?

    $ tmux selectp -e
    $ tmux selectp -d

##
# What is an empty pane?

A pane which was not started to run a command, but simply to print some text.

---

An empty pane is characterized by a 0 pid:

    :display -p '#{pane_pid}'
    0~

Although weirdly enough, `:display -p '#{pane_current_command}'` still outputs `zsh`.

## How to create a new one?

    $ tmux splitw ''
                  ^^

### and make it print the output of a shell command (in a single command)?

    $ echo hello | tmux splitw -I
                               ^^
                               create an empty pane and forward any output from stdin to it

##
## Why do `$ tmux splitw ''` and `$ tmux splitw` behave differently?

*Without* any `shell-command` argument, after  creating a new pane, `:splitw` runs
the command set by the `'default-command'` option.
The default  value of  the latter is  an empty string,  which instructs  tmux to
create a login shell using the value of the `'default-shell'` option.
We use the value `/bin/zsh`.

OTOH, if you pass  an *explicit* empty string to `:splitw`,  in effect, you tell
tmux to ignore `'default-command'`.

---

Btw, don't conflate  the empty string passed to `:splitw`  with the empty string
which is assigned by default to `'default-command'`.
They are used in different contexts, and so can have different meanings.

##
## How to forward the output of a shell command to an existing empty pane?

Pass the `-I` flag to `display-message`.

    $ echo hello | tmux splitw -dI
    $ echo world | tmux display -I -t :.2
                                 ^

## How to send some text to an empty pane from Vim?

Create the empty pane, and save its id.
Then use this id to send your text.
Use the second optional argument of `system()` to pass the text to the stdin of `$ tmux`.

    :let pane_id = system('tmux splitw -PF "#D" -dI', "hello\n")[:-2]
    :call system('tmux display -t ' . pane_id . ' -I', "world\n")
                                                             ^^
                                                             don't forget to add a newline,
                                                             if you want the next text
                                                             to be printed on a different line

