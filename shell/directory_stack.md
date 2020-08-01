# What's the effect of
## `pushd some_dir`?

`some_dir` becomes the new working directory (position `0` in the stack).
The old working directory is moved further  in the stack in position `1` (before
it was in position `0`).

## `pushd`?

The directories 0 and 1 in the stack are swapped.
This implies that the cwd is reset to the directory 1.

If there's no directory 1 in the stack, it's automatically set to `$HOME`.

## `popd`?

The directory 0 is removed from the stack.
The new directory at the top of the stack becomes the cwd.

##
# What's the difference between the directory numbered 0 and the next ones?

It's dynamically  changed by the  shell whenever you  change the cwd,  to always
reflect `$PWD`.

## Is it part of the stack?

In bash yes.
In zsh no.

To check yourself execute, in zsh:

    % echo ${dirstack[@]}

In bash:

    $ echo ${DIRSTACK[@]}

##
# How to view the stack prefixing the directories with numbers?

    % dirs -v
           ^^
           number the directories in the stack when printing.

# How to replace the stack with a new one?

    % \dirs dir1 dir2 ...
      │
      └ make sure NOT to use a `dirs` alias

Note that the new cwd is not changed.
This implies that  `dir1` is added to  the stack in position `1`  (and not `0`),
`dir2` in position `2` ...

# How to remove the directory 2 from the stack?

    % popd +2

# How to clear the directory stack?

    % dirs -c

#
# In a path passed to a command, how to refer to ...
## the home directory of the user `toto`?

    ~toto

## the previous cwd?  (2)

    ~-

    $OLDPWD

Note that `-` is specific to `cd`, while `~-` works for any command.

## the directory 2 from the stack?

    % echo ~2

## the last directory from the stack?

    ~-0

## the last but one?

    ~-1

#
# Moving a directory from the stack to the top:
## How to do it for the directory 2?  the last but one?

    % pushd +2
    % pushd -1
            │
            └ a sign is necessary to prevent the argument from looking like a directory name

## What happens to the other directories when I do it?

They  advance further  in the  stack by  N;  N being  the number  you passed  as
argument to `pushd`.  If necessary, they wrap around the end bottom the stack.

    % dirs
    1 2 3 4 5~

    % pushd +2

    % dirs
    3 4 5 1 2~

## What happens if I try to execute `pushd dir`, `dir` being a directory which is already in the stack?

The cwd is  moved further in the stack  in position `1`, while `dir`  is added a
2nd time to the stack in position `0`.

Exception:
in zsh, if `'pushdignoredups'` is set, `dir` is lifted to position `0`.

Example:

    % mkdir one two three four
    % cd four
    % pushd ../three
    % pushd ../two
    % pushd ../one

    % dirs
    one~
    two~
    three~
    four~

    % pushd ../three
    % dirs
    three~
    one~
    two~
    four~

## I want `pushd +n` to just lift the directory `n`, not rotating the whole stack!  How to do it?

Copy this function in `~/.zshrc`:

    # pushd function to emulate the old zsh behaviour.
    # With this function  pushd +/-n just lifts the selected  element to the
    # top of the stack instead of just cycling the stack.

    local puid
    # if the `pushdignoredups` option is set, assign `1` to `puid`
    # we save the value now, because we're going to reset all options
    [[ -o pushdignoredups ]] && puid=1

    # reset options to their default values
    emulate -R zsh
    # restore all options when the function will return
    setopt localoptions

    #     ┌ number of arguments (more readable version of `$#`)
    #     │
    #     │                     ┌ a plus or minus sign
    #     │                     │
    #     │                     │   ┌ any number (not limited to a single digit) (man zshexpn)
    #     ├──┐                  ├──┐├─┐
    if [[ ARGC -eq 1 && "$1" == [+-]<-> ]] then
        # make sure 'pushdignoredups' is set, so that the next
        # pushd can NOT add the directory `$1` a second time in the stack,
        # and has to lift it instead
        setopt pushdignoredups
        builtin pushd ~$1
        #             ^
        #             force the expansion of `+123` into `/path/to/dir`
        #             to prevent a rotation
    else
        # 'pushdignoredups' may have been reset by `emulate -R zsh`,
        # restore it if needed
        [[ -n $puid ]] && setopt pushdignoredups
        builtin pushd "$@"
    fi

Source: <https://github.com/zsh-users/zsh/blob/master/Functions/Example/pushd>

##
# Todo
## cdr

    man zshcontrib /REMEMBERING RECENT DIRECTORIES

The function  cdr lets you  change the working  directory to a  previous working
directory from a list maintained automatically.
It is similar  in concept to the  directory stack controlled by  the pushd, popd
and dirs  builtins, but is  more configurable, and as  it stores all  entries in
files  it  is maintained  across  sessions  and  (by default)  between  terminal
emulators in the current session.
Duplicates are automatically removed, so that  the list reflects the single most
recent use of each directory.

Note that  the pushd  directory stack is  not actually modified  or used  by cdr
unless  you configure  it to  do so  as described  in the  configuration section
below.

### Use

All direct user interaction is via the cdr function.

The  argument to  cdr is  a  number N  corresponding  to the  Nth most  recently
changed-to directory.
1 is  the immediately preceding  directory; the current directory  is remembered
but is not offered as a destination.
Note that if you  have multiple windows open 1 may refer  to a directory changed
to  in another  window; you  can  avoid this  by having  per-terminal files  for
storing directory as described for the recent-dirs-file style below.

If you  set the recent-dirs-default  style described  below cdr will  behave the
same as cd if given a non-numeric argument, or more than one argument.
The recent directory list is updated just the same however you change directory.

If the argument is omitted, 1 is assumed.
This is similar to pushd's behaviour of swapping the two most recent directories
on the stack.

Completion for the argument  to cdr is available if compinit  has been run; menu
selection is recommended, using:

    zstyle ':completion:*:*:cdr:*:*' menu selection

to allow you to cycle through recent directories; the order is preserved, so the
first choice is the most recent directory before the current one.
The verbose  style is also  recommended to ensure  the directory is  shown; this
style is on by default so no action is required unless you have changed it.

###
### Options

The behaviour of cdr may be modified by the following options.

#### -l

lists the  numbers and the  corresponding directories in abbreviated  form (i.e.
with `~` substitution reapplied), one per line.
The directories here are not quoted (this  would only be an issue if a directory
name contained a newline).  This is used by the completion system.

#### -r

Sets the variable `reply` to the current set of directories.
Nothing is printed and the directory is not changed.

#### -e

Lets you edit the list of directories, one per line.
The list can be edited to any extent you like; no sanity checking is performed.
Completion is available.

No  quoting is  necessary (except  for newlines,  where I  have in  any case  no
sympathy); directories are  in unabbreviated from and contain  an absolute path,
i.e. they start with `/`. Usually the  first entry should be left as the current
directory.

#### -p 'pattern'

Prunes  any items  in the  directory  list that  match the  given extended  glob
pattern; the pattern needs to be  quoted from immediate expansion on the command
line.

The pattern is  matched against each completely expanded file  name in the list;
the full  string must  match, so  wildcards at the  end (e.g.  `*removeme*`) are
needed to remove entries with a given substring.

If output  is to a  terminal, then  the function will  print the new  list after
pruning and prompt for confirmation by the user.
This output and confirmation step can be skipped by using `-P` instead of `-p`.

###
### Configuration

Configuration  is by  means  of the  styles mechanism  that  should be  familiar
from  completion; if  not, see  the  description of  the zstyle  command (see
`man zshmodules(1)`).
The context for setting styles should be `':chpwd:*'` in case the meaning of the
context is extended in future, for example:

    zstyle ':chpwd:*' recent-dirs-max 0

sets the value of the `recent-dirs-max` style to 0.
In practice the  style name is specific  enough that a context of  `*` should be
fine.

An exception is `recent-dirs-insert`, which  is used exclusively by the completion
system  and so  has the  usual completion  system context  (`':completion:*'` if
nothing more specific is needed), though again `*` should be fine in practice.

#### recent-dirs-default

If true, and the command is expecting a recent directory index, and either there
is more than one  argument or the argument is not an  integer, then fall through
to "cd".
This allows the lazy to use only one command for directory changing.
Completion recognises  this, too;  see `recent-dirs-insert`  for how  to control
completion when this option is in use.

#### recent-dirs-file

The file where the list of directories is saved.
The default is `${ZDOTDIR:-$HOME}/.chpwd-recent-dirs`, i.e. this is in your home
directory unless you have set the variable ZDOTDIR to point somewhere else.
Directory names are saved in `$'...'` quoted  form, so each line in the file can
be supplied directly to the shell as an argument.

The value of this style may be an array.
In  this case,  the  first file  in  the list  will always  be  used for  saving
directories while any other files are left untouched.
When reading  the recent  directory list,  if there are  fewer than  the maximum
number of entries  in the first file,  the contents of later files  in the array
will be appended with duplicates removed from the list shown.
The contents of the  two files are not sorted together, i.e.  all the entries in
the first file are shown first.
The special value `+` can appear in the list to indicate the default file should
be read at that point.
This allows effects like the following:

    zstyle ':chpwd:*' recent-dirs-file \
    ~/.chpwd-recent-dirs-${TTY##*/} +

Recent directories are read from a file numbered according to the terminal.
If there  are insufficient  entries the  list is  supplemented from  the default
file.

It is possible to use `zstyle -e` to make the directory configurable at run time:

    zstyle -e ':chpwd:*' recent-dirs-file pick-recent-dirs-file
    pick-recent-dirs-file() {
      if [[ $PWD = ~/text/writing(|/*) ]]; then
        reply=(~/.chpwd-recent-dirs-writing)
      else
        reply=(+)
      fi
    }

In this  example, if the  current directory  is `~/text/writing` or  a directory
under it, then  use a special file  for saving recent directories,  else use the
default.

#### recent-dirs-insert

Used by completion.
If `recent-dirs-default`  is true, then setting  this to true causes  the actual
directory, rather than its  index, to be inserted on the  command line; this has
the same effect as using the  corresponding index, but makes the history clearer
and the line easier to edit.
With this  setting, if part of  an argument was already  typed, normal directory
completion  rather than  recent directory  completion is  done; this  is because
recent directory  completion is expected to  be done by cycling  through entries
menu fashion.

If  the value  of the  style is  always, then  only recent  directories will  be
completed; in  that case,  use the cd  command when you  want to  complete other
directories.

If the  value is fallback, recent  directories will be tried  first, then normal
directory completion is performed if  recent directory completion failed to find
a match.

Finally, if the value  is both then both sets of  completions are presented; the
usual tag mechanism can be used  to distinguish results, with recent directories
tagged as `recent-dirs`.
Note that the  recent directories inserted are abbreviated  with directory names
where appropriate.

#### recent-dirs-max

The maximum number of directories to save to the file.
If this is zero or negative there is no maximum.
The default is 20.
Note this  includes the current directory,  which isn't offered, so  the highest
number of directories you will be offered is one less than the maximum.

#### recent-dirs-prune

This style  is an array determining  what directories should (or  should not) be
added to the recent list.
Elements of the array can include:

    parent

Prune parents (more accurately, ancestors) from the recent list.
If  present, changing  directly down  by any  number of  directories causes  the
current directory to be overwritten.
For example, changing from `~pws`  to `~pws/some/other/dir` causes `~pws` not to
be left on the recent directory stack.
This  only  applies  to  direct   changes  to  descendant  directories;  earlier
directories on the list are not pruned.
For example, changing from  `~pws/yet/another` to `~pws/some/other/dir` does not
cause `~pws` to be pruned.

    pattern:pattern

Gives a zsh pattern for directories that  should not be added to the recent list
(if not already there).
This element can be repeated to add different patterns.
For example, `'pattern:/tmp(|/*)'` stops `/tmp` or its descendants from being added.
The `EXTENDED_GLOB` option is always turned on for these patterns.

#### recent-dirs-pushd

If set to true, cdr will use pushd instead of cd to change the directory, so the
directory is saved on the directory stack.
As the directory  stack is completely separate  from the list of  files saved by
the mechanism used in this file there is no obvious reason to do this.

###
### Use with dynamic directory naming

It is possible  to refer to recent directories using  the dynamic directory name
syntax by using the supplied function `zsh_directory_name_cdr` a hook:

    autoload -Uz add-zsh-hook
    add-zsh-hook -Uz zsh_directory_name zsh_directory_name_cdr

When this  is done, `~[1]`  will refer to the  most recent directory  other than
`$PWD`, and so on.  Completion after `~[...` also works.

### Details of directory handling

This  section  is for the curious or confused; most users will not need
to know this information.

Recent  directories are  saved to  a file  immediately and  hence are  preserved
across sessions.
Note currently  no file locking is  applied: the list is  updated immediately on
interactive commands  and nowhere else (unlike  history), and it is  assumed you
are only going to change directory in one window at once.
This is  not safe on  shared accounts,  but in any  case the system  has limited
utility when someone  else is changing to a different  set of directories behind
your back.

To make this a little safer,  only directory changes instituted from the command
line,  either directly  or  indirectly  through shell  function  calls (but  not
through subshells, evals, traps, completion functions and the like) are saved.
Shell functions should  use `cd -q` or  `pushd -q` to avoid side  effects if the
change to the directory is to be invisible at the command line.
See the contents of the function `chpwd_recent_dirs` for more details.

