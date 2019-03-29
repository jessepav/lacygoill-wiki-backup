# ?

Weird results:

    # expected result
    $ awk '{ print strtonum($1) }' <<<'0x11'
    17~

    # I would expect `9`
    $ awk '{ print strtonum($1) }' <<<'011'
    11~

Why the difference?
Why doesn't `strtonum()` treat `011` as an octal number?

---

May be related to the attribute:

    $ awk '{ print typeof($1) }' <<<'0x11'
    string~

    $ awk '{ print typeof($1) }' <<<'011'
    strnum~

Why does awk consider `0x11` as a string even though it looks like an hex number,
and thus should be considered a numeric string with the strnum attribute?

Look here: <http://pubs.opengroup.org/onlinepubs/9699919799/utilities/awk.html>
And look for “numeric string”.

Update: <https://unix.stackexchange.com/a/364116/289772>

> To clarify, only  strings that are coming  from a few sources  (here quoting the
> POSIX spec): [...] are to be considered  a numeric string if their value happens
> to be numerical  (allowing leading and trailing blanks,  **with variations between**
> **implementations in support for hex**, octal, inf, nan...).

##
# Can I use `0x123` and `0123` as hex and octal numbers?  (two cases to distinguish)

Outside a string, yes:

    $ awk '{ print 0x123 }' <<<''
    291~

    $ awk '{ print 0123 == 83 }' <<<''
    1~

Inside a string, no:

    $ awk '{ print "0x123" + 0 }' <<<''
    0~

    $ awk '{ print "0123" + 0 }' <<<''
    123~

This differs from VimL:

    :echo "0x123" + 0
    291~

    :echo "0123" + 0
    83~

# How to convert a hex or octal number contained in a string into a decimal one?

Use `strtonum()`:

    $ awk '{ print strtonum($0) }' <<<'0x123'
    291~

---

Note that you can't rely on `+ 0`:

    $ awk '{ print $0 + 0 }' <<<'0x123'
    0~

    $ awk '{ print $0 + 0 }' <<<'0123'
    123~

Page 196 of the user's guide:

> Using the  `strtonum()` function is  not the same as  adding zero to  a string
> value; the  automatic coercion of  strings to  numbers works only  for decimal
> data, not  for octal or  hexadecimal.

However, `+ 0` would work with `--non-decimal-data`:

    $ awk -n '{ print $0 + 0 }' <<<'0x123'
    291~

But this option is not recommended by the user's guide.

# Why does `print strtonum($0)` outputs `123` when `$0` is `0123`?

    $ awk '{ print strtonum($0) }' <<<'0123'
    123~

Because of two things:

   1. `0123` comes from the input data, and so is given the `strnum` attribute:

        $ awk '{ print typeof($0) }' <<<'0123'
        strnum~

      As a result, `0123` has two values: a numeric one and a string one.

   2. `strtonum()` is designed to handle both string and number inputs; it looks
      for numbers first, and when it encounters an input number, returns the
      latter without transformation.

<https://unix.stackexchange.com/a/503139/289772>

## How to make `strtonum()` treat `0123` as an octal number then?

Use a dummy string concatenation:

    $ awk '{ print strtonum($0 "") }' <<<'0123'
    83~

The concatenation will  coerce the numeric string into a  regular string, and so
`strtonum()` will receive a data with only one value (not two).

##
# What's the output of the next command?

    $ awk '{ print $1 "" + 0 }' <<<'0123'
    ↣ 01230 ↢

## Why?

The addition operator has priority over the concatenation.
And `"" + 0` evaluates to the number `0`.
Finally, the  concatenation operator expects  strings, so it coerces  the number
`0` into the string `"0"`, and concatenates it to `$1`.

##
# In a test, is `"0"` true or false?

It's true:

    $ awk '{ print "0" ? "true" : "false" }' <<<''
    true~

That's because for awk, *any* non-empty string is true:

    $ awk '{ print "hello" ? "true" : "false" }' <<<''
    true~

Python behaves like awk, btw:

    $ python3 -c "print('true' if '0' else 'false')"
    true~

---

In contrast,  in Vim,  the string would  first be coerced  into a  number, which
makes the result of a test less predictable:

    :echo '0' ? 'true' : 'false'
    :echo 'hello' ? 'true' : 'false'
    false~

## What's the output of the next command?

    $ awk '{ print $1 ? "true" : "false" }' <<<'0'
    ↣ false ↢

### Why?

`"0"` is false because it has the  strnum attribute, and awk first considers its
numeric value, which is `0`.

##
# How does the automatic coercion of numeric strings into numbers differ in awk compared to Vim?

In Vim, it:

   - is able to recognize binary/octal/hexadecimal numbers (see `:h octal`)

   - takes care of converting it into decimal

        :echo '0b101' + 0
        5~

        :echo '0123' + 0
        83~

        :echo '0x123' + 0
        291~

In awk, it does no such things:

    $ awk '{ print "0123" + 0 }' <<<''
    123~

    $ awk '{ print "0x123" + 0 }' <<<''
    0~

##
# Regex
## Which syntax (BRE, ERE, ...) can I use in a regex?

Gawk only recognizes a superset of the ERE syntax.

## How are the metacharacters `^` and `$` interpreted in the middle of a pattern?

Specially:

    $ awk '/ ^ /' <<<'a ^ b'
    ''~

To match a literal `^` in an awk pattern, you need to backslash it:
    ~
    $ awk '/ \^ /' <<<'a ^ b'
    a ^ b~

From this point of view, awk is different than Vim.

---

OTOH, sed interprets `^` and `$` literally even in the middle of a pattern:

    $ sed 's/ ^ /X/' <<<'a ^ b'
    aXb~

##
# ?

For which operators may a strnum data need a dummy concatenation or `+ 0`?

    # `!` parses '0' as a number
    $ awk '{ print !($0) }' <<<'0'
    1~

    # if you want `!` to parses '0' as a string, you need a dummy concatenation
    $ awk '{ print !($0 "") }' <<<'0'
    0~

---

    # contrary to VimL, can't use `printf()` to convert to decimal
    $ awk '{ printf("%d", "0123") }' <<<''
    123~

    # contrary to VimL, can't use `printf()` to convert to decimal
    $ awk '{ printf("%d", "0x123") }' <<<''
    123~

    # but you can use `printf()` to convert from decimal
    $ awk '{ printf("%#x", "291") }' <<<''
    0x123~
    # same thing in python
    $ python -c "print('{:#x}'.format(291))"

    $ awk '{ printf("%#o", "83") }' <<<''
    0123~
    $ python -c "print('{:#o}'.format(83))"
    0o123~

# ?

`3` sorts lexicographically after `1`:

    $ awk '{ x = "3.14"; print (x < 12) }' <<<''
    0~

`CONVFMT` is used whenever a number needs to be coerced into a string:

    $ awk '{ CONVFMT="%.6e"; x = 3.14; print x "" }' <<<''
    3.140000e+00~

As a result, a comparison with a string may be influenced by `CONVFMT`:

    $ awk '{ x = 3.14; print (x == "3.14") }' <<<''
    1~

    $ awk '{ CONVFMT = "%.6e"; x = 3.14; print (x == "3.14") }' <<<''
    0~

# ?

For more info, see page 433 of the gawk user's guide, and:
<http://gawkextlib.sourceforge.net/>
<https://sourceforge.net/projects/gawkextlib/files/>

Install gawk shared library:

    $ git clone git://git.code.sf.net/p/gawkextlib/code gawkextlib
    $ cd ~/GitRepos/gawkextlib/lib
    $ autoreconf -i && ./configure && make && make check

    $ sudo checkinstall

Name it  `libgawkextlib`, and use  the `README` for  the summary the  version is
given in `configure.ac` (look for the line `AC_INIT`).

---

Build `tre` which is a dependency of the `aregex` library extension:

    $ cd ~/GitRepos/
    $ git clone https://github.com/laurikari/tre/
    $ cd tre
    $ ./utils/autogen.sh

    $ ./configure && make && make check

If one  of the test fails,  read the logfile;  you probably need to  install the
locale `en_US ISO-8859-1`.
On Ubuntu, run: `$ locale-gen en_US`.
On Debian, edit `/etc/locale.gen` and run `$ sudo locale-gen`.

You don't need to specify `ISO-8859-1`, because that's the default codepage.
<https://unix.stackexchange.com/a/446762/289772>

You  don't run  the  same command  in  Debian, because  Ubuntu  has tweaked  the
`locale-gen` utility.
<https://unix.stackexchange.com/a/38735/289772>

    $ sudo checkinstall

The installation  may fail because  of the  `Requires` field which  is populated
with `/sbin/ldconfig`.
Debian  wants  the  name of  a  package,  not  a  path: give  the  package  name
`libc-bin`.

---

Build the `aregex` library extension.
Name it `gawk-aregex` instead of just `aregex`.

    $ cd ~/GitRepos/gawkextlib/aregex
    $ autoreconf -i && ./configure && make && make check
    $ sudo checkinstall

For more info, see:

    $ man 3am aregex

“am” stands for Awk Module.

---

Similarly install other library extensions in `gawkextlib/`.

    # Exit gawk without running END rules
    abort

    # test fails atm
    csv

    # convert errno values to strings and vice versa
    errno

    # need the `libgd-dev` package
    # test fails atm
    gd

    # need the `libhpdf-dev` package
    # there's no documentation, except for `~/GitRepos/gawkextlib/haru/test/pdftest.awk`
    haru

    json
    lmdb

    # add 4 functions to work with multibyte strings
    mbs

    # test fails atm
    mpfr

    nl_langinfo
    pgsql
    redis

    # enable I/O multiplexing, non-blocking I/O, and signal trapping
    select

    xml

For more info, see:

    $ man  3am [abort|csv|...]

# ?

Talk about the similarities and difference between awk's `strtonum()` and VimL's `str2nr()`.

# ?

    # STRING STRING: string comparison
    # if 'ab' and 'cd' had been converted into 0, the test would have failed
    #     $ awk '{ print (strtonum("cd") > strtonum("ab")) }' <<<''
    #     0
    $ awk '{ print ("cd" > "ab") }' <<<''
    1~

    # STRING NUMERIC: string comparison
    # if 'ab' had been converted into 0, the test would have failed;
    # it succeeds because digits come before letters in the lexicographical order
    $ awk '{ print ("ab" > 123) }' <<<''
    1~

    # STRING STRNUM: string comparison
    # if 'ab' had been converted into 0, the test would have failed
    $ awk '{ print ("ab" > $1) }' <<<'123'
    1~



    # NUMERIC NUMERIC: numeric comparison
    # if 089 and 89 had been treated as strings, the test would have failed
    $ awk '{ print (089 == 89) }' <<<''
    1~

    # STRNUM STRNUM: numeric comparison
    # if 089 and 89 had been treated as strings, the test would have failed
    $ awk '{ print ($1 == $2) }' <<<'089 89'
    1~

    # NUMERIC STRNUM: numeric comparison
    # if 089 and 89 had been treated as strings, the test would have failed
    $ awk '{ print ($1 == 89) }' <<<'089'
    1~

# ?

What's the output of the next commands:

    $ awk '{ print 0128 }' <<<''
    ↣ 0 ↢

    $ awk '{ print 0x12g }' <<<''
    ↣ 18 ↢

    $ awk '{ var = $1; print typeof(var) }' <<<'0123'

An octal number can't contain digits beyond `7`, and so `0128` is evaluated as `0`.
An hexadecimal number can't contain digits beyond `f`, and so `0128` is evaluated as `0`.

---

    print (031 < 30)
    1~
    print (310 < 30)
    0~
    print (0318 < 300)
    0~

Le 1er test réussit car `031` est interprété comme un nombre octal:

    031₈ < 30₁₀    ✔
    │
    └ 031₈ = 1 + 3*8 = 25

Le 2e test échoue car `0310` est interprété comme un nombre octal:

    0310₈ < 30₁₀    ✘
    │
    └ 0310₈ = 0 + 8 + 3*8*8 = 200

Le 3e test échoue car `0318` est interprété comme un nombre décimal.
En effet, même s'il  commence par un zéro, il ne peut  pas être interprété comme
un nombre octal, car il contient le chiffre 8.


Dans du code awk,  qd c'est possible (pas de chiffres  inexistant en base 8/16),
un nombre commençant par:

   - 0           est interprété comme un nombre octal
   - 0x (et 0X?) est interprété comme un nombre hexadécimal

# ?

How to write an octal or hexadecimal constant
in a program text?

Prefix it with `0`, `0x` or `0X`:

    $ awk '{ print 0123 }' <<<''
    83~

    $ awk '{ print 0x123 }' <<<''
    291~

in the input data?  (2)

Use `strtonum()` and a dummy concatenation:

    $ awk '{ print strtonum($1 "") }' <<<'0123'
    83~

Or (not recommended), use `-n/--non-decimal-data`:

    $ awk -n '{ print $1 + 0 }' <<<'0123'
    83~

---

What's the output of these commands:

    $ awk '{ print 0123 }' <<<''
    ↣ 83 ↢

    $ awk -n '{ print $1 }' <<<'0123'
    ↣ 0123 ↢

Why the difference?

`print` treats its arguments as strings.
Although field  references can  act as  numbers when  necessary, they  are still
strings, so `print` does not try to treat them numerically.

You need to add zero to a field to force it to be treated as a number:

    $ awk -n '{ print $1 + 0 }' <<<'0123'
    83~

---

Can an octal/hexadecimal number be used in a decimal fraction or in scientific notation?

No, you won't get the expected result:

    $ awk '{ print 012.34 }' <<<''
    12.34~

    $ awk '{ print 0x12.34 }' <<<''
    18~

    $ awk '{ print 012.34e-1 }' <<<''
    1.234~

    $ awk '{ print 0x12.34e-1 }' <<<''
    18~

IOW, the base of a number is *not* orthogonal to its form.
You can't use a non-decimal base with any form; only with the integer form.

# ?

Coercion

On peut  séparer les  opérateurs en  3 catégories, en  fonction des  types de
données sur lesquels ils peuvent travailler:

   - nombre
   - chaîne
   - chaîne et nombre

Pour chacune de ces catégories, une coercition peut avoir lieue:

    ┌───────────┬────────────────────┬──────────────────┬─────────────────┐
    │ opérateur │  opérande attendu  │ opérande reçu    │   coercition    │
    ├───────────┼────────────────────┼──────────────────┼─────────────────┤
    │   +-*/%^  │      nombre        │      chaîne      │ chaîne → nombre │
    ├───────────┼────────────────────┼──────────────────┼─────────────────┤
    │   concat  │      chaîne        │      nombre      │ nombre → chaîne │
    ├───────────┼────────────────────┼──────────────────┼─────────────────┤
    │    ~ !~   │      chaîne        │      nombre      │ nombre → chaîne │
    ├───────────┼────────────────────┼──────────────────┼─────────────────┤
    │ ==  !=    │      chaîne        │      nombre      │ nombre → chaîne │
    │ < > >= <= │                    │                  │                 │
    ├───────────┼────────────────────┼──────────────────┼─────────────────┤
    │ ==  !=    │      nombre        │      chaîne      │ nombre → chaîne │
    │ < > >= <= │                    │                  │                 │
    └───────────┴────────────────────┴──────────────────┴─────────────────┘

Ex1:

    $ awk '{ print $1 $2, $3 + 123 }' <<<'123 foo bar'
    123foo 123~

Dans cet exemple, le premier champ est un  nb converti en chaîne, et le 3e champ
est une chaîne convertie en nb.

Ex2:

    # Why using `089` instead of `0123`?
    # To be sure the number is not parsed as octal, and some unexpected
    # conversion alters the test.
    $ awk '{ print $1 == "89" }' <<<'089'
    0~

Dans cet exemple, le 1er champ est un nb converti en chaîne.

Conclusion:

Awk  est  cool,  et  il  convertira  si  besoin  un  nombre  en  une  chaîne  et
réciproquement.

Mais un pb se  pose qd on passe un nombre et une  chaîne à un opérateur binaire,
*et* qu'il peut travailler à la fois sur des nombres et des chaînes.

Awk  doit alors  choisir  quelle  coercition réaliser:  il  choisit toujours  de
convertir le nombre en chaîne.
Contrairement à Vim:

    $ awk '$1 == "089" { print "match!" }' <<<'89'
    ''~

    $ awk '$1 == "089" { print "match!" }' <<<'089'
    match!~

    :echo "89" == 089
    1~

En cas d'ambiguïté, awk donne la priorité aux chaînes, Vim aux nombres.

---

    $ awk '$1 == 042 { print "match!" }' <<<'042'
    ''~

    $ awk '$1 == 142 { print "match!" }' <<<'142'
    match!~

    $ awk '$1 == 0428 { print "match!" }' <<<'0428'
    match!~

Dans du code (!= input), awk interprète `042` comme un nb octal.

---

Qd awk doit convertir une chaîne en nb, il le fait comme Vim.

Rappel, pour Vim:

    :echo 'string'   + 10
    10~
    :echo 'string10' + 10
    10~
    :echo '10string' + 10
    20~

Exception (chaîne commençant par un flottant):

    " VimL
    :echo '10.10' + 10
    20~

    # awk
    $ awk '{ print 10 + $0 }' <<<'10.10string'
    20.1~

---

    string + 0
    number   ""

Force awk à convertir la chaîne `string` en nb et le nb `number` en chaîne.

Pour ce faire, on utilise les opérateurs `+` et implicite (concaténation).
`+0` et ` ""` sont des idiomes permettant de s'assurer qu'une variable a bien le
type désiré.
En jargon anglais, on dit parfois ’cast to int / string’.


Il  est particulièrement  important  de  forcer la  conversion  d'une chaîne  en
nombre, qd elle contient  un nombre qui va être utilisé  comme opérande dans une
comparaison numérique.

Ex:

    var = substr($1, 1, 3)    ✘        var = substr($1, 1, 3)+0    ✔
    if (var < 42)                      if (var < 42)
    print "success!"                   print "success!"

Même si le  1er champ est purement  numérique, on sait que  `var` contiendra une
chaîne, car c'est ce que `substr()` retourne toujours.
Ici, `var` contiendra les 3 premiers caractères du 1er champ.

Sans forcer la coercition de `var` en  nombre, `var < 42` comparerait l'ordre de
chaînes, ce qui n'est probablement pas ce qu'on souhaite en général.

---

    $1     == $2
    $1 + 0 == $2 + 0
    $1  "" == $2

Compare le contenu des champs 1 et 2, en les traitant comme des:

   - nombres ou chaînes, en fonction du type de contenu stocké dans $1 et $2:
     comparaison numérique si les 2 champs sont des nombres, comparaison de
     chaînes autrement

   - nombres

   - chaînes


Dans la 3e comparaison, il n'y a pas  besoin de convertir le 2e champ en chaîne,
car il  suffit qu'un  seul des  opérandes soit une  chaîne pour  que l'opérateur
traite les 2 opérandes comme des chaînes.

---

    $1+0 != 0 ? 1/$1 : "undefined"

Exemple d'expression conditionnelle.
Elle inverse  le 1er champ  numérique s'il est non  nul, autrement elle  vaut la
chaîne "undefined".


Pourquoi `$1+0` et pas simplement `$1` ?
Pour forcer la coercition de `$1` en nb, au cas où ce serait une chaîne.

Explication:

Supposons qu'on écrive `$1 != 0` et que le 1er champ soit "hello".
Voici ce qu'il va se passer:

   1. `!=` convertit le nb `0` en chaîne "0" (règle)

   2. `!=` compare "hello" à "0"

   3. la comparaison échoue

   4. awk évalue 1/"hello"

   5. `/` convertit "hello" en `0`

   6. `/` tente de calculer `1/0`    →    erreur

`!=` et `/` sont tous deux des opérateurs binaires et reçoivent une chaîne et un
nb.
`!=` convertit un nb en chaîne, mais `/` convertit une chaîne en nb.

Pk ne réalisent-ils pas la même coercition?
Car `/` ne travaille que sur des nb,  tandis que `!=` peut travailler sur des nb
ou des chaînes.

---

    print ("11" < 12)
    1~
    print ("1a" < 12)
    0~

Retournent resp. 1 (vrai) et 0 (faux).

Car 12 est converti en "12" *et*  sur ma machine, les lettres sont rangées après
les chiffres donc "a" > "2".


Illustre qu'un  opérateur relationnel  d'infériorité ou de  supériorité, opérant
sur  des chaînes,  teste l'ordre  alphabétique  dans lequel  les opérandes  sont
rangés; l'ordre dépend de la machine.

Montre aussi qu'une expression incluant un opérateur relationnel retourne tjrs 1
ou 0, selon que la relation est vraie ou fausse.

---

    $1 < 0 { print "abs($1) = " -$1 }      ✘
    $1 < 0 { print "abs($1) = " (-$1) }    ✔
    $1 < 0 { print "abs($1) = ", -$1 }     ✔

L'objectif, ici, est  d'afficher la chaîne "abs($1) = "  puis l'opposé numérique
du 1er champ.

La 1e règle pattern-action échoue, les 2 suivantes réussissent.
Illustre que l'opérateur `-` peut provoquer une coercition indésirable.

Explication:

    $1 < 0 { print "abs($1) = " -$1 }      ✘
    │
    └ l'opérateur `-` voit une chaîne et un nb,
    donc il convertit la chaîne en nb

    $1 < 0 { print "abs($1) = " (-$1) }    ✔
    │ │
    │ └ l'opérateur `-` voit juste un nb
    └ l'opérateur de concaténation voit une chaîne et un nb
    donc il convertit le nb en chaîne
    Dans l'ordre, le parser d'awk traite:    () > - > concaténation

    $1 < 0 { print "abs($1) = ", -$1 }     ✔
    │
    └ affiche une chaîne puis un nb

##
# What's the difference between an awk program and an awk utility?

An awk program is the code you write in an `.awk` file.
An awk utility is a binary you run from the command-line (like `/usr/local/bin/gawk`).

##
# Install
## Where is the procedure documented?

    $ vim README.git

## How to install the latest version of gawk?
### Clone the repo

    $ git clone git://git.savannah.gnu.org/gawk.git

### Clean a possible previous compilation

    $ make distclean

### Configure, compile and check the compilation

    # `--enable-mpfr` allows you to use the `-M` command-line option
    $ ./bootstrap.sh &&
      ./configure --enable-mpfr &&
      make &&
      make check

For more  information, read the  `README.git` file (and maybe  the `./configure`
file for some obscure configuration option).

Also, have a look at how the Ubuntu devs compile the gawk package:
<https://launchpad.net/ubuntu/+source/gawk>

click on the button below `Latest upload:`:
<https://launchpad.net/ubuntu/+source/gawk/1:4.2.1+dfsg-1build1>

click on the `amd64` button in the section `Builds`:
<https://launchpad.net/ubuntu/+source/gawk/1:4.2.1+dfsg-1build1/+build/16316647>

click on the `buildlog` button:
<https://launchpadlibrarian.net/407977665/buildlog_ubuntu-disco-amd64.gawk_1%3A4.2.1+dfsg-1build1_BUILDING.txt.gz>

You can even grep the buildlog directly from the shell:

    $ curl -s <build_log_url> | gunzip - | grep ./configure

### Note the version

    $ git describe --tags
    gawk-4.2.1-722-g7081~
         ^^^^^^^^^

Including the patch number.

### Install

    $ sudo checkinstall

Use the previously noted version to fill in the version (`3: Version`):

    9:4.2.1-722~
    ^^

Don't forget to use  an epoch which is higher than the one  used in your default
repository; otherwise, your gawk package may be removed after a system update.

---

You may lose the ability to run the `awk` command (`gawk` will work though).
If that happens, you'll have to play with `update-alternatives`:

    $ sudo update-alternatives --install /usr/bin/awk awk /usr/local/bin/gawk 60 \
      --slave /usr/share/man/man1/awk.1.gz awk.1.gz /usr/local/share/man/man1/gawk.1.gz
    $ sudo update-alternatives --set awk /usr/local/bin/gawk

The `--slave` is there so that `$ man awk` opens the `gawk` manpage.

##
## How to install the latest stable release of gawk?
### Download it from:

<https://ftp.gnu.org/gnu/gawk/>

### Check its authenticity

Download the associated signature, and run gpg to check it:

    $ gpg gawk-4.2.1.tar.xz.sig

If the output contains:

    gpg: Can't check signature: No public key

Note the ID of the public key which was used to sign the archive:

    gpg: assuming signed data in `gawk-4.2.1.tar.xz'
    gpg: Signature made Sun 25 Feb 2018 08:03:55 PM CET using RSA key ID 937EC0D2
                                                                         ^^^^^^^^

Then, import it:

    $ gpg --keyserver hkp://keys.gnupg.net --recv-keys 937EC0D2

If the command fails, try another keyserver:

    $ gpg --keyserver x-hkp://pool.sks-keyservers.net --recv-keys 937EC0D2

In the end, the output should look like this:

    $ gpg --keyserver x-hkp://pool.sks-keyservers.net --recv-keys 937EC0D2
    gpg: requesting key 937EC0D2 from hkp server pool.sks-keyservers.net
    gpg: key 937EC0D2: public key "Arnold Robbins <arnold@skeeve.com>" imported
    gpg: Total number processed: 1
    gpg:               imported: 1  (RSA: 1)

Re-run gpg:

    $ gpg gawk-4.2.1.tar.xz.sig

The output should now contain something like:

    gpg: Good signature from "Arnold Robbins <arnold@skeeve.com>"

### Extract the archive and cd into the project

    $ xt gawk-4.2.1.tar.xz

### Configure

    $ sh ./configure

### Compile

    $ make

### Install

    $ sudo checkinstall

##
# Command-line
## How to run an awk program from a file?  (3)

Use the `-f` (fetch) option:

    $ awk -f progfile input_files ...
          ├─────────┘
          └ `progfile` must contain your awk program

Use a shell script:

    $ cat <<'EOF' >~/bin/sh.sh
    #!/bin/bash
    awk '
    ...
    ' "$@"
    EOF

    $ chmod +x ~/bin/sh.sh

    $ sh.sh input_files ...

Use an awk script:

    $ cat <<'EOF' >~/bin/awk.awk
    #!/usr/bin/awk -f
    ...
    EOF

    $ chmod +x ~/bin/awk.awk

    $ awk.awk input_files ...

The  shebang  tells  the  shell  how  to  run  the  script,  so  when  it  reads
`#!/usr/bin/awk -f`, it runs the script with the command:

    /usr/bin/awk -f /path/to/script.awk input_files ...

---

In the shell script, you need to quote  `$@` to prevent the shell from using the
split+glob operator after the expansion (`$@` → `$1 $2 ...`):

    $ cat <<'EOF' >/tmp/sh.sh
    #!/bin/bash
    awk '
    BEGIN {
    for (i in ARGV)
      print ARGV[i]
    }
    ' $@
    EOF

    $ chmod +x /tmp/sh.sh

    $ /tmp/sh.sh file1 'file 2'
    awk~
    file1~
    file~
    2~

### What's the benefit of `awk -f progfile` compared to the other ways?

`progfile` doesn't need to be executable (no `$ chmod +x` required).

### Which version should I choose?

Use an awk script.

It's better than `$ awk -f`, because you  don't have to type `awk -f` every time
you need to run your script.

It's better than a shell script, because with the latter, all the code is inside
a string, which prevents the awk code from being correctly syntax highlighted.
Besides, your code couldn't easily include a single quote:

    awk '
    BEGIN {
    for (i in ARGV)
      print ARGV[i]
    # Here's a comment    ✘ the single quote ends prematurely the program
    }
    ' "$@"

##
## How to start awk interactively?

Don't provide an input:

    $ rawk '...'
      │
      └ custom shell alias expanding to `rlwrap awk`

Example:

    $ awk '$1 ~ /x/'

Anything you type will be printed back if it contains the character `x`.

### When is the interactive mode useful?

When you need to test a simple piece of code, and see how it reacts to different
inputs:

   1. write the code
   2. write some arbitrary input
   3. watch the output
   4. repeat steps 2 and 3 as many times as you want

### How to exit?

Press <kbd>C-d</kbd>.

This sends the end-of-file signal to the awk foreground process.

##
## I'm writing some example and don't need any real input.  What should I write for the input?

`<<<''` or `/dev/null`.

### When?  Why?

You always need it, otherwise awk would start in interactive mode.

But you don't need  it if the code contains an error; awk  won't wait for you to
type some input, and will raise the error immediately.
You also don't need it if the code contains only the pattern `BEGIN`:

    # the shell prompt reappears immediately
    $ awk 'BEGIN { print }'

    # awk stays in interactive mode
    $ awk 'END { print }'

##
# Syntax
## Why do I have to
### surround an awk program with single quotes?

To be able to write code on several lines.

To protect special characters from being interpreted by the shell.
Like `$` and `SPC` (any shell), or `{` and `}` (only in zsh).

    $ awk '$3 == 0 { print $1 }' /tmp/emp.data

Without  the single  quotes,  you  would have  to  manually  quote each  special
character, which is error-prone:

    $ awk \$3\ ==\ 0\ \{\ print\ \$1\ \} /tmp/emp.data

### surround an action with curly braces?

Because you can omit the pattern or the action.
And if  you *do* omit one  of them, awk must  be able to tell  whether your rule
contains only a pattern  or an action; the curly braces tell  awk that you wrote
an action.

### write the opening curly bracket of an action on the same line as the pattern?

Without a  curly bracket,  awk would  automatically assume  that the  pattern is
bound to the default action `{ print }`:

    pattern
    ⇔
    pattern { print }

So, you can write either of these:

    pattern { action }
    ⇔
    pattern {
        action
    }

But *not* this:

    pattern
    {
        action
    }

###
## If I omit
### a pattern, which one is used?

A pattern matching all the records, such as:

    1

`1` is a true condition no matter the record, because it's a non-zero number.

Example:

    $ awk '1' /tmp/emp.data

This will output the file as is.

### an action, which one is used?

    { print }

##
## In an awk program, can a string
### be surrounded by single quotes?

No, it's a syntax error.

    $ cat <<'EOF' >/tmp/awk.awk
    { printf '%d', 1 }
    #        ^  ^
    #        ✘  ✘
    EOF

    $ awk -f /tmp/awk.awk <<<''
    awk: /tmp/awk.awk:1: { printf '%d', 1 }~
    awk: /tmp/awk.awk:1:          ^ invalid char ''' in expression~
    awk: /tmp/awk.awk:1: { printf '%d', 1 }~
    awk: /tmp/awk.awk:1:          ^ syntax error~

---

    $ cat <<'EOF' >/tmp/awk.awk
    { printf "%s", 'word' }
    #              ^    ^
    #              ✘    ✘
    EOF

    $ awk -f /tmp/awk.awk <<<''
    awk: /tmp/awk.awk:1: { printf "%s", 'word' }~
    awk: /tmp/awk.awk:1:                ^ invalid char ''' in expression~
    awk: /tmp/awk.awk:1: { printf "%s", 'word' }~
    awk: /tmp/awk.awk:1:                ^ syntax error~

---

    $ cat <<'EOF' >/tmp/awk.awk
    { printf "%s ", "word" }
    EOF

    $ awk -f /tmp/awk.awk <<<''
    word~

### contains single quotes?

Yes, as many as you want.

    $ cat <<'EOF' >/tmp/file
    foo
    bar
    baz
    EOF

    $ cat <<'EOF' >/tmp/awk.awk
    { printf "%s   ", "a'''b" }
    #                   ^^^
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    a'''b   a'''b   a'''b   ~

###
## What are the three possible forms of number that awk is able to recognize?

Integer:

   * 1
   * +1
   * -1

Decimal Fraction:

   * 1.2
   * +1.2
   * -1.2

Scientific Notation:

   * 1.2e3
   * 1.2E3
   * 1.2e+3
   * 1.2E+3
   * 1.2e-3
   * 1.2E-3

It's  not  the  [normalized][1]  scientific  notation, because  you  can  use  a
[significand][2] bigger than 10.

    $ awk '{ print $1 + 1 }' <<<'1220e-1'
    123~

But it's still a scientific notation.

### How does awk store any of them internally?

As a float (the precision of which is machine dependent).

    $ awk '$1 == $2' <<<'123 123.0'
    123 123.0~

    $ awk '$1 == $2' <<<'123.0 1.23e2'
    123.0 1.23e2~

The fact that awk prints back the input  line means that the test `$1 == $2` has
succeeded; which means that the first  and second fields are identical, and that
the two numbers are considered to be equal.

##
## How can `print $0` be simplified?

    print

---

By default, `print` uses `$0` as an argument; so you can omit `$0`.

## How can the following assignment be simplified?

    test = var == 123 ? 1 : 0

↣
    test = var == 123
↢

### Why is it possible?

A comparison is an expression, whose value is `1` when true, `0` otherwise.
As such, it can be used (alone) in the rhs of an assignment.

    $ awk '{ var = 123 ; test = var == 123; print test }' <<<''
    1~

##
## What happens if I refer to a non-existent
### variable?

Awk automatically initializes it with the value `""`.
If the variable is used in an arithmetic computation, it's then coerced
into `0`.

### array element?

Awk automatically adds the necessary key in the array and associates it to the value `""`.

    $ cat <<'EOF' >/tmp/awk.awk
    { print a[2] }
    EOF

    $ awk -f /tmp/awk.awk <<<''
    ''~

In contrast,  in VimL,  you would first  need to  add the key  in the  array, or
declare the array with the right size if it's a list:

    :let a = repeat([''], 3)
    :echo a[2]
    ''~

##
## How to refer to a field whose index is stored in a variable?

Use the `$` operator in `$var`.

    $ cat <<'EOF' >/tmp/file
    THE quick brown
    fox JUMPS over
    the lazy DOG
    EOF

    $ awk '{ var++; print $var }' /tmp/file
    THE~
    JUMPS~
    DOG~

This command prints the  first, second and third field of  the first, second and
third record.

##
## When can an assignment be merged with another statement?

When this other statement includes an expression.

    $ awk '{ print (n = 2) + 1, n }' <<<''
    3 2~

    $ awk '{ if ((n = length($1)) > 2) print "has", n, "characters" }' <<<'hello'
    has 5 characters~

### How is it possible?

For awk, an  assignment is an expression  – with the side-effect  of assigning a
value to a variable.

---

Wait a minute...
So, an assignment is both an expression *and* a statement at the same time?

Theory: An assignment or a function is just an expression, not a statement.
However, they can be written alone on a line; in this case, it's syntactic sugar
for a command which evaluates the expression.

##
## How to put several rules on the same line?

Separate them with semicolons.

    rule1; rule2

## How to put several statements in an action on the same line?

Separate them with semicolons.

    pattern { statement1; statement2 }

##
## Where can I break a single statement (or expression) (S) with a newline
### (S) not being a control flow statement?  (4)

After a logical operator:

    1 &&
    2

    3 ||
    4

After `?` or `:`:

    1 ?
    2 :
    3

After a comma:

    print $1,
          $2

After an arbitrarily placed backslash:

    print \
          $1,
          $2

---

All these kinds of locations can be mixed in a single statement:

    printf(\
        "%10s %6s %5s   %s",
        "COUNTRY",
        "AREA",
        "POP",
        "CONTINENT\n\n"\
        )

Here, some newlines are placed after a backslash, others after an argument and a comma.

### (S) being a control flow statement?  (3)

After `(condition)` or `(initialization; condition; increment)`:

    if (e) s

    ⇔

    if (e)
        s

After the `else` or `else if` keyword:

    if (e) s1; else s2

    ⇔

    if (e) s1
    else s2

    ⇔

    if (e)
        s1
    else
        s2

After each  statement in  the body,  provided that  they're surrounded  by curly
braces (to form a compound statement):

    if (e) { s1; s2 } else s3

    ⇔

    if (e) {
        s1
        s2
    } else
        s3

##
## When do I need to put a semicolon between an `if` and `else` statement?

When you put the `else` statement on a line of the `if` statement:

    if (e) s1; else s2

    if (e)
        s1; else s2

But you don't need a semicolon, if the body of `if` is a compound statement:

    if (e) {
        s1
        s2
    } else
        s3

## How can I increase the readibility of a `print` statement with several arguments?  (2)

Break it down on several lines, and comment each one:

    {
        print \
              $1,    # middle of action
              $2     # after action
    }                # after rule

This shows that you can comment *any* end of line.

##
# Pattern
## What are the five kind of patterns?

   - a special keyword:

      * `BEGIN`
      * `END`

      * `BEGINFILE`
      * `ENDFILE`

   - an expression whose value is a scalar (number or string)

   - a (regex) matching expression:

      * `expr  ~ /pat/`
      * `expr !~ "pat"`

   - a compound expression which combines previous expressions
     with `&&`, `||`, `!`, `()`

   - a range:

      *  expr1 , expr2
      * /pat1/ , /pat2/

### When does each of them match?

`BEGIN` matches before the first record.
`END` matches after the last record.

`BEGINFILE` matches before the first record of every file in the input.
`ENDFILE` matches after the last record of every file in the input.

An expression matches if it evaluates to a non-zero number or a non-null string.
Note that a relational, matching or  compound expression always evaluates to `0`
or `1` depending on whether it's true.

A range matches a set of consecutive records.
The first  record in the  range is any record  matched by the  first expression,
let's call it `R1`.
The last record in the range is the next record after `R1` matched by the second
expression.

##
## What can't I do with `BEGIN` and `END`, but can with other patterns?  (2)

You can't omit the associated action.
You can't combine them with another pattern inside a range:

MWE:

    $ awk '/Susie/,END' <<<''
    awk: cmd. line:1: /Susie/,END~
    awk: cmd. line:1:         ^ syntax error~
    awk: cmd. line:1: END blocks must have an action part~

##
## These expressions are syntactic sugar for what?
### `/pat/`

    $0 ~ /pat/

... which is a particular case of:

    (regular) expr

### `!/pat/`

    $0 !~ /pat/

### `/pat1/,/pat2/`

    $0 ~ /pat1/,$0 ~ /pat2/

... which is a particular case of:

    expr1,expr2

##
## How to select the records
### matching `pat1` and not `pat2`?

    /pat1/ && !/pat2/

This shows that you can combine regexes with logical operators.

### whose first character is `e` or comes after `e`?

Use the pattern `$0 > "e"`.

    $ cat <<'EOF' >/tmp/file
    gh
    ef
    cd
    ij
    ab
    EOF

    $ awk '$0 > "e"' /tmp/file
    gh~
    ef~
    ij~

We didn't  need `>=` (in place  of `>`) because `eX`  – no matter what  `X` is –
always come after `e`.

##
## How is a dot interpreted in the left operand of `~`?  In the right operand?

Resp. as a literal dot and as a metacharacter.

    $ awk '"Hello" ~ "Hel.o"' <<<'match!'
    match!~

    $ awk '"Hel.o" ~ "Hello"' <<<'match!'
    ''~

##
## What's the output of the next command?

    $ cat <<'EOF' >/tmp/file
    foo
    A
    bar
    XXX
    foo
    B
    bar
    EOF

    $ awk '/foo/,/bar/' /tmp/file
↣
    foo
    A
    bar
    foo
    B
    bar

Contrary to a range in Vim, a range in awk can match *several* sets of lines.
This is because awk iterates over *all* the records of the input.
Similarly, when you pass  a simple pattern to awk, it  doesn't stop acting after
the first occurrence; it goes on until the end of the input.
↢

## What happens to a range if a record matches the first expression (`R1`), but no record matches the second one?

The range includes all the records from `R1` until the end of the input.

    $ cat <<'EOF' >/tmp/file
    one
    two
    three
    four
    EOF

    $ awk '/two/,/five/' /tmp/file
    two~
    three~
    four~

##
## Why are the following patterns different?

    $2 >= 4 || $3 >= 20

    $2 >= 4
    $3 >= 20

↣
The two snippets don't contain the same number of rules.

When a record satisfies both conditions, it's printed once in the first snippet,
but twice in the second one.
↢

##
## What are the pro/con of using `"pat"` rather than `/pat/`?

Pro:

You can  break it down into  several substrings, and  join them back to  get the
final regex.

By  saving the  substrings in  variables with  telling names,  you increase  the
readibility and maintainability of your code.

Example:

    BEGIN {
        sign     = "[-+]?"
        decimal  = "[0-9]+[.]?[0-9]*"
        fraction = "[.][0-9]+"
        exponent = "[eE]" sign "[0-9]+"
        number   = "^" sign "(" decimal "|" fraction ")(" exponent ")?$"
    }

    $1 ~ number

This code prints the records where the first field is a number.

---

Con:

It is more efficient to use regex constants.
Awk can note  that you have supplied a  regex and store it internally  in a form
that makes pattern matching more efficient.
When  using a  string constant,  awk  must first  convert the  string into  this
internal form and then perform the pattern matching.

Also, with `"pat"`,  you need to double the backslash  for every escape sequence
which you want to send to the regex engine.

##
# Modifying Fields
## How to get the number of fields on a record?

Use the built-in variable `NF`:

    { print NF }

## What's the difference between `NF` and `$NF`?

`NF` is evaluated into the *index* of the last field.
`$NF` is evaluated into the *contents* of the last field.

## How to get the contents of the last but one field?

    { print $(NF-1) }

`NF-1` is an expression evaluated into the  index of the last but one field, and
`$` is an operator converting a field index into a field contents.

---

You  need to  surround  the  expression with  parentheses,  otherwise `$`  would
consider  that  `NF` is  its  operand,  instead of  `NF-1`  (`$`  has a  greater
precedence than `-`).

    $ cat <<'EOF' >/tmp/file
    11 22 33
    44 55 66
    77 88 99
    EOF

    $ awk '{ print $(NF-1) }' /tmp/file
    22~
    55~
    88~

    $ awk '{ print $NF-1 }' /tmp/file
    32~
    65~
    98~

Note that if one  of the last fields began with a  non-digit character, it would
be automatically coerced into the number  `0`; and so `$NF-1` would be evaluated
into `-1`.

##
## How to add a new field to a record?

Refer  to the  field whose  index is  `NF +  1`, and  assign to  it the  desired
contents.

    $ awk '{ $(NF + 1) = "baz"; print }' <<<'foo bar'
    foo bar baz~

## What's the side effect of a field modification?

Awk automatically splits  the record into fields to access  the field to modify,
then replaces every `FS` with `OFS` to create the output record.

    $ cat <<'EOF' >/tmp/file
    This_old_house_is_a_great_show.
    I_like_old_things.
    EOF

    $ cat <<'EOF' >/tmp/awk.awk
    BEGIN { FS = "_"; OFS = "|" }
    { $(NF + 1) = ""; print }
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    This|old|house|is|a|great|show.|~
    I|like|old|things.|~
                      ^
                      separates the previous field (`things.`)
                      from the new last empty field

## What happens if I assign a value to a non-existent field (index bigger than the last one)?

Awk will create as many empty fields as necessary to allow this new field to exist.

Ex:

    $ cat <<'EOF' >/tmp/file
    This_old_house_is_a_great_show.
    I_like_old_things.
    EOF

    $ cat <<'EOF' >/tmp/awk.awk
    BEGIN { FS = "_"; OFS = "|" }
    { $(NF + 3) = ""; print }
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    This|old|house|is|a|great|show.|||~
    I|like|old|things.|||~
                      ^^^
                      there are 3 new empty fields at the end

## How to print the input records, reversing the order of their fields?

    $ cat <<'EOF' >/tmp/file
    3 2 1
    6 5 4
    9 8 7
    EOF

    $ cat <<'EOF' >/tmp/awk.awk
    {
        for (i = NF; i > 0; i--)
            printf "%s ", $i
        print ""
    }
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    1 2 3 ~
    4 5 6 ~
    7 8 9 ~

The purpose of `print ""` is to add a newline at the end of a record.

##
# Printing
## How to print a newline
### at the end of an output record?

    print ""

The reason  why you can omit  `\n` is because, at  the end of an  output record,
`print`  automatically adds  the contents  of `ORS`,  whose default  value is  a
newline.

> print expr-list      Print expressions.  Each expression is  separated
>                      by the value of OFS.  **The output record is termi‐**
>                      **nated with the value of ORS.**

### anywhere?

    printf("\n")

##
## I have the following file:

    $ cat <<'EOF' >/tmp/emp.data
    Beth    4.00   0
    Dan     3.75   0
    Kathy   4.00   10
    Mark    5.00   20
    Mary    5.50   22
    Susie   4.25   18
    EOF

The three columns contain:

   - the name of employees
   - their pay rate in dollars per hour
   - the number of hours they've worked so far

### How to print
#### the last line?

    $ awk 'END { print $0 }' /tmp/emp.data
    Susie   4.25   18~

gawk preserves the value of `$0` from the last record for use in an END rule.

Some other implementations of awk do not.
Alternatively, you could write:

    $ cat <<'EOF' >/tmp/awk.awk
        { last = $0 }
    END { print last }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

#### the *lines* containing the names of the employees which have not worked?

    $ awk '$3 == 0' /tmp/emp.data
    Beth    4.00   0~
    Dan     3.75   0~

#### the names of all the employees?

    $ awk '{ print $1 }' /tmp/emp.data
    Beth~
    Dan~
    Kathy~
    Mark~
    Mary~
    Susie~

#### the lines prefixed with increasing numbers?

Use the `NR` variable:

    $ awk '{ print NR, $0 }' /tmp/emp.data
    1 Beth    4.00   0~
    2 Dan     3.75   0~
    3 Kathy   4.00   10~
    4 Mark    5.00   20~
    5 Mary    5.50   22~
    6 Susie   4.25   18~

####
#### the names of the employees which have worked more than 0 hours, and their total pay?

    $ awk '$3 > 0 { print $1, $2 * $3 }' /tmp/emp.data
           ├────┘         ├┘  ├─────┘
           │              │   └ print their pay
           │              │
           │              └ print their names
           │
           └ only consider the employees which have worked

    Kathy 40~
    Mark 100~
    Mary 121~
    Susie 76.5~

##### same thing, but adding the text `total pay for` before the name, and `is` before the pay?

    $ awk '$3 > 0 { print "total pay for", $1, "is", $2 * $3 }' /tmp/emp.data
    total pay for Kathy is 40~
    total pay for Mark is 100~
    total pay for Mary is 121~
    total pay for Susie is 76.5~

###### same thing, but aligning the names and the pays?

To get more control over the formatting, you need `printf`:

    $ awk '$3 > 0 { printf "total pay for %-8s is %6.2f\n", $1, $2 * $3 }' /tmp/emp.data
    total pay for Kathy    is  40.00~
    total pay for Mark     is 100.00~
    total pay for Mary     is 121.00~
    total pay for Susie    is  76.50~

###
### How to print and sort the names of the employees in reverse order?

Write the names on a pipe connected to the `sort` command:

    $ awk '{ print $1 | "sort -r" }' /tmp/emp.data
    Susie~
    Mary~
    Mark~
    Kathy~
    Dan~
    Beth~

It seems that the rhs of a pipe  inside an action is not processed like the lhs.
The lhs is executed once for each record matching the pattern.
The rhs is executed once for the whole input.

awk probably closes the pipe only after the last record has been processed.

---

Instead of using a built-in pipe, you could also have used an external one:

    $ awk '{ print $1 }' /tmp/emp.data | sort -r

### How to sort the lines according to the total pay?

    $ awk '{ printf("%6.2f  %s\n", $2 * $3, $0) | "sort -n" }' /tmp/emp.data
      0.00  Beth    4.00   0~
      0.00  Dan     3.75   0~
     40.00  Kathy   4.00   10~
     76.50  Susie   4.25   18~
    100.00  Mark    5.00   20~
    121.00  Mary    5.50   22~

### How to save all records inside a list?

Use `NR` to uniquely index them in an array.

    a[NR] = $0

---

    $ cat <<'EOF' >/tmp/awk.awk
        { a[NR] = $0 }
    END { print a[2] }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data
    Dan     3.75   0~

##
## I have the following file, and the following code:

    $ cat <<'EOF' >/tmp/countries
    USSR	8649	275	Asia
    Canada	3852	25	North America
    China	3705	1032	Asia
    USA	3615	237	North America
    Brazil	3286	134	South America
    India	1267	746	Asia
    Mexico	762	78	North America
    France	211	55	Europe
    Japan	144	120	Asia
    Germany	96	61	Europe
    England	94	56	Europe
    EOF

    $ cat <<'EOF' >/tmp/awk.awk
    BEGIN {
        FS = "\t"
        printf("%10s %6s %5s   %s\n\n", "COUNTRY", "AREA", "POP", "CONTINENT")
    }
    {
        TotalArea += $2
        TotalPop += $3
        printf("%10s %6d %5d   %s\n", $1, $2, $3, $4)
    }
    END { printf("\n%10s %6d %5d\n", "TOTAL", TotalArea, TotalPop) }
    EOF

    $ awk -f /tmp/awk.awk /tmp/countries
    COUNTRY   AREA   POP   CONTINENT~

       USSR   8649   275   Asia~
     Canada   3852    25   North America~
      China   3705  1032   Asia~
        USA   3615   237   North America~
     Brazil   3286   134   South America~
      India   1267   746   Asia~
     Mexico    762    78   North America~
     France    211    55   Europe~
      Japan    144   120   Asia~
    Germany     96    61   Europe~
    England     94    56   Europe~

      TOTAL  25681  2819~

### Why do the `printf` statements use `%10s`, `%6d`, `%5d` and `%s` with these particular widths?

The code  wants to  separate the  headings with  the same  number of  spaces; it
chooses 3.

The `COUNTRY`  heading contains 7 characters,  and the code decides  to not only
put 3 spaces between 2 headings, but also before the first heading.

    7+3 = 10

That's where the `%10s` come from.

The `AREA` heading contains `4` characters:

    4 + 3 - 1 = 6
          ├─┘
          └ there's already a space between the first `%s` and `%d` items

That's where the `%6d` come from.

The `POP` heading contains `3` characters:

    3 + 3 - 1 = 5

That's where the `%5d` come from.

The `CONTINENT` heading is  the last one, so we don't need to  make sure each of
its fields ends in the same column, and so there's no need to give it any width.
That's why the last `%s` has no width.

---

Note that the code  works because there's no field whose  length is greater than
the chosen item width.
For example, if there was a country  whose area occupied more than 6 characters,
the alignment would be broken.

##
# Built-in Variables
## What's the value of `NR` in
### a `BEGIN` rule?

0

### a rule matching the last record?

The index of the last record.

E.g., if the input  contains `123` records, in a rule  matching the last record,
the value of `NR` is `123`.

### an `END` rule?

Again, the index of the last record.

##
# Functions
## What happens if I call a function with less values than parameters in its signature?

The missing parameters are initialized with `""`.

    $ cat <<'EOF' >/tmp/awk.awk
    END { myfunc() }
    function myfunc(a) {
        print a
    }
    EOF

    $ awk -f /tmp/awk.awk <<<''
    ''~

##
## What's the scope of a variable created in a function whose signature contains no parameter?

Global.

    $ cat <<'EOF' >/tmp/awk.awk
    { myfunc(); print var }
    function myfunc() {
        var = "hello"
    }
    EOF

    $ awk -f /tmp/awk.awk <<<''
    hello~

If the `var` assignment was local to `myfunc()`, `print var` would print a null string.

## How to make a variable local to a function?

Include it inside the parameters of the function signature.

    $ cat <<'EOF' >/tmp/awk.awk
    BEGIN {
        a[1] = "one"
        a[2] = "two"
        reverse(a)
    }
    END { print temp }
    function reverse(x,    temp) {
        temp = x[1]
        x[1] = x[2]
        x[2] = temp
    }
    EOF

    $ awk -f /tmp/awk.awk <<<''
    ''~

The purpose of `reverse()` is to reverse  the order of the first two elements of
an array; to do so, it needs a temporary variable `temp`.

Inside the function, `temp` contains `"one"`, but outside it contains a null string.
By including it  inside the parameters of the function  signature, we've made it
local to the function.

Note  that, since  there's no  need to  pass a  value to  initialize `temp`,  in
effect, `temp` is an optional parameter of `reverse()`.
In contrast, `x` is mandatory; you need to tell `reverse()` which array you want
to reverse.

### What are the two common conventions to follow when doing so?

Group the  mandatory parameters  at the  start of the  parameters list,  and the
optional local parameters at the end.

Separate the two groups with several spaces.

                     ┌ mandatory parameters
                     │     ┌ optional parameters
                     │     ├──┐
    function reverse(x,    temp) {
                       ^^^^
                       multi-space separation between the two groups of parameters

##
## What are the outputs of the next snippets?

    $ cat <<'EOF' >/tmp/awk.awk
    END {
        a = "foo"
        myfunc(a)
        print a
    }
    function myfunc(a) {
        a = a 42
    }
    EOF

    $ awk -f /tmp/awk.awk <<<''
↣
    foo

`myfunc()` has not modified the global variable `a`.
↢

    $ cat <<'EOF' >/tmp/awk.awk
    END {
        b[1] = "foo"
        myfunc(b)
        print b[1]
    }
    function myfunc(b) {
        b[1] = b[1] 42
    }
    EOF

    $ awk -f /tmp/awk.awk <<<''
↣
    foo42

`myfunc()` *has* modified the first element of `b`.
↢

### Why are they different?

Awk passes scalars by value, and arrays by reference.

##
## How to get the number of characters in
### a string?

Use the `length()` function:

    length(s)

---

    $ awk '{ print length($1) }' <<<'a bc'
    1~

### the current record?

Use `length()`, but without any argument.

---

    $ awk '{ print length() }' <<<'a bc'
    4~

##
# Operators
## How are consecutive operators of equal precedence grouped?

Most operators are *left*-associative:

    7-4+2
    ⇔
    (7-4)+2
     ├─┘
     └ 7 and 4 are grouped first (not 4 and 2)

except for the assignment, conditional,  and exponentiation operators, which are
*right*-associative.

Example:

    $ awk '{ print 2^3^4 }' <<<''
    2417851639229258349412352~

Here, we can see that:

    2 ^ 3 ^ 4
    ⇔
    2 ^ (3 ^ 4)
    ⇔
    2 ^ 81

If `^` was left-associative:

    2 ^ 3 ^ 4
    ⇔
    (2 ^ 3) ^ 4
    ⇔
    8 ^ 4
    ⇔
    4096

## What does grouping allow me to change?

The precedence of an arbitrary operator.

##
## Which mnemonic device can I use to remember the operators in decreasing order of precedence?

GRI ELMACR RAL LTA

### What are they?

    ┌─────────────────────────┬──────────────────────────────────────────────┐
    │ ()                      │ Grouping                                     │
    │ $ Field                 │ Reference                                    │
    │ ++ --                   │ Increment, decrement                         │
    │                         │                                              │
    │ ^                       │ Exponentiation                               │
    │ !+-                     │ Logical “not”, unary plus, unary minus       │
    │ */%                     │ Multiplication, division, modulo (remainder) │
    │ +-                      │ Addition, subtraction                        │
    │                         │ Concatenation                                │
    │ < <= == != > >= >> | |& │ Relational and redirection                   │
    │                         │                                              │
    │ ~ !~                    │ Regex (non)matching                          │
    │ in                      │ Array membership                             │
    │ &&                      │ Logical “and”                                │
    │                         │                                              │
    │ ||                      │ Logical “or”                                 │
    │ ?:                      │ Ternary conditional                          │
    │ = += -= *= /= %= ^=     │ Assignment                                   │
    └─────────────────────────┴──────────────────────────────────────────────┘

## Which mnemonic device can I use to remember the *regex* operators in decreasing order of precedence?

GQPSC ANCA EB E

### What are they?

    ┌────────┬─────────────────────────────────┐
    │ ()     │ Grouping + capture              │
    │ ?      │ Question mark                   │
    │ +      │ Plus                            │
    │ *      │ Star                            │
    │        │ Concatenation                   │
    │        │                                 │
    │ |      │ Alternation                     │
    │ [^abc] │ Complemented bracket expression │
    │ [abc]  │ Bracket Expression              │
    │ .      │ Any character                   │
    │        │                                 │
    │ $      │ End of string                   │
    │ ^      │ Beginning of string             │
    │        │                                 │
    │ \c     │ Escape sequence                 │
    └────────┴─────────────────────────────────┘

The order was found in the book `The AWK Programming Language`, appendix A, page
191 of the book.

##
## How to simplify multiple assignments, all of which have the same rhs?

    var1 = val
    var2 = val

    ⇔

    var1 = var2 = val

### Why does this work?

Because an assignment is an expression:

           ┌ expression returning `val`, and assigning it to `var2`
           ├────────┐
    var1 = var2 = val
    ├───────────────┘
    └ expression returning `val`, and assigning it to `var1`

and because the assignment operator is *right*-associative:

    var1 = var2 = val
    ⇔
    var1 = (var2 = val)

##
##
##
# Affichage
## Alignement

Il existe 3 méthodes pour aligner la sortie d'awk:

   - utiliser `printf` en donnant une largeur de champ suffisante pour chaque colonne
   - jouer sur les variables `FS` et/ou `OFS`
   - pipe la sortie d'awk vers `column`


    BEGIN {      OFS = "\t" }
    BEGIN { FS = OFS = "\t" }

Préserve l'alignement des champs de l'input qd ils sont séparés par des:

   - espaces
   - tabs

En  effet, modifier  un champ  peut  changer sa  largeur, et  donc faire  perdre
l'alignement d'une colonne.
En ajoutant un tab après chaque champ, on restaure l'alignement.


Explication:

Qd on ne modifie pas le contenu d'un record, awk le produit tel quel.
En revanche,  si on modifie directement  le contenu d'un champ  dont l'index est
non nul, awk effectue le remplacement `FS` → `OFS`, sur son record.

En clair, par défaut,  awk remplace chaque séquence d'espaces et  de tabs par un
espace.
Si  on a  utilisé des  tabs pour  aligner des  colonnes au  sein d'un  texte, ce
remplacement peut ruiner l'alignement.

Avec la  2e commande  précédente, awk  ne supprimera  que les  tabs (car  `FS` =
"\t"), qu'il remplacera par des tabs (car `OFS` = "\t").

Update: Playing with `FS` and `OFS` doesn't  seem reliable enough if you've used
several tabs to align some fields.

        $ cat <<'EOF' >/tmp/emp.data
        Beth			4.00	0
        Dan			3.75	0
        KathySomeVeryLongName	4.00	10
        Mark			5.00	20
        Mary			5.50	22
        Susie			4.25	18
        EOF

        $ awk 'BEGIN { FS = "\t+"; OFS = "\t" }; { $3 = "foo"; print }' /tmp/emp.data
        Beth	4.00	foo~
        Dan	3.75	foo~
        KathySomeVeryLongName	4.00	foo~
        Mark	5.00	foo~
        Mary	5.50	foo~
        Susie	4.25	foo~

Note that playing with `FS` and `OFS` is still useful to preserve some alignment:

        $ awk '{ $3 = "foo"; print }' /tmp/emp.data
        Beth 4.00 foo~
        Dan 3.75 foo~
        KathySomeVeryLongName 4.00 foo~
        Mark 5.00 foo~
        Mary 5.50 foo~
        Susie 4.25 foo~

But it's not always perfect.

---

    $ awk ... | column -t [-s:]

Aligne les colonnes de texte de la sortie d'awk.
Par  défaut, l'espace  est  utilisé comme  séparateur entre  2  champs (`-s:`  =
utiliser le double-point à la place)

Commande pratique si awk a transformé du texte et perdu l'alignement des champs.

L'avantage par rapport  aux règles awk précédentes (`BEGIN` ...),  est qu'on n'a
pas besoin de se soucier de savoir  comment l'input d'awk était alignée, ni même
si elle était alignée.

## Précision numérique

When a float is printed, it's formatted according to the format specifier `OFMT`
(no coercion number → string) or `CONVFMT` (coercion).

But when an integer  is printed, it remains an integer, no  matter the values of
`OFMT` and `CONVFMT`:

    $ awk '{ OFMT = CONVFMT = "%.2f"; print 1E2 }' <<<''
    100~

    $ awk '{ OFMT = CONVFMT = "%.2f"; print 1E2 "" }' <<<''
    100~



    { printf "%.6g", 12E-2 }
    0.12~
    { printf "%.6g", 123.456789 }
    123.457~

Il  semble  que les  spécificateurs  de  conversion  `%e`,  `%f`, et  `%g`  sont
identiques entre les fonctions `printf()` de Vim et awk, à deux exceptions près.

Le `%g` du `printf()` d'awk supprime les 0 non significatifs, *et* il interprète
la précision comme le nb de chiffres significatifs.

Celui de Vim ne supprime pas les 0 non significatifs, et interprète la précision
comme le nb de chiffres après la virgule:

    :echo printf("%.6g", 12*pow(10,-2))
    0.120000~
    :echo printf("%.6g", 123.456789)
    123.456789~

---

    BEGIN { var = 1.23456789 }
    END {
        OFMT = "%.2f"
        print (var > 1.234)
    }

Il  faut des  parenthèses autour  de  `var >  1.234`  pour éviter  que `>`  soit
interprété comme une redirection.

Les  parenthèses  forcent  awk  à  évaluer  l'expression  `var  >  1.234`  avant
d'exécuter   `print`  Sans   elles,  awk   exécuterait  d'abord   `print`,  puis
redirigerait la sortie le fichier `1.234`.


L'expression `var > 1.234` retourne `1`  (réussite), ce qui signifie que `var` a
été formatée *après* l'évaluation de `var > 1.234`:

    1.23456789 > 1.234 ✔
    1.23       > 1.234 ✘

... mais *avant* d'afficher le résultat:

    print (var - 1.234)
    0.00 (au lieu de 0.00056789)~

Conclusion: qd  une expression  arithmétique est  affichée, elle  n'est formatée
qu'après son évaluation.

## Print(f)

    Syntaxes des fonctions `print()`, `close()` et `system()`:

    ┌──────────────────────────┬──────────────────────────────────────────────────────────┐
    │ print e1, e2, ...        │ concatène les valeurs des expressions                    │
    │                          │ en incluant OFS entre elles et ORS à la fin,             │
    │                          │ puis écrit le résultat sur la sortie standard du shell   │
    ├──────────────────────────┼──────────────────────────────────────────────────────────┤
    │ print e1, e2, ... >expr  │ écrit dans le fichier dont le nom est la valeur chaîne   │
    │                          │ de `expr`                                                │
    │                          │                                                          │
    │ print e1, e2, ... >>expr │ mode append                                              │
    ├──────────────────────────┼──────────────────────────────────────────────────────────┤
    │ print e1, e2, ... | expr │ écrit sur l'entrée standard de la commande shell         │
    │                          │ stockée dans la valeur chaîne de `expr`                  │
    ├──────────────────────────┼──────────────────────────────────────────────────────────┤
    │ system(expr)             │ exécute la commande shell stockée dans `expr`            │
    │                          │ et affiche sa sortie                                     │
    │                          │                                                          │
    │                          │ retourne son code de sortie                              │
    ├──────────────────────────┼──────────────────────────────────────────────────────────┤
    │ close(expr)              │ la valeur de `expr` doit être une chaîne dont le contenu │
    │                          │ est un chemin vers un fichier ou une commande shell,     │
    │                          │ ayant servi dans une redirection (>, |)                  │
    └──────────────────────────┴──────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────┐
    │ printf(fmt, e1, e2, ...)        │
    ├─────────────────────────────────┤
    │ printf(fmt, e1, e2, ...) >expr  │
    │ printf(fmt, e1, e2, ...) >>expr │
    ├─────────────────────────────────┤
    │ printf(fmt, e1, e2, ...) | expr │
    └─────────────────────────────────┘

Les syntaxes de `printf` sont similaires à `print`, à ceci près que:

   - il faut ajouter l'argument `fmt` (chaîne format)
     ce qui donne à `printf` plus de puissance

   - `printf` ne remplace *rien*:
     ni `FS` → `OFS` entre 2 expressions,
     ni `RS` → `ORS` à la fin

Il faut donc en tenir compte.
Pex, si on veut un newline à la fin, il faut l'inclure dans `fmt`:

    printf("...\n", e1, ...)

---

Si  on passe  en argument  à `print`  ou `printf`,  une expression  utilisant un
opérateur relationnel,  il faut entourer  soit l'expression soit toute  la liste
des arguments avec des parenthèses.

En effet, un opérateur relationnnel  pourrait être interprété comme un opérateur
de redirection:

    print 3 > 2     ✘ écrit `3` dans le fichier dont le nom est `2`
    print(3 > 2)    ✔ affiche 1 car la relation est vraie

Avec les parenthèses, `>` ne "voit" pas `print`, et est donc interprété comme un
opérateur relationnel.

---

    print $1, $2
    print $1  $2

Affiche le contenu des champs 1 et 2 en les séparant par:

   - `OFS`
   - rien

Illustre que  l'opérateur de concaténation  (implicite) n'ajoute rien  entre les
expressions.

---

        { names = names $1 " " }
    END { print names }

Affiche tous les noms des employés sur une même ligne.
Montre comment convertir une colonne en ligne.

---

Une suite d'expressions dans  le rhs d'une affectation n'a pas  de sens, awk les
concatène donc en une seule expression.
Il  a le  droit  de le  faire  car l'opérateur  de  concaténation est  implicite
(contrairement à VimL où il est explicite `.`).

Au passage, si l'une des expressions  est un nb, il est automatiquement converti
en chaîne; c'est  logique puisque l'opérateur de concaténation  ne travaille que
sur des chaînes.

---

    { temp = $2; $2 = $1; $1 = temp; print }

Affiche tous les records en inversant les 2 premiers champs.
Le résultat est obtenu en 3 étapes:

   - sauvegarde temporaire du 2e champ dans la variable `temp`
   - duplication du champ 1 dans le champ 2
   - restauration du champ 2 dans le champ 1 via `temp`


On aurait aussi pu utiliser `printf`.
Pex, pour un input ayant 3 champs:

    { printf "%s %s %s\n", $2, $1, $3}


On remarque qu'on peut utiliser `$1` et `$2` à la fois comme:

   - valeur (expression)    normal
   - nom de variable        surprise!

Il semble qu'en awk  comme en VimL (mais pas en bash), il  y a symétrie entre le
lhs et le rhs d'une affectation.

---

    printf "total pay for %-8s is $%6.2f\n", $1, $2*$3
    total pay for Beth     is $  0.00~
    total pay for Dan      is $  0.00~
    total pay for Kathy    is $ 40.00~
    total pay for Mark     is $100.00~
    total pay for Mary     is $121.00~
    total pay for Susie    is $ 76.50~

On peut utiliser la commande `printf` pour formater un record.

Ici, on  utilise les items  `%-8s` et `%6.2f` pour  insérer le nom  des employés
(`$1`), et leur salaire (`$2*$3`) dans la chaîne principale.

Rappel:

   * -8s     champ de taille 8, alignement à gauche
   * 6.2f    champ de taille 6, flottant avec 2 chiffres signifcatifs après la virgule


Si on n'avait  pas donné la largeur `8`  à la colonne des noms,  ou que certains
noms avaient plus  de 8 caractères, alors les colonnes  suivantes n'auraient pas
été alignées.

Donner  une largeur  de champ  suffisante à  la valeur  d'une expression  permet
d'aligner les colonnes des expressions suivantes.

---

    for (i in a)
        print a[i] | "sort -nr >/tmp/file"

Trie le contenu de l'array `a` dans `/tmp/file`.

Illustre qu'on  peut écrire  toute une  boucle d'instructions  sur un  pipe, pas
seulement une simple instruction; similaire au shell.

---

    print message | "cat 1>&2"
    system("echo '" message "' 1>&2")

    print message >"/dev/tty"

Les 2  premières commandes écrivent le  contenu de la variable  `message` sur la
sortie d'erreur du shell.
La 3e écrit sur le terminal.

Ces 3 commandes résument les différents idiomes qu'il est possible d'utiliser qd
on veut écrire sur la sortie d'erreur ou standard du shell.

##
# Calcul

    atan2(0,-1)
    π~
    exp(1)
    𝑒~
    log(42)/log(10)
    logarithme de 42 en base 10~

Illustre comment utiliser  les fonctions arithmétiques de awk  pour exprimer des
constantes célèbres en maths.


La fonction `atan2()` est une variante de la fonction arc tangente.

Quelle différence entre `atan2()` et `arctan()`?

`atan2()`  retourne  des  angles   dans  l'intervalle  ]-π,π],  `arctan()`  dans
]-π/2,π/2].

On remarque que l'intervalle image de `arctan()` est 2 fois plus petit que celui
de `atan2()`.
En effet, pour chaque  nombre réel `y` il existe 2 angles distincts  `x` et `x +
π` ayant pour image `y` via la fonction tangente:

    y = tan(x) = tan(x+π)

Il faut donc que `arctan()` choisisse entre les 2.
Pour lever cette ambigüité, on utilise l'intervalle ]-π/2,π/2].


Quelle différence entre `atan2(y,x)` et `arctan(y/x)`?

Le rapport `y/x` nous fait perdre de l'information: les signes de `x` et `y`.

    arctan(y/x) = arctan(-y/-x)
    atan2(y,x) != atan2(-y,-x)

IOW, si on imagine un point A  de coordonnée `(x,y)`, `arctan()` ne nous donnera
pas forcément son angle (Ox,OA); il se peut qu'elle rajoute/enlève π.
Tandis qu'avec `atan2()`, on aura toujours exactement l'angle (Ox,OA).

---

    int(x + 0.5)

Arrondit le nb décimal positif `x` à l'entier le plus proche.


    $1 > max { max = $1 }
    END      { print max }

Affiche le plus grand nombre de la 1e colonne.


    # ✘
    $ awk '{ print (1.2 == 1.1 + 0.1 ) }' <<<''
    0

    # ✔
    $ awk '{ x = 1.2 - 1.1 - 0.1 ; print (x < 0.001 && x > 0 || x > -0.001 && x < 0) }' <<<''
    1~

Il se  peut que 2  expressions arithmétiques  diffèrent pour awk  alors qu'elles
devraient être identiques.

Le pb vient du fait que la représentation d'un flottant est parfois inexacte.

Cela peut conduire à des erreurs lors d'une comparaison entre 2 expressions dont
les valeurs sont des flottants.

Ou  encore  lors d'un  calcul  en  plusieurs  étapes,  qui fait  intervenir  des
flottants.
Lorsqu'une erreur,  même petite, se propage  d'une étape à une  autre, elle peut
être amplifiée.
Au final, on peut obtenir un résultat très loin de celui désiré.

Pour un exemple, lire ce lien qui contient un algo approximant π:

<https://www.gnu.org/software/gawk/manual/html_node/Errors-accumulate.html#Errors-accumulate>

Pour une comparaison entre flottants, la solution consiste à ne pas les comparer
directement entre  eux, mais plutôt  leur distance  par rapport à  une précision
arbitraire.

---

    # ✔
    $ awk '1e50 == 1.0e50 { print 1 }' <<<''
    1~

    # ✘
    $ awk '1e500 == 1.0e500 { print 1 }' <<<''
    1~

Le problème peut venir de nombres trop grands, pex:

    1e50  == 1.0e50     ✔
    1e500 == 1.0e500    ✘

    1.2 == 1.1 + 0.1 { print }
    ✘ devrait afficher tous les records de l'input mais atm n'affiche rien car la comparaison échoue~

    { print 1.2 - 1.1 - 0.1 }
    retourne -1.38778e-16, mais devrait retourner 0~
    D'où vient cette différence non nulle ???

    On a le même problème dans Vim!
    :echo 1.2 - 1.1 - 0.1
    -1.387779e-16~

    Autre problème:
    :echo 1.3 - 1.1 - 0.1 == 0.1
    0~

    Bottom line:
    Don't make a float comparison in VimL, nor in awk.

    Read the gawk user's guide, chapter 15 to understand what's going on.

##
# Syntaxe
## Arrays

    array

En  informatique,  une array  est  un  ensemble  d'éléments  indexés par  un  ou
plusieurs indices.

Analogie entre informatique et maths:

    ┌─────────────────────────────────────────┬───────────┐
    │ informatique                            │ maths     │
    ├─────────────────────────────────────────┼───────────┤
    │ array indexée par 0 indice              │ constante │
    │ ≈ scalaire                              │           │
    ├─────────────────────────────────────────┼───────────┤
    │ array indexée par un seul indice        │ vecteur   │
    │                                         │           │
    │ liste ou dictionnaire                   │           │
    │ │        │                              │           │
    │ │        └ les index sont des chaînes   │           │
    │ └ les index sont des nbs                │           │
    ├─────────────────────────────────────────┼───────────┤
    │ array indexée par 2 indices             │ matrice   │
    ├─────────────────────────────────────────┼───────────┤
    │ array indexée par n indices             │ tenseur   │
    └─────────────────────────────────────────┴───────────┘


Dans  awk, une  array  est associative,  i.e.  elle peut  être  indexée par  des
chaînes.

Pk le terme "associative"?
Explication:

Une array associative mémorise des associations.

En  programmation,  les  éléments  d'une  liste sont  indexés  par  des  nombres
consécutifs en partant de 0.
Une  liste n'a  besoin de  mémoriser que  ses éléments,  car elle  peut utiliser
l'ordre dans  lequel ils  sont rangés  pour retrouver  n'importe lequel  via son
index.
Elle n'a pas besoin de mémoriser les associations 'indice élément'.

En revanche, dans une array pouvant être indexée par des chaînes, il n'y a aucun
ordre sur lequel s'appuyer.
Il faut donc que les *associations* 'indice - élément' soient mémorisées, et non
pas simplement les éléments.

---

    array[$1] = $2

Crée une array dont  les indices sont les éléments de la  1e colonne de l'input,
et les valeurs associées sont ceux de la 2e colonne.
Ex:

    foo 1
    bar 2    →    array = { 'foo': 1, 'bar': 2, 'baz':3 }
    baz 3


    i = "A"; j = "B"; k = "C"
    array[i, j, k] = "hello, world\n"

Affecte "hello, world\n" à l'élément de `array` indexé par la chaîne:

    "A\034B034C"

Illustre  qu'awk  supporte  les  arrays multi-dimensionnelles,  et  que  lorsque
l'indice est une liste d'expressions,  ces dernières sont converties en chaînes,
et concaténées  en utilisant le  contenu de  la variable interne  `SUBSEP` comme
séparateur.

---

    if (i in a)
        print a[i]

    if ((i,j) in a)
        print a[i,j]

Teste si `a[i]` / `a[i,j]` existe et si c'est le cas, affiche sa valeur.


`i` et `j` peuvent être des variables,  des chaînes ou des nombres (convertis en
chaînes).


`i in a`  est une expression retournant  `1` si l'array `a`  contient un élément
d'indice `i`, `0` autrement.


Dans une expression utilisant l'opérateur `in`, un indice multi-dimensionnel est
entouré de parenthèses (et non de crochets).

---

    if ("Africa" in pop) ...        ✔
    if (pop["Africa"] != "") ...    ✘

Ces 2 `if` testent si l'indice "Africa" est présent dans l'array `pop`.

Le 2e  `if` ajoute  automatiquement à  `pop` l'élément  d'indice "Africa"  et de
valeur "".
Ce n'est pas le cas du 1er `if`, dont la syntaxe est sans doute à préférer.

---

    delete a
    delete a[42]

Supprime tous les éléments de l'array `a` / l'élément d'indice 42.

---

    for (i in a)
        print a[i]

Affiche tous les éléments de l'array `a`.


Si l'array  est multi-dimensionnelle, et qu'à  l'intérieur de la boucle  on veut
accéder  à  chaque  composant  de  l'indice `i`  séparément,  on  peut  utiliser
`split()` et `SUBSEP`:

    split(i, x, SUBSEP)

... les composants sont stockées dans l'array `x`.


Ne pas confondre la construction awk `for  i in array` avec la construction VimL
`for val in list`.

Une array awk se rapproche davantage d'un dictionnaire Vim.
Toutefois, en VimL et contrairement à awk, on ne peut pas itérer directement sur
les clés d'un dictionnaire, à moins de passer par la fonction `items()`:

    for i in items(mydic)
        echo i[0]
    endfor

Résumé:

    ┌──────┬───────────────────────────────────────────────────────────────────┐
    │ VimL │ for val in list:    `val` itère sur les VALEURS au sein de `list` │
    ├──────┼───────────────────────────────────────────────────────────────────┤
    │ awk  │ for i in array:     `i` itère sur les INDICES de `array`          │
    └──────┴───────────────────────────────────────────────────────────────────┘

##
## Control (flow) statements
### if

    if (e1)
        s1
    else if (e2)
        s2
    else
        s3

    ⇔

    if (e1) s1; else if (e2) s2; else s3

---

    if (e1) {
        s1
        s2
    } else if (e2) {
        s3
        s4
    } else {
        s5
        s6
    }

    ⇔

    if (e1)      { s1; s2 }
    else if (e2) { s3; s4 }
    else         { s5; s6 }

Si plusieurs déclarations doivent être exécutées après un des mot-clés suivants:

   - if
   - else if
   - else
   - while
   - for

... il faut les encadrer avec des accolades.
Autrement, s'il n'y en a qu'une, pas besoin d'accolades.

C'est  logique,  car  awk,  contrairement  à  Python,  n'accorde  aucun  sens  à
l'indentation.
Il a donc besoin d'un mécanisme pour savoir  si `s2` fait partie de la boucle ou
non :

    for (e)
    s1
    s2

    ⇔

        for (e)
    s1
        s2

`s2` est hors de la boucle (awk se fiche de l'indentation).

    for (e) {
    s1
    s2
    }

`s2` est dans la boucle (grâce aux accolades)


Exception: pas  besoin d'accolades, si  les déclarations sont contenues  dans un
bloc `if`, `for`, `while` (imbrication).


On remarque  que `else` doit toujours  être précédé d'un point-virgule  ou d'une
accolade fermée.


Omettre  les parenthèses  autour  de l'expression  à tester  est  une erreur  de
syntaxe !!!


    if (0) if (1) print 2; else print 3
    if (1) if (0) print 2; else print 3

N'affiche rien, car les deux `print` sont  au sein du 1er `if` dont l'expression
est fausse (`0`).
Affiche `3`, car l'expression  du 1er `if` est vraie (`1`)  et celle du deuxième
est fausse (`0`).

Illustre qu'un `else` est toujours associé au `if` à sa gauche le plus proche.

### for

    for (var in array)
        s

---

    for (e1; e2; e3)
        s

    ⇔

    e1 ; while (e2) { s; e3 }
    │           │        │
    │           │        └ transformation
    │           └ condition
    └ initialisation

---

    for (e1 ;; e3)

`e2` étant absente (`;;`), elle est considérée comme vraie par défaut.
Ça implique que cette boucle ne finira jamais.

---

    for (i = 1; i <= 5; i++)

    ⇔

    s
    i = 1
      while (i <= 5) {
          s
          i++
      }

Boucle itérant sur les valeurs de la variable `i`, qui vont de 1 à 5.


La 1e syntaxe peut se décomposer de la façon suivante:

    for (i = 1; i <= 5; i++)
    │      │       │
    │      │       └ transformation    à la fin d'une itération
    │      └ condition                 pour rester dans la boucle
    └ initialisation


Dans la boucle `for`, on pourrait remplacer `i++` par `i += 1`.

---

    END {                                       11           11
        for (i = 1; i <=3; i++)                 12           12
            for (j = 1; j <=3; j++) {      →    21    ≠    * 13
                print i j                       22           21
                if (j == 2) break               31           22
            }                                   32         * 23
    }                                                        31
                                                             32
                                                           * 33

Illustre le fonctionnement de la commande `break`.

Au sein d'une:

   - boucle `for`, `while` ou `do`,  elle permet de sortir de cette dernière
   - imbrication de boucles,         "                        la boucle intérieur

Les nombres préfixés d'un astérisque sont ceux que `break` nous faisait manquer.

---

    END {                                     11           11
        for (i = 1; i <=3; i++) {             12           12
            if (i == 2) continue         →    13    ≠      13
            for (j = 1; j <=3; j++)           31         * 21
                print i j                     32         * 22
        }                                     33         * 23
    }                                                      31
                                                           32
                                                           33

Illustre le fonctionnement de la commande `continue`.

Au sein d'une boucle `for`, `while` ou `do`, elle permet de passer directement à
la prochaine itération de cette dernière.


Les commandes `break` et `continue` fonctionnent comme leurs homonymes Vim.

---

    for (i = 1; i <= NF && $i != ""; i++)
        ;
    if (i < NF) print

Affiche tous les records dont un des champs est vide.
Illustre l'utilité de la déclaration vide `;`.

Explication: La boucle  incrémente `i` tant que  le champ de même  index est non
vide; elle ne fait rien d'autre, car elle ne contient que la déclaration vide.

Une fois  sorti de la boucle,  `if` compare `i` à  `NF`: si `i` est  plus petit,
`print` affiche le record.


Un champ vide n'est pas un champ rempli d'espaces.
Un champ vide correspond à 2 `FS` consécutifs (pex 2 Tabs).

### while

    while (e)
        s

    ⇔

    while (e) s

    ⇔

    do
        s
    while (e)

    ⇔

    do s; while (e)

---

    while (e) {
        s1
        s2
    }

    ⇔

    while (e) { s1; s2 }

    ⇔

    do { s1; s2 } while (e)

Si `e` est fausse dès le début, une boucle `while` n'exécutera jamais `s`.
En revanche, une boucle `do` l'exécutera une fois, car `do` vient avant `while`.

### next / exit

    exit
    exit 123

Se rendre directement à la règle `END`.
Idem, en retournant 123 comme code de sortie du programme awk.

Si `exit`  est utilisé au sein  de la règle  `END`, on quitte le  programme awk,
sans terminer de traiter les actions `END`.

---

    next
    nextfile

Arrête  le  traitement du  record  courant,  ignore les  couples  pattern-action
suivants, et passe:

   - au prochain record du fichier courant
   - au 1er      record du prochain fichier de l'input


Qd `nextfile` est utilisé, certaines variables sont mises à jour:

   - `FILENAME`
   - `ARGIND`
   - `FNR`  →  1


`next` provoque une erreur s'il est utilisé dans la règle `BEGIN` ou `END`.
Idem pour `nextfile`.

---

    pattern { statement1; next}
            { statement2 }

Exécute `statement1`  sur les records  où `pattern` matche, et  `statement2` sur
les autres.

Grâce  à  `next`, on  évite  l'exécution  de  `statement2`  sur les  records  où
`pattern` ne matche pas.

### switch

    switch (e) {
    case value:
        statements1
        break

    case regex:
        statements2
        break

    default:
        statements3
        break
    }

L'expression `e` est comparée à `value`.
Si la comparaison réussit, awk exécute `statements1`.

Autrement,  il  compare  `e`  à   l'expression  régulière  `regex`,  et  exécute
`statements2` en cas de succès.

Autrement, il exécute `statements3`.

La commande `default` est facultative.

En l'absence de commandes `break`, awk continue de traiter le bloc `switch`.
IOW, sans `break`, awk exécute autant  de déclarations qu'il y a de comparaisons
qui réussissent.
Si on veut  qu'il n'en exécute qu'une  (la 1e qui réussit), il  faut inclure des
`break` pour sortir du `switch`.

##
## Functions
### close

La  fonction `close()`  permet de  fermer des  fichiers et  pipes ouverts  (i.e.
auxquels le processus awk accède en lecture).
Ça peut être  nécessaire entre autres car l'OS possède  une limite concernant le
nb  de fd  (file descriptors)  ouverts  simultanément, ce  qui limite  le nb  de
fichiers / pipes pouvant être ouverts à un instant T.

---

    $ cat <<'EOF' >/tmp/awk.awk
    BEGIN {
        "date" | getline var1
        print var1
        system("sleep 3")
        close("date")
        "date" | getline var2
        print var2
    }
    EOF

    $ awk -f /tmp/awk.awk <<<''

Affiche l'heure et la date du jour, dort 3s, puis réaffiche l'heure.

Sans l'instruction `close("date")` qui ferme le précédent pipe `"date" | getline var`,
la  2e commande  shell `date`  n'aurait pas  été exécutée,  et `print`  n'aurait
affiché qu'une seule date.

Illustre qu'il faut  fermer un pipe, si on veut  pouvoir le réutiliser plusieurs
fois.

---

    END {
        for (i in a)
            print a[i] | "sort -nr >/tmp/file"

        close("sort -nr >/tmp/file")

        while ((getline <"/tmp/file") > 0) print
    }

Ce code fait 3 choses:

   1. écrit le contenu de l'array `a` sur l'entrée de la commande shell:

          $ sort -nr >/tmp/file

   2. ferme le pipe

   3. lit et affiche le contenu de `/tmp/file`

Pour que la  1e étape se termine,  et que le fichier `/tmp/file`  soit écrit, la
fermeture du pipe via `close()` dans la 2e étape est nécessaire.
Sans  `close()`,  awk  ne  fermerait  le  pipe  que  lorsque  son  processus  se
terminerait, pas avant.

### getline

`getline` permet, à tout moment, de lire un nouveau record depuis:

   - l'input d'origine (celle passée à awk au moment où on l'a invoqué)
   - un fichier
   - un pipe
   - le clavier

---

Valeurs retournées par `getline`:

    ┌────┬─────────────────────────────────────────────────────────────────────────┐
    │ 1  │ a pu lire un record                                                     │
    ├────┼─────────────────────────────────────────────────────────────────────────┤
    │ 0  │ est arrivée à la fin:                                                   │
    │    │                                                                         │
    │    │     - de l'input d'origine                                              │
    │    │     - du fichier                                                        │
    │    │     - de l'output du pipe                                               │
    ├────┼─────────────────────────────────────────────────────────────────────────┤
    │ -1 │ a rencontré une erreur                                                  │
    └────┴─────────────────────────────────────────────────────────────────────────┘

Le code de sortie  de `getline` est utile pour lire  et opérer sur l'intégralité
d'une source de texte contenant plusieurs records.
Pour  ce faire,  on utilise  la structure  de contrôle  `while`, et  on s'assure
qu'elle est  > 0  (pour éviter  de rester piégé  dans une  boucle infinie  si le
fichier n'est pas lisible).

    ┌───────────────────────────────┬─────────────────────────────────────────────────────────────┐
    │ while (getline > 0)           │ Exécute la déclaration `s`, tant qu'il reste des records    │
    │     s                         │ à traiter dans l'input                                      │
    ├───────────────────────────────┼─────────────────────────────────────────────────────────────┤
    │ while ((getline <expr) > 0)   │ tant qu'il reste des records dans le fichier dont le chemin │
    │     s                         │ est la valeur chaîne de `expr`                              │
    ├───────────────────────────────┼─────────────────────────────────────────────────────────────┤
    │ while (("cmd" | getline) > 0) │ tant qu'il reste des records dans la sortie de "cmd"        │
    │     s                         │                                                             │
    └───────────────────────────────┴─────────────────────────────────────────────────────────────┘

---

`getline` is a command, not a function (source: `$ man gawk`, gawk user's guide):

    getline()    ✘
    getline      ✔

    var = getline()    ✘
    getline var        ✔

    getline(expr)      ✘
    getline <expr      ✔

Le symbole de redirection `<` est nécessaire pour qu'il n'y ait pas de confusion
avec la syntaxe `getline var`.
On  peut aussi  expliquer  le choix  de  ce  symbole par  le  fait qu'on  change
l'argument  par défaut  de `getline`,  à savoir  l'input d'origine:  on redirige
l'entrée de `getline` vers la valeur d'une expression.

---

How do I access a record read by `getline`?

If you provided the name of a variable as an argument, use this variable.
Otherwise, use `$0`.

Note that when `getline` updates `$0`, it also updates `$i` (fields contents) and `NF`.

---

When does `getline` update `NR` and `FNR`?

Only when you use it to read a record from the input.

If you try to read a record from a new file (`getline <"file"`), or from a shell
command (`"cmd" | getline`), `NR` and `FNR` are *not* udpated.

---

When doesn't `getline` update any built-in variable?

When you  read a record  from outside the input  (shell command, file),  and you
save it in a variable.

    $ cat <<'EOF' >/tmp/file
    a
    b c
    d e f
    EOF

    $ cat <<'EOF' >/tmp/awk.awk
    /a/ { "whoami" | getline var ; print $0, NF, NR }
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    a 1 1~

Here, even though we've invoked `getline`:

   - `$0` was not changed to `b c`
   - `NF` was not changed to `2`
   - `NR` was not changed to `2`

---

`getline` est  pratique qd on a  du mal à décrire  le record sur lequel  on veut
agir, mais qu'on peut facilement décrire celui qui le précède.

---

Tout comme `next`, `getline` peut provoquer la lecture du prochain record.
La différence  vient du  fait que  `next` repositionne  l'exécution au  début du
programme, pas `getline`.
IOW,  une fois  `getline` exécutée,  awk ne  compare pas  le nouveau  record aux
patterns des précédents couples pattern-action qu'il a déjà traité.

---

    print "Enter your name: "
    getline var <"-"

Demande à l'utilisateur de taper son nom, et stocke la réponse dans `var`.

Illustre que dans les syntaxes:

    getline <expr
    getline var <expr

... `expr` peut être `"-"`; et que `"-"` désigne le clavier.

---

    "whoami" | getline
    print

    "whoami" | getline me
    print me

Affiche `username` (ex: toto), dans les 2 cas.

Mais la sortie de la commande shell  `whoami` peuple `$0` uniquement dans le 1er
exemple.

### built-in

Fonctions arithmétiques:

    ┌────────────┬────────────────────────────────────────────────────────────────────┐
    │ atan2(y,x) │ arg(x + iy) exprimé en radians dans l'intervalle ]-π,π]            │
    ├────────────┼────────────────────────────────────────────────────────────────────┤
    │ cos(x)     │ cosinus de `x`, `x` étant interprété comme une mesure en radians   │
    ├────────────┼────────────────────────────────────────────────────────────────────┤
    │ exp(x)     │ exponentiel de `x`                                                 │
    ├────────────┼────────────────────────────────────────────────────────────────────┤
    │ int(x)     │ partie entière de `x`                                              │
    ├────────────┼────────────────────────────────────────────────────────────────────┤
    │ log(x)     │ logarithme népérien de `x`                                         │
    ├────────────┼────────────────────────────────────────────────────────────────────┤
    │ rand(x)    │ nombre aléatoire choisi dans [0, 1[                                │
    ├────────────┼────────────────────────────────────────────────────────────────────┤
    │ sin(x)     │ sinus de `x`                                                       │
    ├────────────┼────────────────────────────────────────────────────────────────────┤
    │ sqrt(x)    │ racine carrée de `x`                                               │
    ├────────────┼────────────────────────────────────────────────────────────────────┤
    │ srand(x)   │ définit `x` comme nouvelle graine (seed) pour la fonction `rand()` │
    └────────────┴────────────────────────────────────────────────────────────────────┘

Fonctions opérant sur des chaînes:

    ┌────────────────────────┬─────────────────────────────────────────────────────────────────────────────┐
    │ length(a)              │ retourne le nb d'éléments dans l'array `a`                                  │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ sprintf(fmt,expr-list) │ retourne les expressions `expr-list` formatées selon `fmt`                  │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ index(s,t)             │ retourne la position de la 1e occurrence de `t` au sein de `s`              │
    │                        │ ou bien 0 si `t` est absent de `s`                                          │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ match(s,r)             │ idem, mais en plus peuple les variables RSTART et RLENGTH                   │
    │                        │                                                                             │
    │                        │ on remarque que l'ordre des arguments est le même que pour l'opérateur ~ :  │
    │                        │         string ~ regex                                                      │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ match(s,r,a)           │ idem, mais en plus peuple l'array `a` avec les parties du match             │
    │                        │ correspondant aux sous-expressions de `r`                                   │
    │                        │                                                                             │
    │                        │ a[0] contient le texte matché par toute la regex                            │
    │                        │ a[1] contient la partie du match correspondant à la 1e sous-expression      │
    │                        │ ...                                                                         │
    │                        │                                                                             │
    │                        │ a[1, "start"]  contient l'index du 1er caractère du texte matché par        │
    │                        │                la 1e sous-expression au sein de `s`                         │
    │                        │                                                                             │
    │                        │ a[1, "length"] contient la longueur du texte matché par la 1e               │
    │                        │                sous-expression                                              │
    │                        │ ...                                                                         │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ split(s,a)             │ peuple l'array `a` avec les champs issus de la division de `s` par FS       │
    │                        │ le 1er champ est stocké dans a[1]                                           │
    │                        │                                                                             │
    │                        │ retourne le nombre de champs                                                │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ split(s,a,fs)          │ idem, mais en utilisant `fs` comme séparateur de champs                     │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ substr(s,i)            │ retourne la sous-chaîne de `s` dont l'index du 1er caractère est `i`        │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ substr(s,i,n)          │ idem, mais cette fois la longueur de la sous-chaîne est fixée à `n`         │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ sub(r,s)               │ remplace la 1e occurrence du pattern `r` par la chaîne `s`                  │
    │                        │ au sein du record courant                                                   │
    │                        │                                                                             │
    │                        │ la substitution est faite in-place                                          │
    │                        │                                                                             │
    │                        │ retourne le nb de substitutions effectuées (0 ou 1)                         │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ gsub(r,s)              │ pareil que `sub()` mais globalement                                         │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ sub(r,s,t)             │ remplace la 1e occurrence du pattern `r` par la chaîne `s`                  │
    │                        │ au sein de la chaîne `t`                                                    │
    │                        │                                                                             │
    │                        │ `t` ne peut pas être le résulat d'une évaluation                            │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ gsub(r,s,t)            │ idem mais globalement                                                       │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ gensub(r,s,3)          │ remplace la 3e occurrence de `r` par `s` au sein du record courant          │
    │                        │                                                                             │
    │                        │ contrairement à `sub()` et `gsub()`, le record n'est pas modifié            │
    │                        │ la substitution est faite sur une copie                                     │
    │                        │                                                                             │
    │                        │ retourne le contenu de la copie du record après la substitution             │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ gensub(r,s,"g",t)      │ remplace toutes les occurrences de `r` par `s` au sein de `t`               │
    │                        │                                                                             │
    │                        │ `t` n'est pas modifiée                                                      │
    │                        │                                                                             │
    │                        │ au sein de la chaîne de remplacement `s`, on peut utiliser                  │
    │                        │ les métaséquences `\0`, `\1`, ..., `\9`                                     │
    │                        │                                                                             │
    │                        │ `\0` = `&` = tout le texte matché                                           │
    │                        │                                                                             │
    │                        │ `\1` est développée en le texte correspondant à la 1e sous-expression       │
    │                        │ capturée dans la regex; et ainsi de suite pour les autres métaséquences     │
    └────────────────────────┴─────────────────────────────────────────────────────────────────────────────┘


`sprintf()` n'affiche rien, contrairement à `printf`, elle se contente de retourner une chaîne.

Les fonctions `sub()` et `gsub()` retournent toutes le nb de substitutions effectuées.

Dans le tableau qui précède:

    ┌────────────┬─────────────────────────────────────┐
    │ symbole    │ signification                       │
    ├────────────┼─────────────────────────────────────┤
    │ r          │  /regex/, "regex"                   │
    ├────────────┼─────────────────────────────────────┤
    │ s,t        │  "chaînes" (string, target)         │
    ├────────────┼─────────────────────────────────────┤
    │ p,n        │  nombres (index/position, longueur) │
    ├────────────┼─────────────────────────────────────┤
    │ a          │  [array]                            │
    ├────────────┼─────────────────────────────────────┤
    │ fmt        │  "format"                           │
    ├────────────┼─────────────────────────────────────┤
    │ expr-list  │  suite d'expressions                │
    └────────────┴─────────────────────────────────────┘

---

    var = gensub(/./, " ", "g", substr($2, 1, 3))    ✔
    var = gsub(/./, " ", substr($2, 1, 3))           ✘
                                         ^
                                         └ ’gsub third parameter is not a changeable object’

Chacune de ces 2 commandes a pour  but de remplacer les 3 premiers caractères du
2e champ par des espaces, et de stocker le résultat dans `var`.

Mais la 1e  commande échoue car le 3e  argument de `gsub()` ne peut  pas être le
résultat d'une évaluation.
Ce doit être directement une chaîne, et non une expression évaluée en chaîne.

`gensub()` s'en fiche.
De plus,  `gsub()` procède aux substitutions  in-place et retourne le  nombre de
substitutions, tandis que `gensub()` opère toujours sur une copie et retourne le
contenu du texte une fois substitué.
Tout ceci fait qu'on peut voir `gsub()`  et `sub()` comme une vieille routine de
l'awk originel, et  `gensub()` comme une réelle fonction moderne  ajoutée par le
projet GNU.

---

               print rand()
    srand()  ; print rand()
    srand(42); print rand()

Affiche un nombre aléatoire dans [0, 1[, en utilisant comme graine:

   - 1
   - l'epoch:    date +%s
   - 42


La sortie de `rand()` est entièrement déterminée par la graine.
IOW, si on ne change pas la graine via `srand()`, `rand()` aura toujours la même
valeur.

---

Dans un programme awk, initialement, la graine est toujours `1`.
Puis,  au  cours  de  l'exécution  du  programme,  elle  peut  changer  via  des
invocations de `srand()`.

`srand(42)` et `srand()` ont 2 effets:

   - donne à la graine la valeur `42` / epoch
   - retourne la précédente valeur de la graine

---

    split("banana", array, "na")
    for (i in array)
        print array[i]

Affiche "ba", "", "" sur 3 lignes consécutives.

Explication:

Entre le 1er  et le 2e "na",  il n'y a rien,  et awk considère ce  rien comme la
chaîne vide.
Entre le 2e "na" et  la fin de la chaîne "banana", il n'y  a rien, et à nouveau,
awk considère ce rien comme la chaîne vide.

IOW, qd awk trouve  un séparateur, il considère toujours qu'il y  a qch avant et
après, même si ce qch est la chaîne vide.
Donc, `n` étant  le nb de séparateurs  au sein de la chaîne  passée à `split()`,
awk trouve toujours `n+1` champs.

La  fonction `split()`  de Vim  se comporte  de manière  similaire, à  ceci près
qu'elle ne retourne pas de chaîne vide  si le séparateur est présent au début ou
à la fin de chaîne, à moins qu'on lui passe un 3e argument non nul:

    let array = split("banana", "na", 1)        VimL
    ⇔
                split("banana", array, "na")    awk

---

    { gsub(/people/, "& are &"); print }

Remplace toutes les occurrences de "people" par "people are people".

Illustre  que, comme  dans Vim,  le métacaractère  `&` permet  de se  référer au
pattern matché; et comme dans Vim, on peut lui faire perdre son sens spécial en
le quotant (`\&`).

On peut aussi utiliser `\0`.

### user-defined

    function myfunc(parameter-list) {
        statements
        return expr
    }

Syntaxe générale pour définir une fonction utilisateur.

Les accolades sont toujours obligatoires, même si la fonction ne contient qu'une
seule déclaration.

---

`expr` est facultative, et la déclaration `return expr` aussi.

Si `expr` est présente, ce doit être un scalaire, pas une array.
Pour simuler  un `return  array`, on  pourra peupler  une variable  globale avec
l'array qu'on veut retourner: array = ...


La  définition  d'une   fonction  doit  se  faire  à   l'extérieur  d'une  règle
pattern-action.
C'est  logique,  car   définir  une  fonction  dans   une  règle  pattern-action
impliquerait qu'elle n'est pas dispo tant que le pattern n'a pas été matché.


On peut séparer `myfunc` de la parenthèse ouverte, dans sa définition:

    function myfunc (parameter-list)    ✔

... mais pas qd on l'appelle ensuite:

    myfunc (parameter-list)    ✘

---

    { printf("%-10s %20s\n", $0, new_feature($0)) }

Illustre  comment  développer  une  nouvelle fonctionnalité  pour  un  programme
existant.

Cette action  affiche pour  chaque record,  le champ  d'origine, et  une version
modifiée par `new_feature()`.
On  peut  ainsi  facilement  voir  si `new_feature()`  fonctionne  comme  on  le
souhaite, avant de l'intégrer dans notre programme.

Équivalent VimL:

    :echo New_feature(...)

... = des valeurs identiques aux records

##
## Ligne de commande

    $ awk --lint -f progfile <input>
    $ awk -t    -f  progfile <input>

`--lint`  et `-t`  (`--old-lint`) fournissent  des avertissements  à propos  des
constructions non portables vers la version (unix) d'awk originelle.

`--lint` fournit également des avertissements pour des constructions douteuses.

---

    $ awk -F: 'pgm' <input>
    $ awk -v RS='\t' 'pgm' <input>

Exécute `pgm` sur `<input>` en utilisant:

   - le double-point comme séparateur de champs
   - le tab          comme séparateur de records

La syntaxe  `-v var=val`  permet de configurer  n'importe quelle  variable avant
l'exécution d'un programme awk; `-F<fs>` ne permet de configurer que `FS`.

---

    $ awk -f progfile f1 FS=: f2

Traite le fichier `f1`  avec `FS` ayant sa valeur par défaut  (" "), puis traite
`f2` avec `FS` ayant pour valeur `:`.

Plus généralement,  on peut  configurer une variable  juste avant  le traitement
d'un fichier arbitraire, via la syntaxe:

    $ awk -f progfile f1 var=val f2

---

    $ awk 'pattern { action }'                      file
    $ awk 'pattern { statement1; statement2; ... }' file
    $ awk 'rule1; rule2; ...'                       file

Demande à awk d'exécuter:

   - `action`                            sur les lignes de `file` matchant `pattern`
   - `statement1`, `statement2`, ...       "
   - `rule1`, `rule2`, ...

La partie entre single quotes est un pgm awk complet.

---

Dans un fichier awk, on sépare via un newline:

   - 2 actions consécutives                  devant agir sur un même pattern

   - 2 couples pattern / action consécutifs  devant agir sur l'input

Sur la ligne de commandes, on peut remplacer les newlines par des points-virgules.

---

    $ awk '$1 ~ $2'

Permet de tester une regex, en écrivant du texte dans le 1er champ, et une regex
dans le 2e.

Si la ligne  écrite est réaffichée par  awk, ça signifie que la  regex match une
sous-chaîne du texte écrit dans le 1er champ.

Ne fonctionne que si le texte ne contient pas d'espace, ni de tab.
Autrement, il faut choisir un séparateur qui est absent du texte.
Ex:

    $ awk -F: '$1 ~ $2'
    hello world:\w+\s\w+
      hello world:\w+\s\w+    ✔

                ┌ l'espace au sein du 2e champ est pris en compte dans la regex
                │
    hello world: \w+\s\w+
            ∅                 ✘

---

    $ awk '{ print $1 }; /M/ { print $2 }' /tmp/emp.data
    Beth~
    Dan~
    Kathy~
    Mark~
    5.00~
    Mary~
    5.50~
    Susie~

Dans cet exemple, la sortie de awk mélange des prénoms et des nombres.
À chaque fois qu'un record est traité, son premier champ est affiché.
Son 2e champ l'est aussi, mais uniquement si le record contient le caractère M.

Illustre qu'awk n'itère qu'une seule fois sur les records.
Pour chacun d'eux,  il exécute toutes les règles  pattern-action pour lesquelles
le pattern matche.

IOW, awk  itère d'abord  sur les  records, et seulement  ensuite sur  les règles
pattern-action.

---

    $ awk 'rule' file1 file2

Traite les fichiers `file1` et `file2` en exécutant le code contenu dans `rule`;
illustre que l'input n'est pas limité à un fichier.

## Opérateurs

    ab?
    (ab)?

Matche 'a' ou 'ab', car on répète (`?`) puis on concatène.
Matche 'ab' ou '' , car on concatène puis on répète


Dans une expression – régulière ou non  – pour donner la priorité à un opérateur
arbitraire, il faut utiliser des parenthèses (opérateur de groupage).


Dans une expression régulière, l'opérateur de  groupage sert aussi à capturer du
texte.

---

    x % y

Retourne le reste dans la division euclidienne de x par y.

---

    i++    ++i
    j--    --j

Incrémente `i` et décrémente `j`.

Illustre que les opérateurs `++` et `--`  peuvent être utilisés en préfixe ou en
suffixe.

---

    expr1 && expr2    expr1 &&
                      expr2

    expr3 || expr4    expr3 ||
                      expr4

`expr2` n'est pas évaluée si `expr1` est fausse.
`expr4` " si `expr3` est vraie.

En effet:

   - `expr1` FAUX ⇒ `expr1 && expr2` FAUX (peu importe la valeur de vérité de `expr2`)
   - `expr3` VRAI ⇒ `expr3 || expr4` VRAI (" `expr4`)


L'évaluation d'une  expression logique se fait  de la gauche vers  la droite, et
s'arrête dès que awk connait sa valeur de vérité.


Toute expression évaluée en:

   - 0                    est considérée comme fausse
   - un nombre non nul    est considérée comme vraie

---

    a[++i]
    a[1]++
    i = ++n
    while (++i < 5)

Incrémente:

   - `i` puis cherche le i-ième élément de `a`
   - l'élément de `a` d'indice 1
   - `n` puis l'affecte à `i`
   - `i` tant qu'il est strictement inférieur à 5 (1 → 4)

Illustre que `++`  et `--` peuvent être utilisés dans  des expressions utilisant
d'autres opérateurs.

---

    ┌──────────────────────────┬───────────┐
    │ déclaration              │ affichage │
    ├──────────────────────────┼───────────┤
    │ a[++i] = 4; print a[1]   │ 4         │
    │ a[i++] = 4; print a[0]   │ 4         │
    ├──────────────────────────┼───────────┤
    │ print ++a[0]; print a[0] │ 1, 1      │
    │ print a[0]++; print a[0] │ 0, 1      │
    ├──────────────────────────┼───────────┤
    │ n = ++i; print n         │ 1         │
    │ n = i++; print n         │ 0         │
    ├──────────────────────────┼───────────┤
    │ while (++i <= 2)         │ 1, 2      │
    │     print i              │           │
    │                          │           │
    │ while (i++ <= 2)         │ 1, 2, 3   │
    │     print i              │           │
    └──────────────────────────┴───────────┘

La position de l'opérateur `++` est importante lorsqu'elle est présente dans une
expression utilisant un autre opérateur ou avec `print`.
Dans ce  tableau, on voit que  l'autre opérateur peut être  une comparaison, une
affectation ou un indexage.

`++` doit être traité:

   - avant l'autre opérateur ou print qd il est en préfixe
   - après "                                       suffixe

Tout ceci est valable pour `--` également.

---

    for (i in a)
        if (a[i] ~ /^...$/)
            b[++n] = a[i]

Calcule la  sous-array de `a`  dont tous  les éléments contiennent  exactement 3
caractères, ainsi que sa taille `n`.
L'array obtenue est `b`.

##
## Variables
### Internes
#### Tableau récapitulatif

    ┌─────────────┬──────────────────────────────────────────────────────────────────────────────────┐
    │ ARGC        │ nb d'arguments sur la ligne de commande + 1                                      │
    │             │                                                                                  │
    │             │ +1 car awk est considéré comme le 1er argument                                   │
    │             │ Si awk ne reçoit aucun argument, ARGC = 1.                                       │
    │             │                                                                                  │
    │             │ Les options ne sont pas des arguments.                                           │
    │             │                                                                                  │
    │             │ Détermine jusqu'où awk lit les éléments de ARGV:                                 │
    │             │                                                                                  │
    │             │     ARGV[0] → ARGV[ARGC-1]                                                       │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ ARGIND      │ index du fichier couramment traité dans ARGV                                     │
    │             │                                                                                  │
    │             │ le 1er fichier a pour index 1                                                    │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ ARGV        │ array contenant les arguments sur la ligne de commande (exclue les options)      │
    │             │                                                                                  │
    │             │ Permet d'accéder aux noms des fichiers de l'input.                               │
    │             │ Les éléments de ARGV sont indexés à partir de 0, et le 1er élément est 'awk'.    │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ ENVIRON     │ array contenant les valeurs des variables d'environnement du shell               │
    │             │                                                                                  │
    │             │ les indices sont les noms de ces dernières:                                      │
    │             │                                                                                  │
    │             │     print ENVIRON["HOME"]="/home/username"                                       │
    │             │                                                                                  │
    │             │ changer une valeur de l'array n'a aucun effet sur les processus shell            │
    │             │ qu'awk peut lancer via `system()` ou une redirection                             │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ FILENAME    │ nom du fichier courant (celui traité actuellement)                               │
    │             │                                                                                  │
    │             │ Mise à jour à chaque fois qu'un nouveau fichier est lu.                          │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ FNR/NR      │ index du record courant au sein du fichier / de l'input                          │
    │             │                                                                                  │
    │             │ Incrémentées avant chaque traitement d'un record du fichier                      │
    │             │ courant / de l'input.                                                            │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ FS/OFS      │ chaîne dont la valeur est utilisée comme un séparateur de champs dans            │
    │             │ l'input / output                                                                 │
    │             │                                                                                  │
    │             │ Valeur par défaut: " "                                                           │
    │             │                                                                                  │
    │             │ Même si la valeur par défaut est un espace, awk considère n'importe quelle       │
    │             │ séquence d'espaces et/ou de TABs et/ou de newlines comme un séparateur entre     │
    │             │ 2 champs.                                                                        │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ RS/ORS      │ chaîne dont la valeur est utilisée comme séparateur de records de                │
    │             │ l'input / output                                                                 │
    │             │                                                                                  │
    │             │ Valeur par défaut: "\n"                                                          │
    │             │                                                                                  │
    │             │ Jamais mises à jour.                                                             │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ IGNORECASE  │ Par défaut, toutes les opérations manipulant des chaînes sont sensibles          │
    │             │ à la casse:                                                                      │
    │             │                                                                                  │
    │             │            - comparaisons de chaînes (==, !=, <, >, <=, >=) et de regex (~, !~)  │
    │             │            - division en champs                                                  │
    │             │            - séparation des champs                                               │
    │             │            - gsub(), index(), match(), split(), ...                              │
    │             │                                                                                  │
    │             │ Mais si on donne une valeur non nulle à cette IGNORECASE, elles deviennent       │
    │             │ insensibles.                                                                     │
    │             │                                                                                  │
    │             │ Exception:                                                                       │
    │             │ les indices d'arrays ne sont pas affectés (sauf avec `asort()` et `asorti()`).   │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ NF          │ nb de champs sur le record courant                                               │
    │             │                                                                                  │
    │             │ Mise à jour avant chaque traitement d'un record,                                 │
    │             │ ET à chaque fois que $0 change OU qu'un nouveau champ est créé.                  │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ OFMT        │ format à respecter qd:                                                           │
    │ CONVFMT     │                                                                                  │
    │             │     - un nb est affiché sans conversion en chaîne:    print 1.23456789           │
    │             │     - un nb est converti en chaîne:                   print 1.23456789 ""        │
    │             │                                                                                  │
    │             │ Valeur par défaut: "%.6g"                                                        │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ RLENGTH     │ longueur d'une sous-chaîne matchée par `match()`                                 │
    │             │                                                                                  │
    │             │ Vaut -1 s'il n'y pas de match.                                                   │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ RSTART      │ index du 1er caractère d'une sous-chaîne matchée par `match()`                   │
    │             │                                                                                  │
    │             │ Vaut 0 s'il n'y pas de match. Implique que l'index du 1er caractère est 1        │
    │             │ et non 0.                                                                        │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ RT          │ RS peut être un caractère ou une regex.                                          │
    │             │ Si c'est une regex, le texte qu'elle matche peut changer d'un record à un autre. │
    │             │ awk peuple la variable RT (Record Terminator) avec ce match.                     │
    │             │                                                                                  │
    │             │ RT vaut toujours "" sur le dernier record.                                       │
    │             │                                                                                  │
    │             │ RT est mise à jour pour chaque record.                                           │
    ├─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ SUBSEP      │ séparateur à utiliser pour concaténer 2 indices consécutifs d'une array          │
    │             │ multi-dimensionnelle                                                             │
    │             │                                                                                  │
    │             │ Mnémotechnique:    SUBscript SEParator                                           │
    │             │                    │                                                             │
    │             │                    └─ indice d'une array                                         │
    │             │                                                                                  │
    │             │ Valeur par défaut: "\034"                                                        │
    │             │ Il est peu vraisemblable qu'on trouve ce caractère dans un indice,               │
    │             │ raison pour laquelle il a été choisi.                                            │
    └─────────────┴──────────────────────────────────────────────────────────────────────────────────┘

#### `ARGC`, `ARGV`

          ┌─────────────────────────────┐
          │ BEGIN {                     │
          │     FS      = ":"           │
          │     ARGV[1] = "/etc/passwd" │
          │     ARGC++                  │
          │ }                           │
          │ { print $2, $4, $6 }        │
          └─────────────────────────────┘
               │
               v
    $ awk -f progfile <<<''

Affiche les champs 2, 4 et 6 de `/etc/passwd`.

La déclaration `ARGC++` est nécessaire.
Sans elle, awk n'ajouterait pas `/etc/passwd` à son input.
En effet, il lit les éléments de `ARGV` uniquement jusqu'à l'index `ARGC - 1`.
Or, ici, `ARGC`  = 1, donc `ARGC -  1 = 0` et  awk ne lit que le  1er élément de
`ARGV` ('awk').

Illustre que  pour accroître l'input,  il ne suffit  pas d'ajouter un  élément à
`ARGV`, il faut aussi incrémenter `ARGC`.

---

    BEGIN { ARGV[2] = "" }
      ou
    BEGIN { delete ARGV[2] }

Supprime le 2e fichier de l'input.

Qd awk rencontre une  chaîne vide dans `ARGV`, il passe  au prochain élément, et
continue jusqu'au `(ARGC-1)`ième.

Illustre qu'en  changeant le contenu de  `ARGV` dans une règle  `BEGIN`, on peut
modifier l'input.

---

    awk -f progfile 42
               │
      ┌───────────────────────┐
      │ BEGIN {               │
      │     myvar   = ARGV[1] │
      │     ARGV[1] = "-"     │
      │ }                     │
      └───────────────────────┘

Illustre comment manuellement ajouter l'entrée standard à l'input d'awk.

Dans cet exemple, on veut passer à awk un argument numérique tout en lui faisant
lire son entrée standard.

Malheureusement,  tout argument  suivant  les options  est  interprété comme  un
fichier, et redirige l'input d'awk vers lui.
Pour résoudre  ce problème,  on peut remplacer  `ARGV[1]` qui  initialement vaut
`42` par la valeur spéciale `"-"`.


Si awk ne  reçoit aucun fichier en  argument, dit autrement si  `ARGV` n'a qu'un
seul élément (`ARGC = 1`, `ARGV[0]  = 'awk'`), il lit automatiquement son entrée
standard, qui est connectée soit au clavier soit à un pipe.

#### `FS`, `RS`, `OFS`, `ORS`, `NR`

    BEGIN { FS = "\t" }
          { print $1 }

Modifie la  valeur de `FS` pour  tous les records,  en lui donnant pour  valeur un
tab.

Modifier `FS` n'affecte pas la définition des champs du record courant, uniquement
ceux des records qui suivent.

Si on veut modifier  la définition des champs de tous les  records, y compris le
1er, il faut donc modifier `FS` via le pattern `BEGIN`.

---

Can I change the index of a record?

Yes, `NR` is writable.

    $ cat <<'EOF' >/tmp/file
    a
    b
    c
    EOF

    $ cat <<'EOF' >/tmp/awk.awk
    /a/ { NR += 2 }
        { print $0, NR }
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    a 3~
    b 4~
    c 5~

---

    ┌───────────────────────────────┐    ┌─────────────────────────────────┐
    │ BEGIN { FS = "_"; OFS = "|" } │    │ This_old_house_is_a_great_show. │
    │ {                             │    │ I_like_old_things.              │
    │     sub(/old/, "new ", $0)    │    └─────────────────────────────────┘
    │     sub(/old/, "new ", $2)    │      │
    │     print                     │      │
    │ }                             │      │
    └───────────────────────────────┘      │
                                  │        │
                                  v        v
                        ┌─────────────────────┐       ┌────────────────────────────────┐
                        │ awk -f pgm.awk data │──────>│ This|new|house|is|a|great|show.│
                        └─────────────────────┘       │ I_like_new_things.             │
                                                      └────────────────────────────────┘

On constate qu'awk a effectué le remplacement `FS → OFS` sur le 1er record, mais
pas sur le 2e.
Pk?
Car la  1e déclaration  n'a pas  besoin de  diviser le  record pour  extraire un
champ, elle travaille sur `$0`.
Et la 2e échoue.
Donc, aucune des déclarations ne divise le 2e record.

    sub(/old/, "new ", $0)    ✔ réussit mais pas besoin de diviser le record
    sub(/old/, "new ", $2)    ✘ échoue, car "new" n'est pas présent dans le 2e champ ("like")

---

    ┌─────────────────────────────────┐    ┌─────────────────────────────────┐
    │ BEGIN { FS = "\\."; OFS = "|" } │    │ This.old.house.is.a.great.show. │
    │ {                               │    │ I.like.old.things.              │
    │     $(NF + 1) = ""              │    └─────────────────────────────────┘
    │     print                       │      │
    │ }                               │      │
    └─────────────────────────────────┘      │
                                 │           │
                                 v           v
                       ┌─────────────────────────┐       ┌──────────────────────────────────┐
                       │ awk -f pgm.awk     data │──────>│ This|new|house|is|a|great|show|| │
                       └─────────────────────────┘       │ I|like|new|things||              │
                                                         └──────────────────────────────────┘


Dans  cet exemple,  la valeur  de  `FS` est  interprétée comme  une regex  "\\."
décrivant un point littéral.
Plus généralement, les valeurs de `FS` et `RS` sont interprétées comme des regex
si elles contiennent plusieurs caractères, autrement littéralement:

    FS = "\\."    ⇔    FS = "."
    RS = "\\."    ⇔    RS = "."

Les valeurs de `OFS` et `ORS` sont toujours littérales.

---

    BEGIN { RS = "_"; ORS = "|" }
          { print }

Effectue la transformation suivante:

    I_like_old_things.    →    I|like|old|things.
                               |

Illustre que le remplacement de `RS` par `ORS` est automatique et inconditionnel.


On remarque un pipe sous le `I`, sur une 2e ligne.
awk  considère  qu'il  y  a  un  “record  terminator“  (`RT`)  entre  2  records
consécutifs, mais aussi après le dernier record.

From the gawk user's guide, `4.1.1 Record Splitting with Standard awk`, page 63:

> Reaching the end of  an input file terminates the current  input record, even if
> the last character in the file is not the character in RS.

`RT` est décrit par le caractère / la regex contenu(e) dans `RS`.

Sur le dernier record d'un input, `RT = ""` peu importe la valeur de `RS`.
Awk remplace le dernier `RT` (`""`) par `ORS`.

Par contre,  pourquoi awk  semble ajouter  un newline  après le  dernier record,
alors que `ORS` n'en contient pas?

    I|like|old|things.
    |

    vs

    I|like|old|things.|

Car il y  a toujours un newline  à la fin d'un  fichier / ou de  la sortie d'une
commande shell.

    $ echo '' >/tmp/file
    $ xxd -p /tmp/file
    0a~

    $ echo '' | xxd -p
    0a~

Donc, sur le dernier  record de l'input ou d'un fichier,  ce newline fait partie
du record, et awk ajoute `ORS` *après*.

---

    ┌────────────────────┐  ┌────────────────┐
    │ BEGIN { FS = ":" } │  │ ::foo:bar:baz: │
    │       { print NF } │  └────────────────┘
    └────────────────────┘       │
                      │          │
                      v          v
            ┌─────────────────────────┐
            │ awk -f pgm.awk    data  │
            └─────────────────────────┘

Affiche 6, car awk considère qu'il y a 6 champs.

    ::foo:bar:baz:

En plus de `foo`, `bar` et `baz`, awk divise le début du record `::` en 2 champs
vides, et la fin `:` en un champ vide.

Plus généralement, qd awk divise un record, il génère un champ vide:

   - s'il rencontre 2 délimiteurs consécutifs
   - si le début du record commence par un délimiteur
   - si la fin du record se termine par un délimiteur


Exception:

Qd `FS = " "`, awk ignore les espaces et tabs au début et à la fin d'un record.
`" "` n'est pas un simple espace, c'est une valeur spéciale pour `FS`.

---

    BEGIN { RS = "" }

`""` est une valeur spéciale pour `RS`.
awk semble l'interpréter comme `"\n+"`.

IOW, l'input  est divisée  en records  uniquement au  niveau d'une  ou plusieurs
lignes vides (sans whitespace).

---

    BEGIN { RS = ""; FS = "\n" }

Chaque ligne est considérée comme un champ.

Idiome généralement utilisé pour traiter des records multi-lignes.
Ex:

    Name: John                  |                 |→ champ 1
    Address: 5, Baker Street    |→    record 1    |→ champ 2
    Phone: 12345678             |                 |→ champ 3

    Name: Bruce                 |                 |→ champ 1
    Address: 3, Church Street   |→    record 2    |→ champ 2
    Phone: 87564321             |                 |→ champ 3

### Fields

    $ awk '{ print ($1 < $2) }' <<<'31 30'
    0~

    $ awk '{ print ($1 < $2) }' <<<'31 3z'
    1~

Ces 2 commandes  illustrent que lorsqu'un champ est numérique,  awk affecte à la
variable correspondante une valeur numérique et une valeur chaîne.

En effet, dans la  1ère commande, le test échoue, ce qui  prouve que les valeurs
de `$1` et `$2` étaient des nombres, et pas des chaînes.
Dans la 2e commande, le test réussit, ce qui prouve que, cette fois, les valeurs
sont des chaînes.

Qd l'opérateur de comparaison travaille sur  des opérandes dont au moins une des
valeurs est numérique, il fait une comparaison numérique (commande 1).

Mais, si l'un des opérandes n'a aucune valeur numérique, il fait une comparaison
de chaînes, quitte à faire une coercition si besoin.
C'est ce  qui se  passe dans la  commande 2, où  le 2e  champ n'a pas  de valeur
numérique (`3z`).

---

    $2 = ""; print

Affiche les records en effaçant le 2e champ.

Illustre qu'on peut se  servir de la variable `$i` pour  changer le contenu d'un
champ.


Plus  généralement, une  même  expression nous  permet d'accéder  à  la fois  en
lecture et en écriture à certaines variables (`$1`, `NR`, ...).
Certaines, pas toutes; on ne peut pas modifier `FILENAME`.

Pour rappel, on accède à une variable en:

   - écriture qd elle se trouve dans le côté gauche de l'affectation
   - lecture  "                              droit  "

---

    !$1
    ($1)++

Inverse (au sens logique) / Incrémente la valeur du 1er champ.

##
# Todo
## Study how to write manpages

It's explained in the Appendix A of the "Classic Shell Scripting" book.
To check the formatting of a manual page, run:

    $ groff -man -Tascii program.man

To install a manpage, move your `program.man` file in `~/share/man/man1/`.
Optionally, compress it with `gzip` in `~/share/man/cat1/`.

Why does `$ man` look into `~/share/man` even though it's not in `$MANPATH`?

    https://askubuntu.com/a/244810/867754
    https://askubuntu.com/a/633924/867754
    man 1 manpath
    man 5 manpath

Anyway, version control `~/share/man`.

Also, if you want to draw table in a manpage, you probably need to read `$ man tbl`.
For pictures and equations, see also `$ man pic` and `$ man eqn`.

## Idea of infrastructure

At  the  root of  every  wiki,  you  should have  a  file  which lists  all  the
examples/exercises.
For each exercise, there should be a  telling name and a (concealed) path to the
file (so that you can open it with `ZF`).

Also, in  this file  there should  be a  local mapping  (`cop`?) which  starts a
“preview” mode.
In this mode,  a preview window should  show the contents of  the exercise whose
name/path is  under the cursor;  the contents should  be updated as  your cursor
moves.

Use only one file, even if you have exercises coming from several books.
Divide the file into sections; one per book.
And maybe  divide those sections  further; one  subsection per chapter,  and one
subsubsection per subchapter.

Besides, each exercise should be confined in its own directory:

    ~/wiki/<subject>/examples/<book_title>/ch12/ex34/<script_name>

Inside, it should be accompanied by 2 other files: `input` and `output`.
`input` should contain an example of input on which the example script operates.
`output` should contain the output of the script when passed `input`.

Install a mapping (`-e`?) to open this file from anywhere in the wiki.

The goal is to  reduce the access time to an info you're  looking for, and which
you know is somewhere in an exercise you solved in the past.

## Document that `.` can match a newline in awk (but not in sed).

I read this in ‘Sed & Awk’, page 48 of the pdf, table 3.1.
Make sure it's true.

It's probably because awk can operate on multi-line records.

## Write a `|c` mapping to lint the current awk script (using `--lint`).


## In `elseif cond return ...`, the `elseif` is useless.

Read this:

<https://github.com/soimort/translate-shell/wiki/AWK-Style-Guide>
<https://softwareengineering.stackexchange.com/questions/157407/best-practice-on-if-return#comment300476_157407>

Usually, there's a difference between these snippets:

    if cond1
        do sth
    if cond2
        do sth else

    if cond1
        do sth
    elseif cond2
        do sth else

The difference happens when `cond1` and `cond2` are true simultaneously.
In this  case, the  first snippet  executes both actions,  while the  second one
executes only one action.

But this difference disappears when the action is a `return` statement.
In this case, the first snippet executes only one action, like the second snippet.
So, there's no need for an `else` after a `return`:

    if cond1
        return sth
    elseif cond2
        return sth else

    ⇔

    if cond1
        return sth
    if cond2
        return sth else

## Read the sections 6.3.2.1, 6.3.2.2, 6.3.2.3  in the gawk user's guide,

to better understand how gawk handles the coercion with relational operators.

## Document that a newline is also ignored after the keyword `do` (see gawk book).


## Finish ‘The AWK Programming Language’.

The first time we read our first awk book,  we stopped at the page 84 of the pdf
(72 in the original book).

## Read: <http://www.awklang.org/>

Have a look at the links in the sidebar:
<https://github.com/e36freak/awk-libs>
<https://github.com/ericpruitt/wcwidth.awk> (Miscellaneous > More AWK libraries...)
...

##
# Reference


[1]: https://en.wikipedia.org/wiki/Scientific_notation#Normalized_notation
[2]: https://en.wikipedia.org/wiki/Significand
