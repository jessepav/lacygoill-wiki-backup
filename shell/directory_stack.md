# What's the effect of `pushd some_dir`?

1. The current working directory is moved further in the stack in position `1`
2. `some_dir` becomes the working directory (position `0` in the stack).

# What's the effect of `pushd`?

1. The cwd is pushed onto the stack (in position `1`).

2. If the directory numbered 1 (in the output of `% dirs -v`) exists, it becomes the cwd.
   IOW, the directories 0 and 1 are swapped.
   Otherwise, `$HOME` becomes the cwd.

# What's the effect of `popd`?

1. The directory at the top of the stack is removed.
2. The new directory at the top of the stack becomes the cwd.

# What's the difference between the directory numbered 0 and the next ones?

It's dynamically  changed by the  shell whenever you  change the cwd,  to always
reflect `$PWD`.

# Is the directory numbered 0 (in the output of `% dirs -v`) part of the stack?

In bash yes.
In zsh no.

To check yourself execute, in zsh:

    % echo ${dirstack[@]}
             ^^^^^^^^
             capitalize the name in bash

##
# How to push the cwd onto the stack without the cwd being altered?

        % pushd .

# How to replace the directory stack with a new one?

        % \dirs dir1 dir2 ...
          │
          └ make sure NOT to use a `dirs` alias

Note that the new cwd is not changed.
This implies that  `dir1` is added to  the stack in position `1`  (and not `0`),
`dir2` in position `2` ...

# How to clear the directory stack?

        % dirs -c

#
# How to remove the 3rd directory in the stack?

        % popd +2

# What's the new cwd afterwards?

It's not changed.

#
# In a path passed to a command, how to refer to ...
## the home directory of the user `toto`?

        % echo ~toto

## the previous directory?  (2)

               ┌ `-` is specific to `cd`, while `~-` works for any command
               ├┐
        % echo ~-
        % echo $OLDPWD

## the 3rd directory on the directory stack?

        % echo ~2

## the last directory on the directory stack?  the last but one?

        % echo ~-0
        % echo ~-1

#
# Moving a directory in the stack to the top:
## How to do it for the 3rd directory?  the last but one?

        % pushd +2
        % pushd -1
                │
                └ a sign is necessary
                  to prevent the the argument from looking like a directory name

## What happens to the other directories when I do it?

They rotate (visualize a circle with numbers on it):

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

## I want `pushd +n`  to  just lift the directory `n`, not rotating the whole stack!  How to do it?

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

              ┌ number of arguments (more readable version of `$#`)
              │
              │                     ┌ a plus or minus sign
              │                     │
              │                     │   ┌ any number (not limited to a single digit) (man zshexpn)
              ├──┐                  ├──┐├─┐
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

Source:
        https://github.com/zsh-users/zsh/blob/master/Functions/Example/pushd

