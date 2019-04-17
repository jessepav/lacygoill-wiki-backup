# Vim

    ftp://ftp.vim.org/pub/vim/patches/8.0/README

            ChangeLog pour la version 8.0 de Vim.


    $ which vim
    /usr/bin/vim~

    ls -l /usr/bin/vim
    /etc/alternatives/vim~

    ls -l /etc/alternatives/vim
    /usr/bin/vim.tiny~

    update-alternatives --config vim

            Ces commandes montrent qu'Ubuntu est préinstallé avec le paquet `vim-tiny`.
            Cette version de Vim  est compilée avec un minimum d'options.


    vim.tiny  --version
    :echo has('python')

            Ces commandes montrent que `vim.tiny` ne supportent  pas le langage de script python. En
            effet, dans la  sortie de la 1e  commande shell, les options 'python'  et 'python3' sont
            précédés du symbole -. De même, la sortie de la 2e commande Vim est 0, et non 1.

            Ceci fait qu'on ne peut pas utiliser de plugins nécessitant le support Python avec `vim.tiny`.


    sudo aptitude install vim-gtk

            vim-gtk est la version de Vim la plus complète sous Ubuntu.
            Elle contient le programme en GUI, et une version pour le terminal.
            Entre autres, elle supporte le copier-coller depuis / vers le presse-papier système,
            ainsi que Python.


    sudo update-alternatives --config vim

            Choisir `vim.gtk` dans les choix proposés.

            Informer le système des alternatives pour qu'il  mette à jour les liens symboliques et
            que le shell exécute cette version quand on tapera la commande `$ vim`.

    update-alternatives --get-selections | grep vim

            S'assurer que le système des alternatives n'utilise plus `vim.tiny` pour aucune alternative.


On peut aussi compiler Vim depuis les sources avec toutes les options désirées.
Procédure décrite dans `:h 90.1`.

    sudoedit /etc/apt/sources.list

            Dupliquer la 1e ligne correspondant au dépôt à partir duquel on peut installer Vim.
            Elle peut ressembler à:

                    deb http://ch.archive.ubuntu.com/ubuntu/ saucy main restricted


            Pour trouver la bonne ligne, on peut faire un `apt-cache policy …`, pour voir quels dépôts
            contiennent Vim. Sur la ligne dupliquée, remplacer `deb` par `deb-src`.

            Cette nouvelle ligne ajoute des dépôts contenant le code source des paquets binaires
            présents dans les dépôts de la ligne précédente.

            Si on a peur de faire une erreur dans ce fichier sensible, on peut faire un backup du
            fichier avant:

                    sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup

            Pour + d'infos:

                    https://help.ubuntu.com/community/Repositories/CommandLine


    sudo aptitude update

            Dl le code source présent dans le dépôt nouvellement ajouté.


    sudo aptitude build-dep vim

            Installer les dépendances nécessaires à la compilation d'un binaire vim.


    sudo aptitude install luajit libluajit-5.1-dev

            Installation des dépendances nécessaires pour que l'interface lua utilise luajit:

                    :echo &luadll
                    luadll=libluajit-5.1.so.2~


                                               NOTE:

            En cas de pb pour activer l'interface lua pendant la compilation de Vim, jeter un oeil
            au buildlog de pi-rho (pour trouver des dépendances manquantes ou des options à activer/configurer):

                    curl --compressed -Lo buildlog.txt.gz \
                    https://launchpad.net/~pi-rho/+archive/ubuntu/dev/+build/11804831/+files/buildlog_ubuntu-xenial-amd64.vim_2%3A8.0.0134-1ubuntu1~ppa1~x_BUILDING.txt.gz

                    vim buildlog.txt.gz


    git clone https://github.com/vim/vim.git
    cd vim
    make clean; make distclean
    git checkout master
    git pull
    cd src

            `make clean; make distclean` n'est nécessaire que si a déjà compilé Vim dans le passé.
            Entre autres, elle supprime le binaire vim produit localement dans src/.

            `git pull` permet de mettre à jour le code source.


    ./configure --enable-cscope \
                --enable-fail-if-missing \
                --enable-gui=gtk2 \
                --enable-luainterp=dynamic \
                --enable-multibyte \
                --enable-perlinterp=yes \
                --enable-python3interp=yes \
                --enable-pythoninterp=yes \
                --enable-rubyinterp=dynamic \
                --enable-terminal \
                --prefix=/usr/local \
                --with-compiledby=user \
                --with-features=huge \
                --with-luajit \
                --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu/ \
                --with-python3-config-dir=/usr/lib/python3.5/config-3.5m-x86_64-linux-gnu/

            NE PAS copier-coller cette commande directement dans le shell mais dans Vim, via
            `fc` ou `C-x C-e`. Ce faisant, on pourra plus facilement y apporter des modifications,
            et notamment changer les chemins vers les dossiers de configuration Python.

            Si on veut annuler la commande, quitter Vim en tapant `:cq[uit]`.
            `:cq` se terminera avec un code d'erreur, et ce faisant le shell n'exécutera pas le
            contenu du buffer.

            Ces options ont été trouvées à cette url:

                    https://github.com/Valloric/YouCompleteMe/wiki/Building-Vim-from-source

            On peut ajouter d'autres options.
            Pour voir les options dispo, taper `./configure --help`.

            On peut aussi exécuter `:h :ve`.
            L'aide affiche les différentes options dispo, et pour chacune d'elles la version minimale
            dans laquelle elle est incluse (si elle est dispo via `--with-features=xxx`) via un flag:

                    T   tiny
                    S   small
                    N   normal
                    B   big
                    H   huge
                    m   manually enabled or depends on other features

            On pourrait aussi décommenter les options désirées dans le fichier Makefile
            avant de taper ./configure.

            En ajoutant l'option `--with-features=huge`, on s'assure d'avoir le support de toutes les
            fonctionnalités précédées d'un flag qcq à l'exception de `m` (`T`, `S`, `N`, `B`, `H`).

                    --enable-multibyte

                            Ajoute le support des caractères multioctets (16 et 32 bits).

                    --enable-luainterp=dynamic
                    --enable-perlinterp=yes
                    --enable-pythoninterp=yes
                    --enable-python3interp=yes
                    --enable-rubyinterp=yes

                            Ajoute les interfaces lua/perl/python2/python3/ruby permettant d'utiliser
                            des plugins écrits dans ces langages.


                    --enable-fail-if-missing

                            Demande au script de configuration de s'arrêter s'il rencontre un problème
                            avec une interface.


                    --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu/

                            Configure le chemin vers le dossier de configuration de Python 2.7.

                            Compléter ou changer si besoin ce chemin, en utilisant la complétion `C-x C-f`.
                            Pour ce faire, introduire temporairement un espace après le symbole `=`.
                            Si la complétion `C-x C-f` ne donne rien, supprimer la dernière partie du chemin,
                            et retenter une complétion, pour que Vim nous propose des suggestions valides.

                    --with-python3-config-dir=/usr/lib/python3.4/config-3.4m-x86_64-linux-gnu/

                            Même chose que précédemment.

                    --with-compiledby=user

                            Qd on exécutera `:version`, la ligne `Compiled by` affichera le nom `user`.

                    --enable-gui=gtk2

                            Selon l'aide (:h gui-x11-compiling), cette option n'est pas nécessaire
                            car elle est activée par défaut:

                                    The GTK+ 2 GUI is built by default. Therefore, you usually don't
                                    need to pass any options  such as --enable-gui=gtk2 to configure
                                    and build that.

                            Si on utilise le serveur graphique X11, lors de la configuration, Vim
                            cherchera par ordre de priorité, les fichiers de la librairie graphique:

                                    - GTK+ 2/GTK+ 3
                                    - Motif
                                    - Athena

                            Si GTK+ 2 et GTK+ 3 sont installés, GTK+ 2 sera choisi en priorité, à moins qu'on
                            demande explicitement GTK+ 3 via l'option `--enable-gui=gtk3`.

                            Si on veut utiliser GTK+, le processus de configuration de Vim utilisera
                            `pkg-config` pour vérifier que la librairie GTK+ demandée est correctement
                            installée et utilisable.
                            Avant de lancer `./configure`, il vaut donc mieux vérifier que ce pgm est installé:

                                    pkg-config --modversion gtk+-2.0
                                    OU
                                    pkg-config --modversion gtk+-3.0

                            Si on obtient en sortie la version correcte de notre librairie GTK+,
                            on peut continuer. Autrement, il faudra installer/configurer `pkg-config` et GTK+.

                            Si on veut utiliser GTK+ 2, il faut installer une version supérieure à 2.2.
                            Si on veut utiliser GTK+ 3, l'aide recommende d'installer une version supérieure
                            à 3.10:

                                    we  recommend GTK+  3.10  or later  because  of its  substantial
                                    implementation changes in redraw done at that version.

                    --enable-cscope

                            Inclut l'interface cscope. cscope est un pgm décrit dans `:h cscope`.

                    --prefix=/usr/local

                            Les fichiers seront installés à l'intérieur de `/usr/local`.
                            Si on n'a pas les droits suffisants pour y installer des fichiers,
                            on peut remplacer `/usr/local` par un autre dossier tq `$HOME`.

                                    ./configure … --prefix=$HOME

                            Dans ce cas, il faut vérifier que le chemin `$HOME/bin` est présent
                            dans la variable d'environnement `$PATH`.
                            Si besoin, on peut modifier sa valeur dans `~/.profile`.

                            Pour + d'infos:

                                    http://askubuntu.com/a/60221
                                    http://mywiki.wooledge.org/DotFiles


                            Cette option est très importante si on veut pouvoir utiliser plusieurs Vim.
                            En effet, un Vim installé depuis les dépôts de la distrib utilisera
                            `/usr/share/vim` pour tous ses fichiers runtime.
                            Si on ne configure pas `--prefix`, qd on voudra installer notre Vim compilé,
                            il tentera lui-aussi d'utiliser `/usr/share/vim`, et `checkinstall` échouera
                            car il ne pourra pas écraser des fichiers système existants.

                            C'est pour éviter ce genre de problème qu'il faut toujours installer des programmes
                            compilés dans `/usr/local`.

                    --enable-terminal

                            Inclut le terminal intégré.


    make
    make test

            Lancer la compilation. Puis, tester le binaire généré.

            Au terme de la compilation, le binaire `src/vim` devrait être créé.
            `make test` permet de vérifier qu'elle s'est bien passée.

            La procédure de vérification consiste en une séquence de scripts chargés de tester
            que Vim fonctionne correctement.
            Vim démarrera de nombreuses fois, et différents types de textes et messages apparaîtront
            et disparaîtront rapidement.

            Si la compilation s'est bien passée, à la fin des tests, en scrollant en arrière
            pour relire les messages passés, on devrait voir qques pages en arrière, un message tq:

                    Executed 224 tests
                    Test results:
                    ALL DONE

            Si on obtient au contraire le message:

                    TEST FAILURE

            … ça signifie qu'au moins un test a échoué.
            S'il n'y a qu'un ou 2 messages à propos de tests échoués, Vim peut fonctionner, mais pas
            parfaitement.
            S'il y a bcp de messages d'erreur, ou que Vim n'arrive même pas à finir tous les tests,
            il faut recommencer la compilation en essayant de changer qch (installer/configurer un
            paquet, changer la configuration avant la compilation), ou chercher de l'aide sur internet.

            Pour qu'un maximum de tests réussissent, exécuter la commande en-dehors de tmux, dans un terminal
            en plein écran (un terminal trop petit peut empêcher certains scripts de se lancer).


    ./vim
    :version
    :echo has('lua')
    :echo has('perl')
    :echo has('python2')
    :echo has('python3')
    :echo has('ruby')

            Lance le binaire vim et vérifie qu'on a la bonne version de Vim, et qu'on a le support
            des interfaces pour les langages de script désirés.


    sudo aptitude install checkinstall

            Installer le paquet `checkinstall`.

            Il s'agit d'un pgm qui surveille une procédure d'installation (tq `make install`)
            et crée un paquet standard adapté à notre distribution. Il supporte entre autre les formats
            deb et rpm, pour les distros basés sur resp. debian et RHEL.

            On peut ensuite installer et supprimer ce paquet via notre gestionnaire de paquets système
            (dpkg pour debian).

            On utilisera `checkinstall` pour pouvoir supprimer plus facilement Vim plus tard.


    sudo checkinstall

            Installe Vim.

            Si on n'a pas `checkinstall`, exécuter `sudo make install` à la place.

            La procédure d'installation nous posera qques questions.

            Lorsqu'un menu apparaîtra, on pensera à changer la valeur de l'entrée 2, dont le nom
            est 'Name'. Le nom qu'on donnera au paquet (par défaut `src`, car on est dans un dossier `src`),
            sera celui qu'il faudra utiliser qd on voudra manipuler le paquet par la suite via `dpkg`.

            On pourra aussi changer la valeur des entrées 0, 1 et 11:

                    - 0 (Maintainer: donner son email)
                    - 1 (Summary: VIM compiled from source)
                    - 2 (Name: myvim)
                    - 11 (Provides: editor)

            Il est important de ne pas utiliser le nom `vim` pour notre paquet, si on souhaite installer
            et utiliser en parallèle le paquet `vim` des repos officiels.
            Autrement il y aura conflit, et qd on fera une màj, le paquet des repos supprimera notre paquet.


    update-alternatives-vim.sh

            Met à jour le système des alternatives, pour que l'OS utilise notre Vim compilé
            à chaque fois qu'il a le choix entre plusieurs éditeurs.


    dpkg -L vim
    sudo dpkg -r vim

            Liste les fichiers de Vim installés.
            Supprime Vim.

# Neovim
## How to install Neovim via a PPA?

        $ sudo add-apt-repository ppa:neovim-ppa/stable
        $ sudo aptitude update
        $ sudo aptitude install neovim

Source:

        https://launchpad.net/%7Eneovim-ppa/+archive/ubuntu/stable

##
## How to compile Neovim
### documentation

<https://github.com/neovim/neovim/wiki/Building-Neovim>

### install dependencies

    $ sudo aptitude install libtool libtool-bin autoconf automake cmake g++ pkg-config unzip

Source: <https://github.com/neovim/neovim/wiki/Building-Neovim#build-prerequisites>

### clone and update the Neovim repo

    $ git clone https://github.com/neovim/neovim

    $ git checkout master

    $ git pull

### clean the repo from the files generated during the previous compilation

    $ make clean && make distclean
                         │
                         └ removes, among other things, the `build/` directory

### compile

Use one of these commands:

    $ make

    $ make CMAKE_BUILD_TYPE=Release

    $ make CMAKE_BUILD_TYPE=RelWithDebInfo CMAKE_EXTRA_FLAGS=-DENABLE_JEMALLOC=OFF
                                           ├─────────────────────────────────────┘
                                           └ necessary to be able to use `checkinstall` later

<https://github.com/neovim/neovim/issues/2364#issuecomment-113966180>
<https://github.com/serverwentdown/env/commit/a05a31733443fcb0979fecf18f2aa8e9e2722c7c>

TODO:
What do we lose by disabling jemalloc?
Are we going to suffer from a noticeable performance hit?
I could  be wrong,  but after  reading this  (and because  Neovim is  probably a
single-threaded process) I don't think so:
<https://stackoverflow.com/a/1624744/9780968>

---

If a network connection fails during the compilation, the latter will also fail.
In that case, re-try a compilation (now or a bit later).

### check the version of the binary you've just compiled

    $ ./build/bin/nvim --version | grep ^Build

### test it

    $ LC_ALL=C make test
    $ make oldtest

The second command executes the Vim tests.
They need to be performed in a fullscreen terminal.
If you use Tmux, run the command in an unsplit window, or in zoomed pane.

### install it

    $ sudo checkinstall

If you didn't disable jemalloc during the compilation, the installation may fail.
In that case, run:

    $ sudo make install

### UNinstall it (optional)

    $ sudo rm /usr/local/bin/nvim

    $ sudo rm -r /usr/local/share/nvim/

### fix man plugin

By default, when you  run `$ man man`, the manpage is not  prettified like it is
when you run `:Man man` from a Neovim instance; let's fix that:

    $ sed -i.bak '/function! man#init_pager()/ {/endfunction/s//do <nomodeline> man BufReadCmd/}' /usr/local/share/nvim/runtime/autoload/man.vim

### ?

python integration

    $ python -m pip install --user --upgrade pynvim

    $ python3 -m pip install --user --upgrade pynvim

---

At the  moment, the first command  works, but `:CheckHealth` contains  a warning
message:

    ## Python 2 provider (optional)~
      - INFO: Disabled (g:loaded_python_provider=1).  This might be due to some previous error.~
      - INFO: `g:python_host_prog` is not set.  Searching for python2 in the environment.~
      - INFO: Multiple python2 executables found.  Set `g:python_host_prog` to avoid surprises.~
      - INFO: Executable: /usr/bin/python2~
      - INFO: Other python executable: /bin/python2~
      - INFO: Python version: 2.7.12~
      - INFO: pynvim version: 0.3.1~
      - WARNING: Could not contact PyPI to get latest version.~
      - ERROR: HTTP request failed: error: curl error with https://pypi.python.org/pypi/pynvim/json: 35~

It's due to a SSL handshaking which fails while `$ curl` tries to download this file:
<https://pypi.python.org/pypi/pynvim/json>.

See `$ man curl`, and search for `35` which is the given code error.

---

At the moment, the second command fails:

    Could not find a version that satisfies the requirement pynvim (from versions: )~
    No matching distribution found for pynvim~

Pass the `-vvv` argument to `pip` to get more information.

Also, `:CheckHealth` contains the following messages:

    - INFO: Using: g:python3_host_prog = "/usr/bin/python3"~
    - INFO: Executable: /usr/bin/python3~
    - ERROR: Command error (job=9, exit code 1): `'/usr/bin/python3' -c 'import sys; sys.path.remove(""); import pynvim; print(pynvim.__file__)'` (in '~/wiki/vim')~
    Output: Traceback (most recent call last):  File "<string>", line 1, in <module>ImportError: No module named 'pynvim'~
    Stderr: Traceback (most recent call last):  File "<string>", line 1, in <module>ImportError: No module named 'pynvim'~
    - INFO: Python version: 3.5.2~
    - INFO: pynvim version: unable to load pynvim Python module~
    - ERROR: Importing "neovim" failed.~
    - ADVICE:~
      - Reinstall "pynvim" and optionally "neovim" packages.~
          pip3 uninstall pynvim neovim~
          pip3 install pynvim~
          pip3 install neovim # only if needed by third-party software~
    - ERROR: pynvim is not installed.~
    Error: unable to load pynvim Python module~
    - ADVICE:~
      - Run in shell: pip3 install pynvim~
    - WARNING: Could not contact PyPI to get latest version.~
    - ERROR: HTTP request failed: error: curl error with https://pypi.python.org/pypi/pynvim/json: 35~

See `:h provider-python`, and:

<https://github.com/pypa/pip/issues/3776>
<https://github.com/neovim/neovim/issues/3396>
<https://github.com/neovim/neovim/wiki/FAQ>
<https://github.com/zchee/deoplete-jedi/wiki/Setting-up-Python-for-Neovim>

Update:

`python[3] -m pip install --user --upgrade pynvim` fails because of `Error 104 connection reset by peer`.
Is our IP blacklisted?

Solution:

Go to `https://pypi.org/` and look for the package `pynvim`.
Atm, you'll find this url:

<https://pypi.org/project/pynvim/>

Click on `Homepage` and you'll get this url:

<https://github.com/neovim/pynvim>

Clone the repo:

    $ git clone https://github.com/neovim/pynvim

Then install the package manually:

    $ cd pynvim
    $ python3 -m pip install --user --upgrade .

The installation may fail because of a missing dependency, `msgpack`.

> Could not find a version that satisfies the requirement msgpack>=0.5.0 (from pynvim==0.3.1) (from versions: )
> No matching distribution found for msgpack>=0.5.0 (from pynvim==0.3.1)

In that case repeat the process:

    https://pypi.org/project/msgpack/
    https://github.com/msgpack/msgpack
    $ git clone https://github.com/msgpack/msgpack
    $ cd msgpack
    $ python3 -m pip install --user --upgrade .
    $ cd ../pynvim
    $ python3 -m pip install --user --upgrade .

Note that we often can't access pypi.org...
But sometimes we can...
If  you can't,  try to  look for  the package  directly on  github (hoping  it's
developed there, and not somewhere else, like gitlab or bitbucket).
Or, use the tor browser (it works!).
Or, use a webproxy (like https://proxysite.com/).

Alternatively, maybe you could try to contact another mirror:

    $ python3 -m pip install --user --upgrade -i http://e.pypi.python.org/simple pynvim
                                              ├────────────────────────────────┘
                                              └ https://stackoverflow.com/a/13878827/9780968

Or, use `$ pip` behind a proxy:

    $ export https_proxy=http://web-proxy.mydomain.com
    $ python3 -m pip install --user --upgrade pynvim

Source: <https://stackoverflow.com/a/19962913/9780968>

### ?

    ## Ruby provider (optional)~
      - INFO: Ruby: ruby 2.3.1p112 (2016-04-26) [x86_64-linux-gnu]~
      - WARNING: `neovim-ruby-host` not found.~
        - ADVICE:~
          - Run `gem install neovim` to ensure the neovim RubyGem is installed.~
          - Run `gem environment` to ensure the gem bin directory is in $PATH.~
          - If you are using rvm/rbenv/chruby, try "rehashing".~
          - See :help |g:ruby_host_prog| for non-standard gem installations.~

              https://github.com/rubygems/rubygems.org/issues/1760~
              http://www.fastly-debug.com/~

        ## Node.js provider (optional)~
          - INFO: Node.js: v4.2.6~
          - WARNING: Neovim node.js host does not support v4.2.6~

    $ gem install neovim

    ERROR:  Could not find a valid gem 'neovim' (>= 0), here is why:~
              Unable to download data from https://rubygems.org/ - Errno::ECONNRESET: Connection reset by peer - SSL_connect (https://api.rubygems.org/specs.4.8.gz)~

### ?

    $ sudo update-alternatives --install /usr/bin/vi vi /usr/bin/nvim 60
    $ sudo update-alternatives --config vi
    $ sudo update-alternatives --install /usr/bin/vim vim /usr/bin/nvim 60
    $ sudo update-alternatives --config vim
    $ sudo update-alternatives --install /usr/bin/editor editor /usr/bin/nvim 60
    $ sudo update-alternatives --config editor

Use Neovim for some (or all) of the editor alternatives.

### ?

<https://github.com/mhinz/neovim-remote>
<https://hkupty.github.io/2016/Ditching-TMUX/>

