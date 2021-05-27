# silent/batch mode
## What characterizes this mode?  (4)

The TUI is not drawn.

---

Most initializations are skipped.

---

Most prompts, warnings,  informative/error messages are switched  off; hence the
mode name "silent".

---

The output of these commands is printed to stdout:

   - `:print`
   - `:list`
   - `:number`
   - `:set`

This is especially  useful in a pipeline,  to send the output of  Vim to another
shell command for further processing:

                               v
    $ echo 'a\nb\nc' | vim - -es +'2d|%p|qa!' --not-a-term | tr '[ac]' '[AC]'
    A˜
    C˜

Here, without `-s`, the output would be empty.
This is because Vim would write directly  to the terminal, to draw the output in
its own window; it  would not write the output on its  stdout which is connected
to the shell pipe.

## When is it useful?  (2)

When you need to edit some text non-interactively.
That is, when you want to execute Ex  commands from a file or a pipe, instead of
the keyboard.

---

It's  also useful  when  you want  a  Vim command  to print  its  output on  the
terminal; useful to easily reproduce some  behavior (either in your notes, or in
a bug report).

Instead of writing sth like:

    $ vim
    :ls

You can write a shell one-liner:

    $ vim -es +"pu=execute('ls')" +'%p|qa!'

##
## I have a long series of Ex commands I want to regularly run on some file(s).
### What's the most readable and re-usable way to apply them?

Write them in a `filter` file, then run:

    $ vim -es <filter file
              │
              └ redirect to stdin

Which is equivalent to:

    $ cat filter | vim -es - file

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
    hello˜
    world˜

##
## How to make Vim print the messages output by all Ex commands in this mode?

Increase Vim's verbosity:

    $ vim +'set vbs=1' -es

---

It's better to set `'verbose'` via `:set`:

            v-------v
    $ echo 'set vbs=1|2d' | vim -es =(printf 'one\ntwo\nthree\nfour\nfive')
    three˜

than via `-V1` which produces much more noise:

                    v-v
    $ echo 2d | vim -V1 -es =(printf 'one\ntwo\nthree\nfour\nfive')
    XSMP opening connection˜
    not found in 'packpath': "pack/*/start/*"˜
    GetLatestVimScripts is not vi-compatible; not loaded (you need to set nocp)˜
    not found in 'packpath': "pack/*/start/*"˜
    Opening the X display took 0 msec˜
    Opening the X display took 1 msec˜
    "/tmp/zshgrd5so"˜
    "/tmp/zshgrd5so" [Incomplete last line] 5 lines, 23 characters˜
    Entering Ex mode.  Type "visual" to go to Normal mode.˜
    :˜
    XSMP handling save-yourself request2d˜
    three˜
    :% ˜

### I can't redirect these messages to another shell command!

They are printed  on stderr, even the ones  not due to errors; so  use `2>&1` to
also redirect stderr:

    ✘
    $ vim +'set vbs=1|echo "test"|qa!' -es | wc -m
    test0˜

                                           ✔
                                           v--v
    $ vim +'set vbs=1|echo "test"|qa!' -es 2>&1 | wc -m
    4˜

##
## How to skip *all* initializations?

You need to reset `'loadplugins'` (e.g. via `--noplugin` or `-Nu NONE`):

          v--------v
    $ vim --noplugin -es +'set vbs=1|scriptnames|qa!'
    ''˜

Otherwise, plugins are not skipped:

    $ vim -es +'set vbs=1|scriptnames|qa!'
     1: ~/.vim/plugin/emmet.vim˜
     ...˜
    12: /usr/local/share/vim/vim81/plugin/getscriptPlugin.vim˜
    ...˜
    24: ~/.vim/after/plugin/abolish.vim˜
    ...˜

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

Source: <http://wooledge.org/~greybot/meta/sed-i>
Also, connect to the irc server libera, then run this command:

    /msg greybot sed-i

---

Besides, `$ sed -i` makes you lose Vim's undo tree.
With Vim,  you can preserve  the latter provided  that you set  `'undofile'` and
`'undodir'` appropriately.

##
# What's the difference between `-e` and `-E` when used to start Vim
## non-interactively?

None.

They both start Vim in Ex mode.

## interactively?

`-E` starts an  "improved" Ex mode in which command  line editing and completion
are available.

In a usual Vim session, by default, you can access the Ex mode matching `-e` and
`-E` by pressing resp. `Q` and `gQ`.

##
# Vim used in a shell pipeline
## special filename `-`
### What does it refer to?

Vim's stdin.

The latter can be connected to a pipe via `|`:

    $ echo text | vim -

or to a file via `<`:

    $ </tmp/file vim -
      ^

###
### When I use it, how is the stdin read by Vim?

It depends on the position of `-` relative to `-e`/`-E`.

Before, it's read as literal text:

                          ┌ needed to redirect output of '%p' to Vim's stdout (= terminal)
                          │      ┌ needed because `text` is not read as an Ex command
                          │      │    ┌ remove `Vim: Reading from stdin...` message from output
                          │      ├─┐  ├──────────┐
    $ echo text | vim - -es +'%p|qa!' --not-a-term
    text˜

After, it's read as an Ex command:

    $ echo "pu!='text'|%p" | vim -es -
    text˜

###
### What if I omit it
#### in Vim without using `-e`/`-E`?

Vim errors out:

    $ echo foo | vim
    Vim: Warning: Input is not from a terminal˜
    Vim: Error reading input, exiting...˜
    Vim: preserving files...˜
    Vim: Finished.˜

Rationale: Vim thinks  that you  made an  error, because it's  rarely used  in a
shell pipeline.

OTOH, if you pass `-` to Vim, the command succeeds.
Rationale: you've proved  that you know that  Vim is used in a  pipeline, so you
probably know what you're doing.

#### in Vim with `-e`/`-E`?

Vim assumes `-` at the end of the command-line:

    # quits automatically (because stdin is read as Ex commands)
    $ echo 1t1 | vim   -e
    $ echo 1t1 | vim   -e -

    # populates buffer with '1t1', and starts in Ex mode
    $ echo 1t1 | vim - -e

##
### When can I omit it?  (2)

When you start Vim in Ex mode with `-e`  (or `-E`), and you want the stdin to be
read as an Ex command:

    $ echo '%s/X/l/|%p' | vim -es <(echo "helXo\nworXd")
    hello˜
    world˜

It's probably assumed at the end of the command-line.
But in practice, it's better to use it explicitly to improve readibility.

##
### The next shell command exits with the code 1.  How to fix it?

    $ echo text | vim -es +'%p|qa!'

↣

    $ echo text | vim --not-a-term - -es +'%p' +'qa!'
                                   ^
`--not-a-term` is only necessary to remove this message from the output:

    Vim: Reading from stdin...
↢

#### Explain why the first command fails, while the second works.

Without `-`, Vim processes  the stdin as if it had been specified  at the end of
the shell command-line:

    $ echo text | vim -es +'%p|qa!' -
                                    ^

As a result, its contents is processed as an Ex command, not as text.
So, the Vim buffer is empty, and `%p` fails to print anything.

By specifying `-` *before* `-es`, we make Vim process the stdin as a literal text.

#### Explain why the shell command exits with the code 1.

That's not because `:text` is not a  valid Ex command; that's because the buffer
is empty, and `:p` fails to print anything.

`+'%p|qa!'`  is before  `echo  text`,  so here  `qa!`  is  processed before  the
"command" `text`, and `:text` is not run.

##
## When do I need `qa!`?

Always, unless Vim reads an Ex command from a pipe or a file.

In the latter case, Vim quits automatically.
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

It seems that any command which doesn't  quit automatically can be forced to, by
redirecting stderr to `/dev/null` with `2>/dev/null` or `2</dev/null`.

It could be due to `man vim /^\s*-\s`:

   > -           The  file  to  edit  is read from stdin.  **Commands are read**
   >             **from stderr**, which should be a tty.

##
## When do I need `--not-a-term`?

When you feed *text* to Vim via its stdin (`$ cmd | vim -` or `$ <file vim -`).

But you don't need it when you feed an Ex command:

    $ echo "pu!='text'|%p" | vim -es -
    text˜

##
## In `$ echo cmd  | vim +cmd`, in which order are `echo cmd` and `+cmd` processed?

`+cmd` is processed before `echo cmd |`, even though it's written afterward.

    $ echo 'set vbs=1 number?' | vim -es +'%p' <(echo text)
    text˜
    nonumber˜

Notice that the  value of `'number'` is printed *after*  'text' (which itself is
due to `%p`).

This also explains why this command has no output:

    # `qa!` makes Vim quit before printing the value of the 'number' option
    $ echo 'set vbs=1 number?' | vim -es +'qa!'
    ''˜

While this one has:

    $ echo 'set vbs=1 number?|qa!' | vim -es
      nonumber˜

## In `$ echo text | vim +cmd`, in which order are `echo text` and `+cmd` processed?

`echo text` first populates a Vim buffer, *then* `+cmd` is run on the latter.

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
    Cannot open for reading: "-"˜

##
# Miscellaneous
## What are `ex` and `exim`?

Shell command names equivalent to `$ vim -e` and `$ vim -E`.

---

`ex` is a symlink to the Vim binary:

    $ type ex
    ex is /usr/local/bin/ex˜

    $ ls -lh  /usr/local/bin/ex
    lrwxrwxrwx 1 root root ... /usr/local/bin/ex -> vim˜

When Vim is invoked under the name `ex`, it automatically starts in Ex mode.

---

`exim` is not installed by default; and we  don't have it when we use our script
to manually compile and install Vim from source.

From `:h exim`:

   > exim  vim -E      Start in improved Ex mode (see |Ex-mode|).      *exim*
   >                         (**normally not installed**)

### I get a whole bunch of errors when I run `ex`!

When Vim is called under the name `ex`, it starts in compatible mode.
And even if  the vimrc is skipped,  some plugins are still  sourced; namely, any
vimscript file inside one of these directories:

   - `~/.vim/plugin`
   - `$VIMRUNTIME/plugin`
   - `~/.vim/after/plugin`

You need to reset `'compatible'`:

    $ ex -N
         ^^

And you probably want to use `-u NONE` too.

###
## How to test in a shell script whether my Vim binary was compiled with a python interface?

Run `if has('python3')` in Vim's silent mode.
And if the test succeeds, quit with `:0cq`; the exit status should be 0:

    $ vim -es +'0cq' ; echo $?
    0˜

Otherwise, quit with `:cq`; the exit status will be 1:

    $ vim -es +'cq' ; echo $?
    1˜

Finally, test the exit status of the Vim command with the shell keyword `if`:

    $ if vim -es +'if has("python3")|0cq|else|1cq|endif'; then echo 'Vim has python3'; else echo 'Vim does not have python3'; fi
    Vim has python3˜

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

##
## I'm running a shell pipeline whose exit status is non-zero.  What's the issue?

Increase the verbosity level to get more information:

    $ echo 'set vbs=1|your Ex commands' | vim ...
            ^-------^

### What's the first line in the output of this command?

It's the contents of the current line in the buffer:

    $ echo 'set vbs=1|2d' | vim -es =(printf 'one\ntwo\nthree\nfour\nfive')
    three˜

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

   > Vim will detect if an undo file  is no longer synchronized with the file it
   > was written for (with  a hash of the file contents) and  ignore it when the
   > file was changed after the undo file was written, to prevent corruption.

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

