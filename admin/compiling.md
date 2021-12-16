# How to remove the files generated during the last compilation?

    $ make clean; make distclean

##
# What should I do when the compilation fails because of some missing dependencies?

Run:

    $ apt build-dep PGM

---

Before that, you may need to edit `/etc/apt/sources.list`, and uncomment:

    deb-src http://fr.archive.ubuntu.com/ubuntu/ xenial main restricted

Note that you need to replace `xenial` with the actual codename of your Ubuntu OS as given by:

    $(lsb_release -sc)

And you need  to replace `main restricted` with the  section of the repositories
from which the program can be installed; you can get it by running:

      $ apt policy PGM

Example:

      $ apt policy weechat
      ...˜
           1.4-2 500˜
              500 http://fr.archive.ubuntu.com/ubuntu xenial/universe amd64 Packages˜
                                                      ^-------------^

Then, run `$ sudo apt update`.

##
# How to make sure `make install` installs all the files under `/usr/local`?

It depends on the program you're compiling.
Often, the `configure` script supports a `--prefix` option:

    $ ./configure --prefix=/usr/local ...
                  ^-----------------^

Otherwise, try to  uncomment and edit the relevant line  in the Makefile, before
running `./configure`.

## Why is it important to do so?

To  avoid  a  conflict  with  a  file  of  a  package  installed  from  Ubuntu's
repositories.

## What should I check if I install the files under my home directory?

Make sure that `$HOME/bin` is in your `PATH`.

##
# Installing the compiled binary as a deb package
## How to get the version of the binary?

Assuming it's version-controlled by git:

    $ git describe --tags --abbrev=0

---

`--tags` is useful to avoid this kind of error:

    fatal: No annotated tags can describe 'ab18673731522c18696b9b132d3841646904e1bd'.

From `man git-describe`:

   > --tags
   >    Instead of  using only the annotated  tags, use any tag  found in refs/tags
   >    namespace. This option enables matching a lightweight (non-annotated) tag.

---

`--abbrev=0` is useful to truncate a long tag.
For example, in Vim, sometimes, `$ git describe --tags` outputs:

    v8.1.0648-1-gc8c884926

I think  it happens when  the latest  commit was not  tagged, which seems  to be
always the case when Bram commits lots of changes in `$VIMRUNTIME`.

With `--abbrev=0`, the output is truncated to:

    v8.1.0648

---

If you need to remove a non-numerical prefix, like `v`, use a parameter expansion:

    $ echo ${$(git describe --abbrev=0)#v}
           ^^                          ^-^

See `man bash /Parameter Expansion/;/${parameter#word}`.

## How to prevent the package from being replaced by another version during an `apt upgrade`?

You need to assign a recent version  number to your package, otherwise it may be
replaced in the future during an `$  apt upgrade`, by a more recent package from
the official repositories.

Besides, you may need to prefix the version number with a big enough epoch.

For example, atm, the Vim package in the offical repository has a version number
which looks like this:

    2:8.0.0134-1ubuntu1~ppa1~x 500
    ^^

The `2:` is called the **epoch**:

   > This is a single (generally small) unsigned integer.
   > It may be omitted, in which case zero is assumed.
   > If it is omitted then the `upstream_version` may not contain any colons.
   > It  is provided  to  allow  mistakes in  the  version  numbers of  older
   > versions of a  package, and also a package's  previous version numbering
   > schemes, to be left behind.

Source: <https://serverfault.com/a/604549>

If you don't include an epoch in the version of your package, `0:` is assumed:

    0:X.Y.Z
    ^^

Now, suppose that you install a package built locally under the version `4.5.6`,
while the official repo contains the same package under the version `2:1.2.3`.
When you'll upgrade your system, your local  package will be replaced by the one
from the official repo, even if it's actually older; simply because its epoch is
bigger.

##
# debian source packages
## How to download a debian source package?

Find in which section the file is located:

    $ apt show <package> | grep Section

Uncomment the matching `deb-src` line in `/etc/apt/sources.list`.

Update:

    $ sudo apt update

Download the source package:

    $ apt source <package_name>

This will download the source code in a directory, as well as a few other files:

    vim-7.4.1689˜
    vim_7.4.1689-3ubuntu1.debian.tar.xz˜
    vim_7.4.1689-3ubuntu1.dsc˜
    vim_7.4.1689.orig.tar.gz˜

If `$  apt policy` reports  several versions, you  can target one  in particular
with:

    $ apt source <package_name>=<version>

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

No, they've been automatically applied by `$ apt source`:

    $ apt source vim
    ...˜
    dpkg-source: info: applying 0001-Detect-the-rst-filetype-using-the-contents-of-the-fi.patch˜
    dpkg-source: info: applying 0002-Support-sourcing-a-vimrc.tiny-when-Vim-is-invoked-as.patch˜
    dpkg-source: info: applying 0003-Add-recognition-of-more-LaTeX-commands-for-tex-filet.patch˜
    dpkg-source: info: applying 0004-Document-Debian-s-decision-to-disable-modelines-by-d.patch˜
    dpkg-source: info: applying 0005-Support-defining-compilation-date-in-SOURCE_DATE_EPO.patch˜
    dpkg-source: info: applying 0006-debsources.vim-Move-trusty-to-unsupported.patch˜
    dpkg-source: info: applying ubuntu-grub-syntax.patch˜
    dpkg-source: info: applying update-upstart-syntax.patch˜
    dpkg-source: info: applying ubuntu-releases.patch˜

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
## What happens if I pass the name of a binary package to `$ apt source`?

It will be replaced by the source package from which it can be compiled.

    $ apt source vim-gtk
    ...˜
    Reading package lists... Done˜
    Picking 'vim' as source package instead of 'vim-gtk'˜

## I found a PPA.  Why do the names of its packages on the web differ from the packages I install on my system?

The package names you see on a page like this:
<https://launchpad.net/~pi-rho/+archive/ubuntu/dev>
... are for *source* packages.
You can  compile a  source code  with various  configuration options  to produce
different binaries.

For example, from the Vim source code, you can compile `vim-gtk` or `vim-tiny`.

    $ apt source vim
    $ vim -es vim-*/debian/control +'g/^Package/p' +'qa!'
    Package: vim-common˜
    Package: vim-gui-common˜
    Package: vim-runtime˜
    Package: vim-doc˜
    Package: vim-tiny˜
    Package: vim˜
    Package: vim-gtk˜
    Package: vim-gtk3˜
    Package: vim-nox˜
    Package: vim-athena˜
    Package: vim-gnome˜
    Package: vim-gtk-py2˜
    Package: vim-gtk3-py2˜
    Package: vim-nox-py2˜
    Package: vim-athena-py2˜
    Package: vim-gnome-py2˜

##
# checkinstall
## What are some of its pitfalls?
### It contains many errors.

Atm, shellcheck only finds one error:

    $ shellcheck -f gcc $(which checkinstall)
    /usr/bin/checkinstall:1364:10: note: The mentioned syntax error was in this if expression. [SC1009]˜
    /usr/bin/checkinstall:1364:13: error: Couldn't parse this test expression. Fix to allow more checks. [SC1073]˜
    /usr/bin/checkinstall:1364:24: error: You need a space before the ]. [SC1020]˜
    /usr/bin/checkinstall:1364:24: error: Missing space before ]. Fix any mentioned problems and try again. [SC1072]˜

But that's because this error prevents shellcheck from parsing the file correctly.
If you correct it:

     if [ $? -gt 0]; then
     →
     if [ $? -gt 0 ]; then
                  ^

shellcheck finds 636 errors:

    $ shellcheck -f gcc /usr/bin/checkinstall | wc -l
    636˜

### It leaves a deb package behind.

This  is actually  useful if  you  intend to  install  it later  on a  different
machine; but otherwise it just takes space.

For example, the mpv binary weighs 22M (if stripped).
So,  as you  can see,  the  weights of  packages can  quickly  add up  to a  non
negligible amount of space.

### It creates an archive to backup all overwritten files.

And every time you reinvoke checkinstall, a new archive is created.
This adds up and can quickly amount to a fair amount of space.

To prevent this, you need to use the `--backup=no` option.

### It seems to create files under `/usr/share/doc` no matter what.

Even if you use the prefix `/usr/local`.

This is untidy  if you want *all*  files to be installed  under `/usr/local`, to
avoid any conflict with a system package.

###
### By default, it strips the binary from its debugging symbols.

This prevents you from getting a meaningful backtrace in case of a crash.

#### Solution:

To fix that, you need to use the `--strip=no` option.

This shows that  checkinstall alters your compilation in various  ways, and make
your  binary behave  unexpectedly; and  understanding that  checkinstall is  the
cause of an unexpected behavior is not always easy, nor is it easy to fix it.

###
### Sometimes, it ignores the options `--pkgversion`, `--pkgname`, ...

This  is because  if  it  finds a  `.spec`  file at  the  root  of the  project,
and  its basename  matches  the  name of  the  program (e.g.  `ansifilter.spec`,
`weechat.spec`, ...),  then it uses its  contents to assign the  values of these
options; IOW, a `.spec` file has priority over `--pkg...`.

Besides, sometimes, the values in the `.spec` file are not literal.
For example, in `~/Vcs/weechat/weechat.spec:31`, one can read:

    Version:   %{version}
    Release:   %{release}

This can cause an issue, especially for the version field.
Note that  in the  weechat example, the  `.spec` file is  intended for  rpm, not
dpkg, which creates an additional issue.

#### Solution1:

Use `--spec=/dev/null`.

This will prevent checkinstall from using any `.spec` file.

You may think that checkinstall will still fall back on some other default `.spec` file.
For example, when running checkinstall to install Vim, its output contains these lines:

    Warning: .spec file path "/dev/null" not found.˜
    Warning: Defaulting to "vim.spec".˜

But in reality,  it seems that `/dev/null` *does* work  even though checkinstall
says that if falls back on a `.spec` file.
Case in point:

    $ sudo checkinstall --pkgname=weechat --pkgversion=12.34 --spec=/dev/null

You should see  that checkinstall uses the package version  `12.34`, even though
the weechat `.spec` file specifies a different version (2.5 atm).
If you remove `--spec=/dev/null`, you'll see  that checkinstall tries to use the
wrong version `%{version}`.

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

#### Solution2:

Test the  existence of a `.spec`  file, and if there's  one, use sed to  edit it
before invoking checkinstall.

Here's a first attempt to replace `%{name}` with `weechat`:

    $ sed '/^%define\s\+name/{s/.*\s//; h; s/^/%define name /}; /^Name:/{G; s/^\(Name:\s\+\)%{name}\n\(\w\+\)/\1\2/}' weechat.spec

It's a bit long; maybe the code could be improved.

###
### When used interactively, you can't use readline commands to edit your input.
#### Solution:

Use rlwrap:

    $ sudo rlwrap checkinstall ...

##
## How can I install the latest version of the script?

    $ git clone http://checkinstall.izto.org/checkinstall.git

    # from the INSTALL file
    $ make
    $ su
    $ make install
    $ checkinstall

##
## In general, what information should I provide to checkinstall?

At the very least, you'll need to give a name and a version to the package.

The name is important because it's the one you'll have to use later whenever you
want to manipulate the package via `dpkg(1)` or `apt(8)`.

The version is  important because if it's not recent  enough, your local package
may be replaced later during an `apt upgrade`.

### How to provide them
#### interactively?

When prompted with:

    Enter a number to change any of them or press ENTER to continue:

Type `2`, then provide the desired name for your package:

    Enter new name:
    >>

Then, type `3`, and provide the desired version:

    Enter new version:
    >>

#### from the command-line?

Use the `--pkgname` and `--pkgversion` options.

###
### Why shouldn't I give an ad-hoc name to my package?

Suppose you're trying to compile and  install zsh via checkinstall, and you name
the package `myzsh`; and suppose that zsh is already installed on your system in
a different version.

checkinstall may fail to install your  local package, because it can't overwrite
some file(s) belonging to the `zsh` package:

    dpkg: error processing archive /home/user/Vcs/zsh/zsh_9999.9999-1_amd64.deb (--install):˜
     trying to overwrite '/usr/share/man/man1/zshmodules.1.gz', which is also in package myzsh 999-1˜
    dpkg-deb: error: subprocess paste was killed by signal (Broken pipe)˜

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
                    ^----------------------^
                    move the info file from `/usr/share/info` to `/usr/local/share/info`

##
# Todo
## document `apt-src`, `autoapt`, `autodeb`

- <https://wiki.debian.org/apt-src>
- <https://help.ubuntu.com/community/AutoApt>
- <https://wiki.ubuntu.com/AutoDeb>

auto-apt can find missing dependencies:

    $ auto-apt search Xlib.h
    usr/include/X11/Xlib.h  libdevel/libx11-dev˜

But you need to update its database.

    $ sudo auto-apt update
    $ sudo auto-apt updatedb && sudo auto-apt update-local

And that takes a long time (≈ 25 min).
I don't know how often you have to update.
If you interrupt  an update with `C-c`, the utility  seems broken afterwards; it
doesn't find anything anymore, and you have to restart a complete update.

autodeb is an  experimental script that should perform the  job of both auto-apt
and checkinstall at the same time.

## learn how to create your own package

To avoid:

   - checkinstall which is a hack/too buggy

   - `$ sudo make install` which is untidy

     in particular, it's hard to remove all files installed by `make(1)`:
     you need to get back to the repo, run `$ sudo make uninstall`,
     and hope that the recipe correctly removes all the files

---

- <https://wiki.debian.org/HowToPackageForDebian>
- <https://wiki.debian.org/Packaging>
- <https://github.com/mpv-player/mpv-build#instructions-for-debian--ubuntu-package>

---

    $ ar tv foo.deb

`ar` is used to create, modify, and extract from archives.

The `t` option lists the contents `foo.deb`.

The `v` modifier makes the operations verbose.
With `t`, it  lets you see the  modes, timestamp, owner, group, and  size of the
members.

---

The GNU ar program creates, modifies, and extracts from archives.
An archive is a  single file holding a collection of other  files in a structure
that makes it possible to retrieve the original individual files (called members
of the archive).

The original  files' contents, mode  (permissions), timestamp, owner,  and group
are preserved in the archive, and can be restored on extraction.

The paths  to the  elements of the  archive are stored  relative to  the archive
itself.

## implement a zsh function listing all the locally compiled packages currently installed on our system

Similar to `checkinstall_what_have_i_installed`.

