# targetting
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
##
##
# COMMANDS
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
## select-pane

>         select-pane [-DLRUdel] [-T title] [-t target-pane]

> Make pane target-pane the active pane in window target-window.

> If one of -D, -L, -R, or -U is used, respectively the pane below, to the left,
> to the right, or above the target pane is used.

> -l is the same as using the last-pane command.

> -e enables or -d disables input to the pane.

> -T sets the pane title.

##
## join-pane

>         join-pane [-bdhv] [-l size | -p percentage] [-s src-pane] [-t dst-pane]
>                       (alias: joinp)

> Like split-window, but instead of splitting  dst-pane and creating a new pane,
> split it and move src-pane into the space.
> This can be used to reverse break-pane.
> The -b option causes src-pane to be joined to left of or above dst-pane.

> If -s is omitted and a marked pane is present (see select-pane -m), the marked
> pane is used rather than the current pane.

## swap-pane

> swap-pane [-dDU] [-s src-pane] [-t dst-pane]
>               (alias: swapp)
>         Swap two panes.  If -U is used and no source pane is specified
>         with -s, dst-pane is swapped with the previous pane (before it
>         numerically); -D swaps with the next pane (after it numerically).
>         -d instructs tmux not to change the active pane.

>         If -s is omitted and a marked pane is present (see select-pane
>         -m), the marked pane is used rather than the current pane.

## swap-window

> swap-window [-d] [-s src-window] [-t dst-window]
>               (alias: swapw)
>         This is similar to link-window, except the source and destination
>         windows are swapped.  It is an error if no window exists at
>         src-window.

>         Like swap-pane, if -s is omitted and a marked pane is present
>         (see select-pane -m), the window containing the marked pane is
>         used rather than the current window.

##
##
## ?

What is a mouse event?

## Which mouse events are available?  (8)

    ┌───────────────┬──────────────────────────────────────────────────────────────┐
    │ WheelDown     │ wheel scrolled downward                                      │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ WheelUp       │ wheel scrolled upward                                        │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ DoubleClick1  │ double left click                                            │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ TripleClick1  │ triple left click                                            │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ MouseDown1    │ left click pressed                                           │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ MouseUp1      │ left click released                                          │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ MouseDrag1    │ mouse moving after left click has been pressed               │
    ├───────────────┼──────────────────────────────────────────────────────────────┤
    │ MouseDragEnd1 │ left click released after it was pressed and the mouse moved │
    └───────────────┴──────────────────────────────────────────────────────────────┘

In the last 6 events, `1` can be replaced by `2` or `3`.

    ┌───┬───────────────────┐
    │ 1 │ left click used   │
    ├───┼───────────────────┤
    │ 2 │ middle click used │
    ├───┼───────────────────┤
    │ 3 │ right click used  │
    └───┴───────────────────┘

## I left-click on a pane, then release the click.  Which events are fired?

`MouseDown1` then `MouseUp1`.

## I left-click on a pane, move the mouse, then release the click.  Which events are fired?

`MouseDown1`, `MouseDrag1`, `MouseDragEnd1`.

`MouseUp1` is only fired if the mouse didn't move after `MouseDown1`.

## In which location can a mouse event occur?  (6)

    ┌───────────────┬───────────────────────────────────┐
    │ Pane          │ the contents of a pane            │
    ├───────────────┼───────────────────────────────────┤
    │ Border        │ a pane border                     │
    ├───────────────┼───────────────────────────────────┤
    │ Status        │ the status line window list       │
    ├───────────────┼───────────────────────────────────┤
    │ StatusLeft    │ the left part of the status line  │
    ├───────────────┼───────────────────────────────────┤
    │ StatusRight   │ the right part of the status line │
    ├───────────────┼───────────────────────────────────┤
    │ StatusDefault │ any other part of the status line │
    └───────────────┴───────────────────────────────────┘

## How to build the lhs of a mouse key binding?

Follow the syntax `MouseEvent + Location`.

Which lhs should I use to run a command when I right-click on the left part of my status line?

    MouseDown3StatusLeft
    ├────────┘├────────┘
    │         └ location
    └ mouse event

Usage example:

    $ tmux bind -T root MouseDown3StatusLeft display 'test'

## ?

How to target the session/window/pane where a certain mouse event has occurred in a certain location?

## ?

Document the fact that *I think* the token  `{mouse}` or `=` can only be used in
a key binding.
It may be due to the definition of a mouse event.
Maybe a mouse event only occurs when a key is pressed; after that it's too late;
before that it's too early.

## ?

> In addition, target-session, target-window or target-pane may consist entirely
> of the token ‘{mouse}' (alternative form ‘=') to specify the most recent mouse
> event (see the MOUSE SUPPORT section)  or ‘{marked}' (alternative form ‘~') to
> specify the marked pane (see select-pane -m).

## MOUSE SUPPORT

>      If the mouse option is on (the default is off), tmux allows mouse events
>      to be bound as keys.  The name of each key is made up of a mouse event
>      (such as ‘MouseUp1') and a location suffix, one of the following:

>            Pane             the contents of a pane
>            Border           a pane border
>            Status           the status line window list
>            StatusLeft       the left part of the status line
>            StatusRight      the right part of the status line
>            StatusDefault    any other part of the status line

>      The following mouse events are available:

>            WheelUp       WheelDown
>            MouseDown1    MouseUp1      MouseDrag1   MouseDragEnd1
>            MouseDown2    MouseUp2      MouseDrag2   MouseDragEnd2
>            MouseDown3    MouseUp3      MouseDrag3   MouseDragEnd3
>            DoubleClick1  DoubleClick2  DoubleClick3
>            TripleClick1  TripleClick2  TripleClick3

>      Each should be suffixed with a location, for example ‘MouseDown1Status'.

>      The special token ‘{mouse}' or ‘=' may be used as target-window or
>      target-pane in commands bound to mouse key bindings.  It resolves to the
>      window or pane over which the mouse event took place (for example, the
>      window in the status line over which button 1 was released for a
>      ‘MouseUp1Status' binding, or the pane over which the wheel was scrolled
>      for a ‘WheelDownPane' binding).

>      The send-keys -M flag may be used to forward a mouse event to a pane.

>      The default key bindings allow the mouse to be used to select and resize
>      panes, to copy text and to change window using the status line.  These
>      take effect if the mouse option is turned on.

## send-keys

> send-keys [-lMRX] [-N repeat-count] [-t target-pane] key ...
>               (alias: send)
>         Send a key or keys to a window.  Each argument key is the name of
>         the key (such as ‘C-a' or ‘NPage') to send; if the string is not
>         recognised as a key, it is sent as a series of characters.  The
>         -l flag disables key name lookup and sends the keys literally.
>         All arguments are sent sequentially from first to last.  The -R
>         flag causes the terminal state to be reset.

>         -M passes through a mouse event (only valid if bound to a mouse
>         key binding, see MOUSE SUPPORT).

>         -X is used to send a command into copy mode - see the WINDOWS AND
>         PANES section.  -N specifies a repeat count.

###
## split-window

> split-window [-bdfhIvP] [-c start-directory] [-e environment] [-l size |
>         -p percentage] [-t target-pane] [shell-command] [-F format]
>               (alias: splitw)
>         Create a new pane by splitting target-pane: -h does a horizontal
>         split and -v a vertical split; if neither is specified, -v is
>         assumed.  The -l and -p options specify the size of the new pane
>         in lines (for vertical split) or in cells (for horizontal split),
>         or as a percentage, respectively.  The -b option causes the new
>         pane to be created to the left of or above target-pane.  The -f
>         option creates a new pane spanning the full window height (with
>         -h) or full window width (with -v), instead of splitting the
>         active pane.

>         An empty shell-command ('') will create a pane with no command
>         running in it.  Output can be sent to such a pane with the
>         display-message command.  The -I flag (if shell-command is not
>         specified or empty) will create an empty pane and forward any
>         output from stdin to it.  For example:

>               $ make 2>&1|tmux splitw -dI &

>         All other options have the same meaning as for the new-window
>         command.

## break-pane

> break-pane [-dP] [-F format] [-n window-name] [-s src-pane] [-t
>         dst-window]
>               (alias: breakp)
>         Break src-pane off from its containing window to make it the only
>         pane in dst-window.  If -d is given, the new window does not
>         become the current window.  The -P option prints information
>         about the new window after it has been created.  By default, it
>         uses the format ‘#{session_name}:#{window_index}' but a different
>         format may be specified with -F.

## link-window

> link-window [-adk] [-s src-window] [-t dst-window]
>               (alias: linkw)
>         Link the window at src-window to the specified dst-window.  If
>         dst-window is specified and no such window exists, the src-window
>         is linked there.  With -a, the window is moved to the next index
>         up (following windows are moved if necessary).  If -k is given
>         and dst-window exists, it is killed, otherwise an error is gener‐
>         ated.  If -d is given, the newly linked window is not selected.

## new-window

> new-window [-adkP] [-c start-directory] [-e environment] [-F format] [-n
>         window-name] [-t target-window] [shell-command]
>               (alias: neww)
>         Create a new window.  With -a, the new window is inserted at the
>         next index up from the specified target-window, moving windows up
>         if necessary, otherwise target-window is the new window location.

>         If -d is given, the session does not make the new window the cur‐
>         rent window.  target-window represents the window to be created;
>         if the target already exists an error is shown, unless the -k
>         flag is used, in which case it is destroyed.  shell-command is
>         the command to execute.  If shell-command is not specified, the
>         value of the default-command option is used.  -c specifies the
>         working directory in which the new window is created.

>         When the shell command completes, the window closes.  See the
>         remain-on-exit option to change this behaviour.

>         -e takes the form ‘VARIABLE=value' and sets an environment vari‐
>         able for the newly created window; it may be specified multiple
>         times.

>         The TERM environment variable must be set to ‘screen' or ‘tmux'
>         for all programs running inside tmux.  New windows will automati‐
>         cally have ‘TERM=screen' added to their environment, but care
>         must be taken not to reset this in shell start-up files or by the
>         -e option.

>         The -P option prints information about the new window after it
>         has been created.  By default, it uses the format
>         ‘#{session_name}:#{window_index}' but a different format may be
>         specified with -F.

##
## ?

> Most commands  accept the optional  -t (and sometimes  -s) argument with  one of
> target-client, target-session, target-window, or target-pane.
> These specify the client, session, window or pane which a command should affect.

##
##
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
### pane above/below/to the right/to the left?

Pass the  `-d` flag (disable) or  `-e` flag (enable),  as well as either  of the
`-U` (up), `-D` (down), `-L` (left), `-R` (right) flags, to `selectp`.

For example, to disable the input in the pane above:

    $ tmux selectp -Ud

And to enable the input in the pane to the right:

    $ tmux selectp -Re

---

Note that these commands don't change the active pane.

### previously selected pane?

     $ tmux last-pane -d
     $ tmux last-pane -e

##
## How to make tmux automatically duplicate the input I send to a pane, to all the other panes in the same window?

Set the window option 'synchronize-panes':

    $ tmux set -w synchronize-panes on

### In which panes will tmux *not* duplicate my input?

Any pane which is in a mode.

Besides, if  your active  pane is  in a  mode, the  input you  send will  not be
duplicated *anywhere*.

##
## ?

Anything else related to input:

     command-prompt [-1i] [-I inputs] [-p prompts] [-t target-client] [template]

Open the command prompt in a client.
This may be used from inside tmux to execute commands interactively.

If template is specified, it is used as the command.
If present, `-I` is a comma-separated list of the initial text for each prompt.
If  `-p` is  given,  prompts is  a  comma-separated list  of  prompts which  are
displayed in  order; otherwise  a single prompt  is displayed,  constructed from
template if it is present, or `:` if not.

Before the command is executed, the first  occurrence of the string `%%` and all
occurrences of `%1` are  replaced by the response to the  first prompt, all `%2`
are replaced  with the  response to  the second  prompt, and  so on  for further
prompts.
Up to nine prompt responses may be replaced (`%1` to `%9`).
`%%%` is like `%%` but any quotation marks are escaped.

`-1` makes  the prompt  only accept one  key press, in  this case  the resulting
input is a single character.
`-i` executes  the command every time  the prompt input changes  instead of when
the user exits the command prompt.

---

Run `$ rg command-prompt`  in the tmux repo, and you'll  find key bindings which
pass the `-N` flag to `command-prompt`.

    $ tmux bind -Tcopy-mode-vi M-3 command-prompt -Np'(repeat)' -I3 'send -N \"%%%\"'
                                                   ^

But this flag is not documented.
What does it mean?
It seems to  mean that you can  only press 1 key,  and that it won't  be used to
replace `%%` (or `%%%`), With `-N`, you can press only 1 key.

Actually, there's no need to run `$ rg`.
Just look at the output of `$ tmux lsk | grep command-prompt`:

    bind-key -T copy-mode-vi 3 command-prompt -N -I 3 -p (repeat) "send -N \"%%%\""

Btw, those escaped double-quotes are ugly. Use braces instead.

    bind-key -T copy-mode-vi 3 command-prompt -N -I 3 -p (repeat) {send -N '%%%'}

##
##
##
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

