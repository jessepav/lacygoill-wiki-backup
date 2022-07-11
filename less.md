# Installation
## less

Go to: <http://www.greenwoodsoftware.com/less/download.html>
And download the archive and the signature.

Check the signature:

    $ gpg --verify less-590.sig less-590.tar.gz
    gpg: Signature made Thu 03 Jun 2021 07:45:49 PM CEST˜
    gpg:                using DSA key F153A7C833235259˜
    gpg: Can't check signature: No public key˜

    $ gpg --keyserver hkps://pgp.mit.edu/ --recv-keys F153A7C833235259
    gpg: key F153A7C833235259: public key "Mark Nudelman <markn@greenwoodsoftware.com>" imported˜
    gpg: Total number processed: 1˜
    gpg:               imported: 1˜

    $ gpg --edit-key F153A7C833235259
    gpg> trust
        5 = I trust ultimately

    $ gpg --verify less-590.sig less-590.tar.gz
    gpg: Signature made Thu 03 Jun 2021 07:45:49 PM CEST˜
    gpg:                using DSA key F153A7C833235259˜
    gpg: checking the trustdb˜
    gpg: marginals needed: 3  completes needed: 1  trust model: pgp˜
    gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u˜
    gpg: Good signature from "Mark Nudelman <markn@greenwoodsoftware.com>" [ultimate]˜

Configure, compile and install:

    $ cd less-550
    $ make clean && make distclean
    $ sh configure
    $ make
    $ sudo make install

Inform the system that the pager to use is in `/usr/local/bin/less`:

    $ sudo update-alternatives --install /usr/bin/pager pager /usr/local/bin/less 60
    $ sudo update-alternatives --set pager /usr/local/bin/less

This is necessary, for example, so that  `$ git diff` invokes our compiled less,
instead of writing its output directly onto the terminal.

## lesspipe

Useful to view the contents of compressed files or archives.

    $ git clone https://github.com/wofr06/lesspipe
    $ cd lesspipe

    # TODO: maybe you should set `LESS_ADVANCED_PREPROCESSOR` in `~/.config/fish/conf.d/environment.fish`
    $ make clean
    $ ./configure
    Activate syntax highlighting code [y/N] ? y˜

    interpret html, ps and other mostly ASCII files only if the˜
    ENV variable LESS_ADVANCED_PREPROCESSOR is set [y/N] ? y˜

    $ make
    $ sudo checkinstall --spec /dev/null

---

`lesspipe`  is included  by  default in  the `less`  package  on a  Debian-based
distro, but the script seems extremely old compared to github.

##
# What should I use instead of `$ tail -f log` to watch a log?

    $ less +F log
           ││
           │└ command: scroll forward, and keep trying to read when the end of file is reached
           │
           └ option: the remainder of that option must be taken as an initial command

## Why?

With `$ less +F`, you're not stuck at the end of the file, you can scroll back.

To do so, you need to interrupt the `F` command by pressing `C-c`.
At any  moment, you can re-execute  the `F` command  to keep trying to  read the
file if it's updated, by pressing `F`.

##
# filtering
## How to display only the lines matching `pat`?

Type the `&` command followed by `pat`:

    &pat

## How to display only the lines which do *not* match `pat`?

Type `!` after `&`:

    &!pat
     ^

## How to turn off a filtering?

Use an empty pattern; i.e. press `&` + `Enter`.

## How to suppress the special meaning of metacharacters?

Press `C-r` after `&`; for example, to look for all the lines containing a star:

    & C-r * Enter
        ^
        means: don't interpret *r*egular expression metacharacters

##
# Todo
## ?

Copy the contents of the man pages for less, lesskey and lesspipe and edit them.

Note that we've started configuring less in `~/.config/less/keys`, and in
`~/.config/fish/conf.d/environment.fish`.

---

Read: <http://www.greenwoodsoftware.com/less/faq.html>

