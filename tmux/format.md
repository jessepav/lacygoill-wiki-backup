# Syntax
## Do all commands expand formats?

No.

It depends on the command, and even on the argument of the command.

---

`run-shell` does expand formats:

    $ tmux run 'echo #S'
    study~

`if-shell` too:

    $ tmux if '[ "#S" = "study" ]' 'display -p "you are in the study session"'
    you are in the study session~

`pipe-pane` too:

    $ tmux pipe-pane -o 'cat >>~/output.#I-#P'

But not `detach-client`:

    $ tmux detach-client -E 'echo #S >/tmp/log'

`new-window` doesn't expand a format in 'shell-command':

    $ tmux neww 'echo #S >/tmp/log' ; cat /tmp/log
    #S~

But it does in the argument of `-F`:

    $ tmux neww -P -F '#W'
    zsh~

And it does in the argument of `-c`:

    $ cd /tmp && tmux neww -c '#{pane_current_path}' && cd
    $ pwd
    /tmp~

### When do they expand formats?

At execution time, except for `%if` (cf. nicm).

###
## Is a format expanded in a `var=val` statement?

No.

    $ tmux source =(cat <<'EOF'
    pane_id='#{pane_id}'
    bind C-g display "$pane_id"
    EOF
    ) \; lsk | grep -i ' c-g '
    bind-key  -T prefix  C-g  display-message "#{pane_id}"~
                                               ^^^^^^^^^^
                                               has not been expanded

Rationale:
`var=val` is a shell construct which tmux tries to emulate.
And the shell does not expand a tmux format, because it has no knowledge of what it means.
So, if tmux expanded a format in `var=val`, it would be inconsistent with the shell.

    $ pane_id='#{pane_id}'
    $ tmux bind C-g display "$pane_id" \; lsk | grep -i ' c-g '
    bind-key  -T prefix  C-g  display-message "#{pane_id}"~
                                               ^^^^^^^^^^
                                               has not been expanded

###
## What's the meaning of `-F` for the commands
### `break-pane`, `new-session`, `new-window`, `split-window`?

They  all  accept  a  `-P`  option   which  prints  information  about  the  new
pane/session/window after it has been created.

This information is formatted by default with the format `#{session_name}:#{window_index}`
(except `new-session` which uses `#{session_name}`).

But you can choose an arbitrary format by passing it to `-F`.
For example:

    $ tmux splitw -P -F '#D'

### `choose-buffer`, `choose-client`, `choose-tree`?

It specifies the format for each item in the displayed list/tree.

---

For `choose-buffer`, you would probably use replacement variables beginning with `buffer_`.

Example:

    $ tmux choose-buffer -F '#{buffer_size}'

---

For `choose-client`, the relevant prefix would be `client_`.

Example:

    $ tmux choose-client -F '#{client_termname} : #{client_pid}'

---

And for `choose-tree`, the relevant prefix could be `pane_`, `session_`, or `window_`.

Example:

    $ tmux choose-tree -F '#W : #{pane_id}'

### `list-commands`, `list-buffers`, `list-clients`, `list-panes`, `list-sessions`, `list-windows`

It specifies the format for each item in the displayed list.

---

For `list-commands`, you would probably use replacement variables beginning with `command_`.

Example:

    $ tmux list-commands -F '#{command_list_name} : #{command_list_alias}'

---

For `list-buffers`, the relevant prefix would be `buffer_`.
For `list-clients`, the relevant prefix would be `client_`.
Etc.

###
### `if-shell`?

`-F` changes how the shell command is used.

Without `-F`, it's run and considered succes if the *exit code* is 0:

    $ tmux if '[ "$TERM" = "#{default-terminal}" ]' 'display -p "your tmux.conf has already been sourced once"'
    your tmux.conf has already been sourced once~

Without `-F`, it's *not* run, and is considered succes if neither empty nor 0:

    $ tmux if -F '#{alternate_on}' 'display -p "the pane is in alternate screen"'
    the pane is in alternate screen~

In both cases, formats are expanded before `if-shell` is run, at parse time.

### `set-option`?

`-F` expands formats in the option value (so, at parse time).

    $ tmux set @foo '#S'
    $ tmux show -v @foo
    #S~

               vv
    $ tmux set -F @foo '#S'
    $ tmux show -v @foo
    study~

#### When should I pass `-F` to `set-option`?

Every time your option value contains a format.

Exception:

Some options values are evaluated later, like `status-right`.
And during this evaluation, formats are automatically expanded.
For those, you  will probably want to  let tmux expand the  format at evaluation
time.
Indeed, if you expand a format in  the value of `status-right` at parse time, it
will be  static, while you probably  want it to be  evaluated dynamically, every
few seconds ('status-interval').

##
# Test
## How to write a conditional?

Use this syntax:

    #{?var,alt1,alt2}

If  `var` exists  and is  not 0,  the conditional  is evaluated  into the  first
alternative, otherwise the second one.

Example:

    $ tmux display -p '#{?session_attached,attached,not attached}'
    attached~

And:

    $ tmux display -p '#{?automatic-rename,yes,no}'
    no~

### Which variable can I use?

You can  use variables  in the  global or  session environment,  as well  as any
option (no matter the type, and no matter the scope).

However, you  can't use  a variable  which is  only in  the tmux  server process
environment, and not in the global environment:

    $ tmux setenv -gu EDITOR ; echo $EDITOR
    vim~
    $ tmux display -p '#{?EDITOR,set,not set}'
    not set~

### Which value wins in case of conflict between
#### a variable in the global environment and session environment?

The value in the session environment.

    $ tmux setenv -g foo 1 \; setenv foo 0 \; display -p '#{?foo,set,not set}'
    not set~

#### the global value of an option and its local counterpart?

The local value wins.

    $ tmux set -g automatic-rename 1 \; set automatic-rename 0 \; display -p '#{?automatic-rename,set,not set}'
    not set~

##
## How to compare
### two strings?

Use one of these syntaxes:

    #{==:str1,str2}

    #{!=:str1,str2}

Examples:

    $ tmux display -p '#{==:#{host},ubuntu}'
    1~

    $ tmux display -p '#{!=:#{client_termname},rxvt-unicode-256color}'
    1~

### a shell wildcard pattern to a string?

    #{m:pat,str}

---

    $ tmux display -p '#{m:*256*,#{client_termname}}'
    1~

In the pattern, you can use the metacharacters documented at `$ man 3 fnmatch`.

Except for the ones documented below a flag which is a GNU extension.
To be  able to use  these, you need  to recompile tmux,  to add support  for the
relevant flag.

For example, if you need the `FNM_EXTMATCH`, you will run:

    $ sed -i '/fnmatch(/s/0/FNM_EXTMATCH/' ~/GitRepos/tmux/format.c

### a regex to a string?

Pass the `r` flag to the `m` modifier:

                                             vv
    $ tmux set @foo 'abcd' \; display -p '#{m/r:^[aA].*[dD]$,#{@foo}}'
    1~

#### How to write a quantifier such as `{1,4}`?

Tmux expects an ERE regex, so there's no need to escape the curly braces.
However, in a format, `,` and `}` are special, so you need to escape them with `#`:

                                 v  v
    $ tmux display -p '#{m/r:^.{1#,4#}$,test}'
    1~

###
### how to ignore the case, when doing a shell wildcard pattern or regex comparison?

Pass the `i` flag to the `m` modifier:

                                             vv
    $ tmux set @foo 'ABCD' \; display -p '#{m/i:a*d,#{@foo}}'
    1~

                                             vvv
    $ tmux set @foo 'ABCD' \; display -p '#{m/ri:^a.*d$,#{@foo}}'
    1~

##
## How to check if
### one of two alternatives is true?

    #{||:alt1,alt2}

---

    $ tmux display -p '#{||:#{pane_in_mode},#{alternate_on}}'

### two alternatives are simultaneously true?

    #{&&:alt1,alt2}

---

    $ tmux display -p '#{&&:#{pane_active},#{alternate_on}}'
    1~

##
# Modifiers
## What is `#{l:}`?

It's a format using the undocumented modifier `l:`.
The latter stands for “literal”.

You can find it in the `format_replace()` function from the `format.c` file.

    case 'l':
            modifiers |= FORMAT_LITERAL;
            break;

It allows you to prevent characters in a string from being interpreted specially.

You can find several usage examples in tmux codebase:

    $ rg '#\{l:'

### When is it useful?  (2)

When you have several special characters which you need to escape.

For example, suppose you want tmux to print:

    #{?pane_in_mode,#{?#{==:#{session_name},Summer},ABC,XYZ},xyz}

You need to escape each number sign:

    $ tmux display -p '##{?pane_in_mode,##{?##{==:##{session_name},Summer},ABC,XYZ},xyz}'
                       ^^               ^^  ^^    ^^

More generally, it  can be tricky to  find the characters to escape,  and if you
later change the string, you may need to escape additional characters, or on the
contrary you may need to remove some escape sequences.

OTOH, `#{l:}` is simpler to use and more future-proof:

    $ tmux display -p '#{l:{?pane_in_mode,#{?#{==:#{session_name},Summer},ABC,XYZ},xyz}}'
    {?pane_in_mode,#{?#{==:#{session_name},Summer},ABC,XYZ},xyz}~

---

It can also be useful when you test an `%if` construct:

    %if #{l:1}
    display -p success
    %else
    display -p failure
    %endif

Indeed, `%if` expects a format as an argument.

###
## How to write a literal `#`, `,`, or `}`?

Escape them with `#`:

    ## → #
    #, → ,
    #} → }

##
## How to get
### the value of a tmux option?

Just include its name inside `#{}`:

    $ tmux display -p '#{buffer-limit}'
    10~

###
### the address of the line where
#### a shell wildcard pattern matches in the pane content?

    #{C:pat}

---

    $ tmux display -p '#{C:needle}'
    24~

If the string is not found, `#{C:pat}` evaluates to 0.

In the pattern, you can use the metacharacters documented at `$ man 3 fnmatch`.

#### a regex matches in the pane content?

    #{C/r:pat}
    #{C/ri:pat}
         ^
         ignore case

---

    $ echo needle ; tmux display -p '#{C/r:^n.*le}'
    needle~
    2~

    $ echo NEEDLE ; tmux display -p '#{C/ri:^n.*le}'
    needle~
    2~

##
## How to truncate a string after the first `N` characters?

    #{=N:str}

---

    $ tmux display -p '#{=2:client_termname}'
    st~

### before the last `N` characters?

Use a negative number:

                         vvv
    $ tmux display -p '#{=-8:client_termname}'
    256color~

#### and replace the truncated text with `...`?

    #{=/N/...:string}
       ^ ^^^^

`...` needs to be separated from `N` with a slash, because it could be any text,
and so  could begin  with a digit;  in that  case, tmux needs  to know  when `N`
terminates, and when the replacement text for the truncated text starts.

OTOH, I don't know why `N` needs to be separated from `=` with a slash.

---

    $ tmux set @foo 'one two three' \; display -p '#{=/7/...:@foo}'
    one two...~

    $ tmux set @foo 'one two three' \; display -p '#{=/-9/...:@foo}'
    ...two three~

##
## How to convert a Unix time in a human-readable form?

Use the `t:` modifier:

    #{t:Unit time}

---

    $ tmux display -p '#{t:start_time}'
    Wed Jun 12 12:28:00 2019~

## How to extract the basename or dirname of a path?

Use the `b:` or `d:` modifier:

    #{b:path}

    #{d:path}

---

    $ tmux set -g @foo /tmp/file.txt
    $ tmux display -p '#{b:@foo}'
    file.txt~

    $ tmux display -p '#{d:@foo}'
    /tmp~

## How to escape characters which are special to the sh shell?

Use the `q:` modifier:

    $ tmux set -g @foo 'a$b"c`d&e>f;g|h(i'

                         v
    $ tmux display -p '#{q:@foo}'
    a\$b\"c\`d\&e\>f\;g\|h\(i~

##
## How to expand the *content* of an option, rather than the option itself?

Use the `E:` modifier:

    $ tmux set -g @foo '#[fg=colour15]#{?client_prefix,#[bold],}#S#{?client_prefix,,#[bold]}'

    $ tmux display -p '#{@foo}'
    #[fg=colour15]#{?client_prefix,#[bold],}#S#{?client_prefix,,#[bold]}~

    $ tmux display -p '#{E:@foo}'
    #[fg=colour15]study#[bold]~

### My option contains a strftime(3) specifier (e.g. `%Y`).  How to expand it as well?

Use `T:`:

    $ tmux set @foo '#S %Y'

    $ tmux display -p '#{@foo}'
    #S %Y~
    $ tmux display -p '#{E:@foo}'
    study %Y~
    $ tmux display -p '#{T:@foo}'
    study 2019~

#### What are the two options whose value can include a strftime(3) specifier?

`status-left` and `status-right`:

    $ tmux set -g status-left '%Y'

##
## How to replace `pat` with `rep` in a format?

Use the prefix `s/pat/rep/:`:

    $ tmux set @foo 'pat a pat b' \; display -p '#{s/pat/rep/:@foo}'
    rep a rep b~

    $ tmux set @foo 'pat a pat b' \; display -p '#{s/[^ ]*/rep/:@foo}'
    rep rep rep rep~

### ignoring the case?

Use the `i` flag:

                                                             v
    $ tmux set @foo 'PAT a PAT b' \; display -p '#{s/pat/rep/i:@foo}'
    rep a rep b~

### How to write a quantifier such as `{12,34}` inside a `#{C/r:}`, `#{m/r:}`, `#{s/pat/rep/:}` format?

In `#{C/r:}` and `#{s/pat/rep/:}`:

    {12,34#}

In `#{m/r:}`:

    {12#,34#}

The last syntax works in the 3 contexts.

---

    $ echo suuuper >/tmp/file ; clear ; cat /tmp/file ; tmux display -p '#{C/r:^su{1,3#}per$}'
    suuuper~
    1~

    $ tmux set @foo 'suuuper' \; display -p '#{m/r:u{1#,3#},#{@foo}}'
    1~

    $ tmux set @foo 'suuuper' \; display -p '#{s/u{1,3#}/u/:@foo}'
    super~

####
## What are the two modifiers for which I need to use `#{}` a second time to expand a variable they contain?

`m` and `C`:

    $ tmux set @foo 'abc' \; display -p '#{m:a*,@foo}'
    0~
    $ tmux set @foo 'abc' \; display -p '#{m:a*,#{@foo}}'
    1~

    $ echo abc >/tmp/file ; tmux set @foo abc ; clear
    $ cat /tmp/file ; tmux display -p '#{C:@foo}'
    abc~
    1~
    $ cat /tmp/file ; tmux display -p '#{C:#{@foo}}'
    abc~
    2~

Rationale:

In an `m` and `C` format, you search for some text.
And this text may look like a variable/option, e.g. `@foo`.
But if tmux expanded  automatically `@foo`, you would not be  able to search for
the literal text `@foo`.

##
## How to concatenate the expansions of a format in the context of
### each session?

    #{S:format}

---

                           ┌ alias for `#{session_name}`
                           ├┐
    $ tmux display -p '#{S:#S }'
    my_session_1 my_session_2 ... ~

Maybe I have a network issue, but I can't read your log files, because of `404 Page not found` error.

### each window of the current session?

    #{W:format}

---

                           ┌ alias for `#{window_name}`
                         v ├┐
    $ tmux display -p '#{W:#W }'
    my_window_1 my_window_2 ... ~

### each pane of the current window?

    #{P:format}

---

                           ┌ alias for `#{pane_index}`
                           ├┐
    $ tmux display -p '#{P:#P }'
    1 2 ...~

###
### How to make tmux perform a different expansion in the context of the current window or active pane?

Use two comma-separated formats.
The second will be used for the current window or active pane.

For example, to get a list of windows formatted like in the status line:

    $ tmux display -p '#{W:#{E:window-status-format}   ,#{E:window-status-current-format}   }'
                           ├──────────────────────────┘ ├──────────────────────────────────┘
                           │                            └ expanded in the current window
                           └ expanded in the non-current windows

##
# Replacement variables
## How to test whether
### a window is
#### zoomed?

    #{window_zoomed_flag}

#### the first one?  last one?

    #{window_start_flag}
    #{window_end_flag}

#### the last-but-one to be focused?

    #{window_last_flag}

###
### a pane is in a mode?

    #{pane_in_mode}

#### In which modes can a pane be?  (4)

   - copy mode
   - client mode (entered via `choose-client`)
   - tree mode (entered via `choose-tree`)
   - buffer-mode (entered via `choose-buffer`)

###
### a pane is active?

    #{pane_active}

### a pane shares a border with the top border of the window?  bottom border?  left border?  right border?

    #{pane_at_top}
    #{pane_at_bottom}
    #{pane_at_left}
    #{pane_at_right}

###
### a selection has been started in copy mode?

    #{selection_present}

### a rectangle selection is activated?

    #{rectangle_toggle}

###
### the current application is using the terminal alternate screen?

    #{alternate_on}

### the prefix key has been pressed?

    #{client_prefix}

##
## How to get
### the PID of
#### the first process in the pane?

    #{pane_pid}

#### the tmux client process?

    #{client_pid}

#### the tmux server process?

    #{pid}

###
### the name of the outer terminal?

    #{client_termname}

###
### the name of a window?

    #{window_name} / #W

### the flags of a window?  (e.g. `*`, `-`, ...)

    #{window_flags} / #F

### the number of panes in the current window?

    #{window_panes}

###
### the index of a pane?  window?

    #{pane_index} / #P
    #{window_index} / #I

### the unique ID of a pane?  window?  sesssion?

    #{window_id}
    #{pane_id} / #D
    #{session_id}

### the width of a window?  pane?

    #{window_width}
    #{pane_width}

### the height of a window?  pane?

    #{window_height}
    #{pane_height}

###
### the tty used by a pane?

    #{pane_tty}

### the current working directory of the process run in a pane?

    #{pane_current_path}

###
### the position of the first line in the pane relative to the window?  last line?

    #{pane_top}
    #{pane_bottom}

### the position of the first character in the pane?  last character?

    #{pane_left}
    #{pane_right}

##
### the character under the cursor?

    #{cursor_character}

### the coordinates of the cursor in the active pane?

    #{cursor_x}
    #{cursor_y}

### the number of non-visible lines in the scrollback buffer of a pane?

    #{history_size}

### the last search string in copy mode?

    #{pane_search_string}

###
# Issues
## I'm writing nested formats; I have 3 consecutive `}`.  How to prevent Vim from interpreting them as fold markers?

Use a temporary environment variable.

Example:

    is_vim='#{==:vim,#{pane_current_command}}'
    display -p "#{||:#{==:nano,#{pane_current_command}},${is_vim}}"
    setenv -gu is_vim

Don't forget to use double quotes to  surround the nested formats, to allow tmux
to expand the environment variable.

This also gives the benefit of making the code more readable.

---

Do *not* try to add a space in-between the brackets.
It would break the meaning of the formats.
Indeed, any character inside `#{}` is semantic, including a space:

    $ tmux display -p '#{==:vim,#{pane_current_command}}'
    1~

                                                       v
    $ tmux display -p '#{==:vim,#{pane_current_command} }'
    0~

##
##
##
# The following variables are available, where appropriate:

    window_active                   1 if window active
    pane_pipe                       1 if pane is being piped
    pane_dead                       1 if pane is dead
    pane_marked                     1 if this is the marked pane
    pane_marked_set                 1 if a market pane is set
    pane_synchronized               1 if pane is synchronized
    pane_input_off                  1 if input to pane is disabled
    pane_format                     1 if format is for a pane (not assuming the current)
    session_format                  1 if format is for a session (not assuming the current)
    window_format                   1 if format is for a window (not assuming the current)

    command                         Name of command in use, if any
    command_list_alias              Command alias if listing commands
    command_list_name               Command name if listing commands
    command_list_usage              Command usage if listing commands
    hook                            Name of running hook, if any
    hook_pane                       ID of pane where hook was run, if any
    hook_session                    ID of session where hook was run, if any
    hook_session_name               Name of session where hook was run, if any
    hook_window                     ID of window where hook was run, if any
    hook_window_name                Name of window where hook was run, if any
    pane_current_command            Current command if available
    pane_dead_status                Exit status of process in dead pane
    pane_start_command              Command pane started with
    scroll_position                 Scroll position in copy mode
    scroll_region_lower             Bottom of scroll region in pane
    scroll_region_upper             Top of scroll region in pane
    session_alerts                  List of window indexes with alerts
    session_group                   Name of session group
    session_group_list              List of sessions in group
    session_group_size              Size of session group
    session_stack                   Window indexes in most recent order
    session_windows                 Number of windows in session
    window_layout                   Window layout description, ignoring zoomed window panes
    window_stack_index              Index in session most recent stack

Find which ones could be useful.

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

# We spent a lot of time to write the “Quoting” in `~/wiki/tmux/tmux.md`.

What should we have done to write it quicker?

Hint: Our initial notes were all over the place.
Maybe  this  was the  sign  that  we didn't  really  know  which questions  were
bothering us.
Maybe we should have spent more time on the questions than on the answers; first
trying to find a good structure (main questions, subquestions, ...), then moving
as much of our notes in this structure.

