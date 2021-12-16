# cava

`cava` est un pgm permettant de visualiser sous la forme d'une sorte d'histogramme dynamique.

## Installation

    $ sudo apt install libfftw3-dev libasound2-dev libncursesw5-dev libpulse-dev libtool
    $ sudo apt install m4 autoconf automake
    $ git clone https://github.com/karlstav/cava
    $ cd cava
    $ ./autogen.sh
    $ ./configure
    $ make
    $ sudo make install

## Configuration

    ~/.config/cava/config

            Fichier de conf.

            Le caractère de commentaire est `;`.
            Pour (dé)commenter une ligne, il faut donc enlever/ajouter un `;` à son début.

            Les 2 lignes les plus importantes sont celles définissant les variables `method` et `source`.
            Par défaut, je n'ai pas eu besoin de les modifier (mon serveur audio était alsa), mais gotbletu
            a du le faire lui (peut-être car il utilise pulse comme serveur audio).

            En cas de pb, voir la vidéo de gotbletu:

                    https://www.youtube.com/watch?v=ud_8Up2E_PE

            ... ou lire la section pertinente au sein du readme du projet:

                    https://github.com/karlstav/cava#from-alsa-loopback-device-tricky

            On peut aussi changer la couleur des barres par défaut via la variable `foreground`.


    Left    Right
    Down    Up

            Réduire / augmenter:

                    - la largeur des barres
                    - l'amplitude des barres (sensibilité de cava)

    c    b

            Changer la couleur des barres de façon interactive.

            Pour + d'infos sur les contrôles dispo:

                    https://github.com/karlstav/cava#controls


    r
    q

            Recharger le fichier de conf de cava:
            utile si l'animation reste figée après qu'on ait mis en pause l'unique pgm émettant du son.

            Quitter cava.
