    " ✘
    prof start /tmp/log | prof! file /tmp/vim.vim | so /tmp/vim.vim
    profd file /tmp/vim.vim

    " ✘
    prof start /tmp/log | prof! file */search.vim | ru! */search.vim
    profd file */search.vim

    " ✘
    prof start /tmp/log | prof! file ~/.vim/pack/mine/opt/search/autoload/search.vim | so ~/.vim/pack/mine/opt/search/autoload/search.vim
    profd file ~/.vim/pack/mine/opt/search/autoload/search.vim

    " ✔
    prof start /tmp/log | prof! func search#wrap_n | so ~/.vim/pack/mine/opt/search/autoload/search.vim
    profd func search#wrap_n

    " ✔
    prof start /tmp/log | prof! func Func | so /tmp/vim.vim
    profd func Func

# How to debug an autocmd which is fired when Vim quits?  (i.e. I don't have the time to read the error message)

Start Vim with `-V15/tmp/log`.
Then read the log.

# How to write a shell command starting Vim with a minimal vimrc, whose contents is not written in a file?

    $ vim -Nu <(tee <<'EOF'
    cmd1
    cmd2
    ...
    EOF
    )

This lets you avoid writing the vimrc in a file, which you would do by running 2
commands:

    $ tee <<'EOF' /tmp/vimrc
    cmd1
    cmd2
    ...
    EOF

    $ vim -Nu /tmp/vimrc

##
# Startup
## What are the locations from which Vim sources files when I start it with `$ vim -Nu NORC`?

   1. `~/.vim/plugin/**/*.vim`
   2. `$VIMRUNTIME/plugin/**/*.vim`
   3. `~/.vim/pack/*/start/*/plugin/**/*.vim`
   4. `~/.vim/pack/*/start/*/after/plugin/**/*.vim`
   5. `~/.vim/after/plugin/**/*.vim`

TODO:  Shouldn't the step 3 come *before* 2?

### And if I
#### start it with `$ vim -Nu /tmp/empty_vimrc.vim`?

 1. `/tmp/empty_vimrc.vim`
 2. `~/.vim/plugin/**/*.vim`
 3. `$VIMRUNTIME/plugin/**/*.vim`
 4. `~/.vim/pack/*/start/*/plugin/**/*.vim`
 5. `~/.vim/pack/*/start/*/after/plugin/**/*.vim`
 6. `~/.vim/after/plugin/**/*.vim`

#### write `filetype plugin indent on` in the vimrc?

During the sourcing of the vimrc, and before `~/.vim/plugin/`, Vim sources:

   1. `$VIMRUNTIME/ftplugin.vim`
   2. `$VIMRUNTIME/indent.vim`
   3. `$VIMRUNTIME/syntax/{syntax,synload,syncolor}.vim`

#### write `colo default` at the end of the vimrc?

During the sourcing of the  vimrc, after the filetype/indent/syntax plugins, and
before `~/.vim/plugin/`, Vim sources:

   1. `$VIMRUNTIME/colors/default.vim`

#### add `:packadd!` statements?

Right after `~/.vim/plugin/`, Vim sources the files in `~/.vim/pack/{minpac,mine}/opt/plugin/`.

And right before `~/.vim/after/plugin/`, Vim sources the files in
`~/.vim/pack/{minpac,mine}/opt/*/after/plugin/`.
Those are rare.
The only directory matching this pattern atm on my machine is
`~/.vim/pack/minpac/opt/ultisnips/after/plugin/`.

##
## If I start `$ vim --noplugin`, is `~/.vim/plugin/vim-foo/ftdetect/foo.vim` still sourced?

Yes.

## What's the effect of `--noplugin` when passed to `vim(1)`?

It prevents Vim from sourcing any script in a `plugin/` directory.
Other files/directories are unaffected.

Don't be confused by the word “plugin”.
Usually it's used to refer to a set of related files with a common purpose.
But for Vim, “plugin files” are just the files in a `plugin/` directory.

##
## How to start Vim with no script sourced?

    $ vim -Nu NONE

or

    $ vim -Nu NORC --noplugin
              │      │
              │      └ same as:  --cmd 'set noloadplugins'
              │
              └ nothing except the plugins

### With only the filetype/indent/syntax plugins?

    $ vim -Nu NONE --cmd 'filetype plugin indent on | syntax enable'
                     │
                     └ execute the command before the vimrc

This will make Vim source the scripts:

    ~/.vim/filetype.vim
    $VIMRUNTIME/filetype.vim
    $VIMRUNTIME/ftplugin.vim
    $VIMRUNTIME/indent.vim
    $VIMRUNTIME/syntax/{syntax,syntax,syncolor}.vim

#### my local plugins?

    $ vim -Nu NORC

This will make Vim source the plugins in:

    ~/.vim/plugin/**/*.vim
    $VIMRUNTIME/plugin/**/*.vim
    ~/.vim/after/plugin/**/*.vim

#### my local plugins and the filetype/indent/syntax plugins?

    $ vim -Nu NORC --cmd 'filetype plugin indent on | syntax enable'

This will make Vim source the scripts:

    ~/.vim/filetype.vim
    $VIMRUNTIME/filetype.vim
    $VIMRUNTIME/ftplugin.vim
    $VIMRUNTIME/indent.vim
    $VIMRUNTIME/syntax/{syntax,synload,syncolor}.vim

    ~/.vim/plugin/**/*.vim
    $VIMRUNTIME/plugin/**/*.vim
    ~/.vim/after/plugin/**/*.vim

In effect,  you're starting Vim  with everything except the  third-party plugins
handled by your plugin manager.

Note that  you could change  the order of  these 2 blocks  by using `+`  or `-c`
instead of `--cmd`.

#### the plugin `vim-foo`?

                   v---v         v
    $ vim -Nu NORC --cmd 'set rtp^=/path/to/vim-foo rtp-=~/.vim rtp-=~/.vim/after'
                                                       │           │
                                                       │           └ disable `~/.vim/after/plugin/*.vim`
                                                       └ disable `~/.vim/plugin/*.vim`

Make sure to use `--cmd`, and not `+` or `-c`, so that the path to the plugin is
added to the rtp *before* Vim looks for plugins to source.
Otherwise, the interface of `vim-foo` won't be sourced.

Also, make sure to use `^=` instead of `+=`.

---

Note that by default, there's no way to just source one plugin.
Either you start Vim  with `-Nu NONE` and no plugin is sourced,  or you start it
with `-Nu NORC`, and all the plugins in these directories are sourced:

   - ~/.vim/plugin/
   - $VIMRUNTIME/plugin/
   - ~/.vim/after/plugin/

A guard such as:

    if stridx(&rtp, 'vim-exchange') == -1
        finish
    endif

Or:

    if !exists('g:loaded_sandwich')
        finish
    endif

can disable most plugins in `~/.vim/{after/}plugin/`.

But some  files, such  as `~/.vim/after/plugin/nop.vim`,  can't be  guarded like
this because they're not associated to any third-party plugin.
Which is why we always also use this guard:

    if exists('g:no_{after_}plugin')
        finish
    endif

##
## `:Scriptnames` tells me that some sourced files are not plugins.  Which reasons did Vim have to source them?

They've been sourced by either:

   - an autocmd

   - some interface (mapping, custom Ex command, ...)
     which triggered the sourcing of an autoloaded script

    - a filetype/syntax/indent plugin for a buffer

##
# Verbosity
## How to increase Vim's verbosity level during
### Vim's startup?

Use the `-V` argument:

    $ vim -V2 file

### Vim's startup AND redirect the messages in a file?

Use the `-V` argument:

    $ vim -V2/tmp/messages file
             │
             └ do NOT add a space,
               otherwise Vim will interpret `/tmp/messages` as a regular file to edit,
               instead of the file where to redirect all messages

Technically, this command sets two options:

   - &vbs = 2
   - &vfile = /tmp/log

### the execution of a single Ex command?

    :2verb Cmd

### the execution of several commands separated by bars?

`:verb` only applies to the command up to the next bar, so this doesn't work:

    :2verb set vbs | set vbs
    verbose=2  ✔˜
    verbose=0  ✘˜

You muse also use `:exe`:

    :2verb exe 'set vbs | set vbs'
    verbose=2  ✔˜
    verbose=2  ✔˜

##
## What's the maximum verbosity level above which you shouldn't go without redirecting the messages in a file?

8.

From 9 and above, Vim displays a message for every autocmd executed.
If you  have an  autocmd listening  to `CursorMoved`,  you won't  be able  to do
anything, without being constantly interrupted by a message.

## What to do if Vim's display too many messages after increase its verbosity level?

Redirect them in a file:

    :set vfile=/tmp/messages

        THEN

    :set vbs={lvl}
    :cmd1
    :cmd2
    :cmd3
    ...
    :set vbs=0

        OR

    :{lvl}verb cmd

        FINALLY

    :set vfile=

## What are the six things for which I can ask the last file to have changed their definition?   How to ask?

    ┌─────────────────┬──────────────────┐
    │ augroup         │ verb au foo      │
    ├─────────────────┼──────────────────┤
    │ command         │ verb com Cmd     │
    ├─────────────────┼──────────────────┤
    │ function        │ verb fu Func     │
    ├─────────────────┼──────────────────┤
    │ highlight group │ verb hi HG       │
    ├─────────────────┼──────────────────┤
    │ mapping         │ verb map lhs     │
    ├─────────────────┼──────────────────┤
    │ option          │ verb set option? │
    └─────────────────┴──────────────────┘

##
## Above which verbosity level does Vim display a message when:
### a file is sourced?

2

### a tags or include file is searched?

5

### the viminfo file is read/written?

1

### an exception is thrown, caught, finished, discarded?

13

### an exception or a command is suspended while a finally clause is processed?

14

### a function is executed?

12

### an Ex command is executed?

15

### an autocmd is executed?

9

### a shell command is executed (via `:!`, `:make`, `:grep`, `system[list]()`, backtick expansion ...)?

4

### a group of autocommands is executed for a file?

8

##
## What are the three type of messages for which you can read/set the last message?   How?

    ┌─────────┬──────────────────────────┬──────────────────────────┐
    │ type    │ how to read last message │ how to set last message  │
    ├─────────┼──────────────────────────┼──────────────────────────┤
    │ Error   │ echo v:errormsg          │ let v:errormsg = 'foo'   │
    ├─────────┼──────────────────────────┼──────────────────────────┤
    │ Status  │ echo v:statusmsg         │ let v:statusmsg = 'foo'  │
    ├─────────┼──────────────────────────┼──────────────────────────┤
    │ Warning │ echo v:warningmsg        │ let v:warningmsg = 'foo' │
    └─────────┴──────────────────────────┴──────────────────────────┘

## What type of message does `:verb cmd` give?

Status.

## Does `:sil verb cmd` prevent Vim from giving and displaying messages?

Yes:

    :sil verb ru foobar.vim
    no message displayed˜
    no message added in `:mess`˜

## How to react to a message given by `:verb cmd` without displaying any message?

    let v:statusmsg = ''

    sil verb cmd

    if v:statusmsg is# '...'
        " do sth
    endif

It works because `:sil verb` doesn't prevent Vim from populating `v:statusmsg`.

## How to debug 'fde', 'fex' or 'inde'?

By  default, Vim  doesn't give  any  error message  when an  error occurs  while
evaluating an expression used to set `'fde'`, `'fex'` or `'inde'`.

To change that, set `'debug'` and give it the value `msg` or `throw`:

    ┌─────────────────┬─────────────────────────────────────────────────────────────────────┐
    │ set debug=msg   │ Error messages that would otherwise be omitted will be given anyway │
    ├─────────────────┼─────────────────────────────────────────────────────────────────────┤
    │ set debug=throw │ Error messages that would otherwise be omitted will be given anyway │
    │                 │ and also throw an exception and set `v:errmsg`                      │
    └─────────────────┴─────────────────────────────────────────────────────────────────────┘

Warning:

It seems it can also produce false errors in irrelevant files.
Use sparingly, i.e. only when really needed.

#
#
# Profiling
## general plugin
### What are the five steps necessary to profile a script/function?

   1. set the location of the profile
   2. set the scripts/functions to profile
   3. source the scripts/functions
   4. use the script / invoke the function to use the functionality you want to profile
   5. quit/restart Vim

---

Yes, you need to source the scripts/functions unless they haven't been sourced yet.
I.e. you can skip step 3 iff the scripts/functions haven't been sourced before `:prof`.

### How to set the location of the profile?

    :prof start /tmp/profile.log

Here, the profile will be written in `/tmp/profile.log` once we leave Vim.
If `/tmp/profile.log` already exists, it will be overwritten.

### How to set the scripts/functions to profile?

    :prof! file {pat}
    :prof  func {pat}

### Does `:prof file */foo.vim` profile ALL commands in the matching files?

No.

Only the ones outside functions.

If you want to include the commands inside functions, you must use a bang:

    :prof! file */foo.vim
         ^

TODO: To get as much info as possible, you might also need to temporarily remove
an anti-reinclusion guard.  Make further tests and better document this pitfall.
Do we need `:Runtime` from `vim-scriptease`?

###
### From Vim, which commands should I execute to profile a script named `search.vim` in the rtp?

    :prof  start /tmp/profile.log
    :prof! file */search.vim
    :ru! autoload/search.vim

    " use the plugin, and reproduce the slowdown for which you want to know the cause
    " restart Vim

#### Same question, but from the shell?

    $ vim --cmd 'prof  start /tmp/profile.log' \
          --cmd 'prof! file  */autoload/search.vim' \
          -c    'e +/\\v%>12v%<34v. file' \
          -c    'norm n' \
          -cq

###
### When I profile a script from the shell, should I execute `:prof` via `--cmd` or `-c`?

`--cmd`.

Because after  `:prof` has been executed,  you must still source  the script you
want to profile.
Using  `--cmd`, you  have the  guarantee that  `:prof` will  have been  executed
before the script is sourced, which is required.

Note that `--cmd` is  not necessary if the script is  autoloaded, and not loaded
until you invoke some mapping/command.
But still, be consistent; always use `--cmd` to execute `:prof` from the shell.

### How to detect that a profiling is currently being performed?

During a profiling, `v:profiling` is set to 1.

### What to do if I must execute a command which has nothing to do with what I want to profile, during a profiling?

Temporarily pause the profiling:

    :prof pause
    " execute your irrelevant command
    :prof continue

##
## syntax plugin
### How to profile a syntax plugin?

Disable any feature which may interfere, such as `'cul'`, `'rnu'` and folding.

Then:

    :syntime clear
    :syntime on

    " if the buffer fits on one screen, execute `:redraw!` one or several times;
    " otherwise scroll from top to bottom of the buffer one or several times

    :syntime off
    :syntime report

### How to interpret a syntax plugin's profile?

The columns are:

    ┌─────────┬──────────────────────────────────────────────────────┐
    │ TOTAL   │ total time in seconds spent on matching this pattern │
    ├─────────┼──────────────────────────────────────────────────────┤
    │ COUNT   │ number of times the pattern was searched             │
    ├─────────┼──────────────────────────────────────────────────────┤
    │ MATCH   │ number of times the pattern actually matched         │
    ├─────────┼──────────────────────────────────────────────────────┤
    │ SLOWEST │ the longest time for one search                      │
    ├─────────┼──────────────────────────────────────────────────────┤
    │ AVERAGE │ the average time for one search                      │
    ├─────────┼──────────────────────────────────────────────────────┤
    │ NAME    │ name of the syntax item                              │
    ├─────────┼──────────────────────────────────────────────────────┤
    │ PATTERN │ the pattern being searched                           │
    └─────────┴──────────────────────────────────────────────────────┘

The lines are sorted by total time.

### How to reset the counters to zero (to restart a measuring for the current buffer)?

    :syntime clear

### What should I avoid when using `\@<=` or `\@<!` in a regex?

If you apply  these atoms to a sub-expression containing  a quantifier which can
match a  variable number of characters  (such as `*`), add  a reasonable maximum
size to avoid trying at all positions in the current and previous lines:

    \%(foo.*\)\@<=bar       ✘ too slow
    \%(foo.*\)\@123<=bar    ✔

##
# Testing
## Where can I learn how to write tests for Vim?

   - `:help testing`
   - `~/Vcs/vim/src/testdir/README.txt`
   - `~/Vcs/vim/src/testdir/runtest.vim`
   - `~/Vcs/vim/src/testdir/test_assert.vim`

## How can I run a specific test?

If you want to run all the tests in a particular file, use `make(1)`:

    $ cd ~/Vcs/vim/src/testdir; make test_vim9_func
                                     │
                                     └ name of the script testing the feature you're interested in

If you want to run a particular test in a particular file, use `vim(1)`:

    $ cd ~/Vcs/vim/src/testdir
    $ vim -u NONE -S runtest.vim test_vim9_func.vim bufname
                                                    │
                                                    └ name of the testing function without the "Test_" prefix
                                                      (e.g. "Test_bufname()")

Or set the `$TEST_FILTER` environment variable.  See `~/Vcs/vim/src/Makefile`:

   > # Set $TEST_FILTER to select what test function to invoke, e.g.:
   > #	export TEST_FILTER=Test_terminal_wipe_buffer
   > # A partial match also works:
   > #	export TEST_FILTER=wipe_buffer

### Where can I read the results?

    ~/Vcs/vim/src/testdir/test.log
    ~/Vcs/vim/src/testdir/messages

#
# Pitfalls
## Why should I always press Enter at the hit-enter prompt when an error is raised while I'm debugging some issue?

To be sure that you don't miss any error message.

Indeed, if:

   1. your errors are raised from a function evaluated in the rhs of an `<expr>` mapping
   2. this function is not defined with `abort`
   3. its body raises several errors

Then,  the errors  are printed  separately.  That  is, *each*  error message  is
followed by a its own hit-enter prompt.

    nno <expr> <c-b> Func()
    fu Func()
        invalid1
        invalid2
        invalid3
        return ''
    endfu
    call feedkeys("\<C-b>")

    Error detected while processing function Func:˜
    line    1:˜
    E492: Not an editor command:     invalid1˜
    Press ENTER or type command to continue˜
    Error detected while processing function Func:˜
    line    2:˜
    E492: Not an editor command:     invalid2˜
    Press ENTER or type command to continue˜
    Error detected while processing function Func:˜
    line    3:˜
    E492: Not an editor command:     invalid3˜
    Press ENTER or type command to continue˜

If at any point you press any key  other than Enter, like `Esc`, `C-c` or `C-l`,
you won't see the next errors.

Actually, if you press  `Esc`, it seems all error messages  are printed, but you
probably won't see  them (it depends on your `'timeout*'`  settings); if so, you
can still  retrieve them  with `:mess`,  but chances are  you won't  think about
doing it, and just wrongly assume that there is only one error.

## An exception has been thrown, and caught.  I can't see from where the error is raised!

First, increase the verbosity level to 2; then to 13.

Starting from  2, Vim will give  a message whenever  it sources a file;  it will
also print a message to tell you what causes the sourcing (e.g. autocmd).

Starting from 16, Vim  will give you the number of the line  in the script which
throws an error.   Be careful: with this level of  verbosity, Vim gets difficult
to use.  So, make sure to set `'verbosefile'` too:

                       v------------------v
    $ vim +'set vbs=16 vfile=/tmp/debug.log' -S /tmp/error_repro.vim +'qa!'
    $ vim /tmp/debug.log
    " /^Exception thrown

---

As an example, you might find something like this in the logfile:

    line 12: const FILTER_CMD = {
    Exception thrown: Vim(const):E15: Invalid expression: ]},

    finished sourcing ~/.vim/pack/mine/opt/qf/autoload/qf/preview.vim

This says that the error was raised from the line 12 in `autoload/qf/preview.vim`.
Then, you might read:

    continuing in FileType Autocommands for "qf"

This says that  the autoload script was sourced because  of an autocmd listening
to `FileType qf`.

Then, you might read:

    line 52:     catch
    Exception caught: Vim(const):E15: Invalid expression: ]},

    line 53:         return s:Catch()
    line 16:     echohl ErrorMsg
                                Vim(const):E15: Invalid expression: ]},
    line 23:     echohl NONE
    Exception finished: Vim(const):E15: Invalid expression: ]},

    :return  made pending

    line 54:     endtry
    :return  resumed

    <SNR>159_open returning ''

This says that the exception was caught on line 52 in the function `s:open()`.
The `:catch` clause has invoked `s:Catch()`, which has echo'ed the error message
on its lines 16 and 23.

Finally, you might read:

    continuing in qf#open_auto

    line 23:     endif
    qf#open_auto returning #0

    continuing in QuickFixCmdPost Autocommands for "*"

This says  that `s:open()` was  invoked from `qf#open_auto()`, which  itself was
run from a `QuickFixCmdPost` autocmd.

In this example, here is what could have happened:

   - `:helpg` is run interactively
   - `QuickFixCmdPost` is fired right afterward
   - a `QuickFixCmdPost` autocmd calls `qf#open_auto()`
   - `qf#open_auto()` calls `s:open()`
   - `s:open()` executes `:try | copen | catch | call s:Catch() | endtry`
   - `:copen` triggers `FileType qf`
   - an autocmd listening to `FileType qf` calls `qf#preview#mappings()`
   - to find the latter function Vim executes `:ru autoload/qf/preview.vim`

Finally,  `autoload/qf/preview.vim`  is sourced,  but  contains  an error  which
throws an exception.

Tip: Whenever you find a message like:

    continuing in FileType Autocommands for "qf"
    continuing in QuickFixCmdPost Autocommands for "*"
    ...

You can find out from where the autocmd has been installed with:

    :new|0pu=execute('verb au FileType qf')
    :new|0pu=execute('verb au QuickFixCmdPost *')
    ...

##
# Miscellaneous
## What's the difference between `--cmd` and `-c`/`+`?

   - `--cmd` execute a command BEFORE the vimrc is sourced.

   - `-c`    execute a command AFTER the first file is read
           which includes its autocmds and its modelines

`+` is a synonym of `-c`.

## When does an autocmd listening to `VimEnter` executes its command compared to `+'cmd'`?  Before or after?

After.

From `:h startup`:

   > 12. Execute startup commands
   > ...
   >         The commands given with the |-c| and |+cmd| arguments are executed.
   >         The |v:vim_did_enter| variable is set to 1.
   >         The |VimEnter| autocommands are executed.

Try this:

    $ vim -es -Nu NONE +'pu=v:vim_did_enter|%p' +'qa!'
    0˜

When the  `+` command was  processed, `v:vim_did_enter`  was not set  yet; which
means that `VimEnter` had not been fired.

##
# Debug mode
## What does the debug mode allow me to do?

Step through a sourced file or a user function.
Set breakpoints.

## Does the debug mode have side effects?

Yes.
For example, the display is messed up by the debugging messages.

## Is there an alternative to debug mode?

Yes.

Set the  `'verbose'` options or  use the  `:verbose` modifier to  increase Vim's
verbosity level.

## How to list all breakpoints?

    :breakl[ist]

##
# `:breakadd`  `:profile`  `:runtime`    ‘bpr’
## Do ‘bpr’ accept
### *absolute* file paths?

`:breakadd` and `:profile`, yes.
`:runtime`, no.

### *relative* file paths?   If so, how do they complete the path?

Yes, all of them.

---

`:breakadd` and `:profile` completes the path using the working directory:

    :breakadd file foo.vim
                ⇔
    :breakadd file cwd/foo.vim

---

`:runtime` completes the path using every path present inside `&rtp`:

    :runtime! file foo.vim
                ⇔
    :so dir1/foo.vim
    :so dir2/foo.vim
    ...

Where dir1, dir2, are in the rtp.

### *patterns*?   If so, which metacharacters can be used?

Yes, all of them.

You can use the metacharacters listed in `:h file-pattern`.

##
## What does `*` match in the pattern passed as an argument to
### `:{breakadd|profile}`?

Any string of characters (including a dot).

### `:runtime`?

In the last component of the path, a part of the filename:

    :ru! *foo.vim

Before the last component of the path, ONE directory:

    :ru! */foo.vim
    could source `plugin/foo.vim`˜

    :ru! */*/foo.vim
    could source `plugin/bar/foo.vim`˜

##
## How do ‘bpr’ interpret `*foo.vim`?   What about `*/foo.vim`?

    ┌────────────────────────────────┬─────────────────────────────────────────────────┐
    │ :{breakadd|prof} file *foo.vim │ any file anywhere BELOW a directory of the rtp, │
    │                                │ and whose name ENDS with `foo.vim`              │
    │                                │                                                 │
    │                                │ Examples:                                       │
    │                                │         .../plugin/foo.vim                      │
    │                                │         .../autoload/xfoo.vim                   │
    ├────────────────────────────────┼─────────────────────────────────────────────────┤
    │ :runtime! *foo.vim             │ any file INSIDE a directory of the rtp,         │
    │                                │ and whose name ENDS with `foo.vim`              │
    ├────────────────────────────────┼─────────────────────────────────────────────────┤
    │ :runtime! */*foo.vim           │ any file BELOW a directory of the rtp,          │
    │                                │ and whose name ENDS with `foo.vim`              │
    └────────────────────────────────┴─────────────────────────────────────────────────┘

    ┌─────────────────────────────────┬─────────────────────────────────────────────────┐
    │ :{breakadd|prof} file */foo.vim │ any file anywhere BELOW a directory of the rtp, │
    │                                 │ and whose name IS `foo.vim`                     │
    │                                 │                                                 │
    │                                 │ Examples:                                       │
    │                                 │         .../plugin/foo.vim                      │
    │                                 │         .../autoload/foo.vim                    │
    ├─────────────────────────────────┼─────────────────────────────────────────────────┤
    │ :runtime! */foo.vim             │ any file anywhere BELOW a directory of the rtp, │
    │                                 │ and whose name IS `foo.vim`                     │
    └─────────────────────────────────┴─────────────────────────────────────────────────┘

## Are the two wildcards necessary in
### `:{breakadd|prof} file */*foo.vim`?

No.  One is enough:

                          ┌ useless, because a single star can match two things at the same time:
                          │
                          │     - the path to a directory
                          │     - a part of a filename
                          │
                          ├┐
    :{breakadd|prof} file */*foo.vim

                    ⇔

    :{breakadd|prof} file *foo.vim

### `:runtime! */*foo.vim`?

Yes, if you  want to match a file  whose name ends with `foo.vim`,  you need the
second wildcard.
And if  it can be located  anywhere below a directory  of the rtp, you  need the
first wildcard.

    :runtime! */*foo.vim
              ├┘
              └ NOT useless,  because with `:ru`, a star can  NOT match the
                path to a directory and a part of a filename at the same time

##
## In a script, why doesn't this work:  `breakadd func s:Func`?

You need to translate `s:` manually:

    :exe 'breakadd func ' .. expand('<SID>') .. 'Func'

#
# Issues
## I'm writing a bug report for
### a crash
#### I need the Vim binary to include debugging symbols!

When you configure – before compiling – edit the file `src/Makefile`, to include
the `-g` flag in the `CFLAGS` variable, so that it's sent to the compiler.

    CFLAGS = -g
             ^^

See:

   - `:h debug-gcc`
   - <https://stackoverflow.com/a/1937428/9780968>

---

You don't  have to  do that manually;  we have  a zsh snippet  to compile  a Vim
binary with debugging symbols; use it.

##### It doesn't work!

Make sure  the `STRIP` variable is  not set to  the `strip(1)` binary, but  to a
dummy one like `/bin/true`:

    STRIP = /bin/true

####
#### How to get a backtrace without a core?

    $ gdb -q --args ~/Vcs/vim/src/vim -Nu NONE -S /tmp/crash.vim
    (gdb) set logging on
    # start Vim so that it crashes
    (gdb) run
    # Print the backtrace.
    # If it's too long, it will be printed in a pager.
    # If so, press Enter repeatedly to scroll until you reach the bottom of the pager.
    (gdb) bt full
    (gdb) quit
    # the backtrace should be in gdb.txt

#### I want a core, but Vim doesn't dump any!

Make sure you didn't set any limit on the size of core files which the OS can write:

    $ ulimit -c unlimited

Also, make sure that the `apport` service is at least temporarily stopped:

    $ sudo systemctl stop apport.service

You can start the service again later with:

    $ sudo systemctl start apport.service
                     ^---^

If the apport service is running while Vim crashes, the core might be
intercepted and written at `/var/lib/apport/coredump/`.
Interestingly enough, it seems that `apport` doesn't care about `ulimit(3)`.

---

Also, make  sure there  is no mismatch  between the version  of the  Vim process
which crashes, and the one of the installed binary.

That is,  when you  have such an  issue, restart your  Vim process  whenever you
update the Vim binary.  Otherwise, your OS  might not write a core file.  In the
system log  files, e.g.  in `/var/log/apport.log`, you  might find  some message
like this one:

    ERROR: apport (pid 1234) <some date>: executable was modified after program start, ignoring
                                          ^---------------------------------------------------^

#### I want my backtrace to contain as much info as possible (no <optimized out>)!

Edit `src/Makefile`  to pass  the `-O0`  flag to the  compiler via  the `CFLAGS`
variable:

    CFLAGS = -g -O0
                ^^^

#### When extracting the backtrace, I get a warning message!

    warning: exec file is newer than core file.

The last  time you've reproduced the  crash, there was probably  an existing old
core file in your working directory which prevented Vim from dumping a new one:

   1. remove the old core
   2. reproduce the crash again, to get a new core
   3. extract a backtrace from the latter

####
#### I need a valgrind log!

Run this:

    valgrind --leak-check=yes --num-callers=50 --track-origins=yes --log-file=valgrind.log ./src/vim -Nu NONE

After reproducing the issue, the log should be written in `./valgrind.log`.

Source: <https://github.com/vim/vim/issues/5410#issuecomment-569516803>
See also `:help debug-leaks`.

#### I need an asan log!

    $ git stash -a; git stash clear
    $ make clean; make distclean
    $ sed -i '/^#\s*SANITIZER_CFLAGS.*\\$/,/^$/ s/^#//' src/Makefile
    $ sed -i '/^#LEAK_CFLAGS = -DEXITFREE$/ s/^#//' src/Makefile
    $ ./configure
    $ make; tput bel

    $ ./src/vim -Nu NONE 2>asan.log

After reproducing the issue, the log should be written in `./asan.log`.

---

The purpose of the  first `sed(1)` command is to uncomment  an assignment to the
`SANITIZER_CFLAGS` option.  It assumes that the latter is:

   - written on multiple lines
   - its first line ends with a backslash (which makes the next newline treated as a line continuation)
   - its last line is followed by an empty line

Those assumptions are true at the time I'm writing this.
They  might be  wrong in  the future;  in which  case, you'll  have to  edit the
`sed(1)` command.

The purpose of the second `sed(1)` command  is to uncomment an assignment to the
`LEAK_CFLAGS` option, to avoid false reports.  From `src/Makefile`:

   > # You should also use -DEXITFREE to avoid false reports.

---

Note that in addition to compile Vim  with asan enabled, you can also compile it
with ubsan enabled:

   - option to enable asan (address sanitizer): `-fsanitize=address`
   - option to enable ubsan (undefined behavior sanitizer): `-fsanitize=undefined`

The previous `sed(1)` command should enable both:

    SANITIZER_CFLAGS = -g -O0 -fsanitize-recover=all \
                       -fsanitize=address -fsanitize=undefined \
                       -fno-omit-frame-pointer

An asan log looks like this:

    =================================================================
    ==126361==ERROR: AddressSanitizer: heap-use-after-free on address ...
    READ of size 1 at 0x603000006e86 thread T0
        #0 0x563acc3c9973 in free_type /home/lgc/Vcs/vim/src/vim9type.c:93
        #1 0x563acbc96ab7 in list_free_list /home/lgc/Vcs/vim/src/list.c:273
        #2 0x563acbc96d00 in list_free /home/lgc/Vcs/vim/src/list.c:302
        ...

An ubsan log looks like this:

    ex_docmd.c:2683:10: runtime error: load of null pointer of type 'char_u'

####
#### The devs can't reproduce my crash!

Try to reproduce in a docker container, so as to eliminate any interference from
your current environment (which can't be exactly the same as the one of the devs):

    # install docker
    $ sudo apt install docker.io

    # start Ubuntu 21.10 in a docker container
    $ sudo docker run --interactive=true --tty=true --rm=true ubuntu:21.10

    # install dependencies
    $ apt update
    $ apt --yes install git make gcc libncurses-dev

    # compile Vim
    $ git clone --depth=1 https://github.com/vim/vim
    $ cd vim
    $ make

    # reproduce the crash
    $ VIMRUNTIME=runtime ./src/vim -Nu NONE -U NONE -i NONE -S /tmp/crash.vim

##
### an internal error
#### How to get a backtrace?

You can try to make Vim crash.

In `src/Makefile`, uncomment this line:

    ABORT_CFLAGS = -DABORT_ON_INTERNAL_ERROR

I found `ABORT_CFLAGS` here: <https://github.com/vim/vim/issues/3177#issue-339241917>

You don't have to do that manually; use our zsh snippet to compile Vim.

##### It doesn't work!

Then try this:

   - start Vim in a terminal
   - in another terminal start gdb
   - in gdb, attach to the Vim process:

         (gdb) attach <PID>

   - set a break point to where the internal error is raised and continue execution

         (gdb) br file.c:1234
         (gdb) cont

   - in Vim, reproduce the internal error; it should reach the breakpoint in gdb
   - in gdb, when the breakpoint is reached, look at the stack using the `bt` command

         (gdb) bt full

Source: <https://github.com/vim/vim/issues/5674#issuecomment-838653020>

###
## I can't compile Vim.  The configure script gives an error!

Read `./src/auto/config.log`.
Look for the error message in there; it might look like this:

    configure:12143: error: NOT FOUND!
          You need to install a terminal library; for example ncurses.
          On Linux that would be the libncurses-dev package.
          Or specify the name of the library with --with-tlib.

Once found, look for the previous error message (the first one to cause the issue).

For example here:

    configure:12139: gcc -o conftest -g -O2  -Wl,--enable-new-dtags -Wl,-z,relro ...
    /usr/bin/ld: /tmp/ccP59uKl.o: relocation R_X86_64_32 against `.rodata.str1.1' can not be used when making a PIE object; recompile with -fPIC
    /usr/bin/ld: final link failed: Nonrepresentable section on output
    collect2: error: ld returned 1 exit status
    configure:12139: $? = 1
    configure: failed program was:
    | /* confdefs.h */
    | #define PACKAGE_NAME ""
    | #define PACKAGE_TARNAME ""
    | #define PACKAGE_VERSION ""
    | ...
    | /* end confdefs.h.  */
    | int tgetent(char *, const char *);
    | int
    | main ()
    | {
    | char s[10000]; int res = tgetent(s, "thisterminaldoesnotexist");
    |   ;
    |   return 0;
    | }
    configure:12143: error: NOT FOUND!
          You need to install a terminal library; for example ncurses.
          On Linux that would be the libncurses-dev package.
          Or specify the name of the library with --with-tlib.

The previous error is given by `ld.bfd(1)`:

    /usr/bin/ld: /tmp/ccP59uKl.o: relocation R_X86_64_32 against `.rodata.str1.1' can not be used when making a PIE object; recompile with -fPIC

Notice the suggestion at the end:

    ...; recompile with -fPIC
         ^------------------^

So, try to recompile with these flags:

    CFLAGS=-fPIC ./configure ...
    ^----------^

## Some global variable is created, but I don't know which script did it!

    $ vim -V15/tmp/log
    :q

    $ vim /tmp/log
    /g:your_variable

## I install an Ex command in a plugin, but when I start Vim, it's not there!

    $ vim -V16/tmp/log
    :q
    $ vim /tmp/log
    /YourCommand

Yes, this is (almost) the same answer as the previous one.
The point is, when some interface is wrong because:

   - it contains an incorrect value
   - it should exist, but it does not
   - it shouldn't exist, but it does

And you don't know why that is the  case, a verbose log will tell you everything
Vim did, and why.

Alternatively, you can try to `:vimgrep` your config files.

##
## I'm trying to profile a script, but nothing is written in the profile file.  Why?

The script must be sourced *after* `:prof`.
So, pay attention to the relative order  in which you execute `:prof` and source
your script.

    " ✘
    :ru! autoload/search.vim
    :prof  start /tmp/profile.log
    :prof! file */autoload/search.vim

    " ✔
    :prof  start /tmp/profile.log
    :prof! file */autoload/search.vim
    :ru! autoload/search.vim

---

    # ✘
    $ vim -c 'prof  start /tmp/profile.log' \
          -c 'prof! file  */statusline.vim' \
          -cq

    # ✔
    $ vim --cmd 'prof  start /tmp/profile.log' \
          --cmd 'prof! file  */statusline.vim' \
          -cq

If you use `-c` to execute `:prof`, it will be executed *after* the interface of
your plugins has been sourced, and thus the profiling won't work.

## Why is `:prof start {fname}` dangerous?

If `{fname}` already exists, it will be silently overwritten.
Make sure  to not  mix the name  of the file  where you  want the output  of the
profiling to be written, with the name of the script you want to profile:

    ✘
    :prof start script.vim
    :prof file foo

    ✔
    :prof start foo
    :prof file script.vim

## I've executed `:4verb grep! pat .`, but I can't see the exact shell command which was invoked by Vim!

In this case,  the output of the  shell command is temporarily  displayed in the
terminal, not in a Vim buffer.
And if it's long, you may need to scroll back (tmux copy-mode), to see the exact
shell command which was executed at the beginning.

## I've executed `:4verb cexpr system('grep -RHIins pat *')`, and I have the same issue!

Press `j` then `k`.

The message has been emitted, but not drawn.
Force a redraw by moving the cursor.

MRE:

    $ mkdir /tmp/test && cd /tmp/test
    $ echo 'pat' >>file{1..5}

    $ cat /tmp/vimrc
        augroup myquickfix
            au!
            au QuickFixCmdPost * cw
        augroup END
        filetype plugin indent on

    $ vim -Nu /tmp/vimrc
    :4verb cexpr system('grep -RHIins pat *')

#
#
#
# Profiling

    :profd[el] ...

Stop profiling for the arguments specified.
See `:breakdel` for the arguments.

---

You must always start with a `:prof start fname` command.
The resulting file is written when Vim exits.
Here  is  an  example  of  the  output, with  line  numbers  prepended  for  the
explanation:

  1 FUNCTION  Test2()
  2 Called 1 time
  3 Total time:   0.155251
  4  Self time:   0.002006
  5
  6 count  total (s)   self (s)
  7     9              0.000096   for i in range(8)
  8     8   0.153655   0.000410     call Test3()
  9     8              0.000070   endfor
 10                               " Ask a question
 11     1              0.001341   echo input("give me an answer: ")

The header (lines 1-4) gives the time for the whole function.
The `Total` time is the time passed while the function was executing.
The `Self` time is the `Total` time reduced by time spent in:

   - other user defined functions
   - sourced scripts
   - executed autocommands
   - external (shell) commands

Lines 7-11 show the time spent in each executed line.
Lines that are not executed do not count.
Thus a comment line is never counted.

The Count column shows how many times a line was executed.
Note that the `for` command in line 7 is executed one more time as the following
lines.
That is because the line is also executed to detect the end of the loop.

The time Vim spends waiting for user input isn't counted at all.
Thus how long you take to respond to the input() prompt is irrelevant.

Profiling should give a good indication of where time is spent, but keep in mind
there are various things that may clobber the results:

   - The accuracy of the time measured depends on the gettimeofday() system
     function.  It may only be as accurate as 1/100 second, even though the times
     are displayed in micro seconds.

   - Real elapsed time is measured, if other processes are busy they may cause
     delays at unpredictable moments.  You may want to run the profiling several
     times and use the lowest results.

   - If you have several commands in one line you only get one time.  Split the
     line to see the time for the individual commands.

   - The time of the lines added up is mostly less than the time of the whole
     function.  There is some overhead in between.

   - Functions that are deleted before Vim exits will not produce profiling
     information.  You can check the `v:profiling` variable if needed:

           if !v:profiling
               delfunc MyFunc
           endif

   - Profiling may give weird results on multi-processor systems, when sleep
     mode kicks in or the processor frequency is reduced to save power.

   - The `self` time is wrong when a function is used recursively.

# profiling

    :profdel file */search.vim

            Arrête le profilage des fichiers dont le chemin match `*/search.vim`.


                                               NOTE:

            Il semble  qu'il faille réutiliser  le même pattern qu'on  a utilisé
            dans `:prof file pat`.
            On ne peut donc pas exécuter:

                    ✘
                    prof!   file pack/mine/opt/search/autoload/search.vim
                    profdel file */search.vim

            Car `:prof!  file` a reçu en  argument un chemin absolu,  tandis que
            `:profdel file` a reçu un glob.
            En revanche, on peut exécuter:

                    ✔
                    prof!   file pack/mine/opt/search/autoload/search.vim
                    profdel file pack/mine/opt/search/autoload/search.vim

                    ✔
                    prof!   file */search.vim
                    profdel file */search.vim


    vim --cmd 'prof  start /tmp/script.profile' \
        --cmd 'prof! file  */search.vim' \
        -c    'e +/\\v%>43v%<46v. ~/Dropbox/conf/cheat/vim' \
        -c    'norm n' \
        -cq

            Illustre comment on peut tester un  script et générer un rapport, en
            une seule commande shell, en combinant les arguments:

                    * --cmd    pour profiler le script
                    * -c       pour tester   "

            Dans cet exemple, on cherche à  voir quelle commande de notre plugin
            `vim-search` prend le plus de temps qd on cherche une regex complexe
            dans un grand fichier.


    FUNCTIONS SORTED ON SELF TIME
    count  total (s)   self (s)  function
        2              2.216095  <SNR>91_matches_in_range()
        1   2.288223   0.071750  search#matches_print()
        1              0.000222  <SNR>91_matches_in_line()
        1              0.000180  search#set_nohls()
        1   2.216473   0.000156  <SNR>91_matches_count()
        1   0.000125   0.000110  7()
        1   0.000058   0.000034  search#wrap_n()
        1              0.000031  search#nice_view()
        2              0.000025  8()
        1              0.000024  <SNR>91_set_hls()
        1   0.000153   0.000018  search#blink()
                                    search#wrap_gd()
                                    <SNR>91_cr_ex()
                                    search#set_nohls_on_leave()
                                    <SNR>91_reset_more()
                                    <SNR>91_snr()
                                    <SNR>91_matches_above()
                                    search#wrap_cr()
                                    search#wrap_star()
                                    search#escape()

            Exemple de résumé qu'on peut trouver à la fin d'un rapport de profilage:

                    ┌───────┬─────────────────────────────────────────────────────────────────────┐
                    │ count │ nb de fois que la fonction a été invoquée                           │
                    ├───────┼─────────────────────────────────────────────────────────────────────┤
                    │ total │ temps total pris par la fonction                                    │
                    ├───────┼─────────────────────────────────────────────────────────────────────┤
                    │ self  │ temps total pris par les commandes de la fonction, en dehors de(s): │
                    │       │                                                                     │
                    │       │         - invocations de fonctions utilisateurs externes            │
                    │       │         - scripts sourcés                                           │
                    │       │         - autocmds                                                  │
                    │       │         - commandes shell externes                                  │
                    └───────┴─────────────────────────────────────────────────────────────────────┘

            L'info à laquelle  accorder le plus d'importance n'est  pas le temps
            de la colonne `total`, mais celui de `self`.

            En effet, une  fonction A peut prendre du temps  car elle en appelle
            une autre B, qui est mal optimisée.

            Ce point est illustré dans le rapport précédent.
            Bien que `search#matches_print()` et `<snr>91_matches_count()` aient
            l'air de prendre beaucoup de temps:

                    1   2.288223   0.071750  search#matches_print()
                    1   2.216473   0.000156  <SNR>91_matches_count()

            ... c'est `<SNR>91_matches_in_range()` qui est le réel pb:

                    2              2.216095  <SNR>91_matches_in_range()


    FUNCTION  <SNR>91_matches_in_range()
    Called 2 times
    Total time:   2.216095
     Self time:   2.216095

    count  total (s)   self (s)
        2              2.216045     let output = execute(a:range.'s///gen')
        2              0.000046     return matchstr(output, '\d\+')->str2nr()


            Un  rapport de  profilage  ne  permet pas  seulement  de trouver  la
            fonction qui  prend le  plus de  temps, il  contient aussi  le temps
            passé à exécuter chaque commande d'une fonction.
            On peut donc aller plus loin et chercher la commande prenant le plus
            de temps.

            Ici, on sait que le pb vient de `<SNR>91_matches_in_range()`.
            On a  donc cherché la section  du rapport la détaillant,  et on peut
            s'apercevoir que la commande qui pose pb est:

                    let output = execute(a:range.'s///gen')

#
#
#
# Todo

If  your Vim  is  slow, but  you  don't know  exactly  which function/plugin  is
responsible, you can still use `:prof` to find it out:

    :prof start /tmp/profile.log
    :prof func *
    :prof file *
    " At this point do slow actions
    :prof pause
    :noa qall!

Source: <https://stackoverflow.com/a/12216578/9780968>

To document.

---

After a profiling, maybe we should always run `:prof pause` then `:noa qa!`.
<https://vi.stackexchange.com/a/20276/17449>

---

<https://www.dannyadam.com/blog/2019/05/debugging-in-vim/>

---

We've lost  time debugging dirvish,  because the issue was  not in vimrc  but in
filetype plugin.  How to avoid it in the future?

Update:
You should find a succession of commands loading more and more files.
Example:

    $ vim -Nu NONE
    $ vim -Nu NORC
    $ vim -Nu /tmp/vimrc (with only filetype plugin indent on)
    $ vim

Also, use `:Scriptnames` to see a list of all the loaded scripts.

If there's no problem with `vim -Nu NONE`, but there's one with
another command sourcing more files, then the issue is in one of
the files listed `:Scriptnames`.

---

What kind of info does the verbose level 16 give access to?

<https://github.com/vim/vim/commit/4facea310c2788c88f021b262658b847381a50a8>

##
# OBSCURE

:debugg[reedy]

                Read debug mode  commands from the normal  input stream, instead
                of getting them directly from the user.
                Only useful for test scripts.
                Example:

                                           ┌ start in Ex mode
                                           │
                        echo 'q^Mq' | vim -e -s -c debuggreedy -c 'breakadd file script.vim' -S script.vim
                                              │
                                              └ :h -s-ex :

                                                     Switches off most prompts, informative messages,
                                                     warnings and error messages.

:0debugg[reedy]

                Undo `:debuggreedy`:  get debug mode commands  directly from the
                user, don't use typeahead for debug commands.

# STARTING DEBUG MODE

To enter debugging mode use one of these methods:

1. Start Vim with the `-D` argument:

         $ vim -D file.txt

   Debugging will start as soon as the first vimrc file is sourced.
   This is useful to find out what is happening when Vim is starting up.
   A  side   effect  is  that   Vim  will   switch  the  terminal   mode  before
   initialisations have finished, with unpredictable results.
   For a GUI-only version (Windows, Macintosh)  the debugging will start as soon
   as the GUI window has been opened.
   To make this happen early, add a `:gui` command in the vimrc file.

2. Run a command with `:debug` prepended.
   Debugging will only be done while this command executes.
   Useful for debugging a specific script or user function.
   And for scripts and functions used by autocommands.
   Example:

         :debug edit test.txt.gz

3. Set a breakpoint in a sourced file or user function.
   You could do this in the command-line:

         $ vim -c 'breakadd file */explorer.vim' .

   This will run Vim and stop in the first line of the 'explorer.vim' script.
   Breakpoints can also be set while in debugging mode.

In debugging mode every executed command is displayed before it is executed.
Comment lines, empty lines and lines that are not executed are skipped.
When  a line  contains two  commands,  separated by  `|`, each  command will  be
displayed separately.

# DEFINING BREAKPOINTS

:breaka[dd] func [lnum] {name}

                Set a breakpoint in a function.  Example:

                        :breakadd func Explore

                Doesn't check for a valid function name, thus the breakpoint
                can be set before the function is defined.

:breaka[dd] file [lnum] {name}

                Set a breakpoint in a sourced file.  Example:

                        :breakadd file 123 .vimrc

:breaka[dd] here

                Set a breakpoint in the current line of the current file.
                Like doing:

                        :breakadd file <cursor-line> <current-file>

                Note that this only works for commands that are executed when
                sourcing the file, not for a function defined in that file.

:breaka[dd] expr {expression}

                Sets a breakpoint, that will break whenever the {expression}
                evaluates to a different value.  Example:

                        :breakadd expr g:lnum

                Will break, whenever the global variable lnum changes.
                Note  if  you  watch  a script-variable  this  will  break  when
                switching scripts,  since the script  variable is only  valid in
                the  script where  it has  been defined  and if  that script  is
                called from several other scripts,  this will stop whenever that
                particular variable will become visible or unaccessible again.

The [lnum] is the line number of the breakpoint.
Vim will stop at or after this line.
When omitted line 1 is used.

# DELETING BREAKPOINTS

:breakd[el] {nr}

                Delete breakpoint {nr}.
                Use `:breaklist` to see the number of each breakpoint.

:breakd[el] *

                Delete all breakpoints.

:breakd[el] func [lnum] {name}

                Delete a breakpoint in a function.

:breakd[el] file [lnum] {name}

                Delete a breakpoint in a sourced file.

:breakd[el] here

                Delete a breakpoint at the current line of the current file.

When [lnum] is omitted, the first breakpoint in the function or file is deleted.
The  {name} must  be exactly  the same  as what  was typed  for the  `:breakadd`
command:

    - explorer
    - *explorer.vim
    - *explorer*

... are different.

Because of  this, if you source  a file you want  to debug with `:ru`,  you must
pass an absolute path to `:breakadd`:

    " ✘
    :breakadd plugin/search.vim
    :ru plugin/search.vim

    " ✘
    :breakadd */plugin/search.vim
    :ru plugin/search.vim

    " ✔
    :breakadd ~/.vim/pack/mine/opt/search/plugin/search.vim
    :ru plugin/search.vim

Probably because `:ru`  expands the argument it receives into  an absolute path,
once it finds a matching file in the rtp.

# :debug-name
## automatic anchors

Vim will automatically adds the anchor `^` and `$` around the pattern.
So, there must be a full match.

## 'ic' is not used

`'ignorecase'` is not used, but `\c` can be used in the pattern to ignore case.
Don't include the () for the function name!

## match against full file name

The match for sourced scripts is done against the full file name.
If no path is specified the current directory is used.

## functions

Note that functions are first loaded and later executed.
When they are:

   - loaded,   the 'file' breakpoints are checked
   - executed, the 'func' breakpoints are checked

## Examples

This matches 'explorer.vim' in the current directory:

    breakadd file explorer.vim

---

This matches '.../plugin/explorer.vim', '.../plugin/iexplorer.vim', etc. :

    breakadd file *explorer.vim

---

This  matches   '.../plugin/explorer.vim'  and   'explorer.vim'  in   any  other
directory:

    breakadd file */explorer.vim



The match for functions is done against the  name as it's shown in the output of
`:function`.
For local functions this means that something like `'<SNR>99_'` is prepended.

## How to profile the scripts whose path match `*/autoload/search.vim`, including all functions?

    :prof! file */autoload/search.vim
         │
         └ include all functions

## How to profile the functions whose name begin with `Func`?

    :prof func Func*

## How to profile the functions whose name begin with `Func` and finish with any character different than `a` or `b`?

    :prof func Func[^ab]

## How to profile the functions whose name begin with `Func` and finish with 2 to 5 characters?

    :prof func Func?\\\{2,5\}

# DEBUG MODE

Once in debugging mode, the usual Ex commands can be used.
For example, to inspect the value of a variable:

    echo idx

When inside  a user function,  this will print the  value of the  local variable
`idx`.
Prepend `g:` to get the value of a global variable:

    echo g:idx

All commands are executed in the context of the current function or script.
You can also  set options, for example setting or  resetting 'verbose' will show
what happens, but you  might want to set it just before  executing the lines you
are interested in:

    :set verbose=20

Commands  that require  updating the  screen  should be  avoided, because  their
effect won't be noticed until after leaving debug mode.
For example:

    :help

won't be very helpful.

There is a separate command-line history for debug mode.

The line number for a function line is relative to the start of the function.
If you have trouble  figuring out where you are, edit the  file that defines the
function in another Vim, search for the start of the function and do `99j`.
Replace `99` with the line number.

Additionally, these commands can be used:

    cont            Continue execution until the next breakpoint is hit.

    quit            Abort execution.
                    This is  like using CTRL-C,  some things might  still be
                    executed, doesn't abort everything.
                    Still stops at the next breakpoint.

    next            Execute the  command and  come back  to debug  mode when
                    it's finished.
                    This steps over user function calls and sourced files.

    step            Execute the command and come  back to debug mode for the
                    next command.
                    This steps into called user functions and sourced files.

    interrupt       This is like using CTRL-C, but unlike `>quit` comes back
                    to debug mode for the next command that is executed.
                    Useful for testing `:finally`  and `:catch` on interrupt
                    exceptions.

    finish          Finish the current script or user function and come back
                    to debug mode for the command after the one that sourced
                    or called it.

    backtrace       Show the call stacktrace for current debugging session.
    bt
    where

    frame N         Goes to N backtrace level. + and - signs make movement
                    relative.  E.g., `:frame +3` goes three frames up.

    up              Goes one level up from call stacktrace.

    down            Goes one level down from call stacktrace.

About the additional commands in debug mode:

- There is no command-line completion for them, you get the completion for the
  normal Ex commands only.

- You can shorten them, up to a single character, unless more than one command
  starts with the same letter.
  `f` stands for `finish`, use `fr` for `frame`.

- Hitting <CR> will repeat the previous one.
  When doing  another command, this  is reset (because  it's not clear  what you
  want to repeat).

- When you want to use the Ex command with the same name, prepend a colon:
  `:cont`, `:next`, `:finish` (or shorter).

The backtrace shows the hierarchy of function calls, e.g.:

    >bt
      3 function One[3]
      2 Two[3]
    ->1 Three[3]
      0 Four
    line 1: let four = 4

The `->` points to the current frame.
Use `up`, `down` and `frame N` to select another frame.

In the current frame you can evaluate the local function variables.
There is no way to see the command at the current line yet.

# debug mode

    :debug so my_script
    :debug call Func()

            Source un script / Exécute une fonction en mode déboguage.


                                               NOTE:

            Il  peut  être  judicieux  de maximiser  la  verbosité  juste  avant
            l'exécution d'une étape problématique.
            Puis de ramener la verbosité à un niveau raisonnable.


                                               NOTE:

            L'expression anglaise  “to step through a  function/script“ vient du
            fait que le mode déboguage permet d'avancer étape (step) par étape.


                                               NOTE:

            Le mode  de déboguage permet  d'arrêter l'exécution du code  au sein
            d'un  script ou  d'une  fonction,  à chaque  point  d'arrêt créé  au
            préalable via `:breakadd`.

            Dès lors,  on peut inspecter l'environnement  du script/fonction via
            les commandes Ex habituelles:

                    :echo   myvar
                    valeur de la variable `myvar` locale à la fonction˜

                    :echo g:myvar
                    valeur de la variable globale `myvar`˜

            Les commandes  sont exécutées dans le  contexte de la fonction  / du
            script.


                                               NOTE:

            L'écran n'est plus redessiné.
            Il  ne sert  donc à  rien d'exécuter  des commandes  nécessitant que
            l'écran soit mis à jour:

                    :help

            ... car  on ne verra  pas leur effet tant  qu'on n'aura pas  quitté le
            mode déboguage.


                                               NOTE:

            `:debug` nous fait passer en  mode déboguage le temps d'exécuter une
            commande.
            Ça implique  que nos  mappings custom en  ligne de  commande peuvent
            interférer: ceux dont le rhs appelle une fonction custom.

                    nno cd <cmd>call Func()<cr>
                    fu Func()
                    endfu

                    debug call Func()    ✘ possibilité d'interférence avec mappings custom
                    Debug call Func()    ✔ `:Debug` tente de désactiver temporairement nos mappings custom


                    nno cd <cmd>call Func()<cr>
                    fu Func()
                        let var1 = 'foo'
                        Breakadd here
                    endfu

                    norm! cd
                    norm! cd               ✔ qd on entre en mode déboguage via un breakpoint placé
                                           dans une fonction, seule cette dernière est déboguée;
                                           pas les fonctions utilisées dans nos mappings custom


                                               NOTE:

                    line 3: so /tmp/vim.vim

            Il s'agit d'un message typique dans une session de déboguage.
            Il indique que Vim vient

            The line number for a function line  is relative to the start of the
            function.
            If you have  trouble figuring out where you are,  edit the file that
            defines the  function in another  Vim, search  for the start  of the
            function and do `99j`.
            Replace `99` with the line number.


    $ vim -D file
    : next
      C-m

            Lance Vim  en le faisant entrer  en mode déboguage dès  qu'il source
            son 1er fichier de conf.
            Permet de  déboguer un pb  se produisant pendant le  démarrage d'une
            session Vim.

            En mode déboguage, on peut exécuter n'importe quelle commande Ex.
            On a également accès à qques commandes additionnelles:

                    ┌───────────┬───────────────────────────────────────────────────────┐
                    │ cont      │ Continue execution until the next breakpoint is hit.  │
                    ├───────────┼───────────────────────────────────────────────────────┤
                    │ quit      │ Abort execution.  This is like using CTRL-C, some     │
                    │           │ things might still be executed, doesn't abort         │
                    │           │ everything.  Still stops at the next breakpoint.      │
                    ├───────────┼───────────────────────────────────────────────────────┤
                    │ next      │ Execute the command and come back to debug mode when  │
                    │           │ it's finished.  This steps OVER user function calls   │
                    │           │ and sourced files.                                    │
                    ├───────────┼───────────────────────────────────────────────────────┤
                    │ step      │ Execute the command and come back to debug mode for   │
                    │           │ the next command.  This steps INTO called user        │
                    │           │ functions and sourced files.                          │
                    ├───────────┼───────────────────────────────────────────────────────┤
                    │ interrupt │ This is like using CTRL-C, but unlike `>quit` comes   │
                    │           │ back to debug mode for the next command that is       │
                    │           │ executed.  Useful for testing `:finally` and `:catch` │
                    │           │ on interrupt exceptions.                              │
                    ├───────────┼───────────────────────────────────────────────────────┤
                    │ finish    │ Finish the current script or user function and come   │
                    │           │ back to debug mode for the command after the one that │
                    │           │ sourced or called it.                                 │
                    └───────────┴───────────────────────────────────────────────────────┘

                    ┌───────────┬─────────────────────────────────────────────────────────┐
                    │ bt        │ Show the call stacktrace for current debugging session. │
                    │ backtrace │                                                         │
                    │ where     │                                                         │
                    ├───────────┼─────────────────────────────────────────────────────────┤
                    │ frame N   │ Goes to N backtrace level. + and - signs make movement  │
                    │           │ relative.  E.g., `:frame +3` goes three frames up.      │
                    ├───────────┼─────────────────────────────────────────────────────────┤
                    │ up        │ Goes one level up from call stacktrace.                 │
                    ├───────────┼─────────────────────────────────────────────────────────┤
                    │ down      │ Goes one level down from call stacktrace.               │
                    └───────────┴─────────────────────────────────────────────────────────┘

            Dans l'aide  de Vim, ces commandes  sont préfixées par `>`  pour les
            distinguer  des  commandes  Ex,  qui  elles  sont  accessibles  même
            en-dehors du mode déboguage.


        About the additional commands in debug mode:

                - There is no command-line completion for them, you get the completion for the
                  normal Ex commands only.

                - You can shorten them, up to a single character, unless more than one command
                  starts with the same letter.  `f` stands for `finish`, use `fr` for `frame`.

                - Hitting <CR> will repeat the previous one.  When doing another command, this
                  is reset (because it's not clear what you want to repeat).

                - When you want to use the Ex command with the same name, prepend a colon:
                  `:cont`, `:next`, `:finish` (or shorter).

        The backtrace shows the hierarchy of function calls, e.g.:

                >bt
                  3 function One[3]
                  2 Two[3]
                ->1 Three[3]
                  0 Four
                line 1: let four = 4

        The `->` points to the current frame.
        Use `up`, `down` and `frame N` to select another frame.

        In the current frame you can evaluate the local function variables.
        There is no way to see the command at the current line yet.

