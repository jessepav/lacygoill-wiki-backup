# Unit
## If I don't provide the suffix of a unit passed as an argument of `$ systemctl [subcommand]`, what happens?

systemctl will  append '.service', unless  the command operates only  on another
specific unit type, in which case the right suffix will be appended.

So, for example, these commands are equivalent:

        $ systemctl start sshd
    ⇔
        $ systemctl start sshd.service


        $ systemctl isolate default
    ⇔
        $ systemctl isolate default.target

##
## Which unit does `systemctl` operate on, if I execute
### `$ systemctl status /dev/sda`?

    dev-sda.device

This shows that `systemctl` converts automatically a device node to a device unit name.

### `$ systemctl status /run/user/1000`?

    run-user-1000.mount

This shows that `systemctl` converts automatically a path to a mount unit name.

###
# Unit file configuration
## How can I extend the configuration of a service unit file without modifying it directly?

Write your additional directives in:

                               if you were to extend another type of unit,
                               you would need to change this accordingly
                               v-----v
    /etc/systemd/system/<name>.service.d/my_extra_directives.conf
                                      ^^                    ^---^

## ?

Which files are created/removed because of a `WantedBy` or `RequiredBy` directive in the `[Install]` section?

If you write the directive:

    WantedBy=foo.service

inside the unit file `bar.service`, then,  when you'll execute:

    $ systemctl enable bar.service

systemd will create a symlink in:

    /etc/systemd/system/foo.service.wants/bar.service

For `RequiredBy`, the symlink would be created in:

    /etc/systemd/system/foo.service.requires/bar.service

The symlink will be removed when you execute:

    $ systemctl disable bar.service

---

What's the effect of the `Wants` and `Requires` directives in the `[Unit]` section?

Same effect as the `WantedBy` and `RequiredBy` directives.
But the effect is not obtained  at installation time (`$ systemctl enable ...`),
but when the unit file is loaded at runtime.

---

Also,  the sshd.service.wants/  and  sshd.service.requires/  directories can  be
created.
These directories contain symbolic links to  unit files that are dependencies of
the sshd service.

The  symbolic  links  are   automatically  created  either  during  installation
according to [Install] unit file options or at runtime based on [Unit] options.

---

Many unit file options can be set using the so called unit specifiers – wildcard
strings that are  dynamically replaced by unit parameters when  the unit file is
loaded.
This  enables  creation of  generic  unit  files  that  serve as  templates  for
generating instantiated units.

---

From `man systemd.unit`:

Along with a unit file foo.service, the directory foo.service.wants/ may exist.
All  unit  files  symlinked  from  such a  directory  are  implicitly  added  as
dependencies of type Wants= to the unit.
This is useful to hook units into the start-up of other units, without having to
modify their unit files.
The preferred way to create symlinks in  the .wants/ directory of a unit file is
with the  enable command of the  systemctl(1) tool which reads  information from
the [Install] section of unit files.
A  similar functionality  exists for  Requires= type  dependencies as  well, the
directory suffix is .requires/ in this case.

Along with  a unit  file foo.service, a  "drop-in" directory  foo.service.d/ may
exist.
All files with the  suffix ".conf" from this directory will  be parsed after the
file itself is parsed.
This is useful to alter or add configuration settings for a unit, without having
to modify unit files.
Each drop-in file must have appropriate section headers.

Note that  for instantiated units, this  logic will first look  for the instance
".d/" subdirectory  and read its ".conf"  files, followed by the  template ".d/"
subdirectory and the ".conf" files there.
Also note that settings from the "[Install]" section are not honoured in drop-in
unit files, and have no effect.

...

[INSTALL] SECTION OPTIONS

Unit  files  may include  an  "[Install]"  section, which  carries  installation
information for the unit.
This section is not interpreted by systemd(1)  during runtime; it is used by the
enable and  disable commands of the  systemctl(1) tool during installation  of a
unit.
Note that settings in the "[Install]" section may not appear in `.d/*.conf` unit
file drop-ins (see above).

---

    WantedBy=
    RequiredBy=

This option may be used more than  once, or a space-separated list of unit names
may be given.
A symbolic link is created in the .wants/ or .requires/ directory of each of the
listed units when this unit is installed by `$ systemctl enable`.
This has the effect that a dependency  of type Wants= or Requires= is added from
the listed unit to the current unit.
The primary result is that the current unit will be started when the listed unit
is started.

In case of template units, `$ systemctl  enable` must be called with an instance
name, and this instance  will be added to the .wants/ or  .requires/ list of the
listed unit.

E.g. if  you write `WantedBy=getty.target`  in a service  `getty@.service`, then
execute:

    $ systemctl enable getty@tty2.service

systemd will  create a  symlink from  `getty.target.wants/getty@tty2.service` to
`getty@.service`.

---

    Alias=

A space-separated list of additional names this unit shall be installed under.
The names  listed here must have  the same suffix  (i.e. type) as the  unit file
name.
This option may be specified more than  once, in which case all listed names are
used.
At installation time, `$ systemctl enable` will create symlinks from these names
to the unit filename.

---

How do I know whether a drop-in file exists for a given service?

    $ systemctl status <name>

In the output, look for a line beginning with `Drop-In:`.

    Drop-In: /usr/lib/systemd/system/ssh.service.d
             └─bar.conf, foo.conf

In this example, we can see that  the ssh service has 2 drop-in files `foo.conf`
and `bar.conf`, inside `/usr/lib/systemd/system/ssh.service.d/`.

---

Which extension must I use when writing a drop-in configuration file for a service?

    .conf

It's not `.service`!  How can systemd know which type of unit I'm configuring?

`.service` is present  in the path of the configuration  file, more specifically
in the parent directory name.

---

Which command must I execute after creating/modifying a drop-in configuration file?

    $ systemctl daemon-reload

---

What's the difference between the subcommands `reload` and `daemon-reload`?

    reload PATTERN...

Asks all units listed on the command-line to reload their configuration.
Note  that this  will reload  the service-specific  configuration, not  the unit
configuration file of systemd.
If  you want  systemd  to reload  the  configuration  file of  a  unit, use  the
daemon-reload command.
In  other words:  for the  example  case of  Apache, this  will reload  Apache's
httpd.conf in the web server, not the apache.service systemd unit file.


    daemon-reload

Reload the systemd manager configuration.
This  will rerun  all  generators (see  systemd.generator(7)),  reload all  unit
files, and recreate the entire dependency tree.
While the  daemon is being  reloaded, all sockets  systemd listens on  behalf of
user configuration will stay accessible.


   > Just in case, daemon-reload isn't universal,  have got to run systemctl --user
   > daemon-reload for user services.

Source:
<https://serverfault.com/questions/700862/do-systemd-unit-files-have-to-be-reloaded-when-modified#comment1154734_700956>

---

    $ sudo tee -a /etc/systemd/system/my_service.service <<'EOF'
    [Unit]
    Description=My Application

    [Service]
    ExecStart=/usr/bin/printf 'We have been triggered'
    EOF

    $ systemctl start my_service
    $ journalctl --unit=my_service
    <date> ubuntu systemd[1]: Started My Application.˜
    <date> ubuntu printf[1234]: We have been triggered˜
                         ^--^
                         pid˜

    $ sudo tee -a /etc/systemd/system/my_service.path <<'EOF'
    [Unit]
    Description=Check for files

    [Path]
    PathExists=/tmp/crash.log
     # not necessary, but may make the code more readable
    Unit=my_service.service

    [Install]
    WantedBy=multi-user.target
    EOF

    $ systemctl enable my_service.path
    Created symlink from /etc/systemd/system/multi-user.target.wants/my_service.path˜
                    to   /etc/systemd/system/my_service.path˜

    $ systemctl start my_service.path

    $ journalctl --unit=my_service.path
    <date> ubuntu systemd[1]: Started My Application.˜
    <date> ubuntu printf[1234]: We have been triggered˜

              no new entries

    $ touch /tmp/crash.log

    $ journalctl --unit=my_service.path
    <date>       ubuntu systemd[1]: Started My Application.˜
    <date>       ubuntu printf[1234]: We have been triggered˜
    <other_date> ubuntu systemd[1]: Started My Application.      ← new entry˜
    <other_date> ubuntu printf[5678]: We have been triggered     ← new entry˜

##
# Service
## What's “socket-based activation”?

That's  how  systemd  is  able  to  start  several  services  with  dependencies
relationships, on the condition that they communicate via sockets.

If A  is a service depending  on another service  B, and they communicate  via a
socket usually created by B, systemd creates it immediately in the place of B.

IOW, from A  point of view, B  is **activated** prior to its  start, through the
immediate creation of its socket.

Any data that  A sends to the socket before  B is ready, is sent to  a buffer by
the kernel.
When systemd starts B, it passes the socket as an argument of `exec()`.
Once B is started, it processes the requests stored in the buffer.

If  A expects  a response  from B,  but doesn't  get one  because B  hasn't been
started yet, it automatically stops, and resumes as soon as the response arrives
from the socket.
If for some reason,  B fails to start, systemd aborts the start  of A after some
time.

---

As an example, when it is started,  the D-Bus service connects to the `/dev/log`
socket and uses it  to communicate with the syslog service so  that it can write
status and error messages to the system log if required.

To avoid  making D-Bus  wait for  syslog, systemd  activates syslog  by creating
`/dev/log` itself, and then launches syslog and D-Bus at the same time.

## How can systemd restart a crashed service A, without causing another service B to lose its connection to A?

B is connected to A via a socket.
The latter is maintained by systemd, not by A.
So, when systemd  restarts A, B can  still send its requests to  the socket: the
connection is preserved.

The kernel  will buffer the client  requests it receives from  the socket during
the restart.  The new A process will take over where the old one left off.

## What's the difference between a service and a daemon?

A service is basically just a collection of daemons:
<https://www.youtube.com/watch?v=S9YmaNuvw5U&t=173s>

It corresponds to a cgroup.

###
## What's the difference between
### the `enable` and `reenable` subcommands?

`reenable` is a combination of `disable` and `enable`.
It's  better to  use `reenable`  rather  than `enable`  to enable  a unit  after
editing the `[Install]` section of its unit file.

A  unit is  enabled  through the  creation  of symlinks,  as  configured in  the
`[Install]` section of its unit file.
`enable` is only concerned with the  creation of new symlinks; it doesn't remove
any stale symlink.  So, for example, if you have this section in a unit file:

    [Install]
    WantedBy=multi-user.target
             ^--------^

And you edit it like so:

    [Install]
    WantedBy=graphical.target
             ^-------^

Then execute `$ systemctl enable <name>`, a new symlink would be created in:

    /etc/systemd/system/graphical.target.wants/

But the stale one in:

    /etc/systemd/system/multi-user.target.wants/

would *not* be removed.

### the `disable` and `mask` subcommands?

In addition to  disable a unit, `mask` prevents it  from being started manually,
or automatically by another unit.

### starting/stopping a service unit and enabling/disabling it?

Starting/stopping only affects the **currently** running system and is **not persistent**.

Enabling/disabling  affects the  system at  the  **next** target  change and  is
**persistent**.

Also, these 2 categories of commands are orthogonal.
As a result, if you disable a service while it's running, it will still run:

    $ systemctl is-enabled whoopsie; systemctl is-active whoopsie
    enabled
    active

    $ sudo systemctl disable whoopsie

    $ systemctl is-enabled whoopsie; systemctl is-active whoopsie
    disabled
    active
    ^----^
    even though `whoopsie` has been disabled, it's still running

###
## What happens when
### I enable the whoopsie service unit?

If it didn't already exist, systemd creates a symlink from:

    /etc/systemd/system/multi-user.target.wants/whoopsie.service

To:

    /usr/lib/systemd/system/whoopsie.service

MRE:

                     vv
    $ sudo systemctl reenable whoopsie.service
            Removed symlink /etc/systemd/system/multi-user.target.wants/whoopsie.service.
            Created symlink from /etc/systemd/system/multi-user.target.wants/whoopsie.service to /usr/lib/systemd/system/whoopsie.service.

### I disable the whoopsie service unit?

The symlink is removed.

### I mask the whoopsie service unit?

The symlink is created, but it points to `/dev/null`.

###
## What's a positive/negative dependency between 2 services?

If  a service  requires  **starting** another  service,  there's a  **positive**
dependency between the two.

If  a service  requires  **stopping** another  service,  there's a  **negative**
dependency between the two.

## What happens if I try to start a service with a negative dependency to a currently running service?

The currently running service is automatically stopped.

For example, if  you are running the  postfix service, and you try  to start the
sendmail service, systemd  first automatically stops postfix,  because these two
services are conflicting and cannot run on the same port.

###
## What's the difference between a loaded service and a running service?

A loaded service is a service whose definition has been loaded in the RAM.
But it doesn't mean that it's currently running.
It might:

   - be running
   - have run in the past
   - have failed to run in the past

## What's an enabled service?

A service which will be automatically started when the current target changes.
This includes at boot time.

##
## Why should I kill a service with `$ systemctl kill`, and not with `kill(1)`?

Some services spawn  more than one active process, and  `kill(1)` might not shut
them all  down.  Those services  might linger on  as zombie processes  until the
operating system finally reaps them and gets rid of them.

You don't want zombie processes, so don't use `kill(1)`.

##
## How to print
### detailed information about a given service (pid, memory, log, ...)?

    $ systemctl status <name>.service

### all the properties of the cron service?

    $ systemctl show --all cron

### the alias names of the rsyslog service ?

                     limit display to the `Names` property
                     v--------------v
    $ systemctl show --property=Names rsyslog.service
    rsyslog.service  syslog.service
    ^-------------^  ^------------^
        alias 1         alias 2

### the services that are ordered to start after/before a given service?

    $ systemctl list-dependencies --after  <name>.service

    $ systemctl list-dependencies --before <name>.service

###
## How to
### start the services foo and bar in a single command?

    $ systemctl start foo bar

### reload the config of a service unit?

    $ systemctl reload <name>.service

### restart a service unit?

    $ systemctl restart <name>.service

Note that if the service was not running, this command would still start it.

#### but only if it's running?

    $ systemctl try-restart <name>.service

### reload the config of a service unit, then, if it fails, restart it?

    $ systemctl reload-or-restart     <name>.service
    $ systemctl reload-or-try-restart <name>.service

The `reload-or-restart` subcommand is useful because some services don't support
the “reload my  config” feature (their unit file doesn't  contain a `ReloadExec`
directive).

###
## How to list all services whose name begin with `vbox`?

    $ systemctl list-units --type=service --all 'vbox*'

This shows that you can use glob patterns in some `systemctl(1)` subcommands.

For more info, see:

    man 3 fnmatch
    man 7 glob

But it doesn't seem to work with all of them.
In  particular,  it  doesn't  work  with the  `start`,  `enable`  and  `disable`
subcommands.

The  reason may  be that,  when  expanding a  glob pattern,  for some  commands,
systemctl ignores a unit which is inactive or not loaded.
This seems to be implied in `man systemctl`:

   > Note  that glob  patterns operate  on the  set of  primary names  of currently
   > loaded units.
   > **Units which are not active and are not in a failed state usually are not loaded,**
   > **and will not be matched by any pattern.**
   > In addition,  in case  of instantiated  units, systemd is  often unaware  of the
   > instance name until the instance has been started.
   > **Therefore, using glob patterns with start has limited usefulness.**
   > Also, secondary alias names of units are not considered.

What's weird though, is  that if you disable a unit,  `$ systemctl status` still
reports that it's loaded.
So, it should be taken into consideration when expanding a glob, but in practice
that's not what happens:

    $ sudo systemctl stop ssh
    $ systemctl status ssh
    loaded and inactive˜

    $ sudo systemctl start 'ss*'
    $ systemctl status ssh
    loaded and inactive˜
               ^^
               ✘ it should be loaded and active˜

## How to see the status of all services whose name begin with `vbox`?

    $ systemctl status 'vbox*'

## How to stop all `sshd@.service` instances?

    $ systemctl stop 'sshd@*.service'

##
## How to check the status of the `cron` service on a remote machine, from the local one?

    $ sudo systemctl --host=user@machine status cron.service

More generally, `--host=user@machine` lets you execute an arbitrary
`systemctl(1)` command on a remote machine:

    $ sudo systemctl --host=user@machine <subcommand> <arguments>

##
# Target
## What's the purpose of a target unit?

Group together other systemd units through a chain of dependencies.

---

For  example, the  graphical.target unit,  which is  used to  start a  graphical
session, starts system services such as lightdm (display-manager.service):

    $ cat /usr/lib/systemd/system/graphical.target
            ...
            Wants=display-manager.service
            ...

and also activates the multi-user.target unit:

    $ cat /usr/lib/systemd/system/graphical.target
            ...
            Requires=multi-user.target
            ...

---

Similarly,  the multi-user.target  unit  starts other  system  services such  as
NetworkManager (NetworkManager.service):

    $ ls /etc/systemd/system/multi-user.target.wants/
            ...
            NetworkManager.service
            ...

and DBus (dbus.service):

    $ ls /usr/lib/systemd/system/multi-user.target.wants/
            ...
            dbus.service
            ...

It also activates another target unit named basic.target:

    $ cat /usr/lib/systemd/system/multi-user.target
            ...
            Requires=basic.target
            ...

##
## What's the name of the target unit to
### shut down and reboot the system?

    reboot.target

### shut down and power off the system?

    poweroff.target

### set up a rescue shell?

    rescue.target

### set up a non-graphical multi-user system?

    multi-user.target

### set up a graphical multi-user system?

    graphical.target

###

## What does systemd do when I enter rescue mode?

It mounts all local file systems and starts some important system services.
But it does not activate network interfaces,  nor does it allow more users to be
logged into the system at the same time.

## When should I use it?

When you're unable to complete a regular booting process, and you need to repair
your system.

## What does systemd do when I enter emergency mode?

It mounts the root file system only for reading, and only starts a few essential
services.
It does  NOT attempt  to mount  any other local  file systems,  and it  does NOT
activate network interfaces.

## When should I use it?

When you can't enter rescue mode.

##
## How to turn off the graphical interface?

    $ sudo systemctl isolate multi-user.target

###
## How to list the ACTIVE and loaded target units?

    $ systemctl list-units --type=target

## How to list ALL the loaded target units?

    $ systemctl list-units --type=target --all

## How to change the current target?

    $ sudo systemctl isolate <new>.target

## How to enter rescue mode?

    $ sudo systemctl isolate   rescue.target

## How to exit rescue mode?

    $ sudo systemctl reboot

---

Don't press `C-d`, and don't execute:

    $ exit

Or:

    $ sudo systemctl default

Each time I've tried, the system didn't respond anymore.

The issue  may come from  the fact that stopping  lightdm and thus  the graphics
driver breaks the state of the graphics card:
<https://ubuntuforums.org/showthread.php?t=2330707>

OTOH, you can enter multi-user mode, then get back to graphical mode:

    $ sudo systemctl isolate multi-user.target

    C-M-F2

    # login

    $ sudo systemctl isolate graphical.target
OR
    $ sudo systemctl default

## How to print the default target unit?

    $ systemctl get-default

## How to set the default target unit?

    $ sudo systemctl set-default <new>.target

## What happens when I change the default target unit?

It creates a symlink from:

    /etc/systemd/system/default.target

To:

    /usr/lib/systemd/system/<new>.target

Note that by default, this symlink doesn't exist.
It's created as soon as you use the `set-default` subcommand.

##
# Shutting down the system
## How to halt the system?  (2)

    $ sudo systemctl halt

    $ sudo shutdown --halt

## How to poweroff the system?  (2)

    $ sudo systemctl poweroff

    $ sudo shutdown --poweroff now

## How to reboot the system?  (2)

    $ sudo systemctl reboot

    $ sudo shutdown --reboot

## How to suspend the system?

    $ sudo systemctl suspend

## How to hibernate the system?

    $ sudo systemctl hibernate

## How to hibernate and suspend the system?

    $ sudo systemctl hybrid-sleep

This command makes the OS save the system state on the hard disk (hibernate), so
that the session can be restored even in case of power failure.
And it makes the OS save the system  state in the RAM (suspend), so that you can
resume the session quickly.

IOW, it's supposed to take the best of the 2 concepts:

   - resilience (hibernate)
   - quickness (suspend)

##
## How to shut down the system at 12:34?

    $ sudo shutdown --poweroff 12:34

---

This shows an advantage of `shutdown(8)` over `sytemctl(1)`:
you can pass a time argument to delay the operation.

---

5  minutes before  the system  is  shut down,  the file  `/run/nologin` will  be
created to prevent any user to log on the machine.
If you cancel the shutdown later, the file will be removed.

## How to halt the system in 5 minutes?

    $ sudo shutdown --halt +5

The keyword `now` is an alias for `+0`.

## How to append a custom message to the default one sent to the logged users when a shutdown is scheduled?

Add it at the end of the command:

    $ sudo shutdown --halt +5 'bye people'

Note that to see the message, you must be logged in a console:

    C-M-F1
    # login

## How to prevent any message from being sent?

Use the `--no-wall` option:

    $ sudo shutdown --halt +5 --no-wall
    $ sudo shutdown --poweroff 12:34 --no-wall

## How to cancel a pending shutdown?

    $ sudo shutdown -c

##
# ?

When you log in for the first time, systemd automatically launches a
`$ systemd --user` instance:

    $ pstree -lsp $(pidof systemd)
    systemd(1)───systemd(1150)───(sd-pam)(1151)˜

This process will be killed when you log out.

It's responsible for managing your services, which can be used to run daemons or
automated  tasks,  with  all  the  benefits  of  systemd,  such  as  socket-basd
activation, timers, dependency system or strict process control via cgroups.

Similarly to system  units, user units are located in  the following directories
(in descending order of priority):

When systemd user instance starts, it brings up the target default.target:

    /usr/lib/systemd/user/default.target
    │
    └─ /usr/lib/systemd/user/basic.target
       │
       └─ /usr/lib/systemd/user/sockets.target
          /usr/lib/systemd/user/timers.target
          /usr/lib/systemd/user/paths.target

Other units can be controlled manually with `$ systemctl --user`.

---

Be  aware that  the `systemd  --user` instance  is a  per-user process,  and not
per-session.
This means that all user services run outside of a session.
As a consequence,  programs that need to  be run inside a  session will probably
break in user services.

`systemd --user` runs as a separate process from the `systemd --system` process.
User units can not reference or depend on system units.

---

Basic setup

All the user services will be placed in:

    ~/.config/systemd/user/

If you want to run a service on first login, execute:

    $ systemctl --user enable <service>

for any service you want to be autostarted.
Tip: If  you want  to  enable a  service  for  all users  rather  than the  user
executing the systemctl command, run as root:

    $ systemctl --user --global enable <service>

---

Environment variables

The user instance  of systemd does not inherit any  of the environment variables
set in places like .bashrc etc.
There  are several  ways  to  set environment  variables  for  the systemd  user
instance:

1. For users with a $HOME directory, create a .conf file in the
   ~/.config/environment.d/ directory with lines of the form NAME=VAL.  Affects
   only that user's user unit.  See environment.d(5) for more information.

2. Use the DefaultEnvironment option in /etc/systemd/user.conf file.  Affects all
   user units.

3. Add a drop-in config file in /etc/systemd/system/user@.service.d/.  Affects
   all user units; see #Service example

4. At any time, use systemctl --user set-environment or systemctl --user
   import-environment.  Affects all user units started after setting the
   environment variables, but not the units that were already running.

5. Using the dbus-update-activation-environment --systemd --all command provided
   by dbus.  Has the same effect as systemctl --user import-environment, but also
   affects the D-Bus session.  You can add this to the end of your shell
   initialization file.

6. For "global" environment variables for the user environment you can use the
   environment.d directories which are parsed by systemd generators.  See
   environment.d(5) for more information.

7. You can also write an environment generator script which can produce
   environment variables that vary from user to user, this is probably the best
   way if you need per-user environments (this is the case for XDG_RUNTIME_DIR,
   DBUS_SESSION_BUS_ADDRESS, etc).  See systemd.environment-generator(7).

One variable you may want to set is PATH.

After configuration, the command `systemctl --user show-environment` can be used
to verify that the values are correct.

# ?

From the book "Linux Service Management Made Easy with systemd":

   > Halting with systemctl
   > Using a sudo systemctl halt command halts the operating system, but it doesn't
   > power down the computer. Because I can read your mind, I know that you're saying, But
   > Donnie. Why would I want to halt the operating system but leave the computer running?
   > Well, I don't know. That's something that I've never figured out in my entire Linux career.

Answer to the author's question:
<https://superuser.com/a/900205>

#
# Pitfalls
## Some service fails to start!  Where can I find the best help to make it work?

First, query the systemd journal:

    $ journalctl --catalog --pager-end --unit=some.service
                 ^-------^
                 Augment log lines with explanation texts from the message catalog.
                 Do *not* use this when attaching a log in a bug report.

It might be quite long.  To make it  more readable, try to capture the output in
a Vim buffer, and start a new fold on every line matching `^-- Subject: `.
*Our custom `za` mapping does exactly that.*

Inside, look for some  short help text giving a solution, or a  URL to a support
forum/documentation.

If you don't find anything, look for the name of the command which fails.
Then, find the name of the package providing the binary/script implementing this
command.  Example (on Ubuntu):

    $ apt-file search /path/to/cmd

Next, query your package manager for the description of this package.  Example:

    $ apt show package

Inside the output, look for a URL  to a website where the project developing the
code for the command is hosted.  This website is probably the best place to find
the information  you need.  If it  includes a bug  tracker, type a query  in its
search  box.  If  it's on  github, sort  the filtered  issues so  that the  most
commented ones are at the top.  The  most commented issues are probably the most
relevant for your issue.

### How to get more info about the cause of the error encountered by the service?

Make it use `syslog(3)` to log its stderr:

    $ sed -i 's/^StandardError=.*/StandardError=syslog/' \
        "$(systemctl show --property=FragmentPath -- some.service | sed 's/[^=]*=//')"

    $ systemctl daemon-reload
    $ systemctl start some.service

Now, query  the journal again.  This  time, there should be  more information in
this section:

    -- Subject: A start job for unit some.service has begun execution
    ...
    ... cmd[some pid]: error message given by the command itself
                       ^---------------------------------------^

##
## Which pitfall could I encounter by starting a service without systemd?

The started  process would inherit the  environment of the current  shell, which
could prevent it from working as expected.

This is  especially problematic if the  service starts other processes  (e.g. it
could be an application launcher  like `xbindkeys(1)`), because those would also
inherit the same environment.

With systemd, there are fewer surprises, because the environment is not affected
by whatever  shell you're currently  in.  And  it's less crowded;  compare those
numbers obtained in my current environment:

    $ env  | wc --lines
    161

    $ systemctl show-environment | wc --lines
    11

    $ systemctl --user show-environment | wc --lines
    43

So, don't run sth like this:

    $ xbindkeys

But this:

    $ systemctl --user start xbindkeys

If  you  really  need to  start  a  service  without  systemd, do  it  from  the
application launcher of  your desktop environment.  You might need  to write the
full path to the invoked binaries and to your home:

    $ /usr/bin/xbindkeys --file /home/lgc/.config/keyboard/xbindkeys.conf
      ^-------^                 ^-------^

## I can't kill a service!

Maybe its `Restart` property is set with a value like `on-abort`:

    $ systemctl show --property=Restart <service>
    Restart=on-abort
            ^------^

This means that the service is automatically restarted whenever its main process
receives  an unclean  kill signal.   That  is, a  signal which  doesn't let  the
process clean up after itself (e.g. `SIGKILL`).

See `man systemd.service /Table 2`.

Solution: Be nice when killing the service.  Let it clean up after itself,.
Make sure to send a signal like `SIGTERM` instead of `SIGKILL`.

##
# Issues
## I get a popup window every time I execute a `systemctl` command!

Prefix your command with `sudo(8)`.

You'll still be prompted for your password,  but only once per shell session and
without a popup window.

## My custom service is not executed!

For every executable you invoke, write a *full* path.

If that doesn't help, have a look at `$ journalctl --boot`.
The service must have written why it failed.

## The journal is spammed with `rtkit-daemon` messages!

    Dec 20 01:00:42 ubuntu rtkit-daemon[1019]: Supervising 7 threads of 6 processes of 1 users.
    Dec 20 01:00:42 ubuntu rtkit-daemon[1019]: Supervising 7 threads of 6 processes of 1 users.
    Dec 20 01:01:08 ubuntu rtkit-daemon[1019]: Supervising 7 threads of 6 processes of 1 users.
    ...

It's a known bug:

   - <https://github.com/heftig/rtkit/issues/22>
   - <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=939615>
   - <https://bugs.launchpad.net/ubuntu/+source/rtkit/+bug/1547589>

Consider removing the `rtkit` package:

    $ sudo apt purge rtkit

## The `fwupd-refresh` service fails to start!

    -- Subject: A start job for unit fwupd-refresh.service has begun execution
    ...

    -- Subject: Unit process exited
    ...
    -- The process' exit code is 'exited' and its exit status is 1.
    ...

    -- Subject: Unit failed
    ...

    -- Subject: A start job for unit fwupd-refresh.service has failed
    ...

This is probably caused by a [bug in systemd][1].

---

Solution1: Mask the service:

    $ systemctl mask fwupd-refresh.service

Solution2: Make a dedicated user:

    $ systemctl edit fwupd-refresh.service
    # in the new file, write:
    [Service]
    User=root
    # save and quit
    # the file should end up being written at:  /etc/systemd/system/fwupd-refresh.service.d/override.conf

    $ systemctl daemon-reload
    $ systemctl start fwupd-refresh.service

Solution3: Turn off the `DynamicUser` parameter:

    $ systemctl edit fwupd-refresh.service
    # in the new file, write:
    [Service]
    DynamicUser=no
    # save and quit

    $ systemctl daemon-reload
    $ systemctl start fwupd-refresh.service

For more info, see [this thread][2] on the issue tracker for the `fwupd` project.

## The journal catalog does not print the name of user units!

Yes:

    $ journalctl --user --unit=transmission-daemon.service --catalog | grep Subject

                                     v--v
    -- Subject: A start job for unit UNIT has finished successfully
    ...
                                    v--v
    -- Subject: A stop job for unit UNIT has begun execution
    ...
                                    v--v
    -- Subject: A stop job for unit UNIT has finished

I think it's a known bug.
See [this report][3] and [this one][4].

##
# Reference

[1]: https://github.com/systemd/systemd/issues/22737
[2]: https://github.com/fwupd/fwupd/issues/3037
[3]: https://github.com/systemd/systemd/issues/1972
[4]: https://github.com/systemd/systemd/issues/3351
