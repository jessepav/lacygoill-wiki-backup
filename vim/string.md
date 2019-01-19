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
##
##
# ?

Similitude  entre toutes  les  fonctions  manipulant des  chaînes  / listes,  et
acceptant en argument des index (d'octets, de caractères, d'items, ...):

   • un index négatif est:

   - interprété comme `0` pour une chaîne

   - utilisé pour indexer depuis la fin en commençant à compter à partir de `-1`
     (`-2`, `-3`, ...) pour une liste

# ?

Similitudes et différences entre `match()` et `matchstr()`:

   • elles peuvent chercher dans des chaînes ou des listes de chaînes

   • elles acceptent 1 ou 2 arguments optionnels (start, count):

       - `start` = où commencer à chercher

       * index d'item pour une liste

       * index du 1er octet à partir duquel chercher pour une chaîne

       - `count` = cherche le `count`-ième match

   • `match()`    retourne un index (d'octet au sein d'une chaîne, d'item au sein d'une liste)
     `matchstr()` "        une sous-chaîne

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

    echo stridx('foo:bar:baz', ':')
    3~
    echo stridx('foo:bar:baz', ':', 3 + 1)
    7~

# ?

    echo match(['one', 'two', 'four', 'three'], 't..', 2)
    3~

Index du 2e item dans la liste matchant `t..`.

# ?

    echo match('testing', 't', 2)
    3~

Retourne `3`  (et non pas  `0`) car le 3e  argument optionnel indique  ici qu'il
faut commencer à chercher à partir du 2e octet.

# ?

                               ┌ cherche à partir de l'octet d'index 0 (le tout premier)
                               │  ┌ cherche la 2e occurrence
                               │  │
    echo match('testing', 't', 0, 2)
    3~

# ?

    echo matchlist('abcd', '\v(.(.))(.)')
    ['abc', 'ab', 'b', 'c', '', '', '', '', '', '']~

`matchlist()` retourne des sous-expressions, équivalentes à `\0`, `\1`, ..., `\9`
au sein de la chaîne de remplacement de la commande `:s`.

    \0 = 'abc'
    \1 = 'ab'
    \2 = 'b'
    \3 = 'c'

# ?

    echo matchstr('testing', 'ing', 5)
    ''~

Return an  empty string  because `ing`  can't be found  in `testing`  beyond the
fifth byte.

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

