##
# Todo

    https://github.com/muennich/urxvt-perls

            Extensions intéressantes.


    https://github.com/regnarg/urxvt-config-reload

            This plugin allows  you to reload urxvt configuration  at runtime by
            sending SIGHUP to the urxvt process.


    man urxvtperl

            To read to learn how to write urxvt extensions.

# Configuration

    urxvt --help 2>&1 | grep font | less
                 │
                 └── `urxvt` écrit son aide dans son flux d'erreur (au lieu du terminal)
                     donc, il faut rediriger le flux d'erreur vers le pipe

            Chercher tous les noms d'options en lien avec la police d'écriture.

            Cette commande est utile pour découvrir des options intéressantes,
            à propos d'un sujet donné.


    xrdb -query

            Affiche les ressources de la bdd du serveur X.


    ┌─ X server Resource DataBase utility
    │
    xrdb ~/.Xresources

            Commande à exécuter à chaque fois qu'on change le fichier de conf
            `~/.Xresources`, si on veut voir le résultat sans avoir à relancer X.

            Elle charge  des ressources dans  la bdd  de X, qui  s'appliquent à
            tous les programmes qui affichent qch via X.


                                     NOTE:

            Une commande similaire est exécutée automatiquement au démarrage,
            via un ou plusieurs fichiers systèmes:

                    ag xrdb /etc/

            Atm, le seul fichier qui semble exécuter automatiquement `xrdb` sur
            ma machine est:

                    /etc/xdg/xfce4/xinitrc

            Il ajoute plusieurs fichiers  à `$XRESOURCES`, puis exécute `xrdb`
            sur l'ensemble:

                    cat /dev/null $XRESOURCES | xrdb -merge -


                                     TODO:

            Si  on utilise  des commentaires  commençant par  `!`, et  que l'un
            d'eux  contient  un  single  quote:

                    !  it's  a  comment

            … le préprocesseur C utilisé par `xrdb` se plaint.
            Pour + d'infos, lire notre alias `reload_xres` défini dans `~/.shrc`.

            Actuellement,   notre   `~/.Xresources`   contient   ce   genre   de
            commentaires.   Notre alias  custom évite  le problème  lors d'une
            utilisation interactive de `xrdb`.
            Mais quid du démarrage de la session X: y'a-t-il un risque de bugs louches?

            Peut-être que  les avertissements du préprocesseur  C n'ont aucune
            influence sur ce que `xrdb` exécute.

# Copier-coller

    simple ou double-clic gauche  >  shift + clic gauche

            On peut sélectionner une région de  texte via la souris en faisant
            un simple/double clic gauche sur son  1er mot, puis en répétant le
            même raccourci + shift sur son dernier.

            Fonctionne aussi via des triples clic pour sélectionner une région
            linewise.

            Dans tmux, il faut désactiver l'option 'mouse':

                    pfx m  ⇔  set-option -g mouse off


    middle clic souris

            En  appuyant  sur  la  molette  de la  souris,  on  colle  le  texte
            actuellement sélectionné après le curseur.

            La position du curseur n'est pas modifié par la sélection.

# Documentation

                      http://cvs.schmorp.de/rxvt-unicode/doc/rxvt.7.pod
    http://pod.tst.eu/http://cvs.schmorp.de/rxvt-unicode/doc/rxvt.7.pod

    Gentoo:   https://wiki.gentoo.org/wiki/Rxvt-unicode
    ArchWiki: https://wiki.archlinux.org/index.php/rxvt-unicode
    IRC:      irc.freenode.net #rxvt-unicode
    Tuto:     http://artisan.karma-lab.net/installer-et-parametrer-urxvt

# Installation

    sudo aptitude install rxvt-unicode-256color

# Utilisation

    ctrl + clic droit    les 2 maintenus enfoncés

            Ouvre un menu contextuel.
            Dans la plupart des émulateurs, un simple clic droit suffit.

            Ce menu permet, entre autres, de copier la sélection vers le presse-papier système,
            ou d'évaluer une expression perl.


    ctrl + clic molette    les 2 maintenus enfoncés

            Affiche les options dispo. Celles activées sont préfixées par un astérisque.
            On peut toggle l'état d'une option, en déplaçant la souris (tout en maintenant ctrl+clic molette),
            pour sélectionner une option, puis en relâchant la molette.

# Voca

    root window

            La fenêtre du fond d'écran (d'après le livre `From bash to zsh`).
