# a
## alias/function

An alias is a word which is expanded by the shell into an arbitrary command-line.
A function allows a set of commands to be executed with a simple word.

## argument

From the shell's point of view, everything is an argument.
For example:

        $ ls -I README -l foo 'bar car' baz

The shell parses this command-line into 7 arguments passed to `execve()`:

        1. ls           command name
        2. -I           option
        3. README       parameter to the `-I` option
        4. -l           option
        5. foo          positional parameter
        6. 'bar car'    positional parameter
        7. baz          positional parameter

For more:
        https://stackoverflow.com/a/40654885/9780968

## associative array

It's an Abstract Data Type, composed of a collection of (key, value) pairs, such
that each possible key appears at most once in the collection.

A  hash table  is  a concrete  (!=  abstract) data  structure,  i.e. a  possible
implementation of an associative array.

For more info:
        # Relation and difference between associative array and hashing table?
        https://cs.stackexchange.com/a/6687

##
# f
## fork

When you  execute a shell command,  the shell duplicates itself  by invoking the
system call `fork()`.
The duplicate shell is called a “fork” of the original shell.

Then, the  fork replaces  its code  with the one  of the  command by  invoking a
family of system calls informally called “exec()”.

You can do manually replace the code of the current shell using the `$ exec` command:

        % echo $SHELL
        zsh~

        % exec bash

        $ echo $SHELL
        bash~

Here, `exec bash` has not started a subshell.
You're still in the  same process, which is confirmed by the  fact that when you
press `C-d`, the  terminal window closes (instead of getting  back to the prompt
of the parent shell).

For more info:
        $ man 3 exec

##
# j
## job

It's a background process.

A background process doesn't read its input from the terminal anymore.
Also, it doesn't receive keyboard-generated signals.

This gives back to the user the control of the shell.

##
# k
## keymap (zsh)

It's a set of bindings between sequences of keys and ZLE commands.

You can add a new binding inside a keymap with the `bindkey` command.

Initially, there are only 3 keymaps:

        ┌─────────┬─────────────────────────────────┐
        │ emacs   │ EMACS emulation                 │
        ├─────────┼─────────────────────────────────┤
        │ viins   │ vi emulation - insert mode      │
        │ vicmd   │ vi emulation - normal mode      │
        │ viopp   │ vi emulation - operator pending │
        │ visual  │ vi emulation - selection active │
        ├─────────┼─────────────────────────────────┤
        │ isearch │ incremental search mode         │
        ├─────────┼─────────────────────────────────┤
        │ command │ read a command name             │
        ├─────────┼─────────────────────────────────┤
        │ .safe   │ fallback keymap                 │
        └─────────┴─────────────────────────────────┘

##
# o
## option

An option is  an optional argument to  a command, which is  documented (i.e. you
can't write any arbitrary option name), and whose possible values are hard coded
in the program.

A boolean option is sometimes called “flag” or “switch”.
##
# p
## parameter

A parameter  is an argument that  provides information to either  the command or
one of its options.

E.g., in `-o file`, `file` is the parameter of the `-o` option.

Unlike options, whose possible values are hard coded in programs, parameters are
usually not, so the user is free to use whatever string suits their needs.

If you  need to  pass a  parameter that looks  like an  option but  shouldn't be
interpreted as such, you can separate it from the options with a double hyphen.

For more:
        https://stackoverflow.com/a/36495940/9780968
        https://stackoverflow.com/a/40654885/9780968

## special parameter

A parameter whose meaning is entirely defined by the shell:

        $*
        $@
        $#
        $?
        $-
        $$
        $!
        $0
        $_

## positional parameter

Any remaining arguments after the options have been consumed are commonly called
positional parameters  when the  order in  which they  are given  is significant
(this is in contrast to options which usually can be given in any order).

In a script, you can access them through the variables `$1`, `$2`, ...
And you can access the script name with `$0`.

## process

A program is executed in a process running in the computer's memory.

A process stores some information about the program it's executing:

   - PID
   - state (running, stopped, ...)
   - cwd
   - environment variables

## program

Code stored in a file on the hard drive.

##
# s
## shell

Interface between the user (or a script) and the kernel.

## syntaxic whitespace

Unquoted/unescaped space or tab.

This is a whitespace which has a special meaning to the shell.

##
# v
## variable

A parameter whose first character matches`[a-zA-Z0-9_]`.

## environment variable

Parameter stored in the current shell's environment.

It will be automatically passed to any child process of the shell.
It allows inter-process communication.

##
# w
## widget (zsh)

It's an interactive editing command.
E.g. `up-line-or-history`.

"Widget" refers to something the (zle) editor does when you hit a key.

"Widget" is used instead of "command"  or "function", because those words can be
confusing, and be interpreted as a normal shell command/function.

A widget is usually bound to a sequence of keys inside a ZLE keymap, and calls a
builtin or custom function:

    keyseq → widget → function

## widget function (zsh)

A shell function that is used to add a new widget which extends the line editor.

