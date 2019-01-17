
tr est une commande qui transforme ou supprime des caractères dans un texte.
Elle ne lit que l'entrée standard et n'altère pas le contenu d'origine.

    tr a b < foo > bar              Dans le fichier foo, remplacer toutes les occurrences de a en b, et écrire le résultat dans bar.

    tr 'a-z' 'A-Z' < foo > bar      Faire passer en majuscule tout le texte de foo, et écrire le résultat dans bar.

    echo "0123456789" | tr "0-9" "a-z"
                                    Lire "0123456789" sur l'entrée standard, transformer les chiffres en lettres (a-j),
                                    et produire le résultat sur la sortie standard.

    tr -d 'foo' < bar > baz         Suppression de la chaîne foo du fichier bar, et écriture du résultat dans baz.

    tr -s 'x' < foo > bar       Remplacer toute séquence multiple du même caractère x par une seule occurrence.
                                -s = --squeeze-repeats

    tr -dc 'a-z A-Z \t \n '\32'' < foo > bar

                                Supprimer (-d) tous les caractères à l'exception (-c = --complement) des lettres,
                                tabulations, newlines et espaces.
                                code ascii d'un espace = 32

    tr 'a-z' 'n-za-m' < foo > bar 
    echo "some text" | tr 'a-z' 'n-za-m'

                                Décaler tous les caractères de 13 places (ROT13, cas particulier du chiffre de César).
                                https://fr.wikipedia.org/wiki/ROT13
