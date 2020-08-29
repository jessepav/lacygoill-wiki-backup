# Getting info
## When asking for the value of an option, must I specify its scope?

Yes.

    $ tmux show mouse
    ''~

    $ tmux show -g mouse
    mouse on~

### Its type?

You can, but you don't need to.

tmux can infer the type of an option from its name, except if it's a user option.

##
## How to get the value of the 'clock-mode-colour' option, and *only* its value (i.e. not its name)?

Use the `-v` flag:

                  v
    $ tmux show -gv clock-mode-colour
    blue~

## What are the two differences between `show-options` and `show-options -v`?

`show` shows the value of an option and its name, while `show -v` only shows the value.

`show` shows  the value  of an  option as if  it was  stored in  a double-quoted
string, while `show -v` shows it as if it was stored in a single-quoted string.

    $ tmux set @foo '\z' \; show @foo
    @foo \\z~

    $ tmux set @foo '\z' \; show -v @foo
    \z~

##
# Setting an option
## What's the purpose of the global value of an option?

If the local value is not set, it will inherit the global value.

This also applies to hooks, since they are implemented as array options.

##
## How to make sure tmux uses the global value of an option?

Unset its local value.

    $ tmux set clock-mode-colour green \; clock-mode
    # the clock is in green

                v
    $ tmux set -u clock-mode-colour \; clock-mode
    # the clock is in blue (default global value)

## How to reset an option to its default value?

Unset its global value.

    $ tmux set -g clock-mode-colour red \; clock-mode
    # the clock is in red

                vv
    $ tmux set -gu clock-mode-colour \; clock-mode
    # the clock is in blue

A server option has no global value; in this case, just unset the value.

##
## How to set an option on the condition it hasn't been set yet?

Use the `-o` flag:

    $ tmux set @foo bar \; show @foo
    @foo bar~

    $ tmux set -o @foo qux
    already set: @foo~

### How to make it quietly?

Use the `-q` flag:

    $ tmux set -qo @foo qux
    ''~

##
## I have 2 windows, and I'm in the first one.  How to set the color of the clock in the second window?

Use the `-t` argument:

    $ tmux set -t:2 clock-mode-colour green
                ^-^

## I have 2 sessions, and I'm in the first one.  How to get the value of an option local to the second one?

Again, use the `-t` argument:

    $ tmux show -t2 <option>
                 ^^

##
## What happens if I
### omit `-g` when I set a session, window, or pane option in `~/.config/tmux/tmux.conf`?

tmux will complain with one of these error messages:

    no current session
    no current window
    no current pane

### don't provide a value to `$ tmux set <boolean option>`?

The option is toggled between on and off.

    $ tmux set -g mouse \; show -g mouse
    mouse off~

    $ tmux set -g mouse \; show -g mouse
    mouse on~

##
# Pane options
## For every pane option, is there a window counterpart?

Yes.

This is what lets you set a pane  option in a given pane differently compared to
all the other panes of the window:

    $ tmux set -w allow-rename off \; set -p allow-rename on
    $ tmux show -wv allow-rename \; show -pv allow-rename
    off~
    on~

## For every window option, is there a pane counterpart?

Not necessarily.
For example, `aggressive-resize` is a window  option, but there's no pane counterpart.

##
## What's the default value of an unset pane option?

It inherits its value from its window counterpart.

From `man tmux /OPTIONS`:

   > Pane options inherit from window options.
   > This means any pane option may be set  as a window option to apply the option to
   > all panes in the window without the option set, [...]

## When a window option has a pane counterpart, what benefit do you get?

You get more control over its value.
You can make it different from one pane to another inside the same window.

##
## How to set an option
### local to a pane?

Use `-p`:

    $ tmux set -p @foo bar
               ^^

### local to all panes in a window?

Use `-w`:

    $ tmux set -w @foo bar

### in all panes in all windows?

Use `-gw`:

    $ tmux set -gw @foo bar

##
## The value of a pane option is A in a given pane, but B in the window of that pane.  Who wins, A or B?

A.

The value local to the pane wins in the given pane.
In the other panes, A doesn't apply, so B is used.

## How to set the background color of
### the panes in the current window as green?

    $ tmux set -w window-style bg=green
               ^^

#### and at the same time, the pane of index 1 as red?

    $ tmux set -w     window-style bg=green
    $ tmux set -pt:.1 window-style bg=red
               ^----^

#
## How is `-g` interpreted in `$ tmux set -gp <pane option>`?

It's ignored.

Watch:

    $ tmux -Lx -f =(echo 'set -gp allow-rename on')
    no current pane~
    $ tmux show -gw allow-rename \; show -w allow-rename \; show -p allow-rename
    off~
    ''~
    ''~

The first command seems to show that `set -gp` was processed like `set -p`.
This is confirmed by  the second command which shows that  the `set -gp` command
had no effect, since 'allow-rename' has not the value 'on', no matter the scope.

Possible rationale:

`-g` is ambiguous in this context.
Should it be interpreted as “all panes  in the current window”, or as “all panes
in all windows”?

Besides, there are already less ambiguous alternatives for both possible meanings:

    ┌─────────────────────────────────┬─────┐
    │ all panes in the current window │ -w  │
    ├─────────────────────────────────┼─────┤
    │ all panes in all windows        │ -gw │
    └─────────────────────────────────┴─────┘

## What happens if I use `set-option` or `show-options` for a pane option, without using `-w` nor `-p`?

`$ tmux show` assumes `-w`.

    $ tmux set -p allow-rename on \; set -w allow-rename off \; \
      show -v allow-rename
    off~

    $ tmux set -p allow-rename on \; set -wu allow-rename \; \
      show allow-rename
    ''~

Same thing for `$ tmux set`.

    $ tmux set -p allow-rename on \; set -w allow-rename on \; \
      set allow-rename off \; \
      show -pv allow-rename \; show -wv allow-rename
      on~
      off~

###
# User options
## Is a user option a server option, a session option, a window option or a pane option?

It can be any of them.

    $ tmux set -p @foo bar \; show -p @foo
    @foo bar~

    $ tmux set -w @foo bar \; show -w @foo
    @foo bar~

    $ tmux set @foo bar \; show @foo
    @foo bar~

    $ tmux set -s @foo bar \; show -s @foo
    @foo bar~

The concept is orthogonal to the type of the option.

##
## Which precaution must I take when setting a user option, or asking for its value?

You must specify its type; either with no flag (session), or with a flag:

   - `-p` (pane)
   - `-w` (window)
   - `-s` (server)

### Why?

There's no way for tmux to infer the  type of a user option from its name, since
the latter can be arbitrarily chosen.

##
# Array options
## What is an array option?

An option whose final value is an array of items.

##
## Currently, there are 5 of them.  What are their names?

   - 'command-alias'
   - 'status-format'
   - 'terminal-overrides'
   - 'update-environment'
   - 'user-keys'

Hooks are also stored as array options.

### How can I find them quickly in the manpage?

Search for the pattern `[]`.

##
## How to add an item to an array option?  (2)

With the `-a` flag:

    $ tmux set -a user-keys "\e[123" \; show user-keys \; set -u user-keys
    user-keys[0] \\e[123~

---

Or with an `[123]` index:

               necessary for zsh, where `[` and `]` have a special meaning
               v            v
    $ tmux set 'user-keys[0]' "\e[123" \; show user-keys \; set -u user-keys
    user-keys[0] \\e[123~

### What's the benefit of the first method?

It can't overwrite an existing item.

When you use the second method, there *is* such a risk.
To avoid it, you need to know the size of the array.

    $ tmux set 'user-keys[<size>]' "\e[123"
                          ├────┘
                          └ if the size of the array is 3,
                            then the array contains the items of index 0, 1 and 2;
                            the item of index 3 is free

#### What's its drawback?

You have to make sure not to append the same value every time you resource tmux.conf.

To do so, write a guard surrounding the setting:

    if '[ "$TERM" != "#{default-terminal}" ]' { ... }

If there're several settings, group them (possibly  in a file), so that you only
have 1 guard to write.

##
## How to remove the item of index 123?

Simply pass the `-u` flag to `set-option`:

    $ tmux set -u 'option[123]'
                ^

You may need `-g` if you're working with a session or window option.
And you may need `-s`, `-w`, `-p` if you're working with a user option.

## How to reset the *whole* value of an array option?

Don't use `-a` nor `[123]`.

    $ tmux set user-keys "\e[123" \; show user-keys \; set -u user-keys
    user-keys[0] "\\e[123"~

##
## Comma
### When do I need a comma to set the value of an array option?

When you want to set several items of the array in a single command.
In this case, the comma tells tmux when an item ends, and when the next one starts.

    $ tmux set user-keys 'foo,bar' \; show user-keys \; set -u user-keys
    user-keys[0] foo~
    user-keys[1] bar~

#### But a comma is used in other contexts in `example_tmux.conf` and in the faq!

Example from `example_tmux.conf`:

<https://github.com/tmux/tmux/blob/e8f4ca6a52bdfb7d8e2b8c39b867f2e2528a7631/example_tmux.conf#L17>

    set-option -as terminal-overrides ",xterm*:Tc"
                                       ^

and from the faq:

<https://github.com/tmux/tmux/wiki/FAQ#how-do-i-use-rgb-colour>

    set -as terminal-overrides ",gnome*:RGB"
                                ^

<https://github.com/tmux/tmux/wiki/FAQ#why-are-tmux-pane-separators-dashed-rather-than-continuous-lines>

    set -as terminal-overrides ",*:U8=0"
                                ^
##### Why?

I think that before 2.3, `terminal-overrides` was a string option.

   > * terminal-overrides and update-environment are now array options
<https://github.com/tmux/tmux/blob/8382ae65b7445a70e8a24b541cf104eedadd7265/CHANGES#L575>

And maybe a comma was needed for a string option.

But anyway, now, `terminal-overrides` is an array option.
So, a comma should be useless most of the time.

---

If you want to be sure, try this experiment.

    set -s  terminal-overrides 'xterm*:Tc'
    set -as terminal-overrides 'st*:Cs=\E]12;%p1%s\007'

If tmux didn't  split the value of `terminal-overrides`  after `xterm*:Tc`, then
it  would consider  `xterm*` as  being the  terminal type  pattern for  the `Cs`
capability, which would  prevent us from resetting the color  of the cursor with
`$ printf '\033]12;3\007'` in st (since `st-256color` doesn't match `xterm*`).
And yet,  in practice, we can  reset the color of  the cursor in st  + tmux with
this minimal `tmux.conf`.

###
### For `terminal-overrides`, do I need a comma to separate two capabilities for the same terminal type pattern?

No.

    $ tmux -Lx -f/dev/null new
    $ tmux show terminal-overrides
    terminal-overrides[0] "xterm*:XT:Ms=\\E]52;%p1%s;%p2%s\\007:Cs=\\E]12;%p1%s\\007:Cr=\\E]112\\007:Ss=\\E[%p1%d q:Se=\\E[2 q"~
    terminal-overrides[1] "screen*:XT"~

Notice how the Ms, Cs, Cr, Ss, Se capabilities:

   - are on the same line
   - apply to the same terminal type pattern `xterm*`
   - are not separated by commas

##
## Hooks
### What is a hook?

The equivalent of an event in Vim.

When a hook is  triggered, tmux runs the commands stored in  an array, in order,
which can be set via an option with the same name as the hook.

###
### How to show the global list of hooks and the commands they run?

    $ tmux show-hooks -g

#### the list of hooks local to an arbitrary session?

    $ tmux show-hooks -t =<session>

#### Why should I avoid `show-options -[g]H`?

`-H` doesn't merely display hooks, it *includes* hooks to the output of `show-options`.
IOW, session and user options are *also* included.

##
### How to make a hook run
#### a command when it's triggered?

Use `set-hook`:

    set-hook -ga <hook> 'display -p test'
              ││
              │└ append to the array (otherwise, you would reset it)
              └ global hook

Example:

    $ tmux set-hook -ga window-renamed 'display -p test'

#### all its commands now?

Pass `-R` to `set-hook`:

                    vv
    $ tmux set-hook -R window-renamed
    test~

##### what if it's a hook local to another session?

Use `-t`:

    set-hook -t =<session> -R <hook>
             ^-----------^

Example:

    $ tmux set-hook -t =fun    session-renamed '' \; \
           set-hook -t =fun -a session-renamed 'display -p one' \; \
           set-hook -t =fun -a session-renamed 'display -p two' \; \
           set-hook -t =fun -R session-renamed
    one~
    two~

####
### How to remove
#### an arbitrary command bound to a hook?

Use `-u`:

    set-hook -gu '<hook>[123]'

Example:

    $ tmux set-hook -g   session-renamed '' \; \
           set-hook -ga  session-renamed 'display -p test' \; \
           set-hook -ga  session-renamed 'display -p remove_me' \; \
           set-hook -gu 'session-renamed[1]' \; \
           set-hook -R   session-renamed
    test~

#### a command bound to a hook local to another session?

Use `-u` and `-t`:

    set-hook -t =fun -u '<hook>[123]'

    $ tmux set-hook -t =fun     session-renamed '' \; \
           set-hook -t =fun -a  session-renamed 'display -p test' \; \
           set-hook -t =fun -a  session-renamed 'display -p remove_me' \; \
           set-hook -t =fun -u 'session-renamed[1]' \; \
           set-hook -t =fun -R  session-renamed
    test~

###
### Can I manually make a hook run *one* of its commands?

It seems you can't.

    $ tmux set-hook -g   session-renamed '' \; \
           set-hook -ga  session-renamed 'display -p one' \; \
           set-hook -ga  session-renamed 'display -p two' \; \
           set-hook -gR 'session-renamed[1]'
    ''~

###
### Can I run a command bound to
#### a session hook and ignore the matching global hook?

Well,  that's what  happens  by default,  no  matter whether  you  pass `-g`  to
`set-hook`, so yes.

#### a global hook and ignore the matching session hook?

No, probably because a hook is implemented as an array option.
So, a session hook has priority over a global hook.

    $ tmux set-hook -g  session-renamed '' \; \
           set-hook -ga session-renamed 'display -p global\ hook' \; \
           set-hook     session-renamed '' \; \
           set-hook -a  session-renamed 'display -p session\ hook' \; \
           set-hook -gR session-renamed
    session hook~

##
# activity, bell, silence
## What does it mean for tmux to detect in a window
### some activity?

A process has written new output on the terminal.

###
### the bell?

A process has written `\a` (`\007`) on  the terminal, which caused the latter to
ring its bell.

#### What's the most portable way to manually ring the bell?

    $ tput bel

###
### silence?

A process has not written any new output since the time given to the
`'monitor-silence'` option:

    $ tmux set -w monitor-silence 123
                                  ^-^

##
## When the bell rings in a window,
### how to get a notification in the status line?

    $ tmux set -gw monitor-bell on

You don't  need to  customize your  status line, because  by default,  tmux will
reverse the  background and foreground colors  of the window in  the status line
window list.

But if you want another effect, you need to use the `window_bell_flag`.

See here for an example with `window_activity_flag`:
<https://github.com/tmux/tmux/issues/74#issuecomment-129130023>

#### in addition, how to get an audible notification?

    $ tmux set -gw monitor-bell on
    $ tmux set -g  visual-bell  both
                                ^--^

You'll also need to configure your window manager/terminal/audio server/... appropriately.
<https://forum.xfce.org/viewtopic.php?id=12031>

##### how about a message instead of a sound?

    $ tmux set -gw monitor-bell on
    $ tmux set -g  visual-bell  on
                                ^^

##
## How to prevent any bell notification (sound, message, reverse colors in status line window list)?

    $ tmux set -gw monitor-bell off \; set -gw window-status-bell-style ''
                                │                                       │
                                │                                       └ disable status line indicator
                                └ disable sound and message

## On which condition does the value of 'bell-action' take effect?

`'monitor-bell'` must be on.

### What *is* its effect?

It controls in  which window(s) an audible sound will  be emitted (provided your
DE  is correctly  configured),  and/or  a message  will  be displayed  (provided
`'visual-bell'` is not off), when the bell rings.

Its value can be:

    ┌─────────┬────────────────────────────────────────────────────┐
    │ any     │ a sound/message is emitted/displayed in any window │
    ├─────────┼────────────────────────────────────────────────────┤
    │ none    │ no sound/message in any window                     │
    ├─────────┼────────────────────────────────────────────────────┤
    │ current │ a sound/message only in the current window         │
    ├─────────┼────────────────────────────────────────────────────┤
    │ other   │ a sound/message only in the other windows          │
    └─────────┴────────────────────────────────────────────────────┘

---

But it does  *not* control whether the  colors of the window in  the status line
window list will be reversed:

                                vv                       v--v                       v-v
    $ tmux set -gw monitor-bell on \; set -g bell-action none \; set -g visual-bell off \
        ; sleep 1 ; tput bel

After running the command, focus a different window: the colors of the window in
the status line  window list have been reversed,  despite `'bell-action'` having
the value 'none' and `'visual-bell'` being 'off'.

##
# Issues
## When I try to combine some color with the bold style, I get a different color!

Don't use a named color, and don't use `colour0`, `colour1`, ..., `colour7` either.

Or use st with this patch:

<https://st.suckless.org/patches/bold-is-not-bright/>

---

In a tmux command, when you refer to a color via its name or via `colour0`, ...,
`colour7`, tmux  encodes one  of the  first 8 colors  in the  256-color palette,
using your terminal `setaf` capability.
This gives `\e[30m`, ..., `\e[37m`.

If  you combine  your color  with the  bold style,  tmux sends  to the  terminal
`\e[30;1m`, ..., `\e[37;1m`.
When receiving such sequences, the terminal interprets `1` as bright, not bold:

    $ printf '\e[30;1m  hello  \e[0m\n'

For more info, see our notes about colors in the terminal wiki.

MWE:

    $ tmux -Lx -f =(cat <<'EOF'
    set -gw window-status-format '#[fg=black,bold]#W'
    EOF
    )

The title of a non-focused window should  be in black, but in practice it's in grey.

## Some options which set colors don't work!

Do you use hex color codes, and does your terminal support true colors?
If the answers are yes and no, then make sure the following line is not run when
tmux is started from your terminal:

    set -as terminal-overrides ',*-256color:Tc'

Setting `Tc` may prevent other settings to work, like these for example:

    set -gw window-style        'bg=#cacaca'
    set -gw window-active-style 'bg=#dbd6d1'

This issue is specific to terminals which don't support true colors.

Alternatively, you could use:

   - `colour123` instead of `#ab1234`
   - a terminal supporting true colors

---

MWE:

     $ tmux -Lx -f =(cat <<'EOF'
     set -as terminal-overrides ',*-256color:Tc'
     set -gw window-style         'bg=#000000'
     set -gw window-active-style  'bg=#ffffff'
     EOF
     )

     C-b " (splitw)
     C-b ; (last-pane)

## I'm setting 'status-right'.  The result is unexpected!

Does the value contain a percent character?

If so, you may need to double it:

    $ tmux set -g status-right "#(awk 'BEGIN { printf(\"%%d\", 123) }')"
                                                        ^^

Indeed,  the   values  of  'status-right'   and  'status-left'  are   passed  to
`strftime(3)`, for which the `%` character has a special meaning.
You  need to  double the  character  so that  it's sent  literally to  `awk(1)`;
otherwise, in  the previous example,  `%d` would be replaced  by the day  of the
month (01, 02, ..., 31).

---

Does the value contain a double quote?

If so, you may need to escape it more than what you thought.

    $ tmux set -g status-right "#(echo a\"b)"
    ''~

    $ tmux set -g status-right "#(echo a\\\"b)"
    a"b~

In the first command, when the shell receives `a"b`, the quote is interpreted as
the start of a string which is  never closed; hence why the status line contains
nothing.

Run this in sh:

    $ echo a"b
    >~

You get the secondary prompt string (`>`  by default), because sh expects you to
type more text and close the string with a second `"`.

