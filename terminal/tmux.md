# How to view the description of the outer terminal used by tmux?

    $ tmux info
    $ tmux -L{socket_name} info

The first command will display the  terminfo descriptions of the outer terminals
of all the tmux clients connected to the default server.

The second command will do the same,  but for the clients attached to the server
whose socket name is given as an argument to `-L`.

When a program sends a sequence to  tmux, the latter probably tries to translate
it into the  right sequence for the outer terminal,  via an internal description
of the latter.

This description can be viewed with `$ tmux info` and modified with
`terminal-overrides`.

# Does tmux interfere when you try to send a sequence to the outer terminal?

It depends.

Tmux may  consume the sequence  if it's absent from  the terminfo entry  for the
outer terminal.

For example, AFAIK, there's no capability to describe how to change the color of
the cursor ('OSC 12 ; color ST').
So, inside tmux, you can't directly send this sequence to the outer terminal.

OTOH, you can  send a sequence to  underline some text, or to  change its color,
because usually the terminfo entry for the outer terminal contains a description
of these capabilities (smul, setf).

# How to send a sequence to the outer terminal if it's not in its terminfo description?

You need to “escape” it using this syntax:

    \ePtmux;seq\e\\
            └─┤
              └ sequence we want to send to the terminal;
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


When possible,  it's better to correctly  set the right capability  of the outer
terminal.

Ex:

    :let &t_SI = "\e[6 q"
    :let &t_EI = "\e[2 q"
    $ tmux set -as terminal-overrides ',*:Ss=\E[%p1%d q:Se=\E[2 q'

This way, whenever we enter insert mode, the shape of the cursor becomes a line,
but it's LOCAL to the current pane.
IOW,  without leaving  insert mode,  if  we focus  another pane,  the cursor  is
restored to a block.

This is  due to tmux automatically  sending `Se`, whenever we  focus a different
pane.
And it sends `Ss`  whenever we focus the pane where  we've initially changed the
shape of the cursor.

OTOH, if  we didn't set  the `Ss`, `Se`  capabilities, and manually  escaped the
sequence to send it to the terminal, the change of the shape of the cursor would
be GLOBAL to all panes.

# How to customize the terminfo description of the outer terminal?

    $ tmux set -as terminal-overrides '{pat}:{val}'

You  can customize  the  terminfo  description of  the  outer  terminal via  the
`terminal-overrides` option.

`pat` must  match the  terminal type (see  `man fnmatch` for  the syntax  of the
pattern). `val` must be the sequence to send to change the shape of the cursor.


You can't use extended patterns (ex: '@(pattern-list)').

It would  require that you  set the `FNM_EXTMATCH`  flag which is  not possible,
because you  can't control how `fnmatch()`  is invoked.  Besides this  flag is a
GNU extension, it's probably not available on all systems.

# How to debug a sequence which works outside tmux but not inside?

Try to find and set a capability in the description of the outer terminal.

In particular, in `$ tmux info`, check:

   - bold
   - sitm     italic
   - smul     underline
   - smxx     strikethrough
   - setaf    change definition of ANSI color

... and see whether they are set or followed by `[missing]`.
If one of them is followed by  `[missing]`, the sequence will probably not work,
and the capability in the `tmux-256color` entry needs to be set.

# What's 'terminal-overrides' good for?

It's useful to change the color of  the cursor, or its shape, via the unofficial
terminfo extensions `Cs` / `Cr` (color)  and `Ss` / `Se` (shape), without having
to escape the sequence (via `\ePtmux;...`).

For more info, see `$ man tmux /TERMINFO EXTENSIONS`.

# Can you add ad-hoc capabilities to the outer terminal using 'terminal-overrides'?

No.

You can only override EXISTING capabilities.
The latters can be found by looking  for the pattern `\[missing\]` in the output
of `tmux info`.

You can check this like so:

                                               ┌ `smzz` isn't recognized as a valid
                                               │ capability name by tmux
                                               ├──┐
    $ tmux set -as terminal-overrides ',xterm*:smzz=\E[9m'

    $ tmux info
    no `smzz` capability~

    $ printf '\e[9m   strikethrough  \e[0m\n'
    ✘ the  shell doesn't strike through the text,  even though '\e[9m'~
      may be (in some terminals) the right sequence to strike through text~


Inside tmux,  if you  try to  send a sequence  to the  outer terminal,  which is
absent from its customized terminfo description, tmux won't relay it.

