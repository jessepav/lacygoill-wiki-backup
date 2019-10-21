# New functions to
## detect the pager is active, and customize the mappings which interacts with the pager

Would it be enough?

## get the owner/group of a file

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

The issue is specific to Vim.
In Nvim, you can "fix" it by making sure that the `pum` item is in the value of `'wop'`.

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

