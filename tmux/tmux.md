# Syntax
## What is `info` in `$ tmux info`?  I can't find it in the documentation.

It's an alias for `show-messages -JT`.

    $ tmux show-options -s command-alias
    ...~
    command-alias[3] "info=show-messages -JT"~
    ...~

##
## How does tmux parse a semicolon?

As a command termination (like the shell).

---

From `man tmux /COMMANDS`:

   > Multiple commands may be specified together as part of a command sequence.
   > Each  command should  be  separated  by spaces  and  a  semicolon; commands  are
   > executed  sequentially from  left to  right and  lines ending  with a  backslash
   > continue on to the next line, except when escaped by another backslash.
   > A  literal semicolon  may  be included  by  escaping it  with  a backslash  (for
   > example, when specifying a command sequence to bind-key).

### When do I need to escape a semicolon?

When you install a key binding whose rhs contains several commands, separated by
semicolons.

---

If you write:

    bind <key> cmd1 ; cmd2

tmux will populate its key bindings table with:

    <key> cmd1

Because the semicolon has prematurely terminated `bind`.
Then, tmux will *immediately* run `cmd2`.

### How many backslashes do I need if I install a tmux key binding from the shell?

Three.

    $ tmux bind <key> cmd1 \\\; cmd2
                           ^-^

This  is because  the semicolon  is  also special  for the  shell; the  latter
automatically removes one level of  backslashes; after this removal, tmux will
correctly receive `\;`.

If you only wrote two backslashes, the shell would reduce them into a single one
– passed to tmux – and the remaining semicolon would not be escaped.
So, the shell would try to run `cmd2` itself.

##
### Why does this key binding fail?  `$ tmux bind C-z "run { tmux display -p 'foo' \; tmux display -p 'bar'}"`

Because you've escaped the semicolon; don't do it:

    $ tmux bind C-z "run { tmux display -p 'foo' ; tmux display -p 'bar'}"
                                                 ^
                                                 no escape

You only  need to  escape a  semicolon in  the rhs  of a  key binding  when it's
outside a string and outside braces.
Both  a string  and braces  remove the  special meaning  of the  characters they
contain.

##
## Which escape sequences does tmux translate?  (6)

    ┌────────────┬───────────────────────────────────────────────┐
    │ \e         │ escape character                              │
    ├────────────┼───────────────────────────────────────────────┤
    │ \r         │ carriage return                               │
    ├────────────┼───────────────────────────────────────────────┤
    │ \n         │ newline                                       │
    ├────────────┼───────────────────────────────────────────────┤
    │ \t         │ tab                                           │
    ├────────────┼───────────────────────────────────────────────┤
    │ \uXXXX     │ unicode codepoint corresponding to `XXXX`     │
    │ \uXXXXXXXX │                                    `XXXXXXXX` │
    ├────────────┼───────────────────────────────────────────────┤
    │ \ooo       │ character of octal value `ooo`                │
    └────────────┴───────────────────────────────────────────────┘

### On which condition is the translation/expansion performed?

The escape sequence must be outside a  string, or inside a double-quoted string,
but not inside a single-quoted string.

    set -g @foo a\u00e9b
    $ tmux show -gv @foo
    aéb~

    set -g @foo "a\u00e9b"
    $ tmux show -gv @foo
    aéb~

    set -g @foo 'a\u00e9b'
    $ tmux show -gv @foo
    a\u00e9b~

##
# Quoting
## When must I avoid single quotes in my tmux.conf?

When you need an  environment variable to be expanded, or  an escape sequence to
be translated.

---

For example, this key binding would not print the name of your editor:

    bind C-g display '$EDITOR'

But this one would:

    bind C-g display "$EDITOR"

And this code would not print some text in green on the right of your status line:

    my_color=green
    set -g status-right '#[bg=$my_color]this should be colored in $my_color'

But this one would:

    my_color=green
    set -g status-right "#[bg=$my_color]this should be colored in $my_color"

### But if I write `run 'echo $EDITOR'`, tmux outputs `vim`.  Shouldn't the output be empty?

No, because the command is parsed twice.
Once by tmux, once by a shell.

It's true that  the single quotes prevent tmux from  expanding the variable, but
they're removed once the command is passed to the shell.
The latter simply runs `$ echo $EDITOR`; so it's able to perform the expansion.

##
## In my tmux.conf, should I quote filenames passed to `source-file` with single or double quotes?

With double quotes.

### Why should I do it?  (2)

In case it contains an environment variable whose expansion includes whitespace.
Even if it doesn't contain one now, it may in the future.
Besides, it's  a matter of  consistency: it would be  a bit distracting  to read
filenames which are sometimes quoted, and sometimes not.

---

If a  filename contains  the name  of an option  or command,  the latter  may be
highlighted as such, instead of being highlighted as a filename.

Quoting a filename makes sure that there won't be any dubious syntax highlighting.

The issue is not specific to our custom syntax plugin; it can be reproduced with
the default plugin.

##
## Why can't I use two single quotes to represent a single quote in a single-quoted string?

tmux interprets `''` as  the end of a string followed by the  beginning of a new
one; and then it concatenates them.

    $ tmux source =(cat <<'EOF'
    set @foo 'x''y'
    EOF
    ) \; show -v @foo
    xy~

It behaves just like the shell:

    $ echo 'x''y'
    xy~

### Then how to include a single quote inside a single-quoted string?

Use `'\''`.

    set @foo 'x'\''y'
               │├┘│
               ││ └ start a new string
               │└ insert a single quote
               └ end the string

    $ tmux source =(cat <<'EOF'
    set @foo 'x'\''y'
    EOF
    ) \; show -v @foo
    x'y~

Alternatively, you could use `'"'"'`.

###
## How to write an escape character?

You need a double-quoted string.
Inside, write `\e` or `\033`.

    set user-keys[0] "\ex"
    bind -n User0 display hello

    set user-keys[1] "\033y"
    bind -n User1 display world

---

In the  value of 'terminal-overrides', you  have to use `\E`  in a single-quoted
string or `\\E` in a double-quoted string,  because `\E` is the notation used by
terminfo to denote an escape character.

##
## backslash
### How does tmux process backslashes in strings?

In a single-quoted string, they're preserved.

In a  double-quoted string, tmux removes  any backslash which is  not escaped by
another backslash, just like Vim.

    :display 'a \z b'
    a \z b~

    :display "a \z b"
    a z b~

    :display "a \\z b"
    a \z b~

If the next character has a special meaning, the latter is removed:

    :display "a\"b"
    a"b~

#### Outside strings?

It  is removed,  and if  the next  character is  special, it  loses its  special
meaning:

    :display foo\ bar
    foo bar~

    :display foo\\\ bar
    foo\ bar~
       │
       └ originally, this was the second backslash;
         it has been preserved because the previous backslash removed its special meaning;
         so now, it's treated as a regular character, and as such, is kept in the output

That's also what lets you make a key binding run several commands:

    bind C-g display -p hello \; display -p world
                              ^^

###
### Why is there a difference in the output of `$ tmux display -p "\z"` vs `:display -p "\z"`?

    $ tmux display -p "\z"
    \z~

    :display -p "\z"
    z~

The shell parses the first command before tmux.
It  doesn't remove  the backslash,  because in  a double-quoted  string, `\`  is
removed only when it's special, i.e.  only when it's followed by some characters
(like `$`), and `z` is not one of them.
Also, a  shell –  probably –  only passes  *literal* strings  as arguments  to a
command it runs; so here, zsh passes  the literal string `'\z'` to tmux, and the
latter doesn't replace anything in a literal string.

OTOH, in the second command, tmux is  the first to parse the command (there's no
shell this time); and tmux removes one level of backslash, unconditionally.

###
### What is the output of
#### `:run "echo foo \; echo bar"`?

    foo
    bar

---

After tmux parses the command:

    cmd = sh
    arg = echo foo ; echo bar

After sh parses the command:

    cmd1 = echo
    arg1 = foo

    cmd2 = echo
    arg2 = bar

#### `:run "echo foo \\\; echo bar"`?

    foo ; echo bar

---

After tmux parses the command:

    cmd = sh
    arg = echo foo \; echo bar

After sh parses the command:

    cmd = echo
    arg = foo ; echo bar

#### `$ tmux run "echo foo \; echo bar"`?

    foo ; echo bar

---

After zsh parses the command:

    cmd = tmux
    arg = run 'echo foo \; echo bar'

After tmux parses the command:

    cmd = sh
    arg = echo foo \; echo bar

After sh parses the command:

    cmd = echo
    arg = foo ; echo bar

Initially,  zsh doesn't  remove  the  backslash because  `;`  is  not a  special
character to the shell when it's quoted by `"`.

Then,  tmux doesn't  remove  the backslash,  probably because  it  was passed  a
literal string by zsh.

Finally, sh removes the backslash – which itself has removed the special meaning
of `;` – and includes `;` in the argument of `echo`.

#### `$ tmux run "echo foo \\\; echo bar"`?

    foo \
    bar

---

After zsh parses the command:

    cmd = tmux
    arg = 'echo foo \\; echo bar'

After tmux parses the command:

    cmd = sh
    arg = 'echo foo \\; echo bar'

After sh parses the command:

    cmd1 = echo
    arg1 = foo \

    cmd2 = echo
    arg2 = bar

##
# Getting Information
## How to get the name of the outer terminal?

Use the format variable `#{client_termname}`:

    $ tmux display -p '#{client_termname}'
                    │
                    └ print output to stdout,
                      instead of the target-client status line

However, be  aware that this  information is  not always reliable,  because many
terminals lie about their identity (they pretend to be xterm-256color).

## How can I make the difference between a tmux server and a tmux client in the output of `ps(1)`?

Look at the process state codes.
If you can read `Ss`, it's a server; `S+`, it's a client.

    ┌───┬────────────────────────────────────────────────────────┐
    │ S │ interruptible sleep (waiting for an event to complete) │
    ├───┼────────────────────────────────────────────────────────┤
    │ s │ is a session leader                                    │
    ├───┼────────────────────────────────────────────────────────┤
    │ + │ is in the foreground process group                     │
    └───┴────────────────────────────────────────────────────────┘

See `man ps /PROCESS STATE CODES`.

---

Alternatively, look at the terminal to which the process is attached.
If you can read `?`, it's a server; `pts/123`, it's a client.

## How do I get the pid of the terminal client?  `$ pstree -lsp $$` doesn't work!

`$$` is replaced  by the pid of the  current shell which is handled  by the tmux
server, run probably by your session manager which itself is run by systemd.
Your terminal is not in the tree process.

You need to look at the tmux client, not the tmux server:

    $ pstree -lsp $(tmux display -p '#{client_pid}')

##
# Buffers
## How to delete a tmux buffer interactively?

   1. run `choose-buffer`
   2. select a tmux buffer
   3. press `d`

For more info, see:

    man tmux /choose-buffer

### Several buffers in one keypress?

Tag the buffers you want to delete by  pressing `t` while your cursor is on each
of them, then press `D`.

---

Note the difference between `d` and `D`.
`d` deletes the currently selected buffer.
`D` deletes all the tagged buffers.

### All buffers?

Press `C-t` to tag all buffers, then `D`.

##
# Debugging
## Crash
### How to get a backtrace?

Make sure to run `$ ulimit -c unlimited` before reproducing the crash.
After the crash, tmux should have left a core file in the current directory.
You can extract a backtrace from it by running:

    $ gdb -n -ex 'thread apply all bt full' -batch /path/to/tmux /path/to/core >backtrace.txt

#### It doesn't contain any useful info!

Don't use the installed binary.
Recompile one with our zsh snippet:

    $ git stash; make clean; make distclean; sh autogen.sh && ./configure && make

And use it to extract a backtrace from the core:

    $ gdb -n -ex 'thread apply all bt full' -batch ~/Vcs/tmux/tmux /path/to/core >backtrace.txt
                                                   ^-------------^

---

Explanations:

By  default, checkinstall  strips  the  binary from  all  its  symbols, and  its
debugging information.
This greatly  reduces the size  of the binary, but  prevents you from  getting a
useful backtrace.

<https://unix.stackexchange.com/questions/2969/what-are-stripped-and-not-stripped-executables-in-unix>

Alternatively, you could pass `--strip=no` to checkinstall.

Besides, for some reason, it seems tmux doesn't include debugging information in
the binary if you change the version of the program.
This is why you  need `$ git stash`; to restore `configure.ac`  as it was before
possible modifications.

Btw, don't conflate the *program* version with the *package* version.
The latter is  set via the `--pgkversion` option passed  to checkinstall, and it
has no effect on the current issue.

##### I need even more info!

Edit the `Makefile.am` file:

    $ sed -i '/AM_CFLAGS/s/-O2/-O0/' Makefile.am
                                 ^
                                 optimization level 0

Use the compiled binary to reproduce the crash, *and* to extract a backtrace from the core.

---

See `man gcc` for more info:

   > The output is sensitive to the effects of previous command-line
   > options, so for example it is possible to find out which
   > optimizations are enabled at -O2 by using:
   >
   >         -Q -O2 --help=optimizers
   >
   > Alternatively you can discover which binary optimizations are
   > enabled by -O3 by using:
   >
   >         gcc -c -Q -O3 --help=optimizers > /tmp/O3-opts
   >         gcc -c -Q -O2 --help=optimizers > /tmp/O2-opts
   >         diff /tmp/O2-opts /tmp/O3-opts | grep enabled

---

Note that I don't recommend using `-O0`, by default, all the time.
It has an impact on performance; not  on memory consumption, nor latency, but on
output bandwidth; you can test the latter, roughly, with these commands:

    $ yes | head -n 1000000 >two_megs.txt
    $ time cat two_megs.txt

###
### How to get the value of an expression referred to in the backtrace?

    $ gdb /path/to/tmux /path/to/core
    (gdb) set logging on
    (gdb) p *ctx
    (gdb) p *ctx->s
    (gdb) p *ctx->s->grid
    (gdb) p *s->grid
    (gdb) quit

The output should be in `gdb.txt`.
Here,  `*ctx`,  `*ctx->s`,  `*ctx->s->grid`   and  `*s->grid`  are  examples  of
expressions that the devs could ask you about.

Source: <https://github.com/tmux/tmux/issues/2173>

###
### tmux crashes, but it doesn't dump a core file!
#### How to get a backtrace?

    $ tmux -Lx kill-server

    $ gdb -q --args ./tmux -Lx new
    (gdb) set follow-fork-mode child
    (gdb) run
    # reproduce the crash
    (gdb) set logging on
    (gdb) bt full
    (gdb) quit

The backtrace should be in `gdb.txt`.

---

FIXME: Because  of  `set follow-fork-mode  child`,  a  shell command-line  typed
interactively may be "mangled".  For example,  typing `vim Enter`, may result in
`i Enter`.  If you can't reproduce, try  to make sure you're starting a new tmux
server (kill any existing server if necessary).

#### How to get a trace?

    $ tmux -Lx kill-server
    $ strace -ttt -ff -ostrace.txt tmux -Lx -f/dev/null new
                        ^--------^
                        output file

<https://github.com/tmux/tmux/issues/1603#issuecomment-462955045>

Don't  use the  `.out` extension;  it  seems GitHub  doesn't like  that kind  of
filename when you try to attach it in an issue.  Prefer `.txt`.

##
## How to debug tmux when it's hanging?

You have to consider 2 cases: either the server is hanging or the client.

If the server is hanging, from another terminal, get the pid of the tmux server.
Or, if you can, run this before reproducing the issue:

    $ tmux display -p '#{pid}'

Then, still from another terminal, run:

             make sure it's the same tmux than the one currently hanging
             v-------------------v
    $ gdb -q /path/to/running/tmux PID
    (gdb) set logging on
    (gdb) bt full
    (gdb) quit

The output of `bt full` should be in `gdb.txt`.
Join it to your bug report.

See here to learn more about how to make gdb print to a file instead of stdout:
<https://stackoverflow.com/a/5941271/9780968>

---

If the client is hanging, you can follow the same procedure as previously.
With two differences:

   - make sure *not* to close the terminal window (you would kill the hanging client)
   - to get the pid of the client, use the format variable `#{client_pid}`, and not `#{pid}`

Once you have a backtrace, close  the terminal window (by pressing Alt+F4), then
re-attach from another terminal.
The new tmux client should not hang.

A client may hang if a tmux command block its command queue indefinitely.

Example:

    $ echo 'run "sleep 99999999"' >/tmp/tmux.conf && tmux bind C-z source /tmp/tmux.conf
    # press `C-z`
    # from another terminal, `$ pkill sleep`

For a real example:

   > if-shell  and  run-shell  will  block  the  client  command  queue  where  the
   > source-file happens  until the child  process exits  so the hanging  but being
   > able to  attach a new  client is consistent with  tmux not realising  that the
   > process has exited.
<https://github.com/tmux/tmux/issues/1854#issuecomment-524910268>

   > You can see the same if you have a file that does 'run "sleep 10"' then do C-b
   > : source myfile - the client won't respond until the sleep is finished.
<https://github.com/tmux/tmux/issues/1854#issuecomment-524912247>

   > If it isn't getting SIGCHLD it will never know the processes have exited so it
   > will never let the client continue.
<https://github.com/tmux/tmux/issues/1854#issuecomment-524930364>

## When writing a bug report, which terminal geometry should I use?

Make sure the terminal has 80 columns, and 24 lines.

    $ echo $COLUMNS
    80~

    $ echo $LINES
    24~

The goal is to reproduce with a “standard” geometry.

See `man tmux /^\s*default-size`:

   > The default is 80x24.

See also `:h window-size`:

   > If everything fails a default size of 24 lines and 80 columns is assumed.

##
# Issues
## My `if-shell` and/or `run-shell` tmux command doesn't work!

Remember that tmux runs your shell command via **sh**, not bash:
<https://github.com/tmux/tmux/issues/1603#issuecomment-462955856>

So, do *not* test your command in zsh or bash, but in sh.

---

For example, if you need to toggle  the logging of the tmux server, this command
works in bash/zsh:

    $ kill -s SIGUSR2 $(ps -o ppid= $$)

But in sh, you need to remove the `SIG` prefix:

    $ kill -s USR2 $(ps -o ppid= $$)

<https://unix.stackexchange.com/a/199384/289772>

---

For the same  reason, make sure your  shell command does not  invoke `[[`, which
doesn't exist in sh; instead, use `[` or `test`.

    run '[[ -d $XDG_RUNTIME_DIR/tmux || mkdir $XDG_RUNTIME_DIR/tmux ]]'
         ^^                                                         ^^
         ✘

    run '[ -d $XDG_RUNTIME_DIR/tmux || mkdir $XDG_RUNTIME_DIR/tmux ]'
         ^                                                         ^
         ✔

    run 'test -d $XDG_RUNTIME_DIR/tmux || mkdir $XDG_RUNTIME_DIR/tmux'
         ^--^
         ✔

### It doesn't help!

Then redirect the standard error of the shell command to a file:

    run-shell 'my buggy command 2>/tmp/debug'
                                ^----------^

And read the error message written in the file to get more information.

###
## `$ tmux -Lx` doesn't read `~/.config/tmux/tmux.conf`!

Make sure you don't have a running tmux server listening to the socket `x`:

    $ ps aux | grep tmux | grep x
    user 6771 ... tmux -Lx -f/dev/null~
                           ├─────────┘
                           └ your custom config can't be read because of this

If there's one, kill it – from inside tmux – with `kill-server`:

    $ tmux kill-server

Don't worry, it won't kill another running tmux server.
It probably targets the current server by inspecting `$TMUX`.

---

This issue can happen, even with no  terminal running a tmux client connected to
this `x` socket.

MWE:

    $ xterm
    $ tmux -Lx -f/dev/null
    Alt-F4
    $ ps aux | grep tmux | grep test
    user ... tmux -Lx -f/dev/null~

Alt-F4 kills the client, but not the server.
The server keeps running in the background.

In contrast, if you  had pressed `C-d` to kill the current  shell, and there was
no other shell handled by the tmux server, this would have killed the latter.

## I have a pane running Vim.  `#{pane_current_command}` is not replaced with `vim`!

Are you running Vim in a pipeline?

    $ echo text | vim -

If so, then `#{pane_current_command}` is replaced by `zsh`.
I doubt it's a bug.

Try to get rid of the pipe.
For example, you could write `text` in a file, then pass this file to Vim.

    $ echo text >file ; vim file

If you can't easily get rid of the pipe, then use another heuristic to detect Vim.
For example, if you know that Vim opens an unnamed buffer, you can use:

    #{C:\[No Name\]}

It should be replaced  with a number different than `0`  (the screen line number
where `[No Name]` matches).
You can then use `if -F` to react accordingly:

    if -F '#{C:\[No Name\]}' "display 'Vim is running'" "display 'Vim is NOT running'"

##
## Weird sequences are printed on the screen intermittently!

Something  is  probably sending  escape  sequences  (CSI,  OSC, ...)  which  the
terminal doesn't understand.

It can  happen when  you re-attach to  a running tmux  session from  a different
terminal than the one where you started it.

For example, atm, we have a Vim plugin – vim-term – which sends `CSI 2 SPC q` to
the terminal right before exiting.
And xfce4-terminal, on Ubuntu 16.04, doesn't support this sequence.

Solution: Close the terminal,  and re-attach from another  one which understands
the sequence.

Alternatively,  make sure  to  close  the program  responsible  for sending  the
problematic sequence; then close the terminal,  which will kill the tmux client,
and restart a new one.
Note that  in the case  of vim-term + xfce4-terminal  + Ubuntu 16.04,  you would
also need to make sure you start Vim from a new shell, so that tmux has a chance
to update `$COLORTERM`.
Indeed, vim-term relies on the latter to detect xfce4-terminal.

---

You can  reproduce an example of  this issue by  running `$ printf '\e[ 2q'` in
xfce4-terminal on Ubuntu 16.04, and waiting.
The issue is fixed in more  recent versions of xfce4-terminal; I can't reproduce
on Ubuntu 18.04 in a VM.

## tmux is hanging indefinitely after using a process substitution!

So, you've run sth like:

    $ tmux load-buffer <(echo foobar)

Solution: Use `=()` instead of `<()`.

---

Here's what happens.

The shell opens  a file descriptor it  thinks won't be used and  then passes the
path equivalent of that file descriptor to  the client as an argument, which the
client then passes to the server.

But that  file descriptor might  already be  in use in  the server, so  when the
latter opens the fd,  it gets whatever that is, which might  not be suitable for
reading, so it can block or crash or behaves unexpectedly.

It wouldn't be easy to fix  this issue, without also breaking legitimate devices
like `/dev/null` or blacklisting some paths (which will depend on the platform).

For more info: <https://github.com/tmux/tmux/issues/1755>

Update: I think it has been fixed by:
<https://github.com/tmux/tmux/commit/c284ebe0ade7cc85ad6c3fe5ce7ed5108119222d>

This commit also lets `source-file` read its stdin:
<https://github.com/tmux/tmux/commit/5134666702ce972390f39e34bed9b60fe566263a>

##
##
##
# Theory

Several tmux clients can be attached to the same session.
The tmux server is automatically stopped when all sessions are killed.

---

When you want to attach a tmux client  to a tmux server, you don't start it from
the local machine.  The  server *and* the client are always  running on the same
machine.  The procedure consists in 2 steps:

   1. log in to the remote (for example via ssh)
   2. start a tmux client to attach it to a running tmux server

---

When you start tmux on the remote for the first time, 2 processes are created.
First, one for the client:

    login/urxvt───zsh───tmux: client
                  │
                  └ our initial shell, provided by:

                        - the `login` process in console
                        - a terminal emulator in X

... then another for the server:

    tmux: server───zsh

Both (chain of) processes are started by:

   - the init process in console:

         systemd

   - the display manager in X:

         systemd───lightdm───lightdm───upstart

You can check this with the following commands:

    $ pstree -lsp $(tmux display -p '#{pid}')
    $ pstree -lsp $(tmux display -p '#{client_pid}')

Note that the  server is started after  the first client, so its  pid is bigger,
which may seem counter-intuitive.
Also, the relationship between the 2 processes is NOT parent-child.
It's client-server.
IOW, they are 2 independent processes.
You won't find both of them listed in the output of the same `pstree(1)` command.
They communicate via a socket, which by default is called `default`.
The latter is created in the directory `tmux-{UID}` inside:

   - $TMUX_TMPDIR if the latter set
   - /tmp otherwise

---

Any shell created with a tmux client is a child of the tmux server:

    tmux: server─┬─zsh───vim
                 ├─zsh───pstree
                 └─zsh───cmus

This fact, combined  with the fact that  the tmux client is  a different process
with no parent-child relationship, means  that you're manipulating a shell which
is NOT the child of your current terminal.

This is very unusual: usually the program you're interacting with, is a child of
the terminal (direct or indirect).
Not  here, because  the tmux  client makes  you interact  with the  child of  an
entirely different process: the tmux server.

The  communications between the first  shell opened by the  terminal (before
executing tmux), the tmux client, and the tmux server are all [transparent][1]:
everything in red in the diagram is not visible.

# Démarrage

Voici qques argument qu'on peut passer à tmux au démarrage.

    -c shell-command

            Exécute `shell-command` en utilisant le shell par défaut.

            Ce dernier est défini par l'option `default-shell`.
            Par défaut, elle est vide, et tmux prend donc à la place `$SHELL`.
            `-c shell-command` est utile pour rendre tmux compatible avec le shell `sh` qd tmux
            est utilisé comme un login shell.

##
# Plugins
## heytmux

tmux scripting made easy

Heytmux can read STDIN, so:

    $ cat workspace.yml | heytmux

... is also valid.  It may seem pointless, but it lets you do:

    :w !heytmux

... with a visual selection in Vim.

I primarily  use Heytmux  to write Markdown  documents with  fenced code
blocks of YAML snippets that I can easily select and run with Heytmux in
my editor.

<https://github.com/junegunn/heytmux>

## tpm

If you use tpm, beware of the following pitfall.

Suppose you want to write a command  after `set -g @plugin '...'`; you obviously
need to separate both commands with a semicolon.
But do *not* forget to prefix the semicolon with a space!

    set -g @plugin 'Morantron/tmux-fingers' ; source "$HOME/.tmux/plugins_config/fingers"
                                           ^

Without, tpm would not source the plugin.

I think that's because tpm parses the contents of `~/.config/tmux/tmux.conf`:

    ~/.tmux/plugins/tpm/tpm:44
    ~/.tmux/plugins/tpm/scripts/source_plugins.sh:31
    ~/.tmux/plugins/tpm/scripts/helpers/plugin_functions.sh:37
    ~/.tmux/plugins/tpm/scripts/helpers/plugin_functions.sh:49

It probably  relies on some  regex, and doesn't  expect a semicolon  to follow
immediately a `set -g @plugin ...` statement.

To be clear, I don't think it's a tmux issue, it's a tpm issue.
For example, this works fine:

    $ cat <<'EOF' >/tmp/file
    display -p 'hello'
    EOF
    set -g @option 'value'; source '/tmp/file'
                          ^
                          no space before

##
# Utilitaires
## Reptyr

reptyr est un pgm permettant d'attacher à une session tmux, un processus lancé
depuis un shell hors de la session.

    sudo aptitude install reptyr

            installation

    reptyr 42

            Attacher le processus de pid 42 à la session courante.

            Au cas où le message d'erreur suivant apparaît :

                    Unable to attach to pid xxxx: Operation not permitted
                    The kernel denied permission while attaching.  If your uid matches
                    the target's, check the value of /proc/sys/kernel/yama/ptrace_scope.
                    For more information, see /etc/sysctl.d/10-ptrace.conf

            Faire  passer le  paramètre  `kernel.yama.ptrace_scope`  à 0  dans
            `/etc/sysctl.d/10-ptrace.conf`  puis recharger  la config'  du noyau
            via :

                    sysctl -p /etc/sysctl.d/10-ptrace.conf
                           │
                           └ load in sysctl settings from the file specified

            ... ou peut-être:

                    service procps start

            Cette dernière commande est donnée dans `/etc/sysctl.d/README`.

##
# Configuration
## Options serveur

    buffer-limit 10

            Configure le nb maximum de buffers mémorisés par tmux.

            Les buffers tmux sont mémorisés sous forme de stack.
            Une fois le nb max de buffers atteint, la prochaine fois qu'on copie du texte,
            le dernier buffer de la pile est supprimé pour faire de la place.


    default-terminal screen

            Configure screen comme étant le terminal par défaut pour les nouvelles fenêtres créées.

            Pour que tmux fonctionne correctement, il faut que la valeur soit `screen`, `tmux` ou
            une forme dérivée de ces dernières.

            Il est probable que la valeur par défaut de cette option soit dérivée de `$TERM`.


    escape-time 0

            Configure le temps en millisecondes pendant lequel tmux attend, après avoir reçu un
            caractère escape, pour déterminer s'il fait partie d'une touche fonction (pex F1) ou
            d'une séquence de touches tapées par l'utilisateur.

            Par défaut `escape-time` vaut 500ms.

            Qd cette valeur est >0 on peut expérimenter du lag dans Vim chaque fois qu'on tape
            Escape.  En effet, tmux "retient" escape, le temps défini par l'option, avant de l'envoyer
            à Vim.


    exit-unattached [on | off]

            Si l'option est activée, le serveur s'arrête dès qu'il n'y a plus aucun client attaché.


    focus-events [on | off]

            Si l'option est activée, et que le terminal supporte les évènements focus, tmux demande
            à ce dernier de les lui envoyer pour les passer aux applications qui tournent à l'intérieur.

            Après avoir changé cette option, pour qu'elle prenne effet dans un client, il faut
            détacher et réattacher ce dernier.


    history-file path/to/file

            Si la valeur n'est pas vide, l'historique des commandes tmux exécutées sera écrit
            dans le fichier `path/to/file` qd le serveur s'arrêtera, et chargé qd il démarrera.


    message-limit 50

            Configure le nombre de messages d'informations mémorisés dans le log de messagerie
            de chaque client.

            Valeur par défaut:    100

## Options fenêtres

    allow-rename [on | off]

            Autorise les programmes à renommer la fenêtre en utilisant une séquence d'échappement
            (\ek...\e\\).

            Activée par défaut.


    automatic-rename [on | off]

            Qd cette option est activée, tmux renomme automatiquement une fenêtre en utilisant
            le format spécifié dans l'option `automatic-rename-format`.

            L'option est ignorée lorsqu'on utilise la commande `new-window`, `new-session` ou
            `rename-window`, et qu'on spécifie un nom de fenêtre.


    automatic-rename-format my_format

            Le format de nom à utiliser, si l'option `automatic-rename` est activée, et que tmux doit
            renommer une fenêtre.


    clock-mode-colour green

            Configure la couleur de l'horloge (pfx t) comme étant verte.


    clock-mode-style [12 | 24]

            Configure le format de l'horloge comme étant 12h ou 24h.


    force-height 12
    force-width 34

            Empêche tmux de redimensionner une fenêtre en utilisant:

                    - une hauteur supérieure à 12
                    - une largeur "            34

            Par défaut, ces options ont des valeurs nulles, ce qui signifie que tmux ne connaît
            aucune limite qd il doit redimensionner une fenêtre.

            Attention, ne s'applique pas aux panes à l'intérieur d'une fenêtre, mais bien à la fenêtre
            elle-même.

            Qd on change une de ces valeurs, l'effet est immédiat, la fenêtre est redimensionnée.
            Mais pas le terminal qui l'affiche.
            Qu'affiche le terminal dans la partie désormais vacante? Des points.


    main-pane-height 12
    main-pane-width 34

            Configure la hauteur/largeur du pane principal (en haut/à gauche), qd tmux organise les
            panes de la fenêtre avec le layout `main-horizontal` / `main-vertical`.

            Pour rappel, tmux dispose de plusieurs layouts prédéfinis, qu'on peut:

                    - sélectionner via la commande `select-layout`
                    - alterner via `next-layout` (associée à `pfx + Escape`; custom)

            Dans les layouts `main-horizontal` et `main-vertical`, la 1e fenêtre est la principale
            et occupe:

                    - toute la largeur de l'écran en haut
                    - toute la hauteur de l'écran à gauche


    mode-style my_style

            Configure l'apparence de l'indicateur tmux affichant le nb de lignes présentes
            dans le scrollback buffer qd on passe en mode copie.


    monitor-activity [on | off]

            Surveille l'activité dans la fenêtre.
            Une fenêtre surveillée, et qui connaît une certaine activité, voit la couleur de son nom
            et celle de son fond inversées.


    monitor-silence 42

            Dès que la fenêtre est inactive pendant plus de 42 secondes, tmux met en surbrillance
            le nom de la fenêtre dans la status line.

            Par défaut, cette option vaut 0, ce qui signifie que l'inactivité de la fenêtre n'est
            pas surveillée.


    other-pane-height 12
    other-pane-width  34

            Qd on utilise le layout `main-horizontal`, configure 42 comme étant la hauteur des autres
            panes (!= principal).

            Si `main-pane-height` et `other-pane-height` sont tous deux configurés, et que leur somme
            est inférieure à la hauteur de l'écran, la hauteur du pane principal augmentera pour compenser.
            En revanche, si la somme est supérieure, c'est la hauteur des autres panes qui sera réduite.

            Par défaut cette option vaut 0, ce qui signifie qu'elle est désactivée.

            `other-pane-width` est une option similaire qui contrôle la largeur des autres panes
            qd on utilise le layout `main-vertical`.


    pane-border-format my_format

            Configure le texte à afficher dans la status line d'un pane, si elle est activée.


    pane-border-status [off | top | bottom]

            Désactive la status line des panes (off), ou l'active en haut (top), ou en bas (bottom).


    remain-on-exit [on | off]

            A window with this  flag set is not destroyed when the program  running in it exits.  The
            window may be reactivated with the respawn-window command.


    synchronize-panes [on | off]

            Duplicate input to any  pane to all other panes in the same  window (only for panes that
            are not in any special mode).


    window-active-style my_style

            Configure le style du pane actif (!= fenêtre active).


    window-status-activity-style style

            Set status line style for windows with an  activity alert.  For how to specify style, see
            the message-command-style option.


    window-status-current-style my_style

            Set status line style for the currently active window.  For how to specify style, see the
            message-command-style option.


    window-status-last-style my_style

            Set status  line style for  the last active  window.  For how  to specify style,  see the
            message-command-style option.


    window-status-separator string

            Sets the  separator drawn between windows  in the status  line.  The default is  a single
            space character.


    window-status-style my_style

            Set  status  line  style for  a  single  window.  For  how  to specify  style,  see  the
            message-command-style option.


    window-style my_style

            Set the  default window style.  For  how to specify style,  see the message-command-style
            option.


    wrap-search [on | off]

            Qd l'option est activée, une recherche bouclera à la fin/début du contenu du pane.

            Activée par défaut.

## Options sessions

    assume-paste-time milliseconds

            If keys  are entered  faster than  one in milliseconds,  they are  assumed to  have been
            pasted rather  than typed and tmux  key bindings are  not processed.  The default  is one
            millisecond and zero disables.


    base-index index

            Set the base index  from which an unused index should be searched  when a new window is
            created.  The default is zero.



    default-shell path

            Specify the  default shell.  This  is used as  the login shell  for new windows  when the
            default-command option  is set to empty,  and must be  the full path of  the executable.
            When started  tmux tries to  set a default  value from the  first suitable of  the SHELL
            environment variable, the shell returned by  getpwuid(3), or /bin/sh.  This option should
            be configured when tmux is used as a login shell.


    destroy-unattached [on | off]

            If enabled and the session is no longer attached to any clients, it is destroyed.


    display-panes-active-colour colour

            Set the colour  used by the display-panes  command to show the indicator  for the active
            pane.


    display-panes-colour colour

            Set the  colour used by  the display-panes command to  show the indicators  for inactive
            panes.


    display-panes-time time

            Set the time in milliseconds for which the indicators shown by the display-panes command
            appear.


    key-table key-table

            Set the default key table to key-table instead of root.


    lock-after-time number

            Lock the session (like the lock-session command) after number seconds of inactivity.  The
            default is not to lock (set to 0).


    lock-command shell-command

            Command to run when locking each client.  The default is to run lock(1) with -np.


    message-command-style my_style

            Cette option permet de modifier l'apparence de la ligne de commande tmux lorsqu'on
            utilise les raccourcis Vim au lieu d'emacs pour l'éditer, et qu'on est en mode normal.
            C'est-à-dire après avoir appuyé sur Escape.

            ’my_style’ doit être une liste d'attributs séparés par des virgules.
            Un attribut peut être ’bg=colour’, ’fg=colour’.

            ’colour’ peut être:

                    - black
                    - red
                    - green
                    - yellow
                    - blue
                    - magenta
                    - cyan
                    - white
                    - aixterm
                    - brightred
                    - brightgreen
                    - bright...
                    - colour0
                    - ...
                    - colour255
                    - default
                    - #{6 digits hex code}

            Un attribut peut également être:

                    - bold
                    - bright
                    - default
                    - dim
                    - underscore
                    - blink
                    - reverse
                    - hidden
                    - italics

            On peut également préfixer le nom d'un attribut avec ’no’.
            Dans ce cas il est désactivé au lieu d'être activé.

            Quelques exemples de valeurs possibles pour ’my_style’:

                    fg=yellow,bold,underscore,blink

                    bg=black,fg=default,noreverse

            Pour simplement ajouter un attribut à ’my_style’, et non remplacer ce dernier entièrement,
            bien penser à passer le flag `-a` (append) à la commande `set-option`.

                                     NOTE:

            La syntaxe de ’my_style’ doit être utilisée pour configurer d'autres options:

                    - message-style                   ligne de commande

                      (session)

                    - mode-style                      indicateur en mode copie

                      (fenêtre)

                    - pane-active-border-style        frontières du pane actif
                      pane-border-style               "          des autres panes
                                                      seul `fg` et `bg` sont pris en compte
                      (fenêtre)

                    - status-left-style               style à appliquer à la partie gauche/droite/centrale
                      status-right-style              de la status line
                      status-style

                      (session)

                    - window-active-style             pane actif

                      (fenêtre)

                    - window-status-activity-style    mise en surbrillance du nom d'une fenêtre active
                    - window-status-current-style     "                           de la fenêtre courante
                    - window-status-last-style        "                           de la fenêtre précédente

                      (fenêtre)

                    - window-style                    panes inactifs

                      (fenêtre)

            Elle peut aussi être utilisée dans une séquence de caractères spéciaux (#[...]) au sein
            de la chaîne donnée en valeur aux options:

                    - status-left     info à afficher dans la partie gauche de la status line
                      status-right    "                              droite "

                      (session)

            Exemple:    #[fg=red,bright]


    message-style my_style

            Configure l'apparence de la ligne de commande.

            On peut aussi configurer les attributs ’fg’ et ’bg’ de l'option `message-style` via
            les “pseudo-options“:

                    - message-fg
                    - message-bg

            Il ne s'agit pas de vraies options.  Elles ne sont pas listées qd on tape `show-options -g`.
            Elles ne servent qu'à permettre de modifier les attributs ’fg’ et ’bg’ de `message-style`,
            sans devoir redéfinir tous les autres attributs.


    status [on | off]

            Show or hide the status line.


    status-left-length length

            Set the maximum length of the left component of the status bar.  The default is 10.


    status-left-style my_style

            Set the style  of the left part  of the status line.  For how to specify  style, see the
            message-command-style option.


    status-position [top | bottom]

            Set the position of the status line.


    status-right-length length

            Set the maximum length of the right component of the status bar.  The default is 40.


    status-right-style my_style

            Set the style  of the right part of the  status line.  For how to specify  style, see the
            message-command-style option.


    word-separators string

            Sets the session's conception of what characters are considered word separators, for the
            purposes  of the next and  previous word commands in  copy mode.  The default  is ‘
            -_@’.

##
# Layout

Tous les raccourcis qui suivent doivent être précédés de pfx.

    Esc

            Change le layout des panes.
            Alterne entre plusieurs layouts préexistants.


    C-o    M-o

            Rotation des panes dans le sens horaire ou anti-horaire.


    x    X

            Échange la position du pane actif avec celle du précédent / suivant.


    T

            Convertit le pane en fenêtre.

    *

            Affiche les n° des panes.


    join -s session:window.pane
    C-j

            Amène le pane de la fenêtre d'une session arbitraire dans la fenêtre courante.
            Pour se référer à une fenêtre, on peut utiliser indifféremment un index ou un nom.

            Mnémotechnique:    -s = src-pane
                                j = vers le bas (reçoit)


    join -t session:window
    C-k

            Envoit le pane courant dans la fenêtre d'une session.

            Mnémotechnique:    -t = target-pane
                                k = vers le haut (envoie)
            la fenêtre doit exister au préalable, elle ne peut pas être créée automatiquement


    d    D

            Ferme le pane / la fenêtre ayant le focus.

##
# Copier-Coller
## Modes

    copy_v    copy_Space
    copy_V

            depuis le mode copie, passer en mode visuel (characterwise / linewise)

            En réappuyant sur v / V, on redéfinit le début de la sélection à l'endroit où se trouve le curseur.


    copy_v r

            visual block

            En réappuyant sur r, on alterne entre mode visuel et mode visuel par bloc.


    copy_C-m    copy_q

            revenir au mode normal

## Copier avec la souris

Une copie à la souris pose 2 pbs :

1) tmux capture la copie dans un de ses buffers inaccessible aux autres applications.

Solution : on peut envoyer l'évènement 'copie avec la souris' directement à guake via le raccourci :

    shift + sélection souris + clic-droit + copy

2) dans guake via le raccourci précédent, si on a 2 panes adjacents (horizontalement),
la sélection d'une ligne complète avec la souris, va déborder sur plusieurs panes.

Solution : utiliser le raccourci guake suivant, qui réalise une sélection en bloc :

    ctrl + shift + sélection souris + clic-droit + copy

Une autre solution consiste à zoomer  temporairement le pane dans lequel on veut
copier  du  texte, puis  utiliser  le  précédent  raccourci (shift  +  sélection
souris).

Si  on n'utilise  pas guake,  on peut  aussi désactiver  temporairement le  mode
souris, le temps de copier, puis le réactiver via :

    pfx m
    pfx M

##
# Ouvrir
## des fichiers

    o

            en mode visuel, ouvrir le nom de fichier / url sélectionné avec le programme associé par défaut

    C-o

            en mode visuel, ouvrir le nom de fichier sélectionné avec l'éditeur par défaut


Ces raccourcis sont fournis par le plugin tmux-open :
<https://github.com/tmux-plugins/tmux-open>

On peut les modifier en écrivant dans `~/.config/tmux/tmux.conf` (pex):

    set-option -g @open        'x'
    set-option -g @open-editor 'C-x'

## des urls

    pfx u

            Visualiser les liens présents dans le pane.

Ce raccourci nécessite l'installation du paquet urlview et de l'addon tmux-urlview (pour la définition du hotkey).
https://github.com/tmux-plugins/tmux-urlview

On peut changer le raccourci en écrivant dans `~/.config/tmux/tmux.conf` (pex) :

        set-option -g @urlview-key 'x'

Remarques :
On peut se rendre directement à une url en tapant son n° d'index.
On peut éditer une url avant d'appuyer sur entrée.

Si une url est trop longue pour tenir sur une ligne, urlview ne retient que la 1e ligne,
ce qui rend le lien inexploitable à moins de l'éditer.

Les liens sont dépourvus de contexte.

##
# Raccourcis

    bind-key [-nr] [-t mode-table] [-T key-table] key command [arguments]
    bind

            Bind key key to command.  Keys are bound in a key table.  By default (without -T), the key
            is bound in the  prefix key table.  This table is used for  keys pressed after the prefix
            key (for  example, by default  ‘c’ is  bound to new-window  in the prefix  table, so
            ‘C-b c’ creates a  new window).  The root ta‐ ble is used  for keys pressed without
            the prefix key: binding ‘c’ to new-window  in the root table (not recommended) means
            a plain ‘c’ will create  a new window. -n is an alias for -T  root.  Keys may also be
            bound in custom key tables and the switch-client  -T command used to switch to them from
            a key binding.  The -r flag indicates this key may repeat, see the repeat-time option.

            If -t is present, key is bound in mode-table.

            To view the default bindings and possible commands, see the list-keys command.


    lsk -T prefix

            Affiche la table des raccourcis commençant par pfx.


    send-keys [-lMRX] [-N repeat-count] [-t target-pane] key ...
    send

            Send a  key or  keys to a  window.  Each  argument key is  the name of  the key  (such as
            ‘C-a’ or ‘npage’ ) to send; if the string is not recognised as a key, it is sent
            as a  series of  characters.  The -l  flag disables  key name lookup  and sends  the keys
            literally.  All arguments  are sent sequentially from  first to last.  The  -R flag causes
            the terminal state to be reset.

            -M passes through a mouse event (only valid if bound to a mouse key binding, see MOUSE SUPPORT).

            -X is  used to send a  command into copy  mode - see  the WINDOWS AND PANES  section. -N
            specifies a repeat count to a copy mode command.


    send-prefix [-2] [-t target-pane]

            Send the prefix key, or with -2 the secondary prefix key, to a window as if it was pressed.


    unbind-key [-an] [-t mode-table] [-T key-table] key
    unbind

            Unbind the command  bound to key. -n, -T and  -t are the same as for  bind-key.  If -a is
            present, all key bindings are removed.


    tmux allows a  command to be bound to most  keys, with or without a prefix  key.  When specifying
    keys, most represent themselves (for example ‘A’ to ‘Z’).  Ctrl keys may be prefixed with
    ‘C-’ or ‘^’, and Alt (meta) with  ‘M-’.  In addition, the following special key names
    are accepted: Up, Down,  Left, Right, BSpace, BTab, DC (Delete), End, Enter,  Escape, F1 to F12,
    Home, IC (Insert), NPage/PageDown/PgDn, PPage/PageUp/PgUp, Space, and Tab.  Note that to bind the
    ‘"’ or ‘'’ keys, quotation marks are necessary, for example:

            bind-key '"' split-window
            bind-key "'" new-window

##
# Commandes
## Navigation

    switch-client -p
    switch-client -n

            Naviguer entre les différentes sessions.


    choose-tree
    choose-window

    pfx s
    pfx w

            Sélectionne  une autre  session  / fenêtre  via  un menu.

            Espace  permet de  déplier l'affichage des fenêtres d'une session.
            Dans le menu des sessions, le symbole + devant le  nom d'une  session peut  être déplié
            via la  flèche droite,  afin de  se rendre spécifiquement dans une de ses fenêtres.


    select-window -t :=3
    pfx 3

    command-prompt -p index "select-window -t ':%%'"
    pfx ' 42


            Donne le focus à la fenêtre 3 / 42.
            Si l'index de la fenêtre est composé de plusieurs chiffres, seule la 2e syntaxe est possible.

## Divers

    show-messages [-JT] [-t target-client]
    showmsgs
    pfx !

Show client messages or server information.
Any messages displayed on the status line are saved in a per-client message log,
up to a maximum of the limit set by the message-limit server option.
With -t, display the log for target-client.
-J and -T show debugging information about jobs and terminals.

## Sessions

    a[ttach-session] -t foo

            Restaurer la session foo (n° ou nom).
            On dit aussi qu'on l'attache au terminal (en fait il s'agit de relancer un client tmux).


    copy-mode [-Meu] [-t target-pane]

            Enter copy mode.  The -u option scrolls one page up.  -M begins a mouse drag (only valid if bound to a
            mouse key binding, see MOUSE SUPPORT).  -e specifies that scrolling to the bottom of the history (to
            the visible screen) should exit copy mode.  While in copy mode, pressing a key other than those used
            for scrolling will disable this behaviour.  This is intended to allow fast scrolling through a pane's
            history, for example with:

                    bind PageUp copy-mode -eu


    detach
    pfx @

            se détacher de la session (tuer le client tmux)


    kill-session -t foo
    kill-window  -t foo
    kill-server

            Fermer la session `foo`, la fenêtre `foo`, le serveur tmux.


    next-layout [-t target-window]
    nextl

            Move a window to the next layout and rearrange the panes to fit.


    next-window [-a] [-t target-session]
    next

            Move to the next window in the session.  If -a is used, move to the next window with an alert.


    previous-window [-a] [-t target-session]
    prev

            Move to the previous window in the session.  With -a, move to the previous window with an alert.


    rename-session [-t target-session] new-name
    rename
    pfx $

            Rename the session to new-name.


    rename-window [-t target-window] new-name
    renamew
    pfx ,

            Rename the current window, or the window at target-window if specified, to new-name.

## Fenêtres

    kill-window [-a] [-t target-window]
    killw

Kill the  current window or  the window at  target-window, removing it  from any
sessions to which it is linked.
The `-a` option kills all but the window given with `-t`.

##
##
##
# Reference

[1]: $MY_WIKI/graph/tmux/transparent.pdf
