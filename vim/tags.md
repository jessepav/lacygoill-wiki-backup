# Tag stack / Tag match list

Un tag est un identifiant qui apparaît dans un fichier `tags`.

Il  s'agit d'une  sorte  d'étiquette  permettant de  se  rendre  (sauter) à  une
définition donnée.
Pex, dans un pgm C, chaque nom de fonction peut être utilisé comme un tag.
Pour que  les commandes tq  `:tag` puissent trouver  la définition d'un  tag, le
fichier `tags` doit avoir été généré via un pgm tq ctags:

    $ ctags -R  .

Commande shell qui scanne récursivement le dossier de travail.

Pour se rendre à la définition d'un tag, on peut utiliser:

   - `:tag {ident}`    peu importe où se trouve le curseur
   - `C-]`             le curseur doit se trouver sur l'identifiant désiré

À chaque fois qu'on saute vers une définition, son id est poussé au sommet de la
tag stack.
En revanche, s'il y a plusieurs matchs  possibles pour un id donné, ils viennent
peupler la tag match list.
On  peut naviguer  au sein  de cette  dernière via  les commandes  `:tprevious`,
`:tnext`, `:tfirst`, `:tlast`.

---

    :tags

Afficher la tag stack.

---

    [t
    ]t

Se rendre au précédent / prochain item de la tag match list (mappings custom).

---

    [T
    ]T

Se rendre au 1er / dernier item de la tag match list.

---

    C-]
    :tag [ident]

Se rendre à la  définition du tag sous le curseur ce qui  ajoute un `{ident}` au
sommet de la tag stack.

---

    C-t
    :pop

Revenir à l'étiquette  d'un tag (mot-clé sur lequel on  a fait <kbd>C-]</kbd>) a
pour effet  de retirer un  `{ident}` à la tag  stack on pourrait  aussi utiliser
<kbd>C-o</kbd> (ne retire rien à la tag stack)

Qd on utilise  <kbd>C-t</kbd> pour revenir à l'étiquette d'un  tag et qu'ensuite
on  veut  retourner   à  sa  définition,  on  pourrait   être  tenté  d'utiliser
<kbd>C-i</kbd>, en  se disant, à  tort, que  <kbd>C-t</kbd> nous a  fait reculer
dans la jumplist.
En réalité,  le saut provoqué  par <kbd>C-t</kbd>  a probablement pour  effet de
déplacer l'entrée correspondant à l'étiquette à la fin de la jumplist.
Pk?
Extrait de :h jumplist:

> If you use a  jump command, the current line number is inserted  at the end of
> the jump list.
> If the same line was already in the jump list, it is removed.

Donc, une nouvelle entrée correspondant  à l'étiquette est ajoutée et l'ancienne
entrée est supprimée.
Ceci équivaut à un déplacement.
L'étiquette  devenant  l'entrée  la  plus  récente,  celle  correspondant  à  la
définition est forcément plus ancienne.
Dans ce  cas, c'est donc  <kbd>C-o</kbd> qu'il faut  utiliser pour revenir  à la
définition d'un tag.

---

    g C-]
    :tjump [ident]

Affiche la liste des  tags matchant l'`{ident}` sous le curseur ou  se rend à la
définition du tag s'il n'y a qu'un seul match.

---

    g]
    :tselect [ident]

Affiche les liste  des tags matchant l'identifiant sous le  curseur (ou matchant
`[ident]`).
Si  `[ident]` n'est  pas  fourni  à `:tselect`,  le  dernier  identifiant de  la
tagstack est utilisé.

# How to install `universal-ctags`?

        $ sudo aptitude purge exuberant-ctags
        $ sudo aptitude install python-docutils
        $ git clone https://github.com/universal-ctags/ctags/
        $ cd ctags
        $ ./autogen.sh
        $ ./configure
        $ make
        $ sudo checkinstall

During the installation, `$ checkinstall` will complain about the version number
being invalid: just  type immediately (no menu entry to  select) whatever number
you want (1.2.3).


For more info, read:

https://github.com/universal-ctags/ctags/blob/master/docs/autotools.rst

# How to open the tag under the cursor in a new split?

    C-w C-]

Works also from visual mode, using the visual selection as the tag name.

# How to move forward in the tag stack?

Execute `:tag`.

From below `:h :pop`:

> :[count]ta[g][!]      Jump to [count] newer entry in tag stack (default 1).

---

Note that there's a bug atm, which  prevents `:tag` from moving to the right tag
after `:tselect` or `:tjump`, then `:pop`.

<https://www.reddit.com/r/vim/comments/ao4y3k/for_those_who_use_tags_how_do_you_jump_forward_in/?ref=share&ref_source=link>

# ?

Read `:h preview-window`, `:h tags-and-searches`, `:h usr_29`.

Integrate everything in our notes regarding 'path', 'tags', 'cdpath', `**`.

# ?

Document the interesting features of the preview window:

  - provides default commands to interact with it no matter where we are
    (ex: C-w z, C-w P, pclose, pedit)

    we don't have to save a unique ID

  - preserve focus (cursor doesn't move)

  - no multiple window opened, a single one per tab

Explain that  it has nothing to  do with a  scratch buffer: a preview  window is
just a special window, not a special buffer.
It  doesn't care  of the  buffer it  displays, it  doesn't give  it any  special
attribute.

# ?

    tagfiles()

Returns a  list with  the file  names used to  search for  tags for  the current
buffer; this is the `'tags'` option expanded.

Utile en cas de tags doublons (qd on utilise tab après `:tj /pat`).
Permet de chercher l'emplacement d'un fichier de tags en trop.

# ?

<https://www.reddit.com/r/vim/comments/6oj6gg/what_are_some_lesser_know_tips_and_tricks_in_vim/dkhtx0c/>

> Either I jump directly to a POI  by name (:tj /foo<tab> or :il /foo<tab>, when
> the cursor is not on the symbol) or directly (g<C-]> or [I, when the cursor is
> on the symbol).

# ?

    :lt[ag] ident

Jump to  tag `ident` and add  the matching tags to  a new location list  for the
current window.

`ident` can  be a regexp pattern.

When `ident` is not given, the last tag name from the tag stack is used.

The search pattern  to locate the tag  line is prefixed with `\V`  to escape all
the special characters (very nomagic).

The location list showing the matching tags is independent of the tag stack.

# ?

À propos des commandes permettant de naviguer dans la tag match list (from `:h tag-matchlist`):

> When  there are  several matching  tags, these  commands can  be used  to jump
> between them.
> Note that these commands don't change the tag stack, they keep the same entry.

# ?

        :[count]ta[g] {ident}

Jump to the definition of `{ident}`, using the information in the tags file(s).
Put `{ident}` in the tag stack.

`{ident}` can be a regexp pattern, see |tag-regexp|.

When there are several matching tags for `{ident}`, jump to the `[count]` one.
When `[count]` is omitted the first one is jumped to.
See |tag-matchlist| for jumping to other matching tags.

# ?

The `:tag` and `:tselect` commands accept a regular expression argument.
See `:h pattern` for the special characters that can be used.
When the argument starts with `/`, it is used as a pattern.
If the argument  does not start with `/`,  it is taken literally, as  a full tag
name.

Examples:

    " jumps to the tag "main" that has the highest priority.
    :tag main

    " jumps to the tag that starts with "get" and has the highest priority.
    :tag /^get

    " lists all the tags that contain "norm", including "id_norm".
    :tag /norm

When the  argument both  exists literally, and  match when used  as a  regexp, a
literal match has a higher priority.
For example, `:tag /open` matches `open` before `open_file` and `file_open`.

When using a pattern, case is ignored.
If you want to match case, use `\C` in the pattern.

# ?

    ┌──────────────┬─────────────────────────────────────────────────────────┐
    │   C-w }      │ prévisualise le tag sous le curseur                     │
    │ 5 C-w }      │ " en fixant la hauteur de la fenêtre preview à 5 lignes │
    ├──────────────┼─────────────────────────────────────────────────────────┤
    │   C-w g }    │                                                         │
    │ 5 C-w g }    │                                                         │
    ├──────────────┼─────────────────────────────────────────────────────────┤
    │   ptag ident │ prévisualise le tag `ident`                             │
    │  5ptag ident │ " en fixant la hauteur de la fenêtre preview à 5 lignes │
    ├──────────────┼─────────────────────────────────────────────────────────┤
    │   pedit file │ édite `file` dans la fenêtre preview                    │
    ├──────────────┼─────────────────────────────────────────────────────────┤
    │  C-w z       │ ferme la fenêtre preview                                │
    │   pclose     │                                                         │
    └──────────────┴─────────────────────────────────────────────────────────┘

# ?

    CTRL-W g }

Use identifier under cursor as a tag and perform a `ptjump` on it.
Make the new Preview window (if required) N high.
If N is not given, `'previewheight'` is used.

# ?

    vert pedit +/pat file

Prévisualise `file` en positionnant le curseur sur `pat`.

# ?

    ┌─────────────────┬──────────────────────────────────────────────────────────────────┐
    │ 'previewwindow' │ flag permettant de vérifier qu'on est dans une fenêtre preview   │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┤
    │ 'previewheight' │ hauteur de la fenêtre qd on ne donne pas sa hauteur via un count │
    │                 │ passé à `:ptag` ou `C-w }`                                       │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┤
    │ 'winfixheight'  │ qd ce flag est activé, Vim s'assure que la hauteur de la fenêtre │
    │                 │ reste la même qd on ouvre/ferme d'autres fenêtres                │
    └─────────────────┴──────────────────────────────────────────────────────────────────┘

# ?

    ptag ident

Small difference from `:tag`:

> When  `ident` is  equal to  the  already displayed  tag, the  position in  the
> matching tag list is not reset.
> This makes the CursorHold example work after a `:ptnext`.

FIXME: Est-ce que cette remarque explique la différence de comportement entre `:tjump` et `:ptjump`?

# ?

    3pp[op]

Does `:3pop` in the preview window. See `:h pop` and `:h ptag`.

# ?

    [range]psearch[!] [count] [/]pattern[/]

Works like `:ijump` but shows the found match in the preview window.
The preview window is opened like with `:ptag`.

Like with  the `:ptag`  command, you can  use this  to automatically
show information about the word under the cursor.

This is  less clever than using  `:ptag`, but you don't  need a tags
file and it will also find matches in system include files.

Example:

    au! CursorHold *.txt nested if &ft ==# 'help' | exe 'sil! psearch '.expand('<cword>') | endif

Warning: This can be slow.

This will cause a `:ptag` to be  executed for the keyword under the cursor, when
the cursor hasn't moved for the time set with `'updatetime'`.

The `nested` makes  other autocommands be executed, so  that syntax highlighting
works in the preview window.

The `sil!` avoids an error message when the tag could not be found.

# ?

    tjump
    [p]tjump ident

Liste les tags matchant le dernier nom de tag dans la tag stack.
Liste les tags matchant `ident` (peut être une regex).

S'il n'y en a qu'un, `:tj` nous y amène automatiquement.

S'il y  en a plusieurs, en  tapant le n° d'un  tag sur la ligne  de commande, on
peut sauter vers lui dans la fenêtre courante ou preview ([p]).


Si on ne veut pas sauter automatiquement qd il n'y a qu'un seul match, utiliser `:tselect`.


Le préfixe `>` indique la position courante, si on est en train de naviguer dans
la tag match list.

        nr              pri kind tag       file
        1               F   f    mch_delay os_amiga.c
        mch_delay(msec, ignoreinput)
        > 2             F   f    mch_delay os_msdos.c
        mch_delay(msec, ignoreinput)
        3               F   f    mch_delay os_unix.c
        mch_delay(msec, ignoreinput)


Note that this depends on the current  file, thus using `:tjump xxx` can produce
different results.

The `kind` column gives the kind of tag, if this was included in the tags file.

The `info` column shows information that could be found in the tags file.

It depends on the program that produced the tags file.

# ?

    :tj /^f
    q
    3

Qd la tag match liste est trop longue, le pager de Vim affiche le prompt:

        -- More --

Si le tag qui nous intéresse  est affiché à l'écran, on peut appuyer
sur `q` pour accéder à la ligne de commande et taper son n°.

# ?

Afficher un tag de la tag match list, dans la fenêtre courante ou preview:

    ┌───────────────┬─────────────────┐
    │ 3[p]tnext     │ le 3e prochain  │
    ├───────────────┼─────────────────┤
    │ 3[p]tprevious │ le 3e précédent │
    ├───────────────┼─────────────────┤
    │ [p]tfirst     │ le premier      │
    ├───────────────┼─────────────────┤
    │ [p]tlast      │ le dernier      │
    ├───────────────┼─────────────────┤
    │ 3[p]tfirst    │ le 3e           │
    └───────────────┴─────────────────┘

# ?

When there are multiple matches for a tag, this priority is used:

   1. 'FSC'  A full matching static tag for the current file.
   2. 'F C'  A full matching global tag for the current file.
   3. 'F  '  A full matching global tag for another file.
   4. 'FS '  A full matching static tag for another file.
   5. ' SC'  An ignore-case matching static tag for the current file.
   6. '  C'  An ignore-case matching global tag for the current file.
   7. '   '  An ignore-case matching global tag for another file.
   8. ' S '  An ignore-case matching static tag for another file.


F: respecte totalement la casse
   (Full matching vs ignore-case)

S: tag se référant à qch défini uniquement dans un fichier spécifique,
   typiquement une fonction locale
   (Static vs global)

C: tag se référant à qch défini dans le fichier courant
   (Current vs another)


The ignore-case matches are NOT found for a ':tag' command when:

   - 'tagcase' is 'match'

   - 'ignorecase' is on and 'tagcase' is 'followic'

   - 'tagcase' is 'smart' and the pattern contains an upper case character

   - 'tagcase' is 'followscs' and 'smartcase' option is on and the pattern
     contains an upper case character

The ignore-case matches are found when:

   - a pattern is used (starting with a '/')
   - for ':tjump'

   - when 'tagcase' is 'followic' and 'ignorecase' is off
   - when 'tagcase' is 'followscs' and the 'smartcase' option is off

---

    set tc=followic    " ignore case
    set noic

    set tc=followic    " ignore case
    set ic

Note that using ignore-case tag searching  disables binary searching in the tags
file, which causes a slowdown.
This can be avoided by fold-case sorting the tag file.
See the 'tagbsearch' option for an explanation.

    --sort[=yes|no|foldcase]

 Indicates whether  the tag file  should be sorted on  the tag name  (default is
 yes).

 The foldcase value specifies case insensitive (or case-folded) sorting.

 Fast binary searches of tag files sorted with case-folding will require special
 support from tools  using tag files, such  as that found in  the ctags readtags
 library, or Vim version 6.2 or higher (using "set ignorecase").

# ?

    'tagbsearch'
    'tbs'
    (default on) global

Qd Vim doit chercher un tag dans un  fichier de tags (ex: `:tag ident`), il peut
utiliser 2 méthodes de recherche: binaire (par dichotomie) ou linéaire.

    ┌─────────────────────────────────────────────┬──────────┐
    │ binaire                                     │ linéaire │
    ├─────────────────────────────────────────────┼──────────┤
    │ rapide                                      │ lente    │
    ├─────────────────────────────────────────────┼──────────┤
    │ pas fiable dans un fichier de tags non trié │ fiable   │
    └─────────────────────────────────────────────┴──────────┘

Vim utilise une recherche linéaire ssi:

When a binary search was done and no  match was found in any of the files listed
in 'tags',  and case is  ignored or a  pattern is used  instead of a  normal tag
name, a retry is done with a linear search.

   - l'option 'tagbsearch' est désactivée
   - le fichier de tags indique qu'il est non-trié
   - la précédente recherche binaire n'a produit aucun résultat

Un fichier de tags peut indiquer qu'il n'est pas trié via la ligne suivante dans
son en-tête:

    !_TAG_FILE_SORTED    0   /some comment/
                     │    │
                     │    └─ doit être un tab
                     └─ doit être un tab


Si on  a fichier  de tag qui  est non trié  et qu'il  ne l'indique pas,  il faut
désactiver `'tbs'`,  pour empêcher Vim  de commencer par utiliser  une recherche
binaire qui pourrait donner des résultats incomplets.

Une recherche binaire n'est fiable que dans un fichier trié.

---

Tags in unsorted tags files, and matches  with different case will only be found
in the retry.

If a tag file  indicates that it is case-fold sorted,  the second, linear search
can be avoided when case is ignored.

Use a value of `2` in the `!_TAG_FILE_SORTED` line for this.

For `Exuberant ctags` the --sort=foldcase switch can be used for this as well.

Note that case must be folded to uppercase for this to work.

By default, tag searches are case-sensitive.

Case is ignored  when `'ignorecase'` is set and `'tagcase'`  is `'followic'`, or
when `'tagcase'` is `ignore`.

Also when `'tagcase'` is `'followscs'`  and `'smartcase'` is set, or `'tagcase'`
is `smart`, and the pattern contains only lowercase characters.

When `'tagbsearch'` is  off, tags searching is slower when  a full match exists,
but faster when no full match exists.

Tags in unsorted tags files may only be found with `'tagbsearch'` off.

When the tags  file is not sorted, or  sorted in a wrong way (not  on ASCII byte
value), `'tagbsearch'` should  be off, or the line given  above must be included
in the tags file.

This  option  doesn't  affect  commands  that  find  all  matching  tags  (e.g.,
command-line completion and `:help`).

# ?

    'path' 'pa'     string  default on Unix: '.,/usr/include,,'
                global or local to buffer |global-local|

Search upwards and downwards in a directory tree using `*`, `**` and `;`.
See `file-searching` for info and syntax.

The maximum length is limited.

How  much depends  on  the system,  mostly  it  is something  like  256 or  1024
characters.

You can check if all the include files are found, using the value of `'path'`.

See `:checkpath`.

# ?

File Searching

The file searching  is currently used for the `'path'`,  `'cdpath'` and `'tags'`
options; and for the functions `finddir()` and `findfile()`.

There are three different types of searching:

1) Downward search:                 *starstar*

   Downward  search  uses  the  wildcards  `*`,  `**`  and  possibly  others
   supported by your operating system.

   `*`  and `**`  are handled  inside  Vim, so  they work  on all  operating
   systems.

   Note that `**` only acts as a special wildcard when it is at the start of
   a name.

   The usage of `*` is quite simple: It matches 0 or more characters.

   In a search pattern this would be `.*`  Note that the `.` is not used for
   file searching.

   `**` is more sophisticated:

   - It ONLY matches directories.

   - It matches up to 30 directories deep by default, so you can use it to
     search an entire directory tree

   - The maximum number of levels matched can be given by appending a number to
     `**`.

    Thus `/usr/**2` can match:

        /usr
        /usr/include
        /usr/include/sys
        /usr/include/g++
        /usr/lib
        /usr/lib/X11
        ....

    It does NOT match `/usr/include/g++/std` as this would be three levels.
    The allowed number range is 0 (`**0`  is removed) to 100 If the given number
    is smaller  than 0 it defaults  to 30, if it's  bigger than 100 then  100 is
    used.
    The system also has a limit on the path length, usually 256 or 1024 bytes.

   - `**` can only be at the end of the path or be followed by a path separator
     or by a number and a path separator.

You can combine `*` and `**` in any order:

    /usr/**/sys/*
    /usr/*tory/sys/**
    /usr/**2/sys/*

2) Upward search:

Here you can  give a directory and  then search the directory tree  upward for a
file.
You could give stop-directories to limit the upward search.
The stop-directories  are appended to the  path (for the `'path'`  option) or to
the filename (for the `'tags'` option) with a `;`.
If you want several stop-directories separate them with `;`.
If you want no stop-directory ("search  upward till the root directory) just use `;`.

    /usr/include/sys;/usr

Will search in:

    /usr/include/sys
    /usr/include
    /usr

If  you use  a relative  path  the upward  search  is started  in Vim's  current
directory or in the  directory of the current file (if  the relative path starts
with `./` and `d` is not included in `cpoptions`).

If Vim's current path is `/u/user_x/work/release` and you do:

    :set path=include;/u/user_x

and then search for a file with `gf` the file is searched in:

    /u/user_x/work/release/include
    /u/user_x/work/include
    /u/user_x/include

3) Combined up/downward search:

If Vim's current path is `/u/user_x/work/release` and you do:

    set path=**;/u/user_x

and then search for a file with |gf| the file is searched in:

    /u/user_x/work/release/**
    /u/user_x/work/**
    /u/user_x/**

BE CAREFUL!

This  might consume  a lot  of time,  as the  search of  `/u/user_x/**` includes
`/u/user_x/work/**` and `/u/user_x/work/release/**`.

So `/u/user_x/work/release/**`  is searched three times  and `/u/user_x/work/**`
is searched twice.

In the above example you might want to set path to:

    :set path=**,/u/user_x/**

This searches:

    /u/user_x/work/release/** ~
    /u/user_x/** ~

This searches the same directories, but in a different order.

# ?

This comment seems to imply that you can generate your own custom tags, in any file.

> I think you want tags?
> You'd just define  a custom filetype and  a tag marker of your  choosing and use
> universal-ctags with your regexes.

<https://www.reddit.com/r/vim/comments/87azt5/line_pointers/dwbku57/>

---

It could be very useful to navigate quickly in our notes.
We would need to include some custom markers in the notes (like star in a Vim help file).

Google “how to add support for new language universal ctags”.
And read:

        https://github.com/universal-ctags/ctags/blob/master/docs/optlib.rst
        http://docs.ctags.io/en/latest/optlib.html
        http://ctags.sourceforge.net/EXTENDING.html

See also the TO DO in our vimrc, just above `$MY_WIKI`.

