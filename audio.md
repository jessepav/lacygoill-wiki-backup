# CAVA

`cava` est un pgm permettant de visualiser sous la forme d'une sorte d'histogramme dynamique.

## Installation

On peut installer le pgm en le compilant depuis la page github du projet.

    sudo aptitude install libfftw3-dev libasound2-dev libncursesw5-dev libpulse-dev libtool
    sudo aptitude install m4 autoconf automake
    ./autogen.sh
    ./configure
    make
    sudo checkinstall

            Procédure pour installer cava depuis le repo github:

                    https://github.com/karlstav/cava

            La 1e ligne est donnée par la page readme du projet.
            Elle installe des dépendances nécessaire à la compilation.
            Il se peut que les dépendances changent dans le futur qd cava sera mis à jour:

                    ⇒ ne pas copier cette ligne bêtement, relire le readme

            La 2e ligne installe des dépendances supplémentaires dont j'ai eu besoin lors de ma dernière
            compilation.

            Le binaire est installé dans `/usr/local/bin`.


                                     NOTE:

            Pendant l'installation via `checkinstall`, un message d'erreur apparaît:

                    *** Warning: The package version "0.4.2-17-geed0bca
                    0.4.2-17-geed0bca
                    0.4.2-17-geed0bca
                    0.4.2-17-geed0bca
                    0.4.2-17-geed0bca" is not a
                    *** Warning: debian policy compliant one. Please specify an alternate one

            Le pb vient du fait que le nom du paquet n'est pas conforme à une règle établie par Debian.
            Si on ne corrige pas ce pb, le binaire (paquet?) sera bien installé, mais le paquet ne sera
            pas manipulable via `dpkg`.

            Solution:

            Renommer le paquet en conservant le n° de version, mais en remplaçant ce qui suit par un suffixe
            conforme à la politique de Debian. Ex:

                    0.4.2-17-geed0bca    →    0.4.2-17+dfsg-0ubuntu5

            Le suffixe `+dfsg-0ubuntu5` a été trouvé en s'inspirant du nom du paquet `alsa-base`
            (paquet lui-aussi lié au son), via `aptitude show alsa-base`.


    sudo dpkg -L cava
    sudo dpkg -r cava

            Liste les fichiers au sein du paquet `cava`.
            Supprime le paquet `cava`.


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

            … ou lire la section pertinente au sein du readme du projet:

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
