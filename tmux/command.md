# targetting
## What is an ID?

A unique number which  remains unchanged for the life of  the session, window or
pane in the tmux server.

## Which prefix does tmux use for a session ID?  a window ID?  a pane ID?

    ┌─────────┬───┐
    │ session │ $ │
    ├─────────┼───┤
    │ window  │ @ │
    ├─────────┼───┤
    │ pane    │ % │
    └─────────┴───┘

## How to get a session ID?  window ID?  pane ID?

Use the format variable `#{session_id}`, `#{window_id}`, `#{pane_id}` in a format
passed to `display-message`, `list-sessions`, `list-windows` or `list-panes`.
You  can also  get the  id of  the current  pane by  inspecting the  environment
variable `$TMUX_PANE`.

##
## sessions
### Which kind of values can I use for `target-session`?  (4)

An ID:

    $ tmux command -t '$123'
                      ^    ^
                      prevent the shell from trying to expand `$123` into an empty string (unset variable)

A name:

    $ tmux command -t 'mysession'

A name prefix:

    $ tmux command -t 'mysess'

An fnmatch(3) pattern:

    $ tmux command -t '*sess*'

### How to make sure `target-session` is interpreted as an exact name, not a name prefix?

Prefix it with `=`:

    $ tmux command -t '=mysess'
                       ^

###
### I have a session named `mysession` and no session named `mysess`. I try to target `mysess`.  What happens?

Tmux will target `mysession`.

#### Why?

Tmux interprets `target-session` – with  the following order of precedence, from
highest to lowest – as:

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
### Which kind of values can I use for `target-window`, `src-window` and `dst-window`?  (6)

   1. a special token, such as `^`, `$`, `!`, `+`, `-`
   2. `session_name:window_index` (e.g. `mysession:1`)
   3. a window ID, such as @1
   4. `session_name:window_name` (e.g. `mysession:mywindow`)
   5. `session_name:name_prefix` (eg `mysession:mywin`)
   6. an fnmatch(3) pattern matched against the window name

---

> target-window (or  src-window or  dst-window) specifies a  window in  the form
> session:window.
> session follows the  same rules as for target-session, and  window is looked for
> in order as:

> [...]

> Like sessions, a ‘=' prefix will do an exact match only.
> An empty window name specifies the next unused index if appropriate (for example
> the new-window and link-window commands) otherwise the current window in session
> is chosen.

> The following special tokens are available to indicate particular windows.
> Each has a single-character alternative form.

> Token              Meaning
> {start}       ^    The lowest-numbered window
> {end}         $    The highest-numbered window
> {last}        !    The last (previously current) window
> {next}        +    The next window by number
> {previous}    -    The previous window by number

##
## panes
##
# COMMANDS
## ?

> Most commands  accept the optional  -t (and sometimes  -s) argument with  one of
> target-client, target-session, target-window, or target-pane.
> These specify the client, session, window or pane which a command should affect.

## ?

> target-client should be  the name of the client, typically  the pty(4) file to
> which the client  is connected, for example either of  /dev/ttyp1 or ttyp1 for
> the client attached to /dev/ttyp1.
> If no  client is specified,  tmux attempts to work  out the client  currently in
> use; if that fails, an error is reported.
> Clients may be listed with the list-clients command.

## ?

> target-pane (or src-pane or dst-pane) may be a pane ID or takes a similar form
> to target-window but with the optional addition of a period followed by a pane
> index or pane ID, for example: ‘mysession:mywindow.1'.
> If the pane index is omitted, the  currently active pane in the specified window
> is used.
> The following special tokens are available for the pane index:

> Token                  Meaning
> {last}            !    The last (previously active) pane
> {next}            +    The next pane by number
> {previous}        -    The previous pane by number
> {top}                  The top pane
> {bottom}               The bottom pane
> {left}                 The leftmost pane
> {right}                The rightmost pane
> {top-left}             The top-left pane
> {top-right}            The top-right pane
> {bottom-left}          The bottom-left pane
> {bottom-right}         The bottom-right pane
> {up-of}                The pane above the active pane
> {down-of}              The pane below the active pane
> {left-of}              The pane to the left of the active pane
> {right-of}             The pane to the right of the active pane

## ?

> The tokens ‘+' and ‘-' may be followed by an offset, for example:

>       select-window -t:+2

## ?

> In addition, target-session, target-window or target-pane may consist entirely
> of the token ‘{mouse}' (alternative form ‘=') to specify the most recent mouse
> event (see the MOUSE SUPPORT section)  or ‘{marked}' (alternative form ‘~') to
> specify the marked pane (see select-pane -m).

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

The COMMANDS section lists the tmux commands and their arguments.

# PARSING SYNTAX

*the words in bold are different from the manpage*

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

Outside of **single** quotes and inside double quotes, these replacements are performed:

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

