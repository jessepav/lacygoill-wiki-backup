# Which condition must a variable name satisfy to store a funcref?

It must begin with an uppercase character.

    let g:width = function(exists('*strchars') ? 'strchars' : 'strlen')
    echo g:width('hello')
    E704: Funcref variable name must start with a capital: width~

    let g:Width = function(exists('*strchars') ? 'strchars' : 'strlen')
    echo g:Width('hello')
    5~

Unless it's local to something else than a function:

    let t:width = function(exists('*strchars') ? 'strchars' : 'strlen')
    echo t:width('hello')
    5~

    unlet! g:Width
    fu! Width(string) abort
        let l:width = function(exists('*strchars') ? 'strchars' : 'strlen')
        return l:width(a:string)
    endfu
    echo Width('hello')
    E704: Funcref variable name must start with a capital: l:width~

## Why?

To avoid a conflict with a builtin function.

##
# I save a funcref in a global variable, then define a function whose name (!= code) is identical to the variable:

    let g:Width = function('toupper')
    fu! Width(string) abort
        let l:width = function(exists('*strchars') ? 'strchars' : 'strlen')
        return l:width(a:string)
    endfu

## What will be the output of `Width('hello')`?

The first definition (funcref) seems to win:

    echo Width('hello')
    HELLO~

---

But the definition of the function is weird:

    fu Width
                vvvvvvvvvvvvvvv
       function toupper(string) abort~
    1          let l:width = function(exists('*strchars') ? 'strchars' : 'strlen')~
    2          return l:width(a:string)~
       endfunction~

## Could I have reversed the order of the saving and the definition?

No.

    fu! Width(string) abort
        let l:width = function(exists('*strchars') ? 'strchars' : 'strlen')
        return l:width(a:string)
    endfu
    let g:Width = function('toupper')
    E705: Variable name conflicts with existing function: g:Width~

It seems that `:let` is careful about avoiding conflicts, but not `:fu`.

##
# What's the signature of `function()`?

    function({name} [, {arglist}] [, {dict}])

---

Note that it's *not*:

    function({name} [, {arglist} [, {dict}]])

IOW, `function()` is an **overloaded** function which has a different semantics,
depending on the types of its arguments.

When the second argument is a list, the produced funcref is automatically passed
the latter as  arguments; but when it's  a dictionary, the function  is bound to
it.

So, if you need to bind a function to a dictionary, you don't need to do:

    let Fr = function('Func', [], dict)
                              ^^
You can simply do:

    let Fr = function('Func', dict)

---

`function()` is not the first example of overloaded function.
Any function which  accepts optional arguments is, by  definition, an overloaded
function;  so `mapcheck()`  which accepts  two optional  arguments is  *also* an
overloaded function.
However, so  far, we  only saw  functions whose  semantics changed  according to
their arity; `function()` is the first  one whose semantics changes according to
the type of its arguments.

> The functions must differ either by the arity or types of their parameters

Source: https://en.wikipedia.org/wiki/Function_overloading

# What's the limitation imposed to `funcref()`, but not `function()`?

`funcref()`  can  not  be  passed  the  name  of  a  builtin  function;  only  a
user-defined function:

    :echo funcref('strlen')
    E700: Unknown function: strlen~

##
# When calling a function F, can I replace its name with an expression whose value is a funcref of F?

Yes:

    fu! Func(i,j)
        return a:i + a:j
    endfu
    let list = [function('Func')]
    echo list[0](1, 2)
    3~

##
# What does it mean for a function to be bound to a dictionary?

When calling  the function, the dictionary  will be automatically passed  to the
function; the  latter will be  able to access  the dictionary through  the local
variable `self`.

## How to do it
### without modifying the dictionary?

Pass the dictionary as an argument to `function()`.
The resulting funcref binds the function to the dictionary.

    let adict = {'name': 'toto'}
    fu! Func() dict
        return 'my name is: '.self['name']
    endfu
    let Fr = function('Func', adict)
                              ^^^^^

    " the dictionary was not modified
    echo adict
    {'name': 'toto'}~

    " `Func()` is able to access the dictionary
    echo Fr()
    my name is: toto~

### modifying the dictionary, and giving a proper name to the function?

   1. define the function with the `dict` attribute

   2. store a funcref referring to the function inside the dictionary

Example:

    fu! s:size() dict
        return len(self.data)
    endfu
    let adict = {'data': [0, 1, 2], 'size': function('s:size')}
    echo adict.size()
    3~

---

There's nothing special in the syntax `adict.size()`.
`adict.size` is an expression whose value is a funcref.
So, it  can be used to  call the function referred  to by the funcref,  like any
other expression.

### modifying the dictionary, and without giving a proper name to the function?

Follow this scheme for the name of the function:

    dictionary.key

Example:

    let adict = {'data': [0, 1, 2]}
    fu! adict.size()
        return len(self.data)
    endfu
    echo adict.size()
    3~

This time, you didn't have to:

   • include a funcref in the dictionary

   • give a proper name to the function

   • give it the `dict` attribute

`dictionary.key()` is syntaxic sugar.

##
## What does the `dict` attribute allow a function to do?

If the function is bound to a dictionary, it can access the latter via the local
variable `self`; it couldn't without.

### What does it prevent to do?

You can't call a function defined with `dict` directly:

    fu! Func() dict
        return 1
    endfu
    echo Func()
    E725: Calling dict function without Dictionary: Func~

### Is it always necessary?

Only if the function has a proper name (!= number).

##
## What does Vim do automatically when you name a function `adict.size`?

It  adds the  key `size`  to `adict`,  and give  it a  funcref referring  to the
currently defined function, as a value.

    let adict = {'data': [0, 1, 2]}
    fu! adict.size()
        return len(self.data)
    endfu
    echo adict.size

     ┌ `adict.size` is a funcref~
     │        ┌ its name is `13`~
     │        │    ┌ it's bound to this dictionary~
     │        ├┐   ├─────────────────────────────────────────┐~
    function('13', {'data': [0, 1, 2], 'size': function('13')})~
                                       ├────────────────────┘~
                                       └ a funcref has been added to the dictionary~
                                         to implement the binding~

---

If `adict` already contains a `size` key, the definition of the function fails:

    let adict = {'data': [0, 1, 2], 'size': 0}
    fu! adict.size()
        return len(self.data)
    endfu
    E718: Funcref required~

### What kind of special function is it?

A numbered or anonymous function.

### Why is it called like that?

Because technically, Vim gives it a simple number as a name.

### What should I pass to `:function` to print its definition?

    :fu {123}
         │
         └ numbered name of the function

### Why should I avoid defining such a function?

Debugging it is hard.

If it raises an error, `:WTF` can't show you its location.

Besides, it's automatically  removed as soon as there's no  funcref which refers
to it anymore.
So, if  you think you can  infer where the location  of the function is  in your
codebase, by looking at its definition, you may not even be able to do that:

    let adict = {'data': [0, 1, 2]}
    fu! adict.size()
        return len(self.data)
    endfu
    echo adict.size
    function('13', {'data': [0, 1, 2], 'size': function('13')})~
              ^^

    fu {13}
       function 13() dict~
    1          return len(self.data)~
       endfunction~

    unlet adict
    fu {13}
    E123: Undefined function: 13~

For more info, see:

    https://github.com/LucHermitte/lh-vim-lib/blob/master/doc/OO.md

##
# ?

        fu! Func() dict
            return 'called from '.self['which dict am I']
        endfu
        let adict = {'which dict am I': 'adict'}


        let adict.myFunc = function('Func')
        echo adict.myFunc()

        let adict.myFunc = function('Func')
        let bdict = {'which dict am I': 'bdict'}
        let bdict.myFunc = adict.myFunc
        echo bdict.myFunc()

        let adict.myFunc = function(function('Func'), adict)
        let bdict = {'which dict am I': 'bdict'}
        let bdict.myFunc = adict.myFunc
        echo bdict.myFunc()

---

Note that binding a function to a Dictionary also happens when the function is a
member of the Dictionary:

        let myDict.myFunction = MyFunction
        call myDict.myFunction()

Here `MyFunction()` will get `myDict` passed as "self".
This happens when the "myFunction" member is accessed.
When assigning  "myFunction" to otherDict  and calling it,  it will be  bound to
otherDict:

        let otherDict.myFunction = myDict.myFunction
        call otherDict.myFunction()

Now "self" will be "otherDict".
But when the dictionary was bound explicitly:

        let myDict.myFunction = function(MyFunction, myDict)

it won't happen:

        let otherDict.myFunction = myDict.myFunction
        call otherDict.myFunction()

Here "self" will be "myDict", because it was bound explicitly.

# ?

    let adict = {'data': [0, 1, 2]}
    fu! adict.size()
        return len(self.data)
    endfu
    let bdict = {'data': [0, 1], 'size': function(adict.size)}
    echo bdict.size()
    2~

On  peut se  référer à  la fonction  `adict.size()` (qui  techniquement est  une
fonction numérotée) via une funcref, comme pour n'importe quelle fonction.
Elle n'a pas de statut à part.

Pk `2` et pas `3` comme tout à l'heure?

        echo bdict.size()
      ⇔ echo adict.size()
      ⇔ echo len(self.data)
                 │
                 └ sauf que cette fois `self` ne contient pas `adict` mais `bdict`
                                                               │            │
                                                               │            └ taille 2
                                                               └ taille 3

Ça peut  paraître étrange  puisque c'est  `adict`, et non  pas `bdict`,  qui est
associé à `adict.len()`.

Theory:

`bdict.size()` est une fonction dictionnaire, comme `adict.size()`.
`bdict` lui est donc associé; qd elle  est invoquée Vim lui passe via `bdict` la
variable `self`.

Le  code final  est celui  de `adict.size()`,  mais le  dictionnaire qui  lui est
associé est `bdict`; Vim ne le remplace pas plus tard par `adict`.

Remark:

Comme pour  toute fonction dictionnaire,  Vim ajoute  une funcref se  référant à
elle dans le dico:

    echo bdict
    {~
                                        ┌ fonction “7”~
                                        │~
      'data': [0, 1], 'size': function('7',~
      \                                {'data': [0, 1, 2], 'size': function('7')})~
                                        ├────────────────────────────────────────┘~
                                        └ associée à ce dictionnaire~
    }~

On remarque que `function()` accepte un dictionnaire comme argument optionnel.
Qd elle en reçoit un, elle l'associe à la fonction.

# ?

    fu! Hello()
        echo 'hello'
    endfu

    fu! World()
        echo 'world'
    endfu

    let FR = function('Hello')
    call FR()
    hello~

    let FR = function('World')
    call FR()
    world~

On peut  invoquer une  fonction en remplaçant  son nom par  une funcref,  ou une
expression dont l'évaluation est une funcref.
Ici,  on  remplace  le  nom  de  fonction  `Func`  par  la  variable  `FR`  dont
l'évaluation est une funcref:

    call Func()  →  call FR()

---

    fu! Func(i,j)
        return a:i + a:j
    endfu
    let FR = function('Func')
    let list = [3, 4]
    echo call(FR, list)
    7~

`call()` permet de passer une liste d'arguments à une funcref.
Équivaut à :

    echo FR(3, 4)

Toutefois, cette 2e  syntaxe n'est utilisable que si on  déballe les éléments de
la liste, pas si on les laisse dedans:

    echo call(FR, list)
    ✔
    echo FR(list)
    ✘ E119: Not enough arguments for function: Func~

---

On peut  aussi utiliser `call()`  pour passer une  liste d'arguments
directement à une fonction:

    fu! Func(...)
        let sum = 0
        for i in a:000
            let sum += i
        endfor
        return sum
    endfu

    echo call('Func', [1, 2])
    3~
    echo call('Func', [1, 2, 3])
    6~

Utile pour  passer à une fonction  un ensemble d'arguments dont  la taille n'est
pas connue à l'avance.

---

    fu! Func()                  ┊ "
        return 'foo'            ┊ "
    endfu                       ┊ "
                                ┊
    let FR = function('Func')   ┊   let FR = funcref('Func')
                                ┊
    fu! Func()                  ┊ "
        return 'bar'            ┊ "
    endfu                       ┊ "
                                ┊
    echo FR()                   ┊ "
                                ┊
    bar                         ┊ foo~


Si on crée une funcref, et qu'on  change la définition de la fonction à laquelle
elle se réfère, la funcref se réfère désormais:

   • à la nouvelle définition, si elle a été créée par `function()`

   • à la définition originelle, si elle a été créée par `funcref()`

IOW, la funcref produite par:

   • `function('Func')` cherche `Func` via son nom (la
     définition associée peut changer)

   • `funcref('Func')`  cherche `Func` via sa référence (i.e.
     adresse mémoire)

---

    :echo type(function('system')) == type('')
    0~

Confirme que  la sortie  de `function()`  qui s'affiche à  l'écran est  bien une
référence et non une chaîne.
Une funcref est un type de donnée à part entière.

Pour  obtenir le  nom  d'une funcref  sous  forme de  chaîne,  il faut  utiliser
`string()`:

    string(FR)

---

    fu! Func()
        return 42
    endfu
    let Func = function('Func')
    E705: Variable name conflicts with existing function: Func~

On  ne peut  pas ré-utiliser  le  nom d'une  fonction pour  nommer une  variable
contenant une funcref se référant à elle.

---

En revanche, on  peut ré-utiliser le nom  d'une fonction pour nommer  une clé de
dico dont la valeur est une funcref se référant à elle:

    fu! Func()
        return 42
    endfu
    let mydict = {'data': [0, 1], 'Func': function('Func')}
    echo mydict.Func()
    42~

# ?

    fu! Describe(i, j, object)
        echo (a:i + a:j).' '.a:object
    endfu
    let Description = function('Describe', [1, 2])
    call Description('piggies')
    3 piggies~

`function()` peut lier une liste d'arguments à une fonction.
On dit que le résultat est un “partiel“.

Sans partiel, les 2 dernières lignes du code se ré-écriraient comme ceci:

    let Description = function('Describe')
    call Describe(1, 2, 'piggies')

---

Un partiel est une funcref particulière:

    echo type(Description) == type(function('tr'))
    1~

---

Vim passe les arguments inclus dans  la définition d'un partiel avant ceux qu'on
peut passer au moment de l'invocation:

    1 et 2  avant  'piggies'

---

D'où vient le terme “partiel“ ?

En informatique, une  application de fonction partielle décrit  le processus qui
consiste à  fixer un sous-ensemble des  arguments d'une fonction en  les liant à
des valeurs prédéterminées, produisant une autre fonction, d'arité inférieure.

    https://en.wikipedia.org/wiki/Partial_application

Pour rappel, en mathématiques, l'arité  d'une fonction est le nombre d'arguments
qu'elle requiert.

Exemple:

    f:           x,y  →  x/y
    partial(f):    y  →  1/y

En fixant/liant le 1er argument de la fonction  `f` à la valeur 1, on obtient la
fonction inverse.

Il est possible que  le terme fut choisi car une  fonction partielle est obtenue
en ne fournissant à une autre fonction qu'une partie de ses arguments.

---

    fu! Describe() dict
        echo 'here are some ' . self.name
    endfu
    let object = {'name': 'fruits'}
    let Description = function('Describe', object)
    call Description()
    here are some fruits~

`function()` peut aussi lier un dico à une fonction.
Ici, on lie le dico `object` à la fonction `Describe()`.
Le résultat est stocké dans le partiel `Description`.

Pour que la fonction puisse y accéder, elle doit porter l'attribut `dict`.
Elle peut alors se référer au dico via sa variable locale `self`.

---

    fu! Describe(count, adj) dict
        echo a:count.' '.a:adj.' '. self.name
    endfu
    let object = {'name': 'piggies'}
    let Description = function('Describe', [3], object)
    call Description('little')
    3 little piggies~

Illustre qu'on peut  lier à une fonction  à la fois une liste  d'arguments et un
dico.

Le dico d'un partiel ne fait pas partie de la liste des arguments.
Il s'agit de 2 ensembles totalement séparés.

San partiel, l'exemple précédent se ré-écrirait de la façon suivante:

    let object = {'name': 'piggies'}
    fu! object.Describe(count, adj)
        echo a:count.' '.a:adj.' '. self.name
    endfu
    call object.Describe(3, 'little')

---

    fu! Describe(i, j, object)
        echo (a:i + a:j).' '.a:object
    endfu
    let Desc = function('Describe', [1])
    let NewDesc = function(Desc, [2])
                           │
                           └ partial

    call NewDesc('piggies')
    3 piggies~

Montre que le nom du 1er argument donné à `function()` n'est pas forcément celui
d'une fonction.
Ce peut  être celui d'une funcref  ou d'un partiel (comme  dans l'affectation de
`NewDesc`).

Montre  aussi  qu'on peut  imbriquer  des  appels  à `function()`  pour  ajouter
progressivement des arguments à un partiel.
Ils sont ajoutés les uns à la suite des autres.

Ici, le 1er appel à `function()` ajoute `1` à la liste des arguments du partiel:

    [] + [1]

Et, le 2e appel lui ajoute `2`:

    [1] + [2]

On pourrait continuer:

    [1,2] + [3]

La dernière commande équivaut à :

    call Describe(1, 2, 'piggies')

---

    fu! Func() dict
        echo self.name
    endfu

    let FR = function('Func')
    let mydict = {'name': 'foo'}
    let mydict.myfunc = FR

    call mydict.myfunc()
    foo~

Un partiel n'est pas le seul moyen de lier une fonction à un dico.
On peut aussi le faire en affectant sa funcref à une clé du dico.
Ici, `Func()` reçoit `mydict` via `self` qd on accède à la clé `myfunc`.

---

    fu! Func() dict
        echo self.name
    endfu

    let FR                = function('Func')
    let mydict            = {'name': 'foo'}
    let mydict.myfunc     = FR
    let other_dict        = {'name': 'bar'}
    let other_dict.myfunc = mydict.myfunc

    call other_dict.myfunc()
    bar~

Si on duplique la fonction `mydict.myfunc` en `other_dict.myfunc`:

    let other_dict.myfunc = mydict.myfunc

... en ayant au préalable associé à cette dernière clé de dico une funcref:

    let mydict.myfunc = FR

... la copie est liée au nouveau dico, pas à l'original.
C'est pourquoi  elle reçoit `other_dict` via  `self`, et elle affiche  `bar`, au
lieu de `foo`.

---

    fu! Func() dict
        echo self.name
    endfu

    let FR                = function('Func')
    let mydict            = {'name': 'foo'}
    let mydict.myfunc     = function(FR, mydict)
    let other_dict        = {'name': 'bar'}
    let other_dict.myfunc = mydict.myfunc

    call other_dict.myfunc()
    foo~

En  revanche, si  on la  duplique  en l'ayant  définie comme  un partiel,  qu'on
utilise pour EXPLICITEMENT lier la fonction au dico:

    let mydict.myfunc = function(FR, mydict)

... la copie reste liée à l'ancien dico.

# ?

Read:

   • :h `function()`
   • :h `funcref()`
   • :h `Funcref`
   • :h `Partial`

