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

# What's the major difference of purpose of a range in a sed command vs in a Vim Ex command?

In Vim, you use  addressing to *expand* the number of lines  that are the object
of a  command; in  sed, you  use addressing  to *restrict*  the number  of lines
affected by a command.

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

    $ sed -ns '1p ; $p' /tmp/file1 /tmp/file2
    foo~
    baz~
    spam~
    eggs~

### What's the output of the next command?

    $ sed -n '1p ; $p' /tmp/file1 /tmp/file2
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

##
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

    $ sed -n '1,4p' file

Affiche les 4 premières lignes de `file`.

---

    $ sed -n '$i'p foo

Extraire la i-ème ligne de foo

---

    $ sed 's/day/night/g' file.txt

Replace all occurrences of "day" with "night" and write to stdout.

---

    $ sed -i 's/day/night/g' file.txt

Replace all occurrences of "day" with "night" within file.txt.

---

    $ sed 's/day/night/g' <<<'It is daytime'
    It is nighttime~

Replace all occurrences of "day" with "night" on stdin.

---

    $ sed -i -r 's/^\s+//g' file.txt

Remove leading spaces.

---

    $ sed '/^$/d' file.txt

Remove empty lines and print results to stdout.

---

    $ sed ':a;N;$!ba;s/\n//g'  file.txt

Replace newlines in multiple lines.

##
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

