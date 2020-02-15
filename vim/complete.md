# Where does `C-x C-f` look for matches in insert mode when no text precedes the cursor?

The current working directory (as reported by `:pwd`).

##
# ?

Did we use a timer or a one-shot autocmd in the past where it was not needed?
Are there occasions where we could have delayed the execution of the code simply
by "moving" it later; e.g.:

    ino <expr> <key> <c-r>=FuncA()..FuncB()<cr>
                                    ^^^^^^^
                                    contains the code to be delayed

IOW, when is a timer or a one-shot autocmd really needed?

# ?

Make sure we haven't used a timer to restore an option, while we shouldn't have.
Try to use a one-shot autocmd instead; or try to "move" the code later if possible.

# ?

When `SafeState` is merged in Nvim, replace these lines:

    " ~/.vim/plugged/vim-cmdline/autoload/cmdline.vim:89
    call timer_start(0, {-> feedkeys(':'.cmdline.keys, 'in')})

with:

    let s:rerun_fixed_cmd ={-> feedkeys(':'.cmdline.keys, 'in')}
    au SafeState * ++once call s:rerun_fixed_cmd()

and:

    " ~/.vim/plugged/vim-completion/autoload/completion/spel.vim:57
    let new_line = substitute(getline('.'), '\<'.badword.'\>', suggestion, 'g')
    call timer_start(0, {-> setline('.', new_line)})

with:

    let new_line = substitute(getline('.'), '\<'.badword.'\>', suggestion, 'g')
    let s:fix_word = {-> setline('.', new_line)}
    au SafeState * ++once call s:fix_word()

# ?

Explain  why we  shouldn't  alter `'isk'`  from  a condition  (`s:setup_isk()`);
instead we must redefine a problematic default method.

Update:
I don't remember why I wrote this...
I suspect it was because we restored `'isk'` from a timer.
Indeed, suppose we have a chain of 2 methods `A-B`:

    A saves 'isk', starts a timer to restore it, alters 'isk', but fails to complete
    B saves 'isk', starts a timer to restore it, alters 'isk', and succeeds

The timer from  A will correctly restore  `'isk'`, but the one from  B will *not*.
Because when B was called, it saved the version of `'isk'` modified by A.
In the end, `'isk'` has now the value set by A.
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

# ?

Search for `compl[[=e=]]t` in our notes, and in vimrc.
Integrate any relevant comment here,  and integrate any relevant mapping/setting
in `vim-completion`.
Also integrate some comments from `vim-completion`.

# ?

Document what's the disadvantag of pressing `c-x c-p`, or `c-p`, instead of `c-x c-n`/`c-n`.

`:h 'cot /ctrl-l` doesn't work with `C-x C-p` and `C-p`:

    $ vim -Nu NONE +'set cot=menu,longest|startinsert!' =(cat <<'EOF'
    xx
    xxabc
    xxab
    xxa
    EOF
    )

If you press `C-x C-p`: `xxa` is completed.
If you then press `C-l`: no character is inserted.

Had you pressed `C-x C-n` instead of `C-x C-p`, `C-l` would have inserted `b`.

# ?

Document how the pum is populated with `C-x C-n` and `C-x C-p`.

I think that Vim looks for matches after the current position with `C-x C-n` and
populates the menu from its start down to its end.
OTOH, with  `C-x C-p`, Vim  looks for matches  before the current  position, and
populates the menu from its end up to its start.

If each match is present only once in the buffer, the resulting menu is identical:

    yy
    yya
    yyb
    yyc

However, it's *not*, if one of the match is present twice, and non-consecutively:

    zz
    zza
    zzb
    zzc
    zza

In the same way, document how Vim populates the pum with `C-n` and `C-p`.

# ?

Document that to use  omni completion, you need to set `'ofu'`  with the name of
a  custom  function,  and  that  you can  find  such  default  functions  inside
`$VIMRUNTIME/autoload/`; e.g.:

    setl ofu=syntaxcomplete#Complete

# ?

Le contenu  du pum est  mis à jour dynamiquement  après un `C-h`  (backspace) ou
l'insertion d'un nouveau caractère.
Sauf si une entrée a déjà été automatiquement insérée.
C'est le cas lorsque:

   - on tape C-n ou C-p

   - 'cot' ne contient ni 'noinsert', ni 'noselect'
     Vim insère alors automatiquement la 1e entrée du menu

Dans les 2 cas, l'insertion d'une entrée met fin à la mise à jour dynamique du menu.
La prochaine fois qu'on tapera un caractère manuellement, le menu se fermera.

##
# keybindings
## Voici qques raccourcis permettant d'interagir avec le pum

    C-l

Si le mot précédant  le curseur est plus court que  le match sélectionné, insère
un caractère supplémentaire pour s'en rapprocher.
Si aucun match n'est sélectionné, `C-l` utilise le 1er match du menu.

## Voici qques raccourcis permettant d'entrer dans un mode de complétion:
### `C-n`, `C-p`

Complétion de mots (next, previous).

Cherche  dans  tous  les  endroits  spécifiés  par  l'option  locale  au  buffer
`'complete'`, qui par défaut vaut:

    .,w,b,u,t,i

    ┌────────┬─────────────────────────────────────────────────────────────────────────┐
    │ .      │ buffer courant                                                          │
    ├────────┼─────────────────────────────────────────────────────────────────────────┤
    │ w      │ buffers des autres fenêtres                                             │
    ├────────┼─────────────────────────────────────────────────────────────────────────┤
    │ b      │ buffers chargés de la buffer list                                       │
    ├────────┼─────────────────────────────────────────────────────────────────────────┤
    │ u      │ buffers déchargés de la buffer list                                     │
    ├────────┼─────────────────────────────────────────────────────────────────────────┤
    │ t      │ fichiers tags                                                           │
    ├────────┼─────────────────────────────────────────────────────────────────────────┤
    │ i      │ fichiers précédés par des instructions tq: include, import, request ... │
    ├────────┼─────────────────────────────────────────────────────────────────────────┤
    │ kspell │ dictionnaire de notre langue (seulement qd 'spell' est activée)         │
    └────────┴─────────────────────────────────────────────────────────────────────────┘

### `C-x C-k`

Complète un nom à partir de mots trouvés dans un fichier dictionnaire.
On peut avoir plusieurs dico.
Leurs chemins doivent être ajoutés à la valeur de `'dict'`.

`'dict'` est une option globale ou locale au buffer.

Par  défaut, le  dico `/usr/share/dict/words`  est dispo  (il contient  des mots
anglais).
Pour ajouter un dico français, installer le paquet wfrench.
Il  installera  entre  autres  le fichier  /usr/share/dict/french  qu'on  pourra
ajouter à `'dict'`.

### `C-x C-l`

Complète la ligne (cherche dans les fichiers définis par `'complete'`).

Si on se trouve au milieu d'une ligne ça marche en une seule fois.

Si on se trouve à la fin d'une ligne, on peut directement compléter la suivante :

   - en une seule invocation si on vient juste de compléter la ligne courante

   - en 2 invocations autrement (càd qu'on a tapé la ligne manuellement)
     la 1e invocation repropose juste la ligne courante

En   fait,  ce   chord  se   souvient  des   complétions  similaires
précédentes, de la même façon que `C-x C-n` ou `C-x C-p`.

---

Raccourci  facilement répétable  à condition  de ne  pas insérer  de
lignes vides à l'intérieur d'un bloc de code (pex une fonction).
Autrement, après une ligne vide,  le raccourci proposera bcp trop de
suggestions non  pertinentes, si notre  buffer est rempli  de lignes
vides pour aérer.

### `C-x C-n`, `C-x C-p`

La 1e fois qu'on utilise un de ces chords, Vim complète le mot courant.
La fois suivante, il  se souvient du mot qu'on vient de  compléter et ne propose
que des matchs qui sont précédés de ce mot ailleurs dans le buffer.
Les fois d'après, il continue de se souvenir des précédentes complétions.

Les propositions sont plus ciblées  qu'avec `C-n`/`C-p`, non seulement parce que
ce chord  tient compte des  complétions précédentes,  mais aussi parce  qu'il ne
cherche pas dans tous les buffers, uniquement dans le buffer courant
(cf: `:h compl-current`).

### `C-x C-o`

omni-complétion

Vim devine  la nature  de l'objet  (d'où le  `omni`... omniscient)  précédant le
curseur, et propose des matchs commençant de la même façon.

Utile pour compléter des noms d'objets qui  n'ont pas été analysés par ctags, ou
qui ne peuvent pas l'être comme pex des  noms de fonctions intégrées à Vim ( ex:
`setreg()`).

Pour certains languages il faut installer  un programme tiers pour documenter la
fonction d'omnicomplétion.
Pour python, il y a jedi et son plugin Vim jedi-vim.

L'omni-complétion est  très proche de la  complétion custom (`C-x C-u`):  elle est
gérée par une fonction dont le nom est définie par une option locale au buffer.
`'omnifunc'` pour  `C-x C-o`,  `'completefunc'` pour `C-x C-u` Une  fonction `'omnifunc'`
doit être écrite comme une fonction `'completefunc'` (`if a:findstart | ...`).

La  principale  différence  vient  du   fait  que  la  fonction  'omnifunc'  est
généralement définie par  un filetype plugin, qu'elle est donc  propre à un type
de  fichiers,  et  qu'elle  complète  des mots-clés  propres  à  un  langage  de
programmation (pratique qd on ne connaît pas bien le langage en question).
Une fonction de  complétion omnifunc pour python, une autre  pour html, une pour
css etc.

Permet de compléter automatiquement une balise fermante en html en tenant compte
de la précédante balise ouvrante.

Ex:

    <p> ... </ + C-x C-o
    →
    <p> ... </p>

### `C-x s`

Complète   le  mot   précédant   le  curseur   en   proposant  des   corrections
orthographiques.
Nécessite que l'option (locale à la fenêtre) 'spell' soit activée.

### `C-x C-t`

Complète le mot précédant le curseur en proposant des synonymes.
Les  synonymes sont  cherchés dans  un  fichier dont  le chemin  est présent  ds
l'option `'thesaurus'`.

Ce  type de  complétion est  utile pex  pour accéder  à un  ensemble de  noms de
fonctions, ou  d'autres termes qui  ne sont  pas forcément synonymes  mais qu'on
peut ranger dans une même catégorie.

### `C-x C-u`

Complète via une fonction custom.

Le  nom de  la fonction  est défini  par l'option  locale au  buffer
'completefunc'.
Vim  appelle la  fonction 2  fois consécutivement  en lui  passant à
chaque fois 2 arguments:

   - 1, ''
   - 0, 'texte à compléter'

Au  sein  de  la  fonction,  par convention,  on  peut  appeler  ces
arguments `findstart` et `base`.

Le corps de la fonction doit suivre la syntaxe:

    if a:findstart
        ...
        return {index du 1er octet du texte à compléter -1}
    else
        ...
        return {matchs}
    endif

Pk -1?
Probablement car le nb est utilisé comme un index de chaîne.
Or qd on  indexe des caractères au sein d'une  chaîne, on commence à
compter à partir de 0.

---

On peut trouver le début du texte à compléter de 2 façons:

   - via `searchpos()`

     Ex: pour compléter du curseur jusqu'au précédent double quote:

        return searchpos('"', 'bcnW', line('.'))[1] - 1

   - une boucle `while`

     Ex: pour compléter du curseur jusqu'au précédent caractère absent de la classe `\k`:

        let start = col('.') - 1
        while start > 0 && getline('.')[start - 1] =~ '\k'
            let start -= 1
        endwhile
        return start

Qu'est-ce que `start` ?
Initialement, il s'agit  de l'index du 1er octet  suivant le curseur
(qui peut ne pas exister si on est en fin de ligne), `-1`.

Chaque  itération de  la boucle  teste si  le caractère  (en réalité
octet) précédant `start` est dans `'isk'`.
Si oui, `start` est décrémenté.
Autrement la boucle s'arrête et la fonction retourne `start`, qui au
final contient l'index du 1er octet du texte à compléter, `-1`.

---

Si le  texte à compléter  peut contenir  des caractères multi-octets,  la boucle
while n'est pas fiable.
Il vaut mieux utiliser `searchpos()` (avec pex le pattern `\<\k`).

En effet, `while` s'appuie sur le test:

    getline('.')[start-1] =~ '\k'

Or, si `start-1` correspond à l'index  d'un octet d'un caractère multi-octet, le
test échouera.

Ex:

    getline('.')            =     'élé'
    start                   =     col('.') - 1  =    6 - 1    =    5
    getline('.')[start - 1] =     'élé'[4]      =    <a9>    !~    '\k'

---

Pour peupler les matchs on utilisera pex le code suivant:

    let matches = []
    sil keepj keepp %s/pat/\=add(matches, submatch(0))/gne
    return filter(matches, {_,v -> v[:strlen(a:base)-1] is# a:base})

#
# What can `C-x C-v` complete in addition to Ex commands?

Their arguments.

    com - C-x C-v
    addr~
    bang~
    bar~
    buffer~
    complete~
    count~
    nargs~
    range~
    register~

# Why doesn't `C-x C-v` complete `com` when the line is `foo com`?

The command name  must be at the  beginning of the line, because  Vim parses the
line to try to guess the role of each word.
If your  line begins with  a random  word, it will  be considered as  an invalid
command.

# How to navigate in the pum without inserting any match?

Press `Up` and `Down` instead of `C-n` and `C-p`.

##
# Issues
## A noisy message is logged every time I use dictionary completion!

It's a known issue: <https://github.com/vim/vim/issues/3412#issuecomment-570905815>
It could be fixed in the future.

---

MWE:

    $ vim -Nu NONE +'set dict=/usr/share/dict/words shm+=filmnrwxaoOstTWAIcqFS' +startinsert +'call feedkeys("simul")'
    " press C-x C-k
    " keep pressing C-k
    :mess
    match in file /usr/share/dict/words~
    match in file /usr/share/dict/words~
    ...~

Same issue with the `C-n` (and `C-p`) completion.

---

Note that the reason  why you don't see the messages with  `-Nu NONE` is because
`'showmode'` is set by default, but you reset it in your vimrc.
And when `'showmode'` is set while `'shm'` includes the `c` flag, `-- INSERT --`
is  displayed on  the  command-line  which has  the  side effect  of hiding  the
messages from `C-x C-k`.

The actual messages depend on whether `'showmode'` is set and whether `'shm'` contains `c`.

##
# Todo
## ?

    $ vim -o =(echo ruby) =(echo rubyinterp) +'setl dict=/usr/share/dict/words' +startinsert!

You want to complete `ruby` into `rubyinterp` (which is displayed in the other window).

Press Tab to complete `ruby`.
The pum suggests:

    Ruby /usr/share/dict/words
    ruby /usr/share/dict/words

And the text has been changed to `Ruby`.
Press `C-j`  to try another  completion command;  you don't get  any different
results, and yo don't get `rubyinterp`.

Also,  press `C-q`  to quit  the  pum: `Ruby` stays  in the  buffer, it's  not
replaced with the original text `ruby`.

It's because we include `longest` in `'cot'`, in `vim-completion`.

MWE:

    $ cat <<'EOF' >/tmp/dict
    fooxxa
    fooxxb
    fooxxc
    EOF

    $ vim -Nu NONE =(echo foo) +'setl cot+=longest dict=/tmp/dict' +'startinsert!'
    " press C-x C-k to complete
    " press C-e to cancel: `fooxx` is in the buffer, while originally only `foo` was in the buffer

Solution: Install a custom `C-q` mapping which restores the original text.
Save the latter before the completion starts.
Use your custom mapping in `vim-completion` instead of `C-e`.

Issue: It's hard to save the original text.
It's not stored in any `v:` variable.
And even if you can save it, restoring it would probably break the dot command.

Update: I think it could be considered as a bug.
Here is what `:h popupmenu-keys` says:

>     CTRL-E    End completion, go back to what was there before selecting a
>               match (what was typed **or longest common string**).

I can see why `C-e` behaves like it does (see bold text).
And most of the time, it's probably desirable.
But  I still  think  that  in some  cases  (when you  want  to  try a  different
completion command next) the behavior is undesirable.
Try to ask for `C-e` to restore the original text.
Or for an option to do so.
Or for a function to give the original text.
I guess that the `inserted` item from `:h complete_info(` could help.
But not entirely (what if the case of the text has changed too?).
Also, whatever fix you implement, it would probably break the dot command.

