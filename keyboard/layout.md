# ?

How to print all known keymaps for the virtual console?  for X11?

    # for the virtual console
    $ localectl list-keymaps
    # WARNING: doesn't work on debian-based systems because of a known bug:
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=790955

    # for X11
    $ localectl list-x11-keymaps

Wait: There is no `list-x11-keymaps` subcommand.  Why?
What's the systemd alternative?
What's the difference between a keymap and a layout?

---

Alternative:

    $ sed -n '/^! layout/,/^$/p' /usr/share/X11/xkb/rules/evdev.lst

##
# How to customize the virtual console keyboard layout?

    $ sudo tee -a /etc/systemd/system/getty@.service.d/keyboard-layout.conf <<'EOF'
    [Service]
    ExecStartPre=/usr/bin/loadkeys /home/user/.config/keyboard/vc.conf
    EOF

---

`vc.conf` should contain your customizations, such as:

    altgr keycode 3 = less
    ...
    alt keycode 36 = Scroll_Forward
    ...
    keymaps 0-2,4,6,8,12
    keycode 58 = Control
    ...

Use `dumpkeys(1)` to read the current layout and `showkey(1)` to get the code of
a key.  Read `man 5 keymaps` for the syntax of the file.

---

If you tweak `vc.conf`, you can apply the changes immediately, by pressing `C-d`
then re-logging.

---

TODO: Document how to bind a *sequence* of keys to a key.
Basically, you need to bind it to `F123`, then assign the sequence to the string `F123`.
For example, to make `S-Tab` emit `Esc [ Z`:

    shift keycode 15 = F15
    string F15 = "\033[Z"

See `man 5 keymaps /spare`.

##
# What interesting utility does the `kbd` package provide?

    /bin/dumpkeys
    /bin/loadkeys
    /bin/setfont

    /sbin/kbdrate

    /usr/bin/screendump
    /usr/bin/setleds
    /usr/bin/showconsolefont
    /usr/bin/showkey

##
# What's the difference between the *default* keyboard layout and the *current* layout?

The default layout is the one automatically set up when you start the OS.
It persists after a reboot of the OS.

The current layout is the one currently active.
It might or might *not* persist after a reboot of the OS.

The  two   might  be  different  if   you  have  executed  a   command  such  as
`setxkbmap(1)`, or if you've changed the default layout without rebooting.

##
# default layout
## How to print it for X11?

    $ setxkbmap -query

## How to print it for the virtual console and for X11?

    $ localectl status

The virtual console layout will be printed on the line containing `VC Keymap`:

    VC Keymap: fr

The X11 layout will be printed on the next lines:

       X11 Layout: fr
        X11 Model: pc105
      X11 Variant: latin9
      X11 Options: terminate:ctrl_alt_bksp

---

If you've used  the GUI to untick  “Use system defaults” (Settings  > Keyboard >
Layout), `$ setxkbmap -query` shows all the layouts you've added.
`$ localectl status` only shows you the current layout.

## How to set it for the virtual console and for X11, choosing the 'fr' layout?

    $ localectl set-keymap fr

Or:

    $ localectl set-x11-keymap fr


Or:

    $ sudo dpkg-reconfigure keyboard-configuration
    # It will ask you some questions (the 2nd one is the relevant one).

             Country of origin for the keyboard:
                    French

---

Yes,  `set-keymap` affects  the  X11 layout,  and  `set-x11-keymap` affects  the
virtual console layout.

---

Bug:

If you  use `set-x11-keymap`,  you'll need  to reboot the  OS twice  (instead of
once) before the virtual console layout is set up.

## How to set it for X11 only?

    $ localectl --no-convert set-x11-keymap fr
                ^----------^

Bug:

The  virtual console  layout is  (wrongly) affected  by this  command after  the
second reboot of the OS.

Don't rely on the  output of `$ localectl status` to get  the new default layout
for the virtual console.
It will still report the old one.

---

Alternative: try to manually update the file `/etc/default/keyboard`.

## How to set it for the virtual console only?

    $ localectl --no-convert set-keymap fr
                ^----------^

Bug:

No  layout  is affected  by  this  command,  even  though `$  localectl  status`
correctly reports that the virtual console layout has changed to 'fr'.

It might be a  bug, caused by the lack of  a `systemd-vconsole-setup` service on
debian:

    $ journalctl --unit=systemd-localed --since '5m ago' --no-hostname
    systemd-localed[1234]: Changed virtual console keymap to 'fr' toggle ''
    systemd-localed[1234]: Failed to issue method call: Unit systemd-vconsole-setup.service not found.
    systemd-localed[1234]: Failed to request keymap reload: No such file or directory

For more info, see:

- <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=755194>
- <https://bugzilla.redhat.com/show_bug.cgi?id=837292>

---

Alternative: try to manually update the file `/etc/vconsole.conf`.

##
## Why is `set-x11-keymap` better than `set-keymap`?

With `set-x11-keymap`, you can specify:

   1. the keyboard model
   2. the layout variant
   3. xkb options

Example:

    $ localectl set-x11-keymap fr pc105 latin9 terminate:ctrl_alt_bksp

## Why do these commands have different syntaxes?

Probably because the  main purpose of `set-keymap`  is to set the  layout of the
virtual console.   And the  latter doesn't  support a  keyboard model,  a layout
variant, nor xkb options.

#
## Which files are altered after executing these commands?

    /etc/default/keyboard (X11)
    /etc/vconsole.conf (virtual console)

##
## What does `$ dpkg-reconfigure console-setup` allow me to set up?

Essentially, the fontface and the fontsize used in a virtual console.

## What does `$ dpkg-reconfigure console-data` allow me to set up?

Nothing.

Yes, it lets you choose a keymap, but it doesn't seem to have any effect.

It's only useful to get additional keymaps and fonts for the virtual console.

## Which file(s) do these commands change?

`$ dpkg-reconfigure console-setup` alters `/etc/default/console-setup`.

`$ dpkg-reconfigure console-data` doesn't seem to alter any file.

##
## Why does `$ localectl status` ignore any change performed by `setxkbmap(1)`?

`setxkbmap(1)` alters the *current* layout.

`$ localectl status` shows information  about the *default* keyboard layouts for
X11 and the  virtual console, using the contents  of `/etc/default/keyboard` and
`/etc/vconsole.conf`.

The default layout is not the same thing as the current layout.

##
# current layout
## How to set it, choosing the `pc105` model, `fr` layout, `latin9` variant, and enabling M-C-del?

    $ setxkbmap -model pc105 -layout fr -variant latin9 -option terminate:ctrl_alt_bksp

Note that this command doesn't survive a reboot of the OS, nor a restart of Xorg.
It doesn't alter `/etc/default/keyboard`.

##
## What's the main difference between `setxkbmap(1)` and `localectl set[-x11]-keymap`?

`setxkbmap` sets the *current* layout.
Its effect doesn't persist after a reboot of the OS.

`localectl set[-x11]-keymap` sets the *default* layout.
Its effect *does* persist after a reboot of the OS.

##
# setxkbmap
## How to make `setxkbmap(1)` print a keyboard description?

Use the `-print` option:

    $ setxkbmap -model pc105 -layout fr -variant latin9 -option terminate:ctrl_alt_bksp -print
                                                                                        ^----^

---

The output will look like this:

    xkb_keymap {
            xkb_keycodes  { include "evdev+aliases(azerty)" };
            xkb_types     { include "complete"      };
            xkb_compat    { include "complete"      };
            xkb_symbols   { include "pc+fr(latin9)+inet(evdev)+terminate(ctrl_alt_bksp)"    };
            xkb_geometry  { include "pc(pc105)"     };
    };

---

Note  that each  parameter  passed  to `setxkbmap(1)`  has  been  turned into  a
directive, inside the `xkb_keymap` stanza:

    -model pc105                     →  xkb_geometry { include "pc(pc105)" };
    -layout fr -variant latin9       →  xkb_symbols  { include "...+fr(latin9)+... };
    -option terminate:ctrl_alt_bksp  →  xkb_symbols  { include "...+terminate(ctrl_alt_bksp)" };

## What does this output stand for?

An XKB source file.

## How does `setxkbmap(1)` know how to translate the parameters it receives into an `xkb_keymap` stanza?

The translation is governed by a rule file:

    /usr/share/X11/xkb/rules/evdev

Using the rule file, `setxkbmap(1)` translates  each of its parameters to create
an XKB source file.  For example, the parameter:

    -option terminate:ctrl_alt_bksp

is translated into:

    xkb_symbols   { include "...+terminate(ctrl_alt_bksp)"  };
                                ^-----------------------^

## What are `%m`, `%l` and `%v` in the rule file?

Probably placeholders  which will be replaced  by resp. the keyboard  model, the
language and the variant.

## How are the include directives, contained in the output of `setxkbmap(1)`, resolved?

`setxkbmap(1)` generates an  XKB source file, which it passes to `xkbcomp(1)`.
The latter resolves the include directives, by importing the appropriate stanzas.

For  example,  if  you  used the  `-option  terminate:ctrl_alt_bksp`  parameter,
`xkbcomp(1)` imports the `ctrl_alt_bksp` stanza from:

    /usr/share/X11/xkb/symbols/terminate

The other parameters passed to the include directive are similarly resolved:

    pc           →  /usr/share/X11/xkb/symbols/pc
    fr(latin9)   →  /usr/share/X11/xkb/symbols/fr    (/xkb_symbols "latin9")
    inet(evdev)  →  /usr/share/X11/xkb/symbols/inet  (/xkb_symbols "evdev")

##
# xkbcomp
## How to update the current keymap using the keyboard description stored in `~/.config/xkb/map`?

    $ xkbcomp -I$HOME/.config/xkb $HOME/.config/xkb/map $DISPLAY
      │         │                 │                     │
      │         │                 │                     └ use the compiled keymap to update the keymap
      │         │                 │                       for the current display (aka destination; optional)
      │         │                 │
      │         │                 └ my keyboard description (aka source; mandatory)
      │         │
      │         └ when my keyboard description includes a file,
      │           look for it inside this directory
      │           (in addition to the cwd, and `/usr/share/X11/xkb/`)
      │
      └ compile an XKB keyboard description

## How to generate an XKB source file for the currently used keymap?

    $ xkbcomp $DISPLAY keymap.xkb
                       │
                       └ optional argument
                         without it, the file would be named 'server-0_0.xkb'

The generated  XKB source file  is fully resolved,  i.e. it doesn't  contain any
`include` directive.

## How to update the keymap for the current display with an XKB source file?

    $ xkbcomp keymap.xkb $DISPLAY
                          │
                          └ not optional

## How to generate a compiled keymap from an XKB source file?

    $ xkbcomp keymap.xkb

This will generate a compiled keymap inside:

    keymap.xkm
             │
             └ coMpiled

## How to generate an XKB source file from a compiled keymap?

    $ xkbcomp keymap.xkm

This will generate a source keymap inside:

    keymap.xkb
             │
             └ source

##
# Various links

Get ideas on where to put some characters in new keyboard layout:
<http://bepo.fr/wiki/Utilisateur:Kaze/B%C3%A9po-intl#Variante_.C2.AB.C2.A0d.C3.A9veloppeur.C2.A0.C2.BB>

---

X11 specific:

   - <http://www.xfree86.org/current/XKB-Config.html>
   - <http://pascal.tsu.ru/en/xkb/>
   - <https://www.charvolant.org/doug/xkb/>
   - <https://wiki.archlinux.org/index.php/Keyboard_input>
   - <https://wiki.archlinux.org/index.php/Keyboard_shortcuts>
   - <https://wiki.archlinux.fr/Keyboard>
   - <https://help.ubuntu.com/community/Custom%20keyboard%20layout%20definitions>
   - <https://wiki.archlinux.org/index.php/Keyboard_Configuration_in_Xorg>
   - <https://wiki.archlinux.org/index.php/locale#LC_COLLATE:_collation>
   - <https://wiki.archlinux.org/index.php/Keyboard_Configuration_in_Xorg#Using_X_configuration_files>
   - <http://rlog.rgtti.com/2014/05/01/how-to-modify-a-keyboard-layout-in-linux/>
   - <https://a3nm.net/blog/xkbcomp.html>
   - <https://web.archive.org/web/20170825051821/http://madduck.net:80/docs/extending-xkb/>

The last link is interesting for the systemd unit file at the end.
We could use it as a template for our own services.
Although, we could also read the examples in `man systemd.unit`.

---

Virtual Console specific:

   - `man 5 keyboard`
   - <https://wiki.archlinux.org/index.php/Color_output_in_console>
   - <https://wiki.archlinux.org/index.php/Linux_console>
   - <https://wiki.archlinux.org/index.php/Linux_console/Keyboard_configuration>
   - <https://wiki.archlinux.org/index.php/Screen_capture#Virtual_console>
   - <https://superuser.com/questions/290115/how-to-change-console-keymap-in-linux>
   - <https://wiki.archlinux.org/index.php/Linux_console/Keyboard_configuration>

##
# How do keyboard input and text output work?

<https://unix.stackexchange.com/questions/116629/how-do-keyboard-input-and-text-output-work/116630#116630>

# How to capture the output of all past commands in a virtual console?

<https://wiki.archlinux.org/index.php/Screen_capture#Virtual_console>

    $ setterm -dump 1 -file screen.dump

---

DESCRIPTION

setterm  writes to  standard  output a  character string  that  will invoke  the
specified terminal capabilities.
Where possible terminfo is consulted to find the string to use.
Some options however (marked "virtual consoles only" below) do not correspond to
a terminfo(5) capability.
In this case, if  the terminal type is "con" or "linux"  the string that invokes
the specified capabilities on the PC Minix virtual console driver is output.
Options that are not implemented by the terminal are ignored.

    --dump [console_number]

Writes a  snapshot of  the virtual  console with  the given  number to  the file
specified with  the `--file`  option, overwriting its  contents; the  default is
`screen.dump`.
Without an argument, it dumps the current virtual console.
This overrides `--append`.

    --file filename

Sets the snapshot file  name for any `--dump` or `--append`  options on the same
command-line.
If  this option  is  not present,  the  default is  screen.dump  in the  current
directory.
A path  name that exceeds the  system maximum will be  truncated, see `PATH_MAX`
from linux/limits.h for the value.

    --append [console_number]

Like `--dump`, but appends to the snapshot file instead of overwriting it.
Only works if no `--dump` options are given.

# How to customize the keyboard layout with Wayland?

- <https://unix.stackexchange.com/questions/212573/how-can-i-make-backspace-act-as-escape-using-setxkbmap>
- <https://unix.stackexchange.com/questions/294286/how-can-i-autoload-xkb-customisations-in-gnome>
- <https://unix.stackexchange.com/questions/292868/how-to-customise-keyboard-mappings-with-wayland>
- <https://realh.co.uk/wp/linux-keymap-hacking/>

# Where is the currently used keymap?

All the keymaps are in:

    /usr/share/X11/xkb/symbols/

Each file in  this directory contains several keymap, all  dedicated to the same
language.

For example, the keymap for French are in:

    /usr/share/X11/xkb/symbols/fr

##
##
##
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
## `$ localectl list-keymaps` doesn't work!

    Couldn't find any console keymaps.

    Failed to read list of keymaps: No such file or directory

It comes  from the fact that  the package `console-data` installs  some archives
with the extension `.kmap.gz`, while `localectl(1)` expects `.map.gz`.
This is a debian bug:

<https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=790955>

You could temporarily fix the issue by executing:

    $ sudo apt install console-data
    $ sudo updatedb
    $ locate kmap.gz | vim -
    :saveas /tmp/sh.sh
    :% substitute/^/mv /
    :% substitute/kmap\.gz$/{kmap.gz,map.gz}/
    :0 put ='#!/bin/bash'
    :exit
    $ chmod +x /tmp/sh.sh
    $ sudo /tmp/sh.sh

    # the command should now work
    $ localectl list-keymaps

To undo the fix:

    $ vim /tmp/sh.sh
    :% substitute/{kmap.gz,map.gz}/{map.gz,kmap.gz}/
    :exit
    $ sudo /tmp/sh.sh

## I've executed `$ localectl set-x11-keymap us`, but the virtual console keyboard layout has not been changed!

Restart the OS a second time.

If you  have installed the package  `console-data`, and if you  have renamed the
archives `.kmap.gz` installed by the  latter, using the `.map.gz` extension, the
virtual console layout will be correctly set after the first reboot of the OS.

## `$ localectl <subcommand> <args>` doesn't work!

`localectl(1)`  invokes the  service `systemd-localed`,  so have  a look  at the
journal, to see which issue the latter has encountered:

    $ journalctl --no-hostname --since '5m ago' -u systemd-localed

Alternatively, trace the `localectl` process:

    $ strace -o /tmp/log localectl <subcommand> <args>

##
## Which issues can I encounter if I use
### `xmodmap(1)`
#### compatibility

`xmodmap(1)` can  only work with the  X11 display server, not  with Wayland, nor
with the virtual console.

#### delay on startup

After  the X  session starts,  if you  start `xmodmap(1)`  automatically from  a
script, you  might need to delay  it.  At least, I  did need a delay  when I was
using it.

Sleeping   for   an   arbitrary   amount   of  time   (a   few   seconds)   felt
brittle/unreliable.

#### high CPU consumption

The X.org might consume a lot of CPU after you leave a virtual console.
At least,  it did for  me in the  past (sth like 25%  for for several  dozens of
seconds, IIRC).

#### lost customizations

You lose the custom layout whenever you:

   - enter then leave a virtual console
   - suspend then resume a session
   - log out of a session, then log in back
   - terminate the X server (by pressing `M-C-Del`)

#### config/results depend on current layout/variant

For  example, when  we  used it  on  XFCE, the  config we  needed  to write  was
different depending  on whether we had  ticked “Use system defaults”  in the
GUI settings, and which variant we had chosen.

#### cannot use any variant

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

#### tricky to overload 2 keys using `xcape(1)` to make them behave as same logical modifier

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

#### corner case: different modifier map when validating command with `C-m` or `Enter`

IIRC, in our setup, we had a case where the output of this command was different
depending on the key we pressed to run it:

    $ xmodmap -pm

The latter is meant to print the current modifier map.
I  *guess* that  was due  to an  interaction with  `xcape(1)` which  temporarily
changed the modifier map when replacing a keysym.

###
### `xcape(1)`
#### compatibility

`xcape(1)` can only work with the X11 display server, not with Wayland, nor with
the virtual console.

#### delay on startup

After the X session starts, if you start `xcape(1)` automatically from a script,
you might need to delay it.  At least, I think I needed a delay when I was using
it, just like for `xmodmap(1)`.  Possibly because of the latter...

#### high CPU consumption

`xcape(1)` might cause the X.Org process to temporarily consume more CPU than usual.
Last time I used it on an Ubuntu 20.04 machine:

    $ xcape -e 'Control_L=Escape'
    $ xcape -e 'Control_R=Return'

whenever I  tapped the `Capslock`  key to generate  an `Escape` keysym,  the CPU
went from  1/2% to 5/6% or  even more.  This caused  some lag in Vim,  which was
very distracting.

I *think* `xcape(1)` had an undesirable interaction with the Xorg driver used by
default (`modesetting`).

#### cannot generate a keysym which is not already generated by at least 1 keycode

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

#### corner case: spurious `Enter` keypress in VM

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

    $ sudo dpkg-reconfigure keyboard-configuration

This command asks you some question.
If you press `Enter`  while in the guest system to validate  an answer, you will
automatically validate the next answer without being able to review it.

As a workaround, you can press `C-m`.

###
### Interception Tools
#### `Ctrl+mousewheel` does not work in Firefox

It should change the zoom level of  the current webpage; but it fails when using
pressing the `Capslock`  key (instead of `Ctrl`) while the  `caps2esc` plugin is
running.

