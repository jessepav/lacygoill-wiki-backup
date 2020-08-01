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
    Error detected while processing function Func:~
    line    1:~
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
    Error detected while processing function Func:~
    line    2:~
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

>     When referring to a function and no "s:" or "g:" prefix is used, Vim will
>     search for the function in this order:
>     - Local to the current scope and outer scopes up to the function scope.
>     - Local to the current script file.
>     - Imported functions, see `:import`.

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
```vim
vim9script
def Inner()
    echo 'script level'
enddef
def Outer()
    def Inner()
        echo 'local to Outer()'
    enddef
    Inner()
enddef
Outer()
```
    script level

TODO: The output should be `local to Outer()`.  Probably a bug.
Revisit this snippet if this issue is fixed: <https://github.com/vim/vim/issues/6586>
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
Func()
```
script level

This shows that Vim searches for a  function in the script *before* searching in
the imported ones.   It doesn't matter whether the function  at the script level
is legacy or not.

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

>     In Vim9 script, script-local functions are defined once when the script is sourced
>     and cannot be deleted or replaced.

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

>     - Implement "as Name" in "import Item as Name from ..."

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

>     Global, window, tab, buffer and Vim variables can only be used
>     without `:let`, because they are are not really declared, they can also be
>     deleted with `:unlet`.

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

>     Comparators ~
>
>     The 'ignorecase' option is not used for comparators that use strings.

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
## When I try to assign a value to a list or a dictionary, `E696` is raised!
```vim
vim9script
let l = [1 , 2 , 3]
```
    E696: Missing comma in List: , 2, 3]

You can no longer separate a list or dictionary item from the next comma with whitespace.

    let l = [1 , 2 , 3]
              ^   ^
              ✘   ✘

Remove the whitespace:
```vim
vim9script
let l = [1, 2, 3]
```
    ✔

This requirement was introduced in 8.2.1326.

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

    Error detected while processing function <SNR>1_Func:~
    line    2:~
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

    Error detected while processing function <SNR>1_Func:~
    line    2:~
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

>    The local variables are on the stack  and cannot be accessed outside of the
>    compiled function.

Source: <https://github.com/vim/vim/issues/6401#issuecomment-655071515>

## I hesitate between writing a lambda and an eval string.  Which one is the fastest?

Inside a `:def` function, lambdas are significantly faster:

    $ vim -es -Nu NONE -S <(cat <<'EOF'
        vim9script

        def Lambda()
            let time = reltime()
            map(range(999999), {_, v-> v + 1})
            setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run lambdas')
        enddef
        Lambda()

        def EvalString()
            let time = reltime()
            map(range(999999), 'v:val+1')
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
        map(range(999999), {_, v-> v + 1})
        setline(1, reltime(time)->reltimestr()->matchstr('.*\..\{,3}') .. ' seconds to run lambdas')

        let _time = reltime()
        map(range(999999), 'v:val+1')
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

    Error detected while processing function <SNR>1_Func:~
    line    4:~
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

    Error detected while processing function <SNR>1_Func:~
    line    7:~
    E1001: variable not found: n~

### Now it complains about a script-local variable!

    vim9script
    def Func()
        echo s:var
    enddef
    defcompile
    s:var = 123

    Error detected while processing function <SNR>1_Func:~
    line    1:~
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

>     If the script the function is defined in is Vim9 script, then script-local
>     variables can be accessed without the "s:" prefix.  **They must be defined**
>     **before the function is compiled**.

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

    Error detected while processing function <SNR>1_Foo:~
    line    1:~
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
# Todo
## Refactor all eval strings into lambdas.

But make sure they're inside a `:def` function first.
Don't worry, a lambda in a `:def` function is not slower than an eval string; on
the contrary, it's faster.

    :vim /v:val/gj $MYVIMRC ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/**
    :Cfilter! -other_plugins

## How to change the type of a variable?

    vim9script
    let time = reltime()
    sleep 1
    let time = reltime(time)->reltimestr()->matchstr('.*\..\{,3}')
    echom printf('we slept for %s seconds', time)

    Error detected while processing /proc/9723/fd/11:~
    line    4:~
    E1041: Redefining script item time~

---

For the moment, the only workaround I can think of, is to use an extra variable:

    vim9script
    let time = reltime()
    sleep 1
    let _time = reltime(time)->reltimestr()->matchstr('.*\..\{,3}')
    echom printf('we slept for %s seconds', _time)

## Try to finish rewriting `ccomplete#Complete()` in Vim9 script.

    ~/.vim/autoload/ccomplete.vim

Test:

    $ vim ~/Vcs/vim/src/evalfunc.c
    " press:  gg O e C-x C-o
                   ^
                   inserted text: don't write too much; it could prevent some functions
                   from being invoked (we want to test as many functions as possible)

---

<https://vi.stackexchange.com/questions/26406/how-does-ft-c-omni-work-and-how-can-i-make-it-faster>

## Try to move all our library functions (`vim-lg`) into an `import/` subdirectory.

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

##
## To document:
### cannot redefine a script-local or block-local or imported function

Wait for these issues to be fixed before documenting this:

- <https://github.com/vim/vim/issues/6581>
- <https://github.com/vim/vim/issues/6583>

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

Wait for this issue to be fixed before documenting this:

<https://github.com/vim/vim/issues/6582>

### imported items are local to the script

This is suggested at `:h vim9-scopes`:

>     The result is that functions and variables without a namespace can always be
>     found in the script, either defined there or imported.

---

    imported constant
```vim
vim9script
let lines =<< trim END
    vim9script
    export const s:MYCONST = 123
END
writefile(g:lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import MYCONST from 'foo.vim'
echo s:MYCONST
```
    123

---

    imported variable
```vim
vim9script
let lines =<< trim END
    vim9script
    export let s:var = 123
END
writefile(g:lines, '/tmp/import/foo.vim')
set rtp+=/tmp
import var from 'foo.vim'
echo s:var
```
    123

---

    imported function
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
```
       def <SNR>2_Imported()
    1      echo 'imported'
       enddef

