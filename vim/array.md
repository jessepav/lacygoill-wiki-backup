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
## How to get the number of occurrences of a value in a list?

Use `count()`:

    let list = split('hello', '\zs')
    echo count(list, 'l')
    2~

The `l` character is present twice in `['h', 'e', 'l', 'l', 'o']`.

##
## What's the output of `echo [4] == ['4']`?

`0`

Vim does no coercition when comparing lists.

##
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
## How to add an item in front of a list?

Use `insert()`:

    let list = [1, 2]
    echo insert(list, 'a')
    ['a', 1, 2]~

## How to add an item at the end of a list?

Use `add()`:

    let list = [1, 2]
    call add(list, 3)
    echo list
    [1, 2, 3]~

Note that `add()` operates in-place.

### Can this be used to concatenate lists?

No.

    let list = [1, 2]
    call add(list, [3, 4])
    echo list
    [1, 2, [3, 4]]~

##
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
## How to rotate the items of a list to the left?

Use a combination of  `add()` and `remove()`, to move the first  item to the end
of the list.

    let a = range(1, 4)

    call add(a, remove(a, 0))
    echo a

### to the right?

Use a  combination of `insert()`  and `remove()`, to move  the last item  to the
beginning of the list.

    call insert(a, remove(a, -1), 0)
    echo a

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

Note that the list name changed inside the function (`counts` → `list`).
But it doesn't matter: `counts` has still mutated.
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
## Which list is unable to mutate?

`a:000` can't mutate:

    fu! Func(...) abort
        return map(a:000, 'v:val+1')
    endfu
    echo Func(1, 2, 3)
    E742: Cannot change value of map() argument~

##
# ?

    echo insert(list, item, idx)

Ajoute `item` à `list` en index:

   • `idx`        s'il est positif ou nul
   • `idx` - 1    s'il est négatif

L'index peut aller jusqu'à `len(list)`, mais pas au-delà.
Pex, si la longueur de `list` est 4, on peut écrire:

        let list = [1, 2, 3, 4]
        echo insert(list, 5, 4)
        [1, 2, 3, 4, 5]    ✔~

... mais pas:

        echo insert(list, 5, 5)    ✘

# ?

    let list2 = copy(list1)

Affecte à `list2` une copie superficielle (shallow) de `list1`.

Utile pour pouvoir manipuler une copie d'une liste sans modifier l'originale.
Ex ici:

<http://vi.stackexchange.com/a/7428/6960>

En effet:

    let list2 = list1

ne duplique  pas la donnée contenue  dans `list1`; `list2` et  `list1` partagent
une même référence.
Ceci  implique que  si  on modifie  plus tard  `list2`,  `list1` est  elle-aussi
modifiée.

Si  un des  items de  `list1`  est lui-même  une liste,  appelons-la sublist  et
donnons-lui l'index  `0`, son  contenu n'est pas  dupliqué dans  `list2`, malgré
l'utilisation de `copy()`.
Ce qui est dupliqué dans `list2`, c'est la référence vers sublist.

Ceci implique que si on modifie un item de sublist à l'intérieur de `list2`, pex
comme ceci:

    let list2[0][0] = new_value

...  on modifie  par  la même  occasion `list1`,  car  `list1[0]` et  `list2[0]`
partagent une même référence.

# ?

    let list2 = deepcopy(list1)

Affecte à `list2` une copie profonde (deep) de `list1`.

Contrairement à la fonction  `copy()`, si un des items de  `list1` est une liste
(appelons-la sublist),  `deepcopy()` ne duplique  pas la référence  vers sublist
mais bien la donnée sublist elle-même.

# ?

    echo extend(alist, blist, idx)

Intègre blist dans `alist`,  de telle façon que le 1er item de  `blist` y a pour
index `idx`.

# ?

    echo index(list, item)

Retourne l'index de item au sein de `list` (`-1` s'il n'est pas dedans).

# ?

               ┌ start
               │  ┌ end
               │  │  ┌ step
               │  │  │
    echo range(2, 9, 3)
    [2, 5, 8]~

# ?

    echo range(2, -2, -1)
    [2, 1, 0, -1, -2]~

# ?

Remove the item whose index is `3`:

    unlet list[3]
    echo list

    call remove(list, 3)
    echo list

Remove the items whose indexes are greater than `3`:

    unlet list[3:]
    echo list

    call remove(list, 3, -1)
    echo list

Remove the items `foo`:

    call remove(list, index(list, 'foo'))
    echo list

`remove()` returns whatever was removed.

# ?

    echo repeat([0], 4)
    echo map(range(4), 0)
    [0, 0, 0, 0]~

`repeat()` permet de répéter des chaînes et des listes.

# ?

    echo map(range(3), 'map(range(2), 0)')
    [[0, 0], [0, 0], [0, 0]]~

Une imbrication de `map()` permet d'initialiser une liste de listes (matrice).

##
##
##
# Dictionaries
## How to get the number of occurrences of a value in a dictionary?

    let dict = {'a': 1, 'b': 2, 'c': 3}
    echo count(dict, 3)
    1~

The value `3` is present once in the the dictionary.

##
## I have a list of words.  What's the most efficient way to build a dictionary of words frequencies?

Iterate over the words of the list, to build the dictionary.

        let list = ['one', 'two', 'two', 'three', 'three', 'three']
        let freq = {}
        for word in list
            let freq[word] = get(freq, word, 0) + 1
        endfor
        echo freq
        {'one': 1, 'two': 2, 'three': 3}~

Note that you can't write:

        let freq[word] = freq[word] + 1

Because when  the loop will  encounter `word` for  the first time,  `freq` won't
have any key yet  for it; so `freq[word]` won't exist which  will raise an error
in the rhs of the assignment.

---

Don't use `count()`; it would be less effecient:

        fu! Func()
            let words = []
            %s/\<\k\+\>/\=add(words, submatch(0))/gn
            let freq = {}
            for word in uniq(sort(copy(words)))
                let freq[word] = count(words, word)
            endfor
            echo freq
        endfu
        10Time sil call Func()

        fu! Func()
            let words = []
            %s/\<\k\+\>/\=add(words, submatch(0))/gn
            let freq = {}
            for word in words
                let freq[word] = get(freq, word, 0) + 1
            endfor
            echo freq
        endfu
        10Time sil call Func()

Indeed, assuming your list contains 10  unique words, you would invoke `count()`
10 times.
And  assuming  you have  100  words  in total,  each  time,  it would  make  100
comparisons  to  get  the  number  of  occurrences  of  the  word:  that's  1000
comparisons in total.

##
##
##
# ?

    echo extend(adict, bdict, 'keep')

Ajoute toutes les entrées de `bdict` à `adict`.

Le 3e  argument optionnel indique  à `extend()`  ce qu'il faut  faire lorsqu'une
entrée de `bdict` contient une clé déjà présente dans `adict`:

    ┌─────────┬──────────────────────────────────────────────────────────────────────────────────┐
    │ 'keep'  │ conserver l'entrée de `adict`                                                    │
    ├─────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ 'force' │ la remplacer par celle de `bdict` (valeur par défaut si le 3e argument est omis) │
    ├─────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ 'error' │ produire un message d'erreur                                                     │
    └─────────┴──────────────────────────────────────────────────────────────────────────────────┘

`extend()` n'est nécessaire que pour fusionner 2 dicos.
Pour ajouter une nouvelle entrée, un `let dict.key = 'value'` suffit.

# ?

    let dict = {'ab': 1, 'cd': 2, 'abcd': 3}
    echo filter(dict, {k,v -> k =~# '^a'})
    {'abcd': 3, 'ab': 1}~

Retourne le dictionnaire après lui avoir supprimé  tous les items dont la clé ne
commence pas par `a`.

# ?

    echo get(dict, 'key', -1)

Retourne la  valeur de l'item dont  la clé est  `key` dans `dict`, et  `-1` s'il
n'existe pas.

# ?

    echo has_key(dict, 'foo')

Retourne `1` si la clé `foo` est présente dans dict, `0` autrement.

# ?

    let uk2fr = {'one': 'un', 'two': 'deux', 'three': 'trois',}

Exemple de définition d'un dictionnaire.
La forme générique étant:

    {<key> : <value>, ...}

# ?

    let dict['key'] = 'value'
    let dict.key = 'value'

Assigne à la clé `key` de dict la valeur `value`.
Si aucune entrée n'utilise la clé `key`, elle est créée.

# ?

    dict['foo']
    dict.foo

Retourne la valeur associée à la clé `foo` du dictionnaire `dict`.

La 1e syntaxe autorise l'utilisation d'une plus grande variété de caractères (en
plus de ascii, chiffres et `_`).
De plus, elle permet l'évaluation automatique d'une variable stockant une clé:

    dict[myvar] ✔
    dict.myvar ✘

# ?

    unlet dict.key
    echo remove(dict, key)

Supprime l'entrée de `dict` contenant la clé `key`.

`remove()` retourne l'entrée supprimée qu'on peut ainsi capturer dans une variable:

    let myvar = remove(dict, key)

