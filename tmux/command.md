# Parsing
## What is it?

The process during which tmux splits a command into its name and arguments.

##
## Why does `:confirm-before "display \\"` fail (while `:display "\\"` works)?

Because `display \\b` is parsed twice.

    :confirm-before "display \\"
    y
    Syntax error~

Once for `confirm-before`, the other for `display-message`.
After   the  parsing   of   `confirm-before`,  `\\`   becomes   `\`,  and   when
`display-message` parses  `\`, it raises an  error, because it's used  to remove
the special meaning of the following double quote.
As a result,  the string is unfinished,  because the last quote  doesn't end the
string; it's *included* in the string.

From `man tmux /COMMAND PARSING AND EXECUTION/;/twice`:

> This means that arguments can be parsed twice or more - once when the parent
> command (such as  if-shell) is parsed and again when  it parses and executes
> its command.

### More generally, what can you infer from this?

A command which is passed as an argument to another command is always parsed twice.

##
# Command queue
## What are the three steps which occur when I ask tmux to run commands?

1. the commands are parsed
2. they are added to the command queue
3. commands on the queue are executed in order

## How many command queues does tmux use?

One per tmux client.
Besides,  a global  command queue  – not  attached to  any client  – is  used on
startup for configuration files like `~/.tmux.conf`.

##
## What happens when the command `if-shell` parses its arguments?

It creates a new command which is inserted immediately after itself on the queue.

---

So for example, if the command queue contains:

    if 'true' { display one }
    display two

When `if` parses its arguments, it adds the command `display one` right after itself:

    if 'true' { display one }
    display one   <---
    display two

And *not* at the end of the queue:

    if 'true' { display one }
    display two
    display one   <---

### For which other commands is this also true?  (6)

Any command which accepts another tmux command as argument:

   - `choose-buffer`
   - `choose-client`
   - `choose-tree`
   - `command-prompt`
   - `confirm-before`
   - `display-panes`

###
## Which commands stop the execution of the commands on the queue?  (3)

`if`, `run` and `displayp`.

    # test is not printed until resp. if, run, displayp is finished
    $ tmux if 'sleep 1' '' \; display test
    $ tmux run 'sleep 1' \; display test
    $ tmux displayp -d0 \; display test
    test~

Unless you pass them the `-b` flag:

    $ rm /tmp/file ; tmux if -b 'sleep 1' 'run "echo test >/tmp/file"' ; cat /tmp/file
    $ rm /tmp/file ; tmux run -b 'sleep 1 ; echo test >/tmp/file' ; cat /tmp/file
    $ rm /tmp/file ; tmux displayp -b -d0 'run "echo test >/tmp/file"' ; cat /tmp/file
    cat: /tmp/file: No such file or directory~

---

The execution is blocked until the whole command has been run; this includes the
tmux command passed as argument:

    $ tmux if true 'run "sleep 3"' \; display test

Here, you'll have to wait 3 seconds  before 'test' is displayed, even though the
shell command `true` is instantaneous.

---

`displayp` blocks until you press a key.
From `man tmux /COMMAND PARSING AND EXECUTION/;/subsequent`:

> Commands like if-shell, run-shell and display-panes stop execution of subsequent
> commands on the  queue until something happens - if-shell  and run-shell until a
> shell command finishes and display-panes until a key is pressed.

### Which commands do *not*?

All the other ones.
This includes `copy-pipe` and its variants.

> nicm │ tmux only guarantees a command is started, it doesn't wait for it
> ...
> nicm │ someone talked about making copy-pipe also block but we didn't do it

---

As an example:

    $ tmux pipep -t =study:3.2 -I "echo 'ls'; sleep 60" \; display test

Tmux must  run `$  echo 'ls'; sleep  60` to  get its output,  and then  type the
latter in the pane `study:3.2`.
Afterward, it must display 'test'.
If `pipep` blocked, 'test' would be displayed opened after 60s, but in practice,
it's displayed immediately.

`neww` doesn't block either:

    # test is printed in the status line immediately, not after 3 seconds
    $ tmux neww 'sleep 3' \; display test
    test~

Same thing for `splitw`, `new` and `confirm`:

    $ tmux splitw 'sleep 3' \; display test
    $ tmux new -d 'sleep 3' \; display test
    $ tmux confirm 'display' \; display test

#### When does this have an unexpected consequence?

When a command A runs another command B, and then you run yet another command C.
There's no guarantee that B finishes before C, even though it's written first.

In fact, as  soon as tmux has started  A, it starts C; it  probably doesn't even
wait to start B.
B is  started later, once  A has processed  its arguments, and  inserted another
command on the queue.

##
## What is wrong in the command `$ tmux if -b 'sleep 3' 'run "sleep 3"'`?

`run-shell` should have been passed the `-b` flag.

Otherwise, you'll  get back the  shell prompt  immediately, which will  make you
think that you can interact with your shell as usual.
But after 3 seconds, all your keypresses will be blocked (!= lost) by `run-shell`.
Tmux won't respond anymore, until `run` has finished its job.
Afterward, tmux will relay to the foreground process any key pressed while `run`
was running.

> If you run with if-shell -b then the command is run in the context of the
> attached client, not the command client you started by typing "tmux if ..."
> into the shell. So run-shell will block the attached client not the command
> client. That's why you get the shell prompt back immediately.

<https://github.com/tmux/tmux/issues/1843#issuecomment-512512304>

All of this is confusing and can lead to undesired interactions.
Bottom line: when you pass `-b` to `if`, pass `-b` to `run` too.

Anyway, I don't think it makes much sense to pass `-b` to `if` but not to `run`.

##
# copy-pipe
## The rhs of my key binding is `copy-pipe 'shell_cmd' \; tmux_cmd`?  Is `shell_cmd` run first or `tmux_cmd`?

`shell_cmd`  is forked,  so  there is  no  way to  tell  whether `shell_cmd`  or
`tmux_cmd` will be run first.

Therefore, it's entirely possible for `tmux_cmd` to be run *before* `shell_cmd`.

---

    $ tmux bind -T copy-mode-vi x \
      send -X copy-pipe-and-cancel "tmux deleteb \\; run 'echo test >/tmp/file'" \\\; \
      deleteb

    # empty the stack of buffers
    $ tmux lsb -F '#{buffer_name}' | xargs -I{} tmux deleteb -b {}

    # enter copy mode and press x

    $ cat /tmp/file
    cat: /tmp/file: No such file or directory~

When we pressed  `x`, `/tmp/file` was not created, because  the previous command
in the rhs – `tmux deleteb` – failed.

It failed because:

   1. we've emptied the stack of buffers

   2. the second `deleteb` was run **before** the first one

   3. the second `deleteb` has removed the buffer created by `copy-pipe-and-cancel`

   4. the first `deleteb` can't remove any buffer, because there's no buffer on
      the stack anymore

   5. tmux stops processing commands as soon as one of them fails (here the first `deleteb`)

`2.` shows that `tmux_cmd` (here `deleteb`) can be run *before* `shell_cmd` (here `tmux deleteb ...`).

---

Note that even though `tmux deleteb ...` doesn't read its stdin, the key binding
is still syntactically correct.
So don't think that `/tmp/file` was not created because of some syntax error.
You can  check that the syntax  is valid by  replacing any of the  two `deleteb`
with `display -p foo`:

    $ tmux bind -T copy-mode-vi x \
      send -X copy-pipe-and-cancel "tmux display -p foo \\; run 'echo test >/tmp/file'" \\\; \
      deleteb

    $ tmux bind -T copy-mode-vi x \
      send -X copy-pipe-and-cancel "tmux deleteb \\; run 'echo test >/tmp/file'" \\\; \
      display -p foo

In both cases, if you run these commands afterward:

    # empty the stack of buffers
    $ tmux lsb -F '#{buffer_name}' | xargs -I{} tmux deleteb -b {}

    $ rm /tmp/file

    # enter copy mode and press x

    $ cat /tmp/file
    test~

You'll see that `/tmp/file` is correctly created.

### How to make sure `shell cmd` is run before `tmux_cmd`?

Move it inside the argument passed to `copy-pipe`.

    copy-pipe 'shell_cmd ; tmux tmux_cmd'

##
## tmux buffer
### Will the next key binding work as expected?

    $ tmux bind -T copy-mode-vi x send -X copy-pipe-and-cancel 'cat >/tmp/file' \\\; deleteb
                                                                                     ^^^^^^^

↣
Yes, you can remove  the tmux buffer as soon as you want,  it won't interfere in
the piping process.
This is because the buffer which is piped to the shell command has nothing to do
with the tmux buffer which is put on the stack.
↢

#### How about this one?

    $ tmux bind -T copy-mode-vi x send -X copy-pipe-and-cancel 'cat >/tmp/file ; tmux deleteb'

↣
No, you can't remove the buffer from the shell command passed to `copy-pipe`.
The buffer might not exist yet.

> nicm    the shell command is forked and the text is buffered to go to its stdin
>         before the new tmux buffer is created
> nicm    so there is no way to tell whether the buffer will exist
>         by the time the shell command starts reading the text

*This is not exactly what nicm said.*
*I've fixed what I think were a few typos.*
↢

#
# run-shell
## Where is `test` displayed when I run
### `run 'echo test'`?

In the current terminal.

### `run -b 'echo test'`?

In the current pane, in copy mode.

### `run -t :2 'echo test'`?

In the active pane of the second window, in copy mode.

### `run -b -t :2 'echo test'`?

In the active pane of the second window, in copy mode.

##
## In the shell command run by `run-shell`,
### why is `2>/dev/null` useless?

Because if the command fails, tmux will still print its exit status.

    $ tmux run 'not_a_command 2>/dev/null'
    'not_a_command 2>/dev/null' returned 127~

### can I include a format variable?

Yes:

    $ tmux run 'echo #I'
    1~

##
# Targetting
## What is an ID?

A number uniquely identifying a session, window or pane.
It remains unchanged for the whole life of the latter in the tmux server.

## Which prefix does tmux use for a session ID?  a window ID?  a pane ID?

    ┌─────────┬───┐
    │ session │ $ │
    ├─────────┼───┤
    │ window  │ @ │
    ├─────────┼───┤
    │ pane    │ % │
    └─────────┴───┘

## How to get a session ID?  window ID?  pane ID?

Use the format variables `#{session_id}`, `#{window_id}`, `#{pane_id}` in a format
passed to `display-message`, `list-sessions`, `list-windows` or `list-panes`.

You  can also  get the  id of  the current  pane by  inspecting the  environment
variable `$TMUX_PANE`.

##
## sessions
### Which kinds of values can I use for `target-session`?  (4)

An ID:

    $ tmux command -t '$123'
                      ^    ^
                      prevent the shell from trying to expand `$123` into an empty string (unset variable)

A name:

    $ tmux command -t 'mysession'

A name prefix:

    $ tmux command -t 'mysess'

An fnmatch(3) pattern matched against the session name:

    $ tmux command -t '*sess*'

###
### What should I always do when referring to a session or window via its name?

Prefix the name with `=`.

    $ tmux command -t '=mysession'
                       ^

    $ tmux command -t '=mysession:=mywindow'
                                  ^

#### Why?

Otherwise, the name you provide may be  interpreted as a name prefix, instead of
an exact name.

For example, suppose  that you have a session named  `mysession`, but no session
named `mysess`; you try to target `mysess`: tmux will target `mysession`.

This is because  tmux interprets `target-session` – with the  following order of
precedence, from highest to lowest – as:

   - an ID
   - a name
   - a name prefix
   - an fnmatch(3) pattern

It stops as soon as one interpretation succeeds.
So, even if matching `mysess` as a name fails, tmux still tries to match it as a
name prefix, which succeeds.

###
### I have two sessions named `a_sess_1` and `b_sess_2`.  What happens if I target `*sess*`?

It's an error.

    $ tmux new -d -s a_sess_1 \; new -d -s b_sess_2
    $ tmux lsw -t '*sess*'
    can't find session: *sess*~

---

The issue is not due to the wildcards `*`, it's due to several sessions matching
the pattern;  if your  pattern only  matches one session,  then, there'll  be no
error:

    $ tmux lsw -t 'a*sess*'
    1: zsh* (1 panes) [80x24] [layout 2ce7,80x24,0,0,155] @56 (active)~

##
## windows
### Which kinds of values can I use for `target-window`, `src-window` and `dst-window`?  (6)

Any value must follow the syntax `session:window`.

`session` can have any of the four  kinds of values described earlier (ID, name,
name prefix, fnmatch(3) pattern).

`window` can have any of the next six kinds of values:

   1. a special token among `^`, `$`, `!`, `+`, `-`
   2. a numerical index (e.g. `mysession:1`)
   3. an ID (e.g. `mysession:@1`; although, if you have an ID, you probably don't need the session name: `:@1`)
   4. a name (e.g. `mysession:mywindow`)
   5. a name prefix (`mysession:mywin`)
   6. an fnmatch(3) pattern matched against the window name

### What is the meaning of the special tokens in the set `[$^!+-]`?  What's their long forms?

    ┌────────────┬───────────────────────┬──────────────────────────────────────┐
    │ long form  │ single-character form │               meaning                │
    ├────────────┼───────────────────────┼──────────────────────────────────────┤
    │ {start}    │           ^           │ the lowest-numbered window           │
    ├────────────┼───────────────────────┼──────────────────────────────────────┤
    │ {end}      │           $           │ the highest-numbered window          │
    ├────────────┼───────────────────────┼──────────────────────────────────────┤
    │ {last}     │           !           │ the last (previously current) window │
    ├────────────┼───────────────────────┼──────────────────────────────────────┤
    │ {next}     │           +           │ the next window by number            │
    ├────────────┼───────────────────────┼──────────────────────────────────────┤
    │ {previous} │           -           │ the previous window by number        │
    └────────────┴───────────────────────┴──────────────────────────────────────┘

###
### Which window does tmux target if I use an empty window name?

The next unused index if appropriate, e.g.:

    $ tmux neww -a -t :.

Otherwise the current window in the current session:

    $ tmux renamew -t :. test

###
### How to target the second window after the current one by numer?

Use `+` and a numerical offset:

    $ tmux command -t :+2
                        ^

###
### I have a window named `1`, but whose index is not 1, and a window of index 1 whose name is `mywindow`.
#### What's the output of `$ tmux display -p -t :1 '#W'`

`mywindow`.

##### Why?

Because, in  `-t :1`, tmux tries  to interpret `1` as  each of the six  kinds of
values listed earlier in the given order of precedence.
And in this order, a numerical index has priority over a name.

####
## panes
### Which kinds of values can I use for `target-pane`, `src-pane` and `dst-pane`?  (3)

It must follow the syntax `session:window.pane`.
`session` and `window` can have any of the kinds of values described earlier.

`pane` can be a pane index, a pane ID, or a special token.

### What is the meaning of the special tokens in the set `[!+-]`?  What's their long forms?

    ┌────────────┬───────────────────────┬───────────────────────────────────┐
    │ long form  │ single-character form │              meaning              │
    ├────────────┼───────────────────────┼───────────────────────────────────┤
    │ {last}     │           !           │ the last (previously active) pane │
    ├────────────┼───────────────────────┼───────────────────────────────────┤
    │ {next}     │           +           │ the next pane by number           │
    ├────────────┼───────────────────────┼───────────────────────────────────┤
    │ {previous} │           -           │ the previous pane by number       │
    └────────────┴───────────────────────┴───────────────────────────────────┘

###
### How to target the third pane after the current one by numer?

Use `-` and a numerical offset:

    $ tmux command -t :.-3
                         ^

###
### How to refer to the
#### top/bottom/leftmost/rightmost pane?

In the `pane` field of `session:window.pane`, use one of these special tokens:

    ┌──────────┬────────────────────┐
    │ {top}    │ the top pane       │
    ├──────────┼────────────────────┤
    │ {bottom} │ the bottom pane    │
    ├──────────┼────────────────────┤
    │ {left}   │ the leftmost pane  │
    ├──────────┼────────────────────┤
    │ {right}  │ the rightmost pane │
    └──────────┴────────────────────┘

#### top-left/top-right/bottom-left/bottom-right pane?

    ┌────────────────┬───────────────────────┐
    │ {top-left}     │ the top-left pane     │
    ├────────────────┼───────────────────────┤
    │ {top-right}    │ the top-right pane    │
    ├────────────────┼───────────────────────┤
    │ {bottom-left}  │ the bottom-left pane  │
    ├────────────────┼───────────────────────┤
    │ {bottom-right} │ the bottom-right pane │
    └────────────────┴───────────────────────┘

#### pane above/below the active pane?  pane to the left/right of the active pane?

    ┌────────────┬──────────────────────────────────────────┐
    │ {up-of}    │ the pane above the active pane           │
    ├────────────┼──────────────────────────────────────────┤
    │ {down-of}  │ the pane below the active pane           │
    ├────────────┼──────────────────────────────────────────┤
    │ {left-of}  │ the pane to the left of the active pane  │
    ├────────────┼──────────────────────────────────────────┤
    │ {right-of} │ the pane to the right of the active pane │
    └────────────┴──────────────────────────────────────────┘

###
### Which pane is targeted if I use an empty `pane` field?

The currently active pane in the specified window.

##
## clients
### Which value can I use for `target-client`?

The pty(4) file to which the client is connected.
For example, `/dev/pts/1`.

##
# Pane
## Can a pane have a title?  A name?

A pane can only have a title.

## Can a window have a title?  A name?

A window can have a name.
It can't have its own title, but it automatically gets the one of its active pane.

From `man tmux /NAMES AND TITLES`:
> Windows themselves do not have titles - a window's title is the title of its active pane.

###

## How to get the list of all the panes in the current session?

    $ tmux lsp -s

This is due to what seems to be an undocumented effect of `-s`.
Indeed, `-s` is meant to change the meaning of `-t`:

> If -s is given, target is a session (or the current ses‐ sion).

But there's no `-t` here.
I guess that in the absence of `-t`, when you use `-s`, tmux assumes `-t ''`.

    $ tmux lsp -s -t ''

And an empty session name probably refers to the current session.

##
## How to set the title of
### the current pane?  (2)

    $ printf '\033]2;my title\033\\'

    $ tmux selectp -T 'my title'

### the pane whose id is `%123`?

    $ tmux selectp -t %123 -T 'my title'

###
## What is an empty pane?

A pane which was not started to run a command, but simply to print some text.

---

An empty pane is characterized by a 0 pid:

    :display -p '#{pane_pid}'
    0~

Although weirdly enough, `:display -p '#{pane_current_command}'` still outputs `zsh`.

### How to create a new one?

    $ tmux splitw ''
                  ^^

#### and make it print the output of a shell command (in a single command)?

    $ echo hello | tmux splitw -I
                               ^^
                               create an empty pane and forward any output from stdin to it

###
### Why do `$ tmux splitw ''` and `$ tmux splitw` behave differently?

*Without* any `shell-command` argument, after  creating a new pane, `:splitw` runs
the command set by the `'default-command'` option.
The default  value of  the latter is  an empty string,  which instructs  tmux to
create a login shell using the value of the `'default-shell'` option.
We use the value `/bin/zsh`.

OTOH, if you pass  an *explicit* empty string to `:splitw`,  in effect, you tell
tmux to ignore `'default-command'`.

---

Btw, don't conflate  the empty string passed to `:splitw`  with the empty string
which is assigned by default to `'default-command'`.
They are used in different contexts, and so can have different meanings.

###
### How to forward the output of a shell command to an existing empty pane?

Pass the `-I` flag to `display-message`.

    $ echo hello | tmux splitw -dI
    $ echo world | tmux display -I -t :.2
                                 ^

### How to send some text to an empty pane from Vim?

Create the empty pane, and save its id.
Then use this id to send your text.
Use the second optional argument of `system()` to pass the text to the stdin of `tmux(1)`.

    :let pane_id = system('tmux splitw -PF "#D" -dI', "hello\n")[:-2]
    :call system('tmux display -t ' . pane_id . ' -I', "world\n")
                                                             ^^
                                                             don't forget to add a newline,
                                                             if you want the next text
                                                             to be printed on a different line

##
# Marked pane
## What is the marked pane?

The default target for `-s` when passed to `join-pane`, `swap-pane` and `swap-window`.
It will be used in the place of `src-pane` or `src-window` in the absence of any
explicit value.

There can only be 1 marked pane per tmux server.

##
## How to set the current pane as the marked pane?

Use the `select-pane` command:

    $ tmux selectp -m
                   ^^

### How to clear the mark?

    $ tmux selectp -M
                   ^^

##
## How to refer to the marked pane when I need to target it?

Use the special token `{marked}` or `~`.

---

    $ tmux bind C-z display -t'~' '#{pane_current_command}'

Mark a pane, focus a different one, and press prefix + `C-z`.
Tmux should print the command running in the marked pane, not in the current one.

##
# Input
## What does it mean to disable the input to a pane?

It means tmux won't send any key you press to the process running in that pane.

##
## How to test whether the input is disabled in a pane?

Use the format variable `pane_input_off`.
It's replaced by 1 iff the input is disabled.

##
## How to disable/enable input to the
### current pane

    $ tmux selectp -d
    $ tmux selectp -e

### pane above/below/to the right/to the left?

Pass the  `-d` flag (disable) or  `-e` flag (enable),  as well as either  of the
`-l` (last), `-U` (up), `-D` (down), `-L` (left), `-R` (right), flags, to `selectp`.

For example, to disable the input in the pane above:

    $ tmux selectp -Ud

And to enable the input in the last pane:

    $ tmux selectp -le

---

Note that these commands don't change the active pane.

### previously selected pane?  (2)

     $ tmux last-pane -d
     $ tmux selectp -ld

     $ tmux last-pane -e
     $ tmux selectp -le

##
## How to make tmux automatically duplicate the input I send to a pane, to all the other panes in the same window?

Set the window option 'synchronize-panes':

    $ tmux set -w synchronize-panes on

### In which panes will tmux *not* duplicate my input?

Any pane which is in a mode.

Besides, if  your active  pane is  in a  mode, the  input you  send will  not be
duplicated *anywhere*.

##
## How to make tmux prompt me for some input, then include it in an arbitrary command and run it?

Use `command-prompt`:

    $ tmux command-prompt -p '(my prompt)' 'display %%'

The placeholder `%%` will be replaced by the user input.

### How to prepopulate the command-line with some text?

Use the `-I` flag:

    $ tmux command-prompt -I 'my default input' -p '(my prompt)' 'display %%'
                          ^^^^^^^^^^^^^^^^^^^^^

###
### How to limit the user input to only
#### one keypress?

Use the `-1` flag:

    $ tmux command-prompt -1 -p '(my prompt)' 'display %%'
                          ^^

If you press `abc`,  tmux will only display `a`, then it will  sends `bc` to the
command running in the current pane.

#### a number?

Use the `-N` flag:

    :bind -Tcopy-mode-vi  C-z  command-prompt -N {send -N '%%'}
                                              ^^

As soon as you press a non-numeric key:

   1. the user input is terminated
   2. the template command is run
   3. the non-numeric key is sent to the command running in the current pane

###
### How to make tmux
#### escape double quotes in the user input?

Use the `%%%` placeholder instead of `%%`.

    :command-prompt "display %%%"
    # press a"b
    a"b~

This doesn't seem to escape single quotes though:

    :command-prompt "display %%%"
    # press a'b
    Syntax error~

#### prompts me several times?

Pass a comma separated list of prompts to `-p`:

    $ tmux command-prompt -I 'my input1,my input2' -p '(my prompt1),(my prompt2)' 'display "%1 and %2"'
                                                                   ^^^^^^^^^^^^^

If you press Enter twice, without changing the default inputs, the command will output:

    my input1 and my input2~

`%1` and `%2` will be replaced with respectively the first and second user input.
You're limited to 9 user inputs, so you can only go up to `%9`.

Note that `-I` is optional; only `-p` is required to get several prompts.

#### prompt me in an arbitrary tmux client?

Use the `-t` flag,  followed by the path to the pty(4) file  to which the client
is connected:

    $ tmux command-prompt -t /dev/pts/123  'display "%%%"'
                          ^^^^^^^^^^^^^^^

#### run the command *every time* I press a key?  (not just once when I press Enter)

Use the `-i` flag (i for interactive?):

                    vv
    :command-prompt -i {run 'echo "%%%" >>/tmp/log'}
    # press a, then b, then c
    $ cat /tmp/log
    =a~
    =ab~
    =abc~

##
### What happens if I don't provide
#### a prompt (no `-p '...'` argument)?

Tmux still prompts  you for your input, and the  prompt (!= command-line) prints
the name of the command used in the template (inside parentheses).

For example:

    $ tmux command-prompt 'display "%%"'

This command prompts  you for your input, and the  text `(display)` is displayed
in the prompt.

#### a command to run (no `template` argument)?

Tmux will try to run the first word in your input.
So, for  example, if  you've passed `my  default input` to  `-I`, and  you don't
alter it  (immediately press Enter),  then tmux would  try to run  the (unknown)
command `my`.

#### a prompt nor a command to run?

The tmux  prompt will be opened  (`:`), and possibly prepopulated  with the text
provided by `-I`.

###
### What's the difference between `%%` and `%1`?

Tmux replaces only the first occurrence of `%%` with the user input.
OTOH, it replace *all* occurrences of `%1` with the user input.

### Which pitfall should I avoid when combining the `-p` flag with another flag?

Make sure to write `-p` at the end.

Otherwise, the other flag(s) would be interpreted as the text to write in the prompt.

For example, combined with `-1`, this would either raise an error:

    $ tmux command-prompt -p1 '(my prompt)' 'display "%%%"'
    usage: command-prompt [-1Ni] [-I inputs] [-p prompts] [-t target-client] [template]~

... or `-1` would not limit the user  input to 1 keypress, but instead simply be
written in the prompt:

    $ tmux command-prompt -p1 'display "%%%"'

The same is true for other combinations of flags with `-p`; don't write `-pN` but `-Np`, ...

#### Which flag is also concerned by this pitfall?

`-I`

Don't write `-I1` but `-1I`, and don't write `-IN` but `-NI`, etc.

##
# Miscellaneous
## I'm asking tmux to run a sequence of commands, but one in the middle will fail.  Which command(s) will tmux run?

If the  failure can be  detected at parse time  (i.e. the command  fails because
it's invalid) none.

Otherwise, all the commands which precede.

---

    $ tmux display -p foo \; not_a_cmd \; display -p bar 2>/dev/null
    ''~

Here,  no  command  is  run  because   tmux  has  detected  an  invalid  command
(`not_a_cmd`) at parse time.

    $ tmux lsb -F '#{buffer_name}' | xargs -I{} tmux deleteb -b {} ; \
      tmux display -p foo \; deleteb \; display -p bar 2>/dev/null
      foo~

And here, the first `display` is run because – at parse time – tmux was not able
to detect that `deleteb` would fail.
But at execution time, when `deleteb`  does fail, tmux stops processing the rest
of the commands.

## On which condition does `displayp` run its template argument?

The user  must press a numeric  key matching the index  of a pane opened  in the
current window.

    $ tmux displayp -d0 'display test'

## When does tmux display the output of a command in copy mode?

Whenever the command which outputs the text is not attached to a terminal.
This happens when it's run in the  background, from a key binding, or by another
command:

    $ tmux run -b 'echo test'

    $ tmux bind x display -p test
    # press 'x'

    $ tmux confirm 'display -p test'
    $ tmux choose-buffer 'display -p test'
    $ tmux display-panes 'display -p test'

## Which pitfall must I be aware of when I pass `-r` to `bind-key`?

If the lhs matches the start of another key binding installed in a program which
is sometimes run  in a tmux pane, there's  a risk for it to be  consumed by tmux
while you expected it to be sent to the program.

For example, if you have this tmux key binding:

    bind -r C-j resizep -D 5
         ^^

And this Vim mapping:

    nno <c-j> :wincmd j<cr>

When you  press `C-j` to  focus the  Vim split below,  there's a risk  that tmux
consumes the keypress and resizes the tmux pane instead.

The issue  will arise after you've  pressed *any* tmux key  binding defined with
`-r` (after  the prefix  key the  first time;  without the  prefix key  the next
times), but only for `'repeat-time'` ms.

##
## How to run a command in the context of each
### session?

    $ tmux run 'tmux #{S:my_tmux_command \; }'

### window of the current session?

    $ tmux run 'tmux #{W:my_tmux_command \; }'

For example, to make the clock be displayed in red in all windows of the current session:

    $ tmux run 'tmux #{W:set -w -t:#I clock-mode-colour red \; }'

### pane of the current window?

    $ tmux run 'tmux #{P:my_tmux_command \; }'

#### It doesn't work when I try to set an option with a comma-separated list of values!

Escape the commas by prefixing them with `#`.

    $ tmux run 'tmux #{P:set -w -t:#I window-style "none#,bg=#123456#,fg=#789abc" \; }'
                                                        ^           ^

---

Inside `#{S:}`, `#{W:}`, `#{P:}`, the comma has a special meaning.
It's  used to  separate 2  formats; the  second one  is used  for the  *current*
session/window/pane, while the first one is used for all the other ones.
You need to escape the commas to remove this special meaning.

##
##
##
# join-pane
## ?

>         join-pane [-bdhv] [-l size | -p percentage] [-s src-pane] [-t dst-pane]
>                       (alias: joinp)

> Split dst-pane, and move src-pane into the newly created pane.
> This can be used to reverse break-pane.
> The -b option causes src-pane to be joined to left of or above dst-pane.

> If -s is omitted and a marked pane is present (see select-pane -m), the marked
> pane is used rather than the current pane.

## Which pane is joined to the current window if I run `:join-pane -s 3`?

If the current  window contains a pane whose  index is 3, tmux will  try to join
it, which will obviously fail since it's *already* in the current window.

Otherwise, tmux will join  the pane of the 3rd window which was  the last one to
be active when we left the window.

Bottom line:  the rules can be  quite complex, so  to avoid any surprise,  be as
accurate as possible.

    # ✔
    $ tmux join-pane -s 3

    # ✔✔
    $ tmux join-pane -s :3

    # ✔✔✔
    $ tmux join-pane -s :3.4

    # ✔✔✔✔
    $ tmux join-pane -s mysession:3.4

In practice, I doubt you would want to join a pane which is in another session,
because usually sessions are built around very different themes (e.g. work vs fun).
So, you'll probably want to take the habit of using the third syntax:

    $ tmux join-pane -s :x.y

##
# break-pane

>         break-pane [-dP] [-F format] [-n window-name] [-s src-pane] [-t dst-window]

>               (alias: breakp)

> Break src-pane  off from  its containing window  to make it  the only  pane in
> dst-window.

> If -d is given, the new window does not become the current window.

> The -P option prints information about the new window after it has been created.
> By default, it uses the format ‘#{session_name}:#{window_index}' but a different
> format may be specified with -F.

#
# swap-pane

>         swap-pane [-dDU] [-s src-pane] [-t dst-pane]
>               (alias: swapp)

> Swap two panes.
> If -U is used and no source pane  is specified with -s, dst-pane is swapped with
> the previous pane (before it numerically); -D swaps with the next pane (after it
> numerically).
> -d instructs tmux not to change the active pane.

> If -s is omitted and a marked pane is present (see select-pane -m), the marked
> pane is used rather than the current pane.

# swap-window

>         swap-window [-d] [-s src-window] [-t dst-window]
>               (alias: swapw)

> This is similar to link-window, except  the source and destination windows are
> swapped.
> It is an error if no window exists at src-window.

> Like swap-pane, if -s is omitted and a marked pane is present (see select-pane
> -m), the  window containing the  marked pane is  used rather than  the current
> window.

#
# split-window

> split-window [-bdfhIvP] [-c start-directory] [-e environment] [-l size |
>         -p percentage] [-t target-pane] [shell-command] [-F format]
>               (alias: splitw)

> Create a new pane by splitting target-pane:  -h does a horizontal split and -v
> a vertical split; if neither is specified, -v is assumed.
> The -l and  -p options specify the size  of the new pane in  lines (for vertical
> split) or in cells (for horizontal split), or as a percentage, respectively.
> The  -b option  causes the  new  pane to  be created  to  the left  of or  above
> target-pane.
> The -f option  creates a new pane  spanning the full window height  (with -h) or
> full window width (with -v), instead of splitting the active pane.

> An empty shell-command ('') will create a pane with no command running in it.
> Output can be sent to such a pane with the display-message command.
> The -I flag  (if shell-command is not  specified or empty) will  create an empty
> pane and forward any output from stdin to it.
> For example:

>       $ make 2>&1|tmux splitw -dI &

> All other options have the same meaning as for the new-window command.

# link-window

>         link-window [-adk] [-s src-window] [-t dst-window]
>               (alias: linkw)

> Link the window at src-window to the specified dst-window.
> If dst-window is  specified and no such window exists,  the src-window is linked
> there.
> With -a, the window  is moved to the next index up  (following windows are moved
> if necessary).
> If  -k is  given and  dst-window exists,  it is  killed, otherwise  an error  is
> generated.
> If -d is given, the newly linked window is not selected.

# new-window

>         new-window [-adkP] [-c start-directory] [-e environment] [-F format] [-n
>         window-name] [-t target-window] [shell-command]
>               (alias: neww)

> Create a new window.
> With -a,  the new window  is inserted  at the next  index up from  the specified
> target-window, moving  windows up if  necessary, otherwise target-window  is the
> new window location.

> If -d is given, the session does not make the new window the current window.
> target-window represents the window to be  created; if the target already exists
> an error is shown, unless the -k flag is used, in which case it is destroyed.
> shell-command is the command to execute.
> If shell-command  is not specified, the  value of the default-command  option is
> used.
> -c specifies the working directory in which the new window is created.

> When the shell command completes, the window closes.
> See the remain-on-exit option to change this behaviour.

> -e takes  the form ‘VARIABLE=value' and  sets an environment variable  for the
> newly created window; it may be specified multiple times.

> The  TERM environment  variable must  be  set to  ‘screen' or  ‘tmux' for  all
> programs running inside tmux.
> New windows  will automatically have  ‘TERM=screen' added to  their environment,
> but care must  be taken not to reset  this in shell start-up files or  by the -e
> option.

> The  -P option  prints information  about  the new  window after  it has  been
> created.
> By default, it uses the format ‘#{session_name}:#{window_index}' but a different
> format may be specified with -F.

# new-session

>         new-session [-AdDEPX] [-c start-directory] [-F format] [-n window-name]
>         [-s session-name] [-t group-name] [-x width] [-y height]
>         [shell-command]
>               (alias: new)

> Create a new session with name session-name.

> The new session is attached to the current terminal unless -d is given.
> window-name and  shell-command are the name  of and shell command  to execute in
> the initial window.
> With -d, the initial  size comes from the global default-size  option; -x and -y
> can be used to specify a different size.
> ‘-' uses the size of the current client if any.
> If -x or -y is given, the default-size option is set for the session.

> If run from  a terminal, any termios(4) special characters  are saved and used
> for new windows in the new session.

> The  -A flag  makes  new-session behave  like  attach-session if  session-name
> already exists;  in this case,  -D behaves like  -d to attach-session,  and -X
> behaves like -x to attach-session.

> If -t is given, it specifies a session group.
> Sessions in  the same  group share  the same set  of windows  - new  windows are
> linked to  all sessions  in the group  and any windows  closed removed  from all
> sessions.
> The current and  previous window and any session options  remain independent and
> any session in a group may be killed without affecting the others.
> The group-name argument may be:

> 1.      the name of an existing group, in which case the new ses‐
>         sion is added to that group;

> 2.      the name of an existing session - the new session is
>         added to the same group as that session, creating a new
>         group if necessary;

> 3.      the name for a new group containing only the new session.

> -n and shell-command are invalid if -t is used.

> The  -P option  prints information  about the  new session  after it  has been
> created.
> By default, it uses the format  ‘#{session_name}:' but a different format may be
> specified with -F.

> If -E is used, the update-environment option will not be applied.

# respawn-pane

>         respawn-pane [-k] [-c start-directory] [-e environment] [-t target-pane] [shell-command]
>               (alias: respawnp)

> Reactivate a  pane in  which the  command has  exited (see  the remain-on-exit
> window option).
> If shell-command  is not given,  the command used when  the pane was  created is
> executed.
> The  pane must  be already  inactive,  unless -k  is  given, in  which case  any
> existing command is killed.
> -c specifies a new working directory for the pane.
> The -e option has the same meaning as for the new-window command.

# respawn-window

>         respawn-window [-k] [-c start-directory] [-e environment] [-t target-window] [shell-command]
>               (alias: respawnw)

> Reactivate a  window in which the  command has exited (see  the remain-on-exit
> window option).
> If shell-command is not  given, the command used when the  window was created is
> executed.
> The window  must be  already inactive,  unless -k  is given,  in which  case any
> existing command is killed.
> -c specifies a new working directory for the window.
> The -e option has the same meaning as for the new-window command.

# send-keys

`send-keys` has been updated recently.
Ignore the following text.
Update your tmux, and copy the new documentation.

---

    send-keys [-lMRX] [-N repeat-count] [-t target-pane] key ...

Send a key or keys to a window.
Each argument key is the name of the  key (such as ‘C-a' or ‘NPage') to send; if
the string is not recognised as a key, it is sent as a series of characters.

The -l flag disables key name lookup and sends the keys literally.
All arguments are sent sequentially from first to last.

The -R flag causes the terminal state to be reset; `$ tmux send -R` seems similar to `$ clear`.

-N specifies a repeat count; for example:

    $ tmux send -N3 abc

... will send 'abcabcabc' to the current command.

-X is  used to  send a  command into  copy mode  - see  the WINDOWS  AND PANES
section.

##
# WINDOWS AND PANES

The following commands are supported in copy mode:

    cancel                                       q
    clear-selection                              Escape
    copy-pipe <command> [<prefix>]
    copy-pipe-no-clear <command> [<prefix>]
    copy-pipe-and-cancel <command> [<prefix>]
    copy-selection [<prefix>]
    copy-selection-no-clear [<prefix>]
    goto-line <line>                             :
    halfpage-down-and-cancel
    page-down-and-cancel
    scroll-down-and-cancel
    stop-selection

    page-up                                      C-b
    page-down                                    C-f
    previous-paragraph                           {
    next-paragraph                               }

The  ‘-and-cancel' variants  of some  commands exit  copy mode  after they  have
completed  (for copy  commands)  or  when the  cursor  reaches  the bottom  (for
scrolling commands).
‘-no-clear' variants do not clear the selection.

The next and  previous word keys use  space and the ‘-', ‘_'  and ‘@' characters
as  word  delimiters  by default,  but  this  can  be  adjusted by  setting  the
word-separators session option.
Next word moves to the  start of the next word, next word end  to the end of the
next word and previous word to the start of the previous word.
The three next and  previous space keys work similarly but use  a space alone as
the word separator.

The jump commands enable quick movement within a line.
For instance, typing  ‘f' followed by ‘/'  will move the cursor to  the next ‘/'
character on the current line.
A ‘;' will then jump to the next occurrence.

Commands in copy mode may be prefaced by an optional repeat count.
With vi key bindings, a prefix is entered using the number keys.

The synopsis for the copy-mode command is:

     copy-mode [-Meu] [-t target-pane]

Enter copy mode.
The -u option scrolls one page up.
-M begins a  mouse drag (only valid if  bound to a mouse key  binding, see MOUSE
SUPPORT).
-e specifies that scrolling to the bottom of the history (to the visible screen)
should exit copy mode.
While in  copy mode,  pressing a key  other than those  used for  scrolling will
disable this behaviour.
This is intended  to allow fast scrolling through a  pane's history, for example
with:

    bind PageUp copy-mode -eu

Each window  displayed by tmux may  be split into  one or more panes;  each pane
takes up a certain area of the display and is a separate terminal.
A window may be split into panes using the split-window command.
Windows may be split horizontally (with the -h flag) or vertically.
Panes  may be  resized with  the resize-pane  command, the  current pane  may be
changed  with  the  select-pane  command and  the  rotate-window  and  swap-pane
commands may be used to swap panes without changing their position.
Panes are numbered beginning from zero in the order they are created.

A number of preset layouts are available.
These may be selected with the  select-layout command or cycled with next-layout
(bound to ‘Space' by  default); once a layout is chosen, panes  within it may be
moved and resized as normal.

The following layouts are supported:

    even-horizontal

Panes are spread out evenly from left to right across the window.

    even-vertical

Panes are spread evenly from top to bottom.

    main-horizontal

A large (main)  pane is shown at the  top of the window and  the remaining panes
are spread from left to right in the leftover space at the bottom.
Use the main-pane-height window option to specify the height of the top pane.

    main-vertical

Similar to  main-horizontal but  the large pane  is placed on  the left  and the
others spread from top to bottom along the right.
See the main-pane-width window option.

    tiled

Panes are  spread out as  evenly as  possible over the  window in both  rows and
columns.

In addition, select-layout may  be used to apply a previously  used layout - the
list-windows command displays  the layout of each window in  a form suitable for
use with select-layout.
For example:

    $ tmux list-windows
    0: ksh [159x48]
       layout: bb62,159x48,0,0{79x48,0,0,79x48,80,0}
    $ tmux select-layout bb62,159x48,0,0{79x48,0,0,79x48,80,0}

tmux automatically adjusts the size of the layout for the current window size.
Note that a layout cannot be applied to  a window with more panes than that from
which the layout was originally defined.

# PARSING SYNTAX

This section describes the  syntax of commands parsed by tmux,  for example in a
configuration file or at the command prompt.
Note that when commands are entered into the shell, they are parsed by the shell
– see for example ksh(1) or csh(1).

Each command is terminated by a newline or a semicolon (;).
Commands  separated by  semicolons together  form a  ‘command sequence’  - if  a
command  in  the  sequence  encounters  an error,  no  subsequent  commands  are
executed.

Comments are  marked by the  unquoted # character -  any remaining text  after a
comment is ignored until the end of the line.

If the last character of a line is \, the line is joined with the following line
(the \ and the newline are completely removed).
This is  called line  continuation and  applies both  inside and  outside quoted
strings and in comments.

Command arguments may be specified as strings surrounded by either single (') or
double quotes (").
This is required when the argument contains any special character.
Strings cannot span multiple lines except with line continuation.

Outside of single quotes and inside double quotes, these replacements are performed:

   - Environment variables preceded by $ are replaced with their
     value from the global environment (see the GLOBAL AND SESSION
     ENVIRONMENT section).

   - A leading ~ or ~user is expanded to the home directory of the
     current or specified user.

   - \uXXXX or \uXXXXXXXX is replaced by the Unicode codepoint cor‐
     responding to the given four or eight digit hexadecimal number.

   - When preceded (escaped) by a \, the following characters are
     replaced: \e by the escape character; \r by a carriage return;
     \n by a newline; and \t by a tab.

     Any other characters preceded by \ are replaced by themselves
     (that is, the \ is removed) and are not treated as having any
     special meaning - so for example \; will not mark a command
     sequence and \$ will not expand an environment variable.

Environment variables may  be set by using the syntax  ‘name=value’, for example
‘HOME=/home/user’.
Variables set during parsing are added to the global environment.

Commands may  be parsed conditionally  by surrounding them with  ‘%if’, ‘%elif’,
‘%else’ and ‘%endif’.
The argument to ‘%if’  and ‘%elif’ is expanded as a format  (see FORMATS) and if
it evaluates  to false  (zero or  empty), subsequent text  is ignored  until the
closing ‘%elif’, ‘%else’ or ‘%endif’.
For example:

    %if #{==:#{host},myhost}
    set -g status-style bg=red
    %elif #{==:#{host},myotherhost}
    set -g status-style bg=green
    %else
    set -g status-style bg=blue
    %endif

Will change the status  line to red if running on ‘myhost’,  green if running on
‘myotherhost’, or blue if running on another host.
Conditionals may be given on one line, for example:

    %if #{==:#{host},myhost} set -g status-style bg=red %endif

# COMMAND PARSING AND EXECUTION

tmux distinguishes between command parsing and execution.
In order to  execute a command, tmux needs  it to be split up into  its name and
arguments.
This is command parsing.
If a  command is run from  the shell, the shell  parses it; from inside  tmux or
from a configuration file, tmux does.
Examples of when tmux parses commands are:

   - in a configuration file;

   - typed at the command prompt (see command-prompt);

   - given to bind-key;

   - passed as arguments to if-shell or confirm-before.

To execute commands, each client has a ‘command queue’.
A  global command  queue not  attached  to any  client  is used  on startup  for
configuration files like ~/.tmux.conf.
Parsed commands added to the queue are executed in order.
Some commands, like if-shell and  confirm-before, parse their argument to create
a new command which is inserted immediately after themselves.
This means  that arguments can be  parsed twice or  more - once when  the parent
command (such as if-shell)  is parsed and again when it  parses and executes its
command.
Commands like if-shell, run-shell and display-panes stop execution of subsequent
commands on the  queue until something happens - if-shell  and run-shell until a
shell command finishes and display-panes until a key is pressed.
For example, the following commands:

    new-session; new-window
    if-shell "true" "split-window"
    kill-session

Will  execute  new-session, new-window,  if-shell,  the  shell command  true(1),
split-window and kill-session in that order.

## ?

> shell-command arguments are sh(1) commands.
> This may be a single argument passed to the shell, for example:

>       new-window 'vi /etc/passwd'

> Will run:

>       /bin/sh -c 'vi /etc/passwd'

> Additionally,  the new-window,  new-session, split-window,  respawn-window and
> respawn-pane commands  allow shell-command to  be given as  multiple arguments
> and executed directly (without ‘sh -c').
> This can avoid issues with shell quoting.
> For example:

>       $ tmux new-window vi /etc/passwd

> Will run vi(1) directly without invoking the shell.

## ?

> command [arguments] refers  to a tmux command, either passed  with the command
> and arguments separately, for example:

>       bind-key F1 set-option status off

> Or passed as a single string argument in .tmux.conf, for example:

>       bind-key F1 { set-option status off }

## ?

> Example tmux commands include:

>       refresh-client -t/dev/ttyp2

>       rename-session -tfirst newname

>       set-option -wt:0 monitor-activity on

>       new-window ; split-window -d

>       bind-key R source-file ~/.tmux.conf \; \
>               display-message "source-file done"

> Or from sh(1):

>       $ tmux kill-window -t :1

>       $ tmux new-window \; split-window -d

>       $ tmux new-session -d 'vi /etc/passwd' \; split-window -d \; attach

