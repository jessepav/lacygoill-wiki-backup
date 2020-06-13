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

You can't get that kinf of performance with a `:fu` function.

### When is it compiled?

When the  function is  first called,  or when `:defcompile`  is executed  in the
script where the function is defined.

##
# Issues
## a Vim9 comment must start with a space to be correctly highlighted

     # some comment
    ^
    there must be at least one space before '#'

The issue comes from `$VIMRUNTIME/syntax/vim.vim:632`:

    syn match   vim9LineComment +^[ \t:]\+#.*$+ contains=@vimCommentGroup,vimCommentString,vimCommentTitle
                                        ^^
                                        should be '*'

It looks like a  bug, because there is nothing in the  help which documents this
requirement.  And if `#` is not preceded  by a space, the line is still ignored;
meaning that Vim does not need a space before `#` to correctly parse the line as
a comment.

## cannot use a bar

Source this:

    def! Func()
        let x = 123
        redraw! | echo x
    enddef
    call Func()
    Error detected while processing function Func:~
    line    1:~
    E121: Undefined variable: x~

