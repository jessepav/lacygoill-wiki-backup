
To test the current value of a replacement variable such as `#{pane_tty}`, run:

    # shell command
    tmux -S /tmp/tmux-1000/default display -p #{pane_tty}

    # tmux command
    :display -p #{pane_tty}

    # Vim command
    :echo system('tmux -S /tmp/tmux-1000/default display -p "#{pane_tty}"')

---

        http://man.openbsd.org/OpenBSD-current/man1/tmux.1

        https://github.com/tmux/tmux/wiki/FAQ

        https://devel.tech/tips/n/tMuXz2lj/the-power-of-tmux-hooks/

        https://github.com/tmux-plugins/tmux-sensible

        https://github.com/tmux-plugins/tmux-pain-control

        # extended underline style
        https://github.com/tmux/tmux/commit/bc0e527f32642cc9eb2354d1bdc033ab6beca33b

        # Support for windows larger than visible on the attached client.
        https://github.com/tmux/tmux/commit/646995384d695eed9de1b2363fd2b315ca01785e

---

Document this:

        $ tmux pipe-pane -t study:2.1 -I "echo 'ls'"

This command  executes `$  ls` in  the first pane  of the  second window  of the
`study` session.
The syntax is the following:

        $ tmux pipe-pane -t {session}:{window}.{pane} -I "shell cmd"

The output of  the shell command is  written on the standard input  of the shell
running in the targeted pane.

It could be useful for our re-implementation of `vim-tbone`.

---

Issue:

Sometimes, in  the first pane  of some windows, when  I press `n`,  tmux expands
this key into a keysequence such as:

        n16j16k1l 41lh
        M-SPC SPC
        :

`n16j16k1l 41lh`  is literally inserted  on the shell command-line,  after that,
I'm  not sure  but I  think  tmux types  `M-SPC SPC  :`,  because we  end up  in
copy-mode and the prompt  “(goto line)” which you enter when  you press `:` from
copy-mode.

For the moment, the  only solution which I know is to kill  and restart the tmux
server.

# Theory

Several tmux clients can be attached to the same session.
The tmux server is automatically stopped when all sessions are killed.



When you want to attach a tmux client  to a tmux server, you don't start it from
the local  machine. The server  AND the  client are always  running on  the same
machine. The procedure consists in 2 steps:

    1. log in to the remote (for example via ssh)
    2. start a tmux client to attach it to a running tmux server



When you start tmux on the remote for the first time, 2 processes are created.
First, one for the client:

    login/urxvt───zsh───tmux: client
                  │
                  └ our initial shell, provided by:

                        - the `login` process in console
                        - a terminal emulator in X

… then another for the server:

    tmux: server───zsh

Both (chain of) processes are started by:

    - the init process in console:

            systemd

    - the display manager in X:

            systemd───lightdm───lightdm───upstart

You can check this with the following commands:

    pstree -ps $(pidof tmux|cut -d' ' -f1)
    pstree -ps $(pidof tmux|cut -d' ' -f2)

Note that the  server is started after  the first client, so its  pid is bigger,
which may seem counter-intuitive.
Also, the relationship between the 2 processes is NOT parent-child.
It's client-server.
IOW, they are 2 independent processes. You won't find both of them listed in the
output of the same `pstree` command.
They communicate via a socket, which  by default is called `default`. The latter
is created in the directory `tmux-{UID}` inside:

    - $TMUX_TMPDIR if the latter set
    - /tmp otherwise



Any shell created with a tmux client is a child of the tmux server:

    tmux: server─┬─zsh───vim
                 ├─zsh───pstree
                 └─zsh───cmus

This fact, combined  with the fact that  the tmux client is  a different process
with no parent-child relationship, means  that you're manipulating a shell which
is NOT the child of your current terminal.

This is very unusual: usually the program you're interacting with, is a child of
the terminal (direct or indirect).
Not  here, because  the tmux  client makes  you interact  with the  child of  an
entirely different process: the tmux server.

The  communications between the first  shell opened by the  terminal (before
executing tmux), the tmux client, and the tmux server are all [transparent]($MY_WIKI/graph/tmux/transparent.pdf):
everything in red in the diagram is not visible.

# Installation

    https://tmux.github.io/
    https://github.com/tmux/tmux/releases/

            Url où dl la dernière release stable de Tmux.
            Utile pour voir quelle est le n° de version de la dernière release.


    git clone https://github.com/tmux/tmux
    cd tmux
    git checkout <last release nr>

            Cloner le repo du projet, et se rendre sur la branche de la dernière release.


    api libevent-dev libncurses5-dev

            Dépendances nécessaires à la compilation.


    tar xvzf tmux-X.Y.tar.gz && cd tmux-X.Y
    ./configure
    make
    sudo checkinstall

            Décompresse l'archive contenant le code source.
            Compile.
            Installe.


    sudo dpkg -r tmux

            Supprime le paquet tmux.
            Le nom du paquet n'est pas forcément `tmux`. Ça dépend de comment on l'a nommé au cours
            de l'installation via `checkinstall`.

# Démarrage

Voici qques argument qu'on peut passer à Tmux au démarrage.


    tmux command

            Spécifie à Tmux quelle commande exécuter.
            Si aucune commande n'est donnée, Tmux exécute `new-session`.

            Si `command` accepte des flags en argument, on peut les lui passer ici aussi.


    -C
    -CC

            Flag activant le mode contrôle.
            Idem mais sans qu'aucun message ne soit affiché (echo est désactivé).

            En mode contrôle, on interagit avec Tmux via une interface textuelle.
            Elle peut être utilisée par une application pour communiquer avec Tmux via un protocole
            basé simplement sur du texte.
            Quelle genre d'application?
            Émulateur de terminal (aucun sous Linux actuellement), script (tmuxinator, tmuxp) …

            Le client envoit des commandes Tmux ou des séquences de commandes terminées par des
            newlines écrites sur son entrée standard.
            Chaque commande écrit un bloc de sortie sur sa sortie standard.
            Un bloc de sortie commence par `%begin` et se termine par un `%end` ou `%error`.
            Il ressemble à ça:

                    %begin {epoch time} {command number}
                    tmux command output
                    %end   {epoch time} {command number}

            Si la commande Tmux contient une erreur de syntaxe, le bloc de sortie ne se termine pas
            par `%end` mais par `%error`.
            Quel exemple de commande Tmux peut-on utiliser pour tester le mode contrôle?

                    ls

            Tmux peut également  nous écrire des notifications,  qui sont tjrs
            en-dehors d'un bloc de sortie.

                    - %exit [reason]

                            Le client Tmux doit s'arrêter, peut-être car une erreur est survenue ou
                            car il n'est attaché à aucune session.

                    - %output 42 value

                            Un pane vient de produire une sortie.
                            Au sein de cette dernière, les caractères non imprimables sont échappés
                            et codés sous forme octale:    \xxx

                    - %session-changed 42 foobar

                            Le client vient d'être attaché à la session d'identifiant 42 qui se nomme foobar.

                    - %session-renamed foobar

                            La session courante vient d'être nommée `foobar`.

                    - %sessions-changed

                            Une session a été créée ou détruite.

                    - %unlinked-window-add 42

                            La fenêtre dont l'identifiant est 42 vient d'être créée, mais n'est pas
                            liée à la session courante.

                    - %window-add 42

                            La fenêtre dont l'identifiant est 42 vient d'être liée à la session courante.

                    - %window-close 42

                            La fenêtre dont l'identifiant est 42 vient d'être fermée.

                    - %window-renamed 42 foobar

                            La fenêtre dont l'identifiant est 42 vient d'être renommée `foobar`.


    -c shell-command

            Exécute `shell-command` en utilisant le shell par défaut.

            Ce dernier est défini par l'option `default-shell`.
            Par défaut, elle est vide, et tmux prend donc à la place `$SHELL`.
            `-c shell-command` est utile pour rendre Tmux compatible avec le shell `sh` qd Tmux
            est utilisé comme un login shell.


    -f file

            Spécifie un chemin de fichier de configuration alternatif.


              ┌ don't attach to a running Vim server,
              │ start a new one, identified by the socket name `test`
              │ inside the directory /tmp/tmux-{$UID}
              │
              │           ┌ don't use any config file
         ┌────┤ ┌─────────┤
    tmux -Ltest -f/dev/null

            Useful to debug tmux.
            Start without any config, and without being interfered by a running server.

            `-L` specifies an arbitrary socket name.
            If a server is already running, this allows to run a 2nd one simultaneously.
            Indeed,  a  server  is  identified  by  the  socket  with  which  it
            communicates with its clients.

            By default, if a tmux server  is already running, the `tmux` command
            would simply create a new session managed by the existing server.


    -S socket-path

            Spécifie un chemin alternatif vers le socket du serveur.

            Si  `-S`  est  utilisé,  le dossier  par  défaut  (`$TMUX_TMPDIR`,
            `/tmp`) ainsi que l'argument `-L` sont ignorés.


    -v

            Ask for a verbose logging.
            Can be repeated twice to increase the level of verbosity.

            2/3 log files  are created inside the working directory  (the one from
            which we started tmux). One for the client, the other(s) for the server.

            Their names follow the scheme:

                    - tmux-client-{PID_c}.log
                    - tmux-server-{PID_s}.log
                    - tmux-out-{PID_s}.log (only with `-vv`)

            Where `{PID_c}` and `{PID_s}` are the process ID of the client/server.

            `tmux-server-{PID}.log` is useful to follow how the tmux config file
            has been sourced.

            `tmux-out-{PID}.log` is useful to see the raw sequences sent by tmux
            to the terminal.


            ┌ SIGUSR2
            │
            │   ┌ hint: in the output of `ps -efH|grep tmux`, it's the biggest pid;
            │   │       yes the server seems to be started AFTER the first client …
            │   │
    $ kill -12 {tmux server pid}

            Toggle the  logging of  the activity. However,  when you  enable the
            logging, it seems to only create the `tmux-server-{PID}.log` file.

            Warning:
            The log files  becomes really big, really fast. Enable logging  only for a short
            period of time to debug sth.


    -V

            Affiche la version du pgm Tmux.

# Links

    https://www.reddit.com/r/tmux/comments/5cm2ca/post_you_favourite_tmux_tricks_here/


    https://raw.githubusercontent.com/tmux/tmux/master/CHANGES

            Changelog


    http://tmuxp.readthedocs.io/en/latest/about.html

            tmuxp helps you manage tmux workspaces.

            tmux users can reload common workspaces from YAML, JSON and dict configurations like
            tmuxinator and teamocil.

# Plugins
## Installation / Suppression

    set-option -g @plugin 'author/plugin'
    pfx I
    pfx U

            Procédure d'installation et de mise à jour d'un plugin Tmux hébergé sur github.

            Les raccourcis `pfx I` et `pfx U` permettent resp. d'installer et de mettre à jour les plugins.
            Ils sont associés à des scripts shells fournis par TPM (Tmux Plugin Manager):

                    bind-key  -T prefix    I  run-shell ~/.tmux/plugins/tpm/bindings/install_plugins
                    bind-key  -T prefix    U  run-shell ~/.tmux/plugins/tpm/bindings/update_plugins


    pfx M-u

            Raccourci permettant de supprimer un plugin géré par TPM.
            Toutefois, au préalable, il faut supprimer la ligne du plugin dans `~/.tmux.conf`.
            Le raccourci est associé à un script shell fourni par TPM:

                    bind-key  -T prefix  M-u  run-shell ~/.tmux/plugins/tpm/bindings/clean_plugins

## Futur
### fingers

        copy pasting in terminal with vimium/vimperator like hints.

        https://github.com/morantron/tmux-fingers

### heytmux

        Tmux scripting made easy

        Heytmux can read STDIN, so:

                cat workspace.yml | heytmux

        … is also valid. It may seem pointless, but it allows you to do:

                :w !heytmux

        … with a visual selection in Vim.

        I primarily  use Heytmux  to write Markdown  documents with  fenced code
        blocks of YAML snippets that I can easily select and run with Heytmux in
        my editor.

        https://github.com/junegunn/heytmux

### highlight

        Plugin that highlights when you press tmux prefix key

        https://github.com/tmux-plugins/tmux-prefix-highlight

# Utilitaires
## Reptyr

reptyr est un pgm permettant d'attacher à une session tmux, un processus lancé
depuis un shell hors de la session.

    sudo aptitude install reptyr

            installation

    reptyr 42

            Attacher le processus de pid 42 à la session courante.

            Au cas où le message d'erreur suivant apparaît :

                    Unable to attach to pid xxxx: Operation not permitted
                    The kernel denied permission while attaching. If your uid matches
                    the target's, check the value of /proc/sys/kernel/yama/ptrace_scope.
                    For more information, see /etc/sysctl.d/10-ptrace.conf

            Faire  passer le  paramètre  `kernel.yama.ptrace_scope`  à 0  dans
            `/etc/sysctl.d/10-ptrace.conf`  puis recharger  la config'  du noyau
            via :

                    sysctl -p /etc/sysctl.d/10-ptrace.conf
                           │
                           └ load in sysctl settings from the file specified

            … ou peut-être:

                    service procps start

            Cette dernière commande est donnée dans `/etc/sysctl.d/README`.

# Configuration
## Fichier

Par défaut, tmux charge `/etc/tmux.conf` (s'il existe) puis `~/.tmux.conf`.

Un fichier de configuration tmux n'est rien d'autre qu'une séquence de commandes tmux, qui sont
exécutées la 1e fois que le serveur est lancé.

La commande `source-file` peut être utilisée pour charger un fichier plus tard.

## Commandes de configuration

On peut configurer l'apparence et le comportement de tmux via 3 catégories d'options:

            - serveur
            - fenêtre
            - session


Chaque option fenêtre ou session existe en 2 versions, locale ou globale.
La version locale s'applique uniquement à la fenêtre / session courante.
La globale à toutes les fenêtres / sessions.

En cas de conflit, la locale a la priorité sur la globale.

Si la locale n'est pas configurée explicitement, elle est héritée de la globale.


En plus des options par défaut, un utilisateur peut créer ses propres options dans n'importe quelle
catégories d'options. Pour ce faire, il doit préfixer leur nom avec ’@’.
Une option utilisateur accepte comme valeur une chaîne arbitraire.


La valeur d'une option peut être un nombre, une chaîne ou un flag.
Un flag peut être on, off ou omis. Dans une affectation, si un flag est omis, l'option est toggle.


    Affiche les options :

        ┌──────────────────┬─────────────────────┐
        │ show-options -s  │ serveur             │
        ├──────────────────┼─────────────────────┤
        │ show-options     │ session et locales  │
        ├──────────────────┼─────────────────────┤
        │ show-options -g  │ session et globales │
        ├──────────────────┼─────────────────────┤
        │ show-options -w  │ fenêtre et locales  │
        ├──────────────────┼─────────────────────┤
        │ show-options -gw │ fenêtre et globales │
        └──────────────────┴─────────────────────┘

            `show` est un alias de `show-options`.

            À la place de `show-options -w`, on peut aussi utiliser:

                    - showw
                    - show -w
                    - show-window-options


    Donne la valeur `val` à l'option `opt`, cette dernière étant une option:

        ┌─────────────────────────┬────────────────────┐
        │ set-option -s   opt val │ serveur            │
        ├─────────────────────────┼────────────────────┤
        │ set-option      opt val │ session et locale  │
        ├─────────────────────────┼────────────────────┤
        │ set-option -g   opt val │ session et globale │
        ├─────────────────────────┼────────────────────┤
        │ set-option -w   opt val │ fenêtre et locale  │
        ├─────────────────────────┼────────────────────┤
        │ set-option -gw  opt val │ fenêtre et globale │
        └─────────────────────────┴────────────────────┘

            `set` est un alias de `set-option`.

            À la place de `set-option -w`, on peut aussi utiliser:

                    - setw
                    - set -w
                    - set-window-option


    show-options -gv opt

            Affiche la valeur globale de l'option session `opt` sans afficher son nom (flag `-v`).

            Montre qu'on peut limiter la sortie de `show-options` de 2 façons:

                    - flag `-v`      supprime les noms des options
                    - argument `opt` supprime toutes les options différentes de `opt`


    set-option -g  status-left 'foo'
    set-option -ag status-left 'bar'

            Configure l'option session `status-left` en lui donnant la valeur `foo`.
            Puis, lui ajoute (append) la valeur `bar`.
            La valeur finale est donc `foobar`.

            Le flag `-a` permet d'ajouter (append) une chaîne/un style à une option.


    set-option -g  status-style 'bg=red'
    set-option -ag status-style 'fg=blue'

            Configure l'option session `status-style` en lui donnant la valeur `'bg=red'`.
            `'bg=red'` est un style.
            Puis, lui ajoute le 2e style `'fg=blue'`.

            Le résultat est un avant-plan bleu et un arrière-plan rouge.
            Sans le flag `-a`, le résultat serait un avant-plan bleu et un arrière-plan NOIR (valeur par défaut).


Les commandes `set-option`, `show-options`, `set-window-option` et `show-window-options` acceptent
également les arguments suivants:

            ┌───────────────┬─────────────────────────────────────────────────────┐
            │ -o            │ ne configure pas l'option si elle a déjà une valeur │
            ├───────────────┼─────────────────────────────────────────────────────┤
            │ -q            │ supprime un éventuel message d'erreur               │
            │               │ (option inconnue ou ambigüe)                        │
            ├───────────────┼─────────────────────────────────────────────────────┤
            │ -u            │ supprime la valeur locale d'une option,             │
            │               │ de sorte qu'elle hérite de la globale               │
            ├───────────────┼─────────────────────────────────────────────────────┤
            │ -gu           │ supprime la valeur globale d'une option,            │
            │               │ de sorte qu'elle récupère sa valeur par défaut      │
            ├───────────────┼─────────────────────────────────────────────────────┤
            │ -t my_window  │ configure ou affiche une option d'une fenêtre       │
            │ -t my_session │ ou session arbitraire                               │
            └───────────────┴─────────────────────────────────────────────────────┘

## Options serveur

    buffer-limit 10

            Configure le nb maximum de buffers mémorisés par tmux.

            Les buffers tmux sont mémorisés sous forme de stack.
            Une fois le nb max de buffers atteint, la prochaine fois qu'on copie du texte,
            le dernier buffer de la pile est supprimé pour faire de la place.


    default-terminal screen

            Configure screen comme étant le terminal par défaut pour les nouvelles fenêtres créées.

            Pour que tmux fonctionne correctement, il faut que la valeur soit `screen`, `tmux` ou
            une forme dérivée de ces dernières.

            Il est probable que la valeur par défaut de cette option soit dérivée de `$TERM`.


    escape-time 0

            Configure le temps en millisecondes pendant lequel tmux attend, après avoir reçu un
            caractère escape, pour déterminer s'il fait partie d'une touche fonction (pex F1) ou
            d'une séquence de touches tapées par l'utilisateur.

            Par défaut `escape-time` vaut 500ms.

            Qd cette valeur est >0 on peut expérimenter du lag dans Vim chaque fois qu'on tape
            Escape. En effet, tmux "retient" escape, le temps défini par l'option, avant de l'envoyer
            à Vim.


    exit-unattached [on | off]

            Si l'option est activée, le serveur s'arrête dès qu'il n'y a plus aucun client attaché.


    focus-events [on | off]

            Si l'option est activée, et que le terminal supporte les évènements focus, tmux demande
            à ce dernier de les lui envoyer pour les passer aux applications qui tournent à l'intérieur.

            Après avoir changé cette option, pour qu'elle prenne effet dans un client, il faut
            détacher et réattacher ce dernier.


    history-file path/to/file

            Si la valeur n'est pas vide, l'historique des commandes tmux exécutées sera écrit
            dans le fichier `path/to/file` qd le serveur s'arrêtera, et chargé qd il démarrera.


    message-limit 50

            Configure le nombre de messages d'informations mémorisés dans le log de messagerie
            de chaque client.

            Valeur par défaut:    100

## Options fenêtres

    allow-rename [on | off]

            Autorise les programmes à renommer la fenêtre en utilisant une séquence d'échappement
            (\ek...\e\\).

            Activée par défaut.


    automatic-rename [on | off]

            Qd cette option est activée, tmux renomme automatiquement une fenêtre en utilisant
            le format spécifié dans l'option `automatic-rename-format`.

            L'option est ignorée lorsqu'on utilise la commande `new-window`, `new-session` ou
            `rename-window`, et qu'on spécifie un nom de fenêtre.


    automatic-rename-format my_format

            Le format de nom à utiliser, si l'option `automatic-rename` est activée, et que tmux doit
            renommer une fenêtre.


    clock-mode-colour green

            Configure la couleur de l'horloge (pfx t) comme étant verte.


    clock-mode-style [12 | 24]

            Configure le format de l'horloge comme étant 12h ou 24h.


    force-height 12
    force-width 34

            Empêche tmux de redimensionner une fenêtre en utilisant:

                    - une hauteur supérieure à 12
                    - une largeur "            34

            Par défaut, ces options ont des valeurs nulles, ce qui signifie que tmux ne connaît
            aucune limite qd il doit redimensionner une fenêtre.

            Attention, ne s'applique pas aux panes à l'intérieur d'une fenêtre, mais bien à la fenêtre
            elle-même.

            Qd on change une de ces valeurs, l'effet est immédiat, la fenêtre est redimensionnée.
            Mais pas le terminal qui l'affiche.
            Qu'affiche le terminal dans la partie désormais vacante? Des points.


    main-pane-height 12
    main-pane-width 34

            Configure la hauteur/largeur du pane principal (en haut/à gauche), qd tmux organise les
            panes de la fenêtre avec le layout `main-horizontal` / `main-vertical`.

            Pour rappel, tmux dispose de plusieurs layouts prédéfinis, qu'on peut:

                    - sélectionner via la commande `select-layout`
                    - alterner via `next-layout` (associée à `pfx + Escape`; custom)

            Dans les layouts `main-horizontal` et `main-vertical`, la 1e fenêtre est la principale
            et occupe:

                    - toute la largeur de l'écran en haut
                    - toute la hauteur de l'écran à gauche


    mode-keys [vi | emacs]

            Type de raccourcis à utiliser en mode copie.
            La valeur par défaut est ’emacs’ à moins que `$VISUAL` ou `$EDITOR` ne contienne ’vi’.


    mode-style my_style

            Configure l'apparence de l'indicateur tmux affichant le nb de lignes présentes
            dans le scrollback buffer qd on passe en mode copie.


    monitor-activity [on | off]

            Surveille l'activité dans la fenêtre.
            Une fenêtre surveillée, et qui connaît une certaine activité, voit la couleur de son nom
            et celle de son fond inversées.


    monitor-silence 42

            Dès que la fenêtre est inactive pendant plus de 42 secondes, tmux met en surbrillance
            le nom de la fenêtre dans la status line.

            Par défaut, cette option vaut 0, ce qui signifie que l'inactivité de la fenêtre n'est
            pas surveillée.


    other-pane-height 12
    other-pane-width  34

            Qd on utilise le layout `main-horizontal`, configure 42 comme étant la hauteur des autres
            panes (!= principal).

            Si `main-pane-height` et `other-pane-height` sont tous deux configurés, et que leur somme
            est inférieure à la hauteur de l'écran, la hauteur du pane principal augmentera pour compenser.
            En revanche, si la somme est supérieure, c'est la hauteur des autres panes qui sera réduite.

            Par défaut cette option vaut 0, ce qui signifie qu'elle est désactivée.

            `other-pane-width` est une option similaire qui contrôle la largeur des autres panes
            qd on utilise le layout `main-vertical`.


    pane-active-border-style my_style

            Configure l'apparence des frontières du pane actif.
            ’my_style’ peut contenir les attributs `fg` et `bg` (les autres sont ignorés).


    pane-base-index 42

            Les panes commenceront à être indexés à partir de 42.


    pane-border-format my_format

            Configure le texte à afficher dans la status line d'un pane, si elle est activée.


    pane-border-status [off | top | bottom]

            Désactive la status line des panes (off), ou l'active en haut (top), ou en bas (bottom).


    pane-border-style my_style

            Set the  pane border  style for panes  aside from  the active pane.  For how  to specify
            style, see the message-command-style option. Attributes are ignored.


    remain-on-exit [on | off]

            A window with this  flag set is not destroyed when the program  running in it exits. The
            window may be reactivated with the respawn-window command.


    synchronize-panes [on | off]

            Duplicate input to any  pane to all other panes in the same  window (only for panes that
            are not in any special mode).


    window-active-style my_style

            Configure le style du pane actif (!= fenêtre active).


    window-status-activity-style style

            Set status line style for windows with an  activity alert. For how to specify style, see
            the message-command-style option.


    window-status-current-format string

            Like window-status-format, but is the format used when the window is the current window.


    window-status-current-style my_style

            Set status line style for the currently active window. For how to specify style, see the
            message-command-style option.


    window-status-format string

            Set the format in which the window is  displayed in the status line window list. See the
            status-left option for details of special  character sequences available. The default is
            ‘#I:#W#F’.


    window-status-last-style my_style

            Set status  line style for  the last active  window. For how  to specify style,  see the
            message-command-style option.


    window-status-separator string

            Sets the  separator drawn between windows  in the status  line. The default is  a single
            space character.


    window-status-style my_style

            Set  status  line  style for  a  single  window.  For  how  to specify  style,  see  the
            message-command-style option.


    window-style my_style

            Set the  default window style. For  how to specify style,  see the message-command-style
            option.


    wrap-search [on | off]

            Qd l'option est activée, une recherche bouclera à la fin/début du contenu du pane.

            Activée par défaut.


    xterm-keys [on | off]

            If this option is set, tmux will  generate xterm(1) -style function key sequences; these
            have a number included to indicate modifiers such  as Shift, Alt or Ctrl. The default is
            off.

## Options sessions

    assume-paste-time milliseconds

            If keys  are entered  faster than  one in milliseconds,  they are  assumed to  have been
            pasted rather  than typed and tmux  key bindings are  not processed. The default  is one
            millisecond and zero disables.


    base-index index

            Set the base index  from which an unused index should be searched  when a new window is
            created. The default is zero.


    default-command shell-command

            Set the command  used for new windows (if  not specified when the window  is created) to
            shell-command, which  may be any  sh(1) command. The default  is an empty  string, which
            instructs tmux to create a login shell using the value of the default-shell option.


    default-shell path

            Specify the  default shell. This  is used as  the login shell  for new windows  when the
            default-command option  is set to empty,  and must be  the full path of  the executable.
            When started  tmux tries to  set a default  value from the  first suitable of  the SHELL
            environment variable, the shell returned by  getpwuid(3), or /bin/sh. This option should
            be configured when tmux is used as a login shell.


    destroy-unattached [on | off]

            If enabled and the session is no longer attached to any clients, it is destroyed.


    detach-on-destroy [on | off]

            Qd cette option est activée (c'est le cas par défaut), le client est automatiquement
            détaché dès qu'on tue la session courante.

            Si l'option est désactivée, le client passe le focus à la plus récemment active des
            sessions restantes.


    display-panes-active-colour colour

            Set the colour  used by the display-panes  command to show the indicator  for the active
            pane.


    display-panes-colour colour

            Set the  colour used by  the display-panes command to  show the indicators  for inactive
            panes.


    display-panes-time time

            Set the time in milliseconds for which the indicators shown by the display-panes command
            appear.


    display-time time

            Set the amount of time for which status line messages and other on-screen indicators are
            displayed. If  set to  0, messages  and  indicators are  displayed until  a key  is
            pressed. time is in milliseconds.


    history-limit 50

            Configure 50 comme étant le nb max de lignes préservées dans l'historique d'une fenêtre.

            Si on change la valeur de cette option, la nouvelle valeur n'affectera que les fenêtres
            nouvellement créées. Les anciennes conservent un historique de la taille définie lors
            de leur création.

            Valeur par défaut:     100
            Valeur max:           1400


    key-table key-table

            Set the default key table to key-table instead of root.


    lock-after-time number

            Lock the session (like the lock-session command) after number seconds of inactivity. The
            default is not to lock (set to 0).


    lock-command shell-command

            Command to run when locking each client. The default is to run lock(1) with -np.


    message-command-style my_style

            Cette option permet de modifier l'apparence de la ligne de commande tmux lorsqu'on
            utilise les raccourcis Vim au lieu d'emacs pour l'éditer, et qu'on est en mode normal.
            C'est-à-dire après avoir appuyé sur Escape.

            ’my_style’ doit être une liste d'attributs séparés par des virgules.
            Un attribut peut être ’bg=colour’, ’fg=colour’.

            ’colour’ peut être:

                    - black
                    - red
                    - green
                    - yellow
                    - blue
                    - magenta
                    - cyan
                    - white
                    - aixterm
                    - brightred
                    - brightgreen
                    - bright…
                    - colour0
                    - …
                    - colour255
                    - default
                    - #{6 digits hex code}

            Un attribut peut également être:

                    - bold
                    - bright
                    - default
                    - dim
                    - underscore
                    - blink
                    - reverse
                    - hidden
                    - italics

            On peut également préfixer le nom d'un attribut avec ’no’.
            Dans ce cas il est désactivé au lieu d'être activé.

            Quelques exemples de valeurs possibles pour ’my_style’:

                    fg=yellow,bold,underscore,blink

                    bg=black,fg=default,noreverse

            Pour simplement ajouter un attribut à ’my_style’, et non remplacer ce dernier entièrement,
            bien penser à passer le flag `-a` (append) à la commande `set-option`.

                                     NOTE:

            La syntaxe de ’my_style’ doit être utilisée pour configurer d'autres options:

                    - message-style                   ligne de commande

                      (session)

                    - mode-style                      indicateur en mode copie

                      (fenêtre)

                    - pane-active-border-style        frontières du pane actif
                      pane-border-style               "          des autres panes
                                                      seul `fg` et `bg` sont pris en compte
                      (fenêtre)

                    - status-left-style               style à appliquer à la partie gauche/droite/centrale
                      status-right-style              de la status line
                      status-style

                      (session)

                    - window-active-style             pane actif

                      (fenêtre)

                    - window-status-activity-style    mise en surbrillance du nom d'une fenêtre active
                    - window-status-current-style     "                           de la fenêtre courante
                    - window-status-last-style        "                           de la fenêtre précédente

                      (fenêtre)

                    - window-style                    panes inactifs

                      (fenêtre)

            Elle peut aussi être utilisée dans une séquence de caractères spéciaux (#[…]) au sein
            de la chaîne donnée en valeur aux options:

                    - status-left     info à afficher dans la partie gauche de la status line
                      status-right    "                              droite "

                      (session)

            Exemple:    #[fg=red,bright]


    message-style my_style

            Configure l'apparence de la ligne de commande.

            On peut aussi configurer les attributs ’fg’ et ’bg’ de l'option `message-style` via
            les “pseudo-options“:

                    - message-fg
                    - message-bg

            Il ne s'agit pas de vraies options. Elles ne sont pas listées qd on tape `show-options -g`.
            Elles ne servent qu'à permettre de modifier les attributs ’fg’ et ’bg’ de `message-style`,
            sans devoir redéfinir tous les autres attributs.


    mouse [on | off]

            If on, tmux captures the mouse and allows  mouse events to be bound as key bindings. See
            the MOUSE SUPPORT section for details.


    prefix  M-Space
    prefix2 C-Space

            Configure `M-Space` et `C-Space` comme étant des touches préfixe.


    renumber-windows [on | off]

            Qd l'option est activée, à chaque fois qu'une fenêtre est fermée, les autres sont renumérotées.

            Permet d'éviter que des "trous" se créent.
            Pex, si on:

                    - on désactive l'option `renumber-windows`:

                            set-option -s renumber-windows off

                    - crée les fenêtres 1, 2, 3

                    - on supprime la fenêtre 2

            On termine avec les fenêtres 1 et 3 (2 manque, il y a un trou).


    repeat-time time

            Allow  multiple commands  to be  entered without  pressing the  prefix-key again  in the
            specified time milliseconds (the default is 500).  Whether a key repeats may be set when
            it is bound using the -r flag to  bind-key. Repeat is enabled for the default keys bound
            to the resize-pane command.


    set-titles-string string

            String used to set  the window title if set-titles is on. Formats  are expanded, see the
            FORMATS section.


    status [on | off]

            Show or hide the status line.


    status-interval interval

            Update the status bar  every interval seconds. By default, updates  will occur every 15.
            seconds A setting of zero disables redrawing at interval                               .


    status-justify [left | centre | right]

            Set the position of the window list component  of the status line: left, centre or right
            justi‐ fied.


    status-keys [vi | emacs]

            Use  vi or  emacs-style key  bindings in  the status  line, for  example at  the command
            prompt. The default is emacs, unless the  VISUAL or EDITOR environment variables are set
            and contain the string ‘vi’.


    status-left string

            Display string  (by default  the session  name) to the  left of  the status  bar. string
            will  be  passed  through  strftime(3)  and formats  (see  FORMATS)  will  be  expanded.
            It  may  also contain  the  special  character sequence  #[]  to  change the  colour  or
            attributes, for example  ‘#[fg=red,bright]’ to set a bright red  foreground. See the
            message-command-style option for a description of colours and attributes.

            For details on how the names and titles can be set see the NAMES AND TITLES section.

            Examples are:

                    #(sysctl vm.loadavg)
                    #[fg=yellow,bold]#(apm -l)%%#[default] [#S]

            The default is ‘[#S] ’.


    status-left-length length

            Set the maximum length of the left component of the status bar. The default is 10.


    status-left-style my_style

            Set the style  of the left part  of the status line.  For how to specify  style, see the
            message-command-style option.


    status-position [top | bottom]

            Set the position of the status line.


    status-right string

            Display string to the  right of the status bar. By default, the  current window title in
            double quotes,  the date and  the time  are shown. As  with status-left, string  will be
            passed to strftime(3) and character pairs are replaced.


    status-right-length length

            Set the maximum length of the right component of the status bar. The default is 40.


    status-right-style my_style

            Set the style  of the right part of the  status line. For how to specify  style, see the
            message-command-style option.


    status-style my_style

            Set status line style. For how to specify style, see the message-command-style option.


    update-environment variables

            Configure un ensemble de variables comme devant être copiées dans l'environnement d'une
            session nouvellement créée, ou préexistante et réattachée (qui viendrait d'où? d'un autre serveur?).

            Les variables doivent être écrites dans une chaîne et séparées par des espaces.

            Si une des variables au sein de la chaîne n'existe pas dans l'environnement global de tmux,
            au lieu d'être copiée dans l'environnement de la session (impossible dans ce cas),
            elle est marquée pour être supprimée de l'environnement de la session
            (à condition qu'elle y existe j'imagine…), à chaque fois qu'on lance un nouveau processus.

            Le résultat est identique à:

                    setenv -r VAR

            … où $VAR est une variable d'environnement présente au sein de la chaîne 'variables'
            (elle-même donnée en valeur à l'option `update-environment`), et absente de l'environment
            global.


            Par défaut, la chaîne contient:

                    DISPLAY
                    SSH_AGENT_PID
                    SSH_ASKPASS
                    SSH_AUTH_SOCK
                    SSH_CONNECTION
                    WINDOWID
                    XAUTHORITY


    visual-activity [on | off]

            If on,  display a status  line message when  activity occurs in  a window for  which the
            monitor-activity window option is enabled.


    visual-silence [on | off]

            If monitor-silence  is enabled,  prints a message  after the interval  has expired  on a
            given window.


    word-separators string

            Sets the session's conception of what characters are considered word separators, for the
            purposes  of the next and  previous word commands in  copy mode. The default  is ‘
            -_@’.

# Layout

Tous les raccourcis qui suivent doivent être précédés de pfx.

    Esc

            Change le layout des panes.
            Alterne entre plusieurs layouts préexistants.


    C-o    M-o

            Rotation des panes dans le sens horaire ou anti-horaire.


    x    X

            Échange la position du pane actif avec celle du précédent / suivant.


    T

            Convertit le pane en fenêtre.

    c

            Crée une nouvelle fenêtre.

    *

            Affiche les n° des panes.


    join -s session:window.pane
    C-j

            Amène le pane de la fenêtre d'une session arbitraire dans la fenêtre courante.
            Pour se référer à une fenêtre, on peut utiliser indifféremment un index ou un nom.

            Mnémotechnique:    -s = src-pane
                                j = vers le bas (reçoit)


    join -t session:window
    C-k

            Envoit le pane courant dans la fenêtre d'une session.

            Mnémotechnique:    -t = target-pane
                                k = vers le haut (envoie)
            la fenêtre doit exister au préalable, elle ne peut pas être créée automatiquement


    d    D

            Ferme le pane / la fenêtre ayant le focus.


    HJKL

            Redimensionne le pane dans une des 4 directions principales.
            On peut aussi utiliser la souris.

# Copier-Coller
## Modes

Les modes copie et normal de tmux correspondent resp. aux modes normal et commande de vim.
La différence de terminologie viennent du fait qu'on ne fait pas la même chose en temps normal
dans vim et dans tmux.

    pfx Space

            passer en mode copie


    pfx PgUp

            passer en mode copie et faire un scrollback d'une page en arrière


    copy_v    copy_Space
    copy_V

            depuis le mode copie, passer en mode visuel (characterwise / linewise)

            En réappuyant sur v / V, on redéfinit le début de la sélection à l'endroit où se trouve le curseur.


    copy_v r

            visual block

            En réappuyant sur r, on alterne entre mode visuel et mode visuel par bloc.


    copy_C-m    copy_q

            revenir au mode normal

## Raccourcis

    Enter
    sélection souris

            copier dans un buffer tmux

    copy_y

            Copie la sélection dans le buffer système.

            Ce raccourci est fourni par tmux-yank:

                    https://github.com/tmux-plugins/tmux-yank

            Il nécessite l'installation du paquet xclip ou xsel.
            Préférer xsel:

                    https://wiki.archlinux.org/index.php/Tmux#X_clipboard_integration

            FIXME: cassé; à réparer; en conflit avec un mapping perso


    copy_Y

            Copie la sélection dans un buffer tmux et la coller automatiquement dans la ligne de
            commande (tmux-yank).

            Attention  à  ne pas  copier  un  caractère  de trop  à  la  fin, autrement  il  sera
            interprété comme  un retour  à la ligne,  ce qui  aura le même  effet que  taper sur
            entrée (du coup, pas le temps de relire la ligne de commande avant de valider).


    pfx y

            Copie la ligne de commande (tmux-yank) dans le buffer système
            et dans un buffer tmux. Fonctionne même si la commande se poursuit sur plusieurs lignes

            FIXME: cassé?


    pfx p
    pfx P

            Colle le dernier buffer tmux / celui de son choix (custom).


    pfx -
    pfx +

            Supprime le dernier buffer tmux.
            Écrit le presse-papier système dans un buffer tmux. (custom)


tmux-copycat est un plugin fournissant différents raccourcis pour sélectionner du texte plus rapidement.
https://github.com/tmux-plugins/tmux-copycat

Pour qu'il fonctionne correctement, il ne faut pas que `~/.tmux.conf` contienne la ligne :

        bind -t vi-copy Escape cancel

… associe à escape à la sortie du mode copie. Source:

        https://github.com/tmux-plugins/tmux-copycat/blob/master/docs/limitations.md


    pfx C-f
    pfx C-g
    pfx C-d
    pfx C-u
    pfx M-i
    pfx M-h
    pfx /string
    pfx /pattern[[:digit:]]\\+

            Passer en mode visuel, et chercher le prochain:

                    - chemin (relatifs / absolus) vers un nom de fichier
                    - nom de fichier, après un git status
                    - nombre (mnémotechnique: d = digit)
                    - url
                    - @ipv4
                    - sha1 (utile après un git log)
                    - occurrence de `string`
                    - "              `pattern` suivi d'un nb à 1 ou plusieurs chiffres

            S'il y a d'autres occurrences, on peut naviguer entre elles via `n` et `N`.

## Copier avec la souris

Une copie à la souris pose 2 pbs :

1) tmux capture la copie dans un de ses buffers inaccessible aux autres applications.

Solution : on peut envoyer l'évènement 'copie avec la souris' directement à guake via le raccourci :

        shift + sélection souris + clic-droit + copy

2) dans guake via le raccourci précédent, si on a 2 panes adjacents (horizontalement),
la sélection d'une ligne complète avec la souris, va déborder sur plusieurs panes.

Solution : utiliser le raccourci guake suivant, qui réalise une sélection en bloc :

        ctrl + shift + sélection souris + clic-droit + copy

Une autre solution consiste à zoomer temporairement le pane dans lequel on veut copier du texte,
puis utiliser le précédent raccourci (shift + sélection souris).

Si on  n'utilise pas guake,  on peut aussi  désactiver temporairement le  mode souris, le  temps de
copier, puis le réactiver via :

        pfx m
        pfx M

# Ouvrir
## des fichiers

    o

            en mode visuel, ouvrir le nom de fichier / url sélectionné avec le programme associé par défaut

    C-o

            en mode visuel, ouvrir le nom de fichier sélectionné avec l'éditeur par défaut


Ces raccourcis sont fournis par le plugin tmux-open :

        https://github.com/tmux-plugins/tmux-open

On peut les modifier en écrivant dans ~/.tmux.conf (pex) :

        set-option -g @open        'x'
        set-option -g @open-editor 'C-x'

## des urls

    pfx u

            Visualiser les liens présents dans le pane.

Ce raccourci nécessite l'installation du paquet urlview et de l'addon tmux-urlview (pour la définition du hotkey).
https://github.com/tmux-plugins/tmux-urlview

On peut changer le raccourci en écrivant dans ~/.tmux.conf (pex) :

        set-option -g @urlview-key 'x'

Remarques :
On peut se rendre directement à une url en tapant son n° d'index.
On peut éditer une url avant d'appuyer sur entrée.

Si une url est trop longue pour tenir sur une ligne, urlview ne retient que la 1e ligne,
ce qui rend le lien inexploitable à moins de l'éditer.

Les liens sont dépourvus de contexte.

# Scripting

    send-keys -t 1.2 echo hello Enter
    send

            Tape `echo hello` dans le 2e pane de la 1e fenêtre de la session tmux courante.

            `send-keys` reconnaît certaines touches spéciales tq ’C-a’ ou ’npage’.
            On peut désactiver cette reconnaissance via l'argument `-l` (literal).

            La syntaxe générale de `send-keys` est:

                    :send-keys [-lR] [-t target-pane] key ...

            L'argument -R demande à ce que l'état du terminal soit reset (kézako?).

            On peut utiliser `send-keys` depuis 3 contextes différents:

                    - un script bash
                    - une session interactive en préfixant la commande avec pfx
                    - une session Vim. Ex:

                            call system('tmux send-keys -t 1.2 "echo hello" Enter')


    break-pane -d -t 1.2 -P -F '#{window_index}'

            Sépare le pane ciblé par `-t` de la fenêtre qui le contient, pour en faire le seul pane
            dans une nouvelle fenêtre.

            Les arguments `-d`, `-P` et `-F` signifient resp. :

                    * -d    le pane ne doit pas devenir la fenêtre courante

                    * -P    affiche des informations à propos de la nouvelle fenêtre créée
                            Par défaut, `break-pane` utilise le format suivant:

                                    #{session_name}:#{window_index}

                    * -F    utilise le format qui suit pour afficher les infos

# -----------------------------------------------
# Raccourcis

    $ man tmux
    /key bindings

            liste des raccourcis par défaut


    bind-key [-nr] [-t mode-table] [-T key-table] key command [arguments]
    bind

            Bind key key to command. Keys are bound in a key table. By default (without -T), the key
            is bound in the  prefix key table. This table is used for  keys pressed after the prefix
            key (for  example, by default  ‘c’ is  bound to new-window  in the prefix  table, so
            ‘C-b c’ creates a  new window). The root ta‐ ble is used  for keys pressed without
            the prefix key: binding ‘c’ to new-window  in the root table (not recommended) means
            a plain ‘c’ will create  a new window. -n is an alias for -T  root. Keys may also be
            bound in custom key tables and the switch-client  -T command used to switch to them from
            a key binding. The -r flag indicates this key may repeat, see the repeat-time option.

            If -t is present, key is bound in mode-table.

            To view the default bindings and possible commands, see the list-keys command.


    list-keys
    lsk

            Affiche tous les raccourcis claviers.


    lsk -T prefix

            Affiche la table des raccourcis commençant par pfx.


    lsk -t vi-choice

            Affiche la table des raccourcis dont le mode est vi-choice.

            Il existe 2 modes différents:

                    - emacs-choice
                    - vi-choice

            Il s'agit de raccourcis permettant de:

            Mode key bindings are defined in two tables: vi-choice and emacs-choice for keys used
            when choosing from lists (such as produced by the choose-window command).

                    - sélectionner (menu choose-window pex)
                    - copie
                    - édition (ligne de commande; pfx :)


            Les flags `-n` et `-r` signifient resp.:

                    - no-prefix;
                      le raccourci n'a pas besoin du prefix

                    - repeat-time;
                      une fois le prefix et le raccourci tapés, on dispose d'un bref délai pdt
                      lequel on peut retaper le raccourci sans le prefix


    send-keys [-lMRX] [-N repeat-count] [-t target-pane] key ...
    send

            Send a  key or  keys to a  window. Each  argument key is  the name of  the key  (such as
            ‘C-a’ or ‘npage’ ) to send; if the string is not recognised as a key, it is sent
            as a  series of  characters. The -l  flag disables  key name lookup  and sends  the keys
            literally. All arguments  are sent sequentially from  first to last. The  -R flag causes
            the terminal state to be reset.

            -M passes through a mouse event (only valid if bound to a mouse key binding, see MOUSE SUPPORT).

            -X is  used to send a  command into copy  mode - see  the WINDOWS AND PANES  section. -N
            specifies a repeat count to a copy mode command.


    send-prefix [-2] [-t target-pane]

            Send the prefix key, or with -2 the secondary prefix key, to a window as if it was pressed.


    status-keys [vi | emacs]

            Use vi or emacs-style key bindings in the status line, for example at the command prompt.  The
            default is emacs, unless the VISUAL or EDITOR environment variables are set and contain the
            string ‘vi’.


    unbind-key [-an] [-t mode-table] [-T key-table] key
    unbind

            Unbind the command  bound to key. -n, -T and  -t are the same as for  bind-key. If -a is
            present, all key bindings are removed.


    tmux allows a  command to be bound to most  keys, with or without a prefix  key. When specifying
    keys, most represent themselves (for example ‘A’ to ‘Z’). Ctrl keys may be prefixed with
    ‘C-’ or ‘^’, and Alt (meta) with  ‘M-’. In addition, the following special key names
    are accepted: Up, Down,  Left, Right, BSpace, BTab, DC (Delete), End, Enter,  Escape, F1 to F12,
    Home, IC (Insert), NPage/PageDown/PgDn, PPage/PageUp/PgUp, Space, and Tab. Note that to bind the
    ‘"’ or ‘'’ keys, quotation marks are necessary, for example:

            bind-key '"' split-window
            bind-key "'" new-window


# Commandes
## Shell

    $ tmux -V

            Affiche dans quelle version est installée tmux.


    pfx    :<cmd>
    $ tmux <cmd>

            Envoyer <cmd> à tmux en cli (mode script) ou depuis une session (mode interactif).

            Ceci illustre que toutes les commandes tmux peuvent être scriptées simplement en étant
            préfixées par la commande shell `tmux`. Par exemple:

                    $ tmux new-session -s basic
                    :      new-session -s basic


    $ exit

            Ferme le shell et son pane ainsi que:

                    - la fenêtre courante si elle ne contient qu'un pane

                    - la session courante si elle ne contient qu'une fenêtre, elle-même ne contenant
                      qu'un pane

            Si `exit` ferme la session courante, et que le serveur tmux fait tourner plusieurs
            sessions, il ne donne pas le focus à une autre.
            Toutefois, on peut toujours se rattacher à l'une d'elles via `$ tmux a`.


    $ tmux -S /tmp/your_shared_session
    $ chmod 777 /tmp/your_shared_session

            Start a shared session (partage de terminal / pair programming).
            Il faut être connecté en tant que même user sur le serveur.
            Conseil : maximiser son terminal et diminuer la police d'écriture pour chacun.

## Navigation

    switch-client -p
    switch-client -n
    pfx (
    pfx )

            Naviguer entre les différentes sessions.


    choose-tree
    choose-window

    pfx s
    pfx w

            Sélectionne  une autre  session  / fenêtre  via  un menu.

            Espace  permet de  déplier l'affichage des fenêtres d'une session.
            Dans le menu des sessions, le symbole + devant le  nom d'une  session peut  être déplié
            via la  flèche droite,  afin de  se rendre spécifiquement dans une de ses fenêtres.


    command-prompt "find-window '%%'"
    f string

            Donne le focus à la fenêtre qui affiche qq part à l'écran la chaîne 'string'.


    select-window -t :=3
    pfx 3

    command-prompt -p index "select-window -t ':%%'"
    pfx ' 42


            Donne le focus à la fenêtre 3 / 42.
            Si l'index de la fenêtre est composé de plusieurs chiffres, seule la 2e syntaxe est possible.


    last-pane
    pfx pfx

            alterner entre le pane courant et le dernier actif

## Panes

     capture-pane [-aepPqCJ] [-b buffer-name] [-E end-line] [-S start-line] [-t target-pane]
     capturep

             Capture the contents of a pane.  If -p is given, the output goes to stdout, otherwise to the buffer
             specified with -b or a new buffer if omitted.  If -a is given, the alternate screen is used, and the
             history is not accessible.  If no alternate screen exists, an error will be returned unless -q is
             given.  If -e is given, the output includes escape sequences for text and background attributes.  -C
             also escapes non-printable characters as octal \xxx.  -J joins wrapped lines and preserves trailing
             spaces at each line's end.  -P captures only any output that the pane has received that is the begin‐
             ning of an as-yet incomplete escape sequence.

             -S and -E specify the starting and ending line numbers, zero is the first line of the visible pane and
             negative numbers are lines in the history.  ‘-’ to -S is the start of the history and to -E the end of
             the visible pane.  The default is to capture only the visible contents of the pane.


    kill-pane [-a] [-t target-pane]
    killp

            Destroy the given pane.  If no panes remain in the containing window, it is also destroyed.  The -a
            option kills all but the pane given with -t.


    resize-pane [-DLMRUZ] [-t target-pane] [-x width] [-y height] [adjustment]
    resizep

            Resize a pane, up, down, left or right by adjustment with -U, -D, -L or -R, or to an absolute size with
            -x or -y.  The adjustment is given in lines or cells (the default is 1).

            With -Z, the active pane is toggled between zoomed (occupying the whole of the window) and unzoomed
            (its normal position in the layout).

            -M begins mouse resizing (only valid if bound to a mouse key binding, see MOUSE SUPPORT).


    select-pane [-DdegLlMmRU] [-P my_style] [-t target-pane]
    selectp

            Make pane target-pane the active pane in window target-window, or set its style (with -P).  If one of
            -D, -L, -R, or -U is used, respectively the pane below, to the left, to the right, or above the target
            pane is used.  -l is the same as using the last-pane command.  -e enables or -d disables input to the
            pane.

            -m and -M are used to set and clear the marked pane.  There is one marked pane at a time, setting a new
            marked pane clears the last.  The marked pane is the default target for -s to join-pane, swap-pane and
            swap-window.

            Each pane has a style: by default the window-style and window-active-style options are used,
            select-pane -P sets the style for a single pane.  For example, to set the pane 1 background to red:

                    select-pane -t:.1 -P 'bg=red'

            -g shows the current pane style.


## Divers

    clock-mode [-t target-pane]
    pfx t

            Affiche l'heure.


    show-messages [-JT] [-t target-client]
    showmsgs
    pfx ~

            Show client  messages or server information.  Any messages displayed on  the status line
            are  saved in  a  per-client message  log, up  to  a maximum  of  the limit  set by  the
            message-limit server option. With -t, display the  log for target-client. -J and -T show
            debugging information about jobs and terminals.


            Affiche les derniers messages de tmux.

            Utile pour relire les messages d'erreurs si le fichier de configuration contient
            une erreur de syntaxe. Penser à recharger ce dernier avant de taper `pfx ~`.
            En effet, la 1e fois qu'on lance tmux, si des erreurs surviennent et que tmux les affichent,
            il ne semble pas les mémoriser pour autant.


## Sessions

    a[ttach-session] -t foo

            Restaurer la session foo (n° ou nom).
            On dit aussi qu'on l'attache au terminal (en fait il s'agit de relancer un client tmux).


    break-pane [-dP] [-F format] [-s src-pane] [-t dst-window]
    breakp

            Break src-pane off from its containing window to make it the only pane in dst-window.  If -d is given,
            the new window does not become the current window.  The -P option prints information about the new win‐
            dow after it has been created.  By default, it uses the format ‘#{session_name}:#{window_index}’ but a
            different format may be specified with -F.


    copy-mode [-Meu] [-t target-pane]

            Enter copy mode.  The -u option scrolls one page up.  -M begins a mouse drag (only valid if bound to a
            mouse key binding, see MOUSE SUPPORT).  -e specifies that scrolling to the bottom of the history (to
            the visible screen) should exit copy mode.  While in copy mode, pressing a key other than those used
            for scrolling will disable this behaviour.  This is intended to allow fast scrolling through a pane's
            history, for example with:

                    bind PageUp copy-mode -eu


    detach
    pfx @

            se détacher de la session (tuer le client tmux)


    display-message [-p] [-c target-client] [-t target-pane] [message]
    display

            Display a message.
            If -p  is given, the  output is printed  to stdout, otherwise  it is
            displayed in the target-client status line.
            The  format  of  message  is   described  in  the  FORMATS  section;
            information is taken from target-pane  if -t is given, otherwise the
            active pane for the session attached to target-client.


    if-shell [-bF] [-t target-pane] shell-command command [command]
    if

            Execute the first command if shell-command returns success or the second command otherwise.  Before
            being executed, shell-command is expanded using the rules specified in the FORMATS section, including
            those relevant to target-pane.  With -b, shell-command is run in the background.

            If -F is given, shell-command is not executed but considered success if neither empty nor zero (after
            formats are expanded).


    kill-session -t foo
    kill-window  -t foo
    kill-server

            Fermer la session `foo`, la fenêtre `foo`, le serveur tmux.


    last-pane [-de] [-t target-window]
    lastp

            Select the last (previously selected) pane.  -e enables or -d disables input to the pane.


    list-sessions
    ls

            Lister les sessions actives.


    new-session [-AdDEP] [-c start-directory] [-F format] [-n window-name] [-s session-name] [-t target-session]
                [-x width] [-y height] [shell-command]
    new

            Create a new session with name session-name.

            The new session is attached to the current terminal unless -d is given.  window-name and shell-command
            are the name of and shell command to execute in the initial window.  If -d is used, -x and -y specify
            the size of the initial window (80 by 24 if not given).

            If run from a terminal, any termios(4) special characters are saved and used for new windows in the new
            session.

            The -A flag makes new-session behave like attach-session if session-name already exists; in this case,
            -D behaves like -d to attach-session.

            If -t is given, the new session is grouped with target-session.  This means they share the same set of
            windows - all windows from target-session are linked to the new session, any new windows are linked to
            both sessions and any windows closed removed from both sessions.  The current and previous window and
            any session options remain independent and either session may be killed without affecting the other.
            -n and shell-command are invalid if -t is used.

            The -P option prints information about the new session after it has been created.  By default, it uses
            the format ‘#{session_name}:’ but a different format may be specified with -F.

            If -E is used, the update-environment option will not be applied.


    new-session -s basic [-d]

            Lancer une nouvelle session intitulée basic.
            L'option `-d` permet de lancer la session en mode détaché.


    new-window [-adkP] [-c start-directory] [-F format] [-n window-name] [-t target-window] [shell-command]
    neww

            Create a new window.  With -a, the new window is inserted at the next index up from the specified
            target-window, moving windows up if necessary, otherwise target-window is the new window location.

            If -d is given, the session does not make the new window the current window.  target-window represents
            the window to be created; if the target already exists an error is shown, unless the -k flag is used,
            in which case it is destroyed.  shell-command is the command to execute.  If shell-command is not spec‐
            ified, the value of the default-command option is used.  -c specifies the working directory in which
            the new window is created.

            When the shell command completes, the window closes.  See the remain-on-exit option to change this be‐
            haviour.

            The TERM environment variable must be set to “screen” for all programs running inside tmux.  New
            windows will automatically have “TERM=screen” added to their environment, but care must be taken not to
            reset this in shell start-up files.

            The -P option prints information about the new window after it has been created.  By default, it uses
            the format ‘#{session_name}:#{window_index}’ but a different format may be specified with -F.


    next-layout [-t target-window]
    nextl

            Move a window to the next layout and rearrange the panes to fit.


    next-window [-a] [-t target-session]
    next

            Move to the next window in the session.  If -a is used, move to the next window with an alert.


    previous-window [-a] [-t target-session]
    prev

            Move to the previous window in the session.  With -a, move to the previous window with an alert.


    rename-session [-t target-session] new-name
    rename
    pfx $

            Rename the session to new-name.


    rename-window [-t target-window] new-name
    renamew
    pfx ,

            Rename the current window, or the window at target-window if specified, to new-name.


    run-shell [-b] [-t target-pane] shell-command
    run

            Execute shell-command in the background without creating a window.  Before being executed, shell-com‐
            mand is expanded using the rules specified in the FORMATS section.  With -b, the command is run in the
            background.  After it finishes, any output to stdout is displayed in copy mode (in the pane specified
            by -t or the current pane if omitted).  If the command doesn't return success, the exit status is also
            displayed.


    source-file [-q] path
    source

            Execute commands from path.  If -q is given, no error will be returned if path does not exist.


    split-window [-bdfhvP] [-c start-directory] [-l size | -p percentage] [-t target-pane] [shell-command] [-F format]
    splitw

            Create a new pane by splitting target-pane: -h does a horizontal split and -v a vertical split; if nei‐
            ther is specified, -v is assumed.  The -l and -p options specify the size of the new pane in lines (for
            vertical split) or in cells (for horizontal split), or as a percentage, respectively.  The -b option
            causes the new pane to be created to the left of or above target-pane.  The -f option creates a new
            pane spanning the full window height (with -h) or full window width (with -v), instead of splitting the
            active pane.  All other options have the same meaning as for the new-window command.


    swap-window [-d] [-s src-window] [-t dst-window]
    swapw

            This is similar to link-window, except the source and destination windows are swapped.  It is an error
            if no window exists at src-window.

            Like swap-pane, if -s is omitted and a marked pane is present (see select-pane -m), the window contain‐
            ing the marked pane is used rather than the current window.


## Fenêtres

    kill-window [-a] [-t target-window]
    killw

            Kill the current window or the window at target-window, removing it from any sessions to which it is
            linked.  The -a option kills all but the window given with -t.

# -----------------------------------------------
# Commands

    :list-commands

            afficher toutes les commandes dispo

     This section contains a list of the commands supported by tmux.  Most commands accept the optional -t (and
     sometimes -s) argument with one of target-client, target-session target-window, or target-pane.  These specify
     the client, session, window or pane which a command should affect.

     target-client is the name of the pty(4) file to which the client is connected, for example either of /dev/ttyp1
     or ttyp1 for the client attached to /dev/ttyp1.  If no client is specified, tmux attempts to work out the
     client currently in use; if that fails, an error is reported.  Clients may be listed with the list-clients com‐
     mand.

     target-session is tried as, in order:

           1.   A session ID prefixed with a $.

           2.   An exact name of a session (as listed by the list-sessions command).

           3.   The start of a session name, for example ‘my_sess’ would match a session named ‘my_session’.

           4.   An fnmatch(3) pattern which is matched against the session name.

     If the session name is prefixed with an ‘=’, only an exact match is accepted (so ‘=my_sess’ will only match
     exactly ‘my_sess’, not ‘my_session’).

     If a single session is found, it is used as the target session; multiple matches produce an error.  If a ses‐
     sion is omitted, the current session is used if available; if no current session is available, the most
     recently used is chosen.

     target-window (or src-window or dst-window) specifies a window in the form session:window.  session follows the
     same rules as for target-session, and window is looked for in order as:

           1.   A special token, listed below.

           2.   A window index, for example ‘my_session:1’ is window 1 in session ‘my_session’.

           3.   A window ID, such as @1.

           4.   An exact window name, such as ‘my_session:my_window’.

           5.   The start of a window name, such as ‘my_session:my_win’.

           6.   As an fnmatch(3) pattern matched against the window name.

     Like sessions, a ‘=’ prefix will do an exact match only.  An empty window name specifies the next unused index
     if appropriate (for example the new-window and link-window commands) otherwise the current window in session is
     chosen.

     The following special tokens are available to indicate particular windows.  Each has a single-character alter‐
     native form.

     Token              Meaning
     {start}       ^    The lowest-numbered window
     {end}         $    The highest-numbered window
     {last}        !    The last (previously current) window
     {next}        +    The next window by number
     {previous}    -    The previous window by number

     target-pane (or src-pane or dst-pane) may be a pane ID or takes a similar form to target-window but with the
     optional addition of a period followed by a pane index or pane ID, for example: ‘my_session:my_window.1’.  If the
     pane index is omitted, the currently active pane in the specified window is used.  The following special tokens
     are available for the pane index:

     Token                  Meaning
     {last}            !    The last (previously active) pane
     {next}            +    The next pane by number
     {previous}        -    The previous pane by number
     {top}                  The top pane
     {bottom}               The bottom pane
     {left}                 The leftmost pane
     {right}                The rightmost pane
     {top-left}             The top-left pane
     {top-right}            The top-right pane
     {bottom-left}          The bottom-left pane
     {bottom-right}         The bottom-right pane
     {up-of}                The pane above the active pane
     {down-of}              The pane below the active pane
     {left-of}              The pane to the left of the active pane
     {right-of}             The pane to the right of the active pane

     The tokens ‘+’ and ‘-’ may be followed by an offset, for example:

           select-window -t:+2

     In addition, target-session, target-window or target-pane may consist entirely of the token ‘{mouse}’ (alterna‐
     tive form ‘=’) to specify the most recent mouse event (see the MOUSE SUPPORT section) or ‘{marked}’ (alterna‐
     tive form ‘~’) to specify the marked pane (see select-pane -m).

     Sessions, window and panes are each numbered with a unique ID; session IDs are prefixed with a ‘$’, windows
     with a ‘@’, and panes with a ‘%’.  These are unique and are unchanged for the life of the session, window or
     pane in the tmux server.  The pane ID is passed to the child process of the pane in the TMUX_PANE environ‐
     ment variable.  IDs may be displayed using the ‘session_id’, ‘window_id’, or ‘pane_id’ formats (see the FORMATS
     section) and the display-message, list-sessions, list-windows or list-panes commands.

     shell-command arguments are sh(1) commands.  This may be a single argument passed to the shell, for example:

           new-window 'vi /etc/passwd'

     Will run:

           /bin/sh -c 'vi /etc/passwd'

     Additionally, the new-window, new-session, split-window, respawn-window and respawn-pane commands allow
     shell-command to be given as multiple arguments and executed directly (without ‘sh -c’).  This can avoid issues
     with shell quoting.  For example:

           $ tmux new-window vi /etc/passwd

     Will run vi(1) directly without invoking the shell.

     command [arguments] refers to a tmux command, passed with the command and arguments separately, for exam‐
     ple:

           bind-key F1 set-window-option force-width 81

     Or if using sh(1):

           $ tmux bind-key F1 set-window-option force-width 81

     Multiple commands may be specified together as part of a command sequence.  Each command should be separated by
     spaces and a semicolon; commands are executed sequentially from left to right and lines ending with a backslash
     continue on to the next line, except when escaped by another backslash.  A literal semicolon may be included by
     escaping it with a backslash (for example, when specifying a command sequence to bind-key).

     Example tmux commands include:

           refresh-client -t/dev/ttyp2

           rename-session -tfirst newname

           set-window-option -t:0 monitor-activity on

           new-window ; split-window -d

           bind-key R source-file ~/.tmux.conf \; \
                   display-message "source-file done"

     Or from sh(1):

           $ tmux kill-window -t :1

           $ tmux new-window \; split-window -d

           $ tmux new-session -d 'vi /etc/passwd' \; split-window -d \; attach

# Clients and Sessions

     The tmux server manages clients, sessions, windows  and panes. Clients are attached to sessions
     to interact with them, either when they are created with the new-session command, or later with
     the attach-session command. Each session has one or more windows linked into it. Windows may be
     linked to  multiple sessions and are  made up of  one or more  panes, each of which  contains a
     pseudo terminal. Commands for creating, linking  and otherwise manipulating windows are covered
     in the WINDOWS AND PANES section.


     The following commands are available to manage clients and sessions:


     attach-session [-dEr] [-c working-directory] [-t target-session]
     attach

             If run from outside tmux, create a new  client in the current terminal and attach it to
             target-session. If used from inside, switch the current client. If -d is specified, any
             other  clients  attached to  the  session  are detached.  -r  signifies  the client  is
             read-only (only  keys bound  to the  detach-client or  switch-client commands  have any
             effect)

             If no server is started, attach-session will attempt to start it; this will fail unless
             sessions are created in the configuration file.

             The target-session  rules for attach-session  are slightly  adjusted: if tmux  needs to
             select the most recently used session, it will prefer the most recently used unattached
             session.

             -c will set the session working directory (used for new windows) to working-directory.

             If -E is used, the update-environment option will not be applied.


     detach-client [-aP] [-s target-session] [-t target-client]
     detach

             Detach the  current client  if bound to  a key,  the client specified  with -t,  or all
             clients currently attached to the session specified  by -s. The -a option kills all but
             the client  given with -t.  If -P is  given, send SIGHUP to  the parent process  of the
             client, typically causing it to exit.


     has-session [-t target-session]
     has

             Report an  error and exit with  1 if the specified  session does not exist.  If it does
             exist, exit with 0.

     kill-server

             Kill the tmux server and clients and destroy all sessions.


     kill-session [-aC] [-t target-session]

             Destroy the given session, closing any windows  linked to it and no other sessions, and
             detaching all clients  attached to it. If  -a is given, all sessions  but the specified
             one is killed. The  -C flag clears alerts (activity, or silence)  in all windows linked
             to the session.


     list-clients [-F format] [-t target-session]
     lsc

             List all  clients attached  to the  server. For  the meaning  of the  -F flag,  see the
             FORMATS section.  If target-session is specified,  list only clients connected  to that
             session.


     list-commands [-F format]
     lscm

             List the syntax of all commands supported by tmux.


     list-sessions [-F format]
     ls

             List all  sessions managed  by the  server. For  the meaning  of the  -F flag,  see the
             FORMATS section.


     lock-client [-t target-client]
     lockc

             Lock target-client, see the lock-server command.


     lock-session [-t target-session]
     locks

             Lock all clients attached to target-session.


     new-session [-AdDEP] [-c start-directory] [-F format] [-n window-name] [-s session-name] [-t target-session]
             [-x width] [-y height] [shell-command]
     new

             Create a new session with name session-name.

             The new session is attached to the current terminal unless -d is given. window-name and
             shell-command are the name of and shell command to execute in the initial window. If -d
             is used, -x and -y specify the size of the initial window (80 by 24 if not given).

             If run from  a terminal, any termios(4)  special characters are saved and  used for new
             windows in the new session.

             The  -A flag  makes  new-session  behave like  attach-session  if session-name  already
             exists; in this case, -D behaves like -d to attach-session.

             If -t is given,  the new session is grouped with target-session.  This means they share
             the  same set  of windows  - all  windows  from target-session  are linked  to the  new
             session, any  new windows are  linked to both sessions  and any windows  closed removed
             from both  sessions. The  current and  previous window and  any session  options remain
             independent  and either  session may  be  killed without  affecting the  other. -n  and
             shell-command are invalid if -t is used.

             The -P option  prints information about the  new session after it has  been created. By
             default,  it uses  the  format ‘#{session_name}:’  but a  different  format may  be
             specified with -F.

             If -E is used, the update-environment option will not be applied.


     refresh-client [-S] [-t target-client]
     refresh

             Refresh the current client if  bound to a key, or a single client  if one is given with
             -t. If -S is specified, only update the client's status bar.


     rename-session [-t target-session] new-name
     rename

             Rename the session to new-name.


     source-file [-q] path
     source

             Execute commands from path.  If -q is given, no error will be returned if path does not exist.


     start-server
     start

             Start the tmux server, if not already running, without creating any sessions.


     suspend-client [-t target-client]
     suspendc

             Suspend a client by sending SIGTSTP (tty stop).


     switch-client [-Elnpr] [-c target-client] [-t target-session] [-T key-table]
     switchc

             Switch the current session for client target-client  to target-session. If -l, -n or -p
             is used,  the client is moved  to the last,  next or previous session  respectively. -r
             toggles whether a client is read-only (see the attach-session command).

             If -E is used, update-environment option will not be applied.

             -T sets the client's  key table; the next key from the client  will be interpreted from
             key-table. This may be  used to configure multiple prefix keys, or  to bind commands to
             sequences of keys. For example, to make typing ‘abc’ run the list-keys command:

                   bind-key -Ttable2 c list-keys
                   bind-key -Ttable1 b switch-client -Ttable2
                   bind-key -Troot   a switch-client -Ttable1

# Windows and Panes

     A tmux window  may be in one  of two modes. The  default permits direct access  to the terminal
     attached to  the window. The other  is copy mode,  which permits a  section of a window  or its
     history to be  copied to a paste buffer  for later insertion into another window.  This mode is
     entered with  the copy-mode command,  bound to ‘[’  by default. It  is also entered  when a
     command that produces output, such as list-keys, is executed from a key binding.

     Commands are  sent to  copy mode using  the -X  flag to  the send-keys command.  When a  key is
     pressed, copy mode automatically uses one of two key tables, depending on the mode-keys option:
     copy-mode  for emacs,  or copy-mode-vi  for vi.  Key tables  may be  viewed with  the list-keys
     command.

     The following commands are supported in copy mode:

           append-selection
           append-selection-and-cancel A
           back-to-indentation         ^
           begin-selection             Space
           bottom-line                 L
           cancel                      q
           clear-selection             Escape
           copy-end-of-line            D
           copy-line
           copy-pipe <command>
           copy-pipe-and-cancel <command>
           copy-selection
           copy-selection-and-cancel   Enter
           cursor-down                 j
           cursor-left                 h
           cursor-right                l
           cursor-up                   k
           end-of-line                 $
           goto-line <line>            :
           halfpage-down               C-d
           halfpage-up                 C-u
           history-bottom              G
           history-top                 g
           jump-again                  ;
           jump-backward <to>          F
           jump-forward <to>           f
           jump-reverse                ,
           jump-to-backward <to>       T
           jump-to-forward <to>        t
           middle-line                 M
           next-paragraph              }
           next-space                  W
           next-space-end              E
           next-word                   w
           next-word-end               e
           other-end                   o
           page-down                   C-f
           page-up                     C-b
           previous-paragraph          {
           previous-space              B
           previous-word               b
           rectangle-toggle            v
           scroll-down                 C-e
           scroll-up                   C-y
           search-again                n
           search-backward <for>       ?
           search-forward <for>        /
           search-reverse              N
           select-line                 V
           start-of-line               0
           stop-selection
           top-line                    H

     The next and  previous word keys use space  and the ‘-’, ‘_’ and  ‘@’ characters as
     word delimiters  by default, but  this can be adjusted  by setting the  word-separators session
     option. Next word  moves to the start of  the next word, next  word end to the end  of the next
     word and  previous word to the  start of the previous  word. The three next  and previous space
     keys work similarly but use a space alone as the word separator.

     The jump commands enable quick movement within a line. For instance, typing ‘f’ followed by
     ‘/’ will move the cursor to the next  ‘/’ character on the current line. A ‘;’ will
     then jump to the next occurrence.

     Commands in  copy mode may  be prefaced by  an optional repeat count.  With vi key  bindings, a
     prefix is  entered using the number  keys; with emacs, the  Alt (meta) key and  a number begins
     prefix entry.

     Mode key  bindings are defined  in two  tables: vi-choice and  emacs-choice for keys  used when
     choosing from lists (such as produced by the choose-window command).

     The synopsis for the copy-mode command is:

     copy-mode [-Meu] [-t target-pane]

             Enter copy mode. The -u option scrolls one  page up. -M begins a mouse drag (only valid
             if bound to a mouse key binding, see MOUSE SUPPORT). -e specifies that scrolling to the
             bottom of  the history (to  the visible  screen) should exit  copy mode. While  in copy
             mode, pressing a key  other than those used for scrolling  will disable this behaviour.
             This is intended to allow fast scrolling through a pane's history, for example with:

                   bind PageUp copy-mode -eu

     Each window displayed by tmux may be split into one or more panes; each pane takes up a certain
     area of  the display and is  a separate terminal.  A window may  be split into panes  using the
     split-window command. Win‐ dows  may be split horizontally (with the  -h flag) or vertically.
     Panes  may  be  resized  with  the  resize-pane  command  (bound  to  ‘C-up’,  ‘C-down’
     ‘C-left’  and  ‘C-right’  by  default),  the  current pane  may  be  changed  with  the
     select-pane command  and the  rotate-window and swap-pane  commands may be  used to  swap panes
     without changing their position.  Panes are numbered beginning from zero in  the order they are
     created.

     A number of preset layouts are available.  These may be selected with the select-layout command
     or cycled with  next-layout (bound to ‘Space’  by default); once a layout  is chosen, panes
     within it may be moved and resized as normal.

     The following layouts are supported:


     even-horizontal

             Panes are spread out evenly from left to right across the window.


     even-vertical

             Panes are spread evenly from top to bottom.


    main-horizontal

             A large  (main) pane  is shown at  the top of  the window  and the remaining  panes are
             spread from left to right in the leftover space at the bottom. Use the main-pane-height
             window option to specify the height of the top pane.


     main-vertical

             Similar to  main-horizontal but the  large pane  is placed on  the left and  the others
             spread from top to bottom along the right. See the main-pane-width window option.


     tiled

            Panes are spread out as evenly as possible over the window in both rows and columns.

     In addition,  select-layout may be used  to apply a  previously used layout -  the list-windows
     command displays the layout  of each window in a form suitable for  use with select-layout. For
     example:

           $ tmux list-windows
           0: ksh [159x48]
               layout: bb62,159x48,0,0{79x48,0,0,79x48,80,0}
           $ tmux select-layout bb62,159x48,0,0{79x48,0,0,79x48,80,0}

     tmux automatically adjusts the size of the layout for the current window size.  Note that a layout cannot
     be applied to a window with more panes than that from which the layout was originally defined.

     Commands related to windows and panes are as follows:

     choose-client [-F format] [-t target-window] [template]

             Put a window  into client choice mode,  allowing a client to  be selected interactively
             from a list. After  a client is chosen, ‘%%’ is replaced by  the client pty(4) path
             in  template and  the result  exe‐ cuted  as  a command.  If template  is not  given,
             "detach-client  -t '%%'"  is used.  For the  meaning of  the -F  flag, see  the FORMATS
             section. This command works only if at least one client is attached.


     choose-session [-F format] [-t target-window] [template]

             Put a window  into session choice mode,  where a session may  be selected interactively
             from a list. When  one is chosen, ‘%%’ is replaced by the  session name in template
             and the result executed as a command. If template is not given, "switch-client -t '%%'"
             is used. For  the meaning of the -F  flag, see the FORMATS section.  This command works
             only if at least one client is attached.


     choose-tree [-suw] [-b session-template] [-c window-template] [-S format] [-W format] [-t target-window]

             Put a window  into tree choice mode,  where either sessions or windows  may be selected
             interactively from a list.  By default, windows belonging to a  session are indented to
             show their relationship to a ses‐ sion.

             Note that the choose-window and choose-session commands are wrappers around choose-tree.

             If -s is given, will show sessions.  If -w is given, will show windows.

             By default,  the tree is collapsed  and sessions must  be expanded to windows  with the
             right arrow key. The -u option will start with all sessions expanded instead.

             If -b is  given, will override the  default session command. Note that  ‘%%’ can be
             used and will be replaced with the session name. The default option if not specified is
             "switch-client -t '%%'". If -c is given, will override the default window command. Like
             -b, ‘%%’ can be  used and will be replaced with the session  name and window index.
             When a  window is chosen from  the list, the session  command is run before  the window
             command.

             -S uses  format instead of  the default  session format and  -W instead of  the default
             window format. For the meaning of format, see the FORMATS section.

             This command works only if at least one client is attached.


     choose-window [-F format] [-t target-window] [template]

             Put a window into window choice mode, where a window may be chosen interactively from a
             list. After a window  is selected, ‘%%’ is replaced by the  session name and window
             index in  template and  the result  executed as a  command. If  template is  not given,
             "select-window  -t '%%'"  is used.  For the  meaning of  the -F  flag, see  the FORMATS
             section. This command works only if at least one client is attached.


     display-panes [-t target-client] [template]
     displayp

             Display  a   visible  indicator  of   each  pane   shown  by  target-client.   See  the
             display-panes-time,   display-panes-colour,  and   display-panes-active-colour  session
             options. While  the indicator is on  screen, a pane may  be chosen with the  ‘0’ to
             ‘9’ keys,  which will  cause template  to be  executed as  a command  with ‘%%’
             substituted by the pane ID. The default template is "select-pane -t '%%'".


     find-window [-CNT] [-F format] [-t target-window] match-string
     findw

             Search for  the fnmatch(3) pattern  match-string in  window names, titles,  and visible
             content (but not history). The flags control matching behavior: -C matches only visible
             window contents, -N matches only the window  name and -T matches only the window title.
             The default is  -CNT. If only one  window is matched, it'll  be automatically selected,
             otherwise a  choice list  is shown. For  the meaning  of the -F  flag, see  the FORMATS
             section. This command works only if at least one client is attached.


     join-pane [-bdhv] [-l size | -p percentage] [-s src-pane] [-t dst-pane]
     joinp

             Like split-window, but instead of splitting dst-pane  and creating a new pane, split it
             and move src-pane into the space. This can be used to reverse break-pane. The -b option
             causes src-pane to be joined to left of or above dst-pane.

             If -s is omitted and a marked pane  is present (see select-pane -m), the marked pane is
             used rather than the current pane.


     last-pane [-de] [-t target-window]
     lastp

             Select the last (previously selected) pane.  -e enables or -d disables input to the pane.


     last-window [-t target-session]
     last

             Select the last (previously selected) window. If no target-session is specified, select
             the last win‐ dow of the current session.


     link-window [-adk] [-s src-window] [-t dst-window]
     linkw

             Link the window  at src-window to the specified dst-window.  If dst-window is specified
             and no such win‐  dow exists, the src-window is linked there. With  -a, the window is
             moved to  the next index up  (follow‐ ing windows are  moved if necessary). If  -k is
             given and dst-window  exists, it is killed,  otherwise an error is generated.  If -d is
             given, the newly linked window is not selected.


     list-panes [-as] [-F format] [-t target]
     lsp

             If -a  is given, target is  ignored and all  panes on the  server are listed. If  -s is
             given, target is a  session (or the current session). If neither is  given, target is a
             window  (or the  current window).  For the  meaning  of the  -F flag,  see the  FORMATS
             section.


     list-windows [-a] [-F format] [-t target-session]
     lsw

             If -a is given, list all windows on  the server. Otherwise, list windows in the current
             session or in target-session. For the meaning of the -F flag, see the FORMATS section.


     move-pane [-bdhv] [-l size | -p percentage] [-s src-pane] [-t dst-pane]
     movep

             Like join-pane, but src-pane and dst-pane may belong to the same window.


     move-window [-ardk] [-s src-window] [-t dst-window]
     movew

             This is similar to link-window, except the window at src-window is moved to dst-window.
             With -r, all windows in the session  are renumbered in sequential order, respecting the
             base-index option.


     new-window [-adkP] [-c start-directory] [-F format] [-n window-name] [-t target-window] [shell-command]
     neww

             Create a new window. With -a, the new window  is inserted at the next index up from the
             specified target-window, moving windows up if necessary, otherwise target-window is the
             new window location.

             If  -d  is given,  the  session  does  not make  the  new  window the  current  window.
             target-window represents  the window  to be  created; if the  target already  exists an
             error  is  shown,  unless  the  -k  flag  is used,  in  which  case  it  is  destroyed.
             shell-command is  the command to  execute. If shell-command  is not spec‐  ified, the
             value of  the default-command  option is  used. -c specifies  the working  directory in
             which the new window is created.

             When the shell  command completes, the window closes. See  the remain-on-exit option to
             change this be‐ haviour.

             The TERM  environment variable  must be  set to “screen”  for all  programs running
             inside  tmux. New  windows will  automatically  have “TERM=screen”  added to  their
             environment, but care must be taken not to reset this in shell start-up files.

             The -P  option prints information about  the new window  after it has been  created. By
             default,  it  uses the  format  ‘#{session_name}:#{window_index}’  but a  different
             format may be specified with -F.


     next-layout [-t target-window]
     nextl

             Move a window to the next layout and rearrange the panes to fit.


     next-window [-a] [-t target-session]
     next

             Move to the next window in the session. If  -a is used, move to the next window with an
             alert.


     pipe-pane [-o] [-t target-pane] [shell-command]
     pipep

             Pipe any output sent by the program in  target-pane to a shell command. A pane may only
             be piped to one command at a time,  any existing pipe is closed before shell-command is
             executed.  The  shell-command  string  may  contain  the  special  character  sequences
             supported by the status-left option. If no shell-command is given, the current pipe (if
             any) is closed.

             The -o option only opens  a new pipe if no previous pipe exists,  allowing a pipe to be
             toggled with a single key, for example:

                   bind-key C-p pipe-pane -o 'cat >>~/output.#I-#P'


     previous-layout [-t target-window]
     prevl

             Move to the previous layout in the session.


     previous-window [-a] [-t target-session]
     prev

             Move to the previous  window in the session. With -a, move to  the previous window with
             an alert.


     rename-window [-t target-window] new-name
     renamew

             Rename the current window, or the window at target-window if specified, to new-name.


     respawn-pane [-k] [-t target-pane] [shell-command]
     respawnp

             Reactivate  a pane  in which  the  command has  exited (see  the remain-on-exit  window
             option). If shell-command is  not given, the command used when the  pane was created is
             executed. The  pane must be  already inactive,  unless -k is  given, in which  case any
             existing command is killed.


     respawn-window [-k] [-t target-window] [shell-command]
     respawnw

             Reactivate a  window in  which the  command has exited  (see the  remain-on-exit window
             option). If shell-command is not given, the command used when the window was created is
             executed. The window  must be already inactive,  unless -k is given, in  which case any
             existing command is killed.


     rotate-window [-DU] [-t target-window]
     rotatew

             Rotate the  positions of the panes  within a window, either  upward (numerically lower)
             with -U or down‐ ward (numerically higher).


     select-layout [-nop] [-t target-window] [layout-name]
     selectl

             Choose a  specific layout for a  window. If layout-name  is not given, the  last preset
             layout used  (if any) is  reapplied. -n  and -p are  equivalent to the  next-layout and
             previous-layout commands. -o  applies the last set layout if  possible (undoes the most
             recent layout change).


     select-window [-lnpT] [-t target-window]
     selectw

             Select the window  at target-window. -l, -n  and -p are equivalent  to the last-window,
             next-window and  previous-window commands. If  -T is given  and the selected  window is
             already the current window, the command behaves like last-window.

     split-window [-bdfhvP] [-c start-directory] [-l size | -p percentage] [-t target-pane] [shell-command]
                  [-F format]
     splitw

             Create  a new  pane by  splitting target-pane:  -h  does a  horizontal split  and -v  a
             vertical split;  if nei‐  ther is  specified, -v is  assumed. The  -l and  -p options
             specify  the size  of the  new pane  in lines  (for vertical  split) or  in cells  (for
             horizontal split), or as a percentage, respectively.  The -b option causes the new pane
             to be  created to the left  of or above target-pane.  The -f option creates  a new pane
             spanning the full  window height (with -h)  or full window width (with  -v), instead of
             splitting  the  active pane.  All  other  options have  the  same  meaning as  for  the
             new-window command.


     swap-pane [-dDU] [-s src-pane] [-t dst-pane]
     swapp

             Swap two  panes. If -U  is used and  no source pane is  specified with -s,  dst-pane is
             swapped with  the previous pane  (before it numerically); -D  swaps with the  next pane
             (after it numerically). -d instructs tmux not to change the active pane.

             If -s is omitted and a marked pane  is present (see select-pane -m), the marked pane is
             used rather than the current pane.


     swap-window [-d] [-s src-window] [-t dst-window]
     swapw

             This is similar to link-window, except  the source and destination windows are swapped.
             It is an error if no window exists at src-window.

             Like swap-pane, if -s is omitted and a marked pane is present (see select-pane -m), the
             window contain‐ ing the marked pane is used rather than the current window.


     unlink-window [-k] [-t target-window]
     unlinkw

             Unlink target-window. Unless -k is given, a window may be unlinked only if it is linked
             to multiple sessions - windows may not be linked to no sessions; if -k is specified and
             the window is linked to only one session, it is unlinked and destroyed.

# Key bindings

    list-keys
    pfx ?

            Liste les raccourcis (q pour quitter).


On peut changer les raccourcis par défaut via les commandes `bind-key` et `unbind-key`.

Les raccourcis par défaut sont les suivants:

           ,    $      renommer la fenêtre / session courante

           C-o         Rotate the panes in the current window forwards.
           C-z         Suspend the tmux client.
           !           Break the current pane out of the window.
           #           List all paste buffers.
           -           Delete the most recently copied buffer of text.
           .           Prompt for an index to move the current window.
           D           Choose a client to detach.
           L           Switch the attached client back to the last session.
           f           Prompt to search for text in open windows.
           i           Display some information about the current window.
           l           Move to the previously selected window.
           n           Change to the next window.
           o           Select the next pane in the current window.
           p           Change to the previous window.
           q           Briefly display pane indexes.
           r           Force redraw of the attached client.
           m           Mark the current pane (see select-pane -m).
           M           Clear the marked pane.
           w           Choose the current window interactively.
           z           Toggle zoom state of the current pane.
           {           Swap the current pane with the previous pane.
           }           Swap the current pane with the next pane.
           Page Up     Enter copy mode and scroll one page up.
           Up, Down
           Left, Right
                       Change to the pane above, below, to the left, or to the right of the current pane.
           M-1 to M-5  Arrange panes in one of the five preset layouts: even-horizontal, even-vertical, main-hori‐
                       zontal, main-vertical, or tiled.
           Space       Arrange the current window in the next preset layout.
           M-n         Move to the next window with an activity marker.
           M-o         Rotate the panes in the current window backwards.
           M-p         Move to the previous window with an activity marker.
           C-Up, C-Down
           C-Left, C-Right
                       Resize the current pane in steps of one cell.
           M-Up, M-Down
           M-Left, M-Right
                       Resize the current pane in steps of five cells.

     tmux allows a command to be bound to most keys, with or without a prefix key.  When specifying keys, most
     represent themselves (for example ‘A’ to ‘Z’).  Ctrl keys may be prefixed with ‘C-’ or ‘^’, and Alt (meta) with
     ‘M-’.  In addition, the following special key names are accepted: Up, Down, Left, Right, BSpace, BTab, DC
     (Delete), End, Enter, Escape, F1 to F12, Home, IC (Insert), NPage/PageDown/PgDn, PPage/PageUp/PgUp, Space, and
     Tab.  Note that to bind the ‘"’ or ‘'’ keys, quotation marks are necessary, for example:

           bind-key '"' split-window
           bind-key "'" new-window

     Commands related to key bindings are as follows:


     bind-key [-nr] [-t mode-table] [-T key-table] key command [arguments]
     bind

             Bind key key to command.  Keys are bound in a key table.  By default (without -T), the key is bound in
             the prefix key table.  This table is used for keys pressed after the prefix key (for example, by
             default ‘c’ is bound to new-window in the prefix table, so ‘C-b c’ creates a new window).  The root ta‐
             ble is used for keys pressed without the prefix key: binding ‘c’ to new-window in the root table (not
             recommended) means a plain ‘c’ will create a new window.  -n is an alias for -T root.  Keys may also be
             bound in custom key tables and the switch-client -T command used to switch to them from a key binding.
             The -r flag indicates this key may repeat, see the repeat-time option.

             If -t is present, key is bound in mode-table.

             To view the default bindings and possible commands, see the list-keys command.


     list-keys [-t mode-table] [-T key-table]
     lsk

             List all key bindings.  Without -T all key tables are printed.  With -T only key-table.

             With -t, the key bindings in mode-table are listed; this may be one of: vi-choice or emacs-choice.


     send-keys [-lMRX] [-N repeat-count] [-t target-pane] key ...
     send

             Send a key or keys to a window.  Each argument key is the name of the key (such as ‘C-a’ or ‘npage’ )
             to send; if the string is not recognised as a key, it is sent as a series of characters.  The -l flag
             disables key name lookup and sends the keys literally.  All arguments are sent sequentially from first
             to last.  The -R flag causes the terminal state to be reset.

             -M passes through a mouse event (only valid if bound to a mouse key binding, see MOUSE SUPPORT).

             -X is used to send a command into copy mode - see the WINDOWS AND PANES section.  -N specifies a repeat
             count.

     send-prefix [-2] [-t target-pane]
             Send the prefix key, or with -2 the secondary prefix key, to a window as if it was pressed.


     unbind-key [-an] [-t mode-table] [-T key-table] key
     unbind

             Unbind the command bound to key.  -n, -T and -t are the same as for bind-key.  If -a is present, all
             key bindings are removed.

# Hooks

tmux permet d'exécuter automatiquement une commande arbitraire lors d'un évènement déterminé.
On parle de ’hook’.

L'évènement surveillé par un hook peut être global ou local à une session.
On ne peut pas exécuter 2 hooks différents surveillant un même évènement, même si l'un d'eux
surveille une version globale de l'évènement tandis que l'autre surveille une version locale.

En cas de conflit, entre 2 looks globaux, le dernier exécuté a la priorité.
Entre un global et un local, le local l'emporte.

Pour chaque commande tmux, il existe un évènement se produisant après chacune de ses exécutions.
Son nom suit le schéma ’after-command’. Ex:

    set-hook after-split-window 'selectl even-vertical'

            Installe un hook qui sélectionne le layout `even-vertical` à chaque fois qu'on exécute
            `split-window`.

            L'évènement utilisé ici est `after-split-window`.


Mais certains des évènements dispo ne sont associés à aucune commande tmux:

    alert-activity
    alert-silence

            Une fenêtre a de l'activité.
            "             été silencieuse pendant la durée indiquée par l'option 'monitor-silence'.


    client-attached
    client-detached
    client-resized

            Un client s'est attaché.
            "               détaché.
            "         est redimensionné.


    client-session-changed

            La session à laquelle un client est attachée a changé.


    pane-exited
    pane-died

            Le pgm à l'intérieur d'un pane s'est terminé.
            Idem, mais l'option 'remain-on-exit' (locale à la fenêtre) est activée, et donc le pane
            ne s'est pas fermé.


    session-closed
    session-created
    session-renamed

            Une session est fermée.
            "               créée.
            "               renommée.


    window-linked
    window-renamed
    window-unlinked

            Une fenêtre est liée à une session.
            "               renommée.
            "               déliée d'une session.


    set-hook                 my_event 'command'
    set-hook -t foobar       my_event 'command'
    set-hook -g              my_event 'command'

             Installe le hook exécutant `command` qd `my_event` se produit au sein de:

                    - la session courante
                    - la session foobar
                    - toutes les sessions


    set-hook -u              my_event 'command'
    set-hook -u -t foobar    my_event 'command'
    set-hook -gu             my_event 'command'

            Désinstalle le hook exécutant `command` qd `my_event` se produit au sein de:

                    - la session courante
                    - la session foobar
                    - toutes les sessions

            Selon que le hook qu'on souhaite désinstaller surveille un évènement global ou local
            à une session, il faut utiliser, ou pas, le flag `-g`.


    show-hooks
    show-hooks -t foobar
    show-hooks -g

            Affiche la liste des hooks installés au sein de:

                   - la session courante
                   - la session foobar
                   - toutes les sessions

# Mouse support

     If the mouse option is  on (the default is off), tmux allows mouse events  to be bound as keys.
     The name of each key is made up of a mouse event (such as ‘MouseUp1’) and a location suffix
     (one of ‘Pane’ for  the contents of a pane, ‘Border’ for a  pane border or ‘Status’
     for the status line). The following mouse events are avail‐ able:

           WheelUp       WheelDown
           MouseDown1    MouseUp1      MouseDrag1   MouseDragEnd1
           MouseDown2    MouseUp2      MouseDrag2   MouseDragEnd2
           MouseDown3    MouseUp3      MouseDrag3   MouseDragEnd3
           DoubleClick1  DoubleClick2  DoubleClick3 WheelUp
           TripleClick1  TripleClick2  TripleClick3 WheelDown

     Each should be suffixed with a location, for example ‘MouseDown1Status’.

     The special  token ‘{mouse}’  or ‘=’  may be  used as  target-window or  target-pane in
     commands bound to  mouse key bindings. It resolves  to the window or pane over  which the mouse
     event took place (for  example, the window in the status line over  which button 1 was released
     for  a ‘MouseUp1Status’  binding, or  the pane  over  which the  wheel was  scrolled for  a
     ‘WheelDownPane’ binding).

     The send-keys -M flag may be used to forward a mouse event to a pane.

     The default key  bindings allow the mouse to be  used to select and resize panes,  to copy text
     and to change win‐ dow using the status line. These take effect if the mouse option is turned
     on.

# Formats

Certaines commandes acceptent l'argument `-F` qui attend comme valeur une chaîne appelée format.
Son rôle est de formater la sortie de la commande.

Au sein d'un format, certaines expressions peuvent être évaluées, si elles sont encadrées par `#{` et `}`:

    #{variable tmux}
    #{option tmux}
    #{?variable tmux,val1,val2}    expression conditionnelle
    #{?option tmux,val1,val2}      "

Quelques exemples d'évaluations:

    #{session_name}
    #S

            Retourne le nom de la session courante.
            La 2e syntaxe illustre que certaines variables tmux disposent d'un alias.


    #{?session_attached,attached,not attached}
    #{?automatic-rename,yes,no}

            Retourne la chaîne 'attached' si la session courante est attachée,        'not attached' autrement.
            Retourne la chaîne 'yes'      si l'option `automatic-rename` est activée, 'no'           autrement.


    #{=5:pane_title}
    #{=-5:pane_title}

            Retourne les 5 premiers/derniers caractères du titre du pane.

            #{=number:expr} est une syntaxe permettant de limiter la longueur de la chaîne résultant
            de l'évaluation d'une expression, aux `number` premiers/derniers caractères, suivant le
            signe de `number`.


    #{t:window_activity}

            Retourne la date et l'heure de la dernière activité de la fenêtre dans un format lisible
            par un humain (!=epoch).

            De base, `window_activity` retourne la date de dernière activité en nb de secondes depuis
            l'epoch. Le préfixe `t:` convertit cette date pour donner qch comme:

                    Sun Oct  25 09:25:02  2015

            La plupart (toutes?) des variables tmux stockant une date, utilisent de base le format epoch.
            `t:` (mnémotechnique: Time) est utile pour les convertir en un format plus lisible.


    #{b:socket_path}
    #{d:socket_path}

            Retourne le fichier/dossier du socket utilisé par le serveur tmux.

            `b:` et `d:` sont des préfixes, utilisant `$ basename` et `$ dirname`, pour extraire
            le nom du fichier/dossier d'un chemin vers un fichier stocké dans une variable tmux.


    #{s/foo/bar/:pane_title}

            Retourne le titre du pane en remplaçant toutes les occurrences de `foo` par `bar`.

            `#{s/pattern/replacement:tmux var/opt}` est une syntaxe permettant de faire des substitutions
            dans une variable/option tmux.


    #(uptime)

            Retourne la sortie de la commande shell `uptime`.

            `#(shell cmd)` est une syntaxe permettant d'évaluer une commande shell.
            Si la sortie contient plusieurs lignes, seule la 1e est retenue.

            Qd tmux doit construire un format incluant une commande shell `#(…)`, il n'attend pas
            qu'elle finisse d'être exécutée.
            Soit il utilise un résultat passé de cette même commande, soit il utilise un placeholder.

            On peut le vérifier en exécutant:

                    set-option -g status-right '#(sleep 1)'

            … qui affiche dans la status line à droite:

                    <'sleep 1' not ready>

            Mais seulement la 1e fois. Si on réexécute la commande, rien n'est affiché.
            En effet, la 1e fois un placeholder est utilisé, et la fois d'après tmux connaissant le
            résultat de `$ sleep` (chaîne vide), il affiche immédiatement une chaîne vide.

            Une commande shell évaluée via `#(…)` est exécutée avec l'environnement global de tmux.


Voici les alias disponibles de variables tmux:

            #D           pane_id            42
            #F           window_flags       # * - M Z ~

            #H           host               ubuntu
            #h           host_short         ubuntu
            #I           window_index       3
            #P           pane_index         3
            #S           session_name       study
            #T           pane_title         ?
            #W           window_name        zsh


Voici les variables tmux qu'on peut évaluer:

    Nom                             Remplacé par

    alternate_on                    0 ou 1 selon que le pane is in alternate screen
    alternate_saved_x               Saved cursor X in alternate screen
    alternate_saved_y               Saved cursor Y in alternate screen

    buffer_name                     nom du buffer
    buffer_sample                   Sample of start of buffer
    buffer_size                     Size of the specified buffer in bytes

    (t:)client_activity             time when client had its last activity
    (t:)client_created              time when client was created
    client_control_mode             1 if client is in control mode
    client_height                   Height of client
    client_key_table                Current key table
    client_last_session             Name of the client's last session
    client_pid                      PID of client process
    client_prefix                   1 if prefix key has been pressed
    client_readonly                 1 if client is readonly
    client_session                  Name of the client's session
    client_termname                 Terminal name of client
    client_tty                      Pseudo terminal of client
    client_utf8                     1 if client supports utf8
    client_width                    Width of client

    command                         Name of command in use, if any
    command_list_name               Command name if listing commands
    command_list_alias              Command alias if listing commands
    command_list_usage              Command usage if listing commands

    cursor_flag                     Pane cursor flag
    cursor_x                        Cursor X position in pane
    cursor_y                        Cursor Y position in pane

    history_bytes                   Number of bytes in window history
    history_limit                   Maximum window history lines
    history_size                    Size of history in bytes

    hook                            Name of running hook, if any
    hook_pane                       ID of pane where hook was run, if any
    hook_session                    ID of session where hook was run, if any
    hook_session_name               Name of session where hook was run, if any
    hook_window                     ID of window where hook was run, if any
    hook_window_name                Name of window where hook was run, if any

    host                            nom d'hôte de la machine (côté serveur?)
                                    Ex: ubuntu

    host_short                      " idem, mais sans nom de domaine

    insert_flag                     Pane insert flag

    keypad_cursor_flag              Pane keypad cursor flag
    keypad_flag                     Pane keypad flag

    line                            Line number in the list

    mouse_any_flag                  Pane mouse any flag
    mouse_button_flag               Pane mouse button flag
    mouse_standard_flag             Pane mouse standard flag

    pane_active                     1 if active pane
    pane_bottom                     Bottom of pane
    pane_current_command            Current command if available
    pane_current_path               Current path if available
    pane_dead                       1 if pane is dead
    pane_dead_status                Exit status of process in dead pane
    pane_height                     Height of pane

    pane_id                         identifiant unique du pane actif (!=index qui est non unique)
                                    L'ID est incrémenté à chaque création d'un nouveau pane.

    pane_in_mode                    If pane is in a mode
    pane_input_off                  If input to pane is disabled
    pane_index                      index du pane courant
    pane_left                       Left of pane
    pane_pid                        PID of first process in pane
    pane_right                      Right of pane
    pane_start_command              Command pane started with
    pane_synchronized               If pane is synchronized
    pane_tabs                       Pane tab positions
    pane_title                      Title of pane
    pane_top                        Top of pane
    pane_tty                        Pseudo terminal of pane
    pane_width                      Width of pane

    pid                             Server PID

    scroll_region_lower             Bottom of scroll region in pane
    scroll_region_upper             Top of scroll region in pane
    scroll_position                 Scroll position in copy mode

    session_alerts                  List of window indexes with alerts
    session_attached                Number of clients session is attached to
    (t:)session_activity            time when session had its last activity
    (t:)session_created             time when session was created
    (t:)session_last_attached       last time when session was attached
    session_group                   Number of session group
    session_grouped                 1 if session in a group
    session_height                  Height of session
    session_id                      Unique session ID
    session_many_attached           1 if multiple clients attached
    session_name                    nom de la session
    session_width                   Width of session
    session_windows                 Number of windows in session

    socket_path                     Server socket path

    (t:)start_time                  time when server started

    (t:)window_activity             time when window had its last activity
    window_activity_flag            1 if window has activity
    window_active                   1 if window active
    window_find_matches             Matched data from the find-window

    window_flags                    flags de la fenêtre:

                                            #    activité détectée
                                            *    fenêtre courante
                                            -    précédente fenêtre
                                            M    la fenêtre contient le pane marqué
                                            Z    le pane actif est zoomé
                                            ~    fenêtre silencieuse plus longtemps que `monitor-silence` s

    window_height                   Height of window
    window_id                       Unique window ID
    window_index                    index de la fenêtre courante
    window_last_flag                1 if window is the last used
    window_layout                   Window layout description, ignoring zoomed window panes
    window_linked                   1 if window is linked across sessions
    window_name                     nom de la fenêtre
    window_panes                    Number of panes in window
    window_silence_flag             1 if window has silence alert
    window_visible_layout           Window layout description, respecting zoomed window panes
    window_width                    Width of window
    window_zoomed_flag              1 if window is zoomed

    wrap_flag                       Pane wrap flag

# Names and Titles

    Les fenêtres et les sessions ont des noms, qui peuvent être utilisés comme identifiant pour
    spécifier une cible dans certaines commandes tmux, ou être affichés dans la status line ainsi
    que diverses listes, tq celle affichée par `choose-window`.

    Seuls les panes ont des titres.
    Par défaut, le titre d'un pane est configuré par le pgm qui y tourne.
    Une fenêtre n'a pas de titre qui lui est propre, elle ne fait qu'hériter de celui de son pane actif.

    On peut modifier le nom d'une session via les commandes `new-session` et `rename-session`.
    Celui d'une fenêtre via:

    1.      A command argument (such as -n for new-window or new-session).

    2.      An escape sequence:

                  $ printf '\ekWINDOW_NAME\e\\'

    3.      Automatic renaming, which sets the name to the active command in the window's active pane.  See the
            automatic-rename option.

    When a pane is first created, its title is the  hostname. A pane's title can be set via the OSC
    title setting sequence, for example:

          $ printf '\e]2;My Title\e\\'

# Environment

    Qd le serveur démarre, tmux copie l'environnement du shell dans son environnement global.
    Chaque session dispose en plus de son propre environnement (via l'option session `update-environment`).
    Qd une fenêtre est créée, l'environnement global et celui de la session sont fusionnés.
    Si une variable existe dans les 2 environnements, celle dans l'environnement de la session a la priorité.


    setenv                   VAR val
    setenv -t target-session VAR val
    setenv -g                VAR val

            Configure la variable d'environnement `VAR` en lui donnant la valeur `val`, au sein de
            l'environnement:

                    - de la session courante
                    - de la session target-session
                    - global

            `setenv` est un alias de `set-environment`.


    setenv -r VAR
    setenv -u VAR

            Supprime la variable d'environnement `VAR` avant de lancer un nouveau processus.
            Supprime `VAR`, inconditionnellement.

            `-r` ne semble pas supprimer `VAR` définitivement, puisqu'on peut toujours la voir via
            `showenv`. Elle est simplement précédée d'un signe `-`.
            La suppression est sans doute locale à un processus.

            Quelle est l'utilité de `-r` par rapport à `-u` ?

            `-u` supprime une variable d'environnement pour tous les processus, ce qui peut-être pose
            pb pour d'éventuels processus préexistants (jobs? reptyr?) qui en avaient besoin.
            `-r` permet de conserver la variable pour les anciens processus, tout en la supprimant
            pour les futurs.


    showenv
    showenv -g
    showenv -t target-session
    showenv -s DISPLAY

            Affiche le contenu de:

                    - l'environnement de la session courante
                    - "               global
                    - "               de la session `target-session`
                    - la variable d'environnement DISPLAY

            `showenv` est un alias de `show-environment`.


            La sortie de `showenv` peut ressembler à ça:

                    DISPLAY=:0.0
                    -SSH_AGENT_PID
                    -SSH_ASKPASS
                    SSH_AUTH_SOCK=/run/user/1000/keyring-IoCmFb/ssh
                    -SSH_CONNECTION
                    -WINDOWID
                    XAUTHORITY=/home/username/.Xauthority

            Dans la sortie, un signe `-` précédant une variable signifie qu'à chaque fois qu'on
            lance un processus, elle est supprimée.
            Mais apparemment, la suppression est locale à un processus, car les variables précédées
            d'un `-` restent dans l'environnement même après avoir fini d'exécuter un processus.

            Dans la commande tmux, le flag `-s` convertit la sortie en une séquence de commandes
            shell permettant de reproduire l'environnement:

                    DISPLAY=":0.0"; export DISPLAY;
                    unset SSH_AGENT_PID;
                    unset SSH_ASKPASS;
                    SSH_AUTH_SOCK="/run/user/1000/keyring-IoCmFb/ssh"; export SSH_AUTH_SOCK;
                    unset SSH_CONNECTION;
                    unset WINDOWID;
                    XAUTHORITY="~/.Xauthority"; export XAUTHORITY;


# Status Line

     tmux includes an optional  status line which is displayed in the bottom  line of each terminal.
     By default, the status line is enabled (it  may be disabled with the status session option) and
     contains, from left-to-right:  the name of the current session in  square brackets; the window
     list; the title of the active pane in double quotes; and the time and date.

     The status line is made of three parts: configurable left and right sections (which may contain
     dynamic  content such  as  the  time or  output  from a  shell  command,  see the  status-left,
     status-left-length, status-right, and status-right-length options  below), and a central window
     list. By  default, the  window list  shows the  index, name and  (if any)  flag of  the windows
     present in  the current session  in ascending  numerical order. It  may be customised  with the
     window-status-format and  window-status-current-format options. The  flag is one of  the fol‐
     lowing symbols appended to the window name:

           Symbol    Meaning

           *         Denotes the current window.
           -         Marks the last window (previously selected).
           #         Window is monitored and activity has been detected.
           ~         The window has been silent for the monitor-silence interval.
           M         The window contains the marked pane.
           Z         The window's active pane is zoomed.

     The #  symbol relates  to the  monitor-activity window option.  The window  name is  printed in
     inverted colours if an alert (activity or silence) is present.

     The colour and  attributes of the status line  may be configured, the entire  status line using
     the status-style  session option  and individual windows  using the  window-status-style window
     option.

     The status line is  automatically refreshed at interval if it has changed,  the interval may be
     controlled with the status-interval session option.

     Commands related to the status line are as follows:


     command-prompt [-1] [-I inputs] [-p prompts] [-t target-client] [template]

             Open the  command prompt  in a client.  This may  be used from  inside tmux  to execute
             commands interactively.

             If  template  is  specified,  it  is  used   as  the  command.  If  present,  -I  is  a
             comma-separated list of the initial text for each  prompt. If -p is given, prompts is a
             comma-separated list of prompts which are displayed in order; otherwise a single prompt
             is displayed, constructed from template if it is present, or ‘:’ if not.

             Before the  command is executed,  the first occurrence of  the string ‘%%’  and all
             occurrences of ‘%1’ are replaced by the  response to the first prompt, all ‘%2’
             are replaced with the response to the second  prompt, and so on for further prompts. Up
             to nine  prompt responses  may be  replaced (‘%1’ to  ‘%9’). ‘%%%’  is like
             ‘%%’ but any quotation marks are escaped.

             -1 makes the  prompt only accept one key  press, in this case the resulting  input is a
             single character.

             Sur la ligne de commande on peut utiliser la plupart des raccourcis readline habituels:

                    - C-a, C-e, C-b, C-f, M-b, M-f    mouvements
                    - C-w, C-u, C-k                   suppression
                    - C-p/Up, C-n/Down, Tab           complétion
                    - C-t                             transposition

            On peut également taper C-y pour insérer le contenu du dernier buffer tmux.


     confirm-before [-p prompt] [-t target-client] command
     confirm

             Ask for confirmation before executing command. If  -p is given, prompt is the prompt to
             display; other‐ wise a prompt is constructed from command. It may contain the special
             character sequences supported by the status-left option.

             This command works only from inside tmux.


     display-message [-p] [-c target-client] [-t target-pane] [message]
     display

             Display a  message. If -p is  given, the output is  printed to stdout, otherwise  it is
             displayed in the target-client  status line. The format of message  is described in the
             FORMATS section;  information is taken from  target-pane if -t is  given, otherwise the
             active pane for the session attached to target-client.

# Buffers

tmux maintains a set  of named paste buffers. Each buffer may be  either explicitly or automatically
named. Explicitly named buffers are named when  created with the set-buffer or load-buffer commands,
or by  renaming an automatically  named buffer with set-buffer  -n. Automatically named  buffers are
given a name such  as ‘buffer0001’, ‘buffer0002’ and so on. When  the buffer-limit option is
reached, the oldest automatically named buffer is  deleted. Explicitly named buffers are not subject
to buffer-limit and may be deleted with delete-buffer command.

Buffers may be added  using copy-mode or the set-buffer and load-buffer commands,  and pasted into a
window using the paste-buffer  command. If a buffer command is used and  no buffer is specified, the
most recently added automatically named buffer is assumed.

A configurable history buffer  is also maintained for each window. By default,  up to 2000 lines are
kept; this can be altered with the history-limit option (see the set-option command above).


     The buffer commands are as follows:


     choose-buffer [-F format] [-t target-window] [template]

             Put a window into buffer choice mode, where a buffer may be chosen interactively from a
             list. After a buffer  is selected, ‘%%’ is replaced by the  buffer name in template
             and the result  executed as a com‐  mand. If template is not  given, "paste-buffer -b
             '%%'" is used.  For the meaning of the  -F flag, see the FORMATS  section. This command
             works only if at least one client is attached.


     clear-history [-t target-pane]
     clearhist

             Remove and free the history for the specified pane.


     delete-buffer [-b buffer-name]
     deleteb

             Delete the  buffer named buffer-name,  or the  most recently added  automatically named
             buffer if not specified.


     list-buffers [-F format]
     lsb

             List the global buffers.  For the meaning of the -F flag, see the FORMATS section.


     load-buffer [-b buffer-name] path
     loadb

             Load the contents of the specified paste buffer from path.


     paste-buffer [-dpr] [-b buffer-name] [-s separator] [-t target-pane]
     pasteb

             Insert the contents of a paste buffer  into the specified pane. If not specified, paste
             into the current one. With -d, also  delete the paste buffer. When output, any linefeed
             (LF) characters in the paste buffer are  replaced with a separator, by default carriage
             return (CR). A custom  separator may be specified using the -s flag.  The -r flag means
             to do  no replacement  (equivalent to  a separator of  LF). If  -p is  specified, paste
             bracket control codes  are inserted around the buffer if  the application has requested
             bracketed paste mode.


     save-buffer [-a] [-b buffer-name] path
     saveb

             Save the  contents of  the specified  paste buffer to  path. The  -a option  appends to
             rather than overwriting the file.


     set-buffer [-a] [-b buffer-name] [-n new-buffer-name] data
     setb

             Set the contents of the specified buffer to  data. The -a option appends to rather than
             overwriting the buffer. The -n option renames the buffer to new-buffer-name.


     show-buffer [-b buffer-name]
     showb

             Display the contents of the specified buffer.

# Miscellaneous

     Miscellaneous commands are as follows:

     if-shell [-bF] [-t target-pane] shell-command command [command]
     if

             Execute  the first  command  if shell-command  returns success  or  the second  command
             otherwise. Before being  executed, shell-command is expanded using  the rules specified
             in the FORMATS section, including those relevant to target-pane. With -b, shell-command
             is run in the background.

             If -F is given,  shell-command is not executed but considered  success if neither empty
             nor zero (after formats are expanded).


     lock-server
     lock

             Lock each  client individually  by running  the command  specified by  the lock-command
             option.


     run-shell [-b] [-t target-pane] shell-command
     run

             Execute  shell-command  in the  background  without  creating  a window.  Before  being
             executed,  shell-command  is  expanded using  the rules  specified  in the  FORMATS
             section. With -b, the  command is run in the background. After  it finishes, any output
             to stdout is displayed in copy mode (in the pane specified by -t or the current pane if
             omitted). If the command doesn't return success, the exit status is also displayed.


     wait-for [-L | -S | -U] channel
     wait

             When used without options, prevents the  client from exiting until woken using wait-for
             -S with the same  channel. When -L is used, the channel is  locked and any clients that
             try to  lock the  same channel  are made  to wait  until the  channel is  unlocked with
             wait-for -U. This command only works from outside tmux.

# Terminfo extensions

     tmux understands some unofficial extensions to terminfo(5):

     Cs, Cr  Set the cursor colour.  The first takes a single string argument and is used to set the colour; the
             second takes no arguments and restores the default cursor colour.  If set, a sequence such as this may
             be used to change the cursor colour from inside tmux:

                   $ printf '\e]12;red\e\\'

     Ss, Se  Set or reset the cursor style.  If set, a sequence such as this may be used to change the cursor to an
             underline:

                   $ printf '\e[4 q'

             If Se is not set, Ss with argument 0 will be used to reset the cursor style instead.

     Tc      Indicate that the terminal supports the ‘direct colour’ RGB escape sequence (for example,
             \e[38;2;255;255;255m).

     Ms      Store the current buffer in the host terminal's selection (clipboard).  See the set-clipboard option
             above and the xterm(1) man page.

# Examples

     To create a new tmux session running vi(1):

           $ tmux new-session vi

     Most commands have a shorter form, known as an alias.  For new-session, this is new:

           $ tmux new vi

     Alternatively, the  shortest unambiguous form  of a command is  accepted. If there  are several
     options, they are listed:

           $ tmux n
           ambiguous command: n, could be: new-session, new-window, next-window

     Within an active session,  a new window may be created by typing  ‘C-b c’ (Ctrl followed by
     the ‘b’ key followed by the ‘c’ key).

     Windows may be navigated with: ‘C-b 0’ (to  select window 0), ‘C-b 1’ (to select window
     1), and so  on; ‘C-b n’ to select the  next window; and ‘C-b p’ to  select the previous
     window.

     A  session  may be  detached  using  ‘C-b  d’ (or  by  an  external  event such  as  ssh(1)
     disconnection) and reattached with:

           $ tmux attach-session

     Typing ‘C-b  ?’ lists the current  key bindings in the  current window; up and  down may be
     used to navigate the list or ‘q’ to exit from it.

     Commands  to be  run  when  the tmux  server  is  started may  be  placed  in the  ~/.tmux.conf
     configuration file. Common examples include:

     Changing the default prefix key:

           set-option -g prefix C-a
           unbind-key C-b
           bind-key C-a send-prefix

     Turning the status line off, or changing its colour:

           set-option -g status off
           set-option -g status-style bg=blue

     Setting other options, such as the default command, or locking after 30 minutes of inactivity:

           set-option -g default-command "exec /bin/ksh"
           set-option -g lock-after-time 1800

     Creating new key bindings:

           bind-key b set-option status
           bind-key / command-prompt "split-window 'exec man %%'"
           bind-key S command-prompt "new-window -n %1 'ssh %1'"

# -----------------------------------------------
https://silly-bytes.blogspot.fr/2016/06/seamlessly-vim-tmux-windowmanager_24.html
-------------------------

### Seamlessly Vim-Tmux-WindowManager-Monitor navigator {#seamlessly-vim-tmux-windowmanager-monitor-navigator .post-title .entry-title itemprop="name"}

[![](https://2.bp.blogspot.com/-84QCH6s2Lto/V21_KZG4X9I/AAAAAAAACv8/2echuUpawm8QJz7XEN-YYb3D-mxG5MWmgCLcB/s640/matrix1.jpg){width="640"
height="265"}](https://2.bp.blogspot.com/-84QCH6s2Lto/V21_KZG4X9I/AAAAAAAACv8/2echuUpawm8QJz7XEN-YYb3D-mxG5MWmgCLcB/s1600/matrix1.jpg)

[This Thoughtbot
post](https://robots.thoughtbot.com/seamlessly-navigate-vim-and-tmux-splits)
describes how to make Vim and Tmux *work together in Harmony* based on
[this crhistoomey
plugin](https://github.com/christoomey/vim-tmux-navigator), allowing you
to traverse both your Vim and Tmux windows and panes respectively.\
\
Having the ability to traverse Vim and Tmux splits without having to
think about it using `ctrl-h`, `ctrl-j`, `ctrl-k`, `ctrl-l` is
fantastic! But I still had an annoyance source from the window manager
(Ratpoison) and the multi monitor setup.\
\
So I took the same concept and extend it to those uses cases, so now I
use `ctrl-h`, `ctrl-j`, `ctrl-k`, `ctrl-l` to move through my **Window
Manager splits**, my **Tmux panes**, my **Vim windows** and my
**Monitors** with minimum mental overhead. Here is how.\
\
Some of the scripts are a bit of complex, so instead of explaining them
in detail the general algorithm is described.\
\
\
[]()\
\
Frame-Monitor Navigation
------------------------

[![](https://1.bp.blogspot.com/-x797hts4bo8/V21_IB-rgnI/AAAAAAAACvw/d0wuO5aeW74reCV71ReJUgPWE4nBMNaAACKgB/s320/matrix2.jpg){width="320"
height="176"}](https://1.bp.blogspot.com/-x797hts4bo8/V21_IB-rgnI/AAAAAAAACvw/d0wuO5aeW74reCV71ReJUgPWE4nBMNaAACKgB/s1600/matrix2.jpg)

When traversing frames (Ratpoison splits) it stops at the end of the
current monitor, so first I needed to change to the left or right
monitor when a movement command is triggered at the edge of the current
one.

The script
[frame-mon\_navigator.sh](https://github.com/alx741/dotfiles/blob/master/scripts/.scripts/ratpoison/frame-mon_navigator.sh)
calculates if the current frame is the rightmost or the leftmost in the
current monitor, if it is, it goes to the next of previous monitor
depending on the movement command.

``` {.sourceCode .sh}
#!/bin/sh

ratpoison -c 'fdump'| sed 's/,/\n/g' | awk '{print $5" "$19}' > /tmp/ratpoison_frame_monitor_navigator

# Calculate X coordinate for rightmost frame
greater_x_coordinate=0
while read frame; do
    coordinate=$(echo "$frame" | cut -d' ' -f1)
    if [[ $coordinate -gt $greater_x_coordinate ]];
    then
        greater_x_coordinate=$coordinate
    fi
done < /tmp/ratpoison_frame_monitor_navigator


# Calculate current frame X coordinate
x_coordinate=$(head -n1 /tmp/ratpoison_frame_monitor_navigator | cut -d' ' -f1)
last_access=$(head -n1 /tmp/ratpoison_frame_monitor_navigator | cut -d' ' -f2)
while read frame; do
    access=$(echo "$frame" | cut -d' ' -f2)
    if [[ $access -gt $last_access ]];
    then
        last_access=$access
        x_coordinate=$(echo "$frame" | cut -d' ' -f1)
    fi
done < /tmp/ratpoison_frame_monitor_navigator

function is_leftmost
{
    if [[ $x_coordinate -eq 0 ]]; then
        return 0
    else
        return 1
    fi
}

function is_rightmost
{
    if [[ $x_coordinate -eq $greater_x_coordinate ]]; then
        return 0
    else
        return 1
    fi
}

# Go to previous screen if currently if leftmost frame
# Go to next screen if currently if rightmost frame
# Execute frame focus otherwise
if [[ "$1" == "left" ]]; then
    if is_leftmost; then
        ratpoison -c 'prevscreen'
    else
        ratpoison -c 'focusleft'
    fi
elif [[ "$1" == "right" ]]; then
    if is_rightmost; then
        ratpoison -c 'nextscreen'
    else
        ratpoison -c 'focusright'
    fi
fi
```

</div>

  {#ratpoison-tmux-navigator}
-

  {#ratpoison-tmux-navigator}
-

Ratpoison-Tmux Navigator
------------------------

[![](https://1.bp.blogspot.com/-RmMyv2IaIVg/V21_Je2MfvI/AAAAAAAACv4/hsWXIBzyhucPpQWQZpzQX-nKFhy9jkZ4gCKgB/s320/matrix3.jpg){width="320"
height="212"}](https://1.bp.blogspot.com/-RmMyv2IaIVg/V21_Je2MfvI/AAAAAAAACv4/hsWXIBzyhucPpQWQZpzQX-nKFhy9jkZ4gCKgB/s1600/matrix3.jpg)

We need a way to pass movement commands to Tmux so Vim-Tmux navigation
works as always, but we also need to pass movement commands from Tmux to
Ratpoison when a movement command is triggered from Tmux edge pane.

The script
[rat\_tmux-navigator.sh](https://github.com/alx741/dotfiles/blob/master/scripts/.scripts/ratpoison/rat_tmux-navigator.sh)
is able to tell if the terminal emulator (Urxvt) is currently focused
and, if so, send the movement commands to Tmux so it can handle panes
traversing as usual. It also define functions that Tmux can use to know
if a edge pane is reached and send the movement commands to Ratpoison
through the **frame-mon\_navigator.sh** script so Frame-Monitor
navigation is included in the process.\

``` {.sourceCode .sh}
#!/bin/bash

if [[ "$1" == "rat" ]]; then
current_window=$(ratpoison -c 'info' | sed 's/(.*).*(\(.*\))/\1/'\
                | tr '[:upper:]' '[:lower:]')

elif [[ "$1" == "tmux" ]];then
    window_bottom=$(tmux list-panes -F "#{window_height}" | head -n1)
    window_right=$(tmux list-panes -F "#{window_width}" | head -n1)
    window_bottom=$(($window_bottom - 1))
    window_right=$(($window_right - 1))
    pane=$(tmux list-panes -F "#{pane_left} #{pane_right} #{pane_top} #{pane_bottom} #{pane_active}" | grep '.* 1$')
    pane_left=$(echo "$pane" | cut -d' ' -f 1)
    pane_right=$(echo "$pane" | cut -d' ' -f 2)
    pane_top=$(echo "$pane" | cut -d' ' -f 3)
    pane_bottom=$(echo "$pane" | cut -d' ' -f 4)
fi

function rat_up
{
    if [[ "$current_window" == "urxvt" ]];
    then
        ratpoison -c 'meta C-k'
    else
        ratpoison -c 'focusup'
    fi
}

function rat_down
{
    if [[ "$current_window" == "urxvt" ]];
    then
        ratpoison -c 'meta C-j'
    else
        ratpoison -c 'focusdown'
    fi
}

function rat_right
{
    if [[ "$current_window" == "urxvt" ]];
    then
        ratpoison -c 'meta C-l'
    else
        ~/.scripts/ratpoison/frame-mon_navigator.sh right
    fi
}

function rat_left
{
    if [[ "$current_window" == "urxvt" ]];
    then
        ratpoison -c 'meta C-h'
    else
        ~/.scripts/ratpoison/frame-mon_navigator.sh left
    fi
}

function tmux_up
{
    if [[ $pane_top  -eq 0 ]];
    then
        ratpoison -c 'focusup'
    else
        tmux select-pane -U
    fi
}

function tmux_down
{
    if [[ $pane_bottom  -eq $window_bottom ]];
    then
        ratpoison -c 'focusdown'
    else
        tmux select-pane -D
    fi
}

function tmux_right
{
    if [[ $pane_right  -eq $window_right ]];
    then
        ~/.scripts/ratpoison/frame-mon_navigator.sh right
    else
        tmux select-pane -R
    fi
}

function tmux_left
{
    if [[ $pane_left  -eq 0 ]];
    then
        ~/.scripts/ratpoison/frame-mon_navigator.sh left
    else
        tmux select-pane -L
    fi
}


if [[ "$1" == "rat" ]];then
    case "$2" in
        'up')
            rat_up
            ;;
        'down')
            rat_down
            ;;
        'right')
            rat_right
            ;;
        'left')
            rat_left
            ;;
    esac

elif [[ "$1" == "tmux" ]];then
    case "$2" in
        'up')
            tmux_up
            ;;
        'down')
            tmux_down
            ;;
        'right')
            tmux_right
            ;;
        'left')
            tmux_left
            ;;
    esac
fi
```

</div>

  {#vim-tmux-navigator}
-

  {#vim-tmux-navigator}
-

Vim-Tmux Navigator
------------------

Modifying Tmux mappings to use above scripts will make it work for
Tmux-Ratpoison traversing but when a Vim instance is on an Tmux edge
pane it will not jump to the appropriate Ratpoison split. To solve it I
forked the `vim-tmux-navigator` project and made the right changes to it
in the [vim-tmux-wm-monitor
branch](https://github.com/alx741/vim-tmux-navigator/tree/vim-tmux-wm-monitor)\
Then using [vim-plug](https://github.com/junegunn/vim-plug) I install it
in my `.vimrc` with:\
    Plug 'alx741/vim-tmux-navigator', { 'branch': 'vim-tmux-wm-monitor' }

  {#mappings}
-

  {#mappings}
-

Mappings
--------

Putting all together requires the appropriate mappings for Ratpoison and
Tmux. Vim is already configured with the forked plugin.\
###   {#ratpoison}

### Ratpoison

These lines on `.ratpoisonrc` will do the top level handling. Take into
account the path to the `rat_tmux-navigator.sh` script.\
    definekey top C-k exec ~/.scripts/ratpoison/rat_tmux-navigator.sh rat up
    definekey top C-j exec ~/.scripts/ratpoison/rat_tmux-navigator.sh rat down
    definekey top C-l exec ~/.scripts/ratpoison/rat_tmux-navigator.sh rat right
    definekey top C-h exec ~/.scripts/ratpoison/rat_tmux-navigator.sh rat left

###   {#tmux}

### Tmux

Finally these lines on `.tmux.conf` are basically modified versions of
the `vim-tmux-navigator` plugin ones.\
    is_vim="ps -o state= -o comm= -t '#{pane_tty}' \
        | grep -iqE '^[^TXZ ]+ +(\\S+\\/)?g?(view|n?vim?x?)(diff)?$'"
    bind-key C-h if-shell "$is_vim" "send-keys C-h"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux left'"
    bind-key C-j if-shell "$is_vim" "send-keys C-j"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux down'"
    bind-key C-k if-shell "$is_vim" "send-keys C-k"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux up'"
    bind-key C-l if-shell "$is_vim" "send-keys C-l"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux right'"
    bind-key -n C-h if-shell "$is_vim" "send-keys C-h"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux left'"
    bind-key -n C-j if-shell "$is_vim" "send-keys C-j"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux down'"
    bind-key -n C-k if-shell "$is_vim" "send-keys C-k"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux up'"
    bind-key -n C-l if-shell "$is_vim" "send-keys C-l"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux right'"
    bind-key h if-shell "$is_vim" "send-keys C-h"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux left'"
    bind-key j if-shell "$is_vim" "send-keys C-j"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux down'"
    bind-key k if-shell "$is_vim" "send-keys C-k"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux up'"
    bind-key l if-shell "$is_vim" "send-keys C-l"  "run '~/.scripts/ratpoison/rat_tmux-navigator.sh tmux right'"

