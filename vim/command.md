# Command-line
## What are the two possible special meanings of a bar on the command-line?

In a regex, it can be used to express an alternation.
Outside, it can be used to separate 2 commands.

## What happens if I escape a bar?

In a magic (`\m`) regex, it becomes SPECIAL (alternation).

Outside, it becomes a REGULAR character.
It makes  the bar  (and what follows)  included in the  argument of  the current
command:

    :e abc|def
    E492: Not an editor command: def    ✘~

    :e abc\|def
    edits the file 'abc|def' ✔~

##
## When does Vim remove a backslash outside of a quoted string?

    ┌──────────────────┬────────────────────────────────────────┐
    │ your command use │ a backslash is removed in front of any │
    ├──────────────────┼────────────────────────────────────────┤
    │ -bar             │ |                                      │
    ├──────────────────┼────────────────────────────────────────┤
    │ <f-args>         │ whitespace, backslash                  │
    ├──────────────────┼────────────────────────────────────────┤
    │ -bar + <f-args>  │ |, whitespace, backslash               │
    └──────────────────┴────────────────────────────────────────┘

## What's the output of these commands?

    fu Func(...) abort
        for i in a:000
            " replace a trailing whitespace with `S`
            echo substitute(i, '\s\+$', '\=repeat("S", len(submatch(0)))', '')
        endfor
    endfu

    com -nargs=* Cmd  call Func(<q-args>)

    Cmd ab         ↣ 'ab' ↢
    Cmd a\b        ↣ 'a\b' ↢
    Cmd a\ b       ↣ 'a\ b' ↢
    Cmd a\  b      ↣ 'a\  b' ↢
    Cmd a\\b       ↣ 'a\\b' ↢
    Cmd a\\ b      ↣ 'a\\ b' ↢
    Cmd a\\\b      ↣ 'a\\\b' ↢
    Cmd a\\\ b     ↣ 'a\\\ b' ↢
    Cmd a\\\\b     ↣ 'a\\\\b' ↢
    Cmd a\\\\ b    ↣ 'a\\\\ b' ↢

    com -nargs=* Cmd  call Func(<f-args>)

    Cmd ab         ↣ 'ab' ↢
    Cmd a\b        ↣ 'a\b' ↢
    Cmd a\ b       ↣ 'a b' ↢
    Cmd a\  b      ↣ 'a ', 'b' ↢
    Cmd a\\b       ↣ 'a\b' ↢
    Cmd a\\ b      ↣ 'a\', 'b' ↢
    Cmd a\\\b      ↣ 'a\\b' ↢
    Cmd a\\\ b     ↣ 'a\ b' ↢
    Cmd a\\\\b     ↣ 'a\\b' ↢
    Cmd a\\\\ b    ↣ 'a\\', 'b' ↢

    com -bar -nargs=* Cmd  call Func(<f-args>)

    Cmd a|b         ↣ 'a'    `:b` is executed separately and has no visible effect ↢
    Cmd a\|b        ↣ 'a|b' ↢
    Cmd a\| b       ↣ 'a|' 'b' ↢
    Cmd a\|  b      ↣ 'a|', 'b' ↢
    Cmd a\\|b       ↣ 'a\|b' ↢
    Cmd a\\| b      ↣ 'a\|', 'b' ↢
    Cmd a\\\|b      ↣ 'a\|b' ↢
    Cmd a\\\| b     ↣ 'a\|', 'b' ↢
    Cmd a\\\\|b     ↣ 'a\\|b' ↢
    Cmd a\\\\| b    ↣ 'a\\|', 'b' ↢

##
# Custom command
## What's the name of everything written after `Test` in `com Test call Func()`?

It's called the replacement text:

    com Test call Func()
             ^^^^^^^^^^^

## How to list the help tags useful to create a custom command?

    :h :command- C-d

##
## Attributes
### What happens if I pass a negative count to a command as a prefix?

It's allowed, but  the count is not preserved; it's  subtracted from the current
line address:

    com -count  Test  echo <count>
    :-1 Test
    101~

    com -range  Test  echo <count>
    :-1 Test
    105~

#### As a suffix?

If raises `E488`:

    com -range Test echo <count>
    :Test -123
    E488: Trailing characters~

    com -count Test echo <count>
    :Test -123
    E488: Trailing characters~

###
### How to pass a DEFAULT negative count to a command?

Use `-range=-N`:

    com -range=-123 Test echo <count>
    :Test
    -123~

Note that `-count` can't pass a default negative count.

###
### How to detect whether the user has provided a count when they executed their command?

Use `-range=0`, or `-range=-1`.
In practice, the user would probably never use -1 or 0 as a count.

Note that  if you just  use `-range`,  and you don't  provide any count  to your
command, `<count>` will be replaced by `-1`.

MWE:

    com -nargs=* -range=0  Test  call Func(<count>)
    fu Func(count)
        if !a:count
            echo 'the command was executed WITHOUT count'
        else
            echo 'the command was executed WITH the count '.a:count
        endif
    endfu

    :Test hello
    the command was executed WITHOUT count~

    :123Test
    the command was executed WITH the count 123~

### Why should I avoid `-count=N` and prefer `-range=N` instead?

`<count>`  is  replaced  by  the  last  number  between  the  beginning  of  the
command-line and the first non-digit of the first argument.

So, if the first argument can be a number or can begin with a number, the latter
will be consumed to replace `<count>`:

    com -count -nargs=+ Test echo printf("count: %s\n<lt>q-args>: %s", <count>, <q-args>)
    :12Test 34abc
    count: 34~
    <q-args>: abc~

OTOH, `-range` doesn't allow you to pass  a count after the command name, and so
is immune to this issue.

###
### Some of my custom commands accept an unquoted regex as argument.  To which ones should I give the `-bar` attribute?

None.

    com -bar -nargs=* Cmd  call Func(<q-args>)
    fu Func(...) abort
        echo join(a:000)
    endfu

    Cmd pat1 \| pat2
    pat1 | pat2~

    Cmd pat1 \\| pat2
    pat1 \| pat2~

To send an unescaped bar to the function, the user would have to escape it.
And to send an alternation, the user would have to double the backslash.

This is inconsistent with how regexes are usually written.

And this is way too confusing; consider this:

    pat1 \| pat2
         ^^

What's this?
An alternation, or a simple bar?
Answer: it depends.

In a regex, it's an alternation.
In your poorly-defined command, it's a simple bar.

---

Vim removes  a backslash in front  of every bar,  because it knows that  you may
want to  include a bar in  the argument of the  command, and that to  do so, you
need to escape it.

---

Example: `:EasyAlign`

This command  is not defined with  `-bar` as it  would force the user  to double
escape a bar to make it an alternation:

    :EasyAlign */XXX\|YYY/
               ├─────────┘
               └ align around all (*) sequence of 3 X or 3 Y

For the same reason, these commands have not been given `-bar`:

    :CGrep
    :CGrepBuffer
    :Cfilter
    :Dlist
    :Ilist
    :LGrep
    :LGrepBuffer
    :LiveEasyAlign
    :LogiPat
    :PQ

### More generally, to which custom commands should I give `-bar`?

Most of them.

See the commands in [eunuch][1]: they all have the `-bar` attribute.

However, be CONSISTENT.

If the argument of your command may:

   - contain a bar
   - and be used in another context

Make sure that the bar will be parsed the same way in both contexts.

---

Example 1: `:Shdo`

`:Shdo` executes a shell command on a  set of files selected via the vim-dirvish
plugin.
A shell  command often contains  a bar to  pipe the output  of a command  to the
input of another.
Giving `-bar` to `:Shdo` would force the  user to escape every pipe, which would
be inconsistent with how the same pipeline is written in an interactive shell.
So, `:Shdo` is NOT given `-bar`.

---

Example 2: `:Cp`

This command copies the current file to another one.
It mimics `cp(1)`.
The shell interprets a bar as a pipe:

    $ cp foo bar|baz
    ✘ zsh: command not found: baz~

    $ cp foo bar\|baz
    ✔

Therefore, you  should give `-bar` to  `:Cp` so that its  behavior is consistent
with `cp(1)`.

And if you stumble upon a file whose  name contains a bar, you'll need to escape
it (like with `cp(1)`):

    :Cp bar\|baz

Btw, in case you wonder where the asymmetry comes from, between `:Shdo` which is
given `-bar`  and `:Cp` which is  not, it comes from  the fact that you  are not
trying to send the same kind of bar to the shell.
For `:Shdo`, you want to send a PIPE.
For `:Cp`, you want to send a LITERAL bar.

### If I use `-bar`, I can still write a literal bar by escaping it.  Is the reverse true?

No, outside a regex, escaping a bar makes it literal.
Not the other way around.
The backslash doesn't perform a 2-way transformation; it's a one-way street.

So, you can't make a literal bar become a command termination.

###
### Does `-complete=custom` perform a filtering on the returned candidates?

Yes, from `:command-completion-custom`:

> For the  "custom" argument, it is  not necessary to filter  candidates against
> the (implicit pattern in) ArgLead.

> Vim will filter the candidates with its regexp engine after function return, and
> this is probably more efficient in most cases.

> For  the "customlist"  argument, Vim  will  not filter  the returned  completion
> candidates and the user supplied function should filter the candidates.

This is a basic filtering over which you have no control.

For a candidate to be kept, it must simply begin with `a:arglead`.
The comparison respects `'ignorecase'` and `'smartcase'`

### Should I give the attribute `-complete=custom` or `-complete=customlist` to my completion function??

If  possible use  `-complete=custom`, because  its automatic  filtering is  more
efficient.

Use  `-complete=customlist` if  you need  to control  how the  filtering of  the
candidates will be performed.

###
### What's the difference between `-complete=file` and `-complete=file_in_path`?

    ┌──────────────────────────────────────┬─────────────────────────────┐
    │                 file                 │        file_in_path         │
    ├──────────────────────────────────────┼─────────────────────────────┤
    │ files/directories                    │ files/directories in 'path' │
    │ at the root of the working directory │                             │
    └──────────────────────────────────────┴─────────────────────────────┘

#### If I have to choose between the two, which one should I use?

`-complete=file` gives less  suggestions, and they will be more  relevant if you
configure the working directory to match  the root of the project you're working
on.

##### Which pitfall should I be aware of though?

Characters which are special on Vim's command-line will be automatically expanded:

    com -complete=file -nargs=1 Cmd call Func(<args>)
    fu Func(arg)
        echo a:arg
    endfu
    Cmd 'A%B'
    Acommand.mdB~
     ^^^^^^^^^^
       `%` has been expanded into the name of the current file

---

The same pitfall applies to `-complete=dir`.

####
#### If the local and global working directories are different, which one is used by these attributes?

The local one has always priority.

#### If I use `-complete=file_in_path` and 'path' has the value `.,**`, what will be suggested?

All the  files/directories at the root  of the directory containing  the current
file, and all the files/directories anywhere below the working directory.

###
### Inside a range `.`, `$` and `%` refer to lines addresses.  How to make them refer to buffers or windows?

Use the attribute `-addr=buffers` or `-addr=windows`.

    com Test echo <line1>
    :Test
    line 355~

    com -addr=buffers Test echo <line1>
    :Test
    buffer 11~

    com -addr=windows Test echo <line1>
    :Test
    window 1~

In all the previous commands, the line specifier `.` was implicit (i.e. `Test` ⇔ `.Test`).

Here's the full list of possible values:

    ┌────────────────┬──────────────────────────────────────────────────────────┐
    │ lines          │ default interpretation of `-addr`                        │
    ├────────────────┼──────────────────────────────────────────────────────────┤
    │ arguments      │ position in the arglist                                  │
    ├────────────────┼──────────────────────────────────────────────────────────┤
    │ buffers        │ position in the buffer list, including the unloaded ones │
    ├────────────────┼──────────────────────────────────────────────────────────┤
    │ loaded_buffers │ position in the buffer list, excluding "                 │
    ├────────────────┼──────────────────────────────────────────────────────────┤
    │ windows        │ window number                                            │
    ├────────────────┼──────────────────────────────────────────────────────────┤
    │ tabs           │ tabpage number                                           │
    └────────────────┴──────────────────────────────────────────────────────────┘

###
## Escape sequences
### In general, which escape sequence should I use: `<args>`, `<f-args>`, `<q-args>`?

If you need to:

   - pass non-scalar data like lists or dictionaries, use `<args>`

   - pass a list of strings, use `<f-args>`

   - parse the arguments according to arbitrary rules, use `<q-args>`
     (for example extract the value after a `-option`)

### Do I need to quote strings passed to my command with `<args>`?  `<f-args>`?  `<q-args>`?

You only need to quote them with `<args>`.

###
### If I use `<args>` to send arguments to a function, do I need to use commas to separate them?

Yes.

#### What if I use `<f-args>`?  `<q-args>`?

`<f-args>` will add commas automatically.
`<q-args>` will concatenate all arguments into  one big string, so there will be
nothing to separate.

###
### My command must act differently depending on the number of arguments it receives.  Which sequence should I use?

    <f-args>

Ofc, you could still split one big  string with `split()`, but it makes the code
a little longer.

### When is it necessary to use `<f-args>`?

When your arguments may contain whitespace.
You can then embed a whitespace inside an argument by escaping it.

From `:h <f-args>`:

> To embed whitespace into an argument of <f-args>, prepend a backslash.
> <f-args> replaces every pair of backslashes (\\) with one backslash.

You could use another escape sequence,  but the manual parsing would probably be
non-trivial; `<f-args>` give it to you for free.

### How is `<f-args>` replaced if I provide no argument to the command?

It's replaced with nothing.

    com -nargs=* Cmd  call Func(<f-args>)
    fu Func(...) abort
        echo a:000
    endfu

    :Cmd
    []~

### Does `<f-args>` always split the arguments passed to a custom command at spaces and tabs?

Only if your command is defined as accepting multiple arguments.
IOW, only if you gave the attribute:

    -nargs=*
    -nargs=+

But not with:

    -nargs=1
    -nargs=?

MWE:

    fu Func(...) abort
        echo a:000
    endfu

    com -nargs=* Cmd  call Func(<f-args>)
    Cmd a b c
    ['a', 'b', 'c']~

    com -nargs=+ Cmd  call Func(<f-args>)
    Cmd a b c
    ['a', 'b', 'c']~

    com -nargs=1 Cmd  call Func(<f-args>)
    Cmd a b c
    ['a b c']~

    com -nargs=? Cmd  call Func(<f-args>)
    Cmd a b c
    ['a b c']~

###
### How is `<count>` replaced if I use `-count` without any value, and I don't give a count to my command?

It's replaced by `0`:

    com -count -nargs=*  Test  echo <count>
    :Test
    0~

### Same question if I use `-range`?

It's replaced by `-1`.

    com -range -nargs=*  Test  echo <count>
    :Test

### How are `<line1>` and `<line2>` replaced if I use `-range` without any value, and don't pass any range?

They're both replaced with the current line address:

    com -range -nargs=*  Test  echo '<line1>,<line2>'
    :Test

### How is `<count>` replaced if I use `-count`, and pass the count `12` as a prefix, and the count `34` as a suffix?

The last line specifier is used, here `34`:

    com -count -nargs=*  Test  echo <count>
    :12Test 34
    34~

    :12,34Test 56
    56~

##
### How to get the number of line specifiers used in the range of the command?

Use the `<range>` escape sequence:

    com -range  Test  echo <range>
    :Test
    0~

    :12Test
    1~

    :12,34Test
    2~

##
## Function called by the custom command
### What are the two things to check at the very beginning to make it more reliable?

The syntax of the command:

    “are there enough arguments?”

and the sanity of the arguments when they're non boolean:

    “are they what the function expects?”

---

If the syntax is wrong, print a usage message:
```vim
    "  ┌ `match()` interpret its argument as a pattern;
    "  │ here `index()` is better, because it interprets it as a literal string
    "  │
    if index(args, '-kind') == -1 || index(args, '-filetype') == -1
        echo 'usage:'
        echo '    DebugLocalPlugin -kind ftplugin -filetype sh'
        echo '    DebugLocalPlugin -kind indent   -filetype awk'
        echo '    DebugLocalPlugin -kind syntax   -filetype python'
        return
    endif
```
If the arguments are not sane, print an error message:
```vim
    "         ┌ WHITELIST of expected values
    "         │ (don't use a blacklist, it's not restrictive enough)
    "         ├────────────────────────────┐
    if index(['ftplugin', 'indent', 'syntax'], kind) == -1
        echo 'you did not provide a valid kind; choose:  ftplugin, indent, or syntax'
        return

    elseif index(getcompletion('*', 'filetype'), filetype) == -1
        echo 'you did not provide a valid filetype'
        return
    endif
```
### Why should I pass the range of a command inside the arguments of the called function, and not before `:call`?

In the replacement text  of the command, if you position  the range right before
`:call`, the function will be called ONCE PER LINE in the range.

You could prevent this by giving the  `range` attribute to the function, but the
cursor would still jump to the first line in the range.

    fu Func() range
        echo ''
    endfu
    1,3call Func()
    the cursor jumps on the first line of the buffer~

The jump occurs BEFORE the function is called.
So, you wouldn't be able to save and restore the view inside the function.
You would have to  save the view in a buffer-local  variable BEFORE the function
is called,  and remove  it at the  end of  the function once  the view  has been
restored.
Too cumbersome.

### What's the value of `a:firstline` and `a:lastline` inside a function called without any range?

The address of the current line.

    fu Func()
        echo a:firstline == line('.') && a:lastline == line('.')
    endfu
    call Func()
    1~

### My command includes `<q-args>`.  Which built-in functions should I use to extract its arguments?

The command and the function will look like this:

    com Cmd call Func(<q-args>)
    fu Func(...)
        " ...
    endfu

Your arguments  could be  options with  values (e.g.  `-type file`),  or boolean
options (e.g. `-verbose`).

For the value of an option use `matchstr()`:

    let type = matchstr(a:1, '-type\s\+\zs[^- ]\S*')
                                            ││
                                            │└ the engine can backtrack because the previous atom
                                            │  is followed by a quantifier; don't let it backtrack
                                            │
                                            └ the next word could be another option
                                              we're not interested in this case

And to get a boolean option use `split()` and `index()`:

    " split the command-line at the right characters (probably spaces)
    let args = split(a:1, 'pat')

    let is_verbose = index(args, '-verbose') >= 0

#
# Built-in commands
## Can I pass an argument to the command invoked by the normal command `K`?

Yes, by prefixing it with a count, you can send the latter to the program stored in `'kp'`.

    set kp=:Test
    com -nargs=*  Test  echo <q-args>
    " press 3K on the word 'hello'
    3 hello~

## When I run `:bufdo cmd`, why is `cmd` executed in *every* buffer even if `cmd` raises an error in one of them?

    $ vim -Nu NONE +"bufdo echo x" /tmp/file{1..3}

    E121: Undefined variable: x~
    "/tmp/file2" 0 lines, 0 characters~
    E121: Undefined variable: x~
    "/tmp/file3" 0 lines, 0 characters~
    E121: Undefined variable: x~

You could  think that Vim would  stop iterating over  the buffers as soon  as an
error is raised in one of them, because according to `:h :bufdo`:

>     When an error is detected on one buffer, further
>     buffers will not be visited.

But in reality, an error stops `:bufdo` only when it's raised while visiting the
next buffer, not when executing `cmd`:

    $ vim -Nu NONE +"bn|pu='text'|set hidden|bp|set nohidden|bufdo echo 'msg'" /tmp/file{1..3}
    msg~
    msg~
    Error detected while processing command line:~
    E37: No write since last change (add ! to override)~

Notice how `msg` is printed only twice.

The same is true for all the `:xdo` commands (e.g. `:argdo`, `:windo`, ...).

---

>     I would say this works as intended, since it's the same as with other
>     commands that loop over a list.  But the documentation should say:

>             When going to the next entry fails execution stops.

>     This is so it doesn't get stuck in one position and loop forever.
>     If you use ":argdo s/xxx/yyy" you get as many failures as you have
>     arguments.

Source: <https://github.com/vim/vim/issues/5102#issuecomment-545163473>

##
# Issues
## I've executed `:bufdo e`. Now all my buffers have lost their syntax highlighting!

If you haven't executed `:bufdo e` yet, try this:

    " Warning:
    " This could dramatically increase the time taken by the command
    bufdo let &ei = '' | e

Otherwise:

    bufdo let &ei = '' | do Syntax

During  the  execution  of  commands  iterating  over  buffers  (like  `:argdo`,
`:bufdo`, `:cdo`, ... but not  `:tabdo`, nor `:windo`), the 'Syntax' autocommand
event is disabled.
It's added to `'eventignore'`.
This is done to speed up the edition of each buffer.

---

Note that the issue seems to occur only when you have 3 buffers or more (not just 2).

---

TODO:

The issue may have been fixed by:
<https://github.com/vim/vim/releases/tag/v8.1.1795>

Should we remove this question?

### What's the other drawback of using `:argdo`, `:bufdo`, `:cdo`, ...?

`:windo` and `:tabdo` may change the focused window.
`:argdo`, `:bufdo`, `:cdo`, ... may change the current buffer.

Indeed, all the `:...do` commands are equivalent to the following snippets:

    ┌────────┬───────────┐
    │ :argdo │ :first    │
    │        │ :{cmd}    │
    │        │ :next     │
    │        │ :{cmd}    │
    │        │ ...       │
    ├────────┼───────────┼────────┬───────────┐
    │ :cdo   │ :cfirst   │ :ldo   │ :lfirst   │
    │        │ :{cmd}    │        │ :{cmd}    │
    │        │ :cnext    │        │ :lnext    │
    │        │ :{cmd}    │        │ :{cmd}    │
    │        │ ...       │        │ ...       │
    ├────────┼───────────┼────────┼───────────┤
    │ :cfdo  │ :cfirst   │ :lfdo  │ :lfirst   │
    │        │ :{cmd}    │        │ :{cmd}    │
    │        │ :cnfile   │        │ :lnfile   │
    │        │ :{cmd}    │        │ :{cmd}    │
    │        │ ...       │        │ ...       │
    ├────────┼───────────┼────────┴───────────┘
    │ :tabdo │ :tabfirst │
    │        │ :{cmd}    │
    │        │ :tabnext  │
    │        │ :{cmd}    │
    │        │ ...       │
    ├────────┼───────────┤
    │ :windo │ C-w t     │
    │        │ :{cmd}    │
    │        │ C-w w     │
    │        │ :{cmd}    │
    │        │ ...       │
    └────────┴───────────┘

Which means that after `:windo` and `:tabdo` has been executed, you'll be in the
last window or tabpage.
And after  the other commands, the  current buffer will  be the last one  in the
arglist, or bufferlist, or qflist, ...

### How to prevent it?

If you use your command interactively and you're about to execute:

   - `:windo` or `:tabdo`, make sure you're in the last window/tabpage

   - `:argdo`, `:bufdo`, `:cdo`, ... make sure you're in the last buffer of the
     bufferlist/arglist/qflist ...

If you use your command in a script, and you're about to execute:

   - `:windo` or `:tabdo`, save/restore the current window and tabpage,
     using `win_getid()`/`win_gotoid()`

   - `:argdo`, `:bufdo`, `:cdo`, ... save/restore the current buffer using
     `bufnr('')` and `:b {bufnr}`

---

The following alternative exists for `:bufdo`:

    augroup do_sth
        au!
        au BufEnter * :do sth
        doautoall do_sth BufEnter *
        au!
    augroup END

See `$VIMRUNTIME/syntax/nosyntax.vim` for an example.

Note that this wouldn't work for other `:...do` commands such as `:windo`.
Indeed, `:doautoall` runs a command in the context of every *buffer*.
So, if you tried to use the  previous alternative to emulate `:windo`, you would
*also* run  your command in buffers  which are not displayed  anywhere, which is
not what `:windo` does.

##
## An error is raised for a command which is not even executed!

When Vim parses  a *known* command with  a *wrong* syntax in  a *skipped* block,
the command is not run, *but* an error is raised:

    $ vim -Nu NONE +'if 0 | clear foo | endif'
    Error detected while processing command line:~
    E488: Trailing characters: clear foo~

If that is an issue, use `:exe`:

    $ vim -Nu NONE +'if 0 | exe "clear foo" | endif'
                            ^^^

See also: <https://github.com/neovim/neovim/issues/11136#issuecomment-537253732>

##
# ?

Document that, in practice, you don't need to combine `:update` and `:argdo`:

    :argdo SomeCommand | update
                       ^^^^^^^^

Our `vim-save` plugin automatically updates a buffer on BufLeave.

# ?

Document  that if  you  install a  custom  command which  relies  on the  syntax
highlighting, it needs to run this statement:

    let &ei = '' | do Syntax

Otherwise, it may not work when you use it via `:argdo`, `:bufdo`.

Also, this custom command should *not* do something wrong if there's no syntax.
IOW, if it finds no syntax item under the cursor, the code should bail out.

Right now, we have 2 such commands:

    FixWrongHeaders
    LinkInline2Ref

They don't seem to do anything wrong if there's no syntax.
Make  sure  you don't  have  other  such  commands  which behave  badly  without
highlighting:

    :Vim /\m\C\<synstack(/gj ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/** ~/.vim/vimrc

# ?

Document the [new][2] `-addr=quickfix`.

See:

<https://github.com/vim/vim/issues/3654>
<https://github.com/vim/vim/pull/3653>
<https://github.com/vim/vim/pull/3655>

    com -count -addr=quickfix Test echo <count>
    :vim /the/j %
    :-1 Test
    E16: Invalid range~
    Why?
    Because, there's no previous entry in the qfl before the first one.

    :cnext
    :-1 Test
    1~
    What does this number mean?
    Answer: it's the index of the previous qf entry

Replacing `-count` with `-range` doesn't change the results.

---

Document  the fact  that you  must use  `-addr=other` whenever  you want  to use
-range for some arbitrary count, not tied to any specific type (line address,
buffer number, window number, ...).

Before the patch 8.1.1241, you didn't have  to, but this has changed, because by
default Vim checks whether the count matches the address of an existing line.
The patch  may have introduced a  regression, but it doesn't  matter, you should
use `-addr=other`.
<https://github.com/tpope/vim-scriptease/issues/43>

Atm, Nvim doesn't support `-addr=other`, but it's not an issue because it hasn't
merged 8.1.1241 either.
There would be an issue if Nvim merged 8.1.1241 without 8.1.0560 (`-addr=other`).
I doubt that will happen.

# ?

To read:

`:h sign-support`
<https://vi.stackexchange.com/questions/15846/is-there-a-way-to-quickly-jump-to-signs>
<https://gist.github.com/BoltsJ/5942ecac7f0b0e9811749ef6e19d2176>
<https://github.com/tpope/vim-scriptease/pull/23>

# ?

Read this:
<https://www.reddit.com/r/vim/comments/5mx8jq/is_there_a_way_to_get_vimeunuchs_rename_command/>

When is `%:{filename-modifier}` expanded after pressing Tab?
Make some tests:

    com -nargs=1 -complete=file  Test  echo <q-args>
    :cd ~/Downloads
    :Test %:h
    :Test %:t
    :Test %:r
    :Test %:e

    com -nargs=1 -complete=file_in_path  Test  echo <q-args>
    :cd ~/Downloads
    :Test %:h
    :Test %:t
    :Test %:r
    :Test %:e

    com -nargs=1 -complete=file_in_path  Test  echo <q-args>

It seems to depend on various things:

   - the current working directory
   - the attribute (`-complete=file`, `-complete=file_in_path`, `-complete=custom,...`)
   - the filename modifier

Also, it seems  that some Tab-expansions don't work if  the result doesn't match
an existing file.  For example:

    $ touch /tmp/new_file
    $ vim /tmp/new_file
    :e %Tab
    ∅~
    ihello
    :w
    :e %Tab
    /tmp/new_file~

Also, some Tab-expansions  give wrong results, like `%:r`  which often (always?)
doesn't remove the extension.
That doesn't mean that they don't work as expected once you press Enter.

Also, I think  that you can only use a  filename modifiers with `-complete=file`
and `-complete=file_in_path`.  Not with `-complete=custom...`.

##
##
#
# Rangée

Graphique résumant différentes syntaxes:
<https://2.bp.blogspot.com/-TKrpj9ZOb_8/Ty8Z6uGef1I/AAAAAAAAASQ/5pEwFwtONkU/s1600/vim_ranges_p0.png>


L'absence de rangée peut être interprétée par une commande de 2 façons:

   - tout le buffer    %    1,$    C'est le cas de :g, :goto, :hardcopy, :retab, :w
   - ligne courante    .    .,.    Les autres...


Lorsqu'une rangée est inversée (a,b avec a > b), Vim demande s'il peut la remettre dans l'ordre:

    Backwards range given, OK to swap (y/n)?

Pour auto-accepter cette demande, il suffit de faire précéder la commande Ex préfixée d'une rangée
par la commande :silent.  Ex:

    :sil 5,1s/foo/bar/g


Qd  on  utilise un  pattern  comme  spécificateur  de  ligne, la  recherche  est
influencée par l'option 'wrapscan' comme pour une recherche habituelle.
Elle ne peut “wrapper“  autour de la fin/début du fichier  que si 'wrapscan' est
activée.


Si la  recherche décrite  par un  spécificateur échoue, ni  la commande,  ni les
autres spécificateurs, ne sont exécutés.


Voici qques exemples de spécificateurs de lignes:

    ┌─────┬──────────────────────────────────────────────────────────────────────────────────────┐
    │ .   │ adresse de la ligne courante (implicite par défaut)                                  │
    ├─────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ %   │ toutes les lignes du buffer; tous les buffers (1,$)                                  │
    ├─────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ *   │ la sélection visuelle (équivaut à '<,'>)                                             │
    ├─────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ .+1 │ adresse de la ligne suivant la ligne courante                                        │
    │  +1 │ +1 est un offset                                                                     │
    │  +  │ un signe + ou - seul (sans nb qui suit) est automatiquement interprété comme +1 / -1 │
    ├─────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ \/  │ la prochaine ligne contenant le registre recherche                                   │
    │ //  │                                                                                      │
    ├─────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ \?  │ la précédente "                                                                      │
    │ ??  │                                                                                      │
    ├─────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ \&  │ la prochaine ligne contenant le dernier pattern substitué (:s/pattern/rep/)          │
    └─────┴──────────────────────────────────────────────────────────────────────────────────────┘


                                     NOTE:

            Dans Vim, les spécificateurs `\/`,  `\?` et `\&` ne fonctionnent pas
            en-dessous de la version `8.0.0298`, à cause d'un bug.

            Dans Neovim, ils ne fonctionnent pas non plus, car le patch n'a pas été porté.

            La procédure pour porter un patch de Vim vers Neovim est décrite ici:
                    https://github.com/neovim/neovim/wiki/Merging-patches-from-upstream-vim

            Les 1es commandes à taper dans le repo de Neovim sont:

                    ./scripts/vim-patch.sh -l
                        listing des patchs manquants (vérifier que celui qu'on s'apprête à porter y est)

                    ./scripts/vim-patch.sh -p 8.0.0298
                        préparation du portage

                    patch -p1 < vim-8.0.0298.patch
                        création du patch

            À ce stade, perso, j'ai des erreurs. Donc, j'ai arrêté.


                                     NOTE:

            Même sans le patch, on peut s'en servir seules pour se déplacer avant éventuellement
            d'exécuter une commande. Ex:

                    :\/ | d

            Cette commande déplace le curseur sur la prochaine ligne contenant le registre recherche,
            puis supprime la ligne.


    ┌ look for `pat`
    │    ┌ do it again
    ├───┐├┐
    /pat///

            Ligne contenant la 2e occurrence de `pat` après la ligne courante.

            Si la ligne courante contient déjà `pat`, cette occurrence ne compte pas.
            La recherche débute après la ligne courante, en excluant cette dernière.


    42 /pat/

            1e ligne contenant `pat` après la ligne 42.


    42 +137 /pat/ ---

            Adresse résultant de la recherche:

                1. va sur ligne 42

                2. descend de 137 lignes
                        le + est facultatif car les adresses numériques sont additives par défaut

                3. cherche la prochaine occurrence de `pat`

                4. remonte de 3 lignes
                        on pourrait écrire -3 aussi; les - et + sont cumulatifs


    .+3,$-1
     +3,$-1

            3e ligne qui suit la ligne courante jusqu'à l'avant-dernière.


    ?pat1?+1,/pat2/-1

            Rangée de lignes.
            La 1e est trouvée en cherchant `pat1` vers l'arrière, et en avançant d'une ligne.
            La 2e est trouvée en cherchant `pat2` vers l'avant, et en reculant d'une ligne.

            Les recherches commencent à partir de la ligne courante.


    ?pat?,//

            Lignes entre la précédente et prochaine ligne contenant `pat`.

            // et ?? désignent l'adresse de la ligne où la précédente/prochaine occurrence
            du registre recherche est trouvée. Juste après ?pat?, le registre recherche est peuplé
            avec 'pat'.


    4,/pat/
    5;/pat/

            Lignes entre la 4e et la prochaine (par rapport à la courante) contenant `pat`.
            Lignes entre la 5e et la prochaine (par rapport à la 5e)       contenant `pat`.

            Lorsque le séparateur entre les 2 spécificateurs d'une rangée est un
            point-virgule, le  curseur est déplacé  sur la ligne  dont l'adresse
            est décrite par le 1er spécificateur.
            Autrement, le curseur reste sur la ligne courante.


    ?Preface?/3e point/-,$

            Lignes entre la ligne X et la dernière ligne du buffer.
            X est trouvée de la façon suivante:

                    1. depuis la ligne courante, cherche la précédente ligne contenant 'Preface'
                    2. depuis cette ligne, cherche la prochaine ligne contenant '3e point'
                    3. remonte d'une ligne

            Illustre le fait qu'on peut chaîner autant de patterns qu'on veut pour décrire une adresse.

            Qd on chaîne plusieurs patterns, le registre recherche finit par être peuplé avec:

                    - le dernier pattern s'ils sont tous trouvés
                    - le 1er des patterns non trouvés autrement

            Pex, si 'Preface' est trouvée, le registre recherche est peuplé avec '3e point',
            autrement avec 'Preface'.


                  ┌─ si `EXPORT` est présent sur la dernière ligne, et qu'on n'utilise pas `+`,
                  │  on termine sur la ligne contenant l'avant-dernière occurrence
                  │
    0/EXPORT/    $+?EXPORT?

            Première / dernière ligne du buffer contenant EXPORT.

            Pour la dernière, on pourrait aussi utiliser 0?EXPORT? (ou 1?EXPORT?), mais ça ne fonctionnerait
            que si 'wrapscan' est activée.


                         TODO: read `:h search-offset`

# Aide

Tout en haut  de chaque page d'aide  du manuel de référence se  trouve(nt) un ou
plusieurs liens vers la/les page(s) pertinente(s) du manuel utilisateur.
Pex, en haut de `:h pattern.txt`, se trouvent `:h 03.9` et `:h usr_27` .

Des tags ayant un thème commun commencent par un même préfixe:

    ┌─────────────┬──────────────────────────────────────┐
    │ "           │ registres                            │
    ├─────────────┼──────────────────────────────────────┤
    │ -           │ arguments de la commande shell `vim` │
    ├─────────────┼──────────────────────────────────────┤
    │ /           │ pattern                              │
    ├─────────────┼──────────────────────────────────────┤
    │ :syn-       │ coloration syntaxique                │
    ├─────────────┼──────────────────────────────────────┤
    │ >           │ déboguage                            │
    ├─────────────┼──────────────────────────────────────┤
    │ ^w_         │ manipulation de fenêtre              │
    ├─────────────┼──────────────────────────────────────┤
    │ cpo-        │ flags 'cpo'                          │
    │ go-         │ flags 'go'                           │
    ├─────────────┼──────────────────────────────────────┤
    │ ft-*-indent │ plugin d'indentation                 │
    │ ft-*-omni   │ omni-complétion                      │
    │ ft-*-plugin │ ft plugin                            │
    │ ft-*-syntax │ syntax plugin                        │
    ├─────────────┼──────────────────────────────────────┤
    │ hl-         │ highlight group                      │
    ├─────────────┼──────────────────────────────────────┤
    │ map[-_]     │ mappings                             │
    └─────────────┴──────────────────────────────────────┘

                                     NOTE:

            Pour les commandes de fenêtre, il semble qu'on puisse même se passer
            de l'underscore:

                    :h ^wp ✔


    :h :syn-* C-d

            On peut lister tous les tags commençant par un même préfixe via `C-d`.


                     ┌ plugin géré par `vim-plug`
                     │
    :helptags ~/.vim/plugged/foo/doc/

            (Re)Génère le fichier de tags du plugin foo.

            Sans  ce fichier  tags, on  ne peut  pas consulter  la documentation
            directement depuis Vim via la commande :help (:h foo).

            Si on  crée son  propre plugin  et qu'on veut  pouvoir accéder  à sa
            documentation depuis Vim,  il faudra de la même  manière utiliser la
            commande `:helptags` sur le dossier doc/ la contenant.

                                     NOTE:

            Pour pouvoir consulter  la documentation d'un plugin,  il faut aussi
            qu'il soit dans le rtp.
            En effet,  Vim ne cherche  un fichier  de documentation que  dans un
            dossier `doc/` présent dans un dossier du rtp.


                                     NOTE:

            Pour bénéficier de la coloration  syntaxique, il faut que le fichier
            ait été chargé via `:h {tag}`.
            Pas directement via `:edit`.

# Syntaxe

Petit rappel de vocabulaire:

   - on *évalue*       une expression (demande sa valeur)

   - on *remplace*     du texte par un autre
                        :s, :retab, :%!{filter}, ...

   - on *convertit*    une donnée d'un certain type dans un autre;
                        un fichier utilisant un format ou un encodage donné dans un autre
                        (odt → pdf; latin1 → utf-8)

   - on *développe*    un {lhs} de mapping/abréviation,
                        une séquence d'échappement de commande (<bang>, <line1>, ...),
                        des caractères spéciaux sur la ligne de commande    :h cmdline-special,
                        une variables d'environnement,
                        une commandes shell                                 :h backtick-expansion,
                        un glob

   - on *traduit*      un caractère ou un groupe de caractères en un autre
                        un count en rangée (ex:    5: → :.,.+4)
    
                        Le résultat d'une traduction est tjrs le même.
    
                                "\<C-w>" = "^W"    peu importe le contexte

                        Le résultat d'un développement dépend du contexte:
    
                                :e %:t    le développement de %:t dépend du nom du buffer courant
    
     on *interprète*   un caractère ou un groupe de caractères pour déterminer quel comportement adopter

                        Une  cmd, une fonction, le  parser de Vim, ou  + généralement n'importe
                        quel bout de code peut interpréter certains caractères.
    
                        Ex:  La  plupart des commandes Ex  interprètent la barre
                        verticale  comme  une  terminaison de  commandes;  elles
                        s'arrêtent donc à une barre.
    
                        :s interprète \= au début de la chaîne de remplacement comme le début d'une expression;
                        elle évalue donc cette expression avant de remplacer le pattern.
    
   - on *appelle*      une fonction

   - on *exécute*      une commande Ex

   - on *invoque*      du code informatique (la méthode n'est pas précisée par le terme)


L'aide de Vim ne parle pas d'interpolation, mais plutôt de développement.
Toutefois, dans d'autres langages, qd une  commande ou le nom d'une variable est
automatiquement  remplacée par  sa sortie/valeur,  on parle  plus spécifiquement
d'interpolation.
Pour + d'infos:
<https://en.wikipedia.org/wiki/String_interpolation>



Sur la  ligne de commande de  Vim, certains caractères spéciaux  sont développés
lorsqu'ils suivent une commande Ex qui accepte en argument un nom de fichier, ou
lorsqu'ils doivent être envoyés au shell (:!).

On peut forcer Vim à les développer  avant d'exécuter la commande via Tab ou C-x
C-a.
Qd plusieurs développements sont possibles, C-x C-a les insère tous sur la ligne
de commande.
Tab n'en insère  qu'un sur la ligne  de commande, et propose les  autres dans le
wildmenu.

    ┌──────────────────┬───────────────────────────────────────────┐
    │ %                │ nom du fichier courant                    │
    ├──────────────────┼───────────────────────────────────────────┤
    │ #                │ "              alternatif                 │
    ├──────────────────┼───────────────────────────────────────────┤
    │ #1               │ "              n°1                        │
    ├──────────────────┼───────────────────────────────────────────┤
    │ #2               │ "              n°2                        │
    ├──────────────────┼───────────────────────────────────────────┤
    │ ##               │ noms des fichiers présents dans l'arglist │
    │                  │                                           │
    │                  │ :h :_##                                   │
    ├──────────────────┼───────────────────────────────────────────┤
    │ *                │ glob                                      │
    │ **               │                                           │
    │                  │ ex: !cp /tmp/* ~/Desktop/                 │
    ├──────────────────┼───────────────────────────────────────────┤
    │ $                │ ancre                                     │
    │                  │                                           │
    │                  │ ex: e /tmp/*m$                            │
    ├──────────────────┼───────────────────────────────────────────┤
    │ [abc]            │ collection (a ou b ou c)                  │
    │                  │                                           │
    │                  │ répétable:    :n **/[ab]*[cd]             │
    ├──────────────────┼───────────────────────────────────────────┤
    │ `find . -type f` │ interpolation                             │
    │                  │                                           │
    │                  │ :h backtick-expansion                     │
    ├──────────────────┼───────────────────────────────────────────┤
    │ `=tempname()`    │ fichier temporaire généré par la          │
    │                  │ fonction Vim tempname()                   │
    │                  │                                           │
    │                  │ généralisable à toute expression Vim      │
    │                  │                                           │
    │                  │ :h `=                                     │
    │                  │                                           │
    │                  │ il existe 2 alternatives à cette syntaxe: │
    │                  │                                           │
    │                  │     exe 'cmd '.expr                       │
    │                  │     C-r = expr CR                         │
    │                  │                                           │
    │                  │ Toutefois, ces dernières ne changent pas  │
    │                  │ le sens spécial des caractères:           │
    │                  │                                           │
    │                  │     " | % #                               │
    │                  │                                           │
    │                  │ ... contrairement à `=                    │
    └──────────────────┴───────────────────────────────────────────┘

Parmi les commandes Ex après lesquelles on peut écrire ces caractères spéciaux se trouvent:

    :[arg|tab]edit
    :new
    :split
    :read
    :Foo    à condition qu'elle ait été définie avec l'attribut `-complete=file{_in_path}`

En revanche, on ne peut pas les utiliser après des commandes qui écrivent dans un fichier.
En effet, dans ce cas on provoquerait l'erreur E139. Pex:

    :w #42    ✘

:w #42 demande à écrire le buffer courant dans le fichier dont le nom est celui du buffer 42.
Ceci n'est pas permis, car on obtiendrait un fichier qui serait alors différent du buffer 42.

On peut modifier le développement de ces caractères spéciaux via des filename-modifiers. Ex:

    :!echo %:h    echo le chemin vers le dossier contenant le fichier courant

    :e %:t        édite un buffer de même nom que le fichier courant à l'intérieur du cwd
                  Pex, si on est en train d'éditer /tmp/foo et que le cwd est /home/user,
                  cette commande charge le buffer /home/user/foo.

Le développement inclut un backslash devant chaque éventuel espace présent dans le nom d'un fichier.

:h cmdline-special et :h filename-modifiers pour + d'infos.



Quand on souhaite passer  en argument contenant un espace à  une commande Ex, il
faut l'échapper pour lui faire perdre son caractère syntaxique.
De même, avant  de passer le contenu  d'une variable en argument  à une commande
Ex, il faut passer cette dernière à  fnameescape() pour faire perdre leur sens à
tous ses caractères spéciaux.



    :e `=myvar`
    :exe 'edit '.fnameescape(myvar)

            Éditer le fichier dont le nom est contenu dans myvar.

            La 1e syntaxe n'a pas besoin de fnameescape() car elle protège déjà les caractères spéciaux.
            On peut le vérifier comme ceci:

                :let myvar='foo bar'
                :e `=myvar`                 fonctionne comme prévu
                :e `=fnameescape(myvar)`    ne fonctionne pas comme prévu; édite le fichier 'foo\ bar'
                                            illustre le fait que l'espace avait déjà été échappé


                                     NOTE:

            C'est   sans    doute   pour   ça   que    peupler   l'arglist   via
            `=systemlist('shell cmd')  est +  fiable que directement  via `shell
            cmd`.


    :let var = "/tmp/foo\n/tmp/bar"
    :args `=var`
    :exe 'args '.var

            Peupler l'arglist avec `/tmp/foo` et `/tmp/bar`.

            Fonctionnerait également si `var` contenait une liste:

                    let var = [ '/tmp/foo', '/tmp/bar' ]


Plusieurs commandes Ex  interprètent la barre verticale comme  faisant partie de
leur argument (ce qui n'est pas le cas des commandes de mapping, comme nnoremap,
pour  lesquelles  il faut  échapper  la  barre  verticale  si on  veut  qu'elles
l'incluent dans la commande qu'elles doivent exécuter).
Ça implique qu'on ne peut pas placer  une barre verticale après elles pour faire
commencer une autre commande.

Quelques commandes Ex qui interprètent la barre verticale comme un argument:

    :argdo, :bufdo, :tabdo, :windo          :argdo exe 'norm ohello' | set list

    :autocmd                                la barre verticale fait partie de la commande à exécuter par :autocmd

    :command                                com SV source $MYVIMRC | source ~/.vim/autoload/myfunctions.vim
                                            la barre verticale fait partie de la commande à exécuter par :SV

                                            Sauf si on définit la commande en lui donnant l'attribut -bar.

    :function
    :[v]global                              :g/foo/t. | s/./=/g

                                            :g exécute sur chaque ligne contenant 'foo':
                                            t. | s/./=/g
                                            la barre verticale est donc bien interprété par :g comme un argument

    :make
    :normal                                 interprète | comme : déplacement du curseur sur la 1e colonne
    :read !                                 la barre verticale est passé au shell
    :write !                                "
    :[range]!                               "

Qd  on veut  faire  suivre l'une  des  commandes Ex  précédentes  par une  autre
commande Ex sur la même ligne, il  ne faut pas utiliser la barre verticale, mais
un LF via C-v C-j (traduit en NUL, affiché via ^@).
Ou alors les envelopper dans une chaîne et les exécuter via :exe.

# [++opt][+cmd]

Principales commandes acceptant les arguments optionnels ++opt et +cmd:

               edit/view                   [file]
            [N]argedit                      file
            [N]tabedit/tabnew              [file]

            [N][v]new                      [file]
            [N][v]split                    [file]

               bfirst
               blast
            [N]buffer                      [N]/{bufname}
            [N]bnext
            [N]bprevious
            [N]bmodified                   Go to [N]th next modified buffer

               args/arglocal/argglobal     {arglist}
               first
               last
            [N]argument
            [N]next
            [N]previous

                   saveas                   file
                   wqall
                [N]wnext                   [file]
                [N]wprevious               [file]
            [range]read                     file | !{cmd}
            [range]update             [>>] [file]
            [range]write              [>>] [file | !{cmd}]
            [range]wq/x                    [file]



Les commandes qui permettent de lire/écrire/sauvegarder acceptent l'argument ++opt.
Les commandes qui permettent de naviguer au sein de la buffer list acceptent l'argument +cmd.
Les commandes qui permettent de:

        - charger un buffer       :[arg|tab]edit  :[s]argument  :[v]new
                                  :[s|tab]find

        - agir sur l'arglist

        - splittent               :[v]split

... acceptent les arguments ++opt et +cmd.


L'argument   ++opt  peut   servir   à  configurer   les  options   'fileformat',
'fileencoding' et 'binary', dans le fichier à éditer.

    :e ++ff=unix

            édite le même fichier en utilisant `unix` comme format de fichier
            Un caractère de fin de ligne sera interprété comme étant un <LF>.

    :w ++enc=latin1 newfile

            écrit le buffer courant dans "newfile", en utilisant `latin1` comme système d'encodage

On peut utiliser plusieurs arguments ++opt  séparés par des whitespace, mais ils
doivent tous apparaître avant l'argument +cmd.

L'argument +cmd  peut être utilisé pour  positionner le curseur dans  le fichier
dont le nom suit.
Il peut aussi exécuter n'importe quelle commande Ex.

        :{line address}
        /pattern
        ?pattern
        :Ex command



        :edit                  :view      active l'option 'readonly'
        :split            ⇔    :sview     "
        :first                 :rewind
        :previous              :Next

                Synonymes.


        :[s][b]first            :[s][b]rewind
        :[s][b]previous    ⇔    :[s][b]Next
        :wprevious              :wNext

                Synonymes.


Certaines des précédentes commandes acceptent un count avant ou après elles.
Parmi  celles-ci, les  seules qui  acceptent le  count après  elles sont  celles
permettant de  naviguer au sein de  la buffer list  / arglist, ou de  charger un
buffer de ces 2 listes.
Elles peuvent aussi être préfixées d'un `s` pour charger le buffer/argument dans
un viewport horizontal.

        [s]bnext        N
        [s]bprevious    N
        [s]bmodified    N
        [s]next         N
        [s]previous     N

        [s]buffer       N
        [s]argument     N

        [s][b]first
        [s][b]last

La signification de N varie. Le plus souvent il décrit:

        - un index absolu (de buffer dans la buffer list/arglist):

                :3[s]buffer
                :4[s]argument

        - un index relatif
          avec les commandes utilisant le suffixe `next` ou `previous`. Ex:

                :3[s]bnext
                :4[s]previous
                :5wnext          écrire le buffer, et charger le 5e prochain argument

          Également avec :[s]bmodified et :argedit:

                :3sbmodified    3ième prochain buffer modifié
                :4argedit       ajout du buffer courant dans l'arglist après la 4-ième entrée

        - une hauteur/largeur de fenêtre,
          avec les commandes qui de base splittent (:[v]new, :[v]split)

Il a la même signification pour :tabedit/:tabnew et :tabfind.
Il indique où positionner le nouvel onglet.
Pex:

        :-tabnew    avant l'onglet courant
        :0tabnew    au tout début
        :$tabnew    en dernier

Avec :find et ses dérivées, sa signification est inconsistante:

        :2find foo
        charger le 2e match s'il y en a plusieurs~

        :3sfind foo
        fenêtre de hauteur 3~
        :vert 3sfind foo
        fenêtre de largeur 3~

        :4tabfind foo
        afficher `foo` dans un onglet positionné après le 4e~


Un bang est parfois nécessaire pour permettre à une des commandes précédentes de:

   - abandonner un buffer modifié

   - écrire un buffer modifier dans un fichier RO (:write [file], :wq/:x
      [file], :wqall)

   - écraser un fichier existant (:wnext file, :saveas file)

# Commandes système

Les commandes Ex n'acceptent pas toutes le même type d'argument.
Pex,  :exe attend  une expression,  :normal des  commandes, et  :edit un  nom de
fichier.


Sur  la ligne  de  commande (:  ?  /), C-p  / C-n  permettent  de naviguer  dans
l'historique des commandes  passées (built-in), M-p / M-n  dans un sous-ensemble
de l'historique contenant l'ensemble des  commandes passées qui commencent de la
même façon que la chaîne de caractère précédant le curseur (custom).


    :!{cmd}

            passe {cmd} au shell qui l'exécute

            Une barre verticale  est passé au shell, `:!`  ne l'interprète comme
            une terminaison de commande.

                                     NOTE:

            Pour passer un !, %, # au  shell, il faut les échapper, car ils sont
            développés en:

                    - %    le nom du buffer  courant
                    - #    "                 alternatif
                    - #1   "                 n°1
                    - #2   "                 n°2
                    - !    "                 la dernière commande shell

                                     NOTE:

            Si  le nom  du  buffer développé  contient  lui-même des  caractères
            spéciaux, il faut quoter '%', '#', ... pour éviter que le shell ne les
            interprète.

            Pour être  sûr de ne  pas être  dérangé par des  caractères spéciaux
            dans le nom d'un fichier qu'on  veut passer au shell, il faut passer
            par `shellescape()`:

                    :exe '!chmod +x -- ' . shellescape(expand('%'), 1)

            `expand()` force  le développement de '%'  avant que `shellescape()`
            ne soit appelée, autrement cette dernière recevrait la chaîne '%' au
            lieu du nom du buffer courant.

                                               NOTE:

            Le shell passe le code de sortie d'une commande à Vim via `v:shell_error`.
            On peut donc s'en servir pour réagir en conséquence:

                    if !v:shell_error
                        echo 'The shell cmd succeeded!'
                    else
                        echo 'It failed...'
                    endif


    :!!     réexécuter la dernière commande shell


    :!%

            exécute le contenu du script shell courant

            Fonctionne car Vim développe `%` en le nom buffer courant.
            Toutefois, il faut que le fichier soit exécutable.


    :au {event}

            Lister les autocmd associées à {event}.
            Pour voir quels fichiers les ont installées :verb au {event}.
            On peut filtrer plus finement, voir :h autocmd-list.


    :cquit

            Quitte  Vim  en  fermant  toutes  les fenêtres  (comme  :qa)  et  en
            retournant au shell le code d'erreur 1.
            Aucune modification de buffer non sauvegardée n'est préservée.

            Utile qd on édite une commande shell dans un buffer Vim, après avoir
            invoqué  ce  dernier via  `C-x  C-e`,  et  qu'on veut  annuler  sans
            exécuter la commande.
            En effet, si on quitte via `:quit`, la commande est exécutée.


    :delmark x
    :delmark X | wviminfo!

            Supprimer la marque x / X.

            Pour supprimer une marque globale (X), il semble qu'il faille écrire
            les changements dans le fichier  ~/.viminfo en forçant les nouvelles
            infos à écraser les anciennes (!
            = pas de fusion).
            Autrement, qd on redémarre, Vim recrée les marques.

            Attention, dans  ce cas  on perd des  infos intéressantes  comme les
            derniers changements (:changes).

            Pour + d'infos sur le pb de suppression d'une marque globale:
            https://groups.google.com/forum/#!msg/vim_dev/kre4oyzMRDU/egIH4hlIWo4J


    :delmarks!

            supprimer toutes les marques locales au buffer courant:    a-z


    :filter /^E\d\+/ messages
    :filter /.sh$/ oldfiles

            Affiche  les  messages d'erreurs  s'étant  produit  au cours  de  la
            session courante.
            Affiche les fichiers shell récemment édités.

            `:filter` permet de limiter la  sortie d'une commande Ex à certaines
            lignes contenant un pattern arbitraire.

            Toutefois, pour chaque ligne de la sortie de la commande, le pattern
            n'est comparé qu'à une partie jugée pertinente par Vim:

                    e foo.vim
                    ls
                    1 %a   "foo.vim"                      line 1~
                    filter /vim$/ ls
                    1 %a   "foo.vim"                      line 1~

            De plus, ne fonctionne pas avec toutes les commandes Ex:

                    :filter /garbage/ exe 'ls'
                    rien n'est filtré, toute la sortie de `ls` est affichée~
                    `:filter` ne fonctionne pas avec `:exe`~


    :fu[nction]

            lister les fonctions

    :fu /pattern

            lister les fonctions qui matchent pattern  (ex : :fu /foo$ liste les
            fonctions qui se terminent par foo)

    :history / 6,12

            afficher les entrées 6 à 12 de l'historique de recherche

    :history : -20,

            afficher les  20 dernières  entrées de l'historique  de la  ligne de
            commande

    :history =

            afficher l'historique expression


    :keepp {Ex cmd}

            Qd une commande (:s, :g)  modifie modifie le contenu de l'historique
            ou du registre recherche, on peut l'en empêcher ponctuellement en la
            préfixant avec `:keepp`.

            Lorsqu'elle  est  exécutée  au  sein  d'une  fonction,  le  registre
            recherche est automatiquement  restauré à la fin  de cette dernière,
            cf `:h function-search-undo`.
            En revanche, l'historique est pollué.
            `:keepp` est donc utile même dans une fonction.

            Pour obtenir le même résultat (au sein d'une fonction ou en-dehors),
            on pourrait écrire:

                    :let @/ = histget('search')
                    :call histdel('search', -1)


    :keepj {Ex cmd}

            Qd  une  commande  Ex  ou  normale  (:s,  :g,  :e,  :tag,  {motion},
            ...)  ajoute une  entrée dans  la  jumplist, on  peut l'en  empêcher
            ponctuellement en la préfixant avec `:keepj`.

            Plus généralement, `:keepj` préserve la:

                    - marque ''    jumplist
                    - marque '.    changelist
                    - marque '^

            Pour rappel, les  marques '', '., '^ correspondent à  la position du
            curseur lors du dernier saut, dernière édition, dernière insertion.

                                     NOTE:

            Ne pas  utiliser `:keepj` avec  une commande  globale si au  sein de
            cette dernière on  a besoin de se référer à  la position qu'avait le
            curseur juste avant qu'elle ne soit exécutée, via la marque ''.


    :marks

            afficher les marques

    :noautocmd {cmd}

            exécute {cmd} sans déclencher aucune autocmd
            le temps de l'exécution, l'option 'eventignore'/'ei' vaut 'all'


    :nohlsearch

            Annule la mise en surbrillance du HG Search.

            :noh ne modifie pas la valeur de l'option 'hlsearch'.

            La mise  en surbrillance  est restaurée  dès la  prochaine exécution
            d'une commande recherchant un pattern (n, N, *, #, /, ?, :s, :g).

            Ceci illustre qu'on ne  peut pas se fier à `&hls`  pour savoir si le
            HG Search est mis en surbrillance ou pas.
            En revanche, on peut se fier à `v:hlsearch`:

                    v:hlsearch == 1    →    surbrillance
                    v:hlsearch == 0    →    pas de surbrillance

                                     NOTE:

            Depuis une fonction ou une autocmd:

                    - `noh`          ne fonctionne pas
                                     car le registre recherche est automatiquement restauré

                    - `set nohls`    désactive la mise en surbrillance quelle que soit la valeur
                                     de &hls et v:hlsearch

                    - `set hls`      active la mise en surbrillance ssi &hls = 0


    :sp +enew | 0Nread url
    :$d_ | noautocmd sil w! file | bw

            Télécharge le fichier présent à l'adresse ’url’ dans le fichier ’file’.

            `:Nread` est une commande du plugin netrw.
            Il semble qu'elle  n'ait pas été définie avec  l'attribut `-bar`, et
            qu'elle interprète une  barre verticale comme faisant  partie de son
            argument plutôt qu'une terminaison de commande.
            On ne pourrait donc pas écrire:

                    :0Nread url | $d_        ✘


    :redraw!

            Efface l'écran (!) et le redessine.

            Utile  après  certaines  commandes  qui  corrompent  l'affichage  du
            buffer, ou pour effacer tout ce qu'elles ont affichées.

            Ex  d'affichage   corrompu:  après  l'exécution   silencieuse  d'une
            commande  shell (sil  !echo hello),  une partie  de l'écran  devient
            invisible.

            Utile aussi  pour redessiner l'écran  au milieu de  l'exécution d'un
            script / mapping / fonction:

                    nno <key>    :call MyFunc()<cr>

                    fu MyFunc()
                        let char = ''
                        while char != 'x'
                            let char = input('type a character: ')
                            s/\a/X/
                            redraw
                        endwhile
                    endfu

            Après  avoir  appuyé   sur  <key>  la  boucle   while  effectue  des
            substitutions sur la ligne courante  tant que le caractère saisi par
            l'utilisateur est différent de 'x'.
            Mais  sans  l'instruction  :redraw,   l'écran  ne  serait  redessiné
            qu'après la fin de la fonction.
            Avec  :redraw,  on  peut  voir  en temps  réel,  l'effet  de  chaque
            substitution.


                                     NOTE:

            `:redraw` est également  utile pour bypasser un  prompt:

                    “Press Enter or type command to continue”

            ... causé par la présence de plusieurs messages sur la ligne de commandes.

                    fu Func()
                        let answer = confirm('Do a listing?', "&Yes\n&No", 1)
                        if answer == 1
                            call system('ls')
                            redraw
                            echo 'Did a listing!'
                        endif
                    endfu
                    call Func()

            Dans cet  exemple, sans le  `redraw`, Vim nous imposerait  le prompt
            `Press Enter...`.

            Pk?
            `confirm()` a laissé un message occupant 2 lignes: `Do a listing?` +
            une ligne vide.
            Qd `:echo` devra afficher son message, ça fera 3 lignes.

            Or, qd Vim  termine d'exécuter une série de  commandes, il redessine
            l'écran.
            Notamment,  qd elles  ont produit  une suite  de messages  occupant
            plusieurs lignes:

                    echo "foo\nbar"

            Il le fait afin de rétablir une ligne de commande de hauteur normale.

            Qd Vim  sait qu'il  va effacer  des messages,  il utilise  le prompt
            `Press Enter...`  pour nous  laisser le  temps de  les lire,  avant de
            redessiner.

            En forçant  le redessinage avant  l'affichage du dernier  `echo`, le
            message de ce dernier n'occupe plus qu'une seule ligne.
            Vim n'a donc plus besoin de redessiner immédiatement.
            Donc plus besoin du prompt pour nous laisser le temps de lire.


            `:redraw`  ne fonctionne  que  si  le prompt  est  sur  la ligne  de
            commande de Vim.
            Si le prompt est dans le shell lui-même, il faut utiliser `:silent`:

                    sil !ls
                    redraw

            Ici `:redraw`  ne sert pas à  bypasser le prompt, mais  à redessiner
            l'écran qui a été corrompu.


    :rviminfo    :wviminfo

            lire / écrire dans le fichier .viminfo

            .viminfo contient l'historique des commandes passées, les registres,
            les  marques... Par  défaut, Vim  ne le  lit que  lorsqu'on lance  une
            nouvelle session et n'y écrit que lorsqu'on la ferme.

            Le reste du temps, il écrit et lit dans un buffer.

            De ce fait, l'historique est différent entre 2 sessions.

            Ces  2 commandes  permettent  de forcer  Vim à  lire  / écrire  dans
            .viminfo au milieu  d'une session et ainsi  de partager l'historique
            entre plusieurs sessions.


    :shell
    :suspend    :stop

            Met la session en pause, et:

                    - lance un nouveau shell enfant de Vim
                    - restaure le shell parent de Vim


    :sil[ent][!] {cmd}

            exécute {cmd} sans afficher les messages normaux (! = y compris les messages d'erreur)

            Avantage:        évite qu'un mapping ou une commande ne s'interrompt dès qu'il y a une erreur
                             si la commande provoque un prompt demandant d'appuyer sur Enter pour continuer,
                             celui-ci est bypassé

            Inconvénient:    un prompt bypassé semble corrompre l'affichage du buffer (exécuter :redraw! dans ce cas)

    :sign define foo text=>> texthl=Search

            définit le signe foo, qui affichera le texte >> avec les couleurs du HG Search

            text et texthl sont des arguments de la commande :sign (ou attributs du signe foo)
            Il en existe d'autres:    icon=    chemin vers une icône
                                    linehl=    HG à utiliser pour toute la ligne portant le signe

    :sign list

            liste tous les signes définis dans  tous les buffers ainsi que leurs
            attributs (text, texthl...)

    :sign place 9999 line=10 name=foo file=/tmp/bar

            place le signe foo sur la 10e ligne du fichier /tmp/bar
            Ici, on a choisi l'id 9999. Il nous permettra de manipuler le signe par la suite.

    :sign unplace 9999 file=/tmp/bar

            supprime le signe d'id 9999 présent dans le fichier /tmp/bar

    :swapname

            Affiche le chemin absolu vers le fichier d'échange du buffer courant.
            On peut sauvegarder son nom via execute() et fnamemodify():

                    let swapfile = fnamemodify(execute(':swapname'), ':t')


    :10,40TOhtml

            Convertit  les lignes  10 à  40 du  buffer courant  en html  dans un
            nouveau fichier (foo.html).


    :exe 'TOhtml' | wq

            Convertit le buffer courant en html, écrit et quitte.

            :TOhtml n'a pas été définie avec l'attribut -bar, donc si on écrivait directement:

                :TOhtml | wq

            Elle interprèterait '| wq' comme faisant partie de son argument.

# Commandes utilisateur

`:Next` et `:X` sont les seules commandes système commençant par une majuscule.

    :com foo

            lister les commandes utilisateur dont le nom commence par foo

            La 1e colonne peut inclure les symboles b ou !.
            b = locale au buffer.
            ! = la commande accepte un bang comme modificateur (comme :q et :w pex).
            'Address' détermine à quoi se réfèrerait `.`, `$` et `%` dans une rangée.
            'Complete' détermine le type de suggestions quand on appuie sur Tab.


    com Foo echoerr  Foo()    ✘
    com Foo exe      Foo()    ✔

    fu Foo()
        try
            mksession! /tmp/file
        catch
            return 'echoerr '.string(v:exception)
        endtry
        return ''
    endfu

            Dans la  définition d'une  commande, il  peut être  utile d'utiliser
            `:exe` pour invoquer une routine si cette dernière peut échouer.

            En effet, en cas d'erreur au sein d'une fonction, l'écran est pollué
            par une stacktrace multi-ligne.
            C'est perturbant,  et incohérent avec  les commandes Ex  par défaut,
            qui, en cas d'erreur n'affiche qu'un message mono-ligne.

            Concernant `:echoerr`:

                    - avantage:        efface le nom de la commande qui vient d'être exécutée
                                       qd elle a réussi (echoerr '')

                    - inconvénient:    impossible d'utiliser la commande au sein d'une fonction,
                                       à moins d'utiliser `:silent!` ;
                                       car `:echoerr` produit une erreur reconnue comme valide


    com Del +,$delete

            définit la commande  :Del qui supprime les lignes  depuis celle sous
            le curseur (+ = .+1) jusqu'à la fin du fichier ($)


    com -nargs=1 -complete=customlist,CompleteFunc MyCom call MyFunc()

    fu CompleteFunc(arglead, _cmdline, _pos)
        let candidates = ['foo', 'bar', 'baz']
        return filter(candidates, {_,v -> stridx(v, a:arglead) == 0})
    endfu

            définit la commande :MyCom qui appelle la fonction MyFunc()

            En appuyant sur Tab, la  commande fait des suggestions en s'appuyant
            sur ce que retourne la fonction CompleteFunc().
            Vim  appelle  automatiquement  cette  dernière  en  lui  passant  en
            argument  3 infos,  qu'on peut  appeler (par  convention) `arglead`,
            `_cmdline` et `_pos` au sein de la fonction.

                    arglead  = début d'argument fourni
                    _cmdline = ligne de commande entière
                    _pos     = position du curseur

            CompleteFunc() est  dotée d'une liste de  candidats prédéfinis (foo,
            bar et baz),  qu'elle filtre en comparant le début  de chaque item à
            ce qu'on a commencé à taper après :MyCom (a:arglead).

            Pour  + d'infos  sur  la  complétion custom  de  commandes, lire  :h
            :command-completion-customlist


                                     NOTE:

            On peut donner une fonction de complétion à une commande via 2 attributs:

                    -complete=custom
                    -complete=customlist

            Si on utilise `customlist` la fonction doit:

                    - retourner une liste, et non une chaîne contenant des
                      candidats séparés par des newlines
                    - filtrer les candidats

            Si  le   filtrage  qui  nous   intéresse  consiste  à   comparer  le
            début  de chaque  candidat  à `a:arglead`,  il  vaut mieux  utiliser
            `-complete=custom`: plus lisible, moins verbeux, plus performant.
            En effet, avec cet attribut, Vim effectue un filtrage automatique:

                - le début de chaque candidat est comparé avec `a:arglead`
                - la comparaison respecte 'ignorecase' et 'smartcase'

##
# Reference

[1]: hhttps://github.com/tpope/vim-eunuch/blob/master/plugin/eunuch.vim
[2]: https://github.com/vim/vim/releases/tag/v8.1.0560
