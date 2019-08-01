# Syntax
## What's a format?

A string using format variables such as `pane_current_command`.

Its purpose is to format the  output of the `choose-`, `list-`, `new-` commands,
as well as the `break-pane` and `split-window` commands:

   - `break-pane`
   - `choose-buffer`
   - `choose-client`
   - `choose-tree`
   - `list-buffers`
   - `list-clients`
   - `list-commands`
   - `list-panes`
   - `list-sessions`
   - `list-windows`
   - `new-session`
   - `new-window`
   - `split-window`

Note that a format variable is only expanded when surrounded by `#{` and `}`.

##
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

For `choose-buffer`, you would probably use format variables beginning with `buffer_`.

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

For `list-commands`, you would probably use format variables beginning with `command_`.

Example:

    $ tmux lscm -F '#{command_list_name} : #{command_list_alias}'

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
### two numbers?

Use either of the `-eq`, `-ne`, `-gt`, `-ge`, `-lt`, `-le` shell operators.

Example:

    $ tmux if '[ #{pane_height} -lt 12 ]' 'display -p "fewer than 12 lines"' 'display -p "more than 12 lines"'
                                ^^^

---

Do *not* use `#{>=:}` & similar.
They are for string comparisons only.

###
### the equality between two strings?

Use one of these syntaxes:

    #{==:str1,str2}

    #{!=:str1,str2}

Examples:

    $ tmux display -p '#{==:#{host},ubuntu}'
    1~

    $ tmux display -p '#{!=:#{client_termname},rxvt-unicode-256color}'
    1~

### the lexicographical order between two strings?

Use `>=`, `>`, `<=` or `<`:

    #{>=:str1,str2}
    #{>:str1,str2}
    #{<=:str1,str2}
    #{<:str1,str2}

Example:

    $ tmux display -p '#{<:a,b}'
    1~

###
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

### When does it *not* work?

When your text contains braces.

    $ tmux command-prompt -I "#{l:{a} {b}}"
    {a {b}}~
          ^
          ✘

Note that the issue is specific to braces, not formats; so this would work as expected:

    $ tmux command-prompt -I "#{l:#{a} #{b}}"
    #{a} #{b}~

---

Here's a less contrived example illustrating the issue:

    $ tmux command-prompt -I "#{l:if 'true' {display #{pane_id}} {display 'x'}}"
    :if 'true' {display #{pane_id} { display 'x' }}~
                                                  ^
                                                  ✘

#### What should I do when it doesn't work?

Double all the number signs:

    $ tmux command-prompt -I "if 'true' {display ##{pane_id}} {display 'x'}"
    :if 'true' {display #{pane_id}} { display 'x' }~

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
# Format variables
## Which variable should I use to test whether
### a window is
#### zoomed?

    #{window_zoomed_flag}

#### the first one?  last one?

    #{window_start_flag}
    #{window_end_flag}

#### the last-but-one to be active?

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
# Getting info
## Which command should I try to use first to get an info about
### a given session/window/pane?

`display-message`

#### On which condition can I use it?

You need a description of the given session/window/pane, as described in:

    $ man tmux /COMMANDS /^\s*target-session
    $ man tmux /COMMANDS /^\s*target-window
    $ man tmux /COMMANDS /^\s*target-pane

And pass it to `-t`.

---

Even though the synopsis of `display-message` refers to `target-pane`:

    display-message [-aIpv] [-c target-client] [-t target-pane] [message]
                                                   ^^^^^^^^^^^

... you can still use a description of a session or window if needed.

###
### any session(s)/window(s)/pane(s) satisfying an arbitrary condition?

`list-sessions`, `list-windows` or `list-panes`.

You'll also need to pass the `-F  format` argument, to format the output so that
it suits your needs, and `$ awk` or `$ sed` to extract the desired info.

### any client(s)/buffer(s)/command(s) satisfying an arbitrary condition?

`list-clients`, `list-buffers` or `list-commands` + `$ awk` or `$ sed`.

###
## Which pane ID is output by
### `$ tmux display -p -t =mysession '#D'`?

If `mysession` is being attached, the ID of the currently active pane.
Otherwise, the ID of  the last pane which was active  when `mysession` was being
attached.

### `$ tmux display -p -t '=mysession:^' '#D'`?

The ID of the last pane which was active in the first window of `mysession`, the
last time  the latter was being  attached and you  left the first window  to use
another one.

### `$ tmux display -p -t '=mysession' '#W`'

If `mysession` is being attached, the name of the currently used window.
Otherwise, the name of the last window which was used when `mysession` was being
attached.

##
### More generally, what happens if I pass a description to `-t` which is not accurate enough?

Tmux seems to  use the currently active pane/window if  it's compatible with the
description provided,  otherwise it uses  the last pane/window which  was active
among the set of panes/windows which are compatible with the description.

###
## How to get the command running in
### the current pane?

    $ tmux display -p '#{pane_current_command}'

### the pane whose id is `%123`?

    $ tmux display -pt%123 '#{pane_current_command}'

### the pane of index 1?

    $ tmux display -pt:.1 '#{pane_current_command}'
                      ^^
                      current session:current window

### the pane of index 1 in the window 2?

    $ tmux display -pt :2.1 '#{pane_current_command}'

### the pane of index 1 in the window 2 in the session 'my session'?

    $ tmux display -pt 'my session:2.1' '#{pane_current_command}'

###
### any pane whose title is 'my title'?

    $ delim=$(tr x '\001' <<<x) \
      && tmux lsp -aF "#{pane_title}${delim}#{pane_current_command}" \
       | awk -F"$delim" "/^my title$delim"'/{print $2}'

##

## How to get the list of all
### format variables and their values in the current pane?

    $ tmux display -a

###
### clients attached to the running tmux server?

    $ tmux lsc

### clients connected to the session 'my session'?

    $ tmux lsc -t '=my session'

###
### all windows on the server?

    $ tmux lsw -a
               ^^

### all windows in the current session?

    $ tmux lsw

### all windows in the session 'my session'?

    $ tmux lsw -t '=my session'

###
### all panes on the server?

    $ tmux lsp -a
               ^^

### all panes in the current session?

    $ tmux lsp -s
               ^^

### all panes in the current window?

    $ tmux lsp

### all panes in the window `@123`?

    $ tmux lsp -t @123
               ^^^^^^^

### all panes in the session 'my session'?

    $ tmux lsp -s -t '=my session'
               ^^^^^^^^^^^^^^^^^^^

##
### ?

Here are some (all?) of the info you could ask for:

    cmd (current, initial)
    cwd
    flags
    height
    id
    index
    name / title
    position (first/last line, first/last character)
    tty
    width

    a window is zoomed
    a window is the first/last one
    a window is the last-but-one to be used

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

I think  there are many  other kinds of  info you could  want to get  in various
contexts (current session/window/pane, given session/window/pane, ...).
Find the minimum amount of rules to know to handle all possibilities.
But first, study `$ man tmux /COMMANDS`; you probably need this to know what can
be passed to `-t`.

###
## Can I reliably target a given window via its name?  a pane via its title?

No.

You can have 2 windows with the same name, or 2 panes with the same title.

### a session via its name?

Yes.

You can't have 2 sessions with the same name.

    $ tmux display -p '#S'
    study~

    $ tmux new -s study
    Duplicate session: study~

###
# Issues
## I have a complex format whose expansion is not the one I expected!

To debug the expansion, pass the `-v` flag to `display-message`:

    $ tmux display -pv 'complex format'
                     ^

Example:

    $ tmux display -pv '#{||:#{m:*vim,#{pane_current_command}},#{==:#{pane_current_command},man}}'
                        ├───────────────────────────────────────────────────────────────────────┘
                        └ should be 1 iff the command running in the pane is (n)vim or man

## I can't use braces from the shell!

Prepend `if -F 1` to your braces:

    ✘
    $ tmux bind x '{ display test }'
    unknown command:  display test~

    ✔
    $ tmux bind x 'if -F 1 { display test }'
                   ^^^^^^^

---

Rationale:

The shell doesn't care that `{}` are equivalent to quotes for tmux.
From its point of view, they are just regular characters.
No  matter what  you do,  the  shell will  never  consider them  as quotes  when
invoking `execve()`:

    $ tmux bind x '{display test}'
    →
    execve('tmux', 'bind', 'x', '{display test}')
    →
    :bind x '{display test}'
            ^              ^

Here, the tmux command receives the  subcommand `bind`, as well as the arguments
`x` and  `{display test}`; but  since the last  argument contains a  space, tmux
quotes it.

This seems to be confirmed by the fact that if you remove the space, the command
succeeds:

    $ tmux bind x '{display}'
    →
    execve('tmux', 'bind', 'x', '{display}')
    →
    :bind x {display}
            ^       ^
            this time, tmux did *not* add additional quotes

Anyway, when tmux parses the key binding and finds that the rhs is `'{display test}'`,
it cancels the installation because it realizes that the command you're trying to bind
is `{display test}`. But this is not a valid tmux command; it's a string.
So tmux complains in the exact same way it would complain if you had run:

    $ tmux bind x '"display test"'
    unknown command: display test~

---

Note that it  seems you can use the  exact same syntax to install  a key binding
whether from the shell or from a tmux file:

    $ tmux bind x display test
    ⇔
    :bind x display test

    $ tmux bind x 'display test'
    ⇔
    :bind x 'display test'

    $ tmux bind x '"display test"'
    ⇔
    :bind x '"display test"'

---

Also, note that  in the case of a  key binding, instead of using `if  -F 1`, you
could also repeat the command and the lhs:

    $ tmux bind x 'bind x { display test }'
                   ^^^^^^

But `display test` would not be run until you press `x` twice.
Because the first time you press `x`, the key binding would redefine itself:

    x 'bind x { display test }'
    →
    x { display test }

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
Indeed, any character inside `#{}` is syntaxic, including a space:

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

# We spent a lot of time to write the “Quoting” in `~/wiki/tmux/tmux.md`.

What should we have done to write it quicker?

Hint: Our initial notes were all over the place.
Maybe  this  was the  sign  that  we didn't  really  know  which questions  were
bothering us.
Maybe we should have spent more time on the questions than on the answers; first
trying to find a good structure (main questions, subquestions, ...), then moving
as much of our notes in this structure.

---

Also, we've spent too much time refactoring the Vim mappings `||` and `|x`.
We tried to adapt the code to a few features we wanted.
But the code was too old.
We should have  started from stratch, and first explicitly  tell which inferface
we  wanted  (like   what  each  mapping  was  supposed  to   do,  and  in  which
circumstances; also which signature for the function(s)).
And from  time to time, check  the old code  to avoid documented pitfalls  or to
borrow some interesting lines.


---

We're  spending  too much  time  on  documenting how  to  get  the list  of  all
clients/windows/panes/... sharing a given property.
I think  you should not  try to immediately find  all possible commands  using a
format variable.

What is your goal?
You want to find the minimum amount of rules to get any info in any context.
Ok, find a sample of *some* commands to get *some* info in *some* contexts.
Then, from them, try to infer some rules.
Now, apply those rules to get any info.
Does it work? Great, you've finished.
It doesn't work? Ok, try to tweak the rules (edit/remove/add), and apply the new
rules to get any info in any context.
Repeat until you get a good enough set of rules.
Find your rules with an **iterative** process, progressively, organically, ...

