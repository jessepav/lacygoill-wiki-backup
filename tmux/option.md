# Getting info
## When asking for the value of an option, must I specify its scope?

Yes.

    $ tmux show mouse
    ''~

    $ tmux show -g mouse
    mouse on~

### Its type?

You can, but you don't need to.

Tmux can infer the type of an option from its name, except if it's a user option.

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

    $ tmux set clock-mode-colour green
    $ tmux clock-mode
    # the clock is in green

                v
    $ tmux set -u clock-mode-colour
    $ tmux clock-mode
    # the clock is in blue (default global value)

## How to reset an option to its default value?

Unset its global value.

    $ tmux set -g clock-mode-colour red
    $ tmux clock-mode
    # the clock is in red

                vv
    $ tmux set -gu clock-mode-colour
    $ tmux clock-mode
    # the clock is in blue

##
## How to set an option on the condition it hasn't been set yet?

Use the `-o` flag:

    $ tmux set @foo bar

    $ tmux show @foo
    @foo bar~

    $ tmux set -o @foo qux
    already set: @foo~

### How to make it quietly?

Use the `-q` flag:

    $ tmux set -qo @foo qux
    already set: @foo~

##
## I have 2 windows, and I'm in the first one.  How to set the color of the clock in the second window?

Use the `-t` argument:

    $ tmux set -t2 clock-mode-colour green
                ^^

## I have 2 sessions, and I'm in the first one.  How to get the value of an option local to the second one?

Again, use the `-t` argument:

    $ tmux show -t2 <option>

##
## What happens if I
### omit `-g` when I set a session or window option in `~/.tmux.conf`?

Tmux will complain with one of these error messages:

    no current session
    no current window

### don't provide a value to `$ tmux set <boolean option>`?

The option is toggled between on and off.

    $ tmux set -g mouse && tmux show -g mouse
    mouse off~

    $ tmux set -g mouse && tmux show -g mouse
    mouse on~

##
# User options
## Is a user option a window option, a session one, or a server one?

It can be any of them.

    $ tmux set -w @foo bar
    $ tmux show -w @foo
    @foo bar~

    $ tmux set @foo bar
    $ tmux show @foo
    @foo bar~

    $ tmux set -s @foo bar
    $ tmux show -s @foo
    @foo bar~

The concept is orthogonal to the type of the option.

### Which precaution must I take when setting a user option, or asking for its value?

You must specify its type; either with no flag (server), `-w` (window), or `-s` (session).

#### Why?

There's no way for tmux to infer the  type of a user option from its name, since
the latter can be arbitrarily chosen.

##
# Array options
## What is an array option?

An option whose final value is an array of items.

##
## Currently, there are 6 of them.  What are their names?

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

    $ tmux show user-keys
    user-keys~

    $ tmux set -a user-keys "\e[123"
    $ tmux show user-keys
    user-keys[0] \\e[123~

    $ tmux set user-keys ''

---

Or with an `[123]` index:

    $ tmux show user-keys
    user-keys~

               necessary for zsh, where `[` and `]` have a special meaning
               v            v
    $ tmux set 'user-keys[0]' "\e[123"
    $ tmux show user-keys
    user-keys[0] \\e[123~

    $ tmux set user-keys ''

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
## How to reset the *whole* value of an array option?

Don't use `-a` nor `[123]`.

    $ tmux set user-keys "\e[123"
    $ tmux show user-keys
    user-keys[0] "\\e[123"~

##
## Comma
### When do I need a comma to set the value of an array option?

When you want to set several items of the array in a single command.
In this case, the comma tells tmux when a item ends, and when the next one starts.

    $ tmux set user-keys 'foo,bar'
    $ tmux show user-keys
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

I think that before 2.3, 'terminal-overrides' was a string option.

> * terminal-overrides and update-environment are now array options (the previous
<https://github.com/tmux/tmux/blob/8382ae65b7445a70e8a24b541cf104eedadd7265/CHANGES#L575>

And maybe a comma was needed for a string option.

But anyway, now, 'terminal-overrides' is an array option.
So, a comma should be useless most of the time.

---

If you want to be sure, try this experiment.

    set -s  terminal-overrides 'xterm*:Tc'
    set -as terminal-overrides 'st*:Cs=\E]12;%p1%s\007'

If tmux didn't split after  the value of 'terminal-overrides' after `xterm*:Tc`,
then it would consider `xterm*` as being  the terminal type pattern for the `Cs`
capability, which would  prevent us from resetting the color  of the cursor with
`$ printf '\033]12;3\007'` in st (since 'st-256color' doesn't match 'xterm*').
And yet,  in practice, we can  reset the color of  the cursor in st  + tmux with
this minimal `tmux.conf`.

###
### For 'terminal-overrides', do I need a comma to separate two capabilities for the same terminal type pattern?

No.

    $ tmux -Ltest -f/dev/null new
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

    $ tmux show-hooks -t <session>

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

    set-hook -t <session> -R <hook>
             ^^^^^^^^^^^^

Example:

    $ tmux set-hook -t fun    session-renamed '' \; \
           set-hook -t fun -a session-renamed 'display -p one' \; \
           set-hook -t fun -a session-renamed 'display -p two' \; \
           set-hook -t fun -R session-renamed
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

Use `-t`:

    set-hook -t fun -u '<hook>[123]'

    $ tmux set-hook -t fun     session-renamed '' \; \
           set-hook -t fun -a  session-renamed 'display -p test' \; \
           set-hook -t fun -a  session-renamed 'display -p remove_me' \; \
           set-hook -t fun -u 'session-renamed[1]' \; \
           set-hook -t fun -R  session-renamed
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

###
# Issues
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

     $ tmux -Ltest -f =(cat<<'EOF'
     set -as terminal-overrides ',*-256color:Tc'
     set -gw window-style         'bg=#000000'
     set -gw window-active-style  'bg=#ffffff'
     EOF
     )

     C-b " (splitw)
     C-b ; (last-pane)

##
# Reference

