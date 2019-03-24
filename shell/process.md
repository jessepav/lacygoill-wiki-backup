# ASSIMIL
## ?

    http://www.linusakesson.net/programming/tty/

## ?

Understand the output of `free -h`:

                       total       used        free      shared  buff/cache   available
        Mem:           3,6G        1,8G        408M        262M        1,4G        1,2G
        Swap:          3,8G         50M        3,8G

`Shared` is an obsolete concept and `total` is easy to understand:

                       used        free    buff/cache   available
        Mem:           1,8G        408M          1,4G        1,2G
        Swap:           50M        3,8G

## ?

https://unix.stackexchange.com/questions/138463/do-parentheses-really-put-the-command-in-a-subshell/138498#comment772229_138498

Why does the manual say "The order  of expansions is:

... parameter and  variable expansion, ..., and command substitution  (done in a
left-to-right fashion); word splitting; and filename expansion." Isn't this kind
of misleading?
I had interpreted the manual to mean $x would be expanded first as it has higher
precedence than command substitution.
But apparently this is not the case, as you correctly point out.

        x=1
        echo $(x=2; echo $x)

Which has the priority: variable expansion or command substitution?

## ?

When  we execute  a job  in a  subshell, it's  automatically re-parented  to the
session leader (upstart atm).

I think it's because, even though there's only one command, the subshell doesn't
`exec()` to start the job (i.e. no optimization).
Instead, it `fork()`, then `execve()`.
Once the job has been started in the sub-sub-shell, the sub-shell dies (why?).
So, the job becomes orphan and is re-parented to the session leader.

MWE:

        $ (sleep 100 &)
        $ pstree -s -p $(pidof sleep)
        systemd(1)───lightdm(980)───lightdm(1086)───upstart(1096)───sleep(8274)~
                                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^

---

How to start a job as a daemon?

Solution 1:
        $ (cmd &)

Solution 2:
        $ cmd &
        $ disown %

I think the first solution is more powerful.
Because the second one doesn't work if the job takes time to be started.

If the job contains several commands:

        $ ({ cmd1; cmd2 ;} &)
        $ pstree -s -p $(pidof sleep)
        systemd(1)───lightdm(980)───lightdm(1086)───upstart(1096)───bash(11880)───sleep(11881)~
                                                                    ^^^^^^^^^^^
                                                                    this time, the subshell doesn't die~

---

Explain why none of these work:

        alias dropbox_restart='killall dropbox; ( "${HOME}/.dropbox-dist/dropboxd" ) &'
        alias dropbox_restart='killall dropbox; { "${HOME}/.dropbox-dist/dropboxd" & ;}'
        alias dropbox_restart='killall dropbox; { "${HOME}/.dropbox-dist/dropboxd" ;} &'

Note that according to [Gilles](https://unix.stackexchange.com/a/88235/289772):

>   Parentheses  create a  subshell whereas  braces  don't, but  this is  irrelevant
>   (except as a micro-optimization in some  shells) since a backgrounded command is
>   in a subshell anyway.

## ?

        $ cat /tmp/sh.sh
            #!/bin/bash
            /tmp/sh1.sh

        $ cat /tmp/sh1.sh
            #!/bin/bash
            sleep

        $ /tmp/sh.sh &

        $ pstree -s -p $(pidof sleep)
        systemd(1)───lightdm(980)───lightdm(1086)───upstart(1096)───tmux: server(2784)───zsh(29746)───sh.sh(32569)───sh1.sh(32+~

If you kill `sh.sh`, you get this new process tree:

        systemd(1)───lightdm(980)───lightdm(1086)───upstart(1096)───sh1.sh(32570)───sleep(32571)

This shows  that when  a process  dies, its child  is re-parented  to init  or a
subreaper (here the session leader upstart).

If you kill `sh1.sh`, you get this new process tree:

        systemd(1)───lightdm(980)───lightdm(1086)───upstart(1096)───sleep(32571)

Again, the orphan (`sleep`) is re-apparented to the session leader.

---

However, if you kill the shell from which the script was started, then `sleep` is killed too.

        $ pstree -s -p $(pidof sleep)
        systemd(1)───lightdm(980)───lightdm(1086)───upstart(1096)───tmux: server(2784)───zsh(29746)───sh.sh(32569)───sh1.sh(32+~
                                                                                         ^^^
        $ kill -1 29746
                │
                └ TERM is not enough

This shows that when you exit a shell, the latter sends SIGHUP to all its children.

---

systemd(1)---lightdm(980)---lightdm(1086)---upstart(1096)---sh(6583)---run-or-raise.sh(6584)---firefox(6586)...
                                                            │          │
                                                            │          └ /bin/bash ~/bin/run-or-raise.sh firefox
                                                            │
                                                            └ sh -c ~/bin/run-or-raise.sh firefox

systemd(1)---lightdm(980)---lightdm(1086)---upstart(1096)---sh(2426)---run-or-raise.sh(2427)---urxvt(2429)-+-urxvt(2430)
                                                            │          │
                                                            │          └ /bin/bash /home/user/bin/run-or-raise.sh urxvt
                                                            │
                                                            └ sh -c ${HOME}/bin/run-or-raise.sh urxvt

---

$ cat /tmp/sh.sh
    mousepad [&]

$ /tmp/sh.sh

        systemd(1)---lightdm(980)---lightdm(1086)---upstart(1096)---mousepad(30648)-+-{dconf worker}(30649)
                                                                                    |-{gdbus}(30651)
                                                                                    `-{gmain}(30650)

## Orphan process

A  process can  be orphaned  unintentionally, such  as when  the parent  process
terminates or crashes.
The  process group  mechanism can  be used  to help  protect against  accidental
orphaning, where in coordination with the user's shell will try to terminate all
the child processes with the "hangup"  signal (SIGHUP), rather than letting them
continue to run as orphans.
More precisely, as part of job control,  when the shell exits, because it is the
"session  leader" (its  session id  equals  its process  id), the  corresponding
login  session ends,  and  the shell  sends  SIGHUP to  all  its jobs  (internal
representation of process groups).

It is sometimes desirable to intentionally  orphan a process, usually to allow a
long-running job  to complete  without further  user attention,  or to  start an
indefinitely running service or agent.
Such  processes   (without  an  associated   session)  are  known   as  daemons,
particularly if they are indefinitely running.
A  low-level approach  is to  fork  twice, running  the desired  process in  the
grandchild, and immediately terminating the child.
The grandchild process  is now orphaned, and is not  adopted by its grandparent,
but rather by init.
In any event, the session id (process  id of the session leader, the shell) does
not change,  and the process id  of the session that  has ended is still  in use
until all orphaned processes either terminate  or change session id (by starting
a new session via setsid(2)).

To  simplify system  administration,  it is  often desirable  to  use a  service
wrapper so that processes not designed  to be used as services respond correctly
to system signals.
An alternative  to keep  processes running  without orphaning them  is to  use a
terminal multiplexer and  run the processes in a detached  session (or a session
that becomes detached), so the session is  not terminated and the process is not
orphaned.

A server process is also said to  be orphaned when the client that initiated the
request unexpectedly crashes  after making the request while  leaving the server
process running.

These  orphaned processes  waste server  resources and  can potentially  leave a
server starved for resources.
However, there are several solutions to the orphan process problem:

    - Extermination is the  most commonly used technique; in this  case the
      orphan is killed.

    - Reincarnation is  a technique in  which machines periodically try  to
      locate the parents  of any remote  computations; at which point  orphaned
      processes are killed.

    - Expiration is a technique where each process is allotted a certain amount
      of time to finish before being killed. If need be a  process may "ask" for
      more time to  finish before the allotted time expires.

## Zombie process

A zombie  process or defunct process  is a process that  has completed execution
(via the exit system call) but still has  an entry in the process table: it is a
process in the "Terminated state".
This occurs for  child processes, where the  entry is still needed  to allow the
parent process to read its child's exit status: once the exit status is read via
the wait system call,  the zombie's entry is removed from  the process table and
it is said to be "reaped".
A child  process always  first becomes  a zombie before  being removed  from the
resource table.
In most cases,  under normal system operation zombies are  immediately waited on
by their parent and then reaped by  the system – processes that stay zombies for
a long time are generally an error and cause a resource leak.

The term zombie process derives from the common definition of zombie — an undead
person.
In  the term's  metaphor, the  child process  has "died"  but has  not yet  been
"reaped".
Also,  unlike normal  processes, the  kill  command has  no effect  on a  zombie
process.

Zombie processes should not be confused with orphan processes: an orphan process
is a process that is still executing, but whose parent has died.
These do not remain as zombie  processes; instead, (like all orphaned processes)
they are adopted by init (process ID 1), which waits on its children.
The result is that a process that is  both a zombie and an orphan will be reaped
automatically.

When a process ends via exit, all of the memory and resources associated with it
are deallocated so they can be used by other processes.
However, the process's entry in the process table remains.
The parent can read  the child's exit status by executing  the wait system call,
whereupon the zombie is removed.
The wait call may be executed in sequential code, but it is commonly executed in
a handler for the SIGCHLD signal, which the parent receives whenever a child has
died.

After  the zombie  is removed,  its process  identifier (PID)  and entry  in the
process table can then be reused.
However, if a parent fails to call wait,  the zombie will be left in the process
table, causing a resource leak.
In some situations this may be desirable – the parent process wishes to continue
holding this resource – for example  if the parent creates another child process
it ensures that it will not be allocated the same PID.
On  modern UNIX-like  systems  (that  comply with  SUSv3  specification in  this
respect), the following  special case applies: if the  parent explicitly ignores
SIGCHLD  by setting  its handler  to SIG_IGN  (rather than  simply ignoring  the
signal  by default)  or has  the SA_NOCLDWAIT  flag set,  all child  exit status
information will be discarded and no zombie processes will be left.

Zombies can be identified in the output from the Unix ps command by the presence
of a "Z" in the "STAT" column.
Zombies that exist for more than a short period of time typically indicate a bug
in the parent  program, or just an  uncommon decision to not  reap children (see
example).
If the parent program is no  longer running, zombie processes typically indicate
a bug in the operating system.
As with other resource leaks, the presence  of a few zombies is not worrisome in
itself, but may indicate a problem that would grow serious under heavier loads.
Since there is no memory allocated to  zombie processes – the only system memory
usage is  for the  process table entry  itself – the  primary concern  with many
zombies is not  running out of memory,  but rather running out  of process table
entries, concretely process ID numbers.

To remove zombies  from a system, the  SIGCHLD signal can be sent  to the parent
manually, using the kill command.
If the parent process still refuses to reap  the zombie, and if it would be fine
to terminate  the parent  process, the  next step  can be  to remove  the parent
process.
When a process loses its parent, init becomes its new parent.
init periodically executes the wait system call to reap any zombies with init as
parent.

## ps

        ps -p 42 -o ppid
                  │
                  └ user-defined format

Affiche le PPID (Parent PID) du processus dont le PID est 42, avec une en-tête.
L'en-tête est une ligne affichant un intitulé pour chaque colonne d'info, ex:

        PPID COMMAND

`-o` est  une option  qu'on peut  passer à  `ps` pour  spécifier le  format dans
lequel on veut qu'il affiche les infos.

Ça peut servir à:

        - choisir les infos qui nous intéresse
        - renommer l'intitulé d'une colonne d'info donnée
        - changer sa largeur

Elle accepte comme valeur une liste de mots-clés séparés par des virgules.
Les  mots-clés  utilisables  sont  décrits  dans  la  section  “STANDARD  FORMAT
SPECIFIERS“ de la page man de `ps`.
Parmi eux, on trouve:

        ┌─────────┬──────────────────────────────────────────────────────────────────┐
        │ %cpu    │ consommation cpu     du processus                                │
        │ %mem    │ "            mémoire "                                           │
        ├─────────┼──────────────────────────────────────────────────────────────────┤
        │ cmd     │ commande complète (avec ses arguments) exécutée par le processus │
        │         │ (synonymes: args, command)                                       │
        │         │                                                                  │
        │ comm    │ nom de l'exécutable                                              │
        ├─────────┼──────────────────────────────────────────────────────────────────┤
        │ pid     │ pid du processus                                                 │
        │ ppid    │ pid du parent                                                    │
        ├─────────┼──────────────────────────────────────────────────────────────────┤
        │ ruser   │ proprio du processus                                             │
        └─────────┴──────────────────────────────────────────────────────────────────┘


        1. ps -p 42 -o ppid=
        2. ps -p 42 -o ppid:13
        3. ps -p 42 -o ppid:13=

1. Idem, sauf que cette fois, l'intitulé de la colonne des PIDs est vide grâce
   à l'opérateur `=` qui, ici, est utilisé pour lui affecter une valeur vide.

2. La largeur de la colonne des PIDs est configurée comme étant 13.

3. Idem, et son intitulé est vide.

Si tous  les intitulés de colonne  sont supprimés (en leur  affectant une valeur
nulle via `=`), alors la ligne d'en-tête est elle-même supprimée.

---

        ps -p 42 -o args:13,ppid

Affiche le PPID et la commande complète du processus de PID 42.
La largeur de la colonne consacrée à la commande est configurée comme étant 13.

---

        ps -o pid,ruser=RealUser -o comm=Command

Affiche le pid, l'utilisateur, et le nom de commande des processus.
L'intitulé de la colonne utilisateur est changé en ’RealUser’.

La sortie de:

        ps -o pid=X,comm=Y

... peut être une colonne nommée 'X,comm=Y' ou 2 colonnes nommées 'X' et 'Y'.
Ça dépend de la “personnalité“ de `ps` configurable via `$PS_PERSONALITY`.

Dans le doute, utiliser plusieurs options `-o`.

## apport

        https://stackoverflow.com/q/2065912/8243465

Question intéressante:
        core dumped - but core file is not in current directory?

---

        /proc/sys/kernel/core_pattern

Par défaut, un  fichier “core dump“ est  nommé 'core', mais ce  peut être changé
via un template défini dans `/proc/sys/kernel/core_pattern`.
Atm, le mien contient:

            |/usr/share/apport/apport %p %s %c %P

Ici, le 1er caractère est un pipe.
Ça indique  au kernel qu'il ne  doit pas écrire  le “core dump“ dans  un fichier
mais sur l'entrée standard du programme `apport`.


Les items  `%` sont des  spécificateurs automatiquement remplacés  par certaines
valeurs.
Pour plus d'infos lire `man core`.


`apport` vérifie que le  binaire fait partie d'un paquet, et si  c'est le cas il
génère un rapport qu'il envoit à un bug tracker.

Si le binaire  ne fait pas partie  d'un paquet (pex compilé  en local), `apport`
simule  ce que  le kernel  aurait fait,  à savoir  écrire le  core dump  dans un
fichier  du  CWD  (variable  d'environnement  `Current  Working  Directory`)  du
processus.

Si un utilisateur  a besoin du fichier  core pour générer un  backtrace, il faut
distinguer 3 cas de figure:

        - le binaire fait partie d'un paquet:

                `apport` a généré un rapport dans `/var/crash`

        - le binaire ne fait pas partie d'un paquet, et la taille
          max d'un fichier core est limitée à 0 blocks (limite par
          défaut; vérifiable via `ulimit -a | grep core`):

                il n'y a pas de fichier core

        - le binaire ne fait pas partie d'un paquet, et la taille
          max d'un fichier core n'est pas limitée (ou a une limite
          suffisamment élevée; `ulimit -c unlimited`):

                `apport`  a  écrit le  core  dump  dans  un  fichier du  CWD  du
                processus qui a crashé


        /var/crash

En cas  de crash  d'un binaire  faisant partie d'un  paquet, `apport`  génère un
rapport dans un fichier de ce dossier.
Pex, s'il s'agit de Vim, il l'écrira dans:

        /var/crash/_usr_bin_vim.gtk.1000.crash
                                    │
                                    └ User ID de l'utilisateur au nom duquel tourne le processus?

Ce rapport contient différentes informations, entre autres un backtrace.
Ce dernier n'est sans doute pas très utile  si le binaire qui a crashé ne génère
pas d'infos de déboguage.


        /var/log/apport.log.1

Fichier dans lequel le système logue l'activité de `apport`.

Utile qd  on ne  trouve pas où  `apport` a  écrit le core  dump d'un  binaire ne
faisant pas partie d'un paquet.

## Daemon

A daemon is a program that runs as a background process, rather than being under
the direct control of an interactive user.
Traditionally,  the  process names  of  a  daemon end  with  the  letter d,  for
clarification that  the process  is in  fact a  daemon, and  for differentiation
between a daemon and a normal computer program.
For example, syslogd is the daemon  that implements the system logging facility,
and sshd is a daemon that serves incoming SSH connections.

The parent process of a daemon is often, but not always, the init process.
A daemon is usually either created by a process forking a child process and then
immediately exiting,  thus causing init  to adopt the  child process, or  by the
init process directly launching the daemon.
In addition,  a daemon launched  by forking  and exiting typically  must perform
other operations, such as dissociating the process from any controlling terminal
(tty).
Such procedures  are often implemented  in various convenience routines  such as
daemon(3).

Systems often start daemons at boot time which will respond to network requests,
hardware activity, or other programs by performing some task.
Daemons such as cron may also perform defined tasks at scheduled times.

The term  is inspired from  Maxwell's demon, an  imaginary being from  a thought
experiment that constantly works in the background, sorting molecules.
Unix systems inherited this terminology.
Maxwell's Demon is consistent with  Greek mythology's interpretation of a daemon
as  a supernatural  being working  in the  background, with  no particular  bias
towards good or evil.

After  the  term  was  adopted  for  computer use,  it  was  rationalized  as  a
"backronym" for Disk And Execution MONitor.

Daemons which connect to a computer network are examples of network services.

In a  strictly technical sense,  a process is a  daemon when its  parent process
terminates and the daemon is assigned the init process as its parent process and
has no controlling terminal.
However, more generally a daemon may  be any background process, whether a child
of the init process or not.

The common method for a process to  become a daemon, when the process is started
from the  command-line  or from a  startup script  such as an  init script  or a
SystemStarter script, involves:

    - Optionally removing unnecessary variables from environment.

    - Executing as a background task by  forking and exiting (in the parent
      "half" of the fork). This  allows daemon's  parent (shell  or  startup
      process)  to receive  exit notification and continue its normal execution.

    - Dissociating from  the controlling tty

    - Creating a new session  and becoming the session leader of that session.

    - Becoming a process group leader.
      These  three  steps  are  usually  accomplished  by  a  single  operation,
      setsid().

    - If  the daemon  wants  to  ensure that  it  won't  acquire a  new
      controlling  tty even  by  accident  (which happens  when  a session
      leader without a controlling tty opens a free tty), it may fork and exit
      again. This means  that it is no  longer a session  leader in the new
      session, and can't acquire a controlling tty.

    - Setting the root directory (/) as  the current working directory so that
      the process does  not keep any directory  in use that  may be on
      a  mounted file system (allowing it to be unmounted).

    - Changing the umask to 0 to allow open(), creat(), and other operating
      system calls to provide their  own permission masks and not to  depend on
      the umask of the caller

    - Closing all inherited files  at the time of execution that are left open
      by the  parent process, including file descriptors 0,  1 and 2 for the
      standard streams (stdin, stdout and stderr). Required files will be opened
      later.

    - Using a logfile, the console, or /dev/null as stdin, stdout, and stderr

If the process is  started by a super-server daemon, such  as inetd, launchd, or
systemd, the  super-server daemon will  perform those functions for  the process
(except for old-style  daemons not converted to run under  systemd and specified
as Type=forking and "multi-threaded" datagram servers under inetd).

## gdb

        ┌ commande intégrée au shell; man bash pour plus d'infos
        │
        ulimit -a

Afficher toutes les  limites imposées aux ressources dispo pour  le shell et les
processus qu'il lance.


        ulimit -c unlimited

Débloquer  la  taille  maximale  d'un  fichier core  créé  lors  du  crash  d'un
programme.

Cette commande  doit être  exécutée dans  un shell  interactif depuis  lequel on
tente de reproduire le crash d'un programme.
En effet, par  défaut, la limite est  0, ce qui signifie  qu'aucun fichier n'est
créé.

Si aucun  fichier `core`  n'est créé à  l'issu du crash,  reproduit le  crash en
ayant lancé le processus via `sudo`.

Et lit le contenu de `/var/log/apport.log`.
Il se peut qu'il contienne un message d'erreur expliquant pourquoi le `core` n'a
pas été dumpé, ou bien il peut fournir le chemin vers lequel il a été dumpé.


             ┌ quiet: pas de messages d'intro / copyright
             │
        gdb -q build/bin/nvim core
               └─────────────────┤
                                 └ Lance le  binaire nvim  en spécifiant  un fichier
                                   `core` pour analyser un précédent crash.

                ┌ exécute automatiquement la commande GDB qui suit (ici `bt`)
                │
        gdb -q -ex bt build/bin/nvim core
                   │
                   └ affiche le backtrace de  toutes les stack frames (taper `help
                     bt` dans gdb pour + d'infos)

                                   ┌ appliquer  la commande qui suit  (ici `bt`) à
                                   │ tous les threads neovim est multi-thread
                    ┌──────────────┤
        gdb -q -ex 'thread apply all bt full' build/bin/nvim core
                                        │
                                        └ qualificateur qui demande à afficher les
                                          valeurs des variables locales


             ┌ n'exécute aucune commande d'un fichier d'initialisation `.gdbinit`
             │
        gdb -n -ex 'thread apply all bt full' -batch nvim core >backtrace.txt
                                               │
                                               └ mode batch (!= interactif):
                                                      exécute les commandes demandées et affiche leur sortie
                                                      dans le terminal
                                                 -batch implique `-q`


Générer un backtrace à partir d'un fichier “core dump“.

Qd un  processus reçoit certains  signaux, il crashe  et génère un  fichier core
dump contenant une image de sa mémoire actuelle.
Cette image peut être utilisée par un debugger tq `gdb` pour inspecter l'état du
programme au moment où il s'est terminé.


Si le  crash concerne un  binaire compilé mais  non installé, il  faut remplacer
`nvim` par le chemin vers le binaire, typiquement:

        ./build/bin/nvim


La version `Release` ne génère pas d'informations de déboguage.
En  cas   de  crash,  il  vaut   donc  mieux  le  reproduire   avec  la  version
`RelWithDebInfo` et s'assurer  que la commande `gdb` invoque  bien cette version
de nvim.


Une frame est un ensemble de données associées à un appel de fonction.
Elle contient:

        - les arguments passés à la fonction

        - ses variables locales

        - son adresse d'exécution (≈ à quelle ligne de la fonction l'exécution
          se trouve ?)

On parle  de “stack frame“, car  une fonction peut  en appeler une autre,  et le
processus peut se  répéter, formant ainsi une pile sur  laquelle s'ajoute chaque
nouvelle frame.
La frame  associée à  la fonction où  l'exécution se trouve,  est dite  “la plus
profonde“ (innermost).

Ce qui caractérise une stack n'est pas son implémentation (liste ou autre), mais
son interface: on ne peut que “push“ ou “pop“ un item sur la stack.

        https://en.wikipedia.org/wiki/Stack_(abstract_data_type)#Implementation

##
##
##
# How to kill the process responsible for a GUI window, without knowing its pid?

        $ xkill
        # hover your cursor on the window
        # left-click on it

The only thing that `xkill` does, is to close the connection to the X server.
There's no  guarantee that the application  will abort nicely, or  even abort at
all.
Many existing applications do indeed abort when their connection to the X server
is closed, but some can choose to continue.

##
##
##
# In htop, how to...
## follow the selected process?

Press `F`.

This is useful when the position of the process constantly changes, and you need
to interact with it.

## filter the processes to keep only the ones containing 'pat' in their name?

Press:

        \
        pat
        Enter

## How to undo the filtering?

        \
        C-h ...
        Enter

## toggle the tree view?

Press `t`.

## expand/collapse a node in the tree?

Press `-` / `+`.

## toggle the full program paths?

Press `p`.

## toggle the process threads?

Press `H`.

## toggle the kernel threads?

Press `K`.

## list the files opened for a process?

Select the process and press `l`.

## trace the system calls of a process?

Select the process and press `s`.

##
## sort the processes by memory consumption?

Press `M`.

### by cpu consumption?

Press `P`.

### by time?

Press `T`.

## choose the column to base the sorting on interactively?

Press `F6`.

## reverse the order of the sorting?

Press `I` (think “inverse”).

##
## move the position of uptime?

Press:

        1. S       (to configure htop)
        2. arrows  (to select 'uptime')
        3. Enter
        4. arrows  (to move it)

If, after pressing Enter, you decide to cancel the operation, re-press Enter.

## remove uptime?

Press:

        1. S
        2. arrows to select 'uptime'
        3. Del

##
##
##
# How to get the environment of the Vim process?  (2)

        $ cat /proc/$(pidof vim)/environ | tr '\0' '\n'

Note that this shows the environment as it was when the process was spawned.
Any change the process might have made to its environment won't be visible:

        https://serverfault.com/a/79463

---

Alternatively, start `htop`, select the Vim process, and press `e`.

# How to get the list of processes whose name is 'firefox'?

        $ pidof firefox

# How to get the list of processes whose name matches the regex `fire*`?

        $ pgrep 'fire*'

# How to get the chain of processes from systemd down to the Vim process?

        $ pstree -s $(pgrep vim)
                  │
                  └ show parent processes of the specified process

##
##
##
# Concepts
## Session
### What's a login session?

The period of activity between a user logging in and logging out of the system.

### How is it implemented when there's no graphical user interface?

With a  kernel session: a  collection of process  groups with the  logout action
managed by a session leader.

### How is it implemented when an X display manager is used (like lightdm)?

With the lifetime of a designated user process that the display manager invokes.

### In a kernel session, what is the session leader?

A  process which  interacts with  the controlling  terminal to  ensure that  all
programs are terminated when a user “hangs up” the terminal connection.

On our machine, atm, it seems the session leader is `upstart`:

        $ pstree -s -p $(pgrep upstart | head -n1)
        systemd(1)---lightdm(980)---lightdm(1086)---upstart(1096)...~
                                                                 │~
                      all the programs we start during a session ┘~
                      are children of this `upstart` process~

If the  session leader  is absent,  the processes  in the  terminal's foreground
process group are expected to handle hangups.

### When does a session end?

When the user logs out or exits their interactive shell.

### What happens then?

It terminates the session leader process.
The shell  process then  sends SIGHUP  to all  jobs, and  waits for  the process
groups to end before terminating itself.

###
## Process group
### What's a process group?

A collection of one or more related processes.

Any shell command starts a process group of one or several processes.
There  may be  several because  the  command may  be  a compound  command, or  a
pipeline.
Besides a process may spawn child processes.

### What is it used for?

It is used to send a signal to several related processes simultaneously.

### What's the purpose of the foreground process group of a terminal?

It determines  what processes may  perform I/O to and  from the terminal  at any
given time.

It's  also the  process  group to  which  the tty  device  driver sends  signals
generated by keyboard interrupts, notably C-c, C-z and C-\.

### Who sets it?

The shell.

It partitions  the command pipelines that  it executes into process  groups, and
sets  what process  group is  the foreground  process group  of its  controlling
terminal.

###
## Special processes
### How do you name a process which has started (directly or indirectly) another process?

An ancestor process.

### How do you name a process which has been started (directly or indirectly) by another process?

A descendant process.

###
### What's an orphan process?

A process whose parent has finished or been terminated, but is still running.

### What does “re-parenting” mean?

An operation  performed automatically by  the kernel, which consists  in setting
the parent of an orphan process to init (or a subreaper).

The term can be used in a sentence like so:

        The orphan process has been re-parented to the init process.
                                    ^^^^^^^^^^^ ^^

### What's a subreaper process?

A subreaper fulfills the role of init for its descendant processes.
Upon termination of a  process that is orphan and marked  as having a subreaper,
the nearest  ancestor subreaper will receive  SIGCHLD and be able  to wait(2) on
the orphan to discover its termination status.

For more info, see:

        $ man 2 prctl

        https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ebec18a6d3aa1e7d84aab16225e87fd25170ec2b

###
### What does it mean for a parent process to wait(2) on a child?

It means that the parent calls the  system call `wait()` to get information when
the state of one of its child changes.

A state change is considered to be:

        - the child terminated
        - the child was stopped by a signal
        - the child was resumed by a signal

For more info, see:

        $ man 2 wait

### Why is it important to do so?

When a  child terminates,  performing a  wait allows the  system to  release the
resources associated with it.

### What happens to a terminated child which is not waited on?

It remains in a zombie state.

##
# ps
## Where does the name of the `$ ps` command come from?

Process Status

## How to print information about the processes whose pid are 1, 2 and 3?

        ps -p 1 2 3
            │
            └ pidlist (long form = `--pid`)

## What do the numbers in the TIME column mean?

They stand for how much cpu time the processes have consumed thus far.
They do NOT stand for how long the processes have been running.

## How to limit the output of `$ ps` to the 10 most memory-consuming processes?

        $ ps aux --sort -rss | head -n11
                        │
                        └ print the processes in a DEcreasing order

                          by default, or with a `+` sign, the processes would be
                          displayed in an INcreasing order

##
# Signals
## Where can I find more info about the different signals that I can send to a process?

        $ man 7 signal
        /Standard signals

## What does it mean for a process to “catch” a signal?

It  means  that the  process  has  registered a  signal  handler  which will  be
automatically invoked when the signal is received.
This handler will determine the behavior of the process, which may be completely
different than the default behavior of the process if the signal was not caught.

###
## When does a process receive SIGWINCH?

When the size of the terminal window has changed.

## When does a process receive SIGCHLD?

When one of its children has stopped or died.

## When does a process receive SIGPIPE?

When a process tries to write to a pipe while the reading end has been closed.

The idea is that if you run `foo | bar` and `bar` exits, `foo` gets killed by a
SIGPIPE.

It doesn't necessarily raise an error in the shell.
It does only if the signal handler for SIGPIPE has been set to SIG_IGN (ignore):

        https://unix.stackexchange.com/a/482254/289772

##
## What's the number of the default signal sent by `$ kill` to a process?  What's its name?

        15

        SIGTERM
           ^^^^
           TERMination

## What are the numbers of the 2 other signals I can send to kill a process?  Their names?

        1
        SIGHUP
           ^^^
           HangUP detected on controlling terminal or death of controlling process

        9
        SIGKILL

## Which signal is the most effective?  Least effective?

        SIGKILL > SIGHUP > SIGTERM
        9       > 1      > 15

##
## What happens when a process tries to read from the terminal or write to it, outside the foreground process group?

The tty device driver sends to it the SIGTTIN and SIGTTOU signals.
Unless caught, these signals make the process stop.

Shells often  override the  default stop  action of  SIGTTOU so  that background
processes deliver their output to the controlling terminal by default.

###
## What's the name of the signal generated by C-c?

        SIGINT

## What happens when I press C-c?

The SIGINT signal is sent to the foreground process group.
By default, SIGINT makes processes go back to the main loop.

## What's the name of the signal generated by C-\?

        SIGQUIT

## What happens when I press C-\?

The SIGQUIT signal is sent to the foreground process group.
By default, SIGQUIT makes processes quit immediately.

## What's the name of the signal generated by C-z?

        SIGTSTP

## What happens when I press C-z?

The SIGTSTP signal is sent to the foreground process group.
By default, SIGTSTP makes processes stop, and control is returned to the shell.

##
## Which signals can I use to suspend a job?  What's the difference between them?

        ┌──────────┬───────────────┐
        │ name     │ kill argument │
        ├──────────┼───────────────┤
        │ SIGTSTP  │ -TSTP         │  * Typing SToPped
        ├──────────┼───────────────┤
        │ SIGTSTOP │ -STOP         │
        └──────────┴───────────────┘

SIGTSTP allows the process  to suspend gracefully (i.e. it can  use some time to
organize itself), and can be caught or ignored.

SIGSTOP forces  the process  to suspend  immediately, can't  be caught,  and may
leave the process in an unstable state.

## Which signal can I use to resume a suspended job in the background?

        ┌─────────┬───────────────┐
        │ name    │ kill argument │
        ├─────────┼───────────────┤
        │ SIGCONT │ -CONT         │
        └─────────┴───────────────┘

##
## How to get the list of all possible signal names?

        $ kill -l

## How to get the number of the signal INT?

        $ kill -l INT

## How to get the name of the signal 8?

        $ kill -l 8

## How to get the name of the signal which has terminated or stopped my process?

        $ kill -l <exit status>

Example:

        $ sleep

        C-c
        the exit status is 130~

        $ kill -l 130
        INT~

## How to know which signals a given process block/ignore/catch?

        $ cat /proc/PID/status | grep -E '^Sig(Blk|Ign|Cgt):'
                                               │   │   │
                                               │   │   └ caught signals
                                               │   └ ignored signals
                                               └ blocked signals

The right numbers are bitmasks written in hexadecimal.
To understand their meaning, you must convert them in binary:

        $ echo 'ibase=16;obase=2;ABC123' | bc
        101010111100000100100011~

The INDEX of each non-zero bit stands for the number of a signal.

So, for example, if you have this bitmask:

        SigCgt: 00000000280b2603

It can be converted in binary, and interpreted like so:

        SigCgt: 101010111100000100100011
                                  │   ││
                                  │   │└ the signal 1 is caught (SIGHUP)
                                  │   └ the signal 2 is caught (SIGINT)
                                  └ the signal 6 is caught (SIGUSR1)
                ...


To  automate the  binary  conversion and  interpretation, we  have  a script  in
`~/bin/how_do_you_handle_signals.sh`.
To use it, invoke it  on the command-line and pass it the pid  of a process as a
parameter:

        $ how_do_you_handle_signals.sh $(pidof vim)

For more info, see:

        https://unix.stackexchange.com/a/85365/289772

##
## How to change the character which I have to send to interrupt a process (by default C-c)?

        $ stty intr '^k'
                      │
                      └ case insensitive

Technically,  this command  tells the  terminal device  that the  character that
causes a SIGINT to be sent to the foreground job is `C-k`.

## How to tell the terminal device to never send any signal?

        $ stty -isig

##
## How to suspend the current job, which runs in the background, with `$ kill`?  Without `$ kill`?

With `$ kill`:

        $ kill -TSTP %
or:
        $ kill -STOP %

---

Without `$ kill`:

        $ fg
        C-z

## What should I do before suspending a GUI program with `$ kill` or `C-z`?

Minimize it.
Otherwise its frozen window will take valuable space on your desktop, and you'll
get confused if you try to interact with it (because it won't respond).

##
## How to send SIGKILL to the processes whose pid are 123 and 456, in a single command?

        $ kill -KILL 123 456

## How to send SIGKILL to the jobs whose jobspec are %1, %2 and %3, in a single command?

        $ kill -KILL %1 %2 %3

##
# Debugging
## What does `$ strace` do?

It runs the specified command until it exits, and intercepts the system calls of
the process started by the command, as well as the signals which are received by
the latter.

## How is it useful?

Since  system calls  and  signals  are events  that  happen  at the  user/kernel
interface, a close examination of this boundary is very useful for:

   - bug isolation
   - sanity checking
   - capture race conditions

It's also useful  to solve an issue with  a program for which the  source is not
readily available, since you don't need to recompile it in order to trace it.

##
## Where is the output of `$ strace` written?

By default, on standard error.
But with the `-o` option, you can redirect it into a file.

## What does `123` mean in `system_call(args) = 123`?

It's the return value of the system call.

##
## How to start Vim, and trace all its system calls and received signals?

        $ strace -o log vim
                 ├────┘
                 └ write the output in the `log` file

---

This kind of command is especially useful with small processes, such as `localectl`:

        $ strace -o log localectl list-keymaps

Because the log will be short, and it will be easy to find the cause of an issue.
It's less useful with big processes such as Vim or zsh, but you can still try...

## How to trace an existing Vim process?

        $ strace -o log -p $(pidof vim)
                        ^^^^^^^^^^^^^^^
        $ less +F log

##
## How to trace a process AND all its children?

        $ strace -o log -f firefox
                        ^^

Warning: This can create big files.

## How to log the system calls of each process in a dedicated file?

        $ strace -o log -ff firefox
                        ^^^
                        each process's trace is written to `log.<pid>`
                        where pid is the pid of the process

##
## How to make `$ strace` add an absolute timestamp before each system call?

        $ strace -o log -t vim
                        ^^

## How about a relative timestamp?

        $ strace -o log -r vim
                        ^^

##
## How to trace only the system calls accessing files?

        $ strace -o log -e trace=file vim
                        ^^^^^^^^^^^^^

Useful when a  program fails because it can't find/read  its configuration file,
but doesn't tell you where it's supposed to be.

## How to trace only the system call `open()`?

        $ strace -o log -e trace=open vim
                        ^^^^^^^^^^^^^

## How to trace only the system calls `open()` and `read()`?

        $ strace -o log -e trace=open,read vim
                        ^^^^^^^^^^^^^^^^^^

##
## How to get statistics about the system calls (time, count, number of errors...)?

        $ strace -o log -c vim
                        ^^

##
## The maximum size of printed strings is 32 bytes!  How to get longer strings?

        $ strace -o log -s64 vim
                        ├──┘
                        └ truncate long strings after 64 bytes, instead of 32

This is  especially useful for  `write()` system  calls, because they  may write
long strings of text in files.

Note that filenames are not considered strings and are always printed in full.

##
# Issues
## My process is taking too much time!

        $ strace -o log -r <cmd>
        $ sort log >sorted_log

The lines at the bottoom should match the slowest system calls.
Try to understand why they take so much time...

## I know that my command opens the file 'foo'.  But `$ strace -o log -e trace=open cmd` can't find it!

The process may use another similar system call:

        - openat
        - creat

See `$ man 2 open`.

So, to be more thorough, you should execute:

        $ strace -o log -e trace=open,openat,creat cmd
                                 ^^^^^^^^^^^^^^^^^

It's also possible that the process started by your command spawns child processes.
And maybe it's one of them which opens 'foo'.
So, to be even more thorough, you can execute:

        $ strace -o log -e trace=open,openat,creat -f cmd
                                                   ^^

