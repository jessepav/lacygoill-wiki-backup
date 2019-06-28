# How to make zsh my default shell?

        # add zsh to the list of valid login shells
        $ command -v zsh | sudo tee -a /etc/shells

        # set zsh as my login shell
        $ sudo chsh -s "$(command -v zsh)" "${USER}"

        # logout/login (to restart graphical session)
        $ loginctl terminate-session "$(loginctl session-status | awk 'NR==1{print $1}')"

##
# How to list all the files sourced by zsh on startup?

    % script -c 'zsh -o SOURCE_TRACE' log
    % exit
    % vim log
    :v/^+/d_

##
# What does `[nyae]` mean when I make a typo and the shell suggests me a correction?

        ┌───┬───────┬───────────────────────────────────────────────────────────┐
        │ n │ no    │ refuse the correction, execute the command as it is       │
        ├───┼───────┼───────────────────────────────────────────────────────────┤
        │ y │ yes   │ accept the correction                                     │
        ├───┼───────┼───────────────────────────────────────────────────────────┤
        │ a │ abort │ cancel the execution of the command                       │
        ├───┼───────┼───────────────────────────────────────────────────────────┤
        │ e │ edit  │ cancel the execution of the command,                      │
        │   │       │ and populate a new command-line with the current command, │
        │   │       │ to let me edit it                                         │
        └───┴───────┴───────────────────────────────────────────────────────────┘

`e` is particularly useful  when you make a typo, and  the spelling mechanism is
unable to fix it.

##
# How to list the currently loaded modules?

        # human-readable
        % zmodload

        # machine-readable
        % zmodload -L

# How to load the `complist` module?  How to unload it?

        % zmodload    zsh/complist
        % zmodload -u zsh/complist

# Where does zsh looks for the `complist` module?

zsh adds the standard suffix `.so` to the name you specified to `zmodload`.
Then, it looks in all the paths present in `$module_path`.

##
# How can a function know the name of the widget from which it was invoked?

It can inspect the `$WIDGET` variable.

##
# Alias
## How to print a machine-readable version of the regular aliases?  Global aliases?  Suffix aliases

        % aliases -L -r
        % aliases -L -g
        % aliases -L -s
                   │
                   └ machine-readable

## How to remove the suffix aliases?

        % unalias -s -m '*'
                      │
                      └ the arguments are taken as patterns,
                        and the aliases matching these patterns are targeted by the command

## How to save then restore the suffix aliases?

          # save
          aliases_save="$(alias -L -s)"

          # restore
          eval "${aliases_save}"

## How to suppress the expansion of aliases during the execution of a function?  (2)

Unset the `aliases` option:

        emulate -L zsh
        setopt no_aliases

---

Autoload the function, and load it by passing the `-U` option to `autoload`.

##
# Issues
## zsh takes too much time to start!

You may have installed it from the official repositories.
In this case, `zsh-common` may have been installed as a dependency.
The latter installs the file:

        /etc/zsh/zshrc

Which contains a `compinit` command.
If you  already executed this  command in your  `~/.zshrc`, it will  probably be
executed twice.
In any case, it  increases zsh startup time by approximately  `.5s` (but only if
you  tweak `fpath`  to include  a custom  directory where  you put  a completion
function file).

Solution:

Purge `zsh-common` (and `zsh`), then re-install zsh by compiling from source.

---

Alternatively, you could  try to unset the options `RCS`  and/or `GLOBAL_RCS` in
`~/.zshrc`.
It would prevent zsh from sourcing some remaining startup files.
However, even though  `~/.zshrc` is sourced early,  it may still be  too late to
prevent `/etc/zsh/zshrc`...

Also,  this may  be undesirable,  because you  may want  to source  some of  the
remaining startup files like:

        /etc/zsh_command_not_found

## Some commands work fine in bash, but fail in zsh:  “zsh: no matches found: <some pattern>”!

You probably have passed an argument to your command which contains wildcards:

        ?
        *
        [...]

MWE:

        $ shopt -u nofailglob; echo ?
        ?~

        $ shopt -s nofailglob; echo ?
        bash: no match: ?~
        (because there's no file/directory in the cwd whose name contains only 1 character)~

        % unsetopt nomatch; echo ?
        ?~

        % setopt nomatch; echo ?
        zsh: no matches found: ?~

Both shells try to expand a glob pattern.
The difference is how they react to a glob pattern which they fail to expand.
This behavior is controlled by 'failglob' in bash, and by 'nomatch' in zsh.
But these options  are not set in the  same way, which is why  the shells behave
differently.

When 'failglob' is enabled in bash (it  is NOT by default), or when 'nomatch' is
enabled in zsh  (it IS by default),  then if the filename  generation fails, the
shell reports an error, and the command is not executed.

OTOH,  if 'failglob'  is  disabled,  or 'nomatch'  is  disabled,  then a  failed
filename generation  doesn't make the shell  report any error, which  allows the
command to be executed.

Solution: Quote your arguments properly.

For more info, see:

          https://superuser.com/a/669674/913143
          https://unix.stackexchange.com/a/271402/289772

##
# Todo

To read:

> In zsh, how can I dump all configuration?
<https://unix.stackexchange.com/a/117344/289772>
