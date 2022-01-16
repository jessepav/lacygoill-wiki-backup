
Enregistrer dans foo.txt les commandes tapées dans un shell pour les afficher plus tard.

    script foo.txt		débuter l'enregistrement
    exit		    	finir l'enregistrement

    less foo.txt         lire les commandes enregistrées dans foo.txt.

    script -t foo.txt 2>foo.txt.timing

                        Enregistrer dans foo.txt et les timestamps dans foo.txt.timing,
                        pour pouvoir rejouer les commande en temps réel.

                        La redirection des timestamps se fait en 2 temps, d'abord vers foo.txt via l'option -t,
                        puis vers la sortie d'erreurs elle-même via 2>.

    scriptreplay foo.txt.timing foo.txt [-d | --divisor <n>]

                        Rejouer les commandes enregistrées dans foo.txt en temps réel grâce aux timestamps stockés
                        dans foo.txt.timing
                        On peut accélérer le replay en divisant (-d <n>) par <n> (nb flottant) la durée totale du script.

Pour du partage de terminal en temps réel, voir ici : https://inuits.eu/blog/script-must-know-command-sysadmins
