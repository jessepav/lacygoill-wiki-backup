
Fasd  est un  outil en  cli visant  à augmenter  la productivité.  Il offre  un accès  rapide aux
fichiers / dossiers, en mémorisant ceux auxquels on accède régulièrement.

Quand on ne tape que quelques caractères d'un fichier/dossier/chemin, il essaie de deviner ce qu'on
souhaite, en  s'appuyant sur  une liste  (~/.fasd) d'éléments  triés par  "frecency" :  mix entre
frequency / fréquence et recency / date de dernier accès ; https://en.wikipedia.org/wiki/Frecency

Le  nom fasd  vient  des alias  fournis par  défaut  : f  (fichiers),  a (fichiers  / dossiers),  s
(show/search/select), d (dossiers).

Lire aussi:

    https://github.com/ranger/ranger/wiki/Integration-with-other-programs#fasd

            Décrit 'linstallation d'un plugin, permettant à fasd de mémoriser les fichier qu'on ouvre
            depuis ranger. Sans ce plugin, fasd ne nous proposerait jamais un fichier ouvert depuis
            ranger.


    https://github.com/ranger/ranger/wiki/Commands#visit-frequently-used-directories

            Décrit l'installation d'une commande custom permettant de se rendre vers un dossier
            récent via fasd. Commande à associer à une touche du clavier ?

# INSTALLATION

    git clone https://github.com/clvv/fasd
    sudo checkinstall

# UTILISATION

    ┌────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
    │ f                  │ lister les fichiers OU les dossiers frécents (fréquents + récents)           │
    │ d                  │ f, a et d sont des alias prédéfinis (f = fasd -f, a = fasd -a, d = fasd -d)  │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ a Do lo            │ lister les fichiers ET les dossiers frécents dont le nom matche `Do` et `lo` │
    │                    │                                                                              │
    │                    │ `Do` et `lo` doivent être présents dans le nom du fichier ou du dossier      │
    │                    │ pas ailleurs dans un autre composant de leur chemin                          │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ f foo              │ lister les fichiers frécents dont le nom matche foo                          │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ f js$              │ lister les fichiers récents dont le nom se terminent par js                  │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ z foo              │ se rendre dans le dossier dont le nom matche matche foo                      │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ v foo              │ ouvrir avec vim le fichier le + frécent qui matche foo                       │
    │ f -e vim foo       │                                                                              │
    │                    │                                                                              │
    │ m foo              │ ouvrir avec mpv le fichier le + frécent qui matche foo                       │
    │ f -e mpv foo       │                                                                              │
    │                    │                                                                              │
    │ o foo              │ ouvrir avec le programme associé par défaut le fichier / dossier             │
    │ a -e xdg-open foo  │ le + frécent qui match foo                                                   │
    │                    │                                                                              │
    │ xdg-open $(sf foo) │ afficher les fichiers frécents qui match foo via un menu interactif,         │
    │                    │ puis ouvrir le fichier sélectionné                                           │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ ,foo,bar Tab       │ auto-compléter le fichier ou dossier le + frécent qui contient foo et bar    │
    │                    │ dans son nom                                                                 │
    │                    │                                                                              │
    │ f,foo,bar Tab      │ idem mais spécifiquement pour un fichier                                     │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ d,foo Tab          │ auto-compléter le dossier le + frécent contenant foo dans son chemin         │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ zz                 │ afficher un menu listant les dossiers les + frécents pour en sélectionner un │
    │                    │ et s'y rendre                                                                │
    └────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

                                     TODO:

Il semble que la syntaxe `,foo Tab`, ait un effet similaire à la fonction `fasd-complete-f`
(installée par zsh). Par défaut, cette dernière est associée à `c-x c-f`.


                                     FIXME:

En réalité,  dans les  syntaxes du tableau  précédent, il  semble que `foo`  et `bar`  n'ont pas
besoin d'être présents dans le nom du  fichier/dossier de façon exacte: leurs caractères peuvent
être séparés par 2 caractères (configurable via `$_FASD_FUZZY`).
Revoir le tableau pour tenir compte de l'aspect fuzzy du match.
