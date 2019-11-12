# How to allow an autocmd, which is installed from a function, to access a variable in the function scope?  (3)

Use:

   - a lambda

         fu Func()
            let var = 'defined in outer scope'
            let s:lambda = {-> var}
            au SafeState * ++once echo s:lambda()
         endfu
         call Func()
         defined in outer scope~

   - a closure

         fu Func()
            let var = 'defined in outer scope'
            fu! Closure() closure
                echo var
            endfu
            au SafeState * ++once call Closure()
         endfu
         call Func()
         defined in outer scope~

   - a partial

         fu Func()
            let var = 'defined in outer scope'
            let s:partial = function('s:echo', [var])
            au SafeState * ++once call s:partial()
         endfu
         fu s:echo(var)
            echo a:var
         endfu
         call Func()
         defined in outer scope~

---

The solution  using a  closure can seem  awkward, because you  need to  define a
function inside another function.

---

The solution using a lambda can sometimes seem awkward:

    fu Func()
       let var = 'defined in outer scope'
       let s:lambda = {-> execute('let g:var_save ='..string(var))}
       au SafeState * ++once call s:lambda()
    endfu
    call Func()

    " need to wait for `SafeState` to be fired
    echo g:var_save
    defined in outer scope~

Here, the  `execute()` used  to get  an expression to  pass in  the body  of the
lambda is ugly.
Besides, the `string()` invocation seems brittle.
Although, it seems to work, even if the variable contains quotes:

    fu Func()
       let var = "a'b\"c"
       let s:lambda = {-> execute('let g:var_save ='..string(var))}
       au SafeState * ++once call s:lambda()
    endfu
    call Func()

    echo g:var_save
    a'b"c~

---

The solution using a partial has 2 drawbacks:

   - it's longer

   - you need to come up with yet another variable name (in the previous example `s:partial`),
     and it needs to be unique in the current script

## Each of these solutions requires the creation of an extra variable/function.
### So what is their benefit over simply moving the variable from the function scope to the script scope?

These solutions scale better when you need to access several variables.

Example:

    fu Func()
       let [a, b, c] = [1, 2, 3]
       fu! Closure() closure
           echo a + b + c
       endfu
       au SafeState * ++once call Closure()
    endfu
    call Func()
    6~

    fu Func()
       let [s:a, s:b, s:c] = [1, 2, 3]
       au SafeState * ++once echo s:a + s:b + s:c
    endfu
    call Func()
    6~

In the second case,  you have to create 3 script-local variables  to get the sum
of the variables.

It may seem awkward  because you may consider them relevant  only in the context
of `Func()`, so putting them in the script-local scope may feel like giving them
too much importance.

Besides, the extra `s:` makes the variable names a little harder to read.

Finally,  it's harder  to avoid  conflicts between  script-local variables  than
between function-local ones, simply because a script is usually much longer than
a function.

##
# How to write the quantifier “0 or 1” in the pattern of an autocmd?

    {foo,}bar

This should match `foobar` or just `bar`.

##
# How to write a one-shot autocmd?

Use the `++once` flag.

    au {event} {pat} ++once {cmd}
                     ^^^^^^

## Does `++once` prevent the duplication of an autocmd if its code is sourced multiple times?

No:

    :au CursorHoldI * ++once "
    2@:
    :au CursorHoldI
    CursorHoldI~
        *         "~
                  "~
                  "~

##
## Why shouldn't I wrap all one-shot autocmds inside an augroup?

First, `++once`  is clearly  meant, among  other things, to  make the  code less
verbose, and get rid of the augroup:

> Before:

>     augroup FooGroup
>       autocmd!
>       autocmd FileType foo call Foo() | autocmd! FooGroup FileType foo
>     augroup END

> After:

>     autocmd FileType foo ++once call Foo()

Source: <https://github.com/vim/vim/pull/4100>

---

Second, in practice, a one-shot autocmd will often have a short life (e.g. fired
the next time the cursor is moved), so the risk of duplication is low.

---

Third, even though `++once` does not prevent a duplication, it limits its effects.

To illustrate, in this example:

    :au CursorHoldI * ++once "
    :au CursorHoldI * ++once "
    :au CursorHoldI * ++once "

the  next time  `CursorHoldI` will  be  fired, all  the autocmds  will be  fired
and  removed; without  `++once`,  they would  keep being  run  again every  time
`CursorHoldI` is fired.

### When should I do it then?  (3)

When you *need* to be able to remove it before the event it's listening to:

    augroup some_group
        au!
        au {event} {pat} ++once {cmd}
    augroup END

    if some condition
        au! some_group
    endif

See the `search#nohls()` function in `vim-search` for an example.

---

When your  command needs to  be fired from  two different autocmds  (because you
need two patterns with different meanings or values).
Suppose you want to call `Func()` only once, as soon as `CursorHold` is fired or
you enter the Ex command-line; you could write:

    augroup some_group
        au!
        au CursorHold * call Func()
        au CmdlineEnter : call Func()
    augroup END
    fu Func()
        au! some_group
        " do sth
    endfu

But you couldn't re-write it like this:

    au CursorHold * ++once call Func()
    au CmdlineEnter : ++once call Func()
    fu Func()
        " do sth
    endfu

Because `Func()` would be called twice, not once.
Once for each event.

See the augroup `delay_slow_call` in our vimrc for a real example.

---

When there is a  real risk of duplication, and the  latter would give unexpected
results.

##
## How many times is the autocmd fired if it listens to several events?

Once per event.

### How to fire it just once, regardless of how many events it listens to?

Use a guard.

    unlet! s:did_shoot
    au Event1,Event2,... * ++once
        \ if !get(s:, 'did_shoot', 0)
        \ |     let s:did_shoot = 1
        \ |     " do sth just once
        \ | endif

---

Alternatively,  you could  wrap the  autocmd in  an augroup,  and make  it clear
itself the first time it's fired.
However, be  aware of  a possible  pitfall: if one  of the  commands run  by the
autocmd fails,  the rest won't be  processed; this may prevent  the final `:au!`
command from being run.
To  avoid this  issue,  you need  to  prefix every  command  before `:au!`  with
`:silent!`, or use a `:try` conditional to catch possible errors.

##
# When several autocmds listen to the same event, in which does Vim run them?

In the order they were installed.

# Why does `:LogEvents` logs the events `Syntax`, `FileType` and `BufReadPost` in this order (instead of the reverse)?

Because of this rule:

When Vim runs an autocmd listening to an  event A which triggers an event B, Vim
pushes  the autocmds  listening  to A  on  a stack,  then  immediately runs  the
autocmds listening  to B,  *before* going  on running the  rest of  the autocmds
listening to A.

You must consider 5 autocmds:

    ┌────────────────────────────────────┬──────────────┬──────────────────────────────┐
    │ installed by                       │ listening to │ action                       │
    ├────────────────────────────────────┼──────────────┼──────────────────────────────┤
    │ (1) $VIMRUNTIME/filetype.vim       │ BufReadPost  │ set up 'ft'                  │
    ├────────────────────────────────────┼──────────────┼──────────────────────────────┤
    │ (2) $VIMRUNTIME/syntax/syntax.vim  │ FileType     │ set up 'syntax'              │
    ├────────────────────────────────────┼──────────────┼──────────────────────────────┤
    │ (3) $VIMRUNTIME/syntax/synload.vim │ Syntax       │ loads syntax highlighting    │
    ├────────────────────────────────────┼──────────────┼──────────────────────────────┤
    │ (4) :LogEvents                     │ Syntax       │ log Syntax                   │
    ├────────────────────────────────────┼──────────────┼──────────────────────────────┤
    │ (5) :LogEvents                     │ FileType     │ log FileType                 │
    └────────────────────────────────────┴──────────────┴──────────────────────────────┘

When you load a file:

        1. `BufReadPost` is fired
        2. the autocmds listening to `BufReadPost` are run, (1) being the first of them
        3. 'ft' is set up
        4. `FileType` is fired

        5. Vim stops processing the autocmds listening to `BufReadPost` because
           of the previous rule, and the autocmds listening to `FileType` are
           run, (2) being the first of them

        6. 'syntax' is set up
        7. `Syntax` is fired

        9. Vim stops processing the autocmds listening to `FileType` because of
           the previous rule, and the autocmds listening to `Syntax` are run,
           (3) being the first of them

       10. the syntax highlighting is loaded for the current buffer

       11. (4) is run

           (4) is run after (3)  because `:LogEvents` has installed its autocmds
           after the ones in `$VIMRUNTIME`

       12. the rest of the autocmds listening to `FileType` are run, (5) being
           the first of them

---

Do *not* conflate a **type** of event with an **occurrence** of event.

When you think:

> `BufReadPost` comes before `FileType`

it does not mean:

> ANY occurrence of `BufReadPost` comes before ANY occurrence of `FileType`

but:

> there is ONE occurrence of `BufReadPost` which triggers ONE occurrence of `FileType`

# What are the best events to automatically create/remove a match in a window?

Use `WinEnter` to create a match.
Use `BufWinLeave` to remove it.

---

Do NOT use `BufWinEnter` to create a match, it would fail when you execute:

        :split
        :split file_already_opened

Because in those cases, `BufWinEnter` is not  fired, and the new window does NOT
inherit the matches of the original window.

Do  NOT use  `WinLeave`  to remove  a  match, it  would cause  the  match to  be
installed only when you focus the window.

FIXME:

If  the  buffer  is  displayed  in  another  window  (no  matter  the  tabpage),
`BufWinLeave` won't be fired.
So the match could stay in a window, while it should be removed.

MWE:

        :sp ~/.vim/filetype.vim
        :put ='set error'
            'set ' is highlighted ✔

        :sp
        :e /tmp/file
        :put ='set error'
            'set ' is highlighted ✘

This  is because  when  you ran  `:e /tmp/file`,  `BufWinLeave`  was not  fired,
because `filetype.vim` was still displayed in a window.

##
# What is the difference between `SafeState` and `SafeStateAgain`?

I think they have the same meaning: they're fired when Vim has nothing to do.

However,  `SafeStateAgain` is  fired after  Vim  has invoked  a callback  (think
timer, job, ...), or processed a message from a job.
When invoking  a callback/processing  a message,  Vim is  busy again,  and right
afterward it's idle again (so it's safe to run sth again and `SafeStateAgain` is
fired).

##
##
# Syntaxe

    :verb au         {event}
    :verb au {group} {event}

            Affiche toutes les autocmd déclenchées qd {event} / {event} au sein de {group} se produit,
            et pour chacune le fichier qui l'a installée.


    augroup TEST
        au!
        exe 'au BufEnter * let g:myvar = get(g:, "myvar", 0) + 1'
    augroup END

            Toute commande `:au` exécutée à l'intérieur d'un augroup appartient à cet augroup,
            même si elle est exécutée indirectement via `:exe`.

            IOW, il n'y a pas de duplication si on source plusieurs fois le script où elle est définie.

            On peut le vérifier avec cet exemple.
            Tant que l'instruction `:exe …` reste à l'extérieur de l'augroup, `g:myvar` est incrémentée
            de 1 à chaque fois qu'on change de buffer.

            Mais dès qu'elle passe à l'extérieur, et qu'on la source plusieurs fois, `g:myvar` est incrémentée
            avec une valeur >1.


    doautocmd CursorMoved
    doautoall SessionLoadPost

            Déclenche l'évènement `CursorMoved`     dans      le buffer courant.
                                  `SessionLoadPost` dans tous les buffers.

            En réalité, exécute les autocmd surveillant `CursorMoved` / `SessionLoadPost`, mais
            conceptuellement il est plus facile de voir `:doauto{cmd|all}` comme des déclencheurs
            d'évènement.

            Attention, ne pas utiliser `:doautoall` pour:

                    - supprimer un buffer
                    - charger un autre buffer
                    - changer le contenu d'un buffer

            Le résultat serait imprévisible.
            `:doautoall` est destinée à exécuter des autocmds qui configurent des options,
            changent la coloration syntaxique, etc.
            IOW, `:doautoall` est destinée à modifier l'apparence des buffers, pas leurs contenus.


    if exists('#User#MyFuncPost')
        doautocmd <nomodeline> User MyFuncPost
    endif

            Crée et déclenche l'évènement `MyFuncPost`.

            Utile dans un plugin à la fin de `MyFuncPost()`.
            Permet aux utilisateurs d'exécuter leur propre fonction à chaque fois que `MyFunc()` est exécutée.
            Techniquement, on dit que l'utilisateur enregistre sa fonction en tant que callback.


                                               NOTE:

            Pourquoi tester l'existence de l'autocmd avant de l'exécuter ?
            Car si l'utilisateur n'installe aucune autocmd écoutant `MyFuncPost`, chaque fois
            que `MyFunc()` sera exécutée, il aura le message:

                    No matching autocommands

            Une solution consiste à préfixer `:doautocmd` avec `:silent`:

                    silent doautocmd User MyFuncPost

            Mais du coup, l'utilisateur ne peut plus afficher un message avec `:echo`:

                    silent doautocmd User MyFuncPost
                    autocmd          User MyFuncPost echo 'message'    ✘

            Il devra alors utiliser `:unsilent` pour temporairement “lever“ le silence:

                    silent doautocmd User MyFuncPost
                    autocmd          User MyFuncPost unsilent echo 'message'    ✔

            Pour éviter de devoir recourir à `:unsilent` à chaque fois qu'on veut afficher un message,
            il vaut donc mieux vérifier l'existence de l'autocmd avant son exécution.


                                               NOTE:

            Pourquoi l'argument `<nomodeline>` ?

            Par  défaut, après  avoir  exécuté une  autocmd,  si 'modeline'  est
            activée, et  que la valeur de  'modelines' est différente de  0, Vim
            traite les modelines du buffer courant.
            Il fait  cela pour  que leurs configurations  aient la  priorité par
            rapport à d'éventuelles configurations apportées par les autocmd.

            Le  traitement des  modelines  à la  suite  d'une autocmd  utilisant
            l'évènement `User {MadeUpEvent}` est probablement non désiré.

            Plus   généralement,   on    pensera   à   utiliser   `<nomodeline>`
            systématiquement sauf pour les  évènements `Buf*` (BufAdd, BufEnter,
            BufNew, BufNewFile, BufReadPost, BufUnload, BufWinEnter).
            Exception:
            on peut utiliser `<nomodeline>` avec BufReadPost dans un buffer qf.
            En effet, un buffer qf est spécial: l'utilisateur ne peut pas y
            écrire des modelines.

            Cf `:h :do` et:
            https://github.com/tpope/vim-commentary/issues/26


    autocmd User MyFuncPost call MyFunc()

            Illustre comment un utilisateur peut exécuter sa fonction `MyFunc()` à la suite de la fonction
            `MyFunc()` d'un plugin.
            Nécessite que l'auteur du plugin ait créé et déclenché l'évènement `MyFuncPost` via `:doautocmd`.

# Évènements

Les conditions et l'ordre dans lequel les évènements se produisent est complexe.
Pour s'aider on peut utiliser notre commande custom:

        :LogEvents {events}


Voici qques exemples de suites d'évènements qui se produisent qd on réalise une action donnée:

        donner le focus à une autre fenêtre        WinEnter > BufEnter

        charger un buffer                          BufRead > BufEnter > BufWinEnter

        lancer Vim sans argument                   BufWinEnter > BufEnter

        afficher son vimrc                         WinEnter      > BufRead > BufEnter
        SPC ec                                     > BufWinEnter > BufRead > BufEnter
                                                   > BufWinEnter

        ouvrir un nouvel onglet                    WinEnter > BufEnter > BufWinEnter

        fermer un onglet                           WinEnter > BufEnter


Exemples d'évènements :

    BufLeave

            avant de quitter le buffer courant

            On peut quitter le buffer courant en:

                - passant le focus à une autre fenêtre ne l'affichant pas,
                - affichant un autre buffer dans la fenêtre (:e another_buffer),
                - le déchargeant via :bd (ce qui a pour effet de fermer toutes les fenêtres l'affichant)

            L'évènement n'est pas déclenché si le buffer est le dernier affiché et qu'on quitte Vim.
            Utiliser probablement VimLeave(Pre) dans ce cas.

    BufNewFile

            création d'un nouveau fichier (non existant)

    BufRead(Post)

            après avoir chargé un buffer correspondant à un fichier existant


    ┌─────────────┬──────────────────────────────────────────────────┐
    │ BufEnter    │ après avoir donné le focus à un autre buffer     │
    ├─────────────┼──────────────────────────────────────────────────┤
    │ WinEnter    │ après avoir donné le focus à une autre fenêtre   │
    ├─────────────┼──────────────────────────────────────────────────┤
    │ BufWinEnter │ après qu'un buffer soit affiché dans une fenêtre │
    │             │                                                  │
    │             │ émis même si le buffer est déjà affiché ailleurs │
    └─────────────┴──────────────────────────────────────────────────┘

            Autre façon de voir les choses:

                après qu'ON        entre dans un buffer
                après qu'ON        entre dans une fenêtre
                après qu'UN BUFFER entre dans une fenêtre


    BufWritePre

            Juste avant que le buffer ne soit écrit.


    BufWriteCmd

            Au moment où le buffer doit être écrit.

            C'est à nous d'inclure la commande :write au sein même de l'autocmd.
            On peut donc choisir comment sauvegarder, voire même ne pas sauvegarder du tout
            si certaines conditions ne sont pas remplies.


    CmdUndefined

            Qd une commande utilisateur (donc commençant par une majuscule) est exécutée, mais non définie.

            Ex:

                    augroup test_cmd_undefined
                        au!
                        au CmdUndefined * let g:myvar = expand('<afile>')
                    augroup END

                    :MyUndefinedCommand

            Cette autocmd capture le nom de la commande que l'utilisateur a tenté d'exécuter dans `g:myvar`.


                                               NOTE:

            Si on avait utilisé `<amatch>` au lieu de `<afile>`, il aurait fallu également utiliser
            `fnamemodify()`:

                    au CmdUndefined * let g:myvar = fnamemodify(expand('<amatch>'), ':t')

            … car `<amatch>` ne contient pas juste le nom de la commande, mais aussi le chemin vers le cwd.

                    :echo expand('<amatch>')
                    /home/user/.vim/MyUndefinedCommand~


    CursorHold

            après que le curseur n'ait pas bougé en mode normal
            pendant la durée définie par 'updatetime'

    CompleteDone

            après qu'une complétion ait été réalisée

            MenuPopup n'a rien à voir avec le menu de complétion mais peut-être avec
            le menu contextuel qui s'affiche qd on fait un clic droit dans une fenêtre Vim


    FileType python

            Dès que le type de fichier du buffer courant est détecté comme étant python.

            Se produit qd on charge un buffer pour la 1e fois.
            Raison pour laquelle il se reproduit si on fait :bd puis :b# (reload)


    InsertCharPre

            juste avant l'insertion d'un caractère


                                               NOTE:

            Cet évènement  permet de  changer le  prochain caractère  inséré, en
            modifiant v:char.

            Toutefois, il semble  que v:char soit déjà dans  le typeahead buffer
            qd InsertCharPre se produit.
            En effet, même si on donne le  flag 'i' à feedkeys() pour insérer un
            caractère à taper le plus tôt  possible dans le typeahead buffer, il
            semble que ce dernier soit tjrs tapé après v:char.


    QuitPre

            Se produit qd `:q`, `:wq` ou `:qa` est exécutée, avant de décider s'il faut fermer la fenêtre
            courante ou quitter la session Vim.

            Peut être utile pour fermer automatiquement d'autres fenêtre non-essentielles si la fenêtre
            courante est la dernière importante.


    SourceCmd

            Qd un fichier doit être sourcé.

            C'est à nous d'inclure la commande `:source` au sein même de l'autocmd.
            On peut donc choisir comment sourcer, voire même ne pas sourcer du tout
            si certaines conditions ne sont pas remplies.

            Plus généralement, tous les évènements dont le nom suit le pattern `*Cmd`
            ont en commun le fait de laisser la responsabilité de l'écriture/lecture/sourcage
            d'un fichier à l'utilisateur.


    TerminalOpen  (Vim)
    TermOpen      (Neovim)

            Qd un terminal est ouvert.


Pour une liste exhaustive: :h autocmd-events

# Patterns

Exemples de pattern (qd il match un fichier):

            *                 n'importe quel fichier

            *.txt             n'importe quel fichier texte

            [^l]*             n'importe quel fichier dont le nom ne commence pas par `l`

                              [^l] matche n'importe quel caractère différent d'un `l`.
                              * matche n'importe quelle séquence de caractères.
                              * n'est pas un quantificateur, il est utilisé pour faire du globbing,
                              comme dans le shell qd on tape `$ ls foo*`.

            *.{c,cpp,h,py}    type de fichier c, cpp, h, et py

            {.,}tmux.conf     `tmux.conf` ou `.tmux.conf`

                              ce qui est intéressant ici, est la syntaxe:

                                    {x,}
                                    " le caractère `x` 0 ou une fois

                              Elle permet d'émuler le quantificateur `?` dans une regex.

            /etc/*.conf       n'importe quel fichier de configuration sous le dossier /etc
                                Le fichier peut se situer n'importe où sous /etc,
                                pas forcément à la racine.

            <buffer>          le buffer courant
                                Il s'agit d'un pattern spécial permettant de limiter la portée
                                d'une autocmd au buffer courant (:h autocmd-buflocal).

                                               NOTE:

            Un pattern n'est pas toujours comparé à un nom de fichier.
            Pour savoir à quoi il est comparé, se référer à l'aide de l'évènement.

# Caractères spéciaux

Au sein de la commande exécutée par une autocmd, on peut utiliser certains caractères spéciaux:

    expand('<afile>')     chemin du fichier courant (qui déclenche l'autocmd) relatif au dossier de travail
    expand('<abuf>')      n° du buffer courant (")
    expand('<amatch>')    match obtenu dans la comparaison par rapport au pattern
                          (what is matched against the autocmd pattern)
                          Qd le pattern est comparé à un nom de fichier:
                                                                        - <amatch> est un chemin absolu
                                                                        - expand('<afile>') == expand('<amatch>:.')

En fait, on peut utiliser ces caractères spéciaux même au sein d'une fonction appelée par une autocmd.
Ex:

    augroup last_entered_file
        autocmd!
        autocmd BufEnter * call MyFunc()
    augroup END

    fu MyFunc() abort
        let g:last_entered_file = expand('<amatch>')
    endfu

# Imbrication

Une autocmd ne  se déclenche que lorsque l'évènement qu'elle  surveille se produit naturellement,
pas  s'il est  la  conséquence  d'une autre  autocmd.   Par défaut,  il  n'y  a pas  d'imbrication
d'autocmds (autocmds do not nest).

IOW, qd la commande exécutée par une autocmd  A déclenche un évènement surveillé par une autre
autocmd B, par défaut Vim n'exécute pas la commande de B. Pour lui forcer la main, il faut ajouter
le flag `nested` juste avant la commande de A.  Exemple:

    autocmd BufNewFile * nested call s:default_extension(expand('<afile>:p'))

            Qd on crée un nouveau fichier, cette autocmd appelle une fonction qui ajoute
            automatiquement une extension si il n'y en a pas (uniquement dans certains dossiers).

            Si elle renomme le fichier, elle crée un nouveau buffer (nouvel évènement `BufNewFile`).
            Certaines autocmd surveillent cet évènement pour configurer correctement le type de fichier.
            Mais, sans le flag `nested` dans la définition de la 1e autocmd, elles ne seront pas
            exécutées en cas de renommage du fichier. Pex, si on tape:

                    $ vim foo

            … et que `s:default_extension()` renomme `foo` en `foo.sh`, le type de fichier devrait être
            `sh`, mais ne le sera pas sans le flag `nested`.

                                               NOTE:

            `:copen`, `:edit` et `:write` sont des commandes qui déclenchent souvent des
            évènements surveillés par des autocmd (BufRead, BufWrite).
            Qd une autocmd exécute `:e` ou `:w`, il est probablement judicieux de lui donner le flag nested.

                                               NOTE:

            Leçon à retenir: si une autocmd ne fonctionne pas alors qu'elle devrait, regarder si l'évènement
            qu'elle surveille est parfois déclenché par une autre autocmd.
            Si c'est le cas, ajouter le flag nested à cette dernière.

# Pratique

    fu ToStartOfChange()
        augroup ToStartOfChange
            au!
            au InsertLeave * exe 'norm! g`[' | exe 'au! ToStartOfChange' | aug! ToStartOfChange
        augroup END
        return 'cw'
    endfu
    nnoremap <expr> c,w ToStartOfChange()

            Mapping custom `c,w` qui change un mot et replace le curseur au début du texte changé
            une fois le changement terminé.


                                               NOTE:

            Ce bout de code illustre comment on peut utiliser une autocmd à usage unique.
            En effet, `| exe 'au! …' | aug! …` supprime l'autocmd dès qu'elle s'est déclenchée.
            Ainsi, elle ne s'exécutera pas pour chaque évènement InsertLeave mais pour chaque évènement
            InsertLeave se produisant juste après que le mapping `c,w` a été tapé.


                                               NOTE:

            Attention, `:autocmd` n'interprète pas un pipe comme une terminaison de commande, mais comme
            faisant partie de son argument.
            Il faut en tenir compte, si on souhaite faire suivre la suppression de l'autocmd avec une autre
            commande:

                    augroup Dummy
                        au!
                        au InsertLeave * cmd1 | au! Dummy | cmd2          ✘
                        au InsertLeave * cmd1 | cmd2 | au! Dummy          ✔
                        au InsertLeave * cmd1 | exe 'au! Dummy' | cmd2    ✔
                    augroup END



    au BufNewFile,BufRead /path/to/dir/* setl filetype=markdown

            Imposer markdown comme type de fichier pour n'importe quel fichier créé dans /path/to/dir.

            Cette cmd illustre qu'il est fréquent d'associer les 2 évènements BufNewFile et BufRead,
            pour surveiller le chargement d'un buffer qu'il soit associé à un fichier ou non.


    au BufWritePre *.{c,cpp,h,py} command

            autocmd se déclenchant pour des fichiers portant des extensions différentes.
            La syntaxe utilisée ici illustre comment ne pas répéter le *. (:h file-pattern pour + d'infos).

            Dans un pattern d'autocmd, il y a certaines similitudes entre les tokens `{}` / `,`
            et `()` / `|` d'une regex en mode très magique:

                    ┌─────────────────┬───────┐
                    │ pattern autocmd │ regex │
                    ├─────────────────┼───────┤
                    │ {}              │ ()    │
                    ├─────────────────┼───────┤
                    │ ,               │ |     │
                    └─────────────────┴───────┘


    augroup my_group
        au!
        au FileType c,shell au! my_group BufEnter,BufWritePre <buffer> call Func()
    augroup END

            Cette autocmd appelle automatiquement Func() pour un  buffer dont le type de fichier est
            C ou  shell ET qui est  sur le point d'être  écrit ou qu'on vient  d'afficher dans une
            fenêtre.

            Elle illustre comment  une autocmd en appelant une autre  permet de simuler l'opérateur
            logique ET  entre 2 évènements. En  temps normal, les évènements  sont reliés entre
            eux via un OU.

            Le pattern spécial <buffer> passé à la 2e autocmd est nécessaire pour que sa portée
            soit limitée au  buffer courant. Sans lui, à  partir du moment où un  fichier de type
            C/shell aurait été  détecté pendant la session, Func() serait  appelée ensuite pour
            n'importe quel type de buffer (python, markdown …).

            La 1e  instruction au! empêche la  duplication de l'autocmd lorsqu'on  source plusieurs
            fois le fichier où  est défini l'autocmd. Mais elle ne protège  pas de la duplication
            de la 2e autocmd, à chaque fois  que l'évènement `FileType c,shell` se reproduit pour
            un même buffer.  Ceci se produit, par  exemple, après un :bd suivi  d'un :b# (reload).
            Pour cette raison, il faut vider my_group une 2e fois (au! my_group).


    augroup my_group
        au!
        au BufEnter,BufWritePre * if index(['c', 'shell'], &ft) >= 0 | call MyFunc() | endif
    augroup END

            Cette autocmd fait la même chose que la précédente, mais la syntaxe est beaucoup plus simple
            à comprendre.  À préférer.


                               ┌─ le pipe est écrit avant la prochaine commande Ex`:aug`
                               │
    augroup mine | au! BufRead | augroup END               ✔
    augroup mine | au BufRead * set tw=70 | augroup END    ✘
                                          │
                                          └─ le pipe est écrit après la prochaine commande Ex `:set`

            L'instruction `:au` ne peut être suivie d'une autre commande Ex qu'à condition que celle-ci
            soit précédée d'un pipe.

            IOW, `:au` interprète un pipe différemment selon qu'elle a vue avant lui une commande Ex ou non:

                    ┌────────────────────┬───────────────────────────┐
                    │ au … | cmd1        │ terminaison de commande   │
                    ├────────────────────┼───────────────────────────┤
                    │ au …   cmd1 | cmd2 │ fait partie de l'argument │
                    └────────────────────┴───────────────────────────┘


                                               FIXME:

            J'ai copié cette info de `:h :au`. Mais si c'est vrai, alors la dernière commande,
            dans le code qui suit, devrait fonctionner:

                    augroup mine
                        au!
                        au BufEnter * let g:myvar = 1
                    augroup END

                    au! mine | aug! mine
                               │
                               └─ fonctionne pas: le groupe n'est pas supprimé
                                  on peut le vérifier en exécutant `:au mine`
                                  au lieu de produire une erreur, Vim affiche un augroup vide

            En revanche, cette commande fonctionne:

                    exe 'au! mine' | aug! mine


                                               NOTE:

            Comme pour plein d'autres commandes, on peut empêcher `:au` d'interpréter un pipe comme
            faisant partie de son argument via `:exe`:

                    augroup mine | exe 'au BufRead * set tw=70' | augroup END    ✔


    augroup mine
        au!
                   ┌─ ✘
                   │
        au Event * nested some_cmd | exe 'au! mine' | aug! mine
    augroup END

            Il est déconseillé d'utiliser le flag `nested` dans une autocmd à usage unique.
            En effet, si `some_cmd` réémet `Event`, juste avant que l'autocmd ne soit supprimée,
            alors l'autocmd sera exécutée une 2e fois.

            Mais cette fois-là, la supression de l'autocmd provoquera une erreur car elle n'existe plus.
            On pourrait sans doute utiliser `:sil!`, mais je pense que ce pb met en évidence qch de + profond.
            Une autocmd, dont on n'a besoin que ponctuellement, ne devrait être pas être réappelée.

            Pour un exemple concret chercher la fonction `qf_open_maybe()` dans notre vimrc.


    set verbose=9

            Pratique pour tester des autocmds.
            Vim affiche des messages en temps réel, à chaque fois qu'il exécute une autocmd.

##
# Todo

Document that you can use a regular pattern, and not just a file pattern, as the
pattern of an autocmd.
This allows you to use lookarounds:

From `:h file-pattern`:

> It is possible to use |pattern| items, but they may not work as expected,
> because of the translation done for the above.

See: <https://vi.stackexchange.com/a/19385/17449>

    au BufNewFile  *\(_spec\)\@<!.rb  0r ~/vim/skeleton.rb

---

Document  that the  order  of the  autocmds  in  the output  of  `:au` is  first
alphabetical, then chronological.

That is, the command shows the  autocmds listening to:
`BufDelete`, then `BufEnter`, then `BufHidden`, then `BufLeave`, ...
That doesn't mean that the autocmds listening to `BufHidden` are processed after
the ones listening to `BufEnter`.
It's just that the word `BufHidden` comes after `BufEnter` in the alphabetical order.

OTOH, for a given  event, the autocmds listed in the output  of `:au` are listed
in the order in which they have been  installed (and thus in the order they will
be processed).

