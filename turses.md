
#				DESCRIPTION

turses est un client twitter en console utilisant de nombreux raccourcis vim.

Projet : https://github.com/dialelo/turses
Documentation : https://turses.readthedocs.org/en/latest/

#				INSTALLATION

Pour l'installer, passer par son package manager, ou pour une versio + récente par pip (pip install turses) ou par github :
    git clone https://github.com/dialelo/turses
    cd turses
    sudo python setup.py install

Lors du 1er lancement, turses demandera à pouvoir accéder à notre compte twitter.
Pour ce faire, il génère un token d'authentification à faire valider par twitter.
Puis, il donne une url à laquelle il faut se rendre, se connecter avec son compte, copier le code pin fourni par twitter,
et le coller dans turses.

Par la suite pour utiliser un nouveau token d'authentification (si l'ancien a été compromis) :
    rm .turses/token
Sur son compte twitter : Settings > Apps > cliquer sur le bouton Revoke access de la case turses
Relancer turses.

#				CONFIGURATION

Par défaut, les tweets sont publiques.
Toutefois, il est possible de protéger ses tweets, càd faire en sorte que seuls les followers approuvés puissent les voir.
Pour ce faire, sur son compte twitter : Settings > Security and privacy > cocher Protect my Tweets (section Privacy)
Protéger ses tweets induit d'autres limitations : https://support.twitter.com/articles/14016#

#				UTILISATION

    ?            lister les raccourcis
                 man turses

    escape       quitter la liste des raccourcis

    q            quitter le pgm

    t            envoyer un tweet

    r            répondre à un tweet

    S            rafraîchir toutes les timelines

    h l          naviguer entre les buffers (onglets / timelines : tweets, mentions, favorites, messages, me)

    j k          naviguer entre les tweets

    n       afficher simultanément plusieurs buffers / timelines (raccourci répétable 4 fois pour afficher tous les buffers simultanément)
    N       supprimer de l'affichage simultané le dernier buffer ajouté

    d            supprimer le buffer (timeline) sélectionné

Ajouter le buffer / timeline d'une certaine catégorie de tweets.
    .	home
    _	my tweets
    B	my favorites
    m	mentions (les tweets qui mentionnent mon nom)
    M	direct message
    /	tweets contenant le mot-clé fourni dans la fenêtre qui s'ouvre
    @	tweets de l'utilisateur fourni dans la fenêtre qui s'ouvre
    +	tweets de l'utilisateur à l'origine du tweet ayant le focus
    T	le fil du tweet ayant le focus

Pour + de catégories, lire la section Timelines de l'aide.

    O o       ouvrir dans le navigateur le lien vers le tweet ayant le focus / le lien contenu dans le tweet

