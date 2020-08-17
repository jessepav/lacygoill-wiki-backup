# ?

Some key combinations may produce a no-break space, or some variant of the latter.
To get a list of those, run `:UnicodeTable`,  then search for 'no-break':

    U+00A0  NO-BREAK SPACE
    U+202F  NARROW NO-BREAK SPACE
    U+FEFF  ZERO WIDTH NO-BREAK SPACE

Those characters are rarely useful, and they may cause issues which are hard to debug.
It's better to disable them.
To do so, you can run:

    setxkbmap -option 'nbsp:none'

Or, if you use xmodmap, you can edit `~/.Xmodmap`.
In that case,  you need to look  for the string 'no-break' (or  just 'break', or
'space') as well as the codes `00a0`, `202f`, `feff`.
Then, replace these keysyms with other less problematic/more useful.

Finally, if you create your own layout  with xkbcomp, just make sure that no key
combination generate one of those exotic spaces.

# ?

Document  that when  you install  xbindkeys, the  latter installs  some kind  of
autostart script.

It fails to  start if you don't  create a file in `~/.xbindkeysrc`  (we don't so
we're ok), but still it's probably better to disable it:

    Settings
    > Session and Startup
    > Application Autostart
    > untick “xbindkeys (Start xbindkeys)”

Otherwise, I  think your systemd  journal will  be polluted with  error messages
about xbindkeys which doesn't find its config file.

# ?

- <https://wiki.archlinux.org/index.php/Color_output_in_console>
- <https://wiki.archlinux.org/index.php/Keyboard_input>
- <https://wiki.archlinux.org/index.php/Keyboard_shortcuts>
- <https://wiki.archlinux.org/index.php/Linux_console>
- <https://wiki.archlinux.org/index.php/Linux_console/Keyboard_configuration>
- <https://wiki.archlinux.org/index.php/Screen_capture#Virtual_console>
- <https://wiki.archlinux.fr/Keyboard>

---

/usr/share/keymaps/i386/azerty/fr-pc.kmap.gz
/usr/share/keymaps/i386/include/azerty-layout.inc.gz
/usr/share/keymaps/i386/include/linux-with-alt-and-altgr.inc.gz
/usr/share/keymaps/i386/include/linux-keys-bare.inc.gz

---

- <https://superuser.com/questions/290115/how-to-change-console-keymap-in-linux>

- <https://wiki.archlinux.org/index.php/Linux_console/Keyboard_configuration>
- <https://wiki.archlinux.org/index.php/Keyboard_Configuration_in_Xorg>
- <https://wiki.archlinux.org/index.php/locale#LC_COLLATE:_collation>
- <https://wiki.archlinux.org/index.php/Keyboard_Configuration_in_Xorg#Using_X_configuration_files>

The last link is interesting for the systemd unit file at the end.
We could use it as a template for our own services.
Although, we could also read the examples in `man systemd.unit`.

# ?

Document why using `xkbcomp` is better than `xmodmap`.
With xmodmap:

   - we lose the custom layout whenever we enter then leave a console

   - we lose the custom layout when we suspend-resume a session / terminate the
     X server (M-C-del)

   - Xorg consumes a lot of cpu after we leave a console

   - the  result seems  to  be  affected by  whether  we  tick “Use  system
     defaults” in GUI, and which variant we choose (which is important when we
     want to make AltGr + SPC generate an underscore) (note that we should rely
     on the cli only, not on the GUI, nor on a DE)

   - we need to delay the invocation of xmodmap by an arbitrary amount of time
     (a few seconds) which feels brittle/unreliable

     Indeed, a few seconds after the OS has started (in a VM between 7s and 8s),
     the modifier map is reset:

       * `Alt_R (0x6c)` is removed from `mod1`.
       * `Control_R (0x24)` is removed from `control`.
       * `Control_L (0x42)` is moved from `control` to `lock`.

      Btw, I don't know what this `Alt_R` keysym is.
      But it's there by default.
      You can capture it in a script started at launch.
      Something removes shortly after.
      By  the time  you open  a terminal,  it's too  late, it  already has  been
      removed.

      *I think xcape also needs to be delayed... because of xmodmap?*

# ?

Il semble que le moment où les commandes `xmodmap` et `xcape` sont exécutées, et
leur ordre, a de l'importance.

En  effet,  atm,  je  n'ai  pas   trouvé  de  moyen  fiable  de  faire  exécuter
automatiquement certaines commandes à `xmodmap`.

Je suis obligé de le faire manuellement.
J'ai le même pb avec `xcape`.

Pex, imaginons le script suivant:

    xmodmap -e 'keycode 66 = Control_L'
    xmodmap -e 'clear lock'
    xmodmap -e 'add control = Control_L'
    echo 'the script was executed' > ~/Desktop/test_script.log

Ce script devrait transformer la touche capslock en control.

Si  on  rend  ce  script  exécutable  (chmod  +x)  et  qu'on  le  fait  exécuter
automatiquement  par  le  système  au  démarrage,  soit  via  un  outil  en  GUI
(`Session and Startup`), soit via  `/etc/rc.local`, la touche capslock garde son
comportement d'origine.

Pk ?

On sait  que le  pb ne  vient pas  du script  qui n'aurait  pas exécuté,  car le
fichier `~/Desktop/test_script.log` a bien été créé.

J'ai le même pb avec `xcape`:

    xcape -e 'Alt_L=Alt_L|Q'

Cette commande traduit  un `Alt_L`, tapé seul,  en `M-q`.  Je n'arrive  pas à la
faire exécuter automatiquement.

Update:
J'ai corrigé  le pb en retardant  l'exécution des commandes via  un `sleep 1s`
dans `~/bin/autostartrc`.

# ?

Pour  que 2  touches distinctes  génèrent un  même modificateur  (M0) qd  on les
maintient enfoncées, tout  en générant leur keysym d'origine (K1,  K2) qd on les
presse seules,  on est obligé  de leur  faire générer des  keysyms modificateurs
différents (M1, M2).

Autrement, si on utilisait un même modificateur (M3), on aurait aucun moyen pour
expliquer à `xcape` s'il doit le traduire en K1 ou en K2.

De ce fait, il faut choisir comme valeur pour M2 un 2e modificateur.

Si M2 a le même comportement que  M1 (ex: `Control_R` a le même comportement que
`Control_L`), alors il suffit simplement de s'assurer que la modifier map est au
courant qu'un nouveau keycode est capable de générer M0, via la commande `add`.

En  revanche, si  M2  a un  comportement  différent, il  faut  alors changer  sa
signification via 2 commandes (`remove` et `add`).  Ex:

    xmodmap -e 'remove mod4 = Hyper_L'
    xmodmap -e 'add control = Hyper_L'

Dans cet  exemple, on  change le  sens de `Hyper_L`  pour qu'il  soit interprété
comme un control.

Le  choix  de  M2  est  important  car il  peut  avoir  des  effets  secondaires
indésirables.

Pex, j'ai essayé d'utiliser `Super_R` comme modificateur intermédiaire, pour que
la touche BackSpace puisse jouer le rôle d'un alt.

Pb: qd  je tapais  `M-j` ou  `M-l`, il  semble que  le gestionnaire  de fenêtres
interceptait `C-M-j` et `C-M-l` et nous faisait déplacer de bureau virtuel.

Il vaut donc mieux choisir un modificateur qui a peu d'influence comme:

    Shift_R
    Control_R
    Hyper_R

Se méfier de `Super_R`, et peut-être aussi de `Caps_Lock`, `Num_Lock`.

# ?

    $ xmodmap -e 'keycode  65 = space space space space space space'

    X11 variants

            French (alt.) | oss
            French (alt., Latin9-only) | oss_latin9
            French (alt., no dead keys) | oss_nodeadkeys
            French (alt., with Sun dead keys) | oss_sundeadkeys
            French (AZERTY) | azerty
            French (Bepo, ergonomic, Dvorak way) | bepo
            French (Bepo, ergonomic, Dvorak way, Latin9-only) | bepo_latin9
            French (Breton) | bre
            French (Dvorak) | dvorak
            French (legacy, alt.) | latin9
            French (legacy, alt., no dead keys) | latin9_nodeadkeys
            French (legacy, alt., with Sun dead keys) | latin9_sundeadkeys
            French (Macintosh) | mac
            French (no dead keys) | nodeadkeys
            French (with Sun dead keys) | sundeadkeys

    X11 options

            lv3:ralt_switch

You can choose two variants:

    ┌────────────────────────────┬────────────┐
    │ French (alt., Latin9-only) │ oss_latin9 │
    ├────────────────────────────┼────────────┤
    │ French (legacy, alt.)      │ latin9     │
    └────────────────────────────┴────────────┘

Don't choose:

    ┌─────────────────┬────────┐
    │ French (AZERTY) │ azerty │
    └─────────────────┴────────┘

It's too poor (i.e. there's not enough keysyms on some keys).

Don't choose:

    ┌───────────────┬─────┐
    │ French (alt.) │ oss │
    └───────────────┴─────┘

It's shitty (i.e. too many weird/useless keysyms).

If  you don't  choose any  variant, you  won't  be able  to make  AltGr +  Space
generate an underscore (a little too poor).

---

If you use the GUI to untick “Use system defaults”:

    Settings
    Keyboard
    Layout

You have to choose this variant:

    French (legacy, alternative) (⇔ latin9)

Otherwise, no underscore.
Also,  whatever you  choose with  `dpkg-reconfigure keyboard-configuration`,  it
seems to be ignored.
Also, you can change the layout without restarting the OS.

If you don't untick “Use system defaults”, you can use `oss_latin9` as well, but
you need to  re-execute `~/bin/keyboard.sh` a few seconds after  the session has
started.
And, if you change the layout, I think  you need to restart the OS (at least the
X server, and maybe the OS for the underscore).

Also, when you execute `xmodmap -pm`, the  output seems to depend on the key you
pressed to validate the command (Enter vs C-m).

##
##
##
# How to customize the console keyboard layout?

    $ cat <<'EOF' | sudo tee -a /etc/systemd/system/getty@.service.d/keyboard-layout.conf
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

Use `dumpkeys` to read the current layout and `showkey` to get the code of a key.
Read `man 5 keymaps` for the syntax of the file.

---

If you tweak  `vc.conf`, you can apply the changes  immediately, by pressing C-d
then re-logging.

---

TODO: Document how to bind a *sequence* of keys to a key.
Basically, you need to bind it to `F123`, then assign the sequence to the string `F123`.
For example, to make `S-Tab` emit `Esc [ Z`:

    shift keycode 15 = F15
    string F15 = "\033[Z"

See `man 5 keymaps /spare`.

##
# Where can I find a list of all the possible options that I can pass to `setxkbmap`?

    man 7 xkeyboard-config

##
# What interesting utility does `kbd` provide?

    /bin/dumpkeys
    /bin/loadkeys
    /bin/setfont

    /sbin/kbdrate

    /usr/bin/screendump
    /usr/bin/setleds
    /usr/bin/showconsolefont
    /usr/bin/showkey

##
# I have the decimal keycode of a key.  How to find all the keysyms it can generate (w/ or w/o modifier)?

Convert the code in hexadecimal:

    $ dec2hex <keycode>

Then, run `xkeycaps`:

    $ xkeycaps -keyboard pc105fr
                         │
                         └ found in the output of `$ xkeycaps -h` (/french)

1. On the picture, find the key whose lower-right corner contains your hex keycode.
2. Hover the cursor over this key.
3. At the top of the window, on the second line, read the keysyms following `KeySym:`.

##
# What's the difference between the DEFAULT keyboard layout and the CURRENT layout?

The default layout is the one automatically set up when you start the OS.
It persists after a reboot of the OS.

The current layout is the one currently active.
It may or may NOT persist after a reboot of the OS.

The two may be different if you  have executed a command such as `setxkbmap`, or
if you've changed the default layout without rebooting.

##
# default layout
## How to print it for X11?

    $ setxkbmap -query

## How to print it for the console and for X11?

    $ localectl status

The console layout will be printed on the line containing `VC Keymap`:

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

## How to set it for the console and for X11, choosing the 'fr' layout?

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
console layout.

---

Bug:

If you  use `set-x11-keymap`,  you'll need  to reboot the  OS twice  (instead of
once) before the console layout is set up.

## How to set it for X11 only?

    $ localectl --no-convert set-x11-keymap fr
                ^----------^

Bug:

The console layout is (wrongly) affected by this command after the second reboot
of the OS.

Don't rely on the  output of `$ localectl status` to get  the new default layout
for the console.
It will still report the old one.

---

Alternative: try to manually update the file `/etc/default/keyboard`.

## How to set it for the console only?

    $ localectl --no-convert set-keymap fr
                ^----------^

Bug:

No  layout  is affected  by  this  command,  even  though `$  localectl  status`
correctly reports that the console layout has changed to 'fr'.

It may be a bug, caused by the lack of a `systemd-vconsole-setup` service on debian:

    $ journalctl -u systemd-localed --since '5m ago' --no-hostname

        systemd-localed[1234]: Changed virtual console keymap to 'fr' toggle ''~
        systemd-localed[1234]: Failed to issue method call: Unit systemd-vconsole-setup.service not found.~
        systemd-localed[1234]: Failed to request keymap reload: No such file or directory~

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
console.
And  the latter  doesn't support  a keyboard  model, a  layout variant,  nor xkb
options.

#
## Which files are altered after executing these commands?

    /etc/default/keyboard (X11)
    /etc/vconsole.conf (console)

##
## What does `$ dpkg-reconfigure console-setup` allow me to set up?

Essentially, the fontface and the fontsize used in a console.

## What does `$ dpkg-reconfigure console-data` allow me to set up?

Nothing.

Yes, it lets you choose a keymap, but it doesn't seem to have any effect.

It's only useful to get additional keymaps and fonts for the console.

## Which file(s) do these commands change?

`dpkg-reconfigure console-setup` alters `/etc/default/console-setup`.

`dpkg-reconfigure console-data` doesn't seem to alter any file.

##
## Why does `$ localectl status` ignore any change performed by `setxkbmap(1)`?

`setxkbmap(1)` alters the CURRENT layout.

`$  localectl  status` shows  information  about  the DEFAULT  keyboard  layouts
for  X11 and  the console,  using  the contents  of `/etc/default/keyboard`  and
`/etc/vconsole.conf`.

The default layout is not the same thing as the current layout.

##
# current layout
## How to set it, choosing the 'pc105' model, 'fr' layout, 'latin9' variant, and enabling M-C-del?

    $ setxkbmap -model pc105 -layout fr -variant latin9 -option terminate:ctrl_alt_bksp

Note that this command doesn't survive a reboot of the OS, nor a reboot of Xorg.
It doesn't alter `/etc/default/keyboard`.

##
## What's the main difference between `setxkbmap` and `localectl set[-x11]-keymap`?

`setxkbmap` sets the CURRENT layout.
Its effect doesn't persist after a reboot of the OS.

`localectl set[-x11]-keymap` sets the DEFAULT layout.
Its effect DOES persist after a reboot of the OS.

##
##
##
# keymap
## Where is the keymap for the layout “fr”?

    /usr/share/X11/xkb/symbols/fr

## How to get the names of the keys (such as AE01) used in a keymap?

    $ zathura <(xkbprint -label name $DISPLAY - | ps2pdf -)
                │         ├────────┘ │        │
                │         │          │        └ output
                │         │          └ source
                │         │
                │         └ label to be printed on keys
                │           (legal types are: none, name, code, symbols)
                │
                └ print an XKB keyboard description

## How to get the symbols of the keys?

    $ zathura <(xkbprint -label symbols $DISPLAY - | ps2pdf -)

##
# How to print all known
## keymaps for the console?  for X11?

    # for the console
    $ localectl list-keymaps

    # for X11
    $ localectl list-x11-keymaps

Alternative:

    $ sed -n '/^! layout/,/^$/p' /usr/share/X11/xkb/rules/evdev.lst

## keyboard models?  (2)

    $ localectl list-x11-keymap-models

    $ sed -n '/^! model/,/^$/p' /usr/share/X11/xkb/rules/evdev.lst

## layout variants?  (2)

    $ localectl list-x11-keymap-variants

    $ sed -n '/^! variant/,/^$/p' /usr/share/X11/xkb/rules/evdev.lst

## XKB options?  (2)

    $ localectl list-x11-keymap-options

    $ sed -n '/^! option/,/^$/p' /usr/share/X11/xkb/rules/evdev.lst

##
# setxkbmap
## How to make `setxkbmap` print a keyboard description?

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

Note that each parameter passed to `setxkbmap` has been turned into a directive,
inside the `xkb_keymap` stanza:

    -model pc105                     →  xkb_geometry { include "pc(pc105)" };
    -layout fr -variant latin9       →  xkb_symbols  { include "...+fr(latin9)+... };
    -option terminate:ctrl_alt_bksp  →  xkb_symbols  { include "...+terminate(ctrl_alt_bksp)" };

## What does this output stand for?

An XKB source file.

## How does `setxkbmap` know how to translate the parameters it receives into an `xkb_keymap` stanza?

The translation is governed by a rule file:

    /usr/share/X11/xkb/rules/evdev

Using the rule file, `setxkbmap` translates  each of its parameters to create an
XKB source file.
For example, the parameter:

    -option terminate:ctrl_alt_bksp

is translated into:

    xkb_symbols   { include "...+terminate(ctrl_alt_bksp)"  };
                                ^-----------------------^

## What are `%m`, `%l` and `%v` in the rule file?

Probably placeholders which will be replaced  with resp. the keyboard model, the
language and the variant.

## How are the include directives, contained in the output of `setxkbmap`, resolved?

`setxkbmap` generates an  XKB source file, which it passes to `xkbcomp`.
The latter resolves the include directives, by importing the appropriate stanzas.

For  example,  if  you  used the  `-option  terminate:ctrl_alt_bksp`  parameter,
`xkbcomp` imports the `ctrl_alt_bksp` stanza from:

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
##
##
# How to customize the keyboard layout?

- <https://askubuntu.com/questions/422650/map-altgr-a-z-and-shift-altgr-a-z-to-greek-letter>
- <http://rlog.rgtti.com/2014/05/01/how-to-modify-a-keyboard-layout-in-linux/>
- <https://a3nm.net/blog/xkbcomp.html>
- <https://web.archive.org/web/20170825051821/http://madduck.net:80/docs/extending-xkb/>
- <https://wiki.debian.org/XStrikeForce/InputHotplugGuide>
- <http://pascal.tsu.ru/en/xkb/>
- <https://web.archive.org/web/20160623193905/http://git.madduck.net/v/etc/xsession.git?a=blob;f=.xmodmap;h=bfc01f988893adedec7a70eecef46a0900b5772b>

# keyboard shortcuts

- <https://wiki.archlinux.org/index.php/Keyboard_shortcuts>
- <https://unix.stackexchange.com/questions/116629/how-do-keyboard-input-and-text-output-work/116630#116630>

# How does xmodmap work?

- <https://wiki.archlinux.org/index.php/Xmodmap>
- <https://wiki.archlinux.org/index.php/Keyboard_input>
- <https://wiki.archlinux.org/index.php/Xbindkeys>
- <https://wiki.archlinux.org/index.php/Xorg>

# How to capture the output of all past commands in a virtual terminal?

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
specified  with the  --file option,  overwriting  its contents;  the default  is
screen.dump.
Without an argument, it dumps the current virtual console.
This overrides --append.

       --file filename

Sets the  snapshot file  name for  any --dump  or --append  options on  the same
command-line.
If  this option  is  not present,  the  default is  screen.dump  in the  current
directory.
A path name that exceeds the system maximum will be truncated, see PATH_MAX from
linux/limits.h for the value.

       --append [console_number]

Like --dump, but appends to the snapshot file instead of overwriting it.
Only works if no --dump options are given.

# How to change the keyboard layout in LXDE?

<https://wiki.lxde.org/en/Change_keyboard_layouts>

# How to customize the keyboard layout with Wayland?

- <https://unix.stackexchange.com/questions/212573/how-can-i-make-backspace-act-as-escape-using-setxkbmap>
- <https://unix.stackexchange.com/questions/294286/how-can-i-autoload-xkb-customisations-in-gnome>
- <https://unix.stackexchange.com/questions/292868/how-to-customise-keyboard-mappings-with-wayland>
- <https://realh.co.uk/wp/linux-keymap-hacking/>

##
##
##
##
# xmodmap
## How to install it?

There's no need to.

It's included in the `x11-xserver-utils` which is installed by default.

## How to read the currently used keymap?   And the modifier map?

               ┌ Print Keyboard Expressions (feedable to `xmodmap`)?
               │
    $ xmodmap -pke
    $ xmodmap -pm
               │
               └ Print Modifier map?

## Where is the currently used keymap?

All the keymaps are in:

    /usr/share/X11/xkb/symbols/

Each file in  this directory contains several keymap, all  dedicated to the same
language.

For example, the keymap for French are in:

    /usr/share/X11/xkb/symbols/fr

## Can I quickly switch from a keymap to another?   How?

Yes.

On xubuntu, run:

    $ xfce4-keyboard-settings

## Can I edit a keymap simply by editing a file?

No.

The keymaps are compiled, for the X server to get a quicker access.
The compiled files are stored in the files matching this pattern:

    /var/lib/xkb/*.xkm

So, after editing a keymap, you'll also need to remove existing compiled keymaps:

    rm /var/lib/xkb/*.xkm

Then, restart the X server, so that it compiles and use your new keymap.

Note that this  method is brittle, because your keymap  will probably be removed
after an OS update which upgrades the X server.

## How to use `xmodmap` to make the capslock key generate a `Control_L` keysym?

    xmodmap -e 'keycode 66 = Control_L'
    xmodmap -e 'clear lock'
    xmodmap -e 'add control = Control_L'

    xcape   -e 'Control_L=Escape'

Il n'y  a plus de  keycode générant le keysym  `Caps_Lock`, mais on  s'en fiche.
`Caps_Lock` est inutile.

Ceci dit, on pourrait le restaurer comme ceci:

    xmodmap -e 'keycode 2XX = Caps_Lock'

Ça nous  permettrait de l'utiliser comme  modificateur intermédiaire/jetable, de
la même façon qu'on peut utiliser `Hyper_L` pour que Enter génère `Return`.

## How to use `setxkbmap` to make the capslock key generate a `Control_L` keysym?

    /usr/share/X11/xkb/rules/base.lst

Fichier contenant la liste des options qu'on peut passer à `setxkbmap`.
Y chercher le pattern `! option`.


    setxkbmap -option 'caps:ctrl_modifier'

            Remap CapsLock à Control à l'aide de `setxkbmap`.


    xcape -e 'Caps_Lock=Escape'

            Fait générer le keysym `Escape` à la touche `CapsLock`.


                                     NOTE:

            Il semble  que la précédente  commande avec `setxkbmap`  ne remplace
            pas le keysym suffisamment tôt pour que `xcape` s'en aperçoive.

            Autrement, on devrait exécuter:

                    xcape -e 'Control_L=Escape'


            `setxkbmap`  remplace  le  keysym  qq part  après  que  `xcape`  ait
            intercepté notre frappe, tandis que `xmodmap` le remplace avant.

            En effet, avec `xmodmap`, on devrait exécuter:

                    xcape -e 'Control_L=Escape'

## How to make `xmodmap` source `~/file`?

    $ xmodmap ~/file

## How to make `xmodmap` execute `cmd`?

    $ xmodmap -e 'cmd'

## How to make the key whose keycode is `56` generate the keysym whose code point in Unicode is `1234`?

    $ xmodmap -e 'keycode 56 = U1234'
                               ^---^

Illustrate that you can describe a keysym via its code point in Unicode

##
# Console

    man 5 keyboard

- <http://www.xfree86.org/current/XKB-Config.html>
- <http://pascal.tsu.ru/en/xkb/>
- <https://www.charvolant.org/doug/xkb/>

Sources d'information pour apprendre à configurer  le clavier qd on travaille en
console.

# Links

- <https://askubuntu.com/questions/325272/permanent-xmodmap-in-ubuntu-13-04>
- <https://bugs.launchpad.net/ubuntu/+bug/1243642>
- <https://help.ubuntu.com/community/Custom%20keyboard%20layout%20definitions>
- <https://askubuntu.com/q/254424/698276>

Sources d'infos  à lire, un  jour, si notre  solution actuelle (alias  `fxk`) ne
fonctionne plus.
Certaines solutions en bas du 1er lien sont très intéressantes.

J'y ai notamment trouvé un  lien vers un script python `~/bin/python/xkbmapd.py`
qui  est  censé  charger  automatiquement  la conf  de  `xmodmap`  après  chaque
démarrage, mise en veille, hibernation, changement de disposition de clavier ...


- <https://gitlab.com/interception/linux/tools>
- <https://gitlab.com/interception/linux/plugins/caps2esc>

Transforme la touche capslock en escape et modificateur control.

Un des avantages de ce programme par  rapport à `xcape` et `xmodmap` et qu'il ne
dépend pas de Xorg.

Il fonctionne donc en console.

De plus, il a moins de chances d'être désactivé (comme après une déconnexion).


- <http://bepo.fr/wiki/Utilisateur:Kaze/B%C3%A9po-intl#Variante_.C2.AB.C2.A0d.C3.A9veloppeur.C2.A0.C2.BB>
- <https://wayback.archive.org/web/20160322103150/http://bepo.fr/wiki/Utilisateur:Kaze/B%C3%A9po-intl#Variante_.C2.AB.C2.A0d.C3.A9veloppeur.C2.A0.C2.BB>

Ces liens mènent à une page affichant un layout de clavier bépo intéressant.

On peut s'en inspirer pour trouver  des emplacements judicieux pour des symboles
de programmation.


- <https://github.com/tmk/tmk_keyboard>

Lien menant à un projet github développant des firmwares custom pour clavier.

Si un  jour la customization du  clavier devenait trop complexe  ou insuffisante
via les outils traditionnels (xmodmap, xcape, autokey), on pourrait tenter de le
customizer directement au niveau du firmware.


- <http://efod.se/writings/linuxbook/html/caps-lock-to-ctrl.html>
- <http://www.economyofeffort.com/2014/08/11/beyond-ctrl-remap-make-that-caps-lock-key-useful/>

Procédure pour remap CapsLock à Control avec:

   - xmodmap
   - setxkbmap

##
# Utilities
## xmodmap

<https://wiki.archlinux.org/index.php/Xmodmap>

Source d'infos à propos de `xmodmap`.

---

    keycode 42 = k1 k2 k3 k4 k5 k6
                 │  │  │  │  │  │
                 │  │  │  │  │  └ ISO_Level3_Shift + Shift
                 │  │  │  │  └ ISO_Level3_Shift
                 │  │  │  └ Mode_switch + Shift
                 │  │  └ Mode_switch
                 │  └ Shift
                 └ keysym when the key whose keycode is 42 is pressed without any modifier

Syntaxe  basique  pour  configurer  les   keysyms  générés  par  une  touche  en
combinaison avec certains modificateurs, via `xmodmap`.

`Mode_switch` est  le nom d'un modificateur  qui était généré autrefois  `par la
touche physique AltGr`.

De nos jours, `AltGr` génère `ISO_Level3_Shift`.

<https://unix.stackexchange.com/questions/55076/what-is-the-mode-switch-modifier-for/55154#55154>

---

    keycode 42 <modifier1> <modifier2> … = <keysym1> <keysym2> …

Autre syntaxe valide.

<http://askubuntu.com/a/303966>

---

    keycode 47 Shift_L Control_L = m M Return

La touche    m    génèrera    le keysym    m
`shift + m`       "                        M
`control + m`     "                        Return


WARNING:

`C-m`  sera  traduit  en  `Return`  seulement dans  le  terminal,  et  dans  les
applications GUI utilisant la biblio graphique Xt.

Mais il  ne sera pas  traduit dans les applications  en GUI utilisant  une autre
biblio tq Qt ou Gtk.

La solution pour Gtk est d'utiliser un autre outil, `autokey-gtk`.

Mais pour Qt ...

Ceci pose une autre question:
est-ce que toutes les modifications apportées au layout du clavier, et réalisées
à l'aide de `xmodmap` fonctionnent dans les applications en GUI?

Si  la  réponse  est  non,   c'est  une  raison  supplémentaire  d'utiliser  une
description de clavier custom.

---

    xmodmap -e 'remove shift = Shift_R'
    xmodmap -e 'add mod1 = Shift_R'

Change la signification du keysym `Shift_R`, de `shift` à `mod1` (alt).

Il est  nécessaire de supprimer `Shift_R`  de la ligne logique  `shift` avant de
l'ajouter  dans la  ligne  `mod1`,  autrement la  2e  commande provoquerait  une
erreur.

En effet, un même keysym ne peut pas se trouver sur plusieurs lignes logiques.
Ça n'aurait pas de sens.
Un keysym ne peut avoir qu'une seule signification.

---

    xmodmap -e 'keycode 36 = Control_R'
    xmodmap -e 'add control = Control_R'

Crée une nouvelle touche générant `Control_R`.

La 1e demande  à la touche Enter  (identifiée par son keycode 36)  de générer le
keysym `Control_R`.

La 2e  s'assure que la  modifier map est au  courant qu'un nouveau  keycode peut
générer `Control_R`.

Un même  keysym (ex: `Control_R`, `Alt_L`, ...)  peut être généré par  autant de
touches qu'on veut.

La seule  restriction qui s'impose  à eux, est qu'ils  doivent tous être  sur la
même ligne logique de la modifier map.

## xcape

    xcape -e 'Control_L=Escape'

Qd xcape intercepte un `Control_L` seul, il le remplace par `Escape`.

Illustre que `xcape` peut remplacer un keysym par un autre.

Pas d'espaces autour du symbole d'affectation:

    xcape -e '<keysym1> = <keysym2>'    ✘

---

    xcape -e 'Alt_L=Alt_L|Q'

Qd xcape intercepte un `Alt_L` seul, il le remplace par `M-q`.

Illustre que `xcape` peut remplacer un keysym par un chord.

---

    xmodmap -e 'keycode 36 = Control_R'
    xmodmap -e 'add control = Control_R'
    >   xmodmap -e 'keycode 255 = Return'
    xcape -e 'Control_R=Return'

La 3e  commande demande  à ce  qu'une touche inexistante  de keycode  255 génère
`Return`.

Nécessaire pour  que `xcape` puisse  ensuite remplacer un unique  `Control_R` en
`Return`.

À retenir:
`xcape` ne  peut pas  traduire un  keysym k1 en  un autre  k2, si  aucune touche
(keycode) ne génère k2.

Afin  de choisir  un bon  keycode  pour la  touche inexistante,  lire la  keymap
(`xmodmap -pke`) d'origine (non modifiée), et y chercher un keycode inutilisé.

##
# Issues
## `xcape` works only with Xorg, not with Wayland!

Have a look at these utilities:

- <https://gitlab.com/interception/linux/tools>
- <https://gitlab.com/interception/linux/plugins/caps2esc>

They should work with Wayland.
They may be more powerful than `xcape`.
If you learn how to use them, document them in this file.

---

Alternatively, use a display manager which supports Xorg, and enable it by default.
For example, for gdm, you need to uncomment the line:

    #WaylandEnable=false

In `/etc/gdm/custom.conf`.

For more info, see:

<https://wiki.archlinux.org/index.php/GDM#Use_Xorg_backend>

## AltGr + space generates a space, instead of an underscore!

If you use xmodmap:

   > You can  use xmodmap to redefine  existing mappings as long  as those mappings
   > actually exist in your original keyboard layout.
   > In the case described in the question  you cannot extend behavior of any keys to
   > use AltGr.
   > You can only change the AltGr keysyms for keycodes that are already using AltGr.

Source:

<https://unix.stackexchange.com/a/313711/289772>

IOW, in the keyboard layout that you  have chosen in your OS settings, the space
key must already be generating some keysym when pressed with AltGr.
If it doesn't generate anything by default, you can't make it generate anything,
and AltGr will be ignored.

As a workaround, choose this layout:

    French (legacy, alternative)

In xfce, this assumes that you deselect `Use system defaults` (sure?).

##
## `$ localectl list-keymaps` doesn't work!

    Couldn't find any console keymaps.

It comes  from the fact that  the package `console-data` installs  some archives
with the extension `.kmap.gz`, while `localectl(1)` expects `.map.gz`.
This is a debian bug:

<https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=790955>

You could temporarily fix the issue by executing:

    # temporarily fix the extensions
        $ sudo updatedb
        $ locate kmap.gz | vim -
        :sav /tmp/sh.sh
        :%s/^/mv /
        :%s/kmap\.gz$/{kmap.gz,map.gz}/
        :0put ='#!/bin/bash'
        :x
        $ chmod +x /tmp/sh.sh
        $ sudo /tmp/sh.sh

    # the command should now work
        $ localectl list-keymaps

    # restore the extensions
        $ vim /tmp/sh.sh
        :%s/{kmap.gz,map.gz}/{map.gz,kmap.gz}/
        :x
        $ sudo /tmp/sh.sh

## I've executed `$ localectl set-x11-keymap us`, but the console keyboard layout has not been changed!

Restart the OS a second time.

If you  have installed the package  `console-data`, and if you  have renamed the
archives `.kmap.gz` installed by the  latter, using the `.map.gz` extension, the
console layout will be correctly set after the first reboot of the OS.

## `$ localectl <subcommand> <args>` doesn't work!

`localectl(1)`  invokes the  service `systemd-localed`,  so have  a look  at the
journal, to see which issue the latter has encountered:

    $ journalctl --no-hostname --since '5m ago' -u systemd-localed

Alternatively, trace the `localectl` process:

    $ strace -o /tmp/log localectl <subcommand> <args>

##
## I've installed `usrmerge` on Ubuntu 16.04.  Because of a conflict, the `kbd` package has been removed!

Install a newer version of kbd:

- <https://packages.ubuntu.com/bionic/kbd>
- <https://github.com/legionus/kbd>

