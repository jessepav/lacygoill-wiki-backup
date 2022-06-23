# How to install the most recent python interpreter?
## Download

Go to the python download page: <https://www.python.org/downloads/release>

If you can't access the url, use our custom zsh shell function `tor`.

The latest release should be suggested by a large button.
Atm it's `3.9.4`.
Don't click on the main button, instead click on the link which gives you access
to various installer formats: <https://www.python.org/downloads/release/python-394/>

Download the tarball of the installer, and its signature stored in a PGP ASCII Armored File:
- <https://www.python.org/ftp/python/3.9.4/Python-3.9.4.tgz>
- <https://www.python.org/ftp/python/3.9.4/Python-3.9.4.tgz.asc>

## Check the authenticity of the installer

Import the release manager public keys via the public key file:

    $ curl https://www.python.org/static/files/pubkeys.txt | gpg --import -

If you  can't download `pubkeys.txt`  with `curl(1)`,  use our custom  zsh shell
function `tor`; visit the url, right-click, `Save Page As...`.

Or grab the individual keys directly from the keyserver network:

    $ gpg --keyserver hkps://pgp.mit.edu/ \
          --recv-keys 6A45C816 \
                      36580288 \
                      7D9DC8D2 \
                      18ADD4FF \
                      A4135B38 \
                      A74B06BF \
                      EA5BBD71 \
                      E6DF025C \
                      AA65421D \
                      6F5E1540 \
                      F73C700D \
                      487034E5

Check the authenticity of the installer's tarball:

    $ gpg --verify Python-3.9.4.tgz.asc

You should read a message containing the text “Good signature from ...”:

    $ gpg --verify Python-3.9.4.tgz.asc
    gpg: assuming signed data in `Python-3.9.4.tgz'
    gpg: Signature made Sun 04 Apr 2021 08:25:54 PM CEST using RSA key ID 10250568
    gpg: Good signature from "Łukasz Langa (GPG langa.pl) <lukasz@langa.pl>"
    gpg:                 aka "Łukasz Langa (Work e-mail account) <ambv@fb.com>"
    gpg:                 aka "[jpeg image of size 24479]"
    gpg:                 aka "Łukasz Langa <lukasz@python.org>"
    gpg: WARNING: This key is not certified with a trusted signature!
    gpg:          There is no indication that the signature belongs to the owner.
    Primary key fingerprint: E3FF 2839 C048 B25C 084D  EBE9 B269 95E3 1025 0568

To get rid of the warning:

                     ID of the key used to make the signature,
                     as given on the 2nd line of the previous command's output
                     v------v
    $ gpg --edit-key 10250568
    gpg> trust
        1 = I don't know or won't say
        2 = I do NOT trust
        3 = I trust marginally
        4 = I trust fully
        5 = I trust ultimately
        m = back to the main menu
    Your decision? 5

Now, if you re-run the `--verify` command, there should be no warning anymore:

    $ gpg --verify Python-3.9.4.tgz.asc
    gpg: assuming signed data in `Python-3.9.4.tgz'
    gpg: Signature made Sun 04 Apr 2021 08:25:54 PM CEST using RSA key ID 10250568
    gpg: checking the trustdb
    gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model
    gpg: depth: 0  valid:   8  signed:   4  trust: 0-, 0q, 0n, 0m, 0f, 8u
    gpg: depth: 1  valid:   4  signed:   3  trust: 4-, 0q, 0n, 0m, 0f, 0u
    gpg: next trustdb check due at 2023-09-25
    gpg: Good signature from "Łukasz Langa (GPG langa.pl) <lukasz@langa.pl>"
    gpg:                 aka "Łukasz Langa (Work e-mail account) <ambv@fb.com>"
    gpg:                 aka "[jpeg image of size 24479]"
    gpg:                 aka "Łukasz Langa <lukasz@python.org>"

See:

- <https://serverfault.com/a/569923>
- <https://security.stackexchange.com/a/69089>

## Extract the contents of the tarball

    $ tar xf Python-3.9.4.tgz
    $ rm Python-3.9.4.tgz
    $ cd Python-3.9.4

Don't extract the archive under `/run`; otherwise, the compilation will probably
fail because of a lack of space.

    /usr/bin/ld: final link failed: No space left on device
    collect2: error: ld returned 1 exit status
    Makefile:731: recipe for target 'Programs/_testembed' failed
    make: *** [Programs/_testembed] Error 1

Check how much space you have on the partition where you extract with `df -h` or `dfc`.

- <https://stackoverflow.com/a/31493804/9780968>
- <https://unix.stackexchange.com/a/16158/289772>

## Dependencies

    $ apt install libssl-dev libffi-dev

Without `libssl-dev`,  later, you might  not be able  to install a  package with
`pip`:

    $ python -m pip install --user requests
    pip is configured  with locations that require  TLS/SSL, however the
    ssl module in Python is not available.

    ...

    Could not find a version that satisfies the requirement requests (from versions: )
    No matching distribution found for requests

    Could not  fetch URL https://pypi.python.org/simple/requests/:

    There was a problem confirming the ssl certificate:
    HTTPSConnectionPool(host='pypi.python.org', port=443):
    Max  retries   exceeded  with  url:  /simple/requests/   (Caused  by
    SSLError("Can't connect to  HTTPS URL because the SSL  module is not
    available.",)) - skipping.

See also: <https://stackoverflow.com/a/41601137/9780968>

Without `libffi-dev`, you would get this error when installing a pip package:

    ModuleNotFoundError: No module named '_ctypes'

See also: <https://stackoverflow.com/a/48045929>

## Configure

Read the instructions for the compilation:

    $ vim README.rst

Read the configuration flags:

    $ ./configure --help

Configure:

    $ ./configure --enable-optimizations --with-lto --with-ensurepip=install
                    │                                 │
                    │                                 └ otherwise, later, you won't be able to execute
                    │                                   `pythonx.y -m pip ...`
                    │
                    └ Warning: it increases the compilation time (a lot),
                      and the resources consumed:

                          https://github.com/docker-library/python/issues/160

## Compile

    $ make profile-opt
           │
           └ only relevant if you used the `--enable-optimizations` flag
             during the configuration

## Test

    $ make test

You   probably   don't   need   to   start   the   tests   if   you   used   the
`--enable-optimizations` flag, because the latter will cause `make(1)` to start
them all.

If a  message is  printed about a  failed test  or a traceback  or core  dump is
produced, something is wrong.
You can re-run the failing test(s) in verbose mode::

    $ make test TESTOPTS="-v test_that_failed"

A failed  test may be due  to a missing  python package necessary to  perform the
test:

    test test_gdb failed
    2 tests failed again:
        test_gdb test_urllib2net

Use `$ apt-file search` to search for a missing dependency:

    $ apt-file search test_urllib2net
    ...
    $ apt-file search test_gdb
    ...

## Install

    $ sudo make altinstall

---

Do **not** use the usual `install` recipe; it would overwrite the default system
python binary, which in turn would create many issues.

---

You can now use the most recent python interpreter with commands like:

    $ python3.9
    $ python3.9 -m pip install --user --upgrade <package>
    ...

## Clean

    $ make clean && make distclean

##
# Interpreter
## How to see the list of all the interpreters installed on my machine?

    $ type -a python
    python is /usr/local/bin/python
    python is /usr/bin/python
    python is /bin/python

### In the previous output, what's the absolute path of the interpreter which will be run when I invoke `python`?

    /usr/local/bin/python

### Which environment variable is responsible for this path having the biggest priority?

    $PATH

`/usr/local/bin` comes before `/usr/bin`.

##
## How to leave the Python prompt?

Press `C-d`, or execute `exit()`.

##
## How to execute a script?

    >>> exec(open('/tmp/py.py').read())
                   ^--------^
                   full path to script

### How to import it?

    >>> import os
    >>> os.chdir('/path/to/my/')
    >>> import script.py

You can  ignore the  second command if  you're already in  the directory  of the
script; i.e. if you've started the interpreter from it.

#### ?

What's the difference?

The value  of the global variable  `__name__` is the string  `'script'` when the
module is imported; otherwise, it's `__main__`.

A module is compiled in `__pycache__/`, not a script.

The names  of the  imported functions  are not entered  directly in  the current
symbol table; only the module name is.  Using the module name you can access the
functions.

---

<https://stackoverflow.com/a/2996170>
<https://stackoverflow.com/a/2997044>

##
# Pip
## How to install pip?

If you  have a recent version  of Python (Python  2 >=2.7.9 or Python  3 >=3.4),
it's already installed.

If you've compiled it from source, make sure you've used the
`--with-ensurepip=install` option.

## How to update pip?

Like any other package:

    $ python -m pip install --upgrade --user pip

##
## How to get the version of a specific interpreter?

    $ /path/to/interpreter --version

## How to show details about an installed package?

    $ python -m pip show <package>

## How to list all python packages installed with `pip`?

    $ python -m pip freeze

## How to save the state of the versions of all installed packages, then restore it later?

    $ python -m pip freeze >req.txt
    $ python -m pip install --requirement req.txt

## How to list all python packages installed with `pip` but outdated?

    $ python -m pip list --outdated

## How to list all installed packages which have unsatisfied dependencies?

    $ python -m pip check

##
## How to install a package?

    $ python -m pip install --user <package> ...
                              │
                              └ install it in `~/.local/lib/pythonX.Y/site-packages`

## How to install a package for a specific interpreter?

    $ /path/to/interpreter -m pip install <package>

## How to remove a package?

    $ python -m pip uninstall <package> ...

##
## How to update an outdated package?

    $ python -m pip install --user --upgrade <package> ...

## How to deal with a package which can't be installed/updated?

Read the error message.
You may need  to install another python  or `.deb` package to  satisfy a missing
dependency.
Use commands such as:

   - `pip install`
   - `apt-file search`
   - `apt install`

##
## What's the effect of `python -m` before a `pip` command?

It lets you choose in the environment of which interpreter you want to work.
More specifically, the one called by the `python` command.

Without `python -m`,  it seems you have  no way of knowing  in which environment
`pip` is going to work.

---

Also, look here:
<https://docs.python.org/2/installing/#work-with-multiple-versions-of-python-installed-in-parallel>

##
# Documentation

- <https://docs.python.org/3/>
- <https://pip.pypa.io/en/stable/user_guide/>
- <https://pip.pypa.io/en/stable/reference/>

##
# Miscellaneous
## Can a variable name begin with an underscore?   A number?

An underscore: yes.
A number: no.

##
# Issues
## My `pip` command fails!

Use the `-vvv` flag to make it more verbose, and read the messages to find where
the issue comes from.

Example:

    $ python -m pip -vvv install --user <package>
                    ^--^

---

If you can't install anything with pip, try updating it.
If you can't even update pip, then try  to install a newer version of the python
3 interpreter.
If  you configure  it with  `--with-ensurepip=install`, it  will also  install a
newer version of the pip package manager.

---

You can also install the package manually.

First, find it on `https://pypi.org/`.
For example, for the pynvim package, the url is:

<https://pypi.org/project/pynvim/>

Next, click on `Homepage` and you'll get this url:

<https://github.com/neovim/pynvim>

Clone the repo:

    $ git clone https://github.com/neovim/pynvim

Then install the package like this:

    $ cd pynvim
    $ python -m pip install --user --upgrade .

The installation may fail because of a missing dependency, `msgpack`.

    Could not find a version that satisfies the requirement msgpack>=0.5.0 (from pynvim==0.3.1) (from versions: )
    No matching distribution found for msgpack>=0.5.0 (from pynvim==0.3.1)

In that case repeat the process:

    # https://pypi.org/project/msgpack/
    # https://github.com/msgpack/msgpack
    $ git clone https://github.com/msgpack/msgpack
    $ cd msgpack
    $ python -m pip install --user --upgrade .
    $ cd ../pynvim
    $ python -m pip install --user --upgrade .

---

Alternatively, try to use pip via a proxy:

    $ https_proxy=<IP Address>:<Port> python -m pip install --user <package>
      ^-----------------------------^

See here for more info: <https://stackoverflow.com/a/19962913/9780968>
And here for a list of proxies: <https://www.us-proxy.org/>
Make sure to choose a proxy supporting http**s**.

This solution works (even for `gem(1)`), but you may need to try several proxies
before finding one which succeeds in installing a package.

---

As a last resort, try to torify your command:

    $ . torsocks on
    $ sudo systemctl start tor.service
    $ python -m pip install --user <package>

Note that the second command may be optional.
It's possible  that you have a  tor daemon which runs  the service automatically
when the OS boots up:

    tor --defaults-torrc /usr/share/tor/tor-service-defaults-torrc -f /etc/tor/torrc --RunAsDaemon 0

But I'm  not sure  this is a  good idea; is  there a  risk the program  has been
tampered with?

## Why shouldn't I use `$ sudo pip`?

<https://github.com/zchee/deoplete-jedi/wiki/Setting-up-Python-for-Neovim#why-you-shouldnt-use-sudo>

##
# Todo
## learn how to use p(u)db

It seems that `pdb` is a module which is built by default into the python interpreter.
And `pudb` is a TUI front-end.
To install the latter:

    $ pip install pudb

- <https://documen.tician.de/pudb/starting.html>
- <https://realpython.com/python-debugging-pdb/>

---

Key bindings:

    ? = Help Menu
    C-P = Edit Preferences

Configuration settings are saved in `~/.config/pudb`.

---

Here is an  example of command that you  can run to debug epy  without having to
modify the script:

    $ python -m pudb $(which epy) /home/lgc/VCS/kitty/docs/_build/epub/kitty.epub

---

Note  that  some keys  can  interact  with  the  command-line window  (e.g.  `+`
increases  its height),  but  only  if you  focus  its  `<Clear>` button  (press
`Right`).

## write a custom theme

Put it here:

    ~/.config/pudb/theme.py

---

For a start, copy the relevant code from this file:

    # can be found with:  $ pip show -f pudb | grep theme
    /home/lgc/.local/lib/python3.8/site-packages/pudb/theme.py

## create a README file here:

    ~/.config/pudb/

And version control its contents.
