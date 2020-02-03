# Installation

Go to <https://www.gnu.org/software/sed/>  to find a url to  download the latest
stable source release.
Atm, you can use this url: <https://ftp.gnu.org/gnu/sed/>

Download the archive and its signature, and check it:

    $ gpg --keyserver x-hkp://pool.sks-keyservers.net --recv-keys 000BEEEE
    $ gpg --verify sed-4.7.tar.xz.sig sed-4.7.tar.xz

Finally, configure, compile and install:

    $ ./configure --prefix=/usr --without-included-regex
    $ make
    $ make check
    $ sudo make install

Without `--prefix`, the binary will be in `/usr/local/bin/sed`.
This may break your scripts, if their shebang refers to `/usr/bin/sed` instead.

Without `--without-included-regex`, sed doesn't support equivalence classes:

    $ /usr/bin/sed 's/[[=e=]]/X/g' <<<'a é b e c è'
    a é b X c è~

---

If you want the very latest version:

    $ git clone git://git.sv.gnu.org/sed
    $ ./bootstrap

    # To use the  most-recent gnulib (as opposed to the  gnulib version that the
    # package last synchronized to):
    $ git submodule foreach git pull origin master
    $ git commit -m 'build: update gnulib submodule to latest' gnulib

    $ ./configure --quiet --enable-gcc-warnings
    $ make
    $ make check

    # At this point, there should be  no difference between your local copy, and
    # the GIT master copy; this command should output no difference.
    $ git diff

However, at the moment, this procedure fails at the `make` step.
Not because of a dependency issue, but because of an error in the source code.

##
# Command-line
## In sed, how is the first positional argument interpreted without the `-e`/`-f` options?

As the script *code* to execute on the input:

    $ sed [options] <pgm text> <input file> ...

---

Note that the synopsis of awk and grep look the same:

    $ awk [options] <pgm text> <input file> ...
    $ grep [options] <pattern> <input file> ...

This choice of  order between the program/pattern  and the input data  is due to
the fact that  the latter is unpredictable;  you can't know in  advance what the
user will operate on (one file, two files, ...).
If  the  input  came before  the  program/pattern,  there  would  be no  way  to
distinguish  the  latter from  the  input,  unless you  define  it  as the  last
argument, which seems to be awkward.

### And with `-e` or `-f`?

As an input file:

    $ sed [options] -e <pgm file> <input file>
    $ sed [options] -f <pgm file> <input file>
                    ├───────────┘ ├──────────┘
                    │             └ positional argument
                    └ optional argument

###
## What does `-n` suppress?

The auto-print  of the pattern  space when reaching the  end of the  script, and
before replacing it with the next input line (`n` command).

## What can't `-n` suppress?

The printing of the text added by an `a`, `i`, `c`, `r`, `p` command.

##
## When do I need the `-e` option?

Only when you supply more than one statement on the command-line.
It tells sed to interpret the next argument as a statement:

    $ sed -e 'statement1' -e 'statement2' input_file

When there is  a single statement, sed  is able to make  that determination on
its own:

    $ sed -e 'statement' input_file
    ⇔
    $ sed    'statement' input_file

## How to specify multiple statements on the command-line?  (3)

Separate the statements with a semicolon:

    $ sed 's/pat1/rep1/; s/pat2/rep2/' input_file
                       ^

Or precede each statement by `-e`:

    $ sed -e 's/pat1/rep1/' -e 's/pat2/rep2/' input_file
          ^^                ^^

Or insert a literal newline in an unclosed string:

    $ sed 's/pat1/rep1/
           s/pat2/rep2/' input_file

## How to combine several scripts (`-f`) and/or statements (`-e`)?

Simply use as many `-f` and/or `-e` options as needed.
Their concatenation will be the resulting script.

##
## Which option is implied by `-i`?

`-s`.

`-s`  means that  when you  ask  sed to  edit files  in-place, it  automatically
considers them as separate.

---

`-n` is *not* implied by `-i`.
`-n` suppresses the auto-print of sed.
With  `-i`, there  is *still*  an  output; but  it's not  visible, because  it's
redirected to a file.

## How to make sed create a backup of a file before editing it in-place?

Provide a file extension to `-i`:

    $ sed -i.bak 's/pat/rep/' file

This will create `file.bak` which will contain the original contents of `file`.

---

For this reason, you can't combine `-i` with another single-letter option right after.
For example, you can't combine `-i` and `-e` like this: `-ie`.
`e` would be interpreted as a backup extension.

### How to make a backup in another directory?

Instead of providing an extension to `-i`, you can provide a path.
Inside, you must use the special character `*` as a placeholder to represent the
input file exactly as provided on the command-line.

    $ cat <<'EOF' >/tmp/file
    a
    b
    c
    EOF

    $ cd /tmp; mkdir dir 2>/dev/null; \
      sed -i'dir/*.bak' 's/b/X/' file
                 ^
                 placeholder which will be expanded into `file`

    $ cat /tmp/file
    a~
    X~
    c~

    $ cat /tmp/dir/file.bak
    a~
    b~
    c~

---

`*` can  also be used to  create a backup in  the current directory, but  with a
given prefix instead of a given extension:

    $ cd /tmp; sed -i'bak_*' 's/b/X/' file

    $ cat /tmp/bak_file
    a~
    b~
    c~

#### Which pitfalls should I avoid?

Remember that `*` is expanded into whatever input file you passed to sed, *as you wrote it*.

So, this wouldn't work:

    $ cd /tmp; mkdir dir 2>/dev/null; \
      sed -i'dir/*.bak' 's/bar/XXX/' /tmp/file
    sed: cannot rename /tmp/file: No such file or directory~

Here, `*`  is expanded  into `/tmp/file`, and  sed tries to  create a  backup in
`dir/tmp/file.bak`, but `dir/tmp/` doesn't exist.

---

If you  want to use the  `=` sign between `-i`  and its value, you  must use the
long form of the option, `--in-place`.

    $ cd /tmp; mkdir dir 2>/dev/null; \
      sed --in-place='dir/*.bak' 's/bar/XXX/' file
          ^^^^^^^^^^^

##
## Which commands can *not* be terminated by a semicolon?

`r`, `w`, `a`, `i`, `c`.

Also, the `w` flag of the `s` command.

---

    $ sed -n 's/pat/rep/w /tmp/file; p' <<<'pat'

The  previous command  will save  the  output of  the substitution  in the  file
`/tmp/file; p`.
While you may have expected it to be saved in `/tmp/file`, then `p` to print the
pattern space.

---

    $ seq 3 | sed '2i hello; 3s/./X/'
    1~
    hello; 3s/./X/~
    2~
    3~

The previous command will insert the line `hello; 3s/./X/`.
While  you may  have expected  `hello` to  be inserted,  then `s`  to perform  a
substitution on the third line.

### How to terminate them on the shell's command-line?  (2)

Use several `-e` expressions:

    $ seq 3 | sed -e '2 {w /tmp/file' -e 's/.*/[&]/}'
    1~
    [2]~
    3~

    $ cat /tmp/file
    2~

Or insert a literal newline:

    $ seq 3 | sed '2 {w /tmp/file
    s/.*/[&]/}'

The last command works only if you quote the expression, which you always should
anyway.
Otherwise,  when  you  press  Enter  to insert  the  newline,  the  shell  would
immediately run the command without letting you finish writing it.

##
# Regex
## How to enable the ERE syntax?

Use the `-E` option (same thing for grep).

## In which syntax (BRE vs ERE) can I write `\<` and `\>`?

Both.

`\<` and `\>` are not influenced by the syntax of the regex.
They're always  interpreted the same  way, as anchors,  and they must  always be
backslashed.

## What are the differences between BRE and the magic mode in Vim?

In sed, the equivalent of the Vim's quantifier `\{n,m}` needs two backslashes:

    \{n,m\}
         ^

But in practice, Vim understands `\{n,m\}` too.

---

In Vim (like in  awk) you can include a closing square  bracket inside a bracket
expression *anywhere* by escaping it with a backslash:

    [a\]1]

This regex will match `a` or `]` or `1`.

But it won't work in sed, nor in grep.

##
## How to include an opening bracket in a bracket expression?

Just write it.

There's no need to backslash it or  put it in a special position, because inside
a bracket expression, all characters lose their special meaning; except:

   - `-` (range)
   - `\` (some escape sequence like \t and \n)
   - `]` (end of bracket expression)
   - `^` (complement)

### How about a closing bracket?

Make sure the closing bracket is at the start of the expression, and unescaped:

    []ab]
     ^

This regex will match `]` or `a` or `b`.

---

If you write the complement of a bracket expression, put it in second position:

    $ sed '[^]ab]' file
             ^

This regex will match any character which is *not* `]` or `a` or `b`.

---

Note that all of this also applies to grep, gawk and Vim.

###
## How are the metacharacters `^` and `$` interpreted in the middle of a pattern?

Literally:

    $ sed 's/ ^ /X/' <<<'a ^ b'
    aXb~

From this point of view, sed is similar to Vim (but different from awk).

OTOH, awk *can* compare a regex to multi-line record...

##
# Addressing
## Without any address, which line(s) is/are affected by a sed command, like `s`?

*Every* line in the input.

Because of  its stream orientation,  sed goes through its  input, one line  at a
time, such that each  line becomes a temporary current line,  and the command is
applied to it.

IOW, sed commands are implicitly global.

    # sed command
    s/pat/rep/

    ⇔

    # Vim command
    :%/pat/rep/

---

In contrast,  a Vim  Ex command, like  `:s`, applies to  the current  line; i.e.
wherever the cursor is currently.

## What's the main difference between sed commands and Vim Ex commands with the same name (`s`, `d`, ...)?

In Vim, by default, most Ex commands apply only to the current line.
In sed, by default, commands apply to *all* input lines.

In Vim, you use  addressing to *expand* the number of lines  that are the object
of a command.
In sed,  you use  addressing to  *restrict* the  number of  lines affected  by a
command.

A sed address/range is used as a test:  each time an input line is copied in the
pattern space, sed compares its address with the address/range of the command to
decide whether it sould be run.

###
## How to apply the same range to a set of commands?

Group them inside curly braces:

                            v              v
    $ seq 11 13 | sed '/2$/ {s/1/3/; s/2/4/}'
    11~
    34~
    13~

## How to reverse the meaning of an address/range?

Suffix it with a bang:

    $ printf '%s\n' 1 a b 2 | sed -n '/a/,/b/p'
    a~
    b~
                                             v
    $ printf '%s\n' 1 a b 2 | sed -n '/a/,/b/!p'
    1~
    2~

##
## How to combine ranges? i.e. How to operate on lines matching two specified ranges simultaneously?

Write the command prefixed by the inner range inside curly braces.
Outside the braces, write the outer range.

In the following example, we use this syntax to remove *some* empty lines:

    $ cat <<'EOF' >/tmp/file
    Here, there can be

    empty lines.

    There should be

    no empty lines

    in this block.

    Here, there can also be

    empty lines.
    EOF

    $ sed '/^There/,/^in/ {/^$/d}' /tmp/file
    Here, there can be~
    ~
    empty lines.~
    ~
    There should be~
    no empty lines~
    in this block.~
    ~
    Here, there can also be~
    ~
    empty lines.~

Note that you could write several commands inside the curly braces.
Each of them would be executed on  the condition that the address of the current
line matches its range *and* the range before the curly braces.

### How to combine an arbitrary amount of ranges?

Nest as many curly braces blocks as needed.

                        v       v
    $ printf '%s\n' a b c b a b c b | sed -n '/a/,/a/ { /b/,/b/ { /c/ p } }'
    c~

In this example, we ask sed to print  the lines containing a `c`, inside a range
of lines whose first and last contain a `b`, inside a range of lines whose first
and last contain an `a`.

Only the first `c` is printed.
The second one satisfies only 2 conditions out of 3:

   - it contains a `c`
   - it's inside a range of lines whose first and last contain a `b`
   - it's *not* inside a range of lines whose first and last contain an `a`

##
## How does sed compare the current input line address with a range?

Here's  a probably  simplified  description  of the  algorithm  used  by sed  to
determine whether the current input line matches a range:

   - start from input line 1

   - check whether the line matches the start of the range

   - if it does, go to next line and compare it to the end of the range
     if not, go to next line and compare it to the start of the range

   - continue until the current input line; each time there's a match,
     reverse the comparison (start of range ↔ end of range)

Upon reaching the current input line, if  sed is now comparing the line with the
start of  the range,  and it doesn't  match, it's considered  to be  outside the
range; in *all* other cases, it's considered to be inside:

   - if it's comparing the line with the start of the range and it matches, the
     line is considered to be the first line in a new range

   - if it's comparing the line with the end of the range and it matches, the
     line is considered to be the last line in the current range

   - if it's comparing the line with the end of the range and it does *not*
     match, the line is considered to be in the middle of the current range

##
### What's the output of the next command?

    $ printf '%s\n' a b a b a | sed -n '/a/,/a/ { /b/p }'
↣
    b~
↢

#### Explain what happened.

The code asks sed to print a `b` inside a range delimited by `a`.
At first glance, there seems to be two matches.

    a b a b a
      ^   ^

But the output contains only the first `b` not the second one.
This is  because the range  starting from  the first `a`  has been ended  by the
second `a`.
So, the second `b` is outside any range of `a`.

      ┌ inside a range of `a`
      │   ┌ outside a range of `a`
      │   │
    a b a b a
    │   │   │
    │   │   └ starts another range (but it's too late for the previous `b`)
    │   └ ends the range
    └ starts a range

###
### What happens if the second address of a range is a regex, and it doesn't match any input line?

If the first address  matches a line, sed will operate on  all the lines between
this line and the last one.

    $ printf '%s\n' foo bar baz | sed -n '1,/not_found/p'
    foo~
    bar~
    baz~

This differs from Vim, where the same command would bail out:

    :new
    :call setline(1, ['foo', 'bar', 'baz'])
    :1,/not_found/p
    E486: Pattern not found: not_found~

Explanation:

Contrary to Vim which can see a file  in its entirety, sed has no way of looking
ahead to determine if the second match  will be made, because it always iterates
over  the  input  lines  first  (even  if you  pass  it  an  input  file):  it's
**stream-oriented**.

As soon  as an input  line matches  the first address,  `p` is applied  to *any*
line, until another line matches the second address (if any).

#### and the command is inside a group (`{}`) which is prefixed by another range?

This time, the command does *not* operate on  all the lines until the end of the
input.
Instead, it operates  on all the lines until  the last line in the  range of the
current block:

    $ printf '%s\n' a b a c | sed -n '/a/,/a/ { /b/,/x/ p }'
    b~
    a~

Here, even though the regex `x` fails to match a line, `p` doesn't print all the
lines until the end of the input – if it did, it would also print `c`.
It stops at the  second line `a` because that's the end of  the range applied to
the current block.

##
### When an input line matches the start *and* end of a range, how is it used?

As the start of the range, but not its end.

sed does *not* re-use the same line to match both ends of the range.

    $ printf '%s\n' a b a | sed -n '/b/,/b/ p'
    b~
    a~

Here, the second  input line `b` matches  the start of the  range `/b/,/b/`, but
sed doesn't re-use it to match the end of the range.
If it did, it wouldn't output `a`.
It looks for another `b` line.
Since there's none, `p` outputs all the remaining lines, that is `b` and `a`.

####
# Printing
## What does the `p` command do exactly?

It prints the contents of the pattern space as the latter is when it's invoked.

Nothing more.
In particular, it doesn't clear the pattern space nor does it change the flow of
control in the script.

### In practice, how can this be really useful?

When debugging a script.

It allows you to  inspect the state of the pattern space  right before running a
command.

It's the equivalent of `:echom` in a Vimscript.

##
## How to print the 2nd line of a file?

    $ printf '%s\n' a b c | sed -n '2p'
    b~

The `p` command allows you to print arbitrary lines from sed's input.

### What's the output of the next command?

    $ printf '%s\n' a b c | sed '2p'
↣
    a~
    b~
    b~
    c~
↢

#### Why the difference with the previous command?

By default  (i.e. without `-n`), sed  prints the pattern  space at the end  of a
cycle (except if it has been deleted by commands such as `d`).
To prevent this, you need `-n`.

###
## How to print the last line of a file?

Use the special symbol `$`:

                                    v
    $ printf '%s\n' a b c | sed -n '$p'
    c~

### its first and last line?

    $ printf '%s\n' a b c | sed -n '1p ; $p'

##
## How to print the first and last line of each file in a set of files?

Use the `-s` option:

    $ sed -n -s '1p; $p' <(printf '%s\n' a b c) <(printf '%s\n' d e f)
    a~
    c~
    d~
    f~

### What's the output of the next command?

    $ sed -n '1p; $p' <(printf '%s\n' a b c) <(printf '%s\n' d e f)
↣
    a~
    f~
↢

#### Why the difference with the previous command?

sed treats multiple input files as one long stream.
To force it to consider each file as a *s*eparate stream, you need `-s`.

###
## How to print only the lines where a substitution was made?

Use sed's `-n` option and the `p` flag of the `s` command:

                                vv        v
    $ printf '%s\n' a b c | sed -n 's/a/X/p'
    X~

##
## How to print the pattern space replacing non-printable characters with C-style escaped form?

Use the `l` command.

    $ printf '\e' | sed -n 'l' <<<'\e'
    \033$~

### What's the default line-wrap length?

70

    $ sed -n 'l' <<<$'this is a very very very very very very long line with an \e character'
    this is a very very very very very very long line with an \033 charac\~
    ter$~

### How to wrap the output line after 10 characters?  (2)

Pass the numerical argument `10` to `l`:

    $ sed -n 'l 10' <<<$'this is an \e character'
    this is a\~
    n \033 ch\~
    aracter$~

Or use the `-l` shell option:

    $ sed -l10 -n 'l' <<<$'this is an \e character'
    this is a\~
    n \033 ch\~
    aracter$~

### How to prevent the output line from being wrapped?

Pass the value `0` to the `l` command or to the `-l` option:

    $ sed -n 'l0' <<<$'this is a very very very very very very long line with an \e character'
    $ sed -l0 -n 'l' <<<$'this is a very very very very very very long line with an \e character'
    this is a very very very very very very long line with an \033 character$~

##
## How to print the current input line ADDRESS (with a trailing newline)?

Use the `=` command:

    $ printf '%s\n' aaa bbb ccc | sed =
    1~
    aaa~
    2~
    bbb~
    3~
    ccc~

`=` supports a range too:

    $ printf '%s\n' aaa bbb ccc | sed 1,2=
    1~
    aaa~
    2~
    bbb~
    ccc~

### What happens if this command is run while the pattern space contains multiple lines?

`=` prints the address of the *last* line:

    $ printf '%s\n' a b c d | sed -n 'N; ='
    2~
    4~

    $ printf '%s\n' a b c d | sed -n 'N; N; ='
    3~

##
# Substitution
## What are the five special sequences of characters in the replacement field?

    ┌──────────┬─────────────────────────────────────────────────────────────────────────┐
    │ \1 .. \9 │ references to the portion of the match contained between the n-th \( \) │
    ├──────────┼─────────────────────────────────────────────────────────────────────────┤
    │ &        │ reference to the whole match                                            │
    ├──────────┼─────────────────────────────────────────────────────────────────────────┤
    │ \l       │ turn the next character to lowercase                                    │
    │ \u       │                            uppercase                                    │
    ├──────────┼─────────────────────────────────────────────────────────────────────────┤
    │ \L       │ turn the next characterS to lowercase until a \U or \E                  │
    │ \U       │                             uppercase until a \L or \E                  │
    ├──────────┼─────────────────────────────────────────────────────────────────────────┤
    │ \E       │ stop case conversion started by \L or \U                                │
    └──────────┴─────────────────────────────────────────────────────────────────────────┘

##
## After every successful substitution, how to
### print the pattern space?

Use the `p` flag:

    $ printf '%s\n' a 1 b 2 | sed -n 's/[0-9]/[&]/p'
    [1]~
    [2]~

### write the pattern space?

Use the `w` flag and the path to a file:

                                                  vvvvvvvvvvv
    $ printf '%s\n' 1 a 2 b | sed -n 's/[0-9]/[&]/w /tmp/file'

    $ cat file
    [1]~
    [2]~

`s` has  replaced `1` with  `[1]` and written the  result into `file`,  then has
replaced `2` with `[2]` and *appended* the result into `file`.

##
## How to limit a substitution to
### the `n`th occurrence of the pattern?

Write the index of the occurrence in the flag field of the substitution command:

                 v
    $ sed 's/a/X/2' <<<'a a a'
    a X a~

### all the occurrences beyond the `n`th occurrence of the pattern?

In the flag field, combine the index `n` with the `g` flag:

                 vv
    $ sed 's/a/X/2g' <<<'a a a'
    a X X~

##
## When can a substitution command be broken on multiple lines?

When its replacement field contains a newline.

### How?

By  prefixing the  newline  with a  backslash to  suppress  its special  meaning
(command termination).

    $ sed 's/pat/b\
    c/' <<<'a pat d'
    a b~
    c d~

##
# Appending and inserting
## How to insert a line of text before an input line?

Use the `i` command:

                     ignored, but improves the readability
                     v
    $ seq 3 | sed '2i inserted before 2'
    1~
    inserted before 2~
    2~
    3~

All the whitespace between  the command and the line of text  is ignored, so the
space  between  `i`  and `inserted  before  2`  is  just  there to  improve  the
readability of the code.

## How to append a line of text after an input line?

Use the `a` command:

    $ seq 3 | sed '2a appended after 2'
    1~
    2~
    appended after 2~
    3~

##
## When is the text added by `a` or `i` printed exactly?

At the very end of the current cycle:

    $ printf '%s\n' aa bb cc | sed -n -e '2a appended' -e '='
    1~
    2~
    appended~
    3~

Notice that  the address 2  is printed *before*  `appended`, because `=`  is run
before the end of the cycle.

### When is it added if
#### `a` or `i` is followed by `n`?

The added text is printed immediately, along the current pattern space.

    $ printf '%s\n' aa bb cc | sed -e '1a appended' -e 'n;='
    aa~
    appended~
    2~
    bb~
    cc~

Notice that `appended` is printed *before* the line address of the next line (2).
It's printed right  after `aa`; both are printed because  `n` causes a premature
end of cycle.
The relative position between `aa` and `appended` has nothing to do with how `n`
auto-prints the pattern space; it has to do with the chosen command, `a`.
Had you chosen `i` instead, `appended` would have preceded `aa`.

Note that the address of the third  line is not printed, because just before `=`
is processed,  `n` fails to read  a next input  line (there's none), and  so sed
exits immediately.

#### `a` or `i` is followed by `c` or `d`?

The added text is still printed:

    $ sed -e '1a appended' -e 'c changed' <<<'x'
    changed~
    appended~

    $ sed -e '1i inserted' -e 'd' <<<'x'
    inserted~

This further indicates that the added text is not part of the pattern space.

###
### Is it printed if sed was invoked with `-n`?

Yes.

`a` and `i` explicitly asks sed to output the result of their operation.
In this regard, they are similar to `p` which also ignores `-n`.

    $ seq 3 | sed -ne '2a hello'
    hello~

##
## What's the output of the next command?

    $ printf '%s\n' aa bb | sed -e '2a appended' -e 'n'
↣
    aa~
    bb~
↢

### Why hasn't `appended` been added?

`n` reads `bb` prematurely.
When `bb` is in the pattern space, `2a` has already been processed.

---

`aa` is copied in the pattern space.
`2a` is *not* run because 2 doesn't match the line address of `aa` (1).
`n` is run which auto-prints `aa` and copies `bb` in the pattern space.
The end of the cycle is reached, which auto-prints `bb`.

There's no input line anymore, so there's no other cycle.

---

This shows that `n` desynchronizes the execution from the start of the code.
Normally, when sed reaches the end of a cycle and start a new one, the execution
jumps back to the  start of the code; but not when `n`  is executed: instead, it
stays where it currently is.

###
## How to add *multiple* lines of text before/after an input line?  (2)

Use `\n` to separate the lines of text, or  use a backslash at the end of a line
to suppress the special meaning of the newline (i.e. command termination).

    $ seq 3 | sed '2i\
    hello\
    world'

    $ seq 3 | sed '2i hello\nworld'
    1~
    hello~
    world~
    2~
    3~

Note that the first syntax is the original one.
In old  sed versions, you *had*  to write a  backslash and continue on  the next
line after the `a`,  `i`, and `c` commands, and do the same  after every line of
text except the last one.

Prefer the first syntax, because:

   - the second one is considered an error by Vim's sed syntax plugin

   - it's more readable:
     you clearly see where a line ends, and you're not wondering whether `\n` is translated

## What happens if I prefix the `a` or `i` commands with a range?

They will repeat their operation on every line in the range.

    $ seq 5 | sed '3,4i hello\nworld'
    1~
    2~
    hello~
    world~
    3~
    hello~
    world~
    4~
    5~

Here, `a` appends the lines `hello` and `world` after the lines 2 and 3.

##
## How to add a line beginning with some whitespace, without the latter being removed?

Prefix the whitespace with a backslash.

                     ┌ will be ignored
                     │ ┌ won't be ignored
                     │ ├──┐
    $ seq 3 | sed '2a \    hello'
    1~
    2~
        hello~
    3~

###
## What's the only way to terminate an `a`, `i` or `c` command?

Write a literal newline (!= `\n`).

### Is there another way on the shell command-line?

Yes, use several `-e` options:

    $ seq 3 | sed -e '2i hello' -e 'w /tmp/file'
    1~
    hello~
    2~
    3~

sed will concatenate the statements by adding newlines.

---

This trick  can also be used  to separate the `a`,  `i` or `c` command  from the
first line of text, when using their  original syntax (the one where the command
is immediately followed by a backslash):

    $ seq 3 | sed -e '2i\' -e hello
    1~
    hello~
    2~
    3~

This works because  sed will concatenate the statements by  adding newlines, and
because the backslash  at the end of a statement  suppresses the special meaning
of the newline (command termination).

###
## What's the output of the next `a` command?

    $ seq 3 | sed -e '2a hello' -e '3s/./X/'
↣
    1~
    2~
    hello~
    X~
↢

### Why wasn't the substitution applied on the third line of the output?

Because the line  appended by `a` is not  part of the input (nor  of the pattern
space); it will  simply be output at the  end of the current cycle,  or when the
next input line is read – with `n` – regardless of the presence of `-n`.
While `s` operates on the third *input* line.

---

The same thing would happen if instead of adding text to the output, we removed text:

    $ seq 3 | sed -e '2d; 3s/./X/'
    1~
    X~

Here, even though `d` removes a line,  which leaves us with only 2 output lines,
`s` still  performs its substitution  on the third  input line; it  doesn't care
about the output.

---

More generally, I  think sed commands may  modify the output but  can't have any
effect on the input.

Rationale: It makes the code simpler.
If you had to take into consideration the  change of address of a line caused by
a previous command, it would make thinking about the code more difficult.

###
# Change, Deletion
## How to change the contents of an input line?

Use the `c` command:

    $ seq 3 | sed '2c changed line 2'
    1~
    changed line 2~
    3~

## Is the changed text still printed if sed was invoked with `-n`?

Yes, for the same reason as `a` and `i`.

    $ sed -n -e 'c changed' <<<'x'
    changed~

##
## Which commands following a `d` command are processed?

None.

`d` starts the next cycle immediately.
IOW, the rest of the commands of the script are ignored.

    $ printf '%s\n' a b | sed '1d; ='
    2~
    b~

Here, `=` was not run against the  first line `a`, otherwise 1 would be included
in the output.

Indeed, since  the next  commands (if any)  can only be  applied to  the pattern
space, and since `d` deletes the pattern space, there's nothing left to process.

### What about `c`?

None.

For the same reason as `d` (`c` also deletes the pattern space).

    $ printf '%s\n' a b c | sed -n -e '2c changed' -e '='
    1~
    changed~
    3~

Notice that `=` was not run on the second line; otherwise 2 would be in the output.

---

    $ seq 3 | sed -e '2c hello' -e 'w /tmp/file'
    $ cat /tmp/file
    1~
    3~

##
## What happens if I prefix a `c` command with a range?

`c` can operate on a range of lines, like `a` and `i`.
But, it interprets the range differently.
It doesn't repeat its operation on every line in the range.
Instead, it  operates just once, after  removing (cutting) all the  lines in the
range.

    $ seq 4 | sed '2,3c hello\nworld'
    1~
    hello~
    world~
    4~

## What's the output of the next `c` command?

    $ seq 4 | sed -e '2,3 { c hello' -e '}'
↣
    1~
    hello~
    hello~
    4~
↢

### Why did `c` repeat its operation several times?

Probably because the range is processed by the block, not by `c`.
And a block repeats its commands for each line in its range.
So, in this case, the particular treatment of a `c` range doesn't apply.

####
# Transliteration
## How to uppercase a line?

Use the transliteration command `y` which  applies an arbitrary mapping from one
set of characters to another one:

    y/source-chars/dest-chars/

Example:

    $ sed 'y/abcdefghijklmnopqrstuvwxyz/ABCDEFGHIJKLMNOPQRSTUVWXYZ/' <<<'hello world'
    HELLO WORLD~

---

Note that `source-chars`  and `dest-chars` can contain escape  sequences such as
`\n` or `\t`.

    $ sed 'y/abcdefghijklmnopqrstuvwxyz\t/ABCDEFGHIJKLMNOPQRSTUVWXYZ\n/' <<<'hello	world'
    HELLO~
    WORLD~

##
# Reading, Writing
## How to import the contents of a file into the output of a sed command?

Use the `r` command, whose syntax is:

    r filename

It queues  the contents of  `filename` to be read  and appended into  the output
stream.

Example:

    $ seq 4 | sed '2r/etc/hostname'
    1~
    2~
    ubuntu~
    3~
    4~

### How to import it after every line in a range?

Prefix `r` with the appropriate range.
The file will then be re-read and appended after each of the addressed lines.

    $ seq 5 | sed '2,3r /etc/hostname'
    1~
    2~
    ubuntu~
    3~
    ubuntu~
    4~
    5~

##
## When is run
### a read command?

At the end of the current cycle:

    $ sed -n -e 'r /etc/hostname' -e '=' <<<'x'
    1~
    ubuntu~

Or when the next input line is read with `n`:

    $ sed -n -e 'r /etc/hostname' -e 'n; =' <<<$'a\nb'
    ubuntu~
    2~

### a write command?

Immediately :

    $ sed -e 'w /tmp/file' -e 's/./Y/' <<<'x'
    Y~

    $ cat /tmp/file
    x~

##
## How to read the standard input, when the sed command has been passed a filename as argument?

Use the special value `/dev/stdin`:

    $ seq 3 | sed 'r /dev/stdin' /etc/hostname
    ubuntu~
    1~
    2~
    3~

Here's another  example, where the  stdin is  not connected to  a pipe but  to a
regular file thanks to the `<` operator:

                                       v
    $ sed 'r /dev/stdin' /etc/hostname </etc/environment
    ubuntu~
    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"~

##
## How to extract all the lines containing the word `BUG` inside `/tmp/bugs`?

Use the `w` command to write any line matching `BUG`:

    $ cat <<'EOF' >/tmp/file
    1. this line is ok
    2. this line has a BUG
    3. this line is also ok
    4. this line has also a BUG
    EOF

    $ sed -n -e '/BUG/w /tmp/bugs' /tmp/file

    $ cat /tmp/bugs
    2. this line has a BUG~
    4. this line has also a BUG~

### How to only extract a certain field?

Use a substitution command before `w` to remove all the noise.

    $ cat <<'EOF' >/tmp/file
    Adams,     Henrietta  Northeast
    Banks,     Freda      South
    Dennis,    Jim        Midwest
    Garvey,    Bill       Northeast
    Jeffries,  Jane       West
    Madison,   Sylvia     Midwest
    Sommes,    Tom        South
    EOF

    $ sed -n -e '/\s*Northeast$/ {s///; w /tmp/.region.northeast' -e '}' \
             -e '/\s*South$/ {s///; w /tmp/.region.south' -e '}' \
             -e '/\s*Midwest$/ {s///; w /tmp/.region.midwest' -e '}' \
             -e '/\s*West$/ {s///; w /tmp/.region.west' -e '}' \
          /tmp/file

    $ cat /tmp/.region.northeast
    Adams,     Henrietta~
    Garvey,    Bill~
    $ cat /tmp/.region.south
    Banks,     Freda~
    Sommes,    Tom~
    $ cat /tmp/.region.midwest
    Dennis,    Jim~
    Madison,   Sylvia~
    $ cat /tmp/.region.west
    Jeffries,  Jane~

##
## How to write a file on the standard error?

Use the special value of filename `/dev/stderr`.

    $ seq 3 | sed -n 'w /dev/stderr' >/tmp/out 2>/tmp/err

    $ cat /tmp/out
    ''~

    $ cat /tmp/err
    1~
    2~
    3~

### On the standard output?

Use the special value of filename `/dev/stdout`.

    $ seq 3 | sed -n 'w /dev/stdout' >/tmp/out
    $ cat /tmp/out
    1~
    2~
    3~

#### `p` is equivalent to writing on the standard output. So, how is the previous answer useful?

When you use `-i`, `p` doesn't write on stdout, but on the file:

    # this will double the lines in `file`
    $ sed -i 'p' file

In this case, if you still want to write on stdout, you need `w /dev/stdout`.

##
## I use the same file to write the pattern space with several `w` (command or flag of `s`).
### What will it contain in the end?

Initially, the file is truncated, so whatever text it contained originally is lost.
After that, all the written texts will be appended to the file.

    $ seq 3 | sed -n -e 'w /tmp/file' -e 's/./X/w /tmp/file'
    $ cat /tmp/file
    1~
    X~
    2~
    X~
    3~
    X~

##
# Changing the Normal Flow of Control
## What does the `n` command do exactly?

It makes sed act as if it had reached the end of the cycle, now.
However, it doesn't change where the  execution is currently; the latter doesn't
restart from the start of the code.

`n` causes sed to  auto-print the pattern space, and to print  the text added by
the commands `a`, `i`, `c`, and `r`  now, because that's what happens at the end
of a cycle.

---

*Let's call the current line A, and the next two lines B and C.*

`n` prints the pattern space A – unless sed was invoked with `-n` – and replaces
its contents with the next input line B.

The next  cycle will take this  replacement into account; it  won't re-process B
twice; it will just naturally move on to C.

In effect,  the commands after `n`  won't be applied  to A, and the  ones before
won't be applied to B.

## What happens if there's no input line anymore when `n` or `N` is run?

`n` causes the pattern space to be auto-printed.
After that, for  both `n` and `N`, sed exits  immediately without processing the
rest of the commands.

---

Proof:

    $ printf '%s\n' a b c | sed -n 'N;p'
    a~
    b~

If sed didn't exit, `p` would be processed when `c` is in the pattern space, and
the output would contain it:

    a~
    b~
    c~

## How to remove the next line after any line matching `foo`?

Use the `n` command and `d` commands:

    $ printf '%s\n' foo xxx bar baz | sed '/foo/ {n; d}'
    foo~
    bar~
    baz~

##
# Misc
## Why does sed iterate over the input lines before iterating over the script statements?

There may be other reasons, but if it  did the reverse, when used in a pipeline,
the sed command would block all the following commands.
Indeed,  sed would  have to  wait for  the previous  command to  send *all*  its
output, before being able to process the second statement of the script.

## When does sed print the pattern space?

When:

   - the end of a cycle is reached and `-n` was not used

     Note that the pattern space is, obviously,  not printed if it has just been
     removed by `c` or `d`, since there's nothing left to print.

   - `n` is run and `-n` was not used
     this is because `n` causes a premature end of cycle

   - `p` is run, regardless of `-n`

## What does an empty regex refer to?

It refers to the last matched regex.
This is true regardless of where you  use `//`, and regardless of where the last
regex was used (in a range, in the pattern field of a substitution, ...).

                                    vv
    $ seq 11 13 | sed -n -e '/./=; s//X/p'
    1~
    X1~
    2~
    X2~
    3~
    X3~

In  the previous  command, an  empty regex  is used  in the  pattern field  of a
substitution command.

Let's see another example, where it's used as an address for the `p` command:

                                     vv
    $ seq 11 13 | sed -n -e 's/1/2/; //p'
    21~

Here, `//` refers to 1.
The output contains  only 21, because 12  and 13 have been replaced  with 22 and
23, none of which contains 1.

Here are other examples:

    $ sed '/foo/s//bar/' <<<'foo'
    bar~

                   ┌ hold command
                   │
    $ sed -n '/foo/h; //p' <<<'foo'
    foo~

##
# Pitfalls
## A pattern input by the user is unpredictable. How to avoid a conflict with the delimiter of a `s` command?

Use a literal ‘C-a’ for the delimiter.

To generate one, use this command:

    $ tr 'x' '\001' <<<'x'

Save it in a variable:

    $ A="$(tr 'x' '\001' <<<'x')"

And use it in your `s` command like so:

    $ sed "s${A}/bar/${A}${A}" <<<'foo /bar/ baz'
    foo  baz~

## I need to replace `three` with `two` and `two` with `one`.  It fails: the output contains only `one`!

Your input text is `two three two three`, and you want the output `one two one two`.

You try:

    $ sed 's/three/two/g; s/two/one/g' <<<'two three two three'
    one one one one~

The issue is that after the  first substitution, you can't distinguish between a
`two` which was there originally in the input, and a `two` which has appeared as
a result of the previous edit.
And the next substitution command wants  to replace *only* the `two`s which were
there originally.

Solution:

Reverse the order of the substitutions:

    $ sed 's/two/one/g; s/three/two/g' <<<'two three two three'
    one two one two~

Remember:

When  some text  is used  in  the pattern  *and*  in the  replacement fields  of
substitutions, make sure  to run the substitution where the  text appears in the
pattern field first.

Otherwise, you'll encounter this unexpected chain of substitutions:

    three → two → one

Reverse the order to “break” the chain.

## How to pass several options to sed in a shebang?

The short form of options must be concatenated and `-f` must be at the end:

    #!/usr/bin/sed -nf

None of these would work:

    #!/usr/bin/sed -n -f
    /usr/bin/sed: invalid option -- ' '~

    #!/usr/bin/sed -f -n
    /usr/bin/sed: couldn't open file  -n: No such file or directory~

    #!/usr/bin/sed -fn
    /usr/bin/sed: couldn't open file n: No such file or directory~

Maybe the  first command fails because  the shell only splits  the command after
the path to the  binary; so, it passes the space between `-n`  and `-f` to `sed`
which doesn't recognize it as a valid option.

The last 2 commands  fail because you can't control where  the shell will insert
the path to the script; it's always at the very end.
So, ` -n` and `n` are parsed as the path to a script, which here is not found.

## I have a script which doesn't output anything, even though I don't invoke it with `-n`.  It should!

Make sure it doesn't begin with `#n`.
In a script, the latter is equivalent to `-n` on the command-line.

If it's  there, remove  its line, or  add an  empty line above,  or add  a space
between `#` and `n`, or capitalize `n` ...
Anything which prevents `#n` from being the very first 2 characters of the script.

##
##
##
# Todo
## youtube playlist

<https://www.youtube.com/watch?v=1k7_7e5ugrY&list=PLUQzXLQ6jvHL-Kw9I5H6dvFHal-ynWSTA>

## ?

From irc `#bash`:

            │ !sed-i
    greybot │ Some sed(1)s have -i which claims to "modify" files. It does not: sed is not a FILE editor. The -i flag
            │ re-writes the entire file and replaces the original with the new. This breaks open handles and hard-link
            │ sets, and fails to follow symlinks. -i is also unportable: valid sed on one system will write broken files
            │ on another. Use ed(1) or ex(1) instead: eg. ex -sc '%s/a/b/|wq' file

## ?

Without `-e`  or `-f` options,  sed uses the  first non-option parameter  as the
script, and the following non-option parameters as input files.
If `-e` or `-f` options are used  to specify a script, all non-option parameters
are taken as input files.
Options `-e` and `-f`  can be combined, and can appear  multiple times (in which
case the  final effective  script will  be concatenation  of all  the individual
scripts).

## ?

Placing multiple  commands on the  same line  is highly discouraged  because sed
scripts are difficult  enough to read even  when each command is  written on its
own line.
Note  that the  change,  insert,  and append  commands  must  be specified  over
multiple lines and cannot be specified on the same line.

## ?

    $ sed ':a;N;$!ba;s/\n//g' file.txt

Remove all newlines.

    $ printf '%s\n' 1 2 3 | sed ':a;N;$!ba;s/\n//g'
    123~

## ?

Errata for sed & awk: <https://www.oreilly.com/catalog/errata.csp?isbn=9781565922259>

## ?

When you review  your notes, and you find something  you don't understand, write
an unnamed question right below the current one.
It's better to  write it there than  in a `TO_DO`, because it  provides a better
context.
You'll  immediately  know  where  the  issue   comes  from,  and  where  to  add
modifications once you have a better understanding.

Inside, explicitly write what you don't understand, like a command.
Simplify it several times if needed.
Use the sentence `Let's simplify the command:`.

Maybe you should create a mapping/command which would find all unnamed questions
in a file.

---

If you write a lot of examples which look the same, write a temporary snippet.
Use `complete()` to make it suggest small variations.

For example:

    snippet ex "example" bm
    $1`!p snip.rv = complete(t[1], ['seq 3', 'printf ''%s\\n'' a b c'])` | sed '$0'
    endsnippet

This can be expanded into either of these:

    $ seq 3 | sed ''
    $ printf '%s\n' a b c  | sed ''

