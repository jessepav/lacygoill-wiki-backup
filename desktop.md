# xinit

    xinit - X Window System initializer

    $ xinit  [  [  client ] options ... ] [ -- [ server ] [ display ] options ... ]

The xinit program is used to start the X Window System server and a first client
program on  systems that are not  using a display  manager such as xdm(1)  or in
environments that use multiple window systems.
When this first client exits, xinit will kill the X server and then terminate.
(NB. In reality, xinit kills X when there's no client anymore; that is, if you start
2 sessions – xfce4 and openbox – and you kill one but not the other, xinit doesn't kill X).

If no specific client program is given  on the command line, xinit will look for
a file in the user's home directory called  .xinitrc to run as a shell script to
start up client programs.
If no such file exists, xinit will use the following as a default:

    $ xterm  -geometry  +1+1  -n  login  -display  :0

If no specific server program is given  on the command line, xinit will look for
a file in the  user's home directory called .xserverrc to run  as a shell script
to start up the server.
If no such file exists, xinit will use the following as a default:

    X  :0

Note that  this assumes that there  is a program  named X in the  current search
path.
The site administrator should, therefore, make a link to the appropriate type of
server  on the  machine, or  create  a shell  script  that runs  xinit with  the
appropriate server.

Note, when using a .xserverrc script be sure to ``exec'' the real X server.
Failing to do this can make the X server slow to start and exit.
For example:

    exec Xdisplaytype

An important point is  that programs which are run by .xinitrc  should be run in
the background if they do not exit  right away, so that they don't prevent other
programs from starting up.
However,  the  last longlived  program  started  (usually  a window  manager  or
terminal emulator)  should be left  in the foreground  so that the  script won't
exit (which indicates that the user is done and that xinit should exit).

An alternate client and/or server may be specified on the command line.
The  desired client  program and  its  arguments should  be given  as the  first
command line arguments to xinit.
To specify a  particular server command line,  append a double dash  (--) to the
xinit command  line (after  any client  and arguments)  followed by  the desired
server command.

Both the client program name and the server program name must begin with a slash
(/) or a period (.).
Otherwise, they are  treated as an arguments to be  appended to their respective
startup lines.
This makes it possible to add  arguments (for example, foreground and background
colors) without having to retype the whole command line.

If an  explicit server name  is not given and  the first argument  following the
double dash (--) is  a colon followed by a digit, xinit will  use that number as
the display number instead of zero.
All remaining arguments are appended to the server command line.

---

Examples

Below are several examples of how command line arguments in xinit are used.

    $ xinit

This will start up  a server named X and run the user's  .xinitrc, if it exists,
or else start an xterm.

    $ xinit -- /usr/bin/Xvnc  :1

This is how one could start a specific type of server on an alternate display.

    $ xinit -geometry =80x65+10+10 -fn 8x13 -j -fg white -bg navy

This will start up a server named X,  and will append the given arguments to the
default xterm command.
It will ignore .xinitrc.

    $ xinit -e widgets -- ./Xorg -l -c

This will use  the command .Xorg -l -c  to start the server and  will append the
arguments -e widgets to the default xterm command.

    $ xinit /usr/ucb/rsh fasthost cpupig -display ws:1 --  :1 -a 2 -t 5

This will start a server named X on display 1 with the arguments -a 2 -t 5.
It will then start  a remote shell on the machine fasthost in  which it will run
the command cpupig, telling it to display back on the local workstation.

Below is  a sample .xinitrc that  starts a clock, several  terminals, and leaves
the window manager running as the ``last'' application.
Assuming that  the window manager  has been  configured properly, the  user then
chooses the ``Exit'' menu item to shut down X.

    xrdb -load $HOME/.Xresources
    xsetroot -solid gray &
    xclock -g 50x50-0+0 -bw 0 &
    xload -g 50x50-50+0 -bw 0 &
    xterm -g 80x24+0+0 &
    xterm -g 80x24+0-0 &
    twm

Sites that  want to create  a common startup  environment could simply  create a
default .xinitrc that references a site-wide startup file:

    #!/bin/sh
    . /etc/X11/xinit/site.xinitrc

Another approach is  to write a script  that starts xinit with  a specific shell
script.
Such scripts are usually  named x11, xstart, or startx and  are a convenient way
to provide a simple interface for novice users:

    #!/bin/sh
    xinit /etc/X11/xinit/site.xinitrc -- /usr/bin/X -br

---

Environment Variables

    DISPLAY

This  variable gets  set to  the name  of the  display to  which clients  should
connect.

    XINITRC

This variable specifies  an init file containing shell commands  to start up the
initial windows.
By default, .xinitrc in the home directory will be used.

---

Files

    .xinitrc

default client script

    xterm

client to run if .xinitrc does not exist

    .xserverrc

default server script

    X

server to run if .xserverrc does not exist

# startx

    startx - initialize an X session

    $ startx  [  [ client ] options ... ] [ -- [ server ] [ display ] options ... ]

The startx script is a front end to xinit(1) that provides a somewhat nicer user
interface for running a single session of the X Window System.
It is often run with no arguments.

Arguments immediately following the startx command are used to start a client in
the same manner as xinit(1).
The special argument '--' marks the end of client arguments and the beginning of
server options.
It  may be  convenient to  specify server  options with  startx to  change on  a
per-session basis the default color depth,  the server's notion of the number of
dots-per-inch  the display  device presents,  or take  advantage of  a different
server  layout,  as  permitted  by  the Xorg(1)  server  and  specified  in  the
xorg.conf(5) configuration.
Some examples of specifying server arguments follow; consult the manual page for
your X server to determine which arguments are legal.

    $ startx -- -depth 16

    $ startx -- -dpi 100

    $ startx -- -layout Multihead

Note  that in  the Debian  system,  what many  people traditionally  put in  the
.xinitrc  file  should  go  in  .xsession  instead;  this  permits  the  same  X
environment to be presented whether startx, xdm, or xinit is used to start the X
session.
All discussion of the .xinitrc file  in the xinit(1) manual page applies equally
well to .xsession.
Keep in mind  that .xinitrc is used  only by xinit(1) and  completely ignored by
xdm(1).

To determine the client to run, startx first looks for a file called .xinitrc in
the user's home directory.
If that is not found, it uses the file xinitrc in the xinit library directory.
If command line client options are given, they override this behavior and revert
to the xinit(1) behavior.
To determine the server to run, startx  first looks for a file called .xserverrc
in the user's home directory.
If that is not found, it uses the file xserverrc in the xinit library directory.
If command line server options are given, they override this behavior and revert
to the xinit(1) behavior.
Users rarely need to provide a .xserverrc file.
See the xinit(1) manual page for more details on the arguments.

The  system-wide xinitrc  and xserverrc  files are  found in  the /etc/X11/xinit
directory.

---

Environment Variables

    DISPLAY

This  variable gets  set to  the name  of the  display to  which clients  should
connect.
Note that this gets set, not read.

    XAUTHORITY

This variable, if not already defined, gets set to $(HOME)/.Xauthority.
This  is  to prevent  the  X  server, if  not  given  the -auth  argument,  from
automatically setting up insecure host-based authentication for the local host.
See  the Xserver(1)  and Xsecurity(7)  manual pages  for more  information on  X
client/server authentication.

---

Files

    $(HOME)/.xinitrc

Client to run.
Typically a shell script which runs many programs in the background.

    $(HOME)/.xserverrc

Server to run.
The default is X.

    /etc/X11/xinit/xinitrc

Client to run if the user has no .xinitrc file.

    /etc/X11/xinit/xserverrc

Server to run if the user has no .xserverrc file.

##
# Todo
## progressively switch to a simpler desktop environment

There would be several benefits:

   - fewer bugs
   - less memory/cpu consumption
   - more responsive applications
   - better latency in the terminal (?)
   - easier to understand how the system works (because fewer processes), making issues easier to fix

### small system base

When downloading a Linux ISO, no need for any DE.
For example, for Ubuntu, download the Server Edition:
<https://releases.ubuntu.com/22.04/ubuntu-22.04-live-server-amd64.iso>

### no display manager (aka login manager)

We don't need one:

- <https://github.com/swaywm/sway/wiki#login-managers>
- <https://wiki.gentoo.org/wiki/X_without_Display_Manager>
- <https://askubuntu.com/questions/882422/how-can-i-disable-all-display-managers>
- <https://askubuntu.com/questions/16371/how-do-i-disable-x-at-boot-time-so-that-the-system-boots-in-text-mode/79682#79682>
- <https://superuser.com/questions/974797/how-to-boot-a-linux-system-without-graphical-server>

---

Which file(s) should we use?

According to  the gentoo wiki,  we can  use `~/.xinitrc` and  `~/.bash_login` to
autostart a window manager depending on the virtual console.

    # ~/.xinitrc
    case $(tty | cut -b9-) in
      1) exec startxfce4      ;;
      2) exec openbox-session ;;
    esac

    # ~/.bash_login
    # Auto startx depending on the virtual console
    if [[ -z "$DISPLAY" && $(id -u) -ge 1000 ]] ; then
        TTY=$(tty)
        [[ "${TTY/tty}" != "$TTY" && "${TTY:8:1}" = "3" ]] &&
            startx 1>~/.log/xsession-errors 2>&1 &
        unset TTY
    fi

What's the difference between the two snippets?
Is there a difference between the tty and the virtual console?
What are the pros and cons of using the `exec(1)` command?

If you use them,  the login shell will immediately be replaced  by an X session,
and when you'll quit the latter, you won't get back to the shell.
Con: IOW, you'll have to log in again.
Pro: This should simplify  the output of `pstree(1)` (and maybe  reduce the risk
of issues, because one less process?).
Update: I made  some tests in  a VM.   I can't see  much of a  difference betwen
`exec(1)` and no `exec(1)`.  If you use `exec(1)`, here's the tree of process as
reported by `$ pstree -lsp $$`:

    systemd
    login
    bash
    startx
    xinit
    openbox
    xfce4-terminal
    bash

If you look at  `$ pstree -lsp $(pidof xinit)`, you'll see  that, in addition to
openbox, xinit also starts the Xorg server.
Also, if  you don't use  `exec(1)`, then  there's an additional  `sh(1)` process
just after xinit:

    systemd
    login
    bash
    startx
    xinit
    sh               <<<
    openbox
    xfce4-terminal
    bash

I think that `exec(1)` replaces `sh(1)` with the window manager.
Without `exec(1)`, `sh(1)` stays there.

---

Then, we should use `/etc/systemd/system/x11.service` to implement the autologin:

    [Unit]
    After=systemd-user-sessions.service

    [Service]
    ExecStart=/sbin/mingetty --autologin toto --noclear tty8 38400

    [Install]
    WantedBy=multi-user.target

Then, run:

    $ systemctl enable x11.service

To continue...

However, I'm concerned about this file `/etc/systemd/system/display-manager.service`.
Read `~/wiki/keyboard/magic_keys.md` and search for `display-manager`.
Also, run this:

    $ vim -q <(rg 'display[-. \n]*manager' ~/wiki) +cwindow

Are there configurations which we performed on lightdm, and that we should adapt
to our whatever  new window manager we  end up using?  Anyway,  adapt your notes
whenever possible.

### window manager

Try to find a window manager working on Wayland.
Possibly sway which has the benefit of being a *tiling* window manager:
<https://github.com/swaywm/sway>

---

Don't use awesome WM.
Its documentation is way too bad for a beginner, and doesn't support Wayland.

### status bar

Find sth equivalent to polybar for Wayland:
<https://github.com/polybar/polybar>

Waybar maybe:
<https://github.com/Alexays/Waybar>
Or Swaybar:
<https://github.com/swaywm/sway/wiki#swaybar-configuration>

### turn on the Numlock key when the session starts

If using sway:
<https://wiki.archlinux.org/title/Sway#Initially_enable_CapsLock/NumLock>

---

If using X11, I think we need to install the numlockx package, then run this:

    $ numlockx on &
               │  │
               │  └ probably useless, because the process quits immediately (once its job is done)
               └ probably useless, because that's the default action, but it's more explicit that way

This requires the numlockx package.

Where to write the command?  In `~/.profile`?

### find a replacement for the most useful programs installed by a full-blown desktop environment

Like a screen locker, an app to access  system settings, a panel bar, ... Have a
look  at the  output  of `top(1)`,  and  see what  seems  interesting in  what's
running.

Assuming you use sway, you'll probably need a replacement for redshift:
<https://github.com/swaywm/sway/wiki#redshift-equivalent>

For an image viewer like `feh(1)`:
<https://github.com/swaywm/sway/wiki#wallpapers>

To take screenshots:
<https://github.com/swaywm/sway/wiki#taking-screenshots>

For a program launcher:
- <https://github.com/swaywm/sway/wiki#program-launchers>
- <https://github.com/Cloudef/bemenu>

For `$ xset r rate ...`:
<https://github.com/swaywm/sway/wiki#keyboard-repeat-delay-and-rate>

##
## learn how to reduce latency, and how to better judge terminal

- <https://anarc.at/blog/2018-05-04-terminal-emulators-2/#latency> (read the first part too)
- <https://lwn.net/Articles/751763/> (read the first part too)
- <https://pavelfatin.com/typing-with-pleasure/>
- <https://pavelfatin.com/typometer/>
- <https://github.com/pavelfatin/typometer/issues/2>

Also, maybe we should disable UltiSnips' autotrigger even in Vim.
It might not increase the latency, but it might increase the jitter.

---

Note that you can use export the  results of typometer as a file, then re-import
it later.

<https://github.com/pavelfatin/typometer/issues/2#issuecomment-232727288>

   > the  option to  open  a file  is  intended only  for  importing of  previously
   > exported results

---

Does switching to Wayland increase input latency?
If so, do we need some configurations to mitigate the issue?

<https://zamundaaa.github.io/wayland/2021/12/14/about-gaming-on-wayland.html>

## test the twm window manager

From `$ apt show twm`:

   > twm is a window manager for the X Window System.
   > It  provides title  bars,  shaped  windows, several  forms  of icon  management,
   > user-defined macro  functions, click-to-type and pointer-driven  keyboard focus,
   > and user-specified key and pointer button bindings.

Log out and log back to choose it.
It's a very lightweight package, so it could be useful when we need to make some
tests on a new machine or in a VM.
BTW, when you do some tests, install xterm in addition to twm:

    $ apt install twm xterm

Now, after running `startx(1)`, you can make Xorg display sth (xterm).
This is all mentioned here: <https://wiki.gentoo.org/wiki/Xorg/Guide#Using_startx>

When you start twm, left-click on the desktop, and maintain the click.
A menu will appear.
Each entry which contains a square icon on its right is the title of a submenu.
You can enter it by moving your mouse over the icon.

##
# How to get the list of
## sessions that can be started (like xfce4, openbox, ...)?

    $ update-alternatives --display x-session-manager

## window managers that can be started (like xfwm4, openbox, ...)?

    $ update-alternatives --display x-window-manager

