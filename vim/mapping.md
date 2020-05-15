# Why should I avoid passing the `t` flag to `feedkeys()` all the time?

It will break `feedkeys()` if the latter is called by `:norm`.

---

MWE:

    $ vim -Nu NONE +'nno cd :exe "norm! :call feedkeys(\"aaa\",\"t\")\r"<cr>'
    " press 'cd': nothing is inserted in the buffer~

    $ vim -Nu NONE +'nno cd :exe "norm! :call feedkeys(\"aaa\")\r"<cr>'
    " press 'cd': 'aa' is inserted in the buffer~

This is  a contrived example, but  the issue can  be encountered in a  real life
scenario. For example, in the past, we had these mappings:

    " ~/.vim/plugged/vim-help/after/ftplugin/help.vim
    nno <buffer><nowait><silent> q :<c-u>norm 1<space>q<cr>

    " ~/.vim/plugged/vim-window/plugin/window.vim
    nno <silent><unique> <space>q :<c-u>call lg#window#quit()<cr>

and this function:

    fu window#quit#main() abort
        ...
        if reg_recording() isnot# ''
            return feedkeys('q', 'nt')[-1]
                                   ^
                                   ✘
        endif
        ...

If a register is being recorded, and we're in a help buffer, pressing `q` should
end the recording; in practice, it didn't because of the `t` flag.

---

Note that you really need `:norm` to reproduce the issue.
For example,  if you  try to replace  it with a  second `feedkeys()`,  the issue
disappears (no matter whether you use the `t` flag in any function call):

    nno cd :call feedkeys('gh', 't')<cr>
    nno gh :call feedkeys('aaa', 'nt')<cr>
    " press `cd`: 'aa' is inserted

Also, the issue disappears if you use the `x` flag:

                                                                  v
    $ vim -Nu NONE +'nno cd :exe "norm! :call feedkeys(\"aaa\",\"tx\")\r"<cr>'
    " press 'cd': 'aa' is inserted in the buffer~

##
# One of my custom normal command is not repeatable with the dot command!  Why?

`.` only repeats the *last* default normal command.
So, if your  custom command executes several commands, `.`  will only repeat the
last one instead of the whole sequence.

# What do I need to do to make a custom operator repeatable with `.`?

Nothing.
There's no need to use `repeat#set()` or any other hack.

---

No matter how you implement your custom  operator, in the end, it executes `g@`,
which is  a builtin  Vim command.  `.` repeats the  last Vim  command, including
`g@`.

Note that `.` also repeats the motion or a text-object which you provided to the
operator.

##
# vim-repeat
## Why should I avoid using `repeat#set()` to make it repeatable?

1) The repetition doesn't always work as expected after an undo:

<https://github.com/tpope/vim-repeat/issues/63>

2) And sometimes, `.` repeats an old custom command.

These bugs  and [tpope's comment][1] indicate  that `repeat#set()` is  a brittle
hack, which should be avoided whenever possible.

---

1) You can check it doesn't work correctly after an undo with `vim-easy-align`:

    gaip*|
    u
    .

The dot  command should  repeat the  alignment of  all the  bars in  the current
paragraph.  Instead, it asks again for the characters to align.

The same kind of issue applied to `g SPC` (break line).
After an undo, the repetition didn't break the line, and did something else:
delete the line, put an empty line below...

---

2) In the past, I found another issue with `] SPC`:

   1. `] SPC`
   2. `dd`
   3. `.` to repeat `dd`

Vim repeated `] SPC`, instead of `dd`.

I found a solution, which was to add this line at the end of our custom function
(after invoking `repeat#set()`):

    do <nomodeline> CursorMoved

### I still want to make it repeatable with `repeat#set()`!  How to do it?

    nno <lhs> <rhs>:call repeat#set('<lhs>')<cr>

Or:

    nmap          <lhs>                  <plug>(named_mapping)
    nno <silent>  <plug>(named_mapping)  :cmd1<bar>cmd2...<bar>call repeat#set("\<plug>(named_mapping)")<cr>

Or:

    nmap          <lhs>                  <plug>(named_mapping)
    nno <silent>  <plug>(named_mapping)  :cmd1<bar>cmd2...<bar>call Func()<cr>

    fu Func()
        ...
        sil! call repeat#set("\<plug>(named_mapping)")
        "  ^
        " Sometimes, you may not have the plugin, or it may be temporarily disabled.
        " In this case, the function won't exist.
    endfu

##
## I want `.` to repeat my commands with the same count I used initially!  How to do it?

`repeat#set()` accepts a 2nd optional argument.
Use it to pass `v:count`.

### My mapping is in visual mode, not normal!  How to adapt the code?

In the previous code, replace:

   - `:nmap` with `:xmap`
   - `:nnoremap` with `:noremap`

#### Which pitfalls should I avoid?  (2)

Don't use `:xnoremap` in your 2nd mapping, use `:noremap` instead.

`repeat.vim`  remaps the  dot command,  to  make it  type the  contents of  some
variables updated via some autocmds.
But it remaps the dot command only in normal mode, not in visual mode.

As a result, your 2nd mapping (<plug> → ...) needs to cover both modes:

   - visual when you'll press the lhs initially
   - normal when you'll press `.`

---

Don't  reselect  the visual  selection  with  `gv` at  the  end  of your  custom
commands.  Otherwise,  before being able to  press `.`, you would  need to press
`Escape` to get back to normal mode.

##
# What's a “pseudo-operator”?

The term is not used in the help.
I use it to refer to an operator to which the same text-object is always passed.
Such an operator can be useful to make a custom command repeatable.

# When I implement a custom operator, I often hesitate between `g@_` and `g@l`.  Which one should I use?

If you're *not* implementing a pseudo-operator, use `g@_`.

If you *are* implementing a pseudo-operator, use `g@l`; unless:

   - it needs to refer to the change marks

     and

   - it doesn't care about the column position of the cursor

---

Rationale:

If your custom operator is a pseudo one, and you implemented it like this:

    nno <key> :<c-u>set opfunc=MyOp<bar>norm! g@_<cr>
                                                ^
                                                ✘

The `_` motion will make the cursor jump at the beginning of the line, which you
probably don't want.  You can avoid the jump by replacing the motion `_` with `l`.

---

If your custom operator is *not* a pseudo operator, and you implemented like this:

    nno <key>      :set opfunc=MyOp<cr>g@
    xno <key>      :call MyOp('vis')<cr>
    nno <key><key> :set opfunc=MyOp<bar>exe 'norm! '..v:count1..'g@l'<cr>
                                                                   ^
                                                                   ✘

The `l` motion will  prevent Vim from setting the change marks  on the lines you
want to change, when you press `123<key><key>`.
So,  `MyOp()`  will  need  to  make   a  distinction:  have  I  been  called  by
`<key>{text-object|motion}`, or by `123<key><key>`?

In the first case, it will have to use the change marks.
In the second case, it will have to use the range `.,. +(v:count1 -1)`.

This introduces unneeded complexity...
So, replace the `l` motion with `_`.

## ?

Document this pitfall:

    nno cd :call Func()<cr>bbb
    fu Func() abort
        call input('>')
    endfu

Press  `cd`, and  you'll  see that  `bbb`  has been  consumed  by `input()`  and
inserted on the command-line, instead of being pressed.
But if you rewrite the mapping like this, it works as expected:

    nno cd :call Func()<bar>norm! bbb<cr>
    fu Func() abort
        call input('>')
    endfu

Or you could write this:

    nno cd :call Func()<cr>bbb
    fu Func() abort
        call inputsave()
        call input('>')
        call inputrestore()
    endfu

---

Document this pitfall:

    nno z= :set opfunc=Z_equal<bar>norm! g@l<cr>
    fu Z_equal(_) abort
        setl spell
        call feedkeys('z=', 'n')
    endfu

It could  be tempting  to always  write `norm! g@l`  rather than  pressing `g@l`
directly,  so that  if the  opfunc invokes  a function  consuming the  typeahead
(`input()`, `getchar()`, ...), it doesn't wrongly consume `g@`.

But doing  so would break  commands which requires  the user's input,  like `:s`
with the `c` flag, or `z=`.  Indeed, `:norm` considers these type of commands as
*in*complete  (the user's  input is  missing), and  so it  presses Escape  which
prevents you from providing any input.

From `:h norm`:

>     {commands} should be a complete command.  If
>     {commands} does not finish a command, the last one
>     will be aborted as if <Esc> or <C-C> was typed.

# When should I use `g@_` to implement a pseudo-operator?

When two conditions are satisfied.

1. The commands executed by your function make the cursor jump (e.g. `:s`).

Note that `:keepj`  doesn't prevent the cursor from jumping,  it merely prevents
an entry from being added to the jumplist.

2. You prefer to use this range (for better readability):

        line("'[")..','..line("']")

Instead of:

    '.,.+' .. (v:count1 - 1)

Currently, the only place where these conditions are satisfied is in:

    ~/.vim/plugged/vim-par/plugin/par.vim:98
    /gqs

##
# How to tweak the behavior of a default operator?

Create a wrapper around it.

Example with the `gq` operator:

    nno <silent> gq  :<c-u>set opfunc=<sid>gq<cr>g@
    nno <silent> gqq :<c-u>set opfunc=<sid>gq<bar>exe 'norm! '..v:count1..'g@_'<cr>
    xno <silent> gq  :<c-u>call <sid>gq('vis')<cr>

    fu s:gq()
        " tweak some setting which alters the behavior of `gq`
        ...
        " execute the default `gq`
        if a:type is# 'vis'
            norm! '<V'>gq
        else
            norm! '[gq']
        endif
    endfu

# My custom operator works.  But when I press `.`, it's not repeated!  Why?

If the  function implementing  your operator calls  another operator  during its
execution, `.` will repeat the latter.

Example:

    nno <silent> \d :<c-u>set opfunc=<sid>duplicate_and_comment<cr>g@

    fu s:duplicate_and_comment(type)
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

# How to fix it?

1) Restore `'opfunc'` correctly.

2) Or better, don't use a a second operator B inside an operator A:
   call the function implementing B via an Ex command.

In the previous example, we use `:Commentary`.

Using an Ex  command is better, because resetting `'opfunc'`  inside an operator
function feels clumsy.
Besides, it creates a bad repetition (DRY,  DIE): if one day you change the name
of your operator function, you'll also need to remember to change it on the line
where you restore `'opfunc'`.

##
# opfunc
## My opfunc uses `:s/pat/rep/c`.  It doesn't work!

You may be invoking your opfunc via `:norm!`.
In this case, read this (from `:h :norm`):

>       {commands} should be a complete command.  If
>       {commands} does not finish a command, the last one
>       will be aborted as if <Esc> or <C-C> was typed.

`:s/pat/rep/c` is an unfinished command: it requires the user's input to finish.
So, `:norm!` aborts your `:s/.../c` command.
Use `feedkeys()` instead.

    nno <key> :set opfunc=OpFunc<bar>exe 'norm! '..v:count1..'g@_'<cr>
                                          ^
                                          ✘

    nno <key> :set opfunc=OpFunc<bar>call feedkeys(v:count1..'g@_', 'n')<cr>
                                          ^
                                          ✔

## My opfunc uses `setline()`, not `:s`.  How to pass it a range when I use a count (e.g. `123g@_`)?

Install a wrapper around your opfunc.
Inside the wrapper, call the opfunc by prefixing `:call` with the range:

               ┌ consumes the type
               │
    fu Wrapper(_)
        '[,']call OpFunc()
    endfu

    fu OpFunc()
        " use setline()
    endfu

You  can use  the  change marks  because  Vim should  set  them correctly  after
`123g@_` has been executed.

## My opfunc executes several `:echo`.  Only the last message is printed!

I think that Vim redraws automatically before every command printing a message.
This includes sth like `:echo 'msg'` and `:call input('>')`.

I don't know any solution to this  issue, other than printing your messages from
another function invoked before/after your opfunc, but not directly from it:

    nno cd :set opfunc=Func<bar>norm! g@_<cr>
    fu Func(_)
        call FuncA()
    endfu
    fu FuncA() abort
        echo 'foo'
        echo 'bar'
    endfu
    " ✘
    " press `cd`
    " bar~

    nno cd :set opfunc=Func<bar>exe 'norm! g@_'<bar>:call FuncA()<cr>
    fu Func(_)
    endfu
    fu FuncA() abort
        echo 'foo'
        echo 'bar'
    endfu
    " ✔
    " press `cd`
    " foo~
    " bar~

---

Note that the same issue exists for timers:

    " ✔
    :echo 'foo' | echo 'bar'
    foo~
    bar~

    " ✘
    :call timer_start(0, {-> execute('echo "foo" | echo "bar"', '')})
    bar~

And for autocmds:

    augroup test_echo
        au!
        au CursorHold * call Func() | au! test_echo
    augroup END
    fu Func()
        echo 'foo'
        echo 'bar'
    endfu

##
# `maparg()`
## How to represent the mode 'nvo' in the input of `maparg()`?

Use an empty string:

    vim -Nu NONE +'noremap <c-e> :echom "test"<cr>'
    :echo maparg('<c-e>', '')
                          ^^

### How does `maparg()` represent `nvo` when its output is a dictionary?

With a space:

    vim -Nu NONE +'noremap <c-e> :echom "test"<cr>'
    :echo maparg('<c-e>', '', 0, 1).mode is# ' '
                                              ^

##
## How to represent the operator-pending mode in the input of `maparg()`?

Use 'o':

    vim -Nu NONE +'ono <c-e> :echom "test"<cr>'
    :echo maparg('<c-e>', 'o')
                          ^^^

### How does `mode()` represent the operator-pending mode in its output?

With 'n':

    vim -Nu NONE -S <(cat <<'EOF'
        ono <expr> <c-e> Func()
        fu Func()
            echom mode()
        endfu
    EOF
    )
    " press y C-e: n is printed

Which is the same as for normal mode.
IOW, `mode()`  is useless to detect  operator-pending mode; you need  to pass it
the optional argument `1` for its output to be reliable.

#### What if I pass the optional argument `1`?

Then, `mode(1)` evaluates to 'no', or 'nov', or 'noV' or 'no^V'.

    vim -Nu NONE -S <(cat <<'EOF'
        ono <expr> <c-e> Func()
        fu Func()
            echom mode(1)
        endfu
    EOF
    )
    " press y C-e: no
    " press y v C-e: nov
    " press y V C-e: noV
    " press y C-v C-e: no^V

##
## I'm saving information about this mapping:

    nno <m-b> :call <sid>func()<cr>
    fu s:func()
        echo 'mapping is working'
    endfu
    let save = maparg('<m-b>', 'n', 0, 1)

### What's wrong with the code?  (2)

The `lhs` key is translated:

    echo save.lhs
    â~

This doesn't prevent you from saving/restoring a mapping:

    nno <m-b> :echo 'm-b'<cr>
    let save = maparg('<m-b>', 'n', 0, 1)
    nunmap <m-b>
    exe 'nno '..save.lhs..' '..save.rhs

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

    nno <m-b> :call <sid>func()<cr>
    fu s:func()
        echo 'mapping is working'
    endfu

    vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    let fix = {'lhs': '<m-b>', 'rhs': escape(maparg('<m-b>', 'n'), '|')}
    let save = extend(maparg('<m-b>', 'n', 0, 1), fix)
               ^^^^^^                             ^^^

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
    ^^^

    sil! unmap <c-q>
    map <c-q> <nop>
    sunmap <c-q>
    map <c-q>
    nox<C-Q>         <Esc>~
    ^^^

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

    if empty(mapcheck('abc', 'n'))
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

    if empty(maparg('abc', 'n'))
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

    nno <plug>(abc) :echo 'some feature'<cr>
    nmap cd "_yy<plug>(abc)"_yy
    echo hasmapto('<plug>(abc)', 'n')
    1~

##
# Tricks
## I have a simple mapping whose rhs is just a sequence of normal commands.

Example:

    nno cd xlx

### How to make a count repeat the whole sequence, and not just the first normal command?  (2)

Use the `<expr>` argument:

    nno <expr> cd "\e"..repeat('xlx', v:count1)
        ^^^^^^     ^^                 ^^^^^^^^

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
    nno <plug>(myLeader)a :echo 'foo'<cr>
    nno <plug>(myLeader)b :echo 'bar'<cr>
    nno <plug>(myLeader)c :echo 'baz'<cr>
    ...

<http://vi.stackexchange.com/a/9711/6960>

### What's one pitfall of this trick?

`<plug>(myLeader)a` fails to override a mapping whose lhs is `<space>a`:

    nno <space>a :echo 'original'<cr>

    nmap <space> <plug>(myLeader)
    nno <plug>(myLeader) <nop>
    nno <plug>(myLeader)a :echo 'redefined'<cr>

In contrast, `<leader>a` would succeed:

    let mapleader = ' '
    nno <space>a :echo 'original'<cr>
    nno <leader>a :echo 'overridden'<cr>

### When is it useful?

I guess it's  only useful when you write  a plugin and want to  provide a leader
key to your users.  Although, even then, because of the pitfall, you'll probably
want to write sth like this instead:

    let leader = get(g:, 'user_leader', '<space>')
    for [lhs, rhs] in [['a', ':echo "foo"<cr>'], ['b', ':echo "bar"<cr>'], ['c', ':echo "baz"<cr>']]
        exe 'nno '..leader..lhs..' '..rhs
    endfor

##
# Miscellaneous
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

    $ vim -Nu NONE -S <(cat <<'EOF'
        exe "set <F10>=\ed"
        nno <F10> :echo 'F10 was pressed'<cr>
        exe "set <F5>=\ed"
        nno <F5> :echo 'F5 was pressed'<cr>
    EOF
    )
    " press 'Esc' + 'd': 'F5 was pressed' is printed

In the last example, the `F5` mapping was used even though the `F10` key and the
`F10` mapping were defined earlier.
This is because `F5` comes before `F10` in the output of `:set termcap`.

## When does Vim translate terminal keys (set with sth like `set <m-d>=^[d`)?

When processing mappings; right before trying to expand the keys.
It doesn't matter whether the keys *will be* remapped; what matters is that they
*can* be remapped.

    vim -es -Nu NONE -S <(cat <<'EOF'
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

    vim -es -Nu NONE -S <(cat <<'EOF'
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

    vim -es -Nu NONE -S <(cat <<'EOF'
        exe "set <m-d>=\ed"
        imap <c-b> <esc>dd
        0pu='x'
        call feedkeys("i\<c-b>", 'x')
        %p
        qa!
    EOF
    )
    ädx~

    vim -es -Nu NONE -S <(cat <<'EOF'
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
# Pitfalls
## Why should I avoid a mapping with an `<Esc>` in its lhs?

The terminal uses `Esc` to encode some special keys (e.g. arrow keys, function keys, ...).

Now suppose you have this mapping:

    nno <c-b><esc> :echo 'C-b Esc'<cr>
    nno <c-b><up>  :echo 'C-b Up'<cr>

And you  press `C-b Up`;  instead of  using your 2nd  mapping, Vim will  use the
first one, and insert `A` in the buffer.

Here's what happens:

    typed  | typeahead              | executed
    ------------------------------------------
    C-b Up | C-b Esc O A            |
           | :echo 'C-b Esc' CR O A |
           |                        | :echo 'C-b Esc' CR O A

Vim conflates the `Esc`  produced by the terminal when `Up`  is pressed, with an
`Esc` typed interactively.

This can lead to unexpected behaviors such as the one reported [here][2].

From `LeoNerd` on the `#vim` irc channel.

>     Yeah.. that's because vim's keyboard input system is stupid
>     In vim- raw bytes arrive from the terminal, go into the map engine (which just looks to see if the
>     headofqueue bytes match any of its mappings, and replace them if so), then bytes come out directly into
>     the command system
>     Whereas in nvim, raw bytes go into the termkey instance, which turns them into *keys*, and those *keys*
>     are what goes into the map engine
>     So the map engine is never confused by the individual component bytes that formed those keypresses
>     Just like it isn't confused by the individual bytes that came across the X11 unix socket when in gvim
>     mode, or.. any other stupid crazy things that wouldn't be possible if it was actually sensible

### What if `<Esc>` is used in the rhs of a mapping?

If the mapping is non-recursive, it should be ok.
Otherwise, replace it with `<C-\><C-n>` so that Vim's map engine can't get confused.

In  general, in  the rhs  of  a mapping,  always write  `<C-\><C-n>` instead  of
`<Esc>`; it's  more consistent, and  more future-proof (a  non-recursive mapping
could be refactored into a recursive one in the future).

---

Example to illustrate the pitfall:

    vim -es -Nu NONE -S <(cat <<'EOF'
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
               ^^^^^

    " good
    imap <c-b> <c-\><c-n>ddi
               ^^^^^^^^^^

Now, this is what happens:

    typeahead     | executed
    --------------------
    <c-b>         |
    <c-\><c-n>ddi |
                  | <c-\><c-n>ddi

---

The reason  why non-recursive mappings should  not be affected by  an `<esc>` in
the rhs  is because Vim only  translates terminal keys *right  before* trying to
expand them via mappings. If  the keys have been produced by  a mapping, and the
latter is non-recursive,  then Vim can't expand them a  second time, and there's
no need to translate terminal keys; so it just executes them.

##
## My mapping ignores the count I prefixed it with!

You may have a `:norm!` command somewhere which resets `v:count[1]` to 1.
Try to  capture `v:count[1]`  as soon  as possible in  a variable;  then, always
refer to the latter in your code (never refer to `v:count[1]`).

Capture it either at the very start of the function definition:

    nno cd :call Func()
    fu Func()
        let cnt = v:count1
        " refer to `cnt` when needed
        ...
    endfu

Or at the function call site:

    nno cd :call Func(v:count1)
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

    vim -Nu NONE +'nno xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx abc'
    E474: Invalid argument~

Make the lhs shorter.

---

Note that the weight of `<plug>` is 3 bytes:

    :echo len("\<plug>")
    3~

##
## How to use a chord with the meta modifier in my mappings?

                   ┌ terminal sequence encoding `M-b`
                   ├─┐
    exe "set <M-b>=\eb"
    ino <M-b> ...

### Now I can't insert some accented characters anymore!

Yes, for example, if you have the mapping `ino <m-d> <c-o>de`, you can't insert `ä`.

    vim -Nu NONE -S <(cat <<'EOF'
        exe "set <M-d>=\ed"
        ino <M-d> <c-o>de
        startinsert
    EOF
    )
    " press the dead key '¨' followed by 'a': 'ä' is not inserted

Solutions:

Press `C-v` to suppress mappings:

    C-v ¨ a

From `:h i^v`:

>     The characters typed right after CTRL-V are not considered for mapping.

Or use a digraph:

    C-k a "

Or use replace mode:

    r ¨ a

Or use an equivalence class in a search command.

#### But what causes this pitfall?

When you try to insert `ä`, it's first written in the typeahead buffer.
But internally, Vim encodes `ä` exactly as `<M-d>`:

    vim -Nu NONE
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
                                            vvv
    :echo system('bc <<<"ibase=10; obase=2; 100"')[:-2]
    1100100~
                                              binary code of 'd' with an extra bit set on the left
                                              vvvvvvvv
    :echo system('bc <<<"ibase=2; obase=1010; 11100100"')[:-2]
    228~
    :echo nr2char('228')
    ä~

####
#### I want a fix which doesn't require any extra input!

Try this:

    exe "set <F30>=\ed"
    nno <F30> ...
         ├─┘
         └ arbitrary function key
          (you want to choose one which you'll never use interactively, so forget about F1-F12)

Example:

    vim -Nu NONE -S <(cat <<'EOF'
        exe "set <F30>=\ed"
        nno <F30> :echom 'I pressed M-d'<cr>
    EOF
    )
    " press M-d: Vim logs the message 'I pressed M-d'

---

Note that you can use function keys up to the number 37.

    :set <f37>
    E846: Key code not set: <f37>~

    :set <f38>
    E518: Unknown option: <f38>~

And you  can combine  a function  key with  the shift  modifier to  decrease the
probability you'll ever need to use it interactively:

    nno <S-F30> ...
         ^^

But you can't use any other modifier:

    :set <c-f1>
    E518: Unknown option: <c-f1>~

    :set <m-f1>
    E518: Unknown option: <m-f1>~

---

It works, but in practice, it's cumbersome to use because it's only necessary in
Vim and only if the terminal is not  in modifyOtherKeys mode, so you have to use
this kind of template when installing your meta mappings:

    if has('nvim') || has('gui_running') || &t_TI =~# "\e[>4;2m"
        nno <m-d> ...
    else
        nno <f30> ...
    endif

Besides, using function keys to refer to meta chords makes the code harder to read.

Finally, it doesn't fix the issue for gVim.
Indeed,  when you  press  `M-d`, gVim  doesn't  receive  `Esc +  d`,  like in  a
terminal; it really  receives `ä`.  Press `C-v  M-d` in Vim vs  gVim, and you'll
see the difference.
IOW, if you want your `<m-d>` mapping to work in gVim, you *have to* use `<m-d>`.
And you have to accept that you can't insert `ä` anymore.

##### How does this work?

By telling Vim a lie:

    exe "set <F30>=\ed"

This tells Vim that  whenever it sees the sequence `Esc` +  `d` in the typeahead
buffer, it must translate it into `<F30>`; which is wrong, but bear with me.

From then, whenever you need to refer to `M-d` in a mapping, you write `<F30>`.
As an example, you don't write this:

    ino <M-d> <esc>id
        ^^^^^
        ✘

But this:

    ino <F30> <c-o>de
        ^^^^^
        ✔

Now, when you'll try to insert `ä`, here's what happens:

    typeahead | executed
    --------------------
    ä         |
              | ä

`ä` is not remapped  in the typeahead buffer because you  don't have any mapping
whose lhs is `<M-d>` nor `ä`.

###### Wait.  How does a mapping triggered by `<M-d>` still work if I never write the latter explicitly?

You don't need the  key notation `<M-d>` to make Vim execute  sth when you press
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
    nno <expr> cd "\e"..repeat('xlx', v:count1)

---

If you were  using `@=` for another  reason, you can probably replace  it with a
combination of `:exe` and another command:

    " before
    nno <buffer><nowait><silent> q <c-w><c-p>@=winnr('#')<cr><c-w>c

    " after
    nno <buffer><nowait><silent> q :<c-u>wincmd p <bar> exe winnr('#')..'wincmd c'<cr>
                                                        ^^^              ^^^^^^

##
## `<nowait>` doesn't work!

Try to install your mapping later.

---

The installation order of your mappings matters:

    vim -Nu NONE -S <(cat <<'EOF'
        set showcmd timeoutlen=3000
        nno <nowait> <c-b>  :echo "c-b was pressed"<cr>
        nno          <c-b>x <nop>
    EOF
    )
    " press C-b: you need to wait 3s for the message to be printed

    vim -Nu NONE -S <(cat <<'EOF'
        set showcmd timeoutlen=3000
        nno          <c-b>x <nop>
        nno <nowait> <c-b>  :echo "c-b was pressed"<cr>
    EOF
    )
    " press C-b: the message is printed immediately

---

In practice, you should not encounter this issue, because `<nowait>` is intended
to prevent a global mapping from causing a timeout for a buffer-local mapping.

And a buffer-local mapping is typically installed from a filetype plugin while a
global mapping  is installed from a  regular plugin; regular plugins  are always
sourced before any filetype plugin.

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
## ?

Document when `b:changedtick` is automatically incremented.

    $ touch /tmp/file{1..2} && vim -Nu NONE -S <(cat <<'EOF'
        let g:abuf = 'expand("<abuf>")'
        eval getcompletion('buf*', 'event')
            \->filter({_,v -> v !~# 'Cmd$'})
            \->map({_,v -> execute(printf(
            \ 'au %s * unsilent echom "%s in buf "..%s..": tick is "..getbufvar(%s, "changedtick")'
            \ , v, v, g:abuf, g:abuf))})
        call map(range(10), {_,v -> execute('pu='..v)})
        undo
    EOF
    ) /tmp/file1
    :mess clear
    :e /tmp/file2
    :mess
    BufNew in buf 2: tick is 1~
    BufAdd in buf 2: tick is 1~
    BufCreate in buf 2: tick is 1~

    BufLeave in buf 1: tick is 34~
    BufWinLeave in buf 1: tick is 34~
    BufUnload in buf 1: tick is 34~

    BufRead in buf 2: tick is 1~
    BufReadPost in buf 2: tick is 1~
    BufEnter in buf 2: tick is 2~
    BufWinEnter in buf 2: tick is 2~

Note how `b:changedtick` is initialized to 1 on `BufNew`.
And how  it's incremented on the  first `BufEnter` (it's not  incremented on the
subsequent ones).

It's also incremented on `BufReadPre`, but only when you reload a buffer.
Remember that `BufReadPre` is fired only if the buffer is read from an existing file.

Btw, yes, we really need `expand('<abuf>')`.
If you just write `b:changedtick`, you'll get wrong results.
For example, `BufNew` is  not fired in the context of  the newly created buffer,
but in the context of the one from which it's being created.

Update: `b:changedtick` is not initialized to 1 on `BufNew` when you run `:saveas`.

---

It's also automatically incremented on  `BufWritePost`, provided that the buffer
is modified:

    $ touch /tmp/file && vim -Nu NONE -S <(cat <<'EOF'
        au BufWritePre * echom 'BufWritePre: '..b:changedtick
        au BufWritePost * echom 'BufWritePost: '..b:changedtick
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

---

In an  operator-pending mapping,  `b:changedtick` is  not incremented  until the
mapping has completed and the operator has been executed.

---

When you  delete some  text with  `d`, `b:changedtick` is  incremented by  1, no
matter the text size.

When you change some text with `c`,  `b:changedtick` is incremented by 1 as soon
as the text is deleted, and you enter insert mode; then for each typed key, it's
incremented by 1 more.

## ?

Find  an example  where  the  `CursorMoved` autocmd  of  `vim-repeat` fixed  the
repetition of an omap (at least in the past).  Based on this comment:
<https://github.com/tpope/vim-repeat/issues/8#issuecomment-13951082>

---

Btw, what the  author of the original  issue report describes seems to  be a bug
which was fixed by 7.3.918.
It looks like –  in the past – if you defined a  text-object which enters visual
mode, then Vim  remembered the geometry of  the text which was  operated on, and
the dot command used that info.

This means that the repetition was sometimes unexpected:

    $ vim -Nu NONE +'ono <c-b> :norm! T,vt,<cr>' +"pu!=['a,xxx,b', 'a,xxxx,b']" +'norm! 1Gfx'
    " press: d C-b
             j .

Before 7.3.918, the second line contained:

    a,x,b
      ^
      ✘

After the patch, it contains:

    a,,b
     ^^
     ✔

So `vim-repeat` seems completely irrelevant here.
Update: Actually, it's not completely irrelevant; it could have helped by making
`.` retype the exact same sequence of  keys (instead of the native `.` which was
broken).

## ?

Maybe you should document here when `b:changedtick` is incremented.
Comment from `vim-repeat`:

    " `b:changedtick` is incremented when:
    "
    "    - `BufReadPre` is fired
    "
    "    - `BufEnter` is fired right after `BufReadPre`
    "
    "         touch /tmp/.file && vim -Nu NONE -S <(cat <<'EOF'
    "             augroup test_changedtick | au!
    "                 au BufLeave * unsilent echom 'BufLeave: '..b:changedtick
    "                 au BufEnter * unsilent echom 'BufEnter: '..b:changedtick
    "                 au BufReadPre * unsilent echom 'BufReadPre: '..b:changedtick
    "                 au BufWritePre * unsilent echom 'BufWritePre: '..b:changedtick
    "                 au BufWritePost * unsilent echom 'BufWritePost: '..b:changedtick
    "             augroup END
    "         EOF
    "         ) /tmp/.file
    "         :echo b:changedtick
    "         3~
    "         :e
    "         BufReadPre: 4~
    "         BufEnter: 5~
    "
    "    - `BufWritePost` is fired *while the buffer is modified*
    "
    "         touch /tmp/.file && vim -Nu NONE -S <(cat <<'EOF'
    "             augroup test_changedtick | au!
    "                 au BufLeave * unsilent echom 'BufLeave: '..b:changedtick
    "                 au BufEnter * unsilent echom 'BufEnter: '..b:changedtick
    "                 au BufReadPre * unsilent echom 'BufReadPre: '..b:changedtick
    "                 au BufWritePre * unsilent echom 'BufWritePre: '..b:changedtick
    "                 au BufWritePost * unsilent echom 'BufWritePost: '..b:changedtick
    "             augroup END
    "         EOF
    "         ) /tmp/.file
    "         :echo b:changedtick
    "         3~
    "         :w
    "         BufWritePre: 3~
    "         BufWritePost: 3~
    "         "='' CR p
    "         :echo b:changedtick
    "         4~
    "         :w
    "         BufWritePre: 4~
    "         BufWritePost: 5~
    "
    " It is not  incremented on other `BufEnter` events, nor  on `BufLeave`, nor
    " on `BufWritePre`.

## ?

Document that it's impossible to map keys while Vim's pager is displayed.

From `:h pager`:

>     Note: The typed key is directly obtained from the terminal, it is not mapped
>     and typeahead is ignored.

For the  hit-enter prompt, mappings  do apply,  but `mode()` always  returns `n`
when invoked from an `<expr>` mapping (or when included in the status line).
As  a workaround,  you can  try to  evaluate it  from a  timer (but  that's only
possible in Vim, not in Nvim).  See here for an example:

    ~/.vim/plugged/vim-cmdline/autoload/cmdline.vim
    /hit_enter_prompt_no_recording

You  may wonder  why `mode()`  returns `n`  from an  `<expr>` mapping  while the
hit-enter prompt is visible.
Theory:
No matter the key you press, the hit-enter prompt is closed immediately:

    $ vim -Nu NONE +'nno x <nop>' +"pu='ccc'" +'echo "a\nb"'
    " press 'x': the hit-enter prompt is closed, even though 'x' had no effect because it was a no-op

So, maybe  mappings are probably  processed right  afterward; but in  that case,
it's too late for  `mode()` to return `r`; now, it can  only return `n`, because
the hit-enter prompt is no longer visible and you're really in normal mode.

You may wonder why `mode()` returns `n` in the status line.
Theory: The  status line  is  not  updated on  the  command-line,  nor when  the
hit-enter prompt is visible:

    $ vim -Nu NONE +'set ls=2 stl=%{mode(1)}'
    :echo "a\nb"
    " the status line contains 'n' while you're typing the command (not 'c')
    " the status line still contains 'n' after you've run the command

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

In Nvim, the status line *is* updated when you enter the command-line, but *not*
when the hit-enter prompt is visible.

---

Also, document the  difference between the hit-enter prompt  and the more-prompt
(aka pager).  You're at the former when you reach the end of a multi-line output
(`mode(1)` is `rm`), and at the latter when you scroll back (`mode(1)` is `r`).

---

Explain why  `q` starts a recording  when it's pressed at  the hit-enter prompt,
but not at the more prompt.

At the more-prompt, only a small number of commands are valid:

>     Any other key causes the meaning of the keys to be displayed.

`q` is one of them; it stops the listing.

OTOH, at  the hit-enter prompt, all  the usual normal commands  are valid again,
including `q` which starts a recording.

---

You may want to leave an explanation here: <https://github.com/vim/vim/issues/2589>
As well as this workaround:
<https://vi.stackexchange.com/questions/25109/how-to-map-q-to-cr-for-the-hit-enter-prompt/25140#25140>

---

Document  that –  in  Nvim –  timers's  callbacks are  not  processed while  the
hit-enter  prompt is  visible.   They  are blocked  until  it's  left *and*  you
interact with Nvim. See our comments in:

    " /cmdline#hit_enter_prompt_no_recording(
    ~/.vim/plugged/vim-cmdline/autoload/cmdline.vim

## ?

There's no need to  escape (so that the visual marks are set)  to know where the
visual selection begins/ends.

You can use `getpos('v')`, and `line('.')`:

    xno <expr><silent> <c-a> Func()
    fu Func() abort
        let lnums = [getpos('v')[1], line('.')]
        echom 'the visual selection starts at line '.min(lnums).' and ends at line '.max(lnums)
        return ''
    endfu

Try to use this technique in your plugin(s) instead of escaping.
Unless they really need to update the visual marks.

See `:h line()`:

>     v       In Visual mode: the start of the Visual area (the
>             cursor is the end).  When not in Visual mode
>             returns the cursor position.  Differs from |'<| in
>             that it's updated right away.

    :vim /\m\C\\e/gj $MYVIMRC ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/**
    :Cfilter! -other_plugins

Note that  the start of the  selection does not necessarily  match the character
which will be  marked with `'<`; if you're controlling  `'<`, then `getpos('v')`
gives  the  position of  `'>`,  and  vice  versa;  if you're  controlling  `'>`,
`getpos('v')` gives the position of `'<`.

I think "start of the Visual area" in the help means "controlled corner"...

If you want an expression which tells  you whether you're controlling the end of
the selection:

    line('.') > getpos('v')[1] || line('.') == getpos('v')[1] && col('.') >= getpos('v')[2]

And here's a mapping which gets you the geometry of the current visual selection
without quitting visual mode:

    xno <expr> <c-b> GetVisualSelectionGeometry()
    fu GetVisualSelectionGeometry() abort
        let [curpos, pos_v] = [getcurpos()[1:2], getpos('v')[1:2]]
        let control_end = curpos[0] > pos_v[0] || curpos[0] == pos_v[0] && curpos[1] >= pos_v[1]
        if control_end
            let [start, end] = [pos_v, curpos]
        else
            let [start, end] = [curpos, pos_v]
        endif
        echom printf('the visual selection starts at line %d column %d and ends at line %d column %d',
            \ start[0], start[1], end[0], end[1])
        return ''
    endfu

Note  that if  you've  pressed `O`,  the  reported positions  do  not match  the
upper-left and bottom-right corners, but the upper-right and bottom-left ones.

## ?

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

I think the issue is due to the  existence of a custom mapping on `q`.  When you
press `q`,  Vim probably  detects that  it's not the  default `q`  command which
terminates  a recording;  so it  records the  keypress.  It  turns out  that the
mapping will – in the end – press the default `q` command.

Solution:

In `window#quit#main()`, replace this line:

    if reg_recording() isnot# '' | return feedkeys('q', 'in')[-1] | endif

with this block:

    let regname = reg_recording()
    if regname isnot# ''
        call feedkeys('q', 'in')[-1]
        call timer_start(0, {-> setreg(regname, substitute(getreg(regname), 'q$', '', ''), 'c')})
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

## ?

Document that `:norm` *inserts* keys in the typeahead:

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

---

Also, document that `:norm!` – contrary to `feedkeys()` – executes the keys immediately:

    $ vim -es -Nu NONE -i NONE +"pu='some text'" \
      +'set vbs=1 | echom b:changedtick | call feedkeys("dd", "n") | echom b:changedtick | qa!'
                                          ^^^^^^^^^^^^^^^^^^^^^^^^
    3~
    3~

    $ vim -es -Nu NONE -i NONE +"pu='some text'" \
      +'set vbs=1 | echom b:changedtick | exe "norm! dd" | echom b:changedtick | qa!'
                                          ^^^^^^^^^^^^^^
    3~
    4~

## ?

    $ vim -Nu NONE +'set showcmd | tno <c-w>a bbb' +term
    " press C-w C-w to focus the split below: it works but you need to wait for a timeout

Theory to explain the timeout:

It seems that `'termwinkey'` is not written in the typeahead (not printed in the
`'showcmd'` area immediately).  It must be processed outside.

This creates an issue if you have  a Terminal-Job mode mapping which starts with
`'termwinkey'`.  When you press the key,  should Vim process it with its default
meaning (i.e. start a C-W command)?  Or should it remap the key?

In the first case, the key must stay *outside* the typeahead.
In the second case, the key must be sent *into* the typeahead.
Vim solves  this issue by waiting  `&timeoutlen` ms before sending  the key into
the typeahead.

To get rid of the timeout, install this mapping:

    tno <c-w><c-w> <c-w><c-w>

When you'll press the first `C-w`, there'll still be an ambiguity.
But when you'll press the second `C-w`, Vim will understand that you want to use
the `<c-w><c-w>` mapping and immediately writes the keys in the typeahead.
Note that the issue persists if you  wait more than `&timeoutlen` ms between the
first `C-w` and the second one.

This works under  the assumption that you didn't reset  `'termwinkey'`, and as a
result Vim uses  `<C-w>` to start a  C-W command.  This wouldn't  work if you've
reset the  option to, let's  say, `<C-s>`, and  you press `<C-s><C-w>`  to focus
another window.  For something more reliable, you could try this:

    augroup termwinkey_no_timeout
        au!
        au TerminalWinOpen * let b:_twk = &l:twk == '' ? '<c-w>' : &l:twk
          \ | exe printf('tno <buffer><nowait> %s<c-w> %s<c-w>', b:_twk , b:_twk)
          \ | unlet! b:_twk
    augroup END

Or:

    augroup termwinkey_no_timeout
        au!
        au TerminalWinOpen * let b:_twk = getbufvar(str2nr(expand('<abuf>')), '&twk')
          \ | if b:_twk == '' | let b:_twk = '<c-w>' | endif
          \ | exe printf('tno <buffer><nowait> %s<c-w> %s<c-w>', b:_twk , b:_twk)
          \ | unlet! b:_twk
    augroup END

## ?

Find usage examples for the `!` and `L` flags of `feedkeys()`.

## ?

Move as many comments from `vim-freekeys` here.

## ?

    call setcmdpos(6)

Positionne le curseur juste avant le 6e octet sur la ligne de commande.

Si aucun des  5 premiers caractères de la ligne  de commande n'est multi-octets,
positionne le curseur juste avant le 6e caractère.

Ne fonctionne que lorsqu'on édite la ligne de commande:

   - en y insérant l'évaluation d'une expression via C-r
   - en la remplaçant entièrement par l'évaluation d'une expression via C-\ e

Je  n'ai pas  réussi  à l'utiliser  directement au  sein  du (pseudo?)  registre
expression dans  lequel on entre  qd on  tape `C-r` ou  `C-\ e`.  En  revanche, elle
fonctionne correctement qd on évalue une fonction custom juste après.

Qd on évalue une fonction custom:

   - via `C-\ e`, `setcmdpos()` permet de positionner le curseur sur la nouvelle
     ligne de commande, l'ancienne étant remplacée par l'évaluation

   - via `C-r`, `setcmdpos()`  permet  de positionner  le curseur  sur
     l'ancienne ligne  de commande (qui n'est  pas remplacée), avant que
     l'évaluation ne soit insérée là où se trouve le curseur

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

---

La position du curseur via `setcmdpos()`  n'est pas établie au même moment selon
qu'on utilise `C-r =` ou `C-\ e` / `C-r C-r =`:

   - `C-r =`, après avoir évalué l'expression, *mais avant* de l'insérer

   - `C-r C-r =` et `C-\ e`, après avoir évalué l'expression

## ?

`C-j` (or a NUL) and `C-m` don't make a string end prematurely:

    echo "foo \<c-j> bar"
    foo ~
     bar~

In an `<expr>` mapping, it depends:

    " ✔
    fu Func(str)
        return ''
    endfu
    nno <expr> cd Func('foo <c-j> bar')
    norm cd

    " ✔
    fu Func(str)
        return ''
    endfu
    " nno <expr> cd ':call '..Func('foo <c-j> bar')
    nno <expr> cd Func('foo <c-j> bar')
    norm cd

    " ✘
    fu Func(str)
        return a:str
    endfu
    nno <expr> cd ':call '..Func('foo <c-j> bar')
    norm cd

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

## ?

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
Use an operator then a command. E.g.:

   - `cx`    vim-exchange; exchange the position of 2 text-objects
   - `ys`    vim-surround; surround a text-object with some character

It's an  invalid syntax, because an  operator only manipulates a  text-object or
the text covered by a motion.
You can use any command, except `a` and `i` because those are commonly used as a
prefix to create text-objects (`iw`, `ap`, ...).

Use an operator than a prefix. E.g.: `cz`, `dgb`

Use 2 operators. E.g.: `cd`, `cu`, `y=`

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
    :echo map(taglist('^<keys>'), 'v:val.name')

Output example when `<keys>` = `g CTRL-`

    ['g_CTRL-A', 'g_CTRL-G', 'g_CTRL-H', 'g_CTRL-]'~

FIXME: I think the output of `taglist()` is influenced by the current buffer.
Because it must look  in tags files, and those are set  by a buffer-local option
(`'tags'`); to be checked.

## ?

Read this: <https://vi.stackexchange.com/a/10284/17449>

Useful to better understand the distinction between a:

   - terminal keycode
   - Vim keycode
   - (mapped) key sequence

Hint:

This is a terminal keycode:

    ^[[23~

This is a Vim keycode:

    <S-F1>

This is a mapped key sequence:

    inoremap jk <Esc>:nohl<CR>
             ^^

Note that a mapped key sequence doesn't make sense outside of a mapping.
`jk` by itself is not a mapped key sequence.
It becomes one if it's used in the lhs of a mapping.

By contrast, `^[[23~` and `<S-F1>` don't need any context.
They are terminal/Vim keycodes by themselves.

## ?

Document that  `<nop>` loses  its special  meaning as soon  as it's  followed or
preceded by another key.  IOW, it must be alone.

    $ vim -Nu NONE +'nno cd <nop>x'
    " press 'cd'
    E486: Pattern not found: e~
    " this error is raised by the 'n' in '<nop>'

##
##
##
# Arguments
## Which mappings should never be defined with `<silent>`?

Any mapping in command-line mode.

First, it doesn't make sense.
`<silent>` is useful to  prevent Vim from displaying an Ex  command which is run
after entering the command-line from the rhs of the mapping:

        vvvvvvvv
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

##
## <expr>

    cno <f7> <c-\>e escape(getcmdline(), ' \')<cr>

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
        echohl WarningMsg | echo '['..a:cmd..'] was equivalent' | echohl NONE
    endfu

    nno <silent> <plug>(reminder) :call Reminder(input(''))<cr>

                                     ┌ appelle la fonction
                                     │               ┌ passe-lui cet argument
                                     │               │    ┌ termine/valide la saisie
                                     ├──────────────┐├───┐├──┐
    cnorea <expr> vs 'vs'..feedkeys('<plug>(reminder)C-w v<cr>')[-1]
    cnorea <expr> sp 'sp'..feedkeys('<plug>(reminder)C-w s<cr>')[-1]

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

Mais  `<plug>(...)`  peut poser  un  pb. Si  on doit  passer  un  argument à  la
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
        echohl WarningMsg | echo '['..cmd..'] was equivalent' | echohl NONE
    endfu

    nno <silent> <plug>(reminder) :call Reminder()<cr>

    cnorea <expr> vs 'vs'..feedkeys("<plug>(reminder)C-w v<cr>")[-1]
    cnorea <expr> sp 'sp'..feedkeys("<plug>(reminder)C-w s<cr>")[-1]

## <script>

    nno    <script>     ,dt                <SID>(FindTopic)dd
    nno                <SID>(FindTopic)    /Topic<cr>

    nno                 dd                 :call Func()<cr>

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

    nno <unique> cd :echo 'hello'<cr>

`<unique>` ne créera le mapping que si aucun autre mapping n'utilise `cd` comme lhs.

La vérification portera à la fois sur les mappings globaux et locaux.
Donc, les 2 cas de figure suivants échoueront:

    nno                    cd  :echo 'hello'<cr>
    " ✘
    nno  <buffer><unique>  cd  :echo 'world'<cr>

    " ✘
    nno  <buffer>          cd  :echo 'hello'<cr>
    nno          <unique>  cd  :echo 'world'<cr>


---

Avantage `<unique>`:

   - peu verbeux

Inconvénient `<unique>`:

   - soulève E227 en cas de conflit

Avantages `mapcheck()`:

   - vérifie  non seulement que le lhs n'est pas utilisé,
     mais en plus qu'il ne provoquera pas de lag

   - `if empty(mapcheck())|...|endif`  ne soulève aucun message d'erreur
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

    if empty(mapcheck('<key>', 'n')) && !hasmapto('<Plug>(plugin_some_func)', 'n')
        nno      <key>                       <Plug>(plugin_some_func)
    endif
    nno <silent> <Plug>(plugin_some_func)    :<c-u>call SomeFunc()<cr>

Définit un mapping appelant `SomeFunc()`.

À la place de `<plug>(plugin_some_func)` on pourrait utiliser autre chose, comme
pex `SPC x`, mais dans ce cas on consommerait un mapping existant.
`<plug>` correspond  à un keycode qu'il  est impossible de taper  au clavier, ce
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
        if empty(mapcheck('<key>', 'n')) && !hasmapto('<Plug>(plugin_some_func)', 'n')
            nmap <silent> <key> <Plug>(plugin_some_func)
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

    nno <key> :sil! exe "norm! \<lt>c-w>w\<lt>c-d>\<lt>c-w>w"<cr>

`:silent!` makes Vim ignore any error raised by `:norm`.

`<lt>` is  necessary to  prevent Vim  from translating  `<c-w>` in  the mappings
table before `:exe` is run.
If `<c-w>` is  translated directly in the mappings table,  then Vim will execute
it on  the command-line  with its default  meaning which is  to delete  the word
before the cursor (`:h c^w`).

You  can  use multiple  `<lt>`'s  to  prevent  a  control character  from  being
translated, as many times as necessary:

    nno cd :echo "\<c-w>"<cr>
    " press cd
    E115: Missing quote: "~

    nno cd :echo "\<lt>c-w>"<cr>
    " press cd
    ^W~

    nno cd :echo "\<lt>lt>c-w>"<cr>
    " press cd
    <c-w>~

Here, `<lt>lt>` prevents the translation of  `<c-w>` twice (once by `:nno`, once
by Vim when evaluating the double-quoted string).
Note that this  is a contrived example;  if all you wanted was  to echo `<c-w>`,
you could just write:

    nno cd :echo '<lt>c-w>'<cr>

---

But `:silent!` does *not* make Vim ignore errors raised other commands, like `:call`:

    nno <silent> cd :sil! call UnknownFunc() <bar> let g:d_var = 1<cr>
    " press:  cd
    " run:  :echo g:d_var
    " result:    E121
    " expected:  1 is printed

    nno <silent> cd :sil! 999999d <bar> let g:d_var = 1<cr>
    " press:  cd
    " run:  :echo g:d_var
    " result:    E121
    " expected:  1 is printed

Why?
Is it because of this:
<https://github.com/neovim/neovim/issues/11136#issuecomment-537253732>
You may think it's because for `silent!` to  work, it needs to be applied to the
whole rhs.  That's not true:

    nno <silent> cd :sil! exe 'call UnknownFunc() <bar> let g:d_var = 1'<cr>
    " press:  cd
    " run:  :echo g:d_var
    " result:    E121
    " expected:  1 is printed

I think it just works for `:norm`...

In any case, as a workaround, use `:exe`:

                     vvv
    nno <silent> cd :exe 'sil! call UnknownFunc()' <bar> echom 'processed'<cr>

---

    nno cd :let msg = input('') <bar> echo ' bye'<cr>hello

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

---

    nno <silent><expr> <cr> !empty(&buftype) ?
        \ ? '<cr>'
        \ : ':'..getbufvar('%', 'cr_command', 'norm! 80<bar>')..'<cr>'

Ce mapping remap CR différemment suivant le type de fichiers où l'on se trouve.

    !empty(&buftype)

... condition testant si le buffer est spécial.
Nécessaire car  CR a souvent une  fonction unique dans un  buffer spécial, qu'il
faut préserver.
Pex dans un buffer `qf`, CR charge l'entrée sous le curseur.

    getbufvar('%', '...', '...')

... on ne peut pas créer la variable pour tous les types de fichiers existants.
`getbufvar()`  permet   de  donner   une  valeur  par   défaut  à   la  variable
`b:cr_command`, afin que le mapping n'échoue pas dans les buffers où la variable
n'a pas été créée.

# Objets

    xno {object} {motion}
    ono {object} :norm v{object}<cr>

Définit un nouvel objet dont les caractères sont couverts par `{motion}`.

Ajouter `<silent>` pour que les opérations sur l'objet soient silencieuses.

---

Si le rhs du mapping `:xno` n'est pas un mouvement, mais l'appel à une fonction,
on peut le réutiliser pour le mapping `:ono`:

    xno {object} :<c-u>call MyFunc()<cr>
    ono {object} :<c-u>call MyFunc()<cr>

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

    :omap <expr> {object} '<Esc>'..'v{object}'..v:operator

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

    ono Ob) :norm! vib``<cr>
    ono Oe) :norm! vibo``<cr>

Crée  l'objet allant  du  curseur jusqu'au  début  / à  la fin  de  la paire  de
parenthèses à l'intérieur desquelles il se situe.

Illustration:

             cursor is here
             v
    func1(foo|, func2(), bar);
          ^^^
          text yanked if you press `yOb)`

    func1(foo|, func2(), bar);
              ^^^^^^^^^^^^^^
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

# Opérateurs

Whenever we mention a text-object, a motion is a valid replacement.

---

    nno <key><key> :<c-u>set opfunc=Func<bar>exe 'norm! '..v:count1..'g@_'<cr>

This mapping implements the convention,  which makes an operator act
on a number of lines when it's repeated.

Without a count, the operator acts on the current line.

It defines `Func()` as the function to call, then executes:

    :norm! {v:count1}g@_

The `_` motion makes Vim operate on the current line.
`v:count1` makes  Vim operate  on several  lines, from the  current one,  if the
operator was prefixed with a count.

---

    xno  <key>  :<c-u>call Func('vis')<cr>

    fu Func(type, ...)
        if a:type is# 'vis'
            " process visual selection
        else
            " process other cases
        endif
    endfu

Mapping implementing a visual operator.

We don't need to  execute `g@` because we already know  the text-object on which
we must operate: it's the one surrounded by the visual marks.

However, we need `C-u` so that the function is only called once.
We could eliminate `C-u`, if we gave the `range` attribute to the function.

---

Some people  use this code  to tell  the function that  it has been  called from
visual mode:

    xno <key> :<c-u>call Func(visualmode(), 1)<cr>

    fu Func(type, ...)
        if a:0
            " process visual selection
        else
            " process other cases
        endif
    endfu

We prefer the version  using `vis`, because it makes the  code more readable and
more consistent: we always inspect the value of `a:type`.

The consistency persists even if we also call the function from an Ex command:

    com Cmd call Func('Ex', <line1>, <line2>)

    fu Func(type, ...)
        if a:type is# 'Ex'
            " operate on lines between `a:1` and `a:2`
        endif
    endfu

# Récursivité

Les mappings récursifs peuvent être parfois complexes à comprendre.
Voici qques exemples, ainsi qu'une description de leur traitement par Vim.

    nmap <expr>  N               FuncA()
    nno  <expr>    <plug>(one)   FuncB()
    nno          ge<plug>(one)  :echo 'world'<cr>

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
    nno           N<plug>(one)  :echo 'world'<cr>

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

>     If the {rhs} starts with {lhs}, the first character is not mapped again.

Donc, Vim ne veut en aucune manière remap `N`.
En revanche, il peut remap le reste `<plug>(one)`, ce qu'il fait en utilisant le
2e mapping.
Ainsi, il développe `<plug>(one)` en la sortie de `FuncB()`, à savoir rien.
Mais pendant l'évaluation, il est amené à afficher `hello`.

---

    nmap <expr> cd              FuncA()
    nmap <expr>   <plug>(one)   FuncB()
    nno         cd<plug>(one)  :echo 'world'<cr>

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
    nno <plug>(put_123) :-pu=123<cr>
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
     nno <plug>(put_123) :-pu=123<cr>
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
    nno cD :echom 'test'<cr>
    " press cd: nothing happens

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

    cnorea <expr> update 'update'..feedkeys(":echo 'hello'\r", 'i')[-1]

Instead of printing `hello`, after executing `:update`, Vim executes this:

    :update:echo 'hello'

What's the fix?

Answer: don't pass the `i` flag to `feedkeys()`.

    cnorea <expr> update 'update'..feedkeys(":echo 'hello'\r")[-1]

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
    CR                  | update is replaced with: 'update' .. feedkeys(":echo 'hello'\r", 'i')[-1]
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
    CR                  | update is replaced with: 'update' .. feedkeys(":echo 'hello'\r")[-1]
    CR :echo 'hello' CR | update
                        | update CR :echo 'hello' CR

---

We could probably replace `feedkeys()` with a  timer, but it would make the code
more verbose.

##
# Reference

[1]: https://github.com/tpope/vim-repeat/issues/63#issuecomment-390281441
[2]: https://github.com/vim/vim/issues/2216
