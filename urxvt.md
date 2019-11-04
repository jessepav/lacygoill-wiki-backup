# Installation
## From PPA

    $ sudo add-apt-repository ppa:pi-rho/dev
    $ sudo aptitude update

    $ sudo aptitude install rxvt-unicode-256color

## By Compiling
### clone the repo

    $ cd ~/Vcs/
    $ git clone https://github.com/exg/rxvt-unicode

You could also have run:

    $ sudo aptitude install cvs
    $ cvs -z3 -d :pserver:anonymous@cvs.schmorp.de/schmorpforge co rxvt-unicode

See: <http://software.schmorp.de/pkg/rxvt-unicode.html>.

But working with cvs is harder, in part because it doesn't have the concept of a
global commit id: <https://stackoverflow.com/questions/24487317/cvs-checkout-specific-commit>

So, how do you bisect an issue?
How do you checkout an old version of the code?
How do you get the current version of the project?

### download dependencies

    $ cd rxvt-unicode
    $ cvs -z3 -d :pserver:anonymous@cvs.schmorp.de/schmorpforge co libev
    $ cvs -z3 -d :pserver:anonymous@cvs.schmorp.de/schmorpforge co libptytty

If you're not installing the dependencies for  the first time, and you just want
to update them, try to run `$ cvs update`.

See these links for more info:
<https://unix.stackexchange.com/a/302887/289772>
<http://software.schmorp.de/pkg/libev.html>
<http://software.schmorp.de/pkg/libptytty.html>

### apply patches

    $ cd ~/Vcs/rxvt-unicode/src

    $ patch -b <~/.config/urxvt/patches/00-font-width-fix.patch ; \
      patch -b <~/.config/urxvt/patches/00-256resources.patch ; \
      patch -b <~/.config/urxvt/patches/00-line-spacing-fix.patch ; \
      patch -b <~/.config/urxvt/patches/01_app-defaults.diff ; \
      patch -b <~/.config/urxvt/patches/02_use_dejavu.diff

    $ cd ../doc

    $ patch -b <~/.config/urxvt/patches/07_rgb_location.diff ; \
      patch -b <~/.config/urxvt/patches/12_hyphen_minus_sign.diff

    $ patch -b <~/.config/urxvt/patches/11_fix_lexgrog.diff

The last patch raises this error:

    patching file rxvt.1.pod~
    patching file rxvt.7.pod~
    can't find file to patch at input line 42~
    Perhaps you should have used the -p or --strip option?~
    The text leading up to this was:~
    --------------------------~
    |Index: pkg-urxvt/src/perl/selection-popup~
    |===================================================================~
    |--- pkg-urxvt.orig/src/perl/selection-popup    2013-02-12 12:12:29.227728891 -0500~
    |+++ pkg-urxvt/src/perl/selection-popup 2013-03-20 17:34:07.049845487 -0400~
    --------------------------~
    File to patch:~

Enter this:

    /home/user/Vcs/rxvt-unicode/src/perl/selection-popup
          ^^^^
          replace with your user name

---

The `-b` option passed to `patch(1)` creates a backup of a file before patching it.
The backup file bears the extension `.orig`.

---

If you want to reverse the effect of a patch, use the `-R` option.

Example:

    $ patch -R <~/.config/urxvt/patches/00-font-width-fix.patch
            ^^

---

Not all patches are important, but be sure to apply `00-line-spacing-fix.patch`.
It fixes an issue where all characters have excessive whitespace in between each
other.

If you don't want to apply this patch, then you will have to add this setting to
`~/.Xresources`:

    URxvt.letterSpace: -2

You may need to tweak the value depending on your machine/environment (-1, -5, ...).

The result may not be always as good as the patch.
For more info, see:
<https://bugs.launchpad.net/ubuntu/+source/rxvt-unicode/+bug/309792>
<https://unix.stackexchange.com/questions/118641/font-rendering-issue-in-urxvt-too-much-space-between-characters>

### configure

    $ cd ~/Vcs/rxvt-unicode

    $ ./configure \
    --enable-256-color \
    --enable-combining \
    --enable-fading \
    --enable-font-styles \
    --enable-iso14755 \
    --enable-keepscrolling \
    --enable-lastlog \
    --enable-mousewheel \
    --enable-next-scroll \
    --enable-perl \
    --enable-pixbuf \
    --enable-pointer-blank \
    --enable-rxvt-scroll \
    --enable-selectionscrolling \
    --enable-slipwheeling \
    --enable-smart-resize \
    --enable-startup-notification \
    --enable-transparency \
    --enable-unicode3 \
    --enable-utmp \
    --enable-warnings \
    --enable-wtmp \
    --enable-xft \
    --enable-xim \
    --enable-xterm-scroll \
    --with-term=rxvt-unicode-256color

You can find which options ubuntu devs use here:
<https://launchpadlibrarian.net/411350604/buildlog_ubuntu-disco-amd64.rxvt-unicode_9.22-6_BUILDING.txt.gz>
<https://launchpadlibrarian.net/268049601/buildlog_ubuntu-xenial-amd64.rxvt-unicode_9.22-1ubuntu1~ppa1~x_BUILDING.txt.gz>

This last link was tricky to find.

First, visit:                    <https://launchpad.net/~pi-rho>
Click on “dev”:                  <https://launchpad.net/~pi-rho/+archive/ubuntu/dev>
Click on “View package details”: <https://launchpad.net/~pi-rho/+archive/ubuntu/dev/+sourcepub/6596151/+listing-archive-extra>
Click on “amd64”:                <https://launchpad.net/~pi-rho/+archive/ubuntu/dev/+build/10174196>
Click on “buildlog”:             <https://launchpadlibrarian.net/268049601/buildlog_ubuntu-xenial-amd64.rxvt-unicode_9.22-1ubuntu1~ppa1~x_BUILDING.txt.gz>

Or you can download the source code:

    $ apt-get source rxvt-unicode=<optional version>

Then, read `rxvt-unicode-*/debian/rules`.
And look for the `conf-unicode-256color` recipe.

---

Note that `--enable-everything` does *not* include `--enable-256-color` (see README.configure)

### compile

    $ make

In case you try to run the binary without installing it:

    $ ./src/rxvt

It may crash (`malloc()` memory corruption).
The issue has been introduced in this commit:
<https://github.com/exg/rxvt-unicode/commit/d3fc23b4a4ac48a1185985cad764477e951da688>

You can still install the binary with `checkinstall(8)`, and it will work fine.

### install

    $ sudo checkinstall --pkgname 'rxvt-unicode-256color' --pkgversion "${$(git describe --tags --abbrev=0)##*-}" --spec /dev/null -y

##
# Configuration

    urxvt --help 2>&1 | grep font | less
                 │
                 └── `urxvt` écrit son aide dans son flux d'erreur (au lieu du terminal)
                     donc, il faut rediriger le flux d'erreur vers le pipe

            Chercher tous les noms d'options en lien avec la police d'écriture.

            Cette commande est utile pour découvrir des options intéressantes,
            à propos d'un sujet donné.


    xrdb -query

            Affiche les ressources de la bdd du serveur X.


    ┌─ X server Resource DataBase utility
    │
    xrdb ~/.Xresources

            Commande à exécuter à chaque fois qu'on change le fichier de conf
            `~/.Xresources`, si on veut voir le résultat sans avoir à relancer X.

            Elle charge  des ressources dans  la bdd  de X, qui  s'appliquent à
            tous les programmes qui affichent qch via X.


                                     NOTE:

            Une commande similaire est exécutée automatiquement au démarrage,
            via un ou plusieurs fichiers systèmes:

                    ag xrdb /etc/

            Atm, le seul fichier qui semble exécuter automatiquement `xrdb` sur
            ma machine est:

                    /etc/xdg/xfce4/xinitrc

            Il ajoute plusieurs fichiers  à `$XRESOURCES`, puis exécute `xrdb`
            sur l'ensemble:

                    cat /dev/null $XRESOURCES | xrdb -merge -


                                     TODO:

            Si  on utilise  des commentaires  commençant par  `!`, et  que l'un
            d'eux  contient  un  single  quote:

                    !  it's  a  comment

            … le préprocesseur C utilisé par `xrdb` se plaint.
            Pour + d'infos, lire notre alias `reload_xres` défini dans `~/.shrc`.

            Actuellement,   notre   `~/.Xresources`   contient   ce   genre   de
            commentaires.   Notre alias  custom évite  le problème  lors d'une
            utilisation interactive de `xrdb`.
            Mais quid du démarrage de la session X: y'a-t-il un risque de bugs louches?

            Peut-être que  les avertissements du préprocesseur  C n'ont aucune
            influence sur ce que `xrdb` exécute.

# Copier-coller

    simple ou double-clic gauche  >  shift + clic gauche

            On peut sélectionner une région de  texte via la souris en faisant
            un simple/double clic gauche sur son  1er mot, puis en répétant le
            même raccourci + shift sur son dernier.

            Fonctionne aussi via des triples clic pour sélectionner une région
            linewise.

            Dans tmux, il faut désactiver l'option 'mouse':

                    pfx m  ⇔  set-option -g mouse off


    middle clic souris

            En  appuyant  sur  la  molette  de la  souris,  on  colle  le  texte
            actuellement sélectionné après le curseur.

            La position du curseur n'est pas modifié par la sélection.

# Documentation

                      http://cvs.schmorp.de/rxvt-unicode/doc/rxvt.7.pod
    http://pod.tst.eu/http://cvs.schmorp.de/rxvt-unicode/doc/rxvt.7.pod

    Gentoo:   https://wiki.gentoo.org/wiki/Rxvt-unicode
    ArchWiki: https://wiki.archlinux.org/index.php/rxvt-unicode
    IRC:      irc.freenode.net #rxvt-unicode
    Tuto:     http://artisan.karma-lab.net/installer-et-parametrer-urxvt

##
# Utilisation

    ctrl + clic droit    les 2 maintenus enfoncés

            Ouvre un menu contextuel.
            Dans la plupart des émulateurs, un simple clic droit suffit.

            Ce menu permet, entre autres, de copier la sélection vers le presse-papier système,
            ou d'évaluer une expression perl.


    ctrl + clic molette    les 2 maintenus enfoncés

            Affiche les options dispo. Celles activées sont préfixées par un astérisque.
            On peut toggle l'état d'une option, en déplaçant la souris (tout en maintenant ctrl+clic molette),
            pour sélectionner une option, puis en relâchant la molette.

# Voca

    root window

            La fenêtre du fond d'écran (d'après le livre `From bash to zsh`).

##
# Todo

    https://github.com/muennich/urxvt-perls

            Extensions intéressantes.


    https://github.com/regnarg/urxvt-config-reload

            This plugin allows you to reload  urxvt configuration at run time by
            sending SIGHUP to the urxvt process.


    man urxvtperl

            To read to learn how to write urxvt extensions.

