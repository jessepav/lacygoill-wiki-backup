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
    var x: string
    var x: number
enddef
```
The previous doesn't raise any error, even though we try to change the type of a
variable which is not allowed.  This means that `Func()` was not compiled.
Had you  moved `:defcompile` *after* `Func()`,  an error would have  been raised
during type checking which itself occurs during the compilation:
```vim
vim9script
def Func()
    var x: string
    var x: number
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

         E1012: type mismatch, expected string but got number~

   - the type of a declared variable matches the type of the expression that you assign it later

         $ vim -Nu NONE -S <(cat <<'EOF'
             def Func()
                 var x: string
                 x = 123
             enddef
             defcompile
         EOF
         )

         E1012: type mismatch, expected string but got number~

### When is type checking performed
#### for a legacy `:fu` function?

At runtime.

#### for a `:def` function?

At compile time.

###
### How to postpone type checking for a `:def` function until runtime?

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
            var x: any
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
            var x = 1 + {}
            echo x
        enddef
    EOF
    )

    :def Func
        def Func()~
     1          var x = 1 + {}~
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

For more info, see `:h vim9-scopes`.

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
var lines =<< trim END
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
    imported

This shows that Vim can look for a function invoked from the script level in the
imported namespace.

####
## When can I
### redefine a `:def` function?

Only if it's global:
```vim
vim9script
def g:Func()
    echo 'first'
enddef
def! g:Func()
    echo 'second'
enddef
g:Func()
```
    second

Note that you need to append a bang to the second `:def`.

---

For all other scopes, a function can't be redefined, even after appending a bang to `:def`:
```vim
vim9script
 # block-local
def Outer()
    if 1
        def Inner()
            echo 'first'
        enddef
        def! Inner()
            echo 'second'
        enddef
        Inner()
    endif
enddef
Outer()
```
    E1117: Cannot use ! with nested :def
```vim
vim9script
 # function-local
def Outer()
    def Inner()
        echo 'first'
    enddef
    def! Inner()
        echo 'second'
    enddef
    Inner()
enddef
Outer()
```
    E1117: Cannot use ! with nested :def
```vim
vim9script
 # script-local
def Func()
    echo 'first'
enddef
def! Func()
    echo 'second'
enddef
```
    E477: No ! allowed
```vim
vim9script
 # imported
mkdir('/tmp/import', 'p')

var lines =<< trim END
    vim9script
    export def Func()
        echo 'first'
    enddef
END
writefile(lines, '/tmp/import/a.vim')

lines =<< trim END
    vim9script
    export def! Func()
        echo 'second'
    enddef
END
writefile(lines, '/tmp/import/b.vim')

set rtp+=/tmp
import Func from 'a.vim'
import Func from 'b.vim'
```
    E477: No ! allowed
    E1044: Export with invalid argument

### delete a `:def` function?

When it's global or local to a legacy script:
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
```vim
vim9script
def g:Func()
enddef
delfu g:Func
```
    ✔

But not if it's local to a Vim9 script:
```vim
vim9script
def Func()
enddef
delfu Func
```
    E1084: Cannot delete Vim9 script function Func

Nor if it's local to a function or a block:
```vim
vim9script
def Outer()
    def Inner()
        echo 'Inner'
    enddef
    delfu Inner
enddef
Outer()
```
    E130: Unknown function: Inner
```vim
vim9script
def Outer()
    if 1
        def Inner()
            echo 'Inner'
        enddef
        delfu Inner
    endif
enddef
Outer()
```
    E130: Unknown function: Inner

#### What about a `:fu` function?

Always, except when the function is local to a Vim9 script:
```vim
vim9script
fu Func()
endfu
delfu Func
```
    E1084: Cannot delete Vim9 script function Func

---
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
```vim
vim9script
fu g:Func()
endfu
delfu g:Func
```
    ✔
```vim
vim9script
fu Outer()
    fu Inner()
        echo 'Inner'
    endfu
    delfu Inner
endfu
Outer()
```
    ✔
```vim
vim9script
fu Outer()
    if 1
        fu Inner()
            echo 'Inner'
        endfu
        delfu Inner
    endif
endfu
Outer()
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
From `:h vim9-scopes /replaced`:

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

    var count = 0  # number of occurences

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
        var mylist = [
                'one',
                # some comment
                'two',
                ]
        echo mylist
    enddef
    Func()

    ['one', 'two']~

    def Func()
        var mylist = [
                'one',
                # some comment
                'two',
                ]
        echo mylist
    enddef
    call Func()

    ['one', 'two']~

    vim9script
    var mylist = [
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
    export var name = 'test'
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
var g:name = 123
```
    E1016: Cannot declare a global variable: g:name

So you can't export it either:
```vim
vim9script
export var g:name = 123
```
    E1016: Cannot declare a global variable: g:name
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
# Refactoring
## Vim9 doesn't support curly braces expansion anymore.  How do I refactor one of these?

Case 1: your curly brace expansion is used in an expression.

That's easy; just use a ternary conditional:
```vim
let mode = 'i'
" let's assume that "mode" can only be 'i' or 'c'
let name_i = 123
let name_c = 456
echo name_{mode}
```
    123
```vim
vim9script
var mode = 'i'
var name_i = 123
var name_c = 456
echo mode == 'i' ? name_i : name_c
```
    123

Case 2: your curly brace is in the lhs of an assignment.

You have to bite the bullet; use an `if/else` block:
```vim
let mode = 'i'
let name_{mode} = 123
echo g:
```
    {'name_i': 123, 'mode': 'i'}
```vim
vim9script
var mode = 'i'
var name_i: number
var name_c: number
if mode == 'i'
    name_i = 123
else
    name_c = 123
endif
echo s:
```
    {'name_i': 123, 'mode': 'i'}

Note that if the expression in the  rhs of the assignment is complex, you better
save  it in  an intermediate  variable  to reduce  code duplication  as much  as
possible:
```vim
vim9script
var mode = 'i'
var name_i: number
var name_c: number
var expr = 1 + 2 + 3 + 5 + 6 + 7 + 8 + 9 + 10 + 11 + 12 + 13 + 14 + 15 + 16
if mode == 'i'
    name_i = expr
else
    name_c = expr
endif
echo s:
```
    {'name_i': 132, 'expr': 132, 'mode': 'i', 'name_c': 0}

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

    let s:name = 123
    fu s:LegacyFunc()
    endfu
    def s:Vim9Func()
    enddef

    echo s:name
    fu s:LegacyFunc
    def s:Vim9Func

In Vim9:

    vim9script
    var name = 123
    fu LegacyFunc()
    endfu
    def Vim9Func()
    enddef

    echo name
    fu LegacyFunc
    def Vim9Func

Unless you explicitly specify another namespace:

    vim9script
    g:name = 123
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
## Which difference is there between a legacy `s:name` and a Vim9 `name` variable defined at the script level?

Legacy's `s:name` can be unlet; not Vim9's `name`:

    vim9script
    var name = 123
    unlet name

    E1081: Cannot unlet name~

## In Vim9 script, what's the main difference between a `b:`, `g:`, `t:`, `w:`, `$` variable and other variables?

Variables which are prefixed by a prefix denoting a scope can't be declared, but
can be deleted:

    vim9script
    var b:name = 123

    E1016: Cannot declare a buffer variable: b:name~

    vim9script
    b:name = 123
    unlet b:name
    ✔

Variables  which are  *not* prefixed  by a  scope (block-local,  function-local,
script-local) *can* be declared, but can't be deleted.

    vim9script
    def Func()
        if 1
            var name = 'block-local'
            unlet name
        endif
    enddef
    defcompile

    E1081: Cannot unlet name~

    vim9script
    def Func()
        var name = 'function-local'
        unlet name
    enddef
    defcompile

    E1081: Cannot unlet name~

    vim9script
    var name = 'script-local'
    unlet name

    E1081: Cannot unlet name~

---

See `:h vim9-declaration /unlet`:

   > In Vim9 script `:let` cannot be used.  An existing variable is assigned to
   > without any command.  The same for global, window, tab, buffer and Vim
   > variables, because they are not really declared.  They can also be deleted
   > with `:unlet`.

## How to prevent a variable from being accessible in a later statement?

Put it inside a `{}` block:

    vim9script
    def Func()
        {
            var n = 123
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
        var x = 3
    enddef
    defcompile

See `:h type-inference`.

### When should I *not* omit the type, even though it's allowed?

When you declare a variable by assigning it an empty list or dictionary.

    var x = []
        ^----^
          ✘

    var x = {}
        ^----^
          ✘

    def Func(x = [])
             ^----^
               ✘
        ...
    enddef

#### Why?

When you write sth like:

    var x = []

You don't really want to assign an empty list to `x`.
What you really want is to declare the existence of the variable.
So, what you really want is sth like:

    var x: list<string>

And when you do so, Vim automatically assigns an empty list.

Otherwise, if you just write `var x = []`, it's exactly as if you had written:

    var x: list<any>
                ^^^

Which might  prevent some  optimizations to  be performed or  some errors  to be
caught, at compile time.

##
## Which operands are accepted by the logical operators:
### && and ||

Only booleans and the numbers 0 and 1.

    vim9script
    echo 123 || 0

    E1023: Using a Number as a Bool: 123~

---

In Vim script legacy, `&&` and `||`  accept any number, as well as strings which
are automatically coerced into numbers.

### ! and ??

Any type of value.

##
## What's the evaluation of `'bàr'[1]`
### in Vim script legacy?

A byte:

    <c3>

That's because:

   - `à` is a multibyte character (press `g8` on `à`, and you'll read `c3 a0`)

   - in Vim script legacy, a string index refers to bytes;
     thus, `[1]` refers to the 2nd *byte* in the string `bàr`

### in Vim9 script?

A character:

    à

That's because in Vim9 script, a string  index refers to a character; thus `[1]`
refers to the 2nd *character* in the string `bàr`.

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

###
## What's shadowing?

If you  *try* to  use the  same name  to define  2 variables  or 2  functions in
different  namespaces, then  we say  that the  one in  the most  local namespace
*shadows* the other one.

Shadowing is disallowed in Vim9 script, although this restriction could be relaxed
in some cases in the future: <https://github.com/vim/vim/issues/6585#issuecomment-667580469>

---

For example:
```vim
vim9script
var name = 'script-local'
def Func()
    var name = 'function-local'
enddef
defcompile
```
    E1054: Variable already declared in the script: name

Here, the function-local variable `name` shadows the script-local variable `name`.
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

Here, the block-local `Func()` shadows the function-local `Func()`.
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

Here, the function-local `Func()` shadows the script-local `Func()`.
```vim
vim9script
mkdir('/tmp/import', 'p')
var lines =<< trim END
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

And here, the script-local `Func()` shadows the imported `Func()`.

### I can use the name of a global item for an item in another namespace:
```vim
vim9script
g:name = 'global'
var name = 'script-local'
echo name
```
    script-local
```vim
vim9script
def g:Func()
    echom 'global'
enddef
def Func()
    echom 'script-local'
enddef
Func()
```
    script-local

### Doesn't this contradict the rule that shadowing is disallowed?

No, because it's not a "real" shadowing; you need to write the prefix `g:` for a
global item; thus,  the names are not exactly identical  (`name` != `g:name` and
`Func` != `g:Func`): <https://github.com/vim/vim/issues/7170#issuecomment-712386861>

Besides, we can already do that in Vim script legacy; so this design decision is
consistent.

Finally, no matter which name you choose  for a non-global item, there is always
the  possibility that  it's  already  used in  the  global  namespace; thus,  it
wouldn't make much sense to disallow this type of shadowing.

##
## This snippet raises a mismatch error:
```vim
vim9script
def Func(): job
    return map(['a', 'b'], {_, v -> 'string'})
enddef
defcompile
```
    E1012: Type mismatch; expected job but got list<any>
                                               ^-------^

### Why does it give `list<any>`, and not `list<string>`?

`map()` could convert your list of strings into a list of anything.
I  don't think  Vim  can infer  the  actual type  resulting  from the  arbitrary
transformation performed by `map()`; so it falls back on `any`.

##
# Pitfalls
## My function prints an unexpected error message!  (an error is missing, the order of the errors looks wrong, ...)

Your error message is probably correct.
You have to remember that an error can  be raised at compile time or at runtime,
and that the latter step occurs after the former.

Check whether the error message contains the keyword "processing" or "compiling":

    Error detected while processing ...
                         ^--------^

    Error detected while compiling ...
                         ^-------^

Or, write `:defcompile` at the end of your script.

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
    E1012: type mismatch, expected list<any> but got float
                          ^------------------------------^

You might think the error message is wrong, and instead expect this one:

    E1012: type mismatch, expected float but got list<number>
                          ^---------------------------------^

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
var l = [1 , 2 , 3]
```
    E1068: No white space allowed before ','

In a list or dictionary, the usage of white space is strict:

   - you *can* write a white space after the opening `[` or `{`, and before the closing `]` or `}`

   - you *cannot* write a white space before a comma separating two consecutive items,
     nor after a colon separating a key from its value in a dictionary

   - you *must* write a white space after a comma separating two consecutive items

Example:

                ok but useless
                v                 v
    var dict = { 'a' : 1 , 'b' : 2 }
                    ^ ^ ^ ^   ^ ^
                    ✘ ✔ ✘ ✔   ✘ ✔

                    ✘ = cannot be written
                    ✔ = must be written

Remove the wrong white space:
```vim
vim9script
var dict = {'a': 1, 'b': 2}
```
    ✔

Some (all?) of these rules were introduced in 8.2.1326.

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
        var n = 123
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
        var l = ['aaa', 'bbb', 'ccc', 'ddd']
        range(1, 2)->map('l[v:val]')
        #                ^--------^
        #                    ✘
    enddef
    Func()

    E121: Undefined variable: l~

Solution: use a lambda.

    vim9script
    def Func()
        var l = ['aaa', 'bbb', 'ccc', 'ddd']
        range(1, 2)->map({_, v -> v})
    enddef
    Func()

---

The issue is due to:

   > The local variables are on the stack  and cannot be accessed outside of the
   > compiled function.

Source: <https://github.com/vim/vim/issues/6401#issuecomment-655071515>

## What's the fastest between
### a lambda and an eval string?

Inside a `:def` function, a lambda is significantly faster:

    $ vim -es -Nu NONE -i NONE -U NONE -S <(cat <<'EOF'
        vim9script

        def Lambda()
            var time = reltime()
            range(999999)->map({_, v -> v + 1})
            setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run lambdas')
        enddef
        Lambda()

        def EvalString()
            var time = reltime()
            range(999999)->map('v:val + 1')
            setline(2, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run eval strings')
        enddef
        EvalString()

        :%p
        qa!
    EOF
    )

    0.467 seconds to run lambdas~
    0.706 seconds to run eval strings~

But at the script level, a lambda is significantly slower:

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        vim9script

        var time = reltime()
        range(999999)->map({_, v -> v + 1})
        setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run lambdas')

        var _time = reltime()
        range(999999)->map('v:val + 1')
        setline(2, reltime(_time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run eval strings')

        :%p
        qa!
    EOF
    )

    1.503 seconds to run lambdas~
    0.669 seconds to run eval strings~

Conclusion: always use lambdas, but make sure to write them inside `:def` functions.

### a `map()` and a for loop?

Inside a `:def` function, a for loop is significantly faster:

    $ vim -es -Nu NONE -i NONE -U NONE -S <(cat <<'EOF'
        vim9script
        var mylist = pow(10, 6)->float2nr()->range()

        def Lambda()
            var time = reltime()
            map(mylist, {_, v -> v + 1})
            setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run Lambda()')
        enddef
        Lambda()

        def ForLoop()
            var time = reltime()
            var i = 0
            for _ in mylist
                mylist[i] = mylist[i] + 1
                i += 1
            endfor
            setline(2, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run ForLoop()')
        enddef
        ForLoop()

        :%p
        qa!
    EOF
    )

    0.417 seconds to run Lambda()~
    0.235 seconds to run ForLoop()~

But at the script level, a for loop is significantly slower:

    $ vim -es -Nu NONE -i NONE -U NONE -S <(cat <<'EOF'
        vim9script
        var mylist = pow(10, 6)->float2nr()->range()

        var time = reltime()
        map(mylist, {_, v -> v + 1})
        setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run Lambda()')

        time = reltime()
        var i = 0
        for _ in mylist
            mylist[i] = mylist[i] + 1
            i += 1
        endfor
        setline(2, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run ForLoop()')

        :%p
        qa!
    EOF
    )

    0.868 seconds to run Lambda()~
    5.891 seconds to run ForLoop()~

Conclusion: on huge lists (>= 10^4 items), prefer a `for` loop, but make sure to
write it  inside a  `:def` function.

However, note  that the performance  gain brought by a  `for` loop might  not be
always as significant as in the previous simple test.  Example:

    $ vim -es -Nu NONE -i NONE -U NONE -S <(cat <<'EOF'
        vim9script
        var mylistlist = pow(10, 6)->float2nr()->range()->map({_, v -> [0, 0, 0, 0, 0]})

        def Lambda()
            var time = reltime()
            map(mylistlist, {_, v -> map(v, {_, w -> w + 1})})
            setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run Lambda()')
        enddef
        Lambda()

        def ForLoop()
            var time = reltime()
            var i = 0
            for item in mylistlist
                map(item, {_, v -> v + 1})
                i += 1
            endfor
            setline(2, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run ForLoop()')
        enddef
        ForLoop()

        :%p
        qa!
    EOF
    )

    2.743 seconds to run Lambda()~
    2.490 seconds to run ForLoop()~

The results might  also depend on the size of  the inner lists/dictionaries, and
the type of transformation you perform...

##
## Vim complains that it doesn't know the function-local variable I'm referring to!

    vim9script
    def Func()
        if 1
           var n = 123
        endif
        echo n
    enddef
    defcompile

    E1001: variable not found: n~

A variable is local to its current block.

Solution:  Declare it *before* the block where it's assigned a value.

    vim9script
    def Func()
        var n: number
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
            var n: number
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
        echo s:name
    enddef
    defcompile
    s:name = 123

    E1050: Item not found: name~

Make sure your script-local variable is defined *before* the function – in which
it's referred to – is compiled.

    vim9script
    def Func()
        echo s:name
    enddef
    s:name = 123
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
        var qfl: list<any>
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
        var qfl: list<any>
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
## The following snippet raises an error:
```vim
vim9script
def Func()
  var name: any
  eval name == []
enddef
Func()
```
    E691: Can only compare List with List

### Why?

If  a variable  is declared  with the  type `any`,  but without  any value,  Vim
automatically assigns it the value `0`:
```vim
vim9script
def Func()
  var name: any
  echo name == 0
enddef
Func()
```
    v:true

##
## I can't declare multiple variables on a single line, using the unpack notation!

There is no way around that.

At some point in the future, it might be implemented though:

   > I don't like it, too complicated.  Either type inferrence should work,
   > or the types should be declared separately.

Source: <https://github.com/vim/vim/issues/6494#issuecomment-661320805>

Note that this limitation is specific to declarations; not to assignments.  IOW,
you *can* use the unpack notation to *assign* multiple variables on a single line.

## I can't use the Vim9 syntax in a custom (auto)command which is run in the Vim9 context!

It doesn't matter in which context you're when you run a (auto)command.
What matters is the context where it's defined.
```vim
vim9script

fu InstallCmd()
    com -nargs=1 Cmd call s:Func(<args>)
endfu
def Func(d: dict<any>)
    echo d
enddef
InstallCmd()

Cmd {key: 123}
```
    E121: Undefined variable: key

Here, the error is caused by the usage of the `{}` syntax which is only valid in
Vim9 script.  In legacy Vim script, you need to use `#{}`.
But `:Cmd` was defined  in a legacy context, so you can't  use `{}`, even though
you're in the Vim9 context when you call `:Cmd`.

---

This pitfall is documented at `:h <f-args>` (almost at the very end):

   > If  the  command  is  defined  in   Vim9  script  (a  script  that  starts  with
   > `:vim9script` and in a `:def` function) then  {repl} will be executed as in Vim9
   > script.  Thus this depends on where the command is defined, not where it is used.

Similarly, from `:h autocmd-define`:

   > If the `:autocmd` is in Vim9 script (a script that starts with `:vim9script` and
   > in a `:def` function) then {cmd} will be executed as in Vim9 script.
   > Thus this depends on where the autocmd is defined, not where it is triggered.

## I want to use a closure in a global command or in the replacement of a substitution.  It doesn't work!

Your closure needs to be global.  It can't be local to the outer function:

    ✘
    def Closure()
        ...
    enddef
    s/pat/\=Closure()/

        ✔
        vv
    def g:Closure()
        ...
    enddef
    s/pat/\=Closure()/

This is consistent with Vim script legacy, where a closure must also be global:
```vim
fu Func()
    fu Closure() closure
    endfu
endfu
call Func()
fu /Closure
```
    function Closure() closure
             ^-------^
             this is global

---

Usage example:
```vim
vim9script

def ReverseEveryNLines(n: number, line1: number, line2: number)
    var mods = 'sil keepj keepp lockm '
    var range = ':' .. line1 .. ',' .. line2
    #   vv
    def g:Offset(): number
        var offset = (line('.') - line1 + 1) % n
        return offset != 0 ? offset : n
    enddef
    exe mods .. range .. 'g/^/exe "m .-" .. Offset()'
enddef
repeat(['aaa', 'bbb', 'ccc'], 3)->setline(1)
ReverseEveryNLines(3, 1, 9)
```
---

You could also invoke a script-local function:
```vim
vim9script

def ReverseEveryNLines(n: number, line1: number, line2: number)
    var mods = 'sil keepj keepp lockm '
    var range = ':' .. line1 .. ',' .. line2
    exe mods .. range .. printf('g/^/exe "m .-" .. Offset(%d, %d)', line1, n)
enddef

def Offset(line1: number, n: number): number
    var offset = (line('.') - line1 + 1) % n
    return offset != 0 ? offset : n
enddef

repeat(['aaa', 'bbb', 'ccc'], 3)->setline(1)
ReverseEveryNLines(3, 1, 9)
```
But it's less pretty.

##
# Todo
## To refactor:
### maybe make sure a variable name starting with an underscore is not used

    \C\<var _\S\|\<def.*\%(, \|(\)_\S

Sometimes, we have created and used a variable name starting with an underscore.
This  looks wrong,  because it  goes against  a convention  which I  think we've
followed so far; i.e. a variable name  starting with an underscore should not be
used.

Sometimes, we've  used a variable  name starting with  an underscore to  avoid a
clash with a function argument:

    def Func(name: number)
        var _name = ...
            ^
            ✘

In those cases, I suggest you use the prefix `a` for the argument (reminiscent of `a:`):

             ✔
             v
    def Func(aname: number)
        var name = ...

### eval strings into lambdas

But make sure they're inside a `:def` function first.
Don't worry, a lambda in a `:def` function is not slower than an eval string; on
the contrary, it's faster.

Look for the pattern `v:val\|v:key`.

Update: We have very few `v:val` and `v:key` in our config.
Refactor all  `:fu` functions which include  a `v:val` or `v:key`  into a `:def`
function, then refactor the eval strings into lambdas.

Also, consider updating `:RefVim9` so that  it populates a location list for all
the `v:val` and `v:key`.

---

While I was  trying to refactor a legacy function  (`s:next_fold()`) into a Vim9
function to get rid of `v:val`:

    ~/.vim/plugged/vim-fold/autoload/fold/motion.vim:136

I've come across a bug in `:RefVim9`:

    ~/.vim/plugged/vim-vim/autoload/vim/refactor/vim9.vim:551

The issue is that the `assignments`  loclist is missing some assignments and has
duplicate entries.

Here is what I think is a MWE:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        var lines =<< trim END
            foo xxx
            xxx foo
            foo xxx
            xxx foo
        END
        writefile(lines, '/tmp/file')
        sil e /tmp/file
        vim /\_.*\zsfoo/gj %
        cw
    EOF
    )

I think the issue comes from the `*` quantifier:

    vim /\_.*\zsfoo/gj %
            ^
            ✘

We should use a lazy quantifier:

    vim /\_.\{-}\zsfoo/gj %
            ^--^
             ✔
```vim
vim9script
var lines =<< trim END
    foo xxx
    xxx foo
    foo xxx
    xxx foo
END
writefile(lines, '/tmp/file')
sil e /tmp/file
vim /\_.\{-}\zsfoo/gj %
cw
```
It's better, but we still have a few duplicate entries.
Why?

Once you understand everything, fix the issue in `:RefVim9`.
Also, check whether we've made the kind of mistake elsewhere.

### check whether we could remove a few `extend()` in our Vim9 scripts

Now that Vim9 provides a better support for dictionaries...

### eliminate the `#{}` syntax for literal dictionaries

Refactor as many legacy functions/scripts in Vim9 so that we don't use the `#{}`
syntax for literal dictionaries anymore.  It is confusing to read 2 syntaxes for
dictionaries.  In  Vim9 script,  since 8.2.2015  and 8.2.2017,  there is  only 1
syntax left: `{}`. If you need a key to be evaluated, use square brackets.

### maybe prefix all `:import` commands with `:silent!`

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

### remove useless "s:" scope in vimrc once it's fully refactored

Right now,  it's written in front  of some function names  and possibly variable
names, because we haven't yet written `vim9script` at the top.

Do  the same  in  all scripts  you  progressively refactor  in  Vim9; i.e.  once
finished, remove any useless `s:`.

---

Also, replace `v:true` with `true`, and `v:false` with `false` when possible.

---

Also, remove `:call` in autocmds, at script level, ... (but not in mappings).

---

    =~#
      ^
      ✘
      to remove

---

Same thing for myfuncs.vim.

### should we make sure to never declare a null dictionary / list?

    # ✘
    var somedict: dict<any>

    # ✔
    var somedict: dict<any> = {}
                            ^--^

Rationale:  We've often triggered bugs because of null dictionaries / lists.

### should we specify the types of the arguments in a lambda?

This is possible since [8.2.1956](https://github.com/vim/vim/releases/tag/v8.2.1956).

### should we specify the return type void in the header of a function which doesn't return anything?

              v----v
    def Func(): void
        ...
        # no ":return value" statement anywhere
        ...
    enddef

### should we use `: void` for the return type of a function which doesn't return anything?

That's what is done in vim-fileselect.

### should we rename all the autoload functions which have an underscore in their name?

Because they're in a file which contains an underscore.

    ^\s*\Cdef\s\+[^ (_]*_

### our Vim `gd` snippet should expand into a different guard when used at the top of a Vim9 script file

In Vim9 script, it should be:

    if exists('loaded') | finish | endif
    var loaded = true

Also in legacy Vim script, we probably don't need that:

    if exists('g:myplugin_loaded')
        finish
    endif
    let g:myplugin_loaded

Use this instead:

    if exists('s:loaded') | finish | endif
    let s:loaded = v:true

See:

    ~/.vim/plugged/vim-snippets/pythonx/snippet_helpers.py
    /def plugin_guard(

#### more generally, all our Vim snippets use the legacy syntax

Should we update them to support only the Vim9 syntax?

Or should we  make them smart and use  one syntax or the other  depending on the
current context?

##
## To understand:
### How to change the type of a variable?

    vim9script
    var time = reltime()
    sleep 1
    var time = reltime(time)->reltimestr()->matchstr('.*\..\{,3}')
    echom printf('we slept for %s seconds', time)

    E1041: Redefining script item time~

---

For the moment, the only workaround I can think of, is to use an extra variable:

    vim9script
    var time = reltime()
    sleep 1
    var _time = reltime(time)->reltimestr()->matchstr('.*\..\{,3}')
    echom printf('we slept for %s seconds', _time)

### Can we import a global function?

Last time I tried, it didn't work.

##
## To document:
### cannot use the name of a function as a variable name
```vim
vim9script
def Func()
    var Func = 0
enddef
defcompile
```
    E1073: name already defined: Func = 0
```vim
vim9script
def FuncA()
    var FuncB = 0
enddef
def FuncB()
enddef
defcompile
```
    E1073: name already defined: FuncB = 0

Is it working as  intended?  I guess it is.  Using the same  name for a function
and a  variable is confusing,  and Vim9  script try to  be as less  confusing as
possible.

But why doesn't this raise any error?
```vim
vim9script
var Func = 12
def Func(): number
    return 34
enddef
echo Func
echo Func()
```
    12
    34

I guess it's because the variable assignment `Func` is not compiled.
To be consistent, I think it should also raise an error at the script level.

---

What happens if we use different scopes?
Make more tests.
```vim
vim9script
def g:Func()
    var Func = 0
enddef
defcompile
```
    ✔
```vim
vim9script
def Func()
    g:Func = 0
enddef
defcompile
```
    ✔

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
        var n = 123
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

### nested closures don't always work
```vim
vim9script
def Func()
    var n = 123
    echo {-> {-> n}()}()
enddef
Func()
```
    1
    ^
    ✘
    it should be 123

Workaround:

Move the definition of the nested lambda outside the outer lambda:
```vim
vim9script
def Func()
    var n = 123
    var Inner = {-> n}
    echo {-> Inner()}()
enddef
Func()
```
    123

You can keep the nested reference; but not the nested definition.
```vim
vim9script
def Func()
    var j = 34
    echo {i -> {-> [i, j]}()}(12)
enddef
Func()
```
    [12, 1]

---

For more info, see: <https://github.com/vim/vim/issues/7150>

### why we have "inconsistent" messages when using a wrong type of argument with the "-" and "+" operators
```vim
vim9script
eval '' - 1
```
    at runtime:
    E1030: Using a String as a Number
```vim
vim9script
def Func()
    eval '' - 1
enddef
Func()
```
    at compile time:
    E1036: - requires number or float arguments
```vim
vim9script
def Func()
    eval '' + 1
enddef
Func()
```
    at compile time:
    E1051: Wrong argument type for +

First, the context is different in the  first snippet.  In the latter, the error
occurs at runtime.  In the next snippets, the error occurs at compile time.  Vim
knows more about the  types at runtime than at compile time;  so, it kinda makes
sense that the error messages are different.

Second, `+` has 2 meanings: it can  be used as an arithmetic operator to perform
an addition,  or as a  list concatenation operator.   So, again, it  kinda makes
sense that Vim raises a different error for `+` than for `-`.

<https://github.com/vim/vim/issues/7167#issuecomment-714620921>

### a function-local function is implemented as a lambda function

At least,  that's what  it seems  when reading  an error  message raised  from a
function-local function:

    $ vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            def Nested()
                eval [][0]
            enddef
            Nested()
        enddef
        Func()
    EOF
    )

    Error detected while compiling command line..script /proc/3556/fd/11[8]..function <SNR>1_Func[4]..<lambda>1:
                                                                                                      ^-------^

It's not a bug and it can't be fixed.
The concept of function local to another function didn't exist in Vim script legacy.
A function-local function can't have a public name like "Nested".
It would mean that you can invoke it from the command-line.  That's not possible.

Fortunately, that's not an issue for `vim-stacktrace`.
That's because we can still retrieve the definition site of such a function:

    " still works
    :verb function {'<lambda>123'}

### we don't need `s:` in a lambda at the script level anymore in Vim9 script

Since [8.2.2018](https://github.com/vim/vim/releases/tag/v8.2.2018).

### the `#{}` syntax (literal dictionary) is deprecated in Vim9 script

See `:h vim9 /Dictionary literals`.

Now, `#` should *always* be parsed as a comment leader.

### trick to get the right type in a declaration without too much thinking/guessing

Whenever you  wonder with which type  you should declare a  variable, function's
argument, or function's return value, first use `any`.

Once your code compiles, progressively  replace those `any` with obviously wrong
types; e.g. `job`.

You'll get an error such as:

    E1013: Argument 1: type mismatch, expected job but got number

Or:

    E1013: Argument 1: type mismatch, expected job but got list<any>

One of the types before or after "but got" will be different than `job`.
If it is:

   - not composite, then use it instead of the obviously wrong `job`
   - composite, then replace `job` with `list<job>`, and repeat the process

### backtick expansion is necessary to refer to function-local variable from global context (`:s`, `:g`, ...)

This was not an issue in Vim script legacy:
```vim
fu Func()
    let name = 'function-local'
    g/^/echo name
endfu
call Func()
```
    function-local

But this is not possible in Vim9:
```vim
vim9script
def Func()
    var name = 'function-local'
    g/^/echo name
enddef
Func()
```
    E121: Undefined variable: name

Because:

   > It is simply not possible to access the compiled code and variables from interpreted code.

Source: <https://github.com/vim/vim/issues/7541#issuecomment-751274709>

Solution: Use a backtick expansion:

    g/^/echo name
             ^--^
              ✘

             the value of the variable is inserted in place; if you need quotes, write them explicitly
             v       v
    g/^/echo '`=name`'
              ^^
              ✔
```vim
vim9script
def Func()
    var name = 'function-local'
    g/^/echo '`=name`'
enddef
Func()
```
    function-local

See `:h vim9 /newText`.

---

Note that it might not always work:

   > I'm not sure it fully works, since any command may follow :g/pattern/

Source: <https://github.com/vim/vim/issues/7541#issuecomment-751285484>

If so, consider opening an issue report to make a backtick expansion expanded in
more places.

Alternatively, use  a script-local  funcref, which is  more powerful  and should
work all the time (but is more verbose):
```vim
vim9script
var Name: func
def Func()
    Name = () => 'function-local'
    g/^/echo Name()
enddef
Func()
```
    function-local

See: <https://github.com/vim/vim/issues/7541#issuecomment-751285484>

###
### the difference between using or omitting `function()` when saving a funcref in a variable

   > A user defined function can be used as a function reference in an expression
   > without `function()`. **The argument types and return type will then be checked.**
   > The function must already have been defined. >

   >         var Funcref = MyFunction

   > When using `function()` **the resulting type is "func", a function with any**
   > **number of arguments and any return type.**  The function can be defined later.

The first bold sentence is correct:
```vim
vim9script
def MyFunction(n: number, s: string): list<string>
    return repeat(s, n)
enddef
var Funcref: func(number, string): list<string> = MyFunction
```
    ✔
```vim
vim9script
def MyFunction(n: number, s: string): list<number>
    return repeat(s, n)
enddef
var Funcref: func(number, string): list<string> = MyFunction
```
    E1012: Type mismatch; expected func(number, string): list<string> but got func(number, string): list<number>

But the second bold sentence seems wrong:
```vim
vim9script
def MyFunction(n: number, s: string): list<string>
    return repeat(s, n)
enddef
var Funcref: func(number, string): list<number> = function('MyFunction')
```
    E1012: Type mismatch; expected func(number, string): list<number> but got func(number, string): list<string>
                                                                          ^^^                     ^------------^

According to the help, it should have gotten the return type `any` (because of `function()`).
Although, even if the  return type was correct, I guess an  error would still be
raised; the message should just be different:

    E1012: Type mismatch; expected func(number, string): list<number> but got func(number, string): any
                                                                                                    ^^^

---

Also, the help is slightly incomplete; I think it should be:

   > When using `function()` the resulting type is "func", a function with any
   > number of arguments**, with any types,** and any return type.

#### ?

   > A user defined function can be used as a function reference in an expression
   > without `function()`. The argument types and return type will then be checked.
   > The function must already have been defined. >

   >         var Funcref = MyFunction

   > When using `function()` the resulting type is "func", a function with any
   > number of arguments and any return type.  **The function can be defined later.**

What does it mean?

This doesn't work:
```vim
vim9script
var Funcref = function('MyFunction')
def MyFunction()
enddef
```
This works while the help *seems* (not sure) to say that it shouldn't:
```vim
vim9script

def FuncWithForwardRef()
    var Funcref = DefinedLater
    echo Funcref()
enddef

def DefinedLater(): string
    return 'yes'
enddef

FuncWithForwardRef()
```
---

Maybe this difference can only be observed at compile time, not at runtime?

---

This paragraph was added in this commit:

<https://github.com/vim/vim/commit/d1caa941d876181aae0ebebc6ea954045bf0da24#diff-85b42c1fb69f74ec09315a12804fc50e>

#### ?

   > A user defined function can be used as a function reference in an expression
   > without `function()`. **The argument types and return type will then be checked.**
   > The function must already have been defined. >

   >         var Funcref = MyFunction

   > When using `function()` the resulting type is "func", a function with any
   > number of arguments and any return type.  The function can be defined later.

If I use a  function name as a funcref for the  `{skip}` argument of `search()`,
the argument types and return type of the function will be checked against what?

###
### when we can declare a script-local item (variable or function) in a `:def` function in a legacy script
```vim
def Func()
    var s:name = 123
enddef
call Func()
```
    E1101: Cannot declare a script variable in a function: s:name~

    same error in a Vim9 script
```vim
def Func()
    s:name = 123
    echo s:name
enddef
call Func()
```
    123~

    in a Vim9 script, an error would be raised "E1089: unknown variable: s:name"
    https://github.com/vim/vim/issues/6771#issuecomment-678657763
```vim
def Outer()
    def s:Inner()
    enddef
enddef
call Outer()
```
    E1075: Namespace not supported: s:Inner()~

    same error in a Vim9 script

### when `s:` scope can be omitted

You can omit `s:` in front of:

   - a variable name iff the current script is a Vim9 script

   - a function name iff its immediate *surrounding* context is Vim9
     (the surrounding context of a function's header is not the header itself)

---

Note that  – if you  drop `s:` –  there still can't  be any ambiguity  between a
function-local variable, and a script-local one  which would have the same name;
that's because a function-local variable cannot shadow a script-local one.
```vim
vim9script
var name = 12
def Func()
    var name = 34
enddef
Func()
```
    E1054: Variable already declared in the script: name~

---

For a `:def` function in a legacy script,  you can *not* omit `s:` in front of a
variable name, regardless of whether it was defined at the script level:

    let s:name = 123
    def Func()
        echo name
    enddef
    call Func()

    E1001: variable not found: name~

Or in a `:def` function:

    def Func()
        s:name = 123
        echo name
    enddef
    call Func()

    E1001: variable not found: name~

However, you *can* omit `s:` in front  of a function name, regardless of whether
it's a `:def` function:
```vim
def s:ScriptLocalDef(): number
    return 123
enddef
def Func()
    echo ScriptLocalDef()
enddef
call Func()
```
    123

Or a `:fu` function:
```vim
fu s:ScriptLocalFu()
    return 123
endfu
def Func()
    echo ScriptLocalFu()
enddef
call Func()
```
    123

This seems inconsistent.  Should it be disallowed to omit `s:` before a function
name in a `:def` function in a legacy script?
Answer: no.  See: <https://github.com/vim/vim/issues/6771#issuecomment-678775221>

---

See also:

   - <https://github.com/vim/vim/issues/6771#issuecomment-678657763>
   - `:h :enddef`:

   > If the script the function is defined in is Vim9 script, then script-local
   > variables can be accessed without the "s:" prefix.  They must be defined
   > before the function is compiled.  If the script the function is defined in is
   > legacy script, then script-local variables must be accessed with the "s:"
   > prefix.

---

If all of this sounds confusing, remember only this:
inside a  `:def` function  defined in a  legacy script, we  cannot omit  `s:` in
front of a variable name.

See here for an explanation: <https://github.com/vim/vim/issues/6771#issuecomment-678657763>

The other rules are more obvious.

---

Note however that you can only omit `s:` in the Vim9 context.
```vim
vim9script
def Callback(_j: job, _e: number)
    echom 'callback'
enddef
def Func()
    job_start(['/bin/bash', '-c', ':'], #{exit_cb: function('Callback')})
enddef
Func()
```
    E117: Unknown function: Callback

Here, an error is raised, because:

   - the funcref returned by `function('Callback')` can only work in the Vim9 context
   - when the callback is processed, and the funcref is used, we are no longer in the Vim9 context

Similar pitfall with `listener_add()`:
```vim
vim9script
def Listener(bufnr: number, start: number, end: number, added: number, changes: list<dict<number>>)
  echom 'lines ' .. start .. ' until ' .. end .. ' changed'
enddef
listener_add(function('Listener'), '%')
feedkeys('aaa', 'nt')
```
    E117: Unknown function: Listener

Solution: Don't use `function()` at all.
```vim
vim9script
def Callback(_j: job, _e: number)
    echom 'callback'
enddef
def Func()
    job_start(['/bin/bash', '-c', ':'], #{exit_cb: Callback})
enddef
Func()
```
    callback
```vim
vim9script
def Listener(bufnr: number, start: number, end: number, added: number, changes: list<dict<number>>)
  echom 'lines ' .. start .. ' until ' .. end .. ' changed'
enddef
listener_add(Listener, '%')
feedkeys('aaa', 'nt')
```
---

But why does this work?
```vim
vim9script
def Callback(...l: list<any>)
    echom 'callback'
enddef
popup_create('', #{callback: function('Callback')})
```
Maybe  the  difference is  somehow  explained  by  the  fact that  the  previous
functions (`job_start()` and `listener_add()`) are async, while `popup_create()`
is not.

But watch this:
```vim
vim9script
def Filter(...l: list<any>)
    echom 'filter'
enddef
popup_create('', #{filter: function('Filter')})
feedkeys('j')
```
    E117: Unknown function: Filter

If the previous explanation was true, shouldn't this snippet work?
Maybe the difference is somehow explained by  the fact that a filter function is
not processed  in the same  context as a callback.   It's processed in  the same
context as a mapping; i.e. outside any script.

Bottom line: It is not always obvious whether  `s:` can be dropped in front of a
function name.  You'll have to learn by trial and error.
However,  I would  recommend  you drop  `function()`.  It  makes  the code  more
readable,  and  *always*  lets  you   drop  `s:`.   Obviously,  you  can't  drop
`function()` when you need a partial...

*actually, what seems to matter is not dropping function(),*
*but dropping the quotes around the function name,*
*which seems to be allowed even when using function()*

Update: Now that I think about it a little more, I think it's a bug.
Vim9 should be smart enough to assume `s:` when it's missing.
Besides, if it's  not fixed, when you  press `C-]` on such a  function name, Vim
will fail to jump to the function's definition.

    exit_cb: function('s:Job_handler', [opts, 'exit']),
                         ^---------^
                         if you press `C-]`:
                         Vim(tag):E426: tag not found: s:Job_handler~
                         that's because `Job_handler()` is defined without `s:` in its header

Besides, if you press `C-c`, then the callback function won't be found either:

    vim9script
    def Popup()
        var id = popup_menu(['aaa', 'bbb', 'ccc'], #{
            filter: Filter,
            callback: function('Callback'),
            })
    enddef
    def Filter(winid: number, key: string): bool
        return popup_filter_menu(winid, key)
    enddef
    def Callback(winid: number, choice: number)
    enddef
    Popup()
    feedkeys("\<c-c>")

    E117: Unknown function: Callback~

Same issue if the filter function cannot be found:

    vim9script
    def Popup()
        var id = popup_menu(['aaa', 'bbb', 'ccc'], #{
            filter: function('Filter'),
            callback: function('Callback'),
            })
    enddef
    def Filter(winid: number, key: string): bool
        return popup_filter_menu(winid, key)
    enddef
    def Callback(winid: number, choice: number)
    enddef
    Popup()
    feedkeys('j')

    E117: Unknown function: Filter~
    E117: Unknown function: Callback~

Notice how  – this time  – an  error is also  raised for the  callback function.
It's because of the previous error  caused by the filter function which couldn't
be found.

---

And what about `:var`?  When can we omit it?
It seems we can when `s:` is explicit:
```vim
vim9script
s:name = 'string'
```
Otherwise, we can't:
```vim
vim9script
name = 'string'
```
    E492: Not an editor command: name = 'string'

### workarounds to unlet a script-local variable

If you  use a script-local  variable as some sort  of cache, and  you're worried
that it  might consume too  much memory,  you can simply  reset the cache  to an
empty value (list, dictionary, blob...).

Otherwise,  if you  really want  the reference  not to  exist anymore,  the only
workaround I  can think  of is to  turn your variable  into a  dictionary's key.
Then, when you want to delete the reference, remove the key from the dictionary.

###
### imported items are local to the script

This is suggested at `:h vim9-scopes /result`:

   > The result is that functions and variables without a namespace can always be
   > found in the script, either defined there or imported.

---

    imported constant
```vim
vim9script
mkdir('/tmp/import', 'p')
var lines =<< trim END
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
var lines =<< trim END
    vim9script
    export var s:name = 123
END
writefile(lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import name from 'foo.vim'
echo s:name
```
    123

---

    imported function
```vim
vim9script
mkdir('/tmp/import', 'p')
var lines =<< trim END
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
var lines =<< trim END
    vim9script
    export def Imported()
        echo 'imported'
    enddef
END
mkdir('/tmp/import', 'p')
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
    var s:name = 123
enddef
defcompile
```
    E1101: Cannot declare a script variable in a function: s:name

---
```vim
vim9script
def Func()
    s:name = 123
enddef
defcompile
```
    E1089: unknown variable: s:name

---

The issue disappears in a legacy script:
```vim
def Func()
    s:name = 123
enddef
defcompile
```
---

This pitfall is specific to the script-local namespace:
```vim
vim9script
def Func()
    g:name = 123
    echo g:name
enddef
Func()
```
    123
```vim
vim9script
def Func()
    b:name = 123
    echo b:name
enddef
Func()
```
    123

---

The pitfall only affects  a *new* script-local variable which you  refer to in a
`:def` function.  You can refer to an *existing* script-local variable just fine:
```vim
vim9script
s:name = 123
def Func()
    echo s:name
enddef
Func()
```
    123

---

All of this seems too inconsistent.  Is there some bug?

### cannot use `-=` when lhs is key from dictionary
```vim
vim9script
def Func()
    var d = {key: 123}
    d.key -= 1
enddef
defcompile
```
    Index with operation not supported yet

Same issue with:

    +=
    *=
    /=
    %=

---

Another error is raised atm for `..=`:
```vim
vim9script
def Func()
    var d = {key: 'string'}
    d.key ..= ' abc'
enddef
defcompile
```
    E1019: Can only concatenate to string

I think it's on the todo list (`:h todo /\.\.=`):

   > - Appending to dict item doesn't work:
   >     let d[i] ..= value

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
var x = Func()
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

###
### in a composite value, "function()" suppresses type checking at compile time
```vim
vim9script
def Func()
    var l: list<number>
    l = ['', function('len')]
enddef
defcompile
```
    no error
```vim
vim9script
def Func()
    var d: dict<number>
    d = #{aa: '', bb: function('len')}
enddef
defcompile
```
    no error

That's because `function()` is not considered a constant:
<https://github.com/vim/vim/issues/7171#issuecomment-712315593>

Not sure what that means...

---

Anyway, as a result, this might cause an error to be shadowed:
```vim
vim9script
def Func()
    var l: list<string>
    l = ['', function('len')]
    eval l[0] - 1
enddef
Func()
```
    line 3:
    E1036: - requires number or float arguments

The first error is not this one.
The first error is:

    line 2:
    E1012: Type mismatch; expected list<string> but got list<any>

This might make debugging harder; especially when the lines are far away from each other:
```vim
vim9script
def Func()
    var l: list<string>
    # ...
    # many lines of code
    # ...
    # FIRST ERROR
    l = ['', function('len')]
    # ...
    # many lines of code
    # ...
    # REPORTED ERROR
    eval l[0] - 1
enddef
Func()
```
