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

I would recomment to use `W`:

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

### use `g@[_l]` vs `norm! g@[_l]` vs `feedkeys('g@[_l]', 'n')`?

I think you should use `g@[_l]` by default.
And if you need to pass `v:count1` to the opfunc, use `:exe` + `:norm!`.

However, if  your opfunc invokes  an interactive command  (`z=`, `:s/pat/rep/c`,
`:let c =  getchar()`, ...), `:norm!` will type Escape,  because it considers an
interactive command as incomplete:

    " can't fix 'helzo' into 'hello'
    :new | pu='helzo' | setl spell | norm! z=

    " can't replace 'pat' with 'rep'
    :new | pu='pat' | exe "norm! :s/pat/rep/c\r"

    " can't get a character interactively
    :exe "norm! :let g:char = getchar()\r"
    :echo g:char
    27~
    ^^
    escape

From `:h :norm`:

>     {commands} should  be a complete command.   If {commands} does not  finish a
>     command, the last one will be aborted as if <Esc> or <C-C> was typed.

To avoid this pitfall, you need to press `g@[_l]` via `feedkeys()` instead of `:norm!`.

---

Note that for some reason, `:norm!` does not seem to consider `:call input()` as
incomplete:

    " you can type anything you want, as usual
    :exe "norm! :let g:input = input('')\r"

#### ?

Look for `feedkeys()` everywhere, and read surrounding comments.
Summarize them in our notes about mappings.

---

Example where the 't' flag is useful:

    $ vim -Nu NONE +'cno <c-q> <tab>'
    $ vim -Nu NONE +'cno <expr> <c-q> feedkeys("<tab>", "n")[-1]'
    " press ':', then 'C-q' repeatedly:  Vim inserts literal tab characters

                                                          v
    $ vim -Nu NONE +'cno <expr> <c-q> feedkeys("<tab>", "nt")[-1]'
    " press ':', then 'C-q' repeatedly:  Vim iterates over Ex commands

#### ?

Example where `g@l` causes an issue, and `norm! g@l` is needed:

    nno <buffer><nowait><silent> =rh :<c-u>call Func()<cr>g@l
    fu Func()
        set opfunc=MyOp
        let var = input('prompt: ')
        echom var
    endfu
    fu MyOp(_)
        norm! dd
    endfu

Other example:

    nno <silent> cr :<c-u>call <sid>get_transformation()
                    \<bar>set opfunc=<sid>coerce<bar>norm! g@l<cr>

Other example:
<https://github.com/lervag/vimtex/pull/1247>

Basically,  when `g@[_l]`  is  only preceded  by  `set opfunc=Func`,  everything
should work fine.

Otherwise, if `g@[_l]` is preceded by a function call (which sets 'opfunc'), and
invokes a function which consumes  user input (`input()`, `getchar()`, ...), the
latter may wrongly consume `g@[_l]`.
In that case, use `norm! g@[_l]`.

However, if  your opfunc also invokes  a function consuming user  input, `norm!`
won't work:

    ~/.vim/plugged/vim-par/plugin/par.vim:96

In that case, you need to use `feedkeys()`.

In the previous example (`vim-par`), we don't need `feedkeys()` because there is
a previous function call  which consumes user input (there is  none); we need it
because:

   - we need to use a count – so `g@l` can't be pressed directly
   - the opfunc consumes user input so `norm! g@l` can't be used

#### ?

Decide what we should write by default:

    g@l
    norm! g@l
    call feedkeys('g@l', 'n')

Review  all  locations where  we've  written  `norm! g@[_l]`, and  enforce  this
decision whenever possible.

Update: I think you should use `g@l` by default.
And if that doesn't work, then you should use `call feedkeys('g@l', 'n')`.

Why?
Because when your opfunc fails because of `norm! g@l`, it fails silently, which is bad.
It doesn't give you any info about where the issue comes from.
OTOH, with  `g@l`, if  there is  an issue, you'll  probably understand  where it
comes from (because `g@l` will be  consumed by an input function like `input()`,
or `getchar()`).

And with `feedkeys()`, there should never be an issue.

Refactor all  locations where you used  `norm! g@l`, and replace  it with `g@l`,
unless it breaks sth.

#### ?

Document that you should pass the `t` flag to `feedkeys()` only if it's needed.
It can create issues:

   - `feedkeys()` + `t` flag is not run when invoked from `:norm!`
   - during a recording, the `t` flag causes the fed key(s) to be recorded, which you don't want

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

