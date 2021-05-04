# How to get the version of the distro I'm using?

    $ cat /etc/issue

# How to get its codename?

    $ lsb_release -sc

##
# How to rename the machine?

    $ sudoedit /etc/hosts /etc/hostname

    :argdo %s/old_name/new_name/gc | update

    $ sudo systemctl reboot

For more info, see: <https://askubuntu.com/questions/9540/how-do-i-change-the-computer-name/9614>

# How to reboot the machine?  How to turn it off?

    $ shutdown -r
    $ shutdown {-H|-P}

##
# How to list the groups installed on the system?

    $ getent group
      │
      └ get entries from databases supported by the Name Service Switch libraries

##
# How to prepare a chroot environment?

    $ sudo -i
    $ cd /
    $ mount -t ext4 /dev/sda1 /mnt
    $ mount -t proc proc /mnt/proc
    $ mount -t sysfs sys /mnt/sys
    $ mount -o bind /dev /mnt/dev
    $ chroot /mnt /bin/bash

    # do your stuff

    $ exit
    $ umount /mnt/{proc,sys,dev}
    $ umount /mnt

I tested it on a virtual machine, and it seemed to work.
But this is a minimal procedure, you may need to execute more commands depending
on what you want to do in the chroot environment.
For more info, see: <https://superuser.com/a/111215/913143>

---

When you're finished, and you need to unmount the partitions, do it from outside
the chroot environment, for example directly from /.

---

In a chroot environment, systemctl commands will refuse to perform any action.
That's because the systemd process and the  user that used the chroot command do
not have the same view of the filesystem.

##
# How to get all the names of the kernel parameters?

    $ sysctl -a

# How to get the names of the kernel parameters matching a regex?

    $ sysctl -a -r 'regex'

# How to get the path to a file in `/proc` where the value of the parameter `foo.bar.baz` is stored?

    /proc/sys/foo/bar/baz

Example:

    $ sysctl -a -r 'max_dgram_qlen'
    net.unix.max_dgram_qlen = 512~

    $ cat /proc/sys/net/unix/max_dgram_qlen
    512~

# Where are the kernel parameters configured?

    /etc/sysctl.conf
    /etc/sysctl.d/*

Note that `/etc/sysctl.d/99-sysctl.conf` is a symlink to `/etc/sysctl.conf`.

# How to change a kernel parameter
## at run time?  (2)

    $ sudo sysctl -w <parameter>=<value>
    $ echo 'value' | sudo tee /proc/sys/path/to/parameter

## at boot time?

    $ echo 'parameter=value' | sudo tee -a /etc/sysctl.conf

##
# Grub
## How to configure grub?

Edit its configuration file:

    /etc/default/grub

Then, execute `update-grub(8)`.

## Where can I find the documentation to configure grub?

    :tab new | .!info -f grub -n 'Simple configuration'

## How to make grub remember the entry I've selected the last time I was in its menu?

Make sure these options are enabled in grub's config file:

    # The default menu entry will be the one saved by 'GRUB_SAVEDEFAULT'.
    GRUB_DEFAULT=saved

    # When an entry is  selected, save it as a new default  entry for use by
    # future runs of GRUB.
    GRUB_SAVEDEFAULT=true

## How to make grub's menu wait 2 seconds before automatically selecting an entry?

    GRUB_TIMEOUT=2

## How to remove the splash screen so that I can see the kernel messages when the system boots?

    $ sudoedit /etc/default/grub

    :s/GRUB_CMDLINE_LINUX_DEFAULT="\zsquiet splash\ze"//c

    $ sudo update-grub

Don't use `update-grub2`, it's just a symlink to `update-grub`.

Actually,  the fact  that  it's  a symlink  doesn't  necessarily  mean that  the
commands are equivalent, because the executable program could look at how it was
invoked, but that's not the case here.

<https://askubuntu.com/a/167768/867754>

##
##
# Package management
## How to mark a package so that `aptitude` doesn't update it?  How to undo it?

    $ aptitude hold package
    $ aptitude unhold package

## How to get the limit date beyond which my packages won't be supported anymore?

    $ ubuntu-support-status

For more info:

    $ ubuntu-support-status --show-supported
    $ ubuntu-support-status --show-unsupported

## How to get the list of files installed by a package which I haven't installed yet?

If the package is already on your machine:

    $ dpkg -c /path/to/package.deb
            │
            └ --contents (list contents of archive)

Otherwise:

    $ apt-file list package

Or:

                ┌ --download-only (just download it, don't install it)
                │
    $ aptitude -d install package
    $ cd /var/cache/apt/archives/
    $ dpkg -c package.deb

##
# Appearance
## Where to get information about XFCE?

- <https://docs.xfce.org/start>
- <https://wiki.xfce.org/faq>

## How to change the cursor theme?

See `~/.icons/README.md`.

## How to have pretty icons (paper icons, flat-design)?

    # go to https://snwh.org/paper/download

    # dl the package `paper-icon-theme_XXX.deb`

    # install the package
    $ sudo dpkg -i paper*.deb

    # optional; may be necessary to install missing dependencies
    sudo apt-get install -f

## How to have a pretty theme?

Install `arc-theme`:

    $ git clone https://github.com/horst3180/arc-theme
    $ sudo aptitude install autoconf automake pkg-config libgtk-3-dev gnome-themes-standard gtk2-engines-murrine
    $ ./autogen.sh --prefix=/usr
    $ sudo make install

Once installed, the theme is in `/usr/share/themes/`.

---

Alternatively, you can install it from a repo or grab a binary package from here:
<https://software.opensuse.org/download.html?project=home%3AHorst3180&package=arc-theme>

## Which GUI program can help me configure everything related to the appearance of XFCE (theme, icons, cursor...)?

    $ lxappearance

## How to get borderless windows?

    # Source: https://www.youtube.com/watch?v=U-2KPrzIwao
    $ cd /usr/share/themes/Kokodi/
    $ mkdir xfwm4_backup
    $ mv xfwm4/* xfwm4_backup
    $ cp xfwm4_backup/themerc xfwm4

    Settings
      > Window Manager
      > Style
      > Select 'Kokodi'

## How to import the config of xfce4-terminal from another machine (for the color palette)?

Copy this file from the old machine to the new one:

    ~/.config/xfce4/terminal/terminalrc

Source: <https://askubuntu.com/a/676452/867754>

##
# Issues
## I'm trying to use a documented feature of a command.  It doesn't work at all! It's missing!

Try to recompile  and look for a configuration option  which enables the desired
feature.

## Some configuration for a program I use seems to be ignored!

Maybe something alters your configuration after the file has been processed:

   - delay the processing of the file (`sleep 1s`)
   - move the line(s) at the end of the file

---

Maybe your program has cached its config, and use the latter which is stale.
Remove the cache (e.g. `rm ~/.zcompdump`).

## How to get rid of “Error retrieving accessibility bus address: org.freedesktop.DBus.Error.ServiceUnknown:”?

Install the deb package `at-spi2-core`.

For more info, maybe have a look at this: <https://unix.stackexchange.com/a/148779/289772>

## divers

    Restaurer les consoles tty1-6:    sudoedit /etc/default/grub
                                      décommenter la (les?) ligne `GRUB_TERMINAL=console`
                                      sudo update-grub

            Si aucune console n'est accessible (`C-M-F1..6`), il se peut que la cause soit la résolution
            de la console configurée au démarrage qui n'est pas supportée par la carte/processeur graphique.

            La solution consiste à décommenter une ligne dans le fichier de conf de grub.
            Ceci a également pour effet de donner une faible résolution au menu de grub.
            Plus moche, mais plus lisible car la taille des caractères est bien plus grande.

            Source:
            https://askubuntu.com/questions/162535/why-does-switching-to-the-tty-give-me-a-blank-screen

                    This is usually caused because the graphical text-mode resolution set at boot up
                    is  not compatible  with your  video card.  The solution  is to  switch to  true
                    text-mode by configuring Grub appropriately.


    (II) AIGLX: Suspending AIGLX clients for VT switch
    (II) AIGLX: Resuming AIGLX clients after VT switch
    (II) intel(0): switch to mode 1920x1080@60.0 on VGA1 using pipe 0, position (0, 0), rotation normal, reflection none

            Atm, on a un bug qui fait que lorsqu'on tape C-M-F1 pour se loguer à
            une console,  puis C-M-F7  pour revenir à  l'environnement graphique
            (sans même s'être logué), Xorg consomme 25% du cpu pendant plusieurs
            minutes.

            De plus, il semble qu'il défait notre config xmodmap.
            Enfin, `xdotool` et/ou `wmctrl` ne semblent plus fonctionner pendant
            plusieurs  minutes, car  les raccourcis  qui utilisent  notre script
            `run-or-raise` ne produisent leur effet que bien plus tard.

            Les   3  lignes   écrites   plus  haut   ont   été  copiées   depuis
            `/var/log/Xorg.0.log`.
            Elles correspondent à ce que rapporte  Xorg après qu'on ait tenté de
            se loguer en console.

            Pour chercher une solution, se rendre sur askubuntu.com, et chercher
            les questions taguées par `Xorg`, et contenant le mot-clé AIGLX.

            Voir aussi ce thread:
            https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=541388

            Faire une recherche google avec ces mots-clés:
            xorg console xmodmap aiglx


                                               NOTE:

            Si on commente `~/.Xmodmap`, le pb semble persister mais ne dure que 20s.


                                               NOTE:

            Au démarrage,  Xorg semble consommer  bcp de cpu, et  les raccourcis
            utilisant run-or-raise mettent toujours du temps à répondre, mais ça
            dure pas longtemps.

##
# Todo
## fix bugs where panel and desktop are absent at login

Actually, it seems the  panel is there, but as soon as we  press `M-j` to open a
terminal, it disappears.
Update: and now it's there again...

For the desktop, you may need to run `xfdesktop(1)`.
For the panely, you may try `$ xfce4-panel -r`.

## I have to give my password twice in 2 different screens when I resume a session after suspending the OS!

Google “suspend linux password twice”:

- <https://askubuntu.com/questions/639014/another-password-prompt-when-waking-from-suspend>
- <https://bugs.launchpad.net/bugs/1296270>
- <https://bugs.launchpad.net/bugs/1631715>

For the moment, I tried to fix the issue by running:

    $ light-locker-settings

Then disabling “Lock on suspend”.

---

IMO, this bug illustrates the benefits of using a custom and minimalist DE.
When  you'll build  your own  DE, you  probably won't  install the  light-locker
package; maybe just the xscreensaver package.

See also: <https://askubuntu.com/questions/1063481/lightlocker-and-xscreensaver-conflicting>

---

Note that light-locker seems to have 2 purposes:

   - it can blank the screen after a certain amount of time (screensaver)
   - it can lock the session after a certain amount of time or when you suspend (session-locker)

---

You can configure xscreensaver by running `xscreensaver-demo(1)`.

---

We can configure xscreensaver so that it  asks for our password after the screen
gets blank and a certain amount of additional time has elapsed.
But how  to configure linux so  that it asks for  our password when we  resume a
session (after suspending it)?
We can configure light-locker to do so, but I don't want to rely on this package
because it's tied to  an existing DE (xfce/lxde), and because  it seems to cause
the issue currently discussed (double password).

## Document when `$ aptitude dist-upgrade` is useful.

When you run `$ aptitude [safe-]upgrade` and you can see on the last line of the
output that some packages were not upgraded:

    0 upgraded, 0 newly installed, 0 to remove and 4 not upgraded.~

`$ aptitude dist-upgrade` should upgrade them.

See here for an explanation:
<https://debian-administration.org/article/69/Some_upgrades_show_packages_being_kept_back>

## Document why `xsel(1x)` is better than `xclip(1)`.

`xclip(1)` doesn't close its stdout.

This can make tmux unresponsive:

- <https://askubuntu.com/a/898094/867754>
- <https://wiki.archlinux.org/index.php/Tmux#X_clipboard_integration>
- <https://unix.stackexchange.com/questions/15715/getting-tmux-to-copy-a-buffer-to-the-clipboard/15716#comment349384_16405>

The archwiki link suggests to close it manually with `>/dev/null`.
It may be a known issue: <https://github.com/astrand/xclip/issues/20>

---

Closing xclip's stdout doesn't fix another issue where the `xclip(1)` process is
automatically terminated when we start it from Vim and quit the latter:

<https://unix.stackexchange.com/q/523255/289772>

See our comments inside `tmux#capturePane#main()`:

    ~/.vim/pack/mine/opt/tmux/autoload/tmux/capturePane.vim

## Document `realpath(1)`

`realpath` permet de  fournir le chemin absolu d'un dossier  ou un fichier, même
si c'est un lien symbolique.

    $ ln -s path/to path/destination

    lns() {
       # Usage: lns path/to path/destination
       ln -sv $(realpath $1) $(realpath $2)
    }

## Document how to handle PPAs

    $ sudo add-apt-repository          ppa:jonathonf/vim
    $ sudo add-apt-repository --remove ppa:jonathonf/vim
    $ sudo ppa-purge ppa:jonathonf/vim

Ajoute/Supprime le PPA `ppa:jonathonf/vim` à la liste de ses dépôts.

En cas de suppression via `add-apt-repository`, penser à purger au préalable les
paquets installés depuis le PPA.
Autrement, utiliser `ppa-purge` (nécessite l'installation du paquet éponyme).

---

    $ apt-key list | grep expired
    $ sudo apt-key adv --recv-keys --keyserver <keyserver url> <10-char key ID>

Afficher les clés signant des dépôts installés ayant expirées.

Mettre à jour la clé d'identifiant <10-char key ID>.
Ne fonctionne que si le mainteneur du dépôt a uploadé une nouvelle clé.

Source: <https://serverfault.com/a/615362>

                                     TODO:

Maybe we should update the keys in `up`.


                                     FIXME:

Comment savoir quel serveur de clés utiliser ?

`<keyserver url>` peut être:

   - keys.gnupg.net
   - keyserver.ubuntu.com
   - ... (autres possible ?)

---

    synaptic
    onglet 'Origin'
    tri par 'State'

            Trouver les paquets installés depuis un ppa donné.

## ?

    https://unix.stackexchange.com/questions/484434/sync-a-folder-between-2-computers-with-a-filesystem-watcher-so-that-each-time-a

            Sync a folder between 2 computers, with a filesystem watcher so that
            each time a file is modified, it is immediately replicated


    https://notmuchmail.org/


    https://0x0.st/
    https://github.com/lachs0r/0x0

            No-bullshit file hosting and URL shortening service
            Read the contents of the first link to understand how to use the command.

            Some examples to upload:

                    # a local file
                    curl -F'file=@yourfile.png' https://0x0.st

                    # a remote url
                    curl -F'url=http://example.com/image.jpg' https://0x0.st

                    # a remote url
                    curl -F'shorten=http://example.com/some/long/url' https://0x0.st

                    # output of a shell command
                    command | curl -F'file=@-' https://0x0.st

            We've implemented  a `:Share` command in  `vim-unix` which leverages
            this web service.
            Select  some  text,  and  execute  `:'<,'>Share`,  or  just  execute
            `:Share` while in a file.
            Try it out!


    https://superuser.com/a/602298

            Is there colorizer utility that can take command output and colorize
            it accordingly to pre-defined scheme?

            Also, see this:
            https://github.com/garabik/grc

            See also `ccze(1)`:

                $ aptitude install ccze
                $ cat /var/log/boot.log | ccze -A


    https://beyondgrep.com/feature-comparison/
    https://rentes.github.io/unix/utilities/2015/07/27/moreutils-package/

            À lire.


    https://www.youtube.com/watch?v=wBp0Rb-ZJak

            The Complete Linux Course: Beginner to Power User!


    https://www.gnu.org/software/coreutils/manual/html_node/Directory-Setuid-and-Setgid.html

            27.5 Directories and the Set-User-ID and Set-Group-ID Bits


    https://github.com/jhawthorn/fzy

            Alternative to fzf.

    https://github.com/sharkdp/fd
    https://mike.place/2017/fzf-fd/

            Alternative to `find(1)`.


- <https://www.reddit.com/r/linux/comments/21rm3o/what_is_a_useful_linux_tool_that_you_use_that/>
- <https://www.reddit.com/r/linux/comments/mi80x/give_me_that_one_command_you_wish_you_knew_years/>
- <https://www.reddit.com/r/linux/comments/389mnk/what_are_your_favourite_not_well_known_cli/>

---

What is a bitmask and a mask?
<https://stackoverflow.com/a/31576303>

---

Lire toute la documentation de:

   - fasd
   - fzf
   - ifne
   - ranger
   - rofi
   - strace
   - xsel (`xsel <file`:  écrit file dans le presse-papier)
   - utilitaires fournis par le paquet moreutils

---

<https://github.com/peco/peco>

Alternative à fzf:

   - a l'air plus configurable
   - plus puissant au niveau des regex
   - moins de documentation? less battery included? moins bonne synergie avec Vim?

---

<https://www.booleanworld.com/guide-linux-top-command/>
Guide pour la commande `top`.


`fasd` semble être un simple fichier shell avec peu de code (533 sloc):
<https://github.com/clvv/fasd/blob/master/fasd>

Il y a très peu d'activité sur le projet, et le dernier commit remonte à 5 ans.

Le réimplémenter pour pouvoir facilement continuer son développement par la suite?

##
## Utilities

### Links

    https://github.com/learnbyexample/Command-line-text-processing

            From finding text to search and replace, from sorting to beautifying text and more


    https://aptitude.alioth.debian.org/doc/en/ch02s04s03.html

            Manuel aptitude.  Intéressant pour apprendre à affiner nos recherches de paquets.


    https://github.com/gotbletu/dotfiles

            Dotfiles de Gotbletu.
            La page README est intéressante car Gotbletu y mentionne les principaux programmes qu'il utilise.
            Elle mentionne aussi comment il restaure la configuration des ses programmes.


    https://www.reddit.com/r/commandline/comments/6hnygr/going_full_command_line_what_are_some_underrated/

            Reddit thread titled:
            Going full command-line.  What are some underrated yet extremely useful Terminal packages?

    https://inconsolation.wordpress.com/index/
    https://inconsolation.wordpress.com/index-l-z/

            Blog reviewing obscure and underrated terminal packages.


    https://kmandla.wordpress.com/software/

            K.Mandla's blog of Linux experiences

### atool

`atool` est un outil permettant de manipuler divers types d'archives, via une syntaxe cohérente.
Il s'agit d'un wrapper autour des commandes:

   - acat
   - adiff
   - als
   - apack
   - arepack
   - aunpack

Ces commandes dépendent  elles-mêmes de programmes tiers,  dont certains peuvent
ne pas être installés par défaut.
Pex, pour .rar, il faut installer le paquet `rar`.
Sans lui, on aura un message d'erreur contenant:

    Can't exec "rar": No such file or directory at /usr/bin/atool line 1869.

`atool` est configuré par `/etc/atool[.conf]` et `~/.atoolrc`. `:Man atool` pour plus d'infos.

Un des avantages de `atool` est la création automatique d'un sous-dossier qd on décompresse une archive
contenant plusieurs fichiers.


    ┌──────────────────────────────────────────┬───────────────────────────────────────────────────────────┐
    │ atool -a arc.zip  f1 f2 f3               │ créer une archive à partir de fichiers                    │
    │                                          │                                                           │
    │                                          │     -a = --add                                            │
    ├──────────────────────────────────────────┼───────────────────────────────────────────────────────────┤
    │ atool -cp arc.zip  path/to/file          │ affiche le contenu du fichier `file`                      │
    │                                          │ contenu dans l'archive `arc.zip` dans le pager par défaut │
    │                                          │                                                           │
    │                                          │     -c = --ca t                                           │
    │                                          │                                                           │
    │ atool -c  arc.zip  path/to/file  | vipe  │ idem mais dans l'éditeur par défaut                       │
    │                                          │                                                           │
    ├──────────────────────────────────────────┼───────────────────────────────────────────────────────────┤
    │ atool -d  rc1.tar.gz arc2.tar.gz | vipe  │ lire les différences de contenu entre 2 archives          │
    ├──────────────────────────────────────────┼───────────────────────────────────────────────────────────┤
    │ atool -l     arc.rar                     │ lister le contenu d'une archive                           │
    │ atool -l -e  arc1.rar  arc2.rar          │ "                 de plusieurs archives                   │
    │                                          │                                                           │
    │                                          │     -e = --each                                           │
    │                                          │     execute command for each argument                     │
    ├──────────────────────────────────────────┼───────────────────────────────────────────────────────────┤
    │ atool -x         arc.tar.gz              │ extraire le contenu d'une archive                         │
    │ atool -X /tmp    arc.tar.gz              │ extraire le contenu d'une archive dans /tmp               │
    │                                          │                                                           │
    │                                          │     -X = --extract-to                                     │
    │                                          │                                                           │
    │ atool -x -e  *.tar.gz                    │ extraire toutes les archives .tar.gz du dossier courant   │
    │                                          │                                                           │
    │ atool -x -S  arc.tar.gz                  │ simuler l'extraction d'une archive                        │
    └──────────────────────────────────────────┴───────────────────────────────────────────────────────────┘


    atool -a -F.tar.gz -e path/to/d1 path/to/d2 path/to/d3

        Crée 3 archives `d1.tar.gz`, `d2.tar.gz`, `d3.tar.gz`, à partir du contenu
        des 3 dossiers d1, d2 et d3.

        Chaque archive est créée dans le dossier parent (de d1, d2, d3).


    arepack -F.tar.7z -e *.tar.gz

        Convertir toutes les archives .tar.gz du dossier courant, en archives .tar.7z.
        Les archives d'origine sont préservées.

        Atm, sur ma machine, `atool` ne dispose pas de flag pour exécuter `arepack`.


    find ~ -iname '*.conf' -print0 | atool -0 -a arc.tar.gz -0
                           │               │
                           │               └ lit l'entrée standard en considérant le null caractère
                           │                 comme le séparateur entre 2 noms de fichiers
                           │
                           └ écrit les noms de fichiers en les séparant par un null caractère

            Crée une archive à partir des fichiers trouvés par une commande `find`.

            La combinaison des options `-print0` de `find` et `-0` de `atool` permet de résoudre
            le problème des noms de fichiers contenant des caractères spéciaux (newline, whitespace).


                                               NOTE:

            `find` produit des chemins absolus vers des fichiers, et `atool` s'en sert pour reproduire
            l'arborescence de dossiers d'origine pour chaque fichier.
            IOW, `atool` n'archive pas tous les fichiers trouvés à la racine d'un dossier,
            mais en respectant fidèlement les chemins d'origine.


    atool -x arc.zip -D

            Extrait une archive en forçant la création d'un dossier d'extraction même si l'archive
            ne contient qu'un fichier.  Illustre l'utilisation du flag `-D` (`--subdir`).


    atool -x arc.zip -f
    atool -a arc.zip -f

            Extrait / Crée  une archive en forçant l'écrasement de  fichiers préexistants en cas
            de conflits. -f = --force


### curl

`curl` accept plusieurs arguments.  En voici quelques-uns:


    -f, --fail

            Échoue silencieusement en cas d'erreurs côté serveur.
            Utile pour ne pas dl une page d'erreur expliquant pourquoi le document est inaccessible.
            `curl` retourne alors le code d'erreur 22.
            Ne fonctionne pas tjrs.  En particulier qd l'échec vient d'une erreur d'authentification (401 et 407).


    -L, --location

            Si le serveur répond que la page demandée a changé d'emplacement, `curl` redemandera la page
            à la nouvelle adresse.


    -o, --output <file>

            Écrit dans <file> au lieu de la sortie standard.

            See  also  the  --create-dirs  option  to  create  the  local  directories  dynamically.


    -o </path/to/file> --create-dirs

            Si certains dossiers de `/path/to/file` n'existent pas sur la machine locale,
            `--create-dirs` les créera.


    curl -fLo /path/to/file --create-dirs url

            Télécharge la page présente à l'adresse url, dans le fichier `/path/to/file` en créant
            les dossiers manquant si besoin, silencieusement (-f), et en suivant les changements
            d'emplacement (-L).


### grep

    $ cat <<'EOF' >file
    this line has !bangs!
    this one has -dashes-
    this one has .dots.
    EOF

            On crée un fichier via un `Here Documents` (construction décrite dans `man bash`).


                                               NOTE:

            On  a  quoté  le  délimiteur  EOF  pour éviter  que  bash  ne  procède  à  certains
            développements au sein de l'input saisie.  En particulier, on ne veut pas qu'il tente de
            développer `backticks` comme s'il s'agissait d'une substitution de commande (ex: `ls`).


                                               NOTE:

            Si on veut copier-coller ce code dans un terminal, faire une copie depuis le mode
            visuel par bloc (!= linewise):    _vicY

            Si on fait une copie linewise (Vip), la dernière ligne contiendra 4 espaces puis EOF.
            Les 4 espaces sont pris en compte lors de la comparaison avec le délimiteur déclaré
            au tout début. Ça empêche la vérification d'avoir lieue.


                                               NOTE:

            Il est probable que bash fasse la chose suivante:

                        ┌─ reconnecte l'entrée standard de `cat` vers le fd de `file`
                        │
                    cat file
                    cat <<'EOF'
                        │
                        └─ connecte l'entrée standard de `cat` vers le fd du terminal

            La principale en différence entre `cat` et `cat <<'EOF'` est le support d'une saisie
            multi-lignes.


    ┌────────────────────┬─────────────────────────────────────────────────────────┐
    │ grep '!|-' file    │ ne match rien                                           │
    │                    │                                                         │
    │                    │ le pipe est lu littéralement et non pas                 │
    │                    │ comme une alternation                                   │
    ├────────────────────┼─────────────────────────────────────────────────────────┤
    │ grep '!\|-' file   │ match les bangs et dashs des lignes 1 et 2              │
    │                    │                                                         │
    │ grep -E '!|-' file │ pour que le pipe soit interprété comme un métacaractère │
    │                    │ il faut soit l'échapper soit utiliser le flag `-E`      │
    ├────────────────────┼─────────────────────────────────────────────────────────┤
    │ grep -F '.' file   │ match les points de la ligne 3                          │
    │                    │                                                         │
    │                    │ le point n'est pas interprété comme un métacaractère    │
    │                    │ à cause du flag `-F`                                    │
    └────────────────────┴─────────────────────────────────────────────────────────┘

            -E permet de donner un sens spécial à certains caractères (+?|(){}) présents
            dans un pattern, sans avoir besoin de les échapper.

            -F fait l'opposé: il retire le sens spécial à tous les caractères du pattern.

                    -E  ⇔  \v
                    -F  ⇔  \V


    $ cat <<-'EOF' >file
	toto
	root
	video
    EOF

    grep -F -f file /etc/group

            Affiche les lignes de `/etc/group` contenant une des lignes de `file`.
            La comparaison est littérale grâce à -F.

            `-f file` a pour effet de générer le pattern:

                    'line1\|line2\|...'

            ... où `line1`, `line2` ... sont les lignes de `file`.


                                               NOTE:

            On a préfixé le délimiteur EOF avec `-` pour que bash supprime les leading tabs.
            Sans lui, le pattern généré par `-f file` ne serait pas `toto\|root\|video` mais
            `	toto\|	root\|	video`.

            `-` ne supprime que des leading tabs, pas d'espaces.


    grep -e -foo file    ✔
    grep    -foo file    ✘

            Cherche la chaîne '-foo' dans `file`.

            Sans `-e`, grep penserait que `-foo` est une option.
            Pour être plus précis, il penserait qu'il s'agit de l'option `-f` à laquelle on donne
            la valeur `oo`.  IOW, il chercherait à générer un pattern à partir d'un fichier `oo`.

            `-e` est utile qd on cherche un pattern commençant par un tiret.


### less

    cmd | less → s

            Qd `less` lit la sortie d'une commande, on peut appuyer sur `s` pour sauvegarder ce qu'on lit
            dans un fichier.


    less package.deb

            Affiche le contenu d'un deb (via le pré-processeur `/usr/bin/lesspipe`).

            Seul `less` est capable de faire ça.
            Vim ne fonctionnerait  pas, en revanche on  pourrait l'utiliser pour
            lire la sortie de less:

                    vim package.deb            ✘
                    less package.deb | vipe    ✔

### ls

     ┌─────────────────────┬─────────────────────────────────────────────────────────┐
     │ ls -1               │ une seule entrée par ligne                              │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -A               │ n'affiche pas les entrées `.` et `..`                   │
     │                     │                                                         │
     │                     │ -A = --almost-all                                       │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -b               │ affiche une séquence d'échappement pour représenter     │
     │                     │ un caractère non graphique                              │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -C | less        │ liste les entrées par colonnes et pipe la sortie        │
     │                     │ de `ls` vers `less`                                     │
     │                     │                                                         │
     │                     │ par défaut, qd on redirige la sortie de `ls` vers       │
     │                     │ `less`, `ls` affiche les entrées par lignes (`-1`)      │
     │                     │ `-C` l'oblige à afficher par colonnes                   │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -F               │ ajoute un indicateur à la fin de chaque entrée          │
     │                     │ correspondant à son type                                │
     │                     │                                                         │
     │                     │         @ = lien symbolique                             │
     │                     │         / = dossier                                     │
     │                     │         * = exécutable                                  │
     │                     │                                                         │
     │                     │ -F = --classify                                         │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -Gg              │ long listing (comme `-l`), mais sans le nom du          │
     │                     │ proprio ni celui du groupe                              │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -p               │ ajoute un slash après les noms des dossiers             │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -lt              │ long listing, en triant par date (`-t`)                 │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -X               │ tri par extension                                       │
     │                     │                                                         │
     │                     │    les .avi avant les .mp4                              │
     │                     │ et les .mp4 avant les .txt                              │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │                     │ trie en fonction de la date de:                         │
     │                     │                                                         │
     │ ls -lt --time=mtime │     dernière modification du contenu                    │
     │ ls -lt --time=ctime │                           du contenu ou des métadonnées │
     │ ls -lt --time=atime │     dernier accès en lecture                            │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls *                │ liste tout: fichiers, dossiers, et leurs contenus       │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls */               │ liste les dossiers et leurs contenus                    │
     │                     │                                                         │
     │                     │ le slash empêche le scan des fichiers à la RACINE       │
     │                     │ du dossier courant, mais il n'empêche pas               │
     │                     │ l'affichage des fichiers des sous-dossiers              │
     ├─────────────────────┼─────────────────────────────────────────────────────────┤
     │ ls -d */            │ liste les dossiers mais pas leurs contenus              │
     │                     │                                                         │
     │                     │ `-d` empêche le scan du contenu des dossiers            │
     └─────────────────────┴─────────────────────────────────────────────────────────┘

                                               NOTE:

            touch $'foo\nbar'; ls       →    foo?bar
                               ls -b    →    foo\nbar    # `-b` permet de représenter un caractère non graphique

            touch foo\ bar; ls          →    foo bar
                            ls -b       →    foo\ bar    # les espaces sont également échappés par `-b`


                                               NOTE:

            La plupart du temps, les dossiers n'ont  pas d'extension, `ls -X` est donc pratique pour
            séparer rapidement les  dossiers des fichiers.  Attention, un dossier  peut malgré tout
            avoir une extension (`ls -X /etc`), comme par exemple `folder.d` ou `folder.conf`.


                                               NOTE:

            À chaque fichier/dossier est associé 3 timestamps:

                    - mtime: date de dernière modification du contenu
                    - ctime: "                                        ou des métadonnées
                    - atime: date de dernier accès en lecture

            Mettre à  jour le `atime` de  chaque entrée du  système de fichiers peut  ralentir le
            système, c'est pourquoi la partition racine est souvent montée avec l'option `noatime`
            ou `relatime`.

            `noatime` signifie que `atime` n'est jamais mis à jour. `relatime` signifie que `atime`
            n'est pas mis à jour au-delà d'une certaine limite (une fois par jour pex).

            On peut voir les  options qui ont été activées au moment de  monter une partition via
            la commande `mount`.  Pour plus d'infos: https://unix.stackexchange.com/a/8842/232487

### ls++

    https://github.com/trapd00r/ls--

            ls++ - colorized ls on steroids

            Page du projet.


    $ sudo cpan Term::ExtendedColor
    $ git clone git://github.com/trapd00r/ls--.git
    $ cd ls--
    $ perl Makefile.PL
    $ make
    $ sudo make install
    $ mkdir ~/.config/ls++ ; cp ls++.conf $HOME/.config/ls++/ls++.conf

            Procédure d'installation.


    ~/.config/ls++/ls++.conf

            On peut configurer l'apparence de la sortie de `ls++` via ce fichier.
            Il est écrit en Perl.  Pour plus d'infos, lire `man ls++.conf`.


                                               NOTE:

            À l'intérieur on peut changer la valeur de 4 variables:

                    - @d
                    - @c
                    - $colorscheme
                    - %ls_colors

            @d est une array  contenant les caractères à ajouter pour séparer  les colonnes de la
            sortie de `ls++`.

            @c est une  array contenant 16 codes  de couleur décimaux pour  configurer les couleurs
            d'un color scheme.  Exemple de configuration:

                    elsif($colorscheme eq 'my_colorscheme') {
                      $c[0]  = 237; # ???
                      $c[1]  = 131; # +x
                      $c[2]  = 64;  # d(irectory), +r, K(ilobytes)
                      $c[3]  = 075; # G(igabytes), sec(onds)
                      $c[4]  = 140; # day
                      $c[5]  = 209; # ???
                      $c[6]  = 185; # ???
                      $c[7]  = 129; # +w, owner, size
                      $c[8]  = 202; # group
                      $c[9]  = 172; # hour
                      $c[10] = 243; # ???
                      $c[11] = 161; # ???
                      $c[12] = 240; # ???
                      $c[13] = 025; # ???
                      $c[14] = 242; # B(ytes), mon(th)
                      $c[15] = 196; # Min
                    }

            Pour trouver le code d'une couleur donnée:

                    https://jonasjacek.github.io/colors/
                    https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg


            `$colorscheme` permet de choisir le color scheme à utiliser.
            Exemple de configuration:        $colorscheme = 'mine';

            `%ls_colors` est un hash (tableau/dico/array associative?) dont les clés sont des patterns
            et les valeurs des couleurs ou des attributs.
            Exemple de configuration:

                    %ls_colors = (
                      'README$'        => $c[8],    # utilise la couleur 8 pour un fichier README
                      'Makefile$'      => $c[15],   # "                 15 "               Makefile
                    );

            Les patterns sont des regex, on peut donc utiliser des métacaractères:

                    $    fin du nom de fichier
                    .*   n'importe quelle séquence de caractères
                    \.   un point littéral
                    ?    quantificateur 0 ou 1
                    ()   groupe

            `%ls_colors` est l'équivalent de `LS_COLORS`.
            `LS_COLORS` est une variable d'environnement permettant de configurer les couleurs de la
            commande `ls`.

            `%ls_colors` est plus puissante que `LS_COLORS`, car ses patterns sont comparés aux noms
            des entrées, et non pas seulement aux extensions des fichiers.

            À la place d'une couleur (`c[3]` pex), on peut utiliser la valeur spéciale `IGNORE`.
            Dans ce cas, un fichier dont le nom est décrit par la regex ne sera pas colorisé.


    ┌──────────────┬─────────────────────────────────────────┐
    │ ls++ --pf    │ permissions, file                       │
    ├──────────────┼─────────────────────────────────────────┤
    │ ls++ --psf   │ permissions, size, file                 │
    ├──────────────┼─────────────────────────────────────────┤
    │ ls++ --ptsf  │ permissions, time, size, file (default) │
    ├──────────────┼─────────────────────────────────────────┤
    │ ls++ --potsf │ permissions, owner, time, size, file    │
    └──────────────┴─────────────────────────────────────────┘

            Utilisation.


    ls++ -A           ✔
    ls++ -A | vipe    ✘

            On peut passer une option inconnue à `ls++`, comme ici `-A` pour afficher les éléments cachés.
            En effet, elle est passée d'abord à `ls`, pour être interprétée.

            En revanche, `ls++` ne fonctionne pas comme prévu au sein d'un pipeline, comme le montre
            la 2e commande.  Peut-être en raison des codes couleurs ANSI produits en sortie.

            Un bug report existe, mais le bug n'a jamais été corrigé:

                    https://github.com/trapd00r/ls--/issues/32

            Si on a créé l'alias `alias ls='ls++'`, on peut contourner le pb en le désactivant temporairement:

                    \ls -A | vipe


    ls++ -tg    →   ▕ drwxrwxr-x▏48 year│1493967014B│Documents
                                 │       │
                                 │       └── ✘
                                 └── ✘

            Certaines combinaisons de flags `ls` produisent des résultats étranges avec `ls++`.


### mapscii

    https://github.com/rastapasta/mapscii

            MapSCII is a Braille & ASCII map renderer for your console.


    telnet mapscii.me

            Utiliser la version du programme en ligne.


    sudo npm install -g mapscii

            Installer le programme en local.

            Nécessite le programme `node` en version >= 4.5.

            Atm, sur Ubuntu 16.04, il ne semble pas y avoir de paquet `node`:

                    % apt-cache policy node
                    ∅~

            En revanche, il y a bien un paquet `npm`, mais sa version (3.5.2) ne semble pas suffisante
            pour utiliser/installer correctement `mapscii`:

                    % apt-cache policy npm

                    npm:
                    Installed: (none)
                    Candidate: 3.5.2-0ubuntu4
                    Version table:
                        3.5.2-0ubuntu4 500
                            500 http://fr.archive.ubuntu.com/ubuntu xenial/universe amd64 Packages
                            500 http://fr.archive.ubuntu.com/ubuntu xenial/universe i386 Packages

            Même si l'installation réussit, `mapscii` ne fonctionne pas correctement.
            Il faut donc installer la dernière version LTS de `node`.
            Lire nos notes sur le sujet, dans ce même fichier.


    mapscii

            Lancer le programme compilé localement.


    ┌────────────────────┬────────────────────────────────┐
    │ a                  │ zoomer                         │
    ├────────────────────┼────────────────────────────────┤
    │ z                  │ dézoomer                       │
    ├────────────────────┼────────────────────────────────┤
    │ up down left right │ déplacer le centre de la carte │
    ├────────────────────┼────────────────────────────────┤
    │ q                  │ quitter                        │
    └────────────────────┴────────────────────────────────┘

            Raccourcis claviers utilisables pour trouver un lieu géographique bien précis.

### nmtui

    Text User Interface for controlling NetworkManager

    It's already installed.

### node

    gcc and g++ 4.9.4 or newer
    Python 2.6 or 2.7
    GNU Make 3.81 or newer

            Dépendances pour pouvoir compiler `node` sous Linux.


    https://github.com/nodejs/LTS/

            Page listant les différentes version du programme.
            Chercher la version LTS active la plus récente.  Atm, c'est `6.11.0`.
            On va se servir de ce n° de version dans une commande `git checkout`.


    https://github.com/nodejs/node/blob/master/BUILDING.md#building-nodejs-on-supported-platforms

            Description de la procédure de compilation.


                                               NOTE:

            On peut télécharger un binaire précompilé, ici:

                    https://nodejs.org/en/download/

            Toutefois, je n'ai pas réussi à l'utiliser / installer correctement.
            Si on utilise cette méthode d'installation, penser à vérifier la signature du binaire.

            Au passage, on peut utiliser ce lien pour confirmer le n° de version de la LTS la plus récente.


                                               NOTE:

            Il semble qu'on puisse aussi installer le programme via `apt-get`:

                    https://nodejs.org/en/download/package-manager/

                    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
                    sudo apt-get install -y nodejs

            À utiliser éventuellement, si la compilation échoue ou prend trop de temps.


    $ git clone https://github.com/nodejs/node/
    $ cd node
    $ git checkout v6.11.0
    $ ./configure
    $ make
    $ make test
    $ make doc
    $ man doc/node.1 (test)
    $ ./node -e "console.log('Hello from Node.js ' + process.version)"
    Hello from Node.js v6.11.0   (test)~
    $ sudo make install

            Procédure d'installation.


                                               NOTE:

            `node` est un très gros projet:

                    % du -sh ~/Vcs/node
                    751M    /home/user/Vcs/node

            La compilation peut prendre beaucoup de temps, et consommer pas mal de ressources (mémoire et cpu).

            Pour accélérer la compilation on peut passer le flag `-j` à `make`, pour lui demander d'exécuter
            plusieurs jobs simultanément:

                    make -j4
                           │
                           └ 4 jobs

            Toutefois, ça augmente la consommation de ressources de manière drastique. À éviter sur une machine
            peu puissante.  Voici ce que rapporte la commande `make -j4` sur ma machine atm:

                    make -j4  2160.75s user 97.62s system 363% cpu 10:21.56 total
                                                                   ├────────────┘
                                                                   └ temps pris par la compilation

            On constate qu'elle a augmenté la charge cpu à 363%, et pris 10 minutes et 21 secondes.
            Si on avait réduit le nombre de jobs, la compilation aurait sans doute pris
            beaucoup plus de temps, mais consommé beaucoup moins de ressources.

            Conseil: bite the bullet, et n'utiliser qu'un seul job (`make` sans `-j`).

### notify-send

                      ┌───────────── duration, in milliseconds, for the notification to appear on screen
                      │            ┌ spécifie un nom d'icone custom ou stock (installé avec l'OS)
                      │            │ ici, `edit-copy` est une icône stock
                ┌─────┤ ┌──────────┤
    notify-send -t 5000 -i edit-copy "Title" "Message"

            Envoit une notification sur le bureau, intitulée "Title", et dont le contenu est "Message".

            On peut utiliser toutes les icônes présentes dans notre thème d'icônes.
            Pex, si on utilise le thème “Paper“:

                    cd /usr/share/icons/Paper/ ; tree -a V

### parallel  xargs

    https://www.youtube.com/watch?v=OpaiGYxkSuQ
    https://www.gnu.org/software/parallel/parallel_tutorial.html


    cd /var/cache/apt/archives/
    sudo aptitude download parallel
                  │
                  └ dl le `.deb` dans le répertoire courant

    sudo dpkg --force-conflicts --install parallel Tab (*)
                │
                └ [!] conflicts    Allow installation of conflicting packages
                  description trouvée via `dpkg --force-help`

    sudo /var/lib/dpkg/status
      chercher `package: moreutils`, et supprimer la ligne `conflicts: moreutils` qui suit


            Procédure d'installation du paquet `parallel`, si `moreutils` est déjà présent sur le système.

            Il y a un conflit entre la version du binaire `parallel` présent dans `moreutils`, et
            celle fournie par le paquet `parallel`.

            (*) Tab pour compléter le nom du paquet.  Ex:

                    parallel  →  parallel_20141022+ds1-1_all.deb

            Messages importants pendant l'installation de `parallel`:

                    dpkg: warning: ignoring conflict, may proceed anyway!
                    ...
                    Adding 'diversion of /usr/bin/parallel to /usr/bin/parallel.moreutils by parallel'
                    Adding 'diversion of /usr/share/man/man1/parallel.1.gz to
                                         /usr/share/man/man1/parallel.moreutils.1.gz by parallel'

            Une diversion consiste à déplacer un fichier qd il est en conflit avec un autre lors d'une
            installation.  Elle est réalisée par `dpkg-divert`.
            On peut lister toutes les diversions ayant été réalisées sur le système, et par quels programmes:

                    dpkg-divert --list

            Une fois qu'on a installé une diversion pour un fichier donné, tout paquet le fournissant
            l'installera dans un nouvel endroit, avec un autre nom si désiré.
            Il ne s'agit donc pas d'un simple déplacement, car on informe tout le système que ce déplacement
            doit être répété à chaque installation / mise à jour d'un paquet fournissant le fichier.


            J'ai trouvé toute cette procédure ici:
                    https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=749355;msg=110


            La dernière édition est nécessaire pour empêcher `apt-get` et `aptitude` de se plaindre
            qd on fait une màj:

                    $ sudo aptitude upgrade
                    Unable to resolve dependencies for the upgrade: no solution found.~
                    Unable to safely resolve dependencies, try running with --full-resolver.~

                    $ sudo apt-get upgrade
                    You might want to run 'apt-get -f install' to correct these.~
                    The following packages have unmet dependencies:~
                    parallel: Conflicts: moreutils but 0.57-1 is installed~
                    E: Unmet dependencies.  Try using -f.~


            Il semble que bientôt (?) la procédure ne sera plus utile, car tout ceci sera fait automatiquement
            par le système:

                    https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=749355#133

### printf

    printf '%s\n' 'foo' 'bar' 'baz'
    foo~
    bar~
    baz~

Contrairement à `VimL` et  `awk`, il semble qu'on ne soit  pas obligé de fournir
autant d'items qu'il n'y d'expressions à formater.
Dans cet exemple, il n'y a qu'un seul item `%s`, mais 3 expressions 'foo', 'bar'
et 'baz'.

### renommage

    touch image{1..9}.png
    for f in *.png; do mv "$f" "${f#image}"; done

            Renomme toutes les images du dossier courant:

                    image1.png  →  1.png
                    ...
                    image9.png  →  9.png

            Illustre  la syntaxe  `${parameter#word}`  décrite  dans `man  bash`
            (’parameter expansion’).
            Cette dernière permet de supprimer  un préfixe dans le développement
            d'un paramètre.
            Ici, `parameter = f` et `word = image`.


                                               NOTE:

            `word` est développé avant `parameter` pour produire un pattern.
            Il existe d'autres syntaxes similaires:

                    ┌───────────┬────────────────────────────────────────────────┐
                    │ ${f#p}    │ supprime le plus court préfixe matchant `p`    │
                    ├───────────┼────────────────────────────────────────────────┤
                    │ ${f##p}   │ supprime le plus long préfixe matchant `p`     │
                    ├───────────┼────────────────────────────────────────────────┤
                    │ ${f%p}    │ supprime le plus court suffixe matchant `p`    │
                    ├───────────┼────────────────────────────────────────────────┤
                    │ ${f%%p}   │ supprime le plus long suffixe matchant `p`     │
                    └───────────┴────────────────────────────────────────────────┘

                    ┌───────────┬────────────────────────────────────────────────┐
                    │ ${f/p/r}  │ remplace la 1e occurrence de `p` par `r`       │
                    ├───────────┼────────────────────────────────────────────────┤
                    │ ${f//p/r} │ remplace toutes les occurrences de `p` par `r` │
                    ├───────────┼────────────────────────────────────────────────┤
                    │ ${f/#p/r} │ remplace le préfixe matchant `p` par `r`       │
                    ├───────────┼────────────────────────────────────────────────┤
                    │ ${f/%p/r} │ remplace le suffixe matchant `p` par `r`       │
                    └───────────┴────────────────────────────────────────────────┘

            `f`, `p` et  `r` désignent resp. un paramètre (ex:  nom de fichier),
            un pattern et une chaîne de remplacement.

            Mnémotechnique:
            `#` sert à commenter une ligne, et se place donc au début (préfixe).
            `%` est utilisé à la fin du prompt par défaut de zsh (suffixe).


    touch file{1..9}.bak
    for f in *.bak; do mv "$f" "${f%.bak}"; done

            Renomme tous les fichiers backup en supprimant leur extension.

            Illustre la syntaxe `${parameter%word}`  qui supprime la plus courte
            chaîne matchée par le pattern `word`.
            `${parameter%%word}` supprime la plus longue chaîne.


    for f in .*; do mv "$f" "${f/./}"; done

            Renomme tous  les fichiers cachés  du dossier courant  en supprimant
            leur dot.
            On pourrait remplacer "${f/./}" par "${f#.}".


                                     TODO:
À terminer ...


    rename -v  'y/A-Z/a-z/'  *


                 ┌ zmv '(*)_(*).(*)' '$2-$1.$3'
                 │
    foo_bar.txt  →  bar-foo.txt
    baz_qux.md      baz_qux.md


    zmv 'image(*.png)' '$1'
    zmv -w 'image*.png' '$1.png'

    zmv [ -finqQsvwW ] [ -C | -L | -M | -{p|P} program ] [ -o optstring ]
        srcpat dest
           Move  (usually,  rename)  files matching the pattern srcpat to corresponding files having names of the
           form given by dest, where srcpat contains parentheses surrounding patterns which will be  replaced  in
           turn by $1, $2, ... in dest.  For example,

                  zmv '(*).lis' '$1.txt'

           renames `foo.lis' to `foo.txt', `my.old.stuff.lis' to `my.old.stuff.txt', and so on.

           The  pattern is always treated as an EXTENDED_GLOB pattern.  Any file whose name is not changed by the
           substitution is simply ignored.  Any error (a substitution resulted in an empty string, two  substitu‐
           tions  gave the same result, the destination was an existing regular file and -f was not given) causes
           the entire function to abort without doing anything.

           In addition to pattern replacement, the variable $f can be referrred to in  the  second  (replacement)
           argument.   This  makes  it  possible to use variable substitution to alter the argument; see examples
           below.

           Options:

           -f     Force overwriting of destination files.  Not currently passed down to the mv/cp/ln command  due
                  to vagaries of implementations (but you can use -o-f to do that).
           -i     Interactive:  show each line to be executed and ask the user whether to execute it.  `Y' or `y'
                  will execute it, anything else will skip it.  Note that you just need to type one character.
           -n     No execution: print what would happen, but don't do it.
           -q     Turn bare glob qualifiers off: now assumed by default, so this has no effect.
           -Q     Force bare glob qualifiers on.  Don't turn this on unless you are actually  using  glob  quali‐
                  fiers in a pattern.
           -s     Symbolic, passed down to ln; only works with -L.
           -v     Verbose: print each command as it's being executed.
           -w     Pick  out wildcard parts of the pattern, as described above, and implicitly add parentheses for
                  referring to them.
           -W     Just like -w, with the addition of turning wildcards in the replacement pattern into sequential
                  ${1} .. ${N} references.
           -C
           -L
           -M     Force cp, ln or mv, respectively, regardless of the name of the function.
           -p program
                  Call program instead of cp, ln or mv.  Whatever it does, it should at least understand the form
                  `program -- oldname newname' where oldname and newname are filenames generated by zmv.  program
                  will  be  split  into words, so might be e.g. the name of an archive tool plus a copy or rename
                  subcommand.
           -P program
                  As -p program, except that program does not accept a  following  --  to  indicate  the  end  of
                  options.  In this case filenames must already be in a sane form for the program in question.
           -o optstring
                  The  optstring  is split into words and passed down verbatim to the cp, ln or mv command called
                  to perform the work.  It should probably begin with a `-'.

           Further examples:

                  zmv -v '(* *)' '${1// /_}'

           For any file in the current directory with at least one space in the name, replace every space  by  an
           underscore and display the commands executed.

                  zmv -v '* *' '${f// /_}'

           This does exactly the same by referring to the file name stored in $f.

           For  more complete examples and other implementation details, see the zmv source file, usually located
           in one of the directories named in your fpath, or in Functions/Misc/zmv in the zsh distribution.


    mv -i foo bar

            Renomme `foo` en `bar`.
            Si `bar` existe déjà, le flag `-i` nous demandera une confirmation avant de l'écraser.


    qmv

            Renommer toutes les entrées (fichiers/dossiers) à la racine du dossier de travail.

            Un buffer s'ouvre à l'intérieur duquel des noms d'entrées sont affichés dans 2 colonnes.
            Pour changer le nom d'une entrée, il suffit d'en éditer un dans la colonne de droite.

                    colonne de gauche = anciens noms des entrées
                    colonne de droite = nouveaux noms désirés


                                               NOTE:

            Cette commande est fournie par le paquet `renameutils`.
            Il fournit également:

                    - deurlname
                    - icp
                    - imv
                    - qcp
                    - qmv


    qmv -f do *.jpeg

            Renomme toutes les images du dossier de travail, en utilisant qu'une seule colonne (-f do).

            D'habitude, `qmv` utilise 2 colonnes, une pour afficher l'ancien nom des entrées, l'autre
            pour afficher les noms modifiés.
            Ça peut être ennuyeux qd on veut faire un renommage multiple via une substitution (:%s///g).
            En effet, dans ce cas, on risque de modifier les noms d'origine (colonne 1) ce qui empêchera
            `qmv` de reconnaître les entrées qu'on souhaite renommer: donc aucun renommage.

            `-f do` = `--format destination-only` résoud ce pb.


    qmv -R /tmp/

            Renommer toutes les entrées à l'intérieur de /tmp/.

            L'option -R permet d'explorer les sous-dossiers.


    qmv --help

            Affiche les options supportées par qmv.
            La plupart sont identiques à celles de ls.  qmv s'appuie sur ls et lui passe ces options.

                    -A    affiche toutes les entrées, mêmes cachées
                          mais n'affiche pas les entrées implicites . et .. (contrairement à -a)


    qmv --dummy

            Simule un renommage des entrées du dossier de travail.


    qcp    icp

            Semblables à qmv et imv à ceci près que leur but n'est pas de changer le nom d'entrées
            mais de faire des copies.
            Les nouveaux noms ne sont donc pas utilisés pour changer les anciens mais pour nommer des copies.


    deurlname 'foo%20bar%20baz'    →    'foo bar baz'

            `deurlname` permet de nettoyer un nom de fichier contenant des caractères encodés pour passer
            dans une url (ex: %20 pour espace, %41 pour A ...).

            Certains pgms comme w3m conservent ces caractères indésirables qd on sauvegarde des fichiers
            depuis le web.

### sort

    sort file -o file

            Trie le contenu de `file` in-place.

            Ne surtout pas faire:

                    sort file >file    ✘

            ...  car le  shell  vide  le contenu  de  `file`  lorsqu'il crée  la
            redirection `>file`.
            Il n'y  aurait donc  rien à  trier, et on  finirait avec  un fichier
            vide.


    sort -t$'\t'     -k2,2 file
    sort -t:      -b -k2,2 file

            Trie le contenu de `file` en fonction  du 2e champ des lignes, et en
            considérant le caractère tab comme le séparateur entre 2 champs.

            Idem, mais en  considérant un `:` comme séparateur de  champs, et on
            omettant d'éventuels leading whitespace au sein des champs.


                                               NOTE:

            `-b` est indispensable qd la largeur d'un des champs précédents est variable.

            Il  est  probable que,  par  défaut,  `sort`  n'utilise que  le  1er
            whitespace qu'il rencontre.
            Donc, si  2 champs sont  séparés par plusieurs whitespace,  tous ces
            derniers à l'exception  du 1er sont considérés  comme faisant partie
            du champ.

            Ex:
                    vim <(setopt ksh_option_print; unsetopt)

                    vip
                    !sort    -k2
                    ✘

                    vip
                    !sort -b -k2
                    ✔
                    trie les `off` avant les `on`


                                               NOTE:

            Par défaut, `sort`  utilise les whitespace comme  délimiteurs, et il
            ignore les leading/trailing whitespace de chaque ligne.
            Par  contre,  dès qu'on  utilise  `-t`  pour choisir  un  délimiteur
            arbitraire, `sort` n'ignore plus les leading/trailing whitespace.


                                               NOTE:

            Pk `2,2` et pas `k2` ?

            `-k2` trie  en fonction du  texte commençant  depuis le début  du 2e
            champ jusqu'à la fin de la ligne.
            `-k2,2` trie en  fonction du texte commençant depuis le  début du 2e
            champ jusqu'à la fin du 2e champ.


                                               NOTE:

            L'ordre de tri est influencé par la locale courante.
            Pour ne  pas avoir de  surprise, et si le  texte ne contient  pas de
            caractères spéciaux/accentués, utiliser la locale C:

                    LC_ALL=C sort ...

###
### sudo

#### configuration

    sudo visudo -f /etc/sudoers.d/my_modifications

            Édite un fichier dans `/etc/sudoers.d/`.

            Il est conseillé d'utiliser ce dernier pour modifier le comportement de `sudo`,
            plutôt que `/etc/sudoers`.  Probablement car ce dernier est reset à chaque mise à jour
            du paquet `sudo`.

            `visudo` crée un fichier temporaire, et une fois qu'on quitte l'éditeur, il vérifie la validité
            de la syntaxe du contenu ajouté.


                                               NOTE:

            En cas de conflit entre 2 lignes, c'est celle qui arrive en dernier dans le fichier qui
            a la priorité.


                                               NOTE:

            Les droits, proprio, groupe du dossier et de ses fichiers doivent respecter certaines
            valeurs.  Atm, sous Ubuntu:

                    drwxr-xr-x  root  root  /etc/sudoers.d
                    -r--r-----  root  root  my_modifications


    Defaults    pwfeedback
    Defaults    timestamp_timeout=30

            Active l'option `pwfeedback` pour qu'un astérisque s'affiche à chaque caractère saisi
            qd `sudo` nous demande notre mdp.

            Augmente la durée pendant laquelle notre identification est mise en cache, en la faisant
            passer à 30 minutes.  Par défaut, c'est 15.

            On peut vider ce cache via `sudo -k`, ou au contraire le réinitialiser via `sudo -v`.


     ┌─ Qui ?
     │     ┌─ Où ?
     │     │    ┌─ En tant que qui ?
     │     │    │
    %admin ALL=(ALL)NOPASSWD:/usr/bin/aptitude update
                    │        │
                    │        └─ Quoi ?
                    └─ Comment ?

            Tous les utilisateurs du groupe admin, sur n'importe quelle machine peuvent lancer
            la commande `aptitude update` en tant que n'importe quel autre utilisateur sans donner de mdp.


                                               NOTE:

            Au sein de la commande, tout caractère `:`, `\`, `=` doit être échappé.


    %admin ubuntu=(ALL)NOPASSWD:/usr/bin/aptitude
    %admin ubuntu=(root)NOPASSWD:/usr/bin/aptitude

            Idem mais uniquement sur la machine dont le nom d'hôte est `ubuntu` (`hostname`).
            Idem mais uniquement en tant que root.


                                                         ┌─ pas d'espace après la virgule
                                                         │
    %admin ubuntu=(root)NOPASSWD:/usr/bin/aptitude update,/usr/bin/aptitude safe-upgrade

            Idem mais uniquement pour les commandes `aptitude update` et `aptitude safe-upgrade`.


    %admin ubuntu=(root)NOPASSWD:/usr/bin/aptitude install *

            Idem mais pour toutes les commandes suivant le pattern `aptitude install <paquet>`.


    %admin ubuntu=(root)NOPASSWD:/*/sbin/*

            Idem mais pour toutes les commandes suivant le pattern `/*/sbin/*` comme  p.ex.
            `/usr/sbin`, `/usr/local/sbin/` ou `/home/user/sbin`.


    %admin ubuntu=(root)NOEXEC:/usr/bin/vim

            `NOEXEC` empêche d'utiliser Vim pour lancer des commandes shell, il ne pourra servir
            qu'à éditer du texte.

            Attention `NOEXEC` peut empêcher le bon fonctionnement de certaines commandes.
            Pex, `aptitude` peut avoir besoin de lancer un shell pour y exécuter `dpkg`.


    user ALL=(ALL) ALL

            `user` peut lancer sur n'importe qelle machine, en tant que n'importe quel utilisateur,
            n'importe quelle commande.

#### utilisation

    su -l

            Se connecter en tant que root. `-l` permet de restaurer l'environnement qu'on aurait
            eu si on s'était connecté directement sans passer par le shell courant.

            Il faut fournir le mdp du compte root.

            Plus généralement, `su` permet de se connecter en tant que n'importe quel utilisateur,
            à condition de lui fournir son nom en argument.


          ┌─ reinItialize
          │
    sudo -i

            Lance le shell de root en mode login, et en restaurant l'environnement qu'on aurait eu
            si on s'était connecté directement.

            Il faut fournir le mdp du compte courant.


                                               NOTE:

            Plus généralement, `-i` permet de:

                    - lancer le shell d'un utilisateur cible (via `-u user`)

                      En son absence root est utilisé.

                    - exécuter une commande arbitraire (elle est passée au shell via `-c`; ex: `bash -c 'cmd'`)

                      En son absence, un shell interactif est lancé, avec pour répertoire de travail
                      le home de l'utilisateur cible.


    sudo -l    sudo -ll

            Affiche la politique de sécurité définie dans `/etc/sudoers` relative à l'utilisateur courant.
            `-ll` utilise un format d'affichage plus long.


                       ┌ home de l'utilisateur `www`
                    ┌──┤
    sudo -u www vim ~www/htdocs/index.html

            Éditer `index.html` comme si on était l'utilisateur `www`.


    sudo -g adm vim /var/log/syslog

            Lire les logs système comme si on étant membre du groupe `adm` (admin).


    sudo -u jim -g audio vi ~jim/sound.txt

            Éditer `sound.txt` comme si on était `jim` et membre du groupe `audio`.


    $ sudo    bash -c 'echo $HOME'
    /home/user~
    $ sudo -H bash -c 'echo $HOME'
    /root~

            L'option `-H = --set-home` demande à `sudo` de donner pour valeur à `$HOME` le home
            de l'utilisateur cible.


                                               NOTE:

            Si on avait simplement exécuté:

                    $ sudo    echo $HOME
                    /home/user~
                    $ sudo -H echo $HOME
                    /home/user~

            ... on aurait constaté aucune différence, car `$HOME` aurait été développé avant d'exécuter
            la commande.


    sudo bash -c "cd /home ; du -sh * | sort -rn >USAGE"

            Calculer l'espace occupé par les homes des utilisateurs du système, et écrire le résultat
            dans `/home/USAGE`.

            `/home` est possédé par `root`, et les droits ne permettent pas à un autre utilisateur
            d'y créer un fichier:

                    ls -ld /home
                    drwxr-xr-x 3 root root 4096 Jan 18 18:04 /home~
                            │~
                            └─ pas le droit de modification~

            Il faut donc élever nos privilèges via `sudo`.


                                               NOTE:

            Pk `bash -c` ? Pour 2 raisons:

            1. `sudo` ne peut exécuter que des programmes externes au shell, et `cd` n'en est pas un.

            2. La redirection `>USAGE` est effectuée par le shell courant, dont l'EUID est le simple
               utilisateur courant (car c'est nous qui l'avons lancé).
               Donc, si on n'a pas les droits suffisants pour écrire dans `/home`, le shell courant non plus.


                                               NOTE:

            EUID vs RUID

            Qd on lance  une commande via `sudo`, le processus  qui en résulte a
            un RUID et un EUID différents.
            Le RUID  (Real User ID)  est l'utilisateur  qui a lancé  la commande
            (ex: toto).
            Le EUID (Effective User ID) est l'utilisateur cible (ex: root).


    export FOO=bar; sudo    bash -c 'echo $FOO'
    ∅~
    export FOO=bar; sudo -E bash -c 'echo $FOO'
    bar~

            Par défaut, `sudo` ne préserve pas les variables d'environnement.
            Si on veut les conserver, il faut utiliser l'option `-E`.
            La réussite de la conservation dépend de la politique de sécurité définie dans `/etc/sudoers`.

            `-E` désactive temporairement l'option `env_reset`. Équivaut à:

                    Defaults    !env_reset


                                               NOTE:

            On pourrait aussi inclure `FOO` dans l'option `env_keep`:

                    Defaults    env_keep += "FOO"

            Et si on voulait en préserver plusieurs:

                    Defaults    env_keep += "VAR1 VAR2"


    $ sudo -E         bash -c 'echo $PATH'
    root's path~
    $ sudo PATH=$PATH bash -c 'echo $PATH'
    current user path~

            Ni `-E`, ni `env_keep` ne préservent pas `PATH`, il faut donc la passer manuellement.


#### déboguage

    /var/log/auth.log

            Chaque utilisation de `sudo` ajoute une ligne dans ce fichier.
            À consulter en cas de pb.

###
### tee

    cmd | tee    file        cmd  >file
    cmd | tee -a file        cmd >>file
               │
               └─ append

            `tee` permet d'écrire la sortie d'une commande dans un fichier, en écrasant ou en préservant
            son contenu initial.


    echo 'hello' >> tee -a *

            Écrit `hello` à la fin de tous les fichiers du répertoire courant.

            `tee` permet d'ajouter le support des wildcards à des commandes ne l'ayant pas par défaut.


    cmd | tee file1 file2 file3

            `tee` permet d'écrire la sortie d'une commande dans plusieurs fichiers.


    cmd1 | tee file | cmd2

            `tee` écrit la sortie de `cmd1` dans `file` ET la refile au pipe qui suit,
            qui la refile à `cmd2`.

            En effet, même qd on demande à `tee` de rediriger sa sortie dans un fichier,
            il continue de l'afficher à l'écran (double sortie).

            On peut le vérifier simplement:

                    ls | tee file

            La sortie de `ls` est bien écrite dans `file` ET affichée à l'écran.


               cmd >root_file    ✘
          sudo cmd >root_file    ✘

    cmd | sudo tee  root_file    ✔

            `tee` permet d'écrire la sortie d'une commande dans un fichier pour lequel on n'a pas
            les droits suffisants.

            La 2e commande échoue car ce n'est pas `cmd` qui écrit dans le fichier, mais le shell
            (qui effectue la redirection).
            Il faut donc élever les droits du shell, ou d'une commande écrivant dans le fichier.

###
### Futur

#### atop

    api atop
    man atop

            Ressemble à `top` avec peut-être plus d'infos, et l'enrigstrement de l'activité passée
            (pas juste l'activité courante).

#### chafa

View gifs in your terminal.

    $ git clone https://github.com/hpjansson/chafa.git
    $ sudo aptitude install libmagickwand-dev
    $ ./autogen.sh
    $ make
    $ sudo make install

- <https://www.youtube.com/watch?v=SoYKKzBNnwo>
- <https://github.com/hpjansson/chafa>

#### cylon-deb

    TUI menu driven bash shell script to maintain a Debian based Linux distro.

    https://github.com/gavinlyonsrepo/cylon-deb

                                              469 sloc

    Pourrait être utile pour automatiser une maintenance plus rigoureuse d'une distro basée sur debian.

#### dasht

    Search API docs offline, in terminal or browser.

    https://github.com/sunaku/dasht

    dasht-docsets-install

            lister toutes les documentations installables:

                    ActionScript
                    Akka
                    Android
                    Angular
                    Angular.dart
                    AngularJS
                    AngularTS
                    Ansible
                    Apache_HTTP_Server
                    Appcelerator_Titanium
                    Apple_Guides_and_Sample_Code
                    AppleScript
                    Arduino
                    AWS_JavaScript
                    BackboneJS
                    Bash
                    Boost
                    Bootstrap_2
                    Bootstrap_3
                    Bootstrap_4
                    Bourbon
                    C
                    C++
                    CakePHP
                    Cappuccino
                    Chai
                    Chef
                    Clojure
                    CMake
                    Cocos2D
                    Cocos2D-X
                    Cocos3D
                    CodeIgniter
                    CoffeeScript
                    ColdFusion
                    Common_Lisp
                    Compass
                    Cordova
                    Corona
                    CouchDB
                    Craft
                    CSS
                    D3JS
                    Dart
                    Django
                    Docker
                    Doctrine_ORM
                    Dojo
                    Drupal_7
                    Drupal_8
                    ElasticSearch
                    Elixir
                    Emacs_Lisp
                    EmberJS
                    Emmet
                    Erlang
                    Express
                    ExpressionEngine
                    ExtJS
                    Flask
                    Font_Awesome
                    Foundation
                    GLib
                    Go
                    Gradle_DSL
                    Gradle_Groovy_API
                    Gradle_Java_API
                    Gradle_User_Guide
                    Grails
                    Groovy
                    Groovy_JDK
                    Grunt
                    Gulp
                    Haml
                    Handlebars
                    Haskell
                    HTML
                    Ionic
                    Jade
                    Jasmine
                    Java_EE6
                    Java_EE7
                    Java_EE8
                    JavaFX
                    JavaScript
                    Java_SE6
                    Java_SE7
                    Java_SE8
                    Java_SE9
                    Jekyll
                    Jinja
                    Joomla
                    jQuery
                    jQuery_Mobile
                    jQuery_UI
                    Julia
                    KnockoutJS
                    Kobold2D
                    Laravel
                    LaTeX
                    Less
                    Lo-Dash
                    Lua_5.1
                    Lua_5.2
                    Lua_5.3
                    Man_Pages
                    MarionetteJS
                    Markdown
                    MATLAB
                    Matplotlib
                    Meteor
                    Mocha
                    MomentJS
                    MongoDB
                    Mongoose
                    Mono
                    MooTools
                    MySQL
                    Neat
                    NET_Framework
                    Nginx
                    NodeJS
                    NumPy
                    OCaml
                    OpenCV
                    OpenCV_C
                    OpenCV_C++
                    OpenCV_Java
                    OpenCV_Python
                    OpenGL_2
                    OpenGL_3
                    OpenGL_4
                    Pandas
                    Perl
                    Phalcon
                    PhoneGap
                    PHP
                    PHPUnit
                    Play_Java
                    Play_Scala
                    Polymer.dart
                    PostgreSQL
                    Processing
                    PrototypeJS
                    Pug
                    Puppet
                    Python_2
                    Python_3
                    Qt_4
                    Qt_5
                    R
                    Racket
                    React
                    Redis
                    RequireJS
                    Ruby
                    Ruby_2
                    Ruby_Installed_Gems
                    RubyMotion
                    Ruby_on_Rails_3
                    Ruby_on_Rails_4
                    Ruby_on_Rails_5
                    Rust
                    SailsJS
                    SaltStack
                    Sass
                    Scala
                    SciPy
                    Semantic_UI
                    Sencha_Touch
                    Sinon
                    Smarty
                    Sparrow
                    Spring_Framework
                    SQLAlchemy
                    SQLite
                    Statamic
                    Stylus
                    Susy
                    SVG
                    Swift
                    Symfony
                    Tcl
                    Tornado
                    Twig
                    Twisted
                    TypeScript
                    TYPO3
                    UnderscoreJS
                    Unity_3D
                    Vagrant
                    Vim
                    VMware_vSphere
                    VueJS
                    WordPress
                    Xamarin
                    Xojo
                    XSLT
                    XUL
                    Yii
                    YUI
                    Zend_Framework_1
                    Zend_Framework_2
                    Zend_Framework_3
                    ZeptoJS

    dasht-docsets-install bash

            Installe la documentation bash.

    dasht 'c - x'

            Chercher dans la documentation tous les sujets contenant 'c - x'.

#### dateutils

    https://github.com/hroptatyr/dateutils

            nifty command-line date and time utilities; fast date calculations and conversion in the shell

#### dfc

    TODO: lire `man dfc`
    dfc - display file system space usage using graphs and colors
    (df mais en plus lisible)

#### diana-mui

- <https://www.youtube.com/watch?v=y59JwlYsrAE>
- <https://github.com/baskerville/diana>

#### direnv

- <https://github.com/direnv/direnv>
- <https://github.com/direnv/direnv.vim>

direnv is an environment switcher for the shell.
It knows  how to hook  into bash, zsh,  tcsh, fish shell  and elvish to  load or
unload environment variables depending on the current directory.
This  allows  project-specific  environment  variables  without  cluttering  the
~/.profile file.

Before each prompt,  direnv checks for the  existence of a ".envrc"  file in the
current and parent directories.
If the file exists  (and is authorized), it is loaded into  a bash sub-shell and
all exported  variables are then captured  by direnv and then  made available to
the current shell.

Because direnv is compiled into a single static executable, it is fast enough to
be unnoticeable on each prompt.
It  is also  language-agnostic and  can be  used to  build solutions  similar to
rbenv, pyenv and phpenv.

#### findmnt

    findmnt - find a filesystem

#### khal

    https://github.com/pimutils/khal

            CLI calendar application


    https://github.com/pimutils/vdirsyncer

            Synchronize calendars and contacts.


    https://github.com/scheibler/khard

            Console carddav client.


#### googler

    https://github.com/jarun/googler

            Google Search, Google Site Search, Google News from the terminal

#### grep-typos

    https://github.com/ss18/grep-typos

            Quickly check your project for typos

#### highlight

    $ git clone https://gitlab.com/saalen/highlight && cd *(/oc[1])
    $ git checkout x.y
    $ make help
    $ make
    $ sudo make install

<http://www.andre-simon.de/doku/highlight/en/highlight.php>

#### inotifywait

    https://github.com/rvoicilas/inotify-tools/wiki
    https://superuser.com/a/181543/747860
    https://www.reddit.com/r/neovim/comments/7rk7v7/markdown_pandoc_live_pdf_preview_neovim/dsyinvx/

            File watcher.

            Alternatives:

                    http://entrproject.org/  ✔✔✔ à tester, peut-être meilleur que `inotify`
                    https://github.com/cortesi/modd
                    https://github.com/mattgreen/watchexec
                    https://github.com/stylemistake/runner
                    https://github.com/shanzi/wu

            Pourrait nous permettre de supprimer `vim-gutentags`.

            À propos de `entr`:
            https://news.ycombinator.com/item?id=13856623

#### insect

High precision scientific calculator with support for physical units.
<https://github.com/sharkdp/insect>

#### lnav

Log file navigator http://lnav.org

- <https://github.com/tstack/lnav>
- <https://www.youtube.com/watch?v=D9Tox1ysPXE>


                                               NOTE:

        Procédure d'installation:

                git clone https://github.com/tstack/lnav
                cd lnav
                ./autogen.sh
                ./configure
                make
                sudo make install

        OU

                sudo aptitude install lnav


                                     FIXME:

        Actuellement, la couleur de fond est noire.
        `lnav` utilise probablement  la couleur noire définie par  la palette du
        terminal.
        On  pourrait  peut-être  la  faire  passer en  blanc,  en  la  modifiant
        temporairement, le temps d'une invocation de `lnav`?
        (je doute mais bon...)

        Un bug report existe sur le sujet:

                https://github.com/tstack/lnav/issues/270

        Une PR est en préparation.  Elle pourrait résoudre le pb:

                https://github.com/tstack/lnav/pull/468

#### newsbeuter

    Description: text mode rss feed reader with podcast support newsbeuter is an innovative RSS feed
    reader  for  the  text  console.  It  supports  OPML  import/exports,  HTML  rendering,  podcast
    (podbeuter), offline reading,  searching and storing articles to your  filesystem, and many more
    features.

    Its user interface is coherent, easy to use, and might look common to users of mutt and slrn.

    On a sauvegardé la playlist de Gotbletu consacrée au programme (6 vidéos).

#### newspaper

    https://github.com/desmondhume/newspaper

            Read webpages in readability mode, inside your terminal.

            Inconvénient:

                    Sign up for Mercury and create an api key.

            Sera peut-être résolu dans le futur:

                    Replace Mercury with a readability library

#### noti

    https://github.com/variadico/noti

            Trigger notifications when a process completes.

#### pass

    https://www.passwordstore.org/

            the standard unix password manager

            À comparer à keepasscli.

#### polyglot

    https://github.com/agkozak/polyglot

            Dynamic color Git prompt for zsh, bash, ksh, mksh, pdksh, dash, and busybox sh

                                    196 sloc

#### progress

    https://github.com/Xfennec/progress

            Linux tool to show progress for cp, mv, dd, ... (formerly known as cv)

            sudo api progress

            Ne semble pas génial pour améliorer `cp`, car il n'affiche pas d'information concernant
            la progression globale d'une copie de plusieurs fichiers (progression par fichier uniquement).
            Et ne permet sans doute pas de reprendre la copie en cas d'interruption.
            Lui préférer `rsync`.

            En revanche, pour d'autres commandes (ex: `dd`) ...

#### rat

    Compose shell commands to build interactive terminal applications

    Rat  was developed  as part  of  an effort  to build  a  tig-like application  with very  little
    opinionated UI logic, delegating instead to the capabilities of shell commands like git log with
    its --pretty and --graph options.

    Shell commands  are executed and  the output is  captured and displayed  in pagers.  Configurable
    annotators parse  through the output,  adding annotations  that can be  acted upon to  run other
    shell commands.

    https://github.com/ericfreese/rat

#### rclone

    "rsync for cloud  storage" - Google Drive,  Amazon Drive, S3, Dropbox, Backblaze  B2, One Drive,
    Swift, Hubic, Cloudfiles, Google Cloud Storage, Yandex Files https://rclone.org

    https://github.com/ncw/rclone

#### rev

rev - reverse lines characterwise

See `man rev`.

####
#### rlwrap

<https://github.com/hanslub42/rlwrap>

    ┌──────────┬──────────────────────────────────────────────────────────────────────┐
    │ !foo Tab │ rappeler la dernière saisie commençant par `foo`                     │
    ├──────────┼──────────────────────────────────────────────────────────────────────┤
    │ C-r      │ chercher un pattern au sein de l'historique de saisie de la commande │
    └──────────┴──────────────────────────────────────────────────────────────────────┘

##### What are the limitations of this command?

rlwrap works only with an external command, not with a shell
builtin/alias/function.

---

    $ rlwrap read var
    rlwrap: error: Cannot execute read: No such file or directory~

You could try to run the builtin in a subshell:

    $ rlwrap sh -c 'read var'

But `var` would be lost as soon as the subshell exits.

`read` is a special case, because you don't necessarily need `rlwrap`.
You can use the `-e` flag, but it seems only available in bash (not in zsh).

---

    $ alias foo=checkinstall
    $ rlwrap foo
    rlwrap: error: Cannot execute foo: No such file or directory~
    # fails probably because an alias is only expanded when it's the first word.

    $ func() { checkinstall ;}
    rlwrap: error: Cannot execute func: No such file or directory~

You could run the alias/function from a subshell:

    $ rlwrap zsh -ic 'func'
                  │
                  └ make zsh source the zshrc where `func` is defined

But there would still be 2 issues:

   - you can't press C-c to kill the process started by the function/alias
     (probably consumed by rlwrap)

   - you can't alter the state of the current shell

     So for example, if the purpose of your function is to change the cwd, it will fail.
     Try with `$ fasd_cd -d -i` (alias `jj`).

##### ?

    complétion custom
    historique persistant
    édition de la ligne de commande
    filtres

            Fonctionnalités apportées par `rlwrap` à la commande qu'elle invoque.


    rlwrap [-options] <command> <args>

            Syntaxe basique.


    -f, --file file

       Split file  into words  and add  them to the  completion word  list.  This
       option can  be given more than  once, and adds to  the default completion
       list in $RLWRAP_HOME or /usr/share/rlwrap/completions.

-r, --remember
        Put all words seen on in- and output on the completion list.

With the -r and  -f options you can specify the list of  words which rlwrap will
use  as possible  completions,  taking them  from  a file  (-f  option) or  from
<command>'s standard  in/output.  rlwrap monitors <command>'s  terminal settings,
so that it can do the right thing when command asks for single keypresses or for
a password.  Commands that already  use readline will  always ask for  (and get)
single keypresses, which makes rlwrapping them rather pointless.  However, if one
uses  the  -a  option,  rlwrap  will  use its  own  line  editing  and  history.
Unforunately, in  this case, rlwrap cannot  detect whether <command> asks  for a
password.  This can be remedied by giving the password prompt (excluding trailing
space and possibly the first few letters) as an argument to the -a option.

* EXAMPLES:
Run netcat with command-line editing:

    rlwrap nc localhost 80

Run lprolog and use library1 and library2 to build a completion word list:

    rlwrap -f library1 -f library2 lprolog

Run  smbclient  (which  already  uses   readline),  add  all  input  and  output
to  completion  list, complete  local  filenames,  avoid showing  (and  storing)
passwords:

    rlwrap -cr -aPassword: smbclient '\\PEANUT\C'

* FILTERS

Filters are "plug-in" scripts that give you complete control over rlwrap's input
and output,  history and completion.  They are somewhat experimental,  and their
implementation and the  example filters still are of  slightly dubious ('alpha')
quality.

####
#### rsync

    TODO: lire `man rsync`

    Lire aussi:    ~/Dropbox/ODT/Software/Sauvegarde\ donnees.odt

    Se créer un alias `cpv` pour copier des fichiers / dossiers en ayant une barre de progression,
    pour pouvoir reprendre la copie en cas d'interruption, et pour ne pas avoir besoin de créer
    le dossier de destination (qd la destination est un dossier).  Le `v` dans `cpv` est pour “verbeux“.

    Se créer aussi un alias `mvv` pour déplacer des fichiers/dossiers, avec barre de progression.
    Encore une fois, on appellera `rsync`, mais en plus on supprimera la source une fois la copie
    effectuée.

    Attention, si la source est un dossier, soit on  écrit un chemin absolu ne se finissant pas par
    '/' auquel cas le  dossier source ainsi que son contenu est copié  vers la destination, soit on
    met bien un '/'  à la fin, auquel cas les fichiers/dossiers contenus  ds la source sont copiés
    mais pas le dossier source lui-même.

    L'option `--info=progress2` peut être utile.  La chercher dans le man.

    Lire les réponses à cette question:
    https://unix.stackexchange.com/questions/65077/is-it-possible-to-see-cp-speed-and-percent-copied


    La commande `gcp` (sudo api gcp) pourrait être une alternative à `cpv`.
    Toutefois, sur la page du projet, ils disent que c'est expérimental:

            WARNING gcp is  at an early stage  of development, and really experimental:  use at your
            own risks !

            https://github.com/petronny/gcp

    À quel point est-il fiable?

#### pv

    TODO: lire `man pv`
    pv - monitor the progress of data through a pipe

#### SC-IM

    https://github.com/andmarti1424/sc-im

            SC-IM     is     a      spreadsheet     program     that     is      based     on     SC
            (http://ibiblio.org/pub/Linux/apps/financial/spreadsheet/sc-7.16.tar.gz)   SC   original
            authors are James Gosling and Mark Weiser, and mods were later added by Chuck Martin.

#### sdcv

    https://askubuntu.com/questions/191125/is-there-an-offline-command-line-dictionary

    sudo aptitude install sdcv

#### socat

    http://freecode.com/projects/socat
    https://unix.stackexchange.com/search?tab=votes&q=socat

            Alternative plus puissante à `netcat`.

            man socat

#### streamlink

        https://github.com/streamlink/streamlink

        https://streamlink.github.io/

        https://www.youtube.com/watch?v=QtzB6ZqpfLc

CLI  for extracting  streams from  various websites  to a  video player  of your
choosing.

#### TMSU

    https://github.com/oniony/TMSU

            TMSU lets you  tags your files and then access  them through a nifty
            virtual filesystem from any other application.

            Comment from a redditor:

            People need  to understand the power  of tagging it is  the superior
            way of categorising.
            The subconsciousness usually comes up with  the same set of words as
            you used  to tag  it with  in the  first place  (when you  query and
            search your collection).
            I have thousands of bookmarks:

                    http://pinboard.in/u:dza

            I have  logs of work-related  solutions and avoid googling  the same
            results over and over again.
            I retain much more of what I learn.
            Tagging  and  bookmarking this  way  is  the  best thing  that  ever
            happened to  me to retain  the neverending flow of  information that
            developers get exposed to.
            I would recommend anyone doing it  and I would hope schools teach it
            some day.

#### translate-shell

    https://github.com/soimort/translate-shell/

            Command-line translator using Google Translate, Bing Translator, Yandex.Translate, etc.

            Cette page est très intéressante pour adopter un bon style qd on écrit du code awk:
            https://github.com/soimort/translate-shell/wiki/AWK-Style-Guide

            Cette page produit des traductions de grande qualité:
            https://demo-pnmt.systran.net/production#/translation


    git clone https://github.com/soimort/translate-shell/
    cd translate-shell
    git checkout Tab    (atm, la release la plus récente est 0.9.6.4)
    make
    sudo make install

            Procédure d'installation.


    trans -shell
    hello

            Affiche la prononciation, la définition, des synonymes et des exemples d'utilisation du mot “hello“.
            `-shell` lance `translate-shell` en mode interactif (REPL).

            Taper `:q` pour quitter.


    trans 'Un jour je me lèverai, et il fera beau!'
    trans -brief 'Un jour je me lèverai, et il fera beau!'

            Traduit une phrase en français vers l'anglais (langue système).
            Idem mais en moins verbeux.

#### visidata

A terminal interface for exploring and arranging tabular data.

<https://github.com/saulpw/visidata>
<https://www.visidata.org/docs/>
