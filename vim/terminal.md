# Issues
## I don't have any solution for any of the following issues.
### I can't use my zsh snippets in Vim's terminal!

For some reason, you can't run fzf from a zle widget in Vim's terminal:

    func() {
        echo "foo\nbar" | fzf
    }
    zle -N func
    bindkey '^G^G' func

And you can't even set the command-line buffer from a zle widget:

    func() {
        BUFFER=foobar
    }
    zle -N func
    bindkey '^G^G' func

### Ranger is weirdly displayed!

Yes, the columns (and their borders) are not aligned correctly.
Also, the number of entries in a directory is sometimes not drawn.
And the image preview is misplaced in Vim's terminal.

There are probably other issues with ranger in a (N)Vim terminal.

### Some colors are wrong in Nvim's terminal!

If you set  `'tgc'`, Nvim's terminal seems  to use a palette  which is different
than the one of your regular terminal.

If your color is outside the 16 ANSI colors, I don't think there's a solution.
Afaik, Nvim doesn't let you configure the colors beyond 16.

For example,  in `~/.zshrc`, we  use the color 137  to highlight strings;  but –
when  we set  `'tgc'`  – the  exact  hex code  used by  Nvim's  terminal is  not
identical to the one used by xterm or st:

    # start xterm
    $ nvim -Nu NONE +'set tgc' +terminal
    $ palette

Start Gpick, and hover your mouse over the color 137 to reveal its hex code.
Atm, we find `#875f5f`, which is different than the code used in xterm (`#af875f`).

### Nvim's terminal doesn't support the bracketed paste mode!

MWE:

    $ nvim -Nu NONE +'let @+ = "foo\nbar"' +terminal +startinsert
    C-S-v

`foo` is wrongly run.

