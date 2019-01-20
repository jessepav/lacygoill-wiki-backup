# How to get the number of occurrences of a character in a string?

Use `count()`:

    let str = 'hello'
    echo count(str, 'l')
    2~

The `l` character is present twice in the string `hello`.

# How to make Vim translate special sequences such as `\<tab>` or `\x26` in a literal string?

Concatenate double quotes at the beginning and end of the string.
Then use `eval()`.

    let string = 'foo \x26 bar' | echo eval('"'.string.'"')
    foo & bar~

    let string = 'foo\<tab>bar' | echo eval('"'.string.'"')
    foo    bar~

---

`eval()` expects a string as argument.
`"string"` is *still* a string, so our concatenations didn't cause an issue.

`eval()` looks at what is inside its string argument, and evaluate it.
For example, if it was `&ft`, it would return `markdown`.

Here, it finds `"string"`, so it  returns the evaluation of `"string"`, which is
the same string, but with the special characters translated.

##
# Does the second argument of `execute()` has an influence on
## the evaluation of the first argument?

Yes.
It can be used to prevent Vim from printing any message:

    :call execute('echom "hello"')
    ∅~
    :call execute('echom "hello"', 'silent')
    ∅~
    :call execute('echom "hello"', 'silent!')
    ∅~

    :echo execute('echo "hello"')
    :echo execute('echo "hello"', 'silent')
    :echo execute('echo "hello"', 'silent!')
    hello~

## the output of `execute()`?

Most of the time, no.

However, there's one exception.
If you use `silent!`, the error messages won't be included in the output.

    echo execute('abcd', 'silent!') is# ''
    1~

##
# How to eliminate the newline at the beginning of `execute('ls')`?

    echo execute('ls')[1:]

##
# How is a negative index argument interpreted by a function handling a string?

`0`

##
# I have a string and a pattern.  How to get the list of substrings matching the capturing groups?

Use `matchlist()`:

    echo matchlist(str, pat)

---

    echo matchlist('abcd', '\v(.(.))(.)')
    ['abc', 'ab', 'b', 'c', '', '', '', '', '', '']~
      │      │     │    │
      │      │     │    └ \3
      │      │     └ \2
      │      └ \1
      └ \0

##
##
##
# ?

Similitudes et différences entre `match()` et `matchstr()`:

   • elles acceptent 1 ou 2 arguments optionnels (`start`, `count`):

       - `start` = où commencer à chercher

       * index d'item pour une liste

       * index du 1er octet à partir duquel chercher pour une chaîne

       - `count` = cherche le `count`-ième match

   • `match()`    retourne un index (d'octet au sein d'une chaîne, d'item au sein d'une liste)
     `matchstr()` "        une sous-chaîne

# ?

    echo match('Starting point', 'start')
    0~
    echo stridx('Starting point', 'start')
    -1~

Qd on leur passe une chaîne  en 1er argument, `match()` et `stridx()` retournent
l'index de l'octet précédant la sous-chaîne passée en 2e argument.

Si elles retournent:

   • `0`   ça signifie que  la sous-chaîne a été trouvée au tout début
   • `-1`  ça signifie que  la sous-chaîne est absente

# ?

    echo match('testing', 't', 2)
    3~

Retourne `3`  (et non pas  `0`) car le 3e  argument optionnel indique  ici qu'il
faut commencer à chercher à partir du 2e octet.

# ?

                                    ┌ cherche à partir de l'octet d'index 1 (le deuxième_)
                                    │  ┌ cherche la 2e occurrence
                                    │  │
    echo match('testing this', 't', 1, 2)
    8~

# ?

    echo matchstr('testing', 'ing', 5)
    ''~

Return an  empty string  because `ing`  can't be found  in `testing`  beyond the
fifth byte.

##
##
##
# ?

Différences entre `match()` et `stridx()`:

   • `match()`  peut travailler sur une liste de chaînes
     `stridx()` uniquement sur une chaîne

   • `match()`  cherche un pattern
     `stridx()` "       une chaîne littérale

   • `match()`  et `stridx()` acceptent un 3e argument optionnel {start}
      mais seule `match()` accepte un 4e argument optionnel {count}

   • `match()`  respecte `'ignorecase'` (sauf si on utilise `\c` ou `\C`), mais pas `'smartcase'`
     `stridx()` est toujours sensible à la casse

`match()`  respecte `'ignorecase'` (sauf si on utilise `\c` ou `\C`), mais pas `'smartcase'`

# ?

Différences entre `match()` et `count()`:

   • `count()` peut travailler sur une chaîne ou une liste de chaînes (comme
     `match()`), mais aussi sur (les valeurs d')un dictionnaire

   • `count()` cherche  une chaîne littérale (==#)
     `match()` "        un pattern           (=~#)

     que ce soit au sein d'une chaîne ou d'une liste de chaînes

   • `count()` retourne des nombres d'occurrences
     `match()` des index d'octets ou d'items

   • `count()` respecte toujours la casse sauf si on lui passe un 3e argument optionnel non-nul
     `match()` respect 'ic'

   • pour `count()` 2 occurrences d'un pattern au sein d'une chaîne ne peuvent pas avoir de partie commune
     pour `match()` elles peuvent, ce qui fait une différence pour le 4e argument optionnel

   • pour `count()` les arguments optionnels sont 'ic' puis {start}
     pour `match()` ce sont {start} puis {count}

# ?

    echo match('An Example', 'Example')
    echo stridx('An Example', 'Example')
    3~

# ?

    echo stridx('foo:bar:baz', ':')
    3~
    echo stridx('foo:bar:baz', ':', 3 + 1)
    7~

# ?

    echo matchstr(getline('.'), '\%'.col('.').'c...')

Les 3 caractères après le curseur.

`col('.')` retourne l'index du 1er octet du caractère suivant le curseur.
Donc, si le curseur  est juste avant le caractère dont le 1er  octet est le 10e,
le pattern recherché est `\%10c...`.

`\%10c` est un atome  de largeur nulle / une ancre qui indique  que le 1er octet
du caractère suivant a pour index `10`.
Si aucun des 9 premiers caractères n'est  multi-octets, ça revient à dire que le
caractère suivant a pour index `10`.

`.` peut être n'importe quel caractère.
En supposant qu'il n'y a pas  de caractère multi-octets, `\%10c...` matchera les
caractères occupant les colonnes `10`, `11`, `12` sur la ligne.

# ?

Try to avoid `virtcol('.')`. It's not reliable.

You could be tempted to write this:

    strcharpart(getline('.'), virtcol('.') - 1, 3)

But sometimes it would not work.

To illustrate, write this sentence in `/tmp/file`:

    they would be useful if they were here

Then, start Vim like this:

    $ vim -Nu NONE +'norm! 13l' +'lefta 20vs | setl wrap lbr' /tmp/file
    :echo strcharpart(getline('.'), virtcol('.') - 1, 3)
    l SPC i~

You probably expected `SPC u s`.
The reason for this difference is explained in our notes about `virtcol()`.

Basically, if  there is a  column where no real  character resides in  the file,
between  2 other  columns where  there ARE  real characters,  the column  in the
middle is NOT ignored.

Although, I guess it's ok to use `virtcol()` when you're sure your lines are NOT
wrapped.

# ?

    echo matchstrpos('testing', 'ing')
    ['ing', 4, 7]~

'ing' est la sous-chaîne matchée par le pattern `ing`.
`4` est l'index de l'octet précédant le match.
`7` est l'index du dernier octet au sein du match.

# ?

`matchstrpos()` indexe un octet en commençant à compter à partir de 0.
Idem pour toutes  les fonctions acceptant en argument des  index d'octets (ou de
caractères),  comme  `match()`, `strcharpart()`,  ....  Idem  qd on  extrait  un
caractère d'une chaîne via un index:

    echo matchstrpos('abcdef', 'd')
    ['d', 3, 4]~
    echo match('abcdef', 'd')
    3~
    echo 'abcdef'[3]
    d~

`col('.')`  fait exception,  car  qd elle  exprime la  position  du curseur  via
l'index de l'octet qui le suit, elle commence à compter à partir de `1`.
De même, dans  un pattern de regex,  qd l'atome `\%123c` exprime  la position de
l'octet suivant, il commence à compter à partir de `1`.

# ?

    echo matchstrpos('testing', 'ing', 5)
    ['', -1, -1]~

Il n'y a pas de match au delà du 4e octet.

# ?

    echo matchstrpos([1, '__x'], '\a')
    ['x', 1, 2, 3]~

`1` est l'index du 1er item où le pattern `\a` match.
'x' est la sous-chaîne matchée.
`2` est l'index de l'octet précédant le match.
`3` est l'index du dernier octet au sein du match.

# ?

    echo nr2char(123)

Retourne le caractère n°123 dans  l'encodage défini par `'encoding'` (utf-8 chez
moi).

# ?

    ┌──────────────────────────────┬─────────────────────────────────────────────────────────────────┐
    │ split('foobarbaz', 'bar')    │ ['foo', 'baz']                                                  │
    ├──────────────────────────────┼─────────────────────────────────────────────────────────────────┤
    │ split('fooBARbaz', '\cbar')  │ ['foo', 'baz']                                                  │
    │                              │                                                                 │
    │                              │ La recherche du pattern est insensible à la casse grâce à `\c`. │
    │                              │ La valeur de 'ignorecase' est ignorée.                          │
    ├──────────────────────────────┼─────────────────────────────────────────────────────────────────┤
    │ split('foobarbaz', 'bar\zs') │ ['foobar', 'baz']                                               │
    │                              │                                                                 │
    │                              │ On cherche 'bar' mais on ne retient qu'à partir de ce qui suit. │
    │                              │ Et comme après on n'écrit rien après , rien n'est supprimé.     │
    ├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
    │ split('foobarbaz', '\zebar') │ ['foo', 'barbaz']                                                │
    ├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
    │ split(':a:b:c', ':', 1)      │ ['', 'a', 'b', 'c']                                              │
    │                              │                                                                  │
    │                              │ Le nb 1 passé en 3e argument demande à split() de conserver le   │
    │                              │ le 1er et dernier item s'ils sont vides.                         │
    │                              │                                                                  │
    │                              │ Une chaîne vide en 1er / dernier item signifie que le séparateur │
    │                              │ était présent au tout début / à la fin de la chaîne passée en    │
    │                              │ 1er argument à split().                                          │
    │                              │                                                                  │
    │                              │ Ça peut être utile pour reconstituer la chaîne d'origine:        │
    │                              │                                                                  │
    │                              │ join(split(':a:b:c', ':'), ':')       →    'a:b:c'     ✘         │
    │                              │ join(split(':a:b:c', ':', 1), ':')    →    ':a:b:c'    ✔         │
    ├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
    │ split(getline('.'), '\W\+')  │ la liste des MOTS de la ligne courante                           │
    └──────────────────────────────┴──────────────────────────────────────────────────────────────────┘

# ?

    echo '12' + 3
    15      ✔~

    echo '1.2' + 3
    4       ✘~

    echo str2float('1.2') + 3
    4.2     ✔~

La coercition  par défaut d'une  chaîne en nombre  est correcte pour  un entier,
mais pas pour un flottant; pour ce dernier, il faut invoquer `str2float()`.

# ?

    echo '010' + 1
    9~

    echo str2nr('010') + 1
    11~

Dans le 1er cas, le leading zero fait interpréter le nb comme étant octal (et 10
en base 8 = 8).
Cette  interprétation  peut   poser  problème,  notamment  qd   on  réalise  une
substitution et qu'on  utilise `submatch()` dans la chaîne  de remplacement pour
faire un calcul incluant un nb capturé dans le pattern.
En effet, dans ce  cas Vim va convertir la chaîne contenant le  nb capturé en un
nb en base 8.

`str2nr()` résoud ce pb.
Elle  convertit une  chaîne  en nb  et  peut prendre  un  2e argument  optionnel
correspondant à la base dans laquelle on veut que le nb soit interprété.
Sans ce 2e argument, elle utilise la base 10 par défaut.

# ?

    echo strdisplaywidth("\t", col('.')-1)

Retourne le  nb de  cellules qu'occuperait  un caractère  tab s'il  était inséré
après le curseur.

# ?

    echo strlen('exposé')
    7~
    echo strchars('exposé')
    6~

Retourne la longueur  en octets / caractères de la  chaîne `exposé` (`7` octets;
`6` caractères).

# ?

    echo strcharpart('résumé', 2, 1)
    s~
    echo strpart('résumé', 2, 1)
    <a9>~

Retourne une sous-chaîne de string, commençant après:

   • le 2e caractère et de longueur max 1
   • le 2e octet     et de poids    max 1

# ?

    :echo strcharpart('abcdefg', -2, 4)
    ab~

caractère d'index -2 = '' (car n'existe pas)
caractère d'index -1 = ''
caractère d'index 0  = 'a'
caractère d'index 1  = 'b'

On remarque  que `strcharpart()`  n'interprète pas les  index négatifs  comme le
fait Vim qd on indexe directement une chaîne:

    echo strcharpart('abc', -1, 1)
    ∅~
    echo 'abc'[-1:-1]
    'c'~

# ?

    :echo strcharpart('abcdefg', 5, 4)
    fg~

`4` est trop grand, mais les caractères qui n'existent pas sont considérés comme
une chaîne vide.

# ?

    :echo strcharpart('abcdefg', 3)
    defg~


Sans longueur max, `strcharpart()` va jusqu'à la fin de la chaîne.

# ?

    echo tr('hello there', 'ht', 'HT')
    Hello THere~
    echo tr('<blob>', '<>', '{}')
    {blob}~

`tr()` permet de réaliser plusieurs substitutions en un seul appel de fonction.
Elle TRaduit les caractères d'une chaîne en ceux d'une autre chaîne.

# ?

Document `:h matchend()` and `:h matchstrpos()`.
And maybe `:h str*(`.

##
##
##
# Chaînes
## Caractères de contrôles

Il existe  plusieurs façon de  représenter les  caractères de contrôle  selon le
contexte / objectif recherché.

La [notation caret][1] est particulièrement adaptée  pour les visualiser au sein
d'un texte.

Une séquence d'échappement permet de les écrire littéralement dans une chaîne de
caractères (\n, \r, \t), ce qui est utile dans les regex.

<https://fr.wikipedia.org/wiki/S%C3%A9quence_d'%C3%A9chappement>
<https://en.wikipedia.org/wiki/Escape_sequence#Comparison_with_control_characters>

Elle permet également de produire de nouveaux caractères de contrôle et dépasser
la limite de 33.

Certains caractères de contrôles ne  disposent pas d'une notation abrégée (comme
`\n`, `\r`, `\t`), pex `C-r`.
Pour les représenter dans une chaine, on a 3 possibilités:

   • les insérer littéralement, ex: C-v C-r

   • utiliser une notation utilisant leur point de code, ex: \u12 pour trouver
     le point de code, l'insérer littéralement, faire ga dessus et lire le champ
     Hex

   • écrire une séquence d'échappement tq \<C-R> et utiliser des double quotes
     des single quotes empêchent toute traduction

Mais au bout du compte ils sont transmis aux pgm sous la forme d'un ou plusieurs
octets pour lequel la notation hexadécimale est la plus adapatée.

`$  xxd  -p`  permet  d'afficher  la  représentation  hexadécimale  de  certains
caractères de contrôle (entrée, tab, escape, flèches...).
Pour ce faire taper le caractère de contrôle suivi de la touche entrée et ne pas
tenir compte du 0a à la fin, il correspond à un CR.
Pex, quand on appuie sur la flèche du bas, la commande retourne:

    1b5b420a~

    0x1b = escape , 0x5b = [ , 0x42 = B

Ainsi, le caractère de  contrôle “flèche vers le bas“ est  envoyé à un programme
sous la  forme de la  séquence d'échappement : `escape  [B` ou avec  la notation
caret `^[[B`; de même, F1 = `^[OP`.

---

What's the caret notation of the delete character?
^?

Don't confuse the delete character with the delete key.
https://en.wikipedia.org/wiki/Delete_character


newline est un terme générique désignant n'importe quel caractère ou ensemble de caractères utilisés
pour représenter une nouvelle ligne, ce qui inclut:

        CR LF    Windows
        LF       Unix


Pk utilise-t-on le symbole @ pour représenter le null character en notation caret ?

Dans la  table ASCII, les  caractères de contrôle ont  un point de  code compris
entre 0 et 31 ou égal à 127.
Pour obtenir  la notation caret d'un  caractère de contrôle, on  prend la lettre
majuscule de l'alphabet ayant la même position.
Pex, le caractère  de contrôle de point de  code 1 dans la table  ASCII est noté
^A, celui de point de code 2 est noté ^B etc. Le null character est le caractère
de contrôle de point de code 0 dans la table ASCII.
Pour lui  on étend  le principe en  allant chercher le  caractère ASCII  dont le
point de code (64) précède celui de A (65).

De la même façon, comme le caractère escape  a le point de code 27 dans la table
ASCII et que  le caractère qui suit la  lettre Z (90) est [ (91),  on utilise la
notation ^[ pour escape.

## echo[mnhl]

    " ✘
        echo 'hello'   " some comment
    " ✔
        echo 'hello' | " some comment

            `:echo[m]` sees a double quote as part of its argument.
            Therefore, you can't append a comment like you could with other commands:

                    :y_ " hello

            You need  a bar to explicitly  tell `:echo[m]` that what  follows is
            NOT part of its argument.

            See `:h :comment`.


    echo "foobar\rqux"
    echom "foobar\rqux"

            affiche 'quxbar', 'foobar^Mqux'

            :echo interprète sans doute le CR comme un retour à la ligne (sans en ouvrir une nouvelle),
            il affiche donc 'foobar', puis revient au début de la ligne, et affiche 'qux'.
            Résultat: 'quxbar'

            :echom n'interprète jamais rien, comme d'habitude.


    echon 'foo' 'bar'
    echon 'foo' | echon 'bar'

            affiche le message 'foobar' dans les 2 cas

                    :echo 'foo' 'bar'          →    'foo bar'
                    :echo 'foo' | echo 'bar    →    foo
                                                    bar

            Contrairement à :echo, :echon n'ajoute aucun espace ou newline après une chaîne.


    echom 'that''s enough'

            affiche:    that's enough

            Ceci illustre la seule exception à la règle qui veut que les single quotes empêchent
            toute traduction. Une séquence de 2 ' s'affiche sous la forme d'une seul '.


        On ne peut pas se passer du dot dans:

                    • une sous-expression au sein d'une expression conditionnelle utilisant l'opérateur ternaire ?:
                    • une chaîne passée directement en argument à une fonction (map(), system(), ...)
                    • une affectation de valeur à une variable
                    • le registre expression
                    • la commande :return
                    • ...

                            :echo &list ? 'foo' 'bar' : 'baz'    ✘
                            :echo system('ls' '-l')              ✘
                            :let myvar = 'foo' 'bar'             ✘
                            :<C-R>= 'foo' 'bar'                  ✘

            Il semble également nécessaire d'utiliser dot qd une expression est une fonction
            locale à un script appelée depuis un mapping (sauf si elle se trouve en 1ère). Ex:

                    nno <key>    :echo 'hello' <SID>my_func()<cr>    ✘    E121: Undefined variable: SNR
                    fu! s:my_func()
                        return 'world'
                    endfu

                    nno <key>    :echo <SID>my_func() 'hello'<cr>    ✔    affiche 'world hello'
                    fu! s:my_func()
                        return 'world'
                    endfu


    echo "foo \x{code} bar"

            afficher le message "foo bar" en insérant au milieu un caractère représenté via une notation
            utilisant son point de code en hexa (jusqu'à 2 chiffres) et les caractères spéciaux \x (:h string)


    echo "foo \u{code} bar"

            idem mais en fournissant un point de code hexa en 4 chiffres

                                               NOTE:

            Les caractères spéciaux \d et \o ne peuvent pas être utilisées dans une simple chaîne
            pour représenter un caractère à partir de son point de code en décimal ou en octal.
            Uniquement \x, \u, \U.


    echoe[rr] "This script just failed!"

            Echo en rouge un message d'erreur, logué dans l'historique des messages.
            Si utilisé dans un script / fonction, le n° de sa ligne sera ajouté.


    echo '"foo \<tab> bar"'

            affiche    "foo \<tab> bar"

            Le caractère tab n'est pas traduit, car les single quotes empêchent toute traduction.
            Les doubles quotes à l'intérieur n'y changent rien car les single quotes sont plus à l'extérieur
            et ont donc la priorité.

    :echo eval('"foo \<tab> bar"')

            affiche    foo    bar

            eval() évalue la double chaîne '" ... "' en simple chaîne " ... ", à l'intérieur de laquelle
            les caractères spéciaux peuvent être traduits.

## Indexage

    echo 'foobar'[3]
    b~
    echo 'foobar'[-2:]
    ar~

            L'octet d'index 3 dans la chaîne 'foobar'.
            Les octets depuis celui d'index -2 jusqu'au dernier dans 'foobar'.

            On remarque une différence dans la manière d'indexer entre un nb positif et négatif:

                    • on commencer à compter à partir de 0 pour un index positif
                    • on commencer à compter à partir de -1 pour un index négatif


    echo 'foobar'[:2]
    foo~
    echo 'foobar'[3:]
    bar~
    echo 'foobarbaz'[3:5]
    bar~

            Syntaxe similaire à python (on parle de slicing).


    echo 'foobar'[-1]
    ∅~
    echo 'foobar'[-1:-1]
    r~

            Contrairement aux listes, on ne peut pas  utiliser un simple index négatif pour obtenir
            un caractère d'une chaîne.

            En revanche on peut bien utiliser des index négatifs qd on fait du slicing.


    echo 'fooébar'[3]
    <c3>~

            'fooébar'[3] ne retourne pas le caractère d'index 3, mais l'octet d'index 3.

            Illustre qu'on indexe pas une chaîne avec des n° de caractères mais d'octets.


    getline('.')[col('.')-1]

            Caractère après le curseur.

            S'il est multi-octets, on obtient seulement son 1er octet.

            Qd on  utilise col('.')  pour se  référer au  caractère qui  suit le
            curseur dans un index de chaîne, il faut lui enlever 1.

            En effet,  col('.') rajoute  toujours 1  au poids  de la  chaîne qui
            précède le curseur (sans doute car 0 est réservé pour une erreur).

# Coercition

Dans une comparaison, une chaîne est automatiquement évaluée en:

    • 0            si elle commence par une lettre
    • un entier    si elle commence par un entier ou un flottant
                   dans le cas d'un flottant, seule la partie entière est retenue


La même chose se passe dans un calcul :

    • echo 'hello'   + 10        10
    • echo 'hello10' + 10        10

    • echo '10hello' + 10        20
    • echo '10.10'   + 10        20


Dans une concaténation de chaînes :

    echo 10 . 'foo'

            affiche '10foo'    ; le nb 10 est converti en chaîne '10'

    echo 10.10 . 'foo'

            provoque l'erreur 'E806: using Float as a String' car un nb flottant ne peut être converti
            en chaîne


Avec des dicos:

    echo {1: 'one'}

            retourne {'1': 'one'}
            le nb 1 a été automatiquement converti en la chaîne '1' car la clé d'un dico ne peut être qu'une chaîne

    echo {'1': 'one'}[1]

            retourne '1'
            fonctionne car le nb 1 a été automatiquement converti en la chaîne '1'


En programmation, ce phénomène se nomme conversion de type / coercition.

Dans un test, 0 est considéré comme faux et tout autre entier relatif comme vrai.

##
##
##
# printf()

`printf()` est une fonction utile pour  manipuler une chaîne au sein de laquelle
on veut:

   • tronquer une sous-chaîne ou un flottant
   • ajouter un padding d'espaces ou de zéros
   • convertir un nb décimal en hexa ou en base 8
   • convertir un code ascii décimal en le caractère lui correspondant

---

    printf({fmt}, {expr1} ...)

`{fmt}` est une chaîne pouvant contenir des items `%`.
Pour chaque item utilisé (sauf `%%`), il faut fournir à `printf()` une
expression correspondante.

`printf()`  retourne la  chaîne  `{fmt}` où  les items  sont  remplacés par  les
expressions.
Les items servent à formater les expressions: on parle d'interpolation.
On ne peut pas utiliser plus de 18 expressions.

Le  formatage  est décrit  par  une  spécification  de  conversion qui  suit  le
caractère `%`.
Il  attend 1  argument obligatoire  (spécificateur  de conversion  aka type)  et
accepte  jusqu'à 3  arguments  optionnels (flags,  field-width, precision)  dans
l'ordre suivant:

    %  [flags]  [field-width]  [.precision]  type

---

    type

Il s'agit d'un caractère spécifiant le type de conversion à appliquer.

    ┌───┬───────────────────────────────────────────────────────────────────────────────────────────────┐
    │ s │ chaîne alignée à droite                                                                       │
    │   │ `field-width` et `.precision` sont interprétés comme des nb d'octets                          │
    │   │                                                                                               │
    │   │ La chaîne n'a besoin d'être alignée que si `field-width` est supérieur                        │
    │   │ au nb d'octets qu'elle pèse.                                                                  │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ S │ idem mais `field-width` et `precision` sont interprétés comme des nb de cellules              │
    │   │                                                                                               │
    │   │ La chaîne n'a besoin d'être alignée que si `field-width` est supérieur                        │
    │   │ au nb de cellules qu'elle occupe.                                                             │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ c │ caractère à partir de son code ascii                                                          │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ d │ nb entier décimal/en base 10                                                                  │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ x │ nb hexa                  caractères minuscules                                                │
    │ X │ nb hexa                  caractères maj                                                       │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ o │ nb octal                                                                                      │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ f │ nb flottant                                                                                   │
    │ e │ nb flottant; notation scientifique:      1.234560e+02                                         │
    │ E │ idem, mais en remplaçant l'exposant 'e' par 'E'                                               │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ g │ nb flottant;                                                                                  │
    │   │ équivalent à f si le nb est compris entre 10^-3 (inclus) et 10^7 (exclus), e autrement        │
    │   │                                                                                               │
    │   │ En l'absence de précision, les zéros superflus (ex: 123.456000) sont supprimés                │
    │   │ (contrairement à f).                                                                          │
    │   │ Un zéro juste après la virgule (123.0) n'est pas superflu, car il caractérise                 │
    │   │ le flottant, et le différencie d'un nb entier.                                                │
    │   │                                                                                               │
    │ G │ idem, mais équivaut à E qd le nb est compris entre 10^-3 et 10^7                              │
    ├───┼───────────────────────────────────────────────────────────────────────────────────────────────┤
    │ % │ '%%' est converti en '%' (aucun argument à fournir)                                           │
    └───┴───────────────────────────────────────────────────────────────────────────────────────────────┘

---

    flags

Une suite d'un ou plusieurs caractères.

    #

N'a d'effet qu'avec les types `o`, `x` et `X`.

A pour effet d'ajouter en préfixe `0`, `0x` ou `0X`:

    printf('%#o', 123)
    0173~
    printf('%#x', 123)
    0x7b~
    printf('%#X', 123)
    0X7B~

Permet d'exprimer explicitement la base dans laquelle est écrite le nb.

    0

Padding de zéros au lieu d'espaces.
Ne fonctionne que lorsque le padding est à gauche.
Un padding à droite ne peut être constitué que d'espaces.

    -

Alignement à gauche et non à droite.

    +

Préfixe un `+` devant un nb positif:

    printf('%+d', 123)
    +123~
    printf('%+.2f', 12.34)
    +12.34~

    ' '

Préfixe un espace devant un nb positif:

    printf('% d', 123)
    ' 123'~
    printf('%+ .2f', 12.34)
    '+12.34'~
    + a la priorité sur espace

---

    field-width

`field-width` est un  entier positif spécifiant le poids en  octets de la valeur
convertie.
Sauf pour l'item `%S` où il correspond à une largeur en nb de cellules.

Si `field-width` > poids  en octets de la valeur convertie  (ou nb de cellules),
un padding d'espaces est ajouté à gauche.
Si `field-width` < ..., la valeur n'est *pas* tronquée pour autant.

À la place d'un nb, on peut donner à `field-width` une valeur spéciale `*`.
Dans ce cas, il faudra passer à `printf()` 2 arguments au lieu d'un.
Le 1er correspondant au poids/largeur du champ, le 2e à l'expression à formater.
Ex:

    printf('%d: %*s', nr, width, line)

On a bien 2 items (`%d` et `%s`), mais 3 arguments en plus de la chaîne:

   • `nr`     est l'expression formatée selon %d
   • `width`  est le poids du champ dans lequel doit s'afficher `line`
   • `line`   est l'expression formatée selon %*s

`*` est utile lorsqu'on  a besoin d'une largeur de champ  dynamique, et est plus
lisible qu'une concaténation de chaînes:

    let prec = 9

    ✔
    printf('%'.prec.'f', 1/3.0)
    ✔✔
    printf('%*f', prec, 1/3.0)

---

    .precision

`precision`  est un  nb  interprété  de façon  différente  selon  le type  qu'il
affecte:

   • d, o, x et X     minimum de chiffres à afficher      avec padding (0/espace) si besoin
   • s                maximum d'octets à afficher         troncation si besoin
   • S                maximum de caractères à afficher    "
   • f, e, E, g, G    nb de chiffres après la virgule     "

Les différences d'interprétation sont logiques:  on souhaite souvent tronquer un
flottant, mais pas un entier.

Ceci  étant, pour  obtenir un  padding de  `0` avec  un entier,  il paraît  plus
logique d'utiliser un `field-width` et le flag `0`:

    printf('%06d', 123)

plutôt que

    printf('%.6d', 123)

Ainsi, on  peut considérer  que field-width  et .precision  ont des  usages bien
distincts:

    field-width = padding
    .precision  = troncation

Si on utilise le  flag `.precision` mais sans lui donner  de valeur (ex: `%.s`),
il est considéré comme valant `0` (=troncation max).

Si on n'utilise pas du tout le  flag `.precision` (ex: `%f`), il est malgré tout
considéré comme valant `6` pour un flottant  de type `f` ou `e`/`E`, et `1` pour
un flottant de type `g`/`G`.

Tout comme  pour `field-width`, on  peut donner à  `precision` la valeur  `*` au
lieu d'un nb.
Et à nouveau, dans ce cas, il faudra fournir 2 arguments au lieu d'un.
Un pour la précision de l'item, et un pour son contenu.


                                 ┌─ fonctionne car ...
                                 │
    ┌──────────────────────────┬────────────────────────────────────────────────────────────┐
    │ echo printf('%s',  123)  │ le nb 123 a été initialement converti en la chaîne '123'   │
    │     → '123'              │                                                            │
    ├──────────────────────────┼────────────────────────────────────────────────────────────┤
    │ echo printf('%d', '123') │ la chaîne 123 a été initialement convertie en le nb 123    │
    │     → '123'              │                                                            │
    ├──────────────────────────┼────────────────────────────────────────────────────────────┤
    │ echo printf('%f',  123)  │ le nb 123 a été initialement converti en le flottant 123.0 │
    │     → '123.000000'       │                                                            │
    └──────────────────────────┴────────────────────────────────────────────────────────────┘

`printf()` peut, lorsque c'est nécessaire, convertir un argument d'un type donné
en un autre.
Les seules types de conversions automatiques possibles sont:

   • nb    ↔    chaîne
   • nb    →    flottant

---

    echo printf('this char is %c', 97)
    this char is a~

`%c` permet  d'insérer au sein  d'une chaîne un caractère  à partir de  son code
ascii.


    echo printf('%f', 123.456)
    123.456000~

En l'absence de  précision explicite, printf() considère qu'elle  vaut `6`, d'où
les 6 chiffres après la virgule ici.

---

    printf('%.f', 123.456)
    123~

Qd la précision vaut 0 (`.` = `.0`), la partie décimale d'un flottant est omise:

    %.f    ⇔    %.0f

---

    echo printf('%6d', 123)
       123~
    echo printf('%06d', 123)
    000123~

    echo printf('%.s', 'foobar')
    ''~

En l'absence de précision, elle est considérée comme nulle, et précision nulle =
troncation max:

    %.s    ⇔    %.0s

##
##
##
# Reference

[1]: https://fr.wikipedia.org/wiki/Notation_caret

