# Types of options
## What are the four types of scope that an option can have?

        - global          (233 options have this type atm: /^'.*\n\s*global$)
        - buffer-local    (57)
        - window-local    (37)
        - global-local    (21)

##
## Do all options have a local value?

No.

Some of them only have a global value.
For example, `'cot'`.

## Does a buffer-local option has a global value? If so, what's its purpose?

Yes.

It's used to initialize the local value in all new buffers.

From `:h local-options`:

> ... for each buffer-local  option there also is a global  value, which is used
> for new buffers.

---

Open a help buffer, then run:

        :setg bt?
            ∅

        :setl bt?
            help

The values are different because `'buftype'` has a local and a global value.

## Does a window-local option has a global value? If so, what's its purpose?

Yes.

*In a given window*, a window-local option has:

        - a global value, to initialize its local value in all buffers being
          displayed there

        - a value local to any given buffer displayed in this window

The global value  of a window-local option  is *not* global to  *all* buffers in
*all* windows; it's global to *all* buffers in a *given* window.
IOW,  there's one  global  value per  window,  and one  local  value per  couple
(window, buffer).

---

Execute:

        :setl nu

        :setg nu?
            nonumber

        :setl nu?
            number

The last 2 commands have different outputs because `'number'` has a global and a
local value.

##
## If I load a new buffer in the current window, does it inherit the local options of the previous one?

No.

## If I open a new window, does it inherit the local options of the previous one?

Yes.

##
## global-local
### What are the 21 global-local options?

        'autoread'
        'backupcopy'
        'balloonexpr'
        'cryptmethod'
        'define'
        'dictionary'
        'equalprg'
        'errorformat'
        'formatprg'
        'grepprg'
        'include'
        'keywordprg'
        'lispwords'
        'makeencoding'
        'makeprg'
        'path'
        'statusline'
        'tagcase'
        'tags'
        'thesaurus'
        'undolevels'

### What are the only two global-local options whose type is not a string?

`'autoread'` is boolean.
`'undolevels'` is numeric.

###
### When is a global-local option local, and when is it global?

It depends on the buffer you consider.

If the buffer has a local copy of  the option, from its point of view the option
is local; i.e. it ignores the global value.

If the buffer has NO local copy of the option, from its point of view the option
is global; i.e. it uses the global value.

### When it's local, is it to a buffer?

Yes for most global-local options.

The only exception is `'stl'`, which is global or local to a *window*.

---

In the  next answers, whenever  we mention a buffer,  in reality we  should have
written “buffer or window”.
But it makes the sentences too cumbersome.

###
### How is a global-local option different compared to a buffer-local one?

You can remove the  local value of a global-local option, but you  can NOT for a
buffer-local one.

You can't for a window-local option either.

### What happens if I remove the local value?

The global value is applied in the buffer.

### What's the difference between removing the local value, and making it copy the global value?

Suppose that you are in a buffer A, and you make the local value copy the global
value.
Then, later, you change the global value from another buffer B, via `:set`.

The change will NOT affect A.
It will only affect how the option is initialized in new buffers.

###
### Where is the global value applied?

In any buffer where the local value has been removed.

### What are its two purposes?

Like for any  buffer-local option, it initializes the local  value of the option
when a new buffer is loaded (or a new window is opened in the case of `'stl'`).

But, it's also applied in all buffers where the local value has been removed.

##
## What are the six `'*prg'` options?

   - 'cscopeprg'
   - 'equalprg'
   - 'formatprg'
   - 'grepprg'
   - 'keywordprg'
   - 'makeprg'

##
# Getting information
## What does `:set` do?

It prints the global options whose value is different than the default.
It also prints the local options whose *local* value is different than the default.

`:set` doesn't care about the global value of a local option.

##
## How to print the *local* values of all local options?

        :setl all

## How to print the *global* values of all local options?

        :setg all

##
## How to print the local options whose *local* value is different than the default?

        :setl

## How to print the local options whose *global* value is different than the default?

        :setg

##
## When I execute `:setl ar?`, `--autoread` is displayed. What does `--` mean?

This prefix is only used for a global-local boolean option.
When displayed,  it means there's no  local value in the  current buffer/window,
and thus the global one is applied.

Atm, only one option is global-local AND boolean: `'autoread'`.
So, you aren't likely to encounter `--` often.

Note that `--autoread` does NOT give any information related to the global value.
In particular, it does NOT mean `'autoread'` is enabled in the current buffer.
The global value could be `0`.

`--autoread` should be read as:

> if you  want to know  which value  is used for  'autoread', don't look  at the
> local value, there's none, check the global value instead

## What happens when 'undolevels' has the local value -123456?   -1?    0?

    ┌─────────────────┬──────────────────────────────────────────────┐
    │ &l:ul = -123456 │ the global value is to be used instead       │
    ├─────────────────┼──────────────────────────────────────────────┤
    │ &l:ul = -1      │ there's no undo in this buffer               │
    ├─────────────────┼──────────────────────────────────────────────┤
    │ &l:ul = 0       │ you can undo only one change,                │
    │                 │ and if you press `u` a second time, you redo │
    └─────────────────┴──────────────────────────────────────────────┘

---

`-123456` is a special value.

That's why `:setl ul<` and `:set ul<` seem to have no effect.
They do have an effect (the same as  for `'ar'`), but you need to assign another
local value to see it.

##
## How to print the list of options whose name contains `break`?

    :h '*break C-d

###
# Setting options
## What are the six commands you can use to set an option?

        ┌──────────┬───────────────────────────────────────────────────────────────────┐
        │ :set     │ affect the global AND local value of the option, whichever exists │
        │ :let &   │                                                                   │
        ├──────────┼───────────────────────────────────────────────────────────────────┤
        │ :setl    │ affect the LOCAL value of the option, if it exists                │
        │ :let &l: │                                                                   │
        ├──────────┼───────────────────────────────────────────────────────────────────┤
        │ :setg    │ affect the GLOBAL value of the option, if it exists               │
        │ :let &g: │                                                                   │
        └──────────┴───────────────────────────────────────────────────────────────────┘

##
## How to make the local value of an option copy the global one?

        :setl option<

---

`:set option<` has the same effect, but it's not documented.

`:setg option<` has no effect.

### For which options does the previous command have a different result?

`'autoread'` and `'undolevels'`.

---

`:setl ar<` and `:setl ul<` *remove* the local value.

##
## Why doesn't `:setg nu` enable the column number in the current window?

`'number'` is a window-local option.

All window-local options have two values:

        - one is local  to the buffer CURRENTLY displayed in the window
        - one is global to any buffer which WILL BE displayed in the window

`:setg nu` sets the global value of `'nu'` to `1`.

But the local value of `'nu'`, the one local to the current buffer, is still `0`.
And the local one has priority over the global one.

### What does it do then?

It  initializes the  local value  of  `'nu'`, for  any buffer  displayed in  the
current window, with `1`.

As a result, if you load another buffer in the window, the column number will be
displayed.

##
## global-local
### How to remove the local value of a global-local option?

        :set option<

#### What's the effect?

Now, the global value will always be used in this buffer.
If you change the global value later, it will be reflected in the buffer.

---

`'stl'` is a particular case, because it's the only global-local option which is
local to a window.

And contrary to a global-local option local to a buffer, its global value is not
applied to all buffers in *all* windows.
The global value of `'stl'` is applied to all buffers in the *current* window.

So, if you execute:

        :setl stl<

The  statusline  should now  always  be  the same  no  matter  the buffer  being
displayed in the current window.
But it should have no effect on the other windows.

#### For which options does the previous command have a different result?

`'autoread'` and `'undolevels'`.

---

`:set ar<` and `:set ul<` make the local value copy the global one.

#### How should I undo the setting of a global-local option in a filetype plugin?

Use:

        :set option<

This will remove the local value, which is how Vim is configured by default:

        $ vim -Nu NONE

        :echo &l:path
        ∅~

        :echo &g:path
        .,/usr/include,,~

---

You could also execute:

        :setl option<
            ^

But it would make  the local value copy the global one, which  is NOT how Vim is
configured by default.

###
### What happens if I assign nothing to the local value of a buffer-local option whose type is a string?

The buffer will use an empty local value.

Example:

        :setl mps=

#### What if the option was global-local?

The buffer will use the global.

Example:

        :setl path=

###

### If I reset a global-local option in my vimrc with `:set`, will it have an effect in other buffers?

It will, but only for a buffer which doesn't have a local value.

###
### What happens if I try to set the local value of a global option?

The global value will be set.

Example:

        " 'cot' has no local value,
        " and yet this command will still reset its global value
        setl cot=

From `:h :setl`:

> If the option does not have a local value the global value is set.

##
## In my vimrc, I need to add/remove a value inside a comma-separated list of values for an option.
### Which command should I execute first?

        :set option&vim

### Why?

Suppose you add the value `foo`, by writing in your vimrc:

        :set option+=foo

Later, you want to replace `foo` with `bar`.
You'll first need to remove `foo`, and so write:

        :set option-=foo
        :set option+=bar

Then, you'll need to remove `:set option-=foo` from your vimrc.
It's awkward  and unreliable (for example,  in the meantime, you  may have added
other values via the command-line).

By resetting `'option'`, you make sure that you start with a known value.

##
## I need to assign a value to `'kp'` which is long and contains many special characters.
### How to avoid a “backslash hell” (aka “when should I put a backslash, and how many”)?

Use a [level of indirection][1].

First define a custom command, then assign it to `'kp'`:

    setl kp=:MyCmd
    com! MyCmd call Func()
    fu! Func()
        " complex commands
        " ...
    endfu

---

This is useful, for example, when the value contains a url:

     setl kp=xdg-open\ https://developer.mozilla.org/search\\?topic=api\\&topic=html\\&q=\
                     ^                                     ^^          ^^           ^^   ^

In this example, when we want to include in the value:

   - a space, we need one backslash
   - a backslash, we need two backslashes

We must escape the characters `?` and `&` to prevent the shell from interpreting
them.
`?` could be interpreted  as a glob, and `&` as a  control operator (run process
in background).

We must add a backslash at the end because Vim will append to the value a space,
as well as the word under the cursor when we'll press `K`.
And we want this extra space to be included the value of `'kp'`.
Otherwise, `:setl` would interpret it as a separation between two option names.

As you can see, it's complicated to remember when to use a backslash, and how many.
A level of indirection using a custom command simplifies the assignment.

### Why this mechanism would *not* work for other `'*prg'` options (like `'grepprg'` and `'makeprg'`)?

Because they can't interpret their values as a Vim command.
Only as an external program.

`'kp'` can interpret  its value as an  external program *and* as  a Vim command,
provided it's prefixed with a colon.

##
## ?

        'path'
            global / buffer-local
            default:    .,/usr/incude,,

Liste des dossiers dans lesquels  chercher lorsqu'on utilise certaines commandes
ou fonctions, tq:

        - gf, gF
        - :find, :sfind, :tabfind
        - fnamemodify()
        - C-r C-p (sur la ligne de commande)
        - commande custom portant l'attribut `-complete=file_in_path`

... auxquelles on passe en argument  des chemins de fichiers relatifs; i.e.: qui
ne débutent pas par:

                    -   /
                    -  ./
                    - ../

Les valeurs de `path` peuvent être des chemins relatifs ou absolus.

## ?

        'cdpath'
            global
            default: ,,

Liste des dossiers dans lesquels chercher  lorsqu'on passe un chemin relatif aux
commandes `:cd` et `:lcd`.

                                     NOTE:

Pour Vim:

        - chemin absolu     chemin commençant par /    ./    ../
        - chemin relatif    tous les autres

                            aka, tout ce qui n'a pas de racine explicite:    /
                                                            OU implicite:    ./    ../

Pour bash:

        - chemin absolu     chemin commençant par /
        - chemin relatif    tous les autres

Qd on passe un chemin relatif à `:[l]cd`, elle doit chercher à le compléter, car
il n'a aucune racine (ni explicite, ni implicite).
Pour ce faire, elle utilise les valeurs contenues dans `'path'`.


                                     NOTE:

Attention:

        .    dossier de travail sur la ligne de commande (:cd ./subdir)
             dossier du fichier courant dans les options 'path', 'cdpath', 'tags'

        ,,   dossier de travail dans les options 'path', 'cdpath', 'tags' (chaîne vide)
        ..   parent du dossier de travail sur la ligne de commande

L'incohérence  de la  signification du  dot,  selon qu'on  est sur  la ligne  de
commande ou dans  une des 3 options citées, s'explique  probablement par le fait
que Vim cherche à suivre la convention du shell sur la ligne de commande.

À savoir que le dot signifie “là où je suis en ce moment“.

Dans le shell, cette phrase signifie effectivement le dossier de travail (`$ pwd`).

Mais dans un buffer, on peut l'interpréter différemment:

        le dossier du fichier courant

“Là où je suis“ n'a pas le même  sens, selon qu'on est sur la ligne de commande,
ou dans un buffer.
Les options `'cdpath'`, `'path'`, `'tags'` raisonnent en terme de buffer.

##
# Issues
## 'foo' is a global option used by a normal/Ex command. I need it to be local to a buffer!

In a filetype plugin, assign the value you would want to give to the local value
of `'foo'` (if it could have one) to a buffer-local variable:

        let b:foo = '...'

In your `vimrc`, write a wrapper around the command.
Use the wrapper to temporarily reset `'foo'`:

        " save 'foo'
        let foo_save = &foo

        " alter 'foo'
        let &foo = get(b:, 'foo', &foo)

        " use the default command
        ...

        " restore 'foo'
        let &foo = foo_save

#
# Terminal

    :set termcap

            voir toutes les options du terminal

            Par opposition à :set all qui affiche toutes les options Vim.

Les deux  derniers caractères du nom  d'une option du terminal  représentent une
entrée dans la bdd termcap interne à Vim.

Les options du terminal (t_xx) permettent  de modifier la valeur d'une entrée de
la bdd termcap interne à Vim.


    :echo $TERM

            affiche le nom du type de terminal

    $ echo $termcap

            Chaîne  configurée  par l'émulateur  de  terminal  pour décrire  ses
            caractéristiques auprès du shell et des pgms qu'il affiche.

# Status Line

Les couleurs de la status line  peuvent être configurées via les HG `StatusLine`
(fenêtre active) et `StatusLineNC` (fenêtres inactives).


        set stl+=%-{minwid}.{maxwid}{item}

Ajoute un item à la status line.

À l'exception du % et de {item}, tous les champs sont facultatifs.

Ils servent à formater l'affichage de l'item:

       * {minwid}     largeur minimale en colonnes

       * .{maxwid}    largeur maximale en colonnes

       * -            justification vers la gauche (utile seulement
                      qd {minwid} > longueur de l'item)

Par défaut, qd {minwid} > longueur de l'item, l'item est justifié vers la droite
et le padding utilise des espaces.

On peut demander à ce que le padding  utilise des 0 (pex pour un item produisant
un nb), en faisant précéder {minwid} d'un 0.

`{item}` peut être entre autres:

        - une expression (ex: MyFunc())
        - f    chemin relatif vers le fichier courant
        - l    n° de la ligne courante
        - n    n° du buffer
        - p    %age de lignes lues
        - v    n° de la colonne virtuelle


        set stl+=\ %.20f

Ajout du chemin relatif vers le buffer courant, précédé d'un espace.

Le chemin ne peut prendre plus de 20 colonnes.

`{minwid}` vaut implicitement 0.

Le  point précédant  20  est  obligatoire, autrement  20  sera interprété  comme
`{minwid}` au lieu de `{maxwid}`.


        set stl+=%-10.20(%l,%c%)

Ajout du n° de la ligne, d'une virgule et du n° de la colonne.

L'ensemble doit occuper entre 10 et 20 colonnes et être justifié à gauche (-).

`%-n.m(...%)` permet  de regrouper un ensemble  d'items afin de les  justifier à
gauche et/ou leur attribuer une largeur min/max.


        set stl+=\ %m%r%y%w

Ajout  des flags  modifié  / read-only  /  type de  fichier  / fenêtre  preview,
précédés d'un espace.


        let &stl.='%%  '
        set stl+=%%\ \

Ajout du symbole pourcent suivi de 2 espaces.


        set stl+=%<

Si  la  stl  est trop  longue,  ne  pas  afficher  ce qui  suit  (indicateur  de
troncation).


        set stl+=%=

Les prochains items doivent s'afficher à droite de l'écran.


        set statusline+=%{&ft=='python'?'success':'failure'}

Ajoute la chaîne 'success' si le type  de fichiers du buffer courant est python,
'failure' autrement.

`%{expr}` est une syntaxe permettant d'ajouter l'évaluation d'une expression.

Elle est  évaluée dans  le contexte du  buffer qui s'affiche  dans la  fenêtre à
laquelle appartient chaque status line.

Ceci  permet, pex,  d'afficher  un  indicateur signalant  si  chaque buffer  est
modifié ou non.


        set stl+=%#Keyword#

Utiliser le HG Keyword pour mettre en couleurs la suite de la status line.


        set stl+=%1*

Utiliser le HG `User1` pour mettre en couleurs la suite de la status line.

Le HG `User1` peut être défini comme  on veut: manuellement, ou linké à un autre
HG (pex `:highlight link User1 StatusLine`).

On peut utiliser jusqu'à 9 HG `User{N}`:

        %1* ... %9*


        set stl+=%*

Restaure le HG StatusLine pour la suite des items.
`%*` est la forme abrégée de `%0*`.


        set stl+=%{test\ ?\ expr1\ :\ expr2}
        let &stl.='%{test ? expr1 : expr2}'

Ajoute une expression conditionnelle  utilisant l'opérateur conditionnel `?:` et
contenant des espaces.


        set stl=!%MyFunc()

Définit l'intégralité de la status line comme étant la sortie de `MyFunc()`.

Si on veut intégrer dans sa status line :

        - le n° du buffer
        - le chemin vers son fichier
        - le n° de la ligne courante
        - le symbole '+' si le buffer est modifié

... il faudra écrire dans `MyFunc()` qch comme:

        let string = '%n'
        let string .= '%f'
        let string .= '%l'
        let string .= "%{&mod ? '+' : ''}"
        return string

`MyFunc()` va alors  procéder à diverses concaténations et  retourner une grande
chaîne qui sera ensuite évaluée.


                                     NOTE:

On ne pourrait pas écrire:

        let string .= &mod ? '+' : ''

En effet, `MyFunc()` (et  donc l'expression `&mod ? '+' :  ''`) est évaluée dans
le contexte du buffer de la fenêtre ayant le focus.

Cela implique que,  si le buffer de la fenêtre  active est modifié, l'indicateur
de modification `+`  apparaîtraient dans toutes les fenêtres, même  si les elles
affichaient des buffers non modifiés.

# Commandes

        " ✘
        set option=<SID>MyFunc

        " ✔
        let &option = s:snr() . 'MyFunc'

Si on veut attribuer à la valeur d'une  option le nom d'une fonction locale à un
script, on ne peut pas toujours utiliser `<SID>`.

En effet, la traduction de `<SID>` est une propriété des commandes de mapping.
Donc  `:set  option=<SID>MyFunc`  ne  peut  fonctionner  qu'à  l'intérieur  d'un
mapping.

Une solution consiste à utiliser la 2e syntaxe:

        let &option = s:snr() . 'MyFunc()'

... où `s:snr()` est définie comme suit:

        fu! s:snr()
            return matchstr(expand('<sfile>'), '<SNR>\d\+_')
        endfu


        :set all

Afficher toutes les options Vim.


        :set all&

Réinitialiser toutes les options.

Attention, ceci pourrait poser pb avec des plugins qui avaient modifié la config
par défaut pour leur besoin.
`:h :set-default`:  Warning: This may have a lot of side effects.


        :set ts^=2

Multiplie par 2 la valeur de l'option 'tabstop'.

Illustre qu'on  peut utiliser l'opérateur  `^=` pour multiplier la  valeur d'une
option numérique.


Qd on donne une  valeur à une option via la commande :set,  il faut échapper les
espaces, les pipes et les ", pour leur faire perdre leur caractère syntaxique.

En effet, `:set` interprète:

        - un espace          comme un séparateur entre 2 options

        - un pipe            comme une terminaison de commande

        - un double quote    comme le début d'un commentaire (tout ce qui suit
                             est ignoré)


Un ensemble d'options peuvent configurer Vim dans un certain nb d'états.

On  peut vouloir  passer en  revue toute  ou  partie de  ces états  via un  même
mapping.

Pour ce faire,  on peut créer un dictionnaire dont  les clés représentent chaque
état.

La valeur d'une  clé doit être une  commande choisie de telle façon  que si elle
était exécutée, elle ferait passer Vim dans un autre état, celui de son choix.

Le mapping n'aura alors plus qu'à exécuter la valeur du dictionnaire dont la clé
est l'état courant.

Pex, si `op1` et `op2` sont des options dont les valeurs sont des booléens:

        :exe mydic[&op1 . &op2]

D'un point de vue théorique:

    - le dictionnaire est un modèle de calcul mathématique appelé fsm
      (finite-state machine)

    - les clés sont les états de la machine

    - les valeurs sont les évènements déclencheurs de transitions entre 2 états


                                     NOTE:

On peut représenter un état de la machine via une chaîne contenant:

        - les valeurs des options qui la définissent

          On peut l'obtenir, pex, via join():

                join([&op1, ...], ',')

        - un nb

          Si les options sont  des booléens et que leurs valeurs  sont donc 0 ou
          1, on peut l'obtenir directement:

                &op1 . &op2 . ...

          Les nb seront convertis automatiquement en chaîne et concaténés.

          Autrement,  si les  options ont  des valeurs  plus complexes,  on peut
          obtenir le nb représentant un état de la machine, via index():

                index(states, [&op1, ...])

          Où states est une liste de listes.

          Chaque  liste  qu'elle  contient   regroupe  un  ensemble  de  valeurs
          d'options configurant un état donné.

          Les valeurs dans les listes de states et dans [&op1, ...] doivent être
          tjrs dans  le même ordre, pour  que index() puisse trouver  l'index de
          l'état courant à l'intérieur de `states`.

          Le mapping n'a plus qu'à exécuter la commande permettant la transition
          vers un autre état:

                :exe mydic[index(states, [&op1, ...])]

          La dernière commande :exe peut se décomposer comme ceci:

                states                liste de tous les états possibles
                [&op1, ...]           état courant
                index(states, [...])  position de l'état courant au sein de la fsm (clé du dico)
                mydic[index(...)]     commande pour activer la transition vers le prochain état
                exe mydic[...]        activer la transition


Exemple de mapping illustrant la méthode:

        exe 'set ve=' . {
                        \ ''        : 'block',
                        \ 'block'   : 'all',
                        \ 'insert'  : 'block',
                        \ 'all'     : '',
                        \ 'onemore' : 'block',
                        \ }[&ve]

Au passage, on note  qu'ici on n'a pas eu besoin de  `join()` car les différents
états sont contrôlés par une seule option (`'ve'`).

On remarque aussi  que si les commandes activant la  transition vers un prochain
état suivent toutes la même syntaxe  (comme ici: `set ve={next_state}`), on peut
extraire des valeurs du dico le bout de commande qui se répète (`set ve=`).

Du coup, les valeurs du dico ne sont plus des commandes mais des états.

En résumé, il associe à chaque état possible, le prochain état désiré.


Même si on  n'est pas intéressé par un  état donné, pour que le  mapping soit le
plus robuste possible, il vaut mieux l'inclure dans le dictionnaire.

En  effet, même  si le  mapping ne  devrait jamais  nous amener  à cet  état non
désiré, on pourrait s'y retrouver par accident pour une autre raison.

Dans ce cas, lorsque le mapping serait tapé, on aurait l'erreur:

        E716: Key not present in Dictionary: ...



De nombreuses  options (comme  `'fo'`) prennent  automatiquement une  valeur par
défaut lorsque `'compatible'` est (dés)activée:

                                     NOTE:

> This option is set to the Vi default value when 'compatible' is set and to the
> Vim default value when 'compatible' is reset.

Cette option est activée par défaut, sauf si Vim trouve un vimrc utilisateur (!=
système, != -u ...) au cours de son démarrage.

Dans ce cas, elle est désactivée.

Conseil: ne pas écrire 'set nocompatible' dans son vimrc, pour 2 raisons:

        1. inutile, l'option est déjà désactivée

        2. à chaque fois qu'on source  son vimrc, 'set nocp' réinitialiserait
           plein d'options.


Une option locale à une fenêtre est en réalité liée à un buffer dans une fenêtre.
On peut le vérifier comme ceci:

        " in a buffer `foo`
        :let [&g:cul, &l:cul] = [1, 0]
        :e bar
        :echo &l:cul
        1~

La dernière commande affiche 1 et non pas 0.

Si  l'option 'cursorline'  était réellement  locale à  une fenêtre,  le fait  de
charger un nouveau  buffer dans la fenêtre  ne devrait pas changer  la valeur de
&l:cul.

Or, ici, le fait de charger bar a changé sa valeur: elle est passée de 0 à 1.

La ligne courante est passée de non-mise en surbrillance à mise en surbrillance.

Pk?

Car lorsqu'on charge bar dans la  fenêtre courante, on affiche un nouveau couple
buffer-fenêtre.

Dans ce nouveau  couple, l'option 'cul' reçoit comme valeur  globale la valeur 1
(à cause  de la 1e  commande), et  comme valeur locale  1 aussi (héritage  de la
valeur globale).


Un buffer peut être dans 3 états:

        ┌─────────┬──────────────────────────────────────────────────────────┐
        │ actif   │ affiché dans une fenêtre                                 │
        ├─────────┼──────────────────────────────────────────────────────────┤
        │ caché   │ non affiché dans une fenêtre mais tjrs chargé en mémoire │
        ├─────────┼──────────────────────────────────────────────────────────┤
        │ inactif │ non affiché, non chargé en mémoire                       │
        └─────────┴──────────────────────────────────────────────────────────┘

On  dit qu'on  abandonne  un buffer  quand  on ferme  la  dernière fenêtre  dans
laquelle il était affiché.

Il peut alors devenir caché ou pas en fonction de certaines options.

Un buffer est caché s'il est chargé dans la mémoire mais affiché dans une aucune
fenêtre.


On peut créer divers types de buffers spéciaux via les 4 options suivantes:

        'bufhidden', 'buftype', 'swapfile', 'buflisted'

Lire :h special-buffers


On peut accéder à l'ensemble des options regroupées par thèmes via :opt[ions].
Depuis la fenêtre qui s'ouvre, on peut appuyer sur CR, le curseur étant sur:

    - une ligne numérotée de l'index ('1 important', '2 moving around', ...),
      pour se rendre au paragraphe contenant l'ensemble des options concernées

    - le titre numéroté d'un paragraphe ou la ligne vide juste en-dessous, pour
      revenir à l'index

    - une ligne contenant un nom d'option à l'intérieur d'un paragraphe, pour
      ouvrir une fenêtre d'aide décrivant l'option concernée

    - une ligne contenant la commande :set, soit pour toggle une option de type
      booléen, soit pour exécuter la commande après qu'on l'ait éditée

Si on modifie  la valeur d'une option  depuis la ligne de  commande (sans passer
par  la fenêtre),  on peut  rafraîchir  la ligne  de la  fenêtre :opt  contenant
l'option concernée en positionnant le curseur  sur cette dernière et en appuyant
sur espace.

#
# Options Diverses
## Commandes

        :set colorcolumn=80

Affiche une ligne verticale rouge sur la 80e colonne.

Utile qd on écrit du code et qu'il  existe une règle imposant de ne pas dépasser
un certain nb de caractères par ligne.

Permet de voir qd il faut passer à la  ligne qd on écrit et aussi ce qui dépasse
dans ce qui a déjà été écrit.


        :set list nolist list!

Active list, désactive list, toggle list.

        :set fo+=t

Ajoute le flag `t`  à la valeur globale de l'option `'fo'`  ainsi qu'à sa valeur
locale dans le buffer courant.

N'a aucun impact sur la valeur locale des autres buffers existants déjà.


        :verb setg fo?
        :verb setl fo?

Affiche  le dernier  fichier  à avoir  modifié  la valeur  globale  / locale  de
l'option `'fo'`.

Si on tape: `:verb set fo?`
Atm, Vim affiche le dernier fichier ayant modifié la valeur locale.

Pk?

Probablement parce que la  locale a priorité sur la globale,  et c'est donc elle
qui agit dans le buffer courant.


        :set fo&

Réinitialise l'option `'fo'` en lui donnant sa valeur par défaut.

Celle indiquée dans l'aide de Vim, càd hors vimrc et hors ft plugins.


        :setl bt=nofile nobl noma bh=wipe noswf

Crée un buffer spécial (scratch) laissant un minimum de trace.


        :set ft fenc ff

Afficher le  type de fichier,  son encodage (utf-8, ascii,  ...), et
son format (unix, dos, ...).


        :set isf^=\ 

Ajoute l'espace à l'option `'isf'`.

                                     NOTE:

        set isf+=\ 
        " ou
        let &isf .= ' '

ne fonctionnent pas,  sans doute parce qu'il est impossible  d'avoir un espace à
la fin de la valeur d'une option.

## Noms

        'bufhidden'
            buffer-local
            default: ''

Détermine ce qui se passe lorsqu'on abandonne le buffer courant.
Comme elle est locale, elle a priorité sur 'hidden'.

Par défaut 'bh' vaut '', ce qui  signifie qu'elle se conforme à l'option globale
'hidden'.

Elle peut prendre 4 autres valeurs :

        'hide'      le buffer reste chargé
        'unload'    il est déchargé mais reste dans la liste des buffers
        'delete'    il est déchargé et passe en non-listé dans la liste des buffers
        'wipe'      il est déchargé et totalement supprimé de la liste des buffers


        'buftype'
            buffer-local
            default: ''

Permet de créer un type de buffer spécial, pour lequel les opérations d'écriture
et  de fermeture  de  la fenêtre  ne  sont  pas gérées  comme  pour les  buffers
standards.

Par défaut elle vaut '', ce qui signifie que le buffer est normal.
On peut lui donner une autre valeur parmi 5 possibles dont 'nofile'.

“nofile“ signifie que le buffer ne correspond  pas à un fichier et qu'il ne peut
pas être écrit.

Utile pour éviter un message d'avertissement  parce que le buffer est modifié et
que l'option 'hidden' est désactivée.

Utile pour tester si le buffer courant est spécial ou non:

        !empty(&buftype)


        'includeexpr'
            buffer-local
            default: ''

Si Vim  échoue à ouvrir  le fichier  dont le chemin  est sous le  curseur (parce
qu'il a  mal sélectionné ce dernier),  lui demande de retenter  avec une version
modifiée du chemin Le chemin initialement tenté est stocké dans v:fname.

Ex d'utilisation:

        set includeexpr=substitute(v:fname, '.*=', '', '')

Retente d'ouvrir le fichier en supprimant tout ce qui se trouve après le dernier
symbole =.


        'matchpairs'
            buffer-local
            default:    '(:),{:},[:]'

Contient une liste  de paires de caractères  entre lesquels on se  déplace qd on
appuie sur `%`.
Les caractères d'une paire doivent être différents (pex, pas de ":"), et séparés
par un `:`.

Pex, pour ajouter les chevrons dans un buffer html:

        :setl mps+=<:>


        'swapfile'
            buffer-local
            default: on

Détermine si le buffer  sera copié dans un fichier swap ou  s'il ne sera présent
que dans la RAM.

Dans ce dernier cas, on ne pourra pas récupérer le fichier en cas de pb.


        'term'

Stocke  la  valeur  de  la  variable d'environnement  shell  $TERM  le  nom  que
l'émulateur de terminal se donne.

`:echo &term` ou `:echo $TERM` permet de la lire


        ┌────────────────────────┬──────────────┬────────────────────────────────────┐
        │ 'textwidth'     / 'tw' │ buffer-local │ default: 0                         │
        ├────────────────────────┼──────────────┼────────────────────────────────────┤
        │ 'wrapmargin'    / 'wm' │ buffer-local │ default: 0                         │
        ├────────────────────────┼──────────────┼────────────────────────────────────┤
        │ 'formatoptions' / 'fo' │ buffer-local │ default: tcq                       │
        ├────────────────────────┼──────────────┼────────────────────────────────────┤
        │ 'columns'       / 'co' │ global       │ default: 80 ou largeur du terminal │
        └────────────────────────┴──────────────┴────────────────────────────────────┘

Ces  4 options  (en particulier  les 2  premières) contrôlent  la longeur  d'une
ligne, i.e. qd une ligne est wrappée en dur automatiquement.

Par défaut, 'co' est configurée automatiquement par le terminal qui lui donne le
nb de colonnes qu'il peut afficher actuellement.

Elle est mise à jour dès qu'on redimensionne le terminal.

Réciproquement, elle permet de changer la largeur du terminal depuis Vim.


                                     NOTE:

Influence de `'tw'` et `'wm'` qd on écrit des lignes:

   - &l:tw = &l:wm = 0   ||   &l:fo ne contient pas 'c' (comment line) / 't' (code/text line)
     elles ne sont pas wrappées

   - &l:tw = 0 && &l:wm != 0   &&   &l:fo contient 'c' / 't'
     elles sont wrappées dès que leur longueur dépasse    winwidth(0) - &l:wm

   - &l:tw  != 0   &&   &l:fo contient 'c' / 't'
    elles sont wrappées dès que leur longueur dépasse &l:tw


                                     NOTE:

Influence de `'tw'` et `'wm'` qd on formate des lignes (via gq/gw):

   - &l:tw != 0
     elles sont  wrappées au-delà  de &l:tw  caractères (peu importe la valeur de 'fo')

   - &l:tw = 0
     les lignes sont wrappées qd leur longueur dépasse:

       - winwidth(0) - &l:wm,     si &l:wm != 0
       - min(79, winwidth(0)),    si &l:wm == 0


                                     NOTE:

Largeur de la fenêtre != `&co` si la fenêtre est splittée verticalement.


                                     NOTE:

Les flags `'tc'`  de l'option `'fo'` ne formatent pas  automatiquement une ligne
préexistante qu'on édite après coup.

Pour ajouter le formatage automatique des lignes d'un paragraphe lorsqu'on édite
une de  ses lignes (ajout/suppression  de texte), il faut  donner le flag  `a` à
`'fo'`.


        'thesaurus'
            global / buffer-local

Contient une  suite de chemins vers  des fichiers contenant sur  chaque ligne un
groupe de synonymes.
Ex de fichier de synonymes:

        https://www.gutenberg.org/files/3202/files/mthesaur.txt


                                     NOTE:

Sur une  même ligne,  les synonymes  doivent être séparés  par un  caractère qui
n'est pas dans `'isk'`.

Un espace ou une virgule pex.

Si on ajoute temporairement l'espace à  `'isk'` lors d'une complétion pour qu'un
synonyme contenant  des espaces  soient bien considérés  comme un  seul synonyme
(ex: 'of  vital importance'), il ne  faut évidemment pas utiliser  l'espace pour
séparer 2 synonymes.

Autrement, chaque ligne entière serait considérée comme un seul synonyme.

Préférer la virgule dans ce cas.


        'updatecount'
            global
            default: 200

Nb de  caractères tapés au-delà  desquels le fichier  d'échange sera
écrit sur le disque.

Si vaut 0, aucun fichier swap n'est créé.

`'swapfile'` a  la priorité  sur `'uc'`,  car c'est une  option locale  (local >
global).


        'updatetime'
            global
            default: 4000

Durée en  ms au-delà  de laquelle  Vim écrit le  fichier d'échange  utilisée par
l'évènement `CursorHold`.


        'suffixes'
            global
            default:    '.bak,~,.o,.h,.info,.swp,.obj'

Qd on développe un pattern contenant  un wildcard, les fichiers dont l'extension
est présente dans `&su`, sont traités avec une priorité inférieure aux autres.

Ça  signifie qu'ils  sont ignorés  sauf si  aucun fichier  dont l'extension  est
en-dehors de &su ne match le pattern (sure?).

De plus, les fichiers dont l'extension est dans &su sont cherchés en dernier par
la commande :vimgrep (et sans doute ses amies :lvimgrep ...).


        'viminfo'

Contient une liste de paramètres et de valeurs séparés par des virgules.

Détermine  essentiellement  quelles  informations   seront  mémorisées  entre  2
sessions et dans quel fichier.

        ┌─────────────────────┬────────────────────────────────────────────────────────────────────┐
        │ '100                │ mémorise les marques de jusqu'à 100 fichiers différents au maximum │
        ├─────────────────────┼────────────────────────────────────────────────────────────────────┤
        │ n~/.vim/tmp/viminfo │ stocke les infos dans `~/.vim/tmp/viminfo` (au lieu de ~/.viminfo) │
        └─────────────────────┴────────────────────────────────────────────────────────────────────┘


        'wildignore'
            global
            default: ''

Les fichiers dont le  nom match un pattern présent dans &wig  sont ignorés qd on
développe une expression  contenant un wildcard ou qd on  fait une recherche via
`:vimgrep` (et sans doute ses amies `:lvimgrep`...).

##
# TODO

Document that when you save, change,  and restore an option, the environment may
change, and you must take that into account.

For  example, if  your  function  temporarily changes  `'isk'`,  and change  the
current buffer, when you restore `'isk'`, you can't simply write:

    let &l:isk = isk_save

Instead, you must write:

    let bufnr = bufnr('%')
    ...
    call setbufvar(bufnr, '&isk', isk_save)

Have a look  at `vim#jump_to_tag()` in `~/.vim/plugged/vim-vim/autoload/vim.vim`
for a real example.

---

Document that restoring an option after `CompleteDone` is not reliable.
The latter is not fired when you quit the completion menu by pressing `C-c`.
You must also listen to `TextChanged` or `CursorMoved`, because those are fired.
Read our comment in `completion#util#custom_isk()`:

    ~/.vim/plugged/vim-completion/autoload/completion/util.vim

Check whether we've made this mistake in our vimrc or in other plugins.

---

Document that  you should  use `&option`  instead of  `&l:option`, when  you use
`getbufvar()`, `getwinvar()`, `setbufvar()`, `setwinvar()`, ...

`&l:option` doesn't work with `setbufvar()`, while `&option` works everywhere.

##
# Reference

[1]: https://gist.github.com/romainl/8d3b73428b4366f75a19be2dad2f0987
