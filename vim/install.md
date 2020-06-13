# Compiling
## install dependencies

Find the section of the repo from where the default Vim binary can be installed:

    $ apt-cache policy vim

For example, on Ubuntu 16.04, the default Vim binary can be installed from `xenial/main`:

    2:7.4.1689-3ubuntu1 500
       500 http://fr.archive.ubuntu.com/ubuntu xenial/main amd64 Packages
                                               ^^^^^^^^^^^
                                               relevant section

Backup `sources.list`:

    $ sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup

Edit the file, so that you can download the source code of the default Vim binary:

    $ sudoedit /etc/apt/sources.list
    /deb-src.*xenial main
    " press `gcc` to uncomment the line

If you can't find  a line matching `deb-src.*xenial main`, just  look for a line
matching `deb.*xenial main`, duplicate it, and replace `deb` with `deb-src`.

You should end up with a line such as:

    deb-src http://fr.archive.ubuntu.com/ubuntu/ xenial main restricted

Download the source code of the default Vim binary:

    $ sudo aptitude update

Install the default Vim's binary dependencies:

    $ sudo aptitude build-dep vim

---

Install the dependencies necessary to compile the lua interface:

    $ sudo aptitude install luajit libluajit-5.1-dev

Later, you can check the lua interface has been compiled by running:

    :echo has('lua')
    1~
    :echo &luadll
    libluajit-5.1.so.2~

## get the source code / update

    $ git clone https://github.com/vim/vim.git
    $ cd vim
    $ git checkout master
    $ git pull

## clean repo from files generated during previous compilation

    $ make clean; make distclean

##
##configure the compilation

    ./configure --enable-cscope \
                --enable-fail-if-missing \
                --enable-gui=gtk2 \
                --enable-luainterp=dynamic \
                --enable-multibyte \
                --enable-python3interp=yes \
                --enable-terminal \
                --prefix=/usr/local \
                --with-compiledby=user \
                --with-features=huge \
                --with-luajit \
                --with-python3-config-dir=/usr/lib/python3.5/config-3.5m-x86_64-linux-gnu/

### Why should I avoid the perl and ruby interfaces?

First, you probably don't need them; I  have never found a plugin which requires
the ruby or perl interface to work.

Second, the less code, the less bugs.

---

If yoy really need them, pass these options to `configure`:

    --enable-perlinterp=yes
    --enable-rubyinterp=dynamic

### How can I get the list of all possible `configure` options?

    ./configure --help

###
### What is the effect of
#### `--with-features=huge`?

Enable all the  features documented at `:h +feature-list` which  are prefixed by
the flag `T`, `S`, `N`, `B` or `H`.

See `:h :ve` for the meaning of these flags.

####
#### `--enable-luainterp=dynamic`, `--enable-python3interp=yes`?

Enable the lua/perl/python3 interfaces.
See `:h if_lua` and `:h if_pyth`.

#### `--enable-fail-if-missing`?

Make the configuration script stop if it finds that an interface won't work.

####
#### `--enable-gui=gtk2`?

According to `:h gui-x11-compiling`, it's not necessary, because it's enabled by
default:

>     The GTK+ 2 GUI is built by default. Therefore, you usually don't
>     need to pass any options  such as --enable-gui=gtk2 to configure
>     and build that.

Nevertheless, better be explicit.

In particular, we don't want to use gtk3, because the latter can increase the latency.

>     We can also  note that Vim using GTK3 is slower  than its GTK2 counterpart
>     by  an order  of magnitude. It  might therefore  be possible  that the  GTK3
>     framework  introduces extra  latency,  as  we can  also  observe other  that
>     GTK3-based terminals  (Terminator, Xfce4  Terminal, and GNOME  Terminal, for
>     example) have higher latency.

Source: <https://lwn.net/Articles/751763/>

I can confirm what the article states.
In my limited testing with typometer, the latency doubles after compiling with gtk3.

#### `--enable-multibyte`?

Add support for multibyte characters (16 and 32 bits).

#### `--with-compiledby=user`?

Display `user` on the `Compiled by` line in the output of `:version`.

###
## compile

    $ make

### Where is the newly compiled binary?

    ./src/vim

#### How to test it?

    $ make test

Once all tests have been run,scroll back in the output until you find `Test results`.
A bit later, you should find sth like:

    Executed: 2313 tests
     Skipped:   20 tests
      Failed:    0 test

    ALL DONE

If only a few tests fail, Vim can still work, but not perfectly.
If  many tests  fail,  or Vim  can't  even run  all the  tests,  you'll need  to
re-compile; this  time try to  change the configuration, or  install/configure a
missing dependency.

---

For a maximum of tests to succeed, run them:

   - outside tmux
   - in xterm
   - with a "standard" geometry (24x80)

#### How to install it?

    $ sudo make install

#### How to UNinstall it?

    $ sudo make uninstall

#### How to make Ubuntu use it by default?

Vim can be invoked with many shell commands:

    $ update-alternatives --get-selections | grep vim

We need to tell the system that, from now on, they are all provided by `/usr/local/bin/vim`.
For example, to tell Ubuntu that the `vim` command is provided by `/usr/local/bin/vim`:

    $ sudo update-alternatives --install /usr/bin/vim vim /usr/local/bin/vim 60
    $ sudo update-alternatives --set vim /usr/local/bin/vim

For the `editor` command:

    $ sudo update-alternatives --install /usr/bin/editor editor /usr/local/bin/vim 60
    $ sudo update-alternatives --set editor /usr/local/bin/vim

Etc.

##
## For more info:

- `:h 90.1`
- <https://github.com/Valloric/YouCompleteMe/wiki/Building-Vim-from-source>

