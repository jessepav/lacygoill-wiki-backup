# Sélecteurs

https://css-tricks.com/how-css-selectors-work/


Un sélecteur CSS permet de sélectionner un élément HTML et de lui appliquer un style.

    * {}

            sélecteur universel:
            cible tous les éléments de la page


    .navigation ul * {}

            Sélectionne  tous  les  descendants  (space *)  d'un  élément  <ul>,
            lui-même descendant d'un élément portant la classe `navigation`.

            Illustre  que *  peut  se  trouver au  milieu  d'une combinaison  de
            sélecteurs CSS.


    h1, h2, h3 {}

            sélecteur de type:
            cible des éléments par leur type (nom)

            Ici, le sélecteur cible les éléments h1 ET h2 ET h3.


    .note {}

            sélecteur de classe:
            cible les éléments portant une classe dont la valeur est `note`


    p.note {}

            cible les paragraphes portant une classe dont la valeur est `note`


    #introduction {}

            sélecteur d'ID:
            cible les éléments dont la valeur de l'attribut ID est `introduction`


    li > a {}

            sélecteur d'enfant:     cible les éléments <a> enfants d'un élément <li>
                                    <a> doit être enfant direct de <li>

                                    > = enfant direct


    .module > h2 {}

            Sélectionne les éléments h2  directement enfant d'un élément portant
            la classe `module`.


    p a {}

            sélecteur de descendant:

                                    cible les éléments <a> au sein d'éléments <p>
                                    <a> peut être un petit-enfant, arrière-petit enfant, ...

                                    espace (entre p et a) = enfant qcq


    h1 + p {}

            sélecteur de frère adjacent:

                                    cible les éléments <p> qui suivent directement (frère) un élément <h1>


    h1 ~ li {}

            sélecteur de frère général:

                                    cible les éléments <li> qui suivent et sont frères d'un élément <h1>
                                    ~ = frère suivant qcq

            `>`, `+` et `~` sont des opérateurs de combinaison de sélecteurs CSS.


    .foo.bar

            sélectionne les éléments portant les classes `foo` et `bar`


    [an_attribute="my_value"] {}

            sélecteur d'attribut qcq (!= style, != id, != class)

            Un  sélecteur  d'attribut  est  plus  puissant  qu'un  sélecteur  de
            classe car  il peut être  utilisé avec n'importe quel  attribut (pas
            uniquement `class`), et on peut en plus (en option) l'associer à une
            valeur pour + de granularité.


    tag[attr] {}

            sélectionne les balises `tag` portant l'attribut `attr`


    :nth-child(2) {}

            sélecteur positionnel

            Ici, le sélecteur cible tous les éléments qui sont le 2e enfant d'un
            autre élément.


    :empty

            pseudo-classe ciblant un élément dont le contenu est vide

                                     NOTE:

            Un espace ou un newline n'est pas considéré comme un contenu vide:

                    <div> </div>    ✘

                    <div>           ✘
                    </div>

            Un commentaire est considéré comme un contenu vide:

                    <aside data-blah><!-- nothin' --></aside>    ✔

                                     NOTE:

            Une pseudo-classe  est introduite par le caractère   `:`
            Un  pseudo-élément est introduit  par les caractères `::`


            Une  pseudo-classe permet  de cibler  des éléments  existants en  se
            basant sur une information qui réside en-dehors de l'arbre DOM.
            Ex:

                    :active         :    élément mis en surbrillance
                    :hover          :    élément survolé à la souris
                    :first-child    :    1er enfant d'un élément
                    :visited        :    élément visité


            Un pseudo-élément permet  de cibler des éléments  virtuels, i.e. qui
            n'existent même pas dans l'arbre DOM.
            Ex:

                    ::after         :    dernier enfant virtuel de l'élément qui précède les ::

                                         On peut modifier le contenu de cet élément virtuel via
                                         la propriété CSS `content`.

                    ::before        :    premier enfant virtuel de l'élément qui précède les ::

                    ::first-line    :    1e ligne de l'élément précédant
                    ::first-letter  :    1e lettre de la 1e ligne de l'élément précédant

                    ::selection     :    portion du document mis en surbrillance au sein de l'élément précédant

# Spécificité

https://css-tricks.com/specifics-on-css-specificity/


Qd 2  déclarations de 2  sélecteurs CSS modifient  une même propriété  d'un même
élément HTML, mais chacune différemment,  le navigateur doit décider laquelle il
faut honorer.
Pour ce faire, il suit un ensemble de règles de spécificité.

    .favorite {
        color: red;
    }

    .favorite {
        color: black;
    }

            Dans cet exemple,  les éléments portant la  classe `favorite` seront
            affichés en noir, car la  2e déclaration `color: black;` apparaît en
            dernière.
            Ceci  illustre qu'à  spécificité  égale, la  dernière déclaration  a
            priorité sur les autres.


    HTML                                                         CSS

    <ul id="summer-drinks">                                      ul#summer-drinks > li.favorite {
        <li class="favorite">Whiskey and Ginger Ale</li>            color: red;
        <li>Wheat Beer</li>                                      }
        <li>Mint Julip</li>                                 +
    </ul>                                                        .favorite {
                                                                     color: black;
                                                                 }

            Ici, la couleur appliquée à l'item  "Whiskey and Ginger" ne sera pas
            noire  comme  le demande  la  déclaration  au  sein  du 2e  bloc  de
            déclarations, mais rouge.
            Pk ?
            Car le 1er sélecteur est + spécifique que le 2e.


            La spécificité d'une déclaration est donnée par 5 nombres:

                    !important     style attribute      ID     Class,            Elements,
                                >  (inline styling)  >      >  pseudo-class,  >  pseudo-element
                                                               attribute

                    Le 1er nb vaut 1 si la déclaration est suivie de       '!important',    0 autrement.
                    Le 2e     vaut 1 si l'élément HTML porte l'attribut    `style`,         0 autrement.
                    Le 3e     vaut 1 si la sélecteur utilise l'attribut    `id`,            0 autrement.

                    Le 4e vaut n, n étant le nb d'attributs utilisés par le sélecteur, autres que `style` et `id`.
                    Le 5e vaut n, n étant le nb d'éléments  utilisés par le sélecteur.


Exemples de valeurs de spécificité:

    ul#nav li.active a

            0, 0, 1, 1, 3

    body.ie7 .col_3 h2 ~ h2

            0, 0, 2, 3

    #footer *:not(nav) li

            0, 0, 1, 0, 2

            Le sélecteur universel n'ajoute aucune spécificité.

            La pseudo-classe :not() n'ajoute aucune spécificité en elle-même.
            En revanche, ce qui est contenu entre ses parenthèses oui.

    <li style="color: red;">

            0, 1, 0, 0, 0

    ul > li ul li ol li::first-line

            0, 0, 0, 0, 7

            ::first-line est un pseudo-élément

# Propriétés

    * {
        -webkit-box-sizing:    border-box;
        -moz-box-sizing:       border-box;
        -ms-box-sizing:        border-box;
        box-sizing:            border-box;
    }

            La largeur d'une boîte varie donc en fonction de plusieurs données:

                    width(box) = padding (left & right) + border (left & right) + width (content)

            À  chaque fois  qu'on  change  la valeur  d'une  des propriétés  CSS
            précédentes, la largeur de la boîte change aussi.
            Ceci peut  poser pb si  on veut changer une  de ces valeurs  tout en
            conservant une largeur de boîte constante.

            La propriété CSS 'border-box' résoud  ce pb en modifiant les valeurs
            des  autres  propriétés afin  de  maintenir  la  largeur de  la  box
            constante.

            Cependant, comme  cette propriété est relativement  récente, il faut
            ajouter des "CSS vendor prefixes",  afin de garantir le support pour
            d'anciens navigateurs.

            Ces préfixes sont:

                    -webkit
                    -moz
                    -ms

##
# Links
## linter

        https://github.com/CSSLint/csslint

## validator

        https://jigsaw.w3.org/css-validator/

## vim plugins

        https://github.com/chrisbra/Colorizer/

