
We should progressively switch to a simpler DE.
There would be several benefits:

   - fewer bugs
   - less memory/cpu consumption
   - more responsive applications
   - better latency in the terminal (?)
   - easier to fix bugs; easier to understand how the OS/shell/systemd/... works (because fewer processes)

# How to get the list of
## sessions that can be started (like xfce4, openbox, ...)?

    $ update-alternatives --display x-session-manager

## window managers that can be started (like xfwm4, openbox, ...)?

    $ update-alternatives --display x-window-manager

##
# ?

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

# ?

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
# ?

First, you need to get rid of lightdm.
It's not that lightweight.

Ok, but replace it with what?
Nothing.  We don't need a display manager.

Read this:
<https://wiki.gentoo.org/wiki/X_without_Display_Manager>

We should be able to:

   - start our custom DE from a console
   - autologin
   - “attach” different DEs to different consoles
     (e.g. `exec startx` from console1 → custom DE;
     from console2 → lxde;
     from console3 → xfce)

To begin with, we should learn how to disable lightdm.
It may  not be useful later,  if we re-install a  linux distro with a  custom DE
right from  the start; but  who knows, it  may still be  useful if we  install a
common DE as a fallback in case of an issue.
And anyway, right now, we definitely need to disable lightdm before building our DE.

See:
- <https://askubuntu.com/questions/882422/how-can-i-disable-all-display-managers>
- <https://askubuntu.com/questions/16371/how-do-i-disable-x-at-boot-time-so-that-the-system-boots-in-text-mode/79682#79682>
- <https://superuser.com/questions/974797/how-to-boot-a-linux-system-without-graphical-server>

---

Which file(s) should we use?

According  to the  gentoo  wiki,  we can  use  `~/.xinitrc`  and `~/.zlogin`  to
autostart a WM depending on the VC.

        # ~/.xinitrc
        case $(tty | cut -b9-) in
          1) exec startxfce4      ;;
          2) exec openbox-session ;;
        esac

       # ~/.bash_login
       # Auto startx depending on the VC
       if [[ -z "$DISPLAY" && $(id -u) -ge 1000 ]] ; then
           TTY=$(tty)
           [[ "${TTY/tty}" != "$TTY" && "${TTY:8:1}" = "3" ]] &&
               startx 1>~/.log/xsession-errors 2>&1 &
           unset TTY
       fi

       # ~/.zlogin
       # Auto startx depending on the tty
       if [[ -z $DISPLAY ]] && (( $EUID != 0 )) {
           [[ ${TTY/tty} != $TTY ]] && (( ${TTY:8:1} <= 3 )) &&
               startx 1>~/.log/xsession-errors 2>&1 &
       }

What's the difference between the two snippets?
Is there a difference between the tty and the VC?
Why is there no `fi` in the zsh snippet? Where is this syntax documented?

In the previous snippets, what are the pros and cons of using the `exec` command?

If you use it, the login shell will immediately be replaced by an X session, and
when you'll quit the latter, you won't get back to the shell.
Con: IOW, you'll have to log in again.
Pro: This should simplify  the output of `pstree(1)` (and maybe  reduce the risk
of issues, because one less process?).
Update: I made some tests in a VM.  I can't much of a difference betwen `exec` and no `exec`.
If you use `exec`, here's the tree of process as reported by `$ pstree -lsp $$`:

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
Also, if you  don't use `exec`, then there's an  additional `sh(1)` process just
after xinit:

    systemd
    login
    bash
    startx
    xinit
    sh               <<<
    openbox
    xfce4-terminal
    bash

I think that `exec` replaces `sh(1)` with the window manager.
Without `exec`, `sh(1)` stays there.


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

    $ vim -q <(rg 'display[-. \n]*manager' ~/wiki) +cw

Are there configurations which we performed on lightdm, and that we should adapt
to openbox?
Anyway, adapt your notes whenever possible.

---

If you want a different wallpaper per desktop, see this:
<https://forums.bunsenlabs.org/viewtopic.php?id=657>

I'm not sure this is a good idea though.
Openbox doesn't seem to support this by default, so you have to hack a script.
And the latter may have memory leaks... Besides, it adds useless complexity.
Maybe we should  just settle on a  simpler script which would let  us change the
wallpaper on-demand +  an indicator in conky  or in a panel about  the number of
the current desktop.

# ?

According to this:
<https://wiki.gentoo.org/wiki/Openbox/Guide>

   > If problems are  experienced with automounting, or if dbus  and ConsoleKit are
   > being used, exec ck-launch-session dbus-launch --sh-syntax --exit-with-session
   > openbox-session should be  placed in each user's .xinitrc file  instead of the
   > simple exec openbox-session command mentioned above.

But according to this:
<http://blog.falconindy.com/articles/back-to-basics-with-x-and-systemd.html>

   > There's no “ck-session-launch” equivalent, sure, but it isn't needed.

And then the page proceeds to explain a shell script.

What should we do?

# ?

Next, we need  to find a replacement for  every basic component of a  DE, like a
screen locker, an app to access system settings, a panel bar, ...
Have a look at the output of  `top(1)`, and see what seems interesting in what's
running.

# ?

Finally, we need to find a better window manager (WM).
Right now, we use xfwm4 (which is the default for xfce4).
But this is a *compositing* window manager; that kind of WM increases the latency.
We should prefer a *stacking* WM.

Note that stacking vs compositing has nothing to do with floating vs tiling.
Those are orthogonal concepts.

My ideal WM would be the awesome  WM; it's powerful, supports compositing but is
probably stacking by default, and is scriptable with lua.
Check this for a start:
<https://awesomewm.org/apidoc/documentation/07-my-first-awesome.md.html#>
There are other interesting pages in the left sidebar.

But awesome would probably be a timesink right now.
There's an easier WM: **openbox**.
So, for the time being, try to install and configure openbox.

Read: <http://openbox.org/wiki/Help:Getting_started>

- <http://openbox.org/wiki/Help:Autostart>
- <http://openbox.org/wiki/Help:Openbox-session>
- <http://openbox.org/wiki/Help:Contents#Cool_programs_to_run_with_Openbox>

- <http://openbox.org/wiki/Help:Themes>
- <https://www.opendesktop.org/browse/cat/140/ord/top/>
- <https://www.deviantart.com/customization/skins/linuxutil/winmanagers/openbox/newest/>

Also, have a look at the output of `$ aptitude show openbox`:

    Recommends: obconf, python-xdg | obsession, scrot
    Suggests: menu, fonts-dejavu, python, libxml2-dev, tint2, openbox-menu, openbox-gnome-session (= 3.6.1-1ubuntu2.1), openbox-kde-session (= 3.6.1-1ubuntu2.1)

Maybe you should install some packages to enhance the environment.
Btw, what's this bar:

    Recommends: obconf, python-xdg | obsession, scrot
                                   ^
                                   ?

# ?

We should also learn how to reduce latency, and how to better judge a terminal.

- <https://anarc.at/blog/2018-05-04-terminal-emulators-2/#latency> (read the first part too)
- <https://lwn.net/Articles/751763/> (read the first part too)
- <https://pavelfatin.com/typing-with-pleasure/>
- <https://pavelfatin.com/typometer/>
- <https://github.com/pavelfatin/typometer/issues/2>

We recently have switched from urxvt to st.
I think it was a wise decision for different reasons.
In particular, it has divided the latency by two.
We could gain a few more ms by switching to openbox.
But maybe we could also improve the latency by tweaking `config.h`:

    static unsigned int xfps = 250;
    static unsigned int actionfps = 90;

Try those values, and test the compiled st with typometer.
Does it reduce the latency?
Increase/Reduce them as you see fit.

Try also this:

    static unsigned int dodraw = 1;

Source: <https://lwn.net/Articles/751763/>

Does it help?

Also, maybe we should disable UltiSnips' autotrigger even in Vim.
It may not increase the latency, but it may increase the jitter.

# ?

Test this WM:

   > twm is a window manager for the X Window System.
   > It  provides title  bars,  shaped  windows, several  forms  of icon  management,
   > user-defined macro  functions, click-to-type and pointer-driven  keyboard focus,
   > and user-specified key and pointer button bindings.

Log out and log back to choose it.
It's a very lightweight package, so it could be useful when we need to make some
tests on a new machine or in a VM.
Btw, when you do some tests, install xterm in addition to twm:

    $ aptitude install twm xterm

Now, after running `startx(1)`, you can make Xorg display sth (xterm).
This is all mentioned here: <https://wiki.gentoo.org/wiki/Xorg/Guide#Using_startx>

When you start twm, left-click on the desktop, and maintain the click.
A menu will appear.
Each entry which contains a square icon on its right is the title of a submenu.
You can enter it by moving your mouse over the icon.

# ?

Note that you can use export the  results of typometer as a file, then re-import
it later.

<https://github.com/pavelfatin/typometer/issues/2#issuecomment-232727288>

   > the  option to  open  a file  is  intended only  for  importing of  previously
   > exported results

# ?

To turn on the Numlock key in a X session, as soon as openbox starts, run:

    $ echo 'numlockx on &' >>~/.config/openbox/autostart
                     │  │
                     │  └ probably useless, because the process quits immediately (once its job is done)
                     └ probably useless, because that's the default action, but it's more explicit that way

This requires the numlockx package.

Also, read `~/bin/restore-env` and search for ‘lightdm’ and ‘numlockx’.
There are some commands which we should probably run for openbox.

# ?

I've always wondered why I had locale environment variables with french values:

    $ env | grep LC | grep FR
    LC_ADDRESS=fr_FR.UTF-8
    LC_IDENTIFICATION=fr_FR.UTF-8
    LC_MEASUREMENT=fr_FR.UTF-8
    LC_MONETARY=fr_FR.UTF-8
    LC_NAME=fr_FR.UTF-8
    LC_NUMERIC=fr_FR.UTF-8
    LC_PAPER=fr_FR.UTF-8
    LC_TELEPHONE=fr_FR.UTF-8

Once you've switched to openbox, try to understand.
Use `$ pstree -lsp $$`, and watch `/proc/PID/environ` as well as `/proc/PID/cmdline`.

Update: They seem to be inherited from the upstart process:

    systemd(1)---lightdm(1070)---lightdm(1246)---upstart(1255)---xterm(6169)---zsh(6170)-+-pstree(7772)
                                                 ^-----------^

It's the oldest process which has these variables in its environment:

    $ tr '\0' '\n' </proc/1255/environ | grep FR
    LC_PAPER=fr_FR.UTF-8~
    LC_ADDRESS=fr_FR.UTF-8~
    LC_MONETARY=fr_FR.UTF-8~
    LC_NUMERIC=fr_FR.UTF-8~
    LC_TELEPHONE=fr_FR.UTF-8~
    LC_IDENTIFICATION=fr_FR.UTF-8~
    LC_MEASUREMENT=fr_FR.UTF-8~
    LC_TIME=fr_FR.UTF-8~
    LC_NAME=fr_FR.UTF-8~

I suspect upstart gets these from this config file:

    /etc/default/locale

Which can be set with the update-locale program:

    $ update-locale LANG=en_US.UTF-8

This last command should remove these  variables from the environment of all our
processes.  But do we  really want that?  Maybe it would be  better to keep some
of them; and/or some of them should be set with US values.

