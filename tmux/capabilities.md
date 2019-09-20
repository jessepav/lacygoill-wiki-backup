# How to view the description of
## the outer terminal?

    $ infocmp -x $(tmux display -p '#{client_termname}')

## the terminals of all tmux clients attached to the tmux server, taking into account 'terminal-overrides'?

    $ tmux info

##
# Sending a sequence to the outer terminal
## In the outpuf of `$ tmux info`, how does tmux choose the listed
### capabilities?

They are taken from a predefined list.

You can  read it in  `~/Vcs/tmux/tty-term.c` (search for `TTYC_BEL`);  make sure
you're on master to get the latest list.

### sequences?

They are taken from the terminfo description of the outer terminal.

---

    # start xterm

    $ tic -sx -e xterm-256color <(infocmp -x xterm-256color | sed 's/smxx=\\E\[9m/smxx=\\E\[123m/')
                                                                                            ^^^
    $ tmux -Lx -f/dev/null
    $ tmux info | grep smxx
    203: smxx: (string) \033[123m~
                             ^^^

##
## How to customize the output of `$ tmux info`?

    $ tmux set -as terminal-overrides 'pat:capability=seq'

`pat` must  match the  terminal type (see  `man fnmatch` for  the syntax  of the
pattern); `capability` must be the name of a terminal capability, and `seq` must
be the  sequence to send  to the  outer terminal when  this capability is  to be
used.

If the  capability you're  trying to  override is  a *boolean*  capability (like
`Tc`) – and not a string one – the command becomes:

    $ tmux set -as terminal-overrides 'pat:capability'

---

You can't use extended patterns (ex: '@(pattern-list)').

It would  require that you  set the `FNM_EXTMATCH`  flag which is  not possible,
because you  can't control how `fnmatch()`  is invoked.  Besides this  flag is a
GNU extension, it's probably not available on all systems.

## In the output of `$ tmux info`, what's the value of a capability which I've canceled (with the `@` suffix)?

    [missing]

Example:

    # cancel 'smxx'
    $ tmux -Lx -f/dev/null
    $ tmux set -as terminal-overrides '*:smxx@'
    $ tmux detach
    $ tmux -Lx attach
    $ tmux info | grep smxx
    [missing]~

    # restore 'smxx'
                                       replace with the index of '*:smxx@' in the array
                                       v
    $ tmux set -su 'terminal-overrides[6]'
    $ tmux detach
    $ tmux -Lx attach
    $ tmux info | grep smxx
    203: smxx: (string) \033[9m~

##
## When does tmux discard a CSI / OSC sequence which I try to send to the outer terminal?

Theory:

I think tmux discards a sequence only if one of these statements is true:

   - the sequence is not associated to any capability present in `$ tmux info`
   - the sequence is associated to a capability whose value in `$ tmux info` is `[missing]`

This is equivalent to either of these statements being true:

   - the sequence is not in the description of the outer terminal
   - the sequence is in the description of the outer terminal, but was canceled by 'terminal-overrides'

But if that's the case, when tmux  parses the sequence `\e[9m`, how does it know
where to look in `$ tmux info`? How does it know it should look at `smxx`?

Theory:

When the server starts, it memorizes that  `\e[9m` was assigned to `smxx` in the
outer terminal.

There's an easier  (but wrong) explanation: tmux doesn't  memorize anything, and
it doesn't know  where to look in `$  tmux info`, it just tries  to find `\e[9m`
*anywhere*.

This experiment shows that it's wrong though:

    $ tmux -Lx -f/dev/null
    $ tmux set -as terminal-overrides '*:smxx@:smul=\e[9m'
    $ tmux detach
    $ tmux -Lx attach
    $ tmux info | grep 'smxx\|smul'
    202: smul: (string) \\e[9m~
    203: smxx: [missing]~

    $ printf '\e[9m  strikethrough  \e[0m\n'

The terminal  doesn't strike through  the text,  even though `\e[9m`  is present
inside `$ tmux info`.

---

Tmux doesn't  relay a sequence which  is not associated to  any known capability
(and thus absent from the description of the outer terminal).

    $ tmux -Lx -f/dev/null
    $ printf '\e]4;0;red\a'

The text  in the  status line  should become  red, but  it doesn't,  because the
sequence is not associated to any capability inside `$ tmux info`.

---

Tmux doesn't relay a sequence which has been removed from the description of the
outer terminal.

    $ tic -sx <(infocmp -x | sed '/smxx=/d')
    $ printf '\e[9m  strikethrough  \e[0m\n'

The  terminal  strikes through  the  text,  even though  `smxx`  is  not in  the
description of the terminal; the latter  doesn't need to inspect the terminfo db
to know what it's capable of doing.

    $ tmux -Lx -f/dev/null
    $ printf '\e[9m  strikethrough  \e[0m\n'

The terminal does *not* strike through the  text, because the value of `smxx` is
`[missing]` in `$ tmux info`.

---

Tmux doesn't relay a sequence associated to a canceled capability.

    $ tmux set -as terminal-overrides '*:smxx@'
    $ tmux detach
    $ tmux -Lx attach
    $ tmux info | grep smxx
    203: smxx: [missing]~

    $ printf '\e[9m  strikethrough  \e[0m\n'

The terminal does *not* strike through the  text, because the value of `smxx` is
`[missing]` in `$ tmux info`.

---

The description of the inner terminal is irrelevant.

    $ tmux -Lx -f/dev/null
    $ infocmp | grep smxx
    ''~
    $ tmux info | grep smxx
    203: smxx: (string) \033[9m~

    $ printf '\e[9m  strikethrough  \e[0m\n'

In the  output of `printf`, the  terminal strikes through the  text, even though
`smxx` is not in the description of the inner terminal (`screen`).

### How to send such a sequence in those circumstances?

You need to “escape” it using this syntax:

    \ePtmux;seq\e\\
            ├─┘
            └ sequence you want to send to the outer terminal;
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

Note that you really need the DCS sequence to end with ST (`\e\\`) not BEL (`\a`).
OTOH, since you need to double all  the escape characters in the sequence you're
trying to send to the outer terminal,  prefer to end the latter with BEL instead
of ST, to improve the readability.

Compare:

    $ printf '\ePtmux;\e\e]4;0;red\a\e\\'

Vs:

    $ printf '\ePtmux;\e\e]4;0;red\e\e\\\e\\'

##
# Miscellaneous
## When does tmux inspect the description of the outer terminal?

Only  when a  client is  attached  to a  tmux  server, to  build/update its  own
internal description of the outer terminal as given by `$ tmux info`.

Afterward, you can alter the description of the outer terminal however you like,
it won't affect tmux.

## In practice, what are the two main usages of 'terminal-overrides'?

It's often used to set a capability which is missing from the description of the
outer terminal.

For example, the  description of `st-256color` doesn't currently  include a `Cs`
capability,  nor  a  `Cr`  one,  so  tmux  would  discard  a  sequence  such  as
`\e]12;123\007`.
Unless you  set `Cs` via  'terminal-overrides' (or use  a DCS sequence  with the
prefix `tmux;`):

    $ tmux set -as terminal-overrides '*:Cs=\E]12;%p1%s\007'

---

It's also sometimes used to cancel a capability and prevent tmux from relaying a
sequence which would cause an issue when received by the outer terminal.

    $ tmux set -as terminal-overrides '*:Ss@:Se@'
                                         ├─┘ ├─┘
                                         │   └ cancel Se: never relay '\e[2 q'
                                         └ cancel Ss: never relay '\e[<digit> q'

##
## What's a terminfo extension?

An unofficial extended capability not found in standard terminfo.

### How can I list all terminfo extensions supported by tmux?

    $ infocmp -1x xterm+tmux | sed '1,2d'
    Cr=\E]112\007,~
    Cs=\E]12;%p1%s\007,~
    Ms=\E]52;%p1%s;%p2%s\007,~
    Se=\E[2 q,~
    Ss=\E[%p1%d q,~

##
## Which sequence can I send to the terminal to set the title of
### the current tmux pane?

    OSC 2 ; Pt BEL

Example:

    $ printf '\e]2;my title\a'
    $ tmux display -p '#{pane_title}'

---

Usually, this sequence is used to set the title of the terminal window.

See `OSC Ps ; Pt BEL/;/Ps = 2`.

### the current window?

    Esc k Pt BEL

Example:

    $ tmux set -w allow-rename on
    $ printf '\ekmy window name\a'

---

This sequence is specific to tmux.

##
# Issues
## I've updated 'terminal-overrides' while the tmux server is running.  `$ tmux info` is not updated!

Detach and re-attach your tmux client.

If you have  multiple tmux clients using  the same terminal, you  need to detach
them *all*  before re-attaching  any of  them, because  tmux only  maintains one
description per type of terminal client currently attached to the server.

---

You also need to detach/re-attach if  you've edited the description of the outer
terminal with `tic(1)`.

---

You don't need to detach/re-attach every time you update a server option.
`'terminal-overrides'` is a special case.
It has one *single*  value – like any option – but it's  used to build *several*
descriptions: one per type of terminal client attached to the server.
Those descriptions are only updated when you detach/re-attach.
There's no equivalent of such a mechanism for the other server options.

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

    $ tmux set -as terminal-overrides ',*:Ss=\E[%p1%d q:Se=\E[2 q'
    $ tmux detach
    $ tmux [-Lsocket] attach

