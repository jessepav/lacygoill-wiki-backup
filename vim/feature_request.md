# New functions to
## detect the pager is active, and customize the mappings which interacts with the pager

Would it be enough?

## get the owner/group of a file

## substitute text in buffer

function to substitute text in buffer without side effects

**Is your feature request related something that is currently hard to do? Please describe.**

It is difficult to substitute all matches of a pattern with a replacement text inside the current buffer without side effects.

---

For example, consider this text in a buffer:

    pat pat PAT
    pat pat PAT
    pat pat PAT

The cursor is on line 2 column 5, and this substitution is executed:

    :%s/pat/rep/g

The cursor is now on line 3 column 1:

    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'norm! 2Gw' +'set vbs=1|echo getpos(".")|qa!'

    [0, 2, 5, 0]
        ^  ^

    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'norm! 2Gw' +'%s/pat/rep/g' +'set vbs=1|echo getpos(".")|qa!'

    [0, 3, 1, 0]
        ^  ^

In a script, to preserve the cursor position and the view, `winsaveview()` and `winrestview()` must be invoked:

    let view = winsaveview()
    %s/pat/rep/g
    call winrestview(view)

---

A substitution also adds an entry in the jumplist:

    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'set vbs=1|jumps|qa!'

     jump line  col file/text
       1     4    0

    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'%s/pat/rep/g' +'set vbs=1|jumps|qa!'

     jump line  col file/text
       2     4    0
       1     3    0 rep rep PAT

In a script, to preserve the jumplist, `:keepjumps` must be invoked:

    keepjumps %s/pat/rep/g
    ^-------^

---

A substitution also alters the change marks:

    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'norm! 2Gwyiw' +'set vbs=1|marks|qa!' 2>&1 | grep '\[\|\]'

     [      2    4 pat pat PAT
     ]      2    6 pat pat PAT

    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'norm! 2Gwyiw' +'%s/pat/rep/g' +'set vbs=1|marks|qa!' 2>&1 | grep '\[\|\]'

     [      1    0 rep rep PAT
     ]      4    0

In a script, to preserve the change marks, `:lockmarks` must be invoked (requires [`8.1.2302`](https://github.com/vim/vim/releases/tag/v8.1.2302)):

    lockmarks %s/pat/rep/g
    ^-------^

---

A substitution also alters the search register:

    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'/foo' +'set vbs=1|echo @/|qa!'

    foo

    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'/foo' +'%s/pat/rep/g' +'set vbs=1|echo @/|qa!'

    pat

In a script, to preserve the search register, `:keeppatterns` must be invoked:

    keeppatterns %s/pat/rep/g
    ^----------^

---

If the number of changed lines is greater than `&report`, then a message is written on the command-line.  In a script, to prevent a message from being displayed, `:silent` must be invoked:

    silent %s/pat/rep/g
    ^----^

And the `e` flag must be used to avoid `E486` when the pattern is not found:

    silent %s/pat/rep/ge
                       ^

---

If the user has set `'gdefault'`, then the meaning of the `g` flag is reversed.

    # 'gdefault' is *not* set
    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'set nogdefault' +'%s/pat/rep/g' +'%p|qa!'
    rep rep PAT
    rep rep PAT
    rep rep PAT

    # 'gdefault' *is* set
    $ vim -es -Nu NONE -i NONE +"pu=repeat(['pat pat PAT'], 3)" +'set gdefault' +'%s/pat/rep/g' +'%p|qa!'
    rep pat PAT
    rep pat PAT
    rep pat PAT

In a script, to be sure all matches are replaced, the value of the option must be inspected:

    execute '%s/pat/rep/'..(&gdefault ? '' : 'g')

---

All in all, if you combine everything, the interactive command:

    %s/pat/rep/g

Becomes this in a script which tries to have as fewer side effects as possible and be reliable:

    let view = winsaveview()
    silent execute 'keepjumps keeppatterns lockmarks %s/pat/rep/e'..(&gdefault ? '' : 'g')
    call winrestview(view)

**Describe the solution you'd like**

A `buf_substitute()` function which would take 5 arguments:

    {lnum}, {end}, {pat}, {sub}, {flags}

The `{pat}`, `{sub}`, `{flags}` arguments would be interpreted as in `substitute()`, while the `{lnum}` and `{end}` arguments would be interpreted as the first and last line of a range of lines in the buffer where the substitution should occur.  It would have none of the side effects described earlier.

In a script, `%s/pat/rep/g` could then be re-written like this:

    call buf_substitute(1, '$', 'pat', 'rep', 'g')

**Describe alternatives you've considered**

I've considered writing a custom function which would avoid all the side effects documented earlier, then use the latter whenever I need to do a substitution in a buffer.  Somewhat similar to [`maktaba#buffer#Substitute()`](https://github.com/google/vim-maktaba/blob/ed4357d2caf1d04bd229a24191098759f94b2e25/autoload/maktaba/buffer.vim#L129-L180).

But it would create a dependency in each plugin I would write.

Besides, it would create a difference between the context where the function is called, and the one where the substitution is executed.  This would make it hard to refer to a script-local or function-local variable in the pattern or replacement arguments, if in the end the substitution is not executed in the context of the current script/function but in the context of another function defined in another script.

---

I've also considered using a combination of `setline()`+`getline()`+`map()`+`substitute()`:

    call getline(1, '$')->map('substitute(v:val, "pat", "rep", "g")')->setline(1)

But it's less readable than:

    call buf_substitute(1, '$', 'pat', 'rep', 'g')

And it's much slower than `:s`:

    mv /tmp/version8.txt{,.bak}; vim -Nu NONE +'h version8' +'saveas /tmp/version8.txt|qa!'; for i in {1..10}; do vim -es -Nu NONE -i NONE +"let time = reltime()|%s/pat/rep/g|0pu=matchstr(reltimestr(reltime(time)), '.*\..\{,3}').' seconds to run :s'" +'1p|qa!' /tmp/version8.txt; done

    0.010 seconds to run :s
    0.009 seconds to run :s
    0.009 seconds to run :s
    0.012 seconds to run :s
    0.009 seconds to run :s
    0.008 seconds to run :s
    0.008 seconds to run :s
    0.008 seconds to run :s
    0.008 seconds to run :s
    0.011 seconds to run :s

    # average: 0.009 seconds

    mv /tmp/version8.txt{,.bak}; vim -Nu NONE +'h version8' +'saveas /tmp/version8.txt|qa!'; for i in {1..10}; do vim -es -Nu NONE -i NONE +"let time = reltime()|call getline(1, '$')->map('substitute(v:val, \"pat\", \"rep\", \"g\")')->setline(1)|0pu=matchstr(reltimestr(reltime(time)), '.*\..\{,3}').' seconds to run setline()->...'" +'1p|qa!' /tmp/version8.txt; done

    0.129 seconds to run setline()->...
    0.123 seconds to run setline()->...
    0.123 seconds to run setline()->...
    0.128 seconds to run setline()->...
    0.130 seconds to run setline()->...
    0.162 seconds to run setline()->...
    0.154 seconds to run setline()->...
    0.161 seconds to run setline()->...
    0.128 seconds to run setline()->...
    0.123 seconds to run setline()->...

    # average: 0.136 seconds

That's 15 times slower.

##
# New argument to
## function
### `getfsize()` to get a human readable result

##
## command
### `:prof` (`dump` and `stop`)

<https://github.com/neovim/neovim/pull/2427>

##
# New highlight group for
## the background of the wildmenu

There is a HG for the items in  the wildmenu (`:hi WildMenu`), but *not* for the
background of the wildmenu.

This is an issue if you set `'wmh'` to 0:

    $ vim -Nu NONE +'colo evening' +'set wildmenu wmh=0' +'sp|sp|wincmd w|wincmd _'
    :Tab

The  wildmenu  is hard  to  distinguish  from  the  status line,  because  their
background  is  highlighted by  the  same  HG  (`:hi  StatusLine`); it's  a  bit
confusing.

The issue only arises in the second window counting from the bottom:

   - in the first window, the wildmenu replaces the status line of the current
     window (so no confusion)

   - in the third window, the wildmenu is separated from the status line of the
     current window by the status line of an inactive window which is
     highlighted by a different HG: `StatusLineNC` (so again, no confusion)

   - in the fourth window, the wildmenu is separated from the status line of the
     current window by 2 status lines of inactive windows...

   - ...

## a folded line outside the text

`Folded`  controls the  color  of a  folded  line;  maybe it  would  be nice  to
highlight the title of a fold with special colors, but not the rest of the line.

##
# Issues
## can't customize `C-k` when a dictionary completion is active

If you have a mapping on `C-k`, you've just pressed `C-x C-k`, and you press `C-k`,
Vim will scroll in the wildmenu; it will not invoke your custom mapping.

---

Same issue for other completions: `C-x C-t`, `C-x C-d`, `C-x C-l`, ...

## can't set `'foldopen'` and `'foldclose'` locally to a buffer

It would be useful to toggle an auto-open-fold mode in an arbitrary buffer.

---

Right now,  we do it by  installing temporary mappings (`j`,  `k`, `C-d`, `C-u`,
`gg`, `G`), which automatically open folds.

## can't customize the command-line history interactively

It would be nice to be able to remove an Ex command from the history by deleting
its  line  in  the  command-line  window.

I tried in the past:

    au CmdWinEnter : let s:old_cmd_hist = getline(1, line('$')-1)
    au CmdWinLeave : au WinEnter * ++once call s:update_history()

    fu s:update_history() abort
        let new_hist = filter(getline(1, '$'), {_,v -> v !~# '^\s*$' && v !~# '^.\{,5}$'})
        call histdel(':')
        for line in new_hist
            call histadd(':', line)
        endfor
        let viminfo = expand($HOME..'/.viminfo')
        if !filereadable(viminfo) | return | endif
        let info = readfile(viminfo)
        let deleted_entries = filter(copy(s:old_cmd_hist), {_,v -> index(new_hist, v) == -1})
        call map(deleted_entries, {_,v -> index(info, ':'..v)})
        call sort(filter(deleted_entries, {_,v -> v >= 0}))
        if empty(deleted_entries) | return | endif
        for entry in reverse(deleted_entries)
            call remove(info, entry, entry + 1)
        endfor
        call writefile(info, viminfo, 'b')
    endfu

But it was not reliable; often, the whole command history would be cleared.
Besides,  there were  other issues  (it  failed to  remove a  line containing  a
literal carriage return, ...).

