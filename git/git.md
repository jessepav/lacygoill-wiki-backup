# How to get all the changes introduced by a commit?

    $ git diff COMMIT~ COMMIT

Source: <https://stackoverflow.com/a/17563740/9780968>

---

This is useful when you're looking for  the first commit which has added a given
line of code in a project, but you don't understand its purpose.

Note the commit hash and use the previous command.
You will see all the changes introduced by the commit, in *all* the files of the
project, not just the one file where the line of code was added.
It gives you more context, and may help you better understand the purpose of the
change.

# How to get a url selecting a range of lines in a file hosted on GitHub?

   1. open your file in Vim
   2. visually select the lines
   3. run `:Gbrowse!`

The url should now be in your system clipboard (and printed on the command-line).

This requires the plugins:

   - vim-fugitive
   - vim-rhubarb
   - netrw

##
# gitignore
## Sources
### When Git must decide whether to ignore a path, from which sources does it check gitignore patterns?  (3)

With the following order of precedence, from highest to lowest:

   - from  a `.gitignore` file in the same directory  as the path, or in any
     parent directory, up to the toplevel of the working tree

   - from `.git/info/exclude`

   - from `~/.cvsignore`

### How to decide where to put a gitignore pattern?

If you  want it to be  version-controlled and distributed to  other repositories
via clone (i.e. all developers will also want to ignore it), it should go into a
`.gitignore` file.

If it's specific to a particular repository  but doesn't need to be shared (e.g.
it describes auxiliary files that live inside the repository but are specific to
your workflow), it should go into `.git/info/exclude`.

If it describes  a file you want Git  to ignore in all situations,  it should go
into `~/.cvsignore`.

### When several patterns, from several sources, match for a path, which one wins?

The one in the lowest level file (i.e. the closest one from the path).

`~/.cvsignore` is processed as if it was at the toplevel of the project.

### When several patterns, from the same source, match for a path, which one wins?

The last one.

##
## Patterns
### When a path is matched against a pattern, is it absolute?

No, it's relative to the location of the `.gitignore` file.

`~/.cvsignore` is processed as if it was at the toplevel of the project.

##
### How to exclude all the files under `abc/`?

    abc/
       ^
       tells Git that we only want to exlude a directory `abc/`,
       not files or symlinks `abc`

### Which wildcards can a pattern contain?

   - `*` matches anything except `/`

   - `?` matches any one character except `/`

   - `[]` matches one character in a selected range

For more info, see:

    man 3 fnmatch

Also, in the same manpage have a look at the flag `FNM_PATHNAME`.

### How to make a pattern match only at the beginning of the pathname?

Prefix it with a slash.

As an  example, `/*.c` will  match `foo.c` in  the current directory  (where the
gitignore file lives), but not `dir/foo.c`.

###
### What does `abc/**` match?

All files inside `abc/` with infinite depth.

`abc/` must be in the same directory  as `.gitignore` for a match to occur (i.e.
it's relative to the location of `.gitignore`).

### How to match `a/b`, `a/x/b`, `a/x/y/b`, ...?

    a/**/b

###
### How to re-include a file which has been excluded by a previous pattern?

Use a pattern describing it, and prefix it with a bang:

    tags
    !tags/

Here, the first pattern excludes all files and directories whose name is `tags`,
while the second pattern re-includes the directories whose name is `tags`.
So, in the end, we only exclude the `tags` files.

### When is it impossible to re-include a file?

If one of its parent directory is excluded.

###
### How to include a pattern with a leading hash?  leading bang?  trailing space?

Quote the special character with a backslash:

    \#pat
    pat\ 
    \!pat

##
## Can I ignore already tracked files?

No.

## How to stop tracking a file that is currently tracked?

    $ git rm --cached <file>

FIXME: Are you sure?
https://stackoverflow.com/a/6919257/9780968

---

If the `<file>` has  just been added to the repo (via `$  git add`), then `$ git
rm --cached <file>` unstages the file.

Otherwise, `$  git rm --cached  <file>` unstages the  file, and the  next commit
will remove it from the repo.

---

Remove files from the index, or from the working tree and the index.
The files being  removed have to be identical  to the tip of the  branch, and no
updates  to their  contents can  be  staged in  the index,  though that  default
behavior can be overridden with the `-f` option.
When `--cached` is given, the staged content  has to match either the tip of the
branch or the file on disk, allowing the file to be removed from just the index.

    -f, --force

Override the up-to-date check.

    --cached

Use this option to unstage and remove paths only from the index.
Working tree files, whether modified or not, will be left alone.

---

Effects of `$ git rm --cached <file>`:

If the file was just added to the index:

    A  file
    ?? file~


If the file was already committed:

    D  file
    ?? file


If the file was just modified:

    M  file
      or
     M file
    D  file~
    ?? file~


If the file was modified and staged, then modified again:

    MM file
    D  file~
    ?? file~


Note that in this case you need the `-f` argument:

    $ git rm --cached -f file

To avoid:

       error: the following file has staged content different from both the file and the HEAD:

## ?

Study the effect of these commands:

    $ git rm file
    $ git rm -f file
    $ git rm --cached file

File can be:

   1. ∅∅
   2. A
   3.  M
   4. M
   5. MM

---

Removing the file from the index means one of two things:

   - if `$ git status -s` prints:

           A  file

    it disappears from the index

   - otherwise, `$ git status -s` prints:

           D  file

     The file will be removed from the repo in the next commit.

---

`$ git rm  file` removes the file  from the working tree AND  stages its removal
from the repo.

It works only if the file has NOT been modified compared to:

   - the version from the tip of the branch (last commit of current branch)

   - the version from the index
     (you can ignore this condition if the file is not staged)

---

`$ git rm -f file` removes the file from the working tree AND stages its removal
from the repo.

---

`$ git rm --cached  file` removes the file from the index,  and the file becomes
untracked.

Exception:
If `$ git status -s` reports:

    MM file

the command fails.

Rationale:

If  Git removed  the version  of the  file from  the index,  you would  lose the
changes it contains definitively.
There's no copy anywhere.
In contrast, when `$ git status -s` reports one of:

     M file
    M  file

There's always a copy of the changes (in the version of the working tree).

### 1.

    1. ∅∅

    $ touch abc
    $ git add abc
    $ git commit -m 'msg'
    $ git rm [-f] abc
    'abc' is removed from the working tree and deleted from the index~
    (i.e. it will be removed from the repo in the next commit)~

    $ git rm --cached abc
    D  abc~
    ?? abc~

        the current version of 'abc' becomes untracked
        the version in the repo is removed from the index

### 2.

    2. A

    $ touch abc
    $ git add abc
    $ git rm abc

        error: the following file has changes staged in the index:
            abc
        (use --cached to keep the file, or -f to force removal)

    $ git rm -f abc
    'abc' is removed from the working tree and from the index~

    $ touch abc
    $ git add abc
    $ git rm --cached abc
    'abc' is removed from the index (it's untracked)~

### 3.

    3.  M

    $ touch abc
    $ git add abc
    $ git commit -m 'msg'
    $ echo 'text' >>abc
    $ git rm abc

        error: the following file has local modifications:
            abc
        (use --cached to keep the file, or -f to force removal)

    $ git rm --cached abc
    D  abc~
    ?? abc~

    $ git add abc
    $ git rm -f abc
    'abc' is removed from the working tree and from the index~

### 4.

    4. M

    $ touch abc
    $ git add abc
    $ git commit -m 'msg'
    $ echo 'text' >>abc
    $ git add abc
    $ git rm abc
        error: the following file has changes staged in the index:
            abc
        (use --cached to keep the file, or -f to force removal)

    $ git rm --cached abc
    D  abc~
    ?? abc~

    $ git add abc
    $ git rm -f abc
    'abc' is removed from the working tree and from the index~

### 5.

    5. MM

    $ touch abc
    $ git add abc
    $ git commit -m 'msg'
    $ echo 'text' >>abc
    $ git add abc
    $ echo 'text' >>abc
    $ git rm abc

        error: the following file has staged content different from both the
        file and the HEAD:
            abc
        (use -f to force removal)

    $ git rm -f abc
    'abc' is removed from the working tree and from the index~

##
##
## EXAMPLES

       $ git status
       [...]
       # Untracked files:
       [...]
       #       Documentation/foo.html
       #       Documentation/gitignore.html
       #       file.o
       #       lib.a
       #       src/internal.o
       [...]

       $ cat .git/info/exclude
       # ignore objects and archives, anywhere in the tree.
       *.[oa]

       $ cat Documentation/.gitignore
       # ignore generated html files,
       *.html
       # except foo.html which is maintained by hand
       !foo.html

       $ git status
       [...]
       # Untracked files:
       [...]
       #       Documentation/foo.html
       [...]

Another example:

       $ cat .gitignore
       vmlinux*

       $ ls arch/foo/kernel/vm*
       arch/foo/kernel/vmlinux.lds.S

       $ echo '!/vmlinux*' >arch/foo/kernel/.gitignore

The second `.gitignore` prevents Git from ignoring `arch/foo/kernel/vmlinux.lds.S`.

Example to  exclude everything except  a specific directory `foo/bar`  (note the
`/*`  without the  slash,  the  wildcard would  also  exclude everything  within
`foo/bar`):

       $ cat .gitignore
       # exclude everything except directory foo/bar
       /*
       !/foo
       /foo/*
       !/foo/bar

##
##
##
# How to get a more recent version of Git on Ubuntu, without compiling?

    $ sudo add-apt-repository ppa:git-core/ppa
    $ sudo aptitude update
    $ sudo aptitude safe-upgrade

Source: <https://launchpad.net/~git-core/+archive/ubuntu/ppa>

##
# Compiling Git from source
## download

Download  the  latest  tagged  release  tarball  (`git-X.YY.Z.tar.xz`)  and  its
signature (`git-X.YY.Z.tar.sign`) from one of those links:

- <https://mirrors.edge.kernel.org/pub/software/scm/git/>
- <https://github.com/git/git/releases>

Github doesn't provide signatures, but is easier to find the latest release.

## check the signature of the tarball

          ┌ write the decompressed data to STDOUT instead of a file
          │
          │┌ decompress
          ││                           ┌ assume that:
          ││                           │     - the next argument is a detached signature
          ││                           │     - the next one is the signed data
          ││                           │
          ││                           │ verify the signed data using the signature
          ││                           │
          ││                           │                           ┌ read the signed data from STDIN
          ││                           │                           │
    $ xz -cd git-2.19.2.tar.xz | gpg --verify git-2.19.2.tar.sign  -
    gpg: Signature made Wed 21 Nov 2018 04:04:41 PM CET using RSA key ID 96AFE6CB
    gpg: Can't check signature: public key not found

If the signature can't be verified, note the ID of the public key which was used
to sign the tarball (here it's `96AFE6CB`).
Use the ID to import the public key:

    $ gpg --keyserver hkp://keys.gnupg.net --recv-keys 96AFE6CB
    gpg: requesting key 96AFE6CB from hkp server keys.gnupg.net~
    gpg: key 713660A7: public key "Junio C Hamano <gitster@pobox.com>" imported~
    gpg: no ultimately trusted keys found~
    gpg: Total number processed: 1~
    gpg:               imported: 1  (RSA: 1)~

Try again to verify the signature:

    $ xz -cd git-2.19.2.tar.xz | gpg --verify git-2.19.2.tar.sign -
    gpg: Signature made Wed 21 Nov 2018 04:04:41 PM CET using RSA key ID 96AFE6CB~
    gpg: Good signature from "Junio C Hamano <gitster@pobox.com>"~
    gpg:                 aka "Junio C Hamano <jch@google.com>"~
    gpg:                 aka "Junio C Hamano <junio@pobox.com>"~
    gpg: WARNING: This key is not certified with a trusted signature!~
    gpg:          There is no indication that the signature belongs to the owner.~
    Primary key fingerprint: 96E0 7AF2 5771 9559 80DA  D100 20D0 4E5A 7136 60A7~
         Subkey fingerprint: E1F0 36B1 FEE7 221F C778  ECEF B0B5 E886 96AF E6CB~

This time, you should read “Good signature from ...”.

## configure

    $ xt git-X.YY.Z.tar.xz

    $ make configure

    $ ./configure --prefix=/usr/local

## compile and install

    $ make

    $ sudo checkinstall

## update

Now, you can get the latest updates with your compiled `git`:

    $ git clone git://git.kernel.org/pub/scm/git/git.git

##
# Concepts
## What's the difference between an author and a committer?

The author is the person who originally wrote the work, whereas the committer is
the person who last applied the work.
So, if you send in a patch to a  project and one of the core members applies the
patch, both of you get credit.
You as the author, and the core member as the committer.

## Why does Git uses the word “checkout” when we switch branches?

Theory:

Git CHECKS in `.git/`  the tree of files matching the branch  we want, then pull
them OUT into our working directory.

##
## What's the working tree?

A single checkout of one version of the project.
These files are pulled  out of the compressed database in  `.git/` and placed on
disk for you to use or modify.

## What's the staging area?

A file  in `.git/`  that stores information  about what will  go into  your next
commit.
Its technical name in Git parlance is the “index”.

### What's its purpose?

It gives you control over which file you want to commit, and in which version.

Without it, when  committing, Git would take  a snapshot of all  new or modified
files, in their latest versions.
This may be undesirable because of the  nature of some of the files (e.g. binary
or temporary files) or because of their  versions (you may want to commit an old
version, not the latest one).

##
## What's an untracked file?

A file which was not in your last commit and is not in your index.

## What's a modified file?

A file which  you have changed since  it was checked out /  committed, but which
you haven't staged/committed yet.

## What's a staged file?

A file which you  have changed (or a new untracked file), and  marked to go into
your next commit, in its current version, by adding it to the index.

## What's a committed or unmodified file?

A file which is safely stored in `.git/`.

##
# Documentation
## How to get a list of all available
### subcommands?

    $ git help -a

### guides?

    $ git help -g

##
## How to get the manpage of a subcommand?  (2)

    $ man git-subcommand

    $ git help subcommand

## How to get a usage message and the list of all available options of a subcommand?

    $ git <subcommand> -h

###
# Config
## Where can I find information about how to config Git?

    man git-config

##
## How to change the location of the base of the repository (`.git/`)?

Set `$GIT_DIR`, or use the `--git-dir` command-line option:

    $ GIT_DIR=my_base git init

    $ git --git-dir my_base init

##
## An option name is a dot separated list of words.
### How is the first one called?

The section.

### How is the last one called?

The key.

### If there're more than 2 words, how are the middle ones called?

The subsections.

##
## Which file(s) does Git open by default
### to read an option?

Everywhere, i.e. in the system, global and repository-local configuration files:

    /etc/gitconfig
    ~/.gitconfig  or  ~/.config/git/config
    .git/config

### to write an option?

In the repository-local configuration file:

    .git/config

##
## How to specify which file(s) I want Git to open, when reading/writing an option?

Use one of these options:

    ┌──────────────────┬──────────────────────────────────────┐
    │ option           │ read/write only from/into            │
    ├──────────────────┼──────────────────────────────────────┤
    │--system          │ /etc/gitconfig                       │
    ├──────────────────┼──────────────────────────────────────┤
    │--global          │ ~/.gitconfig or ~/.config/git/config │
    ├──────────────────┼──────────────────────────────────────┤
    │--local           │ .git/config                          │
    ├──────────────────┼──────────────────────────────────────┤
    │--file <filename> │ <filename>                           │
    └──────────────────┴──────────────────────────────────────┘

##
## Which file(s) does Git open when I run `$ git config [--system|--global|--local]`?

    ┌──────────────────────┬─────────────────────────┐
    │ command              │ opened file             │
    ├──────────────────────┼─────────────────────────┤
    │ git config --system  │ /etc/gitconfig          │
    ├──────────────────────┼─────────────────────────┤
    │ git config --global  │    ~/.gitconfig         │
    │                      │ or ~/.config/git/config │
    ├──────────────────────┼─────────────────────────┤
    │ git config [--local] │ .git/config             │
    └──────────────────────┴─────────────────────────┘

### In case of conflict, which one has the priority?

The more specific the option is, the more priority it has.

   1. /etc/gitconfig          |
                              |
   2. ~/.config/git/config    | more priority
                              |
   3. .git/config             v

##
## Reading options
### How to read the value given to the option `user.name`
#### for the current repo?

    $ git config [--local] user.name
                 ├───────┘
                 └ optional because even if Git will look in all the configuration files,
                   it will only print the last value it finds,
                   which will be in `.git/config` if you're in a git repo

#### for all my repos?

    $ git config --global user.name

#### for all the users on the system?

    $ git config --system user.name

#### for any scope?

    $ git config --get-all user.name
                 ^^^^^^^^^

####
### How to read
#### the file from which the option `user.name` received its value?

    $ git config [--global|--system] --show-origin user.name
                                       │
                                       └ requires at least Git version 2.8.0

####
#### all my options local to the current repo?

    $ git config --local --list

Here, `--local` is not optional.
If you  omit it, Git  will list all options  regardless of their  scope (system,
global, local).

#### all my options global to all my repos?

    $ git config --global --list

#### all the system options?

    $ git config --system --list

#### all the options which have been changed thus far?

    $ git config --list

##
#### Why can I see several identical options with different values?

Git may  read the same  option from different files  (`~/.config/git/config` and
`.git/config` for example).

##### Which one is applied?

The last one.

###
## Writing options
### How to set my user name and my email address?

    $ git config --global user.name  'John Doe'
    $ git config --global user.email 'johndoe@example.com'

If you want to override this with a different name or email address for specific
projects, you can  run the command without the `--global`  option when you're in
that project.

#### How will this information be used?

It's baked in  every commit to idenfity  the author of a patch  (i.e. the person
who wrote the code).

It's not used to automatically give your credentials when pushing a commit.

###
### How to set my default editor?

    $ git config --global core.editor vim

#### How will this information be used?

It determines  which editor  will be  started when Git  needs you  to type  in a
message.

#### Which editor will Git start if I don't set it?

Git will use `$EDITOR`.

###
### How to assign a value containing a whitespace to an option?

Quote it:

    $ git config user.name 'John Doe'

OTOH, there's no need to, if the value doesn't contain any whitespace:

    $ git config user.name John_Doe

### What happens if I execute `$ git config user.name John` outside a git repo?

It fails, because Git uses the `--local` scope by default.

##
## Ignoring files
### I've created a global gitignore file.  From which directory of the project is it applied?

From the root of the project.

This matters for example, if you write `/pattern`.
The slash stands for “only in the current directory”.
The notion of current directory is affected by where the gitignore file lives.
A global gitignore lives  outside the project, but is processed as  if it was at
its root.

### I wrote `tags` in a gitignore file.  In which directory of the project will a `tags` entry be ignored?

Any.

A pattern is applied recursively throughout the entire working directory.

###
### How to ignore a `tags` entry but only in the current directory (the one where the gitignore file lives)?

Prefix `tags` with a slash:

    /tags

### How to ignore any directory named `tags/`?

Append `tags` with a slash:

    tags/

### How to ignore any file named `tags`?

    tags
    !tags/

The first pattern  makes Git ignore any file  named tags (✔), and any  file in a
directory named tags (✘).
The second pattern makes Git NOT ignore any file in a directory named tags (✔).

###
### What's the difference between the patterns `tags` and `tags/`?

`tags/` makes Git ignore any file in a `tags/` directory.

`tags` makes Git ignore any file in a `tags/` directory, but also any file named `tags`.

###
### Does Git track an empty directory?

No.

### Does Git track a non-empty directory in which there are only ignored files?

No.

##
# Usage
## How to clone the repo at `<url>` inside the directory `dir/`?

    $ git clone <url> dir

This has nothing to do with the `-C` option.
`-C dir` tells  Git to temporarily change the shell  working directory to `dir/`
while executing the command.
And it doesn't create a new directory.

OTOH, the second optional  argument passed to `$ git clone`  doesn't tell Git to
change its working directory.
It just  tells Git to  rename the new  directory in which  we want to  clone our
repo.

##
## How to stage all the files under a directory?

    $ git add <dir>

That's why this command works:

    $ git add .

##
## I've staged a file (version A), then modified it (B), and finally committed it.  Which version has been committed?

A.

Because it's the one at the time you ran `$ git add`.

### How to make sure version B is committed?

Re-add the file to the index:

    $ git add file

The new version B will overwrite the existing version A inside the index.

##
## I've run `$ git status -s`, there are 2 columns of indicators in front of each file.
### What does each of the 2 columns stand for?

The status of files in:

   - the index
   - the working directory

### What does it mean to read a
#### `M` in the left column?

The file  has been modified since  the last commit,  and is staged for  the next
one.

#### `M` in the right column?

The file has been modified since the last commit, but is NOT staged for the next
one.

#### `M` in both columns?

There's  a modified  version of  the  file in  the index  (staged), and  another
modified version of the file which is NOT in the index (UNstaged).

So, you probably did sth like:

    # edit file which creates version A
    $ vim file

    # stage version A
    $ git add file

    # edit file which creates version B
    $ vim file

The first `M` is for version A, the second one for version B.

#### `A` in the left column?

The file is new (it wasn't tracked before) and has been added to the index.

#### `D` in the left column?

The file will be removed from the repo in the next commit.

But not from the working tree: there will still be a local copy.
Basically, the file is going to be UNversioned.

#### `D` in the right column?

The file has been removed from the working tree.

#### `?` in both columns?

The file is untracked.

##
##
##
# ?

    $ git config --global core.excludesfile  ~/.cvsignore
    $ git config --global merge.tool         vimdiff

Configuration post-installation de Git.

Définition du:

   - fichiers à ignorer dans tous les repos (utile pour les fichiers tags)
   - programme à invoquer qd on exécute `git mergetool`

---

    credential.helper cache
    credential.helper 'cache --timeout=3600'

Active la  mise en cache du  pseudo et du mdp  pendant 15 minutes (défaut)  ou 1
heure (custom).
Utile pour ne pas avoir à redonner son mdp pour chaque commit.

---

    commit.template    ~/.config/git/message.txt

Template de message pour les commits.

Avec   la   valeur   utilisée   ici,   le  template   doit   être   écrit   dans
`~/.config/git/message.txt`.

---

    help.autocorrect 10

Qd  on fait  une  erreur de  typo  en tapant  une commande,  Git  fait tjrs  une
auto-correction.

Cette config lui demande d'attendre 1s avant de la valider.

La valeur est un entier correspondant à une durée en dizièmes de seconde.

---

    user.signingkey <gpg-key-id>

ID de la clé GPG à utiliser pour signer un tag. Facilite la signature d'un tag:

    git tag -s <tag-name>

Plus besoin de spécifier l'id via `-u <keyid>`.

---

    core.excludesfile    ~/.cvsignore

Définit `~/.cvsignore` comme étant une sorte de fichier `.gitignore` global.

Tous les patterns qu'il contient seront ignorés quel que soit le repo.

   - *~           emacs
   - .*.swp       vim
   - .DS_Store    Mac OS X

Git  ne considèrera  jamais un  fichier dont  le nom  correspond à  l'un de  ces
patterns,  comme non  suivi (untracked),  et ne  tentera jamais  de l'ajouter  à
l'index si on exécute `git add` sur lui.

---

    $ cat <<'EOF' >.cvsignore
    *.[oa]          # pas de fichier portant l'extension `.o` ou `.a`
    !lib.a          # n'ignore pas les fichiers `lib.a`, malgré la précédente règle

    /TODO           # pas de fichier TODO à la RACINE du dossier courant (n'ignore pas subdir/TODO)
    build/          # "              du dossier `build/`
    doc/*.txt       # "              portant l'extension `txt` à la racine d'un dossier `doc/`
    doc/**/*.pdf    # "                                  `pdf` n'importe où sous un dossier `doc/`
    EOF

Exemple de contenu d'un fichier `.cvsignore`.
Chaque repo peut disposer d'un fichier de ce type.

Un fichier dont le  nom correspond à l'un des patterns écrit  dans ce fichier ne
sera jamais considéré comme non suivi, et ne sera jamais ajouté à l'index.

Il est IMPORTANT de configurer ce fichier avant de commencer à travailler sur un
repo, pour éviter de valider un commit  contenant des fichiers qu'on ne veut pas
voir au sein du repo.

À l'intérieur des patterns, on peut utiliser les métacaractères suivant:

   - !        ne pas ignorer le pattern qui suit, même si une règle précédente l'exige

   - *        n'importe quelle suite de caractères

   - **       n'importe quelle arborescence de dossiers ; ex:

                  a/**/z  matchera  a/z, a/b/z, a/b/c/z, ...

   - ?        n'importe quel caractère

   - [abc]    collection de caractères (ici, a, b, ou c)

   - [0-9]    rangée de caractères (ici, chiffre de 0 à 9)

   - /        en début de pattern: oblige ce dernier à être matché à la RACINE
                                   du dossier courant
              en fin   de pattern: traite ce dernier comme un dossier, dont le CONTENU
                                   doit être ignoré

---

To read:

- <https://augustl.com/blog/2009/global_gitignores/>
- <https://help.github.com/articles/ignoring-files/#create-a-global-gitignore>

##
# Script
## How to prevent Git from waiting for my credential when I call it from a script to push a commit?

    export GIT_TERMINAL_PROMPT=0

If this environment  variable is set to  0, git will not prompt  on the terminal
(e.g., when asking for HTTP authentication).

##
##
##
# How to version control my config files?

    $ git init --bare $HOME/.cfg
    $ alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
    $ config config --local status.showUntrackedFiles no
    $ config status
    $ config add ~/.vim/vimrc
    $ config commit -m 'add vimrc'
    $ config remote add origin https://github.com/lacygoill/config.git
    $ config push -u origin master

Source:

- <https://news.ycombinator.com/item?id=11070797>
- <https://developer.atlassian.com/blog/2016/02/best-way-to-store-dotfiles-git-bare-repo/>

Alternatives:

<https://www.reddit.com/r/vim/comments/9tzk2o/is_there_a_way_to_store_my_vimrc_on_github_and/>

---

TODO: Learn how to have multiple working directories.
This would allow us to version control files in `/etc`:

<https://stackoverflow.com/questions/6270193/multiple-working-directories-with-git>

In the meantime, you can create a hard  link inside your home pointing to a file
in `/etc`, and version control this hard link.
Git will back up the contents of the file.
With a soft link, git would just back up its path.

---

Also, document this:

<https://news.ycombinator.com/item?id=11071976>

##
# Commands
## How to find the first commit from which some project exhibits a new behavior (like a bug)?

    $ git bisect start
    $ git bisect new
    $ git bisect old v1.2.3

`git bisect new` specifies that the current commit exhibits the new behavior.
`git bisect old  v1.2.3` specifies that the commit tagged  `v1.2.3` exhibits the
old behavior; you can also specify a commit via its sha1 (full or partial).

git should check out a commit in the middle of the range of commits, between the
"old" and "new" commits.  Test whether  the project exhibits the new behavior on
this commit.  If you can, run:

    $ git bisect new

If you can't, run:

    $ git bisect old

Repeat the process until git can tell you which commit introduced the new behavior.
Once you're finished, run:

    $ git bisect reset

to get back on the commit you were on before running `git-bisect(1)`.

### On some commit, I can't test the project!

Run this:

    $ git bisect skip

Note that git may be unable to find the desired commit.
It should still narrow down the search to only a few candidates.

### How to automate the process?

                       ┌ commit exhibiting new behavior
                       │    ┌ commit exhibiting old behavior
                       │    │
    $ git bisect start v3.4 v1.2
    $ git bisect run /path/to/custom-script

The custom script must exit with the error code:

   - 0 if the old behavior can be reproduced on the current commit
   - 1 if the new behavior can be reproduced
   - 125 if there's no way to tell whether the old or new behavior can be reproduced
     (e.g. the compilation fails)

You  can replace  the script  with any  shell command  which exits  with 0  or 1
depending on whether the current commit exhibits the old or new behavior.

###
### After having marked some revisions as old/new, how to get a summary of what I have done so far?

    $ git bisect log

You should see sth like:

    git bisect start
    # new: [dd5299841a87c0bf842488f7f9feb84b7e37c819] Merge branch 'obsd-master'
    git bisect new dd5299841a87c0bf842488f7f9feb84b7e37c819
    # old: [bbcb19917447b960b355ace88ce25c70cf2fd245] 3.0 version.
    git bisect old bbcb19917447b960b355ace88ce25c70cf2fd245
    # old: [444e9f3c582b2d20800b0fe4aa363fb7e801cbc2] Bump 3.1-rc up to master.
    git bisect old 444e9f3c582b2d20800b0fe4aa363fb7e801cbc2
    # old: [450315aa74c9821ce1bc8c4d51f7ab4abf55993a] Merge branch 'obsd-master'
    git bisect old 450315aa74c9821ce1bc8c4d51f7ab4abf55993a
    # skip: [deffef6f1378db4986941dd9d83ba61f11142cd8] Reset background colour on scrolled line.
    git bisect skip deffef6f1378db4986941dd9d83ba61f11142cd8

### I made a mistake when marking a revision!

    $ git bisect log >/tmp/git-bisect.log
    $ vim /tmp/git-bisect.log
    " edit the file to remove the entry matching the revision for which you specified a wrong status
    $ git bisect reset
    $ git bisect replay /tmp/git-bisect.log

###
### How to see the currently remaining commits which git is still bisecting?

    $ git bisect visualize

If you  have installed  `gitk(1)`, a  GUI window will  open and  offer different
views in a single screen (otherwise `git-log(1)` will be invoked); in `gitk(1)`,
you can navigate between the commits with the arrow keys.

#### That's too verbose!

    $ git bisect visualize --oneline
                           ^^^^^^^^^

This time, `git-log(1)` is invoked no matter what.

##
## git-blame

    $ git blame -L 12,34 file

Annote les lignes 12 à 34 de `file` avec les infos suivantes:

   - le sha1 partiel du dernier commit l'ayant modifiée

   - qui l'a écrite

   - quand

L'option `-L` est facultative.
Sans elle, on obtient la même sortie que `:Gblame`.

Si git préfixe un sha1 partiel par un  `^`, ça signifie que la ligne n'a pas été
changée depuis le commit ayant inclut le fichier.

Exemple d'annotation:

    ┌ sha1 partiel
    │         ┌ auteur
    │         │         ┌ date
    │         │         │
    b66520f2 (lacygoill 2017-07-05 22) " some comment
                                   │   │
                                   │   └ contenu
                                   └ n° de ligne

    ^bfeb373 (lacygoill 2017-02-16 23) "
    │
    └ la ligne est là depuis le début

---

La  recherche par  dichotomie et  l'annotation  de fichier  sont des  techniques
complémentaires pour  trouver l'origine  d'un problème: la  1e permet  permet de
trouver son commit d'origine, la 2nde son auteur.

---

    $ git blame -C -L 12,24 fileB

L'option `-C`  demande à `git  blame` de  vérifier si un  snippet de code  a été
copié depuis  un autre  fichier (`fileA`)  qui aurait été  modifié dans  un même
commit.

Si c'est le cas, pour l'annotation de  chaque ligne du snippet, git utilisera le
dernier commit ayant modifié la ligne dans `fileA`.

Sans  `-C`, git  utiliserait  le  dernier commit  ayant  modifié  la ligne  dans
`fileB`.

Càd le commit où on a déplacé la ligne de `fileA` vers `fileB`.

On peut répéter `-C` 2 à 3 fois pour que git cherche l'origine d'un snippet dans
davantage de fichiers:

    -CC     les fichiers présents dans le commit ayant créé `fileB`
            pas juste ceux qui ont été modifiés

    -CCC    les fichiers présents dans n'importe quel commit

Exemple d'annotation via `git blame -C`:

    f344f58d fileA (Scott 2009-01-04 12)
    f344f58d fileA (Scott 2009-01-04 13) - (void) gatherObjectShasFromC
    f344f58d fileA (Scott 2009-01-04 14) {
    70befddd fileA (Scott 2009-03-22 15)         //NSLog(@"GATHER COMMI
    ad11ac80 fileB (Scott 2009-03-24 16)
    ad11ac80 fileB (Scott 2009-03-24 17)         NSString *parentSha;
    ad11ac80 fileB (Scott 2009-03-24 18)         GITCommit *commit = [g
    ad11ac80 fileB (Scott 2009-03-24 19)
    ad11ac80 fileB (Scott 2009-03-24 20)         //NSLog(@"GATHER COMMI
    ad11ac80 fileB (Scott 2009-03-24 21)
    56ef2caf fileA (Scott 2009-01-05 22)         if(commit) {
    56ef2caf fileA (Scott 2009-01-05 23)                 [refDict setOb
    56ef2caf fileA (Scott 2009-01-05 24)

## divers

    $ git add .
    $ git add <file> [...]

Ajoute tout le contenu du dossier à l'index.

Ajoute `<file>`  à l'index du  dépôt pour qu'il soit  tracké et indexé  s'il est
nouveau, ou juste indexé s'il était déjà tracké mais modifié.

L'index est stocké dans le binaire `.git/index`.

---

    $ git branch

Affiche le nom des branches existantes.
La branche sur laquelle on travaille étant précédée d'un astérisque.

Quand on veut  faire une expérimentation ou tester  une nouvelle fonctionnalité,
on crée une nouvelle branche (légère divergence de la base de code principale).

Si au bout  d'un moment on est  satisfait du résultat, on la  fusionnera avec la
branche principale.

---

    $ git checkout <sha1>
    $ git checkout -- <file> ...

Se repositionner sur le commit d'empreinte <sha1> (retour dans le passé).

Annuler les modifications apportées à <file> ..., y compris une suppression.


    ┌──────────────────────────────┬────────────────────────────────────────────────────┐
    │ git checkout -b foo          │ crée la branche foo                                │
    ├──────────────────────────────┼────────────────────────────────────────────────────┤
    │ git checkout foo             │ passe sur la branche foo                           │
    ├──────────────────────────────┼────────────────────────────────────────────────────┤
    │ git branch -d foo            │ supprime la branche locale foo                     │
    ├──────────────────────────────┼────────────────────────────────────────────────────┤
    │ git push origin --delete foo │ supprime la branche foo sur le repo distant origin │
    └──────────────────────────────┴────────────────────────────────────────────────────┘


---

    $ git commit [-a] [-m "msg"]  commit ;

L'option -m permet de lui associer un message.

Si elle est  absente, Vim se lance  pour qu'on écrive un message  car un message
est obligatoire.

Il est important car  il permet de donner du sens aux  changements qu'on fait et
de s'y retrouver plus tard.

L'option `-a`  indique à Git que  tout fichier du  dépôt qui a été  modifié doit
être réajouté à l'index, mais n'est  pas utilisable pour un tout nouveau fichier
évite de devoir taper `git add` pour chacun.

---

    $ git config --get remote.origin.url

Retourne l'url du dépôt central, stockée dans `.git/config`.

---

    $ git diff
    $ git diff --cached

Affiche les différences entre le working tree et:

   - le dernier commit
   - l'index

---

    $ git init

Transforme le dossier courant en dépôt Git (en créant un sous-dossier `.git/`).

---

    $ git log

Affiche tous les commits effectués sous la forme de plusieurs informations, dont
le nom de l'auteur, la date, le message et le sha1 du commit.

Le log tient compte des repositionnements via la commande checkout.
Autrement dit, un retour dans le passé implique que des commits disparaissent du
log

---

    $ git log -S <STRING> --all --source -p | vipe

Affiche le(s) commit(s) ayant ajouté ou supprimé la chaîne <STRING>.

    --all       start from every branch
    --source    show which branch lead to each commit found
    -p          show the patch that each commit has introduced

Si on cherche une regex plutôt qu'une chaîne, il faut remplacer le flag `-S` par
`-G`.

Source:    http://stackoverflow.com/a/5816177

---

Pour lire les commentaires de l'auteur  d'un commit sur github, chercher dans le
buffer Vim le pattern `^commit`.

On peut en trouver plusieurs.

Les passer en revue, du dernier (en bas du buffer) au premier.

Pour chacun  d'eux, faire  une recherche de  son sha1 depuis  le repo  github du
projet.

Un résultat sera trouvé dans l'onglet ’Commits’ (et pas dans ’Code’).

---

    $ git ls-files {--stage | -s}

Affiche les droits, le sha1 et les chemins vers les fichiers de l'index.

---

    $ git pull <repo> <branch>

Récupère  les derniers  changements depuis  le  dépôt central  / upstream;  plus
rapide qu'un clonage intégral et donc régulièrement répétable.

---

    $ git push [-u] <repo> <branch>

Envoie les changements sur la branche <branch> du dépôt <repo>.

Si on utilise un dépôt github, par défaut, <repo> = origin.

Le flag optionnel  `-u` permet de configurer cette branche  comme la branche par
défaut pour les prochains pull / push.

Forme abrégée de `--set-upstream-to`.

---

    $ git reflog

Affiche tout ce qui est arrivé au dernier commit.

Permet de récupérer l'id d'un commit  supprimé et de se repositionner dessus via
un:

    $ git reset --hard id


    $ git remote add <fork> <url>
    $ git fetch <fork>
    $ git checkout -b <fork_branch> <fork>/<branch>

Les 2  premières commandes importent  les branches  du dépôt dont  l'adresse est
`<url>`, à l'intérieur du repo local.

Au passage, leur repo d'origine est nommé `<fork>`.

La 3e  commande crée  la branche  `<fork_branch>` en  copiant `<fork>/<branch>`,
c'est-à-dire la branche `<branch>` du repo distant, appelé localement `<fork>`.
<http://stackoverflow.com/a/14383288>

---

    $ git rev-parse HEAD
    $ git reset --hard <sha1>

Affiche le sha1 du dernier commit.

Restaure le working tree  dans l'état où il était au  moment du commit identifié
par `<sha1>`.

Les 2 commandes peuvent être combinées:

    $ git reset --hard $(git rev-parse HEAD)

    $ git reset --hard <sha1>

Repositionne la  tête (le  dernier commit)  sur le  commit dont  l'empreinte est
`<sha1>`.

Supprime tous les commits qui suivent.

On peut se  contenter de taper uniquement les premiers  chiffres de l'empreinte,
généralement les 4 premiers chiffres suffisent pour une identification.

---

    $ git reset --hard HEAD~1

Repositionne la  tête sur l'avant-dernier commit  (HEAD~2 = avant-avant-dernier,
...).

---

    $ git reset --hard HEAD

Repositionne la tête sur le dernier commit.

N'efface  aucun commit,  mais  efface  tous les  changements  effectués dans  le
dossier de travail et ds l'index depuis le dernier commit.

---

    $ git rev-parse --abbrev-ref HEAD

Affiche la branche locale courante/active.

---

    $ git show
    $ git show --oneline

Montre le commit sur lequel pointe `HEAD`.

La 2e version  présente une version abrégée,  avec juste le sha1  partiel, et le
titre du commit.

---

    $ git stash
    $ git stash apply

Cache / Réapplique les changements non-commits du cwd.

---

Qd on expérimente une branche, pour que les changements ne soient appliqués qu'à
cette dernière, il faut obligatoirement les commit ou les cacher.

Autrement, ils seront appliqués à toutes les branches.

---

    $ git status

Indique si on se  trouve ou non dans un dépôt Git, si  la branche de notre dépôt
local est en avance  par rapport à celle du dépôt distant, et  si des fichiers /
dossiers sont untracked, ou staged mais pas committed.

##
# Fork
## How to update a fork?

    $ git clone git@github.com:YOUR-USERNAME/YOUR-FORKED-REPO.git
    $ cd into/cloned/fork-repo
    $ git remote add upstream git://github.com/ORIGINAL-DEV-USERNAME/REPO-YOU-FORKED-FROM.git
    $ git fetch upstream
    $ git pull upstream master
    $ git push

<https://gist.github.com/CristinaSolana/1885435>

##
# Pull Request
## How to create one?

   1. fork the project

   2. clone the fork locally

   3. create a topic branch (new branch with telling name):

        $ git checkout -b my-branch

      this makes it easier to push follow-up commits if you need to update your proposed changes

   4. edit files

   5. commit the changes with a telling message:

        $ git add .
        $ git commit -v

   6. push the commit to the fork repo:

        $ git push origin my-branch

   7. on github, switch to `my-branch`, and check this kind of message is displayed:

        This branch is 1 commit ahead of <project>:master

   8. click on the `Compare` button (not on `Compare & pull request`)

On the top line, make sure the settings in dropdown menus are correct:

    ┌─────────────────┬───────────────────────────────────────┐
    │ base repository │ remote repo (e.g. `vim/vim`)          │
    ├─────────────────┼───────────────────────────────────────┤
    │ base            │ remote branch (e.g. `master`)         │
    ├─────────────────┼───────────────────────────────────────┤
    │ head repository │ fork repo (e.g. `lacygoill/vim`)      │
    ├─────────────────┼───────────────────────────────────────┤
    │ compare         │ branch on fork repo (e.g. `fix-typo`) │
    └─────────────────┴───────────────────────────────────────┘

Below, make sure the files contain the changes you want your PR to include.

   9. click on the `Create pull request` button

   10. give a title to the PR (by default, it's the one of the commit)

   11. describe the PR in a message below the title

   12. click on the `Create pull request` button

Once the PR has been sent, any new  commit which is pushed toward your branch on
your fork will be automatically added to the PR.

For more info, see: <https://help.github.com/articles/using-pull-requests/>

### The title/message of my commit contains an error!  How to fix it?

    $ git commit --amend

Fix the error in your editor, then:

    $ git push --force origin my-branch

##
## How to test an existing one?

For Vim:

    # may fail if you did it already; in that case, ignore the error and go on
    $ git remote add upstream git://github.com/vim/vim.git

    # when looking for the PR branch, ignore the name of the user before the colon, and ignore the colon as well
    $ git fetch upstream pull/<PR-id>/head:<PR-branch>

    $ git checkout <PR-branch>

For more info, see: <https://github.com/TeamPorcupine/ProjectPorcupine/wiki/How-to-Test-a-Pull-Request>

##
# Github

Chaque projet peut être cloné via https ou ssh. Pour plus d'infos:

- <https://help.github.com/articles/which-remote-url-should-i-use/>
- <https://help.github.com/articles/generating-an-ssh-key/>

L'avantage de ssh est de ne pas avoir besoin de fournir ses identifiants dans le
terminal à chaque fois qu'on push / pull.

Pour supprimer un dépôt (pex un fork devenu inutile):

   1. sélectionner le dépôt
   2. Settings (roue dentée; les settings du dépôt, pas ceux du profil)
   3. Delete this repository (dans la zone rouge "Danger Zone")

Pour link un passage précis dans un bout de code:
cliquer sur le n° de la 1e ligne, shift clic sur le n° de la dernière ligne, <y>.

    ┌─────────┬─────────────────────────────────────────────────────────────────┐
    │ <t>     │ permet de filtrer les fichiers d'un dépôt en donnant un mot-clé │
    ├─────────┼─────────────────────────────────────────────────────────────────┤
    │ history │ bouton visible quand on lit le contenu d'un fichier             │
    │         │ (Raw - Blame - History)                                         │
    │         │ équivalent de `git log` en local,                               │
    │         │ donne accès à l'historique des commits                          │
    └─────────┴─────────────────────────────────────────────────────────────────┘

On peut commit directement depuis l'un de  ses dépôts github, en modifiant un de
ses fichiers.
Pour ce faire cliquer sur l'icône d'edit (stylo), attribuer un message au commit
(en  bas  de la  page;  par  défaut `Update  fichier`)  et  cliquer sur  `Commit
changes`.


<https://guides.github.com/features/issues/>

Mastering issues (10 min read)


Pour obtenir un permalink vers une suite de lignes de code d'un repo:

   - clic-gauche sur la 1e ligne
   - Shift-clic-gauche sur la dernière ligne
   - (optionnel) taper `S-Esc` pour désactiver temporairement Vimperator
   - taper `y`

---

    créer un repo sur github (sans readme, license, .cvsignore)

    $ git init
    $ git add .
    $ git commit -m 'first commit'
    $ git remote add origin <remote repository URL.git>
    $ git remote -v
    $ rlwrap git push -u origin master

Procédure pour envoyer un projet existant vers un nouveau repo github.

<https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/>

# Tricks

En cas de perte  du repo local, si on veut retravailler  sur une branche testing
sur laquelle on était en train de travailler au cours d'une PR:

    $ git clone url

    $ git checkout -b testing origin/testing

Source: http://stackoverflow.com/a/72156

---

    $ git rebase -i HEAD~2
    $ git push origin +master

Supprimer localement le dernier commit.
L'éditeur pop, il faut supprimer la 2e ligne.

Pousser vers github.

Source : http://stackoverflow.com/a/448929

TODO:

Vérifier que c'est une bonne méthode.
Ça a pas l'air en lisant certains commentaires.

# Théorie

Un  _pointeur_ est  une  association hash  -  nom (de  branche,  de dossier,  de
fichier...) stockée dans un fichier.

Les _branches_ sont des pointeurs.

Git utilise 3 types d'objets (blob, tree, commit), tous stockés dans:

    .git/objects/<2 premiers caractères de leur sha1>

... et ayant tous pour nom les 38 derniers caractères de leur sha1.

En effet, le  sha1 sert de clé  pour retrouver n'importe quel  objet; ainsi Git
identifie un fichier par son contenu et non pas par son nom.

    $ git cat-file -t <sha1>

Affiche le type d'objet de l'objet dont l'empreinte est `<sha1>`.

    $ git cat-file -p <sha1>

Affiche le contenu de l'objet dont l'empreinte est `<sha1>`.

Un _blob_ est un fichier compressé stockant des données qcq.

Un  _tree_ est  la représentation  du contenu  d'un dossier  à un  instant donné
(snapshot) sous la forme d'un fichier composé d'une ou plusieurs entrées.

Chaque entrée correspond à un fichier / dossier et contient 4 infos :

   - droits
   - type (blob ou tree)
   - chemin vers le fichier (ou dossier)

   - sha1 du fichier (ou du tree représentant le dossier dans le cas où le
     chemin mène à un dossier) qui sert de pointeur

Un _commit_ est un fichier contenant un ensemble d'infos, dont les 5 suivantes:

   - un message
   - une date
   - un auteur

   - le sha1 du tree sur lequel le commit pointe (l'arborescence du
     snapshot de fichiers qu'il représente)

   - le sha1 du commit parent (celui qui précède dans l'historique)

L'index (binaire `.git/index`) est un tree  spécial; il représente le contenu du
prochain snapshot.
Quand on fait un:

    $ git add <file>

... Git ajoute à l'index une entrée contenant entre autres:

   - les droits du fichier
   - son chemin d'accès (pour savoir où le recréer si besoin)
   - son sha1 (pour pouvoir le retrouver dans ses objets)

Quand on fait un `git checkout`, Git met à jour l'index pour qu'il représente le
contenu du nouveau working directory.

Quand on fait un `$  git add <dir>`, Git fait la même chose,  à ceci près que le
sha1 n'est pas celui  du dossier (un dossier ne peut pas en  avoir), mais de son
tree.

Le principe est  récursif: de la même  façon que Git peut créer  un manifeste du
working / root tree, il peut en créer un pour un sous-dossier.

Quand on crée  un commit, Git enregistre  un message associé au  hash de l'index
actuel.

Le commit  pointe sur  le manifeste qui  pointe sur les  fichiers /  dossiers du
working tree.


Git est un VCS (Version Control System) distribué.

Pas de serveur central contrairement à svn ou cvs.

Il y a un dépôt central / upstream, mais tlm peut accéder à tout l'historique du
code; le  dépôt central n'est  pas différent des  autres pairs, c'est  juste une
machine à laquelle tout le monde a un accès en lecture / écriture.


Il facilite 3  choses: backup, partage, revenir à une  ancienne version du code
en cas de régression.

Git considère les données qu'il gère comme un flux de snapshots (à ceci près que
lorsqu'un  fichier  ne  change  pas,  il  est  sauvegardé  sous  forme  de  lien
symbolique).

En ce  sens il  peut être  vu comme  un mini fs  auquel on  a ajouté  des outils
propres aux VCSs.

Un commit  est un ensemble  de modifications apportées  à un projet  (création /
suppression d'un fichier, ajout de texte, etc.) associé à un message lui donnant
du sens (quel était  le but de ces modifications) et stocké  dans un dépôt local
(.git/ ; bdd de Git).

Il peut être vu comme la création d'un snapshot.

Chaque commit  crée une  nouvelle version  du code, on  dit qu'on  versionne son
code.

L'ensemble des commits constitue l'historique du projet.

Pour Git, un fichier peut être dans 4 états :

   - untracked    le fichier est nouveau     `git add` pour que le fichier soit tracké et indexé
                                             par la même occasion

   - unstaged     il n'est pas nouveau mais modifié et non indexé (`git add` pour que ça change)

   - staged       il est indexé mais pas commited (`git commit` ")

   - unchanged    il est dans le dépôt et n'a pas changé depuis qu'il y est

Dans un projet Git, le workflow se  décompose en 3 étapes : modification d'un ou
plusieurs  fichiers  / dossiers,  indexation  (staging)  de certaines  nouvelles
versions des fichiers / dossiers, commit (ajout dans son dépôt Git local).

L'indexation  permet  de  choisir  parmi toutes  les  modifications,  lesquelles
devront être ajoutées au dépôt lors du prochain commit.

L'index  ou staging  area est  un fichier  dans le  dépôt local  qui stocke  des
informations  déterminant ce  qui  sera ajouté  à ce  dernier  lors du  prochain
commit.

L'intérêt de  l'index est  de permettre de  ne pas ajouter  au dépôt  toutes les
modifications qu'on effectue dans son dossier, uniquement celles qu'on veut.

Quand on veut  faire une expérimentation ou tester  une nouvelle fonctionnalité,
on crée une nouvelle branche (légère divergence de la base de code principale).

Par défaut, quand on crée un dépôt Git, la branche initiale se nomme master.

Si au bout  d'un moment on est  satisfait du résultat, on la  fusionnera avec la
branche principale.


Un dépôt Git est un DAG (Directed Acyclic Graph) + des post-its.
Les nœuds du DAG sont de 3 types : blob, tree et commit.

Un blob stocke un tas d'octets, le + svt un fichier ou un symlink.

Un tree est un dossier.

Il fait référence à des blobs et/ou à d'autres trees.

Un tree  contient des noms de  fichiers, des droits d'accès...  (métadonnées)
Un nœud du DAG ne peut pas exister seul, il faut qu'un autre nœud pointe sur lui
(ou que lui pointe sur un autre nœud).

On peut supprimer les nœuds isolés via:

    $ git gc --auto

... ou récupérer via:

    $ git fsck --full

---

Un commit stocke  un message et fait  référence à un tree  qui représente l'état
des fichiers à un instant donné.

Il peut avoir un ou plusieurs commits parents.

S'il en a plusieurs, le commit est un  merge ; s'il n'en a aucun, il s'agit d'un
commit initial.

Il peut y avoir  plusieurs commits initiaux dans le cas  où deux projets séparés
ont fusionné.

Les références (heads, tags) peuvent être vus comme des post-it ou des bookmarks
associés à des nœuds du DAG.

Ils  ne sont  pas stockés  dans l'historique  (.git/) ni  transférés directement
entre repos.

Contrairement  aux nœuds  du DAG  qui ne  peuvent être  supprimés ou  mutés, les
références peuvent être déplacées librement.

# Ressources

MOOCS:

- <https://www.udacity.com/course/how-to-use-git-and-github--ud775>
- <https://www.codeschool.com/courses/try-git>

INTERACTIVITÉ:

- <http://learngitbranching.js.org/?NODEMO>
- <https://try.github.io/levels/1/challenges/1>

VIDÉOS:

- <https://www.youtube.com/watch?v=zZ2hG6PMjk8>
- <https://www.youtube.com/watch?v=1ffBJ4sVUb4>
- <https://www.youtube.com/watch?v=6LhTe8Mz6jM>
- <https://www.youtube.com/watch?v=ZDR433b0HJY>
- <https://vimeo.com/17118008>

DIVERS:

- <http://rogerdudler.github.io/git-guide/>
- <http://think-like-a-git.net/>
- <http://marklodato.github.io/visual-git-guide/index-en.html>
- <https://www.atlassian.com/git/tutorials/>
- <https://github.com/Gazler/githug>
- <http://www-cs-students.stanford.edu/~blynn/gitmagic/>
- <https://medium.com/@ashk3l/a-visual-introduction-to-git-9fdca5d3b43a#.msc7rc931>
- <https://www.sbf5.com/~cduan/technical/git/git-1.shtml>
- <http://nvie.com/posts/a-successful-git-branching-model/>
- <http://tutorialzine.com/2016/06/learn-git-in-30-minutes/>
- <https://jwiegley.github.io/git-from-the-bottom-up/>
- <https://www.reviewboard.org/docs/codebase/dev/git/clean-commits/>
- <http://ndpsoftware.com/git-cheatsheet.html>
- <http://rypress.com/tutorials/git/index>
- <https://blog.jez.io/cli-code-review/>
- <https://www.conventionalcommits.org/>
- <https://raw.githubusercontent.com/git/git/master/Documentation/howto/revert-a-faulty-merge.txt>
- <https://jwiegley.github.io/git-from-the-bottom-up/>
- <https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow>
- <https://sethrobertson.github.io/GitFixUm/fixup.html>
- <https://github.com/jessfraz/branch-cleanup-action>
- <https://sethrobertson.github.io/GitBestPractices/>

- <https://jonas.github.io/tig/doc/manual.html>
- `man tig`
- `man tigrc`
- `man tigmanual`

##
# Todo
## Document
### `$ vim +'Gedit :'`

<https://twitter.com/jesseleite85/status/1179437557035220993>

> That'll open a vim instance with a fullscreen `:Gstatus` buffer.
> From there, `g?` to see available mappings,  and `:q` to quit, as you would from
> a commit buffer.

##
## Find a way to remove all the binary/big files we've committed by accident in our config repo.

To find them, clone the repo in a temporary directory, then run:

    $ git rev-list --objects --all \
    | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
    | awk '/^blob/ {print substr($0,6)}' \
    | sort --numeric-sort --key=2 \
    | cut --complement --characters=13-40 \
    | numfmt --field=2 --to=iec-i --suffix=B --padding=7 --round=nearest

The big files are at the end of the output.

You can remove one by running:

    $ git filter-branch --index-filter 'git rm --cached --ignore-unmatch my/big/file' HEAD
                                                                         ^^^^^^^^^^^
                                                                         replace with the path to the file
                                                                         you want to remove

Make sure that you don't have any non-committed change.
Source: <https://stackoverflow.com/a/46615578/9780968>

Issue: If you do that, you'll get a message (I think in the output of `$ config status`),
telling you that your local branch has diverged from origin/master.

I don't know how to fix this issue.

To undo the removal of the big file, run:

    $ git reset --hard origin/master

