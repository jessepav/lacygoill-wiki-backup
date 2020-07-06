# Which abbrevation should I write to get this html code?
## 1

```html
        <div id="page">
            <div class="logo"></div>
            <ul id="navigation">
                <li><a href="">Item 1</a></li>
                <li><a href="">Item 2</a></li>
                <li><a href="">Item 3</a></li>
                <li><a href="">Item 4</a></li>
                <li><a href="">Item 5</a></li>
            </ul>
        </div>
```

↣ div#page>div.logo+ul#navigation>li*5>a{Item $} ↢

## 2

```html
        <div>
            <ul>
                <li></li>
            </ul>
        </div>
```

↣ div>ul>li ↢

## 3

```html
        <div></div>
        <p></p>
        <blockquote></blockquote>
```

↣ div+p+bq ↢

## 4

```html
        <div>
            <p id="foo1">
                <a href=""></a>
            </p>
            <p id="foo2">
                <a href=""></a>
            </p>
            <p id="foo3">
                <a href=""></a>
            </p>
        </div>
```
↣ div>p#foo$*3>a ↢

## 5

```html
        <foo></foo>
```

↣ foo ↢

## 6

```html
        <div>foo</div>
    →
        <div class="global">foo</div>
```

↣ C-g C-u .global ↢

The cursor must be inside the opening tag (excluding the `>`):

        <div>foo</div>
        ^--^

## 7

```html
        test1
        test2
        test3

    →

        <ul>
            <li>test1</li>
            <li>test2</li>
            <li>test3</li>
        </ul>
```

↣ Vip C-g , ul>li* ↢

## 8

```html
        test1
        test2
        test3

    →

        <blockquote>
            test1
            test2
            test3
        </blockquote>
```

↣ Vip C-g, bq ↢

##
# html abbreviations

                       <!DOCTYPE html>
                       <html lang="en">
                       <head>
        html:5             <meta charset="UTF-8">
                  →        <title></title>
          OU           </head>
                       <body>
        !
                       </body>
                       </html>


                      <div>
                          <ul>
    div>ul>li    →            <li></li>
                          </ul>
                      </div>

            `>` est un  opérateur permettant de placer un  élément à l'intérieur
            d'un autre (imbrication).


                   <ul>
     test1             <li>test1</li>
     test2    →        <li>test2</li>
     test3             <li>test3</li>
                   </ul>

            vip C-g , ul>li*

                OU

            C-v {motion} S t li
            V 2j S t ul

            via vim-surround


                     <div></div>
    div+p+bq    →    <p></p>
                     <blockquote></blockquote>

            `+` est un opérateur permettant de  placer 2 éléments l'un à côté de
            l'autre, sur un même niveau.

            bq = blockquote


                                             <div></div>
                                             <div>
                                                <p>
    div+div>p>span+em^bq                →           <span></span>
                                                    <em></em>
                                                </p>
                                                <blockquote></blockquote>
                                             </div>

            ^ est un opérateur permettant de remonter d'un niveau dans l'arbre DOM.
            Ce faisant, le contexte des prochains éléments change.

            Ici, ^ nous fait sortir du tag <p> et revenir dans le <div> parent.


                                             <div></div>
                                             <div>
                                                 <p>
     div+div>p>span+em^^bq              →            <span></span>
                                                     <em></em>
                                                 </p>
                                             </div>
                                             <blockquote></blockquote>

            L'opérateur ^ peut être répété autant de fois qu'on veut pour remonter autant de niveaux
            que nécessaire.

            Ici, il est répété 2 fois pour remonter de <p> vers <div>, puis de <div> vers la racine de l'arbre.


                                             <ul>
                                                 <li></li>
                                                 <li></li>
    ul>li*5                             →        <li></li>
                                                 <li></li>
                                                 <li></li>
                                             </ul>

            L'opérateur * permet de répéter un élément.
            Ici, li*5 = li+li+li+li+li


                                             <ul>
     ul>li*2>a                                   <li><a href=""></a></li>
                                                 <li><a href=""></a></li>
                                             </ul>

            Après avoir répété un élément via l'opérateur * (ici li*2), l'opérateur > affecte chacun
            d'eux (pas juste le dernier).

            On pourrait aussi écrire (peut-être plus lisible):

                    ul>(li>a)*2


                                             <div>
                                                 <header>
                                                     <ul>
                                                         <li><a href=""></a></li>
                                                         <li><a href=""></a></li>
     div>(header>ul>li*2>a)+footer>p    →            </ul>
                                                 </header>
                                                 <footer>
                                                     <p></p>
                                                 </footer>
                                             </div>

            Les parenthèses permettent de créer un groupe contenant un sous-arbre de l'arbre DOM
            auquel on peut appliquer un opérateur.

            Ici, sans les parenthèses, il faudrait répéter l'opérateur ^ comme ceci:

                    div>header>ul>li*2>a^^footer>p

            Avec les parenthèses on peut se passer de ^. Pk?
            Car lorsqu'on ferme les parenthèses, on se retrouve dans le contexte dans lequel on se
            trouvait au moment de les ouvrir (ici à la racine du <div>).
            Ainsi, qd on écrit `+footer`, footer est considéré comme un frère du sous-arbre entre parenthèses.


                                             <div>
                                                 <dl>
                                                     <dt></dt>
                                                     <dd></dd>
                                                     <dt></dt>
                                                     <dd></dd>
     (div>dl>(dt+dd)*3)+footer>p        →            <dt></dt>
                                                     <dd></dd>
                                                 </dl>
                                             </div>
                                             <footer>
                                                 <p></p>
                                             </footer>

            On peut imbriquer des parenthèses.
            On peut appliquer l'opérateur * à un groupe.


                                             <div>
                                                 <p id="foo1"><a href=""></a></p>
    div>p#foo$*3>a                      →        <p id="foo2"><a href=""></a></p>
                                                 <p id="foo3"><a href=""></a></p>
                                             </div>


# actions

    i_C-g d
    i_C-g D

            sélectionner le tag fère précédent / courant
            "                   suivant


    i_C-g n
    i_C-g N

            déplacer le curseur au prochain / précédent point d'édition (contenu vide au sein d'un tag)


    i_C-g i

            ajouter les attributs `width` et `height` à un élément <img> avec les valeurs adaptées:
            largeur et hauteur en pixels de l'image en question. Ex:

                    <img src="/path/to/pic">    →    <img src="/path/to/pic" width="1600" height="900">


    <ul>
        <li class="list1"></li>         <ul>
        <li class="list2"></li>    →        <li class="list1"></li><li class="list2"></li><li class="list3"></li>
        <li class="list3"></li>         </ul>
    </ul>

            V2j C-g m

            Le curseur étant sur la ligne 'list1'.

            Mnémotechnique: merge


    <div class="foo">                   <div class="foo">
        <a>cursor is here</a>      →
    </div>                              </div>

            i_C-g k

            supprimer le tag contenant le curseur

            Mnémotechnique: kill


    <div class="foo">
          cursor is here           →    <div class="foo" />    →    <div class="foo"></div>
    </div>

            i_C-g j

            Raccourci répétable permettant d'alterner entre 2 versions d'une même balise html:
            balise auto-fermante et par paire (ouvrante et fermante)

            Mnémotechnique: join


    <div>                               <!-- <div>
        hello world                →        hello world
    </div>                              </div> -->

            i_C-g /

            Raccourci répétable permettant de (dé)commenter une balise html.


    http://www.google.com/         →    <a href="http://www.google.com/">Google</a>

            i_C-g a

            Mnémotechnique: anchor, tag <a>


                                        <blockquote class="quote">
                                        <a href="http://github.com/">How people build software · GitHub</a>
   http://github.com/              →    <br>
                                        <p>Pick a username Enter your email address Create a password
                                        Use at least one letter, one numeral, and...</p>
                                        <cite>http://github.com/</cite>
                                        </blockquote>

            i_C-g A

            Appelle la fonction emmet#anchorizeURL(1).

##
# Links

    https://docs.emmet.io/
    https://github.com/mattn/webapi-vim
    https://raw.githubusercontent.com/mattn/emmet-vim/master/TUTORIAL

