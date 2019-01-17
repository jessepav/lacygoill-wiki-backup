# What's the meaning of BEL, ESC, ST and SP?

    ┌─────┬───────────────────┬─────────────────────┐
    │ key │ meaning           │ notation(s)         │
    ├─────┼───────────────────┼─────────────────────┤
    │ BEL │ Bell              │ C-g  \a  \007  \x07 │    Never use `\a`:
    ├─────┼───────────────────┼─────────────────────┤    it works in the shell, but not in Vim.
    │ ESC │ Escape            │ C-[  \e  \033  \x1b │
    ├─────┼───────────────────┼─────────────────────┤
    │ ST  │ String Terminator │ Esc \               │
    ├─────┼───────────────────┼─────────────────────┤
    │ SP  │ a space           │                     │
    └─────┴───────────────────┴─────────────────────┘

##
# What are the most useful sequences?
## CSI ? 1004 hl

        ┌──────────────┬────────────────────────────────────┐
        │ CSI ? 1004 h │ send FocusIn/FocusOut events       │
        ├──────────────┼────────────────────────────────────┤
        │ CSI ? 1004 l │ don't send FocusIn/FocusOut events │
        └──────────────┴────────────────────────────────────┘

## CSI ? 1049 hl

        ┌──────────────┬────────────────────────────────────────────────────────────────┐
        │ CSI ? 1049 h │ save cursor and use alternate screen buffer, clearing it first │
        ├──────────────┼────────────────────────────────────────────────────────────────┤
        │ CSI ? 1049 l │ use normal screen buffer and restore cursor                    │
        └──────────────┴────────────────────────────────────────────────────────────────┘

Try this:

        $ ls
        $ printf '\e[?1049h'
        $ echo 'hello'
        $ printf '\e[?1049l'

## CSI Ps SP q

Set cursor style.

This whole escape sequence is called DECSCUSR.

It allows  to change the  shape of the cursor  dynamically at runtime,  by being
sent to the terminal, via `echo` or `printf`.


        Change the cursor shape to a:
        ┌─────────────────┬───────────┐
        │ printf '\e[2 q' │ block     │
        ├─────────────────┼───────────┤
        │ printf '\e[4 q' │ underline │
        ├─────────────────┼───────────┤
        │ printf '\e[6 q' │ bar       │
        └─────────────────┴───────────┘

        $ printf '\e[0 q'
        $ printf '\e[3 q'
        $ printf '\e[5 q'

Same but with blinking.

## CSI Pm m

### How is this sequence also called?

SGR, because it invokes the SGR control function:

        Select Graphic Rendition

        https://vt100.net/docs/vt510-rm/SGR.html

Its purpose is to set character attributes (bold, italic, underline, color, ...).

### How to use it to apply a style to some text?

        $ printf '\e[1m   bold             \e[0m\n'
        $ printf '\e[3m   italic           \e[0m\n'
        $ printf '\e[4m   underline        \e[0m\n'
        $ printf '\e[5m   blinking         \e[0m\n'
        $ printf '\e[7m   negative image   \e[0m\n'
        $ printf '\e[8m   invisible image  \e[0m\n'
        $ printf '\e[9m   strikethrough    \e[0m\n'

Apply a style to the text.

Negative image = reverse foreground and background colors.
Invisible image = hide text.

Since the  syntax of  the sequence  contains Pm (and  not Ps),  you can  write a
sequence applying multiple styles.
Example:

        $ printf '\e[1;4;5m bold + underline + blinking \e[0m\n'


                                     NOTE:

If you want to reset:

   • all attributes use '\e[0m'

   • just one attribute, not all of them, add 20 to its code.

     Example:

             printf '\e[3;4m italic + underlined \e[24m just italic\n'
                                                    └┤
                                                     └ 4+20
                                                       │
                                                       └ underlined

### How to use it to color some text?

There are 4 ways  to express `Pm`, depending on which interval  the index of the
desired color belongs to:

        ┌─────────────┬───────────────┐
        │ color index │ Pm            │
        ├─────────────┼───────────────┤
        │ 0-7         │ 30-37         │
        ├─────────────┼───────────────┤
        │ 8-15        │ 90-97         │
        ├─────────────┼───────────────┤
        │ 16-256      │ 38;5;123      │
        ├─────────────┼───────────────┤
        │ true color  │ 38;2;rr;gg;bb │
        └─────────────┴───────────────┘

Add 10 to the  (1st) number to target the background of the  text instead of its
foreground.


        $ printf '\e[30m  text in black    \e[0m\n'
        $ printf '\e[31m  text in red      \e[0m\n'
        $ printf '\e[32m  text in green    \e[0m\n'
        $ printf '\e[33m  text in yellow   \e[0m\n'
        $ printf '\e[34m  text in blue     \e[0m\n'
        $ printf '\e[35m  text in magenta  \e[0m\n'
        $ printf '\e[36m  text in cyan     \e[0m\n'
        $ printf '\e[37m  text in white    \e[0m\n'

These sequences don't  necessarily apply the colors mentioned  above; they apply
the ones set in the terminal color palette (color0, color1, ..., color7).


                                     NOTE:

You can apply the  colors to the background instead of the text  by adding 10 to
the code.
Example:

        $ printf '\e[41m  background in red  \e[0m\n'


                                     NOTE:

You can apply high  intensity colors (color8, ..., color15) by  adding 60 to the
code.
Example:

        $ printf '\e[91m   text       in bright red  \e[0m\n'
        $ printf '\e[101m  background in bright red  \e[0m\n'

In reality, it applies the colors 8 to 15 in the terminal color palette.
So, they will be brighter iff you defined brighter colors in the palette.


        $ printf '\e[38;5;123m foreground in 123th color of palette \e[0m\n'
        $ printf '\e[48;5;123m background in 123th color of palette \e[0m\n'

        $ printf '\e[38;2;123;234;45m foreground in true color \e[0m\n'
        $ printf '\e[48;2;123;234;45m background in true color \e[0m\n'

In the 1st syntax,  the color is expressed via a decimal  code (123) refering to
its index in the terminal palette.

In the  2nd syntax, the  color is expressed via  a rgb code:   (123,234,45) This
syntax allows to express the EXACT color we want.
Whether it  works and whether  the color is  reliably rendered, or  the terminal
just chooses the closest match in its palette, depends on the terminal.
More  specifically,  it  depends  on  whether/how it  supports  the  true  color
capability.

## OSC 2 ; Pt ST

Change Window Title to Pt.

In tmux, the title affects the pane.

Example:

        $ printf '\e]2; new_title for pane \e\\'

## OSC 4 ; c ; spec ST

Change Color Number *c* to the color specified by *spec*.

*spec* can be a name or RGB specification as per XParseColor.
The latter includes the syntax `#RRGGBB`.
`#RRGGBB` is an old and not encouraged syntax (see `man XParseColor`).

Any number of *c*/*spec* pairs may be given.

The color numbers correspond to the ANSI colors 0-7, their bright versions 8-15,
and if supported, the remainder of the 88-color or 256-color table.


        $ printf           '\e]4;0;red\e\\'
        $ printf '\ePtmux;\e\e]4;0;red\e\e\\\e\\'

Make the ANSI color 0 red, outside/inside tmux.
In zsh,  the color  0 applies only  to the non  syntax-highlighted text,  on the
command-line.

## OSC Ps ; Pt ST

P*s* can be (among many other values):

        10  = terminal foreground (affects the percent sign in the prompt of `zsh`)
        11  = terminal background
        12  = cursor foregound
        ...
        708 = terminal border background (urxvt only)
        ...

*Pt* is a color (name or hexcode).


        Colorize in yellow the:

        ┌─────────────────────┬─────────────────────────────┐
        │ terminal foreground │ printf '\e]10;yellow\e\\\n' │
        ├─────────────────────┼─────────────────────────────┤
        │ terminal background │ printf '\e]11;yellow\e\\\n' │
        ├─────────────────────┼─────────────────────────────┤
        │ cursor foreground   │ printf '\e]12;yellow\e\\\n' │
        └─────────────────────┴─────────────────────────────┘

## Esc k Pt ST

Specific to tmux. Sets the name of the current window.

Example:

        $ printf '\ek new_name for window \e\\'

##
# What's the difference between CSI and OSC sequences?

The CSI sequences finish with a printable character.
The OSC sequences finish with ST (BEL can also be used in xterm).

# How to test whether the terminal supports common sequences to set text attributes?

        $ msgcat --color=test

 Useful to test whether we can send sequences to:

   • change the color of the text / background
   • set some styles (bold, italic, underlined)

# How to test whether the terminal supports any sequence?

You must MANUALLY send it via `printf`, or `echo [-e]`.

`echo` is a shell builtin command.
`-e` enables the interpretation of some backslash-escaped characters.
`-e` is necessary in bash, so that `\e` is replaced with a real escape character.
`-e` is useless in zsh, because its builtin `echo` command already uses `-e` by default.

It's impossible to PROGRAMMATICALLY detect whether  a sequence is supported by a
given terminal.

Even querying the terminfo db is not reliable.
For example, by default, xfce4-terminal sets `$TERM` to `xterm`.
The `xterm`  entry in  the terminfo db  contains a `sitm`  field with  the value
`\E[3m`.  Which  means xfce4-terminal reports to  all programs it runs,  that it
supports italics. It's false. It doesn't.

Bottom line: terminals lie to the programs they're running about their identity.

# Why should you use raw sequences as little as possible?

A raw sequence may work on one terminal but not on another.
Use `$ tput` instead. It's more portable.

`tput` will query the terminfo db and return the right sequence (if any) for any
given terminal:

        # ✘
        $ printf 'some \e[1m bold \e[0m text\n'

        # ✔
        $ printf 'some %s bold \e[0m text\n' $(tput bold)

# How to (re)initialize the terminal and the serial line interface?

        $ tput
        $ tset

Useful when a program  has left either of those in an  unexpected state, and the
terminal is no longer usable.

# Links

/usr/share/doc/xterm/ctlseqs.txt.gz    (This file comes from the package `xterm`)

http://invisible-island.net/xterm/ctlseqs/
http://invisible-island.net/xterm/ctlseqs/ctlseqs.html
https://vt100.net/docs/vt510-rm/contents.html
https://en.wikipedia.org/wiki/C0_and_C1_control_codes

http://pod.tst.eu/http://cvs.schmorp.de/rxvt-unicode/doc/rxvt.7.pod#Definitions
http://pod.tst.eu/http://cvs.schmorp.de/rxvt-unicode/doc/rxvt.7.pod#XTerm_Operating_System_Commands

        List of control sequences supported by xterm and urxvt.

