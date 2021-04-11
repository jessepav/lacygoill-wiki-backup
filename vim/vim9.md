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
The previous code doesn't raise any error, even though we try to change the type
of a variable which is not allowed.  This means that `Func()` was not compiled.
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
    E1017: Variable already declared: x

##
## If a `:def` function contains a syntax error, when does Vim raise an error?

At compile time, *and* at runtime:
```vim
vim9script
def Func()
     invalid
enddef
defcompile
Func()
```
    E476: Invalid command: invalid
    E1091: Function is not compiled: <SNR>1_Func

`E476` is raised at compile time; `E1091` at runtime.

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
Func()
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
    E477: No ! allowed
    two
    E193: :enddef not inside a function
    one

### Why?

You can't replace a script-local function.
From `:h vim9-scopes /replaced`:

   > In Vim9 script, script-local functions are defined once when the script is sourced
   > and cannot be deleted or replaced.

This explains why `E477` is raised.
As  a  result, `:def!`  does  not  start a  function  definition,  and the  next
`:enddef` does not match any `:def`; this explains `E193`.

### OK.  But why are the bodies of the 2 function definitions executed in reverse order?

The second  `echom` is *not*  parsed inside  a function (because  `:def!` raised
`E477`); it's parsed at the script level, and executed immediately.

Later, `Func()` is run.

##
## The following snippet raises E1075:
```vim
vim9script
def Outer()
    def s:Inner()
    enddef
enddef
defcompile
```
    E1075: Namespace not supported: s:Inner()

### Why?

That's a consequence of a rule which states that an item must be declared in the
right context.  That is:

   - a script-local variable/function in a script
   - a function-local variable/function in a function
   - a block-local variable/function in a block
   - a function argument in its header

As a result, you cannot declare a script-local function inside another function;
only directly at the script level.

##
# type checking
## What is it?

The parsing step during the compilation of a `:def` function when Vim checks whether:

   - you've specified a type for each function argument
     (not needed for an optional argument; type inferrence can infer a type from the default value)

```vim
vim9script
def Func(x)
enddef
defcompile
```
    E1077: Missing argument type for x

   - you've specified the return type of the function if it returns sth

```vim
vim9script
def Func()
    return 123
enddef
defcompile
```
    E1096: Returning a value in a function without a return type

   - the return type of the function matches the type of the returned expression

```vim
vim9script
def Func(): string
    return 123
enddef
defcompile
```
    E1012: type mismatch, expected string but got number

   - the type of a declared variable matches the type of the expression that you assign to it later

```vim
vim9script
def Func()
    var x: string
    x = 123
enddef
defcompile
```
    E1012: type mismatch, expected string but got number

##
## When is it performed
### for a legacy `:fu` function?

At runtime:
```vim
vim9script
fu Func()
    let s:name = 0
    let s:name = ''
endfu
Func()
```
                         v--------v
    Error detected while processing ...
    E1012: Type mismatch; expected number but got string

But only for script-local variables:
```vim
vim9script
fu Func()
    let name = 0
    let name = ''
endfu
Func()
```
    no error

That makes sense; the concept of declaration  and type only makes sense for Vim9
variables.   A function-local  variable  in  a legacy  function  is  not a  Vim9
variable; it's still a legacy one.

### for a `:def` function?

At compile time:
```vim
vim9script
def Func()
    var name = 0
    name = ''
enddef
Func()
```
                         v-------v
    Error detected while compiling ...
    line    2:
    E1012: Type mismatch; expected number but got string

*And* at runtime:
```vim
vim9script
def Func()
    var name = [0]
    name = [0]->mapnew((_, v) => '')
enddef
Func()
```
                         v--------v
    Error detected while processing ...
    E1012: Type mismatch; expected list<number> but got list<string>

###
## How to postpone it for a `:def` function until runtime?

Whenever you need to specify a type, use `any`:
```vim
vim9script
def Func(x: any)
 #          ^^^
enddef
defcompile
```
    no error
```vim
vim9script
def Func(): any
 #          ^^^
    return 123
enddef
defcompile
```
    no error
```vim
vim9script
def Func()
    var x: any
    #      ^^^
    x = 123
enddef
defcompile
```
    no error

##
## When can I omit the type of a variable?

When you assign it a value, because in that case Vim can infer the type from the latter.

Here, `E1077` is raised because `x` is not assigned a value:
```vim
vim9script
def Func(x)
enddef
defcompile
```
    E1077: Missing argument type for x

Solution: declare the type.
```vim
vim9script
def Func(x: number)
enddef
defcompile
```
    no error

---

Here, no error is raised, because `x` is assigned a default value:
```vim
vim9script
def Func(x = 3)
enddef
defcompile
```
And here again, no error is raised, because `x` is assigned a value:
```vim
vim9script
def Func()
    var x = 3
enddef
defcompile
```
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
## What's the value of a boolean option
### in Vim script legacy?

A boolean *number*:

    :echo getwinvar(winnr(), '&pvw')
    0~

### in Vim9 script?

A *boolean*:

    :vim9 echo getwinvar(winnr(), '&pvw')
    false~

##
## When does Vim use the subtype `<unknown>`?

When it gets an *expression* whose value is an empty list or dictionary.
Because in that case, Vim can't know what its future items (if any) will be.
```vim
vim9script
var d: dict<any>
echo typename(d)
```
    dict<unknown>

Here, `dict<unknown>` is echo'ed even though `d` was declared with `dict<any>`.
That's because  `typename()` doesn't  care about  `d`; it  only cares  about its
value which here is an empty dictionary.

---

Note that  using the subtype `<any>`  would be wrong.  Vim  doesn't know whether
you'll use a mix of values in your list/dictionary.

##
## Why should I specify the types in *all* declarations?

Feeding as much info  as you can to the compiler lets  Vim catch errors earlier,
which makes their resolution easier.

Example:
```vim
vim9script
def Func()
    var lines = getline(1, '$')
        ->map((i, v) => ({text: v}))
    map(lines, (i, v) => lines[i].text =~ '')
enddef
defcompile
```
    E715: Dictionary required

This error looks weird, and is hard to understand.
```vim
vim9script
def Func()
    var lines: list<dict<string>> = getline(1, '$')
        ->map((i, v) => ({text: v}))
    map(lines, (i, v) => lines[i].text =~ '')
enddef
defcompile
```
    E1012: Type mismatch; expected list<dict<string>> but got list<string>

This error is easier to understand, thanks to the explicit type:

    var lines: list<dict<string>> = getline(1, '$')
               ^----------------^

---

Besides, type inferrence might give a problematic type:

    var l = Func()

Suppose `Func()`  returns an  expression of type  `list<number>`, but  later you
need to invoke `extend()`  to include strings inside `l`.  It  will raise a type
mismatch error.

So, instead, you need to write an explicit type:

    var l: list<any> = Func()
           ^-------^

Even if type inferrence gives the right  type now, it doesn't mean it will still
give the right type after a future refactoring.

---

Finally, explicit types let the compiler optimize your code as much as possible.

### Where can I omit a type?

In a guard, because it's useless (you'll never refactor a guard):

    var loaded = true

Also in an optional argument in a  function's header, if the default value is an
"irreducible" scalar:

    def Func(name = 123)
        ...

A scalar is any expression which is not a list/dictionary.
"Irreducible" means that the expression can't be simplified.

In the next  example, `win_getid()` is not irreducible, so  you might still want
to specify the `number` type:

                   v----v
    def Func(name: number = win_getid())
        ...

##
## These 3 very similar snippets give different type error messages:
```vim
vim9script
'' - 1
```
    E1030: Using a String as a Number
```vim
vim9script
def Func()
    '' - 1
enddef
defcompile
```
    E1036: - requires number or float arguments
```vim
vim9script
def Func()
    '' + 1
enddef
defcompile
```
    E1051: Wrong argument type for +

### Why not the same message?

First, the context is different in the  first snippet.  In the latter, the error
occurs at runtime.  In the next snippets, the error occurs at compile time.  Vim
knows more about the  types at runtime than at compile time;  so, it makes sense
that the error messages are different.

Second, `+` has 2 meanings: it can  be used as an arithmetic operator to perform
an addition,  or as a  list concatenation operator.   So, again, it  makes sense
that Vim raises a different error for `+` than for `-`.

See: <https://github.com/vim/vim/issues/7167#issuecomment-714620921>

##
## This snippet raises a type mismatch error:
```vim
vim9script
var d: dict<any> = {a: 0}
extend(d, {b: 0, c: ''})
```
    E1013: Argument 2: type mismatch, expected dict<number> but got dict<any>

### I thought that declaring the dictionary with the type `dict<any>` would avoid this issue.  It doesn't.  Why?

The error is not raised at compile time, but at runtime.
And at runtime, no  function which operates in-place can change  the type of the
items of a composite type value.
This breaks functions such as `extend()`, `flatten()` and `map()`.
Instead, you must use a `*new()` function like `extendnew()`, `flattennew()` or `mapnew()`:
```vim
vim9script
var d: dict<any> = {a: 0}
d = extendnew(d, {b: 0, c: ''})
echo d
```
    {'a': 0, 'b': 0, 'c': ''}

##
## How to get the right type in a declaration without too much thinking/guessing?

First, use `any` so that your code at least compiles.

Then, use `echom typename(name)`  to make Vim print the exact  type of the value
(which is assigned to a variable or returned from a function).

Use this information to replace `any`.

---

Alternatively, you can also replace `any` with a wrong type; e.g. `job`.

You'll get an error such as:

    E1013: Argument 1: type mismatch, expected job but got number

One of the types before or after "but got" will be different than `job`.
If it is:

   - not composite, then use it to replace `job`
   - composite, then replace `job` with `list<job>` or `dict<job>`, and repeat the process

##
## Which pitfall should I be aware of when storing a funcref in a list/dictionary?

It might suppress type checking at compile time:
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
    d = {a: '', b: function('len')}
enddef
defcompile
```
    no error

That's because `function()` is not considered a constant:
<https://github.com/vim/vim/issues/7171#issuecomment-712315593>

Not sure what that means...

### Which issue can it cause?

An error might be shadowed:
```vim
vim9script
def Func()
    var l: list<string>
    l = ['', function('len')]
    l[0] - 1
enddef
defcompile
```
    line 3:
    E1036: - requires number or float arguments

The first error is not this one.  It's:

    line 2:
    E1012: Type mismatch; expected list<string> but got list<any>

The fact that the real first error  is not reported might make debugging harder;
especially when the lines involved are far away from each other:
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
    l[0] - 1
enddef
defcompile
```
##
# Declaration
## What's the difference between "declaring" a variable and "creating" one?

A declaration carries more meaning than a mere creation; in addition to creating
a variable, a  declaration also enforces a  type on the value  that the variable
will be allowed to store for its entire life.

Besides, a  declared variable cannot  be deleted; it will  exist as long  as the
execution is in the context in which it's defined.

##
## Where can I declare a variable?

Only in the Vim9 context.

And for:

   - a script-local variable/function only directly at the script level (i.e. not in a function)
   - a function-local variable/function only directly at a function level (i.e. not in a block)
   - a block-local variable/function only in a block

   - a function argument only in its header;
     a lambda argument only on the left of the `=>` token

### I've found a counterexample!
```vim
def Func()
    s:name = 'I declare that this variable exists'
    echo s:name
enddef
call Func()
```
    I declare that this variable exists

#### What gives?

That's not a counterexample.
You didn't *declare* a variable; you just *created* one.

Watch this:
```vim
def Func()
    s:name = 123
    s:name = "I was a number, but now I'm a string"
    echo s:name
enddef
call Func()
```
    I was a number, but now I'm a string

No error is raised, because there is  no type checking, which means there was no
declaration either.

Don't be confused by the fact that  you're in a `:def` function.  Yes, you're in
the Vim9  context, but that doesn't  matter for a *script*-local  variable.  For
such a variable, what  matters is the script.  Here, the  script is legacy where
there  is  no  concept  of declaration/type  checking.   So,  your  script-local
variable is also legacy, and cannot be declared.

### I've found another counterexample!
```vim
vim9script
fu Func()
    let s:name = 'declared in legacy context'
    echo s:name
endfu
Func()
```
    declared in legacy context

#### What gives?

Yeah, this time, you found one.
It's documented above `:h type-checking`.

But  writing a  legacy function  in a  Vim9 script  is a  corner case,  which is
discouraged in the help:

   > When using `:function` in a Vim9 script file the legacy syntax is used, with
   > the highest |scriptversion|.  However, this can be confusing and is therefore
   > discouraged.

I guess  the purpose of  this exception  is to make  it easier to  copy-paste an
existing legacy function into a new Vim9 script...

###
## I can't create a script-local variable in a :def function.  Isn't this inconsistent with legacy Vim script?

No.  You  cannot simply *create*  a variable in Vim9.   You have to  declare it.
That's a  different mechanism, implemented  with a different keyword  (`:var` vs
`:let`); there's no reason to expect both mechanisms to work the same.

Besides, to declare a script-local variable inside a function, you would have to
prefix its name with  `s:`; otherwise there would be no  way to distinguish them
from function-local variables.  But such prefixes are awkward/ugly when they can
be avoided.

BTW, `b:`, `g:`, `w:`, `t:`, are not awkward/ugly because they can't be avoided.
E.g. there's no equivalent of "current  tab page" in other programming languages
because they're not primarily meant to script an interactive editor.
IOW, Vim9 is a DSL; python/javascript/... are not.

##
## My function fails to be compiled.  One of the declared script-local variable cannot be found!
```vim
vim9script
def Func()
    echo name
enddef
defcompile
var name = 'test'
```
    E1108: Item not found: name

### Why?

Before  a `:def`  function can  be compiled  successfully, all  the script-local
variables which are referred to in its body must have been already declared.

That's because, in a Vim9 script, a script-local variable has a type which needs
to be checked at compile time.  That's only possible if the variable has already
been declared.

### What should I do?

Make  sure  that all  your  script-local  variables  are declared  *before*  the
functions which refer to them are compiled.

Either move the declarations earlier, or delay the compilation.

###
# Comments
## Which comment leader should I write to start a comment in a Vim9 script code?

`#`

    var count = 0  # number of occurences

### Why not the traditional `"`?

It can also be the start of a string, so it can't be used in many places.

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
```vim
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
```
    ['one', 'two']
```vim
def Func()
    var mylist = [
            'one',
            # some comment
            'two',
            ]
    echo mylist
enddef
call Func()
```
    ['one', 'two']
```vim
vim9script
var mylist = [
        'one',
        # some comment
        'two',
        ]
echo mylist
```
    ['one', 'two']

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
```vim
export const MYCONST = 123
```
    E1042: export can only be used in vim9script
```vim
vim9script
export const MYCONST = 123
```
    no error

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
        echo global
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

Note that it keeps working even inside curly brackets:

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
# Differences with legacy
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
var expr = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + 11 + 12 + 13 + 14 + 15
if mode == 'i'
    name_i = expr
else
    name_c = expr
endif
echo s:
```
    {'name_i': 120, 'expr': 120, 'mode': 'i', 'name_c': 0}

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
## Which differences are there between a legacy `s:name` and a Vim9 `name` variable defined at the script level?  (2)

Vim9's `name` has a type (the type of its value can never change); legacy's `name` has no type.

Legacy's `s:name` can be unlet; not Vim9's `name`:
```vim
vim9script
var name = 123
unlet name
```
    E1081: Cannot unlet name

## In Vim9 script, what's the main difference between a `b:`, `g:`, `t:`, `w:`, `$` variable and other variables?

Variables which are prefixed by a prefix denoting a scope can't be declared, but
can be deleted:
```vim
vim9script
var b:name = 123
```
    E1016: Cannot declare a buffer variable: b:name
```vim
b:name = 123
unlet b:name
```
    no error

Variables  which are  *not* prefixed  by a  scope (block-local,  function-local,
script-local) *can* be declared, but can't be deleted.
```vim
vim9script
def Func()
    if 1
        var name = 'block-local'
        unlet name
    endif
enddef
defcompile
```
    E1081: Cannot unlet name
```vim
vim9script
def Func()
    var name = 'function-local'
    unlet name
enddef
defcompile
```
    E1081: Cannot unlet name
```vim
vim9script
var name = 'script-local'
unlet name
```
    E1081: Cannot unlet name

---

See `:h vim9-declaration /unlet`:

   > In Vim9 script `:let` cannot be used.  An existing variable is assigned to
   > without any command.  The same for global, window, tab, buffer and Vim
   > variables, because they are not really declared.  They can also be deleted
   > with `:unlet`.

## How to prevent a variable from being accessible in a later statement?

Put it inside a `{}` block:
```vim
vim9script
def Func()
    {
        var n = 123
    }
    echo n
enddef
defcompile
```
    E1001: variable not found: n

##
## When can the `s:` prefix be omitted?

In front of:

   - a variable name in the Vim9 context
     (script level in Vim9 script, or `:def` function in any type of script)

   - a function name iff its immediate *surrounding* context is Vim9
     (the surrounding context of a function's header is not the header itself)

---

Example showing that  you can omit `s:`  in front of the name  of a script-local
Vim9 function:
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

Similar example for a script-local legacy function:
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

### Why can't there be any ambiguity between function-local / script-local variables even when `s:` is omitted?

Because shadowing is disallowed:
```vim
vim9script
var name = 12
def Func()
    var name = 34
enddef
Func()
```
    E1054: Variable already declared in the script: name

### I can't omit `s:` in this snippet:
```vim
def Func()
    echo name
enddef
defcompile
let s:name = 0
```
    E1001: Variable not found: name

The issue is fixed when I use `s:` inside the `:def` function:
```vim
def Func()
    echo s:name
enddef
defcompile
let s:name = 0
```
    no error

#### Why?

I think allowing `s:` to be omitted would lead to too many issues.

For example, if  you made a typo when  writing the name of a  variable, no error
would be raised at compile time, and  it would be automatically assumed as local
to the script.

BTW, in a legacy script, script-local variables cannot be declared.
So the rule which states that  all script-local variables must have already been
declared is irrelevant here.

IOW, Vim must have some indication that the name indeed refers to a script-local
variable:

   - either because you explicitly prefixed with `s:`
   - or because the name can be found in the script-local scope at the time the
     function is compiled

##
## Which operands are accepted by the logical operators `&&` and `||`?

Only booleans and the numbers 0 and 1.
```vim
vim9script
echo 123 || 0
```
    E1023: Using a Number as a Bool: 123

---

In Vim script legacy, `&&` and `||`  accept any number, as well as strings which
are automatically coerced into numbers.

## Which operators accept any type of value?

`!` and `??`.
```vim
vim9script
echo ![]
echo !{a: 1}
echo [] ?? {} ?? 123
```
    true
    false
    123

## How to use any type of value in a test?

Use the `!` operator twice.  This assumes that you expect any "neutral" value as
false, and all the other ones as true.

I use "neutral" in the mathematical sense of the term.
In maths, `0`  is the neutral element  of the set of real  numbers equipped with
the binary operation `+`. That is, when you  add `0` to any real number, you get
the same number; it doesn't change; so `0` is neutral.

See: <https://en.wikipedia.org/wiki/Identity_element>

Similarly, when you extend  a list with `[]`, you get the same  list, so `[]` is
"neutral".

Anyway, here is an example:
```vim
vim9script
var l = []
def TestList(): string
    if !!l
        return 'the list is NOT empty'
    else
        return 'the list is empty'
    endif
enddef
echo TestList()
l += [0]
echo 'and now ' ..  TestList()
```
    the list is empty
    and now the list is NOT empty

This works because:

   - `!` can handle *any* value as a boolean
   - `!` considers any "neutral" value as falsy, and everything else as truthy
   - the second `!` cancels the first one

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
    true

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

#### Doesn't this contradict the rule that shadowing is disallowed?

No, because it's not a "real" shadowing; you need to write the prefix `g:` for a
global item; thus,  the names are not exactly identical  (`name` != `g:name` and
`Func` != `g:Func`): <https://github.com/vim/vim/issues/7170#issuecomment-712386861>

Besides, we can already do that in Vim script legacy; so this design decision is
consistent.

Finally, no matter which name you choose  for a non-global item, there is always
the  possibility that  it's  already  used in  the  global  namespace; thus,  it
wouldn't make much sense to disallow this type of shadowing.

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
    eval [][0]
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

In a list or dictionary, the usage of whitespace is strict:

   - you *can* write a whitespace after the opening `[` or `{`, and before the closing `]` or `}`

   - you *cannot* write a whitespace before a comma separating two consecutive items,
     nor after a colon separating a key from its value in a dictionary

   - you *must* write a whitespace after a comma separating two consecutive items

Example:

                ok but useless
                v                 v
    var dict = { 'a' : 1 , 'b' : 2 }
                    ^ ^ ^ ^   ^ ^
                    ✘ ✔ ✘ ✔   ✘ ✔

                    ✘ = cannot be written
                    ✔ = must be written

Remove the wrong whitespace:
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
```vim
vim9script
def Func()
    var l = ['aaa', 'bbb', 'ccc', 'ddd']
    range(1, 2)->map('l[v:val]')
    #                ^--------^
    #                    ✘
enddef
Func()
```
    E121: Undefined variable: l

Solution: use a lambda.
```vim
vim9script
def Func()
    var l = ['aaa', 'bbb', 'ccc', 'ddd']
    range(1, 2)->map((_, v) => v)
enddef
Func()
```
---

The issue is due to:

   > The local variables are on the stack  and cannot be accessed outside of the
   > compiled function.

Source: <https://github.com/vim/vim/issues/6401#issuecomment-655071515>

## What's the fastest between
### a lambda and an eval string?

At the moment, an eval string is a bit faster in a `:def` function:

    $ vim -es -Nu NONE -i NONE -U NONE -S <(cat <<'EOF'
        vim9script

        def Lambda()
            var time = reltime()
            range(999999)->map((_, v) => v + 1)
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

    0.623 seconds to run lambdas~
    0.555 seconds to run eval strings~

And at the script level:

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        vim9script

        var time = reltime()
        range(999999)->map((_, v) => v + 1)
        setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run lambdas')

        var _time = reltime()
        range(999999)->map('v:val + 1')
        setline(2, reltime(_time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run eval strings')

        :%p
        qa!
    EOF
    )

    0.596 seconds to run lambdas~
    0.571 seconds to run eval strings~

### a `map()` and a for loop?

Inside a `:def` function, a for loop is significantly faster:

    $ vim -es -Nu NONE -i NONE -U NONE -S <(cat <<'EOF'
        vim9script
        var mylist = pow(10, 6)->float2nr()->range()

        def Lambda()
            var time = reltime()
            map(mylist, (_, v) => v + 1)
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
        map(mylist, (_, v) => v + 1)
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
        var mylistlist = pow(10, 6)->float2nr()->range()->mapnew((_, v) => [0, 0, 0, 0, 0])

        def Lambda()
            var time = reltime()
            map(mylistlist, (_, v) => map(v, (_, w) => w + 1))
            setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run Lambda()')
        enddef
        Lambda()

        def ForLoop()
            var time = reltime()
            var i = 0
            for item in mylistlist
                map(item, (_, v) => v + 1)
                i += 1
            endfor
            setline(2, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run ForLoop()')
        enddef
        ForLoop()

        :%p
        qa!
    EOF
    )

    4.070 seconds to run Lambda()~
    3.286 seconds to run ForLoop()~

The results might  also depend on the size of  the inner lists/dictionaries, and
the type of transformation you perform...

##
## Vim complains that it doesn't know the function-local variable I'm referring to!
```vim
vim9script
def Func()
    if 1
       var n = 123
    endif
    echo n
enddef
defcompile
```
    E1001: variable not found: n

A variable is local to its current block.

Solution:  Declare it *before* the block where it's assigned a value.
```vim
vim9script
def Func()
    var n: number
    if 1
       n = 123
    endif
    echo n
enddef
defcompile
```
This makes  the variable  accessible in  the block where  it's declared  (and in
nested blocks).  Not in outer blocks:
```vim
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
```
    E1001: variable not found: n

### Now it complains about a script-local variable!
```vim
vim9script
def Func()
    echo name
enddef
defcompile
var name = 123
```
    E1050: Item not found: name

Make sure your script-local variable is defined *before* the function – in which
it's referred to – is compiled.
```vim
vim9script
def Func()
    echo name
enddef
var name = 123
defcompile
```
    no error

From `:h fast-functions /prefix`:

   > If the script the function is defined in is Vim9 script, then script-local
   > variables can be accessed without the "s:" prefix.  **They must be defined**
   > **before the function is compiled**.

##
## The line number given in an error message looks wrong!

It's not wrong.

You need to pay attention to the context in which the error is raised:

    Error detected while processing ...:
                                    ^^^
                                    context

Is it raised while processing a file?
Or is it raised while processing a function?

Here is an example where you might find the line number of the error unexpected:
```vim
vim9script
set qftf=QuickFixTextFunc
def QuickFixTextFunc(info: dict<number>): list<any>
    var qfl: list<any>
    qfl = [{}]
    return qfl
enddef
helpg grail
copen
```
    Error detected while processing /proc/2212/fd/11:
    line    8:
    E731: using Dictionary as a String

Instead of line 8, you might have expected line 2, which is the address of:

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

    Error detected while processing /proc/2212/fd/11:
                                    ^--------------^

---

Here's  another example,  where  the  line number  of  the  error looks  correct
immediately:
```vim
set qftf=QuickFixTextFunc
def QuickFixTextFunc(info: dict<number>): list<any>
    var qfl: list<any>
    qfl = true
    return qfl
enddef
helpg grail
copen
```
    Error detected while processing function QuickFixTextFunc:
    line    2:
    E1013: type mismatch, expected list<any> but got bool

Again, let's first explain the error.

It's  simple;  you  declare  a  variable `qlf`  of  type  `list<any>`,  but  you
immediately try  to assign  it a  boolean.  The boolean  type doesn't  match the
expected list type, hence the error.

Now, notice how –  this time – the first line in the  error messages refers to a
function:

    Error detected while processing function QuickFixTextFunc:
                                    ^-----------------------^

## I can't call a `:def` function from a `:fu` one.  The function is not found!
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
    E117: Unknown function: Bar

You forgot the `s:` scope in your legacy function:

    call s:Bar()
         ^^

Fixed code:
```vim
vim9script
fu Foo()
    call s:Bar()
endfu
def Bar()
    echo 'bar'
enddef
Foo()
```
    bar

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
    true

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

##
## I can't use a boolean number where a boolean value is expected!
```vim
vim9script
def Func()
    var b: bool = str2nr('0')
enddef
defcompile
```
    E1012: Type mismatch; expected bool but got number

### Why?

At compile  time, Vim can't  know whether  the output of  `str2nr()` is 0  or 1;
maybe  it can  in  this specific  snippet,  but  not in  the  general case  (the
expression passed to `str2nr()` could be arbitrarily complex).

For more info, see: <https://github.com/vim/vim/issues/7644#issuecomment-757228802>

### OK.  How to work around this pitfall?

Turn the number into a bool with the `?:` operator:
```vim
vim9script
def Func()
    var b: bool = str2nr('0') ? true : false
enddef
defcompile
```
Or with `!!`:
```vim
vim9script
def Func()
    var b: bool = !!str2nr('0')
enddef
defcompile
```
The first workaround is more readable; the second one is less verbose.

###
### But at the script level, there is no issue:
```vim
vim9script
var b: bool = str2nr('0')
```
#### Why?

At the script level, there is no compilation; everything is done at runtime.

At runtime Vim has much more info;  it can evaluate all the expressions and test
their types.  Here, when Vim evaluate  `str2nr('0')`, it sees that the result is
0 which is a valid value for a bool.

### And here, there is no issue either:
```vim
vim9script
def Func()
    var n = 0
    var b: bool = n
enddef
defcompile
```
    no error

#### Why?

It's a special case.

When using `var n = 0` or `var n = 1`, Vim knows that the zero/one could be used
as a bool; a special flag is set on the inferred type to allow `n` to be used as
a bool.

---

If you  explicitly specify the  type `number`, type  inferrence is not  used, no
special flag is set on the type of `n`, and an error is raised as usual:
```vim
vim9script
def Func()
    var n: number = 0
    var b: bool = n
enddef
defcompile
```
    E1012: Type mismatch; expected bool but got number

###
## I can't install a custom Ex command then use it right away in the same function!
```vim
vim9script
def Func()
    com -nargs=1 Cmd echom <args>
    Cmd 123
enddef
Func()
```
    E476: Invalid command: Cmd 123

Use `:exe`; that is, don't write this:

    Cmd 123

But this:

    exe 'Cmd 123'
```vim
vim9script
def Func()
    com -nargs=1 Cmd echom <args>
    exe 'Cmd 123'
enddef
Func()
```
    123

Explanation: When compiling a  function, Vim only knows the  commands which were
defined before.  When it checks the validity  of `:Cmd 123`, it doesn't know yet
about `:Cmd`, therefore an error is raised.

Using `:exe` postpones the check to until the function is executed.
At that time, Vim has full knowledge of all the installed commands.

There are other workarounds, which all  boil down to: "don't execute your custom
Ex  command in  the same  function where  you defined  it".  But  `:exe` is  the
simplest one.

For more info, see: <https://github.com/vim/vim/issues/7618#issuecomment-754089952>

## I can't break a line before after a dictionary at the start of a line and before `->`!
```vim
vim9script
{
   a: 1, b: 2, c: 3
}
   ->setline(1)
```
    E121: Undefined variable: a:

A `{` at the start of a line, and alone on that line, starts a block.
To remove the ambiguity, wrap the dictionary inside parentheses:
```vim
vim9script
({
   a: 1, b: 2, c: 3
})
   ->setline(1)
```
    no error

## I can't copy-paste a legacy function in a Vim9 script.  Suddenly, it gives an `E15` error!

In  a  legacy   function  in  a  Vim9  script,  the   highest  scriptversion  is
automatically used.  From `:h Vim9-script /scriptversion`:

   > When using `:function` in a Vim9 script file the legacy syntax is used, **with**
   > **the highest |scriptversion|**.  However, this can be confusing and is therefore
   > discouraged.

See `:h scriptversion`.  In particular, see `:h scriptversion-2`:

   >  :scriptversion 2
   >       String concatenation with "." is not supported, use ".." instead.
   >       This avoids the ambiguity using "." for Dict member access and
   >       floating point numbers.  Now ".5" means the number 0.5.
```vim
fu Func()
    eval 'a'.'b'
endfu
call Func()
```
    no error
```vim
vim9script
fu Func()
    eval 'a'.'b'
endfu
Func()
```
    E15: Invalid expression: 'a'.'b'

## I can't use a closure in a global command (nor in the replacement of a substitution)!

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

## I can't use `is` to compare any type of operands at the script level, but I can in compiled code!
```vim
vim9script
var x: any
x = ''
eval x is 0
```
    E1072: Cannot compare string with number
```vim
vim9script
def Func()
    var x: any
    x = ''
    eval x is 0
enddef
Func()
```
    no error

### Why the difference?

At the script level, the type *from the value* is used; here `string`.

In compiled code, the type *from the variable* is used; here, it's `any`.
The assignment with a value isn't used there.

   > It's very hard to change this  without introducing other problems. We could just
   > accept any two types for "is", but then a comparison that will always fail won't
   > generate an error. Since "is" is usually  used to compare identity between Lists
   > or  Dicts,  I  think  it's  more  useful  to  give  the  error  than  to  permit
   > everything. So let's leave it as is, even though it might seem inconsistent.

##
# Todo
## To document:
### ?

Since 8.2.2527, an error is raised when a lambda is used at the script level and
it refers to a function which is defined later:
```vim
vim9script
var Foo = () => Bar()
def Bar()
enddef
defcompile
```
    E117: Unknown function: Bar

The same code doesn't raise any error if the lambda is refactored into a `:def` function:
```vim
vim9script
def Foo()
    Bar()
enddef
def Bar()
enddef
defcompile
```
    no error

In practice, the solution is usually to move the funcrefs assignment at the end of the script:
```vim
vim9script
def Bar()
enddef
var Foo = () => Bar()
defcompile
```
    no error

Bug?

Update: Not a bug.  I  think it's just a consequence of  the rule which requires
that  all  script-local items  have  already  been declared/defined  before  the
compilation.

### ?

   - `:h vim9-lambda-arguments`
   - `:h vim9-ignored-argument`

Also:

    /Test_ignored_argument()
    ~/Vcs/vim/src/testdir/test_vim9_func.vim

---

Also:

   > For an unpack assignment the underscore can be used to ignore a list item,
   > similar to how a function argument can be ignored: >
   >         [a, _, c] = theList
   >         [a, b; _] = longList

---

Document that we should never write `..._` instead of a `_, _` (or more).
Because it makes you  lose information.  That is, if you do  that, you no longer
know whether the arguments `..._` are really optional.

Also, that's what Vim does in its tests.

---

Look for these patterns:

    \C\<def\>.*\%(_\|\<any\>\)
    \[.*_.*=

Make sure we've used these new syntaxes whenever possible.
And that we did so correctly.

### ?

   > Global functions must be prefixed with "g:" when defining them, but can be
   > called without "g:".
   >         vim9script
   >         def g:GlobalFunc(): string
   >           return 'text'
   >         enddef
   >         echo GlobalFunc()

###
### ?
```vim
vim9script
def Callback(_j: job, _e: number)
    echom 'callback'
enddef
def Func()
    job_start(['/bin/bash', '-c', ':'], {exit_cb: function('Callback')})
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
    job_start(['/bin/bash', '-c', ':'], {exit_cb: Callback})
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
#### ?

But why does this work?
```vim
vim9script
def Callback(...l: list<any>)
    echom 'callback'
enddef
popup_create('', {callback: function('Callback')})
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
popup_create('', {filter: function('Filter')})
feedkeys('j')
```
    E117: Unknown function: Filter

If the previous explanation was true, shouldn't this snippet work?
Maybe the difference is somehow explained by  the fact that a filter function is
not processed  in the same  context as a callback.   It's processed in  the same
context as a mapping; i.e. outside any script.

Bottom line: It is not always obvious whether  `s:` can be omitted in front of a
function name.  You'll have to learn by trial and error.
However, you should be able to avoid  these issues if you omit the quotes around
the function name (you can also omit `function()`, unless you need a partial).

---

Update: Now that I think about it a little more, I think it's a bug.
Vim9 should be smart enough to assume `s:` when it's missing.

Besides, if you press `C-c`, then the callback function won't be found either:
```vim
vim9script
def Popup()
    var id = popup_menu(['aaa', 'bbb', 'ccc'], {
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
```
    E117: Unknown function: Callback

Same issue if the filter function cannot be found:
```vim
vim9script
def Popup()
    var id = popup_menu(['aaa', 'bbb', 'ccc'], {
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
```
    E117: Unknown function: Filter
    E117: Unknown function: Callback

Notice how  – this time  – an  error is also  raised for the  callback function.
It's because of the previous error  caused by the filter function which couldn't
be found.

---

BTW, try to be consistent when using the `s:` prefix.
That is, if for some reason, you have to use it in front of the name of an item,
you might need to do it for all the occurrences of this item.
Otherwise, pressing  `C-]` on a  reference of this item  might fail to  make Vim
jump to its definition/declaration.
```vim
vim9script
def Func()
enddef
var Ref = function('s:Func')
 #                    ^--^
 #                  if you press `C-]`:
 #                  Vim(tag):E426: tag not found: s:Func
 #                  that's because `Func()` is defined without `s:` in its header
```
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
def MyFunction(n: number, s: string): string
    return repeat(s, n)
enddef
var Funcref: func(number, string): string = MyFunction
```
    no error
```vim
vim9script
def MyFunction(n: number, s: string): number
    return repeat(s, n)
enddef
var Funcref: func(number, string): string = MyFunction
```
    E1012: Type mismatch; expected number but got string

But the second bold sentence seems wrong:
```vim
vim9script
def MyFunction(n: number, s: string): string
    return repeat(s, n)
enddef
var Funcref: func(number, string): number = function('MyFunction')
```
    E1012: Type mismatch; expected func(number, string): number but got func(number, string): string
                                                                    ^^^                     ^------^

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
    E700: Unknown function: MyFunction

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
    yes

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

####
### a lambda does not ignore an unexpected argument
```vim
vim9script
var Ref = () => 'no error'
echo Ref('optional')
```
    E118: Too many arguments for function: <lambda>1

That's a difference from legacy Vim script:
```vim
let Ref = {-> 'no error'}
echo Ref('optional')
```
    no error

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

### a function-local function is implemented as a lambda function

At least,  that's what  it seems  when reading  an error  message raised  from a
function-local function:
```vim
vim9script
def Func()
    def Nested()
        [][0]
    enddef
    Nested()
enddef
Func()
```

    Error detected while processing command line
    ..script /proc/17649/fd/11[8]
    ..function <SNR>1_Func[4]
    ..<lambda>1:
      ^-------^

It's not a bug and it can't be fixed.
The concept of function local to another function didn't exist in Vim script legacy.
A function-local function can't have a public name like "Nested".
It would mean that you can invoke it from anywhere, like the command-line.
That's not possible.

Fortunately, that's not an issue for `vim-stacktrace`.
That's because we can still retrieve the definition site of such a function:

    " still works
    :verb function <lambda>123

### use the script-local namespace when you need to access a function-local variable from the global context

"Global context" = `:s`, `:g`, `:*do`, `win_execute()` ...

This was not an issue in Vim script legacy:
```vim
fu Func()
    let name = 'set in function'
    g/^/echo name
endfu
call Func()
```
    set in function

But this no longer works in Vim9:
```vim
vim9script
def Func()
    var name = 'set in function'
    g/^/echo name
enddef
Func()
```
    E121: Undefined variable: name

Because:

   > It is simply not possible to access the compiled code and variables from interpreted code.

Source: <https://github.com/vim/vim/issues/7541#issuecomment-751274709>

Solution: use a script-local variable:
```vim
vim9script
var name: string
def Func()
    name = 'set in function'
    g/^/echo name
enddef
Func()
```
    set in function

See: <https://github.com/vim/vim/issues/7541#issuecomment-751285484>

### to write an octal number, you need the prefix `0o`
```vim
vim9script
echo 0o7
echo 0o10
echo 0o17
echo 0o20
echo 0o177
echo 0o200
```
    7
    8
    15
    16
    127
    128

See `:h octal` and `:h scriptversion-4`.

This matters for the third argument of `mkdir()`, which is parsed as an octal number.

### `silent!` can only suppress an error at runtime, NOT at compile time
```vim
vim9script
silent! invalid
```
    ✔
```vim
vim9script
def Func()
    silent! invalid
enddef
Func()
```
    E476: Invalid command: invalid

### `silent!` cannot always suppress a thrown error

Sometimes, it can:
```vim
vim9script
def Func()
    throw 'error'
enddef
sil! Func()
```
    ✔

Sometimes, it cannot:
```vim
vim9script
au TerminalWinOpen * sil! Func()
def Func()
    throw 'error'
enddef
try
    term
catch /E123/
endtry
```
    E605: Exception not caught: error

See:

- <https://github.com/vim/vim/issues/7672>
- <https://github.com/vim/vim/issues/7682#issuecomment-761183658>

### don't write this:  "com Cmd exe Func()"
```vim
vim9script
def Func(): string
    [][123]
    return ''
enddef
com Cmd exe Func()
Cmd
```
    E684: list index out of range: 123
    E1050: Colon required before a range: 0

The extra error is noise/confusing.

---

This technique is used  by tpope to make his commands  behave like Vim's builtin
commands:

    com Cmd exe Func()
    def Func(): string
        ...
        if issue
            return 'echoerr ' .. string(v:exception)
        endif
        ...
        return ''
    enddef

That is, when the command encounters an issue, an error is given, yes, but there
is no multiline stacktrace.

But it looks like a hack, and cause the aforementioned issue.
It's better to use an `Error()`  utility function which `:echom` the message, if
you don't want a stacktrace; or `:echoerr` if you do want one.

---

Update: Actually, there is a way to keep using this trick without the issue:

    com Cmd exe ':' .. Func()
                ^----^

Note that,  if an error is  raised and the  function returns 0, the  cursor will
jump on the first line.

### workarounds to unlet a script-local variable

If you  use a script-local  variable as some sort  of cache, and  you're worried
that it  might consume too  much memory,  you can simply  reset the cache  to an
empty value (list, dictionary, blob...).

Otherwise,  if you  really want  the reference  not to  exist anymore,  the only
workaround I  can think  of is to  turn your variable  into a  dictionary's key.
Then, when you want to delete the reference, remove the key from the dictionary.

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

    const SID = execute('fu Opfunc')->matchstr('\C\<def\s\+\zs<SNR>\d\+_')

You might need this in some  circumstances; typically where you write code which
is not run in the context of the script, and when you can't use a funcref.
As an example, when you set the `'opfunc'` option.

##
## In the future, check that a failed `:import` aborts the sourcing of a script

Once this todo item is fixed (`:h todo /abort`):

   > - Error in any command in "vim9script" aborts sourcing.

### Should we use a try conditional for some of our imports, and bail out when they fail?

Because if  an import fails,  there might be no  guarantee that the  script will
work as expected.

For example:

    try
        import Func from 'script.vim'
    catch /^Vim\%((\a\+)\)\=:E\%(1048\|1053\):/
        echohl ErrorMsg
        unsilent echom 'Could not import "Func()" from "script.vim"'
        echohl NONE
        finish
    endtry

---

`E1048` matches this error:

    E1048: Item not found in script: Func

`E1053` matches this error:

    E1053: Could not import "script.vim"

---

`:unsilent` is necessary in case your script is loaded from a filetype plugin.
Because in that case, messages are silent.

---

For a real example, see what we did in:

    ~/.vim/plugged/vim-repmap/autoload/repmap/make.vim

---

Alternatively, we could prefix all `:import` with `silent!`, but I don't like that.
We would also need to prefix any command which uses an imported item with `silent!`.
That's  too much.   Also, when  your  code contains  a bug,  `silent!` can  make
debugging harder, because it can hide the real cause of an issue.

