# How to make zathura the default reader for pdfs and epubs?

    $ xdg-mime default "$(basename "$(locate -r '.*zathura.*pdf.*\.desktop')")" \
        application/pdf \
        application/epub+zip

Tip: Prefix the  command with `echo` first,  to check the validity  of the final
command which is going to be executed.

      v--v
    $ echo xdg-mime default "$(basename "$(locate -r '.*zathura.*pdf.*\.desktop')")" \
            application/pdf \
            application/epub+zip

# Where is zathura's issue tracker?

<https://git.pwmt.org/pwmt/zathura/issues>

##
# Plugins
## How to add support for djvu files?  comic books files?  postscript files?

Install these plugins:

    $ sudo aptitude install zathura-djvu
    $ sudo aptitude install zathura-cb
    $ sudo aptitude install zathura-ps

## How to see the paths to all the plugins used by zathura?

    $ zathura --version
    zathura 0.3.5˜
    (plugin) ps (0.2.3) (/usr/lib/zathura/ps.so)˜
    (plugin) djvu (0.2.5) (/usr/lib/zathura/djvu.so)˜
    (plugin) pdf-mupdf (0.3.1) (/usr/lib/zathura/pdf.so)˜
    (plugin) cb (0.1.5) (/usr/lib/zathura/cb.so)˜

Here, you can see that we have 4 plugins, to read:

   - postscript files
   - djvu files
   - pdf (and epub) files
   - comic book files

##
## What is zathura-pdf-mupdf?

A plugin for zathura.

It allows the latter to use MuPDF as a backend.

### Why should I install it?

zathura is *much* faster to read a pdf when it uses MuPDF as a backend:
<https://askubuntu.com/q/804515/867754>

It also consumes a lot less memory (2-4 times less in my limited testing).

Finally, it provides epub support, which means  that you don't need to convert a
novel into a pdf before being able to read it.

###
### How to install it?

Use a PPA:

    $ sudo add-apt-repository ppa:spvkgn/zathura-mupdf
    $ sudo aptitude update
    $ sudo aptitude install zathura-pdf-mupdf

See: <https://launchpad.net/~spvkgn/+archive/ubuntu/zathura-mupdf>


NOTE: The last `install` command will remove `zathura-pdf-poppler` (because they
provide the same functionality).

---

Alternatively, you can simply download the package from here:
<https://launchpad.net/~spvkgn/+archive/ubuntu/zathura-mupdf/+sourcepub/8048474/+listing-archive-extra>
And its custom dependency `libmupdf-pic-dev` from here:
<https://launchpad.net/~spvkgn/+archive/ubuntu/zathura-mupdf/+sourcepub/8048472/+listing-archive-extra>
Click on the file below the section "Package files" with the extension `amd64.deb`.

And install `libmupdf-pic-dev` then `zathura-pdf-mupdf` with `$ dpkg -i`.
Again, it will purge `zathura-pdf-poppler`:

    ...˜
    dpkg: considering removing zathura-pdf-poppler in favour of zathura-pdf-mupdf ...˜
    dpkg: yes, will remove zathura-pdf-poppler in favour of zathura-pdf-mupdf˜
    ...˜

#### How to compile it from source?

*What follows only applies to Ubuntu 16.04 and 18.04.*

First, you need to compile a recent version of `libmupdf-dev`:

    $ git clone --recursive git://git.ghostscript.com/mupdf.git
    $ cd mupdf
    $ git checkout 1.11-rc1
    $ git submodule update --init
    $ sudo aptitude update
    $ sudo aptitude install libgl1-mesa-dev libglu1-mesa-dev libxcursor-dev libxi-dev libxinerama-dev libxrandr-dev mesa-common-dev pkg-config

    $ CFLAGS=-fPIC make HAVE_X11=no HAVE_GLUT=no prefix=/usr/local
      ├──────────┘
      └ pass some flags to `gcc(1)`, otherwise the compilation of `zathura-pdf-mupdf` will fail,
        with an error  message recommending you to recompile with those flags.

    # Give this description: “development files for the MuPDF viewer”
    $ sudo checkinstall --pkgversion=1.11 --pkgname=libmupdf-dev

If  the  compilation   fails  because  of  a  missing  file,   have  a  look  at
`docs/building.html`, header “Compiling on Linux”  (switch to master if the file
doesn't exist).

Now, you can finally compile the plugin:

    $ git clone https://git.pwmt.org/pwmt/zathura-pdf-mupdf.git
    $ cd zathura-pdf-mupdf
    $ git checkout 0.3.1
    $ sudo aptitude install libjbig2dec0-dev libjpeg-dev libopenjp2-7-dev libssl-dev zathura-dev
    $ sudo make install

    $ sudo CFLAGS=-fPIC make install

Note that  you can't easily  go beyond  certain versions for  `libmupdf-dev` and
`zathura-pdf-mupdf`:

    ┌────────┬──────────────┬───────────────────┐
    │ ubuntu │ libmupdf-dev │ zathura-pdf-mupdf │
    ├────────┼──────────────┼───────────────────┤
    │ 16.04  │     1.11     │       0.3.1       │
    ├────────┼──────────────┼───────────────────┤
    │ 18.04  │     1.13     │       0.3.2       │
    └────────┴──────────────┴───────────────────┘

Otherwise the compilation of the plugin fails.

For more info, see: <https://askubuntu.com/a/1134907>

---

If you later decide to remove the plugin with:

    $ sudo make uninstall

It will remove the `/usr/lib/zathura/pdf.so` library from zathura-pdf-poppler.
So reinstall the latter:

    $ sudo aptitude reinstall zathura-pdf-poppler

###
### It can't read an epub!

If you have  installed zathura *after* the plugin, you  may have overwritten the
`pdf.so` file, in which case your backend is not mupdf but still poppler.

Reinstall the plugin:

    $ sudo aptitude reinstall zathura-pdf-mupdf

Or (if you compiled the plugin):

    $ sudo make install

##
# Todo
## ?

These are some notes about our experience in compiling zathura.

    $ git clone https://github.com/pwmt/zathura
    $ meson build
    meson.build:40:0: ERROR: Native dependency 'girara-gtk3' not found˜

---

<https://pwmt.org/projects/girara/>

    $ git clone https://git.pwmt.org/pwmt/girara.git

    $ vim README

Run  the following  command to  build and  install girara  to your  system using
meson's ninja backend:

    $ meson build
    $ cd build
    $ ninja

    $ ninja install
    meson.build:34:0: ERROR: Invalid version of dependency, need 'glib-2.0' ['>=2.50'] found '2.48.2'.˜

---

<http://www.linuxfromscratch.org/blfs/view/svn/general/glib2.html>

    $ wget ftp://ftp.gnome.org/pub/gnome/sources/glib/2.56/glib-2.56.1.tar.xz
    $ aunpack glib-2.56.1.tar.xz

    $ ./configure
    configure: error: Package requirements (libffi >= 3.0.0) were not met:˜

    No package 'libffi' found˜

    Consider adjusting the PKG_CONFIG_PATH environment variable if you˜
    installed software in a non-standard prefix.˜

    Alternatively, you may set the environment variables LIBFFI_CFLAGS˜
    and LIBFFI_LIBS to avoid the need to call pkg-config.˜
    See the pkg-config man page for more details.˜

---

    $ sudo aptitude install libffi-dev

    $ ./configure
    configure: error: *** Could not find libmount˜

    $ sudo aptitude install libmount-dev
    $ ./configure
    $ make
    $ sudo checkinstall --pkgname myglib

---

Get back to girara/:

    $ meson build
    meson.build:35:0: ERROR: Native dependency 'gtk+-3.0' not found˜

---

    $ wget http://ftp.gnome.org/pub/gnome/sources/gtk+/3.22/gtk+-3.22.30.tar.xz
    $ aunpack gtk+-3.22.30.tar.xz
    $ ./configure --prefix=/usr/local
    configure: error: Package requirements (glib-2.0 >= 2.49.4    atk >= 2.15.1    pango >= 1.37.3    cairo >= 1.14.0    cairo-gobject >= 1.14.0    gdk-pixbuf-2.0 >= 2.30.0) were not met:˜
    No package 'pango' found˜

    $ sudo aptitude install libpango1.0-dev
    $ ./configure --prefix=/usr/local
    $ make
    $ sudo checkinstall --pkgname mygtk3

---

Get back to girara/:

    $ meson build
        Dependency libnotify found: NO˜
        Program doxygen found: NO˜
        Dependency check found: NO˜

    $ rm -rf build
    $ sudo aptitude install doxygen libnotify-dev check
    $ meson --prefix=/usr build
    $ cd build
    $ ninja
    $ sudo ninja install

---

Get back to zathura/:

    $ meson build
    Dependency synctex found: NO˜
    Library magic found: NO˜
    Dependency libseccomp found: NO˜
    Program appstream-util found: NO˜
    Program sphinx-build found: NO˜

    doc/meson.build:1:0: ERROR: Program(s) ['sphinx-build'] not found or not executable˜

    $ rm -rf build
    $ sudo aptitude install libsynctex-dev libmagic-dev libseccomp-dev appstream-util python3-sphinx
    $ cd build
    $ ninja
    $ sudo ninja install

---

zathura can be started but it can't open a pdf.

    error: could not open plugin directory: /usr/local/lib/x86_64-linux-gnu/zathura˜
    error: Unknown file type: 'application/pdf'˜

We need to install this:

<https://pwmt.org/projects/zathura-pdf-poppler/>

    $ git clone https://git.pwmt.org/pwmt/zathura-pdf-poppler.git
    $ cd zathura-pdf-poppler
    $ git checkout --track -b develop origin/develop
    $ mkdir build
    $ meson build
    meson.build:21:0: ERROR: Native dependency 'poppler-glib' not found˜

    $ sudo aptitude install libpoppler-glib-dev
    $ rm -rf build && mkdir build
    $ meson build

    $ cd build
    $ ninja
    $ sudo ninja install

Note that if you  want to remove the files installed by  `$ ninja install`, read
the logfile in `build/meson-logs/install-log.txt`.
It will tell you which files have been installed.

