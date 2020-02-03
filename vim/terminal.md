# Issues
## Vim only
### Ranger is weirdly displayed!

The columns (and their borders) are not aligned correctly.
Also, the number of entries in a directory is sometimes not drawn.
And the image preview is wrongly positioned.

It has been fixed in Nvim, by one of these commits:

    2a590e2293638eb27bbedc7c5758e9241aea0a77
    d57250ae64b61a37fbe84024be9706985186dbc1

### Previewing a picture in ranger causes some part of the screen not to be redrawn!

##
## Nvim only
### When I use one of my zsh snippets, the terminal window flickers!

    $ nvim -Nu NONE +'set so=3 | 10sp | term' +'startinsert'
    # press C-g C-g Esc
    # insert some random characters

### The terminal doesn't support the bracketed paste mode!

MWE:

    $ nvim -Nu NONE +'let @+ = "foo\nbar"' +terminal +startinsert
    C-S-v

`foo` is wrongly run.

It's a known issue: <https://github.com/neovim/neovim/issues/11418>

### Nvim crashes after I delete too many lines in a terminal buffer!

MWE:

    $ nvim -Nu NONE +term +setl\ modifiable +startinsert
    $ cat ~/.vim/vimrc
    C-\ C-n
    dgg
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

###
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

Same issue in bash and zsh, and same issue when you run `fc`.

---

Workaround: set `$EDITOR` to `nvim` (instead of `vim`) when starting ranger.

    EDITOR=nvim ranger

You could try to  set the variable only when inside  a Nvim terminal (inspecting
some environment variable which is only set in the latter).

#### An error is displayed when I open a file in Vim from ranger!

This is the same error as previously.

Workaround: In your zshrc, replace `vim` with `nvim`:

    __sane_vim() STTY=sane command nvim +'...'
                                   ^^^^

##### and when I use `| vipe`!

Workaround: Set `VISUAL` to `nvim`.

