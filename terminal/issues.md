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

# I've pasted some text on the command-line, and the shell has automatically run it.  I wanted to edit it!

The [bracketed paste mode][1] fixes [this issue][2].

If you're using zsh, make sure its version is greater than 5.1.
If you're using  bash, make sure its  version is greater than  4.4 (and readline
version is greater than 7).

If you're using  tmux, you must also make sure  that whenever the `paste-buffer`
command is invoked, it's passed the `-p` option.

From `$ man tmux /paste-buffer`:

> If -p is specified, paste bracket control codes are inserted around the buffer
> if the application has requested bracketed paste mode.

---

Here's a short description of the bracketed paste mode:

> One  of the  least well  known,  and therefore  least used,  features of  many
> terminal emulators is bracketed paste mode.
> When you  are in bracketed  paste mode and you  paste into your  terminal, the
> content will be wrapped by the sequences `\e[200~` and `\e[201~`.
>
> [...] it enables something very cool: programs can tell the difference between
> stuff you type manually and stuff you pasted.
>
> [...]
>
> Lots of terminal applications handle  some characters specially: in particular
> when you hit your enter key it sends a newline.
> Most shells will execute the contents of the input buffer at that point, which
> is usually what you want.
> Unfortunately, this  means that they will  also run the contents  of the input
> buffer if there's a newline in anything you paste into the terminal.
>
> [...]

> For a while I've been running with  bracketed paste mode enabled to protect me
> from myself [...].

##
# Reference

[1]: https://cirw.in/blog/bracketed-paste
[2]: https://unix.stackexchange.com/a/230784/289772
