# moreutils

    $ pipeline | sponge file

            écrire la sortie de pipeline dans file

            Quelle différence avec `tee`?

            `tee` écrit son entrée standard sur sa sortie standard et dans `file`.
            `sponge` écrit uniquement dans `file`.
            De plus, `tee` écrit dans `file` octet par octet, tandis que `sponge` n'écrit dans `file`
            qu'après avoir reçu toute la sortie de `pipeline`.

            Ni `sponge`, ni `tee` n'écrivent les erreurs.


    $ vidir [-v]

            affiche le contenu du dossier de travail dans son éditeur par défaut

            `vidir` permet de:

                    * échanger les noms de 2 éléments (en échangeant leurs n°)

                    * supprimer un élément (en supprimant la ligne où son nom apparaît)

                    * changer le nom d'un fichier / dossier en l'éditant directement.
                      -v permet d'afficher le détail des changements de noms opérés, une fois qu'on
                      quitte vidir.

                    * charger un fichier / dossier via `gf` si on utilise Vim comme éditeur
                      Si on charge un dossier avec Vim, l'explorateur par défaut prend alors le relai
                      (buffer netrw, dirvish, …).
                      Atm, on utilise dirvish, et on peut naviguer dans l'arborescence de fichiers
                      via `h` et `l`.


    $ vidir *.jpeg

            liste les images jpeg du dossier de travail dans notre éditeur


    $ find -type f | vidir -

            liste tous les fichiers présents dans le dossier de travail ou l'un de ses sous-dossiers


    $ pipeline | vipe

            lire la sortie de pipeline dans un buffer de son éditeur

# VimFx

        https://addons.mozilla.org/en-US/firefox/addon/vimfx/
        https://addons.mozilla.org/en-US/firefox/addon/the-fox-only-better/ (hide/customize address bar)

