# ?

    #!/bin/bash

    sudo update-alternatives --remove-all ee

    sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
      --slave /usr/local/bin/BB ff /usr/bin/nmap

    sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/paste 456 \
      --slave /usr/local/bin/CC gg /usr/bin/qmv \
      --slave /usr/local/bin/DD hh /usr/bin/rar

    sudo update-alternatives --set ee /usr/bin/make

    update-alternatives --query ee

    ls -l /usr/local/bin/{CC,DD} /etc/alternatives/{gg,hh}

# ?

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
        --slave /usr/local/bin/BB ff /usr/bin/nmap

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/paste 456 \
        --slave /usr/local/bin/CC gg /usr/bin/qmv \
        --slave /usr/local/bin/DD hh /usr/bin/rar

    $ sudo update-alternatives --set ee /usr/bin/make

    $ update-alternatives --query ee
    Name: ee~
    Link: /usr/local/bin/AA~
    Slaves:~
     ff /usr/local/bin/BB~
     gg /usr/local/bin/CC~
     hh /usr/local/bin/DD~
    Status: manual~
    Best: /usr/bin/paste~
    Value: /usr/bin/make~

    Alternative: /usr/bin/make~
    Priority: 123~
    Slaves:~
     ff /usr/bin/nmap~

    Alternative: /usr/bin/paste~
    Priority: 456~
    Slaves:~
     gg /usr/bin/qmv~
     hh /usr/bin/rar~

This shows how you should read the output of `update-alternatives --query`.
For the master:

   1. `Link`: alternative link
   2. `Name`: alternative name
   3. `Value`: alternative path

As an example, here, it gives:

   1. `/usr/local/bin/AA`
   2. `ee`
   3. `/usr/bin/make`

Which perfectly matches the links managed by `update-alternatives`:

    $ ls -l /usr/local/bin/AA
    lrwxrwxrwx 1 root root ... /usr/local/bin/AA -> /etc/alternatives/ee~
    $ ls -l /etc/alternatives/ee
    lrwxrwxrwx 1 root root ... /etc/alternatives/ee -> /usr/bin/make~

For a slave:

   1. `Slaves` (first block): name and link of the slave

   2. `Value`: master name
      (you need it to find the right block where the)

   3. `Slaves` (block of the master):
      line beginning with the slave name: slave path

As an example, here, it could give:

   1. `/usr/local/bin/BB`, `ff`
   2. `/usr/bin/make` (master to find the right slave)
   3. `/usr/bin/nmap`

Which, again, perfectly matches the links managed by `update-alternatives`:

    $ ls -l /usr/local/bin/BB
    lrwxrwxrwx 1 root root ... /usr/local/bin/BB -> /etc/alternatives/ff~
    $ ls -l /etc/alternatives/ff
    lrwxrwxrwx 1 root root ... /etc/alternatives/ff -> /usr/bin/nmap~

---

You shouldn't  read a  `Slaves:` section  the same  way when  it's in  the first
block, and when it's in another block.

In the first block, you should read the rhs *before* the lhs.
The next line, for example,  means that the alternative link `/usr/local/bin/BB`
points to the alternative name `/etc/alternatives/ff`:

    ff /usr/local/bin/BB~

In the other blocks, you should read the rhs *after* the lhs.
So this  line means that  the alternative name `/etc/alternatives/ff`  points to
the alternative path `/usr/bin/nmap`:

    ff /usr/bin/nmap~

---

Note that some slaves displayed in the first block should *not* be listed, because:

   - they're not associated to the current master path

   - they've been removed when we selected `/usr/bin/make`:

        $ ls -l /usr/local/bin/{CC,DD} /etc/alternatives/{gg,hh}
        ls: cannot access '/usr/local/bin/CC': No such file or directory~
        ls: cannot access '/usr/local/bin/DD': No such file or directory~
        ls: cannot access '/etc/alternatives/gg': No such file or directory~
        ls: cannot access '/etc/alternatives/hh': No such file or directory~

---

Usually in  practice, each path  candidate for the  master is associated  to the
same slaves; so, most of the time, you will probably run something like this:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
        --slave /usr/local/bin/BB ff /usr/bin/nmap
        --slave /usr/local/bin/CC gg /usr/bin/ping

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/paste 456 \
        --slave /usr/local/bin/BB ff /usr/bin/qmv
        --slave /usr/local/bin/CC gg /usr/bin/rar

Same number  of slaves (here  `2`), same slave  links (`/usr/local/bin/{BB,CC}`)
and same slave names (`ff` and `gg`).

---

Initially, slaves are associated to a path.
If the master  gets linked to this  path, the slaves are associated  to the path
*and* to the master.

# ?

Some definitions

`$ man update-alternatives` talks about `master` and `slave` links.
Example:

    $ update-alternatives --query awk
    Name: awk~
    Link: /usr/bin/awk~
    Slaves:~
     awk.1.gz /usr/share/man/man1/awk.1.gz~
     nawk /usr/bin/nawk~
     nawk.1.gz /usr/share/man/man1/nawk.1.gz~
    Status: manual~
    Best: /usr/local/bin/gawk~
    Value: /usr/local/bin/gawk~

    ...~

    Alternative: /usr/local/bin/gawk~
    Priority: 60~
    Slaves:~
     awk.1.gz /usr/local/share/man/man1/gawk.1.gz~

The master of the link group is:

    /usr/bin/awk

According to the `Value:` field, it currently points to `/usr/local/bin/gawk`.

One slave link is:

    /usr/share/man/man1/awk.1.gz

According to the `Slaves:` field of the `/usr/local/bin/gawk` alternative,
it currently points to `/usr/local/share/man/man1/gawk.1.gz`.

Usually the slave links are for manpages.

The master link determines how the slaves will be configured.

Also, a master link and its slaves make up a *link group*.

# ?

Some useful commands

    $ update-alternatives --install /usr/bin/editor editor /usr/local/bin/vim 1

Add  the alternative  `/usr/local/bin/vim` to  the  link group  whose master  is
`/usr/bin/editor`, with the priority 1.

---

    $ update-alternatives --remove editor /usr/local/bin/vim

Remove the alternative `/usr/local/bin/vim` from the group `editor`.
If the link group contains slave links (usually for manpages), they're updated
or removed.

---

    $ update-alternatives --set editor /usr/local/bin/vim

Configure `/usr/local/bin/vim` to be *the* alternative providing `editor`.

---

    $ update-alternatives --config editor

Configure the link group `editor` interactively.

---

    $ update-alternatives --auto editor

Reconfigure  the link  group  `editor` so  that,  from now  on,  it will  always
automatically use the alternative path with the highest priority.

---

    $ update-alternatives --display editor
    $ update-alternatives --query editor

Display  information  about the  link  group  `editor`;  useful to  check  which
alternative path provides `/usr/bin/editor`.

---

    $ update-alternatives --get-selections

Show:

   - each alternative name
   - in which mode they are (manual / auto)
   - the alternative path they're linked to

##
##
##
# What's the purpose of update-alternatives?

It maintains symbolic links which determine default commands.

##
# Why does `update-alternatives` use two symlinks between the link and path of an alternative (instead of one)?

    /usr/bin/editor
    → /etc/alternatives/editor
    → /usr/local/bin/vim

It allows the  OS to confine the changes  of the sysadmin to `/etc`,  which is a
good thing according to the FHS.
IOW, it creates a convenient centralised point of config.

# Where does update-alternatives store its state information (everything about the alternatives)?

In files inside the `/var/lib/dpkg/alternatives/` directory.

##
# What are the four most interesting options?

   * `--log`
   * `--force`
   * `--skip-auto`
   * `--verbose`

# Is there a specific order to respect for the options and the commands?

Yes,  according to  the synopsis  in  `$ man  update-alternatives`, the  options
should come before the command.
Unfortunately, both look the same: they all start with two hyphens.

##
# How to review all alternatives which are not configured in automatic mode?

    $ update-alternatives --skip-auto --all

# How to try and fix all broken alternatives?

    $ yes '' | update-alternatives --force --all

##
# How to add an alternative to a group link?

    $ sudo update-alternatives --install <link>  <name>  <path>  <priority>

If the group doesn't exist, it's created.

Example:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
        --slave /usr/local/bin/BB ff /usr/bin/nmap \
        --slave /usr/local/bin/CC gg /usr/bin/open

    $ ls -l /usr/local/bin/AA /etc/alternatives/ee
    lrwxrwxrwx 1 root root ... /etc/alternatives/ee -> /usr/bin/make~
    lrwxrwxrwx 1 root root ... /usr/local/bin/AA -> /etc/alternatives/ee~

# Which condition must be satisfied for `update-alternatives --install` to succeed?

The path of the alternative must exist, otherwise the command will fail:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/not_a_binary 123
    update-alternatives: error: alternative path /usr/bin/not_a_binary doesn't exist~

The link and the name of the alternative don't have to exist:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123
    update-alternatives: using /usr/bin/make to provide /usr/local/bin/AA (ee) in auto mode~

# How to remove a specific alternative from a group link?

    $ sudo update-alternatives --remove <name>  <path>

Example:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123
    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/paste 456

    $ update-alternatives --query ee
    Name: ee~
    Link: /usr/local/bin/AA~
    Status: auto~
    Best: /usr/bin/paste~
    Value: /usr/bin/paste~

    Alternative: /usr/bin/make~
    Priority: 123~

    Alternative: /usr/bin/paste~
    Priority: 456~

    $ sudo update-alternatives --remove ee /usr/bin/make
    $ update-alternatives --query ee
    Name: ee~
    Link: /usr/local/bin/AA~
    Status: auto~
    Best: /usr/bin/paste~
    Value: /usr/bin/paste~

    Alternative: /usr/bin/paste~
    Priority: 456~

# How to remove a group link?

    $ sudo update-alternatives --remove-all <name>

Example:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
        --slave /usr/local/bin/BB ff /usr/bin/nmap \
        --slave /usr/local/bin/CC gg /usr/bin/open

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/paste 456 \
        --slave /usr/local/bin/BB ff /usr/bin/qmv \
        --slave /usr/local/bin/CC gg /usr/bin/rar

    $ sudo update-alternatives --remove-all ee

The last command should have the same effect as:

    $ rm /usr/local/bin/{AA,BB,CC}
    $ rm /etc/alternatives/{ee,ff,gg}
    $ rm /var/lib/dpkg/alternatives/ee

##
##
##
# Description

update-alternatives creates,  removes, maintains and displays  information about
the symbolic links comprising the Debian alternatives system.

It is possible for several programs  fulfilling the same or similar functions to
be installed on a single system at the same time.
For example, many systems have several text editors installed at once.
This gives  choice to the users  of a system,  allowing each to use  a different
editor, if desired, but  makes it difficult for a program to  make a good choice
for an editor to invoke if the user has not specified a particular preference.

Debian's alternatives system aims to solve this problem.
An  alternative  link  in  the  filesystem is  shared  by  all  files  providing
interchangeable functionality.
The alternatives  system and the  system administrator together  determine which
actual file is referenced by this alternative link.
For  example,  if  the  text  editors   ed(1)  and  nvi(1)  are  both  installed
on  the  system,  the  alternatives  system  will  cause  the  alternative  link
`/usr/bin/editor` to refer to `/usr/bin/nvi` by default.
The  system  administrator   can  override  this  and  cause  it   to  refer  to
`/usr/bin/ed` instead, and  the alternatives system will not  alter this setting
until explicitly requested to do so.

The alternative link is not a direct symbolic link to the selected alternative.
Instead, it is a symbolic link to  a name in `/etc/alternatives/`, which in turn
is a symbolic link to the actual file referenced.
This is done  so that the system administrator's changes  can be confined within
the `/etc/` directory, which according to the FHS is a “Good Thing”.

When each package providing a file with a particular functionality is installed,
changed or  removed, update-alternatives is  called to update  information about
that file in the alternatives system.
update-alternatives is  usually called  from the  postinst (configure)  or prerm
(remove and deconfigure) scripts in Debian packages.

It is often useful for a number of alternatives to be synchronized, so that they
are changed as a  group; for example, when several versions  of the vi(1) editor
are  installed, the  man  page referenced  by `/usr/share/man/man1/vi.1`  should
correspond to the executable referenced by `/usr/bin/vi`.
update-alternatives handles  this by means of  master and slave links;  when the
master is changed, any associated slaves are changed too.
A master link and its associated slaves make up a link group.

Each link group is, at any given time, in one of two modes: automatic or manual.
When a  group is in automatic  mode, the alternatives system  will automatically
decide, as  packages are installed  and removed, whether  and how to  update the
links.
In  manual  mode,  the  alternatives  system  will  retain  the  choice  of  the
administrator and avoid changing the links (except when something is broken).

Link groups are in automatic mode when they are first introduced to the system.
If the  system administrator makes  changes to the system's  automatic settings,
this will  be noticed the  next time update-alternatives  is run on  the changed
link's group, and the group will automatically be switched to manual mode.

Each alternative has a priority associated with it.
When a link group  is in automatic mode, the alternatives  pointed to by members
of the group will be those which have the highest priority.

When  using the  `--config` option,  update-alternatives  will list  all of  the
choices for the link group of which given name is the master name.
The current choice is marked with a `*`.
You will then be prompted for your choice regarding this link group.
Depending on the choice made, the link group might no longer be in auto mode.
You will  need to use the  `--auto` option in  order to return to  the automatic
mode (or you can rerun `--config` and select the entry marked as automatic).

If  you want  to  configure non-interactively  you can  use  the `--set`  option
instead.

Different packages providing the same file need to do so cooperatively.
In other words,  the usage of update-alternatives is mandatory  for all involved
packages in such case.
It is not possible  to override some file in a package that  does not employ the
update-alternatives mechanism.

##
# Terminology

Since the  activities of update-alternatives  are quite involved,  some specific
terms will help to explain its operation.

## alternative link

A name,  like `/usr/bin/editor`, which  refers, via the alternatives  system, to
one of a number of files of similar function.

In `$ man update-alternatives`, it's also called “generic name”.

## alternative name

The name of a symbolic link in `/etc/alternatives/`.

## alternative path

The name of a specific file in  the filesystem, which may be made accessible via
an alternative link using the alternatives system.

In `$ man update-alternatives`, it's also simply called “alternative”.

## link group

A set of related symlinks, intended to be updated as a group.

## master link

The alternative link in a link group which determines how the other links in the
group are configured.

## slave link

An alternative link  in a link group  which is controlled by the  setting of the
master link.

## automatic mode

When a link group is in automatic mode, the alternatives system ensures that the
links in the group point to the alternative path with the highest priority.

## manual mode

When a link group  is in manual mode, the alternatives system  will not make any
changes to the system administrator's settings.

##
# Options
## --log file

Specifies  the  log  file  when  this  is  to  be  different  from  the  default
(`/var/log/alternatives.log`).

## --force

Allow replacing or dropping any real file that is installed where an alternative
link has to be installed or removed.

##
# Commands
## --install link name path priority [--slave link name path]...

Add a group of alternatives to the system.
Zero  or more  `--slave`  options,  each followed  by  three  arguments, may  be
specified.
Note that the path of the master alternative must exist or the call will fail.
However, if  the path of  a slave  alternative doesn't exist,  the corresponding
slave link will simply not be installed.
If some real file is installed where an alternative link has to be installed, it
is kept unless `--force` is used.

If the  alternative name specified  exists already in the  alternatives system's
records, the information supplied will be added as a new set of alternatives for
the group (one master and possibly one or several slaves).
Otherwise,  a  new  group, set  to  automatic  mode,  will  be added  with  this
information.
If the group is in automatic mode, and the newly added alternatives' priority is
higher than any  other installed alternatives for this group,  the symlinks will
be updated to point to the newly added alternatives.

## --set name path

Set the program `path` as alternative for `name`.
This is equivalent to `--config` but is non-interactive and thus scriptable.

## --remove name path

Remove  a path  candidate  for the  master alternative  and  all the  associated
slaves.
`name` is a name in `/etc/alternatives/`,  and `path` is an absolute filename to
which `name` could be linked.

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
        --slave /usr/local/bin/BB ff /usr/bin/nmap

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/paste 456 \
        --slave /usr/local/bin/CC gg /usr/bin/qmv \
        --slave /usr/local/bin/DD hh /usr/bin/rar

    $ ls -l /usr/local/bin/{CC,DD} /etc/alternatives/{gg,hh}
    lrwxrwxrwx 1 root root ... /etc/alternatives/gg -> /usr/bin/qmv~
    lrwxrwxrwx 1 root root ... /etc/alternatives/hh -> /usr/bin/rar~
    lrwxrwxrwx 1 root root ... /usr/local/bin/CC -> /etc/alternatives/gg~
    lrwxrwxrwx 1 root root ... /usr/local/bin/DD -> /etc/alternatives/hh~

    $ sudo update-alternatives --remove ee /usr/bin/paste
    $ ls -l /usr/local/bin/{CC,DD} /etc/alternatives/{gg,hh}
    ls: cannot access '/usr/local/bin/CC': No such file or directory~
    ls: cannot access '/usr/local/bin/DD': No such file or directory~
    ls: cannot access '/etc/alternatives/gg': No such file or directory~
    ls: cannot access '/etc/alternatives/hh': No such file or directory~

If `name`  is indeed linked to  `path`, it will  be updated to point  to another
appropriate  alternative (and  the  group is  put back  in  automatic mode),  or
removed if there is no such alternative left.
Associated slave links will be updated or removed, correspondingly.
If the link is not currently pointing  to `path`, no links are changed; only the
information about the alternative is removed.

## --remove-all name

Remove all alternatives and all of their associated slave links.
`name` is a name in `/etc/alternatives/`.

## --auto name

Switch the link group behind the alternative for `name` to automatic mode.
In the process,  the master symlink and  its slaves are updated to  point to the
highest priority installed alternatives.

## --display name

Display information about the link group:

   - the group's mode (auto or manual)

        editor - manual mode~

   - the master and slave links

        link editor is /usr/bin/editor~
        slave editor.1.gz is /usr/share/man/man1/editor.1.gz~

   - which path the master link currently points to

        link currently points to /usr/local/bin/vim~

   - what other paths are available (and their corresponding slaves)

        /bin/ed - priority -100~
          slave editor.1.gz: /usr/share/man/man1/ed.1.gz~
        /bin/nano - priority 40~
          slave editor.1.gz: /usr/share/man/man1/nano.1.gz~
        /usr/local/bin/vim - priority 60~
          slave editor.1.gz: /usr/local/share/man/man1/nvim.1.gz~

   - the highest priority alternative currently installed

        link best version is /usr/local/bin/vim~

## --get-selections

List all master names (those controlling a link group) and their status.

Each line contains up to 3 fields (separated by one or more spaces).
The first field  is the alternative name,  the second one is  the status (either
auto or manual), and the last one contains the current choice in the alternative
(beware: it's a filename and thus might contain spaces).

## --set-selections

Read configuration of alternatives on standard  input in the format generated by
`--get-selections` and reconfigure them accordingly.

## --query name

Display information about the link group in a machine parseable way.

## --list name

Display the list of paths to the alternatives of the link group.

## --config name

Show available alternatives for a link group and allow the user to interactively
select which one to use; the link group is updated.

##
# Query Format

The `--query`  format is  made of  `n +  1` blocks  where `n`  is the  number of
alternatives available in the queried link group.
The first block contains the following fields:

    Name: name

The name of the alternative.

    Link: link

The link of the alternative.

    Slaves: list-of-slaves

When this field is  present, the next lines hold all the names  and links of the
slaves associated to the master of the group link.
There is one slave per line.
Each line contains one space, the name of the slave, another space, and the link
of the slave.

    Status: status

The status of the link group (auto or manual).

    Best: best-choice

The path of the best alternative for this link group.
Not present if no alternatives are available.

    Value: currently-selected-alternative

The currently selected path for the master alternative.
It can also take the magic value none; used if the link doesn't exist.



The other blocks describe the available paths in the queried link group:

    Alternative: path-of-this-alternative

Path which can be selected for the alternative.

    Priority: priority-value

Current priority of this path.

    Slaves: list-of-slaves

When this field is  present, the next lines hold all the names  and paths of the
slaves associated to the master of the group link.
There is one slave per line.
Each line contains one space, the name of the slave, another space, and the path
of the slave.

Example:

    $ update-alternatives --query editor
    Name: editor~
    Link: /usr/bin/editor~
    Slaves:~
     editor.1.gz /usr/share/man/man1/editor.1.gz~
     editor.fr.1.gz /usr/share/man/fr/man1/editor.1.gz~
     editor.it.1.gz /usr/share/man/it/man1/editor.1.gz~
     editor.pl.1.gz /usr/share/man/pl/man1/editor.1.gz~
     editor.ru.1.gz /usr/share/man/ru/man1/editor.1.gz~
    Status: auto~
    Best: /usr/bin/vim.basic~
    Value: /usr/bin/vim.basic~

    Alternative: /bin/ed~
    Priority: -100~
    Slaves:~
     editor.1.gz /usr/share/man/man1/ed.1.gz~

    Alternative: /usr/bin/vim.basic~
    Priority: 50~
    Slaves:~
     editor.1.gz /usr/share/man/man1/vim.1.gz~
     editor.fr.1.gz /usr/share/man/fr/man1/vim.1.gz~
     editor.it.1.gz /usr/share/man/it/man1/vim.1.gz~
     editor.pl.1.gz /usr/share/man/pl/man1/vim.1.gz~
     editor.ru.1.gz /usr/share/man/ru/man1/vim.1.gz~

# Examples

There are several  packages which provide a text editor  compatible with vi, for
example nvi and vim.
Which one is used  is controlled by the link group vi,  which includes links for
the program itself and the associated manpage.

To display the  available packages which provide vi and  the current setting for
it, use the `--query` action:

    $ update-alternatives --query vi

To choose  a particular  vi implementation,  use this command  as root  and then
select a number from the list:

    $ update-alternatives --config vi

To go  back to  having the  vi implementation chosen  automatically, do  this as
root:

    $ update-alternatives --auto vi

