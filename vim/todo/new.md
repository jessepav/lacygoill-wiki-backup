# functions

   - `:h appendbufline()` + `:h deletebufline()`
   - `:h chdir()`
   - `:h complete_info()` + 'user_data' entry in completion item
   - `:h environ()` + `:h getenv()` + `:h setenv()`
   - `:h expandcmd()`
   - `:h gettagstack()` + `:h settagstack()`
   - `:h interrupt()`
   - `:h listener_add()`
   - `:h listener_remove()`
   - `:h pum_getpos()`
   - `:h rand()` + `:h srand()`
   - `:h sign_define()`
   - `:h sign_getdefined()`
   - `:h sign_getplaced()`
   - `:h sign_place()`
   - `:h sign_undefined()`
   - `:h sign_unplace()`
   - `:h str2list()` + `:h list2str()`
   - `:h strptime()`
   - `:h term_setansicolors()` + `:h term_getansicolors()`
   - `:h term_setsize()`
   - `:h win_splitmove()`

---

`:h  bufadd()` and  `:h  bufload()` are  useful  to  edit a  file  which is  not
currently  loaded, with  `deletebufline()`,  `setbufline()`,  ... and  *without*
side-effects (e.g. no window opened/closed which could alter the layout).

    " buffer gets `u` flag in `:ls` output
    let bufnr = bufadd(expand('~/.shrc'))
    " buffer gets `u` and `h` flag in `:ls` output
    call bufload(bufnr)
    call appendbufline(bufnr, 1, ['some', 'text'])

... but how do you save it?
Answer: with `:wall`:

    $ echo ''>/tmp/file
    $ vim +'let bufnr = bufadd(expand("/tmp/file"))' \
          +'call bufload(bufnr)' \
          +'call setbufline(bufnr, 1, ["some", "text"])' \
          +'sil wall' \
          +'qa!'
    $ cat /tmp/file
    some
    text

## arguments of functions

   - `:h getbufinfo()` includes a `linecount` key in the output dictionary since 8.2.0019
   - `:h getloclist()` supports a `filewinid` key in the optional dictionary argument since 8.1.0345
   - `:h line()` supports an optional `{winid}` argument since 8.1.1967

   - `:h matchadd()` supports a new `window` key in the optional dictionary argument;
     see also `:h matchdelete()`, `:h clearmatches()`, `:h getmatches()` and `:h setmatches()`,
     they all accept a new optional window ID argument

   - `:h mode()` can output `n_ov`, `n_oV`, `n_oC-v` since 8.1.0648
   - `:h winnr()` supports a new argument `{N}[hjkl]` since 8.1.1140

##
# commands

   - `:h :scriptversion`
   - `:h :swapname`

## arguments of commands

   - `:h :cq` (`:{N}cq[uit][!]`, Quit Vim with error code {N}.)

   - `:tabnext` accepts the argument `#` to focus previous tab (Nvim only)
     https://github.com/neovim/neovim/pull/11626/files

   - `:h :unlet-$`

##
# events

   - `:h CmdlineChanged`
   - `:h CompleteChanged`
   - `:h CompleteDonePre`
   - `:h DiffUpdated`
   - `:h DirChanged`
   - `:h ExitPre`
   - `:h SourcePost`
   - `:h TextChangedP`
   - `:h WinClosed` (Nvim only)

# options

   - `:h 'varsofttabstop'` + `:h 'vartabstop'`

   - `:h 'wincolor'` (Vim only); could be used to dim the unfocused windows
    (I think the equivalent in Nvim is `'winhighlight'`; see also `:h hl-NormalNC` and `:h hl-NormalFloat`)

# `v:` variables

   - `:h v:argv` (command-line arguments Vim was invoked with; Vim only)
   - `:h v:echospace`

##
# Miscellaneous
## `:h api-extended-marks` (Nvim only)

## `:h api-buffer-updates` (Nvim only)

## `:h literal-Dict` (Vim only)

## `:h method` and `:h :eval`

This new syntax can improve the readability of nested function calls:

    funcA(funcB(funcC(arg)))

  vs

    arg->funcA()->funcB()->funcC()

Surprisingly, there are not that many  refactorings atm (only ≈ 600); search for
this pattern:

    )\_s*\\\=\s*))\@!

---

You can't write that:

    :call expr->func()

Where `func()` is  a function which mutates  `expr` or has a  side-effect on Vim
(option, buffer, ...).

You could write that:

    :sil echo expr->func()

But that's awkward; that's where `:eval` comes in:

    :eval expr->func()

---

Maybe we should refactor all `:call func(expr)` into `:eval expr->func()`.
In fact, `:call func()` can be replaced with `:eval func()`.
Does that mean that `:call` is useless now?
Should we remove it everywhere?

I think  the only thing `:call`  has over `:eval`,  is that it supports  a range
(`:h e132`).

## `:h optional-function-argument`

You can now set a default value to an argument passed to a function.

    function Something(a = 10, b = 20, c = 30)

---

It will be available in Nvim once the PR 10905 is merged.

---

I *think* you should refactor things like:

    fu Func(...)
        let foo = get(a:, '1', 12)
        let bar = get(a:, '2', 34)
        ...

Into:

    fu Func(foo = 12, bar = 34)
        ...

## `:h prompt-buffer` (Vim only)

##
# Review `https://arp242.net/vimlog/`

Check whether we've missed some interesting new feature in the recent past.

