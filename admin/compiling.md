## ?

    VERSION="$(git describe --tags --abbrev=0)"

---

Why `--tags`?

To avoid this kind of error:

    fatal: No annotated tags can describe 'ab18673731522c18696b9b132d3841646904e1bd'.

---

Why `--abbrev=0`?

Most of the time `$ git describe --tags` will return something like:

    v8.1.0648

But sometimes, it will return something like:

    v8.1.0648-1-gc8c884926

I think it happens  when the latest commit was not  tagged, which seems to
be always the case when Bram commits lots of changes in `$VIMRUNTIME`.

I prefer `v8.1.0648`.

---

Why is it important to always set the option `--prefix` with the value `/usr/local`?

If you don't, when you'll install the files obtained from the compilation, there
is a risk you overwrite the files of an existing package installed from Ubuntu's
repositories.

Note that if you can't write in  `/usr/local`, you may also use `$HOME`:

    $ ./configure --prefix=$HOME ...
                           ^^^^^

In this case, you need to make sure that `$HOME/bin` is in your `PATH`.

---

Instead of passing  options to `configure`, you can also  uncomment the relevant
lines in the Makefile, before running `./configure`.

## ?

    $ VERSION="9:${VERSION#v}"

---

What's this `9:`?

Atm, the  Vim packages in the  offical repositories have a  version number
which looks like this:

    2:8.0.0134-1ubuntu1~ppa1~x 500

The `2:` is what is called the *epoch*.
From: https://serverfault.com/a/604549

> This is a single (generally small) unsigned integer.
> It may be omitted, in which case zero is assumed.
> If it is omitted then the `upstream_version` may not contain any colons.
> It  is provided  to  allow  mistakes in  the  version  numbers of  older
> versions of a  package, and also a package's  previous version numbering
> schemes, to be left behind.

If you don't include  an epoch in the version of your Vim  package, `0:` will be
assumed:

    0:X.Y.Z

As a result, your package will be overwritten by `$ aptitude safe-upgrade`.

## ?

    $ make clean
    $ make distclean

## ?

Edit `/etc/apt/sources.list`.

Uncomment:

    deb-src http://fr.archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main restricted

Then run:

    $ sudo aptitude update
    $ sudo aptitude build-dep vim-gtk

## ?

    $ aptitude install libncurses5-dev \
      luajit libluajit-5.1-dev \
      libperl-dev \
      python-dev \
      python3-dev \
      ruby-dev

## ?

    $ ./configure --enable-cscope                                                    \
                --enable-fail-if-missing                                             \
                --enable-gui=gtk2                                                    \
                --enable-luainterp=dynamic                                           \
                --enable-multibyte                                                   \
                --enable-perlinterp=dynamic                                          \
                --enable-python3interp=dynamic                                       \
                --enable-pythoninterp=dynamic                                        \
                --enable-rubyinterp=dynamic                                          \
                --enable-terminal                                                    \
                --prefix=/usr/local                                                  \
                --with-compiledby=user                                               \
                --with-features=huge                                                 \
                --with-luajit                                                        \
                --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu  \
                --with-python3-config-dir=/usr/lib/python3.5/config-3.5m-x86_64-linux-gnu

## ?

    $ make

    $ xterm -e 'make test' &
                           │
                           └ useless in a script

## ?

*Use `--strip=no` for debugging.*

    $ sudo checkinstall --pkgname=vim --pkgversion="$VERSION" --spec=/dev/null --backup no -y
                                        │
                                        └ don't overwrite my package
                                          with an old version from the official repositories
                                          when I execute `aptitude safe-upgrade`

---

Why can aptitude overwrite our compiled package?

When aptitude  finds several candidates  for the  same package, it  checks their
version to decide which one is the newest.
By default, checkinstall uses the current date as the package version:

    20180914

This would cause an issue for Vim:

    $ apt-cache policy vim
    vim:~
      Installed: (none)~
      Candidate: 2:8.0.0134-1ubuntu1~ppa1~x~
      Version table:~
         2:8.0.0134-1ubuntu1~ppa1~x 500~
            500 http://ppa.launchpad.net/pi-rho/dev/ubuntu xenial/main amd64 Packages~
    ...~

Here the version of the Vim package in the ppa is `2:8.0.0134`.
If the version of our compiled package is `20180914`, it will be considered
older than the one in the ppa.
I think that's because the format of a date is different.
`apt` expects a number before a colon, but there's no colon in a date.
So it assumes that the date should be prefixed by `0:` or `1:` which gives:

    0:20180914
        <
    2:8.0.0134-1ubuntu1~ppa1~x

---

Why don't you use `--pkgname="my{PGM}"` anymore?

When  checkinstall tries  to install  `myPGM`, it  may try  to overwrite  a file
belonging to `PGM` (it  will probably happen if `PGM` is  already installed in a
different version).
If that happens, the installation will fail:

    dpkg: error processing archive /home/user/Vcs/zsh/zsh_9999.9999-1_amd64.deb (--install):~
     trying to overwrite '/usr/share/man/man1/zshmodules.1.gz', which is also in package myzsh 999-1~
    dpkg-deb: error: subprocess paste was killed by signal (Broken pipe)~

### ?

TODO: Sometimes, checkinstall ignores the options `--pkgversion`, `--pkgname`, ...

This is because if  it finds a .spec file at the root  of the project, and
its  basename matches  the  program  (e.g. ansifilter.spec,  weechat.spec,
...), then it uses its contents to assign the values of these options.
IOW, a {vim|tmux|...}.spec file has priority over `--pkg...`.

Besides, sometimes, the values in the .spec file are not literal.
For example, in `~/Vcs/weechat/weechat.spec:31`, one can read:

    Version:   %{version}
    Release:   %{release}

Currently, here are the repos which have a spec file:

   - ansifilter

     it overrides your `--pkgversion`, but this doesn't seem to cause an issue atm

   - jumpapp; issue, because of:

        3 -  Version: [ VERSION ]
        4 -  Release: [ 1%{?dist} ]

   - weechat; issue, because of:

        2 -  Name:    [ 0--name- ]
        3 -  Version: [  ]
        4 -  Release: [ %{release} ]

This can cause an issue, especially for the version field.
Note that for all these 3 projects, the spec file is intended for rpm, not
dpkg; this may explain the issue...

Solution1:

Use `--spec=/dev/null`.
This will prevent checkinstall from using any spec file.

You may think that checkinstall will still fall back on some other default spec file.
For example, if you read the logfile for Vim, you'll find these lines:

    Warning: .spec file path "/dev/null" not found.
    Warning: Defaulting to "vim.spec".

But in reality,  it seems that `/dev/null` *does* work  even though checkinstall
says that if falls back on a spec file.
Case in point:

    $ sudo checkinstall --pkgname=weechat --pkgversion=12.34 --spec=/dev/null --backup=no

You should  see that checkinstall  uses the package version  `12.34`, even
though the weechat spec file specifies a different version (2.5 atm).
If you remove `--spec=/dev/null`, you'll see  that checkinstall tries to use the
garbage version `%{version}`.

The fallback message comes from `/usr/bin/checkinstall:791`.
It's triggered by the non-existence of the file `$SPEC_PATH`.
If you search for the pattern `SPEC_PATH` in the script, you'll find 31 occurrences.
But only the first 7 are relevant.
The remaining ones are for foreign package managers (like rpm).
There are only 2 occurrences of `SPEC_PATH` after the one used in the warning message.

    [ -f SPEC_PATH ] && DEL_SPEC=0

    if [ -f "$SPEC_PATH" ]; then
    ...
      VERSION=`getparameter "^[Vv]ersion"`
    ...
    fi

None of them indicate that the script is going to use some spec file.

Solution2:
Test the existence of a spec file, and  if there's one, use sed to edit it
before invoking checkinstall.

Here's a first attempt to replace `%{name}` with `weechat`:

    $ sed '/^%define\s\+name/{s/.*\s//; h; s/^/%define name /}; /^Name:/{G; s/^\(Name:\s\+\)%{name}\n\(\w\+\)/\1\2/}' weechat.spec

It's a bit long, maybe we could improve the code...

## ?

Vim can be invoked with many commands.
We need to tell the system that, from now on, they're all provided by `/usr/local/bin/vim`.

    $ sudo update-alternatives --get-selections >"${LOGDIR}/update-alternatives-get-selections.bak"
    $ typeset -a names=(editor eview evim ex gview gvim gvimdiff rgview rgvim rview rvim vi view vim vimdiff)
    $ for name in "${names[@]}"; do
      sudo update-alternatives --log "${LOGFILE}" \
        --install /usr/bin/"${name}" "${name}" /usr/local/bin/vim 60
      sudo update-alternatives --log "${LOGFILE}" --set "${name}" /usr/local/bin/vim
    done

## ?

    grep -i 'mimetype' /usr/local/share/applications/gvim.desktop \
      | sed 's/mimetype=//i; s/;/ /g' \
      | xargs xdg-mime default gvim.desktop

---

What's this `gvim.desktop`?

A file installed by the Vim package.
It describes which files Vim can open in the line ‘MimeType=’.

---

What does this command do?

It parses the default `gvim.desktop` to build and run a command such as:

    $ xdg-mime default gvim.desktop text/english text/plain text/x-makefile ...

In effect, it makes gVim the default program to open various types of text files.
This matters when  using `xdg-open(1)` or double-clicking on the  icon of a file
in a GUI file manager.

---

Is it needed?

Once  the `gvim.desktop`  file is  installed, it  doesn't make  gVim the
default program for text files.
It just informs the system that gVim *can* open some of them.

##
# checkinstall
## How can I install the latest version of the script?

    $ git clone http://checkinstall.izto.org/checkinstall.git

    # from the INSTALL file
    $ make
    $ su
    $ make install
    $ checkinstall

##
## Which `make(1)` command does checkinstall run by default?

    $ make install

### How to pass it an arbitrary `make(1)` command?

Just write it right afterwards:

    $ sudo checkinstall make foo

Equivalent of `$  make install foo`, except  that a deb package  is produced and
installed via `$ dpkg -i foo`.

##
## The installation fails!  “trying to overwrite '...', which is also in package”

If you  know that  the file  which the package  was trying  to overwrite  is not
important, you can manually install the .deb generated by checkinstall:

    $ sudo dpkg -i --force-overwrite package.deb

Otherwise, you'll  have to uninstall  the conflicting package which  has already
installed the problematic file.

<https://askubuntu.com/q/176121/867754>

---

Alternatively, if  the path  of the  file ends  with `info/dir`,  try to  find a
configuration option allowing  you to change the location of  the file; it could
be `--infodir`.

Example:

    $ ./configure --infodir=/usr/local/share
                    ^^^^^^^^^^^^^^^^^^^^^^^^
                    move the info file from `/usr/share/info` to `/usr/local/share/info`

##
# debian source packages
## How to download a debian source package?

Find in which section the file is located:

    $ aptitude show <package> | grep Section

Uncomment the matching `deb-src` line in `/etc/apt/sources.list`.

Update:

    $ sudo aptitude update

Download the source package:

    $ apt-get source <package_name>

This will download the source code in a directory, as well as a few other files:

    vim-7.4.1689~
    vim_7.4.1689-3ubuntu1.debian.tar.xz~
    vim_7.4.1689-3ubuntu1.dsc~
    vim_7.4.1689.orig.tar.gz~

If  `$  apt-cache policy`  reports  several  versions,  you  can target  one  in
particular with:

    $ apt-get source <package_name>=<version>

### How to recompile it?

    $ dpkg-buildpackage -us -uc
                         │   │
                         │   └ do not sign the .changes file
                         └ do not sign the source package

You must  be in the source  code tree when you  run the command, and  the deb is
written in the parent directory (where the .dsc file lives), not the current one.

See the chapter 15 “Creating a Debian Package” in The Debian Administrator's Handbook.
More specifically the subchapter 15.1.3. “Starting the Rebuild”.

#### Should I apply the debian patches first?

No, they've been automatically applied by `$ apt-get source`:

    $ apt-get source vim
    ...~
    dpkg-source: info: applying 0001-Detect-the-rst-filetype-using-the-contents-of-the-fi.patch~
    dpkg-source: info: applying 0002-Support-sourcing-a-vimrc.tiny-when-Vim-is-invoked-as.patch~
    dpkg-source: info: applying 0003-Add-recognition-of-more-LaTeX-commands-for-tex-filet.patch~
    dpkg-source: info: applying 0004-Document-Debian-s-decision-to-disable-modelines-by-d.patch~
    dpkg-source: info: applying 0005-Support-defining-compilation-date-in-SOURCE_DATE_EPO.patch~
    dpkg-source: info: applying 0006-debsources.vim-Move-trusty-to-unsupported.patch~
    dpkg-source: info: applying ubuntu-grub-syntax.patch~
    dpkg-source: info: applying update-upstart-syntax.patch~
    dpkg-source: info: applying ubuntu-releases.patch~

#### Which package(s) will be compiled by the previous command?

Any package listed in:

    $ grep -i ^binary: *.dsc

##
## How to find
### the dependencies of a debian source package?

    $ grep -i build-depends: *.dsc
                               │
                               └ Debian Source Control

You can also find the information in the `debian/control` file.

#### Are they all necessary for a compilation?

Not necessarily.

The authoritative  resource on that matter  is the INSTALL file  or some similar
documentation provided by the project.

####
### the configuration options which were used to compile a debian source package?

Read the file `debian/rules`:

    $ vim rxvt-unicode-9.22/debian/rules

And find the right recipe (e.g. `conf-unicode-256color`):

    conf-unicode-256color:
            $(flagscommon) ./configure $(cfgcommon) \
                --enable-unicode3 \
                --enable-combining \
                --enable-xft \
                --enable-font-styles \
                --enable-256-color \
                --enable-pixbuf \
                --enable-transparency \
                --enable-fading \
                --enable-rxvt-scroll \
                --enable-next-scroll \
                --enable-xterm-scroll \
                --enable-perl \
                --enable-xim \
                --enable-iso14755 \
                --enable-mousewheel \
                --enable-slipwheeling \
                --enable-smart-resize \
                --enable-startup-notification \
                --with-term=rxvt-unicode-256color

---

See also: <https://wiki.debian.org/DebianPackageConfiguration>

---

Alternatively, you can try to read the buildlog on the web.

For example, for `zsh`, you would first visit:
<https://launchpad.net/ubuntu/+source/zsh>

Then, you would click on the button below “Latest upload”:
<https://launchpad.net/ubuntu/+source/zsh/5.5.1-1ubuntu3>

Then, on the button “amd64” in the section “Builds”:
<https://launchpad.net/ubuntu/+source/zsh/5.5.1-1ubuntu3/+build/16608683>

Finally, on the button “buildlog”:
<https://launchpadlibrarian.net/418666830/buildlog_ubuntu-disco-amd64.zsh_5.5.1-1ubuntu3_BUILDING.txt.gz>

##
## What happens if I pass the name of a binary package to `$ apt-get source`?

It will be replaced with the source package from which it can be compiled.

    $ apt-get source vim-gtk
    ...~
    Reading package lists... Done~
    Picking 'vim' as source package instead of 'vim-gtk'~

## I found a PPA.  Why do the names of its packages on the web differ from the packages I install on my system?

The package names you see on a page like this:
<https://launchpad.net/~pi-rho/+archive/ubuntu/dev>
... are for *source* packages.
You can  compile a  source code  with various  configuration options  to produce
different binaries.

For example, from the Vim source code, you can compile `vim-gtk` or `vim-tiny`.

    $ apt-get source vim
    $ vim -es vim-*/debian/control +'g/^Package/p' +'qa!'
    Package: vim-common~
    Package: vim-gui-common~
    Package: vim-runtime~
    Package: vim-doc~
    Package: vim-tiny~
    Package: vim~
    Package: vim-gtk~
    Package: vim-gtk3~
    Package: vim-nox~
    Package: vim-athena~
    Package: vim-gnome~
    Package: vim-gtk-py2~
    Package: vim-gtk3-py2~
    Package: vim-nox-py2~
    Package: vim-athena-py2~
    Package: vim-gnome-py2~

##
# Todo
## document `apt-src`, `autoapt`, `autodeb`

<https://wiki.debian.org/apt-src>
<https://help.ubuntu.com/community/AutoApt>
<https://wiki.ubuntu.com/AutoDeb>

auto-apt can find missing dependencies:

    $ auto-apt search Xlib.h
    usr/include/X11/Xlib.h  libdevel/libx11-dev~

But you need to update its database.

    $ sudo auto-apt update
    $ sudo auto-apt updatedb && sudo auto-apt update-local

And that takes a long time (≈ 25 min).
I don't know how often you have to update.
If you interrupt  an update with `C-c`, the utility  seems broken afterwards; it
doesn't find anything anymore, and you have to restart a complete update.

autodeb is an  experimental script that should perform the  job of both auto-apt
and checkinstall at the same time.

## learn how to create your own package (to avoid checkinstall which is a hack/too buggy)

<https://wiki.debian.org/HowToPackageForDebian>
<https://wiki.debian.org/Packaging>

---

    $ ar tv foo.deb

`ar` is used to create, modify, and extract from archives.

The `t` option lists the contents `foo.deb`.

The `v` modifier makes the operations verbose.
With `t`, it allows  you to see the modes, timestamp, owner,  group, and size of
the members.

---

The GNU ar program creates, modifies, and extracts from archives.
An archive is a  single file holding a collection of other  files in a structure
that makes it possible to retrieve the original individual files (called members
of the archive).

The original  files' contents, mode  (permissions), timestamp, owner,  and group
are preserved in the archive, and can be restored on extraction.

The paths  to the  elements of the  archive are stored  relative to  the archive
itself.

