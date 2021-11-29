# Terminfo database
## Can a machine use several terminfo db?

Yes.  Each of these directories can be a db:

   - $HOME/.terminfo
   - /etc/terminfo
   - /usr/lib/terminfo
   - /usr/share/terminfo

## How to view all the entries in all the db?

           ┌ look in all terminal databases; not just the 1st one you find
           │
           │┌ sort the output according to the names of the terminals
           ││
    $ toe -as

Each of the listed directories is a database.

Each db contains a set of subdirectories, with 1-char names.
The  compiled terminal  descriptions are  placed inside  them, according  to the
first character in their canonical name.

For example, the description for `tmux` is inside the subdirectory `t/`.

### What does `*` and `+` mean in the output of the previous command?

When a terminal type is marked with:

   - `*`, it means a *conflicting* entry is present in another db
   - `+`, it means an *equivalent* entry is present in another db

To find the db which `*`/`+` refers to, get its position on the line, subtract 1
and divide by 2.  The result `n` matches  the `n`-th db listed at the top of the
output.

Example:

    --> /home/lgc/.terminfo
    ----> /etc/terminfo
    ------> /lib/terminfo
    --------> /usr/share/terminfo
    *-----+-:	9term     	Plan9 terminal emulator for X
    *---*---:	Eterm     	Eterm with xterm-style color support (X Window System)
        ^

The second `*` on the `Eterm` line refers to the 2nd db at the top:

    ----> /etc/terminfo

Because it's the 5th character on the line, and:  `(5 - 1) / 2 = 2`.

## How to find the db from which our terminal description comes from?

    $ infocmp -x

Look at the first line:

    Reconstructed via infocmp from file: /usr/lib/terminfo/s/screen-256color
                                         ├───────────────┘
                                         └ directory hierarchy

## What is the 'unknown' entry?

It describes  a terminal with minimal  capabilities, but which can  be used when
the real terminal type is unknown.

Here's the info, atm on my machine, for the unknown terminal:

    #   Reconstructed via infocmp from file: /usr/share/terminfo/u/unknown
    unknown|unknown terminal type,
            am, gn,
            cols#80,
            bel=^G, cr=^M, cud1=^J, ind=^J,

## How to install/build a terminfo db?

    $ sudo aptitude install ncurses-base ncurses-term

Installs terminfo descriptions for terminals.

`ncurses-term` installs a LOT of additional descriptions:

    $ dpkg -L ncurses-term

It's automatically installed (dependency) when you install
`rxvt-unicode-256color`.

---

            ┌ (--location) if the page has moved to a different location,
            │              redo the request on the new place
            │
            │┌ write output to a local file named like the remote file we get
            ││
    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ tic -sx terminfo.src

Procedure to build your own terminfo db.
Run these commands as a regular user.
Source: `:h terminfo` in Neovim.

## How to update the terminfo description for the current `$TERM`?

    $ curl -LO http://invisible-island.net/datafiles/current/terminfo.src.gz
    $ gunzip terminfo.src.gz
    $ tic -sx -e $TERM terminfo.src

##
## How to view the description of a terminal?

               ┌ include information for user-defined capabilities
               │
    $ infocmp -x
    $ infocmp -x tmux-256color
    $ infocmp -x unknown

View the description of:

   - the current terminal ($TERM)
   - `tmux-256color`
   - the unknown terminal

### How to configure it?

Edit the description of a terminal:

    $ infocmp -x [termname] >/tmp/entry

Edit the decompiled entry.

Compile the new entry:

    $ tic -sx /tmp/entry
           ││
           │└ include unknown capabilities as user-defined
           │
           └ summarize the compile by  showing  the  database  location  into
             which  entries  are written, and the number of entries which are
             compiled

`tic` is the `terminfo` compiler.

`tic` will compile the  data in a file named according to  the canonical name of
the terminal (first alias in the first field of the entry).

It will  also create  links for  all other  aliases, except  the last  one (long
description), so  that if your  `$TERM` does not use  the canonical name  of the
terminal but an alias, the programs will still be able to find its description.

##
## How does infocmp sort the capabilities?

According the the type of their value:

   1. boolean
   2. numeric
   3. string

## How to deal with a server whose terminfo db is incomplete?

                          ┌ FIXME:
                          │
                          │ What's `-t`?
                          │
                          │        Force pseudo-terminal allocation.   This can be
                          │        used to execute arbitrary screen-based programs
                          │        on a remote machine,  which can be very useful,
                          │        e.g. when implementing menu services.  Multiple
                          │        -t options  force tty  allocation, even  if ssh
                          │        has no local tty.
                          │
        infocmp -x | ssh -t root@remote-host '
        cat > "$TERM.info" && tic -sx "$TERM.info"'

    OR

        infocmp -x | ssh root@remote-host 'tic -sx -'

If you log in  to a remote machine, when the programs will  need to send control
sequences to the terminal  (or the tmux server), they will  look into the remote
terminfo db.
The latter may miss the entry for `$TERM`.

This should copy the local entry for the terminal in the db of the remote.

Source: <https://unix.stackexchange.com/a/67541/275162>

---

`$TERM`  will be  expanded before  starting the  remote shell,  so even  if it's
present in the `ssh` command, it will still match the local terminal.

---

Don't simply copy the local terminfo entry onto the remote.
There's no guarantee that the binary format is the same on both machines.

Besides, the  previous solution takes care  of giving the proper  permissions to
the generated  binary, and place it  in the correct directory  (creating missing
ones if necessary).

## Is there an equivalence between the capabilities of a terminal and its terminfo description?

No.

A terminal can have a capability which is absent from its description.  Ex:

    $ infocmp -1x xfce | grep smxx
    ''

    $ printf '\e[9m strikethrough \e[0m\n'
    ✔ strikes through the text in `xfce4-terminal`˜

#
# Syntax to write an entry
## How to include a comment in a terminfo file?

Prefix it with `#`.

## How to indent the file?

If an  entry is  written on  several lines of  the file,  they must  be indented
(except the first) with one literal tab character.

## Which characters are special? Where must they be used?

Each entry of the db is separated into fields, separated with commas.
The aliases in the first field are separated with bars.

The last field must be followed by a comma.

## What's the purpose of the first field? The next ones?

By convention:

   - the first field lists the alias names for the terminal

   - the first alias in the first field is the canonical name of the terminal
     the last alias in the first field is a long description of the terminal

   - the next fields specify the terminal capabilities

## How does a field (other than the first) begin?

With the name of a capability (2-5 char).

## What does an example of terminfo entry look like?

      wy50|WY50| Wyse Technology WY-50,
          am, cols#80, lines#24, cuu1=^K, clear=^Z,
          home=^^, cuf1=^L, cup=\E=%p1%'\s'%+%c%p2%'\s'%+%c,
    # ^--^                                                 ^
    # tab                                                  don't forget this last comma!

#
# Vim's builtin terminfo db
## How to view it?

In Vim:

    :put =execute('set termcap')

##
# Pitfalls
## `infocmp(1)` doesn't display the capabilities set via the tmux option 'terminal-overrides'!

Those are part of a db internal to tmux.
To view them, run `$ tmux info`.

