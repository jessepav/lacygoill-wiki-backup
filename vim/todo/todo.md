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

##
# Document
## how to squash a non-focused window

    :3resize 0
     │
     └ window number 3

---

Do *not* try to use `win_execute()`; it doesn't work:

    vim -Nu NONE +'set wmh=0|sp|call win_execute(win_getid(2), "resize 0")'

Instead:

    vim -Nu NONE +'set wmh=0|sp|2resize 0'

<https://github.com/vim/vim/issues/5131#issuecomment-546715292>

## how Vim processes unknown commands, and known commands with wrong syntax

<https://github.com/neovim/neovim/issues/11136#issuecomment-537253732>

---

There may be other locations where we could have used a heredoc:

    :vim /[a-z](\[/gj ~/.vim/**/*.{snippets,vim} ~/.vim/template/** ~/.vim/vimrc
          ^^^^^^^^
          there may be other patterns to test

##
# Reference

[1]: https://en.wikipedia.org/wiki/Code_reuse

