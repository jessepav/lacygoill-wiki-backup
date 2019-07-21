# Installation
## less

Go to: <http://www.greenwoodsoftware.com/less/download.html>
And download the archive and the signature.

Check the signature:

    $ gpg --verify less-550.sig less-550.tar.gz
    gpg: Signature made Sat 16 Feb 2019 11:24:15 PM CET using DSA key ID 33235259~
    gpg: Can't check signature: public key not found~

    $ gpg --keyserver x-hkp://pool.sks-keyservers.net --recv-keys 33235259
    gpg: requesting key 33235259 from hkp server pool.sks-keyservers.net~
    gpg: key 33235259: public key "Mark Nudelman <markn@greenwoodsoftware.com>" imported~
    gpg: Total number processed: 1~
    gpg:               imported: 1~

    $ gpg --edit-key 33235259
    > trust
        5 = I trust ultimately

    $ gpg --verify less-550.sig less-550.tar.gz
    gpg: Signature made Sat 16 Feb 2019 11:24:15 PM CET using DSA key ID 33235259~
    gpg: checking the trustdb~
    gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model~
    gpg: depth: 0  valid:   4  signed:   3  trust: 0-, 0q, 0n, 0m, 0f, 4u~
    gpg: depth: 1  valid:   3  signed:   2  trust: 3-, 0q, 0n, 0m, 0f, 0u~
    gpg: next trustdb check due at 2023-09-25~
    gpg: Good signature from "Mark Nudelman <markn@greenwoodsoftware.com>"~

Configure, compile and install:

    $ cd less-550
    $ make clean && make distclean
    $ sh configure
    $ make
    $ sudo checkinstall

TODO: `$ git diff` won't use this new `$ less`.
Many other things will probably won't work too.
I think that's because of the new location (`/usr/local/bin/less` vs `/bin/less`).
Before `$ make`, you'll need to set the prefix to `/` instead of `/usr/local/`.
Or, you'll need to configure the system so that it uses `/usr/local/bin/less`;
try `$ update-alternatives --config pager`, or sth similar.

## lesspipe

Useful to view the contents of compressed files or archives.

    $ git clone https://github.com/wofr06/lesspipe
    $ cd lesspipe

    # TODO: maybe you should set `LESS_ADVANCED_PREPROCESSOR` in `~/.zshenv`
    $ ./configure
    Activate syntax highlighting code [y/N] ? y~

    interpret html, ps and other mostly ASCII files only if the~
    ENV variable LESS_ADVANCED_PREPROCESSOR is set [y/N] ? y~

    $ make
    $ sudo cp lesspipe.sh code2color /usr/local/bin

    # to reset the contents of a field to a default value,
    # type its index then press Enter without filling anything

---

`lesspipe`  is included  by  default in  the `less`  package  on a  debian-based
distro, but the script seems extremely old compared to github.

##
# What should I use instead of `$ tail -f log` to watch a log?  Why?

        $ less +F log
               ││
               │└ command: scroll forward, and keep trying to read when the end of file is reached
               │
               └ option: the remainder of that option must be taken as an initial command

With `$ less +F`, you're not stuck at the end of the file, you can scroll back.

To do so, you need to interrupt the `F` command by pressing `C-c`.
At any  moment, you can re-execute  the `F` command  to keep trying to  read the
file if it's updated, by pressing `F`.

##
# TODO
## ?

Copy the contents of the manpages for less, lesskey and lesspipe and edit them.

Note that we've started configuring less in `~/.config/lesskey`, and in `~/.zshenv`.

---

Read: <http://www.greenwoodsoftware.com/less/faq.html>

