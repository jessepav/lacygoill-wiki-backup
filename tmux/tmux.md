# How can I make the difference between a tmux server and a tmux client in the output of `$ ps`?

Look at the process state codes.
If you can read `Ss`, it's a server; `S+`, it's a client.

    ┌───┬────────────────────────────────────────────────────────┐
    │ S │ interruptible sleep (waiting for an event to complete) │
    ├───┼────────────────────────────────────────────────────────┤
    │ s │ is a session leader                                    │
    ├───┼────────────────────────────────────────────────────────┤
    │ + │ is in the foreground process group                     │
    └───┴────────────────────────────────────────────────────────┘

See `$ man ps /PROCESS STATE CODES`.

---

Alternatively, look at the terminal to which the processes are attached.
If you can read `?`, it's a server; `pts/123`, it's a client.

##
# Syntax
## What is `info` in `$ tmux info`?  I can't find it in the documentation.

It's an alias for `show-messages -JT`.

    $ tmux show-options -s command-alias
    ...~
    command-alias[3] "info=show-messages -JT"~
    ...~

##
## How does tmux parse a semicolon?

As a command termination (like the shell).

---

From `$ man tmux /COMMANDS`:

> Multiple commands may be specified together as part of a command
> sequence.  Each command should be separated by spaces and a semicolon;
> commands are executed sequentially from left to right and lines ending
> with a backslash continue on to the next line, except when escaped by
> another backslash.  A literal semicolon may be included by escaping it
> with a backslash (for example, when specifying a command sequence to
> bind-key).

### When do I need to escape a semicolon?

When you install a key binding whose rhs contains several commands, separated by
semicolons.

---

If you write:

    bind <key> cmd1 ; cmd2

Tmux will populate its key bindings table with:

    <key> cmd1

Because the semicolon has prematurely terminated `bind`.
Then, tmux will *immediately* run `cmd2`.

### How many backslashes do I need if I install a tmux key binding from the shell?

Three.

    $ tmux bind <key> cmd1 \\\; cmd2
                           ^^^

This  is because  the semicolon  is  also special  for the  shell; the  latter
automatically removes one level of  backslashes; after this removal, tmux will
correctly receive `\;`.

If you only wrote two backslashes, the shell would reduce them into a single one
– passed to tmux – and the remaining semicolon would not be escaped.
So, the shell would try to run `cmd2` itself.

##
# Getting Information
## How to get the name of the outer terminal?

Use the replacement variable `#{client_termname}`:

    $ tmux display -p '#{client_termname}'
                    │
                    └ print output to stdout,
                      instead of the target-client status line

However, be  aware that this  information is  not always reliable,  because many
terminals lie about their identity (they pretend to be xterm-256color).

##
# Options
## What happens if I omit `-g` when I set a session or window option in `~/.tmux.conf`?

Tmux will complain with one of these error messages:

    no current session
    no current window

###
## Why doesn't `$ tmux show-options mouse` show anything?

Because you're asking for the value local to the current session, and there's none.

OTOH, if you ask for the *global* value, you will have an output:

    $ tmux show-options -g mouse
    mouse on~

## What happens if I don't provide a value to `$ tmux set-option <boolean option>`?

The option is toggled between on and off.

    $ tmux set-option -g mouse && tmux show-options -g mouse
    mouse off~

    $ tmux set-option -g mouse && tmux show-options -g mouse
    mouse on~

##
# Buffers
## How to delete a tmux buffer interactively?

   1. run `choose-buffer`
   2. select a tmux buffer
   3. press `d`

For more info, see:

    $ man tmux /choose-buffer

### Several buffers in one keypress?

Tag the buffers you want to delete by  pressing `t` while your cursor is on each
of them, then press `D`.

---

Note the difference between `d` and `D`.
`d` deletes the currently selected buffer.
`D` deletes all the tagged buffers.

### All buffers?

Press `C-t` to tag all buffers, then `D`.

##
# Debugging
## When writing a bug report
### which terminal geometry should I use?

Make sure the terminal has 80 columns, and maybe also 24 lines.

    $ echo $COLUMNS
    80~

    $ echo $LINES
    24~

The goal is to reproduce with a “standard” geometry.
See `:h window-size`:

> If everything fails a default size of 24 lines and 80 columns is assumed.

### why should I reproduce the issue with a binary compiled *without* my custom script?

Your script modifies the tmux version.

When you'll write  your bug report, the log files  may contain information which
look incompatible with your tmux version.

Besides, nicm  may wrongly think  that you're not using  master, and ask  you to
reproduce the issue  on master; this kind of  conversation/misunderstanding is a
waste of time and increases confusion.

#### which related pitfall should I be aware of?

Even if you don't use your script now, you've probably used it recently.
It has modified `configure.ac` to change the version; so, make sure to run
`$ git stash` to undo the modifications.

##
## How to get a backtrace?

Make sure to run `$ ulimit -c unlimited` before reproducing the crash.
After the crash, tmux should have left a core file in the current directory.
You can extract a backtrace from it by running:

    $ gdb -n -ex 'thread apply all bt full' -batch /path/to/tmux /path/to/core >~/backtrace.txt

### It doesn't contain any useful info!

Ok, so you've got sth like this:

    #0  0x0000000000414fe6 in ?? ()
     No symbol table info available.
    #1  0x0000000000410787 in ?? ()
     No symbol table info available.
    #2  0x0000000000000000 in ?? ()
     No symbol table info available.

It's probably  because you didn't use  the same tmux binary  when you reproduced
the crash, and when you run `$ gdb` to extract a backtrace from the core.

Make sure to use the same binary.
That is, do *not* run that:

    $ ./tmux -Ltest -f/dev/null new
      ^^^^^^

    $ gdb -n -ex 'thread apply all bt full' -batch tmux core >backtrace.txt
                                                   ^^^^

In the first command, where you reproduce the crash, you're calling the compiled
binary in the current directory.
While  in  the  second  command,   you're  calling  the  installed  tmux  binary
`/usr/local/bin/tmux`.

Choose one or the other, but don't mix the two.

### ?

I have had a crash where tmux was started with the command `$ tmux`, and yet the
next  command seemed  to  not give  enough information  (“No  symbol table  info
available.”):

    $ gdb -n -ex 'thread apply all bt full' -batch tmux core >backtrace.txt
                                                   ^^^^

I think I fixed the issue by running:

    $ gdb -n -ex 'thread apply all bt full' -batch ~/GitRepos/tmux/tmux core >backtrace.txt
                                                   ^^^^^^^^^^^^^^^^^^^^

The next time tmux crashes, check whether  you need to specify the original path
to the compiled binary in `~/GitRepos/tmux`, when extracting a backtrace.

If we need to do this, then document it.

#### It doesn't help!

Do *not* use your custom script to compile tmux:

    # ✘
    $ sudo ~/bin/upp.sh tmux

Instead, use your zsh snippets (`$ chown`, `$ make`), and `$ git stash`:

    $ sudo chown -R user:user .
    $ git stash
    $ make clean; make distclean; sh autogen.sh && ./configure && make

---

Explanation:

Your custom script  modifies the version of the compiled  binary which I suspect
prevents gdb from working correctly.

    # ✘
    $ sed -i "/AC_INIT/s/\S\+)/${VERSION})/" configure.ac

You  need  to   run  `$  git  stash`  to  restore   `configure.ac`,  before  the
modifications  applied by  `$ sed`,  and then  you need  to compile  manually to
prevent `$ sed` from being recalled.

#### ?

The previous  information may not be  relevant anymore, because, for  now, we've
decided to stop editing the version in our script.

If that's the case, remove the previous question.
Also, see our todo in `~/bin/upp.sh`; the one which deals with the `$ sed` command.

#### ?

Document the  fact that if you  want your backtrace to  contain more information
(less `<optimized out>`), you need to edit the `Makefile.am` file:

    $ sed -i '/AM_CFLAGS/s/-O2/-O0/' Makefile.am
                                 ^
                                 optimization level 0

See `$ man gcc` for more info:

> The output is sensitive to the effects of previous command-line
> options, so for example it is possible to find out which
> optimizations are enabled at -O2 by using:
>
>         -Q -O2 --help=optimizers
>
> Alternatively you can discover which binary optimizations are
> enabled by -O3 by using:
>
>         gcc -c -Q -O3 --help=optimizers > /tmp/O3-opts
>         gcc -c -Q -O2 --help=optimizers > /tmp/O2-opts
>         diff /tmp/O2-opts /tmp/O3-opts | grep enabled

---

Note that if you do, it may have an impact on performance.
Not on memory consumption, nor latency, but on output bandwidth.
You can test the latter, roughly, with these commands:

    $ yes | head -n 1000000 > two_megs.txt
    $ time cat two_megs.txt

##
## Tmux crashes, but it doesn't dump a core file!
### How to get a backtrace?

    $ gdb -q --args ./tmux -Ltest -f/dev/null new
    (gdb) set follow-fork-mode child
    (gdb) run
    # reproduce the crash
    (gdb) set logging on
    (gdb) bt full
    (gdb) quit

The backtrace should be in `gdb.txt`.

#### I can't run any command in the shell.  What I type is not what is written on the command-line!

Maybe something in your zshrc is interfering.
Write `return` at its top.

####
### How to get a trace?

    $ tmux -Ltest kill-server
    $ strace -ttt -ff -ostrace.out tmux -vv -Ltest -f/dev/null new
                        ^^^^^^^^^^
                        output file

<https://github.com/tmux/tmux/blob/master/CONTRIBUTING>
<https://github.com/tmux/tmux/issues/1603#issuecomment-462955045>

##
## Tmux is hanging.  I can't interact with it anymore!

From another terminal, get the pid of the tmux server.
Or, if you can, run this before reproducing the issue:

    $ tmux display -p '#{pid}'

Then, still from another terminal, run:

             make sure it's the same tmux than the one currently hanging
             vvvvvvvvvvvvvvvvvvvvv
    $ gdb -q /path/to/running/tmux PID
    (gdb) set logging on
    (gdb) bt full
    (gdb) quit

The output of `bt full` should be in `gdb.txt`.
Join it to your bug report.

---

See here to learn more about how to make gdb print to a file instead of stdout:
<https://stackoverflow.com/a/5941271/9780968>

##
# Issues
## My `if-shell` and/or `run-shell` tmux command doesn't work!

Remember that tmux runs your shell command via **sh**, not bash:
<https://github.com/tmux/tmux/issues/1603#issuecomment-462955856>

So, do *not* test your command in zsh or bash, but in sh.

---

For example, if you need to toggle  the logging of the tmux server, this command
works in bash/zsh:

    $ kill -s SIGUSR2 $(ps -o ppid= $$)

But in sh, you need to remove the `SIG` prefix:

    $ kill -s USR2 $(ps -o ppid= $$)

<https://unix.stackexchange.com/a/199384/289772>

---

For the same  reason, make sure your  shell command does not  invoke `[[`, which
doesn't exist in sh; instead, use `[` or `test`.

    run '[[ -d $XDG_RUNTIME_DIR/tmux || mkdir $XDG_RUNTIME_DIR/tmux ]]'
         ^^                                                         ^^
         ✘

    run '[ -d $XDG_RUNTIME_DIR/tmux || mkdir $XDG_RUNTIME_DIR/tmux ]'
         ^                                                         ^
         ✔

    run 'test -d $XDG_RUNTIME_DIR/tmux || mkdir $XDG_RUNTIME_DIR/tmux'
         ^^^^
         ✔

### It doesn't help!

Then redirect the standard error of the shell command to a file:

    run-shell 'my buggy command 2>/tmp/debug'
                                ^^^^^^^^^^^^

And read the error message written in the file to get more information.

###
## Weird sequences are printed on the screen intermittently!

Something  is  probably sending  escape  sequences  (CSI,  OSC, ...)  which  the
terminal doesn't understand.

It can  happen when  you re-attach to  a running tmux  session from  a different
terminal than the one where you started it.

For example, atm, we have a Vim plugin – vim-term – which sends `CSI 2 SPC q` to
the terminal right before exiting.
And xfce4-terminal, on Ubuntu 16.04, doesn't support this sequence.

Solution: Close the terminal,  and re-attach from another  one which understands
the sequence.

Alternatively,  make sure  to  close  the program  responsible  for sending  the
problematic sequence; then close the terminal,  which will kill the tmux client,
and restart a new one.
Note that  in the case  of vim-term + xfce4-terminal  + Ubuntu 16.04,  you would
also need to make sure you start Vim from a new shell, so that tmux has a chance
to update `$COLORTERM`.
Indeed, vim-term relies on the latter to detect xfce4-terminal.

---

You can  reproduce an example of  this issue by  running `$ printf '\e[ 2q'` in
xfce4-terminal on Ubuntu 16.04, and waiting.
The issue is fixed in more  recent versions of xfce4-terminal; I can't reproduce
on Ubuntu 18.04 in a VM.

## Tmux is hanging indefinitely after using a process substitution!

So, you've run sth like:

    $ tmux load-buffer <(echo foobar)

Solution: Use `=()` instead of `<()`.

---

Here's what happens.

The shell opens  a file descriptor it  thinks won't be used and  then passes the
path equivalent of that file descriptor to  the client as an argument, which the
client then passes to the server.

But that  file descriptor might  already be  in use in  the server, so  when the
latter opens the fd,  it gets whatever that is, which might  not be suitable for
reading, so it can block or crash or behaves unexpectedly.

It wouldn't be easy to fix  this issue, without also breaking legitimate devices
like `/dev/null` or blacklisting some paths (which will depend on the platform).

For more info:
<https://github.com/tmux/tmux/issues/1755>

## `$ tmux -Ltest` doesn't read `~/.tmux.conf`!

Make sure you don't have a running tmux server listening to the socket `test`:

    $ ps aux | grep tmux | grep test
    user 6771 ... tmux -Ltest -f/dev/null new~
                              ├─────────┘
                              └ your custom config can't be read because of this

If there's one, kill it:

    $ kill -9 6771

---

This issue can happen, even with no  terminal running a tmux client connected to
this `test` socket.

MWE:

    $ xterm
    $ tmux -Ltest -f/dev/null new
    Alt-F4
    $ ps aux | grep tmux | grep test
    user ... tmux -Ltest -f/dev/null new~

Alt-F4 kills the client, but not the server.
The server keeps running in the background.

In contrast, if you  had pressed `C-d` to kill the current  shell, and there was
no other shell handled by the tmux server, this would have killed the latter.

## Some options which set colors don't work!

Do you use hex color codes, and does your terminal support true colors?
If the answers are yes and no, then make sure the following line is not run when
tmux is started from your terminal:

    set -as terminal-overrides ',*-256color:Tc'

Setting `Tc` may prevent other settings to work, like these for example:

    set -gw window-style        'bg=#cacaca'
    set -gw window-active-style 'bg=#dbd6d1'

This issue is specific to terminals which don't support true colors.

Alternatively, you could use:

   - `colour123` instead of `#ab1234`
   - a terminal supporting true colors

---

MWE:

     $ cat <<'EOF' >/tmp/tmux.conf

     set -as terminal-overrides ',*-256color:Tc'
     set -gw window-style         'bg=#000000'
     set -gw window-active-style  'bg=#ffffff'

     set -g prefix 'M-space'
     unbind '"'
     bind _ splitw -v
     bind M-space last-pane
     EOF

     $ tmux -Ltest -f/tmp/tmux.conf

     pfx _
     pfx SPC

##
##
##
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

... then another for the server:

    tmux: server───zsh

Both (chain of) processes are started by:

   - the init process in console:

        systemd

   - the display manager in X:

        systemd───lightdm───lightdm───upstart

You can check this with the following commands:

    $ pstree -ps $(pidof tmux|cut -d' ' -f1)
    $ pstree -ps $(pidof tmux|cut -d' ' -f2)

Note that the  server is started after  the first client, so its  pid is bigger,
which may seem counter-intuitive.
Also, the relationship between the 2 processes is NOT parent-child.
It's client-server.
IOW, they are 2 independent processes.
You won't find both of them listed in the output of the same `$ pstree` command.
They communicate via a socket, which by default is called `default`.
The latter is created in the directory `tmux-{UID}` inside:

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
executing tmux), the tmux client, and the tmux server are all [transparent][1]:
everything in red in the diagram is not visible.

# Démarrage

Voici qques argument qu'on peut passer à Tmux au démarrage.


    tmux command

            Spécifie à Tmux quelle commande exécuter.
            Si aucune commande n'est donnée, Tmux exécute `new-session`.

            Si `command` accepte des flags en argument, on peut les lui passer ici aussi.


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
            │   │       yes the server seems to be started AFTER the first client ...
            │   │
    $ kill -12 {tmux server pid}

            Toggle the  logging of  the activity. However,  when you  enable the
            logging, it seems to only create the `tmux-server-{PID}.log` file.

            Warning:
            The log files  becomes really big, really fast. Enable logging  only for a short
            period of time to debug sth.

##
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

Copy pasting in terminal with vimium/vimperator like hints.

<https://github.com/morantron/tmux-fingers>

### heytmux

Tmux scripting made easy

Heytmux can read STDIN, so:

    $ cat workspace.yml | heytmux

... is also valid. It may seem pointless, but it allows you to do:

    :w !heytmux

... with a visual selection in Vim.

I primarily  use Heytmux  to write Markdown  documents with  fenced code
blocks of YAML snippets that I can easily select and run with Heytmux in
my editor.

<https://github.com/junegunn/heytmux>

##
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

            ... ou peut-être:

                    service procps start

            Cette dernière commande est donnée dans `/etc/sysctl.d/README`.

##
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
                    - bright...
                    - colour0
                    - ...
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

            Elle peut aussi être utilisée dans une séquence de caractères spéciaux (#[...]) au sein
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

##
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

##
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


    copy_Y

            Copie la sélection dans un buffer tmux et la coller automatiquement dans la ligne de
            commande (tmux-yank).

            Attention  à  ne pas  copier  un  caractère  de trop  à  la  fin, autrement  il  sera
            interprété comme  un retour  à la ligne,  ce qui  aura le même  effet que  taper sur
            entrée (du coup, pas le temps de relire la ligne de commande avant de valider).


    pfx y

            Copie la ligne de commande (tmux-yank) dans le buffer système
            et dans un buffer tmux. Fonctionne même si la commande se poursuit sur plusieurs lignes


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

... associe à escape à la sortie du mode copie. Source:

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

##
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

##
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

##
# Raccourcis

    $ man tmux /DEFAULT KEY BINDINGS

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

##
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

##
##
##
# Todo
## links to read

<https://www.reddit.com/r/tmux/comments/5cm2ca/post_you_favourite_tmux_tricks_here/>
<https://raw.githubusercontent.com/tmux/tmux/master/CHANGES>
<https://medium.freecodecamp.org/tmux-in-practice-series-of-posts-ae34f16cfab0>
<https://github.com/samoshkin/tmux-config>
<https://silly-bytes.blogspot.fr/2016/06/seamlessly-vim-tmux-windowmanager_24.html>
<https://github.com/tmux/tmux/blob/master/example_tmux.conf>
<http://man.openbsd.org/OpenBSD-current/man1/tmux.1>
<https://github.com/tmux/tmux/wiki/FAQ>
<https://devel.tech/tips/n/tMuXz2lj/the-power-of-tmux-hooks/>
<https://github.com/tmux-plugins/tmux-sensible>
<https://github.com/tmux-plugins/tmux-pain-control>

extended underline style
<https://github.com/tmux/tmux/commit/bc0e527f32642cc9eb2354d1bdc033ab6beca33b>

support for windows larger than visible on the attached client
<https://github.com/tmux/tmux/commit/646995384d695eed9de1b2363fd2b315ca01785e>

support for overline (SGR 53)
<https://github.com/tmux/tmux/commit/1ee944a19def82cb62abf6ab92c17eb30df77a41>

Style to follow when submitting a PR to tmux:
<https://man.openbsd.org/style.9>
<https://github.com/tmux/tmux/pull/1743#issuecomment-493450917>

## here's a way to programmatically get the PID of a process launched by tmux:

    P=$(tmux new -dP -- mycommand); tmux display -pt$P -F '#{pane_pid}'
                        ^^^^^^^^^
                        arbitrary command started in a new tmux window

## linking windows

Watch this:

    $ tmux linkw -s . -t 0

It creates a window of index 0, which is linked to the current window.
I think the command means: link the current window (`-s .`) to a new window of index 0.
Now, everything you type in one of these 2 windows, is also typed in the other.

It seems that windows can also be linked to sessions.
To understand what it means you'll need to first understand the concept of “session group”.
It's described at `$ man tmux /^\s*new-session [`:

> If -t is given, it specifies a session group.  Sessions in the
> same group share the same set of windows - new windows are linked
> to all sessions in the group and any windows closed removed from
> all sessions.  The current and previous window and any session
> options remain independent and any session in a group may be
> killed without affecting the others.

## evaluating a tmux replacement variable in different contexts

To test the current value of a replacement variable such as `#{pane_tty}`, run:

    # shell command
    $ tmux -S /tmp/tmux-1000/default display -p #{pane_tty}

    # tmux command
    :display -p #{pane_tty}

    # Vim command
    :echo system('tmux -S /tmp/tmux-1000/default display -p "#{pane_tty}"')

## including in the status line the number line where a pattern matches in the current pane

If you  include `#{C:hello}` in your  tmux status line, the  latter will contain
the number line where `hello` appears in the current tmux pane.

From `$ man tmux /FORMATS`:
> A  ‘C’ performs  a search  for an  fnmatch(3) pattern  in the  pane content  and
> evaluates to zero if not found, or a line number if found.

##
## pipe-pane

Document this:

$ tmux pipe-pane -t study:2.1 -I "echo 'ls'"

This command  executes `$  ls` in  the first pane  of the  second window  of the
`study` session; the syntax is the following:

$ tmux pipe-pane -t {session}:{window}.{pane} -I "shell-cmd"

`-I` and `-O` specify which of the shell-command output streams are connected to
the pane.

With `-I`, stdout is connected (so anything `shell-cmd` prints is written to the
pane as if it was typed).

You can also run:

$ tmux pipe-pane -t {session}:{window}.{pane} -O "shell cmd"

With  `-O`,  stdin  is  connected  (so  any output  in  the  pane  is  piped  to
`shell-cmd`); both `-I` and `-O` may be used together.

It could be useful for our re-implementation of `vim-tbone`.

### is `pipe-pane` buggy?

Disable your zshrc (`return` at the top).
Press `pfx :` and run `pipe-pane "exec cat - | ansifilter >>/tmp/log"`.
The last command comes from:
<https://github.com/tmux-plugins/tmux-logging/blob/master/scripts/start_logging.sh#L15>

Now, run some shell commands, like `$ ls`, `$ echo 'hello'`, `$ sudo aptitude update`, ...
The output of `$ echo 'hello'` is *not* logged.  Why?
If you re-enable all our zshrc, it's correctly logged.  Why?
There seems  to be a  regular percent sign  (not the special  one we use  in our
prompt), which is added on a dedicated line after every output.  Why?
Only the first executed command is logged (I'm not talking about the output; the
output is usually logged; I'm talking about the executed line).  Why?

Make some tests, with and without our zshrc.
If `pipe-pane` is buggy, report the bugs.

Once `pipe-pane` is fixed, check out the tmux-logging plugin.
Right now, it seems to suffer from the same issues described above.

Also,  we  have  moved  the  code sourcing  the  zsh  syntax  highlighting  into
`~/.zsh/syntax_highlighting.zsh`.
And we have set a guard to disable the sourcing.
And  we  have created  a  zsh  snippet to  disable  the  sourcing on  demand  in
`~/.config/zsh-snippet/main.txt`.
And we have left a question/answer about it in `~/.config/zsh-snippet/README.md`.
We did all  of this thinking that the syntax  highlighting badly interfered with
tmux-logging.
But was it really the case? Or was it just `pipe-pane` which was broken?
If it was not the case, do we want to undo everything we did?

##
## update tmux cheatsheet to make it include tmux-fingers key bindings

## attach-session

From `$ man tmux /^\s*attach-session`

> If run from outside tmux, create a new client in the current terminal and attach
> it to target-session. If used from inside, switch the current client.

I interpret  the second sentence  as tmux switching  the current session  in the
current client; the equivalent of pressing `pfx )`.
Look  at the  description of  the latter;  they use  the same  terminology (i.e.
“switch”).
And yet, in  practice, `$ tmux attach-session` inside tmux  fails with “sessions
should be nested with care, unset $TMUX to force”.

What gives?

## double a percent sign when running a shell process for your status line

If you run some shell command for include some info in your status line, e.g.:

    #{?#(cmd1),#(cmd2),}

And if the command contains a percent sign, e.g.:

    $ date +%s

I think you need to double the percent:

    $ date +%%s
             ^

That's what nicm seemed to suggest once in the #tmux irc channel.

## by default tmux runs a shell process every 15s for the statusline; use `$ sleep` to change that time

    #(while :; do command; sleep 30; done)

In case you wonder why you need a `while` loop, here's nicm's explanation:

> │  guardian │ I'm not sure I undertand why I need to wrap in a while loop
> │      nicm │ there is no mechanism to make tmux run it at particular times, so you need to run it all
> │           │ the time and just do your stuff every 30 seconds

---

In  case you  wonder where  the 15s  come from,  it's the  default value  of the
session option 'status-interval'.

## conditionals `#{?...}`, and similar constructs (`#{||:...}`, `#{m:...}`, ...) can be nested

For example, this will be replaced by 1 if the version of tmux is strictly lower
than 2.4, 0 otherwise:

    #{||:#{m:[01].*,#{version}},#{m:2.[0123],#{version}}}

<https://github.com/tmux/tmux/issues/1747#issuecomment-494292198>

## prevent some panes from being synchronized

Open the clock in them:

> Not really  the solution,  but any pane  set in a  different mode  (e.g. clock
> mode, copy mode, showing help) will not respond to key strokes.
> If you need all but a couple of panes to synchronize, this works pretty well.

<https://stackoverflow.com/questions/12451951/tmux-synchronize-some-but-not-all-panes#comment19620986_12451951>

## syntax of `confirm-before`

It expects a tmux command as last argument (!= shell command):

    $ tmux confirm-before -p "kill-pane #P? (y/n)" kill-pane

and if the command contains several words, you need to quote it:

    $ tmux confirm-before -p "display a message? (y/n)" "display -p 'hello'"
                                                        ^                  ^

Btw, why does `-p` fail here? `display` should print the message on stdout.

## `respawn-pane` is useful when you have a pane which always runs the same application in the same place

Same thing for `respawn-window`.
Note that for a pane/window to be respawned, the `remain-on-exit` option needs to be on.

It is  useful, because you  don't have to restore  the geometry, and  because it
preserve the scrollback buffer.

<https://unix.stackexchange.com/a/512501/289772>

## document `-e` option of `copy-mode` command

It makes tmux quit copy mode only when you reach the end of the screen with PgDown and WheelDown.
And possibly a few others.
But not when you reach it with `j` or `Down`.

You can make some tests with this minimal tmux.conf:

    set -g mouse on
    bind -n a copy-mode -e

Then press `pfx a`,  followed by PgDown or WheelDown until you  reach the end of
the screen; tmux should quit copy mode.

---

If you're looking for a real usage example, see this key binding installed by default:

    bind WheelUpPane if -F -t = "#{mouse_any_flag}" "send -M" "if -Ft= \"#{pane_in_mode}\" \"send -M\" \"copy-mode -et=\""

If you wonder what the `=` sign means here, it's a special token equivalent to `{mouse}`.
See `$ man tmux /MOUSE SUPPORT /{mouse}`.

##
# Reference

[1]: $MY_WIKI/graph/tmux/transparent.pdf

