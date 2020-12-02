# Try conditional structure
## What are the three circumstances in which Vim throws an exception?

   - when an error occurs
   - when we interrupt the processing of a function
   - when we execute `:throw`

## What are the three components into which you can break a try conditional?

                    ┌ try         ┐
                    │ cmd1        │ try block
                    │ cmd2        ┘
                    │ catch /pat/ ┐
    try conditional │     cmd3    │ catch clause
                    │     cmd4    ┘
                    │ finally     ┐
                    │     cmd5    │ finally clause
                    │     cmd6    ┘
                    └ endtry

## What's the main difference between a catch clause and a finally clause?

A finally is executed unconditionally.
A catch is  executed on the condition  its error message matches the  one of the
exception.

## Does a catch clause require a finally clause?  And reciprocally?

No and no.

You can use a catch clause without a finally clause, and reciprocally.

## If an exception matches the pattern of several catch clauses, which one(s) is/are executed?

Only the first one.

Which is why their order matters.
You should write the most specific ones at the top, and the most generic ones at
the bottom.

As a consequence, the order of these clauses is wrong:

    catch /.*/
        echom 'string thrown'
    catch /^\d\+$/
        echom 'number thrown'

Because the second clause will never be taken, since the pattern of the previous
one will always match the exception, no matter what it contains.

#
# Life of an exception
## How to suppress the conversion of an error to an exception?

Prefix the command responsible for the error with `:sil!`.

It works whether the error occurs inside or outside a try conditional.

## What happens when an exception is thrown inside a try block?

The execution skips the remaining commands of the block.
It immediately jumps to:

   - the catch clause matching the error message, if there's such a clause
   - the finally clause otherwise

## What happens when an exception is thrown inside a catch clause? (to the execution and to the exception)

There can only be one exception per try conditional.
So, the original exception is discarded in favor of the most recent one.

Also, the execution immediately jumps to the finally clause.
No other catch clause is taken.

## What happens when an exception is thrown inside a finally clause?

The remaining statements in the clause are skipped.

If the clause has  been taken because of an exception from the  try block or one
of the catch clauses, the original  (pending) exception is discarded in favor of
the new one which is propagated and can be caught in an outer try conditional.

## What happens to an exception, uncaught, when the execution reaches a finally clause?   After?

It's made pending:

    ...
    finally
        echom empty(v:exception)
        1~

It is resumed at the `:endtry`, so that the following commands are not executed.

##
# :break  :continue  :finish  :return    (BCFR)
## What do these four commands have in common?

They make the execution jump to a different location in the code.

## When is a BCFR discarded?

When an error occurs in the finally clause.

Probably to allow us to handle the error.

    try
        while 1
            try
                finish
            finally
                abcd
            endtry
        endwhile
    catch
        echom ':finish has been discarded'
    endtry

## When is an exception discarded?

When a new exception occurs in a catch/finally clause (it replaces the old one).

---

When a BCFR is encountered in the finally clause.

## When are the commands following `:endtry` discarded?

If an  exception was  thrown in  the catch/finally clause,  or if  the exception
thrown from the try block was uncaught.

## When is a statement from a finally clause NOT executed?

If an error occurs  during the processing of a statement in  the clause, all the
subsequent ones are skipped, because the execution jump to `:endtry`.

---

If the clause includes a BCFR, the commands after the latter are skipped.

## What happens when a BCFR is encountered in a try block or catch clause?

   1. the execution jumps to the finally clause
   2. BCFR is made pending


If no exception is thrown in the finally clause:

   3. the clause is processed up to `:endtry`
   4. BCFR resumes

If an exception IS thrown in the finally clause:

   3. the execution jumps to `:endtry`

   4. BCFR is discarded, as well as a possible pending exception
      – in case BCFR was encountered in a catch clause

## What happens when a BCFR is encountered in a finally clause? (execution/possible exception/previous BCFR)

The rest of the clause is skipped, and BCFR is executed as usual.

If the finally clause has been taken  because of an exception or an earlier BCFR
from the  try block  or a  catch clause,  this pending  exception or  command is
discarded.

---

    while 1
        try
        finally
            break
            echom 'this statement is skipped 1'
        endtry
    endwhile

---

    try
        try
            abcd
        finally
            finish
            echom 'this statement is skipped 2'
        endtry
    catch
        echom 'this statement is skipped 3'
        " because the exception of the inner try has been discarded
    endtry

---

    fu Func()
        try
        finally
            return
            echom 'this statement is skipped 4'
        endtry
    endfu
    call Func()

## In which of the following snippets is the finally clause executed?

↣
In all of them.  The finally clause is ALWAYS executed.
Even when the try  block or a catch clause includes a  statement which makes the
execution jump like:

   - break
   - continue
   - finish
   - return

↢

---

BCFR in try block:

    while 1
        try
            let answer = input('?')
            if answer == ''
                break
            endif
        finally
            echom 'finally clause 1'
        endtry
    endwhile



    fu Func()
        try
            let answer = input('?')
            if answer == ''
                return
            endif
        finally
            echom 'finally clause 3'
        endtry
    endfu
    call Func()

---

BCFR in catch clause:

    while get(s:, 'cnt', 0) < 1
        let s:cnt = get(s:, 'cnt', 0) + 1
        try
            abcd
        catch /abcd/
            let answer = input('?')
            if answer == ''
                continue
            endif
        finally
            echom 'finally clause 2'
        endtry
    endwhile
    unlet! s:cnt



    try
        abcd
    catch /abcd/
        let answer = input('?')
        if answer == ''
            finish
        endif
    finally
        echom 'finally clause 4'
    endtry

#
# Nesting
## Is an exception propagated to the outer try if the inner one is inside a function, called in the outer try block?

Yes.

For a  nesting of try  conditionals to succeed, it  does not matter  whether the
inner try  conditional is directly contained  in the outer one,  or whether it's
sourced from a script or called by a function.

    try
        call Func()
    catch
        echom 'catch: the inner exception has been propagated'
    finally
        echom 'finally: the inner exception has been propagated'
    endtry
    "
    "
    fu Func() abort
        try
            abcd
        catch /efgh/
            echom 'the exception won''t be caught by this catch clause'
        finally
            echom 'inner finally'
        endtry
    endfu

## What to do if I suspect an error may be uncaught, or an exception may be thrown from a catch/finally clause?

Wrap your try conditional inside a second outer try.

After the  execution leaves the inner  try, the exception will  be propagated to
the outer try.

## Which statements will be executed in the following snippets?

In the answers, the following symbols are used:

    ┌───┬─────────────────────────┐
    │ ✘ │ an error occurs         │
    ├───┼─────────────────────────┤
    │ ✔ │ the command is executed │
    ├───┼─────────────────────────┤
    │ ∅ │ the command is skipped  │
    └───┴─────────────────────────┘


Source the code to get a confirmation for each answer.


    try
        try
            abcd                         |"  ↣ ✘  E492 ↢
        catch
            echom 'inner catch'          |"  ↣ ✔  the exception is caught ↢
        finally
            echom 'inner finally'        |"  ↣ ✔  the exception is finished (it has been caught already) ↢
        endtry
        echom 'outer block'              |"  ↣ ✔ ↢
    catch
↣       " ∅ not executed: the exception is finished:
↢       "                 there's nothing to catch anymore
        echom 'outer catch'
    finally
        echom 'outer finally'            |"  ↣ ✔  a finally clause is always executed ↢
    endtry

---

    try
        try
            abcd
            echom 'still in block'       |"  ↣ ∅  the execution looks for a catch or finally clause ↢
        catch /efgh/
            echom 'inner catch'          |"  ↣ ∅  /efgh/ doesn't match the error message ↢
        finally
            echom 'inner finally'        |"  ↣ ✔ ↢
        endtry
↣       " ∅  the exception hasn't been caught so far,
↢       "    and thus, resumes in the outer try conditional
        echom 'outer block'
    catch
↣       "  ✔  the exception is caught: you can access it via `v:exception`;
        "     it's the first time since the beginning that `v:exception`
↢       "     is not empty
        echom 'outer catch'
    finally
        echom 'outer finally'            |"  ↣ ✔ ↢
    endtry

---

    try
        try
            abcd
        catch /E492/
            unlet novar                 |"  ↣ ✘  E108: a new exception is thrown; it replaces the previous one ↢
            echom 'inner catch'         |"  ↣ ∅  the execution has jumped to the finally clause ↢
        catch /E108/                    |"  ↣ ∅  same reason as before ↢
            echom 'inner catch'         |"
        finally
            echom 'finally'             |"  ↣ ✔ ↢
        endtry
        echom 'outer block'             |"  ↣ ∅  the exception resumes ↢
    catch
        echom 'outer catch'             |"  ↣ ✔  the exception is caught ↢
    endtry

#
# Issues
## How to debug a try conditional?

Increase the verbosity level to 13 or 14:

    :14verb so myscript.vim
or
    :set verbose=14 | so myscript.vim | set verbose=0

With 13, you'll see when an exception is thrown, discarded, caught, or finished.
With 14, you'll also see when an exception/command is made pending and resumed.

## Is a finally clause executed when I press C-c, while the try block is executed?

Yes.

## Why should I always use a try conditional to restore temporarily changed settings in a finally clause?

If you press C-c to interrupt a script while some settings have been temporarily
changed, the latter will remain in an inconsistent state.

A finally clause lets you make sure they're restored no matter what happens:

   - normal control flow
   - error
   - an explicit ':throw'
   - interrupt

## Why should I be careful when catching all exceptions with `:catch /.*/`?

It may hide from you the presence of an unknown bug which should be fixed:

    augroup my_bufwritepre
        au!
        au BufWritePre * unlet novar
    augroup END
    "
    try
        write
    " ✘
    catch
        " don't  remove this  line, otherwise  you'll have  undesired errors
        " after sourcing the code to test it
        au! my_bufwritepre
    endtry

Here, the  catch clause will  catch the error  `E108` caused by  `:unlet novar`,
triggered by the autocmd.
But this isn't  an error due to  `:write`.  You probably want to  be informed of
`E108` to fix the autocmd.

So prefer this:

    augroup my_bufwritepre
        au!
        au BufWritePre * unlet novar
    augroup END
    "
    try
        write
    " ✔
    catch /^Vim(write):/
    " ✔
    catch /^Vim(unlet):/
        au! my_bufwritepre
    endtry

Bottom line: catch only what you'd like to ignore INTENTIONALLY.

---

It may make a known bug more difficult  to be fixed, because no error message is
displayed.

---

It may prevent you from terminating a script:

    while 1
        try
            " sleep 1
        catch
        endtry
    endwhile

Right now, `:sleep` is commented, so you CAN terminate the script by pressing C-c.
If you do so, the interrupt will be converted into an exception which will make
Vim terminate the script at the end of the try conditional.

If  you uncomment  the  `:sleep` and  source  the  code, you  won't  be able  to
terminate the script, even by pressing C-c, because the interrupt will always be
converted into an exception which will be caught, but not acted upon.

## On which condition is it ok to use `:catch /.*/`?

You should echo  the exception (`v:exception`), and maybe the  location where it
was thrown (`v:throwpoint`):

    try
        " something which may fail
    catch
        echom 'Caught: '.v:exception.' from '.v:throwpoint
    endtry

Or, use a library function, like `lg#catch_error()`, to do something similar:

    try
        " something which may fail
    catch
        return lg#catch_error()
    endtry

## Can I catch an interrupt?   If so, in which exception is it converted into?

Yes, you can.

It will be converted into the exception 'Vim:Interrupt'.

## If I press C-c while Vim executes a try conditional which catches interrupts, is the running script terminated?

No.

#
#
# Catching interrupts

Example:

    fu TASK1()
        sleep 10
    endfu
    "
    fu TASK2()
        sleep 20
    endfu
    "
    while 1
        let cmd = input('Type a command: ')
        try
            if empty(cmd)
                continue
            elseif cmd is# 'END'
                break
            elseif cmd is# 'TASK1'
                call TASK1()
            elseif cmd is# 'TASK2'
                call TASK2()
            else
                echom "\nIllegal command: ".cmd
                continue
            endif
        catch /^Vim:Interrupt$/
            echom "\nCommand interrupted"
            " Caught the interrupt.  Continue with next prompt.
        endtry
    endwhile

You can interrupt  a task here by pressing  C-c; the script then asks  for a new
command.
If you press C-c at the prompt, the script is terminated.

For testing what  happens when C-c would  be pressed on a specific  line in your
script, use  the debug mode and  execute the |>quit| or  |>interrupt| command on
that line.  See |debug-scripts|.

# Cleanup code

Example:

    let first = 1
    while 1
        try
            if first
                echom 'first'
                let first = 0
                continue
            else
                throw 'second'
            endif
        catch
            echom v:exception
            break
        finally
            echom 'cleanup'
        endtry
        echom 'still in while'
    endwhile
    echom 'end'

This displays 'first', 'cleanup', 'second', 'cleanup', and 'end'.

    fu Func()
        try
            return 123
        finally
            echom "cleanup\n"
        endtry
        echom 'Func still active'
    endfu
    "
    echom Func().' returned by Func'

This displays 'cleanup' and '123 returned by Func'.
You don't need to add an extra 'return' in the finally clause.
Above all, this would override the return value.


Using  either  BCFR  or `:throw`  in  a  finally  clause  is possible,  but  not
recommended since it abandons the cleanup actions for the try conditional.
But, of course,  interrupt and error exceptions might get  raised from a finally
clause.
Example where  an error in  the finally clause  stops an interrupt  from working
correctly:

    try
        try
            echom 'press C-c for interrupt'
            while 1
            endwhile
        finally
            unlet novar
        endtry
    catch /novar/
    endtry
    echom 'script still running'
    sleep 1
    throw 'hello'

If you need  to put commands that  could fail into a finally  clause, you should
think  about catching  or ignoring  the errors  in these  commands, see“catching
errors” and “ignoring errors”.

# Exception hierarchies and parameterized exceptions

Some programming languages  allow to use hierarchies of exception  classes or to
pass additional information  with the object of an exception  class.  You can do
similar things in Vim.

In order to throw  an exception from a hierarchy, just  throw the complete class
name with  the components separated  by a colon,  for instance throw  the string
'EXCEPT:MATHERR:OVERFLOW' for an overflow in a mathematical library.

When you want  to pass additional information with your  exception class, add it
in parentheses,  for instance throw the  string 'EXCEPT:IO:WRITEERR(myfile)' for
an error when writing 'myfile'.

With the  appropriate patterns in  `:catch`, you can  catch for base  classes or
derived classes of your hierarchy.
Additional information  in parentheses  can be cut  out from  `v:exception` with
`substitute()`.

Example:

    fu CheckRange(a, func)
        if a:a < 0
            throw 'EXCEPT:MATHERR:RANGE('.a:func.')'
        endif
    endfu
    "
    fu Add(a, b)
        call CheckRange(a:a, 'Add')
        call CheckRange(a:b, 'Add')
        let c = a:a + a:b
        if c < 0
            throw 'EXCEPT:MATHERR:OVERFLOW'
        endif
        return c
    endfu
    "
    fu Div(a, b)
        call CheckRange(a:a, 'Div')
        call CheckRange(a:b, 'Div')
        if a:b == 0
            throw 'EXCEPT:MATHERR:ZERODIV'
        endif
        return a:a / a:b
    endfu
    "
    fu Write(file)
        try
            exe 'write '.fnameescape(a:file)
        catch /^Vim(write):/
            throw printf('EXCEPT:IO(%s, %s):WRITEERR', getcwd(), a:file)
        endtry
    endfu
    "
    try
    "
        " something with arithmetics and I/O
    "
    catch /^EXCEPT:MATHERR:RANGE/
        let function = substitute(v:exception, '.*(\(\a\+\)).*', '\1', '')
        echom 'Range error in '.function
    "
    catch /^EXCEPT:MATHERR/    " catches OVERFLOW and ZERODIV
        echom 'Math error'
    "
    catch /^EXCEPT:IO/
        let dir = substitute(v:exception, '.*(\(.\+\),\s*.\+).*', '\1', '')
        let file = substitute(v:exception, '.*(.\+,\s*\(.\+\)).*', '\1', '')
        if file !~ '^/'
            let file = dir.'/'.file
        endif
        echom 'I/O error for '.string(file)
    "
    catch /^EXCEPT/
        echom 'Unspecified error'
    endtry

The exceptions  raised by Vim  itself (on error or  when pressing CTRL-C)  use a
flat hierarchy: they are all in the 'Vim' class.
You cannot  throw yourself exceptions with  the 'Vim' prefix; they  are reserved
for Vim.

Vim error exceptions are parameterized with the name of the command that failed,
if known.

# Catching errors

If you  want to  catch specific  errors, you  just have  to put  the code  to be
watched in a try block and add a catch clause for the error message.
The presence  of the  try conditional causes  all errors to  be converted  to an
exception.
No message is displayed and |v:errmsg| is not set then.
To find  the right pattern for  the ":catch" command,  you have to know  how the
format of the error exception is.

Error exceptions have the following format:

    Vim({cmdname}):{errmsg}
or
    Vim:{errmsg}

{cmdname} is the name  of the command that failed; the second  form is used when
the command name is not known.
{errmsg} is the error message usually produced when the error occurs outside try
conditionals.
It always  begins with  a capital 'E',  followed by a  two or  three-digit error
number, a colon, and a space.

Examples:

The command

    :unlet novar

Normally produces the error message

    E108: no such variable: "novar"

Which is converted inside try conditionals to an exception

    Vim(unlet):E108: no such variable: "novar"

The command

    :abcd

Normally produces the error message

    E492: not an editor command: abcd

Which is converted inside try conditionals to an exception

    Vim:E492: not an editor command: abcd

You can catch all ':unlet' errors by a

    :catch /^Vim(unlet):/

Or all errors for misspelled command names by a

    :catch /^Vim:E492:/

Some error messages may be produced by different commands:

    :function nofunc

And

    :delfunction nofunc

Both produce the error message

    E128: function name must start with a capital: nofunc

Which is converted inside try conditionals to an exception

    Vim(function):E128: function name must start with a capital: nofunc

Or:

    Vim(delfunction):E128: function name must start with a capital: nofunc

Respectively.  You can catch the error by its number independently on the
command that caused it if you use the following pattern:

    :catch /^Vim(\a\+):E128:/

Some commands like:

    :let x = novar

Produce multiple error messages, here:

    E121: undefined variable: novar
    E15: invalid expression:  novar

Only the first is used for the exception value, since it is the most specific
one (see |except-several-errors|).  So you can catch it by:

    :catch /^Vim(\a\+):E121:/

You can catch all errors related to the name 'nofunc' by:

    :catch /\<nofunc\>/

You can catch all Vim errors in the ':write' and ':read' commands by:

    :catch /^Vim(\(write\|read\)):e\d\+:/

You can catch all Vim errors by the pattern:

    :catch /^Vim\((\a\+)\)\=:e\d\+:/

Note that you should never catch the error message text itself:

    :catch /no such variable/

Only works in the english locale, but not when the user has selected a different
language by the |:language| command.
It is however helpful to cite the message text in a comment:

    :catch /^Vim(\a\+):E108:/   " no such variable

# Peculiarities

The exception handling concept requires that the command sequence causing the
exception is aborted immediately and control is transferred to finally clauses
and/or a catch clause.

In the Vim script language there  are cases where scripts and functions continue
after an  error: in  functions without the  'abort' flag or  in a  command after
`:sil!`, control flow goes to the following line; and outside functions, control
flow goes to the line following the outermost 'endwhile' or 'endif'.
On the other hand, errors should be catchable as exceptions (thus, requiring the
immediate abortion).

This  problem has  been  solved by  converting errors  to  exceptions and  using
immediate abortion (if not suppressed by  'silent!') only when a try conditional
is active.
This is  no restriction since  an (error) exception can  be caught only  from an
active try conditional.
If you want an immediate termination without  catching the error, just use a try
conditional without catch clause.
You can  cause cleanup code  being executed  before termination by  specifying a
finally clause.

When no try conditional is active,  the usual abortion and continuation behavior
is used instead of immediate abortion.
This ensures compatibility of scripts written for Vim 6.1 and earlier.

However, when sourcing  an existing script that does not  use exception handling
commands  (or when  calling one  of  its functions)  from inside  an active  try
conditional of a new  script, you might change the control  flow of the existing
script on error.
You get  the immediate  abortion on  error and can  catch the  error in  the new
script.
If however the sourced script suppresses  error messages by using the ":silent!"
command  (checking  for  errors  by  testing  |v:errmsg|  if  appropriate),  its
execution path is not changed.
The error is not converted to an exception.
(See |:silent|.)  So the only remaining  cause where this happens is for scripts
that don't care about errors and produce error messages.
You probably won't want to use such code from your new scripts.


Syntax errors in the exception handling commands  are never caught by any of the
':catch' commands of the try conditional they belong to.
Its finally clauses, however, is executed.

Example:

    try
        try
            throw 123
        catch /\(/
            echom 'in catch with syntax error'
        catch
            echom 'inner catch-all'
        finally
            echom 'inner finally'
        endtry
    catch
        echom 'outer catch-all caught '.string(v:exception)
    finally
        echom 'outer finally'
    endtry
    inner finally~
    outer catch-all caught 'Vim(catch):E54: Unmatched \('~
    outer finally~

The original exception is discarded and an error exception is raised, instead.


The `:try`, `:catch`, `:finally`, and `:endtry`  commands can be put on a single
line, but  then syntax errors  may make it  difficult to recognize  the `:catch`
line, thus you better avoid this.

Example:

    try | unlet! foo # | catch | endtry

raises an error exception for the trailing characters after the ':unlet!'
argument, but does not see the ':catch' and ':endtry' commands, so that the
error exception is discarded and the 'E488: Trailing characters' message gets
displayed.

---

When  several errors  appear in  a single  command, the  first error  message is
usually the most specific one and therefore converted to the error exception.
Example:

    echo novar

Causes:

    E121: Undefined variable: novar
    E15: Invalid expression: novar

The value of the error exception inside try conditionals is:

    Vim(echo):E121: Undefined variable: novar


But when a syntax error is detected after a normal error in the same command,
the syntax error is used for the exception being thrown.
   Example:

    unlet novar #

Causes:

    E108: No such variable: "novar"
    E488: Trailing characters

The value of the error exception inside try conditionals is:

    Vim(unlet):E488: Trailing characters

This is done because the syntax error might change the execution path in a way
not intended by the user.  Example:

    try
        try | unlet novar # | catch | echom v:exception | endtry
    catch /.*/
        echom "outer catch:" v:exception
    endtry

This displays 'outer catch: Vim(unlet):E488: Trailing characters', and then
a 'E600: Missing :endtry' error message is given, see |except-single-line|.

# Exceptions and autocommands

Exceptions may be used during execution of autocommands.  Example:

    augroup test
        au!
        au User x try
        au User x   throw 'Oops!'
        au User x catch
        au User x   echom v:exception
        au User x endtry
        au User x throw 'Arrgh!'
        au User x echom 'Should not be displayed'
    augroup END
    "
    try
        do User x
    catch
        echom v:exception
    endtry

This displays 'Oops!' and 'Arrgh!'.

---

For  some commands,  autocommands get  executed before  the main  action of  the
command takes place.
If an exception  is thrown and not  caught in the sequence  of autocommands, the
sequence  and the  command  that  caused its  execution  are  abandoned and  the
exception is propagated to the caller of the command.

Example:

    au BufWritePre * throw 'FAIL'
    au BufWritePre * echom 'Should not be displayed'

    try
        write
    catch
        echom 'Caught: '.v:exception.' from '.v:throwpoint
    endtry

Here, `:write` does not write the file currently being edited (as you can see by
checking  'modified'),  since the  exception  from  the BufWritePre  autocommand
abandons the `:write`.
The exception is then caught and the script displays:

    Caught: FAIL from BufWrite Autocommands for "*"

---

For  some commands,  autocommands  get executed  after the  main  action of  the
command has taken place.
If this main action  fails and the command is inside  an active try conditional,
the autocommands are skipped and an error exception is thrown that can be caught
by the caller of the command.

Example:

    au BufWritePost * echom 'File successfully written!'

    try
        write /i/m/p/o/s/s/i/b/l/e
    catch
        echom v:exception
    endtry

This just displays:

    Vim(write):E212: Can't open file for writing (/i/m/p/o/s/s/i/b/l/e)

If you really need to execute the autocommands even when the main action
fails, trigger the event from the catch clause.

Example:

    au BufWritePre  * set noreadonly
    au BufWritePost * set readonly

    try
        write /i/m/p/o/s/s/i/b/l/e
    catch
        do BufWritePost /i/m/p/o/s/s/i/b/l/e
    endtry

You can also use `:sil!`:

    let x = 'ok'
    let v:errmsg = ''
    au BufWritePost * if !empty(v:errmsg)
    au BufWritePost *     let x = 'after fail'
    au BufWritePost * endif
    try
        sil! write /i/m/p/o/s/s/i/b/l/e
    catch
    endtry
    echom x

This displays 'after fail'.

If the main action of the command does not fail, exceptions from the
autocommands will be catchable by the caller of the command:

    au BufWritePost * throw ':-('
    au BufWritePost * echom 'Should not be displayed'

    try
        write
    catch
        echom v:exception
    endtry

---

For  some  commands,  the  normal  action  can be  replaced  by  a  sequence  of
autocommands.
Exceptions from that sequence will be catchable by the caller of the command.

Example:
For `:write`, the caller cannot know  whether the file had actually been written
when the exception occurred.
You need to tell it in some way.

    if !exists('cnt')
        let cnt = 0

        au BufWriteCmd * if &modified
        au BufWriteCmd *     let cnt += 1
        au BufWriteCmd *     if cnt % 3 == 2
        au BufWriteCmd *         throw 'BufWriteCmdError'
        au BufWriteCmd *     endif
        au BufWriteCmd *     write | set nomodified
        au BufWriteCmd *     if cnt % 3 == 0
        au BufWriteCmd *         throw 'BufWriteCmdError'
        au BufWriteCmd *     endif
        au BufWriteCmd *     echom 'File successfully written!'
        au BufWriteCmd * endif
    endif

    try
        write
    catch /^BufWriteCmdError$/
        if &modified
            echom 'Error on writing (file contents not changed)'
        else
            echom 'Error after writing'
        endif
    catch /^Vim(write):/
        echom 'Error on writing'
    endtry

When this  script is  sourced several  times after  making changes,  it displays
first:

    File successfully written!

Then:

    Error on writing (file contents not changed)

Then:

    Error after writing

etc.

---

You cannot spread a try conditional over autocommands for different events.
The following code is ill-formed:

    au BufWritePre  * try

    au BufWritePost * catch
    au BufWritePost *     echom v:exception
    au BufWritePost * endtry

    write

# Throwing and catching exceptions

You can throw any number or string as an exception.
Use the `:throw` command and pass the value to be thrown as argument:

    throw 123
    throw 'string'

You can also specify an expression argument.
The expression is then evaluated first, and the result is thrown:

    throw 123 + strlen('string')
    throw strpart('strings', 0, 6)

An exception might  be thrown during evaluation of the  argument of the ':throw'
command.
Unless it is caught there, the expression evaluation is abandoned.
The ':throw' command then does not throw a new exception.

Example:

    fu Foo(arg)
        try
            throw a:arg
        catch /me/
        endtry
        return 3
    endfu
    "
    fu Bar()
        echom 'in_Bar'
        return 120
    endfu
    "
    throw Foo('you') + Bar()

`'in_Bar'` is  not displayed because  during the evaluation of  `Foo('you')`, an
exception  was thrown,  which  made  Vim abandon  the  evaluation  of the  whole
expression passed to `:throw`.

`'you'` is thrown.
Even though the `:throw` in `:throw  Foo...` has encountered an exception during
the evaluation of its argument, it hasn't thrown a new exception.

Has the command been entirely abandoned?
It seems  so.  Anyway,  we can  still catch  the original  exception with  a try
conditional try around the `:throw Foo...`.

---

This displays `in_Bar` and throws `123`:

    throw Foo('me') + Bar()

---

Any other command  that takes an expression as argument  might also be abandoned
by an (uncaught) exception during the expression evaluation.
The exception is then propagated to the caller of the command.

Example:

    if Foo('arrgh')
        echom 'then'
    else
        echom 'else'
    endif

Here neither of `'then'` or `'else'` is displayed.

---

Note  that `v:exception`  and `v:throwpoint`  are valid  for the  exception most
recently caught as long it is not finished.

Example:

    fu Caught()
        if v:exception != ''
            echom 'caught '.string(v:exception).' in '.v:throwpoint
        else
            echom 'nothing caught'
        endif
    endfu
    "
    fu Func()
        try
            try
                try
                    throw 123
                finally
                    call Caught()
                endtry
            catch /.*/
                call Caught()
                throw 'oops'
            endtry
        catch /.*/
            call Caught()
        finally
            call Caught()
        endtry
    endfu
    call Func()

This displays:

    nothing caught
    caught '123' in function Func, line 4
    caught 'oops' in function Func, line 10
    nothing caught

A practical example:  the following command `:linenumber` displays the line
number in the script or function where it has been used:

    fu Linenumber()
        return substitute(v:throwpoint, '.*\d\(\d\+\).*', '\1', '')
    endfu
    com Linenumber try | throw '' | catch | echom Linenumber() | endtry

---

You can catch an exception and throw a new one to be caught elsewhere from the
catch clause:

    fu Foo()
        throw 'foo'
    endfu
    "
    fu Bar()
        try
            call Foo()
        catch /foo/
            echom 'caught foo, throw bar'
            throw 'bar'
        endtry
    endfu
    "
    try
        call Bar()
    catch /.*/
        echom 'caught '.v:exception
    endtry

This displays 'caught foo, throw bar' and then 'caught bar'.

There is no real rethrow in the Vim script language, but you may throw
`v:exception` instead:

    fu Bar()
        try
            call Func()
        catch /.*/
            echom 'rethrow '.v:exception
            throw v:exception
        endtry
    endfu

Note  that this  method  cannot be  used  to 'rethrow'  Vim  error or  interrupt
exceptions, because it is not possible to fake Vim internal exceptions.
Trying so causes an error exception.
You should throw your own exception denoting the situation.
If  you want  to  cause a  Vim  error exception  containing  the original  error
exception value, you can use the `:echoerr` command:

    try
        try
            abcd
        catch /.*/
            echoerr v:exception
        endtry
    catch /.*/
        echom v:exception
    endtry

This code displays

    Vim(echoerr):Vim:E492: Not an editor command:   abcd

#
#
#
# Old personal notes

    let v:errmsg = ''
    sil! cmd
    if !empty(v:errmsg)
        handle error
    endif

Tente d'exécuter `cmd` en gérant une éventuelle erreur.
Illustre comment on peut utiliser `v:errmsg`.


    " save options
    " create tmp file
    try
        cmd
        r /tmp/unexisting_file

    catch /E484/
        echom 'the file you want to read doesn't exist'

    catch /E492/
        echohl ErrorMsg
        echom v:exception
        echom v:throwpoint
        echohl NONE

    finally
        " restore options
        " delete tmp file
    endtry

Tente d'exécuter `cmd` puis `r /tmp/unexisting_file`.

`cmd` n'est pas une commande valide, ce qui provoque une erreur.
Toute erreur se produisant à l'intérieur  d'un conditionnel try est convertie en
une chaîne appelée exception.

Vim écrit la plus récente exception et l'endroit où elle s'est produite dans:

   - v:exception
   - v:throwpoint

On  pourra  utiliser  ces  informations   après  `:catch`  pour  gérer  l'erreur
nous-mêmes,  et pex  l'afficher à  notre façon  en formatant  son message  ou sa
couleur ...


Change  the  error  handling  for  the commands  between  ":try"  and  ":endtry"
including everything  being executed across ":source"  commands, function calls,
or autocommand invocations.

When  an error  or  interrupt is  detected  and there  is  a `:finally`  command
following, execution continues after the ':finally'.
Otherwise, or when  the ':endtry' is reached thereafter,  the next (dynamically)
surrounding  ':try' is  checked for  a corresponding  ':finally' etc.   Then the
script processing is terminated.
Whether a function definition has an 'abort' argument does not matter.

Example:

    try | edit too much | finally | echom 'cleanup' | endtry
    echom 'impossible'  |" not reached, script terminated above

Moreover, an  error or  interrupt (dynamically) inside  ':try' and  ':endtry' is
converted to an exception.
It can be caught as if it were thrown by a `:throw` command (see `:catch`).
In this case, the script processing is not terminated.

The value 'Vim:Interrupt' is used for an interrupt exception.
An  error   in  a   Vim  command   is  converted   to  a   value  of   the  form
'Vim({command}):{errmsg}', other  errors are  converted to a  value of  the form
'Vim:{errmsg}'.
{command}  is  the full  command  name,  and {errmsg}  is  the  message that  is
displayed if the error exception is  not caught, always beginning with the error
number.

Examples:

    try | sleep 100 | catch /^Vim:Interrupt$/ | endtry
    try | edit | catch /^Vim(edit):E\d\+/ | echom 'error' | endtry


    :cat[ch] /{pat}/

The following  commands until the  next `:catch`, `:finally`, or  `:endtry` that
belongs  to the  same `:try`  as  the ":catch"  are executed  when an  exception
matching  {pat} is  being thrown  and  has not  yet  been caught  by a  previous
':catch'.
Otherwise, these commands are skipped.
When {pat} is omitted all errors are caught.

Examples:

    catch /^Vim:Interrupt$/           " catch interrupts (CTRL-C)
    catch /^Vim\%((\a\+)\)\=:E/       " catch all Vim errors
    catch /^Vim\%((\a\+)\)\=:/        " catch errors and interrupts
    catch /^Vim(write):/              " catch all errors in :write
    catch /^Vim\%((\a\+)\)\=:E123/    " catch error E123
    catch /my-exception/              " catch user exception
    catch                             " catch everything

Another character can be used instead of /  around the {pat}, so long as it does
not have a special meaning (e.g., '|' or '"') and doesn't occur inside {pat}.
Information about the exception is available in `v:exception`.
Also see `throw-variables`.
NOTE:  It is  not reliable to ':catch'  the TEXT of an error  message because it
may vary in different locales.


    finally

The following  commands until the  matching `:endtry` are executed  whenever the
part between the matching `:try` and the ':finally' is left by:

   - falling through to the ':finally'
   - continue
   - break
   - finish
   - return
   - error / interrupt / exception (:throw)

---

    try                              for i in range(1,3)
        echom 'one'                       if i == 3
        finish                               break
        echom 'two'                       endif
    finally
        echom 'three'                     try
    endtry                                   echom i
                                         finally
                                             echom 'broken'
                                         endtry
                                     endfor


    try
        throw 'oops'
    catch
        echom 'caught '.v:exception
    endtry
    'caught oops'~

Illustre l'utilisation de `v:exception`.
The value of the exception most recently caught and not finished.


    try
        throw 'oops'
    catch
        echom 'Exception from '.v:throwpoint
    endtry
    'Exception from {script}, line XXX'~

The point where the exception most recently caught and not finished was thrown.
Not set when commands are typed.
See also `v:exception` and `throw-variables`.



    throw {expr}

Jette l'évaluation de `expr` comme s'il s'agissait d'une exception.

If ':throw' is used after a  `:try` but before the first corresponding `:catch`,
commands are skipped until the first ':catch' matching {expr1} is reached.

If there  is no such ':catch'  or if the ':throw'  is used after a  ':catch' but
before the `:finally`, the commands following  the ':finally' (if present) up to
the matching `:endtry` are executed.

If  the ':throw'  is after  the  ':finally', commands  up to  the ':endtry'  are
skipped.
At  the  ':endtry',  this  process   applies  again  for  the  next  dynamically
surrounding  ':try' (which  may  be  found in  a  calling  function or  sourcing
script), until a matching ':catch' has been found.
If the exception is not caught, the command processing is terminated.


    try | throw 'oops' | catch /^oo/ | echom 'caught' | endtry

Note that 'catch' may need to be on a separate line for when an error causes the
parsing to skip the whole line and not see the '|' that separates the commands.

#
#
#
# Todo
## ?

Compare:

    echoerr v:exception

vs:

    echohl ErrorMsg
    echom v:exception.' | '.v:throwpoint
    echohl NONE

Which is best? Which should be used inside `try|catch|endtry`?

Read `:h echoerr`.

Are there other possibilities?
What's the use of `v:errmsg`?
It contains the last error message produced.  It can even capture messages which
were silent.  The last error message could have happened a long time ago, and it
could be irrelevant to what we're doing:

      v:errormsg   :  large scope
      v:exception  :  local to a try conditional (empty outside)

Look at tpope plugins, in particular vim-scriptease.

Edit:
It seems that returning 'echoerr '.string(v:exception) and executing it,
is faster than returning `v:exception` and echoerr'ing it.
Indeed, if you try to use  the 2nd technique for our mapping `<space>q` (close
window) introduces lag.
Make some tests inside our unimpaired mappings.

## ?

When  an  instruction  causes  several  errors,  and  it's  executed  in  a  try
conditional, the first error can be catched and converted into an exception with
`v:exception` (`:h except-several-errors`).
However, for some reason, I can't display its message.
All  I have  is  the hit-enter  prompt, which  usually  accompanies a  multiline
message (as if Vim was trying to display all the error messages).

MWE:

    $ touch /tmp/file && vim -Nu NONE -S <(cat <<'EOF'
    nno cd <cmd>exe Func()<cr>
    fu Func() abort
        try
            qall
        catch
            return 'echoerr ' .. string(v:exception)
        endtry
        return ''
    endfu
    EOF
    ) /tmp/file
    " press:  o Esc cd
    " result: no message is visible (except for the hit-enter prompt itself)
    " run:  :mess
    Vim(qall):E37: No write since last change~

Update: Actually, if you press `Enter` instead of `Esc` at the hit-enter prompt,
you can see the error.
But sth is  weird.  It seems the  `catch` clause is not processed  (write a
`let g:d_ebug = 1` inside, and you should see that the variable is never set).
However, if you run `:breakadd func Func`, you can see that it *is* processed.
What gives?

I wonder whether this issue is specific to `:qall`...
Can you find other similar issues which don't make Vim quit?

## ?

Is it wrong to run `:throw` without a `:catch`?

It seems it can cause unexpected results:

    $ vim -Nu NONE -S <(cat <<'EOF'
        fu Throw()
            try
                throw 'some error'
            endtry
        endfu
        sil! call Throw()
        try
            call Unknown()
        catch
        endtry
    EOF
    )
    ...~
    E117: Unknown function: Unknown~
    " result:   'E117' is raised
    " expected: 'E117' is caught

Check out where we've run `:throw` without a catch.
Whenever you find one, consider removing it or adding a `:catch`.
Check out whether tpope sometimes runs `:throw` without a `:catch`.

Also,   `E117`  is   still   raised   even  when   we   replace  `:throw`   with
`:echoerr`  or  `:not_a_cmd`.  However,  if  we  remove the  `:try`  surrounding
`:echoerr`/`:not_a_cmd`, then the  issue disappears; i.e.  `E117`  is not raised
anymore.  But it still persists in the case of `:throw`.

Is it a known bug?  From `:h todo`:

   > Problem that a previous silent ":throw" causes a following try/catch not to
   > work. (ZyX, 2013 Sep 28) With examples: (Malcolm Rowe, 2015 Dec 24)

If so, report  it on github, so that  it has a better visibility,  and the issue
can be properly referenced in the todo list.

