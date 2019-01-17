# k
## keycode

Number identifying a physical key.

When you press a key, the keyboard sends a scancode to the kernel.
The latter translates the scancode into a keycode.

You can  see which keycode is  produced by any key  via the utility:

        • xev for X11
        • showkey for the console

## keysym

String identifying a symbol.

Examples:

        ┌───────────────────────┬───────────────────────────┐
        │        Symbol         │          Keysym           │
        ├───────────────────────┼───────────────────────────┤
        │ A                     │ A                         │
        ├───────────────────────┼───────────────────────────┤
        │ F1                    │ F1                        │
        ├───────────────────────┼───────────────────────────┤
        │ Control_L             │ Control_L                 │
        ├───────────────────────┼───────────────────────────┤
        │ à                     │ aacute                    │
        ├───────────────────────┼───────────────────────────┤
        │ `                     │ grave                     │
        ├───────────────────────┼───────────────────────────┤
        │ è                     │ egrave                    │
        ├───────────────────────┼───────────────────────────┤
        │ ~                     │ asciitilde                │
        ├───────────────────────┼───────────────────────────┤
        │ |                     │ bar                       │
        ├───────────────────────┼───────────────────────────┤
        │ []                    │ bracketleft, bracketright │
        ├───────────────────────┼───────────────────────────┤
        │ {}                    │ braceleft, braceright     │
        ├───────────────────────┼───────────────────────────┤
        │ grave accent (ì)      │ dead_grave                │
        └───────────────────────┴───────────────────────────┘

## keymap table

Table maintained by the X server, which translates the keycodes into keysyms.

##
# m
## (logical) modifiers

    • shift
    • lock
    • control
    • mod1..5

## modifier map

Another table (in addition to the keymap table) maintained by `xmodmap`.

It binds up to four couples (keysym, keycode) per logical modifier.

Different physical  keys can be  used to produce the  same keysym, and  the same
logical modifier.

Example 1:

        ┌ logical modifier
        │           ┌ keysym
        │           │          ┌ keycode
        │           │          │
        shift       Shift_L (0x32),  Shift_R (0x3e)


Example 2:

        control     Control_R (0x24),  Control_L (0x25),  Control_L (0x42),  Control_R (0x69)
                    │                  │                  │                  │
                    │                  │                  │                  └ fourth couple
                    │                  │                  └ third couple
                    │                  └ second couple
                    └ first couple

##
# x
## xcape

Utility which allows a modifier key to be used as another key when it is pressed
and released on its own.

The default behaviour is to generate the Escape key in place of Control_L.

## xkb, xmodmap

Utilities which allow you to modify the keymap table.

`xmodmap` is, historically, the traditional utility.

`xkb` is more powerful, and supports more modifiers.

