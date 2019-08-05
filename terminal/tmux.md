# ?

How do you include a double quote inside `#()` to insert the output of a shell command in the status line?

    ✘
    $ tmux set -g status-right "#(echo a\"b)"
    ''~

    ✘
    $ tmux set -g status-right '#(echo a"b)'
    ''~

    ✔
    $ tmux set -g status-right '#(echo a\"b)'
    a"b~

How to include in the status line the output of a shell command which contains a mix of single and double quotes (without using a shell script)?
For example: $ awk 'BEGIN { printf("%d", 123) }'
I've tried: `$ tmux set -g status-right "#(awk 'BEGIN { printf(\"%d\", 123) }')"`.
But it inserts '05' instead of '123'.

# How to view the description of
## the outer terminal?

    $ infocmp -x $(tmux display -p '#{client_termname}')

## the terminals of all tmux clients connected to the tmux server, taking into account 'terminal-overrides'?

    $ tmux info

##
# When does tmux discard a sequence which I try to send to the outer terminal?

When it's absent from the terminfo entry of the latter.

For example, AFAIK, there's no capability to describe how to change the color of
the cursor (`OSC 12 ; color ST`).
So, inside tmux, you can't directly send this sequence to the outer terminal.

OTOH, you can  send a sequence to  underline some text, or to  change its color,
because usually the terminfo entry of  the outer terminal contains a description
of these capabilities (`smul`, `setf`).

## How to prevent this?

You need to “escape” the sequence using this syntax:

    \ePtmux;seq\e\\
            ├─┘
            └ sequence we want to send to the outer terminal;
              any escape character it contains must be doubled

Source:
<https://web.archive.org/web/20150808225911/http://comments.gmane.org:80/gmane.comp.terminal-emulators.tmux.user/1322>

Relevant excerpt:

>    Support passing through  escape sequences to the  underlying terminal by
>    using DCS with a "tmux;" prefix. Escape characters in the sequences must
>    be doubled. For example:
>
>        $ printf '\ePtmux;\e\e]12;red\e\e\\\e\\'
>
>    Will  pass \ePtmux;\e\e]12;red\e\e\\\e\\  to the  terminal
>    (and change the cursor colour in xterm).

##
# How to customize the terminfo description of the outer terminal?

    $ tmux set -as terminal-overrides '{pat}:{val}'

You  can customize  the  terminfo  description of  the  outer  terminal via  the
`terminal-overrides` option.

`pat` must  match the  terminal type (see  `man fnmatch` for  the syntax  of the
pattern). `val` must be the sequence to send to change the shape of the cursor.

---

You can't use extended patterns (ex: '@(pattern-list)').

It would  require that you  set the `FNM_EXTMATCH`  flag which is  not possible,
because you  can't control how `fnmatch()`  is invoked.  Besides this  flag is a
GNU extension, it's probably not available on all systems.

# What are the necessary and sufficient conditions for tmux to relay a sequence to the outer terminal?

The sequence needs to be in `$ tmux info`.

##
# How does tmux choose the capabilities listed in `$ tmux info`?

Tmux uses  a predefined  list.

You can  read it in  `~/GitRepos/tmux/tty-term.c` (search for  `TTYC_BEL`); make
sure you're on master.

##
# I've started tmux like this:

    $ tmux -Lx -f =(cat <<'EOF'
    set -s terminal-overrides '*:smxx@,*:smzz=\E[9m'
    #                            ├───┘   ├──┘
    #                            │       └ set a non-existing 'smzz' capability
    #                            │         with the sequence previously stored in 'smxx'
    #                            └ disable 'smxx'
    EOF
    )

## Will the terminal strike through the text when I run `$ printf '\e[9m  strikethrough  \e[0m\n'`?

No.

### Why?

'smzz' is  not in the output  of `$ tmux info`,  because it's not the  name of a
capability which tmux recognizes.

---

Does the sequence need to be in the description of tmux-256color? `$ tmux info`? xterm-256color?
Does it matter whether we tweak tmux-256color or xterm-256color after starting tmux?

    $ tic -sx <(infocmp -1x xterm-256color | sed '/smxx/d')
    $ tic -sx <(infocmp -1x tmux-256color | sed '/smxx/d')

##
# ?

Can I add ad-hoc capabilities to the outer terminal using 'terminal-overrides'?

No.

You can only override *existing* capabilities.
The latter can be  found by looking for the pattern  `\[missing\]` in the output
of `tmux info`.

You can check this like so:

    $ tmux -Lx -f =(cat <<'EOF'
    set -s terminal-overrides '*:smxx@,*:smzz=\E[9m'
    #                            ├───┘   ├──┘
    #                            │       └ 'smzz' isn't recognized as a valid capability name by tmux
    #                            └ disable 'smxx'
    EOF
    )

    $ tmux info | grep smzz
    ''~

    $ printf '\e[9m  strikethrough  \e[0m\n'
    ✘ xterm doesn't strike through the text, even though '\e[9m' is the right sequence~

Inside tmux,  if you  try to  send a sequence  to the  outer terminal,  which is
absent from its customized terminfo description, tmux won't relay it.

---

Understand this answer.

Also, document that when you disable a capability with the `@` suffix, the value
of the capability is `[missing]` inside the output of `$ tmux info`.

What  happens if  we  disable  'smxx' and  assign  `\e[9m`  to another  existing
sequence?
We still can't strike through text, so it seems tmux doesn't relay the sequence.
Why?
I think that's because the sequence needs to be in `$ tmux info`.
And `$ tmux info`  only seems to include only a  pre-defined set of capabilities
(smzz is not one of them):

    ~/GitRepos/tmux/tty-term.c
    /TTYC_BEL

---

If you tweak a capability with `$ tmux set terminal-overrides ...`,
don't forget to detach and re-attach.
And note  that if you  have multiple tmux clients  using the same  terminal, you
need to detach them *all* before re-attaching any of them.

You also need to detach/re-attach if  you've edited the description of the outer
terminal with `$ tic`.
This seems to  suggest that tmux doesn't care about  the terminfo description of
the outer terminal; it only uses its own internal description.
But the latter is based on the terminfo description, and is updated whenever you
detach/re-attach.

##
## ?

    OSC 2 ; Pt ST

Change Window Title to Pt.

See `OSC Ps ; Pt ST /Ps = 2`.

---

In tmux, this sequence also affects the title of the current pane:

    $ printf '\e]2;my new title\a'
    $ tmux display -p '#{pane_title}'

## ?

    Esc k Pt ST

Specific to tmux. Sets the name of the current window.

Example:

    $ tmux set -w allow-rename on
    $ printf '\ekmy new window name\a'

##
# Terminfo Extensions
## What's a terminfo extension?

An extended capability not found in  standard terminfo, which was probably first
supported in xterm, and later may have been implemented in other terminals.

## How can I list all terminfo extensions supported by tmux?

    $ infocmp -x xterm+tmux
    #       Reconstructed via infocmp from file: /home/user/.terminfo/x/xterm+tmux~
    xterm+tmux|advanced xterm features used in tmux,~
            Cr=\E]112\007, Cs=\E]12;%p1%s\007,~
            Ms=\E]52;%p1%s;%p2%s\007, Se=\E[2 q, Ss=\E[%p1%d q,~

Here, you can see 5 capabilities:

   - Cr
   - Cs
   - Ms
   - Se
   - Ss

##
## What's `Ms`?

It's a way for the terminal to  tell the applications how they should encode and
send  some arbitrary  text, if  they  want the  terminal  to store  it into  the
clipboard.

### Where can I find more information about it?

    OSC Ps ; Pt BEL /Ps = 5 2

        Where is OSC 52 documented?

See also:

    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ vim terminfo.src
    /\m\C\<Ms\>

### What's its default value?

    Ms=\E]52;%p1%s;%p2%s\007

#### What's the meaning of the two parameters?

   - p1 = the storage unit (clipboard, selection or cut buffer)
   - p2 = the base64-encoded clipboard content.

##
# Issues
## I've configured Vim to change the shape of the cursor when I enter insert mode, using a DCS sequence.

    :let &t_SI = "\ePtmux;\e\e[6 q\e\\"
    :let &t_EI = "\ePtmux;\e\e[2 q\e\\"
                  ├─┘
                  └ DCS

### It doesn't work as expected!

The cursor shape is often reset to a block while I'm in insert mode.
And in urxvt,  when I focus another  tmux pane without leaving  insert mode, the
cursor shape is not set back to a block.

Solution: Do *not* use a DCS sequence.

    $ cat <<'EOF' >>~/.vim/vimrc
    let &t_SI = "\e[6 q"
    let &t_EI = "\e[2 q"
    EOF

And set the `Ss` and `Se` capabilities of the outer terminal.

    $ cat <<'EOF' >>~/.tmux.conf
    set -as terminal-overrides ',*:Ss=\E[%p1%d q:Se=\E[2 q'
    EOF

##
# ?

Document what's the purpose of 'terminal-overrides'.

I think it can have 2 purposes.

It can be used to override the value of a capability.
For example, the value of the  civis capability of the tmux-256color terminal is
`\E[?25l`:

    $ infocmp -1x tmux-256color | grep civis
            civis=\E[?25l,~

Same thing for xterm-256color:

    $ infocmp -1x xterm-256color | grep civis
            civis=\E[?25l,~

Now, suppose that the outer terminal  is xterm-256color, and for some reason you
need to send `\E[?123l` instead of `\E[?25l`.
'terminal-overrides' can help you do that:

    set -as terminal-overrides 'xterm-256color:civis=\E[?123l'

When  tmux will  receive  `\E[?25l`,  it will  recognize  the civis  capability,
and  will   send  to  xterm  whatever   new  value  is  assigned   to  civis  by
'terminal-overrides', ignoring the value in the description of xterm-256color.

'terminal-overrides' can also be used to prevent tmux from discarding some given
sequence.
For example,  the description  of st-256color doesn't  currently include  a `Cs`
capability,  nor  a  `Cr`  one,  so  tmux  would  discard  a  sequence  such  as
`\e]12;123\007`; unless you set `Cs` via 'terminal-overrides'.

# ?

    $ tic -sx -e tmux-256color <(infocmp -x tmux-256color | sed 's/civis=\\E\[?25l/civis=\\E\[?123l/')
    $ tmux set -s terminal-overrides '*:civis=\E[?456l'
    $ tic -sx -e xterm-256color <(infocmp -x xterm-256color | sed 's/civis=\\E\[?25l/civis=\\E\[?789l/')

Default:

    25 → 25

Modify tmux-256color:

    123 → 25

Override civis:

    25 → 456

Modify xterm-256color:

    25 → 789

Override + xterm-256color:

    25 → 456

tmux-256color + xterm-256color:

    123 → 789

tmux-256color + override:

    123 → 456

tmux-256color + override + xterm-256color:

    123 → 456

