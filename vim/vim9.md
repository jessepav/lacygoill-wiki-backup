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

        vim -Nu NONE -S <(cat <<'EOF'
            def Func(x)
            enddef
            defcompile
        EOF
        )

        E1077: Missing argument type for x~

   - you've specified the return type of the function if it returns sth

        vim -Nu NONE -S <(cat <<'EOF'
            def Func()
                return 123
            enddef
            defcompile
        EOF
        )

        E1096: Returning a value in a function without a return type~

   - the return type of the function matches the type of the returned expression

        vim -Nu NONE -S <(cat <<'EOF'
            def Func(): string
                return 123
            enddef
            defcompile
        EOF
        )

        E1013: type mismatch, expected string but got number~

   - the type of a declared variable matches the type of the expression that you assign it later

        vim -Nu NONE -S <(cat <<'EOF'
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

    vim -Nu NONE -S <(cat <<'EOF'
        def Func(x: any)
        #         ^---^
        enddef
        defcompile
    EOF
    )

    vim -Nu NONE -S <(cat <<'EOF'
        def Func(): any
        #         ^---^
            return 123
        enddef
        defcompile
    EOF
    )

    vim -Nu NONE -S <(cat <<'EOF'
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

    vim -Nu NONE -S <(cat <<'EOF'
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
## Where can't I use `"` as a comment leader?

When you're writing an *inline* comment inside a `:def` function.

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let x = 1 " Error!
        enddef
        defcompile
    EOF
    )

    Error detected while processing function <SNR>1_Func:~
    line    1:~
    E488: Trailing characters: " Error!~

Instead, you must use `#`:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let x = 1 # works
            #         ^-----^
        enddef
        defcompile
    EOF
    )

Note that this limitation does *not* apply to the function header:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(): void "{{{1
        #                ^
        #                ✔
        enddef
        defcompile
    EOF
    )

##
# Misc
## Where can I write Vim9 script code?  (2)

In a function defined with the `:def` command (instead of `:function`).

Or, in a file whose first command is `:vim9script`.

## When can I omit the type of a variable?

When you assign it a value, because in that case Vim can infer the type from the latter.

Here, `E1077` is raised because `x` is not assigned a value:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(x)
        enddef
        defcompile
    EOF
    )

    E1077: Missing argument type for x~

Solution: declare the type.

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(x: number)
        enddef
        defcompile
    EOF
    )

But this time, no error is raised, because `x` is assigned a default value:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(x = 3)
        enddef
        defcompile
    EOF
    )

And here again, no error is raised, because `x` is assigned a value:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let x = 3
        enddef
        defcompile
    EOF
    )

See `:h type-inference`.

##
# Pitfalls
## My `:def` function raises `E488`.  I don't understand why!

Maybe you have a folding marker at the end of the `:def` line:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func() #{{{1
        enddef
        defcompile
    EOF
    )

    E488: Trailing characters~

If so, make sure you specify a return type.  Use `void` if the function does not
return anything:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(): void #{{{1
        enddef
        defcompile
    EOF
    )

## If I specify the return type of a custom function, what should I pay attention to?

If your function  returns a variable, make  sure that it was set  with the exact
same type:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(): list<string>
        #           ^----------^
            let l = []
        #   ^--------^
        #   ✘
            return l
        enddef
        defcompile
    EOF
    )

    Error detected while processing function <SNR>1_Func:~
    line    2:~
    E1013: type mismatch, expected list<string> but got list<any>~

The error probably comes from the fact that when Vim parses this line:

    let l = []

it probably infers the type `list<any>`.

Fix:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(): list<string>
            let l: list<string> = []
            #    ^------------^
            #          ✔
            return l
        enddef
        defcompile
    EOF
    )

## Vim unexpectedly close the current window when I call a function where I omit to declare an `x` variable!

`x` is a valid Ex command (it's the abbreviated form of `:xit`).
So this is expected:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            x = 1
        enddef
        Func()
    EOF
    )

Solution: don't forget to declare your variable:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let x = 1
        enddef
        Func()
    EOF
    )

##
## My eval string can't access variables in the outer function scope!

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let l = ['aaa', 'bbb', 'ccc', 'ddd']
            range(1, 2)->map('l[v:val]')
            #                ^--------^
            #                    ✘
        enddef
        Func()
    EOF
    )

    Error detected while processing function <SNR>1_Func:~
    line    2:~
    E121: Undefined variable: l~

Solution: use a lambda.

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let l = ['aaa', 'bbb', 'ccc', 'ddd']
            range(1, 2)->map({_,v -> v})
        enddef
        Func()
    EOF
    )

---

The issue is due to:

>    The local variables are on the stack  and cannot be accessed outside of the
>    compiled function.

Source: <https://github.com/vim/vim/issues/6401#issuecomment-655071515>

## I hesitate between writing a lambda and an eval string.  Which one is the fastest?

Inside a `:def` function, lambdas are significantly faster:

    vim -es -Nu NONE -S <(cat <<'EOF'
        vim9script

        def Lambda()
            let time = reltime()
            map(range(999999), {_,v-> v + 1})
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

    vim -es -Nu NONE -S <(cat <<'EOF'
        vim9script

        let time = reltime()
        map(range(999999), {_,v-> v + 1})
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

Conclusion: always use lambdas, but make to write them inside `:def` functions.

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

    vim -Nu NONE -S <(cat <<'EOF'
        set qftf=QuickFixTextFunc
        def QuickFixTextFunc(info: dict<number>): list<any>
            let qfl: list<any>
            qfl = [{}]
            return qfl
        enddef
        helpg grail
        copen
    EOF
    )

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

    vim -Nu NONE -S <(cat <<'EOF'
        set qftf=QuickFixTextFunc
        def QuickFixTextFunc(info: dict<number>): list<any>
            let qfl: list<any>
            qfl = v:true
            return qfl
        enddef
        helpg grail
        copen
    EOF
    )

    Error detected while processing function QuickFixTextFunc:~
    line    2:~
    E1013: type mismatch, expected list<any> but got bool~

Again, let's first explain the error.

It's  simple;  you  declare  a  variable `qlf`  of  type  `list<any>`,  but  you
immediately try  to assign  it a  boolean.  The boolean  type doesn't  match the
expected list type, hence the error.

Now, notice how –  this time – the first line in the  error messages refers to a
function:

    Error detected while processing function QuickFixTextFunc:
                                    ^-----------------------^

##
# Todo
## Refactor all eval strings into lambdas.

But make sure they're inside a `:def` function first.
Don't worry, a lambda in a `:def` function is not slower than an eval string; on
the contrary, it's faster.

    vim /v:val/gj  $MYVIMRC ~/.vim/**/*.vim ~/.vim/**/*.snippets ~/.vim/template/**
    Cfilter! -other_plugins

## How to change the type of a variable?

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let time = reltime()
        sleep 1
        let time = reltime(time)->reltimestr()->matchstr('.*\..\{,3}')
        echom printf('we slept for %s seconds', time)
    EOF
    )

    Error detected while processing /proc/9723/fd/11:~
    line    4:~
    E1041: Redefining script item time~

---

For the moment, the only workaround I can think of, is to use an extra variable:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        let time = reltime()
        sleep 1
        let _time = reltime(time)->reltimestr()->matchstr('.*\..\{,3}')
        echom printf('we slept for %s seconds', _time)
    EOF
    )

## Document that some single-letter variable names can't be used in a declaration inside a `:def` function

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let w: number
        enddef
        defcompile
    EOF
    )

    Error detected while processing function <SNR>1_Func:~
    line    1:~
    E1016: Cannot declare a buffer variable: b~

Same thing for `g`, `s`, `t` and `w`.
Also for `v`, although the error message is a bit different:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let v: number
        enddef
        defcompile
    EOF
    )

    Error detected while processing function <SNR>1_Func:~
    line    1:~
    E1001: variable not found: v: number~

Btw, maybe Vim should raise a more telling error message.
It's not clear what's wrong.
This would be more clear:

    E1234: Cannot declare a variable whose name matches a valid variable scope~

Well, maybe not that *exact* message, but sth similar.  You get the idea.
Report?

## Try to finish rewriting `ccomplete#Complete()` in Vim9 script

    vim +'so ~/Desktop/ccomplete.vim' ~/Vcs/vim/src/evalfunc.c

Right now, we can't go any further because of: <https://github.com/vim/vim/issues/6434>

