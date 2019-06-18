# Concepts
## What are the global environment of the tmux server, and a session environment?

They are two  sets of environment variables  which will be merged  and passed to
each process  started by the  tmux server (which is  typically a shell,  but not
necessarily).

The global environment applies to all sessions, while a session environment only
applies to a given tmux session.

### How are they initialized?

For the global environment, tmux copies  the environment of the shell from where
it's started.

---

For the  session environment,  tmux copies  the variables  listed in  the option
`'update-environment'`, with  the values they  had in  the shell from  which the
tmux client was started.

### How to read what they currently contain?

For the global environment:

    $ tmux showenv -g

For the session environment:

    $ tmux showenv

#### In my current session environment, some variables are prefixed with a minus sign.  What does it mean?

It means that tmux will remove the  variables from the merged environment of any
process it will start in this session.

##### When does tmux prefix a variable with such a sign?

When it's  listed in  `'update-environment'`, but  is absent  in the  shell from
which the tmux client was started.

##
# Syntax
## Which variables does tmux expand?  (2)

The ones in the environment of the tmux server process, as well as `~` and `~user`.

See `$ man tmux /PARSING SYNTAX`.

---

Note  that this  doesn't include  the variables  which are  only in  tmux global
environment, and not in the environment of the process.

Write this in tmux.conf:

    setenv -g myvar hello
    set -g @foo "$myvar"

Reload it, and run:

    :show -gv @foo
    ''~

The output  is empty because `$myvar`  was not in the  tmux process environment,
and so was not expanded.

### In a key binding or hook, does it occur at parse time or at execution time?

At parse time.

Any variable is  expanded at parse time, regardless of  the context (option, key
binding, hook, ...).

Consider this hook:

    set-hook -ga pane-focus-out "display '$EDITOR'"

If  `$EDITOR`  was  expanded  at  execution time,  tmux  would  print  `$EDITOR`
literally, because of the single quotes.
But in practice, it prints `vim`.
This proves that `$EDITOR` has been expanded earlier, at parse time.

---

Thanks  to this,  if  you  used [vim-tmux-navigator][1],  you  could remove  the
`is_vim` variable from tmux global environment:

    $ tmux setenv -gu is_vim

The key bindings would still work.

##
# Adding a variable
## How to add an environment variable into the global environment?  (2)

Use `setenv -g`:

    $ tmux setenv -g VAR value

Example:

    $ tmux setenv -g REPORTTIME 123

---

Or use `var=val` in a file sourced by tmux:

     $ tmux -Lx -f =(cat <<'EOF'
     var=hello
     EOF
     )
     $ tmux showenv -g | grep hello
     var=hello~

     $ tmux source =(echo 'var=world')
     $ tmux showenv -g | grep world
     var=world~

## What happens if I write `var=val`
### in my tmux.conf?

The variable `var` is  added to the environment of the  tmux server process, and
to tmux global environment.

### in `/tmp/file` then run `$ tmux source /tmp/file`?

The variable `var` is only added to tmux global environment.

##
# Unsetting a variable
## How to unset a variable from the merged environment passed by tmux to
### all future shells?

If the variable is only in the session environment:

    $ tmux setenv -{u|r} VAR

Only in the global environment:

    $ tmux setenv -g{u|r} VAR

In both the global and session environments:

    $ tmux setenv -{u|r} VAR \; setenv -g{u|r} VAR

### all future shells of the current session (and only the current session)?

    $ tmux setenv -r VAR

It doesn't matter whether the variable was initially in the session environment,
the global environment, or both; it will always be removed.

After running  the command, tmux adds  the variable to the  session environment,
prefixed with a minus sign:

    $ tmux showenv | grep VAR
    -VAR~
    ^

This removes the old value that the variable had in the session environment, and
indicates to tmux that  when it starts a process, it  should remove the variable
from the merge between the session and global environments.

---

Alternatively, if  the variable is  in the session  environment (and not  in the
global one):

    $ tmux setenv -u VAR

###
## What can `-r` do that `-u` can't?

`-r` can remove a variable from the  environment of all processes started in the
current session, even if it's in the tmux global environment.

    $ tmux setenv -r WINDOWID
    $ tmux splitw
    $ echo $WINDOWID
    ''~

`-u` can't do that.

    $ tmux setenv -u WINDOWID
    $ tmux splitw
    $ echo $WINDOWID
    1234~

If a variable  is in the tmux  global environment, `-u` will remove  it from the
session environment,  but not from  the global one;  as a result,  the processes
will still be initialized with the variable.
`-gu` would remove  the variable from the global environment,  but remember that
we want to remove it only from the processes started in *the current session*.

## `WINDOWID` is in the session and global environment.  What happens if I run `$ tmux setenv -gr WINDOWID`?

Nothing.

This is because:

   - `WINDOWID` is still in the session environment of any tmux session
   - a session environment has priority over the global one

##
# Updating a variable
## automatically
### When does tmux automatically update the value of `KRB5CCNAME` in the environment of a session?  (3)

Whenever you:

   - create a new session

   - switch to an existing session

   - attach a client to a session

---

It doesn't matter how you create a new session, its environment is always updated:

    # from outside a tmux session, into a new tmux server
    $ export KRB5CCNAME=foo
    $ tmux -Lx
    $ tmux showenv | grep KRB5CCNAME
    KRB5CCNAME=foo~

    # from outside a tmux session, into a running tmux server
    $ export KRB5CCNAME=foo
    $ tmux new-session -s test
    $ tmux showenv | grep KRB5CCNAME
    KRB5CCNAME=foo~

    # from inside a tmux session
    $ export KRB5CCNAME=foo
    $ S=$(tmux new-session -d -P)
    $ tmux showenv -t $S | grep KRB5CCNAME
    KRB5CCNAME=foo~

---

In  the   manpage,  the   documentation  about   `'update-environment'`  doesn't
explicitly mention switching to a session  as a case where a session environment
is automatically updated – unless you consider switching to another session as a
special  (?)  case of  attaching  to  a  session –  but  it  is implied  in  the
documentation about `switch-client`:

> If -E is used, update-environment option will not be applied.

---

After attaching a client  to a session, the other sessions  are updated when you
switch to them; not before.

You can check this by running `$ tmux showenv -t other_session | grep KRB5CCNAME`.
The output will still contain the old value of the variable.
And after you switch to `other_session`, `$ tmux showenv | grep KRB5CCNAME` will
finally contain the updated value.

#### Which value is used?

The value of `KRB5CCNAME` in the environment of the shell from which
`new-session`, `switch-client`, `attach-session` has been run.

#### How to prevent this automatic update?

Pass the `-E` flag to `new-session`, `switch-client`, `attach-session`.

###
### How to control which variable is updated like `KRB5CCNAME`?

Add the name of the variable you want to be updated to the array option `'update-environment'`:

    $ tmux set -ga update-environment VAR

#### Why `-g`?

Don't be confused by the semantics of `-g` here.
It doesn't mean that you set the global environment of tmux.
`'update-environment'` only sets the environment local to a session.
`-g` simply means that you set it for *all* sessions; and not just the current one.

#### Why `-a`?

It's useful to keep the variables which are included in the default value of the
option:

    DISPLAY
    KRB5CCNAME
    SSH_AGENT_PID
    SSH_ASKPASS
    SSH_AUTH_SOCK
    SSH_CONNECTION
    WINDOWID
    XAUTHORITY

#### What happens if the variable doesn't exist in the environment of the shell from which I start the tmux client?

It's given a special value: `-VAR`.
It means that  it's set to be  removed from the session environment  (as if `-r`
was given to the `set-environment` command).

##
## manually
### How to reset the value of a variable in the global environment without restarting the tmux server?

    $ tmux setenv -g VAR new_value

###
### Why can't `setenv` modify the environment of the current shell?

`setenv` can only modify the environment of a future process;
not the environment of a process which has already started.

### The environment of my session has been automatically updated.
#### How to reflect this update in the environment of the *current* shell?

Use `$ eval` and pass `-s` to `showenv`:

    $ eval $(tmux showenv -s VAR)
                           │
                           └ the output is formatted as a set of Bourne shell commands

See: <https://unix.stackexchange.com/a/509249/289772>

###
### Why can't I use `setenv` to change the value of a variable set in `~/.zshenv`?

Because `~/.zshenv` is sourced later.
`setenv` modifies the initial environment of any process started by tmux, but it
has no effect after that.
So, if tmux starts  a shell, and the latter sources  `~/.zshenv`, then this file
has the last word on the values of the environment variables it sets.

##
# Miscellaneous
## What does the value of `$TMUX` mean (e.g. `/tmp/tmux-1000/default,31058,2`)?

    /tmp/tmux-1000/default,31058,2
    ├────────────────────┘ ├───┘ │
    │                      │     └ the server handles 3 sessions (2+1)
    │                      └ pid of the tmux server
    └ path to the server socket

#
## What is the output of the next snippet?

    $ tmux setenv foo bar
    :display "$foo"

↣ Nothing. ↢

### Why?

When  expanding  an  environment  variable,   tmux  only  considers  the  global
environment, not the session one.

From `$ man tmux /PARSING SYNTAX`:

> -   Environment variables preceded by $ are replaced with their
>     value from the **global environment** (see the GLOBAL AND SESSION
>     ENVIRONMENT section).

##
## I've run `:set @foo "a$EDITORb"`.  What's the output of `:show -v @foo`?

    a

There's nothing  after `a`, because tmux  tried to expand `EDITORb`;  it doesn't
exist, and so was replaced with an empty string.

### How to get `avimb`?

                v      v
    :set @foo a${EDITOR}b
    :show -v @foo

###
## Does a non-interactive shell started by `run-shell` or `if-shell` inherit
### the environment of the tmux server process?

Yes for `run-shell`:

    $ tmux run 'pstree -s -p $$ >/tmp/.out'
    $ cat /tmp/.out
    systemd(1)---lightdm(1001)---lightdm(1086)---upstart(1095)---tmux: server(3253)---sh(18687)---pstree(18688)~

And yes for `if-shell`:

    $ tmux source =(cat <<'EOF'
    if "pstree -s -p $$ >/tmp/.out" ""
    EOF
    ) ; cat /tmp/.out
    systemd(1)---lightdm(954)---lightdm(1098)---upstart(1110)---tmux: server(3750)---sh(27584)---pstree(27585)~

### the global and session environment?

Yes for `run-shell`:

    $ tmux setenv var_session 123 \; setenv -g var_global 456
    $ tmux run 'env | grep "var_\(session\|global\)"'
    var_session=123~
    var_global=456~

And yes for `if-shell`:

    $ tmux setenv var_session 123 \; setenv -g var_global 456
    $ tmux source =(cat <<'EOF'
    if "env | grep 'var_\\(session\\|global\\)' >/tmp/.out" ""
    EOF
    ) ; cat /tmp/.out
    var_session=123~
    var_global=456~

