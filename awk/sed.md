# ?

    w filename

Write the pattern space to filename.
Two special  values of filename  are supported: `/dev/stderr`, which  writes the
result to  the standard error, and  `/dev/stdout`, which writes to  the standard
output – this is equivalent to `p` unless the `-i` option is being used.

The file will be created (or truncated) before the first input line is read; all
`w` commands  (including instances of the  `w` flag on successful  `s` commands)
which refer  to the same filename  are output without closing  and reopening the
file.

##
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
    $ sudo checkinstall

Without `--prefix`, the binary will be in `/usr/local/bin/sed`.
This may break your scripts, if their shebang refer to `/usr/bin/sed` instead.

Without `--without-included-regex`, sed doesn't support equivalence classes:

    $ /usr/bin/sed 's/[[=e=]]/X/g' <<<'a é b e c è'
    a é b X c è~

If checkinstall fails to install the deb  – because it would have to overwrite a
file which is present in another package – run:

    $ sudo dpkg -i --force-overwrite package.deb

Or,  if the  issue is  with an  `info/dir`  file, try  to move  its location  by
reconfiguring with  `--infodir=/usr/local/share/info` (use any directory  as you
see fit).

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
Not because of a dependency issue; because of an error in the source code.

##
# Command-line
## In sed, like in awk, how is the first positional argument interpreted without the `-f` option?

As the script *code* to execute on the input:

    $ awk [options] <script code> <input file> ...
    $ sed [options] <script code> <input file> ...

---

Note that the synopsis of grep looks the same:

    $ grep [options] <pattern> <input file> ...

This choice of order between the script/pattern and the input data is due to the
fact that the latter  is unpredictable; you can't know in  advance what the user
will operate on (one file, two files, ...).
If  the  input  came  before  the  script/pattern, there  would  be  no  way  to
distinguish the latter from the input.

### And with `-f`?

As the script *file* containing the code to execute on the input:

    $ awk [options] -f <script file> <input file>
    $ sed [options] -f <script file> <input file>

###
## What does `-n` suppress?  (2)

The auto-print  of the pattern  space when reaching the  end of the  script, and
before replacing it with the next input line (`n` command).

## What can't `-n` suppress?

The auto-print of the text inserted by an `a`, `i` or `c` command.

##
## When do I need the `-e` option?

Only when you supply more than one instruction on the command-line.
It tells sed to interpret the next argument as an instruction:

    $ sed -e 'instruction1' -e 'instruction2' input_file

When there is  a single instruction, sed  is able to make  that determination on
its own:

    $ sed -e 'instruction' input_file
    ⇔
    $ sed    'instruction' input_file

## How to specify multiple instructions on the command-line?  (2)

Separate the instructions with a semicolon:

    $ sed 's/pat1/rep1/; s/pat2/rep2/' input_file
                       ^

Or precede each instruction by `-e`:

    $ sed -e 's/pat1/rep1/' -e 's/pat2/rep2/' input_file
          ^^                ^^

## How to combine several scripts (`-f`) and/or expressions (`-e`)?

Simply use as many `-f` and/or `-e` options as needed.
Their concatenation will be the resulting script.

##
## Which option is implied by `-i`?

`-s`.

That is,  when you ask  sed to edit  files in-place, it  automatically considers
them as separate.

## How to make sed create a backup of a file before editing it in-place?

Provide a file extension to `-i`:

    $ sed -i.bak 's/pat/rep/' file

This will create `file.bak` which will contain the original contents of `file`.

---

For this reason, you can't combine `-i` with another single-letter option right after.
For example, you can't combine `-i` and `-e` like this: `-ie`.
`e` would be interpreted as a backup extension.

##
## Which commands can *not* be terminated by a semicolon?

`r`, `w`, `a`, `i`, `c`.

---

    $ sed -n 's/x/y/w /tmp/.file; p' <<<'x'

The  previous command  will save  the  output of  the substitution  in the  file
`/tmp/.file; p`.
While you may  have expected it to  be saved in `/tmp/.file`, then  `p` to print
the pattern space.

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

    $ seq 3 | sed -e '2 {w /tmp/.file' -e 's/.*/[&]/}'
    1~
    [2]~
    3~

    $ cat /tmp/.file
    2~

Or insert a literal newline:

    $ seq 3 | sed -e '2 {w /tmp/.file
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
They're  always interpreted  the same  way,  as anchors,  regardless of  whether
they're backslashed.

## What are the differences between BRE and the magic mode in Vim?

In sed, the equivalent of the Vim's quantifier `\{n,m}` needs two backslashes:

    \{n,m\}
         ^

But in practice, Vim understands `\{n,m\}` too.

---

In Vim (like in  awk) you can include a closing square  bracket inside a bracket
expression by escaping it with a backslash:
bracket expression

    [a\]1]

This regex will match `a` or `]` or `1`.

But it won't work in sed, nor in grep.

##
## How to include an opening bracket in a bracket expression?

Just write it.

There's no need to backslash it or  put it in a special position, because inside
a bracket expression, all characters lose their special meaning; except:

   - `-`
   - `\`
   - `]`
   - `^`

### How about a closing bracket?

Make sure the closing bracket is at the start of the expression, and unescaped:

    []ab]
     ^

This regex will match `]` or `a` or `b`.

---

If the bracket expression is reversed, put it in second position:

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

From this point of view, sed is similar to Vim.

---

OTOH, awk interprets `^` and `$` specially even in the middle of a pattern:

    $ awk '/ ^ /' <<<'a ^ b'
    ''~

To match a literal `^` in an awk pattern, you need to backslash it:
    ~
    $ awk '/ \^ /' <<<'a ^ b'
    a ^ b~

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

###
## How to apply the same range to a set of commands?

Group them inside curly braces:

    $ printf '%s\n' 'x y' 'c x y' 'x y' | sed '/c/ {s/x/a/; s/y/b/}'
    x y~
    c a b~
    x y~

## How to reverse the meaning of an address/range?

Prefix it with a bang:

    $ printf '%s\n' c a b d | sed -n '/a/,/b/p'
    a~
    b~
                                             v
    $ printf '%s\n' c a b d | sed -n '/a/,/b/!p'
    c~
    d~

## How to nest ranges? i.e. How to operate on lines matching a specified range inside another specified range?

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
They would all  be limited to their  respective range *and* to  the range before
the curly braces.

### Can ranges be nested with an arbitrary depth?

Yes:

    $ printf '%s\n' a b c b a b c b | sed -n '/a/,/a/ { /b/,/b/ { /c/ p } }'
    c~

In this example, we ask sed to print  the lines containing a `c`, inside a range
of lines whose first and last contain a `b`, inside a range of lines whose first
and last contain an `a`.

Only the first `c` is printed.
The second one is satisfies only 2 conditions out of 3:

   - it contains a `c`
   - it's inside a range of lines whose first and last contain a `b`
   - it's *not* inside a range of lines whose first and last contain an `a`

##
## What happens if the second address of a range is a regex
### and is identical to the first address?

sed will look for the *next* line which matches the pattern.
It won't re-use the same line:

    $ printf '%s\n' a b a x | sed -n '/a/,/a/ { /b/,/b/ p }'
    b~
    a~

### and it doesn't match any input line?

If the  first address matches a  line, the sed  command will operate on  all the
lines between this line and the last one.

    $ printf '%s\n' foo bar baz | sed -n '1,/bar/p'
    foo~
    bar~

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
ahead to determine  if the second match  will be made, because  it iterates over
the input lines first.
As soon as  an input line matches  the first address, the command  is applied to
*all* lines, until another line matches the second address (if any).

#### and the command is inside a group (`{}`) which is prefixed by another range?

This time, the command does *not* operate on  all the lines until the end of the
input.
Instead, it operates  on all the lines until  the last line in the  range of the
current block:

    $ printf '%s\n' a b a c | sed -n '/a/,/a/ { /b/,/x/ p }'
    b~
    a~

Here, even though  the regex `x` fails  to match a line,  the `p`command doesn't
print all the lines until the end of the  input – if it did, it would also print
`c`.
It stops at the  second line `a` because that's the end of  the range applied to
the current block.

###
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
## I have these two files, `file1` and `file2`:

    $ cat <<'EOF' >/tmp/file1
    foo
    bar
    baz
    EOF

    $ cat <<'EOF' >/tmp/file2
    spam
    ham
    eggs
    EOF

### How to print the line 2 of `file1`?

    $ sed -n '2p' /tmp/file1

The `p` command allows you to print arbitrary lines from sed's input.

#### What's the output of the next command?

    $ sed '2p' /tmp/file1
↣
    foo~
    bar~
    bar~
    baz~
↢

##### Why the difference between the previous command?

By default  (i.e. without `-n`), sed  prints the pattern  space at the end  of a
cycle (except if it has been deleted by commands such as `d`).
To prevent this, you need `-n`.

Note that  this a  fundamental difference  with awk,  which by  default, doesn't
print anything unless you explicitly use `print(f)`.

####
### How to print the last line of `file1`?

Use the special symbol `$`:

    $ sed -n '$p' /tmp/file1
              ^

#### its first and last line?

    $ sed -n '1p ; $p' /tmp/file1

###
### How to print the first and last line of each of the two files?

    $ sed -ns '1p; $p' /tmp/file1 /tmp/file2
    foo~
    baz~
    spam~
    eggs~

#### What's the output of the next command?

    $ sed -n '1p; $p' /tmp/file1 /tmp/file2
↣
    foo~
    eggs~
↢

##### Why the difference between the previous command?

sed treats multiple input files as one long stream.
To force it to consider each file as a *s*eparate stream, you need `-s`.

###
## How to print only the lines where a substitution was made?

Use sed's `-n` option and the `p` flag of the `s` command:

    $ sed -ne 's/pat/rep/p' input_file
          ^^             ^

##
## How to print the pattern space with non-printable characters being represented via C-style escaped form?

Use the `l` command.

    $ sed 'l; s//Escape/' <<<$'this is an \e character'
    this is an \033 character$~
    this is an Escape character~

Since we haven't used `-n`, the input line is printed twice.
The first one is due to the `l`  command, but at that point the Escape character
has not yet been translated.
The second  one is  due to sed  printing the  pattern space at  the end  of each
cycle, and here, at that point, the Escape character *has* been translated.

### What's the default line-wrap length?

70

    $ sed -n 'l; s//Escape/' <<<$'this is a very very very very very very long line with an \e character'
    this is a very very very very very very long line with an \033 charac\~
    ter$~

### How to wrap the output line after 10 characters?  (2)

Pass the numerical argument `10` to `l`:

    $ sed -n 'l 10; s//Escape/' <<<$'this is an \e character'
    this is a\~
    n \033 ch\~
    aracter$~

Or use the `-l` shell option:

    $ sed -l10 -n 'l; s//Escape/' <<<$'this is an \e character'
    this is a\~
    n \033 ch\~
    aracter$~

### How to prevent the output line from being wrapped?

Pass the value `0` to the `l` command or to the `-l` option:

    $ sed -n 'l0; s//Escape/' <<<$'this is a very very very very very very long line with an \e character'
    $ sed -l0 -n 'l; s//Escape/' <<<$'this is a very very very very very very long line with an \e character'
    this is a very very very very very very long line with an \033 character$~

##
## How to print the current input line number (with a trailing newline)?

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
## How to print the pattern space after every successful substitution?

Use the `p` flag:

    $ printf '%s\n' a 1 b 2 | sed -n 's/[0-9]/+&/p'
    +1~
    +2~

## How to write the result of a substitution into a file?

Use the `w` flag:

    $ printf '%s\n' a 1 b 2 | sed -n 's/[0-9]/+&/w file'

    $ cat file
    +1~
    +2~

`s` has  replaced `1`  with `+1` and  written the result  into `file`,  then has
replaced `2` with `+2` and appended the result into `file`.

##
## How to limit a substitution to
### the `n`th occurrence of the pattern?

Write the index of the occurrence in the flag field of the substitution command:

                 v
    $ sed 's/x/y/2' <<<'x x x'
    x y x~

### all the occurrences beyond the `n`th occurrence of the pattern?

Do the same as before, and add the `g` flag:

                 vv
    $ sed 's/x/y/2g' <<<'x x x'
    x y y~

##
## What's the output of the next commands?

    $ sed '/foo/s//bar/' <<<'foo'
↣
    bar~
↢

    $ sed -n '/foo/h; //p' <<<'foo'
↣
    foo~
↢

    $ sed -n '/foo/p; s//bar/p' <<<'foo'
↣
    foo~
    bar~
↢

### What happened?

When sed finds an empty regex, it uses the previous one which matched some text.

##
## When can a substitution command be broken on multiple lines?

When its replacement field contains a newline.

### How?

By writing a backslash anywhere in the replacement field:

    $ sed 's/pat/b\
    c/' <<<'a pat d'
    a b~
    c d~

##
# Insertion
## How to insert a line of text
### before an input line?

Use the `i` command:

    $ seq 3 | sed '2i inserted before 2'
    1~
    inserted before 2~
    2~
    3~

All the whitespace between  the command and the line of text  is ignored, so the
space  between  `i`  and `inserted  before  2`  is  just  there to  improve  the
readability of the code.

### after an input line?

Use the `a` command:

    $ seq 3 | sed '2a inserted before 2'
    1~
    2~
    inserted before 2~
    3~

##
## How to change the contents of an input line?

Use the `c` command:

    $ seq 3 | sed '2c changed line 2'
    1~
    changed line 2~
    3~

##
## When is the text added by `a`, `i`, `c` printed exactly?

At the end of the current cycle, or when the next input line is read with `n`.

    $ printf '%s\n' a b c | sed -e '1a inserted' -e 'n;='
    a~
    inserted~
    2~
    b~
    c~

Notice that `inserted` is printed *before* the line address of the next line.
It's  printed right  after  `a`;  both are  printed  because  of the  auto-print
entailed by `n`.

##
## How to insert *multiple* lines of text before/after an input line?

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

##
## What's the only way to terminate an `a`, `i` or `c` command?

Write a literal newline (!= `\n`).

### Is there another way on the shell command-line?

Yes, use several `-e` options:

    $ seq 3 | sed -e '2i hello' -e 'w /tmp/.file'
    1~
    hello~
    2~
    3~

---

You can  also use this trick  to separate the `a`,  `i` or `c` command  from the
first line of text, when using their  original syntax (the one where the command
is immediately followed by a backslash):

    $ seq 3 | sed -e '2i\' -e hello
    1~
    hello~
    2~
    3~

This works  because sed automatically separates  several expressions (introduced
by `-e`)  with a  newline, and  because the backslash  at the  end of  the first
expression suppresses the special meaning of the newline.

###
## How to insert a line beginning with some whitespace, without the latter being removed?

Prefix the whitespace with a backslash.

                     ┌ will be ignored
                     │ ┌ won't be ignored
                     │ ├──┐
    $ seq 3 | sed '2a \    hello'
    1~
    2~
        hello~
    3~

##
## What's the output of the next
### `a` command?

    $ seq 3 | sed -ne '2a hello'
↣
    hello~
↢

#### Why is there an output even though we used `-n`?

`a`, `i` and `c` explicitly asks sed to output the result of their operation.
In this regard, they are similar to `p` which also ignores `-n`.

##
### `a` command?

    $ seq 3 | sed -e '2a hello' -e '3s/./X/'
↣
    1~
    2~
    hello~
    X~
↢

#### Why wasn't the substitution applied on the third line of the output?

Because the line inserted  by `a` is not added to the input  (nor to the pattern
space); it will  simply be output at the  end of the current cycle,  or when the
next input line is read – with `n` – regardless of the presence of `-n`.
While `s` operates on the third *input* line.

---

More generally, addresses refer to input lines, not to the output.

    $ seq 3 | sed -e '2d; 3s/./X/'
    1~
    X~

Here, even though `d` removes a line,  which leaves us with only 2 output lines,

`s` still  performs its substitution  on the third  input line; it  doesn't care
about the output.

---

IOW, sed commands may modify the output but have no effect on the input.

Rationale: It makes the code simpler.
If you had to take into consideration the  change of address of a line caused by
a previous command, it would make thinking about the code more difficult.

###
### `i` command?

    $ seq 5 | sed '3,4i hello\nworld'
↣
    1~
    2~
    hello~
    world~
    3~
    hello~
    world~
    4~
    5~
↢

#### Explain what happened.

`a` , and `i`, can operate on a range of lines.
Here, `a` appends  the lines `hello` and  `world` after every line  in the range
(that is after line `2` and `3`).

###
## When is the text added by the `a`, `i`, `c` commands printed?

At the very end of the cycle:

    $ printf '%s\n' a b c | sed -e '2a inserted' -e '='
    1~
    a~
    2~
    b~
    inserted~
    3~
    c~

Notice that `inserted` is printed after 2 (`=`) and after `b` (auto-print).

##
# Change, Deletion
## What's the effect of `d` for the next commands?

It starts the next cycle immediately.
IOW, the rest of the commands of the script are ignored.

Indeed, since  the next  commands (if any)  can only be  applied to  the pattern
space, and since `d` deletes the pattern space, there's nothing left to process.

## Which commands following a `c` command are processed?

None.

For the same reason as `d` (`c` also deletes the pattern space).

    $ printf '%s\n' a b c | sed -n -e '2c changed' -e '='
    1~
    changed~
    3~

Notice that `=` was not run on the second line; otherwise we would have read 2.

###
## What's the output of the next
### `d` command?

    $ sed 'p; d' <<<'x'
↣
    x~
↢

#### Explain what happened.

`p` has printed  the input line, but  sed didn't print the pattern  space at the
end of the cycle, because the latter has been deleted.
This illustrates that not only does  `d` make sed ignore subsequent commands, it
also make sed ignore its default action of printing the pattern space.

###
### `c` command?

    $ seq 4 | sed '2,3c hello\nworld'
↣
    1~
    hello~
    world~
    4~
↢

#### Explain what happened.

`c` can operate on a range of lines, like `a` and `i`.
But, it doesn't interpret a range like `a` and `i`.
It doesn't repeat an operation on every line in the range.
Instead, it  operates just once, after  removing (cutting) all the  lines in the
range.

##
### `c` command?

    $ seq 4 | sed -e '2,3 { c hello' -e '}'
↣
    1~
    hello~
    hello~
    4~
↢

#### Why did `c` repeat its operation several times?

This is a particular case.
When `c` is inside  curly braces, and the latter is prefixed by  a range, `c` is
repeated once for every line in the range.

####
### `$ cat` command?

    $ seq 3 | sed -e '2c hello' -e 'w /tmp/.file'
    $ cat /tmp/.file
↣
    1~
    3~
↢

#### Why are there only 2 lines in the file?

Because `c` deletes the pattern space (before replacing its contents).
And  when the  pattern space  is deleted,  the next  commands are  automatically
ignored; sed immediately starts a new cycle.

##
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

It queues  the contents of  `filename` to be read  and inserted into  the output
stream at  the end of  the current cycle,  or when the  next input line  is read
(with sth like `n`).

Example:

    $ seq 4 | sed '2r/etc/hostname'
    1~
    2~
    ubuntu~
    3~
    4~

### How to import it after every line in a range?

Prefix `r` with the appropriate range.
The file will then be reread and inserted after each of the addressed lines.

    $ seq 5 | sed '2,3r /etc/hostname'
    1~
    2~
    ubuntu~
    3~
    ubuntu~
    4~
    5~

##
## How to read the standard input, when the sed command has been passed a filename as argument?

Use the special value `/dev/stdin`:

    $ seq 3 | sed 'r/dev/stdin' /etc/hostname
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

    $ cat <<'EOF' >/tmp/.file
    1. this line is ok
    2. this line has a BUG
    3. this line is also ok
    4. this line has also a BUG
    EOF

    $ sed -n -e '/BUG/ {s/this line//; w /tmp/bugs' -e '}' /tmp/.file

    $ cat /tmp/bugs
    2.  has a BUG~
    4.  has also a BUG~

---

Note that you're not limited to whole lines, you can also extract a particular field:

    $ cat <<'EOF' >/tmp/.file
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
          /tmp/.file

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

## How to write a file on the standard error?

Use the special value of filename `/dev/stderr`.

### On the standard output?

Use the special value of filename `/dev/stdout`.

#### `p` is equivalent to writing on the standard output. So, how is the previous answer useful?

When you use `-i`, `p` doesn't write on stdout, but on the file:

    # will double the lines in file
    $ sed -i 'p' file

In this case, if you still want to write on stdout, you need `w /dev/stdout`.

##
# Changing the Normal Flow of Control
## What does the `n` command do exactly?

*Let's call the current line A, and the next two lines B and C.*

`n` prints the  pattern space – unless  sed was invoked with `-n`  – and replaces
its contents with the next input line.

The next  cycle will take this  replacement into account; it  won't re-process B
twice; it will jump to C.

In effect,  the commands after `n`  won't be applied  to A, and the  ones before
won't be applied to B.

## How to remove the next line after any line matching `foo`?

Use the `n` command:

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

     note that the pattern space is, obviously,  not printed if it has just been
     removed by `c` or `d`

   - `p` is run, regardless of `-n`
   - `n` is run, and `-n` was not used

## When does sed print the text added by `a`, `i`, `c`?

When the pattern space is printed.

But contrary to  the pattern space, which  may not be printed if  `-n` was used,
the text added by `a`, `i`, `c` is *always* printed.

##
## What does an empty pattern refer to?

It refers to the last search pattern:

                                    vv
    $ seq 11 13 | sed -n -e '/./=; s//X/p'
    1~
    X1~
    2~
    X2~
    3~
    X3~

In the  previous command, the empty  pattern is used  in the pattern field  of a
substitution command.
Let's see another example, where it's used as an address for the `p` command:

                                     vv
    $ seq 11 13 | sed -n -e 's/1/2/; //p'
    21~

Here, `//` refers to 1.
The output contains  only 21, because 12  and 13 have been replaced  with 22 and
23, none of which contains 1.

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

Reversing the order “breaks” the chain.

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

## I have a script which doesn't output anything, even though I don't invoke it with `-n`!

Make sure it doesn't begin with `#n`.
In a script, the latter is equivalent to `-n` on the command-line.

If it's  there, remove  its line, or  add an  empty line above,  or add  a space
between `#` and `n`, or capitalize `n` ...
Anything which prevents `#n` from being the very first 2 characters of the script.

##
##
##
# Todo
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

