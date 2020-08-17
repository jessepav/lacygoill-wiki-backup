# :def
## Why is a `:def` function compiled?

So that its execution is faster.
In practice, it's often 10 to 100 times faster.

You can't get that kind of performance with a `:fu` function.

### When is it compiled?

   - when the function is first called
   - when `:defcompile` is executed in the script where the function is defined (*)
   - when it's disassembled by `:disassemble`

(*) Note that this is true only if the function was defined earlier:
```vim
vim9script
defcompile
def Func()
    let x: string
    let x: number
enddef
```
The previous doesn't raise any error, even though we try to change the type of a
variable which is not allowed.  This means that `Func()` was not compiled.
Had you  moved `:defcompile` *after* `Func()`,  an error would have  been raised
during type checking which itself occurs during the compilation:
```vim
vim9script
def Func()
    let x: string
    let x: number
enddef
defcompile
```
    E1017: Variable already declared: x~

##
## What is type checking?

The parsing step during the compilation of a `:def` function when Vim checks whether:

   - you've specified a type for each function argument
     (not needed for an argument which is assigned a default value)

         $ vim -Nu NONE -S <(cat <<'EOF'
             def Func(x)
             enddef
             defcompile
         EOF
         )

         E1077: Missing argument type for x~

   - you've specified the return type of the function if it returns sth

         $ vim -Nu NONE -S <(cat <<'EOF'
             def Func()
                 return 123
             enddef
             defcompile
         EOF
         )

         E1096: Returning a value in a function without a return type~

   - the return type of the function matches the type of the returned expression

         $ vim -Nu NONE -S <(cat <<'EOF'
             def Func(): string
                 return 123
             enddef
             defcompile
         EOF
         )

         E1013: type mismatch, expected string but got number~

   - the type of a declared variable matches the type of the expression that you assign it later

         $ vim -Nu NONE -S <(cat <<'EOF'
             def Func()
                 let x: string
                 x = 123
             enddef
             defcompile
         EOF
         )

         E1013: type mismatch, expected string but got number~

### When is type checking performed
#### for a legacy `:fu` function?

At runtime.

#### for a `:def` function?

At compile time.

###
### How to postpone type checking for a `:def` function to runtime?

Whenever you need to specify a type, use `any`:

    $ vim -Nu NONE -S <(cat <<'EOF'
        def Func(x: any)
        #         ^---^
        enddef
        defcompile
    EOF
    )

    $ vim -Nu NONE -S <(cat <<'EOF'
        def Func(): any
        #         ^---^
            return 123
        enddef
        defcompile
    EOF
    )

    $ vim -Nu NONE -S <(cat <<'EOF'
        def Func()
            let x: any
            #    ^---^
            x = 123
        enddef
        defcompile
    EOF
    )

##
## If a `:def` function contains a syntax or type error, when does Vim raise an error?

At compile time.  That is, when `:defcompile` is run, or when the function is first called.

It does not raise any error at runtime, because its whole body is then emptied.

Example of a function containing a type error:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def g:Func()
            let x = 1 + {}
            echo x
        enddef
    EOF
    )

    :def Func
        def Func()~
     1          let x = 1 + {}~
     2          echo x~
        enddef~

    :call Func()
    E1051: wrong argument type for +~

    :def Func
    function Func()~
    endfunction~

Example of a function containing a syntax error:

    :def Func
        def Func()~
     1          echo 'before error'~
     2          invalid~
     3          echo 'after error'~
        enddef~

    :call Func()
    E476: Invalid command: invalid~

    :def Func
    function Func()~
    endfunction~

## What's the Vim9 equivalent of `let x = get(a:, 1, 3)`?

It's:

    def Func(x = 3)
             ^---^

Remember that an argument can be specified in 3 ways:

    {name}: {type}
    {name} = {value}
    {name}: {type} = {value}

The first one is for mandatory arguments; the last two for optional ones.

##
## Where does Vim look for a function whose name is not prefixed with `s:` nor `g:`?

Vim looks in:

   - the current block, if there is one
   - the outer block, if there is one; the process repeats itself as long as there is an outer block
   - the outer function, if there is one
   - the script
   - the imported functions

For more info, see `:h vim9-scopes`:

   > When referring to a function and no "s:" or "g:" prefix is used, Vim will
   > search for the function in this order:
   > - Local to the current scope and outer scopes up to the function scope.
   > - Local to the current script file.
   > - Imported functions, see `:import`.

---
```vim
vim9script
def Outer()
    if 1
        def Inner()
            echo 'inner'
        enddef
        Inner()
    endif
enddef
Outer()
```
    inner

This shows that Vim  looks for a function invoked from a  function block, in the
block namespace.

---
```vim
vim9script
def Outer()
    if 1
        def Inner()
            echo 'inner'
        enddef
        if 1
            Inner()
        endif
    endif
enddef
Outer()
```
    inner

This shows  that Vim can  look for a function  invoked from a  *nested* function
block, in the outer block namespace.

---
```vim
vim9script
def Outer()
    def Inner()
        echo 'inner'
    enddef
    Inner()
enddef
Outer()
```
    inner

This shows that Vim  looks for a function invoked from  another function, in the
immediate outer function namespace.

---
```vim
vim9script
def Func()
enddef
fu Func
```
        v-----v
    def <SNR>1_Func()
    enddef

This shows that  Vim looks for a  function invoked from the script  level in the
script namespace.

---
```vim
vim9script
mkdir('/tmp/import', 'p')
let lines =<< trim END
    vim9script
    export def Func()
        echo 'imported'
    enddef
END
writefile(lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import Func from 'foo.vim'
Func()
```
This shows that Vim can look for a function invoked from the script level in the
imported namespace.

####
## When can I delete a `:def` function?

Always, except if it's local to a Vim9 script.
```vim
vim9script
def s:Func()
enddef
delfu s:Func
```
    E1084: Cannot delete Vim9 script function s:Func
```vim
vim9script
def g:Func()
enddef
delfu g:Func
```
✔
```vim
def s:Func()
enddef
delfu s:Func
```
✔
```vim
def g:Func()
enddef
delfu g:Func
```
✔

### What about a `:fu` function?

Same answer: always, except if it's local to a Vim9 script.
```vim
vim9script
fu s:Func()
endfu
delfu s:Func
```
    E1084: Cannot delete Vim9 script function s:Func
```vim
vim9script
fu g:Func()
endfu
delfu g:Func
```
✔
```vim
fu s:Func()
endfu
delfu s:Func
```
✔
```vim
fu g:Func()
endfu
delfu g:Func
```
✔

##
## The following snippet raises `E477` and `E193`:
```vim
vim9script
def Func()
    echom 'one'
enddef
def! Func()
    echom 'two'
enddef
Func()
```
    E477: No ! allowed~
    two~
    E193: :enddef not inside a function~
    one~

### Why?

You can't replace a script-local function.

   > In Vim9 script, script-local functions are defined once when the script is sourced
   > and cannot be deleted or replaced.

This explains why `E477` is raised.
As  a  result, `:def!`  does  not  start a  function  definition,  and the  next
`:enddef` does not match any `:def`; this explains `E193`.

### Ok.  But why are the bodies of the 2 function definitions executed in reverse order?

The second  `echom` is *not*  parsed inside  a function (because  `:def!` raised
`E477`); it's parsed at the script level, and executed immediately.

Later, `Func()` is run.

##
# Comments
## Which comment leader should I write to start a comment in a Vim9 script code?

`#`

    let count = 0  # number of occurences

### Why not the traditional `"`?

It can also be the start of a string, so it can't be used in many places.

### Which pitfall should I avoid?

Don't write `{` right after `#`:

    #{some comment
    ^^
    ✘

It would raise `E488` because `#{` is  the start of a "literal" dictionary (i.e.
a dictionary whose keys must not be quoted).

Anyway, you should always add a space after `#` to make the comment more readable:

    #some comment
    ^^
    hard to read

    # some comment
    ^^
    easy to read

So it's only a theoretical pitfall.

##
## Which comment leader can I use
### at the start of a line (whole comment) or at the end of a line of code (inline comment)?

It's simple: you can use `"` in (and only in) legacy Vim script, and `#` in (and
only in) Vim9 script.

Legacy Vim script = script which does not start with `vim9script` or inside `:fu` function.
Vim9 script = script which *does* start with `vim9script` or inside `:def` function.

### at the start of an automatic line continuation?

You can  only use `#` inside  a `:def` function, or  at the script level  if the
latter starts with `:vim9script`.

    vim9script
    def Func()
        let mylist = [
                'one',
                # some comment
                'two',
                ]
        echo mylist
    enddef
    Func()

    ['one', 'two']~

    def Func()
        let mylist = [
                'one',
                # some comment
                'two',
                ]
        echo mylist
    enddef
    call Func()

    ['one', 'two']~

    vim9script
    let mylist = [
            'one',
            # some comment
            'two',
            ]
    echo mylist

    ['one', 'two']~

Everywhere else, neither `"` nor `#` work.

##
# Export
## Which items can be exported?  (4)

   - constants
   - variables
   - `:def` functions
   - classes

See `:h :export`.

## How to export an item?

Prefix the command which defines it with `:export`:

Example for a constant:

    vim9script
    export const MYCONST = 123
    ^----^

Example for a variable:

    vim9script
    export let var = 'test'
    ^----^

Example for a function:

    vim9script
    # v--v
    export def Func()
        # ...
    enddef

##
## On which condition can I
### export items in a script?

The script must start with `:vim9script`.

    export const MYCONST = 123

    E1042: export can only be used in vim9script~

    vim9script
    export const MYCONST = 123
    ✔

### import items from a script?

None.
In particular, you can import items even while you're in a legacy Vim script.
IOW, your script doesn't need to start with `:vim9script`.

    $ cat <<'EOF' >/tmp/.a.vim
      vim9script
      export const MYCONST = 123
    EOF

    $ cat <<'EOF' >/tmp/.b.vim
        import MYCONST from '/tmp/.a.vim'
        echo s:MYCONST
    EOF

    $ vim -Nu NONE -S /tmp/.a.vim -S /tmp/.b.vim

    123~

##
## After sourcing a Vim9 script from a legacy script, which items can I refer to?

Only the items defined in the `b:`, `g:`, `t:`, `w:` namespaces can be used; not
the ones defined in the `s:` namespace, nor the exported items.

    $ cat <<'EOF' >/tmp/exported.vim
        vim9script
        export const MYCONST = 123
    EOF

    $ cat <<'EOF' >/tmp/legacy.vim
        source /tmp/exported.vim
        echo MYCONST
    EOF

    $ vim -Nu NONE -S /tmp/legacy.vim

    E121: Undefined variable: MYCONST~

Here, the legacy script fails to refer  to `MYCONST`, even after sourcing a Vim9
script which  exports the latter  variable; that's because  it was local  to the
Vim9 script.

    $ cat <<'EOF' >/tmp/exported.vim
        vim9script
        g:global = 456
    EOF

    $ cat <<'EOF' >/tmp/legacy.vim
        source /tmp/exported.vim
        echo g:global
    EOF

    $ vim -Nu NONE -S /tmp/legacy.vim

    456~

Here,  the legacy  script  *can*  refer to  `g:global`,  because  it's a  global
variable; not a variable local to the Vim9 script.

## Which items can be exported without being script-local?

Only functions and classes.

Indeed, you can't  export a public constant or variable,  because you can't even
declare it:
```vim
vim9script
let g:var = 123
```
    E1016: Cannot declare a global variable: g:var

So you can't export it either:
```vim
vim9script
export let g:var = 123
```
    E1016: Cannot declare a global variable: g:var
    E1044: export with invalid argument

Btw, when I said "public constant or variable", I meant any constant or variable
that is  not in a  namespace restricted to one  single script (i.e.  `b:`, `g:`,
`t:`, `w:`); as  a result, your script has  no guarantee that if it  sets such a
constant/variable, it won't be overwritten by another script.

##
# Import
## How to import one item from a file which is
### in the same directory as the current script?

           name of the item you want to import
           v-----v
    import MYCONST from './foo.vim'
                        ^---------^
                        location of the script where the item is defined,
                        relative to the directory of the current script

Example:

    $ cat <<'EOF' >/tmp/foo.vim
        vim9script
        export const MYCONST = 'from a script in current directory'
    EOF

    $ cat <<'EOF' >/tmp/bar.vim
        vim9script
        import MYCONST from './foo.vim'
        echo MYCONST
    EOF

    $ vim -Nu NONE -S /tmp/foo.vim -S /tmp/bar.vim

    from a script in current directory~

### in the *parent* directory of the current script?

    import MYCONST from '../foo.vim'
                         ^^

Example:

    $ mkdir -p /tmp/dir

    $ cat <<'EOF' >/tmp/foo.vim
        vim9script
        export const MYCONST = 'from a script in parent directory'
    EOF

    $ cat <<'EOF' >/tmp/dir/bar.vim
        vim9script
        import MYCONST from '../foo.vim'
        echo MYCONST
    EOF

    $ vim -Nu NONE -S /tmp/foo.vim -S /tmp/dir/bar.vim

    from a script in parent directory~

### at an arbitrary location?

Use a full file path:

    import MYCONST from '/path/to/script.vim'
                         ^-----------------^

Example:

    $ cat <<'EOF' >/tmp/foo.vim
        vim9script
        export const MYCONST = 'from /tmp/foo.vim'
    EOF

    $ cat <<'EOF' >/tmp/bar.vim
        vim9script
        import MYCONST from '/tmp/foo.vim'
        echo MYCONST
    EOF

    $ vim -Nu NONE -S /tmp/foo.vim -S /tmp/bar.vim

    from /tmp/foo.vim~

###
### Suppose I write this:

    import MYCONST from 'foo.vim'
                         ^-----^

#### Where will Vim look for `foo.vim`?

In an import subdirectory of the runtimepath.

Example:

    $ mkdir -p /tmp/import

    $ cat <<'EOF' >/tmp/import/foo.vim
        vim9script
        export const MYCONST = 'from foo.vim in import/ subdir'
    EOF

    $ cat <<'EOF' >/tmp/bar.vim
        vim9script
        set rtp^=/tmp
        import MYCONST from 'foo.vim'
        echo MYCONST
    EOF

    $ vim -Nu NONE -S /tmp/bar.vim

    from foo.vim in import/ subdir~

---

Note that  you're not limited  to scripts directly at  the root of  an `import/`
subdirectory.  You can  put your scripts under an arbitrarily  deep hierarchy of
subdirectories.

Example:

    $ mkdir -p /tmp/import/foo/bar

    $ cat <<'EOF' >/tmp/import/foo/bar/baz.vim
        vim9script
        export const MYCONST = 'from foo/bar/baz.vim in import/ subdir'
    EOF

    $ cat <<'EOF' >/tmp/qux.vim
        vim9script
        set rtp^=/tmp
        import MYCONST from 'foo/bar/baz.vim'
        echo MYCONST
    EOF

    $ vim -Nu NONE -S /tmp/qux.vim

    from foo/bar/baz.vim in import/ subdir~

#### Which pitfall should I be aware of when choosing a name for `foo.vim`?

You want a name  which is unique across all the  `import/` subdirectories of the
runtimepath.  Otherwise, there is a risk for Vim to load the wrong file.

###
## In practice, on which occasion will I import items from a script which is
### in the same directory as the current script, or in the parent directory?

When you want to split up a large plugin into several files.

### in an arbitrary location?

Rarely, if ever.

### in an `import/` subdirectory?

When you want the items to be available from different plugins.
This is useful to implement library functions.

###
## How to import multiple items at the same time?

Wrap their names inside curly brackets:

    import {MYCONST, var, Func} from 'foo.vim'
           ^------------------^

## How to import an item under a new arbitrary name?

Use the keyword `as` followed by the desired new name:

    import MYCONST as NEWCONST from 'foo.vim'
                   ^---------^

This is  useful when  the original  name can  collide with  the name  of another
existing item.

---

Note that this has not been implemented yet.
See `:h todo /as Name`:

   > - Implement "as Name" in "import Item as Name from ..."

Also, this is supposed to work even inside curly brackets.
So, you should be able to write something like:

    import {MYCONST, var, Func as NewFunc} from 'foo.vim'
                               ^--------^

## How to import all exported items under a specific identifier?

Use the `*` wildcard and the `as` keyword:

    import * as foo from 'foo.vim'
           ^------^

Then,  you  can  refer  to  the imported  items  via  `foo.MYCONST`,  `foo.var`,
`foo.Func`, etc.

You are free to import the exported items under any arbitrary identifier, but it
is highly recommended  to use the name  of the script from which  the items were
imported, to avoid confusion.

##
## What happens if I use `:import` in a legacy Vim script?

It will be automatically put inside the script-local `s:` namespace.

So, to refer to it later, you'll need to specify `s:`:

    import MYCONST from './exported.vim'
    echo MYCONST
         ^-----^
         ✘

    import MYCONST from './exported.vim'
    echo s:MYCONST
         ^-------^
         ✔

Working example:

    $ cat <<'EOF' >/tmp/exported.vim
        vim9script
        export const MYCONST = 123
    EOF

    $ cat <<'EOF' >/tmp/import.vim
        import MYCONST from './exported.vim'
        echo s:MYCONST
        "    ^^
    EOF

    $ vim -Nu NONE -S /tmp/import.vim

    123~

Notice how we had to prefix `MYCONST` with `s:` in `import.vim`.
Without, when executing  `:echo MYCONST` afterward, Vim would  have searched for
the constant in the global namespace; and after failing to find it, `E121` would
have been raised.

##
# Misc
## Where can I write Vim9 script code?  (2)

In a function defined with the `:def` command (instead of `:function`).

Or, in a file whose first command is `:vim9script`.

## What are the effects of `:vim9script`?  (2)

It  makes Vim  put all  variables  and functions  defined  in the  script, in  a
namespace specific  to the latter.   As a result, you  don't need to  write `s:`
anymore; it's implicit.

In Vim script legacy:

    let s:var = 123
    fu s:LegacyFunc()
    endfu
    def s:Vim9Func()
    enddef

    echo s:var
    fu s:LegacyFunc
    def s:Vim9Func

In Vim9:

    vim9script
    let var = 123
    fu LegacyFunc()
    endfu
    def Vim9Func()
    enddef

    echo var
    fu LegacyFunc
    def Vim9Func

Unless you explicitly specify another namespace:

    vim9script
    g:var = 123
    def g:Func()
    enddef

Or a function name contains a `#`:

    $ mkdir -p /tmp/some/autoload

    $ cat <<'EOF' >/tmp/some/autoload/some.vim
        vim9script
        def some#func()
        enddef
    EOF

    $ vim -Nu NORC --cmd 'set rtp^=/tmp/some'
    :call some#func()
    :def some#func
    def some#func~
    enddef~
    " notice how we didn't need <SNR> when calling the function,
    " and how there is no <SNR> in the header of the function definition as reported by ":def"

---

It makes Vim temporarily reset `'cpo'` to its default Vim value.
It's somewhat equivalent to:

    let s:cpo_save = &cpo
    set cpo&vim
    ...
    let &cpo = s:cpo_save
    unlet s:cpo_save

##
## Which difference is there between a legacy `s:var` and a Vim9 `var` defined at the script level?

Legacy's `s:var` can be unlet; not Vim9's `var`:

    vim9script
    let var = 123
    unlet var

    E1081: Cannot unlet var~

## In Vim9 script, what's the main difference between a `b:`, `g:`, `t:`, `w:`, `$` variable and other variables?

Variables which are prefixed by a prefix denoting a scope can't be declared, but
can be deleted:

    vim9script
    let b:var = 123

    E1016: Cannot declare a buffer variable: b:var~

    vim9script
    b:var = 123
    unlet b:var
    ✔

Variables  which are  *not* prefixed  by a  scope (block-local,  function-local,
script-local) *can* be declared, but can't be deleted.

    vim9script
    def Func()
        if 1
            let var = 'block-local'
            unlet var
        endif
    enddef
    defcompile

    E1081: Cannot unlet var~

    vim9script
    def Func()
        let var = 'function-local'
        unlet var
    enddef
    defcompile

    E1081: Cannot unlet var~

    vim9script
    let var = 'script-local'
    unlet var

    E1081: Cannot unlet var~

---

See `:h vim9-declaration /Global`:

   > Global, window, tab, buffer and Vim variables can only be used
   > without `:let`, because they are are not really declared, they can also be
   > deleted with `:unlet`.

## How to prevent a variable from being accessible in a later statement?

Put it inside a `{}` block:

    vim9script
    def Func()
        {
            let n = 123
        }
        echo n
    enddef
    defcompile

    E1001: variable not found: n~

##
## When can I omit the type of a variable?

When you assign it a value, because in that case Vim can infer the type from the latter.

Here, `E1077` is raised because `x` is not assigned a value:

    vim9script
    def Func(x)
    enddef
    defcompile

    E1077: Missing argument type for x~

Solution: declare the type.

    vim9script
    def Func(x: number)
    enddef
    defcompile

---

Here, no error is raised, because `x` is assigned a default value:

    vim9script
    def Func(x = 3)
    enddef
    defcompile

And here again, no error is raised, because `x` is assigned a value:

    vim9script
    def Func()
        let x = 3
    enddef
    defcompile

See `:h type-inference`.

##
## What's the evaluation of `123 || 0` in
### legacy Vim script?

    echo 123 || 0

    1~

### Vim9 script?

    vim9script
    echo 123 || 0

    123~

##
## How is `expr1 && expr2` evaluated in Vim9 script?

Some types have a "neutral" value:

   - Number: 0
   - Float: 0.0
   - String: ''
   - List: []
   - Dictionary: {}
   - None: v:none

The second operand always wins, unless the first one is neutral; then the latter
wins.

### What about `expr1 || expr2`?

The first operand always wins, unless the second one is neutral; then the latter
wins.

##
## `:h vim9` says that `'ignorecase'` is not used for comparators that use strings.

From `:h vim9 /comparators`:

   > Comparators ~
   >
   > The 'ignorecase' option is not used for comparators that use strings.

### And yet, we can still use `=~#` and `=~?`.  Doesn't this contradict the previous help excerpt?

No, because neither `=~#` nor `=~?` inspect the value of `'ignorecase'`.
They don't care how the user configured the option.
```vim
vim9script
set noic
def Func()
    echo 'abc' =~? 'ABC'
enddef
Func()
```
    v:true

##
# Pitfalls
## My function prints an unexpected error message!  (an error is missing, the order of the errors looks wrong, ...)

Your error message is probably correct.
You have to remember that an error can  be raised at compile time or at runtime,
and that the latter step occurs after the former.

To be sure, write `:defcompile` at the end of your script.

---

As an example, consider this snippet:
```vim
vim9script
def Func(numbers: float)
    for n in numbers
    endfor
enddef
Func([1, 2, 3])
```
    E1013: type mismatch, expected list<any> but got float
                          ^------------------------------^

You might think the error message is wrong, and instead expect this one:

    E1013: type mismatch, expected list<any> but got float
                          ^------------------------------^

But the error message is fine.  It's raised at compile time, not at runtime.
You can check this by writing `:defcompile` at the end:
```vim
vim9script
def Func(numbers: float)
    for n in numbers
    endfor
enddef
defcompile
```
    E1013: type mismatch, expected list<any> but got float
                          ^------------------------------^

And at compile  time, `Func()` hasn't been passed any  value yet.  Besides, when
Vim has  to compile the `:for`  command, it detects  an error: `for ...  in` can
only iterate over a  list, but `numbers` is declared with  the float type, which
doesn't match.

## My try conditional does not catch an error!

Does it look like this?
```vim
vim9script
def Func()
    try
        invalid
    catch
        echom 'caught'
    endtry
enddef
Func()
```
    E476: Invalid command: invalid

If so, it's not a bug.  The error is raised at compile time, not at runtime.
You can check this by replacing `Func()` with `:defcompile`:
```vim
vim9script
def Func()
    try
        invalid
    catch
        echom 'caught'
    endtry
enddef
defcompile
```
    E476: Invalid command: invalid

Notice how the error is raised again, even though `Func()` was not executed.

Explanation:
At compile time, Vim  doesn't care about the logic of  your code; *all* commands
are  parsed and  compiled.  And  if  Vim finds  a  command which  it can  easily
determine as invalid (unknown, wrong syntax, wrong argument type, ...), an error
must be raised.  You  can only catch such an error  from *outside* the function;
so that the function's compilation  (explicit via `:defcompile`, or implicit via
`Func()`) is inside the `try` conditional.
```vim
vim9script
def Func()
    invalid
enddef
try
    defcompile
catch
    echom 'caught'
endtry
```
Note that Vim  cannot detect *any* type  of invalid command; only  some of them.
For example, at compile time, Vim does not detect that a command is invalid even
if it refers to a non-existing member from a list:
```vim
vim9script
def Func()
    echo [1, 2, 3][4]
enddef
defcompile
```
Even though the `:echo` command is wrong – i.e. it will always raise an error at
runtime – no error is raised by the previous snippet.
Vim will only raise an error at runtime.

##
## When I try to assign a value to a list or a dictionary, an error is raised unexpectedly!
```vim
vim9script
let l = [1 , 2 , 3]
```
    E696: Missing comma in List: , 2, 3]

In a list or dictionary, the usage of white space is strict:

   - you *can* write a white space after the opening `[` or `{`, and before the closing `]` or `}`

   - you *cannot* write a white space before a comma separating two consecutive items,
     nor after a colon separating a key from its value in a dictionary

   - you *must* write a white space after a comma separating two consecutive items

Example:

                ok but useless
                v                 v
    let dict = { 'a' : 1 , 'b' : 2 }
                    ^ ^ ^ ^   ^ ^
                    ✘ ✔ ✘ ✔   ✘ ✔

                    ✘ = cannot be written
                    ✔ = must be written

Remove the wrong white space:
```vim
vim9script
let dict = {'a': 1, 'b': 2}
```
    ✔

Some (all?) of these rules were introduced in 8.2.1326.

## If I specify the return type of a custom function, what should I pay attention to?

If your function  returns a variable, make  sure that it was set  with the exact
same type:

    vim9script
    def Func(): list<string>
    #           ^----------^
        let l = []
    #   ^--------^
    #   ✘
        return l
    enddef
    defcompile

    E1013: type mismatch, expected list<string> but got list<any>~

The error probably comes from the fact that when Vim parses this line:

    let l = []

it probably infers the type `list<any>`.

Fix:

    vim9script
    def Func(): list<string>
        let l: list<string> = []
        #    ^------------^
        #          ✔
        return l
    enddef
    defcompile

## Vim unexpectedly populates the arglist when I call a function where I omit to declare an `n` variable!

`n` is a valid Ex command (it's the abbreviated form of `:next`).
So this is expected:

    vim9script
    def Func()
        n = 123
    enddef
    Func()
    args

Solution: don't forget to declare your variable:

    vim9script
    def Func()
        let n = 123
    enddef
    Func()
    args

---

The same issue applies to other single-letter variable names:

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

##
## My eval string can't access variables in the outer function scope!

    vim9script
    def Func()
        let l = ['aaa', 'bbb', 'ccc', 'ddd']
        range(1, 2)->map('l[v:val]')
        #                ^--------^
        #                    ✘
    enddef
    Func()

    E121: Undefined variable: l~

Solution: use a lambda.

    vim9script
    def Func()
        let l = ['aaa', 'bbb', 'ccc', 'ddd']
        range(1, 2)->map({_, v -> v})
    enddef
    Func()

---

The issue is due to:

   > The local variables are on the stack  and cannot be accessed outside of the
   > compiled function.

Source: <https://github.com/vim/vim/issues/6401#issuecomment-655071515>

## I hesitate between writing a lambda and an eval string.  Which one is the fastest?

Inside a `:def` function, lambdas are significantly faster:

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        vim9script

        def Lambda()
            let time = reltime()
            range(999999)->map({_, v-> v + 1})
            setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run lambdas')
        enddef
        Lambda()

        def EvalString()
            let time = reltime()
            range(999999)->map('v:val+1')
            setline(2, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run eval strings')
        enddef
        EvalString()

        :%p
        qa!
    EOF
    )

    0.393 seconds to run lambdas~
    0.596 seconds to run eval strings~

But at the script level, lambdas are significantly slower:

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        vim9script

        let time = reltime()
        range(999999)->map({_, v-> v + 1})
        setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run lambdas')

        let _time = reltime()
        range(999999)->map('v:val+1')
        setline(2, reltime(_time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run eval strings')

        :%p
        qa!
    EOF
    )

    1.225 seconds to run lambdas~
    0.566 seconds to run eval strings~

Conclusion: always use lambdas, but make sure to write them inside `:def` functions.

##
## Vim complains that it doesn't know the function-local variable I'm referring to!

    vim9script
    def Func()
        if 1
           let n = 123
        endif
        echo n
    enddef
    defcompile

    E1001: variable not found: n~

A variable is local to its current block.

Solution:  Declare it *before* the block where it's assigned a value.

    vim9script
    def Func()
        let n: number
        if 1
           n = 123
        endif
        echo n
    enddef
    defcompile

This makes  the variable  accessible in  the block where  it's declared  (and in
nested blocks).  Not in outer blocks:

    vim9script
    def Func()
        if 1
            let n: number
            if 1
               n = 123
            endif
        endif
        echo n
    enddef
    defcompile

    E1001: variable not found: n~

### Now it complains about a script-local variable!

    vim9script
    def Func()
        echo s:var
    enddef
    defcompile
    s:var = 123

    E1050: Item not found: var~

Make sure your script-local variable is defined *before* the function – in which
it's referred to – is compiled.

    vim9script
    def Func()
        echo s:var
    enddef
    s:var = 123
    defcompile
    ✔

From `:h fast-functions /prefix`:

   > If the script the function is defined in is Vim9 script, then script-local
   > variables can be accessed without the "s:" prefix.  **They must be defined**
   > **before the function is compiled**.

##
## The line number given in an error message looks wrong!

It's not wrong.

You need to pay attention to the context in which the error is raised:

    Error detected while processing ...:~
                                    ^-^
                                    context

Is it raised while processing a file?
Or is it raised while processing a function?

Here is an example where you may find the line number of the error unexpected:

    set qftf=QuickFixTextFunc
    def QuickFixTextFunc(info: dict<number>): list<any>
        let qfl: list<any>
        qfl = [{}]
        return qfl
    enddef
    helpg grail
    copen

    Error detected while processing /proc/2212/fd/11:~
    line    8:~
    E731: using Dictionary as a String~

Instead of line 8, you may have expected line 2, which is the address of:

    qfl = [{}]

inside the `QuickFixTextFunc()` function.

First, let's explain the error.

`QuickFixTextFunc()`  is called  to determine  how the  quickfix list  should be
displayed in  the quickfix  window.  It  should return a  list of  strings.  But
here, you  return a list containing  a dictionary.  The dictionary  type doesn't
match the expected string type, hence the error.

Now, Vim doesn't  call the function until  it has to display  the quickfix list;
that is, until `:copen` is executed.  So, from Vim's point of view, the error is
raised from `:copen`, which is on line 8 *in the script*.

Notice how the  first line in the  error messages refers to the  script, not the
function:

    Error detected while processing /proc/2212/fd/11:~
                                    ^--------------^

---

Here's  another example,  where  the  line number  of  the  error looks  correct
immediately:

    set qftf=QuickFixTextFunc
    def QuickFixTextFunc(info: dict<number>): list<any>
        let qfl: list<any>
        qfl = v:true
        return qfl
    enddef
    helpg grail
    copen

    Error detected while processing function QuickFixTextFunc:~
    line    2:~
    E1013: type mismatch, expected list<any> but got bool~

Again, let's first explain the error.

It's  simple;  you  declare  a  variable `qlf`  of  type  `list<any>`,  but  you
immediately try  to assign  it a  boolean.  The boolean  type doesn't  match the
expected list type, hence the error.

Now, notice how –  this time – the first line in the  error messages refers to a
function:

    Error detected while processing function QuickFixTextFunc:~
                                    ^-----------------------^

## I can't call a `:def` function from a `:fu` one.  The function is not found!

    vim9script
    fu Foo()
        call Bar()
    endfu
    def Bar()
        echo 'bar'
    enddef
    Foo()

    E117: Unknown function: Bar~

You forgot the `s:` scope in your legacy function:

        call s:Bar()
             ^^

Fixed code:

    vim9script
    fu Foo()
        call s:Bar()
    endfu
    def Bar()
        echo 'bar'
    enddef
    Foo()

    bar~

Explanation: you can omit `s:` when:

   - defining a `:def` function
   - defining a `:fu` function
   - calling a script-local function from a `:def` function

But you can *not*  omit `s:` when calling a script-local  function from a legacy
function.

##
## After importing items from a script, I've updated the latter and re-imported the items.

    $ cat <<'EOF' >/tmp/exported.vim
        vim9script
        export const MYCONST = 123
    EOF

    $ cat <<'EOF' >/tmp/import.vim
        vim9script
        import MYCONST from './exported.vim'
        echo MYCONST
    EOF

    $ cat <<'EOF' >/tmp/update.vim
        sil e /tmp/exported.vim
        %s/123/456/
        sil w
    EOF

    $ vim -Nu NONE -S /tmp/import.vim -S /tmp/update.vim -S /tmp/import.vim

    123~
    123~

### Their definitions has not changed!  Why?

Once a  Vim9 script file has  been imported, the  result is cached and  used the
next time the same script is imported.  It will not be read again.

To see the effects of your update, simply restart Vim:

    $ vim -Nu NONE -S /tmp/import.vim

    456~

##
## My global command is wrongly parsed as the `g:` global namespace!

You've probably used a colon to surround the pattern of your global command:

    ✘
    g:pat:do sth
     ^   ^

And you  probably did that  because your pattern contained  one or a  few colons
which you didn't want to escape.

Solutions:

Prefix the global command with a colon:

    ✔
    :g:pat:do sth
    ^

Or add a space in between `g` and `:`:

    g :pat:do sth
     ^

Or use the full name of the command:

    global:pat:do sth
    ^----^

---

It's a known issue which won't be fixed: <https://github.com/vim/vim/issues/6593>

##
# Todo
## To refactor:
### try to move all our library functions (`vim-lg`) into an `import/` subdirectory

Benefit: our function calls would no longer be littered with noisy prefix.

Before:

    call lg#textprop#ansi()
         ^----------^
         noise

After:

    call ansi()

Obviously, you would need to prefix the functions definitions with `:export`.
And you would need to import them in any plugin where they are required.
But the end result will still be much more readable.

---

Also, try to refactor imports from the same script into a single command:

    ✘
    import This from 'foo.vim'
    import That from 'foo.vim'

    ✔
    import {This,That} from 'foo.vim'

### eval strings into lambdas

But make sure they're inside a `:def` function first.
Don't worry, a lambda in a `:def` function is not slower than an eval string; on
the contrary, it's faster.

    :vim /v:val/gj $MYVIMRC ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/**
    :Cfilter! -other_plugins

### prefix all `:import` commands with `:silent!`?

And what about the imported functions?
When we call them,  should we prefix the calls with `:silent!`  too, in case the
import failed?

Or maybe we should use a try conditional.
If the imported functions are not available,  bail out at the top of the script,
because there is no guarantee it will work as expected.

See what we did in:

    ~/.vim/plugged/vim-repmap/autoload/repmap/make.vim

If you do use try conditionals, you can remove `:silent!` everywhere.

Update:  It might not be necessary in the future:

   > - Error in any command in "vim9script" aborts sourcing.

Source: `:h todo /abort`
Although, that  would require that  the script from which  you import is  a Vim9
script (i.e. first statement is `vim9script`).

### should we refactor every manual sourcing of an autoload script into an autoload function call?

    ✘
    :ru autoload/path/to/script.vim
    :so autoload/path/to/script.vim

    ✔
    :call path#to#script#_()

Rationale: It could avoid this issue:
<https://github.com/vim/vim/issues/6644>

Update: no longer needed.  The issue was fixed.

---

In any case, manually sourcing an autoload script looks wrong.
At the very  least, we should consider  moving anything which is  not a function
into a separate directory which is not automatically sourced (`macros/`?).
That would apply to our function calls installing mappings in `vim-toggle-settings`.

##
## To understand:
### How to change the type of a variable?

    vim9script
    let time = reltime()
    sleep 1
    let time = reltime(time)->reltimestr()->matchstr('.*\..\{,3}')
    echom printf('we slept for %s seconds', time)

    E1041: Redefining script item time~

---

For the moment, the only workaround I can think of, is to use an extra variable:

    vim9script
    let time = reltime()
    sleep 1
    let _time = reltime(time)->reltimestr()->matchstr('.*\..\{,3}')
    echom printf('we slept for %s seconds', _time)

### Can we import a global function?

Last time I tried, it didn't work.

##
## To document:
### string indexes are counted in characters

<https://github.com/vim/vim/commit/e3c37d8ebf9dbbf210fde4a5fb28eb1f2a492a34>

### cannot shadow a function from a less specific namespace

For example,  a function-local  function cannot  shadow a  script-local function
even in the context of the function where it's defined.
Find examples.

However, I think it is allowed to shadow a global function.
After all, we can  already do that in Vim script legacy;  so maybe this decision
was done for consistency...

---
```vim
vim9script
def Outer()
    def Func()
        echo 'function-local'
    enddef
    if 1
        def Func()
            echo 'block-local'
        enddef
    endif
enddef
Outer()
```
    E1073: name already defined: Func()

---

We can't shadow a script-level function with a function-local one:
```vim
vim9script
def Func()
    echo 'script level'
enddef
def Outer()
    def Func()
        echo 'function-local'
    enddef
    Func()
enddef
Outer()
```
    E1073: name already defined: Func()

---

We can't shadow an imported function with a script-local one:
```vim
vim9script
mkdir('/tmp/import', 'p')
let lines =<< trim END
    vim9script
    export def Func()
        echo 'imported'
    enddef
END
writefile(lines, '/tmp/import/foo.vim')
set rtp+=/tmp
def Func()
    echo 'script level'
enddef
import Func from 'foo.vim'
```
    E1073: name already defined: Func

### cannot redefine a block-local or function-local or script-local or imported function
```vim
 # block-local
vim9script
def Outer()
    if 1
        def Inner()
            echo 'first'
        enddef
        def Inner()
            echo 'second'
        enddef
        Inner()
    endif
enddef
Outer()
```
    E1073: name already defined: Inner()
```vim
 # function-local
vim9script
def Outer()
    def Inner()
        echo 'first'
    enddef
    def Inner()
        echo 'second'
    enddef
    Inner()
enddef
Outer()
```
    E1073: name already defined: Inner()
```vim
 # script-local
vim9script
def Func()
    echo 'first'
enddef
def Func()
    echo 'second'
enddef
```
    E1073: name already defined: <SNR>1_Func
```vim
 # imported
vim9script
mkdir('/tmp/import', 'p')

let lines =<< trim END
    vim9script
    export def Func()
        echo 'first'
    enddef
END
writefile(lines, '/tmp/import/a.vim')

lines =<< trim END
    vim9script
    export def Func()
        echo 'second'
    enddef
END
writefile(lines, '/tmp/import/b.vim')

set rtp+=/tmp
import Func from 'a.vim'
import Func from 'b.vim'
```
    E1073: name already defined: Func

### a block-local function is inherited by all nested blocks
```vim
vim9script
def Outer()
    if 1
        def Inner()
            echo 'inner'
        enddef
        if 1
            Inner()
        endif
    endif
enddef
Outer()
```
    inner

Just like a variable:
```vim
vim9script
def Func()
    if 1
        let n = 123
        if 1
            echo n
        endif
    endif
enddef
Func()
```
    123

### cannot nest a script-local function
```vim
vim9script
def Outer()
    def s:Inner()
    enddef
enddef
Outer()
```
    E1075: Namespace not supported: s:Inner()

### `:silent` is ignored before `:execute`

See: <https://github.com/vim/vim/issues/6530>

Solution: use `:silent` *after* `:execute`.

    silent noautocmd execute "normal! `[\<c-v>`]y"
    ^----^
      ✘

    noautocmd execute "silent normal! `[\<c-v>`]y"
                       ^----^
                         ✔

###
### imported items are local to the script

This is suggested at `:h vim9-scopes`:

   > The result is that functions and variables without a namespace can always be
   > found in the script, either defined there or imported.

---

    imported constant
```vim
vim9script
mkdir('/tmp/import', 'p')
let lines =<< trim END
    vim9script
    export const s:MYCONST = 123
END
writefile(lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import MYCONST from 'foo.vim'
echo s:MYCONST
```
    123

---

    imported variable
```vim
vim9script
mkdir('/tmp/import', 'p')
let lines =<< trim END
    vim9script
    export let s:var = 123
END
writefile(lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import var from 'foo.vim'
echo s:var
```
    123

---

    imported function
```vim
vim9script
mkdir('/tmp/import', 'p')
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
```
       def <SNR>2_Imported()
    1      echo 'imported'
       enddef

#### but they're still tied to their original script
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
echo expand('<SID>')
```
           v----v
       def <SNR>2_Imported()
    1      echo 'imported'
       enddef
    <SNR>1_
    ^-----^

You're used to  `s:` being expanded into  a unique script ID.   That's no longer
true in Vim9 script; now, `s:` can  be expanded into one of multiple script IDs;
the  one of  the current  script, or  the one  of any  script from  which you've
imported a function.

You can see the Vim9 `s:` namespace  as a superset of the legacy `s:` namespace.
It contains  the items local  to the current  script, *and* items  imported from
other scripts.

And btw, `expand('<SID>')` will always give you the ID of the current script.
If you need the ID of a script fom which you've imported a function, use this:

    const s:SID = execute('fu s:Opfunc')->matchstr('\C\<def\s\+\zs<SNR>\d\+_')

You may need this in some circumstances; typically where you write code which is
not run in the context of the script, and when you can't use a funcref.
As an example, when you set the `'opfunc'` option.

###
### cannot create script-local variable from `:def` function
```vim
vim9script
def Func()
    let s:var = 123
enddef
defcompile
```
    E1101: Cannot declare a script variable in a function: s:var

---
```vim
vim9script
def Func()
    s:var = 123
enddef
defcompile
```
    E1089: unknown variable: s:foo

---

The issue disappears in a legacy script:
```vim
def Func()
    s:var = 123
enddef
defcompile
```
---

This pitfall is specific to the script-local namespace:
```vim
vim9script
def Func()
    g:var = 123
    echo g:var
enddef
Func()
```
    123
```vim
vim9script
def Func()
    b:var = 123
    echo b:var
enddef
Func()
```
    123

---

The pitfall only affects  a *new* script-local variable which you  refer to in a
`:def` function.  You can refer to an *existing* script-local variable just fine:
```vim
vim9script
s:var = 123
def Func()
    echo s:var
enddef
Func()
```
    123

---

All of this seems too inconsistent.  Is there some bug?

### when a function raises an error at compile time, its body is emptied
```vim
vim9script
def g:Func()
    invalid
enddef

fu Func

defcompile

fu Func
```
        def Func()
     1              invalid
        enddef

    Error detected while processing ...:
    line    1:
    E476: Invalid command: invalid

    function Func()
    endfunction

---

This is limited to compile time.
If an error is detected at runtime, the body of the function remains the same.
```vim
vim9script
def g:Func()
    echo [1, 2, 3][4]
enddef

fu Func

Func()

fu Func
```
       def Func()
    1      echo [1, 2, 3][4]
       enddef

    Error detected while processing ...:
    line    1:
    E684: list index out of range: 4

       def Func()
    1      echo [1, 2, 3][4]
       enddef

### a `:def` function does not need a return type in its header just because it includes a return statement

But it must contain one if it includes a return statement *which returns a value*.
Otherwise, `E1096` is raised:

    E1096: Returning a value in a function without a return type

---
```vim
vim9script
def Func()
    return
enddef
defcompile
```
    ✔
```vim
vim9script
def Func()
    return 123
enddef
defcompile
```
    E1096: Returning a value in a function without a return type

---

Also, note that even though a function returns 0 by default:

```vim
vim9script
def Func()
enddef
let x = Func()
echom x
```
    0

You can not omit a return statement, even if the function's return type is `number`:
```vim
vim9script
def Func(): number
enddef
defcompile
```
    E1027: Missing return statement

Nor can you omit the return value:
```vim
vim9script
def Func(): number
    return
enddef
defcompile
```
    E1003: Missing return value

