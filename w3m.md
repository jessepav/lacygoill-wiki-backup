# CONFIGURATION

    ~/.w3m/keymap

            Fichier de conf dans lequel on peut (re)définir nos propres raccourcis.
            La syntaxe à utiliser est:

                    keymap <keys> FUNCTION

            Il semble que <keys> ne puisse contenir que 2 touches.
            On peut trouver le nom des fonctions utilisables dans le rhs via `g?`.

            Exemple de key binding:

                    keymap SPCt NEW_TAB  →  ouvrir un nouvel onglet via `SPC t`


    ~/.w3m/bookmark.html
    ~/.w3m/config
    ~/.w3m/cookie
    ~/.w3m/history

            Autres fichiers de configuration intéressants.


                                     NOTE:

            On peut rejeter les cookies d'un site en ajoutant son nom de domaine à l'option suivante:

                    Domains to reject cookies from

# INSTALLATION

    api w3m w3m-img w3m-el

            `w3m-img` permet d'afficher les images trouvées sur le web au sein d'un terminal compatible.
            `w3m-el` est optionnel. Il permet de surfer via w3m au sein d'un buffer Emacs:

                    simple Emacs interface of w3m
                    Emacs-w3m is an interface program of w3m, a pager with WWW capability.
                    It can be used as a lightweight WWW browser on emacsen.

# UTILISATION


extbrowser4 bash -c 'TS_SOCKET=/tmp/w3m tsp youtube-dl -c --restrict-filenames -x --audio-format mp3 -o "~/Music/%(title)s.%(ext)s" "$0" && notify-send -t 5000 -i audio-x-generic "Youtube-DL: Ripping Audio" "$0"'
extbrowser5 bash -c 'tsp mpv --ontop --no-border --force-window --autofit=500x280 --geometry=-15-50 "$0" && notify-send -t 5000 -i video-x-generic "MPV queue" "$0"'
extbrowser6 bash -c 'transmission-remote -a "$0" && notify-send -t 5000 -i emblem-downloads "Adding Torrent" "$0"'
extbrowser7 bash -c 'TS_SOCKET=/tmp/w3m tsp aria2c -j 1 -c -d ~/Downloads "$0" && notify-send -t 5000 -i package-x-generic "Aria2c: Downloading" "$0"'


Si on ne parvient pas à se connecter à un site via w3m, chercher une version mobile du site.
Généralement, une version mobile a moins de fonctionnalités, mais peut permettre de se connecter.
Suggestion de Gotbletu.


    w3m google.com

            Ouvre la page de recherche google dans w3m.


    img_w3m my_picture.jpg

            Affiche `my_picture.jpg` dans le terminal.

            `img_w3m()` est une fonction custom, définie dans `~/.shrc`.
            Par défaut, on n'en a pas besoin. `w3m` peut afficher une image tout seul:

                    w3m my_picture.jpg

            Toutefois, on a désactivé les images en donnant une valeur vide à l'option:

                    External command to display image

            Notre fonction `img_w3m()` rétablit temporairement cette option, le temps d'exécuter
            une commande.


         ┌─ with no other target defined, use the bookmark page for startup
         │
         │  ┌─ modify  one  configuration  item  with  an explicitly given value;
         │  │  without option=value, equivalent to `-show-option`
         │  │
    w3m -B -o display_link_number=1 > file

            Écrit les titres des liens présents dans nos bookmarks vers `file`, en incluant les liens
            eux-mêmes.


    w3m -cols 40 foo.html > foo.txt

            Convertit `foo.html` en `foo.txt` en spécifiant la longueur max des lignes sur la sortie.


         ┌─ explicit characterization of input data by MIME type
         │
    w3m -T text/html -I EUC-JP -O UTF-8 foo.html > foo.txt
                      │           │
                      │           └─ character encoding of output data
                      │
                      └─ character encoding of input data

            Conversion de `foo.html` en `foo.txt`, en spécifiant les encodages d'entrée (EUC-JP)
            et de sortie (UTF-8).


    Voici un certain nombres de raccourcis intéressants.
    Beaucoup sont customs: à l'origine les fonctions étaient associées à des touches peu intuitives.
    Malheureusement, certains sont encore peu intuitifs. Ils sont préfixés par le caractère `✘`.
    Leur trouver de meilleurs alternatives à l'occasion.


    ┌────────┬──────────────────────────────────────────────────────────────────────────────────────┐
    │ C-SPC  │ poser / retirer une marque à l'endroit où se trouve le curseur                       │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ C-a    │ donner le focus à la 1e / dernière entrée dans un popup menu                         │
    │ C-e    │                                                                                      │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ C-f    │ naviguer par pages au sein d'un popup menu                                           │
    │ C-b    │                                                                                      │
    │        │ on peut aussi naviguer en cherchant une regex via /, ?, n et N                       │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ C-g    │ afficher l'adresse de la ligne courante ainsi que le %age de la page lu              │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ C-o    │ charger un fichier html local                                                        │
    │        │                                                                                      │
    │        │ sur la ligne de commande de w3m (pex après avoir tapé `!`), `C-o` ouvre l'éditeur    │
    │        │ et permet d'écrire la commande au sein de Vim                                        │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ C-t    │ ouvrir le lien sous le curseur dans un nouvel onglet                                 │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ M-g    │ déplacer le curseur sur une ligne arbitraire                                         │
    │        │                                                                                      │
    │        │ on peut aussi utiliser une commande tq `42G`                                         │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ M-p    │ naviguer entre les marques posées via C-SPC                                          │
    │ M-n    │                                                                                      │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ M-u    │ charger une adresse relative                                                         │
    │        │                                                                                      │
    │        │ utile pour chercher un mot-clé sur le site courant                                   │
    │        │ pex, on est sur wikipedia, et on cherche vim :                                       │
    │        │                                                                                      │
    │        │         M-u                                                                          │
    │        │         C-u                                                                          │
    │        │         Vim                                                                          │
    │        │         CR                                                                           │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ Enter  │ - saisir du texte dans un champ                                                      │
    │        │ - cliquer sur un bouton                                                              │
    │        │ - suivre un lien                                                                     │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ [  ]   │ naviguer entre éléments interactfis                                                  │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ 42 )   │ se rendre sur le lien [42]                                                           │
    │ 42 (   │                                                                                      │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
 ✘  │ =      │ afficher les infos de la page courante                                               │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ !      │ exécuter une commande shell                                                          │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ a      │ mettre la page courante dans ses bookmarks                                           │
    │ '      │ charger un bookmark                                                                  │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ cw     │ toggle le wrapping autour de la fin de la page pendant une recherche                 │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ E      │ éditer la page courante dans un buffer Vim                                           │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ g?     │ affiche les raccourcis w3m                                                           │
    │ g!     │ affiche les messages d'erreurs                                                       │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gb     │ ouvrir le menu de sélection des buffers                                              │
    │        │                                                                                      │
    │        │ Il semble que w3m n'ait pas de fonction pour avancer dans l'historique d'un onglet.  │
    │        │ `gb` permet donc de contourner ce manque, mais uniquement tant que notre liste       │
    │        │ de buffers est courte.                                                               │
    │        │                                                                                      │
    │        │ `gb` permet aussi de supprimer un buffer, via `D`.                                   │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gc     │ inspecter l'url de la page courante                                                  │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gd     │ afficher le panneau listant les téléchargements effectués au cours de la session     │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gh     │ afficher l'historique des urls                                                       │
    │ gk     │ afficher les cookies                                                                 │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gl     │ ouvrir le menu de sélection des liens sur la page                                    │
    │        │                                                                                      │
    │        │ depuis ce menu, on peut déplacer le curseur à l'endroit où se trouve un lien au sein │
    │        │ de la page en:                                                                       │
    │        │                                                                                      │
    │        │         - tapant l'indice à 2 caractères qui le précède                              │
    │        │         - naviguant via `jk` puis Enter                                              │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gL     │ idem, mais cette fois, on ne se contente pas de se déplacer vers le lien choisi      │
    │        │ on le suit automatiquement                                                           │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gs     │ stopper le chargement des images                                                     │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gt     │ ouvrir le menu de sélection des onglets                                              │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gv     │ visualiser le code source derrière la page courante                                  │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gx     │ ouvrir la page courante dans le 1er ou 2e navigateur,                                │
    │ 2gx    │ ceux définis dans les options de w3m                                                 │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ gX     │ ouvrir le lien sous le curseur dans le navigateur externe                            │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
 ✘  │ i      │ afficher l'image sous le curseur dans `imagemagick`                                  │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ m,     │ déplacer les onglets                                                                 │
    │ m;     │                                                                                      │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ mu     │ marquer toutes les chaînes ressemblant à des url comme étant des ancres              │
    │        │                                                                                      │
    │        │ permet de s'y rendre via [, ] et de les suivre via Enter                             │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ mw     │ marquer le mot sous le curseur comme étant une ancre                                 │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ o      │ configurer les options                                                               │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ q  Q   │ quitter w3m avec/sans demande de confirmation                                        │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ R      │ recharger la page courante                                                           │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ s      │ sauvegarder la cible du lien sous le curseur                                         │
    │        │                                                                                      │
    │        │ Ça marche, mais pas sur tous les liens.                                              │
    │        │ Conseil: si w3m ne donne pas d'extension au fichier dans lequel télécharger          │
    │        │ le contenu de la cible (pdf, html, …), laisser tomber (C-g ou C-c).                  │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ S      │ sauvegarder l'image sous le curseur                                                  │
    │        │                                                                                      │
    │        │ pour voir les infos relatives à un fichier sauvegardé, utiliser `file` ou `identify` │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ C-s    │ sauvegarder la page courante dans un fichier                                         │
    │        │ uniquement le contenu, pas le code html                                              │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ u  C-r │ annuler le dernier mouvement / refaire un mouvement annulé                           │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ U      │ charger une url arbitraire                                                           │
    ├────────┼──────────────────────────────────────────────────────────────────────────────────────┤
    │ 3yy    │ copier l'url de la page courante                                                     │
    │        │                                                                                      │
    │        │ bidouille inspirée de : https://unix.stackexchange.com/a/12572/232487                │
    └────────┴──────────────────────────────────────────────────────────────────────────────────────┘


                                     NOTE:

            Si le navigateur ouvert par `gx` n'est pas celui qu'on veut, taper:

                    update-alternatives --get-selections | vipe
                    /browser

            Puis, configurer l'alternative qui pose pb. Pex:

                    sudo update-alternatives x-www-browser


                                     FIXME:

        Comment avancer dans l'historique d'un onglet ?
        J'ai tenté d'utiliser la fonction `NEXT` dont la description est “Move to next buffer“.
        Ça ne fonctionne pas. Aucun effet. Que fait `NEXT` ?


                                     FIXME:

        Comment scroller par demi-pages ?
        Les raccourcis suivants scrollent trop vite :

                keymap C-u PREV_PAGE
                keymap C-d NEXT_PAGE

        Les raccourcis suivants ne scrollent que d'une ligne :

                keymap C-u MOVE_UP
                keymap C-d MOVE_DOWN

        Les raccourcis suivants ne fonctionnent pas :

                keymap C-u 10MOVE_UP
                keymap C-d 10MOVE_DOWN

                keymap C-u 10 MOVE_UP
                keymap C-d 10 MOVE_DOWN

                keymap C-u MOVE_UP 10
                keymap C-d MOVE_DOWN 10

        … même après avoir activé l'option suivante:

                Enable vi-like numeric prefix        (*)YES  ( )NO

        J'ai cherché le mot-clé `count` dans le manuel :

                http://w3m.sourceforge.net/MANUAL

        … sans rien trouver d'utile. Comment passer un compte à une fonction pour la répéter ?


                                     FIXME:

        Comment désactiver des raccourcis ?

# VOCA

    buffer

            Page web chargée par w3m.
