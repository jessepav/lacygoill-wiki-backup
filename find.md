# What's the general syntax of `find`?

    $ find [options] [starting-points] [expression]
                                    ^

Yes, you can search in several directories in a single command:

    $ find /etc ~/.vim -path '*tmp*' 2>/dev/null

##
# ?

Mention that `-name '*' -print` can be simplified into `-print`.

# ?

The command:

    $ find . -name afile -o -name bfile -print

will never print `afile` because this is actually equivalent to:

    $ find . -name afile -o \( -name bfile -a -print \)

Remember that the precedence of `-a` is higher than that of `-o`, and when there
is no operator specified between tests, `-a` is assumed.

# ?

Without any action, `find` assumes `-print`:

    $ cd ~/wiki; find . -name algo.md
    ./algo.md~

---

Explain this:

    $ cd ~/wiki; find . -name algo.md -o -name bc.md -print
    ./bc.md~

    $ find . -name algo.md -print -o -name bc.md
    ./algo.md~

Theory:
The “branch” in which there's an action doesn't matter.
If one branch contains an action, `find` doesn't assume anything in the others.

---

Explain this:

    $ find /etc -path '*/.*'        -o -path 'conf$'  -prune          2>/dev/null | wc -l
    26~

    $ find /etc -path '*/.*' -print -o -path 'conf$'  -prune          2>/dev/null | wc -l
    26~

    $ find /etc -path '*/.*'        -o -path 'conf$'  -prune  -print  2>/dev/null | wc -l
    0~

---

This should help you:

    $ cd ~/wiki
    $ vimdiff =(find . -path '*awk*' -o -path '*latex*') =(find . -path '*awk*' -o -path '*latex*' -print)
    $ vimdiff =(find . -path '*awk*' -o -path '*latex*') =(find . -path '*awk*' -o -path '*latex*' -prune)
    $ vimdiff =(find . -path '*awk*' -o -path '*latex*') =(find . -path '*awk*' -o -path '*latex*' -fls /tmp/log)

It seems that `-prune` is not treated  as an action, because `find` still prints
the awk files in the second command.
OTOH, `-fls`  *is* treated as  an action, because  `find` doesn't print  the awk
files in the third command.

##
# ?

The  expression  that `find`  uses  to  select files  consists  of  one or  more
primaries, each of which is a separate command line argument to `find`.

`find` evaluates the expression each time it processes a file.

An expression can contain any of the following types of primaries:

   - options affect overall operation rather than the processing of a specific
     file

   - tests return a true or false value, depending on the file's attributes

   - actions have side effects and return a true or false value

     It seems actions are a kind of tests, because:

       1. they return a true/false value
       2. `man find /NON-BUGS` says:

       > Remember that the  precedence of `-a` is higher than  that of `-o`, and
       > when there is no operator specified between tests, `-a` is assumed.
                                                     ^^^^^

       The documentation considers, implicitly, that `-print` is a test.

       So,  it  seems that  an  expression  is  solely  comprised of  tests  and
       operators.
       And  tests can  have side effects,  in which  case they're  named actions
       (special type of tests).

       Update: This section is partially wrong.
       An  expression also  contains positional  and global  options (not  to be
       confused with regular options).
       These options seem to be a kind of tests, since they all return true.
       Read `man find /EXPRESSION`.

   - operators connect the other arguments and affect when and whether they are
     evaluated

You can omit the operator between two primaries; it defaults to `-and`.

If the expression contains no actions other than `-prune`, `-print` is performed
on all files for which the entire expression is true.

Options take effect immediately, rather than  being evaluated for each file when
their place in the expression is reached.
Therefore,  for clarity,  it is  best  to place  them  at the  beginning of  the
expression.
`-daystart` is the  only excpetion; it has different effects  depending on where
in the command line it appears.
This can be confusing, so it's best to keep it at the beginning, too.

Many of the primaries take arguments,  which immediately follow them in the next
command-line argument to `find`.
Some arguments are file names, patterns, or other strings; others are numbers.
Numeric arguments can be specified as:

   * `+n`: greater than `n`
   * -`n`: less than `n`
   * `n`: exactly `n`

# ?

Why the difference:

    $ find /etc -path '*X11*' -prune -o -name '*' 2>/dev/null | wc -l
    3485~

    $ find /etc -path '*X11*' -prune -o -print 2>/dev/null | wc -l
    3484~

Why is `/etc/X11` correctly pruned in the first command (✔), but still printed (✘)?

Theory:

In the first command, there's no action; no, `-prune` is not processed as an action:

    $ cd ~/wiki
    $ vimdiff =(find . -path '*awk*' -o -path '*latex*') =(find . -path '*awk*' -o -path '*latex*' -prune)

So, `find` does this:

    $ find /etc -path '*X11*' -prune -o -name '*' 2>/dev/null | wc -l
    ⇔
    $ find /etc \( -path '*X11*' -prune -o -name '*' \) -print 2>/dev/null | wc -l

But in the second command, there *is* an action: `-print`.
So, `find` doesn't alter the command.

This would also explain the output of:

    $ find /etc \( -path '*/.*' \) -prune 2>/dev/null |vipe
    /etc/apparmor.d/cache/.features~
    /etc/cron.hourly/.placeholder~
    /etc/.pwd.lock~
    /etc/init.d/.depend.boot~
    /etc/init.d/.depend.stop~
    /etc/init.d/.depend.start~
    /etc/cron.daily/.placeholder~
    /etc/cron.d/.placeholder~
    /etc/cron.monthly/.placeholder~
    /etc/cron.weekly/.placeholder~
    /etc/.java~
    /etc/skel/.profile~
    /etc/skel/.bashrc~
    /etc/skel/.xscreensaver~
    /etc/skel/.Xdefaults~
    /etc/skel/.config~
    /etc/skel/.bash_logout~
    /etc/sensors.d/.placeholder~

Note that `.java` is a directory with a hidden subdirectory and hidden files.

Issue:

It seems to contradict `man find`:

>     If  the whole  expression contains  no actions  other than  -prune or  -print,
>     -print is performed on all files for which the whole expression is true.

# ?

Understand this:

    $ find \! -name '.?*' -o \! -prune

>     The command  line I posted  will still print out  all the matching  files, but
>     it'll skip any dotfiles.

Theory:

`-name '.?*'` matches any hidden node.
`! -name '.?*'` matches any non-hidden node.

When `find` processes a non-hidden node, `! -name '.?*'` is true,  and `find` prints it.
When `find` processes a     hidden node, `! -name '.?*'` is false, and `find` evaluates `\! -prune`.
`-prune` prunes  the node  if it's  a directory; without  the bang  `find` would
print the path of the hidden directory;  but *with* the bang, it doesn't because
the item evaluates to false.

# ?

The next comments  are extracted from an old shell  function (`fzf_fd`) which is
now useless, because fzf installs the C-t  key binding which does the same thing
(but better).

It may be interesting to convert some info into questions.

---

Alternative using `find(1)`:

    command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune" \
            + " -o " \
            + ("-type d" if self.quantifier else "") \
            + " -print 2>/dev/null | sed 1d | cut -b3-" \
            + " | fzf -e --preview '{ highlight -O ansi {} || cat {} ;} 2>/dev/null'"

Broken down:

    ┌──────────────────┬──────────────────────────────────────────────────────────┐
    │ -L               │ follow symlinks                                          │
    ├──────────────────┼──────────────────────────────────────────────────────────┤
    │ \( ... \) -prune │ don't descend into the directories matching `...`        │
    ├──────────────────┼──────────────────────────────────────────────────────────┤
    │ -o -type f       │ print file paths                                         │
    ├──────────────────┼──────────────────────────────────────────────────────────┤
    │ sed 1d           │ remove the first line matching the current directory `.` │
    ├──────────────────┼──────────────────────────────────────────────────────────┤
    │ cut -b3-         │ remove the first 2 characters on each line matching `./` │
    └──────────────────┴──────────────────────────────────────────────────────────┘
    ┌────────────────┬────────────────────────────┐
    │ -path '*/\.*'  │ hidden entry               │
    ├────────────────┼────────────────────────────┤
    │ -fstype 'dev'  │ entry on a dev filesystem  │
    ├────────────────┼────────────────────────────┤
    │ -fstype 'proc' │ entry on a proc filesystem │
    └────────────────┴────────────────────────────┘

---

What's the purpose of the `-prune`?

Ignore any file/directory which is:

   - on a dev or proc filesystem
   - hidden; directly (`~/path/to/.hidden_file`), or indirectly (`~/path/.to/hidden_file`)

---

What's the purpose of `-o` in `-o -type f`?

The previous item in the expression is `\(...\) -prune`.

If a file path doesn't match `\(...\)`, we want to print it.
But  if a  file  path doesn't  match `\(...\)`  then  `\(...\) -prune`  will
evaluate to false, because:

   1. it's equivalent to `\(...\) -a -prune`
   2. `\(...\)` is false in this case
   3. `-prune` is always true

So we need another item which will be evaluated even if the previous one was
false; hence, we need `-o`.

---

Is it equivalent to the next `fd(1)`?

No, but these two are:

    $ fd -t f -L -I . | sort
    $ find -L . -path '*/\.*' -prune -o -type f -print | cut -b3- | sort

You can check it like so:

    $ cd /etc
    $ vimdiff =(find -L . -path '*/\.*' -prune -o -type f -print | cut -b3- | sort) =(fd -t f -L -I . | sort)

# ?

Document that using `.config/fd/ignore` should be preferred to `-E` whenever possible.

Why?
If you  want to be sure  that any command  relying on `fd(1)` ignores  a certain
pattern, it's going to be tedious/error-prone to edit each of them.
`.config/fd/ignore` is easier, more reliable, and  scale better to any number of
commands you'll add in the future.

##
# How to make `locate` print the names of all files whose name ends with ‘Makefile’ or ‘makefile’?

    $ locate '*[Mm]akefile'

# How to grep ‘pat’ in all the files whose paths are stored in the file `listing`?

    $ xargs grep pat <listing

`xargs(1)` reads its standard  input, and pass it as an  argument to the command
which follows.
Here, the  operator `<` redirects xarg's  stdin to `listing`, and  so `xargs(1)`
runs `grep(1)` by passing it all the file paths stored in the file.

It's as if you had run:

    $ grep pat file1 file2 ...
               ├─────────────┘
               └ paths stored in `listing`

##
# How to find files in `/etc` whose path matches `apt/source`?

Use `-path`:

    $ find /etc -path '*apt/source*' 2>/dev/null

## Why can't I use `-name`?

Because `-name` makes a  comparison between the *base* of a  file name (the path
with the leading directories removed) and the pattern.

##
# When `find` compares a file path with a pattern, what kind of path does it use: absolute, relative, ...?

The path  starts with the starting-point  specified on the command-line,  and is
not converted to an absolute path.

# What's the output of `cd /; find tmp -path /tmp 2>/dev/null`?

Nothing.

## Why?

Here, the  starting-point is `tmp`, so  when the directory `/tmp`  is processed,
`find` makes its path starts with `tmp` (instead of `/tmp`).
But  the  path `tmp`  can't  match  the pattern  `/tmp`,  so  `find` can't  find
anything.

##
# Todo

Read this: <http://mywiki.wooledge.org/UsingFind>

