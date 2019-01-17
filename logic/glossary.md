# a

        argument

                An argument is a set of statements, some of which (the premises)
                are claimed to provide support for another (the conclusion).

# c

    contingent

            Une combinaison de déclarations est dite 'contingent' en anglais, si
            sa valeur  de vérité varie  et dépend des  valeurs de vérité  de ses
            composants.

            “to be contingent on” is synonymous with “to depend on”.


    contradictoire

            Une combinaison  de déclarations  qui est  tjrs fausse,  peu importe
            la  valeur  de  vérité   des  composants,  est  dite  contradictoire
            (self-contradictory).

            'Contradictoire' est aussi utilisé  pour qualifier 2 combinaisons de
            déclarations dont les valeurs de vérité sont tjrs opposées.


    equivalent
    contradictory
    consistent
    inconsistent

            On peut comparer 2 combinaisons de déclarations via leur table de vérité.
            En anglais, on dit qu'elles sont :

                    - 'equivalent'       si leurs valeurs de vérité sont    identiques     sur toutes les lignes
                    - 'contradictory'    si leurs valeurs de vérité sont    différentes    sur toutes les lignes

                    - 'consistent'       s'il existe une ligne sur laquelle les 2 sont vraies simultanément
                    - 'inconsistent'     s'il n'existe aucune une ligne sur laquelle les 2 sont vraies simultanément

# i

    premise / conclusion indicator

            Word introducing a premise / conclusion.

            Ex:

                    Therefore    conclusion indicator
                    Since        premise indication

            Un  indicateur  de  prémisse peut  introduire  plusieurs  prémisses,
            séparées par des conjonctions de coordination tq et / ou / mais ...
            Parfois, un argument ne contient aucun indicateur.
            Dans ce  cas, généralement,  la conclusion  est rédigée  en premier,
            puis viennent les prémisses.


    inference

            Une inférence  est le processus  de pensée permettant de  passer des
            prémisses à la conclusion.
            Elle peut être déductive ou inductive.
            En pratique, on confond "inférence" avec "argument".

# l

    logic

            The purpose of  logic is to provide methods allowing  us to evaluate
            others' arguments, and build our own ones.


    modal logic

            Kind of logic using concepts such as possibility, necessity, belief,
            doubt...


    categorical   logic
    propositional logic

                All men are mortal                          Every H is M
                Socrates is a man                           x is an H
                Socrates is mortal                          Thus, x is an M

                Tous les hommes sont mortels       formalisation            Tout H est M
                Socrates est un homme                   en             →    x est un H
                Socrates est mortel             logique catégorique         Donc, x est un M

                Différences entre logique catégorique et propositionnelle:

                        - En logique catégorique, les symboles (ici H, M, x)
                          représentent des catégories/membres. Par convention,
                          on utilise des maj pour les catégories, et des
                          minuscules pour les membres.

                          En logique propositionnelle, les symboles représentent
                          des propositions.

                        - Une catégorie n'a pas de valeur de vérité
                          (contrairement à une proposition).

                        - En logique catégorique, on construit une proposition
                          en exprimant une relation entre plusieurs catégories:
                          la relation est de type appartenance / exclusion
                          totale / partielle

                          En logique  propositionnelle, on  ne construit  pas de
                          propositions, mais des combinaisons de propositions.

                        - La logique catégorique s'intéresse au contenu des
                          propositions ("micro logique"), tandis que la logique
                          propositionnelle s'intéresse aux relations entre
                          propositions ("macro logique").

                        - On représente et teste la validité d'un argument
                          catégorique via un diagramme de Venn.

                          En logique propositionnelle, on représente et teste la
                          validité  d'une combinaison  de propositions,  via une
                          table de vérité.

# p

    Predicate Calculus / calcul des prédicats / logique du 1er ordre

            Il s'agit d'une formalisation du langage des mathématiques, proposée par Gottlob Frege
            (fin 19e-début 20e siècle).
            Elle combine la logique catégorique et propositionnelle.


    proposition

            Une proposition est le contenu sémantique (sens) d'une déclaration, même si en pratique
            on confond "proposition" avec "déclaration".


# s

    si
    ssi (iff)

            Dans  une phrase  naturelle,  comment  comprendre intuitivement  les
            conjonctions de coordination “si“ et “ssi“ ?

            Prenons 2 exemples de phrases:

                    ┌ B
                    ├────────────────────┐
                    Le fichier sera écrasé si il ressemble à un fichier de session.
                                              ├──────────────────────────────────┘
                                              └ A

            Peut être réécrit formellement:

                    A ⇒ B :  SI le fichier ressemble à un fichier de session, ALORS il sera écrasé.


                    ┌ B
                    ├────────────────────┐
                    Le fichier sera écrasé ssi il ressemble à un fichier de session.
                                               ├──────────────────────────────────┘
                                               └ A

            Peut être réécrit formellement:

                         A  ⇒  B  : pareil qu'avant
                    +
                        ¬A  ⇒ ¬B  : SI le fichier ne ressemble pas à un fichier de session,
                                    ALORS il ne sera pas écrasé


            Résumé:

                    1. dans une langue naturelle, on écrit souvent:

                               B si A

                       qu'il faut automatiquement interpréter comme:

                               si A alors B


                    2. “ssi“ peut être lu dans n'importe quelle direction (A ⇒ B ou B ⇒ A)
                                       et dans n'importe quelle voie (affirmative ou négative)


                    3. “ssi“ est souvent utilisé pour signifier:

                                                ┌ toute cette partie est ajoutée par le 2e “s“
                                                ├────────────┐
                               si B alors A  +  si ¬B alors ¬A
                               ├──┘             ├───┘
                               │                └ et nécessaire
                               │
                               └ condition suffisante


    syllogisme

            Un syllogisme est un argument  composé d'un ensemble de propositions
            catégoriques et qui applique un raisonnement déductif pour arriver à
            une conclusion.
            Ex:

                    Tous les hommes sont mortels    prémisse majeure
                    Socrates est un homme           prémisse mineure
                    Socrates est mortel             conclusion

    statement

            A statement is a sentence which can be true or false.

            A  question,  exclamation, suggestion,  command  can't  be true  nor
            false, thus it's NOT a statement.

# t

    tautology

            Une tautologie est une combinaison  de déclarations qui est toujours
            vraie, peu importe la valeur de vérité de ces dernières.

