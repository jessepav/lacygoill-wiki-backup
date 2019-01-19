# Pasting text
## What are the pros of using `:put =` over `append()` or `setline()`?

`:put =`  is more handy  on the command-line,  in an interactive  usage, because
less verbose.

Also, it moves the cursor on the last line pasted.
This is handy when you have multiple blocks of text to paste.

With `append()` and `setline()`, you would have to re-compute the line address
from which you want to paste every block, to avoid that they overlap.

## What are the cons of using `:put =`?

   • the cursor moves
   (which may be undesirable when you only have one paste to do)

   • it's not silent
   (you have to prefix it with `:silent`)

   • you have to escape double quotes

   • it doesn't delete the initial empty line in a new buffer

   • it pollutes the expression register

## When should I use `append()`?

When you need to INSERT a single block of text in an EXISTING buffer.

## When should I use `setline()`?

When you need to REPLACE a set of lines in an existing buffer.
Or, when you need to ADD new lines in:

   • a new buffer
   • at the end of an existing buffer, whose last line is empty

###
## What can `setline()` do that `append()` can't?

`setline()` can delete the contents of an existing line.
`append()` will NEVER delete any existing contents.

## Can `setline()` add new lines?

Yes, but only if there're no more lines to replace.
In this  case, `setline()` WILL  add just  enough so that  it can paste  all the
lines it received as argument.

###
## What happens if I call `setline(0, ...)`?

There's no line 0, and `setline()` can only replace FROM an existing line.
So, it won't paste anything.

## What happens if I call `append(0, ['foo', 'bar'])` in a new buffer?

You get an empty line, 'foo', then 'bar'.

Where does the empty line come from?
Think like this:

> “append() INSERTS lines between 2 existing lines”

When  you pass  it the  address  `0`, it  inserts  'foo' and  'bar' between  the
UNexisting line 0 and the existing line 1.
IOW, ABOVE line 1.
The empty line is the old line 1.

## What happens if I execute `:put =['foo', 'bar']` in a new buffer?  What's the difference with the previous `append()`?

Like with the previous `append()`, you get an empty line, 'foo', then 'bar'.
Unlike the previous `append()`, the cursor moves on the 'bar' line.

###
## How to use `append()` and make the cursor move like `:put =`?

        :let lines = [...]
        :call append('.', lines) | exe '+'.len(lines)

## What happens if I use `setline()` to replace 10 lines while there're only 5 below?

It will create 5 new lines, so that  it can replace their empty contents.

##
# Miscellaneous
## How to get the command with which Vim was started?

        :echo system('ps -o command= -p '.getpid())

Useful  if you  want to  parse the  command-line to  install some  configuration
depending on the flags which were passed to Vim on the shell's command-line.

## Why should I prefix any call to `system[list]()` with `:silent`?

When vim is running, the terminal is in “raw” mode: it sends a character as soon
as it receives one.

But when  you execute  a shell  command (via `:!`  or `system()`),  the terminal
switches to “cooked” mode: it buffers the received characters until a CR.

This allows the terminal to implement some rudimentary line-editing functions.
But when the  terminal is in cooked  mode, some stray characters may  be left on
the screen, forcing you to `:redraw`.

MWE:

        :call system('sleep 3')
        " smash the 'l' key
        " ✘ `l` is printed on the command-line~

        :sil call system('sleep 3')
        " smash the 'l' key
        " ✔ nothing is printed on the command-line~

##
# Issues
## Why does  `:call system('grep -IRn pat * | grep -v garbage >file')`  fail to capture the standard error in file?

The pipe between the  two greps redirects only the standard  output of the first
grep, not its standard error.

If you really want  the errors too, then execute use a  subshell to redirect the
standard error of the WHOLE pipeline:

            (grep -IRn pat * | grep -v garbage) >file 2>&1
            ├─────────────────────────────────┘
            └ subshell

##
##
##
# Chaînes
## Caractères de contrôles

Il existe plusieurs façon de représenter les caractères de contrôle selon le contexte / objectif recherché.

La [notation caret][1] est particulièrement adaptée pour les visualiser au sein d'un texte.

Une séquence d'échappement permet de les écrire littéralement dans une chaîne de
caractères (\n, \r, \t), ce qui est utile dans les regex.

        https://fr.wikipedia.org/wiki/S%C3%A9quence_d'%C3%A9chappement
        https://en.wikipedia.org/wiki/Escape_sequence#Comparison_with_control_characters

Elle permet également de produire de nouveaux caractères de contrôle et dépasser la limite de 33.

Certains caractères de contrôles ne disposent pas d'une notation abrégée (comme \n, \r, \t), pex C-r.
Pour les représenter dans une chaine, on a 3 possibilités:

    • les insérer littéralement, ex: C-v C-r

    • utiliser une notation utilisant leur point de code, ex: \u12
      pour trouver le point de code, l'insérer littéralement, faire ga dessus et lire le champ Hex

    • écrire une séquence d'échappement tq \<C-R> et utiliser des double quotes
      des single quotes empêchent toute traduction

Mais au bout du compte ils sont transmis aux pgm sous la forme d'un ou plusieurs
octets pour lequel la notation hexadécimale est la plus adapatée.

La  commande  'xxd  -p'  permet d'afficher  la  représentation  hexadécimale  de
certains caractères de contrôle (entrée, tab, escape, flèches...).
Pour ce faire taper le caractère de contrôle suivi de la touche entrée et ne pas
tenir compte du 0a à la fin, il correspond à un CR.
Pex, quand on appuie sur la flèche du bas, la commande retourne : 1b5b420a.

    0x1b = escape , 0x5b = [ , 0x42 = B

Ainsi, le caractère de  contrôle “flèche vers le bas“ est  envoyé à un programme
sous la forme de la séquence d'échappement : escape [B ou avec la notation caret
^[[B.
De même, F1 = ^[OP.



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

# Expressions

Une expression peut être :

        • un nb
        • une chaîne
        • un dictionnaire
        • une variable
        • une variable d'environnement     préfixe $
        • une option                       préfixe &
        • un registre                      préfixe @
        • une expression conditionnelle    a ? b : c
        • la sortie d'une fonction
        • le résultat d'une opération entre 2 expressions (+, -, *, /, %, .)


        :let myvar42 = 'hello'
        :let idx=42
        :echo myvar{idx}

        :fu! MyFunc42()
        :    return 'world'
        :endfu
        :let idx=42
        :echo MyFunc{idx}()

                On peut développer (interpoler?) une expression au sein même d'un nom de variable
                ou de fonction. Cf. :h curly-braces-names

                                               NOTE:

                Il peut s'agir d'une alternative à eval():

                        :let myvar42 = 'hello'
                        :let idx=42
                        :echo eval('myvar' . idx)

                        :fu! MyFunc42()
                        :   return 'world'
                        :endfu
                        :let idx=42
                        :echo eval('MyFunc' . idx . '()')

                eval() est moins lisible:

                        :echo eval('myvar'.idx)
                        :echo myvar{idx}

                                     NOTE:


        It works even if there's nothing outside the curly braces:

                :let var = 'hello'
                :let {var} = 'world'
                :echo hello
                world ~


    system('ls -l ' . expand('%:p'))

            Une concaténation de chaînes étant une expression, on peut la passer directement en argument
            à une fonction.

            Pas besoin de:

                    system ("ls -l  . expand('%:p') . '")'


    exe "nno cd :echo ".string({'one':1, 'two':2})."\r"    ✔
    exe "nno cd :echo ".{'one':1, 'two':2}."\r"            ✘

            Au sein d'une expression, il y a bien coercition automatique de nb en chaîne:

                    exe "nno cd :echo ".42."\r"    ✔

            ... mais pas de dico en chaîne.

            Il faut donc convertir soi-même le dico en chaîne via `string()`.


# For / While

    for [lnum, col] in [[1, 3], [2, 5], [3, 8]]
        echo getline(lnum)[col]
    endfor

            Montre qu'on peut itérer sur une liste de listes (ici [1,3], [2,5] et [3,8]),
            et ainsi modifier la valeur de plusieurs variables simultanément (au lieu d'une seule
            habituellement: for i in list).
            Utile qd on veut itérer sur les clés/valeurs d'un dico.

            La construction de base avec for est:    for var in list
            Cette autre construction:                for [var1, var2, ...] in listlist
            ... est en fait une variante de la 1e, qui n'est possible que lorsque list est composée exclusivement
            de listes ayant toutes la même dimension.


    for [key, value] in items(mydict)
        " do some stuff
    endfor

            Itère sur les clés et valeurs de mydict.


    fu! s:grab_words()
        call cursor(1, 1)

        let guard         = 0
        let words         = []
        let matchline     = search('\<\k\+\>', 'cW')

        while matchline && guard < 1000
            let words    += [matchstr(getline('.'), '\%' . col('.') . 'c\<\k\+\>')]
            let matchline = search('\<\k\+\>', 'W')
        endwhile
        return words
    endfu

            définit la fonction s:grab_words() qui lance une boucle while pour stocker tous les mots
            du buffer courant dans la liste words

                                               NOTE:

            On pourrait aussi utiliser:

                    let words = split(join(getline(1, '$'), "\n"), '\W\+')

            ... qui est encore + rapide.

            En revanche, le principe sur lequel repose cette commande nécessite qu'on puisse facilement
            décrire l'inverse du pattern recherché.
            Facile pour un mot (\W\+), mais plus difficile pour un pattern arbitraire (! foobar = ?).

                                               FIXME:

            Existe-t-il un moyen simple d'inverser un pattern arbitraire (ex: foobar)?
            J'ai tenté:     foobar\zs\_.\{-}\zefoobar\|^\_.\{-}\zefoobar\|\_.*foobar\zs\_.\{-}$

            ... dans:        :echo split(join(getline(1, '$'), "\n"), 'reverse pattern')
            ... ça semble marcher sauf pour le dernier foobar (dernière branche dans le pattern inversé).
            J'ai aussi tenté:

                           :echo split(join(getline(1, '$'), "\n"), '\v((foobar)@!\_.){-1,}')

                                               NOTE:

            Si on sait que le pattern ne peut être présent qu'une fois par ligne, on peut aussi utiliser:

                    :g/pattern/call add(list, matchstr(getline('.'), 'pattern'))

                                               NOTE:

            On peut imaginer que :while teste toujours une condition en fonction de qch qui se situe
            au-dessus d'elle.
            Ex, ici, :while teste si matchline est non nulle. Elle le fait initialement en se basant sur:

                    let matchline = search('\w\+', 'cW')

            ... qui est juste au-dessus.

            Puis, elle le fait en se basant sur:

                    let matchline = search('\w\+', 'W')

            ... qui, certes, se situe après :while au sein de la fonction, mais est bien exécutée AVANT
            le prochain retour vers :while.
            Donc, c'est un peu comme si ce 2e let se situait juste avant :while (JUSTE avant car il n'y
            a rien entre ce :let et :endwhile, et que :endwhile signifie retour vers :while).

                                               NOTE:

            On passe le flag 'c' à search() initialement, car il se peut qu'il y ait un match dès
            le début du buffer.
            Mais ensuite, au sein de la boucle, on ne passe plus ce flag à search(), autrement
            elle trouverait continuellement le même 1er match. Le curseur ne se déplacerait pas,
            on ne trouverait pas les autres matchs, et la boucle while ne se terminerait jamais.

                                               NOTE:

            On connaît rarement à l'avance le nb d'itérations d'une boucle while, contrairement à une boucle for.
            Il se peut qu'elle en exécute un très grand nb, voire une infinité (infinite loop).
            De ce fait, il est généralement utile d'implémenter un garde-fou.

            Pour ce faire, on créera une variable 'guard' initialisée à 0 avant l'exécution de la boucle.
            Dans la condition testée par while, on vérifiera entre autres que guard est inférieure
            à un certain nb (100, 1000).
            Enfin, au sein de la boucle, on incrémentera guard.
            Ceci permettra de s'assurer que while n'exécute qu'un nb limité d'itérations.

# Let

    let

            affiche l'ensemble des variables actuellement définies


    let list2 = list1

            Affecter à la variable list1 la référence de list2.

            On peut vérifier que list1 et list2 partagent la même référence via:

                    :echo list2 is list1

            Il est probable que pour Vim une donnée soit décomposée en 3 parties (comme dans un fs):

                • son nom (associé à une référence dans une sorte d'annuaire)
                • une référence (pointant vers l'adresse mémoire de la donnée)
                • la donnée elle-même

            Il  ne faut  pas  croire que  dans  la commande  qui  précède, on  a
            dupliqué la donnée stockée dans list1.
            On a simplement créé un nouveau nom pointant vers la référence d'une
            même donnée.
            Ceci explique  pourquoi si on modifie  un item de list1,  on modifie
            par la même occasion list2 ; car les 2 noms d'objets sont associés à
            la même donnée.
            Et réciproquement,  modifier list2  a pour  effet de  modifier aussi
            list1.

            Pour dupliquer la liste stockée dans list1, il faut utiliser la fonction copy() ou deepcopy().


    let [var1, var2; rest] = mylist

            affecter à var1 mylist[0], à var2 mylist[1] et tous les autres items de mylist à la liste rest
            utile pour éviter d'avoir une erreur si la taille de mylist pourrait être plus grand que
            le nb de variables


    let s:myflag = exists('s:myflag') ? !s:myflag : 1
    let s:myflag = !get(s:, 'myflag', 1)

            stocke 1 dans la variable s:myflag si elle vaut 0, 1 autrement

            L'affectation prend en charge le cas où s:myflag n'a pas encore de valeur.
            s:myflag peut être utilisée comme un flag booléen permettant d'exécuter alternativement
            2 actions différentes A, B, A, B... (toggle)

            Utile pex, pour (dés)activer la mise en surbrillance d'un pattern via :match.

                    let s:myflag = ...
                    if s:myflag
                        match /pattern/
                    else
                        match none
                    endif

            Si B n'est pas une action  fixe et dépend d'une valeur, le précédent
            code n'est plus suffisant.
            Dans ce  cas, au lieu  de tester  si s:myflag vaut  0 ou 1,  on peut
            tester si elle  existe ou non et lui affecter  la valeur dont dépend
            B.

            Utile pex,  pour (dés)activer la  mise en surbrillance  d'un pattern
            via matchadd().
            En effet,  cette fois, la  désactivation de la mise  en surbrillance
            n'est  plus  fixe   (:match  none),  mais  dépend   d'un  id  (:call
            matchdelete(id)).

                    if !exists('id')
                        let id = matchadd('SpellBad', 'pattern')
                    else
                        call matchdelete(id)
                        unlet id
                    endif

            L'existence/absence de id répond à la question:    Qu'a-t-on fait la dernière fois, A ou B ?
                                                               Et donc que faire à présent, B ou A ?
            La valeur de id répond à la question:              Comment faire B ?

            Une alternative utilisant le 1er code serait:

                    let s:myflag = exists('s:myflag') ? !s:myflag : 1
                    if s:myflag
                        let id = matchadd('SpellBad', 'pattern')
                    else
                        call matchdelete(id)
                        unlet id    " facultatif
                    endif

            L'inconvénient de cette  2e version est qu'elle crée  2 variables au
            lieu d'une, une pour le flag et une pour l'id.

# Listes

    list[-2]    avant-dernier item de list

            On indexe les items d'une liste à partir de 0 qd on commence à compter depuis la gauche,
            et à partir de -1 qd on commence à compter depuis la droite.

    list[1:-2]

            éléments de list du 2e jusqu'à l'avant-dernier
            syntaxe similaire à python (on parle de slicing)

                                               NOTE:

            Ne fonctionne pas comme prévu qd le premier index est négatif et le 2nd positif. Pex:

                    :echo [1,2,3][-1:0]

            ... ne retourne pas [1,2,3] mais [].

            En effet, on ne peut pas revenir en arrière qd on indexe (ici du dernier jusqu'au 1er).
            En revanche:

                    :echo ['foo','bar','baz'][-2:2]

            ... retourne ['bar','baz'], car l'item d'index 2 ('baz') est bien après celui d'index -2 ('bar').

            À retenir: on ne peut pas revenir en arrière qd on indexe une liste ou une chaîne.

    list[:5]    list[5:]

            éléments de list dont l'index va de 0 jusqu'à 5; de 5 jusqu'à l'index max
            syntaxe similaire à python (on parle de slicing)

    list[s : e]

            sous-liste de list allant de l'index stocké dans la variable s (start) jusqu'à celui
            stocké dans e (end)
            Il est important de placer des espaces autour du : pour éviter que Vim n'interprète
            s:e comme le nom d'une seule variable.

    let list[3:5] = ['foo', 'bar', 'baz']

            affecte aux items d'index 3 à 5 de list les valeurs 'foo', 'bar' et 'baz'


    let list += [7, 8]
    call extend(list, ['7', '8'])

            concatène [7, 8] à list

                                               NOTE:

            L'opérateur + n'altère pas la liste d'origine contrairement à extend() qui réalise
            l'opération in-place.

                    echo list + ['foo', 'bar']           ne change pas list
                    echo extend(list, ['foo', 'bar'])    change list

           extend() ne modifie pas la 2e liste.

                    echo extend(alist, blist)            change alist mais pas blist


    let list[2] += 99

            ajoute 99 au 3e item de list (en supposant que ce dernier soit un nb)
            possible car une liste est un objet mutable


    let list[-1] .= 'foo'

            concatène la chaîne 'foo' au dernier item de list (en supposant que ce dernier soit une chaîne)
            possible car une liste est un objet mutable


    nno cd :call Func()<cr>
    fu! Func()
        let list = [1, 2, 3]
        call FuncA(list)
        echo list
    endfu

    fu! FuncA(other_list)
        let l:other_list = a:other_list
        call map(l:other_list, 'v:val+1')
    endfu

            cd
            [2,3,4]~

            Vim passe les arrays (listes/dicos) par référence,  et non par valeur, ce qui explique
            pourquoi dans cet exemple la liste a muté.

            Ceci reste vrai peu importe comment elles sont passées:
            via une fonction, ou une simple affectation.


                                               NOTE:

            En revanche, Vim passe les scalaires par valeur:

                    nno cd :call Func()<cr>
                    fu! Func()
                        let list = [1, 2, 3]
                        let n = 42
                        call FuncA(n)
                        echo n
                    endfu

                    fu! FuncA(other_n)
                        let l:other_n = a:other_n
                        let l:other_n += 1
                    endfu

                            cd
                            42~

            ... ce qui explique pourquoi le nombre n'a pas muté.
            Globalement, Vim se comporte comme awk.


    fu! Increment(list, i)
        let a:list[a:i] += 1
    endfu
    let list = [0, 0, 0] | call Increment(list, 2) | echo list

            retourne [0, 0, 1]
            possible car une liste est un objet mutable


    fu! Increment(list, i)
        let a:list[a:i] += 1
    endfu
    let counts = [0, 0, 0] |  let patterns = ['foo', 'bar', 'baz']
    for i in range(3)      |  exe '%s/'.patterns[i].'/\=Increment(counts,'.i.')/gn' | endfor

            Stocke dans `counts` les nb d'occurrences des patterns foo, bar et baz.

            Possible car  l'incrémentation qui  a lieue  dans Increment() n'est  pas faite  sur une
            copie de `counts`  qui serait locale à la  fonction, mais sur la liste  d'origine qui a
            été passée en argument.

            On dit que Vim passe les listes (et dicos) par référence, et non par valeur.

            Il n'y a qu'une seule liste, qu'on peut faire muter, pex via des appels successifs à une fonction.

            À l'intérieur de la fonction, le nom donné à la liste n'a pas d'importance.
            Pex, ici, on l'appelle 'list' dans la fonction Increment() alors qu'à l'extérieur
            de cette dernière, elle s'appelle `counts`.
            IOW, la mutation n'est pas affectée par la différence de noms entre l'intérieur et
            l'extérieur de la fonction.


                                               NOTE:

            On peut faire muter une liste passée directement en argument, mais pas `a:000` qui est une liste
            construite par Vim:

                    nno cd :call Func(1,2,3)<cr>
                    fu! Func(...) abort
                        call map(a:000, 'v:val+1')    ✘
                        echo a:000
                    endfu

# Nombres

Vim gère 2 types de nombres, les entiers (signés sur 32 bits, +-2 milliards) et les flottants.

    echo 100            affiche le nombre 100
    echo 0xff           affiche le nb 255 (0x introduit la notation hexadécimale)
    echo 017            affiche le nb 15 (le 1er 0 introduit la notation octale)
    echo 019            affiche le nb 19

                        Au lieu de produire une erreur, Vim ignore silencieusement la notation octale
                        car le chiffre 9 n'existe pas en base 8.
                        De ce fait, il vaut mieux éviter la notation octale quand c'est possible.

    echo 5.45e3         affiche 5450.0 (notation exponentielle)

                        En notation exponentielle, il faut obligatoirement un point et un chiffre après.
                        Ainsi 5e10 n'est pas valide, mais 5.0e10 est valide.

    echo 15.45e-2       affiche 0.1545

    echo 2 * 2.0        affiche 4.0

                        Qd on réalise un calcul ou une comparaison contenant un flottant, Vim convertit
                        les entiers en flottant.

    echo 3 / 2          affiche 1

                        Les deux nb de la division étant des entiers, la division retourne le quotient
                        pour avoir le nb exact, il suffit d'utiliser un flottant qq part (ex: echo 3 / 2.0).

    echo 13 % 5         affiche le reste dans la division de 13 par 5

# Fonctions
## Théorie

Il ne faut jamais créer 2 fichiers dont le chemin depuis un dossier `autoload/` est identique:

        ~/.vim/plugged/a_plugin/autoload/foo.vim
        ~/.vim/plugged/b_plugin/autoload/foo.vim

En effet, si on définit une fonction dans le 2e fichier:

        fu! foo#bar()
            echo 'hello'
        endfu

Elle ne sera jamais trouvée:

        call foo#bar()
        E117: Unknown function: foo#bar~

... car Vim s'arrêtera de chercher  dès qu'il trouvera un fichier `foo.vim` dans
un dossier `autoload/` du rtp.


En programmation, on  appelle subroutine (sous-programme/routine/procédure), une
fonction  dont le  code de  sortie ne  nous intéresse  pas, seule  son exécution
compte.
En vimscript, une procédure est appelée via la commande Ex :call.



En cas d'échec,  le code de sortie des  fonctions système est 0, ou -1  si 0 est
une valeur possible de succès.
Pex, en cas d'échec exists() retourne 0 alors que match() retourne -1.
En effet,  0 est une  valeur possible de  succès pour match()  (ex: match('foo',
'f')), mais pas pour exists().

Lorsqu'une fonction utilise -1 comme code de retour pour un échec, on ne peut pas écrire:

        if [!]MyFunc()

... pour réaliser un test. Il faut obligatoirement comparer la sortie à -1:

        if MyFunc() == -1


    :fu Foo

            afficher le code contenu dans la fonction Foo


Parfois, il peut être intéressant d'“éteindre“ temporairement une fonction, c'est à dire l'empêcher
de s'exécuter, sans pour autant la supprimer ou la commenter.
Pour ce faire, il suffit de créer une variable locale avant la définition de la fonction, et de stopper
son exécution si elle vaut 0.
Ex:

            let s:myvar = 1
            fu! MyFunc()
                if s:myvar == 0
                    return
                endif
                ...
                main code
                ...
            endfu

On peut aller + loin en ajoutant à la fin du script définissant la fonction 3 commandes pour éteindre
/ allumer / toggle cette dernière:

            com! SwitchOnMyFunc     let s:myvar = 1
            com! SwitchOffMyFunc    let s:myvar = 0
            com! ToggleMyFunc       let s:myvar = !s:myvar

## Arguments

On peut définir une fonction qui attend des arguments identifiés (named arguments) limités à 20,
ainsi que des arguments supplémentaires et optionnels (représenté par '...').


Les arguments optionnels sont utiles pour permettre de modifier la valeur par défaut de certaines variables
utilisées au sein de la fonction. Ex:

    fu! MyFunc(...)
        let var1 = a:0 >= 1 ? a:1 : 'foo'
        let var2 = a:0 >= 2 ? a:2 : 'bar'
        let var3 = a:0 >= 3 ? a:3 : 'baz'
    endfu

Pour mieux comprendre, on pourrait tout aussi bien réécrire le code précédent en remplaçant:

    • a:0 >= 1         exists('a:1')
    • a:0 >= 2    →    exists('a:2')
    • a:0 >= 3         exists('a:3')

Une méthode plus élégante consiste à utiliser get() en lui passant en argument entre autres la liste
des arguments optionnels a:000 :

    fu! MyFunc(...)
        let var1 = get(a:000, 0, 'foo')
        let var2 = get(a:000, 1, 'bar')
        let var3 = get(a:000, 2, 'baz')
    endfu

Ici MyFunc() attribue par défaut les valeurs 'foo', 'bar' et 'baz' aux variables
var1, var2 et  var3, mais permet de  modifier certaines d'entre elles  si on lui
passe des valeurs en argument (a:1, a:2, a:3).
Toutefois, on ne peut pas modifier n'importe quel sous-ensemble de variables.
Seulement, [var1], [var1, var2] et [var1, var2, var3].
IOW, seulement un sous-ensemble continu qui débute par var1.
Pex on ne pourrait pas modifier:

    • [var1, var3] car il n'est pas continu; il manque var2
    • [var2, var3] car bien que continu il ne commence pas par var1

De ce fait, qd on écrit MyFunc() il faut veiller à affecter a:1 à la variable la
plus susceptible d'être modifiée.
a:2 à la 2e ayant le + de chances d'être modifiée.
a:3 à celle ayant le moins de chances d'être modifiée.
Pk ?
Supposons qu'on  affecte a:3 à  la variable  var1, qui est  celle ayant le  + de
chances d'être modifiée.
À chaque fois qu'on voudra modifier var1,  il faudra passer 3 valeurs à MyFunc()
donc modifier aussi var2 et var3, qui n'en auront peut-être pas besoin.
Auquel cas, il faudra passer à MyFunc() les valeurs par défaut de var2 et var3.


Depuis une fonction on peut accéder en lecture à un argument (a:bar) mais pas en
écriture.
On  ne peut  donc pas  modifier la  valeur d'un  argument, en  revanche on  peut
affecter sa  valeur à une autre  variable qu'on pourra manipuler  comme bon nous
semble.

    :function Foo(bar) ^@ echom a:bar ^@ endfu
    :call Foo("qux")

            définit  la fonction  Foo(), qui  une fois  appelée, echo  la chaîne
            "qux" (bar est le nom du paramètre) qu'on lui passe

    :function Foo(...) ^@ cmd ^@ endfu

            définit la fonction  Foo() qui attend un groupe  d'arguments dont le
            nb est indéterminé (mais limité à 20)

    :function Foo(bar, ...) ^@ cmd ^@ endfu

            définit la fonction Foo() qui attend l'argument bar et un groupe d'arguments

            a:bar    (est évalué à) contenu de l'argument bar
            a:0      nb d'arguments du groupe ... (n'inclut donc pas bar)
            a:1      1er argument du groupe ... (!= bar)

    a:0

            nb d'arguments optionnels  [...] passé à une fonction  (proche de $#
            dans un script bash)

    a:1, a:2

            1er, 2e argument optionnel
            équivaut à a:000[1], a:000[2]; similaire à $1, $2 dans un script bash

    a:000

            liste des  arguments optionnels passés  à la fonction (proche  de $@
            dans un script bash)

    a:{i}

            ième argument; équivaut à a:i

            découvert via :h 41.7 (section: variable number of arguments)

## Buffers

    Ajoute:

    ┌────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┐
    │ append('$', 'THE END')                 │ la ligne "THE END" après la dernière ligne du buffer courant      │
    ├────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ append('.', '')                        │ une ligne vide après la ligne courante                            │
    ├────────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ append(0, ['Chapter 1', 'some title']) │ les lignes "Chapter 1" et "some title" au début du buffer courant │
    └────────────────────────────────────────┴───────────────────────────────────────────────────────────────────┘

    Teste l'existence d'un buffer dont:

    ┌───────────────────────────────┬────────────────────────────────┐
    │ bufexists(42)                 │ le n° est '2                   │
    ├───────────────────────────────┼────────────────────────────────┤
    │ bufexists('foo')              │ le nom est 'foo'               │
    ├───────────────────────────────┼────────────────────────────────┤
    │ bufexists(expand('~/.vimrc')) │ le nom est '/home/user/.vimrc' │
    └───────────────────────────────┴────────────────────────────────┘

            On peut utiliser un chemin absolu ou relatif par rapport au cwd.
            Mais si on utilise un chemin absolu, il ne doit pas contenir le tilde du home.
            Il faut développer ce dernier via expand().


    Teste l'existence d'un buffer listé et dont:

    ┌──────────────────┬──────────────────┐
    │ buflisted(3)     │ le n° est 3      │
    ├──────────────────┼──────────────────┤
    │ buflisted('foo') │ le nom est 'foo' │
    └──────────────────┴──────────────────┘


    Nom du:
    ┌────────────────┬───────────────────────────────────────┐
    │ bufname('%')   │ buffer courant                        │
    ├────────────────┼───────────────────────────────────────┤
    │ bufname('#')   │ alternate buffer                      │
    ├────────────────┼───────────────────────────────────────┤
    │ bufname('$')   │ dernier buffer                        │
    ├────────────────┼───────────────────────────────────────┤
    │ bufname(3)     │ buffer n° 3                           │
    ├────────────────┼───────────────────────────────────────┤
    │ bufname('foo') │ buffer contenant 'foo' (dans son nom) │
    └────────────────┴───────────────────────────────────────┘


    if !empty(bufname('%'))

            Teste si le buffer courant a bien un nom.


    Retourne le n° du buffer:
    ┌──────────────┬────────────────────────────┐
    │ bufnr('%')   │ courant                    │
    ├──────────────┼────────────────────────────┤
    │ bufnr('#')   │ alternate                  │
    ├──────────────┼────────────────────────────┤
    │ bufnr('$')   │ dernier de la liste        │
    ├──────────────┼────────────────────────────┤
    │ bufnr('foo') │ dont le nom contient 'foo' │
    └──────────────┴────────────────────────────┘

            En cas d'échec, retourne -1, et non 0.


    virtcol('.')

            Number of  the screen column  occupied by the character  right after
            the cursor.

                                     NOTE:

            The value of this expression can sometimes seem surprising.
            Write this sentence in `/tmp/file`:

                    they would be useful if they were here

            Then, start Vim like this:

                    $ vim -Nu NONE +'norm! 13l' +'lefta 20vs | setl wrap lbr' /tmp/file

            Here's what should be displayed:

                                 the cursor should be on this column where a real space resides
                                 v
                    they would be
                    useful if they were
                    here

            From  this position,  `virtcol('.')`  evaluates to  `20`, while  you
            probably expected `14`.
            To better understand what happens, set `'ve'` like this:

                    set ve=all

            And move your cursor on the last screen column, then evaluate `virtcol('.')`.
            You'll get `20`.
            Maybe  `virtcol('.')` should  evaluate to  `14` when  the cursor  is
            right  before the  space, but  as soon  as you  move the  cursor one
            character forward again  to reach the beginning of  the second line,
            it makes complete sense for `virtcol('.')` to return `21`.

            `virtcol('.')` doesn't  make the difference between  a screen column
            where there is a real character, and one where there is none.
            It includes all of them.

            For this reason,  you should prefer `col()` which  is not influenced
            by any option which may change how the text of a file is displayed:

                    • breakat
                    • breakindent
                    • linebreak
                    • showbreak
                    • wrap
                    ...

            Although, I guess it's ok to use  it when you're sure your lines are
            NOT wrapped.



    col('.')

            Byte index du caractère après le curseur, ou dit autrement:

                    • l'index du 1er octet du caractère qui suit le curseur
                    • le poids de la chaîne allant du début de la ligne jusqu'au curseur, +1

                      Pk +1?
                      Sans doute car `0` est réservé pour une erreur.

            Exemple:

                fooé|bar    foo étant au début d'une ligne et le curseur étant représenté par le pipe,
                            col('.') retourne 6

                            Du début de la ligne jusqu'au curseur, il y a 5 octets (dans 'fooé', 'é' en pèse 2),
                            l'octet suivant est donc le 6e.


                                               NOTE:

            col('.') et virtcol('.') ne retournent pas toujours le même nombre.
            En  particulier, si  certains caractères  précédant le  curseur sont
            encodés sur plusieurs octets.
            `virtcol('.')`  est  également   influencée  par  certaines  options
            ('wrap', 'linebreak', ...), contrairement à `col('.')`.


    col('$')

            Poids de la ligne + 1.
            Index de l'octet imaginaire suivant le dernier caractère sur la ligne.


    getbufvar('%', '')

            Dictionnaire contenant toutes les variables locales au buffer courant ainsi que leurs valeurs.

            getbufvar() permet d'accéder à la valeur d'une variable ou option locale à un buffer.
            Ne fonctionne pas pour une option locale à une fenêtre (utiliser getwinvar() pour ça).


    getbufvar('%', '&ft')
    getbufvar(5, 'myvar', 'default')

            Type de fichier du buffer courant
            Valeur de `b:myvar` dans le buffer n° 5, si elle existe; 'default' autrement.


    Contenu de la ligne:

    ┌──────────────┬────────────────────────┐
    │ getline(123) │ dont l'adresse est 123 │
    ├──────────────┼────────────────────────┤
    │ ...('$')     │ à la fin du buffer     │
    ├──────────────┼────────────────────────┤
    │ ...("'a")    │ portant la marque a    │
    ├──────────────┼────────────────────────┤
    │ ...('w0')    │ en haut de la fenêtre  │
    ├──────────────┼────────────────────────┤
    │ ...('w$')    │ en bas de la fenêtre   │
    └──────────────┴────────────────────────┘

    getline(1, '$')

            Retourne toutes les lignes entre la 1e et la dernière du buffer sous la forme d'une liste.
            Chaque item de la liste est une chaîne contenant une ligne du buffer.

            On peut aussi utiliser les fonctions getbufline() et readfile() pour récupérer les lignes
            d'un buffer/ fichier. Chaque fonction est utile dans un contexte différent:

                    • getline()       buffer courant
                    • getbufline()    buffer autre que le courant
                    • readfile()      fichier non chargé dans un buffer

            Pour un buffer déchargé, getbufline() retourne une liste vide [] peu importe son contenu réel.


    Retourne le n° de la ligne:

    ┌───────────┬───────────────────────┐
    │ line('$') │ en bas du buffer      │
    ├───────────┼───────────────────────┤
    │ ...("'a") │ portant la marque a   │
    ├───────────┼───────────────────────┤
    │ ...('w0') │ en haut de la fenêtre │
    ├───────────┼───────────────────────┤
    │ ...('w$') │ en bas de la fenêtre  │
    └───────────┴───────────────────────┘

    line2byte(42)

            retourne le poids en octets du buffer courant depuis son début jusqu'à la fin de la ligne 41
            (les newlines sont inclus)


    line2byte(line('$')+1)

            retourne le poids total en octets du buffer courant + 1

            Cette expression est utile pour vérifier qu'un buffer est vide de contenu:

                    if line2byte(line('$')+1) <= 2
                    ...

            Pk `line('$')+1` et pas `line('$')` tout court?
            Parce que `line2byte(line('$'))` retournerait le poids en octets depuis le début du buffer
            jusqu'à la fin de l'avant-dernière ligne, et non pas jusqu'à la fin de la dernière ligne.

            Ainsi, si le buffer contient une seule ligne et qu'elle est non vide, cette expression
            retournera 1.
            Ce `1` signifie sans doute qu'un buffer contient au moins un octet avant tout texte
            (peut-être le BOM = Byte Order Mark ?).
            Et comme `1 <= 2`, le test passera alors qu'il ne devrait pas puisque le buffer est non vide.

            Pk `<= 2`?
            Parce qu'une ligne vide contiendra au moins un 1er caractère (BOM?) et un newline à la fin.


    setline(5, 'hello world!')
    setbufline(2, 5, 'hello world!')

            Remplace la 5e ligne du buffer courant / buffer n° 2 par 'hello world!'.

            Retourne 0 en cas de succès, 1 autrement.

            Ne fait pas bouger  le curseur.  Utile pour substituer une ligne ou  un morceau de ligne
            (y  compris sur  la courante),  via  un mapping  /  commande. Pour ce  faire, donner  à
            setline(), en 2e argument, la sortie de substitute(getline(...), ...).


    setline(5, ['foo', 'bar', 'baz'])

            remplace la 5e ligne du buffer par 'foo', la 6e par 'bar', et la 7e par 'baz'

## Chaînes

    let option = 'number'
    echo eval('&'.option) ? 'no'.option : option
    'number' ou 'nonumber'~

            `eval()` permet d'évaluer le code contenu dans une chaîne.


    let string = 'foo \u0026 bar'
    echo eval('"'.string.'"')
    foo & bar~

    let string = 'foo\<tab>bar'
    echo eval('"'.string.'"')
    foo    bar~

            Convertit une chaîne littérale en une chaîne non littérale.

            La concaténation a pour but d'intégrer des doubles quotes au sein de
            la chaîne littérale.
            `eval()` évalue l'intérieur de la chaîne, qui est encore une chaîne,
            mais cette fois non littérale, grâce aux double quotes.
            Lors  de l'évaluation  d'une  chaîne non  littérale, les  caractères
            spéciaux sont automatiquement traduits.


    execute('cmd'[, 'silent!'])

            Retourne la sortie de la commande Ex 'cmd'.

            `execute()` est une alternative à `:redir`.

            Le 2e argument est optionnel, il peut prendre comme valeur:

                    • ''
                    • 'silent' (défaut)
                    • 'silent!'


                                               NOTE:

            :call execute('echo "hello"')
            :call execute('echo "hello"', 'silent')
            :call execute('echo "hello"', 'silent!')
            ∅~

            :echo execute('echo "hello"')
            :echo execute('echo "hello"', 'silent')
            :echo execute('echo "hello"', 'silent!')
            hello~

            Le 2e argument optionnel n'a d'influence que pendant l'évaluation de
            `execute()`.
            Il n'a aucune influence sur sa sortie.

            Il  permet  de  demander  à  `execute()`  d'évaluer  une  expression
            silencieusement.
            Mais si on utilise `:echo`, le résultat de cette évaluation, qu'elle
            ait  été  silencieuse  ou  pas,  sera  affiché,  car  la  sortie  de
            `execute()` se fiche de l'argument optionnel.

            Exception:

            Si on  utilise 'silent!',  non seulement  les messages  d'erreurs ne
            sont pas affichés pendant l'évaluation, mais en plus ils ne font pas
            partie de la sortie.
            C'est le seul cas où le 2e argument optionnel a une influence sur la
            sortie de `execute()`.

                    echo execute('abcd', 'silent!') is# ''
                    1~


                                               NOTE:

            Pour se débarrasser du newline au début:

                    execute('cmd')[1:]


    getchar()

            Demande  à l'utilisateur  d'appuyer sur  une touche  et retourne  le n°  du caractère
            correspondant, au sein de l'encodage défini par 'encoding' (utf-8 chez moi).


Similitude entre toutes les fonctions manipulant des chaînes / listes, et acceptant en argument
des index (d'octets, de caractères, d'items, ...):

    • un index négatif est:

              - interprété comme 0 pour une chaîne

              - utilisé pour indexer depuis la fin en commençant à compter à partir de -1 (-2, -3, ...)
                pour une liste

Similitudes et différences entre `match()` et `matchstr()`:

    • elles peuvent chercher dans des chaînes ou des listes de chaînes

    • elles acceptent 1 ou 2 arguments optionnels (start, count):

              - `start` = où commencer à chercher

                          * index d'item pour une liste

                          * index du 1er octet à partir duquel chercher pour une chaîne

              - `count` = cherche le `count`-ième match

    • `match()`    retourne un index (d'octet au sein d'une chaîne, d'item au sein d'une liste)
      `matchstr()` "        une sous-chaîne


Différences entre `match()` et `stridx()`:

    • `match()`  peut travailler sur une liste de chaînes
      `stridx()` uniquement sur une chaîne

    • `match()`  cherche un pattern
      `stridx()` "       une chaîne littérale

    • `match()`  et `stridx()` acceptent un 3e argument optionnel {start}
       mais seule `match()` accepte un 4e argument optionnel {count}

    • `match()`  respecte 'ignorecase' (sauf si on utilise `\c` ou `\C`), mais pas 'smartcase'
      `stridx()` est toujours sensible à la casse


Différences entre `match()` et `count()`:

    • `count()` peut travailler sur une chaîne ou une liste de chaînes (comme `match()`),
      mais aussi sur (les valeurs d')un dictionnaire

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


    echo match('An Example', 'Example')
    echo stridx('An Example', 'Example')
    3~

    echo match('Starting point', 'start')
    0~
    echo stridx('Starting point', 'start')
    -1~

            Qd on leur passe une chaîne en 1er argument, `match()` et `stridx()` retournent l'index
            de l'octet précédant la sous-chaîne passée en 2e argument.

            Si elles retournent:

                    • 0   ça signifie que  la sous-chaîne a été trouvée au tout début
                    • -1  ça signifie que  la sous-chaîne est absente


    echo stridx('get back to work', 'back') != -1
    1~

            Teste la présence de 'back' au sein d'une chaîne.


    echo stridx('foo:bar:baz', ':')
    3~
    echo stridx('foo:bar:baz', ':', 3 + 1)
    7~


    echo match(['one', 'two', 'four', 'three'], 't..', 2)
    3~

            Index du 2e item dans la liste matchant 't..'


    echo match('testing', 't', 2)
    3~

            Retourne 3 (et non pas 0) car le  3e argument optionnel indique ici qu'il faut commencer
            à chercher à partir du 2e octet.


                               ┌ cherche à partir de l'octet d'index 0 (le tout premier)
                               │  ┌ cherche la 2e occurrence
                               │  │
    echo match('testing', 't', 0, 2)
    3~


    echo matchlist('abcd', '\v(.(.))(.)')
    ['abc', 'ab', 'b', 'c', '', '', '', '', '', '']~

            `matchlist()` retourne des sous-expressions, équivalentes à  \0, \1, ..., \9
            au sein de la chaîne de remplacement de la commande :substitute

                    \0 = 'abc'
                    \1 = 'ab'
                    \2 = 'b'
                    \3 = 'c'


    matchstr('testing', 'ing')
    matchstr('testing', 'ing', 5)
    matchstr(@a, '\v.{-}\n')

            Retourne:

                    • 'ing' car il est présent dans 'testing'
                    • '' car 'ing' n'est pas présent dans 'testing' au-delà du 5e octet
                    • la 1e ligne stockée dans le registre a


    matchstr(getline('.'), '\%'.col('.').'c...')

            Les 3 caractères après le curseur.

            col('.') retourne l'index du 1er octet du caractère suivant le curseur.
            Donc, si le curseur est juste avant le caractère dont le 1er octet est le 10e, le pattern
            recherché est '\%10c...'.

            \%10c est un atome de largeur nulle / une ancre qui indique que le 1er octet du caractère
            suivant a pour index 10.
            Si aucun des 9 premiers caractères n'est multi-octets, ça revient à dire que le caractère
            suivant a pour index 10.

            . peut être n'importe quel caractère.
            En supposant qu'il n'y a pas de caractère multi-octets, '\%10c...' matchera les caractères
            occupant les colonnes 10, 11, 12 sur la ligne.


                                               NOTE:

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

            Basically, if there  is a column where no real  character resides in
            the file, between  2 other columns where there  ARE real characters,
            the column in the middle is NOT ignored.

            Although, I guess  it's ok to use `virtcol()` when  you're sure your
            lines are NOT wrapped.


    echo matchstrpos('testing', 'ing')
    ['ing', 4, 7]~

            'ing' est la sous-chaîne matchée par le pattern `ing`.
            4 est l'index de l'octet précédant le match.
            7 est l'index du dernier octet au sein du match.


                                               NOTE:

            `matchstrpos()` indexe un octet en commençant à compter à partir de 0.
            Idem pour toutes les fonctions acceptant en argument des index d'octets (ou de caractères),
            comme `match()`, `strcharpart()`, ....
            Idem qd on extrait un caractère d'une chaîne via un index:

                    echo matchstrpos('abcdef', 'd')
                    ['d', 3, 4]~
                    echo match('abcdef', 'd')
                    3~
                    echo 'abcdef'[3]
                    d~

            `col('.')` fait  exception, car qd  elle exprime la position  du curseur via  l'index de
            l'octet qui le suit, elle commence à compter à partir de 1.
            De même, dans un pattern de regex, qd l'atome `\%123c` exprime la position de l'octet suivant,
            il commence à compter à partir de 1.


    echo matchstrpos('testing', 'ing', 5)
    ['', -1, -1]~

            Il n'y a pas de match au delà du 4e octet.

    echo matchstrpos([1, '__x'], '\a')
    ['x', 1, 2, 3]~

                1 est l'index du 1er item où le pattern `\a` match.
                'x' est la sous-chaîne matchée.
                2 est l'index de l'octet précédant le match.
                3 est l'index du dernier octet au sein du match.


    nr2char(123)

            retourne le caractère n°123 dans l'encodage défini par 'encoding' (utf-8 chez moi)


    ┌──────────────────────────────┬─────────────────────────────────────────────────────────────────┐
    │ split('foo bar baz')         │ ['foo', 'bar', 'baz']                                           │
    ├──────────────────────────────┼─────────────────────────────────────────────────────────────────┤
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
    │ split('foo', '\zs')          │ ['f', 'o', 'o']                                                  │
    │                              │                                                                  │
    │                              │ Ça marche parce qu'en réalité '\zs' est probablement interprété  │
    │                              │ comme '.\zs'.                                                    │
    ├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
    │ split(getline('.'), '\W\+')  │ la liste des MOTS de la ligne courante                           │
    └──────────────────────────────┴──────────────────────────────────────────────────────────────────┘


    echo '12' + 3
    15      ✔~

    echo '1.2' + 3
    4       ✘~

    echo str2float('1.2') + 3
    4.2     ✔~

            La coercition par défaut d'une chaîne en  nombre est correcte pour un entier, mais pas
            pour un flottant. Pour ce dernier, il faut invoquer `str2float()`.


    echo '010' + 1
    9~

    echo str2nr('010') + 1
    11~

            Dans le 1er cas, le leading zero fait interpréter le nb comme étant octal (et 10 en base 8 = 8).
            Cette interprétation peut poser problème, notamment qd on réalise une substitution et
            qu'on utilise `submatch()` dans la chaîne de remplacement pour faire un calcul incluant
            un nb capturé dans le pattern.
            En effet, dans ce cas Vim va convertir la chaîne contenant le nb capturé en un nb en base 8.

            `str2nr()` résoud ce pb.
            Elle convertit une chaîne en nb et peut prendre un 2e argument optionnel correspondant
            à la base dans laquelle on veut que le nb soit interprété.
            Sans ce 2e argument, elle utilise la base 10 par défaut.



    strdisplaywidth("\t", col('.')-1)

            Retourne le nb de cellules qu'occuperait un caractère tab s'il était inséré après le curseur.


    echo strlen('exposé')
    7~
    echo strchars('exposé')
    6~

            Retourne la longueur en octets / caractères de la chaîne 'exposé' (7 octets; 6 caractères).


    echo strcharpart('résumé', 2, 1)
    s~
    echo strpart('résumé', 2, 1)
    <a9>~

            Retourne une sous-chaîne de string, commençant après:

                    • le 2e caractère et de longueur max 1
                    • le 2e octet     et de poids    max 1


    echo strcharpart('abcdefg', -2, 4)
    ab~
    echo strcharpart('abcdefg', 5, 4)
    fg~
    echo strcharpart('abcdefg', 3)
    defg~

            Retourne:

                    • 'ab'

                            caractère d'index -2 = '' (car n'existe pas)
                            caractère d'index -1 = ''
                            caractère d'index 0  = 'a'
                            caractère d'index 1  = 'b'

                            On remarque que `strcharpart()` n'interprète pas les index négatifs
                            comme le fait Vim qd on indexe directement une chaîne:

                                    echo strcharpart('abc', -1, 1)
                                    ∅~
                                    echo 'abc'[-1:-1]
                                    'c'~

                    • 'fg'

                            4 est trop grand, mais les caractères qui n'existent pas sont considérés
                            comme une chaîne vide.

                    • 'defg'

                            Sans longueur max, strcharpart() va jusqu'à la fin de la chaîne.


    tr('hello there', 'ht', 'HT')
    tr('<blob>', '<>', '{}')

            Retourne 'Hello THere' et '{blob}'.

            `tr()` permet de réaliser plusieurs substitutions en un seul appel de fonction.
            Elle TRaduit les caractères d'une chaîne en ceux d'une autre chaîne.

## Développement de noms de fichiers

Les wildcards suivants sont développés automatiquement dans les noms de fichier (:h wildcard):

    • ?       un caractère

    • *       n'importe quelle chaîne de caractères (le point EXCLU!)

    • **      n'importe quel chemin (le point INCLUS!)
              en l'absence de préfixe, vers un fichier du cwd ou l'un de ses sous-dossiers

    • [abc]   le caractère 'a', 'b' ou 'c'


    echo glob('%:t')        ✘
    echo glob('<cword>')    ✘

    echo expand('%:t')      ✔
    echo expand('<cword>')  ✔

            expand() est la seule à pouvoir développer les expressions '<cword>' et '%:t',
            car glob() ne peut produire que des chemins vers des fichiers EXISTANTS.


Vim développe automatiquement les caractères spéciaux au sein d'une commande :grep, juste avant d'exécuter
cette dernière.  Il les développe même s'ils sont encadrés par des single quotes.
Les quotes sont nécessaires qd on envoit leur développement au shell. Ex:

        :grep -R '<cword>' .

Ici, les single quotes empêchent le shell d'interpréter d'éventuels symboles spéciaux présents
dans le mot sous le curseur avant qu'il n'exécute la commande shell grep.
Mais ce n'est pas suffisant. En effet, si <cword> contient un single quote ce dernier sera mal
interprété par le shell. Il faut donc protéger <cword> avec un outil plus puissant: shellescape().
Exemple:

        :exe 'grep -R '.shellescape(expand('<cword>')) .

Dans ce nouvel exemple, on veut passer <cword> à shellescape() pour que tous ses caractères spéciaux
soient échappés, y compris un single quote.
Si on n'utilise pas expand(), Vim ne développera <cword> qu'au dernier moment, et donc shellescape()
ne recevra pas la chaîne contenant le mot sous le curseur mais la chaîne littérale '<cword>'.
Cette fois, les single quotes autour de <cword> ne servent plus à le protéger du shell
mais à obtenir une chaîne à passer à la fonction expand().

                                               FIXME:

Vim ne développe pas <cword> pour :echo. Normal, elle attend une expression et <cword> n'en est pas une.

Mais pk Vim développe <cword> pour :grep? D'après l'aide :grep attend des [arguments]...

Update:
D'après `:h :grep`:

        Just like ":make", but use 'grepprg' instead of
        'makeprg' and 'grepformat' instead of 'errorformat'.

Puis, d'après `:h :lmake`:

        Characters '%' and '#' are expanded as usual on a command-line.

Donc, `:make` développe des caractères spéciaux, et `:grep` se comporte comme `:make`.


                                     FIXME:

Avec `:vimgrep`, pk Vim ne développe <cword> que s'il n'est pas quoté?


    expand('$LANG')

            Retourne la valeur de la variable d'environnement $LANG du shell courant.

            Si la session Vim connaît déjà la variable d'environnement, il n'y a pas besoin d'appeler
            expand(): echo $LANG fonctionnera.

            Mais si elle ne la connaît pas, expand() permet de s'assurer qu'elle sera bien développée.
            Pour ce faire, elle lance un shell pour l'occasion.


                                               NOTE:

            expand() et glob() ne sont pas limités à des fichiers, elles peuvent développer:

                    • des caractères spéciaux (:h cmdline-special)
                    • des commandes shell
                    • des globs
                    • des variables d'environnement

            La seule restriction s'impose à glob(), qui rejette toute valeur ne correspondant pas à
            un chemin vers un fichier existant.


    ┌──────────────────┬────────────────────────────────────────────────────────────────────────┐
    │ expand('%')      │ chemin vers le vers fichier courant, relatif au cwd                    │
    ├──────────────────┼────────────────────────────────────────────────────────────────────────┤
    │ ...('%:t')       │ nom du fichier courant (tail of path)                                  │
    ├──────────────────┼────────────────────────────────────────────────────────────────────────┤
    │ ...('<cfile>:t') │ nom du fichier sous le curseur                                         │
    ├──────────────────┼────────────────────────────────────────────────────────────────────────┤
    │ ...('%:p:h')     │ chemin vers le dossier du fichier courant                              │
    ├──────────────────┼────────────────────────────────────────────────────────────────────────┤
    │ ...('%:h:t')     │ chemin vers le dossier parent du fichier courant (la queue de la tête) │
    └──────────────────┴────────────────────────────────────────────────────────────────────────┘


    ┌ développe un éventuel tilde ($HOME) à l'intérieur du précédent développement
    │      ┌ développe <cfile>
    │      │
    expand(expand('<cfile>'))
    glob('<cfile>')

            Retourne le chemin complet vers le fichier sous le curseur.


    expand('<sfile>')

            À l'intérieur d'une fonction, retourne le nom de la fonction, sous la forme:

                function MyFunc
                    ou
                function <SNR>3_MyFunc

            À l'intérieur d'un script (mais à l'extérieur d'une fonction), retourne le chemin vers le script.


                ┌─ respecte 'su' et 'wig'
                │  ┌─ résultat sous forme de liste et non de chaîne
                │  │
    expand('*', 0, 1)
    glob('*', 0, 1, 1)
                    │
                    └─ inclut tous les liens symboliques,
                       même ceux qui pointent sur des fichiers non-existants

            Noms des fichiers / dossiers du cwd.


                                               NOTE:

            Si le dossier de travail est vide, expand() retourne '*', glob() retourne ''.
            glob() est donc plus fiable.
            Ceci est une propriété générale de expand(). Qd elle ne parvient pas à développer qch,
            elle le retourne tq:

                    echo expand('$FOOBAR')
                    $FOOBAR~


    expand('**/README', 0, 1)
    glob('**/README', 0, 1, 1)

            Liste des chemins vers des fichiers README situés dans le cwd ou l'un de ses sous-dossiers.

            À nouveau, si aucun fichier n'est trouvé, expand() retourne ['**/README'],
            tandis que glob() retourne []. glob() est donc plus fiable.


    glob("`find . -name '*.conf' | grep input`", 0, 1, 1)
    expand("`find . -name '*.conf' | grep input`", 0, 1)
    systemlist("find . -name '*.conf' | grep input")

            Sortie de la commande shell:

                    $ find . -name '*.conf' | grep input

            Quelles différences? :

                • glob() ne retourne que des noms de fichier existants.
                  Elle filtre tout ce qui n'est pas exactement un nom de fichier exact.
                  Les messages d'erreurs sont donc supprimés.

                • expand() retourne la sortie brute du shell (erreurs incluses)

                • system() aussi, mais ajoute un newline à la fin, ce qui fait qu'on a une ligne vide
                  en bas du pager


    globpath(&rtp, 'syntax/c.vim', 0, 1, 1)

            Le chemin relatif `syntax/c.vim` est ajouté en suffixe à chaque chemin absolu du 'rtp'.
            Si le résultat correspond à un fichier existant, il est ajouté à une liste.
            `globpath()` retourne la liste finale, une fois que tous les chemins du 'rtp' ont été utilisés.


    globpath(&rtp, '**/README.txt', 0, 1, 1)

            Idem, sauf que cette fois, le suffixe contient un wildcard, qui à chaque fois est développé
            en une liste de 0, 1 ou plusieurs fichiers correspondant.


                                               NOTE:

            Plus généralement, globpath() attend 2 arguments, tous 2 des expressions évaluées en chaînes:

                    • la 1e doit stocker des chemins séparés par des virgules
                    • la 2e un chemin relatif vers un fichier, incluant éventuellement des wildcards


    substitute(glob2regpat(&wig), ',', '\\|', 'g')

        \.bak\|.*\.swo\|.*\.swp\|.*\~\|.*\.mp3\|.*\.png,...~

            `glob2repat()` convertit un pattern de fichier en un pattern de recherche.
            Utile qd on cherche un nom de fichier, dont le nom est écrit dans un buffer,
            et qui est décrit par un glob contenu dans une option tq 'wig'.

## Dictionnaires

    extend(adict, bdict, 'keep')

            ajoute toutes les entrées de bdict à adict

            Le 3e argument optionnel indique à extend() ce qu'il faut faire lorsqu'une entrée de bdict contient
            une clé déjà présente dans adict:

                'keep'     conserver l'entrée de adict
                'force'    la remplacer par celle de bdict (valeur par défaut si le 3e argument est omis)
                'error'    produire un message d'erreur

                                               NOTE:

            extend() n'est nécessaire que pour fusionner 2 dicos.
            Pour ajouter une nouvelle entrée, un :let mydict.key = 'value' suffit.


    filter(mydict, 'v:key =~ "^foo"')

            retourne le dictionnaire mydict après lui avoir supprimé tous les items dont la clé
            ne commence pas par foo


    get(mydic, 'key', -1)

            retourne la valeur de l'item dont la clé est 'key' dans mydic, et -1 s'il n'existe pas


    has_key(mydict, 'foo')

            retourne 1 si la clé 'foo' est présente dans mydict, 0 autrement


    let uk2fr = {'one': 'un', 'two': 'deux', 'three': 'trois',}

            exemple de définition d'un dictionnaire
            La forme générique étant: {<key> : <value>, ...}


    let mydict['key'] = 'value'
    let mydict.key = 'value'

            assigne à la clé 'key' de mydict la valeur 'value'
            Si aucune entrée n'utilise la clé 'key', elle est créée.


    mydict['foo']
    mydict.foo

            retourne la valeur associée à la clé 'foo' du dictionnaire mydict

            La 1e syntaxe autorise l'utilisation d'une plus grande variété de caractères
            (en + de ascii, chiffres et _).
            De plus, elle permet l'évaluation automatique d'une variable stockant une clé:

                mydict[myvar] ✔
                mydict.myvar ✘


    unlet mydict.key
    remove(mydict, key)

            Supprime l'entrée de `mydict` contenant la clé `key`.

            `remove()` retourne l'entrée supprimée qu'on peut ainsi capturer dans une variable:

                    let myvar = remove(mydict, key)

## Diverses

    inoremap <F2> <C-R>=CustomMenu()<cr>
    fu! CustomMenu()
        call complete(col('.'), ['foo', 'bar', 'baz'])
        return ''
    endfu

            Ce bout de code montre comment utiliser la fonction complete() pour se créer un menu
            de complétion custom.
            Ici, en appuyant sur <F2>, un menu dont les items sont foo, bar et baz s'affichera.

            Le 1er argument précise à partir d'où l'item choisi sera inséré sur la ligne.
            On pourrait lui donner comme valeur:

                    • col('.')

                            ne remplace rien; insertion à partir du curseur

                    • col('.') - 3

                            remplace les 3 derniers caractères

                    • col('.') - len(matchstr(getline('.')[:col('.')-2], '\S\+'))

                            remplace le texte devant le curseur;
                            le texte étant défini comme une séquence de non-whitespace

            Bien sûr, la fonction CustomMenu() pourrait utiliser/construire n'importe quelle liste
            contenant les items qu'on souhaite pouvoir insérer automatiquement.
            Pex, la liste des contenus des registres.

            Toutefois, si ceux-ci contiennent des LF, le menu les traduit en NUL.
            Peut-être car `complete()` n'est pas censée accueillir des items multi-lignes.

            On notera également l'instruction return '' qui est nécessaire pour éviter que `CustomMenu()`
            ne retourne le code de sortie 0 qui serait alors automatiquement inséré à la suite du 1er
            item (foo0), sans que le menu ne s'affiche.


    if [!]empty(expr)

            teste si expr est vide en retournant le nombre 1 si expr est vide, 0 autrement (! inverse le test)

            expr peut être une chaîne, une liste, un dictionnaire ou un nb (vide = 0)


    if exists('*myfunc')
    if exists(':cmd')
    if exists('#current_word#CursorHold')

            Teste l'existence de:

                • d'une fonction du nom de `myfunc`

                • de la commande Ex `:cmd`

                • d'une autocmd dans l'augroup `current_word` surveillant l'évènement `CursorHold`


    if has('gui_running')

            teste si Vim tourne en gui

            la liste des fonctionnalités supportées par Vim est lisible via: :h feature-list

    iconv(string, 'latin1', 'utf-8')

            la chaîne string étant encodée en latin1, retourne cette même chaîne encodée en utf-8


    confirm('Are you sure?', "&yes\n&no\n&quit", 2)

            Affiche une ligne affichant le message 'Are you sure?', propose à l'utilisateur
            un choix entre 'yes', 'no' et 'quit', attend  que l'utilisateur tape 'y', 'n' ou 'q'
            et retourne le n° du choix.
            Le choix par défaut, si on appuie seulement sur Enter, est 'no' (3e argument: 2).

            Les choix doivent être séparés par des \n.
            Pour un choix donné, on peut choisir quelle lettre permet de le sélectionner en la faisant
            précéder de &.
            Retourne 0 si l'utilisateur appuie sur C-c ou Esc.


    let password = inputsecret('Enter sudo password:') . "\n"
    echo system('sudo -S aptitude install package', password)

            inputsecret() est similaire à input() à ceci près que les caractères tapés sont affichés
            sous la forme d'astérisques, et que la saisie n'est pas sauvegardée dans l'historique:
            histget('@')

            `system()` écrit sur l'entrée standard de `sudo`.

            Pb:          par défaut, `sudo` ne lit pas son entrée standard, mais le terminal.
            Solution:    utiliser le flag `-S` (--stdin)
                         Ce flage demande à `sudo` qu'il lise le mdp sur son entrée standard,
                         et qu'il écrive son prompt sur l'erreur standard.

            Le mdp doit être suivi d'un newline (sans doute pour valider).
            En pratique, ça a l'air de fonctionner même sans newline à la fin.

            On pourrait simplement `:call` la fonction `system()`, mais en utilisant `:echo`,
            on peut lire la sortie de la commande shell et ainsi vérifier que l'installation
            du paquet s'est bien passée.

                                               NOTE:

            En pratique, il vaut mieux éviter ces commandes, car on ne peut pas répondre à d'éventuelles
            questions au cours de l'installation (pex pour résoudre des pbs de dépendances).


    let choice = inputlist(['Select color:', '1. red', '2. green', '3. blue'])
    if choice >= 1 && choice <= 3
        let color  = ['red', 'green', 'blue'][choice - 1]
    endif

            stocke dans la variable `color` un des items de la liste ['red', 'green', 'blue'],
            choisi via un menu interactif

            Dans l'exemple précédent, si l'utilisateur veut choisir la couleur verte, il entrera le nb 2.
            Du coup on obtiendra:

                    let color = ['red', 'green', 'blue'][2-1] = 'green'

            Il peut être utile de mettre un prompt comme 1er item (ou alors faire un :echo 'message' avant),
            et de préfixer les autres par un nb pour que l'utilisateur sache exactement quoi taper.

            La taille de la liste passée en argument à inputlist() et ce qu'elle contient n'a pas d'importance,
            elle ne sert qu'à informer l'utilisateur des nb qu'il peut taper et leur conséquence.


    mapcheck('<C-G>', 'c')

            retourne le {rhs} du mapping dont le {lhs} est C-g

    setcmdpos(6)

            positionne le curseur juste avant le 6e octet sur la ligne de commande

            Si aucun des 5 premiers caractères de la ligne de commande n'est multi-octets,
            positionne le curseur juste avant le 6e caractère.

            Ne fonctionne que lorsqu'on édite la ligne de commande:

                    • en y insérant l'évaluation d'une expression via C-r
                    • en la remplaçant entièrement par l'évaluation d'une expression via C-\ e

            Je n'ai pas réussi à l'utiliser directement au sein du (pseudo?) registre expression
            dans lequel on entre qd on tape C-r ou C-\ e.
            En revanche, elle fonctionne correctement qd on évalue une fonction custom juste après.

            Qd on évalue une fonction custom:

                • via C-\ e, setcmdpos() permet de positionner le curseur sur la nouvelle ligne de
                  commande, l'ancienne étant remplacée par l'évaluation

                • via  C-r, setcmdpos()  permet  de positionner  le curseur  sur  l'ancienne ligne  de
                  commande (qui n'est  pas remplacée), avant que l'évaluation ne soit insérée là où se
                  trouve le curseur

            Qd on utilise  C-\ e ou C-r = pour  évaluer une fonction custom, il ne  sert à rien de
            demander  à cette  dernière de  retourner des  caractères de  contrôle tq  <cr> pour
            exécuter la ligne de commande ou <Left>, <Right> pour déplacer le curseur.

            En effet, C-\ e  et C-r ne peuvent qu'insérer des caractères,  donc des caractères de
            contrôle seraient insérés littéralement et non interprétés comme des commandes.

            Si on  veut déplacer le  curseur sur  la ligne de  commande après que  les caractères
            retournés par la fonction custom aient été insérés, il faut utiliser soit:

                    • setcmdpos() au sein de la fonction custom

                    • des <left>, <right> après que la fonction custom ait été évaluée; pex au sein d'un mapping:

                            cno <f8> <c-\>e MyFunc()<cr><left><left>

            On ne rencontrerait pas ce pb avec  un mapping auquel on passerait l'argument <expr>, et
            auquel on demanderait de taper les touches retournées par une fonction custom.

            Dans  ce cas,  les touches  de contrôle  ne  seraient pas  insérées sur  la ligne  de
            commande, mais interprétées comme des actions (validation, mouvement).

                                               NOTE:

            La position du curseur via `setcmdpos()` n'est pas établie au même moment selon qu'on
            utilise `C-r =`  ou  `C-\ e` / `C-r C-r =`:

                    • C-r =        après avoir évalué l'expression, MAIS AVANT de l'insérer

                    • C-r C-r =    après avoir évalué l'expression
                      C-\ e


    submatch()

            À l'intérieur d'une expression de remplacement, permet d'accéder à tout ou partie texte
            matché par le pattern.

            submatch(0) = tout le texte
            submatch(1) = 1ère sous-expression capturée

            On peut utiliser une expression de remplacement (et donc submatch()) dans une commande de substitution:

                    :s:pattern:\=expression:

            ou dans la fonction substitute():

                    substitute('text', 'pattern', '\=expr', 'flags')


                                               NOTE:

            Si on utilise des double quotes pour '\=expr', bien penser à doubler les backslashs
            à l'intérieur y compris le 1er: "\\=expr"


                                               NOTE:

            Alternativement, on peut remplacer '\=expr' par une expression lambda :

                    substitute('text', 'pattern', {-> expr}, 'flags')


    system('cmd')
    system('cmd', 'input')

            retourne la sortie de la commande shell cmd (en écrivant 'input' sur son entrée standard)

    system('ls -l '.expand('%:p'))

            retourne un listing détaillé (ls -l) du fichier courant

            Cette commande illustre le fait que Vim peut évaluer une concaténation de chaînes avant
            d'en passer le résultat à une fonction acceptant une expression comme argument.
            En effet, une concaténation d'expressions est une expression.


    system('tmux send-keys -t 1.2 "echo hello" Enter')

            exécute la commande shell `$ echo hello` dans le 2e pane de la 1e fenêtre de la session
            tmux courante


    tabpagenr()
    tabpagenr('$')

            retourne le n° de l'onglet courant; du dernier onglet


    exe (tabpagenr()-1).'tabnew'

            ouvre un nouvel onglet juste avant l'onglet courant


    taglist('pattern')

            Retourne la liste des tags matchant pattern.

            Chaque item de la liste est un dictionnaire, contenant entre autres les clés `name` et `filename`.


    taglist('pattern')[0].name
    taglist('pattern')[0].filename
    map(taglist('pattern'), 'v:val.name')

            retourne le nom:

                    • du 1er tag                         matchant pattern
                    • du fichier contenant le 1er tag    "
                    • des noms de tous les tags          "

    visualmode()

            retourne le type de la dernière sélection visuelle dans le buffer courant ('v', 'V', '^V')

            Utile pour passer en argument le type de la dernière sélection à une fonction souhaitant
            agir sur cette dernière.
            Par exemple , si visualmode() retourne 'v' la fonction utilisera les marques `< et `>,
            et si elle retourne 'V' la fonction utilisera les marques '< et '>.

## Expression lambda / closure

Document the fact that when you save  a lambda or funcref inside a function, you
should always  use the scope  `l:`, otherwise there could  be a conflict  with a
public custom function.

Review this section, and add `l:` whenever it makes sense.

---

    {args -> expr}

Il  s'agit d'une  expression lambda,  qui crée  une nouvelle  fonction numérotée
retournant l'évaluation d'une expression.
Elle diffère d'une fonction régulière de 2 façons:

   • Le corps de l'expression lambda est une expression et non une séquence de
     commandes Ex.

   • Les arguments ne sont pas dans le scope `a:`.

---

    let F = {arg1, arg2 -> arg1 + arg2}
    echo F(1,2)
    3~

---

    fu! A()
        return 'i am A'
    endfu
    fu! B()
        let A = {-> 42}
        return A()
    endfu
    echo B()
    E705: Variable name conflicts with existing function: A~

    fu! A()
        return 'i am A'
    endfu
    fu! B()
        let l:A = { -> 42 }
        return l:A()
    endfu
    echo B()
    42~

Qd  on  se trouve  à  l'intérieur  d'une fonction,  et  qu'on  doit stocker  une
expression  lambda, ou  une funcref,  dans une  variable, il  faut toujours  lui
donner le scope `l:`.
En effet, le nom doit commencer par  une majuscule, ce qui pourrait provoquer un
conflit entre avec une fonction publique de même nom.

---

    let F = { -> 'hello'.42 }
    echo F()
    hello42~

Une expression lambda peut ne pas avoir d'arguments.

---

    {'<lambda>42'}

Le nom de la fonction numérotée créée par une expression lambda suit ce schéma.
En cas d'erreur au sein de cette dernière, on pourra donc exécuter:

    fu {'<lambda>42'}

... pour lire son code:

                    let F = {-> 'hello'.[42]}
                    echo F()
                    E15: Invalid expression: <lambda>15    ✘~

---

    echo map([1, 2, 3], {i,v -> v + 1})
    [2, 3, 4]~

    echo sort([3,7,2,1,4], {a,b -> a - b})
    [1, 2, 3, 4, 7]~

On peut,  entre autres,  utiliser des  expressions lambda  comme 2e  argument de
`filter()`, `map()` et `sort()`.

---

    let timer = timer_start(500, {-> execute("echo 'Handler called'", '')}, {'repeat': 3})
    Handler called~
    Handler called~
    Handler called~

Les expressions lambda sont aussi utiles pour des timers, canaux, jobs.

---

Si un timer est  exécuté au moment où on se trouve sur  la ligne de commande, le
curseur peut temporairement quitter cette dernière et s'afficher dans le buffer.

    nno <expr> cd Func()
    fu! Func()
        let my_timer = timer_start(2000, { -> execute('sleep 1', '') })
        return ''
    endfu

Taper `cd`, puis écrire qch sur la ligne de commande et attendre.

---

    ✘
    call timer_start(0, {-> execute('call FuncA() | call FuncB()')})
    ✔
    call timer_start(0, {-> FuncA() + FuncB()})

    ✘
    call timer_start(0, {-> execute('if expr | call Func() | endif')})
    ✔
    call timer_start(0, {-> expr ? Func() : 0})
    ✔✔
    call timer_start(0, {-> expr && Func()})

    ✘
    call timer_start(0, {-> execute('if expr | call FuncA() | endif | call FuncB()})
    ✔
    call timer_start(0, {-> (expr ? FuncA() : 0) + FuncB()})
    ✔✔
    call timer_start(0, {-> (expr && FuncA()) + FuncB()})

On  n'a  pratiquement  jamais  besoin d'utiliser  `execute()`  et  `:call`  pour
exécuter une fonction via un lambda.

`:call` est nécessaire sur la ligne de  commande car Vim s'attend à exécuter une
commande.
`:call` n'est pas toujours nécessaire dans un lambda, car Vim s'attend à évaluer
une expression, et une fonction EST un type d'expression.

---

Qd  on exécute  une fonction  via  un lambda,  sa  valeur de  sortie n'a  aucune
importance.

---

N'utilise `||` et `&&` comme connecteur  logique que lorsque c'est nécessaire et
qu'ils correspondent réellement à ce que tu veux faire.
Autrement, préfère un opérateur plus simple tq `+`:

                           exécute 2 fonctions
    ┌────────────────────┬─────────────────────────────────────────┐
    │ FuncA() && FuncB() │ à condition que la 1e ait réussi        │
    ├────────────────────┼─────────────────────────────────────────┤
    │ FuncA() || FuncB() │ à condition que la 1e ait échoué        │
    ├────────────────────┼─────────────────────────────────────────┤
    │ FuncA() + FuncB()  │ peu importe que la 1e ait réussi ou non │
    └────────────────────┴─────────────────────────────────────────┘

---

        expr && FuncA() + FuncB()
    ⇔
        exécute `FuncA` ET `FuncB` à condition que `expr` soit vraie


        (expr && FuncA()) + FuncB()
    ⇔
        exécute `FuncA` à condition que `expr` soit vraie, PUIS `FuncB`


Cette différence découle du fait que l'opérateur `+` a priorité sur `&&`.

Confirmation via:

    echo 0 && 1 + 1
    0~

    echo (0 && 1) + 1
    1~

---

    echo map(range(65, 90), {x -> nr2char(x)})
    [ 'A', 'B', ... ]          attendu~
    [ '', '^A', '^B', ... ]    obtenu~

Pk n'obtient-on pas la liste des lettres majuscules ?
Car  qd  le 2e  argument  de  `map()` est  une  funcref,  `map()` lui  envoit  2
arguments:

   1. l'index (pour une liste) ou la clé (pour un dico) de l'item courant
   2. la valeur de l'item courant

`map()` utilise ensuite la fonction associée  à la funcref pour remplacer chaque
item de la liste.

Donc, dans l'exemple précédent, pour remplacer les nbs 65 à 90, `map()` envoit à
`nr2char()` les valeurs suivantes:

   • nr2char(0, 65)
   • nr2char(1, 66)
     ...
   • nr2char(25, 90)

Or, pour `nr2char()`, le 2e argument est un simple flag:

   • 0 signifie qu'on veut utiliser l'encodage courant

   • 1 l'encodage utf-8

`65` ... `90` sont interprétés comme un `1`.

De plus, `nr2char()` ne reçoit pas les bons codepoints:

    65 ... 90  ✔ ce qu'ell devrait recevoir
    0  ... 25  ✘ ce qu'elle reçoit

Solution:

    map(range(65,90), {i,v -> nr2char(v)})
                       ^^

Conclusion:

Pour pouvoir se  référer à un argument  reçu par une expression  lambda, il faut
correctement tous les déclarer.
Donc,  qd une  fonction  accepte  une expression  lambda  en argument,  toujours
regarder quels arguments elle envoit à cette dernière.
Ici, `map()` n'en envoit pas 1 (`x`), mais 2 (`i`, `v`).


    fu! Foo(arg)
        let i = 3
        return {x -> x + i - a:arg}
    endfu
    let Bar = Foo(4)
    echo Bar(6)
    5~

L'expression lambda utilise dans son calcul les variables `i` et `a:arg`.

`i` appartient  à la portée  locale à `Foo()`,  tandis que `a:arg`  appartient à
celle des arguments de `Foo()`.
L'expression lambda ne se plaint pas que les variables ne sont pas définies :

    E121: Undefined variable: i~
    E121: Undefined variable: a:arg~

... car elle  a la particularité de  pouvoir accéder aux variables  de la portée
extérieur; on parle de “closure“ (clôture).


    fu! Foo()
        let x = 0
        fu! Bar() closure
            let x += 1 " pas d'erreur, grâce à `closure`
            return x
        endfu
        return funcref('Bar')
    endfu

    let F = Foo()
    echo F()
    1~
    echo F()
    2~
    echo F()
    3~

L'incrémentation  de `x` au sein de `Bar()` ne soulève pas d'erreur:

    E121: Undefined variable: x~

...  car  `Bar()`  porte  l'attribut  `closure` qui  lui  permet  d'accéder  aux
variables de la portée extérieure (`Foo()`).

La sortie de `F()` est incrémentée à chaque appel.
Ceci prouve  qu'une fonction  portant l'attribut `closure`  peut continuer  à se
référer à la portée d'une fonction  extérieur même après qu'elle ait terminé son
exécution.

## Fenêtres / Onglets

    getwinvar('%', '')

            retourne un dictionnaire contenant toutes les variables locales à la fenêtre courante
            ainsi que leurs valeurs

            `getwinvar()` permet d'accéder à la valeur d'une variable ou option locale à une fenêtre.
            Ne fonctionne pas pour une option locale à un buffer (utiliser getbufvar() pour ça).

                                     TODO:

            Parler de `gettabwinvar()` qui permet aussi d'obtenir une variable locale à une fenêtre
            mais pas forcément dans l'onglet courant (dans celui de son choix).
            Parler aussi de `gettabvar()` pour obtenir une variable locale à un onglet.

            Parler aussi de `getwininfo()`.


    bufwinnr('%')
    bufwinnr('#')
    bufwinnr('$')
    bufwinnr(3)

            Retourne le n° de la 1e fenêtre dans l'onglet courant qui affiche:

                    • le buffer courant
                    • l'alternate buffer
                    • le dernier buffer listé
                    • le buffer n° 3

            Si le buffer n'existe pas ou n'est affiché dans aucune fenêtre de l'onglet courant,
            -1 est retourné.


    if bufwinnr(42) > 0

            Teste si le buffer n°42 est affiché dans une fenêtre de l'onglet courant.


    if !empty(win_findbuf(42))

            Teste si le buffer n°42 est affiché dans une fenêtre qcq (dans n'importe quel onglet).

            `win_findbuf(42)` retourne une liste d'identifiants de fenêtres affichant le buffer n°42.


    win_getid()
    win_getid([2])
    win_getid([4, 3])

            Retourne l'id de la:

                    • fenêtre courante
                    • 2e fenêtre de l'onglet courant
                    • 3e fenêtre du 4e onglet

            L'id d'une fenêtre est absolu, contrairement à son n° (donné par `winnr()`) qui lui est
            local à l'onglet.


    call win_gotoid(42)
         win_id2win(42)
         win_id2tabwin(42)

            donne le focus                      à la fenêtre d'id 42
            retourne le n° (!= id)              de la "
            retourne la liste [tabnr, winnr]    "

            `win_id2win()` ne retourne le n° de la fenêtre que si on se trouve dans son onglet.
            Autrement, elle retourne 0.


    win_getid(1, 1)

            retourne l'id de la fenêtre de n° 1 dans l'onglet 1


    winnr()    winnr('#')    winnr('$')

            retourne le n° de:

                    • la fenêtre courante
                    • la dernière fenêtre visitée
                    • la dernière fenêtre de l'onglet courant

            Le n° est local à l'onglet.

                                               NOTE:

            On remarque que le caractère spécial # n'a pas le même sens pour winnr() et bufwinnr().
            Pour winnr() il s'agit de la dernière fenêtre visitée, et pour bufwinnr() celle affichant
            l'alternate buffer.

            De même, $ est interprété comme la dernière fenêtre par winnr(), mais comme le dernier buffer
            listé par bufwinnr().

            Enfin, `winnr() != bufwinnr('%')`, car:

                    • winnr()    = n° de la fenêtre courante
                    • bufwinnr() = n° de la 1e fenêtre affichant le buffer courant

                                     TODO:

            Parler aussi de tabpagenr() qui fait qch de similaire: retourner le n° d'un onglet.
            À ceci près qu'il n'accepte pas '#' comme argument; soit rien, soit '$':

                    tabpagenr()       n° onglet courant
                    tabpagenr('$')    n° dernier onglet

            Parler aussi de tabpagewinnr(): retourne le n° d'une fenêtre dans un onglet de son choix.


    @=winnr('#') CR C-w c      mode normal
    :exe winnr('#').'close'    mode Ex

            Fermer la dernière fenêtre qu'on a visité dans l'onglet courant.


    let view = winsaveview()

            sauvegarde l'état de la fenêtre (position du curseur, de la fenêtre...) dans la variable `view`

            winsaveview() retourne un dictionnaire


    call winrestview(view)

            restaure l'état de la fenêtre à partir des informations du dictionnaire stocké dans `view`

                                               NOTE:

            Si la partie du buffer affichée par la fenêtre est pliée, avant d'utiliser cette fonction,
            il faut la déplier (`:norm! zv`).

            Autrement, la position de la ligne courante au sein de la fenêtre est perdue, car Vim
            la positionne au centre de cette dernière peu importe sa position d'origine
            (en haut/bas de la fenêtre ...).

            Le pb vient du fait que winsaveview() ne sauvegarde pas les informations relatives au pliage.

## Fichiers

    delete(fname)

            supprime le fichier `fname`

            Retourne 0 si la suppression a réussie, -1 autrement.

    delete(dir, 'd')

            supprime le dossier `dir`

            Échoue si `dir` n'est pas vide.

    delete(dir, 'rf')

            supprime le dossier `dir` et tout ce qu'il contient, récursivement

            Un lien symbolique est supprimé, mais pas ce sur quoi il pointe.


    escape(file, ' \')

            échappe les espaces et les backslash dans le nom de fichier file
            plus généralement tous les caractères présents dans le 2e argument de escape() sont échappés


    if filereadable('/path/fo/file')

            teste si /path/to/file PEUT ÊTRE LU (et donc aussi son existence)

            Ce test peut s'écrire simplement comme ça car le code de retour de filereadable()
            en cas d'échec est 0. Si c'était -1, il faudrait obligatoirement comparer la sortie à -1.


    if !empty(glob('/path/to/file'))

            TESTE L'EXISTENCE de /path/to/file (fonctionne même si on n'a pas les droits pour le lire)

            Ce test peut s'écrire simplement comme ça car le code de retour de empty()
            en cas d'échec est 0. Si c'était -1, il faudrait obligatoirement comparer la sortie à -1.

            Pour tester l'existence d'un fichier, il faut utiliser cette syntaxe, et non `filereadable()`.


    fnamemodify('fname', ':p:h')

            Retourne le chemin absolu vers le dossier contenant le fichier fname.

            Où la fonction cherche-t-elle le dossier contenant fname ?
            Probablement dans les dossiers de 'path'.

            Cette fonction permet de modifier le nom d'un fichier/dossier à partir de certains
            modificateurs dont la liste est lisible via :h filename-modifiers.
            Les plus utiles sont:

            ┌──────────────┬────────────────────────────────────────────────────────────────────────────┐
            │ :~           │ preserve home                                                              │
            │              │ ne développe pas ~; doit être utilisé avant les autres                     │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :.           │ réduit le chemin de sorte qu'il soit relatif au cwd                        │
            │              │ si c'est possible càd si le fichier courant est sous le cwd                │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :~:.         │ chemin réduit au max                                                       │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :h           │ chemin relatif au cwd, sans le dernier noeud                               │
            │              │ répétable (ex:  :h:h  pour obtenir le dossier du dossier)                  │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :t           │ fichier                                                                    │
            │              │ complément de :h                                                           │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :e           │ extension                                                                  │
            │              │ répétable (ex:  :e:e  pour obtenir les 2 dernières extensions)             │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :r           │ supprime l'éventuelle extension du fichier +   chemin relatif au cwd       │
            │ :p:r         │                                                chemin absolu               │
            │ :t:r         │                                                pas de chemin               │
            │              │                                                                            │
            │              │ répétable, ex:  :r:r  →  supprime les 2 dernières extensions               │
            │              │ complément de :e                                                           │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :e:e:r       │ avant-dernière extension                                                   │
            │              │                                                                            │
            │              │ ex:  e foo.tar.gz                                                          │
            │              │      expand('%:e:e:r')  →  tar                                             │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :p           │ chemin absolu complet                                                      │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :S           │ escape special characters for use with a shell command                     │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :s?pat?sub?  │ substitue la 1e occurrence de pat par sub                                  │
            ├──────────────┼────────────────────────────────────────────────────────────────────────────┤
            │ :gs?pat?sub? │ substitue toutes les occurrences de pat par sub                            │
            └──────────────┴────────────────────────────────────────────────────────────────────────────┘


    fnamemodify(myvar, ':p')

            Retourne le chemin complet vers le fichier/dossier dont le chemin est stocké dans `myvar`.

            La fonction expand() permet aussi de modifier des noms de fichiers mais uniquement ceux
            exprimés via des caractères spéciaux (%, #, <cfile>).

            fnamemodify() est donc + puissante, elle peut même agir sur des noms de fichiers inexistants.
            Ex:

                    :echo fnamemodify('UnexistingFile', ':p')

            ... marche même si `UnexistingFile` n'existe pas.


    echo fnamemodify('/foo/bar/baz/', ':t')
    ''~
    echo fnamemodify('/foo/bar/baz/', ':h:t')
    baz~
    echo fnamemodify('/foo/bar/baz', ':t')
    baz~

            `:h` removes the last path component.
            But the last path component can be empty, if the last character of the path is `/`.


    :exe 'e '.fnameescape('fname')

            Exécute la commande  Ex ':edit fname' en ayant  échappé les symboles
            spéciaux que fname contient.
            Si  fname contient  un %  ou un  |, ça  permet d'éviter  que Vim  ne
            développe ces symboles.


    !isdirectory(expand('$HOME') . '/dir')

            teste la non-existence du dossier /home/user/dir

            Ce test peut s'écrire simplement comme ça car le code de retour de isdirectory()
            en cas d'échec est 0. Si c'était -1, il faudrait obligatoirement comparer la sortie à -1.


    mkdir(expand('$HOME').'foo/bar', 'p')

            crée le dossier /home/user/foo/bar, en créant les dossiers intermédiaires si nécessaire
            (2e argument 'p')


    readfile('/tmp/foo')
    readfile(fname, '', 10)
    readfile(fname, '', -10)

            Retourne une liste dont les items sont des lignes du fichier `/tmp/foo`:

                    • toutes
                    • les 10 premières
                    • les 10 dernières


    let words = split(join(readfile('/tmp/foo'), "\n"), '\W\+')

            stocke dans la variable words une liste contenant le 1er mot de chaque ligne du fichier /tmp/foo

            Ceci illustre comment on peut utiliser la fonction split() pour récupérer toutes les occurrences
            d'un pattern. Ne fonctionne que si on peut facilement décrire l'inverse du pattern.
            Ici on cherche des mots (\w\+), l'inverse est donc facile à décrire \W\+.

            On aurait aussi pu utiliser:    [^a-zA-Z_0-9\d192-\d255]
            Pour trouver des mots dont les caractères sont présents dans 'isk'.


    shellescape(fname, 1)

            protège un nom de fichier qui doit être passé en argument à une commande shell

            La protection consiste à mettre des single quotes autour de fname et à échapper d'éventuels
            single quotes si fname en contient.

            Qd le 2e argument optionnel est non nul, les symboles appartenant à [!%#<] sont échappés.
            Lorsque `shellescape(fname, 1)` sera envoyée au shell, via :! ou :grep,
            sur la ligne de commande Ex, Vim enlèvera les backslashs sans développer les caractères
            spéciaux.

                                               NOTE:

            La règle à retenir est la suivante:

            Qd on veut protéger des caractères spéciaux:

                    • de Vim,             il faut utiliser `fnameescape(...)`
                    • du shell,           "                `shelleescape(...)`
                    • du shell ET de Vim, "                `shellescape(..., 1)`

                                               NOTE:

            `fname` pourrait être autre chose qu'un nom de fichier: pex un nb en hexa
            (commençant donc par un dièse), qu'on souhaite passer à une commande shell:

                    exe '!shell_cmd ' . shellescape('#' . l:mycolor, 1)


    :let @" = 'foo;ls'     | exe 'grep! '.shellescape(@",1).' .'
    :let @" = "that's"     | ...
    :let @" = 'foo%bar'    | ...

            Même si `:grep` est une commande Vim, qd on lui passe une chaîne pouvant contenir
            des caractères spéciaux, il faut utiliser `shellescape()`, et PAS `fnameescape()`.

            Voici la sortie de différentes fonctions, suivant le contenu du registre `z`:

                    ┌───────────────────┬──────────┬─────────────┬────────────┐
                    │                   │ foo;ls   │ that's      │ foo%bar    │
                    ├───────────────────┼──────────┼─────────────┼────────────┤
                    │ fnameescape(@")   │ foo;ls   │ that\'s     │ foo\%bar   │
                    │ shellescape(@")   │ 'foo;ls' │ 'that'\''s' │ 'foo%bar'  │
                    │ shellescape(@",1) │ 'foo;ls' │ 'that'\''s' │ 'foo\%bar' │
                    └───────────────────┴──────────┴─────────────┴────────────┘

            On remarque que `fnameescape()` ne protègerait pas `;`.
            Le shell l'interprèterait comme une fin de commande, et exécuterait le reste
            comme s'il s'agissait d'une autre commande.
            C'est DANGEREUX.
            Imaginons que `@"` contienne la chaîne suivante:

                    foo;rm -rf

            Au lieu de chercher "foo;rm -rf", le shell exécuterait `$ grep foo`, PUIS `rm -rf`.


    system('chmod +x -- ' . shellescape(expand('%')))

            retourne la sortie de la commande shell:

                    $ chmod +x -- 'foo bar'

            'foo bar' étant le nom du buffer courant

                                               NOTE:

            Il existe 2 différences entre les syntaxes:

                    :!exe {expr}
            et
                    :call system({expr})


            • system() permet de capturer la sortie du shell dans une variable ou de la passer
              à une autre commande Vim

            • system() ne lance pas de terminal, elle passe la commande shell directement à un processus
              shell;    :!exe    lance un émulateur de terminal au sein duquel tourne un shell

              Ceci peut avoir son importance si on a besoin d'interagir avec la commande shell.
              C'est le cas pex avec le pgm ranger (file manager).
              On ne peut pas le lancer via system(), car dans ce cas ranger se plaindrait qu'il
              a besoin d'être exécuté depuis un terminal.


    tempname()
    let tmpfile = tempname()

            Retourne / capture le nom d'un fichier temporaire. Ex:

                    /tmp/abcd123/0

            Le dossier le contenant est automatiquement créé dans les 2 cas.


                                               NOTE:

            Le simple fait d'invoquer la commande shell `mktemp` provoque également la création d'un
            dossier temporaire par Vim:

                    echo expand('`mktemp -d /tmp/.pgm.XXXXXXXXXX`')
                    /tmp/abcd123/ + /tmp/.pgm.abcdef12345~
                    call system('mktemp -d /tmp/.pgm.XXXXXXXXXX')
                    /tmp/abcd123/ + /tmp/.pgm.abcdef12345~

            Toutefois, on préfèrera utiliser `tempname()`, car qd on le réinvoquera, Vim créera tous
            les fichiers suivants dans le même dossier.
            De plus, qd on quittera Vim, il supprimera automatiquement le dossier.


    writefile(['foo', 'bar'], 'file', 'a')

            ajoute à la fin du fichier file les chaînes 'foo' et 'bar', séparé par un newline
            le 3e argument 'a' est un flag qui indique à la fonction d'ajouter (append) les chaînes
            au fichier sans écraser son contenu

## Historique

    histadd('/', strftime('%c'))

            ajouter dans l'historique de recherche la date du jour

                                               NOTE:

            Il existe d'autres historiques qu'on peut manipuler via histadd(), histdel(), histget() et histnr():

                : ou cmd       ligne de commande
                / ou search    recherche
                = ou expr      registre expression
                @ ou input     dernières valeurs fournies à la fonction input()
                > ou debug     commandes de déboguage

    histdel('/')    histdel('/', -1)    histdel('/', '^a.*b$')

            supprimer de l'historique de recherche:

                    • toutes les entrées
                    • la dernière entrée
                    • toutes les entrées commençant par a et finissant par b

    histget('/', 5)    histget('/')

            retourne la 5e entrée de l'historique de recherche; la dernière entrée

                                               NOTE:

            • on peut fournir un n° d'index absolu (nb positif), ou relatif par rapport à la fin
              (nb négatif, -1 = dernière entrée)

            • l'index absolu d'une entrée dans l'historique de recherche ne correspond pas forcément
              au n° de la ligne sur laquelle il est présent dans la fenêtre qui pop via q/

    histnr('/')

            retourne le n° d'index de la dernière entrée dans l'historique de recherche


    :search something | call histdel('/', -1) | let @/ = histget('/')

            supprime la dernière recherche, et restocke dans le registre recherche l'avant-dernière
            utile après une recherche dont on ne souhaite laisser aucune trace (ou alors utiliser :keeppatterns)

## Listes

Pour vimscript,  les listes  sont des objets  mutables. On  peut modifier un  item d'une  liste sans
devoir remplacer toute la liste.


    add(list, item)

            ajoute item à list (opération in-place)
            l'item peut être un nb, une chaîne, une liste, un dictionnaire

            retourne la liste qui résulte de l'opération

                                               NOTE:

            Si l'item est une liste, il est ajouté en tant que simple item de list (pas de concaténation).
            Ex:
                    :let alist = ['one']
                    :call add(alist, ['two', 'three'])
                    :echo alist
                    ['one', ['two', 'three']]


             ┌ Array
             │
    call add(a, remove(a, 0))
    call insert(a, remove(a, -1), 0)

            Effectue une rotation sur les éléments de `a`, in-place:

                    • vers la gauche
                    • vers la droite

            Utile entre autres pour remplacer un pattern avec différentes chaînes:

                    %s/pat/foo/
                    %s/pat/bar/
                    %s/pat/baz/

                    let a = ['foo', 'bar', 'baz']
                    %s/pat/\=add(a, remove(a, 0))[-1]/

            Si la liste  ne contient que 2 éléments, on  peut simplifier le code
            en utilisant seulement la fonction `reverse()`:

                    let a = ['bar', 'foo']
                    %s/pat/\=reverse(a)[0]/


    count(list, value)

            Retourne le nb de fois que `value` est présent dans `list`.
            Fonctionne aussi avec:

                    • un dico    ; dans ce cas ce sont les valeurs et non les clés qui sont inspectées
                    • une chaîne ; dans ce cas ce sont les caractères de cette dernière qui sont inspectés

                                               NOTE:

            Utiliser `count()` à répétition peut être une source d'inefficacité.

            Pex, si on a une liste contenant un ensemble de mots, et qu'on souhaite construire un dico
            de fréquences:

                    {mot1: freq1, mot2: freq2, ...}

            ... il est très INefficace d'utiliser `count()`.

            En effet, pour ce faire, il faudrait appeler `count()` pour chaque mot présent dans la liste.
            Chaque `count()` testerait tous les mots de la liste pour vérifier s'il matche le mot dont
            on souhaite la fréquence.
            Avec une liste de 100 mots, dont 10 uniques, il faudrait appeler `count()` 10 fois, et
            chaque appel testerait 100 mots, soit 1000 tests en tout.

            Il est bcp plus efficace de tester chaque mot dans la liste une seule fois
            (100 opérations au lieu de 1000):

                    let freq = {}
                    for word in list
                        let freq[word] = get(freq, word, 0) + 1
                    endfor

            `word` est un nom de variable, on ne peut donc pas utiliser la syntaxe `freq.word`
            En effet, Vim chercherait la valeur associée à la clé dont le nom est 'word'.
            Il n'évaluerait pas la variable `word`.
            Il faut donc utiliser l'autre syntaxe:

                    freq[word]

            On n'a pas besoin d'initialiser le dictionnaire avec les mots uniques présents dans `list`.
            Ils seront progressivement ajoutés au sein de la boucle.
            En effet, qd on affecte une valeur à une clé inexistante, Vim l'ajoute automatiquement au dico.

            En revanche, on ne peut pas simplement écrire:

                    let freq[word] = freq[word] + 1

            En effet, qd la boucle rencontrera un mot pour la 1e fois, la valeur `freq[word]`
            n'existera pas encore.
            Ceci posera un pb pour la partie droite de l'affectation.
            La solution consiste à utiliser `get()` pour donner la valeur par défaut 0 lorsque ce
            cas se produit:

                    let freq[word] = get(freq, word, 0) + 1


    if index([val1, val2, val3], var) >= 0
    if var == val1 || var == val2 || var == val3 ...

            Test si la valeur de `var` est présente dans une liste de valeur.


    echo [4] == ["4"]

            retourne 0, la comparaison de listes est plus stricte que la comparaison de chaînes
            Vim ne fait pas de coercition pour les listes


    insert(list, 'a')

            ajoute l'item 'a' au début de `list` (index 0)


    insert(list, item, idx)

            ajoute `item` à `list` en index:

                    • `idx`        s'il est positif ou nul
                    • `idx` - 1    s'il est négatif

            L'index peut aller jusqu'à `len(list)`, mais pas au-delà.
            Pex, si la longueur de `list` est 4, on peut écrire:

                    let list = [1, 2, 3, 4]
                    echo insert(list, 5, 4)
                    [1, 2, 3, 4, 5]    ✔~

            ... mais pas:

                    echo insert(list, 5, 5)    ✘

    let list2 = copy(list1)

            affecte à list2 une copie superficielle (shallow) de list1

            Utile pour pouvoir manipuler une copie d'une liste sans modifier l'originale.
            Ex ici: http://vi.stackexchange.com/a/7428/6960
            En effet, taper: let list2 = list1 ne duplique pas la donnée contenue dans list1 ;
            list2 et list1 partagent une même référence.
            Ceci implique que si on modifie plus tard list2, list1 est elle-aussi modifiée.

            Si un des items de list1 est lui-même une liste, appelons-la sublist et donnons-lui l'index 0,
            son contenu n'est pas dupliqué dans list2, malgré l'utilisation de copy().
            Ce qui est dupliqué dans list2, c'est la référence vers sublist.

            Ceci implique que si on modifie un item de sublist à l'intérieur de list2, pex comme ceci:
                let list2[0][0] = new_value
            ... on modifie par la même occasion list1, car list1[0] et list2[0] partagent une même référence.

    let list2 = deepcopy(list1)

            affecte à list2 une copie profonde (deep) de list1

            Contrairement à la fonction copy(), si un des items de list1 est une liste (appelons-la sublist),
            deepcopy() ne duplique pas la référence vers sublist mais bien la donnée sublist elle-même.

    extend(alist, blist, idx)

            intègre blist dans alist, de telle façon que le 1er item de blist y a pour index idx


    get(list, 5, 'default')

            retourne la valeur de l'item d'index 5 dans list, et la chaîne 'default' s'il n'existe pas
            utile pour éviter des erreurs quand la liste est trop courte

    index(list, item)

            retourne l'index de item au sein de list (-1 s'il n'est pas dedans)

    len(list)

            retourne le nb d'items dans list (= index max + 1)


    range(4)

            retourne la liste [0, 1, 2, 3]

    range(2, 4)

            retourne [2, 3, 4]

    range(2, 9, 3)

            retourne [2, 5, 8]

            Cette commande illustre la syntaxe générale de range(): range(début, fin, pas)

    range(2, -2, -1)

            retourne [2, 1, 0, -1, -2]


    remove(list, 3)                     unlet list[3]
    remove(list, 3, -1)                 unlet list[3:]
    remove(list, index(list, 'foo'))

            supprime de list l'item:

                    • d'index 3
                    • d'index 3 jusqu'au dernier
                    • 'foo'

            remove() retourne l'item supprimé, ou une liste des items (s'ils sont plusieurs)


    repeat([0], 4)    map(range(4), 0)

            retourne [0, 0, 0, 0]
            repeat() permet de répéter des chaînes et des listes

    map(range(3), 'map(range(2), 0)')

            retourne    [[0, 0], [0, 0], [0, 0]]

            une imbrication de map() permet d'initialiser une liste de listes (matrice)

## Mappings

    if empty(maparg('-', 'n'))

            teste si la touche - est map à quelque chose en mode normal


    maparg('<C-L>', 'v')

            retourne le {rhs} du mapping v_ctrl-l

            Qd le 2e argument est une chaine vide, maparg() cherche un {rhs} pour le mode normal,
            visuel et operator-pending.
            S'il existe 2 mappings utilisant C-l comme {lhs}, un global et un buffer-local, c'est le {rhs}
            du buffer-local qui est retourné. Même chose qd on demande un dictionnaire (maparg(..., 0, 1)).


    maparg('<C-L>', 'v', 0, 1)

            retourne un dictionnaire contenant toutes les infos concernant le mapping v_ctrl-l
            Entre autres:

              est-il silencieux?
              est-il local au buffer?
              son lhs, son rhs
              le rhs est-il récursif?
              son rhs est-il le résultat d'une expression?
              attend-il avant d'exécuter le {rhs} si un autre mapping existe qui commence par le même {lhs}?
              son mode
              le sid du fichier dans lequel il a été défini (3 = vimrc)

              Qd le 3e argument de maparg() est non nul, le 1er argument n'est plus interprété comme le
              {lhs} d'un mapping mais le {lhs} d'une abréviation.


    exe 'nnoremap <Tab> ==' . maparg('<Tab>', 'n')

            préfixe '==' au {rhs} de <Tab> en mode normal

            Pex, si <Tab> en mode normal était associé à 'gm', après la commande précédente,
            il est associé à '==gm'


    mapcheck('abc', 'n')

            Retourne le rhs d'un mapping en mode normal si:

                    'abc' est le début de son lhs (lhs =~ ^abc)
                    ou inversement si le lhs d'un mapping est le début de 'abc' (abc =~ ^lhs)

            Si 'abc'  est le  début du  lhs d'un mapping  (ex: 'abcd'),  alors définir  un nouveau
            mapping dont le lhs  est 'abc' posera pb car lorsqu'on appuiera  sur 'abc', Vim attendra
            3s (&timeoutlen) avant d'exécuter le rhs.

            Réciproquement, si le lhs d'un mapping débute de la même façon que 'abc' (ex: 'ab'),
            alors  définir un  nouveau mapping  dont le  lhs est  'abc' posera  là encore  pb, car
            lorsqu'on appuiera sur 'ab', Vim attendra 3s avant d'exécuter son rhs.

            En testant  que la sortie de  mapcheck('abc') est bien  vide, on peut s'assurer  dans un
            script qu'on peut définir un nouveau mapping dont le {lhs} est 'abc' sans qu'il n'y ait
            jamais d'ambiguïté (pour 'abc' ou pour un autre qui commence pareil: 'a', 'ab').


    hasmapto('abc', 'n')

            Retourne 1 s'il existe un mapping en mode normal, dont le rhs contient `abc`.
            0 autrement.

            Utile dans un plugin pour vérifier si l'utilisateur a déjà associé une séquence de touches
            à un `<plug>` mapping.

## printf()

printf() est une fonction utile pour manipuler une chaîne au sein de laquelle on veut:

    • tronquer une sous-chaîne ou un flottant
    • ajouter un padding d'espaces ou de zéros
    • convertir un nb décimal en hexa ou en base 8
    • convertir un code ascii décimal en le caractère lui correspondant


    printf({fmt}, {expr1} ...)

            {fmt} est une chaîne pouvant contenir des items '%'.
            Pour chaque item utilisé (sauf '%%'), il faut fournir à printf() une expression correspondante.

            `printf()` retourne la chaîne {fmt} où les items sont remplacés par les expressions.
            Les items servent à formater les expressions: on parle d'interpolation.
            On ne peut pas utiliser plus de 18 expressions.

            Le formatage est décrit par une spécification de conversion qui suit le caractère '%'.
            Il attend 1 argument obligatoire (spécificateur de conversion aka type) et accepte
            jusqu'à 3 arguments optionnels (flags, field-width, precision) dans l'ordre suivant:

                %  [flags]  [field-width]  [.precision]  type


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


                                     flags

            Une suite d'un ou plusieurs caractères.

            #     N'a d'effet qu'avec les types o, x et X.

                  A pour effet d'ajouter en préfixe `0`, `0x` ou `0X`:

                        • printf('%#o', 123)
                          0173~
                        • printf('%#x', 123)
                          0x7b~
                        • printf('%#X', 123)
                          0X7B~

                  Permet d'exprimer explicitement la base dans laquelle est écrite le nb.

            0     Padding de zéros au lieu d'espaces.
                  Ne fonctionne que lorsque le padding est à gauche.
                  Un padding à droite ne peut être constitué que d'espaces.

            -     Alignement à gauche et non à droite.

            +     préfixe un '+' devant un nb positif:

                        printf('%+d', 123)
                        +123~
                        printf('%+.2f', 12.34)
                        +12.34~

            ' '   préfixe un espace devant un nb positif

                        printf('% d', 123)
                        ' 123'~
                        printf('%+ .2f', 12.34)
                        '+12.34'~
                        + a la priorité sur espace


                                  field-width

            `field-width` est un entier positif spécifiant le poids en octets de la valeur convertie.
            Sauf pour l'item %S où il correspond à une largeur en nb de cellules.

            Si `field-width` > poids en octets de la valeur convertie (ou nb de cellules),
            un padding d'espaces est ajouté à gauche.
            Si `field-width` < ..., la valeur n'est PAS tronquée pour autant.

            À la place d'un nb, on peut donner à `field-width` une valeur spéciale '*'.
            Dans ce cas, il faudra passer à printf() 2 arguments au lieu d'un.
            Le 1er correspondant au poids/largeur du champ, le 2e à l'expression à formater.
            Ex:

                    printf('%d: %*s', nr, width, line)

            On a bien 2 items (%d et %s), mais 3 arguments en plus de la chaîne:

                • `nr`     est l'expression formatée selon %d
                • `width`  est le poids du champ dans lequel doit s'afficher `line`
                • `line`   est l'expression formatée selon %*s

            '*' est utile lorsqu'on a besoin d'une largeur de champ dynamique, et est plus lisible qu'une
            concaténation de chaînes:

                    let prec = 9

                    printf('%'.prec.'f', 1/3.0)    ✔
                    printf('%*f', prec, 1/3.0)     ✔✔


                                   .precision

            `precision` est un nb interprété de façon différente selon le type qu'il affecte:

                • d, o, x et X     minimum de chiffres à afficher      avec padding (0/espace) si besoin
                • s                maximum d'octets à afficher         troncation si besoin
                • S                maximum de caractères à afficher    "
                • f, e, E, g, G    nb de chiffres après la virgule     "

            Les différences d'interprétation sont logiques:
            on souhaite souvent tronquer un flottant, mais pas un entier.

            Ceci étant, pour obtenir un padding de 0 avec un entier, il paraît plus logique d'utiliser
            un `field-width` et le flag 0:

                    printf('%06d', 123)

            plutôt que

                    printf('%.6d', 123)

            Ainsi, on peut considérer que field-width et .precision ont des usages bien distincts:

                    field-width = padding
                    .precision  = troncation

            Si on utilise le flag `.precision` mais sans lui donner de valeur (ex: '%.s'),
            il est considéré comme valant 0 (=troncation max).

            Si on n'utilise pas du tout le flag `.precision` (ex: '%f'), il est malgré tout considéré
            comme valant 6 pour un flottant de type f ou e/E, et 1 pour un flottant de type g/G.

            Tout comme pour `field-width`, on peut donner à `precision` la valeur '*' au lieu d'un nb.
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

            printf() peut, lorsque c'est nécessaire, convertir un argument d'un type donné en un autre.
            Les seules types de conversions automatiques possibles sont:

                    • nb    ↔    chaîne
                    • nb    →    flottant


    printf('this char is %c', 97)
        → 'this char is a'

            `%c` permet d'insérer au sein d'une chaîne un caractère à partir de son code ascii.


    printf('%f', 123.456)
    123.456000~

            En l'absence de précision explicite, printf() considère qu'elle vaut 6, d'où les 6 chiffres
            après la virgule ici.


    printf('%.f', 123.456)
    123~

            Qd la précision vaut 0 (`.` = `.0`), la partie décimale d'un flottant est omise:

                    %.f    ⇔    %.0f


    printf('%6d', 123)
    '   123'~
    printf('%06d', 123)
    '000123'~

    printf('%.s', 'foobar')

            Retourne ''.

            En l'absence de précision, elle est considérée comme nulle, et précision nulle = troncation max:

                    %.s    ⇔    %.0s

## Recherche / curseur

    cursor(5,10)

            positionne le curseur sur la 10e colonne de la 5e ligne du buffer
            retourne 0 si le curseur a pu être positionné, -1 autrement

            si le n° de ligne est nul le curseur ne change pas de ligne (idem pour la colonne)
            si le n° de ligne est supérieur au nb de lignes du buffer, le curseur se déplace sur la dernière (idem pour la colonne)

            Utile pour positionner le curseur avant de débuter une recherche avec search().

    getcurpos()

            Retourne une liste de 5 nb correspondant aux coordonnées du curseur.

            Le retour est généralement sauvegardé  dans un variable pour pouvoir
            restaurer la position du curseur plus tard.  Ex:

                    let save_cursor = getcurpos()


                                     NOTE:

            Ne  jamais utiliser  `getpos()` pour  sauvegarder puis  restaurer la
            position du curseur. `getpos()` ne sauvegarde pas l'attribut 'curswant'.

            https://vi.stackexchange.com/a/15566/16670


    search(pattern, [flags, stopline])

            Cherche pattern à partir du curseur.
            Retourne le n° de ligne du match s'il y en a un, 0 autrement.

            Le curseur se déplace jusqu'au match.
            stopline est un n° de ligne au-delà duquel la recherche doit s'arrêter.
            On peut passer des flags modifiant le comportement de search(), entre autres:

            ┌─────┬─────────────────────────────────────────────────────────────────────────────┐
            │ 'b' │ recherche vers l'arrière                                                    │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'c' │ accepte un match à l'endroit où se trouve le curseur                        │
            │     │ le curseur ne se déplace pas                                                │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'e' │ déplace le curseur à la fin du match (au lieu du début)                     │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'n' │ ne déplace pas le curseur                                                   │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 's' │ pose la marque ' à l'endroit où se trouve le curseur avant la recherche     │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'w' │ wrap / boucle à la fin du fichier                                           │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'W' │ ne wrap pas à la fin du fichier                                             │
            ├─────┼─────────────────────────────────────────────────────────────────────────────┤
            │ 'z' │ cherche à partir du curseur et non de la colonne 0                          │
            │     │ Même si on omet 'z', et que la recherche commence à partir de la colonne 0, │
            │     │ search() skip les matchs précédant le curseur.                              │
            └─────┴─────────────────────────────────────────────────────────────────────────────┘

                                               FIXME:

            Du coup à quoi sert 'z' ?
            Update:

>                   When the 'z' flag is not given, searching always starts in
>                   column zero **and then matches before the cursor are skipped**.

            If the before the cursor are skipped, then why bother searching from
            column zero.


                                               NOTE:

            Une commande Ex exécutée depuis le mode visuel nous fait toujours quitter ce dernier.
            On ne peut donc pas directement invoquer `search()` pour étendre la sélection jusqu'à
            la prochaine occurrence d'un pattern arbitraire:

                call search('pat')                     ✘ cherche `pat` depuis le mode normal

                                                         Pk le mode normal?
                                                         Car après après avoir appuyé sur Enter pour
                                                         exécuter une commande Ex, on est immédiatement
                                                         en mode normal.

                call search('pat') | norm! gv          ✘ cherche `pat` depuis le mode normal
                                                         et restaure la dernière sélection visuelle

                call search('pat') | norm! m'gv``      ✔

                exe 'norm! gv' | call search('pat')    ✔ cherche `pat` depuis le mode visuel (*)
                                                         et ce faisant met à jour la sélection

            (*) Cette fois, 'norm! gv' restaure la sélection visuelle avant d'invoquer `search()`.


    getline(search('foo', 'bcnW'))

            retourne le contenu de la précédente ligne où se trouve le pattern 'foo' sans faire
            bouger le curseur

    search('(', 'b', line("w0"))

            cherche vers l'arrière le caractère '(' en s'arrêtant à la 1e ligne de la fenêtre
            retourne le n° de ligne du match

    search('END', '', line("w$"))

            cherche la chaîne 'END' en s'arrêtant à la dernière ligne actuellement visible dans la fenêtre
            retourne le n° de ligne du match

    search('\v<' . nr2char(getchar()), 'W', line('.'))

            demande une frappe au clavier, et déplace le curseur sur le prochain mot commençant
            par la lettre tapée

            line('.') indique à Vim d'arrêter sa recherche au-delà de la ligne courante (stopline)

                                               NOTE:

            search() retourne le n° de ligne d'un match, mais il déplace aussi le curseur.
            Ici, c'est le déplacement qui nous intéresse (pas le code de retour).

    searchpos()

            similaire à search() à ceci près qu'elle retourne une liste [lnum, cnum]

    setpos('.', save_cursor)

            restaure la position du curseur sauvegardée dans la variable save_cursor via la fonction getcurpos()

            le 1er argument de setpos() détermine de quel objet la fonction va définir la position:
            le curseur = . ou une marque = 'x

## Registres

    getreg('a')

            retourne le contenu du registre @a sous la forme d'une chaîne

    getreg('a', 1, 1)

            retourne le contenu du registre @a sous la forme d'une liste, dont chaque item correspond
            à une ligne du registre; \n sert de séparateur

            Le 2e argument est facultatif et ignoré sauf pour le registre expression ('=').

            Le 3e argument est facultatif et détermine si le retour sera une chaîne ou une liste.

    getreg('=', 1)

            retourne la dernière expression passée au registre @= avant son évaluation
            si on veut l'évaluation, il faut remplacer le 2e argument par 0

    getregtype('a')

            retourne le type du registre a:

                'v'    ou 'c'         characterwise
                'V'    ou 'l'         linewise
                '10' ou 'b10'       blockwise (10 étant la largeur du bloc)

            Le type d'un registre détermine de quelle façon il sera collé dans un buffer.

            On peut appeler getregtype() sans lui passer d'argument,
            dans ce cas elle retourne le type du registre en cours d'utilisation par un opérateur (v:register).

    setreg('a', string)

            écrit la chaîne string dans le registre @a

    setreg(v:register, @*)

            écrit le contenu du registre sélection dans le registre en cours d'utilisation par un opérateur
            la fonction setreg() retourne 0 en cas de succès, un autre nb autrement

    setreg('*', @%, 'av')

            ajoute (flag 'a' dans le 3e argument) le nom du buffer courant au contenu du registre sélection
            et attribue le type characterwise à ce dernier (flag 'v' dans le 3e argument)

    setreg('a', "1\n2\n3", 'b5')

            stocke la chaîne "1\n2\n3" dans le registre @a et lui attribue le type par bloc avec une largeur 5
            si on ne précise pas la largeur du bloc, elle est égale automatiquement au nb de caractères
            sur la plus longue des lignes

    setreg('a', ['foo', 'bar', 'baz'])

            stocke dans le registre 'a' les chaînes 'foo', 'bar' et 'baz' sur 3 lignes différentes
            le type du registre 'a' est automatiquement 'V'

    setreg('+', '', 'aV')

            fait passer le type du registre @+ à linewise

            Le flag 'a' indique qu'il faut ajouter la valeur à l'ancien contenu du registre @+
            (au lieu de l'écraser), et comme la valeur est '' le contenu de @+ n'est pas modifié
            (mais son type oui).

            Ceci est une astuce illustrant comment changer le type d'un registre, car il n'existe
            pas de fonction setregtype().

## Temps

    localtime()

            retourne l'heure locale en nb de secondes depuis l'epoch (date: 0h UTC 01/01/1970)


    getftime('file')

            retourne la date de la dernière modification de file en nb de secondes depuis l'epoch
            si file ne peut pas être trouvé, -1 est retourné


    reltime()

            retourne l'heure courante sous la forme d'une liste de 2 items
            1er = nb de secondes depuis l'epoch; 2e nb = partie décimale en millionièmes de secondes

    reltime([10, 100000], [15, 300000])

            retourne [5, 200000]    15.3 - 10.1 = 5.2

            reltime() permet de calculer le temps qui s'est écoulé entre 2 dates enregistrées à des moments
            différents (dans des variables) via reltime()

    reltimestr(reltime([10, 100000], [15, 300000]))

            retourne la chaîne '5.200000'

            reltimestr() permet de convertir la sortie de reltime() en une chaîne


    strftime('%F')
    strftime('%c')    strftime('%d %b %Y')

    strftime('%X')
    strftime('%H:%M')
    strftime('%T')

            retourne:

                    • la date du jour    sans l'heure       équivaut à `%Y-%m-%d`
                    • la date du jour    avec l'heure,      système horaire sur 12 heures

                    • l'heure            avec les secondes, système 12 heures
                    • "                  sans les secondes, système 24 heures
                    • "                  avec les secondes, système 24 heures

            En l'absence de 2e argument, strftime() utilise l'heure/date du moment.

            Pour la liste complète des formats supportés par `strftime()`, lire `$ man strftime`.


    strftime('%c', getftime('file'))

            retourne la date de dernière modification de file (format lisible par un humain)

##
# Reference

[1]: https://fr.wikipedia.org/wiki/Notation_caret
