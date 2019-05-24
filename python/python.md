# Can a variable name begin with an underscore?   A number?

An underscore: yes.
A number: no.

##
##
# How to install python?
## Download

Go to the python download page: <https://www.python.org/downloads/release>

If you can't access the url, use our custom zsh shell function `tor`.

The latest release should be suggested in a button.
Atm it's `3.7.0`.
Don't click on the main button, instead click on the link which gives you access
to various installer formats: <https://www.python.org/downloads/release/python-370/>

Download the tarball of the installer, and its signature stored in a PGP ASCII Armored File:
<https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz>
<https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz.asc>

## Check the authenticity of the installer

Import the release manager public keys via the public key file:

    $ curl https://www.python.org/static/files/pubkeys.txt | gpg --import -

If you  can't download  `pubkeys.txt` with  `$ curl`, use  our custom  zsh shell
function `tor`; visit the url, right-click, `Save Page As...`.

Or grab the individual keys directly from the keyserver network:

    $ gpg --keyserver x-hkp://pool.sks-keyservers.net --recv-keys 6A45C816 36580288 7D9DC8D2 18ADD4FF A4135B38 A74B06BF EA5BBD71 E6DF025C AA65421D 6F5E1540 F73C700D 487034E5
                      │
                      └ You can find keyservers addresses here:

                            https://sks-keyservers.net/


Check the authenticity of the installer's tarball:

    $ gpg --verify Python-3.6.5.tgz.asc

You should read a message containing the text “Good signature from ...”:

    $ gpg --verify Python-3.6.5.tgz.asc
      gpg: assuming signed data in `Python-3.6.5.tgz'
      gpg: Signature made Wed 28 Mar 2018 12:28:12 PM CEST using RSA key ID AA65421D
      gpg: Good signature from "Ned Deily (Python release signing key) <nad@python.org>"
      gpg:                 aka "Ned Deily <nad@baybryj.net>"
      gpg:                 aka "keybase.io/nad <nad@keybase.io>"
      gpg:                 aka "Ned Deily (Python release signing key) <nad@acm.org>"
      gpg: WARNING: This key is not certified with a trusted signature!
      gpg:          There is no indication that the signature belongs to the owner.
      Primary key fingerprint: 0D96 DF4D 4110 E5C4 3FBF  B17F 2D34 7EA6 AA65 421D

To get rid of the warning:

    $ gpg --edit-key AA65421D
    gpg> trust
        1 = I don't know or won't say~
        2 = I do NOT trust~
        3 = I trust marginally~
        4 = I trust fully~
        5 = I trust ultimately~
        m = back to the main menu~
    Your decision? 5

See:
<https://serverfault.com/a/569923>
<https://security.stackexchange.com/a/69089>

## Extract the contents of the tarball

    $ xt Python-3.6.5.tgz

Don't extract the archive under `/run`; otherwise, the compilation will probably
fail because of a lack of space.

    /usr/bin/ld: final link failed: No space left on device
    collect2: error: ld returned 1 exit status
    Makefile:731: recipe for target 'Programs/_testembed' failed
    make: *** [Programs/_testembed] Error 1

Check how much space you have on the partition where you extract with `\df -h` or `dfc`.

<https://stackoverflow.com/a/31493804/9780968>
<https://unix.stackexchange.com/a/16158/289772>

## Dependencies

                                  ┌ for `checkinstall` to succeed later;
                                  │ otherwise: `ModuleNotFoundError: No module named '_ctypes'`
                                  │
    $ aptitude install libssl-dev libffi-dev

`libssl-dev` seems  important, otherwise, when,  later, you'll try to  install a
package with `pip`, you may fail:

    $ python3 -m pip install --user requests
    pip is configured  with locations that require  TLS/SSL, however the~
    ssl module in Python is not available.~

    ...~

    Could not find a version that satisfies the requirement requests (from versions: )~
    No matching distribution found for requests~

    Could not  fetch URL https://pypi.python.org/simple/requests/:~

    There was a problem confirming the ssl certificate:~
    HTTPSConnectionPool(host='pypi.python.org', port=443):~
    Max  retries   exceeded  with  url:  /simple/requests/   (Caused  by~
    SSLError("Can't connect to  HTTPS URL because the SSL  module is not~
    available.",)) - skipping.~

See also: <https://stackoverflow.com/a/41601137/9780968>

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
`--enable-optimizations` flag, because  the latter will cause `$  make` to start
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

##
## Install

    $ sudo checkinstall --pkgname mypython
                                  ^^

Immediately after  the install, try  to update your  system, and see  whether an
error occurs.

### Why not naming the package `python`?

This would shadow the default python2 package, and because many programs rely on
it, they'll all get broken.

### Why not naming the package `python3`?

Some programs rely on a specific (and older) version of `python3`.
They would get broken by a new version.

### I have installed the package and named it `python(3)` by accident!

Downgrade your `python(3)` package:

    # find the old (and more compatible) version
    $ apt-cache policy python(3)

    # downgrade the python package
    $ sudo apt-get install python(3)=<package-version-number>
                                     │
                                     └ Ex:   2.7.12-1~16.04
                                             3.5.1-3

Now, you  need to re-execute  `checkinstall`, because your compiled  package has
been removed in the process.

##
## Clean

    $ make clean && make distclean

##
# Interpreter
## How to see the list of all the interpreters installed on my machine?

    $ type -a python3
    python3 is /usr/local/bin/python3~
    python3 is /usr/bin/python3~
    python3 is /bin/python3~

### In the previous output, what's the absolute path of the interpreter which will be run when I invoke `$ python3`?

    /usr/local/bin/python3

### Which environment variable is responsible for this path having the biggest priority?

    $PATH

`/usr/local/bin` comes before `/usr/bin`.

##
## How to print “Hello world!”?

        >>> print("Hello world!")

## How to leave the Python prompt?

Press `C-d`, or execute `exit()`.

##
# Pip
## How to install pip?

If you  have a recent version  of Python (Python  2 >=2.7.9 or Python  3 >=3.4),
it's already installed.

If you've compiled it from source, make sure you've used the
`--with-ensurepip=install` option.

## How to update pip?

Like any other package:

    $ python[3] -m pip install --upgrade --user pip

##
## How to list all the python interpreters installed on my machine?

        $ type -a python
        $ type -a python3

## How to get the version of a specific interpreter?

        $ /path/to/interpreter --version

## How to show details about an installed package?

        $ python[3] -m pip show <package>

## How to list all python packages installed with `pip`?

        $ python[3] -m pip freeze

## How to save the state of the versions of all installed packages, then restore it later?

        $ python[3] -m pip freeze   > req.txt
        $ python[3] -m pip install -r req.txt

## How to list all python packages installed with `pip` but outdated?

        $ python  -m pip list --outdated
        $ python3 -m pip list --outdated

## How to list all installed packages which have unsatisfied dependencies?

        $ python[3] -m pip check

##
## How to install a package?

        $ python[3] -m pip install --user <package> ...
                                     │
                                     └ install it in `~/.local/lib/pythonX.Y/site-packages`

## How to install a package for a specific interpreter?

        $ /path/to/interpreter -m pip install <package>

## How to remove a package?

        $ python[3] -m pip uninstall <package> ...

##
## How to update an outdated package?

        $ python[3] -m pip install --user --upgrade <package> ...
                                            │
                                            └ -U is an alias

## How to deal with a package which can't be installed/updated?

Read the error message.
You may need  to install another python  or `.deb` package to  satisfy a missing
dependency.
Use commands such as:

        - pip install
        - apt-file search
        - aptitude install

##
## What's the effect of `python[3] -m` before a `pip` command?

It  lets you  choose in  the environment  of which  interpreter (python2  or the
python3) you want to work.
More specifically, the one called by the `python[3]` command.

Without `python[3] -m`, it seems you have no way of knowing in which environment
`pip` is going to work.

---

For example, at the moment, when I execute:

        $ pip show srt

There's no output.
Even though I have installed the `srt` package (for a python2 interpreter):

        $ python -m pip install --user srt

I think `pip show srt` checked for  a `srt` package for a `python3` interpreter,
instead of a `python2` one.
Indeed, atm, when I execute:

        $ pip show six

The output contains:

        Location: /home/user/.local/lib/python3.7/site-packages
                                              ^^^

---

Also, look here:
<https://docs.python.org/2/installing/#work-with-multiple-versions-of-python-installed-in-parallel>

##
# Documentation

https://docs.python.org/3/
https://pip.pypa.io/en/stable/user_guide/
https://pip.pypa.io/en/stable/reference/

##
# Issues
## My `pip` command fails!

Use the `-vvv` flag to make it more verbose, and read the messages to find where
the issue comes from.

Example:

    $ python3 -m pip -vvv install --user requests
                     ^^^^

---

If you can't install anything with pip, try updating it.
If you can't even update pip, then try  to install a newer version of the python
3 interpreter.
If  you configure  it with  `--with-ensurepip=install`, it  will also  install a
newer version of the pip package manager.

---

As a last resort, try to use pip via a proxy:

    $ https_proxy=<IP Address>:<Port> python3 -m pip install --user <package>

See here for more info: <https://stackoverflow.com/a/19962913/9780968>
And here for a list of proxies: <https://www.us-proxy.org/>
Make sure to choose a proxy supporting http*s*.

## Why shouldn't I use `$ sudo pip`?

<https://github.com/zchee/deoplete-jedi/wiki/Setting-up-Python-for-Neovim#why-you-shouldnt-use-sudo>

# Todo

Never use print for debugging again:
<https://github.com/cool-RR/PySnooper>

