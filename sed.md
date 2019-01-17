# VOCA

    input    pattern-space    output

            `input` et `output` sont l'entrée et la sortie de sed.
            `input` peut être:

                    - le clavier
                    - un fichier:    sed file
                    - un pipe:       cmd | sed

            `pattern space` est une sorte de cahier de brouillon dans lequel sed travaille.

            Ces termes sont importants pour comprendre le fonctionnement de base de sed:

                    1. sed copie la 1e ligne de `input` dans `pattern space`
                    2. il exécute son programme sur elle
                    3. il supprime la ligne transformée et l'écrit sur sa sortie
                    4. il passe à la 2e ligne de `input`, et répète les mêmes opérations jusqu'à la fin de `input`

# COMMANDES

        sed '' file
        sed -n 'p' file

Affiche le contenu de `file`.

La 1e commande affiche `file`, car par défaut, sed écrit le pattern space sur sa
sortie.
Il affiche le résultat de la transformation qu'on lui a demandée d'opérer.

Ici la transformation est vide '', donc sed affiche `file` inchangé.

La 2e  commande affiche `file`, car  on a désactivé l'écriture  du pattern space
via le flag `-n`, mais on exécute  aussi la commande `p` qui réactive l'écriture
du pattern space:

        -n et 'p' s'annulent

On peut considérer  que sed ajoute automatiquement une commande  `p` implicite à
la fin de n'importe quel programme.
Et `-n` est le seul moyen de la supprimer.

---

    sed -n '' file
    sed 'p' file

            N'affiche rien.
            Dédouble chaque ligne de `file`.

            La 1e commande n'affiche rien, car `-n` (--quiet, --silent) désactive l'écriture
            du pattern space sur la sortie.

            La 2e commande affiche 2 fois chaque ligne de `file`:

                    - une fois à cause de notre commande `p` explicite
                    - une fois à cause de la commande `p` implicite de sed


    cat file | sed -n '1,4p'

            Affiche les 4 premières lignes de `file`.


    sed -n '$i'p foo

            Extraire la i-ème ligne de foo


    sed 's/day/night/g' file.txt

            To replace all occurrences of "day" with "night" and write to stdout:


    sed -i 's/day/night/g' file.txt

            To replace all occurrences of "day" with "night" within file.txt:


    echo 'It is daytime' | sed 's/day/night/g'

            To replace all occurrences of "day" with "night" on stdin:


    sed -i -r 's/^\s+//g' file.txt

            To remove leading spaces


    sed '/^$/d' file.txt

            To remove empty lines and print results to stdout:


    sed ':a;N;$!ba;s/\n//g'  file.txt

            To replace newlines in multiple lines
