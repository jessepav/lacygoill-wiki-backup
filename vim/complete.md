Make sure we haven't used a timer to restore an option, while we shouldn't have.


Explain why we shouldn't alter 'isk' from a condition (`s:setup_isk()`); instead
we must redefine a problematic default method.

Update:
I don't remember why I wrote this...
I suspect it was because we restored 'isk' from a timer.
Indeed, suppose we have a chain of 2 methods `A-B`:

    A saves 'isk', starts a timer to restore it, alters 'isk', but fails to complete
    B saves 'isk', starts a timer to restore it, alters 'isk', and succeeds

The timer from A will correctly restore 'isk', but the one from B will NOT.
Because when B was called, it saved the version of 'isk' modified by A.
In the end, 'isk' has now the value set by A.
It's just a theory though, as I don't remember what was the issue...

I suppose the solution was to restore the option from an autocmd listening
to `CompleteDone`,  which should be  emitted every time  a method is  called (no
matter whether it succeeds).
The  timers on  the other  hand are  probably processed  after Vim  has finished
trying all the methods (because it must empty the typeahead buffer before).

The issue is due to the fact that we don't know when the callback will be processed.
So, we can't be  sure that between the time we change an  option and the time we
restore it,  there will not  be another called function  which will do  the same
thing: save/alter/restore this option.

Probable bottom line:
never restore an option from a timer; restore it from a known point in your code
or event.


Search for `compl[[=e=]]t` in our notes, and in vimrc.
Integrate any relevant comment here,  and integrate any relevant mapping/setting
in `vim-completion`.
Also integrate some comments from `vim-completion`.

# 'cot'

Le comportement d'une complétion est géré par l'option 'completeopt'.
Celle-ci peut prendre une série de valeurs. Les plus importantes sont:

        • 'noinsert'    la 1e entrée n'est pas automatiquement insérée,
                        mais elle peut être automatiquement sélectionnée

        • 'noselect'    elle n'est ni insérée, ni sélectionnée


Le contenu  du menu  est mis à  jour dynamiquement après  un C-h  (backspace) ou
l'insertion d'un nouveau caractère.
Sauf si une entrée a déjà été automatiquement insérée.
C'est le cas lorsque:

        • on tape C-n ou C-p

        • 'cot' ne contient ni 'noinsert', ni 'noselect'
          Vim insère alors automatiquement la 1e entrée du menu

Dans les 2 cas, l'insertion d'une entrée met fin à la mise à jour dynamique du menu.
La prochaine fois qu'on tapera un caractère manuellement, le menu se fermera.

# keybindings

Voici qques raccourcis permettant d'interagir avec le menu de complétion:


    C-l

            Si  le mot  précédant actuellement  le curseur  est +  court que  le
            candidat sélectionné,  insère un caractère supplémentaire  pour s'en
            rapprocher.
            Si aucun candidat n'est sélectionné,  C-l utilise le 1er candidat du
            menu.

Voici qques raccourcis permettant d'entrer dans un mode de complétion:

    C-n    C-p

            complétion de mots (next, previous)

            Cherche  dans tous  les endroits  spécifiés par  l'option locale  au
            buffer 'complete', qui par défaut vaut:

                    .,w,b,u,t,i

            .    buffer courant
            w    buffers des autres fenêtres
            b    buffers chargés de la buffer list
            u    buffers déchargés de la buffer list
            t    fichiers tags
            i    fichiers précédés par des instructions tq: include, import, request …
            kspell
                 dictionnaire de notre langue (seulement qd 'spell' est activée)

    C-x C-f

            Complète un nom  de fichier/dossier en cherchant dans  le dossier de
            travail (:pwd).

            Si un  chemin vers un  dossier précède  le curseur, cherche  dans ce
            dossier plutôt que dans le dossier de travail.
            On peut compléter tout un chemin en répétant ce chord.

    C-x C-k

            Complète  un  nom   à  partir  de  mots  trouvés   dans  un  fichier
            dictionnaire.
            On peut avoir plusieurs dico.
            Leurs chemins  doivent être  ajoutés à la  valeur de  'dictionary' /
            'dict'.

            'dict' est une option globale ou locale au buffer.

            Par défaut, le dico /usr/share/dict/words est dispo (il contient des
            mots anglais).
            Pour ajouter un dico français, installer le paquet wfrench.
            Il installera  entre autres le fichier  /usr/share/dict/french qu'on
            pourra ajouter à 'dict'.

    C-x C-l

            Complète la ligne (cherche dans les fichiers définis par 'complete').

            Si on se trouve au milieu d'une ligne ça marche en une seule fois.

            Si on se trouve à la fin d'une ligne, on peut directement compléter la suivante :

                    • en une seule invocation si on vient juste de compléter la ligne courante

                    • en 2 invocations autrement (càd qu'on a tapé la ligne manuellement)
                      la 1e invocation repropose juste la ligne courante

            En   fait,  ce   chord  se   souvient  des   complétions  similaires
            précédentes, de la même façon que `C-x C-n` ou `C-x C-p`.

                                     NOTE :

            Raccourci  facilement répétable  à condition  de ne  pas insérer  de
            lignes vides à l'intérieur d'un bloc de code (pex une fonction).
            Autrement, après une ligne vide,  le raccourci proposera bcp trop de
            suggestions non  pertinentes, si notre  buffer est rempli  de lignes
            vides pour aérer.


    C-x C-n
    C-x C-p

            La  1e fois  qu'on utilise  un de  ces chords,  Vim complète  le mot
            courant.
            La fois suivante, il se souvient  du mot qu'on vient de compléter et
            ne propose  que des candidats qui  sont précédés de ce  mot ailleurs
            dans le buffer.
            Les  fois  d'après,  il  continue de  se  souvenir  des  précédentes
            complétions.

            Les  propositions sont  plus  ciblées qu'avec  C-n/p, non  seulement
            parce que  ce chord tient  compte des complétions  précédentes, mais
            aussi parce qu'il  ne cherche pas dans tous  les buffers, uniquement
            dans le buffer courant (cf: :h compl-current).


    C-x C-o

            omni-complétion

            Vim  devine la  nature  de l'objet  (d'où  le 'omni'...  omniscient)
            précédant le curseur, et propose des candidats commençant de la même
            façon.

            Utile pour  compléter des noms  d'objets qui n'ont pas  été analysés
            par  ctags, ou  qui ne  peuvent  pas l'être  comme pex  des noms  de
            fonctions intégrées à Vim ( ex: setreg() ).

            Pour certains  languages il faut  installer un programme  tiers pour
            documenter la fonction d'omnicomplétion.
            Pour python, il y a jedi et son plugin Vim jedi-vim.

            L'omni-complétion est très proche de la complétion custom (C-x C-u):
            elle est  gérée par  une fonction  dont le nom  est définie  par une
            option locale au buffer.
            'omnifunc' pour  C-x C-o, 'completefunc'  pour C-x C-u  Une fonction
            'omnifunc' doit  être écrite  comme une fonction  'completefunc' (if
            a:findstart | …).

            La principale  différence vient du  fait que la  fonction 'omnifunc'
            est généralement  définie par un  filetype plugin, qu'elle  est donc
            propre  à un  type de  fichiers, et  qu'elle complète  des mots-clés
            propres à un langage de programmation (pratique qd on ne connaît pas
            bien le langage en question).
            Une  fonction de  complétion omnifunc  pour python,  une autre  pour
            html, une pour css etc.

            Permet de compléter  automatiquement une balise fermante  en html en
            tenant compte de la précédante balise ouvrante.

            Ex:    <p> … </ + C-x C-o    →    <p> … </p>

    C-x s

            Complète le  mot précédant le  curseur en proposant  des corrections
            orthographiques.
            Nécessite que l'option (locale à la fenêtre) 'spell' soit activée.

    C-x C-t

            Complète le mot précédant le curseur en proposant des synonymes.
            Les  synonymes sont  cherchés dans  un  fichier dont  le chemin  est
            présent ds l'option 'thesaurus'.

            Ce type  de complétion est utile  pex pour accéder à  un ensemble de
            noms  de fonctions,  ou d'autres  termes qui  ne sont  pas forcément
            synonymes mais qu'on peut ranger dans une même catégorie.


    C-x C-u

            Complète via une fonction custom.

            Le  nom de  la fonction  est défini  par l'option  locale au  buffer
            'completefunc'.
            Vim  appelle la  fonction 2  fois consécutivement  en lui  passant à
            chaque fois 2 arguments:

                    • 1, ''
                    • 0, 'texte à compléter'

            Au  sein  de  la  fonction,  par convention,  on  peut  appeler  ces
            arguments `findstart` et `base`.

            Le corps de la fonction doit suivre la syntaxe:

                    if a:findstart
                        ...
                        return {index du 1er octet du texte à compléter -1}
                    else
                        ...
                        return {candidates}
                    endif

            Pk -1?
            Probablement car le nb est utilisé comme un index de chaîne.
            Or qd on  indexe des caractères au sein d'une  chaîne, on commence à
            compter à partir de 0.

                                               NOTE:

            On peut trouver le début du texte à compléter de 2 façons:

            • via `searchpos()`

              Ex: pour compléter du curseur jusqu'au précédent double quote:

                     return searchpos('"', 'bcnW', line('.'))[1] - 1

            • une boucle `while`

              Ex: pour compléter du curseur jusqu'au précédent caractère absent de la classe `\k`:

                     let start = col('.') - 1
                     while start > 0 && getline('.')[start - 1] =~ '\k'
                         let start -= 1
                     endwhile
                     return start

            Qu'est-ce que `start` ?
            Initialement, il s'agit  de l'index du 1er octet  suivant le curseur
            (qui peut ne pas exister si on est en fin de ligne), -1.

            Chaque  itération de  la boucle  teste si  le caractère  (en réalité
            octet) précédant `start` est dans 'isk'.
            Si oui, `start` est décrémenté.
            Autrement la boucle s'arrête et la fonction retourne `start`, qui au
            final contient l'index du 1er octet du texte à compléter, -1.


                                               NOTE:

            Si le texte  à compléter peut contenir  des caractères multi-octets,
            la boucle while n'est pas fiable.
            Il vaut mieux utiliser `searchpos()` (avec pex le pattern '\<\k').

            En effet, `while` s'appuie sur le test:

                    getline('.')[start-1] =~ '\k'

            Or,  si `start-1`  correspond à  l'index d'un  octet d'un  caractère
            multi-octet, le test échouera.

            Ex:
                   getline('.')            =     'élé'
                   start                   =     col('.') - 1  =    6 - 1    =    5
                   getline('.')[start - 1] =     'élé'[4]      =    <a9>    !~    '\k'


                                               NOTE:

            Pour peupler les candidats on utilisera pex le code suivant:

                    let candidates = []
                    sil keepj keepp %s/pat/\=add(candidates, submatch(0))/gne
                    return filter(candidates, 'v:val[:strlen(a:base)-1] ==# a:base')

#
#
#
#
# Does C-x C-v complete only Ex commands?

No.

It can also complete their arguments.

# Why doesn't C-x C-v always complete an Ex command?

The command name  must be at the  beginning of the line, because  Vim parses the
line to try to guess the role of each word.
If your  line begins with  a random  word, it will  be considered as  an invalid
command.

# How to navigate in the completion menu without inserting any candidate?

Press `Up` and `Down` instead of `C-n` and `C-p`.

# Can I use a timer to restore the value of an option influencing a completion?

It depends.

If your code involves a chain of completions, then no.
You couldn't be sure  that the callback would be executed before  the try of the
next completion method in the chain.
As a  result, later, you  would risk saving/restoring  a modified value  of your
option.

Instead, you should always try to listen to `CompleteDone`, which is a much more
relevant and precise event than “in a very short period of time”.

Otherwise (no chain of completions), a timer may work as expected.

More generally,  you can use  a timer to restore  something only if  you're sure
that the change can NOT be repeated too quickly, i.e. BEFORE the callback.

