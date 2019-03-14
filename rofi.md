# Installation

<https://github.com/DaveDavenport/rofi/blob/next/INSTALL.md>

Install some dependencies:

    $ sudo aptitude install librsvg2-dev \
        libstartup-notification0-dev \
        libxcb-ewmh-dev \
        libxcb-icccm4-dev \
        libxcb-util-dev \
        libxcb-xinerama0-dev

Compile the `xutils-dev` dependency (can't be installed from the repo of Ubuntu 16.04):

    $ git clone https://github.com/Airblader/xcb-util-xrm/
    $ cd xcb-util-xrm
    # may not always work, because it tries to connect to some machine;
    # if it doesn't, try again in a few hours
    $ git submodule update --init
    # install dependency of `xutils-dev`
    $ sudo aptitude install xutils-dev
    $ ./autogen.sh
    $ make
    $ sudo checkinstall

Compile the `check` dependency (can't be installed from the repo of Ubuntu 16.04 because too old):

    $ git clone https://github.com/libcheck/check
    $ cd check
    $ autoreconf --install
    $ ./configure
    $ make
    $ make check
    $ sudo checkinstall
    $ sudo ldconfig

Install rofi:

    $ git clone https://github.com/DaveDavenport/rofi
    $ cd rofi/
    $ git checkout next
    $ git submodule update --init
    $ autoreconf -i
    $ mkdir build
    $ cd build
    $ ../configure
    $ make
    $ sudo checkinstall --pkgname rofi --provides rofi --pkgversion 1.5.2-1

##
# Rofi

    # gotbletu
    $ rofi -modi drun -show drun
    $ rofi -combi-mobi window,drun -show combi

---

Corrected examples from the manpage (they didn't work originally):

                           ┌ for some reason, our manpage has wrong quotes
                           │
    $ rofi -e "<span color='red'><b>This is still the end</b></span>" -markup

    # this command still doesn't work
    # the original command used `tty-pipe` and `out2html` which don't exist
    $ nmcli device | ansifilter -H | rofi -dmenu -markup-rows

---

What is rofi?

A window switcher, application launcher, run/ssh dialog and dmenu replacement.

---

Synopsis

    $ rofi [ -show mode ]|[ -dmenu ]|[ -e msg ] [ CONFIGURATION ]

---

Usage

rofi's main functionality is to assist in your workflow, allowing you to quickly
switch between windows, start applications or log into a remote machine via ssh.
There are different modi for different types of actions.

rofi can also function as (drop-in) replacement for dmenu(1).

---

   Running rofi

To launch rofi directly in a certain mode, specify a mode with:

    $ rofi -show <mode>

To show the run dialog:

    $ rofi -show run

---

   Emulating dmenu

rofi can emulate dmenu(1) (a dynamic menu for X) when launched with the -dmenu flag.

The website for dmenu can be found here <http://tools.suckless.org/dmenu/>.

rofi does not aim to be 100% compatible with dmenu.
There are simply too many different flavors of dmenu.
The idea  is that the basic  usage command-line flags are  obeyed, theme-related
flags are not.
Besides, rofi  offers some  extended features (like  multi-select, highlighting,
message bar, extra key bindings).

---

   Display Error message

rofi error dialog can also be called from the command line.

    $ rofi -e "my message"

Markup support can be enabled, see CONFIGURATION options.

##
# Dmenu
## Cli

    $ sudo aptitude install suckless-tools

Installe le paquet “suckless-tools“ contenant entre autres le pgm `dmenu`.

---

    $ dmenu_run
    $ dmenu_run -b
    $ dmenu_run -l 10
    $ dmenu_run -fn Monospace-20:normal
    $ dmenu_run -nb '#FF0000'

Affiche le lanceur dmenu:

   - en haut de l'écran
   - en bas  "
   - en présentant les entrées du menu verticalement (sur 10 lignes max)
   - avec la police d'écriture "Monospace" en taille 20 px.
   - avec le fond en rouge

---

    $ dmenu_run
    $ thunar ~/Downloads

Lance le pgm ’thunar’ et affiche le contenu du dossier ’~/Downloads’.

## Key Bindings

    C-a    C-e

Positionne le curseur au début/à la fin du texte saisi.


    C-h    C-d

            Backspace / Delete


    C-m

            Return


    C-b    C-f

            Déplace le curseur vers la gauche / droite.
            Permet de se déplacer au sein du texte saisi, mais aussi de naviguer parmi les entrées
            proposées par dmenu.


    C-n    C-p
    M-j    M-k

            Haut / Bas
            Permet de naviguer parmi les entrées dmenu, entrée par entrée.

            Page up / down
            Permet de naviguer parmi les entrées dmenu, page par page.


                                     NOTE:

            dmenu peut s'afficher verticalement via le flag `-l lines`.


    C-i    Tab

            Développe le texte saisi.


    C-y
    C-S-y

            Au sein du champ de saisie, colle:

                    - la sélection X (le texte mis en surbrillance dans l'application ayant le focus)
                    - le presse-papier X


    C-u    C-k
    C-w

            Supprime:

                    - depuis le curseur jusqu'au début / à la fin de la ligne
                    - le mot à gauche du curseur

