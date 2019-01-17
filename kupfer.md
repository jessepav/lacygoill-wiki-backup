
Le pgm se lance via le raccourci C-space.

L'interface de base se décompose en 2 panneaux : un objet + une action.

Parfois un 3e s'affiche, il correspond à un complément d'information (où, quand) :
pex on peut y passer en mode texte (.) et taper une durée, pour définir un compte à rebours avant que l'action ne s'exécute ;
ou bien on peut y définir où la copie d'un fichier doit s'effectuer.

On peut naviguer entre les panneaux via la touche `tab`.


Pour supprimer un trigger (raccourci) :

        - triggers
        - ↓ et sélectionner le raccourci qu'on souhaite supprimer
        - tab
        - ↓ et sélectionner "Remove Trigger"


# KEY BINDINGS

    backspace

            effacer l'objet / l'action courant(e)

    ↓

            afficher menu déroulant contenant les différents objets / actions disponibles


    ,

            Ajouter l'objet courant (programme, fichier, ...) à  une pile sur laquelle on peut agir
            "comma trick". On  peut pex lancer plusieurs pgm simultanément,  sans avoir à repasser
            par kupfer à  chaque fois. Si les  objets sont de nature différente,  aucune action ne
            sera possible sur la pile.


    /

            chercher un fichier / dossier depuis la racine


    C-Enter

            combiner l'objet et l'action courante (et éventuellement complément)
            ça donne accès, dans le panneau action, à "Add Trigger" et "Run after delay"
            "Add Trigger" permet d'associer un raccourci à une combinaison objet + action (+ complément)
            "Run after delay" permet de définir un compte à rebours avant que l'action ne s'exécute


    home CR

            ouvrir le home


    home →
    home M-→

            Afficher les sous-dossiers et fichiers du home dans un menu déroulant.
            Idem, mais inclut aussi les éléments cachés.


    C-r

            reset tous les panneaux


    C-s

            passer au 1er panneau


    C-t

            sélectionner le texte mis en surbrillance (où qu'il soit : mousepad, vim...)


    C-;

            afficher les préférences


    C-.
            passer en mode texte


    C-g

            sélectionner les éléments (fichiers, dossiers) déjà sélectionnés dans l'exporateur de fichier


    F1

            afficher l'aide du pgm


    =
    =help

            Faire un calcul.
            Afficher toutes les fonctions mathématiques disponibles.

# EXEMPLES D'UTILISATION

Objectif : ouverture de /home dans 3s

        - home
        - C-enter
        - tab
        - flèche bas, sélectionner "Run after delay"
        - tab (pour passer dans un 3e volet qui vient d'apparaître)
        - .(point) 0m3s <enter>


Objectif : affichage du message "faire des courses" dans 5s

        - . faire des courses
        - C-enter
        - Tab
        - flèche bas, sélectionner "Run after delay"
        - Tab
        - . 5s CR
