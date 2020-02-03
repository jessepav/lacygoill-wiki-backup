# How to yank all the lines in open folds?

    qaq
    :folddoopen y A

`:folddoopen` and `:folddoclosed` are similar to `:g`.
They allow you to execute a command on  a set of lines; the lines in open folds,
or the lines in closed folds.

---

Don't conflate `:folddoopen` with `:foldopen`.

##
# What does `'foldlevel'` control?

When set to a number, any fold with  a higher level is closed, and any fold with
a lower level is opened.

## Which normal commands can alter its value?

   - `zM`
   - `zm`

   - `zR`
   - `zr`

---

The commands which can open/close a particular fold, do *not* alter `'foldlevel'`:

   - `zA`
   - `zC`
   - `zO`

   - `za`
   - `zc`
   - `zo`

   - `zv`

##
# What are the four fold-related options which are not window-local?

   - `'debug'`
   - `'foldclose'`
   - `'foldopen'`
   - `'foldlevelstart'`

## What do they control?

If `'foldclose'` is set  to `all`, a fold is automatically  closed when you move
the cursor outside of it and its level is higher than `'foldlevel'`.

---

`'foldopen'` specifies which types of commands will make Vim open a closed fold,
when they make the cursor move into one.

Its default value is:

    block,hor,mark,percent,quickfix,search,tag,undo
    │     │   │    │       │        │      │   │
    │     │   │    │       │        │      │   └ undo or redo: "u" and CTRL-R
    │     │   │    │       │        │      └ jumping to a tag: ":ta", CTRL-T, etc.
    │     │   │    │       │        └ search for a pattern: "/", "n", "*", "gd", etc.
    │     │   │    │       └ ":cn", ":crew", ":make", etc.
    │     │   │    └ "%"
    │     │   └ jumping to a mark: "'m", CTRL-O, etc.
    │     └ horizontal movements: "l", "w", "fx", etc.
    └ "(", "{", "[[", "[{", etc.

---

`'foldlevelstart'` sets `'foldlevel'` when starting to edit a buffer in a window.

Some useful values are:

    ┌────┬──────────────────────────────────────────────┐
    │ -1 │ the option is ignored                        │
    ├────┼──────────────────────────────────────────────┤
    │ 0  │ all folds are closed                         │
    ├────┼──────────────────────────────────────────────┤
    │ 1  │ most folds are closed (except level-1 folds) │
    ├────┼──────────────────────────────────────────────┤
    │ 99 │ no fold is closed                            │
    └────┴──────────────────────────────────────────────┘

It can be overridden by a modeline or by an autocmd listening to `BufReadPre`.

---

If `'debug'`  is set  to `msg`,  when Vim encounters  an error  while evaluating
`'fde'`, it gives an error message.
If it has the value `throw`, it will also throws an exception and set `v:errmsg`.

##
# I'm using the `indent` foldmethod.
## For a given line, how to make Vim use the level of indentation of the line above or below?

If this line starts with a particular character, assign it to `'foldignore'`.

Any line starting with the character saved  inside this option will get its fold
level from the next or previous line (the smallest of the two).
Their own indentation level is ignored, hence the option name.
White space is skipped before checking for the character.

##
# From a script, how to fold the lines 12 to 34?

    :12,34fold

`:fold` is the Ex equivalent of the normal command `zf`.

# `'foldopen'` doesn't work for a command I use in my mapping!

It doesn't apply to commands which are used in a mapping.
Rationale: it gives the user more control over the folds.

Use `zv` or `:norm! zv` in your mapping to get the same effect.

##
# Théorie, mappings
## ?

Se déplacer vers:

    ┌────┬───────────────────────────────────────────────────────────────────────┐
    │ [z │ la précédente fin de pli  peu importe son niveau                      │
    ├────┼───────────────────────────────────────────────────────────────────────┤
    │ ]z │ le prochain   début de pli "                                          │
    ├────┼───────────────────────────────────────────────────────────────────────┤
    │ [Z │ le précédent  début de pli de niveau supérieur ou égal au pli courant │
    ├────┼───────────────────────────────────────────────────────────────────────┤
    │ ]Z │ la prochaine  fin de pli   "                                          │
    └────┴───────────────────────────────────────────────────────────────────────┘

Ce sont des mappings custom; par défaut Vim utilise:

   - zj
   - zk
   - [z
   - ]z

---

TODO: Review this answer.  I don't think it's quite correct.

      [Z │ le précédent  début de pli de niveau supérieur ou égal au pli courant │
                                                ^^^^^^^^^^^^^^^^^
                                                strictly lower?

But first, understand how the default commands work.
Test `zj`, `zk`, `[z`, and `]z` with `:norm!`.

Then, consider refactoring our  mappings so that they really do  what we want in
all cases (whether folds are stacked or nested in markdown).

---

When I use the default `zk` command to move to the end of the previous fold, Vim skips some ends of folds!

No, it does not.

You're probably confused by the nesting foldexpr, which we don't use often.

Suppose you have this markdown file while you're using the nesting foldexpr:

    line address  foldcolumn  text
    1             -           # a
    2             |
    3             |           a
    4             |
    5             |-          ## aa
    6             ||
    7             ||          aa
    8             ||
    9             |-          ##
    10            -           # b
    11            |
    12            |           b
    13            |
    14            |-          ## bb
    15            ||
    16            ||          cursor is on this line

You execute `:norm! zk` to move to the previous end of fold.
You probably expect your cursor to jump on line 13, but in reality it jumps on line 9.
line 13 is *not* the end of a fold; it belongs to the level-1 fold starting on line 10.

## ?

Qd on utilise la méthode `'expr'`, voici les règles à retenir:

   - chaque ligne du buffer a un niveau de pliage, positif ou nul

   - l'expression donnée comme valeur à `'fde'` est évaluée dans le contexte:

       * du buffer courant
       * la fenêtre courante
       * la ligne dont l'addresse est `v:lnum`

   - l'évaluation de cette expression détermine le niveau de chaque ligne;
     elle peut prendre pour valeur:

    ┌───────────────┬────────────────────────────────────────────────────────────────────────┐
    │ 0             │ la ligne n'est pas dans un pli                                         │
    ├───────────────┼────────────────────────────────────────────────────────────────────────┤
    │ -1            │ le niveau est indéfini;                                                │
    │               │ Vim doit utiliser le niveau de la ligne voisine la plus proche,        │
    │               │ celle dont le niveau est le plus petit                                 │
    ├───────────────┼────────────────────────────────────────────────────────────────────────┤
    │   1,    2,  … │ la ligne est dans un pli de ce niveau                                  │
    │ '>1', '>2', … │ idem mais en plus la ligne est la 1e       d'un pli                    │
    │ '<1', '<2', … │ idem "                            dernière d'un pli                    │
    ├───────────────┼────────────────────────────────────────────────────────────────────────┤
    │ 'a1', 'a2', … │ [a]jouter/[s]oustraire 1, 2, … au niveau de la ligne précédente,       │
    │ 's1', 's2', … │ et utiliser le résultat pour la ligne courante                         │
    └───────────────┴────────────────────────────────────────────────────────────────────────┘

   - qd une ligne a le même niveau que la suivante, toutes 2 sont rangées dans un même pli

   - qd une ligne a un niveau supérieur à la précédente, elle débute un nouveau pli; ex:

           a
               b
               c
                   d    ← niveau 2, et la précédente a pour niveau 1 = début d'un pli
                   e
               f
           g

     corollaire:
     il n'est pas nécessaire de lui donner pour niveau `'>N'`, `'N'` suffit

   - qd une ligne a un niveau supérieur à la suivante, elle termine le pli
     courant; ex:

           a
               b
               c
                   d
                   e    ← niveau 2, et la suivante a pour niveau 1 = fin d'un pli
               f
           g

     corollaire:
     il n'est pas nécessaire de lui donner pour niveau `'<N'`, `'N'` suffit

   - qd une ligne a un niveau N, toutes les lignes suivantes de niveau supérieur
     sont incluses dans le même pli (jusqu'à atteindre une ligne de niveau
     inférieur)

## ?

    za
    zA

Toggle:

   - le pli courant
   - le pli courant et tous ses parents / enfants

## ?

    zc
    zC

Ferme:

   - le pli courant s'il est ouvert ou son parent s'il est fermé
   - tous les plis dans lequel se trouve le curseur

En répétant `zc`, on peut  fermer toute une hiérarchie de plis.
`za` se contenterait d'ouvrir / fermer le même pli.

## ?

    zd
    zD
    zE

Supprime:

   - le pli contenant la ligne où se trouve le curseur
   - tous les plis contenant la ligne où se trouve le curseur
   - tous les plis du buffer (Eliminate)

Ne fonctionne que si la méthode de pliage est `manual` ou `marker`.

## ?

    zn
    zN
    zi

Modifie l'option `'foldenable'`:

   - désactivaction
   - activation
   - toggling

`'fen'` est très utile pour temporairement désactiver les plis avant de déplacer
une/des ligne(s), via `:move`.
En effet, un bug  introduit dans le patch 7.4.700 a pour effet  de fermer le pli
dans lequel on déplace une ligne.
Ceci peut avoir des effets inattendus sur les commandes suivantes (ex: `norm!  ==`).

## ?

    zm
    zM

Altère la valeur de l'option `'foldlevel'`, en la:

   - décrémentant d'un
   - faisant passer à 0

Les plis dont le niveau est supérieur à `&l:fdl` sont fermés.
Donc, `zm` ferme un peu plus de plis, tandis que `zM` les ferme tous.

## ?

    zr
    zR

Altère la valeur de l'option `'foldlevel'`, en:

   - l'incrémentant d'un
   - la faisant passer à `niveau de plis max`

`zr` ouvre un peu plus de plis, tandis que `zR` les ouvre tous.

## ?

    zo
    zO

Ouvre:

   - un pli           dans lequel se trouve le curseur
   - tous les plis    "

Si le curseur  se trouve dans une  imbrication de plis, `zo` n'ouvre  que le pli
fermé le plus haut dans la hiérarchie.
`zO` ouvre toute la hiérarchie.

##
# Todo
## Document that in VimL, `:eval foldlevel(1)` is a better alternative than `zx`/`zX`.

Because it preserves manually opened/closed folds.

    $ vim -Nu NONE -S <(cat <<'EOF'
        setl fml=0 fdm=expr fde=getline(v:lnum)=~#'^#'?'>1':'='
        %d|for i in range(2) | sil pu=['#', '']+repeat(['x'], 5)+[''] | endfor
        setl fdm=manual
        1d_
        norm! zoGyyp
    EOF
    ) /tmp/file

    " the first fold stays open
    :setl fdm=expr | eval foldlevel(1) | setl fdm=manual

    " the first fold gets closed
    :setl fdm=expr | exe 'norm! zx' | setl fdm=manual

Note that in both commands, the folds get recomputed, which is why you can close
the new third fold by pressing `zc`.

Also,  this  works  because  evaluating  any  fold-related  function  makes  Vim
recompute all folds; it has to, so that the function can give a correct value.

---

Alternatively, you could execute:

    exe winnr()..'windo "'
    setl fdm=manual

Or:

    let [curwin, curbuf] = [win_getid(), bufnr('%')]
    call timer_start(0, {-> winbufnr(curwin) == curbuf && setwinvar(curwin, '&fdm', 'manual')})

Or:

    let view = winsaveview()
    norm! zizi
    setl fdm=manual
    call winrestview(view)

But note that `:eval foldlevel(1)` is the fastest method:

    " open vimrc
    :10000Time eval foldlevel(1)
    0.055 seconds to run ...~

    :10000Time exe winnr()..'windo "'
    0.080 seconds to run ...~

    :10000Time let [g:curwin, g:curbuf] = [win_getid(), bufnr('%')] | call timer_start(0, {-> winbufnr(g:curwin) == g:curbuf && setwinvar(g:curwin, '&fdm', 'manual')})
    0.150 seconds to run ...~

    :10000Time let view = winsaveview() | exe 'norm! zizi' | call winrestview(view)
    0.270 seconds to run ...~

Besides, the fact that `:123windo "` makes Vim recompute folds is not documented.
It would be brittle to rely on such an undocumented feature, because there is no
guarantee that it continues working in the future.

---

Nvim does not support `:eval` atm.
Use a dummy assigment instead; `let _ = foldlevel(1)`.

## Document that a new fold may be automatically closed when folds are recomputed.

And only a new fold; not existing ones.
And even if you use `:eval foldlevel(1)` instead of `zx`.

Find a MWE.
Does the issue depend on some options?

From our vim-fold plugin:

    " MWE:
    "
    "     $ vim -Nu NONE -S <(cat <<'EOF'
    "         setl fml=0 fdm=manual fde=getline(v:lnum)=~#'^#'?'>1':'='
    "         au BufWritePost * setl fdm=expr | eval foldlevel(1) | setl fdm=manual
    "         %d|sil pu=repeat(['x'], 5)|1
    "     EOF
    "     ) /tmp/md.md
    "
    "     " press:  O # Esc :w  (the fold is closed automatically)
    "     " press:  O # Esc :w  (the fold is closed automatically if 'fml' is 0)
    "
    " I think that for the issue to be reproduced, you need to:
    "
    "    - set `'fdl'` to 0 (it is by default)
    "    - modify the buffer so that the expr method detects a *new* fold
    "    - switch from manual to expr

## Document that in some circumstances, Vim has to decide whether a fold should be open or closed.

When you:

   - press `zx` or `zX`
   - load a buffer
   - add new lines which are detected as a new fold

And in those cases, Vim uses the value of `'foldlevel'`.
A fold above this value is closed; and below this value it's opened.
`'foldlevel'`  is   a  window-local  option   which  may  be   initialized  with
`'foldlevelstart'` (global option).

Make sure our understanding is correct.

## Document that disabling folding temporarily may alter the view.

If your code is not supposed to move the cursor, save and restore the view:

    let view = winsaveview()
    let fen_save = &l:fen
    ...
    let &l:fen = fen_save
    call winrestview(view)

Check out our qfl named `fen_save`.
We still have 3 locations where we temporarily disable folding without restoring the view.
Should we restore it?

