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

## How is it useful?

Without this plugin, the fasd aliases `o`, `m`, `v`... would never suggest you a
file opened from ranger.

##
# Installation

    $ git clone https://github.com/clvv/fasd
    $ sudo checkinstall

Use checkinstall or make to get the manpage.

# Usage
## How to list frecent files?  directories?  files+directories?

    $ f
    $ d
    $ a

These are aliases for:

    $ fasd -f
    $ fasd -d
    $ fasd -a

## ?

    ┌────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
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
# Manpage
## Fasd

Fasd (pronounced similar to "fast") is a command-line productivity booster.
Fasd offers quick access to files and directories for POSIX shells.
It is inspired by tools like [autojump][1], [z][2] and [v][3].
Fasd keeps  track of files  and directories you have  accessed, so that  you can
quickly reference them in the command line.

The name fasd comes from the default suggested aliases `f`(files),
`a`(files/directories), `s`(show/search/select), `d`(directories).

Fasd ranks files and directories by "frecency," that is, by both "frequency" and
"recency." The term "frecency"  was first coined by Mozilla and  used in Firefox
([link][4]).

## Introduction

If you use your shell to navigate  and launch applications, fasd can help you do
it more efficiently.
With fasd, you can open files regardless of which directory you are in.
Just with  a few key strings,  fasd can find  a "frecent" file or  directory and
open it with command you specify.
Below are some hypothetical situations, where you can type in the command on the
left and fasd will "expand" your command into the right side.

    v def conf       =>     vim /some/awkward/path/to/type/default.conf
    j abc            =>     cd /hell/of/a/awkward/path/to/get/to/abcdef
    m movie          =>     mplayer /whatever/whatever/whatever/awesome_movie.mp4
    o eng paper      =>     xdg-open /you/dont/remember/where/english_paper.pdf
    vim `f rc lo`    =>     vim /etc/rc.local
    vim `f rc conf`  =>     vim /etc/rc.conf

Fasd comes with some useful aliases by default:

```sh
alias a='fasd -a'        # any
alias s='fasd -si'       # show / search / select
alias d='fasd -d'        # directory
alias f='fasd -f'        # file
alias sd='fasd -sid'     # interactive directory selection
alias sf='fasd -sif'     # interactive file selection
alias j='fasd_cd -d'     # cd, same functionality as j in autojump
alias jj='fasd_cd -d -i' # cd with interactive selection
```

Fasd will smartly detect when to display a list of files or just the best match.
For instance, when you call fasd in a subshell with some search parameters, fasd
will only return the best match.
This enables you to do:

    $ mv update.html `d www`
    $ cp `f mov` .

## Install

To get fasd working in a shell, some initialization code must be run.
Put the line below in your shell rc.

```sh
eval "$(fasd --init auto)"
```

This will setup a  command hook that executes on every  command and advanced tab
completion for zsh and bash.

If you  want more control  over what gets into  your shell environment,  you can
pass customized set of arguments to `fasd --init`.

    zsh-hook             # define _fasd_preexec and add it to zsh preexec array
    zsh-ccomp            # zsh command mode completion definitions
    zsh-ccomp-install    # setup command mode completion for zsh
    zsh-wcomp            # zsh word mode completion definitions
    zsh-wcomp-install    # setup word mode completion for zsh
    posix-alias          # define aliases that applies to all posix shells
    posix-hook           # setup $PS1 hook for shells that's posix compatible

Example for a minimal zsh setup (no tab completion):

```sh
eval "$(fasd --init posix-alias zsh-hook)"
```

Note that  this method will  slightly increase  your shell start-up  time, since
calling binaries has overhead.
You can cache fasd init code if you want minimal overhead.
Example code for bash (to be put into .bashrc):

```sh
fasd_cache="$HOME/.fasd-init-bash"
if [ "$(command -v fasd)" -nt "$fasd_cache" -o ! -s "$fasd_cache" ]; then
  fasd --init posix-alias bash-hook bash-ccomp bash-ccomp-install >| "$fasd_cache"
fi
source "$fasd_cache"
unset fasd_cache
```

Optionally, if  you can  also source  `fasd` if you  want `fasd`  to be  a shell
function instead of an executable.

You can tweak initialization code.
For instance, if you want to use "c" instead of "j" to do directory jumping, you
can use the alias below:

```sh
    alias c='fasd_cd -d'
    # `-d` option present for bash completion
    # function fasd_cd is defined in posix-alias
```

After you first installed fasd, open some files (with any program) or `cd`
around in your shell. Then try some examples below.

## Examples

    $ f foo           # list frecent files matching foo
    $ a foo bar       # list frecent files and directories matching foo and bar
    $ f js$           # list frecent files that ends in js
    $ f -e vim foo    # run vim on the most frecent file matching foo
    $ mplayer `f bar` # run mplayer on the most frecent file matching bar
    $ j foo           # cd into the most frecent directory matching foo
    $ open `sf pdf`   # interactively select a file matching pdf and launch `open`

You should add your own aliases to fully utilize the power of fasd.
Here are some examples to get you started:

```sh
alias v='f -e vim' # quick opening files with vim
alias m='f -e mplayer' # quick opening files with mplayer
alias o='a -e xdg-open' # quick opening files with xdg-open
```

If you're  using bash, you  have to call `_fasd_bash_hook_cmd_complete`  to make
completion work.
For instance:

    _fasd_bash_hook_cmd_complete v m j o

You could select an entry in the list of matching files.

## Matching

Fasd has three matching modes: default, case-insensitive, and fuzzy.

For a given set of queries (the set of command-line arguments passed to fasd),
a path is a match if and only if:

1. Queries match the path *in order*.
2. The last query matches the *last segment* of the path.

If no match is found, fasd will try the same process ignoring case. If still no
match is found, fasd will allow extra characters to be placed between query
characters for fuzzy matching.

Tips:

* If you want your last query not to match the last segment of the path, append
  `/` as the last query.
* If you want your last query to match the end of the filename, append `$` to
  the last query.

## How It Works

When you run fasd init code or source `fasd`, fasd adds a hook which will be
executed whenever you execute a command. The hook will scan your commands'
arguments and determine if any of them refer to existing files or directories.
If yes, fasd will add them to the database.

## Compatibility

Fasd's basic functionalities are POSIX compliant, meaning that you should be
able to use fasd in all POSIX compliant shells. Your shell need to support
command substitution in `$PS1` in order for fasd to automatically track your
commands and files. This feature is not specified by the POSIX standard, but
it's nonetheless present in many POSIX compliant shells. In shells without
prompt command or prompt command substitution (csh for instance), you can add
entries manually with `fasd -A`. You are very welcomed to contribute shell
initialization code for not yet supported shells.

Fasd has been tested on the following shells: bash, zsh, mksh, pdksh, dash,
busybox ash, FreeBSD 9 /bin/sh and OpenBSD /bin/sh.

## Synopsis

    fasd [options] [query ...]
    [f|a|s|d|j] [options] [query ...]
      options:
        -s         list paths with scores
        -l         list paths without scores
        -i         interactive mode
        -e <cmd>   set command to execute on the result file
        -b <name>  only use <name> backend
        -B <name>  add additional backend <name>
        -a         match files and directories
        -d         match directories only
        -f         match files only
        -r         match by rank only
        -t         match by recent access only
        -R         reverse listing order
        -h         show a brief help message
        -[0-9]     select the nth entry

    fasd [-A|-D] [paths ...]
        -A    add paths
        -D    delete paths

## Tab Completion

Fasd offers two completion modes, command mode completion and word mode
completion. Command mode completion works in bash and zsh. Word mode
completion only works in zsh.

Command mode completion is just like completion for any other commands. It is
triggered when you hit tab on a `fasd` command or its aliases. Under this mode
your queries can be separated by a space. Tip: if you find that the completion
result overwrites your queries, type an extra space before you hit tab.

Word mode completion can be triggered on *any* command. Word completion is
triggered by any command line argument that starts with `,` (all), `f,`
(files), or `d,` (directories), or that ends with `,,` (all), `,,f` (files), or
`,,d` (directories). Examples:

    $ vim ,rc,lo<Tab>
    $ vim /etc/rc.local

    $ mv index.html d,www<Tab>
    $ mv index.html /var/www/

There are also three zle widgets: `fasd-complete`, `fasd-complete-f`,
`fasd-complete-d`. You can bind them to keybindings you like:

```sh
bindkey '^X^A' fasd-complete    # C-x C-a to do fasd-complete (files and directories)
bindkey '^X^F' fasd-complete-f  # C-x C-f to do fasd-complete-f (only files)
bindkey '^X^D' fasd-complete-d  # C-x C-d to do fasd-complete-d (only directories)
```

## Backends

Fasd can take advantage of different sources of recent / frequent files. Most
desktop environments (such as OS X and Gtk) and some editors (such as Vim) keep
a list of accessed files. Fasd can use them as additional backends if the data
can be converted into fasd's native format. Below is a list of available
backends.

```
`recently-used`
GTK's recently-used file (Usually available on Linux)

`current`
Provides everything in $PWD (whereever you are executing `fasd`)

`viminfo`
Vim's editing history, useful if you want to define an alias just for editing
things in vim
```

You can  define your own backend  by declaring a  function by that name  in your
`.fasdrc`.
You can set default backend with `_FASD_BACKENDS` variable in our `.fasdrc`.

Fasd can mimic [v][8]'s behavior by this alias:

```sh
alias v='f -t -e vim -b viminfo'
```

## Tweaks

Some shell variables that you can set before sourcing `fasd`. You can set them
in `$HOME/.fasdrc`

```
$_FASD_DATA
Path to the fasd data file, default "$HOME/.fasd".

$_FASD_BLACKLIST
List of blacklisted strings. Commands matching them will not be processed.
Default is "--help".

$_FASD_SHIFT
List of all commands that needs to be shifted, defaults to "sudo busybox".

$_FASD_IGNORE
List of all commands that will be ignored, defaults to "fasd ls echo".

$_FASD_TRACK_PWD
Fasd defaults to track your "$PWD". Set this to 0 to disable this behavior.

$_FASD_AWK
Which awk to use. Fasd can detect and use a compatible awk.

$_FASD_SINK
File to log all STDERR to, defaults to "/dev/null".

$_FASD_MAX
Max total score / weight, defaults to 2000.

$_FASD_SHELL
Which shell to execute. Some shells will run faster than others. fasd
runs faster with dash and ksh variants.

$_FASD_BACKENDS
Default backends.

$_FASD_RO
If set to any non-empty string, fasd will not add or delete entries from
database. You can set and export this variable from command line.

$_FASD_FUZZY
Level of "fuzziness" when doing fuzzy matching. More precisely, the number of
characters that can be skipped to generate a match. Set to empty or 0 to
disable fuzzy matching. Default value is 2.

$_FASD_VIMINFO
Path to .viminfo file for viminfo backend, defaults to "$HOME/.viminfo"

$_FASD_RECENTLY_USED_XBEL
Path to XDG recently-used.xbel file for recently-used backend, defaults to
"$HOME/.local/share/recently-used.xbel"

```

##
# Readme
## Synopsis

    fasd [options] [query ...]

    [f|a|s|d|j] [options] [query ...]

    fasd [-A|-D] [paths ...]

## Options

    -s         list paths with ranks
    -l         list paths without ranks
    -i         interactive mode
    -e <cmd>   set command to execute on the result file
    -b <name>  only use <name> backend
    -B <name>  add additional backend <name>
    -a         match files and directories
    -d         match directories only
    -f         match files only
    -r         match by rank only
    -t         match by recent access only
    -R         reverse listing order
    -h         show a brief help message
    -[0-9]     select the nth entry

## Description

Fasd keeps track of files and directories you access in your shell and gives you
quick access to them.
You can use fasd to reference files or directories by just a few key identifying
characters.
You can use  fasd to boost your  command line productivity by  defining your own
aliases to launch programs on files or directories.
Fasd, by  default, provides some basic  aliases, including a shell  function "z"
that resembles the functionality of "z" and "autojump."

The   name  "fasd"   comes  from   the  default   suggested  aliases   f(files),
a(files/directories), s(show/search/select), d(directories).

Fasd ranks files and directories by "frecency," that is, by both "frequency" and
"recency." The term "frecency" was first coined by Mozilla and used in Firefox.

## Examples

    j bundle
    f -e vim nginx conf
    f -i rc$
    vi `f nginx conf`
    cp update.html `d www`
    open `sf pdf`

## Shell Initialization

To get fasd working in a shell, some initialization code must be run.
Put lines below in your POSIX compatible shell rc.

    eval "$(fasd --init auto)"

This will setup a  command hook that executes on every  command and advanced tab
completion for zsh and bash.

If you  want more control  over what gets into  your shell environment,  you can
pass customized set of arguments to fasd --init.

    zsh-hook             # define _fasd_preexec and add it to zsh preexec array
    zsh-ccomp            # zsh command mode completion definitions
    zsh-ccomp-install    # setup command mode completion for zsh
    zsh-wcomp            # zsh word mode completion definitions
    zsh-wcomp-install    # setup word mode completion for zsh
    bash-hook            # add hook code to bash $PROMPT_COMMAND
    bash-ccomp           # bash command mode completion definitions
    bash-ccomp-install   # setup command mode completion for bash
    posix-alias          # define aliases that applies to all posix shells
    posix-hook           # setup $PS1 hook for shells that's posix compatible
    tcsh-alias           # define aliases for tcsh
    tcsh-hook            # setup tcsh precmd alias

Example for a minimal zsh setup (no tab completion):

    eval "$(fasd --init posix-alias zsh-hook)"

Note that  this method will  slightly increase  your shell start-up  time, since
calling binaries has overhead.
You can cache fasd init code if you want minimal overhead.
Example code for bash (to be put into .bashrc):

    fasd_cache="$HOME/.fasd-init-bash"
    if [ "$(command -v fasd)" -nt "$fasd_cache" -o ! -s "$fasd_cache" ]; then
    fasd --init posix-alias bash-hook bash-ccomp bash-ccomp-install >| "$fasd_cache"
    fi
    source "$fasd_cache"
    unset fasd_cache

Optionally, if you can also source fasd if  you want fasd to be a shell function
instead of an executable.

You can tweak initialization code.
For instance, if you want to use "c" instead of "j" to do directory jumping, you
can use the alias below:

    alias c='fasd_cd -d'
    # `-d' option present for bash completion
    # function fasd_cd is defined in posix-alias

## Matching

Fasd has three matching modes: default, case-insensitive, and fuzzy.

For a given set of queries (the set of command-line arguments passed to fasd), a
path is a match if and only if:

   1. Queries match the path in order.

   2. The last query matches the last segment of the path.

      If no match is found, fasd will try the same process ignoring case.
      If still no match is found, fasd  will allow extra characters to be placed
      between query characters for fuzzy matching.

      Tips:

      · If you want  your last query not to match the last  segment of the path,
      append `/` as the last query.

      · If you want your last query to match the end of the filename, append `$`
      to the last query.

## Compatibility

Fasd's basic  functionalities are  POSIX compliant, meaning  that you  should be
able to use fasd in all POSIX compliant shells.
Your shell  need to support  command substitution in $PS1  in order for  fasd to
automatically track your commands and files.
This  feature is  not  specified by  the POSIX  standard,  but it's  nonetheless
present in many POSIX compliant shells.
In  shells without  prompt  command  or prompt  command  substitution (tcsh  for
instance), you can add entries manually with "fasd -A".
You  are very  welcomed  to contribute  shell initialization  code  for not  yet
supported shells.

## Tab Completion

Fasd  offers  two  completion  modes,  command mode  completion  and  word  mode
completion.
Command mode completion works in bash and zsh.
Word mode completion only works in zsh.

Command mode completion is just like completion for any other commands.
It is triggered when you hit tab on a fasd command or its aliases.
Under this mode your queries can be separated by a space.
Tip: if  you find that  the completion result  overwrites your queries,  type an
extra space before you hit tab.

Word mode completion can be triggered on any command.
Word completion is  triggered by any command line argument  that starts with ","
(all), "f," (files), or "d," (directories),  or that ends with ",," (all), ",,f"
(files), or ",,d" (directories).
Examples:

    $ vim ,rc,lo<Tab>
    $ vim /etc/rc.local

    $ mv index.html d,www<Tab>
    $ mv index.html /var/www/

There   are  also   three  zle   widgets:  "fasd-complete",   "fasd-complete-f",
"fasd-complete-d".
You can bind them to keybindings you like:

    bindkey '^X^A' fasd-complete    # C-x C-a to do fasd-complete (files and directories)
    bindkey '^X^F' fasd-complete-f  # C-x C-f to do fasd-complete-f (only files)
    bindkey '^X^D' fasd-complete-d  # C-x C-d to do fasd-complete-d (only directories)

## Backends

Fasd can take advantage of different sources of recent / frequent files.
Most desktop environments (such as OS X  and Gtk) and some editors (such as Vim)
keep a list of accessed files.
Fasd can  use them  as additional  backends if  the data  can be  converted into
fasd's native format.
Below is a list of available backends.

   - recently-used: GTK's recently-used file (Usually available on Linux)

   - current:  Provides  everything  in  $PWD (whereever you are executing fasd)

   - viminfo: Vim's editing history, useful if you want to define an alias just
     for editing things in vim

You can  define your own backend  by declaring a  function by that name  in your
.fasdrc.
You can set default backend with `_FASD_BACKENDS` variable in our .fasdrc.

##
## Tweaks

Upon every execution, fasd will source "/etc/fasdrc" and "$HOME/.fasdrc" if they
are present.
Below are some variables you can set:

### `$_FASD_DATA`

Path to the fasd data file, default "$HOME/.fasd".

### `$_FASD_BLACKLIST`

List of blacklisted strings.
Commands matching them will not be processed.
Default is "--help".

### `$_FASD_SHIFT`

List of all commands that needs to be shifted, defaults to "sudo busybox".

### `$_FASD_IGNORE`

List of all commands that will be ignored, defaults to "fasd ls echo".

### `$_FASD_TRACK_PWD`

Fasd defaults to track your "$PWD".
Set this to 0 to disable this behavior.

### `$_FASD_AWK`

Which awk to use.
fasd can detect and use a compatible awk.

### `$_FASD_SINK`

File to log all STDERR to, defaults to "/dev/null".

### `$_FASD_MAX`

Max total score / weight, defaults to 2000.

### `$_FASD_SHELL`

Which shell to execute.
Some shells will run faster than others.
fasd runs faster with dash and ksh variants.

### `$_FASD_BACKENDS`

Default backends.

### `$_FASD_RO`

If  set to  any non-empty  string,  fasd will  not  add or  delete entries  from
database.
You can set and export this variable from command line.

### `$_FASD_FUZZY`

Level of "fuzziness" when doing fuzzy matching.
More  precisely, the  number of  characters that  can be  skipped to  generate a
match.
Set to empty or 0 to disable fuzzy matching.
Default value is 2.

### `$_FASD_VIMINFO`

Path to .viminfo file for viminfo backend, defaults to "$HOME/.viminfo"

### `$_FASD_RECENTLY_USED_XBEL`

Path  to XDG  recently-used.xbel  file for  recently-used  backend, defaults  to
"$HOME/.local/share/recently-used.xbel"

###
## Debugging

If fasd does not work as expected, you can set `_FASD_SINK` in your `.fasdrc` to
obtain a log.

    _FASD_SINK="$HOME/.fasd.log"

##
# Todo
## ?

Once this bug is fixed:

<https://github.com/junegunn/fzf/issues/1486>
<https://bugs.launchpad.net/ubuntu/+source/linux/+bug/1813873>

Have a look at this:

<https://github.com/andrewferrier/fzf-z>

It installs a command which should let you fuzzy search the output of fasd.
It's so brief (<100 sloc) that there's no need to install the script.
Just read and copy the interesting part.

##
# Reference

[1]: https://github.com/joelthelion/autojump
[2]: http://github.com/rupa/z
[3]: https://github.com/rupa/v
[4]: https://developer.mozilla.org/en/The_Places_frecency_algorithm
[5]: https://github.com/clvv/fasd/wiki/Installing-via-Package-Managers
[6]: https://github.com/clvv/fasd/zipball/1.0.1
[7]: https://github.com/clvv/fasd/tarball/1.0.1
[8]: http://github.com/rupa/v
