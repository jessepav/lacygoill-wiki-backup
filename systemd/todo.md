# Review which subcommands of `systemctl` are interesting.

    $ systemctl --help

# review all our systemd services

    # to get list of running services
    $ systemctl --type=service
    $ journalctl --unit <name>.service

    $ systemctl --user --type=service
    $ journalctl --user-unit <name; e.g. pulseaudio>.service
                                                    ^------^
                                                    necessary?

# find a way to version control our customizations of unit files

For example, the files in:

    /etc/systemd/system/getty@.service.d/

# study tool to convert crontab into equivalent .timer and .service units

<https://github.com/systemd-cron/systemd-cron>

# study difference between `Wants`, `Requires`, `PartOf`, `BindsTo`

To help you make tests, use this user `a.service`:

    [Unit]
    Description=Test service A

    [Service]
    Type=simple
    ExecStart=sh -c 'while true; do echo A is alive; sleep 30; done'

And this user `b.service`:

    [Unit]
    Description=Test service B.
          Wants=a.service
    #     Requires=a.service
    #     BindsTo=a.service
    #     PartOf=a.service

    [Service]
    Type=simple
    ExecStart=sh -c 'while true; do echo B is alive; sleep 30; done'

And this shell script:

    #!/bin/bash

    # https://pychao.com/2021/02/24/difference-between-partof-and-bindsto-in-a-systemd-unit/
    # https://systemd-devel.freedesktop.narkive.com/HjzF89ab/why-do-passive-target-units-have-to-exist

    #     # 1
    #     systemctl --user stop {a,b}.service
    #     systemctl --user start a.service
    #     systemctl --user status --no-pager b.service
    #     # when a is started, b is not started
    #     # when a is started, b is not started
    #     # when a is started, b is not started
    #     # when a is started, b is not started

            #     # 2
            #     systemctl --user stop {a,b}.service
            #     systemctl --user start b.service
            #     systemctl --user status --no-pager a.service
            #     # when b is started, a is started
            #     # when b is started, a is started
            #     # when b is started, a is started
            #     # when b is started, a is not started

            #     # 3
            #     systemctl --user start {a,b}.service
            #     systemctl --user stop a.service
            #     systemctl --user status --no-pager b.service
            #     # when a is stopped, b is not stopped
            #     # when a is stopped, b is stopped
            #     # when a is stopped, b is stopped
            #     # when a is stopped, b is stopped

    #     # 4
    #     systemctl --user start {a,b}.service
    #     systemctl --user stop b.service
    #     systemctl --user status --no-pager a.service
    #     # when b is stopped, a is not stopped
    #     # when b is stopped, a is not stopped
    #     # when b is stopped, a is not stopped
    #     # when b is stopped, a is not stopped

            #     # 5
            #     systemctl --user start {a,b}.service
            #     kill -9 $(systemctl --user show --property=ExecMainPID a.service | sed 's/.*=//')
            #     systemctl --user status --no-pager b.service
            #     # when a is stopped abnormally, b is not stopped
            #     # when a is stopped abnormally, b is not stopped
            #     # when a is stopped abnormally, b is stopped
            #     # when a is stopped abnormally, b is not stopped

    #     # 6
    #     systemctl --user start {a,b}.service
    #     kill -9 $(systemctl --user show --property=ExecMainPID b.service | sed 's/.*=//')
    #     systemctl --user status --no-pager a.service
    #     # when b is stopped abnormally, a is not stopped
    #     # when b is stopped abnormally, a is not stopped
    #     # when b is stopped abnormally, a is not stopped
    #     # when b is stopped abnormally, a is not stopped

            #     # 7
            #     systemctl --user start {a,b}.service
            #     sleep 3; systemctl --user restart a.service
            #     systemctl --user status --no-pager {a,b}.service
            #     # when a is restarted, b is not restarted
            #     # when a is restarted, b is restarted
            #     # when a is restarted, b is restarted
            #     # when a is restarted, b is restarted

    #     # 8
    #     systemctl --user start {a,b}.service
    #     sleep 3; systemctl --user restart b.service
    #     systemctl --user status --no-pager {a,b}.service
    #     # when b is restarted, a is not restarted
    #     # when b is restarted, a is not restarted
    #     # when b is restarted, a is not restarted
    #     # when b is restarted, a is not restarted

# study `man systemd-nspawn`

    systemd-nspawn - Spawn a command or OS in a light-weight container
    [...]
    systemd-nspawn may be used to run a command or OS in a light-weight
    namespace container. In many ways it is similar to chroot(1), but more
    powerful since it fully virtualizes the file system hierarchy, as well
    as the process tree, the various IPC subsystems and the host and domain
    name.

Check out the `EXAMPLES` section of the man page.
Also, find some guides.  At the moment, the first page of google gives these:

- <https://wiki.debian.org/nspawn>
- <https://medium.com/@huljar/setting-up-containers-with-systemd-nspawn-b719cff0fb8d>
- <https://clinta.github.io/getting-started-with-systemd-nspawnd/>
- <https://blog.selectel.com/systemd-containers-introduction-systemd-nspawn/>

Update: Is it worth learning this?  It doesn't seem very popular.
Shouldn't we focus on docker/podman instead?

# understand "No protocol specified" error

At some point, we had this error:

    $ sudo systemctl edit --full display-manager.service
    # quit editor
    No protocol specified

We fixed the error like this:

    $ su - $USER -c "unset XAUTHORITY; xauth add $(xauth list)"

Found here:
<https://unix.stackexchange.com/a/209750>

What did our command do exactly?
What was the cause of the issue?
Why can't we reproduce it anymore?

Update: Now that I've reboot the machine, I can reproduce again.
Although, the message has changed:

    Invalid MIT-MAGIC-COOKIE-1 key

And this time the previous command no longer helps.

Update: I've logged out and logged back in.  No issue anymore.

# ?

Here are a few interesting links/commands:

    # Why do I need `--user-unit`? https://unix.stackexchange.com/a/439616/289772
    $ journalctl --user-unit sxhkd

To understand issue “Start request repeated too quickly”:
<https://serverfault.com/a/845473>

<https://askubuntu.com/a/859583/867754>

<https://wiki.archlinux.org/index.php/Systemd/User>

# ?

Explains what happens when we enable a service.

Old comment:

    How to install this service?

        $ systemctl --user enable transmission-daemon.service

        Created symlink
        /home/lgc/.config/systemd/user/graphical.target.wants/transmission-daemon.service
        →
        /home/lgc/.config/systemd/user/transmission-daemon.service

    When the command is run for the first time, a symbolic link is
    created in the `graphical.target.wants/` directory (because of the
    `WantedBy=graphical.target` directive in this file).
    This has the effect that a dependency of type `Wants=` or `Requires=` is added
    from the `graphical.target` unit to the `transmission-daemon` unit.
    The primary result is that the `transmission-daemon` unit will be started when
    the `graphical.target` unit is started.

    For more info, see `man systemd.unit /[UNIT] SECTION OPTIONS/;/^\s*Wants=$`.

# ?

Document the `Type=` directive.

By  default, the  service manager  assumes  `Type=simple`, which  means that  it
proceeds starting follow-up units right  after the `fork()` system call returns.
With `Type=exec`, it waits until `fork()` *and* `execve()` return.

Remember that in Linux, a process creates a child with 2 system calls:

   - it `fork()`s a new process
   - it `execve()` the script/binary to replace the program currently run
     in this new process

##
# Documentation to read/watch
## videos

- <https://www.youtube.com/watch?v=S9YmaNuvw5U>
- <https://www.youtube.com/watch?v=tY9GYsoxeLg>
- <https://www.youtube.com/watch?v=V0xoCA_qO58>

## texts

- <https://systemd-by-example.com/>
- <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/chap-managing_services_with_systemd>
- <https://www.freedesktop.org/wiki/Software/systemd/>
- <https://wiki.archlinux.org/index.php/Systemd>
- <https://wiki.archlinux.org/index.php/Systemd/User>
- <https://wiki.archlinux.org/index.php/Systemd_FAQ>
- <https://wiki.archlinux.org/index.php/Systemd/Timers>

---

systemd units and unit files:
<https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files>

systemd socket units:
<https://www.linux.com/training-tutorials/end-road-systemds-socket-units/>

The difference between `ListenStream=` and `ListenDatagram`:
<https://unix.stackexchange.com/questions/517240/systemd-socket-listendatagram-vs-listenstream>

Monitoring paths and directories:
<https://www.linux.com/topic/desktop/systemd-services-monitoring-files-and-directories/>

How to manage systemd services:
<https://www.howtogeek.com/216454/how-to-manage-systemd-services-on-a-linux-system/>

How to create systemd service files:
<https://linuxconfig.org/how-to-create-systemd-service-unit-in-linux>

Securing and sandboxing applications and services:
<https://www.redhat.com/sysadmin/mastering-systemd>

Managing containers in podman with systemd unit files:
<https://www.youtube.com/watch?v=AGkM2jGT61Y>

##
# Documentation to write
## how to find overridden configuration files

    $ man systemd-delta

## how to redirect the output of a service into a file

Use the `StandardOutput` directive:
<https://stackoverflow.com/a/43830129/9780968>

Otherwise, you might use a hack (`/bin/sh -c 'cmd >redir'`):
<https://stackoverflow.com/a/37595720/9780968>

## how to create a su(1)-like privileged session

I.e. a session which is fully isolated from the original session:

    $ sudo machinectl shell

Source:

- <https://github.com/systemd/systemd/pull/1022>
- <https://github.com/systemd/systemd/issues/825#issuecomment-127957710>
- <https://github.com/systemd/systemd/issues/825#issuecomment-127917622>

You might need to install the `systemd-container` package.

## purpose of tor daemon which may be running on the machine

    tor --defaults-torrc /usr/share/tor/tor-service-defaults-torrc -f /etc/tor/torrc --RunAsDaemon 0

It can help  to torify a shell command  such as `$ pip install`,  when a package
can't be installed because of a network issue (e.g. AS blacklisted).

    $ . torsocks on
    $ python3 -m pip install --user requests

<https://tor.stackexchange.com/questions/12588/debian-tor-user-running-tor-in-the-background-from-startup#comment13069_12588>

If it's not running, you need to start the service manually:

    $ . torsocks on
    $ sudo systemctl start tor.service
    $ python3 -m pip install --user requests

torsocks - Access The Tor Network - Linux CLI: <https://www.youtube.com/watch?v=0uXFffq-UPU>

## how to dynamically get the current username from a unit file

Try the `%u` specifier documented at `man systemd.unit /SPECIFIERS/;/%u`.
And for the home, try `%h`.

Alternatively, try `$USER` and `$HOME`.

##
# High priority
## turn `~/.config/keyboard/setup` into a systemd service

To run this:

    $ xset r rate 175 40

Make sure the service is automatically started after the one which runs `keyd(1)`.

Also, if you install other units related to the keyboard, consider grouping them
under a custom target (`keyboard.target`), if that makes sense...

## do sth similar for `~/bin/autostartrc`

## document how maybe we should always use `--no-block` to start a service from a script

To not block the script.

Unless the rest of the script needs the guarantee that the service has been full
started.

##
## turn our `UpdateConfig` Vim autocmds into systemd services

There is a todo item in our vimrc; look for the `inotifywait` pattern.
We've started to work on this feature in the past; check out these files:

   - `~/bin/reload-config`
   - `~/.config/systemd/user/reload-config.service`

## install a timer to check validity of the wiki files we encrypt in our vimrc

There is a todo item in our vimrc for this; look for the `EncryptFiles()` function.

The timer  should check that  the encrypted archive  is not corrupted,  and that
it's in  sync with our  current files.  To  do so, it  will need to  decrypt the
archive and diff its contents against the current non-encrypted files.
There should be no difference.

If the timer finds  a difference, it should warn us (probably  via a local mail,
because a simple desktop notification is easy to miss).

Make it run once a week.

## install command(s) to measure system startup time

<https://serverfault.com/a/617864>

    $ systemd-analyze critical-chain

    $ systemd-analyze plot > plot.svg
    $ display plot.svg

    $ systemd-analyze dot 'avahi-daemon.*' | dot -Tsvg > avahi.svg
    $ display avahi.svg

## install a service to automatically sanitize filenames under `~/Downloads/`

A downloaded file might contain weird characters:

   - `|`
   - `[`
   - `]`
   - `(`
   - `)`
   - `,`
   ...

Those characters  can make  a path hard  to read, and  even break  some programs
(e.g.  fasd  won't  log a  filename  in  its  db  if the  latter  contains  such
characters).

Use a service starting a file watcher which automatically renames such files.
Make it  replace weird characters  with underscores.  Then, make  it consolidate
multiple consecutive underscores into a single one.

Only accept these characters:

    [-_a-zA-Z0-9./]

Use `mv --no-clobber` to rename the files.

Pitfall: This could break torrents while the files are being downloaded.
To avoid  this issue, create  `~/Download/torrents/`, and make sure  your script
ignores files underneath.

##
# Low priority
## output of `systemctl(1)` is sometimes hard to read

Because  some of  its lines  can be  highlighted with  color 185  (some kind  of
yellow), which is hard to read on a light background.

Short-term solution:

    # disable colorized output
    export SYSTEMD_COLORS=0

Long-term solution:

    # limit palette to the first 16 ANSI colors
    # requires recent systemd version with this commit:
    # https://github.com/systemd/systemd/commit/e4dde4e87d8dafda44f207a3f7c56fd679c11c7d
    export SYSTEMD_COLORS=16

## write a systemd service to start/stop an aria2c daemon

Start from this shell script:
<https://github.com/baskerville/diana/blob/master/dad>

Once you have an `aria2c(1)` daemon, you will  be able to get a TUI frontend for
all of your downloads started with the `aria2c(1)` command.
For that, you'll need to install `aria2p`:

    $ python3 -m pip install --user --upgrade aria2p[tui]
                                                    ^   ^
                                                    those are literal bracket characters to type

For more info, watch this video:
<https://www.youtube.com/watch?v=bc5thl-Dngs>

## sometimes, when we shut down the system, it takes a long time (forever?)

Update: we no longer have this issue.   However, we keep this section because it
might contain valuable information.

---

Read:

   - `/usr/share/doc/systemd/README.Debian.gz`
     (press `za` to get custom folding; read section "Debugging boot/shutdown problems")
   - <https://bugs.launchpad.net/ubuntu/+source/systemd/+bug/1464917>
   - <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=788303>
   - <https://freedesktop.org/wiki/Software/systemd/Debugging/>

---

Try to enable a debug shell before shutting down the system:

    $ sudo systemctl start debug-shell

Then, when the shutdown hangs, press Ctrl+Alt+F9.

You should get a debug shell.
In it, run this to see the hanging jobs:

    $ systemctl list-jobs

If you see any hanging job/error, run `dmesg(1)`.
Run also `$ journalctl -xe`.

You  could  also  try  to include  `debug`  in  `GRUB_CMDLINE_LINUX_DEFAULT`  in
`/etc/default/grub`, to increase the verbosity of the messages.

---

Try to shut down the system by running `$ systemctl poweroff` (don't use `shutdown(8)`).
Or if you need to reboot: `$ systemctl reboot`.

---

Try to disable all swap partitions: `$ sudo swapoff -a`.
You can do this before shutting down the system, or after, in a debug shell.

---

Try to add the `-proposed` archive to your list of sources:
<https://wiki.ubuntu.com/Testing/EnableProposed>

And update systemd.

---

ATM, here's the output of `$ systemctl list-jobs`:

    JOB UNIT                                                          TYPE  STATE
    1529 dev-sda5.swap                                                 stop  running
    1528 dev-disk-by\x2did-wwn\x2d0x55cd2e404bd8ae31\x2dpart5.swap     stop  running
    1385 systemd-poweroff.service                                      start waiting
    1524 umount.target                                                 start waiting
    1525 dev-disk-by\x2dpath-...0000:00:1f.2\x2data\x2d5\x2dpart5.swap stop  running
    1384 poweroff.target                                               start waiting
    1526 dev-disk-by\x2duuid-...2\x2d4f56\x2da70d\x2d99203e934142.swap stop  running
    1527 dev-disk-by\x2did-at...120A3_CVCV434202BE120BGN\x2dpart5.swap stop  running
    1533 final.target                                                  start waiting

    9 jobs listed.

You can see that there are 5 jobs running; they are all related to the swap.
And there  are 4 jobs  waiting; they are  probably waiting for  the swap-related
jobs to be finished.
In conclusion, it seems our hanging issue is related to the swap.

---

Document how to start a debug shell during the boot process.

I think you need to edit `/etc/default/grub`, and append the item
`systemd.debug-shell` in the value assigned to `GRUB_CMDLINE_LINUX` (see
`/usr/share/doc/systemd/README.Debian.gz`), then run `$ sudo update-grub`.

For more info about the difference between `GRUB_CMDLINE_LINUX` and
`GRUB_CMDLINE_LINUX_DEFAULT`, see `info -f grub -n 'Simple configuration'`.

