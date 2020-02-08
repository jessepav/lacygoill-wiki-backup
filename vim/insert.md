# Insert mode
## ?

    C-x C-a

Insérer le  contenu du  registre dot (qui  contient le texte  inséré lors  de la
dernière édition).

Par défaut c'est C-a  tout court, mais on a remap ce  dernier au déplacement sur
le  1er caractère  non whitespace  sur la  ligne, dans  le cadre  des raccourcis
readline, il a fallu trouvé un autre mapping custom.

## ?

    C-@
    C-SPC

Insérer le contenu du registre dot et revenir au mode normal.

En théorie,  seul `C-@` produit  ce résultat,  mais le terminal  perçoit `C-SPC`
comme `C-@`.

## ?

    C-x C-e/y

Passe dans un sous mode du mode insertion dans lequel on peut scroller via C-e /
C-y.

## ?

    C-r C-r a

Insère le contenu du registre a littéralement.

Ex: si @a contient 'ab^Hc' :

   - C-r a        insère    'ac'
   - C-r C-r a    insère    'ab^Hc'

À l'issue de l'insertion:

    @. = @a

car Vim remplace `C-r a` par @a.
Si on n'avait pas inséré @a littéralement:

    @. = C-r a

## ?

    C-r C-o a

Insère le contenu du registre a littéralement.

À l'issue de l'insertion:

    @. = '^R^Oa'

C-o permet d'empêcher Vim de remplacer l'appel au registre `a` par son contenu.
Ceci est utile lorsqu'on veut répéter  l'insertion avec la commande '.' mais que
@a change entre temps.

C'est ce qui se  passe qd l'insertion débute en coupant du  texte (le registre "
est changé à chaque fois) et qu'ensuite on réinsère ce même texte (via C-r ") en
lui faisant subir une certaine transformation.

Ex:

       ciw    (       c-r"    )    = entourer un mot de parenthèses
       ciw    c-r"    c-r"         = doubler un mot

                                     NOTE:

On a 3 méthodes d'insertion de registres:

   - C-r        double remplacement:
                caractères de contrôle au sein du registre +
                contenu du registre au sein du registre dot

   - C-r C-r    simple remplacement (registre dot)
   - C-r C-o    aucun remplacement

## ?

    ciw    C-r C-o "    C-r C-o "    w .    w .

Doubler 3 mots consécutifs.
Ex:

    foo bar baz    →    foofoo barbar bazbaz

`C-r" C-r" w . w .` n'aurait pas produit le résultat désiré, car @. n'aurait pas
stocké C-r" C-r" mais foofoo.

C-o permet d'empêcher Vim de remplacer l'appel  au registre " par son contenu au
sein du registre dot.
Il empêche  aussi de  remplacer d'éventuels caractères  de contrôle  présents au
sein du registre inséré, pex fooz^Hbar → foobar.

## ?

    ciw    (    C-r C-o "    )    w .    w .

            entourer de parenthèses 3 mots consécutifs
            ex: foo bar baz    →    (foo) (bar) (baz)

            ( C-r" ) w . w .    n'aurait pas produit le résultat désiré, car @. n'aurait pas stocké (C-r")
            mais (foo).

## ?

    saiwffoo
    ciw foo( C-r C-o " )

            entourer le mot sous le curseur par la fonction foo()
            les 2 solutions sont répétables par dot

## ?

    C-v      {decimal code point}
    C-v  x   {hexa code point: 2 digits}
    C-v  o   {octal code point}

            insérer un caractère à partir de son point de code:

                - décimal en 3 chiffres, il ne peut dépasser 255
                - hexa    en 2 chiffres, "                   FF     FF₁₆ = 255₁₀
                - octal   en 3 chiffres, "                   377    377₈ = 255₁₀

## ?

    C-v  u  {hexa code point: 4 digits}
    C-v  U  {hexa code point: 8 digits}

            insérer un caractère à partir de son point de code en hexa dans la table unicode

            si le point de code utilise moins de 4 chiffres (2 octets, ≤ 65535), il faut utiliser u
            s'il en utilise entre 5 et 8                    (4 octets),          il faut utiliser U

                                               NOTE:

            On n'est pas obligé de taper les leading 0, on peut se contenter de taper les chiffres
            significatifs puis C-v ou Esc pour valider.  Ex:

                    C-v u 00a0      ✔
                    C-v u a0 C-v    ✔

            À la place de C-v ou Esc, on pourrait taper n'importe quels caractères qui ne soient pas
            des chiffres hexa.
            Avec Esc on retourne en mode normal.
            Avec C-v on reste en mode insertion et le prochain caractère sera inséré littéralement.

## ?

    C-v 5j $ A foo

Insérer foo à la fin de la ligne ainsi que des 5 suivantes.

`$`  en mode  visuel par  bloc permet  de sélectionner  des lignes  de longueurs
différentes, et donc d'avoir un bloc dont le bord droit est irrégulier.

## ?

    C-v 5j C foo Esc `[ P

            insérer foo à la fin de la ligne et des 5 suivantes, les 6 foo étant alignés

            La magie opère lorsqu'on tape C. On coupe alors un bloc et non des lignes.
            Dans le registre par défaut si les lignes n'ont pas la même longueur, Vim ajoute des
            espaces à la fin des + courtes pour toutes les égaliser et bien obtenir un bloc.

## ?

    vip C-v I0 Esc gv gC-a

            Numéroter les lignes du paragraphes courant.

            Si les lignes sont précédées d'un symbole (*, -, …), on peut remplacer I0 <Esc> par r0.
            Alternative via filtrage et le pgm shell nl:

                    !ip nl -ba -w1 -s' '

            -ba      numéroter toutes les lignes du texte (body all)
            -w1      écrire le n° sur la 1e colonne
            -s' '    séparer le n° du texte par un espace

##
# Command-line mode
## ?

    :dig[raphs]    :h digraph-table

            afficher la liste des digraphes actuellement définis
            :h digraph-table est + lisible.

## ?

    :dig a: 228 e: 235

            définir les digraphes a: et e: qui produisent les caractères dont le point de code
            décimal est 228 et 235 (ä et ë; vérifiable via ga)

                                               NOTE:

            Les digraphes sont pratiques pour insérer des caractères compliqués à taper voire absent
            du clavier. Ex:

                    ss       ß
                    =e       €
                    =>       ⇒
                    i'       í
                    13       ⅓    de la même façon, on peut écrire n'importe quelle fraction irréductible
                                  dont le dénominateur est ≤ 6     (autre ex:    ^K56    →    ⅚)

            Dans les digraphes installés par défaut, le 2e caractère respecte certaines conventions
            décrites dans :h digraphs-default.  Pex:

                    '     accent aigu
                    !     accent grave
                    >     accent circonflexe

## ?

    :5insert    :??append

            insérer des lignes de texte au-dessus de la 5e ligne
            insérer des lignes de texte en-dessous de la précédente ligne contenant le dernier pattern
            recherché/substitué

                                               NOTE:

            Qd on utilise ces commandes, on passe en mode Ex.
            On écrit les lignes qu'on souhaite ajouter au buffer, en validant chacune via CR.
            Pour revenir au mode normal et voir le résultat de l'insertion, entrer une ligne contenant
            un seul point. Ou appuyer sur C-c.

## ?

    :g/pattern/norm! C-v C-a    :g/pattern/exe "norm! \<C-A>"

            incrémenter le 1er nb sur chaque ligne contenant pattern
            rappel: le curseur n'a pas besoin d'être sur le nb pour qu'il soit incrémenté

            Dans la 1e solution, C-v C-a insère le caractère de contrôle C-a littéralement sans l'interpréter.

## ?

    :1,64g/^/ 42s:\zefoo:\:

            Insérer 64 backslashs devant le pattern foo de la ligne 42.
            Illustre qu'on peut utiliser la rangée de :g pour répéter une opération un nb arbitraire de fois.

            Avantage:     probablement POSIX-compliant
            contrairement à    :42s:\zefoo:\=repeat('\', 64):

            Inconvénient: nécessite que le buffer ait un nb de lignes suffisant.

## ?

    g:^\s*$:+s:^\S:<p>&
    %s:^\s*\n\zs\ze\S:<p>

            ajouter le tag html <p> au début de chaque paragraphe

            Qd :g trouve une ligne vide, elle appelle :s qui descend d'une ligne (+), et remplace le 1er
            caractère non whitespace de cette-dernière par <p> et le caractère en question.
            La commande fonctionne même si le buffer contient plusieurs lignes vides consécutives.
            En effet, :s n'agit que si elle trouve un caractère non whitespace.

## ?

    g:^\s*$:-s:\S$:&</p>
    %s:\S\zs\ze\n\s*$:</p>

            ajouter le tag html </p> à la fin de chaque paragraphe

## ?

    %s:\v\_$\_s{2,}\_^:</p>&<p>    %s:\v\n(\s*\n)+:</p>&<p>

            ajouter les tags html <p> et </p> au début et à la fin de chaque paragraphe

            Les caractères séparant la fin d'un paragraphe du début du suivant peuvent être décrit comme ceci:

                    \v\_$\_s{2,}\_^

                          \_s{2,}    une séquence de newlines ou whitespace contenant au moins 2 caractères
                                     2 \n consécutifs sont le minimum requis pour séparer 2 paragraphes

                      \_$            le 1er doit être un newline

                                \_^  le dernier doit être un newline

            On est obligé d'utiliser le multi {2,} et non +.  Avec + le pattern matcherait n'importe quel newline.

## ?

    :g/^CHAPTER$/ .,$s//&I/
    :g/^CHAPTER$/ s/IIIII/V/g | s/VV/X/g

            après chaque ligne contenant l'unique mot CHAPTER, ajouter un n° en chiffres romain en incrémentant
            (I pour le 1er, II pour le 2e etc.)

                                               NOTE:

            Si on utilisait la rangée % pour la commande de substitution de la 1e commande globale,
            on ajouterait au final le même nb de I pour tous les chapitres (qui serait égal au nb de chapitres).
            En utilisant la rangée .,$ on ajoute un nb de I qui augmente d'un après chaque nouveau chapitre.

            Si on utilisait la substitution:    s/$/I/g
            …, on ajouterait des I à la fin de lignes qui ne contiennent pas CHAPTER.

## ?

    :%norm Ifoo

            Insérer le mot foo au début de chaque ligne du buffer.

## ?

    :*norm .    V{motion}.

            répéter la dernière édition sur toutes les lignes de la sélection visuelle
            La 2e commande n'est possible que grâce au mapping custom:    xnoremap . :norm .<cr>

## ?

    :startinsert[!]

            passer en mode insertion (depuis le mode Ex)
                :startinsert  → norm! i
                :startinsert! → norm! A

## ?

    :s/\u*/-/g

            réalise la transformation suivante:

                    abcdefghijklm    →    -a-b-c-d-e-f-g-h-i-j-k-l-m

            Le moteur de regex se positionne sur `a`, il cherche à matcher un maximum de `\u` mais
            n'y arrive pas puisque `a` n'est pas une majuscule.
            Cependant, le quantificateur * lui permet malgré tout de matcher 0 majuscules.
            Il y a bien 0 majuscules depuis `a`, et donc `:s` remplace ce texte vide par un tiret.
            Enfin, le moteur de regex avance en `b` et recommence.

                                               NOTE:

            On pourrait remplacer `\u` par n'importe quel atome absent du texte.
            En utilisant, `\n` à la place de `\u`, on ajouterait un tiret de plus à la fin:

                    -a-b-c-d-e-f-g-h-i-j-k-l-m-

##
# Pitfalls
## I want to append some text at the end of multiple lines.  What's one pitfall of `v_b_A`?

Be sure to reset `'wrap'`.
Otherwise, the text may not always be added at the end of the lines.

MWE:

    $ vim +'put =repeat(\"a\", winwidth(0)-5).\"-aaa\nb\"' +'setl wrap' +'exe "norm! 1GV+\<c-v>0o$AXXX"'

Alternatively, use a global command:

    :*g/^/norm! Amy text

