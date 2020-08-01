# I'm going to run these commands:

    $ IFS=:
    $ rm myfile myother:file

## Which arguments will the shell pass to `execve()`?

   1. `rm`
   2. `myfile`
   3. `myother:file`

### Why?

IFS is only during word splitting of *data*, not code.
In the last command, the shell does not split any data, only script code.
And a line of script code is always split only on whitespace.

##
# I'm going to run these commands:

    $ IFS=:
    $ files='myfile myother:file'
    $ rm $files

## Which arguments will the shell pass to `execve()`?

   1. `rm`
   2. `myfile myother`
   3. `file`

### Why?

Initially, there's no data,  so the shell ignores IFS and  splits the command at
the only existing whitspace:

    $ rm $files
        ^

Then, parameter expansion is performed to expand `$files`, and word splitting is
performed on the expansion:

    $ rm myfile myother:file
                       ^

This time, IFS *is* considered because `myfile myother:file` is data.
So the shell splits at the only character present in IFS, i.e. `:`.

##
##
##
# key bindings
## bash
### How to list the key bindings bound to
#### functions?

    $ bind -p
    $ bind -P

The lowercase flag can be fed back to the shell.
The uppercase one is human-readable.

Getting  a machine-readable  output is  useful, if  you want  to redefine  a key
binding programmatically, for example after a `sed(1)` transformation.

#### macros?

    $ bind -s
    $ bind -S

###
### How to list variables?

    $ bind -v
    $ bind -V

                                          ┌ commande d'édition invoquant une fonction
                                          │
    Ex de commande:    bind '"\C-t":      transpose-chars'
    Ex de macro:       bind '"\C-x\C-r":  ". ~/.bashrc"'
                                          │
                                          └ macro rejouant une séquence de frappes

###
## zsh
### How to list the current
#### key bindings?

    $ bindkey

#### keymaps?

    $ bindkey -l

###
### ?

Try to re-implement `start-kbd-macro`, `end-kbd-macro`, `call-last-kbd-macro`.
They're bound to `C-x (`, `C-x )`, `C-x e` in bash.

---

Document that  we've supercharged `C-k`: it  kills the line, *or*  the region if
it's active.

---

    bind '\C-x\C-u:  undo'

Associe à `C-x C-u` la fonction `undo` (déjà par le cas par défaut).

On peut utiliser cette commande dans:

   - une session bash pour une utilisation temporaire

   - son ~/.bash_aliases pour un effet permanent dans bash

   - son ~/.inputrc:

            "\C-x\C-u":  undo

     ... pour un effet permanent dans tous les pgms utilisant readline

La liste des fonctions disponible (du type unix-word-rubout) est lisible via bind -p

---

    M-DEL

Supprime du curseur jusqu'au précédent whitespace.

---

`unix-word-rubout` est le nom de la fonction  utilisée par bash qd on appuie sur C-w.
Cette fonction  supprime tous les  caractères entre  le curseur et  le précédent
début de mot (l'espace semblant être le seul séparateur possible entre 2 mots).
C'est  plutôt  chiant,  car  souvent  on préférera  ne  supprimer  que  jusqu'au
précédent slash et non jusqu'au précédent espace.

Il existe une autre fonction qui supprime jusqu'au précédent début de mot:

    backward-kill-word

Celle-ci est  toutefois différente,  car contrairement à  unix-word-rubout, elle
considère aussi le slash comme un séparateur possible entre 2 mots.
Par défaut, elle est associée à `M-DEL`.

Comme je trouve qu'on supprime plus fréquemment du curseur jusqu'au début du mot
que jusqu'au  précédent whitespace,  et que  C-w est plus  pratique à  taper que
M-DEL, j'ai inversé les fonctions utilisées par ces 2 touches.

Dans  emacs, par  défaut, C-w  supprime tout  le texte  entre le  curseur et  la
marque.

---

Qd readline (ou emacs)  utilise la notation DEL pour désigner  une touche, il ne
s'agit pas de la touche `delete` (`suppr` en fr) mais de la touche `backspace`.

---

FIXME:

Je n'arrive pas à supprimer le texte entre le curseur et la marque.
On a oublié de restaurer une fonction readline?
Vérifier dans ~/.bashrc, ~/.shrc, ~/.zshrc, ~/.inputrc

---

    C-g

Annuler la commande en cours (fonction `abort`).
Utile pex qd on fuzzy search l'historique des commandes (`C-r`).
Un peu plus facile  à taper que `C-c` et n'a pas  d'effet visible (n'affiche pas
de ^C).

---

    C-x C-u
    C-_

Undo.

---

    C-x C-x
    C-space

Échange la position du curseur avec celle de la marque.
Pose la marque à l'endroit où se trouve le curseur.

Les fonctions invoquées par ces chords sont:

        exchange-point-and-mark
        set-mark / set-mark-command

Pratique qd on édite  le milieu de la ligne de  commande, et qu'on a
besoin de temporairement  rajouter qch au début, puis  de revenir là
où on était.


Dans zsh, qd on échange la position de la marque avec celle du curseur, le texte
entre la marque et le curseur est colorisé.


Par défaut, la marque se trouve au début de la ligne.

---

    ┌ pose la marque où se trouve le curseur
    │
    C-SPC M-b M-b M-"        zsh
                  │
                  └ quote le texte entre la marque et le curseur

Quote les 2 mots précédents le curseur.

Par défaut, `M-"` est associé à `quote-region`, qui est un widget zle quotant le
texte entre la marque et le curseur.

---

    M->
    M-<

Nous repositionne à la toute fin / au tout début de l'historique.

---

    M-5 x

Insère `xxxxx`.

---

    M-2 M-.

Insère le 2e argument de la dernière commande.
Répétable: on peut passer en revue tous les 2nds arguments des derniers commandes.

FIXME:

Dans zsh, il semble que l'indexage commence depuis la fin des arguments, au lieu du début:

    (bash): M-2 M-.
    2e argument~

    (zsh):  M-2 M-.
    avant-dernier argument~


FIXME:

(`M-2`) `C-M-y` (`yank-nth-arg`) ne semble pas fonctionner dans zsh.
Et dans bash, quelle différence avec `M-2 M-.`?

---

    C-M-e

Développe la ligne de commande.

Note that Ctrl-Alt-E in bash does not only expand aliases.
It also expands  variables, command substitution (!),  process substitution (!),
arithmetic  expand  and  removes  quotes  (it  doesn't  do  filename  generation
(globbing) or tilde expansion).

---

    C-y

Coller le dernier texte tué (yank ; emacs utilise le terme yank pour coller).

Si on supprime plusieurs mots via C-w, le dernier texte tué est la concaténation
de tous ces mots.

---

    M-y

Changer le dernier texte collé (avec un autre texte tué précédemment).
Répétable pour passer en revue tous les derniers textes tués.

---

    C-n    (custom)
    C-p    (")

Compléter des noms de fichiers.

Les candidats sont choisis à partir des items du dossier courant.
On peut  autocompléter tout  un chemin,  pour ce faire,  il faut  valider chaque
noeud du chemin en faisant pex un `C-b C-f` (ou un `C-x C-n`).

FIXME:

Pas dispo dans zsh.
Plus dispo dans bash non plus (j'ai viré le raccourci).
C'était utile?
Si oui, réimplémenter en changeant les raccourcis.

---

    M-Y    (custom)
    copy-region-as-kill

Copy the text between the cursor and the mark.
You can then paste it wherever you want by pressing `C-y`.
By default, `copy-region-as-kill` is bound to `M-w` in zsh and unbound in bash.

---

    M-#

Préfixe la commande avec un dièse et l'exécute.
N'a aucun effet, car  le dièse commente la ligne ce qui  empêche son code d'être
interprété.
Utile pour conserver dans l'historique une  commande partielle, ou dont on n'est
pas encore sûr.

##
# brace expansion

Il s'agit d'une  fonctionnalité permettant de développer  un série de chaînes,  en les combinant
éventuellement avec  un préambule et  / ou  post-scriptum. Utile pour  passer + rapidement  à une
commande une longue série d'arguments dont le nom est proche.


    echo {foo,bar,baz}
    echo _{foo,bar,baz}
    echo {foo,bar,baz}_
    echo _{foo,bar,baz}-

            foo bar baz
            _foo_bar_baz
            foo_bar_baz_
            _foo-_bar-_baz-


    echo {5..12}
    echo {c..k}

            5 6 7 8 9 10 11 12
            c d e f g h i j k


    a=5; b=12; echo {$a..$b}

            {5..12}               bash
            5 6 7 8 9 10 11 12    zsh

            Pk bash ne développe pas l'expression comme on voulait?

            Le développement des accolades se fait avant celui des variables, et
            bash ne sait développer que des rangées de nb ou de lettres (`$a` et
            `$b` ne sont ni des nb ni des lettres).


    mv long/path/to/foo.{old,,new}

            Renommer `foo.old` en `foo.new`.


    cp foo{,.bak}

            Faire un backup de foo nommé `foo.bak`.


    wget http://domain.com/book/page{1..5}.html

            Dl les pages 1 à 5 d'un site.


    mkdir -p foo/{bar,baz}/{qux,norf}

            Créer une arborescence de dossiers.


    echo "${#foo}"

            Afficher la taille de la chaîne stockée dans la variable `foo`.


    echo "${foo//[bar]}"

            Supprimer toutes les occurrences de la sous-chaîne `bar` au sein de la chaîne stockée dans `foo`.


    echo "${TMUX%/*}"

            Afficher le dossier contenant le socket tmux (dont le chemin est stocké ds la variable $TMUX).

            %/* = on supprime le pattern '/*' (n'importe quel texte après un slash)

# commande substitution

    cmd1 "$(cmd2)"
    cmd1 "$(cmd2 "$(cmd3)")"
    cmd1 "$(cmd2 "$(cmd3 "$(cmd4)")")"

On peut imbriquer autant de substitutions de commandes qu'on veut.

Il n'y jamais besoin de traiter les quotes spécialement (pex les échapper).
C'est pour cette raison que la syntaxe:

    $(...)

... est préférable à:

    `...`

Cette dernière  devient de  plus en  plus complexe au  fur et  à mesure  qu'on a
besoin de niveaux d'imbrications supplémentaires.

# word splitting

Le shell  lit des commandes depuis  son entrée qui  peut être le terminal  ou un
fichier.
Chaque ligne est considérée comme une seule commande.
Il divise  la ligne de  commande en  mots qui sont  séparés par une  séquence de
whitespace syntaxique.
On parle de _word splitting_.

Le 1er  mot est  interprété comme le  nom d'une commande,  les autres  comme des
arguments (options, noms de fichiers).
Le shell appelle alors une fonction dans la famille `exec`:

   - execl()
   - execv()
   - execle()
   - execve()
   - execlp()
   - execvp()

Il lui passe 3 infos:

   - le nom d'un binaire ou d'un script        qui
   - une array d'arguments (chaînes)           quoi
   - une array de variables d'environnement    comment

Pour + d'infos:
<https://indradhanush.github.io/blog/writing-a-unix-shell-part-2/>

L'OS cherche  ensuite dans `$PATH` le  nom du binaire/script, et  l'exécute avec
les arguments passés.


    IFS=: ; files="foo bar:baz" ; rm $files

            Supprime les fichiers `foo bar` et `baz`.

            Dans la dernière commande, le shell doit développer `$files`:
            on parle de Parameter Expansion.

            bash passe à `rm` les arguments `foo bar` et `baz`.
            La valeur de `$IFS` compte à cause du PE.

            Il existe donc 2 types de  splitting qui peuvent se produire sur une
            même ligne de commande:

                    - le FIELD splitting divise une chaîne issues d'un développement
                    - le WORD splitting qui divise la ligne de commande qui en résulte

            Contrairement au  word splitting  qui utilise  tjrs une  séquence de
            whitespace syntaxique  pour délimiter  les mots, le  field splitting
            utilise  la  valeur de  la  variable  spéciale IFS  (Internal  Field
            Separator).

            Pour bash, par défaut  IFS n'a pas de valeur, et  agit comme si elle
            valait " \t\n".
            Le field splitting se produit  lorsque le shell doit développer qch:
            un chemin (~ → /home/path), une variable ($myvar) ...


                                     NOTE:

            Unfortunately,  the  bash  documentation only  uses  the  expression
            “word splitting”,  and the  zsh documentation uses  both expressions
            (word/field) interchangeably:

                    https://unix.stackexchange.com/a/429540/289772
                    https://www.zsh.org/mla/workers/2018/msg00253.html


                                     NOTE:

            Il est déconseillé de modifier IFS  car bash va chercher à remplacer
            les nouveaux mots développés par des noms de fichiers qui match.
            En +, il  est difficile de limiter la portée  d'un field splitting à
            une seule commande.


    IFS=: ; rm foo bar:baz

            Supprime foo et "bar:baz".

            Rien à développer donc la valeur d'IFS n'a pas d'importance.


    read -p 'Enter 3 values: ' foo bar baz

            `read` nous demande de saisir 3 valeurs.

            Le  shell va  diviser la  ligne qu'on  va saisir,  pour en  affecter
            chaque morceau aux variables `foo`, `bar`, `baz`.

            Il s'agit encore une fois d'un field splitting.

##
##
##
# How to get the list of shell builtin commands?

    $ compgen -b
               │
               └ synonym of `-A builtin`

This command works also  in zsh, provided that you enabled  the zsh emulation of
the bash `compgen` function:

    autoload -Uz bashcompinit
    bashcompinit

---

TODO: document the fact that you can get other kinds of completions.

Example:

    $ compgen -c avahi

This should output the list of commands starting with the keyword “avahi”.

You can get the list of all possible  flags – which can be passed to `compgen` –
at `man bash /SHELL BUILTIN COMMANDS/;/^\s*complete/;/^\s*-A`.

##
# How to disable a builtin command to use the external command which is its counterpart?

    $ enable -n printf

    % disable printf

You can check the effect by executing `type printf` before and after the commands.

##
# Is there a limit on the length of arguments which I can pass to a command?

Yes.

## How can I get its current value?

    $ getconf ARG_MAX

## How can I get the values of other similar limits?

    $ getconf -a

Note that these limits are not shell-specific, they are system-specific.
So, the output of this command will be the same whether you're in bash or zsh.

<https://unix.stackexchange.com/a/70370/289772>

##
# When does the shell fork a subshell?

To execute:

   - ( list )
   - a job
   - a command substitution
   - a process substitution
   - a simple command in a pipeline

You can confirm that a job is executed in a subshell with these commands:

    $ { sleep 1000; echo finished ;} &
    $ pstree -lsp $(pidof sleep)
    ... zsh───zsh───sleep~
              ^-^
              subshell~

# Why does a shell fork to execute an external command?

After invoking  `execve()`, the shell  process has  replaced its image  with the
image of an external command.
So, if the shell didn't fork, `execve()` would in effect “kill” the shell.
It would have no way to print another  prompt, and go on doing its job after the
external command has finished.

# Does a subshell always fork to execute an external command?

No.

A subshell doesn't need to fork for the last command it was asked to execute.
Because after the last command, it won't be needed anymore.

The difference  between an interactive shell  which ALWAYS fork, and  a subshell
which SOMETIMES doesn't fork, is:

   - the interactive shell doesn't know when it won't be needed anymore

   - the subshell knows exactly the entire set of commands it will have to
     execute during its lifetime

MWE:

    $ find / -name '*' | wc -l
    $ pstree -lsp $(pidof find)
    ... bash───find~
        │      │
        │      └ Initially this was a subshell started because `find` was part of a pipeline.
        │
        │        It should have forked a sub-sub-shell to execute `find(1)`.
        │        But it didn't.
        │        Instead it immediately called `execve()`.
        │
        └ current shell from which the pipeline is executed

This is an optimization performed by some shells, for some commands:

- <https://unix.stackexchange.com/a/41424/289772>
- <https://unix.stackexchange.com/a/466523/289772>

---

This is also the reason why you  don't see the subshell executing a script, with
`pstree(1)`.
Since the  subshell has only  one command to execute,  it doesn't fork,  it just
calls `execve()` to replace its image with the one of the script.

---

OTOH, if the command is not the last one, the subshell WILL fork a sub-sub-shell:

    $ ( find / -name '*'; true ) | wc -l
    $ pstree -lsp $(pidof find)
    ... bash───bash───find~
        │      │~
        │      └ subshell~
        │~
        └ current shell from which the pipeline is executed~

Similarly:

    $ while true; do find / -name '*'; done | wc -l
    $ pstree -lsp $(pidof find)
    ... bash───bash───find~

In the last example, the subshell is asked to execute a single `while` loop.
But  a  loop may  execute  several  commands,  so  the subshell  considers  that
`find(1)` is not the last command, and forks.

# Why does a shell variable (i.e. non-exported) persist in a subshell but not in a script?

TLDR: A shell variable survives `fork()` but not `execve()`.

---

When you  run `./script`, the shell  forks a subshell which  calls `execve()` to
execute the script.
Internal aspects of the subshell are lost in the `execve()` call.
Non-exported variables, functions, ... are shell notions that the kernel doesn't
know about, and they are lost when the shell executes another program.

Even if that other program happens to be a shell script:

    /bin/bash /path/to/script

... it is  executed by a new shell  instance that doesn't know or  care that its
parent process happens to also be an instance of the same shell.

For more info, see:
<https://unix.stackexchange.com/a/157962/289772>

##
# Why are some commands built into the shell?  (2)

To be more efficient  (e.g. `echo`).

---

Or to be able to modify the shell itself (e.g. `alias`, `cd`).

`alias` and `cd` affect the current shell, by:

   - telling it to expand a word into an arbitrary command
   - changing its current directory

If `alias` and `cd` were not built-in, and instead external programs, they would
be run in child processes of the current shell.
But a child process can't affect its parent.
So, they wouldn't be able to do their job.

# What are the six basic constructs to build a command-line?

   - simple command
   - pipeline
   - list
   - compound command
   - coprocess
   - shell function definition

##
# Must I always put a backslash at the end of a line to continue on the next one?

Not necessarily.

You must iff the line makes sense on its own.
If it doesn't make sense without the next one(s), then you don't need a backslash.

    # `echo 1 &&` doesn't make sense, so you don't need a backslash.
    echo 1 &&
    echo 2

    # `echo 1 2 3` is valid, so you DO need a backslash.
    echo 1 2 3 \
    4

    # `echo 1` is valid, so you DO need a backslash.
    echo 1 \
    && echo 2

    # As soon as you write `(` to begin an array assignment,
    # the shell expects `)` to end it.
    # So, as long as you haven't written `)`, your assignment
    # is not valid, and you don't need a backslash.
    % arr=(
        'one'
        'two'
        'three'
      )

    % string='hello
        world'

    # `ls |` doesn't make sense, so you don't need a backslash
    % ls |
      sort

See: <https://unix.stackexchange.com/a/281310/289772>

##
# How to set a readline variable from an interactive bash session?

    $ bind 'set <variable>'

##
# I'm in `/tmp/old/path/to/dir`, how to quickly get to `/tmp/new/path/to/dir`?

    % cd old new

Note that the substitution is not very smart.
It looks for the first `old` in the path, and replaces it with `new`.
But if it fails, it doesn't try to look further for a possible 2nd `old`.
So, even though you could expect the following commands to succeed, they will fail:

    % mkdir -p /tmp/old/path/to/old/dir
    % mkdir -p /tmp/old/path/to/new/dir
    % cd /tmp/old/path/to/old/dir
    % cd old new
    ✘ cd: no such file or directory: /tmp/new/path/to/old/dir~

##
# How to list all entries under the current directory?  all files?  all directories?  all links?

    % print -l **/*
      │      │
      │      └ put each  entry on its own line instead  of everything on a
      │        single line
      │
      └ zsh shell builtin

    % print -l **/*(.)
    % print -l **/*(/)
    % print -l **/*(@)

# How to execute a command without any shell construct interfering (alias, builtin, function)?

Prefix the command with `env`:

    env [environment variables] <your command>

`env` is  an external  program; it  has no knowledge  of all  the shell-specific
constructs.

<https://unix.stackexchange.com/a/103474/289772>

##
# How to insert the argument of the last command on
## the current interactive command-line?

Press `M-.`.

## on the current scripted command?

Use the special parameter `$_`.

It's especially useful in a script to avoid repeating oneself:

    mkdir -p /long/path/to/dir/
    cd $_

##
##
##
# Quoting
## What is the purpose of quoting?

It's used to remove the special meaning of certain characters or words to the shell.

### Where can I find more info about it?

    man bash /QUOTING

##
## What are the three quoting mechanisms?

The escape character, single quotes, and double quotes.

### What is the escape character?

A non-quoted backslash.

##
## Which characters retain their special meaning within double quotes?

   - `$`
   - `` ` ``
   - `\`
   - `!`

Note that `\` is special only if followed by either of:

   - `$`
   - `` ` ``
   - `\`
   - `"`
   - newline

Also, `!` is special only if history expansion is enabled.
Besides, some characters may inhibit the expansion when they follow immediately.
See `man bash /HISTORY EXPANSION`, and `man zshexpn /HISTORY EXPANSION`.

## Which character gets a new special meaning when quoted?

The newline.

Quoting a newline suppresses its original special meaning (which is to terminate
the input buffer and run it), and gives it a new one (line continuation).

Yes, a line continuation is a  special meaning, because in effect, `\newline` is
removed from the input stream and ignored.

##
## When does the shell remove a backslash?

Outside quotes, always, unless it's quoted by another backslash.
This is similar to what VimL and tmux do with non-literal strings.

    $ printf '%s' a \z b
    azb~

    $ printf '%s' a \\z b
    a\zb~

Inside single quotes, never:

    $ printf '%s' 'a \z b'
    a \z b~

    $ printf '%s' 'a \\z b'
    a \\z b~

Inside double quotes, whenever it's used to remove the special meaning of the next character.

    $ printf '%s' "a \$$ b"
    a $$ b~

    $ printf '%s' "a \z b"
    a \z b~

### What is the exception?

Inside double quotes, the backslash is not removed in front of `!`, in bash and in sh:

    $ bash
    $ printf '%s' "\!\!"
    \!\!~

    $ sh
    $ printf '%s' "\!\!"
    \!\!~

Although, it is in zsh:

    $ zsh
    $ echo '%s' "\!\!"
    !!~

##
## Why should I use `printf` instead of `echo` when testing how the shell processes a string?  (2)

`echo` can add an additional processing, which translates some backslash-escaped
characters (like `\t` or `\u00e9`), after the shell has processed the command.

This makes the reasoning  about what the shell really does  more complex than it
should be.

Besides, `echo` is inconsistent across various shells:

    $ bash -c 'echo "a\u00e9b"'
    a\u00e9b~

    $ sh -c 'echo "a\u00e9b"'
    a\u00e9b~

    $ zsh -c 'echo "a\u00e9b"'
    aéb~

OTOH, by default,  `printf` never translates anything, and  is consistent across
all popular shells:

    $ bash -c 'printf "%s" "a\u00e9b"'
    a\u00e9b~

    $ sh -c 'printf "%s" "a\u00e9b"'
    a\u00e9b~

    $ zsh -c 'printf "%s" "a\u00e9b"'
    a\u00e9b~

---

Note that bash's  `echo` can translate some  backslash-escaped characters like
in zsh, but only if you pass it the `-e` flag.

### Why should I always use a format (like `'%s'`) and not just a string?

Inside a format `printf` removes  any backslash considered to be special, like
the shell does in a double-quoted string.

    $ printf 'a \\z b'
    a \z b~

    $ printf 'a \t b'
    a 	 b~

OTOH, if you use a format, the string won't be altered by `printf`:

    $ printf '%s' 'a \\z b'
    a \\z b~

### What happens if I have more arguments than `%` directives?

The format is reused as many times as necessary to consume all the arguments.

From `$ info printf`:

>     • The FORMAT argument is reused as necessary to convert all the given
>       ARGUMENTs.  For example, the command ‘printf %s a b’ outputs ‘ab’.

##
## ?

Certains caractères ont un sens spécial pour le shell.
Entre autres:    space Tab \n * $ ( ) !

Pour empêcher le shell d'interpréter un caractère de ce type, il faut le quoter.
Pour ce faire, on peut utiliser 3 syntaxes:

   - l'encadrer avec des single quotes
   - "                   double "
   - le préfixer avec un backslash

Les single/double quotes permettent de protéger une zone de texte entière, tandis que le backslash
permet une approche plus granulaire.


    ls
    echo "hello world!!"
    hello worldls    ✘~

    ls
    echo 'hello world!!'
    hello world      ✔~

            Les double quotes ne sont pas aussi strictes que les single quotes.
            Ils autorisent le développement de:

                    - commande:        "$(cmd)"

                    - variable:        "$myvar"

                    - l'historique:    "!!"


    myvar="foo
    > bar
    > baz"

    echo $myvar
    foo bar baz~

    echo "$myvar"
    foo~
    bar~
    baz~

            Illustre que bash réalise un field  splitting sur la chaîne issue du
            développement d'une variable.

            En  effet, dans  la 1e  commande, il  casse le  contenu de  `$myvar`
            (“foo\nbar\nbaz“) à chaque  fois qu'il rencontre un  newline, ce qui
            produit les 3 arguments `foo`, `bar`, `baz`.
            Il passe  ces 3 arguments à  `echo` qui les affiche  en les séparant
            par un espace.

            Pour empêcher bash d'interpréter  les newlines comme des séparateurs
            d'arguments, il faut quoter le contenu de la variable.


                                     NOTE:

            zsh se comporte  différemment, il ne réalise pas  de field splitting
            sur  une chaîne  développée à  partir d'une  variable (sauf  si vous
            activez l'option 'SH_WORD_SPLIT').

            Dans zsh, il n'y a donc pas besoin de quoter `myvar`:

                    echo $myvar
                    foo~
                    bar~
                    baz~


                                     NOTE:

            Au passage, on remarque la présence du prompt secondaire:

                    - >         dans bash
                    - quote>    dans zsh (`dquote>` pour un double quote)


    echo $'foo\nbar'

            Affiche `foo` et `bar` sur 2 lignes.

            La syntaxe $'string' permet d'inclure des caractères spéciaux dans une chaîne:

                   ┌────────┬──────────────────────────────────────────────────────────────────┐
                   │ \b     │ backspace                                                        │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \e     │ escape                                                           │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \f     │ form feed                                                        │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \n     │ new line                                                         │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \r     │ carriage return                                                  │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \t     │ horizontal tab                                                   │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \v     │ vertical tab                                                     │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \\     │ backslash                                                        │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \'     │ single quote                                                     │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \"     │ double quote                                                     │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \cx    │ un caractère C-x (C-a, C-b, ...)                                 │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \123   │ le caractère dont le code octal est 123 (1 à 3 chiffres)         │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \x21   │ le caractère dont le code hexa est 21 (1 à 2 chiffres)           │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │ \u2010 │ le caractère unicode dont le code hexa est 2010 (1 à 4 chiffres) │
                   ├────────┼──────────────────────────────────────────────────────────────────┤
                   │\U10100 │ "                                         10100 (1 à 8 chiffres) │
                   └────────┴──────────────────────────────────────────────────────────────────┘


            Le dollar n'a pas l'air d'être nécessaire pour zsh.

            Pour plus d'infos, lire `man bash`, section ’QUOTING’.

##
# Getting info
## How to get
### the name of the shell I'm using?

    ps -p $$
    PID TTY          TIME CMD~
    21107 pts/11   00:00:00 zsh~

    ps -p $$ -o comm=
    zsh~

Note that, with `-o comm=`, the name of the command is truncated to 15 characters.
But it shouldn't be an issue, as a shell name should be shorter.

---

`$0` is unreliable because you can set the name of a program with `ARGV0`:

    $ ARGV0=sh zsh
    $ echo $0
    sh~
    ^ ✘

For the same reason, don't omit the `-p` option passed to `ps(1)`:

    $ ARGV0=sh zsh
    $ ps $$
    PID  TTY      STAT   TIME COMMAND~
    1234 pts/10   S      0:00 sh~
                              ^
                              ✘

---

`$SHELL` is unreliable, since anything can reset its value.

### the options which have been set during bash invocation (`bash -...`)?

    echo $-

### the pid of the current shell?

        echo $$

### the pid of the parent of the current shell?

        echo $PPID

### the name of the current (pseudo) terminal?

        $ tty

##
## How to start and stop a stopwatch to measure how much time has elapsed between 2 events?

    $ time cat
    # focus a different terminal/tmux pane
    # do your things
    # focus back the terminal running `$ time cat`
    C-d

##
# Environment
## How to print all the environment variables of the current shell?

    $ env

You could also use `printenv`, but `env`  is POSIX and more powerful, because it
also lets you set an environment variable.

## How to get the environment of a shell started from a graphical application?

    Alt-F1
    xterm -e bash --noprofile --norc
                    │           │
                    │           └ do not read: ~/.bashrc
                    └ do not read: /etc/profile, ~/.bash_profile, ~/.bash_login, ~/.profile
    $ env

Alternatively, if the shell started by your GUI application is zsh:

    Alt-F1
    xterm -e zsh -f -d
    % env

## How to get the file from which an environment variable got its value?

    # Print commands and their arguments as they are executed.
    % zsh -xl >/tmp/log 2>&1
           ││
           │└ enable the LOGIN option; this is a login shell
           │
           └ Enables the XTRACE option.

    % exit

If  your variable  is not  in there,  then the  shell probably  inherited it  on
startup, which means that it was set before in some system config file.
You can try to find the file with:

    % find /etc -type f -exec grep -F YOUR_VAR {} +
    % find ~    -type f -exec grep -F YOUR_VAR {} +
                                    │             │
                                    │             └ run `grep(1)` only once:
                                    │                   grep ... file1 file2 ...
                                    │
                                    │               instead of:
                                    │                   grep ... file1
                                    │                   grep ... file2
                                    │                   ...
                                    │
                                    └ interpret YOUR_VAR as a fixed string (instead of a regex)

For more info, see:
<https://unix.stackexchange.com/a/154971/289772>

##
## Where is PATH initialised?

It depends on the OS.

For Ubuntu, have a look at:

   - /etc/login.defs
   - /etc/environment

For more info, see:

   - `man login`
   - <http://unix.stackexchange.com/a/228167>

##
## When a program needs to start a shell, how does it decide which one to use?

It looks at `$SHELL`.

If the variable is unset, it then looks into `/etc/passwd`.
More specifically, it searches for the line  starting with the name of the user,
then on that line, it grabs the last field.

## What's the benefit of the variable compared to the file?

`$SHELL` allows a more granular configuration of the default shell.
On a per-shell basis.
IOW, you  can have 2  shell sessions, each  configured with a  different default
shell.

OTOH, `/etc/passwd` stores a system wide configuration.

##
## How to start the xfce4 terminal, with bash automatically opened?

    SHELL=/bin/bash xfce4-terminal &!

##
## If I start a bash shell from zsh, does the value of `$SHELL` reflects the new shell?

No.

`$SHELL` keeps its old value (`/bin/zsh`).

##
# Hash table
## What's the command hash table?

Whenever you  ask the  shell to execute  a command,  it has to  look in  all the
directories of `$PATH`.
After having found  the full path to the  command, it saves it in  a table whose
elements look like this:

    command=/path/to/command

The next time you'll ask to execute the same command, the shell won't re-look in
`$PATH` but in the table, which is  probably faster (maybe because the latter is
compiled...).

Note that in zsh, as soon as you execute a command, the shell populates the hash
table with all  the commands available in `$PATH` immediately  (i.e. without you
having to execute any of them in the first place).

## How to print the contents of the command hash table?

    $ hash

## How to empty it?

    $ hash -r

## When should I empty it?

When the  shell finds  a wrong  location, and you  don't want  to restart  a new
shell.

Example:

      ┌ you could also use `echo` in zsh, and `echo -e` in bash
      │
      │           ┌ necessary for zsh
      │           │
    $ printf -- "#\!/bin/bash\necho 'from ~/.local/bin'" >~/.local/bin/sh.sh && \
      chmod +x ~/.local/bin/sh.sh

    $ sh.sh
    from ~/.local/bin    ✔~

    $ printf -- "#\!/bin/bash\necho 'from ~/bin'" >~/bin/sh.sh && \
      chmod +x ~/bin/sh.sh

    $ sh.sh
    from ~/.local/bin    ✘~

    $ hash -r && sh.sh
    from ~/bin     ✔~

    # clean up the useless scripts
    $ rm ~/{,.local/}bin/sh.sh

This example assumes  that `~/bin` and `~/.local/bin` are both  in your `$PATH`,
and that `~/bin` comes first.

##
# Brace expansion
## How to create a backup file for `/long/path/to/file.txt`, with a single command, and a single argument?

    $ cp /long/path/to/file.txt{,.bak}

## How to create a backup file for all the files in the current directory by prefixing their name with `OLD-`?

    for f in *; do
      cp {,OLD-}"${f}"
    done

##
# Filename generation
## Which option controls how the shell handles a glob from which no filename can be generated?

In zsh, it's `nomatch`.
In bash, it's `failglob`.

## What's its default value?

In zsh, `nomatch` is set.
In bash, `failglob` is NOT set.

## How does it affect the shell when it's set?

A failed filename generation makes the shell raise an error, and stop processing
the script.

MWE:

    printf "shopt -s failglob ; echo *.foo ; echo afterwards"  | bash
    bash: line 2: no match: *.foo~

    bash -c 'shopt -s failglob; echo *.foo; echo afterwards'
    bash: no match: *.foo~

    printf "setopt nomatch; echo *.foo \n echo afterwards" | zsh
    zsh: no matches found: *.foo~


None  of these  commands print  'afterwards', which  illustrates that  the shell
stopped processing the script as soon as it failed to expand the glob.

---

But weirdly, this command is still able to print 'afterwards':

    printf "shopt -s failglob \n echo *.foo \n echo afterwards" | bash
    bash: line 2: no match: *.foo~
      afterwards~

Same thing if you replace the first newline with a semicolon (but not the second one).

## How does it affect the shell when it's NOT set?

A failed filename generation doesn't raise an  error, and the glob is treated as
a single element:

    % unsetopt nomatch; echo *.foo; echo 'afterwards'
    *.foo~
      afterwards~

    $ shopt -u failglob; echo *.foo; echo 'afterwards'
    *.foo~
      afterwards~

---

In reality, it's  a bit more complex, because several  other options exist which
have an effect on the shell's behavior when a glob can't be expanded.
In particular, if the `nullglob` option is set, the glob is ignored:

    % setopt null_glob; unsetopt nomatch; echo *.foo; echo 'afterwards'
    afterwards (no error)~

    $ shopt -s nullglob; shopt -u failglob; echo *.foo; echo 'afterwards'
    afterwards (no error)~

##
# Editing output
## How to keep only the first 20 characters in the output of a command?  In each line of a file?

    $ cmd | cut -c1-20

    $ cut -c1-20 file

## What's the shortest command to repeat the last command, but this time keeping only the first 10 characters?

    $ ^2^1

##
## My command output is a single column of words.  How to format it into a table?

    $ cmd | column
            │
            └ included in the `bsdmainutils` package

Example:

    $ printf -- '%s\n' word_{1..123} | column

## What does affect the number of columns in the table?

`$COLUMNS` and the length of the longest word.

The longer is the longest word, the less columns there is in the table.

## Which character(s) does `column(1)` add between 2 words to align them?

Tab characters.

## How many terminal cells do each of these characters occupy?

The first tab between two words on a line can occupy from 1 to 8 cells.
The next one(s), if any, occupy 8 cells.

## How to limit the width of the table to 50 terminal cells?

        $ cmd | column -c50

##
## My command output is already a table, but the columns are not correctly aligned.  How to align them?

        $ cmd | column -t
                       ^^

## The columns are filled before the rows.  How to fill the rows first?

        $ cmd | column -t -x
                          ^^

## These commands assume that my columns are separated by whitespace.  But they are separated by colons!

        $ cmd | column -t -s:
                          ^-^

##
## My command output is a whitespace separated list of 12 words.  How to format it into a 3 rows x 4 columns table?

    $ cmd | pr -t -l3 -4
            │  │  │   │
            │  │  │   └ -COLUMN, --columns=COLUMN
            │  │  │
            │  │  │     Output 4 columns and print them down.
            │  │  │     Balance number of lines in the columns on each page.
            │  │  │
            │  │  └ -l, --length
            │  │
            │  │    Set the page length to 3 lines.
            │  │
            │  └ -t, --omit-header
            │
            │    Omit page headers and trailers.
            │
            └ convert text files for printing

                  included in the `coreutils` package

Example:

    $ printf -- '%s\n' word_{1..12} | pr -t -l3 -4

## The columns are filled before the rows.  How to fill the rows first?

Add the `-a` option (`--across`):

        $ cmd | pr -t -l3 -4 -a

## What happens if I use one of these commands, but my command output contains 24 words?

`pr(1)` will format the  first 12 words in a page, then format  the 12 next ones
in a second page.
The  two pages  will  appear next  to  each  other, which  will  give the  false
impression that there's a single page.

##
# Issues
## I'm trying to run a shell command, but it doesn't work as I would expect!  (2)

Write it in a file and press `|c` to make shellcheck lint it.
If any error appears in the quickfix  window, press `gx` on it to get redirected
to the shellcheck wiki where the issue will be described in detail.

Also,  consider using  our  `args` script  to  check how  the  shell splits  the
commands into words:

    $ cat <<'EOF' >~/bin/args
    #!/bin/bash
    printf -- '%d args:' $#
    printf -- ' <%s>' "$@"
    printf -- '\n'
    EOF

    $ args my buggy command
    3 args: <my> <buggy> <command>~

## I'm trying to run a command whose arguments are generated by the output of another command.  Sometimes it fails!

A command substitution should be used only  to generate data, not code (i.e. not
command names or argument): <https://mywiki.wooledge.org/BashFAQ/050>

---

    ✔
    $ tmux set @foo 'if -F 1 "display"' ; \
      tmux $(tmux show -v @foo)

    ✘
    $ tmux set @foo 'if -F 1 "display test"' ; \
      tmux $(tmux show -v @foo)
      syntax error~

This is because:

   1. quoting is performed before command substitution, so when it occurs,
      `$(tmux show -v @foo)` has not been expanded yet, and the quotes around
      `"display test"` can't be interpreted as syntactical, because they don't
      exist yet

   2. an unquoted command substitution is followed by word splitting

   3. when the word splitting occurs, the quotes around `"display test"` are
      parsed as literal (quoting is done, it's too late for them to be parsed
      as syntactical); so the shell splits `"display test"` into `"display` and `test"`

You can check how the command is split using our `args` script:

    $ args $(tmux show -v @foo)
    5 args: <if> <-F> <1> <"display> <test">~

    $ args if -F 1 "display test"
    4 args: <if> <-F> <1> <display test>~

---

In the previous example, using `eval` could work:

    $ tmux set @foo 'if -F 1 "display test"' ; \
      eval "tmux $(tmux show -v @foo)"

but sometimes, it may also give [unexpected results][1], idk.

Here, a better approach is to simply save the output of `$ tmux show -v @foo` in
a file, and make tmux source it.

More generally,  depending on what  you're trying to achieve,  several solutions
exist: <https://mywiki.wooledge.org/BashFAQ/050>

##
##
##
# Scripts
## How to exit
### a `for`/`while` loop?

Use `break`.

### a script or a shell?

Use `exit`.

### a function or a sourced file?

Use `return`.

##
## array
### How to assign a value to a member of an array?

    arr[<number>]=<val>

---

    $ arr[123]=test ; \
      echo ${arr[123]}
    test~

### How to convert a string of space-separated words into an array?

    arr=($str)

---

    $ str='foo bar baz' ; \
      arr=($str)        ; \
      printf -- '%s\n' "${arr[@]}"
      foo~
      bar~
      baz~

##
## conventions / bonnes habitudes

    myvar1=val1
    myvar2=val2
    ...
    code using "$myvar1", "$myvar2", ...

            Stocker toutes les valeurs qui sont susceptibles de changer un jour dans des variables
            déclarées au tout début du script.

            Ça facilite le changement de configuration du script, car toutes les options sont écrites
            au tout début, pas besoin de les chercher.

            Ça crée également un point de centralisation.
            Sans lui, le jour où on veut changer une valeur, il faudra retrouver tous les endroits
            où elle est utilisée.


    myscript=$(basename $0)
    ...
    echo "[$myscript] my status msg" 1>&2

            Écrit le message de statut “my status msg“ dans la sortie d'erreur.

            La redirection `1>&2` n'affecte que la commande `echo`, pas le script entier.

            Quel intérêt à cette commande?

            Dissocie les messages de statuts, utiles uniquement pdt l'exécution du script pour voir
            ce qu'il fait/où il en est, des messages réellement intéressants.
            Si on redirige la sortie du script dans un fichier, ce dernier ne sera pas pollué par
            les messages de statuts.

## debug

    unsetopt GLOBAL_RCS (disable system wide config files)
    ⇔
    % zsh +d
          │
          └ + = unset option
            - = set option


                       ┌─ timestamps relatifs (Incrémentaux)
                       │
                       │  ┌─ format:  `%.s` est spécifique à `ts`, et fournit une précision
                       │  │           de 6 chiffres après la virgule
                       │  │
    zsh -xv 2>&1 | ts -i "%.s" > zsh_startup.log
         ││
         │└─ active l'option `VERBOSE`
         └─ active l'option `XTRACE`
    C-d

            Loguer les appels systèmes/fonctions exécutées par `s` dans un fichier.


                                     NOTE:

            Le timestamp devant une commande correspond au temps pris par la commande précédente.


                                     NOTE:

            Pour arrêter le logging, il faut exécuter `exit`, ou taper C-d.

            Une fois, le fichier généré, on y cherchera les patterns:

                    \v^%(0)@!
                    \v^%(0.0)@!
                    \v^%(0.00)@!
                    ...

            ... pour trouver les commandes qui ont pris, resp., plus d'une seconde, un dizième, centième, ...
            de seconde.


    #!/bin/sh -xv

            Le script écrit sur sa sortie d'erreur:

                    - son code (entrée standard), au fur et à mesure qu'il le lit
                    - chaque commande (précédée d'un signe `+`), avant de l'exécuter

            On remarque qu'un script lit intégralement son code avant de commencer son exécution.

            Mnémotechnique: -x = xtrace
                            -v = verbose


    zsh -f -d

            Lance zsh sans fichier de conf (`man zshoptions /NO_RCS`; `man zshoptions /GLOBAL_RCS`).
            Update: zshenv is still sourced.


    logger -i  MSG
    logger -is MSG
    logger -fi FILE

            Dans `/var/log/syslog`, logue:

                    - MSG, en incluant le pid du processus `logger`
                    - idem mais en l'écrivant aussi sur la sortie d'erreur
                    - le contenu de FILE

            `logger`  est  une  commande   shell  permettant  d'enregistrer  des
            messages dans le log système.


    logger -p PRIORITY MSG

            PRIORITY peut être un nb ou une paire `facility.level`.
            Dans ce cas, `facility` et `level` peuvent prendre les valeurs suivantes:

                    ┌─────────────────┬───────────────────────────────────────────┐
                    │ facility        │ Signification                             │
                    ├─────────────────┼───────────────────────────────────────────┤
                    │ auth            │ messages de sécurité/autorisation         │
                    │ authpriv        │ idem mais à usage privé                   │
                    │ cron            │ démon horloge (cron et at)                │
                    │ daemon          │ démons système divers                     │
                    │ ftp             │ démon ftp                                 │
                    │ lpr             │ sous-système lpr  (line printer)          │
                    │ mail            │ sous-système mail                         │
                    │ news            │ USENET news subsystem                     │
                    │ syslog          │ messages générés en interne par `syslogd` │
                    │ user            │ messages génériques de l'utilisateur      │
                    │ uucp            │ UUCP subsystem                            │
                    │ local0 à local7 │ réservés pour un usage local              │
                    └─────────────────┴───────────────────────────────────────────┘


                    ┌─────────┬──────────────────────────────────────────┐
                    │ level   │ signification                            │
                    ├─────────┼──────────────────────────────────────────┤
                    │ emerg   │ système inutilisable                     │
                    │ alert   │ une action doit intervenir immédiatement │
                    │ crit    │ état critique                            │
                    │ err     │ "    contenant une erreur                │
                    │ warning │ "              un  avertissement         │
                    │ notice  │ "    normal, mais significatif           │
                    │ info    │ message d'information                    │
                    │ debug   │ message de déboguage                     │
                    └─────────┴──────────────────────────────────────────┘


            Les valeurs de `facility` et `level` spécifient resp.:

                    - le type du pgm qui logue le message
                    - son importance

            Par défaut, les messages enregistrés par `logger` reçoivent la priorité `user.notice`.

            `authpriv` est utilisé pour loguer des info de sécurité de nature sensible.


    logger -t TAG MSG

            Enregistre MSG avec le tag TAG.
            Par défaut, les messages enregistrés reçoivent le tag `logger`.


    exec 1> >(logger -s -t $(basename $0)) 2>&1

            Écrit les sorties standard et erreur du shell courant dans `/var/log/syslog`.

            Explication:

                            >(some-command)

            ... a 2 effets:

                    - retourne un fd vers lequel on peut rediriger un flux de données
                    - connecte l'entrée de `some-command` à ce fd


                            exec 1> FD 2>&1

            ... redirige les sorties standard et erreur du shell courant vers FD.

            Donc:

                            exec 1> >(some-command) 2>&1

            ... pipe la sortie du shell vers l'entrée standard de `some-command`.

                            logger -s -t $(basename $0)

            ... `logger` écrit tout ce qui est écrit sur son entrée standard:

                    - dans `/var/log/syslog` en taguant (`-t`) chaque message avec le nom du script courant
                    - sur sa sortie standard (`-s`)

        TODO:

        Pour + d'infos lire:

                http://urbanautomaton.com/blog/2014/09/09/redirecting-bash-script-output-to-syslog/

## declare

    declare

            Affiche les attributs et valeurs de toutes les variables existantes dans l'environnement
            courant.

            Synopsis simplifié de la commande:

                    declare [-aAfgirx] [-p] [name[=value] ...]


                                     NOTE:

            `typeset` et `declare` sont synonymes dans bash et zsh.
            `typeset` est obsolète dans bash, selon `help typeset`.


    declare -p    var1 var2
    declare -p -f myfunc
             │
             └ print

            Affiche les attributs et valeurs de `var1` et `var2`.
            "                                de `myfunc`

            Il est nécessaire de passer le flag `-f` à `declare` qd on veut afficher la valeur
            d'une fonction, autrement le shell ne la trouvera pas.


    function myfunc () {
      declare -g myvar=123
    }

            Crée la variable globale `myvar` et lui affecte la valeur `123`.

            Dans une  fonction, `declare` (tout comme  `local`) limite la portée  d'une variable à
            la fonction et à ses enfants. `-g` supprime ce comportement et rend la variable globale.


    ┌──────────────────┬──────────────────────────────────────────────────────────┐
    │ declare -a myvar │ convertit myvar en array indexée par des nombres (liste) │
    ├──────────────────┼──────────────────────────────────────────────────────────┤
    │ declare -A myvar │ convertit myvar en array associative (dico)              │
    ├──────────────────┼──────────────────────────────────────────────────────────┤
    │ declare -i myvar │ convertit myvar en nombre                                │
    ├──────────────────┼──────────────────────────────────────────────────────────┤
    │ declare -r myvar │ déclare que myvar est read-only                          │
    ├──────────────────┼──────────────────────────────────────────────────────────┤
    │ declare -x myvar │ exporte myvar dans l'environnement des futures commandes │
    └──────────────────┴──────────────────────────────────────────────────────────┘

            Techniquement, `declare`  permet de donner un  attribut à une variable.  Si la variable
            n'existe pas, elle est créée au passage.


                                     NOTE:

            Pour supprimer un attribut, il faut remplacer `-` par `+`:

                    declare +a myvar

            ... supprime l'attribut array de `myvar`.


    declare -i var=123
    var='hello'
    echo $var
    0~

            La chaîne 'hello' a été convertie en le nombre 0, car `var` porte l'attribut `-i`,
            ce qui signifie qu'elle ne peut contenir qu'un nombre.


    declare -r myvar
    myvar='hello'       ✘
    unset myvar         ✘
    exec bash|zsh       ✔

            On ne peut ni modifier ni supprimer une variable read-only.

            La seule solution si on veut vraiment s'en débarrasser, est de relancer le shell via `exec`.
            Le shell lit sa conf', et toutes les variables créées au cours de la session sont perdues.

## read

    read foo

            Demande de saisir une chaîne qui va être affectée à la variable `foo`.


    read -p 'Veuillez saisir foo : ' foo

            Affiche le prompt "Veuillez saisir foo" pour accompagner la demande d'input.


    `read` accepte plusieurs arguments, entre autres:

            ┌────────────┬──────────────────────────────────────────────────────────────────┐
            │ -e         │ permet d'utiliser les raccourcis readline pendant la saisie      │
            ├────────────┼──────────────────────────────────────────────────────────────────┤
            │ -i "hello" │ ajoute automatiquement "hello" au sein de l'input                │
            │            │                                                                  │
            │            │ ne fonctionne que si readline est utilisée (flag `-e`)           │
            ├────────────┼──────────────────────────────────────────────────────────────────┤
            │ -n 12      │ limiter l'input à 12 caractères                                  │
            ├────────────┼──────────────────────────────────────────────────────────────────┤
            │ -r         │ un backslash n'est pas interprété (donc pas supprimé) ; mode raw │
            ├────────────┼──────────────────────────────────────────────────────────────────┤
            │ -s         │ mode silencieux ; l'input n'est pas echo sur la sortie standard  │
            ├────────────┼──────────────────────────────────────────────────────────────────┤
            │ -t 34      │ impose un timeout de 34 secondes                                 │
            └────────────┴──────────────────────────────────────────────────────────────────┘


## repeat

    repeat 10  echo 'hello'
    repeat '5*2' do myvar='hello'; echo "${myvar}"; done
    repeat '5*2'
        do
               myvar='hello'
               echo "${myvar}"
        done

            Affiche 'hello' 10 fois. `repeat` est décrit dans `man zshmisc`.


                                     NOTE:

            L'expression qui suit `repeat` est développée et évaluée en un nombre.
            Dans les derniers exemples précédents, l'expression contient `*`.
            Pour empêcher ce dernier d'être développé, il faut le quoter.

## test
### syntaxe

    test e       test ! e
    [ e ]        [ ! e ]
    [[ e ]]      [[ ! e ]]

            L'expression `e` est vraie / fausse.

            `test`, `[` et `[[` sont des commandes.
            `]` et `]]` sont des arguments de `[` et `[[`, raison pour laquelle il faut mettre
            des espaces entre `e` et les crochets.


    false ; echo $?

            Affiche 1.

            Pour le  shell, 0  est vrai  et n'importe  quel nombre compris  entre 1  et 255  est une
            erreur. En cela, il diffère de  nombreux languages de programmation, qui considèrent 0
            comme faux et 1 comme vrai.


    test ; echo $?
    1~
    [ ]  ; echo $?
    1~

            L'omission d'une expression dans un test équivaut à une expression fausse.
            Peut-être car le shell estime qu'il a échoué à évaluer une expression.


    [ e1 -a e2 ]    [[ e1 && e2 ]]
    [ e1 -o e2 ]    [[ e1 || e2 ]]

            `e1` ET `e2` sont vraies
            "    OU "


    if cmd >/dev/null 2>&1; then
      some_code
    fi

            Exécute `some_code` uniquement si `cmd` a réussi (code de sortie nul).
            Illustre qu'on peut utiliser une commande à la place d'une expression dans une structure
            de contrôle `if` (et `while`?).

### chaînes

    ┌───────────────┬────────────────────────────────────────────────────┐
    │ -z s          │ `s` est une chaîne vide                            │
    │ -n s    s     │ "                  non vide                        │
    ├───────────────┼────────────────────────────────────────────────────┤
    │ s1 = s2       │ `s1` et `s2` sont identiques                       │
    │               │                                                    │
    │ s1 != s2      │ "                 différentes                      │
    ├───────────────┼────────────────────────────────────────────────────┤
    │ [[ s == p ]]  │  le pattern `pat` décrit une sous-chaîne de `s`    │
    ├───────────────┼────────────────────────────────────────────────────┤
    │ s1 < s2       │ `s1` arrive avant `s2` dans un tri lexicographique │
    │ s1 > s2       │ "           après "                                │
    └───────────────┴────────────────────────────────────────────────────┘

    `[[ s == p ]]` fonctionne dans bash, mais n'est pas POSIX. Voici une syntaxe plus portable:

            case "s" in
              p) echo 'match' ;;
              *) echo 'nomatch' ;;
            esac

### fichiers / dossiers

    ┌────────────┬────────────────────────────────────────────────────────┐
    │ expression │ signification                                          │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -e file    │ existe                                                 │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -b file    │ block device                                           │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -c file    │ character device                                       │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -d file    │ dossier                                                │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -f file    │ fichier régulier (!= lien symbolique)                  │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -g file    │ a l'attribut `setgid`                                  │
    │            │                                                        │
    │            │ Qd le fichier est exécuté, le processus qui en résulte │
    │            │ a les mêmes droits que le groupe du fichier.           │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -G file    │ possédé par le groupe courant                          │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -k file    │ le sticky bit est activé                               │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -L file    │ lien symbolique                                        │
    │ -h file    │                                                        │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -N file    │ modifié après qu'on l'ait lu pour la dernière fois     │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -O file    │ possédé par l'utilisateur courant                      │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -p file    │ named pipe (FIFO)                                      │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -r file    │ lisible                                                │
    │ -w file    │ modifiable                                             │
    │ -x file    │ exécutable                                             │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -s file    │ taille > 0                                             │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -S file    │ socket                                                 │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -t file    │ le fd de `file` est ouvert et se réfère à un terminal  │
    ├────────────┼────────────────────────────────────────────────────────┤
    │ -u file    │ a l'attribut `setuid`                                  │
    │            │                                                        │
    │            │ Qd le fichier est exécuté, le processus qui en résulte │
    │            │ a les mêmes droits que le proprio du fichier.          │
    └────────────┴────────────────────────────────────────────────────────┘

    En-dehors  des  expressions  utilisant  `-L`  ou  `-h`,  toutes  les  autres
    déréférencent un lien symbolique.
    Ça veut  dire qu'elles n'affirment  rien à propos  du lien lui-même,  mais à
    propos de sa cible.


    file1 -ef file2

            `file1` et `file2` se réfèrent au même fichier (même n° de device et d'inode).


    file1 -nt file2
    file1 -ot file2

            `file1` est plus récent / ancien que `file2`.

            Mnémotechnique:

                 `nt` = newer than
                 `ot` = older than

            L'ancienneté est mesurée via la date de modification.

                                      NOTE:

            Un fichier qui n'existe pas est considéré comme plus ancien qu'un fichier existant.


    [[ -d ~/log ]] || mkdir ~/log

            Crée le dossier `~/log` s'il n'existe pas.

            Cette commande  montre que l'opérateur  logique `||` (OU)  peut être
            utilisé pour construire une instruction du type:

                    si A est faux, faire B

            ... A étant un test, B une action.

            Cela fonctionne probablement pour 2 raisons.
            D'abord, bash parse la ligne de commande de gauche à droite.
            Et si A est vrai, il ne teste pas B (car la proposition ’A ou B’ est
            vraie peu importe B).
            En revanche, si A  est faux, il doit encore tester  B pour savoir si
            ’A ou B’ est vraie.

            Ensuite, en demandant à vérifier si le code de sortie de la commande
            `mkdir ~/log` est 1 (B est vrai), on crée un dossier.

            De la  même façon, l'opérateur  logique `&&` (ET) peut  être utilisé
            pour construire une instruction du type:

                    si A est vrai, faire B

            On pourrait remplacer `||` par l'opérateur logique `!` :

                    [[ ! -d ~/log ]] && mkdir ~/log

            Résumé:

                    A || B    si A est faux, faire B
                    A && B    si A est vrai, faire B


    TODO: if true; then false; else echo 'boom' ; fi

    if true; then
      false
    else
      echo 'boom'
    fi

### nombres

    n1 <op> n2

              ┌──────┬──────────────────┐
              │ <op> │ meaning          │
              ├──────┼──────────────────┤
              │ -eq  │ equal            │
              │      │                  │
              │ -ne  │ not equal        │
              │      │                  │
              │ -lt  │ lower than       │
              │      │                  │
              │ -gt  │ greater than     │
              │      │                  │
              │ -le  │ lower or equal   │
              │      │                  │
              │ -ge  │ greater or equal │
              └──────┴──────────────────┘

### options / variables

    -o optname

           L'option shell `optname` est activée.


    -v varname

           La variable shell `varname` est configurée: on lui a affecté une valeur.

## variable

    myvar='hello '

    echo "$myvarworld"      ✘
    echo "${myvar}world"    ✔

            Qd la valeur d'une variable est directement suivie de caractères pouvant être utilisés
            dans un nom de variable, le shell risque de se tromper et penser que le nom de la variable
            est plus long que ce qu'on voulait.

            Dans ce cas, pour éviter toute ambigüité, il faut entourer le nom avec des accolades.


    myvar=1
    myvar=$(($myvar*2+3))

    echo "$myvar"

            On n'utilise pas tout à fait la même chose pour faire référence au nom d'une variable
            ou à sa valeur:

                    - `myvar`  = nom
                    - `$myvar` = valeur

            En Vimscript, cette distinction n'existe pas:

                    let myvar = 1
                    let myvar = myvar*2 + 3

            On utilise `myvar` qu'on soit à gauche ou à droite de l'affectation.

##
# Configuration
## alias / fonctions

    https://github.com/robbyrussell/oh-my-zsh/wiki/Cheatsheet

            Inspiration pour des idées de nouveaux alias.


    echopid() }    echo $$
      echo $$
    }

            Si on écrit la  fonction `echopid()` dans un fichier sourcé par  le shell, on constate
            qu'elle affiche le même pid que la commande `echo $$` exécutée dans le shell courant.
            Ceci montre  qu'une fonction custom est  exécutée dans le processus  du shell courant.
            Elle est donc capable  de modifier son environnement. En particulier,  si elle change le
            répertoire courant, il faudra penser à le lui faire restaurer à la fin.

            De la  même façon,  si on  écrit `echo  $$` dans un  fichier et  qu'on le  source, on
            remarque qu'il  affiche le même pid  que celui du  shell. Là encore, ça  prouve qu'un
            fichier sourcé est exécuté dans le processus du shell.

            En revanche,  si on  écrit `echo $$`  dans un  script, avec ou  sans shebang,  et qu'on
            l'exécute, on  remarque qu'il affiche un  pid qui ne  correspond pas à celui  du shell
            courant, et qu'il est  incrémenté à chaque fois qu'on appelle  le script. Ceci prouve
            qu'un script est exécuté dans un sous-shell.


    exec bash
    exec zsh

            Remplace le shell courant par bash/zsh.

            Indirectement, ça resource la config du shell.
            C'est donc une commande pratique pour, pex, activer un nouvel alias qu'on vient de définir
            dans un fichier de conf.

            Cette commande ne lance pas un nouveau shell enfant. Elle remplace le shell courant.
            Même le pid reste inchangé (echo $$).

            `exec` est une commande intégrée à bash/zsh permettant de remplacer le processus courant
            (shell/script), par un pgm arbitraire.


    \ls
    'ls'
    /bin/ls
    command ls
    unalias ls

            Différentes façons  d'exécuter la commande  `ls`, qd on a  défini un
            alias du même nom.
            Les  2 premières  syntaxes quotent  la commande,  ce qui  empêche le
            shell de reconnaître l'alias `ls`.
            Le shell retirera les quotes plus  tard, mais ce sera trop tard pour
            que `ls` soit reconnu comme un alias.
            En  effet,   lors  du  traitement   d'une  ligne  de   commande,  le
            développement  d'alias a  lieu très  tôt, avant  la suppression  des
            quotes.


    type ls
    ls=$(command -v ls)

            Dans un shell  interactif, affiche la commande  complète en laquelle
            est développée l'alias `ls`.
            Dans un script, stocke cette même commande dans la variable `ls`.


                                     NOTE:

            Ne pas utiliser `which`, préférer `type`.

            En effet,  dans bash, `which` ne  semble pas tenir compte  des alias
            définis sur la ligne de commande, au cours de la session courante.
            Il  omet aussi  les  alias  définis dans  d'autres  fichiers, il  ne
            regarde que dans `~/.bashrc`.

            Dans  bash,  `which`  n'est qu'un  pgm  externe  (`/usr/bin/which`),
            tandis que `type` est une commande intégrée au shell.
            Elle a donc accès à plus d'info concernant ce dernier.

            Dans  zsh, il  semble  que `which`  et `type`  soient  toutes 2  des
            commandes intégrées, et donc toutes les 2 fiables.


    my_func() { echo hello ;}

            Contrairement  à zsh  (qui s'en  fout), bash  exige que  la dernière
            commande au sein d'une fonction se termine par un point-virgule.


                                     NOTE:

            bash et zsh  acceptent des noms de fonction incluant  un tiret, mais
            ce n'est pas le cas de tous les shells.

## locale

La localisation permet à un administrateur et aux utilisateurs d'un système de choisir, entre autres:

        - l'ordre lexicographique

        - le symbole pour la devise

        - le fuseau horaire (timezone)

        - l'ensemble des caractères supportés

        - le caractère décimal (ex: 1.23)
                                     - ^
        - le séparateur entre milliers (ex: 1,000,000)

        - la langue utilisée par les programmes
          notamment pour afficher leurs messages d'erreurs

        - le nom des mois de l'année et des jours de la semaine


La localisation (abrégée en `l10n`) s'oppose à l'internationalisation (`i18n`).


    sudo dpkg-reconfigure locales
    sudo locale-gen fr_FR.UTF-8

            Installer de nouvelles locales.
            Installer la locale fr_FR.UTF-8.


    locale -a

            Lister les locales ayant été générées sur le système.


    locale

            Affiche les 15 variables d'environnement liées à la localisation et leurs valeurs.

                    LANG
                    LANGUAGE
                    LC_ADDRESS
                    LC_ALL
                    LC_COLLATE
                    LC_CTYPE
                    LC_IDENTIFICATION
                    LC_MEASUREMENT
                    LC_MESSAGES
                    LC_MONETARY
                    LC_NAME
                    LC_NUMERIC
                    LC_PAPER
                    LC_TELEPHONE
                    LC_TIME

            `LC_ALL` a priorité sur toutes les autres.


    LC_TIME=fr_FR.UTF-8 date
    LC_MONETARY=fr_FR.UTF-8 locale currency_symbol

            Affiche la date en français, même si la locale pour le temps est américaine.
            Affiche la devise française, "

            Illustre qu'on peut changer la valeur d'une variable d'environnement liée à la localisation,
            le temps d'exécuter une commande, afin de modifier le comportement de cette dernière.


    LC_ALL=C cmd

            Exécute `cmd` en utilisant la locale C.

            La locale C est la plus simple des locales, et est particulièrement adaptée aux programmes,
            là où les autres sont destinées aux humains.
            Dans la locale C, tous les caractères sont encodés sur un seul octet, en ASCII.
            Le tri lexicographique est basé uniquement sur ces valeurs octets, et la langue est US.

            `LC_ALL` permet de s'assurer qu'on travaille avec une localisation totalement connue
            (généralement on choisit C), de sorte que le format de la sortie des commandes soit
            connu d'avance. Utile dans un script, ou pour une commande tq `grep` ou `sort`:

                    LC_ALL=C grep ...


                                     NOTE:

            On ne donnera pas la valeur `C` à `LC_ALL` dans un fichier sourcé par un shell interactif,
            si on veut pouvoir y taper des caractères accentués.


                                     TODO:

À terminer...

            https://unix.stackexchange.com/questions/87745/what-does-lc-all-c-do

            You generally run a command with LC_ALL=C to avoid the user's settings to interfere with
            your script. For instance, if you want [a-z]  to match the 26 ASCII characters from a to
            z, you have to set LC_ALL=C.

            On GNU systems,  LC_ALL=C and LC_ALL=POSIX (or  LC_MESSAGES=C|POSIX) override $LANGUAGE,
            while LC_ALL=anything-else wouldn't.

            A few cases where you typically need to set LC_ALL=C:

    sort -u or sort ... | uniq.... In many locales other than C, on some systems (notably GNU ones),
    some characters  have the same sorting  order. sort -u doesn't  report unique lines, but  one of
    each group of  lines that have equal sorting order.  So if you do want unique  lines, you need a
    locale where characters  are byte and all  characters have different sorting order  (which the C
    locale guarantees).

    the same  applies to the =  operator of POSIX compliant  expr or == operator  of POSIX compliant
    awks (mawk  and gawk are  not POSIX in  that regard), that don't  check whether two  strings are
    identical but whether they sort the same.

    Character ranges like  in grep. If you mean to  match a letter in the user's  language, use grep
    '[[:alpha:]]' and don't modify LC_ALL. But if you want to match the a-zA-Z ASCII characters, you
    need  either  LC_ALL=C  grep  '[[:alpha:]]'  or LC_ALL=C  grep  '[a-zA-Z]'.  [a-z]  matches  the
    characters that  sort after a  and before z  (though with many  APIs it's more  complicated than
    that). In  other locales, you  generally don't  know what those  are. For instance  some locales
    ignore case for sorting so [a-z] in some  APIs like bash patterns, could include [B-Z] or [A-Y].
    In many  UTF-8 locales  (including en_US.UTF-8 on  most systems), [a-z]  will include  the latin
    letters from a to y with diacritics but not those of z (since z sorts before them) which I can't
    imagine would be what you want (why would you want to include é and not ź?).

    floating point  arithmetic in ksh93. ksh93  honours the decimal_point setting  in LC_NUMERIC. If
    you write  a script that contains  a=$((1.2/7)), it will stop  working when run by  a user whose
    locale has comma as the decimal separator:

            % ksh93 -c 'echo $((1.1/2))'
            0.55
            % LANG=fr_FR.UTF-8  ksh93 -c 'echo $((1.1/2))'
            ksh93: 1.1/2: arithmetic syntax error

    Then you need things like:

            #! /bin/ksh93 -
            float input="$1" # get it as input from the user in his locale
            float output
            arith() { typeset LC_ALL=C; (($@)); }
            arith output=input/1.2 # use the dot here as it will be interpreted
                                # under LC_ALL=C
            echo "$output" # output in the user's locale

    As a side note: the , decimal separator conflicts with the , arithmetic operator which can cause
    even more confusion.

    When  you need  characters to  be bytes.  Nowadays,  most locales  are UTF-8  based which  means
    characters can take up from 1 to 6 bytes. When dealing with data that is meant to be bytes, with
    text utilities,  you'll want  to set  LC_ALL=C. It will  also improve  performance significantly
    because parsing UTF-8 data has a cost.
    a corollary of the previous point: when processing  text where you don't know what character set
    the input is  written in, but can assume  it's compatible with ASCII (as  virtually all charsets
    are). For instance grep '<.*>'  to look for lines containing a <, > pair  will no work if you're
    in a UTF-8 locale and the input is encoded in a single-byte 8-bit character set like iso8859-15.
    That's because . only  matches characters and non-ASCII characters in  iso8859-15 are likely not
    to form a  valid character in UTF-8. On  the other hand, LC_ALL=C grep '<.*>'  will work because
    any byte value forms a valid character in the C locale.

    Any time where you process  input data or output data that is not  intended from/for a human. If
    you're talking to a  user, you may want to use their convention  and language, but for instance,
    if you generate some  numbers to feed some other application that  expects English style decimal
    points, or English month names, you'll want to set LC_ALL=C:

            % printf '%g\n' 1e-2
            0,01
            % LC_ALL=C printf '%g\n' 1e-2
            0.01
            % date +%b
            août
            % LC_ALL=C date +%b
            Aug

    That  also applies  to  things like  case  insensitive comparison  (like in  grep  -i) and  case
    conversion (awk's toupper(), dd conv=ucase...). For instance:

            grep -i i

    is not guaranteed to match  on I in the user's locale. In some  Turkish locales for instance, it
    doesn't as  upper-case i is İ  (note the dot)  there and lower-case  I is ı (note  the missing
    dot).

## fichiers

    /etc/passwd

            Une fois le login shell configuré via `chsh`, le changement est pris en compte dans
            `/etc/passwd`, à la ligne de l'utilisateur courant.

            Le login shell est celui exécuté qd on se connecte dans une console TTY.
            Normalement, le login shell donne sa valeur à `$SHELL`, qui détermine le shell exécuté
            par défaut par divers programmes, dont les émulateurs de terminaux et `su`:

                    man -Kw '$SHELL'


Les tableaux qui suivent affichent les fichiers sourcés automatiquement par bash
et zsh qd on lance un shell interactif ou non, login ou non.
Chaque fichier existe en 2  versions: system-wide (dans `/etc`) et user-specific
(dans `~`).
Le shell source toujours les 2 en commançant par le system-wide.
Ex:

        /etc/bash.bashrc  →  ~/.bashrc

Après avoir sourcé ces fichiers, qd on se déconnecte de la session courante:

        bash source  ~/.bash_logout  et  /etc/bash.bash.logout
        zsh  source  ~/.zlogout      et  /etc/zlogout


    Bash:
    ┌───────────────────┬───────────────────────────────┐
    │                   │            login              │
    │                   ├──────────────────────┬────────┤
    │                   │          yes         │   no   │
    ├─────────────┬─────┼──────────────────────┼────────┤
    │ interactive │ yes │ bash_profile  bashrc │ bashrc │
    │             ├─────┼──────────────────────┼────────┤
    │             │ no  │ bash_profile         │   -    │
    └─────────────┴─────┴──────────────────────┴────────┘

                                     NOTE:

            Le comportement décrit dans ce tableau n'est pas celui par défaut.
            Je l'ai modifié pour le simplifier.
            Pour mieux comprendre lire les commentaires dans `~/.bash_profile`.


                                     NOTE:

            `bashrc` est toujours sourcé dans un shell interactif.
            `bash_profile` dans un login shell.


    Zsh:
    ┌───────────────────┬─────────────────────────────────────────────────┐
    │                   │                    login                        │
    │                   ├─────────────────────────────────┬───────────────┤
    │                   │ yes                             │ no            │
    ├─────────────┬─────┼─────────────────────────────────┼───────────────┤
    │ interactive │ yes │ zshenv  zprofile  zshrc  zlogin │ zshenv  zshrc │
    │             ├─────┼─────────────────────────────────┼───────────────┤
    │             │ no  │ zshenv  zprofile         zlogin │ zshenv        │
    └─────────────┴─────┴─────────────────────────────────┴───────────────┘

            `zshenv` est toujours sourcé.
            `zshrc` est toujours sourcé dans un shell interactif.
            `zprofile` et `zlogin` sont toujours sourcés dans un login shell.

            Les fichiers sont sourcés dans l'ordre, de gauche à droite.


                                     NOTE:

            Comme  `zshenv`  est toujours  sourcé,  pour  qu'un shell  zsh  non
            interactif se lance le plus vite  possible, il vaut mieux n'y mettre
            que le strict minimum.

            C'est-à-dire  uniquement  les  variables  d'environnement  dont  la
            présence est indispensable dans un shell non interactif.

            IOW, il n'y a aucune raison d'y mettre des variables d'environnement
            spécifiques à un shell interactif.

If the first character in the output of `echo $0` is a hyphen, then you're in an
interactive login shell, otherwise you're in an interactive non-login shell.
<https://unix.stackexchange.com/a/237672/289772>

## options

    ┌─────────────────────────────────────────────┬─────────────────┬───────────────────┬───────────────────┐
    │ action                                      │ bash set        │ bash shopt        │ zsh               │
    ├─────────────────────────────────────────────┼─────────────────┼───────────────────┼───────────────────┤
    │ lister les options actuellement activées    │ ∅               │ shopt -s          │ ∅                 │
    ├─────────────────────────────────────────────┼─────────────────┼───────────────────┼───────────────────┤
    │                                 désactivées │ ∅               │ shopt -u          │ ∅                 │
    ├─────────────────────────────────────────────┼─────────────────┼───────────────────┼───────────────────┤
    │ activer une option                          │ set -o <option> │ shopt -s <option> │ setopt   <option> │
    ├─────────────────────────────────────────────┼─────────────────┼───────────────────┼───────────────────┤
    │ désactiver une option                       │ set +o <option> │ shopt -u <option> │ unsetopt <option> │
    └─────────────────────────────────────────────┴─────────────────┴───────────────────┴───────────────────┘


                                     NOTE:

            Neither `shopt` nor `set [-|+]o` prints the readline variables.
            The latters are a different kind of options which are not specific to bash.


    [[ -o autocd ]] && ...
    if [[ $options[autocd] = on ]]; then ...

            Teste si l'option `autocd` est activée.


                                     NOTE:

            `options` est une array associative fournie par le module `zsh/parameter`.
            Ses clés sont les noms des options, et ses valeurs sont `on` ou `off`.

            `zsh/parameter` est chargé par défaut.

                    zmodload    |grep '/parameter'
                                                    ↳  zsh/parameter


    AUTO_LIST <D>
    AUTO_CD (-J)
    HUP <Z>

            Explication des marques `<D>` et  `<Z>`, ainsi que de l'option `-J`;
            dans zsh, par défaut:

                    - l'option `AUTO_LIST` est activée dans tous les modes
                      d'émulation:

                            zsh, ksh, sh, csh

                    - l'option `AUTO_CD` est désactivée dans tous les modes
                      d'émulation (car pas de marque), et peut être activée qd
                      on lance un shell via l'option `-J`, ou bien désactivée
                      via `+J`

                            zsh -J
                            zsh +J

                    - l'option `HUP` est activée uniquement en mode `zsh`


    KSH_OPTION_PRINT  ⇔  KSHOPTIONPRINT

            Dans zsh, on peut inclure des underscores dans les noms d'options où
            on veut, sans doute pour permettre de gagner en lisibilité.
            Leur forme normalisée:

                    - ne contient pas d'underscores  dans la sortie de `[un]setopt`

                    - contient des underscores       dans le manuel


    LOCAL_OPTIONS <K>

            Si cette  option est  activée, la  plupart des  options qui  ont été
            changées par une fonction sont restaurées au moment où elle finit.

            Si  elle est  désactivée,  elle seule  est restaurée  à  la fin  (+3
            autres).

            Pour se créer un environnement  local à une fonction, qui n'altèrera
            pas la session interactive, on peut aussi utiliser:

                             ┌ active `LOCAL_OPTIONS`
                             │
                    emulate -L  zsh
            OU
                    emulate -LR zsh

##
# Command-line
## command evaluation

FIXME: Toute cette section est à développer en partant du diagramme présent à la page 189 du pdf
(ou 165 du livre) “Classic Shell Scripting“.

Il faudra peut-être confronter le diagramme à `man zshexpn`.
L'ordre des opérations n'a pas l'air d'être le même entre bash et zsh.

   1. alias
   2. tilde expansion
   3. variable substitution
   4. command substitution
   5. arithmetic expression substitution
   6. word splitting
   7. wildcard expansion

D'après `man bash`, l'ordre des développements est:

   1. brace expansion
   2. tilde expansion
   3. parameter and variable expansion
   4. arithmetic expansion
   5. command substitution (done in a left-to-right fashion)
   6. word splitting
   7. pathname expansion

Il manque certaines étapes, comme ’parameter expansion’, ’quote removal’, ’brace expansion’

## constructions
### combinaison de commandes

'combinaison  de  commandes'  est   une  expression  fourre-tout  désignant  des
constructions  qui traitent  une  ou  plusieurs listes  /  expressions de  façon
diverses.

Grouper des commandes permet de:

   - s'assurer qu'elles sont exécutées dans le même environnement
   - appliquer une même redirection à chacune d'elles (pas besoin de se répéter)

#### Case

    case "${var}" in
      p1 | p2)         `p1` ou `p2` matche `var`
        instr1
        ;;
      p3)              `p3` matche `var`
        instr2
        ;;
      *)               autrement
        instr3
        ;;
    esac

    case "${var}" in
      p1 | p2)     instr1 ;;
      p3)          instr2 ;;
      *)           instr3 ;;
    esac

        Si le pattern ou l'instruction est trop long pour tenir sur une seule ligne, on utilisera
        plutôt la 1e forme; autrement la 2nde.


    case "$(ps $PPID)" in
      *"login"*)
      echo "you've just logged in a shell"
    esac

                Teste si le shell courant est un login shell.

                Au passage, on remarque que les métacaractères doivent se trouver à l'extérieur
                de la chaîne, autrement ils perdent leur sens spécial.
                On pourrait se passer de la chaîne:    *login*
                Elle n'est utile que pour s'assurer qu'aucun caractère dans une partie du pattern
                n'aura de sens spécial.


                                     NOTE:

                Que fait ce snippet ?
                `ps $PPID` est développé en 2 lignes (en-tête + infos).

                La ligne d'infos contient le nom de la commande ayant créé le processus parent.
                Si le shell est de type login, la commande devrait contenir le mot-clé `login`,
                pex `/bin/login`.

#### Expression arithmétique

    (( <EXPR> ))

        évalue <EXPR> en tant qu'expression arithmétique

    $((expression))

    i=$((i+1))                 incrémenter la variable i

    i=$(( 3 * ( 2 + 1 ) ))     affecter à i le résultat d'un calcul

#### Expression conditionnelle

    [[ <EXPR> ]]

        évalue <EXPR> en tant qu'expression conditionnelle

#### For

    for <NAME> in <WORDS> ; do <LIST> ; done        for <NAME> in <WORDS> ; do
                                                      <LIST>
                                                    done

        exécute <LIST> en donnant à la variable <NAME> une nouvelle valeur contenue dans <WORDS>
        à chaque itération de la boucle for

    for i in $(seq 1 5);do      boucle for qui echo l'incrément i variant de 1 à 5
        echo $i
    done

    for (( <EXPR1> ; <EXPR2> ; <EXPR3> )) ; do <LIST> ; done

        C-style for-loop (driven by arithmetic expressions)

#### Groupe

    (<LIST>)

        Exécute <LIST> comme un groupe de commandes dans un sous-shell.
        Changer une variable d'environnement dans ce sous-shell n'affecte pas le shell courant/parent.

        `()` est un opérateur. bash le reconnaît même si on ne met pas d'espace entre lui et <LIST>.


    (cd /etc; echo "$PWD")

        Affiche '/etc' mais le dossier courant reste `~`.


    var='hello'; bash -c 'echo $var'

        N'affiche rien.

        En effet,  echo est exécutée  dans un shell  enfant, et un  shell enfant n'hérite  pas de
        l'environnement du parent. Pour que le shell enfant sh voit $var, il faudrait l'exporter.


    var='hello'; (echo $var)

        Affiche 'hello'.

        En effet, echo est exécutée dans un sous-shell qui a hérité de l'environnement du parent.
        Un sous-shell est un shell enfant ayant hérité de l'environnement du parent.

        NOTE: on n'avait pas besoin des parenthèses pour que echo affiche 'hello'.
        Elles sont là uniquement pour montrer qu'un sous-shell hérite de l'environnement du parent,
        contrairement à un simple shell enfant.


    (export FOO=bar; echo $FOO)

        Affiche 'bar'.

        Cette instruction montre comment exécuter une commande dans un environnement custom:

                1.  L'affectation de  variable est  suivie d'un  ; Ça  implique qu'il  s'agit d'une
                instruction à part  entière qui modifie l'environnement du shell  dans lequel elle
                est exécutée. Et non simplement l'environnement de la commande qui suit.

                2. Les  parenthèses permettent  de confiner cette  modification dans  un sous-shell
                pour éviter de polluer le shell courant.

                3. La commande  export permet d'exporter la variable dans  un éventuel shell enfant
                (sh -c '...')

                                     NOTE:

        Une  affectation de  variable n'est  valable que  pour la  commande qui  suit. Pas  pour ses
        arguments, ni pour d'autres éventuelles commandes (après un pipe pex). Ainsi:

                FOO=bar  echo $FOO

        ... n'affichera pas 'bar' car seul l'environnement de echo est modifié, pas celui du shell.
        Or, c'est le shell qui développe `$FOO` avant d'en passer le résultat à `echo`.


    { <LIST>; }

        Exécute <LIST> comme un groupe de commandes dans le shell courant.

        { et } sont des mots réservés.  bash ne les reconnaît que si on met des espaces entre eux et <LIST>.
        La liste des mots réservés est:
                                        !      do     esac   in
                                        {      done   fi     then
                                        }      elif   for    until
                                        case   else   if     while


    ls | read a; echo "$a"

        N'affiche rien car la variable $a n'est pas définie.

        En effet, dans un pipeline, chaque commande est exécutée dans un sous-shell qui lui est propre.
        read est donc exécutée dans un sous-shell, tandis que echo est exécutée dans le shell courant.
        $a est donc définie dans le sous-shell de 'read' mais pas dans le shell courant.


    ls | { read a; echo "$a"; }

        Affiche le 1er item du dossier courant (contenu de la variable `$a`).

        Cette fois, les commandes `read` et `echo`  sont regroupées au sein d'une même combinaison
        de commandes, et donc exécutées dans le même sous-shell créé par le pipeline.

#### Select

    select <NAME> in <WORDS> ; do <LIST> ; done

        Provides simple menus ⇒ article

    echo -e "\nQue souhaitez-vous faire ?\n"

    select action in foo bar baz;do

        if [ $action = foo ];then
            cmd1 ; break
        elif [ $action = bar ];then
            cmd2 ; break
        elif [ $action = baz ];then
            cmd3 ; break
        fi

    done

#### Until

    until <LIST1> ; do <LIST2> ; done

        Execute <LIST2> until <LIST1> returns TRUE (exit status)

#### While

    while <LIST1> ; do <LIST2> ; done

        Execute <LIST2> while <LIST1> returns TRUE (exit status)

###
### commande simple

Une commande simple est:

   1. un ensemble d'affectations de variables
   2. un nom de commande
   3. des arguments
   4. un ensemble de redirections

Tous ces éléments sont optionnels. Le nom de commande est passé au shell en tant qu'argument 0.
Une commande simple a un code de sortie allant de 0 (ok) à 255 (diverses erreurs), auquel on peut
accéder depuis le shell via $?

Exemple de commande simple:

    $ LC_ALL=C ls $HOME >file

Avant d'exécuter une commande simple, bash effectue 3 opérations:

   1. field splitting
   2. développement
   3. évaluation

### fonction

 A shell function definition makes a compound command available via a new name. When the function runs, it has its own "private" set of positional parameters and I/O descriptors. It acts like a script-within-the-script. Simply stated: You've created a new command.

The definition is easy (one of many possibilities):

<NAME> () <COMPOUND_COMMAND> <REDIRECTIONS>

which is usually used with the {...; } compound command, and thus looks like:

print_help() { echo "Sorry, no help available"; }

As above, a function definition can have any compound command as a body. Structures like

countme() for ((x=1;x<=9;x++)); do echo $x; done

are unusual, but perfectly valid, since the for loop construct is a compound command!

If redirection is specified, the redirection is not performed when the function is defined. It is performed when the function runs:

 # this will NOT perform the redirection (at definition time)
f() { echo ok ; } > file

 # NOW the redirection will be performed (during EXECUTION of the function)
f

Bash allows three equivalent forms of the function definition:

NAME ()          <COMPOUND_COMMAND> <REDIRECTIONS>
function NAME () <COMPOUND_COMMAND> <REDIRECTIONS>
function NAME    <COMPOUND_COMMAND> <REDIRECTIONS>

The space between NAME and () is optional, usually you see it without the space.

I suggest using the first form. It's specified in POSIX and all Bourne-like shells seem to support it.

Note: Before version 2.05-alpha1, Bash only recognized the definition using curly braces (name() { ... }), other shells allow the definition using any command (not just the compound command set).

To execute a function like a regular shell script you put it together like this:

 #!/bin/bash
 # Add shebang

mycmd()
{
  # this $1 belongs to the function!
  find / -iname "$1"
}

 # this $1 belongs the script itself!
mycmd "$1" # Execute command immediately after defining function

exit 0

Just informational(1):

Internally, for forking, Bash stores function definitions in environment variables. Variables with the content "() ...".

Something similar to the following works without "officially" declaring a function:

$ export testfn="() { echo test; }"
$ bash -c testfn
test
$

Just informational(2):

It is possible to create function names containing slashes:

/bin/ls() {
  echo LS FAKE
}

The elements of this name aren't subject to a path search.

Weird function names should not be used. Quote from the maintainer:

    It was a mistake to allow such characters in function names (`unset' doesn't work to unset them without forcing -f, for instance). We're stuck with them for backwards compatibility, but I don't have to encourage their use.

Définition d'une fonction foo ; elle utilise une variable locale bar (portée limitée à la fonction).
    foo(){

        local bar=$(expr)
        echo $bar

    }

Appel de la fonction foo.
    foo

Appel de la fonction foo à qui on passe en argument la variable bar.
    foo $bar

Sortir de la fonction avec un code de sortie 0.
    return 0
Le code de sortie peut être analysé hors de la fonction via $?

Création d'une fonction dont le nom est déjà utilisé par une fonction préexistante.
On parle de wrapper. On utilise pour ce faire l'instruction command.
Exemple avec ls :

    ls () {
    command ls -lh
    }

### liste

Une liste est une séquence d'une ou plusieurs commandes simples / pipelines séparés par un opérateur:

        ; <NL> && || &

Une liste peut servir à construire une combinaison de commandes, une fonction, voire un script entier.

    PL1 <NL> PL2    PL1 ; PL2

        Exécute PL2 après que PL1 ait été exécuté, peu importe le code de sortie de ce dernier.


    PL1 && PL2

        Exécute PL2 après que PL1 ait été exécuté et uniquement si son code de sortie est nul (TRUE).


    PL1 || PL2

        Exécute PL2 après que PL1 ait été exécuté et uniquement si son code de sortie est non-nul (FALSE).


    PL1 & PL2

        Exécute PL2 dès que PL1 a été lancé.

        PL1 est exécuté en tâche de fond / de façon asynchrone (il devient un job)
        asynchrone car le début de PL2 n'est pas synchronisé sur la fin de PL1.

        Ex: sleep 5 &

### pipeline

Un pipeline est une séquence d'une  ou plusieurs commandes simples, séparées par
des pipes qui relient leur entrée et sortie.
La dernière commande du pipeline définit le code de sortie.


    set -o pipefail    set +o pipefail

        (dés)active pipefail (off par défaut)

        - = active, + = désactive

        Qd pipefail est activée,  le code de sortie d'un pipeline n'est plus  celui de la dernière
        commande mais de la dernière ayant échoué. Ou 0 si aucune n'a échoué.


    shopt -s lastpipe    shopt -u lastpipe

        (dés)active l'option lastpipe (off par défaut)
        Mnémotechnique: -s = set
                        -u = unset

        Qd lastpipe est activée, la dernière commande d'un pipeline est exécutée dans le shell courant et non dans un sous-shell (à condition que l'option monitor mode soit désactivée:    set +m).
        Qd l'option monitor mode est activée, un job qui se termine affiche une brève description ds le terminal.

        NOTE: quelle différence entre set et shopt?
        Les 2 commandes gèrent des options différentes:
                                                        shopt = les options spécifiques à bash
                                                        set   = les options héritées d'autres shell (ksh surtout)


    if ! grep '^root:' /etc/passwd; then
      echo "L'utilisateur root n'a pas été défini."
    fi

        Cette commande illustre que le code de sortie d'un pipeline peut être inversé en le préfixant d'un !.
        Le shell n'exécute le code à l'intérieur de la structure if qu'à condition que le code de sortie
        soit nul. 0 = TRUE, 1..255 = FALSE


    echo ${PIPESTATUS[@]}

        affiche le code de sortie de chaque commande au sein du dernier pipeline exécuté en avant-plan


    time ls /etc | wc -l

        affiche le temps d'exécution du pipeline 'ls /etc | wc -l'
        time est une commande dont la portée est le pipeline qui la suit.


La syntaxe générale d'un pipeline est donc:

    [time] [!] cmd1 [| cmd2 | ...]

##
##
# Todo
## How to determine where an environment variable come from?

<https://unix.stackexchange.com/a/154971/275162>


>     You'll also see people  exporting things, such as term, in  .bashrc or .zshrc or
>     similar - that will break things in the long run.
>     Exports solely  belong in the  login shell init  file, such as  .bash_profile or
>     .zprofile and even then you don't export some things like term.

<https://github.com/tmux/tmux/issues/353#issuecomment-203038518>

Should we move all our exports out of `~/.bashrc`, `~/.zshrc` and `~/.shrc`?

When the author  of the comment say  “that will break things”, I  think he means
that  sometimes  you  will  start  a  login  shell  which  doesn't  source  your
`~/.bashrc` or `~/.zshrc` ...

---

Study an document `expand(1)` and `unexpand(1)`.

---

    $ touch a b é à ; echo [a-z] ; echo [[:lower:]]

Le 1er `echo` affiche seulement `a` et `b`.
Le 2e `echo` affiche `a`, `b`, `é` et `à`.

            Illustre  que  la  classe   de  caractères  `[[:lower:]]`  est  plus
            puissante  que  la  rangée  `[a-z]`,   car  elle  peut  matcher  des
            caractères accentués.
            Idem pour `[[:upper:]]`

            De plus, il paraît que le  développement d'une rangée en ensemble de
            caractères est déterminé par la valeur de `LC_COLLATE`:

                    https://unix.stackexchange.com/a/227077/232487

            Ce lien explique que certaines locales rangent les caractères minuscules et majuscules,
            de la façon suivante:

                    aAbBcC ... xXyYzZ

            Avec une telle locale, `[a-z]` matche n'importe quel caractère minuscule/majuscule sauf `Z`.
            Et `[A-Z]` matche n'importe quel caractère minuscule/majuscule sauf `A`.
            Toutefois, je n'ai pas réussi à reproduire ce phénomène ...

            Tandis que la locale `C` les range comme ceci:

                    ABC ... XYZabc ... xyz

            Si c'est vrai, ça donne une raison de plus pour utiliser `[[:lower:]]` et `[[:upper:]]`,
            car ces classes ne sont pas influencées par `LC_COLLATE`.
            Ou bien utiliser la locale C, dont le comportement ne produit pas de résultat inattendu:

                    export LC_COLLATE=C


    man zshcompsys:

            The  function   bashcompinit  provides  compatibility   with  bash's
            programmable completion system.
            When run  it will define  the functions, compgen and  complete which
            correspond to the bash builtins with the same names.
            It  will  then be  possible  to  use completion  specifications  and
            functions written for bash.


    hash -d down=~/Downloads

            Permet de donner un nom au dossier de dl, et de s'y rendre via `cd ~down`.

            À développer en lisant `man zshparam` section `Static named directories`,
            et `man zshbuiltins`.


    cd /usr/local/bin
    cd local share    ⇔    cd /usr/local/share

            zsh: Utile qd on  a tapé un long chemin, et  qu'on s'est trompé dans
            l'un des ses composants.
            Plus généralement, `cd  foo bar` remplace la 1e  occurrence de `foo`
            par `bar` dans le chemin du dossier courant.


                                     FIXME:

            Uniquement la 1e occurrence, pas les suivantes.

            Il  faudrait se  créer une  fonction custom  qui tente  de remplacer
            toutes les occurrences.
            Attention, pour qu'elle  soit fidèle au `cd`  d'origine, il faudrait
            aussi qu'elle utilise, si besoin, l'option `CDPATH`:

                    % cd /tmp
                    % Downloads
                    % pwd
                    ~/Downloads/~


    print -l $path

            Affiche chaque valeur au sein de `$PATH` sur une seule ligne.


    echo *(.)   Tab
    echo *(/)   Tab
    echo *(@)   Tab

            Développe le glob qualifier en tous les:

                    - fichiers
                    - dossiers
                    - liens symboliques

            ... du dossier courant.

            FIXME: à développer en lisant `man zshexpn`, section `FILENAME GENERATION`.


    echo   *(   Tab
    print  ${(  Tab
    print  ${   Tab

                    possible glob qualifiers
                    completion candidates for parameter flags
                    complete any currently set variable in the current env


    vared path

            zsh: Édite une variable d'environnement (ici $PATH) en utilisant les
            raccourcis readline.


                                     NOTE:

            Si  on écrit  la variable  d'environnement en  minuscule, et  que la
            variable contient  plusieurs valeurs  séparées par des  `:`, `vared`
            remplace  temporairement les  `:`  par des  espaces  pour gagner  en
            lisibilité.



Se faire  une fonction `go`  qui exécute une  action par défaut  avec différents
type d'arguments.
http://blog.patshead.com/2011/05/my-take-on-the-go-command.html  (vim   avec  un
fichier, cd avec un dossier, xdg-open, fasd, etc)

Inspiration:

        go() {
        if [ -f "$1" ]; then
            if [ -n "`file $1 | grep '\(text\|empty\|no magic\)'`" ]; then
            if [ -w "$1" ]; then
                $EDITOR "$1"
            else
                sudo $EDITOR "$1"
                #$EDITOR /sudo::"$1" # For emacsclient+tramp
            fi
            else
            if [ -e "`which xdg-open`" ]; then
                if [ -n "$DISPLAY" ]; then
                xdg-open "$1" > /dev/null
                else
                echo "DISPLAY not set:  xdg-open requires X11"
                fi
            else
                echo "xdg-open not found:  unable to open '$1'"
            fi
            fi
        elif [ -d "$1" ]; then
            cd "$1"
        elif [ "" = "$1" ]; then
            cd
        elif [ -n "`declare -f | grep '^j ()'`" ]; then
            j "$1"
        else
            echo "Ran out of things to do with '$1'"
        fi
        }

        alias g=go

## Review `~/.inputrc`, and find zsh equivalent to all readline key bindings defined there.

Also, review their lhs so that they're as consistent as possible across bash and zsh.

## To read

- <http://redsymbol.net/articles/unofficial-bash-strict-mode/>
- <https://github.com/alebcay/awesome-shell>
- <https://github.com/unixorn/awesome-zsh-plugins>
- <http://zsh.sourceforge.net/FAQ/>
- <http://zsh.sourceforge.net/Guide/zshguide.html>
- <https://www.commandlinefu.com/commands/browse/sort-by-votes>
- <http://www.shellscript.sh/>
- <http://mywiki.wooledge.org/BashPitfalls>
- <http://mywiki.wooledge.org/BashFAQ>
- <http://stackoverflow.com/a/10834267 (script inplace)>
- <http://wiki.bash-hackers.org/scripting/obsolete (diverses syntaxes obsolètes)>
- <https://google.github.io/styleguide/shell.xml>
- <https://wiki.bash-hackers.org/scripting/style>
- <https://grml.org/zsh/>
- <https://grml.org/zsh/zsh-lovers.pdf>

         cd /tmp ; wget -O .zshrc http://git.grml.org/f/grml-etc-core/etc/zsh/zshrc

- <http://www.bash2zsh.com/>
- <http://www.bash2zsh.com/zsh_refcard/refcard.pdf>
- <https://www-s.acm.illinois.edu/workshops/zsh/toc.html>
- <https://blog.engineyard.com/2014/bats-test-command-line-tools>
- <https://github.com/sstephenson/bats>
- <https://fr.wikipedia.org/wiki/Test_unitaire>
- <https://fr.wikipedia.org/wiki/Test_driven_development>
- <http://www.talisman.org/~erlkonig/documents/commandname-extensions-considered-harmful/>

##
# Reference

[1]: https://mywiki.wooledge.org/BashFAQ/048
