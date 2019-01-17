La commande grep tient son nom de la façon dont était documentée la commande (Ex) globale (:g) dans l'éditeur de texte ex
(extended line editor):    :g/re/p = globally (g) print (p) lines containing a regular expression (re)
:p était la commande Ex servant à imprimer des lignes de texte (:.,+25p = imprimer de la ligne courante jusqu'à la 25e ligne suivante).

    grep -o pattern file        N'afficher que le pattern trouvé, autant de fois qu'il y a de matchs
                                et à chaque fois sur une ligne différente.
                                Par défaut, grep retourne toute la ligne sur laquelle un match a été trouvé.
                                -o, --only-matching

    grep -q pattern file        Ne rien afficher sur la sortie standard,
                                et s'arrêter dès qu'un match est trouvé en produisant le code de sortie 0.

                                Utile dans un script pour vérifier la présence d'une chaîne dans un fichier ou
                                sur la sortie standard d'une précédente commande suivie d'un pipe.

    grep -Rn pattern *          chercher pattern dans tous les fichiers et dossiers du répertoire courant,
                                récursivement (-R) et en faisant précéder chaque match du n° de la ligne du fichier
                                sur laquelle il se trouve (-n)

    grep pattern file               search a file for a pattern

    grep -in pattern file           Case insensitive search (with line numbers)

    grep -R pattern folder          Recursively grep for string <pattern> in folder

    grep -f pattern_file file       Read search patterns from a file (one per line)

    grep -v pattern file            Find lines NOT containing pattern

You can grep with regular expressions
    grep "^00" file  #Match lines starting with 00
    grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" file  #Find IP add

Find all files which match {pattern} in {directory}
This will show: "file:line my research"
    grep -rnw 'directory' -e "pattern"

Exclude grep from your grepped output of ps.
Add [] to the first letter. Ex: sshd -> [s]shd
    ps aux | grep '[h]ttpd'

Colour in red {bash} and keep all other lines
    ps aux | grep -E --color 'bash|$'
