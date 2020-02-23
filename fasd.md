# What's the purpose of fasd?

It  allows  you  to  *quickly  reference*  a file  or  directory  while  on  the
command-line, provided that you accessed it in the past.

##
# Installation

    $ git clone https://github.com/clvv/fasd
    $ sudo make install

##
# Synopsis

    $ fasd [options] [query ...]

    $ [f|a|s|d] [options] [query ...]

    $ j [query ...]

## What does `f` execute? `a`? `s`? `d`?

They are aliases using the fasd command:

    $ type f
    f is an alias for fasd -f~

    $ type a
    ... fasd -a~

    $ type s
    ... fasd -si~

    $ type d
    ... fasd -d~

## What does `j` execute? `jj`?

They are aliases using the `fasd_cd` shell function:

    $ type j
    ... fasd_cd -d~

    $ type jj
    ... fasd_cd -d -i~

    $ type fasd_cd
    fasd_cd is a shell function from ~/.fasd-init-zsh ~

## Why aren't they using the same command/function?

`fasd` can't implement `j`  nor `jj` because it's an external  program, and as a
result it can't change the state of the current shell.

So, `j` and `jj` must be implemented by a shell function.

##
## What is the difference between the options `-a` and `-s`?

There doesn't seem to be any difference between them:

   - `-s`   ⇔ `-a`
   - `-si`  ⇔ `-ai`
   - `-sid` ⇔ `-aid`
   - `-sif` ⇔ `-aif`

## Which word(s) is `s` the initial of?

`s` refers to `s`how, or `s`earch, or `s`elect.

##
# Configuration
## Where is fasd's configuration file located?

    ~/.fasdrc

### Which of the variables it contains can be exported in the shell environment?

None, except `_FASD_RO`.

### Why don't I need to restart a shell after changing the value of a fasd variable?

The file is read on every invocation of a fasd command.

`/etc/fasdrc` is also read.

##
## Where is fasd's database?

    ~/.fasd

### How can I change its location?

Assign the desired path to `_FASD_DATA` in `~/.fasdrc`.

### How can I limit its size?

Set `_FASD_MAX` appropriately.

Its default value is  2000, which means that the database should  not be able to
contain more than about 2000 entries.

However, for some  reason, the database seems  to be able to contain  a few more
entries:

    $ cat <<'EOF' >>~/.fasdrc
    _FASD_DATA=/tmp/.fasd
    _FASD_MAX=1
    EOF

    $ cd /dev
    $ cd /media
    $ cd /opt
    $ cd /var

    # only 3 entries instead of 4
    $ d
    5.4        /opt~
    5.4        /var~
    9.72       /media~

##
## How to disable fasd entirely?

Set `_FASD_RO` to any non-empty string in `~/.fasdrc`.

Note that when fasd is disabled, you can't manually add or remove paths from the
database with `-A` and `-D`.

##
## How to make fasd ignore
### the command-line based on a command name?

Set the variable `_FASD_IGNORE` appropriately.

Its default value is `fasd ls echo`.

### the command-line based on a string?

Set the variable `_FASD_BLACKLIST` appropriately.

Its default value is `--help`.
So any command containing `--help` won't be processed.

### the first word of the command-line?

Set `_FASD_SHIFT` appropriately.

Its default  value is `sudo  busybox`, so any  command beginning with  `sudo` or
`busybox` will  be shifted; i.e. it  will be processed  as if it began  from the
following word.

##
## How to add or remove a path from fasd's database?

Use resp. the `-A` and `-D` options:

    $ fasd [-A|-D] paths ...

Example:

    $ mkdir /tmp/.dir{1,2}
    $ fasd -A /tmp/.dir{1,2}
    $ fasd | grep '.dir[12]'
    6          /tmp/.dir1~
    6          /tmp/.dir2~

    $ fasd -D /tmp/.dir{1,2}
    $ fasd | grep '.dir[12]'
    ''~

Note that the paths must match existing files or directories.

## How to remove all the paths matching `pat` from fasd's database?

Use `` `a | grep pat` `` to get the relevant paths, and feed them to `fasd -D`:

    $ touch /tmp/.pat{1..3}
    $ fasd -A /tmp/.pat{1..3}
    $ a | grep pat
    6          /tmp/.pat1~
    6          /tmp/.pat2~
    6          /tmp/.pat3~

    $ fasd -D `a | grep pat`
    $ a | grep pat
    ''~

##
## How to create the alias `x` to run `cmd` on
### a file opened in the past?

    $ alias x='fasd -f -e cmd'

Or:

    $ alias x='f -e cmd'

### a directory opened in the past?

    $ alias x='fasd -d -e cmd'

Or:

    $ alias x='d -e cmd'

### a file or directory opened in the past?

    $ alias x='fasd -a -e cmd'

Or:

    $ alias x='a -e cmd'

##
# Backends
## How to punctually make fasd consider
### an additional backend?

Use the `-B` option:

    $ fasd -f -B viminfo

### only one specific backend?

Use the `-b` option:

    $ fasd -f -b viminfo

##
## What are the three additional backends provided by fasd?

   - current: provides any file or subdirectory in the current working directory

   - viminfo: Vim's editing history

     The path to this file can be controlled via `_FASD_VIMINFO`.

   - recently-used: GTK's recently-used file

        ~/.local/share/recently-used.xbel

     The path to this file can be controlled via `_FASD_RECENTLY_USED_XBEL`.

### How can I use one of them by default?

Set the variable `_FASD_BACKENDS` appropriately:

    _FASD_BACKENDS=viminfo

##
## How can I define my own backend?

Define a shell function in `~/.fasdrc`, and assign its name to `_FASD_BACKENDS`:

    func() {
        echo '/tmp/.file'
    }
    _FASD_BACKENDS=func

## How to use several backends by default?

Concatenate their names by separating them with spaces, and assign the result as
a string to `_FASD_BACKENDS`.

    funcA() {
        echo '/tmp/.file1'
    }
    funcB() {
        echo '/tmp/.file2'
    }
    _FASD_BACKENDS='funcA funcB'

##
# Getting info
## How to get a reminder of all possible options?

Use the `-h` option:

    $ fasd -h

##
## How to list frecent files?  directories?  files+directories?

    $ f
    $ d
    $ a

## How to list the paths in fasd's database with and without their scores?

Use resp. the `-s` and `-l` options:

    $ fasd -s
    $ fasd -l

##
## How to reverse any listing?

Use the `-R` option:

    $ fasd -lR
    $ fasd -fR
    $ fasd -dR
    ...

## How to get the nth entry from a listing?

Pass its index as an option:

    $ fasd -123

Note that the indexing start from 1, and from the bottom.
So to get the last entry, you would use the option `-1`, the last but one entry `-2`, ...

## How to limit a listing to the entries matching foo?

Pass the query 'foo' to the fasd command:

    $ fasd -l foo
    $ fasd -s foo

    $ fasd -f foo
    $ fasd -d foo
    $ fasd -a foo

##
## When does fasd limit a listing to only the best match?

When it's being called inside a subshell, *not* interactively, *and* it's passed
a query:

    $ touch /tmp/.file{1..3}
    $ fasd -A /tmp/.file{1..3}

    # only passing a query will not limit the listing to the best match
    $ f file
    6          /tmp/.file1~
    6          /tmp/.file2~
    6          /tmp/.file3~

    # same thing when only using a subshell
    $ echo `f`
    ...~

    # finally the listing is limited to the best match
    $ echo `f file`
    /tmp/.file3~

    # but not if fasd is called interactively
    $ echo `f -i file`
    6          /tmp/.file1~
    6          /tmp/.file2~
    6          /tmp/.file3~

    $ fasd -D /tmp/.file{1..3}

---

This allows you to do things like:

    # move `file` to the most frecent directory matching `www`
    $ mv file `d www`

    # copy the most frecent file matching `foo` and `bar` into the cwd
    $ cp `f foo bar` .

---

Inside a pipeline, commands are run in subshells (except the last one?), so when
you run this:

    $ f pdf | fzf

`fasd` is run in a subshell.

##
# Queries
## On which conditions do queries passed to fasd match a path?  (2)

They must match the path *in order*.
The *last* query must match the *last* component of the path.

### If no match is found, how does fasd re-compare the queries with the path?

It tries the same process, but this time it ignores the case.

#### If no match is found, how does fasd re-re-compare the queries with the path?

It tries the same process, but this time it allows extra characters to be placed
between query characters for fuzzy matching.
The exact number can be controlled via `_FASD_FUZZY`.

##
## How to allow a single query to match any component of a path (including the last one)?

Use word mode completion, with an empty second query:

    $ f ,pat, Tab

## How to allow the last query of several to match any component of a path (except the last one)?

Append `/` to the last query.

    $ mkdir -p /tmp/.foo/bar && touch /tmp/.foo/bar/baz && fasd -A /tmp/.foo/bar/baz

    $ f foo bar
    ''~
    $ f foo bar/
    6          /tmp/.foo/bar/baz~

    $ fasd -D /tmp/.foo/bar/baz

Note that the trailing slash does *not* force you to use a full component path.
So, this would work too:

    $ f foo br/
    6          /tmp/.foo/bar/baz~

### Which limitation exists on these last two syntaxes?

When writing a query matching a path component other than the last, you can omit
characters with 2 limitations:

   1. your query can start from any position in the path component,
      but it must go on until its end

   2. after the first character of your query, you can omit characters,
      but never more than 2 consecutive ones
      (this number can be changed via `_FASD_FUZZY` in `~/.fasdrc`)

---

    $ mkdir -p /tmp/.directory \
        && touch /tmp/.directory/file && \
        fasd -A /tmp/.directory/file && \
        f ectory/ && \
        fasd -D /tmp/.directory/file
     12         /tmp/.directory/file~
    # works even though 4 characters were omitted at the start of `f ectory/` ('.', 'd', 'i', 'r')

    $ mkdir -p /tmp/.directory \
        && touch /tmp/.directory/file && \
        fasd -A /tmp/.directory/file && \
        f .direcry/ && \
        fasd -D /tmp/.directory/file
     12         /tmp/.directory/file~
    # works even though 2 characters were omitted in the middle of `f .direcry/` ('t', 'o')

    $ mkdir -p /tmp/.directory \
        && touch /tmp/.directory/file && \
        fasd -A /tmp/.directory/file && \
        f .direry/ && \
        fasd -D /tmp/.directory/file
    ''~
    # fails because more than 2 characters were omitted in the middle of `f .direry/` ('c', 't', 'o')

##
## How to make the last query match the *end* of the last component of a path?

Append `$` to the last query.

    $ touch /tmp/.foo{,bar}
    $ fasd -A /tmp/.foo{,bar}

    $ a foo
    14.1334    /tmp/.foobar~
    15         /tmp/.foo~
    $ a foo$
    15         /tmp/.foo~

    $ fasd -D /tmp/.foo{,bar}

##
# How to make fasd
## sort the frecent files/directories based *only* on
### the last time we accessed them?

Use the `-t` option:

    $ fasd -t

### the frequency with which we accessed them in the past?

Use the `-r` option:

    $ fasd -r

##
## start in interactive mode?

Use the `-i` option:

    $ fasd -i

Note that  in interactive  mode, each  entry is indexed  by a  positive integer,
explicitly printed as a prefix.
You can use this index to select an entry.

### What's the quickest way to refer to a frecent file interactively?

Use the default `sf` alias.
The latter expands to `fasd -sif` which is equivalent to:

    fasd -sif
    ⇔
    fasd -aif
    ⇔
    fasd -if

#### What about a directory?

Use the defaullt `sd` alias.

The latter expands to `fasd -sid` which is equivalent to:

    fasd -sid
    ⇔
    fasd -aid
    ⇔
    fasd -id

##
## open a frecent pdf chosen interactively?

    $ o `sf pdf`

## run a command using the best match as an argument?  (2)

Use the `-e` option:

    $ fasd -e vim pat

Or a subshell:

    $ vim `f pat`

##
# How to quickly reference
## a file or directory I have already opened/visited in the past?  (using fasd)

Use fasd's word mode completion.

Pressing `Tab`  after `,foo,bar`  will make  fasd suggest  all frecent  files or
directories matching `foo` and `bar`.

You're limited to only 2 queries, so this won't work:

    $ vim f,foo,bar,baz Tab

You can limit  the suggestions to only  the files or to only  the directories by
using the `f` or `d` prefix.

    $ vim f,foo,bar Tab

    $ cp file d,foo,bar Tab

---

There   are  also   three  zle   widgets:  `fasd-complete`,   `fasd-complete-f`,
`fasd-complete-d`, that you can bind to the keys you like:

    bindkey '^X^A' fasd-complete    # C-x C-a to do fasd-complete (files and directories)
    bindkey '^X^F' fasd-complete-f  # C-x C-f to do fasd-complete-f (only files)
    bindkey '^X^D' fasd-complete-d  # C-x C-d to do fasd-complete-d (only directories)

I prefer word mode completion to the widgets.

Compare:

    $ zathura awk pdf C-x C-f

    $ zathura ,awk,pdf Tab

The widget only suggests candidates based on the query `pdf`.
`,` can take into account several queries at the same time.
And it's easier to type.

---

Note that `C-x C-d` works only if the command-line is not empty:

    # ✔
    $ ls C-x C-d
      ^^
      there needs to be a command

If it is, `C-d` will cause the shell to quit.

    # ✘
    $ C-x C-d

## a file I have never opened in the past?  (*not* using fasd)

Move to an ancestor directory, and press `C-x C-f` (provided by fzf).
The latter will let you fuzzy search all the files below the cwd.

## a directory I have never visited in the past?  (*not* using fasd)

Move to an ancestor directory, and press `M-j` (provided by fzf).
The latter will let you fuzzy search all the directories below the cwd.

##
## What's one pitfall of fasd's word mode completion?

zsh's path completion may interfere if your query is not specific enough.

    # the issue is influenced by your cwd
    # atm, I can reproduce in `~/wiki/`, but not in `~`
    $ cd ~/wiki/
    $ o ,awk, Tab
    awk/~

    $ cd ~/wiki/
    $ o f,awk Tab
    awk/~

If that  happens, use a  prefix like `f,`  and 2 commas,  even if you  only have
*one* query:

    $ cd ~/wiki/
    $ o f,awk, Tab
    /path/to/gawk.pdf~
    ...~

---

If you're looking for a second query, and  you're trying to open a file, use its
extension (if it has one):

    $ o ,awk,pdf Tab
    /path/to/gawk.pdf~
    ...~

##
# Ranger Integration
## How to jump to a directory via fasd from ranger?

Press `3zz`.
Then, enter some part of a directory path and press Enter.

You can prefix `zz` with any number.
Without a numerical prefix, you would get file paths mixed with directory paths.

---

This requires the creation of a custom command:

    $ cat <<'EOF' >>~/.config/ranger/commands.py
    class fzf_fasd(Command):
        """
        :fzf_fasd

        Find a frecent file using fzf.

        With a prefix argument find only directories.
        """
        def execute(self):
            import subprocess
            import os.path
            command='fasd -lR' \
                    + (' -d' if self.quantifier else '') \
                    + " | fzf --no-sort --preview '{ highlight -O ansi {} || cat {} ;} 2>/dev/null'"
            fzf = self.fm.execute_command(command, universal_newlines=True, stdout=subprocess.PIPE)
            stdout, stderr = fzf.communicate()
            if fzf.returncode == 0:
                fzf_file = os.path.abspath(stdout.rstrip('\n'))
                if os.path.isdir(fzf_file):
                    self.fm.cd(fzf_file)
                else:
                    self.fm.select_file(fzf_file)
    EOF

And mapping it to a key:

    $ cat <<'EOF' >>~/.config/ranger/rc.conf
    map zz fzf_fasd
    EOF

Inspiration: <https://github.com/ranger/ranger/wiki/Custom-Commands#visit-frequently-used-directories>

## How to make ranger log all the opened files, for fasd?

    $ cat <<'EOF' >~/.config/ranger/plugins/plugin_fasd_log.py
    import ranger.api
    try: from shlex import quote
    except ImportError: from pipes import quote

    old_hook_init = ranger.api.hook_init

    def hook_init(fm):
        def fasd_add():
            fm.execute_console("shell fasd --add " + quote(fm.thisfile.path))
        fm.signal_bind('execute.before', fasd_add)
        return old_hook_init(fm)

    ranger.api.hook_init = hook_init
    EOF

Source: <https://github.com/ranger/ranger/wiki/Integration-with-other-programs#fasd>

### How is it useful?

Without this plugin, the fasd aliases `o`, `m`, `v`... would never suggest you a
file opened from ranger.

##
# How to debug fasd?

Set `_FASD_SINK` in your `~/.fasdrc` to obtain a log:

    _FASD_SINK="${HOME}/.fasd.log"

##
# Issues
## I keep opening a file but fasd never adds it to its database!

Make sure the path you used – `~` being expanded – doesn't contain more than 4 slashes.
If  necessary, switch  to a  directory which  is nearer  to the  file and  use a
relative path.

Also, make sure the name of the file does *not* contain:

   - whitespace, or any special character which requires to be escaped (e.g. `#`)
     Rename it if necessary.

   - `~`, or any environment variable
     Expand it if necessary.

Finally, don't quote your filename.

---

Alternatively, if you don't want to  remember all those pitfalls, just open your
file from ranger; the latter uses a plugin which avoids those issues:

    ~/.config/ranger/plugins/plugin_fasd_log.py

Or, add the path manually, using our custom zsh function `fasd_add()`.
The benefit of the latter over `$ fasd -A` is that you get an immediate feedback.
You know whether the path was added to fasd's database.

##
# Todo
## Why can't we redirect the output of `$ fasd -f a`?

    $ fasd -f a

This command currently outputs several lines.
If we try to redirect the output, only the last line is passed to the second command:

    $ fasd -f a | wc -l

What happens to the other ones?

