# How do I write a togglable popup terminal?

See: <https://gist.github.com/lacygoill/0bfef0a2e70ac7015aaee56a670c124b>

##
# Filters
## In which order are mappings and filters processed?

The mappings are processed *before* the filters.

---

    fu s:popup_filter(winid, key)
        if a:key is# '+'
            call popup_setoptions(a:winid, #{minheight: 3})
            return v:true
        endif
        return v:false
    endfu
    call popup_create('test', #{filter: function('s:popup_filter')})
    pedit /tmp/file
    nno z<c-k> <c-w>+
    set showcmd

    " press `z C-k` to increase the height of the current window:
    " it's the popup's height which is increased

Here's what happens.
When you press `z C-k`, the mapping replaces the keys with `C-w +`.
The popup  filter ignores `C-w`, but  consumes `+`; it handles  `+` by resetting
the height of the popup from 1 line to 3 lines.

This shows that the mappings are processed *before* the popup filters.

### In this example, when I press `z C-k` a second time, the preview window is closed.  Why?

After the first `z C-k`, `C-w` remains in the typeahead buffer.
When `z` is pressed, it's appended to the typeahead buffer which now contains:

    C-w z

This forms  a valid command (see  `:h ^wz`), so  Vim executes it and  closes the
preview window.

When `C-k` is typed, it's appended to the typeahead buffer which is now empty.
There are no mappings nor any builtin command starting with `C-k`.
See `:h normal-index /CTRL-K`.
So Vim discards `C-k` because it can't be used in a valid command.

##
## What's the meaning of `return v:false` and `return v:true` in a filter?

`return v:false` means that the key should *not* be consumed.
`return v:true` means that the key *should* be consumed (i.e. removed from the typeahead buffer).

##
# Scrolling
## How to scroll in a popup?

The easiest solution is to use `win_execute()` + `:norm!`.

---

In theory, you should only tweak the `firstline` key:

>     The "firstline" value is the main way how to specify what text to show
>     in a popup window that scrolls.  Using Normal mode commands is a bit of
>     a strange way.  Instead of that you could increment or decrement
>     "firstline".
>     ...
>     The idea is that "firstline" is changed to scroll the window.

Source: <https://github.com/vim/vim/issues/4882#issuecomment-526954273>

However, it's not easy to compute the  new value of `firstline`, when the scroll
moves by more than 1 line (e.g. `C-d`, `C-u`, `G`).

And even when you move by only 1 line, you need to make sure that you don't make
`firstline` go  beyond the  last line  of the buffer;  it would  give unexpected
results when  you try to  scroll backward; which means  you need to  compute the
last line of the buffer via `line('$', winid)`.

See the MWE in this bug report for an example:
<https://github.com/vim/vim/issues/5170#issue-516875178>

In any case, Bram agrees that `win_execute()` + `norm!` *may* be ok:

>     What I mentioned was that the scrolling should normally be implemented
>     by setting "firstline".  But if that somehow doesn't work, using normal
>     mode commands may be a way out.  But I would avoid normal mode commands
>     if possible.

Source: <https://github.com/vim/vim/issues/5170#issuecomment-549566321>

### It doesn't work!

Make sure `firstline` has been reset to 0.

    let id = popup_create({what}, {opts})
    call popup_setoptions(id, #{firstline: 0})
                              ^-------------^

When Vim redraws the screen, it always uses the value bound to `firstline`.
It doesn't care what is the current topline in the popup at that moment.

The value `0` is documented at `:h popup_create-arguments /firstline`:

>     firstline       ...
>                     Set to zero to leave the position as set by commands.

##
## How to scroll to the bottom?  (2)

    call win_execute(id, 'norm! G')
    call popup_setoptions(id, #{firstline: 0})

Or:

                                           vv
    call popup_setoptions(id, #{firstline: -1})
    call popup_setoptions(id, #{firstline: 0})

The value `-1` was added from this commit:
<https://github.com/vim/vim/commit/8c6173c7d3431dd8bc2b6ffc076ef49512a7e175>

You need to reset `firstline` to 0, so that the topline stays the same after Vim
redraws the screen, if you have scrolled.

##
# Preview
## How to make commands opening a preview window (like `:pedit`) use a popup window instead?

Set the `'previewpopup'` option.

    set previewpopup=height:10,width:60,highlight:Visual

All 3 items (`height`, `width`, `highlight`) are optional.
But for the option to take effect, the value must be non-empty.
Without the `highlight` item, the preview popup is highlighted by `Pmenu`.

See: `:h preview-popup`.

## How many preview popups can I have per tab page?

Only one.  Just like you you can only have one regular preview window per tab page.

## How can I find the window id of the preview popup?

    :echo popup_findpreview()

## Is the 'pvw' flag set in a preview popup?

Yes:

    $ vim +'set pvp=height:10,width:60' +'pedit /tmp/file'
    :echo getwinvar(popup_findpreview(), '&pvw')
    1~

##
## Can I have a preview window and a preview popup in the same tab page?

Yes:

    $ vim +'set pvp=height:10,width:60' +'pedit /tmp/file'
    :set pvw
    :echo map([1000, 1001], {_,v -> getwinvar(v, '&pvw')})
    [1, 1]~

##
## What happens if I run `:wincmd P` while the tab page contains
### a preview popup, and a preview window?

Vim focuses the preview window.

### a preview popup, but no preview window?

`E441` is raised:

    E441: There is no preview window

##
## What happens if I run `:wincmd z` while the tab page contains
### a preview popup, and a preview window?

The preview window is closed.

### a preview popup, but no preview window?

The popup is closed.

##
# Pitfalls
## When writing a popup filter, which keys should I avoid consuming?

Any key  which has  a meaning  for Vim;  unless you  pass `mapping:  v:false` to
`popup_create()`, in which case, your filter can consume any key.

Otherwise, as long as  your popup is visible, you can't press  this key with its
default meaning, neither directly, nor in the rhs of a mapping.

    " write this in `/tmp/t.vim`
    fu s:popup_filter(winid, key)
        if a:key is# "\<c-x>"
            echom 'the key "C-x" has been consumed'
            return v:true
        endif
        return v:false
    endfu
    call popup_create('test', #{filter: function('s:popup_filter')})
    pu=123
    nno cd <c-x>

Press `C-x`: it fails, the number is not decreased because `C-x` was consumed by the filter.
Press `cd`: again, it fails, for the same reason.

## None of my mappings work while a popup is open!

Make sure that in the options of the popup, the `mapping` key is not set to `v:false`.

Mappings are disabled when a popup:

   - is currently visible
   - has a filter callback
   - has a `mapping` key set to `v:false`

Note that by default, `mapping` is set to `v:true`.

---

You'll never  want to  set `mapping` to  `v:false`, except if  your popup  has a
filter which is meant to consume all the keys.

From `:h popup-mapping`:

>     If the filter consumes  all the keys, set the "mapping"  property to zero so
>     that mappings do not get in the way.
>     This is default for |popup_menu()| and |popup_dialog()|.

## My filter doesn't work.  When I press a key, it's not handled as expected!

You probably have a mapping which interferes.
Mappings are processed before filters.

Solution: Pass `mapping: v:false` to `popup_create()`.
Downside: This will break all your mappings as long as the popup is visible.

Alternatively, if you  know you'll interact with the popup  only from a specific
buffer, you could  try to install a buffer-local mapping  which replaces the key
with itself:

    nno <buffer><nowait> <key> <key>

Since the  mapping is  local, it  will have  priority over  the global  one, and
prevent the latter from replacing the key with something else.

After the mapping has been applied, the  key will pass to the filter, which will
handle it as if the global mapping had been ignored.

### It doesn't help!

Capture  the key  in a  global variable  at the  start of  your filter  function
(before all the `if`, `elseif` statements), and check what sequence Vim actually
receives.

Here's an example where Vim does *not* receive what you may expect.

Write this in `/tmp/t.vim`:

    fu s:popup_filter(winid, key) abort
        if a:key is# "\<m-g>" || a:key is# "\<m-s-g>"
            call s:setheight(a:winid)
            return v:true
        endif
        return v:false
    endfu
    fu s:setheight(winid) abort
        let s:height = get(s:, 'height', 1) + 1
        call popup_setoptions(a:winid, #{minheight: s:height})
    endfu
    call popup_create('test', #{filter: function('s:popup_filter'), mapping: v:false})

Then, start Vim in an xterm terminal, outside tmux, like this:

    $ vim -Nu NONE -S /tmp/t.vim

Press `M-g`: the height of the popup is increased.
Press `M-S-g`: nothing happens.

If you capture the keys received by the filter:

    fu s:popup_filter(winid, key) abort
        let g:d_keys = get(g:, 'd_keys', []) + [a:key]
        ^--------------------------------------------^

you should see that Vim receives this byte sequence when you press `M-S-g`:

    <80><fc>^BÇ

To limit the noise in your variable, pass `filtermode: 'n'` to `popup_create()`,
so that you don't get all the keys typed on the command-line.

    call popup_create('test', #{filter: function('s:popup_filter'), filtermode: 'n', mapping: v:false})
                                                                    ^-------------^

Anyway, once you get the sequence, use it to fix your `if`/`elseif` statement:

    if a:key is# "\<m-g>" || a:key is# "\<m-s-g>" || a:key is# "\x80\xfc\<c-b>Ç"
                                                               ^---------------^

---

Note that in this particular example, the issue can only be reproduced if:

   - the terminal is xterm

   - `t_TI` and `t_TE` are set with the values `^[[>4;2m` and `^[[>4;m`
     (they are by default if `$TERM` is `xterm` or a derivative)

   - `mapping: v:false` is passed to `popup_create()` (it's set to `v:true` by default)

##
## I can't close my popup terminal with `:close`!

It's forbidden in a popup terminal; use this instead:

    :call popup_close(win_getid())
          ^---------^

### Wait.  Now I have a popup terminal which I *can* close with `:close`.  What gives?

The job associated to the terminal buffer has probably finished (`F` flag in the
output of `:ls`); the restriction has been lifted.

##
## `popup_settext()` alters the contents of a regular buffer (buftype != "popup")!

If  your popup  was  created to  display  a regular  buffer  (i.e. the  `{what}`
argument was a buffer number), then it's tied to this buffer forever.
`popup_settext()` will not create a new one:

    call writefile(['main window'], '/tmp/file')
    e /tmp/file
    let winid = popup_create(bufnr(), {})
    " the main window displays 'main window'

    :call popup_settext(winid, 'popup')
    " the main window displays 'popup'

Solution: Do  *not* use  `popup_settext()` to  replace the  contents of  a popup
which displays a regular buffer.

Instead, close the popup and create a new one:

    call writefile(['main window'], '/tmp/file')
    e /tmp/file
    let winid = popup_create(bufnr(), {})

    :call popup_close(winid) | call popup_create('popup', {})
    "^------------------------------------------------------^

##
# Todo
## Install mappings to resize popup (`M-g C-[hjkl]`, use ad-hoc submode via timer).

Same thing for moving it (`M-g M-[hjkl]`, use ad-hoc submode via timer).

Btw, is `M-m` and `M-p` still a good choice in qfpreview?
It seems inconsistent with `M-g C-[jk]`.

---

And make `M-r` reset cursor to its original position when the popup/float was created.

---

And try to install a mapping (`M-g Tab`) to cycle between several popups/floats.
Implement a  stack of  popup/float ids; `M-g  Tab` would change  the top  of the
stack, and it would temporarily make  the popup/float flash (change `Normal` HG)
to get a visual clue.
Once  a  popup/float is  at  the  top of  the  stack  (and has  "flashed"),  all
scrolling/resizing/moving commands should target the latter.

---

Before all  that, you need  to write a library  function which would  repeat all
those custom commands without the `M-g` prefix (submode).
Once   it's   done,   get   rid  of   `vim-submode`   (too   complex;   probably
over-engineered); and rewrite this file using the library function:

    ~/.vim/autoload/slow_call/submode.vim

Update: Actually, I think you should try to assimilate `vim-submode`.
Also, try to assimilate `vim-tradewinds`, and install a mapping which would stop
`vim-window` from maximizing windows' height in the current tab page.

## Stop the timer which clears the cache when you scroll in a popup window, and start a new one.

See what we did here:

    " ~/.vim/plugged/vim-window/autoload/window.vim
    /window#resize

This should improve  the perf even more, and probably  make the whole experience
more consistent (there  is no reason to  change the last focused  popup right in
the middle of a series of scrolling motions).

## Customize the appearance of the preview popup.

Here are the default settings that Vim seemed  to use the last time it created a
preview popup for a help buffer:

    'highlight': 'Normal',
    'border': [],
    'mousemoved': [0, 0, 0],
    'line': 25,
    'close': 'button',
    'time': 0,
    'drag': 1,
    'cursorline': 0,
    'minheight': 11,
    'wrap': 1,
    'pos': 'botleft',
    'minwidth': 79,
    'fixed': 0,
    'col': 40,
    'maxwidth': 79,
    'zindex': 50,
    'firstline': 0,
    'title': ' /usr/local/share/vim/vim82/doc/helphelp.txt ',
    'scrollbar': 1,
    'posinvert': 1,
    'moved': [0, 0, 0],
    'mapping': 1,
    'tabpage': 0,
    'resize': 1,
    'maxheight': 11,

We've already started to customize the preview popup in `vim-window`:

    " ~/.vim/plugged/vim-window/plugin/window.vim
    /s:customize_preview_popup

Are there still some options we want to set?

FIXME: The title  of a  help preview popup  is still visible  when we've  run an
`:edit` command with a file argument matching an existing file.

    $ vim
    :e $MYVIMRC
    :h
    " press )
    " press p

## Are there settings which we want to apply in all popups?

For example, right now, we reset `'scl'` and `'wrap'` in help popups:

    " ~/.vim/plugged/vim-help/after/ftplugin/help.vim
    au BufWinEnter <buffer> if win_gettype() is# 'popup' | setl scl&vim wrap&vim cole&vim | endif

Do we want that only in *help* popups?  Or in *all* popups?
In the latter case, move the settings in `vim-window`.

## Check out how `:Verb` behaves now that we use a preview popup.

Check out any  custom command/function/plugin which uses  preview commands (like
`:pedit`, `&pvw`, `wincmd }`, ...).

Update: actually, it doesn't behave good.
You would need to install mappings to open file path on current line.
And you can't search for a pattern, or edit the file with `:g`/`:v`.

I think you should make `:Verb` use a regular window, to get more interactivity.

---

We've started some refactoring here and there.
For example, we fixed `!d` by invoking a new `lg#window#scratch()` function:

    " ~/.vim/plugged/vim-debug/autoload/debug/capture.vim
    call lg#window#scratch(vars)

Review this new function, and read `~/wiki/vim/todo/scratch.md`.

I suspect we need sth similar whenever we've used the preview window.
In particular, you'll probably need to refactor `debug#log#output()`.
I never liked this function; too complex; simplify it.

## Write a recipe showing how to set a popup title.

    from `qfpreview#open()`
    let title = printf('[%d/%d] %s', a:idx+1, size, bufname(curitem.bufnr))

    ...

    "\ set a title; it's displayed above the first item in the popup
    \ title: title,
    "\ how to highlight the title;
    "\ if the text is not visible enough, try `QuickFixLine`
    \ borderhighlight: ['Title'],
    "\ The first item needs to be `1`, otherwise the title is not highlighted as expected.{{{
    "\ .
    "\ This is because, without a border, the title is placed inside a padding line.
    "\ From `:h popup_create-arguments /^\s*title`:
    "\ .
    "\ >     If there is no top border one line of padding is added to put the title on.
    "\ }}}
    \ border: [1,0,0,0],
    "\ don't fill the empty cells in the title line with these characters: `═`
    \ borderchars: [' '],

## Document how to create a buffer-relative popup.

Create a dummy text property at the desired position in the buffer, then use the
`textprop` key in the options passed to `popup_create()`.

## I don't understand this excerpt from `:h preview-popup`:

    A few peculiarities:
    - If the file is in a buffer already, it will be re-used.  This will allow for
    editing the file while it's visible in the popup window.
    - No ATTENTION dialog will be used, since you can't edit the file in the popup
    window.  However, if you later open the same buffer in a normal window, you
    may not notice it's edited elsewhere.  And when then using ":edit" to
    trigger the ATTENTION and responding "A" for Abort, the preview window will
    become empty.

Update: I found an example to illustrate the second bullet point:

    " restart the current Vim instance (to be sure a swapfile exists for the current file)

    " start *another* Vim instance
    $ vim +'pedit ~/wiki/vim/popup.md' +'au! swapfile_handling'
    :e ~/wiki/vim/popup.md
    " no `[RO]` flag in status line (!!!!! document this, it's dangerous !!!!)
    :e
    " ATTENTION dialog; " press "a" to abort:  the popup gets empty

As for  the first bullet  point, I think  it means that  if the file  is already
loaded in a buffer, and you display it  in a popup, the latter will display this
buffer;  Vim won't re-read the buffer from the file.
Does that make sense?
Isn't that what Vim does all the time?  How is this a peculiarity?

Regarding this:

    " no `[RO]` flag in status line (!!!!! document this, it's dangerous !!!!)

Note  that the  issue persists  even  if you've  already closed  the popup  when
editing the file:

    $ vim +'pedit ~/wiki/vim/popup.md'
    :call popup_clear()
    :e ~/wiki/vim/popup.md
    " no `[RO]` flag in status line

---

I'm not sure you should have closed this issue: <https://github.com/vim/vim/issues/5822>
It *seems* to contradict what is documented in the previous excerpt.

## Find out why the width of the popup sometimes changes so much in a popup displaying a help buffer.

    $ vim -Nu NONE +'set nowrap mouse=a previewpopup=height:10,width:60'
    :h
    /ba\zsr
    :wincmd }

Scroll with the mouse.

The width  doesn't change  that much when  you run `:wincmd  }` from  an earlier
character (`|`, `b`, `a`).  But it still changes a little (why?).

Check the options  of the popup with `popup_getoptions()` between  a popup whose
width doesn't  change much, and  one whose  width changes a  lot; try to  find a
difference.

## After setting 'pvp', is it still ok for our scripts to run `wincmd P`?  What about `wincmd p`.

We have an item on this subject in our todo in vimrc (nr 38).

## Document that in a popup, Vim resets all window-local options to their default values.

Note that  in the  case of  `'wrap'`, this  behavior can  be overridden  via the
`wrap` key passed in the second argument of `popup_create()`.

---

Note  that the  default value  of `'wrap'`  is on,  while the  default value  of
`'linebreak'` is off.   If Vim wraps a long  line in a popup and  you don't like
where it gets broken, set `'linebreak'`.

How should we set `'wrap'` and `'linebreak'` in a popup?
I guess it depends on what it displays...

## Document that Vim does not reset window-local options (and buffer-local ones?) in a help popup.

Is it a bug?

    $ vim -Nu NONE +'set scl=yes previewpopup=height:10,width:60'
    :h
    /bar
    :wincmd }
    " notice that 'scl' has not been reset to 'auto' in the popup

Maybe not a bug.
From `:h popup-buffer`.

>     If a popup function is called to create a popup from text, **a new buffer** is
>     created to hold the text and text properties of the popup window.
>     [...]
>     - all other buffer-local and window-local options are set to their Vim default
>       value.

Maybe it only applies to only  ad-hoc buffers, created to display some arbitrary
text (!= existing buffers read from files).
If that's the case, the rule does not apply to help buffers which are read from files...

---

For now, I've fixed the issue with a `BufWinEnter` autocmd here:

    ~/.vim/plugged/vim-help/after/ftplugin/help.vim

It also  resets 'wrap' which  is not correctly reset  to 'on'; this  prevents us
from reading the end of long lines when previewing a help tag in a popup.

## Port calendar.vim to Vim.

<https://gist.github.com/lacygoill/c9ce255ff5026505e8cbfa7ceb7de6ba>

    " Config {{{1

    const s:FORMAT = '%A %B %d %Y'
    const s:KEYMAPPING = 'cd'
    hi CalCurrentDay ctermbg=black guibg=black ctermfg=white guifg=white

    " Implementation {{{1

    exe 'nno <silent> '..s:KEYMAPPING..' :<c-u>call <sid>calendar_widget()<cr>'

    fu s:calendar_widget() abort
        let lines = systemlist('cal')[:-2]
        call s:trim(lines)
        let bufnr = nvim_create_buf(v:false, v:true)
        call nvim_buf_set_lines(bufnr, 0, -1, v:true, lines)
        let opts = {
            \ 'relative': 'editor',
            \ 'style': 'minimal',
            \ 'width': 20+&so,
            \ 'height': len(lines),
            \ 'row': 1,
            \ 'col': &columns,
            \ 'anchor': 'NE',
            \ }
        call nvim_open_win(bufnr, 1, opts)
        let s:current = s:current() | let s:orig = deepcopy(s:current)
        call s:highlight_current_day()
        nno <buffer><nowait><silent> <cr> :<c-u>call <sid>insert_date()<cr>
        nno <buffer><nowait><silent> H :<c-u>call <sid>another_month('prev')<cr>
        nno <buffer><nowait><silent> L :<c-u>call <sid>another_month('next')<cr>
    endfu

    fu s:current() abort
        let [month, year] = matchlist(getline(1), '\(\a\+\)\s\+\(\d\+\)')[1:2]
        let month = {
            \ 'January': 1,
            \ 'February': 2,
            \ 'March': 3,
            \ 'April': 4,
            \ 'May': 5,
            \ 'June': 6,
            \ 'July': 7,
            \ 'August': 8,
            \ 'September': 9,
            \ 'October': 10,
            \ 'November': 11,
            \ 'December': 12,
            \ }[month]
        return {'month': month, 'year': str2nr(year)}
    endfu

    fu s:trim(lines) abort
        call map(a:lines, {_,v -> substitute(v, '\s\+$', '', '')})
    endfu

    fu s:highlight_current_day() abort
        let id = nvim_create_namespace('cal')
        let ctrl_seq = '_\b _\b'
        call search(ctrl_seq..'\d\+')
        call nvim_buf_add_highlight(0, id, 'CalCurrentDay',
            \ line('.')-1, col('.'), searchpos(ctrl_seq..'\d\+\zs', 'cn')[1]-1)
        sil exe 'keepj keepp lockm %s/'..ctrl_seq..'//ge'
    endfu

    fu s:another_month(which) abort
        if a:which is# 'next' && s:current.month == 12
            let s:current.month = 1
            let s:current.year += 1
        elseif a:which is# 'prev' && s:current.month == 1
            let s:current.month = 12
            let s:current.year -= 1
        else
            let s:current.month += a:which is# 'next' ? 1 : -1
        endif
        sil %d_
        let lines = systemlist('cal -m '..s:current.month..' '..s:current.year)[:-2]
        call s:trim(lines)
        call nvim_buf_set_lines(0, 0, -1, v:true, lines)
        if s:current == s:orig
            call s:highlight_current_day()
        endif
    endfu

    fu s:insert_date() abort
        let number_under_cursor = '\%(.*\%'..col('.')..'c\)\@=\d\+'..'\%(\%'..col('.')..'c.*\)\@<='
        let day = matchstr(getline('.'), number_under_cursor)
        if day is# '' | return | endif
        let [month, year] = matchlist(getline(1), '\(\a\+\)\s\+\(\d\+\)')[1:2]
        let date = system(printf('date -d "%s %d %d" +"%s"', month, day, year, s:FORMAT))[:-2]
        call nvim_win_close(0, 1)
        let line = nvim_get_current_line()
        let new_line = substitute(line, '\%'..col('.')..'c', date, '')
        call nvim_set_current_line(new_line)
    endfu

Write some recipe/plugin.

## Read `:h popup` in its entirety?

Or maybe just document the main concepts and functions.

