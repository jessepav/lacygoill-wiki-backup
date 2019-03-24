# ?

Without `-e`  or `-f` options,  sed uses the  first non-option parameter  as the
script, and the following non-option parameters as input files.
If `-e` or `-f` options are used  to specify a script, all non-option parameters
are taken as input files.
Options `-e` and `-f`  can be combined, and can appear  multiple times (in which
case the  final effective  script will  be concatenation  of all  the individual
scripts).

##
# Installation

Go to <https://www.gnu.org/software/sed/>  to find a url to  download the latest
stable source release.
Atm, you can use this url: <https://ftp.gnu.org/gnu/sed/>

Download the archive and its signature, and check it:

    $ gpg --keyserver x-hkp://pool.sks-keyservers.net --recv-keys 000BEEEE
    $ gpg --verify sed-4.7.tar.xz.sig sed-4.7.tar.xz

Finally, configure, compile and install:

    $ ./configure
    $ make
    $ make check
    $ sudo checkinstall

    # you may  need this  if checkinstall  fails to install  the deb  because it
    # would have to overwrite a file which is present in another package
    $ sudo dpkg -i --force-overwrite package.deb

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
    foo~
    eggs~

#### Why the difference between the previous command?

sed treats multiple input files as one long stream.
To force it to consider each file as a *s*eparate stream, you need `-s`.

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

