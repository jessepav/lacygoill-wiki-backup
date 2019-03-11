# DMENU
## cli

    sudo aptitude install suckless-tools

            Installe le paquet “suckless-tools“ contenant entre autres le pgm `dmenu`.


    dmenu_run
    dmenu_run -b
    dmenu_run -l 10
    dmenu_run -fn Monospace-20:normal
    dmenu_run -nb '#FF0000'

            Affiche le lanceur dmenu:

                    - en haut de l'écran
                    - en bas  "
                    - en présentant les entrées du menu verticalement (sur 10 lignes max)
                    - avec la police d'écriture "Monospace" en taille 20 px.
                    - avec le fond en rouge


    dmenu_run
    thunar ~/Downloads

            Lance le pgm ’thunar’ et affiche le contenu du dossier ’~/Downloads’.

## key bindings

    C-a    C-e

            Positionne le curseur au début/à la fin du texte saisi.


    C-h    C-d

            Backspace / Delete


    C-m

            Return


    C-b    C-f

            Déplace le curseur vers la gauche / droite.
            Permet de se déplacer au sein du texte saisi, mais aussi de naviguer parmi les entrées
            proposées par dmenu.


    C-n    C-p
    M-j    M-k

            Haut / Bas
            Permet de naviguer parmi les entrées dmenu, entrée par entrée.

            Page up / down
            Permet de naviguer parmi les entrées dmenu, page par page.


                                     NOTE:

            dmenu peut s'afficher verticalement via le flag `-l lines`.


    C-i    Tab

            Développe le texte saisi.


    C-y
    C-S-y

            Au sein du champ de saisie, colle:

                    - la sélection X (le texte mis en surbrillance dans l'application ayant le focus)
                    - le presse-papier X


    C-u    C-k
    C-w

            Supprime:

                    - depuis le curseur jusqu'au début / à la fin de la ligne
                    - le mot à gauche du curseur
