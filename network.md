# Links

    Basic Security Testing with Kali Linux 2

            https://www.amazon.com/Basic-Security-Testing-Kali-Linux/dp/1530506565/

                    380    pages
                    71     reviews
                    4.5/5  stars

            Un bon bouquin sur kali linux et le pentesting pourrait nous aider à mieux comprendre
            comment sécuriser un serveur.


    Kali Linux: Wireless Penetration Testing Beginner's Guide

            https://www.amazon.com/Kali-Linux-Wireless-Penetration-Beginners/dp/1783280417/

                    261     pages
                    36      reviews
                    4.6/5   stars


    Learning Penetration Testing with Python

            https://www.amazon.com/Learning-Penetration-Testing-Python-Christopher-ebook/dp/B013GKGLB2/

                    316     pages
                    6       reviews
                    5.0/5   stars


    Wireshark 101: Essential Skills for Network Analysis

            https://www.amazon.com/Wireshark-101-Essential-Analysis-Solutions-ebook/dp/B00BF50LD0/

                    372     pages
                    81      reviews
                    4.7/5   stars

            Un bon bouquin pour apprendre à faire de la capture réseau.


                                     NOTE:

            À lire également sur le même sujet, un tuto à propos de tcpdump:

                    https://danielmiessler.com/study/tcpdump/


    https://openclassrooms.com/ > Cours > Systèmes et réseaux
                                > Voir aussi les 100 cours non certifiants correspondant à cette recherche

            Comme il n'y a pas de livre correspondant à tout ce qui nous intéresse sur le réseau,
            on peut chercher des cours sur openclassrooms, entre autres:

                    Fondamentaux:

                    https://openclassrooms.com/courses/apprenez-le-fonctionnement-des-reseaux-tcp-ip
                    https://openclassrooms.com/courses/calculer-une-plage-d-adresses-avec-la-methode-magique
                    https://openclassrooms.com/courses/manipulez-les-paquets-reseau-avec-scapy
                    https://openclassrooms.com/courses/comment-se-connecter-manuellement-au-reseau
                    https://openclassrooms.com/courses/l-idle-port-scan
                    https://openclassrooms.com/courses/mise-en-place-d-un-tunnel-tcp-ip-via-ssh
                    https://openclassrooms.com/courses/installer-un-reseau-wi-fi-sur-ubuntu-et-derives

                    Sécurité:

                    https://openclassrooms.com/courses/securiser-son-serveur-linux
                    https://openclassrooms.com/courses/proteger-son-serveur-avec-fail2ban

                    Serveurs:

                    https://openclassrooms.com/courses/mettre-en-place-un-serveur-samba (partage de fichiers)
                    https://openclassrooms.com/courses/mise-en-place-d-un-serveur-dhcp-sous-linux
                    https://openclassrooms.com/courses/un-serveur-d-hebergement-multiutilisateur-sous-linux
                    https://openclassrooms.com/courses/creer-son-propre-serveur-vpn-avec-open-vpn
                    https://openclassrooms.com/courses/creer-son-serveur-ftp
                    https://openclassrooms.com/courses/mise-en-place-des-serveurs-apache-et-dns
                    https://openclassrooms.com/courses/interagir-avec-le-serveur-ftp
                    https://openclassrooms.com/courses/installer-configurer-et-utiliser-xampp-sous-ubuntu

                    DNS:

                    https://openclassrooms.com/courses/gerer-son-nom-de-domaine
                    https://openclassrooms.com/courses/les-noms-de-domaine
                    https://openclassrooms.com/courses/maradns-comme-serveur-dns
                    https://openclassrooms.com/courses/installer-un-serveur-dns-avec-djbdns-sous-debian

                    Divers:

                    https://openclassrooms.com/courses/gerer-votre-mail-a-la-unix
                    https://openclassrooms.com/courses/wake-on-lan
                    https://openclassrooms.com/courses/le-protocole-bittorrent
                    https://openclassrooms.com/courses/personnaliser-le-skin-de-son-ftp
                    https://openclassrooms.com/courses/le-htaccess-et-ses-fonctionnalites

# VNC

Pour + d'infos:

            https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-vnc-on-ubuntu-16-04
            http://onkea.com/ubuntu-vnc-grey-screen/ (fix bug écran gris)

La fin du tuto de digitalocean est utile pour apprendre à configurer le serveur VNC comme un service
systemd, qu'on pourra alors lancer/arrêter/relancer comme n'importe quel autre service systemd.


                                     NOTE:

Il paraît que `x2go` est meilleur, plus rapide, et moins gourmand en ressource:

        http://wiki.x2go.org/doku.php

À confirmer…



    sudo apt install tightvncserver openssh-server

            Installer un serveur VNC et ssh sur la machine distante.


    vncserver

            Lancer le serveur VNC.

            Il va nous demander de choisir un mdp pour qu'on puisse s'authentifier depuis notre pc.
            Il va également nous demander si on veut créer un 2e mdp (`view-only password`), ne permettant
            que de voir le bureau distant sans pouvoir interagir avec (répondre non).


    vncserver -kill :1

            Stopper le serveur.


    mv ~/.vnc/xstartup ~/.vnc/xstartup.bak

            Créer un backup de `~/.vnc/xstartup`.

            Il s'agit d'un fichier de conf lu par le serveur VNC à chaque fois qu'il est lancé.


    vim ~/.vnc/xstartup

            Éditer le fichier de conf du serveur pour y écrire:

                    #!/bin/bash
                    unset SESSION_MANAGER
                    unset DBUS_SESSION_BUS_ADDRESS

                    startxfce4

            On peut ajouter d'autres instructions en s'inspirant du fichier de conf d'origine.
            Pex:
                    [ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources

            Source `$HOME/.Xresources`, si le fichier existe.
            Il s'agit d'un fichier dans lequel l'utilisateur peut modifier certains paramètres du DE.


    sudo chmod +x ~/.vnc/xstartup

            Rendre le fichier de conf du serveur VNC exécutable.


    vncserver [-geometry 1680x1050] :1

            Relancer le serveur avec la résolution de son choix.

            La résolution affecte la taille de la fenêtre sur notre pc.
            On peut lister les différentes résolutions supportées par notre pc via:

                    $ xrandr -q

            Avant de passer à notre pc, penser à désactiver le raccourci `Super-Tab` dans le gestionnaire
            de fenêtres, car ce dernier empêchera chaque appui sur la touche Tab depuis notre pc
            d'être envoyé à l'application ayant le focus (pas d'auto-complétion dans le shell pex).


    ssh -L 5901:127.0.0.1:5901 -N -f -l username server_ip_address

            Depuis notre pc, créer un tunnel ssh vers la machine distante (?) écoutant sur le port 5901 (?),
            pour chiffrer / protéger nos communications.

                    -L port:host:hostport

                          The given port on the local host is to be forwarded to the given host and
                          port on the remote side.
                          This works by allocating a socket to listen to port on the local side.
                          Whenever a connection is made to this port, the connection is forwarded
                          over the secure channel, and a connection is made to host port hostport
                          from the remote machine.

                    -N    Do not execute a remote command.
                          This is useful for just forwarding ports (protocol version 2 only).

                    -f    Requests ssh to go to background just before command execution.


    xtightvncviewer localhost:5901

            Se connecter au / afficher le bureau de la machine distante.

# SCP

    scp -P 22 -pr  local_folder  login@ip:distant_folder
         |     ||
         |     |+-- copie récursivement
         |     +-- préserve les modes, dates de modif/accès
         +-- port sur lequel écoute le serveur ssh distant

            Copie le dossier `local_folder/` dans `distant_folder/`, en se connectant en tant que `login`
            sur la machine identifiée par l'adresse `ip`.

##
# Todo
## Learn the `ss(8)` and `ip(8)` suite of commands.

Apparently, they are better than the old `ifconfig(8)` and `netstat(8)`:
<https://utcc.utoronto.ca/~cks/space/blog/linux/ReplacingNetstatNotBad?showcomments#comments>

