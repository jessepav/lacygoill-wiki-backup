# What's an array?

A non-scalar data: a list or a dictionary.

##
# Lists
## How is a negative index argument interpreted by a function handling a list?

The argument is used to retrieve an item from the end of the list.

`-1` = last item
`-2` = second item from the end
`-3` = third item from the end
...

###
## How to get the first item in `list` which matches `pat`?

    echo matchstr(list, pat)

Example:

    echo matchstr(['foo', 'bar', 'baz'], '^b')
    bar~

## How to get the index of the first item in `list` which matches `pat`?

    echo match(list, pat)

Example:

    echo match(['foo', 'bar', 'baz'], '^b')
    1~

###
## What is slicing?

The process of getting a sublist by appending a list with a range of indexes:

    echo range(1,5)[1:-2]
    [2, 3, 4]~

## On which condition does slicing work as expected?  (2)

The indexes in the range describe two items.
The first item must come *before* the second one.

    echo range(1,5)[-1:0]
    []~

In this example, the output is `[]`, instead of `[1, 2, 3]`, because the item of
index `-1` comes *after* the item of index `0`.

OTOH, in this example, the slicing works:

    echo ['a', 'b', 'c'][-2:2]
    ['b', 'c']~

because the item of index `-2` (`b`) comes before the item of index `2` (`c`).

---

If the  first index is a  variable, you may need  to separate it from  the colon
with a space; otherwise, Vim may wrongly interpret it as a scope.

    echo range(1,3)[s:e]
    E121: Undefined variable: s:e~

    let [s, e] = [0, 2]
    echo range(1,3)[s: e]
    E731: using Dictionary as a String~

    let [s, e] = [0, 2]
    echo range(1,3)[s :e]
    [1, 2, 3]~
    echo range(1,3)[s : e]
    [1, 2, 3]~

## How to change the value of a range of consecutive items in a list in a single statement?

Use an assignment: in the lhs, use slicing; in the rhs use, a list of values.

    let list = range(1,4)
    let list[1:2] = ['a', 'b']
    echo list
    [1, 'a', 'b', 4]~

###
## How to concatenate lists?  (2)

    let list = [1, 2, 3]
    echo list + [4, 5]
    [1, 2, 3, 4, 5]~

    let list = [1, 2, 3]
    echo extend(list, [4, 5])
    [1, 2, 3, 4, 5]~

### What's the difference between the 2 methods?

The `+` operator doesn't alter any existing list:

    let list = [1, 2, 3]
    echo list + [4, 5]
    echo list
    [1, 2, 3]~

While `extend()`  operates in-place, and  alters the  first list it  receives as
argument:

    let list = [1, 2, 3]
    echo extend(list, [4, 5])
    echo list
    [1, 2, 3, 4, 5]~

But not the second one:

    let alist = [1, 2]
    let blist = [3, 4]
    echo extend(alist, blist)
    echo blist
    [3, 4]~

###
## Without altering the rest of a list, how to
### increase a number item?

Use an assignment: in the lhs, use the index of the item you want to change; and
use the `+=` operator.

    let list = [1, 2, 3]
    let list[2] += 99
    echo list
    [1, 2, 102]~

This works because a list is a mutable object.

### concatenate a string to a string item?

Use an assignment: in the lhs, use the index of the item you want to change; and
use the `.=` operator.

    let list = ['a', 'b', 'c']
    let list[1] .= '_x'
    echo list
    ['a', 'b_x', 'c']~

##
## What's the output of the last command in these snippets?
### 1:

    fu! Increment(list, i)
        let a:list[a:i] += 1
    endfu
    let list = [0, 0, 0]
    call Increment(list, 2)
    echo list

↣ [0, 0, 1] ↢

### 2:

    fu! Increment(list, i)
        let a:list[a:i] += 1
    endfu
    let counts = [0, 0, 0]
    let patterns = ['a_word', 'b_word', 'c_word']
    for i in range(3)
        exe '%s/'.patterns[i].'/\=Increment(counts,'.i.')/gn'
    endfor
    echo counts

↣
    [1, 1, 1]~

Note

↢

### 3:

    fu! Func()
        let list = [1, 2, 3]
        let n = 42
        call FuncA(n)
        echo n
    endfu
    fu! FuncA(n)
        let l:n = a:n
        let l:n += 1
    endfu
    call Func()

↣ 42 ↢

###
### How do you explain these results?

The lists have mutated because Vim passes arrays by reference, not by value.
`Increment()`  received a  reference  of `list`  in the  first  snippet, and  of
`counts` in the second one.

The number has not been altered because Vim passes scalars by value.

It  seems  that  Vim behaves  like  awk:  scalars  are  passed by  value,  while
non-scalar values are passed by reference.

### What are the two properties of arrays, without which these results would not be possible?

   1. an array is mutable
   2. an array is passed by reference

##
##
##
# ?

À l'intérieur de la fonction, le nom donné à la liste n'a pas d'importance.
Pex,  ici,  on  l'appelle  `list`  dans la  fonction  `Increment()`  alors  qu'à
l'extérieur de cette dernière, elle s'appelle `counts`.
IOW, la mutation n'est pas affectée  par la différence de noms entre l'intérieur
et l'extérieur de la fonction.

---

On peut faire  muter une liste passée directement en  argument, mais pas `a:000`
qui est une liste construite par Vim:

        fu! Func(...) abort
            " ✘
            call map(a:000, 'v:val+1')
            echo a:000
        endfu
        call Func(1, 2, 3)
        E742: Cannot change value of map() argument~

# ?

Pour vimscript, les listes sont des objets mutables.
On peut modifier un item d'une liste sans devoir remplacer toute la liste.


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


    index(list, item)

            retourne l'index de item au sein de list (-1 s'il n'est pas dedans)

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

    echo map(range(3), 'map(range(2), 0)')

            retourne    [[0, 0], [0, 0], [0, 0]]

            une imbrication de map() permet d'initialiser une liste de listes (matrice)

# ?

Dictionaries

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

