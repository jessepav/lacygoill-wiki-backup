On s'est arrêté à la page 84 du pdf / 72 du livre.

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

In the shell script, you need to quote `$@` to prevent the shell from performing
a word splitting after the expansion (`$@` → `$1 $2 ...`):

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

### Which version should I choose?

Use an awk script.

It's better than `$ awk -f`, because  you don't have to remember the `-f` option
every time you need to run your script.

It's better than a shell script, because with the latter, all the code is inside
a string, which prevents the awk code from being correctly syntax highlighted.

Besides, in a shell script, your code can't include a single quote:

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

Anything you type will be printed back if it contains an `x` character.

### When is the interactive mode useful?

When you need to test a piece of code.

   1. write the code
   2. write some arbitrary input
   3. watch the output
   4. repeat steps 2 and 3 as many times as you want

### How to exit?

Press <kbd>C-d</kbd>.

This sends the end-of-file signal to the awk foreground process.

##
# Syntax
## Why do I have to
### surround an awk program with single quotes?

To be able to write code on several lines.

To protect special characters from being interpreted by the shell.
Like `$` and `SPC` (any shell), or `{` and `}` (only in zsh).

    $ awk '$3 == 0 { print $1 }' /tmp/emp.data

Without  the single  quotes,  you  would have  to  manually  quote each  special
character:

    $ awk \$3\ ==\ 0\ \{\ print\ \$1\ \} /tmp/emp.data

### surround an action with curly braces?

Because you can omit the pattern or the action.
And if you *do* omit one of them,  awk must be able to tell whether your statement
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
## Can a string
### be surrounded by single quotes?

No, it's a syntax error.

    $ cat <<'EOF' >/tmp/file
    foo
    bar
    baz
    EOF

    $ cat <<'EOF' >/tmp/awk.awk
    { printf '%d', 1 }
    #        ^  ^
    #        ✘  ✘
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    awk: /tmp/awk.awk:1: { printf '%d', 1 }~
    awk: /tmp/awk.awk:1:          ^ invalid char ''' in expression~
    awk: /tmp/awk.awk:1: { printf '%d', 1 }~
    awk: /tmp/awk.awk:1:          ^ syntax error~

    $ cat <<'EOF' >/tmp/awk.awk
    { printf "%s", 'word' }
    #              ^    ^
    #              ✘    ✘
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    awk: /tmp/awk.awk:1: { printf "%s", 'word' }~
    awk: /tmp/awk.awk:1:                ^ invalid char ''' in expression~
    awk: /tmp/awk.awk:1: { printf "%s", 'word' }~
    awk: /tmp/awk.awk:1:                ^ syntax error~

    $ cat <<'EOF' >/tmp/awk.awk
    { printf "%s ", "word" }
    EOF

    $ awk -f /tmp/awk.awk /tmp/file
    word word word ~

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
## What are the three possible representations for a number?

Integer:

   * 1
   * +1
   * -1

Decimal:

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

## How does awk store any number?

As a float (the precision of which is machine dependent).

    $ awk '$1 == $2' <<<'123 123.0'
    123 123.0~

    $ awk '$1 == $2' <<<'123.0 1.23e2'
    123.0 1.23e2~

The fact that awk prints back the input  line means that the test `$1 == $2` has
succeeded; which means that the first  and second fields are identical, and that
the two numbers are considered to be equal.

##
## How can `{ print $0 }` be simplified?

    { print }

---

By default, `print` uses `$0` as an argument; so you can omit `$0`.

## How can the following assignment be simplified?

    test = var == 123 ? 1 : 0

↣
    test = var == 123
↢

### Why is it possible?

A  comparison  is an  expression,  whose  value is  `1`  when  it succeeds,  `0`
otherwise; as such, it can be used (alone) in the rhs of an assignment.

    $ awk 'BEGIN { var = 123 ; test = var == 123; print test }'
    1~

##
## How to refer to a field whose index is stored in a variable?

Use the `$var` syntax.

    $ cat <<'EOF' >/tmp/file
    THE quick brown
    fox JUMPS over
    the lazy DOG
    EOF

    $ awk '{ var += 1; print $var }' /tmp/file
    THE~
    JUMPS~
    DOG~

This command prints the  first, second and third field of  the first, second and
third record.

##
# Built-In Variables
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
consider that `NF` is its operand, instead of `NF-1`.

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

Note that  if one of  the field  began with a  non-digit character, it  would be
automatically coerced  into the number  `0`; and  so `$NF-1` would  be evaluated
into `-1`.

##
# Printing
## How to print a newline?
### at the end of an output record?

    print ""

The reason  why you can omit  `\n` is because, at  the end of an  output record,
`print`  automatically adds  the contents  of `ORS`,  whose default  value is  a
newline.

### anywhere?

    printf("\n")

##
# Modifying Fields
## How to add a new field to a record?

Refer to the field whose index is `NF + 1`.
Assign to it the desired contents

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

## What's the side effect of a field modification?

Awk automatically splits  the record into fields to access  the field to modify,
then replaces every `FS` with `OFS` to create the output record.

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
# Regex
## Which common pitfall should I avoid when using a string as a regex?

You need  to double the  backslash for every escape  sequence which you  want to
send to the regex engine.

For example, to describe a literal dot, you can write either of these:

   - `/\./`
   - `"\\."`

## What's the benefit of using a string as a regex (`"regex"`), rather than `/regex/`?

You can  break it down into  several substrings, and  join them back to  get the
final regex.

By  saving the  substrings in  variables with  telling names,  you increase  the
readibility and maintainability of your code.

##
# I have the following file:

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

## How to print
### the names of the employees which have *not* worked?

    $ awk '$3 == 0 { print $1 }' /tmp/emp.data
    Beth~
    Dan~

### the *lines* containing the names of the employees which have not worked?

    $ awk '$3 == 0' /tmp/emp.data
    Beth    4.00   0~
    Dan     3.75   0~

### the names of all the employees?

    $ awk '{ print $1 }' /tmp/emp.data
    Beth~
    Dan~
    Kathy~
    Mark~
    Mary~
    Susie~

### the lines prefixed with increasing numbers?

Use the `NR` variable:

    $ awk '{ print NR, $0 }' /tmp/emp.data
    1 Beth    4.00   0~
    2 Dan     3.75   0~
    3 Kathy   4.00   10~
    4 Mark    5.00   20~
    5 Mary    5.50   22~
    6 Susie   4.25   18~

###
### the names of the employees which have worked more than 0 hours, and their total pay?

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

#### same thing, but adding the text `total pay for` before the name, and `is` before the pay?

    $ awk '{ print "total pay for", $1, "is", $2 * $3 }' /tmp/emp.data
    total pay for Beth is 0~
    total pay for Dan is 0~
    total pay for Kathy is 40~
    total pay for Mark is 100~
    total pay for Mary is 121~
    total pay for Susie is 76.5~

##### same thing, but aligning the names and the pays?

To get more control over the formatting, you would need `printf`:

    $ awk '{ printf "total pay for %-8s is %6.2f\n", $1, $2 * $3 }' /tmp/emp.data
    total pay for Beth     is   0.00~
    total pay for Dan      is   0.00~
    total pay for Kathy    is  40.00~
    total pay for Mark     is 100.00~
    total pay for Mary     is 121.00~
    total pay for Susie    is  76.50~

##
##
##
# Affichage
## Alignement

Il existe 3 méthodes pour aligner la sortie d'awk:

   - utiliser `printf` en donnant une largeur de champ suffisante pour chaque colonne
   - jouer sur les variables FS et/ou OFS
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
non nul, awk effectue le remplacement FS → OFS, sur son record.

En clair, par défaut,  awk remplace chaque séquence d'espaces et  de tabs par un
espace.
Si  on a  utilisé des  tabs pour  aligner des  colonnes au  sein d'un  texte, ce
remplacement peut ruiner l'alignement.

Avec la 2e commande précédente, awk ne  supprimera que les tabs (car FS = "\t"),
qu'il remplacera par des tabs (car OFS = "\t").

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

L'avantage par rapport  aux déclarations awk précédentes (BEGIN  ...), est qu'on
n'a pas besoin de  se soucier de savoir comment l'input  d'awk était alignée, ni
même si elle était alignée.

## Auto-indentation

L'auto-indentation fournie  par l'opérateur `=`  de Vim repose sur  la fonction
`GetAwkIndent()`, elle-même configurée par l'option `indentexpr`.

Par    défaut,     elle    est    définie    dans     le    filetype    plugin
`$VIMRUNTIME/indent/awk.vim`.  Mais, son indentation est souvent fausse. On peut
dl une meilleure version sur vim.org:

        http://www.vim.org/scripts/script.php?script_id=4372

Une  fois   le  plugin  téléchargé,  il   ne  reste  qu'à  le   placer  dans
`~/.vim/after/indent/`.

Atm, le code inclut une  documentation sommaire expliquant comment configurer le
plugin.  La configuration  repose sur un ensemble de variables  globales de type
booléen.

## Précision numérique

    END {
        OFMT = CONVFMT = "%.2f"
        print 1E2                  # affiche 100, et pas 100.00
        print 1E2 ""               # idem
    }

Qd un  flottant est affiché,  il est formaté selon  le template défini  par OFMT
(pas de coercition nb → chaîne) ou CONVFMT (coercition).
Mais qd un entier est affiché, il  reste entier, peu importe les valeurs de OFMT
et CONVFMT.


    END { printf "%.6g", 12E-2 }
    0.12~
    END { printf "%.6g", 123.456789 }
    123.457~

Il  semble  que les  spécificateurs  de  conversion  `%e`,  `%f`, et  `%g`  sont
identiques entre les fonctions `printf()` de Vim et awk, à deux exceptions près.

Le `%g` du  `printf()` d'awk supprime les 0 non  significatifs, ET il interprète
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

Les parenthèses forcent awk à évaluer l'expression `var >`.
1.234` avant d'exécuter `print Sans elles, awk exécuterait`.
d'abord `print`, puis redirigerait la sortie le fichier `1.234 `.


L'expression `var > 1.234` retourne `1`  (réussite), ce qui signifie que `var` a
été formatée APRÈS l'évaluation de `var > 1.234`:

    1.23456789 > 1.234 ✔
    1.23       > 1.234 ✘

... mais AVANT d'afficher le résultat:

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

   - `printf` ne remplace RIEN: ni FS → OFS entre 2 expressions, ni RS → ORS
     à la fin

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

   - OFS
   - rien

Illustre que  l'opérateur de concaténation  (implicite) n'ajoute rien  entre les
expressions.

---

Qd awk traite le record matchant le pattern:

   - BEGIN, NR vaut 0
   - END,   NR vaut l'index du dernier record

Arrivé à END, NR n'est pas incrémenté.
IOW, si un fichier contient 5 lignes, NR vaut 5 sur la dernière ligne, et encore
5 sur la ligne END.

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
seulement une simple instruction.
C'est possible car awk n'exécute pas la  commande shell tant qu'on n'a pas fermé
le pipe nous-mêmes.

awk  ne ferme  jamais un  pipe lui-même,  sauf  à la  fin, qd  son processus  se
termine, et qu'il y est obligé.

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

En revanche, dans l'input, les nombres sont toujours interprétés comme décimaux,
sauf si awk a été lancé avec le flag `-n` (--non-decimal-data).

---

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


    $ awk 'BEGIN { print (1.2 == 1.1 + 0.1 ) }'
    0    ✘~

    $ awk 'BEGIN { x = 1.2 - 1.1 - 0.1 ; print (x < 0.001 && x > 0 || x > -0.001 && x < 0) }'
    1    ✔~

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

<https://www.gnu.org/software/gawk/manual/html_node/Floating_002dpoint-Programming.html>

Pour une comparaison entre flottants, la solution consiste à ne pas les comparer
directement entre  eux, mais plutôt  leur distance  par rapport à  une précision
arbitraire.

---

    $ awk '1e50 == 1.0e50 { print 1 }' <<< ''
    1    ✔~

    $ awk '1e500 == 1.0e500 { print 1 }' <<< ''
    1    ✘~

Le problème peut venir de nombres trop grands, pex:

    1e50  == 1.0e50     ✔
    1e500 == 1.0e500    ✘

    1.2 == 1.1 + 0.1 { print }
    ✘ devrait afficher tous les records de l'input mais atm n'affiche rien car la comparaison échoue~

    { print 1.2 - 1.1 - 0.1 }
    retourne -1.38778e-16, mais devrait retourner 0~
    D'où vient cette différence non nulle ???

<https://www.gnu.org/software/gawk/manual/html_node/Exact-Arithmetic.html#Exact-Arithmetic>

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
    │ │        └─ les index sont des chaînes  │           │
    │ └─ les index sont des nbs               │           │
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
Il faut donc  que les ASSOCIATIONS 'indice - élément'  soient mémorisées, et non
pas simplement les éléments.

---

    a[NR] = $0

Sauvegarde le contenu des records dans l'array `a`.


On remarque qu'on  n'a pas besoin d'initialiser une array  avant de lui affecter
un élément.
On n'a pas non plus besoin de s'assurer qu'elle a une dimension suffisante.
Comme pour  une variable, le  simple fait de  mentionner un élément  d'une array
suffit à l'initialiser avec pour valeur "".

Pour  faire qch  de similaire  en VimL,  il faudrait  d'abord déclarer  la liste
`lines` avec une taille suffisante:

    let lines = repeat([0], NF)
    [0, 0, ...]~

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
et  concaténées en  utilisant le  contenu de  la variable  interne SUBSEP  comme
séparateur.

---

    if (i in a)
        print a[i]

    if ((i,j) in a)
        print a[i,j]

Teste si `a[i]` / `a[i,j]` existe et si c'est le cas, affiche sa valeur.


`i` et `j` peuvent être des variables,  des chaînes ou des nombres (convertis en
chaînes).


`i in a` est  une expression retournant `1` si l'array  `a` contient `un élément
d'indice `i`, 0` autrement.


Dans une expression utilisant l'opérateur `in`, un indice multi-dimensionnel est
entouré de parenthèses (et non de crochets).

---

    if ("Africa" in pop) ...        ✔
    if (pop["Africa"] != "") ...    ✘

Ces 2 `if` testent si l'indice "Africa" est présent dans l'array `pop`.

Le 2e  `if` ajoute  automatiquement à  `pop` l'élément  d'indice "Africa"  et de
valeur "".
Ce n'est pas le cas du 1er `if`, dont la syntaxe est sans doute à préférer.


    delete a
    delete a[42]

Supprime tous les éléments de l'array `a` / l'élément d'indice 42.

---

    for (i in a)
        print a[i]

Affiche tous les éléments de l'array `a`.


Si l'array  est multi-dimensionnelle, et qu'à  l'intérieur de la boucle  on veut
accéder  à  chaque  composant  de  l'indice `i`  séparément,  on  peut  utiliser
`split()` et SUBSEP:

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

## Coercition

On peut  séparer les  opérateurs en  3 catégories, en  fonction des  types de
données sur lesquels ils peuvent travailler:

   - nombre
   - chaîne
   - chaîne et nombre

Pour chacune de ces catégories, une coercition peut avoir lieue:

    ┌───────────┬────────────────────┬──────────────────┬─────────────────┐
    │ opérateur │  opérandes valides │ opérande utilisé │   coercition    │
    ├───────────┼────────────────────┼──────────────────┼─────────────────┤
    │     +     │      nombres       │      chaîne      │ chaîne → nombre │
    │           │                    │                  │                 │
    │ implicite │      chaînes       │      nombre      │ nombre → chaîne │
    │           │                    │                  │                 │
    │     <     │ chaînes et nombres │ chaîne et nombre │ nombre → chaîne │
    └───────────┴────────────────────┴──────────────────┴─────────────────┘

Ex1:

    print $1, 100 * $2

Dans cet exemple, si  le 1er champ est un nb, il sera  converti en chaîne, et si
le 2e champ est une chaîne, elle sera convertie en nb.

    Ex2:

    $4 == "Asia"

Dans cet autre exemple, si le 4e champ est un nb, il sera converti en chaîne.

Conclusion:

Awk  est  cool,  et  il  convertira  si  besoin  un  nombre  en  une  chaîne  et
réciproquement.

Mais un pb se  pose qd on passe un nombre et une  chaîne à un opérateur binaire,
ET qu'il peut travailler à la fois sur des nombres et des chaînes.

Awk  doit alors  choisir  quelle  coercition réaliser:  il  choisit toujours  de
convertir le nombre en chaîne.
Contrairement à Vim:

    ┌ awk parse cet input comme un nb, pas une chaîne
    │
    $ awk '$1 == "089" { print "match!" }' <<< "89"
    ∅~

    $ awk '$1 == "089" { print "match!" }' <<< "089"
    match!~

    :echo "89" == 089
    1~

En cas d'ambiguïté, awk donne la priorité aux chaînes, Vim aux nombres.


Attention à ne pas faire de tests avec `042` au lieu de `089`.
Dans  du  code (!=  input),  awk  interprète `042`  comme  un  nb octal  ce  qui
fausserait nos tests.


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
    print 10 + $2
    si le 2e champ est la chaîne '10.10string', awk affiche `20.1`, et non pas `20`~

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


Pourquoi `$1+0` et pas simplement $1 ?
Pour forcer la coercition de $1 en nb, au cas où ce serait une chaîne.

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

Car 12 est  converti en "12" ET  sur ma machine, les lettres  sont rangées après
les chiffres donc "a" > "2".


Illustre qu'un  opérateur relationnel  d'infériorité ou de  supériorité, opérant
sur  des chaînes,  teste l'ordre  alphabétique  dans lequel  les opérandes  sont
rangés.
L'ordre dépend de la machine.


Montre aussi qu'une expression incluant un opérateur relationnel retourne tjrs 1
ou 0, selon que la relation est vraie ou fausse.

---

    $1 < 0 { print "abs($1) = " -$1 }      ✘
    $1 < 0 { print "abs($1) = " (-$1) }    ✔
    $1 < 0 { print "abs($1) = ", -$1 }     ✔

L'objectif, ici, est  d'afficher la chaîne "abs($1) = "  puis l'opposé numérique
du 1er champ.

La 1e déclaration pattern-action échoue, les 2 suivantes réussissent.
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
## Structure de contrôle
### if

    if (e1)           ⇔    if (e1) s1; else if (e2) s2; else s3
        s1
    else if (e2)
        s2
    else
        s3


    if (e1) {         ⇔    if (e1)      { s1; s2 }
        s1                 else if (e2) { s3; s4 }
        s2                 else         { s5; s6 }
    }
    else if (e2) {
        s1
        s2
    }
    else {
        s1
        s2
    }

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

    for (e)           for (e)
    s1       ⇔    s1         s2 est hors de la boucle (awk se fiche de l'indentation)
    s2                s2

    for (e) {
    s1
    s2                       s2 est dans la boucle (grâce aux accolades)
    }


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


    for (e1; e2; e3)    ⇔    e1 ; while (e2) { s; e3 }
        s                    │           │        │
                             │           │        └ transformation
                             │           └ condition
                             └ initialisation

---

    for (e1 ;; e3)

`e2` étant absente (`;;`), elle est considérée comme vraie par défaut.
Ça implique que cette boucle ne finira jamais.

---

    for (i = 1; i <= 5; i++)        i = 1
        s                             while (i <= 5) {
                                          s
                                          i += 1
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

Illustre le fonctionnement de la déclaration `break`.

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

Illustre le fonctionnement de la déclaration `continue`.

Au sein d'une boucle `for`, `while` ou `do`, elle permet de passer directement à
la prochaine itération de cette dernière.


Les déclarations `break` et `continue` fonctionnent comme leurs homonymes Vim.

---

    for (i = 1; i <= NF && $i != ""; ++i)
        ;
    if (i < NF) print

Affiche tous les records dont un des champs est vide.
Illustre l'utilité de la déclaration vide `;`.

Explication: La boucle  incrémente `i` tant que  le champ de même  index est non
vide.
Elle ne fait rien d'autre, car elle ne contient que la déclaration vide.

Une fois  sorti de  la boucle, `if`  compare `i`  à NF: si  `i` est  plus petit,
`print` affiche le record.


Un champ vide n'est pas un champ rempli d'espaces.
Un champ vide correspond à 2 FS consécutifs (pex 2 Tabs).

### while

    while (e)      ⇔    while (e) s    ⇔    do          ⇔    do s; while (e)
        s                                       s
                                            while (e)

---

    while (e) {    ⇔    while (e) { s1; s2 }            ⇔    do { s1; s2 } while (e)
        s1
        s2
    }

Si `e` est fausse dès le début, une boucle `while` n'exécutera jamais `s`.
En revanche, une boucle `do` l'exécutera une fois, car `do` vient avant `while`.

### next / exit

    exit
    exit 123

Se rendre directement à la déclaration END.
Idem, en retournant 123 comme code de sortie du programme awk.

Si `exit` est utilisé au sein de la déclaration END, on quitte le programme awk,
sans terminer de traiter les actions END.

---

    next
    nextfile

Arrête  le  traitement du  record  courant,  ignore les  couples  pattern-action
suivants, et passe:

   - au prochain record du fichier courant
   - au 1er      record du prochain fichier de l'input


Qd `nextfile` est utilisé, certaines variables sont mises à jour:

   - FILENAME
   - ARGIND
   - FNR  →  1


`next` provoque une erreur s'il est utilisé dans la déclaration BEGIN ou END.
Idem pour `nextfile`.

---

    pattern { action1; next}
            { action2 }

Exécute `action1`  sur les  records où  `pattern` matche,  et `action2`  sur les
autres.

Grâce à `next`,  on évite l'exécution de `action2` sur  les records où `pattern`
ne matche pas.

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

La déclaration `default` est facultative.

En l'absence de déclarations `break`, awk continue de traiter le bloc `switch`.
IOW, sans `break`, awk exécute autant  de déclarations qu'il y a de comparaisons
qui réussissent.
Si on veut  qu'il n'en exécute qu'une  (la 1e qui réussit), il  faut inclure des
`break` pour sortir du `switch`.

##
## Fonctions
### close

La  fonction `close()`  permet de  fermer des  fichiers et  pipes ouverts  (i.e.
auxquels le processus awk accède en lecture).
Ça peut être  nécessaire entre autres car l'OS possède  une limite concernant le
nb  de fd  (file descriptors)  ouverts  simultanément, ce  qui limite  le nb  de
fichiers / pipes pouvant être ouverts à un instant T.

---

    BEGIN {
        "date" | getline var
        print var

        system("sleep 3")
        close("date")

        "date" | getline var
        print var
    }

Affiche l'heure et la date du jour, dort 3s, puis réaffiche l'heure.

Sans l'instruction `close("date")` qui ferme le précédent pipe `"date" | getline var`,
la  2e commande  shell  `date`  n'aurait pas  été  exécutée,  et `print`  aurait
réaffiché exactement la même heure.

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

Bien que  ce soit  une fonction,  sa syntaxe  se rapproche  plus de  celle d'une
déclaration:

    getline()    ✘
    getline      ✔

    var = getline()    ✘
    getline var        ✔

    getline(expr)      ✘
    getline <expr      ✔ Le symbole de redirection est nécessaire pour qu'il n'y ait pas de confusion
                         avec la syntaxe `getline var`. On peut aussi expliquer le choix de ce symbole
                         par le fait qu'on change l'argument par défaut de `getline`, à savoir l'input
                         d'origine: on redirige l'entrée de `getline` vers la valeur d'une expression.

---

Une fois  `getline` exécutée,  en fonction  de la  syntaxe utilisée,  awk peuple
certaines variables internes:

    ┌─────────────────────┬────────────────────────┬──────────────────────────┐
    │ syntaxe awk         │ variables mises à jour │ syntaxe VimL équivalente │
    ├─────────────────────┼────────────────────────┼──────────────────────────┤
    │ getline             │      $0, NF, NR, FNR   │                          │
    │                     │                        │                          │
    │ getline var         │ var        , NR, FNR   │ let var = getline()      │
    ├─────────────────────┼────────────────────────┼──────────────────────────┤
    │ getline <expr       │      $0, NF            │ getline(expr)            │
    │ "cmd" | getline     │      $0, NF            │ getline(system('cmd'))   │
    │                     │                        │                          │
    │ getline var <expr   │ var                    │ let var = getline(expr)  │
    │ "cmd" | getline var │ var                    │ let var = system('cmd')  │
    └─────────────────────┴────────────────────────┴──────────────────────────┘

Qd on utilise une syntaxe peuplant `$0`, awk divise le nouveau record en champs,
auxquels on peut accéder via `$i`.
Dans ce cas, l'ancien record (celui qu'awk était en train de traiter) n'est plus
dispo.

On remarque 2 choses:

   1. Les syntaxes stockant dans une variable le nouveau record lu, ne mettent
      pas à jour `$0`, ni `$i`. Ça  paraît logique:  si on  le stocke  dans une
      variable,  c'est sans  doute car  on est intéressé par son ensemble et non
      certains de ses champs.

      En plus, ça permet de préserver les informations du record courant.
      Si cette  syntaxe mettait à  jour `$0` et  `$i`, on aurait  aucune syntaxe
      nous permettant  d'utiliser `getline` tout  en continuant de  manipuler le
      record courant.

   2. Les syntaxes qui lisent  depuis un fichier ou un pipe ne mettent pas
      à jour NR, ni FNR. Ça paraît logique:  si NR et FNR était  incrémenté, awk
      sauterait un record  au sein de l'input d'origine.

`getline` est  pratique qd on a  du mal à décrire  le record sur lequel  on veut
agir, mais qu'on peut facilement décrire celui qui le précède.

---

Tout comme `next`, `getline` peut provoquer la lecture du prochain record.
La différence  vient du  fait que  `next` repositionne  l'exécution au  début du
programme, pas `getline`.
IOW,  une fois  `getline` exécutée,  awk ne  compare pas  le nouveau  record aux
patterns des précédents couples pattern-action qu'il a déjà traité.

Analogie pour mieux comprendre:

Sur un chronomètre, l'aiguille des  minutes représente la boucle principale d'un
programme awk, celle qui traite les records de l'input.
L'aiguille des  secondes représente la  boucle secondaire, celle qui  traite les
couples pattern-action du programme.
`next` et `getline` font avancer l'aiguille des minutes d'un cran (!).
Mais seule `next` repositionne l'aiguille des secondes sur 12h.

(!) `getline` ne fait pas avancer l'aiguille  des minutes si elle lit un fichier
ou un pipe.

---

    print "Enter your name: "
    getline var <"-"

Demande à l'utilisateur de taper son nom, et stocke la réponse dans `var`.

Illustre que dans les syntaxes:

    getline <expr
    getline var <expr

... `expr` peut être "-". Et que "-" désigne le clavier.

---

    "whoami" | getline        "whoami" | getline me
    print                     print me

Affiche `username` (ex: toto), dans les 2 cas.

Mais la sortie  de la commande shell  `whoami` peuple $0 uniquement  dans le 1er
exemple.

### Internes

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
    │ length(s)              │ retourne le nb de caractères au sein de `s`                                 │
    │                        │ sans `s`, `length()` retourne la longueur du record courant                 │
    ├────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
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
pattern matché.
Et, comme  dans Vim, on  peut lui  faire perdre son  sens spécial en  le quotant
(`\&`).

On peut aussi utiliser `\0`.

### Utilisateur

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


La  définition d'une  fonction doit  se  faire à  l'extérieur d'une  déclaration
pattern-action.
C'est  logique, car  définir une  fonction dans  une déclaration  pattern-action
impliquerait qu'elle n'est pas dispo tant que le pattern n'a pas été matché.


On peut séparer `myfunc` de la parenthèse ouverte, dans sa définition:

    function myfunc (parameter-list)    ✔

... mais pas qd on l'appelle ensuite:

    myfunc (parameter-list)    ✘

---

    function myfunc(a) {             function myfunc(b) {
        a = a 42                         b[1] = b[1] 42
    }                                }

    BEGIN {                          BEGIN {
        a = "foo"                        b[1] = "foo"
        myfunc(a)                        myfunc(b)
    }                                }
    END { print a }                  END { print b[1] }
          │                                │
          └ affiche "foo"                  └ affiche "foo42"


Les 2 codes appellent une fonction similaire `myfunc()`.
Celui de gauche affiche "foo", celui de droite "foo42".

À gauche, `myfunc()` n'a pas modifié la  variable globale `a` qu'on lui a passée
et qu'on avait initialisée dans une déclaration BEGIN.
En revanche, à droite,  elle a modifié le 1er élément  de l'array `b`, lui-aussi
initialisé dans une déclaration BEGIN.

Illustre qu'awk passe les SCALAIRES par valeur, et les ARRAYS par référence.

---

    function myfunc() {             function myfunc(string) {
        string = "hello"                string = "hello"
    }                               }

    BEGIN {                         BEGIN {
        myfunc()                        myfunc()
    }                               }
    END { print string }            END { print string }
          │                               │
          └ affiche "hello"               └ n'affiche rien

À  gauche, l'appel  à `myfunc()`  dans la  déclaration BEGIN,  crée la  variable
globale `string` en lui donnant pour valeur "hello".
À droite, ce même appel ne crée aucune variable globale.

Pk?

Car à droite `myfunc()` est définie  avec le paramètre `string`, ce qui implique
qu'au sein de la fonction, `string` est une variable locale.
En revanche,  à gauche, `myfunc()`  n'est définie  avec aucun paramètre,  ce qui
implique qu'au sein de la fonction, `string` est une variable globale.


La différence par rapport à VimL vient du code de gauche.
En VimL, qd on crée une variable dans une fonction, par défaut elle est locale.
En awk, elle est globale.

De plus,  en VimL,  une fonction se  plaint si on  l'appelle en  lui fournissant
moins d'arguments que le nb de paramètres dans sa définition.
En awk, aucun pb: les variables sont automatiquement initialisées à "".

---

                        ┌ surplus d'espaces conventionnels:
                        │ à gauche paramètres "réelles", à droite variables locales
                        │
    function reverse(x,   temp) {
        temp = x[1]
        x[1] = x[2]
        x[2] = temp
    }

    BEGIN {
        a[1] = "hello"
        a[2] = "world"
        reverse(a)
    }
    END { print a[1], a[2], print temp }
    "world hello"~

La fonction custom `reverse()` inverse les 2 premiers éléments d'une array.
Pour ce faire, elle utilise la variable temporaire `temp`.
Après avoir appelé `reverse()`, aucune variable globale `temp` n'a été créée.

Illustre  le mécanisme  à  utiliser pour  fournir des  variables  locales à  une
fonction:

qd on définit une fonction à laquelle  on veut fournir des variables locales, il
faut déclarer leurs noms (ex: `temp`) dans la liste de ses paramètres.
Généralement,  on  les  déclare  à  la fin,  après  les  paramètres  qu'on  veut
réellement lui passer (ex: `a`).

Par la  suite, qd on appelle  la fonction, on  peut lui passer des  valeurs pour
initialiser ces variables locales, ou bien les omettre.
Si on les omet, awk les initialise en leur donnant pour valeur "".


On remarque que, par convention, on  sépare les variables locales des paramètres
"réels" avec plusieurs espaces.

---

    { printf("%-10s %20s\n", $0, new_feature($0)) }

Illustre  comment  développer  une  nouvelle fonctionnalité  pour  un  programme
existant.

Cette déclaration affiche pour chaque record, le champ d'origine, et une version
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
l'exécution d'un programme awk; `-F<fs>` ne permet de configurer que FS.

---

    $ awk -f progfile f1 FS=: f2

Traite le  fichier `f1` avec FS  ayant sa valeur  par défaut (" "),  puis traite
`f2` avec FS ayant pour valeur `:`.

Plus généralement,  on peut  configurer une variable  juste avant  le traitement
d'un fichier arbitraire, via la syntaxe:

    $ awk -f progfile f1 var=val f2

---

    $ awk 'pattern { action }'                file
    $ awk 'pattern { action1; action2; ... }' file
    $ awk 'statement1; statement2; ...'       file

Demande à awk d'exécuter:

   - `action`                      sur les lignes de `file` matchant `pattern`
   - `action1`, `action2`, ...       "
   - `statement1`, `statement2`, ...

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
Pour  chacun  d'eux, il  exécute  toutes  les déclarations  pattern-action  pour
lesquelles le pattern matche.

IOW,  awk  itère  d'abord  sur  les   records,  et  seulement  ensuite  sur  les
déclarations pattern-action.

---

    $ awk 'statement' file1 file2

Traite  les fichiers  `file1`  et  `file2` en  exécutant  le  code contenu  dans
`statement`; illustre que l'input n'est pas limité à un fichier.

## Terminaisons de commande

    statement1                       ⇔    statement1; statement2
    statement2

    pattern { action1; action2 }    ⇔    pattern {
                                             action1
                                             action2
                                         }

On peut *terminer*  une déclaration pattern-action ou une action  via un newline
ou un point-virgule.

On utilisera plutôt un  newline dans un fichier awk, et  un point-virgule sur la
ligne de commande.

Un newline  peut aussi servir à  *décomposer* une expression ou  une déclaration
sur plusieurs lignes; pour ce faire, il doit être placé après :

    ┌───────────────────────┬───────────┐
    │ une virgule suivant   │ print $1, │
    │ un argument           │       $2  │
    ├───────────────────────┼───────────┤
    │ un backslash          │ print \   │
    │ positionné où on veut │       $1, │
    │                       │       $2  │
    ├───────────────────────┼───────────┤
    │ un opérateur logique  │ 1 &&      │
    │                       │ 2         │
    └───────────────────────┴───────────┘

---

    printf(\
        "%10s %6s %5s   %s",
        "COUNTRY",
        "AREA",
        "POP",
        "CONTINENT\n\n"\
        )

Dans  cet exemple,  on décompose  une action  `printf()` en  utilisant plusieurs
newlines;  certains  sont positionnés  après  un  backslash, d'autres  après  un
argument et une virgule.

---

    {
        print \
              $1,    # middle of action
              $2,    # "
              $3,    # after action
    }                # after statement

On peut commenter n'importe quelle fin de ligne.
Qu'il s'agisse  de la fin d'une  déclaration pattern-action, d'une action  ou au
sein même d'une action.

Décomposer son code sur plusieurs lignes permet de :

   - mieux le documenter
   - gagner en lisibilité


On peut décomposer une action `if`, `for`, `while` en plaçant un newline:

    ┌────────────────────────────────────────────────┬───────────────────────────────┐
    │ après son expression `(e)`                     │ if (e) s            ⇔  if (e) │
    │                                                │                            s  │
    ├────────────────────────────────────────────────┼───────────────────────────────┤
    │ après ou avant le mot-clé `else` ou `else if`  │ if (e) s1; else s2  ⇔  if (e) │
    │                                                │                            s1 │
    │                                                │                        else   │
    │                                                │                            s2 │
    ├────────────────────────────────────────────────┼───────────────────────────────┤
    │ après chacune de ses déclarations (`s1`, `s2`) │ if (e) { s1; s2 } else s3     │
    │ à condition qu'elles soint encadrées par       │             ⇔                 │
    │ des accolades                                  │ if (e) {                      │
    │                                                │     s1                        │
    │ sans les accolades, le newline après `s1`      │     s2                        │
    │ serait interprété comme la fin du bloc `if`    │ }                             │
    │ au lieu de la fin de `s1`                      │ else                          │
    │                                                │     s3                        │
    │ par conséquent, `s2` serait exécutée           │                               │
    │ peu importe la valeur de `e`                   │                               │
    └────────────────────────────────────────────────┴───────────────────────────────┘

## Opérateurs

Il existe 5 petits ensembles d'opérateurs:

    ┌──────────────────────────┬───────────┐
    │         ensemble         │ éléments  │
    ├──────────────────────────┼───────────┤
    │ groupage                 │ ()        │    Le groupage permet de donner la priorité à une opération
    │                          │           │    arbitraire.
    │ champs                   │ $         │
    │                          │           │
    │ concaténation            │ implicite │
    │                          │           │
    │ appartenance à une array │ in        │
    │                          │           │
    │ conditionnel             │ ?:        │
    └──────────────────────────┴───────────┘

... et 6 grands:

    ┌───────────────────────────────┬──────────────────────┐
    │           ensemble            │       éléments       │
    ├───────────────────────────────┼──────────────────────┤
    │ incrémentation/décrémentation │ ++ --                │
    │                               │                      │
    │ arithmétique                  │ + - * / % ^          │
    │                               │                      │
    │ comparaison                   │ < <= == != >= > ~ !~ │
    │                               │                      │
    │ logique                       │ ! && ||              │── Ordre de priorité:    ! > && > ||
    │                               │                      │
    │ affectation                   │ = += -= *= /= %= ^=  │
    │                               │                      │
    │ expression régulière          │ ()  []  ?*+  ∅  |    │
    └───────────────────────────────┴──────────────────────┘
                                                |
                                                |

                        Ordre de priorité:  () > [] > ?*+ > ∅ > |
                                            │    │    │     │
                                            │    │    │     │   └ alternation
                                            │    │    │     └ concaténation
                                            │    │    └ répétition
                                            │    └ collection
                                            └ groupage + capture

---

    7-4+2    =    (7-4)+2

Tous les  opérateurs sont associatifs  à gauche,  ce qui signifie  que lorsqu'il
faut évaluer une expression contenant 2 opérateurs de même priorité, l'opérateur
de gauche est traité en premier.

Il existe 3 types d'opérateurs qui font exception à cette règle:

   - affectation
   - conditionnel
   - exponentiel

Ces derniers sont associatifs à droite.
Ex:

    2^3^4    =    2^(3^4)


L'associativité  à  droite  des  opérateurs  d'affectation  permet  le  chaînage
d'affectations:

    var1 = var2 = val    ⇔    var1 = (var2 = val)
    │       │
    │       └ expression retournant `val`,
    │         et affectant `val` à `var2`
    │
    └ expression retournant `val`, et affectant `val` à `var1`

---

    ab?
    (ab)?

Matche 'a' ou 'ab', car on répète (`?`) puis on concatène.
Matche 'ab' ou '' , car on concatène puis on répète


Dans une  expression régulière ou  non, pour donner  la priorité à  un opérateur
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

        `expr1` FAUX ⇒ `expr1 && expr2` FAUX (peu importe la valeur de vérité de
        `expr2`) `expr3` VRAI ⇒ `expr3 || expr4` VRAI (" `expr4`)


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

---

    if ((n = length($1)) > 0) print

Affecte à la variable `n` la longueur du 1er champ, et en même temps teste si ce
dernier est non vide.

Illustre  que `var  = expr`  est une  expression dont  la valeur  est la  valeur
affectée à la variable.
Ici l'expression `n = length($1)` a pour valeur `length($1)`.

---

    FS = OFS = "\t"
    a = b = 42

Affecte:

   - la chaîne "\t" aux variables internes     FS et OFS
   - le nombre `42` aux variables utilisateurs `a`  et `b`

Illustre qu'on peut réaliser plusieurs affectations en une seule ligne.

## Pattern

Un pattern peut être:

   - BEGIN, END, BEGINFILE, ENDFILE

   - une expression, régulière (/pattern/) ou non

   - une rangée        expr1,expr2
                       /pattern1/,/pattern2/

Qd le pattern est  une expression, il y a match si son  évaluation est un nombre
non nul, ou une chaîne non vide.

---

    BEGIN
    END

Sélectionne le record imaginaire précédant le 1er      record de l'input.
"                                suivant   le dernier  "

Permet d'exécuter une action avant / après que l'input ait été traité.


Ces  patterns spéciaux  sont les  seuls  pour lesquels  on ne  peut pas  omettre
l'action.
De plus, on ne peut pas les combiner avec d'autres patterns.
Ex:

                    /Susie/,END    ✘


BEGINFILE fonctionne de manière similaire,  sauf qu'il sélectionne le 1er record
imaginaire précédant le 1er record de CHAQUE FICHIER de l'input.

Même chose pour ENDFILE (après le dernier record de chaque fichier de l'input).

---

    Sélectionne les records tq:

    ┌─────────────────┬───────────────────────────────────────────────────────────────────┐
    │ $3 == 0         │ le 3e champ est nul                                               │
    │                 │                                                                   │
    │ $2 >= 5         │ le 2e est supérieur à 5                                           │
    │                 │                                                                   │
    │ $2 * $3 > 50    │ le produit des champs 2 et 3 est > 50                             │
    │                 │                                                                   │
    │ NF != 3         │ le nb de champs est différent de 3                                │
    │                 │                                                                   │
    │ NR == 10        │ l'index du record est 10                                          │
    │                 │                                                                   │
    │ $0 >= "M"       │ le record est rangé après le caractère M                          │
    │                 │                                                                   │
    │ $1 == "Susie"   │ le 1er champ est "Susie"                                          │
    ├─────────────────┼───────────────────────────────────────────────────────────────────┤
    │ expr ~ /pat/    │ `pat` décrit une sous-chaîne de `expr`                            │
    │                 │ la valeur de `expr` étant une chaîne, ou un nb converti en chaîne │
    │                 │                                                                   │
    │ expr !~ /pat/   │ `pat` ne décrit aucune sous-chaîne de `expr` (aucun match)        │
    │                 │                                                                   │
    │ $0 ~ /pat/      │ `pat` décrit une sous-chaîne du record                            │
    │      /pat/      │ on dit que le pattern “matche“ le record                          │
    │                 │                                                                   │
    │ $0 ~ expr       │ `expr` décrit une sous-chaîne du record                           │
    │                 │                                                                   │
    │                 │ la valeur de `expr` est interprétée comme une pat, et,            │
    │                 │ si besoin convertie en chaîne                                     │
    └─────────────────┴───────────────────────────────────────────────────────────────────┘


Les dernières syntaxes sont toutes des cas particuliers de la syntaxe générale:

    expr ~ expr


Le rhs de `~` est toujours interprété comme une pat, et le lhs comme un pattern.
Ça implique que:

    "Hello" ~ "Hel.o"    ✔ il y a match, car `.` est interprété comme un métacaractère
    "Hel.o" ~ "Hello"    ✘ pas de match, car `.` est interprété littéralement


On peut abréger `$0 ~ /pat/` en `/pat/`, mais pas `$0 ~ expr` en `expr`.

---

    /pat1/ && !/pat2/

Sélectionne les records décrit ou `pat1` matche mais pas `pat2`.

Illustre  qu'on peut  combiner des  expressions régulières  avec des  opérateurs
logiques (ici &&).
Montre aussi qu'on peut abréger `$0 !~ /pat/` en `!/pat/`.

---

    BEGIN {
        sign     = "[-+]?"
        decimal  = "[0-9]+[.]?[0-9]*"
        fraction = "[.][0-9]+"
        exponent = "[eE]" sign "[0-9]+"
        number   = "^" sign "(" decimal "|" fraction ")(" exponent ")?$"
    }

    $1 ~ number

Affiche  les records  dont le  1er  champ est  un nombre  entier (123),  décimal
(1.23),  ou  une  fraction   (.123),  accompagné  éventuellement  d'un  exposant
(123e456).

Illustre  qu'on   peut  décomposer  un   pattern  de  regex  complexe   via  une
concaténation de chaînes.
Fonctionne pour 2 raisons:

   - le rhs de l'opérateur `~` peut être une expression
   - une concaténation de chaînes est une expression

---

    $2 >= 4 || $3 >= 20
    !($2 < 4 && $3 < 20)

Sélectionne les records tq le 2e champ est supérieur à 4 OU le 3e à 20.


    (1)    (A ou B) est vraie,  ssi (A ou B)         n'est pas fausse.
    (2)    (A ou B) est fausse, ssi (non A ET non B) est vraie.

    (1) ∧ (2)    ⇒    (A ou B) est vraie, ssi (non A ET non B) est fausse.

---

    expr1,expr2

Sélectionne les records qui se situent entre  un record où `expr1` est vraie, et
le suivant où `expr2` est vraie.
Ex:

    FNR == 1, FNR == 5    ⇔    FNR <= 5

---

    /pattern1/,/pattern2/

Sélectionne tous  les records qui  se situent qq  part entre un  record matchant
`pattern1` (notons le R1), et le prochain record après R1 matchant `pattern2`.

On  parle de  “rangée“, et  comme pour  une rangée  dont les  adresses sont  des
patterns dans  une commande Ex Vim,  elle peut matcher plusieurs  successions de
records distinctes.

Ex:

                                      ┌───────┐
    awk '/foo/,/bar/ { print }' file ─│ foo   │
                                      │ word1 │
            foo                       │ bar   │
            word1                     │       │
            bar                       │ one   │
            foo                       │ two   │
            word2                     │       │
            bar                       │ foo   │
                                      │ word2 │
                                      │ bar   │
                                      └───────┘

Si aucun record ne matche:

   - `pattern1`, la rangée est vide

   - `pattern2`, la rangée inclut tous les records depuis celui où `pattern1` a été
     trouvé pour la dernière fois, jusqu'à la fin du fichier

Il s'agit d'une forme abrégée de:

    $0 ~ /pattern1/,$0 ~ /pattern2/

... qui est un cas particulier de:

    expr1,expr2

---

    $ cat progfile

            $2 >= 4
            $3 >= 20

    $ awk -f progfile

    !=

    $ awk '$2 >= 4 || $3 >= 20'

Les 2 pgms ne sont pas équivalents.
Lorsqu'un record satisfait les 2 conditions, il est affiché:

   - 2   fois par le 1er pgm
   - une fois par le 2e  pgm

En effet, le 1er pgm contient 2 déclarations constituées chacune d'un pattern et
d'une action, tandis que le 2e programme ne contient qu'une seule déclaration.
Ici, les actions sont implicites (`{ print }`).

##
## Variables
### Validité des noms / valeurs

Il existe 3 types de variables:

   - définie par l'utilisateur (ex: myvar)
   - interne                   (ex: ARGV)
   - variable de champ         (ex: $1)

Le nom d'une variable utilisateur ne  peut contenir que des lettres, chiffres et
underscores; elle ne doit pas commencer par un chiffre.
Le nom d'une variable interne n'utilise que des lettres majuscules.

La valeur d'une variable est une chaîne ou une constante numérique.
Par défaut, une  variable non initialisée vaut  "", ce qui implique  qu'il n'y a
jamais besoin d'initialiser une variable avec les valeurs suivantes:

    myvar = ""    ✘ fonctionne mais inutile
    myvar = 0     ✘ idem, car "" peut être convertie en 0 (`print i + 1` affiche 1)

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

#### ARGC, ARGV

          ┌─────────────────────────────┐
          │ BEGIN {                     │
          │     FS      = ":"           │
          │     ARGV[1] = "/etc/passwd" │
          │     ARGC   += 1             │
          │ }                           │
          │ { print $2, $4, $6 }        │
          └─────────────────────────────┘
               │
               v
    awk -f progfile

Affiche les champs 2, 4 et 6 de `/etc/passwd`.

La déclaration `ARGC += 1` est nécessaire.
Sans elle, awk n'ajouterait pas `/etc/passwd` à son input.
En effet, il lit les éléments de ARGV uniquement jusqu'à l'index `ARGC - 1`.
Or, ici, ARGC = 1, donc `ARGC - 1 =  0` et awk ne lit que le 1er élément de ARGV
('awk').

Illustre que  pour accroître l'input,  il ne suffit  pas d'ajouter un  élément à
ARGV, il faut aussi incrémenter ARGC.

---

    BEGIN { ARGV[2] = "" }
      ou
    BEGIN { delete ARGV[2] }

Supprime le 2e fichier de l'input.

Qd awk  rencontre une chaîne  vide dans ARGV, il  passe au prochain  élément, et
continue jusqu'au `(ARGC-1)`ième.

Illustre qu'en changeant le contenu de  ARGV dans une déclaration BEGIN, on peut
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
`42` par la valeur spéciale "-".


Si awk ne reçoit aucun fichier en argument, dit autrement si ARGV n'a qu'un seul
élément (ARGC = 1, ARGV[0] = 'awk'), il lit automatiquement son entrée standard,
qui est connectée soit au clavier soit à un pipe.

#### FS, RS, OFS, ORS, NR

    BEGIN { FS = "\t" }
          { print $1 }

Modifie la  valeur de FS pour  tous les records,  en lui donnant pour  valeur un
tab.

Modifier FS n'affecte pas la définition des champs du record courant, uniquement
ceux des records qui suivent.

Si on veut modifier  la définition des champs de tous les  records, y compris le
1er, il faut donc modifier FS via le pattern BEGIN.

---

    NR == 5 { NR = 10 }
            { print NR }

Ce code modifie l'index du 5e record, en lui donnant pour valeur 10.
Les records suivants auront donc pour index 11, 12, ... au lieu de 6, 7, ...

Illustre qu'on peut accéder en écriture  à certaines variables internes, dont NR
et FS.
Exception: FILENAME n'est pas accessible en écriture.

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


Dans  cet  exemple, la  valeur  de  FS est  interprétée  comme  une regex  "\\."
décrivant un point littéral.
Plus généralement, les valeurs de FS et  RS sont interprétées comme des regex si
elles contiennent plusieurs caractères, autrement littéralement:

                    FS = "\\."    ⇔    FS = "."
                    RS = "\\."    ⇔    RS = "."

Les valeurs de OFS et ORS sont toujours littérales.

---

    BEGIN { RS = "_"; ORS = "|" }
          { print }

Effectue la transformation suivante:

    I_like_old_things.    →    I|like|old|things.
    |

Illustre que le remplacement de RS par ORS est automatique et inconditionnel.


On remarque un pipe sous le I, sur une 2e ligne.
awk considère qu'il y a un “record terminator“ (RT) entre 2 records consécutifs,
mais aussi après le dernier record.
RT est décrit par le caractère / la regex contenu(e) dans RS.

Sur le dernier record d'un input, RT = "" peu importe la valeur de RS.
awk remplace le dernier RT ("") par ORS.

FIXME:

Par contre,  pourquoi awk  semble ajouter  un newline  après le  dernier record,
alors que ORS n'en contient pas:

    I|like|old|things.    vs   I|like|old|things.|
    |

Peut-être car il y a toujours un newline à la fin d'un fichier / ou de la sortie
d'une commande shell.

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

En plus de 'foo', 'bar' et 'baz', awk divise le début du record '::' en 2 champs
vides, et la fin ':' en un champ vide.

Plus généralement, qd awk divise un record, il génère un champ vide:

   - s'il rencontre 2 délimiteurs consécutifs
   - si le début du record commence par un délimiteur
   - si la fin du record se termine par un délimiteur


Exception:

Qd FS = " ", awk ignore les espaces et tabs au début et à la fin d'un record.
" " n'est pas un simple espace, c'est une valeur spéciale pour FS.

---

    BEGIN { RS = "" }

"" est une valeur spéciale pour RS.
awk semble l'interpréter comme "\n+".

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

    awk 'END { print ($1 < $2) }' <<< "31 30"
    0~
    awk 'END { print ($1 < $2) }' <<< "31 3z"
    1~

Ces 2 commandes  illustrent que lorsqu'un champ est numérique,  awk affecte à la
variable correspondante une valeur numérique et une valeur chaîne.

En effet,  dans la 1ère  commande, le  test est négatif,  ce qui prouve  que les
valeurs de $1 et $2 étaient des nombres, et pas des chaînes.
Dans la  2e commande, le test  est positif, ce  qui prouve que, cette  fois, les
valeurs sont des chaînes.

Qd l'opérateur de comparaison travaille sur  des opérandes dont au moins une des
valeurs est numérique, il fait une comparaison numérique (commande 1).

Mais, si l'un des opérandes n'a aucune valeur numérique, il fait une comparaison
de chaînes, quitte à faire une coercition si besoin.
C'est ce  qui se  passe dans la  commande 2, où  le 2e  champ n'a pas  de valeur
numérique (`3z`).

---

    $2 = ""; print

Affiche les records en effaçant le 2e champ.

Illustre qu'on  peut se servir  de la variable  `$<nb>` pour changer  le contenu
d'un champ.


Plus  généralement, une  même  expression nous  permet d'accéder  à  la fois  en
lecture et en écriture à certaines variables ($1, NR, ...).
Certaines, pas toutes.
On ne peut pas modifier FILENAME.

Pour rappel, on accède à une variable en:

   - écriture qd elle se trouve dans le côté gauche de l'affectation
   - lecture  "                              droit  "

---

    !$1
    ($1)++

Inverse (au sens logique) / Incrémente la valeur du 1er champ.

##
# Exercises

Print the total number of input lines.

    $ cat <<'EOF' >/tmp/awk.awk
    END { print NR }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print the tenth input line.

    $ cat <<'EOF' >/tmp/awk.awk
    NR == 10
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

No need to write `{ print }`. It's the default action.

---

Print the last field of every input line.

    $ cat <<'EOF' >/tmp/awk.awk
    { print $NF }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print the last field of the last input line.

    $ cat <<'EOF' >/tmp/awk.awk
        { last_field = $NF }
    END { print last_field }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print every input line with more than four fields.

    $ cat <<'EOF' >/tmp/awk.awk
    NF > 4
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print every input line in which the last field is more than `4`.

    $ cat <<'EOF' >/tmp/awk.awk
    $NF > 4
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print the total number of fields in all input lines.

    $ cat <<'EOF' >/tmp/awk.awk
        { total += NF }
    END { print total }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print the total number of lines that contain `Beth`.

    $ cat <<'EOF' >/tmp/awk.awk
    /Beth/ { total += 1 }
    END    { print total }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print the largest first  field and the line that contains  it (assumes some `$1`
is positive).

    $ cat <<'EOF' >/tmp/awk.awk
    $1 > max { max = $1 ; line = $0 }
    END      { print max, line }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print every line that has at least one field.

    $ cat <<'EOF' >/tmp/awk.awk
    NF >= 1
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print every line longer than 80 characters.

    $ cat <<'EOF' >/tmp/awk.awk
    length($0) > 80
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print the number of fields in every line followed by the line itself.

    $ cat <<'EOF' >/tmp/awk.awk
    { print NF, $0}
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print the first two fields, in opposite order, of every line.

    $ cat <<'EOF' >/tmp/awk.awk
    { print $2, $1 }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Exchange the first two fields of every line and then print the line.

    $ cat <<'EOF' >/tmp/awk.awk
    { temp = $1; $1 = $2; $2 = temp; print }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print every line with the first field replaced by the line number.

    $ cat <<'EOF' >/tmp/awk.awk
    { $1 = NR; print }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print every line after erasing the second field.

    $ cat <<'EOF' >/tmp/awk.awk
    { $2 = ""; print }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print in reverse order the fields of every line.

    $ cat <<'EOF' >/tmp/awk.awk
    {
        for (i = 1; i <= $NF; i++) {
            printf("%s ", $i)
        }
        print ""
    }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print the sums of the fields of every line.

    $ cat <<'EOF' >/tmp/awk.awk
    { sum = 0; for (i = 1; i <= NF; i++) sum += $i; print sum }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Add up all fields in all lines and print the sum.

    $ cat <<'EOF' >/tmp/awk.awk
        { for (i = 1; i <= NF; i++) sum += $i }
    END { print sum }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

---

Print every line after replacing each field with its absolute value.

    $ cat <<'EOF' >/tmp/awk.awk
    { for (i = 1; i <= NF; i++) if ($i < 0) $i = -$i; print }
    EOF

    $ awk -f /tmp/awk.awk /tmp/emp.data

##
# TODO

Write a `|c` mapping to lint the current awk script (using `--lint`).

---

<https://www.gnu.org/software/gawk/manual/html_node/Debugger.html>

