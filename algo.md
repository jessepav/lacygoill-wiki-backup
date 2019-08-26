# Which kind of interval should I use to represent a sequence of numbers?

We can represent the sequence of numbers from 1 to N in 4 ways:

    a) 1 <= i <  N+1
    b) 0 <  i <= N
    c) 1 <= i <= N
    d) 0 <  i <  N+1

Which version is better?

Suppose that we want to represent the sequence of numbers from `0` to `N`.
If we used the notation `b` or `d`, we would need a negative lower bound.
This is ugly, so we should avoid them.

Which version is better between `a` and `c`?
Suppose that we want to represent the sequence of numbers from `0` to `1`:

    a) 0 <= i <  2
    c) 0 <= i <= 1

Suppose that we want to represent the sequence of numbers from `0` to `0`:

    a) 0 <= i <  1
    c) 0 <= i <= 0

Suppose that we want to represent the EMPTY sequence of numbers starting from `0`:

    a) 0 <= i <  0
    c) 0 <= i <= -1

`c` is ugly because of the negative upper bound.
So, `a` is the best notation.

Also, `a` provide 2 benefits (`b` provide them too):

   - the difference between the upper and lower bound is equal to the size of
     the sequence

   - if 2 subsequences A and B are “adjacent” (A ∩ B = ∅ and A ∪ B = sequence),
     the upper bound of A is equal to the lower bound of B

Source:

<https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html>

# Why numbering should start at zero?

We know that the best way to represent the sequence of numbers from `1` to `N` is:

    1 <= i < N+1

So, to subscript an array, we could use:

    1 <= i < N+1

or:

    0 <= i < N

The last notation is  shorter, so we should start indexing an  array with 0, and
not 1.

##
##
##
# Algorithms To Live By
## Intro

Du fait,  que nos vies  sont limités en temps  et en espace  (contraintes), nous
rencontrons tous un ensemble de pbs :

   - que devons-nous faire / laisser tomber ?

   - quel degré de désordre devrions-nous adopter / quel degré d'ordre est
     excessif ?

   - quel équilibre entre nouvelles expériences (voyager...) et expériences
     favorites (aller au ciné...) produit la vie la plus épanouissante
     (explore/exploit) ?

Les informaticiens se sont attaqués et ont souvent résolus des problèmes équivalents :

   - comment un processeur devrait allouer son 'attention' pour exécuter toutes
     les tâches demandées par l'utilisateur ?

   - qd devrait-il passer à une autre tâche ?

   - combien de tâches devrait-il prendre en charge ?

   - quelle est la meilleure façon d'utiliser ses ressources en mémoire limitées

   - devrait-il accumuler encore un peu plus d'infos ou agir immédiatement avec
     ce qu'il a déjà


De nos jours, on  demande à nos ordinateurs de résoudre  des pbs complexes comme
discuter avec  des humains  (chatbot), réparer un  fichier corrompu,  gagner une
partie de Go.
Ces pbs  sont complexes, car  les règles ne  sont pas tjrs  évidentes, certaines
informations  nécessaires   sont  manquantes,   ou  trouver  la   bonne  réponse
demanderait trop de calculs.
Les algo qui tentent de les résoudre doivent être à l'aise avec les probabilités
et échanger du temps contre de la précision.
Ils sont confrontés aux même pbs que les humains:

   - Comment gérer un espace fini, un temps fini, une attention limitée, des
     inconnus inconnus (what we don't know we don't know), de l'information
     incomplète et un futur imprévisible ?

   - Comment le faire gracieusement et avec confiance ?

   - Comment le faire au sein d'une communauté d'individus qui essaient tous de
     faire de même simultanément ?

Au bout du  compte, les algos peuvent  nous apprendre des principes  de vie, une
nouvelle façon de voir les pbs qui nous entourent (via leur structure élégante),
une meilleure compréhension  de notre esprit, et un vocabulaire  pour décrire le
monde.

## Optimal stopping
### Règle des 37%

Qd on cherche un appartement, contrairement à  un acheteur en ligne ou un client
dans un magasin, on  n'a pas le temps de comparer, il  faut prendre une décision
immédiatement.
Soit  on prend  l'appartement qu'on  est en  train de  visiter, et  on abandonne
toutes les autres annonces, soit on s'en va sans jamais revenir.

Supposons   qu'on  souhaite   maximiser  nos   chances  d'obtenir   le  meilleur
appartement,  càd réduire  les chances  de quitter  un bon  appartement sans  le
prendre, et réduire les chances de prendre un appartement alors qu'il existe une
meilleure annonce.
Le pb est le suivant:

   1. on a aucune idée de ce que vaut un appartement individuellement dans
      l'absolu, mais on peut facilement les comparer entre eux et trouver qu'on
      en préfère un plutôt qu'un autre. En maths, on pourrait dire qu'on a accès
      aux nombres ordinaux (rangs relatifs des appartements), mais pas aux
      cardinaux (leur note sur une échelle générale).

   2. on a besoin d'un point de comparaison pour pouvoir décider si
      l'appartement qu'on visite est le meilleur

   3. on a donc besoin de visiter un échantillon d'appartements pour établir ce
      point de comparaison; on ne louera aucun d'entre eux, car notre objectif
      ne sera pas de trouver un bon appartment mais un bon point de comparaison

   4. chaque appartement visité uniquement dans le but d'établir le point de
      comparaison augmente la qualité de ce dernier MAIS réduit nos chances
      d'obtenir le meilleur appartement

La réponse intuitive à  ce pb est de trouver un  juste milieu entre compulsivité
et réflexion excessive.
La résolution mathématique de ce pb, nous  dit que pour maximiser nos chances de
trouver le meilleur appartement, il faut  visiter 37% (1/𝑒) d'entre eux sans les
acheter.
Passé cette  phase de  calibrage, il  faut prendre le  1er appartement  qui sera
meilleur que le meilleur appartement visité au sein de l'échantillon.
En utilisant  cette stratégie, le  pourcentage de chances d'obtenir  le meilleur
appartement converge  vers 37% (1/𝑒), comme  le montre la 3e  colonne du tableau
suivant:

        Nb d'appartements  |  Prendre le meilleur  |  Chances d'obtenir
        à visiter          |  appartement après    |  le meilleur
        -------------------|-----------------------|-------------------
        3                  |  1 (33.33%)           |  50%
        4                  |  1 (25%)              |  45.83%
        5                  |  2 (40%)              |  43.33%
        6                  |  2 (33.33%)           |  42.78%
        7                  |  2 (28.57%)           |  41.43%
        8                  |  3 (37.5%)            |  40.98%
        9                  |  3 (33.33%)           |  40.59%
        10                 |  3 (30%)              |  39.87%
        20                 |  7 (35%)              |  38.42%
        30                 |  11 (36.67%)          |  37.86%
        40                 |  15 (37.5%)           |  37.57%
        50                 |  18 (36%)             |  37.43%
        100                |  37 (37%)             |  37.10%
        1000               |  1000 (36.9%)         |  36.81%


À noter que  cette stratégie est loin d'être idéale  (63% de chances d'échouer),
elle est simplement bien meilleure que le hasard pur.
Pex, dans le cas où on aurait 3 appartements à considérer, et qu'on les numérote
en fonction de leur valeur 1, 2 et 3  (1 étant meilleur que 2, et 2 meilleur que
3).
La stratégie nous dit qu'il faut faire  l'impasse sur le 1er, et ne choisir qu'à
partir du 2e.
De plus, on peut les visiter dans 6 (3!) ordres différents:

        1-2-3    on passe à côté du meilleur, car il est visité en 1er (on prendra 3)
        1-3-2    "                                                     (on prendra 2)
        3-2-1    on passe à côté du meilleur, car on prendra 2 qui est meilleur que 3

        2-1-3    on prend le meilleur
        2-3-1    "
        3-1-2    "

Ici, on  voit bien  que la  stratégie nous donne  50% de  chances de  choisir le
meilleur, le hasard ne nous donnerait que 33% de chances.
Plus le nb d'options (ici des  appartements) augmente, plus le hasard nous donne
de faibles chances de choisir la meilleure.
En revanche, la règle des 37% nous donne toujours les mêmes chances:  37%

### Variantes du pb du secrétaire

La  recherche d'un  appartement appartient  à  une classe  de pbs  mathématiques
appelée optimal stopping/arrêt optimal.
C'est aussi  le nom d'une théorie  mathématique qui cherche à  déterminer le bon
moment  où agir  pour maximiser  une récompense  attendue ou  minimiser un  coût
attendu.

Le problème du  secrétaire est le plus  célèbre exemple de pbs au  sein de cette
classe.
De nombreux autres pbs de la vie quotidienne appartiennent à cette même classe:

   - jusqu'où peut-on aller dans une entreprise financière qui rapporte mais qui
     est risquée ?

   - combien de temps refuser des offres pour la voiture qu'on vend ?

   - quel partenaire amoureux choisir ?


Pour certains pbs, le nb d'options à considérer n'est pas évident.
Pex,  pour 'quel  partenaire amoureux  choisir  ?', on  ne sait  pas à  l'avance
combien de  personnes on rencontrera dans  notre vie qui seront  susceptibles de
devenir notre compagnon.
Dans ce cas,  on peut adapter la stratégie en  définissant notre échantillon non
pas comme 37% des options, mais comme 37% de notre temps.
Ainsi,  si on  pense qu'on  cherchera un  partenaire entre  18 et  40 ans,  soit
pendant 22  ans, il  faudra flirter  jusqu'à 26  ans, et  être prêt  à s'engager
au-delà (26 ≈ 18 + 22/𝑒).


Dans la réalité, on peut rencontrer des variantes du problème du secrétaire dont
certaines conditions initiales sont différentes.

Pex, il se peut qu'une personne refuse notre proposition de vie commune (absence
de garantie de succès).
Dans ce cas, en supposant que la  probabilité d'être rejeté soit de 50%, il faut
adapter la stratégie en commençant à  faire des propositions après avoir cherché
25% de son temps (contre 37% auparavant).
Les chances de succès sont alors de 25% également.

Il se peut aussi  qu'on ait droit à une 2e chance  (rappeler une ancienne petite
amie avec laquelle on a rompu).
Dans le  2e cas, en  supposant que la probabilité  d'être accepté lors  d'une 1e
proposition soit de 100%, mais seulement de 50% lors d'une 2e proposition (après
une rupture), il faut faire des propositions après 61% de son temps.
Si on est toujours célibataire après avoir considéré toutes les possibilités, il
faut rappeler  la meilleure petite  amie rencontré pendant  les 61% de  temps de
recherche.
Les chances de succès sont alors de 61% également.

### Règle du seuil

Jusqu'à présent, on n'avait aucune information pour évaluer une option.
De ce  fait, il  fallait passer  par une  phase de  calibrage ('look')  avant de
prendre une option ('leap').
Mais supposons qu'on ait une information et que ce soit la seule qui compte.
En théorie des jeux, on parle alors de jeu à information complète.
En anglais on parle de 'full-information game' (par opposition à 'no-information
game').
Dans ce cas, il n'y a plus besoin de 'look' avant de 'leap'.
Et  au lieu  d'utiliser la  règle des  37%,  ou une  de ses  variantes, il  faut
appliquer la règle du seuil (threshold rule).

Cette nouvelle  règle nous dit qu'il  faut s'arrêter de chercher  ssi l'option a
une valeur supérieure à un certain seuil.
Ce seuil varie en fonction du nb d'options restants à considérer.

Pex, dans le cas du problème du secrétaire, supposons que chaque candidat vienne
avec le résultat d'un test de frappe mesurant à quel centile il appartient.
Un candidat appartenant au 95e centile se présente.
On sait qu'il est + rapide que 95% de la population des dactylos.
La probabilité  que l'un des  n prochains candidats soit  plus rapide est:   1 -
(19/20)ⁿ Si  le nb de  candidats n est suffisamment  grand (≥14) pour  que cette
proba soit ≥ .5, on devrait continuer à chercher:

        1 - (19/20)ⁿ ≥ .5
        (19/20)ⁿ     ≤ .5
        n*ln(19/20)  ≤ ln(.5)
        n            ≥ ln(.5)/ln(.95) ≈ 13.5

Plus  généralement, la  probabilité qu'un  futur  candidat se  présente et  soit
au-dessus d'un certain seuil s, est:  `1 - sⁿ`.
On a intérêt à continuer à chercher ssi cette proba ≥ .5:

        1 -  sⁿ     ≥    .5
             sⁿ     ≤    .5
        n*ln(s)     ≤    ln(.5)
          ln(s)     ≤    ln(.5)/n
             s      ≤    𝑒(ln(.5)/n)

Le seuil  max varie  donc en  fonction du nb  n de  candidats restant,  selon la
relation:

        sₘₐₓ = 𝑒(ln(.5)/n)

        |n  |  sₘₐₓ  |
        |---|--------|
        |1  |  .5    |
        |---|--------|
        |2  |  .70   |
        |---|--------|
        |3  |  .79   |
        |---|--------|
        |4  |  .84   |
        |---|--------|
        |5  |  .87   |
        |---|--------|
        |6  |  .89   |
        |---|--------|
        |7  |  .91   |
        |---|--------|
        |8  |  .92   |
        |---|--------|
        |9  |  .93   |


En respectant la  règle du seuil, la probabilité de  choisir la meilleure option
est de 58%.
On remarque que la règle du seuil  offre un meilleur pourcentage de réussite que
la règle des 37%.

L'enseignement à en tirer est qu'il y a plus de chances de trouver ce qu'on veut
en se basant  sur un critère objectif  (ex: revenu en terme  de centile), plutôt
que subjectif (ex: "amour").
En effet, ce dernier nécessite de  passer par une phase de calibrage/'look' plus
ou moins  longue, pendant laquelle  on risque de passer  à côté de  la meilleure
option.

#
##
##
# Principles
## Cohérence

Qd on  crée une nouvelle fonctionnalité,  fais la se comporter  comme celles qui
existent déjà; n'ajoute pas d'incohérence.

Exemple:

    :mksession file
    échoue car `:mksession` refuse d'écraser un fichier existant~

    :STrack file
    échoue car on copie le comportement de `:mksession`~

---

Toujours nommer  un wrapper autour  d'une commande/fonction exactement  comme la
commande/fonction d'origine.

Si on ne respecte  pas cette règle, on va introduire de  la confusion dans notre
esprit.

Mauvais exemple:

        " ✘
        fu! s:get_qfl()
            return b:qf_is_loclist ? getloclist(0) : getqflist()
        endfu

À force de lire le nom du wrapper, on va oublier le nom de la fonction d'origine.
Agaçant qd on veux lire sa documentation (:h ???).

Bon exemple:

        " ✔
        fu! s:getqflist()
            return b:qf_is_loclist ? getloclist(0) : getqflist()
        endfu

## Design

> Conçoit l'architecture, nomme les composants, documente les détails.

L'algo doit être compréhensible par son architecture.
Les composants (variables, fonctions, ...) par leurs noms.
Les détails par leur documentation.

L'algo doit être le plus clair, simple et logique possible (donc pensé en amont).
Les variables, fonctions... doivent avoir des noms évocateurs.
Seuls les détails doivent être documentés.

## Explicit the issue and the hypotheses

When you have an issue hard to debug:

   1. create a MWE

   2. write explicitly and succinctly the nature of the issue

      Example: sometimes  nested matches in  a Vim  syntax plugin don't  work as
      expected

   3. write explicitly and succinctly some hypotheses which may explain the issue

      Example: it's because the text is multi-line

   4. test each hypothesis by modifying the MWE

      Example: join all the lines, and see whether the issue disappears

Writing the issue is important because it helps you stay focused.

Indeed, while debugging the original issue A, you may find another issue B.
You may end up conflating them, which will make the debugging harder.
And B may distract you from A.
Note B somewhere, but stay focused on A.

You may switch to B later, if A is too hard.
Everything is possible:

   - solving A may fix B

   - solving B may fix A

   - A and B may have nothing in common

Writing the hypotheses is important because it  helps you focus on one idea at a
time, and find  good experiments (modifications of the MWE)  which will make you
gain some insight.
OTOH, having multiple ideas in mind  at the same time, and experimenting blindly
will make you lose time.

Not all experiments have the same value.
Hypotheses help you find the most interesting ones quicker.

## Éviter les non-dits / mensonges

> Expliciter clairement ce qu'on veut, et ce qu'on sait.

Si on n'explique pas clairement:

   - ce qu'on  veut, on risque de perdre  du temps à développer un  code qui ne
     correspond pas totalement à nos attentes

   - ce qu'on sait, on risque de développer un code “faible“, pour lequel le pb
     sera beaucoup plus complexe qu'il ne pourrait l'être

     Toute information pertinente dans le cadre de la résolution d'un pb devrait
     avoir sa traduction formelle dans le code qu'on écrit.
     Qu'elle fasse partie de la catégorie “objectifs“, ou “connaissances“.


> Synthétiser l'objectif d'une fonction en une simple phrase, et le noter à son début.

Utile qd l'écriture d'une fonction ou son refactoring devient trop difficile.

Cet  effort de  synthèse permet  de gagner  en compréhension,  et facilite  tout
raisonnement autour d'un pb qu'on rencontre avec la fonction.


> Le nom d'une fonction (ou variable) ne doit pas mentir.
> Son objectif non plus.

À force de manipuler le code d'une  fonction, pour corriger des bugs ou apporter
des fonctionnalités, son objectif peut changer de manière significative.

Il faut toujours veiller à ce que  son nom, autrefois pertinent, ne devienne pas
mensonger.
Idem pour son objectif noté en commentaire à son début.

## Efficacité

> Dans une boucle, ne jamais tester la valeur d'une expression qui ne dépend pas
> de la variable d'itération.

Pk?
Parce que c'est inefficace.
On répète  le même  test, dans  chaque itération, alors  qu'on avait  la réponse
avant même d'entrer dans la boucle.
De plus, ça rend sans doute le code moins lisible.

## Interference

A program always reads a main configuration file.
For example, Vim reads `~/.vim/vimrc`.
But a program can also read optional configuration files.
For example, Vim can also read `~/.vim/after/plugin/*.vim`.

Those can interfere when you debug some issue.
But you may have forgotten about them.
Or you may not want to disable each of them by writing some statement in their file.
This is why you should be able to disable them through some option/variable.

It's easier to remember a simple variable like `g:no_plugin` than a set of 10 or
more files.
You can include it inside a debugging snippet to be frequently exposed to it.
And if  creating the  variable fixes  your issue, but  you don't  remember which
files are affected by it, you can easily grep it to locate them.

Bottom line: you should be able to disable any *optional* configuration file.
It will help you debug your issues faster.

## Lisibilité

> Écrire une fonction `main()` la plus lisible possible.

Généralement,  un  élément d'interface  (commande,  mapping,  ...) commence  par
appeler une fonction;  appelons cette dernière `main()`; elle doit  être le plus
lisible possible:

   - pour chaque tâche qu'elle réalise, pas trop de lignes, et pas trop de
     complexité

   - pour chaque tâche qu'elle réalise, un commentaire expliquant ce qu'on fait
     ou pourquoi on le fait

     On préfèrera expliquer le “pourquoi” plutôt que le “quoi”.
     Exception: si  la tâche correspond  exactement à l'objectif de  la fonction
     principale, on devra expliquer le “quoi”.

   - si elle doit exécuter une tâche complexe, l'encapsuler dans une
     sous-fonction au nom évocateur

## Récursion

Qd on doit résoudre un problème impliquant un nombre variable de données, utiliser l'algo suivant:

   1. écrire une fonction `f()` acceptant un nombre variable d'arguments

   2. à l'intérieur, tester le nombre d'arguments reçus

   3. si c'est 2, écrire le code pour obtenir le résultat désiré

           g(donnée1,donnée2)

   4. si c'est plus que 2, décomposer le calcul de la façon suivante:

           g(donnée1, f(données restantes))
           ^
           Remarque1:

      Cette fonction `g()` sera identique  à la fonction `g()` dans l'étape
      précédente, ssi, `f(a,b)` a le même type et la même structure que `a`
      et `b`.

       Pour un exemple, où `g()` est différente lire:

             ~/.vim/plugged/vim-hydra/autoload/hydra.vim
            /s:all_combinations()

       Et pour rappel:

              - 1 et 'one'  n'ont pas le même type
                            (nombre vs chaîne)

              - [1,2] et ['one', 'two']  n'ont pas la même structure
                                         (liste de nombres vs liste de chaînes)

      Remarque2:

      En  VimL, cette  étape requiert  `a:000`  pour extraire  la liste  de
      données restantes, et `call()` pour déballer cette dernière et passer
      son contenu à `f()` en tant qu'arguments positionnels.

      Plus généralement, selon le language  utilisé (bash, python, ...), on
      aura besoin de constructions différentes (idiomatiques).

      Alternative:
      On peut aussi  écrire une fonction `f()` dont  la signature n'accepte
      qu'un seul argument de type liste.

      Dans ce cas, on n'a pas besoin de déballer les données restantes.
      En revanche, on aura toujours besoin de les extraire (a:list[1:]), et
      initialement on peut avoir besoin de les emballer en une liste.


   Exemple:

          com! -nargs=+ Prod echo s:product(<f-args>)
          fu! s:product(...) abort
              return a:0 == 2
              \?         a:1 * a:2
              \:         a:1 * call('s:product', a:000[1:])
              "                │                 ├───────┘
              "                │                 └ extraire les données restantes
              "                └ déballer les données restantes
          endfu

   Alternative:

                                              ┌ nécessaire pour emballer les données dans une liste
                                              ├────────┐
            com! -nargs=+ Prod echo s:product([<f-args>])
            fu! s:product(numbers) abort
                return len(a:numbers) == 2
                \?         a:numbers[0] * a:numbers[1]
                \:         a:numbers[0] * s:product(a:numbers[1:])
                "                                   ├───────────┘
                "                                   └ extraire les données restantes
            endfu

## Réutiliser et composer des concepts

> Re-use and composition  of concepts multiplies the utility  of those concepts;
> if a plugin does not reuse a concept, both that concept and the new, redundant
> mechanism are made mutually  less valuable — the sum is less  than the parts —
> because the user  now must learn or choose from  two slightly different things
> instead of one augmented system.

Source: :h dirvish

Pour être efficace dans un environnement donné, il faut réutiliser un maximum de
concepts propres à cet environnement, et les composer entre eux.
Ainsi, leur effet est démultiplié, et on rentabilise leur coût d'assimilation.

Si  on ignore  ce principe,  on risque  de réinventer  la roue,  et de  créer de
nouveaux concepts/ mécanismes, qu'il va falloir assimiler.
La valeur  des anciens concepts n'est  pas augmentée, et celle  des nouveaux est
probablement faible.

De ce principe découle aussi tout l'intérêt de la cohérence et l'harmonie.
Pex, raccourcis identiques d'un pgm à l'autre pour des fonctions similaires.

## Séparation des problèmes

> Dans une fonction utilitaire, respecter la séparation des problèmes.

À chaque fois qu'on appelle une fonction  B au sein d'une fonction utilitaire A,
se demander si elle a un lien direct avec l'objectif de A.
Si la réponse est non, l'appeler depuis:

   - la fonction principale

   - une nouvelle fonction utilitaire elle-même appelée depuis la fonction
     principale

## Simplifier la complexité

Comment gérer un environnement complexe influencé par plusieurs degrés de liberté ?

L'état de l'environnement dans lequel un  algo doit travailler peut être modifié
par plusieurs paramètres; on parle de degrés de liberté.

Chaque paramètre (pᵢ) peut prendre plusieurs (eᵢ) valeurs.
Le nombre total  d'états possibles de l'environnement, E, est  inférieur ou égal
au produit des nombres de valeurs:

        E ≤ Π eᵢ

Il ne faut pas faire l'erreur de penser que:

        E = Π eᵢ

En effet, certains arrangements de valeurs peuvent être impossibles.
Pex,  dans   notre  plugin   `vim-session`,  2  paramètres   peuvent  influencer
l'indicateur dans la statusline:

   - le chargement d'une session  (a eu lieu ou pas)
   - le tracking d'une session    (a lieu ou pas)

Chacun de ces paramètres peut avoir 2 valeurs `on`, `off`.
On pourrait donc penser que E = 4.
Mais il est impossible qu'une session soit trackée sans qu'au préalable elle ait
été chargée; donc:

    E = 4 - 1 = 3

---

Comment accélérer la résolution d'un pb complexe ?

Le transformer en:

   - le décomposant en pbs plus simples (le faire péter)
   - cherchant un pb équivalent qui, lui, est plus simple
   - cherchant un pb plus fondamental (*)

(\*) En  effet, un pb  complexe peut être la  conséquence d'un pb  plus général,
qui, lui, est plus simple.

Pex,  si  un  pgm  a  un  comportement  incohérent  (tantôt  prévisible,  tantôt
incompréhensible),  plutôt  que de  chercher  à  comprendre chaque  comportement
individuel, il vaut mieux  d'abord tenter de trouver un état  dans lequel le pgm
fonctionne correctement, puis trouver le minimum de modifications à lui apporter
pour qu'il perde sa cohérence.

La cause de ce minimum de modification constitue un nouveau pb.
Ce dernier peut être beaucoup plus simple.
Le résoudre  peut permettre  de réparer  plusieurs bugs  en apparence  sans lien
entre eux.

---

Il faut aussi chercher à échouer le plus vite possible.
Pour ce faire, on peut créer un MWE sous la forme d'un petit script/programme.
Attention:
créer un MWE ne consiste pas simplement à supprimer un max de lignes;
parfois, qd le problème est réellement  très compliqué, il faut supprimer un max
de lignes ET un max de caractères sur celles qui restent.


Si ce dernier a besoin d'une input, on pensera à en créer une pour l'occasion.
Ainsi, on n'aura pas besoin d'en regénérer  une à chaque fois qu'on modifiera le
MWE.
Se rappeler de nos  notes à propos des compilers plugins  dans Vim (méthode pour
trouver une valeur à 'efm').

Si pendant la résolution du  problème, d'autres problèmes émergent, les résoudre
en priorité  (via un  MWE à nouveau);  il se peut  que leur  résolution facilite
celle du problème d'origine.

---

Parfois, la complexité découle de plusieurs degrés de liberté.
Dans ce cas, lire la section `Purpose` dans:

    ~/.vim/plugged/vim-hydra/plugin/hydra.vim

## Abstraction and Exposition

Every time you find an interesting (set of) command(s), create an abstraction or
an exposition.

An  abstraction can  be a  mapping,  a custom  command,  an alias,  a script,  a
function ...

An exposition can be an abbreviation,  a snippet, a semi-automatic population of
the command-line (<kbd>C-g v</kbd> in Vim)...

Contrary to an  abstraction, an exposition will constantly show  you the details
of what you're about to execute; therefore, it will:

   - help you remember the commands

   - give you a better understanding of what's important to focus on
     (especially with tabstops/placeholders)

   - give you more control

## Too many degrees of freedom

When you  have a command or  snippet of code  which can be written  in different
forms, and you're confused, ask yourself:

    “Is there a specific result which my command must achieve?”

If  the answer  is yes,  use  `vim-hydra` to  find  what are  the necessary  and
sufficient conditions to get this result.

If the answer is “no, the desired result depends on the context”, ask yourself:

    “Can my command have more than 2 forms?”

If the answer is yes, in a faq  write a question for each degree of freedom (see
the next example).
If the answer is no, ask yourself:

    “Which form is probably the less frequently used?”

Once you've found the less frequent form, `:vimgrep` it in your codebase.
Study all the occurrences written by experienced coders.
Ask yourself why they have used this form rather than the other.
That's what we did for the `-bar` attribute in Vim.

---

Example  of faq  where we  wrote a  question  for each  degree of  freedom of  a
polymorph command (here the command `:com! Cmd call Func()`):

    Which escape sequence should I use: `<args>`, `<f-args>`, `<q-args>`?

    Do I need to quote strings passed to my command with `<args>`?  `<f-args>`?  `<q-args>`?

    Do I need to use commas to separate the arguments replacing `<args>`?  `<f-args>`?  `<q-args>`?

