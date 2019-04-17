# What's the meaning of `-e` in Vim?

It makes Vim start in Ex mode (`Q`).

## `-E`?

It makes Vim start in improved Ex mode (`gQ`).

### How are these options interpreted in Neovim?

They both start Nvim in improved Ex mode.
And if stdin is not a TTY (e.g. a pipe or `<file`), it's read as:

   - Ex commands with `-e`
   - text (into buffer 1) with `-E`

##
# What are the shell commands equivalent to `$ vim -e` and `$ vim -E`?

    $ ex
    $ exim

# What's the influence of `-e` or `-E` on the meaning of `-`?

`-`  always refers  to the  standard input,  however its  contents is  processed
differently depending on whether it's before or after `-e`, `-E`.
Before,  it's processed  as  some text  to  populate the  buffer;  after, as  Ex
commands.

## ... on the meaning of `-s`?

Before `-e` and  `-E`, `-s` expects a file argument  whose contents is processed
as normal commands intended to be sourced.
After, it makes vim enter silent/batch mode, which is a kind of Ex submode.

##
# What characterizes silent/batch mode?

In this  mode, most prompts,  informative messages, warnings and  error messages
are switched off.

Besides, the output of these commands is printed to stdout:

   - `:print`
   - `:list`
   - `:number`
   - `:set`

Finally, initializations are skipped (except the ones given with the "-u" argument).

## When is it useful?

When you need to edit some text non-interactively.
That is, when you want to execute Ex  commands from a file or a pipe, instead of
the terminal keyboard.

Example:

    $ cat <<'EOF' >/tmp/file
    helzo
    worzd
    EOF

    $ cat <<'EOF' >/tmp/filter
    %s/z/l/g | %p
    EOF

    $ vim -e -s </tmp/filter /tmp/file
    hello~
    world~

## How to make Vim print error messages in this mode?

Increase the value of the `'verbose'` option, using for example `-V`:

    $ vim -V1 -es

The messages are printed on stderr.

##
# When don't you need the special file argument `-` to refer to stdin?

When you're using Neovim:

    $ echo text | nvim

Or when you start  Vim in Ex mode with `-e`, and you  want the contents of stdin
to be parsed as Ex commands:

    $ cat <<'EOF' >/tmp/file
    helzo
    worzd
    EOF

    $ echo '%s/z/l/|%p' | vim -es /tmp/file
    hello~
    world~

It's probably assumed at the end of the command-line.
But in practice, it's better to use it explicitly to improve readibility.

# The next shell command exits with the code 1.  How to fix it?

    $ echo foo | vim -es +'%p' +'qa!'

↣
    $ echo foo | vim - -es +'%p' +'qa!'
                     ^
↢

## Explain why the first command failed, while the second works.

Without `-`, Vim processes  the stdin as if it had been specified  at the end of
the shell command-line:

    $ echo foo | vim -es +'%p' +'qa!' -
                                      ^

As a result, its contents is processed as Ex commands.
But `foo` is not a valid Ex command.

By specifying `-` *before* `-es`, we make Vim process the stdin as buffer text.
And `foo` is a valid text.

##
# How to feed the output of a shell command to Vim as normal commands?

Use a process substitution:

    $ vim -s <(echo ifoo)

## What's the other possible way for Neovim?

Instead of a command substitution, you can also use `-` to refer to stdin:

    $ echo ifoo | nvim -s -

This doesn't work in Vim:

    $ echo ifoo | vim -s -
    Cannot open for reading: "-"~

##
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

If  it  affects   you  when  you  use  Vim  interactively,   you  could  try  to
remove/comment all the empty lines in all functions/autoloaded scripts which are
called/sourced when you enter/leave a command-line.
But that would probably be too tedious, and  you would have to do it again every
time you add a new autocmd listening to `CmdlineEnter`/`CmdlineLeave`.

If the issue affects you when you use Vim as TODO: finish this sentence

   - start Nvim with `-es` or `-Es`

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

    $ echo 'y' | nvim -Nu NONE +'fu Func()

    endfu' +'au CmdlineLeave : call Func()' -E
    E501: At end-of-file~

MWE2:

    $ echo 'y' | nvim -Nu NONE +'fu Func()

    endfu' +'au CmdlineLeave : call Func()' -e
    E749: empty buffer~
    :vi
    E749: empty buffer~

