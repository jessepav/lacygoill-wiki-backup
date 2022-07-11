# ?

After studying surfraw, study `locate`.
It's documented in our pdf about `find`.
Also, see `man locate`, `man updatedb`, `man updatedb.conf`.

Also, study `fd`.  They complete each other.
`locate` to find anything older than a day, `fd` for the rest.

---

To allow `locate` to search inside `/media`:

    $ sudo cp updatedb.conf{,.bak}
    $ sudo sed -i 's:/media ::' /etc/updatedb.conf

# ?

How to change the browser opened by surfraw?

##
# Installation

    $ git clone https://gitlab.com/surfraw/Surfraw
    $ cd surfraw
    $ autoreconf -f -i
    $ ./configure
    $ make
    $ sudo make install

##
# How to list all the search engines supported by surfraw?

    $ sr -elvi

##
# Configuration

    ~/.config/surfraw/elvi/

Dans ce dossier, on  peut ajouter des fichiers dont le  code shell implémente un
nouvel elvi.
Utile si  la liste d'elvis  supportés par défaut ne  contient pas un  moteur qui
nous intéresse.

Le  nom du  fichier a  de l'importance,  car c'est  lui qu'il  faudra passer  en
argument à  `sr`/`surfraw` pour lui indiquer  le moteur de recherche  sur lequel
chercher un mot-clé.

---

    $ cd ~/.config/surfraw/elvi/
    $ cp /usr/lib/surfraw/youtube my_custom_site
    $ chmod u+x my_custom_site
    $ vim my_custom_site

Par défaut,  surfraw permet de chercher  un mot-clé sur une  liste prédéfinie de
moteurs de recherche.
Il se peut que le site qui nous intéresse ne soit pas dans cette liste.

Dans ce cas,  il faut créer un fichier  dans `~/.config/surfraw/elvi/` contenant
du code shell implémentant la recherche sur le site en question.

Pour se simplifier la tâche, on peut commencer à travailler à partir d'une copie
de `/usr/lib/surfraw/youtube` (trouvé via `dpkg -L surfraw | youtube$`).

---

Il faut adapter le code du fichier au site qui nous intéresse.

En particulier, les lignes commençant par le mot-clé (fonction?) `w3_browse_url`.

    w3_browse_url "http://www.youtube.com/"
    w3_browse_url "http://www.youtube.com/results?search_query=${escaped_args}"

Il faut changer l'url de base, et  l'url d'une recherche qd on utilise le moteur
du site.

# Utilisation

    $ sr google arch linux
    $ surfraw google arch linux

Cherche 'arch linux' sur  google dans un navigateur en GUI (via  `sr`) ou en TUI
(via `surfraw`).

---

    $ sr -browser=google-chrome google kitten
    $ surfraw -browser=w3m google kitten

L'argument  `-browser`  permet  de  configurer temporairement  le  navigateur  à
utiliser le temps d'une recherche.

##
##
##
# Synopsis

    $ surfraw elviname [options] search words ...
    $ sr elviname [options] search words ...
    $ sr -elvi
    $ sr [options] bookmark [search words]

# Description

Surfraw provides a fast unix command line  interface to a variety of popular WWW
search engines and other artifacts of power.
It reclaims google, altavista, dejanews, freshmeat, research index, slashdot and
many others  from the  false‐prophet, pox‐infested  heathen lands  of htmlforms,
placing these wonders  where they belong, deep in unix  heartland, as god loving
extensions to the shell.

Surfraw consists of  a collection of elvi,  each of which knows how  to search a
specific web site.
To see the list of elvi type:

    $ surfraw -elvi

Note that `sr` is an alias for surfraw, so that could equally be

    $ sr -elvi

To search using an elvis use:

    $ sr elviname [options] search terms..

For example,  to search google for  information on Debian ports,  using the "I'm
feeling lucky" option:

    $ sr google -l debian ports

Adding the  elvi to your  path If you  are a regular  user of surfraw,  you will
probably get sick of typing sr or surfraw each time.
You can regain the old behaviour of running the elvi directly by adding the elvi
directory  (/usr/local/lib/surfraw)  to  your  path, either  manually  or  using
surfraw-update-path(1).

---

Surfraw supports bookmarks.
To  add   a  bookmark,  add  it   to  `/usr/local/etc/xdg/surfraw/bookmarks`  or
`$HOME/.config/surfraw/bookmarks`.

The format of the bookmarks file is simple, each bookmark is on a sepa‐
rate line, with the bookmark and URL separated by whitespace, eg:

    ntk   http://www.ntk.net/

If the url contains  the string %s, you can specify an  optional argument to the
bookmark.
Without an argument, only the domain will be returned.
With arguments, %s will be replaced by the arguments.
This obviates the need to create elvi for sites with very simple search options.

To invoke a bookmark,  use "surfraw bookmark" or "sr bookmark",  and if an elvis
of that name doesn't exist, it searches for a bookmark of that name instead.

    $ sr tpb_mirror

There are some example bookmarks in `/usr/local/etc/xdg/surfraw/bookmarks`.

##
# Options

Use `$ sr elviname -local-help` for elvi‐specific options.

The following options work with all elvi.

## -help

Show summary of options (including elvi‐specific options).

## -local-help

Show elvi‐specific options.

## -version

Show version of program.

## -browser=EXECUTABLE

Set browser (default: sensible-browser).

## -elvi

Display a list of other Surfraw mechanisms for conquering evil.

## -escape-url-args=yes|no

Apply url escaping to arguments (default: yes)

## -q|-quote

Bracket all arguments with " characters (default: no).
Note that putting quotes round arguments works now, so you can do, for example:

    $ sr google foo "bar baz" bam

and the quoting is passed on to the search engine

##
# Examples

    $ sr ask why is jeeves gay?
    $ surfraw google -results=100 RMS, GNU, which is sinner, which is sin?
    $ sr austlii -method=phrase dog like
    $ /usr/local/lib/surfraw/rhyme -method=perfect Julian

# Configuration

Surfraw uses the XDG basedir spec to locate config files.
<http://standards.freedesktop.org/basedir-spec/basedir-spec-0.6.html>

The  default locations  are shown  below,  but can  be modified  by setting  the
environment variables `$XDG_CONFIG_HOME` and `$XDG_CONFIG_DIRS`.
See the spec for more details.

Surfraw gets its configuration from three sources, in order:

1.  Environment variables

2.  /usr/local/etc/xdg/surfraw/conf

3.  $HOME/.config/surfraw/conf

`/usr/local/etc/xdg/surfraw.conf`  and   `$HOME/.config/surfraw/conf`  are  both
fragments of bourne‐shell style shell script.

`/usr/local/etc/xdg/surfraw.conf` should use def and defyn to define variables.
These functions set variables unless they are already set by the environment.
defyn is used for boolean configuration variables, def for all others.
For instance:

    def     SURFRAW_text_browser /usr/bin/lynx
    defyn   SURFRAW_graphical         no

`$HOME/.config/surfraw/conf` should use sh‐style entries, eg:

    SURFRAW_text_browser=/usr/bin/lynx
    SURFRAW_graphical=no

This is because you want them to override environment variables unconditionally.

# Files

    /usr/local/lib/surfraw

Location of the elvi.

    ${HOME}/.config/surfraw/elvi

Per‐user elvi.

    /usr/local/etc/xdg/surfraw/conf

Default system wide configuration file.

    $HOME/.config/surfraw/conf

Default per‐user config file

    /usr/local/etc/xdg/surfraw/bookmarks

System wide bookmarks file.

    $HOME/.config/surfraw/bookmarks

Per‐user bookmarks file.

##
##
##
# Name

    $ surfraw-update-path

Updates PATH in shell config files.

# Synopsis

    $ surfraw-update-path [-add] [-remove] [-check] [-sys] [-all] [-help] [-shell=SHELL]

# Description

surfraw-update-path adds  the surfraw elvi  directory (`/usr/local/lib/surfraw`)
to your PATH in your shell's config file.

Don't forget to login again or source your login files for it to take effect.

##
# Options
## -check

Checks to see if the surfraw config code is present.
This is the default.

## -add

Adds the surfraw config code.

## -remove

Removes the surfraw config code

## -sys

Updates the system-wide shell config instead of the user.
Must be done as root.

## -shell=SHELL

Selects the shell to configure.
Defaults to the value of the $SHELL environment variable.

Currently supported shells are:

sh, ash, bash, dash, csh, tcsh, ksh, pdksh, zsh, rc, and es.

## -all

Attempts to configure the startup files for all known shells

## -help

Gives a usage message

##
# Return Value

`-check` returns 0  if the surfraw code is  present in the file, 1 if  it is not
found, or 2 on error.

All other options return 0 on success, or 2 on error.

##
# Environment
## SHELL

Used to determine which shell to configure, if `-shell` is not given.

## HOME

Used to find users config files.

## ENV Used by posix-compliant shells to specify a startup rc file.

## ZDOTDIR

Used to find user config files for zsh.
If not set, defaults to HOME.

