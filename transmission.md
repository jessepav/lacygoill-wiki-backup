
# Installation

`aptitude install transmission-daemon`

# WebUI

Le serveur web transmission permet de contrôler transmission-daemon depuis une machine distante au travers d'un onglet d'un navigateur.
`Edit > Preferences > Remote > cocher Allow remote acess`

Le client transmission lance alors un serveur (démon) écoutant par défaut sur le port 9091.\
Le démon s'arrête quand on ferme le client transmission.

On peut tester l'interface web, tout de suite en local, en cliquant sur Open web client.\
On peut accéder au démon depuis n'importe quelle machine via l'url :

    http://<ip machine>:9091/transmission/web/

On peut protéger l'accès à l'interface en cochant Use authentication (et en choisissant un pseudo + un mdp),
et / ou en cochant Only allow these IP addresses (par défaut 127.0.0.1, du coup pas de danger).
