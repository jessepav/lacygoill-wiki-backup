# getting the contents of a register
## How to display the contents and types of the registers `a`, `b`, and `c`?

    :reg abc

## How to get the contents of a register as a list of lines?  (2)

Use `getreginfo()`:

    echo getreginfo('r').regcontents

---

Or pass the third optional boolean argument `1` to `getreg()`:

    echo getreg('r', 1, 1)
                        ^

Note that the second argument is ignored here, so you could write any expression
in its place.

## How to get the last expression written in the expression register?  (2)

Use `getreginfo()`:

    echo getreginfo('=').regcontents[0]

---

Or pass the second optional boolean argument `1` to `getreg()`:

    getreg('=', 1)
                ^

Without  this  argument,  or  if  it was  false,  `getreg()`  would  return  the
evaluation of the last expression instead of the expression itself.

## How to get the name of the register which the unnamed register points to?

    :echo getreginfo('"').points_to

Usage example:

                                                 vv
    $ vim -Nu NONE -i NONE +"pu!='text'" +'norm! "ryy'
    :echo getreginfo('"').points_to
    r~

##
# setting the contents of a register
## How to save and restore a register?

Use `getreginfo()` and `setreg()`:

    " save
    let r_save = getreginfo('r')

    " restore
    call setreg('r', r_save)

## How to change the register which the unnamed register points to?

    :call setreg('r', {'isunnamed': v:true})

Example:

    $ vim -Nu NONE -i NONE +'call setline(1, ["aaa", "zzz"])' +'norm! "ayyj"zyy'

    :pu
    " 'zzz' is put
    :echo getreginfo('"').points_to
    z~

    :call setreg('a', {'isunnamed': v:true})

    :pu
    " 'aaa' is put
    :echo getreginfo('"').points_to
    a~

## How to change the type of a register?

Use a combination of `setreg()`, `getreginfo()` and `extend()`:

    call getreginfo('r')->extend({'regtype': 'V'})->setreg('r')
                                              ^
                                              new desired type

### Why not relying on the 3rd argument of `setreg()` and appending an empty string?  (2)

So, you're thinking about sth like this:

    call setreg('r', [''], 'aV')

There are two pitfalls.

First, if you try  to alter the type of the unnamed register  like that, it will
be automatically reconnected to `"0`.

    $ vim -Nu NONE -i NONE +"pu!='text'" +'norm! "ryy'
    :echo getreginfo('"').points_to
    r~

    :call setreg('"', [''], 'av')
    :echo getreginfo('"').points_to
    0~

Second,  if you  – accidentally  –  reset a  linewise register  into a  linewise
register  (yeah, I  know,  it's  useless; hence  the  *accidentally*), Vim  will
happily append an undesirable extra newline:

    $ vim -Nu NONE -i NONE +"pu!='text'" +'norm! yy'
    :call setreg('"', [''], 'aV')
    :reg "
    l  ""   text^J^J~
                  ^^
                  ✘

See: <https://github.com/vim/vim/issues/323>

##
## Why should I never use a string, and rarely a list, to set the contents of the unnamed register?

It would be automatically reconnected to `"0` right before the text is written.

    $ vim -Nu NONE -i NONE +"pu!='text'" +'norm! "ryy'
    :echo getreginfo('"').points_to
    r~

    :call setreg('"', [''], '')
    :echo getreginfo('"').points_to
    0~

Same thing if you use `:let` instead of `setreg()`:

    :norm! "ryy
    :echo getreginfo('"').points_to
    r~

    :let @" = ''
    :echo getreginfo('"').points_to
    0~

### What should I use instead?

A dictionary containing a `points_to` key.

The latter  tells Vim which  "real" register you  want to write  into.  Remember
that the unnamed register is not a real register; it's just a pointer.

### When should I still use a list?

When you want to *modify* (!= restore) the unnamed register definitively.
In that case, if  you use a dictionary to preserve the pointer,  the text may be
written in a non-ephemeral register (e.g. `"r`).
You probably don't want to lose the information contained in such a register.
That's why, you should let Vim reconnect `""` to `"0`.
The latter is ephemeral; you probably don't expect its contents to persist for a
long time.  IOW, you won't find it unexpected that it mutates automatically.

##
## Consider this assignment:

    let @r ..= 'appended'

### What's wrong with it?

It doesn't preserve the original type of the register `r`.

    norm! "ryy
    echo getregtype('r')
    V~

    let @r ..= 'appended'
    echo getregtype('r')
    v~

### How to fix it?

Use the third argument of `setreg()` to preserve the type:

    call setreg('r', ['appended'], 'a'..getregtype('r'))
                                    │   │
                                    │   └ preserve the current type
                                    └ append, don't overwrite

Example:

    norm! "ryy
    echo getregtype('r')
    V~

    call setreg('r', ['appended'], 'a'..getregtype('r'))
    echo getregtype('r')
    V~

##
## What's the default type of a register when I set it with `setreg()`, without a 3rd argument, and
### the 2nd argument is a string?

Characterwise.

    call setreg('r', 'linewise')
    echo getregtype('r')
    v~

### the 2nd argument is a list of strings?

Linewise.

    call setreg('r', ['foo', 'bar', 'baz'])
    echo getregtype('r')
    V~

## Consider these assignments:

    call setreg('"', #{regcontents: 'one', points_to: 'r'})
    call setreg('"', #{regcontents: 'two'})

### Which register does the unnamed register points to in the end?

It points to `"0`:

    echo getreginfo('"').points_to
    0~

Which is  consistent with a  `setreg()` invocation where  the 2nd argument  is a
string or a list.

###
## How to use `:redir` to redirect the output of an Ex command into a register?

    :redir @r | sil! cmd | redir END

This redirects the output of `cmd` inside the register `r`.

---

`:silent` makes sure *all* the output is redirected into the register.

If  the output  is too  long, it  may  be displayed  in Vim's  pager; when  that
happens, you need  to scroll to reach the end,  otherwise the redirection misses
all the lines which were never displayed; `:silent` avoids this pitfall.

### How to do the same thing without overwriting the current contents of the register?  I just want to append.

Uppercase the register name:

    :redir @R | sil! cmd | redir END
            ^

#### That's not possible for the clipboard!

You can also append `>>` to the register name:

    :redir @+>> | sil! cmd | redir END
             ^^

##
# Special registers
## What does `@%` contain?

The name of the current buffer.
The latter describes the path to the current file relative to the cwd.

## What does `@#` contain?

The name of the alternate buffer for the current window.
The latter describes the path to the alternate file relative to the cwd.

##
## Which contents does the unnamed register `""` refer to?

Whatever contents is stored in the last modified register.
For example, if  you've deleted a word  into the register `r`,  then the unnamed
register points to the latter.

### Which commands does it affect?

It's used by default by commands which put text (e.g. `p` == `""p`).

#### How to change this effect?

You can choose a different default register via the `'clipboard'` option.

##
## Which register is automatically restored at the end of a function call?

The search register.

See `:h function-search-undo`.

>     The last used search pattern and the redo command "."
>     will not be changed by the function.

    s/outside func call//ne
    fu! Func()
        s/inside func call//ne
        echom @/
    endfu
    call Func()
    echom @/
    inside func call~
    outside func call~

Warning: Do *not*  use our custom  `+s` operator to  source this code;  it would
interfere with the results.  And do *not* run the code via `:@*` after selecting
it; it wouldn't work as expected either.

Instead, write the code in a file, and source it with `:so%`.

### When is it not restored?

When you set it manually via `:let` or `setreg()`.

    s/outside func call//ne
    fu! Func()
        let @/ = 'inside func call'
      " ^-^
    endfu
    call Func()
    echo @/
    inside func call~

### What about the dot register?  Is it restored?

No:

    norm! o" outside
    echom @.
    fu! Func()
        norm! o" inside
        echom @.
        norm! .
    endfu
    call Func()
    echom @.
    " outside~
    " inside~
    " inside~
      ^----^
      after the function call, the dot register has not been restored

But it doesn't matter.
The dot command is not affected; it keeps its original behavior:

    norm! o" outside
    fu! Func()
        norm! o" inside
        norm! .
    endfu
    call Func()
    norm! .
    " outside~
    " inside~
    " inside~
    " outside~
      ^-----^
      after the function call, the dot command still repeats the last command performed *before* the function call

In fact, as soon as you use it, the `.` register is restored:

    norm! o" outside
    fu! Func()
        norm! o" inside
        norm! .
    endfu
    call Func()
    norm! .
    echom @.
    " outside~

##
## What's stored in the search register `"/`?

The last search pattern used in one of these commands:

    /
    ?
    :s
    :g
    :v

### Which command(s)/option(s) does it affect?

Its contents determines:

   - where `n` and `N` jump
   - the text which is highlighted when `'hlsearch'` is on
   - the text selected by `gn`

### When does the search register differ from the last entry in the search history (`histget('/')`)?

The search history only logs patterns which  were actually used in a `:s`, `:g`,
`:v`, `/`, `?` command.  If you reset  `@/` via `:let`, only the search register
is affected:

    /pat
    :let @/ = 'reset'
    :echo histget('/')
    pat~
    ^-^
    different than 'reset'

###
### What happens if I run `:let @/ = ''` then press `n`?

Vim resets  the search register  with the pattern used  in the last  `:s`, `:g`,
`:v` command.  It then jumps to the next occurrence of this pattern.

    :s/sub//en
    /slash
    :let @/ = ''
    norm! n
    " 'n' jumps to the next occurrence of 'sub'

#### What if I also remove the search register from the history (`:call histdel('/', @/)`) before pressing `n`?

Vim adds the search register back into the history.

    :s/sub//en
    /slash
    :call histdel('/', @/)
    :let @/ = ''
    norm! n
    " 'n' still jumps to the next occurrence of 'sub'

###
## Which features are specific to the expression register `"=`?  (2)

It's the only register which evaluates what you write into it:

    "=1+2 CR p

This should paste `3` and not `1+2`.

---

You can't separate the writing step from the execution/insertion step:

    let @= = 'dd'

Here, we've written an expression into the register.
But if you  try to refer to it (via  `@`, `"`, `C-r`), Vim still asks  you for a
new expression, which in effect makes the previous writing step irrelevant.

In contrast, you can write into a regular register:

    let @r = 'dd'

And later, you can refer to it  (`@r`, `"r`, `C-r r`) without having to redefine
its contents.

## What happens after pressing `C-r =` or `"=` if I don't provide any expression?

The evaluation of the last expression is used:

    $ vim -Nu NONE
    " press:  C-r = 1 + 1 Enter
    " result: 2 is inserted
    " press:  C-r = Enter
    " result: 2 is again inserted

##
## In which register does Vim save
### the last yanked text?

In the numbered register `0`:

    $ vim -Nu NONE -i NONE +"pu='if anything remember this'"
    :norm! wwy$
    :echo @0
    remember this~

Unless you specified another explicit register:

    $ vim -Nu NONE -i NONE +"pu='if anything remember this'"
    :norm! ww"ry$
    :reg 0r
    c  "r   remember this~

### the last changed or deleted text smaller than one line?

In the small delete register `-`:

    $ vim -Nu NONE -i NONE +"pu='once upon DELETEME a time'"
    :norm! wwde
    :echo @-
    DELETEME~

See `:h quote_-`.

### the last changed or deleted text bigger than one line?

In the numbered register `1`:

    $ vim -Nu NONE -i NONE +"pu=['once', 'upon', 'DELETE', 'ME', 'a', 'time']"
    :3,4d
    :echo @1
    DELETE~
    ME~

See: `:h quote_number`.

#### What's the side-effect of such a change/deletion?

The last big change/deletion which was stored in `"1` is shifted into `"2`.
The last but one change/deletion which was stored in `"2` is shifted into `"3`.
The process repeats itself until `"9`.
Whatever was stored in `"9` is now lost.

###
### When does Vim use a different register for a small changed/deleted text?

When you combine the change or delete operator with one of these motions:

    `{a-z}
    '{a-z}
    %
    n
    N
    /
    ?
    (
    )
    {
    }

In that case, Vim always uses the `"1` register (in addition to `"-`).

    $ vim -Nu NONE -i NONE +"pu='once upon (DELETE ME) a time'"
    :norm! wwd%
    :reg 1-
    c  "1   (DELETE ME)~
    c  "-   (DELETE ME)~

    $ vim -Nu NONE -i NONE +"pu='once upon (CHANGE ME) a time'"
    :norm! wwc%replacement
    :reg 1-
    c  "1   (CHANGE ME)~
    c  "-   (CHANGE ME)~

Rationale: These motions can jump to another  line; when used after an operator,
they can span multiple lines, and the resulting text can be considered as "big".
But this is on  a per-motion basis; so instead of parsing  the text to determine
whether it's big for each single motion, Vim probably prefers to simply consider
it as "big" by default.

### In which case doesn't Vim use any of these special registers?

When you:

   - yank some text, or change/delete a text smaller than one line
   - provide an explicit register to the command

Then the text is only saved into that register.

Examples:

    $ vim -Nu NONE -i NONE +"pu='if anything remember this'"
    :norm! ww"ay$
    :echo @0
    ''~

    $ vim -Nu NONE -i NONE +"pu='once upon DELETEME a time'"
    :norm! ww"bde
    :echo @-
    ''~

---

This exception does not affect a big change/deletion:

    $ vim -Nu NONE -i NONE +"pu=['once', 'upon', 'DELETE', 'ME', 'a', 'time']"
    :3,4d c
    :reg 1
    l  "1   DELETE^JME^J~

Which seems to contradict the documentation at `:h quote_number`:

>     Numbered register 1 contains the text deleted by the most recent delete or
>     change command, **unless the command specified another register**

But, oh well...

### What happens when I specify a numbered register bigger than 0 before a yank/delete/change operator?

If your text is  bigger than 1 line and you use a  deletion, then Vim writes the
text in the register 1 *and* in the register you specified +1.
For example, `"3dd` writes the current line in the registers 1 and 4.

    $ vim -Nu NONE -i NONE +"pu='some text'"
    "3dd
    :reg 123456789
    l  "1   some text^J~
    l  "4   some text^J~

---

In all other cases, the text is only written in the register you specified.

    $ vim -Nu NONE -i NONE +"pu='some text'"
    "3diw
    :reg 123456789
    c  "3   some~

The  old contents  from  the numbered  register is  *not*  shifted into  another
numbered register; it's lost.

    $ vim -Nu NONE -i NONE +"pu='some text'" +"pu='some other text'"
    1G
    "3yy
    2G
    "3yy
    :reg 123456789
    c  "3   some other text^J~

##
# Macro
## I'm recording some keys into a register to execute the latter as a macro
### how to assert that my cursor is on a whitespace?

Run this search command:

    /\%#\s

It should not make the cursor move, but it will only succeed if the cursor is on a whitespace.

### how to assert that my cursor is before the mark 's'?

Run this search command:

    /\%#\%<'s

### how to reliably create a new line with the exact same indentation as the current line?

Duplicate the line with `:t` or `yy` and  `p`, then press `C` to change the rest
of the line as you see fit.

This  works  because   when  Vim  puts  the  duplicated  line,   the  cursor  is
automatically positioned on the first non-whitespace character.

    $ vim -Nu NONE -i NONE -S <(cat <<'EOF'
        set list showcmd ai
        let lines = range(1,8)->map({_,v -> repeat(' ', v)..repeat("\t", v < 5 ? 1 : 2)..'some line'})
        call setline(1, lines)
        g/^\s/pu=''
        norm! 1G1|
    EOF
    )

    " press: qqq
             qq
             yyp
             C another line Esc
             /^\s CR
             @q
             q
             :set nows
             @q

---

Do *not* press `cc` instead of `C`.
`cc`  will only  preserve  the  current indentation  if  `'autoindent'` is  set;
otherwise, it will change the whole line, including the indentation.

---

Alternatively, you could yank the indentation of the current line:

    y/\S

Then insert it on your new line with `C-r C-o "`.

Pitfall1:  when opening  your new  line, the  auto indentation  may add  an extra
indentation; you need to temporarily leave  insert mode to undo this, before you
can safely insert the yanked indentation.

Pitfall2: if  the current line  has no indentation,  `y/\S` will still  yank its
first character.  This is not what you want.
To avoid  inserting a wrong  indentation, during  the recording, you  may assert
that the current line has some indentation with:

    0
    /\%#\s

If the assertion fails, `E486` will be raised and the macro will stop.

##
## How to execute a macro on several consecutive lines?

Execute the macro via `:norm!`:

    :12,34norm! @q
     ^---^
     range of lines on which the macro will be executed

---

Remember that  we have a  mapping to execute  a macro on  each line in  a visual
selection:

    :xno <silent> @ :<c-u>exe "'<,'>norm @"..nr2char(getchar())<cr>

Use it to repeat a macro on an arbitrary range of lines.

## My macro needs to move the cursor at the start of the line.  I forgot to record this motion!

Exexute the macro via `:norm!` *with* a range.

    ✘
    :norm! @q

    ✔
    :.norm! @q
     ^

With a range,  `:norm` will automatically move  the cursor at the  start of each
line inside the latter.  Without a range, `:norm` would just press the keys from
the current cursor position.

##
## I need a macro for a complex edition.  How to simplify the process a little?

Break it down into simple editions.
Work out a reliable macro for each of them:

    qa
    ...
    q

    qb
    ...
    q

    ...

During your final recording, execute your simple macros when needed:

     ┌ final
     │
    qf
    ...
    @a
    ...
    @b
    ...
    q

Execute your final macro:

    @f

## What happens if I run `:@q`?

`@q` is expanded into  the contents of the register `q`;  the result is executed
as one or several Ex commands.

    :let @a = 'echo "hello"'
    :@a

Had you pressed `@q` from normal  mode, the contents would have been interpreted
as normal commands.

Bottom line: how `@q` is interpreted depends on the current mode.

---

Note that this only works if `'cpo'` contains the `e` flag, which is the case by
default.  If it does not, you'll need to press CR manually.

    :set cpo-=e
    :let @q = 'echo "test"'
    :@q
    " press CR

From `:h cpo-e`:

>     *cpo-e*
>     ...
>               If this flag is not present, the register
>     is not linewise and the last line does not end in a
>     <CR>, then the last line is put on the command-line
>     and can be edited before hitting <CR>.

##
## How to execute a recursive macro?

Start by clearing the register in which you want to record keys:

    qxq
     ^
     name of the register in which you want to record keys

Start recording as usual:

    qx

Run whatever commands you want to record.

Press `@x` so that the macro recalls itself.
For this to work properly, it's important that you cleared the register at the start.

Finally, stop recording by pressing `q`.

### How to make sure it doesn't re-execute itself indefinitely?

Record  it  so that  an  error  is encountered  at  some  point, and  Vim  stops
processing the macro.

Such  an error  could  be triggered  by  a  disallowed motion,  which  is why  –
before executing  a recursive  macro –  you want `'whichwrap'`  to be  empty and
`'wrapscan'` to be reset, so that a maximum of motions are disallowed.

### How to make it stop at an arbitrary position?

Before starting recording, press `ms` to  set the mark `s` (mnemonic: *s*top) on
the desired position.  Then, as soon as you start recording, run this:

    /\%#\%<'s

This last command should assert that your cursor is before the mark `s`.
When this  assertion fails, `E486` should  be raised, which in  turn should stop
the macro.

If you're sure that the macro will recall itself at a position *after* the mark,
and thus  sure that  `E486` will  be raised,  then you  shouldn't need  to reset
`'wrapscan'` to prevent an infinite loop.

---

If you want to practice, run this:

    $ vim -Nu NONE +'pu=range(1,100)|%j|s/0 \zs/\r/g'
    " set the mark 's' on the first digit of the first number you do *not* want to increment
    " press: qqq
             qq
             /\%#\%<'s
             C-a
             w
             @q
             q
             gg
             @q

All the numbers should be incremented until the mark `s`.

### How to turn an existing non-recursive macro into a recursive one?  (2)

Execute:

    :let @x ..= '@x'

Or press:

    qX@xq

##
## I have a macro which needs to execute another recursive macro, then some commands:

    let @a = "@bvip:v/x/d_\r\e"
    let @b = '^lllyyp$2hd^k$x@b'

The purpose  is to  get a  list of all  three-characters subsequences  from some
arbitrary text line, but only if they contain the character `x`.

The main macro, `@a`, executes `@b` to break the line.
Then, it runs `:v` to remove the lines which don't contain `x`.

You can test `@b` on this line (make sure `'ww'` does not contain `l`):

    abcxdefxghi

It's correctly broken into:

    abc
    bcx
    cxd
    xde
    def
    efx
    fxg
    xgh
    ghi

### The main macro doesn't work!  Why?

I get this:

    abc
    bcx
    cxd
    xde
    def
    efx
    fxg
    xgh
    ghi

Instead of this:

    bcx
    cxd
    xde
    efx
    fxg
    xgh

For `@b` to stop, an error needs to be encountered.
That's the purpose of `lll`; it will fail on a line with fewer than 4 characters.
IOW, when the macro  has broken the line into so many  pieces that the remaining
text contains only 3 characters, it stops re-calling itself.

But this error prevents Vim from processing the rest of the `@a` macro.

You have 2 seemingly contradicting requirements.
On the one hand, you need an error for `@b` to stop.
On the other hand, you need to prevent any error so that `@a` is processed entirely.

### How to fix it?

Don't run `@b` directly; run it from `:norm`.
No error is raised by `:norm`, even if you ask it to run an invalid command:

    " ✔
    :norm! :not a cmd^M
                     ^^
                     literal carriage return

Applied to our issue, it gives:

    let @a = ":norm!@b\rvip:v/x/d_\r\e"
              ^----^

This time, `@a` should get you:

    bcx
    cxd
    xde
    efx
    fxg
    xgh

---

Do *not* use `silent!`, it would make Vim *ignore* any error while pressing the keys:

    let @a = ":sil! norm!@b\rvip:v/x/d_\r\e"
               ^--^
               ✘

You need the error *not* to be ignored for `@b` to stop.

##
## During a recording, I press a key which is mapped.  The rhs invokes `feedkeys()`.  Does Vim record the fed keys?

No, unless you pass the `t` flag to `feedkeys()`:

    $ vim -Nu NONE +'nno <expr> <c-a> feedkeys("<c-b>")[-1]'
    " press:
             qq
             C-a
             q
    :reg q
    c  "q   ^A~

                                                         v
    $ vim -Nu NONE +'nno <expr> <c-a> feedkeys("<c-b>", "t")[-1]'
    " press:
             qq
             C-a
             q
    :reg q
    c  "q   ^A^B~
              ^^

With the  `t` flag, the key  is not processed  as if it  came from the rhs  of a
mapping, and Vim records it.

---

For this reason, use the `t` flag only when it's really necessary.
Otherwise, the replay of a macro may give an unexpected result:

    $ vim -Nu NONE +'set wcm=9 | cno <expr> <s-tab> feedkeys("<s-tab>", "int")[-1]' +"pu='some text'"
    " press:
    "        qq : Tab Tab Tab S-Tab CR
    "        q
    "        @q

The macro should  replay `:#` which should print the  current line; instead, Vim
runs `:!`.

With the `t` flag, when you press `S-Tab`, a second `S-Tab` is recorded.
Because  of  that,  the  recording  contains  *two*  `S-Tab`,  instead  of  just
one.  One for  the `S-Tab` you've pressed interactively, and  another one fed by
`feedkeys()`.

##
# Tricks
## How to force a characterwise or blockwise register to be put linewise?

In command-line mode, use `:put`.

    $ vim -Nu NONE +"pu=['a', 'b']"
    :exe "norm! ggy\<c-v>j"
    :norm! p
    aa~
    bb~

    :undo
    :pu
    a~
    a~
    b~
    b~

In a script, use `setreg()` to reset the type of the register:

    :call getreginfo('"')->extend({'regtype': 'l'})->setreg('"')
                                               ^
                                               linewise

---

In insert mode, you can use `C-r`, but it only works for a blockwise register.

##
## How to review the numbered registers 7, 8, 9?

    "7p
    u.
    u.

### How does this work?

When you provide a  numbered register to a command or  operator, the dot command
does not  repeat the exact  same command;  it increments the  numbered register;
when 9 is reached, it keeps using the register 9 (it doesn't get back to 1).

This is documented at `:h redo-register`.

## How to move 3 non-consecutive big texts (>= 1 line) to non-consecutive new locations?

    " delete a line
    dd
    " delete two lines, anywhere else
    dj
    " delete a paragraph, anywhere else
    dip

    " paste the last deleted paragraph, anywhere you want
    "1p
    " paste the previous deleted block of 2 lines, anywhere else
    .
    " paste the first deleted line, anywhere else
    .

Replace `p` with `P` to paste above:

    "1P
    .
    .

### What if I want to move small texts?

Specify an explicit numbered register for the first deletion:

    " delete a word
    "1daw
    " delete another word, anywhere else
    .
    " delete yet another word, anywhere else
    .

    " paste the last deleted word, anywhere you want
    "1p
    " paste the previous deleted word lines, anywhere else
    .
    " paste the first deleted word, anywhere else
    .

Since the dot command automatically increments a numbered register, this is equivalent to:

    "1daw
    "2daw
    "3daw
    "1p
    "2p
    "3p

## How to duplicate 3 non-consecutive texts to non-consecutive new locations?

    " yank a line
    "1yy

    " yank another line, anywhere else
    "2yy

    " yank yet another line, anywhere else
    "3yy

    " paste the last yanked line, anywhere you want
    "1p

    " paste the previous yanked line, anywhere else
    .

    " paste the first yanked line, anywhere else
    .

Note that you're not limited to lines; you can yank any text-object, motion.

---

You may wonder why  you need to specify the numbered  register for each yanking,
while you don't for deletions/changes.

That's because  yanking and  deletions/changes are  2 very  different mechanisms
when it comes to registers.

By default, Vim writes a yanked text into  register 0, not 1.  And when you yank
another text, it's also written into register 0 (the old contents is not shifted
to  another register).   If you  want to  build a  stack of  texts, you  need to
specify where each yank has to be written; Vim won't do it for you here.

### The yanking is too tedious!

Include the flag `y` into `'cpo'` so that the dot command can also repeat a yank:

    :set cpo+=y

After that the yanking becomes:

    " yank a line
    "1yy

    " yank another line, anywhere else
    .

    " yank yet another line, anywhere else
    .

##
## What's the simplest way to change the alternate file of the current window without any side-effect?

The `#` register is writable.
Simply write the new desired file path in it:

    let @# = '/path/to/new/alternate/file'

This will affect the behavior of `:b#` and `C-^`.

---

Note that the new alternate file must match an existing buffer.

    sil! exe 'bw! '..$MYVIMRC
    let @# = $MYVIMRC
    E94: No matching buffer for ...~

Make sure it exists:

    if !bufexists($MYVIMRC)
        call bufadd($MYVIMRC)
    endif
    let @# = $MYVIMRC

## I have a listing of files A, and another file B.  How to check that all the files from A are present in B?

Use a macro.

Focus A, and press:

   1. `gg`: jump to start of file
   2. `qqq`: empty register `q`
   3. `qq`: start recording in register 'q'
   4. `^y$`: yank the current file path
   5. `C-w w`: focus file B
   6. `G$`: jump to the end of the file
   7. `? ^ \V C-r " \m $ CR`: look for the file path you've just yanked in file B
   8. `C-w w j`: focus back the listing A and move to the next file path
   9. `@q`: make the macro recursive
   10. `q`: stop recording

Now, from the top of the listing A, execute your macro `q`.
If no error is raised, then all the files from the listing A are present in B.

But if a file from the listing A is missing in B, then `E486` should be raised:

    E486: Pattern not found: ^\V/path/to/missing/file\m$
                                ^-------------------^

---

Note that it's important to look for the file path with the `?` command, and not
`/`. Since  file paths in Linux  use the slash  as a delimiter, the  `/` command
would not be able to find a file path without the delimiters being escaped.

And note  that the `?` command  suffers from a  similar issue; i.e. it  won't be
able to find a file path containing a question mark; although, in practice, such
a file  path should be  rare, since  a question mark  is a metacharacter  in the
shell, and thus known to cause issues in general.

---

If you want to practice, run this:

    vim -Nu NONE -S <(cat <<'EOF'
        %d_
        " populate listing A
        pu!='/path/to/file1'
        exe 'norm! yy'..(winheight(0)-1).."p2GVGg\<c-a>gg"
        update
        " focus file B
        wincmd w
        %d
        " import listing A
        0r#
        " remove random existing line whose address is above or equal to 5
        let seed = srand()
        let random = 5 + rand(seed) % (winheight(0)-4)
        exe random..'d_'
        wincmd w
    EOF
    ) -O /tmp/listingA /tmp/fileB

##
# Pitfalls
## When should I avoid `:let` to set (!= restore) a register?  (2)

When the value you assign contains a NUL, because Vim will translate it into a NL.

This issue is explained at `:h NL-used-for-NUL`.

---

Also when it ends with a CR, because Vim will append a literal `C-j`:

    let @q = ":\r"
    reg q
    "q   :^M^J
            ^^

And because of that, when you execute your macro, `C-j` will be pressed.
If you've mapped something to `C-j`, it will have unexpected effects.

Example when CR is pressed in command-line mode:

    vim -Nu NONE +'let @q = ":\<cr>"' +'nno <c-j> :echom "this should NOT be executed"<cr>'
    " press @q: the C-j mapping is executed (the message is logged)

Example when CR is pressed in normal mode:

    vim -Nu NONE +"pu=''" +'let @q = "\<cr>"' +'nno <c-j> :echom "this should NOT be executed"<cr>'
                  ^-----^
                  there needs to be a line after the one from which we press `@q`,
                  otherwise, `^M` would fail and Vim would stop executing the macro

This issue is explained at `:h :let-@`:

>     If the result of {expr1} ends in a <CR> or <NL>, the
>     register will be linewise, otherwise it will be set to
>     characterwise.

`:let` sets a register ending with CR to linewise; and in a linewise register, a
line must always end with `C-j`.

### What should I use instead?

For the first issue, use `setreg()` and pass the value as a list, not as a string:

                                                  ✘
                                                  v------v
    $ vim -es -Nu NONE -i NONE +'call setreg("q", "a\x0ab", "c")' +'pu=execute(\"reg q\") | %p | qa!'
    Type Name Content~
      c  "q   a^Jb~
               ^^
               NUL has been translated into NL

                                                  ✔
                                                  v--------v
    $ vim -es -Nu NONE -i NONE +'call setreg("q", ["a\x0ab"], "c")' +'pu=execute(\"reg q\") | %p | qa!'
    Type Name Content~
      c  "q   a^@b~
               ^^
               NUL has been preserved

---

For the second issue, use `setreg()` and pass it the third argument `c`:

                                                                v
    $  vim -es -Nu NONE -i NONE +'call setreg("q", [":\<cr>"], "c")' +'pu=execute(\"reg q\") | %p | qa!'
    Type Name Content~
      c  "q   :^M~

The `c`  flag prevents  Vim from processing  the contents of  the register  as a
*line* of text, which would cause a trailing `^J` to be added.

Source: <https://groups.google.com/d/msg/vim_use/-pbK15zfqts/jfxLV8zXlC8J>

##
## Why should I never save the contents of a register as a string, to restore it later?

If your register contains a NUL, it will be translated into a NL.
Later,  when you'll  try to  restore  the original  contents, this  NL won't  be
translated back into a NUL, because Vim has no way to distinguish between a real
NL and one which results from the translation of a NUL.

    vim -es -Nu NONE -i NONE -S <(cat <<'EOF'
        call setline(1, "original:  a\x0ab\x0ac")
        norm! ^fa"ry$
        let save = [getreg('r'), getregtype('r')]
        "           ^---------^
        call setreg('r', save[0], save[1])
        pu='restored:  '..execute('reg r')->split('\n')[1]->matchstr(':\s*\zs.*')
        %p
        qa!
    EOF
    )

    original:  a^@b^@c~
    restored:  a^Jb^Jc~
                ^^ ^^
                ✘  ✘

See `:h getreg() /NL`:

>     If {list} is present and |TRUE|, the result type is changed
>     to |List|. Each list item is one text line. Use it if you care
>     about zero bytes possibly present inside register: without
>     third argument both NLs and zero bytes are represented as NLs
>     (see |NL-used-for-Nul|).

See also: <https://github.com/vim/vim/pull/3370#issuecomment-415975411>

>     It is  essential that  it must  be a  list of  strings, you  can't restore
>     registers which have embedded NUL otherwise.

---

OTOH, if you save the register as a  list, and it contains a NUL, Vim will still
translate it as a NL:

    vim -es -Nu NONE -i NONE -S <(cat <<'EOF'
        call setline(1, "a\x0ab")
        norm! ^"ry$
        set vbs=1 | echo getreg('r', 1, 1)
        "                               ^
        qa!
    EOF
    )

    ['a~
    b']~

*But* when you'll restore it, Vim will know that it's not a real NL because it's
inside  a single  list item;  and a  list item  describes *one*  text line,  not
several, which  – by definition  – can't  contain a NL.   As a result,  Vim will
translate it back into a NUL.

    vim -es -Nu NONE -i NONE -S <(cat <<'EOF'
        call setline(1, "original:  a\x0ab\x0ac")
        norm! ^fa"ry$
        let save = [getreg('r', 1, 1), getregtype('r')]
        "                          ^
        call setreg('r', save[0], save[1])
        pu='restored:  '..execute('reg r')->split('\n')[1]->matchstr(':\s*\zs.*')
        %p
        qa!
    EOF
    )

    original:  a^@b^@c~
    restored:  a^@b^@c~

---

Note that this is a theoretical issue.
In  practice, you  should  never use  `getreg()` and  `getregtype()`  to save  a
register.  Instead,  you should use  `getreginfo()` which contains all  the info
you need (and even more thanks to  the `isunnamed` key), and avoids this pitfall
because  it always  return the  contents of  a register  as a  list (never  as a
string).

## I need to use the contents of the register `r` as a pattern.  How should I refer to the latter?

    getreg('r', 1, 1)->join('\n')

---

Do *not* write `@r`.

If `"r` contains a newline, it would be translated into a NUL when expanding `@r`.

    vim -Nu NONE -i NONE -S <(cat <<'EOF'
        call setreg('r', ['a', 'b'], 'l')
        call setline(1, ['a', 'b', "a\nb\n"])
        call matchadd('ErrorMsg', @r)
        "                         ^^
        "                         ✘
        call matchadd('Search', getreg('r', 1, 1)->join('\n'))
    EOF
    )

This is  similar to  Vim inserting  a NUL on  the command-line  when you  try to
insert a NL by pressing `C-v C-j`.

Exceptions:  The  search and  expression registers can't  contain more  than one
item.  See `:h E883`.  So, it's ok to write `@/` or `@=` inside a pattern.

##
## `@@` does not replay my last macro as expected!

The last macro is not necessarily the one you've executed interactively.
Indeed, the latter could have executed another (nested) macro.  If so, then this
other macro *is* the last one.

    vim -Nu NONE +'let @a = "a@a\e@b" | let @b = "a @b \e"'
    " press @a: '@a @b ' is inserted
    " press @@: ' @b'    is inserted

Here, notice how  `@@` repeats `@b`, even though the  last macro you've executed
interactively was `@a`.

---

During a recording, if  you use a mapping whose rhs contains  `@=` , when you'll
execute the resulting register (let's say  `q`), the mapping will cause the last
macro to be  reset to `@=`. Which  means that – subsequently –  `@@` will replay
`@=` and not `@q`.

### How to avoid this pitfall in the future?

You could  install wrapper mappings around  `@` and `@@` to  save/re-execute the
last register which was executed *interactively*.

    vim -Nu NONE -S <(cat <<'EOF'
        let @a = "a@a\e@b" | let @b = "a @b \e"

        nmap <expr><unique> @ <sid>fix_macro_execution()
        fu s:fix_macro_execution() abort
            let char = nr2char(getchar(), 1)
            if empty(reg_executing())
                let s:last_register_executed_interactively = char
            endif
            return '@'..char
        endfu

        nmap <expr><unique> @@ <sid>atat()
        fu s:atat() abort
            return '@'..get(s:, 'last_register_executed_interactively', '@')
        endfu
    EOF
    )

##
## During a recording, after `o` or `O`, do *not* press `C-u` to remove all the indentation of the current line.

Prefer pressing `Escape` then `i`.

Rationale: there  is no  guarantee that  the next time  you execute  your macro,
there will be an indentation; it depends from where you open a new line.  And if
there's no indentation, `C-u` may remove the previous newline.

    vim -Nu NONE <(cat <<'EOF'
        indented
    NOT indented
    EOF
    ) +'set autoindent backspace=eol,start | let @q = "o\<c-u>\<esc>"'

    " press @q on the first line: a new line is opened below
    " press @q on the second line: NO new line is opened below,
    " because C-u has immediately removed the newline added by the 'o' command

##
## My macro doesn't work as expected, unless I disable `exe "set <m-x>=\ex"`?

Cause:

When you  execute the register, Vim  wrongly translates the sequence  `\ex` into
the terminal key `<M-x>`:

    vim -es -Nu NONE -S <(cat <<'EOF'
        set ttm=10
        exe "set <m-f>=\ef"
        0pu=['b.', 'b.']
        1
        let @q = "ia.\ef.ac\e"
        1,2norm! @q
        %p
        qa!
    EOF
    )

    " outputs:

        a.æ.acb.
        a.æ.acb.

    " expected:

        a.b.c
        a.b.c

This issue does not affect a recording thanks to the patch [8.1.1003][1].
I think that, during a recording, Vim  adds a no-op after any escape produced by
pressing the Escape key interactively.

Solution:

Replace any  escape character which is  not part of a  terminal escape sequence,
with a `<c-\><c-n>` sequence:

    ✘
    let @q = "ia.\ef.ac\e"
                 ^-^

    ✔
    let @q = "ia.\<c-\>\<c-n>f.ac\e"
                 ^----------^

Don't use `<c-c>`; it would prevent `InsertLeave` from being fired.

##
# Issues
## When executing a register, one of my mapping is used.  It should not!

When Vim  executes a  register, it  seems that sometimes,  there's some  kind of
"lag" before a mode  is quit.  You don't experience this  lag during a recording
though, maybe because you don't type as fast as Vim...  It looks like a bug.

Examples:

    vim -Nu NONE -S <(cat <<'EOF'
        let @q = 'Vr-x'
        xno <expr> x Func()
        fu Func()
            echom 'x mapping is used'
            return ''
        endfu
        pu!='some text'
        au VimEnter * call feedkeys('@q')
    EOF
    )

    :mess
    x mapping is used~

    vim -es -Nu NONE -S <(cat <<'EOF'
        ono foo bar
        let @q = "ctdfoo\<esc>"
        pu!='abcd'
        call feedkeys('@q', 'x')
        %p
        qa!
    EOF
    )

    bard~
    ^-^
    should be foo

As a workaround, try to press `Esc` to be sure that the rest of the commands are
processed in the mode you expect:

    vim -Nu NONE -S <(cat <<'EOF'
        let @q = "Vr-\ex"
        "            ^^
        xno <expr> x Func()
        fu Func()
            echom 'x mapping is used'
            return ''
        endfu
        pu!='some text'
        au VimEnter * call feedkeys('@q')
    EOF
    )

    :mess
    ''~

If the mode you expect is not normal, use a no-op instead of `Esc`:

    vim -es -Nu NONE -S <(cat <<'EOF'
        ono foo bar
        let @q = "ctd\<c-r>=''\<cr>foo\<esc>"
        "            ^------------^
        pu!='abcd'
        call feedkeys('@q', 'x')
        %p
        qa!
    EOF
    )

    food~

See also:

- <https://github.com/vim/vim/issues/3021#issuecomment-639978098>
- <https://github.com/vim/vim/issues/3678#issuecomment-639992731>

##
# Reference

[1]: https://github.com/vim/vim/releases/tag/v8.1.1003
