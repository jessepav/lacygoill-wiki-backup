# Why should I avoid including a shell variable inside the format passed to `printf`?

The variable will be evaluated by  the shell *before* `printf` parses the format
to replace the specifiers such as `%s`.
So, if the  value contains sth like `%s`,  `printf` will parse it  as a format
specifier, which may be unexpected; you probably want it to be printed verbatim.

    $ coverage='96%'

    ✘
    $ printf "Unit test coverage: $coverage\n"
    printf: %\n: invalid directive~
    Unit test coverage: 96%~

    ✔
    $ printf "Unit test coverage: %s\n" "$coverage"
    Unit test coverage: 96%~

For more info, see:
<https://github.com/koalaman/shellcheck/wiki/SC2059>

# When does `printf` translate an escape sequence such as `\007`?

When it's written inside the format:

    $ printf 'a\007b'
    ab~

    $ var='\007' ; printf "a${var}b"
    ab~

or in an argument bound to the format specifier `%b`:

    $ printf '%b' 'a\007b'
    ab~

---

In all other cases, `printf` does *not* translate an escape sequence:

    $ printf '%s' 'a\007b'
    a\007b~

##
# How to execute all the scripts in a directory?

    $ run-parts /path/to/dir

# How to do the same, but also print the name of the scripts which produce an output?

    $ run-parts --report /path/to/dir
                ^------^

The script's name is  printed to whichever of stdout or  stderr the script first
produces output on.

# My script `sh.sh` is not executed!

    $ run-parts --regex '^[-._0-9a-zA-Z]+$' /path/to/dir
                            ^

By default, `run-parts` doesn't execute scripts whose name contains a dot.
So you have to use `--regex` to manually include it inside the set of valid characters.

##
# How to get the number of positional parameters passed to the current script/function?

    echo $#

# How to get all the positional parameters passed to the current script/function?  (2)

    echo $*
    "$1 $2 ..."~

    echo $@
    "$1" "$2" ...~

##
# Which status code should my function/script use when the user makes a mistake trying to invoke it?

    ┌────┬───────────────────────────────────────────────────┐
    │ 64 │ the command is wrong (probably its syntax)        │
    ├────┼───────────────────────────────────────────────────┤
    │ 65 │ the input data is wrong (argument of the command) │
    ├────┼───────────────────────────────────────────────────┤
    │ 77 │ not enough rights                                 │
    └────┴───────────────────────────────────────────────────┘

These are just conventions.

For more info, see:
<https://www.freebsd.org/cgi/man.cgi?query=sysexits&apropos=0&sektion=0&manpath=FreeBSD+4.3-RELEASE&format=html>

# With which statement?

In a function:

    return XYZ

In a script:

    exit XYZ

##
# How to iterate over the directories in `$PATH`?

In bash:

    for dir in $(tr ':' ' ' <<<"${PATH}"); do

Note that this line is unreliable if a directory name contains a space.

A more reliable way, in zsh, would be:

    for dir in "${path[@]}"; do
      echo "${dir}"
    done

##
# How to write a script, some commands of which require root privileges?

There are 3 issues to solve.

   1. Do you want to just type the name of the script, not its full path?

If so, you'll need to move it in a directory in the `$PATH` of the root user.

---

   2. Do you  want to  elevate the privileges  of the whole  script, or just the
      commands which need it?

For the whole script, you'll need to start the latter with sudo.
For the commands, you'll need to prefix them with sudo inside the script.

---

   3. Do you want to avoid giving the password?

If so, you'll need to add your script/commands in `/etc/sudoers`:

     % sudo visudo
 OR
     % sudo visudo -f custom_file
                      │
                      └ some file in `/etc/sudoers.d/`

Warning:

If your  script is in your  home folder, and  you add it to  `/etc/sudoers`, you
create a serious security breach.
Someone accessing your account could modify your script, and make it execute any
command with root privileges without having to provide a password.

##
# Can a variable assignment pollute the current shell, if it's done from a function?  From a script?

It can from a function, but not from a script.

A script is probably  executed in a subshell, thus, the  pollution of the latter
should not affect the current shell (which is its parent).
In fact, you can't  even use `local` directly in a  script (outside a function);
it's an error.

# How to make a variable assignment local to a function?

Use the shell built-in `local` command:

    func() {
      # ✘
      VAR=...
    }

    func() {
      # ✔
      local VAR=...
    }

However, if the rhs of the assignment is a command substitution, you need
to separate the assignment from the `local` statement:

    func() {
      # ✘
      local VAR="$(...)"
    }

    func() {
      # ✔
      local VAR
      VAR="$(...)"
    }

Indeed, if  an error  occurs while  evaluating the output  of the  command, it
won't be propagated to `local`.
So, if you later inspect `$?` to check whether an error occurred, you'll miss it.

##
# From which functions can an alias be expanded?

In the ones defined in a file sourced by an interactive shell (e.g. `~/.zshrc`).
If the function is defined in a script, there's no alias expansion.
From `man bash` (`ALIASES`):

>  Aliases  are not  expanded  when the  shell is  not  interactive, unless  the
>  expand_aliases shell option is set using  shopt (see the description of shopt
>  under SHELL BUILTIN COMMANDS below).

MWE:

    % cat <<EOF >> ~/.zshrc
    alias what_am_i='echo "I am an alias"'
    func() {
        what_am_i
    }
    EOF

    % source ~/.zshrc
    % func
    I am an alias~

Note that the alias must be defined BEFORE the function.

# How to suppress alias expansion in a function?

Use the `builtin` command:

    % builtin alias_name
      ^-----^

##
# Options
## Are all bash options boolean?  What about zsh?  What about readline variables?

They are all boolean, except readline variables.
The latters may be or not.

## How do I test whether the boolean option 'foo' is set in zsh?

        $ [[ -o foo ]]; echo $?

If the exit status is `0`, the option is set.
If the exit status is `1`, the option is unset.
If the exit status is `3`, the option doesn't exist.

## In bash?

It depends on whether the option is set with `set` or `shopt`:

        $ [[ -o foo ]]; echo $?
        $ shopt foo; echo $?

If the exit status is `0`, the option is set.
If the exit status is `1`, the option is unset or doesn't exist.

## How do I test whether the boolean readline variable 'foo' is set?

        $ bind -v | grep 'foo on'; echo $?

##
# Test
## How to test whether
### a parameter is set?

Use this parameter expansion:

    ${parameter:-word}

Example:

    $ if [[ "${TERM:-none}" == 'none' ]]; then echo 'the parameter is NOT set'; else echo 'the parameter is set'; fi
    the parameter is set~
    $ if [[ "${foo:-none}" == 'none' ]]; then echo 'the parameter is NOT set'; else echo 'the parameter is set'; fi
    the parameter is NOT set~

    $ case ${TERM:-none} in none) echo 'the parameter is NOT set';; *) echo 'the parameter is set';; esac
    the parameter is set~
    $ case ${foo:-none} in none) echo 'the parameter is NOT set';; *) echo 'the parameter is set';; esac
    the parameter is NOT set~

### a directory is empty?

    if [[ -z "$(ls -A -- "${dir}")" ]]; then
      ...
    fi

For more info, see:

- <http://mywiki.wooledge.org/BashFAQ/004>
- <https://unix.stackexchange.com/a/204572/289772>
- <https://unix.stackexchange.com/a/202352/289772>

###
### a command exists on my system?

        if command -v "${cmd}" >/dev/null 2>&1; then
          ...
        fi

#### When is it not reliable?

In zsh, because of the possible interference of a suffix alias.

MWE:

    $ alias -s md=vim
    $ if command -v md.md >/dev/null 2>&1; then echo 'md.md is a valid command!'; fi
    md.md is a valid command!~

#### Which alternative may be more reliable?

    if [[ -x "${cmd}" && ! -d "${cmd}" ]]; then
      ...
    fi

---

FIXME:
Why doesn't `setopt no_aliases` work?

    % alias -s md=vim && setopt no_aliases && md.md
    zsh: command not found: md.md (✔ expected)~

    % alias -s md=vim && setopt no_aliases && command -v md.md
    vim (✘ it shouldn't output anything)~

##
### I'm in a console?

        [[ -z "${DISPLAY}" ]]
        [[ "$(tty)" == *pts* ]]
        [[ "${TERM}" == linux ]]

### a running script has root privileges?

    check_we_are_root() {
      # 0 is the EUID of the root user.
      if [[ "${EUID}" -ne 0 ]]; then
        cat <<EOF >&2
    Please run as root:
        sudo "$0"
    EOF
        # 77 = not sufficient permission
        exit 77
      fi
    }

    check_we_are_root

---

If you have a  `main` function and you redirect its output in  a log file, don't
call `check_we_are_root` from it; call it from outside, before:

    check_we_are_root
    main "$1" 2>&1 | tee -a "${LOGFILE}"

Rationale:

Suppose the script process has no root privileges, but the logfile is owned by root.
If you write this:

    main() {
      check_we_are_root
      ...
    }
    main "$1" 2>&1 | tee -a "${LOGFILE}"

`tee` will report an error *before*  `check_we_are_root` tells us to restart the
script as root; this is noise.

##
# Loop
## How to redirect the output of every command executed inside a for loop into a file?

Write your redirection operator after the `done` keyword.

Example:

        for dir in $(tr ':' ' ' <<<"${PATH}"); do
          echo "I got the name ${dir}"
        done >file
             ^---^

This loop writes the names of all the directories of PATH inside a file.

Note that even though several `echo` are executed, you don't need `>>`.
Using `>` works fine, because it applies to a single `for` loop.
So, the output of the last `echo`  doesn't overwrite the outputs of the previous
ones, because they're all part of the same loop.

## How to pipe the output of all the commands executed inside a for loop through another utility?

Add the `|` operator after the `done` keyword.

Example:

        for dir in $(tr ':' ' ' <<<"${PATH}"); do
          ls "${dir}" 2>/dev/null
        done | sort >file
             ^----^

This loop writes the SORTED names of all the programs in the directories of PATH
inside a file.

##
# Pattern
## What's the difference between `[[ str == pat ]]` and  `[[ str =~ pat ]]`?

The `==` operator allows you to use the metacharacters documented in
`man fnmatch` (fn = filename), i.e. the ones you use in a glob.

The `=~` operator allows you to use any metacharacter valid in an extended regex.

## What's the output of `[[ abc =~ b ]]`?  `[[ abc == b ]]`?  `[[ abc == *b* ]]`?

    [[ abc =~ b ]]
    0, true because 'abc' contains 'b'~

    [[ abc == b ]]
    1, false because 'abc' is not 'b'~

    [[ abc == *b* ]]
    0, true because 'abc' contains 'b'~

Bottom line:
When you use `==`, the pattern must  describe the entire string, not just a part
of it.

Source:
<https://unix.stackexchange.com/questions/119493/whats-the-difference-between-and/119495#comment187541_119495>

## Which operator should I use to check a NON-match (i.e. equivalent of `!~`)?

Use the `!` operator to negate the test.

    [[ ! foo =~ bar ]]
       ^

##
## How to include a space in a pattern?  (2)

    [[:blank:]] = [ \t]
    [[:space:]] = [ \t\n\r\f\v]

## How to describe a non-digit in a pattern?

    [^[:digit:]]

##
# Debug
## How to debug a script?

Include the statement `set -xuv` at the beginning of the script.

`set -x` will print the script lines as they're executed.
In practice, it enables the `xtrace` option  which will make the shell print the
expanded value of PS4, followed by the command and its expanded arguments.

`set -u` will treat unset parameters as an error when performing parameter
expansion, and make the script exits with a non-zero status.
Useful to detect a misspelled variable name.

`set -v` will print the script lines as they're read.

##
# Issues
## `[ -n $TMUX ] && echo 'inside tmux'` outputs `inside tmux` even outside tmux!

You need to quote the variable:

    [ -n "$TMUX" ] && echo test
         ^     ^

When `$TMUX` is unquoted, a blank value will cause it to wordsplit and disappear.
If `$TMUX` is empty, these two statements are identical:

    [ -n $TMUX ]
    [ -n ]

`[ string ]` is shorthand for testing if a string is empty.
This is still true when string happens to be `-n`.
`[ -n ]` is therefore true, and by extension so is `[ -n $TMUX ]`.

See: <https://github.com/koalaman/shellcheck/wiki/SC2070>

## After executing my script, the prompt is not redrawn!

MWE:

        #!/bin/bash
        echo '' | tee /tmp/file &

Invoke the wait command to discover the termination status of the job.

        #!/bin/bash
        echo '' | tee /tmp/file &
        wait

---

Another MWE:

        % tty
        /dev/pts/10~
        # open another terminal
        % echo 'written from another terminal' >/dev/pts/10

---

If you  know how much  time the job  is going to take,  you could also  make the
script sleep a little:

        #!/bin/bash
        echo '' | tee /tmp/file &
        sleep .001

The mere execution of  a command after the job has finished  will make the shell
redraw the prompt.

But in practice, you won't know how much time you have to wait.

##
# Todo
## `set -e`

Maybe you should document this command.
It's used when you want your script to stop as soon as an error is raised by a command.

See `man bash /SHELL BUILTIN COMMANDS/;/^\s*set [`.

Although,  the  command is  not  reliable,  and  because  of this,  some  people
recommend to avoid it:
<http://mywiki.wooledge.org/BashFAQ/105>

---

`set -e` can  be useful to make a  script stop whenever a function  exits with a
non-zero status (no matter the nesting level):
<https://stackoverflow.com/a/9893727/9780968>

Although, there're other ways to achieve the same result:

   - <https://unix.stackexchange.com/a/48550/289772>
   - <https://stackoverflow.com/a/9894126/9780968>

---

If you use `set -e`, you'll need to systematically pass `-f` to `rm(1)`, and `-p` to `mkdir(1)`.
Even if they seem unnecessary.
This is because they suppress errors.

For  commands which  don't provide  an option  suppressing errors,  you need  to
temporarily toggle `set -e`:

    set +e
    problematic_command
    set -e

## ?

In some scripts (or makefiles), we may set variables and then refer to them in paths.
It would be nice if ^x^f could complete those kind of paths.
You could supercharge  our current ^x^f, and make it  check whether the variable
is in the current environment, and if  it's not, it could look for an assignment
in the current file.

<https://vi.stackexchange.com/a/20267/17449>

