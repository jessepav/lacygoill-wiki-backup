Interface for Rapidly Tagging Many Small Files
        https://github.com/oniony/TMSU/issues/124

# Installation

    https://golang.org/dl/

            `go` est une dépendance de `tmsu` (car ce dernier est écrit en `go`).
            Cette url permet de dl un binaire `go`.  Exemple de description à chercher:

                    Linux
                    Linux 2.6.23 or later, Intel 64-bit processor
                    go1.8.3.linux-amd64.tar.gz (86MB)


    $ sudo tar -C /usr/local -xzf go1.8.3.linux-amd64.tar.gz

            Extraire l'archive précédemment téléchargée dans `/usr/local`.
            Commande trouvée ici:

                    https://golang.org/doc/install


    $ vim ~/.config/fish/conf.d/environment.fish
      set --export PATH $PATH:/usr/local/go/bin
      set --export GOPATH $HOME/go

            Indiquer:

                    - au shell  où se trouve le binaire `go`
                    - à `go`    où se trouve notre espace de travail
                                (nécessaire pour que `go get` fonctionne et sache où dl des fichiers)


    $ mkdir -p $HOME/go/src/hello/

    $ tee <<'EOF' $HOME/go/src/hello/hello.go
    package main
    import "fmt"
    func main() {
        fmt.Printf("hello, world\n")
    }
    EOF

    $ cd $HOME/go/src/hello/
    $ go build
    $ ./hello

            Pour vérifier que `go` a été correctement installé, ces commandes créent un programme “hello world“.

            On pourrait l'installer dans $HOME/go/bin/ via:

                    go install

            ... et le supprimer via:

                    go clean


    $ go get -u github.com/mattn/go-sqlite3
    $ go get -u github.com/hanwen/go-fuse/fuse

            Installation des dépendances nécessaires à la compilation du paquet `TMSU`.


    $ git clone https://github.com/oniony/TMSU/
    $ cd TMSU/
    $ git checkout v0.6.1 (la release la plus récente atm)
    $ make
    $ sudo make install

            Compilation et installation du paquet TMSU.

            Pour la description du paquet, utiliser:

                    TMSU lets  you tags  your files  and then  access them  through a  nifty virtual
                    filesystem from any other application.

# Home
## Overview

TMSU est un programme qui permet d'associer des tags à des fichiers.  Il fournit
un outil pour gérer ces tags et  un système de fichiers virtuel pour accéder aux
fichiers via leurs tags.  Les tags sont stockés dans une bdd sqlite.

## Tour

- The [Quick Tour][1] gives you an overview of TMSU usage.

    tmsu init

            Crée une bdd dans le cwd:

                    .
                    └── .tmsu
                        └── db

            Qd `tmsu` est invoqué, il cherche une bdd dans le cwd, puis dans le dossier parent, …
            le processus se répétant jusqu'à la racine.


    tmsu tag file.mp3 music epic mp3
    tmsu tag --tags 'music epic mp3' *.mp3

            Applique les tags `music`, `epic` et `mp3` à:

                    - `file.mp3`
                    - tous les fichiers mp3 du cwd


    Liste les fichiers portant le(s) tag(s):

    ┌────────────────────────────────────┬───────────────────────┐
    │ tmsu files epic and mp3            │ epic et `mp3`         │
    ├────────────────────────────────────┼───────────────────────┤
    │ tmsu files epic and (mp3 or music) │ epic, et mp3 ou music │
    ├────────────────────────────────────┼───────────────────────┤
    │ tmsu files epic and not mp3        │ epic mais pas mp3     │
    └────────────────────────────────────┴───────────────────────┘


    mkdir mp
    tmsu mount mp

            Monte le système de fichiers virtuel, permettant d'accéder aux fichiers via leur tag,
            dans un dossier vide ad-hoc `mp` (Mount Point).

            Initialement, qd la bdd est vide, `mp/` contient:

                    .
                    ├── .database → cwd/.tmsu/db
                    ├── queries
                    │   └── README.md
                    └── tags
                        └── README.md


    cd queries/
    ls 'epic and mp3'
    ls 'epic and (mp3 or music)'

            Depuis `queries/`, on peut invoquer `ls` pour lister les fichiers portant certains tags.

            Après chaque invocation, `tmsu` crée un dossier dont le nom correspond à la requête.
            Ce dernier contient des liens symboliques pointant vers les fichiers.

            Pour supprimer le dossier d'une requête, il faut utilsier `rmdir` et non `rm -r`:

                    rmdir 'epic and mp3'    ✔
                    rm -r 'epic and mp3'    ✘  supprime les tags associés aux fichiers du dossier


    ls mp/tags/
         epic mp3 music

    ls mp/tags/epic
         file1 … mp3/ music/

            Dans `tags/`, se trouve des sous-dossiers correspondant aux tags.
            Dans `tags/epic`, se trouve les fichiers portant le tag `epic`, ainsi que des dossiers
            correspondant aux autres tags associés à ces fichiers.


    cd mp/tags/
         mkdir jazz
         mv epic inspiration
         rm epic/file.mp3
         rmdir unused/

            Crée le tag `jazz`.
            Renomme le tag `epic` en `inspiration`.
            Retire le tag `epic` du fichier `file.mp3`.
            Supprime le tag `unused` (ne fonctionne que si le dossier est vide, i.e. le tag n'est plus
            associé à aucun fichier).

            Illustre comment manipuler les tags depuis le dossier `tags/`.


## Documentation

TMSU has built-in help: use the `help` command.

    $ tmsu help

You can also get help on a particular subcommand:

    $ tmsu help tags

See also:

- [Frequently Asked Questions][2]
- [Troubleshooting][3]
- [Tricks and Tips][4]

### Concepts

- [Virtual Filesystem][5]: how to mount and use the virtual filesystem.
- [Handling Directories][6]: options for tagging directories and their contents.
- [Repairing the Database][7]: repairing the database after files are added, modified, moved and deleted.
- [Switching Databases][8]: working with multiple TMSU databases.
- [Fingerprint Algorithms][9]: changing the fingerprint algorithm.
- [Settings][10]: configuring TMSU's behaviour.

### Technical Details

- [Database Schema][11]: the TMSU Sqlite3 database schema.
- [Tag and Value Names][12]: supported and illegal names.

# Repairing

TMSU does  not watch the  filesystem for changes at  this time.  This  is partly
because  this would  require a  daemon process  to be  running at  all times  to
monitor these events andpartly because such a solution would not work on certain
filesystems (such as remote filesystems).

As a  result, whenever  you move or  alter files  that have  been tagged in  the TMSU  database, the
database will be out-of-date with respect to the actual files on disk.

## Status

TMSU includes a command, `status`, which can  be used to find where the database
is  out  of  synchronicity.   This  command,  in  its  simplest  form  (with  no
arguments), it will  look at each file  in the database and compare  it with the
corresponding file on disk, listing whether the file is in sync (show as `T` for
tagged), missing (`!`) or modified (`M`).

If  paths  are  given as  arguments,  the  `status`  command  will  look  at these  paths  (and  any
files/directories  beneath  them) and  show  the  status  of these  files.  As  such, files  may  be
additionally reported as untagged (`U`), meaning they are on not in the database.

## Repairing

TMSU is able to automatically repair files that  have *either* been moved or modified, but not both.
It can  do this  because when  you tag  files TMSU stores  a number  of attributes  of the  file, in
particular its size and *fingerprint*: a hash of the file's contents.

### Modified Files

By running `repair` without arguments, TMSU will be  able to repair the fingerprints in the database
for files that have been modified but still reside at the same path.

### Moved Files

By  specifying  paths as  arguments  to  `repair`,  TMSU will  (additionally  to
correcting fingerprints) search in these paths  for any files that can no longer
be found at the path when they  were tagged.  It will search under the specified
paths for files with the same file size, and then confirm any match by comparing
the file`s fingerprint with that in the database.  If a match is confirmed, then
TMSU will correct the path in the database.

### Manual Repair

If you know for certain that files have moved from one path to another, for example if you have just
moved them there, you can perform a manual repair:

    $ tmsu repair --manual /some/path /new/path

This will  modify *all* files in  the database under  `/some/path` to `/new/path`, and  update their
fingerprints.

# Database-Schema
### Tag

A tag that can be applied to files.

Name  |Type   |Primary Key
------|-------|-----------
id    |integer|✓
name  |text   |

### File

A file that has been tagged.

Name       |Type    |Primary Key|Comment
-----------|--------|-----------|-------
id         |integer |✓          |
directory  |text    |           |
name       |text    |           |
fingerprint|text    |           |used to detect moved and duplicate files
mod_time   |datetime|           |used to detect modified files
size       |integer |           |used to detect modified files
is_dir     |boolean |           |

### Value

A tag value.

Name       |Type    |Primary Key
-----------|--------|-----------
id         |integer |✓
name       |text    |

### File Tag

An application of a tag upon a file.

Name       |Type    |Primary Key
-----------|--------|-----------
file_id    |integer |✓
tag_id     |integer |✓
value_id   |integer |✓

### Implication

Note: this is in the process of being replaced.

Auto-application of a tag when another is applied.

Name            |Type   |Primary Key
----------------|-------|-----------
tag_id          |integer|✓
value_id        |integer|✓
implied_tag_id  |integer|✓
implied_value_id|integer|✓

### Query

Queries created within the VFS.

Name|Type|Primary Key|Comment
----|----|-----------|-------
text|text|✓          |the query text (e.g. 'apple and pear')

### Setting

Configures TMSU's behaviour.

Name |Type|Primary Key
-----|----|-----------
name |text|✓
value|text|

### Version

This records the TMSU schema version.

When TMSU  starts it checks the  version stored in  this table to  see if the schema  is up-to-date.
There should only ever be a single row in this table.

Name    |Type  |Primary Key
--------|------|-----------
major   |number|✓
minor   |number|✓
patch   |number|✓

# FAQ
## General
### What does TMSU stand for?

It stands for *Tag My Shit Up*.

### How is TMSU pronounced?

It's somewhere between *tiramisu* and a sudden and unexpected sneeze.

### How can I report a bug or make a suggestion?

Either log it in the [issue tracker](//github.com/oniony/TMSU/issues) or email the mailing-list [ml@tmsu.org](mailto:ml@tmsu.org).

### What similar programs are there?

You should also look at:

  - [Tagsistant](http://tagsistant.net/)
  - [TagFS](https://code.google.com/p/tagfilesystem/)
  - [Dantalian](http://dantalian.readthedocs.org/)

## Functionality
### Why does TMSU not detect file moves and renames?

To detect  file moves/renames would require  a daemon process watching  the file
system for changes and  support from the file system for  these events.  As some
file systems cannot provide these events  (e.g. remote file systems) a universal
solution cannot be offered.   Such a function may be added  later for those file
systems that  do provide  file move/modification events  but adding  support for
this to TMSU is not a priority at this time.

The current  solution is to  periodically use the `repair`  command which will  detect moved/renamed
files and also  update fingerprints for modified files.  (The limitation of this is  that files that
are both moved/renamed and modified cannot be detected.)

### How do I exclude tags when listing files?

TMSU supports  a simple query language  consisting of the operators  `and`, `or`
and `not`.  To exclude tags, simply prefix them with `not`:

For example, pull out your audio books:

    $ tmsu files mp3 and not music

The `and` operator is implied if you omit it:

    $ tmsu files mp3 not music

Excluding multiple tags is easiest with parentheses and the `or` operator:

    $ tmsu files mp3 not rock not big-jazz not pop
    $ tmsu files mp3 not (rock or big-jazz or pop)

## Compatibility
### Is a package available for my GNU/Linux distribution's package manager?

At this time probably not.  Help with creating these would be very much appreciated.

- Arch Linux [package is available](https://aur.archlinux.org/packages/tmsu/) in the AUR.
- Ubuntu [stable](https://launchpad.net/%7Etmsu/+archive/ubuntu/ppa) and [daily](https://launchpad.net/%7Etmsu/+archive/ubuntu/daily) PPAs are available for Ubuntu 16.04.1+.
- Gentoo `emerge sys-fs/tmsu`.

### Is completion available for my shell?

If your shell is Zsh then yes, completion is in the `misc` directory of the source tree and binary distributable.

## Database
### Where is the database stored?

Whenever you run `tmsu init`, a database file is created at `.tmsu/db` under the
current working  directory and will be  used whenever you're at  or beneath that
path.  For example, if you run `init`  in your home directory, then you will get
a database at `$HOME/.tmsu/db` and any files  you tag in your home directory (or
sub-directories) will go into this database.

To find out which database you are  currently using, run `tmsu info`.  This will
show you the current database (if one can be found), amongst other details.

*Note: Prior to v0.7.0, TMSU would create a default database at `~/.tmsu/default.db` when you first use it.*

### How does TMSU find the database

Whenever you  run TMSU,  it will  look for  a database  at `.tmsu/db`  under the
current working directory.  If none can  be found, TMSU will look for `.tmsu/db`
in each parent directory in turn, up to and including the root directory.

If a database is not found in the current or a parent directory, TMSU will then look for the default
database created by earlier (<v0.7.0) versions of TMSU at `~/.tmsu/default.db`.

### Can I specify the database explicitly?

Yes.  See [Switching Databases](Switching Databases).

### What format is the database?

The database is a SQLite3 database and can be read with the regular SQLite tooling.

    $ sqlite3 ~/.tmsu/db
    ...
    sqlite> .schema
    ...
    sqlite> select * from file;
    ...
    sqlite> .q

### How do I export my data?

The database is a standard Sqlite3  database.  There are several tools available
that can read the database and which can export the rows as CSV, SQL, &c.

To dump to SQL text, you can use the Sqlite3 tooling:

    $ sqlite3 ~/.tmsu/db .dump >dump.sql

# Fingerprint-Algorithms
### What's a Fingerprint?

When you tag a file, TMSU will create a *fingerprint* of the file and store that
in the  database.  Just  as a  person's fingerprint  can uniquely  identify them
within the  global population, a file  fingerprint can uniquely identify  a file
from all the files  in the world.  The chance of  two different files generating
the same fingerprint is statistically extremely unlikely.

(You may also see file fingerprints referred to as 'hashes' or 'digests'.)

### Use In TMSU

TMSU uses the saved file fingerprints for two purposes:

  - Database repairs
  - Duplicate file identification

TMSU can  find the new path  of moved and rename  files by finding the  new path
with  the  same fingerprint.   Duplicate  files  can  be identified  within  the
database as having the same fingerprint and therefore contents.

### Algorithms

By default,  TMSU uses  a modified  version of  the SHA256  algorithm called  'dynamic:SHA256'. This
algorithm was selected as  it will provide excellent security and *adequate*  performance for a wide
range of uses.

Several different file algorithms are supported:

  - none
  - SHA256
  - MD5
  - SHA1
  - dynamic:SHA256
  - dynamic:MD5
  - dynamic:SHA1

SHA1, SHA256 and  MD5 are well known cryptographic hash  functions, all of which
are  adequate  for uniquely  identifying  tagged  files.   MD5  is known  to  be
compromised and SHA1 is theoretically  compromised but for tagging purposes this
is unlikely to pose a problem.

The dynamic versions of the above algorithms behave differently for files larger
than 5MB.  Instead  of calculating a fingerprint for the  whole file's contents,
instead they create  a fingerprint for three  512kB portions of the  file at its
beginning,  middle and  end.   This dramatically  improves  performance on  slow
filesystems, such  as remote filesystems, but  at the risk of  not detecting all
file modifications.  This does not normally cause a problem as larger files tend
to be music or video files, which are rarely if ever modified.  If you do happen
to modify larger files and would like  TMSU to be able to identify them properly
as moved then use one of the non-dynamic algorithms.

### Which File Algorithm Should I Use?

Use the following as a guide to which algorithm you should use:

  - If you do not care about being able to repair moved files or detect
    duplicates then `none` will give the very best performance.

  - For optimum performance whilst maintaining the ability to repair moved
    files and detect duplicates, choose `dynamic:MD5`.

  - For maximum compatibility with other tooling choose `SHA256`.  Although this
    may perform badly with larger files, especially on a remote filesystem.

  - `dynamic:SHA256` is the default because this provides acceptable
    performance, compatibility with other tooling (except on large files) and
    avoids performance problems with large files or on remote filesystems.

### Changing Algorithm

Before changing  the algorithm, ensure  you run a  'tmsu repair' to  fix any file  modifications and
moves  as otherwise  it will  not be  possible to  make these  repairs once  a new  algorithm is  in
operation.

To change algorithm,  use the `config` subcommand.  For example,  to use the MD5
algorithm for files:

    tmsu config fileFingerprintAlgorithm=MD5

To have TMSU recalculate the fingerprints in the database with the new algorithm issue the following
repair command:

    tmsu repair --unmodified

### Symbolic Link Algorithms

*If you are using a version of TMSU before v0.7 then please see the page history for more details.*

As of  TMSU v0.7.0, it is  possible to separately configure  the algorithm used for  symbolic links.
Usually there is no benefit of doing so, but for people using Git Annex or other similar tools there
are options available to use the target file's name instead of its digest.

  - `none`
  - `follow`
  - `targetName`
  - `targetNameNoExt`

The `follow` option, which is the default, uses  the fingerprint of the target file/directory as per
the configured file/directory fingerprint algorithm, respectively.

`targetName`  and  `targetNameNoExt` use  the  symbolic  link's target  file  or
directory's name as  the fingerprint.  This is beneficial if  the target file is
some kind of  identifier, as is the  case when integrating with  Git Annex.  The
`targetNameNoExt` variant will lop off the extension from the target filename.

### Directories

I would like to reintroduce directory fingerprints but it  is difficult to do this in a way which is
both useful and performant.

# Handling-Directories

There are two ways to handle directories: by tagging just the directory or tagging the directory and
all of its contents.

## Tagging Just a Directory

TMSU, by default, does not tag a directory's contents.

    $ tmsu tag /tmp temporary-files

This adds only the `/tmp` directory to  the database.  TMSU does not look inside
the directory.  This makes the tagging  operation fast and the database smaller.
However, querying  the database will show  only the directory entry  and not the
files contents:

    $ tmsu files temporary-files
    /tmp

To list the matching directories' contents combine the query with a call to 'find':

    $ tmsu files temporary-files | xargs find
    /tmp
    /tmp/banana
    /tmp/cucumber
    /tmp/cucumber/kirby

Recursively listing files in  this manner can obviously be slow, especially  if the directories have
lots of files, if the filesystem is inherently slow or is across a network.

If you  tag just the  directory entry TMSU  does not  fingerprint the files  in the directory  so it
cannot report  duplicate files.  Whilst file  entries will not  be shown  in the  virtual filesystem
directly, it is still possible to navigate to the files via the directory symbolic link.

- Quicker to tag
- Smaller database
- No duplicate file detection
- Slower to list tagged files
- Files not shown in the virtual filesystem (but are still accessible)

## Tagging a Directory and its Contents

    $ tmsu tag --recursive /tmp temporary-files

Tagging the  directory recursively adds  every file  from that directory  to the
database, so it can  be slow and results in a  considerably larger database than
tagging the  directory entries  alone.  However  that cost  is borne  only once:
subsequent queries do not need to consult the filesystem:

    $ tmsu files temporary-files
    /tmp
    /tmp/banana
    /tmp/cucumber
    /tmp/cucumber/kirby

In addition,  because the  files are  in the  database it  means they  are shown
directly in the virtual filesystem, though this may clutter the tag directories.
TMSU is also able  to identify duplicate files as a fingerprint  of each file is
taken when it is added.

- Slower to tag
- Larger database
- Duplicate files detected
- Quicker to list tagged files
- Files shown in the virtual filesystem

# Settings
## Settings

Each TMSU database (since version 0.4.0) carries a `setting` table in which
per-database settings can be entered.

## Making Changes

To change  a setting  use the 'config'  subcommand.  Without  arguments 'config'
will  list the  current settings  from  the database,  if present,  or from  the
defaults.

    $ tmsu config
    autoCreateTags=yes
    autoCreateValues=yes
    fileFingerprintAlgorithm=dynamic:SHA256
    directoryFingerprintAlgorithm=none

To change  a setting, assign  a new  value using '='.  For example, to  turn off
automatic tag creation:

    $ tmsu config autoCreateTags=no

## Settings Explained
### Fingerprint Algorithm

`fileFingerprintAlgorithm`: the fingerprint algorithm TMSU uses to identify files by their contents.
See [Fingerprint Algorithms](Fingerprint Algorithms).

Permitted values:

  - `none`
  - `SHA256`
  - `MD5`
  - `SHA1`
  - `dynamic:SHA256` (default)
  - `dynamic:MD5`
  - `dynamic:SHA1`
  - `symlinkTargetName`
  - `symlinkTargetNameNoExt`

`directoryFingerprintAlgorithm`: the fingerprint algorithm TMSU uses to identify directories by their contents.

Permitted values:

  - `none`
  - `dynamic:sumSizes`
  - `sumSizes`

*Note: directory fingerprinting is a work in progress.  Whilst fingerprints can be calculated for directories they cannot currently identified when moved by 'repair'.*

### Automatic Tag Creation

`autoCreateTags`: whether TMSU will automatically create a tag if a file is tagged with a new tag name.

Permitted values:

  - `yes` (default)
  - `no`

When set to `no`, new tags must be created manually using `tmsu tag --create tagname`.

### Automatic Tag Value Creation

`autoCreateValues`: whether TMSU will automatically create a tag value if a file is tagged with a new tag value.

Permitted values:

  - `yes` (default)
  - `no`

When set to `no` it is not possible to create new tag values.
# Switching-Databases
There are several ways to specify the database for TMSU to use:

1. Local database file (`/some/path/.tmsu/db`)
2. Environment variable (`TMSU_DB`)
3. Command-line option (`--database`)
4. Default database file (`$HOME/.tmsu/default.db`)

The recommended way is to initialise a local database.

## Local Database

TMSU  will look  for  a  database named  `.tmsu/db`  under  the current  working
directory  or  any parent  directory  of  the  current working  directory.   For
example, if the current working directory is `/home/on/the/range` then TMSU will
look for a database file at the following paths, using the first it finds:

    /home/on/the/range/.tmsu/db
    /home/on/the/.tmsu/db
    /home/on/.tmsu/db
    /home/.tmsu/db
    /.tmsu/db

This lets  you have a TMSU  database for a particular  set of files.  To  set up
such a  database, use the  `init` subcommand, which  will create a  new database
under the current working directory:

    $ cd /some/path
    $ tmsu init
    Creating new database at '/some/path/.tmsu/db'.

## Environment Variable

TMSU will look for an environment variable called `TMSU_DB`.  This will override
use of the default and local databases.

    $ export TMSU_DB=~/mydb
    $ tmsu tags --all
    fish
    chips

If the file does not exist then it will be created automatically.

## Command-Line Option

The database to use can be specified as a command-line option:

    $ tmsu --database=~/mydb tags --all
    fish
    chips

Use of the  command-line option has the highest precedence  and overrides all of
the other options.  If  this database file does not exist when  TMSU is run then
it will be created automatically.

To save specifying it each time, you can alias `tmsu`:

    $ alias tmsu='tmsu --database=~/mydb'
    $ tmsu tags --all
    fish
    chips

## Default Database

Earlier versions  of TMSU  would create a  database automatically  if none could  be found.  TMSU no
longer creates such a database, but for backward compatibility it will still pick up a database at
`$HOME/.tmsu/default.db` if no other can be found.

# TODO
### In Progress

*This is the task that I am currently working on.*

* Issue #100: Merging tag=value pairs

### High

*This is the stuff I hope to work on next.*

* Windows support
    - Evaluate Dokan for Windows support
    - Ensure 'repair' file move detection works (as it uses / for root)
* Split out API so TMSU can be embedded in other programs
    - I'm thinking, now, that the 'storage' layer is already an API.  Perhaps it would be better
      renamed and marketed as such.
    - Reposition database layer
    - Move core and CLI into separate sub-projects
* Facility for converting tags to values
    - e.g. '2015' to 'year=2015'
    - perhaps via 'rename' subcommand
* Fingerprints of directories
    - `repair` is not repairing directories
* Testing
    - Improve unit-test coverage, especially on 'files' subcommand
    - Add benchmarks
* Case insensitive tag matching
* Issue #23: 'files' is slow

### Medium

*These tasks I hope to work on soon.*

        * Option on 'files' to show tags for files that match query
        * Issue #20: Repairing a moved file should merge tags
            - is this really a good idea? A repaired moved file requires an untagged file which, by definition, has no tags
        * Issue #19: wildcards when matching tags, e.g. `tmsu files she*` would show files
        matching 'sheep', 'sherbet' and 'shenanigans'
            - would have to avoid shell globing
        * Use Markdown instead of homegrown markup
        * Sort values (maybe tags too) numerically where values contain numbers
        * Issue #5: meta-tags (make the values the tags)
        * Issue #22: ability to tag objects within files
            - tmsu tag /some/path#bob hat sunglasses
        * Go Lint
            - On GitHub
        * Code generation
            - http://clipperhouse.github.io/gen/
        * Subcommand aliases and unambiguous shortening
        * Option on 'tags -a' for listing tags that have values
            - should it do this by default?
        * Consider switching from Hanwen to bazil.org
        * Replace tag implication functionality with tag relationships
            - Implication: A ⇒ B        (A => B)
            - Equilavence: A ⇔ B        (A <=> B)
            - Exclusion: A ⇒ ¬B         (A </> B)
        * Improve Zsh query completion
            - Suggestion for tags and operators should be contextual
        * Add recursive option to 'tags' subcommand
        * Basic auto-tags - provide information already store as auto-tags:
            - File size auto:size
            - File/dir auto:type
            - Modificaiton date auto:mod-date
        * Man page generation
        - Sub-command description and options

### Low

*These tasks I hope to do one day but are not currently a priority.*

        * Filesystem watcher
        * Support for whitespace in tag names/values
            - Investigate supporting spaces in tag values (issue #37)
            - Handle apostrophes in queries, i.e. quoted strings
            - Issue #69: Add comma as tag delimiter in --tags form of subcommands
        * Expanded auto-tags phase 2
            - MIME type
            - Image dimensions
            - video length
            - EXIF information
        * Additional VFS operations
            - Tagging file in VFS should add tags to existing entry rather than create
            new one
            - Copying symbolic link from one tag directory to another should add that tag
        * Way to pull tags to parent directory up or push them down to child files
        * Storage level operations should ensure database consistency.  E.g. deleting a tag should result in corresponding taggings being deleted
        # Tag-and-Value-Names
        Valid Tag Names
        ---------------

As of TMSU  v0.6.0, the restrictions on  tag and value names  have been relaxed.
The following are the current rule: please see the page history for restrictions
applicable to earlier versions.

A legal tag name consists of one or more characters from the following Unicode categories:

        - Letter (L*)
        - Number (N*)
        - Punctuation (P*)
        - Symbol (S*)
        - Space (Z*)

Examples of valid tag names:

        - banana
        - 123
        - 6all00n
        - under_scored
        - high-fun
        - !@%&
        - 日本語
        - in space

### Illegal Tag Names

The following names are not allowed:

    .   and  or  not  eq  ne  lt  gt  le  ge
    ..  AND  OR  NOT  EQ  NE  LT  GT  LE  GE

The following characters are not allowed anywhere within a tag name:

        - Slash (/)
        - Backslash (\\)

The  slash and  backslash  character is  illegal  as it  clashes  with the  path
separator  character on  many  operating  systems.  Likewise  '.'  and '..'  are
illegal as  these could  not be used  as directory names  due to  many operating
systems using them already for the current and parent directories aliases.

### Escaping Problematic Characters

Some characters, such as the comparison  operators and space characters, need to
be escaped  if they are  to be used  within a tag  name.  To escape  a character
precede it with a backslash. (You may  also need to additionally using quotes to
hide the escaping from your shell.)

Working  with  the comparison  operator  and  space  characters can  be  tricky,  as the  number  of
backslashes you need may not be immediately obvious.

### Zsh Equals Character Examples

To tag a file with tag `a` and value `b`, the following are all equivalent:

    $ tmsu tag somefile a=b
    $ tmsu tag somefile 'a=b'
    $ tmsu tag somefile "a=b"

To tag a file with tag `a=b`, the following are all equivalent:

    $ tmsu tag somefile a\\=b
    $ tmsu tag somefile 'a\=b'
    $ tmsu tag somefile "a\=b"

To tag a file with tag `a=b` and value `c`, the following are all equivalent:

    $ tmsu tag a\\=b=c
    $ tmsu tag 'a\=b=c'
    $ tmsu tag "a\=b=c"

To tag a file with tag `a` and value `b=c`, the following are all equivalent:

    $ tmsu tag a=b=c
    $ tmsu tag 'a=b=c'
    $ tmsu tag "a=b=c"

# Tricks-and-Tips
## Tagging
### Copy tags from another file

To copy tag our picture `artichoke.jpg` with the same tags as `avocado.jpg`:

    $ tmsu tag --from=avocado.jpg artichoke.jpg

## Querying
### Query for files and show all of the tags for each match

    $ tmsu files photograph country | xargs tmsu tags
    /home/fred/photos/DCSC-142.jpg: country=uk daytime good landscape photo manual-focus
    ...

### List untagged files in the current directory

    $ tmsu untagged

### Include untagged files in a negative query

In a negative query, where you are looking for files that don't have a
particular tag or tags, you may want to include untagged files:

    $ tmsu files --path /animals not hairy && tmsu untagged /animals

## Filesystem Operations

TMSU does not  make any changes to  your files in the filesystem  (other than to
its own database). As  such, TMSU does not include any  functionality for moving
or renaming files.  To make these operations  easier, TMSU now includes a set of
scripts for performing these operations:

### Delete a file

    $ tmsu-fs-rm path/to/file

Alternatively this can be done manually:

    $ rm path/to/file && tmsu untag --all path/to/file

### Move or rename a file

    $ tmsu-fs-mv path/to/file new/path

Or manually:

    $ mv path/to/file new/path && tmsu repair --manual path/to/file new/path

### Merge files

Sometimes you  may wish to  remove duplicates of a  file, e.g. as  identified by
`tmsu  dupes`.  To  combine  multiple  files into  one,  preserving  all of  the
taggings:

    $ tmsu-fs-merge path/to/file1 path/to/keep

This will delete all but the last file specified, applying the tags from each file deleted to the final file.

To do this manually:

    $ tmsu tag --from=path/to/file1 path/to/keep && rm /path/to/file1 && tmsu untag --all /path/to/file1
# Troubleshooting
### Querying files gives a syntax error about `RECURSIVE`

This suggests the version of Sqlite3 you have installed is older than that required by TMSU, as TMSU
makes use of recursive queries that were only supported from version 3.8.3.

* Upgrade to Sqlite3 version 3.8.3 or later.

### Accessing the virtual filesystem results in `invalid ELF header` errors

This either indicates that you have a corrupt library on your system or that a 32-bit process is trying to load a 64-bit shared library.

- Check the files reported are not corrupt.
- Check the settings at `/etc/ld.so.config` do not override where the linker looks for shared libraries.
- Likewise check the contents of the `LD_LIBRARY_PATH` environment variable.

### `Parser stack overflow` when querying the files

This is a Sqlite3 error that indicates that  the SQL parser has built up a stack
that is over its maximum limit.  By default the maximum limit is 100 items which
you are unlikely to hit in practice  unless you are performing some very complex
queries.

If you *do* hit this problem, it is possible to use a bigger stack by changing value in the Sqlite3 source code:

- Edit `$GOPATH/src/github.com/mattn/go-sqlite3/sqlite3.c`
- Search for the line `#define YYSTACKDEPTH 100` and change the `100` to a larger number.
- Recompile go-sqlite3 by running `go install github.com/mattn/go-sqlite3`
- Recompile and reinstall TMSU by running `make && sudo make install` from the TMSU source directory.

# Virtual-Filesystem
## Overview

The virtual  filesystem (VFS) provides  a filesystem  from which you  can browse
your tagged  files.  It provides virtual  directories to represent the  tags and
symbolic  links for  the  tagged  files: linking  back  to  their original  file
locations.  It lets you access your files by way of tags from any other program.

## Mounting The VFS

The easiest way to mount the VFS is with TMSU itself:

    $ mkdir mp
    $ tmsu mount mp
    $ ls mp
    queries  tags

To unmount:

    $ tmsu unmount mp

Alternatively unmount with the FUSE tool. (This approach will work even in the
highly unlikely event that TMSU crashes.)

    $ fusermount -u mp

## Tags Directory

The virtual file system's `tags` directory contains virtual directories for each
tag you have created.  Within these  directories are symbolic links to the files
that have that particular tag applied.  In addition, each tag directory contains
directories for the other  tags applied to the set of files  visible so that you
can hone in on the file you want.

For example:

    $ cd mp/tags
    $ ls
    good  mp3  music  rock  trance

If we drill down into the `mp3` directory we can get symbolic links to our `mp3`
tagged files and see how our `mp3` files have been further tagged.

    $ cd mp3
    $ ls
    total 0
    lrwxr-xr-x 1 paul...06:55 01 - Some Song.1.mp3 -> /home/paul/music/Some Band/Debut Album/01 - Some Song.mp3
    lrwxr-xr-x 1 paul...06:56 02 - Another Song.2.mp3 -> /home/paul/music/Some Band/Debut Album/02 - Another Song.mp3
    lrwxr-xr-x 1 paul...06:56 03 - Yet Another.3.mp3 -> /home/paul/music/Some Band/Debut Album/03 - Yet Another.mp3
    drwxr-xr-x 0 paul...07:03 good
    drwxr-xr-x 0 paul...07:03 music
    drwxr-xr-x 0 paul...07:03 rock
    drwxr-xr-x 0 paul...07:03 trance

You'll probably notice  that the filenames contain a number  where the originals
did not.   This number is TMSU's  internal file identifier: it's  present in the
filename as otherwise there will be a name  clash if you tag two files that have
the same name with the same tag.

We also  have further tag  directories indicating that  our MP3 files  have been
further  (and variously)  tagged `good`,  `music`, `rock`  and `trance`.   If we
change into one  of these directories we can  get a view of the  files that have
both `mp3` and this further tag (e.g. `rock`) applied:

    $ cd rock
    $ ls -l
    total 0
    lrwxr-xr-x 1 paul...06:56 02 - Another Song.2.mp3 -> /home/paul/music/Some Band/Debut Album/02 - Another Song.mp3
    lrwxr-xr-x 1 paul...06:56 03 - Yet Another.3.mp3 -> /home/paul/music/Some Band/Debut Album/03 - Yet Another.mp3
    drwxr-xr-x 0 paul...07:12 good
    drwxr-xr-x 0 paul...07:12 music

## Virtual File System Operations

It's possible to perform a limited set of tag management operations via the
virtual filesystem itself:

    - Create new tags
    - Remove tags from a file

### Create New Tags

To create a new tag using the virtual filesystem, simply create a new directory
under 'tags':

    $ cd mp/tags
    $ ls
    blue  red
    $ mkdir green                      # tmsu tag --create green
    $ ls
    blue  green  red
    $ tmsu tags --all
    blue
    green
    red

### Rename Tags

To rename a tag, simply rename the tag directory:

    $ cd mp/tags
    $ ls
    blue  green  red
    $ mv red maroon                    # tmsu rename red maroon
    $ ls
    blue green maroon

### Untagging a File

Files  can be  untagged by  removing the  symbolic link  from the  tag directory
you  wish  to  remove.  For  example,  to  remove  a  `panorama` tag  from  file
`mountain.jpg`:

    $ ls -l mp/tags/panorama
    total 0
    lrwxr-xr-x 1 ... mountain.1.jpg -> /tmp/mountain.jpg
    lrwxr-xr-x 1 ... vista.2.jpg -> /tmp/vista.jpg
    $ rm mp/tags/panorama/mountain.1.jpg
    $ tmsu tags /tmp/*.jpg
    /tmp/mountain.jpg: photo
    /tmp/vista.jpg: panorama photo

If you remove a symbolic link from a nested tag directory, e.g.
`mp/tags/photo/panorama`, then only the nested tag, `panorama`, is removed:

    $ ls mp/tags/photo/panorama
    vista.2.jpg
    $ rm mp/tags/photo/panorama/vista.2.jpg
    $ ls mp/tags/photo
    vista.2.jpg

### Deleting Tags

A tag can be deleted by removing the tag directory.  A tag directory can only be
deleted if the tag  is no longer applied so it is necessary  to first delete any
symbolic links *immediately* under the tag directory.

It is not necessary to delete the symbolic links under any nested tag
directories and doing so will remove those tags from the files.

    $ ls mp/tags
    photo  panorama
    $ rmdir mp/tags/photo
    rmdir: failed to remove 'mp/tags/photo': Directory not empty
    $ ls mp/tags/photo
    panorama  vista.2.jpg
    $ rm mp/tags/photo/vista.2.jpg      # removes 'photo' from vista.jpg
    $ ls mp/tags/photo
    $ rmdir mp/tags/photo               # deletes the 'photo' tag

Recursive deletion should be avoided as it will delete the tag intended but not
before it has stripped the files that are tagged with it of all tags! For
example:

    $ tmsu tag /tmp/baa.jpg animal sheep photo
    $ ls mp/tags/
    animal  sheep
    $ ls mp/tags/animal
    photo  sheep  baa.1.jpg
    $ rm -r mp/tags/animal              # WARNING non-obvious result
    $ tmsu tags --count /tmp/baa.jpg
    0

### Applying Tags

Currently it is not possible to tag a file via the virtual filesystem.

(The technical reason for  this is that TMSU adds an  identifier to the symbolic
link names to avoid name clashes within the tag directories.  In order to create
a symbolic link in a tag directory you would have to know, in advance, what that
number should be.  I hope to work around this problem in a subsequent version.)

## Queries Directory

Whilst the `tags` directory provides an immediately view of your tags and files,
it does  have some limits: it  is not possible  to exclude tags or  perform more
complicated tag queries.  The `queries`  directory lets you access a query-based
view of your files instead using the same query language as the `files` command.
Simply access the  directory with the query  text as the directory  name to view
the set of files:

    $ cd mp/queries
    $ ls
    $ ls "good and music"
    02 - Another Song.2.mp3
    $ ls
    good and music
    $ ls "good and (music or photo) and not rainy"
    ...

Note that any accessed query directory  is created and saved automatically so it
is not  necessary to first  create them.  The  directories can be  removed using
`rmdir` when you are finished with them or left to ease subsequent access.

## Advanced Mounting

It is also possible to mount the VFS using regular `mount` command.

First, ensure that the `mount.tmsu` helper script is installed in `/sbin`.  This
script is included with  the TMSU binary in the `bin`  directory or is available
in the repository at `misc/bin`.

Check that a TMSU filesystem can be mounted with `mount`. (This must be done as
root until the mount is configured in `/etc/fstab`.)

    $ mkdir mp
    $ sudo mount -t tmsu ~/.tmsu/default.db mp
    $ sudo umount mp

The VFS can then be configured in the `/etc/fstab` for convenience:

    # /etc/fstab
    /home/paul/.tmsu/default.db /home/paul/mp tmsu user,noauto 0 0

This allows the filesystem to be mounted more simply:

    $ mount /home/paul/mp

(For some reason, FUSE only lets root unmount the filesystem: the 'users'
option appears not to be valid for a FUSE filesystem.)

To have the TMSU VFS automatically mount at start up, change `noauto` to `auto`
in `/etc/fstab`.

## Allowing Other Users Access

FUSE allows only root and the mounting user access to the mounted filesystem by
default.  To grant access to other users you must edit `/etc/fuse.conf` and
enable this functionality:

    user_allow_other

Then, when mounting the VFS pass the `allow_other` option:

    $ tmsu mount -o allow_other mp

Or:

    $ mount -t tmsu ~/.tmsu/default.db -o allow_other mp

Or add this option to `/etc/fstab`:

    # /etc/fstab
    /home/paul/.tmsu/default.db /home/paul/mp tmsu user,noauto,allow_other 0 0
##
# Reference

[1]: http://tmsu.org/
[2]: FAQ
[3]: Troubleshooting
[4]: Tricks-and-Tips
[5]: Virtual-Filesystem
[6]: Handling-Directories
[7]: Repairing
[8]: Switching-Databases
[9]: Fingerprint-Algorithms
[10]: Settings
[11]: Database-Schema
[12]: Tag-and-Value-Names
