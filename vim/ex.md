# What's the difference between `-e` and `-E` in a non-interactive command in
## Vim?

None.

They both start Vim in Ex mode.

---

The only difference between them is in an interactive command.
In the latter,  `-E` start an "improved"  Ex mode in which  command line editing
and completion are available.

In a usual Vim  session, by default, you can access the Ex  mode started by `-e`
and `-E` by pressing resp. `Q` and `gQ`.

## Nvim?

stdin is read as:

   - Ex commands with `-e`
   - text (into buffer 1) with `-E`

---

This is what is documented at `:h -e`; but it's not entirely true:

    # `cmd` is not run
    $ echo cmd | nvim -e

    # `cmd` should be run as an Ex command; instead it's used as text
    $ echo cmd | nvim - -e

Although, those  exceptions are not  important to remember, because  in practice
you'll never use `-e`, nor `-E`, without `-s`.

---

There's no difference between `-e` and `-E` in an interactive command.
Both start Nvim in an "improved" Ex mode.

##
# silent/batch mode
## What characterizes this mode?  (4)

The TUI is not drawn.

---

Most initializations are skipped.

---

Most prompts, warnings, informative/error messages  are switched off (unless you
increase the verbosity level to a non-zero value).

---

The output of these commands is printed to stdout:

   - `:print`
   - `:list`
   - `:number`
   - `:set`

This is especially  useful in a pipeline,  to send the output of  Vim to another
shell command for further processing:

                                                               v
    $ echo 'a\nb\nc' | vim --not-a-term +'2d' +'%p' +'qa!' - -es | tr '[ac]' '[AC]'
    A~
    C~

Here, without `-s`, the output would be empty.
This is because Vim would write directly  to the terminal, to draw the output in
its own window; it  would not write the output on its  stdout which is connected
to the shell pipe.

## When is it useful?

When you need to edit some text non-interactively.
That is, when you want to execute Ex  commands from a file or a pipe, instead of
the keyboard.

##
## I have a long series of Ex commands I want to regularly run on some file(s).
### What's the most readable and re-usable way to apply them?

Write your Ex commands in a `filter` file, then run:

    $ vim -es <filter file
              │
              └ redirect to stdin

---

Example:

    $ cat <<'EOF' >/tmp/file
    heXXY
    wYrXd
    EOF

    $ cat <<'EOF' >/tmp/filter
    %s/X/l/g
    %s/Y/o/g
    x
    EOF

    $ vim -es </tmp/filter /tmp/file && \
      cat /tmp/file
    hello~
    world~

##
## How to make Vim print the messages output by Ex commands in this mode?

Increase Vim's verbosity:

    $ vim +'set vbs=1' -es

---

It's better to set `'verbose'` via `:set`:

            vvvvvvvvv
    $ echo 'set vbs=1|2d' | vim -es =(printf 'one\ntwo\nthree\nfour\nfive')
    three~

than via `-V1` which produces much more noise:

                    vvv
    $ echo 2d | vim -V1 -es =(printf 'one\ntwo\nthree\nfour\nfive')
    XSMP opening connection~
    not found in 'packpath': "pack/*/start/*"~
    GetLatestVimScripts is not vi-compatible; not loaded (you need to set nocp)~
    not found in 'packpath': "pack/*/start/*"~
    Opening the X display took 0 msec~
    Opening the X display took 1 msec~
    "/tmp/zshgrd5so"~
    "/tmp/zshgrd5so" [Incomplete last line] 5 lines, 23 characters~
    Entering Ex mode.  Type "visual" to go to Normal mode.~
    :~
    XSMP handling save-yourself request2d~
    three~
    :% ~

### I can't redirect these messages to another shell command!

They are printed  on stderr, even the ones  not due to errors; so  use `2>&1` to
also redirect stderr:

    ✘
    $ vim +'set vbs=1|echo "test"|qa!' -es | wc -m
    test0~

                                           ✔
                                           vvvv
    $ vim +'set vbs=1|echo "test"|qa!' -es 2>&1 | wc -m
    4~

##
## How to skip *all* initializations
### in Vim?

You need to reset `'loadplugins'` (e.g. via `--noplugin`).

          vvvvvvvvvv
    $ vim --noplugin -es +'set vbs=1|scriptnames|qa!'
    ''~

Otherwise, plugins are not skipped:

    $ vim -es +'set vbs=1|scriptnames|qa!'
     1: ~/.vim/plugin/emmet.vim~
     ...~
    12: /usr/local/share/vim/vim81/plugin/getscriptPlugin.vim~
    ...~
    24: ~/.vim/after/plugin/abolish.vim~
    ...~

### in Nvim?

You need to:

   - reset `'loadplugins'` (e.g. via `--noplugin`) to skip plugins

   - use `-u NONE` to skip the scripts sourcing the filetype/syntax/indent plugins

        1: /usr/local/share/nvim/runtime/filetype.vim
        2: /usr/local/share/nvim/runtime/ftplugin.vim
        3: /usr/local/share/nvim/runtime/indent.vim
        4: /usr/local/share/nvim/runtime/syntax/syntax.vim
        5: /usr/local/share/nvim/runtime/syntax/synload.vim
        6: /usr/local/share/nvim/runtime/syntax/syncolor.vim

   - use `-i NONE` to not write the ShaDa file

Example:

           vvvvvvvvvvvvvvvvvvvvvvvvvv
    $ nvim -u NONE -i NONE --noplugin -es +'set vbs=1|scriptnames|qa!'
    ''~

###
## What's its benefit over `$ sed -i`?

> Some sed(1)s have -i which claims to "modify" files.
> It does not: sed is not a FILE editor.
> The -i flag re-writes the entire file and replaces the original with the new.
> This breaks open handles and hard-link sets, and fails to follow symlinks.
> -i  is also  unportable: valid  sed on  one system  will write  broken files  on
> another.
> Use ed(1) or ex(1) instead: eg.
> ex -sc '%s/a/b/|wq' file

##
# Vim used in a shell pipeline
## In `$ echo cmd  | vim +cmd`, in which order are `echo cmd` and `+cmd` processed?

`+cmd` is processed before `echo cmd |`, even though it's written afterward.

    $ echo 'set vbs=1 number?' | vim -es +'%p' <(echo text)
    text~
    nonumber~

Notice that the  value of `'number'` is printed *after*  'text' (which itself is
due to `%p`).

This also explains why this command has no output:

    # `qa!` makes Vim quit before printing the value of the 'number' option
    $ echo 'set vbs=1 number?' | vim -es +'qa!' <(echo text)
    ''~

While this one has:

    $ echo 'set vbs=1 number?|qa!' | vim -es <(echo text)
      nonumber~

## In `$ echo text | vim +cmd`, in which order are `echo text` and `+cmd` processed?

`echo text` first populates a Vim buffer, *then* `+cmd` is run on the latter.

##
## special filename `-`
### What does it refer to?

The stdin.

The latter can be connected to a pipe via `|`:

    $ echo text | vim -

or to a file via `<`:

    $ cat <<'EOF' >/tmp/file
    foo
    bar
    EOF

    $ </tmp/file vim -

###
### When can I omit it?  (2)

When you're using Neovim:

    $ echo text    | nvim
    $ echo '1t1|x' | nvim -es /tmp/file

Or when you start  Vim in Ex mode with `-e`, and you  want the contents of stdin
to be read as an Ex command:

    $ echo '%s/X/l/|%p' | vim -es <(echo "helXo\nworXd")
    hello~
    world~

It's probably assumed at the end of the command-line.
But in practice, it's better to use it explicitly to improve readibility.

### The next shell command exits with the code 1.  How to fix it?

    $ echo text | vim -es +'%p' +'qa!'

↣
    $ echo text | vim --not-a-term - -es +'%p' +'qa!'
                                   ^
`--not-a-term` is only necessary to remove this message from the output:

    Vim: Reading from stdin...
↢

#### Explain why the first command fails, while the second works.

Without `-`, Vim processes  the stdin as if it had been specified  at the end of
the shell command-line:

    $ echo text | vim -es +'%p' +'qa!' -
                                       ^

As a result, its contents is processed as an Ex command, not as text.
So, the Vim buffer is empty, and `%p` fails to print anything.

By specifying `-` *before* `-es`, we make Vim process the stdin as a literal text.

---

The shell command does not exit with `1`  because of the fact that `text` is not
a valid Ex command.
Indeed, `+cmd` is always processed before `echo cmd`, so here `qa!` is processed
before the "command" `text`, and `text` is not run.

##
### When I use it, how is the stdin read by
#### Vim?

It depends on the position of `-` relative to `-e`/`-E`.

Before, it's read as literal text:

                          ┌ needed to redirect output of '%p' to Vim's stdout (= terminal)
                          │      ┌ needed because `text` is not read as an Ex command
                          │      │    ┌ remove `Vim: Reading from stdin...` message from output
                          │      ├─┐  ├──────────┐
    $ echo text | vim - -es +'%p|qa!' --not-a-term
    text~

After, it's read as an Ex command:

    $ echo "put! ='text'|%p" | vim -es -
    text~

#### Nvim?

With `-E`, `-` is read as literal text:

    $ echo text | nvim -Es +'%p' -
    text~

With `-e`, `-` is read as an Ex command:

    $ echo "put! ='text'|%p" | nvim -es -
    text~

---

Exceptions:

    # `cmd` is not run
    $ echo cmd | nvim -e

    # `cmd` should be run as an Ex command; instead it's used as text
    $ echo cmd | nvim - -e

Those are not  important to remember, because in practice  you'll never use `-e`
nor `-E` without `-s`.

###
### What if I omit it in
#### Vim?

Without `-e`/`-E`, Vim errors out:

    $ echo foo | vim
    Vim: Warning: Input is not from a terminal~
    Vim: Error reading input, exiting...~
    Vim: preserving files...~
    Vim: Finished.~

Rationale: Vim thinks  that you  made an  error, because it's  rarely used  in a
shell pipeline.

OTOH, if you pass `-` to Vim, the command succeeds.
Rationale: you've proved  that you know that  Vim is used in a  pipeline, so you
probably know what you're doing.

---

With `-e`/`-E`, Vim assumes `-` at the end of the command-line:

    # quits automatically (because stdin is read as Ex commands)
    $ echo 1t1 | vim   -e
    $ echo 1t1 | vim   -e -

    # populates buffer with '1t1', and starts in Ex mode
    $ echo 1t1 | vim - -e

#### Nvim?

You  can omit  `-`,  or position  it  wherever  you want;  it  doesn't make  any
difference:

    # populate Nvim buffer with 'text'
    $ echo text | nvim
    $ echo text | nvim -

    # exit status = 0
    $ echo sleep 1m | nvim   -es
    $ echo sleep 1m | nvim   -es -
    $ echo sleep 1m | nvim - -es

    # exit status = 1
    $ echo not_a_cmd | nvim   -es
    $ echo not_a_cmd | nvim   -es -
    $ echo not_a_cmd | nvim - -es

    $ echo not_a_cmd | nvim   -es   +'set vbs=1' 2>&1 | grep 'E[0-9]'
    $ echo not_a_cmd | nvim   -es - +'set vbs=1' 2>&1 | grep 'E[0-9]'
    $ echo not_a_cmd | nvim - -es   +'set vbs=1' 2>&1 | grep 'E[0-9]'
    E492: Not an editor command: not_a_cmd~

##
## When do I need `qa!`?

Always, unless (N)Vim reads an Ex command from a pipe or a file.

In the latter case, (N)Vim quits automatically.
This  is probably  why  an Ex  command  which is  read from  a  pipe, is  always
processed *after* `+cmd`; to allow the latter to be processed.

---

This behavior probably comes from the POSIX vi specification:

> if the  editor detects an  end-of-file condition  from the standard  input, it
> shall be equivalent to a SIGHUP asynchronous event.

<https://pubs.opengroup.org/onlinepubs/9699919799/utilities/vi.html>

---

So, you need `qa!` here:

    $ vim -es +'qa!' file

But not here:

    $ echo '%p' | vim -es file

---

This is also confirmed by:

    # all quit automatically, because `1t1` is read as an Ex command
    $ echo 1t1 | vim -E
    $ echo 1t1 | vim -e
    $ echo 1t1 | vim -E -
    $ echo 1t1 | vim -e -

    # none quit automatically, because `1t1` is read as literal text
    $ echo 1t1 | vim - -E
    $ echo 1t1 | vim - -e

### Which exception to this rule exist?

    # shouldn't quit automatically
    $ echo text | nvim -Es

I think this was implemented in Nvim as a convenience feature.
From <https://vimways.org/2018/vims-social-life/>:

> It also works with -Es (but not -es), **and it exits automatically (no +'qa!' needed)**:

There are other exceptions which are mentioned below.
But this  one is  the only exception  you should remember,  because none  of the
other ones use silent mode; and in practice, you'll always use silent mode.

---

    # shouldn't quit automatically (like `$ echo text | vim - -E`)
    $ echo text | nvim -E -

---

    # should quit automatically (like `$ echo cmd | vim -e` and `$ echo cmd | nvim -e -`)
    $ echo cmd | nvim   -e
    $ echo cmd | nvim - -e

---

Note that here, Nvim doesn't quit automatically:

    $ echo 1t1 | nvim -e

But this is not  an exception to the previous rule, because  `1t1` is *not* read
as an Ex command; it is ignored.

---

It seems that any command which doesn't  quit automatically can be forced to, by
redirecting stderr to `/dev/null` with `2>/dev/null` or `2</dev/null`.

It could be due to `man vim /^\s*-\s`:

> -           The  file  to  edit  is read from stdin.  **Commands are read**
>             **from stderr**, which should be a tty.

##
## When do I need `--not-a-term`?

When you feed *text* to Vim via its stdin (`$ cmd | vim -` or `$ <file vim -`).

But you don't need it when you feed an Ex command:

    $ echo "put! ='text'|%p" | vim -es -
    text~

##
# sourcing normal commands
## How is `-s` interpreted
### before `-e`/`-E`?

It expects  a filename argument whose  contents is processed as  normal commands
intended to be sourced.

### after `-e`/`-E`?

It makes Vim enter silent/batch mode, which is a kind of Ex submode.

##
## How to feed the output of a shell command to Vim as normal commands?

Use a process substitution:

    $ vim -s <(echo ifoo)

---

You can't use a shell pipeline:

    $ echo ifoo | vim -s -
    Cannot open for reading: "-"~

### What's the other possible way for Neovim?

A shell pipeline:

    $ echo ifoo | nvim -s -

#### When is it necessary to use this?

In a shell which doesn't support process substitution, like dash.

##
# Miscellaneous
## What are `ex` and `exim`?

Shell command names equivalent to `$ vim -e` and `$ vim -E`.

---

`ex` is a symlink to the Vim binary:

    $ type ex
    ex is /usr/local/bin/ex~

    $ ls -lh  /usr/local/bin/ex
    lrwxrwxrwx 1 root root ... /usr/local/bin/ex -> vim~

When Vim is invoked under the name `ex`, it automatically starts in Ex mode.

---

`exim` is not installed by default; and we  don't have it when we use our script
to manually compile and install Vim from source.

From `:h exim`:

> exim  vim -E      Start in improved Ex mode (see |Ex-mode|).      *exim*
>                         (**normally not installed**)

---

`ex` and `exim` have been removed from Nvim.
IOW, you can't invoke Nvim under those names.

### I get a whole bunch of errors when I run `ex`!

Initializations are not skipped, so your vimrc and plugins are sourced.
But when Vim is called under the name `ex`, it starts in compatible mode.
You need to reset `'compatible'`:

    $ ex -N
         ^^

###
## How to test in a shell script whether my Vim binary was compiled with a python interface?

Run `if has('python')` in Vim's silent mode.
And if the test succeeds, quit with `:qa!`; the exit status should be 0:

    $ vim -es +'qa!' ; echo $?
    0~

otherwise, quit with `:cq`; the exit status will be 1:

    $ vim -es +'cq' ; echo $?
    1~

Finally, test the exit status of the Vim command with the shell keyword `if`:

    $ if vim -es +'if has("python")|qa!|else|cq|endif'; then echo 'Vim has python2'; else echo 'Vim does not have python2'; fi
    Vim has python2~

---

In Nvim, you can prefix `:cq` with a count, which is used as the exit status:

    $ nvim -es +'123cq' ; echo $?
    123~

So, the previous command can be re-written like this:

    $ if nvim -es +'if has("python")|0cq|else|1cq|endif'; then echo 'Nvim has python2'; else echo 'Nvim does not have python2'; fi
    Nvim has python2~

####
# Issues
## I'm in silent/batch mode.  I can't quit!

Press:

    q!
     ^

Note the bang at the end to force Vim to quit even if the current buffer is modified.

If you've pressed `:vi` earlier, you need to press:

    :q!
    ^

Note the colon.

If you've run  `:a` or `:i`, you need  to enter a line containing  a single dot,
before you're able to quit:

    . CR
    q!

All in all, to be sure to quit no matter the current context, try:

    . CR
    :qa!

## I'm running `$ printf '%%p' | vim -es file`.  There's no output!

You need a trailing newline to run the Ex command:

    $ printf '%%p\n' | vim -es file
                 ^^

Or use `echo` which adds one automatically:

    $ echo '%p' | vim -es file

## I want to edit stdin *and* a file.  It doesn't work!  (Too many edit arguments)

So, you've run sth like:

    $ echo text | vim - file

Vim can edit the stdin, or one/several file(s).
But it can't edit both at the same time.

See `:h vim-arguments`:

> Exactly one out of the following five items may be used to choose how to
> start editing:

Solution:

Use Nvim:

    $ echo text | nvim file
    :ls
    1 %a + "[No Name]"~
    2      "file"~

##
## I'm running a shell pipeline whose exit status is non-zero.  What's the issue?

Increase the verbosity level to get more information:

    $ echo 'set vbs=1|your Ex commands' | vim ...
            ^^^^^^^^^

### What's the first line in the output of this command?

It's the contents of the current line in the buffer:

    $ echo 'set vbs=1|2d' | vim -es =(printf 'one\ntwo\nthree\nfour\nfive')
    three~

Here, `2d` makes Vim move the cursor on the second line and remove it.
At that point, the current line is the one containing 'three'.

### The issue comes from the fact that my file is opened in readonly mode.  Why does that happen?

So, Vim gives this warning:

    W10: Warning: Changing a readonly file

It  could be  due to  the existence  of a  swapfile which  was not  removed when
quitting a Vim session (maybe it crashed).

MWE:

    $ touch /tmp/.file.swp && \
      echo 1t1 | vim -es /tmp/file

If that's  what is  happening, grep  for the  swapfile in  the directory  of the
associated file:

    $ ls -a /tmp | grep '.file.sw'

Once you find it, remove it.

####
## I've edited a file with a shell pipeline invoking Vim in silent mode.  I've lost my undo tree!

Your editions have not been saved in an undo file.
As a result, the contents of the undo  file is not synchronized with the file it
was written for.

From `:h persistent-undo`:
> Vim will detect if an undo file is no longer synchronized with the file it was
> written for (with a hash of the file contents) and ignore it when the file was
> changed after the undo file was written, to prevent corruption.

You  need to  manually  "undo" (can't  use `:undo`  nor  `u`) the  modifications
applied since the last time the undo file was saved.
You can do it interactively or not; but in any case, you must unset `'undofile'`
so that your editions do not alter the contents of the undo file.
The goal is to  make the contents of your file synchronized with  the one of its
undo file again.

### How to avoid this issue in the future?

Set `'undofile'` (boolean) and `'undodir'` (string) appropriately.

    $ echo '1t1|x' | vim -es --cmd 'set udf udir=$HOME/.vim/tmp/undo' /tmp/file
                                                 ├─────────────────┘
                                                 └ value I currently use in my vimrc

##
## When entering/leaving improved Ex mode (`gQ`), `E501` or `E749` is raised.  What does that mean?

Some empty line is sourced.

You  may have  an autocmd  listening to  `CmdlineEnter` or  `CmdlineLeave` which
calls a function or sources a script which contains an empty line.
Note that  if the  called function  is autoloaded,  it causes  Vim to  source an
entire script;  and if  the latter  contains an empty  line anywhere,  the issue
applies again.

Or, you may have a mapping such as:

    cno <expr> <cr> Func()
    fu! Func()

        return "\<cr>"
    endfu

Which, again, contains an empty line sourced when you leave improved Ex mode.

---

I don't understand the root cause of the issue.

The issue should not affect you when you use Vim as a scripting tool, because in
that case, you  should start it in silent mode,  which skips initializations and
switches off most messages.

If  it  affects   you  when  you  use  Vim  interactively,   you  could  try  to
remove/comment all the empty lines in all functions/autoloaded scripts which are
called/sourced when you enter/leave a command-line.
But that would probably be too tedious, and  you would have to do it again every
time you add a new autocmd listening to `CmdlineEnter`/`CmdlineLeave`.

At the moment, we have 7 plugins which are affected by this issue:

   * vim-capslock
   * vim-cmdline
   * vim-iabbrev
   * vim-readline
   * vim-save
   * vim-term
   * vim-toggle-settings

---

MWE1:

    $ echo text | nvim -Nu NONE +'fu Func()

    endfu' +'au CmdlineLeave : call Func()' -E
    :vi
    E501: At end-of-file~

MWE2:

    $ echo cmd | nvim -Nu NONE +'fu Func()

    endfu' +'au CmdlineLeave : call Func()' -e
    :vi
    E749: empty buffer~

