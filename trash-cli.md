# Commands

## How to install `trash-cli`?

        sudo aptitude install trash-cli

## How to put some files in the trash can?

        $ trash-put     file1 file2 ...
        $ gvfs-trash -f file1 file2 ...
                      │
                      └ ignore non-existent and non-deletable files

You can use glob qualifiers too:

        $ trash-put     file*
        $ gvfs-trash -f file*

Do NOT quote the pattern.
The commands don't know how to expand the glob qualifier.
The shell must be able to do it.

## How to list the contents of the trash can?

To get a maximum of information (date of deletion, full paths, ...), execute:

      $ trash-list


To only read the filenames, execute:

      $ gvfs-ls -h trash://
                 │
                 └ --hidden = show hidden files

This command is provided by the  package `gvfs-bin` installed by default in some
DEs.

The `gvfs` acronym probably means Gnome Virtual FileSystem.

The main difference between:

        • `gvfs-ls`   vs  `ls`,
        • `gvfs-cat`  vs  `cat`,
        • `gvfs-cp`   vs  `cp`
        ...

Is that `gvfs-xyz` can also work on remote locations.

## How to look for a file in the trash can?

      $ trash-list | grep filename

## How to empty/restore the contents of the trash can?

        $ trash-empty

        $ trash-restore


Before restoring anything, `trash-restore` will display a number-indexed menu to
let you choose which file/directory you want to restore.


It seems that the menu will  only let you choose files/directories deleted below
the current directory.

And only if there aren't several  partitions mounted somewhere below the current
directory. In which case  I suppose there's an ambiguity on  the identity of the
trash can  you want to restore  something from, because each  partition probably
has its own independent trash can.


`trash-restore` is a custom alias.
The original  command is `restore-trash`,  which imo is  a poor name  because it
doesn't use the same prefix as the other commands.

## How to remove all files with the name 'foo' in the trash can?   All files ending with '.o'?

        $ trash-rm foo

        $ trash-rm '*.c'

Note that you must  NOT supply a full path to `trash-rm`,  only a filename (last
component in the path).

Contrary to `trash-put`, if you supply  a pattern containing a glob qualifier to
`trash-rm`, you MUST quote it. The shell must NOT expand the glob qualifier.

## How to remove the files in the trash can, only if they've been there more than a week?

        $ trash-empty 7

# Ranger integration

## Which key bindings can I use in `ranger` to handle the trash can?

        ┌──────────┬────────────────────────────────────────────────────────┐
        │   key    │                        meaning                         │
        ├──────────┼────────────────────────────────────────────────────────┤
        │ te       │ empty trash can                                        │
        ├──────────┼────────────────────────────────────────────────────────┤
        │ tl       │ list contents of trash can
        ├──────────┼────────────────────────────────────────────────────────┤
        │ tr       │ restore trash can                                      │
        ├──────────┼────────────────────────────────────────────────────────┤
        │ tp       │ put file in trash can                                  │
        │          │                                                        │
        │ <DELETE> │ same, but ignore errors due to files which don't exist │
        │          │ or can't be deleted                                    │
        └──────────┴────────────────────────────────────────────────────────┘

## How can I change them?

Edit this file:

        ~/.config/ranger/rc.conf

Also, for inspiration, have a look at:

        https://github.com/gotbletu/dotfiles/blob/5a0c745845c1ecb21d3355d93f5d7ef7c6e94dc2/ranger/.config/ranger/rc.conf

# Miscellaneous

## Where's the trash can of the main partition (the one including the /home directory)?

        $HOME/.local/share/Trash/

# Issues

## How to fix “OSError: [Errno 13] Permission denied:  ...” message when executing `trash-empty`?

The trash can contains one or several files which you don't own, or which are in
a directory you don't have write access to.

Raise your privileges:

        $ sudo trash-empty

Or `cd` into  the trash can, search  for the offending file(s),  and remove them
manually (`sudo rm ...`).

## How to eliminate “TrashDir skipped because parent not sticky: ...” message when executing `trash-list`?

The full message looks like this:

        TrashDir skipped because parent not sticky: /media/user/mount_point/.Trash/1000

To eliminate this message, add the sticky bit to the PARENT directory, which here is:

        /media/user/mount_point/.Trash/

You can do so by executing this command:

        $ sudo chmod +t /media/user/mount_point/.Trash/

When the  sticky bit (or  restricted deletion flag) is  given to a  directory, a
user can delete a file/subdirectory inside, only if they own the latter.

For more info, read:

        https://github.com/andreafrancia/trash-cli/issues/59#issuecomment-219863563

