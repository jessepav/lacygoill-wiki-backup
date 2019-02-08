# ?

`C-j` (or a NUL) and `C-m` don't make a string end prematurely:

    echo "foo \<c-j> bar"
    foo ~
     bar~

In an `<expr>` mapping, it depends:

    " ✔
    fu! Func(str)
        return ''
    endfu
    nno <expr> cd Func('foo <c-j> bar')
    norm cd

    " ✔
    fu! Func(str)
        return ''
    endfu
    nno <expr> cd ':call ' . Func('foo <c-j> bar')
    norm cd

    " ✘
    fu! Func(str)
        return a:str
    endfu
    nno <expr> cd ':call ' . Func('foo <c-j> bar')
    norm cd

However, they *can* in a regular mapping:

    fu! Func(str)
        echo a:str
    endfu
    nno cd :call Func('foo <c-j> bar')<cr>
    norm cd
    E115: Missing quote: 'foo ~

This  is probably  because  the keys  in  the  rhs are  processed  while on  the
command-line; and on  the command-line, when `C-j` or `C-m`  is pressed, it ends
the command.

# ?

:h index           key sequences mapped by default
:h key-notation    notation for keys

http://vimcasts.org/blog/2014/02/follow-my-leader/
https://vimeo.com/85343734

You could want to create 3 types of `{lhs}`:

        - one calling a function or command
        - one calling an operator
        - an object

You could divide the keys on the keyboard in 4 categories:

        - motion      ' ` # $ % ^ *  ( ) 0 _ - + w W  e E t T { } [ ] f F G h H j k l L , ; | b B n N M ? /

        - command     a A C D i I J K m o O p P q Q r R s S u U v V x X Y Esc ~ @ & : .

        - operator    c d y = < > !

        - prefix      g z Z ' " \ Ctrl [ ]

To build a `{lhs}` which won't override / shadow a default functionality, you can make it begin with a prefix.
E.g.:

        gl (vim-lion), gc (vim-commentary)

Or choose a syntax which doesn't make sense to Vim.
Use an operator then a command. E.g.:

              cx    vim-exchange; exchange the position of 2 text-objects
              ys    vim-surround; surround a text-object with some character

It's an invalid syntax, because an operator only manipulates a text-object or the text covered by a motion.
You can use any command, except `a` and `i` because those are commonly used as a prefix to create text-objects
(`iw`, `ap`, …).

Use an operator than a prefix. E.g.: `cz`, `dgb`

Use 2 operators. E.g.: `cd`, `cu`, `y=`

Note that `op1`+`op2` doesn't make sense only if there's no text-object using `op2` as its `{lhs}`.
If `op2` only uses one character, this is not an issue, because there aren't any operator and text-object
using the same 1-char `{lhs}`. IOW, there's a `c` operator, but there's no `c` object.

En fait, il y a une autre raison: y'a pas d'objet utilisant un seul caractère.

              Dit autrement, il n'existe pas d'objet `c`, `d`, `y`, `=`, `<`, `>`, `!`.
              Pk?
              Car ça violerait la convention qui veut que répéter un opérateur revient à lui passer
              la ligne courante en argument.
              Pex, s'il existait un objet `d`, alors `dd` ne supprimerait plus la ligne courante,
              mais l'objet `d`.

              Qd l'opérateur2 utilise plusieurs caractères, le pb peut se poser (cf `gc`), ou pas (`gl`).

              Pex, vim-commentary crée l'opérateur et l'objet `gc`.
              De fait, on ne pourrait donc pas utiliser `dgc` comme un {lhs}.
              Malgré cela, l'opérateur `gc` peut agir sur la ligne courante via une forme de répétition.
              En effet, une 2e convention veut que lorsqu'un opérateur utilise 2 caractères,
              il peut agir sur la ligne courante si on le répète intégralement (plus possible avec `gc`),
              ou bien si on répète seulement son 2e caractère (`gcc` est tjrs dispo et Tim Pope l'a
              correctement défini).

              En revanche, vim-lion ne crée pas d'objet `gl`, on pourrait donc utiliser `dgl` comme {lhs}.

… ou encore un {lhs} valide mais peu utile car il existe un synonyme:    C-n C-p + - s S …
Pex, dirvish/vinegar remap `-` car `k` fait pratiquement la même chose et est plus utilisé.
sneak remap `s` et `S` car ils sont peut utilisés et `cl`/`cc` sont des synonymes.
`gs` est aussi un bon candidat, car inutile dans l'absolu.

On peut utiliser ces méthodes pour créer non pas un {lhs} mais un nouveau namespace à l'intérieur duquel
on créera des mappings similaires (ex: `co`, `[o`, `]o` dans unimpaired).



Qd on cherche un {lhs} pour un objet, généralement son début suit un des patterns suivants:

            cmd1 + cmd2
            cmd  + opérateur
            cmd  + mouvement
            cmd  + namespace

`cmd1` étant très souvent `i` ou `a`.
En théorie, on pourrait aussi le faire commencer par le {lhs} d'un opérateur (ex: `gc`), mais
parfois ça pourrait introduire du lag (`gcgc` vs `gcgcfoo`) ou un namespace.
Pour des exemples, lire:

        https://github.com/kana/vim-textobj-user/wiki
        https://github.com/wellle/targets.vim



On peut se créer son propre leader via l'astuce suivante:
http://vi.stackexchange.com/a/9711/6960

A priori, `[unite]` pourrait être remplacé par `<Plug>(unite)` ce qui présenterait l'avantage
de ne masquer / outrepasser aucun mapping préexistant.

        nno  [myLeader]a  :echo 'hello'<CR>
        nno  [myLeader]b  :echo 'world'<CR>

        nno  <Plug>(myLeader)a  :echo 'hello'<CR>
        nno  <Plug>(myLeader)b  :echo 'world'<CR>


Certaines commandes normales sont pensées pour être outrepassées:    `gq` ('formatprg'), `=` ('equalprg')
D'autres peuvent être étendues. Pex, `z=` ne fonctionne que si 'spell' est activée.
On pourrait lui faire qch (de similaire) qd l'option est désactivée, comme suggérer des synonymes
du mot sous le curseur.


Vim ne définit aucun mapping contenant des chiffres à l'exception de 3:

        0 C-d    insertion
        g0
        g8
        8g8


Some key sequences can begin with one of 2 symmetrical characters, such as `[`, `]`.
Don't use them to perform completely unrelated actions.
You would lose the symmetry.
Use them to perform reverse operations.

There can even be a set of more than 2 characters, which by default are related in some way.
For example, `<`, `=`, `>` all operate on the level of indentation of some lines.
So, they could be used as prefixes to build 3 mappings, performing 3 custom related operations,
provided by your plugin.


You can check whether a key sequence is already bound to some default action in Vim,
by looking at the output of:

        :echo taglist('^<keys>')
        :echo map(taglist('^<keys>'), 'v:val.name')

        Output example when `<keys>` = `g CTRL-`

                ['g_CTRL-A', 'g_CTRL-G', 'g_CTRL-H', 'g_CTRL-]'

FIXME:
I think the output of `taglist()` is influenced by the current buffer.
Because it must look in tags files, and those are set by a buffer-local option ('tags').
To be checked.

# ?

Read this:

        https://vi.stackexchange.com/a/10284/17449

Useful to better understand the distinction between a:

        - terminal keycode
        - Vim keycode
        - (mapped) key sequence

Hint:

This is a terminal keycode:

        ^[[23~

This is a Vim keycode:

        <S-F1>

This is a mapped key sequence:

        inoremap jk <Esc>:nohl<CR>
                 ^^

Note that a mapped key sequence doesn't make sense outside of a mapping.
'jk' by itself is not a mapped key sequence.
It becomes one if it's used in the lhs of a mapping.

By contrast, `^[[23~` and `<S-F1>` don't any context.
They are terminal/Vim keycodes by themselves.

##
##
# When do I need to use `inputsave()` and `inputrestore()`?

Every time your mapping invokes `input()`.

Exception:

For  some reason,  you  don't  need `inputsave()`  and  `inputrestore()` if  the
remainder of the  mapping (i.e. everything after `input()`) belongs  to the same
sequence of Ex commands separated by bars.

---

        nno  cd  :<c-u>call Func()<cr>bbb
        fu! Func() abort
            call input('>')
        endfu

✘

`input()` consumes `bbb`.

---

        nno  <silent>  cd  :<c-u>call Func()<cr>bbb
        fu! Func() abort
            call input('>')
        endfu

✘

Same issue,  but this time, because  of `<silent>`, you  have to press a  key to
make Vim redraw what's after the prompt  `>`, otherwise you won't see that `bbb`
has been consumed and is written on the command-line.

Theory:

`<silent>` tells Vim to not redraw the command-line while pressing the keys from
the rhs.
And `bbb` belongs to the rhs, so Vim doesn't redraw while pressing `bbb`.
But the first key pressed by the user  to give their input doesn't belong to the
rhs, therefore  Vim redraws the command-line  as soon as the  user starts typing
their input.

---

        nno  cd  :<c-u>call Func()<bar>norm! bbb<cr>
        fu! Func() abort
            call input('> ')
        endfu

✔

`input()` doesn't consume  `bbb`, because `:norm!` belongs to  the same sequence
of Ex commands as `:call Func()`.

##
# My opfunc uses `:s/pat/rep/c`.  It doesn't work!

You may be invoking your opfunc via `:norm!`.
In this case, read this (from `:h :norm`):

>       {commands} should be a complete command.  If
>       {commands} does not finish a command, the last one
>       will be aborted as if <Esc> or <C-C> was typed.

`:s/pat/rep/c` is an unfinished command: it requires the user's input to finish.
So, `:norm!` aborts your `:s/.../c` command.
Use `feedkeys()` instead.

        nno  <key>  :set opfunc=OpFunc<bar>exe 'norm! '.v:count1.'g@_'<cr>
                                                ^
                                                ✘

        nno  <key>  :set opfunc=OpFunc<bar>call feedkeys(v:count1.'g@_', 'int')<cr>
                                                ^
                                                ✔

# My opfunc uses `setline()`, not `:s`.  How to pass it a range when I use a count (e.g. `123g@_`)?

Install a wrapper around your opfunc.
Inside the wrapper, call the opfunc by prefixing `:call` with the range:

                    ┌ consumes the type
                    │
        fu! Wrapper(_)
            '[,']call OpFunc()
        endfu

        fu! OpFunc()
            " use setline()
        endfu

You  can use  the  change marks  because  Vim should  set  them correctly  after
`123g@_` has been executed.

# My opfunc executes several `:echo`.  Only the last message is printed!

I think that Vim redraws automatically before every command printing a message.
This includes sth like `:echo 'msg'` and `:call input('>')`.

I don't know any solution to this  issue, other than printing your messages from
another function invoked before/after your opfunc, but not directly from it:

        nno cd :set opfunc=Func<cr>g@_
        fu! Func(_)
            call FuncA()
        endfu
        fu! FuncA() abort
            echo 'foo'
            echo 'bar'
        endfu
        " ✘
        " press `cd`
        " bar~

        nno cd :set opfunc=Func<cr>g@_:call FuncA()<cr>
        fu! Func(_)
        endfu
        fu! FuncA() abort
            echo 'foo'
            echo 'bar'
        endfu
        " ✔
        " press `cd`
        " foo~
        " bar~

---

Note that the same issue exists for timers:

        " ✔
        :echo 'foo' | echo 'bar'
        foo~
        bar~

        " ✘
        :call timer_start(0, {-> execute('echo "foo" | echo "bar"', '')})
        bar~

And for autocmds:

    augroup test_echo
        au!
        au CursorHold * call Func() | au! test_echo
    augroup END
    fu! Func()
        echo 'foo'
        echo 'bar'
    endfu

##
# One of my custom normal command is not repeatable with the dot command!  Why?

`.` only repeats the LAST default normal command.
So, if your  custom command executes several commands, `.`  will only repeat the
last one instead of the whole sequence.

# Do I need to make a custom operator repeatable with `.`?

No.

By default, `.` repeats the last operator AND the last text-object.
So, there's no need to use `repeat#set()` or any other hack.

##
# Why should I avoid using `repeat#set()` to make it repeatable?

1) The repetition doesn't always work as expected after an undo:

        https://github.com/tpope/vim-repeat/issues/63

2) And sometimes, `.` repeats an old custom command.

These bugs and [tpope's comment][1] indicate that `repeat#set()` is
a brittle hack, which should be avoided whenever possible.

---

1) You can check it doesn't work correctly after an undo with `vim-easy-align`:

        gaip*|
        u
        .

The dot  command should  repeat the  alignment of  all the  bars in  the current
paragraph.
Instead, it asks again for the characters to align.

The same kind of issue applied to `g SPC` (break line).
After an undo, the repetition didn't break the line, and did something else:
delete the line, put an empty line below...

---

2) In the past, I found another issue with `] SPC`:

        1. ] SPC
        2. dd
        3. `.` to repeat `dd`

        Vim repeated `] SPC`, instead of `dd`~

I found a solution, which was to add this line at the end of our custom function
(after invoking `repeat#set()`):

        do <nomodeline> CursorMoved

# I still want to make it repeatable with `repeat#set()`! How to do it?

        nno  <lhs>  <rhs>:call repeat#set('<lhs>')<cr>

Or:

        nmap          <lhs>                  <plug>(named_mapping)
        nno <silent>  <plug>(named_mapping)  :cmd1<bar>cmd2...<bar>call repeat#set("\<plug>(named_mapping)")<cr>

Or:

        nmap          <lhs>                  <plug>(named_mapping)
        nno <silent>  <plug>(named_mapping)  :cmd1<bar>cmd2...<bar>call Func()<cr>

        fu! Func()
            ...
            sil! call repeat#set("\<plug>(named_mapping)")
            "  ^
            " Sometimes, you may not have the plugin, or it may be temporarily disabled.
            " In this case, the function won't exist.
        endfu

# I want `.` to repeat my commands with the same count I used initially! How to do it?

`repeat#set()` accepts a 2nd optional argument.
Use it to pass `v:count1`.

# My mapping is in visual mode, not normal! How to adapt the code?

In the previous code, replace:

        - `:nmap` with `:xmap`
        - `:nnoremap` with `:noremap`
                             ^
                             != nnoremap

# Are there any pitfalls to avoid?

Yes, two.

1) Don't use `:xnoremap` in your 2nd mapping, use `:noremap` instead.

`repeat.vim` remaps the dot command, to make it type the contents of some
variables updated via some autocmds.
But it remaps the dot command only in normal mode, not in visual mode.

As a result, your 2nd mapping (<plug> → ...) need to cover both modes:

        - visual    when you'll press the `{lhs}` initially
        - normal    when you'll press `.`

---

2) Don't  reselect  the visual  selection  with  `gv` at  the  end  of your  custom
commands.
Otherwise, before being able  to press `.`, you would need  to press `Escape` to
get back to normal mode.

##
# What's a “pseudo operator”?

The term is not used in the help.
I use it to refer to an operator to which the same text-object is always passed.
Such an operator can be useful to make a custom command repeatable.

# When I implement a custom operator, I often hesitate between `g@_` and `g@l`.  Which one should I use?

If you're implementing a non-pseudo operator, use `g@_`.
For a pseudo-operator, use `g@l`, unless:

        - it needs to refer to the change marks
          and
        - it doesn't care about the column position of the cursor

---

Rationale:

If your custom operator is a pseudo one, and you implemented it like this:

        nno  <key>  :<c-u>set opfunc=MyOp<cr>g@_
                                               ^
                                               ✘

The `_` motion will make the cursor jump at the beginning of the line, which you
probably don't want.
You can avoid the jump by replacing the motion `_` with `l`.


If your custom operator is a non-pseudo operator, and you implemented like this:

        nno  <key>       :set opfunc=MyOp<cr>g@
        xno  <key>       :call MyOp('vis')<cr>
        nno  <key><key>  :set opfunc=MyOp<bar>exe 'norm! '.v:count1.'g@l'<cr>
                                                                       ^
                                                                       ✘

The `l` motion will  prevent Vim from setting the change marks  on the lines you
want to change, when you press `123<key><key>`.
So,  `MyOp()`  will  need  to  make   a  distinction:  have  I  been  called  by
`<key>{text-object|motion}`, or by `123<key><key>`?

In the first case, it will have to use the change marks.
In the second case, it will have to use the range `.,. +(v:count1 -1)`.

This introduces unneeded complexity...
So, replace the `l` motion with `_`.

# When should I use `g@_` to implement a pseudo-operator?

When two conditions are satisfied.

1. The commands executed by your function make the cursor jump (e.g. `:s`).

Note that `:keepj`  doesn't prevent the cursor from jumping,  it merely prevents
an entry from being added to the jumplist.

2. You prefer to use this range (for better readability):

        line("'[").','.line("']")

Instead of:

        '.,.+'.(v:count1 - 1)

Currently, the only place where these conditions are satisfied is in:

        ~/.vim/plugged/vim-par/plugin/par.vim:98
        /gqs

##
# How to tweak the behavior of a default operator?

Create a wrapper around it.

Example with the `gq` operator:

        nno <silent>  gq   :<c-u>set opfunc=<sid>gq<cr>g@
        nno <silent>  gqq  :<c-u>set opfunc=<sid>gq<bar>exe 'norm! '.v:count1.'g@_'<cr>
        xno <silent>  gq   :<c-u>call <sid>gq('vis')<cr>

        fu! s:gq()
            " tweak some setting which alters the behavior of `gq`
            ...
            " execute the default `gq`
            if a:type is# 'vis'
                norm! '<V'>gq
            else
                norm! '[gq']
            endif
        endfu

# My custom operator works. But when I press `.`, it's not repeated!  Why?

If the  function implementing  your operator calls  another operator  during its
execution, `.` will repeat the latter.

Example:

        nno <silent>  \d  :<c-u>set opfunc=<sid>duplicate_and_comment<cr>g@

        fu! s:duplicate_and_comment(type)
            norm! '[y']

            " norm gc']     ✘
            ']Commentary    ✔

            norm! ']p
        endfu

Here, the normal command:

        norm gc']

... would cause an issue, because it invokes the operator `gc`.
So, after  pressing `\dip`  (duplicate and comment  inside paragraph),  `.` will
repeat `gc']` instead of `\dip`.

# How to fix it?

1) Restore `'opfunc'` correctly.

2) Or better, don't use a a second operator B inside an operator A:
   call the function implementing B via an Ex command.

In the previous example, we use `:Commentary`.

Using an Ex  command is better, because resetting `'opfunc'`  inside an operator
function feels clumsy.
Besides, it creates a bad repetition (DRY,  DIE): if one day you change the name
of your operator function, you'll also need to remember to change it on the line
where you restore `'opfunc'`.

##
##
##
# Tricks

Use `<C-c>` instead of `<Esc>` in a mapping in insert mode, if you don't want to
trigger InsertLeave.

# Arguments
## <expr>

    nno <silent> <expr> {lhs} MyFunc()

            définit un mapping qui à {lhs} associe la sortie de MyFunc()

            La sortie de MyFunc() sera interprétée comme une succession de frappes au clavier
            au même titre qu'un {rhs} explicite.

            Permet de définir un mapping dynamique. Ex: on veut insérer le caractère 'a' lorsque
            la ligne est vide, 'b' autrement.

                                               NOTE:

            - À la place de MyFunc(), on peut écrire directement une expression.

            - Si on écrit directement une expression, il faut:

                * encadrer avec des quotes ce qu'on veut voir taper
                * laisser tel quel ce qu'on veut voir évaluer

            - Si à la place de MyFunc(), on écrit une expression conditionnelle utilisant l'opérateur
              conditionnel `?:`,
              et qu'on veut que le {lhs} ne produise rien lorsque le test réussit/échoue il faut utiliser
              la chaine vide '', ex:    test ? val : ''

            - :nnoremap ne développe le {rhs} qu'une seule fois, au moment où le fichier qui définit
              le mapping est sourcé.
              Après ça, :nnoremap ne joue plus aucun rôle, c'est Vim qui exécute et évalue le rhs d'un mapping.
              Cela implique que si la sortie de MyFunc() contient des caractères de contrôle,
              pex C-g ou C-r, il faut absolument les échapper pour que Vim (et non pas :nnoremap)
              les traduise correctement (et non littéralement) au moment où le lhs sera frappé.

            À retenir: il n'y a jamais besoin d'écrire \<cr> ou \<C-G> ou \<C-R> dans un mapping.


    ┌─────────────────────────┬────────────────────────────────────────────────────────────┐
    │ ✘                       │ ✔                                                          │
    ├─────────────────────────┼────────────────────────────────────────────────────────────┤
    │ nno <expr> <key> Func() │ nno         <Plug>(open_line)    :call append('.', '')<cr> │
    │                         │ nno         <Plug>(abc)          abc                       │
    │ fu! Func()              │                                                            │
    │ call append('.', '')    │ nmap <expr> <key>                Func()                    │
    │     return 'abc'        │                                                            │
    │ endfu                   │ fu! Func()                                                 │
    │                         │     return "\<Plug>(open_line)\<Plug>(abc)"                │
    │                         │ endfu                                                      │
    └─────────────────────────┴────────────────────────────────────────────────────────────┘


            Le mapping de gauche tente de remap `<key>` à `abc`, tout en ouvrant une nouvelle ligne:

                    call append('.', '')

            Ça ne fonctionnera pas et soulèvera l'erreur E523.

            En effet, à l'intérieur d'une fonction qui doit retourner des touches à taper, certaines
            restrictions s'imposent.
            Elles sont décrites dans `:h :map-expression` et `:h textlock`.
            Parmi elles on trouve l'interdiction de modifier le texte du buffer.

            La restriction n'existerait pas si on n'utilisait pas `<expr>`.
            Si on veut absolument utiliser `<expr>` ET changer le buffer, il faut que le changement
            soit réalisé par les touches retournées par la fonction.


                                               NOTE:

            Si on tente d'afficher un message dans `Func()`, le curseur semble rester figé sur la ligne
            de commande. Il se débloque une fois qu'on agit, via un mouvement pex, ou que qch se produit
            automatiquement, comme une sauvegarde (:checktime, :update).

            De plus, si on tente d'appliquer un hl, via `matchadd()` pex, il n'est pas
            visible immédiatement. Là encore, il faut pex bouger le curseur.

            Le pb vient sans doute du fait que lorsque le texte est verrouillé, l'écran n'est plus
            redessiné.

            Utiliser un 2e niveau de mappings permet également de résoudre ce genre de problèmes.

                    ┌──────────────────────┬──────────────────────────────────────────────┐
                    │ ✘                    │ ✔                                            │
                    ├──────────────────────┼──────────────────────────────────────────────┤
                    │ nno <expr> cd Func() │ nmap <expr>  cd            FuncA()           │
                    │                      │ nno          <plug>(plug)  :call FuncB()<cr> │
                    │ fu! Func()           │                                              │
                    │     echo 'hello'     │ fu! FuncA()                                  │
                    │     return ''        │     return "\<plug>(plug)"                   │
                    │ endfu                │ endfu                                        │
                    │                      │                                              │
                    │                      │ fu! FuncB()                                  │
                    │                      │     echo 'hello'                             │
                    │                      │ endfu                                        │
                    └──────────────────────┴──────────────────────────────────────────────┘


    noremap <expr> <key>    ':<c-u>call MyFunc(' . string(mode()) . ')<cr>'
    fu! MyFunc(mode)
        echo 'This function was called from ' . a:mode . ' mode'
    endfu

            Ce bout de code illustre une autre utilisation possible de l'argument <expr>.
            Il permet d'évaluer mode() avant que le {rhs} d'un mapping ne soit exécuté, ce qui permet de passer à
            une fonction le mode depuis lequel elle a été appelée.

                                               NOTE:

            On n'a pas forcément besoin que `mode()` soit directement au sein du {rhs}.
            On peut aussi l'évaluer au sein de `MyFunc()`.
            Sa valeur sera tjrs juste grâce à l'argument `<expr>`.
            Pour un autre exemple d'utilisation, voir:

            https://github.com/kana/vim-niceblock/blob/master/doc/niceblock.txt


    cmap <F7> <C-\>e escape(getcmdline(), ' \')<cr>

            <F7> échappe tous les espaces et les backslash sur la ligne de commande

            L'espace entre <C-\>e et la fonction escape() n'est pas nécessaire, il rend juste le code
            un peu + lisible.

            <C-\>e est une commande système permettant de  remplacer toute la ligne de commande par
            l'évaluation d'une expression.

            Elle est particulièrement utile dans le  {rhs} d'un mapping :cmap ou d'une abréviation
            :cnoreabbrev.

                                               NOTE:

            <expr> est + puissant pour 2 raisons:

                - il permet de remplacer toute ou partie de la ligne de commande (C-\ e seulement tout)

                - il permet de simuler des frappes au clavier et donc d'effectuer des actions sur la
                  ligne de commande contrairement à `C-\ e` qui ne peut qu'insérer des caractères

            Ex: on peut demander  à appuyer sur la touche '<Up>' pour  rappeler le précédent item
            dans l'historique. On peut  aussi directement se déplacer sur la  ligne de commande via
            des  '<Left>', '<Right>'.  Tandis qu'avec  C-\  e, le  seul  moyen de  se déplacer  est
            d'envelopper l'expression dans une fonction  custom qui appellera `setcmdpos()` avant de
            retourner le contenu de la nouvelle ligne de commande.


                                               NOTE:

            Toutefois C-\ e est spécial.

            Dans un mapping, <expr>, <C-R>=, et :exe ajoute du texte.
            C-\ e n'est dispo qu'en mode ligne de commande, et ne se contente pas d'ajouter du texte.
            Il revient en arrière pour analyser tout ce qu'on a tapé sur la ligne de commande.
            Aucun autre mapping/argument/commande ne permet un retour en arrière.
            On peut simuler C-\ e via <expr> en ajoutant au début du {rhs}: '<c-e><c-u>'
            Mais c'est plus moche.


    cnorea <expr> e               getcmdtype() ==# ':' && getcmdpos() == 2 ? 'E'  : 'e'
    cnorea        e         <C-R>=getcmdtype() ==# ':' && getcmdpos() == 1 ? 'E'  : 'e'<cr>
    cno    <expr> e<space>        getcmdtype() ==# ':' && getcmdpos() == 1 ? 'E ' : 'e '
    cno           e                                                           E

            Ces 4 commandes ont pour but de remplacer automatiquement la commande `:e` par `:E`.

            La 1e syntaxe est la meilleure car:

              - développement que lorsque l'abréviation est seule (pas à la fin d'un mot)
              - développement qu'après un trigger (caractère non keyword, pex espace ou C-])

            La 2e syntaxe est bien mais plus verbeuse.

            La 3e syntaxe n'est pas bonne car:

              - elle n'est pas développée à la fin d'un mot
              - on perd le trigger C-]
              - l'espace doit être tapé avant le timeout; avec une abréviation, pas de timeout.

            La 4e syntaxe est  la pire car le développement est effectué  n'importe où (en début
            de mot, à la fin, au milieu ...).


                                               NOTE:

            Dans un mapping, on ne devrait pas utiliser l'argument <expr> si le {rhs} contient une commande Ex.
            Pk?
            Esthétiquement, voir des ':', "\r" fait moche (et rend le code un peu plus long).
            Préférer:

                - <C-r>=                    pour insérer l'évaluation d'une expression

                - exe test ? cmd1 : cmd2    pour évaluer et exécuter une expression dont le résultat
                                            est une commande Ex

                - <C-\>e                    pour remplacer la ligne de commande par l'évaluation d'une expression

            Exception: qd la commande Ex appelle un input(), et que d'autres commandes suivent,
            <expr> empêche ce dernier de consommer les caractères de ces dernières.

## <plug>

    fu! Reminder(cmd)
        " erase the input before displaying next message
        redraw
        echohl WarningMsg | echo '['.a:cmd.'] was equivalent' | echohl NONE
    endfu

    nno <silent> <plug>(my_reminder)  :call Reminder(input(''))<cr>

                                                         ┌ appelle la fonction
                                                         │    ┌──── passe-lui cet argument
                                                         │    │   ┌ termine/valide la saisie
                                       ┌─────────────────┤┌───┤┌──┤
    cnorea <expr> vs    'vs'.feedkeys('<plug>(my_reminder)C-w v<cr>')[1]
    cnorea <expr> sp    'sp'.feedkeys('<plug>(my_reminder)C-w s<cr>')[1]

            Ce snippet illustre qu'on  peut passer un argument arbitraire à  une fonction, même si
            elle est appelée depuis un mapping <plug>.

            Ce qui peut étonner, c'est d'utiliser `input()`,  qui en tant normal est utilisée pour
            permettre à l'utilisateur de saisir un texte de son choix.

            Ici, son usage est détourné.
            Pour mieux comprendre, revenons à `<plug>(...)`.
            Pk utiliser ce genre de mapping? Il peut y avoir plusieurs raisons:

                    - fournit une abstraction simple, et facile à manipuler

                    - utile pour exécuter une fonction via `feedkeys()`
                      (ex: vim-repeat)

                    - permet d'appeler une fonction locale à un script depuis un autre script
                      (<plug>(...) est une forme d'interface publique)

            Mais `<plug>(...)`  peut poser  un pb. Si  on doit  passer un  argument à  la fonction,
            comment  faire?  On  pourrait  créer  un mapping  `<plug>(...)`  par valeur  d'argument
            valide, mais il peut y en avoir beaucoup.

            La solution est décomposable en 2 étapes:

                    1. écrire notre argument dans le typeahead buffer juste après `<plug>(...)`

                    2. utiliser `input('')` au sein de la fonction invoquée par `<plug>(...)`,
                       pour lui demander de consommer l'argument

            Analogie:

            Étape 1 = jeter des graines de pigeons sur le sol
            Étape 2 = attirer l'attention des pigeons pour qu'il les mange

            Toute  la raison  d'être de  `input('')` est  de forcer  la fonction  à consommer  les
            touches  qui  suivent `<plug>(...)`. Sans  elle,  la  fonction  les ignorerait,  et  Vim
            taperait l'argument en mode  normal (ou n'importe quel autre mode:  celui dans lequel on
            est).


                                               NOTE:

            C'est ce genre de mécanisme que vim-surround utilise dans un mapping tq `ds(`.
            Le plugin installe un mapping qui:

                    - utilise `ds` comme `lhs`
                    - demande à l'utilisateur de fournir un caractère (via `getchar()`)
                    - appelle une fonction en lui passant ce caractère


                                               NOTE:

            On aurait pu déplacer `input()` au sein même de `Reminder()`:

                    fu! Reminder()
                        let cmd = input('')
                        redraw
                        echohl WarningMsg | echo '['.cmd.'] was equivalent' | echohl NONE
                    endfu

                    nno <silent> <plug>(my_reminder)  :call Reminder()<cr>

                    cnorea <expr> vs    'vs'.feedkeys("<plug>(my_reminder)C-w v<cr>")[1]
                    cnorea <expr> sp    'sp'.feedkeys("<plug>(my_reminder)C-w s<cr>")[1]

## <script>

    nno    <script>     ,dt                <SID>(FindTopic)dd
    nno                <SID>(FindTopic)    /Topic<cr>

    nno                 dd                 :call Func()<cr>

Ces 3 mappings illustrent l'utilité de  l'argument `<script>` dans une commande de
mapping.
Par  défaut, on  peut  autoriser ou  interdire  le  remap de  tout  le {rhs}  en
utilisant (ou pas) le mot-clé `nore` (nmap vs nnoremap).

Mais, si  on veut  autoriser le  remap d'une partie  du {rhs}  et pas  du reste,
`nore` ne fonctionne pas.
C'est là que `<script>` intervient.
`<script>` ne remap qu'une suite de caractères commençant par `<SID>`.
Il ne peut donc pas tenir compte des mappings définis dans un autre script.
En effet, `<SID>` est automatiquement traduit en un identifiant unique au script
(`<SNR>123_`).
Un mapping défini dans  un autre script ne peut pas  avoir son `{lhs}` identique
au `<SID>` du script courant.

Dans l'exemple  précédent, les 2 premiers  mappings sont définis dans  un script
(plugin pex).
Le 3e est défini dans un autre fichier (vimrc utilisateur pex).

Le  1er  mapping a  besoin  que  `<SID>(FindTopic)`  soit  remap, de  sorte  que
lorsqu'on tape `,dt`, Vim cherche le mot `Topic`.
Le `{rhs}` de  ce mapping se termine  par `dd` car il veut  ensuite supprimer la
ligne où se trouve `Topic`.

Cela pose  un pb,  car l'utilisateur  peut avoir  remap `dd`  pour faire  qch de
totalement différent, comme appeler une fonction custom.
Le pb est cependant résolu par `<script>`  qui n'autorisera pas le remap de `dd`
car il ne commence pas par `<SID>`.

                                     NOTE:

`<script>` a priorité sur le mot-clé `nore`.
On peut donc écrire `nnoremap <script>` ou `nmap <script>` indifféremment.
Toutefois, comme `<script>`  interdit en grande partie tout  remap, on préfèrera
`nnoremap <script>` pour gagner en lisibilité.

                                     NOTE:

Dans la table  des mappings, `<script>` est signalé via  le caractère `&`, juste
avant le `{rhs}`.

                                     NOTE:

On pourrait se passer de `<script>` et utiliser un `<plug>` à la place:

        nmap   ,dt                      <SID>(FindTopic)<Plug>(norecursive_dd)
        nno    <Plug>(norecursive_dd)    dd
        nno    <SID>(FindTopic)          /Topic<cr>

Mais on doit écrire une ligne de code supplémentaire, et on perd en lisibilité.

## <silent>

    cno <silent> <c-a> foo    ✘

            Ne jamais utiliser `<silent>` pour un mapping en mode ligne de commande:

            Ça empêche la ligne de commande d'être redessinée.

## <unique>

    nno <unique> cd :echo 'hello'<cr>

            `<unique>` ne créera le mapping que si aucun autre mapping n'utilise `cd` comme `{lhs}`.

            La vérification portera à la fois sur les mappings globaux et locaux.
            Donc, les 2 cas de figure suivants échoueront:

                    nno                    cd  :echo 'hello'<cr>
                    nno  <buffer><unique>  cd  :echo 'world'<cr>    ✘

                    nno  <buffer>          cd  :echo 'hello'<cr>    ✘
                    nno          <unique>  cd  :echo 'world'<cr>


                                               NOTE:

            Avantage `<unique>`:

                    - peu verbeux

            Inconvénient `<unique>`:

                    - soulève E227 en cas de conflit

            Avantages `mapcheck()`:

                    - vérifie  non seulement que le lhs n'est pas utilisé,
                      mais en plus qu'il ne provoquera pas de lag

                    - `if empty(mapcheck())|...|endif`  ne soulève aucun message d'erreur
                      car le mapping n'est pas installé en cas de conflit

            Inconvénients `mapcheck()`:

                    - verbeux

                    - lent (car il faut une invocation de fonction par mapping)

            Conseils:

                    - n'utiliser aucun des 2 dans `vimrc`, les ftplugins, et plus généralement
                      pour tout mapping local à un buffer

                    - utiliser `<unique>` dans nos plugins privés

                    - utiliser `mapcheck()` dans nos plugins publics

# Commandes

    :map

            affiche la table des mappings

            Juste devant le champ {rhs}, on peut parfois voir un symbole:

                    - *    non récursif
                    - @    local au buffer
                    - &    récursif uniquement au sein du script (attribut <script>)

    :nmap ,

            affiche tous les mappings en mode normal dont le {lhs} commence par une virgule

            Pratique pour trouver un mapping qui n'introduira pas d'ambigüité (cf. mapcheck()).


    :map         {lhs}    {rhs}
    :noremap!    {lhs}    {rhs}

            définit un mapping récursif en mode nvo
            définit un mapping non-récursif en mode ic

            C'est la même commande dans les 2 cas, simplement le bang fait passer du mode nvo à ic,
            et nore de récursif à non-récursif.

    :xunmap {lhs}

            supprimer {lhs}; celui défini pour le mode visuel

            On peut définir plusieurs mappings utilisant un même {lhs} mais réalisant des actions différentes
            suivant le mode dans lequel on se trouve.
            On peut donc aussi limiter la suppression d'un mapping à un mode donné.

                                               NOTE:

            Qd on veut supprimer un mapping local à un buffer, il faut réutiliser l'argument <buffer>:

                    :xunmap <buffer> {lhs}

            Si on ne donne pas l'argument <buffer> à :[...]unmap, cette dernière tentera de supprimer un mapping
            global ayant pour lhs: {lhs}

    :cmapclear

            supprimer TOUS les raccourcis du mode commande

    ino <ESC> <NOP>

            désactive la touche <Escape> en mode insertion
            parfois, il est utile de désactiver un raccourci pour accélérer l'apprentissage d'un nouveau

# lhs

Qd on écrit un plugin, le dossier `autoload/` ne devrait contenir aucun mapping dont le `{lhs}` est
du type `<Plug>(...)`.

Si un mapping, défini dans `plugin/`, doit appeler une fonction à l'intérieur de `autoload/`, il ne peut pas
le faire par l'intermédiaire d'un `<Plug>(...)` qui serait installé dans `autoload/`:

        nno <key>           <Plug>(my_func)                  dans plugin/      ✘
        nno <Plug>(my_func) :call my_script#my_func()<cr>    dans autoload/    ✘

En effet, avant que `autoload/` ne soit chargé, `<Plug>(my_func)` ne sera pas dispo.
Il ne peut pas non plus appeler une fonction locale à un fichier dans `autoload/`.

Il doit donc l'appeler directement, et celle-ci doit avoir un nom global:

        nno <key>           :call my_script#my_func()<cr>    dans plugin/      ✔


Dans :h keycodes, on s'aperçoit que pour des raisons techniques il est impossible pour Vim
de distinguer certaines touches, comme pex C-i et Tab, ou C-m et CR.
Exception: Vim parvient à distinguer BS et C-h (parce qu'en pratique bcp d'OS produisent C-?
qd on appuie sur backspace).
Il faut en tenir compte lors de la création d'un mapping.
Pex, il ne faut pas remap Tab en mode normal, sinon C-i n'avancera plus dans la jumplist.


    :h key-notation

            affiche la notation des touches spéciales


    if empty(mapcheck('<key>', 'n')) && !hasmapto('<Plug>(plugin_some_func)', 'n')
        nno      <key>                       <Plug>(plugin_some_func)
    endif
    nno <silent> <Plug>(plugin_some_func)    :<c-u>call SomeFunc()<cr>

            Définit un mapping appelant `SomeFunc()`.

            À la place de <Plug>(plugin_some_func) on pourrait utiliser autre chose, comme pex SPC x,
            mais dans ce cas on consommerait un mapping existant.
            <Plug> correspond à un keycode qu'il est impossible de taper au clavier, ce faisant on ne
            consomme aucun mapping.

                                               NOTE:

            Quel intérêt de “casser“ un mapping en deux comme cela ?
            Pour le moment, j'en vois 3:

                    - simplification
                    - normalisation
                    - répétition

            La simplification permet à l'utilisateur de manipuler un {rhs} au nom plus évocateur,
            et de masquer la complexité de la fonctionnalité (≈ abstraction):

                    <Plug>(plugin_some_func)

            La normalisation  permet de vérifier  si oui ou non  l'utilisateur a
            déjà  map  une touche  à  la  fonctionnalité  offerte par  le  {rhs}
            (`hasmapto('<plug>(...)')`):

                    nmap <key>    <Plug>(plugin_some_func)

            Enfin, il est ainsi possible de créer un mécanisme qui répète le mapping et qui
            est indépendant du {lhs} choisi par l'utilisateur (voir `mucomplete`).

                                               NOTE:

            Dans les mappings utilisant `<Plug>`, pk écrit-t-on `plugin_some_func`, et non pas
            simplement `some_func`?
            C'est une convention pour s'assurer de ne pas entrer en conflit avec une autre fonction
            de même nom définie dans un autre script. C'est une sorte de namespace.

            Pk l'entourer de parenthèses ?
            Supposons qu'on ait les 2 mappings suivants:

                    nno <Plug>plugin_some_func        :<c-u>call SomeFunc()<cr>
                    nno <Plug>plugin_some_func_bis    :<c-u>call SomeFuncBis()<cr>

            Qd on tapera le mapping développé en `<Plug>plugin_some_func`, Vim attendra &timeout ms
            avant d'appeler `SomeFunc()`, pour laisser le temps à `_bis` d'être tapé et éventuellement
            appeler `SomeFuncBis()`.
            Le pb vient du fait que les {lhs} des 2 mappings `:nno` commencent de la même façon.

            En ajoutant une parenthèse fermante, on s'assure qu'il n'existera jamais 2 mappings
            commençant de la même façon.
            On peut la voir comme un caractère signifiant que le {lhs} est terminé et qu'il n'y a
            plus rien à attendre après.
            La parenthèse ouvrante n'est pas nécessaire, mais on l'ajoute pour gagner en lisibilité.

                                               NOTE:

            Malgré qu'on ait cassé notre mapping en 2 étages, `<c-u>` est tjrs utile.
            Si on frappe accidentellement un nb avant le {lhs}, `:call MyFunc()` recevra tjrs une rangée.
            `<c-u>` permet dans ce cas de l'éliminer.

                                               NOTE:

            Il semble qu'un seul <silent> soit suffisant, pour qu'un enchaînement de mappings
            soit silencieux.
            Généralement, on le met sur le 2e, celui où le <Plug> est à gauche, et dont le {rhs}
            contient le code qui nous intéresse.
            Ce faisant, on s'assure que la mapping sera silencieux, que l'utilisateur est utilisé
            `<silent>` dans le 1er étage du mapping.


Qd l'auteur d'un plugin dispose d'une fonctionnalité dont il pourrait faire profiter ses utilisateurs
via un mapping, s'il veut déranger l'utilisateur un minimum, il y a 3 conditions qu'il pourrait vérifier
avant de l'installer:

    - l'utilisateur a donné son accord

       Généralement, les auteurs de plugin choisissent un système en opt-out
       (les mapping sont installés par défaut).
       Et ils désactivent les mappings qd la valeur d'une variable globale ad hoc est différente de 0.

    - le mapping ne remplacera aucun mapping préexistant, ni n'introduira du lag

    - l'utilisateur n'a pas déjà map la fonctionnalité à une touche


Exemple d'installation d'un mapping vérifiant ces 3 conditions:

            if !exists('g:mappings_disabled') || !g:mappings_disabled
                if empty(mapcheck('<key>', 'n')) && !hasmapto('<Plug>(plugin_some_func)', 'n')
                    nmap <silent> <key> <Plug>(plugin_some_func)
                endif
            endif

# rhs

    nno    {lhs}    :cmd1 <Bar> cmd2<cr>

            définit un mapping qui exécute cmd1 puis (|) cmd2

            Qd le {rhs} inclut un pipe, il faut le remplacer par <Bar>,  autrement la commande de
            mapping l'interprètera comme la fin du mapping et le début d'une nouvelle commande Ex.
            Alternativement, on peut l'échapper \|.



Qd on préfixe un mapping en mode normal avec un compteur, et que le {rhs} est une commande Ex,
le count est traduit en rangée.

Ex:    nno    <key>      :TW<cr>          :TW étant une commande custom qui supprime des trailing whitespace
             5<key>
             :.,.+4TW~

Si la commande Ex n'accepte pas de rangée, il faut inclure dans le {rhs} de son mapping, le keycode <c-u>.
Si la commande Ex est :call, 2 possibilités:

   - la fonction appelée gère elle-même un possible count (v:count1):
     on ajoute <c-u>

   - la fonction appelée ne gère pas un possible count:
     on n'ajoute pas <c-u> pour que la fonction soit appelée v:count1 fois



    ino ,, <lt>CR>

            crée le mapping ,, qui insère la chaîne <cr>

            Sans le <lt>, <cr> serait automatiquement traduit en ^M au moment où vimrc est sourcé.
            <lt> peut être vu comme un moyen de protéger les touches spéciales de toute traduction
            qd vimrc est sourcé.

            Cette traduction automatique n'a pas uniquement lieue au cours du sourcage d'un fichier de conf.
            Il suffit de taper la commande précédente au cours d'une session pour s'en apercevoir.

            Cette traduction automatique n'est pas propre à :inoremap.
            Elle est propre à toute commande qui modifie une table de mapping ou de commande.
            On peut accéder à la table des commandes via:    :com
            À celle des mappings via:                        :map (nvo) :imap :cmap

            Ex:    set <M-p>=                    fonctionne
                                                 car :set ne modifie en rien la table des commandes

                   com! DisMeta set <M-p>=       ne fonctionnera pas qd on voudra l'utiliser
                                                 E518: Unknown option: ð=

                   com! DisMeta set <lt>M-p>=    fonctionnera



Qd le {rhs} d'un mapping en mode normal exécute une suite de commandes et que l'une d'elles échoue,
les commandes qui suivent ne sont pas exécutées. Exemple:

        nno <key>    <c-w>w<c-d><c-w>w

Lorsqu'on a 2 fenêtres, ce mapping est censé:

        1. donner le focus à la fenêtre inactive          C-w w
        2. la scroll vers le bas                          C-d
        3. puis rendre le focus à la fenêtre d'origine    C-w w

La plupart du temps, il fonctionnera comme prévu, sauf si le curseur se trouve déjà tout en bas du
buffer dans la fenêtre alternative. En effet, dans ce cas, C-d échouera et le focus ne sera pas
rendu à la fenêtre d'origine.
Solution:

        nno <key>    :sil! exe "norm! \<lt>c-w>w\<lt>c-d>\<lt>c-w>w"<cr>

`:silent!` (le bang est important) permet de poursuivre l'exécution de la commande `:normal` même si
celle-ci rencontre une erreur.

L'utilisation de `<lt>` est nécessaire pour éviter que Vim ne traduise <c-w> dans la table de mapping
avant que :exe et :norm n'aient pu le faire correctement.
En effet, si on laisse Vim traduire <C-w> en un ^W littéral, au moment où il sera exécuté, il aura
pour effet de supprimer le mot qui précède.

Plus généralement, à chaque fois qu'un caractère de contrôle est dans une chaîne entre double quote,
et que cette dernière est lue par une commande de mapping ou passée en argument à une fonction,
il faut protéger le caractère de contrôle autant de fois que nécessaires via plusieurs <lt> imbriqués.

        Ex:    \<lt>lt>CR>    un CR protégé 2 fois



Qd le {rhs} d'un mapping appelle une fonction locale à un script, il faut la faire précéder de <SID>
qui sera automatiquement développé en qch comme <SNR>123{underscore} lorsque le mapping sera lu et installé.
En effet, qd le mapping sera tapé, il ne sera pas exécuté dans le contexte du script.
En dehors de ce cas de figure, il n'est pas nécessaire de faire précéder le nom d'une fonction ou
d'une variable de <SID> pour pouvoir y accéder. s: suffit du moment qu'on reste dans le contexte du script.



Le {rhs} d'un mapping ne peut pas appeler une variable locale à un script, car au moment où le {lhs}
sera frappé, le contexte ne sera plus celui du script.
Pour accéder à une variable locale à un script depuis un mapping, il faut passer par une fonction ex:

            let s:myvar = 'hello world!'
            fu! s:my_func()
                return s:myvar
            endfu
            nno <key>    :echo <SID>my_func()<cr>



Qd le {rhs} d'un mapping se finit par une commande Ex, il faut la faire suivre de <cr> pour la valider.
Ex:
            nno <silent>    <space>h    :nohlsearch<cr>

Plus généralement, qd le {rhs} d'un mapping inclut une commande Ex (à n'importe quel endroit,
pas forcément à la fin) qu'on souhaite valider, il faut la faire suivre de <cr> pour simuler l'appui
sur la touche entrée.  Ex:

            nno    gb            :ls<cr>:buffer<Space>
            nno    <space>cd    :cd %:p:h<cr>:pwd<cr>

En revanche, un mapping qui ne contient pas de commande Ex n'a pas besoin de se finir par <cr>.
Pk ? Parque le fichier vimrc est un fichier vimscript comme un autre, et à ce titre n'importe quelle
ligne est automatiquement exécutée en étant considérée comme une commande Ex.



Qd le {rhs} d'un mapping inclut la lettre 'q' les frappes qui suivent sont bien exécutées mais pas enregistrées.



Quand on définit un mapping perso dont le {rhs} contient plusieurs commandes normales et qu'on l'utilise
en le préfixant d'un count, le {rhs} n'est pas intégralement répété, seule sa première commande
normale l'est.

Pour définir un mapping pour lequel un count répètera l'intégralité des commandes, on peut passer par
le registre expression, ex:   nnoremap {lhs} @='keystrokes'<cr>

Cela fonctionne car une macro accepte un count. Pex: 10@q rejoue la macro q 10 fois
Il faut encadrer les frappes au clavier avec des quotes, car le registre = attend une expression à évaluer.
Sans les quotes, il va tenter d'évaluer les frappes au clavier comme un nom de variable.
Si on trouve cette solution trop cryptique, on peut la démystifier un peu en testant en mode normal: @='dd'



    nno <key>    m'{do some stuff}``

            mapping exécutant des commandes normales sans perdre la position d'origine du curseur

            m' ajoute la position courante comme dernière entrée dans la jumplist
            `` nous y ramène

            m' n'est nécessaire que si la 1e commande normale n'ajoute pas d'entrée dans la jumplist.
            En effet, si la 1e commande n'ajoute pas d'entrée et qu'on oublie m', `` nous ramènera
            à la dernière entrée qui correspondra à un emplacement + ancien et complètement différent.

            Ne fonctionne que si les autres commandes normales n'ajoutent pas d'entrée dans la jumplist.
            Autrement il faut utiliser une marque alphabétique.



    nno    <key>    :<c-u>exe input('first line: ') ',' input('last line: ') 'copy .'<cr>

            Définit un mapping qui demande le n° d'une  1e ligne (via la fonction input()), le n°
            d'une 2e ligne, puis duplique toutes les lignes entre ces 2 n° sous la ligne courante.

            Une fois l'expression du {rhs} évaluée, le résultat pourrait être pex:

                    :<c-u>5,10copy .<cr>


    nno  cd  :let msg = input('') <bar> echo ' bye'<cr>hello

            Ce mapping stocke la chaîne 'hello' + le texte qu'il nous demande de saisir.
            Puis, il affiche ' world' à la suite de l'ensemble.

            Par exemple, si on saisit ' world', Vim affichera:

                    hello world bye

            ... et `msg` contiendra la chaîne 'hello world'.
            Illustre que `input()` consomme les caractères qui suivent son invocation au sein d'un mapping.



                                               NOTE:

            Pk `input()` consomme `hello` avant `world`?

            Elle est invoquée dès que CR est tapé. Juste après ce dernier vient `hello`.
            Pour que `input()` consomme `hello` après `world`, il faudrait qu'on tape ce dernier plus
            vite que Vim n'insère `hello` dans le typeahead buffer: impossible.


                                               NOTE:

            Pk `input()` ne consomme pas `echo 'bye'`?
            Peut-être car le pipe interdit au mapping  d'écrire ce texte dans le typeahead buffer,
            tant que les commandes précédentes, ici `:let msg = input()`, n'ont pas fini leur travail.

            En tant normal, qd on appuie sur CR pour valider une commande, on est habitué à ce que
            Vim la traite de gauche à droite.
            Mais ce n'est pas une obligation. Ici, le mapping traite le mapping dans l'ordre suivant:

                                       ┌─────────────────────────── 1. écrit un début de commande dans
                                       │                               le typeahead buffer
                                       │
                                       │                          ┌ 2. écrit `CR hello` dans
                                       │                          │    le typeahead buffer
                                       │                          │    ce qui exécute la commande
                                       │                          │    et fait consommer `hello` à `input()`
                    ┌──────────────────┤                  ┌───────┤
                    :let msg = input('') <bar> echo ' bye'<cr>hello
                                               └─────────┤
                                                         └ 3. le mapping attend que `input()` ait
                                                              capturé la saisie de l'utilisateur
                                                              avant d'écrire `echo ' bye' CR` dans
                                                              le typeahead buffer


            En revanche, ici, `input()` consomme `hello CR` AVANT la saisie, et non après:

                    nno  cd  :let msg = input('')<cr>hello<cr>

            Il semble qu'un CR, contrairement à un pipe, n'interdit pas au mapping d'écrire ce qui suit
            dans le typeahead buffer.


    nno <key> :exe b:key_command<cr>      vimrc

    let b:key_command = 'echo "hello"'    ftplugin
    let b:key_command = 'echo "world"'    ...
    ...

            Crée un mapping qui exécute différentes actions suivant le type de fichier.
            La 1e ligne doit être écrite dans le vimrc, les autres dans des ftplugins.


            Exemple avancé:

            nno <silent> <expr> <cr> !empty(&buftype) ?
                                     \ '<cr>' :
                                     \ ':'.getbufvar('%', 'cr_command', 'norm! 80<Bar>').'<cr>'

            Ce mapping remap CR différemment suivant le type de fichiers où l'on se trouve.

                    !empty(&buftype)

            ... condition testant si le buffer est spécial.
            Nécessaire car CR a souvent une fonction unique dans un buffer spécial, qu'il faut préserver.
            Pex dans un buffer `qf`, CR charge l'entrée sous le curseur.

                    getbufvar('%', '...', '...')

            ... on ne peut pas créer la variable pour tous les types de fichiers existants.
            getbufvar() permet de donner une valeur par défaut à la variable `b:cr_command`,
            afin que le mapping n'échoue pas dans les buffers où la variable n'a pas été créée.

# Objets

Le mode operator-pending est le mode dans lequel on se trouve lorsqu'on vient de
taper un opérateur (c,d,y...).
Dans ce  mode, on doit  entrer un objet  : cela peut être  tout ce qui  se situe
entre le curseur et  une destination, auquel cas il suffit de taper  un mvt ; ou
bien tout ce qui se situe entre une  paire de caractères ( ex: accolades = i{ ou
a{ ) On peut créer ses propres objets via la commande :onoremap.


    xno {objet}    {motion}
    ono {objet}    :norm v{objet}<cr>

            définit un nouvel objet dont les caractères sont couverts par {motion}

            Ajouter <silent> pour que les opérations sur l'objet soient silencieuses.

                                               NOTE:

            Il est important de ne pas mettre de bang après la 2e commande :norm pour permettre
            à {objet} d'être remap et développé en le {rhs} du mapping :xnoremap.

                                               NOTE:

            Si le {rhs} du mapping :xno n'est pas un mouvement, mais l'appel à une fonction,
            on peut le réutiliser pour le mapping :ono:

                    xno {objet}  :<c-u>call MyFunc()<cr>
                    ono {objet}  :<c-u>call MyFunc()<cr>

            Si le {rhs} du mapping :xno est un mouvement, pk ne peut-on pas lui-aussi le réutiliser dans :ono?
            Car on est en mode operator-pending. Il faut soit le quitter via <Esc>, soit passer en mode ligne
            de commande (:), pour appeler une fonction (:call) ou exécuter une commande (:norm).
            Le but étant de sélectionner le texte sur lequel doit agir l'opérateur.

                                               NOTE:

            Si on fait commencer le {rhs} du mapping :ono par un escape, non seulement on quitte le mode
            operator-pending pour revenir en mode normal, mais en plus on annule l'opération.
            Ça signifie qu'il faut appeler le bon opérateur soi-même via v:operator à la fin du {rhs},
            une fois que le texte a été sélectionné.

                                               NOTE:

            On pourrait remplacer le mapping :onoremap par celui-ci:

                    :omap <expr> {objet} '<Esc>' . 'v{objet}' . v:operator

                    '<Esc>'       revenir en mode normal
                    v{objet}      sélectionner l'objet
                    v:operator    agir dessus

            Mais la récursivité de :omap, qui est nécessaire pour remap {objet}, affecterait tout le {rhs}
            (et non juste {objet}) et pourrait donc avoir parfois des effets inattendus.
            De plus, v:operator ne semble pas enregistrer un opérateur custom (ex: cs = change surroundings).


    ono <expr>  w   v:operator ==# 'd' ? 'aw' : 'iw'

            Crée l'objet  w qui se  comporte comme 'aw' lorsque  l'opérateur qui
            précède est 'd', 'iw' autrement.

            `v:operator` was first seen here:

                    https://vi.stackexchange.com/a/6518/17449

            The original code was (unnecessarily?) more complex.


    ono Ob) :norm! vib``<cr>
    ono Oe) :norm! vibo``<cr>

            Crée l'objet allant du curseur jusqu'au début / à la fin de la paire de parenthèses
            à l'intérieur desquelles il se situe.

            Mnémotechnique:    Object Beginning parenthesis
                                      Ending    "

            Illustration:

                    Ob)    func1(foo|, func2(), bar);
                                 ^^^

                    Oe)    func1(foo|, func2(), bar);
                                     ^^^^^^^^^^^^^^

            Ceci illustre également que, si on divise un text-object en 2 parties, la position du
            curseur étant la limite entre les 2, on peut cibler ces dernières via 2 autres text-objects.

            Pour ce faire, on utilise le fait que qd on sélectionne visuellement un text-object,
            le curseur se positionne automatiquement sur le dernier caractère de ce dernier.
            Ça crée un saut, une entrée est ajoutée dans la jumplist et la marque '' est posée à l'endroit
            où se trouvait le curseur initialement.

            On peut ainsi “diviser“ le text-object en 2 parties en utilisant la marque ''.

# Opérateurs

Whenever we mention a text-object, a motion is a valid replacement.


                                         ┌ this is what makes Vim prompt us for a text-object
                                         │ and this is what makes Vim set the change marks
                                         │
    nno  <key>  :<c-u>set opfunc=Func<cr>g@

            Mapping implementing a custom operator.

            Once you  provide a text-object  to the  operator, Vim will  set the
            change  marks and  call  `Func()`, passing  to it  the  type of  the
            text-object:

                    'char'     characterwise
                    'line'     linewise
                    'block'    blockwise

            `Func()` must be defined with an argument (typically called `type`).
            The  function  can then  act  upon  the  characters covered  by  the
            text-object via `a:type` and some marks (change or visual).


                                     NOTE:

            `Func()` will  test the type  of the text-object to  determine which
            marks surround it. Then, it will yank it:

                    ┌──────────────────┬─────────────────────────┐
                    │ type             │ command                 │
                    ├──────────────────┼─────────────────────────┤
                    │ characterwise    │ norm! `[v`]y            │
                    ├──────────────────┼─────────────────────────┤
                    │ linewise         │ norm! '[V']y            │
                    ├──────────────────┼─────────────────────────┤
                    │ blockwise        │ exe "norm! `[\<C-v>`]y" │
                    ├──────────────────┼─────────────────────────┤
                    │ visual selection │ norm! gvy               │
                    └──────────────────┴─────────────────────────┘

            Here's an example of blockwise motion:    C-v j


                                     NOTE:

            Why do we use visual mode to yank the text?

                    norm! `[y`]    ✘
                    norm! `[v`]y   ✔

            Because a motion towards a mark  is exclusive, thus the `y` operator
            won't yank  the character which is  the nearest from the  end of the
            buffer.

            OTOH, v`] makes this same  motion inclusive, thus `y` will correctly
            yank all the characters in the text-object.
            On the condition that 'selection' has the value 'inclusive'.


                                               NOTE:

            L'utilisation de l'opérateur visuel (v ou V) altère les marques '<, '>.
            On peut le vérifier avec le plugin vim-exchange:

                    - sélectionner un texte visuellement
                    - taper cxiw   sur un mot en-dehors du texte sélectionné visuellement
                    - taper .      sur un autre mot tjs en-dehors
                    - taper gv     pour faire apparaître la sélection visuelle

            Le texte sélectionné visuellement n'est plus celui d'origine mais le dernier mot sur lequel
            l'opérateur cx a agit.

                                     TODO:

            Should we save/restore the visual marks, in all our plugins?
            Should we yank with noautocmd to prevent our visual ring from saving
            a possible selection?


    nno  <key><key>  :<c-u>set opfunc=Func<bar>exe 'norm! '.v:count1.'g@_'<cr>

            This mapping implements the convention,  which makes an operator act
            on a number of lines when it's repeated.

            Without a count, the operator acts on the current line.

            It defines `Func()` as the function to call, then executes:

                    :norm! {v:count1}g@_

            The `_` motion makes Vim operate on the current line.
            `v:count1` makes Vim operate on several lines, from the current one,
            if the operator was prefixed with a count.


                                               NOTE:

            If the lhs of the operator  implementing the operator uses two keys,
            theoretically, the lhs of the mapping makeing the operator work on a
            number of lines, should repeat the keys twice.

            In practice, another convention allows us to only repeat the last key:

                    cx  →  cxcx    ✔
                    cx  →  cxx     ✔✔


    xno  <key>  :<c-u>call Func('vis')<cr>

    fu! Func(type, ...)
        if a:type is# 'vis'
            " process visual selection
        else
            " process other cases
        endif
    endfu


            Mapping implementing a visual operator.

            We  don't  need  to  execute   `g@`  because  we  already  know  the
            text-object on which we must operate: it's the one surrounded by the
            marks '<, '>.

            However, we need `C-u` so that the function is only called once.
            We could  eliminate `C-u`, if we  gave the `range` attribute  to the
            function.


                                     NOTE:

            Some people  use this  code to  tell the function  that it  has been
            called from visual mode:

                    xno  <key>  :<c-u>call Func(visualmode(), 1)<cr>

                    fu! Func(type, ...)
                        if a:0
                            " process visual selection
                        else
                            " process other cases
                        endif
                    endfu

            We prefer  the version using 'vis',  because it makes the  code more
            readable  and  more  consistent:  we always  inspect  the  value  of
            `a:type`.

            The consistency remains even if we also call the function from an Ex
            command:

                    com! Cmd call Func('Ex', <line1>, <line2>)

                    fu! Func(type, ...)
                        if a:type is# 'Ex'
                            " operate on lines between `a:1` and `a:2`
                        endif
                    endfu


    nno <cr> :MyCom <Bar> repeat#set("<lt>CR>")<cr>

            If the rhs of a mapping contains a CR, you must protect it via <lt>.

            Otherwise, it will  be translated into a literal CR  in the mappings
            table. Then, this literal CR will prematurely validate the command,
            before we have closed the string ("), and the function ( ) ).

# Récursivité

Les mappings récursifs peuvent être parfois complexes à comprendre.
Voici qques exemples, ainsi qu'une description de leur traitement par Vim.

    nmap <expr>  N               FuncA()
    nno  <expr>    <plug>(one)   FuncB()
    nno          ge<plug>(one)  :echo 'world'<cr>

    fu! FuncA()
        return "ge\<plug>(one)"
    endfu

    fu! FuncB()
        echo 'hello'
    endfu

    norm N
    world~

            Qd N est tapé, il n'y a aucune ambigüité, car aucun autre mapping ne commence par N.
            N est donc développé en la sortie de `FuncA()`:    `ge<plug>(one)`

            Le 1er mapping N est récursif, donc Vim cherche à remap tout ou partie du développement.
            Il voit le 3e mapping `ge<plug>(one)`, et redéveloppe donc en `:echo 'world'<cr>`.
            Ce qui affiche la chaîne `world`.


    nmap  <expr>  N              FuncA()
    nno   <expr>   <plug>(one)   FuncB()
    nno           N<plug>(one)  :echo 'world'<cr>

    fu! FuncA()
        return "N\<plug>(one)"
    endfu

    fu! FuncB()
        echo 'hello'
        return ''
    endfu

    call feedkeys('N')
    hello + timeout~
    NOTE: `norm N` ne reproduit pas le timeout, taper N, ou utiliser `feedkeys()`

        Qd N est  frappé, il y a ambigüité,  car Vim ne sait pas si  on tente de
        taper le 1er ou 3e mapping.
        Il attend pour nous laisser le temps de taper `<plug>(one)`, ce que bien
        sûr on ne peut pas faire.
        Après le timeout, il comprend qu'on  tape le 1er mapping, et développe N
        en la sortie de `FuncA()`: `N<plug>(one)`

        Comme le mapping est récursif, Vim cherche à développer davantage.
        Il devrait développer `N<plug>(one)` en `:echo 'world'`, mais ne le fait pas.
        Pk?
        Probablement car le lhs (N) est répété au début du rhs. Extrait de `:h recursive_mapping`:

                If the {rhs} starts with {lhs}, the first character is not mapped
                again (this is Vi compatible).

        Donc, Vim ne veut en aucune manière remap N.
        En revanche, il peut remap le reste `<plug>(one)`, ce qu'il fait en utilisant le 2e mapping.
        Ainsi, il développe `<plug>(one)` en la sortie de `FuncB()`, à savoir rien.
        Mais pendant l'évaluation, il est amené à afficher `hello`.


    nmap <expr> cd              FuncA()
    nmap <expr>   <plug>(one)   FuncB()
    nno         cd<plug>(one)  :echo 'world'<cr>

    fu! FuncA()
        return "cd\<plug>(one)"
    endfu

    fu! FuncB()
        echo 'hello'
        return ''
    endfu

    call feedkeys('cd')
    ∅ + timeout~

            Qd on tape `cd`, il y a ambigüité: 1er ou 3e mapping ?
            Vim attend jusqu'au timeout.
            Puis, il développe `cd` en la sortie de `FuncA()`, `cd<plug>(one)`.

            Le 1er mapping est récursif, donc Vim cherche à remap le développement.
            Il exclut `cd` du remap car il s'agit du lhs qui est répété au début du rhs
            (:h recursive_mapping).
            Il pourrait développer `<plug>(one)` en la sortie de `FuncB()`, mais ne le fait pas.
            Pk?
            Car `cd` est une séquence invalide. Vim abandonne le traitement d'un mapping dès qu'il
            en rencontre une (:h map-errror).


                                               NOTE:

            Le fait que `hello` n'est pas affiché suggère que `cd` est tapé immédiatement, AVANT même
            de développer le <plug>. On peut le vérifier en ajoutant:

                    let g:myvar = 1    dans FuncA()
                    let g:myvar = 2    dans FuncB()

            `echo g:myvar` affichera 1.

            À retenir: Vim n'attend pas d'avoir absolument tout développé pour taper le développement
            d'un mapping récursif. Dès qu'il trouve qch de non-récursif, il le tape.


    nmap cd bcd

            Qd le lhs d'un mapping récursif se répète dans le rhs, en général, le développement
            se répète indéfiniment jusqu'à rencontrer une erreur.
            C'est pourquoi, dans cet exemple, si on tape `cd`, le curseur retourne jusqu'au début du buffer.

            Toutefois, il y a 3 exceptions qui empêchent un développement infini:

                - la répétition a lieu dans un mode différent

                    nmap cd acd
                            │
                            └─ fait passer en mode insertion, mais le mapping travaille en mode normal

                - la répétition se produit au début du rhs

                    nmap ge geb

                - la répétition est le préfixe d'un autre mapping

                    nmap ge   y#geb
                    nno  geb  <nop>

            Pour plus d'infos, lire `:h recursive_mapping`.

# Retardement

    nno <expr> cd Func()
    fu! Func()
        put =42                                         ✘ E523: Not allowed here
        return 'yy'
    endfu

    nno <expr> cd Func()
    fu! Func()
        call timer_start(0, {-> execute('put =42')})    ✔
        return 'yy'
    endfu

    nno <expr> cd Func()
    nno <plug>(put_42) :put =42<cr>
    fu! Func()
        call feedkeys("\<plug>(put_42)")                ✔
        return 'yy'
    endfu

            On peut vouloir retarder l'exécution d'une commande.

            C'est le cas  si elle modifie le  buffer, mais qu'elle doit être  exécutée depuis une
            fonction utilisée  dans le rhs  d'un mapping <expr>; le  texte est verrouillé  tout au
            long du traitement d'une telle fonction.

                    Solution: retarder l'exécution de la commande, jusqu'à ce que le verrouillage soit levé

            On peut utiliser un timer, ou bien invoquer la fonction `feedkeys()`, à laquelle on passera
            en seul argument, un mapping `<plug>(...)`.

            Concernant les flags de feedkeys():

                    - i : qu'on l'utilise ou pas, les touches seront écrites dans le typeahead buffer
                          après celles retournées par Func()

                          En effet, les touches qui ont invoquées Func(), `cd`, sont déjà écrites
                          dans le typeahead buffer. L'évaluation de Func() a simplement pour but
                          de les remplacer. feedkeys() ne peut donc rien écrire avant les touches
                          retournées par Func().

                    - n : pas possible, car on a besoin que `(plug>(...)` soit développé

                    - t : utile qd les touches contiennent des commandes manipulant des plis, l'undo
                          tree, le wildmenu ...


    cnorea <expr> update 'update'.feedkeys(":echo 'hello'\r")[1]         ✔
    cnorea <expr> update 'update'.feedkeys(":echo 'hello'\r", 'i')[1]    ✘

            Le développement d'une abréviation est différent de celui d'un mapping, en raison
            du concept de “trigger“ qui n'existe pas pour un mapping.
            Ce dernier est toujours écrit dans le typeahead buffer AVANT le trigger (Enter, Space).

            Dans cet exemple, on souhaite afficher un message à chaque fois qu'on exécute `:update`:
            Le flag `i` passé à `feedkeys()` *A* une importance (contrairement à l'exemple précédent).
            Au moment où l'abréviation est développée, le CR qui a validé la commande `:ud`
            n'est pas encore écrit dans le typeahead buffer.
            En effet, s'il l'était, une abréviation ne pourrait pas fonctionner correctement:

                    :ud Enter
                    :ud Enter update~
                              │~
                              └─ ✘ tapé en mode normal~

            Donc, avec le flag `i`, qd l'abréviation serait développée, le typeahead buffer
            contiendrait:

                    :ud Enter
                    :update :echo 'hello' Enter Enter    ✘~

            Sans le flag `i`:

                    :ud Enter
                    :update Enter :echo 'hello' Enter    ✔~


                                               NOTE:

            On pourrait sans doute utiliser un timer, mais ça rendrait le code plus verbeux
            qu'avec feedkeys().

##
# Reference

[1]: https://github.com/tpope/vim-repeat/issues/63#issuecomment-390281441

