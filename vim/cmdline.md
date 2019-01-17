# ?

What must follow `**` in a file pattern? (2 possibilities)

        • nothing
        • a slash

Dans un file pattern `'**'` ne peut être utilisé que:

        • à la fin
        • en étant suivi d'un slash
        • en étant suivi d'un nombre puis d'un slash

          n'importe quoi ✘


# ?

`**` peut être utilisé dans 2 contextes différents.
Celui qu'on  vient de voir: au  sein d'un argument  passé à une commande  Ex qui
attend des noms de fichiers.

Et  un autre:  au sein  de  la valeur  de certaines  options ('path',  'cdpath',
'tags') ou en argument passé à certaines fonctions (`finddir()`, `findfile()`).

L'usage de `**` dans ces 2 contextes est décrit dans:

        :h starstar-wildcard
        :h starstar

Qd `**` est  suivi d'un nombre, ce dernier est  interprété littéralement dans le
1er contexte, et comme un limiteur de “profondeur“ dans le 2e:

        set path=/etc/**2

Tous les sous-dossiers  de `/etc` dont la  profondeur est <=2 sont  ajoutés à la
valeur de 'path'.


        vim /pat/ /etc/**2

`:vim` cherche `pat` dans tous les fichiers de `/etc` tq la fin du 1er composant
dans leur chemin est le caractère `2`.

# ?

finddir({name} [, {path} [, {count}]])

                Find directory {name} in {path}.

                Supports   both  downwards   and  upwards   recursive  directory
                searches.

                See |file-searching| for the syntax of {path}.

                Returns the path of the first found match.

                When  the  found directory  is  below  the current  directory  a
                relative path is returned.

                Otherwise a full path is returned.

                If {path} is omitted or empty then 'path' is used.

                If the optional  {count} is given, find  {count}'s occurrence of
                {name} in {path} instead of the first one.

                When {count} is negative return all the matches in a |List|.

                This is quite similar to the ex-command |:find|.


findfile({name} [, {path} [, {count}]])

                Just like |finddir()|, but find a file instead of a directory.
                Uses 'suffixesadd'.

                Example:

			:echo findfile('tags.vim', '.;')

                Searches from the directory of the current file upwards until it
                finds the file 'tags.vim'.

# ?

    11. File Searching

    The file  searching is currently  used for  the 'path', 'cdpath'  and 'tags'
    options, for `finddir()` and `findfile()`.

    Other commands use |wildcards| which is slightly different.

    There are three different types of searching:

    1) Downward search:

    Downward search uses  the wildcards '*', '**' and  possibly others supported
    by your operating system.
    '*' and '**' are handled inside Vim, so they work on all operating systems.
    Note that "**" only acts as a special  wildcard when it is at the start of a
    name.

    The usage of '*' is quite simple: It matches 0 or more characters.
    In a search pattern this would be ".*".
    Note that the "." is not used for file searching.

    '**' is more sophisticated:

        • It ONLY matches directories

        • It matches up to 30 directories deep by default, so you can use it to
          search an entire directory tree

        • The maximum number of levels matched can be given by appending
          a number to '**'.

            Thus '/usr/**2' can match:

                    /usr
                    /usr/include
                    /usr/include/sys
                    /usr/include/g++
                    /usr/lib
                    /usr/lib/X11
                    ....

        It does NOT match '/usr/include/g++/std' as this would be three levels.

        The allowed  number range is  0 ('**0' is removed)  to 100 If  the given
        number is smaller than 0 it defaults to 30, if it's bigger than 100 then
        100 is used.
        The system  also has  a limit on  the path length,  usually 256  or 1024
        bytes.

        • '**' can only be at the end of the path or be followed by a path
          separator or by a number and a path separator.

    You can combine '*' and '**' in any order:

            /usr/**/sys/*
            /usr/*tory/sys/**
            /usr/**2/sys/*

    2) Upward search:

    Here you can give a directory and  then search the directory tree upward for
    a file.
    You could give stop-directories to limit the upward search.
    The stop-directories are appended to the  path (for the 'path' option) or to
    the filename (for the 'tags' option) with a ';'.
    If you want several stop-directories separate them with ';'.
    If you want no stop-directory ("search  upward till the root directory) just
    use ';'.

            /usr/include/sys;/usr

    will search in:

            /usr/include/sys
            /usr/include
            /usr

    If you  use a relative  path the upward search  is started in  Vim's current
    directory or  in the  directory of  the current file  (if the  relative path
    starts with './' and 'd' is not included in 'cpoptions').

    If Vim's current path is /u/user_x/work/release and you do

            :set path=include;/u/user_x

    and then search for a file with |gf| the file is searched in:

            /u/user_x/work/release/include
            /u/user_x/work/include
            /u/user_x/include

    3) Combined up/downward search:

    If Vim's current path is /u/user_x/work/release and you do

            set path=**;/u/user_x

    and then search for a file with |gf| the file is searched in:

            /u/user_x/work/release/**
            /u/user_x/work/**
            /u/user_x/**

    BE CAREFUL!
    This might consume  a lot of time, as the  search of '/u/user_x/**' includes
    '/u/user_x/work/**' and '/u/user_x/work/release/**'.
    So    '/u/user_x/work/release/**'    is    searched    three    times    and
    '/u/user_x/work/**' is searched twice.

    In the above example you might want to set path to:

            :set path=**,/u/user_x/**

    This searches:

            /u/user_x/work/release/**
            /u/user_x/**

    This searches the same directories, but in a different order.

    Note that completion  for ":find", ":sfind", and ":tabfind"  commands do not
    currently work with 'path'  items that contain a URL or  use the double star
    with depth limiter (/usr/**2) or upward search (;) notations.

# Raccourcis

    ┌────────────┬────────────────────────────────────────────────────────────────────────────────────┐
    │            │ au sein du pager de Vim avancer / reculer:                                         │
    │            │                                                                                    │
    │ j        k │     • d'une ligne                                                                  │
    │ d        u │     • d'un écran                                                                   │
    │ Space    b │     • d'une page                                                                   │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ C-x C-a    │ développe le caractère spécial (glob, %, ...) précédant le curseur                 │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ tab  s-tab │ naviguer entre les différents matchs d'une recherche sans quitter la ligne         │
    │            │ de commande                                                                        │
    │            │                                                                                    │
    │            │ raccourcis customs, ceux d'origine sont c-g et c-t                                 │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ C-n    C-p │ naviguer dans l'historique de commande, ou dans le wildmenu                        │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ C-r C-w    │ insérer le mot qui était sous le curseur avant qu'on passe en mode Ex              │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ C-r C-a    │ insérer le MOT qui était sous le curseur avant qu'on passe en mode Ex              │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ C-r C-f    │ insérer le chemin vers le fichier qui était sous le curseur avant qu'on passe      │
    │            │ en mode Ex fonctionne aussi dans dirvish                                           │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ C-r C-p    │ insérer le chemin développé (via l'option 'path') vers le fichier qui était sous   │
    │            │ le curseur avant qu'on passe en mode Ex                                            │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ q: q/ q?   │ ouvrir la fenêtre de la ligne de commande contenant l'historique des commandes Ex, │
    │            │ ou recherches                                                                      │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ C-c        │ depuis la fenêtre de la ligne de commande, revenir à la ligne de commande          │
    │            │ depuis la ligne de commande, revenir au buffer courant                             │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ C-r :      │ sur la ligne de commande insérer après le curseur la dernière commande tapée       │
    ├────────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ S-Left     │ déplacer le curseur vers le début du mot précédent / suivant                       │
    │ S-Right    │                                                                                    │
    │            │ utile dans une fonction custom utilisée pour retourner des touches à taper         │
    │            │ et qu'on souhaite se déplacer de mots en mots                                      │
    └────────────┴────────────────────────────────────────────────────────────────────────────────────┘

    FIXME:

    Write `vimrc` in this file.
    Position cursor on it.
    Type:
        : C-r C-p
        E447~

    Do the same experiment in `~/.vim/vimrc`.
    It works.

    Why the difference?



                          ┌── hit C-l
                          │
    e ~/.vim/**/vim-sn    →    ~/.vim/plugged/vim-sn
    e ~/.vim/**/vim-sn    →    ~/.vim/plugged/vim-sneak ~/.vim/plugged/vim-snippets
                          │
                          └── hit C-x C-a

            Contrairement à `C-x C-a` qui développe un glob en le remplaçant par
            tous  les  matchs possibles,  C-l  ne  développe  un glob  qu'en  le
            remplaçant par la plus longue partie commune à tous les matchs.


                                               NOTE:

            Si on tente:

                    e ~/.vim/**/*sne  +  C-l

            ... non seulement rien n'est développé mais en plus `**/*sne` est supprimé.
            La raison est ce fichier:

                    ~/.vim/tmp/undo/%home%user%.vim%plugged%vim-sneak%autoload%sneak%hl.vim
                                                                └─┤
                                                                  └ match le `sne` dans le pattern précédent

            À cause de lui, la plus longue partie commune à tous les matchs est:

                    ~/.vim/

            Conclusion:    C-l peut aussi supprimer du texte.


                                               NOTE:

            Il peut être intéressant de combiner C-l et C-d.
            C-l pour  insérer la partie  la plus longue  à tous les  matchs d'un
            pattern, et C-d pour les lister.


    /pat C-l

            Si un  match du pattern est  visible à l'écran, ajoute  le caractère
            qui suit le match courant.

            Ex:

                    utopie bienveillante   buffer
                    /\w*pie\s\w*veilla     ligne de commande

            Dans cet  exemple, si on appuie  sur C-l à répétition,  Vim ajoutera
            `n`, puis `t`, puis `e`.


    :next *C-x C-a
    :next foo bar baz~
    :bd  b*C-x C-a
    :bd bar baz~
    :r %C-x C-a
    :r { set of files whose path begins like the one of the current file }~

            Exemple  de développement  de caractères  spéciaux sur  la ligne  de
            commande de Vim (le dossier de travail contenant les fichiers `foo`,
            `bar` et `baz`).
            Utile qd on veut modifier un chemin vers un fichier avant d'exécuter
            une commande Ex.

#
# How is `**/*.txt` expanded on the command-line? (the expansion can use `*`, but not `**`)

                    *.txt
         +        */*.txt
         +      */*/*.txt
         +    ...
         +  */.../*/*.txt
            ├───────────┘
            │
            └ up to 100 path components

# How is `/usr/inc**/types.h` expanded on the command-line?

                    /usr/inc*/types.h
        +         /usr/inc*/*/types.h
        +       /usr/inc*/*/*/types.h
        +               ...
        +   /usr/inc*/*/.../*/types.h
                 ├───────────┘
                 │
                 └ up to 100 path components


When `**`  is preceded/followed  by non-wildcard characters,  they only  need to
match in the first component of the expansion; not in the (up to 99) next ones.

IOW:

        /usr/inc**/types.h

                ⇔

        /usr/inc*/*/*/.../types.h

                !=

        /usr/inc*/inc*/inc*/.../types.h

#
# How to execute the contents of a register containing an Ex command?

        :@{regname}

What happens  probably, is that when  you press Enter, in  the typeahead buffer,
`@{regname}` is expanded into its contents.

# How to execute the current line assuming it contains an Ex command?

        echom 'hello'
        yy:@"
          │
          └ you need a colon, because the unnamed register doesn't begin with one

        :echom 'hello'
        yy@"
          │
          └ you do NOT need a colon, because the unnamed register already begins with one

# How to execute the current line assuming it contains an Ex command, without altering the "0 register?

        echom 'hello'
        "cyy:@"
         ^
         `c` named register

When you yank into a named register, `"0` is not altered.

#
#
#
