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

---

In that case, you need `'cul'` to enabled.
Otherwise,  when  you move  with  `M-j`  and `M-k`,  you  may  not see  anything
happening for  quite some  time; you  may wrongly  end up  thinking that  sth is
broken.

Note that there would be no issue if we scrolled (!= moved) with `C-e` and `C-y`.
But that doesn't work well with `zMzv` which we use to open just enough folds to
see the current line.

At the  moment, we  set `'cul'` in  the `window#scroll_preview()`  function from
`~/plugged/vim-window/autoload/window.vim`, so you don't have  to set it in your
implementation of a scratch buffer.

---

Update:

Pro:

   - keep focus where it currently is

   - auto-open-fold for free

    Otherwise, you'll need to run `:norm coz`.

    But that's unreliable, because you may change the lhs of your `coz` mapping.

    And because,  if you install a  shell function to start  Vim and immediately
    open the scratch buffer, it won't work (`coz` is installed on `CursorHold`).
    Although,  you could  convert  `s:auto_open_fold()` into  a public  function
    though, and call the latter...

Con:

   - `z}` is harder to press to close the window (vs `q`)

   - you may want to implement some interactive features; if so, you'll need to
     focus the window cancelling the main benefit of a preview window

   - if there is already a preview window, its contents is replaced

   - adds noise in the status line (`[Preview]` flag)

### `(`, `)`, `[[`, `]]`, `{`, `}`, `<`, `>` as lhs in various local mappings

Right now,  we tend  to use  `)` and  `(` to  preview the  next/previous "entry"
(whatever that means in the context of the current buffer):

    :vim /nno.*<buffer>\S*\s\+\%([()]\|\[\[\|\]\]\)\s/gj ~/.vim/**/*.{snippets,vim} ~/.vim/template/** ~/.vim/vimrc
                                       ^^^^^^^^^^
                                       we also use `[[` and `]]` as a secondary pair of lhs

We chose  `(`/`)` – instead of  `{`/`}` – because  previewing sth seems to  be a
feature we  frequently want, and  because we rarely  press `(`/`)` (so  we don't
lose much).

OTOH:

   - we use `{`/`}` more frequently
   - `{`/`}` is harder to press

If you  need other  pairs of  lhs, I would  recommend –  in descending  order of
preference:

   - `[[`/`]]`
   - `{`/`}`
   - `<`/`>`

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

---

All of the above is irrelevant if the info in your scratch buffer is read from a
regular file; in which case, you should just edit it in read-only mode.

The read-only mode will prevent you from wrongly editing the file by accident.
In particular, the auto-save feature won't save a modified read-only buffer.
But it will still allow you to edit the file if you really want to (`:w!`).

## at most, only one scratch buffer should be displayed per tab page

IOW, if we run the command which opens a window displaying a scratch buffer of a
given type, while there's already one opened, the latter should be closed first.

## the name of the buffer should be carefully chosen

Which one to choose?

    'foobar'
    tempname().'foobar'
    'plugin://foobar'
    ...

## how to handle the name of a scratch buffer in the status line?

Look at what we did for `fex_tree` buffers.
Should we do the same for all scratch buffers?

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

---

Update: I think  that now we  use `:q`  everywhere; probably because  we thought
`:close` was too annoying when it raised an error...
Is it a good idea? Should we use `:close` back? Or this:

    exe winnr('$') > 1 ? 'close' : 'q'

?

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

## make sure no error is raised when we reload a scratch buffer which is in a tab page containing only 1 window

Find a design which prevents this possible issue.

##
## once you've come up with a design
### use it to bring consistency (and fix errors) in the way we've created a scratch buffer in the past

    :vim /setl.*bt=nofile/gj ~/.vim/**/*.vim ~/.vim/**/vim.snippets ~/.vim/vimrc

### enforce it via snippets/templates/vim-projectionist...

##
# Reference

[1]: https://en.wikipedia.org/wiki/Code_reuse
