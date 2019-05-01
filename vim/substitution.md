Replace one pattern out of two with `foo`, and the other with `bar`:

    let a = ['bar', 'foo']
    %s/pat/\=reverse(a)[0]/

Replace one pattern out  of two with `foo`, another with  `bar`, and yet another
with `baz`:

    let a = ['foo', 'bar', 'baz']
    %s/pat/\=add(a, remove(a, 0))[-1]/

These commands work because `reverse()`, `add()` and `remove()` operate in-place.

---

Always  escape a  literal  opening  square bracket  in  a substitution  command,
otherwise the whole command will become the pattern.

E.g.:

    :%s/a[b/rep/

This command doesn't replace `a[b` with `rep`, but `a[b/rep/` with nothing.

---

            Utilisé  dans un  pattern,  chaîne de  remplacement,  ou une  simple
            recherche,  est développé  en la  chaîne de  remplacement qui  a été
            utilisée dans la dernière commande de substitution.


    & a plusieurs significations suivant le champ où il se trouve:

                    - dans un pattern \& relie 2 concats
                    - dans une chaîne de remplacement, & est développé en le pattern matché
                    - dans les flags, & est développé en les flags utilisés lors de la dernière substitution
                      (it must be first flag)


    g&
    :%s//~/&

            Répète la dernière substitution sur tout le buffer.

            Utilise le registre recherche comme pattern.
            Préserve les flags, et utilise % comme rangée.


    :~
    :s//~/

            Répète la dernière substitution sur la ligne courante.

            Utilise le registre recherche comme pattern.
            Les flags et la rangée sont perdus, mais on peut en fournir de nouveaux:

                    :%~g


    &
    :&
    :s

            Répète la dernière substitution sur la ligne courante.

            Utilise le pattern utilisé par la dernière commande :s/:g.
            Les flags et la rangée sont perdus, mais on peut en fournir de nouveaux à :s et :&:

                     ┌─ toutes les lignes
                     │ ┌─ toutes les occurrences sur une même ligne
                     │ │
                    :%&g
                    :&&
                      │
                      └─ mêmes flags que lors de la dernière substitution


                                               NOTE:

            `:&&` est très utile pour exécuter une substitution sur une rangée de lignes non contiguës:

                    :1,10s/pat/rep/g | 20,30&&
                  ⇔ :{1,10 + 20,30} s/pat/rep/g


                                               NOTE:

            Parmi les différentes commandes permettant de répéter une substitution, :& et :s sont
            les  seules  à réutiliser  le  pattern  de la  dernière  commande  :s/:g. Les  autres
            utilisent le registre recherche.
            Pour corriger ça, on peut leur ajouter le flag r:

                    :&r
                    :sr

                                               NOTE:

            Attention: si juste avant on a tapé & les flags sont perdus.
            Il ne sert plus à rien de taper :&& juste après.

                                               NOTE:

            Même sans le flag g, on peut malgré tout remplacer toutes les occurrences sur une ligne
            en répétant &.
            Il faut voir & comme une petite substitution permettant un remplacement plus fin:

                    :s//~/     remplace la prochaine occurrence
                    :s//~/g    remplace toutes les occurrences
                    &&&        remplace les 3 prochaines occurrences


                                               NOTE:

            Il existe d'autres abréviations de commandes de substitutions (:h sgn).


    c_C-s

            rechercher le pattern sans tenir compte des accents
            Mapping custom à taper en mode commande (à la fin d'une recherche).

    v_C-s

            rechercher un pattern à l'intérieur de la sélection visuelle via :*g/\%V/# (custom)

    i_C-x C-s

            corriger la dernière faute d'orthographe précédant le curseur (custom)


    :s/

            supprimer sur la ligne courante la prochaine occurrence du pattern matchant le registre /

            Qd on omet la chaîne de remplacement, :s supprime le pattern au lieu de le remplacer par qch.
            Qd on omet le pattern, :s utilise le registre /.

            On peut tout omettre, pattern, chaîne de remplacement, flags.


    :%s/\\u\x\+/\=eval('"'.submatch(0).'"')/g
    :%s/\v\\u(\x+)/\=nr2char('0x'.submatch(1), 1)/g

            Traduire tous les caractères spéciaux (\u ou \U) suivis de points de code en leurs équivalents
            littéraux. Ex:    \u20ac    →    €

            submatch(0) est une chaîne, et la concaténation a pour effet d'inclure des double quotes
            au sein de cette dernière.
            Puis on appelle eval() qui les enlève qd elle évalue le contenu de la double chaîne '" … "':

                    '…'    →    '" … "'    →    "…"
                     concaténation       eval()

            Les 2 opérations s'annulent, à ceci près que la sortie de eval() n'est plus une chaîne
            littérale, mais non littérale.
            Ses caractères spéciaux sont donc automatiquement traduits (\u20ac → €).


    :%s/\v\n(\s+)/\1/

            fusionne des blocs de code en une seule ligne. Ex:

                    foo
                      bar    →    foo  bar  baz
                      baz

            Arrivé au 1er newline, Vim remplace `\n  ` en `  `, et ce faisant fusionne les 2 premières
            lignes `foo\n  bar` en `foo  bar`.
            Puis, tjrs depuis la ligne d'adresse 1, Vim avance et rencontre à nouveau le pattern `\n  `
            qu'il réduit en `  `.
            Ce faisant, il fusionne `foo  bar\n  baz` en `foo  bar  baz`.


    :%s/\v\n(\s+)/^A\1/
    :sort
    :%s/^A/\r/g

            Trie des blocs de lignes en fonction de leur 1e ligne.
            Un bloc se termine lorsqu'on rencontre une ligne sans leading whitespace (niveau d'indentation 0).
            Ex:

                    case foo         case bar
                        cmd1             cmd3
                        cmd2             cmd4
                    case bar    →    case baz
                        cmd3             cmd5
                        cmd4             cmd6
                    case baz         case foo
                        cmd5             cmd1
                        cmd6             cmd2

            Le trie n'altère pas l'ordre des lignes à l'intérieur d'un bloc, uniquement les positions
            relatives des blocs les uns par rapport aux autres.

            L'astuce consiste à réaliser que pour pouvoir trier des blocs de ligne, il faut les fusionner.
            Concrètement, ici, on:

                - fusionne temporairement les blocs sur une seule ligne, en séparant les anciennes
                  lignes par un caractère dont sait qu'il est absent de ces dernières

                  Un caractère de contrôle tq ^A fera l'affaire généralement.

                - trie les lignes restantes

                  Les autres ne gênent plus car elles ont été fusionnées.

                - casse les lignes triées pour retrouver les blocs d'origine

                  C'est là que ^A est utile, il indique à :s où elle doit réinsérer des newlines.

                                               NOTE:

            On pourrait limiter le tri à une sélection visuelle en remplaçant la
            rangée % par *.
            Pas besoin  de gv pour  resélectionner les blocs fusionnés  avant de
            les casser, la rangée * serait tjrs valide, car les marques '< et '>
            sont tjrs posées au même endroit.


    :s/\v(%#.*)@<= /_/g

            remplacer tous les espaces après la position courante en underscores


    :%s/foo\|bar/\=submatch(0) ==# 'foo' ? 'bar' : 'foo'

            remplacer foo par bar, et bar par foo


    :/foo/s///
    :/foo/s/

            supprimer la prochaine occurrence de foo


    :s/.*\zsfoo\ze.*foo/bar/

            remplacer l'avant-dernière occurrence de foo par bar
            Fonctionne car le 1er multi * est greedy.

            Seul le  1er multi a  besoin d'être greedy:  le 1er .*foo  pousse le
            moteur de  regex vers le  dernier foo,  puis en ajoutant  au pattern
            .*foo ou  .\{-}foo, le moteur est  obligé de reculer pour  que .*foo
            corresponde désormais  à l'avant-dernier  foo et  ainsi faire  de la
            place au 2e .*foo / .\{-}foo.

            La  raison pour  laquelle  le 2e  multi peut  être  non greedy  sans
            changer  le match  de la  regex, est  que les  sous-expressions sont
            identiques, et que  la greediness du 1er multi a  priorité sur celle
            du 2nd (donc le moteur recule un minimum).

            En revanche:    .*foo.*bar    n'est pas équivalent    à .*foo.\{-}bar
                                          car les sous-expressions ne sont pas identiques, le moteur n'est donc pas
                                          obligé de reculer un minimum


    :s/\v.{-}foo.{-}\zsfoo/bar/

            remplacer la 2e occurrence de foo par bar
            Fonctionne car le multi {-} est non-greedy (les 2 multi doivent être non-greedy).

            RÉSUMÉ:  foo                    1e occurrence
                     .\{-}foo.\{-}\zsfoo    2e "
                     .*\zsfoo\ze.*foo       avant-dernière
                     .*foo                  dernière


    %s:\v^(.*)(\n\1)+:\1:

            remplacer les séquences de lignes consécutives identiques par une seule occurrence

            Il ne faut pas placer le newline dans le 1er capturing group.
            En apparence ça  semblerait marcher, mais ça échouerait  dans le cas
            un doublon se trouverait sur la dernière ligne du buffer.
            En effet, cette dernière n'est pas  suivie d'un newline et ne serait
            donc pas matchée.


    :%s/\w\+/\=add(words, submatch(0))/gn

            crée une liste words contenant tous les mots du buffer

            Montre comment le flag n de  :s et l'utilisation d'une expression \=
            à  la place  de la  chaîne de  remplacement, permet  d'effectuer une
            opération arbitraire sur tous les matchs d'un pattern.


    :%s/\w\+/\=len(add(words, submatch(0))) ? submatch(0) : submatch(0)/g

            crée une liste words contenant tous les mots du buffer

            Cette syntaxe devrait fonctionner peu importe la version de Vim, car
            on n'utilise pas le flag n.

            :s remplace tous les mots par  eux-mêmes, donc le buffer est modifié
            mais le contenu reste identique.

            L'expression:

                    len(…) ? submatch(0) : submatch(0)

            … évalue la fonction add() qui ajoute un item à words.

            Pk l'appel à len() ?

                    add(words, submatch(0))

            … ne retourne pas un nb mais la liste words.

            On ne peut pas tester directement une liste comme ceci:     if list    ✘
            En revanche on peut tester un nb comme ceci:                if n       ✔
            len(…) permet de convertir la liste words en un nb (sa taille) qui peut être directement testé.


    :%s/".\{-1,}"/"foo"/g

            remplace tous les textes encadrés avec des guillemets par "foo"

            Il  ne  faut surtout  pas  utiliser  \zs  et  \ze pour  exclure  les
            guillemets du pattern comme ceci:

                :%s/"\zs.\{-1,}\ze"/foo/g

            Pk? Car la ligne suivante: "hello" and "world" serait remplacée par:

                    "foo"foo"foo"

            au lieu de:

                    "foo" and "foo"

            Plus  généralement: qd  on  veut  décrire un  texte  encadré par  un
            symbole ouvrant puis un autre  fermant, il faut inclure ces symboles
            dans le match.
            Si on les exclut, la regex va également matcher du texte encadré par
            un 1er symbole fermant puis un 2e ouvrant.
            Généralement ce n'est pas ce qu'on souhaite.


    :%s/\cfoo/\=submatch(0)[0] ==# 'F' ? 'BAR' : 'bar' /g

            remplacer toutes les occurrences de FOO par BAR, et celles de foo par bar


    :s:\v(\w+):\U\1
    :s:\v(\w+):\L\1

            fait passer le 1er mot de la  ligne en majuscule / minuscule :h s/\U
            + généralement, dans une chaîne  de remplacement, \U et \L modifient
            la casse de tout ce qui suit


    :s:\v(\w+):\u\1
    :s:\v(\w+):\l\1

            fait passer le 1er  caractère du 1er mot de la  ligne en majuscule /
            minuscule + généralement, dans une  chaîne de remplacement, \u et \l
            modifient la casse du caractère suivant


    :s:\v(\w+) (\w+) (\w+):\U\1\E \2 \U\3

            fait  passer  le  1er et  3e  mot  de  la  ligne en  majuscule  (les
            mots  étant simplement  séparés par  un espace)  dans une  chaîne de
            remplacement, \E met  un terme à une modification  de casse apportée
            par \U ou \L

                                               NOTE:

            Pas besoin de \E qd on passe directement de \U à \L ou l'inverse.
            \E n'est utile  que lorsqu'on souhaite préserver  la casse d'origine
            d'une partie du pattern.


    :/\v(foo)/s//\U\1

            Fait passer en majuscule la prochaine en occurrence de foo.

            Illustre qu'on peut  capturer du texte dans un  pattern présent dans
            l'adresse  d'une rangée  et le  faire  passer jusqu'à  la chaîne  de
            remplacement d'une commande de substitution.


    :%s:\d\+:\=str2nr(submatch(0))+5:g

            Ajouter 5 à tous les nb du buffer.

            Cette commande illustre le fait  que lorsqu'on évalue une expression
            dans la chaîne de remplacement  de la commande de substitution (\=),
            pour se  référer à tout  ou partie du match,  il faut passer  par la
            fonction submatch() (équivalent de \0, \1 … \9)

            Attention: si le nb auquel se  réfère submatch() débute par un 0, il
            est converti en un nb octal.
            Ceci peut poser  problème si on réalise un calcul  dans la chaîne de
            remplacement, comme pex incrémenter un  nb capturé dans le pattern (
            submatch(1) + 1 ).

            Pour résoudre ce pb, il faut envelopper submatch() dans str2nr() qui
            peut  convertir une  chaîne contenant  des  chiffres en  un nb  dans
            n'importe quelle base.
            La base peut être fournie via un 2e argument optionnel.
            Sans ce 2e argument, la base 10 est choisie par défaut.


    :exe '*s/' . join(keys(mydict), '\|') . '/\=mydict[submatch(0)]/g'

            Au sein de la sélection  visuelle, substituer toutes les occurrences
            des clés du dico `mydic` par leurs valeurs.
            Exemple de dico:

                    let mydict = {'foo': 'bar', 'bar': 'foo'}

            En  utilisant ce  dico, on  remplacerait toutes  les occurrences  de
            'foo' par 'bar' et toutes celles de 'bar' par 'foo'.
            Technique  intéressante dans  une  commande,  fonction, script  pour
            regrouper un ensemble de substitutions.


    :let c=0 | 10,20g//let c += 1 | s/^/\=c . "\t"

            Numéroter les lignes 10 à 20 à partir de 1.

            Cette commande  illustre le fait  que \= permet d'évaluer  aussi des
            variables  (ici le  compteur  c),  en plus  de  pouvoir évaluer  des
            fonctions.


    :*s/^*/\=line('.') - line("'<") + 1 . '.'

            Remplace une  liste dont les  lignes commencent par  des astérisques
            par une liste numérotée à condition d'avoir sélectionné visuellement
            la liste.


    :let [c,d]=[0,0] | g/^* /let [c,d]=[line('.')==d+1? c+1: 1, line('.')] | s//\=c.'. '

            Transforme  toutes  les  listes  dont  les  items  débutent  par  un
            astérisque en listes numérotées.

            La variable c sert d'incrément.
            La variable d sert  à déterminer si on est tjrs  dans la même liste,
            si c'est  le cas (line('.')==d+1)  on incrémente c, autrement  on la
            réinitialise à 1


    :%s/, /\r/g

            Transforme foo, bar, baz en foo
                                        bar
                                        baz


    :%s/^/\=line('.') . "\t"

            Numéroter  chaque ligne  en  remplaçant  son début  (^)  par son  n°
            (line('.')) et un caractère tab ("\t").


    :%s:foo\zs\_.\{-}\zebar:\=insert(readfile('note.txt'), ''):g

            Remplacer le texte encadré par foo  et bar par le contenu du fichier
            note.txt.

                                               NOTE:

            - fonctionne même si foo et bar sont sur des lignes différentes
              (grâce à \_. qui inclue un newline)

            - cette commande illustre le fait que l'expression de substitution
              peut aussi être une liste en effet, readfile() retourne une liste
              :h sub-replace-expression explique que lorsque cela se produit,
              les items de la liste sont automatiquement fusionnés et séparés
              des newlines

            - on appelle insert() pour ajouter une chaîne vide à la liste
              readfile(…) de sorte que lorsque la fusion ait lieue, un newline
              soit ajouté au tout début et que le texte de remplacement débute
              sur une nouvelle ligne. Pas obligé mais peut être utile.


    foo          foo1          foo1
    bar    ⇒     foo2    ⇒     foo2
    baz          foo3          foo3
                               bar1
                 bar1          bar2
                 bar2          bar3
                 bar3          baz1
                               baz2
                 baz1          baz3
                 baz2
                 baz3

            :%s/.*/\=map(range(1,3), 'submatch(0) . v:val')                    1e transfo

            :%s/.*/\=join(map(range(1,3), 'submatch(0) . v:val'), "\n")        2e transfo

                                               NOTE:

            La 1e substitution insère sur une ligne différente chaque item de la
            liste ( map(range(1,3), …) ), en insérant automatiquement un newline
            à la fin.
            Raison pour  laquelle on a  une ligne vide  toutes les 4  lignes: il
            s'agit du newline ajouté au dernier item de la liste.


    :g/^/s//> / | pu_ | j

            ajouter '> ' au début d'une ligne sur 2

            Après la 1e substitution, :g colle  une ligne vide sous la 1e ligne,
            et le curseur se déplace sur cette dernière.
            Puis, :g  fusionne cette ligne  vide avec  la 3e ligne  (ancienne 2e
            ligne).
            Le résultat est une ligne identique  à l'ancienne 2e ligne, mais qui
            n'a pas été marquée par :g lors de sa 1e passe.
            Ainsi, elle ne sera pas affectée par la substitution.

            Le processus se répète, et ainsi  seule une ligne sur 2 est affectée
            par une substitution.

            Plus généralement, | pu_  | j répété n fois permet  de demander à la
            commande globale de ne traiter qu'une ligne sur n+1.


    ┌───────────────────────────────────────┬────────────────────────────────┐
    │ 123456789.000    →    123,456,789.000 │ s/\v(\d)((\d{3})+\d@!)@=/\1,/g │
    │ 123456789        →    123,456,789     │                                │
    └───────────────────────────────────────┴────────────────────────────────┘

            Décomposition du pattern:

                    \v(\d)((\d{3})+\d@!)@=
                      │   ││         │
                      │   ││         └ suivi de n'importe quoi qui n'est pas un chiffre
                      │   ││              (point, lettre, fin de ligne)
                      │   ││
                      │   │└ ce qch est un multiple de 3 chiffres:    (\d{3})+
                      │   │
                      │   └ affirme que qch doit se trouver après:    ()@=
                      │
                      └ capture un chiffre

            Le pattern peut être trouvé en se posant la question: "qu'est-ce qui
            caractérise l'endroit où il faut insérer une virgule ?"

            Réponse:
            Après une virgule il doit y avoir exactement `3n` chiffres.

            Au moins `3n` qch peut s'écrire:

                    ((qch){3})+

            Peut matcher `3n`, `3n + 1`, `3n + 2` qch.

            Exactement `3n` qch peut s'écrire:

                    ((qch){3})+(qch)@!


    Input:

    123 1234 1345 123456 12344567 12345678
    123 1234 1345 123456 12344567 12345678 123 1234 1345 123456 12344567 12345678

    Output:

    1231234 1345123456 1234456712345678
    1231234 1345123456 1234456712345678 1231234 1345123456 1234456712345678

            %s/\v (\S* |$)/\1/g

            Explanation:

            The goal is to remove every odd numbered space.
            The pattern '  \S* ' will match  an odd numbered space  and the next
            even numbered space.

            We capture everything,  except what we want to remove  (i.e. the odd
            numbered space).
            So that, by replacing the whole pattern with the capturing group, we
            can remove the odd numbered space.

            We need to add the `$` anchor  to match the last odd numbered space,
            in case it's at  the end of the line and not followed  by a word and
            an even numbered space.

            This technique works because once  the regex engine has MATCHed some
            text, it can't go back, only move forward.
            We force  it to consume the  even numbered space, so  that it's left
            unchanged.

            This wouldn't work:

                    :s/\S*\zs \ze\S* //g

            Because the  match would NOT  consume the even numbered  space after
            removing an odd numbered space.
            As a result, all spaces would be removed.

            Remember:
            When you want some text to be left unchanged, make it a part of the match.
            Being part of a lookaround is not enough.

            Alternative:

            *g/^/let a = [' ', ''] | s/\d\zs\s\+/\=reverse(a)[0]/g

            For  every visually  selected  line,  reset an  array,  and use  its
            contents to replace the pattern.
            Reverse its contents before every substitution.
            Since one of its elements is an empty string, in effect, you replace
            the pattern once every two matches.

            The trick can be generalized to any sequence of replacements.
            Search `reverse(` in our notes about VimL.

