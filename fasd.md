# How to jump to a directory via fasd from ranger?

    :j partial_dirname Enter

This requires the creation of a custom plugin:

    $ cat <<'EOF' >>~/.config/ranger/commands.py
    class j(Command):
        """
        :fasd

        Jump to directory using fasd
        """
        def execute(self):
            import subprocess
            arg = self.rest(1)
            if arg:
                directory = subprocess.check_output(["fasd", "-d"]+arg.split(), universal_newlines=True).strip()
                self.fm.cd(directory)
    EOF

Source: <https://github.com/ranger/ranger/wiki/Custom-Commands#visit-frequently-used-directories>

# How to make ranger log all the opened files, for fasd?

    $ cat <<'EOF' >~/.config/ranger/plugins/plugin_fasd_log.py
    import ranger.api

    old_hook_init = ranger.api.hook_init

    def hook_init(fm):
        def fasd_add():
            fm.execute_console("shell fasd --add '" + fm.thisfile.path + "'")
        fm.signal_bind('execute.before', fasd_add)
        return old_hook_init(fm)

    ranger.api.hook_init = hook_init
    EOF

<https://github.com/ranger/ranger/wiki/Integration-with-other-programs#fasd>

### How is it useful?

Without this plugin, the fasd aliases `o`, `m`, `v`... would never suggest you a
file opened from ranger.

##
# Installation

    $ git clone https://github.com/clvv/fasd
    $ sudo checkinstall

# Utilisation

    ┌────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
    │ f                  │ lister les fichiers OU les dossiers frécents (fréquents + récents)           │
    │ d                  │ f, a et d sont des alias prédéfinis (f = fasd -f, a = fasd -a, d = fasd -d)  │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ a Do lo            │ lister les fichiers ET les dossiers frécents dont le nom matche `Do` et `lo` │
    │                    │                                                                              │
    │                    │ `Do` et `lo` doivent être présents dans le nom du fichier ou du dossier      │
    │                    │ pas ailleurs dans un autre composant de leur chemin                          │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ f foo              │ lister les fichiers frécents dont le nom matche foo                          │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ f js$              │ lister les fichiers récents dont le nom se terminent par js                  │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ j foo              │ se rendre dans le dossier dont le nom matche matche foo                      │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ v foo              │ ouvrir avec vim le fichier le + frécent qui matche foo                       │
    │ f -e vim foo       │                                                                              │
    │                    │                                                                              │
    │ m foo              │ ouvrir avec mpv le fichier le + frécent qui matche foo                       │
    │ f -e mpv foo       │                                                                              │
    │                    │                                                                              │
    │ o foo              │ ouvrir avec le programme associé par défaut le fichier / dossier             │
    │ a -e xdg-open foo  │ le + frécent qui match foo                                                   │
    │                    │                                                                              │
    │ xdg-open $(sf foo) │ afficher les fichiers frécents qui match foo via un menu interactif,         │
    │                    │ puis ouvrir le fichier sélectionné                                           │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ ,foo,bar Tab       │ auto-compléter le fichier ou dossier le + frécent qui contient foo et bar    │
    │                    │ dans son nom                                                                 │
    │                    │                                                                              │
    │ f,foo,bar Tab      │ idem mais spécifiquement pour un fichier                                     │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ d,foo Tab          │ auto-compléter le dossier le + frécent contenant foo dans son chemin         │
    ├────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
    │ jj                 │ afficher un menu listant les dossiers les + frécents pour en sélectionner un │
    │                    │ et s'y rendre                                                                │
    └────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

TODO:

Il  semble que  la syntaxe  `,foo Tab`,  ait un  effet similaire  à la  fonction
`fasd-complete-f` (installée par zsh).
Par défaut, cette dernière est associée à `c-x c-f`.


FIXME:

En réalité, dans les syntaxes du tableau précédent, il semble que `foo` et `bar`
n'ont pas besoin d'être présents dans le nom du fichier/dossier de façon exacte:
leurs  caractères  peuvent  être  séparés par  2  caractères  (configurable  via
`$_FASD_FUZZY`).
Revoir le tableau pour tenir compte de l'aspect fuzzy du match.

##
# ?

Once this bug is fixed:

<https://github.com/junegunn/fzf/issues/1486>
<https://bugs.launchpad.net/ubuntu/+source/linux/+bug/1813873>

Have a look at this:

<https://github.com/andrewferrier/fzf-z>

It installs a command which should let you fuzzy search the output of fasd.
It's so brief (<100 sloc) that there's no need to install the script.
Just read and copy the interesting part.

