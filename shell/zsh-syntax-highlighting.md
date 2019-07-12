<https://github.com/zsh-users/zsh-syntax-highlighting/>

            Repo du projet.

Il s'agit d'un plugin colorisant les tokens de la ligne de commande en fonction de leur sens.
Pex:

   - rouge pour une commande invalide
   - vert  pour une commande valide
   - jaune pour une chaîne
   - bleu  pour un glob qualifier

Le plugin est constitué de “highlighters“, qu'on peut activer individuellement:

    ┌──────────┬──────────────────────────────────────────────────────┐
    │ main     │ le highlighter de base, et le seul activé par défaut │
    ├──────────┼──────────────────────────────────────────────────────┤
    │ brackets │ gère les parenthèses, accolades, crochets            │
    ├──────────┼──────────────────────────────────────────────────────┤
    │ pattern  │ gère des patterns définis par l'utilisateur          │
    ├──────────┼──────────────────────────────────────────────────────┤
    │ cursor   │ gère le caractère après le curseur                   │
    ├──────────┼──────────────────────────────────────────────────────┤
    │ line     │ gère toute la ligne de commande                      │
    ├──────────┼──────────────────────────────────────────────────────┤
    │ root     │ idem, mais seulement si l'utilisateur est root       │
    └──────────┴──────────────────────────────────────────────────────┘

Avec ce plugin, la coloration syntaxique est configurée via 3 arrays:

    ┌────────────────────────────┬─────────────────────────────────────────────────────────┐
    │ ZSH_HIGHLIGHT_HIGHLIGHTERS │ détermine quels highlighters sont activés par le plugin │
    ├────────────────────────────┼─────────────────────────────────────────────────────────┤
    │ ZSH_HIGHLIGHT_STYLES       │ détermine quels highlightings ils doivent appliquer     │
    ├────────────────────────────┼─────────────────────────────────────────────────────────┤
    │ zle_highlight              │ détermine la coloration syntaxique intégrée à zsh       │
    └────────────────────────────┴─────────────────────────────────────────────────────────┘

    ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern)

            Active les highlighters `main`, `brackets`, et `pattern`, en les ajoutant à l'array
            `ZSH_HIGHLIGHT_HIGHLIGHTERS`.

            Ils appliquent les highlightings définis dans l'array associative `ZSH_HIGHLIGHT_STYLES`.


    ZSH_HIGHLIGHT_STYLES[function]='fg=magenta,underline'
    ZSH_HIGHLIGHT_STYLES[bracket-level-3]='fg=yellow,bold'
    ZSH_HIGHLIGHT_PATTERNS+=('rm -rf *' 'fg=white,bold,bg=red')

            Configure l'apparence des:

                    - noms de fonction
                      nécessite l'activation du highlighter `main`

                    - parenthèses imbriquées (3e niveau d'imbrication)
                      nécessite l'activation du highlighter `brackets`

                    - commandes commençant par `rm -rf *`
                      nécessite l'activation du highlighter `pattern`

                      Contrairement aux autres affectations, on utilise `+=` et non `=` pour éviter
                      d'écraser les styles de précédents patterns.

                      La différence vient du fait que `ZSH_HIGHLIGHT_PATTERNS` peut gérer plusieurs patterns,
                      et donc stocker plusieurs valeurs.


    default:fg=white,bold

            Valeur par défaut de l'array builtin `zle_highlight`.

            `zle_highlight` est intéressante pour 2 raisons:

                    - elle permet de configurer la coloration syntaxique intégrée à zsh par défaut

                    - la syntaxe des valeurs qu'elle accepte est identique à celles qu'on peut donner à
                      `ZSH_HIGHLIGHT_STYLES`
                      cette syntaxe est décrite dans `man zshzle`,  section `CHARACTER HIGHLIGHTING`


Chaque valeur dans `zle_highlight` suit le schéma suivant:

        contexte:h1,h2,...
        │        │
        │        └ quels highlightings appliquer
        └ où les highlightings suivants doivent être appliqués

`contexte` peut être au choix:

    ┌─────────┬────────────────────────────────────────────────────────────────────────────────────┐
    │ default │ tout texte affecté par aucun highlighting                                          │
    ├─────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ isearch │ qd un widget de recherche incrémental est actif, la région de la ligne de commande │
    │         │ où le pattern s'affiche                                                            │
    ├─────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ region  │ la région entre le curseur et la marque qd on l'active via `C-x C-x` ou `C-space`  │
    ├─────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ special │ caractères n'ayant pas de glyphes mais affichés de manière spéciale                │
    ├─────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ suffix  │ caractères de type suffixe qui pourraient être supprimés si la complétion          │
    │         │ s'arrêtait à eux                                                                   │
    │         │                                                                                    │
    │         │ ex:    cd ~; echo Do Tab Tab    →    Documents/                                    │
    │         │                                               │                                    │
    │         │                                               └ caractère suffixe                  │
    ├─────────┼────────────────────────────────────────────────────────────────────────────────────┤
    │ paste   │ le texte qu'on vient de coller via C-S-v                                           │
    └─────────┴────────────────────────────────────────────────────────────────────────────────────┘



Qd `region_highlight` est configurée, les styles de `zle_highlight` et `region_highlight` sont appliqués
dans cet ordre:

        1. styles `zle_highlight` associés aux contextes isearch, region, suffix, paste
        2. styles `region_highlight`
        3. styles `zle_highlight` associés aux contextes default et special

Si un caractère est affecté par plusieurs styles, le dernier appliqué l'emporte.

                                     TODO:

À terminer...

zle_highlight  may  contain  additional  fields for  controlling  how  'terminal
sequences to change colours' are output.
Each of the  following is followed by a  colon and a string in the  same form as
for key bindings.
This will not  be necessary for the  vast majority of terminals  as the defaults
shown in parentheses are widely used.

fg_start_code (\e[3)

        The start of the escape sequence for the foreground colour.
        This is followed by an ASCII digit representing the colour.

fg_default_code (9)

        The number to use instead of the colour to reset the default foreground colour.

fg_end_code (m)

        The end of the escape sequence for the foreground colour.

bg_start_code (\e[4)

        The start  of the escape sequence  for the background colour.  This is followed by  an ASCII
        digit repre‐ senting the colour.

bg_default_code (9)

        The number to use instead of the colour to reset the default background colour.

bg_end_code (m)

        The end of the escape sequence for the background colour.


The available types of  highlighting are the following. Note that not all  types of highlighting are
available on all terminals:

none

        No highlighting is applied to the given context.
        It is not useful for this to appear with other types of highlighting; it
        is used to override a default.

fg=colour

        The foreground colour should be set  to colour, a decimal integer or the
        name of one of the eight most widely-supported colours.

        Not all  terminals support this and,  of those that do,  not all provide
        facilities to  test the support, hence  the user should decide  based on
        the terminal type.
        Most  terminals support  the colours  black, red,  green, yellow,  blue,
        magenta, cyan and white, which can be set by name.
        In addition.
        default may be used to set the terminal's default foreground colour.
        Abbreviations are allowed; b or bl selects black.
        Some terminals may generate additional  colours if the bold attribute is
        also present.

        On recent terminals and on  systems with an up-to-date terminal database
        the number  of colours supported  may be  tested by the  command `echotc
        Co'; if  this succeeds, it  indicates a limit  on the number  of colours
        which will be enforced by the line editor.
        The number of colours is in any case limited to 256 (i.e. the range 0 to
        255).

        Colour is also known as color.

bg=colour

        The background colour should be set to colour.
        This works similarly to the  foreground colour, except the background is
        not usually affected by the bold attribute.

bold

        The characters in the given context are shown in a bold font.
        Not all terminals distinguish bold fonts.

standout

        The characters in the given context are shown in the terminal's standout
        mode.
        The actual effect  is specific to the terminal; on  many terminals it is
        inverse video.
        On some such terminals, where the  cursor does not blink it appears with
        standout  mode negated,  making  it  less than  clear  where the  cursor
        actually is.
        On  such terminals  one  of  the other  effects  may  be preferable  for
        highlighting the region and matched search string.

underline

        The characters in the given context are shown underlined.
        Some terminals  show the  foreground in a  different colour  instead; in
        this case whitespace will not be highlighted.

The characters described  above as `special` are  as follows. The formatting described  here is used
irrespective of whether the characters are highlighted:

ASCII control characters

        Control characters in the ASCII range are shown as `^` followed by the base character.

Unprintable multibyte characters

        This item  applies to control  characters not  in the ASCII  range, plus
        other characters as follows.
        If the  MULTIBYTE option is in  effect, multibyte characters not  in the
        ASCII character set  that are reported as having zero  width are treated
        as combining characters when the option COMBINING_CHARS is on.
        If  the option  is off,  or  if a  character appears  where a  combining
        character is not valid, the character is treated as unprintable.

        Unprintable  multibyte  characters are  shown  as  a hexadecimal  number
        between angle brackets.
        The number is the code point of the character in the wide character set;
        this may or may not be Unicode, depending on the operating system.

Invalid multibyte characters

        If the MULTIBYTE option is in effect,  any sequence of one or more bytes
        that does  not form a  valid character in  the current character  set is
        treated as a series of bytes each shown as a special character.
        This case can be distinguished  from other unprintable characters as the
        bytes are represented as two  hexadecimal digits between angle brackets,
        as distinct from the four or  eight digits that are used for unprintable
        characters that are nonetheless valid in the current character set.

        Not  all   systems  support   this:  for  it   to  work,   the  system's
        representation of wide characters must be code values from the Universal
        Character Set, as defined by IS0 10646 (also known as Unicode).

Wrapped double-width characters

        When a double-width character appears in  the final column of a line, it
        is instead shown on the next line.
        The  empty space  left  in the  original position  is  highlighted as  a
        special character.

If zle_highlight is  not set or no value  applies to a particular context, the  defaults applied are
equivalent to

        zle_highlight=(region:standout special:standout suffix:bold isearch:underline)

i.e. both the region and special characters are shown in standout mode.

Within  widgets,  arbitrary regions  may  be  highlighted by  setting  the  special array  parameter
region_highlight; see above.

zle peuple automatiquement un certain nb de paramètres spéciaux, qu'on peut utiliser au sein des
fonctions custom invoqués par nos widgets. En voici une liste non exhaustive:

BUFFER (scalaire)

       Tout le contenu du buffer à éditer.
       On parle  de buffer au  lieu de ligne  de commande, probablement  car zle
       manipule cette  dernière via un  buffer, comme n'importe quel  éditeur le
       ferait.

       Si  une fonction  change le  buffer, le  curseur gardera,  si le  nouveau
       buffer est suffisamment long, la même position.


LBUFFER (scalaire)
RBUFFER (scalaire)

       Partie du buffer à gauche / droite du curseur.
       Si une fonction change l'un des deux, le curseur sera toujours positionné
       entre LBUFFER et RBUFFER.


CURSOR (entier)

       Position du curseur au sein du buffer, comprise entre 0 et `$#BUFFER`.
       Par définition, $#BUFFER = $#LBUFFER.
       Modifier la  valeur de ce  paramètre modifie probablement la  position du
       curseur.


PREDISPLAY (scalar)
POSTDISPLAY (scalar)

       Texte à afficher avant /après la partie éditable du buffer.
       Pour  afficher une  ligne vide,  on écrira  un newline  au sein  de leurs
       valeurs.


region_highlight (array)

       Each  element  of this  array  may  be set  to  a  string that  describes
       highlighting for an  arbitrary region of the command-line  that will take
       effect the next time the command-line is redisplayed.
       Highlighting of the non-editable parts  of the command-line in PREDISPLAY
       and POSTDISPLAY  are possible,  but note  that the P  flag is  needed for
       character indexing to include PREDISPLAY.

       Each string consists of the following parts:

              Optionally, a `P' to signify that the start and end offset that follow include any  string  set
              by  the  PREDISPLAY  special parameter; this is needed if the predisplay string itself is to be
              highlighted.  Whitespace may follow the `P'.

              A start offset in the same units as CURSOR, terminated by whitespace.

              An end offset in the same units as CURSOR, terminated by whitespace.

              A highlight specification in the same format as used for contexts in  the  parameter  zle_high‐
              light, see the section `Character Highlighting' below; for example, standout or fg=red,bold

       For example,

              region_highlight=("P0 20 bold")

       specifies that the first twenty characters of the text including any predisplay string should be high‐
       lighted in bold.

       Note that the effect of region_highlight is not saved and disappears as soon as the line is accepted.

       The final highlighting on the command-line depends on both region_highlight and zle_highlight; see the
       section CHARACTER HIGHLIGHTING below for details.

---

Lien expliquant comment créer son propre highlighter:
<https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/docs/highlighters.md>


La création d'un highlighter, foo, se fait en 5 étapes:

   1. créer et éditer `/path/to/plugin/highlighters/foo/foo-highlighter.zsh`

   2. y écrire la fonction `_zsh_highlight_highlighter_foo_predicate`
                                                          │
                                                          └ predicate = qd le highlighter doit être actif

       Elle doit retourner 0 qd on veut que le highlighter soit actif, un autre nb autrement. Ex:

                _zsh_highlight_highlighter_foo_predicate() {
                  # notre highlighter ne doit être actif que dans un repot git
                  [[ -d .git ]]
                }

   3. y écrire la fonction `_zsh_highlight_highlighter_foo_paint`
                                                            │
                                                            └ paint = quel style applique le highlighter

       C'est elle qui réalise la coloration syntaxique, en appelant `_zsh_highlight_add_highlight`
       et en lui passant 3 arguments:

                - début de la région à coloriser
                - fin de la région
                - style (via une clé de `ZSH_HIGHLIGHT_STYLES`)

       Le highlighting doit être défini au sein de notre script, et en dehors de toute fonction,
       via la syntaxe suivante:

                : ${ZSH_HIGHLIGHT_STYLES[foo:mystyle]:=value}

       Exemple:

                : ${ZSH_HIGHLIGHT_STYLES[foo:mystyle]:=fg=green}
                │                        │           │
                │                        │           └ `:=` est un opérateur builtin
                │                        │             il ne modifie le lhs que s'il est non défini ou nul
                │                        │
                │                        └ le nom de la clé doit suivre le schéma:
                │                          foo : mystyle
                │
                └ commande builtin qui n'a aucun effet, à ceci près que ses arguments sont développés
                  ce qui peut avoir un effet sur des paramètres shell

                # coloriser tout le buffer avec le style 'mystyle'
                _zsh_highlight_highlighter_foo_paint() {

                _zsh_highlight_add_highlight 0 $#BUFFER foo:mystyle
                #                            │ │        │
                #                            │ │        └ highlighting à appliquer
                #                            │ └ fin de la région (variable interne à zsh; `man zshzle`)
                #                            └ début de la région à coloriser
                }


                                     NOTE:

       En pratique, il semble que si le highlighter n'applique qu'un seul style, on peut se passer
       de 'mystyle' et simplifier la clé 'foo:mystyle' en 'foo'.
       De même, si le highlighter applique plusieurs styles, on peut se passer de 'foo'.
       La seule chose qui semble importante, c'est que chaque style soit associé à une clé ayant un nom unique.

   4. nommer nos fonctions et variables globales `_zsh_highlight_foo_*`

       FIXME: Quelles fonctions et quelles variables ?
              Et pk les appeler comme ça: obligation ou convention ?

   5. activer notre highlighter dans notre vimrc:

                ZSH_HIGHLIGHT_HIGHLIGHTERS+=(foo)


    https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/tests/README.md

            Lien  expliquant   comment  écrire  un  test   pour  vérifier  qu'un
            highlighter custom se comporte comme on le souhaite dans différentes
            circonstances.

