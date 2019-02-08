# c
## constant

There are 2 kinds of constants:

   - string
   - numerical

## control flow

Order  in which  individual statements,  instructions  or function  calls of  an
imperative program are executed or evaluated.

The emphasis  on explicit control  flow distinguishes an  imperative programming
language from a declarative programming language.

Within  an  imperative programming  language,  a  control  flow statement  is  a
statement, the execution of which results in  a choice being made as to which of
two or more paths to follow.

## ?

    structure de contrôle
    control structure

Une  structure de  contrôle est  une  instruction particulière  d'un langage  de
programmation impératif pouvant dévier le flot de contrôle d'un programme.

Quelques catégories de structures de contrôle:

   - les alternatives (if, if–else,  switch, ...)
   - les boucles  (while, do–while, for, ...)
   - les constructions de gestion  d'exceptions (try–catch,  ...)

## ?

    control flow graph

<https://en.wikipedia.org/wiki/Control_flow_graph>

Ensemble de tous les flots de contrôle possibles d'un programme.

##
# e
## escape sequence

A string can contain the following escape sequences:

    ┌───────┬──────────────────────────────────┐
    │  \b   │ backspace                        │
    ├───────┼──────────────────────────────────┤
    │  \f   │ form feed                        │
    │       │                                  │
    │       │ ask the printer to eject         │
    │       │ the current page, and continue   │
    │       │ printing on a new page           │
    ├───────┼──────────────────────────────────┤
    │  \n   │ line feed                        │
    ├───────┼──────────────────────────────────┤
    │  \r   │ carriage return                  │
    │       │                                  │
    │       │ position the cursor at the       │
    │       │ beginning of the current line    │
    ├───────┼──────────────────────────────────┤
    │  \t   │ tab                              │
    ├───────┼──────────────────────────────────┤
    │ \123  │ character whose octal code       │
    │       │ is `123`                         │
    ├───────┼──────────────────────────────────┤
    │ \x123 │ character whose hexadecimal code │
    │       │ is `123`                         │
    ├───────┼──────────────────────────────────┤
    │  \\   │ literal backslash                │
    ├───────┼──────────────────────────────────┤
    │  \"   │ literal double quote             │
    └───────┴──────────────────────────────────┘

## expression

A combination of one or more:

   - arrays
   - constants
   - functions
   - operators
   - variables

... which a programming language (such as awk):

   1. interprets (according to its particular rules of precedence and of association)
   2. computes
   3. from the result, produces a new value of a given type
      (numerical, string, logical - true / false, function, ...)

In mathematics, this process is called “evaluation”.

##
# i
## input

Set of all data processed by awk.

##
# o
## ?

    ┌─────────────────────────────┬──────────────────────────────┐
    │ opérateur de comparaison    │ relationnel + correspondance │
    ├─────────────────────────────┼──────────────────────────────┤
    │ opérateur relationnel       │ ==  !=  <  >  <=  >=         │
    ├─────────────────────────────┼──────────────────────────────┤
    │ opérateur de correspondance │ !   !~                       │
    └─────────────────────────────┴──────────────────────────────┘

## ?

    opérateur unaire / binaire

Opérateur associant une valeur à 1/2 opérande(s).

Ex:

    + est un opérateur arithmétique BINAIRE:    1 + 2    →    3
    ? est un opérateur de regex UNAIRE:         r?       →   'r' ou ''

##
# r
## record

Awk splits automatically the input into records.
By default, it considers a newline as a separator between 2 consecutive records.

## regular expression

It can be either:

   - a combination of operators and metacharacters surrounded by a pair of
     delimiters (typically `/`)

   - a string

##
# s
## statement

This can be a `pattern { action }`, or a command inside an action.

## ?

    syntactic sugar

Une construction  syntaxique est  qualifiée de  “sucre syntaxique“,  à condition
qu'elle remplisse les 2 conditions suivantes:

   - elle simplifie la lecture/écriture d'une autre construction syntaxique

   - sa suppression ne ferait pas perdre d'expressivité, ou de fonctionnalité au
     langage de programmation


Exemple:

`printf   "fmt",  expr-list`   est   probablement  du   sucre  syntaxique   pour
`printf("fmt", expr-list)`.


Autre Exemple:

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

##
# v
## value

A value is an expression whose evaluation can not be reduced to a simpler form.

## ?

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

