# Find a consistent design to display a scratch buffer
## check how plugin authors implement one

How do they implement the filetype detection and the syntax highlighting?

Which mappings and local settings do they set?
For which purpose exactly?
Look for `bt=nofile` or `buftype=nofile`.

## when should the window be horizontal instead of vertical?

## to read

    :h special-buffers
    :h new-buftype
    :h 'bt

##
## consider using
### a preview window

If you don't need to interact with  the scratch buffer, only read it, maybe make
it use a preview window:

    let &l:pvw = 1

### `{`, `}`, `(`, `)`, `[[`, `]]` as lhs in various local mappings

### enabling auto-opening fold

Tricky, because the  state of this feature  must be restored when  the window is
closed, no matter how it's closed (`:q`, `q`, `SPC q`, ...).

##
## the buffer should be reloadable

If you want  the buffer to be  reloadable via `:e`, do not  populate it directly
from the function called by a mapping.
It should be populated from an autocmd (maybe listening to bufnewfile).
If the  autocmd needs  some additional  info, make  it inspect  the name  of the
buffer, and use the latter to pass the info.
Look at what we did with `:Tree` for inspiration.

---

The cursor position should be preserved.

---

Should we also make a scratch buffer reloadable via a custom mapping?
(lhs = `r` or `R`; maybe `R` to not be too easy to press by accident...)

## at most, only one scratch buffer should be displayed per tab page

IOW, if we run the command which opens a window displaying a scratch buffer of a
given type, while there's already one opened, the latter should be closed first.

## the name of the buffer should be carefully chosen

Which one to choose?

    'foobar'
    tempname().'foobar'
    'plugin://foobar'
    ...

##
## mappings
### There should should be a mapping on C-l to focus the previous window:

    nno <buffer><nowait><silent> <c-l> :<c-u>call <sid>focus_previous_window_if_on_right()<cr>

    fu! s:focus_previous_window_if_on_right() abort
        if s:previous_window_is_on_right()
            wincmd p
        else
            wincmd l
        endif
    endfu

    fu! s:previous_window_is_on_right() abort
        let nr = winnr()
        let rightedge_current_window = win_screenpos(nr)[1] + winwidth(nr) - 1
        let nr = winnr('#')
        let leftedge_previous_window = win_screenpos(nr)[1]
        return rightedge_current_window + 1 == leftedge_previous_window - 1
    endfu

Otherwise, if you use the regular `C-l`,  you won't always focus back the window
from which you came.

---

In case you wonder why the mapping sometimes runs `wincmd l` instead of `wincmd p`:

    $ vim
    :Cheat
    :h
    C-j
    C-l

I would  expect the  last `C-l`  to focus the  window on  the right;  instead it
focuses the window on the top.
IOW, the previous window may not be on  the right; but if that's the case, `C-l`
should still focus a window on the right.

### ?

We should not run `:q` to close a scratch buffer via custom buffer-local mapping.

Instead, maybe we should use:

    exe winnr('$') > 1 ? 'close' : 'q'

Why?

    $ vim
    :h
    :FreeKeys
    :2q

If you now run `:q` to close the freekeys window, Vim quits.
With `:close`, Vim would not have quit, and you could still read the help window.

---

It seems that `:close`  doesn't make Vim quit when there's  only one help window
left, and that it's not documented.

Is it a good idea to rely on an undocumented feature?

### never install custom mappings to open filepaths using special keys (C-s, C-v C-v, C-t)

There are already default commands for that:

   - gf
   - gF
   - C-w f
   - C-w F
   - C-w gf
   - C-w gF
   - C-w T

You should rely on default commands as much as possible.
It gives a more consistent global interface.
Besides,  when they're  improved (by  you, a  plugin, Vim's  developers), you'll
benefit from it automatically.

Avoid  the NIH  syndrome:  don't  create an  ad-hoc  system  which doesn't  work
everywhere, and not always in the same manner.

[Reuse code][1] as much as possible.

##
## options
### `'winfixwidth'` (or `'winfixheight'`) should be set

Without, the  width of the window  may change when closing/opening  a window, or
simply when you change the focused window.
As an example, if you don't use `'wfw'`  in vim-freekeys, when you get back to a
regular window, the width of the freekeys window slightly increases by one cell.

MWE:

    $ vim +vs
    :FreeKeys
    :2q

The width of the freekeys window increases by a lot.

---

If you use a horizontal window, then `'winfixheight'` should be set instead.

### `bh` should be set to `delete`, not `wipe`

Never use `bh=wipe`.
It would prevent  you from recovering the  buffer if you lose  it temporarily by
accident, by pressing `C-^` or `--` for example.

If  the  buffer  is  automatically   populated  on  `BufNewFile`,  you  can  use
`bh=delete`.
Indeed, if  you lose  it by pressing  `C-^`, pressing `C-^`  a second  time will
trigger `BufNewFile` (whose definition is: starting  to edit a file that doesn't
exist) which will re-populate the buffer.

### `bt` should be set to `nofile`, not `nowrite`

You  probably don't  want to  create a  real file  every time  you display  some
temporary info.
Besides, contrary  to `nowrite`, `nofile`  makes the  name of the  buffer fixed,
i.e. it's not updated whenever you change the working directory (`:cd`).

See `:h special-buffers`:

>    directory   Displays directory contents. [...]
>                The buffer is created with these settings:
>                            :setlocal buftype=nowrite
>                            ...
>                The buffer name is the name of the directory and is adjusted
>                when using the |:cd| command.

See also `:h 'bt`:

>    nofile only:    The buffer name is fixed, it is not handled like a
>                    file name.  It is not modified in response to a |:cd|
>                    command.

##
## the window should be opened with either `:leftabove` or `:topleft`

We read from the left to the right.
So, it makes more sense to display the information on the left than on the right.

If the information is specific to the current buffer, choose `:leftabove`.
Otherwise, choose `:topleft`.

##
## once you've come up with a design
### use it to bring consistency (and fix errors) in the way we've created a scratch buffer in the past

    :vim /setl.*bt=nofile/gj ~/.vim/**/*.vim ~/.vim/**/vim.snippets ~/.vim/vimrc

### enforce it via snippets/templates/vim-projectionist...

##
# Reference

[1]: https://en.wikipedia.org/wiki/Code_reuse
