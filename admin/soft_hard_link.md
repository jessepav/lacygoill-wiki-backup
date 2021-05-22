# What “dereference” means?

For a utility such as `cp(1)` or `ls(1)`, it means:
NOT operate on a symlink, but rather on its target.

# By default, does a utility dereference?

No, it operates on the link itself:

    $ cd /tmp
    $ sudo ln -s ~/.bashrc /tmp/link2bashrc
    $ ls -l link2bashrc
    lrwxrwxrwx 1 root root <small size> <recent date> link2bashrc → /home/user/.bashrc˜
    ^

    $ ls -lL link2bashrc
    -rw-r--r-- 1 john john <big size> <old date> link2bashrc˜
    ^

Between the 2 listings, you will notice that:

   1. `-l` prints the 'root' user/group ; `-lL` prints the 'john' user
   2. "           a small size          ; `-lL` prints a big size
   3. "           a recent date         ; `-lL` prints an old date

# What are the 3 usual options which can be passed to a utility to alter how it processes a symlink?

    ┌────────┬───────────────────────────────────────────────────────────────────┐
    │ option │                             behavior                              │
    ├────────┼───────────────────────────────────────────────────────────────────┤
    │ -P     │ not follow the link                                               │
    ├────────┼───────────────────────────────────────────────────────────────────┤
    │ -H     │ follow the link, non-recursively                                  │
    │        │ (only once)                                                       │
    ├────────┼───────────────────────────────────────────────────────────────────┤
    │ -L     │ follow the link, recursively                                      │
    │        │ (several times if the symlink's target is itself another symlink) │
    └────────┴───────────────────────────────────────────────────────────────────┘

#
# What's an inode?

A  data structure  which describes  a  filesystem object  such  as a  file or  a
directory.

Each inode  stores the  attributes and  disk block  location(s) of  the object's
data.
Filesystem object attributes may include metadata (times of last change, access,
modification), as well as owner and permission data.

You can view an inode as all the metadata of a file, except its name.

# When is an inode removed?

When no filename refers to it anymore.

#
# What's the difference between a hard link and a soft link?

A hard link is just a NEW NAME for an existing file.
A soft link is a NEW FILE, pointing to an existing file.

# What can a soft link do, that a hard link can't?  (3)

A soft link can:

   - point to a directory (a hard link can't refer to a directory)
   - cross filesystem boundaries
   - cross partitions

#
# What happens to the contents of a file, if I delete it after creating
## a hard link referring to it?

The contents of the file are still accessible:

    $ echo 'hello' >file  && \
      ln file hlink       && \
      rm file             && \
      cat hlink
      hello˜

## a soft link referring to it?

The contents of the file are lost:

    $ echo 'hello' >file
    $ ln -s file slink
    $ rm file
    $ cat slink
    cat: slink: No such file or directory˜

#
# What happens to a hard link, if I rename or move the original file?

It still works and gives you access to the contents of the original file.

Indeed, a hard link refers to an inode (via its number), not to a filename.
And changing  the name of  a file doesn't change  its inode, because  the latter
doesn't store the name.
You can have several filenames referring to the same inode.

## What about a soft link?

It's broken, and you can't use it anymore to access the contents of the original
file.

##
# How to get the inode numbers of all the files/directories in the current directory?

    $ ls -i1

##
# How to create the hard link `hlink` and the soft link `slink` pointing to `file`?

    $ ln    file hlink
    $ ln -s file hlink

## Are the inode numbers of `hlink` and `file` identical?

Yes.

## Are the inode numbers of `slink` and `file` identical?

No.

#
# My directory contains a symlink.  I've executed `ls -H`, but the listing still refers to the link, not its target!

The options `-P`, `-H`, `-L` only affect the arguments passed to `ls(1)`.

If you want `ls(1)` to dereference, you need to pass the symlink as an argument:

    $ ls -H my_symlink

# If I cd to a symlink pointing to a directory, how to prevent `pwd` from lying about the cwd?  (3)

    $ pwd -P

    # the external binary `pwd` does NOT lie,
    # contrary to the shell builtin equivalent
    $ /bin/pwd

    # bash
    $ set -o physical
    # zsh
    % setopt chaselinks

