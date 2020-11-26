# Refactoring
## When should we
### pass `W`, `c` or `z` to `search()`?

I think we definitely need to pass `c` in a while loop.
And if `search()` is passed `b`, I  think `W` should be passed too, even outside
a loop.
Otherwise, you're allowing Vim to wrap around  the end of the file, and it could
find sth *after* your current position, which may be unexpected.

I'm not sure for the rest of the time.
I  tend to  think that  `W` should  always be  passed, but  there may  be a  few
exceptions...

    :vim /\m\Csearch\%(pos\|pair\|pairpos\)\=(\%(.*W\)\@!)\@!/gj ~/.vim/**/*.{snippets,vim} ~/.vim/template/** ~/.vim/vimrc
    Cfilter! -other_plugins

As for `z`, does it improve the perf?
If so, should we have passed it to `search()` and `searchpos()` all the time?

---

Now that  I think  about it,  you probably don't  want `W`  if you're  writing a
motion which you want  to wrap around the end of the file,  like the default `n`
motion when `'wrapscan'` is set.

---

Mmm.
I thought that `b`  without `W` lead to unexpected results, but  I'm not so sure
anymore.
You may want  to look for sth backward,  but if that sth can't  be found before,
you may want  to look for it  after, and so let  Vim wrap around the  end of the
file...

Although, that seems theoretical.
In practice, I think using `W` with `b` will be fine.

---

If you do sth like this:

    call cursor(1, 1)
    call search(pat)

I would recommend to use `W`:

    call search(pat, 'W')

It's not needed but it explicits what is going to happen.
Either `search()` finds `pat`,  and it doesn't wrap around the  end of the file,
or it  does not find  `pat`, and again,  it doesn't wrap  around the end  of the
file.
In both cases, it won't wrap; `W` tells us that.

---

Make sure we have not used `W` when we should not have in the past.

    :vim /\m\Csearch\%(pos\|pair\|pairpos\)\=(\%(.*W\)\@=/gj ~/.vim/**/*.{snippets,vim} ~/.vim/template/** ~/.vim/vimrc
                                             │├─────────┘
                                             ││
                                             │└ there must be a W flag
                                             └ there must be an open parenthesis

---

I think that if you use `search()` to:

   - describe some text, you should use `W`

   - move the cursor, you should not use `W`

     With one exception: if your custom motion is a wrapper around a default motion, then
     respect its behavior.
     For example, `}` does not wrap, so if you customize it, it should still not wrap.

### use `mapnew()` instead of `map()` + `[deep]copy()`?

What is the most effective?

Make tests with huge nested lists/dictionaries.

##
## use <cmd> whenever possible

    \C\<\%(map(\@!\|nm\%[ap]\|vm\%[ap]\|xm\%[ap]\|smap\|om\%[ap]\|map!\|im\%[ap]\|lm\%[ap]\|cm\%[ap]\|tma\%[p]\|nore\%[map]\|nn\%[oremap]\|vn\%[oremap]\|xn\%[oremap]\|snor\%[emap]\|ono\%[remap]\|no\%[remap]!\|ino\%[remap]\|ln\%[oremap]\|cno\%[remap]\|tno\%[remap]\)\>\c\%(.*<cmd>\)\@!\%(.*\%(<expr>\|<c-\\>e\|:.*<cr>\)\)\@=

---

Note that:

   - you don't need `<silent>` when you use `<cmd>`

   - a prefix count is not translated into a range (e.g.: 3 → .,.+2); so no need of `<c-u>`
     (`:h N:`)

   - for a visual mapping, you might want to press `<esc>` before `<cmd>` so that the visual marks are set

   - for a visual mode mapping starting with `:`,
     the visual range is not automatically put at the start of the command

         xno <F3> :s/pat/rep/<cr>
         →
         xno <F3> <cmd>*s/pat/rep/<cr>
                       ^
                       necessary

   - you can't use `<cmd>` if the rhs contains keycodes such as `<c-r><c-w>`
     (because they are interpreted as plain, unmapped keys)
     note that, for some reason, `<cmd>` works fine with `<bar>` (and `<lt>`?)

---

Cannot use `setcmdpos()` with `<cmd>`.  To document.

    $ vim -Nu NONE -S <(cat <<'EOF'
        " ✔
        " nno <F3> :abCde<c-r>=setcmdpos(3)[-1]<cr>
        " ✘
        nno <F3> :abCde<cmd>call setcmdpos(3)<cr>
        call feedkeys("\<F3>")
    EOF
    )

Also, cannot use `<plug>` with `<cmd>`:
```vim
vim9script
nmap <plug>(test) :echom 'test'<cr>
nno <F3> <cmd>call feedkeys('<plug>(test)')<cr>
call feedkeys("\<F3>")
```
    E1137: <Cmd> mapping must not include <Plug> key

But it can be used if it's not directly in the rhs:
```vim
vim9script
nmap <plug>(test) :echom 'test'<cr>
nno <F3> <cmd>call Func()<cr>
def Func()
    call feedkeys("\<plug>(test)")
enddef
call feedkeys("\<F3>")
```
    test

To document.

---

Refactor our Vim notes to use `<cmd>` as much as possible.

---

Check whether we could remove some:

   - `<silent>`
   - `norm! gv`, `gv`

---

Try to  use `<c-\><c-n>`  in front of  `<cmd>` (in a  visual mapping)  only when
really  necessary.   You  don't  always  need it;  remember  that  you  can  use
`line('v')` and `line('.')` instead of `line("'<")` and `line("'>")`.

## replace 0 and 1 with v:false, v:true whenever possible

Pattern to look for:

    [(,]\s*[01]\s*[,)]`\@!

Or:

    \%(\%(^\s*["#]\|{{{\|}}}\).*\)\@<!\<[01]\>

Don't forget:

    :Cfilter! -other_plugins
    :Cfilter! -tmp

---

Also, try  to use `:h optional-function-argument`  to reduce noise; i.e.  it can
help you omit a boolean at various call sites.

##
# Document
## how to squash a non-focused window

    :3resize 0
     │
     └ window number 3

---

Do *not* try to use `win_execute()`; it doesn't work:

    $ vim -Nu NONE +'set wmh=0|sp|call win_getid(2)->win_execute("resize 0")'

Instead:

    $ vim -Nu NONE +'set wmh=0|sp|2resize 0'

<https://github.com/vim/vim/issues/5131#issuecomment-546715292>

## how Vim processes unknown commands, and known commands with wrong syntax

<https://github.com/neovim/neovim/issues/11136#issuecomment-537253732>

---

There may be other locations where we could have used a heredoc:

    :vim /[a-z](\[/gj ~/.vim/**/*.{snippets,vim} ~/.vim/template/** ~/.vim/vimrc
          ^------^
          there may be other patterns to test

##
# Reference

[1]: https://en.wikipedia.org/wiki/Code_reuse

