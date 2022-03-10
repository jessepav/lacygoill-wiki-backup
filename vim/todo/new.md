# functions

   - `:help appendbufline()` + `:help deletebufline()`
   - `:help charclass()`
   - `:help chdir()`
   - `:help complete_info()` + 'user_data' entry in completion item
   - `:help environ()` + `:help getenv()` + `:help setenv()`
   - `:help expandcmd()`
   - `:help fullcommand()`
   - `:help gettagstack()` + `:help settagstack()`
   - `:help interrupt()`
   - `:help prop_add_list()`
   - `:help pum_getpos()`
   - `:help setcellwidths()`
   - `:help str2list()` + `:help list2str()`
   - `:help strptime()` (*str*ing *p*arse *time* ?)
   - `:help term_setansicolors()` + `:help term_getansicolors()`
   - `:help term_setsize()`
   - `:help terminalprops()`

   - `:help getcharpos()` (alternative to `getpos()` based on characters instead of bytes)
   - `:help setcharpos()` (alternative to `setpos()` based on characters instead of bytes)
   - `:help getcursorcharpos()` (alternative to `getcurpos()` based on characters instead of bytes)
   - `:help setcursorcharpos()`

---

`:help  bufadd()` and  `:help  bufload()` are  useful  to  edit a  file  which is  not
currently  loaded, with  `deletebufline()`,  `setbufline()`,  ... and  *without*
side effects (e.g. no window opened/closed which could alter the layout).

    " buffer gets `u` flag in `:ls` output
    let bufnr = expand('~/.shrc')->bufadd()
    " buffer gets `u` and `h` flag in `:ls` output
    call bufload(bufnr)
    call appendbufline(bufnr, 1, ['some', 'text'])

... but how do you save it?
Answer: with `:wall`:

    $ echo ''>/tmp/file
    $ vim +'let bufnr = expand("/tmp/file")->bufadd()' \
          +'call bufload(bufnr)' \
          +'call setbufline(bufnr, 1, ["some", "text"])' \
          +'sil wall' \
          +'qa!'
    $ cat /tmp/file
    some
    text

---

I  think  `strptime()`  is  useful  to convert  a  human-readable  date  into  a
machine-readable form.  Useful when you need  to do some computation on it.  For
example, you might  want to sort human-readable dates; `strptime()`  may help by
temporarily converting the dates into simple integers.

## arguments of functions

   - `:help getbufinfo()` includes a `linecount` key in the output dictionary since 8.2.0019
   - `:help getcompletion()` supports the `cmdline` argument since 8.2.0925
   - `:help getcurpos()` supports a new argument `winid` since 8.2.1727
   - `:help getloclist()` supports a `filewinid` key in the optional dictionary argument since 8.1.0345
   - `:help line()` supports an optional `{winid}` argument since 8.1.1967

   - `:help matchadd()` supports a new `window` key in the optional dictionary argument;
     see also `:help matchdelete()`, `:help clearmatches()`, `:help getmatches()` and `:help setmatches()`,
     they all accept a new optional window ID argument

   - `:help mode()` can output `n_ov`, `n_oV`, `n_oC-v` since 8.1.0648
   - `:help readdir()` and `:help readdirex()` support a new optional `{dict}` argument
   - `:help search()` supports a new `{skip}` argument
   - `:help winnr()` supports a new argument `{N}[hjkl]` since 8.1.1140
   - `:help getqflist()` supports the new arguments `end_col` and `end_lnum` since 8.2.3019
   - `:help prop_list()` supports new keys in the optional argument `{props}`:
     `end_lnum`, `types`, `ids`
   - `:help win_move_separator()` and `:help win_move_statusline()`

## output of functions

   - `:help win_gettype()` can now output `preview` and `autocmd`

##
# commands
## Ex

   - `:help :argdedupe`
   - `:help :balt`
   - `:help :echoconsole`
   - `:help :scriptversion`
   - `:help :swapname`

### arguments

   - `:help ctermul` (argument of `:help :highlight`)
     + terminal options: `:help t_AU`, `:help t_8u`, `:help t_Cs`, `:help t_Ce`

   - `:help :cq` (`:{N}cq[uit][!]`, Quit Vim with error code {N}.)

   - `:help :unlet-$`

   - `:help :vimgrep` (`f` flag for fuzzy search)

##
## visual mode

   - `:help v_P`
     `P` does not change the unnamed register.
     But it still changes the small/big deletion register (aka `"-` and `"1`).

## select mode

   - `:help v_CTRL-R`

##
# events

   - `:help CmdlineChanged`
   - `:help CompleteChanged`
   - `:help CompleteDonePre`
   - `:help DiffUpdated`
   - `:help DirChangedPre`
   - `:help DirChanged`
   - `:help ExitPre`
   - `:help InsertLeavePre`
   - `:help ModeChanged`
   - `:help SigUSR1`
   - `:help SourcePost`
   - `:help TextChangedP`
   - `:help TextChangedP`
   - `:help WinClosed`

Note: `InsertLeave` is fired right *after* leaving insert mode.
`InsertLeavePre` is fired right *before* leaving insert mode.

# options

   - `:help 'autoshelldir'`

   - `:help 'quickfixtextfunc'`

   - `:help 'varsofttabstop'` + `:help 'vartabstop'`

   - `:help 'wildoptions'` (`fuzzy` item)

   - `:help 'wincolor'`; could be used to dim the unfocused windows

# `v:` variables

   - `v:collate`
   - `v:exiting`
   - `v:maxcol`

---

When `TextYankPost` is fired, `v:event` now contains a `visual` key.
Could be useful for our `vim-selection-ring` plugin...

##
# Miscellaneous
## `:help prompt-buffer`

## `:help falsy-operator`

Also known as "null coalescing operator".

Example:

    :echo 0 ?? 'str'
    str˜

    :echo 0 ?? '' ?? [0]
    [0]˜

    :echo 0 ?? '' ?? [] ?? #{key: 123}
    {'key': 123}˜

Not sure,  but maybe the expression  "null coalescing" comes from  the fact that
this operator lets you ignore/reduce/coalesce  an arbitrary number of null/false
values.

It can be somewhat emulated with `?:`:

    const a = b ?? 3
    ⇔
    const a = b ? b : 3

But actually, the two are not really equivalent.
With `?:`, `b` is evaluated twice.
With `??`, `b` is evaluated only once.
This difference matters if the evaluation has side-effects.

The operator was introduced in 8.2.1794.

---

Note that it doesn't work with an undefined variable:

    :echo var ?? 123
    E121: Undefined variable: var˜

Should we ask for this to work as a feature request?

##
# Review `https://arp242.net/vimlog/`

Check whether we've missed some interesting new feature in the recent past.

