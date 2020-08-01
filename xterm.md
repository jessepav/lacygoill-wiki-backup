# How to compile xterm from source?

Visit the developer's site: <https://invisible-island.net/xterm/xterm.html>

Download the source code: <ftp://ftp.invisible-island.net/xterm/xterm.tar.gz>

Extract the archive.

Enter the extracted directory:

    cd xterm-123

Configure:

    ./configure --exec-prefix=/usr/local \
         --disable-imake \
         --enable-256-color \
         --enable-backarrow-is-erase \
         --enable-dabbrev \
         --enable-exec-xterm \
         --enable-logging \
         --enable-luit \
         --enable-narrowproto \
         --enable-sixel-graphics \
         --enable-wide-chars \
         --with-icon-theme=yes \
         --with-icondir=/usr/local/share/icons \
         --with-tty-group=tty \
         --with-utempter

Compile:

    make

Install:

    sudo make install

---

In case you wonder where the previous configuration options come from:

    $ cd /tmp
    $ apt-get source xterm
    $ cd xterm-123
    $ vim debian/rules +'/override_dh_auto_configure'

##
# Todo
## Find a way to get notified whenever a new version is available.

Try to convert this link into a rss feed:

<https://invisible-island.net/xterm/xterm.log.html>
