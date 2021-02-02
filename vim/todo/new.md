# functions

   - `:h appendbufline()` + `:h deletebufline()`
   - `:h charclass()`
   - `:h charcol()`
   - `:h charidx()`
   - `:h chdir()`
   - `:h complete_info()` + 'user_data' entry in completion item
   - `:h environ()` + `:h getenv()` + `:h setenv()`
   - `:h expandcmd()`
   - `:h getcharpos()`
   - `:h getcursorcharpos()`
   - `:h gettagstack()` + `:h settagstack()`
   - `:h interrupt()`
   - `:h listener_add()`
   - `:h listener_remove()`
   - `:h pum_getpos()`
   - `:h readdir()` + `:h readdirex()`
   - `:h setcellwidths()`
   - `:h setcharpos()`
   - `:h setcursorcharpos()`
   - `:h slice()`
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

I  think  `strptime()`  is  useful  to convert  a  human-readable  date  into  a
machine-readable form.  Useful when you need  to do some computation on it.  For
example, you  may want to  sort human-readable  dates; `strptime()` may  help by
temporarily converting the dates into simple integers.

---

Don't try to use `typename()` to blindly replace every `v:t_*` variable, like this:
Should we do this kind of refactoring?

    if type(expr) == v:t_number
    →
    if typename(expr) == 'number'

First, it's more verbose.
Second, for composite types, it makes the code less readable:

    if type(expr) == v:t_dict
    →
    if typename(expr)[: 3] == 'dict'
                     ^---^
                     ugly

However, `typename()` is useful when you need to get more info about the type of
a composite type.  For example, if you  want to check whether an expression is a
list of dictionaries of jobs, you can simply write:

    if typename(expr) == 'list<dict<job>>'

## arguments of functions

   - `:h expand()` supports a new `<stack>` argument `{N}[hjkl]` since 8.2.1297
   - `:h getbufinfo()` includes a `linecount` key in the output dictionary since 8.2.0019
   - `:h getcompletion()` supports the `cmdline` argument since 8.2.0925
   - `:h getcurpos()` supports a new argument `winid` since 8.2.1727
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

   - `:h :balt`
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
   - `:h InsertLeavePre`
   - `:h SigUSR1`
   - `:h SourcePost`
   - `:h TextChangedP`

Note: `InsertLeave` is fired right *after* leaving insert mode.
`InsertLeavePre` is fired right *before* leaving insert mode.

# options

   - `:h 'quickfixtextfunc'`

   - `:h 'varsofttabstop'` + `:h 'vartabstop'`

   - `:h 'wincolor'`; could be used to dim the unfocused windows

# `v:` variables

   - `v:collate`
   - `v:exiting`

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

## `:h falsy-operator`

Also known as "null coalescing operator".

Example:

    :echo 0 ?? 'str'
    str~

    :echo 0 ?? '' ?? [0]
    [0]~

    :echo 0 ?? '' ?? [] ?? #{key: 123}
    {'key': 123}~

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
    E121: Undefined variable: var~

Should we ask for this to work as a feature request?

##
# Review `https://arp242.net/vimlog/`

Check whether we've missed some interesting new feature in the recent past.

