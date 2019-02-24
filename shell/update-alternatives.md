# Miscellaneous
## What's the purpose of update-alternatives?

It is possible for several programs  fulfilling the same or similar functions to
be installed on the system.
If another program needs to invoke these functions, it has to make a good choice
between all of these similar programs.

update-alternatives aims to solve this problem.

## Why does update-alternatives use two symlinks between the link and path of an alternative (instead of one)?

    /usr/bin/editor          → /etc/alternatives/editor
    /etc/alternatives/editor → /usr/local/bin/vim

It allows the  OS to confine the changes  of the sysadmin to `/etc`,  which is a
good thing according to the FHS.
IOW, it creates a convenient centralised point of config.

Indeed, once you've installed a group link, the first symlink doesn't change anymore:

    /usr/bin/editor → /etc/alternatives/editor

Only the second one can:

    /etc/alternatives/editor → /usr/local/bin/vim
    /etc/alternatives/editor → /usr/local/bin/emacs
    ...

## What's the specific order to respect when I pass options and a subcommand to update-alternatives?

According to  the synopsis  in `$ man  update-alternatives`, the  options should
come before the subcommand.
Unfortunately, both look the same: they all start with two hyphens.

`--slave` is an option of the subcommand `--install`; as such, it comes after.

##
# Terminology

Since the  activities of update-alternatives  are quite involved,  some specific
terms will help to explain its operation.

## alternative link

A symlink, like `/usr/bin/editor`,  which refers to one of a  number of files of
similar function.

In `$ man update-alternatives`, it's also called “generic name”.

## alternative name

The name of a symlink in `/etc/alternatives/`.

## alternative path

The name of a specific file in  the filesystem, which may be made accessible via
an alternative link using the alternatives system.

In `$ man update-alternatives`, it's also simply called “alternative”.

## link group

A set of related symlinks (master link + associated slave links), intended to be
updated as a group.

Its name is the name of the master alternative.

## master link

The alternative link in a link group which determines how the other links in the
group are configured.

## slave link

An alternative link  in a link group  which is controlled by the  setting of the
master link.

## automatic mode

When a link group is in automatic mode, the alternatives system ensures that the
master link points to the alternative path with the highest priority.

## manual mode

When a link group  is in manual mode, the alternatives system  will not make any
changes to the system administrator's settings.

##
# Getting info
## Where does update-alternatives write its activity?

    /var/log/alternatives.log

Unless you use the `--log` option:

    $ update-alternatives --log /tmp/log ...

##
## How to make `update-alternatives` verbose?

Use the `--verbose` option:

    $ update-alternatives --verbose ...

## How to print all choices for the master alternative path of the link group `editor`?

Use the `--list` subcommand:

    $ update-alternatives --list editor

## How to print the available programs which provide `editor`, and the one currently used?  (2)

Use the `--display` or `--query` subcommands:

    $ update-alternatives --display editor
    $ update-alternatives --query editor

### What's the difference between the 2 methods?

The output of `--display` is human-readable.
The output of `--query` is machine-parseable.

##
## How to print the list of all the names of master alternatives, and how they are currently configured?

    $ update-alternatives --get-selections

Each line contains 3 fields:

   1. alternative name
   2. status (either auto or manual)
   3. current choice for the alternative path

## How to save this list, then restore the configuration of all the alternatives according to this list?

Use the `--get-selections` and `--set-selections` subcommands:

    $ update-alternatives --get-selections >file
    $ sudo update-alternatives --set-selections <file

Usage example:

    # save update-alternatives' state info
    $ update-alternatives --get-selections >/tmp/state_info

    # temporarily modify state info
    $ sudo update-alternatives --set awk /usr/bin/mawk
    $ sudo update-alternatives --set editor /bin/nano
    $ update-alternatives --get-selections | grep 'awk\|^editor'
    awk                            manual   /usr/bin/mawk~
    editor                         manual   /bin/nano~

    # restore state info
    $ sudo update-alternatives --set-selections </tmp/state_info
    $ update-alternatives --get-selections | grep 'awk\|^editor'
    awk                            manual   /usr/local/bin/gawk~
    editor                         manual   /usr/local/bin/vim~

##
## I've installed a master alternative with 2 choices for the path, and some slave alternatives:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
        --slave /usr/local/bin/BB ff /usr/bin/nmap

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/paste 456 \
        --slave /usr/local/bin/CC gg /usr/bin/qmv \
        --slave /usr/local/bin/DD hh /usr/bin/rar

    $ sudo update-alternatives --set ee /usr/bin/make

### Here's the output of `update-alternatives --display`:

    $ update-alternatives --display ee
    ee - manual mode~
      link best version is /usr/bin/paste~
      link currently points to /usr/bin/make~
      link ee is /usr/local/bin/AA~
      slave ff is /usr/local/bin/BB~
      slave gg is /usr/local/bin/CC~
      slave hh is /usr/local/bin/DD~
    /usr/bin/make - priority 123~
      slave ff: /usr/bin/nmap~
    /usr/bin/paste - priority 456~
      slave gg: /usr/bin/qmv~
      slave hh: /usr/bin/rar~

#### What is its general structure?

It's divided into indented blocks; here, there are 3 of them.

The first block always describes the master alternative.

The other blocks always describe the available  paths in the link group, and the
slaves associated to each of them.

##### How to read the first block?

For the master alternative, the third and fourth lines are the most important ones:

      link currently points to /usr/bin/make~
      link ee is /usr/local/bin/AA~

This tells you that:

   - the *link* of the master alternative is `/usr/local/bin/AA`
   - the *name* of the master alternative is `ee`
   - the *path* of the master alternative is `/usr/bin/make`

Which perfectly matches the links managed by update-alternatives:

    $ ls -l /usr/local/bin/AA
    lrwxrwxrwx 1 root root ... /usr/local/bin/AA -> /etc/alternatives/ee~
    $ ls -l /etc/alternatives/ee
    lrwxrwxrwx 1 root root ... /etc/alternatives/ee -> /usr/bin/make~

##### How to read the other blocks?

For a  slave alternative, the  two lines beginning  with `slave <name>`  – where
`<name>` is the name of the alternative – are the most important ones:

    slave ff is /usr/local/bin/BB~
    slave ff: /usr/bin/nmap~

This tells you that:

   - the *link* of the slave alternative is `/usr/local/bin/BB`
   - the *name* of the slave alternative is `ff`
   - the *path* of the slave alternative is `/usr/bin/nmap`

Which, again, perfectly matches the links managed by update-alternatives:

    $ ls -l /usr/local/bin/BB
    lrwxrwxrwx 1 root root ... /usr/local/bin/BB -> /etc/alternatives/ff~
    $ ls -l /etc/alternatives/ff
    lrwxrwxrwx 1 root root ... /etc/alternatives/ff -> /usr/bin/nmap~

####
#### Why are the slaves `gg` and `hh` present in the first block, even though they're not used?

Their links need to be remembered in case they get used in the future.

#### What happens to the slave `ff` if I choose `/usr/bin/paste` as the master alternative path?

Its link and name will be removed.

    $ sudo update-alternatives --set ee /usr/bin/make
    $ ls -l /usr/local/bin/BB /etc/alternatives/ff
    ls: cannot access '/usr/local/bin/BB': No such file or directory~
    ls: cannot access '/etc/alternatives/ff': No such file or directory~

#### On which condition are the link and name of a slave removed when I change the path of a master alternative?

No slave associated to  the new master alternative path must  have the same link
and name.

Consider this:

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

If you choose `/bin/ed` instead of `/usr/bin/vim.basic`, the slaves `editor.{fr,it,pl,ru}`
will be removed, because the new master path has no such slaves:

    $ rm /usr/share/man/{fr,it,pl,ru}/man1/editor.1.gz \
         /etc/alternatives/editor.{fr,it,pl,ru}.1.gz

But the slave `editor.1.gz` will be kept; only its path will be updated:

    /usr/share/man/man1/editor.1.gz → /etc/alternatives/editor.1.gz
    /etc/alternatives/editor.1.gz   → /usr/share/man/man1/vim.1.gz
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                      new path

###
# Configuration
## Where does update-alternatives store its state information?

In files inside the `/var/lib/dpkg/alternatives/` directory.

##
## How to choose the path of the master alternative for the link group `editor`
### interactively?

Use the `--config` subcommand:

    $ update-alternatives --config editor

### non-interactively?

Use the `--set` subcommand:

    $ sudo update-alternatives --set editor /new/path

Example:

    $ update-alternatives --set editor /usr/local/bin/vim

##
## How to review all link groups?

    $ update-alternatives --all

### And automatically fix the broken alternatives?

    $ yes '' | update-alternatives --all --force
                                           │
                                           └ Allow replacing or dropping any real file that is installed
                                             where an alternative link has to be installed or removed.

### Review only the ones which are configured in manual mode?

    $ update-alternatives --all --skip-auto

##
## How to add an alternative path to the list of choices that a master alternative can be linked to?

    $ sudo update-alternatives --install <link>  <name>  <path>  <priority>

If the master link and name don't exist, they're created.

Example:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123

    $ ls -l /usr/local/bin/AA /etc/alternatives/ee
    lrwxrwxrwx 1 root root ... /etc/alternatives/ee -> /usr/bin/make~
    lrwxrwxrwx 1 root root ... /usr/local/bin/AA -> /etc/alternatives/ee~

### How to associate slave alternatives to this path?

Use the `--slave` option of the `--install` subcommand:

    $ sudo update-alternatives --install <link> <name> <path> <priority> \
        --slave <link> <name> <path> \
        --slave ...

You can specify one or more `--slave` options, each followed by three arguments.

Example:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
        --slave /usr/local/bin/BB ff /usr/bin/nmap \
        --slave /usr/local/bin/CC gg /usr/bin/open

### What happens if I use
#### a link which is already present in update-alternatives state info?

It fails:

    $ sudo update-alternatives --install /usr/local/bin/AA xx /usr/bin/a2ping 789
    update-alternatives: error: alternative link /usr/local/bin/AA is already managed by ee~

A link can *not* point to a new name.

#### a name which is already present in update-alternatives state info?

The old link is removed, and the new one is installed:

    $ sudo update-alternatives --install /usr/local/bin/XX ee /usr/bin/a2ping 789
    update-alternatives: renaming ee link from /usr/local/bin/AA to /usr/local/bin/XX~
    $ ls -l /usr/local/bin/AA
    ls: cannot access '/usr/local/bin/AA': No such file or directory~

A name *can* be targeted by a new link.

###
## How to remove a path choice for a master alternative?

    $ sudo update-alternatives --remove <name>  <path>

Example:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123
    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/paste 456

    $ update-alternatives --display ee
    ee - auto mode~
      link best version is /usr/bin/paste~
      link currently points to /usr/bin/paste~
      link ee is /usr/local/bin/AA~
    /usr/bin/make - priority 123~
    /usr/bin/paste - priority 456~

    $ sudo update-alternatives --remove ee /usr/bin/make
    $ update-alternatives --display ee
    ee - auto mode~
      link best version is /usr/bin/paste~
      link currently points to /usr/bin/paste~
      link ee is /usr/local/bin/AA~
    /usr/bin/paste - priority 456~

### What happens to the associated slave links?

They're updated or removed.

A slave link is updated if:

   - the removed path choice was used by the master alternative
   - its name is associated to the new selected path

Otherwise it's removed:

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
    # the slaves `gg` and `hh` have been correctly installed

    $ sudo update-alternatives --remove ee /usr/bin/paste
    $ ls -l /usr/local/bin/{CC,DD} /etc/alternatives/{gg,hh}
    ls: cannot access '/usr/local/bin/CC': No such file or directory~
    ls: cannot access '/usr/local/bin/DD': No such file or directory~
    ls: cannot access '/etc/alternatives/gg': No such file or directory~
    ls: cannot access '/etc/alternatives/hh': No such file or directory~
    # the slaves `gg` and `hh` don't exist anymore

### What happens if the master name is currently linked to this path?

The master name will be either:

   - updated to point to another appropriate  alternative (and  the  group is
     put back in automatic mode)

   - removed if there is no path choice left

## How to remove all path choices for a master alternative?

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

###
## Which condition must be satisfied for `update-alternatives --install` to succeed?

The path of the master alternative must exist, otherwise the command will fail:

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/not_a_binary 123
    update-alternatives: error: alternative path /usr/bin/not_a_binary doesn't exist~

OTOH, its link and name don't have to exist:

    $ sudo update-alternatives --install /usr/local/bin/not_a_binary not_a_name /usr/bin/make 123
    update-alternatives: using /usr/bin/make to provide /usr/local/bin/AA (ee) in auto mode~

---

If  the path  of  a slave  alternative  doesn't exist,  the  command will  still
succeed, but the corresponding slave link won't be installed.

    $ sudo update-alternatives --install /usr/local/bin/AA ee /usr/bin/make 123 \
        --slave /usr/local/bin/BB ff /usr/bin/not_a_binary
    update-alternatives: using /usr/bin/make to provide /usr/local/bin/AA (ee) in auto mode~
    update-alternatives: warning: skip creation of /usr/local/bin/BB because associated file /usr/bin/not_a_binary (of link group ee) doesn't exist~

## How to overwrite a file located where I want an alternative link to be installed?

Use the `--force` option.

Example without `--force`:

    $ echo 'hello' | sudo tee /usr/local/bin/file
    $ sudo update-alternatives --install /usr/local/bin/file ee /usr/bin/make 123
    update-alternatives: using /usr/bin/make to provide /usr/local/bin/file (ee) in auto mode~
    update-alternatives: warning: not replacing /usr/local/bin/file with a link~
    $ ls -l /usr/local/bin/file
    -rw-r--r-- 1 root root ... /usr/local/bin/file~

Example using `--force`:

    $ sudo update-alternatives --remove-all ee
    $ echo 'hello' | sudo tee /usr/local/bin/file
                               vvvvvvv
    $ sudo update-alternatives --force --install /usr/local/bin/file ee /usr/bin/make 123
    update-alternatives: using /usr/bin/make to provide /usr/local/bin/file (ee) in auto mode~
    $ ls -l /usr/local/bin/file
    lrwxrwxrwx 1 root root ... /usr/local/bin/file -> /etc/alternatives/ee~

---

Note that the alternative is partially installed, even without `--force`.
But since the link is not installed, it won't work as expected.

###
## How to make the link group `editor` switch to automatic mode?

    $ update-alternatives --auto editor

In the process, the  links of the master alternative is updated  to point to the
alternative path choice with the highest priority; the slaves are also updated.

---

You could also rerun `--config` and select the entry marked as automatic.

##
##
##
# Description

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

Different packages providing the same file need to do so cooperatively.
In other words,  the usage of update-alternatives is mandatory  for all involved
packages in such case.
It is not possible  to override some file in a package that  does not employ the
update-alternatives mechanism.

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
slaves associated to the master of the link group.
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
slaves associated to the master of the link group.
There is one slave per line.
Each line contains one space, the name of the slave, another space, and the path
of the slave.
