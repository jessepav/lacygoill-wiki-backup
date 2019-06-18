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

For `list-buffers`, the relevant prefix would `buffer_`.
For `list-clients`, the relevant prefix would `client_`.
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
For those, you will probably want to let tmux expand the format at evaluation time.
Indeed, if you expand a format in  the value of `status-right` at parse time, it
will be static, while you probably want it to be evaluated dynamically, every 15
seconds ('status-interval').

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

### a pattern to a string?

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

It's a replacement variable using the undocumented modifier `l:`.
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

### the address of the line where a pattern matches in the pane content?

    #{C:pat}

---

    $ tmux display -p '#{C:needle}'
    24~

If the string is not found, `#{C:pat}` evaluates to 0.

In the pattern, you can use the metacharacters documented at `$ man 3 fnmatch`.

##
## How to truncate a string after the first `n` characters?

    #{=n:str}

---

    $ tmux display -p '#{=2:client_termname}'
    st~

### before the last `n` characters?

Use a negative number:

                         vvv
    $ tmux display -p '#{=-8:client_termname}'
    256color~

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
# Replacement variables
## How is `#{pane_in_mode}` evaluated?

Into 1 iff the pane is in a mode; 0 otherwise.

### In which modes can a tmux pane be?  (4)

   - copy mode
   - client mode (entered via `choose-client`)
   - tree mode (entered via `choose-tree`)
   - buffer-mode (entered via `choose-buffer`)

###
## How is `#{alternate_on}` evaluated?

Into 1 if the current application is using the terminal alternate screen.

---

The alternate  screen is used  by many interactive  programs such as  vim, htop,
less ...
It's like a different buffer of  the terminal content, which disappears when the
application exits,  so the whole  terminal gets restored  and it looks  like the
application hasn't output anything.

<https://stackoverflow.com/questions/11023929/using-the-alternate-screen-in-a-bash-script>

It can be manually used by running `$ tput smcup`.
And you can leave it by running `$ tput rmcup`.

##
##
##
# How to expand the content of an option, rather than the option itself?

Use the `E:` modifier:

    $ tmux display -p '#{status-left}'
    #[fg=colour15]#{?client_prefix,#[bold],}#S#{?client_prefix,,#[bold]}~

    $ tmux display -p '#{E:status-left}'
    #[fg=colour15]study#[bold]~

## My option contains a strftime(3) specifier.  How to expand it as well?

Use `T:`:

    $ tmux set -g status-right '#S %Y'

    $ tmux display -p '#{status-right}'
    #S %Y~
    $ tmux display -p '#{E:status-right}'
    study %Y~
    $ tmux display -p '#{T:status-right}'
    study 2019~

##
# ?

Old code extracted from our tmux.conf.
We don't  use it anymore,  because I think monitoring  the bell is  better (less
noise) than monitoring the activity:

<https://stackoverflow.com/a/39180062/9780968>

See whether we should extract some info in our notes.

    Ignore the activity in a (N)Vim/cmus/mpv/newsboat/weechat window.
    What's `#{?var,off,on}`?

    A replacement variable, using a conditional operator.
    It will  be replaced with  'off' if `var` evaluates  to anything else  than 0,
    'on' otherwise.

    Here `var` is:

        #{||:#{m:*vim,#{pane_current_command}},#{==:cmus,#{pane_current_command}} }

    ---

      `#{||:var1,var2}`?

    A replacement variable  which will be evaluated  to true if any  of `var1` and
    `var2` is true.

    Here, `var1` is:

        #{m:*vim,#{pane_current_command}}

    And `var2` is:

        #{==:cmus,#{pane_current_command}}

    ---

      `#{m:pat,str}`?

    A replacement variable which will be evaluated to true if `pat` matches `str`.
    Here, `pat` is `*vim`, and `str` is `#{pane_current_command}`.

    ---

      `#{==:str1,str2}`?

    A replacement variable which will be evaluated to true if `str1` and `str2` are identical.
    Here, `str1` is `#{pane_current_command}`, and `str2` is `cmus`.

    ---

        is_distraction='#{||:#{==:#{pane_current_command},cmus},#{||:#{==:#{pane_current_command},mpv},#{||:#{==:#{pane_current_command},newsboat},#{==:#{pane_current_command},weechat}}}}'
        set-hook -ga pane-focus-out \
          'setw -F monitor-activity \
              "#{?#{||:#{m:*vim,#{pane_current_command}},$is_distraction},off,on}"'
        setenv -gu is_distraction

    ---

    TODO: Ask nicm whether `#{||:}` could be made to accept more than two operands.

    It would make the code more readable/maintainable.

    Even better, you could rely on the FNM_EXTMATCH flag which you can pass to the
    C function `fnmatch()`:

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

    This would allow you to write sth like:

        $ tmux display -p '#{m:+(foo|bar|baz),bar}'

    Try to  ask nicm whether an  option could be set  at compile-time so  that the
    FNM_EXTMATCH flag is set at runtime.
    The compile-time option would not be set by default of course.

    Or write  a sed  script which  would edit all  the tmux  C files  which invoke
    `fnmatch()` (`$ rg 'fnmatch\('`).
    Ask nicm whether such a script is reliable; is it likely to break in the future?

    ---

    Do *not* add a space in-between three consecutive `}`.

    For example, if you exchange the position of `#{pane_current_command}` and `cmus`:

        "#{?#{||:#{m:*vim,#{pane_current_command}},#{==:cmus,#{pane_current_command} }},off,on}"'
                                                                                    ^
                                                                                    ✘

    It would be tempting to add a space to prevent Vim from detecting the end of a fold.
    Unfortunately, it  would also break  the hook,  probably because the  space is
    semantic in this position; same thing after the second `}`.

# ?

When does tmux expand strftime(3) specifiers (e.g. `%Y`)?

In the value of `status-left`, `status-right`, and in any format using the `T:` modifier.

    $ tmux set -g @foo '%Y'
    $ tmux display -p '#{T:@foo}'
    2019~

---

Should we document the fact that `T:` is like `E:` + the strftime expansion?
Also, maybe we shouldn't have said that `E:` was useful to expand the content of an *option*.
I think `E:` is more general; it expands *anything* twice.

    $ tmux set -g @foo '#[fg=colour15]#{?client_prefix,#[bold],}#S#{?client_prefix,,#[bold]}'
    $ tmux display -p '#{E:@foo}'

# ?

`S:`, `W:` or `P:`  will loop over each  session, window or pane  and insert the
format once for each.

For windows and  panes, two comma-separated formats may be  given: the second is
used for the current window or active pane.

For example, to get a list of windows formatted like the status line:

    #{W:#{E:window-status-format} ,#{E:window-status-current-format} }

# ?

A prefix of the form `s/foo/bar/:` will substitute `foo` with `bar` throughout.

# ?

In addition, the last line of a shell command's output may be inserted using `#()`.

For example, `#(uptime)` will insert the system's uptime.

When constructing  formats, tmux  does not  wait for  `#()` commands  to finish;
instead,  the previous  result  from running  the  same command  is  used, or  a
placeholder if the command has not been run before.

If the command hasn't  exited, the most recent line of output  will be used, but
the status line will not be updated more than once a second.

Commands are executed  with the tmux global environment set  (see the GLOBAL AND
SESSION ENVIRONMENT section).

# The following variables are available, where appropriate:

Probably useful:

    # what's the difference between these 2? (they seem to have the same output)
    client_name                     Name of client
    client_tty                      Pseudo terminal of client

    client_pid                      PID of client process
    pane_pid                        PID of first process in pane
    pid                             Server PID

    client_session                  Name of the client's session
    client_termname                 Terminal name of client
    cursor_character                Character at cursor in pane
    rectangle_toggle                1 if rectangle selection is activated
    window_panes                    Number of panes in window

Find which ones could be useful:

    command                         Name of command in use, if any
    command_list_alias              Command alias if listing commands
    command_list_name               Command name if listing commands
    command_list_usage              Command usage if listing commands

    cursor_flag                     Pane cursor flag
    cursor_x                        Cursor X position in pane
    cursor_y                        Cursor Y position in pane

    history_bytes                   Number of bytes in window history
    history_limit                   Maximum window history lines
    history_size                    Size of history in lines

    hook                            Name of running hook, if any
    hook_pane                       ID of pane where hook was run, if any
    hook_session                    ID of session where hook was run, if any
    hook_session_name               Name of session where hook was run, if any
    hook_window                     ID of window where hook was run, if any
    hook_window_name                Name of window where hook was run, if any
    host                   #H       Hostname of local host
    host_short             #h       Hostname of local host (no domain name)

    insert_flag                     Pane insert flag

    keypad_cursor_flag              Pane keypad cursor flag
    keypad_flag                     Pane keypad flag

    pane_active                     1 if active pane
    pane_at_bottom                  1 if pane is at the bottom of window
    pane_at_left                    1 if pane is at the left of window
    pane_at_right                   1 if pane is at the right of window
    pane_at_top                     1 if pane is at the top of window
    pane_bottom                     Bottom of pane
    pane_current_command            Current command if available
    pane_current_path               Current path if available
    pane_dead                       1 if pane is dead
    pane_dead_status                Exit status of process in dead pane
    pane_format                     1 if format is for a pane (not assuming the current)
    pane_height                     Height of pane
    pane_id                #D       Unique pane ID
    pane_in_mode                    If pane is in a mode
    pane_index             #P       Index of pane
    pane_input_off                  If input to pane is disabled
    pane_left                       Left of pane
    pane_marked                     1 if this is the marked pane"
    pane_marked_set                 1 if a market pane is set"
    pane_menu                       The default pane menu
    pane_mode                       Name of pane mode, if any.
    pane_pipe                       1 if pane is being piped
    pane_right                      Right of pane
    pane_search_string              Last search string in copy mode
    pane_start_command              Command pane started with
    pane_synchronized               If pane is synchronized
    pane_tabs                       Pane tab positions
    pane_title             #T       Title of pane
    pane_top                        Top of pane
    pane_tty                        Pseudo terminal of pane
    pane_width                      Width of pane

    scroll_position                 Scroll position in copy mode
    scroll_region_lower             Bottom of scroll region in pane
    scroll_region_upper             Top of scroll region in pane

    selection_present               1 if selection started in copy mode

    session_alerts                  List of window indexes with alerts
    session_attached                Number of clients session is attached to
    session_format                  1 if format is for a session (not assuming the current)
    session_group                   Name of session group
    session_group_list              List of sessions in group
    session_group_size              Size of session group
    session_grouped                 1 if session in a group
    session_id                      Unique session ID
    session_menu                    The default session menu
    session_stack                   Window indexes in most recent order
    session_windows                 Number of windows in session

    window_active                   1 if window active
    window_activity_flag            1 if window has activity
    window_bigger                   1 if window is larger than client
    window_end_flag                 1 if window has the highest index
    window_flags           #F       Window flags
    window_format                   1 if format is for a window (not assuming the current)
    window_height                   Height of window
    window_id                       Unique window ID
    window_index           #I       Index of window
    window_last_flag                1 if window is the last used
    window_layout                   Window layout description, ignoring zoomed window panes
    window_linked                   1 if window is linked across sessions
    window_menu                     The default window menu
    window_name            #W       Name of window
    window_offset_x                 X offset into window if larger than client
    window_offset_y                 Y offset into window if larger than client
    window_silence_flag             1 if window has silence alert
    window_stack_index              Index in session most recent stack
    window_start_flag               1 if window has the lowest index
    window_width                    Width of window
    window_zoomed_flag              1 if window is zoomed

    wrap_flag                       Pane wrap flag

##
##
##
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

# ?

We spent a lot of time to write the “Quoting” in `~/wiki/tmux/tmux.md`.
What should we have done to write it quicker?

Hint: Our initial notes were all over the place.
Maybe  this  was the  sign  that  we didn't  really  know  which questions  were
bothering us.
Maybe we should have spent more time on the questions than on the answers; first
trying to find a good structure (main questions, subquestions, ...), then moving
as much of our notes in this structure.

