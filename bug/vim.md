<https://github.com/vim/vim/blob/master/runtime/doc/vim9.txt>
<https://github.com/vim/vim/blob/master/runtime/doc/todo.txt>

# bug: imported constants and variables are not added to the "s:" dictionary

    imported constant
```vim
vim9script
g:lines =<< trim END
    vim9script
    export const s:MYCONST = 123
END
writefile(g:lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import MYCONST from 'foo.vim'
echo s:MYCONST
echo s:
echo get(s:, 'MYCONST', 456)
```
    123
    ✔
    {}
    ✘
    456
    ✘

---

    imported variable
```vim
vim9script
g:lines =<< trim END
    vim9script
    export let s:var = 123
END
writefile(g:lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import var from 'foo.vim'
echo s:var
echo s:
echo get(s:, 'var', 456)
```
    123
    ✔
    {}
    ✘
    456
    ✘

# bug: function nested in a legacy function can be invoked with the "s:" prefix
```vim
vim9script
fu Outer()
    def Inner()
        echo 'inner'
    enddef
endfu
Outer()
s:Inner()
g:Inner()
```
    inner
    inner
    ✘

`s:Inner()`  should  fail,  because  `Inner()`  is  a  global  function,  not  a
script-local one.

---

It doesn't matter whether `Inner()` is a legacy function or not.
The results are the same.

# bug: imported function can be invoked with the "g:" prefix
```vim
vim9script
let lines =<< trim END
    vim9script
    export def Imported()
        echo 'imported'
    enddef
END
writefile(lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import Imported from 'foo.vim'
fu Imported
g:Imported()
```
       def <SNR>2_Imported()
    1      echo 'imported'
       enddef
    imported

`g:Imported()` should raise `E117`, because `Imported()` is script-local, not global.

# bug: can delete a function-local or block-local function nested in a legacy function

MWE for a function-local function:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        fu Outer()
            def Inner()
                echo 'inner'
            enddef
            delfu Inner
        endfu
        Outer()
    EOF
    )

Actual: No error is raised
Expected: E130 or E1084 is raised (preferably the latter):

    E130: Unknown function: Inner
    E1084: Cannot delete Vim9 script function Inner

Rationale: to be consistent with script-local functions which can't be deleted.
```vim
vim9script
fu s:Func()
endfu
delfu s:Func
```
    E1084: Cannot delete Vim9 script function s:Func
```vim
vim9script
def s:Func()
enddef
delfu s:Func
```
    E1084: Cannot delete Vim9 script function s:Func

---

MWE for a block-local function:
```vim
vim9script
fu Outer()
    if 1
        def Inner()
            echo 'inner'
        enddef
        delfu Inner
    endif
endfu
Outer()
```
    ✔

---

If this is working as intended, then the help should be updated at `:h vim9-scopes`.

From this:

>     Global functions can be still be defined and deleted at nearly any time.  In
>     Vim9 script script-local functions are defined once when the script is sourced
>     and cannot be deleted or replaced.

To this:

>     Global functions can be still be defined and deleted at nearly any time.  In
>     Vim9 script, script-local functions are defined once when the script is sourced
>     and cannot be deleted or replaced.  Similarly, a function local to a function
>     is defined when the latter is run, and cannot be deleted or replaced.
>     The same is true fo a function local to a block.

# bug: inconsistent error message when trying to delete local function nested in ":def" function

The issue also affects an imported function:
```vim
vim9script
let lines =<< trim END
    vim9script
    export def Imported()
        echo 'imported'
    enddef
END
writefile(lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import Imported from 'foo.vim'
delfu s:Imported
```
    E130: Unknown function: s:Imported

Shouldn't the error rather be:

    E1084: Cannot delete Vim9 script function s:Imported

Just like for a non-imported script-local function:
```vim
vim9script
def Func()
enddef
delfu s:Func
```
---

    function-local function
```vim
vim9script
def Outer()
    def Inner()
        echo 'inner'
    enddef
    delfu Inner
enddef
Outer()
```
    E130: Unknown function: Inner

Shouldn't the error rather be:

    E1084: Cannot delete Vim9 script function Inner

After all, the function should be known to Vim:
it should look for the function in the function scope according to `:h vim9-scopes`.

Note: the error is only raised for a `:def` inside a `:def`.
If the  outer function is  a `:fu`, no  error is raised;  no matter the  type of
inner function.

---
```vim
vim9script
def Outer()
    if 1
        def Inner()
            echo 'inner'
        enddef
        delfu Inner
    endif
enddef
Outer()
```
    E130: Unknown function: Inner

Shouldn't the error rather be:

    E1084: Cannot delete Vim9 script function Inner

After all, the function should be known to Vim:
it should look for the function in the block scope according to `:h vim9-scopes`.

Note: the error is only raised for a `:def` inside a `:def`.
If the  outer function is  a `:fu`, no  error is raised;  no matter the  type of
inner function.

##
# missing documentation: we cannot define a ":def" function inside a ":fu" function

We can nest a `:def` inside a `:fu`:
```vim
vim9script
fu Legacy()
    def Vim9()
    enddef
endfu
Legacy()
```
This is documented at `:def`.

But we cannot nest a `:fu` inside a `:def`:
```vim
vim9script
def Vim9()
    fu Legacy()
    endfu
enddef
Vim9()
```
    E1086: Cannot use :function inside :def

It's not documented; neither at `:h def`, nor at `:h :fu`.
It should be (at `:h :fu`?).

Trick  to memorize  the rule:  we can  progress (legacy  → Vim9),  but we  can't
regress (Vim9 → legacy).

# documentation error: a nested function is not always local to the outer function

>     When using `:function` or `:def` to specify a new function inside a function,
>     the function is local to the function.

This should be rephrased like this:

>     When using `:function` or `:def` to define a nested function inside a `:def` function,
>     the nested function is local to the outer function.

---

Explanation:

First, the repetition of the word "function" without any qualifier is confusing.

Second, the original sentence is only true for a `:def` function inside a `:def`
function.  Not for a `:fu` or `:def` function inside a `:fu` function.
In the latter cases, the nested function is global by default:
```vim
vim9script
fu Outer()
    fu Inner()
        echo 'inner'
    endfu
endfu
call Outer()
fu Inner
```
       function Inner()
    1          echo 'inner'
       endfunction
```vim
vim9script
fu Outer()
    def Inner()
        echo 'inner'
    enddef
endfu
call Outer()
fu Inner
```
       def Inner()
    1          echo 'inner'
       enddef

This is still true when the nested function is inside a block:
```vim
vim9script
fu Outer()
    if 1
        fu Inner()
            echo 'inner'
        endfu
    endif
endfu
call Outer()
fu Inner
```
       function Inner()
    1          echo 'inner'
       endfunction
```vim
vim9script
fu Outer()
    if 1
        def Inner()
            echo 'inner'
        enddef
    endif
endfu
call Outer()
fu Inner
```
       def Inner()
    1          echo 'inner'
       enddef

# documentation error: it is possible to define a script-local function inside another function

>     It is not possible to define a script-local function inside a function.

This should be rephrased like this:

>     It is not possible to define a script-local function inside a `:def` function.

Explanation:

The original sentence is only true for a function inside a `:def` function.
Not for a function inside a `:fu` function.
```vim
vim9script
fu Outer()
    fu s:Inner()
        echo 'inner'
    endfu
endfu
Outer()
s:Inner()
```
    inner
```vim
vim9script
fu Outer()
    def s:Inner()
        echo 'inner'
    enddef
endfu
Outer()
s:Inner()
```
    inner

# inconsistency: when we ask for the definition of a Vim9 function, comments are sometimes included, but not always.

    $ vim -Nu NONE -S <(cat <<'EOF'
        def g:Func()
            echo 'one' # inline comment
            # whole comment
            echo 'two' # inline comment
        enddef
        def Func
    EOF
    )

        def Func()~
     1          echo 'one' # inline comment~
     2          # whole comment~
     3          echo 'two' # inline comment~
        enddef~

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def g:Func()
            echo 'one' # inline comment
            # whole comment
            echo 'two' # inline comment
        enddef
        def Func
    EOF
    )

        def Func()~
     1          echo 'one' # inline comment~
     3          echo 'two' # inline comment~
        enddef~

`:vim9script` filters out whole comments in definitions of `:def` functions.
Is it intended?
If so, should it be documented at `:h vim9`?

##
# ?

Should Vim9 script implement the concept of a block at the script level?
```vim
vim9script
if 1
    def Func()
        echo 'test'
    enddef
endif
Func()
```
    test

No error is raised, but `E117` should be raised if the function was local to the
block.

---

Related todo item:

> - At the script level, keep script variables local to the block they are
>   declared in?  Need to remember what variables were declared and delete them
>   when leaving the block.

Although, this one is dedicated to variables; not functions.

Related issue: <https://github.com/vim/vim/issues/6498>

# ?

Can't use ":breakadd func" with a `:def` function.
Maybe it can't work with a compiled function.
If so, it should be documented at `:h vim9-differences`.

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def g:Func()
            echo 'inside'
        enddef
        breakadd func Func
        g:Func()
    EOF
    )

---

Why does it not work for a legacy function in a Vim9 script?

    $ vim -Nu NONE -S <(cat <<'EOF'
        fu Func()
            echo 'inside'
        endfu
        breakadd func Func
        call Func()
    EOF
    )
    ✔

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        fu Func()
            echo 'inside'
        endfu
        breakadd func Func
        Func()
    EOF
    )
    ✘

Probably because `Func()` is now script-local.
But then, why isn't this enough to fix the issue:

    breakadd func s:Func
                  ^^

The issue disappears if we use a global function everywhere:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        fu g:Func()
            echo 'inside'
        endfu
        breakadd func Func
        g:Func()
    EOF
    )

---

What about `:profile`?

# ?

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        # applies to other scopes too
        s:d = {}
        def Func()
            s:d['key'] = 'val'
        enddef
        Func()
    EOF
    )

    E1088: cannot use an index on s:d~

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let d = {}
            d.key = 0
        enddef
        Func()
    EOF
    )

    Not supported yet: d.key = 0~

These  errors are  annoying.   They prevent  us from  refactoring  the start  of
the  autoload script  in `vim-search`;  they  also prevent  us from  eliminating
`strpart()` in `ccomplete.vim`.

I suspect the 2 error messages come from the same limitation.
It may be a known limitation, listed at `:h todo`:

> - Assignment to dict doesn't work:
>       let ret: dict<string> = #{}
>       ret[i] = string(i)

# ?

https://github.com/vim/vim/issues/6553

OTOH, the current documentation is correct when it says that `g:` is needed for a global *variable*, even when the name of the latter contains `#`:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let foo#bar = 123
    EOF
    )

    :echo foo#bar
    E121: Undefined variable: g:foo#bar~

Note how an error is raised because `g:` is missing in the assignment.

Why do we need `g:` for an autoload variable, but not for an autoload function?
<https://github.com/vim/vim/issues/6553#issuecomment-665878820>

>     Normally, in Vim9 script all functions are local.
>     To use a function outside of the script, it either has to be exported/imported, or made global.
>     Autoload scripts are different; they define a third type of function: "autoloadable".
>     Those are recognized by the "name#" prefix.
>     It's like these are exported to this autoload namespace.
>     These functions are not global, in the sense that the g: prefix is not used,
>     neither where it's defined nor where it is called.

---

Also, watch this:
```vim
vim9script
let foo#bar = 123
echo s:
```
    {'foo#bar': 123}
```vim
vim9script
let foo#bar = 123
echo s:foo#bar
```
    E121: Undefined variable: s:foo#bar

If an autoload variable is script-local, why can't we refer to it with an explicit `s:` scope?

# ?

By default, a function is local to the current script, right?

Does that remain true for:

   - `function('Func')`
   - `:breakadd func Func`
   - `:prof func Func`
   ...

If not, is this a bug?

# Vim9: name of `:def` function can't start with a lowercase alphabetic character

Since a `:def` function is script-local  by default, and a script-local `:fu` or
`:def`  function *can*  start with  a  lowercase alphabetic  character, I  would
expect  being able  to start  the name  of a  `:def` function  with a  lowercase
alphabetic character.

---

> Using the "s:" prefix is optional.
<https://github.com/vim/vim/blob/37394ff75270877a032422abcd079a6732a29730/runtime/doc/vim9.txt#L120>

If it  was completely optional, then  I should be able  to drop it even  when it
prefixes a function name starting with a lowercase character.
That's not the case; if you drop `s:`  in front of a function name starting with
a lowercase character, you also have to capitalize the name.

---

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def func()
        enddef
    EOF
    )

    E128: Function name must start with a capital or "s:": func()~
    E193: :enddef not inside a function~

# Vim9: should Vim's help include its own Vim9 script style guide similar to ":h coding-style"?

Maybe it could be based on the one provided by Google.

# ?

Should we enforce the usage of full names of commands and options?

Would this make it easier for Vim developers to write new Vim9 features, and fix Vim9 bugs?

Would it provide other technical benefits?  Like maybe this would make it easier to write a [Vim9 parser](https://github.com/vim/vim/issues/6372), which in turn could be used to write other tools for Vim9, like a [full optimizer](https://github.com/vim/vim/issues/6372#issuecomment-652634882)?

---

FWIW, the Vimscript [style guide from Google](https://google.github.io/styleguide/vimscriptfull.xml?showone=Settings#Settings) recommends using full names:

>    Prefer long names of built in settings (i.e. tabstop over ts).

---

This would also have the obvious benefits of making people write code which is both more readable, and more consistent. For example, there would be only a single way to execute `:nnoremap`, compared to 6 right now:

    :nno
    :nnor
    :nnore
    :nnorem
    :nnorema
    :nnoremap

---

As a side benefit, there would be no extra unexpected behavior when we forget to declare a single-letter variable.  For example, if we forget to declare the variable `n`, instead of Vim populating the arglist with the file paths `=` and `123` when running the following snippet:
```vim
vim9script
n = 123
```
An error would be raised, such as:

    E488: Trailing characters: = 123: n = 123
    E1100: Missing :let: n = 123

Because Vim would not parse `n` as the Ex command `:next`.

# ?
```vim
vim9script
b = 123
```
    ┌───┬───────────────────────────────────────────┐
    │ b │ E94: No matching buffer for = 123         │
    ├───┼───────────────────────────────────────────┤
    │ e │ edit file '= 123'                         │
    ├───┼───────────────────────────────────────────┤
    │ f │ E95: Buffer with this name already exists │
    ├───┼───────────────────────────────────────────┤
    │ g │ global command (equivalent to 'g/123')    │
    ├───┼───────────────────────────────────────────┤
    │ h │ E149: Sorry, no help for = 123            │
    ├───┼───────────────────────────────────────────┤
    │ m │ E16: Invalid range                        │
    ├───┼───────────────────────────────────────────┤
    │ n │ populate arglist with '=' and '123'       │
    ├───┼───────────────────────────────────────────┤
    │ o │ edit file '= 123'                         │
    ├───┼───────────────────────────────────────────┤
    │ r │ E484: Can't open file = 123               │
    ├───┼───────────────────────────────────────────┤
    │ s │ E486: Pattern not found:  123             │
    ├───┼───────────────────────────────────────────┤
    │ t │ E16: Invalid range                        │
    ├───┼───────────────────────────────────────────┤
    │ v │ vglobal command                           │
    ├───┼───────────────────────────────────────────┤
    │ w │ E139: File is loaded in another buffer    │
    ├───┼───────────────────────────────────────────┤
    │ z │ E144: non-numeric argument to :z          │
    └───┴───────────────────────────────────────────┘

All these pitfalls could be fixed if Vim forced the user to prefix these commands with a colon.

Alternatively, the pitfall related to `t` could be fixed by disallowing the commands, just like `:a`, `:c`, `:i`, `:x` are disallowed, in favor of `:copy` which is more readable anyway.

##
##
##
# errors at `:h vim9`
## 98

>     `:def` has no options like `:function` does: "range", "abort", "dict" or
>     "closure".  A `:def` function always aborts on an error, does not get a range
>     passed and cannot be a "dict" function.

The first sentence mentions closures, but not the second one.
Support for closures is in the todo list:

>     - Make closures work:
>       - Create closure in a loop.  Need to make a list of them.

Maybe the doc could say:

>     A `:def` function always aborts on an error, does not get a range
>     passed, cannot be a "dict" function, and may be a closure.

Although, it depends on how it will be implemented.
Here's how it works in python:
<https://stackoverflow.com/a/4020443/9780968>

It seems that there's  nothing special to do to make a  closure work; no special
argument  like  `:h :func-closure`.   However,  the  technical definition  of  a
closure is a bit tricky; for a function to be considered a closure, it must:

   - be nested in another function
   - access at least one variable from the outer scope
   - do so while the outer function has finised its execution

You could argue that  it's too early to be documented,  but `:type` and `:class`
*are* documented even though they haven't been implemented yet.

## 102

>     The argument types and return type need to be specified.  The "any" type can
>     be used; type checking will then be done at runtime, like with legacy
>     functions.

If it  can have a  negative impact on the  function's performance, it  should be
mentioned, so that users don't abuse the `any` type.

## 131

>     - Local to **the current scope and outer scopes** up to the function scope.

Not clear.
I would rather read "the current code block and outer code blocks".

Rationale: Coming from  legacy Vim script,  there is  no smaller scope  than the
function one.  The current sentence implies that there is one – which is true in
Vim9 script – without  specifying what it is.  It's explained  a little later at
`:h vim9-declaration`, but imo `:h vim9-scopes` should be understandable on its own.

## 151

>     Variables can be local to a script, function or code block:

What about the other scopes?  buffer-local, window-local, ...
```vim
vim9script
b:var = 123
```
## 186

From `:h vim9-declaration /Global`:

>     Global, window, tab, buffer and Vim variables can only be used
>     without `:let`, because they are are not really declared, they can also be
>     deleted with `:unlet`.

There should be  a semicolon somewhere, but  I'm not sure which  comma should be
replaced.  Try this:

>     Global, window, tab, buffer and Vim variables can only be used
>     without `:let`**;** because they are are not really declared, they can also be
>     deleted with `:unlet`.

Or this:

>     Global, window, tab, buffer and Vim variables can only be used
>     without `:let`, because they are are not really declared**;** they can also be
>     deleted with `:unlet`.

---

Here is an explanation:

>     Somewhere along the way I realized that  allowing the user of :let with global
>     variables is inconsistent. It  would mean that script-local  variables need to
>     be declared with :let and then later  cannot be used with :let for assigning a
>     value,  while global  variables  would  allow :let  to  be  used anywhere.   I
>     consider it  simpler to only use  :let for declarations, and  global variables
>     are not really declared. I hope this works best.

Source: <https://github.com/vim/vim/issues/6514#issuecomment-662683671>

>     These  variables can  be set  to any  value in  legacy Vim  script and  legacy
>     functions. Specifying a type  has very limited use that way. It  would work to
>     catch mistakes in  Vim9 code, in case you  try to assign a value  of the wrong
>     type, but one  cannot assume that these variables actually  have the specified
>     type. This  also means  that in  compiled functions  the type  always must  be
>     checked anyway.  For consistency I thought it  might be better to just not use
>     types for  these variables, based  on the  namespace. It could be  possible to
>     attach the type to the variable  (would require more memory though). Thus then
>     what you get is  once a variable has been given a type  in Vim9 code, the type
>     will also be checked in legacy  code. This also has runtime overhead, the type
>     needs  to be  checked on  every  assignment. And then  you will  have some  g:
>     variables with a specified type and  some without. Also, what if a variable is
>     deleted and added back with a  different type? Would be confusing, and will be
>     hard to avoid.

Source: <https://github.com/vim/vim/issues/6521#issuecomment-663148684>

I don't understand everything,  but it seems the main issue  is that `b:`, `g:`,
`t:`, `v:`,  `w:`, `$` variables  are "public"; they  can be changed  by various
plugins.

Therefore, it's expected that their type may change over time.
Therefore, it doesn't make sense to give them a type.

It  would be  nice if  the  documentation briefly  explained why  they can't  be
declared like local variables (local to a block, function or script).
What's the main issue?  Again, I think that it boils down to them being public.

---

Once this is fixed, integrate the previous github comments in our notes:

    ## In Vim9 script, what's the main difference between a `b:`, `g:`, `t:`, `w:`, `$` variable and other variables?

Update: I think the help has been fixed/updated.

## 191

>     Variables cannot shadow previously defined variables.

What does this mean?
Does it mean that you can't re-declare a variable?

## 237

From `:h vim9-declaration /cyclic`

>     Note that while variables need to be defined before they can be used,
>     **functions can be called before being defined**.  This is required to be able
>     have cyclic dependencies between functions.  It is slightly less efficient,
>     since the function has to be looked up by name.  And a typo in the function
>     name will only be found when the call is executed.

I can't find a working example.
```vim
vim9script
A()
def A()
enddef
```
    E117: Unknown function: A
```vim
vim9script
def A()
    B()
enddef
A()
def B()
    echo 'test'
enddef
```
    E117: Unknown function: B

## 244

  > Omitting function() ~
  >
  > A user defined function can be used as a function reference in an expression
  > without `function()`. The argument types and return type will then be checked.
  > The function must already have been defined. >
  >
  >         let Funcref = MyFunction

Does not seem to work:
```vim
vim9script
def MyFunction()
    echo 'test'
enddef
let Funcref = MyFunction
```
Could be on the todo list:
<https://github.com/vim/vim/blob/d032f34a51c6722101626c4167dffecc427ac343/runtime/doc/todo.txt#L113-L115>

## 299

From `:h E1050`:

>     recognized, it is required to put a colon before a range.  This will add
>     "start" and print: >

Why do we have to  put a colon in front of a range even  when it's preceded by a
modifier like `:silent`?
```vim
vim9script
def Func()
    sil %d
enddef
Func()
```
    Error detected while processing function <SNR>1_Func:
    line    1:
    E1050: Colon required before a range

Shouldn't `:silent`  be enough to prevent  Vim from parsing/confusing `%`  as an
operator?

Maybe it's because modifiers have not been implemented yet.
<https://github.com/vim/vim/issues/6530#issuecomment-663903048>

## 413

I would rewrite this whole paragraph:

> The boolean operators "||" and "&&" do not change the value: >
>         8 || 2   == 8
>         0 || 2   == 2
>         0 || ''  == ''
>         8 && 2   == 2
>         0 && 2   == 0
>         2 && 0   == 0
>         [] && 2  == []

into this:

> The boolean operators "||" and "&&" do not change the value: >
>         8 || 2   evaluates to  8
>         0 || 2   evaluates to  2
>         0 || ''  evaluates to  ''
>         8 && 2   evaluates to  2
>         0 && 2   evaluates to  0
>         2 && 0   evaluates to  0
>         [] && 2  evaluates to  []

Or into this:

> The boolean operators "||" and "&&" do not change the value: >
>         ( 8 || 2 )  == 8
>         ( 0 || 2 )  == 2
>         ( 0 || '' ) == ''
>         ( 8 && 2 )  == 2
>         ( 0 && 2 )  == 0
>         ( 2 && 0 )  == 0
>         ( [] && 2 ) == []

It's less confusing.  Otherwise, you're tempted  to run the command as is, which
can give unexpected results.

For example:
```vim
vim9script
echo [] && 2 == []
```
    []

While I would expect  `v:true`.  You can get the latter  if you explicitly group
the first 2 operands:
```vim
vim9script
echo ([] && 2) == []
```
    v:true

---

Also, at `:h expr2`, I would briefly explain how `expr1 && expr2` and
`expr1 || expr2` are evaluated:

    expr1 && expr2  ==  expr2  (except if expr1 is 0, 0.0, '', [], {}, v:none)
    expr1 || expr2  ==  expr1  (except if expr2 is 0, 0.0, '', [], {}, v:none)

## 430

At `:h  vim9-gotchas`, I would add  a gotcha about  the fact that you  can *not*
omit `s:` when calling a script-local function from a `:fu` function.
It sounds  obvious, but in  practice, I bet you  may sometimes forget  and don't
understand why your code doesn't work.
```vim
vim9script
fu Foo()
    call Bar()
endfu
def Bar()
    echo 'bar'
enddef
Foo()
```
    Error detected while processing function <SNR>1_Foo:
    line    1:
    E117: Unknown function: Bar

The reason why  you may forget, is because  in Vim9 script you can  omit `s:` in
front of a function name most of the time; that is when:

   - defining a `:def` function
   - defining a `:fu` function
   - calling a script-local function from a `:def` function

## 450

> Vim9 functions are compiled as a whole: >
>         def Maybe()
>           if !has('feature')
>             return
>           endif
>           use-feature  " May give compilation error
>         enddef

I can't reproduce this pitfall:
```vim
vim9script
def Maybe()
    if !has('ruby')
        return
    endif
    ruby print('Hello')
enddef
Maybe()
```
---

> For a workaround, split it in two functions: >
>         func Maybe()
>           if has('feature')
>             call MaybyInner()
>           endif
>         endfunc
>         if has('feature')
>           def MaybeInner()
>             use-feature
>           enddef
>         endif

Why mixing a legacy `:fu` function and a `:def` function?
Why not 2 `:def`?

> For a workaround, split it in two functions: >
>         **def** Maybe()
>           if has('feature')
>             call MaybyInner()
>           endif
>         **enddef**
>         if has('feature')
>           def MaybeInner()
>             use-feature
>           enddef
>         endif

---

I don't understand how the workaround works.
If  Vim  doesn't  support  `feature`,  then  why  isn't  there  any  error  when
`MaybeInner()` is compiled?   One explanation would be  that `if has('feature')`
is evaluated at compile time, and if it fails, `MaybeInner()` is not compiled.
But watch this:
```vim
vim9script
def Func()
    ruby print('Hello')
enddef
defcompile
```
This doesn't raise any error, even though my Vim doesn't support the ruby interface.

## 520

>     If the script the function is defined in is Vim9 script, then script-local
>     variables can be accessed without the "s:" prefix.  They must be defined
>     before the function is compiled.  If the script the function is defined in is
>     legacy script, then script-local variables must be accessed with the "s:"
>     prefix.

I would re-write this paragraph like so:

>     If the function is defined in a Vim9 script, then script-local variables can
>     be accessed without the "s:" prefix.  They must be defined before the function
>     is compiled.  If the function is defined in a legacy script, then script-local
>     variables must be accessed with the "s:" prefix.

Easier to understand.

## 558

> The following builtin types are supported:

Maybe the doc should mention that composite types can be nested up to 2 levels:
```vim
vim9script
def Func(arg: list<list<any>>)
enddef
Func([[0]])
```
✔
```vim
vim9script
def Func(arg: list<list<list<any>>>)
enddef
Func([[[0]]])
```
    Error detected while processing function <SNR>1_Func:
    line    1:
    E1013: type mismatch, expected list<list<list<any>>> but got list<list<any>>
                                                             ^-----------------^

Note that if  you nest a composite type,  it must declare the type  of its items
with `<any>`; nothing else:
```vim
vim9script
def Func(arg: list<list<number>>)
enddef
Func([[0]])
```
    Error detected while processing function <SNR>1_Func:
    line    1:
    E1013: type mismatch, expected list<list<number>> but got list<list<any>>

Is all of this working as intended?
That is, the fact that the maximum level of nesting is 2, and a nested composite
type must use `<any>`.

## 666

From `:h :vim9 /common`:

>     In Vim9 script the global "g:" namespace can still be used as before.  And the
>     "w:", "b:" and "t:" namespaces.  These have in common that variables are not
>     declared and they can be deleted.

Maybe environment variables should be mentioned as well.

And maybe registers (like `@r`).
Indeed, you can't use `:let` with them; but you can't you use `:unlet` either.

Also, I would rewrite the whole paragraph like this:

>     In Vim9 script the global "g:" namespace can still be used as before.  And the
>     "w:", "b:", "t:", and "$" namespaces.  These have in common that their
>     variables cannot be declared but can be deleted.
>     For variables which are local to a script, function or code block, the opposite
>     is true.  They can be declared but cannot be deleted.

## 725

>     The `import` commands are executed when encountered.
>     If that script  (directly or indirectly) imports the current  script, then items
>     defined after the `import` won't be processed yet.
>     Therefore, cyclic imports can exist, but may result in undefined items.

What is "that script"?  The current script, or the script from which we import items?

I *think* it's the script from which we import items.

What are "items defined after the `import`"?
Items defined after the `import` in  the current script?  Or items defined after
the `import` in the script from which we import items?

I *think* it's the items defined after the import in the current script.

The paragraph would really benefit from an example.
Does the following commands do a good job illustrating the pitfall?

    $ cat <<'EOF' >/tmp/bar.vim
        vim9script
        export const FOO = 123
        import BAR from './foo.vim'
    EOF

    $ cat <<'EOF' >/tmp/foo.vim
        vim9script
        import FOO from './bar.vim'
        export const BAR = 456
    EOF

    $ vim -Nu NONE -S /tmp/foo.vim

    Error detected while processing /tmp/bar.vim:~
    line    3:~
    E1048: Item not found in script: BAR~

## 800

>     The error can be given at compile time, no error handling is needed at runtime.

If  the function  contains a  type error,  it's still  installed (like  a legacy
function), but its body is empty.

This is neat, and maybe it should be documented.
If a  legacy function  contains syntax/type errors,  and was  invoked frequently
(e.g. `InsertCharPre` autocmd),  the same  errors were raised  repeatedly.  This
shoud not happen with a `:def` function.

## 887

>     When sourcing a Vim9 script from a legacy script, only the items defined
>     globally can be used; not the exported items.

Actually, I think you can also use any item defined in the `b:`, `t:`, and `w:` namespace;
but not one defined in the `s:` namespace.

##
# missing doc at `:h vim9`
## can't use `.` for concatenation

You must use `..`:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let str = 'a' . 'b'
    EOF
    )

    E15: Invalid expression: 'a' . 'b'

This is not documented at `:h vim9-differences`.
Although, there is this:

>     When using `..` for string concatenation the arguments are always converted to
>     string. >
>             'hello ' .. 123  == 'hello 123'
>             'hello ' .. v:true  == 'hello true'

But this makes it seem as if `.` was still ok.
It is not.

I would write this instead:

>     `.` can no longer be used for string concatenation.  Instead, `..` must be used.
>     Note that `..` always converts its operands to string. >
>             'hello ' .. 123  == 'hello 123'
>             'hello ' .. v:true  == 'hello true'

## can drop ":call" in commands and autocommands but not in mappings

Maybe this should be documented at `:h vim9-gotchas`?
```vim
vim9script
set ut=500
augroup test | au!
    au CursorHold * Func()
augroup END
def Func()
    echom 'test'
enddef
```
    test
```vim
vim9script
com Cmd Func()
def Func()
    echom 'test'
enddef
Cmd
```
    test
```vim
vim9script
nno cd :<sid>Func()<cr>
def Func()
    echom 'test'
enddef
feedkeys('cd', 'it')
```
    E488: Trailing characters: SNR>1_Func()

Btw, the leading `<` is missing because it was parsed as the `:<` Ex command; as
a result, the rest of the line is parsed as an argument, but `:<` doesn't accept
this kind of argument (only a number).

## can't declare a register inside a ":def" function

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let @a = 'text'
        enddef
        Func()
    EOF
    )

    E1066: Cannot declare a register: @a

This – as well as `E1066` – should be documented at `:h vim9-declaration`.

Drop the `let`:
```vim
vim9script
def Func()
    @a = 'text'
enddef
Func()
reg a
```
Or use `getreg()` and `setreg()` when you need to refer to the contents of a register.

## concept of block-local function

There is this at `:h vim9-declaration`:

>     The variables are only visible in the block where they are defined and nested
>     blocks.  Once the block ends the variable is no longer accessible: >

But it's about variables; there is nothing about functions.

##
# error at `:h autoload`

`:h vim9` was correctly updated, but not `:h autoload`:
<https://github.com/vim/vim/issues/6553>

---

>     It's like these are exported to this autoload namespace.

If an autoload  function is really exported  to some namespace, does  it mean we
don't need to use the `export` command to export it?
And we  can automatically  import it  under whatever name  we want  from another
script?  Make some tests.

#
# Plan

Re-read the whole Vim9 documentation in your Vim fork.
Make sure there is no typo, no missing comma/semicolon, no wrong word...

Once you've reviewed the documentation, make sure all the minor errors mentioned
in this  file have  been correctly  fixed in your  fork.  Then,  save a  diff in
`~/Desktop/patch.txt`.

Next, review the remaining Vim9 items in this file.
Refactor anything which looks like a bug into a proper dedicated report.

Finally, submit a PR for the patch,  and explain the various changes; no need to
repeat yourself for similar  errors, but do give an explanation  for a family of
errors (like comma splices).

Also, review the  remaining Vim9 items in  this file; for each of  them, leave a
remark in the OP of your PR.

---

Also,  submit a  report  regarding the  `:h  todo` items  related  to Vim9  (and
possibly a few others from the current file).

In this report, mention the fact that this issue is absent from the todo list:
<https://github.com/vim/vim/issues/6496>

And maybe that it would be nice for `:def` to have a completion.
Useful when you  want to get the  definition of a function  while debugging some
issue; like: what does that function where an error was raised?
Sure, you can use `:fu` instead; but it's inconsistent to define a function with
`:def` then ask for its definition with `:fu`.
Although, I'm reluctant to mention this because  we already did it in #6525, and
closed the issue.
But look at it this way:  `:def` is the *most important* command in Vim9 script.
Indeed, the main goal  of the latter is to provide  better performance, which is
achieved by compiling functions, which can only be done in a `:def` function.
And yet, right now, there is no completion for `:def`; this is really unexpected.
I could understand for a more obscure command, however `:def` is anything but obscure.

Temporary workaround:

    cnorea <expr> def getcmdtype() is# ':' && getcmdpos() == 4 ? 'Def' : 'def'
    com -bar -complete=custom,s:def_complete -nargs=? Def exe s:def(<q-args>)
    fu s:def_complete(argLead, _l, _p) abort
        return getcompletion(a:argLead, 'function')->join("\n")
    endfu
    fu s:def(name) abort
        let name = trim(a:name, '()')
        try
            exe 'def ' .. name
        catch
            return 'echoerr ' .. string(v:exception)
        endtry
        return ''
    endfu

Limitation: contrary to `:fu`, `:Def` can't complete script-local functions.
That's because `getcompletion()` can't either.  Is it a bug?

##
# try finish @andymass patch regarding "setreg()" so that it gets merged

I think all that is missing is some documentation.
<https://github.com/vim/vim/pull/3370>

> OK, then it would be good to write the help for this, and cover the corner cases. Should cover all possible types of contents and what happens when the register type is changed. Esp. from/to block.

---

There are 9 tests to conduct.

Note: when changing the type of the register *to* blockwise, make several subtests.
Make the width of the block vary across all numbers between 1 and 15.

                           ┌──────────────────────────────────────┐
                           │                  to                  │
                           ├───────────────┬──────────┬───────────┤
                           │ characterwise │ linewise │ blockwise │
    ┌──────┬───────────────┼───────────────┼──────────┼───────────┤
    │      │ characterwise │               │          │           │
    │      ├───────────────┼───────────────┼──────────┼───────────┤
    │ from │ linewise      │               │          │           │
    │      ├───────────────┼───────────────┼──────────┼───────────┤
    │      │ blockwise     │               │          │           │
    └──────┴───────────────┴───────────────┴──────────┴───────────┘

TODO: Add a highlight for the character from which we put.
Convert all matches into text-properties.

    11: no change
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G4|v4G5|"ry
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'c'})
bo vnew
norm! "rp
call Matchadd()
```
    12: new empty line above when putting
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G4|v4G5|"ry
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'l'})
bo vnew
norm! "rp
call Matchadd()
```
    13: no change, regardless of the width of the block
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G4|v4G5|"ry
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'b20'})
bo vnew
norm! "rp
call Matchadd()
```
    21: *no* new empty line above when putting
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G"r3yy
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'c'})
bo vnew
norm! "rp
call Matchadd()
```
    22: no change
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G"r3yy
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'l'})
bo vnew
norm! "rp
call Matchadd()
```
    23: *no* new empty line added above when putting
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G"r3yy
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'b20'})
bo vnew
norm! "rp
call Matchadd()
```
    31: no change
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil exe "norm! 2G3|\<c-v>4G8|" .. '"ry'
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'c'})
bo vnew
norm! "rp
call Matchadd()
```
    32: new empty line above when putting
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil exe "norm! 2G3|\<c-v>4G8|" .. '"ry'
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'l'})
bo vnew
norm! "rp
call Matchadd()
```
    33: no change, regardless of the width of the block
```vim
call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil exe "norm! 2G3|\<c-v>4G8|" .. '"ry'
call Matchadd()
bo vnew
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'b20'})
bo vnew
norm! "rp
call Matchadd()
```
Conclusion:

   - if the type is unchanged, the register is unchanged

         11: no change
         22: no change
         33: no change, regardless of the width of the block

   - if the type is changed *from* linewise, there is no longer an empty line left
     above when putting

         21: *no* new empty line above when putting
         23: *no* new empty line added above when putting

   - if the type is changed *to* linewise, there *is* an empty line left
     above when putting

         12: new empty line above when putting
         32: new empty line above when putting

   - if the type is changed from or to blockwise, the register is unchanged

         13: no change, regardless of the width of the block
         31: no change

---

Reconduct the same tests, but this time, put the register right in the middle of
an existing text.  When changing the type  of a register to blockwise, we should
sometimes see that Vim adds spaces.

    11: no change
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G4|v4G5|"ry
call Matchadd()
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()

call setreg('r', #{regtype: 'c'})
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()
```
    12: reset to linewise
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G4|v4G5|"ry
call Matchadd()
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()

call setreg('r', #{regtype: 'l'})
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()
```
    13: if necessary, Vim adds trailing whitespace to compensate for lines which are shorter
        than the width of the block
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G4|v4G5|"ry
call Matchadd()
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()

call setreg('r', #{regtype: 'b20'})
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()
```
    21: reset to characterwise
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G"r3yy
call Matchadd()
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()

call setreg('r', #{regtype: 'c'})
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()
```
    22: no change
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G"r3yy
call Matchadd()
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()

call setreg('r', #{regtype: 'l'})
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()
```
    23: if necessary, Vim adds trailing whitespace to compensate for lines which are shorter
        than the width of the block
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil norm! 2G"r3yy
call Matchadd()
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()

call setreg('r', #{regtype: 'b20'})
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()
```
    31: reset to characterwise
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil exe "norm! 2G3|\<c-v>4G8|" .. '"ry'
call Matchadd()
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()

call setreg('r', #{regtype: 'c'})
bo vnew
call Setline()
norm! 3G5|"rp
call Matchadd()
```
    32: reset to linewise
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil exe "norm! 2G3|\<c-v>4G8|" .. '"ry'
call Matchadd()
bo vnew
call Setline()
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'l'})
bo vnew
call Setline()
norm! "rp
call Matchadd()
```
    33: if necessary, Vim adds trailing whitespace to compensate for lines which are shorter
        than the width of the block
```vim
fu Setline()
    call setline(1, ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX'])
    let &l:ul = &l:ul
endfu
call Setline()

fu Matchadd()
    call matchadd('ErrorMsg', ' ', 100, -1)
    let type = getregtype('r')
    let text = getreg('r', 1, 1)
    if type is# 'v'
        let text = join(text, "\n")
        let pat = '\%' .. line('.') .. 'l\%' .. virtcol('.') .. 'v\_.\{' .. strchars(text, 1) .. '}'
    elseif type is# 'V'
        let pat = '\%' .. line('.') .. 'l\_.*\%' .. (line('.') + len(text) - 1) .. 'l'
    elseif type =~# "\<c-v>" .. '\d\+'
        let [line, vcol] = [line('.'), virtcol('.')]
        let pat = map(text, {i -> '\%' .. (line + i) .. 'l\%' .. vcol .. 'v.\{' .. strchars(text[i], 1) .. '}'})->join('\|')
    endif
    call matchadd('Search', pat, 90, -1)
endfu

sil exe "norm! 2G3|\<c-v>4G8|" .. '"ry'
call Matchadd()
bo vnew
call Setline()
norm! "rp
call Matchadd()

call setreg('r', #{regtype: 'b20'})
bo vnew
call Setline()
norm! "rp
call Matchadd()
```
Conclusion:

   - no change from characterwise to characterwise, nor from linewise to linewise

   - from any type to characterwise or linewise, the type is simply reset

   - from any type to blockwise, if necessary, Vim adds trailing whitespace to
     compensate for lines which are shorter than the width of the block;
     if a line is shorter than the specified block width, it is not truncated

---

Just to be clear, the patch does not add any new feature.  We can already reset the type of a register from any type to any type.  For example, if the register `r` contains a characterwise text, and we want to reset its type to `^V123`, we can do so with:

    :call getreginfo('r')->extend({'regtype': 'b123'})->setreg('r')

The patch simply provides a simpler way to do the same thing:

    :call setreg('r', {'regtype': 'b123'})

That being said, I *think* I tested all the possibilities, and here is a summary of what I observed:

   1. if the register type is reset from characterwise to characterwise, or from linewise to linewise, no attribute of the register changes

   2. when the register is put from normal mode, if its type has been changed and reset to either characterwise or linewise, it's correctly put as a characterwise or linewise register

   3. when the register is put from command-line mode (via `:put`) or inserted via `CTRL-R`, the register is put as if it was linewise; which is equivalent to either `1.` or `2.`

   4. if the register type is reset to blockwise, and one of its line is shorter or longer than the specified block width, the line is neither truncated nor extended

   5. when the register is put from normal mode, if its type has been reset to blockwise, and one of its line is shorter than the specified block width, Vim adds as many trailing spaces as necessary to compensate if necessary

The tricky part to explain is the "if necessary".

Each line of the register is going to be put on some line of the buffer. And the cursor has a column position. Those 2 numbers *may* give a valid position in the buffer; one for each register line. I think Vim adds trailing spaces if, and only if, that position is valid and there exists a character in the buffer *after* it.

Since `1.` and `2.` don't describe anything unexpected, I'm not sure they need to be documented.
`3.` is already documented.
`4.` and `5.` may be unexpected, therefore need to be documented.
`4.` is easy to document, but `5.` is not.

Here is my first attempt:
```diff
diff --git a/runtime/doc/eval.txt b/runtime/doc/eval.txt
index ed4f8aab0..b17654b49 100644
--- a/runtime/doc/eval.txt
+++ b/runtime/doc/eval.txt
@@ -9265,8 +9265,20 @@ setreg({regname}, {value} [, {options}])
 		You can also change the type of a register by appending
 		nothing: >
 			:call setreg('a', '', 'al')
+<
+		Or by using a dictionary which includes the "regtype" key: >

-<		Can also be used as a |method|, the base is passed as the
+                        :call setreg('a', {'regtype': 'l'})
+<
+		Note: If you reset the type of a register to blockwise, and one
+		of its line is longer or shorter than the specified width of the
+		block, the line is neither truncated nor extended.  When you put
+		the register from normal mode, if one of its line is shorter
+		than the specified width of the block, Vim adds as many trailing
+		spaces as necessary to compensate, if necessary; that is, if
+		they are needed to reach an existing character in the buffer.
+
+		Can also be used as a |method|, the base is passed as the
 		second argument: >
 			GetText()->setreg('a')

```
@andymass: What is your opinion regarding these observations; did I miss anything?  And what about the help, can you rephrase it in a more understandable way?

---

Oh I see; I misunderstood what was required.  I thought we only needed to document the usage of a dictionary.  But you're right; it would be better to document everything: dictionary, list, string.  I'll try to make more tests when I have the time, but it's not going to be easy, because there are so many parameters to consider:

   - which conversion type do we perform? (3 x 3 = 9 possibilities)
   - do we use a dictionary or a list/string as the second argument of `setreg()` (2 possibilities)
   - do we put from normal mode or insert/command-line mode (2 possibilities)

That's already 9 x 2 x 2 = 36 possibilities.
And then, there's the special case of resetting a register to blockwise:

   - are there some lines which are shorter than the specified size?  (2 possibilities)
   - are there some lines which are longer than the specified size?  (2 possibilities)
   - do we specify a size or not? (2 possibilities)

This means that each of the 12 previous possibilities which convert to blockwise:

   - characterwise to blockwise using a dictionary, but without a specified size
   - linewise to blockwise using a dictionary, but without a specified size
   - blockwise to blockwise using a dictionary, but without a specified size

   - characterwise to blockwise using a list/string, but without a specified size
   - linewise to blockwise using a list/string, but without a specified size
   - blockwise to blockwise using a list/string, but without a specified size

   - characterwise to blockwise using a dictionary, and with a specified size
   - linewise to blockwise using a dictionary, and with a specified size
   - blockwise to blockwise using a dictionary, and with a specified size

   - characterwise to blockwise using a list/string, and with a specified size
   - linewise to blockwise using a list/string, and with a specified size
   - blockwise to blockwise using a list/string, and with a specified size

must be multiplied by 2 x 2 x 2 = 8 additional possibilities.  Which makes 8 x 12 + 36 = 132 possibilities to test.

I did already make [some tests](https://gist.github.com/lacygoill/4f4922b19dea44497da9dc9ed962da7b), but nowhere near enough.

> Block size doesn't really depend on contents, and with a specified size

True, it doesn't change the register, but it changes what will be put in a buffer when using the `p` or `P` normal command.  I thought it should be documented, but I'm not sure anymore.

# abbreviation sometimes unexpectedly expanded inside a word

**Describe the bug**

An abbreviation is sometimes unexpectedly expanded in the middle of a word.

**To Reproduce**

Run this shell command:

    vim -Nu NONE -S <(cat <<'EOF'
        set bs=start
        inorea ab cd
        pu!='yyyy'
        norm! 3|
        call feedkeys("i\<c-u>xxab ", 't')
    EOF
    )

The buffer contains the line:

    xxcd yy

Notice how `ab` has been expanded into `cd`.

**Expected behavior**

The buffer contains the line:

    xxab yy

**Environment**

 - Vim version: 8.2 Included patches: 1-1058
 - OS: Ubuntu 16.04.6 LTS
 - Terminal: XTerm(356)

**Additional context**

This behavior is documented somewhere below `:h abbreviations` (look for the word `rule`):

> full-id   In front of the match is a non-keyword character, **or this is where**
>           **the line or insertion starts.**

I'm not sure what is the rationale behind this behavior; I guess it's convenient to be able to expand an abbreviation from any point in the line, by entering insert mode right in front of the latter.
But I find it unexpected to persist even after you've deleted some text before the insertion point.

---

Assuming it can be considered as a bug, I don't know whether it can be fixed.  For the moment, I'm experimenting this code:

    augroup restrict_abbreviations | au!
        au InsertEnter * let s:start_insertion = col('.')
        au InsertCharPre * call s:restrict_abbreviations()
    augroup END
    fu s:restrict_abbreviations() abort
        if v:char =~# '\k'
            \ || s:start_insertion -1 <= searchpos('[^[:keyword:]]', 'bn')[1]
            \ || state() =~# 'm'
            return
        endif
        call feedkeys("\<c-v>"..v:char, 't')
        let v:char = ''
    endfu

So far, it seems to work.

# some todo items are stale

I had a look at the first half of the todo list, and found some items which could be stale.  I don't submit a PR, because I'm not sure for all of them.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L137-L140):

> - With some sequence get get hidden finished terminal buffer. (#5768)
>     Cannot close popup terminal (#5744)
>     Buffer can't be wiped, gets status "aF". (#5764)
>     Is buf->nwindows incorrect?

No longer relevant since [8.2.0743](https://github.com/vim/vim/releases/tag/v8.2.0743).

Actually, I'm not sure that `#5768` is no longer relevant since 8.2.0743.  Maybe it was fixed by another patch; but it is fixed anyway.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L141-L142):

> - popup_clear() and popup_close() should close the terminal popup, and
>    make the buffer hidden. #5745

No longer relevant since [8.2.0747](https://github.com/vim/vim/releases/tag/v8.2.0747).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L498-L499):

> v:register isn't reset early enough, may be used by next command.
> (Andy Massimino, #5294, possible fix in #5305)

No longer relevant since [8.2.0929](https://github.com/vim/vim/releases/tag/v8.2.0929):

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L583-L584):

> Add a way to create an empty, hidden buffer.  Like doing ":new|hide".
> ":let buf = bufcreate('name')

*Maybe* no longer relevant since Vim supports `bufadd()` and `bufload()`.  Now, one can run:

    vim -Nu NONE +'let buf = bufadd("name") | call bufload(buf) | call setbufvar(buf, "&buflisted", 1)'

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1202-L1204):

> Implement named arguments for functions:
>     func Foo(start, count = 1 all = 1)
>     call Foo(12, all = 0)

No longer relevant since [8.1.1310](https://github.com/vim/vim/releases/tag/v8.1.1310).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1396):

> Cannot delete a file with square brackets with delete(). (#696)

No longer relevant since [8.1.1378](https://github.com/vim/vim/releases/tag/v8.1.1378).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1406):

> 'hlsearch' interferes with a Conceal match. (Rom Grk, 2016 Aug 9)

*Maybe* no longer relevant since [8.1.1082](https://github.com/vim/vim/releases/tag/v8.1.1082).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1419):

> Possibly wrong value for seq_cur. (Florent Fayolle, 2016 May 15, #806)

No longer relevant since [8.0.1290](https://github.com/vim/vim/releases/tag/v8.0.1290).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1439):

> Add redrawtabline command. (Naruhiko Nishino, 2016 Jun 11)

No longer relevant since [8.1.0706](https://github.com/vim/vim/releases/tag/v8.1.0706).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1510):

> Patch to show search statistics. (Christian Brabandt, 2016 Jul 22)

No longer relevant since [8.1.1270](https://github.com/vim/vim/releases/tag/v8.1.1270).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1516-L1522):

> Using ":windo" to set options in all windows has the side effect that it
> changes the window layout and the current window.  Make a variant that saves
> and restores.  Use in the matchparen plugin.
> Perhaps we can use ":windo <restore> {cmd}"?
> Patch to add <restore> to :windo, :bufdo, etc. (Christian Brabandt, 2015 Jan
> 6, 2nd message)
> Alternative: ":keeppos" command modifier: ":keeppos windo {cmd}".

*Maybe* no longer relevant since [8.1.1418](https://github.com/vim/vim/releases/tag/v8.1.1418).

Rationale: you can now use `map()` + `win_execute()` to emulate `:windo` without side-effects:

    :call range(1, winnr('$'))->map({_, v -> win_execute(v, '" set some option')})

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1553):

> Add "===" to have a strict comparison (type and value match).

*Maybe* no longer relevant since Vim supports `is#`.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1726):

> Patch to add :arglocal and :arglists. (Marcin Szamotulski, 2014 Aug 6)

`:arglocal` already exists, so this item seems at least partially stale.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1754-L1755):

> Include a plugin manager with Vim? Neobundle seems to be the best currently.
> Also Vundle: https://github.com/gmarik/vundle

Right now, I think the most popular plugin manager is [vim-plug](https://github.com/junegunn/vim-plug), not Neobundle.

Although, one could make the argument that it would be better to include [minpac](https://github.com/k-takata/minpac) since it leverages the builtin package feature.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1808-L1809):

> Patch for XDG base directory support. (Jean François Bignolles, 2014 Mar 4)
> Remark on the docs.  Should not be a compile time feature.  But then what?

Maybe this item should be updated to reference the issue #2034 which is relevant (the [last comment](https://github.com/vim/vim/issues/2034#issuecomment-559254363) is imo especially interesting).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1869-L1870):

> Exception caused by argument of return is not caught by try/catch.
> (David Barnett, 2013 Nov 19)

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L2093-L2094):

> Bug in try/catch: return with invalid compare throws error that isn't caught.
> (ZyX, 2011 Jan 26)

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L2687):

> try/catch not working for argument of return. (Matt Wozniski, 2008 Sep 15)

Some of these items *could* be duplicate.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L1905):

> patch to add "combine" flag to  syntax commands. (so8res, 2012 Dec 6)

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L2284-L2285):

> Patch to add "combine" to :syntax, combines highlight attributes. (Nate
> Soares, 2012 Dec 3)

These items *could* be duplicate.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L2479-L2480):

> Consider making YankRing or something else that keeps a list of yanked text
> part of standard Vim.  The "1 to "9 registers are not sufficient.

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L5982-L5984):

> 6   When yanking into the unnamed registers several times, somehow make the
>     previous contents also available (like it's done for deleting).  What
>     register names to use?  g"1, g"2, etc.?

These items *could* be duplicate.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L3259-L3260):

> 7   Add a command that goes back to the position from before jumping to the
>     first quickfix location.  ":cbefore"?

The name `:cbefore` is already taken.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L3297):

> 7   Implement 'prompt' option.	Init to off when stdin is not a tty.

Maybe no longer relevant since the `'prompt'` option exists.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L3475-L3476):

> 8   X11 GUI: When menu is disabled by excluding 'm' from 'guioptions', ALT key
>     should not be used to trigger a menu (like the Win32 version).

Maybe no longer relevant.  Test with:

    vim -Nu NONE -g --cmd 'set go-=m' +startinsert

Press `M-f`: the `File` menu is not opened, and a character is inserted.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L3515-L3516):

> 8   A dead circumflex followed by a space should give the '^' character
>     (Rommel).  Look how xterm does this.

Maybe no longer relevant as it works for me.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L3615-L3616):

> -   Can't disable terminal flow control, to enable the use of CTRL-S and
>     CTRL-Q.  Add an option for it?

No longer relevant since [8.2.0852](https://github.com/vim/vim/releases/tag/v8.2.0852) and [8.2.0856](https://github.com/vim/vim/releases/tag/v8.2.0856).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L3619-L3625):

> -   When the quickfix window is open and executing ":echo 'hello'" using the
>     Command-line window, the text is immediately removed by the redrawing.
>     (Michael Henry, 2008 Nov 1)
>     Generic solution: When redrawing while there is a message on the
>     cmdline, don't erase the display but draw over the existing text.
>     Other solution, redraw after closing the cmdline window, before executing
>     the command.

No longer relevant since [8.1.0698](https://github.com/vim/vim/releases/tag/v8.1.0698).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L4085-L4086):

> -   Support spelling words in CamelCase as if they were two separate words.
>     Requires some option to enable it. (Timothy Knox)

No longer relevant since [8.2.0953](https://github.com/vim/vim/releases/tag/v8.2.0953).

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L4693-L4694):

    8   When reading from stdin allow suppressing the "reading from stdin"
        message.

No longer relevant since [7.4.1453](https://github.com/vim/vim/releases/tag/v7.4.1453) which provides `--not-a-term`.

---

[Source](https://github.com/vim/vim/blob/df069eec3b90401e880e9b0e258146d8f36c474d/runtime/doc/todo.txt#L4461-L4462):

> 8   Add referring to key options with "&t_xx".  Both for "echo &t_xx" and
>     ":let &t_xx =".  Useful for making portable mappings.

No longer relevant since [8.0.0302](https://github.com/vim/vim/releases/tag/v8.0.0302).

---

Closing as *if* some of those items are stale, they'll be removed in the next update of the runtime files.

## new batch of stale items

> Completion for :!cmd shows each match twice. #1435

Fixed by: <https://github.com/vim/vim/releases/tag/v8.1.0017>

---

> When 'keywordprg' starts with ":" the argument is still escaped as a shell
> command argument. (Romain Lafourcade, 2016 Oct 16, #1175)

Fixed by: <https://github.com/vim/vim/releases/tag/v8.0.0060>

---

From `:h map-<expr>`

> Note that there are some tricks to make special keys work and escape CSI bytes
> in the text.  The |:map| command also does this, thus you must avoid that it
> is done twice.  This does not work: >
>         :imap <expr> <F3> "<Char-0x611B>"
> Because the <Char- sequence is escaped for being a |:imap| argument and then
> again for using <expr>.  This does work: >
>         :imap <expr> <F3> "\u611B"
> Using 0x80 as a single byte before other text does not work, it will be seen
> as a special key.

Most of this (if not all) is no longer relevant since [7.3.283](https://github.com/vim/vim/releases/tag/v7.3.283).

##
# Vim todo list
## line 1189

This could be very useful to make `/tmp/.vimkeys` human-readable:

    Add a "keytrans()" function, which turns the internal byte representation of a
    key into a form that can be used for :map.  E.g.
        let xx = "\<C-Home>"
        echo keytrans(xx)
        <C-Home>

Report it here?  <https://github.com/vim/vim/issues/4725>

Also, this issue looks similar: <https://github.com/vim/vim/issues/4029>
Are they duplicate?

Also, read this: <https://vi.stackexchange.com/a/22312/17449>

## line 3289

Can't reproduce.

    7   The ":undo" command works differently in Ex mode.  Edit a file, make some
        changes, "Q", "undo" and _all_ changes are undone, like the ":visual"
        command was one command.
        On the other hand, an ":undo" command in an Ex script only undoes the last
        change (e.g., use two :append commands, then :undo).

Related: <https://github.com/vim/vim/issues/1662>

## line 3311

Can't reproduce.

    7   This Vi-trick doesn't work: "Q" to go to Ex mode, then "g/pattern/visual".
        In Vi you can edit in visual mode, and when doing "Q" you jump to the next
        match.  Nvi can do it too.

## line 3628

Can't reproduce:

    9   When the last edited file is a help file, using '0 in a new Vim doesn't
        edit the file as a help file.  'filetype' is OK, but 'iskeyword' isn't,
        file isn't readonly, etc.

`git-bisect(1)` tells us one of these fixed the issue:

    b3d17a20d243f65bcfe23de08b7afd948c5132c2
    56a63120992cc3e1f50d654a3f8aeace40bf12ef

But they seem irrelevant...

## We've stopped looking for errors here:

    8   When an ":edit" is inside a try command and the ATTENTION prompt is used,
        the :catch commands are always executed, also when the file is edited
        normally.  Should reset did_emsg and undo side effects.  Also make sure
        the ATTENTION message shows up.  Servatius Brandt works on this.

##
# The descriptions of the local plugins are not aligned in the main help file:

    vim -Nu NORC -S <(cat <<'EOF'
        set rtp-=~/.vim
        set rtp-=~/.vim/after
        set rtp^=~/.vim/plugged/asyncmake
        set rtp^=~/.vim/plugged/vim-autoread
        set rtp^=~/.vim
        set rtp+=~/.vim/after
    EOF
    )

# duplicate runtime bugs

Those reports all have in common a  wrong syntax highlighting in a bash file due
to a curly brace:

    https://github.com/vim/vim/issues/2949

        var="${var/#/"${new_prefix}"}"

    https://github.com/vim/vim/issues/1750

        if [ -n "${arg%{*}" ]; then
          echo $arg
        fi

    https://github.com/vim/vim/issues/5085

        #!/usr/bin/bash

        echo "${1//\${/dollar curly}"
        echo "The rest of this file is shDerefPPSleft inside double quotes"
        echo and shDoubleQuote _outside_ double quotes

##
# C-e does not always get back the originally typed text

According to `:h complete_CTRL-E`, `C-e` can be pressed while the pum is open to get back the originally typed text:

>                                                             *complete_CTRL-E*
>     When completion is active you can use CTRL-E to stop it and go back to the
>     originally typed text.  The CTRL-E will not be inserted.

# `no_mail_maps`

Hello,

According to `:h no_mail_maps` and `:h no_plugin_maps`, the user should be able to prevent the definition of filetype specific mappings by setting the variable `no_{filetype}_maps` (for a given filetype) or `no_plugin_maps` (for all filetypes).

So, I wrote this PR to prevent the installation of the mappings in case the user set one of the variables `g:no_plugin_maps` or `g:no_python_maps`.

Thank you very much for your plugin.

---

Don't forget to update the date of last change in the files.

---

    if !exists("no_plugin_maps") && !exists("no_vim_maps")
        ...
    endif

https://github.com/vim/vim/pull/2409

Default filetype plugins installing mappings and NOT respecting `g:no...map`:

    $VIMRUNTIME/ftplugin/abaqus.vim
    $VIMRUNTIME/ftplugin/ada.vim
    $VIMRUNTIME/ftplugin/context.vim
    $VIMRUNTIME/ftplugin/fortran.vim
    $VIMRUNTIME/ftplugin/gitcommit.vim
    $VIMRUNTIME/ftplugin/hamster.vim
    $VIMRUNTIME/ftplugin/hog.vim
    $VIMRUNTIME/ftplugin/j.vim
    $VIMRUNTIME/ftplugin/mf.vim
    $VIMRUNTIME/ftplugin/mp.vim
    $VIMRUNTIME/ftplugin/vb.vim
    $VIMRUNTIME/ftplugin/vhdl.vim

    $VIMRUNTIME/ftplugin/rust.vim
    $VIMRUNTIME/ftplugin/changelog.vim
    $VIMRUNTIME/ftplugin/php.vim

