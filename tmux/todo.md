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

##
        pfx ?
        pfx f
        gawk: ~/.tmux/plugins/tmux-fingers/scripts/hinter.awk:139: (FILENAME=- FNR=1) warning: regexp escape sequence `\"' is not a known regexp operator

# links to read

   - <https://www.reddit.com/r/tmux/comments/5cm2ca/post_you_favourite_tmux_tricks_here/>
   - <https://medium.freecodecamp.org/tmux-in-practice-series-of-posts-ae34f16cfab0>
   - <https://github.com/samoshkin/tmux-config>
   - <https://silly-bytes.blogspot.fr/2016/06/seamlessly-vim-tmux-windowmanager_24.html>
   - <https://github.com/tmux/tmux/blob/master/example_tmux.conf>
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

# move `~/wiki/terminal/tmux.md` from the terminal wiki to the tmux wiki?

# create a new session from within tmux

    $ tmux switchc -t$(tmux new -dP -F '#{session_id}')

# linking windows

Watch this:

    $ tmux linkw -s . -t 0
    # update: it seems you can omit `-s .`:    $ tmux linkw -t0

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

# evaluating a format variable in different contexts

To test the current value of a format variable such as `pane_tty`, run:

    # shell command
    $ tmux -S /tmp/tmux-1000/default display -p '#{pane_tty}'

    # tmux command
    :display -p '#{pane_tty}'

    # Vim command
    :echo system('tmux -S /tmp/tmux-1000/default display -p "#{pane_tty}"')

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

    $ tmux confirm -p "killp #P? (y/n)" killp

and if the command contains several words, you need to quote it:

    $ tmux confirm -p "display a message? (y/n)" "display -p 'hello'"
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

    $ tmux -Lx -f =(cat <<'EOF'
    set -g mouse on
    bind -n a copy-mode -e
    EOF
    )

Then press `a`, followed  by PgDown or WheelDown until you reach  the end of the
screen; tmux should quit copy mode.

---

If you're looking for a real usage example, see this key binding installed by default:

    bind WheelUpPane if -Ft= '#{mouse_any_flag}' { send -M } \
    { if -Ft= '#{pane_in_mode}' 'send -M' 'copy-mode -et=' }
                                                      ^

---

What's `mouse_any_flag`?

<https://github.com/tmux/tmux/blob/d769fec8d670ce37d476da3e31d6e68f9d43408c/regress/conf/58304907c117cab9898ea0b070bccde3.conf#L65>

    # var|bind \ cmd  |   vim   |   less    | copy |  zsh
    # pane_in_mode    |    0    |     0     |   1  |   0
    # mouse_any_flag  |    1    |     0     |   0  |   0
    # alternate_on    |    1    |     1     |   0  |   0
    # WheelUpPane     | send -M | send Up   |   *  | send Up (** or copy-mode -e)
    # WheelDownPane   | send -M | send Down |   *  | send Down
    # * panes in copy mode have scroll handled by different bindings

If you run `:set mouse=` in Vim, `mouse_any_flag` is 0 in tmux.
If you run `:set mouse=a` in Vim, `mouse_any_flag` is 1 in tmux.

---

Here are all our current key bindings which can copy text in copy mode:

    bind -T copy-mode-vi S                 send -X copy-pipe-and-cancel "xargs -I {} tmux run 'xdg-open \"https://www.google.com/search?q={}\"'"
    bind -T copy-mode-vi Y                 send -X copy-selection-and-cancel \; paste-buffer -p
    bind -T copy-mode-vi x                 send -X copy-pipe-and-cancel "xargs -I {} tmux run 'xdg-open \"{}\"'"
    bind -T copy-mode-vi y                 send -X copy-pipe-and-cancel "xsel -i --clipboard"
    bind -T copy-mode-vi MouseDragEnd1Pane send -X copy-pipe-and-cancel "xsel -i --primary"
    bind -T copy-mode-vi M-y               send -X copy-pipe-and-cancel "xsel -i --clipboard; tmux paste-buffer"

Try to modify them so that the name of the tmux buffers they create is shorter (`buf0`, `buf1`, ...).

> Copy  commands may  take an  optional buffer  prefix argument  which is  used to
> generate  the  buffer  name  (the  default is  ‘buffer'  so  buffers  are  named
> ‘buffer0', ‘buffer1' and so on).

# document `-A` option of `new-session` command

> The -A flag makes new-session behave like attach-session if
> session-name already exists; in this case, -D behaves like -d to
> attach-session, and -X behaves like -x to attach-session.

It could be useful in a script to make tmux attach to a session, or create it if
it doesn't exist, without having to test the output of some command like `$ tmux ls ...`.

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

See: <https://github.com/tmux/tmux/wiki/Contributing>

> Small things
> ...
> A command in copy mode to toggle the selection.

# implement `M-S-a` to focus the next window with an alert

Use the `-a` argument passed to `:next-window`.

> next-window [-a] [-t target-session]
>               (alias: next)
>         Move to the next window in the session.  If -a is used, move to
>         the next window with an alert.

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

## prevent the command-prompt history from polluting the regular history

    :command-prompt 'display %%'
    (display) hello~
              ^^^^^
              type that

      press this
      vv
    : Up
    hello~

#
# document the `synchronize-panes` window option

This key binding should toggle it:

    bind <key> set -w synchronize-panes

When it's on, anything you type in one pane, is typed in all the others.

      osse │ tmux synchronize-panes is pretty neat when debugging :) Can have the good case in one pane and the bad case
           │ in the other
    steven │ I don't think I get it, sync panes literally just sends the same keystrokes to all panes, right?
           │ so how can you have two different cases
      osse │ by turning on syncronize-panes after the two cases have been initialized
           │ in this particular case, open vim in two different directories

# study how v, V, C-v behave in Vim when we're already in visual mode; try to make tmux copy-mode consistent

The format variables `rectangle_toggle` (1  if rectangle selection is activated)
and `selection_present` (1 if selection started in copy mode) may be useful.

Here's what doesn't work like Vim atm:

    v    + select sth +  V
    v    + select sth +  C-v
    V    + select sth +  v
    V    + select sth +  C-v
    C-v  + select sth +  v
    C-v  + select sth +  V

---

I  think we  would need  a new  variable, `#{line_toggle}`,  to detect  when the
selection is linewise.

You also need  a way to get  the line address of  the first or last  line of the
selection.
Indeed, to be  able to set the correct characterwise  selection, from a linewise
one, you  would need  to start  a new characterwise  selection from  the current
cursor position,  then move a  few lines up or  down (depending on  whether your
cursor is on the first line or last line of the linewise selection).
You should be  able to use `#{cursor_x}` and `#{cursor_y}`,  but for some reason
they aren't updated in copy mode.

---

Prevent `h`  and `l` from wrapping  around the first/last column  of the screen,
when we have a rectangle selection.
`#{pane_left}` and `#{pane_right}` could be useful.

---

Try to install a key binding using `append-selection`.
The latter  command allows you  to yank the selection,  append it to  the latest
tmux buffer, and quit copy mode.

---

`stop-selection` is interesting.
You stay in copy  mode, and you can move your cursor wherever  you want, but the
selection remains active.

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

    $ time tmux neww 'echo foo;sleep 3'

Vs:
    ~
    $ time tmux neww 'echo foo;sleep 3;tmux wait-for -S neww-done' \; wait-for neww-done

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

##
# typos in manpage

'user-keys' is documented in the session options.
But it's not a session option; it's a server one.

                                             vv
    $ tmux set -a user-keys "\e[123" \; show -s user-keys \; set user-keys ''
    user-keys[0] \\e[123~

It's the only option which is in the wrong section.
Here's how you can check.
First copy, the lines in the manpage describing the options of a given type.
Position your  cursor on  an empty line,  and press `""]p`,  so that  the option
names are indented with 0 space.
Select the pasted lines (`V']`), then run:

    :*v/^\S/d_
    :*s/\%(\[\]\)\=\s.*//
    :*s/^/tmux show -gw /
    :*g/^/s/.*/\=join(systemlist(getline('.')), '    ')/

In the last but one command, replace `-gw` with `-s` for the server options, and
with nothing for the session options.

If you get  an empty line somewhere, it  means that the option name  – which was
there originally – is not documented in the right section.
Look at the  option above/below – to  memorize its relative position  – and undo
the last `:g` command; you should be able to find the name of the option.

---

> This section describes the commands supported by tmux.  Most commands
> accept the optional -t (and sometimes -s) argument with one of
> target-client, target-session**,** target-window, or target-pane.
                             ^
                             missing comma

---

> pane_mode                       Name of pane mode, if any.
                                                         ^
                                                         there should be no dot

---

> alternate_on                    If pane is in alternate screen
> pane_in_mode                    If pane is in a mode
> pane_input_off                  If input to pane is disabled
> pane_synchronized               If pane is synchronized

`If` should be replaced with `1 if`.

---

> set-titles-string string
>         String used to set the **window title** if set-titles is on.  Formats
>         are expanded, see the FORMATS section.

Shouldn't `window title` be replaced with `client terminal title`?

From `$ man tmux /OPTIONS /set-titles`:

> set-titles [on | off]
>         Attempt to set the **client terminal title** using the tsl and fsl
>         terminfo(5) entries if they exist.  tmux automatically sets these
>         to the \e]0;...\007 sequence if the terminal appears to be
>         xterm(1).  This option is off by default.

---

`next-matching-bracket` and `previous-matching-bracket` are not documented.

---

Inconsistency in the terminology.

From `$ man tmux /^\s*display-message /^\s*-v`:

> -v prints verbose logging as the format is parsed and -a lists
> the **format variables** and their values.

From `$ man tmux /FORMATS`:

> **Replacement variables** are enclosed in ‘#{' and ‘}', for example ‘#{session_name}'.

It should probably settle down on one term (not two).

Personally, I prefer “format variables”.
It's shorter, and tells you that it only exists in the context of a format.
From “variable”, you can infer that it can be replaced or evaluated.

---

From `$ man tmux /^\s*display-message`:

> information is taken from target-pane if -t is given, otherwise the
> active pane for the session attached to target-client.

    $ tmux lsc
    /dev/pts/4: study [119x34 st-256color] (utf8) ~
    /dev/pts/10: fun [80x24 xterm-256color] (utf8) ~
                            ^^^^^^^^^^^^^^
                            second terminal attached to the second session

From the xterm terminal, and the 'fun' session, run:

    $ echo test | less

Next, from the st terminal, and the 'study' session, run:

    $ tmux display -c $(tmux lsc | awk -F: '/fun/{print $1}') '#{alternate_on}'

Finally, focus the xterm terminal, and run `:show-messages`.
You should see `0` in the log.
So, `-c '/dev/pts/10'` made tmux print the message in a different client, but it
didn't take the info from the active pane attached to the 'fun' session.
If that was the case, `0` would not have been logged, but `1`.

Is the documentation wrong? Or is it right but there's a bug?

Btw, if you  use `-p` with `-c`, the  message is printed in the  current pane of
the current client, and not in the active pane of the client passed to `-c`.

---

From `$ man tmux /^\s*select-pane`:

>         select-pane [-DLRUdel] [-T title] [-t target-pane]

> Make pane target-pane the active pane **in window target-window**.

There's no `target-window` in the synopsis of the command.
Should “in window target-window” be replaced by “in current window”?

---

From `$ man tmux /^\s*last-pane`:

> last-pane [-de] [-t target-window]

Why is `[-t target-window]` mentioned in the synopsis?
`target-window` is not mentioned in the description of the command.
I tried to provide a window ID (`@123`) to `-t`, but it didn't have any effect.

It seems the right synopsis is just:

> last-pane [-de]

---

The `-N` flag which one can pass to `command-prompt` is not documented.

I think `-N` makes the prompt only accept numeric key presses.

---

From `$ man tmux /MOUSE SUPPORT`:

> In addition, target-session, target-window or target-pane may consist entirely
> of the token ‘{mouse}' (alternative form ‘=') to specify **the most recent mouse**
> **event** (see the MOUSE SUPPORT section)  or ‘{marked}' (alternative form ‘~') to
> specify the marked pane (see select-pane -m).

I think  it should  be “the session,  window, pane where  the most  recent mouse
event occurred”.

---

From `$ man tmux /WINDOWS AND PANES`:

> copy-end-of-line [<prefix>]                  D               C-k

Imo, `Y` would be a better choice.
I understand why `D` was chosen though; by symmetry with `C-k` in emacs.
Indeed, Vim's `D` is equivalent to emacs's `C-k`.
But it's irrelevant; `copy-end-of-line` doesn't delete text.
The reason why `C-k` was chosen in emacs is probably because there's no equivalent of `Y`.
It was the closest command, but not the exact one.

