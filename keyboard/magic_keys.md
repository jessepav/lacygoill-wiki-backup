# Numlock
## How to turn on the Numlock key in a X session, as soon as lightdm starts?

        $ sudo aptitude install numlockx
        $ echo 'greeter-setup-script=/usr/bin/numlockx on' | sudo tee -a /etc/lightdm/lightdm.conf

Source:

        https://wiki.archlinux.org/index.php/LightDM#NumLock_on_by_default
        https://www.freedesktop.org/wiki/Software/LightDM/CommonConfiguration/
        https://github.com/CanonicalLtd/lightdm/blob/master/data/lightdm.conf

---

If your desktop environment is LXQt:

        $ cat <<'EOF' >>~/.config/lxqt/session.conf

[Keyboard]
numlock=true
EOF

Source:

        https://wiki.archlinux.org/index.php/Activating_Numlock_on_Bootup#LXQt

---

If your display manager is not lightdm, but LXDM:

        $ echo 'numlockx=1' | sudo tee -a /etc/lxdm/lxdm.conf

---

If your window manager is OpenBox:

        $ echo 'numlockx &' >>~/.config/openbox/autostart

##
# X server
## How to make `Ctrl-Alt-BS` terminate the X server?

For a permanent solution:

        $ sudo dpkg-reconfigure keyboard-configuration

It will ask you some questions.
The relevant one is the last one:

>        Use Control+Alt+Backspace to terminate the X server?
>               Yes

After that, you need to restart the OS.

This will add the line:

        XKBOPTIONS="terminate:ctrl_alt_bksp"

inside `/etc/default/keyboard`.

You could also edit the file manually...

---

For the current session only:

        $ setxkbmap -model pc105 -layout fr -variant latin9 -option terminate:ctrl_alt_bksp
                                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

## Who is the parent of the X server?

The display manager:

        $ pstree -s -p $(pidof Xorg)
        systemd(1)───lightdm(996)───Xorg(1011)───{Xorg}(1018)~
                     ^^^^^^^

## How to restart the X server (with a shell command)?

        $ sudo systemctl restart display-manager

##
# Reboot
## Which key should I press to restart the OS from a console?

Ctrl-Alt-Del.

For more info, see:

        $ man systemd
        /SIGINT

## Which shell command is it equivalent to?

        $ systemctl start ctrl-alt-del.target

---

You can find the (disabled) “ctrl-alt-del” target in the output of:

        $ systemctl list-unit-files -t target | grep ctrl

##
# SysRq functions
## What's a sysrq function?

A kernel function you can invoke by pressing some key combination.

## What's its purpose?

Several functions  can be invoked successively  to restore the system  to a safe
state, or to obtain a clean reboot when nothing else works.

## Where can I find more information about the SysRq functions?

        https://fedoraproject.org/wiki/QA/Sysrq
        https://en.wikipedia.org/wiki/Magic_SysRq_key

        https://askubuntu.com/questions/4408/what-should-i-do-when-ubuntu-freezes
        https://askubuntu.com/questions/11002/alt-sysrq-reisub-doesnt-reboot-my-laptop

##
## How to invoke a sysrq function?

Press `M-SysRq`, then a (command) key.

M-SysRq makes you enter a special mode,  in which you can send commands directly
to the Linux kernel.

In this mode, pressing a (command) key invokes a kernel function.
The kernel will respond immediately, unless it's completely locked.

## Which condition must the kernel satisfy for a sysrq function to be invokable?

It must have been compiled with the `CONFIG_MAGIC_SYSRQ` option enabled.

## How to check it satisfies the condition?

        $ grep -i config_magic_sysrq "/boot/config-$(uname -r)"

The output should contain:

        CONFIG_MAGIC_SYSRQ=y

###
## How to check which sysrq functions are allowed to be invoked via a command key
### by the kernel?

        $ grep -i config_magic_sysrq "/boot/config-$(uname -r)"

It should contain:

        CONFIG_MAGIC_SYSRQ_DEFAULT_ENABLE=0x<some_hex_number>

The value of this option is a hex number.
The decimal representation of the latter tell  you which commands can be sent to
the kernel.

Note that even if the kernel has  a function enabled at compile-time, the distro
may still disable it at boot time, using `/etc/sysctl.conf`.

### by the distro?  (2)

        $ sysctl -a -r 'sysrq'
          │       │  ├───────┘
          │       │  └ only consider parameters that match the pattern 'sysrq'
          │       │
          │       └ print all parameters currently available
          │
          └ configure kernel parameters at runtime

        $ cat /proc/sys/kernel/sysrq

###
## Which values can the kernel parameter 'kernel.sysrq' have?

0, 1, or a sum of powers of two (e.g. 2^3 + 2^4 = 24).

---

From `$ man 5 proc`:

       0    Disable sysrq completely

       1    Enable all functions of sysrq

       >1   Bit mask of allowed sysrq functions:

              2  Enable control of console logging level
              4  Enable control of keyboard (SAK, unraw)
              8  Enable debugging dumps of processes etc.
             16  Enable sync command
             32  Enable remount read-only
             64  Enable signaling of processes (term, kill, oom-kill)
            128  Allow reboot/poweroff
            256  Allow nicing of all real-time tasks

If the value is bigger than 1, it's a bitmask.
Its decimal representation is obtained by  adding the decimal code associated to
each allowed sysrq function.
So, for example, the value 176 used in Ubuntu is the result of the sum:

        128 + 32 + 16

It means that by default, Ubuntu allows:

        • reboot/poweroff
        • remount read-only
        • sync command

Why is it called a bitmask?
Because you  can check whether  a given function  is allowed, by  converting its
decimal code into binary, as well as  the bitmask, then perform an AND operation
between the two:

        Mask:   10110000 (176)
        Value:  01000000 (64)
        ---- AND ---------
        Result: 00000000
                 ^
                 ✘

The result tells us that the function associated to 64 is NOT allowed.

        Mask:   10110000 (176)
        Value:  00010000 (32)
        ---- AND ---------
        Result: 00010000
                   ^
                   ✔

The result tells us that the function associated to 32 IS allowed.

Another way of looking at it:
every bit whose value is 1 stands for an allowed function.

## Why is the value of 'kernel.sysrq' lower in Ubuntu compared to Debian?

In Ubuntu, its value is 176.
In Debian, its value is 438.

It's  lower in  Ubuntu, because  the latter  disables the  access to  more SysRq
functions via command keys, for security reasons.

## Where does Ubuntu configure 'kernel.sysrq'?

In `/etc/sysctl.d/10-magic-sysrq.conf`:

        $ grep ^kernel.sysrq /etc/sysctl.d/10-magic-sysrq.conf
        kernel.sysrq = 176~

###
## How to allow all SysRq functions to be invoked by command keys
### during the current session?  (2)

        $ sudo sysctl -w kernel.sysrq=1

Or:

        $ echo 1 | sudo tee /proc/sys/kernel/sysrq

### definitively?

        $ echo 'kernel.sysrq = 1' | sudo tee -a /etc/sysctl.conf

###
## How to invoke a SysRq function even if the distro prevents it from being invoked by a command key?

Write the command key into:

        /proc/sysrq-trigger

Example:

        $ echo <cmd> | sudo tee /proc/sysrq-trigger

## How to read the output of the function?

If you've executed the command from a terminal, execute:

        $ dmesg | less

If you've executed the command from a console, there's no need to.
The output is automatically written in the console.

## How to get some help to know which command key to press to invoke a function?

        $ echo h | sudo tee /proc/sysrq-trigger

        $ dmesg | less

###
## When the system becomes very unresponsive, how to
### reboot the machine?  (2)

Press the following command keys in the same order they're written:

        ┌───────────┬──────────────────────────────────────────────────────────┐
        │ M-SysRq-r │ switch the keyboard from raw to XLATE mode               │
        ├───────────┼──────────────────────────────────────────────────────────┤
        │ M-SysRq-e │ send a SIGTERM signal to all processes                   │
        ├───────────┼──────────────────────────────────────────────────────────┤
        │ M-SysRq-i │ send a SIGKILL signal to all processes                   │
        ├───────────┼──────────────────────────────────────────────────────────┤
        │ M-SysRq-s │ sync all mounted filesystems                             │
        │           │ and flush all changes from cache to the disk immediately │
        ├───────────┼──────────────────────────────────────────────────────────┤
        │ M-SysRq-u │ remount all filesystems in read only mode                │
        ├───────────┼──────────────────────────────────────────────────────────┤
        │ M-SysRq-b │ reboot                                                   │
        └───────────┴──────────────────────────────────────────────────────────┘

Mnemonic:

Reboot Even If System Utterly Broken.

---

Alternatively, from a console, press M-C-Del more than 7 times in 2s.

For more information, see:

        $ man systemd
        /SIGINT

> SIGINT
>
> Upon  receiving  this   signal  the  systemd  system  manager   will  start  the
> ctrl-alt-del.target unit.
> This is mostly equivalent to systemctl start ctl-alt-del.target.
> If this  signal is received  more than  7 times per  2s, an immediate  reboot is
> triggered.
> Note that pressing Ctrl-Alt-Del on the console will trigger this signal.
> Hence, if a reboot is hanging, pressing  Ctrl-Alt-Del more than 7 times in 2s is
> a relatively safe way to trigger an immediate reboot.
>
> systemd user managers treat this signal the same way as SIGTERM.

See also:

        https://askubuntu.com/questions/763887/how-do-we-disable-ctrl-alt-del-on-ubuntu-16-04

### shut down the machine?

Press:

        M-SysRq-reisuo
                     ^
                     poweroff

##
## What does pressing and releasing `M-SysRq` do?

If you're in  a virtual console, it  cycles between the current  console and the
previous one.

##
# Issues
## I've pressed `M-SysRq` while the OS was shutting down.  I can't see the kernel messages anymore!

Press and release `M-SysRq` again.

When the OS is shutting down, pressing and releasing M-SysRq makes you alternate
between two buffers.

One used to print the different steps performed  to shut down the OS, as well as
the effect of the SysRq functions if they are invoked.
The other is used by a console (1? 7?).

## I've pressed `M-SysRq-e` to terminate all processes.  I'm back to the desktop!

This is due  to the `display-manager` service, which  automatically restarts the
display manager.

According to the [archwiki](https://wiki.archlinux.org/index.php/Keyboard_shortcuts#Kernel), it should not prevent the “reisub” sequence from working:

> If you  are using a  display manager and  after Alt+SysRq+e you  are presented
> with the login  screen (or full desktop  if autologin is enabled),  it is most
> likely caused by Restart=always directive in the relevant service file.
> If  necessary, edit  the  unit, however  this should  not  prevent the  "REISUB"
> sequence from working.

Nevertheless,  if   you  wish  to   prevent  the  display  manager   from  being
automatically restarted, you need to comment out the directive:

        Restart=always

in the service file:

        /etc/systemd/system/display-manager.service

## I've pressed `M-SysRq-m` to output current memory information to the console.  It doesn't work!

When you press `M-SysRq`, the keyboard layout temporarily switches to QWERTY.
And with  a QWERTY  layout, the `m`  keysym is  produced by the  `,` key  (on an
AZERTY keyboard).

So, press `M-SysRq-,`.
                   ^

For more info, see:

        https://en.wikipedia.org/wiki/Magic_SysRq_key#Commands

## I've pressed `M-SysRq-<command key>`.  It doesn't work!

Try again, but this time replace the Alt key with the AltGr key.

Otherwise, the keyboard is probably the issue:

        • On laptops, the `Fn` key may need to be pressed to use the magic `SysRq` key.

        • Some keyboards have  `SysRq` on another key than `PrtSc`,  which must
          be pressed with a function key. For example, it could be `Fn+End`.

        • Some keyboards  don't like 4  keys to be pressed  at the same  time,
          and stop being a keyboard until you release some.

For more info, see:

        https://askubuntu.com/a/240691/867754

