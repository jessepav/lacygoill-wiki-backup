# How to view the values of all the current settings?

Press `?s`.

# How to get the path to the config directory used by the current ranger instance?

From ranger, run:

    :eval fm.notify(ranger.args.confdir, True)

##
# What's a prefix argument?

Suppose you bind a custom command to `<key>`, and you press `123<key>`:
`123` is a prefix argument.

# How to uninstall ranger?

If you used `pip`, then run:

    $ python3 -m pip uninstall ranger-fm

##
# How to get more information when an error occurs?

Restart ranger in debug mode, by passing it the `-d` or `--debug` option:

    $ ranger -d

Whenever an error occurs, ranger will exit and print a full traceback.
The  default behavior  is to  merely  print the  name  of the  exception in  the
statusbar/log and try to keep running.

Do *not* use this option by default, only for debugging purposes.
Indeed, ranger will crash for any kind  of error, regardless of its severity, to
dump a stack trace on the terminal.

# How to start ranger with no custom configuration?

Restart ranger in clean mode, by passing it the `-c` or `--clean` option:

    $ ranger -c

ranger will not access  or create any configuration files nor  will it leave any
traces on your system.
This  is useful  when  your configuration  is  broken, when  you  want to  avoid
clutter, etc.

##
# I'm selecting a file; how to
## reset its rights to 123?

Press `123=`.

## add the right to execute it for the owner?

Press `+x`.

## remove the right to write it from the others?

Press `-ow`.

## add the right to read it for the group?

Press `+gr`.

##
##
##
# AIDE

    :help → m                                       dans ranger

    :Man /home/user/GitRepos/ranger/doc/ranger.1    dans Vim
    :Man /home/user/GitRepos/ranger/doc/rifle.1

# BUGS

Open an audio/video file from ranger, then try quit ranger.

    Not quitting: Tasks in progress: Use `quit!` to force quit

---

    api w3m-img
    vim config/rc.conf    →    set preview_images true
    ranger --copy-config=scope

            Procédure pour activer la prévisualisation d'images. Elle est décrite ici:

                    https://github.com/ranger/ranger/wiki/Image-Previews

            La 3e étape n'est pas nécessaire si on a déjà un fichier `config/scope.sh`.

            Ne fonctionne que dans certains terminaux (xterm, rxvt-unicode, st), et en-dehors de tmux.
            Trouver un moyen de faire marcher ça dans notre terminal (guake ou autre + tmux).
            Ou trouver qch d'équivalent.


    sudo api w3m-img ffmpegthumbnailer
    ranger --copy-config=scope
    vim config/scope.sh    →    uncomment 3 lines:

                                video/*)
                                    ffmpegthumbnailer -i "${FILE_PATH}" -o "${IMAGE_CACHE_PATH}" -s 0 && exit 6
                                    exit 1;;

            Procédure pour activer la prévisualisation de vidéos. Elle est décrite ici:

                    https://github.com/ranger/ranger/wiki/Video-Previews

            La 2e étape n'est pas nécessaire si on a déjà un fichier `config/scope.sh`.

            La prévisualisation repose sur le programme `ffmpegthumbnailer`.
            Malheureusement ça ne marche pas, il n'y a aucune prévisualisation qd on sélectionne
            un fichier vidéo dans ranger.

            Le problème semble venir de ffmpegthumbnailer.
            En effet, ranger obtient une prévisualisation en exécutant une commande du genre:

                    ffmpegthumbnailer -i video_file -o output_image -s 0

            Qd on exécute cette commande dans le terminal, on obtient un message d'erreur similaire à:

                    Error: basic_string::substr: __pos (which is 18446744073709551615) > this->size() (which is 4)

            J'ai purgé `ffmpegthumbnailer` et tenté d'installer une version plus récente, en compilant
            depuis la source. La procédure de compilation est sommairement décrite ici:

                    https://github.com/dirkvdb/ffmpegthumbnailer/blob/master/INSTALL

            Je suis parvenu à compiler en installant quelques dépendances, et en utilisant
            `checkinstall` plutôt que `make` (pour pouvoir supprimer ensuite via `dpkg -r ffmpegthumbnailer`):

                    sudo aptitude install cmake libavcodec-dev libavformat-dev libavfilter-dev
                    cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_GIO=ON -DENABLE_THUMBNAILER=ON .
                    make
                    sudo checkinstall

            Un autre problème se pose, car ce nouveau `ffmpegthumbnailer` ne sait pas où trouver une
            bibliothèque dont il a besoin quand on l'exécute.
            Pour le lui apprendre, il semble qu'on ait 2 possibilités:

                    sudo ldconfig

                        OU

                    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/libffmpegthumbnailer.so.4
                    export LD_LIBRARY_PATH

            Plus d'infos sur le sujet ici:

                    https://stackoverflow.com/questions/480764/linux-error-while-loading-shared-libraries-cannot-open-shared-object-file-no-s

            Mais même avec cette version plus récente de `ffmpegthumbnailer`, la génération de vignette
            continue d'échouer avec le même message d'erreur qu'auparavant.
            Trouver une solution.


# CONFIGURATION

Pour ajouter le support des VCS (glyphes git), dans `~/.config/ranger/rc.conf` remplacer `set vcs_aware false` par:
`setlocal path=~/home/user/GitRepos/ vcs_aware true`

Source: https://github.com/hut/ranger/wiki/VCS-integratio://github.com/hut/ranger/wiki/VCS-integration

Pour afficher / masquer par défaut la preview des fichiers et des dossiers, faire passer set preview_files
et set preview_directories à true ou false dans `~/.config/ranger/rc.conf`.

Pour afficher la preview des images telles quelles, il faut installer w3m, faire passer set preview_images à true
et utiliser un émulateur de terminal capable d'exécuter la fonction w3mimgdisplay (pour le moment j'ai trouvé que xterm qui la supporte).

Si les bookmarks ne sont pas sauvegardés entre 2 sessions, vérifier que `~/.config/ranger/bookmarks` nous appartient bien (et non pas à root).

rifle est un script (?) qui se charge de lancer les bons programmes externes pour ouvrir les fichiers (ex: feh pour voir ses images).
Sa config est dans : `~/.config/ranger/rifle.conf`.

`~/.config/ranger/scope.sh` est un script qui gère la preview des fichiers.
Pour qu'il puisse correctement afficher la preview des images en ascii, il faut installer le paquet caca-utils
(qui contient la fonction img2txt).

# INSTALLATION

Try to install ranger as a debian package.
This way, you'll have the manpages (ranger(1), rifle(1)).

---

atm préférer la version de git à  celle des dépôts officiels, car elle résoud un
bug qui empêche l'affichage de certaines aides :

        https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=711510

Instructions d'installation : http://ranger.nongnu.org/download.html

Official User Guide : https://github.com/hut/ranger/wiki/Official-user-guide

    cd && git clone git://git.savannah.nongnu.org/ranger.git    cloner ranger
    cd ranger
    git checkout stable                                         utiliser la version stable
    git pull                                                    mettre à jour ranger
    ranger --copy-config=all                                    crée une config par défaut


    sudo aptitude install atool

            Recommends: bash-completion, binutils, bzip2, file, lbzip2 | pbzip2, unzip, zip
            Suggests: arc, arj, cpio, lzip, lzma, lzop, nomarch, p7zip, rar, rpm, unace,
                    unalz, unrar, xz-utils
            Description:

            tool for  managing file archives of  various types atool  is a script for  managing file
            archives  of various  types  (tar, tar+gzip,  zip  etc). The  main  command is  probably
            aunpack, extracting files  from an archive. It overcomes the  dreaded "multiple files in
            archive root" problem by first extracting to a unique subdirectory, and then moving back
            the  files if  possible. aunpack  also prevents  local files  from being  overwritten by
            mistake.  Other commands  provided  are  apack (create  archives),  als  (list files  in
            archives), and acat (extract files to standard out).


            # avoid password prompt by providing empty password
            ext 7z, has 7z = 7z -p l "$@" | "$PAGER"
            # This requires atool
            ext ace|ar|arc|bz2?|cab|cpio|cpt|deb|dgc|dmg|gz,  has als     = als -- "$@" | "$PAGER"
            ext iso|jar|msi|pkg|rar|shar|tar|tgz|xar|xpi|xz|zip, has als     = als -- "$@" | "$PAGER"
            ext 7z|ace|ar|arc|bz2?|cab|cpio|cpt|deb|dgc|dmg|gz,  has aunpack = aunpack -- "$@"
            ext iso|jar|msi|pkg|rar|shar|tar|tgz|xar|xpi|xz|zip, has aunpack = aunpack -- "$@"

# RACCOURCIS

    C-c         annuler une commande (ex: :rename)

    C-n         open new tab
    C-w, q      close tab
    tab         switch to next tab

    ' '             cycle between current dir and last marked dir that we went to
    t               ajoute un astérisque comme repère visuel
    "<char>         ajoute un caractère comme repère visuel

    :flat <n>       tous les fichiers du dossier courant et de ses sous-dossiers
                    (jusqu'à <n> niveaux d'imbrication) sont affichés simultanément

                    si <n> = -1, absoluments tout est affiché... gaffe...
                    si <n> = 0, affichage normal par défaut

    dc              calcule la taille du dossier sélectionné
    du              calcule la taille du dossier courant et de tout ce qu'il contient

    E               lancer le file explorer de Vim au niveau du dossier courant

    f               chercher dans le dossier courant et ses sous-dossiers

    m<x>            placer le bookmark <x> sur le répertoire courant
    um<x>           supprimer le bookmark <x>

    Mi Mf Mp        en plus des noms, affiche le type de données / les tailles / les permissions de tous les éléments

    os oS            trier les fichiers par taille

    r               choisir le pgm pour ouvrir le fichier
    R               reload current working dir
    S               open shell in current dir
    V               sélectionner une suite de fichiers / dossiers
    uv              annuler la sélection

    ya / da         ajouter l'élément sélectionné au buffer "copier" / "couper" ( a = add)
    uy / ud         vider le buffer "copier" / "coller" (u = undo ?)

    zf <str>        filtre ; n'affiche que les fichiers / dossiers contenant <str> dans leur nom
    zh              toggle hidden files
    zp              toggle preview files
    zP              toggle preview dirs

# Commands.md
Here's a place for your custom commands!

Add the commands you want into `~/.config/ranger/commands.py`. Note: You always need to import the `Command` class at the top of your `commands.py`:

```python
from ranger.api.commands import Command
```

## upload files

This command may be used for quickly uploading a file to a server via scp.

```python
class up(Command):
    def execute(self):
        if self.arg(1):
            scpcmd = ["scp", "-r"]
            scpcmd.extend([f.realpath for f in self.fm.thistab.get_selection()])
            scpcmd.append(self.arg(1))
            self.fm.execute_command(scpcmd)
            self.fm.notify("Uploaded!")


    def tab(self):
        import os.path
        try:
            import paramiko
        except ImportError:
            """paramiko not installed"""
            return

        try:
            with open(os.path.expanduser("~/.ssh/config")) as file:
                paraconf = paramiko.SSHConfig()
                paraconf.parse(file)
        except IOError:
            """cant open ssh config"""
            return

        hosts = paraconf.get_hostnames()
        # remove any wildcard host settings since they're not real servers
        hosts.discard("*")
        return (self.start(1) + host + ":" for host in hosts)
```

## Visit frequently used directories

This command uses [fasd][2] to jump to a frequently visited directory with a given substring of its path.

```python
class fasd(Command):
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
```

See also [Integration with other programs][3] for logging opened files to fasd.

## mkcd (mkdir + cd)

```python
class mkcd(Command):
    """
    :mkcd <dirname>

    Creates a directory with the name <dirname> and enters it.
    """

    def execute(self):
        from os.path import join, expanduser, lexists
        from os import makedirs
        import re

        dirname = join(self.fm.thisdir.path, expanduser(self.rest(1)))
        if not lexists(dirname):
            makedirs(dirname)

            match = re.search('^/|^~[^/]*/', dirname)
            if match:
                self.fm.cd(match.group(0))
                dirname = dirname[match.end(0):]

            for m in re.finditer('[^/]+', dirname):
                s = m.group(0)
                if s == '..' or (s.startswith('.') and not self.fm.settings['show_hidden']):
                    self.fm.cd(s)
                else:
                    ## We force ranger to load content before calling `scout`.
                    self.fm.thisdir.load_content(schedule=False)
                    self.fm.execute_console('scout -ae ^{}$'.format(s))
        else:
            self.fm.notify("file/directory exists!", bad=True)
```

## Toggle flat

```python
class toggle_flat(Command):
    """
    :toggle_flat

    Flattens or unflattens the directory view.
    """

    def execute(self):
        if self.fm.thisdir.flat == 0:
            self.fm.thisdir.unload()
            self.fm.thisdir.flat = -1
            self.fm.thisdir.load_content()
        else:
            self.fm.thisdir.unload()
            self.fm.thisdir.flat = 0
            self.fm.thisdir.load_content()
```


## fzf integration

```python
class fzf_select(Command):
    """
    :fzf_select

    Find a file using fzf.

    With a prefix argument select only directories.

    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        import os.path
        if self.quantifier:
            # match only directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -type d -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        else:
            # match files and directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        fzf = self.fm.execute_command(command, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.decode('utf-8').rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)
```
Now, simply bind this function to a key: `map <C-f> fzf_select`

## tmsu integration
```python
class tmsu_tag(Command):
    """:tmsu_tag

    Tags the current file with tmsu
    """

    def execute(self):
        cf = self.fm.thisfile

        self.fm.run("tmsu tag \"{0}\" {1}".format(cf.basename, self.rest(1)))
```

## OSX - Reveal selected files in Finder

The following command is useful if you need to select files and drag-and-drop them. For example, as an attachment to gmail message composer. Simply select the files, and run the command:

```python
class show_files_in_finder(Command):
    """
    :show_files_in_finder

    Present selected files in finder
    """

    def execute(self):
        import subprocess
        files = ",".join(['"{0}" as POSIX file'.format(file.path) for file in self.fm.thistab.get_selection()])
        reveal_script = "tell application \"Finder\" to reveal {{{0}}}".format(files)
        activate_script = "tell application \"Finder\" to set frontmost to true"
        script = "osascript -e '{0}' -e '{1}'".format(reveal_script, activate_script)
        self.fm.notify(script)
        subprocess.check_output(["osascript", "-e", reveal_script, "-e", activate_script])
```

or

```python
class show_files_in_finder(Command):
    """
    :show_files_in_finder

    Present selected files in finder
    """

    def execute(self):
        self.fm.run('open .', flags='f')

```

## the_silver_searcher (Ag) integration [Not production ready]
Use Ag to search files and display results in ranger's pager

```python
class ag(Command):
    """:ag 'regex'
    Looks for a string in all marked paths or current dir
    """
    editor = os.getenv('EDITOR') or 'vim'
    acmd = 'ag --smart-case --group --color --hidden'  # --search-zip
    qarg = re.compile(r"""^(".*"|'.*')$""")
    patterns = []
    # THINK:USE: set_clipboard on each direct ':ag' search? So I could find in vim easily

    def _sel(self):
        d = self.fm.thisdir
        if d.marked_items:
            return [f.relative_path for f in d.marked_items]
        # WARN: permanently hidden files like .* are searched anyways
        #   << BUG: files skipped in .agignore are grep'ed being added on cmdline
        if d.temporary_filter and d.files_all and (len(d.files_all) != len(d.files)):
            return [f.relative_path for f in d.files]
        return []

    def _arg(self, i=1):
        if self.rest(i):
            ag.patterns.append(self.rest(i))
        return ag.patterns[-1] if ag.patterns else ''

    def _quot(self, patt):
        return patt if ag.qarg.match(patt) else shell_quote(patt)

    def _bare(self, patt):
        return patt[1:-1] if ag.qarg.match(patt) else patt

    def _aug_vim(self, iarg, comm='Ag'):
        if self.arg(iarg) == '-Q':
            self.shift()
            comm = 'sil AgSet def.e.literal 1|' + comm
        # patt = self._quot(self._arg(iarg))
        patt = self._arg(iarg)  # No need to quote in new ag.vim
        # FIXME:(add support)  'AgPaths' + self._sel()
        cmd = ' '.join([comm, patt])
        cmdl = [ag.editor, '-c', cmd, '-c', 'only']
        return (cmdl, '')

    def _aug_sh(self, iarg, flags=[]):
        cmdl = ag.acmd.split() + flags
        if iarg == 1:
            import shlex
            cmdl += shlex.split(self.rest(iarg))
        else:
            # NOTE: only allowed switches
            opt = self.arg(iarg)
            while opt in ['-Q', '-w']:
                self.shift()
                cmdl.append(opt)
                opt = self.arg(iarg)
            # TODO: save -Q/-w into ag.patterns =NEED rewrite plugin to join _aug*()
            patt = self._bare(self._arg(iarg))  # THINK? use shlex.split() also/instead
            cmdl.append(patt)
        if '-g' not in flags:
            cmdl += self._sel()
        return (cmdl, '-p')

    def _choose(self):
        if self.arg(1) == '-v':
            return self._aug_vim(2, 'Ag')
        elif self.arg(1) == '-g':
            return self._aug_vim(2, 'sil AgView grp|Ag')
        elif self.arg(1) == '-l':
            return self._aug_sh(2, ['--files-with-matches', '--count'])
        elif self.arg(1) == '-p':  # paths
            return self._aug_sh(2, ['-g'])
        elif self.arg(1) == '-f':
            return self._aug_sh(2)
        elif self.arg(1) == '-r':
            return self._aug_sh(2, ['--files-with-matches'])
        else:
            return self._aug_sh(1)

    def _catch(self, cmd):
        from subprocess import check_output, CalledProcessError
        try:
            out = check_output(cmd)
        except CalledProcessError:
            return None
        else:
            return out[:-1].decode('utf-8').splitlines()

    # DEV
    # NOTE: regex becomes very big for big dirs
    # BAD: flat ignores 'filter' for nested dirs
    def _filter(self, lst, thisdir):
        # filter /^rel_dir/ on lst
        # get leftmost path elements
        # make regex '^' + '|'.join(re.escape(nm)) + '$'
        thisdir.temporary_filter = re.compile(file_with_matches)
        thisdir.refilter()

        for f in thisdir.files_all:
            if f.is_directory:
                # DEV: each time filter-out one level of files from lst
                self._filter(lst, f)

    def execute(self):
        cmd, flags = self._choose()
        # self.fm.notify(cmd)
        # TODO:ENH: cmd may be [..] -- no need to shell_escape
        if self.arg(1) != '-r':
            self.fm.execute_command(cmd, flags=flags)
        else:
            self._filter(self._catch(cmd))

    def tab(self):
        # BAD:(:ag <prev_patt>) when input alias ':agv' and then <Tab>
        #   <= EXPL: aliases expanded before parsing cmdline
        cmd = self.arg(0)
        flg = self.arg(1)
        if flg[0] == '-' and flg[1] in 'flvgprw':
            cmd += ' ' + flg
        return ['{} {}'.format(cmd, p) for p in reversed(ag.patterns)]
```

NOTE: You may need to add the following line to your commands.py:
```python
import re
```
# Common-Changes.md
# Changing the editor or pager

By default, ranger uses `vim` as the editor and `less` as the pager.  You can change those by setting the environment variables `$EDITOR` and `$PAGER`.  This can be done in a number of ways.  The easiest is adding these lines to your shell rc file, e.g. `~/.bashrc`:

```sh
export EDITOR=nano
export PAGER=more
```
# Custom-linemodes.md
It is fairly easy to implement a custom linemode (see [this section][1] of the ranger guide for an explanation what is a linemode).


Let's try to implement a linemode displaying a filename with a comment (added via `:meta`) on the left side and the file owner on the right. So it would look like this:

    my_video.mp4 (sweet cats)                             john

Each linemode is a class implementing the `LinemodeBase` interface, so we start with:

```Python
class MyLinemode(LinemodeBase):
```

A linemode must have a name:

```Python
    name = "awesome_linemode"
```

...then we specify that we will be using the metadata (see: `:meta`) and `ranger` should load it:

```Python
    uses_metadata = True
```

We may use `required_metadata` list to specify which metadata tags are necessary for our linemode to make sense (it will fall back to the default linemode if any of them is not set):

```Python
    required_metadata = ["comment"]
```

Now we will define two methods, one for each side of the line. Each takes two arguments: a file object (`FSObject`) and an object with the metadata.

```Python
    def filetitle(self, file, metadata):
        return file.relative_path + " (" + metadata.comment + ")"
    def infostring(self, file, metadata):
        return file.user
```

It's almost over. What's left is registering the brand new linemode:

```Python
register_linemode(MyLinemode)
```

To summarize:

```Python
import ranger.api
import ranger.core.linemode

@ranger.api.register_linemode     # It may be used as a decorator too!
class MyLinemode(ranger.core.linemode.LinemodeBase):
    name = "awesome_linemode"

    uses_metadata = True
    required_metadata = ["comment"]

    def filetitle(self, file, metadata):
        return file.relative_path + " (" + metadata.comment + ")"

    def infostring(self, file, metadata):
        return file.user
```

To actually see it in action, you need to tag some files with the "comment" tag using `:meta` and set an appropriate linemode:

    :meta comment sweet cats
    :linemode awesome_linemode

You may also set the default linemode in your `rc.conf` with `:default_linemode`.
# FAQ:-Frequently-Asked-Questions.md
## Why is my text editor opening a new file "--" instead of the file I want?

Your editor of choice (EoC) likely does not support the `--` flag.

The `--` flag tells most programs that everything following it is a filename. This is as security feature to prevent accidental application of flags when they are not wanted _(Example: `$EDITOR -- -V` will open a new file named `-V`)_.

If your EoC is opening `--` as a file, you can either change rifle.conf to not use `--`, or you could submit a patch to your EoC to support use of the `--` flag. It is highly recommended to submit a patch to your EoC.

**[BEWARE]** Should you choose to edit your rifle.conf, know that you are putting yourself at some level of risk of unforeseen bugs with rifle/ranger!

### Editing rifle.conf
The configuration option you are looking for is in the rifle.conf file in the config directory (default is `~/.config/ranger/rifle.conf`).

The relevant lines in rifle.conf are:  
line 86: `mime ^text, label editor = $EDITOR -- "$@"`  
line 88: `!mime ^text, label editor, ext xml|json|csv|tex|py|pl|rb|js|sh|php = $EDITOR -- "$@"`  
line 207: `label editor, !mime ^text, !ext xml|json|csv|tex|py|pl|rb|js|sh|php = $EDITOR -- "$@"`  
(the lines may vary a bit)

Remove the `--` from those lines, and restart ranger!
# Home.md
#### Welcome to the ranger wiki!

A good place to start is the [[official user guide|Official User Guide]] and [[FAQ|FAQ: Frequently Asked Questions]] pages.  Then there are some places for exchanging ranger customizations:

* [[Custom key bindings|Keybindings]]
* [[Custom linemodes|Custom linemodes]]
* [[Custom commands and program integrations|Commands]]
* [[Non-command integrations with other programs|Integration with other programs]]
* [[Ranger Plugins|Plugins]]

More guides:

* [[Common Changes]]
* [[Enabling Video Previews|Video Previews]] and [[Image Previews]]
* [[Signals and Hooks|Signals and Hooks]]
* [[Enabling git/mercurial/bazaar integration|VCS integration]]

If you upgraded ranger and something stopped working, check:

* [[Upgrading problems|Upgrading]]

See also:

* [[ArchWiki page|https://wiki.archlinux.org/index.php/Ranger]]
* [[dotshare.it page with some color schemes|http://dotshare.it/category/fms/ranger/]]
# Image-Previews.md
Since 1.6.0, ranger can preview images in full color.  This works by calling a program named `w3mimgdisplay` that's included in the [w3m web browser][4], which draws images directly into the terminal.

If you use [iTerm2][5], a Mac OS X terminal replacement, you can enable a method that takes advantage of the built-in drawing functionality so you won't need w3m.

Steps to enable it:

### With w3mimgdisplay

* Get a compatible terminal.  Terminals that are known to work are *rxvt-unicode*, *xterm* and *st* (at least since st 0.6).
* install w3m with the image drawing feature.  On Arch Linux, the package is called "w3m", on Debian it's "w3m-img".
* Add the line `set preview_images true` to your `~/.config/ranger/rc.conf`.
* In the most recent git version, you also need to get the `scope.sh` configuration file by running `ranger --copy-config=scope`
* Restart ranger and navigate to an image file. \o/

### With urxvt

The image preview methods `urxvt` and `urxvt_full` can be used with the urxvt terminal and are typically more reliable. They use a special escape sequence to change the background of the terminal in order to render the image.

* Run urxvt with pixbuf support (some operating systems ship it without pixbuf support, but for example ArchLinux has an AUR package called `rxvt-unicode-pixbuf` which should work)
* Add the line `set preview_images true` to your `~/.config/ranger/rc.conf`.
* Add the line `set preview_images_method urxvt` to your `~/.config/ranger/rc.conf`. You can also choose `urxvt_full` if you would like the image to fill the whole terminal rather than just the preview pane.
* Restart ranger and navigate to an image file. \o/

### With iTerm2

**NOTE: You need at least iTerm2 version 2.9 for the image preview feature to work.**

* Add the line `set preview_images true` to your `~/.config/ranger/rc.conf`.
* Add the line `set preview_images_method iterm2` to your `~/.config/ranger/rc.conf`.
* Restart ranger and navigate to an image file. \o/

### With mpv

**NOTE: You need at least mpv version 0.25 for the below method to work.**

**NOTE: Requires modification of ranger itself.**

The mpv image preview method allows ranger to control an external client for viewing media. The benefit of this approach is that both images and videos share a single, separate window. Some changes are planned, so this method is not included in ranger yet. If you would like to make the changes youself, here are the steps. The rest of this section assumes `$ranger` is the location of your copy of ranger, not your configuration.

* Add the following lines to the end of `$ranger/ext/img_display.py`:
```
import subprocess
import json
import atexit
import socket
from pathlib import Path

import logging
from logging import info
import traceback

class MPVImageDisplayer(ImageDisplayer):
    """Implementation of ImageDisplayer using mpv, a general media viewer.
    Opens media in a separate X window.

    mpv 0.25+ needs to be installed for this to work.
    """

    def _send_command(self, path, sock):

        message = '{"command": ["raw","loadfile",%s]}\n' % json.dumps(path)
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(str(sock))
        info('-> ' + message)
        s.send(message.encode())
        message = s.recv(1024).decode()
        info('<- ' + message)

    def _launch_mpv(self, path, sock):

        proc = Popen([
            * os.environ.get("MPV", "mpv").split(),
            "--no-terminal",
            "--force-window",
            "--input-ipc-server=" + str(sock),
            "--image-display-duration=inf",
            "--loop-file=inf",
            "--no-osc",
            "--no-input-default-bindings",
            "--keep-open",
            "--idle",
            "--",
            path,
        ])

        @atexit.register
        def cleanup():
            proc.terminate()
            sock.unlink()

    def draw(self, path, start_x, start_y, width, height):

        path = os.path.abspath(path)
        cache = Path(os.environ.get("XDG_CACHE_HOME", "~/.cache")).expanduser()
        cache = cache / "ranger"
        cache.mkdir(exist_ok=True)
        sock = cache / "image-slave.sock"

        try:
            self._send_command(path, sock)
        except (ConnectionRefusedError, FileNotFoundError):
            info('LAUNCHING ' + path)
            self._launch_mpv(path, sock)
        except Exception as e:
            logging.exception(traceback.format_exc())
            sys.exit(1)
        info('SUCCESS')
```
* Edit `$ranger/core/fm.py` then search for `ImageDisplayer()` and make the following changes:
```
elif self.settings.preview_images_method == "urxvt-full":
    return URXVTImageFSDisplayer()
elif self.settings.preview_images_method == "mpv":          # add this line
    return MPVImageDisplayer()                              # add this line
else:
    return ImageDisplayer()
```
* Ensure the following lines appear in your `~/.config/ranger/rc.conf`:
```
set preview_images true
set use_preview_script true
set preview_script ~/path/to/your/scope.sh     # or whatever your preview script is
```
* Restart ranger and navigate to an image file. \o/


If you want mpv to support common image viewing features, see [this gist][6] for a sample mpv configuration.


### Troubleshooting

If the w3m program doesn't show images itself, then ranger won't show them either in the w3mimgdisplay mode. Try `w3m xkcd.com` for example.

Sometimes black stripes are drawn over the images when using w3mimgdisplay.  This is due to the unreliable drawing mechanism, and for some people it helps to set the option `draw_borders` to true.

Sometimes it helps trying a different terminal emulator or a different displaying method.

w3mimgdisplay appears not to work with compositing managers like xcompmgr.

If your image previews broke after upgrading ranger's git after september 2015, you need to update scope.sh for image previews to work.  See https://github.com/hut/ranger/wiki/Upgrading#image-previews-stopped-working-after-updating-ranger-git

### ASCII previews

Oldschool ASCII art previews can be enabled like this:

* install libcaca (or whatever package provides the "img2txt" executable)
* get a current scope.sh config, e.g. with `ranger --copy-config=scope`
* The following `~/.config/ranger/rc.conf` settings are also essential, though the default rc.conf already includes them, so usually you don't need to change anything.
```
set preview_images false
set use_preview_script true
set preview_script ~/path/to/your/scope.sh
```

`set preview_images false` is necessary because otherwise ranger might use full color previews instead.
# Integration-with-other-programs.md
# Bulk

Bulk is a command similar to, and more powerful than `:bulkrename`: https://github.com/alexherbo2/bulk

# fasd

[fasd][7] is an amazing utility that allow to quickly jump to recent files / directories.
You can log files opened in ranger to fasd by creating ~/.config/ranger/plugins/plugin_fasd_log.py containing :

```
import ranger.api

old_hook_init = ranger.api.hook_init

def hook_init(fm):
    def fasd_add():
        fm.execute_console("shell fasd --add '" + fm.thisfile.path + "'")
    fm.signal_bind('execute.before', fasd_add)
    return old_hook_init(fm)

ranger.api.hook_init = hook_init
```

See also [Visit frequently used directories][8] for using fasd inside ranger.

# vim / neovim

The following plugin let you use ranger in place of the builtin `netrw`. It's a nice alternative to the popular `NERDTree`: https://github.com/francoiscabrol/ranger.vim

# kakoune

This text editor has commands to quickly open ranger in Tmux panes or X11 windows: https://github.com/mawww/kakoune/blob/master/rc/extra/ranger.kak
# Keybindings.md
Here is a place for useful custom key bindings. Share what you got!

### Quick editing rc.conf

`map X chain shell vim -p ~/.config/ranger/rc.conf %rangerdir/config/rc.conf; source ~/.config/ranger/rc.conf`

Explanation: By starting the binding with a "chain" command, we can supply multiple commands separated by ";".  The first command opens vim with the custom rc.conf and the default rc.conf as a reference in two separate tabs.  When you close vim, the second command will source the default config, so that your changes take effect in the current ranger instance.

### Smart "cw"
`map cw eval fm.execute_console("bulkrename") if fm.thisdir.marked_items else fm.open_console("rename ")`

When typing cw, usually the console is opened with the content "rename " for quick renaming.  But ranger includes a feature for quickly renaming multiple files at once, the so-called "bulkrename" command.  The mapping above will check whether you have any selected files in the current directory and pick the appropriate renaming method.

### Go to currently played song in MPD
`map go eval from ranger.ext.spawn import spawn; fm.select_file("/media/external/music/" + spawn("mpc -f %file% | head -1"))`

This command moves to the song that is currently played in MPD, the music player daemon.  You have to specify the root directory of MPD in the command.  Here is a version that extracts the root directory from /etc/mpd.conf, but it may be unreliable:

`map go eval from ranger.ext.spawn import spawn; fm.select_file(spawn("grep ^music_directory /etc/mpd.conf | grep -oP '(?<=\").*(?=\")'").strip() + "/" + spawn("mpc -f %file% | head -1"))`

### tmux-related commands

* `map ef eval fm.run("tmux splitw -h 'rifle \"" + fm.thisfile.basename + "\"'")`
* `map ev eval fm.run("tmux splitw -v 'rifle \"" + fm.thisfile.basename + "\"'")`
* `map ew eval fm.run("tmux new-window 'rifle \"" + fm.thisfile.basename + "\"'")`

The above three commands open the highlighted file with whatever you've told rifle to use to open it- useful if you want to open a file while still using your current ranger instance.
# Official-user-guide.md
## Introduction

This guide will teach you how to efficiently use `ranger`.

## User interface

The main window consists of three panels by default (it's called [Miller columns][9] by the way):

-   the middle one with the contents of the current directory,
-   the left one shows the parent directory, with the current directory
    highlighted,
-   the right one serves various previews; I will tell you more about it
    later.

If you're familiar with [vim][10], you should feel right at home with
`ranger's` UI conventions. `ranger` uses the "hjkl" keys for navigation
and borrows many idioms from `vim`. For example: "yy" (copy line in
`vim`) copies a file, "pp" pastes it and "dd" prepares a file to be
moved (by being pasted somewhere else later, like with copy). The more
complex functions may be called from the command-line invoked with ":"
(a colon).

The current file's attributes may be seen at the bottom and the current
directory path may be seen at the top.

### For the `mc` users

If you're familiar with `mc` ([Midnight Commander][11]) the first thing you
may notice is the lack of the second panel for the file navigation. It
may seem like a limitation but in most cases people use only one panel
at a time. `ranger` allows you to create new tabs (like in a web
browser) and switch between them with either `Alt-number` or `Tab`. If
you open just two tabs, `ranger's` tabs effectively behave just like
`mc's` panels. And you can even open more if such need arises.

## Movement

The basic movement keys are inspired by `vim`: "jk" moves up and down,
"l" enters the selected directory or opens a file and "h" returns to the
parent directory. Many other navigation keys known from `vim` work too,
feel free to try them.

## Configuration files

`ranger` uses 4 main configuration files:

-   `commands.py` contains various functions' implementation, written in
    Python, used to modify `ranger's` behavior,
-   `rc.conf` is used for setting various options and binding the keys
    to functions,
-   `rifle.conf` decides which program to use for opening which file,
-   `scope.sh` is a shell script used to generate the previews for
    various file types.

It's quite common to use `ranger --copy-config=all` to copy the
default config files to `~/.config/ranger` and modify them there. Be
aware that for `rc.conf` and `commands.py`, ranger reads *both* the global *and*
the user's config (in that order). It allows the user to maintain only a small
config which sets only the things not set in the default one.  For `scope.sh`
and `rifle.conf`, ranger reads *either* the users *or* the global config.

The best practice is to only add the options/keybindings you actually want to
change to your rc.conf, rather than to have a complete copy of the default
rc.conf.  This eliminates the need to update your config manually and gives you
the benefits from new options/keybindings of future ranger versions.
If you want to keep the full rc.conf though, you may want to set the
environment variable `RANGER_LOAD_DEFAULT_RC` to `FALSE` to avoid loading
*both* the default and your own rc.conf.  In this case you have to update your
config manually though.

## File operations

To copy a file, highlight it, press "yy" to mark it for copying
(analogously to copying a line in `vim` with "yy"), then navigate to a
target directory (or switch a tab if you decided to do it the "`mc`
way") and then press "pp" to paste it (again, almost like in `vim`).

Moving a file differs very little from copying it: just use "dd" instead
of "yy" at the beginning.

To copy/move multiple files, just mark them with `Space` then use
"dd/yy". If you want to operate on multiple files stored in different
directories, you may use "ya/da" to add them to the list of files to be
copied/moved before pasting them.

(Note that the copy/cut buffers can be used for other operations as
well, by using the "%c" macro in your commands. For example, adding
files to the cut/copy buffer using "ya"/"da" then using the `:shell -w
printf %c | xargs rm` command allows you to delete multiple files in
multiple directories. Remember to clear the buffer once you're done
using "ud"/"uy".)

If you'd like to copy files from one ranger instance to another, type
`:save_copy_buffer` in one and `:load_copy_buffer` in the other ranger
instance.  This method can also be used to export a list of files.  They are
saved in the file `~/.config/ranger/copy_buffer`.

## Tabs

If you're working in more than one directory at a time -- and you most
likely do -- you may create tabs for each directory to which you want to
have a quick access. The tabs are numbered. To switch to the N-th tab,
press `Alt-N`, where `N` is the tab number. If such tab does not exist
yet, it will be created. To close a tab, press "q" (if you close the
last tab, the entire `ranger` process will close).

## Previews

I've mentioned the previews in the right column of `ranger`. I believe
they deserve a separate section in this guide.

All file previews are supplied by the `scope.sh` config file. It is a
regular shell script and it's behavior is documented in detail inside of
it.

### Image previews

A very special case of the previews are the image previews. Yes,
`ranger` can display images in your terminal. It uses an utility
supplied with the `w3m` web browser (sometimes packaged in a separate
package, like `w3m-img` in Debian). While it's reliable most of the
time, please be aware that it is a hack and may behave very strangely at
times.

Since the commit `9b73aeb` (merged around 10 October 2016) `ranger` supports reliable image previews in `urxvt` and `iTerm2` terminal emulators. To enable it, set `preview_images_method` to either `urxvt` or `iTerm2`. Please refer to the documentation for further information. For the `urxvt` method to work on Arch Linux it might be needed to install the `rxvt-unicode-pixbuf` package instead of the regular `rxvt-unicode`.

### Custom image previews

In the recent versions of `ranger`, the mechanism of the image previews
was extended and generalized. When calling `scope.sh`, `ranger` sets the
`$cached` environmental variable containing a unique path to a file
where the image preview may be generated if needed. `scope.sh` may then
save an image to that path and exit with the exitcode "6" (documented
inside `scope.sh`, may be a subject to some changes) to tell `ranger` to
use it. Simply saying: if you can convert a file to a jpg, `ranger` is
able to show a graphical preview for it. Videos, PDFs, all sort of
files.

## Rifle

`rifle` is a powerful smart file opener bundled with `ranger`. It
tries to guess with what program it should open a given file based on
its MIME type, extension, the available programs and a few other
factors. It is configured with the `rifle.conf` file. It is used by
`ranger` internally but may be used as a standalone program too.

## More tips
### File tagging

By pressing "t" you may mark a file with an asterisk ("\*"). It is
persistent and will be there until you remove it manually. It may be
used for example for marking the already read e-books, or files that
need some action.

You can actually mark files with almost any other character besides the
asterisk. Pressing a quotation mark (' " ') followed by any other
character marks the file with that character.

The tags may also be used to automatically enable some options in
certain directories. Refer to the documentation of the `:setintag`
command.

### Metadata

Storing the file metadata is a brand new feature of `ranger`. It may
be used to add arbitrary key-value data to any file. Calling `:meta
title a very interesting title` will set the tag "title" of the
current file to "a very interesting title".

`:meta` is most commonly used in conjunction with `:linemode`. The
built-in linemodes are bound to "M" followed by some letter. At the
moment of writing this guide, there are 3 built-in linemodes:

-   `filename`: no metadata, the default mode of ranger,
-   `permissions`: file permissions are displayed next to the files,
-   `metatitle`: see below.

The last line mode, `metatitle`, is extremely handy for organizing all
sorts of documents: books, movies, pictures and more. It displays the
files based on their metadata. The current format is:
`[[year - ]title] alignment [authors]`. Bracketed content is ignored
if empty. The `title` field is mandatory for this to work. To define
a custom linemode, please refer to this page:
[[Custom linemodes|Custom linemodes]].

`:meta` stores the metadata in the ".metadata.json" file for each
directory in which it is used.

### Directory flattening

If you're browsing a moderetely nested directory tree, you may find
`:flat` useful. It allows to browse a directory tree in a linear
fashion: all the files up to the n-th level are shown together. It's a
bit hard to explain so just call `:flat 1` and observe what happens.
The argument is the maximum number of directories to flatten. Pass -1
for no limit (use with caution!) and 0 to disable `:flat`.

### Bulk renaming

`ranger` supports bulk file renaming with the `:bulkrename` command.
Mark the files that you want to rename and call `:bulkrename`. It
should open a file containing a list of these files in your text
editor (determined with `rifle`). You may freely change the names in
that file. When you are done, save the file and close the editor.
`ranger` will show you a preview of what will happen in a few moments.

`:bulkrename` works great with `:flat`!
# Plugins.md
Here's a place for your custom plugins!

Add the plugins to the directory `~/.config/ranger/plugins/`.

## git annex plugin
https://github.com/matze/ranger-annex
## plugin directory diff
https://github.com/alex8866/eranger/blob/master/ranger/config/plugins/plugin_direcory_diff.py

## Ranger Devicons plugin ( file icon glyphs for ranger)
https://github.com/alexanderjeurissen/ranger_devicons
# Shell-aliases.md
Creating `r.shell` script somewhere in your PATH (like at `/usr/local/bin`) will allow you to expand your shell aliases inside `:shell ...` command. It's certainly useful, when you have several hundreds of them.

Script `r.shell`:

    #!/bin/bash

    # EXPL: simplify when r.shell -c $SHELL
    if [[ $# == 2 && $1 == -c && ($2 == $SHELL || $2 == '$SHELL') ]]
    then shift 2; fi

    # EXPL: overwrite when SHELL=r.shell
    [[ -x /usr/bin/zsh ]] \
    && export SHELL=/usr/bin/zsh \
    || export SHELL=/usr/bin/bash

    # USE: Interactive shell
    (($#)) || exec ${SHELL:?}

    # USE: Cmdline populated with aliases
    [[ $1 != -c ]] || shift
    exec ${SHELL:?} -c '
    (( $(id -u) )) || HOME=/home/${SUDO_USER:-${USER:-${USERNAME:?}}}
    source ~/.shell/aliases
    [[ ${SHELL:?} =~ zsh$ ]] && setopt aliases || shopt -s expand_aliases
    eval "$@"
    ' "$0" "$@"

Of course, you need to change way to launch ranger, as I don't recommend exporting SHELL globally:

    alias r.ranger='SHELL=/usr/local/bin/r.shell ranger'
    $ r.ranger
# Signals-and-Hooks.org
* Hooks

There are a few functions/methods in ranger's code specifically designed to be overwritten, or "monkey patched" by the user:

  * ranger.api.hook_init
  * ranger.api.hook_ready
  * ranger.container.directory.accept_file

And there is ranger.api.register_linemode(), a function that enables the user to add [[https://github.com/hut/ranger/wiki/Custom-linemodes][custom linemodes]].

See =pydoc ranger.api= and doc/examples/plugin_hello_world.py for more information.

* Signals

There are certain objects which emit signals.  You can bind your own functions to those signals with e.g. =<object>.signal_bind("<signal>", <function>)= and they will be run whenever that signal is emitted.  See =pydoc ranger.ext.signals= for details.

This is a list of all signals.  See also =grep "signal_emit" -Inr ranger/*=

|object|signal|when|
|------+------|---------|
|fm|execute.before|before a file is executed|
|fm|execute.after|after a file is executed|
|fm|tab.change|moving to a different tab|
|fm|runner.execute.before|before fm.run()|
|fm|runner.execute.after|after fm.run()|
|fm|move|when moving cursor to another file|
|fm|cd|when changing the directory|
|fm|loader.before|before adding a Loadable object|
|fm|loader.after|after finishing a Loadable object, possibly with errors, but without manually canceling it|
|fm|loader.destroy|after manually canceling a Loadable object (e.g. by typing `Ctrl+C` or `dd` in the task view (`W`))|
|fm.settings|setopt|when changing any option|
|fm.settings|setopt.<settingname>|when changing a specific option|
|CommandLoader|before|right after starting a command with CommandLoader|
|CommandLoader|after|after finishing a command with CommandLoader|
|CommandLoader|pause|on pausing a command execution|
|CommandLoader|unpause|on resuming a command execution|
|CommandLoader|destroy|on finishing or stopping a command execution|
# Upgrading.md
# Outdated configuration files?

When upgrading to a new minor version (e.g. from 1.6.1 to 1.7.0), there may be incompatibilities in the configuration files.  To find out if that is the case, run

`ranger --clean`

If ranger now works for you, it means you need to update your configuration.  It's located at `~/.config/ranger/` and consists of the files `rc.conf`, `commands.py`, `scope.sh` and `rifle.conf`.  To update them, simply deleting them should suffice, because then the default ones will be used.  If you have customized them, you need to merge them manually with the new default configs.

# Image previews stopped working after updating ranger-git

In September 2015, there was a backwards-incompatible change of scope.sh which broke image previewing.  To fix this, rename/delete your old `~/.config/ranger/scope.sh`, run `ranger --copy-config=scope` and, if necessary, merge your changes to scope.sh into the new version.
# VCS-integration.md
To enable the intergration with version control systems like git, mercurial or bazaar, run the following command:

```
:set vcs_aware true
```

Now it should look like this:

![screenshot][12]

When you have many repositories, this command will be very slow and it makes sense to only enable it in certain directories like this:

```
setlocal path=/home/hut/repos/ranger vcs_aware true
```
# Video-Previews.md
Since 1.7.0, ranger supports video previews.  More generally, you can define rules in the scope.sh configuration file to convert any file type into an image and display that image as a preview with w3mimgdisplay.

Video previews are disabled by default.  To turn them on:

1. install w3mimgdisplay. It's used to draw images into the terminal.  On archlinux, the package is called "w3m", on debian it's "w3m-img"
2. install ffmpegthumbnailer. It's used to generate a thumbnail of a video
3. get a recent scope.sh config file, e.g. by typing `ranger --copy-config=scope`
4. Uncomment the rule in the scope.sh below the line "Image preview for videos, disabled by default:"

Done!
##
# Todo

Read: <http://ranger.nongnu.org/cheatsheet.svg>

##
# Reference

[1]: https://github.com/hut/ranger/wiki/Official-user-guide#metadata
[2]: https://github.com/clvv/fasd
[3]: https://github.com/ranger/ranger/wiki/Integration-with-other-programs#fasd
[4]: http://w3m.sourceforge.net/
[5]: https://iterm2.com/
[6]: https://gist.github.com/haasn/7919afd765e308fa91cbe19a64631d0f
[7]: https://github.com/clvv/fasd
[8]: https://github.com/ranger/ranger/wiki/Commands#visit-frequently-used-directories
[9]: https://en.wikipedia.org/wiki/Miller_columns
[10]: http://www.vim.org
[11]: https://www.midnight-commander.org
[12]: http://ranger.nongnu.org/screenshots/vcs.png
