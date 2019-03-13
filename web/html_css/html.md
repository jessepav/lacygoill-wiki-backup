# How to view the source code of a webpage in Vim directly from Firefox?

Go to `about:config`, and set these options:

    view_source.editor.external true
    view_source.editor.path     /usr/bin/urxvt
    view_source.editor.args     -e vim

Now, when  you'll right-click and  select `View Page  Source` on a  webpage, the
source code will be opened in Vim.

##
# balises
## esthétique

    <br>

            saut de ligne

            Utile pour une adresse ou un poème, où les retours à la ligne ont du
            sens.

            Ne pas  utiliser <br>  pour augmenter l'espace  entre des  lignes de
            texte.
            Utiliser la propriété CSS `margin` ou l'élément <p>.

            Ex d'utilisation:


                    Mozilla Foundation<br>
                    1981 Landings Drive<br>
                    Building K<br>
                    Mountain View, CA 94043-0801<br>
                    USA


    <b> ... </b>

            Mettre en gras afin d'attirer l'attention du lecteur.

            Style par défaut:    mise en gras

            Ex d'utilisation:    <b>: mots-clés dans un document abstrait,
                                      noms de produits dans une critique

            Une bonne  pratique consiste à  lui ajouter l'attribut  `class` pour
            transmettre une information sémantique; pex:

                    <b class="lead">

            ... pour la 1e phrase d'un paragraphe.
            Ainsi,  on pourra  définir  plusieurs styles  pour  les balises  <b>
            individuellement.

            <b> ne devrait être utilisé qu'en dernier recours, qd <strong>, <em>
            et mark> ne conviennent pas.
            Si  la mise  en gras  n'a aucune  valeur sémantique,  il vaut  mieux
            utiliser la propriété CSS `font-weight`.


    <i> ... </i>

            Faire ressortir un  mot/une phrase afin de le/la  faire ressortir du
            texte.

            Style par défaut:    mise en italique

            Utile pour un terme technique, une expression étrangère, les pensées
            intérieures d'un personnage.

            Ex d'utilisation:

                    The <i>Queen Mary</i> sailed last night.

                    The word <i>the</i> is an article.

                    The Latin phrase <i>Veni, vidi, vici </i>is often mentioned in music, art, and literature.

            Contrairement à <em>, il n'y a aucune accentuation sur le mot "Queen
            Mary".
            <i> indique simplement  que "Queen Mary" n'est pas à  prendre au 1er
            degré, il ne  s'agit pas réellement d'une reine  appelée Marie (mais
            un bateau qui porte ce nom).

            Comme pour <b>, une bonne pratique consiste à lui ajouter l'attribut
            `class` pour transmettre une information sémantique.
            Ainsi,  on pourra  définir  plusieurs styles  pour  les balises  <i>
            individuellement.

## sémantique

    <strong> ... </strong>

            Donne au texte une forte importance.

            Style par défaut:    mise en gras

            Comme  pour  <b>,  <strong>  a pour  but  d'attirer  l'attention  du
            lecteur.
            Mais contrairement  à <b>,  le style de  <strong> peut  être modifié
            dans un fichier css.
            On  pourrait aussi  modifier l'apparence  de <b>,  mais ça  n'aurait
            aucun sens.

            <b> sert  à mettre en  gras, sans  donner aucun sens  particulier au
            texte.
            <strong> sert  à donner une grande  importance au texte, ce  qui par
            défaut se traduit par une mise en gras.

            Ex d'utilisation:

                    When doing x it is <strong>imperative</strong> to do y before proceeding.

    <em> ... </em>

            Place  une accentuation  sur le  texte s'il  devait être  prononcé à
            haute voix.

            Style par défaut:    mise en italique

            Ex d'utilisation:

                    We <em>had</em> to do something about it.


    <mark> ... </mark>

            Indique la pertinence du texte dans un contexte donné.

            Style par défaut:    mise en surbrillance jaune

            Ça peut servir,  par exemple, à mettre en  surbrillance chaque terme
            correspondant  à  une  recherche  de  l'utilisateur,  sur  une  page
            montrant des résultats de recherche.

            Ne pas  utiliser <mark> pour  de la coloration  syntaxique; utiliser
            <span> dans ce cas.

            Au sein d'une citation, indique que le texte est référencé en-dehors
            de cette dernière.


    <blockquote> ... </blockquote>

            Indique que le texte est une citation longue (avec newline).

                    <blockquote cite="http://developer.mozilla.org">
                        <p>This is a quotation taken from the Mozilla Developer Center.</p>
                    </blockquote>

            Généralement, les navigateurs indentent la citation.

            On peut  ajouter l'attribut `cite` afin  de définir une url  d'où la
            citation est tirée.


    <q> ... </q>

            Indique que  le texte est une  courte citation tenant sur  une seule
            ligne (pas de newline).
            Généralement, les  navigateurs mettent  des guillemets autour  de la
            citation.
            Ex:

                    <p>Everytime Kenny is killed, Stan will announce
                    <q cite="http://en.wikipedia.org/wiki/Kenny_McCormick#Cultural_impact">
                        Oh my God, you/they killed Kenny!
                    </q>.
                    </p>

            Comme pour <blockquote>,  on peut ajouter l'attribut  `cite` afin de
            définir une url d'où la citation est tirée.


    <cite> ... </cite>

            Fait référence à une œuvre originale.

            Ce peut  être un livre,  journal, essai, poème,  partition musicale,
            chanson, script, film, série TV,  jeu, sculpture, peinture, pièce de
            théâtre, opéra, comédie  musicale, programme informatique, site/page
            web,  post  sur  un   blog/forum,  commentaire,  tweet,  déclaration
            orale...

            Doit inclure le titre de l'œuvre ou une URL de référence.


    <dfn> ... </dfn>

            Encadre un terme pour lequel on est en train de fournir une définition.

## listes

    <ul>
        <li>...</li>
        <li>...</li>
        ...
    </ul>

            Liste non ordonnée.


    <ol>
        <li>...</li>
        <li>...</li>
        ...
    </ol>

            Liste ordonnée.


    <dl>
        <dt>...</dt>
        <dd>...</dd>

        <dt>...</dt>
        <dd>...</dd>

        ...
    </dl>

            Liste de couples:    terme - description

            Utile pour afficher un glossaire (jargon, liste de voca technique, ...),
            ou des métadonnées (clés-valeurs d'un dico).

                    <dl>
                        <dt>Name</dt>
                        <dd>Godzilla</dd>

                        <dt>Born</dt>
                        <dd>1952</dd>

                        <dt>Birthplace</dt>
                        <dd>Japan</dd>

                        <dt>Color</dt>
                        <dd>Green</dd>
                    </dl>

## div / span

Un div est une division du document HTML, aka un bloc.


Une box est composée de 3 parties:

        - content
        - padding    couleur héritée du background de la box
        - border     couleur héritée de la couleur de la box

Pour compléter le modèle d'une boîte, il faut ajouter une 4e partie, la marge, qui sépare les boîtes
entre elles:

        - margin     transparent

##
# id / class

`id` et `class` sont des attributs  html permettant de construire des sélecteurs
css, et d'appliquer des styles à des éléments HTML.

Les 2 s'utilisent différemment:

        - Une balise html ne peut porter qu'un seul id.

        - Un id donné ne peut apparaître qu'une seule fois par page html.
          Pk? Pour 2 raisons:

                  1. un id peut servir d'ancre dans un lien hypertexte; ex:

                          http://www.mon_site.com/ma_page#mon_id

                  2. la fonction javascript getElementById() ne serait pas fiable autrement


        - Une balise html peut porter plusieurs classes différentes; ex:

                  <div class="widget big"></div>

          ... ici l'élément `div` portent les classes `widget` et `big`.
          On remarque qu'on peut donner plusieurs valeurs à `class` simplement en les séparant
          par des espaces.

        - Une classe donnée peut apparaître plusieurs fois sur une même page html.



On peut parfaitement utiliser les 2 attributs `class` et `id` sur une même balise.



Conseil:

Qd  on donne  une valeur  à un  id,  ne pas  décrire son  positionnement ou  son
apparence mais plutôt sa fonction (esthétique vs sémantique).

        <div id="right-col">    ✘    `right-col` = colonne droite
        <div id="sidebar">      ✔    `sidebar`   = barre latérale

On devrait réserver l'emploi d'un id à  un élément dont on souhaite manipuler le
style individuellement.
Analogie:    id ≈ numéro de série

On devrait utiliser une classe dès qu'on souhaite modifier le style de plusieurs
éléments simultanément.
Analogie:    class ≈ code-barre, modèle d'un produit



Les classes  et id sont également  utilisés comme métadonnées afin  de donner du
sens à l'information.
Pour ce  faire, on leur donne  des valeurs conventionnelles (fn,  org, tel, url,
vcard) dont  le sens  est défini  par ce qu'on  appelle un  microformat (parfois
abrégé en μF ou uF).

Ça permet  aux infos destinées  aux utilisateurs  finaux et ayant  une structure
constante (telles  qu'un carnet  d'adresses, des coordonnées  géographiques, des
numéros de téléphone,  des événements) d'être utilisées  automatiquement par des
applications desktop ou web (crawlers web, client mail, gestionnaire de contact,
calendrier, Google Maps) via un plugin du navigateur.

Plusieurs microformats  ont été développés,  hCard et hCalendar étant  les seuls
ratifiés par le W3C.

Illustration:

        <ul>
        <li>John Doe</li>
        <li>The Example Company</li>
        <li>604-555-1234</li>
        <li><a href="http://example.com/">http://example.com/</a></li>
        </ul>

... pourrait être formaté comme ceci:

        <ul class="vcard">
        <li class="fn">Joe Doe</li>
        <li class="org">The Example Company</li>
        <li class="tel">604-555-1234</li>
        <li><a class="url" href="http://example.com/">http://example.com/</a></li>
        </ul>

Dans cet exemple, le nom formaté  (fn), l'organisation (org), le n° de téléphone
(tel), l'adresse web  (url) ont été identifiés en utilisant  des noms de classes
spécifiques.
Le tout  est enveloppé dans  une classe 'vcard'  qui indique qu'il  s'agit d'une
hCard (μF): HTML vCard, carte de visite (format de fichier) HTML.

##
# Links
## style guide

        https://google.github.io/styleguide/htmlcssguide.html

## validators

        https://validator.w3.org/
        https://validator.w3.org/checklink
        https://validator.w3.org/i18n-checker/

## resources

        http://learn.shayhowe.com/html-css/
        http://learn.shayhowe.com/advanced-html-css/

## vim plugins

        https://github.com/jceb/emmet.snippets

