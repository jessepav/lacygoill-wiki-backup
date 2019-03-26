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

    $ ./sed/sed 's/[[=e=]]/X/g' <<<'a é b e c è'
    a é b X c è

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
# In sed, like in awk, how is the first positional argument interpreted without the `-f` option?

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

## And with `-f`?

As the script *file* containing the code to execute on the input:

    $ awk [options] -f <script file> <input file>
    $ sed [options] -f <script file> <input file>

##
# Without any address, which line(s) is/are affected by a sed command, like `s`?

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

# What's the main difference between sed commands and Vim Ex commands with the same name (`s`, `d`, ...)?

In Vim, by default, most Ex commands apply only to the current line.
In sed, by default, commands apply to *all* input lines.

In Vim, you use  addressing to *expand* the number of lines  that are the object
of a command.
In sed,  you use  addressing to  *restrict* the  number of  lines affected  by a
command.

##
# When do I need the `-e` option?

Only when you supply more than one instruction on the command-line.
It tells sed to interpret the next argument as an instruction:

    $ sed -e 'instruction1' -e 'instruction2' input_file

When there is  a single instruction, sed  is able to make  that determination on
its own:

    $ sed -e 'instruction' input_file
    ⇔
    $ sed    'instruction' input_file

# How to specify multiple instructions on the command-line?  (2)

Separate the instructions with a semicolon:

    $ sed 's/pat1/rep1/; s/pat2/rep2/' input_file
                       ^

Or precede each instruction by `-e`:

    $ sed -e 's/pat1/rep1/' -e 's/pat2/rep2/' input_file
          ^^                ^^

# How to combine several scripts (`-f`) and/or expressions (`-e`)?

Simply use as many `-f` and/or `-e` options as needed.
Their concatenation will be the resulting script.

##
# I have these two files, `file1` and `file2`:

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

## How to print the line 2 of `file1`?

    $ sed -n '2p' /tmp/file1

The `p` command allows you to print arbitrary lines from sed's input.

### What's the output of the next command?

    $ sed '2p' /tmp/file1
↣
    foo~
    bar~
    bar~
    baz~
↢

#### Why the difference between the previous command?

By default  (i.e. without `-n`),  sed prints  all processed input  (except input
that has been modified/deleted by commands such as `d`).
To prevent this, you need `-n`.

Note that  this a  fundamental difference  with awk,  which by  default, doesn't
print anything unless you explicitly use `print(f)`.

###
## How to print the last line of `file1`?

    $ sed -n '$p' /tmp/file1

### its first and last line?

    $ sed -n '1p ; $p' /tmp/file1

##
## How to print the first and last line of each of the two files?

    $ sed -ns '1p; $p' /tmp/file1 /tmp/file2
    foo~
    baz~
    spam~
    eggs~

### What's the output of the next command?

    $ sed -n '1p; $p' /tmp/file1 /tmp/file2
↣
    foo~
    eggs~
↢

#### Why the difference between the previous command?

sed treats multiple input files as one long stream.
To force it to consider each file as a *s*eparate stream, you need `-s`.

##
# How to print only the lines where a substitution was made?

Use sed's `-n` option and the `p` flag of the `s` command:

    $ sed -ne 's/pat/rep/p' input_file
          ^^             ^

##
# Why does sed iterate over the input lines before iterating over the script statements?

There may be other reasons, but if it  did the reverse, when used in a pipeline,
the sed command would block all the following commands.
Indeed,  sed would  have to  wait for  the previous  command to  send *all*  its
output, before being able to process the second statement of the script.

# What happens if, in the second address of a range, I use a regex which doesn't match any input line?

If the  first address matches a  line, the sed  command will operate on  all the
lines between this line and the last one.

    $ sed -n '1,/bar/p' <<<$'foo\nbar\nbaz\n'
    foo~
    bar~

    $ sed -n '1,/not_found/p' <<<$'foo\nbar\nbaz\n'
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

##
# How to reverse the meaning of an address/range?

Prefix it with a bang:

    $ sed -n '/foo/,/bar/p' <<<$'one\nfoo\nbar\ntwo\n'
    foo~
    bar~
                         v
    $ sed -n '/foo/,/bar/!p' <<<$'one\nfoo\nbar\ntwo\n'
    one~
    two~

# How to nest ranges? i.e. How to operate on lines matching a specified range inside another specified range?

Write the first range, then use curly braces to surround the command prefixed by
the second range.

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
`two` which was there  originally in the input, and a  `two` which have appeared
as a result of the previous edit.
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

##
##
# Voca

    input    pattern-space    output

`input` et `output` sont l'entrée et la sortie de sed.
`input` peut être:

   - le clavier
   - un fichier:    sed file
   - un pipe:       cmd | sed

`pattern space` est une sorte de cahier de brouillon dans lequel sed travaille.

Ces termes sont importants pour comprendre le fonctionnement de base de sed:

   1. sed copie la 1e ligne de `input` dans `pattern space`

   2. il exécute son programme sur elle

   3. il supprime la ligne transformée et l'écrit sur sa sortie

   4. il passe à la 2e ligne de `input`, et répète les mêmes opérations jusqu'à
      la fin de `input`

# Commandes

    $ sed '' file
    $ sed -n 'p' file

Affiche le contenu de `file`.

La 1e commande affiche `file`, car par défaut, sed écrit le pattern space sur sa
sortie.
Il affiche le résultat de la transformation qu'on lui a demandée d'opérer.

Ici la transformation est vide '', donc sed affiche `file` inchangé.

La 2e  commande affiche `file`, car  on a désactivé l'écriture  du pattern space
via le flag `-n`, mais on exécute  aussi la commande `p` qui réactive l'écriture
du pattern space; `-n` et `'p'` s'annulent.

On peut considérer  que sed ajoute automatiquement une commande  `p` implicite à
la fin de n'importe quel programme.
Et `-n` est le seul moyen de la supprimer.

---

    $ sed -n '' file

N'affiche rien,  car `-n`  (--quiet, --silent)  désactive l'écriture  du pattern
space sur la sortie.

---

    $ sed 'p' file

Affiche 2 fois chaque ligne de `file`:

   - une fois à cause de notre commande `p` explicite
   - une fois à cause de la commande `p` implicite de sed

---

    $ sed -i -E 's/^\s+//g' file.txt

Remove leading spaces.

---

    $ sed ':a;N;$!ba;s/\n//g'  file.txt

Replace newlines in multiple lines.

# Resources

Errata for sed & awk: <https://www.oreilly.com/catalog/errata.csp?isbn=9781565922259>

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

