# DESCRIPTION

Fast unix command-line interface to WWW

Surfraw is the acronym of:

        Shell Users' Revolutionary Front Rage Against the World Wide Web

It provides a fast unix command-line interface to  a variety of popular WWW search engines.

It abstracts the browser away from input. Doing so, lets it get on with what it's good at. Browsing.
Interpretation of linguistic forms  is handed back to the shell, which is  what it, and human beings
are good at. Homepage:

        http://surfraw.alioth.debian.org

# CONFIGURATION

Lien utile:

            http://surfraw.alioth.debian.org/#configuration


    sudo aptitude install surfraw

            installation du pgm


    ┌────────────────────────┬───────────────────────┐
    │ Ubuntu man page        │ project documentation │
    ├────────────────────────┼───────────────────────┤
    │ /etc/xdg/surfraw/conf  │ /etc/surfraw.conf     │
    │                        │                       │
    │ ~/.config/surfraw/conf │ $HOME/.surfraw.conf   │
    └────────────────────────┴───────────────────────┘

            Ces fichiers gèrent la configuration du pgm.
            Ubuntu (et Debian?) utilise des chemins de conf différents de ceux mentionnés par la
            documentation sur le site du projet.
            Je trouve que le choix d'Ubuntu / XDG est plus judicieux (centralisation des
            fichiers de conf de tous les pgm au sein de ~/.config/).

            Pour limiter nos réglages à notre compte utilisateur, utiliser les fichier du $HOME.
            S'ils n'existent pas, les créer en copiant les fichiers de conf système dans `/etc/`.


                                     NOTE:

            Attention, la syntaxe à utiliser dans le fichier de conf n'est pas la même suivant
            qu'on édite le fichier système, ou celui dédié à l'utilisateur.
            En effet au sein de `/etc/xdg/surfraw/conf`, on peut lire:

                    # WARNING: This file has a different format to that of $HOME/.surfraw.conf!
                    # $HOME/.surfraw.conf entries should always be written sh style:
                    #
                    # 	SURFRAW_text_browser=w3m
                    # etc

            Le fichier utilisateur semble devoir utiliser une syntaxe similaire à un script shell.


    ┌─────────────────────────────┬──────────────────────────┐
    │ Ubuntu man page             │ project documentation    │
    ├─────────────────────────────┼──────────────────────────┤
    │ /etc/xdg/surfraw/bookmarks  │ /etc/surfraw.bookmarks   │
    │                             │                          │
    │ ~/.config/surfraw/bookmarks │ $HOME/.surfraw.bookmarks │
    └─────────────────────────────┴──────────────────────────┘

            Ces fichiers mémorisent nos bookmarks.

            La syntaxe d'une ligne est la suivante:

                    keyword    url    # tag1 tag2 tag3 …

            En réalité, tout ce qui suit `url` est ignoré.
            On peut donc écrire du texte arbitraire qu'on utilisera comme s'il s'agissait de tags.
            Le dièse permettant de visuellement repérer où finit une url, et où commence les tags

            Les tags seront utiles qd on cherchera un bookmark via `fzf`.

            keyword ne doit pas contenir d'espace.


    ~/.config/surfraw/elvi/

            Dans ce dossier, on peut ajouter des fichiers dont le code shell implémente un nouvel elvi.
            Utile si la liste d'elvis supportés par défaut ne contient pas un moteur qui nous intéresse.

            Le nom du fichier a de l'importance, car c'est lui qu'il faudra passer en argument à
            `sr`/`surfraw` pour lui indiquer le moteur de recherche sur lequel chercher un mot-clé.


    SURFRAW_text_browser=google-chrome

            Choisir google-chrome comme le navigateur dans lequel ouvrir les liens.
            À écrire dans ~/.config/surfraw/conf.

            On pourrait aussi choisir 'www-browser' ou 'xdg-open' comme valeur.


    SURFRAW_text_browser=w3m
    SURFRAW_graphical=no

            Cette fois, on choisit un navigateur en TUI.

            D'autres variables d'environnement permettant de configurer `surfraw` existent.
            Consulter la section ’CONFIGURATION VARIABLES’ de la page man de `surfraw`.


    freak    http://torrentfreak.com/

            Définir 'freak' comme un mot-clé correspondant au site 'http://torrentfreak.com'.
            À écrire dans ~/.config/surfraw/bookmarks.


    cd ~/.config/surfraw/elvi/
    cp /usr/lib/surfraw/youtube my_custom_site
    chmod +x my_custom_site
    vim my_custom_site

            Par défaut, surfraw permet de chercher un mot-clé sur une liste prédéfinie de moteurs de
            recherche. Il se peut que le site qui nous intéresse ne soit pas dans cette liste.

            Dans ce cas, il faut créer un fichier dans `~/.config/surfraw/elvi/` contenant du code
            shell implémentant la recherche sur le site en question.

            Pour se simplifier la tâche, on peut commencer à travailler à partir d'une copie de
            `/usr/lib/surfraw/youtube` (trouvé via `dpkg -L surfraw | youtube$`).


                                     NOTE:

            Il faut adapter le code du fichier au site qui nous intéresse.

            En particulier, les lignes commençant par le mot-clé (fonction?) `w3_browse_url`.

                    w3_browse_url "http://www.youtube.com/"
                    w3_browse_url "http://www.youtube.com/results?search_query=${escaped_args}"

            Il faut changer l'url de base, et l'url d'une recherche qd on utilise le moteur du site.

# UTILISATION

    sr google arch linux
    surfraw google arch linux

            Cherche 'arch linux' sur google dans un navigateur en GUI (via `sr`) ou en TUI (via `surfraw`).


    sr -elvi
    sr Tab Tab

            Liste les moteurs de recherche supportés par défaut.
            La 2e méthode permet de sélectionner le moteur qu'on veut.


    sr -browser=google-chrome google kitten
    surfraw -browser=w3m google kitten

            L'argument `-browser` permet de configurer temporairement le navigateur à utiliser le temps
            d'une recherche.

            Couplé au fait que `sr` est un alias de `surfraw`, on peut utiliser 2 navigateurs
            différents (graphique/TUI) en créant nos propres alias:

                    alias sr='sr -browser=google-chrome'
                    alias surfraw='surfraw -browser=w3m'


    fzf-sr
    fzf-surfraw

            Fonctions custom permettant de fuzzy search nos bookmarks, et d'ouvrir un lien trouvé
            dans un navigateur en GUI (`fzf-sr`) ou en TUI (`fzf-surfraw`).
