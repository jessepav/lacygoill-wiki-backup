# k
## keycode

Number identifying a physical key.

When you press a key, the keyboard sends a scancode to the kernel.
The latter translates the scancode into a keycode.

You can see which keycode is produced by any key via the utility:

   - `xev(1)` for X11
   - `showkey(1)` for the virtual console

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

You can read it with:

    $ xmodmap -pke

Its contents depends on the chosen keyboard layout and variant.
It ignores configurations performed at a level lower than the X server (e.g. via
`keyd(1)`).

You can ignore the keysyms beyond the 4th one; they probably don't mean anything:
<https://unix.stackexchange.com/a/299267>

##
# l
## level of key

On a physical keycap of some keys, several characters are displayed.
For example, on the 3rd key of the  2nd row, suppose the keycap displays these 3
characters:

    2
    é ~

`é` can be accessed without any modifier; it's the first level of the key.
`2` can only be accessed with the `Shift` modifier; it's the 2nd level of the key.
`~` can only be accessed with the `AltGr` modifier; it's the 3rd level of the key.

---

BTW, I *think* that `ralt_switch` is  set automatically when you choose the `fr`
layout, and that it's  a useful option.  For example, it  would be unexpected to
not be able to generate `~` by  pressing `AltGr+é`, even though it's written on
the keycap.

##
# m
## (logical) modifiers

   - shift
   - lock
   - control
   - mod1..5

## modifier map

Another table (in addition to the keymap table) maintained by `xmodmap(1)`.

It binds up to four couples `keysym (keycode)` per logical modifier.

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
# t
## tap

"Tapping" a key means pressing a key, then releasing the same key.

In contrast, "holding" a key means maintaining a pressed without releasing it.

##
# x
## xcape

Utility which allows a modifier key to be used as another key when it is pressed
and released on its own.

The default behaviour is to generate the Escape key in place of `Control_L`.

## xkbcomp, xmodmap

Utilities which allow you to modify the keymap table.

`xmodmap(1)` is, historically, the traditional utility.

`xkbcomp(1)` is more powerful, and supports more modifiers.
