# ?

What does “static” mean in the output of `$ systemctl list-unit-files`

From `man systemctl`:

> The  unit file  is  not enabled,  and  has  no provisions  for  enabling in  the
> "[Install]" section.

# ?

       disable NAME...

Disables one or more units.
This  removes  all   symlinks  to  the  specified  unit  files   from  the  unit
configuration directory, and hence undoes the changes made by enable.
Note however  that this removes all  symlinks to the unit  files (i.e. including
manual additions), not just those actually created by enable.
This call implicitly  reloads the systemd daemon  configuration after completing
the disabling of the units.
Note  that this  command  does not  implicitly  stop the  units  that are  being
disabled.
If this is desired,  either --now should be used together  with this command, or
an additional stop command should be executed afterwards.

This command will print the actions executed.
This output may be suppressed by passing --quiet.

This command honors --system, --user, --runtime and --global in a similar way as
enable.

---

       enable NAME...

Enable  one or  more unit  files or  unit file  instances, as  specified on  the
command-line.
This will create a number of symlinks  as encoded in the "[Install]" sections of
the unit files.
After the symlinks have been created,  the systemd configuration is reloaded (in
a way that is equivalent to daemon-reload)  to ensure the changes are taken into
account immediately.
Note that this does not have the effect  of also starting any of the units being
enabled.
If this is desired,  either --now should be used together  with this command, or
an additional start command must be invoked for the unit.
Also  note that,  in case  of instance  enablement, symlinks  named the  same as
instances are  created in the  install location, however  they all point  to the
same template unit file.

This command will print the actions executed.
This output may be suppressed by passing --quiet.

Note that this operation creates only the suggested symlinks for the units.
While this command  is the recommended way to manipulate  the unit configuration
directory,  the administrator  is free  to make  additional changes  manually by
placing or removing symlinks in the directory.
This  is particularly  useful to  create  configurations that  deviate from  the
suggested default installation.
In this case, the administrator must  make sure to invoke daemon-reload manually
as necessary to ensure the changes are taken into account.

Enabling units should not be confused  with starting (activating) units, as done
by the start command.
Enabling and  starting units is orthogonal:  units may be enabled  without being
started and started without being enabled.
Enabling simply  hooks the unit into  various suggested places (for  example, so
that the  unit is  automatically started on  boot or when  a particular  kind of
hardware is plugged in).
Starting actually spawns the daemon process (in case of service units), or binds
the socket (in case of socket units), and so on.

Depending on whether --system, --user, --runtime, or --global is specified, this
enables the unit for  the system, for the calling user only,  for only this boot
of the system, or for all future logins of all users, or only this boot.
Note that in the last case, no systemd daemon configuration is reloaded.

Using enable on masked units results in an error.

---

       --runtime

When used with enable, disable, edit,  (and related commands), make changes only
temporarily, so that they are lost on the next reboot.
This will have  the effect that changes  are not made in  subdirectories of /etc
but in /run, with identical immediate effects, however, since the latter is lost
on reboot, the changes are lost too.

Similarly, when used  with set-property, make changes only  temporarily, so that
they are lost on the next reboot.

---

       --global

When used  with enable  and disable,  operate on  the global  user configuration
directory, thus enabling or disabling a unit file globally for all future logins
of all users.

---

       --user

Talk to the service manager of the calling user, rather than the service manager
of the system.

---

       --system

Talk to the service manager of the system.
This is the implied default.

##
##
##
# Init systems comparison
## Traditionally, what is the init process responsible for?

It must configure the userland, i.e.:

   - implement the filesystems that are required for system operation

   - configure the network

   - launch the services that run in the background,
     including those that enable users to log into the system

## Why is the old sysvinit system not well suited to a modern Linux distribution?

Linux is  now used on  a wide variety of  devices (mobile devices,  desktop PCs,
TVs, ...).
This has changed the requirements for the init process.

##
## What are the main characteristics of systemd (compared to other init systems)?

It doesn't require the dependencies between services to be specified in advance.
As a  result, it can start  them **in parallel**, which  uses hardware resources
more efficiently and allows the system to start quicker.

It   also   handles   various   tasks  that   were   previously   performed   by
distribution-specific scripts.
As  a  side effect,  it  eliminates  various configuration  differences  between
distributions.

## What does systemd do after the system has boot up?

It remains in the background, mostly in an idle state.

It communicates with  the kernel and will  be informed of events such  as a user
pressing Ctrl+Alt+Del.
When  the user  runs a  command such  as `$  systemctl poweroff`,  it will  then
initiate everything that's required to cleanly shut down the system.

###
## In a SysV-init distribution, if a service A depends on another B, when is A started?

After B is fully functional.

## In a systemd distribution, if a service A depends on another B, when is A started?

A and B are started simultaneously.

##
# Systemd
## What's the command executed by the first process?

Atm, on ubuntu, it's:

    /sbin/init splash

## It doesn't contain the word 'systemd'!  Why?

`/sbin/init` is a symlink to `[/usr]/lib/systemd/systemd`.

## Where is the default config of systemd?

    /etc/systemd/system.conf

##
# Unit
## What's the purpose of a “unit”?

It describes services,  listening sockets, and other objects  that are necessary
for systemd to perform its tasks.

## How is it implemented?

By a configuration file, called “unit file”.

For systemd running in `--system` mode, it's located in:

    ┌──────────────────────────┬──────────────────────────────────────────────────────┐
    │ /etc/systemd/system/     │ where system-wide user units are placed              │    |
    │                          │ by the system administrator                          │    |
    ├──────────────────────────┼──────────────────────────────────────────────────────┤    | decreasing order
    │ /run/systemd/system/     │ units created at run time                            │    | of priority
    ├──────────────────────────┼──────────────────────────────────────────────────────┤    |
    │ /usr/lib/systemd/system/ │ where units of packages installed system-wide belong │    v
    └──────────────────────────┴──────────────────────────────────────────────────────┘

For systemd running in `--user` mode, it's located in:

    ┌──────────────────────────────┬───────────────────────────────────────────────────┐
    │ ~/.config/systemd/user/      │ current user units                                │    |
    ├──────────────────────────────┼───────────────────────────────────────────────────┤    |
    │ /etc/systemd/user/           │ system-wide user units placed                     │    |
    │                              │ by the system administrator                       │    |
    ├──────────────────────────────┼───────────────────────────────────────────────────┤    | decreasing
    │ /run/user/1000/systemd/user/ │ units created at run time (for the current user?) │    | order
    ├──────────────────────────────┼───────────────────────────────────────────────────┤    | of
    │ /run/systemd/user/           │ units created at run time (for all users?)        │    | priority
    ├──────────────────────────────┼───────────────────────────────────────────────────┤    |
    │ ~/.local/share/systemd/user/ │ units of packages                                 │    |
    │                              │ that have been installed in the home directory    │    |
    ├──────────────────────────────┼───────────────────────────────────────────────────┤    |
    │ /usr/lib/systemd/user/       │ units of packages installed system-wide           │    v
    └──────────────────────────────┴───────────────────────────────────────────────────┘

## What are the different types of units?

    ┌────────────────┬────────────────┬────────────────────────────────────────────────┐
    │ Unit Type      │ File Extension │ Description                                    │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Service unit   │ .service       │ a system service                               │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Socket unit    │ .socket        │ an inter-process communication socket          │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Target unit    │ .target        │ a group of systemd units                       │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Device unit    │ .device        │ a device file recognized by the kernel         │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Mount unit     │ .mount         │ a file system mount point                      │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Automount unit │ .automount     │ a file system automount point                  │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Swap unit      │ .swap          │ a swap device or a swap file                   │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Timer unit     │ .timer         │ a systemd timer                                │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Snapshot unit  │ .snapshot      │ a saved state of the systemd manager           │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Path unit      │ .path          │ a file or directory in a file system           │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Slice unit     │ .slice         │ a group of hierarchically organized units that │
    │                │                │ manage system processes                        │
    ├────────────────┼────────────────┼────────────────────────────────────────────────┤
    │ Scope unit     │ .scope         │ an externally created process                  │
    └────────────────┴────────────────┴────────────────────────────────────────────────┘

You can get a similar list by executing:

    $ systemctl list-units -t help

Or shorter:

    $ systemctl -t help

Atm, it doesn't give the exact same list:
it omits 'snapshot', and includes 'busname' (no idea what this stands for).

##
## What's the purpose of
### a device unit?

It allows  systemd to  start a  service when  a particular  type of  hardware is
plugged in or becomes available.

### a mount unit?

It allows systemd to automatically mount a partition during the system boot.

### an automount unit?

It allows  systemd to automatically mount  a partition when you  enter its mount
point via a graphical file manager, or via `cd`.

### a path unit?

It  allows  systemd   to  automatically  start  a  service   when  a  particular
file/directory is accessed.
systemd uses `inotify` to monitor the file/directory.

### a socket unit?

It allows systemd to create a socket for socket activation.
However, it doesn't actually start the related service.
This will be done by a service unit that is associated with the socket unit.
When  a connection  request  is received,  systemd starts  the  service that  is
defined there, submitting the open socket.

##
## Why should an adminsys put their unit files in `/etc/systemd/system/` instead of `/usr/lib/systemd/system/`?

If  the  adminsys  uses  `/usr/lib/systemd/system/`, when  the  system  will  be
updated, the changes could be overwritten.

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

## Why can't I find any `.device`, `.scope` and `.swap` unit files on my system?

Systemd dynamically generates certain units itself.
As a result, these units don't show up in the filesystem, but they do appear in:

    $ systemctl list-units

## Which unit does `systemctl` operate on, if I execute `$ systemctl status /dev/sda`?

    dev-sda.device

This shows that systemctl converts automatically a device node to a device unit name.

Which unit does `systemctl` operate on, if I execute `$ systemctl status /run/user/1000`?

    run-user-1000.mount

This shows that systemctl converts automatically a path to a mount unit name.

## What's the default subcommand executed by `systemctl(1)`?

It's `list-units`:

    $ systemctl -t help
⇔
    $ systemctl list-units -t help

###
# Unit file configuration
## Why should I install the package `usrmerge`?

For the general case, see:
<https://www.freedesktop.org/wiki/Software/systemd/TheCaseForTheUsrMerge/>
<https://wiki.debian.org/UsrMerge>

For systemd in particular, it makes things simpler to understand, otherwise unit
files may be in one of:

    /lib/systemd/system
    /usr/lib/systemd/system

And they don't have the exact same  contents, so whenever you have an issue with
a unit file installed from a package, you have to look in 2 directories.

After installing `usrmerge`, the 2 paths lead to the exact same set of files.
Indeed the package seems  to move the existing binaries from  `/` to `/usr/` and
installs these symlinks for backward compatibility:

    /bin   → /usr/bin
    /sbin  → /usr/sbin
    /lib   → /usr/lib
    /lib64 → /usr/lib64

Btw, a backronym  for `usr` is “Universal System Resources”  (but originally, it
really stood for “USeR”):
<https://unix.stackexchange.com/a/103348/289772>

---

Note that you shouldn't  need to install the package for  Ubuntu 19.04 and later
versions.
Also, in  Debian, merged  /usr has  been the  default since  debootstrap 1.0.85,
reverted in 1.0.87 and re-enabled in 1.0.102.

##
## What's the name of a line in a unit file?

A directive.

## Where can I find information about all possible lines I can write in a unit file?

    man systemd.directives

## How can I extend the configuration of a service unit file without modifying it directly?

Write your additional directives in:

                               ┌ if you were to extend another type of unit,
                               │ you would need to change this accordingly
                               ├─────┐
    /etc/systemd/system/<name>.service.d/my_extra_directives.conf
                                      ^^                    ^^^^^

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
but when the unit file is loaded at run time.

---

Also,  the sshd.service.wants/  and  sshd.service.requires/  directories can  be
created.
These directories contain symbolic links to  unit files that are dependencies of
the sshd service.

The  symbolic  links  are   automatically  created  either  during  installation
according to [Install] unit file options or at run time based on [Unit] options.

---

Many unit file options can be set using the so called unit specifiers – wildcard
strings that are dynamically replaced with unit parameters when the unit file is
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
This section is not interpreted by systemd(1) during run time; it is used by the
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

    $ cat <<'EOF' | sudo tee -a /etc/systemd/system/my_service.service
    [Unit]
    Description=My Application

    [Service]
    ExecStart=/usr/bin/printf 'We have been triggered'
    EOF

    $ systemctl start my_service
    $ journalctl -u my_service
    <date> ubuntu systemd[1]: Started My Application.~
    <date> ubuntu printf[1234]: We have been triggered~
                         ^^^^
                         pid~

    $ cat <<'EOF' | sudo tee -a /etc/systemd/system/my_service.path
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
    Created symlink from /etc/systemd/system/multi-user.target.wants/my_service.path~
                    to   /etc/systemd/system/my_service.path~

    $ systemctl start my_service.path

    $ journalctl -u my_service.path
    <date> ubuntu systemd[1]: Started My Application.~
    <date> ubuntu printf[1234]: We have been triggered~

              no new entries

    $ touch /tmp/crash.log

    $ journalctl -u my_service.path
    <date>       ubuntu systemd[1]: Started My Application.~
    <date>       ubuntu printf[1234]: We have been triggered~
    <other_date> ubuntu systemd[1]: Started My Application.      ← new entry~
    <other_date> ubuntu printf[5678]: We have been triggered     ← new entry~

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
When systemd starts B, it passes the socket as an argument of exec().
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

---

Note that systemd doesn't start a service until a connection is made to its socket.

## How can systemd restart a crashed service A, without causing another service B to lose its connection to A?

B is connected to A via a socket.
The latter is maintained by systemd, not by A.
So, when systemd  restarts A, B can  still send its requests to  the socket: the
connection is preserved.

The kernel  will buffer the client  requests it receives from  the socket during
the restart.
The new A process will take over where the old one left off.

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
'[Install]' section of its unit file.
`enable` is only concerned with the creation of new symlinks.
It doesn't remove any stale symlink.
So, for example, if you have this section in a unit file:

    [Install]
    WantedBy=multi-user.target
             ^^^^^^^^^^

And you edit it like so:

    [Install]
    WantedBy=graphical.target
             ^^^^^^^^^

Then execute `$ systemctl enable <name>`, a new symlink would be created in:

    /etc/systemd/system/graphical.target.wants/

But the stale one in:

    /etc/systemd/system/multi-user.target.wants/

would NOT be removed.

### the `disable` and `mask` subcommands?

In addition to  disable a unit, `mask` prevents it  from being started manually,
or automatically by another unit.

### starting/stopping a service unit and enabling/disabling it?

Starting/stopping only affects the **currently** running system and is **not persistent**.

Enabling/disabling affects the  system at the **next** target  (runlevel) change and
is **persistent**.

Also, these 2 categories of commands are orthogonal.
As a result, if you disable a service while it's running, it will still run:

    $ systemctl is-enabled whoopsie; systemctl is-active whoopsie
    enabled~
    active~

    $ sudo systemctl disable whoopsie

    $ systemctl is-enabled whoopsie; systemctl is-active whoopsie
    disabled~
    active~
    ^^^^^^
    even though `whoopsie` has been disabled, it's still running~

###
## What happens when
### I enable the whoopsie service unit?

If it didn't already exist, systemd creates a symlink from:

    /etc/systemd/system/multi-user.target.wants/whoopsie.service

To:

    /usr/lib/systemd/system/whoopsie.service

MWE:

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

A loaded service is a service whose definition has been loaded in the ram.
But it doesn't mean that it's currently running.
It may, or it may have run in the past, or it may have failed.

## What's an enabled service?

A  service which  will  be  automatically started  when  the  current target  (≈
runlevel) changes.
This includes at boot time.

## How to print
### the status of all loaded services (i.e. are they running or not)?

    $ systemctl list-units -t service -a
                            │          │
                            │          └ short form of `--all`; include inactive services
                            │
                            └ short form of `--type`

### the enablement state of all installed service unit files?

    $ systemctl list-unit-files -t service

### detailed information about a given service (pid, memory, log, ...)?

    $ systemctl status <name>.service

### all the properties of the cron service?

    $ systemctl show -a cron

### the alias names of the lightdm service ?

                     ┌ limit display to the `Names` property
                     ├──────┐
    $ systemctl show -p Names lightdm.service
    lightdm.service  display-manager.service~
    ^                ^
    alias 1          alias 2~

Another example:

    $ systemctl show -p Names rsyslog.service
    rsyslog.service  syslog.service~
    ^                ^
    alias 1          alias 2~

###
## How to
### check whether a service unit is running?

    $ systemctl is-active <name>.service

### check whether a service unit is enabled?

    $ systemctl is-enabled <name>.service

### print the services that are ordered to start after/before a given service?

    $ systemctl list-dependencies --after  <name>.service

    $ systemctl list-dependencies --before <name>.service

###
## How to
### start and stop a service unit?

    $ systemctl start <name>.service
                            ├──────┘
                            └ optional
                              without, systemd assumes that <name> refers to a service unit

    $ systemctl stop <name>.service

### start the services foo and bar in a single command?

    $ systemctl start foo bar

### enable and disable a service unit?

    $ systemctl enable  <name>.service
    $ systemctl disable <name>.service

### reload the config of a service unit?

    $ systemctl reload <name>.service

### restart a service unit?

    $ systemctl restart <name>.service

Note that if the service was not running, this command would still start it.

### restart a service unit, but only if it's running?

    $ systemctl try-restart <name>.service

### reload the config of a service unit, then, if it fails, restart it?

    $ systemctl reload-or-restart     <name>.service
    $ systemctl reload-or-try-restart <name>.service

The `reload-or-restart` subcommand is useful because some services don't support
the “reload my  config” feature (their unit file doesn't  contain a `ReloadExec`
directive).

###
## How to list all services whose name begin with `vbox`?

    $ systemctl list-units -a -t service 'vbox*'

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

What's weird though, is that if you  disable a unit, `$ systecmctl status` still
reports that it's loaded.
So, it should be taken into consideration when expanding a glob, but in practice
that's not what happens:

    $ sudo systemctl stop ssh
    $ systemctl status ssh
    loaded and inactive~

    $ sudo systemctl start 'ss*'
    $ systemctl status ssh
    loaded and inactive~
               ^^
               ✘ it should be loaded and active~

## How to see the status of all services whose name begin with `vbox`?

    $ systemctl status 'vbox*'

## How to stop all `sshd@.service` instances?

    $ systemctl stop 'sshd@*.service'

##
## How to check the status of the `cron` service on a remote machine, from the local one?

    $ sudo systemctl -H user@machine status cron.service
                      │
                      └ abbreviation of `--host`

More generally, `-H user@machine` allows you to execute an arbitrary `systemctl`
command on a remote machine:

    $ sudo systemctl -H user@machine <subcommand> <arguments>

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

    $ systemctl list-units -t target

## How to list ALL the loaded target units?

    $ systemctl list-units -t target -a

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

    $ sudo shutdown {-H|--halt}

## How to poweroff the system?  (2)

    $ sudo systemctl poweroff

    $ sudo shutdown {--poweroff|-P|-h} now

## How to reboot the system?  (2)

    $ sudo systemctl reboot

    $ sudo shutdown {--reboot|-r}

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

    $ sudo shutdown -P 12:34

---

This shows an advantage of `shutdown(8)` over `sytemctl(1)`:
you can pass a time argument to delay the operation.

---

5  minutes before  the system  is  shut down,  the file  `/run/nologin` will  be
created to prevent any user to log on the machine.
If you cancel the shutdown later, the file will be removed.

## How to halt the system in 5 minutes?

    $ sudo shutdown -H +5

The keyword `now` is an alias for `+0`.

## How to append a custom message to the default one sent to the logged users when a shutdown is scheduled?

Add it at the end of the command:

    $ sudo shutdown -H +5 'bye people'

Note that to see the message, you must be logged in a console:

    C-M-F1
    # login

## How to prevent any message from being sent?

Use the `--no-wall` option:

    $ sudo shutdown -H +5    --no-wall
    $ sudo shutdown -P 12:34 --no-wall

## How to cancel a pending shutdown?

    $ sudo shutdown -c

##
##
##
# ?

Files that end in .target define groups of units.
They  achieve  little  themselves  and  serve  to  call  other  units  that  are
responsible for services, filesystems or other components.
They allow boot targets to be defined  that are equivalent to the classical SysV
runlevels.
For  example,  the multi-user.target  unit  starts  all  the services  that  old
distributions would call in runlevel 3.
IOW,  it fully  starts  the  system, but  without  launching  a graphical  login
manager.
The  latter  appears  with  the  graphical.target unit,  making  this  unit  the
equivalent of runlevel 5 and the typical default target.

Target units  start other units  via dependencies and  can be compared  to Sys-V
runlevels.
When the  system is  booted, systemd activates  a special  default.target target
unit.
Typically, default.target is only used as an alias for different targets such as
graphical.target or multi-user.target.
Targets can also build or depend on each other.
For example, graphical.target will wait for multi-user.target to start before it
launches the graphical user interface.

Where  necessary, the  addition of  "wants" to  the unit  files allows  users to
manually define dependencies between units.
This can be relevant for services such as the Apache web server, which expects a
fully configured network environment when it is started.
These services should depend on the network.target.
However, services  such as Avahi  or Bind  don't require the  dependency because
they can  correctly handle network  interfaces that  appear or disappear  at run
time.

##
##
##
# How to get the system status?

    $ systemctl status

# How to list the active units?

    $ systemctl

# How to list all units?

    $ systemctl -a

# How to list the failed units?

    $ systemctl --state failed

# How to list the installed unit files?

    $ systemctl list-unit-files

You only get the filenames.

#
#
#
# ?

When you log in for the first time, systemd automatically launches a
`$ systemd --user` instance:

    $ pstree -lsp $(pidof systemd)
    systemd(1)───systemd(1150)───(sd-pam)(1151)~

This process will be killed when you log out.

It's responsible for managing your services, which can be used to run daemons or
automated tasks,  with all the benefits  of systemd, such as  socket activation,
timers, dependency system or strict process control via cgroups.

Similarly to system  units, user units are located in  the following directories
(in decreasing order of priority):

    ┌──────────────────────────────┬───────────────────────────────────────────────────────┐
    │ ~/.config/systemd/user/      │ where the user puts their own units                   │
    ├──────────────────────────────┼───────────────────────────────────────────────────────┤
    │ /etc/systemd/user/           │ where system-wide user units are placed               │
    │                              │ by the system administrator                           │
    ├──────────────────────────────┼───────────────────────────────────────────────────────┤
    │ ~/.local/share/systemd/user/ │ where units of packages                               │
    │                              │ that have been installed in the home directory belong │
    ├──────────────────────────────┼───────────────────────────────────────────────────────┤
    │ /usr/lib/systemd/user/       │ where units provided by installed packages belong     │
    └──────────────────────────────┴───────────────────────────────────────────────────────┘

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
   ~/.config/environment.d/ directory with lines of the form NAME=VAL. Affects
   only that user's user unit. See environment.d(5) for more information.

2. Use the DefaultEnvironment option in /etc/systemd/user.conf file. Affects all
   user units.

3. Add a drop-in config file in /etc/systemd/system/user@.service.d/. Affects
   all user units; see #Service example

4. At any time, use systemctl --user set-environment or systemctl --user
   import-environment. Affects all user units started after setting the
   environment variables, but not the units that were already running.

5. Using the dbus-update-activation-environment --systemd --all command provided
   by dbus. Has the same effect as systemctl --user import-environment, but also
   affects the D-Bus session. You can add this to the end of your shell
   initialization file.

6. For "global" environment variables for the user environment you can use the
   environment.d directories which are parsed by systemd generators. See
   environment.d(5) for more information.

7. You can also write an environment generator script which can produce
   environment variables that vary from user to user, this is probably the best
   way if you need per-user environments (this is the case for XDG_RUNTIME_DIR,
   DBUS_SESSION_BUS_ADDRESS, etc). See systemd.environment-generator(7).

One variable you may want to set is PATH.

After configuration, the  command systemctl --user show-environment  can be used
to verify that the values are correct.

# systemd

DESCRIPTION

When run as first process on boot (as PID 1), it acts as init system that brings
up and maintains userspace services.

When  run  as a  system  instance,  systemd  interprets the  configuration  file
system.conf  and the  files in  system.conf.d directories;  when run  as a  user
instance, systemd interprets  the configuration file user.conf and  the files in
user.conf.d directories.
See systemd-system.conf(5) for more information.

<https://askubuntu.com/questions/676007/how-do-i-make-my-systemd-service-run-via-specific-user-and-start-on-boot>
<https://superuser.com/questions/476379/how-do-i-setup-a-systemd-service-to-be-started-by-a-non-root-user-as-a-user-daem>
<https://superuser.com/questions/853717/systemd-user-and-system>

<https://wiki.archlinux.org/index.php/Systemd>
<https://wiki.archlinux.org/index.php/Systemd/User>
<https://wiki.archlinux.org/index.php/Systemd_FAQ>
<https://wiki.archlinux.org/index.php/Environment_variables#Using_pam_env>
<https://wiki.archlinux.org/index.php/Systemd/Timers>

CONCEPTS

systemd provides a dependency system  between various entities called "units" of
12 different types.
Units  encapsulate various  objects that  are  relevant for  system boot-up  and
maintenance.
The majority of  units are configured in unit configuration  files, whose syntax
and basic set of options is described in systemd.unit(5).

Units may be:

   - "active"

     started, bound, plugged in, ..., depending on the unit type

   - "inactive"

     stopped, unbound, unplugged, ...

   - "activating"

     in the process of being activated

   - "deactivating"

     in the process of being deactivated

   - "failed"

     the  service  is inactive  because  it  failed  in some  way;  process
     returned error code on exit, or crashed, or an operation timed out
     If this state is entered, the cause will be logged, for later reference.

Note that  the various  unit types  may have a  number of  additional substates,
which are mapped to the five generalized unit states described here.

The following unit types are available:

1. Service units, which start and control daemons and the processes they consist
   of.

   For details, see systemd.service(5).

2. Socket units, which encapsulate local IPC or network sockets in the system,
   useful for socket-based activation.

   For details about socket units, see systemd.socket(5).
   For details  on socket-based  activation and other  forms of  activation, see
   daemon(7).

3. Target units are useful to group units, or provide well-known synchronization
   points during boot-up.

   See systemd.target(5).

4. Device units expose kernel devices in systemd and may be used to implement
   device-based activation.

   See systemd.device(5).

5. Mount units control mount points in the file system.

   See systemd.mount(5).

6. Automount units provide automount capabilities, for on-demand mounting of
   file systems as well as parallelized boot-up.

   See systemd.automount(5).

7. Timer units are useful for triggering activation of other units based on
   timers.

   See systemd.timer(5).

8. Swap units are very similar to mount units and encapsulate memory swap
   partitions or files of the operating system.

   See systemd.swap(5).

9. Path units may be used to activate other services when file system objects
   change or are modified.

   See systemd.path(5).

10. Slice units may be used to group units which manage system processes (such
    as service and scope units) in a hierarchical tree for resource management
    purposes.

    See systemd.slice(5).

11. Scope units are similar to service units, but manage foreign processes
    instead of starting them as well.

    See systemd.scope(5).

Units are named as their configuration files.
Some units have special semantics.
See systemd.special(7).

systemd knows  various kinds  of dependencies,  including positive  and negative
requirement  dependencies (i.e. Requires=  and Conflicts=)  as well  as ordering
dependencies (After= and Before=).
NB: ordering and requirement dependencies are orthogonal.
If  only a  requirement dependency  exists between  two units  (e.g. foo.service
requires  bar.service),  but  no  ordering dependency  (e.g.  foo.service  after
bar.service) and both are requested to start, they will be started in parallel.
It  is a  common pattern  that both  requirement and  ordering dependencies  are
placed between two units.

Application programs and  units (via dependencies) may request  state changes of
units.
In systemd,  these requests are encapsulated  as 'jobs' and maintained  in a job
queue.
Jobs may succeed or  can fail, their execution is ordered  based on the ordering
dependencies of the units they have been scheduled for.

On boot,  systemd activates  the target  unit `default.target`  whose job  is to
activate  on-boot services  and  other  on-boot units  by  pulling  them in  via
dependencies.

Processes systemd  spawns are  placed in individual  Linux control  groups named
after the unit which they belong to in the private systemd hierarchy.
systemd uses this to effectively keep track of processes.
Control group information is maintained in the kernel, and is accessible via the
file system  hierarchy (beneath  /sys/fs/cgroup/systemd/), or  in tools  such as
systemd-cgls(1)  or  ps(1) (ps  xawf  -eo  pid,user,cgroup,args is  particularly
useful to list all processes and the systemd units they belong to.).

systemd has a minimal transaction system: if  a unit is requested to start up or
shut  down,  systemd  will add  it  and  all  its  dependencies to  a  temporary
transaction.
Then, it will verify if the transaction is consistent (i.e. whether the ordering
of all units is cycle-free).
If it is not, systemd will try to fix it up, and removes non-essential jobs from
the transaction that might remove the loop.
Also, systemd tries to suppress non-essential jobs in the transaction that would
stop a running service.
Finally it is  checked whether the jobs of the  transaction contradict jobs that
have already been queued, and optionally the transaction is aborted then.
If all worked out and the transaction is consistent and minimized in its impact,
it is merged with all already outstanding jobs and added to the run queue.
Effectively this means that before executing a requested operation, systemd will
verify that it makes sense, fixing it if possible, and only failing if it really
cannot work.

Systemd  contains  native implementations  of  various  tasks  that need  to  be
executed as part of the boot process.
For example, it sets the hostname or configures the loopback network device.
It also sets up and mounts various API file systems, such as /sys or /proc.

Units may be  generated dynamically at boot and system  manager reload time, for
example based  on other configuration files  or parameters passed on  the kernel
command-line.
For details, see systemd.generator(7).

# target units

NAME
       systemd.target - Target unit configuration

DESCRIPTION

A unit configuration file whose name ends in ".target" encodes information about
a target  unit of systemd,  which is used for  grouping units and  as well-known
synchronization points during start-up.

This unit type has no specific options.
See systemd.unit(5) for the common options of all unit configuration files.
The  common  configuration  items  are  configured in  the  generic  [Unit]  and
[Install] sections.
A separate [Target] section does not exist, since no target-specific options may
be configured.

Target units  do not offer  any additional functionality  on top of  the generic
functionality provided by units.
They exist merely to group units  via dependencies (useful as boot targets), and
to establish standardized names for  synchronization points used in dependencies
between units.
Among  other things,  target  units are  a more  flexible  replacement for  SysV
runlevels in the classic SysV init system.
(And for  compatibility reasons  special target  units such  as runlevel3.target
exist which are used by the SysV runlevel compatibility code in systemd.
See systemd.special(7) for details).

AUTOMATIC DEPENDENCIES

Unless  DefaultDependencies=  is  set  to   no,  target  units  will  implicitly
complement  all   configured  dependencies   of  type  Wants=,   Requires=  with
dependencies of type  After=, unless an ordering dependency of  any kind between
the target and the respective other unit is already in place.
Note that this behaviour is disabled if either unit has DefaultDependencies=no.

#
# journalctl
## description

    $ journalctl [OPTIONS...] [MATCHES...]

`journalctl` may be used to query the contents of the systemd(1) journal.

If called  without parameters, it  will show the  full contents of  the journal,
starting with the oldest entry collected.

If one or more match arguments are passed, the output is filtered accordingly.
A match is in the format "FIELD=VALUE", e.g.:

    _SYSTEMD_UNIT=httpd.service

referring to the components of a structured journal entry.
See systemd.journal-fields(7) for a list of well-known fields.

> Entries in the journal resemble an  environment block in their syntax but with
> fields that can include binary data.
> Primarily, fields  are formatted  UTF-8 text strings,  and binary  formatting is
> used only where formatting as UTF-8 text strings makes little sense.
> New fields may freely be defined by  applications, but a few fields have special
> meaning.
> All fields with special meanings are optional.
> In some cases, fields may appear more than once per entry.
>
> USER JOURNAL FIELDS
>
> User fields are fields that are directly passed from clients and stored in the
> journal.
>
> TRUSTED JOURNAL FIELDS
>
> Fields prefixed  with an underscore are  trusted fields, i.e. fields  that are
> implicitly added by the journal and cannot be altered by client code.
>
> KERNEL JOURNAL FIELDS
>
> Kernel fields are  fields that are used by messages  originating in the kernel
> and stored in the journal.

If multiple matches are specified matching different fields, the log entries are
filtered by both, i.e. the resulting  output will show only entries matching all
the specified matches of this kind.
If two matches apply  to the same field, then they  are automatically matched as
alternatives, i.e.  the resulting output will  show entries matching any  of the
specified matches for the same field.
Finally, the character "+" may appear as  a separate word between other terms on
the command-line.
This causes all matches  before and after to be combined  in a disjunction (i.e.
logical OR).

As  shortcuts  for  a few  types  of  field/value  matches,  file paths  may  be
specified.
If a file  path refers to an  executable file, this is equivalent  to an `_EXE=`
match for the canonicalized binary path.
Similarly, if a path refers to a device  node then match is added for the kernel
name of the device (`_KERNEL_DEVICE=`).
Also,  matches  for  the kernel  names  of  all  the  parent devices  are  added
automatically.
Device node paths are not stable across reboots, therefore match for the current
boot id (`_BOOT_ID=`) is always added as well.
Note that only  the log entries for  the existing device nodes  maybe queried by
providing path to the device node.

Additional  constraints may  be added  using options  --boot, --unit=,  etc., to
further limit what entries will be shown (logical AND).

Output  is interleaved  from  all  accessible journal  files,  whether they  are
rotated or currently being written, and regardless of whether they belong to the
system itself or are accessible user journals.

The set of  journal files which will  be used can be modified  using the --user,
--system, --directory, and --file options, see below.

All users are granted access to their private per-user journals.
However, by default, only root and users who are members of a few special groups
are granted access to the system journal and the journals of other users.
Members of the groups "systemd-journal", "adm", and "wheel" can read all journal
files.
Note  that  the  two  latter groups  traditionally  have  additional  privileges
specified by the distribution.
Members of the "wheel" group can often perform administrative tasks.

When outputting  to a  tty, lines  are colored according  to priority:

   - lines of level ERROR and higher are colored red
   - lines of level NOTICE and higher are highlighted
   - other lines are displayed normally

## some useful commands

    $ journalctl -p4
    $ journalctl -xb (suggested when you enter rescue mode)
    $ journalctl -xn
    $ journalctl -u <unit>
    $ journalctl -b
    $ journalctl -f
    $ journalctl --since '10m ago'
                          │
                          └ you could also write '10 min ago'

## -p, --priority=

Filter output by message priorities or priority ranges.
Takes either a  single numeric or textual log level  (i.e. between 0/"emerg" and
7/"debug"), or a range of numeric/text log levels in the form FROM..TO.
The log levels are the usual syslog  log levels as documented in syslog(3), i.e.
"emerg" (0),  "alert" (1), "crit" (2),  "err" (3), "warning" (4),  "notice" (5),
"info" (6), "debug" (7).
If a single log level is specified, all  messages with this log level or a lower
(hence more important) log level are shown.
If a range is specified, all messages within the range are shown, including both
the start and the end value of the range.
This will add "PRIORITY=" matches for the specified priorities.

## -x, --catalog

Augment log lines with explanation texts from the message catalog.
This will add explanatory help texts to log messages in the output where this is
available.
These  short  help   texts  will  explain  the  context  of   an  error  or  log
event,  possible solutions,  as well  as pointers  to support  forums, developer
documentation, and any other relevant manuals.
Note that help texts  are not available for all messages,  but only for selected
ones.
For more information on the message catalog, please refer to the Message Catalog
Developer Documentation[4].

Note: when attaching journalctl output to bug reports, please do not use -x.

## -n, --lines=

Show the most recent journal events and limit the number of events shown.
If --follow is used, this option is implied.
The argument is a positive integer or "all" to disable line limiting.
The default value is 10 if no argument is given.

## -u, --unit=UNIT|PATTERN

Show messages for the  specified systemd unit UNIT (such as  a service unit), or
for any of the units matched by PATTERN.
If a pattern is specified, a list of unit names found in the journal is compared
with the specified pattern and all that match are used.
For  each   unit  name,   a  match   is  added  for   messages  from   the  unit
(`_SYSTEMD_UNIT=UNIT`), along with additional  matches for messages from systemd
and messages about coredumps for the specified unit.

This parameter can be specified multiple times.

## -b [ID][±offset], --boot=[ID][±offset]

Show messages from a specific boot. This will add a match for `_BOOT_ID=`.

The argument may be empty, in which case logs for the current boot will be shown.

If the  boot ID is omitted,  a positive offset  will look up the  boots starting
from the  beginning of the journal,  and an equal-or-less-than zero  offset will
look up boots starting from the end of the journal.
Thus, 1 means the first boot found  in the journal in chronological order, 2 the
second and so on; while -0 is the last boot, -1 the boot before last, and so on.
An empty offset is equivalent to specifying  -0, except when the current boot is
not the last boot (e.g. because --directory was specified to look at logs from a
different machine).

If the  32-character ID is  specified, it may  optionally be followed  by offset
which identifies the boot relative to the one given by boot ID.
Negative values mean earlier boots and positive values mean later boots.
If offset  is not specified, a  value of zero is  assumed, and the logs  for the
boot given by ID are shown.

## -f, --follow

Show only the most recent journal entries, and continuously print new entries as
they are appended to the journal.

## -S, --since=, -U, --until=

Start showing entries on  or newer than the specified date, or  on or older than
the specified date, respectively.
Date specifications should be of the format "2012-10-30 18:17:16".
If the time part is omitted, "00:00:00" is assumed.
If only the seconds component is omitted, ":00" is assumed.
If the date component is omitted, the current day is assumed.
Alternatively the strings "yesterday", "today", "tomorrow" are understood, which
refer to 00:00:00 of the day before the current day, the current day, or the day
after the current day, respectively.
"now" refers to the current time.
Finally, relative times may be specified, prefixed with "-" or "+", referring to
times before or after the current time, respectively.
For complete time and date specification, see systemd.time(7).

#
# systemctl
## description

NAME

systemctl - Control the systemd system and service manager

SYNOPSIS

    $ systemctl [OPTIONS...] COMMAND [NAME...]

DESCRIPTION

systemctl  may be  used to  introspect and  control the  state of  the "systemd"
system and service manager.
Please  refer to  systemd(1) for  an introduction  into the  basic concepts  and
functionality this tool manages.

## some useful commands

    $ systemctl  enable   <unit>
    $ systemctl  disable  <unit>
    $ systemctl  start    <unit>
    $ systemctl  stop     <unit>
    $ systemctl  reload   <unit>
    $ systemctl  restart  <unit>
    $ systemctl  status   <unit>

## enable NAME...

Enable  one or  more unit  files or  unit file  instances, as  specified on  the
command-line.
This will create a number of symlinks  as encoded in the "[Install]" sections of
the unit files.
After the symlinks have been created,  the systemd configuration is reloaded (in
a way that is equivalent to daemon-reload)  to ensure the changes are taken into
account immediately.
Note that this does not have the effect  of also starting any of the units being
enabled.
If this is desired,  either --now should be used together  with this command, or
an additional start command must be invoked for the unit.
Also  note that,  in case  of instance  enablement, symlinks  named the  same as
instances are  created in the  install location, however  they all point  to the
same template unit file.

This command will print the actions executed.
This output may be suppressed by passing --quiet.

Note that this operation creates only the suggested symlinks for the units.
While this command  is the recommended way to manipulate  the unit configuration
directory,  the administrator  is free  to make  additional changes  manually by
placing or removing symlinks in the directory.
This  is particularly  useful to  create  configurations that  deviate from  the
suggested default installation.
In this case, the administrator must  make sure to invoke daemon-reload manually
as necessary to ensure the changes are taken into account.

Enabling units should not be confused  with starting (activating) units, as done
by the start command.
Enabling and  starting units is orthogonal:  units may be enabled  without being
started and started without being enabled.
Enabling simply  hooks the unit into  various suggested places (for  example, so
that the  unit is  automatically started on  boot or when  a particular  kind of
hardware is plugged in).
Starting actually spawns the daemon process (in case of service units), or binds
the socket (in case of socket units), and so on.

Depending on whether --system, --user, --runtime, or --global is specified, this
enables the unit for  the system, for the calling user only,  for only this boot
of the system, or for all future logins of all users, or only this boot.
Note that in the last case, no systemd daemon configuration is reloaded.

Using enable on masked units results in an error.

## disable NAME...

Disables one or more units.
This  removes  all   symlinks  to  the  specified  unit  files   from  the  unit
configuration directory, and hence undoes the changes made by enable.
Note however  that this removes all  symlinks to the unit  files (i.e. including
manual additions), not just those actually created by enable.
This call implicitly  reloads the systemd daemon  configuration after completing
the disabling of the units.
Note  that this  command  does not  implicitly  stop the  units  that are  being
disabled.
If this is desired,  either --now should be used together  with this command, or
an additional stop command should be executed afterwards.

This command will print the actions executed. This output may be suppressed by passing --quiet.

This command honors --system, --user, --runtime and --global in a similar way as enable.

## start PATTERN...

Start (activate) one or more units specified on the command-line.

Note that glob patterns operate on the  set of primary names of currently loaded
units.
Units which are not active and are not in a failed state usually are not loaded,
and will not be matched by any pattern.
In addition,  in case  of instantiated  units, systemd is  often unaware  of the
instance name until the instance has been started.
Therefore, using glob patterns with start has limited usefulness.
Also, secondary alias names of units are not considered.

## stop PATTERN...

Stop (deactivate) one or more units specified on the command-line.

## reload PATTERN...

Asks all units listed on the command-line to reload their configuration.
Note  that this  will reload  the service-specific  configuration, not  the unit
configuration file of systemd.
If  you want  systemd  to reload  the  configuration  file of  a  unit, use  the
daemon-reload command.
In  other words:  for the  example  case of  Apache, this  will reload  Apache's
httpd.conf in the web server, not the apache.service systemd unit file.

This command should not be confused with the daemon-reload command.

## restart PATTERN...

Restart one or more units specified on the command-line.
If the units are not running yet, they will be started.

## status [PATTERN...|PID...]]

Show terse runtime status information about  one or more units, followed by most
recent log data from the journal.
If no units are specified, show system status.
If  combined  with  --all,  also  show  the status  of  all  units  (subject  to
limitations specified with -t).
If a PID is passed, show information about the unit the process belongs to.

This function is intended to generate human-readable output.
If you are looking for computer-parsable output, use show instead.
By default, this function only shows 10  lines of output and ellipsizes lines to
fit in the terminal window.
This can be changed with --lines and --full, see above.
In addition, journalctl --unit=NAME or journalctl --user-unit=NAME use a similar
filter for messages and might be more convenient.

#
#
#
# Issues
## I get a popup window every time I execute a `systemctl` command!

Prefix your command with `sudo(8)`.

You'll still be prompted for your password,  but only once per shell session and
without a popup window.

## My custom service is not executed!

For every executable you invoke, write a *full* path.

If that doesn't help, have a look at `$ journalctl -b`.
The service must have written why it failed.

##
# Todo
## Sometimes, when we shut down the system, it takes a long time (forever?).

Read:

   - `/usr/share/doc/systemd/README.Debian.gz`
     (press `-l` to get folding; read section "Debugging boot/shutdown problems")
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

Atm, here's the output of `$ systemctl list-jobs`:

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

I   think  you   need  to   edit  `/etc/default/grub`,   and  append   the  item
`systemd.debug-shell`  in  the  value   assigned  to  `GRUB_CMDLINE_LINUX`  (see
`/usr/share/doc/systemd/README.Debian.gz`), then run `$ sudo update-grub`.

For   more  info   about   the  difference   between  `GRUB_CMDLINE_LINUX`   and
`GRUB_CMDLINE_LINUX_DEFAULT`, see `info -f grub -n 'Simple configuration'`.

##
## Watch these videos

<https://www.youtube.com/watch?v=S9YmaNuvw5U>
<https://www.youtube.com/watch?v=tY9GYsoxeLg>
<https://www.youtube.com/watch?v=V0xoCA_qO58>

## try to install an xbindkeys service, and a `keyboard_setup.sh` service

We could ask it to reload its config.
This  would  be  useful  to  reload the  config  of  xbindkeys  after  modifying
`~/.config/keyboard/xbindkeys.conf`.

You could try this code in `~/.config/systemd/user/xbindkeys.service`:

    [Unit]
    Description=xbindkeys

    [Service]
    ExecStart=/usr/bin/xbindkeys -n -X :0.0 -f %h/.config/keyboard/xbindkeys.conf
    Restart=always

    [Install]
    WantedBy=graphical.target

Then, you would need to run `$ systemctl --user enable xbindkeys` and restart the system.
It seems to work on Ubuntu 16.04; but maybe not on Ubuntu 18.04, for the latter you may
need to replace `graphical.target` with `default.target`.

Note that  you need to  pass the `-n` flag  to xbindkeys; otherwise  the process
fails to be started.

However, there are several issues with this code.

First, we should not need to explicitly tell which display to use (`-X :0.0`);
xbindkeys should use the current value of `$DISPLAY`.
I tried to include the directive `PassEnvironment=DISPLAY`, but it didn't work.
I also tried to run `$ systemctl --user import-environment DISPLAY`, but it didn't work either
(maybe because I ran the command too early – in `~/.config/keyboard/setup.sh`).
I don't  know exactly what environment  does the previous command  refer to, but
you can inspect it by running `$ systemctl --user show-environment`.

Also, after editing your service file, you may need to run `$ systemctl --user daemon-reload`.

Another issue is that if you kill xbindkeys (or run `$ systemctl --user restart xbindkeys`),
all the programs that you have run via the latter are killed (terminal, tmux, webbrowser, ...).
I tried to run `$ systemctl --user reload xbindkeys`, but it didn't work.

    Failed to reload xbindkeys.service: Job type reload is not applicable for unit xbindkeys.service.
    See user logs and 'systemctl --user status xbindkeys.service' for details.

This link is also interesting: <https://superuser.com/a/1128905/913143>
It explains how to install an xbindkeys service.
Basically, it gives sth like:

    cat <<EOF >~/.config/systemd/user/xsession.target
    [Unit]
    Description=Xsession running
    BindsTo=graphical-session.target
    EOF

    cat <<EOF >~/.config/systemd/user/xbindkeys.service
    [Unit]
    Description=xbindkeys
    PartOf=graphical-session.target

    [Service]
    ExecStart=/usr/bin/xbindkeys -n -f %h/.config/keyboard/xbindkeys.conf
    Restart=always

    [Install]
    WantedBy=xsession.target
    EOF

    cat <<EOF >>~/bin/keyboard.sh
    systemctl --user import-environment PATH DBUS_SESSION_BUS_ADDRESS
    systemctl --no-block --user start xsession.target
    EOF

    systemctl --user enable xbindkeys

I'm not sure the added complexity is really useful though.
I'm also not sure that `graphical-session.target` really exists.
I can't find it in the output of `$ systemctl list-units -t target`.
Did the author mean `graphical.target`?
Note that this version needs you to run `systemctl --user start ...`;
our version doesn't  need to, provided that  you choose the right  target in the
`WantedBy` directive (default.target or graphical.target).

Here are a few other interesting links/commands:

    # Why do I need `--user-init`? https://unix.stackexchange.com/a/439616/289772
    $ journalctl --user-unit xbindkeys

To understand issue “Start request repeated too quickly”:
<https://serverfault.com/a/845473>

<https://askubuntu.com/a/859583/867754>

<https://wiki.archlinux.org/index.php/Systemd/User>

---

We have the same issue with `~/.config/keyboard/setup.sh`.
See the todo at the top.

And we probably have the same issue with xfce4-panel.
Suppose you restart it from a shell managed by tmux:

    $ xfce4-panel -r

I'm not sure but  I think that from now on, any program  started from it will be
polluted with tmux variables.
Make some tests to be sure.

## Find a way to dynamically get the current username from a unit file.

I don't think we can use $HOME.

## Find a way to version control our customizations of unit files.

For example, the files in:

    /etc/systemd/system/getty@.service.d/

## Convert `~/.config/keyboard/setup.sh` as a systemd service/timer.

Maybe we should do the same for everything in `~/bin/autostartrc`.

## ?

The new way of creating su(1)-like privileged sessions, which are fully isolated
from the original session is:

    $ sudo machinectl shell

Source:

<https://github.com/systemd/systemd/pull/1022>
<https://github.com/systemd/systemd/issues/825#issuecomment-127957710>
<https://github.com/systemd/systemd/issues/825#issuecomment-127917622>

However, the readline key bindings don't work.
Why?
I think the command starts this service:

    /usr/lib/systemd/system/rescue.service

It executes these commands:

    /bin/plymouth quit
    /bin/echo -e 'Welcome to rescue mode! After logging in, type "journalctl -xb" to view\\nsystem logs, "systemctl reboot" to reboot, "systemctl default" or ^D to\\nboot into default mode.'
    /bin/sh -c "/sbin/sulogin; /bin/systemctl --job-mode=fail --no-block default"

None of them suffer from this issue.
Where does the issue come from?
Try to remove as many directives as possible until the issue disappears.
Find a MWE.

Update: I think  that's because `sudo  machinectl shell`  starts sh (which  is a
symlink to dash).
You can check this by running:

    $ echo $SHELL
    /bin/sh~

You need to make `machinectl shell` start sh with the `-E` flag, to enable emacs
key bindings. I don't know how atm.
But even if you manage to do it, there's another issue:
our sh has been compiled without `--with-libedit`.
You would need to make `machinectl shell` start our custom sh installed in `~/.local/bin/dash`.
To understand how we produced this binary, in zshrc, read our comments above the `sh` alias.

## ?

<https://serverfault.com/a/617864>

    $ systemd-analyze critical-chain

    $ systemd-analyze plot > plot.svg
    $ display plot.svg

    $ systemd-analyze dot 'avahi-daemon.*' | dot -Tsvg > avahi.svg
    $ display avahi.svg

## We can't redirect the output of a service into a file.

We need a more recent version of systemd to use the StandardOutput directive.
<https://stackoverflow.com/a/43830129/9780968>

Otherwise, you may use a hack (`/bin/sh -c 'cmd >redir'`):
<https://stackoverflow.com/a/37595720/9780968>

## ?

    $ systemd-delta

It has a lot of output.
I wonder whether all those `[OVERRIDDEN]` are due to `usrmerge`.
If that's the case, and you need to clean the output:

    :sil exe 'g/ are identical$/.-2,.d_' | g/^$/d_

## Talk about the `--no-hostname` option:

    $ journalctl -b --no-hostname
                    ^^^^^^^^^^^^^

It's not available in ubuntu 16.04, but it is in 18.04.

It makes the  output more readable, because it removes  the hostname which gives
more room for the messages.

## Convert all commands inside `/etc/rc.local` into systemd services

## Document the purpose of the tor daemon which may be running on your machine

    tor --defaults-torrc /usr/share/tor/tor-service-defaults-torrc -f /etc/tor/torrc --RunAsDaemon 0

It can help  to torify a shell command  such as `$ pip install`,  when a package
can't be installed because of a network issue (AS blacklisted).

    $ . torsocks on
    $ python3 -m pip install --user requests

<https://tor.stackexchange.com/questions/12588/debian-tor-user-running-tor-in-the-background-from-startup#comment13069_12588>

If it's not running, you need to start the service manually:

    $ . torsocks on
    $ sudo systemctl start tor.service
    $ python3 -m pip install --user requests

torsocks - Access The Tor Network - Linux CLI: <https://www.youtube.com/watch?v=0uXFffq-UPU>

