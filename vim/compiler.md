# Compiler plugin
## What's the purpose of a compiler plugin?

It sets the `'errorformat'` and `'makeprg'` options.

`:make` will use:

   - 'makeprg'     to determine which shell command to execute
   - 'errorformat' to determine how to parse the output

##
## Where can I find examples of code for a compiler plugin?

    :next $VIMRUNTIME/compiler/*.vim

## Where to put my compiler plugin?

In:

   - `~/.vim/after/compiler`
     to overrule some settings of the default compilers in `$VIMRUNTIME/compiler/`

   - `~/.vim/compiler`
     to bypass the default compilers entirely

The bypassing  works ONLY if you  assign a value to  `current_compiler`, because
the default  compilers have a  guard which  checks whether this  variable exists
(similar to `b:did_ftplugin`).

Currently,  we take  care of  automatically assigning  `current_compiler` via  a
template in  [~/.vim/template/by_name/compiler.txt][2], AND the addition  of the
assignment via [vim-unix][3].

##
## Should my compiler plugin contain a guard?

It depends where you put it.

If you put it in:

    ~/.vim/after/compiler
           ^---^

don't make it begin with:

    if exists('current_compiler')
        finish
    endif

This guard  would prevent your plugin  from being sourced, because  the variable
will have been set by the default plugin in `$VIMRUNTIME/compiler/`.

See the end of `:help CompilerSet`:

   > When you  write a compiler  plugin to overrule  settings from a  default plugin,
   > don't check "current_compiler".
   > This plugin is supposed  to be loaded last, thus it should be  in a directory at
   > the end of 'runtimepath'.
   > For Unix that could be ~/.vim/after/compiler.

OTOH, as  the help says,  if you put your  plugin in `~/.vim/compiler`,  you can
include a guard.

##
## How to use a compiler plugin
### manually?

Use `:compiler`.

`:compiler` sets local options, while `:compiler!` sets global options.

### automatically?

Listen to `FileType` and `BufWritePost`:

    " or write `compiler rustc` in a rust filetype plugin
    au  FileType      rust  compiler rustc
    au  BufWritePost  *.rs  sil make! | redraw!
                                     │
                                     └ no need to add % because the default compiler already does it
                                       when it configures 'mp':

                                            $VIMRUNTIME/compiler/rustc.vim:22

                                        Although, maybe we should write `%:p:S`, because
                                        it could be more reliable...

##
## What does `:compiler foo` do (6 steps)?

1. delete the variables `current_compiler` and `b:current_compiler`

Probably to prevent a guard from stopping the sourcing in step 3.

2. define the `:CompilerSet` user command, which will set options with:

    - :setlocal  if  :compiler   was NOT followed by a bang
    - :set       if  :compiler   WAS     followed by a bang

3. execute:

         :runtime! compiler/foo.vim

The plugin `foo.vim` is expected to set options with `:CompilerSet`, and set the
`current_compiler` variable to the name of the compiler.

Also,   to   support  older   Vim   versions,   `foo.vim`  should   always   use
`current_compiler` and not `b:current_compiler`.
`b:current_compiler` will be set automatically in step 5.

4. delete the `:CompilerSet` user command

5. set `b:current_compiler` to the value of `current_compiler`

6. without `!`, the old value of `current_compiler` is restored

Indeed, `current_compiler` is a global variable, and so it contains the value of
the current global compiler.
But without `!`, `:compiler` should only  set the local compiler, not the global
one.

#

# :make
## Is `:make` only useful to start a compiler?

No.

It's true that the primary purpose of `:make` is to handle a compiler, hence the
name of the `:compiler` command, and the `compiler/` directory.
This is also why  compilers are often mentioned in this document,  as well as in
`:help quickfix`.

However,   more    generally,   `:make`   can    be   used   to    execute   any
[build automation][1] tool and parse the output of the latter to populate a qfl.

Compiling is  only one step in  a building process; others  exist like packaging
and testing.
`make(1)` is an example of build automation tool.
`gcc(1)` is an example of compiler.

## Which command should I type to manually invoke `:make`?

             ┌ if you don't include % in 'mp', you may need to do it here
             │
    sil make! | redraw! | cw
    │       │         │   │
    │       │         │   └ open the window if the qfl contains valid errors; close it otherwise
    │       │         │
    │       │         └ eliminate possible rendering artifacts;
    │       │           an artifact is any pixel whose color has been generated randomly
    │       │
    │       └ don't jump to the first error
    │
    └ don't show me the output in the shell

##
## Does `:make` alter the output of the shell command?

Yes.  It replaces all NUL characters with SOH (Start Of Heading: 0x01).

Same thing for `:grep`, btw.

##
# 'makeprg'
## What's the most reliable way to refer to the current file in this option?

    -- %:p:S

The `:S`  filename modifier makes sure  to quote possible special  characters in
the filename.

`--` makes  sure to  prevent the  shell from interpreting  the beginning  of the
filename as an option of the compiler command if it begins with a hyphen.
For example, if your file is named `-a`,  you don't want the shell to parse `-a`
as an optional argument, but as a positional one.

##
## Do I need to protect the characters which are special on
### Vim's command-line?

No:

    :sp +put\ ='hello\ world!' /tmp/some_str\%nge_name.md
    :set mp=pandoc\ -o\ %:p:r.pdf\ %:p | 4verb make
    ✔

### the shell's command-line?

Yes:

    :sp +put\ ='hello\ world!' /tmp/some\ strange\|name.md
    :set mp=pandoc\ -o\ %:p:r.pdf\ %:p | 4verb make
    Calling shell to execute: "pandoc -o /tmp/some strange|name.pdf /tmp/some strange|name.md  2>&1| tee /tmp/vBQggd1/5"˜
    ✘
    zsh:1: command not found: name.pdf˜
    pandoc: strange: openBinaryFile: does not exist (No such file or directory)˜
    zsh:1: command not found: name.md˜


                             vv         vv
    :set mp=pandoc\ -o\ %:p:r:S.pdf\ %:p:S | 4verb make
    Calling shell to execute: "pandoc -o '/tmp/some strange|name'.pdf '/tmp/some strange|name.md'  2>&1| tee /tmp/vBQggd1/9"˜
    ✔

##
## Do I need to use `--` after the optional arguments of my shell command?

Prefer using `:p`.

`--` is useful when one of your filepaths begins with a hyphen.
But if you expand all the filepaths with `:p`, they will be absolute.
And an absolute filepath can *not* begin  with a hyphen; it always begins with a
slash.

##
# 'errorformat'
## What's the purpose of this option?

When an error occurs during the compilation of a file, a message will be output.
Vim uses `'efm'` to parse the  message, extract useful information, and use them
to populate the fields of a qfl entry.

## What does it contain?

It specifies a list of formats.

The first one which matches the error message is used.
`'efm'`  can  contain  several  formats for  different  messages  your  compiler
produces (or even for different compilers).

Two consecutive formats must be separated by commas.

Each entry in `'efm'` is a scanf-like string that describes the format.

##
## What's the difference between an entry, a format, a pattern?

They all refer to the same thing, but in different contexts:

   - it's an ENTRY from the point of view of 'efm' as a whole
   - it's an error FORMAT string when it's used to parse the line, and extract some info
   - it's a PATTERN when it's matched against a compiler's output line

##
## Can I build 'efm' progressively?

Yes, `:CompilerSet` can be passed the `+=` operator:

    :CompilerSet efm+=val1
    :CompilerSet efm+=val2
    :CompilerSet efm+=val3
    ...

##
## In which order are the formats compared to the compiler's output lines?

Every SINGLE line in the output of  the compiler is matched against EVERY format
in `'efm'`, from the first one until the last one, or until a match is found.

For example, if one has:

    setl efm=F₁,F₂,F₃

Where F₁, F₂, F₃ are formats.
Each line  in the output of  the compiler will  be matched against F₁,  then F₂,
then F₃.
Just because F₂ matches  a compiler's output line does NOT mean  that F₃ will be
tried first on the next line, even if F₂ and F₃ are multiline formats using `%C`
or `%Z`.

## Is the comparison case-sensitive?

No.

If you want the case to match, add the atom `\C` to the format using the `%\\C` item.

##
## What happens if no format in 'efm' matches the error message?

The matching parts from the last format  will be used, although the file name is
removed.

Also, the  error message is set  to the whole line,  which is useful to  let the
user know on which line the parser has failed, and for which kind of output they
should modify `'efm'`.

This produces an invalid, and non-interactive, entry in the qfl.

---

Exception: if the last format is:

    %-G%.%#

the line will simply be ignored.

## What happens if I use the same item several times?

    ┌──────────────────────────────────┬───────────────────┬─────────────────────────────┐
    │                                  │ the item is %m    │ the item is NOT %m          │
    ├──────────────────────────────────┼───────────────────┼─────────────────────────────┤
    │ the items are spread across      │ the matched texts │ the first matched text wins │
    │ several multiline formats        │ are concatenated  │                             │
    ├──────────────────────────────────┼───────────────────┼─────────────────────────────┤
    │ the items are in a single format │ E372              │ E372                        │
    └──────────────────────────────────┴───────────────────┴─────────────────────────────┘

## What to do if a format may match the output of several compilers, but not in a right way?

IOW, you have a format F₁ which correctly matches the output of a compiler C₁,
but also INcorrectly matches the output of another compiler C₂.

In this  case, Vim may use  F₁ to parse the  output of C₂, and  populate the qfl
with a wrong entry.


Solution:

Assuming you have a format F₂ matching the output of C₂ which does NOT match the
output of C₁ (thus more restrictive), move F₁ after F₂.

IOW, the more  compilers' output your format  matches, the more to  the right of
`'efm'` it should be.

That's my interpretation of this recommendation in `:help efm-entries`:

   > If there is a pattern that  may match output from several compilers (but
   > not in a right way), put it after one that is more restrictive.

I could be wrong.

---

In practice, this rule is especially useful for this format:

    %C%.%#

It lets you make Vim overread any line in a multiline output.
However, it doesn't extract any information (`%f`, `%l`, `%c`, ...), so you must
move it at the end of `'efm'`, because Vim should use it as a last resort.

##
# % items
## Which % items can I use in a format?
### % [a-z]

    ┌──────────┬───────────────────────────────────────────────┬────────────────────┐
    │ % item   │ how it's going to be interpreted              │ what does it match │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %f       │ file name                                     │ string             │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %l       │ line number                                   │ number             │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %c       │ column number                                 │ number             │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %v       │ virtual column number                         │ number             │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %n       │ error number (for lookup in a documentation)  │ number             │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %t       │ error type                                    │ single character   │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %m       │ error message                                 │ string             │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %o       │ text to display in the filename column        │ string             │
    │          │                                               │                    │
    │          │ mnemonic: mOdule                              │                    │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %p       │ pointer line                                  │ sequence of:       │
    │          │                                               │                    │
    │          │ its length will be used for the column number │ -  .  SPC  Tab     │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %r       │ the Rest of a line matched by a format        │ string             │
    │          │ beginning with the prefix %O, %P or %Q        │                    │
    ├──────────┼───────────────────────────────────────────────┼────────────────────┤
    │ %s       │ search text                                   │ string             │
    └──────────┴───────────────────────────────────────────────┴────────────────────┘

### % [A-Z]

You can read the output of programs that produce multiline messages.
Possible prefixes are:

    ┌────┬─────────────────────────────────────────────────┐
    │ %A │ start of a multiline message (unspecified type) │
    ├────┼─────────────────────────────────────────────────┤
    │ %E │ start of a multiline error message              │
    ├────┼─────────────────────────────────────────────────┤
    │ %I │ start of a multiline informational message      │
    ├────┼─────────────────────────────────────────────────┤
    │ %N │ start of a multiline note message               │
    ├────┼─────────────────────────────────────────────────┤
    │ %W │ start of a multiline warning message            │
    ├────┼─────────────────────────────────────────────────┤
    │ %C │ continuation of a multiline message             │
    ├────┼─────────────────────────────────────────────────┤
    │ %Z │ end of a multiline message                      │
    └────┴─────────────────────────────────────────────────┘

    ┌────┬─────────────────────────────────┐
    │ %D │ 'enter directory' format string │
    ├────┼─────────────────────────────────┤
    │ %X │ 'leave directory' format string │
    └────┴─────────────────────────────────┘

    ┌────┬─────────────────┐
    │ %G │ general message │
    └────┴─────────────────┘

    ┌────┬────────────────────────────────────────────────────────────┐
    │ %O │ single-line filename message: overread the matched part    │
    ├────┼────────────────────────────────────────────────────────────┤
    │ %P │ single-line filename message: push file %f onto a stack    │
    ├────┼────────────────────────────────────────────────────────────┤
    │ %Q │ single-line filename message: pop the last file from stack │
    └────┴────────────────────────────────────────────────────────────┘

Overread probably means sth like  overlook, i.e. reading without taking anything
into account.

### % special char

It's possible to specify (nearly) any Vim regex in a format.
Meta characters have to be prefixed with `%`:

    ┌────┬──────────────────────────────────────────────────────────┐
    │ %\ │ a backslash to create an atom                            │
    │    │                                                          │
    │    │ It has to be escaped ('%\\') in ':set efm=' definitions. │
    ├────┼──────────────────────────────────────────────────────────┤
    │ %. │ any character                                            │
    ├────┼──────────────────────────────────────────────────────────┤
    │ %# │ '*' quantifier                                           │
    ├────┼──────────────────────────────────────────────────────────┤
    │ %[ │ beginning of a collection []                             │
    ├────┼──────────────────────────────────────────────────────────┤
    │ %^ │ The anchor '^', or the negation of a collection.         │
    │    │                                                          │
    │    │ Not useful as an anchor:                                 │
    │    │ Vim automatically prefix a format with it.               │
    ├────┼──────────────────────────────────────────────────────────┤
    │ %% │ a percent character                                      │
    └────┴──────────────────────────────────────────────────────────┘

##
## What does `%*` mean?

It's a  scanf-like notation  supported for backward-compatibility  with previous
versions of Vim.
It's equivalent to the `+` quantifier in  a regex, except that you must write it
before the atom you want to repeat, not after.

### Is there any pitfall when using it?

Yes:

   - do NOT escape the following atom with a percent
   - do NOT use it to repeat a literal character (with no special meaning)

For example, all of these items are wrong:

    %*a
      │
      └ ✘ you can NOT apply `%*` to a literal character

    %*%\\d
      │
      └ ✘ you must NOT escape a character class with %

    %*%[0-9]
      │
      └ ✘ you must NOT escape the beginning of the collection with %

    %*[%^0-9]
       │
       └ ✘ if you use ^ to negate the collection, you must NOT escape it with %

Instead, they should be written like this:

    %*[a]
    a%\\+

    %*[0-9]
    %[0-9]%\\+

    %*[^0-9]
    %[^0-9]%\\+

    %*\\d
    %\\d%\\+

##
## What's the purpose of the conversion
### `%+` and `%-`?

These codes can be combined with most uppercase items (AEIW C Z G OPQ):

    ┌────┬────────────────────────────────────────────────────────────────┐
    │ %- │ do not use anything in this line to add to the `message` field │
    ├────┼────────────────────────────────────────────────────────────────┤
    │ %+ │ append the whole matching line to the `message` field;         │
    │    │ without `+`, only the text matched by the %m item is added     │
    └────┴────────────────────────────────────────────────────────────────┘

---

`%+` has no effect  on any item in a format, except `%m`  which is ignored since
Vim will use the whole line to append to the message.

---

`%-` has a different effect depending on the uppercase item it's combined with:

   - with [AEIW G OPQ], the whole line is ignored

     the line doesn't even create an entry in the qfl

   - with [CZ], nothing changes

     it's as if you had used `%C`, `%Z`

### `%>`?

Suppose Vim finds a format F which  contains `%>` and which matches a compiler's
output line.
Because of `%>`, when  Vim will parse the next line, it  will ignore all formats
before F.

It's useful  for patterns  that match  anything, because  Vim does  NOT remember
which format in `'efm'` matched the previous line.

For example, if the error looks like this:

    Error in line 123 of foo.c:
    unknown variable "i"

This can be parsed with:

    :CompilerSet efm=%-Gunknown%.%#
        \,%E%>Error\ in\ line\ %l\ of\ %f:
        \,%Z%m

The resulting qfl will be:

    foo.c  |123 error  |  unknown variable "i"

Without `%>`:

    :CompilerSet efm=%-Gunknown%.%#
        \,%EError\ in\ line\ %l\ of\ %f:
        \,%Z%m

The qfl would be:

    foo.c  |123 error  |

Here the "unknown" line has been matched by the 1st format, so has been ignored,
which prevented it from populating the `message` field of the qfl entry.

### `%o`?

It populates the `module` field of a qfl entry.

If present, it will be used in the quickfix window instead of the filename.
The module name is used only for  displaying purposes, the filename is used when
jumping to the file.

### `%p`?

It populates the  `col` field of a  qfl entry, when the compiler  outputs a line
like:

    ---------^

to indicate the column of the error.

Usually,  `%p`  is used  in  a  multiline error  message,  and  followed by  the
character(s):

    ┌──────────────┬─────────────────────────┐
    │ character(s) │ match this pointer line │
    ├──────────────┼─────────────────────────┤
    │ ^            │ ---------^              │
    ├──────────────┼─────────────────────────┤
    │ 1            │          1              │
    ├──────────────┼─────────────────────────┤
    │ \|           │ .........|              │
    ├──────────────┼─────────────────────────┤
    │ %*[0-9^]     │ -------123^             │
    └──────────────┴─────────────────────────┘

You need to escape  the bar in `%p\|` to prevent it from  being interpreted as a
command termination by `:set` or `:CompilerSet`.

Usage example:

    $ tee <<'EOF' /tmp/log
    /tmp/log:here iz an error
    ---------------^
    EOF

    $ tee <<'EOF' /tmp/efm.vim
        set mp=cat\ /tmp/log
        set efm=%E%f:%m,%-Z%p^
        sil make! | redraw!
        copen
    EOF

    $ vim -S /tmp/efm.vim
    " Press Enter on the qfl entry, and the cursor will jump onto the `z` of `iz`.

See `:help errorformat-javac` for another useful example.

### `%s`?

It populates the `pattern` field of a qfl entry.
This field is used to locate the error line.

To  make the  search as  accurate as  possible, Vim  adds (to  the text  used to
convert `%s`):

   - the anchors `^` and `$`
   - the `\V` atom as a prefix

Which gives:

    ^\V pat \$
        │
        └ text used to replace %s

Usage example:

    $ tee <<'EOF' /tmp/log
    some text
    look for me
    /tmp/log:look for me:here iz an error
    some text
    EOF

    $ tee <<'EOF' /tmp/efm.vim
        set mp=cat\ /tmp/log
        set efm=%f:%s:%m,%-G%.%#
        sil make! | redraw!
        copen
    EOF

    $ vim -S /tmp/efm.vim

Press Enter on the qfl entry, and the cursor will jump on the `look for me` line.

### `%t`?

It populates the `type` field of a qfl entry.

Here are some usage examples taken from `$VIMRUNTIME/compiler/`:

    ┌────────────────────────────────────────┬────────────────────────────────────┐
    │ items                                  │ can match                          │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %t%*[^:]                               │  error:    info:                   │
    │ ├┘├┘├──┘                               │  ^         ^                       │
    │ │ │ └ any character other than a colon │                                    │
    │ │ └ the next atom can be repeated 1    │  note:     warning:                │
    │ │   or as many times as you want       │  ^         ^                       │
    │ └ a character                          │                                    │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %trror                                 │ Error                              │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ Syntax%trror                           │ SyntaxError                        │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ LaTeX\ %trror                          │ LaTeX Error                        │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %tatal Error                           │ Fatal Error                        │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %tarning                               │ warning                            │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %tBORT                                 │ ABORT                              │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %tOTE                                  │ NOTE                               │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %tEVERE                                │ SEVERE                             │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %tEBUG                                 │ DEBUG                              │
    ├────────────────────────────────────────┼────────────────────────────────────┤
    │ %tNFO                                  │ INFO                               │
    └────────────────────────────────────────┴────────────────────────────────────┘

##
## Does the `%f` conversion always match a filename?

Not necessarily.

If nothing follows `%f`, the rest of the line is included in the conversion.
Otherwise, `%f`  will consume as much  text as necessary to  reach what follows,
regardless of whether the consumed characters are in `'isf'`.

    $ tee <<'EOF' /tmp/log
    foo:bar:12:baz
    qux:34:norf
    EOF

    $ tee <<'EOF' /tmp/efm.vim
        set mp=cat\ /tmp/log
        set efm=%f:%l:%m
        sil make! | redraw!
        copen
    EOF

After sourcing `/tmp/efm.vim`, the qfl will be:

    foo:bar  |12  | baz
    qux      |34  | norf

The first  entry shouldn't  be valid, because  `:` is not  in `'isf'`,  and thus
`foo:bar` is not a valid filename.

### How to make sure it always matches a filename?

Append a backslash right after `%f`:

    set efm=%f\\:%l:%m
              ^^

This time, after sourcing `/tmp/efm.vim`, the qfl will be:

    || foo:bar:12:baz
    qux |34| norf

The first entry is not a valid entry anymore, which is expected.

##
## Does the `%m` conversion always match an error message?

Not necessarily.

It matches ANY string of text.  Even a pointer line:

    ----------^

This line can be matched by `%p` AND `%m`.


`%m` is equivalent to `%.%#`, except that  it populates the `message` field of a
qfl entry.
So,  if nothing  follows `%m`  in the  format, the  rest of  the output  line is
included in the conversion.

##
## Should I write `%^` or `^`?

TLDR:

Use  `%^`  only to  negate  a  collection to  which  you  don't apply  the  `%*`
quantifier.
Otherwise, use `^`.

---

You don't need `%^` as an anchor, because Vim adds it automatically to a format.

If you use `^` to negate a collection, you MUST escape it with a percent:

    "                ┌ `^` is escaped
    "                │
    let &efm = '%f:%[%^x]:%m'
    cgetexpr ['/tmp/efm.vim:y:some message']
    copen

But you must NOT escape it if you apply the `%*` quantifier:

    "                 ┌ `^` is NOT escaped
    "                 │
    let &efm = '%f:%*[^x]:%m'
    cgetexpr ['/tmp/efm.vim:yyy:some message']
    copen

Finally, after a pointer, whether you prefix `^` with a percent, or not, doesn't
matter:

    "                   ┌ escaped
    "                   │
    let &efm = '%f %l %p%^%m'
    cgetexpr ['/tmp/efm.vim 3 ---------^ some message']
    copen

    "                   ┌ not escaped
    "                   │
    let &efm = '%f %l %p^%m'
    cgetexpr ['/tmp/efm.vim 3 ---------^ some message']
    copen

I would still recommend you use `%p^`.
Because, that's what the authors of the default compilers do most of the time:

    :vim /%p^/gj $VIMRUNTIME/compiler/*.vim
        14 matches

    :vim /%p%^/gj $VIMRUNTIME/compiler/*.vim
        3 matches

##
## Can `%#` be used after anything?

Yes.

After a character, an atom, or a collection.

    a%.%#

    %\\s%#

    %[%^:]%#

##
## Why must I escape an atom with `%`, instead of a backslash?

The leading  `%` is probably  necessary for the parsing  of `'efm'` to  send the
desired atom to the regex engine.
Without `%`, the latter would receive a simple character.

Indeed, when  Vim parses a  `:set efm` command  to determine which  option(s) to
set, and how, it removes one level of backslash (see `:help option-backslash`).
Then, when Vim parses the `'efm'` value to determine which format(s)/item(s) are
written, it removes one level of percent sign and one level of backslash.
But if it  encounters `%\`, it doesn't remove both  characters; only the percent
sign.

Here's what happens when you add `%` in front of an atom for a whitespace:

        %\\s
     →   %\s
     →    \s

And without `%`:

         \\s
       →  \s
       →   s
           ^
           the regex engine would receive a literal `s` character

---

However, note that in theory, you could replace `%` with `\\`:

    set efm=%f:%l:\\.\\*:%m
    cgetexpr ['/tmp/file:123:foobar:some message']
    copen

    set efm=%f:%l:\\\\u:%m
    cgetexpr ['/tmp/file:123:A:some message']
    copen

But  `%` makes  the  code a  little  more readable,  by  reducing the  backslash
explosions.

##
## What happens if I use the items `%s` and `%l`, and the error message contains a line number?

If the search  is successful, the line  number will not be used  when jumping to
the entry.  The `pattern` field has priority over the `lnum` one.

MWE:

    $ tee <<'EOF' /tmp/log
    some text
    look for me
    /tmp/log:3:look for me:here iz an error
    some text
    EOF

    $ tee <<'EOF' /tmp/efm.vim
        set mp=cat\ /tmp/log
        set efm=%f:%l:%s:%m,%-G%.%#
        sil make! | redraw!
        copen
    EOF

    $ vim -S /tmp/efm.vim

Press Enter on  the qfl entry, and the  cursor will jump on the  2nd line (which
matches the pattern `^\Vlook for me\$`).
It doesn't jump on the 3rd line, even though the `lnum` field of the qfl entry is `3`.

##
# Special characters
## In a format, can I include
### `[0-9]`?

Yes.

MWE:

    let &efm = '%f: %*[0-9] %m'
    cgetexpr ['/tmp/efm.vim: 123 text']
    copen

However in `:help quickfix-valid`:

   > Some examples for C compilers that produce single-line error outputs:
   >
   > `%f:%l:\ %t%*[^0123456789]%n:\ %m`    for Manx/Aztec C error messages
   >                                     **(scanf() doesn't understand [0-9])**

It seems to indicate that, in order to  parse the output of a compiler, Vim uses
the `scanf()` function of the latter, which seems to be confirmed by `:help error-file-format`:

   > Each entry in 'errorformat' is a scanf-like string that describes the format.
   > First, you need to know how scanf works.
   > Look in the documentation of YOUR C compiler.

To see all  the locations where a  collection of digits is written  in a default
compiler plugin, run:

    :vim /\[^\=\d/gj $VIMRUNTIME/compiler/*.vim

### a newline?

No.

Every SINGLE  line of the compiler's  output is matched against  every format in
`'efm'`.
So, don't try to include `\n` in a  format to match a multiline message, it will
never work.

### a tilde?

Yes, but you must NOT escape it with a percent.

Otherwise, it  will be  expanded into  the replacement string  used in  the last
successful substitution command.

MWE:

    let &efm = '%f:%l:%~:%c:%m'
    s/pat/rep/ne
    cgetexpr ['/tmp/efm.vim:1:rep:2: some message']
    copen

### `\%(...\)`?

Yes.

In `/tmp/log` write:

    /tmp/file:12:error one foo
    /tmp/file:34:error two bar
    /tmp/file:56:error three baz

Then source:

    set mp=cat\ /tmp/log
    set efm=%f:%l:%m\ %\\%%(foo%\\\|baz%\\)

    silent make! | redraw!
    copen

The qfl should  display only 2 valid  entries; the one containing  'foo' and the
one containing 'baz'.


Note:

    \%(foo\|baz\)            in a regular Vim regex
        ⇔
    %\%%(foo%\|baz%\)        in 'efm' (:let)
        ⇔
    %\\%%(foo%\\\|baz%\\)    in 'efm' (:set)

### `\(...\)`?

No.

It is reserved for internal conversions.

That's what the help says, but in reality I think you can.
However Vim won't treat the text as  a sub-expression to which you can refer via
a backref.

I still  recommend you don't  use `\(...\)`, and  prefer `\%(...\)` so  that the
code explicitly tells that the text is not remembered.

### any Vim regex?

Yes, almost.

You can't use `\(...\)` to capture some text, then use backreferences.

Otherwise,  you   can  probably  use   any  Vim  atom,   including  lookarounds,
alternations, and `%\(...%)`.
Just remember to  escape an atom with a  `%`, and if you use  `:set`, double the
backslash.

##
## What's the difference between
### `%m` and `%\\m`?

`%m` refers to a message error string.

`%\m` and `%\\m` refer to the magic mode  in a regex, resp. inside a `:let &efm`
assignment, and inside a `:set efm` assignment.

### `%s` and `%\\s`?

`%s` refers to a string used to locate an error.

`%\s` and `%\\s`  refer to a whitespace, resp. inside  a `:let &efm` assignment,
and inside a `:set efm` assignment.

##
## How to include a backslash/bar/comma/"/SPC in a format in 'efm'?

If you  use `:set`  to assign  a value  to `'efm'`,  and you  want to  include a
special character, you may need to escape it.

    ┌──────────────┬─────────────────────┬─────────────────────┐
    │ character    │ write this for :let │ write this for :set │
    ├──────────────┼─────────────────────┼─────────────────────┤
    │ backslash    │ \                   │ \\                  │
    ├──────────────┼─────────────────────┼─────────────────────┤
    │ bar          │ \|                  │ \\|                 │
    ├──────────────┼─────────────────────┼─────────────────────┤
    │ comma        │ \,                  │ \\,                 │
    ├──────────────┼─────────────────────┼─────────────────────┤
    │ double quote │ "                   │ \"                  │
    ├──────────────┼─────────────────────┼─────────────────────┤
    │ space        │ SPC                 │ \ SPC               │
    └──────────────┴─────────────────────┴─────────────────────┘

When there're several backslashes, one level  of them will be removed by `:set`,
because a backslash has a special meaning for the latter: it allows to include a
backslash, bar, comma, double quote, space in an option value.

## Why do I need two backslashes to include a comma in a format?

`'efm'` is assigned a SINGLE value, which may contain a list of SEVERAL formats.

The  1st  backslash  prevents  Vim,   when  parsing  the  `:set`  command,  from
interpreting a comma as a separator between 2 option values (again, there's only
one value).
The  2nd  backslash prevents  Vim,  when  parsing  the  value of  `'efm'`,  from
interpreting the comma as a separator between 2 formats.

## How to match a literal backslash in an error message?

If you use `:let`, multiply the backslashes by 4:

    let &efm = '%f:%l:\\\\z:%m'
    cgetexpr ['/tmp/file:123:\z:some message']
    copen

The  parsing of  `'efm'`, then  the invocation  of the  regex engine,  will each
remove on level of backslash.

---

If you use `:set`, or `:CompilerSet`, multiply the backslashes by 8:

    CompilerSet efm=%f:%l:\\\\\\\\z:%m

This time, the parsing of the `:set`  command, then the parsing of `'efm'`, then
the regex engine, will each remove one level of backslash.

This explosion of backslashes is due to the fact that a backslash is special for
every context:

   - the parsing of `:set ...`  (used to escape some special characters)
   - the parsing of 'efm'       (")
   - the regex engine           (")

The more  contexts (`n`)  a token  is special in,  the more  backslashes (`2^n`)
you'll need to match it literally.

##
# Multiline error messages
## What's the purpose of `%D` and `%X`?

Some compilers produce messages that consist  of directory names that have to be
prepended to each file name read by `%f` (example: GNU make).

`%D` and `%X` allow you to manipulate an internal directory stack in which those
names are stored.

They resp. push  a directory name on  the stack, and pop the  directory from the
top of the stack.
Vim prepends the directory at the top  of the stack to each erroneous file found
with a relative path.

Both expect a following `%f` that finds the directory name.

### Are they reliable?

It depends on whether the compiler prints  the absolute path of any directory it
enters, and a message once it leaves it.

GNU-make does this, although it may be useful to use the option `-w` to force it
to print out the working directory before and after processing.

Other compilers don't print any information about their working directory.

In this case, you need to enhance  the makefile to make sure the compiler prints
absolute directory names and "Leaving directory" messages.

Examples for Makefiles:

    Unix:
        libs:
                for dn in $(LIBDIRS); do                            \
                    (cd $$dn; echo "Entering dir '$$(pwd)'"; make); \
                    echo "Leaving dir";                             \
                done

To parse the output produced by such a makefile, add to your 'efm':

         %DEntering\ dir\ '%f'
       \,%XLeaving\ dir

Note  that Vim  doesn't check  if the  directory name  in a  "Leaving directory"
message is the compiler's current directory.
That's why you can print the message "Leaving dir" without any additional name.

##
## What's the difference between `%[EINW]` and `%t`?

`%E`, `%I`,  `%N` and `%W`  automatically populate the  `type` field of  the qfl
entry with the values `error`, `info`, `note`, `warning`.

However, if you also use `%t`, the latter will have the priority:

    $ tee <<'EOF' /tmp/log
    /tmp/file:12:info:some message
    EOF

    $ tee <<'EOF' /tmp/efm.vim
        set mp=cat\ /tmp/log
        set efm=%E%f:%l:%t%*[^:]:%m
        sil make! | redraw!
        copen
    EOF

`%E` should yield a qfl entry whose type is `error`, but because of `%t` and the
string `:i:` in `/tmp/log`, its type will be `info`.

##
## How to use `%G`?

    ┌─────────┬────────────────────────────────────────────────────────────────────┐
    │ %-G     │ ignore an empty line                                               │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ %-G%.%# │ ignore any line                                                    │
    │         │                                                                    │
    │         │ useful at  the end  of 'efm'  to prevent  an unmatched  line from  │
    │         │ creating an invalid entry in the qfl                               │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ %G      │ create an entry in the qfl whose only populated field is `message` │
    │         │ use the text matched by the `%m` item to populate `message`        │
    ├─────────┼────────────────────────────────────────────────────────────────────┤
    │ %+G     │ same thing                                                         │
    │         │ but this time, use the whole line to populate 'message'            │
    └─────────┴────────────────────────────────────────────────────────────────────┘

More  generally, `%-G{fmt}`  is useful  to ignore  general information  like the
compiler version or other headers.

## How to use `%O`, `%P`, `%Q`, `%r`?

These prefixes  are useful  if the file  name is given  only ONCE,  and multiple
errors follow that refer to this file name.

`%O`, `%P` and `%Q` parse a file name matched by a following `%f`.

`%O` doesn't push the file name onto an internal stack.
`%P` pushes the file name onto an internal stack.
`%Q` pops the file name at the top of the stack.

`%r` prevents the matched text (rest of the line) from being consumed.
It will be parsed afterwards in another pass.

---

Example 1:

Given a compiler that produces the following error logfile:

    [/tmp/file1]
    (1,17)  error: foo
    (21,2)  warning: bar
    (67,3)  error: baz

    [/tmp/file2]

    [/tmp/file3]
    (2,2)   warning: qux
    (67,3)  warning: norf

It can be properly parsed by this `'efm'`:

    CompilerSet efm=%-P[%f]
        \,(%l\\,%c)%*[\ ]%t%*[^:]:%m
        \,%-Q

A call to `:clist` writes the errors with their correct filenames:

    /tmp/file1:1 col 17 error: foo
    /tmp/file1:21 col 2 warning: bar
    /tmp/file1:67 col 3 error: baz
    /tmp/file3:2 col 2 warning: qux
    /tmp/file3:67 col 3 warning: norf

Note that  usually `%f` matches  ANY file, but here,  because of `%P`,  the file
MUST exist (it's a Vim bug).
This matters when you try to debug a format prefixed by `%P`, and you wonder why
the entries in the qfl don't pick up some non-existing filenames.

---

Example 2:

Given a compiler that produces the following error logfile:

    (/tmp/file4) [/tmp/file1]
    (1,17) foo
    (21,2) bar
    (67,3) baz

    (/tmp/file5) [/tmp/file2]

    (/tmp/file6) [/tmp/file3]
    (2,2)  qux
    (67,3) norf

It can be properly parsed by this `'efm'`:

    CompilerSet efm=%-O(%f)%r
        \,%-P%[%^()]%#[%f]
        \,(%l\\,%c)\ %m
        \,%-Q

A call to `:clist` writes the errors with their correct filenames:

    /tmp/file1  |1 col 17  | foo
    /tmp/file1  |21 col 2  | bar
    /tmp/file1  |67 col 3  | baz
    /tmp/file3  |2 col 2   | qux
    /tmp/file3  |67 col 3  | norf

## How to ignore a line?

If it's inside a multiline message, use `%-C`, otherwise `%-G`.
In both cases, don't include any item extracting info (`%m`, `%l`, `%p`, ...).

The more specific the format you use to  match the line is, the more to the left
of `'efm'`, you should move it.
In particular,  `%-C%.%#` and  `%-G%.%#` should  always be to  the far  right of
`'efm'`.

## How to take into account only the first error in a stacktrace?

Write `%C{fmt}` at the beginning of `'efm'`.
Where  `{fmt}` is  a  format which  matches  the  2nd, 3rd,  ...  errors in  the
stacktrace, but doesn't  contain any item populating the qfl  entry (`%m`, `%p`,
...).

It will make Vim ignore all errors  between the beginning of a multiline message
(`%[AEIW]`) and its end (`%Z`).

## How to prevent an output line from creating any entry in the qfl?

Usually each output line produces a distinct entry in the qfl.

But not if it's matched by a format prefixed with `%C`, `%Z` or `%G`.

With  `%C` and  `%Z`,  only some  information  are extracted  from  the line  to
populate the entry CURRENTLY built in the qfl.
But it doesn't create a new entry.

With `%-G`, you can ignore the line entirely.

##
## Why shouldn't I use a simple `%P` without `+` or `-`?

Because `%P` doesn't accept any item except `%f` and `%r`:

    E373: Unexpected %m in format string

So, if you don't  combine `%P` with `+` or `-`, you'll end  up with an (invalid)
entry without any message.
You should  use `%+P` to get  an (invalid) entry displaying  the filename pushed
onto the stack.
Or use `%-P` to eliminate the entry entirely.

## Must a format prefixed with `%Z` be at the end of 'efm'?

Not necessarily.

It can be anywhere inside `'efm'`.
Same thing for `%[AEIWCG]`.
There's  no obvious  relation between  the  position of  a line  in a  multiline
message, and the position of its format in `'efm'`.

Usually, the formats in  `'efm'` are ordered from the most  specific to the less
one:

    CompilerSet efm=%A%f:%l:\ %m,%+Z%p^,%+C%.%#,%-G%.%#

Here, we have 4 formats:

    %A%f:%l:\ %m
    %+Z%p^
    %+C%.%#
    %-G%.%#

The `%A` format is the most specific one, because it contains the most info.
The `%Z` format is less specific, because  it contains less info, but still some
(`%Z`, `%p`, `^`).
The `%C` format is less specific, (only `%C` is an info).
The `%G` format  is the least specific (all  we know is that it's  a random line
outside a multiline message).

## Must a multiline message be parsed in this order: beginning-continuation-end?

Yes.

You can parse it in this order:

    ┌ beginning (%A, %E, %I, %W)
    │┌ continuation (%C)
    ││┌ end (%Z)
    │││
    ACZ

But not in these orders:

    AZC    the continuation line(s) would not be recognized as such
    ZAC    "
    CAZ

    ZCA    the continuation line(s) and the ending line would not be recognized
    CZA    "


MWE:

    $ tee <<'EOF' /tmp/log
    /tmp/foo:12
     hello
            ^

    /tmp/bar:34
     world
                ^
    EOF

    $ tee <<'EOF' /tmp/efm.vim
        set mp=cat\ /tmp/log
        set efm=%A%f:%l,%C\ %m,%Z%p^
    EOF

Then, reorder the formats in `'efm'`, and the lines in the log file.

##
## Can a format parse only a part of a line?

Only a format prefixed with `%O`, `%P` or `%Q` can do that.

All the other formats parse WHOLE lines.

If a format is  prefixed with `%O`, `%P`, or `%Q`, the text  matched by the `%r`
item won't be consumed.
It will be parsed during another pass.
So, you can parse the same output  line in several consecutive passes, until the
end of line is reached.

Each step will push, pop or overread a filename.
This is useful  if the output line  contains several file names,  and you aren't
interested in the 1st one.

## Can I use several uppercase items in the same format?

No.

You can only use one uppercase item as a prefix at the beginning of a format.

## Can I use an uppercase item after the beginning of a format?

No.

Any uppercase item must appear at the very beginning of a format.

##
## What are some examples of 'efm' values to parse multiline messages?

Suppose your compiler writes errors in the following format:

    Error 275
    line 42
    column 3
    ' ' expected after '--'

Set `'efm'` like this:

    CompilerSet efm=%E%trror\ %n
        \,%Cline\ %l
        \,%Ccolumn\ %c
        \,%Z%m

---

Suppose your python interpreter produces the following error message:

    Traceback (most recent call last):
      File "unittests/dbfacadeTest.py", line 89, in testFoo
        self.assertEquals(34, dtid)
      File "/usr/lib/python2.2/unittest.py", line 286, in
     failUnlessEqual
        raise self.failureException, \
    AssertionError: 34 != 33

And you want to parse all these lines to populate the qfl with this single entry:

    unittests/dbfacadeTest.py:89:  AssertionError: 34 != 33

Set `'efm'` like this:

    CompilerSet efm=%C\ %.%#
        \,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#
        \,%Z%[%^\ ]%\\@=%m
        \,%-GTraceback%.%#


Note that the format using `%C` is given before the one using `%A`.
Necessary to ignore the 2nd error:

    File "/usr/lib/python2.2/unittest.py", line 286, in

Indeed, when the first line beginning with 'File' will be parsed, it won't match
the `%C` format,  because Vim won't have found a  beginning of multiline message
yet.
So, it will be matched by the `%A` format instead.
OTOH, the  2nd line beginning  with 'File' will be  matched by the  `%C` format,
because at  that point  in time, Vim  WILL have found  a beginning  of multiline
message.


Also, note that the format using `%-G` is useful to ignore the 1st line:

    Traceback (most recent call last):

Without `%-G`, this line would not be matched by any format:

   - the 1st format describes the continuation of a multiline message  (Traceback... is not ✘)
   - the 2nd format describes the beginning of a multiline message     (" ✘ )
   - the 3rd format describes the end of a multiline message           (" ✘ )

So,  Vim would  use the  last format  to  parse this  line, which  would give  a
non-interactive entry in the qfl.

`%-G` lets you eliminate that kind of noise.

##
# Issues
## How to debug 'efm'?

Warning:

For some reason, after you edit `efm.vim`,  you often have to source it multiple
times before Vim updates the qfl.
If the qfl doesn't display what you expect, make sure to re-source your script a
few times before trying to fix it.


    $ tee <<'EOF' /tmp/efm.vim

    set efm=%f:%s:%m
    call setqflist([], 'f')
    cgetexpr ['/tmp/efm.vim:" bar:baz']
    copen

    " bar baz
    " bar
    " foo bar
    EOF

    $ vim -S /tmp/efm.vim

Don't set the  local value of `'efm'`;  the format would be tied  to the current
buffer which is *not* the set of lines we're going to pass to `:cgetexpr`.

Replace the value assigned to `'efm'` with the one you want to test.
Same thing  for the  compiler's output  lines and  the list  of lines  passed to
`:cgetexpr`:

    set efm={your value}
    cgetexpr ['your output lines', ...]

---

Alternative (better suited for multilines compiler's outputs):

                     ┌ write the output of a compiler you want to parse
                     │
    set mp=cat\ /tmp/log
    set efm={your value}
    call setqflist([], 'f')
    sil make! | redraw!
    copen

---

When you debug a multiline output, and  your qfl contains too much noise because
of invalid entries, use `:cl` (`:clist`), to only see the valid entries.
Use `:cl!` to see them all.

## Are there some bugs?

Yes:
<https://github.com/vim/vim/search?q=is%3Aissue+is%3Aopen+errorformat&type=Issues&utf8=%E2%9C%93>

---

If you use `%P` and `%f` together, `%f` will only match an EXISTING filename:
<https://github.com/vim/vim/issues/2334>

So, when you try to debug a format prefixed with `%P`, make sure to use existing
filenames.

The same issue applies to `%D` and `%X`:
Vim won't push/pop a non-existing directory onto/from its internal stack.

---

There are some weird items in the default compilers:

    %\t
    %-G\\s

IMO, they should be written like this:

    %\\t
    %-G%\\s

I've made some tests, and both versions work.
Don't pay attention to  the first version, it probably works  only because of an
undocumented detail of implementation.

---

Another weird item involves the literal character [.
To illustrate, we're going to parse this output:

    cgetexpr ['/tmp/file:123:[A-Z] some message']
    copen

Here's what happens depending on the value we give to `'efm'`:

    set efm=%f:%l:[A-Z]\ %m
    set efm=%f:%l:\[A-Z\]\ %m
    let &efm = '%f:%l:[A-Z] %m'

    " ✔  [A-Z] will be interpreted literally as 5 characters


    let &efm = '%f:%l:\[A-Z\] %m'

    " ✘  [A-Z] will be wrongly interpreted as a collection
      It's wrong because:

            - it's inconsistent with how Vim interprets `\[` in `:set`
            - for `[` to get a special meaning, it should be prefixed with `%` (or %*)

---

In `%-C` and `%-Z`, `-` has no effect.
Even when the format includes a `%m` item.

It seems wrong.
It should prevent Vim from adding anything to the `message` field, like with `%-G`.

One could argue  that such items are  syntactically wrong, but they  are used 38
times in the default compilers:

    :vim /\C%-[CZ]/gj $VIMRUNTIME/compiler/*.vim

And they're mentioned 6 times in `:help quickfix`.

## How to deal with an output which is too difficult to parse?

Before parsing it, you can apply  an arbitrary transformation using any command,
or custom script, to get a much-easier-to-parse output.
Awk and sed are good tools for this purpose.

For example:

    CompilerSet mp=make\ \\\|&\ my_filter
                         ├┘├┘
                         │ └ same reason, but for when `:make` is executed
                         │
                         │   in  the  end,  we  want to  get  the  bash  `|&`
                         │   redirection  operator  which connects  both  the
                         │   standard error  and the  standard output  of the
                         │   first  command  to  the standard  input  of  the
                         │   filter
                         │
                         └ to  prevent the  bar from  being interpreted  as a
                           command separator when `:set` is parsed



This 'efm' has been  reported to work well for javac, which  outputs a line with
'^' to indicate the column of the error:

    CompilerSet efm=%A%f:%l:\ %m
                  \,%-Z%p^
                  \,%-C%.%#
                  \,%-G%.%#

Here is an alternative for Unix that filters the output first:

    CompilerSet efm=%Z%f:%l:\ %m,%A%p^,%-G%.%#
    CompilerSet mp=javac\ %:p:S\ 2>&1\ \\\|\ vim-javac-filter
                             ├┘
                             └ escape characters special to the shell



You need to put the following in "vim-javac-filter" somewhere in your path
(e.g., in ~/bin) and make it executable:

    #!/bin/sed -f
    /\^$/s/\t/\ /g;/:[0-9]\+:/{h;d};/^[ \t]*\^/G;

Broken down:

    /\^$/s/\t/\ /g

            On every  line finishing  with ^ (end  of pointer),  replace all
            tabs with spaces.

    /:[0-9]\+:/{h;d}

            Copy ([h]old) and delete every line which contains a line number
            surrounded by colons.

    /^[ \t]*\^/G

            Append  ([G]et)  the  copied  line after  the  next  line  which
            contains only a sequence of whitespace and ends with ^.

IOW, this script moves the line with the filename, line number, error message to
just AFTER the pointer line.

That  way,  the unused  error  text  between doesn't  break  Vim's  notion of  a
multiline message and also doesn't force us to include it as a continuation of a
multiline message.

## How does Vim deal with a compiler which doesn't print enough info for `%D` and `%X`?

To test any of the following examples, execute:

    $ tee <<'EOF' /tmp/efm.vim
        set mp=cat\ /tmp/log

        set efm=%f:%l:\ %m,
              \,%Dmake:\ Entering\ directory\ `%f'
              \,%Xmake:\ Leaving\ directory\ `%f'

        sil make! | redraw!
        copen
    EOF

Vim uses a 3-steps algorithm.
Here's how it works.

1. Check if the given directory is a subdirectory of the compiler's working
   directory (i.e. a subdirectory of the top of the Quickfix Internal Directory
   Stack aka QIDS).  If it IS, push it on the QIDS.

Example:

    $ mkdir -p /tmp/test/dir1/dir2
    $ touch    /tmp/test/dir1/dir2/file

    $ tee <<'EOF' /tmp/log
    make: Entering directory `/tmp/test/dir1'
    make: Entering directory `dir2'
    file:123: some error
    EOF

    $ vim -S /tmp/efm.vim

When creating an entry  in the qfl, Vim correctly completes  the path to `file`,
because  `dir2` is  a  subdirectory  of `/tmp/test/dir1`  which  is the  working
directory of the compiler.

2. If it's NOT a subdirectory of the compiler's working directory, check whether
   it's a subdirectory of one of the directories below in the QIDS.

Example:

    $ mkdir -p /tmp/test/dir{1,2}/
    $ touch    /tmp/test/dir2/file

    $ tee <<'EOF' /tmp/log
    make: Entering directory `/tmp/test/'
    make: Entering directory `/tmp/test/dir1'
    make: Entering directory `dir2'
    file:123: some error
    EOF

When creating  an entry  in the  qfl, Vim  will correctly  complete the  path to
`file`, because  `dir2` is a  subdirectory of  `/tmp/test/` which is  inside the
QIDS.

3. If it's NOT a subdirectory of one of the directories below in the QIDS, it's
   assumed to be a subdirectory of Vim's working directory.

Example:

    $ mkdir -p /tmp/test/dir
    $ touch    /tmp/test/dir/file

    $ tee <<'EOF' /tmp/log
    make: Entering directory `dir'
    file:123: some error
    EOF

    $ vim +'cd /tmp/test' -S /tmp/efm.vim

When creating an  entry in the qfl,  Vim correctly completes the  path to `file`
(but only into the relative path `dir/file`), because `dir` is a subdirectory of
`/tmp/test/` which is Vim's working directory.

---

Additionally  for  every file,  Vim  checks  whether  it  really exists  in  the
constructed directory.
If it  does NOT, it's  searched in  all other directories  of the QIDS  (NOT the
directory subtree!).
If it's still not found, it's assumed to be in Vim's working directory.

---

This algorithm has some limitations.
These  examples assume  that `make`  just  prints information  about entering  a
directory in the form "Making all in dir".

1. Let's assume you have the following directories and files:

         ./dir1
         ./dir1/file1.c
         ./file1.c

If `make` processes  `dir1/` before the current directory and  there is an error
in `./file1.c`, you will end up with Vim loading `./dir1/file1.c`.

This can only be solved with a "leave directory" message.

2. Let's assume you have the following directories and files:

         ./dir1
         ./dir1/dir2
         ./dir2

You get the following:

    ┌──────────────────────┬──────────────────────────────┬────────────────┐
    │ Make output          │ Directory interpreted by Vim │ Is it correct? │
    ├──────────────────────┼──────────────────────────────┼────────────────┤
    │ "Making all in dir1" │ ./dir1                       │ ✔              │
    ├──────────────────────┼──────────────────────────────┼────────────────┤
    │ "Making all in dir2" │ ./dir1/dir2                  │ ✔              │
    ├──────────────────────┼──────────────────────────────┼────────────────┤
    │ "Making all in dir2" │ ./dir1/dir2                  │ ✘              │
    └──────────────────────┴──────────────────────────────┴────────────────┘

This can  be solved by  printing absolute  directories in the  "enter directory"
message or by printing "leave directory" messages.

##
# Todo
## Document the errorformat shell utility

- <https://github.com/reviewdog/errorformat>
- <https://reviewdog.github.io/errorformat-playground/>

   > It's basically for practicing and checking errorformat with ease in browsers.
   > I expect users can write erroformats in playground first, validate them, and use
   > it for vim's  quickfix list or other use cases  like reviewdog or efm-langserver
   > outside vim too.
   > https://github.com/reviewdog/errorformat#use-cases-of-errorformat-outside-vim

Source: <https://www.reddit.com/r/vim/comments/d7vdbk/erroformat_playground/>

##
# Reference

[1]: https://en.wikipedia.org/wiki/Build_automation
[2]: https://github.com/lacygoill/config/blob/master/.vim/template/byName/compiler.txt
[3]: https://github.com/lacygoill/vim-unix/blob/88238b4cefb226ce95a5c7447eccf065910fa9cf/plugin/unix.vim#L254-L260

