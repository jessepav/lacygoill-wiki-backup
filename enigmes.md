# VOCA

    incompossible

            Se dit de 2 êtres / choses qui ne peuvent exister simultanément.
            Qui se détruit réciproquement.


    interrogation totale / partielle

            Une interrogation:

                    - totale est une question qui porte sur l'ensemble d'une phrase
                    - partielle est une question qui porte sur une partie d'une phrase

            On ne peut répondre à une question totale que par oui ou par non.


# PRINCIPES

    Formaliser l'objectif AVANT l'énoncé.

    ET à partir de l'objectif formalisé, remonter dans le raisonnement aussi loin que possible,
    par équivalences successives.

            Dans le pb du barbier de Seville, on a perdu bcp de temps, car on a tout de suite
            formalisé l'énoncé, en pensant que la solution émergerait naturellement des formules.

            De plus, nos formules étaient de mauvaise qualité, car trop complexe.
            Elles pouvaient s'exprimer sous une forme bien plus simple.
            Cette trop grande complexité nous a fait perdre du temps.

            D'un objectif clair découle une bonne compréhension de l'énoncé et des formules simples:

                    trouver ce qu'il faut démontrer ⇒ bonne compréhension de l'énoncé ⇒ formules simples


    Pour trouver une info avec une seule question, alors qu'on est confronté à une situation variable,
    la question doit elle-même contenir un mot variable.

            Ce peut être "Je", "Vous", "Ceci/Cela", "maintenant"…

            Tous ces mots peuvent être interprétés différemment selon le contexte.
            Aucun n'est absolu.  Ils sont donc tous variables.

            On a découvert ce principe à l'occasion d'une énigme où il fallait trouver la bonne route
            pour arriver à destination d'une ville, en interrogeant une personne qui dit tjrs la vérité,
            ou qui ment tjrs.


# FORMULES

        A ⇒ B ⇔ ¬(A ∧ ¬B)

            (1) "A implique B" est vrai, ssi, "A implique B" n'est pas faux.
            (2) "A implique B" est faux, ssi, "A est vrai et B est faux" est vrai.

            (1) ∧ (2):

                    "A implique B" est vrai, ssi, "A est vrai et B est faux" n'est pas vrai.

            En français:

            une implication est vraie, ssi, elle N'est PAS (¬(...)) fausse (A ∧ ¬B).


# CHEVALIERS ET DOMESTIQUES
## île déserte

Imaginez une île où les seuls habitants sont des chevaliers et des domestiques.
Les chevaliers disent toujours la vérité, mais les domestiques disent tjrs des mensonges.

Vous rencontrez 3 habitants, A, B et C.
Vous demandez à A s'il est un chevalier ou un domestique.
A marmonne une réponse incompréhensible.
Vous demandez à B ce que A a dit.

B répond:        "Il a dit qu'il était un domestique"
C intervient:    "B ment !"

Que pouvez-vous dire sur A, B et C ?

        Réponse:

        B ment, car aucun habitant ne pourrait dire "Je suis un domestique".
        Donc B est un domestique.
        Donc C a dit la vérité, et C est un chevalier.

        On ne peut rien dire à propos de A.  Il a forcément dit "Je suis un chevalier", mais
        rien ne garantit qu'il a dit la vérité.


## le récit de Fernando

Vous rencontrez un jour un voyageur, Fernando, qui affirme avoir été dans une ville appelée Lem,
où ne vivent que des chevaliers et des domestiques.
Il raconte y avoir rencontré 2 habitants, A et B, et avoir demandé à A:
"Est-ce qu'au moins l'un d'entre vous est un chevalier ?"

Après avoir entendu la réponse, le voyageur sut immédiatement ce qu'était chacun d'eux.

Quelle fut la réponse donnée au voyageur, et qu'étaient A et B ?

Réponse:

        Si la réponse avait été "oui", alors Fernando n'aurait pas pu en déduire l'identité des
        2 habitants.
        La réponse à sa question fut donc "non".

        Répondre "non" revient à dire que ni A ni B n'est un chevalier.
        Un chevalier ne pourrait donc pas répondre "non", car il mentirait.
        A est donc un domestique.

        Comme A est un domestique, sa réponse, "non", est fausse.
        L'un deux est donc un chevalier.
        Donc, B est un chevalier.


## la ville de Lem

Un jour, le célèbre logicien L.N. Cornelius voyagea dans la ville de Lem.
Il arrêta toutes les paires d'habitants A et B possibles au sein de la ville.
À chaque fois, il demanda à A:

        "Est-ce que B est un chevalier ?"

… et à B:

        "Est-ce que A est un chevalier ?"

Quelle(s) relations existe(nt)-t-il entre la réponse de A et celle de B ?
Exemples de relations possibles:

        les réponses seront tjrs les mêmes, OU, tjrs différentes
        parfois elles seront pareilles et parfois différentes

En fonction de la relation entre leurs réponses, quelle information L. N. Cornelius peut-il en déduire ?

        Réponse:

        On a 3 types de paires d'habitants possibles, et donc 3 paires de réponses possibles:

                chevalier  - chevalier
                oui + oui˜
                domestique - domestique
                oui + oui˜
                chevalier  - domestique
                non + non˜

        On s'aperçoit que:

                - A et B donneront tjrs la même réponse
                - si A et B sont identiques, ils répondront "oui"
                - si A et B sont différents, ils répondront "non"


## un guide de Lem qui laisse perplexe

Un jour, vous vous rendez dans la ville de Lem.
Vous organisez une visite qui doit être dirigée par un guide.
Au moment de retrouver votre guide pour démarrer la visite, vous tombez sur 2 habitants de Lem, A et B.
A dit:
        "Votre guide est un chevalier."

B dit:
        "Votre guide est un domestique."

Qui est votre guide, A ou B ?

        Réponse:

        Le guide est soit un chevalier, soit un domestique.

        S'il est un chevalier, alors A dit la vérité et B ment.
        Donc, A est un chevalier et B un domestique.
        Donc, A est votre guide.

        S'il est un domestique, alors A ment et B dit la vérité.
        Donc, A est un domestique et B un chevalier.
        Donc, A est votre guide.

        Dans les 2 cas, votre guide est A.


## comment gravir l'échelle sociale dans Lem


Les habitants de Lem se distinguent par leur:

        - statut      (domestique vs chevalier)
        - rang social (riche vs pauvre)

La ville de Lem se décompose donc en 4 catégories d'habitants:

        ┌──────┬──────┬──────┬──────┐
        │      │      │      │      │    H = chevalier
        │  M   │  M   │  H   │  H   │    M = domestique
        │  P   │  R   │  R   │  P   │    R = riche
        │      │      │      │      │    P = pauvre
        └──────┴──────┴──────┴──────┘


Il est interdit de révéler son statut ou son rang que ce soit par la parole, ou en portant un signe
distinctif.

Vous êtes:

        - une fille domestique et riche
        - une fille qui souhaite épouser un garçon bien précis
        - tous les 2, vous êtes des habitants de Lem

La famille du garçon veut qu'il épouse une riche domestique.
Vous trouvez le moyen d'organiser une rencontre avec la famille pendant 1 minute.

Quelle phrase pouvez-vous prononcer qui les convaincrait que vous êtes une riche domestique ?

        Réponse:

                "Je suis une pauvre domestique"

        À partir de cette phrase, la famille peut déduire que:

                1. vous n'êtes pas une chevalière

                    En effet, une chevalière qui prononcerait cette phrase mentirait,
                    ce qui est impossible.

                2. vous êtes donc effectivement une domestique

                3. vous mentez, car vous êtes une domestique

                4. vous n'êtes donc pas pauvre mais riche


        L'enseignement à retirer de cette énigme est qu'un ensemble de propositions connectées
        par l'opérateur logique ET est:

                - faux ssi UNE SEULE des propositions est  fausse
                - vrai ssi TOUTES    les propositions sont vraies

        Ainsi, même si vous êtes bien une domestique, et que vous devez donc mentir, vous pouvez
        malgré tout dire une vérité ("je suis une domestique"), à condition de l'accompangner d'un
        mensonge ("ET je suis pauvre").


Même question si vous êtes un garçon qui souhaite épouser une fille dont la famille veut qu'elle
épouse un chevalier riche.
Que pouvez-vous dire pour convaincre que vous êtes un chevalier riche (sachant que vous en êtes
réellement un)?

        Réponse:

                "Je ne suis pas un chevalier pauvre."

        À partir de cette phrase, la famille peut déduire que:

                1. vous êtes un chevalier

                    En effet, cette phrase est une vérité pour tout domestique, peu importe son rang.
                    Aucun domestique ne pourrait donc la prononcer.

                2. donc vous dites la vérité

                3. donc vous n'êtes pas pauvre (car c'est ce que vous dites)

                4. donc vous êtes riche

        Pour mieux comprendre, se référer au diagramme du début.


## les sociétés secrètes de Lem

Vous faites partie d'une société secrète visant à changer les mœurs au sein de la ville de Lem.
Vous buvez un café dans un bar.

Un client vous aborde en vous disant que lui-aussi fait partie de la société secrète.
Vous ne savez pas s'il dit la vérité, ou s'il ment et qu'il s'agit en fait d'un agent secret du gvt.

Le serveur du bar le connaît.
Vous ne savez pas si le serveur est un domestique ou un chevalier.

Quelle question pouvez-vous poser au serveur pour identifier le statut du client ?

        Réponse:

        Il peut y avoir 4 situations différentes:

                   ┌─────────┬────────┬──────────┬─────────┐
                   │ serveur │ client │ question │ réponse │
                   ├─────────┼────────┼──────────┼─────────┤
                   │ H       │ H      │    ?     │   X     │  H = cHevalier
                   │ M       │ H      │    ?     │   X     │  M = doMestique
                   │ H       │ M      │    ?     │   Y     │
                   │ M       │ M      │    ?     │   Y     │
                   └─────────┴────────┴──────────┴─────────┘


        On ne peut pas directement demander au serveur le statut du client, car on ne peut pas
        lui faire confiance.
        Il faut donc trouver une question (?), dont la réponse (X ou Y) pourra être associée au statut
        du client.
        IOW, il faut que la réponse change en fonction du statut du client, mais pas en fonction
        du statut du serveur.

        La question:

                "Avez-vous tous les 2 le même statut ?"

        … satisfait à cette condition.

        En effet, peu importe le statut du serveur, si le client est un:

                - chevalier,  alors le serveur répondra tjrs "oui" (X)
                - domestique, "                              "non" (Y)


## révolution dans Lem

Une révolution a eu lieue dans la ville de Lem.
Désormais, en plus des chevaliers et des domestiques, les gens ordinaires sont autorisés à vivre
dans Lem.
Un ordinaire n'est pas obligé de dire la vérité ou de mentir, il peut faire ce qu'il veut.

Un crime a eu lieu pendant la révolution, et vous êtes suspecté.
Vous devez passer devant un jury pour être jugé.
Le jury sait que le criminel est un domestique.
Vous êtes un domestique, mais vous êtes innocent du crime pour lequel vous êtes jugé.

Quelle déclaration pouvez-vous prononcer qui convaincrait le jury de votre innocence ?

        Réponse:

                "Je suis coupable."

        Le jury sait que vous êtes soit chevalier, soit domestique, soit ordinaire.

        Un chevalier ne peut pas dire qu'il est coupable, car ce serait un mensonge.
        En effet, on sait que le coupable est un domestique.

        Un ordinaire ou un domestique pourrait dire "Je suis coupable".
        Mais dans les 2 cas, ils mentiraient (pour des raisons différentes).

        Un ordinaire disant "Je suis coupable" mentirait car ça contredit l'information rapportant
        que le criminel est un domestique.
        Un domestique mentirait par simple définition.

        Donc, le jury peut déduire que vous mentez qd vous dites être coupable, sans savoir si vous
        êtes un domestique ou un ordinaire.

Même question, si vous êtes un chevalier suspecté à tort du crime, et que le jury sait que le criminel
est un chevalier.

        Réponse:

                "Je ne suis pas coupable"

        Le coupable est un chevalier, donc un domestique disant "Je ne suis pas coupable" dirait la vérité.
        C'est impossible par définition, donc le jury sait que vous n'êtes pas un domestique.

        Vous êtes soit un ordinaire, soit un chevalier.

        Si vous êtes un ordinaire, vous n'êtes pas coupable, car le coupable est un chevalier.
        Si vous êtes un chevalier, vous dites la vérité par définition, donc vous êtes innocent.


## l'avocat de Lem

Vous êtes un avocat.
Votre client est suspecté d'un crime, pour lequel vous savez qu'il est innocent.
Vous ne connaissez pas le statut de votre client: il peut être un chevalier, un domestique ou un ordinaire.

Le jury sait que le criminel n'est pas un ordinaire.

Quelle phrase pourriez-vous conseiller à votre client, qui convaincrait le jury de son innocence
et qu'il pourrait prononcer peu importe son statut ?

        Réponse:

        1. Il faut que ce soit une vérité pour un chevalier, mais un mensonge pour le domestique.
        2. Il faut que ça prouve l'innocence du client.

        La condition 1. implique que le fait à énoncer doit être perçu différemment du point de vue
        d'un chevalier ou d'un domestique.  Il faut donc qu'il contienne un élément variable.
        Le pronom "Je" est un élément variable, car il ne désigne pas la même chose selon la personne
        qui le prononce.
        On devrait sans doute conseiller à notre client de dire qch à propos de lui-même.

        La condition 2. implique que le client doit parler de son innocence ou de sa culpabilité.
        En effet, il n'existe que 2 moyens de prouver son innocence:

                - parler de son innocence/culpabilité
                - dire qu'on est un ordinaire

        On ne connaît pas le statut de notre client, il se peut donc qu'il s'agisse d'un chevalier.
        Et un chevalier ne peut pas mentir en disant qu'il est un ordinaire.

        Après avoir tenté différentes phrases tq "Je suis un innocent chevalier", ou "Je ne suis pas un
        coupable domestique", on se rend vite compte qu'aucune simple proposition ne peut suffire.
        Il faut donc vraisemblablement une conjonction de plusieurs propositions.
        En cherchant un peu, on trouve:

                "Je suis un innocent chevalier OU un coupable domestique"

        Cette phrase peut être prononcée par n'importe quel client, peu importe son statut.
        De plus, on peut en déduire que notre client est innocent qu'il soit un:

                - ordinaire   car on sait que le coupable n'est pas un ordinaire

                - chevalier   car il dit la vérité et qu'il ne peut pas être un coupable domestique.
                                Il est donc un innocent chevalier.

                - domestique  car il ment, il n'est donc ni un innocent chevalier (évident),
                                ni un coupable domestique.  Il est donc un innocent domestique.


## le maire de Lem

Vous êtes un ordinaire et souhaitez être candidat au poste de maire.
Seul un ordinaire a le droit de se présenter à l'élection.
Vous devez prononcer une phrase qui prouve que vous êtes un ordinaire, mais pesonne ne doit savoir
si ce que vous dites est vrai ou faux.

Quelle phrase pouvez-vous prononcer pour devenir candidat à l'élection ?

        Réponse:

        La phrase doit être:

                - un mensonge             pour un chevalier
                - une vérité              pour un domestique
                - de véracité inconnue    pour un ordinaire


        Donc, pour la même raison que dans l'énigme ’avocat’, il est probable que la phrase contienne
        le pronom "Je".

        On trouve rapidement la phrase suivante:

                "Je suis un domestique"    ✘

        Un chevalier  ne peut pas prononcer cette phrase, car il mentirait.
        Un domestique "                                          dirait la vérité.

        Pb:
        on déduit de cette phrase que vous êtes un ordinaire et donc que vous mentez.
        Or, personne ne doit savoir si vous mentez ou dites la vérité.

        Il faut trouver une phrase similaire, mais qui en dit moins sur vous.
        Dire "Je suis un domestique" équivaut à dire "Je mens TOUJOURS".
        Il faudrait une phrase se rapprochant de "Je vais mentir UNE fois":

                "Si vous me posez une question, je vous répondrai par un mensonge"


        Autres réponses possibles:

                "Cette phrase est fausse"
                "Je suis un domestique OU un ordinaire qui a pris une douche ce matin"

        La 1e phrase ne peut être prononcée ni par un chevalier, ni par un domestique car il s'agit
        d'un paradoxe.  On peut pas dire de cette phrase qu'elle est vraie ou fausse.
        On en déduit que vous êtes un ordinaire, et on ne sait pas si vous dites la vérité ou si vous mentez.

        La 2e phrase ne peut être prononcée ni par un chevalier, ni par un domestique, à cause de la 1e
        proposition "Je suis un domestique".
        En revanche, l'ajout de la 2e proposition "OU je suis un ordinaire qui a pris une douche ce matin"
        permet de restaurer un doute quant à la véracité de la phrase.
        Personne ne sait si vous avez pris une douche ou non ce matin.


## le cabinet du maire

Vous êtes engagé comme adjoint du maire.
Ce dernier est un ordinaire et souhaite engager dans son cabinet 2 personnes, qui ne sont pas des ordinaires.
2 candidats, A et B, se présentent et vous savez qu'ils ne sont pas des ordinaires.

Le maire veut savoir quel est le statut de A et de B, avant de les engager.
La seule information dont vous disposez est le fait que A a dit:

        (S) "Si B est un chevalier, alors je suis un domestique"

Quel est le statut de A et de B ?

        Réponse:

        Une implication (P ⇒ Q) est fausse ssi son antécédent (P) est vrai, ET son conséquent (Q) est faux.

        Donc, la phrase (S) est fausse, ssi B est un chevalier et A n'est pas un domestique.
        IOW, (S) est fausse ssi A et B sont tous 2 des chevaliers.
        Or, si A et B sont des chevaliers, alors A ment, ce qui est impossible.
        Donc, l'hypothèse "(S) est fausse" est impossible: (S) est nécessairement vraie.

        Donc A est un chevalier, car il dit la vérité.

        Si B était un chevalier, alors on peut déduire de (S) que A est un domestique, ce qui est impossible.
        Donc B ne peut pas être un chevalier:    B est un domestique.


## Lnonc et Lancon

Vous êtes un ordinaire travaillant pour le maire.
Le maire a reçu l'information selon laquelle une révolution (pour rejeter les ordinaires) se préparerait
dans un quartier périphérique de la ville, au sein duquel vivrait un nombre impair de chevaliers.

Il s'agit soit du quartier ’lnonc’, soit du quartier ’lancon’.
Ces 2 quartiers ne sont peuplés que par des chevaliers et des domestiques.

Vous êtes chargés par le maire de découvrir dans quel quartier se prépare la révolution.
Vous vous rendez dans le quartier de ’lancon’ pour y interroger ses habitants.

Vous y rencontrez 3 personnes: A, B et C

A vous dit: (S1) "Un nombre pair de domestiques se trouve en ce moment à Lancon"
B vous dit: (S2) "Un nombre impair de personnes se trouve en ce moment à Lancon"
C vous dit: (S3) "Je suis un chevalier ssi A et B ont le même statut"

Où se prépare la révolution ?

Réponse:

        Supposons que C est un chevalier.
        A et B ont donc le même statut (cf. S3)

                Supposons que A et B sont des chevaliers.
                Comme ils disent tous 2 la vérité, on déduit de (S1) et (S2) qu'un nombre pair
                de chevaliers vit à Lancon.

                En effet:

                        nb de chevaliers = nb total de personnes - nb de domestiques - 1 (vous)
                                            = nb impair - nb pair - 1
                                            = nb pair

                Donc la révolution se prépare à Lnonc.

                Supposons que A et B sont des domestiques.
                Comme ils mentent tous les 2, on déduit de (S1) et (S2) la même chose que précédemment.


        Supposons que C est un domestique.
        C ment donc l'une des 2 implications suivantes est fausse:

                (I1)   C est un chevalier          ⇒   A et B ont le même statut
                (I2)   A et B ont le même statut   ⇒   C est un chevalier

        Pour rappel, une implication est fausse ssi son antécédent est vrai, mais son conséquent est faux.
        (I1) ne peut pas être fausse, car C est un domestique, par hypothèse.
        Donc (I2) doit être fausse.  Donc A et B ont le même statut.

                On aurait aussi pu se rendre compte qu'une équivalence entre 2 propositions
                signifie que ces dernières ont tjrs la même valeur de vérité.
                Donc, si C est un domestique et qu'il ment, il faut que les 2 propositions aient
                des valeurs de vérité différentes.
                Enfin, la proposition "C est un chevalier" est fausse (par hypothèse), donc
                "A et B ont le même statut" doit être vraie.

        Comme A et B ont le même statut, on en déduit à nouveau qu'un nb pair de chevaliers vit à Lancon.

        Conclusion:

        La révolution se prépare à Lnonc.


## l'inquisition de Lnonc

Une révolution a eu lieue pour chasser les ordinaires de la ville, et l'ancien maire/pouvoir a été renversé.
Vous devez être jugé lors d'un procès par 5 magistrats, A, B, C, D et E.
Les magistrats sont tous des chevaliers ou des domestiques.

Lors du procès, on vous montre 3 portes: P, Q et R.
On vous dit que l'une d'elle est sans danger, les 2 autres conduisent à la mort.

A dit: "P est la porte est sans danger"                                (S1)
B dit: "Q est …"                                                       (S2)
C dit: "A et B ne sont pas tous les 2 des domestiques"                 (S3)
D dit: "A est un domestique, OU B est un chevalier"                    (S4)
E dit: "Je suis un domestique, OU C et D ont le même statut"           (S5)

Quelle porte devez-vous choisir pour survivre ?

        Réponse:

        Si E est un domestique, alors (S5) est vraie peu importe le statut de C et D.
        C'est impossible, car un domestique ment tjrs.
        Donc E est un chevalier qui dit la vérité, (S5) est vraie, et "C et D ont le même statut".

        Supposons que C et D sont des domestiques.

                C ment ⇒ (S3) est faux ⇒ A et B sont des domestiques
                D ment ⇒ (S4) est faux ⇒ A n'est pas un domestique, ET B n'est pas un chevalier

                Les 2 précédentes conclusions se contredisent, donc l'hypothèse de départ était fausse:

                        C et D sont des chevaliers.

        Donc:

                C est un chevalier ⇒  (S3) est vrai           ⇒ un seul des 2 magistrats A ou B est un chevalier
                                        + A et B se contredisent

        Si A est un chevalier, alors B est un domestique, et (S4) est faux.
        C'est impossible car D est un chevalier qui dit la vérité.
        Donc A est un domestique et B un chevalier.

        Conclusion: la porte sans danger est la porte Q.

## les prisons de Lem

Après le procès, et choisi la bonne porte, vous finissez dans une cellule de prison.
4 prisonniers s'y trouvent déjà.  Un chevalier et 3 autres: A, B et C

Le chevalier vous apprend qu'il sait que les prisonniers A, B et C savent si oui ou non il existe
un moyen de s'échapper de la cellule.
Il sait aussi qu'au maximum l'un d'eux (A, B ou C) est un ordinaire.

Il le sait car ils ont accepté de répondre à 2 de ses interrogations totales.
Vous-aussi, vous pouvez leur poser 2 interrogations totales.

Quelles sont les 2 interrogations totales que vous pouvez poser à A, B, ou C pour découvrir si oui
ou non il est possible de s'échapper ?

        Réponse:

        Choisissons A comme le prisonnier à qui on posera notre 1e question.
        Celle-ci doit nous permettre de trouver un prisonnier non ordinaire à qui poser notre 2e question.

        On ne peut pas faire confiance à A car il peut être un ordinaire et répondre n'importe quoi,
        donc on l'éliminera quoi qu'il arrive.
        On cherche simplement à savoir, via A, en qui peut-on faire confiance parmi B et C.

        La question suivante permet d'obtenir cette info:

                Êtes-vous un chevalier ssi B est un ordinaire ?

        IOW, les affirmations:

                A est un chevalier    (P1)
                B est un ordinaire    (P2)

        … ont-elles la même valeur de vérité dans l'univers où nous vivons ?

                ┌─────┬─────┬──────┬──────┬───────────┬────────────────┐
                │  A  │  B  │  P1  │  P2  │  P1 ⇔ P2  │  réponse de A  │
                ├─────┼─────┼──────┼──────┼───────────┼────────────────┤
                │  H  │  H  │  v   │  f   │     f     │       n        │
                │  H  │  M  │  v   │  f   │     f     │       n        │
                │  M  │  H  │  f   │  f   │     v     │       n        │
                │  M  │  M  │  f   │  f   │     v     │       n        │
                │  H  │  O  │  v   │  v   │     v     │       o        │
                │  M  │  O  │  f   │  v   │     f     │       o        │
                │  O  │  H  │  f   │  f   │     v     │      o/n       │
                │  O  │  M  │  f   │  f   │     v     │      o/n       │
                └─────┴─────┴──────┴──────┴───────────┴────────────────┘


        Si A répond "non", soit il n'y a pas d'ordinaire parmi A et B, soit A est un ordinaire.
        Dans les 2 cas, B n'est pas un ordinaire.  Car il ne peut pas y en avoir plus qu'un.

        Si A répond "oui", soit B est un ordinaire, soit A est un ordinaire.
        Dans les 2 cas, C n'est pas un ordinaire.

        À l'issue de la 1e question, on peut donc identifier un non ordinaire:

                - B    si A a répondu non
                - C    "              oui


                                    NOTE:

        On pourrait remplacer (P1) par "A est un domestique", ça fonctionnerait aussi, les réponses
        seraient simplement inversées.


        En interrogeant un prisonnier non ordinaire (B ou C), la 2e question doit nous permettre
        de savoir s'il y a un moyen de s'échapper.
        Supposons qu'on interroge B.  La question à lui poser devra être:

                Êtes-vous un chevalier ssi il y a un moyen de s'échapper ?

        IOW, les affirmations:

                - B est un chevalier    (P1)
                - on peut s'échapper    (P2)

        … ont-elles la même valeur de vérité dans l'univers où nous vivons ?

                ┌─────┬──────┬──────┬───────────┬────────────────┐
                │  B  │  P1  │  P2  │  P1 ⇔ P2  │  réponse de A  │
                ├─────┼──────┼──────┼───────────┼────────────────┤
                │  H  │  v   │  v   │     v     │       o        │
                │  M  │  f   │  v   │     f     │       o        │
                │  H  │  v   │  f   │     f     │       n        │
                │  M  │  f   │  f   │     v     │       n        │
                └─────┴──────┴──────┴───────────┴────────────────┘

        On en conclut que si A répond "oui", il existe un moyen de s'échapper, autrement non.

                                    NOTE:

        Méthodologie pour trouver cette question.

        On se doute bien qu'il faudra demander s'il existe un moyen de s'échapper, utiliser (P2)
        est donc évident.

        On ne peut pas faire confiance à B, car il se peut qu'il soit un domestique.
        Il faut donc lui parler de son identité. (P1) semble donc aussi évident.

        Notre question doit exprimer une relation entre (P1) et (P2).
        Le but est de trouver cette relation.

        On doit trouver une question tq B réponde tjrs la même chose, peu importe son statut.
        IOW, il faut que la dernière colonne dans notre table précédente soit:

                o
                o
                n
                n

        Ou l'inverse.
        Pour obtenir cette colonne, il faut que celle qui précède soit:

                v
                f
                f
                v

        Les relations logiques ET et OU ne fonctionnent pas, car elles ne permettent pas de produire
        cette colonne à partir des précédentes.

        Il ne reste plus qu'à tester la relation d'équivalence, qui heureusement elle, fonctionne.


## la fuite de Lem

Vous parvenez à vous échapper de prison, mais êtes arrêté par des guardes.
Vous êtes à nouveau jugé, mais cette fois par une cour composée de 9 hauts magistrats:

        A B C D E F G H I

Ce sont tous des chevaliers ou des domestiques, et ils sont impressionnés par vos capacités de
raisonnement logique.
Ils vous promettent de vous laisser quitter la ville, si vous parvenez à passer un ultime test.

5 boissons sont placées devant vous:

        S T U V W

Au moins 2 ne contiennent pas de poison.
Vous devez en choisir 2, une pour vous, et une pour votre ami (le chevalier avec qui vous vous êtes échappé).

Chacun des 9 magistrats vous donne une information:

        (P1)    A: S est sans danger
        (P2)    B: au moins l'une des 2 boissons, T ou U, est sans danger
        (P3)    C: A et B sont tous les 2 des chevaliers
        (P4)    D: S et T sont toutes les 2 sans danger
        (P5)    E: S et U "
        (P6)    F: D ou E est un chevalier
        (P7)    G: si C est un chevalier, alors F aussi
        (P8)    H: si H et G sont des chevaliers, alors A est un chevalier et B un domestique
        (P9)    I: si parmi les 9 magistrats ici présents, le nb de chevaliers est pair, alors W est du poison

Quelles boissons choisir ?


        Réponse:

        Supposons que G est un domestique.

                (P7) est faux ⇒ (C, F)       = (chevalier, domestique)
                                ⇒ (P3, P6)     = (vrai, faux)
                                ⇒ (A, B, D, E) = (chevalier, chevalier, domestique, domestique)

                (A, B) = (chevalier, chevalier) ⇒ S est danger, et T ou U aussi
                                                ⇒ (P4 ∨ P5) est vrai
                                                ⇒ D ou E est un domestique

        Le dernier résultat, (D ou E est un domestique), est impossible, car il contredit le précédent
        résultat (D, E) = (domestique, domestique)

        Donc, l'hypothèse de départ était fausse:

                ┌───────────────┐
                │ G = chevalier │
                └───────────────┘

        Supposons que C et H sont des chevaliers.

                (H, G) = (chevalier, chevalier) ⇒ (P8) est vrai ⇒ (A, B) = (chevalier, domestique)

                C = chevalier                   ⇒ (P3) est vrai ⇒ (A, B) = (chevalier, chevalier)

        Les 2 derniers résultats sont contradictoires.
        Donc, C et H ne sont pas tous 2 des chevaliers.
        Donc, C ou H est un domestique.


        Supposons que H est un domestique.

                H = domestique ⇒ (P8) est faux
                                ⇒ [(H, G) = (chevalier, chevalier)] ∧ [(A, B) ≠ (chevalier, domestique)]
                                ⇒  (H, G) = (chevalier, chevalier)
                                ⇒       H = chevalier

        Le dernier résulat contredit l'hypothèse de départ, donc cette dernière était fausse.
        Donc, H n'est pas un domestique.

                ┌──────────────────────────────────┐
                │ (C, H) = (domestique, chevalier) │
                └──────────────────────────────────┘

        H = chevalier ⇒ (P8) est vrai

                          ┌──────────────────────────────────┐
                        ⇒ │ (A, B) = (chevalier, domestique) │
                          └──────────────────────────────────┘

                        ⇒ (P1) est vrai, (P2) est faux

                          ┌───────────────────────────────────────────────┐
                        ⇒ │ S est sans danger, ET,  T et U sont du poison │
                          └───────────────────────────────────────────────┘

                        ⇒ (P4) est faux, ET, (P5) est faux

                          ┌───────────────────────────────────┐
                        ⇒ │ (D, E) = (domestique, domestique) │
                          └───────────────────────────────────┘

                        ⇒ (P6) est faux

                          ┌────────────────┐
                        ⇒ │ F = domestique │
                          └────────────────┘

        Supposons que I soit un domestique.

                (P9) est faux ⇒ nb de magistrats chevaliers pair ET W n'est pas du poison
                                ⇒ nb de magistrats chevaliers pair

        Le dernier résultat est impossible, car si I est un domestique, alors il y a un nb impair
        de magistrats chevaliers, à savoir:    A, G, H

        Donc, l'hypothèse de départ était fausse, et I est un chevalier.

                I = chevalier ⇒ (P9) est vrai
                                                                                ┌─────────────────┐
                (P9) vrai ∧ [ nb pair de magistrats chevaliers (A, G, H, I) ] ⇒ │ W est du poison │
                                                                                └─────────────────┘


        Conclusion:

        T, U et W sont du poison.
        Il faut donc choisier les boissons S et V.


## l'île aux yeux bleus

Après avoir réussi à vous échappé de la  ville de Lem, vous prenez un bateau, et
voyagez jusqu'à une île du nom de “Blurona“.

Sur Blurona vivent 200 personnes.
100 ont les yeux bleus, et 100 les yeux marrons.
Vous-même avez les yeux bleus.

Un  soir, une  fête  a lieu  à  laquelle vous  et tous  les  habitants de  l'île
participez.
Vous vous exclamez PUBLIQUEMENT devant tout le monde:

            Comme c'est agréable de voir une  autre personne avec des yeux de la
            même couleur que les miens.

Soudain, la fête est arrêtée, et on vous renvoit à votre bateau avec un livre du
logicien L. N. Cornelius.

Dans le livre, Cornelius fournit un certain nb d'infos à propos des habitants de
Blurona:

        - personne ne connaît la couleur de ses propres yeux (pas de miroir)

        - il est interdit de parler de la couleur des yeux des habitants

        - si un habitant découvre la couleur de ses propres yeux, il doit
          quitter l'île à bord d'un bateau qui part chaque jour à midi

        - chaque jour, chaque habitant doit rencontrer tous les autres habitants

        - chaque habitant est un parfait logicien:

            un parfait  logicien est  qn qui déduira  immédiatement tout  ce qui
            peut être déduit de n'importe quelle situation donnée

        - chaque habitant connaît toutes les infos du livre de Cornelius, et
          sait que tous les autres habitants connaîssent eux-aussi ces infos


Au début, vous pensez avoir été simplement  banni pour avoir parlé de la couleur
des yeux de qn.
Mais après mûre réflexion, vous réalisez avoir fait qch d'horrible, qui aura des
conséquences pour les habitants de l'île.

Que va-t-il se passer ? Qd ? Pk ?


        Indice:

        Il faut commencer par se demander ce qui se passerait s'il n'y avait qu'un BEP
        (blue-eyed people) sur l'île.
        Puis, ce qu'il se passerait s'il y avait 2 BEPs.
        Puis, 3.
        …


        Réponse:

        Supposons qu'il n'y ait qu'un seul BEP, A.

                A quittera l'île le lendemain à midi.
                En effet,  il verra que tous  les autres habitants ont  les yeux
                marrons, et déduira que lorsque vous vous êtes exclamé:

                        "Comme c'est agréable de voir une autre personne avec des yeux de la même
                        couleur que les miens"

                … vous étiez en train de parler de lui.


        Supposons qu'il n'y ait que 2 BEPs, A et B.

                Le seul BEP que A verra sera B.
                A fera l'hypothèse que B est le seul BEP sur l'île.
                Et A s'attendra à ce que B parte le jour suivant à midi.

                Mais B ne quittera pas l'île, car il fera le même raisonnement, et s'attendra à
                ce que ce soit A le seul BEP, et que ce soit A qui quitte l'île le lendemain.

                Voyant que B ne quitte pas l'île, A en déduira que son hypothèse était fausse:

                        B n'était pas le seul BEP.

                Le seul autre habitant pouvant avoir les yeux bleus est lui-même.
                A déduira qu'il a lui-aussi les yeux bleus.

                B fera le même raisonnement et le 2e jour, A et B quitteront l'île.


        Supposons qu'il n'y ait que 3 BEPs, A, B et C.

                Les seuls BEPs que A verra, seront B et C.
                A fera l'hypothèse que B et C sont les seuls BEPs sur l'île.
                Et A s'attendra à ce que B et C partent le 2e jour à midi.

                Mais ni B, ni C ne quitteront l'île, car ils feront le même raisonnement, et
                s'attendront à ce que resp. (A, C), et (A, B) soient les seuls BEPs,
                et que ce soit resp. (A, C) et (A, B) qui quitte l'île le lendemain.

                Voyant que personne ne quitte l'île au bout de 2 jours, A en déduira que son
                hypothèse était fausse:

                        (B, C) n'était pas les seuls BEPs.

                Le seul autre habitant pouvant avoir les yeux bleus est lui-même.
                A déduira qu'il a lui-aussi les yeux bleus.

                B et C feront le même raisonnement et le 3e jour, A, B et C quitteront l'île.


        On en déduit ce qui va se passer sur l'île après votre départ.
        Tous les habitants aux yeux bleus quitteront l'île le 100e jour.



Quelle simple phrase auriez-vous pu prononcer qui aurait obligé tous les habitants à prendre
le bateau et quitter l'île ?

        Réponse:

                Je vois 100 personnes aux yeux bleus et 100 personnes aux yeux marrons.

                                    OU

                Je vois une personne aux yeux verts.

        À partir de la 1e phrase, les habitants déduiront directement la couleur de leurs yeux
        et quitteront l'île dès le 1er jour.

        La 2e phrase est un mensonge.
        Mais si les habitants vous croient, alors ne voyant aucune personne aux yeux verts
        sur l'île, chacun d'eux en déduira qu'il est l'unique personne aux yeux verts.
        Croyant connaître la couleur de ses yeux, chacun quittera l'île dès le 1er jour.



Quelle  est l'information  que  les habitants  de l'île  ont  gagné après  votre
exclamation, qu'ils n'avaient pas déjà ?

        Réponse:

        Supposons qu'il n'y ait que 2 BEP.  Alice et Bob.

                Alice savait déjà qu'il y avait un BEP sur l'île, mais elle ne savait pas si Bob
                lui-aussi savait qu'il y avait un BEP.
                Dans l'esprit d'Alice, il était parfaitement possible que Bob soit le seul BEP,
                et qu'il n'avait donc jamais vu aucun BEP jusqu'ici.

                Après  votre exclamation,  Alice a  gagné l'information  que Bob
                sait qu'il y a un BEP sur l'île.

                                     NOTE:

                Alice ne gagne cette information que si votre exclamation est PUBLIQUE.
                Si vous vous contentez de voir chaque habitant de l'île en lui disant à chaque fois:

                        il y a au moins un BEP sur l'île

                … vous ne lui apprendriez rien.  Il le sait déjà.

                Sans une exclamation publique, rien ne se passerait sur l'île après votre départ.


        Supposons qu'il n'y ait que 3 BEPs.  Alice, Bob et Charlie.

                Alice savait déjà qu'il y avait 2 BEPs sur l'île, mais elle ne savait pas si Bob
                savait que Charlie savait qu'il y avait un BEP.

                Dans l'esprit d'Alice, il était parfaitement possible que Bob et Charlie soient
                les seuls BEPs.
                Donc, dans l'esprit d'Alice, il était possible que dans l'esprit de Bob, Charlie
                soit le seul BEP.

                Après votre exclamation, Alice a gagné l'information que Bob sait que Charlie
                sait qu'il y a un BEP sur l'île.


        Supposons qu'il n'y ait que 4 BEPs.  Alice, Bob, Charlie et Dan.

                Alice savait déjà qu'il y avait 3 BEPs sur l'île, mais elle ne savait pas si Bob
                savait que Charlie savait que Dan savait qu'il y avait un BEP.

                Dans l'esprit d'Alice, il était parfaitement possible que Bob, Charlie et Dan soient
                les 3 seuls BEPs.
                Donc, dans l'esprit d'Alice, il était possible que dans l'esprit de Bob, Charlie
                et Dan sonts les 2 seuls BEPs.
                Donc, dans l'esprit d'Alice, il était possible que dans l'esprit de Bob, il était
                possible que dans l'esprit de Charlie, Dan est le seul BEP.

                Après votre exclamation, Alice a gagné l'information que Bob sait que Charlie
                sait que Dan sait qu'il y a un BEP sur l'île.


        À chaque fois que qn se projète dans l'esprit de qn d'autre, if fait l'hypothèse qu'il n'a
        pas les yeux bleus.  Ces hypothèses s'enchaînent dans l'esprit d'Alice.

        La 1e est:    Je n'ai pas les yeux bleus

        La 2e est:    Bob n'a pas les yeux bleus
                        (dans l'esprit de Bob imaginé par Alice)

        La 3e est:    Charlie n'a pas les yeux bleus
                        (dans l'esprit de Charlie imaginé par Bob imaginé par Alice)

        La 4e est:    Dan n'a pas les yeux bleus
                        (dans l'esprit de Dan imaginé par Charlie imaginé par Bob imaginé par Alice)
        …


        Techniquement, "il y a au moins un BEP sur l'île" est une connaissance universelle avant
        même votre arrivée.
        Mais après votre exclamation, elle devient une connaissance commune:

                https://fr.wikipedia.org/wiki/Connaissance_commune
                https://en.wikipedia.org/wiki/Common_knowledge_%28logic%29



Que se passerait-il si au bout de 100 jours, pour une raison donnée, les 100 BEPs ne peuvent pas
quitter l'île ?

        Réponse:

        Tout le monde quittera l'île le 101e jour.
        En effet, passé le 100e jour, chaque habitant aux yeux marrons pensera que si les 100 BEPs
        ne sont pas partis, c'est parce qu'il y a au moins 101 BEPs sur l'île.
        Et comme il ne peut en voir que 100, chaque habitant aux yeux marrons en déduira qu'il est
        le 101e BEP.



Pour + d'infos:

        https://math.stackexchange.com/questions/489308/blue-eyes-a-logic-puzzle
        http://math.stackexchange.com/a/490824
        https://puzzling.stackexchange.com/questions/236/in-the-100-blue-eyes-problem-why-is-the-oracle-necessary

# TO MOCK A MOCKINGBIRD

Dans une énigme faisant intervenir un oiseau, on peut formaliser ce dernier comme un opérateur de combinaison.

En informatique, un pgm ou une fonction peut être vu comme un opérateur de combinaison.

## Logic Puzzles
### The Prize and Other Puzzles
#### Le jardin de fleurs

Dans un certain jardin de fleurs, toutes les fleurs sont rouges, jaunes ou bleues.
Les 3 couleurs sont bien représentées par au moins une fleur.

Un jour, un statisticien visita ce jardin, et constata:

        (P1) peu importe le triplet de fleurs qu'on peut cueillir, il contient tjrs au moins une
             fleur rouge

Un autre jour, un 2e statisticien constata:

        (P2) peu importe le triplet de fleurs qu'on peut cueillir, il contient tjrs au moins une
             fleur jaune

En apprenant ces 2 informations, un étudiant en logique fit la déduction suivante:

        Peu importe le triplet de fleurs qu'on cueille dans ce jardin, au moins une est bleue.

Son camarade classe s'exclama:

        Bien sûr que non !

Lequel des 2 étudiants a raison ?


        Réponse:

        Soit j, r, b le nb de fleurs jaunes, rouges et bleues.

                j ≥ 3 ⇒ (R1) on peut cueillir 3 fleurs, aucune n'étant rouge

                        (R1) ⊥ (P1) ⇒ j < 3

                j = 2 ⇒ (R2) on peut cueillir 3 fleurs, dont 2 sont jaunes et 1 bleue; aucune n'est rouge

                        (R2) ⊥ (P2) ⇒ j < 2 ⇒ j = 1

        De la même façon, on peut prouver que `r = 1`.

        Conclusion:

        Il n'y a qu'une seule fleur jaune et une seule fleur rouge dans le jardin.
        Qd on cueille 3 fleurs, la 3e est donc nécessairement bleue.
        Le 1er étudiant avait raison.

        De plus, on pourrait facilement prouver qu'il n'y a qu'une seule fleur bleue dans le jardin:

                j = r = b = 1


#### Quelle question ?

Il existe une question que je pourrai vous poser, pour laquelle une réponse définie existe, mais à
laquelle vous ne pouvez logiquement pas répondre.

Il se peut que vous connaissiez la réponse, mais vous ne pouvez pas la donner.
N'importe qui d'autre peut connaître la réponse, et peut la donner.

Quelle question ai-je en tête ?


        Réponse:

                (Q) Allez-vous répondre non à cette question ?


        Soit (P) la proposition:

                (P) Je vais répondre ’non’ à votre question

        La question précédente équivaut à:

                (P) est-elle vraie ?

        Si je réponds ’non’, j'affirme que (P) est fausse.
        Pourtant, je viens de répondre ’non’, ce qui prouve que (P) est vraie.
        Contradiction.

        Si je réponds ’oui’, j'affirme que (P) est vraie.
        Pourtant, je viens de répondre ’oui’, ce qui prouve que (P) est fausse.
        Contradiction.

        Peu importe ma réponse, je mentirai.


#### Les 3 prix

Je vous fais participer à un jeu suivant pour lequel 3 récompenses sont dispo:    A, B et C
A a plus de valeur que B, qui elle-même a plus de valeur que C.

La règle du jeu est que si vous me donnez une affirmation qui est:

        - vraie,  je vous donnerai A ou B
        - fausse, "                C

Quelle affirmation pourriez-vous prononcer qui m'obligerait à vous donner A ?


        Réponse:

                (P) Vous ne me donnerez pas B.

        Si je vous donne C, alors (P) était vraie.  Donc, j'aurai dû vous donner A ou B.
        Si je vous donne B, alors (P) était fausse.  Donc, j'aurai dû vous donner C.

        Je suis obligé de vous donner A.



J'ajoute un 4e prix, D dont la valeur est égale à celle de C.
La règle du jeu est que si vous me donnez une affirmation qui est:

        - vraie,  je vous donnerai A ou B
        - fausse, "                C ou D

Quelle affirmation pourriez-vous prononcer qui m'obligerait à vous donner C ?


        Réponse:

                (P) Vous me donnerez D.

        Si je vous donne A ou B, alors (P) était fausse.  Donc, j'aurai dû vous donner C ou D.
        Si je vous donne D, alors (P) était vraie.  Donc, j'aurai dû vous donner A ou B.

        Je suis obligé de vous donner C.



La règle du jeu n'a pas changé, et il y a tjrs 4 prix:    A, B, C, D

Quelle affirmation pourriez-vous prononcer qui m'obligerait à violer la règle du jeu ?

        Réponse:

                (P) Vous me donnerez C ou D.

        Si je vous donne A ou B, alors (P) était fausse.  Donc, j'aurai dû vous donner C ou D.
        Si je vous donne C ou D, alors (P) était vraie.  Donc, j'aurai dû vous donner A ou B.

        Peu importe le prix que je vous offrirai, je violerai la règle du jeu.


#### Le paradoxe de Sancho Panza

Dans une certaine ville, un décret a été voté qui dit la chose suivante:

        Tout étranger franchissant le pont pour entrer dans la ville doit être arrêté, et doit fournir
        une affirmation (P).
        Si (P) est vraie, il peut passer.  Si (P) est fausse, il doit être pendu.

Quelle affirmation l'étranger pourrait-il prononcer qui empêcherait le décret de lui être appliqué ?


        Réponse:

                Je vais être pendu.

        S'il est pendu, (P) était vraie, et donc il ne fallait pas le pendre.
        S'il n'est pas pendu, (P) était fausse, et donc il aurai dû être pendu.

### The Absentminded Logician
#### John, James, et Williams

Vous connaissez 3 frères John, James et Williams.
Ils sont indistinguables en apparence.
John et James mentent toujours, tandis que Williams dit toujours la vérité.

Un jour, vous rencontrez l'un des 3 frères dans la rue, et souhaitez savoir s'il s'agit de John,
car ce dernier vous doit de l'argent.
Vous pouvez lui poser une seule question, qui ne peut contenir que 3 mots, et à laquelle il ne peut
répondre que par oui par non.

Quelle question devriez-vous lui poser ?

        Réponse:

                Êtes-vous James ?

        Soit A le frère que j'interroge.

        Si A est John, il va mentir, et répondre oui.
        Si A est James, il va mentir, et répondre non.
        Si A est Williams, il va dire la vérité, et répondre non.

        Conclusion:

        Si A répond oui, je sais qu'il s'agit de John.  Autrement, ce n'est pas lui.


On change les conditions précédentes.  Cette fois, John et James disent la vérité, et Williams ment.
Vous rencontrez à nouveau l'un des 3 frères.
Quelle question de 3 mots pourriez-vous lui poser pour savoir s'il s'agit de John ?

        Réponse:

                Êtes-vous James ?

        Soit A le frère que j'interroge.

        Si A est John, il va dire la vérité, et répondre non.
        Si A est James, il va dire la vérité, et répondre oui.
        Si A est Williams, il va mentir, et répondre oui.

        Conclusion:

        Si A répond non, je sais qu'il s'agit de John.  Autrement, ce n'est pas lui.


#### Arthur et son frère

Arthur et son frère sont une paire d'individus incluant un menteur et une honnête personne.
On ignore lequel des 2 est honnête, et lequel ment.

Un jour, vous rencontrez les 2 frères dans la rue, et souhaitez savoir lequel est Arthur.
Pour ce faire, vous avez droit à une interrogation totale que vous pouvez poser à l'un des 2 frères.

Quelle question pourriez-vous lui poser ?

        Réponse:

                Arthur ment-il ?

        Supposons qu'on pose la question à Arthur.

                - Si Arthur dit la vérité, il répondra non.
                - Si Arthur ment, il répondra non.

        Supposons qu'on pose la question au frère d'Arthur.

                - Si le frère dit la vérité, il répondra oui.
                - Si le frère ment, il répondra oui.

        Conclusion:

        La réponse varie en fonction de l'interlocuteur.
        Donc, si la personne répond non, l'interlocuteur est Arthur, autrement son frère.



Cette fois, vous voulez savoir si Arthur dit la vérité ou ment.
Quelle question de 3 mots pourriez-vous poser ?

        Réponse:

                Êtes-vous Arthur ?

        Si Arthur dit la vérité, il répondra oui, et son frère aussi.
        S'il ment, il répondra non, et son frère aussi.

        Conclusion:

        Si la personne répond oui, on en déduit qu'Arthur dit la vérité, autrement il ment.



Cette fois, vous voulez savoir lequel dit la vérité, et lequel ment.
Quelle question de 3 mots vous permettrez d'obtenir cette info ?

        Réponse:

                Suis-je Arthur ?

        Je ne suis pas Arthur, donc dans tous les univers, le menteur répondra oui, et celui qui dit
        la vérité répondra non.



Cette fois, vous devez trouver une question contenant au plus 4 mots, à laquelle la personne que vous
interrogerez répondra oui à coup sûr.  Quelle question poser ?


        Réponse:

                Dites-vous la vérité ?

        Le menteur répondra tjrs oui, et celui qui dit la vérité aussi.


#### L'intersection

Vous vous dirigez vers la ville de Pleasantville.
Vous arrivez à une intersection, et il faut choisir dans quelle direction continuer le voyage:
à gauche ou à droite.
À cette intersection se trouve un individu qui sait dans quelle direction se trouve Pleasantville,
mais qui dit tjrs la vérité OU qui ment tjrs.

Quelle question pourriez-vous lui poser pour deviner dans quelle direction se trouve Pleasantville ?


        Réponse:

                Si je vous demandais si la route de gauche mène à Pleasantville, pourriez-vous répondre oui ?

        Soit (P) la proposition:

                La route de gauche mène à Pleasantville.

        Si l'individu répond oui et qu'il ment, ça signifie qu'il ne pourrait pas affirmer que (P) est vrai.
        IOW, il affirmerait que (P) est faux.
        S'il affirmait que (P) est faux alors qu'il est un menteur, ça implique que (P) est vrai.
        Donc, la bonne route est celle de gauche.

        Si l'individu répond oui et qu'il dit la vérité, ça veut dire qu'il pourrait affirmer que (P) est vrai.
        Et s'il affirmait que (P) est vrai, comme il dit la vérité, on pourrait en déduire que (P) est vrai.
        Donc, encore une fois, la bonne route est celle de gauche.

        Conclusion:
        Si l'individu répond oui, qu'il mente ou pas, la bonne route est celle de gauche.
        On pourrait montrer de la même façon que s'il répondait non, la bonne route serait celle de droite.

                                     NOTE:

        Plus généralement, qd une personne connaît la véracité d'une proposition (P), et qu'elle ment
        tjrs ou dit tjrs la vérité, on peut construire une question similaire et la lui soumettre:

                Si je vous demandais si (P) est vraie, pourriez-vous répondre oui ?

        Il s'agit du principe de Nelson Goodman (philosophe).

        Comme on peut le voir dans d'autres énigmes (Arthur et son frère, le logicien distrait, …),
        on est obligé d'utiliser ce principe uniquement qd on a aucune information à propos de la personne
        qu'on interroge.

        Qd on a une information (la personne à qui je parle est: Arthur ou son frère, ma femme ou sa soeur, …),
        on peut s'en servir pour construire une question moins alambiquée que celle produite par le principe
        de Nelson Goodman.


#### Le logicien distrait

Vous avez rencontré 2 soeurs jumelles, Teresa et Lenore.
Teresa dit tjrs la vérité, et Lenore ment tjrs.
Vous tombez amoureux de l'une d'elles, et l'épousez sans savoir de laquelle des 2 il s'agit.
L'autre soeur n'épousera personne avant plusieurs années.

Après le mariage, vous devez vous absenter pour assister à une conférence.
De retour, vous rencontrez l'une des soeurs au cours d'un cocktail.
Vous ignorez de qui il s'agit: Teresa ou Lenore.

Quelle question d'au plus 4 mots pourriez-vous lui poser pour savoir s'il s'agit de votre femme ?


        Réponse:

                Teresa est-elle mariée ?

        Supposons que vous soyez marié à Teresa (qui dit tjrs la vérité).

                Si la soeur que vous rencontrez est:

                        - Teresa, elle répondra oui
                        - Lenore, "             non

        Supposons que vous soyez marié à Lenore (qui ment tjrs).

                Si la soeur que vous rencontrez est:

                        - Teresa, elle répondra non
                        - Lenore, "             oui


        Conclusion:

        Dans tous les univers, si la soeur répond oui il s'agit de votre femme.



Cette fois, vous voulez savoir quel est le nom de votre femme.
Quelle question d'au plus 3 mots vous pourriez poser à la personne en face de vous pour obtenir cette info ?

        Réponse:

                Êtes-vous mariée ?

        Supposons que vous soyez marié à Teresa.

                Si la soeur que vous rencontrez est:

                        - Teresa, elle répondra oui
                        - Lenore, "             oui

        Supposons que vous soyez marié à Lenore.

                Si la soeur que vous rencontrez est:

                        - Teresa, elle répondra non
                        - Lenore, "             non

        Conclusion:
        La réponse à la question varie en fonction du prénom de votre femme.
        Donc, si la personne répond oui, votre femme s'appelle Teresa, autrement Lenore.


Cette fois, vous voulez savoir le nom de votre femme ET qui est la personne en face de vous.
Vous pouvez poser une interrogation totate contenant autant de mots que vous voulez.
Quelle question pourriez-vous poser ?


        Réponse:

        Aucune.

        On peut être marié à Teresa ou à Lenore (2 possibilités), et la personne en face de nous peut
        être Teresa ou Lenore (2 possibilités).  Il existe donc 4 univers possibles.

        Une question n'ayant pour réponses possibles que oui ou non, ne permet de faire la différence
        qu'entre au plus 2 univers, pas 4.

### The Barber of Seville
#### Double paradoxe du barbier (Arturo et Roberto)

Arturo et Roberto vivent dans un village.
Pour tout habitant X, autre qu'Arturo, Arturo  rase X ssi X ne rase pas Arturo.
"                                      Roberto rase X ssi X rase Roberto.

Ces règles conduisent-elles à un paradoxe ?


        L'énoncé nous donne les propositions suivantes:

                (P1) Arturo  rase X  ⇔  X ne rase pas Arturo    X ≠ Arturo
                (P2) Roberto rase X  ⇔  X rase Roberto          X ≠ Roberto

        (H1) Supposons que "Roberto rase Arturo"

                (H1) ∧ (P2) ⇒ (P3) Arturo rase Roberto
                (P1) ∧ (P3) ⇒ (P4) Roberto ne rase pas Arturo

                        (P4) ⊥ (H1) ⇒ (H1) faux

        (H2) Supposons que "Roberto ne rase pas Arturo"

                (H2) ∧ (P1) ⇔ (P5) Arturo  rase Roberto
                (P2) ∧ (P5) ⇔ (P6) Roberto rase Arturo

                        (P6) ⊥ (H2) ⇒ (H2) faux

        Conclusion:
        Peu importe l'hypothèse de départ (Roberto rase Arturo, ou pas), on aboutit à une contradiction logique.
        Donc oui, il y a bien un paradoxe.

        Arturo et Roberto sont incompossibles:
        chacun pris indépendamment peut exister dans son village sans qu'il n'y ait de contradicition.
        Mais les 2 ne peuvent pas exister dans un même village.



Arturo et Roberto vivent dans un même village.
Arturo  rase X, ssi X rase Roberto.
Roberto rase X, ssi X ne rase pas Arturo.

Ces règles conduisent-elles à un paradoxe ?


        Un paradoxe se produit si dans tous les univers possibles, on trouve une contradiction logique.
        Ceci implique qu'il n'y a pas de paradoxe si on peut trouver un univers dans lequel il n'y a pas
        de contradiction.

        Dans un souci de simplification du pb, considérons l'univers dans lequel le village ne contient
        que 2 habitants: Arturo et Roberto.

        On utilise la notation XrY pour formaliser la proposition "X rase Y".

        L'énoncé nous donne les propositions suivantes (A et R désignent Arturo et Roberto):

                (P1) ArX  ⇔   XrR
                (P2) RrX  ⇔  ¬XrA


        Si on remplace X par A dans (P1) et (P2), on obtient les équivalences suivantes:

                (E1) ArA  ⇔   ArR
                (E2) RrA  ⇔  ¬ArA

        Si on remplace X par R dans (P1) et (P2), on obtient les équivalences suivantes:

                (E3) ArR  ⇔   RrR
                (E4) RrR  ⇔  ¬RrA

        On déduit des 4 précédentes équivalences:

                (E1) ∧ (E3)    ⇔    (ArA  ⇔  ArR  ⇔  RrR)           (E5)

                                  ┌──────────────────────────────────────┐
                (E5) ∧ (E4)    ⇔  │ (ArA  ⇔  ArR  ⇔  RrR  ⇔  ¬RrA)  (E6) │
                                  └──────────────────────────────────────┘

                  (E6)         ⇔  (E1) ∧ (E3) ∧ (E4)
           (1)    (E6) ∧ (E2)  ⇔  (E1) ∧ (E3) ∧ (E4) ∧ (E2)

                  (E6)         ⇒  (E2)
           (2) ⇒  (E6) ∧ (E2)  ⇔  (E6)

                                  ┌──────────────────────────────────────┐
                (1) ∧ (2)      ⇒  │  (E1) ∧ (E2) ∧ (E3) ∧ (E4)  ⇔  (E6)  │
                                  └──────────────────────────────────────┘

        L'énoncé de départ équivaut donc à (E6).

        Or d'après (E6):

                - si Arturo se rase lui-même, alors il rase aussi Roberto, et Roberto se rase lui-même,
                  mais pas Arturo

                - si Arturo ne se rase pas lui-même, alors il ne rase pas non plus Roberto, et Roberto rase
                  seulement Arturo (pas lui-même).

                  En effet:

                          ¬(E6)    ⇔    (¬ArA  ⇔  ¬ArR  ⇔  ¬RrR  ⇔  RrA)

        Pour qu'il y ait paradoxe, il aurait fallu que nos 2 hypothèses aboutissent à des contradictions,
        ce qui n'est pas le cas.  Aucune n'aboutit à une contradiction.

        On a trouvé un univers dans lequel il n'y a pas contradiction, donc l'énoncé ne contient pas de paradoxe.

#### Barbier pour un jour

Dans, un village de 365 habitants mâles, il fut un jour décidé que le temps d'une année, chaque homme
serait barbier pendant exactement un jour.
Soit X le barbier d'un jour donné, et X' la 1e personne que X rase ce jour-là.
On a:

    (P)    ∀D: ∃E: ∀X: ∀Y    X rase Y le jour E  ⇒  X' rase Y le jour D

De plus, X n'est pas le seul à pouvoir raser le jour D.

Comment déduire de cet énoncé que chaque jour de l'année, il existe au moins un homme qui se rase lui-même.


        (P) est vraie pour tout Y, en particulier pour Y=X'.
        Dans (P), on peut donc remplacer Y par X':

                (P1):   ∀D: ∃E: ∀X:       X rase X' le jour E  ⇒  X' rase X' le jour D

        X' est la 1e personne à être rasée par X le jour E.  Donc, il est vrai que:

                (P2)    X rase X' le jour E

        (P1) ∧ (P2)  ⇒  chaque jour D, X' se rase lui-même

#### Le club des barbiers

Il existe un club de barbiers pour lequel les faits suivants sont vrais:

    (P1) chaque membre du club a rasé au moins un membre
    (P2) aucun membre ne s'est jamais rasé lui-même
    (P3) aucun membre n'a jamais été rasé par plus d'un membre
    (P4) il existe un membre qui n'a jamais été rasé du tout

Le nb de membres au sein de ce club est tenu secret.
Une rumeur prétend qu'il serait inférieur à 1000.
Une autre qu'il serait supérieur à 1000.

Quelle rumeur est vraie?

            Soit n le nb de membres du club.

            Si on admet la possibilité que n soit infini, alors la 2e rumeur est la bonne.

            On peut le vérifier comme ceci:

                    (P4)                      ⇒ ∃M1: ∀i ∈ {1,…,n} : ¬(Mi r M1)

                    (P1) ∧ (P2) ∧ (P4)        ⇒ ∃M2: M2 ∉ {M1, M2}        ∧ (M1 r M2)
                    (P1) ∧ (P2) ∧ (P3) ∧ (P4) ⇒ ∃M3: M3 ∉ {M1, M2, M3}    ∧ (M2 r M3)

                                                  …

                    (P1) ∧ (P2) ∧ (P3) ∧ (P4) ⇒ ∃Mp: Mp ∉ {M1, M2, …, Mp} ∧ (Mp-1 r Mp)

            (P1) affirme que Mp a rasé qn.

            (P2) empêche Mp de raser  Mp
            (P3) "                   {M2,…,Mp-1}
            (P4) "                    M1

            Donc, Mp est obligé de raser un membre différent des précédents: Mp+1

            Conclusion:
            Chaque membre est obligé de raser un tout nouveau membre, donc n doit être infini.
            En particulier n>1000.

#### Un autre club de barbiers

Un autre club de barbiers obéit aux règles suivantes:

    (P1) si un membre a rasé un membre, que ce soit lui-même ou un autre, alors tous les membres l'ont rasé
    (P2) 4 membres s'appellent:    Guido, Lorenzo, Petruchio, Cesare
    (P3) Guido a rasé Cesare

Petruchio a-t-il rasé Lorenzo ?

        (P1) ∀X: (∃Y: XrY) ⇒ (∀Z: ZrX)
        (P3) GrC

        (P1) ⇒ [(∃Y: GrY) ⇒ (∀Z: ZrG)] (P4)    en remplaçant X par G dans (P1)
        (P1) ⇒ [(∃Y: LrY) ⇒ (∀Z: ZrL)] (P5)    en remplaçant X par L dans (P1)

        (P3) ∧ (P4) ⇒ (∀Z: ZrG) ⇒ LrG
        LrG  ∧ (P5) ⇒ ∀Z: ZrL ⇒ PrL

        Oui, Petruchio a bien rasé Lorenzo.

#### Le club exclusif

Il existe un autre club, appelé "le club exclusif".

(P1) Une personne appartient à ce club, ssi elle ne rase personne qui la rase.
(P2) Cardano se vante d'avoir rasé tous les membres du club, et personne d'autre.

Comment prouver que c'est impossible ?

        Supposons que Cardano fasse partie du club.
        Il ne rase donc personne qui le rase.
        Mais Cardano se vante de raser tous les membres du club, donc il devrait se raser, puisqu'il
        fait partie du club.  Contradiction.

        Supposons que Cardano ne fasse pas partie du club.
        Il existe donc au moins une personne que Cardano rase et qui rase Cardano.
        Appelons-la Antonio.

        Antonio fait partie du club, car Cardano dit qu'il ne rase que des membres du club
        ("et personne d'autre")

        Antonio rase Cardano, et Cardano rase Antonio.
        Donc Antonio rase qn qui le rase, et Antonio ne fait pas partie du club.
        Contradiction.

        Que Cardano appartienne ou non au club, on aboutit à une contradiction logique.

#### Le barbier de Seville

Dans la ville de Seville, tous les habitants hommes portent une perruque qd on ils ont envie.
Il n'existe aucun couple d'hommes distincts qui se comportent de la même façon chaque jour de l'année.

        ∀X: ∀Y: (X ≠ Y) ⇒ ∃d ((Xp ∧ ¬Yp) ∨ (¬Xp ∧ Yp))
         │   │            │    │    │
         │   │            │    │    └ Y ne la porte pas
         │   │            │    └ X porte la perruque
         │   │            └ un jour de l'année
         │   └ un autre homme de Seville
         └ un homme de Seville

Si chaque jour où X porte la perruque, Y aussi, on dit que Y est un suiveur de X.
Si chaque jour où X et Y portent tous les 2 la perruque, Z aussi, on dit que Z est un suiveur de X et Y.

Alfredo, Bernardo, Benito, Roberto, Ramano sont 5 habitants de Seville.
Chacun d'eux utilise une perruque qui a tjrs la même couleur:

        (A)  Alfredo   noire
        (B1) Bernardo  blanche
        (B2) Benito    grise
        (R1) Roberto   rouge
        (R2) Ramano    brune

Bernardo et Benito ont un comportement opposé:
qd Bernardo porte la perruque, Benito ne la porte pas et inversement.

        (B1p ⇒ ¬B2p) ∧ (B2p ⇒ ¬B1p)
      ⇔ (B1p ⇒ ¬B2p) ∧ (¬B2p ⇒ B1p)

      ⇔          B1p ⇔ ¬B2p

Roberto et Ramano ont eux-aussi un comportement opposé.

                 R1p ⇔ ¬R2p


Ramano porte la perruque ssi Alfredo et Benito portent tous 2 la perruque.

        R2p ⇔ Ap ∧ B2p

Seville compte un seul barbier (B3).

Bernardo est un suiveur d'Alfredo et du barbier.

        Ap ∧ B3p ⇒ B1p

Quel que soit l'habitant X, si Bernardo est un suiveur d'Alfredo et de X, alors le barbier est un suiveur
de X.

        ∀X: (Ap ∧ Xp ⇒ B1p) ⇒ (Xp ⇒ B3p)

Un matin de Pâques, on vit le barbier porter une perruque.
De quelle couleur était-elle ?


        Il n'y aucune info dans l'énoncé qui parle de la couleur de la perruque du barbier.
        Donc, soit il y a un paradoxe, et le barbier n'existe pas ou il ne porte pas de perruque,
        soit il existe et porte une perruque.
        Dans ce dernier cas, quelle pourrait être la 2e proposition (X), en partant de la fin du
        raisonnement, nous permettant de déduire la couleur de sa perruque ?

                (X) ⇒ la perruque du barbier est rose

        L'énoncé ne parle pas de la couleur rose, et il ne parle pas de mélanger des couleurs, donc
        la dernière étape du raisonnement ne peut pas être:

                la perruque du barbier est rose

        L'énoncé ne parle que des couleurs {noire, blanche, grise, rouge, brune}.
        En revanche, la dernière étape pourrait être:

                la perruque du barbier est grise

                (X) ⇒ la perruque du barbier est grise

        La seule info qu'on a à propos de la couleur grise est qu'il s'agit de la couleur de perruque
        de Benito (B2).  Il est donc probable que (X) parle de Benito.
        Exemples de propositions parlant du barbier et de Benito:

                (X) qd le barbier porte une perruqe, Benito aussi
        OU
                (X) qd le barbier porte une perruqe, Benito n'en porte pas

        Ces propositions comparent le comportement du barbier et de Benito, mais elles ne parlent pas
        de la couleur de la perruque du barbier.
        Quelle proposition (X), parlant du barbier et de Benito, nous permettrait de déduire que la
        couleur de la perruque du barbier est grise ?

                (X) le barbier est Benito

        ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
        │ S'il n'y a pas de paradoxe, le but de l'énigme est donc d'identifier le barbier comme étant │
        │ A, B1, B2, R1 ou R2.                                                                        │
        └─────────────────────────────────────────────────────────────────────────────────────────────┘


        Quelle pourrait être la 3e proposition (Y), en partant de la fin du raisonnement ?

                (Y) ⇒ le barbier est Benito

        D'après (P1), on sait qu'il n'existe aucun couple d'hommes distincts qui se comportent de la
        même façon chaque jour de l'année.
        Si on démontrait que le barbier et Benito se comportent de la même façon tous les jours de l'année,
        alors on en conclurait que le barbier est Benito.

                (P1) ∧ (B2 ≠ B3)
            ⇒   ∃d: (B2 ∧ ¬B3) ∨ (¬B2 ∧ B3)
                               │
                               └ si B2 et B3 se comportent tjrs pareil, c'est faux

                (P1) ∧ (B2 ≠ B3) est faux
                (B2 ≠ B3) est faux (car (P1) est vrai par hypothèse)

        En français:
        (P1) nous apprend que le comportement d'un homme vis à vis de sa perruque suffit à l'identifier.

        ┌──────────────────────────────────────────────────────────────────────────────────────────┐
        │ Il faut démontrer que le barbier et l'un des 5 habitants A, B1, B2, R1, R2 se comportent │
        │ tjrs pareil.                                                                             │
        └──────────────────────────────────────────────────────────────────────────────────────────┘

        Que signifie "se comporter pareil" ?

        Deux habitants X et Y se comportent pareil, ssi, qd X porte une perruque Y en porte aussi,
        et qd X n'en porte pas, Y n'en porte pas non plus:

                (Xp ⇒ Yp) ∧ (¬Xp ⇒ ¬Yp)
            ⇔   (Xp ⇒ Yp) ∧ (Yp ⇒ Xp)
            ⇔         (Xp ⇔ Yp)

        Il faut donc chercher à démontrer:

                               ┌─────────────────────────────────┐
                (B3p ⇔ Xp)  ⇔  │ B3p ⇒ Xp    X ∈ {A,B1,B2,R1,R2} │
                               │ Xp  ⇒ B3p                       │
                               └─────────────────────────────────┘



        On triche un peu, la solution est `B3 = R1`, on va donc chercher tout de suite à démontrer
        les 2 précédentes implications, en remplaçant X par R1.
        Sans tricher, il aurait fallu tenter de les démontrer pour X=A, X=B1, X=B2, X=R1 et X=R2.
        Le livre triche lui-aussi, il cherche immédiatement à prouver `B3 = R1` sans expliquer pourquoi
        R1 et pas un autre habitant.


        La formalisation de l'énoncé du pb nous donne:

                (P1) ∀X: ∀Y: (X ≠ Y) ⇒ ∃d (Xp ∧ ¬Yp) ∨ (¬Xp ∧ Yp)

                (P2) B1p ⇔ ¬B2p
                (P3) R1p ⇔ ¬R2p

                (P4) R2p ⇔ Ap ∧ B2p

                (P5) Ap ∧ B3p ⇒ B1p

                (P6) ∀X: (Ap ∧ Xp ⇒ B1p) ⇒ (Xp ⇒ B3p)


        Montrons `B3p ⇒ R1p`:

                  B3p ⇒ R1p

                ⇔ B3p ⇒ ¬R2p          on peut remplacer R1p par ¬R2p        d'après (P3)

                ⇔ B3p ⇒ ¬Ap ∨ ¬B2p    "                ¬R2p par ¬Ap ∨ ¬B2p  d'après (P4)

                ⇔ ¬(B3p ∧ Ap ∧ B2p)   d'après la formule: (A ⇒ B) ⇔ ¬(A ∧ ¬B)
                                      dire que A est vrai équivaut à dire qu'elle n'est pas fausse

        Supposons `B3p ∧ Ap ∧ B2p`:

                (B1p ∧ B2p) ⊥ (P2)    on peut remplacer B3p ∧ Ap par B1p d'après (P5)

        Ceci prouve `¬(B3p ∧ Ap ∧ B2p)` et donc `B3p ⇒ R1p`.

        En français:

                Supposons qu'un jour le barbier, Alfredo et Benito portent tous une perruque.
                D'après (P5), on sait que Bernardo est un suiveur d'Alfredo et Benito.
                Donc, ce jour-là, Bernardo porte lui-aussi une perruque.
                Ceci est impossible car Bernardo et Benito ont des comportements opposés, cf. (P2).

                Donc, il n'existe aucun jour de l'année où le barbier, Alfredo et Benito portent la perruque.

                Considérons un jour où le barbier porte la perruque.
                D'après le résultat précédant, on sait qu'Alfredo et Benito ne portent pas tous les 2
                la perruque ce même jour.
                Or, d'après (P4), Ramano porte la perruque ssi Alfredo et Benito la portent simultanément.
                Donc, ce jour-là, Ramano ne porte pas la perruque.

                Enfin, d'après (P3), Ramano et Roberto ont des comportements opposés.
                Donc, ce jour-là, Roberto porte la perruque: Roberto est un suiveur du barbier.


        Montrons `R1p ⇒ B3p`:

                D'après (P6), si on prouvait `Ap ∧ R1p ⇒ B1p`, alors on prouverait `R1p ⇒ B3p`.
                Or:

                            Ap ∧ R1p ⇒ B1p
                       ⇔    Ap ∧ R1p ⇒ ¬B2p
                       ⇔  ¬(Ap ∧ R1p ∧ B2p)

                Supposons `Ap ∧ R1p ∧ B2p`:

                          Ap ∧ R1p  ∧ B2p
                      ⇔ (R2p ∧ R1p) ⊥ (P3)     on peut remplacer Ap ∧ B2p par R2p, d'après (P4)

                Ceci prouve que `Ap ∧ R1p ∧ B2p` est faux, donc que `Ap ∧ R1p ⇒ B1p` est vrai,
                et donc (d'après (P6)) que `R1p ⇒ B3p`.

        En français:

                Supposons qu'un jour Alfredo, Roberto et Benito portent tous une perruque.
                D'après (P4), on sait que Ramano est un suiveur d'Alfredo et Benito.
                Donc, ce jour-là, Ramano porte lui-aussi une perruque.
                Ceci est impossible car Roberto et Ramano ont des comportements opposés, cf. (P3).

                Donc, il n'existe aucun jour de l'année où Alfredo, Roberto et Benito portent la perruque.
                Ceci équivaut à dire que si Alfredo et Roberto portent la perruque, alors Benito ne la porte pas.
                Ou encore, que si Alfredo et Roberto portent la perruque, alors Bernardo la porte aussi.

                Donc, Bernardo est un suiveur d'Alfredo et Roberto.
                Ceci implique, d'après (P6), que le barbier est un suiveur de Roberto.


        Conclusion:

                    (B3p ⇒ R1p) ∧ (R1p ⇒ B3p)
                ⇒   B3p ⇔ R1p
                ⇒   B3p = R1p
                ⇒   le barbier est Roberto, et sa perruque est donc rouge

### The Mystery of the Photograph
#### L'exact diseur de vérité et l'inexact menteur

2 frères jumeaux se distinguent par le fait que l'un ne se trompe jamais et dit tjrs la vérité,
tandis que l'autre se trompe tjrs et ment tjrs.
Quelle question totale pourriez-vous poser à l'un d'eux pour l'identifier ?

        Êtes-vous le diseur de vérité exact ?

        Soit A et B, resp. le diseur de vérité et le menteur.

        Si on pose la question précédente à A, son exact jugement lui fera penser que la réponse est oui,
        et comme il dit la vérité il répondra oui.

        Si on pose la question à B, son INexact jugement lui fera penser que oui, mais comme il ment
        il répondra non.


                                     NOTE:

        Ceci est la réponse du livre.  Perso, j'avais pensé à:

                Votre jugement est-il exact ?

        Il me semble que ça marche aussi…

#### Distinguer les 4 frères

4 frères sont des quadruplet indistinguables en apparence physique.
Leur nom et leur comportement sont les suivants:

        Arthur     diseur de vérité exact
        Bernard    diseur de vérité inexact
        Charles    menteur exact
        David      menteur inexact

Un jour, vous rencontrez l'un des 4 frères dans la rue et vous souhaitez connaître son prénom.
Quel est le nb de minimums de questions totales à lui poser, et quelles sont ces questions ?

        2 + 2 = 4 ?

                Arthur     oui
                Bernard    non
                Charles    non
                David      oui

        Si la réponse est oui, on sait que la personne est Arthur ou David, et donc on poursuit
        avec "Êtes-vous Arthur?":

                Arthur     oui
                David      non

        Si la réponse est non, on sait que la personne est Bernard ou Charles, et donc on poursuit
        avec "Êtes-vous Bernard?":

                Bernard    non
                Charles    oui


                                     NOTE:

        Ceci est la réponse du livre.  Perso, j'avais pensé à:

        Votre jugement est-il exact ?

                Arthur     oui
                Bernard    oui
                Charles    non
                David      non

        Dites-vous la vérité ?

                Arthur     oui
                Bernard    non
                Charles    oui
                David      non

        Les réponses à ces 2 questions suffisent à identifier chaque frère:

                Arthur     oui oui
                Bernard    oui non
                Charles    non oui
                David      non non


#### Marié/célibataire et/ou riche/pauvre

Arthur et Bernard sont mariés, Charles et David sont célibataires.
Arthur et Charles sont riches, Bernard et David sont pauvres.

Un jour, vous rencontrez l'un des 4 frères dans la rue.
Quelle question totale de 3 mots pourriez-vous lui poser pour savoir s'il est marié ?

        Êtes-vous riche ?

                Arthur     oui
                Bernard    oui
                Charles    non
                David      non

        Si la personne répond oui, on sait qu'il s'agit d'Arthur ou Bernard, qui sont tous les 2 mariés.
        Si elle répond non, il s'agit de Charles et David, qui sont tous les 2 célibataires.


                                     NOTE:

        De la même façon, si on voulait savoir si la personne est riche, il faudrait lui demander si
        elle est mariée.


#### Question inutile

Un jour, vous rencontrez l'un des 4 frères, et vous lui posez une question.
Aussitôt, vous vous rendez compte que poser la question était inutile car vous connaissez d'avance la réponse.

Quelle était la question ?

        La question doit contenir un mot variable du genre "vous".

        Êtes-vous un diseur de vérité exact / Arthur ?

                Arthur     oui
                Bernard    oui
                Charles    oui
                David      non

        Ça marche pas à cause de David qui répond non.
        On pourrait essayer d'ajouter la proposition "ou David" pour forcer David à répondre oui.

        ┌─────────────────────────────┐
        │ Êtes-vous Arthur ou David ? │
        └─────────────────────────────┘

                Arthur     oui
                Bernard    oui
                Charles    oui
                David      oui

#### Une ou deux questions

Vous devez deviner l'identité d'un des 4 frères via une ou 2 questions totales.

Vous devez décider à l'avance si vous poserez une ou 2 questions.
Si vous choisissez la stratégie à 1 question et que vous devinez l'identité du frère, vous gagnerez 1000 dollars.
"                                 2 questions                                                        100 dollars.

Quelle stratégie devriez-vous choisir ?

        Celle à 1 question.

        La stratégie à 2 questions permet d'identifier la personne dans 100% des cas, et rapporte 100 dollars.

        Celle à 1 question permet d'éliminer la moitié des possibilités (4 frères → 2 frères).
        Puis, on peut choisir arbitrairement l'un des 2 frères possibles restants.
        On a 50% de chances de trouver le bon.

        En moyenne, cette stratégie nous rapporte 500 dollars (> 100 dollars).


#### Pensez-vous que 2+2=4 ?

Si on demande aux 4 frères si 2+2 fait bien 4, quelle sera la réponse de chacun ?

        ┌─────────┬─────────────┬────────────┬─────────┐
        │         │ évaluation  │ évaluation │ réponse │
        │         │ proposition │ pensée     │         │
        ├─────────┼─────────────┼────────────┼─────────┤
        │ Arthur  │ oui         │ oui        │ oui     │
        │ Bernard │ non         │ oui        │ oui     │
        │ Charles │ oui         │ oui        │ non     │
        │ David   │ non         │ oui        │ non     │
        └─────────┴─────────────┴────────────┴─────────┘

Pour pouvoir répondre, chaque frère doit passer par 3 étapes:

   1. évaluer la proposition "2+2=4"; ceci va produire une pensée
   2. évaluer la pensée précédente
   3. répondre

Le résultat des étapes 1 et 2 dépend de l'exactitude du frère.
Le résultat de l'étape 3 dépend de son honnêteté.

                                     NOTE:

On remarque que cette question permet de distinguer les menteurs des diseurs de vérité,
en faisant abstraction de leur exactitude.

Vous posez les 2 questions suivantes à l'un des 4 frères:

   > Est-ce que 2+2=4 ?
   > Pensez-vous que 2+2=4 ?

Il répond resp. non et oui.  De quel frère s'agit-il ?

Puisqu'il répond non à la 1e question, on sait que son jugement est incorrect.
Et comme il répond oui à la 2e question, on sait qu'il dit la vérité.

Donc, il s'agit de Bernard.

#### Metapuzzle des 4 frères

Un jour, un logicien rencontra l'un des 4 frères et lui demanda "Qui êtes-vous ?".
La personne lui répondit en lui donnant UN prénom (Arthur, Bernard, Charles ou David), et le logicien
sut de quel frère il s'agissait réellement.

Qques minutes plus tard, un second logicien rencontra ce même frère.
Cette fois, le logicien lui demanda "Qui pensez-vous être ?".
La personne lui répondit en lui donnant UN prénom, et le logicien sut à nouveau de quel frère il s'agissait.

On considère que la personne ment ssi elle dit qch qu'elle pense être faux.
Ceci implique qu'une personne disant la vérité peut dire qch qui n'est pas exactement ce qu'elle pense,
et qu'elle peut dire qch dont elle ne sait pas si c'est vrai ou non.

Quel frère les 2 logiciens ont-ils rencontré ?


                Q: Qui êtes-vous ?

                ┌───────┬───────────────────┬──────────┐
                │ Frère │ qui il pense être │ réponse  │
                ├───────┼───────────────────┼──────────┤
                │ A     │ A                 │ A        │
                │ B     │ A ∨ C ∨ D         │ A, C, D  │
                │ C     │ C                 │ A, B, D  │
                │ D     │ A ∨ B ∨ C         │ D        │
                └───────┴───────────────────┴──────────┘

        Si la personne avait répondu "Arthur" ou "David" à la question du 1er logicien, alors ce dernier
        n'aurait pas pu en déduire son réel prénom.
        En effet, plusieurs frères pouvaient répondre "Arthur" ou "David".

        En revanche, seul Bernard pouvait répondre "Charles" et seul Charles pouvait répondre "Bernard".
        Donc, si le logicien a été capable de déduire le réel prénom de la personne en face de lui,
        ça implique qu'elle a répondu "Charles" ou "Bernard", et qu'il s'agissait de Bernard ou de Charles.


                                     NOTE:

        Bernard a pu répondre "Arthur", ou "Charles", ou "David".
        Quelle que fut sa réponse, elle a été différente de sa pensée qui, elle, était:

                Je suis Arthur ou Charles ou David

        Bien que sa réponse fut différente de sa pensée, il a bien dit la vérité, comme l'exige sa
        condition de diseur de vérité.
        Pex, s'il a répondu "Arthur", dans son esprit, Arthur étant une identité possible, il n'a pas
        menti (cf. la définition du mensonge dans l'énoncé), donc il a dit la vérité.


                Q: Qui pensez-vous être ?

                ┌───────┬───────────────────┬──────────────────────────┬─────────────────┐
                │ Frère │ qui il pense être │ qui il pense qu'il pense │ ce qu'il répond │
                │       │                   │ être                     │                 │
                ├───────┼───────────────────┼──────────────────────────┼─────────────────┤
                │ A     │ A                 │ A                        │ A               │
                │ B     │ A ∨ C ∨ D         │ ¬A ∧ ¬C ∧ ¬D             │ B               │
                │ C     │ C                 │ C                        │ A, B, D         │
                │ D     │ A ∨ B ∨ C         │ ¬A ∧ ¬B ∧ ¬C             │ A, B, C         │
                └───────┴───────────────────┴──────────────────────────┴─────────────────┘

        Si la personne avait répondu "Arthur" ou "Bernard" à la question du 2e logicien, alors ce dernier
        n'aurait pas pu en déduire son réel prénom.
        En effet, plusieurs frères pouvaient répondre "Arthur" ou "Bernard".

        En revanche, seul Charles pouvait répondre "David" et seul David pouvait répondre "Charles".
        Donc, si le logicien a été capable de déduire le réel prénom de la personne en face de lui,
        ça implique qu'elle a répondu "David" ou "Charles", et qu'il s'agissait de Charles ou de David.

        Conclusion:
        la seule personne que le 1er et le 2e logicien peuvent avoir rencontré est Charles.

        Ce dernier a répondu "Bernard" et "David" aux questions des logiciens.
        À chaque fois, il a correctement menti, et à chaque fois les logiciens ont pu déduire son identité
        car seul lui pouvait fournir ces réponses.


#### Le mystère de la photographie

Vous rendez visite aux 4 frères.
Dans le salon de leur maison, se trouve une photographie montrant l'un d'eux.
Vous demandez à chacun d'eux:

        Est-ce vous sur la photo ?

3 d'entre eux répondent "non", et un répond "oui".

Puis, vous demandez à chacun d'eux:

        Pensez-vous que vous êtes sur la photo ?

À nouveau, 3 d'entre eux répondent "non", et un répond "oui".

Qui est sur la photo ?


                Est-ce vous sur la photo ?

        Supposons que A est sur la photo, les réponses seront:

                ┌───────┬─────────────────────────┬─────────┐
                │ Frère │ pense être sur la photo │ réponse │    ✘
                ├───────┼─────────────────────────┼─────────┤
                │ A     │           oui           │   oui   │
                │ B     │           oui           │   oui   │
                │ C     │           non           │   oui   │
                │ D     │           oui           │   non   │
                └───────┴─────────────────────────┴─────────┘

        Supposons que D est sur la photo, les réponses seront:

                ┌───────┬─────────────────────────┬─────────┐
                │ Frère │ pense être sur la photo │ réponse │    ✘
                ├───────┼─────────────────────────┼─────────┤
                │ A     │           non           │   non   │
                │ B     │           oui           │   oui   │
                │ C     │           non           │   oui   │
                │ D     │           non           │   oui   │
                └───────┴─────────────────────────┴─────────┘

        A et D ne peuvent pas être sur la photo, car 3 frères sur 4 répondraient "oui" à la question,
        et seulement un répondrait "non".

        On peut facilement montrer que si B ou C se trouve sur la photo, alors 3 frères sur 4 répondraient
        "non" et un répondrait "oui".  Si B est sur la photo, seul C répondrait "oui", et inversement,
        si C est sur la photo, seul B répondrait "oui".

        +----------------------------------+
        | Le frère sur la photo est B ou C |
        +----------------------------------+

                Pensez-vous que vous êtes sur la photo ?

        Supposons que A est sur la photo, les réponses seront:

                ┌───────┬─────────────────────────┬─────────────────────────────────────┬─────────┐
                │ Frère │ pense être sur la photo │ pense qu'il pense être sur la photo │ réponse │    ✘
                ├───────┼─────────────────────────┼─────────────────────────────────────┼─────────┤
                │ A     │           oui           │                 oui                 │   oui   │
                │ B     │           oui           │                 non                 │   non   │
                │ C     │           non           │                 non                 │   oui   │
                │ D     │           oui           │                 non                 │   oui   │
                └───────┴─────────────────────────┴─────────────────────────────────────┴─────────┘

        Supposons que B est sur la photo, les réponses seront:

                ┌───────┬─────────────────────────┬─────────────────────────────────────┬─────────┐
                │ Frère │ pense être sur la photo │ pense qu'il pense être sur la photo │ réponse │    ✘
                ├───────┼─────────────────────────┼─────────────────────────────────────┼─────────┤
                │ A     │           non           │                 non                 │   non   │
                │ B     │           non           │                 oui                 │   oui   │
                │ C     │           non           │                 non                 │   oui   │
                │ D     │           oui           │                 non                 │   oui   │
                └───────┴─────────────────────────┴─────────────────────────────────────┴─────────┘

        A et B ne peuvent pas être sur la photo, car 3 frères sur 4 répondraient "oui" à la question,
        et seulement un répondrait "non".

        On peut facilement montrer que si C ou D se trouve sur la photo, alors 3 frères sur 4 répondraient
        "non" et un répondrait "oui".  Si C est sur la photo, seul D répondrait "oui", et inversement,
        si D est sur la photo, seul C répondrait "oui".

        ┌──────────────────────────────────┐
        │ Le frère sur la photo est C ou D │
        └──────────────────────────────────┘


        Conclusion: le frère sur la photo est C, car:

        X étant sur la photo,    X ∈ {B, C} ∩ {C, D} = {C}

## Knights, Knaves, And The Fountain Of Youth
### Some Unusual Knights and Knaves
