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
# Issues
## can't customize `C-k` when a dictionary completion is active

If you have a mapping on `C-k`, you've just pressed `C-x C-k`, and you press `C-k`,
Vim will scroll in the wildmenu; it will not invoke your custom mapping.

---

Same issue for other completions: `C-x C-t`, `C-x C-d`, `C-x C-l`, ...

## can't set `'foldopen'` and `'foldclose'` locally to a buffer

It would be useful to toggle an auto-open-fold mode in an arbitrary buffer.

    nno <silent> coz :<c-u>call <sid>auto_open_fold('enable')<cr>

    fu! s:auto_open_fold(action) abort
        if s:auto_open_fold('is_active')
            call s:auto_open_fold('disable')
            echo '[auto open folds] OFF'
        else
            call s:auto_open_fold('enable')
            echo '[auto open folds] ON'
        endif
        if a:action is# 'is_active'
            return exists('s:fold_options_save')
        elseif a:action is# 'enable' && !exists('s:fold_options_save')
            let s:fold_options_save = {
            \                           'close'  : &foldclose,
            \                           'open'   : &foldopen,
            \                           'enable' : &foldenable,
            \                           'level'  : &foldlevel,
            \                         }
            set foldclose=all
            set foldopen=all
            set foldenable
            set foldlevel=0
        elseif a:action is# 'disable' && exists('s:fold_options_save')
            for op in keys(s:fold_options_save)
                exe 'let &fold'.op.' = s:fold_options_save.'.op
            endfor
            norm! zMzv
            unlet! s:fold_options_save
        endif
    endfu

