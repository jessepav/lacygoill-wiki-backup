# ?

zathura is *much* faster to read a pdf when it uses MuPDF as a backend:
<https://askubuntu.com/q/804515/867754>

It also  supports reading  epub, which means  that you don't  need to  convert a
novel into a pdf before being able to read it in zathura.

This requires to install the `zathura-pdf-mupdf` plugin.

---

On Ubuntu 16.04 use this PPA:
<https://launchpad.net/~spvkgn/+archive/ubuntu/zathura-mupdf>

If you use it to install the plugin, it will pull in `libopenjp2-7` as a dependency,
and remove `zathura-pdf-poppler` (because they provide the same functionality).

You don't have to install the PPA, you can simply download the package from here:
<https://launchpad.net/~spvkgn/+archive/ubuntu/zathura-mupdf/+sourcepub/8048474/+listing-archive-extra>

---

On Ubuntu 18.04, you can try to compile the plugin:

    # for virtual machine only
    $ sudo systemctl disable --now apt-daily{,-upgrade}.{timer,service}
    $ sudo apt install git
    $ git clone https://git.pwmt.org/pwmt/zathura-pdf-mupdf.git
    $ cd zathura-pdf-mupdf
    $ git checkout 0.3.2

    $ sudo aptitude install meson
    $ meson build
      meson.build:18:0: ERROR: Pkg-config not found.~
    $ sudo aptitude install pkg-config
    $ meson build
      meson.build:18:0: ERROR: Native dependency 'zathura' not found~
    $ sudo aptitude install zathura-dev
      meson.build:18:0: ERROR: Invalid version of dependency, need 'zathura' ['>=0.3.9'] found '0.3.8'.~

    $ git checkout 0.3.3
    $ meson build
      meson.build:18:0: ERROR: Invalid version of dependency, need 'zathura' ['>=0.3.9'] found '0.3.8'.~

    $ git checkout 0.3.2
    $ meson build
      Neither directory contains a build file meson.build.~

    $ make install
      No package 'libcrypto' found~
      ...~
      document.c:5:10: fatal error: mupdf/fitz.h: No such file or directory~
    $ sudo apt install apt-file
    $ apt-file update
    $ apt-file search libcrypto
      ...~
      libssl-dev~
      ...~
    $ apt-file search mupdf/fitz.h
      libmupdf-dev: /usr/include/mupdf/fitz.h~
    $ sudo apt install libssl-dev libmupdf-dev

    $ make install
      /usr/bin/ld: cannot find -ljbig2dec~
      /usr/bin/ld: cannot find -lopenjp2~
      /usr/bin/ld: cannot find -ljpeg~
    $ apt-file search -x 'lib.*jbig2dec.*dev'
      libjbig2dec0-dev~
    $ apt-file search -x 'lib.*openjp2.*dev'
      libopenjp2-7-dev~
    $ apt-file search -x 'lib.*jpeg.*dev'
      libjpeg-dev~
      ...~
    $ sudo apt install libjbig2dec0-dev libopenjp2-7-dev libjpeg-dev

    $ make install
    pdf build options:~
    CFLAGS  = -std=c99 -fPIC -pedantic -Wall -Wno-format-zero-length -pthread -I/usr/include/gtk-3.0 -I/usr/include/at-spi2-atk/2.0 -I/usr/include/at-spi-2.0 -I/usr/include/dbus-1.0 -I/usr/lib/x86_64-linux-gnu/dbus-1.0/include -I/usr/include/gtk-3.0 -I/usr/include/gio-unix-2.0/ -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/harfbuzz -I/usr/include/pango-1.0 -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pixman-1 -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/libpng16 -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -pthread -I/usr/include/gtk-3.0 -I/usr/include/at-spi2-atk/2.0 -I/usr/include/at-spi-2.0 -I/usr/include/dbus-1.0 -I/usr/lib/x86_64-linux-gnu/dbus-1.0/include -I/usr/include/gtk-3.0 -I/usr/include/gio-unix-2.0/ -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/harfbuzz -I/usr/include/pango-1.0 -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pixman-1 -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/libpng16 -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/json-c  -I/usr/include/cairo -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/pixman-1 -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/freetype2 -I/usr/include/libpng16 -pthread -I/usr/include/gtk-3.0 -I/usr/include/at-spi2-atk/2.0 -I/usr/include/at-spi-2.0 -I/usr/include/dbus-1.0 -I/usr/lib/x86_64-linux-gnu/dbus-1.0/include -I/usr/include/gtk-3.0 -I/usr/include/gio-unix-2.0/ -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/harfbuzz -I/usr/include/pango-1.0 -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/libpng16 -I/usr/include/json-c -I/usr/include/cairo -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/pixman-1 -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/harfbuzz -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include~
    LDFLAGS = -fPIC~
    DFLAGS  = -g~
    CC      = cc~
    LD pdf.so~
    /usr/bin/ld: /usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib/libmupdf.a(draw-device.o): relocation R_X86_64_PC32 against symbol `fz_empty_irect' can not be used when making a shared object; recompile with -fPIC~
    /usr/bin/ld: final link failed: Bad value~
    collect2: error: ld returned 1 exit status~
    Makefile:46: recipe for target 'pdf.so' failed~
    make: *** [pdf.so] Error 1~

The Makefile can be read here: <https://0x0.st/zNkF.txt>
It's indented with a space to prevent `0x0.st` from handling it as a binary file
(you wouldn't be able to read it online, only download it).

    $ gcc -v
    Using built-in specs.~
    COLLECT_GCC=gcc~
    COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/7/lto-wrapper~
    OFFLOAD_TARGET_NAMES=nvptx-none~
    OFFLOAD_TARGET_DEFAULT=1~
    Target: x86_64-linux-gnu~
    Configured with: ../src/configure -v --with-pkgversion='Ubuntu 7.3.0-27ubuntu1~18.04' --with-bugurl=file:///usr/share/doc/gcc-7/README.Bugs --enable-languages=c,ada,c++,go,brig,d,fortran,objc,obj-c++ --prefix=/usr --with-gcc-major-version-only --program-suffix=-7 --program-prefix=x86_64-linux-gnu- --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-libmpx --enable-plugin --enable-default-pie --with-system-zlib --with-target-system-zlib --enable-objc-gc=auto --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-offload-targets=nvptx-none --without-cuda-driver --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu~
    Thread model: posix~
    gcc version 7.3.0 (Ubuntu 7.3.0-27ubuntu1~18.04) ~

---

Once the plugin is installed, evince will be the default program to open a pdf.
This is because the file `zathura-pdf-mupdf.desktop` doesn't exist anymore.
Solution:

    $ xdg-mime default zathura-pdf-mupdf.desktop application/pdf

# ?

        $ git clone https://github.com/pwmt/zathura
        $ meson build
        $ meson.build:40:0: ERROR: Native dependency 'girara-gtk3' not found

---

https://pwmt.org/projects/girara/

        $ git clone https://git.pwmt.org/pwmt/girara.git

        $ vim README

        Run the following command to build and install girara to your system using
        meson's ninja backend:

          meson build
          cd build
          ninja
          ninja install

        meson.build:34:0: ERROR: Invalid version of dependency, need 'glib-2.0' ['>=2.50'] found '2.48.2'.

---

        http://www.linuxfromscratch.org/blfs/view/svn/general/glib2.html

        $ wget ftp://ftp.gnome.org/pub/gnome/sources/glib/2.56/glib-2.56.1.tar.xz

        $ aunpack glib-2.56.1.tar.xz

        $ ./configure

        configure: error: Package requirements (libffi >= 3.0.0) were not met:

        No package 'libffi' found

        Consider adjusting the PKG_CONFIG_PATH environment variable if you
        installed software in a non-standard prefix.

        Alternatively, you may set the environment variables LIBFFI_CFLAGS
        and LIBFFI_LIBS to avoid the need to call pkg-config.
        See the pkg-config man page for more details.

---

        $ sudo aptitude install libffi-dev

        $ ./configure

        configure: error: *** Could not find libmount

        $ sudo aptitude install libmount-dev

        $ ./configure
            # ✔

        $ make
            # ✔

        $ sudo checkinstall --pkgname myglib
            # ✔

---

Get back to girara/:

        $ meson build
        meson.build:35:0: ERROR: Native dependency 'gtk+-3.0' not found

---

        $ wget http://ftp.gnome.org/pub/gnome/sources/gtk+/3.22/gtk+-3.22.30.tar.xz

        $ aunpack gtk+-3.22.30.tar.xz

        $ ./configure --prefix=/usr/local

        configure: error: Package requirements (glib-2.0 >= 2.49.4    atk >= 2.15.1    pango >= 1.37.3    cairo >= 1.14.0    cairo-gobject >= 1.14.0    gdk-pixbuf-2.0 >= 2.30.0) were not met:

        No package 'pango' found

        $ sudo aptitude install libpango1.0-dev

        $ ./configure --prefix=/usr/local
            # ✔

        $ make
            # ✔

        $ sudo checkinstall --pkgname mygtk3
            # ✔

---

Get back to girara/:

        $ meson build
            Dependency libnotify found: NO
            Program doxygen found: NO
            Dependency check found: NO

        $ rm -rf build

        $ sudo aptitude install doxygen libnotify-dev check

        $ meson --prefix=/usr build

        $ cd build

        $ ninja

        $ sudo ninja install

---

Get back to zathura/:

        $ meson build

        Dependency synctex found: NO
        Library magic found: NO
        Dependency libseccomp found: NO
        Program appstream-util found: NO
        Program sphinx-build found: NO

        doc/meson.build:1:0: ERROR: Program(s) ['sphinx-build'] not found or not executable

        $ rm -rf build
        $ sudo aptitude install libsynctex-dev libmagic-dev libseccomp-dev appstream-util python3-sphinx
        $ cd build
        $ ninja
        $ sudo ninja install

---

zathura can be started but it can't open a pdf.

        error: could not open plugin directory: /usr/local/lib/x86_64-linux-gnu/zathura
        error: Unknown file type: 'application/pdf'

We need to install this:

        https://pwmt.org/projects/zathura-pdf-poppler/

        $ git clone https://git.pwmt.org/pwmt/zathura-pdf-poppler.git
        $ cd zathura-pdf-poppler
        $ git checkout --track -b develop origin/develop
        $ mkdir build
        $ meson build

        meson.build:21:0: ERROR: Native dependency 'poppler-glib' not found

        $ sudo aptitude install libpoppler-glib-dev
        $ rm -rf build && mkdir build
        $ meson build

        $ cd build
        $ ninja
        $ sudo ninja install


Note that if you want to remove the files installed by `ninja install`, read the
logfile in `build/meson-logs/install-log.txt`.
It will tell you which files have been installed.

