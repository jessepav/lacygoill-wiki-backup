# Animes

        https://animetorrents.me/

# Audiobook

    https://www.youtube.com/watch?v=e8ah2L9-UCQ&t=180s

            The Name of the Wind (Kingkiller Chronicle #1) by Patrick Rothfuss Part 1

# Reddit

        https://www.reddit.com/r/Piracy/
        https://www.reddit.com/r/TPB/
        https://www.reddit.com/r/megalinks/
        https://www.reddit.com/r/trackers/

# Ebooks

To read:

https://www.reddit.com/r/Piracy/comments/7q856s/is_there_a_problem_with_library_genesis/
https://www.reddit.com/r/Scholar/comments/2raea8/libgen_down/
https://genofond.org/viewtopic.php?p=9000/
https://ebookee.org
https://www.reddit.com/r/Piracy/comments/60gbf7/library_genesis_broken/
https://www.reddit.com/r/Scholar/comments/3bs1rm/meta_the_libgenscihub_thread_howtos_updates_and/
https://www.reddit.com/r/antilibrary/comments/6ow6tq/antilibrary_faq/
https://www.reddit.com/r/Piracy/comments/3i9y7n/guide_for_finding_textbooks/
https://www.reddit.com/r/trackers/comments/hrgmv/tracker_with_pdfsebooks_of_college_textbooks/c1xrq44


    http://gen.lib.rus.ec/

            Cliquer sur le bouton EN en haut à droite pour faire passer la langue de russe à anglais.


    /server irc.irchighway.net
    /j #ebooks

            Pour + d'infos sur comment fonctionne ce channel:

                    http://ebooks.byethost6.com/index.html

            En gros, il suffit de taper `@search nom_d'un_livre`, pour recevoir une liste de résultats
            dans une archive .zip.
            Chercher une ligne contenant le nom exact du livre qui nous intéresse (ainsi que son auteur),
            et taper la commande qui lui est associée (commence par un bang).  Ex:

                    @search The Troop
                    … extrait archive zip …
                    !temerut Nick Cutter - The Troop (epub).rar


    /server irc.undernet.org
    /j #bookz


    https://cse.google.com/cse/publicurl?cx=011394183039475424659:5bfyqg89ers

            moteur de recherche google custom qui cherche dans une liste de sites prédéfinis,
            dont voici les adresses: http://pastebin.com/62tKNmm1



On peut également louer / acheter un livre sur amazon, faire sauter le DRM, et rendre le livre.
Faire sauter le DRM nécessite les programmes Calibre, DeDRM Tools (version modifiée?), KindleUnpack.

# Youtube-dl

    youtube-dl --help

            Affiche l'aide.


    -g    --get-url
    mpv $(youtube-dl -g 'url')

            Affiche l'URL où se trouve la vidéo.
            Streame la vidéo dont la page est présente à l'adresse url.


    --get-filename
    --restrict-filenames

            Affiche le nom du fichier s'il était téléchargé.
            Interdit l'usage de caractères non ASCII dans le nom du fichier.


    -x    --extract-audio

            Convertit les fichiers vidéos en fichiers audio.
            Nécessite `ffmpeg` ou `avconv`, et `ffprobe` ou `avprobe`.


    --audio-format mp3

            Sélectionne mp3 comme type de fichier audio en sortie.


    --write-sub
    --write-auto-sub
    --all-subs

            Écrire les sous-titres dans un fichier:

                    - ceux dont la langue a été sélectionnée par `--sub-lang`
                    - ceux générés automatiquement par YouTube
                    - tous les sous-titres dispo


    --list-subs
    --sub-lang fr,en

            Liste les langues pour lesquelles des sous-titres sont dispo.
            Sélectionne les langues françaises et anglaises pour les sous-titres à dl.


    --skip-download

            Ne dl pas la vidéo. Utile qd on veut récupérer uniquement les sous-titres.


    --playlist-items 1-3,7,10-13

            Dl les vidéos au sein d'une playlist, dont l'index est:

                    - compris entre 1 et 3
                    - 7
                    - compris entre 10 et 13

            Illustre que `playlist-items` accepte comme valeur à la fois des index absolus et des rangées.


    -o "%(autonumber)02d - %(title)s.%(ext)s"

            Template à utiliser pour les noms des fichiers vidéos.

            Exemple de résultat:

                    42 - My Wonderful Video.mp4
                    │    │                  │
                    │    │                  └ %(ext)s
                    │    └ %(title)s
                    └ %(autonumber)02d

            Dans un template, l'item `%(autonumber)0Nd` permet de numéroter les vidéos téléchargées,
            qd il y en a plusieurs (ex: playlist).
            Le chiffre `2` spécifie le nb de chiffres à utiliser.

            Si on pense qu'on va téléchargé entre 10 et 99 vidéos, il vaut mieux utiliser 2.
            Entre 100 et 999 vidéos, il faut utiliser 3.
            Etc.


    -F      --list-formats
    -f42    --format 42
    -f12+34

            Liste tous les formats dans lesquels la vidéo est dispo.

            Sélectionne le flux dont le code de format est 42.

            Sélectionne et multiplexe les flux dont les codes de format sont 12 et 34.

            Pour + d'infos, voir la section `FORMAT SELECTION` dans `man youtube-dl`.

##
# Issues
## tpb is unavailable.  What to do?

Try to visit the tor site:

        http://www.uj3wazyk5u4hnvtk.onion/

Then:

        $ cd ~/Downloads/tor/tor-browser_en-US/Browser/
        $ ./start-tor-browser

