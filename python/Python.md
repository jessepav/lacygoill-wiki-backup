# How to install the most recent python interpreter?
## Download

Go to the python download page: <https://www.python.org/downloads>

If you can't access the URL, use our custom shell function `tor`:
<https://github.com/lacygoill/config/blob/master/.config/fish/functions/tor.fish>

The latest release should be suggested by a large button.
ATM it's `3.10.6`.
Don't click on the main button, instead use `aria2c(1)`:

    $ aria2c https://www.python.org/ftp/python/3.10.6/Python-3.10.6.tar.xz
    $ aria2c https://www.python.org/ftp/python/3.10.6/Python-3.10.6.tar.xz.asc

The commands download 2 archives: one  containing the installer, the other a PGP
ASCII Armored File.

## Check the authenticity of the installer

Import the OpenPGP key of the release manager:

    $ gpg --keyserver=hkps://pgp.mit.edu/ --recv-keys 64E628F8D684696D
                                                      ^--------------^

The key ID can be found on the download web page: <https://www.python.org/downloads>
Under the section "OpenPGP Public Keys":

       release manager
    v-------------------v
    Pablo Galindo Salgado (3.10.x and 3.11.x source files and tags) (key id: 64E628F8D684696D)
                                                                             ^--------------^

If the previous shell command fails, click on the name of the release manager.
ATM, it opens this page:
<https://keybase.io/pablogsal/>

Inside this page, click on the key  ID; inside the popup window, you should find
a `gpg(1)` command such as:

    $ curl https://keybase.io/pablogsal/pgp_keys.asc | gpg --import

Now, check the authenticity of the installer's archive:

    $ gpg --verify Python-3.10.6.tar.xz.asc

You should read a message containing the text “Good signature from ...”:

    gpg: assuming signed data in 'Python-3.10.6.tar.xz'
    gpg: Signature made Mon 01 Aug 2022 10:39:02 PM CEST
    gpg:                using RSA key CFDCA245B1043CF2A5F97865FFE87404168BD847
    gpg: Good signature from "Pablo Galindo Salgado <pablogsal@gmail.com>" [unknown]
    gpg: WARNING: This key is not certified with a trusted signature!
    gpg:          There is no indication that the signature belongs to the owner.
    Primary key fingerprint: A035 C8C1 9219 BA82 1ECE  A86B 64E6 28F8 D684 696D
         Subkey fingerprint: CFDC A245 B104 3CF2 A5F9  7865 FFE8 7404 168B D847

To get rid of the warning:

                     ID of the key used to make the signature,
                     as given on the 3rd line of the previous command's output
                     v--------------------------------------v
    $ gpg --edit-key CFDCA245B1043CF2A5F97865FFE87404168BD847
    gpg> trust
        1 = I don't know or won't say
        2 = I do NOT trust
        3 = I trust marginally
        4 = I trust fully
        5 = I trust ultimately
        m = back to the main menu
    Your decision? 5
                   ^
                   choose to trust the key ultimately

Now, if you re-run the `--verify` command, there should be no warning anymore:

    $ gpg --verify Python-3.10.6.tar.xz.asc
    gpg: assuming signed data in 'Python-3.10.6.tar.xz'
    gpg: Signature made Mon 01 Aug 2022 10:39:02 PM CEST
    gpg:                using RSA key CFDCA245B1043CF2A5F97865FFE87404168BD847
    gpg: Good signature from "Pablo Galindo Salgado <pablogsal@gmail.com>" [ultimate]

See:

- <https://serverfault.com/a/569923>
- <https://security.stackexchange.com/a/69089>

## Extract the contents of the archive

    $ tar xf Python-3.10.6.tar.xz
    $ rm Python-3.10.6.tar.xz
    $ cd Python-3.10.6

Don't extract the archive under `/run`; otherwise, the compilation will probably
fail because of a lack of space.

    /usr/bin/ld: final link failed: No space left on device
    collect2: error: ld returned 1 exit status
    Makefile:731: recipe for target 'Programs/_testembed' failed
    make: *** [Programs/_testembed] Error 1

Check how much space you have on  the partition where you extract with `$ df -h`
or `dfc(1)`.

- <https://stackoverflow.com/a/31493804/9780968>
- <https://unix.stackexchange.com/a/16158/289772>

## Dependencies

    $ sudo apt install libssl-dev libffi-dev

Without `libssl-dev`,  later, you might  not be able  to install a  package with
`pip(3)`:

    $ python -m pip install --user --upgrade requests
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

    $ ./configure --with-ensurepip=install --with-readline

`--with-ensurepip` installs pip module, which you'll need to run commands such as:

    $ python -m pip install --user --upgrade <package>

---

To learn how to configure the build:

    $ vim README.rst
    $ ./configure --help

---

`--enable-optimizations` (and  `--with-lto`) enables some  optimizations (making
the python binary around 10% faster).

However, it increases the build time a lot (from a few minutes, to maybe half an
hour  or more).   To keep  the  build time  reasonable,  you would  need to  set
`PROFILE_TASK` to prevent some long tests to be run.

For more info, see:

   - <https://bugs.python.org/issue36044#msg347649>
   - <https://github.com/docker-library/python/issues/160#issuecomment-509426916>

## Compile

    $ make

## Test (optional)

    $ make test

Note that  `--enable-optimizations` already  run all the  tests (unless  you set
`PROFILE_TASK`).

If a  message is  printed about a  failed test  or a traceback  or core  dump is
produced, something is wrong.
You can re-run the failing test(s) in verbose mode::

    $ make test TESTOPTS='-v test_that_failed'

A failed test might be due to  a missing python package necessary to perform the
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

    $ python3.10
    $ python3.10 -m pip install --user --upgrade <package>
    ...

## Clean

    $ sudo make clean && sudo make distclean

##
# How does Python compute an integer division, where one of the operands is negative?

The result is rounded down:
```python
print(-7 // 4)
```
    -2

If you prefer the result to be rounded up (i.e. the fractional to be discarded),
use the `int()` function:
```python
print(int(-7 / 4))
```
    -1

Notice that this time, we used the `/` operator, instead of `//`.
The former  returns the *algebraic* quotient  of its operands, while  the latter
returns the *floored* quotient of its operands.

# How is a floating point number stored internally?

It's  represented according  to the  IEEE 754  double-precision binary  floating
point  format, which  is stored  in 64  bits of  information divided  into three
sections: sign, exponent, and mantissa.

##
# In which order should the various kinds of parameters be declared in a function header?

   1. mandatory (aka non-default) parameters (`param`)
   2. optional (aka default) parameters (`param='value'`)
   3. parameter for variadic arguments (`*param`)
   4. parameter for variadic keyword arguments (`**param`)

---

Usually, mandatory parameters should come first.
You can't put optional parameters before:
```python
def func(optional=123, mandatory):
    pass
```
    SyntaxError: non-default argument follows default argument

Nor the parameter for variadic keyword arguments:
```python
def func(**kwargs, mandatory):
    pass
```
    SyntaxError: invalid syntax

---

The parameter for variadic keyword arguments must come last.
Nothing can come after.  Neither mandatory parameters:
```python
def func(**kwargs, mandatory):
    pass
```
    SyntaxError: invalid syntax

Nor optional parameters:
```python
def func(**kwargs, optional=0):
    pass
```
    SyntaxError: invalid syntax

Nor the parameter for variadic arguments:
```python
def func(**kwargs, *args):
    pass
```
    SyntaxError: invalid syntax

## Which exception to this order is allowed?

You  can  put  the  parameter   for  variadic  arguments  before  the  mandatory
parameters:
```python
def func(*args, mandatory):
    pass
```
But only in Python 3 (not in Python 2).
And if  you do  so, the mandatory  parameters can only  be assigned  via keyword
arguments (not positional ones):
```python
def func(*args, mandatory):
    pass

 #      ✘
 #      v
func(1, 2)
```
    TypeError: func() missing 1 required keyword-only argument: 'mandatory'
```python
def func(*args, mandatory):
    print(mandatory)

 #           ✔
 #      v---------v
func(1, mandatory=2)
```
    2

IOW,  you  can  only  move  the parameter  for  variadic  arguments  before  the
keyword-only parameters;  not before the positional-only  parameters, nor before
the positional-or-keyword parameters.

##
# How does Python assigns the arguments from a function call to the parameters in the function header?

First, it  assigns the positional  arguments (i.e. which  are not prefixed  by a
keyword, and which can be assigned to a non-variadic parameter).

Then, it assigns the keyword arguments  (i.e. which *are* prefixed by a keyword,
and which can be assigned to a non-variadic parameter).

Finally, all remaining non-keyword arguments –  if any – are assigned to the
parameter for variadic arguments (via a single tuple).
Similarly, all  remaining keyword arguments –  if any – are  assigned to the
parameter for variadic keyword arguments (via a single dictionary).

##
# When is a keyword argument necessary?

Obviously, you have to use a keyword argument to assign a keyword-only parameter
(i.e. a  parameter which is declared  after the special parameter  `*`, or after
the parameter for variadic arguments).

But you might also need one when you want to skip over some optional argument(s)
in a function call.

For example, suppose a function accepts  2 optional arguments, and in a function
call you need to pass a value for  the 2nd argument, but not for the 1st (you're
OK with its default value).  If you want  to skip the latter, you need a keyword
argument:
```python
def my_function(opt1=12, opt2=34):
    print(opt1, opt2)

my_function(opt2=56)
 #          ^-----^
```
    12 56

Without,  you would  have  to specify  the  default value  of  the 1st  optional
argument in the function call:
```python
def my_function(opt1=12, opt2=34):
    print(opt1, opt2)

my_function(12, 56)
 #          ^^
```
## When should I use one (even if not stricly required)?

Whenever its meaning is not easy to understand from the context.
The context being the name of the function, and the position of the argument.

##
# What's the difference between a script and a module?  (2)

When a file is executed as a script, `__name__` has the value `'__main__'`.
When it's imported as a module, it's `'script'`.
BTW, `__name__` is a global variable.

---

A module is compiled under `__pycache__/`, not a script.

##
# Issues
## My `pip` command fails!

Use the `-vvv` flag to make it more verbose, and read the messages to find where
the issue comes from.

Example:

    $ python -m pip -vvv install --user --upgrade <package>
                    ^--^

---

If you can't install anything with pip, try updating it:

    $ python -m pip install --user --upgrade pip

---

You can also install the package manually.

First, find it on `https://pypi.org/`.
For example, for the pynvim package, the URL is:

<https://pypi.org/project/pynvim/>

Next, click on `Homepage` and you'll get this URL:

<https://github.com/neovim/pynvim>

Clone the repo:

    $ git clone https://github.com/neovim/pynvim

Then install the package like this:

    $ cd pynvim
    $ python -m pip install --user --upgrade .

The installation might fail because of a missing dependency, `msgpack`.

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

This  solution works  (even for  `gem(1)`), but  you might  need to  try several
proxies before finding one which succeeds in installing a package.

---

As a last resort, try to Torify your command:

    $ . torsocks on
    $ sudo systemctl start tor.service
    $ python -m pip install --user <package>

Note that the second command might be optional.
It's possible  that you have a  Tor daemon which runs  the service automatically
when the OS boots up:

    tor --defaults-torrc /usr/share/tor/tor-service-defaults-torrc -f /etc/tor/torrc --RunAsDaemon 0

But I'm  not sure  this is a  good idea; is  there a  risk the program  has been
tampered with?

## Why shouldn't I use `$ sudo pip`?

Mainly for 2 reasons: stability and security.

For stability: Your Python installation is handled by your package manager (e.g.
`apt(8)`).   You don't  want to  change the  state of  this installation  with 2
different tools:  package manager +  `pip(8)`.  They  are not aware  of whatever
change is performed  by the other.  Your  Python installation is a  part of your
OS; thus, it's meant  to be handled by your package manager.  Let  it do its job
properly without having another tool messing up its work.

For  security: `pip(1)`  runs  a  `setup.py` script.   It  that script  contains
malicious  code (because  the  project  you're downloading  code  from has  been
somehow compromised), you don't want it  to run with root privileges, with which
it could do more damage.
