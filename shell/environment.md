# How to inspect the environment of a process?

    $ tr '\0' '\n' < /proc/<pid>/environ

Alternatively, use our `$ environ` function:

    $ environ <pid>

##
# What's the environment of a program started by pressing a keyboard shortcut?

Any (most?) program you start from  a keyboard shortcut is temporarily the child
of xbindkeys.

So, its initial environment is inherited from the xbindkeys daemon.

## What about a program started from rofi?

Same thing.

rofi inherits its initial environment from xbindkeys.
And any program started from rofi, inherits its initial environment from the latter.

## How to remove a variable from this environment?

Make sure it's not  in your current shell (unset it  if necessary), then restart
xbindkeys.

##
# What's the purpose of this `MYMANSECT` variable to which you refer in `~/.zshenv` and in your vimrc?

In `~/.zshenv`, we have this line:

    export MYMANSECT="${MANSECT}"

And in Vim:

    let $MANSECT = $MYMANSECT

We use `$MYMANSECT` as a backup of  `$MANSECT`, to restore its value when we run
a `$ man` command.
Without this, the following would fail:

    $ man man
    :Man mount
    man.vim: command error (11) man -w mount: No manual entry for mount~
    See 'man 7 undocumented' for help when manual pages are not available.~

Indeed, for some reason,  in the environment of a `$ man`  process, the value of
`$MANSECT` is split after each colon.
As  a result,  the  value of  `$MANSECT`  is truncated  after  the first  manual
section.

    $ unset MANPAGER
    $ man man
    $ tr '\0' '\n' </proc/1234/environ
    ...~
    MANSECT=1~
    n~
    l~
    8~
    3~
    2~
    3posix~
    3pm~
    3perl~
    5~
    4~
    9~
    6~
    7~
    ...~

The output should be:

    ...~
    MANSECT=1:n:l:8:3:2:3posix:3pm:3perl:5:4:9:6:7~
    ...~

Note that `1234`, in the `$ tr` command, is the pid of the `$ man` process.
You can get it by running `$ echo $$` before running `$ man`, and noting the pid of the shell.
Then by running `$ pstree -s -p <shell pid>`, to get the pid of the `$ man` child.

## Is there a better solution?

I don't have one atm.
It could be a bug in `$ man`.

If you want to investigate more, try to run `$ man` in debug mode:

    $ man -d man
          ^^

Or use `$ strace`:

    $ strace -f -o /tmp/log man man

Or visit the issue tracker of `man-db`:
<https://savannah.nongnu.org/bugs/?group=man-db>

Or the mailing list for developers:
<https://lists.nongnu.org/mailman/listinfo/man-db-devel>

##
# In the past, we had a guard (`MY_ENVIRONMENT_HAS_BEEN_SET`) in `~/.zshenv`.  What did it look like?

At the top of `~/.zshenv`:

    if [[ -n "${MY_ENVIRONMENT_HAS_BEEN_SET}" ]]; then
      return
    fi
    export MY_ENVIRONMENT_HAS_BEEN_SET=yes

## Why did we use it?

We didn't want some variables – the  ones to which we append/prepend values – to
grow each time we start a new subshell (i.e. `$SHLVL` is incremented).

Having duplicates can sometimes lead to issues.
For example, `XDG_CONFIG_DIRS` and `XDG_DATA_DIRS` are  used by Nvim to add some
paths in its rtp.
If one of them contains a duplicate path,  and we have a Nvim filetype plugin in
it, the filetype plugin may be sourced twice which could raise errors.

---

The idea of using a guard was suggested here:
<https://www.zsh.org/mla/users/2012/msg00784.html>

##
## We don't use it anymore, because it causes too many issues.  Which ones?
### You need to unset the variable (or empty it) before restarting xbindkeys.

For example, you need to change your `xbindkeys_restart` alias like this:

    alias xbindkeys_restart='killall xbindkeys; unset MY_ENVIRONMENT_HAS_BEEN_SET; xbindkeys -f ...'
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#### Why?

Suppose you edit `~/.zshenv` to set a new environment variable, or to update the
value of an existing one.
Now,  suppose you've  also  edited  `~/.config/keyboard/xbindkeys.conf` and  you
restart xbindkeys.
Finally, you press Alt-F4 to close the  current terminal, and Super-j to start a
new one.
You expect the environment of the shell in this new terminal to contain whatever
modification you applied in `~/.zshenv`.
But that won't happen if you didn't unset or empty `MY_ENVIRONMENT_HAS_BEEN_SET`
before restarting xbindkeys.

Explanation:

Super-j is intercepted  by the xbindkeys daemon; it looks  for the command which
is bound to this key combo – here, the terminal – and runs it.
I think (*) that the terminal is then, temporarily, the child of an `$ xbindkeys`
process (which is forked from the daemon).
So, if  the latter  contains `$MY_ENVIRONMENT_HAS_BEEN_SET` in  its environment,
then the terminal inherits it, as well as the shell started by the terminal.
As a result,  when the shell reads  `~/.zshenv`, it doesn't process  most of its
code, because of our initial guard.

(*) It's the only explanation I can find.
But it's a temporary child, because we  can't see this relationship in `$ pstree -s -p $$`,
when we're inside the terminal started by pressing Super-j.
I think that the terminal is quickly reparented to the session leader
(`$ upstart` atm) after the fork of `$ xbindkeys` dies.

If you want to check this theory, here's how.
Run Vim to temporarily clear the value of `$LESS` in `~/.zshenv`.
Quit Vim, and from the current shell, restart xbindkeys.
Finally, press Alt-F4 and Super-j.
Check the value of `$LESS`.
It should  be empty, but  it will  still have its  old value, before  you edited
`~/.zshenv`.

###
### You need to remove the variable from the tmux global environment.

If you edit `~/.zshenv`, for the change  to take effect in all the future shells
opened by tmux,  you need to remove `MY_ENVIRONMENT_HAS_BEEN_SET`  from the tmux
global environment, by writing in `~/.tmux.conf`:

    setenv -gu MY_ENVIRONMENT_HAS_BEEN_SET

Otherwise,  you  would need  to  restart  the  tmux  server, whenever  you  edit
`~/.zshenv`.
Indeed, a new shell is initialized  with the tmux global environment *before* it
can read its config files (`~/.zshrc`, `~/.zshenv`, ...).

### You need to remove the variable from Vim's environment.

When we start Vim's builtin terminal, by default `$TERM` is set to `xterm`.
We need to reset this value to  `xterm-256color`, so that the programs know that
our terminal  supports 256  colors, and  that they don't  limit themselves  to a
restricted palette of 8/16 colors.
We do this in `~/.zshenv`:

    if [[ -n "${VIM_TERMINAL}" ]]; then
      export TERM=xterm-256color
    fi

But, if `MY_ENVIRONMENT_HAS_BEEN_SET` is set, this block won't be processed.
So, you need to allow all the `~/.zshenv` to be sourced by adding this line in your vimrc:

    unlet $MY_ENVIRONMENT_HAS_BEEN_SET

##
## What do you use instead now?

We rely on  an anonymous function at  the end of `~/.zshenv`  to remove possible
duplicates in some variables.

At the moment, it looks like this:

    () {
      emulate -L zsh
      local -A vars=( \
        [PATH]="${PATH}" \
        [INFOPATH]="${INFOPATH}" \
        [MANPATH]="${MANPATH}" \
        [XDG_CONFIG_DIRS]="${XDG_CONFIG_DIRS}" \
        [XDG_DATA_DIRS]="${XDG_DATA_DIRS}" \
        )
      local key
      for key in "${(k)vars[@]}"; do
        if [[ -n "${vars[$key]}" ]]; then
          local copy=
          local rebuild=
          copy="${vars[$key]}":
          while [[ -n "${copy}" ]]; do
            entry="${copy%%:*}"
            case "${rebuild}": in
              *:"${entry}":*) ;;
              *) rebuild="${rebuild}:${entry}" ;;
            esac
            copy="${copy#*:}"
          done
          eval "$key=\"${rebuild#:}\""
        fi
      done
    }

### How does this compare to the guard, performance-wise?

It's not as good, but good enough.
In particular, make sure to guard any `$ eval` command.
They seem to have a big impact on performance.

    # ✘
    eval "$(lesspipe)"

    # ✔
    if [[ -z "${LESSOPEN}" ]]; then
      eval "$(lesspipe)"
    fi

You can measure how much time your `~/.zshenv` takes to be sourced by running:

    $ time zsh -c 'repeat 1000 source ~/.zshenv'
    zsh -c 'repeat 1000 source ~/.zshenv'  1,80s user 0,30s system 99% cpu 2,099 total~
                                                                           ^^^^^

Read the `total` field, and divide by 1000.
Right now, it takes around 2ms, which is good enough for me.

##
# Issues
## I've changed the value of a variable in `~/.zshenv`.  It's ignored when I start a new shell!

You're  probably inside  a tmux  session, and  the setting  of your  variable is
probably guarded:

    if [[ -z "${LESSOPEN}" ]]; then
      eval "$(lesspipe)"
    fi

If that's the case,  then your change is ignored because  of the non-empty value
of your variable in the tmux global environment.
Whenever  a shell  is started,  your variable  is set  with this  value *before*
`~/.zshenv` is read, which prevents your change from being applied.

Solution:

Restart the tmux server, or change the value of your variable in the tmux global
environment:

    $ tmux setenv -g VAR new_value

