# Glossary
## binding

Specifiy the behaviour of a particular key.

##
## layer

Collection of bindings.

### default layer

Layer named `[main]`; it should contain definitions of common bindings.

By default, in this layer, each key is bound to itself.

Exception: the  modifier keys  are bound  to eponymously  named layers  with the
corresponding modifiers.

For example,  the `meta`  key is  bound to the  `layer(meta)` action,  where the
layer named `meta` is internally defined as `[meta:M]`.

##
# How does `keyd(1)` handle multiple layers activated at the same time?

They form a stack of "occluding" keymaps consulted in activation order.

That is, when  a layer is activated, it  does not erase all the  bindings of the
previous one;  but if both layers  have different definitions for  the same key,
the last  one wins.  Another  way of putting  it: a binding for  a key in  a top
layer occludes a binding for the same key in a bottom layer.

---

Example:

     - -   3rd layer activated; 3rd consulted
    -- --  2nd layer activated; 2nd consulted
    - - -  1st layer activated; 1st consulted

In this example, there are 3 layers on the stack.
Each hyphen represents a binding for a key.
All the bindings in a given column apply to the same key.
The binding for the k-th key will be taken from the l-th layer, where `(k, l)` is:

    (1, 2)
    (2, 3)
    (3, 1)
    (4, 3)
    (5, 2)

##
# Pitfalls
## I've messed up the config.  Now the machine is unusable!

Press this panic sequence:

    <backspace>+<escape>+<enter>

It will force `keyd(1)` to terminate.

##
# Todo
## document
### the benefits of `keyd(1)` over our old suite of tools

<https://github.com/rvaiya/keyd>

The old suite was too complex:

   - to change layout: `xmodmap(1)` or  `xkbcomp(1)`, and `loadkeys(1)` (for the virtual console)
   - overload Capslock with Escape+Ctrl: `xcape(1)` or `caps2esc` (interception plugin)
   - overload right Enter with Enter+Control: `enter2ctrl` (our interception plugin)

`keyd(1)` can replace all of them:

   - replace `xmodmap(1)`/`xkbcomp(1)`
   - replace `loadkeys(1)`
   - replace `xcape(1)`/`caps2esc`
   - replace `enter2ctrl`
   - support X11 *and* Wayland

---

In  particular,  `keyd(1)`  is  an improvement  over  the  interception  plugins
(`caps2esc` and `enter2ctrl`).

With those, in Firefox, `Ctrl+mousewheel` does  not change the zoom level of the
current webpage.  It does with `keyd(1)`

Besides, our  `enter2ctrl` plugin needed  more work to make  it work as  well as
`caps2esc`.  It did not work in a virtual  console at all.  And even in the GUI,
it  did not  work properly.   When pressing  `C-a`, control  and `a`  had to  be
pressed in a  too specific manner: it was  not enough for `a` to  be pressed, it
*also* had to be released (and it had to be released while control was held).

---

Note that  `keyd(1)` cannot change the  keyboard repeat rate; that's  the job of
the display server.  You can use:

   - `xset(1)` on X11
   - `kbdrate(8)` in the virtual console
   - some GUI/tool provided by the desktop environment on Wayland

<https://github.com/rvaiya/keyd/issues/97#issuecomment-1012404919>

---

A benefit of `keyd(1)` over `xkbcomp(1)` is that it works even in a VM.
No need to transfer your custom keyboard layout from the guest to the host.
That's because `xkbcomp(1)` only works at the display server level.
Each  time  your keyboard  talk  to  a different  display  server,  you need  to
customize the latter; which is brittle and tiresome.

`keyd(1)` is a lower-level tool; you only need to configure it once.

### `--expression`

    -e, --expression <expression> [<expression>...]

      Modify bindings of the currently active keyboard.

### the formal definition of a layer heading/binding

Formally, a layer heading has the form:

        "[" <layer name>[:<modifier set>] "]"
        <modifier_set> =: <modifier1>[-<modifier2>]...
        <modifierN> =: C|M|A|S|G

        C = Control
        M = Meta/Super
        A = Alt
        S = Shift
        G = AltGr

And a layer heading is followed by a set of bindings which take the form:

    <key> = <keycode>|<macro>|<action>

---

Should we write a template, a cheat sheet, a markdown note, ...?

##
## What do these sentences from man page mean?

    Note: All keyboards defined within a given config file will share the
    same state. This is useful for linking separate input devices together
    (e.g foot pedals).

I *think* the state of the keyboard refers to the currently active layer.
Which means that  if you change the  layer of a keyboard which  is configured in
file A, you change the layer of all the other keyboards configured in A.

---

    These layers play nicely with other modifiers and preserve existing
    stacking semantics.

?

## Does `keyd(1)` load *all* `.conf` files under `/etc/keyd`?

    Configuration files are stored in /etc/keyd/ and are loaded upon ini‐
    tialization.
    [...]
    A valid config file has the extension .conf and must begin with an
    [ids] section that has one of the following forms:
    [...]

## In a layer heading what does `:<modifier>` mean?

I  *think* it's  used as  a fallback,  in case  the layer  does not  contain any
binding for the pressed key.

For example, if you  press the key `x`, while the  layer `[foo:C]` is activated,
then `keyd(1)` will send `control+x`.

Similarly, if  you press the  key `y`, while  the layer `[bar:A]`  is activated,
then `keyd(1)` will send `alt+y`.

Make sure our understanding is correct.
##
## find a way to make the system execute `~/.config/keyboard/setup` automatically whenever `keyd(1)` is (re)started

The latter should mainly contain this command:

    $ xset r rate 175 40

And possibly another `kbdrate(8)` command for the virtual console.

Anyway, make sure whatever commands it contains are run *after* `keyd(1)`.

Otherwise, your custom key repeat rate and delay will be lost.

BTW, I *think* this is an issue for all similar tools.
For example, `caps2esc` has the same issue:
<https://github.com/oblitum/caps2esc/issues/1>

---

Also, remove this line:

    "$HOME/.config/keyboard/setup" &

From this script:

    ~/bin/autostartrc
