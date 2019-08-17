# Configuration
## How to
### choose the font?

    $ sudo dpkg-reconfigure -plow console-setup
                             │
                             └ show all questions (priority low)

`TerminusBold` is a good font, and `16x32` a good size.

Then, for the change to take effect immediately, execute:

    $ setupcon
      │
      └ set up the font and the keyboard of the console

Otherwise, restart the OS.

Source: https://unix.stackexchange.com/a/49823/232487

---

What's this `-plow` option?

It's optional.

It sets the minimal priority of the questions we want to be asked.
Here we choose the priority `low`.
The possible priorities are:

   - low
   - medium
   - high
   - critical

You can find them by typing:

    $ dpkg-reconfigure -p Tab

For most packages, by default, `dpkg-reconfigure` will choose the low priority.

---

Alternative 1:

    $ sudoedit /etc/default/console-setup

---

Alternative 2:

    $ setfont /usr/share/consolefonts/Lat7-TerminusBold32x16.psf.gz

### change the color scheme?

Try this:

    # https://terminal.sexy (google.light)
    printf -- '\e]P%d%X' 0  0x1d1f21
    printf -- '\e]P%d%X' 1  0xcc342b
    printf -- '\e]P%d%X' 2  0x198844
    printf -- '\e]P%d%X' 3  0xfba922
    printf -- '\e]P%d%X' 4  0x3971ed
    printf -- '\e]P%d%X' 5  0xa36ac7
    printf -- '\e]P%d%X' 6  0x3971ed
    printf -- '\e]P%d%X' 7  0xc5c8c6
    printf -- '\e]P%d%X' 8  0x969896
    printf -- '\e]P%d%X' 9  0xcc342b
    printf -- '\e]P%d%X' 10 0x198844
    printf -- '\e]P%d%X' 11 0xfba922
    printf -- '\e]P%d%X' 12 0x3971ed
    printf -- '\e]P%d%X' 13 0xa36ac7
    printf -- '\e]P%d%X' 14 0x3971ed
    printf -- '\e]P%d%X' 15 0xffffff

---

Alternative:

    _SEDCMD='s/.*\*color\([0-9]\{1,\}\).*#\([0-9a-fA-F]\{6\}\).*/\1 \2/p'
    for i in $(sed -n "$_SEDCMD" "${HOME}/.Xresources" | awk '$1 < 16 {printf "\\e]P%X%s", $1, $2}'); do
        echo -en "$i"
    done
    clear

This script relies on the colors used in `~/.Xresources`.

Source:
<https://wiki.archlinux.org/index.php/Color_output_in_console#Virtual_console>

---

See also:

   - <http://user.it.uu.se/~embe8573/cols/www/index.html> (section ’the Linux VTs’)
   - <http://user.it.uu.se/~embe8573/cols/www/COLORS>
   - <http://user.it.uu.se/~embe8573/cols/run>
   - <http://user.it.uu.se/~embe8573/cols/set_cols.sed>
   - <http://user.it.uu.se/~embe8573/cols/color_sets/>
   - <http://user.it.uu.se/~embe8573/scripts/cols>

I didn't manage to make this code work...

---

Note that each program you use may have its own color scheme:
ls, zsh-syntax-highlighting, ...

You may need to also tweak them so that the text they print is readable.

### make the background color white immediately (before a successful login)?

    $ sudo mkdir -p /etc/systemd/system/getty@.service.d

    $ cat <<'EOF' | sudo tee -a /etc/systemd/system/getty@.service.d/white-background.conf
    [Service]
    ExecStartPre=/bin/sh -c '/usr/bin/setterm -background white -foreground black -store >/dev/%I'
    ExecStartPre=/bin/sh -c '/usr/bin/clear >/dev/%I'
    EOF

The `setterm` command was found here:
<https://web.archive.org/web/20180303034251/http://www.tuxradar.com/answers/482>

---

Alternatively,  if your  systemd  version  is recent  enough,  and supports  the
`StandardOutput` option:

    $ sudo mkdir -p /etc/systemd/system/getty@.service.d

    $ sudo cat <<'EOF' > /etc/systemd/system/getty@.service.d/white-background.conf
    [Service]
    StandardOutput=file:/dev/%I
    ExecStartPre=/usr/bin/setterm -background white -foreground black -store
    ExecStartPre=/usr/bin/clear
    EOF

---

About `-background` and `-foreground`:
we could  also use `--`,  but `man  setterm` recommends to  use `-` in  a script
(section `COMPATIBILITY`).

### increase the size of the scrollback buffer?

Use tmux.

Otherwise, I think you would need to recompile the kernel to set some option:
<https://superuser.com/a/281876/913143>

### turn on the Numlock key by default?

    $ sudo mkdir -p /etc/systemd/system/getty@.service.d
    $ cat <<'EOF' | sudo tee -a /etc/systemd/system/getty@.service.d/activate-numlock.conf
    [Service]
    ExecStartPre=/bin/sh -c 'setleds -D +num < /dev/%I'
    EOF

Source: <https://wiki.archlinux.org/index.php/Activating_Numlock_on_Bootup#Extending_getty@.service>

#### How does it work?

Whenever you try to log in from a console, systemd starts a service instantiated
from the template unit:

    /usr/lib/systemd/system/getty@.service

This can be confirmed by looking at the output of:

    $ systemctl status getty@tty1.service
    Loaded: loaded (/lib/systemd/system/getty@.service ...~

This service starts `agetty` to let you login from a virtual console:

    ExecStart=-/sbin/agetty --noclear %I $TERM
               ^^^^^^^^^^^^

To turn  the Numlock  key on,  we extend  the configuration  of the  template by
including the following directive:

    ExecStartPre=/bin/sh -c 'setleds -D +num < /dev/%I'

`ExecStartPre` will execute `/bin/sh -c '...'` before `agetty` is invoked, which
will invoke `setleds`, which will turn the Numlock key on.

#### Why executing `/bin/sh -c` instead of directly `setleds ...`?

Because of the stdin redirection.

From `man systemd.service`:

> redirection using "<", "<<", ">", and  ">>", pipes using "|", running programs
> in  the background  using "&",  and  other elements  of shell  syntax are  not
> supported.

#### Is there an alternative?

Yes,  if  you  use   a  recent  enough  version  of  systemd,   you  can  use  a
`StandardInput` directive:

    [Service]
    StandardInput=file:/dev/%I
    ExecStartPre=/usr/bin/setleds -D +num

For more information about the `StandardInput` option:

   - <https://github.com/systemd/systemd/pull/7198>
   - <https://www.freedesktop.org/software/systemd/man/systemd.exec.html>

#### But why a redirection is necessary in the first place?

Theory: by default `$  setleds` affect the current tty which  is attached to its
stdin.
However, here, the command is executed outside the context of a tty.
So, we need to reconnect the stdin of  `$ setleds` to the tty for which `agetty`
is going to be invoked by the systemd service.

#### What's `%I`?

A specifier which is replaced with  the unescaped instance name (`tty1`, `tty2`,
...) of the instantiated service.

See `man systemd.unit`.

#### What does `-D` do?

`$ setleds` changes the led flag settings of the VC.
`$ setleds -D` does the same thing, but also changes their default values.

#### What does `+num` do?

It sets the NumLock flag.

###
### increase the keyboard repeat rate, and decrease the delay time?

Use `$ kbdrate`:

    $ sudo kbdrate -r 50 -d 150 </dev/tty1
                                │
                                └ only needed if you're under X

<https://unix.stackexchange.com/a/58652/289772>

To run it automatically, include the command in `/etc/rc.local`:

    $ sudo sed -i.bak '/^exit 0/i kbdrate -r 50 -d 150 </dev/tty1' /etc/rc.local

<https://askubuntu.com/a/290100/867754>

TODO: Convert that in a systemd service.
<https://askubuntu.com/a/960333/867754>

##
# Usage
## How to switch to another console?  (2)

Use the `$ chvt` command:

    $ chvt 3

Or press `C-M-Fx` if you're in the graphical environment, or `M-Fx` if you're in a console.
Replace `x` with the number of the console.

##
## How to view
### a pdf?

Use `less`.

This requires  that you  have the `lesspipe`  utility (on  debian-based distros,
it's included in the `less` package).

It also requires that you have exported the environment variables `LESSOPEN` and
`LESSCLOSE`; you can do so by executing, in `~/.zshenv`:

    eval "$(lesspipe)"

### a video?

    $ mpv -vo drm my_video.mkv

`drm` stands for Direct Rendering.
It seems  to be a  method allowing the  graphics driver to  communicate directly
with the kernel rather than with Xorg.

For more info:
<https://unix.stackexchange.com/a/301402/232487>

    $ man mpv /drm

### an image?

    $ sudo aptitude install fbi
    $ sudo adduser user video

    $ fbi my_pic.jpg

#### Why do I have to add my user to the `video` group?

`fbi` needs to write on `/dev/fb0`.
This file is owned by the root user, and the video group.
So, `fbi` needs to be started by the root user (sudo), or by a user in the video
group.

For more information about the framebuffer:

   - <https://en.wikipedia.org/wiki/Framebuffer>
   - <https://unix.stackexchange.com/search?tab=votes&q=framebuffer>

