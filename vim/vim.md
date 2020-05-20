# Starting (N)Vim
## How to get the name of the shell command which was executed to start the current Vim process?

    :echo v:progname

Example:

    $ vimdiff ~/.bashrc ~/.zshrc
    :echo v:progname
    vimdiff~

## How to get the name of the binary which was executed to start the current Vim process?

Several Vim binaries can be installed.  How to detect which one is responsible for the current Vim process?

    :echo v:progpath

##
## When starting Vim, how to make it become a server?

    $ vim --servername MYSERVER

### How to do it *after* Vim was started?

    :call remote_startserver('MYSERVER')

## How to print all running servers on stdout?

    $ vim --serverlist

## How to print all running servers in Vim?

    :echo serverlist()

This doesn't work as you may expect in Nvim.
It doesn't list *all* Nvim running servers.
It  only lists  the running  Nvim servers  which were  started from  the current
instance via `serverstart()` (which is an Nvim-only function).

##
## From another shell, how to make a running Vim server
### edit some file?

    $ vim --remote /path/to/file --servername MYSERVER
          ^^^^^^^^

#### in a new tab page?

    $ vim --remote-tab /path/to/file --servername MYSERVER
                  ^^^^

### type some keys?

    $ vim --remote-send '<esc>:echom "test"<cr>' --servername MYSERVER
                  ^^^^^

Note that  the string argument  passed to  `--remote-send` is able  to translate
special sequences such as `<esc>` and `<cr>` just like any mapping command.

### evaluate some Vim expression?

    $ vim --remote-expr 'Func()' --servername MYSERVER
                  ^^^^^

##
## When starting Nvim, how to make it become a server?

There's no need to.  Nvim becomes a server automatically.

### How to get its address?  (2)

    :echo v:servername
    :echo $NVIM_LISTEN_ADDRESS

### How to set its address from the shell?  (2)

    $ nvim --listen '/tmp/mysocket'
    $ NVIM_LISTEN_ADDRESS=/tmp/mysocket nvim

### How to pass a `--remote-*` argument to Nvim?

You can't directly.  But you can install the `neovim-remote` package via the pip installer:
<https://github.com/mhinz/neovim-remote>

It provides the `nvr` command; use it as a replacement to `nvim` in your command.
Examples:

    $ nvr --remote file1 file2

    $ nvr --remote-send 'iabc<esc>'

    $ nvr --remote-expr 'bufname("")'

##
## What's special about the server names `VIM` and `/tmp/nvimsocket`?

They are used as a fallback when you use `--remote-*`, but not `--servername`,
resp. in a Vim command and in a nvr one.

#
# Misc.
## Which help tags can give me an overview of all the available commands?

    :h quickref
    :h index

In `:h quickref`, commands are organized around common themes.
In `:h index`, they are organized around modes.

## How to make Vim display all the hidden buffers?

Use `:unhide`.

    $ vim -p /tmp/file{1..3}
    :tabonly
    :unhide

It only works  if you don't have  too many hidden buffers  (otherwise `E36`: not
enough room).

---

Note that it doesn't work here:

    $ vim /tmp/file{1..3}
    :unhide

That's  because even  though `/tmp/file2`  and `/tmp/file3`  are not  displayed,
technically,  they are  not hidden  buffers.  They  are just  file paths  in the
buffer list.  They will be loaded/created once you visit them.

## Why does the cursor move one character backward when I press `i Esc`?

In insert mode, a character is *between* 2 characters.
In normal mode, a character is *on* a character.

And while in normal  mode there are `n` possible characters  on which the cursor
may be, in insert mode there are `n+1` possible positions for the cursor (“posts
vs fences”).

When you  switch to insert  mode from  normal mode, the  cursor has to  choose a
position between 2 characters.   And when you press `i`, it  chooses to be right
before the character on which it was in normal mode: this makes it look like the
cursor moves half a character backward.

Now you  may wonder why Vim  chooses to go to  the left position instead  of the
right one.  That's because, most of the  time, when you're typing, the cursor is
at the end of  the line, and there, `Esc` can only go  left.  So the most common
behavior was generalized to other cursor positions (i.e. in the middle of a line).

Further reading:
- <https://unix.stackexchange.com/a/11405/289772>
- <https://github.com/neovim/neovim/issues/11456#issuecomment-558072430>
- <https://www.reddit.com/r/vim/comments/a9zzv5/last_character_end_of_file/ecnwnln/>

##
# Pitfalls
## I've lost all the undo history of my file!

You probably have modified your file from outside Vim.
For example, assuming `file` is *not* opened in a Vim instance, if you run:

    $ echo 'hello' >>file

All the undo history of `file` is lost.

That's because the  hash of the contents  of the file no longer  matches the one
which was saved in the undo file.  See `:h undo-persistence`.

You  can try  to recover  the undo  history  by editing  the text  so that  it's
identical to  the last time  the undo file  was saved; but  you need to  do that
while `'undofile'` is reset.

See `ex.md`, and look for `undofile`.

---

If  the file  is still  currently loaded  in  a Vim  buffer, and  if the  latter
contains fewer than 10000 lines (see  `:h 'undoreload'`), just reload the buffer
with `:e` or `:e!`.  When Vim re-reads the file, the undo tree should be updated
and saved.

If you don't reload,  and just quit Vim, when you'll re-edit  the file, the undo
history will be lost.

In practice, I think we don't have to reload the buffer in such a case, probably
because:

   - we set `'autoread'`
   - we execute `:checktime` from various events (`BufEnter`, `CursorHold`, `InsertEnter`, ...)

So Vim automatically reloads the buffer when it detects that the file has changed.

##
##
##
# Édition
## Divers

Un opérateur (c, d, y, g@ …) est:

   - une commande normale appelant une fonction qui agit sur le texte encadré
     par les “change marks”

   - une commande normale appelée depuis le mode visuel et agissant sur le
     texte encadré par les “visual marks”

En mode normal, il attend un mouvement ou un text-object pour pouvoir placer les
change marks avant d'appeler la fonction.
Un  mouvement  peut   être  utilisé  à  la  place  d'un   text-object  (en  mode
operator-pending).

---

    just = make,
           all,
           the,
           commas,
           line,
           up

            C-v 4j C,ESC P gv:s/,

    :'a,'b yank / delete / join

            copier / supprimer / fusionner les lignes entre les marques a et b

    :y | d | j    5

            copier / supprimer / fusionner la ligne courante et les 4 qui suivent

                                               NOTE:

            On pourrait aussi utiliser la commande suivante:

                    :.,.+5    y | d | j

            Le point peut être omis :    ,+5    y|d|j


    :g/^Error/.w! >> errors.txt

            Écrire toutes les lignes du buffer commençant par 'Error' dans le fichier `errors.txt`.

                                               NOTE:

            On remarque que `:write` doit être précédée de l'adresse `.` (ligne courante).
            En effet, `:write` est une des rares commandes Ex qui par défaut utilise comme rangée
            tout le buffer. D'habitude une commande Ex utilise par défaut la ligne courante.

            On fait également connaissance avec le token `>>` qui permet d'append des lignes à la fin
            d'un fichier.
            Sans `>>`, `:write` écrase entièrement le contenu du fichier qu'on lui passe en argument.

            Le bang à la suite de `:w` permet de créer `errors.txt` s'il n'existait pas au départ.
            Sans le bang, on aurait l'erreur suivante:

                    "errors.txt" E212: Can't open file for writing


    ga    g8

            affiche des informations sur le caractère sous le curseur

            g8 affiche les octets utilisés pour coder le caractère.
            Ils dépendent de l'encodage utilisé par le fichier.

            On peut s'apercevoir que les octets utilisés pour les 256 premiers caractères sont
            identiques au point de code de ces derniers.

            En revanche, au-delà, les 2 diffèrent.  Même leur taille peuvent différer. Ex:

                    ―    \u2015      2 octets
                         e2 80 95    3 octets

    gQ    g/BUG/vi[sual]    {edits}    gQ    …

            effectuer une suite d'éditions arbitraire ({edits}) autour de chaque ligne contenant le pattern BUG:

                1. gQ                 passe en mode Ex

                2. g/BUG/vi[sual]     nous amène en mode “visuel“ pour chaque ligne contenant BUG
                                      où on pourra effectuer nos éditions

                3. {edits}            on effectue nos éditions complexes / imprévisibles car dépendent
                                      du contexte

                4. gQ                 nous ramène en mode Ex, dans lequel la commande globale tourne tjrs
                                      :g nous refait passer en mode “visuel“ à la prochaine ligne contenant BUG

            Utile qd  nos éditions sont  trop imprévisibles pour être  passées à
            :g, et qu'on ne peut pas facilement utiliser n/N pour naviguer d'une
            occurrence de BUG à une autre, car nos éditions modifient sans cesse
            le registre recherche.

            On profite du fait qu'à chaque fois que :g exécute :visual depuis le
            mode Ex, elle est obligée d'attendre  qu'on ait fini nos éditions et
            qu'on quitte le mode “visuel“.

            Si BUG apparaît 100 fois dans le buffer et qu'après avoir traité les
            10 premières occurrences, on pense  avoir terminé, on peut rester en
            mode visuel jusqu'à la fin de la session.
            Mais si on a à nouveau besoin du mode Ex, et qu'on appuie sur gQ, :g
            nous amène automatiquement à la 11e occurrence de BUG.
            On ne  peut plus  utiliser le mode  Ex tant qu'on  n'a pas  passé en
            revue les 90 occurrences restantes.
            Comment annuler la commande globale suspendue?

                    - écrire le buffer, puis le recharger
                    - taper C-c C-c puis :vi

                                               NOTE:

            Quelle différence entre Q et gQ ?
            Q nous fait entrer dans un mode qui essaie d'émuler l'éditeur Ex aussi fidèlement que possible.
            gQ nous fait entrer dans un mode similaire, mais contrairement à Q, il conserve tout ce qu'on
            peut utiliser sur la ligne de commande traditionnelle:

                    - complétion via Tab
                    - navigation sur la ligne de commande (C-e pour aller à la fin de la ligne…)
                    - abréviations (cnorea)
                    - mappings (cmap), …

    :5,10norm! .

            Répéter la dernière édition sur les lignes 5 à 10.
            Plus généralement, on peut  passer n'importe quelle rangée (visuelle
            pex `*`) et ainsi répéter une édition sur un groupe de lignes


    :m+1
    :undojoin | m+1

            déplacer la ligne courante d'une ligne vers la fin du buffer (:m+1)
            puis répéter l'opération sans casser le bloc d'éditions
            i.e. si on fait un undo, on défait les 2 déplacements d'un coup (pas besoin de 2 undo)

            Équivalent en mode ligne de commande de C-g U en mode insertion.

    :*!cat -n

            numéroter les lignes sélectionnées visuellement

            On filtre la rangée de lignes via la commande shell cat.
            Cette dernière echo les lignes qu'on écrit sur son entrée standard en les préfixant d'un n°,
            à cause de l'argument -n.

                                               NOTE:

            On perd l'alignement des lignes, car cat ajoute des espaces avant et après les n° ainsi
            qu'un caractère tab après chaque n°.
            Début de solution:        :*s/\s\+// | *s/\t\s*/    /


    C-viw 5j 42 C-a

            incrémente le nombre sous le curseur et les 5 suivants de 42


    gaip*=

            aligner les champs du paragraphe se terminant par = en ajoutant des espaces à la gauche de chaque =

            Ex:

                 foo = 2 + 2 = 4                     foo    = 2 + 2         = 4
                 barbaz = 2 * 3 + 3 = 9        ⇒     barbaz = 2 * 3 + 3     = 9
                 qux = 1 + 1 + 1 + 2 = 5             qux    = 1 + 1 + 1 + 2 = 5

            Commande possible grâce au plugin vim-easy-align qui fournit l'opérateur `ga`.


    2gaib,

            aligner les 2 premiers champs se terminant par une virgule à l'intérieur du bloc entre parenthèses
            en ajoutant des espaces à la droite de chaque virgule

            Ex:
                 $names = array(                                    $names = array(
                     'bill', 'samantha', 'ray', 'ronald',               'bill',    'samantha', 'ray', 'ronald',
                     'mo', 'harry', 'susan', 'ted',           →         'mo',      'harry',    'susan', 'ted',
                     'timothy', 'bob', 'wolverine', 'cat',              'timothy', 'bob',      'wolverine', 'cat',
                     'lion', 'alfred', 'batman', 'linus',               'lion',    'alfred',   'batman', 'linus',
                 );                                                 );


                     hello foo world bye all     hello           foo world bye all
    ga2j C-x foo  →  hello world foo bye all  →  hello world     foo bye all
                     hello world bye foo all     hello world bye foo all

            Aligner les champs se terminant par foo sur la ligne courante et les 2 suivantes.


    ~    g~~    g~{motion}

            changer la casse:

                    - du caractère sous le curseur ou de la sélection visuelle
                    - de la ligne
                    - des caractères couverts par {motion}

            ~ ne se comporte comme un opérateur que si l'option 'tildeop' est activée ou en mode visuel.
            Autrement, ~ est une forme abrégée de g~l.

            g~ est un opérateur et g~~ est une forme abrégée de g~g~.


    guu    gUU

            faire passer le texte sur la ligne en minuscule / majuscule

                                               NOTE:

            Ceci illustre 2 conventions respectées par les opérateurs:

                    - qd on répète 2 fois un opérateur, il agit sur toute la ligne. Ex:

                            cc
                            dd
                            yy
                            ~~
                            !!
                            ==
                            >>
                            <<

                    - qd l'opérateur est composé de 2 caractères, on peut se contenter de répéter
                      son dernier caractère:

                            g~~
                            guu
                            gUU
                            gqq
                            g??

                    g~~, guu, gUU, gqq, g?? sont des formes abrégées (g~g~, …).

    guib    gUib

            faire passer le texte entre parenthèses en minuscule / majuscule

    v{motion}u    v{motion}U

            faire passer la sélection visuelle en minuscule / majuscule

    3 g C-a
    5 g C-x

            {in|dé}crémenter chaque chiffre d'une colonne de chiffres sélectionnée en mode visuel
            par bloc, en ajoutant / retirant à chacun n*[count] (n étant la position dans la colonne)

            Fonctionne aussi avec des lettres si on a ajouté la valeur 'alpha' à l'option 'nrformats'.

            `g C-a` et `g C-x` permettent de générer des suites arithmétiques.


    C-o v {motion} v

            passer en mode visuel depuis le mode insertion, sélectionner du texte et revenir au mode insertion
            {motion} permet de déplacer le curseur via des commandes normales sans quitter le mode insertion.

    3 .

            Répéter 3 fois le dernier changement.

            Le dernier changement est le dernier opérateur + text object/motion.
            Le précédent count, qui a pu précéder ou suivre l'opérateur, est remplacé par 3.
            IOW, les invocations suivantes de `.` utiliseront 3 comme count, peu importe le count
            d'origine.

                    2daw
                    3.
                    3daw~

                    d C-v 2j
                    3.
                    3 d C-v j~

                      C-v 2j d
                      3.
                      3 d C-v j~

            Si le dernier opérateur nous a fait passé en mode insertion, le texte inséré fait partie du
            dernier changement.

    yy 99p u 1.

            Yank current line, paste it 99 times, undo (because you realized you
            made a mistake), re-paste but only once.

            This shows that you can fix the count of the last edition when you repeat it.

    :echo "\U0045\U0308\U0301\U033D\U0359\U0359\U032C\u0044\u0357\u0303\u0352\u0305\u0310\u0326\u0049\u036f\u0300\u036b\u0351\u0367\u031e\u0054\u031e\u004f\u0306\u0306\u030e\u030d\u034d\u032d\u0052\u0313\u0346\u033a\u031f\u033c\u0348"

            Outputs `Ë͙͙̬̹͈͔̜́̽D̦̩̱͕͗̃͒̅̐I̞̟̣̫ͯ̀ͫ͑ͧT̞Ŏ͍̭̭̞͙̆̎̍R̺̟̼͈̟̓͆`.
            Illustrates how you can generate composing (or combining?) characters.
            You use an escape sequence for a base character (like `E`, `D`, `I`,
            ...) then you add escape sequences for combining characters.

## Coller / Importer

    C-v {motion1} y {motion2} p

            coller un bloc de texte A à la suite d'un autre B

            {motion1} sélectionne le bloc A
            {motion2} nous amène à la fin de la 1e ligne de B

                                               NOTE:

            Qd on copie un bloc de texte dont la longueur des lignes est irrégulière,
            Vim insère automatiquement des espaces pour que toutes les lignes aient la même longueur.
            Ce comportement peut être indésirable si on ne veut pas que le texte soit altéré.
            La question et la réponse suivante montre comment résoudre ce pb.

---

En mode normal, on peut coller du texte de 5 façons différentes (les 3 dernières sont custom):

    gp    gP    positionne le curseur à la fin du texte collé et non au début

    ]p    [p    respecte le niveau d'indentation de la ligne courante
                contrairement aux autres méthodes, ici le préfixe ] / [ contient 2 informations:

                    - l'action: coller en respectant le niveau d'indentation
                    - le lieu:  ] = en-dessous, [ = au-dessus

                Le p n'est nécessaire que pour rendre ces 2 mappings cohérents avec les autres,
                et pour éviter un pb de timeout ([[, ]], …).

    >p    >P    ajoute un niveau d'indentation par rapport à la ligne courante
    <p    <P    supprime un niveau d'indentation par rapport à la ligne courante
    =p    =P    auto-indente

Les 4 dernières façons permettent de coller un texte characterwise sur une ligne dédiée, au lieu de la ligne
courante.

---

    ]p    [p

            colle le texte sous/au-dessus de la ligne courante en respectant son
            niveau d'indentation

            ex: On coupe un bloc de  texte avec différentes lignes indentées qui
            ont différents niveaux d'indentation.

            La 1e ligne du bloc (et  donc toutes les suivantes) est indentée par
            un caractère tab inutile.
            On  place  son  curseur  sur   une  ligne  sur  laquelle  le  niveau
            d'indentation est nul.
            Une ligne vide a un niveau d'indentation nul.
            En collant avec ce raccourci, la  1e ligne du bloc reçoit un nouveau
            niveau d'indentation identique à celle qui précède, donc nul ici, et
            les  autres reçoivent  un niveau  d'indentation égal  à leur  ancien
            niveau - 1.

            Résultat:  on colle  bien le  bloc sans  changer les  différences de
            niveau d'indentation entre les lignes du bloc, mais on supprime bien
            au passage un niveau pour chaque ligne.

    >p    >P

            colle le texte sous/au-dessus de la ligne courante en ajoutant un niveau d'indentation
            par rapport à cette dernière

    <p    <P

            colle le texte sous/au-dessus de la ligne courante en supprimant un niveau d'indentation
            par rapport à cette dernière

    =p    =P

            colle le texte sous/au-dessus de la ligne courante en auto-indentant, en respectant nos
            options relatives à l'indentation.

    P    p

            Si le registre par défaut contient un texte:

                    - characterwise,    le coller avant le curseur / après le caractère suivant le curseur
                                        et positionner le curseur SUR le DERNIER caractère collé

                    - linewise,         le coller avant / après la ligne courante
                                        et positionner le curseur SUR le 1ER caractère collé

                                               NOTE:

            Si on utilise à la place gP et gp, le résultat est similaire à ceci près que le curseur
            est TOUJOURS positionné APRÈS le DERNIER caractère collé.

            Si le texte collé est linewise, le dernier caractère est un newline et donc le curseur
            est positionné sur la ligne suivante.

    :put _

            coller une ligne vide sous la ligne courante

    :g/\v^%2l|%4l/pu _    :4pu _ | 2pu _

            insérer une ligne vide après la 2e et 4e ligne

            Qd on insère une ligne vide sous la 2e ligne, on change les adresses des lignes en-dessous.
            Si on veut en insérer plusieurs, il faut donc commencer par celles du bas et remonter ensuite.
            Solution 2:    :4pu _ | 2pu _

            Ou bien utiliser la commande globale :g et les atomes du type %123l.
            En effet, au cours de sa 2e passe, :g n'agit pas sur les lignes d'adresses 2 et 4,
            mais sur les lignes qui ont été marquées au cours de la 1e passe.

    :put! =nr2char(10)

            coller au-dessus de la ligne courante un newline (insérer une ligne vide)

                                               NOTE:

            Par défaut, :put colle en-dessous de l'adresse qu'on lui passe (ici la ligne courante).
            Pour lui demander de coller au-dessus plutôt qu'en-dessous il faut lui ajouter un bang.

    :r #42

            importer le contenu du buffer n° 42

    :r !date^@-j

            importer la date du jour sur la ligne courante
            Par défaut, :r importe du texte sur une nouvelle ligne.
            Pour positionner le texte sur la ligne courante, on fusionne depuis la ligne d'origine (-j = .-1join).
            Les 2 commandes Ex (:r et :j) sont séparées par un LF traduit en NUL.

            On ne peut pas utiliser un pipe pour séparer :!date de :-j car il serait envoyé au shell
            au lieu d'être interprété par Vim comme une terminaison de commande Ex.

    :r !date^@-j

            insère sous la ligne courante la date et l'heure (:.read !date), puis (^@) réalise
            une fusion de lignes (join) à partir de la ligne précédant la ligne courante (.-1)

    :r !echo $RANDOM
    :put =system('echo $RANDOM')

            coller un nb aléatoire

            Illustre les 2 méthodes possibles pour coller la sortie d'une commande shell.

    :23r fname

            insère le contenu du fichier fname sous la ligne 23

                                               NOTE:

            Qd on utilise une commande :read ou :write en lui donnant un nom de fichier en argument,
            ce dernier devient automatiquement l'alternate file pour la fenêtre courante.
            Pour empêcher cela, il faut retirer les flags a (:r) et/ou A (:w) à l'option 'cpo'.

            Pour l'empêcher ponctuellement le temps d'une seule commande, on peut passer par un hack
            utilisant /bin/cat:

                        :r !/bin/cat fname      insérer le contenu de fname
                        :w !/bin/cat > fname    écrire le buffer courant dans fname

            Comme on ne passe pas de nom de fichier en argument à :r/:w, l'alternate file n'est pas modifié.
            Dans le 2e cas, on écrit sur l'entrée standard de cat et on utilise une redirection > pour
            écrire dans fname.


    :r !sed -n 10,23p fname

            insère les lignes 10 à 23 du fichier `fname` sous la ligne courante


    :r `dpkg -L surfraw \| grep youtube$`
    :r `=system('dpkg -L surfraw | grep youtube$')`

            Insère le fichier contenu dans le package `surfraw` dont le nom se finit par `youtube`.

            Illustre comment importer le contenu d'un fichier dont le chemin est obtenu par une commande
            shell.

            La 2e syntaxe est probablement plus fiable.


    :redir > file
    :redir >> file

            redirige la sortie des prochaines commandes dans file (rajouter un ! si file existe déjà)
            idem mais en mode append (sans écraser)

    :redir => var
    :redir =>> var

            redirection dans la variable var (qui stockera la sortie sous la forme d'une chaîne)
            idem mais en mode append

## Copier / Dupliquer

    :3copy 7    :3t7

            duplique la ligne 3 après la ligne 7
            3 et 7 sont les numéros actuels des lignes, avant que :copy / :t n'opèrent.

            :copy / :t ont besoin d'être suivies d'une adresse, mais pas forcément précédées d'une rangée.
            . est alors implicite.

    :3co.    :3t.

            duplique la ligne 3 après la ligne courante

    :-10,-5t.

            duplique les lignes depuis la 10e jusqu'à la 5e ligne au-dessus de la ligne courante,
            en-dessous de cette dernière

    :+5t.-1

            duplique la 5e ligne en-dessous de la ligne courante, au-dessus de cette dernière

    :-t-    :+t+

            duplique la ligne du dessus / dessous
            équivaut à:    .-1t.-1    .+1t.+1

            Illustre que dans une rangée, il y a 2 caractères qui peuvent être omis/implicites (. et 1).

    :g/foo/t.

            copier chaque ligne contenant la chaîne foo et la coller sous la ligne courante
            résultat: les lignes contenant foo sont dupliquées

    :g/foo/t.|s/./=/g

            copier chaque ligne contenant la chaîne foo, la coller sous la ligne courante puis
            remplacer chaque caractère de la ligne courante par le caractère =

            résultat: souligner les lignes foo avec des lignes remplies de ===

    :1,10g/^/%t$

            duplique le buffer courant 1024 fois (2^10)
            Plus généralement, on peut répéter une commande arbitraire 2^N fois, via:    :1,Ng/^/cmd

            Also, `$` is a line specifier used in a range.
            So, this command shows that you  can use any line specifier (like an
            arbitrary mark `'m`) as the argument of `:t`.
            Same thing for `:m`.

    :g/foo/ mark a | t$ | 'a s/foo/bar/

            dupliquer toutes les lignes contenant foo à la fin du fichier, et substituer foo par
            bar sur les lignes d'origine

                                               NOTE:

            Parmi les commandes exécutées par :g, on peut en utiliser une pour marquer la ligne
            courante , mais on ne peut pas utiliser '' (pour ajouter une ligne comme dernière entrée
            à la jumplist).  Utiliser une marque alphabétique.

                                               NOTE:

            Qd la commande exécutée par :g est une succession de commandes Ex dont plusieurs utilisent
            des adresses relatives à la ligne courante, on risque des effets inattendus. Pex:

                    :g/^$/-s/$/END/ | ++s/^/BEGINNING

            Cette commande est censée ajouter BEGINNING et END au début et à la fin de chaque paragraphe,
            en supposant que 2 paragraphes soient simplement séparés par une ligne vide.

            L'adresse ++ est relative à la position courante, qui dépend de la précédente commande.
            On peut considérer que ++ est relative à - qui est relative à ligne de départ.
            Pb: si le buffer commence par une ligne vide, la 1e substitution ne se fera pas sur la ligne
            précédente comme elle devrait (-s/…), mais sur la ligne courante, car :s ne peut pas remonter
            d'une ligne.
            La 2e substitution (++s/…) ne va donc pas se faire sur la 1e ligne du paragraphe, mais la 2e.

            La 2e erreur aurait pu être évitée. Comment?
            En marquant la ligne courante dès le début (:mark a), puis en se référant constamment
            à cette position. Ainsi, au lieu d'écrire ++s/…, on préférera 'a+s/…

## Corriger

    :mkspell! ~/.vim/spell/fr.utf-8.add

            Regénère le fichier binaire ~/.vim/spell/fr.utf-8.add.spl

            Les mots justes / faux qu'on ajoute sont stockés dans ~/.vim/spell/fr.utf-8.add.
            Pour que Vim tienne compte du contenu de ce fichier, il faut qu'une vérification sur
            le binaire fr.utf-8.add.spl réussisse.

            Versionner ce binaire avec git peut poser pb (conflits entre différentes versions).
            La commande :mkspell! permet de regénérer le binaire qd on passe sur une autre machine.
            Le bang ! permet d'écraser un ancien binaire s'il en existe déjà un.


    :runtime spell/cleanadd.vim

            Supprimer les entrées de la liste fr.utf-8.add qui ont été commentées.
            Le script se situe ds $VIMRUNTIME.


    :spellrepall

            Répète le remplacement réalisé par le dernier `z=` pour tous les autres mots identiques
            au sein de la fenêtre courante.


    1z=

            appliquer automatiquement la 1e suggestion de correction proposée (sans passer par le menu)

    [s    ]s

            se rendre au précédent/suivant mot contenant une faute d'orthographe

    [S    ]S

            Idem, mais cette fois on ignore les mots rares (SpellRare) ou provenant d'une autre région (SpellLocal).
            Cherche uniquement un mot mis en surbrillance par le HG SpellBad.

    zg    zw

            indique à Vim que le mot sous le curseur est juste / faux (g = good, w = wrong)

            Le mot est ajouté à une liste dans le 1er fichier présent dans l'option locale au buffer 'spellfile'.

            Par défaut, cette dernière est vide, ce qui signifie que Vim la configure automatiquement qd
            on appuie sur zg/zw: il choisit le 1er dossier présent dans &rtp (il y crée le sous-dossier spell/),
            et y écrit un fichier dont le nom suit la forme {&spelllang}.{&encoding}.add
            Ex: ~/.vim/spell/fr.utf-8.add

            Qd on écrit dans plusieurs langues, pour disposer de listes distinctes, on peut configurer
            l'option 'spellfile' et lui fournir une liste de chemins vers différents fichiers.
            Ensuite, qd on tapera {N}zg ou {N}zw, le mot sous le curseur sera ajouté au Ne fichier de 'spf'.

    zG    zW

            idem que zg et zw, à ceci près que les mots sont ajoutés à une liste interne à Vim qui
            est perdue une fois qu'on quitte la session ou qu'on configure 'encoding'

    zug    zuw

            commenter un mot juste / faux de la liste fr.utf-8.add pour annuler un zg / zw

---

La correction orthographique dépend de la valeur de l'option spelllang.
Quand celle-ci vaut 'en', ça implique que si un mot est juste dans une région de
la langue anglaise (`en_gb` =  anglais britannique, `en_us` = anglais américain)
mais pas dans une autre, il ne sera pas corrigé.

Quand l'orthographe  d'un mot  est mauvais  dans une région  d'une langue  (ex :
color dans `en_gb`) mais  juste dans une autre région de  cette même langue (ex:
color  dans `en_us`),  et  que  la correction  orthographique  est activée  (set
spell), il n'est pas colorisé et souligné dans la même couleur que les mots faux
(rouge…) mais dans une autre couleur (vert, bleu…).

## Couper / Changer

    c//e

            couper depuis le curseur jusqu'au dernier caractère de la prochaine occurrence du
            registre recherche

    5cl    5s

            supprimer les 5 caractères après le curseur et passer en mode insertion

    cgn[.]

            Après une recherche, changer la prochaine occurrence (par rapport à la position du curseur).
            Le point permet de répéter le changement de la prochaine occurrence.

            gn permet d'agir sur la prochaine occurrence en combinaison avec n'importe quel opérateur
            (dgn, gUgn,…), et le point permet tjrs de répéter l'action.

    c%
            coupe un bloc de code situé entre 2 instructions faisant partie d'une même structure syntaxique
            Ne fonctionne que si le curseur se trouve sur une instruction (de préférence sur son 1er caractère).

            Pex, entre 2 instructions consécutives de:

                    if           / else        / endif
                    function     / return      / endfu
                    augroup name / augroup END
                    <body>       / </body>

            Dans le cas d'un tag, le curseur ne doit pas se trouver sur un chevron, autrement
            c'est simplement le tag qui sera changé, et non pas tout ce qui se trouve entre les tags
            ouvrant et fermant.

    fXc%

            coupe l'appel à une fonction (le curseur étant avant le début de son nom) dont le nom commence par X
            Ex: le curseur est placé au début de la ligne     call MyFunc(foo, bar, baz) | other command
                fMc% change uniquement                             MyFunc(foo, bar, baz)


    func1(x|, func2(), y);    →    func1(x, foobar);
                          c])foobar

            `])` est un mouvement qui déplace le curseur sur la prochaine parenthèse non matchée.
            Ici, il couvre tous les caractères entre le curseur et la parenthèse fermant les
            arguments de `func1()`.


    fooqux → barqux    fq cb bar

            changer fooqux en barqux

            À retenir:    f{char} cb    est très utile pour changer le préfixe d'un mot
                                        {char} étant le 1er caractère du suffixe


## Déplacer

    cx C-v 4j    .

            Échanger la position de 2 colonnes de 5 caractères.

            Illustre qu'on peut opérer sur des mouvements / objets blockwise, même avec un opérateur custom.
            À condition que ce dernier ait été correctement codé, et prenne en charge le cas où Vim
            lui envoie l'argument type = 'block'.


    :g/^/m0
    :11,20g/^/m 10

            Inverser l'ordre de tri des lignes:

                    - du buffer (toutes)
                    - 11 à 20


    :g/^/exe 'm -'..(line('.')%4 ? line('.')%4 : 4)

            Inverser l'ordre de tri toutes les 4 lignes.


    :move 10

            Déplace la ligne courante après la ligne actuellement numérotée 10.

            Si l'adresse de la ligne courante est > 10, elle devient 11, car ça ne change rien pour
            les  lignes qui  précèdent  actuellement la  ligne 10.  Elles  conservent toutes  leur
            adresse.

            En revanche, si l'adresse de la ligne courante est < 10, elle devient 10, car les lignes
            entre celle qui suit la ligne courante et la ligne 10 (incluse) reculent d'une place.

            Pour  mieux  comprendre, il  suffit  de  se représenter  toutes  les  lignes comme  des
            personnes dans  une file  d'attente et  la ligne  courante c'est  nous. 'm  10' signifie
            'placez-vous après la 10e personne'.

            Si on  est 20e dans la  file d'attente, on passe  en 11e position, car  les 10 personnes
            devant n'ont pas été affectées par notre déplacement.

            Si  on est  5e dans  la file  d'attente, on  passe en  10e position,  car les  personnes
            actuellement 6 à 10 gagnent une place.


    :m0    :m$

            Déplace la ligne courante en 1e / dernière position.

            Combinée avec une commande globale, m0 et m$ sont utiles pour déplacer des lignes matchant un pattern:

                - au début du buffer (en inversant leur ordre relatif)
                - à la fin du buffer (en conservant leur ordre relatif)

    :4m7

            Déplace la  ligne 4  après la ligne  7.
            4 et  7 sont  les numéros actuels  des lignes (avant que le mouvement ne soit opéré).


    :1,10m$

            Déplace les lignes 1 à 10 à la fin du buffer.


    :+10,+20m.

            Déplace les lignes 10 à 20 (adresses relatives à la ligne courante) sous la ligne courante.
            Forme abrégée de:    .+10,.+20m.


    :m -2    :m +1

            Faire reculer / avancer la ligne courante d'une place.

            Qd on donne en argument à la commande :move une adresse relative (-2, +1),
            elle est traduite en adresse absolue (.-2 .+1).


    :m 'x-1

            Déplacer la ligne courante au-dessus de celle qui porte la marque x.


    :?bar?m/foo/

            Déplacer la précédente ligne contenant bar après la prochaine ligne contenant foo.

    :/pat/ | 1,5m.

            Déplacer les lignes 1 à 5 après la prochaine ligne contenant `pat`.
            On pourrait remplacer le pipe par un point-virgule.

## Filtrer

Infographie résumant les différents types d'interaction possibles entre Vim et un programme externe:
<https://4.bp.blogspot.com/-MhHrs8Q-S_A/UJpAuI_mOZI/AAAAAAAAAZ0/aJrXwjlvoYs/s1600/vim_pipes.png>


    !{motion}{filter}

            passer les lignes couvertes par {motion} au programme {filter}

            Le 1er bang indique à Vim qu'on veut remplacer des lignes du buffer par la sortie d'un filtre.

            Après le bang, Vim attend un mouvement pour savoir quelles lignes, puis nous fait passer en mode ligne
            de commande en peuplant la ligne avec:

                    :{range}!

            … où {range} correspond à la rangée de lignes couvertes par le mouvement.

            Ex:    !3j en mode normal se traduit par    :.,.+3! en mode ligne de commande.

            Un filtre est un pgm qui accepte du texte sur son entrée standard, le traite, et écrit le résultat
            sur la sortie standard.
            Par défaut, Vim écrit les lignes couvertes par {motion} sur l'entrée standard du filtre.
            Mais si celui-ci n'accepte pas l'entrée standard comme argument, il peut falloir lui donner
            le nom du buffer courant via '%'.


    :'<,'>!awk '{print $1, $2, $5, $4, $3}'

            échanger les champs n° 3 et 5 sur chaque ligne de la sélection visuelle

            one two three four five      →    one two five four three
            un deux trois quatre cinq         un deux cinq quatre trois


    !!bc

            la ligne courante contenant un calcul, la remplacer par son résultat

    seq 0 250 | xargs printf '%02x\n' | fmt -w49
    !!sh

            insérer un tableau d'une largeur de 49 colonnes remplis des nb de 0 à 250 écrits en hexa

            Explication:

            !!sh passe au shell la ligne courante qui contient la commande 'seq … fmt …'

                    seq 0 250                   retourne la liste des nb 0 à 250

                    | xargs printf '%02x\n'     exécute printf sur chaque nb
                                                %02x\n = padding de 0, 2 chiffres, en hexa, suivi d'un newline

                    | fmt -w49                  formate l'affichage sous la forme d'un tableau de 49 colonnes
                                                de largeur max
                                                fmt est un outil shell permettant de formater du texte,
                                                un peu à la manière de gw dans Vim

                                                Ex:    $ fmt -w40 ~/.bashrc
                                                affiche dans le terminal le contenu de ~/.bashrc avec des lignes
                                                de 40 colonnes max

    5!!{filter}

            envoyer la ligne courante et les 4 suivantes au programme {filter} et les remplacer par sa sortie

    %!column -t [-s:]

            formater l'affichage du buffer en alignant le texte par colonnes
            par défaut, l'espace est utilisé comme délimiteur entre 2 champs (-s: = utiliser le
            double-point à la place)

    %!markdown

            convertir un buffer texte (ou markdown) en html

    !ip nl -ba -w1 -s' '

            numéroter les lignes du paragraphe courant

    !ip sort    !ip shuf

            trier/mélanger les lignes du paragraphes courant

    !ip wc

            remplacer le paragraphe par son nb de lignes, mots et caractères (via la commande shell wc)

    vip!{filter}

            sélectionner visuellement le paragraphe courant pour l'envoyer au programme {filter}
            et le remplacer par la sortie de ce dernier

            vip! = {!}

    vip!tac

            inverser les lignes du paragraphe courant
            tac est un pgm shell qui affiche le contenu d'un fichier ou de ce qu'on écrit sur son entrée
            standard (comme cat), mais en inversant l'ordre des lignes

    vip!uniq -u    vip!uniq -d

            supprime les lignes en double du paragraphe courant
            supprime les lignes uniques + ne conserve qu'une ligne par groupe de lignes identiques

            nécessite que les lignes soient triées au préalable

    :5,10{filter}

            envoyer les lignes 5 à 10 au programme de filtrage {filter} et les remplacer par sa sortie

            Qd on passe directement par le mode Ex pour envoyer des lignes du buffer à un programme de filtrage,
            l'édition n'est pas répétable avec dot (.).
            Ce qui est répété par dot, c'est l'édition qui précède, car le résultat produit par une commande Ex
            n'est pas considéré comme une édition.

            Pour pouvoir répéter une édition réalisée par un programme de filtrage, il faut passer par le mode normal.
            !{motion}filter
            !!{filter}
            vip!{filter}

    !!sh

            passe la ligne courante au shell qui l'exécute et affiche la sortie à la place de la ligne courante

            Il s'agit d'un cas particulier de !{motion}{filter}.
            Ici, le 2e bang remplace {motion} et indique à Vim que le mouvement ne couvre que la ligne courante.
            Résultat on passe en mode ligne de commande avec le début de commande:    :.!

            Il ne reste plus qu'à préciser à quel programme de filtrage on veut envoyer la ligne courante:
            sh = le shell (/bin/sh)

    :%!odt2txt '%'

            convertit un odt en txt

            Le filtre odt2txt n'accepte pas l'entrée standard comme argument, il lui faut un nom de fichier.
            On lui passe donc '%' que Vim va développer en le nom du buffer courant.

            Le 1er % indique simplement qu'on souhaite remplacer l'intégralité du buffer par la sortie
            de la commande shell qui suit.

    :%!xxd [-r]

            convertit le code binaire contenu dans le buffer en hexa (et reconvertit en sens inverse via le flag -r)

            Attention: avant d'éditer un fichier binaire il faut activer l'option 'binary' / 'bin'
            (locale au buffer), pour éviter que Vim n'endommage le fichier en procédant à des …

                    pour ce faire
                    :e ++bin file
                    vim -b file

                                               TODO:

            À compléter

## Formater

    gw{motion}

            formate le texte couvert par {motion}

            Le formatage introduit automatiquement un retour à la ligne, dès qu'une ligne atteint:

                - &tw si != 0
                - min(largeur de la fenêtre, 79), si &tw = 0

            Utilise la fonction de formatage interne à Vim, dont le comportement peut être modifié via l'option
            'formatoptions' / 'fo'.

            Utile pour formater une sélection visuelle contenant des lignes qui ont dépassé &tw caractères.

    gq{text-object}

            formate le texte couvert par {text-object}

            Différences entre les opérateurs gq et gw:

            - gq déplace le curseur sur la dernière ligne formatée, gw le laisse à sa place

            - gq appelle par ordre de priorité:

                  1. la fonction custom définie par l'option locale au buffer    'fex' / 'formatexpr'
                  2. le pgm externe défini par l'option GLOBALE                   'fp' / 'formatprg'
                  3. la même fonction interne que celle utilisée par gw, qui s'appuie uniquement sur &tw, &fo, &wm.

            Vim peuple automatiquement 3 variables qu'on peut utiliser dans une fonction custom ('fex') :

                    - v:lnum     adresse de la 1e ligne à formater
                    - v:count    nb de lignes à formater
                    - v:char     caractère qui va être inséré qd la fonction est évaluée (formatage automatique)

            v:lnum et v:count sont utiles qd la fonction est appelée manuellement via gq.
            Grâce à elles, on pourra pex définir les variables start et end comme ceci:

                    let start = v:lnum
                    let end   = v:lnum + v:count - 1

            … et utiliser la rangée start,end pour répéter une opération sur chaque ligne à l'intérieur.
            Pour raccourcir le code, on pourra aussi les passer directement en argument à la fonction:

                    setl fex=MyFormatExpr(v:lnum,v:lnum+v:count-1)

                    fu MyFormatExpr(start, end)
                        sil! exe a:start . ',' . a:end . 's/[.!?]\zs /\r/g'
                    endfu

            Ici, la fonction casse les lignes après chaque caractère de ponctuation (.!?).

            v:char est utile si la fonction est évaluée automatiquement (formatage automatique,
            celui qui hard wrap une ligne dépassant &tw).

## Fusionner

    :%join[!]

            fusionner toutes les lignes du buffer (% = 1,$)

            Le bang empêche Vim d'ajouter / supprimer des espaces au cours de la fusion.

    :'a,'bg/foo/j

            dès qu'une ligne entre les marques a et b contient foo, la fusionner avec la ligne qui suit
            équivaut à appuyer sur J en mode normal

    :g/^\s*$/,/\S/-j

            fusionner toutes les lignes vides

    :%g/^ /-1j

            fusionner chaque ligne précédant (-1) une ligne commençant par un espace avec la suivante

    :1,4g/^/5m.|-j!

            fusionner les lignes 5 à 8 avec les lignes 1 à 4

    :.,.+3g/^/''+4m.|-j!

            fusionner le bloc de lignes commençant à partir de la ligne courante et ayant 4 lignes,
            avec le bloc de 4 lignes qui suit

            Cette commande utilise le fait que la commande globale laisse la marque '' sur la ligne
            où se trouve le curseur avant de sauter vers la 1e ligne à traiter (techniquement on dit
            qu'elle ajoute une entrée dans la jumplist).
            Elle ne le fait pas pour toutes les lignes à traiter, juste avant la 1e.
            De ce fait, ici,    '' = adresse de la 1e ligne du 1er bloc
                        et    ''+4 = adresse de la 1e ligne du 2e bloc.

    gJ

            fusionner 2 lignes sans ajouter ou supprimer d'espaces

            si la 2e ligne commence par des leading whitespace, gJ les préserve (J les remplace par un espace)
            si la 2e ligne ne commence pas par des leading whitespace, gJ n'ajoute rien (J ajoute un espace)

    5J

            fusionner la ligne courante et les 4 suivantes

## Historique

    :ea 1f

            remettre le fichier dans l'état où il était lors de la dernière sauvegarde
            (:ea 2f = il y a 2 sauvegardes, etc.)

    :ea[rlier] N

            remettre le fichier dans l'état où il était il y a N modifications

    :ea Ns, Nm, Nh, Nd

            N secondes, minutes, heures, jours

    :lat[er] N
    :la Ns, Nm, Nh, Nd

            opérations inverses des précédentes

## Indenter

Qd on insère un tab, le nombre de cellules qu'il occupe dépend de l'endroit où l'on se trouve sur la ligne.
En effet, l'insertion d'un tab signifie qu'on souhaite que le texte qui suit ait pour niveau d'indentation
(nb de cellules précédentes; sortie de indent('.')) le plus petit multiple de &ts possible.
Pex, si on a la ligne 'abcde', un tab inséré après:

    - a       occupe    3 cellules    de sorte que 'bcde'    ait un niveau d'indentation de 4
    - ab         "      2     "       "            'cde'     "
    - abc        "      1     "       "            'de'      "
    - abcd       "      4     "       "            'e'       ait un niveau d'indentation de 8
                                                             4 ne serait pas possible car il y a déjà
                                                             'abcd' + le tab = 5 caractères qui précèdent

Modifier l'alignement de colonnes de texte utilisant des tabs s'avère souvent pénible car il est difficile
de prévoir le résultat de l'insertion / suppression d'un tab au milieu d'une ligne.
Raison pour laquelle on ne devrait jamais aligner du texte avec des tabs.
De toute façon, les tabs n'ont pas été pensés pour l'alignement. Ex:
                                                                        var x = 10,
                                                                            y = 0;

La 2e ligne ne peut être alignée qu'à condition que &ts = 4. Pour toute autre valeur, on perd l'alignement.


    =

            auto-indentation de la sélection visuelle

                                               NOTE:

            Les commandes = et == appellent par ordre de priorité:

                  1. le pgm externe défini par l'option locale au buffer 'equalprg' / 'ep'

                  2. la fonction custom définie par l'option locale au buffer 'indentexpr' / 'inde'

                  3. une fonction de formatage interne dont le comportement peut être modifié via certaines
                     options, qui sont (par ordre croissant de priorité):

                                'autoindent'     copie l'indentation de la ligne précédente

                                'smartindent'    comme 'ai' mais reconnaît en plus certains éléments
                                                 de syntaxe C pour ajuster l'indentation qd il faut

                                'cindent'        comme 'si' mais plus intelligent, et peut s'adapter
                                                 à différents styles d'indentations

                     Elles sont toutes de type booléen et locales au buffer.
                     Elles sont décrites dans :h C-indenting

                     Si 'cindent' est activée, on peut configurer le style d'indentation via 3 options
                     locales au buffer supplémentaires:

                                'cinkeys'        touches qui provoquent une réindentation qd on appuie
                                                 sur elles en mode insertion
                                                 :h cinkeys-format

                                'cinoptions'     style d'indentation
                                                 :h cinoptions-values

                                'cinwords'       liste de mots-clés ajoutant un niveau d'indentation
                                                 sur la ligne suivante


            L'ordre de priorité 'equalprg' > 'indentexpr' diffère par rapport à l'opérateur gq:

                    'formatexpr' > 'formatprg'

            Vim peuple automatiquement la variable v:lnum (adresse de la ligne à indenter) qu'on peut
            utiliser dans la fonction custom définie par 'inde'.
            Celle-ci doit retourner le niveau d'indentation de la ligne v:lnum, ou -1 s'il ne doit pas
            changer (copier le niveau de la ligne précédente).
            Pour écrire une telle fonction, certaines fonctions systèmes peuvent s'avérer utiles:

                    - indent()
                    - prevnonblank()
                    - searchpair()    ou    searchpairpos()

            Si 'indentexpr' est non-vide, les touches qui provoquent une réindentation en mode insertion
            sont définies par l'option locale au buffer 'indentkeys' / 'indk' dont la valeur suit le format
            décrit dans :h indentkeys-format (même tag que cinkeys-format, et même format que pour 'cinkeys').

    5==

            auto-indenter la ligne courante et les 4 qui suivent


    =iB

            auto-indenter les lignes au sein du bloc de code courant ({…})

    0 C-d

            en mode insertion, supprime tous les niveaux d'indentation au début de la ligne

    C-f

            autoindenter (en mode insertion) en utilisant la fonction définie par 'indentexpr'

                                               NOTE:

            Par défaut, fonctionne depuis n'importe où sur la ligne, mais chez nous ne fonctionne
            que si on est à la fin de la ligne, car on a rebind C-f pour avancer d'un caractère.

            Ne fonctionne que si l'option locale au buffer 'indentexpr' / 'inde' est non vide.
            Donc, ne fonctionne pas par défaut dans un fichier markdown, ni dans un fichier d'aide.

    vip 3>

            augmenter l'indentation des lignes du paragraphe de 3 niveaux

            Qd un opérateur est appelé depuis le mode visuel, on peut le préfixer d'un count.

    :1,42<    :5,10>

            désindente les lignes 1 à 42
            indente les lignes 5 à 10

    :retab 8

            Si 'et' est désactivée, remplace toutes les séquences de whitespace contenant au moins
            un tab, par une séquence de tabs de largeur 8, la nouvelle séquence occupant un même nb
            de cellules que l'ancienne.
            Pex, :retab 8 remplace 2 tabs occupant chacun 4 cellules, en un seul tab occupant 8 cellules.

            Si on ne passe pas d'argument numérique à :retab, elle utilise &ts à la place.
            Autrement, elle change 'ts', avant d'utiliser la nouvelle valeur &ts.

            Si on ajoute un bang à :retab, il remplace aussi les séquences de whitespace ne contenant
            pas de tabs, que des espaces.

            Si 'et' est activée, :retab remplace les tabs en un nb approprié d'espaces.

## Rechercher

    tab    S-tab

            Naviguer entre les  différents textes matchés au milieu d'une  recherche avant d'avoir
            validé avec Enter.


    /~

            Cherche la chaîne de remplacement utilisée dans la dernière substitution.

            Si elle utilisait des métacaractères (backref &, \0, \1..9), ils ne sont pas développés
            mais interprétés littéralement.


    *    #

            Peuple le  registre recherche avec le  mot sous le curseur  (ou le +
            proche sur la  ligne), encadrés par les ancres \<  et \>, et déplace
            le  curseur  sur le  1er  caractère  de  la prochaine  /  précédente
            occurrence

                                               NOTE:

            - Accepte un count (3* cherche la 3e occurrence du mot sous le curseur)

            - Le registre recherche est peuplé par ordre de priorité avec:

                    1. le mot ('isk') sous le curseur
                    2. le prochain mot après le curseur

                    … et s'il n'y pas de mots sur la ligne:

                    3. la séquence de caractères non whitespace sous le curseur
                    4. la prochaine séquence de caractères non whitespace après le curseur

            - Le déplacement ajoute la position initiale dans la jumplist.

              S'il n'y a qu'une seule occurrence  et que le curseur se trouve au
              milieu du mot, il est automatiquement déplacé sur le 1er caractère
              du mot.

              Même  ce  déplacement de  seulement  qques  caractères ajoute  une
              entrée dans la jumplist.


    g*    g#

            idem mais cette fois sans les ancres \< et \>

            La recherche (unbounded) est donc plus large; équivaut à taper /foo ou ?foo


    Déplace le curseur sur le 1er caractère de la 3e prochaine occurrence de:

    ┌───────┬──────────────────────┐
    │ 3n    │ registre recherche   │
    ├───────┼──────────────────────┤
    │ 3*    │ mot sous le curseur  │
    ├───────┼──────────────────────┤
    │ 3/foo │ foo                  │
    ├───────┼──────────────────────┤
    │ 3?bar │ bar (vers l'arrière) │
    └───────┴──────────────────────┘

            Toutes ces commandes peuplent le registre recherche sauf `n`.


    :1,5print
    :1,5number
    :1,5#

            Affiche les lignes 1 à 5.

            `:number` et `:#` préfixent chaque ligne par son adresse.

            Attention, comme  beaucoup de commandes  EX, le comportement  de ces
            commandes  est  faussé  lorsque  le buffer  contient  des  plis  non
            ouverts.

            Ainsi, dans les exemples précédents, si les lignes 1 à 5 font partie
            d'un pli non ouvert, les  commandes afficheront TOUTES les lignes du
            pli.

            Pour elles, un pli non ouvert est traité comme une seule ligne.


      |g{motion}
    v_|g

            Recherche le texte couvert par  {motion} récursivement dans tous les
            fichiers du cwd. Fonctionne aussi en mode visuel.


    :g/
    :g//#

            Afficher toutes les lignes contenant le registre recherche, sans/avec le n° des lignes.


                                               NOTE:

            `:g` utilise, en l'absence de:

                    pattern  →  le contenu du registre recherche
                    action   →  la commande `:print`


     Afficher certaines lignes contenant le mot sous le curseur, au sein du fichier courant
     et au sein des fichiers include:

     ┌─────────────┬──────────────────────────────────────────────┬────────────────┐
     │ cmd normale │ description                                  │ cmd Ex voisine │
     ├─────────────┼──────────────────────────────────────────────┼────────────────┤
     │   [i        │ la 1e ligne                                  │ :is            │
     │ 3 [i        │ la 3e ligne                                  │ :is! 3         │
     ├─────────────┼──────────────────────────────────────────────┼────────────────┤
     │   ]i        │ la prochaine ligne                           │ :+,$is         │
     │ 3 ]i        │ la 3e prochaine ligne                        │ :+,$is! 3      │
     ├─────────────┼──────────────────────────────────────────────┼────────────────┤
     │   [I        │ toutes les lignes depuis le début du fichier │ :il!           │
     │   ]I        │                          la prochaine ligne  │ :+,$il!        │
     └─────────────┴──────────────────────────────────────────────┴────────────────┘


                                               NOTE:

            Toutes ces commandes:

                    - ajoutent les ancres `\<` et `\>`

                    - incluent les lignes commentées dans leur recherche ssi on leur passe un count:

                            [i      ignore     les lignes commentées
                          1 [i    n'ignore pas "

                      Exception:

                            [I      cherchent dans les lignes commentées malgré l'absence de count
                            ]I

                    - cherchent bien la Ne ligne contenant le mot sous le curseur, pas sa Ne occurrence

                            Pex, si on tape `3 [i`, dans le fichier:

                                    foo     one
                                    foo foo two
                                    foo     three

                            … Vim affichera:

                                    foo     three

                            Et non pas:

                                    foo foo two


                                               NOTE:

            S'il y a des des fichiers  include, ils sont traités dans l'ordre où
            ils apparaissent.

            IOW, si  on est dans  le fichier A et  qu'au milieu il  contient une
            directive  include faisant  référence à  un fichier  B, `[i`  et ses
            amies cherche  depuis le  début de A  jusqu'à la  directive include,
            puis elle cherche  dans B, enfin depuis la directive  jusqu'à la fin
            de A.


                                               NOTE:

            [I et ]I sont des commandes de recherche très utiles pour 2 raisons:

                    1. comparer tous les matchs en un coup d'oeil

                    2. se déplacer à un autre endroit du buffer, sans perdre le contexte courant

                       Une recherche classique via  slash pourrait beaucoup nous
                       éloigner de notre position courante;  qd ça se produit on
                       se sent perdu et perturbe la concentration.

                       Slash est  plus adapté  lorsque le pattern  recherché est
                       affiché dans l'écran courant.


     Sauter vers la 1e / 3e ligne contenant le mot sous le curseur, en cherchant
     au sein du fichier courant et de ses fichiers include:

     ┌─────────────┬──────────────────────────────────────────────────┬────────────────┐
     │ cmd normale │ description                                      │ cmd Ex voisine │
     ├─────────────┼──────────────────────────────────────────────────┼────────────────┤
     │   [ C-i     │ la recherche commence depuis le début du fichier │ :ij            │
     │ 3 [ C-i     │                                                  │ :ij! 3         │
     ├─────────────┼──────────────────────────────────────────────────┼────────────────┤
     │   ] C-i     │ la recherche commence après la ligne courante    │ :+,$ij         │
     │ 3 ] C-i     │                                                  │ :+,$ij! 3      │
     ├─────────────┼──────────────────────────────────────────────────┼────────────────┤
     │   C-w i     │ ouvre une fenêtre,                               │ :isp           │
     │ 3 C-w i     │ puis cherche depuis le début du fichier          │ :isp! 3        │
     └─────────────┴──────────────────────────────────────────────────┴────────────────┘

                                               NOTE:

            `] C-i` remplace  avantageusement `* n` qd on cherche  à se rendre à
            la prochaine occurrence  du mot sous le curseur, car  elle ne change
            pas le contenu du registre /.

            Si la prochaine occurrence peut  se trouver sur une ligne commentée,
            utiliser un count:

                    1 ] C-i


                    ┌ le pattern doit être unbounded
                    │ mnémotechnique: les slashs brisent les ancres
                    │
                    │ permet aussi de faire suivre `:isp` d'une autre commande Ex, après un pipe;
                    │ sans les slashs, `|other_cmd` serait interprété comme faisant partie du pattern
                    ├───┐
    :5,10isearch! 3 /pat/
                │
                └ cherche aussi dans les lignes commentées

    :5,10ilist!     /pat/

            Affiche LA 3e / LES ligne(s), entre les lignes 5 et 10, contenant pattern.

            Affiche aussi le n° de chaque match (contrairement à :g//#).


                                               NOTE:

            Si on passe une rangée à :is (ou :il), comment s'applique-t-elle aux
            directives include ?

            Vim traverse le  fichier courant et les fichiers include  de la même
            façon qu'avec `[i` est ses amies, à savoir dans l'ordre exact où ils
            apparaissent.

            De  plus, pour  `:is`, l'ensemble  des lignes  d'un fichier  include
            compte pour 1.

            La ligne  de la  directive include  dans le  fichier courant  est la
            seule affectée par la rangée.

            La rangée ne s'applique pas au  contenu d'un fichier include, mais à
            sa directive.


    :5,10ijump!    3  /pat/
    :5,10isplit!   3  /pat/
    :5,10psearch!  3  /pat/

            Cherche `pattern` au sein des lignes 5 à 10 du fichier courant et des fichiers include puis:

                    - saute   vers la 3e ligne où il y a match, dans la fenêtre courante
                    - "                                       , dans un split
                    - affiche      "                          , dans la fenêtre preview

                                               NOTE:

            `:psearch` est utile dans un fichier n'ayant pas de fichier de tags.


                                               NOTE:

            `:ij` et  `:isp` offrent plus  de flexibilité que leurs  cousines
            `[C-i` et `C-w i`, car elles permettent de:

                    - limiter la recherche à une rangée

                    - inclure ou exclure les commentaires de la recherche, via le bang,
                      indépendamment du fait qu'on leur ait passé un count ou pas

                    - réaliser une recherche unbounded (en mettant des slashs autour du pattern)

---

Document  that  Vim  adds  anchors  around a  non-delimited  pattern  passed  to
`:isearch` & similar commands, but only for those commands.

It does not do that for `:vim` for example.
See `:h include-search` and `:h :search-args`.

## Remplacer

    3rx

            Remplacer les 3 prochains caractères par le caractère x.


    5r C-e
    5r C-y

            Remplacer les  5 prochains  caractères par les  5 caractères situés  sur la  ligne du
            dessous / dessus (même colonnes).


    R C-r 0

            Remplacer les prochains caractères par le contenu du registre copie.

            En mode remplacement, on peut coller n'importe quel registre.
            Ne fonctionne pas qd on remplace un seul caractère (r):

                    r C-r 0    remplace le caractère sous le curseur par ^R
                               puis positionne le curseur au début de la ligne

    r C-k =e

            Remplace le caractère sous le curseur par le symbole euro (€) en tapant son digraphe (=e).
            Fonctionne aussi en mode remplacement avec R.


    R {char} … BS

            Qd on passe en mode remplacement via R, et qu'on change des caractères ({char}…),
            on peut à tout moment révéler à nouveau les derniers caractères remplacés via BS (backspace).

            Cependant, il s'agit bien d'une nouvelle édition (pas un undo).


    gR

            passe en mode remplacement virtuel

                                               NOTE:

            Dans ce  mode, au lieu  de remplacer  des caractères du  fichier, on
            remplace des cellules,  de sorte que l'affichage  des caractères qui
            suivent ne soit pas modifié.
            Ils n'ont pas l'air de bouger.

            On peut voir une différence par rapport au mode remplacement (R), qd
            on remplace un caractère par un:

                - tab     gR peut remplacer plusieurs caractères (au lieu d'un seul en mode remplacement);
                          Il en remplace autant qu'il occuperait de cellules si on en insérait un.

                          De même, qd on remplace un tab par un autre caractère, ce dernier ne remplace
                          pas le tab si ce dernier occupe plusieurs cellules.
                          En effet, dans ce cas, le caractère est bien inséré mais le tab reste.
                          En revanche, il occupe une cellule de moins.

                          Un BS révèle le(s) caractère(s) remplacé(s).

                - CR      tous les caractères qui suivent sur la ligne sont supprimés,
                          et le curseur passe sur le 1er non whitespace de la ligne suivante

                          Plusieurs BS révèlent le(s) caractère(s) remplacé(s).

                - C-t     Le niveau d'indentation de la ligne augmente comme d'habitude,
                          mais les caractères suivants ne semblent pas bouger.

                          C-d révèle les caractères remplacés.

                - C-d     Le niveau d'indentation de la ligne diminue comme d'habitude,
                          mais les caractères suivants ne semblent pas bouger.
                          Pour ce faire Vim double les caractères précédant le curseur.

                          C-t révèle les caractères remplacés.

            gr fait passer en mode remplacement virtuel uniquement pour le prochain caractère tapé.

            D'après :h vreplace-mode, ce mode est utile pour entrer de nouvelles données dans un tableau
            sans perturber l'alignement.


    yiw {motion} ciw C-r 0 Esc [{motion} . …]

            Remplacer un mot (pex 'bar') par un autre copié précédemment (pex 'foo').
            [optionnellement, répéter la substitution avec dot .]

            {motion} est le mvt nécessaire pour passer de 'foo' à 'bar'.


    yiw {motion} viw p    [{motion} viw "0p …]

            Remplacer un mot (pex 'bar') par un autre copié précédemment (pex 'foo')
            [optionnellement répéter la substitution autant de fois qu'on veut].

            Pk doit-on préfixer p par "0 qd on veut répéter la substitution?
            Car au moment où on remplace le 1er mot sélectionné, celui-ci est supprimé et part dans le registre -.
            Du coup le registre unnamed pointe désormais vers "- et non plus vers "0.
            Qd on collera ensuite, si on ne précise pas "0, c'est "- qui sera utilisé.


    yiw {motion} viw p # viw p

            Échanger de place 2 mots.

            yiw         copie le mot 'foo'                          @0 et @" = 'foo'
            {motion}    amène au mot 'bar'
            viw         sélectionne 'bar'
            p           colle 'foo'                                 @0 = 'foo'    @- et @" = 'bar'
                                                                    car 'bar' est supprimé
            #           amène à la précédente occurrence de 'foo'
            viw         sélectionne le 1er 'foo'
            p           colle 'bar'                                 car @" = 'bar'

## Sélectionner

:h visual-repeat

Qd on sélectionne du  texte puis qu'on agit dessus avec un opérateur,  la commande dot se souvient
non seulement de  l'opérateur mais aussi des dimensions  (nb lignes x nb colonnes) du  texte. Qd on
appuiera sur dot, depuis la position courante du curseur, elle sélectionnera la zone de texte ayant
les même dimensions, puis appellera le même opérateur.

Qd un opérateur est appelé depuis le mode visuel, dot ne mémorise pas d'objets, ni de mouvements.
Pex, si on sélectionne un paragraphe de 5 lignes (V}) et qu'on appuie sur > pour l'indenter, dot ne
mémorise pas une indentation  de paragraphe, mais une indentation de 5 lignes.  Donc, si ensuite on
se  déplace au  milieu d'un  autre paragraphe,  dot  ne l'indentera  pas, elle  indentera la  ligne
courante et les 4 suivantes.

De la même façon, si  on sélectionne un mot (viw) de 10 caractères et  qu'on le supprime, dot ne
mémorise pas une suppression de mot, mais une suppression de 10 caractères. Donc, si ensuite on se
déplace au  milieu d'un autre  mot, dot ne  le supprimera pas,  elle supprimera les  10 caractères
suivants.

Pour cette raison, il est préférable d'utiliser un opérateur depuis le mode normal que visuel.
Car _depuis le mode visuel, dot perd de l'information_ (ip → 5 lignes).

---

Qd on répète un objet via un count, qu'ajoute-t-on ?
Il semble que ça dépende des limites de l'objet:

            - caractères non connus à l'avance                  →    prochain objet              ex: d2aw
            - une paire de (groupe de) caractères différents    →    objet incluant              ex: y2ab
            - une paire de caractères identiques                →    n'ajoute rien (sauf pour l'opérateur visuel)

La répétition en  mode visuel d'un objet  dont les limites sont des  caractères identiques semble
complexe.  Il y a plusieurs choses étranges avec ce genre d'objets:

        - vi'        si le curseur ne se trouve pas entre 2 quotes, sélectionne le prochain texte sur
                     la ligne entre quotes;
                     mais si le curseur ne se trouve pas entre 2 parenthèses, vib ne sélectionne rien

        - vi'i'i'    ne sélectionne pas le même texte que v3i'

        - v4i'       ne sélectionne rien de plus que v3i'
                     mais v4a' peut sélectionner plus de texte que v3a'

                     Il semble qu'on puisse utiliser un count aussi grand qu'on veut avec l'adverbe a,
                     mais seulement jusqu'à 3 avec i.


    g C-v

            le dernier texte édité (mapping custom)


    3v

            sélectionne le caractère sous le curseur et les 2 suivants

---

Dans toutes les  commandes qui suivent l'opérateur v pourrait  être remplacé par
c, d ou y pour agir sur le texte sélectionné.

De plus,  si on remplace v  par V, quels  que soient les objets,  on sélectionne
tjrs des lignes entières.
Pex, V{backtick}a sélectionne tout le texte  situé entre la ligne courante et la
ligne de la marque a (les 2 lignes incluses).


    v%

            depuis le curseur jusqu'au prochain symbole ouvrant / fermant

                                               NOTE:

            généralement, si on est en A la sélection va jusqu'à B:

                A = intérieur des symboles              →    B = symbole ouvrant
                A = extérieur des symboles, et avant    →    B = symbole fermant

            Utile pour sélectionner tout une fonction en ayant le curseur sur function ou endfu (V%).

    vi% va%

            le texte situé entre les prochains (), [], {}    (objets custom)

            targets.vim serait sans doute meilleur, car il crée des objets distincts pour ces 3 symboles,
            qui en + acceptent un count.


    va`    va'    va"

            Le (prochain) texte encadré par des backticks / apostrophes / guillemets,
            symboles entourants inclus.

            S'il n'y a pas d'espaces autour de l'objet encadré, seuls les caractères entourants
            sont inclus en plus de l'objet.

            S'il y a un espace avant mais pas après, l'espace d'avant est inclus en plus de l'objet.

            S'il y a un espace après, seul l'espace d'après est inclus (qu'il y ait un espace avant ou non).


    va<  va>      va[  va]      vab      vaB

            le (prochain) texte encadré par des <>, [], (), {}
            seuls les caractères entourants sont inclus en plus de l'objet encadré,
            peu importe qu'il y ait des espaces autours ou non

            On peut aussi utiliser va(, va) à la place de vab, ainsi que va{, va} à la place de vaB
            mais ces derniers peuvent introduire une certaine confusion, car les caractères () et {}
            ont un sens différents lorsqu'ils ne sont pas précédés d'un “adverbe“ i ou a:

                    début / fin de phrase, début / fin de paragraphe

            mnémotechnique: b = (block of code)    B = {Block of code}



    ―――――――――――――――――――    v2ab
     ―――――――――――――――――     v2ib

    (baz (bar) ("f|oo"))   La position du curseur est représentée par le pipe, et on veut sélectionner
                           différents groupes de caractères.

                 ―――       vi"
                ―――――      va" ou vib
               ―――――――     vab


                           Pk tape-t-on v2ab et non pas va2b ? 'ab' est un objet (:h v_ab), le compteur
                           ne peut pas le casser, il doit donc le précéder.
                           Idem pour 'aB', 'ib', 'iB', 'a[', 'a]', 'i[', 'i]', … ce sont tous des objets
                           (donc incassables).

    ―――――――――――――――――――    v2a[
     ―――――――――――――――――     v2i[

    [baz [bar] [`f|oo`]]

                 ―――       vi`
                ―――――      va` ou vi[
               ―――――――     va[

    C-v /foo

            rectangle de texte dont le curseur et le f du prochain pattern foo sont des coins opposés

    v3/foo/e+1

            du curseur jusqu'au caractère suivant la fin de la 3e prochaine occurrence de foo

    viw/C-r C-w

            du mot sous le curseur jusqu'à sa prochaine occurrence

            On pourrait aussi utiliser * (viw*), mais on l'a déjà remap à une fonction
            custom pour rechercher la sélection visuelle vers l'avant.

    viw?C-r C-w n

            du mot sous le curseur jusqu'à sa précédente occurrence

            On pourrait aussi utiliser # (viw#), mais on l'a déjà remap à une fonction
            custom pour rechercher la sélection visuelle vers l'arrière.

            Le n est nécessaire pour répéter la recherche car la 1e recherche trouve le mot sous
            le curseur et la sélection ne change pas.

    v'a

            du curseur (inclus) jusqu'au 1er caractère non whitespace de la ligne sur laquelle
            se trouve la marque a (inclus aussi)

            Les opérateurs c, d et y incluent toute la ligne sur laquelle se trouve le curseur
            et toute la ligne sur laquelle se trouve la marque a.
            Pk? Car généralement, un mouvement qui déplace le curseur entre plusieurs lignes
            est considéré par un opérateur comme linewise (:h linewise).
            Y'a des exceptions…
            Ex:    d'a supprime les lignes entre la courante et celle portant la marque a (normal)
                   d`a supprime depuis le caractère courant jusqu'à celui portant la marque a (exception)

    v`a

            du curseur jusqu'au caractère de la marque a

    vap

            le paragraphe courant (texte situé entre 2 lignes vides) en incluant une ligne vide

            Si le paragraphe est précédé mais pas suivi d'une ligne vide (paragraphe de fin),
            la ligne vide qui précède est incluse.
            Si le paragraphe est suivi d'une ligne vide (peu importe qu'une ligne vide précède ou non),
            cette dernière est incluse.

    v2ap

            les 2 prochains paragraphes
            “l'adverbe“ a est plus intéressant que i dans ce cas, car i considère chaque ligne vide
            suivant un paragraphe comme un paragraphe distinct

    vip C-v o $

            sélectionner le paragraphe courant en mode visuel par bloc

    vis    vas

            La phrase courante en excluant (vis) ou incluant (vas) un whitespace si la phrase est précédée
            mais pas suivie d'un whitespace (phrase de fin), le whitespace précédant est inclus.

            Vim considère une phrase comme le texte situé entre un whitespace et un point.

            Si la phrase est suivie d'un whitespace (peu importe qu'un whitespace précède ou non),
            le whitespace suivant est inclus.

    vit    vat

            le texte entre 2 balises (tags) en excluant / incluant les balises
            le curseur doit se trouver sur les balises ou sur le texte entre elles

            seuls les caractères entourants sont inclus en plus de l'objet encadré,
            peu importe qu'il y ait des espaces autours ou non

    gn    gN

            la prochaine / précédente occurrence du registre recherche

            Il ne s'agit pas d'un objet (onoremap), mais d'un opérateur (v) + un objet (next/previous match).
            Toutefois, on peut l'utiliser comme un objet, de la même façon que pour changer le mot
            sous le curseur, on peut taper:    cviw

                                               NOTE:

            iw est un objet qu'on pourrait considérer comme un mouvement characterwise inclusif.
            Qd on le fait précéder d'un opérateur, il inclut les caractères de début et de fin du mot.
            Toutefois, qd on intercale v entre un opérateur et un mouvement characterwise inclusif,
            il devient exclusif. Raison pour laquelle cviw ne change pas la dernière lettre du mot.

            On peut aussi considérer gn et gN comme des mappings systèmes.
            Si le curseur se trouve:

                - en-dehors d'un match:                   v//e<cr>o//<cr>    ⇔    gn
                                                          v??<cr>o??e<cr>    ⇔    gN

                - sur le 1er caractère d'un match:        v//e<cr>
                - sur le dernier caractère d'un match:    v??<cr>
                - au milieu d'un match:                   v//e<cr>o??<cr>

            Comment tester si le curseur est à l'intérieur d'un match ou à l'extérieur ?
            Si la prochaine fin de match se situe avant le prochain début de match, on est à l'extérieur.
            Autrement, on est à l'intérieur:

                let next_begin = searchpos(@/, 'n')
                let next_end   = searchpos(@/, 'cne')

                fu IsBefore(pos1, pos2)
                    return a:pos1[0] < a:pos2[0] || (a:pos1[0] == a:pos2[0] && a:pos1[1] < a:pos2[1])
                endfu

                if IsBefore(next_begin, next_end)
                    …

    3gn

            la 3e prochaine occurrence du registre recherche

    v//

            du curseur jusqu'au début de la prochaine occurrence du registre recherche

                                               NOTE:

            Si v est remplacé par un opérateur (c, d, y), l'opération est exclusive:
            elle n'affecte pas le 1er caractère du pattern.
            Il en va de même si on ajoute un offset après //.

            Exception: l'offset e (end) rend une opération inclusive car le dernier caractère du pattern
            est bien affecté.  Ex:
            c//e coupe depuis le curseur jusqu'au dernier caractère, inclus, de la prochaine occurrence
            du registre recherche.
            Logique qd on y pense, on veut rarement affecter le début d'un texte et presque toujours
            inclure la fin d'un texte.

    v//e

            du curseur jusqu'à la fin de la prochaine occurrence du registre recherche

    v//e+5

            du curseur jusqu'au 5e caractère suivant le dernier caractère de la prochaine occurrence
            du registre recherche

    v//s-3

            du curseur jusqu'au 3e caractère précédant le 1er caractère de la prochaine occurrence
            du registre recherche

            // est synonyme de //s

    v//+2

            du curseur jusqu'au 1er caractère de la 2e ligne suivant celle où se trouve la prochaine
            occurrence du registre recherche

                                               NOTE:

            Lorsque le mouvement // est suivi d'un offset purement numérique (+-5 pex),
            si on remplace v par un opérateur l'opération devient linewise:
            Elle affecte des lignes entières en incluant celle où se trouve le curseur et la (5e)
            suivant/précédant celle où se trouve la prochaine occurrence du registre recherche.

    v(    v)

            du curseur jusqu'au début / à la fin de la phrase
            et pas jusqu'à la prochaine parenthèse, comme dans va(, va) ou vi(, vi)

    v{    v}

            du curseur jusqu'au début / à la fin du paragraphe
            et pas jusqu'à la prochaine accolade, comme dans va{, va} ou vi(, vi)

    v5}

            depuis le curseur jusqu'à la fin du 4e paragraphe suivant le paragraphe courant

    v3k

            depuis le curseur (inclus) jusqu'au caractère situé sur la même colonne 3 lignes
            au-dessus (inclus aussi)
            v est characterwise mais c, d, y sont linewise dans ce cas (c3k, d3k, y3k incluent des lignes entières)

    v2tx

            jusqu'à la 2e occurrence du caractère x

            Pk écrit-on 2tx et non pas t2x ?
            Parce que t (tout comme f, F, T) est une fonction système qui attend en argument un caractère.
            Si on la fait suivre du caractère 2, elle va déplacer le curseur juste avant le prochain 2.
            tx est un objet, il faut respect la syntaxe:    opérateur + count + objet

## Supprimer

    3D

            supprimer la ligne courante et les 2 suivantes
            Un peu plus rapide que `3dd`, d'autant qu'on a déjà un doigt sur shift pour taper un nb.

            On remarque que `D` se comporte différemment suivant qu'il est précédé d'un nb ou non.
            Précédé d'un nb, il supprime les newlines à la fin de chaque ligne.
            Sans nb, il conserve le newline à la fin de la ligne courante.

    dvip

            Réduire toutes les lignes vides entre 2 lignes de texte, en une seule ligne vide.


                                               NOTE:

            Comment ça marche ?
            Si le curseur se trouve sur une ligne vide au sein d'un ensemble:

                    - `vip` ne sélectionne rien
                    - `yip`, `dip`, `cip`, … opère sur toutes les lignes vides

            Donc, ici, `dip` supprimerait toutes les lignes vides.
            Mais l'opérateur `d` a été modifié par `v`, et comme `ip` est un objet linewise,
            il est rendu exclusif (:h o_v):

                    If the motion was linewise, it will become exclusive.

            Ceci explique pourquoi il reste une ligne vide. C'est la dernière, qui a été exclue.


    :g/foo/v/bar/d_

            Supprime toutes les lignes contenant foo mais pas bar.

            Il s'agit d'un cas particulier de composition de commandes globales.
            Pour chaque ligne contenant `foo`, Vim exécute `:v`, en lui passant pour rangée la ligne courante.
            Il n'y a donc pas vraiment de récursion, et il est interdit (E147) de donner une rangée
            à `:v`.


    :g/^/+,+9d_
    :%norm! 9"_dd

            supprime les 9/10e du buffer

            Si on imagine que le buffer est divisé en blocs de 10 lignes, la 1e commande conserve
            les 1e lignes, la 2e les dernières lignes.

            :g agit sur des lignes marquées contrairement à :norm qui agit sur des adresses de lignes.

            :g et :norm passent de 1e ligne de bloc en 1e ligne de bloc.
            :g supprime toutes les lignes d'un bloc sauf la 1e (qui est exclue de la rangée +,+9).
            :norm supprime toutes les lignes sauf la dernière (pas affectée par un 9dd).

            La commande globale produit ici le résultat attendu, grâce au fait qu'elle n'agit pas
            sur / depuis des lignes marquées qui n'existent plus.
            Autrement toutes les lignes du buffer seraient supprimées (sauf la 1e?).

            Comment fonctionne la commande :norm ?
            Depuis la ligne 1, elle supprime 9 lignes. La dernière ligne du 1er bloc devient la ligne 1.
            Depuis la ligne 2, elle supprime 9 autres lignes. La dernière ligne du 2e bloc devient la ligne 2.
            Etc.

            À un moment donné, :norm est probablement appelée pour des (adresses de) lignes qui n'existent plus.
            En effet, si le buffer avait initialement 100 lignes, :norm devrait être appelée 100 fois.
            Les 10 premiers appels devraient supprimer 90 lignes.
            Puis les 90 derniers appels devraient se faire sur les lignes 11 à 100 qui n'existent plus.
            Et tout comme :g ignore un appel sur/depuis une ligne inexistante, :norm a l'air de
            s'en foutre (pas de message d'erreur).

            On n'est pas obligé de passer la rangée % à :norm:
            1,N suffit (N correspondant au nb de blocs dans le fichier). Mais % est + simple et rapide à taper.


    g/^/5s/\v^(.*$)\_.*\zs\n\1$/

            supprimer toutes les lignes du buffer identiques à la 5e (5e ligne exclue)

            La substitution:    5s/\v^(.*$)\_.*\zs\n\1$/
            … supprime la dernière ligne du buffer identique à la 5e.

            Il peut y avoir jusqu'à N-1 lignes identiques (N étant le nb de lignes du buffer).
            Il faut donc répéter la substitution au moins N-1 fois pour s'assurer de les avoir toutes supprimées.
            Pour ce faire, on utilise la commande globale :g/^/…


    g/\v^(.*)\_$\_.*\_^\1$/d_

            supprimer toute ligne présente en plusieurs exemplaires, sauf la dernière

                                               NOTE:

            Si on souhaite préserver la 1e plutôt que la dernière, il suffit de taper:    :g/^/m0
            … avant et après, pour inverser temporairement les lignes.

            Plus généralement, ceci inverse l'effet d'une transfo arbitraire:

                    g/^/m0 | transfo | g/^/m0

                                               NOTE:

            Ceci montre que lorsqu'on donne un pattern multi-lignes à :g, lorsqu'elle trouve
            un match, elle ne marque que la 1e ligne de ce dernier.
            Si c'était pas le cas, cette commande ne supprimerait pas juste les doublons, mais carrément
            toutes les lignes entre 2 doublons.

                                               NOTE:

            On pourrait remplacer l'un des atomes \_$ ou \_^ par \n, mais pas les 2.
            Avec 2 newlines, :g ne trouverait pas 2 lignes identiques consécutives, qui ne sont séparées
            que par 1 seul newline.
            Rappel:    \_$ et \_^ n'ajoutent pas de newline au pattern, elles disent simplement que
            le 1er et dernier caractère décrit par \_.* doivent être tous 2 des newlines.


    :setl noet
    i Tab Tab 2 Esc
    qq yyp >> C-a q
    538@q
    :g/\v^(\t{2,})\1+\d/d
    :%s/\t//g

            génère la liste des 100 premiers nb premiers (1 n'est pas premier)

            Toute l'astuce est dans l'avant-dernière ligne qui supprime les lignes contenant
            un nb de tab non premier.
            Pour ce faire, on les décrit à :g via le pattern:

                    \v^(\t{2,})\1+

            Qui peut être lu de la façon suivante:

                un groupe d'au moins 2 tabs (\t{2,}) répété une ou plusieurs fois (\1+)

            Pex, dans le cas de la ligne débutant par 35 tabs, \t{2,} matchera 7 tabs et \1+ les répètera 5 fois.

            Montre qu'on peut utiliser une backref au sein même d'un pattern passé à :s/:g,
            et pas seulement dans la chaîne de remplacement de :s.

            Montre aussi qu'une backref permet de simuler une multiplication ou division.

    gg                       :g/^/if search('begin', 'bnW') > search('.*end', 'bcnW') | d | endif
    :set nowrapscan
    :/begin/+1;/end/-1 d
    999@:

            Supprime toutes  les lignes à  l'intérieur des blocs  commençant par
            une ligne contenant 'begin' et  se terminant par une ligne contenant
            'end'.

            On pourrait remplacer :d par n'importe quelle commande Ex.
            Illustre comment agir sur des blocs de lignes bien déterminés/délimités.

            Dans la  1e solution, il est  important de séparer les  2 bornes par
            `;` et non `,`.
            En effet, on  cherche la ligne contenant 'end' après  la ligne où se
            trouve le prochain  'begin', et non pas après celle  où se trouve le
            curseur actuellement.

            La 2e solution s'appuie sur la logique suivante:
            si on est à l'extérieur d'un bloc, le prochain début de bloc se situe avant la prochaine fin de bloc
            si on est à l'intérieur, c'est l'inverse

            Pk le flag 'b' ? Sans 'b', on devrait exécuter qch comme:

                    g/^/if search('.*begin', 'cnW') > search('end', 'nW') | d | endif

            Pb:    ça fonctionnerait pour tous les blocs sauf le dernier.
            En effet, dans le dernier bloc,    search('.*begin', 'cnW')    retournerait 0,
            car on serait sur une ligne située après la dernière ligne 'begin'.
            Du coup la condition ne serait plus respectée.
            Il faudrait donc traiter ce cas particulier (peut-être en modifiant la condition).

            Pk le pb ne se pose pas avec 'b' ?
            Qch de similaire se produit avec 'b', mais ça ne pose aucun pb.
            Qd on est sur une ligne à l'intérieur du 1er bloc,    search('.*end', 'bcnW')    retourne 0.
            Mais cette fois, la condition reste vraie.

            Dans la logique précédente, si on remplace les termes prochain(e) par précédent(e),
            la logique reste valide. Donc l'ajout du flag 'b' ne pose pas de pb.

            Pk le .* dans la recherche de 'end' ?
            Parce que lorsque :g est sur une ligne contenant 'end', on veut que la recherche trouve
            la ligne courante. Or, :g positionne le curseur sur la 1e colonne de la ligne, et donc,
            si jamais du texte se trouve avant 'end' ('some text end'), search() ne trouvera pas 'end'
            sur la ligne courante mais sur une précédente.

            Dans la 2e solution, si on voulait inclure les lignes 'begin' et 'end', il faudrait ajouter
            le flag 'c' à la recherche de 'begin', et le retirer à la recherche de 'end'.


    /foo d C-v ``

            Supprime un rectangle  de texte dont le curseur et  le f du prochain
            pattern foo sont des coins opposés.
            Le saut  vers /foo  ajoute une  entrée dans  la jumplist  (marque ')
            correspondant à la position actuelle du curseur.
            On peut y retourner via ``.

    dvj

            Supprime depuis le curseur jusqu'au caractère de la même colonne sur la ligne suivante.

            Cette   commande    illustre   le   fait    qu'on   peut   contrôler    le   caractère
            characterwise/linewise/blockwise  d'un  mouvement  en   suffixant  l'opérateur  qui  le
            précède avec v/V/^V

            Ici, j est un  mouvement linewise, raison pour laquelle dj  supprime 2 lignes entières.
            Pourtant,  dvj supprime  depuis le  caractère  sous le  curseur  et non  depuis le  1er
            caractère de la ligne courante, car on a suffixé l'opérateur d avec v.


    d C-v `a

            supprime le rectangle dont le caractère sous le  curseur et celui sous la marque a sont
            des sommets opposés

    2x

            supprime le caractère sous le curseur et le suivant

    4X

            supprime les 4 caractères avant le curseur

    yib vab p

            supprime les parenthèses autour du texte où se trouve le curseur

                yib    copier l'intérieur
                vab    sélectionner tout
                p      remplacer le tout par l'intérieur

            On peut aussi utiliser l'opérateur ds fourni par le plugin vim-surround:    dsb

## Types de mouvements

L'opérateur de sélection visuelle v est intéressant par rapport aux opérateurs c, d, y, car il permet
de voir ce qu'on sélectionne avant d'agir dessus.  Toutefois, il présente 2 inconvénients:

   1. une touche de plus
   2. non répétable via dot

---

Un mouvement peut être:

   - characterwise s'il peut déplacer le curseur au sein d'une même ligne
   - linewise s'il déplace le curseur entre des lignes

Un texte copié, coupé ou supprimé via un mouvement linewise sera collé sous (p) / au-dessus de (P)
la ligne du curseur (car getregtype('"') = V).
S'il l'est via un mouvement characterwise, il sera collé après (p) / avant (P) le curseur (car getregtype('"') = v).
S'il l'est via un mouvement blockwise, il sera collé après / avant le bloc dont la frontière droite
est une colonne passant par le curseur (car getregtype('"') = ^V).

Remarques:

   - un mouvement qui déplace le curseur entre plusieurs lignes est généralement linewise (mais y'a des exceptions)

   - { et } (déplacements par paragraphes) sont characterwise.
     d} supprime depuis le caractère sous le curseur jusqu'à la fin du paragraphe.
     S'il était linewise, d} supprimerait depuis le 1er caractère de la ligne courante.

   - Un mouvement vers une marque précédée d'un backtick est characterwise.
     Un mouvement vers une marque précédée d'une apostrophe est linewise.

---

Un mouvement linewise est tjrs inclusif (précédé d'un opérateur, ce dernier affecte les lignes de
départ et d'arrivée).

Un mouvement characterwise peut être inclusif ou exclusif:

   - inclusif signifie que lorsqu'il est précédé d'un opérateur ce dernier agit sur le caractère
     de départ et d'arrivée

   - exclusif signifie que lorsqu'il est précédé d'un opérateur ce dernier n'agit pas sur le dernier
     caractère: celui le + proche de la fin du buffer;
     ça peut être le caractère de départ ou celui d'arrivée suivant le sens du mouvement

     Exemples de mouvements characterwise exclusifs:

       * F    cFx = coupe jusqu'au précédent caractère x mais pas le caractère sous le curseur
       * w    yw  = copie jusqu'au début du prochain mot mais ne copie pas le 1er caractère de ce dernier


On peut forcer  un mouvement à devenir characterwise, linewise  ou blockwise, le
temps d'une opération.
Pour ce faire, il suffit de suffixer l'opérateur avec v, V ou C-v.

Ex:

    dj         supprimer la ligne courante et celle qui suit
    dvj        supprimer depuis le curseur jusqu'au caractère de la même colonne sur la ligne suivante
    d C-v j    supprimer le caractère où se trouve le curseur et celui sur la même colonne sur la ligne suivante

Lorsqu'on suffixe  un opérateur  avec v,  alors que  l'opérateur est  suivi d'un
mouvement qui est déjà characterwise, ce  dernier passe d'inclusif à exclusif ou
d'exclusif à inclusif.
Pex, on peut transformer les mouvements exclusifs F et w en mouvements inclusifs
via les mapping:

    ono  F  vF
    ono  w  vw

---

F n'est pas un objet mais une commande qui attend en argument un caractère.
Le 1er  mapping ne crée pas  un nouvel objet, il  se contente d'ajouter v  qd on
tape F en mode operator-pending, afin de faire passer le mouvement characterwise
F{char} d'exclusif à inclusif.

#
# Listes De Fichiers / Navigation
## Buffer list
### Mouvements dans un buffer

    5H    5L

            5e ligne en partant du haut/bas de la fenêtre.


    gd    gD

            Tente de se déplacer à l'endroit où la variable sous le curseur est définie / déclarée.

            gd cherche une variable locale;     la recherche débute au début de la méthode / fonction ([[)
            gD "                    globale;    "                            du buffer


    gi

            déplace le curseur au dernier endroit où on a inséré du texte, et fait passer en mode insertion


    g'x    g`x

            Se rendre au début de la ligne de la marque x (quelle qu'elle soit) ou précisément sur
            la marque x sans ajouter la position de départ dans la jumplist.


    zh    zl
    zH    zL

            scroller horizontalement d'un caractère / demi-écran vers  la gauche / droite qd on se
            trouve sur une longue  ligne qui dépasse la largeur de l'écran  et que l'option 'wrap'
            est désactivée

    5fx

            se déplacer jusqu'à la 5e occurrence du caractère x

            opérateurs du même type que f : F, t, T
            Pk écrit-on 5fx et non pas f5x ? Parce que fx est un objet.
            Le nb se place dc naturellement devant lui et non au milieu, comme on écrit 5w pour désigner 5 mots.


    5_

            1er caractère non whitespace de la 4e ligne qui suit
            5^ déplacerait toujours le curseur au 1er caractère non whitespace de la ligne courante

    3$

            dernier caractère sur la 2e ligne qui suit

    3-    3+

            descendre / monter de 3 lignes en plaçant le curseur sur le 1er caractère non whitespace

    :25

            se rendre à la ligne 25; contrairement à 25G, la jumplist n'est pas modifiée


    :mark '    :norm! m'

            ajouter la ligne courante en dernière entrée dans la jumplist

            La 1e commande place la marque sur le 1er caractère non whitespace, la 2e sur le caractère
            sous le curseur.  :norm! m' semble donc meilleure.

            De manière plus générale :mark x posera toujours la marque x sur 1er caractère non whitespace,
            ce qui s'explique sans doute par le fait que Vim n'a pas connaissance de la position du curseur
            qd il exécute :mark car il est en mode Ex.
            En revanche, il sait où se trouve le curseur avec :norm car il exécute les commandes qui
            suivent en mode normal.

                                               NOTE:

            Qd on exécute une commande globale, il ne semble pas possible de modifier la marque ''.
            Pour cette raison, il ne vaut mieux pas l'utiliser dans un mapping.

            En effet, si on passe en mode Ex (gQ) et qu'on exécute la commande globale:

                    :g/BUG/vi

            … pour pouvoir nous rendre de ligne en ligne contenant le pattern BUG via gQ, et effectuer
            des éditions arbitraires autour de celles-ci, un mapping ayant besoin de modifier la marque '
            ne fonctionnera pas comme prévu.
            Pk?    Car il n'y parviendra pas: la marque est sans doute verrouillée sur la position qu'on avait
            juste avant d'exécuter :g/BUG/vi.

    :10km

            pose la marque m sur la ligne 10 (colonne 0)

            :k est une forme abrégée de :mark
            Elle est spéciale car contrairement à :mark, elle ne demande pas à être séparée de son argument
            par un espace:

                :km       ✔
                :markm    ✘


    _    g_

            début / fin du texte sur la ligne (exclut les whitespaces)

            Mouvements linewise qui acceptent également un count.
            Pex, `2_` déplace le curseur sur le 1er non whitespace de la ligne suivante.

            _ peut être utilisé après un opérateur pour agir sur la ligne courante, et les suivantes
            s'il est précédé d'un count.
            On peut donc le considérer comme l'objet “ligne“.  Ex:

                    d_     supprimer la ligne          dd est son synonyme

                    2c_    couper la ligne courante    2cc est son synonyme
                           et la suivante

                    gc_    (dé)commenter la ligne      gcgc (ou gcc) est son synonyme


    (    )

            précédente / prochaine phrase (1er caractère non whitespace après un point)

            Ajoute la position courante à la jumplist, même si le début/fin de la phrase est sur
            la même ligne que la ligne courante.
            On peut donc revenir là où on se trouvait avant d'appuyer sur ( ou ) via C-o.

    {    }

            précédent / prochain paragraphe (ligne vide)

            Comme pour ( et ), ajoute la position courante dans la jumplist.

    [[    ]]
    []    ][

            Précédent / prochain début de section.
            Précédent / prochain fin de section.

            La nature d'une section dépendant du type de fichier Pex une fonction vimscript.

            Mnémotechnique:
            Le 1er crochet indique la direction de déplacement.
            Si le 2e est identique au 1er, on se déplacer sur un début de section.
            Autrement sur une fin.


    [{    ]}
    [(    ])

            prochaine / précédente accolade / parenthèse non fermée

            Permet de se rendre au début ou à la fin d'un bloc de code.

            Très pratique, pex, qd le curseur est au milieu d'une imbrication de dictionnaires,
            et qu'on veut se rendre au début peu importe où le curseur se trouve.
            Du moment qu'il est à l'intérieur de l'imbrication, `[{` le placera au début du dico.


Quelques propriétés concernant une marque:

   - elle n'est supprimée que si on supprime sa ligne
   - elle est restaurée si on annule la suppression de sa ligne
   - sa coordonnée ligne peut changer si on supprime/ajoute des lignes avant elle
   - sa coordonnée colonne ne change pas, même si on ajoute/supprime du texte avant elle

On peut se rendre à une marque de 4 façons différentes, en la préfixant avec:

    - `    endroit exact
    - '    1er caractère non whitespace sur la ligne où se trouve la marque
    - g`   comme ` mais sans poser la marque ' sur la ligne courante avant le déplacement
    - g'   comme ' mais "


    10yy']    p`]

            Copier 10 lignes et se déplacer sur la dernière ligne copiée.
            Coller du texte et se rendre juste AVANT le dernier caractère collé.
            gp nous amène juste APRÈS le dernier caractère collé.

            Ceci montre que la marque ] est très utile après avoir opéré sur du texte.

    `(    `)

            1er / dernier caractère de la phrase courante

    `{    `}

            1er / dernier caractère du paragraphe courant

    ``

            1er caractère où on se trouvait avant le dernier saut
            permet d'alterner entre les 2 dernières entrées de la jumplist

                                               NOTE:

            Vim considère comme un saut, tout mouvement pour lequel on ne connaît pas à l'avance
            la distance entre le départ et l'arrivée. Ex:

                   5j        on connaît la distance dc Vim ne marque pas le départ

                   *         on ne connaît pas la distance dc Vim marque le départ
                   /foo/     "

                                               NOTE:

            Vim considère `` comme un saut.
            Donc `` a 2 effets:

                    - il nous ramène à l'endroit correspondant à la dernière entrée de la jumplist

                    - il ajoute la position de départ à la jumplist (là où se trouvait le curseur avant le saut)
                      L'endroit où on se trouve qd on appuie sur `` devient donc la nouvelle dernière
                      entrée de la jumplist.

    `.

            dernier caractère modifié

            N'importe quel opérateur: c, d, s … qui change une portion du texte modifie cette marque.
            Pex après l'insertion d'un mot avec ciw, la marque . se trouve sur le dernier caractère inséré.
            Utilisé par g;.

    `^

            caractère où se trouvait le curseur qd on a quitté le mode insertion pour la dernière fois
            Utilisé par gi.

    `"

            caractère où se trouvait le curseur qd on a quitté le buffer pour la dernière fois
            la marque n'est posée / mise à jour qu'après avoir fermé sa dernière fenêtre

    ['    ]'
    M-p   M-n

            ligne où se trouve la précédente / prochaine marque a-z

            ]` peut poser pb si la ligne est + courte que le n° de colonne de la prochaine marque.

            Ça peut se produire si la ligne a été modifiée après qu'on ait posé la marque.
            En effet, dans ce cas, Vim ne parvient pas à déplacer le curseur sur la colonne mémorisée
            par la marque.
            À chaque fois qu'on appuiera sur ]`, Vim “butera“ sur une ligne trop courte.

            Pour naviger de marque en marque, il vaut donc mieux utiliser:

                1.    ['    ]'    pour atteindre la ligne de la marque qui nous intéresse
                2.    ]`          "              la colonne "

### Navigation entre buffers

    ┌────────────────────┬────────────────────────────────────────────────────────────────────────────┐
    │ :b pat C-d         │ lister les buffers dont le nom matche pat                                  │
    ├────────────────────┼────────────────────────────────────────────────────────────────────────────┤
    │ :b *foo/**/*bar    │ afficher le buffer dont un des dossiers sur le chemin se finit par foo     │
    │                    │ et dont le nom du fichier se finit par bar                                 │
    ├────────────────────┼────────────────────────────────────────────────────────────────────────────┤
    │ 3 C-^              │ charger le buffer n° 3                                                     │
    └────────────────────┴────────────────────────────────────────────────────────────────────────────┘

### Commandes diverses

    g C-g
    :echo wordcount()

            afficher des infos sur le buffer courant, entre autres : nb de mots, caractères, octets
            on pourrait aussi passer par le shell : :!wc -{m,w,c} %

            wordcount() retourne la même information que g C-g mais sous la forme d'un dico.

    :bd foo bar

            décharger les buffers foo et bar; supporte la complétion


    :bd *.conf C-x C-a

            Décharge tous les buffers dont le nom contient `.conf`.


    :bd 5 10
    :5,10bd

            décharger les buffers 5 et 10
            décharger les buffers 5 à  10

    :1,10bufdo cmd

            exécute cmd sur tous buffers 1 à 10 de la buffer list

    :bufdo e!

            annuler toutes les modification apportées aux buffers de la buffer list
            depuis leur dernière sauvegarde


    :enew    :new    :vnew    :tabe

            éditer un nouveau buffer sans nom dans:

                    - la fenêtre courante
                    - un viewport horizontal
                    - "        vertical
                    - un nouvel onglet

            Pour le sauvegarder taper    :sav[eas] foo, ou taper les commandes précédentes en leur
            donnant comme nom de fichier foo (puis :w comme d'hab).


    :file /path/to/foo

            Définit /path/to/foo comme étant le nom du buffer courant.

            Ceci a pour effet de:

                - créer un nouveau buffer dont le contenu est le même que l'ancien
                - faire passer l'ancien buffer en buffer alternatif, non listé et non modifié
                  (sauf s'il n'avait pas de nom)

            Si on modifie le nouveau buffer et qu'on l'écrit, le contenu de l'ancien buffer
            est préservé (mais modifié).

            Si on recharge le nouveau buffer, on obtient au choix:

                - un buffer vide si son nom ne correspond à aucun fichier existant dans le dossier de travail
                - le buffer correspondant à un fichier s'ils ont le même nom

            Attention: bien vérifier que le nom qu'on choisit n'est pas déjà pris par un buffer existant.
            Autrement erreur. Pour ce faire:

                    if !bufexists('bufname') | silent file bufname | endif

                                               NOTE:

            Si on:

                    - définit une commande utilisant `:file`, dont le nom est composé exclusivement de majuscules
                    - tape toute ou partie de son nom en minuscules sur la ligne de commandes
                    - appuie sur Tab afin de développer et/ou faire passer son nom en maj avant de l'exécuter

            Ex:

                    com ABC vnew | file foobar

            … il se peut qu'on voit un message du genre:

                    "foobar" [Not edited] --No lines in buffer--

            Il faut alors appuyer sur une touche (CR, Esc, …) avant de pouvoir voir le résultat de la commande.
            Le pb ne se pose pas si on tape le nom de la commande explicitement, sans la développer via Tab.

            C'est pour cette raison qu'il vaut mieux prendre l'habitude de préfixer `:file` par un `:silent`.
            En effet, avec `:silent`, peu importe comment on tape le nom de la commande, on peut voir
            son résultat immédiatement.


    :ls!

            lister tous les buffers même ceux déchargés (:bd) et même ceux utilisés pour afficher l'aide

            taper :h ls pour comprendre les symboles placés devant les noms des fichiers
            Quelques-uns :

            u    unlisted buffer
                 le buffer ne sert pas à être édité mais pex à afficher un fichier d'aide,
                 ou alors il a été déchargé via :bd

            a    active buffer (chargé et affiché dans une fenêtre)
            h    hidden buffer (chargé mais non affiché)
            -    le buffer ne peut pas être modifié
            +    le buffer contient des modifications non enregistrées
            =    le buffer est read-only (fichier aide de Vim, ou fichier système ouvert
                 sans les droits roots)

    :write %.bak

            fait un backup du buffer courant (si le fichier d'origine s'appelle file,
            le backup s'appelle file.bak)
            contrairement à :saveas, :write ne change pas le buffer courant
            en fait il ne charge même pas de nouveau buffer, il écrit dans un fichier et c'est tout

    :'{,'}w !espeak

            Envoyer le paragraphe courant au programme espeak pour qu'il le lise à voix haute.
            Concrètement, :w écrit sur la sortie standard de espeak.

    :w !sudo tee '%'

            sauvegarder le buffer courant en élevant ses privilèges si on n'a pas les droits suffisants

            Concrètement, on écrit tout le buffer (sans préciser de rangée, :w prend par défaut
            tout le buffer), sur l'entrée standard du programme shell tee.
            Ce dernier echo son entrée sur sa sortie, qui par défaut est le terminal,
            mais ici est le fichier courant.
            En effet, % est développé en le nom du buffer courant avant que la commande ne soit
            envoyée au shell.

            On risque d'avoir un message d'avertissement nous disant que le fichier et le buffer ont changé.
            Taper L ([L]oad) pour charger le nouveau fichier (identique au buffer) dans le buffer courant.

    :5,7w!

            remplacer le fichier par les lignes 5 à 7 du buffer

            Le buffer reste entier, mais si on le recharge à partir du fichier (:e), seules les lignes 5 à 7
            sont restaurées.

            Le bang est nécessaire pour autoriser Vim à écrire un buffer partiel.


    :wqa[ll]    :xa[ll]

            idem + quitter Vim

                                               NOTE:

            :x et par extension :xa ne sauvegarde qu'un buffer modifié, contrairement à :w.

##
## Fichiers

Qd on  doit passer  un nom de  fichier en  argument à une  commande Ex,  on peut
utiliser un chemin relatif par rapport au dossier de travail.
Ce dernier peut être modifié via :cd ou :lcd.
Un dossier  de travail judicieux,  càd juste  au-dessus des fichiers  qu'on veut
éditer pendant la session, permet donc d'économiser des frappes au clavier.

---

    :bro[wse] {cmd}

            Ouvre l'explorateur de fichiers, attend qu'on choisisse un fichier, et exécute {cmd}
            en lui passant le fichier choisi en argument.

            Ça ne fonctionne que pour certaines commandes (dont certaines uniquement en GUI).
            Dans le terminal, les commandes suivantes fonctionnent:

                    :edit & friends (:tabedit)
                    :[v]split
                    :[s]view
                    :tabnew


Ouvre dirvish pour laisser l'utilisateur choisir un fichier:

    ┌────────────────────────┬──────────────────────────────────────────────────────────────────────────┐
    │ :browse e /path/to/dir │ dirvish affiche le contenu de `/path/to/dir`                             │
    │                        │ puis Vim charge le fichier choisi par l'utilisateur                      │
    ├────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ :browse e              │ dirvish affiche le contenu du répertoire courant                         │
    │                        │ puis Vim charge le fichier choisi                                        │
    │                        │                                                                          │
    │                        │ en théorie le dossier affiché par dirvish est déterminé par 'browsedir', │
    │                        │ mais cette option n'est censée fonctionner que pour Vim en GUI           │
    └────────────────────────┴──────────────────────────────────────────────────────────────────────────┘


    :drop /path/to/file

            Donne le focus à la fenêtre où `file` est affiché, si elle existe.
            Autrement, l'affiche dans la fenêtre courante.

            L'arglist est redéfinie:    [ '/path/to/file' ]


    :    drop  file1 file2
    :tab drop  file1 file2

            Idem, mais cette fois l'arglist est redéfinie comme étant:

                    [ 'file1', 'file2' ]

            La 1e commande affiche `file1`.
            La 2e commande affiche `file1` et `file2`, chacun dans un tab page dédié.


    :cd %:p:h

            Change le dossier de travail pour qu'il corresponde au dossier du fichier courant.

            %:p:h est développé en le chemin absolu vers le dossier du fichier courant.
            On peut le vérifier en tapant Tab avant d'exécuter la commande.
            Tab permet de forcer le développement de ce genre d'expression avant l'exécution
            de la ligne de commande.


                                               NOTE:

            Ça peut être utile qd on travaille sur un ensemble de fichiers présents dans un dossier
            différent du dossier de travail, car pour éditer un de ses fichiers on aura juste à taper:

                    :e {fname}

            … et non pas:

                    :e /long/path/to/{fname}

            Toutefois,  en  pratique, il  vaut  mieux  faire en  sorte  que  le dossier  de  travail
            corresponde  à  la  racine  du  projet. Puis,  d'utiliser  des  mappings  qui  taperont
            automatiquement le  chemin vers la  racine du projet ou  le dossier du  fichier courant.
            Cette  méthode présente  l'avantage de  s'adapter  à n'importe  quel sous-dossier  du
            projet, sans avoir à changer le dossier de travail.


                                               NOTE:

            On pourrait se contenter du modificateur :h:

                    cd %:h


    :e %:h Tab

            Peuple la ligne de commande avec la commande `:edit` suivi du chemin vers le dossier
            du fichier courant.


                                               NOTE:

            Je pense que `expand()` n'est nécessaire que lorsque l'expression à développer est complexe,
            ou qd on veut forcer un développement à avoir lieu tout de suite, dans le traitement
            d'une ligne de commande complexe (par défaut, je crois qu'il a lieu à la fin).


    :e.    :sp.    :vs.

            Ouvre l'explorateur  de fichiers dans  le dossier de  travail (abréviation de  :edit .)
            dans la fenêtre active, un viewport horizontal / vertical.


    :find foo    :sfind foo    :vert sfind foo    :tabfind foo

            Cherche le fichier foo dans un dossier de l'option 'path' et l'édite dans:

                    - la fenêtre courante
                    - un viewport horizontal
                    - un viewport vertcical
                    - un nouvel onglet


    gf
    gF

            Charger le buffer dont le chemin se trouve sous le curseur.
            Idem mais en positionnant le curseur sur le n° de ligne qui se trouvait après le chemin.

            Il se peut que le lien sous le curseur omette l'extension du fichier.
            Vim ne trouvera pas le fichier et se plaindra via l'erreur:

                    E447: Can't find file "/tmp/foo" in path

            Dans ce cas, on peut aider Vim à compléter le chemin via l'option locale au buffer
            'suffixesadd':

                    :set suffixesadd+=.sh,.vim

            Désormais, lorsque Vim ne trouvera pas un fichier, il tentera de compléter son chemin
            en ajoutant les extensions `.sh` et `.vim`


    ┌───────────────┬───────────────────────────────────────────────────────────────────────────────────────────┐
    │ 'A            │ 1er caractère non whitespace de la ligne où la marque globale A a été posée               │
    ├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
    │ `A            │ endroit exact de la marque A                                                              │
    ├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
    │ `0   ...   `9 │ endroit où on se trouvait au moment où la dernière / 9e précédente session s'est terminée │
    └───────────────┴───────────────────────────────────────────────────────────────────────────────────────────┘

