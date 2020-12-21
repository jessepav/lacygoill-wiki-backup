# Terminology
## What's a terminal key code?

A sequence of bytes emitted by the terminal when you press a given key on your keyboard.

For example, when you press `S-Tab`, xterm emits this sequence of 3 bytes:

    1b 5b 5a
    │  │  │
    │  │  └ Z
    │  └ [
    └ Esc

This is the key code for `S-Tab`.

See also: <https://vi.stackexchange.com/a/10284/17449>

## What's a Vim key code?

A notation to represent some special keys (or chords) on the keyboard.

Examples:

   - `<CR>`
   - `<Esc>`
   - `<Left>`
   - `<F1>`

See `:h keycode`.

## What's a mapped key sequence?

A sequence of keys and/or Vim key codes used as the lhs of a mapping.

Example:

    inoremap jk <Esc><cmd>nohl<CR>
             ^^
             this is a mapped key sequence

The term is used at `:h 'ttimeout'`.

Note that a mapped key sequence doesn't make sense outside of a mapping.
`jk` by itself is not a mapped key sequence.
It becomes one if it's used as the lhs of a mapping.

By contrast, `^[[Z` and `<S-Tab>` don't need any context.
They are terminal/Vim key codes by themselves.

##
# opfunc
## What's a “pseudo-operator”?

The term is not used in the help.  I use it to refer to an operator to which the
same text-object  is always  passed (typically  `l`).  Such  an operator  can be
useful to make a custom command repeatable.

Example:

    nno <expr> <c-b> Transpose()
    fu Transpose(...)
        if !a:0
            set opfunc=Transpose
            return 'g@l'
        endif
        norm! xp
    endfu

    " press:  C-b .
    " 'C-b' transposes 2 characters, and dot repeats the transposition

Here, the  sole purpose of the  opfunc is to  make `xp` repeatable with  the dot
command.

## When I implement a custom operator, I often hesitate between `g@_` and `g@l`.  Which one should I use?

Use `g@l` for a pseudo-operator; `g@_` otherwise.

---

If your custom operator is a pseudo one, and you implement it like this:

    nno <expr> <key> Op()

    fu Op(...)
        if !a:0
            let &opfunc = 'Op'
            return 'g@_'
                      ^
                      ✘
        endif
        ...
    endfu

The `_` motion will make the cursor jump at the beginning of the line, which you
probably don't want.  You can avoid the jump by replacing the motion `_` with `l`.

If your custom operator is *not* a pseudo operator, and you implement it like this:

    nno <expr> <key> Op()
    xno <expr> <key> Op()
    nno <expr> <key><key> Op() .. 'l'
                                   ^
                                   ✘

    fu Op(...)
        if !a:0
            let &opfunc = 'MyOP'
            return 'g@'
        endif
        ...
    endfu

The change marks will be wrongly set.

### Which pitfall should I be aware of about `g@l`?

Don't use it for a visual mode mapping.  For the latter, just use `g@`:

    nno <expr> <key> Op()
    xno <expr> <key> Op()
    fu Op(...)
        if !a:0
            let &opfunc = 'Op'
            return 'g@' .. (mode() is# 'n' ? 'l' : '')
            "              ^-------------------------^
        endif
        ...
    endfu

`g@` is enough to execute your operator in visual mode.
It doesn't expect a text-object (or a motion); the selection *is* the text-object.
So `l` would be useless; worse, it would make the cursor move.

##
## My opfunc substitutes text via `setline()`, not `:s`.  How to pass it a range when I use a count (e.g. `123g@_`)?

Move the code of your opfunc into another function.
Inside the opfunc, call this other  function by prefixing `:call` with the range
`'[,']`.

       opfunc = dispatch
       v-----v
    fu OpSetup(...)
        if !a:0
            let &opfunc = 'OpSetup'
            return 'g@'
        endif
        '[,']call Op()
        ^---^
    endfu

Example:

    $ vim -Nu NONE -S <(cat <<'EOF'
        nno <expr> <c-b>      OpSetup()
        nno <expr> <c-b><c-b> OpSetup() .. '_'

        fu OpSetup(...)
            if !a:0
                let &opfunc = 'OpSetup'
                return 'g@'
            endif
            '[,']call Op()
        endfu

        fu Op()
            call getline('.')->substitute('pat', 'rep', 'g')->setline('.')
        endfu
        let text =<< trim END
            " pat pat pat
            " foo foo foo
            " pat pat pat
            " foo foo foo
            " pat pat pat
        END
        sil pu!=text
        1
    EOF
    )

    " press:  3 C-b C-b
    " result:  'pat' is replaced on line 1 and 3

## My opfunc executes several `:echo`.  Only the last message is printed!

I  guess the  other messages  are cleared  because Vim  has redrawn  the screen;
similar to what this comment explains:

   > The messages are actually output, but the screen is redrawn right away
   > afterwards.  Try adding a sleep after the messages.

<https://github.com/vim/vim/issues/3960#issuecomment-463769646>

I don't know any solution to this  issue, other than printing your messages from
another function invoked before/after your opfunc, but not directly from it:

    nno <expr> <c-b> Func()
    fu Func(...)
        if !a:0
            let &opfunc = 'Func'
            return 'g@_'
        endif
        call FuncA()
    endfu
    fu FuncA()
        echom 'foo'
        echom 'bar'
    endfu
    " ✘
    " press:  C-b
    " bar~

    nno <c-b> <cmd>set opfunc=Func<bar>exe 'norm! g@_'<bar>call FuncA()<cr>
    fu Func(_)
    endfu
    fu FuncA() abort
        echom 'foo'
        echom 'bar'
    endfu
    " ✔
    " press:  C-b
    " foo~
    " bar~

---

Note that the same issue exists for autocmds:

    augroup test_echo | au!
        au CursorHold * ++once call Func() | au! test_echo
    augroup END
    fu Func()
        echom 'foo'
        echom 'bar'
    endfu

And for timers:

    " ✔
    :echom 'foo' | echom 'bar'
    foo~
    bar~

    " ✘
    :call timer_start(0, {-> execute('echom "foo" | echom "bar"', '')})
    bar~

   > Not sure if you really want to do this, the user may be doing something
   > that should not be interrupted by a list of messages. The callback
   > functions are not really intended to output a list of messages, that
   > would mess up the screen.

Source: <https://github.com/vim/vim/issues/836#issuecomment-221404233>

##
# feedkeys()
## When is it useful to use the `t` flag?

When a key doesn't behave exactly as expected.

For example, witouth `t`, `Tab` and  `S-Tab` don't interact with the wildmenu in
command-line mode (open it or cycle to the next/previous entry):

    $ vim -Nu NONE +'cno <c-q> <cmd>call feedkeys("<tab>", "n")<cr>'
    " press ':', then 'C-q' repeatedly:  Vim inserts literal tab characters

                                                             v
    $ vim -Nu NONE +'cno <c-q> <cmd>call feedkeys("<tab>", "nt")<cr>'
    " press ':', then 'C-q' repeatedly:  Vim iterates over Ex commands

And without  `t`, `u` doesn't automatically  open the fold where  the change was
performed:

    $ vim -Nu NONE +"set fdm=marker | pu!=['fold {{{1', 'some text', 'some text']"
    " press:  zRGdk
    :call feedkeys('u', 't')
                         ^
    " without the 't' flag, 'u' would not have opened the fold

### And when should I avoid it?

When a recording is being performed.
Indeed, during a recording,  the `t` flag causes the fed  key(s) to be recorded,
which you probably don't want.

MWE:

    ✘
    $ vim -Nu NONE +'nno <expr> <c-b> feedkeys("ix<esc>", "int")[-1]'
    " press:  qq
    "         C-b
    "         q
    "         @q
    " resulting line:  xxx
    " expected line:   xx

    ✔
    $ vim -Nu NONE +'nno <expr> <c-b> feedkeys("ix<esc>", "in" .. (reg_recording()->empty() ? "t" : ""))[-1]'
                                                                   ^---------------------------------^

---

Also, don't use the `t` flag if `feedkeys()` can be invoked from `:norm` (unless
you also use the `x` flag).

Indeed, `feedkeys()` + `t` flag has no effect when invoked from `:norm`.

MWE:

    $ vim -Nu NONE +'nno cd <cmd>exe "norm! :call feedkeys(\"aaa\",\"t\")\r"<cr>'
    " press 'cd': nothing is inserted in the buffer

    $ vim -Nu NONE +'nno cd <cmd>exe "norm! :call feedkeys(\"aaa\")\r"<cr>'
    " press 'cd': 'aa' is inserted in the buffer

This is  a contrived example, but  the issue can  be encountered in a  real life
scenario.  For example, in the past, we had these mappings:

    " ~/.vim/plugged/vim-help/after/ftplugin/help.vim
    nno <buffer><nowait> q <cmd>norm 1<space>q<cr>

    " ~/.vim/plugged/vim-window/plugin/window.vim
    nno <unique> <space>q <cmd>call lg#window#quit()<cr>

and this function:

    fu window#quit#main() abort
        ...
        if reg_recording() != ''
            return feedkeys('q', 'nt')[-1]
                                   ^
                                   ✘
        endif
        ...

If a register is being recorded, and we're in a help buffer, pressing `q` should
end the recording; in practice, it didn't because of the `t` flag.

---

Note that you really need `:norm` to reproduce this last issue.
For example, if you try to replace `:norm` with a second `feedkeys()`, the issue
disappears (no matter whether you use the `t` flag in any function call):

    nno cd <cmd>call feedkeys('gh', 't')<cr>
    nno gh <cmd>call feedkeys('aaa', 'nt')<cr>
    " press `cd`: 'aa' is inserted

Also, the issue disappears if you use the `x` flag:

                                                                      v
    $ vim -Nu NONE +'nno cd <cmd>exe "norm! :call feedkeys(\"aaa\",\"tx\")\r"<cr>'
    " press 'cd': 'aa' is inserted in the buffer

##
## Why should I use the `i` flag as often as possible?

To make the replay of a macro more reliable.

    $ vim -Nu NONE -i NONE +"let &wcm = &wc | pu!='xxx'" +'cno <expr> <s-tab> feedkeys("<s-tab>", "n")[-1]'
    " press:  qq
              : Tab Tab Tab S-Tab Enter
              q
              @q
    E33: No previous substitute regular expression~
    " '@q' should have executed ':#'; instead it has executed ':&'

When you replay the macro, here's what happens:

    typeahead       | executed
    --------------------------
    @q              |
    :^I^I^I<80>kB^M |
     ^I^I^I<80>kB^M | :
       ^I^I<80>kB^M | :^I
         ^I<80>kB^M | :^I^I
           <80>kB^M | :^I^I^I
           ^----^
           Vim's internal encoding of 'S-Tab'

At that point, `S-Tab` is remapped into nothing (empty string).
But during  the evaluation of  the mapping's  rhs, `feedkeys()` is  invoked, and
*appends* a new `S-Tab` in the typeahead, which gives:

    typeahead       | executed
    --------------------------
           ^M<80>kB | :^I^I^I
             <80>kB | :^I^I^I^M
                    | :^I^I^I^M<80>kB

As you can see, without the `i` flag, `S-Tab` is appended, which means that it's
executed *after* whatever Ex command is currently selected in the wildmenu.
IOW, it's executed too late, and has  no effect (unless you've mapped `S-Tab` in
normal mode); it should  have made Vim select `:#` (which  is the previous entry
before `:&`).

Similar issue: <https://github.com/tpope/vim-repeat/issues/23>

Btw, @chrisbra has the same opinion:

   > After thinking a bit more, I think,  when the keys have not been typed, they
   > should **always** be inserted at the current position.

Source: <https://github.com/vim/vim/issues/212#issuecomment-132351526>

### And when should I avoid it?

When you want to delay the execution  of the key sequence until Vim has entirely
finished processing a mapping or an abbreviation.
This is typically  the case when the  purpose of `feedkeys()` is  not to emulate
some interactive key press, but to postpone some arbitrary code.

Example:
<https://gist.github.com/lacygoill/88437bcbbe90d1d2e2787695e1c1c6a9#reminder>
Here, passing the `i` flag to `feedkeys()` would break the code.

Before timers were added to Vim, `feedkeys()`  was a good way to emulate a timer
with  a  0ms  waiting time  (or  to  emulate  a  one-shot autocmd  listening  to
`SafeState`):

    fu Func()
        echom 'start of Func'
        call timer_start(0, {-> execute('echom "delayed after Func"', '')})
        echom 'end of Func'
    endfu
    :call Func()
    :mess
    start of Func~
    end of Func~
    delayed after Func~

    ⇔

    fu Func()
        echom 'start of Func'
        nno <plug>(func) <cmd>echom 'delayed after Func'<cr>
        call feedkeys("\<plug>(func)")
        echom 'end of Func'
    endfu
    :call Func()
    :mess
    start of Func~
    end of Func~
    delayed after Func~

It worked with or without the `i` flag.
But the `i` flag was undesirable when the typeahead was not empty:

                                                                        ✘
                                                                        v
    nno cd :echom 'start rhs' \| call feedkeys("\<plug>(not_delayed)", 'i')<cr><cmd>echom 'end rhs'<cr>
    nno <plug>(not_delayed) <cmd>echom 'not delayed'<cr>

    " press 'cd'
    :mess
    start rhs~
    not delayed~
    end rhs~

##
## comparison with `:norm`
### Does `:norm` append or insert keys in the typeahead?

It always inserts keys:

    $ vim -Nu NONE <(cat <<'EOF'
        " a
        " b
        " c
        " some folded text {{{
        " some folded text
        " some folded text }}}
    EOF
    ) +'set fdm=marker noro' +1d +'$'
    :call feedkeys('3gsu', 'n') | norm! zv

Notice how the fold is immediately opened, but the undo command is not run before 3s.
That's because Vim has executed the keys in this order:

    zv3gsu
    ^^
    inserted; not appended

In contrast, `feedkeys()` only inserts keys if you pass it the `i` flag.

### Are the keys typed by `:norm` executed immediately?

Yes:

    $ vim -es -Nu NONE -i NONE +"pu='some text'" \
      +'set vbs=1 | echo b:changedtick | exe "norm! dd" | echo b:changedtick | qa!'
                                         ^------------^
    3~
    4~

In contrast, `feedkeys()` executes the keys immediately only if you pass it the `x` flag:

    $ vim -es -Nu NONE -i NONE +"pu='some text'" \
      +'set vbs=1 | echo b:changedtick | call feedkeys("dd", "n") | echo b:changedtick | qa!'
                                         ^----------------------^
    3~
    3~

    $ vim -es -Nu NONE -i NONE +"pu='some text'" \
      +'set vbs=1 | echo b:changedtick | call feedkeys("dd", "nx") | echo "\n" .. b:changedtick | qa!'
                                         ^-----------------------^
    3~
    4~

##
# `maparg()`
## How to represent the mode 'nvo' in the input of `maparg()`?

Use an empty string:

    $ vim -Nu NONE +'noremap <c-e> <cmd>echom "test"<cr>'
    :echo maparg('<c-e>', '')
                          ^^

### How does `maparg()` represent `nvo` when its output is a dictionary?

With a space:

    $ vim -Nu NONE +'noremap <c-e> <cmd>echom "test"<cr>'
    :echo maparg('<c-e>', '', 0, 1).mode is# ' '
                                              ^

##
## How to represent the operator-pending mode in the input of `maparg()`?

Use 'o':

    $ vim -Nu NONE +'ono <c-e> <cmd>echom "test"<cr>'
    :echo maparg('<c-e>', 'o')
                          ^-^

### How does `mode()` represent the operator-pending mode in its output?

With 'n':

    ono <c-e> <cmd>call Func()<cr>
    fu Func()
        echom mode()
    endfu

    " press:  y C-e
    " 'n' is printed

Which is the same as for normal mode.
IOW, `mode()`  is useless to detect  operator-pending mode; you need  to pass it
the optional argument `1` for its output to be reliable.

#### What if I pass the optional argument `1`?

Then, `mode(1)` evaluates to 'no', or 'nov', or 'noV' or 'no^V'.

    ono <c-e> <cmd>call Func()<cr>
    fu Func()
        echom mode(1)
    endfu

    " press y C-e: no
    " press y v C-e: nov
    " press y V C-e: noV
    " press y C-v C-e: no^V

##
## I'm saving information about this mapping:

    nno <m-b> <cmd>call <sid>func()<cr>
    fu s:func()
        echo 'mapping is working'
    endfu
    let save = maparg('<m-b>', 'n', 0, 1)

### What's wrong with the code?  (2)

The `lhs` key is translated:

    echo save.lhs
    â~

This doesn't prevent you from saving/restoring a mapping:

    nno <m-b> <cmd>echo 'm-b'<cr>
    let save = maparg('<m-b>', 'n', 0, 1)
    nunmap <m-b>
    exe 'nno ' .. save.lhs .. ' ' .. save.rhs

    nno <m-b>
    No mapping found~

    " press M-b: 'm-b' is displayed

But as you  can see, after the restoration,  you can't refer to it  via the same
notation in a `:map` command, which is unexpected.

---

Pseudo-keys (like `<sid>`) are *not* translated in the `rhs` key:

    echo save.rhs
    :call <sid>func()<cr>~

When you  later try to  restore the mapping, `<sid>`  will be translated  in the
context of the current script, which  will probably be different than the script
where `s:func()` was originally defined; IOW, the translation will be wrong.

---

All  the other  keys should  not cause  any issue;  they are  either numbers  or
boolean flags, so there's nothing to translate.

### How to fix it?

    nno <m-b> <cmd>call <sid>func()<cr>
    fu s:func()
        echo 'mapping is working'
    endfu

    v------------------------------------------------------------------v
    let fix = {'lhs': '<m-b>', 'rhs': maparg('<m-b>', 'n')->escape('|')}
    let save = maparg('<m-b>', 'n', 0, 1)->extend(fix)
                                           ^----^ ^-^

Note that  the fix relies  on the fact  that `maparg()`, *without*  the `{dict}`
argument, *does* translate pseudo-keys.
But after `maparg()`  translates `<bar>` into a literal bar,  you need to escape
it to prevent it from terminating a mapping command (hence the `escape()`).

##
## What is a pseudo-mode?

The term is not used in the official  documentation, but we use it to refer to a
collection of  modes which can appear  for a single  mapping in the output  of a
`:map` command  (or a  similar command  for other  modes), or  in the  output of
`maparg()`.

A pseudo-mode is not  a real mode, because you can't be in  several modes at the
same time.

---

For  example, `:map`  and `maparg()`  use a  space to  describe the  pseudo-mode
matching normal mode, visual/select mode, and operator-pending mode:

    noremap <c-q> <esc>
    map <c-q>
       <C-Q>       * <Esc>~
    ^
    echo maparg('<c-q>', '', 0, 1).mode is# ' '
    1~

Similarly, `:map!` and  `maparg()` use `!` to describe  the pseudo-mode matching
insert mode and command-line mode:

    noremap! <c-q> <esc>
    imap <c-q>
    !  <C-Q>       * <Esc>~
    echo maparg('<c-q>', 'i', 0, 1).mode
    !~

And `:vmap` and  `maparg()` use `v` to describe the  pseudo-mode matching visual
and select mode:

    vnoremap <c-q> <esc>
    vmap <c-q>
    v  <C-Q>       * <Esc>~
    echo maparg('<c-q>', 'i', 0, 1).mode
    v~

### In the next snippet, what is the pseudo-mode in the output of `:map` and `maparg()`?

    noremap <c-q> <esc>
    nunmap <c-q>

    map <c-q>
↣
    ov <C-Q>       * <Esc>~
    ^^
↢

    echo maparg('<c-q>', '', 0, 1).mode
↣
    ov~
↢

#### Explain the result.

When a mapping  is installed in a  pseudo-mode, then removed in one  of the real
modes  contained in  this pseudo-mode,  `:map`  and `maparg()`  don't break  the
mapping into several (one for each remaining mode).

---

This  creates another  category  of pseudo-modes  in which  a  mapping can't  be
installed via a single mapping command (you always need an extra `:unmap` command):

    sil! unmap <c-q>
    map <c-q> <nop>
    nunmap <c-q>
    map <c-q>
    ov <C-Q>         <Esc>~
    ^^

    sil! unmap <c-q>
    map <c-q> <nop>
    vunmap <c-q>
    map <c-q>
    no <C-Q>         <Esc>~
    ^^

    sil! unmap <c-q>
    map <c-q> <nop>
    ounmap <c-q>
    map <c-q>
    nv <C-Q>         <Esc>~
    ^^

    sil! unmap <c-q>
    map <c-q> <nop>
    xunmap <c-q>
    map <c-q>
    nos<C-Q>         <Esc>~
    ^-^

    sil! unmap <c-q>
    map <c-q> <nop>
    sunmap <c-q>
    map <c-q>
    nox<C-Q>         <Esc>~
    ^-^

### What about this snippet?

    noremap <c-q> <esc>
    nunmap <c-q>
    nnoremap <c-q> <esc>

    map <c-q>
↣
    n  <C-Q>       * <Esc>~
    ov <C-Q>       * <Esc>~
↢

    echo maparg('<c-q>', '', 0, 1).mode
↣
    n~
↢

#### Explain the result.

When you re-install the exact same mapping, Vim does not merge back the mappings
into a single one (using a "bigger" pseudo-mode).

### What about this one?

    sil! unmap <c-q>
    nnoremap <c-q> <esc>
    xnoremap <c-q> <esc><esc>
    snoremap <c-q> <esc><esc><esc>
    onoremap <c-q> <esc><esc><esc><esc>

    echo maparg('<c-q>', '')
↣
    <Esc><Esc><Esc><Esc>~
↢

#### Explain the result.

If:

   - you ask for info about a mapping in the pseudo-mode `''` (aka `nvo`)
   - there is no mapping in this pseudo-mode
   - but there *is* a mapping in `n`, `x`, `s`, or `o` mode

then `maparg()` outputs the mapping which was installed last.

##
# Tests
## My plugin needs to install a mapping on `abc`.
### How to check whether it will cause a timeout for some other mapping?

    if mapcheck('abc', 'n')->empty()
        " can install mapping on `abc`
    endif

`mapcheck()` returns an empty string iff none of these statements is true:

   - `abc` matches at the start of the lhs of an existing mapping
   - the lhs of an existing mapping matches at the start of `abc`

If the user has a mapping on `ab`, the new mapping on `abc` will cause a timeout for the latter.
If the user has a mapping on `abcd`, it will cause a timeout for the new mapping on `abc`.

In the first case, `mapcheck('abc')` will return the rhs of the `ab` mapping.
In the second case, `mapcheck('abc')` will return the rhs of the `abcd` mapping.

### How to check whether `abc` is already mapped?

    if maparg('abc', 'n')->empty()
        " `abc` is not mapped
    endif

##
## My plugin provides some feature via a `<plug>` mapping.
### How to check whether the user has already mapped a key sequence to this `<plug>`?

    if !hasmapto('<plug>(abc)', 'n')
        " no mapping is currently mapped to `<plug>(abc)`
    endif

Actually, `hasmapto()`  returns 1 iff  `<plug>(abc)` is contained  *anywhere* in
the rhs of a mapping.  It doesn't need to be *exactly* the rhs of a mapping.

Example:

    nno <plug>(abc) <cmd>echo 'some feature'<cr>
    nmap cd "_yy<plug>(abc)"_yy
    echo hasmapto('<plug>(abc)', 'n')
    1~

##
# repetition
## One of my custom normal command is not repeatable with the dot command!  Why?

`.` only repeats the *last* default normal command.
So, if your  custom command executes several commands, `.`  will only repeat the
last one instead of the whole sequence.

## What do I need to do to make a custom operator repeatable with `.`?

Nothing.
There's no need to use `repeat#set()` or any other hack.

---

No matter how you implement your custom  operator, in the end, it executes `g@`,
which is  a builtin  Vim command.  `.` repeats the  last Vim  command, including
`g@`.

Note that `.` also repeats the motion or a text-object which you provided to the
operator.

## Do I have the guarantee that `.` will repeat my custom opfunc with the same count/register?

Yes.

    nno <expr> <c-b> Op()
    fu Op(...)
        if !a:0
            set opfunc=Op
            return 'g@'
        endif
        echom 'the count is ' .. v:count
        echom 'the register is ' .. v:register
        norm! "b4yl
    endfu

    " press:  "a 3 C-b l
    " press:  .
    :mess
    the count is 3~
    the register is a~
    the count is 3~
    the register is a~

Notice how `"b4yl` did not reset the count  to 4, nor the register to `"b`, when
the dot command was executed.

`v:count` and `v:register` are temporary variables;  as soon as the operator has
been executed, they are reset to resp. 0 and `"`.
But Vim remembers the last count/register which was passed to the operator.
See `:h .`:

   > Without a count, the count of the last change is used.

## After executing an operator from visual mode, on what text does `.` operate?

Briefly put, on a region of text which starts from the cursor position and which
has the same geometry as the previous selection.

For more detail, see `:h visual-repeat`.

##
## My custom operator works.  But when I press `.`, it's not repeated!  Why?

If the  function implementing  your operator calls  another operator  during its
execution, `.` will repeat the latter.

Example:

    nno <expr> \d <sid>duplicate_and_comment()

    fu s:duplicate_and_comment(...)
        if !a:0
            let &opfunc = expand('<sfile>')->matchstr('<SNR>\w*$')
            return 'g@'
        endif
        norm! '[y']

        " ✘
        " norm gc']
        " ✔
        ']Commentary

        norm! ']p
    endfu

Here, the normal command:

    norm gc']

... would cause an issue, because it invokes the operator `gc`.
So, after  pressing `\dip`  (duplicate and comment  inside paragraph),  `.` will
repeat `gc']` instead of `\dip`.

### How to fix it?

1) Restore `'opfunc'` correctly.

2) Or better, don't use a a second operator B inside an operator A:
   call the function implementing B via an Ex command.

In the previous example, we use `:CommentToggle`.

Using an Ex  command is better, because resetting `'opfunc'`  inside an operator
function feels clumsy.
Besides, it creates a bad repetition (DRY,  DIE): if one day you change the name
of your operator function, you'll also need to remember to change it on the line
where you restore `'opfunc'`.

##
## vim-repeat
### How to make a mapping repeatable with `repeat#set()`?

    nno {lhs} {rhs}:call repeat#set('{lhs}')<cr>

Or:

    nmap          {lhs}                  <plug>(named_mapping)
    nno <silent>  <plug>(named_mapping)  {rhs}:call repeat#set('<plug>(named_mapping)')<cr>

Or:

    nmap  {lhs}                  <plug>(named_mapping)
    nno   <plug>(named_mapping)  <cmd>call Func()<cr>

    fu Func()
        ...
        sil! call repeat#set("\<plug>(named_mapping)")
        "  ^
        " Sometimes, you may not have the plugin, or it may be temporarily disabled.
        " In this case, the function won't exist.
    endfu

#### My mapping is in visual mode, not normal mode!  How to adapt the code?

If you don't use a `<plug>` mapping, just replace `:nno` with `:xno`.

Otherwise, replace:

   - `:nmap` with `:xmap`
   - `:nno` with `:noremap`

##### Which pitfalls should I avoid?  (2)

Don't use `:xno` in for your `<plug>` mapping, use `:noremap` instead.

Rationale: `repeat.vim` remaps the dot command,  to make it type the contents of
some variables updated via some autocmds; but only in normal mode, not in visual
mode.

As a result, your 2nd `<plug>` needs to support both modes:

   - visual when you'll press the lhs initially
   - normal when you'll press `.`

---

Don't  reselect  the visual  selection  with  `gv` at  the  end  of your  custom
commands.  Otherwise,  before being able to  press `.`, you would  need to press
`Escape` to get back to normal mode.

###
### I want `.` to repeat my commands with the same count I used initially!  How to do it?

`repeat#set()` accepts a 2nd optional argument.
Use it to pass `v:count`.

##
# pager
## What's the difference between the hit-enter prompt and the more prompt?

When you run a  command with a long output (more lines than  what the screen can
display), you're initially at the more prompt:

    -- More --

If you  scroll downward, eventually  you reach the last  line of the  output; at
that moment you're at the hit-enter prompt:

    Press ENTER or type command to continue

### In a script, how can I determine whether I'm at one or at the other?

Try to inspect the output of `mode(1)`.
If it's `r`, you're at the hit-enter prompt.
If it's `rm`, you're at the more prompt.

##
## I've included `mode()` in my status line.  It returns `n` even when I'm at the hit-enter prompt!

Theory: The  status line  is  not  updated on  the  command-line,  nor when  the
hit-enter prompt is visible:

    $ vim -Nu NONE +'set ls=2 stl=%{mode(1)}'
    :echo "a\nb"
    " the status line contains 'n' while you're typing the command (not 'c')
    " the status line still contains 'n' after you've run the command and the pager is open

    $ vim -Nu NONE -S <(cat <<'EOF'
        set ls=2 stl=%{Stl()}
        fu Stl()
            let mode = mode(1)
            let g:modes = get(g:, 'mode', []) + [mode]
            return mode
        endfu
    EOF
    )
    :echo "a\nb"
    " wait for a minute
    :echo g:modes
    " the list should contain a lot of items; it only contains a few

##
## When can I map a key while Vim's pager is open?

Only when you're  at the hit-enter prompt;  not when you're at  the more prompt.
That's because at the latter, mappings are ignored.  From `:h pager`:

   > Note: The typed key is directly obtained from the terminal, it is not mapped
   > and typeahead is ignored.

## I'm trying to install a mapping triggered when I'm at the hit-enter prompt.

    nno <c-b> <cmd>call Func()<cr>
    fu Func()
        if mode(1) is# 'r'
            echom 'I''m at the hit-enter prompt'
        endif
    endfu

    :ls
    " press:  C-b
    :mess
    " result:   no message has been logged
    " expected: "I'm at the hit-enter prompt" has been logged

### Why does it not work?

When you press `C-b`, `mode(1)` returns `n` while you would expect `r`.

No matter the key you press, the hit-enter prompt is closed immediately:

    $ vim -Nu NONE +'nno x <nop>' +"pu='ccc'" +'echo "a\nb"'
    " press:  x
    " result: the hit-enter prompt is closed, even though 'x' had no effect because it was a no-op

And  *maybe* mappings  are  processed right  afterward; but  it's  too late  for
`mode()`  to return  `r`; now,  it can  only return  `n`, because  the hit-enter
prompt is no longer visible and you're really in the regular normal mode.

#### Ok, is there a workaround?

You can't test whether  the pager is open when you press your  key.  But you can
test it before.  Indeed,  for the pager to be opened, an Ex  command needs to be
run, so you know that `CmdlineLeave` is always fired right before.

    let s:is_pager_open = v:false
    au CmdlineLeave : call timer_start(0, {-> mode() is# 'r' && SetFlag()})
    fu SetFlag()
        let s:is_pager_open = v:true
        au SafeState * ++once let s:is_pager_open = v:false
    endfu
    nno <c-b> <cmd>eval {-> C_b()}()<cr>
    fu C_b()
        if s:is_pager_open
            echom "C-b has been pressed while the pager was open"
        endif
    endfu

    " press C-b:  nothing happens
    :ls
    " press C-b:  the message is printed on the command-line

---

It seems that  `<expr>` is not necessary  here, but it makes the  code easier to
understand and possibly more reliable.  If you wrote this instead:

    nno <c-b> <cmd>call C_b()<cr>

When pressing `C-b`, you would enter and leave the command-line which would fire
`CmdlineLeave`  a second  time.   Then  you have  to  wonder,  when this  second
`CmdlineLeave` is fired, is the pager still open?
It looks like  it is, but it  must be for a  short period of time,  and it's not
obvious why:

    $ vim -Nu NONE
    :ls
    :call reltime()
    " the pager is closed as soon as Enter is pressed

In any  case, with `<expr>`, there's  no such question; the  command-line is not
entered nor leaved.

---

Do *not* pass a `1` argument to `mode()`:

    au CmdlineLeave : call timer_start(0, {-> mode(1) is# 'r' && SetFlag()})
                                                   ^
                                                   ✘

When you've run a command with an output longer than the current visible screen,
and `-- more --` is printed at the bottom, `mode(1)` is `rm`, *not* `r`.
As a result, if  you wrote `mode(1)`, your flag would not  be set correctly when
the pager has many lines to display.

##
## Why does `q` start a recording when it's pressed at the hit-enter prompt, but not at the more prompt?

At the more-prompt, only a small number of commands are valid.
From `:h pager /other`:

   > Any other key causes the meaning of the keys to be displayed.

`q` is one of them; it stops the listing:

   > q, <Esc> or CTRL-C                    stop the listing

OTOH, at the hit-enter prompt, `q` gets back its default meaning (i.e. start/end
a recording):

   > -> Press ':' or any other Normal mode command character to start that command.

As a workaround, you could try [this code][1].

##
# Tricks
## How to tweak the behavior of a builtin operator?

Create a wrapper around it.

Example with the `gq` operator:

    nno <expr> gq  <sid>gq()
    nno <expr> gqq <sid>gq() .. '_'
    xno <expr> gq  <sid>gq()

    fu s:gq(...)
        if !a:0
            let &opfunc = expand('<sfile>')->matchstr('<SNR>\w*$')
        endif
        " tweak some setting which alters the behavior of `gq`
        ...
        " execute the default `gq`
        norm! '[gq']
    endfu

##
## I have a simple mapping whose rhs is just a sequence of normal commands.

Example:

    nno cd xlx

### How to make a count repeat the whole sequence, and not just the first normal command?  (2)

Use the `<expr>` argument:

    nno <expr> cd "\e" .. repeat('xlx', v:count1)
        ^----^     ^^                   ^------^

Note that the escape is only needed to cancel a possible count.
Basically,  it tells  Vim: "forget  the  first count,  I need  to reposition  it
elsewhere in my command".

You can test the mapping against this line:

    abcdefg
    ^
    cursor here

`2cd` should get you:

    beg

Which is the result of `xlxxlx`, meaning that the count was correctly applied to
the whole sequence  `xlx`, and not just  the first `x` (in which  case Vim would
have just run `2xlx`).

---

Or execute the commands via `@=`:

    nno <silent> cd @='xlx'<cr>

##
## How to create my own pseudo-leader key?

    " define `<plug>(myLeader)` as a pseudo-leader key
    nmap <space> <plug>(myLeader)

    " make sure it doesn't have any effect if you don't press any key after the leader until the timeout,
    " just like the regular leader key does
    nno <plug>(myLeader) <nop>

    " you can use your leader key
    nno <plug>(myLeader)a <cmd>echo 'foo'<cr>
    nno <plug>(myLeader)b <cmd>echo 'bar'<cr>
    nno <plug>(myLeader)c <cmd>echo 'baz'<cr>
    ...

<http://vi.stackexchange.com/a/9711/6960>

### What's one pitfall of this trick?

`<plug>(myLeader)a` fails to override a mapping whose lhs is `<space>a`:

    nno <space>a <cmd>echo 'original'<cr>

    nmap <space> <plug>(myLeader)
    nno <plug>(myLeader) <nop>
    nno <plug>(myLeader)a <cmd>echo 'redefined'<cr>

In contrast, `<leader>a` would succeed:

    let mapleader = ' '
    nno <space>a <cmd>echo 'original'<cr>
    nno <leader>a <cmd>echo 'overridden'<cr>

### When is it useful?

I guess it's  only useful when you write  a plugin and want to  provide a leader
key to your users.  Although, even then, because of the pitfall, you'll probably
want to write sth like this instead:

    let leader = get(g:, 'user_leader', '<space>')
    for [lhs, rhs] in [['a', ':echo "foo"<cr>'], ['b', ':echo "bar"<cr>'], ['c', ':echo "baz"<cr>']]
        exe 'nno ' .. leader .. lhs .. ' ' .. rhs
    endfor

##
# Miscellaneous
## What are 3 benefits of the pseudo-key `<cmd>`?

It does not trigger `CmdlineEnter` nor `CmdlineLeave`.

---

It makes  a mapping silent, without  having to use `<silent>`;  the latter comes
with its own pitfalls.

---

You don't need `<c-u>` at the start of a command-line anymore (`:h N:`).
That's because  `<cmd>` prevents Vim  from automatically inserting a  range when
entering  the  command-line; usually,  that  happens  when the  command-line  is
entered from visual  mode (`:'<,'>`), or a count was  pressed (`:.,.+123`) right
before.

Note that  as a consequence, in  a visual mapping,  you might need to  write the
visual range explicitly:

    " before
    xno <F3> :s/pat/rep/<cr>

    " after
    xno <F3> <cmd>*s/pat/rep/<cr>
    "             ^
    "             necessary

## Between `<cmd>` and the next mandatory `<cr>`, which keycodes
### lose their special meaning?

Any keycode whose  purpose is to interact with the  command-line in some special
way (i.e. other than just inserting a character).
For  example,  `<c-r>=` (evaluate  expression  and  insert result),  or  `<c-w>`
(delete previous word).

That's because they are interpreted as plain, unmapped keys.
This is documented at `:h <cmd>`:

   > no user interaction is expected.

---

Exception:

`<C-v>` keeps its special meaning (`:h c^v`).
```vim
nno <F3> <cmd>echo '<c-v>'<cr>
call feedkeys("\<F3>")
```
    nothing is echo'ed
```vim
nno <F3> <cmd>echo '<c-v><c-v>'<cr>
call feedkeys("\<F3>")
```
    ^V
```vim
### are disallowed?

Most keycodes which don't have a glyph:

   - function keys
   - arrow keys
   - `<plug>`
   ...

Presumably because they're meant to interact with Vim which is not expected.

Exception: keycodes using the control or meta modifiers.

#### What if I still want to write one of them between `<cmd>` and `<cr>`?

Delay its translation with `<lt>`:
```vim
" ✘
norm! o
nno <F3> <cmd>call feedkeys("atest\<up>")<cr>
call feedkeys("\<F3>")
```
    E1137: <Cmd> mapping must not include <Up> key
```vim
" ✔
norm! o
nno <F3> <cmd>call feedkeys("atest\<lt>up>")<cr>
call feedkeys("\<F3>")
```
    'test' is inserted, and the cursor is moved 1 line up

This works because the limitation only exists when the mapping is being read.
Not afterward, when it's being typed.

---

Alternatively, for some keycodes, you might use another notation.
For example, in a double-quoted string, `\<esc>` can be replaced with `\e`.
The latter notation is also able to work around the limitation.

##
## What's the exact effect of `set <M-d>=^[d`?

It changes  how the  keys in the  typeahead buffer are  processed; it  makes Vim
translate the sequence `Esc` + `d` into `<M-d>`.

This is confirmed by the output of `set termcap`:

    <ä>        ^[d~
     ^
     notice how Vim does not write <M-d>

---

But it does *not* change the way Vim encodes `<M-d>` internally:

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        exe "set <m-d>=\ed"
        nno <esc>d dd
        0pu=['a', 'b', 'c']
        2
        call feedkeys("\<m-d>", 'x')
        %p
        qa!
    EOF
    )
    a~
    b~
    c~

Here, you may have thought that  `feedkeys()` would have written `<esc>d` in the
typeahead buffer because of `set <m-d>=^[d`,  and as a result, the mapping would
have deleted the text line `b`.

However, that's not what happens.
Vim still encodes `<M-d>` like `ä`;  so `feedkeys()` writes `ä` in the typeahead
buffer, *not* `esc` + `d`, and thus the mapping is not used.

Conclusion: it  does not work in  both ways; after running  this `:set` command,
`<M-d>` and `^[d` are not equivalent.

    ✔
    esc + d ⇒ M-d

    ✘
    M-d ⇒ esc + d

## What happens if I use the same key sequence to define several terminal keys?

Vim uses the first one in its internal termcap db (`:set termcap`).
What matters is the  order of the keys in the db; not  the order in which you've
run your `:set <...>` commands.

    exe "set <F10>=\ed"
    nno <F10> <cmd>echo 'F10 was pressed'<cr>
    exe "set <F5>=\ed"
    nno <F5> <cmd>echo 'F5 was pressed'<cr>
    " press 'Esc' + 'd': 'F5 was pressed' is printed

In the last example, the `F5` mapping was used even though the `F10` key and the
`F10` mapping were defined earlier.
This is because `F5` comes before `F10` in the output of `:set termcap`.

## When does Vim translate terminal keys (set with sth like `set <m-d>=^[d`)?

When processing mappings; right before trying to expand the keys.
It doesn't matter whether the keys *will be* remapped; what matters is that they
*can* be remapped.

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        exe "set <m-d>=\ed"
        call feedkeys("i\<esc>d", 'x')
        %p
        qa!
    EOF
    )
    ä~

Here is what happened:

    typeahead | executed
    --------------------
    <esc>d    |
    <m-d>     |
    ä         |

There was no mapping  in the mappings table, and yet  Vim did translate `<esc>d`
into `<m-d>`.  This is because `<esc>d` was fed without the `n` flag, so Vim had
to try to expand the keys; but before doing so, it had to try to translate them.

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        exe "set <m-d>=\ed"
        ino <m-d> <esc>dd
        0pu=['a', 'b', 'c']
        2
        call feedkeys("i\<esc>d", 'x')
        %p
        qa!
    EOF
    )
    a~
    c~

This time,  there *was* a mapping,  and Vim used  it; the result can  only be
explained  if the  terminal  keys  (here `<esc>d`)  were  translated (here  into
`<m-d>`) *before* trying to expand them using mappings (here `ino <m-d> <esc>dd`).

---

This  is confirmed  by  yet 2  other  experiments where  `<esc>d`  is not  typed
directly but expanded from a `<c-b>` mapping:

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        exe "set <m-d>=\ed"
        imap <c-b> <esc>dd
        0pu='x'
        call feedkeys("i\<c-b>", 'x')
        %p
        qa!
    EOF
    )
    ädx~

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        exe "set <m-d>=\ed"
        ino <c-b> <esc>dd
        0pu='x'
        call feedkeys("i\<c-b>", 'x')
        %p
        qa!
    EOF
    )
    ''~

Here's what happened in the first experiment:

    typeahead | executed
    --------------------
    <c-b>     |
    <esc>dd   |
    <m-d>d    |
    äd        |
              | äd

And in the second one:

    typeahead | executed
    --------------------
    <c-b>     |
    <esc>dd   |
              | <esc>dd

`<esc>d` is  only translated in the  first experiment because it's  the only one
where the mapping is recursive, and so Vim has to try to remap the keys one more
time.

##
## How is `b:changedtick` incremented when I change the contents of the buffer?

    $ vim -Nu NONE +"pu='some text'"
    :echo b:changedtick
    3~
    " press:  dd
    :echo b:changedtick
    4~

Notice that  the size  of a  deletion does not  matter; `b:changedtick`  is only
incremented by 1.

    $ vim -Nu NONE +"pu='some text'"
    " press:  cc new text
    :echo b:changedtick
    12~

Notice that  the size  of the  inserted text  *does* matter;  `b:changedtick` is
incremented by 1 as  soon as the text is cut, then by  1 more for every inserted
character.

    $ vim -Nu NONE +"pu='some text'"
    :echo b:changedtick
    3~
    " press:  dd
    :echo b:changedtick
    4~
    " press:  u
    6~
    " press:  C-r
    8~

Notice that the size of an undone/redone change does not matter, `b:changedtick`
by always incremented by 2.

### On which event is it initialized?

On `BufNew`, it is initialized to 1:

    $ touch /tmp/file{1..2}; vim -Nu NONE -S <(cat <<'EOF'
        let g:abuf = 'expand("<abuf>")'
        call getcompletion('buf*', 'event')
            \->filter({_, v -> v !~# 'Cmd$'})
            \->map({_, v -> printf(
            \ 'au %s * unsilent echom "%s in buf " .. %s .. ": tick is " .. getbufvar(%s, "changedtick")'
            \ , v, v, g:abuf, g:abuf)->execute()})
    EOF
    ) /tmp/file1

    :e /tmp/file2
    :mess
    BufNew in buf 2: tick is 1~
    ...~

Btw, yes, you really need `expand('<abuf>')`.
If you just write `bufnr('')` and `b:changedtick`, you'll get wrong results.
That's because `BufNew` is not fired in the context of the newly created buffer,
but in the context of the one from which it's being created.

    $ touch /tmp/file{1..2} && vim -Nu NONE \
        --cmd 'au BufNew * echom printf("bufnr: %d, <abuf>: %d", bufnr(""), expand("<abuf>"))' /tmp/file1

    :e /tmp/file2
    :mess
    bufnr: 1, <abuf>: 2~

---

Note that things  are a little different  if the current buffer, or  the one you
load, is unnamed.

    # special case where current buffer is unnamed
    $ touch /tmp/file; vim -Nu NONE -S <(cat <<'EOF'
        let g:abuf = 'expand("<abuf>")'
        call getcompletion('buf*', 'event')
            \->filter({_, v -> v !~# 'Cmd$'})
            \->map({_, v -> printf(
            \ 'au %s * unsilent echom "%s in buf " .. %s .. ": tick is " .. getbufvar(%s, "changedtick")'
            \ , v, v, g:abuf, g:abuf)->execute()})
    EOF
    )
    :e /tmp/file
    BufDelete in buf 1: tick is~
    BufWipeout in buf 1: tick is~
    BufUnload in buf 1: tick is~
    BufNew in buf 1: tick is~
    BufAdd in buf 1: tick is~
    BufCreate in buf 1: tick is~
    "/tmp/file" 0L, 0C~
    BufRead in buf 1: tick is~
    BufReadPost in buf 1: tick is~
    BufEnter in buf 1: tick is~
    BufWinEnter in buf 1: tick is~

    # special case where new buffer is unnamed
    $ touch /tmp/file; vim -Nu NONE -S <(cat <<'EOF'
        let g:abuf = 'expand("<abuf>")'
        call getcompletion('buf*', 'event')
            \->filter({_, v -> v !~# 'Cmd$'})
            \->map({_, v -> printf(
            \ 'au %s * unsilent echom "%s in buf " .. %s ..": tick is " .. getbufvar(%s, "changedtick")'
            \ , v, v, g:abuf, g:abuf)->execute()})
    EOF
    ) /tmp/file
    :new
    BufNew in buf 2: tick is~
    BufAdd in buf 2: tick is~
    BufCreate in buf 2: tick is~
    BufLeave in buf 1: tick is~
    BufEnter in buf 2: tick is~
    BufWinEnter in buf 2: tick is~

Not sure what to make of these results, but those are special cases.
Most of the time, you deal with buffers which are read from files.
Buffers which are  not tied to a  file are special, and you  probably don't care
about `b:changedtick` for a special buffer.

### On which event(s) is it incremented automatically (i.e. without any manual modification)?

   - on `BufReadPre` when you reload a buffer

         $ touch /tmp/file{1..2}; vim -Nu NONE -S <(cat <<'EOF'
             let g:abuf = 'expand("<abuf>")'
             call getcompletion('buf*', 'event')
                 \->filter({_, v -> v !~# 'Cmd$'})
                 \->map({_, v -> printf(
                 \ 'au %s * unsilent echom "%s in buf " .. %s .. ": tick is " .. getbufvar(%s, "changedtick")'
                 \ , v, v, g:abuf, g:abuf)->execute()})
         EOF
         ) /tmp/file1

         :echo b:changedtick
         3~
         :e
         ...~
         BufRead in buf 1: tick is 4~
         ...~

     Remember that  `BufReadPre` is  fired only  if the buffer  is read  from an
     existing file.

   - on the *first* `BufEnter` (the one fired right after `BufReadPre`)

         $ touch /tmp/file{1..2}; vim -Nu NONE -S <(cat <<'EOF'
             let g:abuf = 'expand("<abuf>")'
             call getcompletion('buf*', 'event')
                 \->filter({_, v -> v !~# 'Cmd$'})
                 \->map({_, v -> printf(
                 \ 'au %s * unsilent echom "%s in buf " .. %s .. ": tick is " .. getbufvar(%s, "changedtick")'
                 \ , v, v, g:abuf, g:abuf)->execute()})
         EOF
         ) /tmp/file1

         :e /tmp/file2
         BufNew in buf 2: tick is 1~
         ...~
         BufEnter in buf 2: tick is 2~
         ...~

   - on `BufWritePost` provided that the buffer is modified

         $ touch /tmp/file && vim -Nu NONE -S <(cat <<'EOF'
             au BufWritePre * echom 'BufWritePre: ' .. b:changedtick
             au BufWritePost * echom 'BufWritePost: ' .. b:changedtick
         EOF
         ) /tmp/file

         :echo b:changedtick
         3~
         :w
         BufWritePre: 3~
         BufWritePost: 3~
         "='' CR p
         :echo b:changedtick
         4~
         :w
         BufWritePre: 4~
         BufWritePost: 5~

###
## How to get the count given for the previous normal command?

Check the value of `v:prevcount`.

---
```vim
" v:count holds the count given for the currently executed normal command
call feedkeys("3d:echom v:count\r")
```
    3~
```vim
" v:count is reset to 0 immediately after the normal command has been executed
call feedkeys("3d:\r:echom v:count\r")
```
    0~
```vim
" but v:prevcount still holds the count which was given
call feedkeys("3d:\r:echom v:prevcount\r")
```
    3~

### The following snippet outputs 0:
```vim
set showcmd
fu Opfunc(...)
    if !a:0
        let &opfunc = 'Opfunc'
        return 'g@'
    endif
    echom v:prevcount
endfu
nno <expr> <c-b> Opfunc()
ono io <cmd>norm! viw<cr>
pu='foo bar baz'
call feedkeys("3\<c-b>io")
```
    0~

#### Why is it not 3?

`:norm` resets the count to 0, and  when Vim processes the bottom of the opfunc,
`:norm` has been  fully executed; which means  that the count it has  set is now
assigned to `v:prevcount`.

MWE:
```vim
call feedkeys("12d:norm! 34\"\r", 'n')
call feedkeys(":echom v:prevcount\r", 'n')
```
    34~

You might wonder why `:norm` resets the count to 0, and not to 1:
for the same reason that `v:count` is 0 when no count was given.
IOW, when  no count was  given, `v:prevcount`  behaves like `v:count`,  not like
`v:count1`.

##
# Pitfalls
## In xterm, Vim doesn't make the difference between `<m-g>` and `<m-G>`!

The shift modifier must be explicit:

    <m-s-g>
       ^^

Example:

    ✘
    $ vim -Nu NONE +'nno <m-g> <cmd>echo "m-g"<cr>' +'nno <m-G> <cmd>echo "m-G"<cr>'
    " press m-g and m-G: no difference

    ✔
    $ vim -Nu NONE +'nno <m-g> <cmd>echo "m-g"<cr>' +'nno <m-s-g> <cmd>echo "m-G"<cr>'
                                                             ^^
    " press m-g and m-G: Vim makes the difference

##
## Why should I avoid a mapping with an `<Esc>` in its lhs?

The terminal uses `Esc` to encode some special keys (e.g. arrow keys, function keys, ...).

Now suppose you have these mappings:

    $ vim -Nu NONE -S <(cat <<'EOF'
        nno <c-b><esc> <cmd>echo 'C-b Esc'<cr>
        nno <c-b><up>  <cmd>echo 'C-b Up'<cr>
    EOF
    )

And you  press `C-b Up`;  instead of  using your 2nd  mapping, Vim will  use the
first one, and insert `A` in the buffer.

Here's what happens:

    typed  | typeahead                  | executed
    ----------------------------------------------
    C-b Up | C-b Esc O A                |
           | <cmd>echo 'C-b Esc' CR O A |
           |                            | <cmd>echo 'C-b Esc' CR O A

Vim conflates the `Esc`  produced by the terminal when `Up`  is pressed, with an
`Esc` typed interactively.

This can lead to unexpected behaviors such as the one reported [here][2].

From `LeoNerd` on the `#vim` irc channel.

   > Yeah.. that's because vim's keyboard input system is stupid
   > In vim- raw bytes arrive from the terminal, go into the map engine (which just looks to see if the
   > headofqueue bytes match any of its mappings, and replace them if so), then bytes come out directly into
   > the command system
   > Whereas in nvim, raw bytes go into the termkey instance, which turns them into *keys*, and those *keys*
   > are what goes into the map engine
   > So the map engine is never confused by the individual component bytes that formed those keypresses
   > Just like it isn't confused by the individual bytes that came across the X11 unix socket when in gvim
   > mode, or.. any other stupid crazy things that wouldn't be possible if it was actually sensible

### What if `<Esc>` is used in the rhs of a mapping?

If the mapping is non-recursive, it should be ok.
Otherwise, replace it with `<C-\><C-n>` so that Vim's map engine can't get confused.

In  general, in  the rhs  of  a mapping,  always write  `<C-\><C-n>` instead  of
`<Esc>`; it's  more consistent, and  more future-proof (a  non-recursive mapping
could be refactored into a recursive one in the future).

---

Example to illustrate the pitfall:

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        exe "set <F31>=\ed"
        imap <c-b> <esc>ddi
        0pu=['a', 'b', 'c']
        2
        call feedkeys("i\<c-b>", 'x')
        %p
        qa!
    EOF
    )

    " outputs:

        a
        <F31>dib
        c

    " instead of:

        a
        c

Here is what I think happens:

    typeahead | executed
    --------------------
    <c-b>     |
    <esc>ddi  |
    <F31>di   |
              | <F31>di

Replacing `<esc>` with `<c-\><c-n>` fixes the issue:

    " bad
    imap <c-b> <esc>ddi
               ^---^

    " good
    imap <c-b> <c-\><c-n>ddi
               ^--------^

Now, this is what happens:

    typeahead     | executed
    --------------------
    <c-b>         |
    <c-\><c-n>ddi |
                  | <c-\><c-n>ddi

---

The reason  why non-recursive mappings should  not be affected by  an `<esc>` in
the rhs  is because Vim only  translates terminal keys *right  before* trying to
expand them via mappings.  If the keys  have been produced by a mapping, and the
latter is non-recursive,  then Vim can't expand them a  second time, and there's
no need to translate terminal keys; so it just executes them.

##
## Why should I avoid `@=` in the rhs of a mapping?

It would reset the last used macro, and make a subsequent `@@` behave unexpectedly:

    $ printf 'a\nb\nc\nd\ne\nf' | vim -Nu NONE +'nno J @="J"<cr>' -
    " press: qq A, Esc J q
             j @q
             j @@

`@@` should get you `e, f` in the last line, but instead you get `e f`.
That's because  when you've executed `@q`,  the last executed register  has been
reset by `@=`.  So  `@@` repeats `@='J'`, and simply joins  the lines; it doesn't
append a comma to the first line before.

### What should I use instead?

If  you were  using `@=`  for a  count to  be applied  to a  sequence of  normal
commands, use `<expr>` instead:

    " before
    nno <silent> cd @='xlx'<cr>

    " after
    nno <expr> cd "\e" .. repeat('xlx', v:count1)

---

If you were  using `@=` for another  reason, you can probably replace  it with a
combination of `:exe` and another command:

    " before
    nno <buffer><nowait><silent> q <c-w><c-p>@=winnr('#')<cr><c-w>c

    " after
    nno <buffer><nowait> q <cmd>wincmd p <bar> exe winnr('#') .. 'wincmd c'<cr>
                                               ^^^                ^----^

###
## When should I avoid `<c-r>=` in a command-line mode mapping?

Whenever you want to be able to use the mapping in the expression command-line.

### Why?

You can't press `C-r =` if you're already on the expression command-line.
It has no effect.

    $ vim -Nu NONE +"cno <c-b> <c-r>='test'<cr>"
    " press:  : C-r = C-b Enter
    " expected:  'test' is inserted
    " result:    nothing is inserted

Note that  if the expression  register is not empty,  `C-r = Enter`  inserts the
evaluation of the  last expression.  Here, nothing is inserted  because there is
no last expression.

### What should I use instead?

`:h c_CTRL-\_e`:

                               v----v
    $ vim -Nu NONE +"cno <c-b> <c-\>e 'test'<cr>"
    " press:  : C-r = C-b
    " result: 'test' is inserted

Note that contrary  to `C-r =` which *inserts* the  evaluation of an expression,
`C-\ e` *replaces* the whole command-line with the evaluation of an expression.
You need to take that into account when writing your mapping.

##
## My mapping ignores the count I prefixed it with!

You may have a `:norm!` command somewhere which resets `v:count[1]` to 0/1.
Try to  capture `v:count[1]`  as soon  as possible in  a variable;  then, always
refer to the latter in your code (never refer to `v:count[1]`).

Capture it either at the very start of the function definition:

    nno cd <cmd>call Func()
    fu Func()
        let cnt = v:count1
        " refer to `cnt` when needed
        ...
    endfu

Or at the function call site:

    nno cd <cmd>call Func(v:count1)
    fu Func(cnt)
        " refer to `a:cnt` when needed
        ...
    endfu

---

It's not always possible or a good idea to capture the count at the call site.
It's not possible when the function is used as an opfunc.
It's  not  a  good idea  when  the  function  is  called repeatedly  in  various
mappings/commands (DRY, DIE).

In those cases, capture the variable at the start of the function definition.

## My mapping raises E474 when I try to install it!

The limit size of a lhs is 50 bytes.

    $ vim -Nu NONE +'nno xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx abc'
    E474: Invalid argument~

Make the lhs shorter.

---

Note that the weight of `<plug>` is 3 bytes:

    :echo len("\<plug>")
    3~

## My mapping invokes `input()`.  But the latter consumes the end of the rhs!

    nno cd <cmd>call Func()<cr>bbb
    fu Func() abort
        call input('>')
    endfu

Press  `cd`, and  you'll  see that  `bbb`  has been  consumed  by `input()`  and
inserted on the command-line, instead of being pressed.

Solution:

Surround `input()` with `inputsave()` and `inputrestore()`:

    nno cd <cmd>call Func()<cr>bbb
    fu Func() abort
        call inputsave()
        call input('>')
        call inputrestore()
    endfu

---

Alternatively, you could use `:norm` to execute the end of the rhs before the CR
which invokes `input()`.

    nno cd <cmd>call Func()<bar>norm! bbb<cr>
    fu Func() abort
        call input('>')
    endfu

But this would lead to another pitfall if `Func()` executes an interactive command.
Besides, it makes the code less readable: "why did I use :norm ?".
In the future, you may forget the purpose of `:norm`, and think you can simplify
the code by getting rid of it:

    nno cd <cmd>call Func()<bar>norm! bbb<cr>
    →
    nno cd <cmd>call Func()<cr>bbb

So, I recommend you avoid this solution; don't be clever, be explicit.

## My mapping invokes a command which requires some user input.  It doesn't ask for my input!

Make sure your command is not executed via `:norm`:

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

`:norm` considers interactive  commands/functions, like `z=`, `:s`  with the `c`
flag, `getchar()`,  ... as  *in*complete (the  user's input  is missing).   As a
result, it presses Escape which prevents you from providing any input.

From `:h norm`:

   > {commands} should be a complete command.  If
   > {commands} does not finish a command, the last one
   > will be aborted as if <Esc> or <C-C> was typed.

Solution: Find a way to execute your command without `:norm`, via `feedkeys()` if needed.

---

The issue persists even if `:norm` executes your command indirectly:

    ✘
    nno z= <cmd>set opfunc=Z_equal<bar>norm! g@l<cr>
    fu Z_equal(_)
        setl spell
        call feedkeys('z=', 'in')
    endfu
    " press 'z=' right above the misspelled word 'helzo':  you can't choose any suggestion in the pager
    " and yet, between ':norm' and 'z=', there were 'g@l', 'Z_equal()' and 'feedkeys()'

    ✔
    nno <expr> z= Z_equal()
    fu Z_equal(...)
        if !a:0
            setl spell
            let &opfunc = 'Z_equal'
            return 'g@l'
        endif
        call feedkeys('z=', 'in')
    endfu

---

Note  that for  some reason,  `:norm!` does  not seem  to consider  `input()` as
incomplete:

    " you can type anything you want, as usual
    :exe "norm! :let g:input = input('')\r"

## My terminal mapping suffers from an unexpected timeout!

    $ vim -Nu NONE +'set showcmd | tno <c-w>a bbb' +term

    " press:  C-w C-w
    " result:   Vim focuses the bottom window after 1s
    " expected: Vim focuses the bottom window immediately

Solution: install this mapping:

    tno <c-w><c-w> <c-w><c-w>

Test it like this:

    $ vim -Nu NONE +'set showcmd | tno <c-w>a bbb' +'tno <c-w><c-w> <c-w><c-w>' +term
                                                     ^-----------------------^

---

Issue explanation.

It seems that `'termwinkey'` is not written in the typeahead (not printed in the
`'showcmd'` area immediately).  I guess it's processed outside.

This creates an issue if you have  a Terminal-Job mode mapping which starts with
`'termwinkey'`.  When you press the key,  should Vim process it with its default
meaning (i.e. start a C-W command)?  Or should it remap the key?

In the first case, the key must stay *outside* the typeahead.
In the second case, the key must be sent *into* the typeahead.
Vim solves  this issue by waiting  `&timeoutlen` ms before sending  the key into
the typeahead.

---

Solution explanation.

    tno <c-w><c-w> <c-w><c-w>

With the  previous mapping,  when you  press the first  `C-w`, there's  still an
ambiguity.  But when  you press the second `C-w`, Vim  understands that you want
to  use  the  `<c-w><c-w>`  mapping  and immediately  writes  the  keys  in  the
typeahead.  Note that the issue persists  if you wait more than `&timeoutlen` ms
between the first `C-w` and the second one.

---

Limitation.

The solution  works under the  assumption that you didn't  reset `'termwinkey'`,
and as a result Vim uses `<C-w>` to  start a C-W command.  This wouldn't work if
you've reset  the option to, let's  say, `<C-s>`, and you  press `<C-s><C-w>` to
focus another window.  For something more reliable, try this:

    augroup termwinkey_no_timeout | au!
        au TerminalWinOpen * let b:_twk = &l:twk == '' ? '<c-w>' : &l:twk
          \ | exe printf('tno <buffer><nowait> %s<c-w> %s<c-w>', b:_twk , b:_twk)
          \ | unlet! b:_twk
    augroup END

Or:

    augroup termwinkey_no_timeout | au!
        au TerminalWinOpen * let b:_twk = expand('<abuf>')->str2nr()->getbufvar('&twk')
          \ | if b:_twk == '' | let b:_twk = '<c-w>' | endif
          \ | exe printf('tno <buffer><nowait> %s<c-w> %s<c-w>', b:_twk , b:_twk)
          \ | unlet! b:_twk
    augroup END

## My visual mapping uses `<cmd>`.  It doesn't work as expected!

Check whether it refers  to the visual marks `'<` and `'>` (or  to the range `*`
which is an alias for `'<,'>`).

Remember  that those  are updated  only  when leaving  visual mode;  but if  you
execute an Ex command  with `<cmd>`, you stay in visual mode,  and the marks are
not updated.

Solution 1:

Press `<c-\><c-n>`  right before `<cmd>` to  force Vim to leave  visual mode and
update the marks.

    xno <key> <c-\><c-n><cmd>call Func()<cr>
              ^--------^

Solution 2:

Use these expressions to get the coordinates of the starting mark:

   - line('v')
   - col('v')

And these for the ending mark:

   - line('.')
   - col('.')

Example:
```vim
xno <F3> <cmd>call Func()<cr>
def Func()
    " ✘
    :*s/pat/rep/g
enddef
```
```vim
xno <F3> <cmd>call Func()<cr>
def Func()
    " ✔
    var range = line('v') .. ',' .. line('.')
    exe range .. 's/pat/rep/g'
enddef
```
##
## How to use a chord with the meta modifier in my mappings?

If you use the  GUI, you don't need anything special, but you  need at least the
patch [8.2.0851][3].

If  you  use Vim  in  a  terminal  which  supports the  modifyOtherKeys  feature
(typically xterm), again,  you don't need anything special.   The feature should
be enabled by default, but if that's not  the case, you can enable it by setting
the terminal options `'t_TI'` and `'t_TE'`:

                       ┌ 1 = enables this feature for keys excluding keys with well-known behavior
                       │ 2 = enables this feature for all keys (see `man xterm /^\s*modifyOtherKeys`)
                       │
    let &t_TI = "\e[>4;2m"
    let &t_TE = "\e[>4;m"

If you use Vim in a terminal which does not support the modifyOtherKeys feature,
write this:

                   ┌ terminal sequence encoding `M-b`
                   ├─┐
    exe "set <M-b>=\eb"
    ino <M-b> ...

---

You can  check whether  the modifyOtherKeys  feature is  enabled by  pressing in
insert mode `C-S-v` followed by `C-v`.

If Vim inserts this key code:

    ^[[27;5;118~

Then it's enabled; otherwise, if you just get:

    ^V

Then it's disabled.

Note that for the test to succeed, you need to make sure that you don't have any
terminal key binding on `C-S-v`, like this one in `~/.Xresources` for example:

    XTerm*VT100.Translations: #override \
                     Ctrl Shift <Key>V:    insert-selection(CLIPBOARD) \n\
                     Ctrl Shift <Key>C:    copy-selection(CLIPBOARD)

If you have one, try to disable it temporarily.

### Now I can't insert some accented characters anymore!

It  probably means  that  you're  using a  terminal  which  doesn't support  the
modifyOtherKeys feature, or you didn't enable the feature.

In that case, if you have the mapping `ino <m-d> <c-o>de`, you can't insert `ä`:

    exe "set <M-d>=\ed"
    ino <M-d> <c-o>de
    startinsert
    " press the dead key '¨' followed by 'a':  'ä' is not inserted

Workarounds:

Use gVim or a terminal which supports the modifyOtherKeys feature (and make sure
it's enabled).

Or press `C-v` to suppress mappings:

    C-v ¨ a

From `:h i^v`:

   > The characters typed right after CTRL-V are not considered for mapping.

Or use a digraph:

    C-k a "

Or use replace mode:

    r ¨ a

Or use an equivalence class in a search command (`[[=a=]]`).

#### But what causes this pitfall?

When you try to insert `ä`, it's first written in the typeahead buffer.
But internally, Vim encodes `ä` exactly as `<M-d>`:

    $ vim -Nu NONE
    :echo "\<m-d>"
    ä~

So, it's as if you had press `<M-d>`, which is then remapped according to your mappings.

---

The  reason  why Vim  encodes  `<M-d>`  like `ä`  is  probably  due to  history.
Originally, I think terminals could encode up to 128 characters using seven bits
(via a  standard named ASCII).   And to encode  chords using the  meta modifier,
they flipped the eighth bit:

    character | binary encoding | decimal code
    ------------------------------------------
      d       | 01100100        | 100
    M-d       | 11100100        | 228
                ^
                flipped

Later, terminals  switched to  extended ASCII  to encode  up to  256 characters.
They needed the  eighth bit to encode  new characters; it could not  be used for
meta anymore.  As  an example, the binary  code `11100100` could not  be used to
encode `M-d` anymore; now it was meant to encode `ä`.

So,  to encode  chords, terminals  switched to  a different  scheme; instead  of
sending only 1 byte, they sent several; the first one always encoding the escape
character.  As a result,  `M-d` is now encoded as `Esc` + `d`  (at least by most
terminals, including xterm).

From the terminal's  point of view, there's no ambiguity  between `M-d` and `ä`;
it sends different sequences for the two characters.
But Vim, up to this day, still encodes `<M-d>` just like `ä`.

This is my understanding based on this answer:
<https://vi.stackexchange.com/a/3570/17449>

---

Btw, you can check that all  the previous binary/decimal codes are correct, from
Vim, by running:

    :echo char2nr('d')
    100~
                                            decimal code of 'd'
                                            v-v
    :echo system('bc <<<"ibase=10; obase=2; 100"')[:-2]
    1100100~
                                              binary code of 'd' with an extra bit set on the left
                                              v------v
    :echo system('bc <<<"ibase=2; obase=1010; 11100100"')[:-2]
    228~
    :echo nr2char('228')
    ä~

####
#### I don't want to change my terminal, and I want a fix which doesn't require any extra input!

Try this:

    exe "set <F30>=\ed"
    nno <F30> ...
         ├─┘
         └ arbitrary function key
          (you want to choose one which you'll never press interactively, so forget about F1-F12)

Example:

    exe "set <F30>=\ed"
    nno <F30> <cmd>echom 'I pressed M-d'<cr>
    " press M-d:  Vim logs the message 'I pressed M-d'

---

Note that you can use function keys up to the number 37.

    :set <f37>
    E846: Key code not set: <f37>~

    :set <f38>
    E518: Unknown option: <f38>~

And you  can combine  a function  key with  the shift  modifier to  decrease the
probability you'll ever press it interactively:

    nno <S-F30> ...
         ^^

But you can't use any other modifier:

    :set <c-f1>
    E518: Unknown option: <c-f1>~

    :set <m-f1>
    E518: Unknown option: <m-f1>~

---

It works, but in practice it's cumbersome  to use because it's only necessary in
Vim and only if modifyOtherKeys is not enabled,  so you have to use this kind of
template when installing your meta mappings:

    if has('gui_running') || &t_TI =~# "\e[>4;[12]m"
        nno <m-d> ...
    else
        nno <f30> ...
    endif

Besides, using function keys to refer to meta chords makes the code harder to read.

##### How does this work?

By telling Vim a lie:

    exe "set <F30>=\ed"

This tells Vim that  whenever it sees the sequence `Esc` +  `d` in the typeahead
buffer, it must translate it into `<F30>`; which is wrong, but bear with me.

From then, whenever you need to refer to `M-d` in a mapping, you write `<F30>`.
As an example, you don't write this:

    ino <M-d> <esc>id
        ^---^
        ✘

But this:

    ino <F30> <c-o>de
        ^---^
        ✔

Now, when you'll try to insert `ä`, here's what happens:

    typeahead | executed
    --------------------
    ä         |
              | ä

`ä` is not remapped  in the typeahead buffer because you  don't have any mapping
whose lhs is `<M-d>` nor `ä`.

###### Wait.  How does a mapping triggered by `<M-d>` still work if I never write the latter explicitly?

You don't need the  Vim key code `<M-d>` to make Vim execute  sth when you press
`M-d` in the terminal.

Consider the previous code:

    exe "set <F30>=\ed"
    ino <F30> <c-o>de

And suppose you press `M-d`; here's what happens:

    typeahead | executed
    --------------------
    <esc>d    |
    <F30>     |
    <c-o>de   |
              | <c-o>de

####
## Sometimes, my autocmd listening to `InsertLeave` is not triggered!

If you've quit insert mode by pressing `C-c`, `InsertLeave` was not fired.
Note that this is  working as intended; if that's an issue  for you, you'll need
to find a workaround which does not rely on `InsertLeave`.

##
## `<nop>` doesn't work!

`<nop>`  loses its  special meaning  as  soon as  it's followed  or preceded  by
another key.  IOW, it must be alone.

    $ vim -Nu NONE -i NONE +'nno <c-b> <nop>x'
    " press:  C-b
    E35: No previous regular expression~
    " this error is raised by the 'n' in '<nop>'

## `<nowait>` doesn't work!

Try to install your mapping later.

---

The installation order of your mappings matters:

    $ vim -Nu NONE -S <(cat <<'EOF'
        set showcmd timeoutlen=3000
        nno <nowait> <c-b>  <cmd>echo "c-b was pressed"<cr>
        nno          <c-b>x <nop>
    EOF
    )
    " press C-b: you need to wait 3s for the message to be printed

    $ vim -Nu NONE -S <(cat <<'EOF'
        set showcmd timeoutlen=3000
        nno          <c-b>x <nop>
        nno <nowait> <c-b>  <cmd>echo "c-b was pressed"<cr>
    EOF
    )
    " press C-b: the message is printed immediately

---

In practice, you should not encounter this issue, because `<nowait>` is intended
to prevent a global mapping from causing a timeout for a buffer-local mapping.

And a buffer-local mapping is typically installed from a filetype plugin while a
global mapping  is installed from a  regular plugin; regular plugins  are always
sourced before any filetype plugin.

---

See also: <https://github.com/vim/vim/issues/6810#issuecomment-683425978>

## `:h modifyOtherKeys` doesn't work when Vim runs inside tmux!

Make sure to set the server option `extended-keys`:

    set -s extended-keys on

And to enable  the `extkeys` feature by including the  entry `xterm*:extkeys` in
the server option `terminal-features`:

    set -as terminal-features 'xterm*:extkeys'
                               ^----^
                               if you have a terminal which supports extended keys
                               but whose '$TERM' does not start with 'xterm', you may
                               need to add another pattern, or just use '*'

Usage example:

    $ tmux -Lx -f <(cat <<'EOF'
        set -s extended-keys on
        set -as terminal-features 'xterm*:extkeys'
    EOF
    )

    $ vim -Nu NONE --cmd 'let [&t_TI, &t_TE] = ["\e[>4;1m", "\e[>4;m"]' \
      +'nno <C-Enter> <cmd>echom "C-Enter was pressed"<cr>'
    " press:  C-Enter
    C-Enter was pressed~
    " note that 'Enter' is really the 'Enter' key, not 'C-m'

---

Technically,  enabling the  `extkeys`  feature  makes Vim  set  the `Dseks`  and
`Eneks` capabilities in `$ tmux info`.

    $ tmux info | grep '\(Ds\|En\)eks'
    31: Dseks: (string) \033[>4m~
    41: Eneks: (string) \033[>4;1m~

It's equivalent to:

    set -as terminal-overrides 'xterm*:Eneks=\E[>4;1m'
    set -as terminal-overrides 'xterm*:Dseks=\E[>4;m'

For more info, see:
- <https://github.com/tmux/tmux/wiki/Modifier-Keys#extended-keys>
- <https://github.com/tmux/tmux/issues/2216#issuecomment-629600225>
- <https://github.com/tmux/tmux/issues/2216#issuecomment-629601762>

### It still doesn't work.  I can't make Vim distinguish between `Tab` and `C-i`!

tmux only supports `modifyOtherKeys = 1`, not `modifyOtherKeys = 2`.
The difference  is that  the former does  not enable the  feature for  keys with
well-known behavior like `Tab`.

The latter would be tricky to implement:
<https://github.com/tmux/tmux/issues/2216#issuecomment-629597863>

---

From `man xterm /^\s*modifyOtherKeys`:

   > modifyOtherKeys (class ModifyOtherKeys)
   >         Like modifyCursorKeys,  tells  xterm  to  construct  an  escape
   >         sequence  for  other  keys  (such as “2”) when modified by Con‐
   >         trol-, Alt- or Meta-modifiers.  This feature does not apply  to
   >         function  keys and well-defined keys such as ESC or the control
   >         keys.  The default is “0”:
   >
   >         0    disables this feature.
   >
   >         1    enables this feature for keys except for those with  well-
   >              known behavior, e.g., Tab, Backarrow and some special con‐
   >              trol character cases, e.g., Control-Space to make a NUL.
   >
   >         2    enables this feature for  keys  including  the  exceptions
   >              listed.

---

For this reason, inside tmux, you could also (should?) set `'t_TI'` like this:

    let &t_TI = "\<Esc>[>4;1m"
                           ^

Instead of this:

    let &t_TI = "\<Esc>[>4;2m"
                           ^

##
## I have an `<expr>` mapping calling a `:def` function which invokes `getchar()` and `nr2char()`:
```vim
vim9script
set ut=50
au CursorHold * #
nno <expr> <F3> <sid>Func()
def Func(): string
    getchar()->nr2char()
    return ''
enddef
feedkeys("\<F3>")
```
### It raises E1030: Using a String as a Number: "<80><fd>`"!

When a function is invoked in an `<expr>` mapping, the `<CursorHold>` key is pressed.
This is documented at `:h <cursorhold>`:

   > Internally the autocommand is triggered by the
   > <CursorHold> key. In an expression mapping
   > |getchar()| may see this character.

This is not an issue in a legacy function because there's no type checking there.
But it *is* in a `:def` function.

Anyway, use `<cmd>` instead of `<expr>`:
```vim
vim9script
set ut=50
au CursorHold * #
nno <F3> <cmd>call <sid>Func()<cr>
def Func()
    getchar()->nr2char()
enddef
feedkeys("\<F3>")
```
##
# Issues
## When I press some special key (`<f1>`, `<up>`, `<M-b>`, ...) it doesn't behave as expected!

Make sure that you don't have any mapping containing `Esc` in its lhs.
Run `:new|pu=execute('map')`, and look for the  pattern `<esc>`, but only in the
lhs of a mapping.

If one  of them does, and  you want to keep  it, then you'll have  to double the
`Esc`  (and obviously  you'll need  to press  it twice  for your  mapping to  be
triggered now).  What is  important is that there is no way  for Vim to conflate
this `Esc` with  the start of a sequence  of key codes (like `Esc O  A` which is
produced by `<up>` in xterm).

- <https://github.com/vim/vim/issues/2216>
- <https://vi.stackexchange.com/a/24403/17449>

##
# Todo
## operators
### Why should I use `<expr>` when installing an operator mapping?

Without `<expr>`, the count and register are not passed naturally to the opfunc,
and by the time the opfunc is processed, they have been reset to resp. 0 and `"`.

    nno <c-b> <cmd>set opfunc=Op<cr>g@
    fu Op(_)
        echom 'the count is ' .. v:count
        echom 'the register is ' .. v:register
    endfu

    " press:  "a 3 C-b l
    :mess
    the count is 0~
    the register is "~

You'll need to pass them manually, either via `:norm` or `feedkeys()`.
But both come with pitfalls.
For example, `:norm` can break an  interactive command by pressing `Esc` when an
input is asked:

    "                                          v---v
    nno <c-b><c-b> <cmd>set opfunc=Op<bar>exe 'norm! ' .. (v:count ? v:count : '') .. 'g@_'<cr>
    call setline(1, ["a\x01b"])
    fu Op(_)
        '[,']s/[[:cntrl:]]//c
    endfu

    " press:     C-b C-b
    " result:    nothing happens
    " expected:  the literal ^A is removed

Not  that  from *inside*  the  opfunc,  you could  still  access  the count  via
`v:prevcount` instead of `v:count`, but:

   - not the register; there is no `v:prevregister`
   - you want `v:count`, and not `v:prevcount`, if you need the count from *outside* the opfunc
     (e.g. to execute sth like `123g@_`)

`feedkeys()` can avoid the issue, but passing it the right flags can be tricky.

Besides, the operator would not work as expected when preceded by a count.

    nno <c-b> <cmd>set opfunc=Op<cr>g@
    fu Op(type)
        if a:type is# 'line'
            sil norm! '[V']y
        elseif a:type is# 'char'
            sil norm! `[v`]y
        elseif a:type is# 'block'
            sil exe "norm! `[\<c-v>`]y"
        endif
        echom @@
    endfu
    call setline(1, ['aaa', 'bbb', 'ccc'])

    " ✔
    " press:  C-b 2 j
    aaa^@bbb^@ccc^@~

    " ✘
    " press:  2 C-b j
    aaa^@bbb^@~
    " '2 C-b j' should behave like '2dj'; i.e. operate on 3 lines, not 2

With `<expr>`,  all these issues are  fixed, because the count  and register are
passed naturally:

    nno <expr> <c-b> Op()
    fu Op(...)
        if !a:0
            set opfunc=Op
            return 'g@'
        endif
        echom 'the count is ' .. v:count
        echom 'the register is ' .. v:register
    endfu

    " press:  "a 3 C-b l
    :mess
    the count is 3~
    the register is a~

See also: <https://vi.stackexchange.com/a/12557/17449>

---

Without `<expr>`, visual mode needs to be handled specially:

    nno <c-b> <cmd>set opfunc=CountSpaces<cr>g@
    xno <c-b> <cmd>call CountSpaces(visualmode(), 1)<cr>
    fu CountSpaces(type, ...)
        if a:0
            set opfunc=CountSpaces
            " can't use ':norm', because dot would be reset at the end of the function
            " feedkeys() avoids the issue, because the keys are processed *after* the function
            return feedkeys('gvg@', 'in')
        elseif a:type is# 'line'
            sil norm! '[V']y
        elseif a:type is# 'char'
            sil norm! `[v`]y
        elseif a:type is# 'block'
            sil exe "norm! `[\<c-v>`]y"
        endif
        echom count(@@, ' ')
    endfu

With `<expr>`,  there's no need to,  because visual mode can  be handled exactly
like normal mode:

    nno <expr> <c-b> CountSpaces()
    xno <expr> <c-b> CountSpaces()
    fu CountSpaces(...)
        if !a:0
            set opfunc=CountSpaces
            return 'g@'
        endif
        let type = a:1
        if type is# 'line'
            sil norm! '[V']y
        elseif type is# 'char'
            sil norm! `[v`]y
        elseif type is# 'block'
            sil exe "norm! `[\<c-v>`]y"
        endif
        echom count(@@, ' ')
    endfu

---

The mappings are easier to read.  Compare:

    nno <c-b> <cmd>set opfunc=CountSpaces<cr>g@
    xno <c-b> <cmd>call CountSpaces(visualmode(), 1)<cr>
    nno <c-b><c-b> <cmd>set opfunc=CountSpaces<bar>exe 'norm! ' .. (v:count ? v:count : '') .. 'g@_'<cr>

Versus:

    nno <expr> <c-b> CountSpaces()
    xno <expr> <c-b> CountSpaces()
    nno <expr> <c-b><c-b> CountSpaces() .. '_'

---

With `<expr>`, the mappings don't  enter the command-line, so `CmdlineEnter` and
`CmdlineLeave` are not fired, and the code has fewer side-effects.

#### How to pass an arbitrary argument to my opfunc?

Use two functions; for example `OpSetup()` and `Op()`.
Use the first one to save the argument in a script-local variable.
Use the second one to implement the operator.

    nno <expr> <c-a> OpSetup('some arg')
    xno <expr> <c-a> OpSetup('some arg')
    nno <expr> <c-a><c-a> OpSetup('some arg') .. '_'

    nno <expr> <c-b> OpSetup('another arg')
    xno <expr> <c-b> OpSetup('another arg')
    nno <expr> <c-b><c-b> OpSetup('another arg') .. '_'

    fu OpSetup(arg)
        let s:arg = a:arg
        let &opfunc = 'Op'
        "              ^^
        return 'g@'
    endfu

    fu Op(type)
        " the argument passed to the opfunc is in 's:arg'
        ...
    endfu

###
### What's the type received by an opfunc when using `:h o_v`, `:h o_V`, `:h o^v`?

As expected, the type is `char` for `:h o_v`, `line` for `:h o_V`, and `block` for `:h o^v`.

    nno <expr> <c-b> Op()
    fu Op(...)
        if !a:0
            let &opfunc = 'Op'
            return 'g@'
        endif
        let type = a:1
        echom type
    endfu

    " press:  C-b v j
    " Vim prints:  char

    " press:  C-b V l
    " Vim prints:  line

    " press:  C-b C-v j
    " Vim prints:  block

That's because `g@` can only send the types `char`, `line`, `block`, and nothing else.
In particular, it can't send sth like `v`, `vis` or `visual`.
So, in your opfunc, you don't need  to worry about the type having an unexpected
value (or  one which makes your  code handle the  text-object as if you  were in
visual mode) even when the text-object was prefixed by `v`, `V` or `C-v`.

###
### ?

Should we use `:keepj` in all our operators?
See `myfuncs#op_replace_without_yank()`.

It doesn't seem useful for the jumplist (update: now it seems useful...), but it
is for  the changelist.   It seems that  if you use  `:keepj` for  every edition
performed in your  opfunc, then no entry  is added in the  changelist.  OTOH, if
you omit `:keepj`  for *any* edition performed by your  opfunc, then *one* entry
is added in the changelist.

tommy uses it here: <https://vi.stackexchange.com/a/8748/17449>
But I don't see why...

---

Dirvish uses `keepj` for `tabnext` and `wincmd w`:
<https://github.com/justinmk/vim-dirvish/blob/fa6197150dbffe0f93028c46cd229bcca83105a9/autoload/dirvish.vim#L4>

    exe s:noau 'tabnext' a:tnr
    exe s:noau wnr.'wincmd w'
    exe s:noau origwinalt.'wincmd w|' s:noau origwin.'wincmd w'
    exe s:noau 'tabnext '.curtab
    exe s:noau curwinalt.'wincmd w|' s:noau curwin.'wincmd w'

Why?

Update: It seems  that creating  a new  window /  tabpage adds  an entry  in the
jumplist of the latter, which points to  the last cursor location in the file of
the  previous window.   Unless  you do  a simple  split  (`:sp`).  And  `:keepj`
prevents that.

Should we do the same?
Are there other commands for which we should have used `keepj` in the past?
Tpope uses `:keepj` in only 2 plugins:

    " fugitive
    silent keepjumps $delete _
    silent keepjumps 2delete _
    silent keepjumps %delete_
    keepjumps 1
    keepjumps call search('^parent ')
    silent keepjumps delete_
    silent exe (exists(':keeppatterns') ? 'keeppatterns' : '') 'keepjumps s/\m\C\%(^parent\)\@<! /\rparent /e' .. (&gdefault ? '' : 'g')
    keepjumps let lnum = search('^encoding \%(<unknown>\)\=$', 'W', line('.') + 3)
    silent exe (exists(':keeppatterns') ? 'keeppatterns' : '') 'keepjumps 1,/^diff --git\|\%$/s/\r$//e'
    keepjumps call setpos('.',pos)
    exe 'silent keepjumps ' .. (lnum + 1) .. ',' .. lnum2 .. 'delete _'
    keepjumps syncbind

    " vim-rails
    exe 'keepjumps djump' def

You can check this by going to github, then looking for:

    keepjumps user:tpope

then clicking on the `code` tab button.

---

Check whether we've used `:keepj` in the right places in the past:

    :vim /keepj/gj $MYVIMRC ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/**

Tpope seems to use `:keepj` whenever he runs `:delete`.
Check whether we've done the same:

    :vim /\C\%(g:\)\@2<!\%([^[:keyword:]]\|\d\)\@<=d_\%(ebug\|count\)\@!/gj $MYVIMRC ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/**

### ?

Have we used `:s`, where `setline()` would have been better?

### ?

Check whether we should have set `g:opfunc.yank` to `v:false` for some of our custom operators:

    :vim /\COpfunc/gj $MYVIMRC ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/**

Have a look at our `dr` operator for an example where we need to do that.

##
## text-objects
### These 2 omaps give different results:

    ono ii <cmd>norm! TXctY<cr>
    ono ii TXctY

Tested against this text:

    aXbbbbbYcc
        ^
        cursor

With the first omap, after pressing `cii`, the text is:

    ac

With the second omap, after pressing `cii`, the text is:

    aXctYbbbYcc

#### Why?

Both omaps define a text-object via a motion, not a visual selection.

In the first one, the motion is an Ex command (`:norm! ...`).
In the second one, the motion is `TX`.
It doesn't  matter that there  are other  keys in the  rhs of the  omap (`ctY`);
they're not part of the `TX` motion.  As a result, `ctY` is executed from insert
mode, because that's the mode in which Vim is after executing `cTX`.

Similarly, when you install  a normal-mode mapping, all the keys  in the rhs are
not necessarily  executed in normal mode;  e.g. if you write  `:` somewhere, all
the subsequent keys are executed in command-line mode.

###
### Consider the next mapping which should operate on the text between an `X` and a `Y`:

    ono ii <cmd>exe 'norm! TX' .. v:operator .. 'tY'<cr>

#### It doesn't work as expected on this text:

     aXbbbbbYcc
         ^
         cursor here

If you press `dii`, you get this:

     aXc

And if you press `cii`, you get this:

    ac

In both cases, it should be:

     aXYcc

##### Why?

When `Tx` is executed, Vim moves the cursor right after `x`:

    aXbbbbbYcc
      ^

But the `d` operator is not executed  yet.  It still waits for the whole `:norm`
command to be processed to determine what is the text-object.

Then, `dtY` is executed, and Vim deletes up to `Y`:

    aXYcc

That's because `dtY` is run by `:norm`, and  thus Vim is in normal mode when the
keys are processed.   It's not in operator-pending mode (even  though `:norm` is
run from the latter mode).

*Now*, `d` determines what is the text-object.  There is no visual selection, so
it uses  the text between  the current cursor  position and the  original cursor
position.  Currently, the cursor is on column 3:

    aXYcc
      ^
      cursor

But originally it was on column 5:

    aXbbbbbYcc
        ^
        cursor

So `d` considers that the text-object  is composed of all the characters between
the column 3 (included) and 5 (excluded):

    aXYcc
      ^^

You may wonder why column 3 is included but not 5.
That's because a `:cmd` motion is exclusive.
From `:h exclusive /Note.*:`:

   > Note that when using ":" any motion becomes characterwise exclusive.

---

The  reason why  `X` is  unexpectedly  removed when  using the  `c` operator  is
because `TXctY` is  an incomplete command, which causes `:norm`  to press `Esc`,
which in turn causes the cursor to move 1 character backward *on* the `X`.

##### How to fix it?

Cancel the original operator before re-invoking it with `v:operator`:

    ono ii <c-\><c-n><cmd>exe 'norm! TX' .. v:operator .. 'tY'<cr>
           ^--------^

Or better yet, use an `<expr>` mapping:

    ono <expr> ii 'TX' .. v:operator .. 'tY'

In both cases, the sequence of commands `TXdtY` is no longer processed as a motion.

###
### What's one pitfall of an omap which relies on `v:operator`?

It's probably not repeatable with `.`.

For example, consider this omap:

    ono <expr> ii 'TX' .. v:operator .. 'tY'

And this text:

        cursor
        v
    aXbbbbbYc
    aXbbbbbYc
        ^
        cursor

If you press `dii` on the first line, you get:

    aXYc

But if you then press `.` on the second line, you get:

    aXbbYc

That's because `dii` executes 2 operations: `dTX` and `dtY`.
`.` only repeats the last one, i.e. `dtY`.

###
### In the rhs of an `:ono` mapping, should I use `:h c^u` at the start of a command-line?

No.

Whether you use `<cmd>` or not, `<c-u>` is useless:

    ono ix <cmd>eval 0<cr>
    call feedkeys('123dix')
    E481 is not raised~

    ono ix :eval 0<cr>
    call feedkeys('123dix')
    E481 is not raised~

### My text-object is noisy when reused with the dot command.  The rhs is printed on the command-line!
```vim
ono <silent> ix :eval 0<cr>
call feedkeys('dix.')
```
    "eval 0" is printed on the command-line
    ✘


Solution: Use `<cmd>`:
```vim
ono ix <cmd>eval 0<cr>
call feedkeys('dix.')
```
    nothing is printed on the command-line
    ✔

---

The issue may  not be visible if  the operation has changed  more than `&report`
lines; that's because in that case, Vim prints some message on the command-line,
such as:

    3 fewer lines

---

There  are  other   solutions,  like  using  `<expr>`  to   avoid  entering  the
command-line, or writing  a command which causes the command-line  to be erased,
at the end of the code implementing the text-object, like:

    :echo
    :exe "norm! \<c-\>\<c-n>"

But those solutions look like hacks.

### When I use my text-object with the "!" operator, the command-line is not drawn immediately!
```vim
ono <silent> ix :call search('pat')<cr>
call feedkeys('!ix')
```
    the command-line is not redrawn

To make Vim redraw the command-line, press `SPC` then `BS`.

Solution:

Drop `<silent>` and use `<cmd>`:
```vim
ono ix <cmd>call search('pat')<cr>
call feedkeys('!ix')
```
    the command-line *is* redrawn

###
### ?

Review all  custom text-objects: make sure  they all position the  cursor on the
end  of the  selection, to  be consistent  with what  Vim seems  to do  with its
builtin text-objects (e.g. try `vi{` in a shell function).

    \C\<\%(ono\%[remap]\|omap\|noremap\|map\)\>(\@!

### ?

Make sure that none of your text-objects force a particular type of visual mode.

For example, in the past, when we pressed  `C-v ]z`, we ended up with a linewise
selection:

    exe 'norm! ' .. fixed_corner .. 'GV' .. line('.') .. 'G'
                                      ^
                                      ✘

We've fixed that.  Now, we preserve the blockwise mode:

    exe 'norm! ' .. fixed_corner .. 'G' .. a:mode .. line('.') .. 'G'
                                           ^----^
                                             ✔

### ?

Make sure your text-objects correctly handle a `v`, `V`, `C-v` prefix, by inspecting the
output of `mode(1)`: <https://github.com/vim/vim/releases/tag/v8.1.0648>

It  means that  all  our  text-objects should  be  implemented  with `<cmd>`  or
`<expr>`.  Otherwise, the output of `mode(1)` is unreliable.

    \C\<\%(ono\%[remap]\|omap\|noremap\|map\)\>(\@!

### ?

Make sure  your text-objects handle a  count.  For example, right  now, it looks
like `il` does not; `5dil` deletes only the current line.  Shouldn't it delete 5
lines?  Study  how builtin objects  handle counts; check whether  their behavior
differ depending on whether they start with `i` or `a` (e.g. `iw` vs `aw`).

    \C\<\%(ono\%[remap]\|omap\|noremap\|map\)\>(\@!

### ?

Document this issue: <https://github.com/vim/vim/issues/6374>
Refactor your  text-objects so that  `v:register` is always correctly  passed to
the opfunc.

    xno io iw
    ono io <cmd>exe 'normal vio"' .. v:register<cr>
                               ^--------------^

Note that when `v:register` is evaluated, Vim  is *not* in visual mode.  It's in
command-line mode; `:norm` has not been executed  yet; btw, this is why the last
register has not yet been reset and you can still access it with `v:register`.

See: <https://vi.stackexchange.com/a/20327/17449>

---

Should we do sth similar to pass `v:count` to the opfunc?
The count is lost  when using a custom text-object (only  when it's defined with
`:norm`, right?), regardless of whether the operator is builtin or custom.

   1. builtin operator + a builtin text-object
   2. builtin operator + a custom text-object
   3. custom operator + a builtin text-object
   4. custom operator + a custom text-object

Test 1:

    set showcmd
    pu='aaa bbb ccc ddd'

    " press:  3daw
    " 3 words are deleted ✔

Test 2:

    set showcmd
    pu='aaa bbb ccc ddd'
    xno io iw
    ono io <cmd>norm vio<cr>

    " press:  3dio
    " only 1 word is deleted ✘

Test 3:

    set showcmd
    pu='aaa bbb ccc ddd'
    fu Opfunc(...)
        if !a:0
            let &opfunc = 'Opfunc'
            return 'g@'
        endif
        pu=printf('v:count: %d, v:prevcount: %d', v:count, v:prevcount)
    endfu
    nno <expr> <c-b> Opfunc()

    " press:  3 C-b iw
    " Vim puts the text 'v:count: 3, v:prevcount: 0' ✔

Test 4:

    set showcmd
    pu='aaa bbb ccc ddd'
    fu Opfunc(...)
        if !a:0
            let &opfunc = 'Opfunc'
            return 'g@'
        endif
        pu=printf('v:count: %d, v:prevcount: %d', v:count, v:prevcount)
    endfu
    nno <expr> <c-b> Opfunc()
    xno io iw
    ono io <cmd>norm vio<cr>

    " press:  3 C-b io
    " Vim puts the text 'v:count: 0, v:prevcount: 0' ✘

Answer:

I don't think we need to do sth similar for `v:count`.
The count is only necessary to determine the text on which to operate.
But, once it's done, the change marks are set; and those are not altered.

What do you think?

If you disagree, try this:

    fu Opfunc(...)
        if !a:0
            let &opfunc = 'Opfunc'
            return 'g@'
        endif
        echom printf('v:register: %s, v:count: %d', v:register, v:count)
    endfu
    nno <expr> <c-b> Opfunc()
    xno io iw
    omap <expr> io '<c-\><c-n>vio'
        "\   necessary because of our `nno "" "+` mapping
        "\   v-----------------------v
        \ .. (v:register == '"' ? '' : '"' .. v:register)
        \ .. (v:count ? v:count : '') .. v:operator

Although, this omap doesn't work as expected when repeated with `.`.
It seems we need `:norm` for `.` to work; do we?
Why though?  I mean `:norm vio` also enters visual mode...

##
## Misc.
### ?

Try to use `GetSelectionCoords()` in your plugin(s) instead of escaping.

    ~/.vim/plugged/vim-lg-lib/import/lg.vim

Unless they really  need to update the  visual marks, or you really  want to get
back to normal mode.

    \C\\e\|\c<esc>

---

Also, document this (from `:h line()`):

   > v       In Visual mode: the start of the Visual area (the
   >         cursor is the end).  When not in Visual mode
   >         returns the cursor position.  Differs from |'<| in
   >         that it's updated right away.

Note that  the start of the  selection does not necessarily  match the character
which will be  marked with `'<`; if you're controlling  `'<`, then `getpos('v')`
gives  the  position of  `'>`,  and  vice  versa;  if you're  controlling  `'>`,
`getpos('v')` gives the position of `'<`.

I think "start of the Visual area" in the help means "controlled corner"...

If you want an expression which tells  you whether you're controlling the end of
the selection or its start:

    line('.') > getpos('v')[1] || line('.') == getpos('v')[1] && col('.') >= getpos('v')[2]

### ?

    $ vim
    :h
    C-k
    qq
    ll
    C-j
    ll
    q
    :reg q
    c  "q   ll^@llq~
                  ^
                  ✘

This is documented at `:h q`:

   > q                     Stops recording.  (Implementation note: The 'q' that
   >                       stops recording is not stored in the register, **unless**
   >                       **it was the result of a mapping**)

The issue is  due to the existence of  a custom mapping on `q`,  which feeds `q`
into the typeahead.

Solution:

In `window#quit#main()`, replace this line:

    if reg_recording() != '' | return feedkeys('q', 'in')[-1] | endif

with this block:

    let regname = reg_recording()
    if regname != ''
        call feedkeys('q', 'in')[-1]
        call timer_start(0, {-> setreg(regname, getreg(regname)->substitute('q$', '', ''), 'c')})
        return ''
    endif

Should we wrap that  in a `lg#` function and use it wherever  we've used a local
`q` mapping?
Note that I  don't think that a trailing  `q` has any effect in  a recording; at
least, it doesn't start a new recording.
I think that the special meaning of `q` is disabled while replaying a recording;
maybe because  it would cause an  infinite recursion when pressing  `q` during a
recording.

Bonus question: If we add the `t` flag, why isn't `q` recorded twice?
Answer: I think that the `q` we press interactively is always recorded.
But the one which is fed is never recorded, because it ends the recording.

### ?

Find usage examples for the `!` and `L` flags of `feedkeys()`.

                                 v
    rg 'feedkeys.*[''"][mntLix!]*L[mntLix!]*[''"]' ~/Vcs/vim/src/testdir/
    rg 'feedkeys.*[''"][mntLix!]*![mntLix!]*[''"]' ~/Vcs/vim/src/testdir/
                                 ^

### ?

Move as many comments from `vim-freekeys` here.

### ?

    call setcmdpos(6)

Positionne le curseur juste avant le 6e octet sur la ligne de commande.

Si aucun des  5 premiers caractères de la ligne  de commande n'est multi-octets,
positionne le curseur juste avant le 6e caractère.

Ne fonctionne que lorsqu'on édite la ligne de commande:

   - en y insérant l'évaluation d'une expression via C-r
   - en la remplaçant entièrement par l'évaluation d'une expression via C-\ e

Qd on utilise `C-\ e` ou `C-r =`  pour évaluer une fonction custom, il ne sert à
rien de  demander à cette  dernière de retourner  des caractères de  contrôle tq
`<cr>` pour exécuter  la ligne de commande ou `<Left>`,  `<Right>` pour déplacer
le curseur.

En  effet, `C-\  e` et  `C-r`  ne peuvent  qu'insérer des  caractères, donc  des
caractères de contrôle  seraient insérés littéralement et  non interprétés comme
des commandes.

Si on veut déplacer le curseur sur la ligne de commande après que les caractères
retournés par la fonction custom aient été insérés, il faut utiliser soit:

   - `setcmdpos()` au sein de la fonction custom

   - des `<left>`, `<right>` après que la fonction custom ait été évaluée; pex au sein d'un mapping:

         cno <f8> <c-\>e Func()<cr><left><left>

On ne  rencontrerait pas ce  pb avec un  mapping auquel on  passerait l'argument
`<expr>`,  et auquel  on demanderait  de taper  les touches  retournées par  une
fonction custom.

Dans ce cas,  les touches de contrôle  ne seraient pas insérées sur  la ligne de
commande, mais interprétées comme des actions (validation, mouvement).

Update:  I think that's only true in command-line mode.
In insert mode, you can use `<c-r>=` to return `<left>`, `<right>`, `<bs>`, ...

---

La position du curseur via `setcmdpos()`  n'est pas établie au même moment selon
qu'on utilise `C-r =` ou `C-\ e` / `C-r C-r =`:

   - `C-r =`, après avoir évalué l'expression, *mais avant* de l'insérer

   - `C-r C-r =` et `C-\ e`, après avoir évalué l'expression

### ?

`C-j` (or a NUL) and `C-m` don't make a string end prematurely:

    echo "foo \<c-j> bar"
    foo ~
     bar~

In an `<expr>` mapping, it depends:
```vim
fu Func(str)
    return ''
endfu
nno <expr> cd Func('foo <c-j> bar')
norm cd
```
    ✔
```vim
fu Func(str)
    return a:str
endfu
nno <expr> cd ':call ' .. Func('foo <c-j> bar')
norm cd
```
    E107: Missing parentheses: foo

However, they *can* in a regular mapping:

    fu Func(str)
        echo a:str
    endfu
    nno cd :call Func('foo <c-j> bar')<cr>
    norm cd
    E115: Missing quote: 'foo ~

This  is probably  because  the keys  in  the  rhs are  processed  while on  the
command-line;  and on  the  command-line, when  `C-j` or  `C-m`  is pressed,  it
terminates the command.

### ?

If you wonder whether your chosen lhs is going to override a default command, have a look at these help tags:

   - `:h insert-index`
   - `:h normal-index`
   - `:h visual-index`
   - `:h ex-edit-index`

They list all the default commands in resp. insert/normal/visual/ex mode.

---

- <http://vimcasts.org/blog/2014/02/follow-my-leader/>
- <https://vimeo.com/85343734>

You could want to create 3 types of lhs:

   - one calling a function or command
   - an operator
   - a text-object

You could divide the keys on the keyboard in 4 categories:

   - motion      ' ` # $ % ^ *  ( ) 0 _ - + w W  e E t T { } [ ] f F G h H j k l L , ; | b B n N M ? /
   - command     a A C D i I J K m o O p P q Q r R s S u U v V x X Y Esc ~ @ & : .
   - operator    c d y = < > !
   - prefix      g z Z ' " \ Ctrl [ ]

To build  a lhs which won't  override a default  command, you can make  it begin
with a prefix.

E.g.:

   - `gl` (vim-lion)
   - `gc` (vim-commentary)

Or choose a syntax which doesn't make sense to Vim.
Use an operator then a command.  E.g.:

   - `cx`    vim-exchange; exchange the position of 2 text-objects
   - `ys`    vim-surround; surround a text-object with some character

It's an  invalid syntax, because an  operator only manipulates a  text-object or
the text covered by a motion.
You can use any command, except `a` and `i` because those are commonly used as a
prefix to create text-objects (`iw`, `ap`, ...).

Use an operator than a prefix.  E.g.: `cz`, `dgb`

Use 2 operators.  E.g.: `cd`, `cu`, `y=`

Note that  `op1 + op2` doesn't make sense  only if there's no  text-object using
`op2` as its lhs.
If `op2` only uses one character, this is not an issue, because there aren't any
operator and text-object using the same 1-char lhs.
For example, there is a `c` operator, but there is no `c` object.
In fact, there is no one-character text-object.

I think this is because it would  violate the convention which makes an operator
repeated twice is equivalent to making it operate on the current line.
For example,  if the  `d` text-object  existed, then `dd`  would not  delete the
current line anymore, but whatever text is targeted by this `d` object.

If `op2` contains several characters, then `op1 + op2` may be valid or not.

      Qd l'opérateur2 utilise plusieurs caractères, le pb peut se poser (cf `gc`), ou pas (`gl`).

      Pex, vim-commentary crée l'opérateur et l'objet `gc`.
      De fait, on ne pourrait donc pas utiliser `dgc` comme un lhs.
      Malgré cela, l'opérateur `gc` peut agir sur la ligne courante via une forme de répétition.
      En effet, une 2e convention veut que lorsqu'un opérateur utilise 2 caractères,
      il peut agir sur la ligne courante si on le répète intégralement (plus possible avec `gc`),
      ou bien si on répète seulement son 2e caractère (`gcc` est tjrs dispo et Tim Pope l'a
      correctement défini).

      En revanche, vim-lion ne crée pas d'objet `gl`, on pourrait donc utiliser `dgl` comme lhs.

... ou encore un lhs valide mais peu utile car il existe un synonyme:

   - `C-n`
   - `C-p`
   - `+`
   - `-`
   - `s`
   - `S`
   - ...

Pex, dirvish/vinegar remap `-` car `k` fait pratiquement la même chose et est plus utilisé.
sneak remap `s` et `S` car ils sont peut utilisés et `cl`/`cc` sont des synonymes.
`gs` est aussi un bon candidat, car peu utile en général.

On  peut utiliser  ces  méthodes pour  créer  non  pas un  lhs  mais un  nouveau
namespace  à l'intérieur  duquel on  créera des  mappings similaires  (ex: `co`,
`[o`, `]o` dans unimpaired).

---

Qd on cherche un lhs pour un objet, généralement son début suit un des patterns suivants:

   - cmd1 + cmd2
   - cmd  + opérateur
   - cmd  + mouvement
   - cmd  + namespace

`cmd1` étant très souvent `i` ou `a`.
En théorie, on pourrait aussi le faire  commencer par le lhs d'un opérateur (ex:
`gc`), mais  parfois ça pourrait introduire  du lag (`gcgc` vs  `gcgcfoo`) ou un
namespace.

Pour des exemples, lire:

- <https://github.com/kana/vim-textobj-user/wiki>
- <https://github.com/wellle/targets.vim>

---

Certaines  commandes   normales  sont  pensées  pour   être  outrepassées:  `gq`
('formatprg'), `=` ('equalprg') D'autres peuvent être étendues.
Pex, `z=` ne fonctionne que si `'spell'` est activée.
On  pourrait lui  faire qch  (de similaire)  qd l'option  est désactivée,  comme
suggérer des synonymes du mot sous le curseur.

---

Vim ne définit aucun mapping contenant des chiffres à l'exception de:

   - 0 C-d (insert mode)
   - g0
   - g8
   - 8g8

---

Some key sequences can begin with one  of 2 symmetrical characters, such as `[`, `]`.
Don't use them to perform completely unrelated actions.
You would lose the symmetry.
Use them to perform reverse operations.

There can even be a set of more  than 2 characters, which by default are related
in some way; for example, `<`, `=`,  `>` all operate on the level of indentation
of some lines.
So, they  could be  used as prefixes  to build 3  mappings, performing  3 custom
related operations, provided by your plugin.

---

You can check whether a key sequence  is already bound to some default action in
Vim, by looking at the output of:

    :echo taglist('^<keys>')
    :echo taglist('^<keys>')->map('v:val.name')

Output example when `<keys>` = `g CTRL-`

    ['g_CTRL-A', 'g_CTRL-G', 'g_CTRL-H', 'g_CTRL-]'~

FIXME: I think the output of `taglist()` is influenced by the current buffer.
Because it must look  in tags files, and those are set  by a buffer-local option
(`'tags'`); to be checked.

### ?

We haven't seriously taken into account `:redraw`: `:h :echo-redraw`.
Maybe we should have used `:redraw` more often before an `:echo`.

<https://github.com/google/vim-searchindex/blob/28c509b9a6704620320ef74b902c064df61b731f/plugin/searchindex.vim#l187-l189>

### ?

    $ vim -Nu <(cat <<'EOF'
        set lz
        nmap n <plug>(a)<plug>(b)
        nno <plug>(a) n
        nno <plug>(b) <nop>
    EOF
    ) +"pu=repeat(['some text'], &lines)"

Search for `text`, then press `n` a few times: the cursor does not seem to move.
In reality, it does move, but you don't see it because the screen is not redrawn
enough; press `C-l`, and you should see it has correctly moved.

It think that's because when `'lz'` is  set, Vim doesn't redraw in the middle of
a mapping.  Indeed, if you reverse the order of the `<plug>` mappings, the issue
disappears:

    $ vim -Nu <(cat <<'EOF'
        set lz
        nmap n <plug>(a)<plug>(b)
        nno <plug>(a) <nop>
        nno <plug>(b) n
    EOF
    ) +"pu=repeat(['some text'], &lines)"

### ?

Maybe we  should document  here that if  we press `C-c`  to interrupt  a mapping
which takes a long time to be  processed and is followed by `<c-r>=`, the latter
(and everything which follows?) is literally dumped into the buffer.

See this question in `config.md`:

    ## Document that restoring an option after `CompleteDone` is not reliable.
    ### Why not
    #### saving and restoring the option with 2 `C-r = Func()`?

MWE:

    $ vim -Nu NONE +"ino <c-z> <c-x><c-k><c-r>=''<cr>" +'set dict=/usr/share/dict/words' +startinsert
    C-z
    C-c
    AA=''~
      ^^^

Btw, try  to understand why that  happens, and check  whether there is a  way to
prevent it.

##
##
##
# Arguments
## Which mappings should *never* be defined with `<silent>`?

Any mapping in command-line mode.

First, it doesn't make sense.
`<silent>` is  useful to prevent  Vim from printing an  Ex command which  is run
after entering the command-line from the rhs of the mapping:

        v------v
    nno <silent> cd :call Func()<cr>
    fu Func()
        " ...
    endfu

This is  useless for a  command-line mode mapping,  because you can't  enter the
command-line from it; you're *already* on the command-line.

Second, it prevents the command-line from being redrawn:

    $ vim -Nu NONE +'cno <silent> <c-z> <c-b>'
    " enter the command-line
    " insert some text
    " press `C-z` to jump to the start of the command-line: the cursor seems to have stayed where it was
    " press `Right`: the cursor is now on the second character of the line
      (which means that it was previously – and correctly – at the start)

## Should I use `<silent>` with `<expr>`?

It depends on whether the rhs expression returns a `:` which enters the command-line.

If it does,  you probably want `<silent>`.
Unless, the goal is to populate the  command-line, but not execute a command; in
that case, you don't want `<silent>`.

Otherwise, you don't need `<silent>`.

##
## <expr>

    cno <f7> <c-\>e getcmdline()->escape(' \')<cr>

`<f7>` échappe tous les espaces et les backslash sur la ligne de commande.

`<c-\>e` est une commande permettant de remplacer toute la ligne de commande par
l'évaluation d'une expression.

Elle  est particulièrement  utile  dans  le rhs  d'un  mapping  `:cno` ou  d'une
abréviation `:cnoreabbrev`.

---

`<expr>` est plus puissant pour 2 raisons:

   - il permet de remplacer toute ou partie de la ligne de commande (`c-\ e`
     seulement tout)

   - il permet de simuler des frappes au clavier et donc d'effectuer des actions
     sur la ligne de commande contrairement à `c-\ e` qui ne peut qu'insérer des
     caractères

Ex: on peut demander  à appuyer sur la touche `<up>`  pour rappeler le précédent
item dans l'historique.
On peut aussi directement se déplacer sur la ligne de commande via des `<left>`,
`<right>`.
Tandis qu'avec `c-\ e` , le seul moyen de se déplacer est d'envelopper l'expression
dans  une fonction  custom qui  appellera  `setcmdpos()` avant  de retourner  le
contenu de la nouvelle ligne de commande.

---

Toutefois `c-\ e` est spécial.

Dans un mapping, `<expr>`, `<c-r>=`, et `:exe` ajoute du texte.
`c-\  e` n'est  dispo  qu'en mode  ligne  de  commande, et  ne  se contente  pas
d'ajouter du texte.
Il  revient en  arrière pour  analyser tout  ce  qu'on a  tapé sur  la ligne  de
commande.
Aucun autre mapping/argument/commande ne permet un retour en arrière.
On peut simuler `c-\  e` via `<expr>` en ajoutant au  début du rhs: `<c-e><c-u>`
Mais c'est plus moche.

---

    cnorea <expr> e               getcmdtype() ==# ':' && getcmdpos() == 2 ? 'E'  : 'e'
    cnorea        e         <C-R>=getcmdtype() ==# ':' && getcmdpos() == 1 ? 'E'  : 'e'<cr>
    cno    <expr> e<space>        getcmdtype() ==# ':' && getcmdpos() == 1 ? 'E ' : 'e '
    cno           e                                                           E

Ces 4 commandes ont pour but de remplacer automatiquement la commande `:e` par `:E`.

La 1e syntaxe est la meilleure car:

  - développement que lorsque l'abréviation est seule (pas à la fin d'un mot)
  - développement qu'après un trigger (caractère non keyword, pex espace ou C-])

La 2e syntaxe est bien mais plus verbeuse.

La 3e syntaxe n'est pas bonne car:

  - elle n'est pas développée à la fin d'un mot
  - on perd le trigger `c-]`
  - l'espace doit être tapé avant le timeout; avec une abréviation, pas de timeout.

La 4e  syntaxe est la  pire car le développement  est effectué n'importe  où (en
début de mot, à la fin, au milieu ...).

---

Dans  un mapping,  on ne  devrait  pas utiliser  l'argument `<expr>`  si le  rhs
contient une commande Ex.
Pk?
Esthétiquement, voir des `':'`,  `"\r"` fait moche (et rend le  code un peu plus
long); préférer:

   - `<c-r>=`
     pour insérer l'évaluation d'une expression

   - `exe test ? cmd1 : cmd2`
     pour évaluer et exécuter une expression dont le résultat est une commande Ex

   - `<c-\>e`
     pour remplacer la ligne de commande par l'évaluation d'une expression

Exception: qd  la commande Ex  appelle un  `input()`, et que  d'autres commandes
suivent,  `<expr>`  empêche  ce  dernier  de consommer  les  caractères  de  ces
dernières.

## <plug>

    fu Reminder(cmd)
        " erase the input before displaying next message
        redraw
        echohl WarningMsg | echo '[' .. a:cmd .. '] was equivalent' | echohl NONE
    endfu

    nno <plug>(reminder) <cmd>call input('')->Reminder()<cr>

    "                         ┌ appelle la fonction
    "                         │               ┌ passe-lui cet argument
    "                         │               │    ┌ termine/valide la saisie
    "                         ├──────────────┐├───┐├──┐
    cnorea <expr> vs 'vs' .. feedkeys('<plug>(reminder)C-w v<cr>')[-1]
    cnorea <expr> sp 'sp' .. feedkeys('<plug>(reminder)C-w s<cr>')[-1]

Ce snippet  illustre qu'on peut  passer un  argument arbitraire à  une fonction,
même si elle est appelée depuis un mapping `<plug>`.

Ce qui peut étonner, c'est d'utiliser `input()`, qui en tant normal est utilisée
pour permettre à l'utilisateur de saisir du texte arbitraire.

Ici, son usage est détourné.
Pour mieux comprendre, revenons à `<plug>(...)`.
Pk utiliser ce genre de mapping? Il peut y avoir plusieurs raisons:

   - fournit une abstraction simple, et facile à manipuler

   - utile pour exécuter une fonction via `feedkeys()`
     (ex: vim-repeat)

   - permet d'appeler une fonction locale à un script depuis un autre script
     (`<plug>(...)` est une forme d'interface publique)

Mais  `<plug>(...)` peut  poser un  pb.   Si on  doit  passer un  argument à  la
fonction, comment faire?  On pourrait créer un mapping `<plug>(...)` pour chaque
valeur d'argument valide, mais que faire s'il y en a trop?

La solution est décomposable en 2 étapes:

   1. écrire notre argument dans le typeahead buffer juste après `<plug>(...)`

   2. utiliser `input('')` au sein de la fonction invoquée par `<plug>(...)`,
      pour lui demander de consommer l'argument

Toute la raison d'être de `input('')` est  de forcer la fonction à consommer les
touches qui  suivent `<plug>(...)`.  Sans  elle, la fonction les  ignorerait, et
Vim les exécuterait dans le mode courant (mode normal en général).

---

C'est ce genre de mécanisme que vim-surround utilise dans un mapping tq `ds(`.
Le plugin installe un mapping qui:

   - utilise `ds` comme lhs
   - demande à l'utilisateur de fournir un caractère (via `getchar()`)
   - appelle une fonction en lui passant ce caractère

---

On aurait pu déplacer `input()` au sein même de `Reminder()`:

    fu Reminder()
        let cmd = input('')
        redraw
        echohl WarningMsg | echo '[' .. cmd .. '] was equivalent' | echohl NONE
    endfu

    nno <plug>(reminder) <cmd>call Reminder()<cr>

    cnorea <expr> vs 'vs' .. feedkeys("<plug>(reminder)C-w v<cr>")[-1]
    cnorea <expr> sp 'sp' .. feedkeys("<plug>(reminder)C-w s<cr>")[-1]

Update:  These snippets work as expected when we press Enter right after `:vs` or `:sp`.
But they don't work as expected when we insert a space after `:vs` or `:sp`.

## <script>

    nno    <script>     ,dt                <SID>(FindTopic)dd
    nno                <SID>(FindTopic)    /Topic<cr>

    nno                 dd                 <cmd>call Func()<cr>

Ces 3 mappings  illustrent l'utilité de l'argument `<script>`  dans une commande
de mapping.  Par défaut, on peut autoriser  ou interdire le remap de tout le rhs
en utilisant (ou pas) le mot-clé `nore` (nmap vs nnoremap).

Mais, si on veut autoriser le remap d'une  partie du rhs et pas du reste, `nore`
ne fonctionne pas.
C'est là que `<script>` intervient.
`<script>` ne remap qu'une suite de caractères commençant par `<SID>`.
Il ne peut donc pas tenir compte des mappings définis dans un autre script.
En effet, `<SID>` est automatiquement traduit en un identifiant unique au script
(`<SNR>123_`).
Un mapping défini  dans un autre script  ne peut pas avoir son  lhs identique au
`<SID>` du script courant.

Dans l'exemple  précédent, les 2 premiers  mappings sont définis dans  un script
(plugin pex).  Le 3e est défini dans un autre fichier (vimrc utilisateur pex).

Le  1er  mapping a  besoin  que  `<SID>(FindTopic)`  soit  remap, de  sorte  que
lorsqu'on tape `,dt`, Vim cherche le mot `Topic`.
Le rhs de ce mapping se termine par  `dd` car il veut ensuite supprimer la ligne
où se trouve `Topic`.

Cela pose  un pb,  car l'utilisateur  peut avoir  remap `dd`  pour faire  qch de
totalement différent, comme appeler une fonction custom.
Le pb est cependant résolu par `<script>`  qui n'autorisera pas le remap de `dd`
car il ne commence pas par `<SID>`.

---

`<script>` a priorité sur le mot-clé `nore`.
On peut donc écrire `nnoremap <script>` ou `nmap <script>` indifféremment.
Toutefois, comme `<script>`  interdit en grande partie tout  remap, on préfèrera
`nnoremap <script>` pour gagner en lisibilité.

---

Dans la table  des mappings, `<script>` est signalé via  le caractère `&`, juste
avant le rhs.

---

On pourrait se passer de `<script>` et utiliser un `<plug>` à la place:

    nmap ,dt                    <SID>(FindTopic)<Plug>(norecursive_dd)
    nno  <Plug>(norecursive_dd)  dd
    nno  <SID>(FindTopic)        /Topic<cr>

Mais on doit écrire une ligne de code supplémentaire, et on perd en lisibilité.

## <unique>

    nno <unique> cd <cmd>echo 'hello'<cr>

`<unique>` ne créera le mapping que si aucun autre mapping n'utilise `cd` comme lhs.

La vérification portera à la fois sur les mappings globaux et locaux.
Donc, les 2 cas de figure suivants échoueront:

    nno                    cd  <cmd>echo 'hello'<cr>
    " ✘
    nno  <buffer><unique>  cd  <cmd>echo 'world'<cr>

    " ✘
    nno  <buffer>          cd  <cmd>echo 'hello'<cr>
    nno          <unique>  cd  <cmd>echo 'world'<cr>


---

Avantage `<unique>`:

   - peu verbeux

Inconvénient `<unique>`:

   - soulève E227 en cas de conflit

Avantages `mapcheck()`:

   - vérifie  non seulement que le lhs n'est pas utilisé,
     mais en plus qu'il ne provoquera pas de lag

   - `if mapcheck()->empty()|...|endif`  ne soulève aucun message d'erreur
     car le mapping n'est pas installé en cas de conflit

Inconvénients `mapcheck()`:

   - verbeux

   - lent (car il faut une invocation de fonction par mapping)

Conseils:

   - n'utiliser aucun des 2 dans `vimrc`, les ftplugins, et plus généralement
     pour tout mapping local à un buffer

   - utiliser `<unique>` dans nos plugins privés

   - utiliser `mapcheck()` dans nos plugins publics

##
# lhs

    if mapcheck('<key>', 'n')->empty() && !hasmapto('<Plug>(plugin_some_func)', 'n')
        nno <key> <Plug>(plugin_some_func)
    endif
    nno <Plug>(plugin_some_func) <cmd>call SomeFunc()<cr>

Définit un mapping appelant `SomeFunc()`.

À la place de `<plug>(plugin_some_func)` on pourrait utiliser autre chose, comme
pex `SPC x`, mais dans ce cas on consommerait un mapping existant.
`<plug>` correspond à un  key code qu'il est impossible de  taper au clavier, ce
faisant on ne consomme aucun mapping.

---

Quel intérêt de “casser“ un mapping en deux comme cela ?
Pour le moment, j'en vois 3:

   - simplification
   - normalisation
   - répétition

La  simplification permet  à  l'utilisateur  de manipuler  un  rhs  au nom  plus
évocateur, et de masquer la complexité de la fonctionnalité (≈ abstraction):

    <plug>(plugin_some_func)

La normalisation permet de  vérifier si oui ou non l'utilisateur  a déjà map une
touche à la fonctionnalité offerte par le rhs (`hasmapto('<plug>(...)')`):

    nmap <key> <plug>(plugin_some_func)

Enfin, il est ainsi possible de créer  un mécanisme qui répète le mapping et qui
est indépendant du lhs choisi par l'utilisateur (voir `mucomplete`).

---

Malgré qu'on ait cassé notre mapping en 2 étages, `<c-u>` est tjrs utile.
Si on frappe accidentellement un nb  avant le lhs, `:call MyFunc()` recevra tjrs
une rangée; `<c-u>` permet dans ce cas de l'éliminer.

---

Il  semble qu'un  seul `<silent>`  soit  suffisant, pour  qu'un enchaînement  de
mappings soit silencieux.
Généralement, on le met sur le 2e, celui où le `<plug>` est à gauche, et dont le
rhs contient le code qui nous intéresse.
Ce faisant,  on s'assure que la  mapping sera silencieux, que  l'utilisateur est
utilisé `<silent>` dans le 1er étage du mapping ou pas.

---

Qd  l'auteur d'un  plugin dispose  d'une fonctionnalité  dont il  pourrait faire
profiter ses  utilisateurs via un  mapping, s'il veut déranger  l'utilisateur un
minimum, il y a 3 conditions qu'il pourrait vérifier avant de l'installer:

   - l'utilisateur a donné son accord

     Généralement, les auteurs de plugin  choisissent un système en opt-out (les
     mapping sont installés par défaut).
     Et ils désactivent les mappings qd  la valeur d'une variable globale ad hoc
     est différente de 0.

   - le mapping ne remplacera aucun mapping préexistant, ni n'introduira du lag

   - l'utilisateur n'a pas déjà map la fonctionnalité à une touche

Exemple d'installation d'un mapping vérifiant ces 3 conditions:

    if !exists('g:mappings_disabled') || !g:mappings_disabled
        if mapcheck('<key>', 'n')->empty() && !hasmapto('<Plug>(plugin_some_func)', 'n')
            nmap <key> <Plug>(plugin_some_func)
        endif
    endif

# rhs

When the  rhs of a mapping  executes a sequence  of normal commands, and  one of
them fails, the remaining ones are not executed.

Example:

    nno <key> <c-w>w<c-d><c-w>w

When you have 2 windows, this mapping should:

   1. focus the inactive window (`C-w w`)
   2. scroll half-a-page down (`C-d`)
   3. focus back the original window (`C-w w`)

Most of the time, it will work as expected.
But not when the cursor is already at the bottom of the inactive window.
In that case, `C-d` will fail to scroll, and Vim won't focus back the original window.

Solution:

    nno cd <cmd>sil! exe "norm! \<lt>c-w>w\<lt>c-d>\<lt>c-w>w"<cr>

`:silent!` makes Vim ignore any error raised by `:norm`.

`<lt>` is  necessary to  prevent Vim  from translating  `<c-w>` in  the mappings
table before `:exe` is run.
If `<c-w>` is  translated directly in the mappings table,  then Vim will execute
it on  the command-line  with its default  meaning which is  to delete  the word
before the cursor (`:h c^w`).

You  can  use multiple  `<lt>`'s  to  prevent  a  control character  from  being
translated, as many times as necessary:

    nno cd :echo "\<c-w>"<cr>
    call feedkeys('cd')
    E115: Missing quote: "~

    nno cd :echo "\<lt>c-w>"<cr>
    call feedkeys('cd')
    ^W~

    nno cd :echo "\<lt>lt>c-w>"<cr>
    call feedkeys('cd')
    <c-w>~

Here, `<lt>lt>` prevents the translation of  `<c-w>` twice (once by `:nno`, once
by Vim when evaluating the double-quoted string).
Note that this  is a contrived example;  if all you wanted was  to echo `<c-w>`,
you could just write:

    nno cd :echo '<lt>c-w>'<cr>
    call feedkeys('cd')
    <c-w>~

Update: Now that we have `<cmd>`, it *seems* that this is irrelevant.

    nno cd <cmd>echo '<c-w>'<cr>
    call feedkeys('cd')
    <c-w>~

But it's not:

    nno cd <cmd>echo '<up>'<cr>
    call feedkeys('cd')
    E1137: <Cmd> mapping must not include <Up> key~

    nno cd <cmd>echo '<lt>up>'<cr>
    call feedkeys('cd')
    <up>~

---

But `:silent!` does *not* make Vim ignore errors raised by other commands, like `:call`:

    nno cd <cmd>sil! call UnknownFunc() <bar> let g:d_var = 1<cr>
    " press:  cd
    " run:  :echo g:d_var
    " result:    E121
    " expected:  1 is printed

    nno cd <cmd>sil! 999999d <bar> let g:d_var = 1<cr>
    " press:  cd
    " run:  :echo g:d_var
    " result:    E121
    " expected:  1 is printed

Why?
Is it because of this:
<https://github.com/neovim/neovim/issues/11136#issuecomment-537253732>
You may think it's because for `silent!` to  work, it needs to be applied to the
whole rhs.  That's not true:

    nno cd <cmd>sil! exe 'call UnknownFunc() <bar> let g:d_var = 1'<cr>
    " press:  cd
    " run:  :echo g:d_var
    " result:    E121
    " expected:  1 is printed

I think it only works for `:norm`...

In any case, as a workaround, use `:exe`:

                vvv
    nno cd <cmd>exe 'sil! call UnknownFunc()' <bar> echom 'processed'<cr>

---

    nno cd <cmd>let msg = input('') <bar> echo ' bye'<cr>hello

Why does `input()` consume `hello`, but not `echo 'bye'`?

Because for `input()` to be invoked, `<cr>` must be executed.
When that happens, `<bar> echo ' bye'` has already been executed.

    typeahead                                       | command-line
    --------------------------------------------------------------
    cd                                              |
    :let msg = input('') <bar> echo ' bye'<cr>hello |
     let msg = input('') <bar> echo ' bye'<cr>hello | :
      et msg = input('') <bar> echo ' bye'<cr>hello | :l
       t msg = input('') <bar> echo ' bye'<cr>hello | :le
         msg = input('') <bar> echo ' bye'<cr>hello | :let
    ...
                                              hello | :let msg = input('') <bar> echo ' bye'<cr>

When `<cr>` is executed, the  command-line is executed, which invokes `input()`,
which in turn consumes whatever is in the typeahead buffer (here `hello`).

# Objets

    xno {object} {motion}
    ono {object} <cmd>norm v{object}<cr>

Définit un nouvel objet dont les caractères sont couverts par `{motion}`.

---

Si le rhs du mapping `:xno` n'est pas un mouvement, mais l'appel à une fonction,
on peut le réutiliser pour le mapping `:ono`:

    xno {object} <cmd>call MyFunc()<cr>
    ono {object} <cmd>call MyFunc()<cr>

Si le  rhs du mapping `:xno`  est un mouvement,  pk ne peut-on pas  lui-aussi le
réutiliser dans `:ono`?
Car on est en mode operator-pending.
Il faut  soit le  quitter via  `<Esc>`, soit  passer en  mode ligne  de commande
(`:`), pour appeler une fonction (`:call`) ou exécuter une commande (`:norm`).
Le but étant de sélectionner le texte sur lequel doit agir l'opérateur.

---

Si on fait  commencer le rhs du  mapping `:ono` par un escape,  non seulement on
quitte le  mode operator-pending pour  revenir en mode  normal, mais en  plus on
annule l'opération.
Ça signifie qu'il  faut appeler le bon opérateur soi-même  via `v:operator` à la
fin du rhs, une fois que le texte a été sélectionné.

---

On pourrait remplacer le mapping `:ono` par celui-ci:

    :omap <expr> {object} '<Esc>' .. 'v{object}' .. v:operator

   - `<Esc>`       revenir en mode normal
   - `v{object}`   sélectionner l'objet
   - `v:operator`  agir dessus

Mais  la récursivité  de  `:omap`,  qui est  nécessaire  pour remap  `{object}`,
affecterait tout le rhs (et non juste `{object}`) et pourrait donc avoir parfois
des effets inattendus.
De plus, `v:operator` ne semble pas  enregistrer un opérateur custom (ex: `cs` =
change surroundings).

---

    ono <expr> w v:operator ==# 'd' ? 'aw' : 'iw'

Crée l'objet `w` qui se comporte  comme `aw` lorsque l'opérateur qui précède est
`d`, `iw` autrement.

`v:operator` was first seen here: <https://vi.stackexchange.com/a/6518/17449>

The original code was (unnecessarily?) more complex.

---

    ono Ob) <cmd>norm! vib``<cr>
    ono Oe) <cmd>norm! vibo``<cr>

Crée  l'objet allant  du  curseur jusqu'au  début  / à  la fin  de  la paire  de
parenthèses à l'intérieur desquelles il se situe.

Illustration:

             cursor is here
             v
    func1(foo|, func2(), bar);
          ^-^
          text yanked if you press `yOb)`

    func1(foo|, func2(), bar);
              ^------------^
          text yanked if you press `yOe)`

Ceci  illustre également  que, si  on  divise un  text-object en  2 parties,  la
position du curseur  étant la limite entre  les 2, on peut  cibler ces dernières
via 2 autres text-objects.

Pour  ce  faire, on  utilise  le  fait que  qd  on  sélectionne visuellement  un
text-object, le curseur  se positionne automatiquement sur  le dernier caractère
de ce dernier.
Ça crée un saut,  une entrée est ajoutée dans la jumplist et  la marque `''` est
posée à l'endroit où se trouvait le curseur initialement.

On peut ainsi “diviser“ le text-object en 2 parties en utilisant la marque `''`.

# Récursivité

Les mappings récursifs peuvent être parfois complexes à comprendre.
Voici qques exemples, ainsi qu'une description de leur traitement par Vim.

    nmap <expr>  N               FuncA()
    nno  <expr>    <plug>(one)   FuncB()
    nno          ge<plug>(one)   <cmd>echo 'world'<cr>

    fu FuncA()
        return "ge\<plug>(one)"
    endfu

    fu FuncB()
        echo 'hello'
    endfu

    norm N
    world~

Qd `N` est tapé, il n'y a  aucune ambigüité, car aucun autre mapping ne commence
par `N`; `N` est donc développé en la sortie de `FuncA()`: `ge<plug>(one)`

Le 1er mapping `N` est récursif, donc Vim cherche à remap tout ou partie du développement.
Il voit le 3e mapping `ge<plug>(one)`, et redéveloppe donc en `:echo 'world'<cr>`.
Ce qui affiche la chaîne `world`.

---

    nmap  <expr>  N              FuncA()
    nno   <expr>   <plug>(one)   FuncB()
    nno           N<plug>(one)   <cmd>echo 'world'<cr>

    fu FuncA()
        return "N\<plug>(one)"
    endfu

    fu FuncB()
        echo 'hello'
        return ''
    endfu

    call feedkeys('N')
    hello + timeout~
    NOTE: `norm N` ne reproduit pas le timeout, taper N, ou utiliser `feedkeys()`

Qd `N` est frappé, il y a ambigüité, car Vim ne sait pas si on tente de taper le
1er ou 3e mapping.
Il attend pour nous laisser le temps  de taper `<plug>(one)`, ce que bien sûr on
ne peut pas faire.
Après le timeout, il comprend qu'on tape  le 1er mapping, et développe `N` en la
sortie de `FuncA()`: `N<plug>(one)`

Comme le mapping est récursif, Vim cherche à développer davantage.
Il devrait développer `N<plug>(one)` en `:echo 'world'`, mais ne le fait pas.
Pk?
Probablement car le lhs (`N`) est répété au début du rhs.
Extrait de `:h recursive_mapping`:

   > If the {rhs} starts with {lhs}, the first character is not mapped again.

Donc, Vim ne veut en aucune manière remap `N`.
En revanche, il peut remap le reste `<plug>(one)`, ce qu'il fait en utilisant le
2e mapping.
Ainsi, il développe `<plug>(one)` en la sortie de `FuncB()`, à savoir rien.
Mais pendant l'évaluation, il est amené à afficher `hello`.

---

    nmap <expr> cd              FuncA()
    nmap <expr>   <plug>(one)   FuncB()
    nno         cd<plug>(one)   <cmd>echo 'world'<cr>

    fu FuncA()
        return "cd\<plug>(one)"
    endfu

    fu FuncB()
        echo 'hello'
        return ''
    endfu

    call feedkeys('cd')
    ∅ + timeout~

Qd on tape `cd`, il y a ambigüité: 1er ou 3e mapping?
Vim attend jusqu'au timeout.
Puis, il développe `cd` en la sortie de `FuncA()`, `cd<plug>(one)`.

Le 1er mapping est récursif, donc Vim cherche à remap le développement.
Il exclut `cd` du remap car il s'agit du lhs qui est répété au début du rhs.
See: `:h recursive_mapping`.
Il pourrait développer `<plug>(one)` en la  sortie de `FuncB()`, mais ne le fait
pas.
Pk?
Car `cd` est une séquence invalide.
Vim  abandonne  le traitement  d'un  mapping  dès  qu'il  en rencontre  une.
See `:h map-error`.

---

Le fait que  `hello` n'est pas affiché suggère que  `cd` est tapé immédiatement,
*avant* même de développer le `<plug>`.
On peut le vérifier en ajoutant:

    let g:myvar = 1    dans FuncA()
    let g:myvar = 2    dans FuncB()

`echo g:myvar` affichera 1.

À  retenir: Vim n'attend  pas d'avoir  absolument tout  développé pour  taper le
développement d'un mapping récursif.
Dès qu'il trouve qch de non-récursif, il le tape.

---

    nmap cd bcd

Qd  le  lhs  d'un mapping  récursif  se  répète  dans  le rhs,  en  général,  le
développement se répète indéfiniment jusqu'à rencontrer une erreur.
C'est pourquoi, dans cet exemple, si  on tape `cd`, le curseur retourne jusqu'au
début du buffer.

Toutefois, il y a 3 exceptions qui empêchent un développement infini:

   - la répétition a lieu dans un mode différent

         nmap cd acd
                 │
                 └ fait passer en mode insertion, mais le mapping travaille en mode normal

   - la répétition se produit au début du rhs

         nmap ge geb

   - la répétition est le préfixe d'un autre mapping

         nmap ge   y#geb
         nno  geb  <nop>

Pour plus d'infos, lire `:h recursive_mapping`.

# Retardement

    fu Func()
        " ✘ E523: Not allowed here
        -pu=123
        return 'dd'
    endfu

    nno <expr> cd Func()
    fu Func()
        " ✔
        call timer_start(0, {-> execute('-pu=123')})
        return 'dd'
    endfu

    nno <expr> cd Func()
    nno <plug>(put_123) <cmd>-pu=123<cr>
    fu Func()
        " ✔
        call feedkeys("\<plug>(put_123)")
        return 'dd'
    endfu

On peut vouloir retarder l'exécution d'une commande.

C'est le cas si  elle modifie le buffer, mais qu'elle  doit être exécutée depuis
une fonction utilisée dans le rhs d'un mapping `<expr>`; le texte est verrouillé
tout au long du traitement d'une telle fonction.

Solution: retarder  l'exécution de la  commande, jusqu'à ce que  le verrouillage
soit levé.

On peut utiliser un timer, ou  bien invoquer la fonction `feedkeys()` à laquelle
on passera en seul argument un mapping `<plug>(...)`.

Concernant les flags de `feedkeys()`:

   - `i`: qu'on l'utilise ou pas, `dd` est exécutée *avant* `<plug>(...)`

   - `n`: pas possible, car on a besoin que `<plug>(...)` soit développé

   - `t`: utile qd les touches contiennent des commandes manipulant des plis,
     l'undo tree, le wildmenu ...

You may wonder why `dd` is  executed before `<plug>(...)` even when `feedkeys()`
receives the `i` flag.

Here's what – I think – happens:

    typeahead           | executed
    ---------------------------------
    cd                  |
    Func() is evaluated |
    dd<plug>(put_123)   |

Bottom line:

   - when `feedkeys()` is  invoked, the typeahead buffer is empty;  so it
     doesn't matter whether you use the `i` flag or not

   - then, `dd` is *inserted* and not appended; probably because the evaluation
     of `Func()` is meant to replace `cd` which originally was at the *start* of
     the typeahead

Note that we can observe the same results when replacing `<expr>` with `@=`:

     nno cd @=Func()<cr>
     nno <plug>(put_123) <cmd>-pu=123<cr>
     fu Func()
         call feedkeys("\<plug>(put_123)")
         return 'dd'
     endfu

But this time, I think the explanation is different:

    typeahead           | executed
    ---------------------------------
    cd                  |
    @=Func() CR         |
                        | @=Func() CR
    <plug>(put_123)     | dd
                          ^^
                          executed immediately

Yeah, `dd`  is really executed  immediately; it's  not written in  the typeahead
buffer; there's no need to, since the keys are not checked for remapping.
Watch this:

    nmap cd @='cD'<cr>
    nno cD <cmd>echom 'test'<cr>
    " press cd:  'test' is not printed

In this  last example,  if `cD`  was remapped after  pressing `cd`,  then `test`
would be printed.  That's not the case.

Remember: remapping only occurs in the typeahead buffer.
When `@=cD<cr>` is executed, `cD` is *not* in the typeahead buffer anymore.

Also,  note that  when `@='cD'<cr>`  is  in the  typeahead buffer,  `cD` is  not
remapped using  the second  mapping; that's  because the  second mapping  is for
normal mode, while `cD` is on the  expression command-line (and thus can only be
remapped by command-line mode mappings).

---

Suppose  we want  to (ab)use  an  abbreviation to  make Vim  print some  message
whenever we run the command `:update`.

So, we write this:

    cnorea <expr> update 'update' .. feedkeys(":echo 'hello'\r", 'i')[-1]

Instead of printing `hello`, after executing `:update`, Vim executes this:

    :update:echo 'hello'

What's the fix?

Answer: don't pass the `i` flag to `feedkeys()`.

    cnorea <expr> update 'update' .. feedkeys(":echo 'hello'\r")[-1]

How does this work?

With the `i`  flag, `:echo 'hello' CR`  was inserted too early;  i.e. before the
carriage return typed interactively to execute `:update`:

    typeahead           | executed
    ------------------------------
    u                   | u
    p                   | p
    d                   | d
    ...                 | ...
    e                   | e
    CR                  | update is replaced by: 'update' .. feedkeys(":echo 'hello'\r", 'i')[-1]
    :echo 'hello' CR CR | update
                        | update :echo 'hello' CR CR

*Without* the `i` flag, `:echo 'hello' CR` is correctly inserted *after* the carriage return:

    typeahead           | executed
    ------------------------------
    u                   | u
    p                   | p
    d                   | d
    ...                 | ...
    e                   | e
    CR                  | update is replaced by: 'update' .. feedkeys(":echo 'hello'\r")[-1]
    CR :echo 'hello' CR | update
                        | update CR :echo 'hello' CR

---

We could probably replace `feedkeys()` with a  timer, but it would make the code
more verbose.

##
# Reference

[1]: https://vi.stackexchange.com/a/25140/17449
[2]: https://github.com/vim/vim/issues/2216
[3]: https://github.com/vim/vim/releases/tag/v8.2.0851
