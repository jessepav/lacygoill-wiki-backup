# What's a chunk?

A sequence of statements.

It can be  as simple as a  single statement, or it  can be composed of  a mix of
statements and function definitions.
It can be as large as you wish (even several megabytes).

It can be a file, or a single line in interactive mode.

# How to quit the stand-alone interpreter running in interactive mode?  (2)

Press `C-d`.

Run `os.exit()`.

# How to get the value of π?

    > math.pi

# How to assign the value `15` to the variable `a`?

    > a = 15

##
##
#
# LINKS

    http://lua-users.org/wiki/LuaStyleGuide

    https://rawgit.com/dlaurie/lua-notes/master/glossary.html

            A glossary of some essential Lua terms


    https://en.wikipedia.org/wiki/Category:Lua-scriptable_software

            Liste des programmes scriptables via Lua.  Entre autres:

                    - conky
                    - mpv
                    - nmap
                    - openwrt
                    - weechat
                    - wireshark


    https://www.reddit.com/r/lua/

            Subreddit Lua.  Jeter un oeil à la sidebar.


    https://www.lua.org/manual/5.3/readme.html
    https://www.lua.org/manual/5.3/manual.html#8

            Changements incompatibles entre Lua 5.2 et Lua 5.3


    https://luarocks.org/#quick-start

            Package manager pour gérer des modules Lua (appelés “rocks“).


    https://luarocks.org/stats/this-week

            Modules Lua les plus téléchargés la semaine dernière.


    https://github.com/LewisJEllis/awesome-lua

            A curated list of quality Lua packages and resources.


    http://www.inf.puc-rio.br/~roberto/lpeg/
    http://www.inf.puc-rio.br/~roberto/lpeg/re.html

    https://luarocks.org/search?q=lpeg
    https://luarocks.org/modules/gvvaughan/lpeg

            LPeg is  a new pattern-matching  library for Lua,  based on Parsing  Expression Grammars
            (PEGs).  The  nice thing about PEGs  is that it has  a formal basis (instead  of being an
            ad-hoc set  of features), allows an  efficient and simple implementation,  and does most
            things we  expect from  a pattern-matching library  (and more, as  we can  define entire
            grammars).

            Questions:

            `lpeg` a l'air puissant.
            Plus puissant que le moteur de regex intégré à Vim ?
            Si oui, permettrait-il d'avoir une meilleure coloration syntaxique ?
            Moins d'erreurs, et de meilleurs perf' ?
            Est-ce réservé aux devs de Vim, ou peut-on en profiter en tant que simple utilisateur
            via l'interface `lua` (:luafile, luaeval(), :luado).


    https://github.com/luafun/luafun
    https://luafun.github.io/

            Lua  Fun is  a high-performance  functional programming  library for  Lua designed  with
            LuaJIT's trace compiler in mind.

            Lua  Fun provides  a set  of  more than  50  programming primitives  typically found  in
            languages  like  Standard  ML,  Haskell,  Erlang,  JavaScript,  Python  and  even  Lisp.
            High-order functions  such as  map, filter,  reduce, zip,  etc., make  it easy  to write
            simple and efficient functional code.


                                     NOTE:

            Pas sûr que le projet soit stable et pérenne:
            https://github.com/luafun/luafun/issues/31


    https://github.com/rrthomas/luaposix
    https://luaposix.github.io/luaposix/


            Lua bindings for POSIX APIs.


    https://github.com/torch/paths

            This package provides portable functions and variables to manipulate the file system:

                    - Manipulating filenames : functions for manipulating filenames
                    - Directory functions : functions for listing and manipulating directories
                    - Directory paths : paths to well known directories
                    - Miscellaneous : uncategorized functions

            (probablement installable via luarocks)


    https://github.com/luvit/luv

            libuv bindings for luajit and lua 5.1/ 5.2/ 5.3.

            This library makes libuv available to lua scripts.  It was made for the luvit project but
            should usable from nearly any lua project.

            The best docs currently  are the libuv docs themselves.  Hopfully soon  we'll have a copy
            locally tailored for lua.


            https://github.com/libuv/libuv

            libuv is  a multi-platform  support library  with a  focus on  asynchronous I/O.  It was
            primarily developed for  use by Node.js, but  it's also used by Luvit,  Julia, pyuv, and
            others.

            Feature highlights

                    - Full-featured event loop backed by epoll, kqueue, IOCP, event ports
                    - Asynchronous TCP and UDP sockets
                    - Asynchronous DNS resolution
                    - Asynchronous file and file system operations
                    - File system events
                    - ANSI escape code controlled TTY
                    - IPC with socket sharing, using Unix domain sockets or named pipes (Windows)
                    - Child processes
                    - Thread pool
                    - Signal handling
                    - High resolution clock
                    - Threading and synchronization primitives

            http://docs.libuv.org/en/v1.x/


    https://github.com/duncanc/icu4lua

            Lua has  no Unicode  support (at  the very least  you don't  get string.len  and pattern
            matching functions to recognize Unicode characters).  This link provides a binding to ICU
            library that implements full Unicode support.

            To read the doc, save the next link in `/tmp/html.html` and open in Firefox:
            https://raw.githubusercontent.com/duncanc/icu4lua/master/doc/index.html


                                     NOTE:

            En fait, depuis la version 5.3, Lua intègre une librairie gérant l'UTF-8.
            https://www.lua.org/manual/5.3/manual.html#6.5


    https://github.com/stevedonovan/Penlight
    https://stevedonovan.github.io/Penlight/api/manual/01-introduction.md.html

            Penlight  is a  collection of  useful  libraries, partly  based on  the Python  standard
            libraries,  but  also  providing useful  ways  to  process  input  data.  The  only  real
            prerequisite is LuaFileSystem (for some libraries), although Alien is also needed if you
            wish pl.dir.copyfile to work properly on Windows.

            pl.path and pl.dir provide platform-independent ways to work with files and directories.
            Also included is NickTrout's Python List class,  as well as a class which implements the
            Python string interface.

            pl.tablex provides  extended operations  on tables, such  as deepcompare  and functional
            forms such as map,filter and reduce.

            There is also PenlightLibraries.


    http://notebook.kulchenko.com/programming/lua-good-different-bad-and-ugly-parts

            Lien intéressant intitulé “Lua: Good, bad, and ugly parts“.
            Lire en particulier les parties “bad“ et “ugly“, entre autres car elles peuvent nous faire
            découvrir des librairies.


    https://stackoverflow.com/questions/154672/what-can-i-do-to-increase-the-performance-of-a-lua-program
    https://www.lua.org/gems/sample.pdf
    http://lua-users.org/wiki/OptimisationTips

            Conseils pour optimiser son code Lua.


    https://github.com/tpope/vim-haystack/blob/master/autoload/haystack.vim

            justinmk dit que convertir ce plugin VimL en Lua aurait de la valeur:
            https://www.reddit.com/r/neovim/comments/6bfn33/any_documentation_on_how_to_use_native_lua/dhmifjl/

            Lire `:h lua`.

# LOVE

    https://www.reddit.com/r/gamedev/comments/67frk2/tutorial_on_making_a_complete_game_with_lua_and/
    https://love2d.org/
    https://github.com/SSYGEA/blog/issues/11
    https://github.com/SSYGEA/blog/issues/12
    https://github.com/SSYGEA/blog/issues/13
    https://github.com/SSYGEA/blog/issues/14

            Série de tutos pour apprendre à coder un jeu en Lua.

            Procédure d'installation du framework LÖVE:

                    hg clone https://bitbucket.org/rude/love

                    sudo aptitude install build-essential \
                                        autotools-dev \
                                        automake \
                                        libtool \
                                        pkg-config \
                                        libdevil-dev \
                                        libfreetype6-dev \
                                        libluajit-5.1-dev \
                                        libphysfs-dev \
                                        libsdl2-dev \
                                        libopenal-dev \
                                        libogg-dev \
                                        libvorbis-dev \
                                        libflac-dev \
                                        libflac++-dev \
                                        libmodplug-dev \
                                        libmpg123-dev \
                                        libmng-dev \
                                        libturbojpeg \
                                        libtheora-dev

                    ./platform/unix/automagic
                    ./configure
                    make

            En cas de problème, lire:
            https://love2d.org/wiki/Building_L%C3%96VE

            Pour apprendre à utiliser le framework:
            https://love2d.org/wiki/Getting_Started

