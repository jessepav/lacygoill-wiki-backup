# getting the contents of a register
## How to get the contents of a register as a list of lines?

Pass the third optional boolean argument `1` to `getreg()`:

    :echo getreg('q', 1, 1)
                         ^
Note that the second argument is ignored here, so you could write any expression
in its place.

## How to get the last expression written in the expression register?

Pass the second optional boolean argument `1` to `getreg()`:

    getreg('=', 1)
                ^

Without  this  argument,  or  if  it was  false,  `getreg()`  would  return  the
evaluation of the last expression instead of the expression itself.

##
# setting the contents of a register
## ?

`setreg()`

    setreg('a', string)

            écrit la chaîne string dans le registre @a

    setreg(v:register, @*)

            écrit le contenu du registre sélection dans le registre en cours d'utilisation par un opérateur
            la fonction setreg() retourne 0 en cas de succès, un autre nb autrement

    setreg('*', @%, 'av')

            ajoute (flag 'a' dans le 3e argument) le nom du buffer courant au contenu du registre sélection
            et attribue le type characterwise à ce dernier (flag 'v' dans le 3e argument)

    setreg('a', "1\n2\n3", 'b5')

            stocke la chaîne "1\n2\n3" dans le registre @a et lui attribue le type par bloc avec une largeur 5
            si on ne précise pas la largeur du bloc, elle est égale automatiquement au nb de caractères
            sur la plus longue des lignes

    setreg('a', ['foo', 'bar', 'baz'])

            stocke dans le registre 'a' les chaînes 'foo', 'bar' et 'baz' sur 3 lignes différentes
            le type du registre 'a' est automatiquement 'V'

    setreg('+', '', 'aV')

            fait passer le type du registre @+ à linewise

            Le flag 'a' indique qu'il faut ajouter la valeur à l'ancien contenu du registre @+
            (au lieu de l'écraser), et comme la valeur est '' le contenu de @+ n'est pas modifié
            (mais son type oui).

            Ceci est une astuce illustrant comment changer le type d'un registre, car il n'existe
            pas de fonction setregtype().

    :call setreg('d', @a..@b..@c,    getregtype('d'))
    :call setreg('d', @d..MyFunc(), getregtype('d'))

            Stocker dans le registre `d`, la concaténation:

                    - des registres a, b et c
                    - du registre d et de la sortie de `MyFunc()`

                                               NOTE:

                    :let @d  = @a.@b.@c    ✘
                    :let @d .= MyFunc()    ✘

            Les opérateurs `=` et `.=` ne sont pas fiables car ils ne préservent pas le type du registre.


    :let save_reg = [getreg('a'), getregtype('a')]
    :call setreg('a', save_reg[0], save_reg[1])

            sauvegarde puis restaure le registre a

            Qd on manipule des registres, il  faut se méfier des opérateurs = et
            .= car  il est possible  qu'ils ne préservent  pas tjrs le  type des
            registres.
            L'instruction suivante n'est donc pas fiable:

                let save_reg = @a    ✘

##
# Noms

    ""         registre unnamed

               Ce registre a 2 propriétés:

                   - il pointe vers le dernier registre modifié
                   - il est utilisé par défaut par les commandes qui collent du texte:    p = ""p

               La 1e propriété est non modifiable, la 2e oui (via 'clipboard').

    "0         registre de la plus récente commande yank
               après une nouvelle copie, le contenu de ce registre est perdu
               yy = "0yy    yiw = "0yiw

    "1         registre de la plus récente longue suppression / changement
               pour voir la signification de “longue“ lire :h registers
               dd = "1dd

               "2 = 2e plus récente longue suppression / changement, ..., "9 = 9e plus récente...

    ".         registre de la plus récente édition
               Vim y stocke les frappes au clavier tapées la dernière fois qu'on était en mode insertion

    "-         registre de la plus récente courte suppression (lettre, mot)


    "/         registre recherche

               Contient le dernier pattern recherché via /, ?, :s ou :g/:v

                                               NOTE:

               Le contenu de ce registre détermine:

                        - les mots entre lesquels on navigue via n/N
                        - le texte mis en surbrillance qd 'hlsearch' est activée
                        - le texte sur lequel on opère via gn (dgn, cgn, ...)

               Il  faut  distinguer  ce  registre   de  la  dernière  entrée  de
               l'historique consultable via q/.
               Les 2 ne sont pas tjrs identiques.
               Par  exemple, si  on vide  son  contenu (let  @/=''), le  dernier
               pattern recherché reste dans l'historique q/.
               À ce moment-là, les 2 diffèrent.

                                               NOTE:

               Le  registre   recherche  et   l'historique  de   recherche  sont
               automatiquement repeuplés dans certaines circonstances:

                     1. Si on vide le registre recherche, il est automatiquement repeuplé par
                        le pattern de la dernière commande :s, :g lors d'une recherche via:

                                n N

                     2. Si en plus, on supprime de l'historique, le pattern de la dernière commande
                        :s, :g :

                                :call histdel('/', @/),

                        ... ce dernier est automatiquement réintégré à l'historique lors de la prochaine
                        recherche via:

                                n N

                        Il  est   probable  que   le  pattern  de   la  dernière
                        commande :s,  :g, soit  mémorisé qq  part (en  dehors de
                        l'historique), de sorte que  lorsqu'on demande à répéter
                        la recherche, Vim peut s'appuyer sur qch.
                        Ça expliquerait  comment Vim fait pour  s'en souvenir qd
                        on appuie sur n, N.

                        Il est  également probable  que Vim restaure  d'abord le
                        registre recherche, puis,  par conséquence, réintègre la
                        recherche au sein de l'historique.

                     3. À l'issue de l'exécution d'une fonction ou d'une
                        autocmd, les registres . et / sont restaurés, cf :h
                        function-search-undo

                        Exception:

                                nno cd :call MyFunc()<cr>

                                fu MyFunc()                      fu MyFunc()
                                    s/foo/bar/                       let @/='foo'
                                endfu                            endfu

                        Qd on appuiera  sur `cd` en utilisant la  1er version de
                        `MyFunc()` le registre @/ sera bien restauré.
                        Mais pas avec la 2e version.
                        Conclusion, si on manipule  @/ directement, il n'est pas
                        restauré.


                                     NOTE:

               Qd on  insère ce registre,  les caractères ayant un  sens spécial
               dans un pattern (^$*~/ ...) sont automatiquement échappés.


    "=         registre expression
               permet d'insérer, en mode insertion ou ligne de commande, le résultat d'une expression vimscript,
               d'une commande shell, ou d'un script externe (python, ...)

               Le registre expression diffère des autres registres pour 2 raisons:

               1. il évalue ce qu'on lui passe avant de l'exécuter (les autres registres n'évaluent rien)
               2. on définit son contenu et on l'exécute/insère son évaluation directement ensuite

                  Les  autres  registres  distinguent  clairement  la  phase  de
                  définition (let @a='dd') de la phase d'exécution/insertion (@a
                  / C-r a).
                  En effet, si  on définit le contenu du  registre expression au
                  préalable (let @=  = 'dd'), au moment de  l'exécuter (@=), Vim
                  nous demande de le redéfinir de toute façon.

               Pour  évaluer une  expression  écrite sur  la  ligne courante  du
               buffer, on peut taper:

                   - pour la lire:       _y$    →    :echo eval(@")
                   - pour l'exécuter:    _y$    →    @=@"
                   - pour l'insérer:                 C-r =@"

                   yy copierait le newline qui soulèverait une erreur, raison pour laquelle on utilise _y$.


    ":         registre commande; contient la dernière commande tapée

    "_         registre trou noir ( sorte de /dev/null )
               c'est un trou noir pour 2 raisons :
               il n'est pas possible de lire / écrire son contenu; le registre unnamed ne pointe jamais sur lui

    "%         registre du nom du buffer courant

    "#         registre du nom du buffer alternatif pour la fenêtre courante
               On peut écrire dans ce registre et ainsi modifier le buffer alternatif.
               :b# et <C-^> voient leur comportement modifier.

    v:register

               variable interne stockant le nom du registre en cours d'utilisation par un opérateur
               Elle vaut:

                   - " si aucun registre n'est en cours d'utilisation
                   - + si &clipboard commence par unnamedplus

# Utilisation

Un nom de registre / une macro peut être précédée d'un :

    @      qd on veut exécuter son contenu en mode normal / Ex
           OU qd on veut y écrire en mode Ex (let @a = ...)

    "      qd on veut y accéder en lecture (coller) / écriture (copier) depuis le mode normal
     C-r   qd on veut y accéder en lecture (coller) depuis le mode insertion / Ex

    rien   qd on le passe en argument à une des commandes Ex suivantes: :change, :delete, :put, :yank

---

Une macro est enregistrée dans un registre normal.
Ceci est très pratique pour éditer une longue macro qu'on doit modifier car elle n'a pas tout à fait
le comportement attendu.  Pour ce faire, il suffit de :

   1. coller le contenu de la macro dans un buffer (ex: "ap),
   2. l'éditer en insérant littéralement les caractères de contrôle si besoin
   3. la recopier dans le registre ("aY),
   4. et enfin la rejouer.

---

Qd on enregistre une macro, on peut avoir besoin de déplacer un mot ou une ligne
à un autre endroit.
Il peut alors être utile de les supprimer dans des registres aux noms évocateurs
comme n pour un nombre, ou x pour un texte:

    "nde

            supprimer dans le registre n depuis le curseur jusqu'à la fin du mot
            le curseur étant au début d'un nombre

    "xdd

            supprimer la ligne dans le registre x

Ces registres n et x peuvent désormais servir de mémoire temporaire.
On peut utiliser n'importe quel registre sauf  celui dans lequel on est en train
d'enregistrer sa macro.

---

On peut  avoir besoin  d'opérer une  transformation sur 2  lignes au  lieu d'une
seule.  Dans ce cas, on peut:

   - les sélectionner visuellement, juste avant l'enregistrement, de sorte
     qu'elles correspondent aux frontières de la sélection

   - dupliquer les marques visuelles, juste après le début de l'enregistrement,
     pour ne pas les perdre si on doit sélectionner qch au cours de
     l'enregistrement:    mt o mb    (t = top, b = bottom)

Désormais on pourra s'y rendre via les mouvements 't et 'b.
Il faudra  s'assurer de sélectionner les  2 lignes désirées avant  de rejouer la
macro.

À retenir:
Pendant l'enregistrement d'une macro, ne pas hésiter à utiliser des registres ou
des marques pour déplacer de l'information  (texte), ou en préserver (adresse de
ligne).

---

Pendant l'enregistrement d'une macro, on peut exécuter une autre macro.
Ceci permet  de réaliser des  opérations complexes, en fragmentant  les éditions
dans plusieurs macros, imbriquées si besoin.
Pex, on peut avoir la macro principale @q qui appelle à des moments divers les 3
macros @a, @b et @c.

---

Parfois on ne sait pas cb de fois  rejouer sa macro pour qu'elle affecte tout le
fichier.
Dans ce  cas, on peut la  préfixer d'un gd  nombre (ex: 9999) ou bien  créer une
macro récursive.
Une macro récursive s'appelle elle-même.
Pour créer une macro récursive stockée dans le registre q, il faut:

   1. qqq      vider le contenu du registre q
   2. qq       débuter l'enregistrement de la macro q
   3. xxx      réaliser sa macro

   4. @q       appeler la macro a depuis elle-même
               c'est ici qu'il est important d'avoir vidé le contenu du registre q au début

   5. q        finir l'enregistrement

Pour limiter la  répétition d'une macro à  la ligne courante plutôt  que tout le
buffer, faire débuter la macro avec:

    let a=line('.')

Et à la fin de la macro, remplacer @q par:

    if line('.')==a | exe 'norm @q' | endif

Cette dernière  commande ne rejoue  la macro que  si le n°  de la ligne  n'a pas
changé.

---

    "=1+2 CR p

            colle l'évaluation du registre expression, contenant 1+2: 3

            Le registre expression ne devient pas le dernier registre modifié.
            Il n'est utilisé que temporairement.
            Une fois  qu'on a collé  son contenu, p  (et ses amies)  utilisent à
            nouveau "" ou "+.

    qA

            débute  un  enregistrement  des  frappes  dans  le  registre  a  (en
            mode  append,  sans  écraser   son  contenu)  utile  pour  reprendre
            l'enregistrement  d'une macro  dont  on a  interrompu la  définition
            prématurément

    @a    :@a

            exécuter le contenu du registre a en mode normal / sur la ligne de commande

            Sur  la ligne  de commande,  le contenu  du registre  est interprété
            comme des commandes Ex:

                   :let @a = 'echo "hello"'
                   :@a

                                               NOTE:

            En mode  normal, si  le registre  a contient  le caractère  'q', les
            frappes qui suivent sont bien  exécutées, mais pas enregistrées dans
            une macro.


    nno <key> :call MyFunc(@%)<cr>
    au FileType python  call MyFunc(@#)

            Définit un mapping  qui appelle une fonction à laquelle on passe le nom du buffer courant.
            "       une autocmd "                                                             alternatif

    0v^hy

            copier l'indentation de la ligne courante
            Utile si on veut donner le même niveau d'indentation à une autre ligne.


    :let @a ..= '@a'
    qA@aq

            rend la macro a récursive

    :let altbuf = bufnr('#') | ... | let @# = altbuf

            Stocke le n°  du buffer alternatif dans la  variable altbuf, exécute
            des commandes  qui modifient  le buffer  alternatif pour  la fenêtre
            courante, restaure le buffer alternatif d'origine.

            Cette commande illustre le fait qu'on peut écrire dans le registre #
            et que ce dernier contrôle le buffer alternatif.

    :.,$norm @q
    :*norm @q

            rejouer la macro q sur les lignes du fichier entre la ligne courante
            et la fin du fichier ou sur la sélection visuelle

            J'ai défini  des mappings customs  (@@, @a-z) permettant  de rejouer
            automatiquement une macro sur une sélection visuelle.
            Donc la 2e  commande est bonne à connaître mais  ne devrait pas être
            utile.

    :{range}norm! C-r q

            rejouer une séquence de frappes sur chaque ligne à l'intérieur d'une rangée

            En passant les frappes directement à :norm!
            plutôt que le nom de la macro,  on peut les éditer par la suite dans
            l'historique des commandes (q: ou ↑).

            De plus, :1,5norm!  C-r q présente un autre avantage par rapport à 5@q.
            En effet, 5@q nécessite que  pendant l'enregistrement de la macro q,
            on s'assure qu'à la fin on finit  bien au début de la ligne suivante (j_).
            :norm le fait automatiquement pour nous.

    :reg xy

            afficher le contenu des registres x et y

    :23,27 y[ank] a

            copier les lignes 23 à 27 dans le registre a

Une macro peut inclure des changements de fenêtre.
Cas de figure où ça peut être utile: on a un buffer contenant un listing de noms
de fichiers  et un  autre contenant  du texte dont  on souhaite  s'assurer qu'il
contient chaque nom de fichier du listing (ex: un makefile).

    gg0              se rend au début du fichier
    qf               débute l'enregistrement de la macro f
    y$               copie la 1e ligne contenant un 1er nom de fichier
     C-w w           passe à l'autre fenêtre (celle du makefile)
    /C-r " CR        cherche le nom de fichier copié (stocké dans le registre par défaut)
    C-w wj           repasse à la fenêtre du listing et on descend d'une ligne
    @f               appelle la macro f pour que celle-ci devienne récursive
    q                termine l'enregistrement de la macro

Résultat, si tous les noms de fichiers  sont bien présents dans le makefile, ils
seront tous mis en surbrillance.
En revanche,  si à  un moment  donné, un  fichier n'est  pas trouvé,  une erreur
survient et la macro s'interrompt

                                     FIXME:

En théorie,  chez moi  ça marche  pas; toutefois on  peut toujours  regarder les
messages d'erreur via `:messages`.

Source: <http://vim.wikia.com/wiki/Record_a_recursive_macro>

##
# Pitfalls
## During a recording
### after `o` or `O`, do *not* press `C-u` to remove all the indentation of the current line.

Prefer pressing `Escape` then `i`.

Rationale: there is no guarantee that  the next time you execute your recording,
there will be an indentation; it depends from where you open a new line.  And if
there's no indentation, `C-u` may remove the previous newline.

    vim -Nu NONE <(cat <<'EOF'
        indented
    NOT indented
    EOF
    ) +'set autoindent backspace=eol,start | let @q = "o\<c-u>\<esc>"'
    " press @q on the first line: a new line is opened below
    " press @q on the second line: NO new line is opened below,
    " because C-u has immediately removed the newline added by the 'o' command

### do *not* end your recording right after pressing `CR`.

Press something afterwards, like `Escape`, then you can end your recording.

Rationale: for some reason, Vim adds a `C-j` to a register ending with `CR`:

    let @q = ":\r"
    reg q
    "q   :^M^J
            ^^

And because of that, when you execute your recording, `C-j` may be pressed.
If you've mapped something to `C-j`, it may have unexpected effects.

    vim -Nu NONE +'let @q = ":\<cr>"' +'nno <c-j> :echom "this should NOT be executed"<cr>'
    " press @q: the C-j mapping is executed (the message is logged)

I can reproduce when `CR` is pressed in other modes, like normal mode:

    vim -Nu NONE +"pu=''" +'let @q = "\<cr>"' +'nno <c-j> :echom "this should NOT be executed"<cr>'
                  ^^^^^^^
                  there needs to be a line after the one from which we press `@q`,
                  otherwise, `^M` would fail and Vim would stop executing the recording

---

It may be related to `:h 'ff'` and `:h file-formats`.

                            vvv
    $ vim -Nu NONE +'set ff=mac | let @q = ":\r"'
    reg q
    "q   :^J^J
          ^^

What's weird  is that  the translation  of `^M` into  `^M^J` occurs  even though
I'm  on  Linux  and not  on  Windows,  and  even  if I  set  `'fileformat'`  and
`'fileformats'` to `unix`.

Or maybe the issue is related to  `:h CR-used-for-NL`, `:h NL-used-for-Nul`...

##
# Issues
## I can't copy more than 4000 characters in the clipboard from Nvim!

Nvim may be using `xsel(1x)`, which has [an issue][1].

It has been fixed by [this PR][2].

Update `xsel(1x)`, or compile it from source:

    $ git clone https://github.com/kfish/xsel
    $ cd xsel
    $ ./autogen.sh
    $ ./configure
    $ make
    $ sudo make install

## I've copied a block of text in the system clipboard from Nvim.  Pasted in another Vim instance it gets linewise!

    $ nvim -Nu NONE <(cat <<'EOF'
    xxx
    xxx
    xxx
    EOF

    " yank the second column of x's in the clipboard selection (`"+y`)
    :echo getregtype('+')
    ^V1~

    " without closing the first Nvim instance, start a second one
    $ nvim -Nu NONE
    :echo getregtype('+')
    V~

It seems to be an issue with Nvim.
I don't have a solution right now.
I've tried to  use another clipboard manager (taken from  `:h g:clipboard`), but
none fixed the issue:

    let g:clipboard = {
        \   'name': 'my_clipboard',
        \   'copy': {
        \      '+': 'xclip -selection clipboard',
        \      '*': 'xclip -selection clipboard',
        \    },
        \   'paste': {
        \      '+': 'xclip -selection clipboard -o',
        \      '*': 'xclip -selection clipboard -o',
        \   },
        \   'cache_enabled': 1,
        \ }

    let g:clipboard = {
        \   'name': 'my_clipboard',
        \   'copy': {
        \      '+': 'xsel -ib',
        \      '*': 'xsel -ib',
        \    },
        \   'paste': {
        \      '+': 'xsel -ob',
        \      '*': 'xsel -ob',
        \   },
        \   'cache_enabled': 1,
        \ }

    let g:clipboard = {
          \   'name': 'myClipboard',
          \   'copy': {
          \      '+': 'tmux load-buffer -',
          \      '*': 'tmux load-buffer -',
          \    },
          \   'paste': {
          \      '+': 'tmux save-buffer -',
          \      '*': 'tmux save-buffer -',
          \   },
          \   'cache_enabled': 1,
          \ }

    let g:clipboard = {
          \   'name': 'myClipboard',
          \   'copy': {
          \      '+': {lines, regtype -> extend(g:, {'foo': [lines, regtype]}) },
          \      '*': {lines, regtype -> extend(g:, {'foo': [lines, regtype]}) },
          \    },
          \   'paste': {
          \      '+': {-> get(g:, 'foo', [])},
          \      '*': {-> get(g:, 'foo', [])},
          \   },
          \ }

Worse,  with all  of them  – except  the last  one –  the type  is automatically
converted from `^V` to `V`, inside the Nvim instance where the text is yanked.

See also [this issue][3] (it may be related ... or not).

##
# Reference

[1]: https://github.com/kfish/xsel/issues/13
[2]: https://github.com/kfish/xsel/pull/16
[3]: https://github.com/neovim/neovim/issues/1822
