# CONSTANTES

Nb d'Euler ou constante de Napier/Néper:

        𝑒 ≈ 2.71828
        𝑒 = lim (1+1/n)ⁿ    n → +∞
        𝑒 = Σ (1/n!)        n ∈ [0; +∞[

On peut également définir 𝑒 via la relation suivante:

        aire sous la courbe 1/x entre 1 et 𝑒 = 1
        ln(𝑒) - ln(1)                        = 1 (1-0)

# NOMBRES COMPLEXES

    +1
    -1
     i

            Pour enlever toute confusion/mystère autour du nombre `i`, communément appelé "imaginaire",
            Gauss aurait préféré qu'on qualifie `1`, `-1` et `i` de nombre:

                    - direct
                    - inverse
                    - latéral

            Pour comprendre ces qualifications, il faut se représenter, dans un plan de repère (O, Ox, Oy),
            les points de coordonnées:

                    - (1,  0)
                    - (-1, 0)
                    - (0,  1)

                             y  latéral

                             ^
                             |
                            i+
                             |
                            O|
            inverse    --+---+---+--> x    direct
                        -1   |   1
                             |


    Toute équation polynomiale de degré `n` a exactement `n` solutions/racines

            Théorème fondamental de l'algèbre démontré par Gauss.
            https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_fondamental_de_l%27alg%C3%A8bre

            Un peu de voca anglais sur le sujet:

                    f(x) = Σ (αi * x^i)

            "We could plug `n` complex numbers into this function, and get `0` out":

                    - plug into
                    - get `0` out


    x^2 + 1 = 0

            Cette équation a 2 solutions, d'après le théorème fondamental de l'algèbre.

            Ça peut paraître étrange, car on ne voit pas quel nombre réel on pourrait brancher (plug into),
            dans cette équation pour obtenir 0 en sortie (get `0` out).

            Le pb vient du fait qu'on ne cherche les solutions que dans un espace à 1 dimension.

            Si on ajoute une 2e dimension à l'espace de définition de la fonction `f(x) = x^2 + 1`,
            on passe d'un domaine de définition unidimensionnel à un domaine bidimensionnel.
            D'une droite (axe des abscisses `y = 0`), à un plan (`z = 0`).

            Et on passe également d'un espace image unidimensionnel (parabole), à un espace image bidimensionnel.


    x = [-b ± √(b^2 - 4ac)]/2a

            Formule quadratique permettant de résoudre les équations du 2e degré.

            Qd le déterminant `b^2 - 4ac` est négatif, on obtient des racines carrés de nombres négatifs.
            Aucun nombre réel élevé au carré n'est négatif.

            La formule quadratique semble donc échouer pour certains coef `a`, `b` et `c` judicieusement choisis.


    x = ∛[d/2 + √[(d/2)^2 - (c/3)^3]] + ∛[d/2 - √[(d/2)^2 - (c/3)^3]]

            Formule cubique permettant de résoudre les équations du 3e degré du type:

                    x^3 = c*x + d

            Qd `(d/2)^2 - (c/3)^3` est négatif, on obtient à nouveau des racines carrés de nombres négatifs.
            Et à nouveau, il semble qu'on ait une formule qui peut échouer pour certains coef `c` et `d`
            bien choisis. C'est par exemple le cas pour l'équation:

                    x^3 = 15x + 4

            Mais cette fois, on sait qu'il doit y avoir au moins une solution. En effet, la représentation
            d'une fonction cubique, peu importe les coef choisis, coupe tjrs l'axe des abscisses en au moins
            un point.
            Ceci contraste avec la parabole d'une fonction quadratique, qui peut ne jamais couper l'axe
            des abscisses.


    √-1

            Qd les mathématiciens ont cherché à résoudre les équations cubique du type `x^3 = c*x + d`,
            ils ont été obligés d'inventer un nombre dont le carré était `-1`.

            De la même façon que dans le passé, ils ont été obligés d'inventer les fractions, puis les nombres
            négatifs, et le nombre 0 pour résoudre d'autres problèmes.

            On pourrait aussi parler de "découverte", plutôt que d'"invention", mais quel terme choisir
            est une question philosophique.

            En inventant `√-1`, on peut exprimer la racine carré de n'importe quel nombre négatif:

                    √(-25) = √(-1) * √(25) = 5√(-1)

            Toutefois, dans un calcul, il faut faire attention à tjrs exprimer la racine carré d'un nb
            négatif comme une quantité de `√-1` dès le début:

                    √-2 * √-5
                  = √(-2 * -5)
                  = √10           ✘

                    √-2 * √-5
                  = (√2 * √-1) * ( √5 * √-1)
                  = √10 * (√-1)^2
                  = -√10          ✔

# STATISTIQUES

    http://students.brown.edu/seeing-theory/index.html

# THÉORÈMES
## d'incomplétude de gödel

    "Cette phrase est fausse."

        Cette phrase est-elle vraie ou fausse ?

        Si cette phrase est vraie alors ce qu'elle dit est vrai, et elle est fausse.    (impossible)
        Si cette phrase est fausse alors ce qu'elle dit est faux, et elle est vraie.    (")

        Il s'agit du paradoxe du menteur.


    Let R = {x | x ∉ x},    then    R ∈ R ⇔ R ∉ R

        Notons R l'ensemble des ensembles qui ne sont pas un élément d'eux-mêmes.

        R est-il un élément de lui-même ou pas ?

        Si R est un élément de lui-même, alors il ne l'est pas.    (impossible)
        Si R n'est pas un élément de lui-même, alors il l'est.     (")

        Il s'agit du paradoxe de Russell, variante du paradoxe du menteur transposé de la philo
        à la théorie des ensembles (fondatrice des maths).


    P(E) = {x: x ⊂ E}

        Cette relation définit ce qu'est l'ensemble des parties d'un ensemble E.
        Il s'agit de l'ensemble de tous les ensembles inclus dans E, noté P(E).

        On peut considérer P comme un opérateur prenant comme opérande un ensemble E, auquel il associe
        un nouvel ensemble P(E) (appelé 'power set' en anglais). Ex:

                P({0,1}) = {∅, {0}, {1}, {0,1}}


    |P(E)| > |E|

        Il s'agit du théorème de Cantor, qui dit que le cardinal d'un ensemble est tjrs strictement
        inférieur à celui de l'ensemble de ses parties.

        Card(E) et |E| sont 2 notations désignant le cardinal d'un ensemble, sa taille.
        La démonstration fait intervenir les affirmations suivantes:

                |E| = n    ⇒    |P(E)| = 2ⁿ
                2ⁿ  > n

        La 1e implication dit que si le cardinal d'un ensemble E est n, alors celui de l'ensemble
        de ses parties est 2ⁿ.

        2 ensembles A et B ont le même cardinal ssi il existe une bijection de A sur B.
        Dans ce cas, on dit qu'ils sont équipotents.

        On déduit du théorème que l'ensemble des parties de ℕ est plus grand que ℕ:

                |P(ℕ)| > |ℕ|

        Ceci prouve qu'il existe des ensembles infinis plus grand que d'autres.
        De plus, on peut répéter l'opération P autant de fois qu'on veut :

                … > |P(P(ℕ))| > |P(ℕ)| > |ℕ|

        Il existe donc une infinité d'ensembles infinis tous de tailles différentes.


What is a formal system?


    Un caillou a senti la couleur neuf.

        Il s'agit d'un exemple de phrase correcte syntaxiquement mais n'ayant pas de sens sémantique:

                - Un caillou ne peut pas sentir.
                - On ne peut pas sentir une couleur.
                - La couleur neuf n'existe pas.


L'énigme MU.

        Alphabet:

            Σ = {M, U, I}

        Règle de syntaxe:

            une chaîne doit contenir exactement un M

        Règles de déductions:

                - xI       >    xIU
                - Mx       >    Mxx
                - xIIIy    >    xUy
                - xUUy     >    xy

        x, y peuvent être n'importe quelles chaînes valides, y compris la chaîne vide.

        Axiome:

                MI

        Pb:

                prouver MU

                2^x - 6y = 0    ⇔    3y = 2^(x-1)    ✘

                La dernière égalité est impossible, MU est bien une wff mais pas un théorème.

##
# To read

<https://venhance.github.io/napkin/Napkin.pdf>
