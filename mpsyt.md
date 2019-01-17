Page du projet : https://github.com/mps-youtube/mps-youtube

Installer / Mettre à jour mps-youtube.
    sudo -H pip3 install [--upgrade] mps-youtube

    h | help                    Afficher l'aide.

    h <topic>                   Afficher l'aide de topic.

    /foo (vidéos)               chercher des vidéos / playlists à propos de foo
    //foo (playlists)

    <id de la vidéo> <CR>       Lancer la lecture d'une vidéo.

Contrôles pendant la lecture.
    Avancer / Reculer	    flèches directionnelles (hjkl ne fonctionne pas).
    pause			        space
    quitter			        q
    volume			        9 (diminuer), 0 (augmenter)

    1-5                     Lire les résultats 1 à 5, en boucle ou de façon aléatoire.
    repeat 1-5
    shuffle 1-5

    all                     Lire tous les résultats.

    n | p                   Naviguer dans les pages des résultats de recherche.

    h config                Voir les options de configuration disponibles.

    set                     Voir la configuration active.

    set show_video false        Configurer mpsyt pour qu'il ne télécharge que l'audio.

    set search_music true       Configurer mpsyt pour qu'il ne cherche que de la musique.

    set player mpv              Définir mpv comme lecteur par défaut.

    quit                        Quitter le pgm.

    h edit                      Commandes pour manipuler les résultats de recherche.

    h playlists                 Commandes pour gérer ses playlists.

    h tips                      Astuces
