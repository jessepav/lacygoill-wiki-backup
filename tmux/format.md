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
    window_id='#{window_id}'
    bind C-g display "$window_id"
    EOF
    ) \; lsk | grep -i ' c-g '
    bind-key  -T prefix  C-g  display-message "#{window_id}"~
                                               ^^^^^^^^^^^^
                                               has not been expanded

Rationale:
`var=val` is a shell construct which tmux tries to emulate.
And the shell does not expand a tmux format, because it has no knowledge of what it means.
So, if tmux expanded a format in `var=val`, it would be inconsistent with the shell.

    $ window_id='#{window_id}'
    $ tmux bind C-g display "$window_id" \; lsk | grep -i ' c-g '
    bind-key  -T prefix  C-g  display-message "#{window_id}"~
                                               ^^^^^^^^^^^^
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

    $ tmux choose-tree -F '#W : #{window_id}'

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
## Which variable should I use to test whether
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
## Which variable should I use to get
### the PID of
#### the first process in a pane?

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

### the number of windows in a session?

    #{session_windows}

### the number of panes in a window?

    #{window_panes}

###
### the index of a pane?  window?

    #{pane_index} / #P
    #{window_index} / #I

### the unique ID of a pane? (3)  window?  sesssion?

    #{pane_id} / #D / $TMUX_PANE
    #{window_id}
    #{session_id}

### the width of a window?  pane?

    #{window_width}
    #{pane_width}

### the height of a window?  pane?

    #{window_height}
    #{pane_height}

###
### the command currently running in a pane?

    #{pane_current_command}

### the initial command run in a pane?

    #{pane_start_command}

### the current working directory of the process run in a pane?

    #{pane_current_path}

### the tty used by a pane?

    #{pane_tty}

###
### the position of the first line in a pane relative to the window?  last line?

    #{pane_top}
    #{pane_bottom}

### the position of the first character in a pane?  last character?

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
### ?

Here are some (all?) of the info you could ask for:

    cmd (current, initial)
    cwd
    flags
    ^C prevents `InsertLeave` from being fired.
    height
    id
    index
    name / title
    position (first/last line, first/last character)
    tty
    width

    a window is zoomed
    a window is the first/last one
    a window is the last-but-one to be focused

    a pane is in a mode
    a pane is active
    a pane shares a border with the top/bottom/left/right border of the window

    a selection has been started in copy mode
    a rectangle selection is activated

    the current application is using the terminal alternate screen

For each info, you could want to specify a context:

    current session/window/pane

    session/window/pane by name
    session/window/pane by ID
    session/window/pane by index

---

    Does the error message tell you the name of the script/function from which the error was raised?
    This plugin might help to jump to the origin of the error: https://github.com/tweekmonster/exception.vim/

    # current pane
    $ tmux display -p '#{pane_current_command}'

    # pane %123
    $ tmux display -pt%123 '#{pane_current_command}'

    # title 'my title'
    $ delim=$(tr x '\001' <<<x) \
      && tmux lsp -aF "#{pane_title}${delim}#{pane_current_command}" \
      | awk -F"$delim" "/^my title$delim"'/{print $2}'

    # title 'my title' in current window
    # title 'my title' in given window of current session
    # title 'my title' in given window of given session
    $ tmux ???

    # index 1 in current window
    $ tmux display -pt:.1 -F '#{pane_current_command}'

    # index 1 in window 2 of current session
    $ delim=$(tr x '\001' <<<x) \
      && tmux lsp -s -t $(tmux display -p '#S') -F "#I.#P${delim}#{pane_current_command}" \
      | awk -F"$delim" "/^2.1$delim"'/{print $2}'

    # index 1 in window 2 of session 'my session'
    $ delim=$(tr x '\001' <<<x) \
      && tmux lsp -s -t 'my session' -F "#I.#P$delim"'#{pane_current_command}' \
      | awk -F"$delim" "/^2.1$delim"'/{print $2}'

I think  there are many  other kinds of  info you could  want to get  in various
contexts (current session/window/pane, given session/window/pane, ...).
Find the minimum amount of rules to know to handle all possibilities.
But first, study `$ man tmux /COMMANDS`; you probably need this to know what can
be passed to `-t`.

---

Rule 1:  to extract an  information, you  should use either  of `list-sessions`,
`list-windows`, `list-panes`, `list-clients` in conjunction with `$ awk`.

Rule 2: to extract  an information in the current window  (any pane), you should
use `display-message`.

Rule 3:  targeting a window/pane  with its  name/title is not  reliable, because
there's no guarantee for it to be unique.
OTOH, targeting  a session with its  name should be reliable,  because you can't
have two sessions with the same name:

    $ tmux new -s study
    Duplicate session: study~

---

We need  to fully understand  the syntax of  `display-message`, `list-sessions`,
`list-windows`, `list-panes`, `list-clients`.
For example, study the `-I` flag which one can pass to `display-message`.

    $ echo hello | tmux splitw -dI
    $ echo world | tmux display -I -t :.2

> display-message [-aIpv] [-c target-client] [-t target-pane] [message]
>               (alias: display)

>         Display a message.  If -p is given, the output is printed to std‐
>         out, otherwise it is displayed in the target-client status line.
>         The format of message is described in the FORMATS section; infor‐
>         mation is taken from target-pane if -t is given, otherwise the
>         active pane for the session attached to target-client.

>         -v prints verbose logging as the format is parsed and -a lists
>         the format variables and their values.

>         -I forwards any input read from stdin to the empty pane given by
>         target-pane.

What is an empty pane?
It seems to be a pane which was not started with any particular command.
By default, when you run `:splitw` (or sth similar like `:neww`), tmux runs `$ zsh`.
It may run any arbitrary command, if you provide it.
But on some occasions, a pane can be created without *any* command.
E.g.:

    $ echo hello | tmux splitw -dI

The pane opened by `$ tmux splitw` doesn't run any command.
`$ tmux '#{pane_pid}'` outputs 0; but weirdly enough, `$ tmux '#{pane_current_command}'`
still outputs `zsh`.

---

Again, we're spending too much time on documenting sth.
I think  you should not  try to immediately find  all possible commands  using a
replacement variable.

What is your goal?
You want to find the minimum amount of rules to get any info in any context.
Ok, find a sample of *some* commands to get some info in some contexts.
Then, from them try to infer some rules.
Now, apply those rules to get any info.
Does it work? Great, you've finished.
It doesn't work? Ok, try to tweak the rules (edit/remove/add), and apply the new
rules to get any info in any context.
Repeat until you get a good enough set of rules.

https://github.com/justinmk/config/blob/38c4292d5d6891a152e1c89e2b5b7b46c4b9a805/.config/nvim/init.vim#L777-L817

### COMMANDS

> This section describes the commands supported by tmux.  Most commands
> accept the optional -t (and sometimes -s) argument with one of
> target-client, target-session, target-window, or target-pane.  These spec‐
> ify the client, session, window or pane which a command should affect.

> target-client should be the name of the client, typically the pty(4) file
> to which the client is connected, for example either of /dev/ttyp1 or
> ttyp1 for the client attached to /dev/ttyp1.  If no client is specified,
> tmux attempts to work out the client currently in use; if that fails, an
> error is reported.  Clients may be listed with the list-clients command.

> target-session is tried as, in order:

>       1.   A session ID prefixed with a $.

>       2.   An exact name of a session (as listed by the list-sessions
>            command).

>       3.   The start of a session name, for example ‘mysess' would match
>            a session named ‘mysession'.

>       4.   An fnmatch(3) pattern which is matched against the session
>            name.

> If the session name is prefixed with an ‘=', only an exact match is
> accepted (so ‘=mysess' will only match exactly ‘mysess', not
> ‘mysession').

> If a single session is found, it is used as the target session; multiple
> matches produce an error.  If a session is omitted, the current session
> is used if available; if no current session is available, the most
> recently used is chosen.

> target-window (or src-window or dst-window) specifies a window in the
> form session:window.  session follows the same rules as for
> target-session, and window is looked for in order as:

>       1.   A special token, listed below.

>       2.   A window index, for example ‘mysession:1' is window 1 in ses‐
>            sion ‘mysession'.

>       3.   A window ID, such as @1.

>       4.   An exact window name, such as ‘mysession:mywindow'.

>       5.   The start of a window name, such as ‘mysession:mywin'.

>       6.   As an fnmatch(3) pattern matched against the window name.

> Like sessions, a ‘=' prefix will do an exact match only.  An empty window
> name specifies the next unused index if appropriate (for example the
> new-window and link-window commands) otherwise the current window in
> session is chosen.

> The following special tokens are available to indicate particular win‐
> dows.  Each has a single-character alternative form.

> Token              Meaning
> {start}       ^    The lowest-numbered window
> {end}         $    The highest-numbered window
> {last}        !    The last (previously current) window
> {next}        +    The next window by number
> {previous}    -    The previous window by number

> target-pane (or src-pane or dst-pane) may be a pane ID or takes a similar
> form to target-window but with the optional addition of a period followed
> by a pane index or pane ID, for example: ‘mysession:mywindow.1'.  If the
> pane index is omitted, the currently active pane in the specified window
> is used.  The following special tokens are available for the pane index:

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

> The tokens ‘+' and ‘-' may be followed by an offset, for example:

>       select-window -t:+2

> In addition, target-session, target-window or target-pane may consist
> entirely of the token ‘{mouse}' (alternative form ‘=') to specify the
> most recent mouse event (see the MOUSE SUPPORT section) or ‘{marked}'
> (alternative form ‘~') to specify the marked pane (see select-pane -m).

> Sessions, window and panes are each numbered with a unique ID; session
> IDs are prefixed with a ‘$', windows with a ‘@', and panes with a ‘%'.
> These are unique and are unchanged for the life of the session, window or
> pane in the tmux server.  The pane ID is passed to the child process of
> the pane in the TMUX_PANE environment variable.  IDs may be displayed
> using the ‘session_id', ‘window_id', or ‘pane_id' formats (see the
> FORMATS section) and the display-message, list-sessions, list-windows or
> list-panes commands.

> shell-command arguments are sh(1) commands.  This may be a single argu‐
> ment passed to the shell, for example:

>       new-window 'vi /etc/passwd'

> Will run:

>       /bin/sh -c 'vi /etc/passwd'

> Additionally, the new-window, new-session, split-window, respawn-window
> and respawn-pane commands allow shell-command to be given as multiple
> arguments and executed directly (without ‘sh -c').  This can avoid issues
> with shell quoting.  For example:

>       $ tmux new-window vi /etc/passwd

> Will run vi(1) directly without invoking the shell.

> command [arguments] refers to a tmux command, either passed with the com‐
> mand and arguments separately, for example:

>       bind-key F1 set-option status off

> Or passed as a single string argument in .tmux.conf, for example:

>       bind-key F1 { set-option status off }

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

### How to get the name of the current window?

    $ tmux display -p '#W'

#### of the second window in the session 'fun'?

    $ tmux lsw -F '#W' -t fun | sed -n '2p'

### How to get the number of windows of the current session?

    $ tmux display -p '#{session_windows}'

#### the number of windows of the first session?

    $ tmux ls -F '#{session_windows}' | sed -n '1p'

##### in the session 'fun'?

    $ tmux ls | grep '^fun:' | cut -d' ' -f2

##
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
    hook                            Name of running hook, if any
    hook_pane                       ID of pane where hook was run, if any
    hook_session                    ID of session where hook was run, if any
    hook_session_name               Name of session where hook was run, if any
    hook_window                     ID of window where hook was run, if any
    hook_window_name                Name of window where hook was run, if any
    pane_dead_status                Exit status of process in dead pane
    scroll_position                 Scroll position in copy mode
    scroll_region_lower             Bottom of scroll region in pane
    scroll_region_upper             Top of scroll region in pane
    session_alerts                  List of window indexes with alerts
    session_group                   Name of session group
    session_group_list              List of sessions in group
    session_group_size              Size of session group
    session_stack                   Window indexes in most recent order

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

