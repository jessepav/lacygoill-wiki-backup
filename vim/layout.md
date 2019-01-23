# Vocabulaire

Vim permet d'organiser son travail via 3 niveaux d'abstraction:

    1. buffers
    2. fenêtres
    3. onglets

Un buffer correspond à peu près à un fichier.

Une fenêtre n'est  qu'un espace de l'écran permettant de  visualiser un buffer :
fermer  une fenêtre  n'implique donc  pas de  fermer un  buffer, on  peut ouvrir
plusieurs fenêtre offrant des vues différentes sur un même fichier.

Les fenêtres sont  utiles pour comparer plusieurs fichier d'un  seul coup d'oeil
ou pouvoir lire un fichier (documentation) tout en écrivant dans un autre.

En revanche, gérer tous ses buffers en les affichant dans une fenêtre dédiée est
souvent pénible voire impossible, car on  est limité par l'espace offert par son
écran pour afficher tous ses buffers.

Un  onglet correspond  à un  espace de  travail (bureau  virtuel) permettant  de
regrouper plusieurs fenêtres ensembles, pex autour d'un projet commun.

Un  onglet peut  s'avérer utile  qd on  veut éditer  rapidement un  fichier sans
modifier la disposition des fenêtres de l'onglet courant.

En revanche, gérer tous  ses fichiers en les affichant dans  un onglet dédié est
une stratégie sous-optimale.

Pk?

Car la barre des titres des onglets  (tabline) ne permet pas d'afficher les noms
des fichiers  dans leur intégralité  qd ils sont  trop longs ou  qd il y  a trop
d'onglets.

Il est donc souvent impossible de trouver l'onglet qui nous intéresse réellement
du 1er  coup et il faut  donc se résigner à  passer en revue (cycling)  tous ses
onglets via des mappings (gt / gT).

# Fenêtres

    Ouvrir le fichier dont le chemin est sous le curseur dans:
    ┌──────────────────┬──────────────────────────────────────────────────────────────────────────────────┐
    │ gf               │ le viewport courant                                                              │
    ├──────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ C-w f            │ un viewport horizontal                                                           │
    ├──────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ C-w f C-w L      │ un viewport vertical, en maximisant sa hauteur                                   │
    │                  │                                                                                  │
    │ :winc f | winc L │                                                                                  │
    ├──────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ C-w v gf         │ un viewport vertical, en donnant la même hauteur au viewport vertical qu'au      │
    │                  │ viewport courant, ce faisant il respecte les viewports au-dessus/en-dessous      │
    │ :vert winc f     │                                                                                  │
    │                  │ NOTE: il semble que `:vert` transforme l'argument `f` en le pseudo-argument      │
    │                  │       `v gf` (pseudo, car invalide pour `:wincmd`)                               │
    ├──────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ C-w gf           │ un onglet                                                                        │
    ├──────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ C-w gF           │ un onglet, et placer le curseur sur le n° de ligne qui suivait le nom du fichier │
    │                  │                                                                                  │
    │                  │ Ex:                                                                              │
    │                  │     ~/.bashrc:12                                                                 │
    │                  │     ~/.zshrc  34                                                                 │
    └──────────────────┴──────────────────────────────────────────────────────────────────────────────────┘

    Ouvrir le tag sous le curseur dans:
    ┌───────┬──────────────────────┐
    │ C-w } │ la fenêtre preview   │
    │       │                      │
    │ C-w ] │ une nouvelle fenêtre │
    └───────┴──────────────────────┘


    Fermeture:
    ┌────────────┬─────────────────────────────────────────────────────────────────────────────┐
    │ C-w o      │ fermer toutes les fenêtres sauf celle ayant le focus                        │
    │ :on[ly]    │                                                                             │
    │            │                                                                             │
    │ :tabo[nly] │ fermer tous les onglets sauf l'onglet courant                               │
    ├────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ 3 C-w c    │ fermer la 3e fenêtre                                                        │
    │ :3close    │                                                                             │
    │            │ contrairement à `:quit`:                                                    │
    │            │                                                                             │
    │            │ :close ne ferme pas la fenêtre courante s'il s'agit de la dernière restante │
    │            │ :close ne déclenche pas l'évènement QuitPre                                 │
    ├────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ :+2q       │ fermer la 2e prochaine fenêtre                                              │
    │ :$q        │ fermer la dernière fenêtre                                                  │
    ├────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w q      │ quitter la fenêtre courante                                                 │
    │ :q         │                                                                             │
    ├────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w z      │ fermer la fenêtre preview peu importe où on est                             │
    │ :pc[lose]  │                                                                             │
    └────────────┴─────────────────────────────────────────────────────────────────────────────┘

    Split:
    ┌───────┬────────────────────────────────────────────────┐
    │ C-w s │ diviser la fenêtre horizontalement             │
    │       │                                                │
    │       │ équivaut à:  :split                            │
    ├───────┼────────────────────────────────────────────────┤
    │ C-w v │ diviser la fenêtre verticalement               │
    │       │                                                │
    │       │ équivaut à:  :vsplit                           │
    ├───────┼────────────────────────────────────────────────┤
    │ C-w n │ ouvre une fenêtre et y édite un nouveau buffer │
    │       │                                                │
    │       │ équivaut à:  :split | enew  ou  :new           │
    └───────┴────────────────────────────────────────────────┘

    Rotation:
    ┌─────────┬───────────────────────────────────────────────────────────────────────────────┐
    │ C-w r R │ rotation des fenêtres dans un sens ou dans un autre                           │
    │         │                                                                               │
    │ C-w x   │ échanger la position de la fenêtre courante avec celle de droite / du dessous │
    └─────────┴───────────────────────────────────────────────────────────────────────────────┘

    La rotation des fenêtres via `C-w r`  ou `C-w R` ne peut être qu'horizontale
    ou verticale, pas circulaire.

    IOW,  ne fonctionne  que si  on  se trouve  dans une  fenêtre appartenant  à
    un  ensemble  de fenêtres  alignées  horizontalement,  aucune n'étant  split
    horizontalement (:sp).

    Ou à  un ensemble de  fenêtres alignées verticalement, aucune  n'étant split
    verticalement (:vs).


    Redimensionnement:
    ┌───────────────┬─────────────────────────────────────────────────────────────────────────────┐
    │ C-w 5+-       │ augmenter / réduire la hauteur de la fenêtre de 5 lignes                    │
    │               │                                                                             │
    │               │ équivaut à:  :res -+5                                                       │
    ├───────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w 5><       │ augmenter / réduire la largeur de la fenêtre de 5 colonnes                  │
    │               │                                                                             │
    │               │ équivaut à:  :vert res -+5                                                  │
    ├───────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w 5_        │ redimensionner la fenêtre à 5 lignes de hauteur                             │
    │               │                                                                             │
    │               │ équivaut à:  :res 5                                                         │
    ├───────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w 5|        │ redimensionner la fenêtre à 5 colonnes de largeur                           │
    │               │                                                                             │
    │               │ équivaut à:  :vert res 5                                                    │
    ├───────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w _         │ maximiser la hauteur de la fenêtre                                          │
    │ C-w 1_        │ minimiser la hauteur de la fenêtre                                          │
    ├───────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w |         │ maximiser la largeur de la fenêtre                                          │
    │ C-w 1|        │ minimiser la largeur de la fenêtre                                          │
    ├───────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w =         │ égaliser les dimensions des fenêtres                                        │
    ├───────────────┼─────────────────────────────────────────────────────────────────────────────┤
    │ C-w H J K L   │ déplacer la fenêtre courante pour qu'elle s'étende sur tout le côté gauche, │
    │               │ bas, haut, droit                                                            │
    │               │                                                                             │
    │               │ équivaut à:  :wincmd H  :wincmd J  …                                        │
    └───────────────┴─────────────────────────────────────────────────────────────────────────────┘


    Focus:
    ┌───────────────────┬──────────────────────────────────────────────────────────────────────┐
    │ C-w j             │ déplace le focus d'une fenêtre vers le bas                           │
    │ :wincmd j         │                                                                      │
    ├───────────────────┼──────────────────────────────────────────────────────────────────────┤
    │ :3wincmd w        │ donne le focus à la fenêtre n° 3                                     │
    │                   │                                                                      │
    │                   │ Plus généralement, la syntaxe de `:wincmd` est la suivante:          │
    │                   │                                                                      │
    │                   │     :[N]wincmd {arg}                                                 │
    │                   │                                                                      │
    │                   │ Elle équivaut à:                                                     │
    │                   │                                                                      │
    │                   │     C-w [N] {arg}                                                    │
    ├───────────────────┼──────────────────────────────────────────────────────────────────────┤
    │ C-w p             │ alterner le focus entre les 2 dernières fenêtres (previous)          │
    ├───────────────────┼──────────────────────────────────────────────────────────────────────┤
    │ C-w P             │ donner le focus à la fenêtre preview                                 │
    ├───────────────────┼──────────────────────────────────────────────────────────────────────┤
    │ C-w b             │ donner le focus à la fenêtre tout en bas ou tout à droite            │
    │ C-w t             │ "                                    haut ou tout à gauche           │
    │                   │                                                                      │
    │                   │ Si Vim a le choix entre plusieurs fenêtres, la fenêtre qui recevra   │
    │                   │ le focus est celle qui contiendra la colonne/ligne dans laquelle     │
    │                   │ se trouve le curseur.                                                │
    │                   │                                                                      │
    │                   │ mnémotechnique: botright                                             │
    │                   │                 topleft                                              │
    ├───────────────────┼──────────────────────────────────────────────────────────────────────┤
    │ C-w C-w           │ alterner le focus entre les 2 dernières fenêtres visitées            │
    └───────────────────┴──────────────────────────────────────────────────────────────────────┘


    SPC wh

            fixer ponctuellement la hauteur d'une fenêtre et outrepasser le réglage
            winheight=999 (mode rolodex)


    C-w CR

            Depuis la fenêtre qfl, ouvrir l'entrée sous le curseur dans un viewport.


    :bd

            décharger le buffer, le supprimer de la liste des buffers
            et fermer toutes les fenêtres où il est affiché


    :all [N]    :ball [N]

            Afficher chaque buffer de l'arglist ou de la bufferlist dans une fenêtre horizontale distincte.


                                               NOTE:

            À la place de fenêtres horizontales, on peut demander à afficher les buffers dans des
            fenêtres verticales ou des onglets, en préfixant les commandes avec le modificateur
            :vert ou :tab. Ex:

                    :vert all    buffers de l'arglist dans des fenêtres verticales
                    :tab ball    buffers de la buffer list dans des onglets


                                               NOTE:

            Les nouvelles fenêtres remplacent les anciennes, elles ne s'y ajoutent pas.
            Idem pour les onglets.


                                               NOTE:

            Le nb de fenêtres / onglets pouvant être ouverts est limité par N et par:

                    - 'winheight'     pour des fenêtres horizontales
                    - 'winwidth'      "                 verticales (:vert)
                    - 'tabpagemax'    "        onglets (:tab)

            Par défaut, 'winheight' vaut 1, 'winwidth' 20 et 'tabpagemax' 10.


                                               NOTE:

            :tab est un modificateur de commande similaire à :vert.

            Lorsque la commande qui le suit ouvre une nouvelle fenêtre, :tab lui
            demande de le faire dans un nouvel onglet.


    :lcd

            changer le répertoire de travail de la fenêtre courante
            :cd affecte toutes les fenêtres globalement

            Quand on  divise une  fenêtre, la nouvelle  hérite du  répertoire de
            travail de l'ancienne.

            Cela implique  que la  commande :lcd  est très  utile pour  avoir un
            répertoire de travail distinct par onglet ouvert.


    :windo cmd

            exécute cmd dans toutes les fenêtres de l'onglet courant


    :set scrollbind

            une fois tapé dans 2 fenêtres adjacentes, scroller l'une fera scroller
            l'autre ('scrollbind' = 'scb')

# Modificateurs :vert / :tab

Qd on crée  un viewport horizontal via  :sp ou :new, par défaut  il s'affiche en
haut.

Qd on  crée un viewport  vertical via  :vs ou :vnew,  par défaut il  s'affiche à
gauche.

On  peut changer  ces  positions par  défaut en  activant  les options  globales
'splitbelow' et/ou 'splitright'.

On peut également changer ces  positions temporairement, le temps d'exécuter une
commande créant un viewport, via certains modificateurs de commande:

    - :abo[veleft], :lefta[bove]
    - :bel[owright], :rightb[elow]
    - :to[pleft]
    - :bo[tright]
    - :vert[ical]
    - :tab

Qd  :abo/:lefta est  suivi d'une  commande  Ex qui  split horizontalement,  elle
demande à cette dernière de le créer en haut.

Et qd elle est suivie d'une commande  Ex qui split verticalement, elle demande à
cette dernière de le créer à gauche.

On peut utiliser :abo ou :lefta indifféremment, toutefois il paraît plus logique
d'écrire :abo devant une commande Ex splittant horizontalement, et :lefta devant
une commande Ex splittant verticalement.

Mêmes remarques pour :bel et :rightb.

:to est similaire à :abo à ceci près qu'elle demande à créer le nouveau viewport
TOUT en haut ou TOUT à gauche.

:abo demande à ce  que le nouveau viewport soit créé JUSTE  au-dessus ou JUSTE à
gauche de la fenêtre courante.

Même remarque pour :bo.

:vert demande à la commande Ex qui  suit de créer son split verticalement et non
pas horizontalement.
Utile pour :sb car il n'existe pas de commande :vsb.
On peut donc l'utiliser comme ceci:

        :vert sb



Voici 8 commandes qui créent un viewport et qui n'utilisent pas 'switchbuf'/'swb'.
Pk 8? Chacune illustre l'utilisation d'un modificateur différent:

    4 directions relatives (haut, bas, gauche, droite)  à la fenêtre courante
    4 directions absolues  (tout en haut, tout en bas, …)

    Créer un viewport:
    ┌──────────────┬────────────────────────────────────────────────────────────────────┐
    │ :abo sp      │ horizontal  en haut                                                │
    ├──────────────┼────────────────────────────────────────────────────────────────────┤
    │ :lefta vs    │ vertical    à gauche                                               │
    ├──────────────┼────────────────────────────────────────────────────────────────────┤
    │ :bel new     │ horizontal  en bas         en chargeant un nouveau buffer sans nom │
    ├──────────────┼────────────────────────────────────────────────────────────────────┤
    │ :rightb vnew │ vertical    à droite       "                                       │
    ├──────────────┼────────────────────────────────────────────────────────────────────┤
    │ :to sp       │ horizontal  tout en haut                                           │
    ├──────────────┼────────────────────────────────────────────────────────────────────┤
    │ :to vs       │ vertical    tout à gauche                                          │
    ├──────────────┼────────────────────────────────────────────────────────────────────┤
    │ :bo new      │ horizontal  tout en bas    en chargeant un nouveau buffer sans nom │
    ├──────────────┼────────────────────────────────────────────────────────────────────┤
    │ :bo vnew     │ vertical    tout à droite  "                                       │
    └──────────────┴────────────────────────────────────────────────────────────────────┘


Voici 10 commandes qui créent un viewport et qui utilisent 'swb'.
Pk 10? Chacune illustre l'utilisation d'un modificateur différent:

    les 2 premières sont similaires à :sp et :vs sans modificateurs
    les 4 suivantes "                            avec modificateurs relatifs (:abo, rightb, :bel, :lefta)
    les 4 dernières "                            avec modificateurs absolus (:to, :bo)

    :sb foo    :sb[uffer] 42

            crée un viewport horizontal et y afficher le buffer n°42 ou le buffer `foo`
            en utilisant l'option 'swb'

            Tout comme :sp, en l'absence de modificateurs de position, :sb positionne le viewport
            en respectant l'option 'splitbelow'.

            Les différences entre :sb et :sp sont les suivantes:

                - :sp dispose d'un homologue en mode vertical (:vsp), pas :sb
                  Il n'existe pas de commande :vsb, il faut écrire:    :vert sb

                - si le buffer est déjà affiché dans une fenêtre / onglet, :sb lui donne le focus au lieu
                  d'ouvrir “bêtement“ une 2e fenêtre (pour peu qu'on ait bien configuré l'option 'swb')

                - :sb accepte un n° de buffer en argument, pas :sp
                  :sp 42 n'ouvrirait pas le buffer listé de numéro 42, mais un nouveau buffer dont le nom serait 42

    :vert sb foo    :vert sb 42

            crée un viewport vertical et y affiche le buffer n°42 ou le buffer `foo` en utilisant l'option 'swb'

            Tout comme :vs, en l'absence de modificateur de position, :vert sb positionne le viewport
            en respectant l'option 'splitright'.

    :abo            sb foo
    :lefta  vert    sb foo
    :bel            sb 42
    :rightb vert    sb 42

            crée un viewport en haut, à gauche, en bas, à droite
            et y affiche le buffer foo ou 42 en utilisant l'option 'swb'

    :to          sb foo
    :to vert     sb foo
    :bo          sb 42
    :bo vert     sb 42

            crée un viewport tout en haut, tout à gauche, tout en bas, tout à droite
            et y affiche le buffer foo ou 42 en utilisant l'option 'swb'

    :tab split

            affiche (!=déplace) le buffer courant dans un nouvel onglet

            Équivalent de <prefix>! pour tmux,
            à ceci près que la fenêtre où s'affiche le buffer à l'origine reste ouverte.

            Utile pour simuler un zoom sur un viewport particulier sans foutre en l'air
            le layout de notre onglet.

                                               NOTE:

            :tabedit % équivaut à créer un onglet et à y charger le buffer courant:

                    :tabnew + :edit {current file}

            Comportement indésirable si le buffer contient des modifications non sauvegardées.
            :tab split est donc peut-être plus indiqué.

    :tab help uganda

            afficher l'aide à propos du tag uganda dans un nouvel onglet

            Plus généralement, qd on fait suivre :tab de n'importe quelle commande qui
            ouvre une nouvelle fenêtre, c'est un nouvel onglet qui est ouvert à la place.
            :tab est une commande voisine de :vertical.

            En cas de conflit (:tab + :vert), :tab a la priorité.

# Onglets

    :tabnext        gt
    :tabprevious    gT

            avancer / reculer d'un onglet

    5gt    :tabnext 5

            se rendre au 5e onglet

    :3tabnew

            ouvrir un nouvel onglet après le 3e

    :tabclose  ,ct

            fermer l'onglet courant (et toutes les fenêtres qu'il contient)

    :tabedit foo

            afficher le fichier foo dans un nouvel onglet
            :tabedit n'accepte qu'un seul nom de fichier en argument

    :Tabedit foo bar baz

            afficher les fichier foo, bar et baz chacun dans un onglet dédié
            :Tabedit est une commande perso

    C-w T

            déplacer la fenêtre courante dans un onglet dédié (où elle sera seule)

    :tabfirst    :tablast

            se rendre au premier / dernier onglet

    :tabmove

            déplacer l'onglet courant en dernier

    :tabmove 0

            déplacer l'onglet courant en premier

    :tabmove 5

            déplacer l'onglet courant après le 5e

    :tabs

            afficher la liste des noms d'onglets ouverts, et pour chacun d'eux les noms des buffers
            qu'ils affichent dans des fenêtres

# Vimdiff

    vim -d[R] foo bar baz

            Compare et affiche les différences entre les fichiers foo, bar et baz (-R = mode read-only).


    vim -d <(ls dir1) <(ls dir2)

            Compare le contenu des dossiers `dir1` et `dir2`.


                                               NOTE:

            Cette commande est très utile qd on apprend une nouvelle commande / programme, et qu'on
            cherche à comprendre l'influence d'une ou plusieurs options:

                    vim -d  <(new_cmd --option=foo)   <(new_cmd --option=bar)   <(new_cmd --option=baz)

                    vim -d  <(awk -f prog1 data.txt)  <(awk -f prog2 data.txt)  <(awk -f prog3 data.txt)


    :diffget    :diffput

            Modifie le buffer courant / l'autre buffer pour défaire les différences.

                                               FIXME:

            À compléter ([range], [bufspec], commandes normales do, dp)


    :set diffopt+=iwhite

            Ignorer une différence lorsqu'il s'agit de trailing whitespace.


    :diffthis    [od
    :diffoff     ]od

            Ajoute / Retire la fenêtre courante à la liste des fenêtres à comparer.
            (Dés)Active l'option locale à la fenêtre 'diff' (booléen).


    :windo diffthis
    :windo diffoff    :diffoff!

            Ajoute / Retire toutes les fenêtres de l'onglet courant à / de la liste des fenêtres à comparer.


    :tab split | vs foo | windo diffthis

            1. ouvre un nouvel onglet affichant le buffer courant

            2. ouvre un viewport vertical affichant le buffer foo

            3. compare les 2 buffers


    :diffupdate[!]

            Mettre à jour la comparaison entre les buffers.
            Parfois nécessaire après avoir modifié l'un d'eux depuis Vim.

            Le bang demande à Vim de recharger les buffers à partir des fichiers d'origine ;
            nécessaire après avoir modifié l'un deux depuis un pgm externe.


    cod

            Toggle l'option 'diff' de la fenêtre (ajoute / supprime de la liste des fenêtres à comparer).


    ]c    [c

            Naviguer entre les différences.

