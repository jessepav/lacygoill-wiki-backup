# checkinstall

L'installation d'un pgm  compilé via un `make install` crée  des fichiers un peu
partout dans le fs.
Très souvent, le  développeur du pgm n'ajoute pas de  règle `uninstall` dans son
Makefile, ce qui fait qu'on a aucun moyen simple pour le supprimer plus tard.
De plus, si un jour on souhaite installer  ce même pgm via un paquet, on recevra
des erreurs et le pgm compilé cessera de fonctionner.

`Checkinstall` résoud ces pbs.

Pour ce faire il  garde une trace des fichiers installés  par un `make install`,
crée un paquet deb (ou rpm) leur correspondant, et l'ajoute à la bdd des paquets
installés.
En  fait `checkinstall`  peut garder  une trace  (dans le  package manager)  des
fichiers installés  par n'importe  quelle installation en  cli (pas  juste `make
install`).

Un  autre avantage  de  `checkinstall` est  qu'il laisse  une  copie du  binaire
compilé dans le dossier de travail, qu'on peut réinstaller sur d'autres machines
sans avoir à recompiler à chaque fois.

Sources:
<https://help.ubuntu.com/community/CheckInstall>
<http://www.asic-linux.com.mx/~izto/checkinstall/>

    $ sudo aptitude install checkinstall

            Installe `checkinstall`.


    $ sudo checkinstall

            Installe un pgm compilé. (équivalent de make install)


    $ sudo checkinstall make foo

            Installe le pgm compilé foo (équivalent de make install foo), via la commande `dpkg -i foo`.


    $ dpkg -L foo

            Liste les fichiers de foo installés.


    $ sudo dpkg -r foo

            Supprime foo

Il existe d'autres outils facilitant la compilation d'un pgm:

   - auto-apt (installe automatiquement les dépendances manquantes à une compilation):

        https://help.ubuntu.com/community/AutoApt

   - autodeb (script expérimental qui fait le travail de checkinstall et auto-apt en même temps):

        https://wiki.ubuntu.com/AutoDeb

## The installation fails!  “trying to overwrite '...', which is also in package”

If the path of the file ends with `info/dir`, try to find a configuration option
allowing you to change the location of the file; it could be `--infodir`.

Example:

    $ ./configure --infodir=/usr/local/share
                    ^^^^^^^^^^^^^^^^^^^^^^^^
                    move the info file from `/usr/share/info` to `/usr/local/share/info`

---

Alternatively,  if you  know  that the  file  which the  package  was trying  to
overwrite  is not  important, you  can manually  install the  .deb generated  by
checkinstall:

    $ sudo dpkg -i --force-overwrite package.deb

Otherwise, you'll  have to uninstall  the conflicting package which  has already
installed the problematic file.

<https://askubuntu.com/q/176121/867754>

##
# How to find the configuration options which were used to compile a deb package?

In `/etc/apt/sources.list` or in a file in `/etc/apt/sources.list.d/`, uncomment
the `deb-src` line from which the source code of the package can be downloaded.

Then:

    $ sudo aptitude update
    $ mkdir /tmp/dir; cd /tmp/dir
    $ apt-get source <package_name>

If  `$  apt-cache policy`  reports  several  versions,  you  can target  one  in
particular with:

    $ apt-get source <package_name>=<version>

Example:

    $ apt-get source rxvt-unicode-256color

This will download the source code in a directory, as well as a few other files:

    rxvt-unicode-9.22/~
    rxvt-unicode_9.22-1ubuntu1~ppa1~x.debian.tar.xz~
    rxvt-unicode_9.22-1ubuntu1~ppa1~x.dsc~
    rxvt-unicode_9.22.orig.tar.bz2~

Finally, read the file `debian/rules`:

    $ vim rxvt-unicode-9.22/debian/rules

And find the right recipe (e.g. `conf-unicode-256color`):

    conf-unicode-256color:
            $(flagscommon) ./configure $(cfgcommon) \
                --enable-unicode3 \
                --enable-combining \
                --enable-xft \
                --enable-font-styles \
                --enable-256-color \
                --enable-pixbuf \
                --enable-transparency \
                --enable-fading \
                --enable-rxvt-scroll \
                --enable-next-scroll \
                --enable-xterm-scroll \
                --enable-perl \
                --enable-xim \
                --enable-iso14755 \
                --enable-mousewheel \
                --enable-slipwheeling \
                --enable-smart-resize \
                --enable-startup-notification \
                --with-term=rxvt-unicode-256color

---

Alternatively, you can try to read the buildlog on the web.

For example, for `zsh`, you would first visit:
<https://launchpad.net/ubuntu/+source/zsh>

Then, you would click on the button below “Latest upload”:
<https://launchpad.net/ubuntu/+source/zsh/5.5.1-1ubuntu3>

Then, on the button “amd64” in the section “Builds”:
<https://launchpad.net/ubuntu/+source/zsh/5.5.1-1ubuntu3/+build/16608683>

Finally, on the button “buildlog”:
<https://launchpadlibrarian.net/418666830/buildlog_ubuntu-disco-amd64.zsh_5.5.1-1ubuntu3_BUILDING.txt.gz>

##
# Todo

Document this: <https://wiki.debian.org/apt-src>

