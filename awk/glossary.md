# c

    constant

There are 2 kinds of constants:

   - string
   - numerical

# e

    expression

Un expression est une combinaison d'une ou plusieurs:

   - array
   - constante
   - invocation de fonction
   - opérateur
   - variable

... qu'un langage de programmation:

   - interprète (en respectant des règles de précédences et d'association)
   - calcule
   - à partir du résultat, produit une nouvelle valeur d'un type donné
     (numérique, chaîne, logique - vrai / faux, fonction, nouvelle expression ...)

En mathématiques, ce procédé est appelé "évaluation".

---

    regular expression

Une expression régulière  est une combinaison d'opérateurs  et de métacaractères
encadrée par une paire de délimiteurs (typiquement /).

On  peut  aussi  utiliser  une  chaîne   comme  regex,  mais  dans  ce  cas  les
métacaractères  doivent être  doublement  échappés car  le  parser d'awk  retire
automatiquement un  backslash présent dans  une chaîne  pour changer le  sens du
caractère suivant (métacaractère ↔ caractère littéral).

IOW, pour alterner  entre le sens spécial  / littéral d'un caractère,  il faut 2
backslashs dans une chaîne: un pour awk, et un pour le moteur de regex.

L'avantage d'utiliser une chaîne plutôt  qu'une regex, est qu'on peut décomposer
le  pattern en  plusieurs  sous-chaînes  stockées dans  des  variables aux  noms
évocateurs.

Il faudra ensuite concaténer leurs valeurs pour retrouver le pattern global.
Une décomposition  judicieuse augmente  la lisibilité  d'une regex  complexe, et
facilite sa maintenance.

# f

    control flow

Ordre dans lequel les instructions d'un programme impératif sont exécutées.

La manipulation  explicite du  flot de  contrôle par  le programmeur,  grâce aux
structures  de  contrôle, est  la  principale  caractéristique des  langages  de
programmation impératifs vis-à-vis des autres paradigmes de programmation.


    graphe de flot de contrôle

Ensemble de tous les flots de contrôle possibles d'un programme.


    input

Ensemble des données traitées par le pgm awk.


    ┌─────────────────────────────┬──────────────────────────────┐
    │ opérateur de comparaison    │ relationnel + correspondance │
    ├─────────────────────────────┼──────────────────────────────┤
    │ opérateur relationnel       │ ==  !=  <  >  <=  >=         │
    ├─────────────────────────────┼──────────────────────────────┤
    │ opérateur de correspondance │ !   !~                       │
    └─────────────────────────────┴──────────────────────────────┘


    opérateur unaire / binaire

Opérateur associant une valeur à 1/2 opérande(s).
Ex:

    + est un opérateur arithmétique BINAIRE:    1 + 2    →    3
    ? est un opérateur de regex UNAIRE:         r?       →   'r' ou ''


    passage par valeur / référence

Qd une fonction est appelée, et qu'un de ses paramètres est une variable définie
précédemment, on dit qu'on lui “passe une variable“.
Ex:

    function calculateBirthYear(int yourAge) {
        return CURRENT_YEAR - yourAge;
    }

    int myAge = 24;
    calculateBirthYear(myAge);

Dans   cet  exemple,   à   la  fin,   la  variable   `myAge`   est  “passée”   à
`calculateBirthYear()` pour calculer mon année de naissance.
Mais  `myAge` peut  être  passée de  2  façons différentes:  par  valeur ou  par
référence.

    ┌───────────────┬────────────────────────────────────────────────────────────────────────┐
    │ par valeur    │ une copie de `myAge` est créée (`yourAge`), puis passée à la fonction  │
    │               │                                                                        │
    │               │ si la fonction modifie la copie, l'originale (`myAge`) n'est pas       │
    │               │ affectée                                                               │
    ├───────────────┼────────────────────────────────────────────────────────────────────────┤
    │ par référence │ l'adresse mémoire de `myAge` (sa référence) est passée à la fonction   │
    │               │                                                                        │
    │               │ si la fonction modifie `yourAge`, l'originale (`myAge`) est elle-aussi │
    │               │ modifiée                                                               │
    └───────────────┴────────────────────────────────────────────────────────────────────────┘


    record / enregistrement

awk divise automatiquement l'input en records.
Par défaut, il le fait en considérant les newlines comme séparateurs.


    séquence d'échappement

Une chaîne peut contenir les séquences d'échappement suivantes:

    ┌─────┬─────────────────────────────────┐
    │ \b  │ backspace                       │
    ├─────┼─────────────────────────────────┤
    │ \f  │ form feed                       │
    │     │                                 │
    │     │ force l'imprimante à éjecter    │
    │     │ la page courante, et à continuer│
    │     │ d'imprimer sur une nouvelle page│
    ├─────┼─────────────────────────────────┤
    │ \n  │ line feed                       │
    ├─────┼─────────────────────────────────┤
    │ \r  │ carriage return                 │
    │     │                                 │
    │     │ repositionne le curseur         │
    │     │ au début de la ligne courante   │
    ├─────┼─────────────────────────────────┤
    │ \t  │ tab                             │
    ├─────┼─────────────────────────────────┤
    │\123 │ caractère dont le code          │
    │     │ octal est `123`                 │
    ├─────┼─────────────────────────────────┤
    │ \\  │ backslash littéral              │
    ├─────┼─────────────────────────────────┤
    │ \"  │ double quote littéral           │
    └─────┴─────────────────────────────────┘


    structure de contrôle

Une  structure de  contrôle est  une  instruction particulière  d'un langage  de
programmation impératif pouvant dévier le flot de contrôle d'un programme.

Quelques catégories de structures de contrôle:

   - les alternatives (if, if–else,  switch, ...)
   - les boucles  (while, do–while, for, ...)
   - les constructions de gestion  d'exceptions (try–catch,  ...)

---

    sucre syntaxique

Une construction  syntaxique est  qualifiée de  “sucre syntaxique“,  à condition
qu'elle remplisse les 2 conditions suivantes:

   - elle simplifie la lecture/écriture d'une autre construction syntaxique

   - sa suppression ne ferait pas perdre d'expressivité, ou de fonctionnalité au
     langage de programmation


Exemple:

`printf   "fmt",  expr-list`   est   probablement  du   sucre  syntaxique   pour
`printf("fmt", expr-list)`.


Autre exemple:

Dans un langage  de programmation, pour obtenir un élément  d'une array, il faut
généralement invoquer une fonction système à laquelle on passera 2 arguments.
Notons-les pex:

   - la fonction:                                              get_array()
   - le 1er argument, l'array:                                 Array
   - le 2e  argument, un indice sous la forme d'un vecteur:    vector(i,j)

        get_array(Array, vector(i,j))    →    Array[i,j]
        │                                     │
        │                                     └ sucre syntaxique
        └ écriture fondamentale

De  la  même  façon,  donner  une  valeur  à  un  élément  d'une  array  revient
généralement à invoquer une fonction à laquelle on passe 3 arguments:

   - set_array()
   - Array
   - vector(i,j)
   - value

        set_array(Array, vector(i,j), value)    →    Array[i,j] = value
        │                                            │
        │                                            └ sucre syntaxique
        └ écriture fondamentale

Les  processeurs du  langage (interpréteur,  préprocesseur, compilateur  ...) se
chargent de développer du sucre syntaxique en constructions fondamentales, avant
de traiter le code: on parle de “désucrage“ (“desugaring“).

# s

    statement

This can be a `pattern { action }`, or a command inside an action.

# v

    value

A value is an expression whose evaluation can not be reduced to a simpler form.

