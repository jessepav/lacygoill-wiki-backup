# Compiling Vim
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

## get the source code

    $ git clone https://github.com/vim/vim.git
    $ cd vim
    $ make clean; make distclean
    $ git checkout master
    $ git pull

##
##configure the compilation

    ./configure --enable-cscope \
                --enable-fail-if-missing \
                --enable-gui=gtk2 \
                --enable-luainterp=dynamic \
                --enable-multibyte \
                --enable-python3interp=yes \
                --enable-pythoninterp=yes \
                --enable-terminal \
                --prefix=/usr/local \
                --with-compiledby=user \
                --with-features=huge \
                --with-luajit \
                --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu/ \
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
#### `--enable-luainterp=dynamic`, `--enable-pythoninterp=yes`, `--enable-python3interp=yes`?

Enable the lua/perl/python[23] interfaces.
See `:h if_lua` and `:h if_pyth`.

#### `--enable-fail-if-missing`?

Make the configuration script stop if it finds that an interface won't work.

####
#### `--enable-gui=gtk2`?

According to `:h gui-x11-compiling`, it's not necessary, because it's enabled by
default:

> The GTK+ 2 GUI is built by default. Therefore, you usually don't
> need to pass any options  such as --enable-gui=gtk2 to configure
> and build that.

Nevertheless, better be explicit.

In particular, we don't want to use gtk3, because the latter can increase the latency.

> We can also  note that Vim using GTK3 is slower  than its GTK2 counterpart
> by  an order  of magnitude. It  might therefore  be possible  that the  GTK3
> framework  introduces extra  latency,  as  we can  also  observe other  that
> GTK3-based terminals  (Terminator, Xfce4  Terminal, and GNOME  Terminal, for
> example) have higher latency.

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

#### ?

How to install it?

    $ sudo checkinstall

Si on n'a pas `checkinstall`, exécuter `sudo make install` à la place.

La procédure d'installation nous posera qques questions.

Lorsqu'un menu apparaîtra, on pensera à changer la valeur de l'entrée 2, dont le
nom est 'Name'.
Le nom  qu'on donnera au paquet  (par défaut `src`,  car on est dans  un dossier
`src`), sera celui qu'il faudra utiliser qd on voudra manipuler le paquet par la
suite via `dpkg`.

On pourra aussi changer la valeur des entrées 0, 1 et 11:

   - 0 (Maintainer: donner son email)
   - 1 (Summary: VIM compiled from source)
   - 2 (Name: myvim)
   - 11 (Provides: editor)

Il  est important  de ne  pas utiliser  le nom  `vim` pour  notre paquet,  si on
souhaite installer et utiliser en parallèle le paquet `vim` des repos officiels.
Autrement  il y  aura  conflit, et  qd  on fera  une màj,  le  paquet des  repos
supprimera notre paquet.

---

finish importing comments from `~/bin/upp`.

##
## For more info:

- `:h 90.1`
- <https://github.com/Valloric/YouCompleteMe/wiki/Building-Vim-from-source>

##
# Compiling Neovim
## documentation

<https://github.com/neovim/neovim/wiki/Building-Neovim>

## install dependencies

    $ sudo aptitude install libtool libtool-bin autoconf automake cmake g++ pkg-config unzip

Source: <https://github.com/neovim/neovim/wiki/Building-Neovim#build-prerequisites>

## clone and update the Neovim repo

    $ git clone https://github.com/neovim/neovim

    $ git checkout master

    $ git pull

## clean the repo from the files generated during the previous compilation

    $ make clean && make distclean
                         │
                         └ removes, among other things, the `build/` directory

## compile

    $ make CMAKE_BUILD_TYPE=Release
           ├──────────────────────┘
           └ Full compiler optimisations and no debug information.
             Expect the best performance from this build type.
             Often used by package maintainers.

You could also replace `Release` with `RelWithDebInfo`.
The latter  enables many optimisations and  adds enough debug info  so that when
nvim ever crashes, you can still get a backtrace.

---

If a network connection fails during the compilation, the latter will also fail.
In that case, re-try a compilation (now or a bit later).

## check the version of the binary you've just compiled

    $ ./build/bin/nvim --version | grep ^Build

## test it

    $ LC_ALL=C make test
    $ make oldtest

The second command executes the Vim tests.
They need to be performed in a fullscreen terminal.
If you use Tmux, run the command in an unsplit window, or in zoomed pane.

## ?

install it

    $ sudo checkinstall --pkgname "nvim" --pkgversion "$(git describe)" --spec /dev/null -y

---

If the installation fails, try to recompile:

- <https://github.com/neovim/neovim/issues/2364#issuecomment-113966180>
- <https://github.com/serverwentdown/env/commit/a05a31733443fcb0979fecf18f2aa8e9e2722c7c>

Note that there may be a performance cost if you disable jemalloc, I don't know.
See here to understand what jemalloc is:
<https://stackoverflow.com/a/1624744/9780968>

Note that Nvim is multi-threaded:
<https://github.com/neovim/neovim/wiki/Development-tips/fd1582128edb0130c1d5c828a3a9b55aa9107030>

> `thread apply all bt` may be necessary because **Neovim is multi-threaded**.

Alternatively, you  could try  to pass  an option to  checkinstall, and  make it
generate a deb without installing it.
Then, you could try to force its installation with `dpkg` and the right options.

---

    # If this command fails for Nvim

    #     checkinstall --pkgname="${PGM}" --pkgversion="${VERSION}" --spec=/dev/null --backup=no -y

    # try to recompile and replace:
    #
    #     $ make CMAKE_BUILD_TYPE=Release
    #
    # With:
    #
    #     $ make CMAKE_BUILD_TYPE=Release CMAKE_EXTRA_FLAGS=-DENABLE_JEMALLOC=OFF
    #
    # See:
    # https://github.com/neovim/neovim/issues/2364#issuecomment-113966180
    # https://github.com/serverwentdown/env/commit/a05a31733443fcb0979fecf18f2aa8e9e2722c7c
    #
    # Note that I  don't know whether there's a performance  cost if you disable
    # jemalloc.
    #
    # See here to understand what jemalloc is:
    # https://stackoverflow.com/a/1624744/9780968
    #
    # Note that Nvim is multi-threaded:
    # > `thread apply all bt` may be necessary because **Neovim is multi-threaded**.
    #
    # Source: https://github.com/neovim/neovim/wiki/Development-tips/fd1582128edb0130c1d5c828a3a9b55aa9107030
    #
    # ---
    #
    # Alternatively, you  could try  to pass  an option to  checkinstall, and  make it
    # generate a deb without installing it.
    # Then, you could try to force its installation with `dpkg` and the right options.

## UNinstall it (optional)

    $ sudo rm /usr/local/bin/nvim

    $ sudo rm -r /usr/local/share/nvim/

## ?

python integration

    $ python -m pip install --user --upgrade pynvim

    $ python3 -m pip install --user --upgrade pynvim

---

At the  moment, the first command  works, but `:CheckHealth` contains  a warning
message:

    ## Python 2 provider (optional)~
      - INFO: Disabled (g:loaded_python_provider=1).  This might be due to some previous error.~
      - INFO: `g:python_host_prog` is not set.  Searching for python2 in the environment.~
      - INFO: Multiple python2 executables found.  Set `g:python_host_prog` to avoid surprises.~
      - INFO: Executable: /usr/bin/python2~
      - INFO: Other python executable: /bin/python2~
      - INFO: Python version: 2.7.12~
      - INFO: pynvim version: 0.3.1~
      - WARNING: Could not contact PyPI to get latest version.~
      - ERROR: HTTP request failed: error: curl error with https://pypi.python.org/pypi/pynvim/json: 35~

It's due to a SSL handshaking which fails while `curl(1)` tries to download this file:
<https://pypi.python.org/pypi/pynvim/json>.

See `man curl`, and search for `35` which is the given code error.

---

At the moment, the second command fails:

    Could not find a version that satisfies the requirement pynvim (from versions: )~
    No matching distribution found for pynvim~

Pass the `-vvv` argument to `pip` to get more information.

Also, `:CheckHealth` contains the following messages:

    - INFO: Using: g:python3_host_prog = "/usr/bin/python3"~
    - INFO: Executable: /usr/bin/python3~
    - ERROR: Command error (job=9, exit code 1): `'/usr/bin/python3' -c 'import sys; sys.path.remove(""); import pynvim; print(pynvim.__file__)'` (in '~/wiki/vim')~
    Output: Traceback (most recent call last):  File "<string>", line 1, in <module>ImportError: No module named 'pynvim'~
    Stderr: Traceback (most recent call last):  File "<string>", line 1, in <module>ImportError: No module named 'pynvim'~
    - INFO: Python version: 3.5.2~
    - INFO: pynvim version: unable to load pynvim Python module~
    - ERROR: Importing "neovim" failed.~
    - ADVICE:~
      - Reinstall "pynvim" and optionally "neovim" packages.~
          pip3 uninstall pynvim neovim~
          pip3 install pynvim~
          pip3 install neovim # only if needed by third-party software~
    - ERROR: pynvim is not installed.~
    Error: unable to load pynvim Python module~
    - ADVICE:~
      - Run in shell: pip3 install pynvim~
    - WARNING: Could not contact PyPI to get latest version.~
    - ERROR: HTTP request failed: error: curl error with https://pypi.python.org/pypi/pynvim/json: 35~

See `:h provider-python`, and:

<https://github.com/pypa/pip/issues/3776>
<https://github.com/neovim/neovim/issues/3396>
<https://github.com/neovim/neovim/wiki/FAQ>
<https://github.com/zchee/deoplete-jedi/wiki/Setting-up-Python-for-Neovim>

Update:

`python[3] -m pip install --user --upgrade pynvim` fails because of `Error 104 connection reset by peer`.
Is our IP blacklisted?

Solution:

Go to `https://pypi.org/` and look for the package `pynvim`.
Atm, you'll find this url:

<https://pypi.org/project/pynvim/>

Click on `Homepage` and you'll get this url:

<https://github.com/neovim/pynvim>

Clone the repo:

    $ git clone https://github.com/neovim/pynvim

Then install the package manually:

    $ cd pynvim
    $ python3 -m pip install --user --upgrade .

The installation may fail because of a missing dependency, `msgpack`.

> Could not find a version that satisfies the requirement msgpack>=0.5.0 (from pynvim==0.3.1) (from versions: )
> No matching distribution found for msgpack>=0.5.0 (from pynvim==0.3.1)

In that case repeat the process:

    https://pypi.org/project/msgpack/
    https://github.com/msgpack/msgpack
    $ git clone https://github.com/msgpack/msgpack
    $ cd msgpack
    $ python3 -m pip install --user --upgrade .
    $ cd ../pynvim
    $ python3 -m pip install --user --upgrade .

Note that we often can't access pypi.org...
But sometimes we can...
If  you can't,  try to  look for  the package  directly on  github (hoping  it's
developed there, and not somewhere else, like gitlab or bitbucket).
Or, use the tor browser (it works!).
Or, use a webproxy (like https://proxysite.com/).

Alternatively, maybe you could try to contact another mirror:

    $ python3 -m pip install --user --upgrade -i http://e.pypi.python.org/simple pynvim
                                              ├────────────────────────────────┘
                                              └ https://stackoverflow.com/a/13878827/9780968

Or, use `pip` behind a proxy:

    $ export https_proxy=http://web-proxy.mydomain.com
    $ python3 -m pip install --user --upgrade pynvim

Source: <https://stackoverflow.com/a/19962913/9780968>

## ?

    ## Ruby provider (optional)~
      - INFO: Ruby: ruby 2.3.1p112 (2016-04-26) [x86_64-linux-gnu]~
      - WARNING: `neovim-ruby-host` not found.~
        - ADVICE:~
          - Run `gem install neovim` to ensure the neovim RubyGem is installed.~
          - Run `gem environment` to ensure the gem bin directory is in $PATH.~
          - If you are using rvm/rbenv/chruby, try "rehashing".~
          - See :help |g:ruby_host_prog| for non-standard gem installations.~

              https://github.com/rubygems/rubygems.org/issues/1760~
              http://www.fastly-debug.com/~

        ## Node.js provider (optional)~
          - INFO: Node.js: v4.2.6~
          - WARNING: Neovim node.js host does not support v4.2.6~

    $ gem install --user-install neovim

    ERROR:  Could not find a valid gem 'neovim' (>= 0), here is why:~
              Unable to download data from https://rubygems.org/ - Errno::ECONNRESET: Connection reset by peer - SSL_connect (https://api.rubygems.org/specs.4.8.gz)~

    # choose a proxy supporting http*s* from here: <https://www.us-proxy.org/>
    $ https_proxy=<ip>:<port> gem install --user-install neovim

## ?

    $ sudo update-alternatives --install /usr/bin/vi vi /usr/bin/nvim 60
    $ sudo update-alternatives --config vi
    $ sudo update-alternatives --install /usr/bin/vim vim /usr/bin/nvim 60
    $ sudo update-alternatives --config vim
    $ sudo update-alternatives --install /usr/bin/editor editor /usr/bin/nvim 60
    $ sudo update-alternatives --config editor

Use Neovim for some (or all) of the editor alternatives.

## ?

<https://github.com/mhinz/neovim-remote>
<https://hkupty.github.io/2016/Ditching-TMUX/>

