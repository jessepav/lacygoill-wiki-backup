# Terminfo database
## Can a machine use several terminfo db?

Yes. Each of these directories can be a db:

   • $HOME/.terminfo
   • /etc/terminfo
   • /usr/lib/terminfo
   • /usr/share/terminfo

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

## How to find the db from which our terminal description comes from?

        $ infocmp -x

Look at the first line:

        Reconstructed via infocmp from file: /usr/lib/terminfo/s/screen-256color
                                             └───────────────┤
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

        $ aptitude install ncurses-base ncurses-term

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
        $ tic -x terminfo.src

Procedure to build your own terminfo db.
Run these commands as a regular user.
Source: `:h terminfo` in Neovim.

##
## How to view the description of a terminal?

                   ┌ include information for user-defined capabilities
                   │
        $ infocmp -x
        $ infocmp -x tmux-256color
        $ infocmp -x unknown

View the description of:

   • the current terminal ($TERM)
   • `tmux-256color`
   • the unknown terminal

### How to configure it?

        $ infocmp -x [termname]

        # edit the decompiled entry

        $ tic -x
               │
               └ include unknown capabilities as user-defined

Edit the description of a terminal.

`tic` is the `terminfo` compiler.

`tic` will compile the  data in a file named according to  the canonical name of
the terminal (first alias in the first field of the entry).

It will  also create  links for  all other  aliases, except  the last  one (long
description), so  that if your  `$TERM` does not use  the canonical name  of the
terminal but an alias, the programs will still be able to find its description.

##
## Does infocmp sort the capabilities?

Yes. According the the type of their value:

   1. boolean
   2. numeric
   3. string

## Does infocmp show the capabilities customized via the tmux option 'terminal-overrides'?

No.

It only shows the default db (external to tmux); not the one internal to tmux.
Use `$ tmux info` instead.

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
        cat > "$TERM.info" && tic -x "$TERM.info"'

    OR

        infocmp -x | ssh root@remote-host 'tic -x -'

If you log in  to a remote machine, when the programs will  need to send control
sequences to the terminal  (or the tmux server), they will  look into the remote
terminfo db.
The latter may miss the entry for `$TERM`.

This should copy the local entry for the terminal in the db of the remote.

Source:

        https://unix.stackexchange.com/a/67541/275162

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

A terminal can have a capability which is absent from its description. Ex:

    infocmp -x xfce
    ∅ no smxx capability (strikethrough style)~

    printf '\e[9m   strikethrough  \e[0m\n'
    ✔ strikes through the text in `xfce4-terminal`~

#
# Syntax to write an entry
## How to include a comment in a termcap/terminfo file?

Prefix it with `#`.

## How to indent the file?

If an  entry is  written on  several lines of  the file,  they must  be indented
(except the first) with one literal tab character.

## Which characters are special? Where must they be used?

Each entry of  the db is separated into fields,  separated with COLONS (termcap)
or COMMAS (terminfo). The aliases in the first field are separated with BARS.


A termcap entry must be defined on a single logical line.
Therefore, a BACKSLASH is needed to suppress a newline (like in bash/zsh).
A terminfo entry doesn't need to be on a single line.
Therefore, a backslash is not needed to suppress a newline.


In the terminfo db, the last field must be followed by a comma.

## What's the purpose of the first field? The next ones?

By convention:

    • the first field lists the alias names for the terminal

    • the first alias in the first field is the canonical name of the terminal
      the last alias in the first field is a long description of the terminal

    • the next fields specify the terminal capabilities

## How does a field (other than the first) begin?

With the name of a capability (2-char in termcap; 2-5 char in terminfo).

## What does an example of termcap/terminfo entry look like?

    n9|wy50|WY50| Wyse Technology WY-50:\
        :bs:am:co#80:li#24:\
        :up=^K:cl=^Z:ho=^^:nd=^L:cm=\E=%+ %+ :
  # ^^^^                │
  # tab                 C-^

        Partial description of a termcap entry.


    wy50|WY50| Wyse Technology WY-50,
        am, cols#80, lines#24, cuu1=^K, clear=^Z,
        home=^^, cuf1=^L, cup=\E=%p1%'\s'%+%c%p2%'\s'%+%c,
  # ^^^^                                                 ^
  # tab                                                  don't forget this last comma!

        Partial description of a terminfo entry.

#
# (Neo)Vim's builtin termcap/terminfo db
## How to view it?

In Vim:

        :put =execute('set termcap')

In Neovim:

        $ nvim -V3/tmp/log file
        :q
        $ nvim /tmp/log
        :sil exe '1,/{{{$/g/^/d_' | /}}}$/,$g/^/d_

