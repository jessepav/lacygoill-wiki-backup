# How to yank all the lines in open folds?

    qaq
    :folddoopen y A

`:folddoopen` and `:folddoclosed` are similar to `:g`.
They allow you to execute a command on  a set of lines; the lines in open folds,
or the lines in closed folds.

---

Don't conflate `:folddoopen` with `:foldopen`.

##
# Théorie, mappings

Voici les options permettant de configurer le pliage dans un fichier ou de manière générale:

    ┌──────────────────┬─────────────────────────────────────────────────────────────────────────────────┐
    │ 'debug'          │ en cas d'erreur lors de l'évaluation de 'fde' aucun message d'erreur n'est émis │
    │                  │ sauf si on donne la valeur 'msg' ou 'throw' à 'debug'                           │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldclose'      │ si sa valeur est 'all', tout pli ne contenant pas le curseur, et dont le niveau │
    │                  │ est supérieur à &l:foldlevel est automatiquement fermé                          │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldcolumn'     │ largeur de la colonne de pliage (contient les symboles -+|)                     │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldenable'     │ détermine si le pliage est activé dans la fenêtre                               │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldexpr'       │ sa valeur est une expression dont l'évaluation est le niveau de pli d'une ligne │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldignore'     │ suite de caractères                                                             │
    │                  │                                                                                 │
    │                  │ toute ligne dont le 1er caractère est dans cet ensemble hérite son niveau       │
    │                  │ d'indentation d'une ligne voisine; son niveau d'indentation est ignoré          │
    │                  │                                                                                 │
    │                  │ n'a d'effet que lorsque la méthode de pliage est 'indent'                       │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldlevel'      │ les plis dont le niveau est supérieur sont fermés par défaut                    │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldlevelstart' │ valeur par défaut de 'foldlevel'                                                │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldmarker'     │ marqueurs de début et de fin pour la méthode est 'marker'                       │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldmethod'     │ méthode de pliage                                                               │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldminlines'   │ minimum de lignes qu'un pli doit contenir                                       │
    │                  │                                                                                 │
    │                  │ un pli contenant moins de lignes ne peut pas être fermé individuellement        │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldnestmax'    │ niveau de pli maximum (on ne peut pas aller au-delà de 20)                      │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldopen'       │ liste des commandes ouvrant automatiquement un pli qd on entre dedans           │
    ├──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
    │ 'foldtext'       │ sa valeur est une expression dont l'évaluation sert de titre pour les plis      │
    └──────────────────┴─────────────────────────────────────────────────────────────────────────────────┘

Toutes les options sont locales à la fenêtre, sauf:

   - `'debug'`
   - `'foldclose'`
   - `'foldopen'`
   - `'foldlevelstart'`

---

Par défaut, `'fdm'` = manual, ce qui implique 2 choses:

   1. pour plier une section de texte, il faut le faire manuellement avec `zf`

   2. les plis ne sont pas sauvegardés au-delà de la session

      Pour les faire persister au-delà d'une session, il faut utiliser `:mkview`
      et `:loadview`, via une autocmd.

`'foldmethod'` peut prendre 5 autres valeurs:

    ┌────────┬──────────────────────────────────────────────────────────────┐
    │ diff   │ utilisée dans les fenêtres diff pour plier le texte inchangé │
    ├────────┼──────────────────────────────────────────────────────────────┤
    │ expr   │ le pliage est configuré par une expression (méthode avancée) │
    ├────────┼──────────────────────────────────────────────────────────────┤
    │ indent │ plis basés sur le niveau d'indentation                       │
    ├────────┼──────────────────────────────────────────────────────────────┤
    │ marker │ plis basés sur des marqueurs présents au sein du texte,      │
    │        │ souvent dans des commentaires:    {{{                        │
    ├────────┼──────────────────────────────────────────────────────────────┤
    │ syntax │ plis basés sur la syntaxe; ex: pliage des blocs de code      │
    └────────┴──────────────────────────────────────────────────────────────┘

---

Qd on  utilise la  méthode `'indent'`,  les lignes  commençant par  un caractère
présent dans la  valeur `'foldignore'` prennent comme niveau de  pli celui de la
prochaine ou précédente ligne; le plus petit des 2.
Leur niveau d'indentation est ignoré, d'où le nom de l'option.

---

Qd on utilise la méthode `'expr'`, voici les règles à retenir:

   - chaque ligne du buffer a un niveau de pliage, positif ou nul

   - l'expression donnée comme valeur à `'fde'` est évaluée dans le contexte:

       * du buffer courant
       * la fenêtre courante
       * la ligne dont l'addresse est `v:lnum`

   - l'évaluation de cette expression détermine le niveau de chaque ligne;
     elle peut prendre pour valeur:

    ┌───────────────┬────────────────────────────────────────────────────────────────────────┐
    │ 0             │ la ligne n'est pas dans un pli                                         │
    ├───────────────┼────────────────────────────────────────────────────────────────────────┤
    │ -1            │ le niveau est indéfini;                                                │
    │               │ Vim doit utiliser le niveau de la ligne voisine la plus proche,        │
    │               │ celle dont le niveau est le plus petit                                 │
    ├───────────────┼────────────────────────────────────────────────────────────────────────┤
    │   1,    2,  … │ la ligne est dans un pli de ce niveau                                  │
    │ '>1', '>2', … │ idem mais en plus la ligne est la 1e       d'un pli                    │
    │ '<1', '<2', … │ idem "                            dernière d'un pli                    │
    ├───────────────┼────────────────────────────────────────────────────────────────────────┤
    │ 'a1', 'a2', … │ [a]jouter/[s]oustraire 1, 2, … au niveau de la ligne précédente,       │
    │ 's1', 's2', … │ et utiliser le résultat pour la ligne courante                         │
    └───────────────┴────────────────────────────────────────────────────────────────────────┘

   - qd une ligne a le même niveau que la suivante, toutes 2 sont rangées dans un même pli

   - qd une ligne a un niveau supérieur à la précédente, elle débute un nouveau pli; ex:

           a
               b
               c
                   d    ← niveau 2, et la précédente a pour niveau 1 = début d'un pli
                   e
               f
           g

     corollaire:
     il n'est pas nécessaire de lui donner pour niveau `'>N'`, `'N'` suffit

   - qd une ligne a un niveau supérieur à la suivante, elle termine le pli
     courant; ex:

           a
               b
               c
                   d
                   e    ← niveau 2, et la suivante a pour niveau 1 = fin d'un pli
               f
           g

     corollaire:
     il n'est pas nécessaire de lui donner pour niveau `'<N'`, `'N'` suffit

   - qd une ligne a un niveau N, toutes les lignes suivantes de niveau supérieur
     sont incluses dans le même pli (jusqu'à atteindre une ligne de niveau
     inférieur)

---

Le  pliage automatique  (toute  méthode  différente de  manual  et marker)  peut
entraîner  des  ralentissements, en  particulier  en  mode insertion  (pour  une
solution voir plugin `FastFold`).

---

    :10,20fold

Plie les lignes 10 à 20.

`:fold` est l'équivalent en mode Ex de la commande normale `zf`.

---

    za
    zA

Toggle:

   - le pli courant
   - le pli courant et tous ses parents / enfants

N'affecte pas `'fdl'`.

---

    zc
    zC

Ferme:

   - le pli courant s'il est ouvert ou son parent s'il est fermé
   - tous les plis dans lequel se trouve le curseur

En répétant `zc`, on peut  fermer toute une hiérarchie de plis.
`za` se contenterait d'ouvrir / fermer le même pli.

N'affecte pas `'fdl'`.

---

    zd
    zD
    zE

Supprime:

   - le pli contenant la ligne où se trouve le curseur
   - tous les plis contenant la ligne où se trouve le curseur
   - tous les plis du buffer (Eliminate)

Ne fonctionne que si la méthode de pliage est `manual` ou `marker`.

---

    zfap
    zfaB

Plie:

   - le paragraphe
   - le texte entre les accolades

---

    zn
    zN
    zi

Modifie l'option `'foldenable'`:

   - désactivaction
   - activation
   - toggling

`'fen'` est très utile pour temporairement désactiver les plis avant de déplacer
une/des ligne(s), via `:move`.
En effet, un bug  introduit dans le patch 7.4.700 a pour effet  de fermer le pli
dans lequel on déplace une ligne.
Ceci peut avoir des effets inattendus sur les commandes suivantes (ex: `norm!
==`).

---

Se déplacer vers:

    ┌────┬───────────────────────────────────────────────────────────────────────┐
    │ [z │ la précédente fin de pli  peu importe son niveau                      │
    ├────┼───────────────────────────────────────────────────────────────────────┤
    │ ]z │ le prochain   début de pli "                                          │
    ├────┼───────────────────────────────────────────────────────────────────────┤
    │ [Z │ le précédent  début de pli de niveau supérieur ou égal au pli courant │
    ├────┼───────────────────────────────────────────────────────────────────────┤
    │ ]Z │ la prochaine  fin de pli   "                                          │
    └────┴───────────────────────────────────────────────────────────────────────┘

Ce sont des mappings custom; par défaut Vim utilise:

   - zj
   - zk
   - [z
   - ]z

---

    zm
    zM

Altère la valeur de l'option `'foldlevel'`, en la:

   - décrémentant d'un
   - faisant passer à 0

Les plis dont le niveau est supérieur à `&l:fdl` sont fermés.
Donc, `zm` ferme un peu plus de plis, tandis que `zM` les ferme tous.

---

    zr
    zR

Altère la valeur de l'option `'foldlevel'`, en:

   - l'incrémentant d'un
   - la faisant passer à `niveau de plis max`

`zr` ouvre un peu plus de plis, tandis que `zR` les ouvre tous.

---

    zo
    zO

Ouvre:

   - un pli           dans lequel se trouve le curseur
   - tous les plis    "

Si le curseur  se trouve dans une  imbrication de plis, `zo` n'ouvre  que le pli
fermé le plus haut dans la hiérarchie.
`zO` ouvre toute la hiérarchie.

N'affecte pas `'fdl'`.

# Configuration

    setl foldlevel=3

Définit 3 comme étant le niveau max d'imbrication pour un pli ouvert.
Au-delà de ce niveau, un pli est fermé.

La valeur de cette option est modifiée par:

   - zm
   - zM
   - zr
   - zR

Mais pas par:

   - za
   - zA
   - zc
   - zC
   - zo
   - zO
   - zv

Une commande  normale qui  altère simplement l'état  d'un pli  (ouvert/fermé) ne
change pas `'fdl'`.
Seule les commandes qui altèrent l'ensemble des plis affectent `'fdl'`.

---

`'foldlevel'` est locale à une fenêtre comme la plupart des options de pliage.

Ne pas la confondre avec `'foldlevelstart'` qui elle est globale.
Cette dernière configure la valeur  initiale de `'foldlevel'` dans toute fenêtre
où un nouveau buffer est édité.

---

    set fcs=vert:\|,fold:-

Définit le séparateur vertical (celui affiché  dans la barre séparant 2 fenêtres
après un `:vs`) comme étant `|`, et  le caractère de remplissage sur la 1e ligne
d'un pli comme étant `-`.

Il  faut échapper  le pipe  pour  éviter que  `:set` ne  l'interprète comme  une
terminaison de commande.

Il s'agit en fait de la valeur par défaut de fillchars.
`'fillchars'` permet aussi de configurer d'autres caractères de remplissage.

