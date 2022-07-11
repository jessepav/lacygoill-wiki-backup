# alternative tools
## `qmk_keyboard`

- <https://docs.qmk.fm/>
- <https://github.com/qmk/qmk_firmware>

Tool to develop custom keyboard firmware.

---

Pro:

   - more reliable and powerful than all the other software,
     because it operates at the lowest possible level (other possible levels are
     the Linux kernel, and the display server)

Cons:

   - probably more difficult to use
   - the code you write is tied to 1 physical keyboard;
     if you need to work on a different keyboard, you probably need to write new code

##
## Interception Tools

- <https://gitlab.com/interception/linux/tools>
- <https://gitlab.com/interception/linux/plugins/caps2esc>

This can overload  the `Capslock` key to  make it behave like  `Ctrl` when held,
and like `Escape` when tapped.

---

To install the `caps2esc` plugin:

    $ sudo add-apt-repository ppa:deafmute/interception
    $ sudo apt install interception-caps2esc

During the installation, you might be asked this question:

    Would you like to update the recomended config for your interception plugins
    (at /etc/interception/udevmon.d/deafmute-ppa-*.yaml)? [y/n]:

Answer "yes".

### I changed the layout to make the `Enter` key behave like `Ctrl` when held.  How to make it behave like `Enter` when tapped?

`udevmon(1)` is automatically started as a systemd service thanks to this file:

    /etc/systemd/system/multi-user.target.wants/udevmon.service

Which is a symlink to:

    /usr/lib/systemd/system/udevmon.service

`udevmon(1)` only sources this config file:

    /etc/interception/udevmon.d/deafmute-ppa-caps2esc.yaml

Whose contents is:
```yaml
- JOB: intercept -g $DEVNODE | caps2esc -m 1 | uinput -d $DEVNODE
  DEVICE:
    EVENTS:
      EV_KEY: [KEY_CAPSLOCK]
```
Change it like this:
```yaml
 #                                           v----------v
- JOB: intercept -g $DEVNODE | caps2esc -m 1 | enter2ctrl | uinput -d $DEVNODE
  DEVICE:
    EVENTS:
      EV_KEY: [KEY_CAPSLOCK, KEY_ENTER]
 #                           ^-------^
```
`enter2ctrl` should be a custom binary inspired by `caps2esc`.
The README of `interception` gives this starting point:
```c
 #include <stdio.h>
 #include <stdlib.h>
 #include <linux/input.h>

int main(void) {
    setbuf(stdin, NULL), setbuf(stdout, NULL);

    struct input_event event;
    while (fread(&event, sizeof(event), 1, stdin) == 1) {
        if (event.type == EV_KEY && event.code == KEY_X)
            event.code = KEY_Y;

        fwrite(&event, sizeof(event), 1, stdout);
    }
}
```
#### It doesn't behave exactly like I want!

The previous code makes `enter2ctrl` replace the `Enter` keysym *unconditionally*.
If you want  to replace it on  the condition it was tapped  (because that's what
`caps2esc` does), then read the code of `caps2esc`.
Or read this one:
<https://gitlab.com/interception/linux/plugins/space2meta/-/blob/master/space2meta.c>

As for the names of the key that you should write in your code
(e.g. `KEY_CAPSLOCK`), look in this file:

    /usr/include/linux/input-event-codes.h

---

Here is yet another starting point:
```c
 #include <stdio.h>
 #include <stdlib.h>

 #include <unistd.h>
 #include <linux/input.h>

const struct input_event
enter_up     = {.type = EV_KEY, .code = KEY_ENTER,     .value = 0},
ctrl_up      = {.type = EV_KEY, .code = KEY_RIGHTCTRL, .value = 0},
enter_down   = {.type = EV_KEY, .code = KEY_ENTER,     .value = 1},
ctrl_down    = {.type = EV_KEY, .code = KEY_RIGHTCTRL, .value = 1},
enter_repeat = {.type = EV_KEY, .code = KEY_ENTER,     .value = 2},
ctrl_repeat  = {.type = EV_KEY, .code = KEY_RIGHTCTRL, .value = 2},
syn          = {.type = EV_SYN, .code = SYN_REPORT,    .value = 0};

int equal(const struct input_event *first, const struct input_event *second) {
    return first->type == second->type && first->code == second->code &&
           first->value == second->value;
}

int read_event(struct input_event *event) {
    return fread(event, sizeof(struct input_event), 1, stdin) == 1;
}

void write_event(const struct input_event *event) {
    if (fwrite(event, sizeof(struct input_event), 1, stdout) != 1)
        exit(EXIT_FAILURE);
}

int main(void) {
    int enter_is_ctrl = 0;
    struct input_event input, key_down, key_up, key_repeat;
    enum { START, ENTER_HELD, KEY_HELD } state = START;

    setbuf(stdin, NULL), setbuf(stdout, NULL);

    while (read_event(&input)) {
        if (input.type == EV_MSC && input.code == MSC_SCAN)
            continue;

        if (input.type != EV_KEY) {
            write_event(&input);
            continue;
        }

        switch (state) {
            case START:
                if (enter_is_ctrl) {
                    if (input.code == KEY_ENTER) {
                        input.code = KEY_RIGHTCTRL;
                        if (input.value == 0)
                            enter_is_ctrl = 0;
                    }
                    write_event(&input);
                } else {
                    if (equal(&input, &enter_down) ||
                        equal(&input, &enter_repeat)) {
                        state = ENTER_HELD;
                    } else {
                        write_event(&input);
                    }
                }
                break;
            case ENTER_HELD:
                if (equal(&input, &enter_down) || equal(&input, &enter_repeat))
                    break;
                if (input.value != 1) {
                    write_event(&enter_down);
                    write_event(&syn);
                    usleep(20000);
                    write_event(&input);
                    state = START;
                } else {
                    key_down = key_up = key_repeat = input;

                    key_up.value     = 0;
                    key_repeat.value = 2;
                    state            = KEY_HELD;
                }
                break;
            case KEY_HELD:
                if (equal(&input, &enter_down) || equal(&input, &enter_repeat))
                    break;
                if (equal(&input, &key_down) || equal(&input, &key_repeat))
                    break;
                if (!equal(&input, &enter_up)) {
                    write_event(&ctrl_down);
                    enter_is_ctrl = 1;
                } else {
                    write_event(&enter_down);
                }
                write_event(&syn);
                usleep(20000);
                write_event(&key_down);
                write_event(&syn);
                usleep(20000);
                write_event(&input);
                state = START;
                break;
        }
    }
}
```
But there are 2 issues.

First, when  pressing `C-x`, `Ctrl`  and `x` must be  pressed in a  too specific
manner; for  example, it is not  enough for `x` to  be pressed, it must  also be
released (and it must be released while  `Ctrl` is held). `caps2esc` is not that
restrictive.

Second, it  doesn't work  in the  virtual console. `caps2esc`  does work  in the
console, so it should be possible for `enter2ctrl` to work too.

##
## `xkbcomp(1)`

`xkbcomp(1)` can only customize the layout in a GUI program in an X session; not
in a virtual console.

To use it, you would start by running something like this:

    $ setxkbmap -print \
        | sed '/xkb_symbols/s/\([^"]*"\)\([^"]*\)\(".*\)/\1\2+my_symbol_file(my_symbol_map)\3/' \
        >~/.config/xkb/custom_layout

    $ cat <<'EOF' >~/.config/xkb/symbols/my_symbol_file
    // this is a comment
    partial alphanumeric_keys
    xkb_symbols "my_symbol_map" {
        // arbitrary examples of a few mappings (write as many as you want)
        key <TLDE> { [ oe, 1, oe, OE ] };
        key <AE02> { [ eacute, 2, less, Eacute ] };
        key <AE03> { [ quotedbl, 3, greater ] };
        key <AC09> { [ l, L ] };
        key <AD01> { [ a, A, bar ] };
        key <SPCE> { [ space, space, underscore, NoSymbol ] };
    };

To find the name a key on the keyboard (e.g. `<TLDE>`), run this:

    $ xkbprint -label name $DISPLAY - | ps2pdf - >/tmp/pdf.pdf && xdg-open /tmp/pdf.pdf

To find the name of a symbol (e.g. `eacute`), run this:

    $ xkbprint -label symbols $DISPLAY - | ps2pdf - >/tmp/pdf.pdf && xdg-open /tmp/pdf.pdf

`NoSymbol` is a special symbol name which disables a given key+modifier.
A symbol  name is  case sensitive.  For  example, for the  Enter key,  you would
write the symbol name `return`; not `Return`.

On a key line, the four first symbols are meant to be produced with:

   1. no modifier
   2. the `Shift` modifier
   3. the `AltGr` modifier
   4. the `Shift-AltGr` modifier

Finally, you would run this:

    $ xkbcomp -I"$HOME/.config/keyboard/xkb" ~/.config/xkb/custom_layout $DISPLAY
              ^----------------------------^
              tells `xkbcomp(1)` where to look for  included files;
              it also look in the CWD and `/usr/share/X11/xkb/`

---

The way  `setxkbmap(1)` translates  the parameters it  receives into  XKB source
code is governed by this rule file:

    /usr/share/X11/xkb/rules/evdev
    # %m, %l, and %v are probably placeholderswhich will be replaced by resp.
    # the keyboard model, the language and the variant

Inside this code, there are include directives.
Those are resolved by `xkbcomp(1)`:

    # `setxkbmap(1)` argument
    -option terminate:ctrl_alt_bksp
            ^-------^
    →
    # XKB source code
    xkb_symbols   { include "...+terminate(ctrl_alt_bksp)"  };
                                 ^-------^
    →
    # `xkbcomp(1)` includes the `ctrl_alt_bksp` stanza from:
    /usr/share/X11/xkb/symbols/terminate
                               ^-------^

## loadkeys(1)

`loadkeys(1)` can only customize  the layout in a virtual console;  not in a GUI
program in an X session.

To use it, you  would start by writing a config file  whose syntax is documented
at `man 5 keymaps`.  For example, in `~/.config/loadkeys.conf`:

    # make `AltGr-d` emit `]`
    altgr keycode 32 = bracketright

    # make `C-]` emit `^]` (by pressing `AltGr-d` for `]`)
    altgr control keycode 32 = Control_bracketright


    # make `S-Tab` emit `Esc [ Z`
    # see `man 5 keymaps /spare`
    shift keycode 15 = F13
    string F13 = "\033[Z"

    # make `M-@` emit `Esc @`
    altgr alt keycode 11 = F14
    string F14 = "\033@"

    # make `M-Y` emit `Esc Y`
    shift alt keycode 21 = F15
    string F15 = "\033Y"


    # we're going to map some keys to some modifiers;
    # the modifier should only apply to the columns whose index is given here;
    # see `man 5 keymaps /careful`
    keymaps 0-2,4,6,8,12

    keycode 58 = Control
    keycode 42 = Shift

To find the keynumber of a physical key:

    $ showkey
    # press your key
    # to quit: stop pressing any key for 10s

To find the symbol you need to write in your mapping:

    $ dumpkeys --long-info | less
    # this should dump the whole current keyboard layout
    # see `man 5 keymaps /ABBREVIATIONS`

When the config file is read, run:

    $ loadkeys ~/.config/loadkeys.conf

##
## `xmodmap(1)` + `xcape(1)`
### How to use them to make the `Capslock` key behave as `Control` in a chord, and as `Escape` when tapped?

    $ xmodmap -e 'keycode 66 = Control_L'
    $ xmodmap -e 'clear lock'
    $ xmodmap -e 'add control = Control_L'

    $ xcape -e 'Control_L=Escape'

### Same question with `setxkbmap(1)` instead of `xmodmap(1)`.

    $ setxkbmap -option 'caps:ctrl_modifier'

    $ xcape -e 'Caps_Lock=Escape'

##
# Issues
## `xmodmap(1)`
### compatibility

`xmodmap(1)` can  only work with the  X11 display server, not  with Wayland, nor
with the virtual console.

### delay on startup

After  the X  session starts,  if you  start `xmodmap(1)`  automatically from  a
script, you  might need to delay  it.  At least, I  did need a delay  when I was
using it.

Sleeping   for   an   arbitrary   amount   of  time   (a   few   seconds)   felt
brittle/unreliable.

### high CPU consumption

The X.org might consume a lot of CPU after you leave a virtual console.
At least,  it did for  me in the  past (sth like 25%  for for several  dozens of
seconds, IIRC).

### lost customizations

You lose the custom layout whenever you:

   - enter then leave a virtual console
   - suspend then resume a session
   - log out of a session, then log in back
   - terminate the X server (by pressing `M-C-Del`)

### config/results depend on current layout/variant

For  example, when  we  used it  on  XFCE, the  config we  needed  to write  was
different depending  on whether we had  ticked “Use system defaults”  in the
GUI settings, and which variant we had chosen.

### cannot use any variant

`xmodmap(1)` cannot  make a chord  generate a keysym if  the latter does  not by
default.  It can only *change* a keysym which is generated by default by a chord.

   > You can  use xmodmap to redefine  existing mappings as long  as those mappings
   > actually exist in your original keyboard layout.
   > In the case described in the question  you cannot extend behavior of any keys to
   > use AltGr.
   > You can only change the AltGr keysyms for keycodes that are already using AltGr.

Source: <https://unix.stackexchange.com/a/313711/289772>

IIRC, if you still try, `xmodmap(1)` will fail silently.

---

This means that you might be limited to some variants only for your chosen layout.
For example, if your  layout is `fr`, and you want  `AltGr+space` to generate an
underscore, you  can't choose  some variants  (IIRC including  `azerty`) because
they don't make `AltGr+space` generate any keysym by default.

It seems the best variants for `fr` are `latin9` or `oss_latin9`.

`azerty` is too poor (i.e. there's not enough keysyms on some keys).
`oss` is too weird (i.e. too many weird/useless keysyms).

Note that if  you don't choose any `fr` variant,  `AltGr+space` doesn't generate
any keysym.  IOW, you  have to choose a variant for  `AltGr+space` to produce an
underscore.

### tricky to overload 2 keys using `xcape(1)` to make them behave as same logical modifier

Suppose you want to use:

   - `xmodmap(1)` to make 2 keys to behave as the `control` logical modifier
     when used in a chord

   - `xcape(1)` to overload them so that the generate the `a` and `b` keysyms
     when tapped

You can't use `Control_L` for the 2 `xmodmap(1)` expressions.
You have to use different keysyms, like `Control_L` and `Control_R`

Otherwise, if  you used `Control_L`  for both, there  would be an  ambiguity for
`xcape(1)`, which would be unable to know  whether to translate that into `a` or
`b` when the keys are tapped.

And you need to make sure that the modifier map knows that a new keycode is able
to generate the `control` logical modifier, via the command `add`:

    $ xmodmap -e 'add control = Control_L'

### corner case: different modifier map when validating command with `C-m` or `Enter`

IIRC, in our setup, we had a case where the output of this command was different
depending on the key we pressed to run it:

    $ xmodmap -pm

The latter is meant to print the current modifier map.
I  *guess* that  was due  to an  interaction with  `xcape(1)` which  temporarily
changed the modifier map when replacing a keysym.

##
## `xcape(1)`
### compatibility

`xcape(1)` can only work with the X11 display server, not with Wayland, nor with
the virtual console.

### delay on startup

After the X session starts, if you start `xcape(1)` automatically from a script,
you might need to delay it.  At least, I think I needed a delay when I was using
it, just like for `xmodmap(1)`.  Possibly because of the latter...

### high CPU consumption

`xcape(1)` might cause the X.Org process to temporarily consume more CPU than usual.
Last time I used it on an Ubuntu 20.04 machine:

    $ xcape -e 'Control_L=Escape'
    $ xcape -e 'Control_R=Return'

whenever I  tapped the `Capslock`  key to generate  an `Escape` keysym,  the CPU
went from  1/2% to 5/6% or  even more.  This caused  some lag in Vim,  which was
very distracting.

I *think* `xcape(1)` had an undesirable interaction with the Xorg driver used by
default (`modesetting`).

### cannot generate a keysym which is not already generated by at least 1 keycode

`xcape(1)` can't  replace a keysym  S1 into another S2,  if there is  no keycode
generating S2.

For example, suppose you want the `Enter`  key to behave as the control modifier
when held:

    $ xmodmap -e 'keycode 36 = Control_R'
    $ xmodmap -e 'add control = Control_R'

This has removed the only keycode which was generating `Return` from the table.
But for `xcape(1)`  to be able to replace `Control_R`  into `Return`, there must
be at  least 1  keycode generating `Return`,  which is why  you need  this extra
command:

    $ xmodmap -e 'keycode 255 = Return'

Now, `xcape(1)` can work:

    $ xcape -e 'Control_R=Return'

---

To  choose  a good  keycode,  look  for one  which  is  unused in  the  original
non-modified keymap (`$ xmodmap -pke`).  `255` seems like a good fit:

   - it doesn't seem to match a physical key on our keyboard
     (no risk of unexpectedly changing the meaning of a key we sometimes press)

   - it does generate a keysym by default (which is necessary for `xmodmap(1)` to work)

### corner case: spurious `Enter` keypress in VM

Suppose you want to overload the `Enter` key so that:

   1. it behaves like `Ctrl` when held
   2. it behaves like `Enter` when tapped

To achieve  `1.`, you use a  tool working at  the display server level,  such as
`xmodmap(1)` or `xkbcomp(1)`.  And to achieve `2.`, you use `xcape(1)`.

Everything seems to work fine, until you use a VM.
In a VM, when you press `Enter` once, the guest receives it twice.

The issue  comes from `xcape(1)`, because  the issue disappears if  you kill its
process:

    $ killall xcape

The issue has already been reported on `xcape(1)`'s bug tracker:
<https://github.com/alols/xcape/issues/99>

This can have unexpected consequences.  For example:

    $ sudo dpkg-reconfigure <some package>

This command asks you some question.
If you press `Enter`  while in the guest system to validate  an answer, you will
automatically validate the next answer without being able to review it.

As a workaround, you can press `C-m`.

##
## Interception Tools
### `Ctrl+mousewheel` does not work in Firefox

It should change the zoom level of  the current webpage; but it fails when using
pressing the `Capslock`  key (instead of `Ctrl`) while the  `caps2esc` plugin is
running.

