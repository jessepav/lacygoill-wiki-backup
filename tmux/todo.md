# pipe-pane

Document this:

    $ tmux pipe-pane -t study:2.1 -I "echo 'ls'"

This command  executes `$  ls` in  the first pane  of the  second window  of the
`study` session; the syntax is the following:

    $ tmux pipe-pane -t {session}:{window}.{pane} -I "shell-cmd"

`-I` and `-O` specify which of the shell-command output streams are connected to
the pane.

With `-I`, stdout is connected (so anything `shell-cmd` prints is written to the
pane as if it was typed).

You can also run:

    $ tmux pipe-pane -t {session}:{window}.{pane} -O "shell cmd"

With  `-O`,  stdin  is  connected  (so  any output  in  the  pane  is  piped  to
`shell-cmd`); both `-I` and `-O` may be used together.

It could be useful for our re-implementation of `vim-tbone`.

## is it buggy?

Disable your zshrc (`return` at the top).
Press `pfx :` and run `pipe-pane 'ansifilter >/tmp/log'`.
*Btw, the original command from tmux-logging looked like this*:

    pipe-pane "exec cat - | ansifilter >>/tmp/log"

*Imo `$ cat` is useless, but what about `$ exec`?*
*Is it useful to prevent the shell from forking?*
*Better performance?*
*If so, maybe we should take the habit of always using `$ exec` when tmux pipes text to a shell command...*
*Also, what about `>>`?*
*Is it really necessary? It doesn't seem so...*
*Maybe it's useful to prevent overwriting an existing file. *

Now, run some shell commands, like `$ ls`, `$ echo 'hello'`, `$ sudo aptitude update`, ...
The output of `$ echo 'hello'` is *not* logged.  Why?
Update: it *is* logged, but there are 120 characters in front of it (a `%` then 119 spaces).
So, you don't see it, unless you set Vim's 'wrap' option.
Why does tmux receive those 120 characters?
Update: You can prevent them by unsetting `PROMPT_SP`:

    unsetopt PROMPT_SP

If you re-enable all our zshrc, it's correctly logged.  Why?
Update: It seems to be thanks to our `PS1` line.

There seems  to be a  regular percent sign  (not the special  one we use  in our
prompt), which is added on a dedicated line after every output.  Why?
Update: again, run `unsetopt PROMPT_SP`. I think it will remove it.
However, unsetting this option would clear the output of a command which doesn't
terminate by a newline:

    $ print -n 'this is a test'

So, you would need to also unset `PROMPT_CR`.
But now,  after running a command  which doesn't terminate by  a newline, you'll
get the  current directory  at the  end of  the output  (instead of  the regular
percent in reverse video):
<https://unix.stackexchange.com/a/302710/289772>
No big  deal, but a  percent in reverse video  is less distracting  because more
consistent.
Here's another solution:

    :pipe-pane 'ansifilter | sed "/^%\\s*$/d" >/tmp/log'

Only the first executed command is logged (I'm not talking about the output; the
output is usually logged; I'm talking about the executed line).  Why?

> llua │ basically when zle is enabled, zsh reads input and prints the prompt to the same fd
>      │ but without, zsh just prints it to fd2
>      │ so that feature of yours isn't capturing fd10
>      │ and zsh doesn't use readline, it uses zle, the zsh line editor

> llua │ most shells print their prompt to stderr, we are def a standout in this
>      │ i am unsure why and lack an opinion either way tho
> llua │ since zle can interactively update the prompt, i guess that is why
>      │ eg: a keybind could change the prompt, so it may be why they decided on using its own fd

> llua │ "Pipe output sent by the program in target-pane to a shell command or vice versa."
>      │ so tmux is prob only checking for fd 1 and 2

> llua │ since tmux is the parent process, it passes 0, 1 and 2 to zsh and is prob why its able to record those,
>      │ since zsh opens additional fds for its own use, tmux prob can't work with it the same as 0,1 and 2

> llua │ then again, with tmux being a terminal, you would think that it can tell when someone writes something to
>      │ it, regardless of the fd used
>      │ idk

Make some tests, with and without our zshrc.
If `pipe-pane` is buggy, report the bugs.

Once `pipe-pane` is fixed, check out the tmux-logging plugin.
Right now, it seems to suffer from the same issues described above.

Update: Even if  you fix these issues,  if you edit the  command-line (C-w, C-h,
...), you'll get every single character you inserted (not the final command).
This makes me think that `pipe-pane` is not the right tool for the job.
`capture-pane` seems better.

---

Also,  we  have  moved  the  code sourcing  the  zsh  syntax  highlighting  into
`~/.zsh/syntax_highlighting.zsh`.
And we have set a guard to disable the sourcing.
And  we  have created  a  zsh  snippet to  disable  the  sourcing on  demand  in
`~/.config/zsh-snippet/main.txt`.
And we have left a question/answer about it in `~/.config/zsh-snippet/README.md`.
We did all  of this thinking that the syntax  highlighting badly interfered with
tmux-logging.
But was it really the case? Or was it just `pipe-pane` which was broken?
If it was not the case, do we want to undo everything we did?

#
# Plugins
## study these plugins

Tmux:

   - <https://github.com/tmux-plugins/tmux-sensible>
   - <https://github.com/tmux-plugins/tmux-pain-control>
   - <https://github.com/tmux-plugins/tmux-resurrect>
   - <https://github.com/tmux-plugins/tmux-continuum>

Vim:

   - <https://github.com/tmux-plugins/vim-tmux>

## reimplement/assimilate tmux-yank and tmux-logging

## tmux-fingers
### it wrongly renames the current window

This is fixed by the unmerged PR #67:
<https://github.com/Morantron/tmux-fingers/pull/67/files>

We've merged it locally, but it may break in a future update.
Try to assimilate the plugin?

### sometimes it fails (maybe because of an error in gawk)

MWE:

    press `pfx ?`
    press `pfx f`
    gawk: ~/.tmux/plugins/tmux-fingers/scripts/hinter.awk:139: (FILENAME=- FNR=1) warning: regexp escape sequence `\"' is not a known regexp operator~

##
        pfx ?
        pfx f
        gawk: ~/.tmux/plugins/tmux-fingers/scripts/hinter.awk:139: (FILENAME=- FNR=1) warning: regexp escape sequence `\"' is not a known regexp operator

# links to read

   - <https://www.reddit.com/r/tmux/comments/5cm2ca/post_you_favourite_tmux_tricks_here/>
   - <https://raw.githubusercontent.com/tmux/tmux/master/CHANGES>
   - <https://medium.freecodecamp.org/tmux-in-practice-series-of-posts-ae34f16cfab0>
   - <https://github.com/samoshkin/tmux-config>
   - <https://silly-bytes.blogspot.fr/2016/06/seamlessly-vim-tmux-windowmanager_24.html>
   - <https://github.com/tmux/tmux/blob/master/example_tmux.conf>
   - <http://man.openbsd.org/OpenBSD-current/man1/tmux.1>
   - <https://github.com/tmux/tmux/wiki/FAQ>
   - <https://devel.tech/tips/n/tMuXz2lj/the-power-of-tmux-hooks/>
   - <https://github.com/tmux-plugins/tmux-sensible>
   - <https://github.com/tmux-plugins/tmux-pain-control>

extended underline style
<https://github.com/tmux/tmux/commit/bc0e527f32642cc9eb2354d1bdc033ab6beca33b>

support for windows larger than visible on the attached client
<https://github.com/tmux/tmux/commit/646995384d695eed9de1b2363fd2b315ca01785e>

support for overline (SGR 53)
<https://github.com/tmux/tmux/commit/1ee944a19def82cb62abf6ab92c17eb30df77a41>

Style to follow when submitting a PR to tmux:
   - <https://man.openbsd.org/style.9>
   - <https://github.com/tmux/tmux/pull/1743#issuecomment-493450917>

# here's a way to programmatically get the PID of a process launched by tmux:

    P=$(tmux new -dP -- mycommand); tmux display -pt$P -F '#{pane_pid}'
                        ^^^^^^^^^
                        arbitrary command started in a new tmux window

# linking windows

Watch this:

    $ tmux linkw -s . -t 0

It creates a window of index 0, which is linked to the current window.
I think the command means: link the current window (`-s .`) to a new window of index 0.
Now, everything you type in one of these 2 windows, is also typed in the other.

It seems that windows can also be linked to sessions.
To understand what it means you'll need to first understand the concept of “session group”.
It's described at `$ man tmux /^\s*new-session [`:

> If -t is given, it specifies a session group.  Sessions in the
> same group share the same set of windows - new windows are linked
> to all sessions in the group and any windows closed removed from
> all sessions.  The current and previous window and any session
> options remain independent and any session in a group may be
> killed without affecting the others.

On the subject of session groups, see also: <https://github.com/tmux/tmux/issues/1793>

# evaluating a tmux replacement variable in different contexts

To test the current value of a replacement variable such as `#{pane_tty}`, run:

    # shell command
    $ tmux -S /tmp/tmux-1000/default display -p '#{pane_tty}'

    # tmux command
    :display -p '#{pane_tty}'

    # Vim command
    :echo system('tmux -S /tmp/tmux-1000/default display -p "#{pane_tty}"')

# including in the status line the number line where a pattern matches in the current pane

If you  include `#{C:hello}` in your  tmux status line, the  latter will contain
the number line where `hello` appears in the current tmux pane.

From `$ man tmux /FORMATS`:
> A  ‘C’ performs  a search  for an  fnmatch(3) pattern  in the  pane content  and
> evaluates to zero if not found, or a line number if found.

# attach-session

From `$ man tmux /^\s*attach-session`

> If run from outside tmux, create a new client in the current terminal and attach
> it to target-session. If used from inside, switch the current client.

I interpret  the second sentence  as tmux switching  the current session  in the
current client; the equivalent of pressing `pfx )`.
Look  at the  description of  the latter;  they use  the same  terminology (i.e.
“switch”).
And yet, in  practice, `$ tmux attach-session` inside tmux  fails with “sessions
should be nested with care, unset $TMUX to force”.

What gives?

# double a percent sign when running a shell process for your status line

If you run some shell command for include some info in your status line, e.g.:

    #{?#(cmd1),#(cmd2),}

And if the command contains a percent sign, e.g.:

    $ date +%s

I think you need to double the percent:

    $ date +%%s
             ^

That's what nicm seemed to suggest once in the #tmux irc channel.

# by default tmux runs a shell process every 15s for the statusline; use `$ sleep` to change that time

    #(while :; do command; sleep 30; done)

In case you wonder why you need a `while` loop, here's nicm's explanation:

> │  guardian │ I'm not sure I undertand why I need to wrap in a while loop
> │      nicm │ there is no mechanism to make tmux run it at particular times, so you need to run it all
> │           │ the time and just do your stuff every 30 seconds

---

In  case you  wonder where  the 15s  come from,  it's the  default value  of the
session option 'status-interval'.

# prevent some panes from being synchronized

Open the clock in them:

> Not really  the solution,  but any pane  set in a  different mode  (e.g. clock
> mode, copy mode, showing help) will not respond to key strokes.
> If you need all but a couple of panes to synchronize, this works pretty well.

<https://stackoverflow.com/questions/12451951/tmux-synchronize-some-but-not-all-panes#comment19620986_12451951>

# syntax of `confirm-before`

It expects a tmux command as last argument (!= shell command):

    $ tmux confirm-before -p "kill-pane #P? (y/n)" kill-pane

and if the command contains several words, you need to quote it:

    $ tmux confirm-before -p "display a message? (y/n)" "display -p 'hello'"
                                                        ^                  ^

Btw, why does `-p` fail here? `display` should print the message on stdout.

# `respawn-pane` is useful when you have a pane which always runs the same application in the same place

Same thing for `respawn-window`.
Note that for a pane/window to be respawned, the `remain-on-exit` option needs to be on.

It is  useful, because you  don't have to restore  the geometry, and  because it
preserve the scrollback buffer.

<https://unix.stackexchange.com/a/512501/289772>

# document `-e` option of `copy-mode` command

It makes tmux quit copy mode only when you reach the end of the screen with PgDown and WheelDown.
And possibly a few others.
But not when you reach it with `j` or `Down`.

You can make some tests with this minimal tmux.conf:

    set -g mouse on
    bind -n a copy-mode -e

Then press `pfx a`,  followed by PgDown or WheelDown until you  reach the end of
the screen; tmux should quit copy mode.

---

If you're looking for a real usage example, see this key binding installed by default:

    bind WheelUpPane if -F -t = "#{mouse_any_flag}" "send -M" "if -Ft= \"#{pane_in_mode}\" \"send -M\" \"copy-mode -et=\""

If you wonder what the `=` sign means here, it's a special token equivalent to `{mouse}`.
See `$ man tmux /MOUSE SUPPORT /{mouse}`.

# can some of the lhs used in our custom key bindings interfere with sequences used by programs?

Yes, I think.

But which kind of interference are we talking about?
Answer: suppose that a program sends the sequence `seq` to the terminal, but you
already use it in the lhs of a key binding.
When the program will send `seq`:

   1. the terminal will not receive it (which *may* cause the program to behave unexpectedly)
   2. the rhs of our custom key binding will be run (which *will* be unexpected)

But are `1.` and `2.` necessarily issues?
I  guess it  depends on  whether  the sequence  is  used by  your programs,  and
supported by your terminal.
If none of your program sends `seq`, then there should be no issue.
And if your  terminal doesn't support `seq`, then it's  possible that no program
will  send  it,  because  it  won't  be  present  in  your  terminal's  terminfo
description.

IOW, the more obscure the sequence is, the less issues you should have...

---

Document the fact that if your tmux sometimes runs commands that you didn't ask,
it may be because of `2.`.

---

As an example, you don't want to bind anything to the sequence `ESC O A`.

    $ cat <<'EOF' >/tmp/tmux.conf
    set -s user-keys[0] "\eOA"
    bind -n User0 display hello
    EOF

    $ tmux -Lx -f/tmp/tmux.conf

Press Up to recall the last run command in the history of the shell commands:
tmux prints 'hello'.

Btw, this seems  to show that when  tmux receives a sequence  which both matches
the  lhs of  a key  binding  *and* an  escape  sequence supported  by the  outer
terminal,  tmux  runs the  rhs;  it  doesn't relay  the  sequence  to the  outer
terminal.

---

One possible lhs concerned by this issue is `M-:`:

> ESC :     Select #3 Character Set.

<https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Tektronix-4014-Mode>

---

You can find all escape sequences supported by xterm like so:

    :sp /tmp/file
    :r /usr/share/doc/xterm/ctlseqs.txt.gz
    :v/^ESC/d_
    :%s/.\{10}\zs.\{2,}/
    +tip
    gsip
    :RemoveDuplicateLines

Note that at the moment, it seems there may be an issue with `ESC SP F` and `ESC SP L`.
Indeed, we  use `pfx F` to  run the tmux  command `find-window`, and `pfx  L` to
toggle the logging of the tmux server.
And since our prefix is `M-SP`, `pfx F` is `ESC SP F`, and `pfx L` is `ESC SP L`.

# implement the equivalent of Vim's `gv` in copy mode

Is it sth which is already planned?

See: https://github.com/tmux/tmux/wiki/Contributing

> Small things
> ...
> A command in copy mode to toggle the selection.

# implement `pfx L` (similar to `ZL` in Vim)

The key binding would move a horizontal pane into a vertical one to the right.
Implement similar  ones with `H`, `J`  and `K`, to gain  consistency between Vim
and tmux.

# play with `$ echo hello | tmux splitw -dI &`

From `$ man tmux /splitw`:

> An empty shell-command ('') will create a pane with no command
> running in it.  Output can be sent to such a pane with the
> display-message command.  The -I flag (if shell-command is not
> specified or empty) will create an empty pane and forward any
> output from stdin to it.  For example:
>
>         $ make 2>&1|tmux splitw -dI &

Maybe we should use this to get rid of a temporary file in `:LogEvents`.
Maybe it would simplify the code.

#
# find a way to
## configure the indicator `(x/y results)` after a search in copy-mode

Right  now, it  starts indexing  from  the bottom,  which means  that the  match
indexed by 1 is at the bottom, while the last one is at the top.
In Vim, that's the opposite.
This is a continuous source of distraction.

## configure the indicator `[123/456]` in the upper-right corner of the screen, when we enter copy mode

The first number is  the number of lines in the scrollback  buffer which are not
visible and are below the last line of the screen.
It's a **dynamic**  number; i.e. it can  change when you move  in the scrollback
buffer.
It gives you a sense of **how far** from the bottom of the buffer you are.

The second number is the number of  lines in the scrollback buffer which are not
visible and are above the first line of the screen when you quit copy mode.
It's a **static** number; i.e. it doesn't change when you move in the scrollback
buffer.
It gives you a sense of **how big** the buffer is.

This is confusing.
I would  prefer the first number  to be the address  of the current line  in the
scrollback buffer  (starting from its end;  i.e. the bottom line  would have the
address 1), and the second number to be the total number of lines in the latter.

## make `n` and `N` move in absolute directions in copy mode

It  would be  nice if  `n` and  `N`  could always  move in  the same  direction,
regardless of whether we started a search with `/` or `?`.

## filter the output of `show-messages`

Often, you pile up a lot of useless messages.
It would  be useful  to be  able to  remove them,  so that  a new  and important
message stands out better.

Maybe install a Vim command which would capture capture the output of
`$ tmux show-messages`, dump it in a  buffer, and remove some common and useless
messages.

    com! TxShowMessages call s:tx_show_messages()
    fu! s:tx_show_messages()
        new +setl\ bt=nofile\ bh=hide\ nobl\ noswf\ wfw
        call setline(1, systemlist('tmux show-messages'))
        sil! g/\m\CConfiguration reloaded.$\|No previous window\|No next window/d_
    endfu

#
# document the `synchronize-panes` window option

This key binding should toggle it:

    bind <key> setw synchronize-panes

When it's on, anything you type in one pane, is typed in all the others.

# study how v, V, C-v behave in Vim when we're already in visual mode; try to make tmux copy-mode consistent

The  replacement  variables  `rectangle_toggle`  (1 if  rectangle  selection  is
activated) and `selection_present` (1 if selection  started in copy mode) may be
useful.

# finish reading `~/Desktop/split-window_tmux.md`

Copied from here:
<https://gist.github.com/sdondley/b01cc5bb1169c8c83401e438a652b84e>

We've already started reading the document, and editing it.
It begins with fairly basic information, but ends with advanced ones.
You'll probably better understand tmux key  bindings, and learn how to do things
you didn't know were possible before.
For example,  it explains how to  create your own  custom key table, and  how to
“chain” key bindings.

Once you've read it, use your new knowledge to improve our tmux.conf.

# study wait-for

Compare:

    $ time tmux new-window -t fun 'echo foo;sleep 10'

Vs:
    ~
    $ time tmux new-window -t fun 'echo foo;sleep 10;tmux wait-for -S fun-neww-done' \; \
      wait-for fun-neww-done

<https://unix.stackexchange.com/a/137547/289772>

# swap windows pane interactively

<https://www.youtube.com/watch?v=_OOSbjHmLPY>

# try to use extended patterns as described at `$ man 3 fnmatch /FNM_EXTMATCH`

You can pass the `FNM_EXTMATCH` flag to the C function `fnmatch()`:

> crose   `fnmatch(3)` is mentioned several times in `$ man tmux`.
>         And according to `$ man 3 fnmatch`, if the flag `FNM_EXTMATCH` is set, you can use extended patterns.
>         I'm interested in this, because it lets you use `|` which could be useful to simplify some formats
>         when you have more than 2 alternatives.
> crose   Unfortunately, it doesn't seem to be set in tmux, because
>         `$ tmux display -p '#{m:foo|bar|baz,bar}'` outputs 0.
>         Is there a way for the user to set this flag?

> nicm    it is a flag you pass to fnmatch
> nicm    but its not portable so not going to happen
> nicm    you could add it for your local build if you wanted
> nicm    look for fnmatch in format.c
> nicm    and change the 0 to FNM_EXTMATCH

This allows you to write sth like:

    $ tmux display -p '#{m:+(foo|bar|baz),bar}'

Try to  ask nicm  whether an  option could be  set at  compile-time so  that the
`FNM_EXTMATCH` flag is set at runtime.
The compile-time option would not be set by default of course.

Or write a sed script which edits all the tmux C files invoking `fnmatch()` (`$ rg 'fnmatch\('`).
Ask nicm whether such a script is reliable; is it likely to break in the future?

# is `window-status-silence-style` missing?

`window-status-activity-style` and `window-status-bell-style` exist, so it seems
`window-status-silence-style` should exist too...

