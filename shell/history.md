# What's the benefit of a history expansion compared to editing the command-line with readline key bindings?

It can be faster.

# What are the 3 main steps into which a history expansion can broken down?

   1. selection of an event from the history list

   2. selection of words from this event

   3. modification of the words

# ?

2 composants consécutifs d'un développement d'historique:

   - désignateur d'évènement
   - désignateur de mots
   - modificateurs

... doivent être  séparés par un `:`.
`:` peut être  omis entre un désignateur d'évènement et  un désignateur de mots,
si ce dernier commence par un des caractères suivants: `^$*`


    zen: pas d'exemples tordus, que du vraisemblable
         du plus simple au plus compliqué (pas l'inverse)

    ┌────────────────┬────────────────────────────────────────────────────────────────────────────────────────┐
    │ !!             │ dernière commande (forme abrégée de `!-1`)                                             │
    │ !1             │ première commande                                                                      │
    │ !-2            │ avant-dernière commande                                                                │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !com           │ commande la plus récente et COMMENÇANT par la chaîne ’com’                             │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !?mand         │ commande la plus récente et CONTENANT la chaîne ’mand’                                 │
    │                │                                                                                        │
    │                │ si un désignateur de mots doit suivre, il faut utiliser un 2e `?`; ex:                 │
    │                │                                                                                        │
    │                │     !?mand?$    →    dernier argument de la précédente commande contenant ’mand’       │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !#             │ toute la ligne de commande tapée jusqu'ici                                             │
    │                │                                                                                        │
    │ !#:2           │ le 2e argument de la ligne courante                                                    │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !^             │ 1er argument de la dernière commande                                                   │
    │                │                                                                                        │
    │                │ on remarque que lorsque `!!` est suivi d'un désignateur de mots ou d'un modificateur,  │
    │                │ on peut l'abréger en `!`                                                               │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !$             │ dernier argument                                                                       │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !*             │ tous les arguments                                                                     │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !:0            │ nom de commande de la dernière commande                                                │
    │ !:3            │ 3e argument                                                                            │
    │ !:2-4          │ arguments entre 2 et 4                                                                 │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !:-3           │ commande + arguments entre 1 et 3                                                      │
    │ !:3*   !:3-$   │ tous les arguments d'index supérieur à 3                                               │
    │        !:3-    │ idem, sauf le dernier                                                                  │
    ├────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ !cat:*         │ tous les arguments de la dernière commande commençant par `cat`                        │
    └────────────────┴────────────────────────────────────────────────────────────────────────────────────────┘

    Dans la  plupart des exemples  précédents, on  peut remplacer `!`  par `!1` ou  n'importe quel
    désignateur d'évènement.


        ┌ ne pas écrire la sortie dans l'éditeur
        │ ┌ toutes les lignes de l'historique depuis la 1e
        │ │
    fc -l 1 | grep curl    zsh
    history | grep curl    bash

            Affiche les commandes `curl` au sein de l'historique, ainsi que leur index.
            Utile pour s'y référer ensuite dans un développement d'historique.  Ex:

                    !42:s/foo/bar

            Dans  zsh,  on  n'utilisera  pas  `history`,  car  il  s'agit  d'une
            abréviation  de `fc  -l`,  qui affiche  seulement  les 16  dernières
            lignes de l'historique.


    foo !1 !! bar

            Est  développé en  la  commande  `foo ...  bar`  avec  au milieu  la
            première et dernière commande de l'historique.
            Illustre qu'on  peut utiliser plusieurs  développements d'historique
            sur une  même ligne et  les faire précéder/suivre de  n'importe quel
            texte.


    ┌────────────────────────────────┬───────────────────────────────┐
    │ cp -R dir long_dirname         │                               │
    │ ...                            │                               │
    │ cd !cp:$                       │ se rendre dans `long_dirname` │
    ├────────────────────────────────┼───────────────────────────────┤
    │ cp file /path/to/long_filename │                               │
    │ ...                            │                               │
    │ vim !cp:$:t                    │ éditer `long_filename`        │
    └────────────────────────────────┴───────────────────────────────┘


    Modificateurs ne conservant dans un chemin que:

    ┌───┬────────────────────────────────────────────┐
    │ h │ head: tous les composants, sauf le dernier │
    ├───┼────────────────────────────────────────────┤
    │ t │ tail: le dernier                           │
    ├───┼────────────────────────────────────────────┤
    │ r │ root: tout sauf l'extension du fichier     │
    ├───┼────────────────────────────────────────────┤
    │ e │ extension: l'extension                     │
    └───┴────────────────────────────────────────────┘

            Exemples d'utilisation:

                    echo    /foo/bar.txt    /qux/norf.md

                    echo    !^:h    !$:t
                    /foo        norf.md˜

                    echo    !^:r    !$:e
                    /foo/bar    md˜


    echo foo\ bar baz

    !*:x    →    'foo\' 'bar' 'baz'
    !*:q    →    'foo\ bar baz'    OU    'foo\ bar' 'baz'
                 │                       │
                 │                       └ zsh
                 └ bash

            `x` et `q` sont des modificateurs ayant pour effet de quoter:

                    - chaque mot; les mots étant séparés par des espaces ou des newlines
                    - l'ensemble des arguments (bash) ou chaque argument (zsh)


                                     NOTE:

            Le modificateur `q` de zsh semble plus utile que son homologue bash.
            Entre `q`  bash, `q` zsh  et `x`,  c'est probablement `q`  zsh qu'on
            utilisera le plus souvent.


    !curl:p

            Affiche  la  dernière  commande   `curl`,  sans  l'exécuter,  et  la
            repositionne à la fin de l'historique.
            Pratique si  on doit  se référer  souvent à  elle dans  la prochaine
            commande, et  qu'on veut éviter  de devoir répéter `!curl`  à chaque
            fois; `!` suffira désormais.


    Modificateurs spécifiques à zsh:

    ┌───┬───────────────────────────────────────────────────────────────────┐
    │ a │ remplace un chemin relatif en absolu                              │
    ├───┼───────────────────────────────────────────────────────────────────┤
    │ A │ idem + résoud les symlinks                                        │
    ├───┼───────────────────────────────────────────────────────────────────┤
    │ c │ remplace un nom de commande par le chemin absolu vers son binaire │
    │   │                                                                   │
    │   │     !:0:c                                                         │
    ├───┼───────────────────────────────────────────────────────────────────┤
    │ l │ fait passer un mot en lowercase                                   │
    ├───┼───────────────────────────────────────────────────────────────────┤
    │ u │ idem en uppercase                                                 │
    ├───┼───────────────────────────────────────────────────────────────────┤
    │ Q │ retire un niveau de quoting                                       │
    └───┴───────────────────────────────────────────────────────────────────┘

    Réexécute la dernière commande en:

    ┌───────────────────┬────────────────────────────────────────────────────────────────────┐
    │ ^old              │ supprimant la 1e occurrence de `old`                               │
    ├───────────────────┼────────────────────────────────────────────────────────────────────┤
    │ ^old^new          │ remplaçant la 1e occurrence de `old` par `new`                     │
    ├───────────────────┼────────────────────────────────────────────────────────────────────┤
    │ r foo=bar baz=qux │ remplaçant la 1e occurrence de `foo` par `bar`, et `baz` par `qux` │
    └───────────────────┴────────────────────────────────────────────────────────────────────┘

            Les 2 premières syntaxes sont des abréviations de:

                    !!:s/old/new

            Elles fonctionnent peu importe le shell.

            En revanche, `r` est une commande intégrée à `zsh`.
            Contrairement à `^old^new` qui ne  peut remplacer qu'une chaîne, `r`
            peut en remplacer plusieurs simultanément.

            `r` est une abréviation de:

                    ┌ interagit avec certains évènements de l'historique
                    │ par défaut charge la dernière commande dans $EDITOR
                    │
                    fc -e -
                       ├──┘
                       └ aucun éditeur de texte n'est invoqué


    s/old/new/
    s/old/very_&/
    s//new/

            Modificateur remplaçant la 1e occurrence:

                    - de `old` par `new`

                    - de `old` par `very_old`

                    - du dernier pattern remplacé par `new`

                      S'il n'y a jamais eu de substitution (ou pas mémorisée tout du moins),
                      le shell utilisera la dernière chaîne recherchée via `!?string?`.

            Le dernier `/` est optionnel s'il est le dernier sur la ligne.

            Si `&` apparaît dans le champ de remplacement, il est développé en la chaîne à substituer.

            Si `old` ou `new` contiennent un slash, on peut l'échapper pour qu'il ne soit pas
            interprété comme un délimiteur, ou alors changer de délimiteur.


    &
    g

            Modificateur répétant la précédente substitution.
            "            demandant à la substitution de s'appliquer à toutes les occurrences sur la ligne.

            Exemples d'utilisation:

                    echo foo bar baz
                    foo bar baz˜


                    echo !*:s/b/c
                    foo car baz˜
                        ^
                    echo !*:gs/b/c
                    foo car caz˜
                        ^   ^
                    echo !*:g&
                    "˜

##
# Glossary
## event

A line selected from the history list during a history expansion.

## event designator

A reference to a command-line entry in the history list.

## word designator

A reference to some words in an event.
