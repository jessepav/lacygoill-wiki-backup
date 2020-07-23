# :def
## Why is a `:def` function compiled?

So that its execution is faster.
In practice, it's often 10 to 100 times faster.

You can't get that kind of performance with a `:fu` function.

### When is it compiled?

When the  function is  first called,  or when `:defcompile`  is executed  in the
script where the function is defined.

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
## What's the default scope of
### a function?

It's local to the current script.

    vim9script
    def Func()
        echo expand('<sfile>')
    enddef
    Func()

    function <SNR>1_Func~
             ^-----^

### a *nested* function?

It's local to the outer function.

    vim9script
    def FuncA()
        def FuncB()
        enddef
    enddef
    FuncB()

    E117: Unknown function: FuncB~

    vim9script
    def FuncA()
        def FuncB()
        enddef
        FuncB()
    enddef
    FuncA()
    ✔

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
   - functions
   - classes

## How to export one item?

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

## How to export several items in a single command?

First, define them as usual.
Then,  export  all of  them  after  wrapping  them  inside curly  brackets,  and
separating them with commas:

    vim9script

    const MYCONST = 123
    let var = 'test'
    def Func()
        # ...
    enddef

    export {MYCONST, var, Func}
           ^------------------^

Note: It doesn't work at the moment:

    E1043: Invalid command after :export~

Probably a bug, or the feature has not been implemented yet.

##
## On which condition can I export items in a script?

The script must start with `:vim9script`.

    export const MYCONST = 123

    E1042: export can only be used in vim9script~

    vim9script
    export const MYCONST = 123
    ✔

## On which condition can I import items from a script?

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

Rarely if ever.

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
anymore; it's implicit:

    " legacy
    let s:var = 123
    fu s:Func()
    endfu

    " Vim9
    vim9script
    let var = 123
    def Func()
    enddef

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

1

    echo 123 || 0

    1~

### Vim9 script?

123

    vim9script
    echo 123 || 0

    123~

##
# Pitfalls
## My `:def` function raises `E488`.  I don't understand why!

Maybe you have a folding marker at the end of the `:def` line:

    vim9script
    def Func() #{{{1
    enddef
    defcompile

    E488: Trailing characters~

If so, make sure you specify a return type.  Use `void` if the function does not
return anything:

    vim9script
    def Func(): void #{{{1
    enddef
    defcompile

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

## Vim unexpectedly close the current window when I call a function where I omit to declare an `x` variable!

`x` is a valid Ex command (it's the abbreviated form of `:xit`).
So this is expected:

    vim9script
    def Func()
        x = 1
    enddef
    Func()

Solution: don't forget to declare your variable:

    vim9script
    def Func()
        let x = 1
    enddef
    Func()

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
    " press:  gg O e_a C-x C-o

---

<https://vi.stackexchange.com/questions/26406/how-does-ft-c-omni-work-and-how-can-i-make-it-faster>

---

There is an issue with a Vim9 fold marker:

    #{{{1

It breaks the syntax highlighting of everything which comes afterward.
I think it has to do with `:h literal-Dict`.
Workaround:

    # {{{1
     ^
     add a space

Report, document, integrate, ...

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

