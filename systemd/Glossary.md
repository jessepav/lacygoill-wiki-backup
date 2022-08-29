# d
## directive

Inside a  section in a unit  file, sets a  unit parameter which specifies  how a
resource should be handled on the system:

    [Section]
    Parameter=value
    ^-------------^
       directive

It can also specify some metadata (like a URL to some documentation).

###
## drop-in
### directory

The contents of  a `.conf` file in  such a directory is  automatically parsed to
extend the configuration of a given unit.

The name of its last path component is: `<unit>.d`.
Example:

    /etc/systemd/system/apache2.service.d/
                        ^----------------^

"drop-in" means that you can **drop** a file **in** the directory without having
to worry  about merging your  new configuration  with the existing  one. systemd
will take  care of that.  Even  better, your configuration will  be preserved no
matter what; even if a system update overwrites the original unit file.

### file

File with the suffix `.conf` in a drop-in directory.

It must contain appropriate section headers.
That is,  you can't just  write a  directive in there,  without the name  of the
section to which it belongs.

##
# s
## section

The first organization level in a unit file.
A section contains one or several directives, and terminates at the start of the
next section (or at the end of the file).

Example:

    [Section A]
    KeyOne=value 1
    KeyTwo=value 2
    ...

    [Section B]
    ...

    [Section C]
    ...

##
# t
## types (of units/unit files)
### device

Encode information about a device.

Can be used to start a service when  a particular type of hardware is plugged in
or becomes available.

### path

Start a service when a particular file/directory is accessed.

systemd uses `inotify(7)` to monitor the file/directory.

---

As an example, the `cups.path` unit automatically starts the `cups.service` unit
as soon as the `/var/cache/cups/org.cups.cupsd` file exists:

    $ systemctl cat cups.path | grep -i 'PartOf\|PathExists'
    PartOf=cups.service
    PathExists=/var/cache/cups/org.cups.cupsd

###
### mount

Mount a partition during the system boot.

### automount

Mount a partition when you enter its mount point via a file manager, or via `cd`.

###
### scope

Manage a set of system processes.

Unlike a  service unit, a scope  unit manages externally created  processes, and
does not fork off processes on its own.

Its purpose  is to group worker  processes of a system  service for organization
and for managing resources.

Even though a  scope unit is named like  a file, it's not configured  via a unit
file;  instead,  it's  created  programmatically using  the  bus  interfaces  of
systemd.

### service

Configure a service.

It replaces  an old-fashioned init  shell script that was  used on old  System V
systems.

### slice

Configure cgroups.

### socket

Create a socket which enables communication between different system services.

It can also wake up a sleeping service when it receives a connection request.

### swap

Encode information about a swap partition controlled and supervised by systemd.

###
### target

Group other units for a particular purpose.

It also  provides a  well-known synchronization point,  relative to  which other
units can be started.  For example, a unit `foo` can specify that it wants to be
started before or  after a target `bar`. `bar` provides  a synchronization point
to which `foo` can refer to in a `Before=` or `After=` directive.

### timer

Schedule jobs (similar to the cron system).

##
# u
## unit

A standardized representation of some system  resource that systemd knows how to
operate on and manage.

As an example, a unit can be a service or a listening socket.

### active state

A given active state is available to *any* type of unit.

It's printed in the `ACTIVE` column in the output of `systemctl list-units`.
It answers these questions: "Is this unit active?  If not, why?"
It can be:

   - active
   - inactive

   - failed

   - activating
   - deactivating
   - reloading

#### active

The unit has been "started" successfully.

###
### load state

A given load state is available to *any* type of unit.

It's printed in the `LOAD` column in the output of `systemctl list-units`.
It answers these questions: "Is this unit loaded?  If not, why?"
It can be:

   - loaded

   - bad-setting
   - error
   - masked
   - not-found

#### loaded

Systemd has read the configuration of this unit from disk into memory.

This happens when the unit is being  interacted with (e.g. started, or even with
a simple `list-units`), or  when it's called in as a  dependency of another unit
that is being loaded.

###
### substate

A given substate is only available to a *specific* type of unit.

It's printed in the `SUB` column in the output of `systemctl list-units`.

###
## unit file

A configuration file implementing a unit.

There  are various  types of  unit  files; each  of  them is  identified by  its
filename extension.

### states
#### enabled

Unit file  for which  a set  of symlinks have  been created,  as encoded  in the
"[Install]" section of  the relevant unit file.  Their purpose  is, for example,
to automatically start the  unit on boot, or when a  particular kind of hardware
is plugged in.

---

There is no relationship between an enabled unit file and an active unit.

Those states are orthogonal.
A unit file might be enabled without its unit being active.
A unit might be active without its file being enabled.

Enabling a unit file creates a set of symlinks.
Activating a unit actually spawns a daemon  process (in case of a service unit),
or binds a socket (in case of a socket unit), and so on.

#### static

Unit  file  which  can neither  be  enabled  nor  disabled  (because it  has  no
provisions for enabling in the "[Install]" section).
Rather, another unit will call it in as a dependency.

#### transient

Unit file which has been created dynamically with the runtime API.
It cannot be enabled.

###
### watchdog (timer)

There are 2 kinds of watchdogs: hardware and software.
Their  purpose is  to prevent  boundless hangs,  either of  the system  or of  a
particular service.

Technically, a watchdog starts a short  timer whose callback restarts the system
or a  process.  During normal operation,  the timer should never  elapse and run
its callback; instead,  the supervised system/process is meant to  send a signal
that it's still alive.  Upon reception of this signal, the watchdog restarts its
timer.
