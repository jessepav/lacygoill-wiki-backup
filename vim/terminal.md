# Issues
## I don't have any solution for any of the following issues.
##
## (N)Vim
### Ranger is weirdly displayed!

Yes, the columns (and their borders) are not aligned correctly.
Also, the number of entries in a directory is sometimes not drawn.
And the image preview is misplaced in Vim's terminal.

There are probably other issues with ranger in a (N)Vim terminal.

##
## Vim only
### I can't use my zsh snippets!

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

##
## Nvim only
### Some colors are wrong!

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

### The terminal doesn't support the bracketed paste mode!

MWE:

    $ nvim -Nu NONE +'let @+ = "foo\nbar"' +terminal +startinsert
    C-S-v

`foo` is wrongly run.

### I can't edit the current command-line by pressing `C-x C-e`!

Well it doesn't make much sense to do it.
I mean, you're in already in an editor.
If you want to edit the line with Nvim commands, just press Escape.

But yeah, it's broken:

    :term
    $ ls C-x C-e
    Error detected while processing function <SNR>119_LoadRemotePlugins[1]..<SNR>119_GetManifest[1]..~
    line    7:~
    E117: Unknown function: stdpath~

There seems  to be  some kind of  recursive loop;  `s:LoadRemotePlugins()` keeps
calling itself again and again.

Same issue in bash and zsh, and same issue when you run `$ fc`.

### Nvim crashes after I delete too many lines in a terminal buffer!

MWE:

    $ nvim -Nu NONE +term +setl\ modifiable +startinsert
    $ cat ~/.vim/vimrc
    C-\ C-n
    dGG
    i
    ls Enter

It's a known issue:

>    Will crash if all lines are deleted.
>
>    It's difficult  to support line  deletions, because scrollback  is received
>    passively from  libvterm.  Instead, one  can safely and  correctly "delete"
>    lines by temporarily setting 'scrollback' option to a smaller value.

<https://github.com/neovim/neovim/pull/6142>

>    Note there is a known issue: deleting lines may cause a crash.
>    Deleting lines isn't supported (it will be prevented in a future PR).

<https://github.com/neovim/neovim/pull/6142#issuecomment-282690785>

