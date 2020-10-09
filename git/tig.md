# How to install tig?

    $ git clone https://github.com/jonas/tig && cd tig
    $ make configure
    $ ./configure --with-readline --with-ncursesw
    $ make
    $ sudo make install

During  the configuration,  `--with-readline` is  necessary for  tig to  support
readline commands  in various prompts.   And `--with-ncursesw` is  necessary for
tig to be able  to display some unicode characters (e.g. the ones  we use in our
Vim diagrams).

##
# Where can I find
## tig's documentation?

   - `man tig` (196 lines)
   - `man tigrc` (987 lines)
   - `man tigmanual` (650 lines)

## an example of config file?

    /usr/local/etc/tigrc

##
# Todo
## <https://github.com/iberianpig/tig-explorer.vim>

Is it worth integrating this Vim plugin in our workflow?

