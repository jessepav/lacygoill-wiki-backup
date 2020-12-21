# New functions to
## detect the pager is active, and customize the mappings which interacts with the pager

Would it be enough?

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
# Miscellaneous
## Provide a mechanism to annotate mappings (like tmux)?

I'm not sure it's  a good idea.  We need to experiment with  the feature in tmux
to see how it works, how useful it is, and how it could be ported into Vim.

## Suppress hit-enter prompt when looking for a very long pattern.
```vim
vim9script
setline(1, repeat(['the quick brown fox jumps over the lazy dog'], 3))
:%j
('/' .. repeat(['the weird brown fox jumps over the lazy dog'], 3)->join() .. "\r")->feedkeys()
```
Notice the hit-enter prompt.
```vim
vim9script
setline(1, repeat(['the quick brown fox jumps over the lazy dog'], 3))
:%j
('/' .. repeat(['the quick brown fox jumps over the lazy dog'], 3)->join() .. "\r")->feedkeys()
set shm-=S
```
Again, notice the hit-enter prompt.

Press  Enter, then  `n`; notice  that this  time, there's  no hit-enter  prompt,
because the pattern is truncated in the middle:

    /the quick brown fox jumps over the la...x jumps over the lazy dog        [1/1]
                                          ^^^
                                          truncation

This is neat.  Could  Vim do the same thing in the 2  previous cases, so that we
never have  this annoying  hit-enter prompt?  If  it breaks  compatibility, then
maybe we could ask for a new flag in `'shortmess'`...

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
        let new_hist = getline(1, '$')->filter({_, v -> v !~# '^\s*$' && v !~# '^.\{,5}$'})
        call histdel(':')
        for line in new_hist
            call histadd(':', line)
        endfor
        let viminfo = expand($HOME .. '/.viminfo')
        if !filereadable(viminfo) | return | endif
        let info = readfile(viminfo)
        let deleted_entries = copy(s:old_cmd_hist)->filter({_, v -> index(new_hist, v) == -1})
        call map(deleted_entries, {_, v -> index(info, ':' .. v)})
        call filter(deleted_entries, {_, v -> v >= 0})->sort()
        if empty(deleted_entries) | return | endif
        for entry in reverse(deleted_entries)
            call remove(info, entry, entry + 1)
        endfor
        call writefile(info, viminfo, 'b')
    endfu

But it was not reliable; often, the whole command history would be cleared.
Besides,  there were  other issues  (it  failed to  remove a  line containing  a
literal carriage return, ...).

