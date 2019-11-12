# pipe-pane

Document this:

    $ tmux pipe-pane -t =study:2.1 -I "echo 'ls'"

This command  executes `ls(1)`  in the first  pane of the  second window  of the
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

*Imo `cat(1)` is useless, but what about `exec`?*
*Is it useful to prevent the shell from forking?*
*Better performance?*
*If so, maybe we should take the habit of always using `exec` when tmux pipes text to a shell command...*
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

   - <https://github.com/Morantron/tmux-fingers>
   - <https://github.com/tmux-plugins/tmux-continuum>
   - <https://github.com/tmux-plugins/tmux-logging>
   - <https://github.com/tmux-plugins/tmux-pain-control>
   - <https://github.com/tmux-plugins/tmux-resurrect>
   - <https://github.com/tmux-plugins/tmux-sensible>
   - <https://github.com/tmux-plugins/tmux-yank>
   - <https://github.com/zolrath/wemux>

Vim:

   - <https://github.com/tmux-plugins/vim-tmux>

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
It's described at `man tmux /^\s*new-session [`:

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

From `man tmux /^\s*attach-session`

> If run from outside tmux, create a new client in the current terminal and attach
> it to target-session. If used from inside, switch the current client.

I interpret  the second sentence  as tmux switching  the current session  in the
current client; the equivalent of pressing `pfx )`.
Look  at the  description of  the latter;  they use  the same  terminology (i.e.
“switch”).
And yet, in  practice, `$ tmux attach-session` inside tmux  fails with “sessions
should be nested with care, unset $TMUX to force”.

What gives?

# by default tmux runs a shell process every 15s for the statusline; use `sleep(1)` to change that time

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

# `respawn-pane` is useful when you have a pane which always runs the same application in the same place

Same thing for `respawn-window`.
Note that for a pane/window to be respawned, the `remain-on-exit` option needs to be on.

It is  useful, because you  don't have to restore  the geometry, and  because it
preserve the scrollback buffer.

<https://unix.stackexchange.com/a/512501/289772>

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

    com TxShowMessages call s:tx_show_messages()
    fu s:tx_show_messages()
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

## name a buffer created by `copy-selection`, `copy-pipe` and friends

Atm, all we can do is choose a prefix, but not the entire name.
This is an  issue when we need  to remove the buffer shortly  after its creation
(because we only need it temporarily).
Indeed, `deleteb` expects a full name.
Alternatively, as a  feature request, ask for `deleteb` to  accept a pattern, so
that we can run:

    deleteb -b prefix*

## pass to `send` a count which is the result of a numeric computation

It would be useful to write sth like this:

    command-prompt -I 1 -p 'number of commands:' { send -X -N (%1 + 1) search-backward '٪' }
                                                                  ^^^

## make tmux print the keys pressed so far (like what Vim does when 'showcmd' is set)

We would need a format variable which gives us this info, and we would use it in
our status line.

This would be very useful when we press sth like `"Ayiw` in copy mode.

## make tmux repeat an arbitrary subset of keys

Right now,  when `-r` is  passed to  `bind`, tmux enters  in a sort  of “repeat”
submode, in which **all** key bindings defined with `-r` can be repeated without
the prefix key.

This often leads to confusing situations.
For example, we have these key bindings:

    bind -r C-h resizep -L 5
    bind -r C-j resizep -D 5
    bind -r C-k resizep -U 5
    bind -r C-l resizep -R 5

Now suppose we want to make `(` and `)` repeatable:

    bind -r ( switchc -p
    bind -r ) switchc -n

We press the prefix key then `)` to focus the next session and have a brief look
at a window in the next session.
We press `)` again to get back to our other session which is running Vim.
In Vim, we have several splits; we want to focus the one below the current one,
and so we press `C-j`.
Instead of Vim focusing the split below, tmux will resize the current pane.
This is unexpected.
It would be  better if we coud tell  tmux to only repeat `)` and  `(`; not *any*
key binding defined with `-r`.
Basically, we would need sth equivalent to `vim-submode`.

## prevent tmux from wrapping long lines in copy mode

Wrapping long lines makes the output of `lsk` hard to read.
It would be nice if tmux could print a long line of text on a single screen line.
We would need a command to scroll the text horizontally.

## set up the color of the selection in copy mode, as well as the color of the indicator in the upper-right corner

## tell `if -F '#{@my_option}'` which scope we want to use for a user option

This matters if we have several user options with the same name but different scopes.

By default, tmux gives the priority to a server option:

    $ tmux set -s @my_option 0 \; set @my_option 1 \; set -w @my_option 1 \; set -p @my_option 1 \; if -F '#{@my_option}' 'display -p yes' 'display -p no'
    no~

Then a pane option:

    $ tmux set -us @my_option \; set -p @my_option 0 \; set -w @my_option 0 \; set -s @my_option 0 \; if -F '#{@my_option}' 'display -p yes' 'display -p no'
    no~

Then a window option:

    $ tmux set -us @my_option \; set -up @my_option \; set -s @my_option 0 \; set -w @my_option 1 \; if -F '#{@my_option}' 'display -p yes' 'display -p no'
    no~

Finally a session option.

#
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
selection is linewise; or try to infer it from:

   - `#{selection_start_x}`
   - `#{selection_start_y}`
   - `#{selection_end_x}`
   - `#{selection_end_y}`

You also need  a way to get  the line address of  the first or last  line of the
selection.
Indeed, to be  able to set the correct characterwise  selection, from a linewise
one, you  would need  to start  a new characterwise  selection from  the current
cursor position,  then move a  few lines up or  down (depending on  whether your
cursor is on the first line or last line of the linewise selection).
You should be able to use `#{copy_cursor_x}` and `#{copy_cursor_y}`.

---

Prevent `h`  and `l` from wrapping  around the first/last column  of the screen,
when we have a rectangle selection.
`#{pane_left}` and `#{pane_right}` could be useful.

---

`stop-selection` is interesting.
You stay in copy  mode, and you can move your cursor wherever  you want, but the
selection remains active.

# use `#{copy_cursor_line}` and `#{copy_cursor_word}` to solve issues/implement new features

# finish reading `~/Desktop/split-window_tmux.md`

Copied from here:
<https://gist.github.com/sdondley/b01cc5bb1169c8c83401e438a652b84e>

We've already started reading the document, and editing it.
It begins with fairly basic information, but ends with advanced ones.

# study wait-for

Compare:

    $ time tmux neww 'echo foo;sleep 3'
    ... 0,011 total~
        ^^^^^

Vs:
    ~
                                            ┌ my interpretation: emit the “signal” ‘neww-done’
                                            │                         ┌ wait for the signal ‘neww-done’
                                            ├───────────────────┐     ├────────────────┐
    $ time tmux neww 'echo foo;sleep 3;tmux wait-for -S neww-done' \; wait-for neww-done
    ... 3,019 total~
        ^^^^^

<https://unix.stackexchange.com/a/137547/289772>

# swap windows pane interactively

<https://www.youtube.com/watch?v=_OOSbjHmLPY>

# try to use extended patterns as described at `man 3 fnmatch /FNM_EXTMATCH`

You can pass the `FNM_EXTMATCH` flag to the C function `fnmatch()`:

> crose   `fnmatch(3)` is mentioned several times in `man tmux`.
>         And according to `man 3 fnmatch`, if the flag `FNM_EXTMATCH` is set, you can use extended patterns.
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
`FNM_EXTMATCH` flag is set at run time.
The compile-time option would not be set by default of course.

Or write a sed script which edits all the tmux C files invoking `fnmatch()` (`$ rg 'fnmatch\('`).
Ask nicm whether such a script is reliable; is it likely to break in the future?

# is `window-status-silence-style` missing?

`window-status-activity-style` and `window-status-bell-style` exist, so it seems
`window-status-silence-style` should exist too...

# tmux may fall back on the root table if it can't find a pressed key in the copy-mode table?

> orbisvicis │ does a root key binding have priority over a copy-mode key binding?
>            │ or do they both run, etc?
>            │ I mean, from experimenting it seems the copy-mode key binding has priority and the root binding is never
>            │ executed (testing copy-word in copy-mode where DoubleClick1Pane in root displays a message)
>            │ but then why do the default root bindings test #{pane_in_mode}, like MouseDrag1Pane or WheelUpPane?
>       nicm │ because if there is no binding in copy-mode it will go to the root
>            │ but it is probably unnecessary
>       nicm │ if you don't want it to do that you can bind the Any key in the table

# what's the `Any` key binding? how is it useful?

<https://github.com/tmux/tmux/issues/1953#issuecomment-544356973>

See `man tmux /the Any key`.

# try to use C-e, C-y, H, L, M more often in copy mode

    ┌─────┬─────────────┐
    │ C-e │ scroll-down │
    │ C-y │ scroll-up   │
    ├─────┼─────────────┤
    │ H   │ top-line    │
    │ L   │ bottom-line │
    │ M   │ middle-line │
    └─────┴─────────────┘

# some key bindings / plugins create undesired buffers

For example, fingers (after we press a hint):

    ~/.tmux/plugins/tmux-fingers/scripts/fingers.sh:115

Try to eliminate all those undesired buffers.
We should only have buffers we've explicitly ask tmux to create, and they should
all be named with the pattern `buf_123`.

# learn how to save and restore a layout

<https://wiki.archlinux.org/index.php/tmux#Get_the_default_layout_values>
*Read the rest of the page for other ideas...*

The format variables `#{window_layout}` and `#{window_visible_layout}` may help,
as well as `select-layout`.
More generally, read everything in the manpage which contains 'layout'.

---

You can save the current layout in an option with:

    $ tmux set -Fw @layout "#{window_layout}"

And you can restore the layout with:

    $ tmux run 'tmux select-layout "#{@layout}"'

---

Usage example (toggle  between moving the pane to the  far right, maximizing it,
or restoring original layout):

    $ cat <<'EOF' >/tmp/tmux.conf
    if -F '#{@layout}' \
        {run 'tmux select-layout "#{@layout}" \; set -uw @layout'} \
        {set -Fw @layout "#{window_layout}" ; splitw -fh  ; swapp -t ! ; killp -t !}
    EOF

    $ tmux neww \; splitw \; display -p one \; splitw -h

    $ tmux source /tmp/tmux.conf
    $ tmux source /tmp/tmux.conf
    ...

# install a key binding to remove the text before the cursor on command prompt

Right now, `C-u` removes all the line.
Btw, why does `C-u` delete the whole line by default?
Does it come from emacs?
It certainly doesn't come from readline.

Update: It comes from sh.

    $ sh
    $ foo bar M-b C-u

---

Also, `M-d` is missing, as well as `C-_` and `M-t`.
Also missing (but those are custom):

   - `M-p`     history-search-backward
   - `M-n`     history-search-forward
   - `M-u u`   upcase-word
   - `M-u l`   downcase-word
   - `M-u c`   capitalize-word

And when you delete some text with `C-u` or `C-k`, you can't paste it afterward with `C-y`.
And if you delete several words with `C-w`, you can't paste them with `C-y` (only the last one).

---

Idea:  if we  could ask  tmux to  give us  the position  of the  cursor and  the
contents of the command-line, we could  give these info to `vim-readline`, which
would compute the new command-line.
And if we could then tell tmux to replace the old command-line with the new one,
we could implement most of these key bindings.
Except  for `M-p`  and  `M-n`; for  those  we  would also  need  the history  of
commands,  which atm  is in  `~/.tmux/command_history`,  but it  seems it's  not
updated in real-time (I think you have to quit tmux to make it update).

Otherwise, you'll have to learn a bit of C and edit `status.c`.

# learn the difference between `send -l` and `send -ll`

> Bit more complicated than I thought because keys are always Unicode so we need
> a flag to say that they aren't.
> Please try this, you can use two  -l (send-keys -ll) to send literal keys rather
> than UTF-8: x.diff.txt

<https://github.com/tmux/tmux/issues/1832#issuecomment-509624368>

# maybe we could use control mode

> thomas_ada▹│ It's interesting that tmuxc is the only other client besides iterm which uses control mode.
>   zdykstra │ Nobody even uses tmuxc, I wrote it to scratch my own itch.
>            │ Which isn't to say I wouldn't mind more users ;)
>            │ Couple of quirks using control mode in cloned sessions - if memory serves, everything is printed to the
>            │ control stream once for each cloned session. So if you have 10 cloned sessions, you get 10 instances of
>            │ %window-add, and so on

<https://github.com/zdykstra/tmuxc>

# what's the closest command to a NOP?

    if -F 0 ''
    run ''
    refresh

For now, I would say `if -F 0 ''`.

<https://en.wikipedia.org/wiki/NOP_(code)>

# understand how to target an arbitrary pane in `command` inside `if -F -t! '...' {command}`

I'm trying to write a key binding which would run some commands on the condition
that the current pane is running a shell, and the previous one is running Vim.
And I'm confused  by the rules which  govern in which pane the  commands will be
run.

This key binding works as expected:

    is_shell='#{m:*sh,#{pane_current_command}}'
    is_vim='#{m:*vim,#{pane_current_command}}'

    bind x if -F "$is_shell" {if -F -t! "$is_vim" \
        {display 'you are in a shell and the previous pane runs Vim'} \
        {display 'you are in a shell but the previous pane is NOT running Vim'}}

But this one doesn't:

    is_shell='#{m:*sh,#{pane_current_command}}'
    is_vim='#{m:*vim,#{pane_current_command}}'

    bind x if -F "$is_shell" {if -F -t! "$is_vim" \
        {copy-mode} \
        {display 'you are in a shell but the previous pane is NOT running Vim'}}

because I want to enter copy mode in the shell pane, not in the Vim pane.
So I tried to pass `-t!` to `copy-mode`:

    is_shell='#{m:*sh,#{pane_current_command}}'
    is_vim='#{m:*vim,#{pane_current_command}}'

    bind x if -F "$is_shell" {if -F -t! "$is_vim" \
        {copy-mode -t!} \
        {display 'you are in a shell but the previous pane is NOT running Vim'}}

but it doesn't work.
Then I tried to run `last-pane` before `copy-mode`:

    is_shell='#{m:*sh,#{pane_current_command}}'
    is_vim='#{m:*vim,#{pane_current_command}}'

    bind x if -F "$is_shell" {if -F -t! "$is_vim" \
        {last-pane ; copy-mode} \
        {display 'you are in a shell but the previous pane is NOT running Vim'}}

but it doesn't work either.
I tried 2 other things which didn't work either.

From all those  experiments, I inferred the following rule:  “once you've passed
`-t` to `if-shell`, no matter what you will do, the tmux commands will be run in
the context of the pane you've targeted”.

But then,  I tried  to make  `copy-mode` be run  by `command-prompt`  instead of
being run directly:

    is_shell='#{m:*sh,#{pane_current_command}}'
    is_vim='#{m:*vim,#{pane_current_command}}'

    bind x if -F "$is_shell" {if -F -t! "$is_vim" \
        {command-prompt -p ':' {copy-mode}}}

For some  reason, `copy-mode` is now  correctly run in the  shell pane, provided
that I don't cancel the prompt and press Enter.
And it seems  that when `-t!` is passed  to a command or `last-pane`  is used in
the template of `command-prompt`, they both work as expected.

So what is the rule?
“once you've  passed `-t` to  `if-shell`, no matter what  you will do,  the tmux
commands will be run  in the context of the pane you've  targeted; except if you
use `command-prompt`, then everything will work as expected”.

---

`:confirm-before` and `run-shell` have the same effect.
`:choose-buffer` (and  probably all `choose-*`  commands) has a  similar effect;
i.e. it gives you the ability to target the pane you want.

What about any command which can run another command:

   - choose-buffer
   - choose-client
   - choose-tree
   - display-menu
   - display-panes
   - new
   - neww
   - pipe-pane
   - respawn-pane
   - respawn-window
   - splitw

These commands don't have the same effect:

   - if-shell

# try to compile your own libevent

    wget https://github.com/libevent/libevent/releases/download/release-2.1.10-stable/libevent-2.1.10-stable.tar.gz
    tar -zxvf libevent-2.1.10-stable.tar.gz
    cd libevent-2.1.10-stable
    CFLAGS="-g -O0" ./configure --enable-shared --prefix=$HOME/libeventbuild --disable-silent-rules
    make
    make install
    cd ..
    git clone https://github.com/tmux/tmux.git
    cd tmux
    sh autogen.sh
    PKG_CONFIG_PATH=$HOME/libeventbuild/lib/pkgconfig ./configure --prefix=$HOME/tmuxbuild
    make
    LD_LIBRARY_PATH=$HOME/libeventbuild/lib ./tmux new

<https://github.com/tmux/tmux/issues/1840#issuecomment-513273184>

This would give a little more info in a backtrace.
Not sure this would really help; just consider it.

# decipher the default value of 'status-format'

    status-format[0] "#[align=left range=left #{status-left-style}]#{T;=/#{status-left-length}:status-left}#[norange default]#[list=on align=#{status-justify}]#[list=left-marker]<#[list=right-marker]>#[list=on]#{W:#[range=window|#{window_index} #{window-status-style}#{?#{&&:#{window_last_flag},#{!=:#{window-status-last-style},default}}, #{window-status-last-style},}#{?#{&&:#{window_bell_flag},#{!=:#{window-status-bell-style},default}}, #{window-status-bell-style},#{?#{&&:#{||:#{window_activity_flag},#{window_silence_flag}},#{!=:#{window-status-activity-style},default}}, #{window-status-activity-style},}}]#{T:window-status-format}#[norange default]#{?window_end_flag,,#{window-status-separator}},#[range=window|#{window_index} list=focus #{?#{!=:#{window-status-current-style},default},#{window-status-current-style},#{window-status-style}}#{?#{&&:#{window_last_flag},#{!=:#{window-status-last-style},default}}, #{window-status-last-style},}#{?#{&&:#{window_bell_flag},#{!=:#{window-status-bell-style},default}}, #{window-status-bell-style},#{?#{&&:#{||:#{window_activity_flag},#{window_silence_flag}},#{!=:#{window-status-activity-style},default}}, #{window-status-activity-style},}}]#{T:window-status-current-format}#[norange list=on default]#{?window_end_flag,,#{window-status-separator}}}#[nolist align=right range=right #{status-right-style}]#{T;=/#{status-right-length}:status-right}#[norange default]"

    status-format[1] "#[align=centre]#{P:#{?pane_active,#[reverse],}#{pane_index}[#{pane_width}x#{pane_height}]#[default] }"

The default value of 'status-format' as given by `$ tmux -Lx -f/dev/null start \; show -g status-format` is: https://0x0.st/zOUx.txt
It contains this snippet: `#{T;=/#{status-left-length}:status-left}`.
I know the `T` format modifier, but I don't understand the meaning of the semicolon which follows immediately.
And I can't find a single example of a format modifier followed by a semicolon in the manpage.

The latter is also weird; it follows the syntax `#{=/number:...}` which doesn't seem to match any documented syntax.
Like `#{=5:...}`, `#{=-5:...}`, `#{=/5/prefix:...}`, `#{=/-5/suffix:...}`.
None of them match `#{=/number:...}`.

I think the semicolon is a way to combine several modifiers:
                                                                      v
    $ tmux set -g @foo 'some long text' \; display -p '#{s/long/short/;=/10/...:@foo}'
    some short...~
                                                                 v
    $ tmux set -g @foo 'some long text' \; display -p '#{=/10/...;s/long/short/:@foo}'
    some short...~

And what about this `range` token?
I think you can use it to define when the left part of the status line begins and when it ends.

    #[range=left] ... #[norange] = left part

Same thing for the right part:

    #[range=right] ... #[norange] = right part

Same thing for a particular window:

    #[range=window|123 ... #[norange] = part of the window list matching the window 123

This is mainly (only?) useful for the mouse.
When you click on  some part of the status line, tmux must  know how to consider
the location: left part? right part? window list?

##
# document
## the `synchronize-panes` window option

This key binding should toggle it:

    bind <key> set -w synchronize-panes

When it's on, anything you type in one pane, is typed in all the others.

      osse │ tmux synchronize-panes is pretty neat when debugging :) Can have the good case in one pane and the bad case
           │ in the other
    steven │ I don't think I get it, sync panes literally just sends the same keystrokes to all panes, right?
           │ so how can you have two different cases
      osse │ by turning on syncronize-panes after the two cases have been initialized
           │ in this particular case, open vim in two different directories

## how to run a custom zsh function from tmux

If the function doesn't run any command which requires a controlling terminal:

    $ tmux run 'zsh -ic "func"'

Otherwise:

    $ tmux neww 'zsh -ic "func"'

fzf is an example of command which needs a controlling terminal:

    func() { fzf; }

## `-e` option of `copy-mode` command

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

## `-A` option of `new-session` command

> The -A flag makes new-session behave like attach-session if
> session-name already exists; in this case, -D behaves like -d to
> attach-session, and -X behaves like -x to attach-session.

It could be useful in a script to make tmux attach to a session, or create it if
it doesn't exist, without having to test the output of some command like `$ tmux ls ...`.

## that when you run `$ tmux source`, `#{pane_current_command}` is 'tmux'

    $ cat <<'EOF' >/tmp/.tmux.conf
    is_shell='#{m:*sh,#{pane_current_command}}'
    if -F "$is_shell" {display 'you are in a shell'} {display 'you are NOT in a shell'}
    EOF

    $ tmux source /tmp/.tmux.conf
    you are NOT in a shell~

This may seem unexpected, because if the same command is run from a key binding,
then the current command is the shell (and not 'bind'):

    $ cat <<'EOF' >/tmp/.tmux.conf
    is_shell='#{m:*sh,#{pane_current_command}}'
    bind x if -F "$is_shell" {display 'you are in a shell'} {display 'you are NOT in a shell'}
    EOF

    $ tmux source /tmp/.tmux.conf
    # press pfx + x
    you are in a shell~

Although, now  that I  think about it,  it wouldn't make  sense for  the current
command to be 'bind',  because `bind` doesn't run the command  when we press pfx +x;
it *installs* the key binding.

## how to use valgrind to debug tmux

<https://github.com/tmux/tmux/issues/1829#issuecomment-509632045>

    $ valgrind --log-file=v.out tmux -Lx new

Note that for some reason, the command doesn't work atm on Ubuntu 16.04.
According to this answer: <https://askubuntu.com/a/280757/867754>
the issue should be fixed by installing `libc6-dbg:i386`.
In practice, it doesn't fix the issue.

Maybe we've somehow broken our Ubuntu 16.04, idk.
In any case, this valgrind command does work on Ubuntu 18.04 in a VM.

## that when you pass `-p` and `-c` to `display`

... the message is printed in the current pane of the current client, and not in
the active pane of the client passed to `-c`.

---

Also document the effect of `-c` alone:

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

This shows that `-c` changes in which client the message is displayed, but *not*
in which client the format variable is evaluated.

## the difference between `saveb -` and `showb`

I think there's none.
If that's true, then `showb` is probably better because more explicit.

## that we can install key bindings which are local to a session

To do so, you need to create a new key table and set the 'key-table' option accordingly.

## most of the `-status` and `-style` options

Not all; just the one you find the most useful.
Group them  according to  some themes, and  write questions/answers  about their
effect (not their syntax).

Sth like:

    # status line
    ## contents
    ### Which option should I set to change
    #### its left part?
    #### its right part?
    #### the window list in the middle?
    #### ...
    ## style
    ### Which option should I set to change the style of
    #### the left part?
    #### ...

## the `-c` argument passed of `attach-session`

This allows to set the default working directory used for new windows.
Right now, when you create a new window, the cwd is probably `~`.
Run these commands:

    $ tmux detach
    $ tmux attach -c /tmp

Now, when you create a new window, its cwd is `/tmp`.
Note that this is local to the session to which you attach.
If you switch to another session and create a new window, the cwd will be `~`, not `/tmp`.

All of this illustrate a new concept: the session working directory.
It's the working  directory set by default  to any process started  from a given
session (I think).

## how to get the index of the last window

    $ tmux display -p '#{W:#{?window_end_flag,#I,}}'

##
# typos in manpage

From `man tmux /OPTIONS`:

    OPTIONS
         The appearance and behaviour of tmux may be modified by changing the
         value of various options.  There are four types of option: server
         options, session options, window options and pane options.
                                 ^
                                 missing comma

---

`select-pane` supports the `-P` option, but it's not documented:

<https://github.com/tmux/tmux/issues/1856#issuecomment-514935016>

---

`load-buffer`  and  `save-buffer` support  the  special  filename `-`  which  is
interpreted as resp. the stdin and the stdout:

    $ printf 'test' | tmux loadb -
    $ tmux saveb - | wc -m
    4~

This is not documented.

---

`\ePtmux;seq\e\\` is not documented.
It's useful, for example, to send an OSC 52 sequence to the terminal, regardless
of how `set-clipboard` is set.

---

The documentation about `message-command-style` is unclear:

> message-command-style style
>         Set status line message command style.  For how to specify style,
>         see the STYLES section.

<https://github.com/tmux/tmux/issues/1065#issuecomment-328431849>

This would be more clear:

> message-command-style style
>         Set status line message command style for when you are in command mode with vi keys.
>         For how to specify style, see the STYLES section.

If you  need to  test the option:

    $ tmux -Lx -f =(cat <<'EOF'
      set -g status-keys vi
      set -g message-command-style fg=white,bg=colour31
      EOF
      )

     # press `C-b :` to enter command prompt
     # insert some text
     # press `Escape` to enter pseudo vi normal mode
     # press `i` to get back to insert mode

Note that `message-style`  controls the style of the command  prompt when you're
in insert mode, or when you're using emacs keys.
It also controls the style of the status line messages.

---

The possibility of combining 2 format modifiers with a semicolon is not documented.

    $ tmux set -g @foo 'some long text' \; display -p '#{s/long/short/;=/10/...:@foo}'
    some short...~

    $ tmux display -p '#{t;s/^.../XXX/:start_time}'
    XXX Aug  8 13:11:27 2019~

Note that you can't combine several modifiers of the same type:

> nicm │ crose: the way modifiers are implemented you can only have one of each type

For example this command outputs `next-3.Y`, instead of `Xext-3.Y`:

    $ tmux display -p '#{s/^./X/;s/.$/Y/:version}'

This is only an issue for `s` though, and it may change in the future:

> nicm │ id like it to work so it might change at some point
>      │ it only really makes sense for s
>      │ which wouldn't be that hard to do

You can also combine more than 2 modifiers:

    $ tmux display -p '#{t;=/10/;s/^.../XXX/:start_time}'

You should also document all of this in our notes.

---

The synopsis of some commands includes `start-directory`.
I  think   it  should   be  `working-directory`  to   be  consistent   with  the
terminology used  in the description  of the commands  and with the  synopsis of
`attach-session`.

