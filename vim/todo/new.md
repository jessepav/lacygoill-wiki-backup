# functions

   - `:h appendbufline()` + `:h deletebufline()`
   - `:h charclass()`
   - `:h chdir()`
   - `:h complete_info()` + 'user_data' entry in completion item
   - `:h environ()` + `:h getenv()` + `:h setenv()`
   - `:h expandcmd()`
   - `:h gettagstack()` + `:h settagstack()`
   - `:h interrupt()`
   - `:h listener_add()`
   - `:h listener_remove()`
   - `:h pum_getpos()`
   - `:h readdir()` + `:h readdirex()`
   - `:h reduce()`
   - `:h setcellwidths()`
   - `:h str2list()` + `:h list2str()`
   - `:h strptime()` (*str*ing *p*arse *time* ?)
   - `:h term_setansicolors()` + `:h term_getansicolors()`
   - `:h term_setsize()`
   - `:h terminalprops()`
   - `:h win_splitmove()`

---

`:h  bufadd()` and  `:h  bufload()` are  useful  to  edit a  file  which is  not
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

Look for `eval(.*join(` everywhere.
For every match, check whether we could use `reduce()` instead.

---

I  think  `strptime()`  is  useful  to convert  a  human-readable  date  into  a
machine-readable form.  Useful when you need  to do some computation on it.  For
example, you  may want to  sort human-readable  dates; `strptime()` may  help by
temporarily converting the dates into simple integers.

## arguments of functions

   - `:h expand()` supports a new `<stack>` argument `{N}[hjkl]` since 8.2.1297
   - `:h getbufinfo()` includes a `linecount` key in the output dictionary since 8.2.0019
   - `:h getcompletion()` supports the `cmdline` argument since 8.2.0925
   - `:h getloclist()` supports a `filewinid` key in the optional dictionary argument since 8.1.0345
   - `:h line()` supports an optional `{winid}` argument since 8.1.1967

   - `:h matchadd()` supports a new `window` key in the optional dictionary argument;
     see also `:h matchdelete()`, `:h clearmatches()`, `:h getmatches()` and `:h setmatches()`,
     they all accept a new optional window ID argument

   - `:h mode()` can output `n_ov`, `n_oV`, `n_oC-v` since 8.1.0648
   - `:h readdir()` and `:h readdirex()` support a new optional `{dict}` argument
   - `:h search()` supports a new `{skip}` argument
   - `:h setqflist()` supports a new `quickfixtextfunc` key inside the `{what}` dictionary since 8.2.0869
   - `:h trim()` can trim only at the start or end thanks to the third optional argument `{dir}` since 8.2.0868
   - `:h winnr()` supports a new argument `{N}[hjkl]` since 8.1.1140

## output of functions

   - `:h win_gettype()` can now output `preview` and `autocmd`

##
# commands

   - `:h :scriptversion`
   - `:h :swapname`

## arguments of commands

   - `:h ctermul` (argument of `:hi`) + terminal options: `:h t_AU`, `:h t_8u`, `:h t_Cs`, `:h t_Ce`

   - `:h :cq` (`:{N}cq[uit][!]`, Quit Vim with error code {N}.)

   - `:h :unlet-$`

##
# events

   - `:h CmdlineChanged`
   - `:h CompleteChanged`
   - `:h CompleteDonePre`
   - `:h DiffUpdated`
   - `:h DirChanged`
   - `:h ExitPre`
   - `:h SigUSR1`
   - `:h SourcePost`
   - `:h TextChangedP`

# options

   - `:h 'quickfixtextfunc'`

   - `:h 'varsofttabstop'` + `:h 'vartabstop'`

   - `:h 'wincolor'`; could be used to dim the unfocused windows

# `v:` variables

   - `v:collate`

---

When `TextYankPost` is fired, `v:event` now contains a `visual` key.
Could be useful for our `vim-selection-ring` plugin...

##
# Miscellaneous
## `:h literal-Dict`

## `:h method` and `:h :eval`

You can't write that:

    :call expr->func()

Where `expr` is not a function (custom or builtin; doesn't matter).

Example:

    :call 'some string'->strlen()
    E129: Function name required~

You *could* write that:

    :sil echo expr->func()

But that's awkward; that's where `:eval` comes in:

    :eval expr->func()

Obviously, that's only useful if `func()` has a side-effect.

---

Maybe we should refactor all `:call func(expr)` into `:eval expr->func()`.
In fact, `:call func()` can be replaced by `:eval func()`.
Does that mean that `:call` is useless now?
Should we remove it everywhere?

I think `:call` has 2 benefits over `:eval`:

   - it can be followed by a bar (`:eval` consumes it)
   - it supports a range (`:h E132`)

## `:h prompt-buffer`

##
# Review `https://arp242.net/vimlog/`

Check whether we've missed some interesting new feature in the recent past.

