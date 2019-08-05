# Configuration
## Which options control the shell program started by `:grep` and `:make`?

    'grepprg' / 'gp'
    'makeprg' / 'mp'

## Inside the values of these options, how to refer to the arguments passed to `:grep` and `:make` at run time?

Use the placeholder `$*`.

You can use several `$*` if needed.

##
## On which options do `:grep`, `:make`, `:cgetexpr` (& friends) rely to parse what they read?

`:grep` relies on `'gfm'`.

All the other commands rely on `'efm'`.

##
## An option can be set to change how Vim redirects the output of a shell command.
### What's this option for a shell command executed by
#### `system()` or `:!`?

    'shellredir' / 'srr'

#### `:make` or `:grep`?

    'shellpipe'

##
### How to refer to the temporary file in the value assigned to these options?

Use the `%s` token.

If you don't use `%s`, it's appended automatically at the end.

### On which option does the default value of these options depend?

The second path component of `'shell'`:

    ┌───────────────────────────────┬───────────────────────┐
    │ 2nd path component of 'shell' │ default value of 'sp' │
    ├───────────────────────────────┼───────────────────────┤
    │ ∅                             │ | tee                 │
    ├───────────────────────────────┼───────────────────────┤
    │ csh                           │ |& tee                │
    │ tcsh                          │                       │
    ├───────────────────────────────┼───────────────────────┤
    │ bash                          │ 2>&1| tee             │
    │ ksh                           │                       │
    │ mksh                          │                       │
    │ pdksh                         │                       │
    │ sh                            │                       │
    │ zsh                           │                       │
    └───────────────────────────────┴───────────────────────┘

Notice that if  you use bash or zsh,  the errors will also be  redirected in the
temporary file thanks to the presence of `2>&1` in `'sp'`.

###
### How to prevent 'sp' from redirecting anything?

Set `'sp'` to an empty string.

#### When is it useful to do that?

When  you want  `:make` to  write to  the tempfile  itself, and  you set  `'mp'`
accordingly.

##
## How to change the location of the temporary file created to redirect the output of a shell command?

Configure:

    ┌─────────────┬────────────────────────┐
    │ option      │ affects these commands │
    ├─────────────┼────────────────────────┤
    │ 'makeef'    │ :make                  │
    │             │ :grep                  │
    ├─────────────┼────────────────────────┤
    │ 'errorfile' │ $ vim -q               │
    │             │                        │
    │             │ :cgetexpr (& friends)  │
    └─────────────┴────────────────────────┘

## What's the default value of 'errorfile'?

    errors.err

## What's the value of 'errorfile' if I populate a qfl by parsing the contents of a file?

The path to the latter.

Examples:

    $ grep -RHIins pat /etc | vim -q /dev/stdin
    :echo &ef
    /dev/stdin~

    $ grep -RHIins pat /etc >/tmp/my_error_file ; vim -q /tmp/my_error_file
    :echo &ef
    /tmp/my_error_file~

    $ vim -q <(shell cmd)
    :echo &ef
    /proc/self/fd/123~

    $ vim
    :cd /tmp
    :cfile my_error_file
    :echo &ef
    my_error_file~

##
# Properties of a qf entry
## What are the five properties of a qf entry related to its location?

   - bufnr
   - col
   - vcol
   - lnum
   - pattern

## What are its five other properties?

   - module
   - nr
   - text
   - type
   - valid

## What property of a qf entry can I set, but not get?

    'filename'

You can set it:

    :call setqflist([{'filename': $VIMRUNTIME.'/filetype.vim', 'valid': 1}])
    :cw

But not get it:

    :echo keys(getqflist()[0])
    ['lnum', 'bufnr', 'col', 'pattern', 'valid', 'vcol', 'nr', 'type', 'module', 'text']~
      no 'filename' key~

## What's the only property that a qf entry in Neovim currently misses, compared to Vim?

    'module'

##
## What's the 'module'  property of a qf entry?

The original purpose of the `'module'`  property is to replace the possible long
filepath of an entry with the much-shorter  name of a module, for which there is
an equivalence (i.e. only one filename matches this module name and vice versa).

As a result, the module name is used only for displaying purposes.
The file name is still used when jumping to the file.

> For some languages the file paths can be really long.
> For example in PureScript we often have locations as long as:
>
>     ./src/bower_components/purescript-free/src/Control/Comonad/Cofree.purs
>
> And it might get even longer when it expands to a fullpath.
> This might  be helpful for  other languages where  there is a  clear mapping
> between file system and **module name space** (Haskell, Python, NodeJs, etc).

<https://github.com/vim/vim/pull/1757#issuecomment-325200776>

## What's the 'pattern' property of a qf entry?

It's used to locate the position of the entry in the buffer.

## What's the 'type'    property of a qf entry?

It's a character standing for the type of the error (warning, information, ...).

For more info, read:    `:h errorformat-multi-line`

##
# Properties of a qfl
## What are the nine properties of a qfl?

   - changedtick
   - context

   - id
   - nr
   - idx

   - items    (qfl entries)
   - size
   - title
   - winid    (id of the qf window if opened)


You can ask any of them via:

    :echo getqflist({'key': 0})

Example, to get the size of the current qfl:

    :echo getqflist({'size': 0})

## What are the three pseudo-properties of a qfl that I can ask, but not get?

   - all     (all of the properties of the qfl)
   - efm
   - lines

You can ask for `'all'`:

    :echo getqflist({'all': 0})

But you won't get the key `'all'` in the dictionary output.

## What are the five qfl properties I can ask, but not set?

   - all
   - changedtick
   - idx
   - size
   - winid

## What are the properties that a qfl in Neovim currently misses, compared to Vim?

   - changedtick

TODO: Aren't there other missing properties?
Like `qfbufnr`, `filewinid`, `module`, ...

##
## What's the 'context' property of a qfl?

It allows you to bind an arbitrary data (string, list, dictionary, ...) to a qfl:

Usage example:

    call setqflist([], 'a', {'id': 3, 'context': ['foo', 'bar', 'baz']})

This command binds the list `['foo', 'bar', 'baz']` to the qfl whose identifier is 3.

## What are the 'id' and 'idx' properties of a qfl?

`'id'` is a unique identifier assigned to the qfl.
Contrary to the position of a qfl in the stack (`'nr'`), which can change during
a Vim session, this identifier never changes.

`'idx'` is the position of the current entry in the qfl.

## What's the 'nr' property of a qf entry?   Of a qfl?

For  a  qf entry,  `'nr'`  is  its  error number  that  you  can  look up  in  a
documentation to get more info about the meaning of the error.

For a qfl, `'nr'` is its position in the stack.

##
## What's the main effect of giving the value `0` to a qfl property when using `getqflist()`?

The output  dictionary will  contain the  key matching  this property,  with the
right value for the selected qfl.

##
## If I describe a qfl via the nr `0`, which qfl does Vim select?

If you also describe  it via its `'id'` property, then Vim  selects the qfl with
this id.

Otherwise, it selects the current list.

## If I describe a qfl via the id `0`, which qfl does Vim select?

If you also describe it via its  `'nr'` property, then Vim selects the qfl whose
position in the stack is `'nr'`.

Otherwise, it selects the current list.

## If I describe a qfl via the nr `2` and the id `3`, which qfl does Vim select?

The qfl whose `'id'` is 3.

`'id'` has priority over `'nr'`.

## If I don't describe the qfl via 'id' nor 'nr', which qfl does Vim select?

The current one.

##
## If I set the two properties of a qf entry 'bufnr' and 'filename', how is its location determined?

`'bufnr'` has priority.
`'filename'` is ignored.

## If I set the three properties of a qf entry 'lnum', 'col', 'pattern', how is its location determined?

`'pattern'` has priority over `'lnum'` and `'col'`.

##
## How to refer to a qfl when I use `getqflist()` or `setqflist()`?

Via its `'nr'`  property and its position  in the stack, or  its `'id'` property
and its unique identifier.

If you need to target a qfl according to:

   - its contents, use its id (because it never changes)
   - its position in the stack, use its nr

## How to refer to the last qfl in the stack?

Assign the value `'$'` to its `'nr'` property.

##
## How to get the identifier of the third qfl in the stack?

    :echo getqflist({'nr':3, 'id':0}).id
                                  ^
                                  do NOT give `1`

                                  If you do, you probably won't get any valid info, because
                                  there's no qfl whose id and position in the stack are 1 and 3:

                                      :echo getqflist({'nr':3, 'id':1}).id
                                      {'nr': 0, 'id': 0} ✘~

## How to get the position in the stack of the qfl whose identifier is `3`?

    :echo getqflist({'nr':0, 'id':3}).nr

Here, the purpose of `'nr':0` is not to describe the qfl in which we're interested;
it's to force `getqflist()` to include the `'nr'` key in the output dictionary.

## How to get the entries of the first qfl in the stack?

    :echo getqflist({'nr': 1, 'items': 0})

## How to get the size of the third qfl in the stack?   The size of the stack?

Size of the third qfl:

    :echo getqflist({'nr': 3, 'size': 1}).size

Size of the qf stack:

    :echo getqflist({'nr': '$'}).nr

##
## How to check whether the qfl whose ID is 123 exists?

    if getqflist({'id':123}).id == 123

## Why is it important for a plugin to be able to detect whether the qfl has been modified?

While a plugin is asynchronously updating a  qfl, the user may invoke a quickfix
command, or another plugin could incorrectly update the quickfix list.

If that  happens, the plugin  should be able to  cancel the modification  it was
about to perform on the qfl.

IOW, the plugin needs a way to detect  that the qfl was modified, since the last
time it inspected the qfl.

## How can a plugin detect whether a qfl has been modified since the last time it inspected it?

It can inspect the `'changedtick'` property:

    " populate a qfl
    let last_change = getqflist({'changedtick':0}).changedtick
    ...

    let new_change = getqflist({'changedtick':0})changedtick
    if new_change != last_change
        return
    endif
    ...


Don't use `b:changedtick`;  the latter tracks the number of  times the qf buffer
has been modified. The qf buffer is NOT the qfl (data structure).

##
# Populate a qfl from Vim
## What are the three commands similar to `:grep`?

    :grepadd

    :lgrep
    :lgrepadd

The commands beginning with `l` populate the loclist instead of the qfl.
The ones finishing  with `add` APPEND the matches to  the existing list, instead
of creating a new one.

## What are the pro/con(s) of `:vimgrep` compared to `:grep`?

Con:

It's slower than `:grep` because each searched file is loaded in memory.

Pro:

It can search any Vim regex. Including multi-line patterns, because newlines and
the encoding are automatically recognized.

## What are the three main characteristics defining the commands such as `:cgetexpr`?

This family of commands contains 18 members (2 x 3 x 3).

Their name can be broken down in 3 parts:

    A + B + C
    │   │   │
    │   │   └ end
    │   └ middle
    └ beginning

They can:

    ┌──────────────────────┬─────────┐
    │ populate the qfl     │ A = 'c' │
    ├──────────────────────┼─────────┤
    │ populate the loclist │ A = 'l' │
    └──────────────────────┴─────────┘

    ┌──────────────────────────────────────┬───────────┐
    │ JUMP to the first entry              │ B = ''    │
    ├──────────────────────────────────────┼───────────┤
    │ NOT jump and REPLACE the list        │ B = 'get' │
    ├──────────────────────────────────────┼───────────┤
    │ NOT jump and ADD entries to the list │ B = 'add' │
    └──────────────────────────────────────┴───────────┘

    ┌───────────────────────┬──────────────┐
    │ read a Vim expression │ C = 'expr'   │
    ├───────────────────────┼──────────────┤
    │ read a file           │ C = 'file'   │
    ├───────────────────────┼──────────────┤
    │ read a buffer         │ C = 'buffer' │
    └───────────────────────┴──────────────┘

## What type of argument does each of these commands expect?

It depends on the middle part of its name.

If it's:

    - 'expr'    the command expects an expression
    - 'file'    "                   a file name
    - 'buffer'  "                   a buffer number

##
## What are the seven steps occurring when I execute `:make`?

1. Vim executes the autocmds listening to `QuickFixCmdPre`

2. Vim writes the modified buffers (`&modified` = 1)

3. Vim creates a temporary error file

4. Vim passes to the shell  `'shell'` the program `'mp'` + the optional
arguments passed to `:make`.

The output of `'mp'` is redirected into the error file via `'shellpipe'`.

5. Vim parses the error file via 'efm' to populate the qfl.

       :h error-file-format

6. Vim executes the autocmds listening to `QuickFixCmdPost`

7. Vim removes the error file

## What command is similar to `:make`?

    :lmake

##
## How to look for `pat` in the buffer 1-10?

    :cexpr []
    :sil! noa 1,10bufdo [l]vimgrepadd /pat/gj %
        │ │
        │ └ see # Issues
        │
        └ if the pattern is absent from a buffer, it will raise an error,
          which could prevent `:bufdo` from finishing visiting the next buffers
          inside the range


To search in all the buffers, remove the range in front of `:bufdo`.


Also, our  custom commands `:{C|L}GrepBuffer`  implement this snippet in  a more
complete way.

## How to look for `pat` in ALL (any depth) `.c` and `.h` files of `:pwd`?

    :[l]vim /pat/gj **/*.[ch]
                 ││
                 │└ don't jump to the first entry
                 │
                 └ if there're several occurrences on the same line, get all of them

## How to look for `pat` in the subdirectories ending with `.d/` inside `/etc/apt`?

                           ┌ no need to escape the dot;
                           │ in a FILE pattern:
                           │
                           │     - dot is not interpreted as a meta character
                           │     - `?` matches any single character
                           │
    :[l]vim /pat/gj /etc/**.d


`:[l]vim` expects file names, not directory names.
And yet, here, `/etc/**.d` matches directories, not files.
This probably  shows that, when necessary,  Vim automatically appends `/*`  to a
pattern:

    :[l]vim /pat/gj /etc/**.d

                ⇔

    :[l]vim /pat/gj /etc/**.d/*
                             ^^

## How to look for `pat` in all the files of `:pwd`, changed in the last hour?

                    ┌ backtick expansion:
                    │ expanded into the output of `$ find ...`
                    ├────────────────────────┐
    :[l]vim /pat/gj `find . -type f -cmin -60`
                          │
                          └ matches the output of `:pwd`, NOT `$PWD`

Whenever you  want to look  for a pattern  in a set of  files which can  only be
defined by a shell command, use a backtick expansion.


About `$ find`:

There are six options similar to `-cmin`.

    -amin
    -atime
    -mmin
    -mtime
    -cmin
    -ctime

The `a`, `m` and `c` prefixes stand for “access”, “modification”, and “change”.

A file is:

- accessed as soon as the user or a process opens it
- modified as soon as its contents are altered
- changed  as soon as its contents or its file attributes are altered

When an option ends with the suffix:

    - min     the following number is interpreted as a duration in minutes
    - time    the "                                                days

##
## How to parse all the lines containing `pat` in the current buffer to populate the qfl?

    :cexpr []


     ┌ see # Issues
     │
    :noa g/pat/.caddbuffer


It should work if the lines can be parsed by at least one format in `'efm'`.

But if they don't, you'll need to transform them so that they can be parsed.
For example, assuming your lines look like this:

    /path/to/some/file@line number@message

And you want them to be parsable by the format `'%f:%l:%m'`, you could try:

    :noa g/pat/caddexpr substitute(getline('.'), '@', ':', 'g')

## How to parse the output of a shell command and get a qfl, without modifying the qf stack?

    echo getqflist({ 'lines': systemlist('# shell cmd'),
    \                'efm':   '{format}'})


When  you pass  the optional  dictionary `{'lines':  ...}` to  `getqflist()`, it
returns a dictionary with a single `'items'` key.
The value associated to this key is a list of sub-dictionaries.

Each of them contains some information about an entry in the qfl:

    - line
    - column
    - text
    - ...

For Vim to  parse the output of  the shell command, it needs  to create unlisted
buffers to read the files where there's at least one entry.
Therefore, every entry in the qfl has a `'bufnr'` key.

In  addition to  `'lines'`, you  may include  an `'efm'`  key in  the dictionary
passed to `getqflist()`, to let Vim know how to parse the output.
Without the `'efm'` key, Vim will use the `'efm'` option.

##
## How to populate the qfl with a grep-like shell command different than `&grepprg`?

    :cgetexpr system('grep-like cmd')

## How to populate a valid qfl with `$ find /etc -name '*conf'` without altering the 'efm' option?

        let qfl = getqflist({'lines': systemlist('find /etc/ -name "*.conf"'),
            \                'efm':   '%f'})
        call setqflist(get(qfl, 'items', []))
        cw

## How to populate a qfl with a location which has never been visited (i.e. absent from all buffers)?

Use the `'filename'` property:

        :call system('touch /tmp/new_file')
        :call setqflist([{'filename': '/tmp/new_file', 'valid': 1}])
        :cw

        :call system('trash-put /tmp/new_file')

## How to populate the qfl whose id is `123` with the output of a shell command?   (in one line)

        call setqflist([], 'r', {'id':123, 'lines': systemlist('your shell cmd')})

##
## I have a long-to-type set of files. How to effectively and CONSECUTIVELY look for different patterns in it?

Populate the arglist with the set of files (`:args`).
Then, use the special characters `##` to refer to it:

        :vim /pat1/gj ##
        :vim /pat2/gj ##
        ...

`##`  allows  you  to abstract  a  complex  set  of  files, and  focus  on  what
varies/matters:    the pattern.

## What rarely-mentioned commands are necessary to look for several patterns SIMULTANEOUSLY in a codebase?

`:colder` and `:cnewer`.


For example, suppose you want to refactor `FuncA()`.
You  begin by  populating the  qfl  with all  the locations  where `FuncA()`  is
defined/called:

        :vim /FuncA/gj *.c

But before changing the implementation, you want to rename `FuncA()`:

        :cdo s/FuncA/NewNameA/e | update

In the process,  you've noticed that `FuncA()` called `FuncB()`,  whose name was
derived from `FuncA`.
It has become irrelevant, so now you also need to rename `FuncB()`:

        :vim /FuncB/gj *.c
        :cdo s/FuncB/NewNameB/e | update

The process repeats itself.

After having  renamed every function,  you can go back  to the original  qfl via
`:colder [count]`.
And at any  moment, in case of an  error, you could have moved in  the stack via
`:colder` and `:cnewer`.


The qf stack allows you to bind to each pattern a separate qfl.

##
## How to create a new qfl at the end of the stack?

        call setqflist([], ' ', {'nr' : '$', 'lines' : systemlist('grep -RHIins pat *')})

## What `$ grep` command should I execute to get an output that 'efm' can parse?

                   ┌ ignore case
                   │┌ print the number of the lines
                   ││
                   ││┌ suppress error messages about nonexistent or unreadable files
                   │││
        $ grep -RHIins pat *
                │││
                ││└ ignore binary files
                │└ print file names
                └ recursively (enter subdirectories)


The `-n` option  is necessary for Vim to  parse the output of `$  grep`, via the
format `'%f:%l:%m'` in the default value of `'efm'`.

Otherwise, Vim will populate the qfl only with invalid entries.

---

If there're several matches on a single line, you'll get only one entry.
If you want as many entries matches, you need to also include the `-o` option.
However, doing so makes you lose context; you don't get the entire line, but just the match.

Solution: Use ripgrep instead.
When  you pass  the  option `--vimgrep`  to  `$ rg`,  you get  each  match on  a
dedicated line, *with* its context.

    $ rg --vimgrep -i -L pat file ...

TODO: Should we replace all our `$ grep` commands with `$ rg` equivalent?

---

For a permanent usage, you can configure `'grepprg'` like this:

        set grepprg=grep\ -RHIins\ $*

##
# Populate a qfl from the shell
## How to parse the output of the last shell command during Vim startup?

        $ vim -q <(!!)

Don't use this:

        $ !! | vim --not-a-term -q /dev/stdin

It works, but it may leave the terminal in an unexpected state:
on my machine, after using this command,  I can't close the terminal with `C-d`;
I need to execute `$ exit`.

## How to look for all the lines matching `pat` in $PWD, and send them to a running Vim server?

                              ┌ don't use the options `-RHIins`;
                              │ you don't know which program is started by `:grep`;
                              │ the options should be passed when setting 'grepprg'
                              │
    $ vim --remote-send ':grep pat *<cr><cr>' --servername {name of the vim server}
                                         │
                                         └ bypass “press Enter” prompt

Or:

    $ nv -q 'grep -RHIins pat *'
      │
      └ custom shell function

##
# Limit the population of a qfl
## How to empty the qfl? (via a command and via a function)

This command CREATES a new empty qfl in the stack:

        :cexpr []


These commands REPLACE the current qfl with an empty list:

        :call setqflist([], 'r')
        :call setloclist(0, [], 'r')

## How to make `:cgetbuffer` read only the lines 12 to 34 of the buffer 56?

Any command whose final part of the name is `buffer` accepts a range.
So, you can execute:

        :12,34cgetbuffer 56

## How to stop `:vimgrep` from populating the qfl after having found 123 matches in a file?

        :123vim pat file

This syntax  is particularly  useful to  check whether a  file contains  a given
pattern, without looking for all the matches:

        :1vim pat file

##
# Open the qf window
## How to open the qf window with a height of 15 lines?

        :copen 15
        :cwindow 15

## Does `:[l]vim` open the qf window?

No.

But, it emits `QuickFixCmdPost`.
So,  you can  install  an autocmd  listening  to  this event,  and  Vim will  to
automatically open the qf window after a `:vim` command.

## What commands are DIRECTLY responsible for the opening of the qf window?

        :copen
        :cwindow

If the qf  window is opened on  your system after a `:vim`  or `:helpg` command,
it's only because of an autocmd/plugin.

## In which state (open/closed) is the qf window after `:copen`?   After `:cwindow`?

After `:copen`, the qf window is open, no matter what.

After `:cwindow`,  the qf window  is open IFF the  qfl contains at  least one
entry whose `'valid'` key has the value 1.

## When does `QuickFixCmdPost` occur?

After a command (!= function) populating the qfl or loclist is executed.
Whether it finds something doesn't matter.

`FileType qf` is fired afterwards.

## Do `setqflist()` and `setloclist()` fire `QuickFixCmdPost`?   Why?

No.

Theory:

These are functions, not commands.

Functions are low-level tools for plugins developers (or advanced users).
As  such, they  must do  one thing  and  one thing  only, to  let the  developer
implement the exact behavior they want.

OTOH, built-in commands  (`:make`, `:grep`, ...) are for users,  who most of the
time want the qf window to be  opened automatically. To do so, they need to have
an event to listen to, and install an autocmd.

IOW, if  `:make` didn't fire  `QuickFixCmdPost`, the user  would have no  way to
make it open the qf window  automatically, aside from creating a custom wrapper,
and an abbreviation (`:make` → `:Make`).

## Do `setqflist()` and `setloclist()` open the qf window?   Do they focus the qf window?

No and no.

However, assuming  you have  a custom  autocmd which handles  how the  qf window
should be opened, you can rely on the latter via `:doautocmd`:

        " autocmd opening the qf window
        au QuickFixCmdPost  *  ...
                               │
                               └ custom command/function invoking:

                                         :c{window|open} [height]

                                 it can get the name of the command populating the qfl via:

                                         expand('<amatch>')


        " populate the qfl by invoking `setqflist()`
        call setqflist(...)
                       │
                       └ for a simple test, use:    [ {'valid': 1} ]


        " rely on the previous autocmd to handle how the qf window should be opened
        do <nomodeline> QuickFixCmdPost grep
                                        │
                                        └ if your autocmd reacts differently
                                          depending on whether the qf window displays a location list,
                                          or depending on the name of the command which populated the qfl,
                                          choose the name wisely

## How to automate the execution of a command after a command populating the qfl (!= loclist) has been executed?

                            ┌ all the commands populating a loclist begin with an `l`
                            │ so all the ones populating a qfl begin with `[^l]`
                         ┌──┤
        QuickFixCmdPost  [^l]*  Your_command
                             │
                             └ a star is not equivalent to the quantifier `*` in a file pattern
                               it's equivalent to the regex `.*`

                               IOW:

                                    [^l]*         ⇔  [^l].*
                                    file pattern     regex

You can't use `c*` because some commands populating the qfl don't begin with `c`:

        - make
        - vimgrep[add]
        - grep[add]

##
# Navigate in a qfl
## How to display the qf stack?

        :chi

The current one is prefixed with a `>`.

## How to navigate in the qf stack?

        :colder
        :cnewer

## How to jump back to the current entry in the loclist?

        :cc
        :ll

Useful after navigating in the file or other files.

## How to jump to the entry 123?

        :cc 123
        :ll 123

## What are the other six motions you can perform in a qfl?   How to perform them?

    ┌─────────────────────────────────┬────────────────┬────────────────┐
    │             purpose             │   Ex command   │ normal command │
    ├─────────────────────────────────┼────────────────┼────────────────┤
    │ previous entry                  │ cprevious      │ [q             │
    │                                 │ lprevious      │ [l             │
    ├─────────────────────────────────┼────────────────┼────────────────┤
    │ next entry                      │ cnext          │ ]q             │
    │                                 │ lnext          │ ]l             │
    ├─────────────────────────────────┼────────────────┼────────────────┤
    │ first entry                     │ cfirst         │ [Q             │
    │                                 │ lfirst         │ [L             │
    ├─────────────────────────────────┼────────────────┼────────────────┤
    │ last entry                      │ clast          │ ]Q             │
    │                                 │ llast          │ ]L             │
    ├─────────────────────────────────┼────────────────┼────────────────┤
    │ last entry in the previous file │ cpfile         │ [ C-q          │
    │                                 │ lpfile         │ [ C-l          │
    ├─────────────────────────────────┼────────────────┼────────────────┤
    │ first entry in the next file    │ cnfile         │ ] C-q          │
    │                                 │ lnfile         │ ] C-l          │
    └─────────────────────────────────┴────────────────┴────────────────┘

## What are the two motions you can perform in the qf stack?   How to perform them?

    ┌──────────┬────────────┬────────────────┐
    │ purpose  │ Ex command │ normal command │
    ├──────────┼────────────┼────────────────┤
    │ previous │ colder     │ <q             │
    │          │ lolder     │ <l             │
    ├──────────┼────────────┼────────────────┤
    │ next     │ cnewer     │ >q             │
    │          │ lnewer     │ >l             │
    └──────────┴────────────┴────────────────┘

## How to prevent Vim from jumping to the first entry, when I execute a command to populate the qfl?

It depends on the command you use.

----------

If the name of the command follows this scheme:

        :{c|l}[add|get]{buffer|expr|file}

Use `get` or `add` in the middle of the name of the command.

Example:

        :cgetfile
          ^^^

----------

If the command is `:[l]vimgrep[add]`, use the `j` flag.

Example:

        :vim /pat/gj files
                   ^

----------

If the command is `:[l]grep[add]` or `:[l]make`, use a bang.

Example:

        :make!
             ^

##
# Operate on the entries of a qfl
## What are the four actions I can pass to `setqflist()` in its second argument?

    ┌────────┬─────────────────────────────┐
    │ 'a'    │ append the items to the qfl │
    ├────────┼─────────────────────────────┤
    │ 'f'    │ free the qf stack           │
    ├────────┼─────────────────────────────┤
    │ 'r'    │ replace the qfl             │
    ├────────┼─────────────────────────────┤
    │ ' '/'' │ create a new qfl            │
    └────────┴─────────────────────────────┘

## How to modify the qfl (data structure) by directly editing the qf buffer?

You can't ONLY edit the qf buffer and be done with it.

There would be a discrepancy between the qf buffer and the qfl.
As a result, clicking on an entry may have an unexpected result.

You  need to  also execute  `:cgetbuffer`, AND  have a  properly set  `'efm'` by
adding something like this in `~/.vim/after/ftplugin/qf.vim`:

        let &l:efm = '%f%*\s\|%l col %c%*\s\|%m'


From there, here's the procedure you need to follow:

        - make the qf buffer temporarily modifiable

        - edit the buffer

        - update the qfl using `:cgetbuffer`

        - make the qf buffer unmodifiable, and unmodified

Relevant help section:

        :h ^w_<cr>

## How to replace all occurrences of a pattern in all the files of the qfl?

                          ┌ avoid E486
                          │
        :cfdo %s/pat/rep/ge | update
                            └──────┤
                                   └ avoid E37 and E89 if 'hidden' is reset

## How to delete all the lines containing an entry in the qfl, except the first ten?

        :11,$cdo d_ | update

## How to yank the first entry of:   the file 1 in the qfl + ... +  the file 10 in the qfl?

        qaq
        :1,10cfdo y A

This will yank in the register `a`, the line of the first entry in:

        - the first  file of the qfl
        - the second file of the qfl
        ...
        - the tenth  file in the qfl

This works because  `:cfdo` moves the cursor on  the first entry
of each file in the qfl.

## I want to repeat a command for each entry in the qfl. How to make it more reliable?

If you execute a command which modifies the buffer, update it afterwards:

        " ✘
        :sil! noa cdo d_

        " ✔
        :sil! noa cdo d_ | update
                         ^^^^^^^^

---

If you execute a substitution command, use the `e` flag:

        " ✘
        :noa cdo s/pat/rep/ | update

        " ✔
        :noa cdo s/pat/rep/e | update
                           ^

---

If you  execute a command  which MAY change the  focused window, prefix  it with
`:noautocmd`:

        " ✘
        :sil!     bufdo vimgrepadd /pat/gj %

        " ✔
        :sil! noa bufdo vimgrepadd /pat/gj %
              ^^^

---

If you  execute `:{arg|buf|c|cf|l|lf|tab|win}do`, and you  suspect the following
command may raise an error, prefix the whole command with `silent!`:

        " ✘
        :     noa argdo %caddbuffer

        " ✔
        :sil! noa argdo %caddbuffer
         ^^^^

## How does `:cdo` interpret a range?   What about `:cfdo`?   `:cgetbuffer`?  `:bufdo`?

    ┌─────────────┬─────────────────────────────────────────────┐
    │ :cdo        │ positions of the ENTRIES in the qfl         │
    ├─────────────┼─────────────────────────────────────────────┤
    │ :cfdo       │ positions of the FILES in the qfl           │
    ├─────────────┼─────────────────────────────────────────────┤
    │ :cgetbuffer │ addresses of the LINES in the buffer        │
    ├─────────────┼─────────────────────────────────────────────┤
    │ :bufdo      │ positions of the BUFFERS in the buffer list │
    └─────────────┴─────────────────────────────────────────────┘

## How to shorten the filepath displayed in the qf window to the filename?

Use the `'module'` and `'items'` key:

        call setqflist([],
        \              'r',
        \              {'items': map(getqflist(),
        \                            {i,v -> extend(v, {'module': fnamemodify(bufname(v.bufnr), ':t')})})})

`'module'` allows you to change the text displayed in the filename column.

`'items'` allows you to update the items in the qfl without affecting its title,
in a single invocation of `setqflist()`.
Without `'items'`, you would need two:

        let new_qfl = map(getqflist(), {i,v -> extend(v, {'module': fnamemodify(bufname(v.bufnr), ':t')})
        call setqflist(new_qfl, 'r')
        call setqflist([], 'a', {'title': get(getqflist({'title': 0}), 'title', ':setqflist()')})

Because:

        - `call setqflist(list, 'r')` replaces the items in the qfl, but ALSO
          its title

        - `setqflist()` ignores  the first  argument, when  you provide  the
          third optional one; so you can't replace both the items and the title
          of a qfl at the same time, with:

                call setqflist([...], 'r', {'title': '...'})

##
# Miscellaneous
## When executing `$ ag ...`, how to get ALL matches on any given line?   What about `$ grep ...`?

Pass the `--vimgrep` option to `$ ag`.

Pass the `-o` option to `$ grep`.


`-o` (--only-matching) makes `$ grep` print only the matched parts of a matching
line, with each such part on a separate output line.

However, we lose  the context: we don't  see the rest of the  line anymore, only
the matched part.

## Why is the output of the compiler displayed on the screen when I compile a file?

Because of the default value given to `'shellpipe'` on linux:

        &shellpipe = '2>&1| tee'
                            │
                            └ `$ tee` redirects its input to a file AND to the terminal

This also affects `:grep`.

## When I use `:lh` or `:helpg`, is the search  case-sensitive or -insensitive?

Sensitive, no matter how `'ignorecase'` is set.

If you want it to be insensitive, add the atom `\c`:

        :lh \cfoo.\{,12}bar
            ^^

In this example, we search for `foo` + 0 up to 12 characters + `bar` in the help
files.

## How to set the title of a qfl?

If a window displaying the qfl is opened, and it's currently focused:

        let w:quickfix_title = 'your title'

Otherwise:

        call setqflist(    [], 'a', {'title': 'your title'})
        call setloclist(0, [], 'a', {'title': 'your title'})

The second solution is more reliable:

        - you don't need to be in the qf window
        - it persists even after closing and re-opening the qf window

## How to get all the info about all the opened qf windows in the current Vim session?

For the qf windows:

        :echo filter(getwininfo(), {i,v -> v.quickfix && !v.loclist})

For the location windows:

        :echo filter(getwininfo(), {i,v -> v.quickfix &&  v.loclist})

## How to programmatically detect whether Vim was started with the `-q` argument?

If Vim was started with `-q`, `'ef'` will contain the path to the file which was
parsed to populate the qfl, instead of the default value `errors.err`.

        if &ef is# 'errors.err'
            " Vim was started WITHOUT `-q`
        else
            " Vim was started WITH `-q`
        endif

##
## Why is the output of `getqflist()` not reliable to be saved, then used later to restore the qfl?

If you wipe the buffer before restoring the qfl, it will raise an error.

        $ echo 'pat' >/tmp/file

        :vim /pat/j /tmp/file
        :let qfl = getqflist()
        :bw /tmp/file

        :call setqflist(qfl)
        E92: Buffer 123 not found~

## How to reliably save then later restore the qfl?

For each entry, add the `'filename'` key, and then remove the `'bufnr'` key:

        let qfl = map(getqflist(),
        \             {i,v -> extend(v,
        \                           {'filename': fnamemodify(bufname(remove(v, 'bufnr')), ':p')})})

##
# Issues
## Why does  `:helpg \~$`  fail?

From `:h :helpg`:

> The pattern does not support line breaks, it must match within one line.

---

Although, for some reason, replacing `$` with `\n` fixes the issue:

        " ✔
        :helpg \~\n

But the pattern breaks the command again if you add something after the newline:

        " ✘
        :helpg \~\n\_.

## Why does  `$ vim -q $(cmd)`  fail?

`-q` expects a file name containing valid errors.
Not directly the errors themselves.

## Why does  `:vim /pat/gj /etc/apt/**/`  fail?

Usually, Vim would complete such a file pattern by adding `/*` at the end:

        :vim /pat/gj /etc/apt/**

                    ⇔

        :vim /pat/gj /etc/apt/**/*

Not here, because of the ending slash.

Maybe  an  ending slash  indicates  to  Vim that  you're  really  looking for  a
directory, not files.

## Why does  `:vim /pat/gj /etc/*.conf | cdo s//rep/e`  fail?

The pattern  used in  a `:[l]vimgrep[add]`  command is NOT  saved in  the search
register.

So, you need to write the pattern explicitly in the substitution:

        :vim /pat/gj /etc/*.conf | cdo s/pat/rep/e | update
                                         ^^^
## Why does  `:bufdo grepadd pat %`  sometimes fail?

`:grepadd` jumps to the first error, which is forbidden by `:bufdo`.

Add a bang after `:grepadd`.

        :bufdo grepadd! pat %
                      ^

Also, you should probably use `:silent!` so that `:bufdo` processes all buffers,
even if an error occurs in one of them.

## Why does  `:cgetexpr system('cmd1 | cmd2')`  fail?

You need to escape the bar.

Otherwise, it will be parsed as a separation between two Vim commands:

        :cgetexpr system('grep -RHIins pat * \| grep -v garbage')
                                             │
                                             └ the bar needs to be escaped

---

This shouldn't happen because the bar is inside a string.
Besides, it's inconsistent with other similar commands:

        :echo system('grep -RHIins pat * | grep -v garbage')

        :echo expand('`... | ...`')

        :e `=system('grep -RHIins pat * | tail -1 | cut -d: -f1')`

---

Note that the issue disappears if `:cexpr` doesn't see the bar directly.
It  happens, for  example, if  the output  of `system()`  is first  stored in  a
variable:

                                              no need of escaping the bar
        " ✔                                   v
        :let var = system('grep -RHIins pat * | grep -v garbage')
        :cexpr var

## Why do commands populating the qfl progressively (:vimgrepadd, :caddexpr, ...) sometimes fail?

If you have an autocmd opening the qf window, it could interfere in the process.

The solution is to prefix your qf commands with the `:noautocmd` modifier.


Example 1:

        " ✘
        " This will open a new split for every buffer.

        :sil!     bufdo vimgrepadd /pat/gj %

        " ✔

        :sil! noa bufdo vimgrepadd /pat/gj %
              ^^^


Example 2:

        " ✘
        " This will probably capture only the first line where `pat` matches,
        " because when the qf window is opened, the focus is changed.

        :    g/pat/caddexpr substitute(getline('.'), '@', ':', 'g')

        " ✔

        :noa g/pat/caddexpr substitute(getline('.'), '@', ':', 'g')
         ^^^

##
##
#
# TODO
## ?

Sometimes, we have stray characters when  we run a custom command populating the
qf window (like `:CGrep`).
It's a hard-to-debug issue, because it seems influenced by many factors.
I suspect it has nothing to do with `system()`, nor with `:cexpr`.
I  can reproduce  it with  a simple  `:copen`, when  the qf  window takes  a few
seconds to open.

Find a fix.

## ?

Document the `qfbufnr` property.

## ?

Document that  the result of `:vimgrep`  is influenced by `'isk'`  (and probably
`'isf'`, `'isi'`, ...), if the pattern contains sth like `\k` or `\<`, `\>`.
Indeed, if  `:vimgrep` searches  inside a  file which is  currently loaded  in a
buffer, it uses the buffer-local value of `'isk'`.

    :sp /tmp/file
    :call append('.', ['foo', 'bar', 'foo#bar'])
    :vim /\<bar/gj %
    /tmp/file  |3 col 1  | bar~
    /tmp/file  |4 col 5  | foo#bar~

    :setl isk+=#
    :vim /\<bar/gj %
    /tmp/file  |3 col 1  | bar~

The previous command shows that `:vim` is influenced by the local value of `'isk'`.

    :bd
    :vim /\<bar/gj /tmp/file
    /tmp/file  |3 col 1  | bar~
    /tmp/file  |4 col 5  | foo#bar~

But *not* if the buffer where the search is performed is unloaded.

## ?

Install a `!j` mapping which would open an interactive window, in which we could
see all the running jobs, and stop them.

## ?

Try to remove `get()` whenever you can.
You've used it too much in the past to access the value of a qfl property.

Search for `\C\<get(` in this file and in all our notes/plugins/...

You  may find  a lot  of matches,  but don't  worry (`:Cfilter!  -other_plugins`)
removes a lot of them.

## ?

We've  made  a   fundamental  mistake  in  the  past,  every   time  we've  used
`setqflist()` or `setloclist()`.

MWE:

    :CFreeStack
    :exe 'helpg vim' | exe 'helpg fast' | exe 'helpg unix' | exe 'helpg text' | exe 'helpg editor'
    :col 3
    :chi
    :call setqflist([], ' ')
    :chi

When you invoke `setqflist()`, all the qfl after the current one are removed.
That's why `vim-asyncmake` sets the `nr` property to `$`:

    call setqflist([], ' ', {'nr': '$',
    ...

---

The same issue exists whenever we've executed `:make`, `:grep`, `:vimgrep`, ...

Before executing any of  those commands, you should make sure  you're at the top
of the stack:

    :let stack_size = getqflist({'nr': '$'}).nr
    :let current_qfl = getqflist({'nr': 0}).nr
    :exe (stack_size - current_qfl).'cnewer'

Maybe you should  use a library function (`lg#...()`), which  would take care of
all those kind of details, and would  set the qfl without altering the stack too
much.

    :Vim :[cl]\%(add\|get\)\=\%(expr\|file\|buffer\)\|l\=make\|l\=vim\%[grep]\%(add\)\=\>.*/[^/]*/[gj]\{1,2}:gj ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/** ~/.vim/vimrc
    :Cfilter! -tmp -commented -other_plugins

## Document that you can set the current entry in the qfl via `setqflist()` and the 'idx' property.

<https://github.com/vim/vim/pull/3701>

## Talk about the 'filewinid' property of a location window.

See `:h getloclist()`.
See also one of our TO DO in:

        ~/.vim/plugged/vim-lg-lib/autoload/lg/window.vim

'filewinid' can  help simplify the  code which  is responsible for  focusing the
window associated to the current location window when we press `z[`.

## If I remove `tee`  from 'sp', the output of the shell  command is still echoed...
to the screen, when I execute `:grep! pat /etc`. Why?

Update:
Because we haven't redirected the errors to the temp file:

        set sp=>%s\ 2>&1

However, we still have the hit-enter prompt.
You can't avoid its printing. But you can avoid to have to press Enter,
with `:sil`.

## How to remove errors from `:grep`?

It was necessary in the past, because we used `:grep`.
But now we use `:cgetexpr`, for which this code doesn't work:
we use `filter()` instead.
(update: now we use `2>/dev/null`; see `s:op_grep_get_qfl()` in myfuncs.vim)


By default, the output of `:grep` includes errors (“permission denied“).
It's because of 'shellpipe' / 'sp', whose default value is `2>&1| tee`.

When we're looking for a pattern in files, these errors are noise: remove them.
We do so by temporarily tweaking 'sp':

        2>&1| tee  →  |tee

let &l:sp = '| tee'

## How to make `:grep` ignore errors encountered when the shell command has been unable to open a file?

Temporarily remove `2>&1` from `'sp'`.

        let &sp = '| tee'
        :grep ...
        let &sp = '2>&1| tee'



Could we integrate `2>/dev/null` somewhere else?

Update:
Nope, it seems we can't:

        grep! foobar /etc 2>/dev/null

Why does it not work?

Update:
Probably because of a subshell created by Vim.
Try this:

        set sp=>
        grep! foobar /etc 2>/dev/null

## Why does `sil grep! pat . | redraw!` make the screen “flash” (even if we remove `tee` from 'sp')?

## How to open the qf window from a script, using an autocmd installed elsewhere?

        do <nomodeline> QuickFixCmdPost copen
        do <nomodeline> QuickFixCmdPost lopen
        do <nomodeline> QuickFixCmdPost cwindow
        do <nomodeline> QuickFixCmdPost lwindow

The last command is wrong; `:copen` is not a valid command to populate a qfl.
However, it doesn't matter.
We can use it to communicate some info to the autocmd opening the qf window:

        - do we  want to open the  window unconditionally, or on  the condition
          it contains at least one valid error?

        - do we want to open the qf window or the location window?

Document somewhere  the fact that  the pattern used  in a `:do`  command doesn't
have to be valid. It can be (ab)used to pass arbitrary info.

---

Also, we've used copen/cwindow/lopen/lwindow, inconsistently in our code.
Clean this mess:

        noa vim /do\%[autocmd]\s*\%(<nomodeline>\)\=\s*QuickFixCmdPost/gj ~/.vim/**/*.vim ~/.vim/**/vim.snippets ~/.vim/vimrc | cw

Note that if you use `[c|l]window`, sometimes you'll need to add this after:

        if &bt isnot# 'quickfix'
            return
        endif

To avoid, for example, adding conceal outside a qf buffer.

##
## Why does Vim sometimes mix absolute and relative filepaths for files in the same directory?

MWE:

        /tmp/test/foo
        ├── /tmp/test/foo/file1
        ├── /tmp/test/foo/file2
        └── /tmp/test/foo/file3

        $ cd /tmp/test
        $ vim -Nu NONE foo/file1

        :vim /^/gj ./** | cw

            foo/file1    |1 col 1  |
            ./foo/file2  |1 col 1  |
            ./foo/file3  |1 col 1  |


If the  buffer where an  entry is  located was already  loaded prior to  the qfl
being populated, Vim will use a relative filepath.
Otherwise, if the buffer didn't exist or  was unloaded, Vim will use an absolute
(albeit reduced; i.e. cwd → `.`) filepath.

For more info:

        https://vi.stackexchange.com/a/4816/17270
        https://github.com/vim/vim/issues/2846

## Why does Vim sometimes jump to a wrong location when I press Enter on an entry in the qf window?

MWE:

        " disable `vim-cwd`
        :cd ~/.vim/plugged/vim-completion/
        :sil CFreeStack | noa vim /timer_start/gj ~/.vim/**/*.vim | cw
        SPC R
        :cd ~/wiki/
        z(
        ]q
        " Keep pressing `]q` until you find entries whose path is relative, like:
        ""
        "         autoload/completion/custom.vim ...
        "         autoload/completion/spel.vim   ...
        ""
        " You'll end up in a buffer not associated with any file.

Simplify this MWE, so that it doesn't refer to any custom configuration.

## When does Vim expand relative filepaths?

## When does Vim jump to wrong location?

## What's the difference between `:CGrep`, `:PQ`, `|g`?

Also, maybe we should integrate `:CGrepBuffer` into a cycle `C-g .`.
Remove `:PA` and `:PQ` once you've finished studying all these commands.

## Why does `:4verbose cexpr system('')` corrupts the display?

The statusline position moves when we move the cursor.

Update:
It's probably  one of those circumstances  where the display becomes  messed up.
See this:

        :lh \<mess\%[ed]\>

Make a summary of those circumstances, and document it.

Update:

To reproduce the issue, you need to do that:

    $ vim -Nu NONE +'set laststatus=2' +'helpg vim'
    :q
    :4verb cexpr system('')
    " insert some text, and watch the status line

## What's the purpose of 'items'?

It seems we could without it (:h setqflist-examples):

        :echo getqflist({'id' : qfid, 'items' : 0}).items
        ⇔
        ??? (no equivalent here)

        I think we couldn't extract the items of a non-current qfl without 'items'.
        Also, I think 'items' allows you to replace the items in a qfl without affecting
        its title.



        :let newItems = [{'filename' : 'a.txt', 'lnum' : 10, 'text' : "Apple"},
                        \ {'filename' : 'b.txt', 'lnum' : 20, 'text' : "Orange"}]
        :call setqflist([], 'a', {'id' : qfid, 'items' : newItems})
        ⇔
        :let newItems = [{'filename' : 'a.txt', 'lnum' : 10, 'text' : "Apple"},
                        \ {'filename' : 'b.txt', 'lnum' : 20, 'text' : "Orange"}]
        :call setqflist(newitems, 'a', {'id' : qfid})


        :call setloclist(3, [], 'r', {'items' : newItems})
        ⇔
        :call setloclist(3, newItems, 'r')

## How to get rid of the qfl `:hub push` produced by fugitive?

Idea:

Remap `Up` so that after executing `:Gpush`, it checks the contents of the qfl.
And, if the latter doesn't contain any  important message, try to remove it, and
get back to the previous one.

Issue:
You'll need to find an event fired by `:Gpush`, but I can't find one.

