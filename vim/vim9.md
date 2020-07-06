# Where can I write Vim9 script code?  (2)

In a function defined with the `:def` command (instead of `:function`).

Or, in a file whose first command is `:vim9script`.

##
# Which comment leader should I write to start a comment in a Vim9 script code?

`#`

    let count = 0  # number of occurences

## Why not the traditional `"`?

It can also be the start of a string, so it can't be used in many places.

## Which pitfall should I avoid?

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
# `:def`
## Why is a `:def` function compiled?

So that its execution is faster.
In practice, it's often 10 to 100 times faster.

You can't get that kind of performance with a `:fu` function.

### When is it compiled?

When the  function is  first called,  or when `:defcompile`  is executed  in the
script where the function is defined.

##
# Pitfalls
## Vim unexpectedly close the current window when I invoke a function where I omit to declare an `x` variable!

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
# Todo
## Document that you need to declare the type of a function argument.

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(x)
        enddef
        defcompile
    EOF
    )

    Error detected while processing /proc/22267/fd/11:~
    line    2:~
    E1077: Missing argument type for x~
    line    3:~
    E193: :enddef not inside a function~

Exception: You don't need to if it's an optional argument; because in that case,
you need to assign it a default value, and Vim can infer a type from the latter.

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func(x = 3)
        enddef
        defcompile
    EOF
    )

---

You may find this unexpected.  After all,  you don't need to declare the type of
all your variables in a `:def` function:

    vim -Nu NONE -S <(cat <<'EOF'
        vim9script
        def Func()
            let x = 1
        enddef
        defcompile
    EOF
    )

But that's because  – again – you  assign values to your variables,  and Vim can
use them to infer their type.  See `:h type-inference`.

Bottom line: Without a value, Vim *needs* a type.

## Document the Vim9 equivalent of `let x = get(a:, 1, 3)`

It's:

    def Func(x = 3)
             ^---^

Remember that an argument can be specified in 3 ways:

    {name}: {type}
    {name} = {value}
    {name}: {type} = {value}

The first one is for mandatory arguments; the last two for optional ones.
